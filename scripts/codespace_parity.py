#!/usr/bin/env python
"""codespace_parity.py -- "a Codespace lane works" as a repository check, not a lifecycle that
merely completed (`[#1335]`; `to-browser/CODESPACE-PARITY-DEFINITION-2026-10-03.md`; lane
foundation-5-codespace-parity, batch FOUNDATION).

WHAT IT ANSWERS. One real task, run once in a local worktree and once in a Codespace from the same
base sha, must agree on five conditions. This script builds the evidence for each in the
environment it runs in (`collect`), compares two such records (`check`), and prints ONE verdict per
condition -- `PASS`, `FAIL`, or `NOT-RUN <reason>` -- with the two values compared as evidence:

    1 environment   Python, `uv`, the `uv.lock` hash, `uv sync --locked` exit, the versions of the
                    tools a lane needs (`claude`, `gh`, `codex`, `grok`, `agy`), the installed
                    git-hook set -- identical except the OS-specific entries declared below, in
                    code. EACH MODEL CLI ALSO ANSWERS ONE CALL (b2-codespace-1to1, R63): the id it
                    SERVED is read from the tool's own record and must equal what
                    `ecosystem/provider-registry.yaml` routes that CLI's role to (R61) -- a CLI that
                    prints the pinned `--version` and silently serves another model is a FAIL naming
                    both ids. A tool the Codespace has but is not logged in to is a NAMED auth item
                    (`PASS except named auth items: ...`), never a silent exception.
    2 gates         a FIXED set of pre-commit hooks, `audit.py health` and a FIXED pytest
                    selection, same verdict on both sides or a declared OS case with its own row.
    3 landing       same base sha and tree; the Codespace's pushed branch resolves to its HEAD.
                    The integrator leg (local `--no-ff` merge + the CI push verdict) is NOT-RUN:
                    a lane cannot merge, and a check that printed PASS for a leg nobody ran would
                    be the vacuous pass this file exists to refuse.
    4 transport     the Codespace reads the Drive transport by rclone (the secret is checked for
                    PRESENCE only, never read into a record). The write leg is NOT-RUN unless
                    `collect --probe-write NAME` is given (foundation-13): a write probe creates a
                    transport path, so a contract must name the file; it is read back and deleted.
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
pytest junit file) plus the already-declared `click` and `pyyaml` (the registry is read as the YAML
file it is, not through a second parser); `pre-commit` and `pytest` are the existing runners;
`codespace_regime.uptime_minutes` is reused for cost. The served-id probes (b2-codespace-1to1) call
each CLI's own headless mode and read each CLI's own record -- no vendor SDK, no new dependency.

    uv run --locked python scripts/codespace_parity.py collect --out record.json [--push-branch B]
    uv run --locked python scripts/codespace_parity.py check --local l.json --remote r.json
    uv run --locked python scripts/codespace_parity.py check --local l.json --codespace NAME
    uv run --locked python scripts/codespace_parity.py verify-cleanup --codespace NAME ...
"""
from __future__ import annotations

import enum
import hashlib
import json
import logging
import os
import platform
import re
import secrets
import shlex
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
import yaml

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
#: `codex` and `grok` are the review routes, `agy` the other read route). Declared here
#: rather than argued in prose: a tool absent on one side, absent on both, or at two versions is
#: a FAIL naming it.
LANE_TOOLS: tuple[str, ...] = ("claude", "gh", "codex", "grok", "agy")

#: The model CLIs among them: each answers one call and reports the id it SERVED (R61, R63).
MODEL_CLIS: tuple[str, ...] = ("claude", "codex", "grok", "agy")

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

#: Condition 1's AUTH ITEMS (foundation-13, R63 step 1). Installing a tool does not log it in, and a
#: login or token is something a repository check must neither create nor hide. `collect` records
#: each tool's login state by its own status command (output discarded -- no token can enter a
#: record); `check` then NAMES every tool the Codespace has installed but not authenticated, with
#: what it needs, as `AUTH-ITEM` evidence and in the verdict line. They are exceptions to the
#: environment PASS, never silent ones: condition 1 reads `PASS except named auth items: ...`.
#: `agy` and `grok` have no non-interactive status command, so they are `unprobed` until their model
#: call answers (that call is then the proof of login) and named for that reason otherwise.
AUTH_PROBES: dict[str, Optional[tuple[str, ...]]] = {
    "claude": ("claude", "auth", "status"),
    "gh": ("gh", "auth", "status"),
    # `codex login status` reads the ChatGPT login only: it printed "Not logged in" on a Codespace
    # whose `CODEX_API_KEY` answered every call (night leg 5, D9), so C1 named codex an auth item
    # on every run. Like grok and agy it has no status command that tells the truth; its served-id
    # call is the proof of login (`_fold_model_proof_into_auth`).
    "codex": None,
    "grok": None,
    "agy": None,
}

AUTH_NEEDS: dict[str, str] = {
    "claude": "the CLAUDE_CODE_OAUTH_TOKEN Codespaces secret (from `claude setup-token`)",
    "gh": "GITHUB_TOKEN or GH_TOKEN in the environment, or `gh auth login`",
    "codex": "`codex login --device-auth` run once in the Codespace (ChatGPT device sign-in; "
             "no Codespaces secret holds it)",
    "grok": "`grok login --device-auth` run once in the Codespace (xAI device sign-in for a headless "
            "host; no Codespaces secret holds it)",
    "agy": "an `agy` sign-in: run `agy` once in the Codespace (`gh codespace ssh`), open the Google "
           "URL it prints in a browser and complete the sign-in (no login subcommand, no Codespaces "
           "secret; its model call is what shows the login)",
}

#: The folders a probe may write into besides the transport root: exactly one, `to-browser/`, where
#: the lanes' own handbacks go. A probe addresses ONE file there -- never a deeper path, never a
#: sibling folder, never `..` -- so it can only ever create the file a contract names.
TRANSPORT_PROBE_DIRS: tuple[str, ...] = ("to-browser",)

#: The one path `collect --probe-write` may write on the transport: a single plain file name at the
#: root, or a single plain file name directly inside one of `TRANSPORT_PROBE_DIRS`.
_PROBE_NAME_RE = re.compile(r"^(?:(?:" + "|".join(re.escape(d) for d in TRANSPORT_PROBE_DIRS)
                            + r")/)?[A-Za-z0-9][A-Za-z0-9._-]*$")

def _probe_name_ok(name: str) -> bool:
    """A probe name the regex admits AND that is not a folder's own name (a root file called
    `to-browser` would collide with the folder it shadows)."""
    return bool(_PROBE_NAME_RE.fullmatch(name)) and name not in TRANSPORT_PROBE_DIRS


HOOK_NAMES: tuple[str, ...] = ("pre-commit", "commit-msg", "pre-push")
_HOOK_SIGNATURE = "File generated by pre-commit"  # scripts/arm_hooks.py::_SIGNATURE

LANDING_MERGE_NOT_RUN_REASON = (
    "no integration record was supplied: the local --no-ff merge of the test lane's branch on a "
    "scratch `worktree-integrate-*` branch, the re-run of the outcome test and that branch's CI "
    "push verdict are measured by `integrate` and read here by `check --integration`; a leg "
    "nobody ran is NOT-RUN, never PASS")

TRANSPORT_WRITE_NOT_RUN_REASON = (
    "the write leg was not exercised: `collect --probe-write PATH` exercises it (PATH is one plain "
    "file name, or one file in `to-browser/`, that the contract names); until it runs only the "
    "read leg is measured")

