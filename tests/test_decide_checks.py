"""scripts/decide_checks.py -- the /decide command's eight deterministic checks.

RED-FIRST (ADR-108 SS B): every check below is exercised against a synthetic fixture pair
(one clean, one carrying exactly the defect the check exists to catch) under
`tests/fixtures/decide/`, plus edge cases (byte cap, the excluded-roots fallback, the CLI's
exit codes) that do not need a fixture file at all.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import decide_checks as dc

_FIX = Path(__file__).resolve().parent / "fixtures" / "decide"
_REPO = Path(__file__).resolve().parents[1]


# --- check 1: paths resolve -------------------------------------------------------------------

def test_paths_resolve_is_clean_on_real_locators():
    assert dc.check_paths_resolve([_FIX / "paths_good.md"], repo_root=_REPO) == []


def test_paths_resolve_flags_a_stale_file_line_claim():
    defects = dc.check_paths_resolve([_FIX / "paths_bad.md"], repo_root=_REPO)
    assert len(defects) == 1
    assert defects[0].rule == "decide.paths_resolve"
    assert "does_not_exist_decide_fixture.py" in defects[0].detail


def test_paths_resolve_raises_on_a_missing_file():
    with pytest.raises(dc.DecideChecksError):
        dc.check_paths_resolve([_FIX / "no-such-file.md"], repo_root=_REPO)


# --- checks 2/3: the matrix --------------------------------------------------------------------

def test_matrix_recomputed_is_clean_on_a_correct_table():
    assert dc.check_matrix(_FIX / "matrix_good.md") == []


def test_matrix_recomputed_flags_a_wrong_declared_total():
    defects = dc.check_matrix(_FIX / "matrix_bad_total.md")
    assert len(defects) == 1
    assert defects[0].rule == "decide.matrix_recomputed"
    assert "declared" in defects[0].detail and "recomputed" in defects[0].detail


def test_matrix_weights_must_sum_to_100():
    defects = dc.check_matrix(_FIX / "matrix_bad_weights.md")
    assert len(defects) == 1
    assert defects[0].rule == "decide.matrix_weights"


def test_matrix_ignores_a_later_unrelated_table(tmp_path):
    # terra HIGH 2026-09-28: a second table below the matrix (a response table, say) must
    # never be read as more matrix rows.
    text = (_FIX / "matrix_good.md").read_text(encoding="utf-8") + (
        "\n## Unrelated later table\n\n"
        "| id | note |\n|---|---|\n| Z1 | this is not a matrix row |\n")
    fixture = tmp_path / "matrix_with_trailer.md"
    fixture.write_text(text, encoding="utf-8")
    assert dc.check_matrix(fixture) == []


def test_unmeasured_score_caps_at_3():
    defects = dc.check_matrix(_FIX / "matrix_bad_unmeasured.md")
    assert len(defects) == 4
    assert all(d.rule == "decide.unmeasured_cap" for d in defects)


def test_matrix_recomputed_tolerates_rounding_within_half_a_cent():
    # 3*25 + 1*20 + 1*20 + 2*10 + 3*10 + 1*15 = 180 -> 1.80 exactly; a declared 1.795 or 1.805
    # both round-trip within the 0.005 tolerance the check documents.
    text = (_FIX / "matrix_good.md").read_text(encoding="utf-8")
    tight = text.replace("| 1.80 |", "| 1.803 |", 1)
    fixture = _FIX / "matrix_good.md"
    tmp = fixture.parent / "_tmp_tight_matrix.md"
    tmp.write_text(tight, encoding="utf-8")
    try:
        defects = dc.check_matrix(tmp)
        assert not any(d.rule == "decide.matrix_recomputed" and "A1 today" in d.detail
                       for d in defects)
    finally:
        tmp.unlink()


# --- check 4: evaluator attestation -------------------------------------------------------------

def test_evaluator_attestation_is_clean_on_independent_evaluators():
    defects = dc.check_evaluator_attestation(
        [_FIX / "eval_codex_good.md", _FIX / "eval_copilot_good.md"],
        producer_model="claude-opus-5-5")
    assert defects == []


def test_evaluator_attestation_flags_the_producers_own_model():
    defects = dc.check_evaluator_attestation([_FIX / "eval_same_producer.md"],
                                             producer_model="claude-opus-5-5")
    assert len(defects) == 1
    assert defects[0].rule == "decide.evaluator_not_independent"


def test_evaluator_attestation_flags_missing_fields():
    defects = dc.check_evaluator_attestation([_FIX / "eval_missing_fields.md"],
                                             producer_model="claude-opus-5-5")
    assert any(d.rule == "decide.evaluator_attestation" for d in defects)


# --- check 5: response coverage -----------------------------------------------------------------

def test_response_coverage_is_clean_when_every_finding_has_one_row():
    defects = dc.check_response_coverage(
        [_FIX / "eval_codex_good.md", _FIX / "eval_copilot_good.md"],
        _FIX / "response_good.md")
    assert defects == []


def test_response_coverage_flags_a_finding_with_no_row():
    defects = dc.check_response_coverage(
        [_FIX / "eval_codex_good.md", _FIX / "eval_copilot_good.md"],
        _FIX / "response_missing.md")
    assert len(defects) == 1
    assert "P1" in defects[0].detail


def test_response_coverage_flags_two_distinct_findings_sharing_one_id(tmp_path):
    # terra HIGH 2026-09-28: a `set` used to silently collapse two distinct findings that
    # happen to share an id, letting one response row satisfy both.
    eval_a = tmp_path / "eval_a.md"
    eval_a.write_text("- id: C1 -- first objection\n", encoding="utf-8")
    eval_b = tmp_path / "eval_b.md"
    eval_b.write_text("- id: C1 -- a SECOND, unrelated objection sharing the same id\n",
                      encoding="utf-8")
    response = tmp_path / "response.md"
    response.write_text("| C1 | ... | **Accepted** -- ... |\n", encoding="utf-8")
    defects = dc.check_response_coverage([eval_a, eval_b], response)
    assert any(d.rule == "decide.duplicate_finding_id" and "C1" in d.detail for d in defects)


def test_response_coverage_flags_a_finding_answered_twice():
    defects = dc.check_response_coverage(
        [_FIX / "eval_codex_good.md", _FIX / "eval_copilot_good.md"],
        _FIX / "response_duplicate.md")
    ids = {d.detail.split()[1] for d in defects}
    assert "P1" in ids  # missing
    assert any("C1" in d.detail and "2 rows" in d.detail for d in defects)  # doubled


# --- check 6: ADR sections + size caps -----------------------------------------------------------

def test_adr_sections_is_clean_on_a_complete_draft():
    assert dc.check_adr_sections(_FIX / "adr_good.md") == []


def test_adr_sections_flags_a_missing_quality_attributes_section():
    defects = dc.check_adr_sections(_FIX / "adr_missing_qa.md")
    assert any(d.rule == "decide.adr_section" and "Quality attributes" in d.detail
              for d in defects)


def test_adr_sections_flags_an_incomplete_quality_attributes_section():
    defects = dc.check_adr_sections(_FIX / "adr_incomplete_qa.md")
    assert any("response measure" in d.detail for d in defects)
    assert not any("missing its 'quality attribute(s)'" in d.detail for d in defects)


def test_adr_sections_enforces_the_byte_cap(tmp_path):
    huge = tmp_path / "huge.md"
    huge.write_text("# huge\n\n" + ("x" * (dc.DECIDE_DOC_BYTE_CAP + 1)), encoding="utf-8")
    defects = dc.check_adr_sections(huge)
    assert any(d.rule == "decide.size_cap" for d in defects)


# --- check 7: subagent brief exclusions -----------------------------------------------------------

def test_subagent_brief_exclusions_is_clean_when_the_root_is_named():
    assert dc.check_subagent_brief_exclusions([_FIX / "brief_good.md"], repo_root=_REPO) == []


def test_subagent_brief_exclusions_flags_a_brief_missing_the_root():
    defects = dc.check_subagent_brief_exclusions([_FIX / "brief_bad.md"], repo_root=_REPO)
    assert len(defects) == 1
    assert "OneDrive - Blue Yonder" in defects[0].detail


def test_load_excluded_roots_falls_back_when_the_yaml_is_absent(tmp_path):
    roots, is_fallback = dc.load_excluded_roots(repo_root=tmp_path)
    assert is_fallback is True
    assert roots == list(dc._FALLBACK_EXCLUDED_ROOTS)


def test_load_excluded_roots_prefers_the_real_file_once_it_exists(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "excluded-roots.yaml").write_text(
        "roots:\n  - a-real-root\n", encoding="utf-8")
    roots, is_fallback = dc.load_excluded_roots(repo_root=tmp_path)
    assert is_fallback is False
    assert roots == ["a-real-root"]


# --- check 8: subagent claims spot-checked --------------------------------------------------------

def test_subagent_claims_is_clean_when_every_probe_passes_or_is_unverified():
    assert dc.check_subagent_claims(_FIX / "claims_good.md", repo_root=_REPO) == []


def test_subagent_claims_flags_a_failing_probe_and_an_unmarked_claim():
    defects = dc.check_subagent_claims(_FIX / "claims_bad.md", repo_root=_REPO)
    rules = [d.rule for d in defects]
    assert rules.count("decide.subagent_claim_probe_failed") == 2
    assert rules.count("decide.subagent_claim_unchecked") == 1


def test_subagent_claims_flags_a_missing_section():
    defects = dc.check_subagent_claims(_FIX / "claims_missing_section.md", repo_root=_REPO)
    assert len(defects) == 1
    assert defects[0].rule == "decide.subagent_claims"


def test_run_probe_path_line():
    ok, _ = dc._run_probe("scripts/decide_checks.py:1", _REPO)
    assert ok is True


def test_run_probe_unrecognised_syntax_is_never_a_silent_pass():
    ok, detail = dc._run_probe("something weird", _REPO)
    assert ok is False
    assert "unrecognised" in detail


def test_run_probe_refuses_a_path_line_probe_that_escapes_the_repo():
    ok, detail = dc._run_probe("../outside.txt:1", _REPO)
    assert ok is False
    assert "escapes" in detail


def test_run_probe_refuses_an_absolute_path_line_probe():
    ok, detail = dc._run_probe("/etc/passwd:1", _REPO)
    assert ok is False
    assert "escapes" in detail


def test_run_probe_refuses_a_grep_probe_that_escapes_the_repo():
    ok, detail = dc._run_probe("grep -c 'x' ../../outside.txt", _REPO)
    assert ok is False
    assert "escapes" in detail


def test_run_probe_rejects_line_zero_as_a_locator():
    ok, detail = dc._run_probe("scripts/decide_checks.py:0", _REPO)
    assert ok is False
    assert "not a valid" in detail


# --- CLI exit codes ------------------------------------------------------------------------------

def test_main_exits_0_on_a_clean_check():
    assert dc.main(["paths", str(_FIX / "paths_good.md"), "--repo-root", str(_REPO)]) == 0


def test_main_exits_1_on_a_defect():
    assert dc.main(["paths", str(_FIX / "paths_bad.md"), "--repo-root", str(_REPO)]) == 1


def test_main_exits_2_on_an_internal_error():
    assert dc.main(["paths", str(_FIX / "no-such-file.md"), "--repo-root", str(_REPO)]) == 2
