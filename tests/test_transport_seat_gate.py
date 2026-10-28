"""[#1746] ADR-132 D3: the successor half of `seat_ids_both` moves to the successor's first
transport write. `transport.write` / `append` refuse a `by:` that names a Tech-Architect id the
generated `ecosystem/seat-ids.yaml` has not registered, unless the file's own head states that
seat's id/session pair (the registering write). Every test drives a synthetic transport in
`tmp_path`; nothing here touches the real drive."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

SEATS = [
    {"seat": "Tech-Architect-43", "session": "2026-10-02-dev-knowledge-architect",
     "provenance": "to-cc/AMEND-seed-43.md", "stated_in": 1},
    {"seat": "Tech-Architect-44", "session": "2026-10-08-dev-knowledge-architect",
     "provenance": "to-cc/AMEND-seed-44.md", "stated_in": 1},
]


@pytest.fixture()
def t():
    return importlib.import_module("transport")


@pytest.fixture()
def world(tmp_path: Path, t, monkeypatch) -> dict:
    root = tmp_path / "drive"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-browser").mkdir()
    seat_file = tmp_path / "seat-ids.yaml"
    t.write_seat_ids(seat_file, seats=list(SEATS), inventory={})
    monkeypatch.setattr(t, "known_root", lambda: root)
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", seat_file)
    return {"root": root, "browser": root / "to-browser", "seat_file": seat_file}


def _doc(by: str) -> str:
    return f"by: {by}\ndate: 2026-10-10\nsummary: a digest\n\n# D\ndev-knowledge\n"


def test_an_unregistered_tech_architect_id_in_by_is_refused_naming_the_fix(t, world):
    dest = world["browser"] / "DIGEST-succ-2026-10-10.md"
    with pytest.raises(t.TransportWriteRefused) as err:
        t.write("operator", dest, _doc("Tech-Architect-48 (R91)"))
    assert "Tech-Architect-48" in str(err.value)
    assert "seat-ids --write" in str(err.value)
    assert not dest.exists()


def test_a_registered_tech_architect_id_in_by_is_written(t, world):
    dest = world["browser"] / "DIGEST-ok-2026-10-10.md"
    t.write("operator", dest, _doc("Tech-Architect-44 (R91)"))
    assert dest.is_file()


def test_the_registering_write_that_states_its_own_pair_is_allowed(t, world):
    dest = world["browser"] / "DIGEST-first-2026-10-10.md"
    t.write("operator", dest, _doc("Tech-Architect-48 (2026-10-29-dev-knowledge-architect)"))
    assert dest.is_file()
    pairs = {(s["seat"], s["session"]) for s in t.build_seat_map(world["root"])["seats"]}
    assert ("Tech-Architect-48", "2026-10-29-dev-knowledge-architect") in pairs


def test_a_by_with_no_tech_architect_id_is_not_gated(t, world):
    dest = world["browser"] / "DIGEST-lane-2026-10-10.md"
    t.write("operator", dest, _doc("CC lane bind-handoff (claude-sonnet-5-5) for the E2.2 orchestrator"))
    assert dest.is_file()


def test_append_is_gated_the_same_way(t, world):
    dest = world["browser"] / "SESSION-succ.md"
    with pytest.raises(t.TransportWriteRefused):
        t.append("lane", dest, _doc("Tech-Architect-48 (R91)"))
    assert not dest.exists()


def test_a_scratch_tree_that_is_not_the_known_transport_is_not_gated(t, world, tmp_path):
    scratch = tmp_path / "scratch" / "to-browser"
    scratch.mkdir(parents=True)
    t.write("operator", scratch / "DIGEST-x-2026-10-10.md", _doc("Tech-Architect-48 (R91)"))
    assert (scratch / "DIGEST-x-2026-10-10.md").is_file()


def test_an_empty_registry_has_nothing_to_check_against_and_does_not_gate(t, world):
    t.write_seat_ids(world["seat_file"], seats=[], inventory={})
    dest = world["browser"] / "DIGEST-empty-2026-10-10.md"
    t.write("operator", dest, _doc("Tech-Architect-48 (R91)"))
    assert dest.is_file()