#: CI states a scratch-branch merge may LAND on -- `merge_path.LANDABLE_STATES`, restated so this
#: reader needs no import of the merge path (a test holds the two equal). `PASS` is the only green;
#: `PRE-EXISTING` is every failing test accounted for against the base.
CI_LANDABLE_STATES: tuple[str, ...] = ("PASS", "PRE-EXISTING")
#: CI states that MEASURED a red: the leg ran and failed.
CI_FAILED_STATES: tuple[str, ...] = ("REGRESSED", "RED", "CANCELLED")

#: The only branch a scratch integration may push: the integrator's own prefix (`merge_path.
#: INTEGRATION_BRANCH_PREFIX`) and a plain slug, never `main`.
_SCRATCH_BRANCH_RE = re.compile(r"^worktree-integrate-[a-z0-9][a-z0-9-]*$")
_RUN_BRANCH_RE = re.compile(r"^worktree-[a-z0-9][a-z0-9-]*$")
_FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

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


class Leg(enum.Enum):
    """What ONE measured leg of a condition came to -- three values that cannot stand in for each
    other (N1, R59). `NOT_RUN` is not a weak `PASS` and not a soft `FAIL`: it is the leg nobody
    measured, and a condition made of legs is `PASS` only when every leg is `PASS`."""

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT-RUN"


@dataclass(frozen=True)
class LegResult:
    leg: Leg
    detail: str


def fold_legs(legs: Sequence[LegResult]) -> tuple[str, str]:
    """`(status, reason)` of a condition from its legs: FAIL if any leg failed, else NOT-RUN if
    any leg was unmeasured -- or if there are no legs at all (an empty fold would be `all passed`
    by vacuity, the pass this check exists to refuse) -- else PASS."""
    failed = [r.detail for r in legs if r.leg is Leg.FAIL]
    if failed:
        return "FAIL", "; ".join(failed)
    unmeasured = [r.detail for r in legs if r.leg is Leg.NOT_RUN]
    if unmeasured or not legs:
        return "NOT-RUN", "; ".join(unmeasured) or "no leg was measured"
    return "PASS", ""


def default_run(argv: Sequence[str], *, cwd: Optional[Path] = None, timeout: int = 900,
                env: Optional[Mapping[str, str]] = None) -> CmdResult:
    """The one place a subprocess starts. Never raises: a command that cannot be started is
    exit 127 and one that timed out is 124 -- data the verdicts reason about."""
    exe = shutil.which(argv[0])
    if exe is None:
        return CmdResult(127, "", f"{argv[0]}: not found on PATH")
    try:
        # stdin is closed: `codex exec` prints "Reading additional input from stdin..." and waits
        # forever on an open pipe (found building the served-id probe, 2026-10-04).
        proc = subprocess.run([exe, *argv[1:]], cwd=str(cwd) if cwd else None, text=True,
                              encoding="utf-8", errors="replace", capture_output=True,
                              stdin=subprocess.DEVNULL,
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


def _status_probe(argv: Sequence[str]) -> list[str]:
    """A login-state command, run the way `_tool_probe` runs a version: a LOGIN shell on POSIX."""
    if os.name == "nt":
        return list(argv)
    return ["bash", "-lc", shlex.join(argv)]


def collect_auth(run: Runner, tools: Mapping[str, Mapping], *, root: Path = _REPO_ROOT) -> dict:
    """Each lane tool's login state, from its own status command. The command's output is read
    for one boolean and discarded; the record carries only the state and the command's name."""
    auth: dict[str, dict] = {}
    for name in LANE_TOOLS:
        cmd = AUTH_PROBES.get(name)
        label = " ".join(cmd) if cmd else "(no non-interactive status command)"
        if not (tools.get(name) or {}).get("present"):
            state = "tool-absent"
        elif cmd is None:
            state = "unprobed"
        else:
            res = run(_status_probe(cmd), cwd=root, timeout=60)
            if res.returncode in (124, 127):
                # timed out / would not start: no login was observed either way. Recording it as
                # `unauthenticated` would let C1 print a named exception for a check that never ran.
                state = "probe-error"
            elif name == "claude":
                state = "authenticated" if res.returncode == 0 and re.search(
                    r'"loggedIn"\s*:\s*true', res.stdout or "") else "unauthenticated"
            else:
                state = "authenticated" if res.returncode == 0 else "unauthenticated"
        auth[name] = {"state": state, "probe": label}
    return auth



# ====================================================== C1 served model ids (b2-codespace-1to1)

#: The registry file the served ids are compared with -- the declared home of every provider, CLI
#: and model string on the live surface. Read at call time so a test can point it elsewhere.
REGISTRY_PATH = _REPO_ROOT / "ecosystem" / "provider-registry.yaml"

#: Where the registry says each model CLI's id lives: (provider id, role). `claude` is the lane's
#: runner (`implement`); `codex` and `grok` are the review routes; `agy` has no role-level model
#: (its `read` entry pins none), so its id is the one `antigravity` row under `models:`.
_MODEL_SEAMS: dict[str, tuple[str, Optional[str]]] = {
    "claude": ("anthropic", "implement"),
    "codex": ("openai", "review"),
    "grok": ("xai", "review"),
    "agy": ("antigravity", None),
}

#: agy lists each family in tiers (`agy models`: gemini-3.8-flash-{high,medium,low}); the registry
#: row is the family, so a served tier of that family is the registered model.
_AGY_TIERS = ("high", "medium", "low")

#: What a failed call says when the login is what is missing. Matched only on a call whose nonce did
#: not come back, so a model's own words about "signing in" in an answer never reclassify it (agy
#: logs its model label before it authenticates, so a served id is not proof the call went through).
_LOGIN_MISSING = re.compile(
    r"not (?:logged|signed) in|please (?:run /)?log ?in|sign(?:ed)?[ -]?in|log ?in required"
    r"|unauthori[sz]ed|\b401\b|missing credentials|authentication (?:required|failed)",
    re.IGNORECASE)

PROBE_TIMEOUT = 240


@dataclass(frozen=True)
class ExpectedModel:
    id: Optional[str]
    where: str


def load_registry(path: Optional[Path] = None) -> dict:
    """The provider registry as a plain mapping; `{}` when it cannot be read (every expected id is
    then absent, which the comparison reports by name rather than skipping)."""
    target = Path(path) if path is not None else REGISTRY_PATH
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    return data if isinstance(data, dict) else {}


def expected_models(registry: Mapping) -> dict[str, ExpectedModel]:
    """cli -> the id the registry routes that CLI to, and where the registry says so."""
    out: dict[str, ExpectedModel] = {}
    for cli, (provider, role) in _MODEL_SEAMS.items():
        if role is not None:
            order = ((registry.get("roles") or {}).get(role) or {}).get("order") or []
            entry = next((e for e in order if isinstance(e, Mapping)
                          and e.get("provider") == provider), None)
            model = (entry or {}).get("model")
            where = f"roles.{role}, provider {provider}"
            out[cli] = ExpectedModel(str(model) if model else None,
                                     where if model else f"{where}: no model pinned")
        else:
            rows = [name for name, row in (registry.get("models") or {}).items()
                    if isinstance(row, Mapping) and row.get("provider") == provider]
            where = f"models row of provider {provider}"
            out[cli] = ExpectedModel(rows[0] if len(rows) == 1 else None,
                                     where if len(rows) == 1 else f"{where}: {len(rows)} rows, need one")
    return out


def served_matches(cli: str, served: Optional[str], expected: Optional[str]) -> bool:
    """Exact equality; `agy` alone also accepts a tier of the registered family."""
    if not served or not expected:
        return False
    if served == expected:
        return True
    return cli == "agy" and served.startswith(expected + "-") \
        and served[len(expected) + 1:] in _AGY_TIERS


def probe_prompt(nonce: str) -> str:
    """One line, no quotes: it crosses a login shell and, on Windows, a `.cmd` shim. It is not an
    instruction to repeat an exact string -- grok refuses that wording -- but a check code to return."""
    return f"This is a connectivity check and the check code is {nonce}. Please reply with the check code."


def model_probe_argv(cli: str, nonce: str, model: str, log_file: str) -> list[str]:
    """The one trivial headless call for `cli`, asking for the registry's id by name. A lane asks
    for its model by id too, so the probe tests that the CLI SERVES the id it was asked for."""
    prompt = probe_prompt(nonce)
    if cli == "claude":
        return ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json",
                "--verbose", "--no-session-persistence", "--max-turns", "1",
                "--setting-sources", "user"]
    if cli == "codex":
        return ["codex", "exec", "--skip-git-repo-check", "--color", "never", "-m", model,
                "-s", "read-only", prompt]
    if cli == "grok":
        return ["grok", "-m", model, "-p", prompt, "--output-format", "json", "--max-turns", "1"]
    if cli == "agy":
        return ["agy", "-p", prompt, "--output-format", "json", "--log-file", log_file]
    raise ValueError(f"no served-id probe is declared for {cli!r}")


