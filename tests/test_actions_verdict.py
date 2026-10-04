"""The integrator READS the Actions result, RED-first (`[#675]` target 3.2).

THE TARGET, verbatim from `[#675]`'s Done-when:

    (2) full suite and index regeneration on GitHub Actions, with the integrator READING the
    result -- not merely running there, because a green run nobody reads is not a gate

THE PREMISE IS WORSE THAN THE ROW STATES, and it was measured on 2026-09-12 rather than
assumed. The three most recent `conductor.yml` runs on `main` all concluded `failure`:

    ec18875e  failure   Merge branch 'docs/batch-x2-anchor'
    9136f133  failure   Merge branch 'docs/batch-x-integration'
    cec75ebc  failure   Merge branch 'docs/batch-x-teardown-record'

and job-level, the failing job is `pytest` while `ruff`, `seal`, `phase-gate` and `terra` pass.
Every one of those verdicts was printed at SessionStart, by `conductor.py session-start`, and
every merge proceeded. So the live state is not "a green run nobody reads" -- it is a RED run
nobody reads, which is the same defect with the loss already realised.

WHY THIS REPORTS A DIFFERENTIAL AND DOES NOT SIMPLY BLOCK. A gate that refuses any non-green
run would refuse every merge in this repo today, and a gate that refuses everything is turned
off in a window -- the failure mode `seat_refusals` names in its own contract. The honest
mechanism is to make the integrator read WHAT THIS MERGE CHANGED: a job failing at the baseline
is reported as pre-existing and named, a job this merge broke is a refusal. Neither is laundered
into a pass, which is the actual requirement.

NEVER GREEN-BY-SKIP, and it has three distinct absences rather than one. No run for the SHA, a
run still in progress, and `gh` unavailable are each their own verdict with their own exit
state. Collapsing them into "not green" would be as dishonest as collapsing them into "green":
the integrator needs to know whether to wait, to investigate, or to install something.
"""
from __future__ import annotations

import json
import subprocess

import pytest

import actions_verdict as av


# --- helpers ----------------------------------------------------------------

def _run(sha: str, conclusion: str, jobs: dict[str, str], *, status: str = "completed") -> dict:
    return {
        "databaseId": 1,
        "headSha": sha,
        "status": status,
        "conclusion": conclusion,
        "displayTitle": "a merge",
        "jobs": [{"name": name, "conclusion": c} for name, c in jobs.items()],
    }


def _gh(mapping: dict[str, dict | None]):
    """A fake `gh` that answers per SHA. `None` means 'no run for that SHA'."""
    def fetch(sha: str, *, repo_root=None, workflow=None):
        if sha not in mapping:
            raise av.ActionsUnavailable("gh is not installed or not authenticated")
        return mapping[sha]
    return fetch


# --- the target: the verdict is READ, per job -------------------------------

def test_a_green_run_passes_and_names_every_job_it_read():
    """Reading means reporting what was read. A gate that prints only PASS has not shown the
    integrator anything they could have disagreed with."""
    verdict = av.verdict_for("abc", fetch=_gh({"abc": _run("abc", "success",
                                                           {"pytest": "success",
                                                            "ruff": "success"})}))

    assert verdict.state == av.STATE_PASS
    assert verdict.ok is True
    assert set(verdict.jobs) == {"pytest", "ruff"}
    assert "pytest" in verdict.render() and "ruff" in verdict.render()


def test_a_job_THIS_MERGE_broke_is_a_REFUSAL_and_is_named():
    fetch = _gh({
        "tip": _run("tip", "failure", {"pytest": "success", "ruff": "failure"}),
        "base": _run("base", "success", {"pytest": "success", "ruff": "success"}),
    })

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state == av.STATE_REGRESSED
    assert verdict.ok is False
    assert verdict.newly_failing == ("ruff",)
    assert "ruff" in verdict.render()


def test_a_job_ALREADY_failing_at_the_baseline_is_reported_as_PRE_EXISTING_not_as_a_pass():
    """The measured live case. `pytest` has failed on `main` for at least three merges, so a
    merge that inherits it did not cause it -- and must not be credited with a green run
    either. Pre-existing is its own verdict, printed, with the job named.
    """
    # foundation-4 item 10: the job-level differential no longer applies to a PYTEST job -- a
    # pytest leg red at both ends is judged by node id (see the `test_G4_*` tests below, which
    # carry this case and its 424d6c72 sibling). The job-level behaviour this test pins is still
    # live for every other job, so it is stated on `ruff`.
    fetch = _gh({
        "tip": _run("tip", "failure", {"pytest (ubuntu-latest)": "success", "ruff": "failure"}),
        "base": _run("base", "failure", {"pytest (ubuntu-latest)": "success", "ruff": "failure"}),
    })

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.pre_existing == ("ruff",)
    assert verdict.newly_failing == ()
    assert "PRE-EXISTING" in verdict.render()
    assert "ruff" in verdict.render()


def test_a_merge_that_FIXES_a_failing_job_says_so_rather_than_staying_silent():
    """Reported for the same reason a regression is: the differential is the thing being read,
    and a silent improvement teaches the integrator that the tool only ever complains."""
    fetch = _gh({
        "tip": _run("tip", "success", {"pytest": "success"}),
        "base": _run("base", "failure", {"pytest": "failure"}),
    })

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state == av.STATE_PASS
    assert verdict.newly_passing == ("pytest",)
    assert "pytest" in verdict.render()


