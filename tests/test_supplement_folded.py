"""Tests for audit.py::check_supplement_folded — R4 of the 2026-08-26 handoff census.

THE DEFECT, measured rather than supposed. The supplement is filled AFTER the paste is
assembled, and until this check nothing re-folded it. 63 bundles carry a filled SUPPLEMENT
ANSWERS region alongside an assembled PASTE_THIS.md; 62 folded, and the ONE that did not is
the most recent architect handoff before the census —
`docs/handoffs/2026-08-23-dev-knowledge-architect/`, whose SUPPLEMENT.md carries 87 answer
lines while its PASTE_THIS.md carries four sections and no `=== SUPPLEMENT.md ===`. The
outgoing architect's rulings, rejections, off-repo context and Q7 register did not reach the
next seat, and nobody found out — silent, irreplaceable loss.

The predicate is deliberately reusable (`supplement_fold_violations`) so the RED can be
reproduced against the REAL bundle on disk, not only against a fixture.
"""
from __future__ import annotations

from pathlib import Path

import audit as aud  # noqa: E402

_REPO = Path(__file__).resolve().parents[1]

_FILLED_SUPPLEMENT = (
    "# Supplement\n\n"
    "## Q1\nwhat changed?\n\n"
    "<!-- PASTE CHAT ANSWERS BELOW THIS LINE -->\n"
    "A1. The register is the durable home; the transient is not.\n"
)
_COLD_SUPPLEMENT = (
    "# Supplement\n\n"
    "## Q1\nwhat changed?\n\n"
    "<!-- PASTE CHAT ANSWERS BELOW THIS LINE -->\n"
    "<!-- (operator: paste the outgoing chat's answers here) -->\n"
)
_PASTE_WITHOUT = "=== RESIDUAL.md ===\n\nbody\n\n---\n\n=== PROBES.md ===\n\nbody\n"
_PASTE_WITH = _PASTE_WITHOUT + "\n---\n\n=== SUPPLEMENT.md ===\n\nA1. …\n"


def _bundle(tmp_path, name, *, supplement=None, paste=None):
    b = tmp_path / "docs" / "handoffs" / name
    b.mkdir(parents=True)
    if supplement is not None:
        (b / "SUPPLEMENT.md").write_text(supplement, encoding="utf-8")
    if paste is not None:
        (b / "PASTE_THIS.md").write_text(paste, encoding="utf-8")
    return tmp_path


# --- the predicate ----------------------------------------------------------

def test_predicate_reds_against_the_real_2026_08_23_bundle():
    """THE contract test (census R4): the check must reproduce RED against the one live
    instance. Run against the REAL repo, so this is evidence about the tree and not about a
    fixture — and it is why the predicate is separable from the era-gated adapter below."""
    names = [b for b, _ in aud.supplement_fold_violations(_REPO)]
    assert "2026-08-23-dev-knowledge-architect" in names


def test_predicate_finds_only_that_one_instance_in_the_live_corpus():
    """Measured 2026-08-26: 63 filled-with-a-paste bundles, exactly one unfolded. A second
    name appearing here is either a new defect or a regression in the predicate — either way
    it is worth failing over rather than absorbing."""
    names = sorted(b for b, _ in aud.supplement_fold_violations(_REPO))
    assert names == ["2026-08-23-dev-knowledge-architect"]


def test_predicate_flags_filled_supplement_with_unfolded_paste(tmp_path):
    repo = _bundle(tmp_path, "2026-09-01-x",
                   supplement=_FILLED_SUPPLEMENT, paste=_PASTE_WITHOUT)
    assert [b for b, _ in aud.supplement_fold_violations(repo)] == ["2026-09-01-x"]


def test_predicate_clean_when_the_paste_carries_the_section(tmp_path):
    repo = _bundle(tmp_path, "2026-09-01-x",
                   supplement=_FILLED_SUPPLEMENT, paste=_PASTE_WITH)
    assert aud.supplement_fold_violations(repo) == []


def test_predicate_ignores_a_cold_supplement(tmp_path):
    """An UNFILLED supplement is an honest record of a duty undischarged, not a fold failure —
    and folding an empty ANSWERS region is exactly what assemble_paste declines to do."""
    repo = _bundle(tmp_path, "2026-09-01-x",
                   supplement=_COLD_SUPPLEMENT, paste=_PASTE_WITHOUT)
    assert aud.supplement_fold_violations(repo) == []


def test_predicate_ignores_a_bundle_with_no_assembled_paste(tmp_path):
    """No PASTE_THIS.md means nothing was ever assembled — there is no fold to have missed."""
    repo = _bundle(tmp_path, "2026-09-01-x", supplement=_FILLED_SUPPLEMENT)
    assert aud.supplement_fold_violations(repo) == []


def test_predicate_skips_excluded_bundle_dirs(tmp_path):
    """archive / aborted / in-progress are not live bundles (the _BUNDLE_EXCLUDE_DIRS set
    every other bundle-walking check already honours)."""
    repo = _bundle(tmp_path, "aborted", supplement=_FILLED_SUPPLEMENT, paste=_PASTE_WITHOUT)
    assert aud.supplement_fold_violations(repo) == []


# --- the ALL_CHECKS adapter -------------------------------------------------

def test_check_is_fail_class_for_an_in_era_bundle(tmp_path):
    repo = _bundle(tmp_path, "2026-09-01-x",
                   supplement=_FILLED_SUPPLEMENT, paste=_PASTE_WITHOUT)
    findings = aud.check_supplement_folded(repo)
    assert [f.status for f in findings] == ["fail"]
    assert "2026-09-01-x" in findings[0].evidence
    assert "|" not in findings[0].evidence


def test_check_grandfathers_a_pre_era_bundle_without_blocking(tmp_path):
    """IMMUTABLE-AND-LOST, recorded rather than repaired. The 2026-08-23 loss already
    happened: the seat that needed those answers booted on 2026-08-25 without them, and
    rewriting a sealed bundle's paste now would edit an immutable artifact (Critical Rule #3)
    to falsify what was actually delivered. So a pre-era violation is NAMED in the evidence —
    visible, permanent, un-suppressed — and does not block."""
    repo = _bundle(tmp_path, "2026-08-23-x",
                   supplement=_FILLED_SUPPLEMENT, paste=_PASTE_WITHOUT)
    findings = aud.check_supplement_folded(repo)
    assert [f.status for f in findings] == ["pass"]
    assert "2026-08-23-x" in findings[0].evidence
    assert "immutable-and-lost" in findings[0].evidence


def test_check_passes_cleanly_with_no_violations(tmp_path):
    repo = _bundle(tmp_path, "2026-09-01-x",
                   supplement=_FILLED_SUPPLEMENT, paste=_PASTE_WITH)
    findings = aud.check_supplement_folded(repo)
    assert [f.status for f in findings] == ["pass"]


def test_check_is_not_applicable_without_a_handoffs_dir(tmp_path):
    findings = aud.check_supplement_folded(tmp_path)
    assert findings[0].status == "n/a"


def test_check_is_registered_in_all_checks():
    assert aud.check_supplement_folded in aud.ALL_CHECKS


def test_check_is_green_on_the_live_repo():
    """The live tree: the single violation is pre-era, so the deployed gate passes while
    still naming it. A NEW unfolded bundle would FAIL here."""
    findings = aud.check_supplement_folded(_REPO)
    assert [f.status for f in findings] == ["pass"]
    assert "2026-08-23-dev-knowledge-architect" in findings[0].evidence