def _json_lines(text: str) -> list[dict]:
    rows = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _json_object(text: str) -> Optional[dict]:
    """The first JSON object in `text` (a CLI may print a warning line before it)."""
    text = text or ""
    start = text.find("{")
    if start < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def read_claude(stdout: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is the stream's own assistant message `message.model` -- the
    transcript record -- and `<synthetic>` (what Claude Code writes for its own error text) is not a
    served model."""
    served: Optional[str] = None
    texts: list[str] = []
    for obj in _json_lines(stdout):
        if obj.get("type") != "assistant":
            continue
        message = obj.get("message") or {}
        model = message.get("model")
        if model and model != "<synthetic>" and served is None:
            served = str(model)
        for block in message.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(str(block.get("text") or ""))
    return served, nonce in "\n".join(texts)


_ANSI = re.compile("\x1b\\[[0-9;]*m")


def read_codex(stderr: str, stdout: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is the `model:` line of Codex's own run header -- the block
    between the first two rules of STDERR (colour-coded when a terminal is attached, measured
    2026-10-04). Nothing the model prints can reach it: STDOUT is never searched for the id, and a
    `model:` line the transcript echoes after the header is outside the block. The answer is the
    nonce on STDOUT, the final message; the prompt echoed on stderr carries it too and is not one."""
    parts = re.split(r"^-{8}\s*$", _ANSI.sub("", stderr or ""), maxsplit=2, flags=re.MULTILINE)
    header = parts[1] if len(parts) >= 3 else ""
    match = re.search(r"^model:\s*(\S+)", header, re.MULTILINE)
    return (match.group(1) if match else None), nonce in _ANSI.sub("", stdout or "")


def read_grok(stdout: str, nonce: str, home: Path) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is `primaryModelId` in the session store's `usage.json`
    (`~/.grok/sessions/<cwd>/<session>/usage.json`) for the session this call printed."""
    obj = _json_object(stdout)
    if obj is None:
        return None, False
    answered = nonce in str(obj.get("text") or "")
    session = str(obj.get("sessionId") or "")
    served: Optional[str] = None
    if session and re.fullmatch(r"[A-Za-z0-9._-]+", session):
        for usage in sorted(Path(home, ".grok", "sessions").glob(f"*/{session}/usage.json")):
            try:
                data = json.loads(usage.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            primary = ((data or {}).get("session") or {}).get("primaryModelId")
            if primary:
                served = str(primary)
                break
    return served, answered


def _label_slug(label: str) -> str:
    return re.sub(r"[^a-z0-9.]+", "-", label.lower()).strip("-")


def read_agy(stdout: str, log_text: str, nonce: str) -> tuple[Optional[str], bool]:
    """(served id, answered). The id is the model label agy's own run log propagates to its
    backend (`label="Gemini 3.8 Flash (High)"`), as the slug `agy models` lists it under."""
    obj = _json_object(stdout) or {}
    answered = obj.get("status") == "SUCCESS" and nonce in str(obj.get("response") or "")
    labels = re.findall(r'label="([^"]+)"', log_text or "")
    return (_label_slug(labels[-1]) if labels else None), answered


def _probe_one(cli: str, run: Runner, workdir: Path, expected: Optional[ExpectedModel],
               nonce: str, home: Path, timeout: int) -> dict:
    log_file = workdir / "agy.log"
    if expected is None or not expected.id:
        why = expected.where if expected else "no registry entry"
        return {"state": "no-expected", "served_id": None,
                "detail": f"the registry names no model for {cli} ({why}); the call was not made"}
    res = run(_status_probe(model_probe_argv(cli, nonce, expected.id, str(log_file))),
              cwd=workdir, timeout=timeout)
    if res.returncode in (124, 127):
        how = "timed out" if res.returncode == 124 else "could not start"
        return {"state": "probe-error", "served_id": None,
                "detail": f"the call did not run (exit {res.returncode}: {how})"}
    out = res.stdout or ""
    if cli == "claude":
        served, answered = read_claude(out, nonce)
    elif cli == "codex":
        served, answered = read_codex(res.stderr or "", out, nonce)
    elif cli == "grok":
        served, answered = read_grok(out, nonce, home)
    else:
        try:
            log_text = log_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            log_text = ""
        served, answered = read_agy(out, log_text, nonce)
    if served and answered:
        return {"state": "served", "served_id": served,
                "detail": "served id read from the tool's own record; the nonce came back"}
    said = out + "\n" + (res.stderr or "")
    if not answered and _LOGIN_MISSING.search(said):
        return {"state": "unauthenticated", "served_id": None,
                "detail": "the call said the login is missing"}
    return {"state": "no-answer", "served_id": served,
            "detail": (f"exit {res.returncode}; "
                       + ("the nonce did not come back" if served else "no served id in the tool's record"))}


def collect_models(run: Runner, tools: Mapping[str, Mapping], auth: Mapping[str, Mapping],
                   expected: Mapping[str, ExpectedModel], *, home: Optional[Path] = None,
                   nonce: Optional[str] = None, timeout: int = PROBE_TIMEOUT) -> dict:
    """Each model CLI's served id, from ONE call each, run in an empty directory so no project
    context shapes the answer. The record keeps state, id and a one-line detail only -- never the
    model's output, the nonce or any credential."""
    home = Path(home) if home is not None else Path.home()
    nonce = nonce or "CHK-" + secrets.token_hex(4).upper()
    out: dict[str, dict] = {}
    with tempfile.TemporaryDirectory(prefix="parity-probe-") as tmp:
        for cli in MODEL_CLIS:
            if not (tools.get(cli) or {}).get("present"):
                out[cli] = {"state": "tool-absent", "served_id": None, "detail": f"{cli} is not installed"}
            elif ((auth.get(cli) or {}).get("state")) == "unauthenticated":
                out[cli] = {"state": "not-probed-auth", "served_id": None,
                            "detail": "login missing -- a named auth item; the call was not made"}
            else:
                out[cli] = _probe_one(cli, run, Path(tmp), expected.get(cli), nonce, home, timeout)
    return out


def _fold_model_proof_into_auth(auth: dict, models: Mapping[str, Mapping]) -> None:
    """A model call is the only login probe `grok` and `agy` have: an answered call proves the login,
    and one that said the login is missing names it. Status-command verdicts are left alone."""
    for cli in MODEL_CLIS:
        entry, model = auth.get(cli), models.get(cli) or {}
        if entry is None:
            continue
        if model.get("state") == "served" and entry.get("state") == "unprobed":
            auth[cli] = {"state": "authenticated", "probe": "a model call answered (served-id probe)"}
        elif model.get("state") == "unauthenticated":
            auth[cli] = {"state": "unauthenticated", "probe": entry.get("probe", "")}


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
                        hooks: Optional[Sequence[str]] = None, home: Optional[Path] = None,
                        nonce: Optional[str] = None) -> dict:
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
    auth = collect_auth(run, tools, root=root)
    models = collect_models(run, tools, auth,
                            expected_models(load_registry(root / "ecosystem" / "provider-registry.yaml")),
                            home=home, nonce=nonce)
    _fold_model_proof_into_auth(auth, models)
    return {
        "python": py.stdout.strip() or None if py.returncode == 0 else None,
        "uv": _semver(uv.stdout) if uv.returncode == 0 else None,
        "uv_lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest() if lock.is_file() else None,
        "uv_sync_exit": sync.returncode,
        "tools": tools,
        "auth": auth,
        "models": models,
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


def _exact_head(ls_remote_stdout: str, branch: str) -> Optional[str]:
    """The sha of `refs/heads/<branch>` itself. `git ls-remote <pattern>` also returns every
    head that merely ENDS with the pattern (`refs/heads/a/<branch>`), so the first line is not
    the branch (review finding, grok-4.7 P3)."""
    for line in (ls_remote_stdout or "").splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == f"refs/heads/{branch}":
            return parts[0]
    return None


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
            sha = _exact_head(listed.stdout, push_branch) if listed.returncode == 0 else None
            if sha:
                landing["pushed_branch"], landing["pushed_sha"] = push_branch, sha
    return {"base_sha": head, "tree_sha": tree, "branch": branch, "dirty": dirty,
            "landing": landing}


def _probe_write(run: Runner, name: str) -> dict:
    """Condition 4's write leg: write ONE named file, read it back byte-for-byte, delete it, and
    list the remote to prove it is gone. The delete is attempted whenever the write succeeded,
    so a failing read-back cannot leave the probe behind; a file that survives is reported as
    `gone_after: False` and is the caller's to remove (the record names it)."""
    folder, _, leaf = name.rpartition("/")   # "" and the whole name for a root-level probe
    content = (f"{name}\nwritten by scripts/codespace_parity.py collect --probe-write\n"
               f"nonce {hashlib.sha256(os.urandom(16)).hexdigest()[:16]}\n")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / leaf
        src.write_text(content, encoding="utf-8", newline="\n")
        wrote = run(["rclone", "copyto", str(src), f"gdrive:{name}"], timeout=120)
    leg: dict = {"name": name, "write_exit": wrote.returncode, "readback_ok": False,
                 "delete_exit": None, "gone_after": None}
    if wrote.returncode == 0:
        back = run(["rclone", "cat", f"gdrive:{name}"], timeout=120)
        leg["readback_ok"] = back.returncode == 0 and back.stdout == content
        leg["delete_exit"] = run(["rclone", "deletefile", f"gdrive:{name}"], timeout=120).returncode
    # absence is read in the probe's OWN folder: a listing of the root would never show a file
    # that lives in `to-browser/`, and so would call a surviving probe gone
    listed = run(["rclone", "lsf", f"gdrive:{folder}", "--files-only", "--include", leaf],
                 timeout=120)
    if listed.returncode == 0:
        leg["gone_after"] = not listed.stdout.strip()
    return leg


def collect_transport(run: Runner, *, env: Optional[Mapping[str, str]] = None,
                      probe_write: Optional[str] = None) -> dict:
    """Condition 4's read leg -- and, when a contract names the file, its write leg
    (`probe_write`). The secret is a BOOLEAN here -- its value never enters a record."""
    if probe_write is not None and not _probe_name_ok(probe_write):
        raise ValueError(f"--probe-write {probe_write!r} is not a single plain file name "
                         "(letters, digits, '.', '_', '-'), optionally directly inside "
                         f"{' or '.join(d + '/' for d in TRANSPORT_PROBE_DIRS)}; a probe never "
                         "addresses any other path")
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
        # no write to a transport that could not even be read
        if probe_write is not None and read.returncode == 0 and out["read_entries"]:
            out["write"] = _probe_write(run, probe_write)
    return out


# ================================================ C3's integration leg (b2-codespace-green)

def _default_verdict(sha: str, **kw):
    """CI's one verdict for `sha` -- `merge_path.read_verdict`, the integrator's own reader."""
    try:  # pragma: no cover -- exercised by whichever path the caller uses
        from scripts import merge_path as mp
    except ImportError:  # pragma: no cover
        import merge_path as mp
    return mp.read_verdict(sha, **kw)


def collect_integration(run: Runner, *, root: Path, run_branch: str, scratch_branch: str, base: str,
                        outcome_test: Sequence[str], workdir: Path, ci_timeout_s: int = 3600,
                        ci_interval_s: int = 30, verdict_fn: Optional[Callable] = None,
                        onto: Optional[str] = None, ci_base: Optional[str] = None) -> dict:
    """The integrator's acts on the test lane's pushed branch, on a SCRATCH branch, never on main.

    1. read the run branch's tip on origin and fetch it;
    2. cut `scratch_branch` (`worktree-integrate-*`) from `onto` (default `base`) in a temporary
       worktree and merge the run tip into it with `--no-ff` -- the local merge the integrator
       does. `base` is the parity base the run branch must descend from; `onto` is what the
       integrator cuts from, origin/main: CI's spine job judges an integration-branch push as if
       it landed on main, so a scratch branch cut from a lane tip would show the lane's own
       commits as direct ones (b2-codespace-green run 2);
    3. re-run the outcome test on the merged tree;
    4. push the scratch branch alone and read CI's push verdict for the merge commit
       (`merge_path.read_verdict`, the one verdict function the merge path itself uses);
    5. ALWAYS delete the scratch branch on origin, the worktree and the local branch, and read each
       back -- `cleanup` records what was PROVEN gone, not what was asked.

    A leg that did not run leaves its key out of the record (`compare_landing` reads that as
    NOT-RUN); nothing here is ever pushed to `main`, and a scratch name that is not an integrate
    branch is refused before any command runs."""
    if not _SCRATCH_BRANCH_RE.fullmatch(scratch_branch):
        raise ValueError(f"scratch branch {scratch_branch!r} is not a `worktree-integrate-<slug>` "
                         "branch; the integration leg never pushes anywhere else")
    if not _RUN_BRANCH_RE.fullmatch(run_branch) or run_branch == scratch_branch:
        raise ValueError(f"run branch {run_branch!r} is not a `worktree-<slug>` branch")
    if not _FULL_SHA_RE.fullmatch(base):
        raise ValueError(f"base {base!r} is not a full 40-hex sha")
    onto = base if onto is None else onto
    if not _FULL_SHA_RE.fullmatch(onto):
        raise ValueError(f"onto {onto!r} is not a full 40-hex sha")
    # `ci_base` is the commit whose CI run the merge's run is judged AGAINST: main as it is now when
    # the caller knows it (CI runs the scratch branch against the current `main` ref, so an older
    # baseline reads every main-side change since as NEW -- b2-codespace-green run 5); default the
    # commit the scratch branch was cut from.
    ci_base = onto if ci_base is None else ci_base
    if not _FULL_SHA_RE.fullmatch(ci_base):
        raise ValueError(f"ci_base {ci_base!r} is not a full 40-hex sha")
    workdir = Path(workdir)
    record: dict = {"schema": SCHEMA, "side": "integration", "run_branch": run_branch,
                    "scratch_branch": scratch_branch, "base_sha": base, "onto_sha": onto, "ci_base_sha": ci_base, "run_sha": None,
                    "run_cut_from_base": None}
    listed = run(["git", "ls-remote", "--heads", "origin", run_branch], cwd=root, timeout=120)
    run_sha = _exact_head(listed.stdout, run_branch) if listed.returncode == 0 else None
    if not run_sha:
        record["note"] = f"the run branch {run_branch} is not on origin: nothing to merge"
        return record
    record["run_sha"] = run_sha
    fetched = run(["git", "fetch", "origin", run_branch], cwd=root, timeout=300)
    if fetched.returncode != 0:
        record["note"] = f"git fetch of {run_branch} exited {fetched.returncode}"
        return record

    created = pushed = False
    try:
        added = run(["git", "worktree", "add", "-b", scratch_branch, str(workdir), onto],
                    cwd=root, timeout=300)
        if added.returncode != 0:
            record["note"] = f"git worktree add exited {added.returncode}"
            return record
        created = True
        merge_base = run(["git", "merge-base", base, run_sha], cwd=root, timeout=120)
        record["run_cut_from_base"] = (merge_base.returncode == 0
                                       and merge_base.stdout.strip() == base)
        merged = run(["git", "merge", "--no-ff", "--no-edit", "-m",
                      f"Merge {run_branch} @ {run_sha[:8]} (parity integration leg, scratch)",
                      run_sha], cwd=workdir, timeout=300)
        record["merge"] = {"exit": merged.returncode, "sha": None, "parents": []}
        if merged.returncode != 0:
            return record
        head = run(["git", "rev-parse", "HEAD"], cwd=workdir, timeout=60).stdout.strip()
        parents = run(["git", "rev-list", "--parents", "-n", "1", "HEAD"], cwd=workdir,
                      timeout=60).stdout.split()
        record["merge"].update(sha=head or None, parents=parents[1:])
        tested = run(list(outcome_test), cwd=workdir, timeout=3600)
        counted = re.search(r"(\d+) passed", tested.stdout or "")
        record["outcome_test"] = {"argv": list(outcome_test), "exit": tested.returncode,
                                  "passed": int(counted.group(1)) if counted else 0}
        if tested.returncode != 0 or not head:
            return record
        push = run(["git", "push", "origin", f"HEAD:refs/heads/{scratch_branch}"], cwd=workdir,
                   timeout=300)
        pushed = push.returncode == 0
        record["push_exit"] = push.returncode
        if pushed:
            record["ci"] = _read_ci(head, base=ci_base, root=root, timeout_s=ci_timeout_s,
                                    interval_s=ci_interval_s, verdict_fn=verdict_fn)
        return record
    finally:
        if pushed:
            run(["git", "push", "origin", "--delete", scratch_branch], cwd=root, timeout=300)
        if created:
            run(["git", "worktree", "remove", "--force", str(workdir)], cwd=root, timeout=300)
            # DECIDED-BY-LANE: `-D`, not `-d`. The scratch branch is unmerged into main BY DESIGN
            # (it is the test lane's merge, never landed), so `-d` can only refuse; it is this
            # call's own branch, created above, and deleted only after it was pushed or abandoned.
            run(["git", "branch", "-D", scratch_branch], cwd=root, timeout=60)
        record["cleanup"] = _read_cleanup(run, root, scratch_branch, workdir)


def default_onto(run: Runner, *, root: Path, base: str) -> str:
    """The main commit the integrator cuts its scratch branch from: the one `base` ALREADY contains
    -- `git merge-base origin/main <base>` after a fetch.

    The integrator lands a lane it has synced to main. Cutting from the CURRENT origin/main instead
    made every lane that main had outrun conflict on the generated files both sides regenerate
    (b2-codespace-green run 3: `ecosystem/doc-counts.md`), which says main moved, not that the
    lane is wrong. A lane that is not synced is the integrator's re-sync, not this tool's guess."""
    fetched = run(["git", "fetch", "origin", "main"], cwd=root, timeout=300)
    if fetched.returncode != 0:
        raise ValueError(f"git fetch origin main exited {fetched.returncode}: pass --onto explicitly")
    found = run(["git", "merge-base", "origin/main", base], cwd=root, timeout=120)
    onto = found.stdout.strip() if found.returncode == 0 else ""
    if not _FULL_SHA_RE.fullmatch(onto):
        raise ValueError(f"no merge-base of origin/main and {base}: pass --onto explicitly")
    return onto


def _read_ci(sha: str, *, base: str, root: Path, timeout_s: int, interval_s: int,
             verdict_fn: Optional[Callable]) -> dict:
    try:
        verdict = (verdict_fn or _default_verdict)(sha, base=base, root=root, timeout_s=timeout_s,
                                                   interval_s=interval_s)
    except Exception as exc:  # noqa: BLE001 -- an unreadable CI is NOT-RUN, said by name
        return {"sha": sha, "state": "GH-UNAVAILABLE", "landable": False, "run_id": None,
                "missing_contexts": [], "reason": f"{type(exc).__name__}: {exc}"[:300]}
    state = str(getattr(verdict, "state", "") or "")
    missing = [str(c) for c in (getattr(verdict, "missing_contexts", ()) or ())]
    return {"sha": sha, "state": state, "landable": state in CI_LANDABLE_STATES and not missing,
            "run_id": getattr(verdict, "run_id", None), "missing_contexts": missing,
            "reason": str(getattr(verdict, "reason", "") or "")[:300],
            "new_reds": [str(r) for r in (getattr(verdict, "new_reds", ()) or ())][:40],
            "flagged": [str(f) for f in (getattr(verdict, "flagged", ()) or ())][:20]}


def _read_cleanup(run: Runner, root: Path, scratch_branch: str, workdir: Path) -> dict:
    """What is PROVEN gone, each read back: the scratch ref on origin, the worktree, the local
    branch. A read that could not be made is False -- 'could not look' is not 'gone'."""
    heads = run(["git", "ls-remote", "--heads", "origin", scratch_branch], cwd=root, timeout=120)
    remote_gone = heads.returncode == 0 and _exact_head(heads.stdout, scratch_branch) is None
    trees = run(["git", "worktree", "list", "--porcelain"], cwd=root, timeout=60)
    here = Path(workdir).as_posix().lower()
    worktree_gone = trees.returncode == 0 and here not in trees.stdout.replace("\\", "/").lower()
    local = run(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{scratch_branch}"],
                cwd=root, timeout=60)
    return {"remote_deleted": remote_gone, "worktree_removed": worktree_gone,
            "local_branch_removed": local.returncode != 0 and local.returncode != 127}


def collect_record(run: Runner = default_run, *, root: Path = _REPO_ROOT, side: str = "",
                   push_branch: Optional[str] = None, via_gate: bool = False,
                   skip_gates: bool = False, probe_write: Optional[str] = None) -> dict:
    if probe_write is not None and not _probe_name_ok(probe_write):
        # refused BEFORE the gates run: a bad name must not cost a long collect to find out
        raise ValueError(f"--probe-write {probe_write!r} is not a single plain file name, or "
                         "one file directly inside to-browser/")
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
        "transport": collect_transport(run, probe_write=probe_write),
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

def compare_environment(local: Mapping, remote: Mapping,
                        registry: Optional[Mapping] = None) -> Verdict:
    le, re_ = local["environment"], remote["environment"]
    registry = load_registry() if registry is None else registry
    problems: list[str] = []
    evidence: list[str] = []
    for key in sorted(set(le) | set(re_)):
        if key in OS_SPECIFIC_ENTRIES:
            evidence.append(f"{key}: declared OS-specific ({OS_SPECIFIC_ENTRIES[key]}) -- "
                            f"local={le.get(key)} codespace={re_.get(key)}")
            continue
        if key in ("tools", "uv_sync_exit", "hooks", "auth", "models"):
            continue    # compared below, each with its own verdict wording
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
    model_named = _compare_models(le, re_, registry, problems, evidence)
    auth_items = _auth_items(le, re_, evidence, model_named)
    for name in LANE_TOOLS:     # an auth probe that never ran is a FAIL, not a named exception
        if ((re_.get("auth") or {}).get(name) or {}).get("state") == "probe-error":
            problems.append(f"the auth probe for {name} could not run on the codespace -- its "
                            "login state is unknown")
    if problems:
        return _verdict(1, "FAIL", "; ".join(problems), evidence)
    if auth_items:
        return _verdict(1, "PASS", "except named auth items: " + ", ".join(auth_items), evidence)
    return _verdict(1, "PASS", "", evidence)


def _compare_models(le: Mapping, re_: Mapping, registry: Mapping, problems: list[str],
                    evidence: list[str]) -> set[str]:
    """Each model CLI's served id against the registry (R61), on both sides. Returns the CLIs the
    CODESPACE could not probe for want of a login: they are named as auth items, never failed, never
    passed silently. The workstation is the reference, so a local CLI with no served id fails."""
    expected = expected_models(registry)
    named: set[str] = set()
    for cli in MODEL_CLIS:
        if not expected[cli].id:
            problems.append(f"the registry names no model for {cli} ({expected[cli].where}): "
                            "its served id cannot be checked")
    for side, env in (("local", le), ("codespace", re_)):
        models = env.get("models")
        if not isinstance(models, Mapping):
            problems.append(f"no served model id on the {side}: the record has no model probe "
                            f"({', '.join(MODEL_CLIS)})")
            continue
        for cli in MODEL_CLIS:
            rec = models.get(cli) or {}
            state, served, exp = rec.get("state"), rec.get("served_id"), expected[cli]
            if state == "tool-absent":
                continue    # reported once, by the tool comparison above
            if state in ("not-probed-auth", "unauthenticated") and side == "codespace":
                evidence.append(f"served model {cli} {side}: not probed -- login missing "
                                "(a named auth item)")
                named.add(cli)
                continue
            if state == "served" and served:
                evidence.append(f"served model {cli} {side}={served} registry={exp.id} ({exp.where})")
                if exp.id and not served_matches(cli, served, exp.id):
                    problems.append(f"{cli} served {served!r} on the {side} but the registry routes "
                                    f"it to {exp.id!r} ({exp.where})")
                continue
            detail = rec.get("detail") or "no detail recorded"
            evidence.append(f"served model {cli} {side}: none ({state or 'no record'})")
            problems.append(f"{cli} returned no served model id on the {side} "
                            f"({state or 'no record'}: {detail})")
    return named


def _auth_items(le: Mapping, re_: Mapping, evidence: list[str],
                model_named: Sequence[str] = ()) -> list[str]:
    """The tools the Codespace has installed but not logged in, each named with what it needs.

    An exception is only ever NAMED here -- it neither fails condition 1 (installation is what
    condition 1 measures) nor passes silently. A record with no `auth` section (an older one)
    names nothing, so no exception can be invented for a side that was never probed. A CLI whose
    model call found the login missing (`model_named`) is named even where its auth state was
    `unprobed`, which is the only state `grok` and `agy` can have before they answer."""
    named: list[str] = []
    for name in LANE_TOOLS:
        theirs = (re_.get("auth") or {}).get(name)
        if name not in model_named and (
                not theirs or theirs.get("state") in ("authenticated", "tool-absent", "probe-error")):
            continue    # tool-absent and probe-error are each their own FAIL, not an exception
        ours = ((le.get("auth") or {}).get(name) or {}).get("state")
        evidence.append(f"AUTH-ITEM {name}: codespace={(theirs or {}).get('state', 'unprobed')} "
                        f"local={ours} -- needs {AUTH_NEEDS[name]}")
        named.append(name)
    return named


def compare_gates(local: Mapping, remote: Mapping) -> Verdict:
    lg, rg = local["gates"], remote["gates"]
    problems: list[str] = []
    evidence: list[str] = []
    for side, g in (("local", lg), ("codespace", rg)):
        if not g.get("tests"):
            problems.append(f"empty pytest selection on {side} -- nothing ran, nothing to compare")
        hooks = g.get("hooks") or {}
        unexercised = [h for h in GATE_HOOKS if hooks.get(h) in (None, "", "unknown", "skipped")]
        if unexercised or g.get("audit_health") not in ("pass", "fail"):
            problems.append(f"the pre-commit hooks or audit.py health never ran on {side} -- two "
                            "empty verdict sets compare equal on nothing")
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
        if key in DECLARED_OS_CASES and key not in declared_cases_problems():
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


def integration_legs(local: Mapping, integration: Optional[Mapping],
                     evidence: list[str]) -> list[LegResult]:
    """C3's integrator legs, each judged from what `integrate` MEASURED. A leg whose record is
    absent or carries no result is `NOT_RUN`; one that ran and failed is `FAIL`; only a measured
    pass is `PASS`. CI is judged by its STATE (`landable` is a convenience flag, never trusted)."""
    if not isinstance(integration, Mapping):
        return [LegResult(Leg.NOT_RUN, f"merge leg NOT-RUN: {LANDING_MERGE_NOT_RUN_REASON}")]
    legs: list[LegResult] = []
    base = local.get("base_sha")

    merge = integration.get("merge")
    if not isinstance(merge, Mapping) or merge.get("exit") is None:
        legs.append(LegResult(Leg.NOT_RUN, "merge leg NOT-RUN: no merge was attempted "
                              f"({integration.get('note') or 'the record carries none'})"))
    else:
        parents = list(merge.get("parents") or [])
        evidence.append(f"merge: {integration.get('scratch_branch')} merged "
                        f"{integration.get('run_branch')} at {integration.get('run_sha')} onto "
                        f"{integration.get('onto_sha') or integration.get('base_sha')} (base "
                        f"{integration.get('base_sha')}) -> {merge.get('sha')} "
                        f"(exit {merge.get('exit')})")
        bad = []
        if integration.get("base_sha") != base:
            bad.append(f"the integration base {integration.get('base_sha')} is not the compared "
                       f"base {base}")
        if integration.get("run_cut_from_base") is not True:
            bad.append("the run branch was not cut from the compared base")
        if merge.get("exit") != 0:
            bad.append(f"merge exit {merge.get('exit')}")
        elif len(parents) != 2:
            bad.append(f"the merge commit is not a two-parent merge ({len(parents)} parent(s))")
        else:
            onto_sha = integration.get("onto_sha") or integration.get("base_sha")
            if parents[0] != onto_sha:
                bad.append(f"the merge's first parent {parents[0]} is not the commit the scratch "
                           f"branch was cut from ({onto_sha})")
            if parents[1] != integration.get("run_sha"):
                bad.append(f"the merge's second parent {parents[1]} is not the run branch tip")
        legs.append(LegResult(Leg.FAIL, "; ".join(bad)) if bad else
                    LegResult(Leg.PASS, "merge"))

    outcome = integration.get("outcome_test")
    if not isinstance(outcome, Mapping) or outcome.get("exit") is None:
        legs.append(LegResult(Leg.NOT_RUN, "outcome test NOT-RUN: it was not re-run on the merge"))
    else:
        evidence.append(f"outcome test: exit {outcome.get('exit')}, {outcome.get('passed')} "
                        f"passed ({' '.join(outcome.get('argv') or [])})")
        if outcome.get("exit") != 0:
            legs.append(LegResult(Leg.FAIL, f"outcome test exit {outcome.get('exit')} on the merge"))
        elif not isinstance(outcome.get("passed"), int) or outcome["passed"] < 1:
            legs.append(LegResult(Leg.FAIL, "outcome test passed no test on the merge (a run that "
                                  "selected nothing is not a pass)"))
        else:
            legs.append(LegResult(Leg.PASS, "outcome test"))

    ci = integration.get("ci")
    state = str((ci or {}).get("state") or "") if isinstance(ci, Mapping) else ""
    if not isinstance(ci, Mapping):
        legs.append(LegResult(Leg.NOT_RUN, "CI verdict NOT-RUN: the scratch branch's push run "
                              "was not read"))
    else:
        evidence.append(f"CI: {state or '(no state)'} for {ci.get('sha')} (run {ci.get('run_id')}"
                        f"; missing contexts {list(ci.get('missing_contexts') or [])})")
        merge_sha = (merge or {}).get("sha") if isinstance(merge, Mapping) else None
        if state in CI_FAILED_STATES:
            legs.append(LegResult(Leg.FAIL, f"CI verdict {state}: {ci.get('reason') or 'red'}"))
        elif state in CI_LANDABLE_STATES:
            if merge_sha and ci.get("sha") != merge_sha:
                legs.append(LegResult(Leg.FAIL, f"the CI verdict is for {ci.get('sha')}, not the "
                                      f"merge commit {merge_sha}"))
            elif ci.get("missing_contexts"):
                legs.append(LegResult(Leg.FAIL, "CI verdict has missing required contexts: "
                                      + ", ".join(map(str, ci["missing_contexts"]))))
            else:
                legs.append(LegResult(Leg.PASS, "CI verdict"))
        else:
            legs.append(LegResult(Leg.NOT_RUN, f"CI verdict NOT-RUN: state {state!r} is not a "
                                  "measured pass or fail"))

    cleanup = integration.get("cleanup")
    if not isinstance(cleanup, Mapping):
        legs.append(LegResult(Leg.NOT_RUN, "scratch cleanup NOT-RUN: nothing was read back"))
    else:
        left = [k for k in ("remote_deleted", "worktree_removed", "local_branch_removed")
                if cleanup.get(k) is not True]
        evidence.append(f"scratch cleanup read back: {dict(cleanup)}")
        legs.append(LegResult(Leg.FAIL, "the scratch integration was not cleaned up: "
                              + ", ".join(left)) if left else LegResult(Leg.PASS, "scratch cleanup"))
    return legs


def compare_landing(local: Mapping, remote: Mapping,
                    integration: Optional[Mapping] = None) -> Verdict:
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
    push_leg = (LegResult(Leg.PASS, "push") if pushed else
                LegResult(Leg.NOT_RUN, f"push leg not exercised (the Codespace pushed no branch; "
                          f"push exit {landing.get('push_exit')})"))
    status, reason = fold_legs([push_leg, *integration_legs(local, integration, evidence)])
    return _verdict(3, status, reason, evidence)


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
                f"{t.get('read_entries')} entries; local {lt.get('read_entries')})"]
    write = t.get("write")
    if write is None:
        evidence.append(f"write: NOT-RUN -- {TRANSPORT_WRITE_NOT_RUN_REASON}")
        if problems:
            return _verdict(4, "FAIL", "; ".join(problems), evidence)
        return _verdict(4, "NOT-RUN", TRANSPORT_WRITE_NOT_RUN_REASON, evidence)
    # The write leg ran (`collect --probe-write`): it is judged on its own steps, and a good write
    # never rescues a failed read.
    name = write.get("name")
    wp: list[str] = []
    if not name:
        wp.append("the write probe carries no file name")
    elif write.get("write_exit") != 0:
        wp.append(f"write exit {write.get('write_exit')}")
    else:
        if not write.get("readback_ok"):
            wp.append("the read-back of the probe file did not match what was written")
        if write.get("delete_exit") != 0:
            wp.append(f"delete exit {write.get('delete_exit')}")
    if name and write.get("gone_after") is not True:
        wp.append(f"probe file {name} is still on the transport (or its absence could not be read)")
    evidence.append(
        f"write: {'FAIL' if wp else 'PASS'} ({name}: write exit {write.get('write_exit')}, "
        f"read-back {'identical' if write.get('readback_ok') else 'NOT identical'}, delete exit "
        f"{write.get('delete_exit')}, absent afterwards {write.get('gone_after')})")
    problems.extend(wp)
    if problems:
        return _verdict(4, "FAIL", "; ".join(problems), evidence)
    return _verdict(4, "PASS", "", evidence)


