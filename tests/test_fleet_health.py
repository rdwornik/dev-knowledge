"""Unit tests for scripts/fleet_health.py (ADR-70 Tier-2 daily fleet audit)."""

import importlib.util
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock


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
        "---\nrun_date: 2026-06-02\nrepos_total: 5\nrepos_green: 5\nrepos_issues: 0\n"
        "completed_at: 2026-06-02T09:00:00\n---\n",
        encoding="utf-8",
    )
    line = fh.surface_line(f)
    assert "5/5" in line and "green" in line and "2026-06-02" in line
    assert "INCOMPLETE" not in line


def test_surface_line_has_issues(tmp_path):
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(
        "---\nrun_date: 2026-06-02\nrepos_total: 5\nrepos_green: 3\nrepos_issues: 2\n"
        "completed_at: 2026-06-02T09:00:00\n---\n",
        encoding="utf-8",
    )
    line = fh.surface_line(f)
    assert "2 issue" in line and "FLEET-HEALTH.md" in line
    assert "INCOMPLETE" not in line


def test_surface_line_flags_incomplete_baseline(tmp_path):
    # A digest with today's run_date but NO completed_at = a failed/partial run.
    # The throttle skips a same-day rerun, so surface_line must not report it as
    # healthy -- it flags INCOMPLETE (Codex HIGH #2).
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(
        "---\nrun_date: 2026-06-02\nrepos_total: 5\nrepos_green: 5\nrepos_issues: 0\n---\n",
        encoding="utf-8",
    )
    line = fh.surface_line(f)
    assert "INCOMPLETE" in line


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


def test_load_state_yaml_captures_path(tmp_path):
    sf = tmp_path / "state.yaml"
    sf.write_text(
        "name: r\npath: /some/path\nlast_audit: '2026-06-02'\n"
        "findings:\n- check_name: x\n  status: pass\n",
        encoding="utf-8",
    )
    assert fh._load_state_yaml(sf)["path"] == "/some/path"


# --- siblings_available (cloud / isolated-clone fail-soft guard) ------------

def _write_state(eco: Path, name: str, path: str):
    (eco / name).mkdir(parents=True)
    (eco / name / "state.yaml").write_text(
        f"name: {name}\npath: {path}\n"
        f"findings:\n- check_name: x\n  status: pass\n",
        encoding="utf-8",
    )


def test_siblings_available_false_missing_ecosystem(tmp_path):
    assert fh.siblings_available(tmp_path / "nope", tmp_path) is False


def test_siblings_available_false_when_isolated(tmp_path):
    # Stored path is a Windows abs path (absent on the test host) and no
    # conventional <parent>/<name> slot exists -> isolated clone -> False.
    hub = tmp_path / "hub"
    hub.mkdir()
    _write_state(hub / "ecosystem", "ai-council", "C:\\Users\\x\\ai-council")
    assert fh.siblings_available(hub / "ecosystem", hub) is False


def test_siblings_available_true_when_conventional_slot_present(tmp_path):
    hub = tmp_path / "hub"
    hub.mkdir()
    (tmp_path / "ai-council").mkdir()  # <parent>/<name> slot next to hub
    _write_state(hub / "ecosystem", "ai-council", "C:\\Users\\x\\ai-council")
    assert fh.siblings_available(hub / "ecosystem", hub) is True


def test_siblings_available_true_when_stored_path_exists(tmp_path):
    hub = tmp_path / "hub"
    hub.mkdir()
    real_sib = tmp_path / "elsewhere" / "corp-ops"
    real_sib.mkdir(parents=True)
    _write_state(hub / "ecosystem", "corp-ops", str(real_sib))
    assert fh.siblings_available(hub / "ecosystem", hub) is True


# --- round-trip: build_digest + parse_health_date ---------------------------

def test_round_trip_date_parseable():
    out = fh.build_digest(_STATES, date(2026, 6, 2))
    assert fh.parse_health_date(out) == date(2026, 6, 2)


# --- hardening (#85, ADR-76): timeout, atomic write, completed_at, stale ----

# run_audit per-repo-sized timeout budget -----------------------------------

def test_run_audit_success_returns_true(tmp_path):
    fake = mock.Mock(returncode=0, stderr="", stdout="")
    with mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.run_audit(tmp_path, timeout_s=120) is True


def test_run_audit_findings_exit1_still_true(tmp_path):
    # audit.py run exits 1 on FAIL findings -- a healthy execution, not a crash.
    fake = mock.Mock(returncode=1, stderr="", stdout="")
    with mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.run_audit(tmp_path, timeout_s=120) is True


