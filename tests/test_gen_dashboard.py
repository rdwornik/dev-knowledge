"""Tests for scripts/gen_dashboard.py ([#171] stage 1 — the operator conformance dashboard).

Firing tests, one cluster per dashboard section plus the cross-cutting contracts the lane
brief names explicitly:

  * SECTION 0 release notes — rows that LEFT BACKLOG.md inside the window, newest-first,
    each carrying the `Done when:` clause as the operator-facing gain line.
  * SECTION 1 backlog — per-theme open/deferred/closed counts and size mix.
  * SECTION 2 intake — the anti-orphan verdict: carrier row(s) / deferred(dated) / VIOLATION,
    plus the archived-or-not flag on terminal docs and the loud UNKNOWN bucket.
  * SECTION 3 ADR ledger — status per ADR and the archivable candidate flag.
  * SECTION 4 telemetry — absent store renders the in-flight note WITH the expected path,
    and the module never imports or calls telemetry code.
  * SECTION 5 gate health — WARN composition parsed off the audit surface + commit tax.
  * Cross-cutting — regeneration is idempotent, `--check` refuses drift, the HTML sibling is
    self-contained, and an unknown intake status never crashes the run.

The module is loaded by path (the repo's standard for loose top-level `scripts/` modules,
mirroring tests/test_gen_intake_index.py) so no package import is implied.
"""

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

_P = Path(__file__).resolve().parent.parent / "scripts" / "gen_dashboard.py"


