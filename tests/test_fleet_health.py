"""Unit tests for scripts/fleet_health.py (ADR-70 Tier-2 daily fleet audit)."""

import contextlib
import importlib.util
import json
import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock

import pytest


_P = Path(__file__).resolve().parent.parent / "scripts" / "fleet_health.py"


def _load():
    spec = importlib.util.spec_from_file_location("fleet_health", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fh = _load()


@contextlib.contextmanager
def _prompts_dir_matching():
    """Neutralise the ambient CLAUDE_PROMPTS_DIR scopes for tests that are NOT about the
    E-29 guard.

    Without it, `main()` returns 2 or 0 depending on whether the machine running the suite
    happens to carry a stale inherited value -- so three unrelated digest tests would pass
    in CI and fail on the operator's box, which is an env-dependent RED arriving in the
    wrong place. The guard's own tests below seed both values explicitly instead.
    """
    with mock.patch.object(fh, "read_prompts_dir_scopes", return_value=("X", "X")):
        yield


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


# --- [#99] a red digest row names the failing check(s) ----------------------

_STATE_YAML = """name: repo-x
path: /somewhere/repo-x
last_audit: '2026-08-28'
findings:
- check_name: vision_md
  evidence: fine
  status: pass
- check_name: canonical_freshness
  evidence: 'CLAUDE.md: last_reviewed 2026-07-27 is 32d old
    (> 30d cadence)'
  status: fail
- check_name: substrate_declaration
  evidence: nope
  status: fail
"""


def test_check_status_pairs_survives_multiline_evidence(tmp_path):
    """The pairing is order-based, so wrapped evidence must not break attribution."""
    f = tmp_path / "state.yaml"
    f.write_text(_STATE_YAML, encoding="utf-8")
    st = fh._load_state_yaml(f)
    assert st["checks"] == [
        ("vision_md", "pass"),
        ("canonical_freshness", "fail"),
        ("substrate_declaration", "fail"),
    ]


def test_failing_check_names_lists_only_failures(tmp_path):
    f = tmp_path / "state.yaml"
    f.write_text(_STATE_YAML, encoding="utf-8")
    st = fh._load_state_yaml(f)
    assert fh.failing_check_names(st) == "canonical_freshness, substrate_declaration"


def test_failing_check_names_empty_when_green():
    assert fh.failing_check_names({"checks": [("a", "pass"), ("b", "warn")]}) == ""


def test_failing_check_names_caps_and_counts_the_overflow():
    """The cap must never DROP a failure silently -- the remainder is counted."""
    st = {"checks": [(f"c{i}", "fail") for i in range(5)]}
    assert fh.failing_check_names(st, cap=2) == "c0, c1 (+3 more)"


def test_status_without_a_check_name_is_attributed_not_dropped(tmp_path):
    """An unnameable failing check still has to be counted."""
    f = tmp_path / "state.yaml"
    f.write_text("findings:" + chr(10) + "  status: fail" + chr(10), encoding="utf-8")
    st = fh._load_state_yaml(f)
    assert st["checks"] == [("?", "fail")]
    assert fh.failing_check_names(st) == "?"


def test_build_digest_red_row_carries_the_failing_check_name():
    """[#99]'s Done-when: a red repo's digest line carries the failing check name(s)."""
    states = [
        {"name": "repo-a", "statuses": ["pass"], "checks": [("vision_md", "pass")]},
        {"name": "repo-b", "statuses": ["pass", "fail"],
         "checks": [("vision_md", "pass"), ("canonical_freshness", "fail")]},
    ]
    out = fh.build_digest(states, date(2026, 6, 2))
    red = [ln for ln in out.splitlines() if ln.startswith("| repo-b")][0]
    assert "canonical_freshness" in red
    green = [ln for ln in out.splitlines() if ln.startswith("| repo-a")][0]
    assert "canonical_freshness" not in green


def test_build_digest_tolerates_states_without_checks_key():
    """Legacy callers pass states with no `checks` key; they must not crash."""
    out = fh.build_digest(_STATES, date(2026, 6, 2))
    assert "| repo-b | !! | 1 | 1 |" in out


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


# ---------------------------------------------------------------------------
# Operator-load gauge ([#270]) — the gating FIRST element of any Tier-2 nightly
# layer. Design of record: docs/audits/2026-07-05-draft-tier2-nightly-layer.md.
# Every producer below is SEEDED and the rendered count asserted, per the row's
# Done-when leg 1 ("renders ... from live counts").
# ---------------------------------------------------------------------------

# --- producer 1: open nightly-triage Issues (the one non-local read) --------

def _git_repo(tmp_path: Path) -> Path:
    """gh resolves the repo from the cwd's git remote, so the counter refuses
    without spawning anything outside a git worktree. Seed the marker."""
    (tmp_path / ".git").mkdir(exist_ok=True)
    return tmp_path


def test_count_triage_issues_parses_gh_json(tmp_path):
    fake = mock.Mock(returncode=0, stdout='[{"number": 47}, {"number": 45}]', stderr="")
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) == 2


def test_count_triage_issues_zero_open_is_zero_not_none(tmp_path):
    # Zero open Issues is a MEASUREMENT (0), not an unavailable producer (None).
    # Collapsing the two would make an empty funnel indistinguishable from a
    # broken gh, which is exactly the blindness M2 exists to catch.
    fake = mock.Mock(returncode=0, stdout="[]", stderr="")
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) == 0


def test_count_triage_issues_refuses_outside_a_git_worktree(tmp_path):
    # No .git -> no repo for gh to resolve -> refuse WITHOUT spawning. Pinned
    # because it is also what keeps every other test in this file hermetic.
    ran = mock.Mock(side_effect=AssertionError("gh must not be spawned"))
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", ran):
        assert fh.count_open_triage_issues(tmp_path) is None


def test_count_triage_issues_none_when_gh_absent(tmp_path):
    with mock.patch.object(fh.shutil, "which", return_value=None), \
         mock.patch.object(fh, "_gh_fallback_path", return_value=None):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) is None


def test_count_triage_issues_none_when_gh_fails(tmp_path):
    fake = mock.Mock(returncode=1, stdout="", stderr="auth required")
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) is None


def test_count_triage_issues_none_on_timeout(tmp_path):
    boom = fh.subprocess.TimeoutExpired(cmd="gh", timeout=1)
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", side_effect=boom):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) is None


def test_count_triage_issues_none_on_garbage_json(tmp_path):
    fake = mock.Mock(returncode=0, stdout="not json at all", stderr="")
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) is None


# --- producer 2: pending closure proposals ----------------------------------

_BACKLOG_TWO_OPEN = "- [#11] [P2][M] eleven\n- [#22] [P3][S] twenty-two\n"


def test_count_pending_closures_counts_unchecked_and_still_open(tmp_path):
    (tmp_path / "PROPOSALS-2026-08-01.md").write_text(
        "- [ ] **#11** - a\n- [x] **#22** - already reviewed\n", encoding="utf-8")
    assert fh.count_pending_closures(tmp_path, _BACKLOG_TWO_OPEN) == 1


def test_count_pending_closures_ignores_ids_no_longer_open(tmp_path):
    # #98's still-open guard, mirrored: an unchecked proposal for an id that has
    # since left BACKLOG is NOT operator load -- it is already discharged.
    (tmp_path / "PROPOSALS-2026-08-01.md").write_text(
        "- [ ] **#11** - a\n- [ ] **#999** - closed long ago\n", encoding="utf-8")
    assert fh.count_pending_closures(tmp_path, _BACKLOG_TWO_OPEN) == 1


def test_count_pending_closures_dedupes_across_files(tmp_path):
    # The same id unchecked in two PROPOSALS files is ONE pending decision.
    (tmp_path / "PROPOSALS-2026-08-01.md").write_text("- [ ] **#11** - a\n", encoding="utf-8")
    (tmp_path / "PROPOSALS-2026-08-02.md").write_text("- [ ] **#11** - a\n", encoding="utf-8")
    assert fh.count_pending_closures(tmp_path, _BACKLOG_TWO_OPEN) == 1


def test_count_pending_closures_zero_when_no_files(tmp_path):
    assert fh.count_pending_closures(tmp_path / "nope", _BACKLOG_TWO_OPEN) == 0


# --- producer 3: disposition-register rows ----------------------------------

