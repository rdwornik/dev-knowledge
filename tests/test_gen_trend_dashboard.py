"""Tests for the HY-4 additions to scripts/gen_trend_dashboard.py -- the TRENDS burn-down
panel (done vs remaining per north-star arc, over time) and the quota panel folded in by
architect ruling CUT-5.

RED-first (ADR-108 section B): every assertion here was written and run against the
pre-lane module, where `arc_counts`, `collect_task_frontmatter`, `build_arc_burndowns`,
`render_burndown_panel`, `QuotaRow`, `collect_quota_rows` and `render_quota_panel` did not
exist, before any of them were added.

WHY A SEPARATE FILE, RATHER THAN APPENDING TO `test_trend_dashboard.py` -- the lane's
write-scope is frozen to `scripts/gen_trend_dashboard.py` and THIS file; the existing test
file is out of footprint and untouched. Its own tests still run against the changed module
(same `tests/` directory) and their assertions therefore double as a regression net: the
new panels have to prove they do not change a byte of the OLD render path when a caller
does not ask for them.

THE TWO CONTRACT DISCIPLINES this file exists to pin:

  1. THE ARC SET IS READ, NEVER RESTATED. `build_arc_burndowns` must cover exactly the arcs
     declared in `scripts/gen_north_star.py::ARCS` -- so a new arc, or a retired one, shows
     up here without editing this module (done-contract item 1).
  2. THE QUOTA PANEL NAMES ITS OWN LIMIT. No store in this repo can compute a numeric
     credit balance for any provider (verified against `ecosystem/provider-registry.yaml`
     and its schema, and against the 2026-08-31 quota-visibility audit this lane's packet
     cites) -- so `collect_quota_rows` derives PROVIDER IDENTITY live and renders CREDITS as
     a named absence, and the panel states the `[#615]` model-attribution limit in its own
     text rather than rendering a column that looks whole and is not (done-contract items
     3-4).
"""
from __future__ import annotations

import importlib.util
import re
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gtd = _load("gen_trend_dashboard")


def _pts(*vals, start=date(2026, 8, 1)):
    return [(start + timedelta(days=7 * i), float(v)) for i, v in enumerate(vals)]


# --- arc_counts: the pure split, testable without git ------------------------

def test_arc_counts_splits_done_and_remaining_by_theme():
    fm = {
        "tasks/1.md": {"theme": "[E7] Tooling & evaluation", "status": "closed"},
        "tasks/2.md": {"theme": "[E7] Tooling & evaluation", "status": "open"},
        "tasks/3.md": {"theme": "[E7] Tooling & evaluation", "status": "open"},
        "tasks/4.md": {"theme": "[E2] Enforced governance", "status": "open"},
    }
    assert gtd.arc_counts(fm, ("[E7] Tooling & evaluation",)) == (1, 2)


def test_arc_counts_ignores_rows_outside_the_theme_selector():
    fm = {"tasks/1.md": {"theme": "some other theme", "status": "open"}}
    assert gtd.arc_counts(fm, ("[E7] Tooling & evaluation",)) == (0, 0)


def test_arc_counts_does_not_fold_deferred_retired_superseded_into_either_band():
    """THE FIVE-VALUE ENUM, applied here too (C6, 2026-08-19). A row that is neither open
    nor closed belongs to neither band -- folding it into either would misstate progress
    the same way folding `retired` into `closed` misstates the ledger."""
    fm = {f"tasks/{i}.md": {"theme": "t", "status": s}
          for i, s in enumerate(["deferred", "retired", "superseded"])}
    assert gtd.arc_counts(fm, ("t",)) == (0, 0)


def test_arc_counts_handles_a_row_missing_a_theme_field():
    fm = {"tasks/1.md": {"status": "open"}}
    assert gtd.arc_counts(fm, ("t",)) == (0, 0)


def test_arc_counts_supports_an_arc_with_multiple_themes():
    """The DEPLOYMENT arc is declared with two themes; a row matching either counts."""
    fm = {
        "tasks/1.md": {"theme": "[E6] Cross-repo universalization", "status": "closed"},
        "tasks/2.md": {"theme": "[E9] Fleet Desired-State System (North Star)",
                       "status": "open"},
    }
    themes = ("[E6] Cross-repo universalization",
             "[E9] Fleet Desired-State System (North Star)")
    assert gtd.arc_counts(fm, themes) == (1, 1)


