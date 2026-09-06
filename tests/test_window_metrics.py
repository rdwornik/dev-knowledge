"""Tests for scripts/window_metrics.py ([#461] — mechanize the six window metrics).

The defect [#461] names: every one of the six was assembled BY HAND for the [#382] close, and a
hand-assembled figure is a claim, not a measurement — the window brief carried a net-delta of +6
against a verified +3. So the tests pin two things: that each derivable metric is computed from
committed state, and that each NON-derivable one says so in the report rather than carrying a
number nobody can reproduce.

The pure functions are tested against fixtures; the git-reading wrappers are exercised once
against the live repo so the report is not merely internally consistent.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


wm = _load("window_metrics")


# --- metric 2: net backlog delta (the one the brief got wrong) ---------------

_BASE = "# Backlog\n- [#1] a\n- [#2] b\n- [#3] c\n"
_HEAD = "# Backlog\n- [#2] b\n- [#3] c\n- [#4] d\n- [#5] e\n"


def test_backlog_delta_separates_filed_closed_and_net():
    """+2 filed, -1 closed, net +1 — the three numbers the brief conflated into one."""
    d = wm.backlog_delta(_BASE, _HEAD)
    assert (d["start"], d["end"], d["net"]) == (3, 4, 1)
    assert d["filed"] == ["#4", "#5"]
    assert d["closed"] == ["#1"]


def test_backlog_delta_counts_only_task_rows():
    """Story/theme headings and prose must not inflate the count."""
    text = "# Backlog\n### [S1] a story\nSo that prose.\n- [#7] real row\n  - [#8] indented\n"
    assert wm.count_backlog_rows(text) == 1


# --- metric 1: boot round-trips ---------------------------------------------


def test_boot_round_trips_reads_the_spec_version():
    assert wm.boot_round_trips("Version: 6.0.1\n")[0] == 1
    assert wm.boot_round_trips("Version: 5.7\n")[0] == 10


def test_boot_round_trips_is_honest_about_an_unknown_version():
    """An unmapped major must not silently borrow a neighbour's number."""
    n, note = wm.boot_round_trips("Version: 9.0\n")
    assert n is None and "unmapped" in note.lower()


# --- metrics 4 and 5: the ones that must NOT carry a computed number --------


def test_windows_to_cutoff_is_declared_a_judgment_input():
    m = wm.collect(_BASE, _HEAD, spec_text="Version: 6.0.1\n", merges=[], boot_bytes=1,
                   paste_count=0, drift_runs=None)
    assert m["windows_to_cutoff"]["value"] is None
    assert "judgment" in m["windows_to_cutoff"]["basis"].lower()


def test_drift_report_runs_reports_not_instrumented(tmp_path):
    """desired_state_report prints to stdout and writes no artifact, so runs leave no committed
    trace. The report must say that rather than print 0 — a 0 would read as 'measured none'."""
    m = wm.collect(_BASE, _HEAD, spec_text="Version: 6.0.1\n", merges=[], boot_bytes=1,
                   paste_count=0, drift_runs=None)
    assert m["drift_report_runs"]["value"] is None
    assert "not-instrumented" in m["drift_report_runs"]["basis"]


def test_render_marks_uncomputed_metrics_and_never_prints_a_bare_zero():
    m = wm.collect(_BASE, _HEAD, spec_text="Version: 6.0.1\n", merges=["a"], boot_bytes=100,
                   paste_count=0, drift_runs=None)
    out = wm.render(m, "base..head")
    assert "NOT COMPUTED" in out
    for line in out.splitlines():
        if "drift-report runs" in line or "windows to cutoff" in line:
            assert "NOT COMPUTED" in line


def test_report_is_ascii_only():
    """cp1252 console discipline ([#470]) — the report is printed, so a non-cp1252 glyph
    crashes exactly the run that produces it."""
    m = wm.collect(_BASE, _HEAD, spec_text="Version: 6.0.1\n", merges=["m"], boot_bytes=9,
                   paste_count=1, drift_runs=None)
    wm.render(m, "base..head").encode("ascii")


# --- metric 6: byte budgets --------------------------------------------------


