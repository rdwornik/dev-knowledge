"""lane-transport-registry (BATCH-WAVE5B-N1 #9): the transport's kinds, registered, and the
one write gate every future writer composes.

Done-when 1: `ecosystem/transport-registry.yaml` lists every kind the code uses, and a test
derives the kind set from the code and asserts none is missing -- `test_derivation_finds_
nothing_missing_from_the_real_registry` below, against the real `scripts/` tree, not a fixture.

Done-when 2: `transport.write` refuses an unregistered writer -- `test_handback_cannot_write_
the_integrators_refused_kind` is the literal case the contract names.

Done-when 3: the stray-file report is exercised in `test_scan_*` (report-only: `scan()` never
writes, moves or deletes).

Every test but the derivation one drives a synthetic transport in `tmp_path`; nothing here
touches the real drive.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

REGISTRY_PATH = _REPO / "ecosystem" / "transport-registry.yaml"


def _mod(name: str):
    return importlib.import_module(name)


@pytest.fixture()
def t():
    return _mod("transport")


@pytest.fixture()
def registry(t):
    return t.load_registry(REGISTRY_PATH)


@pytest.fixture()
def world(tmp_path: Path) -> dict:
    root = tmp_path / "drive"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-browser").mkdir()
    return {"root": root, "cc": root / "to-cc", "browser": root / "to-browser"}


# --- the registry itself, as data ----------------------------------------------------------------

def test_the_real_registry_loads_and_every_row_is_well_formed(t, registry):
    assert len(registry) >= 15
    names = [k.name for k in registry]
    assert len(names) == len(set(names)), "duplicate kind names"
    for k in registry:
        assert k.folder in t.FOLDERS
        assert k.writers, f"{k.name} has no writer"
        assert k.prefix.endswith("-"), f"{k.name}'s prefix must end in '-': {k.prefix!r}"


def test_every_kind_classifies_a_filename_shaped_from_its_own_prefix(t, registry):
    """Round-trip: a synthetic filename built from a kind's own `prefix` must classify back to
    THAT kind (not a shorter sibling prefix) -- catches a `pattern` that drifted from `prefix`."""
    for k in registry:
        sample = f"{k.prefix}example-2026-09-25.md"
        got = t.classify(sample, registry)
        assert got is not None, f"{k.name}'s own prefix {k.prefix!r} does not self-classify"
        assert got.name == k.name, (
            f"{sample!r} classified as {got.name!r}, not {k.name!r} -- a shorter sibling "
            f"prefix (e.g. LANE- vs LANE-END-) is shadowing it")


def test_longest_prefix_wins_lane_end_over_the_bare_lane_contract_kind(t, registry):
    assert t.classify("LANE-END-lane-x.md", registry).name == "LANE_END"
    assert t.classify("LANE-a-539-ch8.md", registry).name == "LANE_CONTRACT"


# --- Done-when 1: derived from the code, not hand-copied ------------------------------------------

def test_derivation_finds_nothing_missing_from_the_real_registry(t, registry):
    derived = t.derive_kinds_from_code(_SCRIPTS)
    registered_prefixes = {k.prefix for k in registry}
    missing = derived - registered_prefixes
    assert not missing, (
        f"the code builds {sorted(missing)} on the transport and "
        f"{REGISTRY_PATH.name} has no row for it")


def test_derivation_finds_the_known_kinds_this_lane_read_off_the_code(t):
    """A floor, not a ceiling: these specific prefixes are the ones this lane's own research
    (handback.py, transport_report.py, gen_ledger.py, gen_seat_boot.py, gen_lane_contract.py,
    gen_handoff.py, propose_row_closures.py) found built on the transport. A future refactor
    that stops literally building one of these is fine; a run that finds NONE of them means the
    scan itself broke."""
    derived = t.derive_kinds_from_code(_SCRIPTS)
    expected = {"GO-", "LEDGER-", "LANE-END-", "HANDBACK-REFUSED-", "SESSION-", "SEAT-BOOT-",
               "MERGE-PLAN-", "ESCALATE-", "DECLARE-", "AMEND-", "BATCH-", "LANE-",
               "RATIFICATION-", "STATUS-", "QUESTION-", "ANSWER-", "CLOSURE-LIST-"}
    assert expected <= derived, f"missing from the scan: {sorted(expected - derived)}"


def test_derivation_does_not_pick_up_a_concrete_historical_filename(t, tmp_path):
    """A docstring citing an already-resolved past artifact (no placeholder after the prefix)
    is not a template -- the false positive this lane's own build hit first."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "example.py").write_text(
        'to_browser = resolve_transport()\n'
        '# see `to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md` for the full account\n',
        encoding="utf-8")
    assert t.derive_kinds_from_code(scripts_dir) == set()