def test_WITHOUT_a_baseline_a_failure_is_UNATTRIBUTED_rather_than_blamed_on_this_merge():
    """No baseline is missing evidence, not evidence of innocence OR of guilt. Calling an
    unattributed failure a regression would make the tool cry wolf on this repo's standing RED;
    calling it pre-existing would launder a real break."""
    verdict = av.verdict_for("tip", fetch=_gh({"tip": _run("tip", "failure",
                                                           {"pytest": "failure"})}))

    assert verdict.state == av.STATE_UNATTRIBUTED
    assert verdict.ok is False
    assert "no baseline" in verdict.render().lower()


# --- never green-by-skip: three distinct absences ---------------------------

def test_NO_RUN_for_the_sha_is_its_own_verdict_and_is_never_a_pass():
    """The most dangerous absence: a merge pushed but Actions never fired, or fired on a
    different SHA. Nothing ran, so nothing passed."""
    verdict = av.verdict_for("ghost", fetch=_gh({"ghost": None}))

    assert verdict.state == av.STATE_NO_RUN
    assert verdict.ok is False
    rendered = verdict.render()
    assert av.STATE_NO_RUN in rendered
    assert "no Actions run exists" in rendered, "the absence is spelled out, not just coded"
    assert "PASS" not in rendered


def test_a_run_still_IN_PROGRESS_tells_the_integrator_to_WAIT_rather_than_to_investigate():
    verdict = av.verdict_for("tip", fetch=_gh({"tip": _run("tip", None, {"pytest": None},
                                                           status="in_progress")}))

    assert verdict.state == av.STATE_IN_PROGRESS
    assert verdict.ok is False
    assert "wait" in verdict.render().lower()


def test_gh_being_UNAVAILABLE_is_a_DIFFERENT_verdict_from_a_failing_run():
    """Install-something and investigate-something are different next actions, so they are
    different verdicts. This is the `[#675]` defect in miniature: one word for two states."""
    verdict = av.verdict_for("tip", fetch=_gh({}))

    assert verdict.state == av.STATE_UNAVAILABLE
    assert verdict.ok is False
    assert "gh" in verdict.render()


def test_the_four_NOT_GREEN_states_are_all_DISTINCT():
    """Asserted as a set so a later simplification that collapses two of them fails here."""
    states = {av.STATE_PASS, av.STATE_REGRESSED, av.STATE_PRE_EXISTING,
              av.STATE_UNATTRIBUTED, av.STATE_NO_RUN, av.STATE_IN_PROGRESS,
              av.STATE_UNAVAILABLE, av.STATE_JOBS_UNREADABLE}

    assert len(states) == 8


# --- the reading is RECORDED, which is what makes it a gate -----------------

def test_the_verdict_renders_the_RUN_URL_so_the_reading_can_be_checked_afterwards():
    """A recorded verdict nobody can re-open is a claim. The run id travels with it."""
    verdict = av.verdict_for("abc", fetch=_gh({"abc": _run("abc", "success",
                                                           {"pytest": "success"})}))

    assert "1" in verdict.render()


def test_the_verdict_is_JSON_SERIALISABLE_so_it_can_ride_the_merge_receipt():
    verdict = av.verdict_for("abc", fetch=_gh({"abc": _run("abc", "success",
                                                           {"pytest": "success"})}))

    round_tripped = json.loads(json.dumps(verdict.to_dict()))

    assert round_tripped["state"] == av.STATE_PASS
    assert round_tripped["sha"] == "abc"


def test_INDEX_REGENERATION_is_reported_as_NOT_COVERED_by_the_runner_today():
    """Target 3.2 asks for the full suite AND index regeneration on Actions. The suite is there
    (`conductor.yml`'s `pytest` job); index regeneration is NOT, and this names the gap rather
    than letting a green `pytest` read as though both halves ran.

    The gap is not closed here on purpose: `.github/workflows/conductor.yml` is `[#689]`'s
    declared footprint and this lane's is not, so writing it would be the exact collision
    `[#675]` target 3.4 exists to refuse -- measured with this lane's own
    `seat_refusals.declared_footprint`. A proposed diff rides in the end-of-lane artifact.
    """
    verdict = av.verdict_for("abc", fetch=_gh({"abc": _run("abc", "success",
                                                           {"pytest": "success",
                                                            "ruff": "success"})}))

    assert "index regeneration" in verdict.render().lower()
    assert av.INDEX_REGEN_JOB not in verdict.jobs


def test_a_runner_that_GAINS_the_index_job_stops_reporting_the_gap():
    """The gap notice retires itself when the gap closes, rather than becoming a stale line
    somebody has to remember to delete."""
    verdict = av.verdict_for("abc", fetch=_gh({"abc": _run(
        "abc", "success", {"pytest": "success", av.INDEX_REGEN_JOB: "success"})}))

    assert "index regeneration" not in verdict.render().lower()


# --- CLI --------------------------------------------------------------------

def test_the_cli_exits_NON_ZERO_on_every_not_green_state(monkeypatch):
    from click.testing import CliRunner

    monkeypatch.setattr(av, "fetch_run", _gh({"tip": _run("tip", "failure",
                                                          {"pytest": "failure"})}))
    result = CliRunner().invoke(av.cli, ["--sha", "tip"])

    assert result.exit_code != 0
    assert "pytest" in result.output


def test_the_cli_prints_the_verdict_even_when_it_PASSES(monkeypatch):
    """A gate that is silent on success has not been read; it has been assumed."""
    from click.testing import CliRunner

    monkeypatch.setattr(av, "fetch_run", _gh({"tip": _run("tip", "success",
                                                          {"pytest": "success"})}))
    result = CliRunner().invoke(av.cli, ["--sha", "tip"])

    assert result.exit_code == 0
    assert "pytest" in result.output


@pytest.mark.parametrize("state", [av.STATE_NO_RUN, av.STATE_IN_PROGRESS, av.STATE_UNAVAILABLE,
                                   av.STATE_JOBS_UNREADABLE])