def compare_cleanup(cleanup: Optional[Mapping]) -> Verdict:
    if cleanup is None:
        return _verdict(5, "NOT-RUN",
                        "no cleanup record supplied (run `verify-cleanup` after teardown)")
    problems = []
    evidence = []
    if cleanup.get("listing_exit") != 0 or cleanup.get("ls_remote_exit") != 0:
        problems.append("the cleanup record carries no read evidence (listing_exit and "
                        "ls_remote_exit must both be 0): it was not written by `verify-cleanup`")
    if cleanup.get("codespace_listed_after"):
        problems.append(f"codespace {cleanup.get('codespace')} still listed after teardown")
    if cleanup.get("branch_listed_after"):
        problems.append(f"branch {cleanup.get('branch')} still on origin")
    # the extra branches a run creates (the test lane's own, C3's scratch integration): each one
    # must carry a READ of its absence, and every read must say gone
    after = cleanup.get("extra_branches_listed_after")
    for extra in cleanup.get("extra_branches") or []:
        if not isinstance(after, Mapping) or extra not in after:
            problems.append(f"branch {extra} was named for cleanup but no read of it is recorded")
        elif after[extra] is not False:
            problems.append(f"branch {extra} still on origin")
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
    extras = list(cleanup.get("extra_branches") or [])
    evidence.append(f"codespace {cleanup.get('codespace')} and branch {cleanup.get('branch')} "
                    + (f"and {len(extras)} more branch(es) ({', '.join(extras)}) " if extras else "")
                    + "all gone")
    return _verdict(5, "PASS", "", evidence)


