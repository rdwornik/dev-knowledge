"""Test pairing -- which of the reds on a merge are the lane's, answered in minutes.

`main` carries reds nobody owns, so every merge needs one question answered: which of these did
THIS lane cause? The integrator used to answer it by hand -- clone the merge-base, run both trees,
diff the sets -- and it took an hour for one branch. This is that procedure as an organ. Its
specification is `to-browser/SESSION-integrator-loop-eval.md` section 4.

    test_pairing.py BASE HEAD            two commits
    test_pairing.py --lane NAME          BASE = merge-base(main, worktree-NAME), HEAD = that branch

WHAT IT REPORTS (all in the verdict artifact, `TEST-PAIRING-VERDICT.json`, UPPERCASE-KEBAB and
undated like every other receipt; stdout carries the same JSON):

  * `preexisting` -- red on BOTH commits. Somebody else's.
  * `lane`        -- red only on HEAD, minus flakes. Each entry says what it was on BASE:
                     `absent` (a test the lane added), or `PASSED` (a green the lane turned red).
  * `turned_red`  -- the `PASSED`-on-BASE subset of `lane`, named because it is the more
                     alarming half: nobody wrote a failing test, an existing one broke.
  * `flakes`      -- red on HEAD, but green on a rerun in isolation. Both observations are kept.
  * `fixed`       -- red on BASE, green on HEAD. Informational.

EXIT CODE: 0 nothing is the lane's; 1 the lane's set is non-empty; 2 the tool could not run;
3 the selection declined to narrow and there was nothing safe to fall back on (NOT-EVALUATED --
"I evaluated nothing" must not read as "nothing is red"); 4 the comparison is UNATTRIBUTABLE
(registry mode only: the skip counts differ, see below).

BATCH REGISTRY MODE (lane-known-reds, R-W4-2). The two-commit form above runs BASE and HEAD
for every lane, which is what cost the wave-3 integrator an hour a merge. A batch has ONE base,
so the base is run ONCE per batch and every lane is compared against that record:

    test_pairing.py record-base --commit REF --batch B (--lane NAME ... | --tests FILE ...)
    test_pairing.py compare     --head REF   --batch B [--since REF]

`record-base` runs the selected test files on the base commit once and writes the REGISTRY: the
red set, the passed ids, the skipped ids and their count. It refuses to overwrite a registry
(`--replace` says so out loud): re-recording mid-batch would launder a lane's red into "pre-existing".
`compare` runs only the merged tree -- the tests impacted by what changed since the base (or
`--since`) -- and classifies against the registry, with the same verdict keys as the two-commit form:
red in the registry AND the merged tree is `preexisting`; red only in the merged tree is `lane`
(`was: absent` -- a test the lane added -- or `PASSED` -- a registry green it turned red, listed
again in `turned_red`); a merged-tree red that passes on an isolated rerun is a `flake`.

THE SKIP-COUNT GUARD. A comparison whose skip count differs from the registry's, over the test
files both runs covered, is REFUSED as UNATTRIBUTABLE (exit 4, nothing classified): a lane that
skips, xfails or importorskips a test turns a red it would have shown into a green-looking skip,
and the integrator found that blind spot on 2026-09-20. Collection-level skips count too.

THE REGISTRY HOME. `RECON-NIGHT-2026-09-20.md` section 2.2 names exactly three admissible shapes
for a machine-written receipt and this is shape (a): a gitignored, per-batch file in
`logs/receipts/` (`HARNESS_RECEIPTS_DIR` overrides), UPPERCASE-KEBAB with no date in the name
(`TEST-PAIRING-REGISTRY-<BATCH>.json`), because `logs_retention.py` moves a dated name out from
under its own path. It is the home lane L1 chose for every receipt (`scripts/dodo.py`, `.gitignore`
"SPINE / MOMENT RECEIPTS"). Shape (b) is a committed flat file, which a per-batch target cannot be,
and shape (c) is a new committed directory, which needs an operator ruling; no option here writes
a registry anywhere else.

THE SELECTION IS `impacted_tests.select`, NOT THE FULL SUITE. When it declines to narrow (it
returns `full_suite` for an environment file, an unmapped path...) that is written into the
verdict (`selection.declined`, `selection.note`) and the run falls back to the test files the
diff itself changed -- never to everything. The full suite belongs to CI; no option here runs it.
That fallback is partial by construction, and the verdict says so.

FLAKE RULE. A red that appears once is not attributed on one observation. Each candidate is
rerun in isolation on HEAD; if any rerun passes it is a FLAKE and the lane is not charged for it.
A red that stays red keeps both observations, so the integrator can see it was tried twice.

BASELINE RULE. The same doubt applies to BASE: a pre-existing red that passes on a rerun on BASE
was never pre-existing and could be hiding a lane-caused red of the same id. The pre-existing
set is rerun once on BASE (batched); any that pass become lane candidates (`was:
red-once-on-base`) and face the HEAD rerun. `--no-confirm-baseline` skips this, cheaper and weaker.

FAILS CLOSED. No event file, a malformed event row, or a pytest exit code that contradicts the
events (failures reported, none recorded) is exit 2, never a CLEAN verdict. The caller's
PYTHONPATH is not passed on, and `--tests` takes files or node ids, never a directory.

HONEST LIMITS OF THE REGISTRY. A comparison is against the BASE the registry was recorded at, not
against main's moving tip, so a red an earlier lane of the batch left behind is charged to whichever
lane is compared next unless the integrator refused it first. A selected file the registry never
ran that ALREADY existed on the base has no known baseline, so the comparison is UNATTRIBUTABLE
(`unregistered` names them; `record-base --replace` with the lane included); a file the lane added
did not exist on the base and is the lane's. A docs-only selection is the `live_repo` marker,
resolved to its FILES (a superset, the direction `impacted_tests` itself takes). The skip guard
counts skips only over files both sides covered, and refuses any skip the registry lacked even
when the count is level.

HONEST LIMITS. (1) A test red on BASE for a flaky reason and green on HEAD shows as `fixed`.
(2) A test whose result depends on gitignored state (e.g. `ecosystem/*/state.yaml`) sees neither
side's copy -- both clones lack it, so it cannot skew the PAIR, but the reds it produces are
reds of a bare checkout. (3) `impacted_tests` measures a miss-rate of about one affected file in
twenty; a clean pairing is not a full-suite pass. (4) THE REGISTRY IS NODE-ID GRANULAR, NOT
FINDING GRANULAR (finding 8, DIGEST-WAVE4-FINAL-2026-09-22): a test already red in the registry
stays `preexisting` even when the LANE'S diff adds a second, distinct cause of that same test's
failure -- classification here is PASSED/FAILED per node id, and a node id carries no notion of
"which finding, or how many". This is not a bug to patch here: it is what "the registry compares
pytest outcomes" means, and widening it would mean parsing assertion messages per test, which no
option in this module does. THE INSTRUMENT THAT CAN SEE IT is whatever already reports FINDINGS
rather than a pass/fail verdict for the test wrapping them -- `scripts/decision_coverage.py check`
is the live example: it prints one `ProbeFinding` (`.subject`, `.evidence`) per uncovered decision,
so two decisions missing their row are TWO printed lines even while
`tests/test_decision_coverage.py::test_the_live_tree_carries_no_IN_ERA_uncovered_decision` is a
single red node id either way. A lane whose diff could plausibly ADD a finding inside an
already-red test should read that instrument directly rather than trust this registry to notice.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import impacted_tests  # noqa: E402

SCHEMA = "test-pairing/1"
VERDICT_NAME = "TEST-PAIRING-VERDICT.json"

#: The isolation is a CLONE, never a worktree, and this is the only reason that matters.
ISOLATION_REASON = (
    "a clone, not a worktree: several tests read `git worktree list`, so adding a worktree "
    "would itself change the result being measured"
)

_RED = ("FAILED", "ERROR")
_TEST_FILE = re.compile(r"(^|/)(test_[^/]*|[^/]*_test)\.py$")

#: LANE-5A-3 (D7): the heavy-run admission gate, invoked as a SUBPROCESS -- see the comment at
#: `run_pytest_full`'s call site for why this is `subprocess` (stdlib), never `import
#: memory_admission_gate`. Both constants are paired with that module's own
#: `DISABLE_ENV`/`TIMEOUT_EXIT_CODE` and must move together if either changes.
_MEMORY_GATE_SCRIPT = Path(__file__).resolve().parent / "memory_admission_gate.py"
_MEMORY_GATE_DISABLE_ENV = "HARNESS_MEMORY_GATE_DISABLE"
_MEMORY_GATE_TIMEOUT_EXIT_CODE = 124


class PairingError(RuntimeError):
    """The tool could not produce a verdict (as opposed to a verdict of red)."""


# --- git ---------------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    if done.returncode != 0:
        raise PairingError(f"git {' '.join(args)} failed: {done.stderr.strip() or done.stdout.strip()}")
    return done.stdout.strip()


def resolve(repo: Path, ref: str) -> str:
    return _git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")


def _is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    """`True` iff `ancestor` is reachable from `descendant` -- `git merge-base --is-ancestor`,
    whose exit 1 means "no" (a normal outcome, not a git failure) so it cannot go through
    `_git`'s check-returncode-!=-0-is-an-error convention."""
    done = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant],
                          cwd=repo, capture_output=True, text=True, check=False)
    if done.returncode not in (0, 1):
        raise PairingError(f"git merge-base --is-ancestor {ancestor} {descendant} failed: "
                           f"{done.stderr.strip() or done.stdout.strip()}")
    return done.returncode == 0