# --- collect_task_frontmatter: the git-backed collector -----------------------

def test_collect_task_frontmatter_pairs_status_and_theme_per_file():
    fm = gtd.collect_task_frontmatter("HEAD")
    assert fm, "expected at least one tasks/*.md row at HEAD"
    assert any("status" in row and "theme" in row for row in fm.values())


def test_collect_task_frontmatter_excludes_archived_rows():
    """`tasks/archive/*.md` holds relocated records of rows already born (terra third
    pass, N2's reasoning, applied here): counting them would double-count a member the
    live row set already carries."""
    fm = gtd.collect_task_frontmatter("HEAD")
    assert not any(p.startswith("tasks/archive/") for p in fm)


def test_collect_task_frontmatter_strips_the_yaml_quoting():
    """Theme values are double-quoted YAML strings on disk (`theme: "[E7] ..."`); the
    collector must hand back the bare value so it compares equal to `ARCS[i]["themes"]`."""
    fm = gtd.collect_task_frontmatter("HEAD")
    themes = {row["theme"] for row in fm.values() if "theme" in row}
    assert themes, "no theme values found at HEAD"
    assert all(not t.startswith('"') and not t.endswith('"') for t in themes)


def test_collect_task_frontmatter_returns_none_on_a_failed_git_call():
    """Missing versus empty (terra second pass, N1's contract, applied here): a REVISION
    that does not exist must not be indistinguishable from one with no matching rows."""
    assert gtd.collect_task_frontmatter("not-a-real-revision-token") is None


# --- build_arc_burndowns: the arc set is READ, never restated -----------------

def test_build_arc_burndowns_covers_every_declared_arc():
    """Done-contract item 1: a new arc, or a retired one, must appear here without
    editing this module -- so the set is compared against the live import, not a copy."""
    built = {ab.key for ab in gtd.build_arc_burndowns(weeks=4)}
    declared = {a["key"] for a in gtd._north_star.ARCS}
    assert built == declared
    assert built, "the live arc set must not be empty"


def test_build_arc_burndowns_states_are_all_legal_and_carry_a_basis():
    for ab in gtd.build_arc_burndowns(weeks=4):
        assert ab.state in {"ok", "insufficient", "absent"}, ab.key
        assert ab.basis.strip(), f"{ab.key} has no basis"


def test_build_arc_burndowns_names_its_theme_selector_in_the_basis():
    """C6's requirement, applied to this panel too: the predicate must be stated, not
    merely computed, or a reader cannot tell which selector produced the count."""
    for ab in gtd.build_arc_burndowns(weeks=4):
        if ab.state == "absent":
            continue
        assert any(t in ab.basis for t in ab.themes), (
            f"{ab.key} basis does not name its own theme selector")


def test_build_arc_burndowns_bounds_every_arc_to_the_declared_window():
    weeks = 4
    start = gtd.sample_dates(date.today(), weeks)[0]
    for ab in gtd.build_arc_burndowns(weeks=weeks):
        for d, _ in ab.done + ab.remaining:
            assert d >= start, f"{ab.key} plotted {d}, outside the {weeks}w window"


def test_build_arc_burndowns_done_and_remaining_share_the_same_sample_dates():
    """The two lines are drawn on one shared x-axis; a caller that draws them from
    mismatched date lists would silently misalign the polylines."""
    for ab in gtd.build_arc_burndowns(weeks=4):
        assert [d for d, _ in ab.done] == [d for d, _ in ab.remaining]


# --- render_burndown_panel: absence and insufficiency draw no chart -----------

def test_render_burndown_panel_absent_draws_no_chart():
    ab = gtd.ArcBurndown(key="k", name="ARC K", themes=("t",), done=[], remaining=[],
                         basis="NO STORE", state="absent")
    html = gtd.render_burndown_panel(ab)
    assert "absent" in html
    assert "<polyline" not in html


def test_render_burndown_panel_insufficient_declines_a_direction():
    ab = gtd.ArcBurndown(key="k", name="ARC K", themes=("t",), done=_pts(1, 2),
                         remaining=_pts(9, 8), basis="2 samples", state="insufficient")
    html = gtd.render_burndown_panel(ab)
    assert "insufficient" in html
    assert "improving" not in html and "worsening" not in html


