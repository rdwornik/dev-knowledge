"""First coverage for scripts/gen_claude_rosters.py ([#258] phase-2).

The phase-1 generator (commands-repo + recent-adrs fragments) shipped with no
tests; the phase-2 freshness hook (`gen_claude_rosters.py --check`, wired as the
`claude-rosters-freshness` pre-commit gate) needs the generator's parsing +
render + check semantics pinned. Collectors/renderers take a dir param, so the
tmp cases exercise the real code path; the live-repo case proves the shipped
fragments are fresh (the gate's own green).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_claude_rosters as gcr  # noqa: E402


# --- collect_commands --------------------------------------------------------


def _cmd_file(d: Path, stem: str, *, name=None, desc=None) -> None:
    fm = ["---"]
    if name is not None:
        fm.append(f"name: {name}")
    if desc is not None:
        fm.append(f"description: {desc}")
    fm.append("---")
    (d / f"{stem}.md").write_text("\n".join(fm) + "\n\nbody\n", encoding="utf-8")


def test_collect_commands_reads_frontmatter_and_sorts(tmp_path):
    # frontmatter `name:` carries NO leading slash (render prepends the `/`).
    _cmd_file(tmp_path, "zebra", name="zed", desc="last alphabetically by file")
    _cmd_file(tmp_path, "alpha", name="aa", desc="first by filename")
    rows = gcr.collect_commands(tmp_path)
    assert [n for n, _ in rows] == ["aa", "zed"]  # filename-sorted (alpha.md < zebra.md)
    assert rows[0] == ("aa", "first by filename")


def test_collect_commands_missing_description_is_loud(tmp_path):
    _cmd_file(tmp_path, "x", name="x")  # no description
    rows = gcr.collect_commands(tmp_path)
    assert rows == [("x", "(no description frontmatter)")]


def test_collect_commands_name_falls_back_to_stem(tmp_path):
    _cmd_file(tmp_path, "no-name-cmd", desc="only a description")
    rows = gcr.collect_commands(tmp_path)
    assert rows == [("no-name-cmd", "only a description")]


# --- collect_recent_adrs -----------------------------------------------------


def _adr(d: Path, num: int, *, status="Accepted", date="2026-07-01", title="T", bare=False):
    prefix = "" if bare else "- "
    body = (
        f"# ADR-{num}: {title}\n\n"
        f"{prefix}**Status:** {status}\n"
        f"{prefix}**Date:** {date}\n"
    )
    (d / f"ADR-{num}-slug.md").write_text(body, encoding="utf-8")


def test_collect_recent_adrs_last_n_ascending(tmp_path):
    for n in (10, 11, 12, 13, 14):
        _adr(tmp_path, n, title=f"t{n}")
    rows = gcr.collect_recent_adrs(tmp_path, count=3)
    assert [r[0] for r in rows] == [12, 13, 14]  # last 3 by number, ascending


def test_collect_recent_adrs_both_status_dialects_and_qualifier_trim(tmp_path):
    _adr(tmp_path, 20, status="Accepted (ratified 2026-07-03)", bare=False)  # list form + qualifier
    _adr(tmp_path, 21, status="Proposed — pending", bare=True)               # bare form + dash qualifier
    rows = {r[0]: r for r in gcr.collect_recent_adrs(tmp_path, count=5)}
    assert rows[20][1] == "Accepted"   # parenthetical qualifier trimmed
    assert rows[21][1] == "Proposed"   # dash qualifier trimmed, bare dialect parsed


def test_collect_recent_adrs_missing_field_is_unparsed_not_dropped(tmp_path):
    (tmp_path / "ADR-30-x.md").write_text("# ADR-30: only a title\n\nno status/date\n",
                                          encoding="utf-8")
    rows = gcr.collect_recent_adrs(tmp_path, count=5)
    assert rows == [(30, "(unparsed)", "(unparsed)", "only a title")]


# --- render + generated note -------------------------------------------------


def test_render_commands_carries_generated_note(tmp_path):
    _cmd_file(tmp_path, "x", name="x", desc="d")
    out = gcr.render_commands(tmp_path)
    assert gcr._GENERATED_NOTE in out
    assert "- `/x` — d" in out
    assert out.endswith("\n")


def test_render_is_deterministic(tmp_path):
    _adr(tmp_path, 40)
    assert gcr.render_adrs(tmp_path) == gcr.render_adrs(tmp_path)  # byte-identical


# --- check semantics (live + monkeypatched drift) ----------------------------


def test_live_fragments_are_fresh():
    # the shipped fragments match disk -> the gate is green (exit 0)
    assert gcr.main(["--check"]) == 0


def test_check_reports_drift(tmp_path, monkeypatch, capsys):
    target = tmp_path / "commands-repo.md"
    target.write_text("stale content\n", encoding="utf-8")
    monkeypatch.setattr(gcr, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(gcr, "_TARGETS", [(target, lambda: "fresh content\n")])
    rc = gcr.main(["--check"])
    assert rc == 1
    assert "stale vs disk state" in capsys.readouterr().err


def test_check_reports_missing_target(tmp_path, monkeypatch):
    target = tmp_path / "absent.md"
    monkeypatch.setattr(gcr, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(gcr, "_TARGETS", [(target, lambda: "x\n")])
    assert gcr.main(["--check"]) == 2


def test_write_then_check_roundtrips(tmp_path, monkeypatch):
    target = tmp_path / "frag.md"
    monkeypatch.setattr(gcr, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(gcr, "_GENERATED_DIR", tmp_path)
    monkeypatch.setattr(gcr, "_TARGETS", [(target, lambda: "generated\n")])
    assert gcr.main(["--write"]) == 0
    assert target.read_text(encoding="utf-8") == "generated\n"
    assert gcr.main(["--check"]) == 0
