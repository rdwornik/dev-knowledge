"""Tests for scripts/gen_trend_dashboard.py -- DB-1, the dashboard successor.

RED-FIRST. Every assertion here was written and run BEFORE the generator existed, and the
run is recorded in the lane packet. The three operator acceptance tests are pinned as
literal tests rather than as prose, because the thing being replaced
(`ecosystem/conformance.html` + `ecosystem/conformance.md`) failed on exactly the axes the
acceptance names:

  1. DIRECTION visible in one glance  -> `test_every_rendered_panel_declares_a_direction`
     and the `direction()` unit tests. A panel that renders a series and declines to say
     which way it is going is a value table with extra steps.
  2. Zero colored-table markdown      -> `test_output_carries_no_markdown_table`.
  3. Regenerable, ONE command, idempotent -> `test_render_page_is_idempotent`.

Two further properties are pinned because they are this repo's recorded hazards, not
because the contract asked:

  * ASCII-ONLY OUTPUT (`test_output_is_pure_ascii`). `gen_dashboard`-class generators here
    emit silent mojibake and exit 0 without `PYTHONUTF8=1`. The successor sidesteps the
    hazard structurally rather than documenting it: direction glyphs are DRAWN as SVG
    polygons, never typed as arrow characters, so there is no non-ASCII byte to launder.
  * ABSENCE IS NOT ZERO (`test_absent_series_*`, `test_insufficient_series_*`). A series
    with no store renders as a named absence with a reason. Rendering it as a flat zero
    line is the failure mode the contract calls "a chart of invented history".
"""
from __future__ import annotations

import importlib.util
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gtd = _load("gen_trend_dashboard")


def _pts(*vals, start=date(2026, 8, 1)):
    """(date, value) points one week apart, so a series is trivially readable."""
    from datetime import timedelta
    return [(start + timedelta(days=7 * i), v) for i, v in enumerate(vals)]


# --- direction: the headline the whole surface exists to carry ---------------

def test_direction_falling_series_improves_when_lower_is_better():
    verdict, delta = gtd.direction(_pts(100, 80, 60), better="down")
    assert verdict == "improving"
    assert delta == -40


def test_direction_falling_series_worsens_when_higher_is_better():
    verdict, delta = gtd.direction(_pts(100, 80, 60), better="up")
    assert verdict == "worsening"
    assert delta == -40


def test_direction_rising_series_improves_when_higher_is_better():
    verdict, _ = gtd.direction(_pts(1, 5, 9), better="up")
    assert verdict == "improving"


def test_direction_flat_series_is_flat_under_either_polarity():
    assert gtd.direction(_pts(7, 7, 7), better="up")[0] == "flat"
    assert gtd.direction(_pts(7, 7, 7), better="down")[0] == "flat"


def test_direction_reads_the_window_not_the_last_step():
    """A series that fell 100->10 and ticked 10->11 at the end is still improving.

    Direction is the property of the WINDOW. Keying off the final step would let one
    noisy sample flip the headline, which is how a trend surface starts lying.
    """
    verdict, _ = gtd.direction(_pts(100, 50, 10, 11), better="down")
    assert verdict == "improving"


def test_direction_of_a_single_point_is_unknown_never_flat():
    """One sample is not a trend. 'flat' would be a claim the data cannot support."""
    assert gtd.direction(_pts(5), better="up")[0] == "unknown"


def test_direction_of_an_empty_series_is_unknown():
    assert gtd.direction([], better="up")[0] == "unknown"


# --- the store parsers -------------------------------------------------------

_GIT_GREP = (
    "status: closed\n"
    "status: open\n"
    "status: open\n"
    "status: deferred\n"
    "status: retired\n"
    "status: superseded\n"
)