def test_render_burndown_panel_ok_draws_both_lines_and_a_direction_glyph():
    ab = gtd.ArcBurndown(key="k", name="ARC K", themes=("t",),
                         done=_pts(2, 5, 9), remaining=_pts(20, 12, 4),
                         basis="status split", state="ok")
    html = gtd.render_burndown_panel(ab)
    assert html.count("<polyline") == 2, "expected one line for done and one for remaining"
    assert "<polygon" in html, "no drawn direction glyph"
    assert "improving" in html, "falling remaining is improving progress toward done-when"


def test_render_burndown_panel_falling_remaining_is_improving_even_if_done_is_flat():
    """The verdict tracks REMAINING, because an arc's done-when is reached when remaining
    hits zero -- a flat `done` line (nothing newly closed) must not mask real burn-down
    if remaining is still falling (e.g. rows leaving the theme, or being retired)."""
    ab = gtd.ArcBurndown(key="k", name="ARC K", themes=("t",),
                         done=_pts(5, 5, 5), remaining=_pts(20, 10, 2),
                         basis="b", state="ok")
    html = gtd.render_burndown_panel(ab)
    assert "improving" in html


def test_render_burndown_panel_names_its_arc_and_predicate():
    ab = gtd.ArcBurndown(key="k", name="THE METRIC ARC", themes=("[E7] Tooling",),
                         done=_pts(1, 2, 3), remaining=_pts(9, 8, 7),
                         basis="the stated basis text", state="ok")
    html = gtd.render_burndown_panel(ab)
    assert "THE METRIC ARC" in html
    assert "the stated basis text" in html


# --- QuotaRow / collect_quota_rows: identity derived, credits named absent ----

def test_collect_quota_rows_reads_provider_identity_from_the_live_registry():
    """Provider identity is DERIVED (done-contract item 4): a provider added to or removed
    from ecosystem/provider-registry.yaml must appear or vanish here without editing this
    module."""
    import yaml
    registry = yaml.safe_load(
        (gtd._REPO_ROOT / "ecosystem" / "provider-registry.yaml").read_text(
            encoding="utf-8"))
    declared = set(registry["providers"])
    rows = gtd.collect_quota_rows()
    assert {r.provider for r in rows} == declared


def test_collect_quota_rows_never_states_a_numeric_credits_value():
    """THE CENTRAL DISCIPLINE (CUT-5): no store in this repo can compute a credit balance,
    so every row's credits_state is an absence, never a number that looks whole."""
    rows = gtd.collect_quota_rows()
    assert rows, "expected at least one provider row"
    for r in rows:
        assert r.credits_state == "absent"
        assert r.credits_basis.strip()
        assert not re.search(r"\d", r.credits_basis) or "615" in r.credits_basis or (
            "2026" in r.credits_basis), (
            f"{r.provider} credits_basis contains an unexplained digit: {r.credits_basis!r}")


def test_collect_quota_rows_carries_display_name_and_cli():
    rows = gtd.collect_quota_rows()
    anthropic = next(r for r in rows if r.provider == "anthropic")
    assert anthropic.display_name == "Anthropic"
    assert anthropic.cli == "claude"


# --- render_quota_panel: no table, no fabricated column, the limit is stated -

def test_render_quota_panel_names_every_provider():
    rows = gtd.collect_quota_rows()
    html = gtd.render_quota_panel(rows)
    for r in rows:
        assert r.display_name in html, f"{r.provider} vanished from the quota panel"


def test_render_quota_panel_never_renders_a_table():
    """ACCEPTANCE 2 (test_trend_dashboard.py) forbids the predecessor's shape anywhere on
    this page; the quota panel is a second section of the same page and inherits the rule."""
    rows = gtd.collect_quota_rows()
    html = gtd.render_quota_panel(rows)
    assert not re.search(r"<(table|thead|tbody|tr|td|th)\b", html, re.I)
    assert not re.search(r"(?m)^\s*\|.*\|\s*$", html)


def test_render_quota_panel_states_its_own_model_attribution_limit():
    """Done-contract item 3, verbatim: the panel says so in its own text rather than
    rendering a column that looks whole and is not."""
    html = gtd.render_quota_panel(gtd.collect_quota_rows())
    assert "[#615]" in html
    assert "MODEL" in html.upper()


