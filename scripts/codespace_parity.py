#!/usr/bin/env python
"""codespace_parity.py -- "a Codespace lane works" as a repository check, not a lifecycle that
merely completed (`[#1335]`; `to-browser/CODESPACE-PARITY-DEFINITION-2026-10-03.md`; lane
foundation-5-codespace-parity, batch FOUNDATION).

WHAT IT ANSWERS. One real task, run once in a local worktree and once in a Codespace from the same
base sha, must agree on five conditions. This script builds the evidence for each in the
environment it runs in (`collect`), compares two such records (`check`), and prints ONE verdict per
condition -- `PASS`, `FAIL`, or `NOT-RUN <reason>` -- with the two values compared as evidence:

    1 environment   Python, `uv`, the `uv.lock` hash, `uv sync --locked` exit, the versions of the
                    tools a lane needs (`claude`, `gh`, `codex`, `agy`), the installed git-hook
                    set -- identical except the OS-specific entries declared below, in code.
    2 gates         a FIXED set of pre-commit hooks, `audit.py health` and a FIXED pytest
                    selection, same verdict on both sides or a declared OS case with its own row.
    3 landing       same base sha and tree; the Codespace's pushed branch resolves to its HEAD.
                    The integrator leg (local `--no-ff` merge + the CI push verdict) is NOT-RUN:
                    a lane cannot merge, and a check that printed PASS for a leg nobody ran would
                    be the vacuous pass this file exists to refuse.
    4 transport     the Codespace reads the Drive transport by rclone (the secret is checked for
                    PRESENCE only, never read into a record). The write leg is NOT-RUN: a write
                    probe would create a transport path no contract names.
    5 cleanup/cost  after teardown no Codespace is listed and no run branch is on origin; wall
                    time and core-hours are recorded (`codespace_regime.uptime_minutes`, the one
                    uptime formula).

THE NO-VACUOUS-PASS RULE (R59). A Codespace that cannot be created, reached or read, or whose
record is empty, unparseable, the wrong shape, or claims to be the local side (two local records
compared would be green by construction), is a typed failure -- exit 3, `FAILURE
RemoteUnavailable: <why>` -- and every condition prints `NOT-RUN`. No condition that needed the
remote side can print a green verdict. Exit codes: 0 all PASS | 1 at least one FAIL | 2 no FAIL,
at least one NOT-RUN | 3 remote side unavailable | 4 local record unusable.

WHERE THE CODESPACE DRIVER LIVES. Two drivers exist and this file moves neither: win-tooling's
`Dispatch-Codespace` (outside the hub) and the hub's `scripts/dispatch.py` `codespace-*` verbs
(R11(3)). This check needs no agent, so the run is plain `gh codespace create / cp / ssh / delete`;
the only remote read is `gh codespace ssh ... cat` (measured: `cp` has failed this transport three
ways, `cat` fails visibly).

PRIOR-ART CHECK (library-first). stdlib (`json`, `hashlib`, `subprocess`, `xml.etree` for the
pytest junit file) plus the already-declared `click`; `pre-commit` and `pytest` are the existing
runners; `codespace_regime.uptime_minutes` is reused for cost. No new dependency, no new runner.

    uv run --locked python scripts/codespace_parity.py collect --out record.json [--push-branch B]
    uv run --locked python scripts/codespace_parity.py check --local l.json --remote r.json
    uv run --locked python scripts/codespace_parity.py check --local l.json --codespace NAME
    uv run --locked python scripts/codespace_parity.py verify-cleanup --codespace NAME ...
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence

import click

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import codespace_regime as _regime
except ImportError:  # pragma: no cover
    import codespace_regime as _regime

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("codespace-parity")

SCHEMA = 1

#: The Codespace side's record, where `collect` writes it and `check --codespace` reads it.
DEFAULT_REMOTE_FILE = "/tmp/parity-remote.json"

# ============================================================ what is declared, in code

#: The tools a lane's close-out needs on EITHER substrate (`claude` runs the lane, `gh` lands it,
#: `codex` is the review route after the Grok window, `agy` the other read route). Declared here
#: rather than argued in prose: a tool absent on one side, absent on both, or at two versions is
#: a FAIL naming it.
LANE_TOOLS: tuple[str, ...] = ("claude", "gh", "codex", "agy")

#: Condition-1 manifest entries that legitimately differ by OS, each with its reason. Everything
#: else in the manifest must be equal. `platform` is the OS and CPU by definition.
OS_SPECIFIC_ENTRIES: dict[str, str] = {
    "platform": "the operating system and CPU architecture differ by definition between a "
                "Windows workstation and a Linux container",
}

#: Condition-2 differences forgiven because they are a known OS case with its OWN row: key (a
#: hook id or a pytest node id) -> the row id. Empty on purpose: nothing is pre-forgiven, and an
#: entry without a row id is refused by `declared_cases_problems`.
DECLARED_OS_CASES: dict[str, str] = {}

#: Condition 2's fixed hook set -- the hooks armed at the `pre-commit` stage whose verdict does
#: not depend on the staged diff or the branch name (so the same sha gives the same answer).
GATE_HOOKS: tuple[str, ...] = (
    "codemap-freshness",
    "roster-freshness",
    "claude-rosters-freshness",
    "organ-index-freshness",
    "quality-requirements-freshness",
    "provider-registry-agreement",
    "dispatch-conformance",
)

#: Condition 2's fixed pytest selection: the owned fix sites' own tests plus this check's.
GATE_TESTS: tuple[str, ...] = (
    "tests/test_codespace_parity.py",
    "tests/test_codespace_admission.py",
    "tests/test_codespace_regime.py",
    "tests/test_provision_legs.py",
    "tests/test_provision_sh.py",
)

HOOK_NAMES: tuple[str, ...] = ("pre-commit", "commit-msg", "pre-push")
_HOOK_SIGNATURE = "File generated by pre-commit"  # scripts/arm_hooks.py::_SIGNATURE

LANDING_MERGE_NOT_RUN_REASON = (
    "a lane cannot merge: the local --no-ff merge, the integrator's own re-run of the outcome "
    "test and the CI push verdict are the integrator's acts, not this check's")

TRANSPORT_WRITE_NOT_RUN_REASON = (
    "the write leg was not exercised: a write probe would create a transport path no contract "
    "names, so only the read leg is measured")

#: Cores per Codespace machine type -- the multiplier GitHub bills core-hours by. A machine not
#: listed is refused (`core_hours`), never priced at zero.
MACHINE_CORES: dict[str, int] = {
    "basicLinux32gb": 2,
    "standardLinux32gb": 4,
    "premiumLinux": 8,
    "largePremiumLinux": 16,
}

CONDITION_NAMES = {1: "environment", 2: "gates", 3: "landing", 4: "transport", 5: "cleanup"}

_REQUIRED_KEYS = ("environment", "gates", "landing", "transport", "base_sha", "tree_sha", "side")


def declared_cases_problems() -> list[str]:
    """Each declared OS case must carry a row id -- a bare forgiveness is a hidden FAIL."""
    return [k for k, row in DECLARED_OS_CASES.items() if not str(row).startswith("[#")]


# =============================================================================== types

class RemoteUnavailable(RuntimeError):
    """The Codespace side could not be created, reached or read -- the typed R59 failure."""


class LocalRecordUnusable(RuntimeError):
    """The local record is missing or malformed -- nothing to compare against."""


@dataclass(frozen=True)
class CmdResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


Runner = Callable[..., CmdResult]


@dataclass(frozen=True)
class Verdict:
    condition: int
    name: str
    status: str  # PASS | FAIL | NOT-RUN
    reason: str
    evidence: tuple[str, ...] = ()

    def render(self) -> str:
        head = f"{self.status} cond={self.condition} {self.name}"
        return f"{head} {self.reason}".rstrip() if self.reason else head


def _verdict(n: int, status: str, reason: str = "", evidence: Sequence[str] = ()) -> Verdict:
    return Verdict(n, CONDITION_NAMES[n], status, reason, tuple(evidence))


def default_run(argv: Sequence[str], *, cwd: Optional[Path] = None, timeout: int = 900,
                env: Optional[Mapping[str, str]] = None) -> CmdResult:
    """The one place a subprocess starts. Never raises: a command that cannot be started is
    exit 127 and one that timed out is 124 -- data the verdicts reason about."""
    exe = shutil.which(argv[0])
    if exe is None:
        return CmdResult(127, "", f"{argv[0]}: not found on PATH")
    try:
        proc = subprocess.run([exe, *argv[1:]], cwd=str(cwd) if cwd else None, text=True,
                              encoding="utf-8", errors="replace", capture_output=True,
                              timeout=timeout, env=dict(env) if env is not None else None)
    except OSError as exc:
        return CmdResult(127, "", str(exc))
    except subprocess.TimeoutExpired:
        return CmdResult(124, "", f"timed out after {timeout}s")
    return CmdResult(proc.returncode, proc.stdout or "", proc.stderr or "")


_SEMVER = re.compile(r"\d+\.\d+(?:\.\d+)*")


def _semver(text: str) -> Optional[str]:
    match = _SEMVER.search(text or "")
    return match.group(0) if match else None


# =============================================================================== collectors

def _tool_probe(name: str) -> list[str]:
    """A lane runs under a LOGIN shell on a Codespace (`codespace_admission.py`: PATH is only
    complete there), so on POSIX a tool is probed through `bash -lc`."""
    if os.name == "nt":
        return [name, "--version"]
    return ["bash", "-lc", f"command -v {name} >/dev/null 2>&1 && {name} --version"]


def installed_hooks(run: Runner, root: Path) -> list[str]:
    """Hook types whose shim exists and is pre-commit-managed in the RESOLVED hooks dir."""
    where = run(["git", "rev-parse", "--git-path", "hooks"], cwd=root)
    if where.returncode != 0 or not where.stdout.strip():
        return []
    hooks_dir = Path(where.stdout.strip())
    if not hooks_dir.is_absolute():
        hooks_dir = root / hooks_dir
    found = []
    for name in HOOK_NAMES:
        shim = hooks_dir / name
        try:
            if shim.is_file() and _HOOK_SIGNATURE in shim.read_text(encoding="utf-8",
                                                                      errors="replace"):
                found.append(name)
        except OSError:
            continue
    return sorted(found)


def collect_environment(run: Runner, *, root: Path = _REPO_ROOT,
                        hooks: Optional[Sequence[str]] = None) -> dict:
    """Condition 1's manifest, built in the environment this runs in."""
    uv = run(["uv", "--version"], cwd=root)
    sync = run(["uv", "sync", "--locked"], cwd=root)
    py = run(["uv", "run", "--locked", "python", "-c",
              "import platform;print(platform.python_version())"], cwd=root)
    lock = root / "uv.lock"
    tools = {}
    for name in LANE_TOOLS:
        res = run(_tool_probe(name), cwd=root, timeout=60)
        present = res.returncode == 0
        first = (res.stdout.strip().splitlines() or [""])[0]
        tools[name] = {"present": present,
                       "version": (_semver(first) or first or None) if present else None}
    return {
        "python": py.stdout.strip() or None if py.returncode == 0 else None,
        "uv": _semver(uv.stdout) if uv.returncode == 0 else None,
        "uv_lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest() if lock.is_file() else None,
        "uv_sync_exit": sync.returncode,
        "tools": tools,
        "hooks": sorted(hooks) if hooks is not None else installed_hooks(run, root),
        "platform": {"system": platform.system(), "machine": platform.machine()},
    }