def test_parse_band_counts_covers_the_five_value_enum():
    """C6 (2026-08-19) measured a FIVE-value enum and warned that a binary chart strands
    deferred/retired/superseded -- 9.6% of the tree at the time. All five are counted."""
    bands = gtd.parse_band_counts(_GIT_GREP)
    assert bands == {"open": 2, "closed": 1, "deferred": 1, "retired": 1, "superseded": 1}


def test_parse_band_counts_does_not_fold_retired_into_closed():
    """Folding `retired` into `closed` lets the ledger go net-negative by relabelling --
    the exact gaming C6 flagged. They stay separate bands."""
    bands = gtd.parse_band_counts(_GIT_GREP)
    assert bands["closed"] == 1
    assert bands["retired"] == 1


def test_parse_band_counts_ignores_unknown_status_values():
    bands = gtd.parse_band_counts("status: open\nstatus: banana\n")
    assert bands["open"] == 1
    assert "banana" not in bands


def test_parse_doc_rot_count_reads_a_history_snapshot():
    snap = (
        "### 2026-07-31\n\n"
        "| Check | Status | Evidence |\n"
        "|---|---|---|\n"
        "| vision_md | pass | fine |\n"
        "| doc_rot | warn | bloat A |\n"
        "| doc_rot | warn | bloat B |\n"
    )
    assert gtd.parse_doc_rot_count(snap) == 2


def test_parse_doc_rot_count_of_a_snapshot_that_ran_it_clean_is_zero():
    """A snapshot where the check RAN and passed is a real zero, and stays a data point."""
    snap = ("| Check | Status | Evidence |\n|---|---|---|\n"
            "| vision_md | pass | fine |\n| doc_rot | pass | no rot |\n")
    assert gtd.parse_doc_rot_count(snap) == 0


def test_parse_doc_rot_count_is_none_when_the_check_did_not_exist_yet():
    """THE REGRESSION THIS PINS, found in the generator's own first real output.

    `doc_rot` is registered check #24 and appears in no snapshot before 2026-07-31. These
    snapshots record passing checks too, so a check that is ABSENT from one never ran
    there. Scoring those as clean zeros produced a fifteen-sample flat line and a
    confident "WORSENING +2" headline that described nothing but the check being added --
    the invented history this surface exists to refuse.
    """
    snap = "| Check | Status | Evidence |\n|---|---|---|\n| vision_md | pass | fine |\n"
    assert gtd.parse_doc_rot_count(snap) is None


def test_collect_doc_rot_drops_pre_existence_snapshots_rather_than_zeroing_them():
    """The collector must not turn the None above back into a point."""
    pts = gtd.collect_doc_rot()
    assert all(isinstance(v, float) for _, v in pts)
    # Live-repo guard: no snapshot before doc_rot existed may appear in the series.
    assert all(d >= date(2026, 7, 1) for d, _ in pts), pts


def test_collect_doc_rot_honours_the_window_bound():
    """A panel outside the declared window makes directions incomparable (terra H5)."""
    assert gtd.collect_doc_rot(since=date(2099, 1, 1)) == []


def test_latest_snapshot_takes_the_days_final_run():
    """A dated history file can hold SEVERAL audit runs -- 2026-05-16.md holds twelve.

    Counting findings across all of them produces an aggregate no single audit run ever
    recorded (terra pre-merge, H6).
    """
    text = ("### 2026-05-16 - 08:00\n| doc_rot | warn | early |\n"
            "### 2026-05-16 - 20:00\n| doc_rot | warn | late A |\n"
            "| doc_rot | warn | late B |\n")
    assert gtd.parse_doc_rot_count(gtd.latest_snapshot(text)) == 2, (
        "findings were summed across runs instead of taking the day's final run")


def test_latest_snapshot_passes_through_an_unmarked_file():
    text = "| Check | Status |\n| doc_rot | warn | only |\n"
    assert gtd.latest_snapshot(text) == text