def test_run_audit_crash_exit2_returns_false(tmp_path):
    fake = mock.Mock(returncode=2, stderr="boom", stdout="")
    with mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.run_audit(tmp_path, timeout_s=120) is False


def test_run_audit_timeout_returns_false(tmp_path, capsys):
    exc = fh.subprocess.TimeoutExpired(cmd="audit.py", timeout=1)
    with mock.patch.object(fh.subprocess, "run", side_effect=exc):
        assert fh.run_audit(tmp_path, timeout_s=1) is False
    assert "timed out" in capsys.readouterr().err.lower()


def test_run_audit_passes_timeout_kwarg(tmp_path):
    fake = mock.Mock(returncode=0, stderr="", stdout="")
    with mock.patch.object(fh.subprocess, "run", return_value=fake) as m:
        fh.run_audit(tmp_path, timeout_s=77)
    assert m.call_args.kwargs.get("timeout") == 77


def test_audit_timeout_budget_scales_with_repo_count():
    # The overall budget is the per-repo allowance times the repo count.
    assert fh.audit_timeout_budget(5) == fh._PER_REPO_TIMEOUT_S * 5
    assert fh.audit_timeout_budget(0) == fh._PER_REPO_TIMEOUT_S  # floor at 1 repo


# atomic digest write --------------------------------------------------------

def test_atomic_write_creates_file(tmp_path):
    target = tmp_path / "OUT.md"
    fh._atomic_write(target, "hello")
    assert target.read_text(encoding="utf-8") == "hello"


def test_atomic_write_overwrites_existing(tmp_path):
    target = tmp_path / "OUT.md"
    target.write_text("old", encoding="utf-8")
    fh._atomic_write(target, "new")
    assert target.read_text(encoding="utf-8") == "new"


def test_atomic_write_leaves_no_tmp_file(tmp_path):
    target = tmp_path / "OUT.md"
    fh._atomic_write(target, "x")
    leftovers = sorted(p.name for p in tmp_path.iterdir() if p.name != "OUT.md")
    assert leftovers == []


def test_atomic_write_does_not_clobber_concurrent_tmp(tmp_path):
    # Regression for the shared-temp-name race (Codex HIGH #1): a concurrent
    # writer's temp file (here the OLD fixed `.tmp` name) must survive our write
    # untouched -- we use a process-unique temp and clean up only our own.
    target = tmp_path / "FLEET-HEALTH.md"
    foreign = tmp_path / "FLEET-HEALTH.md.tmp"
    foreign.write_text("other-process-in-flight", encoding="utf-8")
    fh._atomic_write(target, "mine")
    assert target.read_text(encoding="utf-8") == "mine"
    assert foreign.exists()
    assert foreign.read_text(encoding="utf-8") == "other-process-in-flight"


# build_digest completed_at + status line ------------------------------------

def test_build_digest_completed_stamps_completed_at():
    out = fh.build_digest(_STATES, date(2026, 6, 2), completed_at="2026-06-02T18:00:00")
    assert "completed_at: 2026-06-02T18:00:00" in out


def test_build_digest_incomplete_omits_completed_at():
    out = fh.build_digest(_STATES, date(2026, 6, 2), completed_at=None)
    assert "completed_at:" not in out


def test_build_digest_completed_status_line():
    states = [{"name": "r", "statuses": ["pass", "pass"]}]
    out = fh.build_digest(states, date(2026, 6, 2), completed_at="2026-06-02T18:00:00")
    assert "baseline completed" in out.lower()


def test_build_digest_incomplete_status_line():
    out = fh.build_digest(_STATES, date(2026, 6, 2), completed_at=None)
    assert "incomplete" in out.lower()


def test_build_digest_backcompat_two_arg_still_green_line():
    # The legacy "All N repos green" body line is preserved (separate from the
    # new baseline-status line) so prior counting semantics don't shift.
    states = [{"name": "r", "statuses": ["pass", "pass"]}]
    out = fh.build_digest(states, date(2026, 6, 2), completed_at="2026-06-02T18:00:00")
    assert "All 1 repos green" in out


# completed_at parse + stale (>48h) detection --------------------------------

def test_parse_completed_at_reads_it():
    text = "---\nrun_date: 2026-06-02\ncompleted_at: 2026-06-02T18:00:00\n---\n"
    assert fh.parse_completed_at(text) == "2026-06-02T18:00:00"


def test_parse_completed_at_missing_returns_none():
    assert fh.parse_completed_at("---\nrun_date: 2026-06-02\n---\n") is None


def test_is_completed_stale_true_when_older_than_48h():
    text = "completed_at: 2026-06-01T00:00:00\n"
    assert fh.is_completed_stale(text, datetime(2026, 6, 6, 0, 0, 0)) is True