_HOOK_STATUS = re.compile(r"(Passed|Failed|Skipped)\s*$", re.MULTILINE)


def _hook_verdict(res: CmdResult) -> str:
    """pass | fail | skipped, read from pre-commit's own status word -- exit 0 alone cannot tell
    a hook that ran from one pre-commit skipped for want of files (a vacuous green)."""
    found = _HOOK_STATUS.findall(res.stdout or "")
    if res.returncode != 0:
        return "fail"
    return found[-1].lower() if found else "unknown"


def parse_junit(path: Path) -> dict[str, str]:
    """`classname::name` -> passed | failed | skipped | error. A missing or unparseable file is
    an EMPTY selection, which `compare_gates` refuses rather than reading as 'nothing differs'."""
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError):
        return {}
    out: dict[str, str] = {}
    for case in root.iter("testcase"):
        key = f"{case.get('classname', '')}::{case.get('name', '')}"
        if case.find("failure") is not None:
            out[key] = "failed"
        elif case.find("error") is not None:
            out[key] = "error"
        elif case.find("skipped") is not None:
            out[key] = "skipped"
        else:
            out[key] = "passed"
    return out


def collect_gates(run: Runner, *, root: Path = _REPO_ROOT, via_gate: bool = False) -> dict:
    """Condition 2's verdict set: the fixed hooks, `audit.py health`, the fixed pytest selection."""
    hooks = {}
    for hook in GATE_HOOKS:
        res = run(["uv", "run", "--locked", "pre-commit", "run", hook, "--hook-stage",
                   "pre-commit", "--all-files"], cwd=root, timeout=600)
        hooks[hook] = _hook_verdict(res)
    health = run(["uv", "run", "--locked", "python", "scripts/audit.py", "health"], cwd=root,
                 timeout=900)
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / "junit.xml"
        pytest_argv = ["uv", "run", "--locked", "pytest", *GATE_TESTS, "-p", "no:cacheprovider",
                       "-q", "--junitxml", str(xml)]
        if via_gate:  # the gate computes and appends `-n <workers>`; verdicts do not depend on it
            argv = ["uv", "run", "--locked", "python", "scripts/memory_admission_gate.py", "run",
                    "--workers-flag", "-n", "--", *pytest_argv]
        else:
            argv = [*pytest_argv, "-n0"]
        run(argv, cwd=root, timeout=3600)
        tests = parse_junit(xml)
    return {"hooks": hooks, "audit_health": "pass" if health.returncode == 0 else "fail",
            "tests": tests}


