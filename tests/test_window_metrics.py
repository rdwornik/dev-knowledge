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


# --- live wiring -------------------------------------------------------------


@pytest.mark.live_repo
def test_live_report_renders_for_a_real_range():
    out = wm.report_for_range("HEAD~1..HEAD")
    assert "Window metrics" in out and "net backlog delta" in out
    out.encode("ascii")