def test_every_absence_state_carries_a_REMEDY_naming_the_next_action(state):
    """`SeatRefusal`'s rule, one organ over: a verdict that names no way forward gets worked
    around rather than acted on."""
    assert av.REMEDIES[state].strip(), state


# --- `[#742]`: AN UNREADABLE JOB LIST IS NOT AN EMPTY ONE -------------------
#
# RED-FIRST WITNESS (ADR-108 SB). At `dbac84b8`, `fetch_run`'s second `gh` call --
# `gh run view <id> --json jobs` -- collapsed EVERY failure mode onto `match["jobs"] = []`:
# a non-zero exit, an `OSError`, a `subprocess.TimeoutExpired` and malformed JSON all became
# "this run has no jobs". `verdict_for` then computed `failing = set()` over that empty list
# and returned `STATE_PASS`. An integrator who could not read the result at all was told the
# merge was green.
#
# The module already knew how to say "I could not read this": the FIRST `gh` call raises
# `ActionsUnavailable` on exactly these conditions. The second simply did not use it.
#
# THESE TESTS DRIVE THE REAL `fetch_run`, not an injected fake, and that is the point. The
# defect lives in `fetch_run`'s except branch, so a witness that stubbed `fetch` would test
# the fix's shape rather than the bug's absence. Stubbing `subprocess.run` puts the failure
# where the bug is, which means reintroducing `match["jobs"] = []` makes these RED again.

# `event: push` since foundation-4 item 11 (G7): `fetch_run` asks for push runs only and refuses a
# row that does not say it is one, so a real `gh run list --json ...,event` row carries it.
_RUN_ROW = {"databaseId": 7, "headSha": "abc0000dead", "status": "completed",
            "conclusion": "success", "displayTitle": "a merge", "event": "push"}


def _ok(command, payload: str) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(command, 0, payload, "")


def _gh_whose_JOB_call_fails(monkeypatch, failure):
    """`gh run list` answers; `gh run view --json jobs` fails the way `failure` says.

    Two calls, one failing -- the exact shape of the hole. The run itself is READABLE, so
    nothing upstream raises `ActionsUnavailable` and the verdict is reached with a job list
    that was never read.
    """
    def fake_run(command, **kwargs):
        if "list" in command:
            return _ok(command, json.dumps([_RUN_ROW]))
        return failure(command)
    monkeypatch.setattr(av.subprocess, "run", fake_run)


def _non_zero_exit(command):
    return subprocess.CompletedProcess(command, 1, "", "gh: HTTP 502 from api.github.com")


def _raises_oserror(command):
    raise OSError("gh is on the PATH and then it is not")


def _raises_timeout(command):
    raise subprocess.TimeoutExpired(command, av.GH_TIMEOUT_S)


def _malformed_json(command):
    return _ok(command, '{"jobs": [{"name": "pytest"')


_JOB_CALL_FAILURES = [
    pytest.param(_non_zero_exit, id="non-zero-exit"),
    pytest.param(_raises_oserror, id="OSError"),
    pytest.param(_raises_timeout, id="TimeoutExpired"),
    pytest.param(_malformed_json, id="malformed-JSON"),
]


@pytest.mark.parametrize("failure", _JOB_CALL_FAILURES)
def test_an_UNREADABLE_job_list_is_NEVER_a_PASS(monkeypatch, tmp_path, failure):
    """`[#742]`'s Done-when, first leg. Each of the four failure modes, asserted NOT to be
    `STATE_PASS` -- so the empty-list degradation cannot be reintroduced silently."""
    _gh_whose_JOB_call_fails(monkeypatch, failure)

    verdict = av.verdict_for("abc0000", repo_root=tmp_path)

    assert verdict.state != av.STATE_PASS
    assert verdict.ok is False


@pytest.mark.parametrize("failure", _JOB_CALL_FAILURES)
def test_an_unreadable_job_list_surfaces_as_its_OWN_state_not_as_a_failure(monkeypatch, tmp_path,
                                                                          failure):
    """Distinct from PASS *and* from FAIL. "The suite failed" and "I could not find out whether
    the suite failed" are different next actions, which is this module's founding rule."""
    _gh_whose_JOB_call_fails(monkeypatch, failure)

    verdict = av.verdict_for("abc0000", repo_root=tmp_path)

    assert verdict.state == av.STATE_JOBS_UNREADABLE
    assert verdict.state not in (av.STATE_PASS, av.STATE_REGRESSED, av.STATE_PRE_EXISTING)
    assert "could not be read" in verdict.render()


def test_a_run_with_GENUINELY_NO_JOBS_gets_a_DIFFERENT_answer_than_an_unreadable_one(monkeypatch,
                                                                                    tmp_path):
    """`[#742]`'s Done-when, third leg: "no failing jobs" and "no READABLE jobs" are two facts,
    and the whole hole was that one word stood for both. A job-less run is read successfully --
    it really has no jobs -- and keeps the answer it always had."""
    def job_less(command, **kwargs):
        if "list" in command:
            return _ok(command, json.dumps([_RUN_ROW]))
        return _ok(command, json.dumps({"jobs": []}))
    monkeypatch.setattr(av.subprocess, "run", job_less)
    job_less_verdict = av.verdict_for("abc0000", repo_root=tmp_path)

    _gh_whose_JOB_call_fails(monkeypatch, _non_zero_exit)
    unreadable_verdict = av.verdict_for("abc0000", repo_root=tmp_path)

    assert job_less_verdict.state != unreadable_verdict.state
    # foundation-4 item 11 (G7): a job-less run used to read PASS -- "no failing jobs". A pass now
    # needs a pytest leg that RAN and succeeded, so the job-less run reads NO-RUN with the reason
    # named. It is still a different fact from an unreadable list, which is what this test pins.
    assert job_less_verdict.state == av.STATE_NO_RUN
    assert "no pytest leg" in job_less_verdict.reason
    assert unreadable_verdict.state == av.STATE_JOBS_UNREADABLE