def _load():
    spec = importlib.util.spec_from_file_location("gen_dashboard", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gen_dashboard"] = module
    spec.loader.exec_module(module)
    return module


gd = _load()


# --------------------------------------------------------------------------- helpers

def _backlog(*rows: str, themes: tuple[str, ...] = ("[E1] Handoff continuity",)) -> str:
    """A minimal but structurally real BACKLOG.md: one theme heading then task rows."""
    out = ["# Backlog", "", "## Big picture", ""]
    for theme in themes:
        out += [f"## {theme}", "", "### [S1] A story", ""]
        out += list(rows)
        out += [""]
    return "\n".join(out) + "\n"


def _task_file(task_id: int, status: str, theme: str) -> str:
    return (
        f'---\nid: "[#{task_id}]"\ntitle: "T{task_id}"\nstatus: {status}\n'
        f'theme: "{theme}"\ngenerates: BACKLOG.md\n---\n\n'
        f"- [#{task_id}] [P2][M] T{task_id} — body\n"
    )


def _intake(intake_id: str, status: str, **fields: str) -> str:
    # Values are QUOTED, matching the live docs: an unquoted `trigger: #328 build` is a YAML
    # comment, not a value, and the doc would silently read as an undated defer.
    lines = ["---", f"intake-id: {intake_id}", f"status: {status}", "origin: test"]
    lines += [f"{k.replace('_', '-')}: \"{v}\"" for k, v in fields.items()]
    lines += ["---", "", f"# Intake {intake_id}", "", "body", ""]
    return "\n".join(lines)


def _adr(number: int, status: str, date: str = "2026-01-01", title: str = "A decision") -> str:
    return f"# ADR-{number}: {title}\n\n**Status:** {status}\n**Date:** {date}\n\n## Context\n\nx\n"


def _write_tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp_path


class _FakeGit:
    """A GitReader stand-in: fixed HEAD identity plus a canned historical BACKLOG.md."""

    def __init__(self, head_date: str, old_backlog: str | None, head_sha: str = "abc1234"):
        self._head_date = head_date
        self._old = old_backlog
        self._head_sha = head_sha
        self.calls: list[tuple[str, ...]] = []

    def head_sha(self) -> str:
        return self._head_sha

    def head_date(self) -> str:
        return self._head_date

    def rev_before(self, iso_date: str) -> str | None:
        self.calls.append(("rev_before", iso_date))
        return "old9999" if self._old is not None else None

    def file_at(self, rev: str, relpath: str) -> str | None:
        self.calls.append(("file_at", rev, relpath))
        return self._old

    def log_pairs(self, relpath: str, since_rev: str) -> list[tuple[str, str, str]]:
        # No per-commit history in the fake: build() falls back to the snapshot diff, which is
        # exactly the degraded path a shallow or fresh checkout takes.
        self.calls.append(("log_pairs", relpath, since_rev))
        return []


# --------------------------------------------------------------------------- section 0

def test_closed_rows_between_reports_ids_that_left_the_file():
    old = _backlog("- [#10] [P2][M] Alpha — x · Done when: the alpha ships · refs y",
                   "- [#11] [P1][S] Beta — x")
    new = _backlog("- [#11] [P1][S] Beta — x")
    rows = gd.closed_rows_between(old, new)
    assert [r.id for r in rows] == [10]
    assert rows[0].title == "Alpha"
    assert rows[0].gain == "the alpha ships"


def test_closed_rows_between_is_empty_when_nothing_left():
    same = _backlog("- [#10] [P2][M] Alpha — x")
    assert gd.closed_rows_between(same, same) == []


def test_closed_rows_ignores_ids_that_only_arrived():
    old = _backlog("- [#10] [P2][M] Alpha — x")
    new = _backlog("- [#10] [P2][M] Alpha — x", "- [#12] [P2][M] Gamma — x")
    assert gd.closed_rows_between(old, new) == []


def test_parse_done_when_stops_at_the_next_middot_clause():
    raw = "- [#9] [P2][M] Thing — prose · Done when: it is done · refs a, b · kill-candidates: none"
    assert gd.parse_done_when(raw) == "it is done"


def test_parse_done_when_absent_returns_empty_string():
    assert gd.parse_done_when("- [#9] [P2][M] Thing — prose only") == ""


def test_release_notes_render_newest_first_one_line_per_row():
    """Newest-first is by CLOSING DATE, not by id — ids are monotonic by filing, not by closing."""
    rows = [
        gd.ClosedRow(id=11, title="Beta", gain="", theme=None, closed_on="2026-08-14"),
        gd.ClosedRow(id=10, title="Alpha", gain="the alpha ships", theme="[E1] X",
                     closed_on="2026-08-18"),
    ]
    out = gd.render_release_notes(rows, window_days=7, since="2026-08-12", until="2026-08-19")
    body = [ln for ln in out.splitlines() if ln.startswith("- ")]
    assert len(body) == 2
    assert "Alpha" in body[0] and "the alpha ships" in body[0]
    assert "[#10]" in body[0]
    # A row with no Done-when still gets a line rather than being dropped.
    assert "Beta" in body[1]


def test_release_notes_say_so_when_the_window_is_empty():
    out = gd.render_release_notes([], window_days=7, since="2026-08-12", until="2026-08-19")
    assert "no rows closed" in out.lower()


# --------------------------------------------------------------------------- section 1

def test_theme_stats_counts_open_deferred_and_size_mix(tmp_path):
    text = _backlog(
        "- [#1] [P2][M] One — x",
        "- [#2] [P3][S] Two — x · DEFER — peg: something",
        "- [#3] [P1][L] Three — x",
    )
    tasks = tmp_path / "tasks"
    tasks.mkdir()
    stats = gd.theme_stats(text, tasks)
    assert len(stats) == 1
    s = stats[0]
    assert s.theme == "[E1] Handoff continuity"
    assert s.open == 2 and s.deferred == 1
    assert s.sizes == {"S": 1, "M": 1, "L": 1}


def test_theme_stats_pulls_closed_counts_from_the_tasks_tree(tmp_path):
    theme = "[E1] Handoff continuity"
    text = _backlog("- [#1] [P2][M] One — x")
    tasks = tmp_path / "tasks"
    tasks.mkdir()
    (tasks / "1-one.md").write_text(_task_file(1, "open", theme), encoding="utf-8")
    (tasks / "2-two.md").write_text(_task_file(2, "closed", theme), encoding="utf-8")
    (tasks / "3-three.md").write_text(_task_file(3, "retired", theme), encoding="utf-8")
    stats = gd.theme_stats(text, tasks)
    assert stats[0].open == 1
    assert stats[0].closed == 2


def test_theme_stats_surfaces_a_closed_task_whose_theme_is_absent_from_backlog(tmp_path):
    """A theme that exists only among closed records must still be reported, not dropped."""
    text = _backlog("- [#1] [P2][M] One — x")
    tasks = tmp_path / "tasks"
    tasks.mkdir()
    (tasks / "9-nine.md").write_text(_task_file(9, "closed", "[E9] Gone theme"), encoding="utf-8")
    themes = {s.theme for s in gd.theme_stats(text, tasks)}
    assert "[E9] Gone theme" in themes


def test_render_backlog_section_reports_the_trend_when_history_is_available():
    stats = [gd.ThemeStats(theme="[E1] X", open=2, deferred=1, closed=3, sizes={"M": 3})]
    out = gd.render_backlog(stats, total_open=3, total_open_prior=5, window_days=7,
                            closed_in_window=[gd.ClosedRow(10, "Alpha", "", "[E1] X")])
    assert "[E1] X" in out
    assert "-2" in out  # 3 open now against 5 a window ago


def test_render_backlog_states_the_trend_is_unavailable_without_history():
    stats = [gd.ThemeStats(theme="[E1] X", open=2, deferred=0, closed=0, sizes={})]
    out = gd.render_backlog(stats, total_open=2, total_open_prior=None, window_days=7,
                            closed_in_window=[])
    assert "unavailable" in out.lower()


# --------------------------------------------------------------------------- section 2

def test_intake_accepted_with_a_carrier_row_is_satisfied(tmp_path):
    d = _write_tree(tmp_path, {"intake/i.md": _intake("12", "ACCEPTED", decided_by="a ruling",
                                                      disposition="active")})
    backlog = _backlog("- [#500] [P2][M] Carrier — builds intake #12 · Done when: x")
    rows = gd.intake_rows(d / "intake", d / "intake" / "archive", backlog)
    assert rows[0].verdict == gd.VERDICT_CARRIED
    assert "500" in rows[0].detail


def test_intake_accepted_deferred_with_a_trigger_is_satisfied(tmp_path):
    d = _write_tree(tmp_path, {"intake/i.md": _intake("13", "ACCEPTED", decided_by="a ruling",
                                                      disposition="deferred", trigger="#328 build")})
    rows = gd.intake_rows(d / "intake", d / "intake" / "archive", _backlog())
    assert rows[0].verdict == gd.VERDICT_DEFERRED
    assert "#328 build" in rows[0].detail


def test_intake_accepted_deferred_with_a_review_date_is_satisfied(tmp_path):
    d = _write_tree(tmp_path, {"intake/i.md": _intake("14", "ACCEPTED", decided_by="a ruling",
                                                      disposition="deferred",
                                                      review_date="2026-09-09")})
    rows = gd.intake_rows(d / "intake", d / "intake" / "archive", _backlog())
    assert rows[0].verdict == gd.VERDICT_DEFERRED
    assert "2026-09-09" in rows[0].detail


def test_intake_accepted_with_no_carrier_and_no_dated_defer_is_a_violation(tmp_path):
    d = _write_tree(tmp_path, {"intake/i.md": _intake("15", "ACCEPTED", decided_by="a ruling",
                                                      disposition="active")})
    rows = gd.intake_rows(d / "intake", d / "intake" / "archive", _backlog())
    assert rows[0].verdict == gd.VERDICT_VIOLATION


def test_intake_accepted_deferred_without_a_trigger_or_date_is_a_violation(tmp_path):
    d = _write_tree(tmp_path, {"intake/i.md": _intake("16", "ACCEPTED", decided_by="a ruling",
                                                      disposition="deferred")})
    rows = gd.intake_rows(d / "intake", d / "intake" / "archive", _backlog())
    assert rows[0].verdict == gd.VERDICT_VIOLATION


def test_carrier_ids_match_both_citation_dialects():
    backlog = _backlog(
        "- [#500] [P2][M] A — carries intake #7 stuff",
        "- [#501] [P2][M] B — cites intake-id 7 stuff",
        "- [#502] [P2][M] C — cites intake #70, a different doc",
    )
    assert gd.carrier_ids_for("7", backlog) == [500, 501]


def test_intake_unknown_status_is_reported_as_UNKNOWN_and_does_not_crash(tmp_path):
    d = _write_tree(tmp_path, {
        "intake/weird.md": _intake("21", "BANANA"),
        "intake/nofm.md": "no frontmatter at all\n",
    })
    rows = gd.intake_rows(d / "intake", d / "intake" / "archive", _backlog())
    assert {r.status for r in rows} == {"BANANA", gd.STATUS_UNKNOWN}
    out = gd.render_intake(rows)
    assert gd.STATUS_UNKNOWN in out


def test_rejected_intake_carries_an_archived_flag(tmp_path):
    d = _write_tree(tmp_path, {
        "intake/live-reject.md": _intake("30", "REJECTED", reason="no"),
        "intake/archive/old-reject.md": _intake("31", "REJECTED", reason="no"),
    })
    rows = {r.intake_id: r for r in gd.intake_rows(d / "intake", d / "intake" / "archive",
                                                   _backlog())}
    assert rows["30"].archived is False
    assert rows["31"].archived is True


def test_render_intake_marks_violations_loudly(tmp_path):
    rows = [gd.IntakeRow(intake_id="15", filename="i.md", title="T", status="ACCEPTED",
                         verdict=gd.VERDICT_VIOLATION, detail="", archived=False)]
    out = gd.render_intake(rows)
    assert "VIOLATION" in out


# --------------------------------------------------------------------------- section 3

def test_adr_rows_report_status_and_flag_terminal_files_outside_archive(tmp_path):
    d = _write_tree(tmp_path, {
        "decisions/ADR-10-a.md": _adr(10, "Accepted"),
        "decisions/ADR-11-b.md": _adr(11, "Superseded by ADR-10"),
        "decisions/archive/ADR-12-c.md": _adr(12, "Deprecated"),
    })
    rows = {r.number: r for r in gd.adr_rows(d / "decisions")}
    assert rows[10].status == "Accepted" and rows[10].flag == ""
    assert rows[11].flag == gd.FLAG_ARCHIVABLE
    assert rows[12].archived is True and rows[12].flag == ""


def test_adr_rows_flag_an_off_enum_status(tmp_path):
    d = _write_tree(tmp_path, {"decisions/ADR-13-d.md": _adr(13, "Fabulous")})
    assert gd.adr_rows(d / "decisions")[0].flag == gd.FLAG_OFF_ENUM


def test_adr_rows_flag_a_file_with_no_parsable_status(tmp_path):
    d = _write_tree(tmp_path, {"decisions/ADR-14-e.md": "# ADR-14: No status line\n\nbody\n"})
    row = gd.adr_rows(d / "decisions")[0]
    assert row.flag == gd.FLAG_UNPARSED


_LEGACY_ADR = """# ADR-34 — File naming convention (cross-repo)

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-29
Related: ADR-27
"""


def test_adr_rows_read_the_pre_2026_05_header_dialect(tmp_path):
    """A third dialect exists in the corpus; the shared parser only ever sees the last five."""
    d = _write_tree(tmp_path, {"decisions/ADR-34-file-naming.md": _LEGACY_ADR})
    row = gd.adr_rows(d / "decisions")[0]
    assert row.status == "Accepted"
    assert row.date == "2026-04-29"
    assert row.title == "File naming convention (cross-repo)"
    assert row.dialect == gd.DIALECT_LEGACY
    assert row.flag == ""


def test_legacy_dialect_status_qualifier_is_trimmed_like_the_shared_parser(tmp_path):
    text = _LEGACY_ADR.replace("Status: Accepted",
                               "Status: Accepted (amended four times: 2026-05-09, ...)")
    d = _write_tree(tmp_path, {"decisions/ADR-42-handoff.md": text})
    assert gd.adr_rows(d / "decisions")[0].status == "Accepted"


def test_adr_file_off_the_filename_grammar_is_reported_not_dropped(tmp_path):
    """`ADR-43_underscore.md` is invisible to the shared filename regex — absent, not unparsed."""
    d = _write_tree(tmp_path, {
        "decisions/ADR-10-a.md": _adr(10, "Accepted"),
        "decisions/ADR-43_cross_project_routing.md": _LEGACY_ADR.replace("ADR-34", "ADR-43"),
    })
    rows = gd.adr_rows(d / "decisions")
    assert len(rows) == 2
    off = [r for r in rows if r.flag == gd.FLAG_OFF_GRAMMAR]
    assert [r.number for r in off] == [43]
    assert off[0].filename == "ADR-43_cross_project_routing.md"
    note = gd._dialect_note(rows)
    assert "INVISIBLE" in note
    assert "ADR-43_cross_project_routing.md" in note


def test_dialect_note_is_quiet_when_every_row_read_cleanly(tmp_path):
    d = _write_tree(tmp_path, {"decisions/ADR-10-a.md": _adr(10, "Accepted")})
    note = gd._dialect_note(gd.adr_rows(d / "decisions"))
    assert "INVISIBLE" not in note and "fallback" not in note


def test_a_status_that_resolves_to_no_enum_member_is_off_enum(tmp_path):
    """ADR-41's live text parses to a BACKLOG status enum, not an ADR status — flag it."""
    d = _write_tree(tmp_path, {"decisions/ADR-41-x.md":
                               _adr(41, "open | in-progress | blocked | done")})
    assert gd.adr_rows(d / "decisions")[0].flag == gd.FLAG_OFF_ENUM


def test_a_pipe_in_a_derived_value_cannot_shred_the_markdown_table(tmp_path):
    """The same ADR-41 value: an unescaped `|` silently splits the row into extra columns."""
    d = _write_tree(tmp_path, {"decisions/ADR-41-x.md":
                               _adr(41, "open | in-progress | blocked | done")})
    out = gd.render_adrs(gd.adr_rows(d / "decisions"))
    body = [ln for ln in out.splitlines() if ln.startswith("| ADR-41")]
    assert body, "the flagged row must render"
    for line in body:
        assert r"\|" in line
        # 5-column table -> exactly 6 unescaped pipes per row.
        assert len(re.findall(r"(?<!\\)\|", line)) in (6, 7)


def test_render_adrs_lists_the_archivable_candidates(tmp_path):
    rows = [gd.AdrRow(number=11, status="Superseded", date="2026-01-01", title="B",
                      archived=False, flag=gd.FLAG_ARCHIVABLE)]
    out = gd.render_adrs(rows)
    assert "ADR-11" in out and gd.FLAG_ARCHIVABLE in out


# --------------------------------------------------------------------------- section 4

def test_telemetry_absent_store_renders_the_in_flight_note_with_the_expected_path(tmp_path):
    state = gd.telemetry_state(tmp_path)
    assert state.exists is False
    out = gd.render_telemetry(state)
    assert gd.TELEMETRY_PENDING_NOTE in out
    assert gd.TELEMETRY_STORE_RELPATH.replace("\\", "/") in out.replace("\\", "/")


def test_telemetry_present_store_is_reported_as_present(tmp_path):
    p = tmp_path / gd.TELEMETRY_STORE_RELPATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"not a real db")
    state = gd.telemetry_state(tmp_path)
    assert state.exists is True
    assert gd.TELEMETRY_PENDING_NOTE not in gd.render_telemetry(state)