def make_clone(repo: Path, sha: str, dest: Path) -> Path:
    """A shared clone of `repo`, detached at `sha` -- see ISOLATION_REASON."""
    _git(dest.parent, "clone", "--quiet", "--shared", "--no-checkout", str(repo), str(dest))
    _git(dest, "checkout", "--quiet", "--detach", sha)
    return dest


def _writable_then_retry(func, path, _exc) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path: Path) -> bool:
    """Remove `path` and VERIFY it is gone (no leftovers); True when it is."""
    for _ in range(5):
        if not path.exists():
            return True
        shutil.rmtree(path, onexc=_writable_then_retry)
        if not path.exists():
            return True
        time.sleep(0.5)
    return not path.exists()


# --- pytest ------------------------------------------------------------------------------

def _xdist_args(workers: int) -> list[str]:
    return ["-n", str(workers)] if importlib.util.find_spec("xdist") else []


#: The results surface. Reading pytest's own hooks gives EXACT node ids; parsing the `-rA`
#: summary cannot, because a parametrised id may legally contain ` - ` and unmatched brackets
#: and the summary appends ` - <message>` to the same line. The plugin runs INSIDE pytest, so it
#: is not part of this module's imports; this module only reads the JSON lines it writes.
_PLUGIN = """\
import json
import os


def _path():
    return os.environ["TEST_PAIRING_EVENTS"] + "." + str(os.getpid())


def _emit(row):
    with open(_path(), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\\n")


def pytest_sessionstart(session):
    open(_path(), "a", encoding="utf-8").close()


def pytest_runtest_logreport(report):
    _emit({"id": report.nodeid, "when": report.when, "outcome": report.outcome})


def pytest_collectreport(report):
    if report.failed:
        _emit({"id": report.nodeid, "when": "collect", "outcome": "failed"})
    elif report.skipped:
        _emit({"id": report.nodeid, "when": "collect", "outcome": "skipped"})
"""
_PLUGIN_NAME = "tp_events_plugin"


@dataclass(frozen=True)
class RunResult:
    """One pytest run as the plugin saw it: the verdicts, and the ids that were skipped.

    A skip is not a verdict and never enters `results`; it is kept apart because the registry's
    skip-count guard needs it and `read_events` callers must keep seeing PASSED/FAILED/ERROR only.
    """

    results: dict[str, str]
    skipped: frozenset[str]


def read_events(path: Path) -> dict[str, str]:
    """{nodeid: PASSED|FAILED|ERROR} from the plugin's JSON lines; see `read_run`."""
    return read_run(path).results


def read_run(path: Path) -> RunResult:
    """The plugin's JSON lines as a `RunResult`; stdlib only.

    `path` is one file, or the prefix of the per-process files `<prefix>.<pid>` the plugin writes
    (one writer per file, so xdist workers cannot interleave). It FAILS CLOSED: no file at all
    means the plugin never ran, and a malformed row means a result may have been lost -- either
    would otherwise read as "nothing is red". A failed `call` is FAILED; a failed
    setup/teardown/collect is ERROR; a red is never overwritten by a green; duplicates (xdist
    reports in both the worker and the controller) change nothing. A skipped setup, call (this
    is also how an xfail reports) or collection is SKIPPED -- unless the same id also went red.
    """
    files = [path] if path.is_file() else sorted(path.parent.glob(path.name + ".*"))
    if not files:
        raise PairingError(f"no event file at {path.name}: the reporting plugin did not run")
    results: dict[str, str] = {}
    skipped: set[str] = set()
    for file in files:
        for line in file.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError as exc:
                raise PairingError(f"malformed event row in {file.name}: a result may be lost") from exc
            test_id, when, outcome = row.get("id"), row.get("when"), row.get("outcome")
            if not test_id:
                continue
            if outcome == "failed":
                status = "FAILED" if when == "call" else "ERROR"
            elif outcome == "passed" and when == "call":
                status = "PASSED"
            elif outcome == "skipped" and when in ("setup", "call", "collect"):
                skipped.add(test_id)
                continue
            else:
                continue
            if status in _RED:
                if results.get(test_id) not in _RED or (status == "FAILED"
                                                        and results[test_id] == "ERROR"):
                    results[test_id] = status
            else:
                results.setdefault(test_id, status)
    return RunResult(results, frozenset(skipped - results.keys()))


def run_pytest(clone: Path, args: list[str], *, workers: int, timeout: float | None) -> dict[str, str]:
    return run_pytest_full(clone, args, workers=workers, timeout=timeout).results


