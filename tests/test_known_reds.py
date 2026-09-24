"""scripts/known_reds.py -- ADR-121 step 1: baseline identity, attribution, no anonymous red.

RED-FIRST (ADR-108 SS B). Every test here was authored and witnessed FAILING before
scripts/known_reds.py existed.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def kr():
    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    return _load("known_reds_under_test", _REPO / "scripts" / "known_reds.py")


WITNESS_1 = (
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_live_spine_is_ordered_rebuild_first_and_always_runs"
)


# --- baseline id -----------------------------------------------------------------------

def test_compute_baseline_id_is_deterministic_regardless_of_dict_order(kr):
    a = {"x": {"attribution": "pre-freeze"}, "y": {"attribution": "witness"}}
    b = {"y": {"attribution": "witness"}, "x": {"attribution": "pre-freeze"}}
    assert kr.compute_baseline_id(a, date="2026-09-24") == kr.compute_baseline_id(b, date="2026-09-24")


def test_compute_baseline_id_changes_with_content(kr):
    a = {"x": {"attribution": "pre-freeze"}}
    b = {"x": {"attribution": "unattributed", "reason": "why"}}
    assert kr.compute_baseline_id(a, date="2026-09-24") != kr.compute_baseline_id(b, date="2026-09-24")


def test_compute_baseline_id_carries_the_date(kr):
    members = {"x": {"attribution": "pre-freeze"}}
    assert kr.compute_baseline_id(members, date="2026-09-24").startswith("2026-09-24-")


# --- refresh -----------------------------------------------------------------------------

def test_refresh_carries_forward_previous_attribution_and_marks_witnesses(kr):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-17-abc", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": {"attribution": "pre-freeze"}})
    failed = frozenset({"tests/a.py::t1", WITNESS_1})
    registry, dropped = kr.refresh(failed=failed, workers=4, commit="new", measured_via="local",
                                   date="2026-09-24", attribution={}, previous=previous)
    assert registry.members["tests/a.py::t1"] == {"attribution": "pre-freeze"}
    assert registry.members[WITNESS_1]["attribution"] == kr.WITNESS
    assert dropped == []


def test_refresh_refuses_a_new_unattributed_red(kr):
    failed = frozenset({"tests/a.py::t1", "tests/b.py::t2"})
    with pytest.raises(kr.KnownRedsError, match="tests/b.py::t2"):
        kr.refresh(failed=failed, workers=4, commit="new", measured_via="local",
                  date="2026-09-24", attribution={"tests/a.py::t1": {"attribution": "pre-freeze"}},
                  previous=None)


def test_refresh_accepts_a_new_red_with_real_attribution(kr):
    failed = frozenset({"tests/b.py::t2"})
    attribution = {"tests/b.py::t2": {"attribution": {"first_bad_sha": "deadbeef", "lane": "x"}}}
    registry, _ = kr.refresh(failed=failed, workers=4, commit="new", measured_via="local",
                             date="2026-09-24", attribution=attribution, previous=None)
    assert registry.members["tests/b.py::t2"]["attribution"] == {"first_bad_sha": "deadbeef",
                                                                   "lane": "x"}


def test_refresh_drops_members_no_longer_failing(kr):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": {"attribution": "pre-freeze"},
                                    "tests/fixed.py::t9": {"attribution": "pre-freeze"}})
    registry, dropped = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                                   measured_via="local", date="2026-09-24", attribution={},
                                   previous=previous)
    assert dropped == ["tests/fixed.py::t9"]
    assert "tests/fixed.py::t9" not in registry.members


def test_refresh_is_idempotent_on_the_same_failed_set(kr):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": {"attribution": "pre-freeze"}})
    r1, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                       measured_via="local", date="2026-09-24", attribution={}, previous=previous)
    r2, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                       measured_via="local", date="2026-09-24", attribution={}, previous=r1)
    assert r1.baseline_id == r2.baseline_id


# --- registry round-trip ------------------------------------------------------------------

def test_registry_round_trips_through_json(kr, tmp_path):
    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-24-abc123", measured_at_sha="s",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": {"attribution": "pre-freeze"}})
    path = tmp_path / "registry.json"
    kr.write_registry(path, registry)
    loaded = kr.load_registry(path)
    assert loaded == registry


def test_load_registry_missing_file_fails_closed(kr, tmp_path):
    with pytest.raises(kr.KnownRedsError, match="no registry"):
        kr.load_registry(tmp_path / "absent.json")


def test_load_registry_wrong_schema_refuses(kr, tmp_path):
    path = tmp_path / "registry.json"
    path.write_text('{"schema": "something-else/1"}', encoding="utf-8")
    with pytest.raises(kr.KnownRedsError, match="schema"):
        kr.load_registry(path)


# --- compare -------------------------------------------------------------------------------

def _registry(kr, members, workers=4):
    return kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-24-xyz", measured_at_sha="s",
                       measured_via="local", workers=workers, members=members)


def test_compare_prints_baseline_id_on_a_clean_run(kr):
    registry = _registry(kr, {})
    result = kr.compare(frozenset(), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["baseline_id"] == registry.baseline_id


def test_compare_prints_baseline_id_on_a_failing_run(kr):
    registry = _registry(kr, {})
    result = kr.compare(frozenset({"tests/new.py::t"}), registry, workers=4)
    assert result["verdict"] == "fail"
    assert result["baseline_id"] == registry.baseline_id


def test_compare_a_known_member_is_pre_existing_not_a_regression(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["pre_existing"] == ["tests/a.py::t1"]
    assert result["regressions"] == []


def test_compare_an_unknown_failure_is_a_regression(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1", "tests/new.py::t"}), registry, workers=4)
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["tests/new.py::t"]
    assert result["pre_existing"] == ["tests/a.py::t1"]


def test_compare_a_witness_is_reported_separately_never_as_a_regression(kr):
    registry = _registry(kr, {WITNESS_1: {"attribution": kr.WITNESS}})
    result = kr.compare(frozenset({WITNESS_1}), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["witnesses"] == [WITNESS_1]
    assert result["regressions"] == []
    assert result["pre_existing"] == []


def test_compare_worker_mismatch_is_not_comparable(kr):
    registry = _registry(kr, {}, workers=4)
    result = kr.compare(frozenset(), registry, workers=2)
    assert result["verdict"] == "fail"
    assert "NOT COMPARABLE" in result["reason"]


def test_compare_a_broken_pytest_exit_is_not_comparable(kr):
    registry = _registry(kr, {})
    result = kr.compare(frozenset(), registry, workers=4, pytest_exit=2)
    assert result["verdict"] == "fail"
    assert "NOT COMPARABLE" in result["reason"]


def test_compare_names_an_unattributed_known_member(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": kr.UNATTRIBUTED, "reason": "x"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["unattributed"] == ["tests/a.py::t1"]


def test_render_compare_uses_no_pipe_tables(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    report = kr.render_compare(result)
    assert "|" not in report
    assert registry.baseline_id in report


# --- find_lane -------------------------------------------------------------------------------

def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.strip()


def _init_repo(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")


@pytest.fixture
def toy_repo(tmp_path):
    repo = tmp_path / "toy"
    _init_repo(repo)
    (repo / "README.md").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-q", "-m", "init")
    return repo


def test_find_lane_reads_the_merge_subject_when_the_first_bad_sha_is_itself_the_merge(kr, toy_repo):
    _git(toy_repo, "checkout", "-q", "-b", "worktree-my-lane")
    (toy_repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(toy_repo, "add", "f.txt")
    _git(toy_repo, "commit", "-q", "-m", "work")
    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m", "Merge branch 'worktree-my-lane' @ deadbeef",
        "worktree-my-lane")
    merge_sha = _git(toy_repo, "rev-parse", "HEAD")
    assert kr.find_lane(toy_repo, merge_sha, merge_sha) == "my-lane"


def test_find_lane_reads_the_first_merge_on_the_ancestry_path(kr, toy_repo):
    _git(toy_repo, "checkout", "-q", "-b", "worktree-my-lane")
    (toy_repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(toy_repo, "add", "f.txt")
    _git(toy_repo, "commit", "-q", "-m", "work")
    first_bad = _git(toy_repo, "rev-parse", "HEAD")
    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m", "Merge branch 'worktree-my-lane' @ deadbeef",
        "worktree-my-lane")
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "later, unrelated")
    tip = _git(toy_repo, "rev-parse", "HEAD")
    assert kr.find_lane(toy_repo, first_bad, tip) == "my-lane"


# --- attribute: the real git-bisect-run wrapper, end to end ---------------------------------

def test_attribute_bisects_a_tiny_repo_and_names_the_first_bad_commit_and_lane(kr, toy_repo):
    tests_dir = toy_repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_toy.py").write_text("def test_toy():\n    assert True\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_toy.py")
    _git(toy_repo, "commit", "-q", "-m", "add a passing toy test")
    good_sha = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "-b", "worktree-break-it")
    (tests_dir / "test_toy.py").write_text("def test_toy():\n    assert False\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_toy.py")
    _git(toy_repo, "commit", "-q", "-m", "break the toy test")
    break_sha = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m",
        "Merge branch 'worktree-break-it' @ deadbeef", "worktree-break-it")
    bad_sha = _git(toy_repo, "rev-parse", "HEAD")

    result = kr.attribute(toy_repo, "tests/test_toy.py::test_toy", good=good_sha, bad=bad_sha,
                          venv_python=Path(sys.executable), timeout=60.0)
    assert result["first_bad_sha"] == break_sha
    assert result["lane"] == "break-it"


def test_attribute_skips_commits_where_the_test_file_does_not_yet_exist(kr, toy_repo):
    """The test file is added AFTER `good`; bisect must skip through the commits where it does
    not exist rather than mis-report the range as untestable."""
    tests_dir = toy_repo / "tests"
    tests_dir.mkdir()
    good_sha = _git(toy_repo, "rev-parse", "HEAD")  # the toy_repo's own init commit: no tests/

    _git(toy_repo, "checkout", "-q", "-b", "worktree-add-it")
    (tests_dir / "test_new.py").write_text("def test_new():\n    assert True\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_new.py")
    _git(toy_repo, "commit", "-q", "-m", "add the test, passing")
    (tests_dir / "test_new.py").write_text("def test_new():\n    assert False\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_new.py")
    _git(toy_repo, "commit", "-q", "-m", "break it later")
    break_sha = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m",
        "Merge branch 'worktree-add-it' @ deadbeef", "worktree-add-it")
    bad_sha = _git(toy_repo, "rev-parse", "HEAD")

    result = kr.attribute(toy_repo, "tests/test_new.py::test_new", good=good_sha, bad=bad_sha,
                          venv_python=Path(sys.executable), timeout=60.0)
    assert result["first_bad_sha"] == break_sha
