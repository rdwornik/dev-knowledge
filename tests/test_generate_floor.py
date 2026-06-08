"""Tests for scripts/generate_floor.py — ceiling refusal, hash stability, content fidelity,
F5 self-containment, and emit behavior (ADR-78 O2)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest
from click.testing import CliRunner

import generate_floor as gf


# ---------------------------------------------------------------------------
# The shipped template
# ---------------------------------------------------------------------------

def test_shipped_template_is_valid_under_ceiling():
    floor = gf.render_floor()
    assert gf.validate(floor) == []
    assert gf.estimate_tokens(floor) <= gf.FLOOR_TOKEN_CEILING


def test_shipped_template_is_f5_clean_and_urlless():
    floor = gf.render_floor()
    assert gf.f5_hits(floor) == []
    assert gf.url_hits(floor) == []


def test_shipped_template_whitelist_content_present():
    """Content-set fidelity: each ADR-75 methodology_surface whitelist element surfaces."""
    floor = gf.render_floor()
    assert "Model" in floor and "Effort" in floor          # prompt-header
    assert "STOP after UNDERSTAND" in floor                 # valve discipline
    assert "after each numbered step" in floor              # cadence
    assert "--no-ff" in floor and "/ship" in floor          # ship rule
    assert "/clear" in floor                                # context budget
    assert "Re-anchor rule" in floor                        # re-anchor mechanic
    assert "gotchas skill" in floor                         # safety pointer
    assert ".dev-knowledge" in floor                        # labeled escape-hatch (ADR-78 D1)


# ---------------------------------------------------------------------------
# Hash stability / determinism
# ---------------------------------------------------------------------------

def test_hash_is_deterministic():
    floor = gf.render_floor()
    assert gf.floor_sha256(floor) == gf.floor_sha256(floor)


def test_hash_is_crlf_invariant():
    """autocrlf-proof: CRLF and LF variants of the same content hash identically."""
    lf = "# Floor\n\nLine one.\nLine two.\n"
    crlf = lf.replace("\n", "\r\n")
    assert gf.floor_sha256(lf) == gf.floor_sha256(crlf)


def test_render_floor_ends_with_single_newline():
    assert gf.render_floor().endswith("\n")


# ---------------------------------------------------------------------------
# Ceiling refusal
# ---------------------------------------------------------------------------

def _write_template(tmp_path: Path, body: str) -> Path:
    t = tmp_path / "floor.md.tmpl"
    t.write_text(body, encoding="utf-8")
    return t


def test_ceiling_refusal_validate(tmp_path: Path):
    big = "# Floor\n\n" + ("word " * 2000)  # ~10k chars -> ~2860 tokens
    floor = gf.render_floor(_write_template(tmp_path, big))
    issues = gf.validate(floor)
    assert any("token ceiling exceeded" in i for i in issues)


def test_ceiling_refusal_generate_exits_1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", tmp_path / "hub.sha256")
    big = "# Floor\n\n" + ("word " * 2000)
    tpl = _write_template(tmp_path, big)
    result = CliRunner().invoke(gf.cli, ["generate", "--template", str(tpl)])
    assert result.exit_code == 1
    assert "REFUSED" in result.output
    assert not (tmp_path / "hub.sha256").exists()  # refused before any write


# ---------------------------------------------------------------------------
# F5 self-containment + zero-URL
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("leak", [
    "See [#121] in the hub backlog.",
    "Read LESSONS.md for context.",
    "Prepend to JOURNAL.md at wrap.",
    "Per ADR-78 the floor is generated.",
    "Check docs/handoffs/ for the bundle.",
])
def test_f5_leak_detected(tmp_path: Path, leak: str):
    floor = gf.render_floor(_write_template(tmp_path, f"# Floor\n\n{leak}\n"))
    assert gf.f5_hits(floor)
    assert any("F5 self-containment" in i for i in gf.validate(floor))


def test_url_policy_detected(tmp_path: Path):
    floor = gf.render_floor(_write_template(tmp_path, "# Floor\n\nSee https://example.com\n"))
    assert gf.url_hits(floor)
    assert any("zero-URL" in i for i in gf.validate(floor))


# ---------------------------------------------------------------------------
# Emit behavior
# ---------------------------------------------------------------------------

def test_generate_out_dir_writes_floor_and_matching_sidecar(tmp_path: Path, monkeypatch):
    hub_sha = tmp_path / "hub.sha256"
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", hub_sha)
    child = tmp_path / "child"
    child.mkdir()
    result = CliRunner().invoke(gf.cli, ["generate", "--out-dir", str(child)])
    assert result.exit_code == 0

    # Floor + sidecar land under the child's .claude/, NOT the repo root.
    claude_dir = child / gf.CHILD_CLAUDE_DIRNAME
    floor_file = claude_dir / gf.FLOOR_FILENAME
    sidecar = claude_dir / gf.SIDECAR_FILENAME
    assert floor_file.exists() and sidecar.exists()
    assert not (child / gf.FLOOR_FILENAME).exists()  # not at root
    # The install note (with the @-include + pre-commit install steps) is printed.
    assert "@.claude/CLAUDE-FLOOR.md" in result.output
    assert "pre-commit install" in result.output

    expected = gf.floor_sha256(floor_file.read_text(encoding="utf-8"))
    assert expected in sidecar.read_text(encoding="utf-8")
    # Hub canonical reference matches the emitted sidecar (currency anchor parity).
    assert expected in hub_sha.read_text(encoding="utf-8")


def test_generate_no_out_dir_only_refreshes_hub_ref(tmp_path: Path, monkeypatch):
    hub_sha = tmp_path / "hub.sha256"
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", hub_sha)
    result = CliRunner().invoke(gf.cli, ["generate"])
    assert result.exit_code == 0
    assert hub_sha.exists()
    assert gf.floor_sha256(gf.render_floor()) in hub_sha.read_text(encoding="utf-8")


def test_generate_refuses_bad_out_dir(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(gf, "HUB_CANONICAL_SHA", tmp_path / "hub.sha256")
    missing = tmp_path / "does-not-exist"
    result = CliRunner().invoke(gf.cli, ["generate", "--out-dir", str(missing)])
    assert result.exit_code == 1
    assert "not a directory" in result.output


def test_check_exits_0_on_shipped_template():
    result = CliRunner().invoke(gf.cli, ["check"])
    assert result.exit_code == 0
    assert "floor valid" in result.output