def test_live_history_files_with_multiple_runs_are_not_summed():
    """Live-repo guard for the same defect: every doc-rot point must be reproducible from
    ONE snapshot of that day, never from the file's total."""
    base = Path(__file__).resolve().parent.parent / "ecosystem/.dev-knowledge/history"
    for f in base.glob("????-??-??.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        if text.count("\n### ") + text.startswith("### ") < 2:
            continue
        whole = len(re.findall(r"(?m)^\|\s*doc_rot\s*\|\s*(?:warn|fail)\s*\|", text))
        last = gtd.parse_doc_rot_count(gtd.latest_snapshot(text))
        assert last is None or last <= whole


# --- velocity: closures fund births -----------------------------------------

def test_velocity_pairs_closures_against_births():
    """The operator's standing frame is 'closures fund births', so the pair is the series.

    Closures are derived as the DELTA of the banked band, which is exact here because no
    task file has ever been deleted (C6: `git log --diff-filter=D -- tasks/*.md` = 0), so
    a row can only leave `open` by changing its own frontmatter.
    """
    banked = _pts(10, 14, 20)
    births = {banked[1][0]: 3, banked[2][0]: 1}
    windows = gtd.velocity(banked, births)
    assert [w["closures"] for w in windows] == [4, 6]
    assert [w["births"] for w in windows] == [3, 1]
    assert [w["net"] for w in windows] == [1, 5]


def test_archived_records_are_not_counted_as_births():
    """THE REGRESSION THIS PINS (terra third pass).

    A birth is a row coming into EXISTENCE. `tasks/archive/` holds relocated records of
    rows that were already born, so an archival counted as a birth double-counts it.
    Measured on the live tree: the 2026-08-22..29 window counted 57 additions, 21 of them
    archive files -- a 58% overstatement on the one metric whose headline had already
    flipped once in this lane.
    """
    assert gtd.is_task_row_path("tasks/601-a-real-row.md")
    assert not gtd.is_task_row_path("tasks/archive/112.md")
    assert not gtd.is_task_row_path("tasks/archive/README.md")
    assert not gtd.is_task_row_path("tasks/manifest.json")


def test_live_archive_additions_are_excluded_from_the_birth_count():
    """Live-repo guard: `tasks/archive/` exists and is populated, so the filter is load-
    bearing rather than theoretical."""
    archive = Path(__file__).resolve().parent.parent / "tasks" / "archive"
    if not archive.is_dir():
        return
    assert any(archive.glob("*.md")), "fixture assumption changed: archive is empty"
    assert not any(gtd.is_task_row_path(f"tasks/archive/{f.name}")
                   for f in archive.glob("*.md"))


def test_sample_dates_spans_the_full_requested_window():
    """N SAMPLES ARE N-1 INTERVALS (terra fourth pass).

    Returning exactly `weeks` dates made `--weeks 12` advertise twelve weeks while reading
    77 days, and `--weeks 1` span no interval at all -- a window label that did not
    describe the data beneath it.
    """
    end = date(2026, 8, 29)
    dates = gtd.sample_dates(end, 12)
    assert dates[-1] == end
    assert (end - dates[0]).days == 84, "a 12-week window must cover 12 weeks"
    assert (end - gtd.sample_dates(end, 1)[0]).days == 7


def test_sampler_reads_the_first_parent_mainline():
    """terra fifth pass. Every change lands here by `--no-ff` merge, so the first-parent
    spine IS the history of main; without the flag `rev-list -1 --before` can return an
    unmerged lane commit and the page reports a lane's private state as the repo's."""
    rev = gtd._rev_at(date(2026, 8, 22))
    assert rev, "the sampler resolved no revision for a date inside live history"
    spine = gtd._git("rev-list", "--first-parent", "HEAD").split()
    assert rev in spine, "the sampler selected a commit off main's first-parent spine"


def test_git_env_is_scrubbed_so_an_inherited_git_dir_cannot_redirect_the_read():
    """terra fourth pass. An inherited GIT_DIR overrides both cwd and -C, so every
    collector would read ANOTHER repo while the page labelled it as this one."""
    scrubbed = gtd._gitenv.scrubbed_git_env()
    assert "GIT_DIR" not in scrubbed
    assert "GIT_WORK_TREE" not in scrubbed


def test_sample_dates_refuses_a_non_positive_window():
    """A zero window yields no dates, and every caller indexes dates[0] -- so the CLI
    accepted an input that crashed with IndexError instead of refusing (terra third
    pass)."""
    for bad in (0, -1):
        with pytest.raises(ValueError):
            gtd.sample_dates(date(2026, 8, 29), bad)
    with pytest.raises(SystemExit):
        gtd.main(["--weeks", "0"])


def test_velocity_matches_births_by_date_not_by_index():
    """THE REGRESSION THIS PINS (terra pre-merge, H1).

    `collect_bands` drops sample dates from before `tasks/` existed, so its list is
    SHORTER than the sample vector. Pairing the two positionally shifted every birth
    count by the number of dropped samples and silently overstated net velocity. Here the
    births dict is keyed by real dates and carries an extra EARLIER key that positional
    indexing would have consumed first.
    """
    banked = _pts(10, 14, 20)
    stale = date(2026, 1, 1)
    windows = gtd.velocity(banked, {stale: 99, banked[1][0]: 3, banked[2][0]: 1})
    assert [w["births"] for w in windows] == [3, 1], "births were matched positionally"


def test_velocity_skips_a_window_whose_births_cannot_be_resolved():
    """An unmeasurable window is omitted, never defaulted to 0 births -- 'could not
    measure' and 'nothing was filed' are different facts and only the second is a zero."""
    banked = _pts(10, 14, 20)
    windows = gtd.velocity(banked, {banked[2][0]: 1})
    assert [w["date"] for w in windows] == [banked[2][0]]


def test_velocity_of_a_single_banked_sample_is_empty():
    assert gtd.velocity(_pts(10), {}) == []


# --- absence: the contract's central discipline ------------------------------

def test_absent_series_renders_its_reason_and_no_chart():
    s = gtd.Series(
        key="suite_time", label="suite wall-time", predicate="n/a",
        points=[], basis="NO STORE -- nothing records suite wall-time",
        better="down", state="absent")
    html = gtd.render_panel(s)
    assert "NO STORE" in html
    assert "absent" in html
    assert "<polyline" not in html and "<path" not in html


def test_absent_series_never_renders_a_zero():
    s = gtd.Series(key="k", label="l", predicate="p", points=[],
                   basis="NO STORE", better="down", state="absent")
    html = gtd.render_panel(s)
    assert not re.search(r">\s*0\s*<", html), "an absent series rendered a zero value"


def test_insufficient_series_declines_to_claim_a_direction():
    """Two points is a line, not a trend. The panel says so instead of drawing an arrow."""
    s = gtd.Series(key="k", label="l", predicate="p", points=_pts(5, 4),
                   basis="2 samples", better="down", state="insufficient")
    html = gtd.render_panel(s)
    assert "insufficient" in html
    assert "improving" not in html and "worsening" not in html


def test_classify_state_marks_a_short_series_insufficient():
    assert gtd.classify_state(_pts(1, 2)) == "insufficient"
    assert gtd.classify_state(_pts(1, 2, 3)) == "ok"
    assert gtd.classify_state([]) == "absent"


# --- the telemetry store: four outcomes, and the right quantity --------------

def _seed_store(path, rows):
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT,"
                " event_type TEXT, name TEXT, outcome TEXT, duration_ms INTEGER,"
                " context_json TEXT DEFAULT '{}', run_id TEXT DEFAULT '')")
    con.executemany("INSERT INTO events (ts, event_type, name, outcome, duration_ms,"
                    " run_id) VALUES (?,?,?,?,?,?)", rows)
    con.commit()
    con.close()


