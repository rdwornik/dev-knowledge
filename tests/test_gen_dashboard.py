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
    lines = ["---", f"intake-id: {intake_id}", f"status: {status}", "origin: test"]
    lines += [f"{k.replace('_', '-')}: {v}" for k, v in fields.items()]
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
    rows = [
        gd.ClosedRow(id=10, title="Alpha", gain="the alpha ships", theme="[E1] X"),
        gd.ClosedRow(id=11, title="Beta", gain="", theme=None),
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


def test_module_never_imports_telemetry_code():
    """Lane L2 owns the emit path; this generator must not import or call it (brief §4)."""
    source = _P.read_text(encoding="utf-8")
    for forbidden in ("import telemetry_emit", "from telemetry_emit", "single_flight",
                      "spec_from_file_location(\"telemetry_emit\""):
        assert forbidden not in source
    assert "telemetry_emit" not in sys.modules


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
    assert gh.current_total == 26  # 6 + 18 + 0 under the 'after' column


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


@pytest.mark.parametrize("verb", ["--write", "--check"])
def test_main_accepts_both_verbs(verb, tmp_path, monkeypatch):
    repo = _fixture_repo(tmp_path)
    monkeypatch.setattr(gd, "_REPO_ROOT", repo)
    monkeypatch.setattr(gd, "_reader", lambda root: _FakeGit(head_date="2026-08-19",
                                                             old_backlog=None))
    rc = gd.main([verb])
    assert rc in (0, 1)