def test_an_unreadable_BASELINE_does_not_manufacture_a_REGRESSION():
    """THE SAME HOLE WITH THE SIGN FLIPPED, found while resolving `[#742]`'s locator and fixed
    with it because it is the same missing distinction.

    An unreadable baseline job list used to yield `base_jobs = {}` with `base_read = True`, so
    `base_failing` was empty and EVERY failing job at the tip was attributed to this merge --
    `STATE_REGRESSED`, naming jobs the merge may not have broken. A false accusation is as
    unusable as a false pass: the integrator reverts a merge that was innocent.
    """
    tip = _run("tip", "failure", {"pytest": "failure"})
    unreadable_base = {**_run("base", "failure", {}), "jobs": None}
    fetch = _gh({"tip": tip, "base": unreadable_base})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state != av.STATE_REGRESSED
    assert verdict.newly_failing == ()
    assert verdict.state == av.STATE_UNATTRIBUTED


def test_the_cli_exits_NON_ZERO_when_the_job_list_could_not_be_read(monkeypatch, tmp_path):
    """The gate's exit code is the only part of it a script reads."""
    from click.testing import CliRunner

    _gh_whose_JOB_call_fails(monkeypatch, _non_zero_exit)
    result = CliRunner().invoke(av.cli, ["--sha", "abc0000", "--repo-root", str(tmp_path)])

    assert result.exit_code != 0
    assert av.STATE_JOBS_UNREADABLE in result.output


# =====================================================================================
# foundation-4-merge-gate, item 10 (G4) and item 11 (G7): the TEST-LEVEL read.
#
# RED-first witnesses. Before this lane `verdict_for` classified a run by JOB NAME, so a NEW
# test red inside a pytest job that was already red read PRE-EXISTING -- the `424d6c72` cut
# merge turned `test_registered_check_never_fails_on_live_repo` red for 16 runs that way.
# =====================================================================================

import known_reds as kr  # noqa: E402

_LEG_U = "pytest (ubuntu-latest)"
_LEG_W = "pytest (windows-latest)"
_KNOWN = "tests/test_known.py::test_known_red"
_NEW = "tests/test_registered_check.py::test_registered_check_never_fails_on_live_repo"
_TS = "2026-10-02T10:00:00.0000000Z"


def _registry(*members, workers=4, by_os=None):
    return kr.Registry(
        schema=kr.SCHEMA, baseline_id="2026-10-01-reg", measured_at_sha="s", measured_via="ci",
        workers=workers, members={m: {"attribution": kr.PRE_FREEZE} for m in members},
        members_by_os=by_os or {})


def _gh_log(job: str, failures: dict, *, extra=()) -> str:
    """A `gh run view --job <id> --log` text: `<job>\\t<step>\\t<ts> <text>` per line."""
    lines = ["============ short test summary info ============"]
    lines += [f"FAILED {nid} - {reason}" for nid, reason in failures.items()]
    lines += list(extra)
    lines.append(f"===== {len(failures)} failed in 61.20s =====")
    return "\n".join(f"{job}\tRun the suite\t{_TS} {line}" for line in lines)


def _run_with_logs(sha, conclusion, jobs, *, status="completed", event="push"):
    """`jobs` = {name: conclusion}; every job gets a databaseId so its log can be fetched."""
    return {"databaseId": 7, "headSha": sha, "status": status, "conclusion": conclusion,
            "displayTitle": "a merge", "event": event,
            "jobs": [{"name": n, "conclusion": c, "databaseId": 100 + i}
                     for i, (n, c) in enumerate(jobs.items())]}


def _logs(per_sha_job: dict):
    """A fake `fetch_logs(run, job)`: `{(sha, job name): text | None}`."""
    def fetch_logs(run, job, *, repo_root=None):
        return per_sha_job.get((run["headSha"], job["name"]))
    return fetch_logs


def _registry_loader(registry):
    return lambda ref, *, repo_root=None: registry


