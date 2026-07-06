"""Coverage for scripts/gen_audit_index.py (Block-3.3 audits navigation index)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_audit_index as gai  # noqa: E402


def _audit(d: Path, name: str, title: str | None = "T") -> None:
    body = (f"# {title}\n\nbody\n" if title is not None else "no heading here\n")
    (d / name).write_text(body, encoding="utf-8")


def test_collect_parses_date_slug_title_and_sorts_newest_first(tmp_path):
    _audit(tmp_path, "2026-01-02-alpha.md", "Alpha audit")
    _audit(tmp_path, "2026-07-05-zulu.md", "Zulu audit")
    rows = gai.collect_audits(tmp_path)
    assert [r[0] for r in rows] == ["2026-07-05", "2026-01-02"]  # newest first
    assert rows[0][1] == "zulu" and rows[0][3] == "Zulu audit"


def test_collect_excludes_the_index_readme(tmp_path):
    _audit(tmp_path, "2026-01-01-x.md")
    _audit(tmp_path, "README.md", "The index itself")
    names = {r[2] for r in gai.collect_audits(tmp_path)}
    assert "README.md" not in names  # an index never indexes itself


def test_collect_undated_file_kept_not_dropped(tmp_path):
    _audit(tmp_path, "not-a-dated-name.md", "Legacy")
    rows = gai.collect_audits(tmp_path)
    assert rows == [("", "not-a-dated-name", "not-a-dated-name.md", "Legacy")]


def test_title_placeholder_when_no_heading(tmp_path):
    _audit(tmp_path, "2026-02-02-x.md", title=None)  # no `# ` heading
    rows = gai.collect_audits(tmp_path)
    assert rows[0][3] == "(no # title)"


def test_render_has_note_count_and_month_headers(tmp_path):
    _audit(tmp_path, "2026-07-05-a.md", "Ay")
    _audit(tmp_path, "2026-06-01-b.md", "Bee")
    out = gai.render_index(tmp_path)
    assert gai._GENERATED_NOTE in out
    assert "**2 audit documents.**" in out
    assert "## 2026-07" in out and "## 2026-06" in out
    assert "- [2026-07-05](2026-07-05-a.md) — Ay" in out
    # month order: 2026-07 section appears before 2026-06 (reverse-chronological)
    assert out.index("## 2026-07") < out.index("## 2026-06")
    assert out.endswith("\n")


def test_render_is_deterministic(tmp_path):
    _audit(tmp_path, "2026-05-05-x.md")
    assert gai.render_index(tmp_path) == gai.render_index(tmp_path)


def test_pipe_in_title_is_table_safe(tmp_path):
    _audit(tmp_path, "2026-03-03-x.md", "A | B title")
    assert "A / B title" in gai.render_index(tmp_path)


# --- check/write semantics via monkeypatched module targets ------------------


def _wire(tmp_path, monkeypatch):
    target = tmp_path / "README.md"
    monkeypatch.setattr(gai, "_AUDITS_DIR", tmp_path)
    monkeypatch.setattr(gai, "_TARGET", target)
    monkeypatch.setattr(gai, "_REPO_ROOT", tmp_path)
    return target


def test_check_missing_is_2(tmp_path, monkeypatch):
    _wire(tmp_path, monkeypatch)
    _audit(tmp_path, "2026-01-01-x.md")
    assert gai.main(["--check"]) == 2


def test_write_then_check_roundtrips(tmp_path, monkeypatch):
    _wire(tmp_path, monkeypatch)
    _audit(tmp_path, "2026-01-01-x.md", "Ex")
    assert gai.main(["--write"]) == 0
    assert gai.main(["--check"]) == 0


def test_check_detects_drift(tmp_path, monkeypatch, capsys):
    _wire(tmp_path, monkeypatch)
    _audit(tmp_path, "2026-01-01-x.md")
    gai.main(["--write"])
    _audit(tmp_path, "2026-08-08-new.md", "New audit")  # a new file drifts the index
    assert gai.main(["--check"]) == 1
    assert "stale vs docs/audits/" in capsys.readouterr().err


def test_live_index_is_fresh():
    # the shipped docs/audits/README.md matches disk (the generator's own green)
    assert gai.main(["--check"]) == 0