def test_is_completed_stale_false_when_recent():
    text = "completed_at: 2026-06-06T00:00:00\n"
    assert fh.is_completed_stale(text, datetime(2026, 6, 6, 12, 0, 0)) is False


def test_is_completed_stale_false_when_missing():
    # Missing completed_at is the INCOMPLETE signal (surfaced elsewhere), not a
    # >48h-stale signal -- can't compute an age, so not "stale".
    assert fh.is_completed_stale("run_date: 2026-06-06\n", datetime(2026, 6, 6)) is False


def test_is_completed_stale_false_on_garbage_timestamp():
    assert fh.is_completed_stale("completed_at: not-a-date\n", datetime(2026, 6, 6)) is False


# refresh integration: completed vs incomplete digest ------------------------

def _seed_states(tmp_path):
    eco = tmp_path / "ecosystem"
    (eco / "repo-a").mkdir(parents=True)
    (eco / "repo-a" / "state.yaml").write_text(
        "name: repo-a\nlast_audit: '2026-06-02'\n"
        "findings:\n- check_name: x\n  status: pass\n",
        encoding="utf-8",
    )
    return eco


def test_refresh_completed_writes_completed_at(tmp_path):
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    health = logs / "FLEET-HEALTH.md"
    with mock.patch.object(fh, "run_audit", return_value=True):
        ok = fh.refresh(tmp_path, eco, logs, health, date(2026, 6, 2))
    assert ok is True
    text = health.read_text(encoding="utf-8")
    assert "completed_at:" in text and "baseline completed" in text.lower()


def test_refresh_incomplete_omits_completed_at(tmp_path):
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    health = logs / "FLEET-HEALTH.md"
    with mock.patch.object(fh, "run_audit", return_value=False):
        ok = fh.refresh(tmp_path, eco, logs, health, date(2026, 6, 2))
    assert ok is False
    text = health.read_text(encoding="utf-8")
    assert "completed_at:" not in text and "incomplete" in text.lower()


# --- drift roll-up ([#244] P4 Step 7) ---------------------------------------
# Aggregation from each consumer's own .methodology.yaml (no central store). The
# waivability policy comes from the REAL hub manifest (session-end-backpressure
# non-waivable; hub-toc-hooks waivable) -- the same invariant release_lint locks.


def _write_consumer(base: Path, name: str, allowlist: str | None) -> Path:
    root = base / name
    root.mkdir(parents=True)
    (root / "JOURNAL.md").write_text("# Journal\n", encoding="utf-8")
    if allowlist is not None:
        (root / ".methodology.yaml").write_text(allowlist, encoding="utf-8")
    return root


def test_drift_summaries_aggregates_on_disk_consumers(tmp_path):
    hub = tmp_path / "hub"
    hub.mkdir()
    eco = hub / "ecosystem"
    c1 = _write_consumer(
        tmp_path, "ai-council",
        "sanctioned_divergences:\n"
        "  - component: hub-toc-hooks\n"
        "    reason: CLI has no ARCHITECTURE.md TOC to gate\n"
        "    review_date: 2999-01-01\n")
    c2 = _write_consumer(tmp_path, "corp-ops", None)
    _write_state(eco, "ai-council", str(c1))
    _write_state(eco, "corp-ops", str(c2))
    out = fh.drift_summaries(eco, hub, date(2026, 7, 4))
    assert set(out) == {"ai-council", "corp-ops"}
    assert out["ai-council"]["declared"] == 1
    assert out["ai-council"]["valid"] == 1          # hub-toc-hooks is waivable -> valid
    assert out["corp-ops"]["declared"] == 0


def test_drift_summaries_flags_non_waivable_as_rejected(tmp_path):
    """A consumer that allowlists a NON-waivable component (session-end-backpressure) is a real
    drift signal even statically -> rejected_non_waivable == 1 (contract 2, aggregated)."""
    hub = tmp_path / "hub"
    hub.mkdir()
    eco = hub / "ecosystem"
    c = _write_consumer(
        tmp_path, "ai-council",
        "sanctioned_divergences:\n"
        "  - component: session-end-backpressure\n"
        "    reason: we think we can skip it\n"
        "    review_date: 2999-01-01\n")
    _write_state(eco, "ai-council", str(c))
    out = fh.drift_summaries(eco, hub, date(2026, 7, 4))
    assert out["ai-council"]["rejected_non_waivable"] == 1
    assert out["ai-council"]["valid"] == 0


def test_drift_summaries_skips_when_isolated(tmp_path):
    """No sibling on disk (stored path absent, no <parent>/<name> slot) -> empty roll-up,
    no writes (cloud-safe skip)."""
    hub = tmp_path / "hub"
    hub.mkdir()
    eco = hub / "ecosystem"
    _write_state(eco, "ai-council", "C:\\nope\\ai-council")
    assert fh.drift_summaries(eco, hub, date(2026, 7, 4)) == {}