def test_G4_a_NEW_red_inside_an_ALREADY_red_pytest_leg_is_REGRESSED_not_PRE_EXISTING():
    """THE 424d6c72 REPLAY. Base: the pytest leg fails {KNOWN}. Tip: the same leg fails {KNOWN,
    NEW}. Job name says 'failing at both' -> the old read said PRE-EXISTING."""
    fetch = _gh({
        "tip": _run_with_logs("tip", "failure", {_LEG_U: "failure", "ruff": "success"}),
        "base": _run_with_logs("base", "failure", {_LEG_U: "failure", "ruff": "success"}),
    })
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: k", _NEW: "KeyError"}),
                  ("base", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: k"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_REGRESSED
    assert any(_NEW in t for t in verdict.new_tests)
    assert not verdict.ok
    assert _NEW in verdict.render()


def test_G4_the_same_failures_with_the_same_signatures_are_PRE_EXISTING_and_COMPLETE():
    fetch = _gh({
        "tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
        "base": _run_with_logs("base", "failure", {_LEG_U: "failure"}),
    })
    both = _gh_log(_LEG_U, {_KNOWN: "AssertionError: k"})
    logs = _logs({("tip", _LEG_U): both, ("base", _LEG_U): both})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.new_tests == () and verdict.signature_changed == ()
    assert verdict.ok is False, "PRE-EXISTING is never a pass"


def test_G4_a_known_id_failing_with_a_CHANGED_signature_is_FLAGGED_not_refused():
    """Red on both sides, failing differently now. b2-merge-gate (R64): FLAGGED by name -- it was
    REGRESSED at foundation-4, which made the gate refuse a clean merge on a red main."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "KeyError: 'x'"}),
                  ("base", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: k"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_PRE_EXISTING
    assert any(_KNOWN in t for t in verdict.signature_changed)
    assert any(kr.BUCKET_SIGNATURE_CHANGED in f and _KNOWN in f for f in verdict.flagged)
    assert verdict.new_tests == ()


def test_G4_a_base_failure_ABSENT_from_the_registry_is_flagged_never_a_silent_baseline():
    """Red on both sides but nobody registered it: a regression that reached main must not become
    the baseline just because it is red there (D5(b)) -- it is NAMED in the verdict and owes a
    registry entry or a row, but it does not refuse a merge that did not introduce it (R64)."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})
    both = _gh_log(_LEG_U, {_NEW: "KeyError"})
    logs = _logs({("tip", _LEG_U): both, ("base", _LEG_U): both})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.new_tests == ()
    assert any(_NEW in f and kr.BUCKET_UNREGISTERED in f for f in verdict.flagged)
    assert verdict.ok is False, "flagged is landable, never green"


def test_G4_each_OS_leg_is_compared_against_ITS_OWN_base_leg():
    """The Windows leg fails {KNOWN} at base and tip; the Ubuntu leg was green at base and fails
    {NEW} at the tip. A per-run comparison would blur the two."""
    fetch = _gh({
        "tip": _run_with_logs("tip", "failure", {_LEG_U: "failure", _LEG_W: "failure"}),
        "base": _run_with_logs("base", "failure", {_LEG_U: "success", _LEG_W: "failure"}),
    })
    green_base = f"{_LEG_U}	Run the suite	{_TS} ===== 9211 passed in 61.20s ====="
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_NEW: "KeyError"}),
                  ("base", _LEG_U): green_base,
                  ("tip", _LEG_W): _gh_log(_LEG_W, {_KNOWN: "AssertionError: k"}),
                  ("base", _LEG_W): _gh_log(_LEG_W, {_KNOWN: "AssertionError: k"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_REGRESSED
    assert [t for t in verdict.new_tests if _LEG_U in t and _NEW in t]
    assert not [t for t in verdict.new_tests if _LEG_W in t]


@pytest.mark.parametrize("conclusion", ["cancelled", "timed_out"])
def test_G4_a_pytest_job_that_never_finished_is_a_REGRESSION_not_a_known_red(conclusion):
    """A job timeout / cancel carries no node id to compare; it is a regression, never an id-less
    'nothing new failed'."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: conclusion}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})
    logs = _logs({("tip", _LEG_U): None,
                  ("base", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: k"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_REGRESSED
    assert any(_LEG_U in n and conclusion in n for n in verdict.non_test)


def test_G4_a_FAILED_leg_with_no_node_id_in_its_log_is_a_REGRESSION():
    """xdist crash / a step before pytest / a collection abort: the leg is red and names no test."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "success", {_LEG_U: "success"})})
    log = "\n".join(f"{_LEG_U}\tRun the suite\t{_TS} {t}" for t in
                    ("worker 'gw3' crashed while running 'tests/x.py::t'", "INTERNALERROR> boom"))

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             fetch_logs=_logs({("tip", _LEG_U): log}),
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_REGRESSED
    assert any(_LEG_U in n for n in verdict.non_test)


def test_G4_an_unreadable_registry_is_UNATTRIBUTED_so_a_lane_cannot_launder_by_registering():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})
    both = _gh_log(_LEG_U, {_KNOWN: "AssertionError: k"})

    def broken_loader(ref, *, repo_root=None):
        raise kr.KnownRedsError("no registry at base")

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             fetch_logs=_logs({("tip", _LEG_U): both, ("base", _LEG_U): both}),
                             registry_loader=broken_loader)

    assert verdict.state == av.STATE_UNATTRIBUTED
    assert "registry" in verdict.reason


def test_G4_an_unreadable_LOG_is_UNATTRIBUTED_never_pre_existing():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=_logs({}),
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_UNATTRIBUTED
    assert "log" in verdict.reason


