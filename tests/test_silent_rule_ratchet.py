"""Coverage for the [#436] silent-rule ratchet — scripts/silent_rule_detector.py plus the
`silent_rule_ratchet` ALL_CHECKS member in scripts/audit.py.

The four contract cases the build was gated on (operator-adopted D4 semantics, 2026-07-27)
are pinned here FIRST-CLASS and named accordingly:

    pass-at-baseline        test_pass_at_baseline
    fail-above-baseline     test_fail_above_baseline
    ratchet-down accepted   test_ratchet_down_accepted / test_transition_allows_drain
    baseline-raise rejected test_baseline_raise_rejected / test_transition_rejects_raise

Everything else here defends the detector contract itself: the metric is only meaningful
if the detector that produced the baseline is the detector producing the live count.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as aud
import silent_rule_detector as srd

REPO_ROOT = Path(__file__).resolve().parent.parent


def _measurement(count: int, detector_id: str = srd.DETECTOR_ID, files: int = 56):
    return srd.Measurement(detector_id=detector_id, count=count, files=files)


def _baseline(value: int, detector_id: str = srd.DETECTOR_ID) -> dict:
    return {"detector_id": detector_id, "baseline": value}


def _status(findings) -> str:
    assert len(findings) == 1, f"expected exactly one Finding, got {findings!r}"
    return findings[0].status


# ---------------------------------------------------------------------------
# The four contract cases
# ---------------------------------------------------------------------------

def test_pass_at_baseline():
    """CASE 1 — live count exactly equal to the committed baseline PASSES.

    Equality is the steady state: the pool has not grown. A gate that fired here would
    RED on its own first run, which is what the arm-time stop existed to prevent.
    """
    findings = aud._ratchet_findings(_measurement(428), _baseline(428))
    assert _status(findings) == "pass"
    assert "428" in findings[0].evidence


def test_fail_above_baseline():
    """CASE 2 — one candidate line above the baseline FAILS, and names both numbers."""
    findings = aud._ratchet_findings(_measurement(429), _baseline(428))
    assert _status(findings) == "fail"
    ev = findings[0].evidence
    assert "429" in ev and "428" in ev, f"evidence must name live and baseline: {ev}"


def test_ratchet_down_accepted():
    """CASE 3 — live BELOW the baseline passes: draining is the point, not a violation.

    The check must not demand exactness, or every drained rule would break the gate.
    """
    findings = aud._ratchet_findings(_measurement(400), _baseline(428))
    assert _status(findings) == "pass"


def test_baseline_raise_rejected():
    """CASE 4 — raising the committed baseline is rejected by the transition validator.

    This is the invariant that makes it a RATCHET rather than a high-water mark: the
    number may fall or hold, never rise. Enforced as a pure function so it is testable
    without a git history, and consumed by the check's git-previous leg.
    """
    reason = srd.validate_transition(old=428, new=500)
    assert reason is not None
    assert "428" in reason and "500" in reason
    assert "reject" in reason.lower()


# ---------------------------------------------------------------------------
# Transition validator — both directions, including the boundary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("old,new", [(428, 428), (428, 427), (428, 0)])
def test_transition_allows_drain(old, new):
    """Holding steady and lowering are both legal transitions."""
    assert srd.validate_transition(old=old, new=new) is None


@pytest.mark.parametrize("old,new", [(428, 429), (0, 1), (100, 1000)])
def test_transition_rejects_raise(old, new):
    """Any increase at all is rejected — there is no tolerance band."""
    assert srd.validate_transition(old=old, new=new) is not None


def test_no_baseline_raising_function_exists():
    """RATCHET-DOWN ONLY is a structural property, not a convention.

    The module must expose no callable that writes or raises a baseline. If someone adds
    one, this test names it — the escape hatch has to be a reviewed commit, never a code
    path that quietly re-arms the gate at a higher number.
    """
    forbidden = [n for n in dir(srd)
                 if any(tok in n.lower() for tok in ("write", "raise_", "set_baseline",
                                                     "update_baseline", "bump"))]
    assert forbidden == [], f"module exposes baseline-mutating callables: {forbidden}"


# ---------------------------------------------------------------------------
# Detector-contract defences
# ---------------------------------------------------------------------------

def test_detector_id_mismatch_fails_rather_than_comparing():
    """Two detectors' counts are not commensurable — comparing them is the failure mode
    the whole module exists to prevent, so a stamp mismatch FAILS loudly."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428, detector_id="silent-rule-v0"))
    assert _status(findings) == "fail"
    assert "silent-rule-v0" in findings[0].evidence


def test_absent_baseline_warns_and_does_not_pass_vacuously():
    """No baseline = inert gate. That must be visible, never a silent green."""
    findings = aud._ratchet_findings(_measurement(428), None)
    assert _status(findings) == "warn"


def test_malformed_baseline_value_fails():
    """A non-integer baseline is a corrupt gate, not a zero."""
    findings = aud._ratchet_findings(_measurement(428), {"detector_id": srd.DETECTOR_ID,
                                                         "baseline": "many"})
    assert _status(findings) == "fail"


