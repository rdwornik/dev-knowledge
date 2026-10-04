"""CI's verdict read as data (LANE-5A-6). Fixture runs for green, red and not-run.

Every `gh` call is injected (`list_fn`/`view_fn`/`jobs_fn`/`log_fn`) so these tests never shell
out and never sleep for real -- `sleep_fn`/`clock_fn` are fakes too, which is what lets the
IN-PROGRESS-then-completes and the timeout-while-waiting cases run in test time rather than
`POLL_TIMEOUT_S`.
"""
from __future__ import annotations

import json
import subprocess

import pytest

import ci_verdict as cv

_LOG_PREFIX = "pytest\tUNKNOWN STEP\t2026-09-23T19:20:47.0000000Z "


def _log_line(text: str) -> str:
    return _LOG_PREFIX + text


def _suite_gate_log(baseline: str, regressions: tuple = ()) -> str:
    lines = [_log_line("conductor suite-baseline gate"), _log_line(""),
             _log_line(f"baseline sha   : {baseline}"),
             _log_line("baseline source: Actions `conductor` run **1**, `push`, x"),
             _log_line("baseline pin   : -n 4"), _log_line("frozen members : 87"), _log_line("")]
    lines.append(_log_line("pre-existing   : 0"))
    lines.append(_log_line(f"regressions    : {len(regressions)}"))
    for nid in regressions:
        lines.append(_log_line(f"  REGRESSION    {nid}"))
    lines.append(_log_line(""))
    verdict = "PASS" if not regressions else f"FAIL -- REGRESSION -- {len(regressions)} failure(s)"
    lines.append(_log_line(f"verdict        : {verdict}"))
    return "\n".join(lines)


def _run(sha: str, *, run_id: int = 1, status: str = "completed",
        conclusion: str = "success") -> dict:
    # `event: push` since foundation-4 item 11 (G7): the one verdict function reads PUSH runs
    # only, so a fixture run that does not say it is one is not a candidate.
    return {"databaseId": run_id, "headSha": sha, "status": status, "conclusion": conclusion,
            "event": "push",
            "displayTitle": "a merge", "url": f"https://github.com/x/x/actions/runs/{run_id}",
            "createdAt": "2026-09-24T00:00:00Z", "updatedAt": "2026-09-24T00:08:00Z"}


def _list_fn(runs: list):
    def fn(*, repo_root, workflow=cv.WORKFLOW):
        return runs
    return fn


def _jobs_fn(jobs: list):
    def fn(run_id, *, repo_root):
        return jobs
    return fn


def _log_fn(logs: dict):
    def fn(run_id, job_id, *, repo_root):
        return logs.get(job_id)
    return fn


def _no_sleep(_seconds):
    return None


def _fake_time():
    """A controllable (clock_fn, sleep_fn) pair. Every test whose `wait_for_run` loop can run
    more than one iteration MUST use this (or an equivalent bound) rather than the real clock --
    a real `time.monotonic` with a no-op `sleep_fn` busy-loops for the WHOLE real `timeout_s`
    (Codex terra, 2026-09-24, HIGH: this is exactly what made the first real run of this file
    take ~900s on one test alone)."""
    clock = {"t": 0.0}

    def clock_fn():
        return clock["t"]

    def sleep_fn(seconds):
        clock["t"] += seconds

    return clock_fn, sleep_fn


# --- green --------------------------------------------------------------------------------