def compare_all(local: Mapping, remote: Mapping, cleanup: Optional[Mapping] = None,
                registry: Optional[Mapping] = None,
                integration: Optional[Mapping] = None) -> list[Verdict]:
    return [compare_environment(local, remote, registry), compare_gates(local, remote),
            compare_landing(local, remote, integration), compare_transport(local, remote),
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
              save_remote: Optional[Path] = None,
              integration_path: Optional[Path] = None) -> tuple[int, str]:
    """Compare the two records. Returns (exit code, report text); never raises.

    `integration_path` is the record `integrate` wrote: condition 3's merge, outcome-test and CI
    legs. Without it those legs are NOT-RUN and the check cannot exit 0.

    `save_remote` keeps the record read over gh: the Codespace is deleted at teardown, and a
    verdict whose remote evidence died with it cannot be re-derived (found on the first run)."""
    try:
        local = load_local(local_path)
    except LocalRecordUnusable as exc:
        return 4, _unavailable_report(str(exc), "LocalRecordUnusable")
    try:
        if remote_path is not None and codespace:
            raise RemoteUnavailable("both --remote and --codespace were given: a file would "
                                    "stand in for a Codespace that was never contacted -- give one")
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
    integration: Optional[dict] = None
    integration_problem = ""
    if integration_path is not None:
        try:
            integration = json.loads(Path(integration_path).read_text(encoding="utf-8"))
            if not isinstance(integration, dict) or integration.get("schema") != SCHEMA:
                integration_problem = "the integration record is not a schema-1 JSON object"
                integration = None
        except (OSError, json.JSONDecodeError) as exc:
            integration_problem = f"the integration record is unreadable ({exc})"
    verdicts = compare_all(local, remote, cleanup, integration=integration)
    if cleanup_problem:
        verdicts[4] = _verdict(5, "FAIL", cleanup_problem)
    if integration_problem:
        verdicts[2] = _verdict(3, "FAIL", integration_problem)
    code = exit_code(verdicts)
    return code, render_report(verdicts) + f"\nexit={code}"