def test_commit_gate_sums_hooks_within_a_run_before_averaging(tmp_path):
    """THE QUANTITY (terra pre-merge, H3). Gate wall-time is what ONE invocation costs.

    Two runs on one day: 100+200=300 and 400+500=900, so the day is 600. Averaging the
    four individual hooks instead gives 300 -- a different number that moves whenever the
    NUMBER of hooks changes rather than when the gate gets slower.
    """
    db = tmp_path / "T.db"
    _seed_store(db, [
        ("2026-08-01T00:00:00", "hook_run", "a", "pass", 100, "r1"),
        ("2026-08-01T00:00:01", "hook_run", "b", "pass", 200, "r1"),
        ("2026-08-01T00:00:02", "hook_run", "a", "pass", 400, "r2"),
        ("2026-08-01T00:00:03", "hook_run", "b", "pass", 500, "r2"),
    ])
    points, reason = gtd.collect_commit_gate(db)
    assert reason is None
    assert points == [(date(2026, 8, 1), 600.0)]


def test_commit_gate_groups_sibling_hooks_separately_as_the_store_requires(tmp_path):
    """WHAT A run_id GROUP ACTUALLY IS (terra third pass).

    `telemetry_emit.current_run_id` exports the id to a process's DESCENDANTS, not its
    SIBLINGS, and pre-commit spawns each hook as its own child -- so one commit normally
    yields one run_id PER HOOK. The panel is labelled "per runner invocation" for exactly
    that reason. Two sibling hooks of 100 and 200 average to 150; reporting 300 would be
    claiming a whole-commit figure the store cannot support.
    """
    db = tmp_path / "T.db"
    _seed_store(db, [
        ("2026-08-01T00:00:00", "hook_run", "ruff", "pass", 100, "r1"),
        ("2026-08-01T00:00:01", "hook_run", "audit-health", "pass", 200, "r2"),
    ])
    assert gtd.collect_commit_gate(db)[0] == [(date(2026, 8, 1), 150.0)]