def test_a_clean_run_is_GREEN_and_carries_the_baseline_id_even_with_no_regressions():
    jobs = [{"name": "pytest", "conclusion": "success", "databaseId": 9},
           {"name": "ruff", "conclusion": "success", "databaseId": 10}]
    verdict = cv.verdict_for(
        "abc123", repo_root=None,
        list_fn=_list_fn([_run("abc123")]), jobs_fn=_jobs_fn(jobs),
        log_fn=_log_fn({9: _suite_gate_log("c5108329")}), sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_GREEN
    assert verdict.new_reds == ()
    assert verdict.baseline_id == "c5108329"
    assert verdict.run_id == 1
    assert verdict.run_url.endswith("/runs/1")
    assert verdict.duration_seconds == pytest.approx(480.0)


# --- red ------------------------------------------------------------------------------------

def test_a_run_with_REGRESSIONS_is_RED_and_NAMES_the_new_reds_from_the_gates_own_log():
    jobs = [{"name": "pytest", "conclusion": "failure", "databaseId": 9},
           {"name": "ruff", "conclusion": "success", "databaseId": 10}]
    log = _suite_gate_log("c5108329", regressions=("tests/test_x.py::test_a",
                                                    "tests/test_y.py::test_b"))
    verdict = cv.verdict_for(
        "def456", repo_root=None,
        list_fn=_list_fn([_run("def456", conclusion="failure")]), jobs_fn=_jobs_fn(jobs),
        log_fn=_log_fn({9: log}), sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_RED
    assert verdict.new_reds == ("tests/test_x.py::test_a", "tests/test_y.py::test_b")
    assert verdict.baseline_id == "c5108329"
    assert "new red" in verdict.reason


def test_a_run_that_CONCLUDES_non_success_with_no_failing_job_is_RED_not_green():
    """The workflow's own `conclusion` is checked too, never inferred solely from job
    conclusions -- a `cancelled`/`timed_out` run with every listed job reading success/skipped
    (or an empty job list) must not read as green (Codex terra, 2026-09-24, HIGH)."""
    jobs = [{"name": "pytest", "conclusion": "success", "databaseId": 9}]
    verdict = cv.verdict_for(
        "jkl012", repo_root=None,
        list_fn=_list_fn([_run("jkl012", conclusion="cancelled")]), jobs_fn=_jobs_fn(jobs),
        log_fn=_log_fn({9: _suite_gate_log("c5108329")}), sleep_fn=_no_sleep)

    # foundation-4 item 11 (G7): a CANCELLED run is not evidence of a red, it is the absence of a
    # verdict (`cancel-in-progress` cancels the older run when a newer push lands). It was
    # RED/`workflow:cancelled`, which named a "new red" that no test or job had produced. It
    # still fails closed -- never green -- but as NOT-RUN with its own state.
    assert verdict.verdict == cv.STATE_NOT_RUN
    assert verdict.state == "CANCELLED"
    assert "cancelled" in verdict.reason


def test_a_RED_run_with_no_suite_gate_block_falls_back_to_NAMING_the_failing_jobs():
    """`ruff` broke before the pytest job's gate step ever ran -- there is no regression list
    to read, so the fallback names what actually failed rather than reporting nothing."""
    jobs = [{"name": "pytest", "conclusion": "success", "databaseId": 9},
           {"name": "ruff", "conclusion": "failure", "databaseId": 10}]
    verdict = cv.verdict_for(
        "ghi789", repo_root=None,
        list_fn=_list_fn([_run("ghi789", conclusion="failure")]), jobs_fn=_jobs_fn(jobs),
        log_fn=_log_fn({9: _suite_gate_log("c5108329")}), sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_RED
    assert verdict.new_reds == ("ruff",)
    assert "job(s) did not conclude success" in verdict.reason


# --- not-run --------------------------------------------------------------------------------

def test_no_matching_run_is_NOT_RUN_and_never_reads_as_a_pass():
    """A bounded fake clock, not the real one -- an empty `list_fn` never finds a run, so an
    unbounded wait would spin for the real `timeout_s` (see `_fake_time`'s docstring)."""
    clock_fn, sleep_fn = _fake_time()

    verdict = cv.verdict_for("ghost", repo_root=None, list_fn=_list_fn([]),
                             timeout_s=30, interval_s=10, sleep_fn=sleep_fn, clock_fn=clock_fn)

    assert verdict.verdict == cv.STATE_NOT_RUN
    assert verdict.run_id is None
    assert "no Actions run matched" in verdict.reason


def test_gh_UNAVAILABLE_is_NOT_RUN_not_a_silent_pass():
    def broken_list(*, repo_root, workflow=cv.WORKFLOW):
        raise cv.GhUnavailable("gh is not installed")

    verdict = cv.verdict_for("abc", repo_root=None, list_fn=broken_list, sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_NOT_RUN
    assert "gh unavailable" in verdict.reason


def test_an_UNREADABLE_job_list_is_NOT_RUN_not_a_silent_pass():
    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc")]),
        jobs_fn=lambda run_id, *, repo_root: None, sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_NOT_RUN
    assert "job list could not be read" in verdict.reason
    assert verdict.run_id == 1


def test_a_run_still_IN_PROGRESS_past_the_timeout_is_NOT_RUN_and_NAMES_the_run():
    """Fully hermetic: a fake clock so the timeout fires without any real waiting, and an
    injected `view_fn` so re-polling never shells out to the real `gh`."""
    clock_fn, sleep_fn = _fake_time()
    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", status="in_progress")]),
        view_fn=lambda run_id, *, repo_root: _run("abc", status="in_progress"),
        timeout_s=10, interval_s=5, sleep_fn=sleep_fn, clock_fn=clock_fn)

    assert verdict.verdict == cv.STATE_NOT_RUN
    assert verdict.run_id == 1
    assert "still in_progress" in verdict.reason


def test_a_run_FOUND_then_UNREADABLE_on_a_later_poll_keeps_the_run_id_it_already_had():
    """The honest-limit fix: a transient `gh` failure on a RE-poll must not erase a run this
    organ already confirmed existed."""
    calls = {"n": 0}

    def flaky_view(run_id, *, repo_root):
        calls["n"] += 1
        raise cv.GhUnavailable("HTTP 502")

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", status="in_progress")]),
        view_fn=flaky_view, timeout_s=10, interval_s=5, sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_NOT_RUN
    assert verdict.run_id == 1
    assert "could not read it" in verdict.reason
    assert calls["n"] == 1


# --- polling actually waits ------------------------------------------------------------------

def test_waiting_POLLS_IN_PROCESS_until_the_run_completes():
    """The run is IN-PROGRESS on the first read and COMPLETED on the second -- this organ must
    re-read it itself rather than returning the stale IN-PROGRESS answer."""
    calls = {"n": 0}

    def view_fn(run_id, *, repo_root):
        calls["n"] += 1
        status = "in_progress" if calls["n"] == 1 else "completed"
        return _run("abc", status=status)

    sleeps = []
    clock_fn, real_sleep_fn = _fake_time()

    def sleep_fn(seconds):
        sleeps.append(seconds)
        real_sleep_fn(seconds)

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", status="in_progress")]),
        view_fn=view_fn, jobs_fn=_jobs_fn([{"name": "pytest", "conclusion": "success",
                                            "databaseId": 9}]),
        log_fn=_log_fn({9: _suite_gate_log("c5108329")}),
        sleep_fn=sleep_fn, timeout_s=1000, interval_s=5, clock_fn=clock_fn)

    assert verdict.verdict == cv.STATE_GREEN
    assert calls["n"] >= 1
    assert sleeps, "the wait must actually sleep between polls"


# --- CLI --------------------------------------------------------------------------------------

def test_the_cli_prints_JSON_and_exits_ZERO_on_green(monkeypatch, tmp_path):
    from click.testing import CliRunner

    monkeypatch.setattr(cv, "resolve_sha", lambda ref, *, repo_root: "abc123")
    monkeypatch.setattr(cv, "list_runs", lambda *, repo_root, workflow=cv.WORKFLOW: [_run("abc123")])
    monkeypatch.setattr(cv, "fetch_jobs", lambda run_id, *, repo_root: [
        {"name": "pytest", "conclusion": "success", "databaseId": 9}])
    monkeypatch.setattr(cv, "fetch_job_log",
                        lambda run_id, job_id, *, repo_root: _suite_gate_log("c5108329"))

    result = CliRunner().invoke(cv.cli, ["--ref", "abc123", "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["verdict"] == "green"
    assert payload["baseline_id"] == "c5108329"


def test_the_cli_exits_NON_ZERO_on_red(monkeypatch, tmp_path):
    from click.testing import CliRunner

    monkeypatch.setattr(cv, "resolve_sha", lambda ref, *, repo_root: "def456")
    monkeypatch.setattr(cv, "list_runs",
                        lambda *, repo_root, workflow=cv.WORKFLOW: [_run("def456",
                                                                        conclusion="failure")])
    monkeypatch.setattr(cv, "fetch_jobs", lambda run_id, *, repo_root: [
        {"name": "pytest", "conclusion": "failure", "databaseId": 9}])
    monkeypatch.setattr(cv, "fetch_job_log",
                        lambda run_id, job_id, *, repo_root: _suite_gate_log(
                            "c5108329", regressions=("tests/test_x.py::test_a",)))

    result = CliRunner().invoke(cv.cli, ["--ref", "def456", "--repo-root", str(tmp_path)])

    assert result.exit_code != 0
    payload = json.loads(result.output)
    assert payload["verdict"] == "red"
    assert payload["new_reds"] == ["tests/test_x.py::test_a"]


def test_the_cli_exits_NON_ZERO_on_not_run(monkeypatch, tmp_path):
    from click.testing import CliRunner

    monkeypatch.setattr(cv, "resolve_sha", lambda ref, *, repo_root: "ghost")
    monkeypatch.setattr(cv, "list_runs", lambda *, repo_root, workflow=cv.WORKFLOW: [])

    result = CliRunner().invoke(cv.cli, ["--ref", "ghost", "--repo-root", str(tmp_path),
                                        "--timeout", "0", "--interval", "0"])

    assert result.exit_code != 0
    payload = json.loads(result.output)
    assert payload["verdict"] == "not-run"


# --- the parser itself ------------------------------------------------------------------------

def test_parse_suite_gate_block_reads_the_baseline_and_every_regression():
    log = _suite_gate_log("c5108329", regressions=("tests/test_a.py::test_1",
                                                    "tests/test_b.py::test_2"))

    block = cv.parse_suite_gate_block(log)

    assert block["found"] is True
    assert block["baseline_id"] == "c5108329"
    assert block["regressions"] == ("tests/test_a.py::test_1", "tests/test_b.py::test_2")


def test_parse_suite_gate_block_reports_NOT_FOUND_when_the_gate_step_never_ran():
    block = cv.parse_suite_gate_block(_log_line("Sync the locked environment") + "\n"
                                      + _log_line("ERROR: uv sync failed"))

    assert block["found"] is False
    assert block["baseline_id"] is None
    assert block["regressions"] == ()


def _log_line_at(ts: str, text: str) -> str:
    return f"pytest\tUNKNOWN STEP\t{ts} {text}"


# --- foundation-4 item 11 (G7): ONE verdict function ------------------------------------------
# RED-first witnesses. Before this lane `verdict_for` listed runs of EVERY event, treated a
# cancelled run as a named red, and knew only a job called exactly `pytest` -- the matrix legs
# (`pytest (ubuntu-latest)`) never reached the suite-gate log read.

_LEG_U, _LEG_W = "pytest (ubuntu-latest)", "pytest (windows-latest)"
_ALL_SIX = (_LEG_U, _LEG_W, "ruff", "seal", "spine", "anchor")


def _jobs_all_success(*names):
    return [{"name": n, "conclusion": "success", "databaseId": 200 + i}
            for i, n in enumerate(names or _ALL_SIX)]


def test_G7_a_non_PUSH_run_for_the_sha_is_never_the_verdict():
    other = {**_run("abc123"), "event": "pull_request"}

    verdict = cv.verdict_for("abc123", repo_root=None, list_fn=_list_fn([other]),
                             timeout_s=0, interval_s=1, sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_NOT_RUN
    assert verdict.state == "NO-RUN"


def test_G7_list_runs_asks_gh_for_push_runs_only(monkeypatch, tmp_path):
    seen = []

    def fake_gh(command, *, repo_root, timeout=cv.GH_TIMEOUT_S):
        seen.append(command)
        return []

    monkeypatch.setattr(cv, "_gh_json", fake_gh)

    cv.list_runs(repo_root=tmp_path)

    assert "--event" in seen[0] and seen[0][seen[0].index("--event") + 1] == "push"


def test_G7_a_run_still_in_progress_at_the_poll_timeout_is_NOT_RUN_with_state_IN_PROGRESS():
    clock_fn, sleep_fn = _fake_time()

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", status="in_progress")]),
        view_fn=lambda run_id, *, repo_root: _run("abc", status="in_progress"),
        timeout_s=10, interval_s=5, sleep_fn=sleep_fn, clock_fn=clock_fn)

    assert verdict.verdict == cv.STATE_NOT_RUN and verdict.state == "IN-PROGRESS"
    assert verdict.run_id == 1


def test_G7_gh_UNAVAILABLE_carries_its_own_state():
    def broken_list(*, repo_root, workflow=cv.WORKFLOW):
        raise cv.GhUnavailable("no gh")

    verdict = cv.verdict_for("abc", repo_root=None, list_fn=broken_list, sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_NOT_RUN and verdict.state == "GH-UNAVAILABLE"


def test_G7_the_matrix_LEGS_are_read_for_the_suite_gate_block_not_only_a_job_named_pytest():
    """`pytest (windows-latest)` red with a REGRESSION in its gate block: the old exact-name
    lookup found no pytest job and fell back to naming the job."""
    jobs = [{"name": _LEG_U, "conclusion": "success", "databaseId": 9},
            {"name": _LEG_W, "conclusion": "failure", "databaseId": 10}]
    log = _suite_gate_log("c5108329", regressions=("tests/test_x.py::test_a",))

    verdict = cv.verdict_for(
        "def456", repo_root=None,
        list_fn=_list_fn([_run("def456", conclusion="failure")]), jobs_fn=_jobs_fn(jobs),
        log_fn=_log_fn({10: log}), sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_RED
    assert verdict.new_reds == (f"{_LEG_W}: tests/test_x.py::test_a",)


def test_G7_every_REQUIRED_context_must_be_present_and_success():
    """The merge path names its required contexts; a completed all-success run that never showed
    `spine` is not mergeable (the ruleset would refuse it too)."""
    names = tuple(n for n in _ALL_SIX if n != "spine")

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc")]),
        jobs_fn=_jobs_fn(_jobs_all_success(*names)), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.verdict == cv.STATE_RED
    assert verdict.missing_contexts == ("spine",)
    assert "spine" in verdict.reason


def test_G7_a_SKIPPED_required_context_is_not_a_success():
    jobs = _jobs_all_success()
    jobs[3] = {**jobs[3], "conclusion": "skipped"}

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc")]), jobs_fn=_jobs_fn(jobs),
        log_fn=_log_fn({}), sleep_fn=_no_sleep, required_contexts=_ALL_SIX)

    assert verdict.verdict == cv.STATE_RED
    assert "seal" in verdict.missing_contexts


def test_G7_all_six_contexts_success_is_GREEN():
    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc")]),
        jobs_fn=_jobs_fn(_jobs_all_success()), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.verdict == cv.STATE_GREEN and verdict.state == "PASS"
    assert verdict.missing_contexts == ()


def test_G4_ONE_function_the_424d6c72_replay_through_ci_verdict_names_the_new_test():
    """`ci_verdict.verdict_for(.., baseline=)` classifies through `actions_verdict` -- there is no
    second classifier. The leg is red at base AND tip; only the tip carries a NEW test red."""
    import actions_verdict as av

    new_id = "tests/test_registered_check.py::test_registered_check_never_fails_on_live_repo"
    known = "tests/test_known.py::test_known_red"

    def leg_log(job, ids):
        body = ["FAILED " + i + " - AssertionError: x" for i in ids]
        return "\n".join(f"{job}\tRun\t2026-10-02T10:00:00.0000000Z {t}" for t in body)

    tip_jobs = [{"name": _LEG_U, "conclusion": "failure", "databaseId": 9}]
    base_run = {**_run("base", conclusion="failure"), "jobs": [
        {"name": _LEG_U, "conclusion": "failure", "databaseId": 19}]}
    import known_reds as kr
    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="r", measured_at_sha="s",
                           measured_via="ci", workers=4,
                           members={known: {"attribution": kr.PRE_FREEZE}})

    verdict = cv.verdict_for(
        "tip", repo_root=None, list_fn=_list_fn([_run("tip", conclusion="failure")]),
        jobs_fn=_jobs_fn(tip_jobs),
        log_fn=lambda run_id, job_id, *, repo_root: leg_log(_LEG_U, [known, new_id])
        if job_id == 9 else leg_log(_LEG_U, [known]),
        baseline="base", fetch_base=lambda sha, *, repo_root=None, workflow=None: base_run,
        registry_loader=lambda ref, *, repo_root=None: registry, sleep_fn=_no_sleep)

    assert verdict.verdict == cv.STATE_RED
    assert verdict.state == av.STATE_REGRESSED
    assert any(new_id in r for r in verdict.new_reds)
    assert not any(known in r for r in verdict.new_reds)


# --- b2-merge-gate (R64; architect seat ruling 3 of 2026-10-04) ------------------------------
#
# RED-FIRST at `2dd2067d`: every non-pass required context read the one undifferentiated state
# `RED` (and a REQUIRED pytest leg that was merely red on both sides ALSO landed in
# `missing_contexts`, so `merge_path.is_landable` refused it however the test-level read went).
# The gate refuses only a NEW red test and a non-pass state of a required check -- each distinct.

@pytest.mark.parametrize("conclusion,state", [
    ("skipped", "SKIPPED"), ("timed_out", "TIMED-OUT"), ("cancelled", "CANCELLED"),
    (None, "IN-PROGRESS")])
def test_b2_each_non_pass_REQUIRED_context_is_its_own_refusing_state(conclusion, state):
    jobs = _jobs_all_success()
    jobs[3] = {**jobs[3], "conclusion": conclusion}

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", conclusion="failure")]),
        jobs_fn=_jobs_fn(jobs), log_fn=_log_fn({}), sleep_fn=_no_sleep, required_contexts=_ALL_SIX)

    assert verdict.verdict == cv.STATE_RED and verdict.state == state
    assert verdict.missing_contexts == ("seal",)


def test_b2_a_required_context_that_never_ran_is_NO_RUN():
    names = tuple(n for n in _ALL_SIX if n != "anchor")

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc")]),
        jobs_fn=_jobs_fn(_jobs_all_success(*names)), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.verdict == cv.STATE_RED and verdict.state == "NO-RUN"
    assert verdict.missing_contexts == ("anchor",)


def test_b2_the_run_level_TIMED_OUT_is_its_own_state_and_never_green():
    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", conclusion="timed_out")]),
        jobs_fn=_jobs_fn(_jobs_all_success()), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.verdict == cv.STATE_RED and verdict.state == "TIMED-OUT"


def test_b2_a_timed_out_context_is_a_refusal_even_with_NO_baseline_and_when_the_base_timed_out_too():
    jobs = _jobs_all_success()
    jobs[2] = {**jobs[2], "conclusion": "timed_out"}
    base_run = {**_run("base", conclusion="failure"), "jobs": jobs}

    verdict = cv.verdict_for(
        "tip", repo_root=None, list_fn=_list_fn([_run("tip", conclusion="failure")]),
        jobs_fn=_jobs_fn(jobs), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX, baseline="base",
        fetch_base=lambda sha, *, repo_root=None, workflow=None: base_run)

    assert verdict.state == "TIMED-OUT", "not laundered into PRE-EXISTING by the base"


def _leg_log(job, ids):
    body = ["FAILED " + i + " - AssertionError: x" for i in ids]
    return "\n".join(f"{job}\tRun\t2026-10-02T10:00:00.0000000Z {t}" for t in body)


def _red_on_both_sides(tip_ids, base_ids, *, registry):
    """Both pytest legs `failure` at tip and base, the other four required contexts success."""
    tip_jobs = [{"name": n, "conclusion": "failure" if n in (_LEG_U, _LEG_W) else "success",
                 "databaseId": 100 + i} for i, n in enumerate(_ALL_SIX)]
    base_jobs = [{**j, "databaseId": 300 + i} for i, j in enumerate(tip_jobs)]
    base_run = {**_run("base", conclusion="failure"), "jobs": base_jobs}

    def log_fn(run_id, job_id, *, repo_root):
        ids = tip_ids if job_id < 300 else base_ids
        return _leg_log(_LEG_U if job_id % 100 == 0 else _LEG_W, ids)

    return cv.verdict_for(
        "tip", repo_root=None, list_fn=_list_fn([_run("tip", conclusion="failure")]),
        jobs_fn=_jobs_fn(tip_jobs), log_fn=log_fn, sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX, baseline="base",
        fetch_base=lambda sha, *, repo_root=None, workflow=None: base_run,
        registry_loader=lambda ref, *, repo_root=None: registry)


def _empty_registry():
    import known_reds as kr
    return kr.Registry(schema=kr.SCHEMA, baseline_id="r", measured_at_sha="s", measured_via="ci",
                       workers=4, members={})


def test_b2_a_required_pytest_leg_that_is_RED_ON_BOTH_SIDES_is_PRE_EXISTING_with_no_missing_context():
    """The merge that introduced nothing, on a red main: both pytest legs `failure`, the same
    unregistered ids at the base. Before this lane the two legs landed in `missing_contexts`
    (and so were never landable) and the unregistered ids read REGRESSED."""
    ids = ["tests/test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH"]

    verdict = _red_on_both_sides(ids, ids, registry=_empty_registry())

    assert verdict.state == "PRE-EXISTING", verdict.reason
    assert verdict.missing_contexts == ()
    assert verdict.flagged and all("[unregistered]" in f for f in verdict.flagged)
    assert verdict.to_dict()["flagged"] == list(verdict.flagged)


def test_b2_a_PINNED_run_id_reads_that_run_alone_even_when_a_newer_green_one_exists():
    """Item 4's second half: the cancelled `main` push run (37176995845), offered ALONE, reads as a
    non-pass. Without a pin the newest push run for the sha wins, which is the right default and
    the wrong way to ask about one particular run."""
    cancelled = _run("abc", run_id=11, conclusion="cancelled")
    newer = _run("abc", run_id=12, conclusion="success")

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([newer, cancelled]),
        view_fn=lambda rid, *, repo_root: {11: cancelled, 12: newer}[rid], run_id=11,
        jobs_fn=_jobs_fn(_jobs_all_success()), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.state == "CANCELLED" and verdict.run_id == 11
    assert verdict.verdict == cv.STATE_RED or verdict.verdict == cv.STATE_NOT_RUN
    assert verdict.verdict != cv.STATE_GREEN


def test_b2_a_pinned_run_id_whose_run_is_for_ANOTHER_sha_is_NO_RUN_never_a_verdict_on_this_one():
    other = _run("zzz", run_id=11, conclusion="success")

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([]), view_fn=lambda rid, *, repo_root: other,
        run_id=11, jobs_fn=_jobs_fn(_jobs_all_success()), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.state == "NO-RUN" and verdict.verdict == cv.STATE_NOT_RUN
    assert "zzz" in verdict.reason or "another" in verdict.reason


def test_b2_a_pinned_run_id_of_a_non_push_run_is_NO_RUN():
    pr = {**_run("abc", run_id=11), "event": "pull_request"}

    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([]), view_fn=lambda rid, *, repo_root: pr,
        run_id=11, jobs_fn=_jobs_fn(_jobs_all_success()), log_fn=_log_fn({}), sleep_fn=_no_sleep,
        required_contexts=_ALL_SIX)

    assert verdict.state == "NO-RUN"


def test_b2_a_NEW_red_on_a_required_pytest_leg_still_refuses():
    ids = ["tests/test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH"]

    verdict = _red_on_both_sides(ids + ["tests/test_new.py::test_new"], ids,
                                 registry=_empty_registry())

    assert verdict.state == "REGRESSED"
    assert any("tests/test_new.py::test_new" in r for r in verdict.new_reds)


def test_parse_suite_gate_block_WINDOW_ignores_a_shape_match_outside_the_real_step():
    """The defect Codex terra found (2026-09-24, HIGH): text shaped like the gate's own output,
    printed by ANOTHER step (pytest's own captured stdout can echo anything), must not be read
    as the verdict once a window scopes the read to the real step's own time range. Unscoped,
    the parser has no notion of "the real one" -- it keeps overwriting as it walks the log, so
    whichever matching line comes LAST wins; here that is a decoy that sorts after the real
    line, which is exactly why an unscoped read cannot be trusted."""
    real = _log_line_at("2026-09-24T00:05:00.0000000Z", "baseline sha   : c5108329")
    decoy = _log_line_at("2026-09-24T00:10:00.0000000Z", "baseline sha   : deadbeef00")
    log = "\n".join([_log_line_at("2026-09-24T00:05:00.0000000Z",
                                  "conductor suite-baseline gate"), real, decoy])
    window = (cv.datetime.fromisoformat("2026-09-24T00:04:00+00:00"),
             cv.datetime.fromisoformat("2026-09-24T00:06:00+00:00"))

    unscoped = cv.parse_suite_gate_block(log)
    scoped = cv.parse_suite_gate_block(log, window=window)

    assert unscoped["baseline_id"] == "deadbeef00", "unscoped, the LAST matching line wins -- the decoy, not the real one"
    assert scoped["baseline_id"] == "c5108329"


def test_step_window_reads_the_gate_steps_own_started_and_completed_PADDED_by_one_second():
    """Padded, not exact -- `steps[].startedAt`/`completedAt` carry second resolution while the
    log's own timestamps carry microseconds; a step that starts and ends within one reported
    second (measured live, 2026-09-24) would otherwise exclude its own output. See
    `_STEP_WINDOW_PAD`'s docstring."""
    job = {"steps": [{"name": "Sync the locked environment",
                      "startedAt": "2026-09-24T00:00:00Z", "completedAt": "2026-09-24T00:01:00Z"},
                     {"name": cv.SUITE_GATE_STEP_NAME,
                      "startedAt": "2026-09-24T00:05:00Z",
                      "completedAt": "2026-09-24T00:05:30Z"}]}

    window = cv._step_window(job, cv.SUITE_GATE_STEP_NAME)

    assert window is not None
    assert window[0].isoformat() == "2026-09-24T00:04:59+00:00"
    assert window[1].isoformat() == "2026-09-24T00:05:31+00:00"


def test_step_window_is_NONE_when_the_step_never_ran():
    job = {"steps": [{"name": "Sync the locked environment",
                      "startedAt": "2026-09-24T00:00:00Z", "completedAt": "2026-09-24T00:01:00Z"}]}

    assert cv._step_window(job, cv.SUITE_GATE_STEP_NAME) is None


# --- foundation-4-merge-gate, repair 2: the merge path's own log reader ----------------------

def test_repair2_fetch_job_log_reads_the_FULL_job_log_by_the_api_endpoint(monkeypatch, tmp_path):
    """`gh run view --job <id> --log` cuts the pytest step (0 FAILED lines on a 74-failure leg);
    `ci_verdict.fetch_job_log` is the merge path's reader (`merge_path verdict`), so it is
    the same defect as `actions_verdict._default_fetch_logs` and takes the same endpoint."""
    seen = []

    def fake_run(command, **kwargs):
        seen.append(list(command))
        return subprocess.CompletedProcess(command, 0, stdout="2026-10-04T01:00:00.0Z FAILED t", stderr="")

    monkeypatch.setattr(cv.subprocess, "run", fake_run)

    assert "FAILED t" in cv.fetch_job_log(7, 111333531317, repo_root=tmp_path)
    assert seen == [["gh", "api", "repos/{owner}/{repo}/actions/jobs/111333531317/logs"]]


def test_repair2_fetch_job_log_is_NONE_when_the_api_read_fails(monkeypatch, tmp_path):
    monkeypatch.setattr(cv.subprocess, "run", lambda command, **kw: subprocess.CompletedProcess(
        command, 1, stdout="", stderr="HTTP 404"))

    assert cv.fetch_job_log(7, 5, repo_root=tmp_path) is None


@pytest.mark.parametrize("blank", ["", "   \n"])
def test_repair2_fetch_job_log_is_NONE_for_a_blank_api_body_never_an_empty_string(
        monkeypatch, tmp_path, blank):
    monkeypatch.setattr(cv.subprocess, "run", lambda command, **kw: subprocess.CompletedProcess(
        command, 0, stdout=blank, stderr=""))

    assert cv.fetch_job_log(7, 5, repo_root=tmp_path) is None
