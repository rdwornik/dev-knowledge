"""Tests for scripts/archive_row_body.py — [#612] doc-rot row-body archival.

The load-bearing assertion of this module is BYTE-IDENTITY, so the tests are built to fail
if relocation ever becomes lossy: a synthetic tree is relocated and then reconstructed, and
the reconstruction is compared to the ORIGINAL bytes rather than to a recorded digest. The
refusal set is pinned individually, because each refusal exists to stop a specific way the
mechanism could destroy something (a gate-read clause, a derived-frontmatter flip, a
retired allocation record, a relocation that costs more than it saves).

The live-tree test at the bottom is the one that would catch a real regression on this
repo: every committed record must still prove out.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import archive_row_body as arb  # noqa: E402
import gen_task_tree as gtt  # noqa: E402

TODAY = date(2026, 8, 29)

_LONG = ("**RE-CUT 2026-08-27** (K3) — a long dated amendment clause that carries enough "
         "narration to be worth relocating, repeated so it comfortably exceeds the pointer "
         "it will be replaced by. " * 3).strip()
_OLDER = "UN-DEFERRED 2026-08-09 (ARC-2): peg met 2026-07-07; un-blocks the chain"


def _body(task_id: int, *clauses: str) -> str:
    head = f"- [#{task_id}] [P2][M] **A synthetic row** — scope prose that stays put."
    return arb.SEP.join([head, *clauses])


def _tree(tmp_path: Path, rows: dict[int, str], *, referenced: set[int] | None = None) -> Path:
    """A minimal `tasks/` tree: one file per row plus a manifest that references them."""
    tasks = tmp_path / "tasks"
    tasks.mkdir()
    nodes: list[dict] = [{"prose": "# synthetic BACKLOG"}]
    ref = rows.keys() if referenced is None else referenced
    for tid, body in rows.items():
        name = f"{tid}-synthetic-row.md"
        arb.write_text(tasks / name, f'---\nid: "[#{tid}]"\ngenerates: BACKLOG.md\n---\n\n'
                                     f"{body}\n")
        if tid in ref:
            nodes.append({"task": tid, "file": name})
    arb.write_text(tasks / "manifest.json", json.dumps({"schema": 2, "nodes": nodes}, indent=2))
    return tmp_path


# --- clause classification --------------------------------------------------------------

def test_split_clauses_round_trips():
    body = _body(1, "one", "two", "three")
    assert arb.SEP.join(arb.split_clauses(body)) == body


@pytest.mark.parametrize("clause", [
    "Done when: the thing is done on 2026-08-01",
    "refs #11, ADR-81, LESSONS 2026-05-29",
    "kill-candidates: none — nothing since 2026-08-01",
    "depends-on: 439 as of 2026-08-01",
    "serialize-group: playbook (set 2026-08-01)",
    "routine: nightly since 2026-08-01",
    "review_date=2026-08-01",
    "DEFERRED 2026-08-22 (architect): held on one unmade policy",
])
def test_structural_clauses_are_never_relocatable(clause):
    assert arb.is_structural(clause) is not None
    assert arb.eligible_run(_body(1, clause), None, TODAY) == []


def test_prose_that_merely_mentions_a_deferral_is_still_relocatable():
    # The `· DEFER` marker is a PREFIX, not a word anywhere in the clause: blocking every
    # mention would refuse exactly the narration this drain exists for.
    c = "**UN-DEFERRED 2026-08-24** — the deferral below is spent; the row stays open"
    assert arb.is_structural(c) is None
    assert arb.eligible_run(_body(1, c), None, TODAY) == [c]


def test_an_undated_clause_is_not_narration():
    assert arb.eligible_run(_body(1, "a clause with no date at all"), None, TODAY) == []


def test_a_citation_date_is_a_name_not_history():
    # Reuses validate_doc_rot's citation-blindness, so the drain and the detector agree.
    c = "see docs/audits/2026-08-15-technical-thing.md for the numbers"
    assert arb.eligible_run(_body(1, c), None, TODAY) == []


def test_clause_zero_is_never_eligible():
    # A row whose ONLY clause is the head, and that head carries a date.
    body = "- [#1] [P2][M] **Row** — landed 2026-08-01 and nothing else"
    assert arb.eligible_run(body, None, TODAY) == []


def test_the_run_stops_at_the_first_structural_clause():
    body = _body(1, "Done when: 2026-08-01 x", "**A 2026-08-02**", "**B 2026-08-03**")
    assert arb.eligible_run(body, None, TODAY) == ["**A 2026-08-02**", "**B 2026-08-03**"]


def test_the_run_ends_before_an_existing_pointer():
    ptr = arb.pointer_for("tasks/archive/1.md")
    body = _body(1, "**A 2026-08-02**", ptr)
    assert arb.eligible_run(body, ptr, TODAY) == ["**A 2026-08-02**"]


def test_the_pointer_is_path_qualified_and_carries_no_date():
    ptr = arb.pointer_for("tasks/archive/1.md")
    assert "tasks/archive/" in ptr
    assert arb._rot._history_dates(ptr, TODAY) == []


def test_worth_relocating_demands_the_row_saves_what_the_pointer_costs():
    ptr = arb.pointer_for("tasks/archive/1.md")
    assert arb.worth_relocating(1000, 1000 - len(ptr), ptr)
    assert not arb.worth_relocating(1000, 1000 - len(ptr) + 1, ptr)


# --- relocation is byte-identical -------------------------------------------------------

def test_relocation_is_byte_identical_and_strictly_shorter(tmp_path):
    original = _body(1, "Done when: it is done", _OLDER, _LONG)
    root = _tree(tmp_path, {1: original})

    before, after, n = arb.relocate(root, 1, TODAY)
    assert n == 2
    assert after < before

    rec = arb.parse_record(root / "tasks" / "archive" / "1.md")
    live = arb._row_body(root / "tasks" / "1-synthetic-row.md")
    assert live.endswith(arb.SEP + rec.pointer)
    # The claim, checked against the ORIGINAL bytes rather than a recorded digest.
    assert arb.reconstruct_before(live, rec.events[-1], rec.pointer) == original

    failures, notes = arb.verify(root, TODAY)
    assert failures == []
    assert notes == []


def test_a_second_wave_appends_an_event_and_keeps_the_pointer_last(tmp_path):
    original = _body(1, "Done when: it is done", _OLDER, _LONG)
    root = _tree(tmp_path, {1: original})
    arb.relocate(root, 1, TODAY)

    # A human appends more narration BEFORE the pointer, as the row grows again.
    row = root / "tasks" / "1-synthetic-row.md"
    ptr = arb.pointer_for("tasks/archive/1.md")
    after_first = arb._row_body(row)
    grown = after_first[: -len(arb.SEP + ptr)] + arb.SEP + _LONG + arb.SEP + ptr
    arb._set_row_body(row, grown)

    arb.relocate(root, 1, TODAY)
    rec = arb.parse_record(root / "tasks" / "archive" / "1.md")
    assert len(rec.events) == 2
    assert rec.events[-1].had_pointer_before is True

    # Each event proves its OWN act. Event 2 reproduces the row as it stood when event 2
    # fired -- the grown row, pointer still last.
    live = arb._row_body(row)
    assert live.endswith(arb.SEP + ptr)
    assert live.count(ptr) == 1
    assert arb.reconstruct_before(live, rec.events[-1], rec.pointer) == grown
    # Event 1 reproduces the ORIGINAL from the row as it stood right after event 1.
    assert arb.reconstruct_before(after_first, rec.events[0], rec.pointer) == original

    failures, _ = arb.verify(root, TODAY)
    assert failures == []


def test_a_chained_unwind_is_only_exact_when_nothing_was_appended_between_events(tmp_path):
    """The stated limit of a MULTI-EVENT record, pinned so it cannot be forgotten.

    Unwinding every event in reverse reproduces the original row **only** when the row was
    not edited between relocations. When narration was appended in between (the normal
    case), the chain reproduces that appended text too -- each event is exact about the
    body IT acted on, which is the claim `verify` actually makes.
    """
    original = _body(1, "Done when: it is done", _OLDER, _LONG)
    root = _tree(tmp_path, {1: original})
    arb.relocate(root, 1, TODAY)
    row = root / "tasks" / "1-synthetic-row.md"
    ptr = arb.pointer_for("tasks/archive/1.md")
    body = arb._row_body(row)
    arb._set_row_body(row, body[: -len(arb.SEP + ptr)] + arb.SEP + _LONG + arb.SEP + ptr)
    arb.relocate(root, 1, TODAY)

    rec = arb.parse_record(root / "tasks" / "archive" / "1.md")
    got = arb._row_body(row)
    for ev in reversed(rec.events):
        got = arb.reconstruct_before(got, ev, rec.pointer)
    assert got != original                              # the documented limit, not a defect
    # ... and it is a limit about ORDER, never about loss: every clause of the original is
    # still present in the unwind, which is the property the archive actually guarantees.
    assert all(c in arb.split_clauses(got) for c in arb.split_clauses(original))


def test_the_record_survives_a_clause_containing_a_triple_backtick_fence(tmp_path):
    # The payload is verbatim row prose; a 3-backtick run inside it must not terminate the
    # 4-backtick fence the record stores it in.
    nasty = "**NOTE 2026-08-02** — the row said ```py\\nx=1\\n``` and more " * 4
    original = _body(1, "Done when: it is done", nasty.strip())
    root = _tree(tmp_path, {1: original})
    arb.relocate(root, 1, TODAY)
    rec = arb.parse_record(root / "tasks" / "archive" / "1.md")
    assert rec.events[0].clauses == [nasty.strip()]
    assert arb.verify(root, TODAY) == ([], [])


def test_records_are_written_lf_only(tmp_path):
    # write_text launders LF->CRLF on Windows and read_text cannot detect it; a record
    # written CRLF would hash differently from the row it claims to be identical to.
    root = _tree(tmp_path, {1: _body(1, "Done when: it is done", _LONG)})
    arb.relocate(root, 1, TODAY)
    for p in (root / "tasks" / "archive" / "1.md",
              root / "tasks" / "1-synthetic-row.md"):
        assert b"\r\n" not in p.read_bytes()


# --- the refusals -----------------------------------------------------------------------

def test_relocate_refuses_a_row_with_no_eligible_run(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: it is done")})
    with pytest.raises(ValueError, match="no eligible dated-amendment clause run"):
        arb.relocate(root, 1, TODAY)


def test_relocate_refuses_when_the_saving_is_smaller_than_the_pointer(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", "**tiny 2026-08-02**")})
    with pytest.raises(ValueError, match="in indirection than it gains"):
        arb.relocate(root, 1, TODAY)


def test_relocate_refuses_a_retired_row(tmp_path):
    # An unreferenced task file is an allocation record (ADR-107 6.3), not a queue row.
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)}, referenced=set())
    with pytest.raises(ValueError, match="has no file in tasks/"):
        arb.relocate(root, 1, TODAY)
    assert arb.propose(root, None, TODAY) == []


def test_relocate_refuses_a_status_flip(tmp_path):
    # The whole row's `· DEFER` marker sits in the LAST clause, which also reads as
    # narration; taking it would silently flip the row from deferred to open.
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG,
                                     "DEFERRED 2026-08-22 (architect): held")})
    assert gtt.derive_status(arb._row_body(root / "tasks" / "1-synthetic-row.md")) == "deferred"
    with pytest.raises(ValueError, match="no eligible dated-amendment clause run"):
        arb.relocate(root, 1, TODAY)


def test_nothing_is_written_when_relocate_refuses(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: it is done")})
    before = arb.read_text(root / "tasks" / "1-synthetic-row.md")
    with pytest.raises(ValueError):
        arb.relocate(root, 1, TODAY)
    assert arb.read_text(root / "tasks" / "1-synthetic-row.md") == before
    assert not (root / "tasks" / "archive").exists()


# --- verify's legs ----------------------------------------------------------------------

def test_verify_fails_when_an_archived_clause_is_altered(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    arb.write_text(rec_path, arb.read_text(rec_path).replace("comfortably exceeds",
                                                             "comfortably EXCEEDS", 1))
    failures, _ = arb.verify(root, TODAY)
    assert any("LEG A" in f for f in failures)


def test_verify_fails_when_the_row_drops_its_pointer(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    row = root / "tasks" / "1-synthetic-row.md"
    ptr = arb.pointer_for("tasks/archive/1.md")
    arb._set_row_body(row, arb._row_body(row)[: -len(arb.SEP + ptr)])
    failures, _ = arb.verify(root, TODAY)
    assert any("LEG B" in f for f in failures)


def test_verify_reports_unproven_not_failed_when_the_row_is_edited_later(tmp_path):
    # The stated honest limit: an edited row makes leg C uncomputable. It must be LOUD and
    # it must not be a FAIL -- a false RED on ordinary row maintenance kills the mechanism.
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    row = root / "tasks" / "1-synthetic-row.md"
    ptr = arb.pointer_for("tasks/archive/1.md")
    body = arb._row_body(row)
    arb._set_row_body(row, body[: -len(arb.SEP + ptr)] + arb.SEP + "a later note" +
                      arb.SEP + ptr)
    failures, notes = arb.verify(root, TODAY)
    assert failures == []
    assert any("UNPROVEN" in n for n in notes)


# --- the live tree ----------------------------------------------------------------------

def test_every_committed_record_still_proves_out():
    """THE REGRESSION TEST: every record in this repo's `tasks/archive/` verifies clean."""
    if not arb.record_files(_REPO):
        pytest.skip("no archived records in this checkout")
    failures, _ = arb.verify(_REPO, date.today())
    assert failures == [], "archived records no longer prove byte-identical: " + "; ".join(
        failures[:5])
