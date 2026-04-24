"""Unit tests for ratio-aware hybrid enforcement in validate_scope_tags.py."""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_scope_tags as vst


def _make_content(hybrid: int, dev: int) -> str:
    """Generate minimal markdown content with the given tag counts.

    Three preamble lines after H1 exhaust the file-level detection window so
    per-section tags are validated by the section-scan path, not the H1 path.
    """
    lines = ["# Title\n\nLine one.\n\nLine two.\n\nLine three.\n\n---\n\n"]
    for i in range(hybrid):
        lines.append(f"## Section H{i}\n<!-- scope: hybrid -->\n\nbody\n\n")
    for i in range(dev):
        lines.append(f"## Section D{i}\n<!-- scope: dev -->\n\nbody\n\n")
    return "".join(lines)


def _make_staged(tmp_path, fname: str, hybrid: int, dev: int) -> str:
    """Write a temp file and return its path string."""
    p = tmp_path / fname
    p.write_text(_make_content(hybrid, dev), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# Case 1: Stable above ceiling (30% HEAD == 30% WT) → pass
# ---------------------------------------------------------------------------
def test_ratio_pass_when_stable_above_ceiling(monkeypatch, tmp_path):
    staged = _make_staged(tmp_path, "ESSENTIALS.md", hybrid=3, dev=7)  # 30%

    def fake_head(fname):
        if fname == "ESSENTIALS.md":
            return _make_content(hybrid=3, dev=7)
        return None

    monkeypatch.setattr(vst, "_head_content", fake_head)
    exit_code, info, err = vst._enforce_ratio([staged])
    assert exit_code == 0
    assert err == ""
    assert "HEAD: 30%" in info


# ---------------------------------------------------------------------------
# Case 2: Ratio increasing from 20% to 30%, above ceiling → block
# ---------------------------------------------------------------------------
def test_ratio_block_when_increasing_above_ceiling(monkeypatch, tmp_path):
    staged = _make_staged(tmp_path, "ESSENTIALS.md", hybrid=3, dev=7)  # 30%

    def fake_head(fname):
        if fname == "ESSENTIALS.md":
            return _make_content(hybrid=2, dev=8)  # 20%
        return None

    monkeypatch.setattr(vst, "_head_content", fake_head)
    exit_code, info, err = vst._enforce_ratio([staged])
    assert exit_code == 1
    assert "regression" in err
    assert "20%" in err and "30%" in err


# ---------------------------------------------------------------------------
# Case 3: Ratio decreasing from 30% to 20% (hygiene) → pass
# ---------------------------------------------------------------------------
def test_ratio_pass_when_decreasing(monkeypatch, tmp_path):
    staged = _make_staged(tmp_path, "ESSENTIALS.md", hybrid=2, dev=8)  # 20%

    def fake_head(fname):
        if fname == "ESSENTIALS.md":
            return _make_content(hybrid=3, dev=7)  # 30%
        return None

    monkeypatch.setattr(vst, "_head_content", fake_head)
    exit_code, info, err = vst._enforce_ratio([staged])
    assert exit_code == 0
    assert err == ""


# ---------------------------------------------------------------------------
# Case 4: Genesis, working tree at 40% → block
# ---------------------------------------------------------------------------
def test_genesis_block_above_ceiling(monkeypatch, tmp_path):
    staged = _make_staged(tmp_path, "ESSENTIALS.md", hybrid=4, dev=6)  # 40%

    monkeypatch.setattr(vst, "_head_content", lambda fname: None)
    exit_code, info, err = vst._enforce_ratio([staged])
    assert exit_code == 1
    assert "genesis" in err
    assert "40%" in err


# ---------------------------------------------------------------------------
# Case 5: Genesis, working tree at 20% → pass
# ---------------------------------------------------------------------------
def test_genesis_pass_below_ceiling(monkeypatch, tmp_path):
    staged = _make_staged(tmp_path, "ESSENTIALS.md", hybrid=2, dev=8)  # 20%

    monkeypatch.setattr(vst, "_head_content", lambda fname: None)
    exit_code, info, err = vst._enforce_ratio([staged])
    assert exit_code == 0
    assert err == ""
    assert "HEAD: n/a" in info