def test_G4_non_pytest_jobs_keep_the_job_level_differential():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {"ruff": "failure"}),
                 "base": _run_with_logs("base", "failure", {"ruff": "failure"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=_logs({}),
                             registry_loader=_registry_loader(_registry()))

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.pre_existing == ("ruff",)


# --- G7: a run that is not completed-and-successful is never a pass -------------------------

def test_G7_a_run_still_IN_PROGRESS_is_IN_PROGRESS_and_never_ok():
    fetch = _gh({"tip": _run_with_logs("tip", None, {_LEG_U: None}, status="in_progress")})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state == av.STATE_IN_PROGRESS and verdict.ok is False


def test_G7_a_CANCELLED_run_is_its_own_state_and_never_ok():
    """`cancel-in-progress` cancels the older run when a newer push lands. Its jobs may read
    success/skipped; the run is still not a verdict on anything."""
    fetch = _gh({"tip": _run_with_logs("tip", "cancelled", {_LEG_U: "success", "ruff": "success"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state == av.STATE_CANCELLED and verdict.ok is False
    assert av.REMEDIES[av.STATE_CANCELLED]


def test_G7_a_pass_needs_every_pytest_leg_to_have_run():
    """A completed `success` run whose pytest legs are absent is not a pass on the suite."""
    fetch = _gh({"tip": _run_with_logs("tip", "success", {"ruff": "success"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state != av.STATE_PASS
    assert verdict.ok is False


def test_G7_gh_UNAVAILABLE_is_never_ok():
    verdict = av.verdict_for("tip", baseline="base", fetch=_gh({}))
    assert verdict.state == av.STATE_UNAVAILABLE and verdict.ok is False


def test_G7_fetch_run_asks_gh_for_PUSH_runs_only(monkeypatch, tmp_path):
    """A `pull_request`/`workflow_dispatch` run for the same sha is not the push run the ruleset's
    check-runs belong to."""
    seen = []

    def fake_run(command, **kwargs):
        seen.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="[]", stderr="")

    monkeypatch.setattr(av.subprocess, "run", fake_run)

    assert av.fetch_run("abc1234", repo_root=tmp_path) is None
    assert "--event" in seen[0] and seen[0][seen[0].index("--event") + 1] == "push"


def test_G7_a_non_push_run_is_never_chosen(monkeypatch, tmp_path):
    listing = json.dumps([
        {"databaseId": 1, "headSha": "abc1234", "status": "completed", "conclusion": "success",
         "displayTitle": "pr run", "event": "pull_request", "createdAt": "2026-10-02T10:00:00Z"}])

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 0, stdout=listing, stderr="")

    monkeypatch.setattr(av.subprocess, "run", fake_run)

    assert av.fetch_run("abc1234", repo_root=tmp_path) is None


# =====================================================================================
# foundation-4-merge-gate, repair 2: the DEFAULT log fetcher reads the FULL job log.
#
# `gh run view <run> --job <id> --log` (gh 2.93.0) cut the pytest step of job 111333531317 to 550
# lines: 1151 lines, 0 `FAILED tests/` lines, no "short test summary". The full log, by
# `gh api repos/{owner}/{repo}/actions/jobs/<id>/logs`, is 3538 lines with 74 `FAILED tests/`
# lines. Every fixture above feeds a synthetic log through `fetch_logs=`, so none of them could
# see it: a red-but-pre-existing pytest leg read "names no failing test node id" -> REGRESSED.
# =====================================================================================

_JOB_LOG_API = "repos/{owner}/{repo}/actions/jobs/"


def _api_log(failures: dict) -> str:
    """The `gh api .../actions/jobs/<id>/logs` shape: `<ts> <text>`, no job/step columns."""
    lines = ["============ short test summary info ============"]
    lines += [f"FAILED {nid} - {reason}" for nid, reason in failures.items()]
    lines.append(f"===== {len(failures)} failed in 61.20s =====")
    return "\n".join(f"{_TS} {line}" for line in lines)


def _truncated_gh_log() -> str:
    """What `gh run view --job <id> --log` returned for a red leg: the step is cut before pytest's
    summary, so there is no FAILED line and no 'short test summary'."""
    body = ["Run uv run --locked python scripts/conductor.py suite", "collected 8870 items",
            "tests/test_a.py ....F...", "tests/test_b.py ...F..."]
    return "\n".join(f"pytest (ubuntu-latest)\tRun the suite\t{_TS} {line}" for line in body)


def _fake_gh(monkeypatch, *, api_text="", api_rc=0, view_text=None):
    """Replace `av.subprocess.run` with a `gh` that answers like the real one, and record every
    command. `gh run view --log` returns the TRUNCATED text; `gh api` returns the full one."""
    seen: list = []

    def fake_run(command, **kwargs):
        seen.append(list(command))
        if command[:2] == ["gh", "api"]:
            return subprocess.CompletedProcess(command, api_rc, stdout=api_text, stderr="")
        if command[:3] == ["gh", "run", "view"] and "--log" in command:
            return subprocess.CompletedProcess(
                command, 0, stdout=view_text if view_text is not None else _truncated_gh_log(),
                stderr="")
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="unexpected")

    monkeypatch.setattr(av.subprocess, "run", fake_run)
    return seen


def test_repair2_the_default_fetcher_reads_the_FULL_job_log_by_the_api_endpoint(
        monkeypatch, tmp_path):
    seen = _fake_gh(monkeypatch, api_text=_api_log({_KNOWN: "AssertionError: k"}))

    text = av._default_fetch_logs({"databaseId": 7}, {"databaseId": 111333531317, "name": _LEG_U},
                                  repo_root=tmp_path)

    assert text is not None and f"FAILED {_KNOWN}" in text
    assert seen == [["gh", "api", f"{_JOB_LOG_API}111333531317/logs"]]
    assert not any("--log" in c for c in seen), "`gh run view --log` truncates the pytest step"


@pytest.mark.parametrize("rc,text", [(1, "boom"), (0, ""), (0, "   \n")])
def test_repair2_the_default_fetcher_keeps_NONE_WHEN_UNREADABLE_never_an_empty_string(
        monkeypatch, tmp_path, rc, text):
    _fake_gh(monkeypatch, api_text=text, api_rc=rc)

    assert av._default_fetch_logs({"databaseId": 7}, {"databaseId": 5, "name": _LEG_U},
                                  repo_root=tmp_path) is None


def test_repair2_a_gh_that_cannot_run_is_NONE_not_a_raise(monkeypatch, tmp_path):
    def boom(command, **kwargs):
        raise OSError("gh not found")

    monkeypatch.setattr(av.subprocess, "run", boom)

    assert av._default_fetch_logs({"databaseId": 7}, {"databaseId": 5, "name": _LEG_U},
                                  repo_root=tmp_path) is None


def test_repair2_a_job_without_an_id_is_NONE(monkeypatch, tmp_path):
    seen = _fake_gh(monkeypatch)

    assert av._default_fetch_logs({"databaseId": 7}, {"name": _LEG_U}, repo_root=tmp_path) is None
    assert seen == []


def test_repair2_a_red_but_pre_existing_leg_read_through_the_DEFAULT_fetcher_is_PRE_EXISTING(
        monkeypatch, tmp_path):
    """The live shape, end to end: no `fetch_logs=` override, so the production fetcher runs
    against a `gh` whose `run view --log` is truncated and whose `api` is full."""
    _fake_gh(monkeypatch, api_text=_api_log({_KNOWN: "AssertionError: k"}))
    fetch = _gh({
        "tip": _run_with_logs("tip", "failure", {_LEG_U: "failure", "ruff": "success"}),
        "base": _run_with_logs("base", "failure", {_LEG_U: "failure", "ruff": "success"}),
    })

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, repo_root=tmp_path,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_PRE_EXISTING, verdict.render()
    assert verdict.non_test == () and verdict.new_tests == ()


def test_repair2_the_truncated_shape_alone_is_still_read_as_no_node_id_so_the_fix_is_the_FETCH(
        monkeypatch, tmp_path):
    """Pins that the PARSER stays fail-closed: a log with no FAILED line is not 'nothing failed'.
    What changes is which text the default fetcher hands it."""
    _fake_gh(monkeypatch, api_text="", api_rc=1)           # the API is down; only the cut text exists
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, repo_root=tmp_path,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state != av.STATE_PRE_EXISTING and verdict.state != av.STATE_PASS


# =====================================================================================
# b2-merge-gate (R64; architect seat rulings of 2026-10-04): the gate REFUSES only what a merge
# introduces -- a test red on the merge and green on the base -- and every non-pass state of a
# required check. A red on BOTH sides is FLAGGED into the verdict (and so the receipt) by bucket.
# RED-first: at `2dd2067d` every case in the first block below read REGRESSED, and the
# `required_contexts` block had no state of its own for `skipped` / `timed_out`.
# =====================================================================================

def test_b2_only_red_on_both_sides_reads_PRE_EXISTING_and_prints_its_flagged_buckets():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure", _LEG_W: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure", _LEG_W: "failure"})})
    both = _gh_log(_LEG_U, {_KNOWN: "AssertionError: k", _NEW: "KeyError"})
    both_w = _gh_log(_LEG_W, {_KNOWN: "AssertionError: k", _NEW: "KeyError"})
    logs = _logs({("tip", _LEG_U): both, ("base", _LEG_U): both,
                  ("tip", _LEG_W): both_w, ("base", _LEG_W): both_w})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_PRE_EXISTING, verdict.render()
    assert verdict.new_tests == () and verdict.ok is False
    assert len(verdict.flagged) == 2, "one flagged line per leg"
    text = verdict.render()
    assert "FLAGGED" in text and f"[{kr.BUCKET_UNREGISTERED}]" in text and _NEW in text
    assert kr.UNREGISTERED_OWES in text
    assert verdict.to_dict()["flagged"] == list(verdict.flagged)


def test_b2_a_NEW_red_still_refuses_and_only_the_new_one_is_named_as_new():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})
    unreg = "tests/other.py::t_unregistered"
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: k", unreg: "E",
                                                    _NEW: "KeyError"}),
                  ("base", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: k", unreg: "E"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_REGRESSED
    assert [t for t in verdict.new_tests] == [f"{_LEG_U}: {_NEW}"]
    assert any(unreg in f for f in verdict.flagged)


def test_b2_the_registered_flaky_sibling_swap_is_flagged_on_its_own_leg():
    """Windows base failed flaky test A; the tip fails flaky test B of the same file instead."""
    flaky_a = "tests/test_graph_spine.py::test_an_expired_lock_is_broken"
    flaky_b = "tests/test_graph_spine.py::test_an_overrun_builder_does_not_release_its_SUCCESSORS_lock"
    registry = _registry(_KNOWN, by_os={"windows-latest": {
        n: {"attribution": kr.FLAKY} for n in (flaky_a, flaky_b)}})
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_W: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_W: "failure"})})
    logs = _logs({("tip", _LEG_W): _gh_log(_LEG_W, {_KNOWN: "AssertionError: k", flaky_b: "E"}),
                  ("base", _LEG_W): _gh_log(_LEG_W, {_KNOWN: "AssertionError: k", flaky_a: "E"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(registry))

    assert verdict.state == av.STATE_PRE_EXISTING, verdict.render()
    assert any(kr.BUCKET_FLAKY_SWAP in f and flaky_b in f for f in verdict.flagged)
    assert verdict.new_tests == ()


def test_b2_a_per_merge_value_in_a_signature_is_not_a_changed_signature():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "failure", {_LEG_U: "failure"})})
    logs = _logs({
        ("tip", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: assert {'2026-10-04-...erge-gate.md'} == set()"}),
        ("base", _LEG_U): _gh_log(_LEG_U, {_KNOWN: "AssertionError: assert {'2026-10-04-...-approved.md'} == set()"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry(_KNOWN)))

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.signature_changed == () and verdict.flagged == ()


# --- every non-pass state of a REQUIRED check is its own refusing state ----------------------

def _six(**over):
    jobs = {c: "success" for c in av.REQUIRED_CONTEXTS}
    jobs.update(over)
    return jobs


@pytest.mark.parametrize("conclusion,state", [
    ("skipped", av.STATE_SKIPPED), ("timed_out", av.STATE_TIMED_OUT),
    ("cancelled", av.STATE_CANCELLED), (None, av.STATE_IN_PROGRESS)])
def test_b2_each_non_pass_required_context_is_its_OWN_refusing_state(conclusion, state):
    fetch = _gh({"tip": _run_with_logs("tip", "failure", _six(**{"ruff": conclusion}))})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             required_contexts=av.REQUIRED_CONTEXTS)

    assert verdict.state == state and verdict.ok is False
    assert verdict.non_pass == (f"ruff: {conclusion or 'in-progress'}",)
    assert av.REMEDIES[state]
    assert "ruff" in verdict.render()


def test_b2_a_required_context_that_never_ran_is_NO_RUN_and_names_the_context():
    jobs = _six()
    del jobs["spine"]
    fetch = _gh({"tip": _run_with_logs("tip", "success", jobs)})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             required_contexts=av.REQUIRED_CONTEXTS)

    assert verdict.state == av.STATE_NO_RUN and verdict.ok is False
    assert verdict.non_pass == ("spine: not-run",)


def test_b2_the_non_pass_states_are_distinct_from_each_other_and_from_a_pass():
    states = {av.STATE_SKIPPED, av.STATE_TIMED_OUT, av.STATE_CANCELLED, av.STATE_IN_PROGRESS,
              av.STATE_NO_RUN}
    assert len(states) == 5 and av.STATE_PASS not in states


def test_b2_a_required_context_timed_out_on_BOTH_sides_is_not_laundered_into_PRE_EXISTING():
    """The job-level differential read a non-pytest job that failed at both ends as PRE-EXISTING;
    `timed_out` is not a failure of a test, it is a check that did not finish."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", _six(ruff="timed_out")),
                 "base": _run_with_logs("base", "failure", _six(ruff="timed_out"))})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             required_contexts=av.REQUIRED_CONTEXTS)

    assert verdict.state == av.STATE_TIMED_OUT


def test_b2_a_required_context_that_FAILED_is_judged_by_the_differential_not_refused_here():
    """`failure` is the one non-success a required context may show and still be landable: it is
    judged test by test (pytest legs) or job by job (the rest) against the base."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", _six(ruff="failure")),
                 "base": _run_with_logs("base", "failure", _six(ruff="failure"))})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             required_contexts=av.REQUIRED_CONTEXTS)

    assert verdict.state == av.STATE_PRE_EXISTING and verdict.non_pass == ()


