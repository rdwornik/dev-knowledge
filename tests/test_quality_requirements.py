"""The register's own proof layer -- `ecosystem/quality-requirements.yaml` ([#765], AN2-1).

THREE LEGS, AND ONLY THE THIRD IS THE INTERESTING ONE.

  1. SCHEMA. The register keeps its own contract: ids well-formed and unique, attributes
     inside the declared set, `measured` carrying `organ` and `trip_test`, `candidate`
     carrying neither. Refusing a candidate that names an organ is the asymmetry the whole
     design rests on, so it gets a negative control rather than a claim.
  2. RESOLUTION. Every `measured` entry's organ resolves to a file that exists and its
     trip-test resolves to a test function that exists. This is the leg a reader assumes is
     the whole check, and it is the weakest one: a path that exists says nothing about what
     lives at it.
  3. THE NEUTERED-ORGAN LEG, which is what the done-contract actually asks for -- "a
     `measured` entry whose trip-test passes unconditionally is a REFUSAL, not a pass". A
     path check cannot see that. So each trip body is run TWICE: once against its live
     organ (it has to pass) and once against the same organ with exactly one refusal
     replaced by a permissive stand-in (it has to go RED). A trip-test that survives its
     organ being disabled is measuring something else, and this is the only leg that can
     tell.

WHY THE MUTATION IS OF THE ORGAN AND NOT OF THE TRIP-TEST. Mutating the test would ask
"does this test test anything"; mutating the organ asks "does this test test THE ORGAN THE
REGISTER NAMES", which is the claim the register makes. The distinction is the difference
between a test that is not vacuous and a test that is about the right subject.

THE LEG ALSO BINDS THE MAPPING, not just the tests in it: every `measured` id in the
register has to appear in `TRIPS`, and every `TRIPS` key has to be a `measured` id. A trip
whose register entry was demoted to `candidate` would otherwise keep passing while proving
a requirement nobody claims.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import quality_requirements as qr  # noqa: E402

from test_quality_requirement_trips import TRIPS  # noqa: E402


@pytest.fixture(scope="module")
def register() -> dict:
    return qr.load(_REPO_ROOT)


# ------------------------------------------------------------------ leg 1: schema


def test_the_live_register_keeps_its_own_schema(register):
    assert qr.schema_defects(register) == []


def test_the_register_declares_a_floor_tier_with_a_reason(register):
    """AN2-1 rules the register a floor component; a tier with no reason is not a
    declaration, it is a value."""
    floor = register["floor"]
    assert str(floor["tier"]).strip()
    assert str(floor["reason"]).strip()


def test_a_candidate_that_names_an_organ_is_REFUSED(register):
    """The asymmetry, as a negative control.

    This is the failure mode the register exists to prevent -- a requirement dressed as
    enforcement -- so it is asserted rather than described. Without this test the schema's
    `candidate` branch could be deleted and every live entry would still pass.
    """
    poisoned = {
        "register_version": register["register_version"],
        "floor": register["floor"],
        "attributes": register["attributes"],
        "requirements": [dict(register["requirements"][0])],
    }
    row = poisoned["requirements"][0]
    row["status"] = qr.STATUS_CANDIDATE
    row["organ"] = "scripts/audit.py"
    row["trip_test"] = "tests/test_audit.py::test_anything"
    defects = qr.schema_defects(poisoned)
    assert any("candidate" in d and "organ" in d for d in defects), defects


def test_a_measured_entry_with_no_trip_test_is_REFUSED(register):
    poisoned = {
        "register_version": register["register_version"],
        "floor": register["floor"],
        "attributes": register["attributes"],
        "requirements": [dict(r) for r in qr.measured(register)[:1]],
    }
    poisoned["requirements"][0].pop("trip_test")
    defects = qr.schema_defects(poisoned)
    assert any("trip_test" in d for d in defects), defects


def test_every_requirement_carries_a_measured_incident(register):
    """The register is bounded BY DESIGN (AN2-1: "a register, not more backlog rows"), and
    the incident field is what bounds it: a requirement with no incident behind it is a
    preference, and preferences are unbounded."""
    for row in qr.requirements(register):
        assert str(row["incident"]).strip(), row["id"]


# ------------------------------------------------------------------ leg 2: resolution


def test_every_measured_entry_resolves_its_organ_and_its_trip_test(register):
    assert qr.unresolved_organs(register, _REPO_ROOT) == []


def test_every_named_trip_test_function_exists(register):
    """The trip-test is named as `<file>::<function>`; the FUNCTION has to be there.

    Collected through the mapping rather than by reading the file's source text: importing
    the module and looking the name up answers the question the register asks, while a grep
    for `def <name>` would answer whether the characters appear.
    """
    import test_quality_requirement_trips as trips

    for row in qr.measured(register):
        _, test_name = qr.parse_trip(row["trip_test"])
        assert hasattr(trips, test_name), (
            f"{row['id']}: names {row['trip_test']}, and that function does not exist")


# ------------------------------------------------------------------ leg 3: the mutation


def test_the_trip_mapping_and_the_register_agree(register):
    measured_ids = {row["id"] for row in qr.measured(register)}
    assert measured_ids == set(TRIPS), (
        "the register's measured set and the TRIPS mapping disagree -- "
        f"register-only {sorted(measured_ids - set(TRIPS))}, "
        f"mapping-only {sorted(set(TRIPS) - measured_ids)}")


@pytest.mark.parametrize("requirement_id", sorted(TRIPS))
def test_each_trip_test_passes_against_its_live_organ(requirement_id, tmp_path):
    body, organ, _ = TRIPS[requirement_id]
    body(organ, tmp_path)


@pytest.mark.parametrize("requirement_id", sorted(TRIPS))
def test_each_trip_test_goes_RED_when_its_organ_is_NEUTERED(requirement_id, tmp_path):
    """The done-contract's refusal clause, as a mechanism.

    `AssertionError` specifically, and not any exception: a trip that blew up with a
    `TypeError` against the stand-in would also "fail", and would prove the stand-in is
    malformed rather than that the trip notices the missing refusal.
    """
    body, _, neuter = TRIPS[requirement_id]
    with pytest.raises(AssertionError) as caught:
        body(neuter(), tmp_path)
    assert "VIOLATED" in str(caught.value), (
        f"{requirement_id}: the trip failed against a neutered organ, but not on the "
        f"assertion that names the requirement -- got {caught.value!r}")


# ------------------------------------------------------------------ the rendered section


def test_the_architecture_section_is_current(register):
    """Regen-and-diff, the same idiom the neighbouring generated indices use."""
    assert qr.render_defects(_REPO_ROOT) == []


def test_the_rendered_section_names_every_requirement(register):
    body = qr.render_section(register)
    for row in qr.requirements(register):
        assert row["id"] in body, f"{row['id']} is absent from the rendered section"


def test_a_candidate_renders_with_no_organ_column(register):
    """The section has to make the measured/candidate split visible, because a reader who
    cannot see it reads the whole table as enforcement."""
    body = qr.render_section(register)
    for line in body.splitlines():
        if not line.startswith("| `QR-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        status, organ_cell, trip_cell = cells[2], cells[4], cells[5]
        if status == qr.STATUS_CANDIDATE:
            assert organ_cell == "—" and trip_cell == "—", line
        else:
            assert organ_cell != "—" and trip_cell != "—", line
