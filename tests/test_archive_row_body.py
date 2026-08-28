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

    failures, notes, _ = arb.verify(root, TODAY)
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

    failures, _, _ = arb.verify(root, TODAY)
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
    assert arb.verify(root, TODAY) == ([], [], 1)


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


def test_relocate_refuses_when_the_row_already_quotes_the_pointer(tmp_path):
    # A row ABOUT this mechanism is the realistic case. Two copies of the pointer would
    # break leg B and the tail splice, so it is refused BEFORE anything is written.
    ptr = arb.pointer_for("tasks/archive/1.md")
    root = _tree(tmp_path, {1: _body(1, f"Done when: the row reads {ptr} correctly", _LONG)})
    with pytest.raises(ValueError, match="requires exactly 1"):
        arb.relocate(root, 1, TODAY)
    assert not (root / "tasks" / "archive" / "1.md").exists()


def test_a_failed_post_write_proof_rolls_the_pair_back(tmp_path, monkeypatch):
    # The post-write proof is the last line of defence, so the state it rejects must not
    # survive: neither a half-relocated row nor a record that does not describe one.
    root = _tree(tmp_path, {1: _body(1, "Done when: it is done", _LONG)})
    before_row = (root / "tasks" / "1-synthetic-row.md").read_bytes()
    monkeypatch.setattr(arb, "reconstruct_before",
                        lambda *a, **k: "not the original body")
    with pytest.raises(RuntimeError, match="NOT byte-identical"):
        arb.relocate(root, 1, TODAY)
    assert (root / "tasks" / "1-synthetic-row.md").read_bytes() == before_row
    assert not (root / "tasks" / "archive" / "1.md").exists()


def test_verify_never_calls_an_empty_set_proven(capsys, tmp_path):
    # CLAUDE.md 10: a validator must not report a vacuous pass as proof.
    _tree(tmp_path, {1: _body(1, "Done when: it is done")})
    monkey = arb._REPO_ROOT
    try:
        arb._REPO_ROOT = tmp_path
        assert arb.main(["verify"]) == 0
    finally:
        arb._REPO_ROOT = monkey
    assert "nothing to verify" in capsys.readouterr().out


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
    failures, _, _ = arb.verify(root, TODAY)
    assert any("LEG A" in f for f in failures)


def _two_event_record(tmp_path: Path) -> tuple[Path, Path]:
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _OLDER, _LONG)})
    arb.relocate(root, 1, TODAY)
    row = root / "tasks" / "1-synthetic-row.md"
    ptr = arb.pointer_for("tasks/archive/1.md")
    body = arb._row_body(row)
    arb._set_row_body(row, body[: -len(arb.SEP + ptr)] + arb.SEP + _LONG + arb.SEP + ptr)
    arb.relocate(root, 1, TODAY)
    return root, root / "tasks" / "archive" / "1.md"


def test_deleting_a_whole_event_section_is_detected(tmp_path):
    # DELETION is the failure the clause digests CANNOT catch on their own: remove a
    # section and every surviving digest still matches. The declared counts are what make
    # it detectable, which is why they are parsed rather than merely rendered.
    root, rec_path = _two_event_record(tmp_path)
    text = arb.read_text(rec_path)
    head, _, _ = text.partition("## Event 1 — relocated")
    _, _, tail = text.partition("## Event 2 — relocated")
    arb.write_text(rec_path, head + "## Event 2 — relocated" + tail)
    with pytest.raises(ValueError, match="event section was added or removed|not 1.."):
        arb.parse_record(rec_path)
    failures, _, _ = arb.verify(root, TODAY)
    assert any("unreadable record" in f for f in failures)


def test_deleting_one_clause_block_inside_an_event_is_detected(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _OLDER, _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    lines = arb.read_text(rec_path).split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.startswith("### Clause 1.1"))
    arb.write_text(rec_path, "\n".join(lines[:start] + lines[start + 5:]))
    with pytest.raises(ValueError, match="clause block|not contiguous"):
        arb.parse_record(rec_path)