def test_count_dispositions_counts_entry_ids(tmp_path):
    reg = tmp_path / "disposition-register.yaml"
    reg.write_text(
        "# a comment mentioning - id: not-an-entry\n"
        "dispositions:\n"
        "  - id: warn-one\n    organ: x\n"
        "  - id: warn-two\n    organ: y\n", encoding="utf-8")
    assert fh.count_dispositions(reg) == 2


def test_count_dispositions_none_when_missing(tmp_path):
    assert fh.count_dispositions(tmp_path / "absent.yaml") is None


# --- producer 4: ARCHITECT-REVIEW-PENDING markers ---------------------------

def test_count_review_pending_counts_heading_and_bold_shapes(tmp_path):
    (tmp_path / "a.md").write_text(
        "## SELF-ADJUDICATION LOG (ARCHITECT-REVIEW-PENDING)\n", encoding="utf-8")
    (tmp_path / "b.md").write_text(
        "text\n**ARCHITECT-REVIEW-PENDING: AC-1** (the hooksPath unset)\n", encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 2


def test_count_review_pending_excludes_prose_and_backticked_mentions(tmp_path):
    # THE PRECISION LEVER. A bare substring grep over docs/audits/ scores 7 hits
    # on the live tree, of which 5 are prose ABOUT the marker (a design doc, an
    # evidence sheet, a table cell). A gauge that reports 7 where the truth is 2
    # is noise, and noise is what this row's own kill criterion demotes.
    (tmp_path / "prose.md").write_text(
        "the ratification funnel (closure proposals, nightly-triage Issues,\n"
        "ARCHITECT-REVIEW-PENDING items, grooming digests) saturates.\n", encoding="utf-8")
    (tmp_path / "backticked.md").write_text(
        "  4. `ARCHITECT-REVIEW-PENDING` markers in the latest run artifacts\n", encoding="utf-8")
    (tmp_path / "table.md").write_text(
        "| epic | a narrowing left ARCHITECT-REVIEW-PENDING without closure | - |\n",
        encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 0


def test_count_review_pending_counts_files_not_occurrences(tmp_path):
    # One artifact carrying a heading AND a bold item is ONE pending artifact.
    (tmp_path / "a.md").write_text(
        "## SELF-ADJUDICATION LOG (ARCHITECT-REVIEW-PENDING)\n"
        "**ARCHITECT-REVIEW-PENDING: AC-1** (one)\n"
        "**ARCHITECT-REVIEW-PENDING: AC-2** (two)\n", encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 1


def test_count_review_pending_zero_when_dir_absent(tmp_path):
    assert fh.count_review_pending(tmp_path / "nope") == 0


# --- Lane h0: dispatch traces per day ----------------------------------------

def test_count_traces_today_counts_todays_files(tmp_path):
    prompts = tmp_path / "prompts"
    prompts.mkdir()
    (prompts / "2026-09-05-lane-h0-trace.md").write_text("x", encoding="utf-8")
    (prompts / "2026-09-05-lane-a-1.md").write_text("x", encoding="utf-8")
    (prompts / "2026-09-04-lane-old.md").write_text("x", encoding="utf-8")
    assert fh.count_traces_today(tmp_path, date(2026, 9, 5)) == 2


def test_count_traces_today_zero_when_dir_absent(tmp_path):
    assert fh.count_traces_today(tmp_path, date(2026, 9, 5)) == 0


def test_count_traces_today_none_when_unreadable(tmp_path):
    with mock.patch.object(fh, "_scan_md", return_value=None):
        assert fh.count_traces_today(tmp_path, date(2026, 9, 5)) is None


# --- producer 5: open BACKLOG by priority band ------------------------------

def test_count_backlog_by_priority_bands():
    text = ("- [#1] [P1][M] one\n- [#2] [P2][S] two\n- [#3] [P2][L] three\n"
            "- [#4] [P3][S] four\nsome prose [P2] that is not a row\n")
    assert fh.count_backlog_by_priority(text) == {"P1": 1, "P2": 2, "P3": 1}


def test_count_backlog_by_priority_empty_text():
    assert fh.count_backlog_by_priority("") == {"P1": 0, "P2": 0, "P3": 0}


# --- the funnel total + the rendered line -----------------------------------

_COUNTS = {"triage": 3, "closures": 45, "dispositions": 10, "review_pending": 6,
           "backlog": {"P1": 7, "P2": 91, "P3": 100}, "funnel_total": 64}


def test_funnel_total_sums_the_four_funnel_producers():
    assert fh.funnel_total({"triage": 3, "closures": 45,
                            "dispositions": 10, "review_pending": 6}) == 64


def test_funnel_total_sums_only_available_producers():
    # A partial total is honest and recoverable (the per-producer cells are stored
    # alongside it); recomputing later from an `n/a` cell would silently differ.
    assert fh.funnel_total({"triage": None, "closures": 45,
                            "dispositions": 10, "review_pending": 6}) == 61


def test_funnel_total_none_when_every_producer_unavailable():
    assert fh.funnel_total({"triage": None, "closures": None,
                            "dispositions": None, "review_pending": None}) is None


def test_load_line_renders_all_five_counts():
    line = fh.load_line(_COUNTS, delta=4)
    assert line.startswith("[load] ")
    for token in ("3 triage", "45 closures", "10 dispositions", "6 review-pending",
                  "7 P1", "91 P2", "100 P3"):
        assert token in line, f"{token!r} missing from {line!r}"
    assert "64" in line          # the funnel total
    assert "+4" in line          # signed 7d delta


def test_load_line_is_ascii_only():
    # The cp1252 lesson: this string reaches a Windows SessionStart console.
    fh.load_line(_COUNTS, delta=-4).encode("ascii")
    fh.load_line({"triage": None, "closures": None, "dispositions": None,
                  "review_pending": None, "backlog": {"P1": 0, "P2": 0, "P3": 0},
                  "funnel_total": None}, delta=None).encode("ascii")


def test_load_line_renders_na_for_unavailable_producer():
    counts = dict(_COUNTS, triage=None)
    line = fh.load_line(counts, delta=None)
    assert "n/a triage" in line
    assert "delta: n/a" in line


def test_load_line_negative_delta_is_signed():
    assert "-9" in fh.load_line(_COUNTS, delta=-9)


# --- the CSV: one row per run, header-stable, append-not-overwrite ----------

def test_append_load_row_writes_header_then_row(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 11), _COUNTS)
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == ",".join(fh.LOAD_CSV_HEADER)
    assert len(lines) == 2
    assert lines[1].startswith("2026-08-11,3,45,10,6,7,91,100,64")


def test_append_load_row_appends_across_two_runs(tmp_path):
    # Done-when leg 2, pinned: the CSV APPENDS per run and never overwrites.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 10), _COUNTS)
    fh.append_load_row(csv_path, date(2026, 8, 11), dict(_COUNTS, funnel_total=60))
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3                       # header + two runs
    assert lines[0] == ",".join(fh.LOAD_CSV_HEADER)   # header written ONCE
    assert lines[1].startswith("2026-08-10,")
    assert lines[2].startswith("2026-08-11,")


def test_append_load_row_header_stays_stable_across_runs(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    for i in range(3):
        fh.append_load_row(csv_path, date(2026, 8, 10 + i), _COUNTS)
    text = csv_path.read_text(encoding="utf-8")
    assert text.count(",".join(fh.LOAD_CSV_HEADER)) == 1


def test_append_load_row_writes_na_for_unavailable_producer(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 11), dict(_COUNTS, triage=None))
    assert "2026-08-11,n/a,45," in csv_path.read_text(encoding="utf-8")


def test_append_load_row_creates_parent_dir(tmp_path):
    csv_path = tmp_path / "logs" / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 11), _COUNTS)
    assert csv_path.exists()


def test_append_load_row_never_raises_on_unwritable_path(tmp_path):
    # Fail-soft contract: the gauge never breaks SessionStart. tmp_path itself is
    # a directory, so opening it for append raises inside -- and must be swallowed.
    fh.append_load_row(tmp_path, date(2026, 8, 11), _COUNTS)


# --- the 7d trend delta -----------------------------------------------------

def test_load_delta_compares_against_a_seven_day_old_row(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 4), dict(_COUNTS, funnel_total=50))
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) == 14   # 64 - 50


def test_load_delta_uses_the_newest_row_at_least_seven_days_old(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 7, 1), dict(_COUNTS, funnel_total=10))
    fh.append_load_row(csv_path, date(2026, 8, 4), dict(_COUNTS, funnel_total=50))
    fh.append_load_row(csv_path, date(2026, 8, 10), dict(_COUNTS, funnel_total=63))  # too recent
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) == 14   # vs 08-04, not 07-01/08-10


