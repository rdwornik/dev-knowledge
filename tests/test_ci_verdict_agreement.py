from __future__ import annotations

from pathlib import Path

import actions_verdict as av
import ci_verdict as cv
import merge_path as mp


def test_ci_verdict_and_merge_path_agree_for_the_same_sha_and_actions_data(
        tmp_path: Path, monkeypatch):
    sha = "a" * 40
    run = {
        "databaseId": 41,
        "headSha": sha,
        "status": "completed",
        "conclusion": "success",
        "event": "push",
        "url": "https://example.invalid/actions/runs/41",
        "createdAt": "2026-10-23T10:00:00Z",
        "updatedAt": "2026-10-23T10:10:00Z",
    }
    contexts = av.required_contexts_for(False)
    jobs = [
        {"name": name, "conclusion": "success", "databaseId": index}
        for index, name in enumerate(contexts, start=1)
    ]

    monkeypatch.setattr(cv, "list_runs", lambda **_kwargs: [run])
    monkeypatch.setattr(cv, "fetch_jobs", lambda _run_id, **_kwargs: jobs)
    monkeypatch.setattr(cv, "fetch_job_log", lambda *_args, **_kwargs: None)

    direct = cv.verdict_for(
        sha, repo_root=tmp_path, baseline="", required_contexts=contexts, sleep_fn=lambda _s: None)
    through_merge_path = mp.read_verdict(
        sha, base="", root=tmp_path, timeout_s=0, interval_s=0, contexts=contexts)

    assert direct.sha == through_merge_path.sha == sha
    assert direct.state == through_merge_path.state, (
        "ci_verdict and merge_path must judge the same check-runs for this SHA identically")
    assert direct.state == "PASS", "the shared all-success Actions fixture must be landable"