def test_byte_budget_reports_usage_against_the_live_budget():
    b = wm.byte_budget(16842, 18000)
    assert b["bytes"] == 16842 and b["budget"] == 18000 and b["pct"] == 94


def test_paste_budget_is_single_sourced_from_assemble_paste():
    """[#611]: the two-rival-budgets defect (this module's own `paste_budget: int = 65_000`
    default disagreeing with assemble_paste's `_SIZE_WARN_BYTES = 48_000`) is closed by
    importing ONE constant rather than declaring a second one -- so `collect`'s default must
    equal `assemble_paste.PASTE_BYTE_CEILING` (20,000), never a locally re-derived number."""
    m = wm.collect(_BASE, _HEAD, spec_text="Version: 6.0.1\n", merges=[], boot_bytes=1,
                   paste_count=0, drift_runs=None)
    assert wm.PASTE_BYTE_CEILING == 20_000
    assert f"warn budget {wm.PASTE_BYTE_CEILING}" in m["boot_paste_bytes"]["basis"]


# --- live wiring -------------------------------------------------------------


@pytest.mark.live_repo
def test_live_report_renders_for_a_real_range():
    out = wm.report_for_range("HEAD~1..HEAD")
    assert "Window metrics" in out and "net backlog delta" in out
    out.encode("ascii")


# --- item 7 scorecard (docs/intake/2026-09-05-tech-handoff-process-v71-amendment-pack.md,
# CANDIDATE per protocols/STANDING_RULINGS.md AE-2 -- ten rows is a ceiling, not a quota) ---

_ASKS_NONE_RED = [{"name": "a", "date": "2026-09-01", "reasked": 0, "body": ""}]
_ASKS_ONE_RED = [
    {"name": "a", "date": "2026-09-01", "reasked": 2, "body": ""},
    {"name": "b", "date": "2026-09-01", "reasked": 0, "body": ""},
]


def test_scorecard_rows_closed_touched_reuses_backlog_delta():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0)
    assert m["rows_closed_touched"]["value"] == 1  # #1 closed, per _BASE/_HEAD above


def test_scorecard_asks_red_reasked_reuses_fleet_health():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_ONE_RED, boot_bytes=1,
                              paste_count=0)
    assert m["asks_red_reasked"]["value"] == 1
    assert "1 RED / 2 total" in m["asks_red_reasked"]["basis"]


def test_scorecard_bundle_bytes_pct_matches_boot_paste_bytes_figures():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=9000,
                              paste_count=2)
    assert m["bundle_bytes_pct"]["value"] == 9000
    assert "50%" in m["bundle_bytes_pct"]["basis"]


def test_scorecard_declares_six_rows_not_computed_never_a_bare_zero():
    """AE-2: ten is a ceiling, not a quota. Six rows have no existing computed surface and
    must say NOT COMPUTED, never a number that looks measured."""
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0)
    not_computed_keys = {"hard_fail_warn_trend", "failing_nodeids_baseline",
                          "p1_premerge_regressions", "time_to_merge_per_lane",
                          "pct_lanes_codespace", "consumers_zero_fail",
                          "tokens_by_model_class"}
    for key in not_computed_keys:
        assert m[key]["value"] is None, key
        assert "NOT COMPUTED" in m[key]["basis"], key


def test_render_scorecard_prints_ten_rows_and_marks_uncomputed():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_ONE_RED, boot_bytes=1,
                              paste_count=0)
    out = wm.render_scorecard(m, "base..head")
    assert len(wm._SCORECARD_LABELS) == 10
    for _, label in wm._SCORECARD_LABELS:
        assert f"**{label}:**" in out
    assert out.count("NOT COMPUTED") >= 6


def test_scorecard_report_is_ascii_only():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_ONE_RED, boot_bytes=1,
                              paste_count=0)
    wm.render_scorecard(m, "base..head").encode("ascii")


@pytest.mark.live_repo
def test_live_scorecard_renders_for_a_real_range():
    out = wm.scorecard_for_range("HEAD~1..HEAD")
    assert "Scorecard" in out and "asks RED/re-asked" in out
    out.encode("ascii")