def test_load_delta_none_when_no_old_enough_row(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 10), _COUNTS)
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) is None


def test_load_delta_none_when_csv_absent(tmp_path):
    assert fh.load_delta(tmp_path / "absent.csv", _COUNTS, date(2026, 8, 11)) is None


def test_load_delta_none_when_today_total_unavailable(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 4), dict(_COUNTS, funnel_total=50))
    counts = dict(_COUNTS, funnel_total=None)
    assert fh.load_delta(csv_path, counts, date(2026, 8, 11)) is None


def test_load_delta_skips_rows_whose_total_is_na(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 3), dict(_COUNTS, funnel_total=50))
    fh.append_load_row(csv_path, date(2026, 8, 4), dict(_COUNTS, funnel_total=None))
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) == 14   # falls back to 08-03


def test_load_delta_never_raises_on_garbage_csv(tmp_path):
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    csv_path.write_text("not,a,valid\nheader\x00\n", encoding="utf-8")
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) is None


# --- the digest section + the SessionStart read-back ------------------------

def test_build_digest_renders_load_section():
    out = fh.build_digest(_STATES, date(2026, 8, 11), "2026-08-11T09:00:00",
                          None, dict(_COUNTS, delta_7d=4))
    assert "## Operator load" in out
    assert "[load] " in out
    assert "3 triage" in out


def test_build_digest_no_load_section_when_absent():
    out = fh.build_digest(_STATES, date(2026, 8, 11), "2026-08-11T09:00:00")
    assert "Operator load" not in out
    assert "[load]" not in out


def test_load_surface_line_reads_it_back_from_the_digest(tmp_path):
    # Done-when leg 1: the line renders at SessionStart. It is read BACK from the
    # digest rather than recomputed, so the every-session path costs no gh call --
    # the same pattern surface_line already uses for the repo counts.
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(fh.build_digest(_STATES, date(2026, 8, 11), "2026-08-11T09:00:00",
                                 None, dict(_COUNTS, delta_7d=4)), encoding="utf-8")
    line = fh.load_surface_line(f)
    assert line is not None
    assert line.startswith("[load] ")
    assert "45 closures" in line


def test_load_surface_line_none_when_digest_has_no_load_block(tmp_path):
    f = tmp_path / "FLEET-HEALTH.md"
    f.write_text(fh.build_digest(_STATES, date(2026, 8, 11), "2026-08-11T09:00:00"),
                 encoding="utf-8")
    assert fh.load_surface_line(f) is None


def test_load_surface_line_none_when_file_missing(tmp_path):
    assert fh.load_surface_line(tmp_path / "absent.md") is None


# --- collect_load: the aggregation, fail-soft per producer ------------------

def _seed_load_inputs(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "PROPOSALS-2026-08-01.md").write_text("- [ ] **#11** - a\n", encoding="utf-8")
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "disposition-register.yaml").write_text(
        "dispositions:\n  - id: warn-one\n  - id: warn-two\n", encoding="utf-8")
    audits = tmp_path / "docs" / "audits"
    audits.mkdir(parents=True)
    (audits / "run.md").write_text(
        "## SELF-ADJUDICATION LOG (ARCHITECT-REVIEW-PENDING)\n", encoding="utf-8")
    (tmp_path / "BACKLOG.md").write_text(_BACKLOG_TWO_OPEN, encoding="utf-8")
    _git_repo(tmp_path)
    return logs, eco / "disposition-register.yaml", audits


def test_collect_load_reads_every_producer(tmp_path):
    logs, reg, audits = _seed_load_inputs(tmp_path)
    fake = mock.Mock(returncode=0, stdout='[{"number": 1}, {"number": 2}, {"number": 3}]',
                     stderr="")
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", return_value=fake):
        counts = fh.collect_load(tmp_path, logs, reg, audits)
    assert counts["triage"] == 3
    assert counts["closures"] == 1
    assert counts["dispositions"] == 2
    assert counts["review_pending"] == 1
    assert counts["backlog"] == {"P1": 0, "P2": 1, "P3": 1}
    assert counts["funnel_total"] == 7


def test_collect_load_degrades_to_none_per_producer(tmp_path):
    logs, reg, audits = _seed_load_inputs(tmp_path)
    reg.unlink()
    with mock.patch.object(fh.shutil, "which", return_value=None), \
         mock.patch.object(fh, "_gh_fallback_path", return_value=None):
        counts = fh.collect_load(tmp_path, logs, reg, audits)
    assert counts["triage"] is None
    assert counts["dispositions"] is None
    assert counts["funnel_total"] == 2          # 1 closure + 1 review-pending
    line = fh.load_line(counts, delta=None)     # still renders, still ASCII
    line.encode("ascii")


def test_collect_load_never_raises_when_nothing_exists(tmp_path):
    with mock.patch.object(fh.shutil, "which", return_value=None), \
         mock.patch.object(fh, "_gh_fallback_path", return_value=None):
        counts = fh.collect_load(tmp_path, tmp_path / "l", tmp_path / "r", tmp_path / "a")
    # No BACKLOG.md at all is UNAVAILABLE, not an empty backlog (see the regression below).
    assert counts["backlog"] == {"P1": None, "P2": None, "P3": None}
    assert counts["closures"] is None


# --- terra HIGH regressions (2026-08-11) ------------------------------------
# Four correctness defects found by the gpt-5.6-terra review of this lane's diff. All
# four reproduced against live state; none closed as not-reproduced. Pinned here so a
# later edit cannot quietly reintroduce them.


def test_triage_query_passes_an_explicit_limit(tmp_path):
    # terra HIGH #1: `gh issue list` page-caps at 30 without --limit, so the funnel
    # would silently understate itself past 30 open Issues -- the meter going blind
    # exactly when the saturation it measures arrives.
    seen = {}

    def fake_run(cmd, **kw):
        seen["cmd"] = cmd
        return mock.Mock(returncode=0, stdout="[]", stderr="")

    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", fake_run):
        fh.count_open_triage_issues(_git_repo(tmp_path))
    assert "--limit" in seen["cmd"]
    limit = seen["cmd"][seen["cmd"].index("--limit") + 1]
    assert int(limit) >= 100, f"page cap {limit} is too low to be honest"


def test_unreadable_backlog_is_na_not_zero(tmp_path):
    # terra HIGH #2: degrading an unreadable BACKLOG.md to "" reported a serene, EMPTY
    # funnel at the exact moment the repo could not be read -- 0 where the contract
    # requires n/a. Both text-dependent producers must go unavailable together.
    logs, reg, audits = _seed_load_inputs(tmp_path)
    (tmp_path / "BACKLOG.md").unlink()
    with mock.patch.object(fh.shutil, "which", return_value=None), \
         mock.patch.object(fh, "_gh_fallback_path", return_value=None):
        counts = fh.collect_load(tmp_path, logs, reg, audits)
    assert counts["backlog"] == {"P1": None, "P2": None, "P3": None}
    assert counts["closures"] is None
    line = fh.load_line(counts, delta=None)
    assert "n/a P1" in line and "n/a closures" in line
    assert counts["funnel_total"] == 3          # dispositions 2 + review-pending 1 only


def test_csv_header_is_written_once_under_a_concurrent_create(tmp_path):
    # terra HIGH #3: the existence check happened BEFORE the open, so a scheduled run
    # and an interactive SessionStart could both see "no file" and both emit a header.
    # Simulated by letting a second writer land between the check and the write.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    real_open = fh.os.open

    def racing_open(path, flags, *a, **kw):
        # The competing process wins the create; ours must NOT also write a header.
        if not Path(path).exists():
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(",".join(fh.LOAD_CSV_HEADER) + "\n")
        return real_open(path, flags, *a, **kw)

    with mock.patch.object(fh.os, "open", racing_open):
        fh.append_load_row(csv_path, date(2026, 8, 11), _COUNTS)
    text = csv_path.read_text(encoding="utf-8")
    assert text.count(",".join(fh.LOAD_CSV_HEADER)) == 1, text


def test_csv_headers_an_empty_preexisting_file(tmp_path):
    # The truncated-prior-run case the atomic create cannot claim.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    csv_path.write_text("", encoding="utf-8")
    fh.append_load_row(csv_path, date(2026, 8, 11), _COUNTS)
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == ",".join(fh.LOAD_CSV_HEADER)
    assert len(lines) == 2


