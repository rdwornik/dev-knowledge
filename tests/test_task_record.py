"""Coverage for scripts/task_record.py — ADR-122 step 1 (the pydantic model, the `task`
library/CLI, and the row/archive-record converter).

RED-FIRST (ADR-108 §B): written before scripts/task_record.py existed, so the whole
module failed to import; see the lane's session file for the pre-implementation run.

Scope, stated rather than assumed: step 1 is CONTRACT + RECONCILIATION, not the flip
(ADR-122 "Do not: flip the source of truth"). These tests cover the model's own
invariants (D1-D9) and the converter's classification of BOTH corpora named in the
ADR's step-1 exit criteria — live task rows under tasks/ and the row-body-archival
records under tasks/archive/ — against synthetic fixtures. The full-corpus run (667
rows + 86 archive records) is exercised separately by the lane's own converter CLI
invocation into job tmp, not by this suite (that run is measured, not asserted green —
see the ADR's step-1 exit criteria and the session file's DONE-ITEM 4 line).
"""
from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

import task_record as tr


# --- Criterion / Verifier (D2) -----------------------------------------------------------

def test_command_verifier_requires_nonempty_argv():
    with pytest.raises(ValidationError):
        tr.CommandVerifier(argv=())


def test_command_verifier_minimal():
    v = tr.CommandVerifier(argv=("pytest", "-x"))
    assert v.kind == tr.VerifierKind.command
    assert v.expected_result == "exit_zero"


def test_review_verifier_requires_all_three_fields():
    with pytest.raises(ValidationError):
        tr.ReviewVerifier(rubric="x", evidence_required="y")  # reviewer_role missing


def test_unresolved_verifier_requires_reason():
    with pytest.raises(ValidationError):
        tr.UnresolvedVerifier(reason="")


def test_criterion_supports_close_false_for_unresolved():
    c = tr.Criterion(id="c1", requirement="x",
                      verifier=tr.UnresolvedVerifier(reason="not classified"))
    assert c.supports_close is False


def test_criterion_supports_close_true_for_command():
    c = tr.Criterion(id="c1", requirement="x",
                      verifier=tr.CommandVerifier(argv=("true",)))
    assert c.supports_close is True


def test_criterion_discriminates_verifier_kind_from_dict():
    """D2's whole point: a criterion's verifier is a DISCRIMINATED union, not a blob —
    round-tripping through plain dicts (as the converter and any JSON store must) keeps
    the concrete type, not a base class."""
    c = tr.Criterion.model_validate({
        "id": "c1", "requirement": "req",
        "verifier": {"kind": "review", "rubric": "r", "evidence_required": "e",
                     "reviewer_role": "architect"},
    })
    assert isinstance(c.verifier, tr.ReviewVerifier)


# --- KillCandidates ------------------------------------------------------------------

def test_kill_candidates_needs_ids_or_none_reason():
    with pytest.raises(ValidationError):
        tr.KillCandidates()


def test_kill_candidates_ids_and_none_reason_are_exclusive():
    with pytest.raises(ValidationError):
        tr.KillCandidates(ids=("#1",), none_reason="x")


def test_kill_candidates_none_reason_alone_is_valid():
    kc = tr.KillCandidates(none_reason="no open row tracks this")
    assert kc.ids == ()


# --- TaskRecord (D1, D4, D9) -----------------------------------------------------------

def test_task_record_rejects_unknown_key():
    with pytest.raises(ValidationError):
        tr.TaskRecord.model_validate({
            "id": "[#1]", "title": "t", "status": "open",
            "kill_candidates": {"none_reason": "x"},
            "totally_unknown_field": True,
        })


def test_task_record_is_frozen():
    rec = tr.TaskRecord(id="[#1]", title="t", status=tr.TaskStatus.open,
                         kill_candidates=tr.KillCandidates(none_reason="x"))
    with pytest.raises(ValidationError):
        rec.title = "changed"


def test_task_record_closure_refuses_unresolved_criteria():
    """D2/D4: an unresolved criterion cannot support a close — a TaskRecord that carries
    both a closure and an unresolved criterion is an illegal transition, refused at
    construction rather than left for a later gate to catch."""
    with pytest.raises(ValidationError):
        tr.TaskRecord(
            id="[#1]", title="t", status=tr.TaskStatus.closed,
            kill_candidates=tr.KillCandidates(none_reason="x"),
            criteria=(tr.Criterion(id="c1", requirement="r",
                                    verifier=tr.UnresolvedVerifier(reason="n/a")),),
            closure=tr.ClosureRecord(commit="deadbeef", definition_digest="abc123"),
        )