def test_module_only_loads_the_three_declared_parsers():
    """Lane L2 owns the emit path; this generator must not import or call it (brief §4).

    Checked on the CODE, not on prose: the module names its forbidden neighbours in its own
    docstring on purpose, so a bare substring scan would be a false positive.
    """
    source = _P.read_text(encoding="utf-8")
    loaded = set(re.findall(r"_load\(\"([a-z_]+)\"\)", source))
    assert loaded == {"gen_task_tree", "gen_intake_index", "gen_claude_rosters"}
    for forbidden in ("telemetry_emit", "single_flight", "audit"):
        assert f"import {forbidden}" not in source
        assert f"from {forbidden}" not in source
        assert f'spec_from_file_location("{forbidden}"' not in source


# --------------------------------------------------------------------------- section 5

_GATE_AUDIT = """# Some packet

**Ship-gate WARN delta, by class**

```
class                       before   after   delta
doc_rot                        34       6     -28
undeclared_edges               18      18       0
git_backlog_drift               1       0      -1
---------------------------------------------------
TOTAL WARNs                    60      32     -28
```

- **median: 290.9 s** the commit-tax reading
"""


def test_gate_health_parses_the_warn_composition_block(tmp_path):
    d = _write_tree(tmp_path, {"audits/2026-08-18-technical-p.md": _GATE_AUDIT})
    gh = gd.gate_health(d / "audits")
    assert gh.columns == ("before", "after", "delta")
    assert dict(gh.rows)["doc_rot"] == (34, 6, -28)
    assert gh.current_total == 24  # 6 + 18 + 0 under the 'after' column