def test_csv_recovery_path_never_truncates_a_concurrent_writers_row(tmp_path):
    # terra HIGH, SECOND pass — and it refuted this function's own comment. The comment
    # claimed an empty-but-existing file could only come from a truncated prior run and
    # never from a concurrent create. FALSE: O_EXCL creates a ZERO-BYTE file, so a racing
    # writer observes size 0; the recovery then opened with "w" and truncated the
    # creator's already-written row. That is data loss. The recovery is append-only now.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    real_open = fh.os.open

    def racing_open(path, flags, *a, **kw):
        # Our O_EXCL loses; the winner then completes header + a row before we resume.
        if not Path(path).exists():
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(",".join(fh.LOAD_CSV_HEADER) + "\n")
                f.write("2026-08-04,1,1,1,1,1,1,1,4\n")
        return real_open(path, flags, *a, **kw)

    with mock.patch.object(fh.os, "open", racing_open):
        fh.append_load_row(csv_path, date(2026, 8, 11), _COUNTS)
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("2026-08-04,") for line in lines), \
        f"the concurrent writer's row was destroyed: {lines}"
    assert any(line.startswith("2026-08-11,") for line in lines)


def test_triage_count_at_the_page_ceiling_is_na_not_the_ceiling(tmp_path):
    # terra HIGH, second pass: --limit moved the blindness rather than removing it.
    # Reporting the ceiling as an exact count would be a wrong number wearing the
    # costume of a measurement — the one thing this gauge refuses to emit.
    payload = json.dumps([{"number": i} for i in range(fh._GH_ISSUE_LIMIT)])
    fake = mock.Mock(returncode=0, stdout=payload, stderr="")
    with mock.patch.object(fh.shutil, "which", return_value="gh"), \
         mock.patch.object(fh.subprocess, "run", return_value=fake):
        assert fh.count_open_triage_issues(_git_repo(tmp_path)) is None


def test_load_delta_survives_non_utf8_history(tmp_path):
    # terra HIGH, second pass: UnicodeDecodeError subclasses ValueError, which neither
    # OSError nor csv.Error catches — so ONE cp1252 byte in the trend history escaped to
    # refresh()'s wrapper and discarded the WHOLE gauge for that run. Corrupt history
    # must cost the delta and nothing else.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    csv_path.write_bytes(
        ",".join(fh.LOAD_CSV_HEADER).encode() + b"\n"
        + b"2026-08-04,1,1,1,1,1,1,1,50\n"
        + b"2026-08-05,\x96corrupt,1,1,1,1,1,1,7\n")
    delta = fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11))
    assert delta == 14                       # still reads the 08-04 row: 64 - 50


def test_refresh_writes_no_trend_row_when_the_digest_write_fails(tmp_path):
    # terra HIGH, second pass: the row was appended BEFORE the digest was durably
    # replaced, so a failed _atomic_write left a row for a run that never completed —
    # quietly breaking the one-row-per-digest-run invariant leg 2 rests on.
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    csv_path = logs / "OPERATOR-LOAD.csv"
    with mock.patch.object(fh, "run_audit", return_value=True), \
         mock.patch.object(fh, "drift_summaries", return_value={}), \
         mock.patch.object(fh, "count_open_triage_issues", return_value=3), \
         mock.patch.object(fh, "_atomic_write", side_effect=PermissionError("held open")):
        with pytest.raises(PermissionError):
            fh.refresh(tmp_path, eco, logs, tmp_path / "logs" / "FLEET-HEALTH.md",
                       date(2026, 8, 11))
    assert not csv_path.exists(), "an orphan trend row outlived a digest that never landed"


def test_refresh_still_writes_the_digest_when_the_csv_append_explodes(tmp_path):
    # The converse, pinned so the reordering above cannot invert the priority: the trend
    # is subordinate to the digest, never the other way round.
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    health = logs / "FLEET-HEALTH.md"
    with mock.patch.object(fh, "run_audit", return_value=True), \
         mock.patch.object(fh, "drift_summaries", return_value={}), \
         mock.patch.object(fh, "count_open_triage_issues", return_value=3), \
         mock.patch.object(fh, "append_load_row", side_effect=RuntimeError("boom")):
        assert fh.refresh(tmp_path, eco, logs, health, date(2026, 8, 11)) is True
    assert "## Operator load" in health.read_text(encoding="utf-8")


def test_csv_creator_cannot_overwrite_a_racing_writers_row(tmp_path):
    # terra HIGH, THIRD pass: making only the RECOVERY path append-only left the CREATOR
    # holding a "w" descriptor at offset 0, so a racer could append header + row into the
    # just-created file and the creator would write straight over them. O_EXCL now only
    # claims the name; every writer, creator included, uses O_APPEND.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    real_close = fh.os.close

    def racing_close(fd):
        # We won the create. A competitor appends between our create and our append.
        result = real_close(fd)
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            f.write(",".join(fh.LOAD_CSV_HEADER) + "\n")
            f.write("2026-08-04,1,1,1,1,1,1,1,50\n")
        return result

    with mock.patch.object(fh.os, "close", racing_close):
        fh.append_load_row(csv_path, date(2026, 8, 11), _COUNTS)
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("2026-08-04,") for line in lines), \
        f"the racing writer's row was overwritten by the creator: {lines}"
    assert any(line.startswith("2026-08-11,") for line in lines)


def test_unreadable_proposals_file_makes_closures_unavailable(tmp_path):
    # terra HIGH, third pass: an OSError on one candidate was swallowed with `continue`,
    # so a partial tally was reported as a measurement -- the n/a-never-0 contract
    # violated in the same breath as it was being enforced for BACKLOG.
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "PROPOSALS-2026-08-01.md").write_text("- [ ] **#11** - a\n", encoding="utf-8")
    with mock.patch.object(Path, "read_text", side_effect=PermissionError("locked")):
        assert fh.count_pending_closures(logs, _BACKLOG_TWO_OPEN) is None


def test_unreadable_audit_artifact_makes_review_pending_unavailable(tmp_path):
    audits = tmp_path / "audits"
    audits.mkdir()
    (audits / "a.md").write_text("## X (ARCHITECT-REVIEW-PENDING)\n", encoding="utf-8")
    with mock.patch.object(Path, "read_text", side_effect=PermissionError("locked")):
        assert fh.count_review_pending(audits) is None


def test_absent_producer_dir_is_zero_not_unavailable(tmp_path):
    # The distinction the fix above must NOT blur: nothing to read is a measurement (0);
    # something present that cannot be read is an outage (None).
    assert fh.count_pending_closures(tmp_path / "nope", _BACKLOG_TWO_OPEN) == 0
    assert fh.count_review_pending(tmp_path / "nope") == 0