# ============================================================================ verify-cleanup

def verify_cleanup(name: str, branch: str, created: str, deleted: str, machine: str,
                   run: Runner = default_run, *, root: Path = _REPO_ROOT,
                   extra_branches: Optional[Sequence[str]] = None) -> dict:
    """Condition 5's record: read AFTER teardown that the Codespace is not listed and the run
    branch (and every `extra_branches` entry -- the test lane's own, C3's scratch integration) is
    not on origin. A listing that cannot be read raises -- 'could not look' is not 'gone'."""
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
    record = {"schema": SCHEMA, "codespace": name, "machine": machine, "created": created,
              "deleted": deleted, "codespace_listed_after": name in names, "branch": branch,
              "branch_listed_after": _exact_head(heads.stdout, branch) is not None,
              "listing_exit": listing.returncode, "ls_remote_exit": heads.returncode}
    if extra_branches:
        after: dict[str, bool] = {}
        for extra in extra_branches:
            more = run(["git", "ls-remote", "--heads", "origin", extra], cwd=root, timeout=120)
            if more.returncode != 0:
                raise RemoteUnavailable(f"git ls-remote exited {more.returncode} for {extra}: "
                                        "cannot say the branch is gone")
            after[extra] = _exact_head(more.stdout, extra) is not None
        record["extra_branches"] = list(extra_branches)
        record["extra_branches_listed_after"] = after
    return record


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
@click.option("--probe-write", "probe_write", default=None,
              help="Condition 4's write leg: write, read back and delete this ONE file name on "
                   "the transport (a root-level name or one file directly in to-browser/; a "
                   "contract must name it). Default: not exercised.")