def test_editing_a_clause_length_without_its_digest_is_detected(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    text = arb.read_text(rec_path)
    arb.write_text(rec_path, text.replace(_LONG, _LONG + " and one more sentence.", 1))
    with pytest.raises(ValueError, match="its heading claims"):
        arb.parse_record(rec_path)


def test_a_record_may_not_claim_an_id_that_is_not_its_filename(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    arb.write_text(rec_path, arb.read_text(rec_path).replace('id: "[#1]"', 'id: "[#2]"', 1))
    with pytest.raises(ValueError, match="belongs in"):
        arb.parse_record(rec_path)


def test_verify_fails_on_an_orphan_pointer_with_no_record(tmp_path):
    """LEG E — completeness, enumerated from the ROWS (terra HIGH, 2026-08-29).

    Every other leg starts at a record, so deleting the record removes the only thing that
    would have complained. This leg starts at the rows, so absence is a failure.
    """
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    (root / "tasks" / "archive" / "1.md").unlink()
    failures, _, proven = arb.verify(root, TODAY)
    assert any("LEG E" in f and "GONE, not relocated" in f for f in failures)
    assert proven == 0


def test_a_corrupted_post_digest_fails_rather_than_disabling_leg_c(tmp_path):
    """terra HIGH, 2026-08-29: gating leg C on the `body_after` digest let one flipped hex
    character turn the check off and still exit 0. The reconstruction is attempted FIRST."""
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    rec = arb.parse_record(rec_path)
    bad = ("0" if rec.events[-1].body_after_sha256[0] != "0" else "1") \
        + rec.events[-1].body_after_sha256[1:]
    arb.write_text(rec_path,
                   arb.read_text(rec_path).replace(rec.events[-1].body_after_sha256, bad, 1))
    # The corruption must NOT buy silence: leg C still reconstructs and still proves out.
    failures, notes, proven = arb.verify(root, TODAY)
    assert failures == []
    assert notes == []
    assert proven == 1


def test_verify_fails_when_the_row_was_altered_but_still_matches_the_post_digest(tmp_path):
    # The other half of the same fix: a record whose clauses no longer reconstruct the
    # recorded original, on a row that IS what the record says it left behind, is a FAILURE
    # rather than an UNPROVEN note -- a later edit cannot be the excuse.
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    rec = arb.parse_record(rec_path)
    bad = ("0" if rec.events[-1].body_before_sha256[0] != "0" else "1") \
        + rec.events[-1].body_before_sha256[1:]
    arb.write_text(rec_path,
                   arb.read_text(rec_path).replace(rec.events[-1].body_before_sha256, bad, 1))
    failures, _, _ = arb.verify(root, TODAY)
    assert any("content was destroyed or altered" in f for f in failures)


@pytest.mark.parametrize("clause", [
    "consumer=ops-bot, reading the digest since 2026-07-01",
    "consumption_path=SessionStart digest, live since 2026-07-01",
    "trigger=nightly since 2026-07-01",
    "verified_by=the 2026-07-01 probe",
])
def test_routine_declaration_fields_are_structural(clause):
    """terra HIGH, 2026-08-29: the `routine:` marker and its FIELDS are separate clauses.

    `check_routine_consumers._ROUTINE_FIELD_RE` reads `· consumer=` / `· consumption_path=`
    off the row, so blocking only the marker clause would let a trailing field be relocated
    out of a declared-routine row and FAIL that gate.
    """
    assert arb.is_structural(clause) is not None
    assert arb.eligible_run(_body(1, clause), None, TODAY) == []


def test_verify_fails_when_the_row_drops_its_pointer(tmp_path):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    row = root / "tasks" / "1-synthetic-row.md"
    ptr = arb.pointer_for("tasks/archive/1.md")
    arb._set_row_body(row, arb._row_body(row)[: -len(arb.SEP + ptr)])
    failures, _, _ = arb.verify(root, TODAY)
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
    failures, notes, _ = arb.verify(root, TODAY)
    assert failures == []
    assert any("UNPROVEN" in n for n in notes)


# --- rerender ---------------------------------------------------------------------------

def test_rerender_changes_prose_and_never_the_payload(tmp_path, monkeypatch):
    original = _body(1, "Done when: x", _OLDER, _LONG)
    root = _tree(tmp_path, {1: original})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    before = arb.parse_record(rec_path)

    assert arb.rerender(root) == []          # idempotent when the prose is current

    real = arb.render_record
    monkeypatch.setattr(arb, "render_record",
                        lambda *a: real(*a).replace("Relocated verbatim",
                                                    "RELOCATED VERBATIM", 1)
                        if "Relocated verbatim" in real(*a)
                        else real(*a).replace("relocated **verbatim**",
                                              "relocated VERBATIM", 1))
    assert arb.rerender(root) == [1]
    after = arb.parse_record(rec_path)
    assert after.events == before.events     # the payload is untouched, event for event
    assert arb.read_text(rec_path) != ""
    failures, _, proven = arb.verify(root, TODAY)
    assert failures == [] and proven == 1


def test_rerender_rolls_back_if_it_would_change_content(tmp_path, monkeypatch):
    root = _tree(tmp_path, {1: _body(1, "Done when: x", _LONG)})
    arb.relocate(root, 1, TODAY)
    rec_path = root / "tasks" / "archive" / "1.md"
    before = rec_path.read_bytes()
    real = arb.render_record
    # A renderer that quietly drops a clause is exactly what the round-trip must catch.
    monkeypatch.setattr(arb, "render_record",
                        lambda tid, row, rel, evs: real(tid, row, rel, evs).replace(
                            "- clauses relocated: 1", "- clauses relocated: 0", 1))
    with pytest.raises((RuntimeError, ValueError)):
        arb.rerender(root)
    assert rec_path.read_bytes() == before


# --- the live tree ----------------------------------------------------------------------

def test_every_committed_record_still_proves_out():
    """THE REGRESSION TEST: every record in this repo's `tasks/archive/` verifies clean."""
    if not arb.record_files(_REPO):
        pytest.skip("no archived records in this checkout")
    failures, _, proven = arb.verify(_REPO, date.today())
    assert failures == [], "archived records no longer prove byte-identical: " + "; ".join(
        failures[:5])
    # An empty `proven` with an empty `failures` is the vacuous pass this assertion exists
    # to refuse: legs A/B/D can all hold over records whose leg C never reconstructed.
    assert proven == len(arb.record_files(_REPO))