def collect_landing(run: Runner, *, root: Path = _REPO_ROOT,
                    push_branch: Optional[str] = None) -> dict:
    """Condition 3's facts. The push leg runs only when a branch name is given (the Codespace
    side); `ls-remote` is read back so the pushed sha is origin's, not this process's belief."""
    head = run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=root).stdout.strip()
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root).stdout.strip()
    dirty = bool(run(["git", "status", "--porcelain"], cwd=root).stdout.strip())
    landing: dict = {"pushed_branch": None, "pushed_sha": None, "push_exit": None}
    if push_branch:
        push = run(["git", "push", "origin", f"HEAD:refs/heads/{push_branch}"], cwd=root,
                   timeout=300)
        landing["push_exit"] = push.returncode
        if push.returncode == 0:
            listed = run(["git", "ls-remote", "--heads", "origin", push_branch], cwd=root,
                         timeout=120)
            sha = listed.stdout.split()[0] if listed.returncode == 0 and listed.stdout.split() else None
            if sha:
                landing["pushed_branch"], landing["pushed_sha"] = push_branch, sha
    return {"base_sha": head, "tree_sha": tree, "branch": branch, "dirty": dirty,
            "landing": landing}


def collect_transport(run: Runner, *, env: Optional[Mapping[str, str]] = None) -> dict:
    """Condition 4's read leg. The secret is a BOOLEAN here -- its value never enters a record."""
    env = os.environ if env is None else env
    ver = run(["rclone", "--version"], timeout=60)
    present = ver.returncode == 0
    out: dict = {
        "rclone": {"present": present,
                   "version": _semver((ver.stdout.strip().splitlines() or [""])[0]) if present else None},
        "token_present": bool(env.get("RCLONE_CONFIG_GDRIVE_TOKEN")),
        "read_exit": None,
        "read_entries": None,
    }
    if present:
        read = run(["rclone", "lsf", "gdrive:", "--max-depth", "1"], timeout=120)
        out["read_exit"] = read.returncode
        out["read_entries"] = (len([ln for ln in read.stdout.splitlines() if ln.strip()])
                               if read.returncode == 0 else None)
    return out


