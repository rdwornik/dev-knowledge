"""Tests for the satellite onboarding-profile rulings register + its advisory checker.

Two layers:
  1. THE SHIPPED REGISTER (ecosystem/satellite-onboarding-rulings.yaml) is well-formed
     and encodes the four operator rulings exactly — all four `full`, and life-architect
     carries the override block naming BOTH sides (census floor-only -> operator full).
     This is the "machine-checkable" leg of the arc closure.
  2. THE CHECKER'S SCHEMA TEETH — synthetic fixtures prove a malformed register is caught
     (exit 1) and an unusable one is refused (exit 2), so the advisory checker can never
     render a broken contract green. Fixtures are synthesized so the suite does not couple
     to the live register's lifecycle.
"""
from __future__ import annotations


from click.testing import CliRunner


import validate_onboarding_rulings as vor  # noqa: E402


# --- layer 1: the shipped register --------------------------------------------

def _shipped() -> dict:
    return vor.load_register(vor.DEFAULT_REGISTER)


def test_shipped_register_is_well_formed():
    assert vor.schema_defects(_shipped()) == []


# The 2026-07-16 operator batch. Pinned as a SUBSET rather than the whole register since
# 2026-08-26: the register is a live decision log, so a later ruling by a different party on
# a different date is growth, not drift, and an equality pin would make every admission a
# test edit. What must not drift is that these four still say exactly what the operator ruled.
_OPERATOR_BATCH_2026_07_16 = frozenset({
    "corp-ops", "corp-sca-time-automation", "life-architect", "demo-prep"})


def test_shipped_register_encodes_the_four_operator_rulings():
    rulings = _shipped()["rulings"]
    assert _OPERATOR_BATCH_2026_07_16 <= set(rulings)
    # operator ruled ALL FOUR full (life-architect overriding the census floor-only).
    for name in _OPERATOR_BATCH_2026_07_16:
        e = rulings[name]
        assert e["profile"] == "full"
        assert e["ruled_by"] == "operator"
        assert e["ruled_date"] == "2026-07-16"
        assert e["census_ref"]


def test_every_ruling_names_a_profile_a_ruler_and_its_proposing_surface():
    """The invariant that outlives any one batch — every entry, not just the first four."""
    for name, e in _shipped()["rulings"].items():
        assert e["profile"] in {"full", "floor-only"}, name
        assert e["ruled_by"], name
        assert e["census_ref"], name


def test_life_architect_override_names_both_sides():
    la = _shipped()["rulings"]["life-architect"]
    ov = la["override"]
    assert ov["proposed"] == "floor-only"      # census
    assert ov["ruled"] == "full"               # operator
    assert ov["proposed"] != ov["ruled"]
    assert ov["ruled_reason"]                  # the "why" is recorded


def test_shipped_register_cli_is_green():
    res = CliRunner().invoke(vor.main, [])     # default path = the shipped register
    assert res.exit_code == 0
    assert "[onboarding-rulings]" in res.output
    # Every shipped ruling to date is `full`, so the digest's full-count IS the entry count —
    # asserted against the live register rather than a literal, which would pin the surface
    # line to one moment in the register's life (it read "4 full" until win-tooling joined).
    n = len(_shipped()["rulings"])
    assert f"{n} satellite(s) ruled: {n} full, 0 floor-only" in res.output
    assert "life-architect" in res.output      # the override is surfaced


# --- layer 2: checker schema teeth --------------------------------------------

_GOOD_ENTRY = (
    "    profile: full\n"
    "    ruled_by: operator\n"
    "    ruled_date: 2026-07-16\n"
    "    census_ref: docs/audits/x.md\n"
)


def _write(tmp_path, body: str):
    p = tmp_path / "reg.yaml"
    p.write_text("version: 1\nrulings:\n" + body, encoding="utf-8")
    return p


def test_missing_ruled_by_is_a_defect(tmp_path):
    p = _write(tmp_path, "  corp-ops:\n    profile: full\n    ruled_date: 2026-07-16\n"
                         "    census_ref: x\n")
    res = CliRunner().invoke(vor.main, ["--path", str(p)])
    assert res.exit_code == 1
    assert "missing ruled_by" in res.output


def test_bad_date_is_a_defect(tmp_path):
    p = _write(tmp_path, "  corp-ops:\n    profile: full\n    ruled_by: operator\n"
                         "    ruled_date: 20260716\n    census_ref: x\n")
    res = CliRunner().invoke(vor.main, ["--path", str(p)])
    assert res.exit_code == 1
    assert "ruled_date" in res.output


def test_override_missing_a_side_is_a_defect(tmp_path):
    p = _write(tmp_path, "  life-architect:\n" + _GOOD_ENTRY
               + "    override:\n      proposed: floor-only\n      ruled_reason: because\n")
    res = CliRunner().invoke(vor.main, ["--path", str(p)])
    assert res.exit_code == 1
    assert "override missing ruled" in res.output


def test_override_proposed_equals_ruled_is_a_defect(tmp_path):
    p = _write(tmp_path, "  life-architect:\n" + _GOOD_ENTRY
               + "    override:\n      proposed: full\n      ruled: full\n"
                 "      ruled_reason: x\n")
    res = CliRunner().invoke(vor.main, ["--path", str(p)])
    assert res.exit_code == 1
    assert "not an override" in res.output


def test_unusable_register_exits_2(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("just a scalar\n", encoding="utf-8")      # no rulings: map
    res = CliRunner().invoke(vor.main, ["--path", str(p)])
    assert res.exit_code == 2
    assert "UNUSABLE" in res.output


def test_missing_file_exits_2(tmp_path):
    res = CliRunner().invoke(vor.main, ["--path", str(tmp_path / "nope.yaml")])
    assert res.exit_code == 2
