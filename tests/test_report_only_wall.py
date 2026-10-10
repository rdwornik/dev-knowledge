"""The [#501] report-only wall's workflow contract, pinned as data rather than as prose.

WHY THIS FILE EXISTS. The wall is the one organ in this repo whose defects are invisible
locally: a bad input is a `##[warning]` nobody reads, and a mis-gated job is a bill nobody
sees. Both happened. LA-2 passed `python-version-file:` to an action that does not accept it,
so the line CLAIMED a runner-Python pin it never delivered — silently, on every run. LA-4 let
a pilot with no verdict run on every push to `main`, ~70s each, emitting `not checked` 84
times. Neither is caught by any local gate, and neither would be caught by re-reading the YAML
carefully, because both look correct.

THE ASYMMETRY THIS FILE PROTECTS, and it is the load-bearing one: the **record** job must fire
on EVERY push to `main` — a wall with a filter is not a record of what landed — while the
**pilot** must fire only when it has something to do. That is why the gate is per-job (a
`changes` job feeding the pilot's `if`) and NOT a workflow-level `paths:` filter, which would
gate both. A future edit reaching for the simpler `paths:` would quietly disarm the wall, so
`test_the_record_job_is_never_gated` asserts the asymmetry directly.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

_WF = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "report-only-wall.yml"

requires_workflow = pytest.mark.skipif(not _WF.is_file(), reason="workflow absent")


def _load() -> dict:
    doc = yaml.safe_load(_WF.read_text(encoding="utf-8"))
    # PyYAML resolves the bare key `on:` to the BOOLEAN True (YAML 1.1 truthiness), so a test
    # reading doc["on"] silently gets None and asserts nothing. Normalised once, here.
    if True in doc and "on" not in doc:
        doc["on"] = doc.pop(True)
    return doc


@requires_workflow
def test_the_trigger_is_push_to_main_plus_dispatch():
    """The whole [#255] correction is the TRIGGER: its predecessor was `pull_request`, which
    never fired under a local-merge workflow. Pinned so a future edit cannot quietly undo the
    one property that makes this organ different from the one that was deleted."""
    on = _load()["on"]
    assert on["push"]["branches"] == ["main"]
    assert "workflow_dispatch" in on


@requires_workflow
def test_no_step_passes_an_input_the_action_does_not_accept():
    """LA-2 regression pin. `python-version-file:` is not a `setup-uv@v5` input; passing it
    produced `##[warning]Unexpected input(s)` on both jobs while the value was ignored, so the
    workflow asserted a pin it did not deliver. uv reads `.python-version` itself during
    `uv sync`, which is where the pin was always actually enforced.

    Asserted over EVERY step of every job rather than the two known sites: the defect class is
    "an input that looks plausible and is silently dropped", and it recurs by copy-paste."""
    doc = _load()
    for job_name, job in doc["jobs"].items():
        for step in job.get("steps", []):
            with_ = step.get("with") or {}
            assert "python-version-file" not in with_, (
                f"{job_name} / {step.get('name') or step.get('uses')} passes "
                "`python-version-file:` — not a setup-uv@v5 input (LA-2)")


@requires_workflow
def test_the_record_job_is_never_gated():
    """THE ASYMMETRY. The wall records what LANDED, so it fires on every push — no `if`, no
    `needs`, and no workflow-level `paths:` filter that would reach it. This is the assertion
    that stops someone gating the pilot the easy way and disarming the recorder with it."""
    doc = _load()
    record = doc["jobs"]["record"]
    assert "if" not in record, "the record job must fire on every push"
    assert "needs" not in record, "the record job must not wait on another job"
    assert "paths" not in doc["on"]["push"], (
        "a workflow-level paths filter would gate the RECORD job too — gate the pilot "
        "per-job instead")
    assert "paths-ignore" not in doc["on"]["push"]


@requires_workflow
def test_the_mutation_pilot_is_gated_until_502_has_a_verdict():
    """LA-4 regression pin. The pilot runs on manual dispatch, or when a push actually touched
    its own subject — never unconditionally. Both arms are asserted: dropping the dispatch arm
    would make the pilot unrunnable on demand, and dropping the other would restore the
    every-push burn."""
    doc = _load()
    pilot = doc["jobs"]["mutation-pilot"]
    cond = " ".join(str(pilot.get("if", "")).split())
    assert cond, "the mutation pilot must carry a gate ([#502] has no verdict yet)"
    assert "workflow_dispatch" in cond, "the pilot must stay runnable on demand"
    assert "pilot_subject" in cond, "the pilot must consult the changed-subject filter"
    assert pilot.get("needs") == "changes"

    gate = doc["jobs"]["changes"]
    assert gate["outputs"]["pilot_subject"], "the filter job must publish its verdict"

    # [#1103] / R81.3: "on demand and nightly". The schedule arm is a third admitted event, added
    # beside the two above (neither is weakened). On a schedule the `changes` job answers
    # pilot_subject=false (no `event.before`), so only the event-name arm can admit the nightly run.
    on = doc["on"]
    assert on.get("schedule"), "the wall must carry a nightly schedule (R81.3)"
    crons = [entry["cron"] for entry in on["schedule"]]
    assert len(crons) == 1, "one nightly run, not several"
    minute, hour = crons[0].split()[:2]
    assert minute.isdigit() and hour.isdigit(), "a fixed nightly time, not a */N cadence"
    assert minute != "0", "an off-hour minute: GitHub drops on-the-hour schedule load"
    assert "github.event_name == 'schedule'" in cond, "the pilot must admit the scheduled event"

    # P-L3-3 (S-34): a scheduled run must not displace a pending push `record` run, so the pilot
    # carries its own job-level concurrency group, distinct from the workflow's.
    pilot_group = (pilot.get("concurrency") or {}).get("group", "")
    assert pilot_group and pilot_group != doc["concurrency"]["group"]
    assert pilot["concurrency"].get("cancel-in-progress") is False

    # Codex review HIGH (close-out of this lane): the job-level group does not lift the run out of
    # the WORKFLOW-level group, and a run that queues behind an active one replaces an earlier
    # PENDING run in the same group -- so a nightly run could displace a pending push `record`
    # (the record of a landed sha, which must never be dropped). The workflow group therefore
    # keys the schedule event apart from pushes, and still never cancels in progress.
    wf_group = doc["concurrency"]["group"]
    assert "github.event_name == 'schedule'" in wf_group, (
        "the scheduled run must sit in its own workflow-level concurrency group")
    assert "github.ref" in wf_group, "the push group stays keyed by ref"
    assert doc["concurrency"].get("cancel-in-progress") is False


@requires_workflow
def test_the_nightly_pilot_keeps_only_its_artifact_and_summary():
    """[#1103] Done 4b. R81.3 does not authorise a write-back: the nightly run records to its
    step summary and its artifact, and the workflow's token stays read-only."""
    doc = _load()
    assert doc["permissions"] == {"contents": "read"}
    for name, job in doc["jobs"].items():
        assert "permissions" not in job or "write" not in str(job["permissions"]), name


@requires_workflow
def test_the_pilot_filter_answers_false_when_it_cannot_tell():
    """FAILS TOWARD NOT-RUNNING. An unresolvable push range (branch creation, a force-push
    over the parent) must answer false rather than guessing true — guessing true reinstates
    exactly the every-push behaviour the gate removes. Asserted on the step's script text,
    which is where the decision lives."""
    doc = _load()
    script = "".join(s.get("run", "") for s in doc["jobs"]["changes"]["steps"])
    assert "pilot_subject=false" in script
    assert "0000000000000000000000000000000000000000" in script, (
        "the all-zero before-sha (branch creation) must be handled explicitly")


@requires_workflow
def test_every_measured_leg_still_records_rather_than_judges():
    """The organ's defining posture, unchanged by this arc's gating work: the measured legs
    are `continue-on-error`, so a RED is recorded and the job stays green. A setup failure
    still reds the job deliberately — a green job with no environment would be a lie — so this
    asserts the posture of the MEASURED steps only, not of every step."""
    doc = _load()
    measured = [s for s in doc["jobs"]["record"]["steps"]
                if "recorded, never blocking" in (s.get("name") or "")]
    assert len(measured) >= 3, f"expected the three measured legs, found {len(measured)}"
    for s in measured:
        assert s.get("continue-on-error") is True, f"{s['name']} must not block"


# --- [#1103] S-56 (CI-clock amend): the pilot's copy, and a pilot that cannot pass empty -------

_ROOT = Path(__file__).resolve().parent.parent

# The exact tail of run 38061081144's `mutmut.out` (artifact mutation-pilot-ff57acc4...): the pilot
# job concluded `success` with this on its screen and 0 mutants executed.
_FAILED_TO_COLLECT = (
    "ERROR tests/test_fleet_analytics.py - validate_hermetization.ShapeSpecError: fleet shape spec "
    "absent: /home/runner/work/dev-knowledge/dev-knowledge/mutants/ecosystem/fleet-shape-spec.yaml\n"
    "1 error in 22.66s\n"
    "failed to collect stats. runner returned 2\n"
)
# mutmut's progress line, as it writes it to stdout: "\r<spinner> <executed>/<total>  <killed emoji>
# <killed> <no-tests emoji> ..." (emoji written as escapes: a test file stays ASCII-clean).
_KILLED = "\U0001F389"
_REST = " 0 \U0001FAE5 0  ⏰ 0  \U0001F914 0  \U0001F641 "


def _mutmut_table() -> dict:
    return tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["mutmut"]


def test_the_mutmut_copy_carries_the_data_files_the_import_chain_reads():
    """[#1103] S-56. mutmut copies `scripts/`, `tests/` and the project files into `mutants/`
    and nothing else, then runs the suite there. The import chain of `scripts/fleet_analytics.py`
    reads `ecosystem/fleet-shape-spec.yaml` at import time (`validate_hermetization.SHAPE_SPEC`,
    since 01104de3), so without `also_copy` the pilot collects no test: run 38061081144, 0
    mutants executed, "failed to collect stats". Every entry must also EXIST: mutmut skips an
    absent `also_copy` path in silence, so a typo would re-open the same hole."""
    also = _mutmut_table().get("also_copy", [])
    assert "ecosystem/fleet-shape-spec.yaml" in also
    for entry in also:
        assert (_ROOT / entry).exists(), f"also_copy names a path that is not in the repo: {entry}"


def test_a_file_entry_of_also_copy_follows_a_directory_entry_that_creates_its_parent():
    """[#1103] S-56, shown by dispatched run 38072722475: mutmut 3.7.0's `copy_also_copy_files`
    copies a FILE with a bare `shutil.copy2`, which does not create `mutants/<parent>/`, and
    `mutants/ecosystem/` does not exist (only the source paths are copied first), so a lone
    `ecosystem/fleet-shape-spec.yaml` entry crashed the run with FileNotFoundError. A DIRECTORY
    entry goes through `copytree`, which does create the parents. So a file entry works only
    after a directory entry at or below its parent."""
    seen: list[Path] = []
    for entry in _mutmut_table().get("also_copy", []):
        path = Path(entry)
        if (_ROOT / path).is_dir():
            seen.append(path)
            continue
        parent = path.parent
        if parent != Path("."):
            assert any(parent == d or parent in d.parents for d in seen), (
                f"{entry}: mutants/{parent.as_posix()} does not exist when this file is copied; "
                "list a directory entry at or below it first")


def _copy_the_way_mutmut_does(dest: Path) -> None:
    """mutmut 3.7.0, `copy_src_dir` then `copy_also_copy_files`, for this table's `source_paths`
    and the files it always copies. The also_copy loop is mutmut's own, bug included."""
    table = _mutmut_table()
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    for name in (*table["source_paths"], "tests"):
        shutil.copytree(_ROOT / name, dest / name, ignore=ignore)
    for name in ("pyproject.toml", "uv.lock"):
        shutil.copy2(_ROOT / name, dest / name)
    for entry in table.get("also_copy", []):
        src, dst = _ROOT / entry, dest / entry
        if not src.exists():
            continue
        if src.is_file():
            shutil.copy2(src, dst)        # no parent created: mutmut's behaviour
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)


def test_the_mutants_copy_collects_the_pilots_tests(tmp_path):
    """[#1103] S-56, the outcome the pilot needs before it can execute one mutant: in the copy
    mutmut builds, the selected tests COLLECT. This is the step that failed on run 38061081144
    ("failed to collect stats", 0 mutants executed) and, with the shape spec alone, would fail on
    the next data file the import chain reads. The directory is named `mutants`: the suite
    itself branches on that name (test_hub_is_included_as_a_mining_target)."""
    mutants = tmp_path / "mutants"
    mutants.mkdir()
    _copy_the_way_mutmut_does(mutants)
    selected = _mutmut_table()["pytest_add_cli_args_test_selection"]
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-o", "addopts=", "-n", "0",
         "-p", "no:cacheprovider", *selected],
        cwd=mutants, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    assert proc.returncode == 0, (proc.stdout + proc.stderr)[-1500:]


