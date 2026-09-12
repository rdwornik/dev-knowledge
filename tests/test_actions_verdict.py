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
    fetch = _gh({
        "tip": _run("tip", "failure", {"pytest": "failure", "ruff": "success"}),
        "base": _run("base", "failure", {"pytest": "failure", "ruff": "success"}),
    })

    verdict = av.verdict_for("tip", baseline="base", fetch=fetch)

    assert verdict.state == av.STATE_PRE_EXISTING
    assert verdict.pre_existing == ("pytest",)
    assert verdict.newly_failing == ()
    assert "PRE-EXISTING" in verdict.render()
    assert "pytest" in verdict.render()


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
              av.STATE_UNAVAILABLE}

    assert len(states) == 7


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


@pytest.mark.parametrize("state", [av.STATE_NO_RUN, av.STATE_IN_PROGRESS, av.STATE_UNAVAILABLE])
def test_every_absence_state_carries_a_REMEDY_naming_the_next_action(state):
    """`SeatRefusal`'s rule, one organ over: a verdict that names no way forward gets worked
    around rather than acted on."""
    assert av.REMEDIES[state].strip(), state