def test_drift_summaries_skips_the_hub_itself(tmp_path):
    """The hub is the baseline, not a consumer to check against itself -> excluded."""
    hub = tmp_path / "hub"
    hub.mkdir()
    eco = hub / "ecosystem"
    _write_state(eco, ".dev-knowledge", str(hub))
    assert fh.drift_summaries(eco, hub, date(2026, 7, 4)) == {}


def test_build_digest_renders_drift_section():
    drift = {"ai-council": {"declared": 1, "valid": 1, "rejected_non_waivable": 0,
                            "static_absent_mapped_organs": 2}}
    out = fh.build_digest(_STATES, date(2026, 7, 4),
                          completed_at="2026-07-04T09:00:00", drift_by_repo=drift)
    assert "## Drift" in out
    drift_block = out.split("## Drift")[1]
    assert "ai-council" in drift_block           # consumer row rendered in the drift section
    assert "| ai-council | 1 | 1 | 0 | 2 |" in drift_block


def test_build_digest_no_drift_section_when_empty():
    assert "## Drift" not in fh.build_digest(_STATES, date(2026, 7, 4))
    assert "## Drift" not in fh.build_digest(_STATES, date(2026, 7, 4), drift_by_repo={})


# --- groom_escalation_line (overdue quarterly-groom escalation) --------------

# Footer shaped like the real BACKLOG "Grooming log" line (Recent: dates + Next quarterly:).
_GROOM_OLD = ("**Grooming log:** git history is the record. "
              "Recent: 2026-01-10 · 2026-02-15 · 2026-03-20. Next quarterly: 2026-04-01.\n")
_GROOM_FUTURE = ("**Grooming log:** Recent: 2026-01-01 · 2026-01-15. "
                 "Next quarterly: 2026-12-31.\n")


def test_groom_escalation_fires_when_overdue():
    line = fh.groom_escalation_line(_GROOM_OLD, date(2026, 10, 15))  # ~209d past 2026-03-20
    assert line is not None
    assert "overdue quarterly groom" in line
    assert "2026-03-20" in line          # newest PAST *Recent* date reported...
    assert "2026-04-01" not in line      # ...NOT the excluded "Next quarterly:" target (F2-twin)


def test_groom_escalation_silent_when_fresh():
    assert fh.groom_escalation_line(_GROOM_OLD, date(2026, 5, 1)) is None  # 30d, within cadence


def test_groom_escalation_excludes_future_next_quarterly():
    # The future "Next quarterly: 2026-12-31" must NOT count as a completed groom; the
    # newest PAST date (2026-01-15) drives the age -> overdue.
    line = fh.groom_escalation_line(_GROOM_FUTURE, date(2026, 6, 1))
    assert line is not None
    assert "2026-01-15" in line
    assert "2026-12-31" not in line


def test_groom_escalation_past_next_quarterly_does_not_mask():
    # F2-twin frozen contract (GPT-5.6 A/B trial 2026-07-11, verified-real): once the
    # "Next quarterly:" TARGET is itself in the past, it must NOT count as a completed groom
    # — else it resets the cadence clock and MASKS the overdue escalation. Here the real
    # groom (2026-06-01, 141d) is overdue but the past target (2026-09-01, 49d) would
    # suppress the escalation entirely if it were counted. Mirrors
    # test_grooming_cadence_past_next_quarterly_does_not_mask in test_validate_doc_rot.py.
    log = "**Grooming log:** Recent: 2026-06-01. Next quarterly: 2026-09-01.\n"
    line = fh.groom_escalation_line(log, date(2026, 10, 20))
    assert line is not None                 # escalation NOT masked
    assert "2026-06-01" in line             # clock pinned to the real groom...
    assert "2026-09-01" not in line         # ...not the past target date


def test_groom_escalation_none_when_no_grooming_line():
    assert fh.groom_escalation_line("# a digest with no grooming footer\n", date(2026, 10, 15)) is None


def test_groom_escalation_boundary_at_threshold():
    last = date(2026, 1, 1)
    at = last + timedelta(days=fh._GROOM_QUARTERLY_DAYS)       # age == 92 -> not yet overdue
    over = last + timedelta(days=fh._GROOM_QUARTERLY_DAYS + 1)  # age == 93 -> overdue
    footer = f"**Grooming log:** Recent: {last.isoformat()}.\n"
    assert fh.groom_escalation_line(footer, at) is None
    assert fh.groom_escalation_line(footer, over) is not None