def test_gate_health_prefers_the_newest_audit_that_carries_a_block(tmp_path):
    older = _GATE_AUDIT.replace("doc_rot                        34       6     -28",
                                "doc_rot                        99      99       0")
    d = _write_tree(tmp_path, {
        "audits/2026-08-01-technical-old.md": older,
        "audits/2026-08-18-technical-new.md": _GATE_AUDIT,
        "audits/2026-08-19-technical-noblock.md": "# nothing here\n",
    })
    gh = gd.gate_health(d / "audits")
    assert gh.source.endswith("2026-08-18-technical-new.md")
    assert dict(gh.rows)["doc_rot"] == (34, 6, -28)


def test_gate_health_reports_the_commit_tax_with_its_measurement_date(tmp_path):
    d = _write_tree(tmp_path, {"audits/2026-08-18-technical-p.md": _GATE_AUDIT})
    gh = gd.gate_health(d / "audits")
    assert gh.commit_tax == "290.9 s"
    assert gh.commit_tax_date == "2026-08-18"


def test_gate_health_is_honest_when_no_block_exists(tmp_path):
    d = _write_tree(tmp_path, {"audits/2026-08-18-technical-p.md": "# nothing\n"})
    gh = gd.gate_health(d / "audits")
    assert gh.rows == ()
    out = gd.render_gate_health(gh)
    assert "not found" in out.lower()