def test_review_pending_item_marker_requires_a_structured_id(tmp_path):
    # terra HIGH, third pass — the ACCEPTED half. A per-item marker names an id; prose
    # after the colon is explanatory text, not a tracked item.
    (tmp_path / "prose.md").write_text(
        "**ARCHITECT-REVIEW-PENDING: why this exists** is explained below.\n",
        encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 0
    (tmp_path / "real.md").write_text(
        "**ARCHITECT-REVIEW-PENDING: AC-1** (the hooksPath unset)\n", encoding="utf-8")
    (tmp_path / "real2.md").write_text(
        "**ARCHITECT-REVIEW-PENDING: SEQ-2** (a sequencing fork)\n", encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 2


def test_review_pending_heading_recall_is_deliberately_kept_broad(tmp_path):
    # terra HIGH, third pass — the DECLINED half, pinned so the decision is visible and
    # a later tightening has to argue with a test rather than a comment. A log titled
    # something other than "SELF-ADJUDICATION LOG" must still COUNT: for a debt gauge a
    # miss (silently under-reporting load, M1's own failure mode) is worse than a false
    # positive (over-reports, gets read, gets dismissed).
    (tmp_path / "differently-titled.md").write_text(
        "## OPEN ADJUDICATIONS (ARCHITECT-REVIEW-PENDING)\n", encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 1


def test_unreadable_producer_directory_is_na_not_zero(tmp_path):
    # terra HIGH, FOURTH pass: Path.exists()/glob() swallow a directory-access OSError,
    # so an ACL-denied logs/ or docs/audits/ listed as empty and its producer reported 0
    # -- the n/a-never-0 contract defeated one level up from where pass 3 enforced it.
    logs = tmp_path / "logs"
    logs.mkdir()
    with mock.patch.object(fh.os, "scandir", side_effect=PermissionError("denied")):
        assert fh.count_pending_closures(logs, _BACKLOG_TWO_OPEN) is None
        assert fh.count_review_pending(logs) is None


def test_delta_is_na_when_today_is_partial(tmp_path):
    # terra HIGH, fourth pass — the sharpest of the run. funnel_total is DELIBERATELY
    # partial when a producer is down, so a partial-minus-complete subtraction invented a
    # precise signed number for a change nobody measured. Here the baseline is a complete
    # 90 and today's triage is unavailable, so the naive delta reads -90: the funnel
    # "collapsing" when it was merely unobserved. M1's own series must not invent movement.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    complete = {"triage": 90, "closures": 0, "dispositions": 0, "review_pending": 0,
                "backlog": {"P1": 0, "P2": 0, "P3": 0}, "funnel_total": 90}
    fh.append_load_row(csv_path, date(2026, 8, 4), complete)
    today = dict(complete, triage=None, funnel_total=0)
    assert fh.load_delta(csv_path, today, date(2026, 8, 11)) is None


def test_delta_skips_a_partial_baseline_row(tmp_path):
    # The other direction: a stored row whose own producers were partial is not a
    # baseline, and the scan falls back to an older COMPLETE row.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 1), dict(_COUNTS, funnel_total=50))
    fh.append_load_row(csv_path, date(2026, 8, 4),
                       dict(_COUNTS, triage=None, funnel_total=61))
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) == 14   # vs 08-01's 50


def test_delta_uses_the_newest_run_of_a_same_day_baseline(tmp_path):
    # terra HIGH, fourth pass: `d > best[0]` never replaced an equal date, so the OLDEST
    # run of the baseline day won -- contradicting the function's own "newest stored row"
    # contract. One row per RUN makes same-day rows normal, so this is a live shape.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    fh.append_load_row(csv_path, date(2026, 8, 4), dict(_COUNTS, funnel_total=50))
    fh.append_load_row(csv_path, date(2026, 8, 4), dict(_COUNTS, funnel_total=60))
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) == 4    # 64 - 60, not -14


def test_triage_rejects_well_formed_json_of_the_wrong_shape(tmp_path):
    # terra HIGH, FIFTH pass: `[{"number": "not-an-int"}]` and `[null]` parse as
    # one-element lists, so len() rendered `1 triage` from garbage. Well-formed JSON of
    # the wrong shape is still an unavailable producer, not a measurement of 1.
    for payload in ('[{"number": "not-an-int"}]', "[null]", '["17"]', '[{"id": 4}]'):
        fake = mock.Mock(returncode=0, stdout=payload, stderr="")
        with mock.patch.object(fh.shutil, "which", return_value="gh"), \
             mock.patch.object(fh.subprocess, "run", return_value=fake):
            assert fh.count_open_triage_issues(_git_repo(tmp_path)) is None, payload


def test_delta_rejects_a_corrupt_baseline_cell(tmp_path):
    # terra HIGH, fifth pass: the pass-4 completeness guard tested "not n/a", so a
    # CORRUPT cell sailed through and became a complete baseline -- a hole in exactly
    # the case (damaged history) the guard exists for. Cells must PARSE, not merely
    # differ from the n/a token.
    csv_path = tmp_path / "OPERATOR-LOAD.csv"
    csv_path.write_text(
        ",".join(fh.LOAD_CSV_HEADER) + "\n"
        + "2026-08-01,1,1,1,1,1,1,1,50\n"
        + "2026-08-04,corrupt,0,0,0,0,0,0,90\n", encoding="utf-8")
    # falls back to the 08-01 row (64 - 50), never 64 - 90
    assert fh.load_delta(csv_path, _COUNTS, date(2026, 8, 11)) == 14


def test_review_pending_excludes_prose_headings_and_explanatory_bold(tmp_path):
    # terra HIGH #4: the first cut matched ANY heading or bold run containing the token,
    # so prose ABOUT the marker still counted -- recreating the false-positive class the
    # lever exists to remove. The real shapes are parenthesized-terminal (heading) and
    # colon-plus-id (item).
    (tmp_path / "prose-heading.md").write_text(
        "## Why ARCHITECT-REVIEW-PENDING exists\n", encoding="utf-8")
    (tmp_path / "prose-bold.md").write_text(
        "**ARCHITECT-REVIEW-PENDING is a marker** we use for adjudication.\n",
        encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 0
    # ...and the two real shapes still count.
    (tmp_path / "real-heading.md").write_text(
        "## SELF-ADJUDICATION LOG (ARCHITECT-REVIEW-PENDING)\n", encoding="utf-8")
    (tmp_path / "real-item.md").write_text(
        "**ARCHITECT-REVIEW-PENDING: AC-1** (the hooksPath unset)\n", encoding="utf-8")
    assert fh.count_review_pending(tmp_path) == 2


# --- refresh wiring: one CSV row per digest run -----------------------------

def test_refresh_appends_exactly_one_load_row_per_run(tmp_path):
    # Done-when leg 2 end-to-end, through the real refresh() path.
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    health = logs / "FLEET-HEALTH.md"
    csv_path = logs / "OPERATOR-LOAD.csv"
    with mock.patch.object(fh, "run_audit", return_value=True), \
         mock.patch.object(fh, "drift_summaries", return_value={}), \
         mock.patch.object(fh, "count_open_triage_issues", return_value=3):
        fh.refresh(tmp_path, eco, logs, health, date(2026, 8, 10))
        fh.refresh(tmp_path, eco, logs, health, date(2026, 8, 11))
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3                       # header + one row per run
    assert lines[1].startswith("2026-08-10,3,")
    assert lines[2].startswith("2026-08-11,3,")


def test_refresh_renders_the_load_block_into_the_digest(tmp_path):
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    health = logs / "FLEET-HEALTH.md"
    with mock.patch.object(fh, "run_audit", return_value=True), \
         mock.patch.object(fh, "drift_summaries", return_value={}), \
         mock.patch.object(fh, "count_open_triage_issues", return_value=3):
        fh.refresh(tmp_path, eco, logs, health, date(2026, 8, 11))
    text = health.read_text(encoding="utf-8")
    assert "## Operator load" in text
    assert "3 triage" in text
    assert fh.load_surface_line(health) is not None


def test_refresh_survives_a_gauge_that_explodes(tmp_path):
    # The gauge is a MEASUREMENT bolted onto a health organ. If it breaks, the
    # health digest must still be written -- the gauge is never load-bearing for
    # the thing it measures.
    eco = _seed_states(tmp_path)
    logs = tmp_path / "logs"
    health = logs / "FLEET-HEALTH.md"
    with mock.patch.object(fh, "run_audit", return_value=True), \
         mock.patch.object(fh, "drift_summaries", return_value={}), \
         mock.patch.object(fh, "collect_load", side_effect=RuntimeError("boom")):
        assert fh.refresh(tmp_path, eco, logs, health, date(2026, 8, 11)) is True
    assert health.exists()
    assert "Fleet Health" in health.read_text(encoding="utf-8")


def test_main_prints_the_load_line(tmp_path, capsys):
    health = tmp_path / "FLEET-HEALTH.md"
    health.write_text(fh.build_digest(_STATES, date.today(), "2026-08-11T09:00:00",
                                      None, dict(_COUNTS, delta_7d=4)), encoding="utf-8")
    with mock.patch.object(fh, "_HEALTH_FILE", health), _prompts_dir_matching():
        assert fh.main() == 0
    assert "[load] " in capsys.readouterr().out


def test_main_prints_the_traces_line(tmp_path, capsys):
    health = tmp_path / "FLEET-HEALTH.md"
    health.write_text(fh.build_digest(_STATES, date.today(), "2026-08-11T09:00:00"),
                      encoding="utf-8")
    logs_dir = tmp_path / "logs"
    prompts = logs_dir / "prompts"
    prompts.mkdir(parents=True)
    (prompts / f"{date.today().isoformat()}-lane-h0-trace.md").write_text("x", encoding="utf-8")
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "_LOGS_DIR", logs_dir), \
         _prompts_dir_matching():
        assert fh.main() == 0
    assert "[traces] 1 today" in capsys.readouterr().out


# --- v7 BOOT-INVERSION digest ([#611], protocols/HANDOFF_PROCESS.md §17) ----------------

