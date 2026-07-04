"""Tests for scripts/gen_methodology_roster.py — the [#244] P3 roster generator.

The generator turns the manifest's `components:[].roster` (the deployed methodology corpus)
into `.claude/methodology-roster.md`, `@`-imported into CLAUDE.md. These tests guard the
things that could silently break the R3 close: the active/removed/null FILTER, the
leading-@import NEUTRALIZE (so the @-imported file does not recurse into a dangling floor
import on the hub), DETERMINISM (the drift check depends on byte-identical regen), fixed
SECTION ORDER, and the --check exit-code contract (0 clean / 1 drift / 2 missing).

Pure + fixture-driven (no live-file mutation): CLI-path tests monkeypatch the module globals
`resolve_manifest_path` + `_TARGET` onto a tmp fixture, mirroring the toc/codemap test shape.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_methodology_roster as gmr  # noqa: E402

_FIXTURE_MANIFEST = """\
methodology_version: "9.9.9"
carriers:
  - id: dummy
    implemented: true
components:
  - id: cmd-a
    status: active
    roster:
      section: command
      line: "/alpha — does alpha"
  - id: hook-removed
    status: removed
    removed_in: "9.9.9"
    roster:
      section: precommit-hook
      line: "removed-hook — must not appear"
  - id: cfg-null
    status: active
    roster: null
  - id: active-no-roster
    status: active
  - id: hdr-a
    status: active
    roster:
      section: header
      line: "@.claude/CLAUDE-FLOOR.md — methodology floor"
  - id: sess-a
    status: active
    roster:
      section: session-hook
      line: "Stop: something happens"
"""


def _write_manifest(dir_path, name="manifest-v9.9.9.yaml", body=_FIXTURE_MANIFEST):
    p = dir_path / name
    p.write_text(body, encoding="utf-8")
    return p


# --- manifest resolution -------------------------------------------------------------------

def test_resolve_manifest_path_picks_max_semver(tmp_path):
    # 1.10.0 > 1.2.0 numerically (not lexically) — the semver-tuple sort must win.
    for v in ("1.0.0", "1.2.0", "1.10.0"):
        _write_manifest(tmp_path, f"manifest-v{v}.yaml")
    assert gmr.resolve_manifest_path(tmp_path).name == "manifest-v1.10.0.yaml"


def test_resolve_manifest_path_raises_when_none(tmp_path):
    import pytest
    with pytest.raises(RuntimeError):
        gmr.resolve_manifest_path(tmp_path)


# --- filtering -----------------------------------------------------------------------------

def test_collect_roster_filters_removed_null_and_missing(tmp_path):
    version, buckets = gmr.collect_roster(_write_manifest(tmp_path))
    assert version == "9.9.9"
    # active + roster present, grouped by section
    assert buckets["command"] == ["/alpha — does alpha"]
    assert buckets["session-hook"] == ["Stop: something happens"]
    assert buckets["header"] == ["@.claude/CLAUDE-FLOOR.md — methodology floor"]
    # removed tombstone, roster:null, and active-without-roster all excluded
    assert buckets["precommit-hook"] == []
    assert all("removed-hook" not in line for lines in buckets.values() for line in lines)


def test_unknown_roster_section_raises(tmp_path):
    import pytest
    body = _FIXTURE_MANIFEST.replace("section: command", "section: bogus-section")
    with pytest.raises(RuntimeError):
        gmr.collect_roster(_write_manifest(tmp_path, body=body))


def test_live_manifest_excludes_ruff_gate_and_includes_the_three_commands():
    # Read-only guard against the REAL current manifest: ruff-gate is status:removed (must be
    # absent) and the three deployed commands must render. No file is written.
    body = gmr.render(gmr.resolve_manifest_path())
    assert "ruff" not in body.lower() or "ruff-gate" not in body  # removed tombstone gone
    assert "/review-closures" in body
    assert "/ship" in body
    assert "/override" in body


# --- import neutralization -----------------------------------------------------------------

def test_neutralize_import_wraps_leading_at_only():
    # A leading bare @path is backtick-wrapped (inert to Claude Code's recursive @import parser)
    assert gmr._neutralize_import("@.claude/CLAUDE-FLOOR.md — floor") == \
        "`@.claude/CLAUDE-FLOOR.md` — floor"
    # A mid-line @ already inside a code span (the plugin line) is NOT touched
    line = "Plugin `tier1-lifecycle@dev-knowledge-methodology` enabled"
    assert gmr._neutralize_import(line) == line
    # A plain line is unchanged
    assert gmr._neutralize_import("/alpha — does alpha") == "/alpha — does alpha"


def test_rendered_floor_line_has_no_active_leading_import(tmp_path):
    body = gmr.render(_write_manifest(tmp_path))
    # No rendered bullet may begin with a bare @path (would dangle-import on the hub)
    for line in body.splitlines():
        if line.startswith("- "):
            assert not line[2:].startswith("@"), f"un-neutralized import bullet: {line!r}"


# --- determinism + section order -----------------------------------------------------------

def test_render_is_deterministic(tmp_path):
    mp = _write_manifest(tmp_path)
    assert gmr.render(mp) == gmr.render(mp)


def test_render_section_order_is_fixed(tmp_path):
    body = gmr.render(_write_manifest(tmp_path))
    positions = [body.find(f"## {gmr._SECTION_HEADINGS[s]}")
                 for s in ("header", "command", "session-hook")]
    assert positions == sorted(positions), "sections must render in _SECTION_ORDER"
    # empty sections (precommit-hook, skill) are omitted entirely
    assert gmr._SECTION_HEADINGS["skill"] not in body
    assert gmr._SECTION_HEADINGS["precommit-hook"] not in body


def test_generated_note_and_honest_header_present(tmp_path):
    body = gmr.render(_write_manifest(tmp_path))
    assert gmr._GENERATED_NOTE in body
    assert "DEPLOYABLE methodology corpus" in body  # LOCK-1 honesty framing
    assert "filesystem inventory" in body


# --- CLI exit-code contract (0 clean / 1 drift / 2 missing) --------------------------------

def _point_cli_at_fixture(monkeypatch, tmp_path):
    mp = _write_manifest(tmp_path)
    target = tmp_path / ".claude" / "methodology-roster.md"
    monkeypatch.setattr(gmr, "resolve_manifest_path", lambda *a, **k: mp)
    monkeypatch.setattr(gmr, "_TARGET", target)
    monkeypatch.setattr(gmr, "_REPO_ROOT", tmp_path)
    return target


def test_check_missing_target_returns_2(monkeypatch, tmp_path):
    _point_cli_at_fixture(monkeypatch, tmp_path)
    assert gmr.main(["--check"]) == 2


def test_write_then_check_is_clean(monkeypatch, tmp_path):
    target = _point_cli_at_fixture(monkeypatch, tmp_path)
    assert gmr.main(["--write"]) == 0
    assert target.exists()
    assert gmr.main(["--check"]) == 0  # regen-then-check: no drift (contract #1/#5)


def test_check_detects_injected_drift(monkeypatch, tmp_path):
    # The contract #5 demonstrated-catch: a hand-edit to the generated file is caught.
    target = _point_cli_at_fixture(monkeypatch, tmp_path)
    gmr.main(["--write"])
    target.write_text(target.read_text(encoding="utf-8") + "\n- hand-edited drift\n",
                      encoding="utf-8")
    assert gmr.main(["--check"]) == 1
