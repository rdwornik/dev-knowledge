"""RED-first witnesses for the substitution gate at the landing path (`merge_path.land`).

For an applicable batch (`subst_gate.batch_applies`) `land` refuses BEFORE any push when the handback
carries no MODELS block, a served model differs from the requested one without a VENDOR-FAIL, or no
launch receipt exists. A batch the gate does not apply to lands exactly as before.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from click.testing import CliRunner

import merge_path as mp

BASE = "b" * 40
TIP = "a" * 40
BATCH = "E2.0"
SLUG = "m"
SONNET = "claude-sonnet-5-5"

GOOD = "MODELS:\n  implement: requested=copilot/default served=claude-sonnet-5.5\n"
SUBSTITUTED = f"MODELS:\n  implement: requested={SONNET}/high served=claude-opus-5-5\n"
VENDOR_FAIL_LINE = f"  implement: requested={SONNET}/high served=claude-opus-5-5 VENDOR-FAIL: implement INC-7"


@dataclass
class _Verdict:
    state: str = "PASS"
    reason: str = ""
    missing_contexts: tuple = ()
    new_reds: tuple = ()

    def to_dict(self):
        return {"state": self.state}


@dataclass
class Rig:
    calls: list = field(default_factory=list)

    def git(self, args):
        self.calls.append(list(args))
        if args[0] == "rev-list":
            return 0, f"{TIP} {BASE} {'c' * 40}"
        if args[0] == "ls-remote":
            return 0, f"{BASE}\trefs/heads/main"
        if args[0] == "push":
            return 0, ""
        return 1, "unexpected"

    def pushes(self):
        return [c for c in self.calls if c[0] == "push"]


@pytest.fixture
def receipts_dir(tmp_path, monkeypatch):
    target = tmp_path / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


def _handback(tmp_path, models: str) -> Path:
    path = tmp_path / "handback.json"
    path.write_text(json.dumps({"models": models}), encoding="utf-8")
    return path


def _local_receipt(receipts_dir: Path, batch=BATCH):
    receipts_dir.mkdir(parents=True, exist_ok=True)
    (receipts_dir / f"LAUNCH-{SLUG.upper()}.json").write_text(
        json.dumps({"organ": "launch", "batch": batch}), encoding="utf-8")


def _land(tmp_path, rig, *, batch=BATCH, **kw):
    return mp.land(tmp_path, slug=SLUG, batch=batch, sha=TIP, base=BASE, git=rig.git,
                   verdict_fn=lambda sha, **k: _Verdict(), record_push_fn=lambda root, **k: None,
                   record_suite_fn=lambda root, **k: None, **kw)


# --- refused, before any push -------------------------------------------------------------------

def test_a_handback_with_no_models_block_is_refused_and_nothing_is_pushed(tmp_path, receipts_dir):
    _local_receipt(receipts_dir)
    rig = Rig()

    result = _land(tmp_path, rig, handback=_handback(tmp_path, "HANDBACK m @ abc"))

    assert not result.landed and result.state == "SUBST-GATE-REFUSED"
    assert "REFUSED [models-block]" in result.reason
    assert rig.pushes() == []


def test_no_handback_at_all_is_refused_for_an_applicable_batch(tmp_path, receipts_dir):
    _local_receipt(receipts_dir)
    rig = Rig()

    result = _land(tmp_path, rig, handback=None)

    assert result.state == "SUBST-GATE-REFUSED" and rig.pushes() == []


def test_a_served_model_that_differs_without_vendor_fail_is_refused(tmp_path, receipts_dir):
    _local_receipt(receipts_dir)
    rig = Rig()

    result = _land(tmp_path, rig, handback=_handback(tmp_path, SUBSTITUTED))

    assert not result.landed and result.state == "SUBST-GATE-REFUSED"
    assert "implement" in result.reason and rig.pushes() == []


def test_a_matching_block_with_no_launch_receipt_is_refused(tmp_path, receipts_dir):
    rig = Rig()

    result = _land(tmp_path, rig, handback=_handback(tmp_path, GOOD))

    assert not result.landed and result.state == "SUBST-GATE-REFUSED"
    assert "REFUSED [launch-receipt]" in result.reason
    assert rig.pushes() == []


# --- accepted -----------------------------------------------------------------------------------

def test_a_substitution_with_vendor_fail_lands_and_is_carried_on_the_result(tmp_path, receipts_dir):
    _local_receipt(receipts_dir)
    rig = Rig()

    result = _land(tmp_path, rig, handback=_handback(tmp_path, "MODELS:\n" + VENDOR_FAIL_LINE + "\n"))

    assert result.landed
    assert any("VENDOR-FAIL: implement INC-7" in line for line in result.substitutions)


def test_a_matching_block_and_a_local_launch_receipt_lands(tmp_path, receipts_dir):
    _local_receipt(receipts_dir)
    rig = Rig()

    result = _land(tmp_path, rig, handback=_handback(tmp_path, GOOD))

    assert result.landed and result.state == "PASS"
    assert len(rig.pushes()) == 2


def test_a_matching_block_and_a_codespace_receipt_row_lands(tmp_path, receipts_dir):
    ledger = tmp_path / "logs" / "CODESPACE-RECEIPTS.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(json.dumps({"slug": SLUG, "batch": BATCH}) + "\n", encoding="utf-8")

    result = _land(tmp_path, Rig(), handback=_handback(tmp_path, GOOD))

    assert result.landed


def test_the_gate_refuses_a_malformed_batch(tmp_path, receipts_dir):
    rig = Rig()

    result = _land(tmp_path, rig, batch="Y", handback=None)

    assert not result.landed and result.state == "SUBST-GATE-REFUSED"
    assert "REFUSED [batch-grammar]" in result.reason and rig.pushes() == []


# --- CLI ----------------------------------------------------------------------------------------

def test_the_land_verb_offers_a_handback_option():
    out = CliRunner().invoke(mp.cli, ["land", "--help"])
    assert out.exit_code == 0
    assert "--handback" in out.output
