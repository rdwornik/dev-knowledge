"""lane-l8-lane-end: lane_digest -- one plain-language digest from the receipts of a batch.

RED-first (ADR-108 s.B): authored and witnessed FAILING before `scripts/lane_digest.py` existed
(see the RED commit of the lane; these tests were split out of `test_lane_end.py` afterwards so each
script has the test file the impacted-tests guard looks for).
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_DIGEST = _SCRIPTS / "lane_digest.py"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

LANE = "lane-l8-lane-end"


def _mod(name: str):
    return importlib.import_module(name)


def _receipt(organ: str, status: str = "ok", exit_code: int = 0, duration_ms: int = 12) -> dict:
    return {"schema": 1, "organ": organ, "status": status, "exit_code": exit_code,
            "duration_ms": duration_ms, "input_hash": "abc123", "model_requested": None,
            "model_reported": None, "command": ["x"], "output_file": None,
            "finished_at": "2026-09-20T10:00:00+00:00"}


def _write_receipts(receipts: Path, rows: list[dict]) -> None:
    receipts.mkdir(parents=True, exist_ok=True)
    for row in rows:
        (receipts / f"MOMENT-{row['organ'].upper().replace('_', '-')}.json").write_text(
            json.dumps(row), encoding="utf-8")


# --- the digest ---------------------------------------------------------------------------------

def _lane(ld, name, receipts, did=(), cost=None):
    return ld.LaneInput(name=name, receipts=list(receipts), did=list(did), cost_usd=cost)


def test_digest_names_every_lane_and_every_open_item():
    ld = _mod("lane_digest")
    lanes = [
        _lane(ld, "lane-l2-dispatch-guards", [_receipt("lane_cost"), _receipt("gates")],
              did=["guard the dispatch verb"], cost=3.5),
        _lane(ld, "lane-l3-organ-truth",
              [_receipt("lane_cost"), _receipt("gates", "failed", 1),
               _receipt("no_leftovers", "SKIPPED-NOT-BUILT", 0)], did=["fix the organ table"]),
        _lane(ld, "lane-l4-integrator-surface", []),
    ]
    text = ld.render_digest(lanes)
    for name in ("lane-l2-dispatch-guards", "lane-l3-organ-truth", "lane-l4-integrator-surface"):
        assert name in text
    assert "guard the dispatch verb" in text and "fix the organ table" in text
    # every non-ok organ is an open item, in words
    assert "gates" in text and "no leftovers" in text
    # a lane with no receipts is itself an open item
    assert "no receipts" in text.lower()


def test_digest_gives_each_lane_a_verdict_and_a_cost_or_says_none_was_recorded():
    ld = _mod("lane_digest")
    text = ld.render_digest([
        _lane(ld, "lane-a", [_receipt("gates")], cost=12.34),
        _lane(ld, "lane-b", [_receipt("gates", "failed", 1)]),
    ])
    assert "12.34" in text
    assert "not recorded" in text.lower()
    verdicts = ld.verdicts([_lane(ld, "lane-a", [_receipt("gates")]),
                            _lane(ld, "lane-b", [_receipt("gates", "failed", 1)]),
                            _lane(ld, "lane-c", [_receipt("gates", "SKIPPED-NOT-BUILT", 0)])])
    assert verdicts["lane-a"] != verdicts["lane-b"] != verdicts["lane-c"]
    assert len(set(verdicts.values())) == 3


def test_digest_is_plain_language_no_internal_identifiers():
    ld = _mod("lane_digest")
    text = ld.render_digest([_lane(ld, "lane-a", [
        _receipt("gates", "failed", 1), _receipt("digest", "SKIPPED-NOT-BUILT", 0),
        _receipt("transport_report", "SKIPPED-NO-INPUT", 0)])])
    assert "SKIPPED" not in text and "abc123" not in text and ".json" not in text
    assert "exit_code" not in text and "input_hash" not in text


def test_a_receipt_of_an_unrecognised_shape_is_an_open_item_never_dropped(tmp_path):
    ld = _mod("lane_digest")
    receipts = tmp_path / "receipts"
    _write_receipts(receipts, [_receipt("gates")])
    (receipts / "MOMENT-ODD.json").write_text(json.dumps({"status": "ok"}), encoding="utf-8")
    (receipts / "MOMENT-LIST.json").write_text("[1, 2]", encoding="utf-8")
    (receipts / "MOMENT-BROKEN.json").write_text("{not json", encoding="utf-8")
    lane = ld.LaneInput(name="lane-a", receipts=ld.load_receipts(receipts))
    assert ld.verdict(lane) == ld.VERDICT_ATTENTION
    items = ld.open_items(lane)
    assert len(items) == 3 and all("could not be read" in i for i in items)


def test_digest_cli_reads_the_receipts_of_a_batch(tmp_path):
    root = tmp_path / "worktrees"
    _write_receipts(root / "lane-a" / "logs" / "receipts", [_receipt("gates")])
    _write_receipts(root / "lane-b" / "logs" / "receipts", [_receipt("gates", "failed", 1)])
    costs = tmp_path / "LANE-COSTS.jsonl"
    costs.write_text(json.dumps({"slug": "lane-a", "usd": 7.25}) + "\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(_DIGEST), "--root", str(root), "--costs-file", str(costs),
                           "--repo", str(tmp_path)], capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert "lane-a" in proc.stdout and "lane-b" in proc.stdout and "7.25" in proc.stdout


def test_digest_lane_form_is_the_moment_command_and_never_fails_the_lane(tmp_path):
    """`lane_digest.py --lane {lane}` is the command harness.yaml declares."""
    receipts = tmp_path / "receipts"
    _write_receipts(receipts, [_receipt("gates")])
    proc = subprocess.run([sys.executable, str(_DIGEST), "--lane", LANE, "--receipts-dir", str(receipts),
                           "--repo", str(tmp_path), "--costs-file", str(tmp_path / "none.jsonl")],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    assert LANE in proc.stdout
