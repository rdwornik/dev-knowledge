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
"I evaluated nothing" must not read as "nothing is red").

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

HONEST LIMITS. (1) A test red on BASE for a flaky reason and green on HEAD shows as `fixed`.
(2) A test whose result depends on gitignored state (e.g. `ecosystem/*/state.yaml`) sees neither
side's copy -- both clones lack it, so it cannot skew the PAIR, but the reds it produces are
reds of a bare checkout. (3) `impacted_tests` measures a miss-rate of about one affected file in
twenty; a clean pairing is not a full-suite pass.
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
"""
_PLUGIN_NAME = "tp_events_plugin"


def read_events(path: Path) -> dict[str, str]:
    """{nodeid: PASSED|FAILED|ERROR} from the plugin's JSON lines; stdlib only.

    `path` is one file, or the prefix of the per-process files `<prefix>.<pid>` the plugin writes
    (one writer per file, so xdist workers cannot interleave). It FAILS CLOSED: no file at all
    means the plugin never ran, and a malformed row means a result may have been lost -- either
    would otherwise read as "nothing is red". A failed `call` is FAILED; a failed
    setup/teardown/collect is ERROR; a red is never overwritten by a green; duplicates (xdist
    reports in both the worker and the controller) change nothing.
    """
    files = [path] if path.is_file() else sorted(path.parent.glob(path.name + ".*"))
    if not files:
        raise PairingError(f"no event file at {path.name}: the reporting plugin did not run")
    results: dict[str, str] = {}
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
            else:
                continue
            if status in _RED:
                if results.get(test_id) not in _RED or (status == "FAILED"
                                                        and results[test_id] == "ERROR"):
                    results[test_id] = status
            else:
                results.setdefault(test_id, status)
    return results


def run_pytest(clone: Path, args: list[str], *, workers: int, timeout: float | None) -> dict[str, str]:
    scratch = clone.parent
    (scratch / f"{_PLUGIN_NAME}.py").write_text(_PLUGIN, encoding="utf-8", newline="\n")
    events = scratch / f"events-{uuid.uuid4().hex}.jsonl"
    cmd = [sys.executable, "-m", "pytest", "-q", "--no-header", "--color=no",
           "-p", "no:cacheprovider", "-p", _PLUGIN_NAME, "--continue-on-collection-errors",
           *_xdist_args(workers), *args]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
           "TEST_PAIRING_EVENTS": str(events),
           # The caller's PYTHONPATH is DROPPED: a source checkout on it could shadow the tree
           # under test and hide a lane-caused red. Only the plugin's directory is added.
           "PYTHONPATH": str(scratch)}
    try:
        done = subprocess.run(cmd, cwd=clone, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise PairingError(f"pytest exceeded {timeout}s in {clone.name}") from exc
    tail = (done.stderr or done.stdout).strip()[-400:]
    if done.returncode in (3, 4):
        raise PairingError(f"pytest exited {done.returncode} in {clone.name}: {tail}")
    results = read_events(events)
    if done.returncode == 2 and not results:
        raise PairingError(f"pytest was interrupted in {clone.name} with no result: {tail}")
    if done.returncode == 1 and not any(v in _RED for v in results.values()):
        raise PairingError(f"pytest reported failures in {clone.name} but the events show none: {tail}")
    return results


# --- selection ---------------------------------------------------------------------------

def _changed(repo: Path, base: str, head: str) -> list[str]:
    out = _git(repo, "diff", "--name-only", base, head)
    return [line for line in out.splitlines() if line]


def choose_tests(clone: Path, changed: list[str]) -> dict:
    """The selection block: what to run on HEAD, and whether the selector declined."""
    selection = impacted_tests.select(clone, changed)
    if selection.full_suite:
        own = sorted(c for c in changed if _TEST_FILE.search(c) and (clone / c).is_file())
        return {
            "declined": True, "ran_full_suite": False, "marker": None, "test_files": own,
            "reasons": {k: list(v) for k, v in selection.reasons.items()},
            "note": ("impacted selection declined to narrow (full suite); "
                     + ("ran only the test files this diff changed -- a PARTIAL pairing"
                        if own else "no changed test file to fall back on -- nothing was run")),
        }
    files = [f for f in selection.test_files if (clone / f).is_file()]
    return {
        "declined": False, "ran_full_suite": False,
        "marker": selection.marker if not files else None, "test_files": files,
        "reasons": {k: list(v) for k, v in selection.reasons.items()},
        "note": "narrowed by impacted_tests.select",
    }


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


def main(argv: list[str] | None = None) -> int:
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
    out = Path(args.out) if args.out else (
        Path(os.environ.get("HARNESS_RECEIPTS_DIR") or repo / "logs" / "receipts") / VERDICT_NAME
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, out)
    print(json.dumps(verdict, indent=2))
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