def test_b2_a_run_that_TIMED_OUT_at_the_run_level_is_its_own_state():
    fetch = _gh({"tip": _run_with_logs("tip", "timed_out", _six())})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             required_contexts=av.REQUIRED_CONTEXTS)

    assert verdict.state == av.STATE_TIMED_OUT and verdict.ok is False


# =====================================================================================
# b2-merge-gate repair 1: a base leg that concludes `success` can still carry red tests.
#
# `main`'s ubuntu leg runs the raw pytest step `continue-on-error: true` and is judged by the
# known-reds compare, so it concludes `success` while 73 tests are red. `_judge_pytest_legs` used
# to read the base log only for a non-success base leg, so the base set was empty and every tip
# red read NEW (merge `5f82efaa`, run 37216985245 vs base 37177553087: 75 "new" reds, REGRESSED).
# =====================================================================================

_PRE_A = "tests/test_pre.py::test_pre_red_a"
_PRE_B = "tests/test_pre.py::test_pre_red_b"


def test_B2R1_a_base_leg_that_concludes_SUCCESS_but_logs_failing_ids_does_not_make_them_NEW():
    """RED-first. Base leg `success` with {PRE_A, PRE_B} red in its log; the tip leg `failure`
    with the same two. Nothing is red on the merge and green on the base -> PRE-EXISTING."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure", "ruff": "success"}),
                 "base": _run_with_logs("base", "success", {_LEG_U: "success", "ruff": "success"})})
    both = _gh_log(_LEG_U, {_PRE_A: "AssertionError: a", _PRE_B: "AssertionError: b"})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch,
                             fetch_logs=_logs({("tip", _LEG_U): both, ("base", _LEG_U): both}),
                             registry_loader=_registry_loader(_registry()))

    assert verdict.new_tests == ()
    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.flagged, "the red-on-both-sides ids must still be FLAGGED with their bucket"


def test_B2R1_a_NEW_red_still_refuses_against_a_SUCCESS_base_leg_that_logs_other_reds():
    """The refusal class is unchanged: red on the merge, green on the base."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "success", {_LEG_U: "success"})})
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_PRE_A: "AssertionError: a", _NEW: "boom"}),
                  ("base", _LEG_U): _gh_log(_LEG_U, {_PRE_A: "AssertionError: a"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry()))

    assert verdict.state == av.STATE_REGRESSED
    assert [n for n in verdict.new_tests if _NEW in n] and not [n for n in verdict.new_tests if _PRE_A in n]


def test_B2R1_a_SUCCESS_base_leg_with_NO_failing_ids_still_lets_a_new_tip_red_refuse():
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "success", {_LEG_U: "success"})})
    clean_base = f"{_LEG_U}\tRun the suite\t{_TS} ===== 9211 passed in 61.20s ====="
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_NEW: "boom"}), ("base", _LEG_U): clean_base})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry()))

    assert verdict.state == av.STATE_REGRESSED
    assert any(_NEW in n for n in verdict.new_tests)


def test_B2R1_an_unreadable_log_of_a_SUCCESS_base_leg_is_UNATTRIBUTED_never_an_empty_base():
    """An unreadable base log is missing evidence, not a base with no reds."""
    fetch = _gh({"tip": _run_with_logs("tip", "failure", {_LEG_U: "failure"}),
                 "base": _run_with_logs("base", "success", {_LEG_U: "success"})})
    logs = _logs({("tip", _LEG_U): _gh_log(_LEG_U, {_PRE_A: "AssertionError: a"})})

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch, fetch_logs=logs,
                             registry_loader=_registry_loader(_registry()))

    assert verdict.state == av.STATE_UNATTRIBUTED
    assert verdict.new_tests == ()