def collect_record(run: Runner = default_run, *, root: Path = _REPO_ROOT, side: str = "",
                   push_branch: Optional[str] = None, via_gate: bool = False,
                   skip_gates: bool = False) -> dict:
    if not side:
        side = "codespace" if os.environ.get("CODESPACES") == "true" else "local"
    landing = collect_landing(run, root=root, push_branch=push_branch)  # first: before any run dirties the tree
    return {
        "schema": SCHEMA,
        "side": side,
        "os": platform.system(),
        "base_sha": landing["base_sha"],
        "tree_sha": landing["tree_sha"],
        "branch": landing["branch"],
        "dirty": landing["dirty"],
        "environment": collect_environment(run, root=root),
        "gates": ({"hooks": {}, "audit_health": None, "tests": {}} if skip_gates
                  else collect_gates(run, root=root, via_gate=via_gate)),
        "landing": landing["landing"],
        "transport": collect_transport(run),
    }


def write_record(path: Path, record: Mapping) -> None:
    Path(path).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8",
                          newline="\n")


# ============================================================================ cost

def core_hours(created: Optional[datetime], deleted: Optional[datetime], machine: str) -> float:
    if machine not in MACHINE_CORES:
        raise ValueError(f"unknown Codespace machine type {machine!r} -- refusing to price it at "
                         f"zero (known: {', '.join(sorted(MACHINE_CORES))})")
    return _regime.uptime_minutes(created, deleted) / 60.0 * MACHINE_CORES[machine]