def _pilot_check_script() -> str:
    """The python heredoc of the pilot's `executed no mutant` step, as the runner receives it."""
    steps = _load()["jobs"]["mutation-pilot"]["steps"]
    named = [s for s in steps if "executed" in (s.get("name") or "")]
    assert len(named) == 1, "the pilot must carry exactly one step that checks a mutant executed"
    step = named[0]
    # Report-only is the posture of the MEASURED steps; this one judges whether they measured
    # anything, so it must be able to fail the job and must run after a failed measured step.
    assert step.get("continue-on-error") is not True, "the vacuity check must be able to fail the job"
    assert "always()" in str(step.get("if", "")), "it must run after a failed measured step too"
    run = step["run"]
    start = run.index("<<'PY'\n") + len("<<'PY'\n")
    return run[start:run.rindex("\nPY")]


def _run_pilot_check(tmp_path: Path, mutmut_out: str | None) -> subprocess.CompletedProcess:
    if mutmut_out is not None:
        (tmp_path / "mutmut.out").write_bytes(mutmut_out.encode("utf-8"))
    return subprocess.run([sys.executable, "-"], input=_pilot_check_script().encode("ascii"),
                          cwd=tmp_path, capture_output=True, timeout=60)


@requires_workflow
@pytest.mark.parametrize("label,out", [
    ("the failed run's own output", _FAILED_TO_COLLECT),
    ("a progress line with 0 executed", "\r⠋ 0/84  " + _KILLED + _REST + "0\n"),
    ("no progress line at all", "done\n"),
    ("no mutmut.out at all", None),
], ids=["failed-run-output", "zero-executed", "no-progress-line", "no-file"])
def test_a_pilot_that_executed_no_mutant_fails_the_job(tmp_path, label, out):
    """[#1103] S-56 Done 4c. A check that passes while checking nothing is a false positive: every
    measured step is `continue-on-error`, so the job read `success` on run 38061081144 with 0
    mutants executed. The step the job ends with fails on `failed to collect stats`, on an
    executed count of 0, and on a missing progress line. The script under test is the one the
    workflow carries, extracted and run, not a copy of its logic."""
    proc = _run_pilot_check(tmp_path, out)
    assert proc.returncode != 0, f"{label}: the vacuous pilot passed ({proc.stdout!r})"


@requires_workflow
def test_a_pilot_that_executed_a_mutant_passes_the_check(tmp_path):
    """The other half of the pin: the same step stays quiet when the tool executed mutants,
    killed or survived. A step that fails everything would also satisfy the test above."""
    out = ("\r⠋ 1210/2291  " + _KILLED + " 865" + _REST + "345\n"
           "\r⠙ 2291/2291  " + _KILLED + " 865" + _REST + "1426\n")
    proc = _run_pilot_check(tmp_path, out)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
