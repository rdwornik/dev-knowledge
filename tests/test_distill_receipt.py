"""Tests for the [#1535] distiller front stage -- `DistillReceipt` and `gen_lane_contract distill --row`.

[#1535] Done-when (5): the distiller reads a phased `tasks/` row, scores every NEW path in a
plan against the organ index and `why`, and emits a `DistillReceipt` that REFUSES a NEW path
with a reuse candidate unless it carries a NEW-JUSTIFIED line AND a CHALLENGE from a vendor
other than the producer. An unphased row is refused (exit 1). The receipt schema is a
generated file that `--check` holds byte-equal to the model.

Done-when (6) is covered by `tests/test_challenge_receipt.py`; the nested `challenge` here is
built from a dict, never from a live reviewer.

Every new symbol is imported INSIDE a helper or test, so a missing module or attribute fails
that one test, not the collection of the file.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import gen_lane_contract as glc  # noqa: E402

BASELINE = ["C-TASK", "C-SCOPE", "C-RED", "C-VENDOR", "C-CLEAN"]
SHA = "a" * 64
NEW_PATH = "scripts/read_gate_v2.py"

_FRONT = '---\nid: "[#4242]"\ntitle: "Read gate v2"\nstatus: open\npriority: P2\nsize: S\n---\n\n'
_LINE = ("- [#4242] [P2][S] **Read gate v2** - widen the read gate "
         "· touches: `scripts/x.py`, tests{phase} · Done when: (1) it works\n")


def _write_row(root: Path, phase: str | None) -> Path:
    tasks = root / "tasks"
    tasks.mkdir(parents=True, exist_ok=True)
    clause = f" · phase: {phase}" if phase else ""
    path = tasks / "4242-some-slug.md"
    path.write_text(_FRONT + _LINE.format(phase=clause), encoding="utf-8")
    return path


def _challenge_dict(reviewer: str | None = "openai", producer: str = "anthropic",
                    verdict: str = "AGREE") -> dict:
    return {
        "schema": "challenge-receipt/1", "idea_sha256": SHA, "title": "read gate v2",
        "proposes": NEW_PATH, "verdict": verdict,
        "row_state": "proceed" if verdict in ("AGREE", "AMEND") else "INPUT_REQUIRED",
        "producer_vendor": producer, "reviewer_vendor": reviewer,
        "served_model": "gpt-5" if reviewer == "openai" else None, "nonce": "n" * 16,
    }


def _receipt_dict(**over) -> dict:
    base = {
        "schema": "distill-receipt/1", "row": "4242", "row_phase": "task", "title": "Read gate v2",
        "reuse_candidates": [{"path": "scripts/read_gate.py", "source": "why", "score": 0.67,
                              "matched": NEW_PATH}],
        "reuse_threshold": 0.5, "constraints": list(BASELINE), "boosted_prompt": "do the thing",
        "plan_new_paths": [NEW_PATH], "new_justified": None, "producer_vendor": "anthropic",
        "challenge": None,
    }
    base.update(over)
    return base


def _receipt_cls():
    from ecosystem.schema.distill_receipt import DistillReceipt
    return DistillReceipt


# --- load_task_row / require_phased ------------------------------------------------------------

def test_load_task_row_reads_a_tmp_tasks_dir(tmp_path):
    _write_row(tmp_path, "task")
    row = glc.load_task_row(tmp_path, "4242")
    assert "4242" in row.id
    assert "Read gate v2" in row.title
    assert row.phase == "task"
    assert "scripts/x.py" in row.touches
    assert "tests" in row.touches
    assert row.path.name == "4242-some-slug.md"


def test_load_task_row_missing_row_is_refused(tmp_path):
    _write_row(tmp_path, "task")
    with pytest.raises(glc.DistillRefused):
        glc.load_task_row(tmp_path, "999999")


def test_load_task_row_without_phase_clause_has_phase_none(tmp_path):
    _write_row(tmp_path, None)
    assert glc.load_task_row(tmp_path, "4242").phase is None


def test_require_phased_refuses_an_unphased_row(tmp_path):
    _write_row(tmp_path, None)
    row = glc.load_task_row(tmp_path, "4242")
    with pytest.raises(glc.DistillRefused, match="(?i)unphased"):
        glc.require_phased(row)


def test_require_phased_accepts_task_and_build(tmp_path):
    for phase in ("task", "build"):
        _write_row(tmp_path, phase)
        glc.require_phased(glc.load_task_row(tmp_path, "4242"))


def test_require_phased_refuses_an_unknown_phase(tmp_path):
    _write_row(tmp_path, "epic")
    with pytest.raises(glc.DistillRefused):
        glc.require_phased(glc.load_task_row(tmp_path, "4242"))


# --- organ index + similarity ------------------------------------------------------------------

def test_organ_index_entries_parses_the_real_index_and_finds_decide():
    text = (_REPO_ROOT / "ecosystem" / "organ-index.md").read_text(encoding="utf-8")
    entries = glc.organ_index_entries(text)
    assert len(entries) > 10
    by_name = dict(entries)
    assert "/decide" in by_name
    assert by_name["/decide"].endswith(".claude/commands/decide.md")


def test_organ_index_entries_parses_a_tiny_fixture_table():
    text = ("| Name | Class | Trigger | Source | Distribution | Status |\n|---|---|---|---|---|---|\n"
            "| `/widget` | command | operator-invoke | `.claude/commands/widget.md` | hub | ARMED |\n")
    assert ("/widget", ".claude/commands/widget.md") in glc.organ_index_entries(text)


def test_tokens_lowercases_and_drops_stopwords():
    assert glc.tokens("Scripts/Read_Gate.py") == frozenset({"read", "gate"})
    assert glc.tokens("the tests of a command") == frozenset()


def test_similarity_is_jaccard_and_zero_on_empty():
    assert glc.similarity("read_gate_v2", "read_gate") == pytest.approx(2 / 3)
    assert glc.similarity("alpha", "beta") == 0.0
    assert glc.similarity("", "beta") == 0.0
    assert glc.similarity("the", "the") == 0.0


def test_reuse_candidates_finds_read_gate_for_read_gate_v2(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "read_gate.py").write_text("# existing\n", encoding="utf-8")
    (tmp_path / "scripts" / "unrelated_thing.py").write_text("# other\n", encoding="utf-8")
    cands = glc.reuse_candidates(
        tmp_path, [NEW_PATH], title="widen the gate", organ_index_text="",
        why=lambda p: "reads the gate" if p.endswith("read_gate.py") else None)
    hit = [c for c in cands if c.path == "scripts/read_gate.py"]
    assert hit, f"scripts/read_gate.py not among {[c.path for c in cands]}"
    assert hit[0].source == "why"
    assert hit[0].matched == NEW_PATH
    assert hit[0].score == pytest.approx(2 / 3, abs=0.01)
    assert hit[0].purpose == "reads the gate"
    assert not [c for c in cands if c.path == "scripts/unrelated_thing.py"]
    assert [c.score for c in cands] == sorted((c.score for c in cands), reverse=True)


def test_reuse_candidates_scores_organ_index_entries(tmp_path):
    text = ("| Name | Class | Trigger | Source | Distribution | Status |\n|---|---|---|---|---|---|\n"
            "| `read_gate` | hook | pre-commit | `scripts/read_gate.py` | hub | ARMED |\n")
    cands = glc.reuse_candidates(tmp_path, [NEW_PATH], organ_index_text=text, why=lambda p: None)
    assert any(c.source == "organ-index" and c.matched == NEW_PATH and c.score > 0.5
               for c in cands)


# --- DistillReceipt ----------------------------------------------------------------------------

def test_receipt_refuses_a_new_path_with_a_candidate_and_no_justification():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(_receipt_dict())


def test_receipt_refuses_justified_but_challenge_from_the_producers_own_vendor():
    from pydantic import ValidationError
    # the challenge is itself valid (producer openai, reviewer anthropic); the DISTILL producer
    # is anthropic, so this reviewer is the distill producer's own vendor
    data = _receipt_dict(new_justified="the old gate cannot be widened",
                         challenge=_challenge_dict(reviewer="anthropic", producer="openai"))
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(data)


def test_receipt_refuses_justified_without_any_challenge():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(_receipt_dict(new_justified="because"))


def test_receipt_accepts_justified_plus_an_agreeing_challenge_from_another_vendor():
    receipt = _receipt_cls().model_validate(
        _receipt_dict(new_justified="the old gate cannot be widened", challenge=_challenge_dict()))
    assert receipt.row_state == "ready"
    assert receipt.challenge.reviewer_vendor == "openai"
    assert receipt.model_dump(by_alias=True)["schema"] == "distill-receipt/1"


def test_receipt_accepts_a_new_path_below_the_reuse_threshold():
    cands = [{"path": "scripts/read_gate.py", "source": "why", "score": 0.3, "matched": NEW_PATH}]
    assert _receipt_cls().model_validate(_receipt_dict(reuse_candidates=cands))


def test_receipt_accepts_a_new_path_with_no_candidate():
    assert _receipt_cls().model_validate(_receipt_dict(reuse_candidates=[]))


@pytest.mark.parametrize("missing", BASELINE)
def test_receipt_refuses_constraints_missing_a_baseline_id(missing):
    from pydantic import ValidationError
    data = _receipt_dict(reuse_candidates=[], constraints=[c for c in BASELINE if c != missing])
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(data)


def test_receipt_refuses_empty_constraints():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(_receipt_dict(reuse_candidates=[], constraints=[]))


# --- CLI ---------------------------------------------------------------------------------------

def test_cli_distill_row_on_an_unphased_row_exits_1(tmp_path, monkeypatch):
    # cmd_distill derives repo_root = _SCRIPTS.parent and the spec adds no --repo-root option,
    # so the tmp repo is selected by pointing the module's _SCRIPTS at <tmp>/scripts.
    (tmp_path / "scripts").mkdir()
    _write_row(tmp_path, None)
    monkeypatch.setattr(glc, "_SCRIPTS", tmp_path / "scripts")
    result = CliRunner().invoke(glc.cli, ["distill", "--row", "4242"])
    assert result.exit_code == 1, result.output
    assert "unphased" in result.output.lower()


# --- schema file -------------------------------------------------------------------------------

def test_distill_schema_file_is_current():
    from ecosystem.schema import distill_receipt
    assert distill_receipt.main(["--check"]) == 0
    assert (_REPO_ROOT / "ecosystem" / "schema" / "distill-receipt.schema.json").is_file()


# --- round-2 RED (reviewer terra): a challenge justifies only the path it proposes --------------

SECOND_PATH = "scripts/other_gate_v2.py"


def test_receipt_refuses_an_agreeing_challenge_that_proposes_a_different_path():
    from pydantic import ValidationError
    challenge = _challenge_dict()
    challenge["proposes"] = "scripts/something_else.py"
    data = _receipt_dict(new_justified="the old gate cannot be widened", challenge=challenge)
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(data)


def test_receipt_refuses_two_conflicting_new_paths_when_the_challenge_proposes_only_one():
    from pydantic import ValidationError
    cands = [
        {"path": "scripts/read_gate.py", "source": "why", "score": 0.67, "matched": NEW_PATH},
        {"path": "scripts/other_gate.py", "source": "why", "score": 0.7, "matched": SECOND_PATH},
    ]
    data = _receipt_dict(reuse_candidates=cands, plan_new_paths=[NEW_PATH, SECOND_PATH],
                         new_justified="neither old gate can be widened",
                         challenge=_challenge_dict())  # proposes == NEW_PATH only
    with pytest.raises(ValidationError):
        _receipt_cls().model_validate(data)
