import json

import dispatch as d
import subst_gate


def test_repair_preserves_first_launch_and_copies_valid_receipt(
    tmp_path, monkeypatch
):
    slug = "test-lane"
    batch = "E2.1"
    first_job_id = "first123"
    receipts_dir = tmp_path / "harness-receipts"
    worktree = tmp_path / ".claude" / "worktrees" / slug
    worktree.mkdir(parents=True)
    receipts_dir.mkdir()
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(receipts_dir))

    contract = tmp_path / "contract.md"
    contract.write_text("Test contract\n", encoding="utf-8")

    launch_request = d.LaunchRequest(
        slug=slug,
        provider="claude",
        model="sonnet",
        effort="medium",
        permission_mode="default",
        contract=contract,
        batch=batch,
    )
    launch_result = d.LaunchResult(
        slug=slug,
        provider="claude",
        model_requested="sonnet",
        model_reported="sonnet",
        job_id=first_job_id,
        worktree=str(worktree),
        session_name="test-session",
        pid=1,
        argv=["claude"],
    )
    d._write_launch_records(launch_request, launch_result)

    repair_request = d.RepairRequest(
        slug=slug,
        attempt=1,
        model="sonnet",
        effort="medium",
        contract=contract,
        batch=batch,
    )
    d.repair_lane(
        repair_request,
        repo_root=tmp_path,
        spawn=lambda argv, env, cwd, log_path=None: d.Spawned(
            returncode=0, stdout="backgrounded deadbeef\n", pid=1
        ),
        environ={},
        prelaunch=lambda request, repair=False: d.PreLaunch(True, ""),
    )

    receipt_path = worktree / "logs" / "receipts" / f"LAUNCH-{slug.upper()}.json"
    assert receipt_path.is_file()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    assert any(
        launch["job_id"] == first_job_id and launch["kind"] == "launch"
        for launch in receipt["launches"]
    )
    assert subst_gate.launch_receipt_problems(
        root=worktree, slug=slug, batch=batch
    ) == []