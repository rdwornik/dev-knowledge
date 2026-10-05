"""RED-first witnesses for `scripts/codespace_state.py` — the recovery-container discriminator.

WHY THIS TEST EXISTS BEFORE THE CODE (ADR-108 §B). The defect being closed is that a recovery
container is EXTERNALLY INDISTINGUISHABLE from ours: GitHub's documented `state` enum has no
value for it, no API field reports it, and it is reachable and reports a live state throughout
(`DIGEST-2026-09-15-codespaces-reference.md` §b, §g). For a month the symptom was treated instead
of the cause — the dispatcher's exit-91 guard catches "claude is not installed in this
devcontainer", which is what a recovery container LOOKS like downstream while naming the wrong
thing entirely.

THE MARKERS ARE MEASURED, NOT INVENTED, and that is the whole reason this module can exist. They
come from this repo's own creation log on the operator's probe codespace `lane-z-substrate-probe`
(created 2026-09-14 23:36Z), read at
`/workspaces/.codespaces/.persistedshare/creation.log` and recorded verbatim in the [#746]
amendment. A classifier built on strings someone expected the platform to emit would be a
decoration; these are strings the platform DID emit, here, on the container that died.
"""
from __future__ import annotations

import pytest

import codespace_state as cs


# The measured creation-log tail from the 2026-09-14 recovery event ([#746] amendment).
MEASURED_RECOVERY_LOG = """\
[2026-09-14 23:37:11.882Z] Running the postCreateCommand from devcontainer.json...
python: can't open file '/workspaces/dev-knowledge/scripts/cloud_provisioning.py': [Errno 2] No such file or directory
[provision] REFUSED: B1 the history guard could not look (exit 2)
[2026-09-14 23:37:14.201Z] postCreateCommand failed with exit code 1.
Container creation failed.
Creating recovery container.
"""

MEASURED_HEALTHY_LOG = """\
[2026-09-15 08:02:41.100Z] Running the onCreateCommand from devcontainer.json...
[provision] provisioning /workspaces/dev-knowledge
[provision] L1 uv 0.11.19 == pin
[provision] DONE — 7 leg(s) acted; all four legs assert clean and a real gate ran here
[2026-09-15 08:04:02.884Z] Finished configuring codespace.
"""


class TestCreationLogVerdict:
    """The discriminator itself: creation-log text in, a named verdict out."""

    def test_measured_recovery_log_is_named_recovery_container(self):
        """The 2026-09-14 log must classify as RECOVERY_CONTAINER, by that name."""
        verdict = cs.classify_creation_log(MEASURED_RECOVERY_LOG)
        assert verdict.verdict is cs.ContainerVerdict.RECOVERY_CONTAINER
        # The point of the module is that it names the CAUSE, not the downstream symptom.
        assert "recovery" in verdict.reason.lower()

    def test_recovery_verdict_quotes_the_line_it_fired_on(self):
        """Evidence, not assertion — the caller gets the matched line back to print."""
        verdict = cs.classify_creation_log(MEASURED_RECOVERY_LOG)
        assert any("Creating recovery container." in line for line in verdict.evidence)

    def test_healthy_log_is_not_a_recovery_container(self):
        verdict = cs.classify_creation_log(MEASURED_HEALTHY_LOG)
        assert verdict.verdict is cs.ContainerVerdict.OURS

    def test_lifecycle_failure_without_recovery_line_is_its_own_verdict(self):
        """A failed hook is not yet a recovery container; conflating them loses information."""
        log = (
            "[2026-09-14 23:37:14.201Z] postCreateCommand failed with exit code 1.\n"
            "Container creation failed.\n"
        )
        verdict = cs.classify_creation_log(log)
        assert verdict.verdict is cs.ContainerVerdict.CREATION_FAILED

    def test_empty_log_is_indeterminate_never_ours(self):
        """An absent log is not evidence of health. This is the vacuous-gate refusal."""
        verdict = cs.classify_creation_log("")
        assert verdict.verdict is cs.ContainerVerdict.INDETERMINATE

    def test_whitespace_only_log_is_indeterminate(self):
        assert cs.classify_creation_log("   \n  \n").verdict is cs.ContainerVerdict.INDETERMINATE