def test_derivation_ignores_a_same_shaped_local_receipt_path_with_no_transport_anchor(t, tmp_path):
    """`X() / f"LAUNCH-{slug}.json"` is exactly the (join) shape a real transport write has --
    the thing that tells them apart is a nearby transport-resolving call, not the syntax."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "unrelated.py").write_text(
        'def receipts_dir():\n'
        '    return Path("logs/receipts")\n'
        '\n'
        'def launch_path(slug):\n'
        '    return receipts_dir() / f"LAUNCH-{slug.upper()}.json"\n',
        encoding="utf-8")
    assert t.derive_kinds_from_code(scripts_dir) == set()


# --- the write gate --------------------------------------------------------------------------

def test_write_succeeds_for_the_kinds_registered_writer(t, world, registry):
    dest = world["browser"] / "HANDBACK-REFUSED-lane-x.md"
    got = t.write("handback", dest, "line one\n", registry=registry)
    assert got == dest
    assert dest.read_text(encoding="utf-8") == "line one\n"


def test_handback_cannot_write_the_integrators_refused_kind(t, world, registry):
    """Done-when 2's literal case: `REFUSED-<lane>.md` is the INTEGRATOR's own repair-order
    path (D10); `handback` writing it would be exactly the collision D10 exists to prevent."""
    dest = world["browser"] / "REFUSED-lane-x.md"
    with pytest.raises(t.TransportWriteRefused, match="REFUSED"):
        t.write("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_write_refuses_an_entirely_unregistered_kind(t, world, registry):
    dest = world["browser"] / "ODD-NAME-lane-x.md"
    with pytest.raises(t.TransportWriteRefused, match="no registered kind"):
        t.write("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_write_is_atomic_and_replaces_rather_than_appends(t, world, registry):
    dest = world["browser"] / "LANE-END-lane-x.md"
    t.write("transport_report", dest, "first\n", registry=registry)
    t.write("transport_report", dest, "second\n", registry=registry)
    assert dest.read_text(encoding="utf-8") == "second\n"


def test_append_is_gated_the_same_way_as_write(t, world, registry):
    dest = world["browser"] / "REFUSED-lane-x.md"
    with pytest.raises(t.TransportWriteRefused):
        t.append("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_append_keeps_prior_content_and_adds_a_separating_newline(t, world, registry):
    dest = world["browser"] / "SESSION-lane-x.md"
    dest.write_text("some narrative the lane wrote by hand\n", encoding="utf-8")
    t.append("handback", dest, "HANDBACK worktree-lane-x @ deadbeef code", registry=registry)
    text = dest.read_text(encoding="utf-8")
    assert "some narrative the lane wrote by hand" in text
    assert "HANDBACK worktree-lane-x @ deadbeef code" in text
    assert text.count("HANDBACK ") == 1


# --- the stray-file report (Done-when 3, report-only) ----------------------------------------

def test_scan_is_clean_over_a_transport_holding_only_registered_kinds_in_their_own_folder(
        t, world, registry):
    (world["cc"] / "GO-batch1.md").write_text("x", encoding="utf-8")
    (world["browser"] / "SESSION-lane-x.md").write_text("x", encoding="utf-8")
    assert t.scan(world["root"], registry) == []


def test_scan_reports_an_unregistered_kind(t, world, registry):
    (world["browser"] / "ODD-NAME.md").write_text("x", encoding="utf-8")
    findings = t.scan(world["root"], registry)
    assert len(findings) == 1
    assert findings[0].path == "to-browser/ODD-NAME.md"
    assert "unregistered" in findings[0].reason


def test_scan_reports_a_registered_kind_sitting_in_the_wrong_folder(t, world, registry):
    """The lane's own Value line: 'a report once landed in the wrong folder.'"""
    (world["cc"] / "HANDBACK-REFUSED-lane-x.md").write_text("x", encoding="utf-8")
    findings = t.scan(world["root"], registry)
    assert len(findings) == 1
    assert findings[0].path == "to-cc/HANDBACK-REFUSED-lane-x.md"
    assert "HANDBACK_REFUSED" in findings[0].reason and "to-browser" in findings[0].reason


def test_scan_never_writes_moves_or_deletes_anything(t, world, registry):
    (world["browser"] / "ODD-NAME.md").write_text("x", encoding="utf-8")
    before = sorted(p.name for p in world["browser"].iterdir())
    t.scan(world["root"], registry)
    after = sorted(p.name for p in world["browser"].iterdir())
    assert before == after
