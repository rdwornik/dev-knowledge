"""RED-first witnesses: a `dispatch.py repair` launch leaves a LAUNCH receipt the merge gate accepts.

Measured defects (see the lane SESSION file): the repair OVERWROTE the lane's first-launch receipt
(`LAUNCH-<SLUG>.json`, job and kind lost) and wrote only under the verb's own receipts dir, not under
the lane worktree's `logs/receipts` that the gate's default lookup reads.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import dispatch as d
import subst_gate as sg

SLUG = "lane-repair-r"
BATCH = "E2.1"


@pytest.fixture
def primary_receipts(tmp_path, monkeypatch):
    target = tmp_path / "primary" / "logs" / "receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


@pytest.fixture
def repo_root(tmp_path):
    root = tmp_path / "repo"
    (root / ".claude" / "worktrees" / SLUG).mkdir(parents=True)
    return root


class _Spawn:
    def __init__(self, job):
        self.job = job

    def __call__(self, argv, env, cwd, log_path=None):
        return d.Spawned(returncode=0, stdout=f"backgrounded {self.job}\n", pid=1)


class _Prelaunch:
    def __call__(self, request, repair=False):
        return d.PreLaunch(True, "")


def _launch(tmp_path, primary_receipts):
    contract = tmp_path / "LANE.md"
    contract.write_text("# LANE\n", encoding="utf-8")
    request = d.LaunchRequest(slug=SLUG, provider="anthropic", model="claude-sonnet-5-5", effort="medium",
                              permission_mode="bypassPermissions", contract=contract, batch=BATCH)
    result = d.LaunchResult(slug=SLUG, provider="anthropic", model_requested=request.model,
                            model_reported=d.MODEL_PENDING, job_id="07f32b10", worktree="w",
                            session_name=SLUG, pid=1, argv=["claude"])
    d._write_launch_records(request, result)
    return contract


def _repair(tmp_path, repo_root, contract, job="faffac9a"):
    request = d.RepairRequest(slug=SLUG, attempt=2, model="claude-sonnet-5-5", effort="medium",
                              contract=contract, batch=BATCH)
    d.repair_lane(request, repo_root=repo_root, spawn=_Spawn(job), environ={}, prelaunch=_Prelaunch())
    return repo_root / ".claude" / "worktrees" / SLUG


def test_a_repair_keeps_the_first_launch_receipt_content(tmp_path, repo_root, primary_receipts):
    contract = _launch(tmp_path, primary_receipts)
    _repair(tmp_path, repo_root, contract)

    body = json.loads((primary_receipts / f"LAUNCH-{SLUG.upper()}.json").read_text(encoding="utf-8"))
    assert body["organ"] == "launch" and body["kind"] == "repair" and body["batch"] == BATCH
    first, = [h for h in body["launches"] if h["job_id"] == "07f32b10"]
    assert first["kind"] == "launch"
    assert (primary_receipts / "LAUNCH-JOB-07f32b10.json").is_file()
    assert (primary_receipts / "LAUNCH-JOB-faffac9a.json").is_file()


def test_the_gate_accepts_the_repair_receipt_from_the_primary_dir(tmp_path, repo_root, primary_receipts):
    contract = _launch(tmp_path, primary_receipts)
    _repair(tmp_path, repo_root, contract)

    assert sg.launch_receipt_problems(primary_receipts.parent.parent, SLUG, BATCH) == []


def test_the_gate_default_lookup_for_the_lane_worktree_finds_the_repair_receipt(
        tmp_path, repo_root, primary_receipts):
    contract = _launch(tmp_path, primary_receipts)
    tree = _repair(tmp_path, repo_root, contract)

    assert sg.launch_receipt_problems(tree, SLUG, BATCH) == []
    body = json.loads((tree / "logs" / "receipts" / f"LAUNCH-{SLUG.upper()}.json").read_text(encoding="utf-8"))
    assert body["kind"] == "repair" and body["job_id"] == "faffac9a"