def run_pytest_full(clone: Path, args: list[str], *, workers: int,
                    timeout: float | None) -> RunResult:
    scratch = clone.parent
    (scratch / f"{_PLUGIN_NAME}.py").write_text(_PLUGIN, encoding="utf-8", newline="\n")
    events = scratch / f"events-{uuid.uuid4().hex}.jsonl"
    base_cmd = [sys.executable, "-m", "pytest", "-q", "--no-header", "--color=no",
               "-p", "no:cacheprovider", "-p", _PLUGIN_NAME, "--continue-on-collection-errors"]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
           "TEST_PAIRING_EVENTS": str(events),
           # The caller's PYTHONPATH is DROPPED: a source checkout on it could shadow the tree
           # under test and hide a lane-caused red. Only the plugin's directory is added.
           "PYTHONPATH": str(scratch)}
    # LANE-5A-3 (D7): every pytest subprocess this module spawns waits for a memory reserve
    # and a machine-wide slot before it runs, and its `-n` is computed from free memory rather
    # than the caller's literal `workers` -- EXCEPT `workers == 0` (an isolated single-test
    # rerun, e.g. flake/baseline confirmation), which asks for serial explicitly and is never
    # promoted to parallel. `HARNESS_MEMORY_GATE_DISABLE` is the done-contract's "old behaviour
    # by a flag": both gates are skipped and `-n <workers>` (the caller's own number, verbatim,
    # matching this function's pre-gate behaviour byte for byte) is used instead.
    #
    # SHELLED OUT, NEVER IMPORTED: `memory_admission_gate.py` depends on click/psutil/filelock/
    # pyyaml, and `test_parsing_and_isolation_use_only_the_standard_library` (this module's
    # own tested invariant) forbids this file from importing anything but `impacted_tests` and
    # the standard library -- this tool is the final arbiter of "is this red the lane's fault"
    # and must keep working even when the dependency graph is broken. `subprocess` (stdlib) is
    # the boundary; `memory_admission_gate.py run` is the process-boundary entry point built
    # for exactly this caller (see that command's own docstring).
    gate_disabled = bool(os.environ.get(_MEMORY_GATE_DISABLE_ENV))
    if gate_disabled:
        cmd = [*base_cmd, *_xdist_args(workers), *args]
        try:
            done = subprocess.run(cmd, cwd=clone, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", env=env,
                                  timeout=timeout, check=False)
        except subprocess.TimeoutExpired as exc:
            raise PairingError(f"pytest exceeded {timeout}s in {clone.name}") from exc
    else:
        want_xdist = workers != 0 and importlib.util.find_spec("xdist") is not None
        cmd = [*base_cmd, *args]
        # `--receipt` pinned HERE, per call, inside `scratch` (never the gate's own
        # `HARNESS_RECEIPTS_DIR`-derived default): `scratch` is this invocation's own throwaway
        # dir, same as `events` above, so the gate's admission receipt can never land beside a
        # caller's own redirected receipts home (e.g. `test_test_pairing.py`'s `home` fixture,
        # which inherits `env` below and asserts nothing but its own registry lives there).
        gate_receipt = scratch / f"memory-gate-receipt-{uuid.uuid4().hex}.json"
        gate_cmd = [sys.executable, str(_MEMORY_GATE_SCRIPT), "run", "--receipt", str(gate_receipt)]
        if want_xdist:
            gate_cmd += ["--workers-flag", "-n"]
        if timeout is not None:
            gate_cmd += ["--timeout", str(timeout)]
        gate_cmd += ["--", *cmd]
        # NO outer timeout: the gate's OWN `--timeout` bounds pytest once it starts (pytest is
        # its direct child, so its kill cannot orphan a grandchild -- see
        # `resource_lifecycle.py`'s own "naive_kill leaves grandchild running" note for why
        # that distinction matters); waiting for MEMORY has no timeout by design
        # (DECLARE-NIGHT-AUTONOMY N2: a run is resumed, not abandoned).
        done = subprocess.run(gate_cmd, cwd=clone, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=env, check=False)
        if done.returncode == _MEMORY_GATE_TIMEOUT_EXIT_CODE:
            raise PairingError(f"pytest exceeded {timeout}s in {clone.name}")
    tail = (done.stderr or done.stdout).strip()[-400:]
    if done.returncode in (3, 4):
        raise PairingError(f"pytest exited {done.returncode} in {clone.name}: {tail}")
    run = read_run(events)
    if done.returncode == 2 and not run.results:
        raise PairingError(f"pytest was interrupted in {clone.name} with no result: {tail}")
    if done.returncode == 1 and not any(v in _RED for v in run.results.values()):
        raise PairingError(f"pytest reported failures in {clone.name} but the events show none: {tail}")
    return run


# --- selection ---------------------------------------------------------------------------

def _changed(repo: Path, base: str, head: str) -> list[str]:
    out = _git(repo, "diff", "--name-only", base, head)
    return [line for line in out.splitlines() if line]


def _selection_to_dict(clone: Path, changed: list[str], selection, note: str) -> dict:
    """`impacted_tests.Selection` -> the plain dict shape every downstream helper expects.

    Shared by `choose_tests` (a two-dot diff against a supplied `changed` list) and
    `choose_tests_from_lane_diff` (the lane's own `main...lane` diff) -- everything past
    "what did impacted_tests decide" is identical between the two entry points.
    """
    if selection.full_suite:
        own = sorted(c for c in changed if _TEST_FILE.search(c) and (clone / c).is_file())
        return {
            "declined": True, "ran_full_suite": False, "marker": None, "test_files": own,
            "reasons": {k: list(v) for k, v in selection.reasons.items()}, "changed": changed,
            "note": ("impacted selection declined to narrow (full suite); "
                     + ("ran only the test files this diff changed -- a PARTIAL pairing"
                        if own else "no changed test file to fall back on -- nothing was run")),
        }
    files = [f for f in selection.test_files if (clone / f).is_file()]
    return {
        "declined": False, "ran_full_suite": False,
        "marker": selection.marker if not files else None, "test_files": files,
        "reasons": {k: list(v) for k, v in selection.reasons.items()}, "changed": changed,
        "note": note,
    }


def choose_tests(clone: Path, changed: list[str]) -> dict:
    """The selection block: what to run on HEAD, and whether the selector declined."""
    selection = impacted_tests.select(clone, changed)
    return _selection_to_dict(clone, changed, selection, "narrowed by impacted_tests.select")


def choose_tests_from_lane_diff(clone: Path, main_ref: str, lane_ref: str) -> dict:
    """Like `choose_tests`, sourced from the LANE'S OWN diff `main_ref...lane_ref`
    (`impacted_tests.select_lane_diff`) rather than a two-dot diff against a supplied
    list. `main_ref`/`lane_ref` are resolved SHAs, never symbolic names: the clone this
    runs in has no `origin` remote of its own, so a name like `origin/main` would not
    resolve inside it, but the commit objects are present either way (a shared clone).
    """
    changed = impacted_tests.changed_from_lane_diff(clone, main_ref, lane_ref)
    selection = impacted_tests.select_lane_diff(clone, main_ref=main_ref, lane_ref=lane_ref)
    return _selection_to_dict(clone, changed, selection,
                              "narrowed by impacted_tests.select_lane_diff")


def _file_part(target: str) -> str:
    return target.split("::", 1)[0]


def validate_targets(clone: Path, targets: list[str]) -> None:
    """Explicit `--tests` are files or node ids in the tree -- never a directory or `.`, which
    would quietly run the suite the contract says this organ never runs."""
    for target in targets:
        path = _file_part(target)
        if not path.endswith(".py") or not (clone / path).is_file() or ".." in Path(path).parts:
            raise PairingError(f"--tests takes test files or node ids, not {target!r}")


def _pytest_args(selection: dict, clone: Path) -> list[str] | None:
    if selection["test_files"]:
        return [f for f in selection["test_files"] if (clone / _file_part(f)).is_file()] or None
    if selection["marker"]:
        return ["-m", selection["marker"]]
    return None


# --- classification ----------------------------------------------------------------------

def _was(test_id: str, base: dict[str, str]) -> str:
    if test_id in base:
        return base[test_id]
    if "::" not in test_id:  # a file that now errors at collection: judge it by its old tests
        old = [s for k, s in base.items() if k.startswith(test_id + "::")]
        if old:
            return "PASSED" if "PASSED" in old else old[0]
    return "absent"


