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


def test_scorecard_declares_uncomputable_rows_never_a_bare_zero():
    """AE-2: ten is a ceiling, not a quota. A row with no existing committed surface says
    NOT COMPUTED, never a number that looks measured. These four have none even when every
    optional surface is supplied, so they are the permanent floor of the uncomputed set."""
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0)
    not_computed_keys = {"failing_nodeids_baseline", "p1_premerge_regressions",
                          "pct_lanes_codespace", "tokens_by_model_class"}
    for key in not_computed_keys:
        assert m[key]["value"] is None, key
        assert "NOT COMPUTED" in m[key]["basis"], key


def test_scorecard_rows_go_uncomputed_when_their_surface_is_absent():
    """The two history-fed rows and the merge-timing row degrade to NOT COMPUTED rather
    than to 0 -- an unreadable surface is not a measurement of none."""
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0, fleet_checks=None, merge_stats=None)
    for key in ("hard_fail_warn_trend", "consumers_zero_fail", "time_to_merge_per_lane"):
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


# --- the three addenda: one placeholder by instruction, two from inbox 031 section 3 ----


def test_addenda_are_beside_the_ten_not_members_of_it():
    """The item-7 roster is TEN. The addenda live in their own list so "ten numbers" stays
    literally countable in the output -- a scorecard of thirteen labelled rows that cannot
    say which ten are the ten has lost the property the bar is stated in."""
    assert len(wm._SCORECARD_LABELS) == 10
    assert len(wm._SCORECARD_ADDENDA_LABELS) == 3
    ten = {k for k, _ in wm._SCORECARD_LABELS}
    assert ten.isdisjoint({k for k, _ in wm._SCORECARD_ADDENDA_LABELS})


def test_tokens_saved_by_offload_is_a_printed_placeholder_zero():
    """Carried by instruction as a LINE with the value 0 -- not computed, and its absence
    of instrumentation is declared in the basis so the 0 cannot be read as a measurement."""
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0)
    assert m["tokens_saved_by_offload"]["value"] == 0
    assert "PLACEHOLDER" in m["tokens_saved_by_offload"]["basis"]


def test_031_addenda_declare_their_missing_surface():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0)
    for key in ("turns_per_window", "connector_bytes_per_window"):
        assert m[key]["value"] is None, key
        assert "NOT COMPUTED" in m[key]["basis"], key


def test_render_scorecard_prints_all_thirteen_rows():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_ONE_RED, boot_bytes=1,
                              paste_count=0)
    out = wm.render_scorecard(m, "base..head")
    for _, label in wm._SCORECARD_LABELS + wm._SCORECARD_ADDENDA_LABELS:
        assert f"**{label}:**" in out
    assert "**tokens saved by offload (placeholder):** 0" in out


# --- the committed surfaces the two history rows and the merge row read -----------------

_HISTORY_TWO_RUNS = """### 2026-09-01 — 2026-09-01T09:00:00

| Check | Status | Evidence |
|---|---|---|
| vision_md | pass | fine |
| doc_rot | warn | drifting |
| hooks_armed | fail | not armed |
| floor_integrity | n/a | not adopted |

### 2026-09-05 — 2026-09-05T09:00:00

| Check | Status | Evidence |
|---|---|---|
| vision_md | pass | fine |
| doc_rot | warn | drifting |
| doc_structure | warn | also drifting |
| hooks_armed | pass | armed now |
"""


def test_parse_history_runs_reads_each_run_block_oldest_first():
    runs = wm.parse_history_runs(_HISTORY_TWO_RUNS)
    assert [r["date"] for r in runs] == ["2026-09-01", "2026-09-05"]
    assert (runs[0]["pass"], runs[0]["fail"], runs[0]["warn"]) == (1, 1, 1)
    assert (runs[1]["pass"], runs[1]["fail"], runs[1]["warn"]) == (2, 0, 2)


def test_parse_history_runs_does_not_fold_n_a_into_pass():
    """`n/a` means the check did not apply to this repo. Counting it as a pass would
    inflate a green reading with checks that never ran."""
    runs = wm.parse_history_runs(_HISTORY_TWO_RUNS)
    assert runs[0]["pass"] == 1          # four rows, one of them n/a


def test_fleet_check_counts_carries_the_direction_not_just_the_level():
    """AE-2: the trend IS the feature. An absolute WARN count moves with the calendar
    (doc_rot) while the tree does not, so the level alone is unreadable."""
    counts = wm.fleet_check_counts({"repo-a": wm.parse_history_runs(_HISTORY_TWO_RUNS)})
    assert (counts["fail"], counts["warn"], counts["total"]) == (0, 2, 2)
    assert counts["delta_fail"] == -1 and counts["delta_warn"] == 1
    assert counts["compared"] == 1


def test_fleet_check_counts_declares_an_uncomparable_direction():
    """One run and no predecessor is not a direction of zero."""
    one_run = [{"date": "2026-09-05", "pass": 1, "fail": 2, "warn": 0}]
    counts = wm.fleet_check_counts({"repo-a": one_run})
    assert counts["fail"] == 2
    assert counts["delta_fail"] is None and counts["delta_warn"] is None