def test_commit_gate_panel_does_not_claim_to_measure_a_commit():
    """The label and predicate must not over-claim past the store's own honest limit."""
    gate = next(s for s in gtd.build_series(weeks=4) if s.key == "commit_gate")
    assert "runner invocation" in gate.label
    assert "commit-gate wall-time" != gate.label


def test_commit_gate_excludes_check_run_because_it_nests_inside_a_hook(tmp_path):
    """THE DOUBLE-COUNT (terra second pass, N2), pinned as a test.

    `check_run` is emitted per audit check from inside `scripts/audit.py`, and `audit.py`
    IS the `audit-health` hook, which emits its own enclosing `hook_run`. Summing both
    charges the same milliseconds twice. Here the hook took 100ms and contains two checks
    of 40ms each; the answer is 100, and 180 is the double-count.
    """
    db = tmp_path / "T.db"
    _seed_store(db, [
        ("2026-08-01T00:00:00", "hook_run", "audit-health", "pass", 100, "r1"),
        ("2026-08-01T00:00:00", "check_run", "doc_rot", "pass", 40, "r1"),
        ("2026-08-01T00:00:00", "check_run", "vision_md", "pass", 40, "r1"),
    ])
    assert gtd.collect_commit_gate(db)[0] == [(date(2026, 8, 1), 100.0)]


def test_commit_gate_distinguishes_missing_store_from_empty_store(tmp_path):
    """FOUR OUTCOMES, NOT ONE (terra pre-merge, H4). Collapsing them made a present-but-
    unusable store render as the reassuring 'telemetry was never enabled'."""
    missing = gtd.collect_commit_gate(tmp_path / "nope.db")
    assert missing[0] == [] and "NO STORE" in missing[1]

    db = tmp_path / "empty.db"
    _seed_store(db, [])
    empty = gtd.collect_commit_gate(db)
    assert empty[0] == [] and "NO CORRELATED RUNS" in empty[1]
    assert "never enabled" not in empty[1], "an empty store claimed telemetry was off"