def test_render_quota_panel_of_no_rows_is_a_named_absence_not_a_crash():
    html = gtd.render_quota_panel([])
    assert "absent" in html
    assert "<polyline" not in html


# --- render_page: additive only, backward-compatible with the old call shape -

def test_render_page_without_new_args_is_unchanged_from_the_pre_lane_shape():
    """The two existing test-file call sites (`render_page(series, meta=meta)`) must keep
    producing exactly what they always produced -- no burndown or quota SECTION leaks in
    when the caller does not ask for one. (The static CSS block, always present, is
    allowed to carry `.quota-row`/`.burndown` style rules -- those are not a rendered
    section and are not what this guard is checking.)"""
    meta = {"generated_at": "2026-08-29T00:00:00Z", "sha": "deadbeef", "window": "12w"}
    page = gtd.render_page(gtd.demo_series(), meta)
    assert "north-star arcs" not in page
    assert "provider credits" not in page


def test_render_page_includes_arc_burndowns_when_given():
    meta = {"generated_at": "x", "sha": "y", "window": "4w"}
    arcs = [gtd.ArcBurndown(key="k", name="THE METRIC", themes=("t",),
                            done=_pts(1, 2, 3), remaining=_pts(9, 6, 3),
                            basis="b", state="ok")]
    page = gtd.render_page(gtd.demo_series(), meta, arc_burndowns=arcs)
    assert "THE METRIC" in page


def test_render_page_includes_quota_rows_when_given():
    meta = {"generated_at": "x", "sha": "y", "window": "4w"}
    rows = [gtd.QuotaRow(provider="anthropic", display_name="Anthropic", cli="claude",
                         credits_state="absent", credits_basis="no store")]
    page = gtd.render_page(gtd.demo_series(), meta, quota_rows=rows)
    assert "Anthropic" in page
    assert "[#615]" in page


def test_render_page_with_new_sections_stays_pure_ascii():
    meta = {"generated_at": "x", "sha": "y", "window": "4w"}
    arcs = gtd.build_arc_burndowns(weeks=4)
    rows = gtd.collect_quota_rows()
    page = gtd.render_page(gtd.demo_series(), meta, arc_burndowns=arcs, quota_rows=rows)
    page.encode("ascii")


def test_render_page_with_new_sections_still_carries_no_table():
    meta = {"generated_at": "x", "sha": "y", "window": "4w"}
    arcs = gtd.build_arc_burndowns(weeks=4)
    rows = gtd.collect_quota_rows()
    page = gtd.render_page(gtd.demo_series(), meta, arc_burndowns=arcs, quota_rows=rows)
    assert not re.search(r"<(table|thead|tbody|tr|td|th)\b", page, re.I)
    assert not re.search(r"(?m)^\s*\|.*\|\s*$", page)


# --- build_series is UNCHANGED: the new panels are a second section, not a new key -

def test_build_series_key_set_does_not_gain_the_new_panels():
    """`test_trend_dashboard.py::test_build_series_emits_every_contracted_series` asserts
    an EXACT key set. Folding the burn-down or quota data into `build_series` would break
    that frozen assertion in a file this lane may not edit -- so both new panels are
    assembled and rendered through their own functions instead."""
    keys = {s.key for s in gtd.build_series(weeks=4)}
    assert "quota" not in keys
    assert not any(k.startswith("arc_") for k in keys)


# --- the real pipeline, end to end --------------------------------------------

def test_main_renders_both_new_panels_through_the_real_pipeline(tmp_path):
    target = tmp_path / "trends.html"
    assert gtd.main(["--write", "--weeks", "4", "--out", str(target)]) == 0
    page = target.read_text(encoding="ascii")
    for a in gtd._north_star.ARCS:
        assert a["name"] in page, f"arc {a['key']} missing from the real page"
    assert "[#615]" in page
    assert not re.search(r"(?m)^\s*\|.*\|\s*$", page)
    assert not re.search(r"<(table|thead|tbody|tr|td|th)\b", page, re.I)


def test_main_with_new_panels_is_still_idempotent_across_two_real_runs(tmp_path):
    a, b = tmp_path / "a.html", tmp_path / "b.html"
    gtd.main(["--write", "--weeks", "4", "--out", str(a)])
    gtd.main(["--write", "--weeks", "4", "--out", str(b)])
    assert a.read_bytes() == b.read_bytes()