def classify(base: dict[str, str], head: dict[str, str]) -> dict:
    base_red = {k for k, s in base.items() if s in _RED}
    head_red = {k for k, s in head.items() if s in _RED}
    lane = sorted(head_red - base_red)
    return {
        "preexisting": sorted(base_red & head_red),
        "candidates": [{"id": k, "was": _was(k, base)} for k in lane],
        "fixed": sorted(k for k in base_red - head_red if head.get(k) == "PASSED"),
    }


def _rerun(clone: Path, test_id: str, first: str, *, reruns: int,
           timeout: float | None) -> list[str]:
    observations = [first]
    for _ in range(reruns):
        status = run_pytest(clone, [test_id], workers=0, timeout=timeout).get(test_id, "NOT-RUN")
        observations.append(status)
        if status == "PASSED":
            break
    return observations


def pair(repo: Path, base: str, head: str, *, tests: list[str] | None = None, reruns: int = 1,
         workers: int = 6, timeout: float | None = None, workdir: Path | None = None,
         confirm_baseline: bool = True) -> dict:
    """Pair BASE against HEAD and return the verdict dict (also the artifact's content)."""
    if reruns < 1:
        raise PairingError("--reruns must be at least 1: zero would charge a flake to the lane")
    base_sha, head_sha = resolve(repo, base), resolve(repo, head)
    changed = _changed(repo, base_sha, head_sha)
    scratch = Path(tempfile.mkdtemp(prefix="tp-", dir=workdir))
    try:
        head_clone = make_clone(repo, head_sha, scratch / "head")
        if tests:
            validate_targets(head_clone, tests)
            selection = {"declined": False, "ran_full_suite": False, "marker": None,
                         "test_files": sorted(tests), "reasons": {},
                         "note": "explicit --tests, selection not consulted"}
        else:
            selection = choose_tests(head_clone, changed)
        selection["changed"] = changed
        args = _pytest_args(selection, head_clone)
        verdict = {"schema": SCHEMA, "base": base_sha, "head": head_sha, "isolation": "clone",
                   "isolation_reason": ISOLATION_REASON, "selection": selection,
                   "preexisting": [], "lane": [], "turned_red": [], "flakes": [], "fixed": [],
                   "baseline_confirmed": False}
        if args is None:
            verdict["verdict"] = "NOT-EVALUATED" if selection["declined"] else "CLEAN"
            if not selection["declined"]:
                selection["note"] += "; the selection is empty, nothing to run"
        else:
            head_results = run_pytest(head_clone, args, workers=workers, timeout=timeout)
            base_clone = make_clone(repo, base_sha, scratch / "base")
            # On BASE a node id may not exist yet (a test the lane added), so run its FILE.
            base_args = args if args[0] == "-m" else sorted(
                {_file_part(a) for a in args if (base_clone / _file_part(a)).is_file()})
            base_results = (run_pytest(base_clone, base_args, workers=workers, timeout=timeout)
                            if base_args else {})
            found = classify(base_results, head_results)
            preexisting, candidates = found["preexisting"], list(found["candidates"])
            if confirm_baseline and preexisting:
                # A red on BASE that passes on a rerun was never pre-existing: it could be
                # hiding a real lane-caused red of the same id. One batched rerun, on BASE.
                again = run_pytest(base_clone, preexisting, workers=workers, timeout=timeout)
                unstable = [i for i in preexisting if again.get(i) == "PASSED"]
                preexisting = [i for i in preexisting if i not in unstable]
                candidates += [{"id": i, "was": "red-once-on-base"} for i in unstable]
            verdict["baseline_confirmed"] = confirm_baseline
            for cand in candidates:
                obs = _rerun(head_clone, cand["id"], head_results[cand["id"]], reruns=reruns,
                             timeout=timeout)
                if "PASSED" in obs[1:]:
                    verdict["flakes"].append({"id": cand["id"], "observations": obs})
                else:
                    verdict["lane"].append({**cand, "observations": obs})
            verdict["preexisting"] = preexisting
            verdict["fixed"] = found["fixed"]
            verdict["turned_red"] = [e["id"] for e in verdict["lane"] if e["was"] == "PASSED"]
            verdict["verdict"] = "LANE-RED" if verdict["lane"] else "CLEAN"
    finally:
        removed = remove_tree(scratch)
    verdict["cleanup"] = "removed" if removed else f"LEFTOVER {scratch}"
    verdict["counts"] = {k: len(verdict[k]) for k in ("preexisting", "lane", "turned_red", "flakes",
                                                     "fixed")}
    verdict["exit_code"] = {"LANE-RED": 1, "NOT-EVALUATED": 3}.get(verdict["verdict"], 0)
    if not removed and not verdict["exit_code"]:
        verdict["exit_code"] = 2  # a leaked clone must not ride along on a green verdict
    return verdict


# --- the batch registry ------------------------------------------------------------------

REGISTRY_SCHEMA = "test-pairing-registry/1"
REGISTRY_STEM = "TEST-PAIRING-REGISTRY-"
EXIT_UNATTRIBUTABLE = 4
_BATCH_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")


def receipts_home(repo: Path) -> Path:
    """L1's receipts home: `HARNESS_RECEIPTS_DIR`, else the checkout's gitignored `logs/receipts/`."""
    return Path(os.environ.get("HARNESS_RECEIPTS_DIR") or repo / "logs" / "receipts")


def resolve_batch(given: str | None) -> str:
    """The batch name, from `--batch` or `HARNESS_BATCH`; a plain name only (it becomes a filename)."""
    batch = given or os.environ.get("HARNESS_BATCH") or ""
    if not batch:
        raise PairingError("no batch: give --batch NAME or set HARNESS_BATCH")
    if not _BATCH_NAME.match(batch):
        raise PairingError(f"--batch takes a plain name (letters, digits, . _ -), not {batch!r}")
    return batch


def registry_path(repo: Path, batch: str) -> Path:
    return receipts_home(repo) / f"{REGISTRY_STEM}{resolve_batch(batch)}.json"


@dataclass(frozen=True)
class Registry:
    """What main looked like when the batch began: the record every lane is compared against."""

    batch: str
    commit: str
    files: tuple[str, ...]
    red: dict[str, str]
    passed: tuple[str, ...]
    skipped: tuple[str, ...]
    base_flakes: tuple[str, ...]
    baseline_confirmed: bool
    lanes: tuple[str, ...]
    notes: tuple[str, ...]

    @property
    def skip_count(self) -> int:
        return len(self.skipped)

    def to_json(self) -> dict:
        return {"schema": REGISTRY_SCHEMA, "batch": self.batch, "commit": self.commit,
                "isolation": "clone", "isolation_reason": ISOLATION_REASON,
                "lanes": list(self.lanes), "notes": list(self.notes), "files": list(self.files),
                "baseline_confirmed": self.baseline_confirmed, "red": dict(sorted(self.red.items())),
                "base_flakes": list(self.base_flakes), "skip_count": self.skip_count,
                "skipped": list(self.skipped), "passed": list(self.passed)}

    @classmethod
    def from_json(cls, data: dict, source: str) -> Registry:
        if data.get("schema") != REGISTRY_SCHEMA:
            raise PairingError(f"{source}: schema {data.get('schema')!r}, expected "
                               f"{REGISTRY_SCHEMA!r} -- record the base again")
        try:
            return cls(batch=data["batch"], commit=data["commit"], files=tuple(data["files"]),
                       red=dict(data["red"]), passed=tuple(data["passed"]),
                       skipped=tuple(data["skipped"]), base_flakes=tuple(data["base_flakes"]),
                       baseline_confirmed=bool(data["baseline_confirmed"]),
                       lanes=tuple(data["lanes"]), notes=tuple(data["notes"]))
        except (KeyError, TypeError) as exc:
            raise PairingError(f"{source}: registry is missing or has a malformed field: {exc}") from exc


