from __future__ import annotations

import json
import subprocess
from pathlib import Path

import actions_verdict as av
import ci_verdict as cv
import merge_path as mp
import pytest


_C6618_REGISTRY_SHA = "c6618dbb7"
_C6618_REGRESSIONS = (
    "tests/test_dispatch_launch.py::test_the_real_pre_launch_moment_refuses_an_occupied_husk",
    "tests/test_graph_spine.py::test_the_live_orphan_census_reaches_zero_against_its_stated_class",
    "tests/test_graph_spine_commit_tier.py::test_the_live_spine_is_ordered_rebuild_first_and_always_runs",
    "tests/test_graph_spine_commit_tier.py::test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-orphan-census]",
    "tests/test_graph_spine_commit_tier.py::test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-process-list]",
    "tests/test_graph_spine_commit_tier.py::test_the_refusal_blocks_a_real_commit_and_only_its_own_hook_blocks_it[graph-task-coverage]",
)
_LEG_UBUNTU = "pytest (ubuntu-latest)"
_LOG_PREFIX = "pytest\tUNKNOWN STEP\t2026-10-23T10:05:00.0000000Z "


def _known_reds_log(regressions: tuple[str, ...]) -> str:
    lines = [
        "known-reds compare",
        "",
        "baseline id    : 2026-10-04-fdf4f4952211",
        "os key         : ubuntu-latest",
        "pre-existing   : 0",
        "witnesses      : 0",
        f"regressions    : {len(regressions)}",
        *(f"  REGRESSION    {node_id}" for node_id in regressions),
    ]
    return "\n".join(_LOG_PREFIX + line for line in lines)


def _read_failed_pytest_verdict(
    regressions: tuple[str, ...], *, repo_root: Path, known_ids_fn=None,
) -> cv.CiVerdict:
    run = {
        "databaseId": 41,
        "headSha": _C6618_REGISTRY_SHA,
        "status": "completed",
        "conclusion": "failure",
        "event": "push",
        "url": "https://example.invalid/actions/runs/41",
        "createdAt": "2026-10-23T10:00:00Z",
        "updatedAt": "2026-10-23T10:10:00Z",
    }
    jobs = [{"name": _LEG_UBUNTU, "conclusion": "failure", "databaseId": 1}]
    kwargs = {}
    if known_ids_fn is not None:
        kwargs["known_ids_fn"] = known_ids_fn

    return cv.verdict_for(
        _C6618_REGISTRY_SHA,
        repo_root=repo_root,
        baseline=None,
        list_fn=lambda **_kwargs: [run],
        jobs_fn=lambda _run_id, **_kwargs: jobs,
        log_fn=lambda _run_id, _job_id, **_kwargs: _known_reds_log(regressions),
        sleep_fn=lambda _seconds: None,
        **kwargs,
    )


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


def test_c6618_registry_members_are_not_new_reds_without_a_baseline(tmp_path: Path):
    seen = []

    def known_ids_fn(sha, *, repo_root, os_key):
        seen.append((sha, repo_root, os_key))
        return frozenset(_C6618_REGRESSIONS)

    verdict = _read_failed_pytest_verdict(
        _C6618_REGRESSIONS, repo_root=tmp_path, known_ids_fn=known_ids_fn)

    assert verdict.new_reds == ()
    assert verdict.state == "PRE-EXISTING"
    assert verdict.verdict == cv.STATE_RED
    assert "known-reds registry members" in verdict.reason
    assert seen == [(_C6618_REGISTRY_SHA, tmp_path, "ubuntu-latest")]


def test_known_reds_filter_keeps_a_new_id_with_its_leg_prefix(tmp_path: Path):
    new_id = "tests/test_new_behavior.py::test_new_failure"
    regressions = (*_C6618_REGRESSIONS[:5], new_id)

    verdict = _read_failed_pytest_verdict(
        regressions,
        repo_root=tmp_path,
        known_ids_fn=lambda _sha, *, repo_root, os_key: frozenset(_C6618_REGRESSIONS),
    )

    assert verdict.new_reds == (f"{_LEG_UBUNTU}: {new_id}",)


def test_without_known_ids_fn_baseline_none_keeps_reporting_regressions(tmp_path: Path):
    verdict = _read_failed_pytest_verdict(
        ("tests/test_new_behavior.py::test_failure",), repo_root=tmp_path)

    assert verdict.new_reds == (
        f"{_LEG_UBUNTU}: tests/test_new_behavior.py::test_failure",
    )
    assert verdict.state == "RED"


def test_c6618_registry_contains_the_six_regression_ids():
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "show", f"{_C6618_REGISTRY_SHA}:logs/KNOWN-REDS-REGISTRY.json"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        pytest.skip(f"commit {_C6618_REGISTRY_SHA} is unavailable")

    registry = json.loads(result.stdout)
    assert set(_C6618_REGRESSIONS) <= set(registry["members"])
