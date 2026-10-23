from __future__ import annotations

from pathlib import Path


import actions_verdict as av
import merge_receipt as mr

_SINCE = "2026-01-01T00:00:00Z"
_UNTIL = "2026-01-10T00:00:00Z"
_PUSHED_SHA = "a" * 40


def _receipt_with_integration_verdict(root: Path, sha: str) -> None:
    mr.open_receipt(root, slug="reuse", batch="reuse")
    mr.record_push(root, slug="reuse", target="integration",
                   branch="worktree-integrate-reuse", sha=sha, seconds=1.0)
    receipt = mr.load_receipt(root, "reuse")
    receipt.steps.append(mr.StepTiming(
        step="suite",
        step_class=mr.CLASS_TESTS,
        seconds=60.0,
        ok=True,
        returncode=0,
        command="read integration-branch CI",
        started="2026-10-23T10:00:00Z",
        verdict_state=av.STATE_PASS,
        baseline_sha="b" * 40,
    ))
    mr.save_receipt(root, receipt)


def test_main_push_reuses_the_recorded_integration_verdict_without_another_suite_read(
        tmp_path: Path, monkeypatch):
    _receipt_with_integration_verdict(tmp_path, _PUSHED_SHA)

    def unexpected_verdict_read(*_args, **_kwargs):
        raise AssertionError("main push must reuse the integration-branch verdict")

    monkeypatch.setattr(mr._av, "verdict_for", unexpected_verdict_read)
    receipt = mr.record_push(
        tmp_path, slug="reuse", target="main", branch="main", sha=_PUSHED_SHA, seconds=2.0)

    assert receipt.suite_verdict() == av.STATE_PASS
    assert [step.step for step in receipt.steps].count("suite") == 1
    assert receipt.steps[-1].step == mr.STEP_PUSH_MAIN