def test_task_record_closure_with_resolved_criteria_is_legal():
    rec = tr.TaskRecord(
        id="[#1]", title="t", status=tr.TaskStatus.closed,
        kill_candidates=tr.KillCandidates(none_reason="x"),
        criteria=(tr.Criterion(id="c1", requirement="r",
                                verifier=tr.CommandVerifier(argv=("true",))),),
        closure=tr.ClosureRecord(commit="deadbeef", definition_digest="abc123"),
    )
    assert rec.closure.commit == "deadbeef"


def test_task_record_round_trips_through_json():
    rec = tr.TaskRecord(id="[#1]", title="t", status=tr.TaskStatus.open,
                         kill_candidates=tr.KillCandidates(none_reason="x"),
                         implements=("ADR-122",))
    back = tr.TaskRecord.model_validate_json(rec.model_dump_json())
    assert back == rec


# --- convert_row (the converter, over a synthetic body line) --------------------------

_SYNTH_BODY_COMMAND = (
    '- [#9001] [P2][S] **Synthetic row** - some narrative text · Done when: the thing '
    'holds -- `grep -q "x" some/file.md` · implements: ADR-122 · depends-on: #42 · '
    'serialize-group: fake-group · refs some/other.md · kill-candidates: none -- nothing '
    'tracks this yet'
)

_SYNTH_BODY_PROSE = (
    '- [#9002] [P3][M] **Prose-only row** - narrative · Done when: someone reviews it and '
    'agrees · kill-candidates: #9001'
)


def test_convert_row_classifies_command_verifier_and_known_clauses():
    rec = tr.convert_row(9001, _SYNTH_BODY_COMMAND, theme="[E4] Decision management",
                          story="[S11] Keep it navigable", frontmatter_status=None)
    assert rec.id == "[#9001]"
    assert rec.status == tr.TaskStatus.open
    assert rec.implements == ("ADR-122",)
    assert rec.depends_on == ("#42",)
    assert rec.serialize_group == ("fake-group",)
    assert len(rec.criteria) == 1
    v = rec.criteria[0].verifier
    assert isinstance(v, tr.CommandVerifier)
    assert v.argv[:2] == ("grep", "-q")
    assert rec.kill_candidates.none_reason is not None
    assert rec.theme_id == "E4"
    assert rec.story_id == "S11"


def test_convert_row_prose_done_when_is_unresolved_with_reason():
    rec = tr.convert_row(9002, _SYNTH_BODY_PROSE, theme=None, story=None,
                          frontmatter_status=None)
    assert len(rec.criteria) == 1
    v = rec.criteria[0].verifier
    assert isinstance(v, tr.UnresolvedVerifier)
    assert v.reason  # non-empty — operator question 2's "why unclassified" trail
    # A kill-candidates value naming an id (not "none") is D3's OTHER classified shape —
    # `KillCandidates.ids`, not legacy_body.
    assert rec.kill_candidates == tr.KillCandidates(ids=("#9001",))
    assert rec.legacy_body is None


def test_convert_row_preserves_an_uncaptured_clause_in_legacy_body():
    """HIGH finding, codex terra review of this lane: a clause D1-D9 names no field for
    (e.g. `routine:`) must land in legacy_body, not vanish."""
    body = ('- [#9004] [P2][S] **x** - text · Done when: it holds -- `true` · '
            'routine: consumer=foo path=bar/baz.py')
    rec = tr.convert_row(9004, body, theme=None, story=None, frontmatter_status=None)
    assert rec.legacy_body is not None
    assert "routine:" in rec.legacy_body


def test_convert_row_terminal_status_preserved_from_frontmatter():
    body = '- [#9003] [P2][S] **Closed row** - text · Done when: it shipped -- `true`'
    rec = tr.convert_row(9003, body, theme=None, story=None, frontmatter_status="closed")
    assert rec.status == tr.TaskStatus.closed


def test_convert_row_no_unexplained_field_difference_vs_gen_task_tree_derivers():
    """The converter must not silently disagree with the derivers gen_task_tree.py
    already uses as the source-of-truth oracle for priority/size/title."""
    import gen_task_tree as gtt
    rec = tr.convert_row(9001, _SYNTH_BODY_COMMAND, theme=None, story=None,
                          frontmatter_status=None)
    assert rec.priority == gtt.derive_priority(_SYNTH_BODY_COMMAND)
    assert rec.size == gtt.derive_size(_SYNTH_BODY_COMMAND)
    assert rec.title == gtt.derive_title(_SYNTH_BODY_COMMAND)


# --- convert_archive_record ------------------------------------------------------------