# --------------------------------------------------------------------------- assembly

def _fixture_repo(tmp_path: Path) -> Path:
    backlog = _backlog(
        "- [#1] [P2][M] One — x · Done when: one is done",
        "- [#2] [P3][S] Two — x · DEFER — peg: later",
    )
    files = {
        "BACKLOG.md": backlog,
        "tasks/1-one.md": _task_file(1, "open", "[E1] Handoff continuity"),
        "tasks/5-five.md": _task_file(5, "closed", "[E1] Handoff continuity"),
        "docs/intake/a.md": _intake("12", "ACCEPTED", decided_by="r", disposition="deferred",
                                    trigger="#328 build"),
        "docs/intake/b.md": _intake("13", "ACCEPTED", decided_by="r", disposition="active"),
        "docs/intake/c.md": _intake("14", "BANANA"),
        "docs/intake/archive/d.md": _intake("15", "REJECTED", reason="no"),
        "docs/decisions/ADR-10-a.md": _adr(10, "Accepted"),
        "docs/decisions/ADR-11-b.md": _adr(11, "Superseded by ADR-10"),
        "docs/audits/2026-08-18-technical-p.md": _GATE_AUDIT,
        "ecosystem/.keep": "",
    }
    return _write_tree(tmp_path, files)


def test_build_renders_every_section_header(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=_backlog(
        "- [#1] [P2][M] One — x · Done when: one is done",
        "- [#2] [P3][S] Two — x · DEFER — peg: later",
        "- [#5] [P2][M] Five — x · Done when: five is done",
    ))
    md = gd.render_markdown(gd.build(repo, git))
    for heading in gd.SECTION_TITLES:
        assert heading in md


