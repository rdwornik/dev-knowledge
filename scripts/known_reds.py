#!/usr/bin/env python
"""known_reds.py -- the known-reds organ (ADR-121 step 1, LANE-5A-1).

WHY THIS EXISTS. `logs/SUITE-BASELINE-FREEZE.md` compares a run to a frozen roster of node ids,
but the roster carries no identity beyond a measurement SHA, and a red that lands ABOVE the
freeze is invisible until the next re-measure -- which is exactly how CI's regression count rose
from 9 to 17 while every batch's own local registry (`scripts/test_pairing.py`) reported clean:
each batch only knows the reds present when IT started, so a regression from an EARLIER batch
reads as "pre-existing" forever. `to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md` C5d/C7/C8
names this "laundering."

WHAT THIS MODULE ADDS, on top of `logs/SUITE-BASELINE-FREEZE.md`'s node-id-membership idea:
  1. **A baseline id** (`<date>-<content hash>`) stamped on every verdict this module renders,
     so a disagreement between two verdicts is visible as "different baseline" rather than silent
     (ADR-121 D5).
  2. **Attribution.** Every member of the registry carries either a real attribution
     (`{"first_bad_sha", "lane"}`, found by `attribute`'s `git bisect run`), `"pre-freeze"`
     (inherited from the 2026-09-17 measurement, before this organ existed), `"witness"` (the
     four `[#664]` commit-tier tests, deliberately kept OUT of every frozen/known set so a run
     showing them is never silently absorbed), or `"unattributed"` with a reason. No member is
     anonymous (done-contract item 2).
  3. **`refresh` refuses to launder.** A currently-failing node id that was not already a
     registry member and has no attribution in the supplied `--attribution` file is a REFUSAL,
     not a silent addition (done-contract item 5) -- the opposite of what a raw re-measure of
     the old freeze file would do.

THE REGISTRY IS COMMITTED, THE BATCH REGISTRY IS NOT. `scripts/test_pairing.py`'s
`TEST-PAIRING-REGISTRY-<BATCH>.json` is gitignored and per-batch by design (recording it twice
would launder a lane's red into "pre-existing" for every OTHER lane of that batch -- see that
module's own docstring). This module's registry answers a different question -- "what does CI,
which has no batch context, already know about" -- so it lives at a path convention alongside
the other committed suite artifact it supersedes: `logs/KNOWN-REDS-REGISTRY.json`, sibling to
`logs/SUITE-BASELINE-FREEZE.md`. The two coexist until one CI run has judged a push against the
registry and come back green or with its new reds named (done-contract item 4); only then does
the frozen prose file retire.

THE BISECT WRAPPER (`attribute`) is a CLONE, never the caller's own worktree -- same
`ISOLATION_REASON` as `scripts/test_pairing.py`: `git bisect` repeatedly checks out different
commits, and doing that in a worktree several other tools read (`git worktree list`, open
editors, a live session's cwd) would make the checkout itself part of what is being measured.
Each bisect step runs the ONE named test, nothing else, and reports one of three outcomes to
`git bisect run`: 0 (good -- passed), 1 (bad -- collected and failed), 125 (skip -- the test
does not exist or does not collect at this commit, e.g. because the file was added later). `git
bisect run`'s own skip-tolerant binary search converges on the first commit where the test both
EXISTS and FAILS, which is what "first bad sha" means here even when the test file itself is
younger than the comparison range's start.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import conductor  # noqa: E402 -- parse_failed_node_ids is the shared, tested extractor

SCHEMA = "known-reds-registry/1"
REGISTRY_PATH = "logs/KNOWN-REDS-REGISTRY.json"
EXIT_UNCOMPARABLE = 2

WITNESS = "witness"
PRE_FREEZE = "pre-freeze"
UNATTRIBUTED = "unattributed"

#: The four [#664] commit-tier witnesses: `logs/SUITE-BASELINE-FREEZE.md` keeps them OUT of its
#: frozen set on purpose so every run keeps reporting them; this registry keeps them OUT of
#: `red`'s "known and quiet" bucket for the same reason, but tracks them by name (never
#: anonymous) with attribution "witness" rather than leaving them to read as ordinary regressions.
WITNESS_MEMBERS = (
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_live_spine_is_ordered_rebuild_first_and_always_runs",
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-orphan-census]",
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-process-list]",
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-task-coverage]",
)


class KnownRedsError(RuntimeError):
    """The organ could not produce a verdict (as opposed to producing a red verdict)."""


# --- baseline identity --------------------------------------------------------------------

def compute_baseline_id(members: dict, *, date: str) -> str:
    """`<date>-<12 hex chars>`; the hash is over the sorted (id, attribution) pairs, so two
    registries with the same members and the same attributions always share a baseline id
    regardless of dict insertion order, and any change to who-is-known or why changes it."""
    canonical = json.dumps({k: members[k] for k in sorted(members)}, sort_keys=True)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
    return f"{date}-{digest}"


# --- registry ------------------------------------------------------------------------------

@dataclass(frozen=True)
class Registry:
    schema: str
    baseline_id: str
    measured_at_sha: str
    measured_via: str
    workers: int
    members: dict  # {node_id: {"attribution": ...} | {"attribution": ..., "reason": ...}}
    notes: tuple = field(default_factory=tuple)

    def to_json(self) -> dict:
        return {"schema": self.schema, "baseline_id": self.baseline_id,
                "measured_at_sha": self.measured_at_sha, "measured_via": self.measured_via,
                "workers": self.workers,
                "members": {k: self.members[k] for k in sorted(self.members)},
                "notes": list(self.notes)}

    @classmethod
    def from_json(cls, data: dict, source: str) -> Registry:
        if data.get("schema") != SCHEMA:
            raise KnownRedsError(f"{source}: schema {data.get('schema')!r}, expected {SCHEMA!r}")
        try:
            return cls(schema=data["schema"], baseline_id=data["baseline_id"],
                       measured_at_sha=data["measured_at_sha"], measured_via=data["measured_via"],
                       workers=int(data["workers"]), members=dict(data["members"]),
                       notes=tuple(data.get("notes", ())))
        except (KeyError, TypeError) as exc:
            raise KnownRedsError(f"{source}: malformed registry field: {exc}") from exc


def load_registry(path: Path) -> Registry:
    if not path.is_file():
        raise KnownRedsError(f"no registry at {path}: an absent registry must not read as "
                             "'nothing is known' -- run `refresh` first")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise KnownRedsError(f"{path}: not valid JSON: {exc}") from exc
    return Registry.from_json(data, str(path))


def write_registry(path: Path, registry: Registry) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry.to_json(), indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")


# --- refresh: build/update the registry from a run + attribution evidence ------------------

def refresh(*, failed: frozenset, workers: int, commit: str, measured_via: str, date: str,
            attribution: dict, previous: Registry | None) -> tuple[Registry, list[str]]:
    """Build the next registry. `attribution` supplies evidence for ids not already carried
    from `previous` (each value is `{"attribution": ...}` or `{"attribution": ..., "reason":
    ...}`). Returns (registry, dropped) where `dropped` lists previous members no longer
    failing (informational -- they are simply not carried forward, never re-added).

    Raises KnownRedsError naming every currently-failing id that is neither carried from
    `previous` nor present in `attribution`: a refresh that could not attribute a NEW red must
    refuse rather than silently file it as known (done-contract item 5).
    """
    prev_members = dict(previous.members) if previous else {}
    members: dict = {}
    missing: list[str] = []
    for node_id in failed:
        if node_id in WITNESS_MEMBERS:
            members[node_id] = {"attribution": WITNESS,
                                "reason": "[#664] commit-tier witness -- deliberately never "
                                          "frozen; a run showing it is expected, not a surprise"}
        elif node_id in prev_members:
            members[node_id] = prev_members[node_id]
        elif node_id in attribution:
            members[node_id] = dict(attribution[node_id])
        else:
            missing.append(node_id)
    if missing:
        raise KnownRedsError(
            "refresh refused: " + str(len(missing)) + " currently-failing id(s) are neither "
            "carried from the previous registry nor attributed in --attribution -- a refresh "
            "never adds an unattributed red:\n  " + "\n  ".join(sorted(missing)))
    dropped = sorted(set(prev_members) - failed)
    baseline_id = compute_baseline_id(members, date=date)
    registry = Registry(schema=SCHEMA, baseline_id=baseline_id, measured_at_sha=commit,
                        measured_via=measured_via, workers=workers, members=members,
                        notes=previous.notes if previous else ())
    return registry, dropped


# --- compare: CI's own comparator, replacing a node-id diff against the prose freeze -------

def compare(failed: frozenset, registry: Registry, *, workers: int,
            pytest_exit: int | None = None) -> dict:
    """Judge one run against `registry`. Mirrors `conductor.suite_gate`'s shape (verdict,
    reason, regressions, pre_existing) plus `baseline_id` on every branch (done-contract item 3)
    and a `witnesses` bucket so a [#664] witness is reported by name, not folded into either
    'pre-existing' (which would hide that it is DESIGNED to fail) or 'regressions' (which would
    make every run report a fail that arming required-checks could never clear).
    """
    base = {"baseline_id": registry.baseline_id}
    if pytest_exit is not None and pytest_exit not in (0, 1):
        return {**base, "verdict": "fail",
                "reason": f"NOT COMPARABLE -- pytest itself exited {pytest_exit}",
                "regressions": [], "pre_existing": [], "witnesses": [], "unattributed": []}
    if workers != registry.workers:
        return {**base, "verdict": "fail",
                "reason": f"NOT COMPARABLE -- resolved at {workers} workers, the registry is "
                          f"pinned at {registry.workers}",
                "regressions": [], "pre_existing": [], "witnesses": [], "unattributed": []}
    known = registry.members
    regressions = sorted(n for n in failed if n not in known)
    pre_existing = sorted(n for n in failed if n in known
                          and known[n]["attribution"] not in (WITNESS,))
    witnesses = sorted(n for n in failed if n in known and known[n]["attribution"] == WITNESS)
    unattributed_known = sorted(n for n in pre_existing if known[n]["attribution"] == UNATTRIBUTED)
    if regressions:
        return {**base, "verdict": "fail",
                "reason": f"REGRESSION -- {len(regressions)} failure(s) not in the registry "
                          f"(baseline {registry.baseline_id})",
                "regressions": regressions, "pre_existing": pre_existing,
                "witnesses": witnesses, "unattributed": unattributed_known}
    return {**base, "verdict": "pass",
            "reason": f"{len(pre_existing)} known failure(s), {len(witnesses)} witness(es), "
                      f"0 outside the registry (baseline {registry.baseline_id})",
            "regressions": [], "pre_existing": pre_existing, "witnesses": witnesses,
            "unattributed": unattributed_known}


def render_compare(result: dict) -> str:
    """Flat key/value + bullet lines (CLAUDE.md section 4): no pipe tables."""
    lines = ["known-reds compare", "", f"baseline id    : {result['baseline_id']}"]
    lines.append(f"pre-existing   : {len(result['pre_existing'])}")
    for nid in result["pre_existing"]:
        lines.append(f"  known         {nid}")
    lines.append(f"witnesses      : {len(result['witnesses'])}")
    for nid in result["witnesses"]:
        lines.append(f"  witness       {nid}")
    lines.append(f"regressions    : {len(result['regressions'])}")
    for nid in result["regressions"]:
        lines.append(f"  REGRESSION    {nid}")
    if result["unattributed"]:
        lines.append(f"unattributed known members still failing: {len(result['unattributed'])}")
        for nid in result["unattributed"]:
            lines.append(f"  UNATTRIBUTED  {nid}")
    lines.append("")
    lines.append(f"verdict        : {result['verdict'].upper()} -- {result['reason']}")
    return "\n".join(lines)


# --- attribute: the git-bisect-run wrapper --------------------------------------------------

#: See the module docstring's "THE BISECT WRAPPER" paragraph for why this is a clone.
ISOLATION_REASON = (
    "a clone, not a worktree: git bisect repeatedly checks out different commits, and several "
    "tests read `git worktree list`, so bisecting in a worktree would make the checkout itself "
    "part of what is being measured"
)

_FIRST_BAD_RE = re.compile(r"^([0-9a-f]{40}) is the first 'bad' commit", re.MULTILINE)


def _git(repo: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    if done.returncode != 0:
        raise KnownRedsError(f"git {' '.join(args)} failed: "
                             f"{done.stderr.strip() or done.stdout.strip()}")
    return done.stdout.strip()


def find_lane(repo: Path, first_bad_sha: str, bad_ref: str) -> str | None:
    """The `worktree-<lane>` name of the first merge on the ancestry path from `first_bad_sha`
    to `bad_ref` -- the merge that actually carried it into main -- or `None` if `first_bad_sha`
    itself is that merge (a lane's tip merged with no fix-up commits after it), in which case
    the caller already has the merge subject line to parse, or if no merge is found at all
    (the range never merges, e.g. a still-open branch)."""
    if first_bad_sha == _git(repo, "rev-parse", first_bad_sha):
        subject = _git(repo, "log", "-1", "--format=%s", first_bad_sha)
        m = re.match(r"^Merge branch '(?:worktree-)?([^']+)'", subject)
        if m:
            return m.group(1)
    out = _git(repo, "log", "--merges", "--ancestry-path", "--reverse", "--format=%s",
              f"{first_bad_sha}..{bad_ref}")
    first_line = out.splitlines()[0] if out else ""
    m = re.match(r"^Merge branch '(?:worktree-)?([^']+)'", first_line)
    return m.group(1) if m else None


def attribute(repo: Path, test_id: str, *, good: str, bad: str, venv_python: Path,
             workdir: Path | None = None, timeout: float = 180.0) -> dict:
    """`git bisect run` the ONE test between `good` (assumed to pass, or to not yet collect)
    and `bad` (assumed to fail). Returns
    `{"test": test_id, "first_bad_sha": sha, "lane": name_or_None, "bisect_log": text}`.

    Raises KnownRedsError if bisect could not converge (too many skips, or `good` itself fails).
    """
    scratch_root = Path(tempfile.mkdtemp(prefix="known-reds-", dir=workdir))
    clone = scratch_root / "clone"
    try:
        _git(scratch_root, "clone", "--quiet", "--shared", "--no-checkout", str(repo), str(clone))
        _git(clone, "bisect", "start", bad, good)
        step_script = Path(__file__).resolve()
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["_KNOWN_REDS_BISECT_TEST_ID"] = test_id
        env["_KNOWN_REDS_BISECT_VENV_PY"] = str(venv_python)
        env["_KNOWN_REDS_BISECT_CLONE"] = str(clone)
        env["_KNOWN_REDS_BISECT_TIMEOUT"] = str(timeout)
        done = subprocess.run(
            ["git", "bisect", "run", str(venv_python), str(step_script), "_bisect-step"],
            cwd=clone, capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env, check=False)
        log = done.stdout + done.stderr
        m = _FIRST_BAD_RE.search(log)
        if not m:
            raise KnownRedsError(f"bisect for {test_id!r} did not converge on a first-bad "
                                 f"commit:\n{log[-2000:]}")
        first_bad_sha = m.group(1)
        lane = find_lane(clone, first_bad_sha, bad)
        return {"test": test_id, "first_bad_sha": first_bad_sha, "lane": lane, "bisect_log": log}
    finally:
        # No `git bisect reset` needed: the whole clone is removed next, so there is nothing
        # left to leave in a detached-HEAD state.
        _rmtree(scratch_root)


def _rmtree(path: Path) -> None:
    import shutil
    import stat

    def _writable_then_retry(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    if path.exists():
        shutil.rmtree(path, onexc=_writable_then_retry)


def _bisect_step() -> int:
    """One `git bisect run` step, invoked as `<venv-python> known_reds.py _bisect-step` with
    the test id / venv / clone / timeout passed by environment (see `attribute`). Exit 0 good
    (passed), 1 bad (collected and failed), 125 skip (does not exist / does not collect here)."""
    test_id = os.environ["_KNOWN_REDS_BISECT_TEST_ID"]
    venv_py = os.environ["_KNOWN_REDS_BISECT_VENV_PY"]
    clone = os.environ["_KNOWN_REDS_BISECT_CLONE"]
    timeout = float(os.environ["_KNOWN_REDS_BISECT_TIMEOUT"])
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONPATH", None)
    cmd = [venv_py, "-m", "pytest", "-q", "--no-header", "--color=no", "-p", "no:cacheprovider",
          "--continue-on-collection-errors", test_id]
    try:
        done = subprocess.run(cmd, cwd=clone, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 125  # untestable at this commit within budget -- skip rather than misreport
    out = done.stdout + done.stderr
    sys.stderr.write(out[-2000:])
    lowered = out.lower()
    if "no tests ran" in lowered or "error: not found" in lowered or "collected 0 items" in out:
        return 125
    if done.returncode == 0:
        return 0
    if done.returncode == 1:
        return 1
    return 125  # collection error / interrupted / usage error: ambiguous, never call it bad


# --- CLI -------------------------------------------------------------------------------------

def _load_attribution_file(path: str | None) -> dict:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for node_id, entry in data.items():
        out[node_id] = entry if isinstance(entry, dict) else {"attribution": entry}
    return out


def main(argv: list[str] | None = None) -> int:
    if argv is None and len(sys.argv) > 1 and sys.argv[1] == "_bisect-step":
        return _bisect_step()

    ap = argparse.ArgumentParser(description="The known-reds organ: baseline id, attribution, "
                                            "and CI's comparator (ADR-121 step 1).")
    ap.add_argument("--repo-root", default=None)
    sub = ap.add_subparsers(dest="command", required=True)

    ref = sub.add_parser("refresh", help="build/update logs/KNOWN-REDS-REGISTRY.json")
    ref.add_argument("--pytest-output", required=True)
    ref.add_argument("--workers", required=True, type=int)
    ref.add_argument("--commit", required=True)
    ref.add_argument("--measured-via", default="local")
    ref.add_argument("--date", required=True, help="YYYY-MM-DD, for the baseline id")
    ref.add_argument("--attribution", default=None, help="JSON {node_id: {attribution, reason?}}")
    ref.add_argument("--previous", default=None, help="a prior registry to carry members from")
    ref.add_argument("--registry", default=REGISTRY_PATH)

    cmp_ = sub.add_parser("compare", help="judge a run against the committed registry")
    cmp_.add_argument("--pytest-output", required=True)
    cmp_.add_argument("--workers", required=True, type=int)
    cmp_.add_argument("--pytest-exit", default=None, type=int)
    cmp_.add_argument("--registry", default=REGISTRY_PATH)

    attr = sub.add_parser("attribute", help="git bisect run, one test, and name the lane")
    attr.add_argument("--test", required=True)
    attr.add_argument("--good", required=True)
    attr.add_argument("--bad", required=True)
    attr.add_argument("--venv-python", required=True)
    attr.add_argument("--workdir", default=None)
    attr.add_argument("--timeout", default=180.0, type=float)

    for p in (ref, cmp_, attr):
        p.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd()

    if args.command == "refresh":
        text = Path(args.pytest_output).read_text(encoding="utf-8", errors="replace")
        failed = conductor.parse_failed_node_ids(text)
        previous = load_registry(root / args.previous) if args.previous else None
        attribution = _load_attribution_file(args.attribution)
        try:
            registry, dropped = refresh(failed=failed, workers=args.workers, commit=args.commit,
                                        measured_via=args.measured_via, date=args.date,
                                        attribution=attribution, previous=previous)
        except KnownRedsError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        write_registry(root / args.registry, registry)
        report = (f"known_reds: wrote {args.registry} -- baseline {registry.baseline_id}, "
                 f"{len(registry.members)} member(s), {len(dropped)} dropped (no longer failing)")
        print(report)
        if args.out:
            Path(args.out).write_text(report + "\n", encoding="utf-8", newline="\n")
        return 0

    if args.command == "compare":
        text = Path(args.pytest_output).read_text(encoding="utf-8", errors="replace")
        failed = conductor.parse_failed_node_ids(text)
        try:
            registry = load_registry(root / args.registry)
        except KnownRedsError as exc:
            print(str(exc), file=sys.stderr)
            return EXIT_UNCOMPARABLE
        result = compare(failed, registry, workers=args.workers, pytest_exit=args.pytest_exit)
        report = render_compare(result)
        if args.out:
            Path(args.out).write_text(report + "\n", encoding="utf-8", newline="\n")
        print(report)
        return 0 if result["verdict"] == "pass" else 1

    if args.command == "attribute":
        result = attribute(root, args.test, good=args.good, bad=args.bad,
                           venv_python=Path(args.venv_python), workdir=Path(args.workdir)
                           if args.workdir else None, timeout=args.timeout)
        report = json.dumps({k: v for k, v in result.items() if k != "bisect_log"}, indent=2)
        print(report)
        if args.out:
            Path(args.out).write_text(json.dumps(result, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
        return 0

    return 1  # pragma: no cover -- argparse's `required=True` makes this unreachable


if __name__ == "__main__":
    sys.exit(main())