# =========================================================================== comparators

def compare_environment(local: Mapping, remote: Mapping) -> Verdict:
    le, re_ = local["environment"], remote["environment"]
    problems: list[str] = []
    evidence: list[str] = []
    for key in sorted(set(le) | set(re_)):
        if key in OS_SPECIFIC_ENTRIES:
            evidence.append(f"{key}: declared OS-specific ({OS_SPECIFIC_ENTRIES[key]}) -- "
                            f"local={le.get(key)} codespace={re_.get(key)}")
            continue
        if key in ("tools", "uv_sync_exit", "hooks"):
            continue
        lv, rv = le.get(key), re_.get(key)
        evidence.append(f"{key}: local={lv} codespace={rv}")
        if lv != rv or lv is None:
            problems.append(f"{key} differs (local={lv} codespace={rv})")
    for side, env in (("local", le), ("codespace", re_)):
        evidence.append(f"uv sync --locked exit ({side})={env.get('uv_sync_exit')}")
        if env.get("uv_sync_exit") != 0:
            problems.append(f"uv sync --locked exit {env.get('uv_sync_exit')} on {side}")
    for name in LANE_TOOLS:
        lt = le.get("tools", {}).get(name, {"present": False, "version": None})
        rt = re_.get("tools", {}).get(name, {"present": False, "version": None})
        evidence.append(f"{name} version local={lt.get('version')} codespace={rt.get('version')}")
        if not lt.get("present") and not rt.get("present"):
            problems.append(f"{name} absent on both sides")
        elif lt.get("present") != rt.get("present"):
            where = "codespace" if lt.get("present") else "local"
            problems.append(f"{name} absent on {where}")
        elif lt.get("version") != rt.get("version"):
            problems.append(f"{name} version skew (local={lt.get('version')} "
                            f"codespace={rt.get('version')})")
    lh, rh = list(le.get("hooks", [])), list(re_.get("hooks", []))
    evidence.append(f"hook set local={lh} codespace={rh}")
    if sorted(lh) != sorted(rh) or not lh:
        problems.append(f"hook set differs (local={lh} codespace={rh})")
    if problems:
        return _verdict(1, "FAIL", "; ".join(problems), evidence)
    return _verdict(1, "PASS", "", evidence)


def compare_gates(local: Mapping, remote: Mapping) -> Verdict:
    lg, rg = local["gates"], remote["gates"]
    problems: list[str] = []
    evidence: list[str] = []
    for side, g in (("local", lg), ("codespace", rg)):
        if not g.get("tests"):
            problems.append(f"empty pytest selection on {side} -- nothing ran, nothing to compare")
    flat_l: dict[str, str] = {}
    flat_r: dict[str, str] = {}
    for src, dst in ((lg, flat_l), (rg, flat_r)):
        for hook, v in (src.get("hooks") or {}).items():
            dst[hook] = v
        dst["audit.py health"] = src.get("audit_health")
        for node, v in (src.get("tests") or {}).items():
            dst[node] = v
    differing = []
    for key in sorted(set(flat_l) | set(flat_r)):
        lv, rv = flat_l.get(key), flat_r.get(key)
        if lv == rv:
            continue
        if key in DECLARED_OS_CASES:
            evidence.append(f"declared OS case {key} -> {DECLARED_OS_CASES[key]} "
                            f"(local={lv} codespace={rv})")
            continue
        differing.append(f"{key} (local={lv} codespace={rv})")
    evidence.append(f"compared {len(set(flat_l) | set(flat_r))} verdicts; "
                    f"{len(differing)} differ, {len(DECLARED_OS_CASES)} declared case(s)")
    if differing:
        problems.append(f"{len(differing)} verdict(s) differ: " + "; ".join(differing[:12])
                        + (f"; +{len(differing) - 12} more" if len(differing) > 12 else ""))
    if problems:
        return _verdict(2, "FAIL", " | ".join(problems), evidence)
    return _verdict(2, "PASS", "", evidence)