class TestTripLeg:
    """The trip-test leg: prove the organ REFUSES when neutered.

    `ecosystem/quality-requirements.yaml` refuses a trip-test that passes unconditionally
    (`tests/test_quality_requirements.py`), so the register's `trip_test` for the
    recovery-discriminator entry points here: emptying the marker table must make the measured
    recovery log stop being detected.
    """

    def test_emptying_the_marker_table_stops_detection(self, monkeypatch):
        monkeypatch.setattr(cs, "RECOVERY_MARKERS", ())
        verdict = cs.classify_creation_log(MEASURED_RECOVERY_LOG)
        assert verdict.verdict is not cs.ContainerVerdict.RECOVERY_CONTAINER

    def test_every_marker_carries_its_provenance(self):
        """A marker with no provenance is a guess wearing a measurement's clothes."""
        assert cs.RECOVERY_MARKERS, "the marker table must not be empty in the shipped organ"
        for marker in cs.RECOVERY_MARKERS:
            assert marker.provenance, f"{marker.text!r} carries no provenance"
            assert marker.provenance in cs.PROVENANCE_VALUES


class TestLaneStateCross:
    """alive / working / finished / died / timed-out, as a pure cross of two inputs.

    Deliberately a PURE FUNCTION over (container_state, progress_age_s) and not a poller: which
    mechanism supplies those two inputs — outside polling, inside push, or both — is intake #102's
    open architectural question and is not decided here.
    """

    @pytest.mark.parametrize(
        "container_state,progress_age_s,expected",
        [
            ("Available", 5, cs.LaneState.WORKING),
            ("Available", 99_999, cs.LaneState.HUNG),
            ("Shutdown", 99_999, cs.LaneState.DIED),
            ("Failed", 10, cs.LaneState.DIED),
            ("Provisioning", None, cs.LaneState.STARTING),
        ],
    )
    def test_cross(self, container_state, progress_age_s, expected):
        assert cs.classify_lane(container_state, progress_age_s, stale_after_s=900) is expected

    def test_available_with_no_progress_signal_is_not_working(self):
        """`Available` means the machine is up, not that anything is running (docs, §g).

        Reporting WORKING on the strength of the platform state alone is precisely the false
        green that let two detached lanes produce zero work unnoticed.
        """
        assert cs.classify_lane("Available", None, stale_after_s=900) is not cs.LaneState.WORKING

    def test_finished_is_only_reachable_with_an_explicit_completion(self):
        assert cs.classify_lane("Available", 5, stale_after_s=900, completed=True) is cs.LaneState.FINISHED


# ============================================================================================
# b2-codespace-green (item 3, item 5; R63, R65): the classifier reads the substrate as it is
# ============================================================================================

import json  # noqa: E402
import subprocess  # noqa: E402


class _Run:
    """A `runner` stand-in: records argv and keyword arguments, answers from a table."""

    def __init__(self, returncode=0, stdout="", stderr="", raises=None):
        self.calls: list[tuple[list[str], dict]] = []
        self.returncode, self.stdout, self.stderr, self.raises = returncode, stdout, stderr, raises

    def __call__(self, argv, **kw):
        self.calls.append((list(argv), kw))
        if self.raises is not None:
            raise self.raises
        return subprocess.CompletedProcess(argv, self.returncode, stdout=self.stdout,
                                           stderr=self.stderr)