def collect_cmd(out: Path, side: str, push_branch: Optional[str], via_gate: bool,
                skip_gates: bool, probe_write: Optional[str]) -> None:
    """Build this environment's record (conditions 1-4's evidence) and write it to --out."""
    try:
        record = collect_record(side=side, push_branch=push_branch, via_gate=via_gate,
                                skip_gates=skip_gates, probe_write=probe_write)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc
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
@click.option("--integration", "integration_path", default=None, type=click.Path(path_type=Path),
              help="The record `integrate` wrote: condition 3's merge / outcome-test / CI legs.")
def check_cmd(local_path: Path, remote_path: Optional[Path], codespace: Optional[str],
              remote_file: str, cleanup_path: Optional[Path], save_remote: Optional[Path],
              integration_path: Optional[Path]) -> None:
    """One verdict per condition; exit 0 all PASS | 1 FAIL | 2 NOT-RUN | 3 remote unavailable."""
    code, text = run_check(local_path, remote_path=remote_path, codespace=codespace,
                           remote_file=remote_file, cleanup_path=cleanup_path,
                           save_remote=save_remote, integration_path=integration_path)
    click.echo(text)
    sys.exit(code)


@cli.command("integrate")
@click.option("--run-branch", required=True, help="The test lane's pushed branch (worktree-<slug>).")
@click.option("--scratch-branch", required=True, help="worktree-integrate-<slug>; never main.")
@click.option("--base", required=True, help="Full 40-hex sha the run branch was cut from.")
@click.option("--onto", default=None,
              help="Full sha the scratch branch is cut from; default: the main commit --base "
                   "already contains (`git merge-base origin/main <base>`). Not --base itself: "
                   "CI judges the push as if it landed on main.")