def compare_landing(local: Mapping, remote: Mapping) -> Verdict:
    evidence = [f"base sha local={local.get('base_sha')} codespace={remote.get('base_sha')}",
                f"tree sha local={local.get('tree_sha')} codespace={remote.get('tree_sha')}"]
    problems = []
    if local.get("base_sha") != remote.get("base_sha"):
        problems.append("the two sides did not start from the same base sha")
    if local.get("tree_sha") != remote.get("tree_sha"):
        problems.append("the trees differ at the compared commits")
    for side, rec in (("local", local), ("codespace", remote)):
        if rec.get("dirty"):
            problems.append(f"the {side} work tree was dirty: the compared commit is not what ran")
    landing = remote.get("landing") or {}
    pushed = landing.get("pushed_branch")
    if pushed:
        evidence.append(f"pushed branch {pushed} on origin at {landing.get('pushed_sha')}; "
                        f"codespace HEAD {remote.get('base_sha')}")
        if landing.get("pushed_sha") != remote.get("base_sha"):
            problems.append("the pushed branch is not the Codespace's HEAD")
    if problems:
        return _verdict(3, "FAIL", "; ".join(problems), evidence)
    notrun = []
    if not pushed:
        notrun.append(f"push leg not exercised (the Codespace pushed no branch; push exit "
                      f"{landing.get('push_exit')})")
    notrun.append(f"merge leg NOT-RUN: {LANDING_MERGE_NOT_RUN_REASON}")
    return _verdict(3, "NOT-RUN", "; ".join(notrun), evidence)


def compare_transport(local: Mapping, remote: Mapping) -> Verdict:
    t = remote["transport"]
    lt = local.get("transport") or {}
    problems = []
    if not (t.get("rclone") or {}).get("present"):
        problems.append("rclone absent on the Codespace")
    if not t.get("token_present"):
        problems.append("RCLONE_CONFIG_GDRIVE_TOKEN not set on the Codespace")
    if (t.get("rclone") or {}).get("present"):
        if t.get("read_exit") != 0:
            problems.append(f"read exit {t.get('read_exit')}")
        elif not t.get("read_entries"):
            problems.append(f"read returned {t.get('read_entries')} entries")
    evidence = [f"read: {'FAIL' if problems else 'PASS'} (exit {t.get('read_exit')}, "
                f"{t.get('read_entries')} entries; local {lt.get('read_entries')})",
                f"write: NOT-RUN -- {TRANSPORT_WRITE_NOT_RUN_REASON}"]
    if problems:
        return _verdict(4, "FAIL", "; ".join(problems), evidence)
    return _verdict(4, "NOT-RUN", TRANSPORT_WRITE_NOT_RUN_REASON, evidence)


def compare_cleanup(cleanup: Optional[Mapping]) -> Verdict:
    if cleanup is None:
        return _verdict(5, "NOT-RUN",
                        "no cleanup record supplied (run `verify-cleanup` after teardown)")
    problems = []
    evidence = []
    if cleanup.get("codespace_listed_after"):
        problems.append(f"codespace {cleanup.get('codespace')} still listed after teardown")
    if cleanup.get("branch_listed_after"):
        problems.append(f"branch {cleanup.get('branch')} still on origin")
    try:
        created = datetime.fromisoformat(cleanup["created"]) if cleanup.get("created") else None
        deleted = datetime.fromisoformat(cleanup["deleted"]) if cleanup.get("deleted") else None
        if created is None or deleted is None:
            problems.append("no creation or deletion time recorded: the cost is not measurable")
        else:
            wall = _regime.uptime_minutes(created, deleted)
            hours = core_hours(created, deleted, cleanup.get("machine", ""))
            evidence.append(f"wall time {wall:.1f} min on {cleanup.get('machine')}; "
                            f"core-hours {hours:.2f} ({MACHINE_CORES[cleanup['machine']]} cores)")
            if wall <= 0:
                problems.append("zero recorded uptime")
    except (ValueError, KeyError, TypeError) as exc:
        problems.append(f"cost not computable: {exc}")
    if problems:
        return _verdict(5, "FAIL", "; ".join(problems), evidence)
    evidence.append(f"codespace {cleanup.get('codespace')} and branch {cleanup.get('branch')} "
                    "both gone")
    return _verdict(5, "PASS", "", evidence)