class TestCreationLogOverSsh:
    """D3: `gh codespace logs` answered `Permission denied (publickey,password)` and hung on a
    recovery container; `gh codespace ssh -- cat <creation.log>` worked."""

    def test_the_creation_log_is_read_over_ssh_cat_not_gh_codespace_logs(self):
        run = _Run(stdout=MEASURED_HEALTHY_LOG)
        text = cs.fetch_creation_log("night-cs-1", runner=run)
        argv, _ = run.calls[0]
        assert argv[:7] == ["gh", "codespace", "ssh", "-c", "night-cs-1", "--", "cat"]
        assert argv[7] == "/workspaces/.codespaces/.persistedshare/creation.log"
        assert "logs" not in argv
        assert text == MEASURED_HEALTHY_LOG

    def test_the_read_carries_a_timeout_so_a_hung_recovery_container_cannot_block(self):
        run = _Run(stdout="")
        cs.fetch_creation_log("x", runner=run)
        assert run.calls[0][1].get("timeout"), "no timeout: the 300 s hang of the night"

    def test_a_timed_out_read_is_an_empty_log_which_classifies_indeterminate_never_ours(self):
        run = _Run(raises=subprocess.TimeoutExpired(cmd="gh", timeout=1))
        text = cs.fetch_creation_log("x", runner=run)
        assert text == ""
        assert cs.classify_creation_log(text).verdict is cs.ContainerVerdict.INDETERMINATE

    def test_a_failed_read_is_an_empty_log(self):
        run = _Run(returncode=255, stdout="", stderr="Permission denied (publickey,password)")
        assert cs.fetch_creation_log("x", runner=run) == ""


class TestAbsentIsNotUnknown:
    """D4: `fetch_view` of a deleted Codespace is `{}`, which read `unknown`."""

    def test_a_listing_that_succeeds_without_the_name_is_absent(self):
        run = _Run(stdout=json.dumps([{"name": "other", "state": "Available"}]))
        assert cs.fetch_state("gone-cs", runner=run) == cs.ABSENT_STATE

    def test_a_listing_that_has_the_name_returns_its_state(self):
        run = _Run(stdout=json.dumps([{"name": "live-cs", "state": "Available"}]))
        assert cs.fetch_state("live-cs", runner=run) == "Available"

    def test_a_listing_that_failed_says_nothing_about_absence(self):
        """'could not look' is not 'gone' (the same rule `verify-cleanup` applies)."""
        assert cs.fetch_state("x", runner=_Run(returncode=1, stdout="")) is None
        assert cs.fetch_state("x", runner=_Run(stdout="not json")) is None

    def test_classify_lane_reads_absent_as_absent_not_unknown(self):
        assert cs.classify_lane(cs.ABSENT_STATE, None) is cs.LaneState.ABSENT
        assert cs.classify_lane(None, None) is cs.LaneState.UNKNOWN


def _reading(**over):
    base = dict(reachable=True, age_s=10.0, runner_alive=True, receipt_present=False, error="")
    base.update(over)
    return cs.ProgressReading(**base)


class TestProgressSignal:
    """D4 / N5: the signal is the run log's age read over ssh from the REMOTE clock, with the
    runner's own heartbeat saying whether the runner process still lives."""

    def test_the_probe_output_parses_into_ages_on_the_remote_clock(self):
        r = cs.parse_progress("now=1000 log=900 hb=990 receipt=0\n")
        assert r.reachable and r.age_s == 100.0 and r.runner_alive is True
        assert r.receipt_present is False

    def test_a_missing_run_log_has_no_progress_age_never_a_zero(self):
        r = cs.parse_progress("now=1000 log=- hb=- receipt=0\n")
        assert r.reachable and r.age_s is None and r.runner_alive is False

    def test_a_receipt_is_the_completion_signal(self):
        assert cs.parse_progress("now=1000 log=900 hb=- receipt=1\n").receipt_present is True

    @pytest.mark.parametrize("text", ["", "garbage", "now=x log=1 hb=1 receipt=0"])
    def test_an_unreadable_answer_is_unreachable_not_progress(self, text):
        r = cs.parse_progress(text)
        assert not r.reachable and r.age_s is None

    def test_the_probe_runs_over_ssh_with_a_timeout(self):
        run = _Run(stdout="now=5 log=4 hb=4 receipt=0\n")
        r = cs.fetch_progress("cs-1", "/workspaces/dispatch", runner=run)
        argv, kw = run.calls[0]
        assert argv[:6] == ["gh", "codespace", "ssh", "-c", "cs-1", "--"]
        assert "/workspaces/dispatch/run.log" in " ".join(argv)
        assert kw.get("timeout")
        assert r.reachable and r.age_s == 1.0

    def test_a_probe_that_times_out_or_fails_is_unreachable(self):
        for run in (_Run(raises=subprocess.TimeoutExpired(cmd="gh", timeout=1)),
                    _Run(returncode=255, stderr="connection reset")):
            r = cs.fetch_progress("cs-1", "/w", runner=run)
            assert not r.reachable and r.error