def test_detector_catches_the_three_adjudicated_silent_rules():
    """The empirical basis for the token choice, pinned so a future 'tidy-up' cannot
    silently narrow it back to uppercase-only.

    These three lines are the rules the 2026-07-27 arm-time probe adjudicated as genuinely
    new-and-silent. An uppercase-anchored detector matched 0 of 3 — it would have been
    blind to the exact growth that stopped the build.
    """
    probes = [
        "**Never branch, commit, or merge under a live session.**",
        "`marketplace add` **must** precede `install`",
        "`.gitignore` floor negations **must use the contents form**",
    ]
    for line in probes:
        assert srd.TOKEN_RE.search(line), f"detector blind to a known silent rule: {line}"


def test_parity_surfaces_excluded_from_scope():
    """parity-surfaces.yaml rows are `tier:` ENUM VALUES read by fleet_parity — enforced
    by construction. In scope they were 120 of 148 candidate lines (81%), so the ratchet
    would have fired on ADDING ENFORCEMENT. Pinned because that is a subtle regression."""
    scoped = {p.relative_to(REPO_ROOT).as_posix() for p in srd.iter_scoped_files(REPO_ROOT)}
    assert "ecosystem/parity-surfaces.yaml" not in scoped


def test_baseline_file_excluded_from_its_own_scope():
    """The baseline lives in ecosystem/*.yaml; counting its own provenance prose would
    make the metric self-referential (and self-inflating on every re-stamp)."""
    scoped = {p.relative_to(REPO_ROOT).as_posix() for p in srd.iter_scoped_files(REPO_ROOT)}
    assert srd.BASELINE_RELPATH not in scoped


def test_archive_paths_excluded_from_scope():
    """Retiring doctrine into archive/ is a genuine drain, so archived files are out."""
    scoped = [p.relative_to(REPO_ROOT).as_posix() for p in srd.iter_scoped_files(REPO_ROOT)]
    assert not [r for r in scoped if "/archive/" in r or r.startswith("archive/")]


def test_measure_is_deterministic_and_sorted():
    """Two runs agree, and enumeration order is stable — a metric that wobbles between
    runs cannot gate anything."""
    first, second = srd.measure(REPO_ROOT), srd.measure(REPO_ROOT)
    assert first == second
    rels = [p.relative_to(REPO_ROOT).as_posix() for p in srd.iter_scoped_files(REPO_ROOT)]
    # Sorted on the CASEFOLDED relpath — see iter_scoped_files: ordering has to agree
    # across case-sensitive and case-insensitive filesystems.
    assert rels == sorted(rels, key=str.casefold)


def test_committed_baseline_matches_live_measurement():
    """The committed baseline must actually hold on the live repo — i.e. the gate is
    GREEN as shipped. This is the test that would have caught arming at 176."""
    doc = aud._load_silent_rule_baseline(REPO_ROOT)
    assert doc is not None, f"missing {srd.BASELINE_RELPATH}"
    assert doc["detector_id"] == srd.DETECTOR_ID
    live = srd.measure(REPO_ROOT)
    assert live.count <= doc["baseline"], (
        f"live {live.count} exceeds committed baseline {doc['baseline']}")


def test_check_registered_and_green_on_live_repo():
    """The check is in ALL_CHECKS (so it is a ship-gate leg by construction) and passes
    against the live hub."""
    assert aud.check_silent_rule_ratchet in aud.ALL_CHECKS
    findings = aud.check_silent_rule_ratchet(REPO_ROOT)
    assert _status(findings) == "pass"


# ---------------------------------------------------------------------------
# Regression cover for the five terra HIGH findings (2026-07-27). Each names the
# defect it pins so a later refactor cannot quietly reintroduce it.
# ---------------------------------------------------------------------------

def test_detector_failure_blocks_rather_than_shipping_green(monkeypatch):
    """terra HIGH — a measurement failure used to emit `unavailable`, which ship-gate does
    NOT block on (it blocks `fail` and undispositioned `warn` only). An unmeasured corpus
    would have shipped green. It must FAIL.

    Patches `aud._srd`, not the test's own `srd`: audit.py resolves the detector via
    `from scripts import silent_rule_detector`, which is a DIFFERENT module object from a
    bare `import silent_rule_detector` when both the repo root and scripts/ are on the
    path. Patching the wrong one silently no-ops and the test passes vacuously.
    """
    def boom(_root):
        raise UnicodeDecodeError("utf-8", b"", 0, 1, "simulated cp1252 corpus")

    monkeypatch.setattr(aud._srd, "measure", boom)
    findings = aud.check_silent_rule_ratchet(REPO_ROOT)
    assert _status(findings) == "fail", findings
    assert "could not measure" in findings[0].evidence


def test_raise_guard_reads_integration_target_not_head():
    """terra HIGH — the guard read HEAD, so once a raise was committed it compared the new
    baseline against itself and passed. It must read the integration target."""
    import inspect

    src = inspect.getsource(aud._previous_committed_baseline)
    assert "origin/main" in src or "_BASELINE_REFS" in src
    assert "HEAD:" not in src, "raise-guard must not compare the baseline against HEAD"
    assert aud._BASELINE_REFS[0] == "origin/main"