def compare_all(local: Mapping, remote: Mapping, cleanup: Optional[Mapping] = None) -> list[Verdict]:
    return [compare_environment(local, remote), compare_gates(local, remote),
            compare_landing(local, remote), compare_transport(local, remote),
            compare_cleanup(cleanup)]


def exit_code(verdicts: Sequence[Verdict]) -> int:
    statuses = {v.status for v in verdicts}
    if "FAIL" in statuses:
        return 1
    if "NOT-RUN" in statuses:
        return 2
    return 0


# ============================================================================ loading, checking

def _validate(text: str, side: str, exc: type) -> dict:
    if not text or not text.strip():
        raise exc("the record is empty")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        raise exc(f"the record is not JSON ({err.msg} at char {err.pos})") from err
    if not isinstance(data, dict):
        raise exc("the record is not a JSON object")
    if data.get("schema") != SCHEMA:
        raise exc(f"the record's schema is {data.get('schema')!r}, expected {SCHEMA}")
    missing = [k for k in _REQUIRED_KEYS if k not in data]
    if missing:
        raise exc(f"the record lacks {', '.join(missing)}")
    if data.get("side") != side:
        raise exc(f"the record says side={data.get('side')!r}, expected {side!r} -- comparing "
                  "a side with itself would be green by construction")
    return data


def load_local(path: Path) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise LocalRecordUnusable(f"cannot read the local record: {exc}") from exc
    return _validate(text, "local", LocalRecordUnusable)


def read_remote_file(path: Path) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise RemoteUnavailable(f"cannot read the Codespace record: {exc}") from exc
    return _validate(text, "codespace", RemoteUnavailable)


def read_remote_via_gh(name: str, remote_file: str, run: Runner) -> dict:
    """`gh codespace ssh ... cat`, never `cp` (measured: `cp` exits 0 having written nothing)."""
    res = run(["gh", "codespace", "ssh", "-c", name, "--", "cat", remote_file], timeout=300)
    if res.returncode != 0:
        detail = (res.stdout or res.stderr or "").strip().replace("\n", " ")[:200]
        raise RemoteUnavailable(f"gh codespace ssh exited {res.returncode} reading {remote_file}"
                                f"{': ' + detail if detail else ''}")
    return _validate(res.stdout, "codespace", RemoteUnavailable)


def _unavailable_report(why: str, label: str = "RemoteUnavailable") -> str:
    lines = [f"FAILURE {label}: {why}"]
    for n, name in CONDITION_NAMES.items():
        lines.append(f"NOT-RUN cond={n} {name} remote side unavailable -- nothing was compared")
    return "\n".join(lines)


def render_report(verdicts: Sequence[Verdict]) -> str:
    lines = []
    for v in verdicts:
        lines.append(v.render())
        lines.extend(f"    {e}" for e in v.evidence)
    return "\n".join(lines)


