"""RED witnesses for Done-contract item 2: each landing pushes its own receipt line."""
from __future__ import annotations

import json
import subprocess

import pytest

import merge_receipt
from test_land_lane import Env, _git, do_land


@pytest.fixture(autouse=True)
def _git_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "safe.bareRepository")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "all")
    monkeypatch.setenv("GIT_CONFIG_KEY_1", "core.autocrlf")
    monkeypatch.setenv("GIT_CONFIG_VALUE_1", "false")
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")


@pytest.fixture
def env(tmp_path, monkeypatch):
    e = Env(tmp_path / "env")
    monkeypatch.chdir(e.worktree)
    return e


def _landed_receipt(env, report):
    entries = [
        json.loads(line)
        for line in _git(env.origin, "show", "main:logs/MERGE-RECEIPTS.jsonl").splitlines()
        if line.strip()
    ]
    return next(
        (
            entry
            for entry in entries
            if entry.get("slug") == "lane-a" and entry.get("merge_sha") == report.sha
        ),
        None,
    )


def test_landing_receipt_is_already_on_main_when_land_returns(env):
    """Done-contract item 2: the landing's own receipt is pushed with that landing."""
    report = do_land(env)
    assert report.ok, report.message

    assert _landed_receipt(env, report) is not None


def test_receipt_merge_sha_is_an_ancestor_of_main(env):
    """Done-contract item 2: the receipt names the judged merge reachable from main."""
    report = do_land(env)
    assert report.ok, report.message
    entry = _landed_receipt(env, report)

    assert entry is not None
    assert entry["merge_sha"] == report.sha
    subprocess.run(
        ["git", "-C", str(env.origin), "merge-base", "--is-ancestor", entry["merge_sha"], "main"],
        check=True,
        capture_output=True,
    )


def test_landing_leaves_no_receipt_for_a_successor_to_carry(env):
    """Done-contract item 2: the same landing consumes its carry file."""
    report = do_land(env)
    assert report.ok, report.message

    assert not env.carry.exists() or not env.carry.read_text(encoding="utf-8").strip()


def test_main_first_parent_spine_contains_no_non_merge_landing_commit(env):
    """Done-contract item 2: receipt recording does not add a first-parent commit."""
    base = env.origin_ref("main")
    report = do_land(env)
    assert report.ok, report.message

    non_merges = _git(
        env.origin,
        "rev-list",
        "--first-parent",
        "--no-merges",
        f"{base}..main",
    )
    assert non_merges == ""


def test_receipt_record_failure_refuses_without_changing_origin(env, monkeypatch):
    """Done-contract item 2: receipt failure refuses before main is pushed."""
    before = env.origin_ref("main")

    def fail_close(*_args, **_kwargs):
        raise RuntimeError("injected receipt recording failure")

    monkeypatch.setattr(merge_receipt, "close_receipt", fail_close)
    report = do_land(env)

    assert not report.ok
    assert report.exit_code != 0
    assert env.origin_ref("main") == before