def test_bootstrap_raise_guard_is_surfaced_not_silent():
    """terra HIGH — when the previous value cannot be read the guard cannot run. In the
    BOOTSTRAP case (an integration ref resolves but carries no baseline yet) that is
    legitimate, but it must still be visible, or 'did not run' reads like 'passed'."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428),
                                     previous=None, ref_state="bootstrap")
    assert _status(findings) == "pass"
    assert "bootstrap" in findings[0].evidence


def test_unverifiable_raise_guard_blocks(monkeypatch):
    """terra HIGH RE-REVIEW — the first fix still passed (with a note) when NO integration
    ref resolved, and ship-gate ignores notes on a passing finding. A detached or ref-less
    checkout could therefore raise the baseline and ship green. That case must WARN, which
    ship-gate blocks on unless explicitly dispositioned."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(428),
                                     previous=None, ref_state="unknown")
    assert _status(findings) == "warn"
    assert "UNVERIFIABLE" in findings[0].evidence


def test_ref_state_distinguishes_bootstrap_from_unknown(tmp_path):
    """A non-git directory resolves no integration ref => 'unknown', never 'bootstrap'."""
    assert aud._baseline_ref_state(tmp_path) == "unknown"
    assert aud._baseline_ref_state(REPO_ROOT) == "bootstrap"


def test_raise_guard_fails_when_previous_is_lower():
    """The guard's positive case: a branch raising the committed baseline is blocked."""
    findings = aud._ratchet_findings(_measurement(428), _baseline(500), previous=428)
    assert _status(findings) == "fail"
    assert "reject" in findings[0].evidence.lower()


def test_metric_is_reflow_stable():
    """terra HIGH — a per-line count moves under pure reflow: joining two rule lines lowers
    it without removing a rule. Occurrence counting must be invariant under rewrapping."""
    joined = "A rule that must hold. Another that shall hold. A third that never yields."
    split = "A rule that must hold.\nAnother that shall hold.\nA third that never yields."
    assert len(srd.TOKEN_RE.findall(joined)) == len(srd.TOKEN_RE.findall(split)) == 3
    per_line_joined = sum(1 for ln in joined.splitlines() if srd.TOKEN_RE.search(ln))
    assert per_line_joined == 1, "per-line counting is the gameable unit v2 replaced"


def test_path_exclusions_are_case_insensitive(tmp_path):
    """terra HIGH — Windows can surface `templates/Archive/...` or a differently-cased
    excluded path; case-sensitive comparison would silently INCLUDE it, so the same tree
    would measure differently per platform."""
    (tmp_path / "protocols").mkdir()
    (tmp_path / "templates" / "Archive").mkdir(parents=True)
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "templates" / "Archive" / "old.md").write_text("must", encoding="utf-8")
    (tmp_path / "protocols" / "live.md").write_text("must", encoding="utf-8")
    rels = [p.relative_to(tmp_path).as_posix() for p in srd.iter_scoped_files(tmp_path)]
    assert "templates/Archive/old.md" not in rels, rels
    assert "protocols/live.md" in rels


def test_detector_id_bumped_for_v2_unit_change():
    """The contract says a unit change bumps the id. v1 counted lines, v2 counts
    occurrences — the ids must not be reused, or two incompatible metrics share a name."""
    assert srd.DETECTOR_ID == "silent-rule-v2"


def test_enumeration_is_case_insensitive_on_extensions(tmp_path):
    """terra HIGH RE-REVIEW — `Path.glob` inherits the platform's case sensitivity, so a
    `.MD` file counted on Windows and vanished on Linux: the same tree, two numbers.
    Enumeration now filters on a casefolded suffix explicitly."""
    (tmp_path / "protocols").mkdir()
    (tmp_path / "protocols" / "UPPER.MD").write_text("must", encoding="utf-8")
    (tmp_path / "protocols" / "lower.md").write_text("must", encoding="utf-8")
    rels = [p.relative_to(tmp_path).as_posix() for p in srd.iter_scoped_files(tmp_path)]
    assert rels == ["protocols/lower.md", "protocols/UPPER.MD"], rels
    assert srd.measure(tmp_path).count == 2


def test_ordering_is_total_under_casefold_collision(tmp_path):
    """Casefolding alone leaves paths differing only by case tied, so their order could
    swap between runs. A raw-relpath secondary key makes the sort total."""
    (tmp_path / "protocols").mkdir()
    for name in ("Alpha.md", "alpha.md", "ALPHA.md"):
        try:
            (tmp_path / "protocols" / name).write_text("must", encoding="utf-8")
        except OSError:                        # case-insensitive FS: fewer distinct files
            pass
    a = [p.relative_to(tmp_path).as_posix() for p in srd.iter_scoped_files(tmp_path)]
    b = [p.relative_to(tmp_path).as_posix() for p in srd.iter_scoped_files(tmp_path)]
    assert a == b == sorted(a, key=lambda r: (r.casefold(), r))
