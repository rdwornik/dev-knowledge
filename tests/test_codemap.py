"""Tests for scripts/codemap/ — ast_walker, mermaid_emit, generator, check, cli."""
from __future__ import annotations

import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FIXTURES = Path(__file__).parent / "fixtures"
SIMPLE_REPO = FIXTURES / "codemap-simple-repo"
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))

from codemap.ast_walker import analyze_repo  # noqa: E402


# ---------------------------------------------------------------------------
# Step 1 — ast_walker
# ---------------------------------------------------------------------------


def test_ast_walker_simple_repo():
    result = analyze_repo(SIMPLE_REPO)
    assert result["packages"] == ["pkg_a", "pkg_b"]
    assert result["edges"] == [("pkg_a", "pkg_b")]


def test_ast_walker_no_src_dir(tmp_path, capsys):
    result = analyze_repo(tmp_path)
    assert result == {"packages": [], "edges": []}
    captured = capsys.readouterr()
    assert "warning" in captured.err.lower()


def test_ast_walker_skips_relative(tmp_path):
    src = tmp_path / "src"
    pkg_a = src / "pkg_a"
    pkg_b = src / "pkg_b"
    for d in [pkg_a, pkg_b]:
        d.mkdir(parents=True)
        (d / "__init__.py").write_text("")
    (pkg_a / "mod.py").write_text("from . import something\nfrom .sub import x\n")
    result = analyze_repo(tmp_path)
    assert result["edges"] == []


def test_ast_walker_deterministic():
    r1 = analyze_repo(SIMPLE_REPO)
    r2 = analyze_repo(SIMPLE_REPO)
    assert r1 == r2