def test_missing_store_reports_the_observable_fact_not_a_history_claim():
    """terra second pass, N5. File absence proves no store is readable HERE -- not that
    telemetry was never enabled. A store can be deleted, relocated by
    DEV_KNOWLEDGE_TELEMETRY_DB, or belong to another checkout."""
    _, reason = gtd.collect_commit_gate(Path("no", "such", "store.db"))
    assert "not present in this checkout" in reason
    # The message must not make a claim about history at all -- not even to deny one,
    # since a crude substring guard cannot tell an assertion from its negation.
    assert "never enabled" not in reason
    assert "never ran" not in reason


def test_git_checked_separates_failure_from_empty_output():
    """terra second pass, N1. A collector that reads a FAILED git call as "" cannot tell
    'nothing was filed' from 'the command did not run', and renders both as a zero."""
    assert gtd._git_checked("rev-parse", "--verify", "definitely-not-a-ref") is None
    assert gtd._git_checked("rev-parse", "HEAD") is not None


def test_collect_funnel_walks_revisions_not_weekly_samples():
    """terra second pass, N4. The baseline is regenerated irregularly and two revisions
    can land inside one week, so a weekly sampler drops real measurements while the panel
    still claims 'per rev'. Walking the file's own log is what the label promises."""
    all_revs = gtd.collect_funnel()
    assert all_revs, "the committed funnel baseline has revisions to read"
    assert all(isinstance(v, float) for _, v in all_revs)
    assert [d for d, _ in all_revs] == sorted(d for d, _ in all_revs), "not oldest-first"
    assert gtd.collect_funnel(since=date(2099, 1, 1)) == [], "window bound not applied"


def test_commit_gate_reports_an_unreadable_store_as_a_failure_not_an_absence(tmp_path):
    db = tmp_path / "corrupt.db"
    db.write_bytes(b"this is not a sqlite database, not even close")
    points, reason = gtd.collect_commit_gate(db)
    assert points == []
    assert "UNREADABLE" in reason
    assert "never enabled" not in reason, "a corrupt store was reported as telemetry-off"


def test_commit_gate_ignores_uncorrelated_rows(tmp_path):
    """Rows predating the [#565] run_id column carry an empty id. Averaging them together
    would present many unrelated events as one run."""
    db = tmp_path / "T.db"
    _seed_store(db, [("2026-08-01T00:00:00", "hook_run", "a", "pass", 100, "")])
    assert gtd.collect_commit_gate(db)[0] == []


# --- the pipeline, not just the renderer (terra pre-merge, H8) ---------------

_REQUIRED_KEYS = {"open_rows", "banked_ledger", "velocity", "paste_bytes",
                  "funnel_orphans", "doc_rot", "commit_gate", "suite_time",
                  "model_quality"}


def test_build_series_emits_every_contracted_series():
    """The contract names seven series plus two from the operator addendum. An assembly
    that silently dropped one would still pass every renderer test."""
    built = gtd.build_series(weeks=6)
    assert {s.key for s in built} == _REQUIRED_KEYS


def test_build_series_states_are_all_legal_and_absences_carry_a_reason():
    for s in gtd.build_series(weeks=6):
        assert s.state in {"ok", "insufficient", "absent"}, s.key
        assert s.basis.strip(), f"{s.key} has no basis"
        if s.state == "absent":
            assert not s.points, f"{s.key} is absent but carries points"


def test_build_series_bounds_every_panel_to_the_declared_window():
    """H5 end to end: no panel may plot a point older than the window it advertises."""
    weeks = 4
    start = gtd.sample_dates(date.today(), weeks)[0]
    for s in gtd.build_series(weeks=weeks):
        for d, _ in s.points:
            assert d >= start, f"{s.key} plotted {d}, outside the {weeks}w window"


