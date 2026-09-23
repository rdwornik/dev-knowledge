"""CI's verdict read as data (LANE-5A-6). Fixture runs for green, red and not-run.

Every `gh` call is injected (`list_fn`/`view_fn`/`jobs_fn`/`log_fn`) so these tests never shell
out and never sleep for real -- `sleep_fn`/`clock_fn` are fakes too, which is what lets the
IN-PROGRESS-then-completes and the timeout-while-waiting cases run in test time rather than
`POLL_TIMEOUT_S`.
"""
from __future__ import annotations

import json

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
    return {"databaseId": run_id, "headSha": sha, "status": status, "conclusion": conclusion,
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
    verdict = cv.verdict_for("ghost", repo_root=None, list_fn=_list_fn([]), sleep_fn=_no_sleep)

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
    clock = {"t": 0.0}
    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", status="in_progress")]),
        view_fn=lambda run_id, *, repo_root: _run("abc", status="in_progress"),
        timeout_s=10, interval_s=5, sleep_fn=lambda seconds: clock.__setitem__("t", clock["t"] + seconds),
        clock_fn=lambda: clock["t"])

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
    verdict = cv.verdict_for(
        "abc", repo_root=None, list_fn=_list_fn([_run("abc", status="in_progress")]),
        view_fn=view_fn, jobs_fn=_jobs_fn([{"name": "pytest", "conclusion": "success",
                                            "databaseId": 9}]),
        log_fn=_log_fn({9: _suite_gate_log("c5108329")}),
        sleep_fn=sleeps.append, timeout_s=1000, interval_s=5)

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
