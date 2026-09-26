"""scripts/ci_red_age.py -- LANE-5B2-17 ([#802]): how long has main's CI been red, and since when.

RED-FIRST (ADR-108 SS B). Every test here was authored and witnessed FAILING before
scripts/ci_red_age.py existed.
"""
from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

_REPO = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def cra():
    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    return _load("ci_red_age_under_test", _REPO / "scripts" / "ci_red_age.py")


NOW = datetime(2026, 9, 26, 12, 0, 0, tzinfo=timezone.utc)


def _run(created_hours_ago: float, conclusion, *, sha="s", url="u", createdAt=None):
    return {
        "databaseId": 1, "headSha": sha, "conclusion": conclusion, "status": "completed",
        "url": url,
        "createdAt": (createdAt or (NOW - timedelta(hours=created_hours_ago))).isoformat()
                     .replace("+00:00", "Z"),
    }


# --- red_since -------------------------------------------------------------------------

def test_red_since_is_none_when_the_newest_judged_run_is_green(cra):
    runs = [_run(1, "success"), _run(2, "failure")]
    assert cra.red_since(runs, now=NOW) is None


def test_red_since_is_none_on_an_empty_run_list(cra):
    assert cra.red_since([], now=NOW) is None


def test_red_since_skips_an_in_progress_run_without_breaking_the_streak(cra):
    """`conclusion: None` (in_progress/queued) neither breaks nor extends the streak."""
    runs = [
        {"databaseId": 3, "headSha": "c", "conclusion": None, "status": "in_progress",
         "url": "u3", "createdAt": NOW.isoformat().replace("+00:00", "Z")},
        _run(1, "failure", sha="b"),
        _run(23, "failure", sha="a"),
        _run(30, "success", sha="z"),
    ]
    result = cra.red_since(runs, now=NOW)
    assert result is not None
    assert result.sha == "a"
    assert result.hours == pytest.approx(23.0, abs=0.01)


def test_red_since_at_23_hours_is_a_finding_but_not_yet_over_the_threshold(cra):
    runs = [_run(23, "failure", sha="oldest-red"), _run(30, "success", sha="green")]
    result = cra.red_since(runs, now=NOW)
    assert result is not None
    assert result.hours == pytest.approx(23.0, abs=0.01)
    assert result.hours <= cra.RED_AGE_THRESHOLD_H
    assert result.sha == "oldest-red"
    assert result.truncated is False


def test_red_since_at_25_hours_is_over_the_threshold(cra):
    runs = [_run(25, "failure", sha="oldest-red"), _run(30, "success", sha="green")]
    result = cra.red_since(runs, now=NOW)
    assert result is not None
    assert result.hours == pytest.approx(25.0, abs=0.01)
    assert result.hours > cra.RED_AGE_THRESHOLD_H


def test_red_since_walks_the_whole_streak_across_several_runs(cra):
    runs = [_run(1, "failure", sha="newest"), _run(5, "cancelled", sha="mid"),
           _run(25, "failure", sha="oldest-red"), _run(30, "success", sha="green")]
    result = cra.red_since(runs, now=NOW)
    assert result.sha == "oldest-red"
    assert result.hours == pytest.approx(25.0, abs=0.01)


def test_red_since_reports_truncated_when_every_fetched_run_is_red(cra):
    runs = [_run(1, "failure", sha="a"), _run(10, "failure", sha="b")]
    result = cra.red_since(runs, now=NOW)
    assert result is not None
    assert result.truncated is True


def test_red_since_is_not_truncated_when_a_green_run_bounds_the_streak(cra):
    runs = [_run(1, "failure", sha="a"), _run(10, "success", sha="b")]
    result = cra.red_since(runs, now=NOW)
    assert result.truncated is False


# --- render ------------------------------------------------------------------------------

def test_render_uses_the_contracts_own_wording(cra):
    result = cra.RedAge(since="2026-09-25T12:00:00Z", hours=25.0, sha="abc", url="http://x")
    report = cra.render(result)
    assert report.startswith("RED-SINCE 2026-09-25T12:00:00Z 25.0")


def test_render_a_clean_verdict_names_no_since(cra):
    assert "RED-SINCE none" in cra.render(None)


def test_render_flags_a_truncated_streak(cra):
    result = cra.RedAge(since="s", hours=1.0, sha="a", url="u", truncated=True)
    assert "truncated" in cra.render(result)


# --- compute (the injectable seam) --------------------------------------------------------

def test_compute_uses_the_module_level_list_fn_by_name_so_monkeypatch_works(cra, monkeypatch, tmp_path):
    calls = []

    def fake_list_runs(*, repo_root, workflow, branch, limit):
        calls.append((workflow, branch, limit))
        return [_run(25, "failure"), _run(30, "success")]

    monkeypatch.setattr(cra, "list_runs", fake_list_runs)
    result = cra.compute(repo_root=tmp_path, clock_fn=lambda: NOW)
    assert result.hours == pytest.approx(25.0, abs=0.01)
    assert calls == [(cra.WORKFLOW, cra.BRANCH, 30)]


# --- CLI -----------------------------------------------------------------------------------

def test_cli_exits_zero_at_23_hours_and_one_at_25_hours(cra, monkeypatch, tmp_path):
    def make_fake(hours):
        def fake_list_runs(*, repo_root, workflow, branch, limit):
            return [_run(hours, "failure"), _run(hours + 5, "success")]
        return fake_list_runs

    monkeypatch.setattr(cra, "list_runs", make_fake(23))
    runner = CliRunner()

    class _FrozenDateTime(cra.datetime):
        @classmethod
        def now(cls, tz=None):
            return NOW

    monkeypatch.setattr(cra, "datetime", _FrozenDateTime)
    result = runner.invoke(cra.cli, ["--repo-root", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "RED-SINCE" in result.output

    monkeypatch.setattr(cra, "list_runs", make_fake(25))
    result = runner.invoke(cra.cli, ["--repo-root", str(tmp_path)])
    assert result.exit_code == 1, result.output


def test_cli_writes_out_json_with_the_structured_fields(cra, monkeypatch, tmp_path):
    def fake_list_runs(*, repo_root, workflow, branch, limit):
        return [_run(25, "failure", sha="deadbeef", url="http://run"), _run(30, "success")]

    monkeypatch.setattr(cra, "list_runs", fake_list_runs)

    class _FrozenDateTime(cra.datetime):
        @classmethod
        def now(cls, tz=None):
            return NOW

    monkeypatch.setattr(cra, "datetime", _FrozenDateTime)
    out_path = tmp_path / "ci-red.json"
    runner = CliRunner()
    result = runner.invoke(cra.cli, ["--repo-root", str(tmp_path), "--out-json", str(out_path)])
    assert result.exit_code == 1
    import json
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["sha"] == "deadbeef"
    assert payload["url"] == "http://run"
    assert payload["hours"] == pytest.approx(25.0, abs=0.01)


def test_cli_reports_gh_unavailable_as_exit_2(cra, monkeypatch, tmp_path):
    def broken_list_runs(*, repo_root, workflow, branch, limit):
        raise cra.GhUnavailable("gh not found")

    monkeypatch.setattr(cra, "list_runs", broken_list_runs)
    runner = CliRunner()
    result = runner.invoke(cra.cli, ["--repo-root", str(tmp_path)])
    assert result.exit_code == 2
