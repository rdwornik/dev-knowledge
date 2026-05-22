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
from codemap.mermaid_emit import emit_mermaid  # noqa: E402
from codemap.generator import generate_codemap  # noqa: E402


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


# ---------------------------------------------------------------------------
# Step 2 — mermaid_emit
# ---------------------------------------------------------------------------


def test_mermaid_emit_simple():
    out = emit_mermaid(["pkg_a", "pkg_b"], [("pkg_a", "pkg_b")])
    assert out.startswith("flowchart TD\n")
    assert "pkg_a[pkg_a]" in out
    assert "pkg_b[pkg_b]" in out
    assert "pkg_a --> pkg_b" in out
    assert "classDef foundation" in out


def test_mermaid_emit_orphan_class():
    out = emit_mermaid(["pkg_a", "pkg_b", "pkg_c"], [("pkg_a", "pkg_b")])
    assert "pkg_c[pkg_c]:::orphan" in out


def test_mermaid_emit_cycle_class():
    packages = ["pkg_a", "pkg_b"]
    edges = [("pkg_a", "pkg_b"), ("pkg_b", "pkg_a")]
    out = emit_mermaid(packages, edges)
    assert "linkStyle" in out
    assert "stroke:#e03131" in out


def test_mermaid_emit_layers():
    layers = {"pkg_a": "core", "pkg_b": "foundation"}
    out = emit_mermaid(["pkg_a", "pkg_b"], [("pkg_a", "pkg_b")], layers=layers)
    assert "pkg_a[pkg_a]:::core" in out
    assert "pkg_b[pkg_b]:::foundation" in out


def test_mermaid_emit_click_directives():
    out = emit_mermaid(["pkg_a", "pkg_b"], [], click_directives=True)
    assert 'click pkg_a href "src/pkg_a/"' in out
    assert 'click pkg_b href "src/pkg_b/"' in out


def test_mermaid_emit_deterministic():
    packages = ["pkg_b", "pkg_a"]
    edges = [("pkg_b", "pkg_a"), ("pkg_a", "pkg_b")]
    r1 = emit_mermaid(packages, edges)
    r2 = emit_mermaid(packages, edges)
    assert r1 == r2


# ---------------------------------------------------------------------------
# Step 3 — generator
# ---------------------------------------------------------------------------

WITH_TACH = FIXTURES / "codemap-with-tach"
WITH_ORPHAN = FIXTURES / "codemap-with-orphan"
WITH_CYCLE = FIXTURES / "codemap-with-cycle"


def test_generator_full_flow():
    mermaid, warnings = generate_codemap(SIMPLE_REPO)
    assert mermaid.startswith("flowchart TD\n")
    assert "pkg_a" in mermaid
    assert "pkg_b" in mermaid
    assert "pkg_a --> pkg_b" in mermaid
    assert warnings == []


def test_generator_with_tach():
    mermaid, warnings = generate_codemap(WITH_TACH)
    assert "pkg_a[pkg_a]:::core" in mermaid
    assert "pkg_b[pkg_b]:::foundation" in mermaid


def test_generator_orphan_warning():
    mermaid, warnings = generate_codemap(WITH_ORPHAN)
    assert any("orphan" in w for w in warnings)
    assert "pkg_orphan[pkg_orphan]:::orphan" in mermaid


def test_generator_cycle_warning():
    mermaid, warnings = generate_codemap(WITH_CYCLE)
    assert any("circular" in w for w in warnings)
    assert "linkStyle" in mermaid


def test_generator_no_tach():
    mermaid, warnings = generate_codemap(SIMPLE_REPO)
    # no tach.toml in simple-repo → no layer classes, no tach warning
    assert not any("tach" in w.lower() for w in warnings)
    assert "flowchart TD" in mermaid