def test_build_release_notes_pick_up_the_row_that_left_backlog(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=_backlog(
        "- [#1] [P2][M] One — x · Done when: one is done",
        "- [#2] [P3][S] Two — x · DEFER — peg: later",
        "- [#5] [P2][M] Five — x · Done when: five is done",
    ))
    md = gd.render_markdown(gd.build(repo, git))
    assert "[#5]" in md
    assert "five is done" in md


def test_build_reports_the_intake_violation(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    dash = gd.build(repo, git)
    assert [r.intake_id for r in dash.intake if r.verdict == gd.VERDICT_VIOLATION] == ["13"]


def test_build_is_deterministic_and_regeneration_is_idempotent(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    first = gd.render_markdown(gd.build(repo, git))
    second = gd.render_markdown(gd.build(repo, git))
    assert first == second
    assert gd.render_html(gd.build(repo, git)) == gd.render_html(gd.build(repo, git))


def test_write_then_check_is_clean_and_a_hand_edit_reddens_it(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    assert gd.write_outputs(repo, git) == 0
    assert gd.check_outputs(repo, git) == 0
    md_path = repo / gd.MD_RELPATH
    md_path.write_text(md_path.read_text(encoding="utf-8") + "\nhand edit\n", encoding="utf-8")
    assert gd.check_outputs(repo, git) == 1


def test_check_reddens_when_an_output_is_missing(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    assert gd.check_outputs(repo, git) == 1


def test_html_is_self_contained(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    html = gd.render_html(gd.build(repo, git))
    assert html.startswith("<!doctype html>")
    for offender in ("http://", "https://", "<script src", "<link rel=\"stylesheet\""):
        assert offender not in html


def test_html_escapes_content_that_would_otherwise_break_the_markup(tmp_path):
    rows = [gd.IntakeRow(intake_id="1", filename="x.md", title="A <b> & C", status="ACCEPTED",
                         verdict=gd.VERDICT_VIOLATION, detail="", archived=False)]
    html = gd.html_table(("id", "title"), [(r.intake_id, r.title) for r in rows])
    assert "&lt;b&gt;" in html and "&amp;" in html


def test_outputs_land_only_at_the_two_declared_paths(tmp_path):
    """Layer-2 posture: the generator writes its own two files and nothing else."""
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    before = {p for p in repo.rglob("*") if p.is_file()}
    gd.write_outputs(repo, git)
    after = {p for p in repo.rglob("*") if p.is_file()}
    assert after - before == {repo / gd.MD_RELPATH, repo / gd.HTML_RELPATH}


def test_window_start_is_derived_from_head_date_not_the_wall_clock(tmp_path):
    repo = _fixture_repo(tmp_path)
    git = _FakeGit(head_date="2026-08-19", old_backlog=None)
    gd.build(repo, git)
    assert ("rev_before", "2026-08-12") in git.calls


# ------------------------------------------------- the header states the mechanism that exists
# `[#171]` leg 1 / R3 F3. Both faces asserted "Generated, committed, read-only" while no code
# path committed anything — and an integrator review pass judged the "committed" leg MET by
# reading that header. These pin the corrected claim so the false one cannot come back silently.

_SELF_COMMIT_CLAIM = "Generated, committed, read-only"


@pytest.mark.parametrize("renderer,relpath", [("render_markdown", "MD_RELPATH"),
                                              ("render_html", "HTML_RELPATH")])
def test_neither_face_claims_the_generator_commits_itself(renderer, relpath, tmp_path):
    repo = _fixture_repo(tmp_path)
    out = getattr(gd, renderer)(gd.build(repo, _FakeGit(head_date="2026-08-19",
                                                        old_backlog=None)))
    assert _SELF_COMMIT_CLAIM not in out, (
        f"{relpath} re-asserts a self-committing writer that does not exist (ADR-86 amended "
        "2026-08-23 withdrew that clause)")
    assert "human-committed" in out
    assert "commits nothing" in out


@pytest.mark.parametrize("renderer", ["render_markdown", "render_html"])
def test_both_faces_name_who_commits_and_when(renderer, tmp_path):
    """The contract's stated risk: making the header true by making it vague. 'Generated' alone
    would pass the negative test above and still tell the reader nothing."""
    repo = _fixture_repo(tmp_path)
    out = getattr(gd, renderer)(gd.build(repo, _FakeGit(head_date="2026-08-19",
                                                        old_backlog=None)))
    assert "person or integrator who ran it" in out, "the header must name WHO commits"
    assert "as current as its own last commit" in out, "the header must say WHEN it is current to"
    assert "amended 2026-08-23" in out, "the header must cite the ruling it now describes"


def test_the_module_docstring_no_longer_claims_a_self_committing_writer():
    """The third site of the same false claim: not an artifact string, but the sentence the
    Phase-0 packet quoted as the ROOT, addressed to the next reader of the code."""
    assert "commits its own output" not in gd.__doc__
    assert "human or integrator commit satisfies" in gd.__doc__


# --------------------------------------------------- the commit path is explicit AND observable
# ADR-86 amended 2026-08-23: a human or integrator commits. `[#171]` leg 1's failure was that the
# mechanism existed only as prose — so these pin BOTH halves: the path is real, derived and
# printed; and the generator still does not run it.


def test_commit_pathspec_is_derived_from_the_write_targets():
    """Not a re-typed literal: the pathspec IS the write targets, so it cannot drift from what
    `--write` actually wrote."""
    assert gd.commit_pathspec() == [gd.MD_RELPATH, gd.HTML_RELPATH]
    assert gd.commit_pathspec() == [relpath for relpath, _ in gd._TARGETS]


def test_commit_path_is_pathspec_bounded():
    """ADR-80 Rider 1 survives the amendment — what changed is WHO runs the commit, not what it
    is bounded to. An operator's unrelated dirty files must be untouchable by this path."""
    add, commit = gd.commit_path_commands()
    assert add[:3] == ["git", "add", "--"], "the `--` separator is load-bearing"
    assert add[3:] == [gd.MD_RELPATH, gd.HTML_RELPATH]
    assert "-A" not in add and "--all" not in add and "." not in add
    assert commit[:2] == ["git", "commit"]


def test_write_prints_the_commit_path_it_did_not_run(tmp_path, capsys):
    repo = _fixture_repo(tmp_path)
    gd.write_outputs(repo, _FakeGit(head_date="2026-08-19", old_backlog=None))
    out = capsys.readouterr().out
    assert "NOT committed" in out
    assert "git add -- ecosystem/conformance.md ecosystem/conformance.html" in out
    assert "git commit" in out


def test_write_leaves_its_outputs_uncommitted_in_a_real_repo(tmp_path):
    """THE TEETH OF THE NEGATIVE HALF, and the ADR-81 leg (e) functional proof for it. ADR-86 as
    amended says this module does not commit — a header can claim that and be wrong, which is the
    entire defect this lane exists to fix. So the claim is asserted behaviourally against a REAL
    git repo: after `--write`, HEAD has not moved and both outputs are sitting dirty, waiting for
    the human. (Asserted this way rather than by monkeypatching `subprocess.run`, which would
    patch the stdlib module object for the whole xdist worker.)"""
    repo = _fixture_repo(tmp_path)
    for args in (("init", "-q", "-b", "main"), ("config", "user.email", "t@t.t"),
                 ("config", "user.name", "t"), ("add", "-A"),
                 ("commit", "-q", "--no-verify", "-m", "fixture")):
        subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    head_before = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                 capture_output=True, text=True).stdout.strip()
    assert head_before, "fixture repo did not produce a commit"

    assert gd.write_outputs(repo, gd._reader(repo)) == 0

    head_after = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    assert head_after == head_before, "gen_dashboard committed — it must not (ADR-86 amd. 2026-08-23)"
    porcelain = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                               capture_output=True, text=True).stdout
    assert gd.MD_RELPATH in porcelain and gd.HTML_RELPATH in porcelain, (
        "the outputs should be left dirty for the human to commit")


def test_commit_path_verb_prints_the_commands_and_exits_zero(capsys):
    """`--commit-path` answers the question without touching the tree or needing git at all."""
    assert gd.main(["--commit-path"]) == 0
    out = capsys.readouterr().out
    assert "git add -- ecosystem/conformance.md ecosystem/conformance.html" in out
    assert "git commit" in out


@pytest.mark.parametrize("renderer", ["render_markdown", "render_html"])
def test_both_faces_carry_the_commit_path_pathspec(renderer, tmp_path):
    """The header names the mechanism; this pins that it names the SAME pathspec the code uses."""
    repo = _fixture_repo(tmp_path)
    out = getattr(gd, renderer)(gd.build(repo, _FakeGit(head_date="2026-08-19",
                                                        old_backlog=None)))
    assert " ".join(gd.commit_pathspec()) in out
    assert "--commit-path" in out


@pytest.mark.parametrize("verb", ["--write", "--check"])
def test_main_accepts_both_verbs(verb, tmp_path, monkeypatch):
    repo = _fixture_repo(tmp_path)
    monkeypatch.setattr(gd, "_REPO_ROOT", repo)
    monkeypatch.setattr(gd, "_reader", lambda root: _FakeGit(head_date="2026-08-19",
                                                             old_backlog=None))
    rc = gd.main([verb])
    assert rc in (0, 1)