_ASKS_FIXTURE = """\
**Seed entries, 2026-09-01 (from intake #66):**

```
alpha    asked 2026-09-01  re-asked 3  visible-fix: abc123 (a real change the
         operator can see across two lines)
bravo    asked 2026-09-01  re-asked 2  blocker: a named, dated blocker text
charlie  asked 2026-09-01  re-asked 2  no visible-fix and no blocker here
delta    asked 2026-09-01  re-asked 1  no visible-fix and no blocker here either
```
"""


def test_parse_operator_asks_reads_all_rows_and_joins_continuations():
    entries = fh.parse_operator_asks(_ASKS_FIXTURE)
    assert [e["name"] for e in entries] == ["alpha", "bravo", "charlie", "delta"]
    assert "operator can see across two lines" in entries[0]["body"]


def test_parse_operator_asks_absent_fence_returns_empty():
    assert fh.parse_operator_asks("no registry here\n") == []


def test_ask_is_red_visible_fix_discharges():
    entries = fh.parse_operator_asks(_ASKS_FIXTURE)
    assert fh.ask_is_red(entries[0]) is False  # alpha: re-asked 3, visible-fix present


def test_ask_is_red_blocker_discharges():
    entries = fh.parse_operator_asks(_ASKS_FIXTURE)
    assert fh.ask_is_red(entries[1]) is False  # bravo: re-asked 2, blocker present


def test_ask_is_red_fires_with_no_fix_and_no_blocker():
    entries = fh.parse_operator_asks(_ASKS_FIXTURE)
    assert fh.ask_is_red(entries[2]) is True  # charlie: re-asked 2, neither


def test_ask_is_red_false_below_reasked_threshold():
    entries = fh.parse_operator_asks(_ASKS_FIXTURE)
    assert fh.ask_is_red(entries[3]) is False  # delta: re-asked 1


def test_operator_asks_line_names_red_entries():
    line = fh.operator_asks_line(_ASKS_FIXTURE)
    assert line.startswith("[asks] 1 RED / 4 total")
    assert "charlie" in line


def test_operator_asks_line_all_green():
    text = _ASKS_FIXTURE.replace(
        "charlie  asked 2026-09-01  re-asked 2  no visible-fix and no blocker here",
        "charlie  asked 2026-09-01  re-asked 2  visible-fix: def456 now present")
    line = fh.operator_asks_line(text)
    assert line == "[asks] 0 RED / 4 total"


def test_operator_asks_line_missing_registry_is_reported_not_silent():
    assert "unavailable" in fh.operator_asks_line("nothing here")


def test_funnel_health_line_reports_all_four_numbers(tmp_path):
    fake_fl = mock.Mock()
    fake_fl.LEG_A1, fake_fl.LEG_A2, fake_fl.LEG_B, fake_fl.LEG_C = "a1", "a2", "b", "c"
    measurement = mock.Mock()
    measurement.by_leg.side_effect = lambda leg: {"a1": [1], "a2": [], "b": [2], "c": [3, 4]}[leg]
    fake_fl.measure.return_value = measurement
    fake_bf = mock.Mock()
    fake_bf.load_open_rows.return_value = ["row"] * 5
    fake_bf.unblocked_frontier.return_value = ["row"] * 3
    fake_bf.score_frontier.return_value = ["row"] * 3
    fake_bf.select_batch.return_value = mock.Mock(selected=["row"] * 2)
    with mock.patch.object(fh, "_import_funnel_lifecycle", return_value=fake_fl), \
         mock.patch.object(fh, "_import_boot_frontier", return_value=fake_bf):
        line = fh.funnel_health_line(tmp_path)
    assert line == "[funnel] rot 2 / orphan 2 / unblocked 3 / batch 2 proposed"


def test_funnel_health_line_fail_soft_returns_none(tmp_path):
    with mock.patch.object(fh, "_import_funnel_lifecycle", side_effect=RuntimeError("boom")):
        assert fh.funnel_health_line(tmp_path) is None


def test_main_prints_asks_before_funnel_before_fleet_line(tmp_path, capsys):
    health = tmp_path / "FLEET-HEALTH.md"
    health.write_text(fh.build_digest(_STATES, date.today(), "2026-08-11T09:00:00"),
                      encoding="utf-8")
    handoff_process = tmp_path / "HANDOFF_PROCESS.md"
    handoff_process.write_text(_ASKS_FIXTURE, encoding="utf-8")
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "_HANDOFF_PROCESS_PATH", handoff_process), \
         mock.patch.object(fh, "funnel_health_line", return_value="[funnel] rot 0 / orphan 0 / unblocked 0 / batch 0 proposed"), \
         _prompts_dir_matching():
        assert fh.main() == 0
    out = capsys.readouterr().out
    assert out.index("[asks] ") < out.index("[funnel] ") < out.index("[fleet] ")


# --- CLAUDE_PROMPTS_DIR scope guard (DEFECT E-29 / inbox 013-A) -------------------------
# Closure clause under test: seeded mismatch -> refusal; match -> silent pass.
# The two values are ALWAYS seeded here. Reading the real machine's scopes would make these
# tests assert about the box they run on rather than about the predicate.

_STALE = "C:\\somewhere\\stale"
_TRUE = "Z:\\a dir\\with spaces"


def test_prompts_dir_status_mismatch_refuses():
    verdict, line = fh.prompts_dir_status(_STALE, _TRUE)
    assert verdict == fh.PROMPTS_REFUSED
    assert line.startswith("[prompts] REFUSED")


def test_prompts_dir_refusal_names_BOTH_values():
    """E-29's stated reason for the second value: naming only the correct one leaves the
    reader unable to tell a stale process from a wrong User setting."""
    _, line = fh.prompts_dir_status(_STALE, _TRUE)
    assert _STALE in line and _TRUE in line


def test_prompts_dir_refusal_is_one_line():
    _, line = fh.prompts_dir_status(_STALE, _TRUE)
    assert "\n" not in line


def test_prompts_dir_status_match_is_ok():
    verdict, line = fh.prompts_dir_status(_TRUE, _TRUE)
    assert verdict == fh.PROMPTS_OK
    assert "REFUSED" not in line


def test_prompts_dir_trailing_separator_is_not_staleness():
    assert fh.prompts_dir_status(_TRUE + "\\", _TRUE)[0] == fh.PROMPTS_OK


def test_prompts_dir_case_difference_is_not_staleness():
    assert fh.prompts_dir_status(_TRUE.upper(), _TRUE.lower())[0] == fh.PROMPTS_OK


def test_prompts_dir_surrounding_quotes_are_not_staleness():
    assert fh.prompts_dir_status(f'"{_TRUE}"', _TRUE)[0] == fh.PROMPTS_OK


def test_prompts_dir_unset_process_value_refuses():
    """013-A's predicate: unset IS a difference from a set User value, because an unset
    process value falls through to the launcher fallback silently."""
    verdict, line = fh.prompts_dir_status(None, _TRUE)
    assert verdict == fh.PROMPTS_REFUSED
    assert _TRUE in line


def test_prompts_dir_empty_string_counts_as_unset():
    assert fh.prompts_dir_status("   ", _TRUE)[0] == fh.PROMPTS_REFUSED


def test_prompts_dir_both_unset_warns_and_is_never_silent():
    verdict, line = fh.prompts_dir_status(None, None)
    assert verdict == fh.PROMPTS_UNSET
    assert line.strip()
    assert "REFUSED" not in line


def test_prompts_dir_no_user_scope_is_unverifiable_not_ok():
    """The shape 013-A's sketch does not cover. Nothing was compared, so calling it a pass
    would be the silent conflation the whole defect is about."""
    verdict, line = fh.prompts_dir_status(_STALE, None)
    assert verdict == fh.PROMPTS_NO_USER_SCOPE
    assert verdict != fh.PROMPTS_OK
    assert "unverifiable" in line


def test_guard_module_hard_codes_no_path():
    """013's standing rule: the variable is the source, never a path. Both values are read;
    neither is compared against a spelled constant."""
    source = _P.read_text(encoding="utf-8")
    assert not re.search(r"[A-Za-z]:\\\\", source)
    assert "Downloads" not in source


# --- the PreToolUse leg: the one that actually refuses ----------------------------------

def test_prompts_guard_exits_2_on_a_seeded_mismatch(capsys):
    with mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_STALE, _TRUE)):
        assert fh.prompts_guard() == 2
    err = capsys.readouterr().err
    assert "[prompts] REFUSED" in err and _STALE in err and _TRUE in err