def test_main_renders_the_real_pipeline_end_to_end(tmp_path):
    """H8: the acceptance assertions above pin the RENDERER via demo_series(). This one
    drives the real collectors and asserts the output the operator actually opens."""
    target = tmp_path / "trends.html"
    assert gtd.main(["--write", "--weeks", "6", "--out", str(target)]) == 0
    page = target.read_text(encoding="ascii")
    assert "direction of travel" in page
    assert "per-model change quality" in page, "an absent series vanished from the page"
    assert "gen_trend_dashboard.py --write" in page, "the regenerate command is missing"
    assert not re.search(r"(?m)^\s*\|.*\|\s*$", page)


def test_main_is_idempotent_across_two_real_runs(tmp_path):
    """ACCEPTANCE 3, measured through main() rather than through a fixed meta dict.

    The wall-clock stamp made this false (terra pre-merge, H7): every regeneration
    differed by a few bytes, so the page could never satisfy the acceptance test it
    claimed. The stamp is now HEAD's own commit date -- derived from the input, not the
    clock.
    """
    a, b = tmp_path / "a.html", tmp_path / "b.html"
    gtd.main(["--write", "--weeks", "6", "--out", str(a)])
    gtd.main(["--write", "--weeks", "6", "--out", str(b)])
    assert a.read_bytes() == b.read_bytes()


# --- the three acceptance tests, as tests ------------------------------------

def _page():
    return gtd.render_page(gtd.demo_series(), meta={"generated_at": "2026-08-29T00:00:00Z",
                                                    "sha": "deadbeef", "window": "12w"})


def test_every_rendered_panel_declares_a_direction():
    """ACCEPTANCE 1. Every series in state `ok` carries a direction word AND a drawn glyph."""
    page = _page()
    for s in gtd.demo_series():
        if s.state != "ok":
            continue
        panel = gtd.render_panel(s)
        assert any(v in panel for v in ("improving", "worsening", "flat")), s.key
        assert "<polygon" in panel, f"{s.key} has no drawn direction glyph"
    assert page


def test_output_carries_no_table_of_any_kind():
    """ACCEPTANCE 2. The predecessor is a colour-coded markdown table. Rebuilding one --
    even inside HTML -- is rebuilding the thing being replaced.

    The HTML half was added after terra's second pass (N6) pointed out that the original
    assertion rejected only pipe syntax, so a `<table>` rebuild of the predecessor would
    have passed the very test written to forbid it.
    """
    page = _page()
    assert not re.search(r"(?m)^\s*\|.*\|\s*$", page), "output contains a markdown table row"
    assert not re.search(r"(?m)^\s*\|[-: |]+\|\s*$", page), "output contains a table rule"
    assert not re.search(r"<(table|thead|tbody|tr|td|th)\b", page, re.I), (
        "output contains an HTML table -- the predecessor rebuilt in another syntax")


def test_the_no_table_assertion_actually_rejects_a_table():
    """The guard above is only worth having if it discriminates, so prove it does."""
    assert re.search(r"<(table|thead|tbody|tr|td|th)\b",
                     "<table><tr><td>x</td></tr></table>", re.I)


def test_render_page_is_idempotent():
    """ACCEPTANCE 3. Same inputs, byte-identical output -- otherwise 'regenerate' produces
    a diff every run and the artifact can never be trusted or gated."""
    meta = {"generated_at": "2026-08-29T00:00:00Z", "sha": "deadbeef", "window": "12w"}
    assert gtd.render_page(gtd.demo_series(), meta=meta) == gtd.render_page(
        gtd.demo_series(), meta=meta)


def test_output_is_pure_ascii():
    """The `gen_dashboard` mojibake hazard, closed structurally rather than documented."""
    _page().encode("ascii")


def test_page_names_every_absent_series_in_the_legend():
    """The contract: a series with no store is 'rendered as absent, NAMED IN THE LEGEND,
    not silently dropped'. Dropping it is how a gap becomes invisible."""
    page = _page()
    for s in gtd.demo_series():
        if s.state == "absent":
            assert s.label in page, f"absent series {s.key} vanished from the page"