class TestFates:
    """N5: every observed lane state has a stated fate; a stalled or disconnected lane is FAILED
    with its reason and the step that failed, never `unknown` with no fate."""

    def test_the_bounds_are_stated_constants(self):
        assert cs.STALE_AFTER_S == 900.0 and cs.DISCONNECT_AFTER_S == 300.0

    def test_a_live_lane_with_fresh_progress_is_working_and_running(self):
        a = cs.assess_lane("Available", _reading(age_s=20))
        assert a.state is cs.LaneState.WORKING and a.fate == "RUNNING"

    def test_a_stalled_lane_is_hung_and_failed_with_reason_and_step(self):
        """RED on cd3ab8a6: there is no `assess_lane`; `classify_lane` alone returned UNKNOWN when
        nothing supplied progress and had no fate to attach."""
        a = cs.assess_lane("Available", _reading(age_s=901))
        assert a.state is cs.LaneState.HUNG and a.fate == "FAILED" and a.step == "run"
        assert "901" in a.reason and "900" in a.reason

    def test_a_lane_just_inside_the_bound_is_still_working(self):
        assert cs.assess_lane("Available", _reading(age_s=900)).state is cs.LaneState.WORKING

    def test_a_dead_runner_without_a_receipt_is_died_not_hung(self):
        a = cs.assess_lane("Available", _reading(age_s=5000, runner_alive=False))
        assert a.state is cs.LaneState.DIED and a.fate == "FAILED" and a.step == "run"

    def test_a_disconnected_lane_is_detected_within_the_bound(self):
        unreachable = _reading(reachable=False, age_s=None, runner_alive=None, error="ssh 255")
        early = cs.assess_lane("Available", unreachable, unreachable_for_s=299)
        assert early.state is cs.LaneState.UNKNOWN and early.fate == "WAITING"
        late = cs.assess_lane("Available", unreachable, unreachable_for_s=300)
        assert late.state is cs.LaneState.DISCONNECTED and late.fate == "FAILED"
        assert late.step == "observe" and "300" in late.reason

    def test_no_reading_at_all_is_waiting_on_a_named_gate_never_working(self):
        a = cs.assess_lane("Available", None)
        assert a.state is cs.LaneState.UNKNOWN and a.fate == "WAITING" and a.reason

    def test_a_receipt_is_a_handback_not_a_working_lane(self):
        a = cs.assess_lane("Available", _reading(age_s=1, receipt_present=True))
        assert a.state is cs.LaneState.FINISHED and a.fate == "HANDBACK"

    def test_a_deleted_codespace_is_torn_down_when_this_line_deleted_it(self):
        a = cs.assess_lane(cs.ABSENT_STATE, None, expected_gone=True)
        assert a.state is cs.LaneState.ABSENT and a.fate == "TORN-DOWN"

    def test_a_vanished_codespace_nobody_deleted_is_failed(self):
        a = cs.assess_lane(cs.ABSENT_STATE, None, expected_gone=False)
        assert a.state is cs.LaneState.ABSENT and a.fate == "FAILED"

    def test_a_shut_down_box_is_failed_at_the_run_step(self):
        a = cs.assess_lane("Shutdown", None)
        assert a.state is cs.LaneState.DIED and a.fate == "FAILED" and a.step == "run"

    def test_a_starting_box_is_running(self):
        assert cs.assess_lane("Provisioning", None).fate == "RUNNING"

    def test_every_state_has_a_fate_in_the_closed_set(self):
        for st in ("Available", "Shutdown", "Provisioning", cs.ABSENT_STATE, None, "Weird"):
            for rd in (None, _reading(), _reading(age_s=99999),
                       _reading(reachable=False, age_s=None)):
                a = cs.assess_lane(st, rd, unreachable_for_s=999)
                assert a.fate in cs.FATES and a.reason