def test_prompts_guard_passing_says_so_on_stdout_and_stays_silent_on_stderr(capsys):
    """A pass PROVES it evaluated, and the proof is the marker.

    Added 2026-09-11 by the fresh Codex review of this branch (HIGH-1). Before it, the
    guard's pass was pure SILENCE plus an exit of 0 -- and silence-plus-0 is precisely
    what a `python` that never ran this file also produces. Any shim, wrapper or wrong
    interpreter first on PATH satisfied the old hook command's pass test, so the hook
    permitted the tool call while believing it had checked one. Under the AX15-1 posture
    that is the worst remaining hole: declared enforcement, no enforcement.

    The marker closes it POSITIVELY -- only this file can emit it, so the hook can require
    evidence rather than infer it from the absence of an error. Note the split of streams
    is load-bearing and is what keeps the original no-noise argument intact: the marker
    goes to STDOUT, which a PreToolUse hook shows only in transcript mode, while STDERR --
    the stream that reaches the model on a refusal -- stays empty on every passing verdict.
    """
    with mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_TRUE, _TRUE)):
        assert fh.prompts_guard() == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == fh.GUARD_EVALUATED_MARKER
    assert captured.err == ""


def test_prompts_guard_marks_a_pass_it_had_nothing_to_compare(capsys):
    """Runs once per TOOL CALL, so STDERR stays clean -- a warning line here would be
    noise, not signal, and the SessionStart leg has already printed it once.

    The marker is emitted here too, and that is deliberate rather than incidental: an
    unset scope is a guard that RAN and reached a non-refusing verdict, which is exactly
    what the marker attests. Withholding it on this path would refuse every consumer that
    has never set the variable -- the same over-reach the fail-closed inversion was
    explicitly scoped to avoid (see the commit that landed AX15-1).
    """
    with mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(None, None)):
        assert fh.prompts_guard() == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == fh.GUARD_EVALUATED_MARKER
    assert captured.err == ""


def test_prompts_guard_never_marks_a_refusal_as_evaluated(capsys):
    """The marker means "evaluated and NOT refusing". If a refusal carried it too, the
    hook's pass test would match on the very call the guard was refusing -- turning the
    positive proof into a bypass. Pinned on both refusal routes: the verdict and the raise.
    """
    with mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_STALE, _TRUE)):
        assert fh.prompts_guard() == 2
    captured = capsys.readouterr()
    assert fh.GUARD_EVALUATED_MARKER not in captured.out + captured.err

    with mock.patch.object(fh, "read_prompts_dir_scopes", side_effect=RuntimeError("boom")):
        assert fh.prompts_guard() == 2
    captured = capsys.readouterr()
    assert fh.GUARD_EVALUATED_MARKER not in captured.out + captured.err


def test_prompts_guard_refuses_when_it_cannot_run(capsys):
    """Fail-CLOSED on the guard's own crash, per AX15-1 (2026-09-11, batch X lane W-2').

    This test asserted the OPPOSITE until that ruling, and the inverted form is kept
    deliberately as the record of the reversal. The old argument was that a guard which
    bricked every tool call because it raised would be worse than the defect it guards.
    AX15-1 answers it on a different axis -- *"a guard that permits when it cannot run is
    declared enforcement without enforcement"* -- and pays for the inversion with the
    narrowed matcher (the break-glass stays ungated) and with a refusal that teaches.

    The exception TEXT must survive into the message: a refusal whose cause is
    `RuntimeError('boom')` is diagnosable, one that says only "unavailable" is not.
    """
    with mock.patch.object(fh, "read_prompts_dir_scopes", side_effect=RuntimeError("boom")):
        assert fh.prompts_guard() == 2
    err = capsys.readouterr().err
    assert "REFUSED" in err and "Cause:" in err and "Fix:" in err
    assert "boom" in err, f"the refusal swallowed the underlying error: {err!r}"


def test_main_dispatches_the_guard_flag():
    with mock.patch.object(fh, "prompts_guard", return_value=2) as guard:
        assert fh.main(["--prompts-guard"]) == 2
    assert guard.call_count == 1


# --- the SessionStart PREFLIGHT: verify once what the per-call guard needs ---------------
#
# AX15-1's second sentence: *"A SessionStart check verifies interpreter + guard script once
# and reports loudly, so per-call refusals are the exception."* It exists BECAUSE the leg
# above now fails closed -- without it the first news of a missing interpreter is a refused
# tool call with no preceding warning, which is MA-1's presentation all over again.
#
# RED-first (ADR-108 section B): every test below fails on today's module, which has no
# preflight at all.

def test_resolve_guard_script_prefers_the_project_dir(tmp_path):
    """The preflight must reproduce the HOOK's resolution order, not invent its own -- a
    preflight that checks a different path than the hook reaches is worse than none."""
    project = tmp_path / "project" / "scripts"
    project.mkdir(parents=True)
    (project / "fleet_health.py").write_text("", encoding="utf-8")
    cwd = tmp_path / "cwd" / "scripts"
    cwd.mkdir(parents=True)
    (cwd / "fleet_health.py").write_text("", encoding="utf-8")
    found = fh.resolve_guard_script(str(tmp_path / "project"), str(tmp_path / "cwd"))
    assert found == project / "fleet_health.py"


def test_resolve_guard_script_falls_back_to_cwd(tmp_path):
    """`[ -f "$g" ] || g="./scripts/..."` -- the hook's SECOND leg, which is what a
    non-Claude reader with no CLAUDE_PROJECT_DIR actually takes."""
    cwd = tmp_path / "cwd" / "scripts"
    cwd.mkdir(parents=True)
    (cwd / "fleet_health.py").write_text("", encoding="utf-8")
    assert fh.resolve_guard_script(str(tmp_path / "nowhere"), str(tmp_path / "cwd")) == (
        cwd / "fleet_health.py")
    assert fh.resolve_guard_script(None, str(tmp_path / "cwd")) == cwd / "fleet_health.py"


def test_resolve_guard_script_returns_none_when_neither_leg_resolves(tmp_path):
    assert fh.resolve_guard_script(str(tmp_path / "a"), str(tmp_path / "b")) is None


def test_guard_preflight_reports_ok_with_both_facts_named(tmp_path):
    script = tmp_path / "scripts" / "fleet_health.py"
    verdict, line = fh.guard_preflight_status(script, "/usr/bin/python")
    assert verdict == fh.GUARD_PREFLIGHT_OK
    assert "fleet_health.py" in line and "python" in line


def test_guard_preflight_no_script_names_cause_and_fix():
    """Loud, and actionable: AX15-2's deploy defect is exactly this shape on a consumer --
    the hook block carried, the script not. The line has to say which half is missing."""
    verdict, line = fh.guard_preflight_status(None, "/usr/bin/python")
    assert verdict == fh.GUARD_PREFLIGHT_NO_SCRIPT
    assert "Cause:" in line and "Fix:" in line
    assert "scripts/fleet_health.py" in line


def test_guard_preflight_no_interpreter_names_cause_and_fix(tmp_path):
    verdict, line = fh.guard_preflight_status(tmp_path / "scripts" / "fleet_health.py", None)
    assert verdict == fh.GUARD_PREFLIGHT_NO_INTERPRETER
    assert "Cause:" in line and "Fix:" in line
    assert "python" in line


def test_guard_preflight_says_what_it_will_cost(tmp_path):
    """The point of the preflight is that the reader learns the CONSEQUENCE before paying
    it once per tool call. Both failing verdicts must say the guard will refuse."""
    for args in ((None, "/usr/bin/python"), (tmp_path / "s" / "fleet_health.py", None)):
        _verdict, line = fh.guard_preflight_status(*args)
        assert "refuse" in line.lower(), f"preflight hid the consequence: {line!r}"


def test_hook_path_drops_the_venv_uv_prepends(tmp_path):
    """The preflight must measure the PATH the HOOK sees, not this process's.

    SessionStart runs under `uv run --locked`, which prepends the venv's script dir;
    PreToolUse runs on the system interpreter and does not. Measuring the venv would report
    green on a machine whose plain shell has no python -- green on exactly the
    configuration where every tool call is about to be refused.
    """
    venv = tmp_path / "proj" / ".venv"
    entries = [str(venv / "Scripts"), str(tmp_path / "sys" / "bin")]
    got = fh.hook_path({"PATH": os.pathsep.join(entries), "VIRTUAL_ENV": str(venv)})
    assert got == str(tmp_path / "sys" / "bin")


