from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_TESTS = Path(__file__).resolve().parent
for _path in (str(_REPO), str(_REPO / "scripts"), str(_TESTS)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from ecosystem.schema import phase_receipt  # noqa: E402
from scripts import run_phase  # noqa: E402
import test_conductor_run as lane_tests  # noqa: E402


_NOW = "2026-11-02T00:00:00Z"


def _phase_run() -> run_phase.PhaseRun:
    return run_phase.PhaseRun(
        status="ok", exit_code=0, killed=False, targeted=(), survivors=(),
        started_at=_NOW, finished_at=_NOW, duration_ms=1, payload=None,
        payload_sha256=None, reason="",
    )


def _receipt_kwargs() -> dict:
    return {
        "organ": "phase:P1",
        "row": "1856",
        "lane": "head-sha-test",
        "phase": "P1",
        "round_no": 1,
        "argv": [sys.executable, "-c", "pass"],
        "input_hash": "a" * 64,
        "nonce": "nonce-00000000",
        "inputs": [],
    }


def test_item1r_real_doit_receipts_capture_the_head_before_each_phase_spawn(tmp_path):
    assert callable(lane_tests.conductor.run_lane)
    world = lane_tests._world(tmp_path)

    result = lane_tests._run_lane(world)

    assert result.verdict == "ACCEPT"
    heads = {
        item["phase"]: item["head_sha"]
        for item in (json.loads(line) for line in
                     (world["markers"] / "heads.jsonl").read_text(encoding="utf-8").splitlines())
    }
    for phase in lane_tests._PHASE_IDS:
        receipt = lane_tests._phase_receipt(world, phase)
        assert receipt["head_sha"] == heads[phase], phase
    base = lane_tests._git(world["repo"], "rev-parse", "origin/main").stdout.strip()
    red_commit = json.loads(
        (lane_tests._round_dir(world) / "COMMIT-red.json").read_text(encoding="utf-8")
    )["sha"]
    assert lane_tests._phase_receipt(world, "P2")["head_sha"] == base
    assert lane_tests._phase_receipt(world, "P3")["head_sha"] == red_commit


def test_item1r_build_receipt_defaults_and_legacy_receipts_validate():
    receipt = run_phase.build_receipt(_phase_run(), **_receipt_kwargs(), head_sha=None)

    assert receipt.head_sha is None
    old = receipt.model_dump(by_alias=True)
    old.pop("head_sha")
    assert phase_receipt.PhaseReceipt.model_validate(old).head_sha is None


def test_item1r_generated_schema_includes_head_sha():
    assert "head_sha" in phase_receipt.PhaseReceipt.model_fields
    assert "head_sha" in phase_receipt.json_schema()["properties"]
    assert phase_receipt.SCHEMA_FILE.read_text(encoding="utf-8") == phase_receipt.render_json_schema()


def test_item1r_non_git_phase_root_records_none_head_sha(tmp_path):
    world = lane_tests._world(tmp_path, initialize_git=False)
    harness = lane_tests._make_round_harness(world)

    result = lane_tests._run_round(world, harness)

    assert (result.verdict, result.exit_code) == ("ACCEPT", 0)
    for phase in lane_tests._PHASE_IDS:
        assert lane_tests._phase_receipt(world, phase)["head_sha"] is None