def run_check(local_path: Path, *, remote_path: Optional[Path] = None,
              codespace: Optional[str] = None, remote_file: str = DEFAULT_REMOTE_FILE,
              cleanup_path: Optional[Path] = None, run: Optional[Runner] = None,
              save_remote: Optional[Path] = None) -> tuple[int, str]:
    """Compare the two records. Returns (exit code, report text); never raises.

    `save_remote` keeps the record read over gh: the Codespace is deleted at teardown, and a
    verdict whose remote evidence died with it cannot be re-derived (found on the first run)."""
    try:
        local = load_local(local_path)
    except LocalRecordUnusable as exc:
        return 4, _unavailable_report(str(exc), "LocalRecordUnusable")
    try:
        if remote_path is not None:
            remote = read_remote_file(remote_path)
        elif codespace:
            remote = read_remote_via_gh(codespace, remote_file, run or default_run)
        else:
            raise RemoteUnavailable("no remote record and no Codespace named -- nothing to compare")
    except RemoteUnavailable as exc:
        return 3, _unavailable_report(str(exc))
    if save_remote is not None:
        write_record(save_remote, remote)
    cleanup: Optional[dict] = None
    cleanup_problem = ""
    if cleanup_path is not None:
        try:
            cleanup = json.loads(Path(cleanup_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            cleanup_problem = f"the cleanup record is unreadable ({exc})"
    verdicts = compare_all(local, remote, cleanup)
    if cleanup_problem:
        verdicts[4] = _verdict(5, "FAIL", cleanup_problem)
    code = exit_code(verdicts)
    return code, render_report(verdicts) + f"\nexit={code}"


# ============================================================================ verify-cleanup

def verify_cleanup(name: str, branch: str, created: str, deleted: str, machine: str,
                   run: Runner = default_run, *, root: Path = _REPO_ROOT) -> dict:
    """Condition 5's record: read AFTER teardown that the Codespace is not listed and the run
    branch is not on origin. A listing that cannot be read raises -- 'could not look' is not
    'gone'."""
    listing = run(["gh", "codespace", "list", "--json", "name"], timeout=120)
    if listing.returncode != 0:
        raise RemoteUnavailable(f"gh codespace list exited {listing.returncode}: cannot say "
                                "the Codespace is gone")
    try:
        names = [row.get("name") for row in json.loads(listing.stdout or "[]")]
    except (json.JSONDecodeError, AttributeError) as exc:
        raise RemoteUnavailable(f"gh codespace list returned unreadable output: {exc}") from exc
    heads = run(["git", "ls-remote", "--heads", "origin", branch], cwd=root, timeout=120)
    if heads.returncode != 0:
        raise RemoteUnavailable(f"git ls-remote exited {heads.returncode}: cannot say the "
                                "branch is gone")
    return {"schema": SCHEMA, "codespace": name, "machine": machine, "created": created,
            "deleted": deleted, "codespace_listed_after": name in names, "branch": branch,
            "branch_listed_after": bool(heads.stdout.strip())}


# ============================================================================================ CLI

@click.group()
def cli() -> None:
    """The five-condition Codespace parity check ([#1335])."""


@cli.command("collect")
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
@click.option("--side", default="", help="local | codespace; default: from $CODESPACES.")
@click.option("--push-branch", default=None, help="Codespace side: push HEAD to this branch.")
@click.option("--via-gate", is_flag=True, help="Run the pytest leg through memory_admission_gate.")
@click.option("--skip-gates", is_flag=True, help="Debug only: an empty gates leg, which `check` refuses.")
def collect_cmd(out: Path, side: str, push_branch: Optional[str], via_gate: bool,
                skip_gates: bool) -> None:
    """Build this environment's record (conditions 1-4's evidence) and write it to --out."""
    record = collect_record(side=side, push_branch=push_branch, via_gate=via_gate,
                            skip_gates=skip_gates)
    write_record(out, record)
    click.echo(f"record written: side={record['side']} base={record['base_sha'][:12]} -> {out}")


@cli.command("check")
@click.option("--local", "local_path", required=True, type=click.Path(path_type=Path))
@click.option("--remote", "remote_path", default=None, type=click.Path(path_type=Path))
@click.option("--codespace", default=None, help="Read the remote record over gh codespace ssh.")
@click.option("--remote-file", default=DEFAULT_REMOTE_FILE, show_default=True)
@click.option("--cleanup", "cleanup_path", default=None, type=click.Path(path_type=Path))
@click.option("--save-remote", "save_remote", default=None, type=click.Path(path_type=Path),
              help="Keep the record read over gh, so the evidence outlives the Codespace.")
def check_cmd(local_path: Path, remote_path: Optional[Path], codespace: Optional[str],
              remote_file: str, cleanup_path: Optional[Path],
              save_remote: Optional[Path]) -> None:
    """One verdict per condition; exit 0 all PASS | 1 FAIL | 2 NOT-RUN | 3 remote unavailable."""
    code, text = run_check(local_path, remote_path=remote_path, codespace=codespace,
                           remote_file=remote_file, cleanup_path=cleanup_path,
                           save_remote=save_remote)
    click.echo(text)
    sys.exit(code)


@cli.command("verify-cleanup")
@click.option("--codespace", "name", required=True)
@click.option("--branch", required=True)
@click.option("--created", required=True, help="ISO-8601 creation time.")
@click.option("--deleted", required=True, help="ISO-8601 deletion time.")
@click.option("--machine", required=True)
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
def verify_cleanup_cmd(name: str, branch: str, created: str, deleted: str, machine: str,
                       out: Path) -> None:
    """After teardown: read that the Codespace and the run branch are gone; write the record."""
    try:
        record = verify_cleanup(name, branch, created, deleted, machine)
    except RemoteUnavailable as exc:
        click.echo(f"FAILURE RemoteUnavailable: {exc}")
        sys.exit(3)
    write_record(out, record)
    click.echo(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    cli()
