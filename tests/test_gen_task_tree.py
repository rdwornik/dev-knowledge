"""Coverage for scripts/gen_task_tree.py ([#433] BACKLOG restructure strangler STEP 1-2)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_task_tree as gtt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKLOG = REPO_ROOT / "BACKLOG.md"
TREE = REPO_ROOT / "tasks"


def test_roundtrip_live_backlog_byte_identity():
    raw = BACKLOG.read_bytes()
    text = raw.decode("utf-8")
    model = gtt.parse_backlog(text)
    assert gtt.reassemble_from_model(model) == text
    assert gtt.reassemble_from_model(model).encode("utf-8") == raw


def test_disk_roundtrip_tmp_tree_byte_identity(tmp_path):
    """THE core acceptance test: live BACKLOG.md -> tree on disk -> byte-identical text."""
    raw = BACKLOG.read_bytes()
    text = raw.decode("utf-8")
    model = gtt.parse_backlog(text)
    out_dir = tmp_path / "tasks"
    gtt.write_tree(model, out_dir)
    result = gtt.reassemble_from_tree(out_dir)
    assert result == text
    assert result.encode("utf-8") == raw


def test_committed_tree_coherent_with_backlog():
    if not (TREE / "manifest.json").exists():
        pytest.skip("tasks/ not yet generated (module 3 commits it)")
    text = BACKLOG.read_bytes().decode("utf-8")
    assert gtt.reassemble_from_tree(TREE) == text


def test_live_parse_structural_properties():
    text = BACKLOG.read_bytes().decode("utf-8")
    model = gtt.parse_backlog(text)
    tasks = [row for kind, row in model.nodes if kind == "task"]
    ids = [t.id for t in tasks]
    assert len(ids) == len(set(ids))  # unique
    for t in tasks:
        assert t.raw.startswith(f"- [#{t.id}] ")
        assert t.theme is not None
        assert t.story is not None
    assert len(tasks) > 100  # no pin on the exact live count -- known test-smell avoidance


def test_fence_guard_synthetic():
    text = "\n".join(
        [
            "# Title",
            "",
            "## [E1] Theme One",
            "",
            "### [S1] Story One",
            "- [#1] [P1][S] **Real task** — body text",
            "",
            "```",
            "- [#999] looks like a task",
            "## [E9] fenced theme-shaped line (must NOT pollute lineage)",
            "### [S9] fenced story-shaped line (must NOT pollute lineage)",
            "```",
            "",
            "| **R1** | x |",
            "",
            "- [#2] [P1][S] **Second task** — after the fence",
            "",
            "Footer text.",
            "",
        ]
    )
    model = gtt.parse_backlog(text)
    tasks = [row for kind, row in model.nodes if kind == "task"]
    ids = [t.id for t in tasks]
    assert ids == [1, 2]
    assert 999 not in ids
    assert tasks[0].theme == "[E1] Theme One"
    assert tasks[0].story == "[S1] Story One"
    # the fenced theme/story-shaped lines are prose: lineage carries across the fence
    assert tasks[1].theme == "[E1] Theme One"
    assert tasks[1].story == "[S1] Story One"
    assert gtt.reassemble_from_model(model) == text


def test_frontmatter_shape_and_body(tmp_path):
    raw = (
        "- [#42] [P2][M] **Bold title** — rest of description "
        "· serialize-group: audit-py · depends-on: 270 · DEFER — peg: x"
    )
    task = gtt.TaskRow(id=42, raw=raw, theme=None, story=None)
    model = gtt.Model(nodes=[("task", task)], source_text=raw)
    gtt.write_tree(model, tmp_path)

    fname = gtt.task_filename(task)
    file_text = (tmp_path / fname).read_bytes().decode("utf-8")
    lines = file_text.splitlines()

    assert 'id: "[#42]"' in lines
    assert "status: deferred" in lines
    assert "priority: P2" in lines
    assert "size: M" in lines
    assert "serialize-group: audit-py" in lines
    assert 'depends-on: "270"' in lines  # raw preserved, never normalized to "#270"

    assert gtt.extract_body(file_text) == raw
    assert file_text.endswith("\n")
    assert not file_text.endswith("\n\n")


def test_extract_body_rejects_malformed():
    with pytest.raises(ValueError):
        gtt.extract_body("---\nid: 1\nno closing fence in this text\n")
    with pytest.raises(ValueError):
        gtt.extract_body("id: 1\n---\n\nbody\n")


def test_crlf_rejected():
    with pytest.raises(ValueError):
        gtt.parse_backlog("a\r\nb")


def test_write_tree_never_deletes(tmp_path, capsys):
    out_dir = tmp_path / "tasks"
    out_dir.mkdir()
    (out_dir / "README.md").write_text("keep me\n", encoding="utf-8", newline="\n")
    (out_dir / "9999-stray.md").write_text("stray content\n", encoding="utf-8", newline="\n")
    (out_dir / "notes.txt").write_text("notes\n", encoding="utf-8", newline="\n")

    text = "\n".join(
        [
            "# Title",
            "",
            "## [E1] Theme",
            "",
            "### [S1] Story",
            "- [#1] [P1][S] **A task** — body",
            "",
        ]
    )
    model = gtt.parse_backlog(text)
    gtt.write_tree(model, out_dir)

    assert (out_dir / "README.md").read_text(encoding="utf-8") == "keep me\n"
    assert (out_dir / "9999-stray.md").read_text(encoding="utf-8") == "stray content\n"
    assert (out_dir / "notes.txt").read_text(encoding="utf-8") == "notes\n"

    out = capsys.readouterr().out
    orphan_lines = [line for line in out.splitlines() if "orphan (not touched):" in line]
    assert len(orphan_lines) == 1
    assert "9999-stray.md" in orphan_lines[0]


def test_check_detects_body_corruption(tmp_path):
    source = tmp_path / "BACKLOG.md"
    text = "\n".join(
        [
            "# Title",
            "",
            "## [E1] Theme",
            "",
            "### [S1] Story",
            "- [#1] [P1][S] **A task** — body",
            "",
        ]
    )
    source.write_bytes(text.encode("utf-8"))
    out_dir = tmp_path / "tasks"
    model = gtt.parse_backlog(text)
    gtt.write_tree(model, out_dir)

    task = next(row for kind, row in model.nodes if kind == "task")
    fname = gtt.task_filename(task)
    target = out_dir / fname
    corrupted = target.read_bytes().decode("utf-8").replace("body", "bidy")
    target.write_text(corrupted, encoding="utf-8", newline="\n")

    rc = gtt.main(["--check", "--source", str(source), "--out", str(out_dir)])
    assert rc == 1
