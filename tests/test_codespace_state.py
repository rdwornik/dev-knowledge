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