def test_page_states_each_panel_predicate_literally():
    """C6's requirement: three live denominators already disagree, so a panel that does not
    name its predicate entrenches whichever one it happened to pick."""
    page = _page()
    for s in gtd.demo_series():
        if s.state != "absent":
            assert s.predicate in page, f"{s.key} renders without naming its predicate"


# --- honest-limit guards -----------------------------------------------------

def test_shallow_clone_refuses_a_git_derived_series():
    """C6 section 2.6 promoted this from a caveat to a page-wide rule, and reused
    `telemetry_emit.is_shallow_repository`. A truncated series is worse than none: it
    renders a plausible short line that reads as the whole history."""
    assert gtd.shallow_basis(True) is not None
    assert "shallow" in gtd.shallow_basis(True)
    assert gtd.shallow_basis(None) is not None, "'could not tell' is also unavailable"
    assert gtd.shallow_basis(False) is None


def test_write_to_an_out_of_tree_path_does_not_crash(tmp_path):
    """`--out` may point outside the repo (a scratch dir, a diff harness). `relative_to`
    RAISES rather than falling back when it does -- which crashed the first real
    idempotence measurement AFTER the file had already been written correctly."""
    target = tmp_path / "trends.html"
    assert gtd.main(["--write", "--weeks", "3", "--out", str(target)]) == 0
    assert target.read_bytes()


def test_sparkline_of_a_flat_series_does_not_divide_by_zero():
    pts = _pts(5, 5, 5)
    assert gtd.sparkline_points(pts, 100, 20)


def test_budget_line_sits_on_the_same_scale_as_the_polyline():
    """A budget panel exists to show HEADROOM, so the ceiling must be positioned by the
    same mapping as the series it judges. Scaling it separately puts the dashed line at an
    arbitrary height and silently misreports how close the value is to the ceiling.

    Here the ceiling (18000) is above every sample, so it must land at the TOP of the box
    (y == 0) and every sample must sit strictly below it.
    """
    pts = _pts(5964, 12000, 17196)
    panel = gtd.render_panel(gtd.Series(
        key="paste_bytes", label="paste", predicate="p", points=pts, basis="b",
        better="down", state="ok", unit="bytes", extra={"budget": 18000.0}))
    y = float(re.search(r'class="budget"[^>]*y1="([\d.]+)"', panel).group(1))
    assert y == pytest.approx(0.0), "ceiling above every sample must pin to the top"
    ys = [float(c.split(",")[1])
         for c in re.search(r'<polyline points="([^"]+)"', panel).group(1).split()]
    assert all(v > y for v in ys), "no sample may render at or above an unbreached ceiling"


def test_budget_line_is_crossed_when_the_series_breaches_it():
    """The other half: a breach must be visible AS a breach, not clamped out of sight."""
    pts = _pts(17000, 18500, 19000)
    panel = gtd.render_panel(gtd.Series(
        key="paste_bytes", label="paste", predicate="p", points=pts, basis="b",
        better="down", state="ok", unit="bytes", extra={"budget": 18000.0}))
    y = float(re.search(r'class="budget"[^>]*y1="([\d.]+)"', panel).group(1))
    ys = [float(c.split(",")[1])
         for c in re.search(r'<polyline points="([^"]+)"', panel).group(1).split()]
    assert min(ys) < y < max(ys), "a breaching series must cross its budget line"


def test_sparkline_maps_low_values_to_the_bottom_of_the_box():
    """y is inverted for SVG. A rising series must go UP on screen, which is the single
    easiest thing to get backwards and the one that would invert every headline."""
    pts = _pts(0, 10)
    coords = gtd.sparkline_points(pts, 100, 20)
    ys = [float(c.split(",")[1]) for c in coords.split()]
    assert ys[0] > ys[-1], "a rising series must render upward"