def test_fleet_check_counts_compares_only_repos_present_in_both_points():
    """A repo appearing for the first time must not masquerade as a rise."""
    counts = wm.fleet_check_counts({
        "repo-a": wm.parse_history_runs(_HISTORY_TWO_RUNS),
        "new-repo": [{"date": "2026-09-05", "pass": 0, "fail": 9, "warn": 0}],
    })
    assert counts["fail"] == 9 and counts["repos"] == 2
    assert counts["compared"] == 1 and counts["delta_fail"] == -1


def test_fleet_check_counts_is_none_when_nothing_was_read():
    assert wm.fleet_check_counts({}) is None
    assert wm.fleet_check_counts({"repo-a": []}) is None


def test_consumers_zero_fail_counts_repos_not_checks():
    counts = wm.fleet_check_counts({
        "green": [{"date": "2026-09-05", "pass": 3, "fail": 0, "warn": 1}],
        "red": [{"date": "2026-09-05", "pass": 1, "fail": 2, "warn": 0}],
    })
    assert counts["zero_fail_repos"] == 1 and counts["repos"] == 2
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0, fleet_checks=counts)
    assert m["consumers_zero_fail"]["value"] == 1
    assert "1 of 2 repo(s)" in m["consumers_zero_fail"]["basis"]
    assert m["hard_fail_warn_trend"]["value"] == 3   # 2 fail + 1 warn


def test_merge_duration_stats_is_none_for_an_empty_range():
    """No lane merged is not a measurement of zero hours -- a 0 would read as
    'merged instantly'."""
    assert wm.merge_duration_stats([]) is None


def test_merge_duration_stats_reports_median_and_max():
    s = wm.merge_duration_stats([1.0, 5.0, 3.0])
    assert s == {"lanes": 3, "median_h": 3.0, "max_h": 5.0}
    assert wm.merge_duration_stats([2.0, 4.0])["median_h"] == 3.0


def test_time_to_merge_row_reads_the_merge_stats():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_NONE_RED, boot_bytes=1,
                              paste_count=0,
                              merge_stats=wm.merge_duration_stats([1.0, 5.0, 3.0]))
    assert m["time_to_merge_per_lane"]["value"] == 3.0
    assert "3 lane(s)" in m["time_to_merge_per_lane"]["basis"]


def test_read_fleet_history_sees_a_dot_prefixed_repo_directory(tmp_path):
    """`ecosystem/.dev-knowledge/` is the hub's own row. A shell-style glob drops a leading
    dot silently, which would under-count the fleet by exactly the repo doing the counting."""
    for name in (".dev-knowledge", "win-tooling"):
        hist = tmp_path / name / "history"
        hist.mkdir(parents=True)
        (hist / "2026-09-05.md").write_text(_HISTORY_TWO_RUNS, encoding="utf-8")
    runs = wm.read_fleet_history(tmp_path)
    assert set(runs) == {".dev-knowledge", "win-tooling"}
    assert len(runs[".dev-knowledge"]) == 2


def test_read_fleet_history_keeps_only_the_newest_files(tmp_path):
    hist = tmp_path / "repo" / "history"
    hist.mkdir(parents=True)
    for day in ("2026-09-01", "2026-09-02", "2026-09-03"):
        (hist / f"{day}.md").write_text(
            f"### {day} — {day}T09:00:00\n\n| Check | Status | Evidence |\n"
            "|---|---|---|\n| vision_md | pass | fine |\n", encoding="utf-8")
    runs = wm.read_fleet_history(tmp_path, keep=2)
    assert [r["date"] for r in runs["repo"]] == ["2026-09-02", "2026-09-03"]


def test_read_fleet_history_is_empty_when_the_directory_is_absent(tmp_path):
    assert wm.read_fleet_history(tmp_path / "nope") == {}


def test_scorecard_report_is_ascii_only():
    m = wm.collect_scorecard(_BASE, _HEAD, asks_entries=_ASKS_ONE_RED, boot_bytes=1,
                              paste_count=0)
    wm.render_scorecard(m, "base..head").encode("ascii")


@pytest.mark.live_repo
def test_live_scorecard_renders_for_a_real_range():
    out = wm.scorecard_for_range("HEAD~1..HEAD")
    assert "Scorecard" in out and "asks RED/re-asked" in out
    out.encode("ascii")


@pytest.mark.live_repo
def test_live_scorecard_prints_every_row_including_the_addenda():
    """The bar is that each row is PRINTED -- a scorecard that computes some and narrates
    the rest has not met it. Against the live repo, all thirteen labels appear."""
    out = wm.scorecard_for_range("HEAD~1..HEAD")
    for _, label in wm._SCORECARD_LABELS + wm._SCORECARD_ADDENDA_LABELS:
        assert f"**{label}:**" in out, label


@pytest.mark.live_repo
def test_live_history_and_merge_surfaces_actually_resolve():
    """Both new surfaces are read from committed state in THIS repo -- so the two rows are
    computed here, not merely computable in principle."""
    counts = wm.fleet_check_counts(wm.read_fleet_history(wm._REPO_ROOT / "ecosystem"))
    assert counts is not None and counts["repos"] >= 1
    assert isinstance(wm.lane_merge_durations("HEAD~5..HEAD"), list)
