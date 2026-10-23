from __future__ import annotations

from pathlib import Path

import pytest

import actions_verdict as av
import merge_receipt as mr
import test_flow_metrics as tfm

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


def test_main_push_rejects_a_verdict_recorded_before_the_integration_push(
        tmp_path: Path, monkeypatch):
    mr.open_receipt(tmp_path, slug="reuse", batch="reuse")
    prior_verdict = av.Verdict(sha=_PUSHED_SHA, state=av.STATE_PASS)
    monkeypatch.setattr(mr._av, "verdict_for", lambda *_args, **_kwargs: prior_verdict)
    mr.record_actions_verdict(
        tmp_path,
        slug="reuse",
        sha=_PUSHED_SHA,
        first_parent=lambda _root, _sha: "b" * 40,
    )
    mr.record_push(
        tmp_path, slug="reuse", target="integration",
        branch="worktree-integrate-reuse", sha=_PUSHED_SHA, seconds=1.0)

    try:
        mr.record_push(
            tmp_path, slug="reuse", target="main", branch="main", sha=_PUSHED_SHA, seconds=2.0)
    except mr.MergeReceiptError as exc:
        assert "suite" in str(exc), "the refusal must identify the missing integration-branch read"
    else:
        pytest.fail("a pre-integration verdict was reused for the main push")


def test_m2_counts_same_sha_same_verdict_as_reuse_but_counts_a_different_sha():
    landed = {
        "kind": "merge",
        "slug": "feat",
        "merge_sha": "sha-a",
        "steps": [{"step": "push-main", "ended": "2026-01-03T00:00:00Z"}],
    }
    runs = [
        {"databaseId": 1, "headBranch": "worktree-feat", "headSha": "sha-a",
         "workflowName": "conductor", "conclusion": "success"},
        {"databaseId": 2, "headBranch": "main", "headSha": "sha-a",
         "workflowName": "conductor", "conclusion": "success"},
        {"databaseId": 3, "headBranch": "worktree-feat", "headSha": "sha-b",
         "workflowName": "conductor", "conclusion": "success"},
    ]
    jobs = {
        run["databaseId"]: [{
            "name": "pytest (ubuntu-latest)",
            "conclusion": "success",
            "startedAt": "2026-01-02T10:00:00Z",
            "completedAt": "2026-01-02T10:05:00Z",
        }]
        for run in runs
    }

    result = tfm.m2_runs_per_landing(
        [landed], runs, jobs, since=_SINCE, until=_UNTIL)

    assert result["per_landing"] == [{"slug": "feat", "suite_runs": 2}], (
        "same-SHA same-verdict reruns are reuse; a distinct SHA is a separate suite run")