@click.option("--ci-base", "ci_base", default=None,
              help="Full sha whose CI run the merge's run is judged against; default: origin/main's "
                   "tip now (CI runs the scratch branch against the current main ref).")
@click.option("--workdir", required=True, type=click.Path(path_type=Path),
              help="Where the scratch worktree is created (and removed).")
@click.option("--test", "outcome_test", required=True,
              help="The outcome test as a JSON argv list, run on the merged tree.")
@click.option("--ci-timeout", "ci_timeout_s", default=3600, show_default=True, type=int)
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
def integrate_cmd(run_branch: str, scratch_branch: str, base: str, onto: Optional[str],
                  ci_base: Optional[str], workdir: Path, outcome_test: str, ci_timeout_s: int,
                  out: Path) -> None:
    """Condition 3's integration legs: merge the run branch on a scratch branch, test, read CI."""
    try:
        argv = json.loads(outcome_test)
        if not (isinstance(argv, list) and argv and all(isinstance(a, str) for a in argv)):
            raise ValueError("--test must be a non-empty JSON list of strings")
        if onto is None:
            onto = default_onto(default_run, root=_REPO_ROOT, base=base)
        if ci_base is None:
            listed = default_run(["git", "ls-remote", "--heads", "origin", "main"], cwd=_REPO_ROOT,
                                 timeout=120)
            ci_base = _exact_head(listed.stdout, "main") if listed.returncode == 0 else None
            if not ci_base:
                raise ValueError("could not read origin/main for the CI baseline: pass --ci-base")
        record = collect_integration(default_run, root=_REPO_ROOT, run_branch=run_branch,
                                     scratch_branch=scratch_branch, base=base, onto=onto,
                                     ci_base=ci_base, outcome_test=argv, workdir=workdir,
                                     ci_timeout_s=ci_timeout_s)
    except (ValueError, json.JSONDecodeError) as exc:
        raise click.UsageError(str(exc)) from exc
    write_record(out, record)
    click.echo(f"integration record written: merge={record.get('merge')} "
               f"ci={(record.get('ci') or {}).get('state')} -> {out}")


@cli.command("verify-cleanup")
@click.option("--codespace", "name", required=True)
@click.option("--branch", required=True)
@click.option("--created", required=True, help="ISO-8601 creation time.")
@click.option("--deleted", required=True, help="ISO-8601 deletion time.")
@click.option("--machine", required=True)
@click.option("--also-branch", "also_branches", multiple=True,
              help="Another branch that must be gone from origin (repeatable): the integration "
                   "scratch branch.")
@click.option("--out", "out", required=True, type=click.Path(path_type=Path))
def verify_cleanup_cmd(name: str, branch: str, created: str, deleted: str, machine: str,
                       also_branches: tuple[str, ...], out: Path) -> None:
    """After teardown: read that the Codespace and the run branch are gone; write the record."""
    try:
        record = verify_cleanup(name, branch, created, deleted, machine,
                                extra_branches=list(also_branches) or None)
    except RemoteUnavailable as exc:
        click.echo(f"FAILURE RemoteUnavailable: {exc}")
        sys.exit(3)
    write_record(out, record)
    click.echo(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    cli()
