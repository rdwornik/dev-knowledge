"""Tests for the per-repo methodology-floor carrier (ADR-92 C4).

Covers the (three-state) reconcile model on the floor carrier
(deploy/carrier_floor.py) against the ADR-92 contract:

- absent floor: ABSENT -> apply -> verify passes (floor + sidecar written under the
  consumer's .claude/);
- drifted (floor edited / sidecar missing / sidecar stale): PRESENT_DRIFTED -> apply
  -> verify;
- idempotency: apply then apply again writes nothing (byte-identical);
- verify reports failures rather than silently passing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged;
- the carrier writes ONLY the consumer tree — apply() does NOT refresh the HUB's
  templates/child-methodology-floor.sha256 anchor (the differentiator from shelling
  out to generate_floor.py generate --out-dir).

The consumer is a temp dir; the floor is rendered from the real hub template. No
network, no real consumer repos, and the hub tree is left untouched.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_floor as cf  # noqa: E402
import contract  # noqa: E402

_FLOOR_TARGET = {
    "floor_path": ".claude/CLAUDE-FLOOR.md",
    "sidecar_path": ".claude/CLAUDE-FLOOR.md.sha256",
}

# Oracle: the corpus-state floor body + digest, computed independently of the
# carrier's own helper (straight from the hub generator's public functions).
_FLOOR_BODY = cf.gf.render_floor()
_FLOOR_DIGEST = cf.gf.floor_sha256(_FLOOR_BODY)


def _carrier(repo: Path) -> cf.FloorCarrier:
    return cf.FloorCarrier(repo)


def _floor_file(repo: Path) -> Path:
    return repo / ".claude" / "CLAUDE-FLOOR.md"


def _sidecar_file(repo: Path) -> Path:
    return repo / ".claude" / "CLAUDE-FLOOR.md.sha256"


def _hook_script(repo: Path) -> Path:
    return repo / ".claude" / "check_floor_hash.py"


def _claude_md(repo: Path) -> Path:
    return repo / "CLAUDE.md"


def _gitignore(repo: Path) -> Path:
    return repo / ".gitignore"


def _settings(repo: Path) -> Path:
    return repo / ".claude" / "settings.json"


# ---------------------------------------------------------------------------
# absent -> apply -> verify
# ---------------------------------------------------------------------------


def test_absent_detects_then_applies_and_verifies(tmp_path):
    car = _carrier(tmp_path)
    assert not _floor_file(tmp_path).exists()
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_FLOOR_TARGET)
    assert result.changed is True
    # armed set on a bare consumer: floor + sidecar + hook script + @-include +
    # .gitignore negation block + settings.json SessionStart hook (structured output).
    assert len(result.changes) == 6

    assert _floor_file(tmp_path).exists()
    assert _sidecar_file(tmp_path).exists()
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True


def test_apply_writes_floor_and_sidecar_matching_hub_render(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    # floor body is byte-for-byte the hub render (LF-normalized read to be autocrlf-proof)
    assert cf.gf.normalize(_floor_file(tmp_path).read_text(encoding="utf-8")) == _FLOOR_BODY
    # sidecar records the matching content-integrity digest
    assert cf._read_sidecar_hash(_sidecar_file(tmp_path)) == _FLOOR_DIGEST


def test_floor_written_under_consumer_claude_dir(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    assert (tmp_path / ".claude").is_dir()  # the consumer's own CC config dir, created


# ---------------------------------------------------------------------------
# drifted -> reconcile (three drift shapes)
# ---------------------------------------------------------------------------


def test_drifted_floor_edited_detects_then_reconciles(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    # tamper the floor body — content hash no longer matches the corpus digest.
    _floor_file(tmp_path).write_text(_FLOOR_BODY + "\nTAMPER\n", encoding="utf-8", newline="\n")
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_FLOOR_TARGET)
    assert result.changed is True
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True


def test_drifted_sidecar_missing_detects_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _sidecar_file(tmp_path).unlink()  # floor intact, sidecar gone
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_FLOOR_TARGET)
    assert car.verify(_FLOOR_TARGET).ok is True


def test_drifted_sidecar_stale_detects_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _sidecar_file(tmp_path).write_text("0" * 64 + "\n", encoding="utf-8", newline="\n")
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_FLOOR_TARGET)
    assert cf._read_sidecar_hash(_sidecar_file(tmp_path)) == _FLOOR_DIGEST  # re-pinned
    assert car.verify(_FLOOR_TARGET).ok is True


# ---------------------------------------------------------------------------
# idempotency — apply twice writes nothing the second time
# ---------------------------------------------------------------------------


def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    floor_before = _floor_file(tmp_path).read_bytes()
    sidecar_before = _sidecar_file(tmp_path).read_bytes()

    second = car.apply(_FLOOR_TARGET)
    assert second.changed is False
    assert second.changes == ()
    assert _floor_file(tmp_path).read_bytes() == floor_before
    assert _sidecar_file(tmp_path).read_bytes() == sidecar_before


# ---------------------------------------------------------------------------
# verify reports failures (not a silent pass)
# ---------------------------------------------------------------------------


def test_verify_on_absent_floor_is_not_ok(tmp_path):
    result = _carrier(tmp_path).verify(_FLOOR_TARGET)
    assert result.ok is False
    assert any("floor absent" in f for f in result.failures)


def test_verify_reports_floor_and_sidecar_failures(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _floor_file(tmp_path).write_text(_FLOOR_BODY + "\nTAMPER\n", encoding="utf-8", newline="\n")
    _sidecar_file(tmp_path).unlink()
    failures = car.verify(_FLOOR_TARGET).failures
    assert any("floor content hash" in f for f in failures)
    assert any("sidecar absent" in f for f in failures)


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_floor); verify must still pass."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_floor (D9)")

    monkeypatch.setattr(cf, "_classify_floor", _boom)
    assert car.verify(_FLOOR_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_floor); detect must still classify."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_floor (D9)")

    monkeypatch.setattr(cf, "_verify_floor", _boom)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# consumer-scoped — apply() never mutates the HUB canonical SHA anchor
# ---------------------------------------------------------------------------


def test_apply_does_not_refresh_hub_canonical_sha(tmp_path):
    # The differentiator from `generate_floor.py generate --out-dir` (which refreshes
    # the hub anchor as a side-effect): this carrier writes ONLY the consumer tree.
    hub_anchor = cf.gf.HUB_CANONICAL_SHA
    assert hub_anchor.exists()
    before = hub_anchor.read_bytes()

    _carrier(tmp_path).apply(_FLOOR_TARGET)

    assert hub_anchor.read_bytes() == before  # hub anchor untouched


# ---------------------------------------------------------------------------
# ARMING (ADR-93) — apply does not merely drop content; it arms the floor so a
# fresh clone self-arms. Six artifacts; PRESENT_CORRECT requires ALL.
# ---------------------------------------------------------------------------


def test_apply_writes_canonical_guard_script(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    # The one canonical guard both legs run, single-sourced from the hub generator.
    assert _hook_script(tmp_path).exists()
    assert (
        _hook_script(tmp_path).read_text(encoding="utf-8")
        == cf.gf.CHECK_FLOOR_HASH_SCRIPT
    )


def test_apply_adds_at_include_to_claude_md(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    assert cf.INCLUDE_LINE in _claude_md(tmp_path).read_text(encoding="utf-8")


def test_apply_inserts_include_after_frontmatter_preserving_content(tmp_path):
    existing = "---\nlast_reviewed: 2026-06-02\n---\n\n# CLAUDE.md — Consumer\nBody.\n"
    _claude_md(tmp_path).write_text(existing, encoding="utf-8", newline="\n")
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    text = _claude_md(tmp_path).read_text(encoding="utf-8")
    assert cf.INCLUDE_LINE in text
    assert "# CLAUDE.md — Consumer" in text and "Body." in text  # content preserved
    # include sits after the frontmatter close, before the H1
    assert text.index(cf.INCLUDE_LINE) > text.index("last_reviewed")
    assert text.index(cf.INCLUDE_LINE) < text.index("# CLAUDE.md — Consumer")


def test_apply_rewrites_bare_claude_gitignore_to_contents_form(tmp_path):
    _gitignore(tmp_path).write_text("# Claude\n.claude/\n", encoding="utf-8", newline="\n")
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    lines = [ln.strip() for ln in _gitignore(tmp_path).read_text(encoding="utf-8").splitlines()]
    assert ".claude/" not in lines  # bare dir form replaced (defeats negations, #138)
    assert ".claude/*" in lines
    for neg in ("!.claude/CLAUDE-FLOOR.md", "!.claude/CLAUDE-FLOOR.md.sha256",
                "!.claude/check_floor_hash.py"):
        assert neg in lines


def test_apply_adds_sessionstart_guard_with_both_legs(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    cmds = [
        h["command"]
        for g in data["hooks"]["SessionStart"]
        for h in g["hooks"]
    ]
    # verify leg runs --require-present so a deleted-but-tracked floor fails loud (ADR-93)
    assert any("check_floor_hash.py --require-present" in c for c in cmds)
    assert any("pre_commit install" in c for c in cmds)           # bootstrap arm leg


def test_apply_arms_all_three_hook_stages(tmp_path):
    """#275b: the SessionStart arm command the carrier writes arms ALL THREE hook stages
    (pre-commit / commit-msg / pre-push), not just pre-commit — else commit-msg / pre-push
    stage hooks land wired-but-dormant on a fresh consumer."""
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    cmds = [h["command"] for g in data["hooks"]["SessionStart"] for h in g["hooks"]]
    arm = next(c for c in cmds if "pre_commit install" in c)
    for tok in ("-t pre-commit", "-t commit-msg", "-t pre-push"):
        assert tok in arm, f"arm cmd missing {tok!r} (#275b): {arm!r}"


def test_apply_merges_sessionstart_preserving_existing_settings(tmp_path):
    existing = {"enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": True}}
    _settings(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    _settings(tmp_path).write_text(json.dumps(existing), encoding="utf-8", newline="\n")
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert data["enabledPlugins"] == existing["enabledPlugins"]  # preserved
    assert data["hooks"]["SessionStart"]                          # guard added


@pytest.mark.parametrize("break_it", [
    lambda repo: _claude_md(repo).write_text("# no include\n", encoding="utf-8", newline="\n"),
    lambda repo: _hook_script(repo).write_text("print('tampered')\n", encoding="utf-8", newline="\n"),
    lambda repo: _gitignore(repo).write_text(".claude/\n", encoding="utf-8", newline="\n"),
    lambda repo: _settings(repo).write_text("{}", encoding="utf-8", newline="\n"),
])
def test_missing_arming_artifact_detects_drifted_then_reconciles(tmp_path, break_it):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    break_it(tmp_path)  # floor+sidecar intact, but one arming artifact broken
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    assert car.verify(_FLOOR_TARGET).ok is False

    car.apply(_FLOOR_TARGET)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True