_SYNTH_ARCHIVE = """---
id: "[#9099]"
row: tasks/9099-synthetic.md
record: row-body-archival
schema: 1
events: 1
pointer: "**Archived annotations:** `tasks/archive/9099.md`"
---

# Archived row annotations — [#9099]

Some narration body, verbatim.
"""


def test_convert_archive_record_preserves_id_and_marks_legacy_body():
    rec = tr.convert_archive_record(_SYNTH_ARCHIVE)
    assert rec.id == "[#9099]"
    assert rec.row == "tasks/9099-synthetic.md"
    assert rec.schema_number == 1
    assert rec.events == 1
    assert "Some narration body, verbatim." in rec.legacy_body


# --- CLI surface (D9): show / list --json / check over a scratch record file ----------

def test_cli_show_prints_json_for_a_synthetic_body(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "row.txt").write_text(_SYNTH_BODY_COMMAND, encoding="utf-8")
    rc = tr.main(["show", "--body-file", "row.txt", "--id", "9001"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["id"] == "[#9001]"


def test_cli_check_refuses_a_record_with_unresolved_closure(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({
        "id": "[#1]", "title": "t", "status": "closed",
        "kill_candidates": {"none_reason": "x"},
        "criteria": [{"id": "c1", "requirement": "r",
                       "verifier": {"kind": "unresolved", "reason": "n/a"}}],
        "closure": {"commit": "deadbeef", "definition_digest": "abc"},
    }), encoding="utf-8")
    rc = tr.main(["check", "--record", str(bad)])
    assert rc == 1


def test_cli_new_refuses_a_record_path_inside_tasks_dir(tmp_path, monkeypatch):
    """CRITICAL finding, codex terra review of this lane: the write verbs must never
    be able to land a scratch record inside the live tasks/ tree — ADR-122 step 1
    explicitly does not flip the source of truth."""
    monkeypatch.setattr(tr, "_TASKS_DIR", tmp_path / "tasks")
    (tmp_path / "tasks").mkdir()
    target = tmp_path / "tasks" / "sneaky.json"
    rc = tr.main(["new", "--record", str(target), "--id", "[#1]", "--title", "t",
                  "--kill-candidates-none", "x"])
    assert rc == 1
    assert not target.exists()


def test_cli_set_refuses_a_record_path_inside_tasks_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(tr, "_TASKS_DIR", tmp_path / "tasks")
    (tmp_path / "tasks").mkdir()
    target = tmp_path / "tasks" / "sneaky.json"
    target.write_text('{"id": "[#1]"}', encoding="utf-8")
    rc = tr.main(["set", "--record", str(target), "--field", 'title="x"'])
    assert rc == 1


def test_cli_close_refuses_a_record_path_inside_tasks_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(tr, "_TASKS_DIR", tmp_path / "tasks")
    (tmp_path / "tasks").mkdir()
    target = tmp_path / "tasks" / "sneaky.json"
    target.write_text('{"id": "[#1]"}', encoding="utf-8")
    rc = tr.main(["close", "--record", str(target), "--commit", "deadbeef",
                  "--definition-digest", "abc"])
    assert rc == 1


def test_cli_new_writes_outside_tasks_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(tr, "_TASKS_DIR", tmp_path / "tasks")
    target = tmp_path / "scratch" / "rec.json"
    target.parent.mkdir()
    rc = tr.main(["new", "--record", str(target), "--id", "[#1]", "--title", "t",
                  "--kill-candidates-none", "x"])
    assert rc == 0
    assert json.loads(target.read_text(encoding="utf-8"))["id"] == "[#1]"


def test_cli_set_then_close_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(tr, "_TASKS_DIR", tmp_path / "tasks")
    target = tmp_path / "rec.json"
    target.write_text(tr.TaskRecord(
        id="[#1]", title="t", status=tr.TaskStatus.open,
        kill_candidates=tr.KillCandidates(none_reason="x"),
        criteria=(tr.Criterion(id="c1", requirement="r",
                                verifier=tr.CommandVerifier(argv=("true",))),),
    ).model_dump_json(), encoding="utf-8")
    assert tr.main(["set", "--record", str(target), "--field", 'title="renamed"']) == 0
    assert json.loads(target.read_text(encoding="utf-8"))["title"] == "renamed"
    assert tr.main(["close", "--record", str(target), "--commit", "deadbeef",
                     "--definition-digest", "abc"]) == 0
    assert json.loads(target.read_text(encoding="utf-8"))["status"] == "closed"


def test_cli_check_accepts_a_well_formed_record(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(json.dumps({
        "id": "[#1]", "title": "t", "status": "open",
        "kill_candidates": {"none_reason": "x"},
    }), encoding="utf-8")
    rc = tr.main(["check", "--record", str(good)])
    assert rc == 0
