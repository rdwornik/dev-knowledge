"""Tests for the [#1535] CHALLENGE sub-stage -- `ChallengeReceipt` and `gen_lane_contract.challenge`.

[#1535] Done-when (6) (R76): an idea that proposes an organ the index already holds is a
DISAGREE with row_state INPUT_REQUIRED, decided by the harness with no reviewer launched; a
non-duplicate idea passes ONLY on a fresh, nonce-matched payload from a reviewer of another
vendor; no reachable reviewer is INPUT_REQUIRED, never a pass; a matrix with an uncited score
above 3 is refused. Done-when (5) is covered by `tests/test_distill_receipt.py`.

The fake reviewer is a python script that writes a valid payload to $PHASE_PAYLOAD (temp name,
then os.replace) and then sleeps 600 s -- it never exits, so a COMPLETE verdict also proves the
adapter harvests the payload and kills the tree.

Every new symbol is imported INSIDE a helper or test, so a missing module fails that one test.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import gen_lane_contract as glc  # noqa: E402

SHA = "b" * 64
ORGAN_INDEX = (_REPO_ROOT / "ecosystem" / "organ-index.md").read_text(encoding="utf-8")

_FAKE_REVIEWER = textwrap.dedent('''
    import json, os, time
    path = os.environ["PHASE_PAYLOAD"]
    body = {"nonce": os.environ["PHASE_NONCE"], "input_hash": os.environ["PHASE_INPUT_HASH"],
            "verdict": "AGREE", "reasons": ["no existing organ covers this"]}
    with open(path + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(body, fh)
    os.replace(path + ".tmp", path)
    time.sleep(600)
''')

_CITED_MATRIX = """Weights: a=50 b=50

| Option | a | b | Σ |
|---|---|---|---|
| X | 4[^1] | 3 | 3.50 |

[^1]: measured -- run 123, jobs/1/log.txt:5
"""
_UNCITED_MATRIX = """Weights: a=50 b=50

| Option | a | b | Σ |
|---|---|---|---|
| X | 4 | 3 | 3.50 |
"""


def _idea(proposes: str = "zebra-quux-frobnicator") -> str:
    return f"title: A fresh idea\nproposes: {proposes}\nclass: decision\n\nbody text\n"


def _fake(tmp_path: Path) -> Path:
    script = tmp_path / "fake_reviewer.py"
    script.write_text(_FAKE_REVIEWER, encoding="utf-8")
    return script


def _run(tmp_path, idea, reviewers, **kw):
    kw.setdefault("timeout_s", 10)
    return glc.challenge(idea, producer_vendor="anthropic", organ_index_text=ORGAN_INDEX,
                         reviewers=reviewers, work_dir=tmp_path, **kw)


def _receipt_dict(**over) -> dict:
    base = {"schema": "challenge-receipt/1", "idea_sha256": SHA, "title": "t", "proposes": "x",
            "verdict": "AGREE", "row_state": "proceed", "producer_vendor": "anthropic",
            "reviewer_vendor": "openai", "served_model": None, "nonce": "n" * 16}
    base.update(over)
    return base


def _cls():
    from ecosystem.schema.challenge_receipt import ChallengeReceipt
    return ChallengeReceipt


# --- challenge(): behaviour --------------------------------------------------------------------

def test_duplicate_of_an_existing_organ_is_a_deterministic_disagree(tmp_path):
    receipt = _run(tmp_path, _idea("/decide"), reviewers=[])
    assert receipt.verdict == "DISAGREE"
    assert receipt.row_state == "INPUT_REQUIRED"
    assert receipt.duplicates
    assert receipt.reviewer_vendor == "harness"
    assert any("decide" in d for d in receipt.duplicates)


def test_non_duplicate_idea_with_a_fake_reviewer_agrees(tmp_path):
    script = _fake(tmp_path)
    receipt = _run(tmp_path, _idea(), reviewers=[("openai", [sys.executable, str(script)])])
    assert receipt.verdict == "AGREE"
    assert receipt.row_state == "proceed"
    assert receipt.reviewer_vendor == "openai"
    assert receipt.producer_vendor == "anthropic"
    assert receipt.nonce
    assert not receipt.duplicates


def test_unreachable_reviewers_are_input_required_never_agree(tmp_path):
    receipt = _run(tmp_path, _idea(), reviewers=[("openai", ["no-such-reviewer-cli-xyz"]),
                                                 ("xai", ["no-such-reviewer-cli-xyz2"])])
    assert receipt.verdict == "INPUT_REQUIRED"
    assert receipt.row_state == "INPUT_REQUIRED"
    assert receipt.reviewer_vendor is None


def test_a_reviewer_of_the_producers_own_vendor_is_skipped(tmp_path):
    script = _fake(tmp_path)
    receipt = _run(tmp_path, _idea(), reviewers=[("anthropic", [sys.executable, str(script)])])
    assert receipt.verdict == "INPUT_REQUIRED"
    assert receipt.row_state == "INPUT_REQUIRED"
    assert receipt.reviewer_vendor is None
    assert not (tmp_path / "challenge-anthropic.json").exists()


def test_a_matrix_with_an_uncited_four_is_refused(tmp_path):
    matrix = tmp_path / "matrix.md"
    matrix.write_text(_UNCITED_MATRIX, encoding="utf-8")
    with pytest.raises(glc.DistillRefused, match="unmeasured_cap"):
        _run(tmp_path, _idea(), reviewers=[], matrix_path=matrix)


def test_a_cited_matrix_passes(tmp_path):
    matrix = tmp_path / "matrix.md"
    matrix.write_text(_CITED_MATRIX, encoding="utf-8")
    script = _fake(tmp_path)
    receipt = _run(tmp_path, _idea(), reviewers=[("openai", [sys.executable, str(script)])],
                   matrix_path=matrix)
    assert receipt.verdict == "AGREE"
    assert receipt.matrix_defects == []


# --- ChallengeReceipt: validators --------------------------------------------------------------

def test_receipt_refuses_reviewer_vendor_equal_to_producer_vendor():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _cls().model_validate(_receipt_dict(reviewer_vendor="anthropic"))


def test_receipt_refuses_agree_without_a_reviewer():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _cls().model_validate(_receipt_dict(reviewer_vendor=None))


def test_receipt_refuses_disagree_with_a_proceed_row_state():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _cls().model_validate(_receipt_dict(verdict="DISAGREE", row_state="proceed"))


def test_receipt_refuses_non_empty_matrix_defects():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _cls().model_validate(_receipt_dict(matrix_defects=["decide.unmeasured_cap: X/a"]))


def test_receipt_accepts_input_required_without_a_reviewer():
    receipt = _cls().model_validate(_receipt_dict(
        verdict="INPUT_REQUIRED", row_state="INPUT_REQUIRED", reviewer_vendor=None))
    assert receipt.row_state == "INPUT_REQUIRED"


def test_receipt_accepts_a_valid_agree_from_another_vendor():
    receipt = _cls().model_validate(_receipt_dict())
    assert receipt.model_dump(by_alias=True)["schema"] == "challenge-receipt/1"


# --- schema file -------------------------------------------------------------------------------

def test_challenge_schema_file_is_current():
    from ecosystem.schema import challenge_receipt
    assert challenge_receipt.main(["--check"]) == 0
    assert (_REPO_ROOT / "ecosystem" / "schema" / "challenge-receipt.schema.json").is_file()
