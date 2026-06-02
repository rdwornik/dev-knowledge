"""Unit tests for scripts/fleet_health.py (ADR-70 Tier-2 daily fleet audit)."""

import importlib.util
from datetime import date, timedelta
from pathlib import Path


_P = Path(__file__).resolve().parent.parent / "scripts" / "fleet_health.py"


def _load():
    spec = importlib.util.spec_from_file_location("fleet_health", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fh = _load()


# --- parse_health_date ------------------------------------------------------

def test_parse_health_date_reads_frontmatter():
    text = "---\nrun_date: 2026-06-02\nrepos_total: 5\n---\n"
    assert fh.parse_health_date(text) == date(2026, 6, 2)


def test_parse_health_date_missing_returns_none():
    assert fh.parse_health_date("# no frontmatter\n") is None


# --- is_stale ---------------------------------------------------------------

def test_is_stale_missing_file(tmp_path):
    assert fh.is_stale(tmp_path / "FLEET-HEALTH.md") is True


def test_is_stale_today_not_stale(tmp_path):
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(f"---\nrun_date: {date.today().isoformat()}\n---\n", encoding="utf-8")
    assert fh.is_stale(f) is False


def test_is_stale_yesterday_is_stale(tmp_path):
    f = tmp_path / "FLEET-HEALTH.md"
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    f.write_text(f"---\nrun_date: {yesterday}\n---\n", encoding="utf-8")
    assert fh.is_stale(f) is True


# --- build_digest -----------------------------------------------------------

_STATES = [
    {"name": "repo-a", "statuses": ["pass", "pass", "pass"]},
    {"name": "repo-b", "statuses": ["pass", "fail", "warn"]},
]


def test_build_digest_frontmatter_contains_run_date():
    out = fh.build_digest(_STATES, date(2026, 6, 2))
    assert "run_date: 2026-06-02" in out


def test_build_digest_green_count():
    out = fh.build_digest(_STATES, date(2026, 6, 2))
    assert "repos_green: 1" in out
    assert "repos_issues: 1" in out


def test_build_digest_table_contains_both_repos():
    out = fh.build_digest(_STATES, date(2026, 6, 2))
    assert "repo-a" in out
    assert "repo-b" in out


def test_build_digest_all_green():
    states = [{"name": "r", "statuses": ["pass", "pass"]}]
    out = fh.build_digest(states, date(2026, 6, 2))
    assert "repos_green: 1" in out
    assert "All 1 repos green" in out


# --- surface_line -----------------------------------------------------------

def test_surface_line_all_green(tmp_path):
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(
        "---\nrun_date: 2026-06-02\nrepos_total: 5\nrepos_green: 5\nrepos_issues: 0\n---\n",
        encoding="utf-8",
    )
    line = fh.surface_line(f)
    assert "5/5" in line and "green" in line and "2026-06-02" in line


def test_surface_line_has_issues(tmp_path):
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(
        "---\nrun_date: 2026-06-02\nrepos_total: 5\nrepos_green: 3\nrepos_issues: 2\n---\n",
        encoding="utf-8",
    )
    line = fh.surface_line(f)
    assert "2 issue" in line and "FLEET-HEALTH.md" in line


def test_surface_line_missing_file(tmp_path):
    line = fh.surface_line(tmp_path / "FLEET-HEALTH.md")
    assert "no health data" in line


# --- load_all_states --------------------------------------------------------

def test_load_all_states_reads_state_yamls(tmp_path):
    eco = tmp_path / "ecosystem"
    for name in ("repo-a", "repo-b"):
        (eco / name).mkdir(parents=True)
        (eco / name / "state.yaml").write_text(
            f"name: {name}\nlast_audit: '2026-06-02'\nfindings:\n"
            f"- check_name: vision_md\n  evidence: ok\n  status: pass\n"
            f"- check_name: adr38\n  evidence: ok\n  status: fail\n",
            encoding="utf-8",
        )
    states = fh.load_all_states(eco)
    assert len(states) == 2
    names = {s["name"] for s in states}
    assert names == {"repo-a", "repo-b"}
    for s in states:
        assert s["statuses"] == ["pass", "fail"]


def test_load_all_states_empty_ecosystem(tmp_path):
    assert fh.load_all_states(tmp_path / "ecosystem") == []


# --- round-trip: build_digest + parse_health_date ---------------------------

def test_round_trip_date_parseable():
    out = fh.build_digest(_STATES, date(2026, 6, 2))
    assert fh.parse_health_date(out) == date(2026, 6, 2)