def test_hook_path_is_the_whole_path_when_no_venv_is_active(tmp_path):
    """It drops the venv and NOTHING else -- this is not an attempt to reconstruct the
    hook's environment, and a preflight that silently narrowed PATH further would start
    reporting failures the hook would not have."""
    raw = os.pathsep.join([str(tmp_path / "a"), str(tmp_path / "b")])
    assert fh.hook_path({"PATH": raw}) == raw


def test_hook_path_keeps_a_sibling_that_merely_shares_a_prefix(tmp_path):
    """`.venv-old/Scripts` is not inside `.venv`. String-prefix matching without the
    separator would drop it, which would be the narrowing the test above forbids."""
    venv = tmp_path / ".venv"
    sibling = str(tmp_path / ".venv-old" / "Scripts")
    got = fh.hook_path({"PATH": os.pathsep.join([str(venv / "Scripts"), sibling]),
                        "VIRTUAL_ENV": str(venv)})
    assert got == sibling


def test_hook_path_keeps_an_empty_entry_that_posix_reads_as_the_cwd(tmp_path):
    """An EMPTY `PATH` component is not padding -- on POSIX it means the current
    directory, and dropping it changes where the interpreter is looked up.

    Added 2026-09-11 by the fresh Codex review of this branch (MEDIUM). The filter existed
    only to stop `normpath("")` -- which returns `"."` -- from being compared against the
    venv prefix, and it silently took the empty component with it. The two tests above
    forbid narrowing PATH beyond the venv; this is a case of exactly that, so it is the
    same rule applied to the component whose emptiness is its meaning. Hook commands run
    through a POSIX shell here (measured 2026-09-11), so the semantics are live, not
    theoretical.
    """
    venv = tmp_path / ".venv"
    raw = os.pathsep.join([str(venv / "Scripts"), "", str(tmp_path / "sys" / "bin")])
    got = fh.hook_path({"PATH": raw, "VIRTUAL_ENV": str(venv)})
    assert got == os.pathsep.join(["", str(tmp_path / "sys" / "bin")])
    assert "" in got.split(os.pathsep), f"the cwd component was dropped: {got!r}"


def test_main_prints_the_preflight_line(tmp_path, capsys):
    """It renders on the SessionStart leg, beside the [prompts] banner -- a preflight
    nobody reaches is not a preflight (the same argument 013-A made for that banner).

    `_HEALTH_FILE` is patched to a FRESH temp digest, as every other `main()` test here
    does, and that is not decoration: without it `is_stale()` reads the live digest and
    `main()` can take the `refresh()` branch, i.e. spawn the real cross-repo audit from a
    unit test. Measured the hard way while writing this -- the unpatched form ran for
    minutes before being killed.
    """
    health = _digest_at(tmp_path)
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(None, None)), \
         mock.patch.object(fh, "read_guard_preflight", return_value=(None, "python")):
        fh.main([])
    out = capsys.readouterr().out
    assert "[prompts-guard] PREFLIGHT FAILED" in out


def test_main_returns_two_on_a_failed_preflight(tmp_path, capsys):
    """An honest non-zero, not a block: a SessionStart hook CANNOT refuse (measured -- see
    the module's own hook-wiring block), so this is the same shape as the PROMPTS_REFUSED
    exit it sits beside. It becomes a real signal for free if a later CLI honours it.

    The prompts verdict is deliberately a PASSING one, so the 2 can only have come from the
    preflight -- a seeded mismatch would return 2 either way and prove nothing.
    """
    health = _digest_at(tmp_path)
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(None, None)), \
         mock.patch.object(fh, "read_guard_preflight", return_value=(None, "python")):
        assert fh.main([]) == 2
    capsys.readouterr()


def test_main_returns_zero_when_both_the_verdict_and_the_preflight_are_clean(tmp_path,
                                                                             capsys):
    """The other side of the exit contract, without which the test above is satisfied by a
    `main()` that always returns 2."""
    health = _digest_at(tmp_path)
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_TRUE, _TRUE)), \
         mock.patch.object(fh, "read_guard_preflight",
                           return_value=(tmp_path / "scripts" / "fleet_health.py",
                                         "python")):
        assert fh.main([]) == 0
    assert "[prompts-guard] preflight OK" in capsys.readouterr().out


# --- the SessionStart leg: loud banner, honest (non-blocking) exit ----------------------

def _digest_at(tmp_path):
    health = tmp_path / "FLEET-HEALTH.md"
    health.write_text(fh.build_digest(_STATES, date.today(), "2026-08-11T09:00:00"),
                      encoding="utf-8")
    return health


def test_main_renders_the_prompts_line_first_of_all(tmp_path, capsys):
    """Above OPERATOR ASKS and everything below it -- a boot banner nobody reaches is not
    a banner."""
    health = _digest_at(tmp_path)
    handoff_process = tmp_path / "HANDOFF_PROCESS.md"
    handoff_process.write_text(_ASKS_FIXTURE, encoding="utf-8")
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "_HANDOFF_PROCESS_PATH", handoff_process), \
         mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_STALE, _TRUE)):
        fh.main([])
    out = capsys.readouterr().out
    assert out.index("[prompts] ") < out.index("[asks] ") < out.index("[fleet] ")


def test_main_returns_2_on_a_seeded_mismatch(tmp_path, capsys):
    health = _digest_at(tmp_path)
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_STALE, _TRUE)):
        assert fh.main([]) == 2
    captured = capsys.readouterr()
    assert "[prompts] REFUSED" in captured.out
    # also on stderr: stdout is folded into context, stderr is the operator's own surface
    assert "[prompts] REFUSED" in captured.err


def test_main_returns_0_and_stays_quiet_on_a_match(tmp_path, capsys):
    health = _digest_at(tmp_path)
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_TRUE, _TRUE)):
        assert fh.main([]) == 0
    captured = capsys.readouterr()
    assert "[prompts] OK" in captured.out
    assert "REFUSED" not in captured.out and "REFUSED" not in captured.err


def test_main_still_returns_2_when_the_digest_below_it_blows_up(tmp_path, capsys):
    """The refusal outranks the digest's own fail-soft return: a stale value must not be
    laundered into a 0 by an unrelated error further down."""
    with mock.patch.object(fh, "read_prompts_dir_scopes", return_value=(_STALE, _TRUE)), \
         mock.patch.object(fh, "is_stale", side_effect=RuntimeError("boom")):
        assert fh.main([]) == 2


def test_main_survives_a_guard_that_raises(tmp_path, capsys):
    """Fail-soft the other way: the digest is never lost to the guard."""
    health = _digest_at(tmp_path)
    with mock.patch.object(fh, "_HEALTH_FILE", health), \
         mock.patch.object(fh, "read_prompts_dir_scopes", side_effect=RuntimeError("boom")):
        assert fh.main([]) == 0
    captured = capsys.readouterr()
    assert "[fleet] " in captured.out
    assert "WARNING" in captured.err


# --- the User-scope reader --------------------------------------------------------------

def test_read_user_scope_returns_none_when_the_value_is_absent():
    winreg = pytest.importorskip("winreg")
    with mock.patch.object(winreg, "QueryValueEx", side_effect=OSError("no value")):
        assert fh.read_user_scope("A_NAME_NO_ONE_SET") is None


def test_read_user_scope_returns_none_when_the_key_cannot_be_opened():
    winreg = pytest.importorskip("winreg")
    with mock.patch.object(winreg, "OpenKey", side_effect=OSError("denied")):
        assert fh.read_user_scope() is None


def test_read_user_scope_returns_a_plain_string_value():
    """The success path -- the boundary that actually supplies the comparison value.
    Without this the reader could regress to always-None and every test above would still
    pass, because a None resolution is a non-refusing verdict."""
    winreg = pytest.importorskip("winreg")
    with mock.patch.object(winreg, "QueryValueEx", return_value=(_TRUE, winreg.REG_SZ)):
        assert fh.read_user_scope() == _TRUE


def test_read_user_scope_expands_a_reg_expand_sz_value():
    winreg = pytest.importorskip("winreg")
    with mock.patch.dict(os.environ, {"E29_FIXTURE": "expanded"}), \
         mock.patch.object(winreg, "QueryValueEx",
                           return_value=("%E29_FIXTURE%\\tail", winreg.REG_EXPAND_SZ)):
        assert fh.read_user_scope() == "expanded\\tail"


def test_read_user_scope_treats_an_empty_value_as_absent():
    winreg = pytest.importorskip("winreg")
    with mock.patch.object(winreg, "QueryValueEx", return_value=("", winreg.REG_SZ)):
        assert fh.read_user_scope() is None
