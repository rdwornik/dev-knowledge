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
    regressions: tuple[str, ...], *, repo_root: Path, known_ids_fn=None, extra_jobs: tuple = (),
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
    jobs = [
        *extra_jobs,
        {"name": _LEG_UBUNTU, "conclusion": "failure", "databaseId": 1},
    ]
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


def _init_ci_verdict_registry_repo(repo_root: Path, *, with_registry: bool = True) -> str:
    from scripts import known_reds

    subprocess.run(["git", "init", "--quiet"], cwd=repo_root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo_root, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.invalid"], cwd=repo_root, check=True)
    if with_registry:
        owned = {
            "attribution": "pre-freeze",
            "task": "[#9001]",
            "owner": "rob",
            "expiry": "2099-01-01",
        }
        unattributed = {
            "attribution": "unattributed",
            "task": "[#9002]",
            "owner": "rob",
            "expiry": "2099-01-01",
        }
        registry = known_reds.Registry(
            schema=known_reds.SCHEMA,
            baseline_id="fixture",
            measured_at_sha="fixture",
            measured_via="local",
            workers=4,
            members={
                "tests/test_shared.py::test_shared": owned,
                "tests/test_unattributed.py::test_unattributed": unattributed,
            },
            members_by_os={
                "ubuntu-latest": {"tests/test_ubuntu.py::test_ubuntu": owned},
                "windows-latest": {"tests/test_windows.py::test_windows": owned},
            },
        )
        known_reds.write_registry(repo_root / "logs" / "KNOWN-REDS-REGISTRY.json", registry)
    else:
        (repo_root / "README.txt").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "fixture"], cwd=repo_root, check=True)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, check=True, capture_output=True, text=True,
    ).stdout.strip()


def test_registry_known_ids_reads_shared_and_only_the_requested_os_bucket(tmp_path: Path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    sha = _init_ci_verdict_registry_repo(repo_root)

    ubuntu_ids = cv._registry_known_ids(sha, repo_root=repo_root, os_key="ubuntu-latest")
    windows_ids = cv._registry_known_ids(sha, repo_root=repo_root, os_key="windows-latest")
    shared_ids = cv._registry_known_ids(sha, repo_root=repo_root, os_key=None)

    assert ubuntu_ids == frozenset({
        "tests/test_shared.py::test_shared",
        "tests/test_ubuntu.py::test_ubuntu",
    })
    assert windows_ids == frozenset({
        "tests/test_shared.py::test_shared",
        "tests/test_windows.py::test_windows",
    })
    assert shared_ids == frozenset({"tests/test_shared.py::test_shared"})


def test_registry_known_ids_raises_when_registry_is_missing_at_sha(tmp_path: Path):
    from scripts import known_reds

    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    sha = _init_ci_verdict_registry_repo(repo_root, with_registry=False)

    with pytest.raises(known_reds.KnownRedsError):
        cv._registry_known_ids(sha, repo_root=repo_root, os_key="ubuntu-latest")


def test_resolve_known_ids_fn_uses_default_only_without_injected_ci_fetch_seams():
    def explicit(*_args, **_kwargs):
        return frozenset()

    assert cv._resolve_known_ids_fn(None, {}) is cv._registry_known_ids
    assert cv._resolve_known_ids_fn(None, {"log_fn": object()}) is None
    assert cv._resolve_known_ids_fn(explicit, {}) is explicit


def test_live_registry_known_ids_contains_c6618_regressions():
    repo_root = Path(__file__).resolve().parents[1]
    available = subprocess.run(
        ["git", "cat-file", "-e", f"{_C6618_REGISTRY_SHA}:logs/KNOWN-REDS-REGISTRY.json"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if available.returncode:
        pytest.skip(f"commit {_C6618_REGISTRY_SHA} is unavailable")

    assert set(_C6618_REGRESSIONS) <= cv._registry_known_ids(
        _C6618_REGISTRY_SHA, repo_root=repo_root, os_key="ubuntu-latest")


def test_registry_known_ids_does_not_excuse_members_without_attribution(tmp_path: Path):
    from scripts import known_reds

    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    _init_ci_verdict_registry_repo(repo_root, with_registry=False)

    missing_attribution = "tests/test_missing_attribution.py::test_missing"
    attributed = "tests/test_attributed.py::test_attributed"
    registry_path = repo_root / "logs" / "KNOWN-REDS-REGISTRY.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(
        json.dumps({
            "schema": known_reds.SCHEMA,
            "baseline_id": "fixture",
            "measured_at_sha": "fixture",
            "measured_via": "local",
            "workers": 4,
            "members": {
                missing_attribution: {
                    "task": "[#9001]", "owner": "rob", "expiry": "2099-01-01",
                },
                attributed: {
                    "attribution": "pre-freeze",
                    "task": "[#9002]", "owner": "rob", "expiry": "2099-01-01",
                },
            },
            "hooks": {},
            "members_by_os": {},
            "notes": [],
        }),
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", "logs/KNOWN-REDS-REGISTRY.json"], cwd=repo_root, check=True)
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "add raw registry"], cwd=repo_root, check=True)
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_root, check=True, capture_output=True, text=True,
    ).stdout.strip()

    known_ids = cv._registry_known_ids(sha, repo_root=repo_root, os_key=None)

    assert missing_attribution not in known_ids
    assert attributed in known_ids


@pytest.mark.parametrize("malformed", [None, 42])
def test_malformed_known_ids_result_fails_closed(
        tmp_path: Path, malformed):
    verdict = _read_failed_pytest_verdict(
        _C6618_REGRESSIONS,
        repo_root=tmp_path,
        known_ids_fn=lambda *_args, **_kwargs: malformed,
    )

    assert verdict.new_reds == tuple(
        f"{_LEG_UBUNTU}: {regression}" for regression in _C6618_REGRESSIONS)
    assert "registry" in verdict.reason and "could not be read" in verdict.reason


def test_unexplained_failing_job_stays_separate_from_known_pytest_regressions(
        tmp_path: Path):
    verdict = _read_failed_pytest_verdict(
        _C6618_REGRESSIONS,
        repo_root=tmp_path,
        known_ids_fn=lambda *_args, **_kwargs: frozenset(_C6618_REGRESSIONS),
        extra_jobs=({"name": "commit-gate", "conclusion": "failure", "databaseId": 2},),
    )

    assert verdict.new_reds == ("commit-gate",)
    assert not any(regression in str(red)
                   for red in verdict.new_reds for regression in _C6618_REGRESSIONS)


def test_c6618_registry_lock_tests_do_not_skip():
    source = Path(__file__).read_text(encoding="utf-8")
    skip_call = "pytest" + ".skip("

    assert skip_call not in source