def load_registry(repo: Path, batch: str) -> Registry:
    path = registry_path(repo, batch)
    if not path.is_file():
        raise PairingError(f"no registry for batch {batch!r} at {path}: run `record-base` first -- "
                           "an absent registry must not read as 'main has no reds'")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise PairingError(f"{path.name} is not valid JSON: {exc}") from exc
    return Registry.from_json(data, path.name)


def write_registry(path: Path, registry: Registry, *, replace: bool = False) -> None:
    """Publish the registry atomically. Without `replace` the create is EXCLUSIVE (a hard link
    fails if the name exists), so two racing `record-base` runs cannot overwrite each other; the
    temp name is unique per writer and is always removed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(json.dumps(registry.to_json(), indent=2) + "\n", encoding="utf-8", newline="\n")
    try:
        if replace:
            os.replace(tmp, path)
        else:
            try:
                os.link(tmp, path)
            except FileExistsError as exc:
                raise PairingError(f"{path.name} already exists: a registry is written once per "
                                   "batch (--replace to overwrite)") from exc
    finally:
        tmp.unlink(missing_ok=True)


def selection_files(clone: Path, selection: dict) -> list[str]:
    """The FILES a selection means. A docs-only selection is the `live_repo` marker; running
    `-m` would make the registry and the comparison disagree on what a file list covers, so the
    marker is resolved to the files carrying it (a superset -- see `impacted_tests`)."""
    files = {_file_part(f) for f in selection["test_files"] if (clone / _file_part(f)).is_file()}
    if not files and selection["marker"]:
        files = set(impacted_tests.live_repo_test_files(clone))
    return sorted(files)


def record_base(repo: Path, commit: str, batch: str, *, lanes: list[str] | None = None,
                tests: list[str] | None = None, workers: int = 6, timeout: float | None = None,
                workdir: Path | None = None, confirm_baseline: bool = True,
                replace: bool = False) -> tuple[Registry, Path, bool]:
    """Run the batch's selected tests on `commit` ONCE and write the registry.

    Returns (registry, its path, whether the scratch clone was removed). The base is a CLONE for
    the reason in ISOLATION_REASON. With `lanes`, the files are the union of what each lane's diff
    (against its merge-base with `commit`) impacts, restricted to files that exist on `commit`;
    with `tests`, the named files. Reds are confirmed once here, so no comparison repeats it.
    """
    batch = resolve_batch(batch)
    path = registry_path(repo, batch)
    if path.exists() and not replace:
        raise PairingError(f"{path.name} already exists: a registry is written once per batch -- "
                           "re-recording mid-batch would turn a lane's red into a pre-existing one "
                           "(--replace if that is really what you mean)")
    if bool(lanes) == bool(tests):
        raise PairingError("give the batch's --lane NAME (one or more) or explicit --tests, not both "
                           "and not neither")
    sha = resolve(repo, commit)
    scratch = Path(tempfile.mkdtemp(prefix="tp-", dir=workdir))
    try:
        clone = make_clone(repo, sha, scratch / "base")
        notes: list[str] = []
        if tests:
            validate_targets(clone, tests)
            files = sorted({_file_part(t) for t in tests})
            lane_names: list[str] = []
        else:
            lane_names = list(dict.fromkeys(lanes or []))
            found: set[str] = set()
            for lane in lane_names:
                head = resolve(repo, f"worktree-{lane}")
                selection = choose_tests(clone, _changed(repo, _git(repo, "merge-base", sha, head), head))
                found.update(selection_files(clone, selection))
                if selection["declined"]:
                    notes.append(f"{lane}: {selection['note']}")
            files = sorted(found)
        if not files:
            raise PairingError("nothing to record: the batch's lanes select no test file that exists "
                               f"on {sha[:8]}")
        run = run_pytest_full(clone, files, workers=workers, timeout=timeout)
        red = {k: v for k, v in run.results.items() if v in _RED}
        flakes: list[str] = []
        if confirm_baseline and red:
            again = run_pytest(clone, sorted(red), workers=workers, timeout=timeout)
            flakes = sorted(i for i in red if again.get(i) == "PASSED")
            red = {k: v for k, v in red.items() if k not in flakes}
        registry = Registry(
            batch=batch, commit=sha, files=tuple(files), red=red,
            passed=tuple(sorted(k for k, v in run.results.items() if v == "PASSED")),
            skipped=tuple(sorted(run.skipped)), base_flakes=tuple(flakes),
            baseline_confirmed=confirm_baseline, lanes=tuple(lane_names), notes=tuple(notes))
        write_registry(path, registry, replace=replace)
    finally:
        removed = remove_tree(scratch)
    return registry, path, removed


def _was_in_registry(test_id: str, registry: Registry) -> str:
    """What a merged-tree red was at the registry's base, in `classify`'s vocabulary."""
    if test_id in registry.base_flakes:
        return "red-once-on-base"
    passed = set(registry.passed)
    if test_id in passed:
        return "PASSED"
    if "::" not in test_id and any(p.startswith(test_id + "::") for p in passed):
        return "PASSED"  # a file that now errors at collection: judge it by its old tests
    return "absent"


def skip_guard(registry: Registry, head_skipped: frozenset[str], files: list[str]) -> dict:
    """Compare skips over the test files BOTH the registry and this run covered.

    A merged tree that runs only the lane's impacted files cannot be held to the registry's whole
    count, so both sides are cut to the same files; when the run covers every registry file the cut
    is the registry's own skip count. A different COUNT is a mismatch, and so is any skip the
    registry did not have even when the count is level: un-skipping one test while skipping a red
    one keeps the count and hides the red.
    """
    covered = {f for f in files if f in registry.files}
    then = sorted(s for s in registry.skipped if _file_part(s) in covered)
    now = sorted(s for s in head_skipped if _file_part(s) in covered)
    added, removed = sorted(set(now) - set(then)), sorted(set(then) - set(now))
    # A brand-new node id -- never red, passed, OR skipped in the registry -- cannot be
    # hiding a registry-known result, because there was nothing recorded for it to hide.
    # Finding 2 (DIGEST-WAVE4-FINAL-2026-09-22): before this, a lane that added a new test
    # INSIDE an existing (covered) file and marked it skipped tripped the guard identically
    # to a KNOWN id being silenced -- purely because file-level `covered` membership was the
    # only boundary the guard could see. The identical new test in a brand-NEW file was
    # already exempt (a new file is never `in registry.files`), so the asymmetry was which
    # side of a FILE boundary the same new id happened to land on, not anything about risk.
    known = set(registry.red) | set(registry.passed) | set(registry.skipped)
    # Codex terra HIGH: a COLLECTION-level skip (a module unconditionally `pytest.skip()`-ed
    # at import time, or file-level `collect_ignore`) reports a single skip whose id is the
    # FILE, not any one test node -- so it never equals a known per-test node id and slid
    # past the check above even while it silences every known red/passed/skipped node in
    # that file. `_file_part` a known id has no "::" for a file-level `a`, so a file-level
    # `a` that names a file carrying known ids is exactly as dangerous as a known id itself.
    known_files = {_file_part(k) for k in known}
    dangerous_added = [a for a in added
                       if a in known or ("::" not in a and a in known_files)]
    return {"status": "match" if not dangerous_added else "mismatch",
            "registry": len(then), "head": len(now), "added": added, "removed": removed}


def _exists_at(repo: Path, sha: str, path: str) -> bool:
    done = subprocess.run(["git", "cat-file", "-e", f"{sha}:{path}"], cwd=repo,
                          capture_output=True, check=False)
    return done.returncode == 0


def _run_against_registry(clone: Path, registry: Registry, selection: dict, head_sha: str, *,
                          reruns: int, workers: int, timeout: float | None) -> dict:
    """Run `selection`'s files on `clone` and classify against `registry`.

    Shared by `compare()` (selection sourced from a two-dot diff against the registry's own
    base commit) and `record_lane()` (selection sourced from the lane's OWN diff against
    `--main`) -- everything past "what to run" is identical between the two entry points,
    and duplicating it was how the FR3 lane-record mode would have drifted from `compare()`'s
    already-hardened classification the first time either one changed.
    """
    files = selection_files(clone, selection)
    if selection["marker"] and not selection["test_files"] and files:
        selection["note"] += "; the live_repo marker was resolved to its files"
    selection["test_files"] = files
    selection["outside_registry"] = [f for f in files if f not in registry.files]
    # A file the registry never ran that ALREADY existed on the base has an unknown baseline:
    # any red in it, or any skip hiding one, could be main's. It is refused, not guessed at.
    # (A file the lane added did not exist on the base and is the lane's by construction.)
    unregistered = [f for f in selection["outside_registry"]
                    if _exists_at(clone, registry.commit, f)]
    verdict = {"schema": SCHEMA, "mode": "registry", "batch": registry.batch,
               "base": registry.commit, "head": head_sha, "isolation": "clone",
               "isolation_reason": ISOLATION_REASON, "selection": selection,
               "preexisting": [], "lane": [], "turned_red": [], "flakes": [], "fixed": [],
               "baseline_confirmed": registry.baseline_confirmed,
               "unregistered": unregistered, "skip_guard": {"status": "not-run"}}
    if unregistered:
        verdict["verdict"] = "UNATTRIBUTABLE"
    elif not files:
        verdict["verdict"] = "NOT-EVALUATED" if selection["declined"] else "CLEAN"
        if not selection["declined"]:
            selection["note"] += "; the selection is empty, nothing to run"
    else:
        run = run_pytest_full(clone, files, workers=workers, timeout=timeout)
        verdict["skip_guard"] = skip_guard(registry, run.skipped, files)
        if verdict["skip_guard"]["status"] != "match":
            verdict["verdict"] = "UNATTRIBUTABLE"
        else:
            head_red = {k for k, s in run.results.items() if s in _RED}
            registry_red = set(registry.red)
            verdict["preexisting"] = sorted(head_red & registry_red)
            verdict["fixed"] = sorted(k for k in registry_red - head_red
                                      if run.results.get(k) == "PASSED")
            for test_id in sorted(head_red - registry_red):
                obs = _rerun(clone, test_id, run.results[test_id], reruns=reruns, timeout=timeout)
                if "PASSED" in obs[1:]:
                    verdict["flakes"].append({"id": test_id, "observations": obs})
                else:
                    verdict["lane"].append({"id": test_id, "was": _was_in_registry(test_id, registry),
                                            "observations": obs})
            verdict["turned_red"] = [e["id"] for e in verdict["lane"] if e["was"] == "PASSED"]
            verdict["verdict"] = "LANE-RED" if verdict["lane"] else "CLEAN"
    return verdict


def compare(repo: Path, registry: Registry, head: str, *, since: str | None = None,
            reruns: int = 1, workers: int = 6, timeout: float | None = None,
            workdir: Path | None = None) -> dict:
    """Run the merged tree at `head` and classify it against `registry`; no base run happens."""
    if reruns < 1:
        raise PairingError("--reruns must be at least 1: zero would charge a flake to the lane")
    head_sha = resolve(repo, head)
    changed = _changed(repo, resolve(repo, since) if since else registry.commit, head_sha)
    scratch = Path(tempfile.mkdtemp(prefix="tp-", dir=workdir))
    try:
        clone = make_clone(repo, head_sha, scratch / "head")
        selection = choose_tests(clone, changed)
        selection["changed"] = changed
        verdict = _run_against_registry(clone, registry, selection, head_sha,
                                        reruns=reruns, workers=workers, timeout=timeout)
    finally:
        removed = remove_tree(scratch)
    verdict["cleanup"] = "removed" if removed else f"LEFTOVER {scratch}"
    verdict["counts"] = {k: len(verdict[k]) for k in ("preexisting", "lane", "turned_red", "flakes",
                                                     "fixed")}
    verdict["exit_code"] = {"LANE-RED": 1, "NOT-EVALUATED": 3,
                            "UNATTRIBUTABLE": EXIT_UNATTRIBUTABLE}.get(verdict["verdict"], 0)
    if not removed and not verdict["exit_code"]:
        verdict["exit_code"] = 2  # a leaked clone must not ride along on a green verdict
    return verdict


# --- FR3: lane-side record by tree ---------------------------------------------------------
#
# `compare()` above answers ONE question per invocation and never persists it for reuse. FR3
# (`to-cc/PLAN-WAVE4B-SESSION-2026-09-22.md`) asks for the LANE to run its own verification
# and hand the integrator a record it can trust WITHOUT re-running it, provided the one thing
# that could invalidate it -- origin/main moving -- did not happen. `record_lane` writes that
# record, KEYED BY (tree sha, origin/main sha) as the two fields on it that answer "does this
# still apply"; `reuse_check` is the second mode that answers that question.
#
# THE RECORD IS NOT THE BATCH REGISTRY. The registry (`record_base`/`Registry`) is written
# ONCE per batch and is exclusive by design -- re-recording it would launder a lane's red into
# "pre-existing" for every other lane. A lane's own record is the opposite: it is the LANE'S,
# re-verifying after a new commit is the normal path rather than a laundering risk, and it is
# always overwritten (`os.replace`, no exclusivity) -- the file always answers for the lane's
# CURRENT tree, and `reuse_check`'s STALE-TREE outcome is what tells a caller a stored record
# has gone stale rather than silently comparing an old one.

LANE_RECORD_SCHEMA = "test-pairing-lane-record/1"
LANE_RECORD_STEM = "TEST-PAIRING-LANE-"

LANE_STATUS_REUSABLE = "REUSABLE"
LANE_STATUS_STALE_TREE = "STALE-TREE"
LANE_STATUS_MAIN_MOVED = "MAIN-MOVED"
LANE_STATUS_NOT_RECORDED = "NOT-RECORDED"

EXIT_NOT_RECORDED = 5
EXIT_STALE_TREE = 6
EXIT_MAIN_MOVED = 7


def lane_record_path(repo: Path, batch: str, lane: str) -> Path:
    return receipts_home(repo) / f"{LANE_RECORD_STEM}{resolve_batch(batch)}-{lane}.json"


def record_lane(repo: Path, batch: str, lane: str, *, main_ref: str = "origin/main",
                lane_ref: str | None = None, reruns: int = 1, workers: int = 6,
                timeout: float | None = None, workdir: Path | None = None) -> dict:
    """Run the LANE'S OWN selection on its current tree, classify against the batch
    registry, and persist the verdict keyed by (tree sha, origin/main sha) at
    `lane_record_path`. `lane_ref` defaults to `worktree-<lane>`, matching the `--lane`
    convention the two-commit CLI already uses.
    """
    if reruns < 1:
        raise PairingError("--reruns must be at least 1: zero would charge a flake to the lane")
    batch = resolve_batch(batch)
    registry = load_registry(repo, batch)
    main_sha = resolve(repo, main_ref)
    resolved_lane_ref = lane_ref or f"worktree-{lane}"
    head_sha = resolve(repo, resolved_lane_ref)
    # Codex terra HIGH: the clone below is detached at `head_sha` alone and NEVER
    # combines `main_sha` into the tested tree, so a record claiming to answer for
    # "origin/main + lane" (the schema's own `origin_main` field) would be false for a
    # lane that has not synced -- it tested only itself. Refuse rather than silently
    # narrow what the record means; WAVE4B-COMMON rule 1 already requires the lane to
    # `git fetch origin && git merge origin/main`, so a synced lane passes trivially.
    if not _is_ancestor(repo, main_sha, head_sha):
        raise PairingError(
            f"record-lane: {main_ref} ({main_sha[:8]}) is not merged into "
            f"{resolved_lane_ref} ({head_sha[:8]}) -- sync the lane first "
            "(git fetch origin && git merge origin/main); a record keyed to an "
            "origin/main sha the lane never actually combined with would be false"
        )
    scratch = Path(tempfile.mkdtemp(prefix="tp-", dir=workdir))
    try:
        clone = make_clone(repo, head_sha, scratch / "head")
        selection = choose_tests_from_lane_diff(clone, main_sha, head_sha)
        verdict = _run_against_registry(clone, registry, selection, head_sha,
                                        reruns=reruns, workers=workers, timeout=timeout)
    finally:
        removed = remove_tree(scratch)
    verdict["cleanup"] = "removed" if removed else f"LEFTOVER {scratch}"
    verdict["counts"] = {k: len(verdict[k]) for k in ("preexisting", "lane", "turned_red", "flakes",
                                                     "fixed")}
    verdict["exit_code"] = {"LANE-RED": 1, "NOT-EVALUATED": 3,
                            "UNATTRIBUTABLE": EXIT_UNATTRIBUTABLE}.get(verdict["verdict"], 0)
    if not removed and not verdict["exit_code"]:
        verdict["exit_code"] = 2
    record = {"schema": LANE_RECORD_SCHEMA, "batch": batch, "lane": lane,
              "tree": head_sha, "origin_main": main_sha, "verdict": verdict}
    path = lane_record_path(repo, batch, lane)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, path)  # always overwritten -- see the section note above
    return record


def reuse_check(repo: Path, batch: str, lane: str, *, main_ref: str = "origin/main",
               lane_ref: str | None = None) -> dict:
    """Tell the integrator whether `lane`'s recorded run is REUSABLE, without re-running it.

    Four outcomes, each answering a DIFFERENT question:
      * NOT-RECORDED -- no record exists for this lane; run `record-lane` first.
      * STALE-TREE   -- the lane has new commits since the record: the tree sha itself
                        changed, so the record's SELECTION was computed against a tree
                        that no longer exists at the lane's tip. A full `record-lane`
                        re-run is needed, not a subset.
      * MAIN-MOVED   -- the recorded tree is UNCHANGED, but origin/main advanced since
                        the record was made (typically: a sibling lane merged). The
                        subset that must re-run is exactly what `impacted_tests.select`
                        finds for the diff main itself made (`old_origin_main
                        ...new_origin_main`) -- never the lane's whole selection again.
      * REUSABLE     -- neither moved; the recorded verdict stands as-is.
    """
    batch = resolve_batch(batch)
    path = lane_record_path(repo, batch, lane)
    if not path.is_file():
        return {"status": LANE_STATUS_NOT_RECORDED, "reusable": False,
                "note": f"no record at {path.name}: run `record-lane` first"}
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise PairingError(f"{path.name} is not valid JSON: {exc}") from exc
    if record.get("schema") != LANE_RECORD_SCHEMA:
        raise PairingError(f"{path.name}: schema {record.get('schema')!r}, expected "
                           f"{LANE_RECORD_SCHEMA!r} -- record the lane again")
    current_tree = resolve(repo, lane_ref or f"worktree-{lane}")
    current_main = resolve(repo, main_ref)
    if record["tree"] != current_tree:
        return {"status": LANE_STATUS_STALE_TREE, "reusable": False,
                "recorded_tree": record["tree"], "current_tree": current_tree,
                "note": "the lane advanced since the record; run `record-lane` again"}
    if record["origin_main"] == current_main:
        return {"status": LANE_STATUS_REUSABLE, "reusable": True,
                "tree": current_tree, "origin_main": current_main, "verdict": record["verdict"],
                "note": (f"origin/main unchanged since the record ({current_main[:8]}); reusing "
                         f"it without a re-run -- verdict {record['verdict']['verdict']}")}
    changed = impacted_tests.changed_from_lane_diff(repo, record["origin_main"], current_main)
    selection = impacted_tests.select(repo, changed) if changed else impacted_tests.Selection()
    return {
        "status": LANE_STATUS_MAIN_MOVED, "reusable": False, "tree": current_tree,
        "recorded_origin_main": record["origin_main"], "current_origin_main": current_main,
        "rerun_selection": {"full_suite": selection.full_suite,
                            "test_files": list(selection.test_files), "marker": selection.marker},
        "note": ("origin/main advanced since the record; re-run only the tests impacted by "
                 "what main itself changed, not the lane's whole selection again"),
    }


def _reuse_check_exit_code(status: dict) -> int:
    if status["status"] == LANE_STATUS_REUSABLE:
        return status["verdict"]["exit_code"]
    return {LANE_STATUS_NOT_RECORDED: EXIT_NOT_RECORDED, LANE_STATUS_STALE_TREE: EXIT_STALE_TREE,
           LANE_STATUS_MAIN_MOVED: EXIT_MAIN_MOVED}[status["status"]]


# --- command line ------------------------------------------------------------------------

def _default_workers() -> int:
    return 6 if importlib.util.find_spec("xdist") else 0


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    p.add_argument("commits", nargs="*", metavar="BASE HEAD", help="two commits, or use --lane")
    p.add_argument("--lane", help="pair merge-base(main, worktree-LANE) against worktree-LANE")
    p.add_argument("--main", default="main", help="the main ref for --lane (default: main)")
    p.add_argument("--repo", default=".", help="repository to pair in (default: cwd)")
    p.add_argument("--out", help=f"verdict path (default: <receipts home>/{VERDICT_NAME})")
    p.add_argument("--tests", nargs="+", help="explicit test files, bypassing the selection")
    p.add_argument("--reruns", type=int, default=1,
                   help="isolated reruns of a lane-red, at least 1 (default 1)")
    p.add_argument("--no-confirm-baseline", action="store_true",
                   help="do not rerun the pre-existing reds on BASE (cheaper; a transient baseline "
                        "red can then mask a lane-caused one)")
    p.add_argument("--workers", type=int, default=_default_workers(),
                   help="xdist workers (default 6; 0 = in-process)")
    p.add_argument("--timeout", type=float, help="seconds allowed per pytest invocation")
    p.add_argument("--workdir", help="parent directory for the clones (default: system temp)")
    return p


def _registry_parser(command: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=f"test_pairing.py {command}",
                                description=f"batch registry mode: {command} (see the module docstring)")
    p.add_argument("--batch", help="the batch name (default: $HARNESS_BATCH)")
    p.add_argument("--repo", default=".", help="repository to pair in (default: cwd)")
    p.add_argument("--workers", type=int, default=_default_workers(),
                   help="xdist workers (default 6; 0 = in-process)")
    p.add_argument("--timeout", type=float, help="seconds allowed per pytest invocation")
    p.add_argument("--workdir", help="parent directory for the clones (default: system temp)")
    if command == "record-base":
        p.add_argument("--commit", required=True, help="the batch's base commit (main before any merge)")
        p.add_argument("--lane", action="append", help="a lane of the batch (repeatable); its impacted "
                       "test files join the registry")
        p.add_argument("--tests", nargs="+", help="explicit test files instead of --lane")
        p.add_argument("--replace", action="store_true", help="overwrite an existing registry")
        p.add_argument("--no-confirm-baseline", action="store_true",
                       help="do not rerun the reds once on the base (a transient red then becomes "
                            "'pre-existing' for the whole batch)")
    else:
        p.add_argument("--head", required=True, help="the merged tree to compare")
        p.add_argument("--since", help="select tests impacted by changes since this ref "
                                       "(default: the registry's base commit)")
        p.add_argument("--out", help=f"verdict path (default: <receipts home>/{VERDICT_NAME})")
        p.add_argument("--reruns", type=int, default=1,
                       help="isolated reruns of a lane-red, at least 1 (default 1)")
    return p


def _lane_parser(command: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=f"test_pairing.py {command}",
                                description=f"FR3 lane-record mode: {command} (see the module docstring)")
    p.add_argument("--batch", help="the batch name (default: $HARNESS_BATCH)")
    p.add_argument("--lane", required=True, help="the lane's slug (branch worktree-<lane>)")
    p.add_argument("--main", default="origin/main", help="the lane's sync point (default: origin/main)")
    p.add_argument("--repo", default=".", help="repository to run in (default: cwd)")
    if command == "record-lane":
        p.add_argument("--workers", type=int, default=_default_workers(),
                       help="xdist workers (default 6; 0 = in-process)")
        p.add_argument("--timeout", type=float, help="seconds allowed per pytest invocation")
        p.add_argument("--workdir", help="parent directory for the clone (default: system temp)")
        p.add_argument("--reruns", type=int, default=1,
                       help="isolated reruns of a lane-red, at least 1 (default 1)")
    else:
        p.add_argument("--out", help="also write the status JSON to this path")
    return p


def _lane_main(command: str, argv: list[str]) -> int:
    args = _lane_parser(command).parse_args(argv)
    try:
        repo = Path(_git(Path(args.repo).resolve(), "rev-parse", "--show-toplevel"))
        batch = resolve_batch(args.batch)
        if command == "record-lane":
            record = record_lane(repo, batch, args.lane, main_ref=args.main,
                                 reruns=args.reruns, workers=args.workers, timeout=args.timeout,
                                 workdir=Path(args.workdir) if args.workdir else None)
            print(json.dumps(record, indent=2))
            v = record["verdict"]
            print(f"test_pairing: recorded lane {args.lane} at {record['tree'][:8]} against "
                  f"origin/main {record['origin_main'][:8]} -- {v['verdict']}", file=sys.stderr)
            return v["exit_code"]
        status = reuse_check(repo, batch, args.lane, main_ref=args.main)
    except PairingError as exc:
        print(f"test_pairing: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    if getattr(args, "out", None):
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(status, indent=2))
    print(f"test_pairing: {status['status']} -- {status['note']}", file=sys.stderr)
    return _reuse_check_exit_code(status)


def _publish(verdict: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, out)
    print(json.dumps(verdict, indent=2))


def _registry_main(command: str, argv: list[str]) -> int:
    args = _registry_parser(command).parse_args(argv)
    workdir = Path(args.workdir) if args.workdir else None
    try:
        repo = Path(_git(Path(args.repo).resolve(), "rev-parse", "--show-toplevel"))
        batch = resolve_batch(args.batch)
        if command == "record-base":
            registry, path, removed = record_base(
                repo, args.commit, batch, lanes=args.lane, tests=args.tests, workers=args.workers,
                timeout=args.timeout, workdir=workdir, confirm_baseline=not args.no_confirm_baseline,
                replace=args.replace)
            print(json.dumps({"registry": str(path), "batch": batch, "commit": registry.commit,
                              "files": len(registry.files), "red": len(registry.red),
                              "skip_count": registry.skip_count,
                              "cleanup": "removed" if removed else "LEFTOVER"}, indent=2))
            print(f"test_pairing: registry {path.name} -- {len(registry.files)} file(s) at "
                  f"{registry.commit[:8]}, {len(registry.red)} red, {registry.skip_count} skipped",
                  file=sys.stderr)
            return 0 if removed else 2
        verdict = compare(repo, load_registry(repo, batch), args.head, since=args.since,
                          reruns=args.reruns, workers=args.workers, timeout=args.timeout,
                          workdir=workdir)
    except PairingError as exc:
        print(f"test_pairing: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    _publish(verdict, Path(args.out) if args.out else receipts_home(repo) / VERDICT_NAME)
    c, guard = verdict["counts"], verdict["skip_guard"]
    print(f"test_pairing: {verdict['verdict']} -- lane {c['lane']} (turned red {c['turned_red']}), "
          f"pre-existing {c['preexisting']}, flake {c['flakes']}, fixed {c['fixed']}"
          f"{' -- selection DECLINED' if verdict['selection']['declined'] else ''}", file=sys.stderr)
    if verdict["verdict"] == "UNATTRIBUTABLE" and verdict["unregistered"]:
        print(f"test_pairing: UNATTRIBUTABLE -- {verdict['unregistered']} existed on the base but the "
              "registry never ran them, so their baseline is unknown; nothing is attributed. "
              "`record-base --replace` with this lane included.", file=sys.stderr)
    elif verdict["verdict"] == "UNATTRIBUTABLE":
        print(f"test_pairing: UNATTRIBUTABLE -- the merged tree skips {guard['head']} test(s) where the "
              f"registry recorded {guard['registry']} over the same files (added {guard['added']}, "
              f"removed {guard['removed']}); a skip can hide a red, so nothing is attributed. Look at "
              "the skips, or `record-base --replace` if main itself changed.", file=sys.stderr)
    if verdict["cleanup"] != "removed":
        print(f"test_pairing: {verdict['cleanup']}", file=sys.stderr)
    return verdict["exit_code"]


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("record-base", "compare"):
        return _registry_main(argv[0], argv[1:])
    if argv and argv[0] in ("record-lane", "reuse-check"):
        return _lane_main(argv[0], argv[1:])
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        repo = Path(_git(Path(args.repo).resolve(), "rev-parse", "--show-toplevel"))
        if args.lane:
            if args.commits:
                parser.error("give either BASE HEAD or --lane, not both")
            head = resolve(repo, f"worktree-{args.lane}")
            base = _git(repo, "merge-base", args.main, head)
        elif len(args.commits) == 2:
            base, head = args.commits
        else:
            parser.error("give BASE HEAD, or --lane NAME")
        verdict = pair(repo, base, head, tests=args.tests, reruns=args.reruns,
                       workers=args.workers, timeout=args.timeout,
                       workdir=Path(args.workdir) if args.workdir else None,
                       confirm_baseline=not args.no_confirm_baseline)
    except PairingError as exc:
        print(f"test_pairing: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    _publish(verdict, Path(args.out) if args.out else receipts_home(repo) / VERDICT_NAME)
    c = verdict["counts"]
    print(f"test_pairing: {verdict['verdict']} -- lane {c['lane']} (turned red {c['turned_red']}), "
          f"pre-existing {c['preexisting']}, flake {c['flakes']}, fixed {c['fixed']}"
          f"{' -- selection DECLINED' if verdict['selection']['declined'] else ''}",
          file=sys.stderr)
    if verdict["cleanup"] != "removed":
        print(f"test_pairing: {verdict['cleanup']}", file=sys.stderr)
    return verdict["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
