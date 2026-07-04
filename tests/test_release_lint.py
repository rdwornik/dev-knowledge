"""release-lint teeth (P1) — green on the live consistent state, FAIL on every
injected anchor/schema mismatch class (demonstrated, not asserted).

Each teeth test copies the REAL hub state (manifest + plugin.json + floor
template/sidecar) into a tmp root, injects exactly one inconsistency, and
requires the lint to FAIL naming that check. The pass-case fixture is derived
from the real manifest, so it stays realistic by construction. The git-tag
probe is injected — no test depends on real tags.
"""
from __future__ import annotations

import copy
import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import release_lint as rl  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[1]
_TAG_OK = lambda tag, root: True  # noqa: E731 — injected probe: tag always resolves


def _fails(findings):
    return [f for f in findings if f.status == "fail"]


def _checks_failing(findings):
    return {f.check for f in _fails(findings)}


# ---------------------------------------------------------------------------
# Tmp-root builder — real hub state, one injected mutation.
# ---------------------------------------------------------------------------


def make_root(tmp_path: Path, mutate=None) -> Path:
    root = tmp_path / "hub"
    (root / "deploy").mkdir(parents=True)
    spec = yaml.safe_load(
        (_REPO_ROOT / "deploy" / "manifest-v1.1.0.yaml").read_text(encoding="utf-8"))
    if mutate is not None:
        mutate(spec)
    (root / "deploy" / "manifest-v1.1.0.yaml").write_text(
        yaml.safe_dump(spec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    for rel in (rl.PLUGIN_JSON_REL, rl.FLOOR_TMPL_REL, rl.FLOOR_SIDECAR_REL):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(_REPO_ROOT / rel, dst)
    return root


# ---------------------------------------------------------------------------
# Green paths.
# ---------------------------------------------------------------------------


def test_live_hub_state_is_green():
    """The real repo passes — keeps every anchor honest from now on."""
    findings = rl.lint(_REPO_ROOT, "1.1.0", tag_probe=_TAG_OK)
    assert _fails(findings) == [], [f.evidence for f in _fails(findings)]


def test_unmutated_copy_is_green(tmp_path):
    """The tmp-root builder itself introduces no failure (teeth aren't vacuous)."""
    root = make_root(tmp_path)
    findings = rl.lint(root, "v1.1.0", tag_probe=_TAG_OK)
    assert _fails(findings) == [], [f.evidence for f in _fails(findings)]


def test_live_v120_state_is_green():
    """The real v1.2.0 manifest (ruff-gate tombstone) passes -- keeps P2 honest."""
    findings = rl.lint(_REPO_ROOT, "1.2.0", tag_probe=_TAG_OK)
    assert _fails(findings) == [], [f.evidence for f in _fails(findings)]


# ---------------------------------------------------------------------------
# P2 tombstone teeth (C6 removed_in coherence) — direct check_components calls
# against the real v1.2.0 spec, one injected mutation each.
# ---------------------------------------------------------------------------

_V120_SPEC = yaml.safe_load(
    (_REPO_ROOT / "deploy" / "manifest-v1.2.0.yaml").read_text(encoding="utf-8"))


def _v120_components(mutate=None):
    spec = copy.deepcopy(_V120_SPEC)
    if mutate is not None:
        mutate(spec)
    return rl.check_components(spec)


def test_c6_valid_tombstone_passes():
    """ruff-gate removed WITH removed_in -> C6 green (the shipped shape)."""
    assert not _fails(_v120_components())


def test_c6_removed_without_removed_in_fails():
    def mut(s):
        next(c for c in s["components"] if c["id"] == "ruff-gate").pop("removed_in")
    findings = _v120_components(mut)
    assert "C6-components" in _checks_failing(findings)
    assert any("removed_in" in f.evidence for f in _fails(findings))


def test_c6_active_with_removed_in_fails():
    def mut(s):
        next(c for c in s["components"] if c["status"] == "active")["removed_in"] = "1.2.0"
    findings = _v120_components(mut)
    assert "C6-components" in _checks_failing(findings)
    assert any("removed_in" in f.evidence for f in _fails(findings))


def test_c6_deprecated_status_still_rejected():
    """2-state lifecycle (D3): `deprecated` is never legal, even post-P2."""
    def mut(s):
        next(c for c in s["components"] if c["status"] == "active")["status"] = "deprecated"
    assert "C6-components" in _checks_failing(_v120_components(mut))


def test_c6_waivable_non_bool_fails():
    """waivable must be a bool -> a string value FAILs C6 ([#244] P4)."""
    def mut(s):
        next(c for c in s["components"] if c["status"] == "active")["waivable"] = "yes"
    findings = _v120_components(mut)
    assert "C6-components" in _checks_failing(findings)
    assert any("waivable" in f.evidence for f in _fails(findings))


def test_c6_missing_waivable_on_active_fails():
    """Once the manifest declares waivable, every status:active component must carry it."""
    def mut(s):
        next(c for c in s["components"] if c["status"] == "active").pop("waivable")
    findings = _v120_components(mut)
    assert "C6-components" in _checks_failing(findings)
    assert any("waivable" in f.evidence for f in _fails(findings))


def test_load_bearing_components_non_waivable():
    """The FULL non-waivable floor set is locked false on the real v1.2.0 manifest
    ([#244] P4 contract 2 — load-bearing / fail-closed, NOT derived from verify type)."""
    non_waivable = {c["id"] for c in _V120_SPEC["components"] if c.get("waivable") is False}
    assert non_waivable == {
        "session-end-backpressure",
        "canonical-freshness",
        "methodology-floor",
        "floor-hash-verify-hook",
        "floor-sessionstart-guard",
    }


def test_missing_tag_is_warn_not_fail(tmp_path):
    """Pre-tag authoring state: WARN (operator tags at release), never FAIL."""
    root = make_root(tmp_path)
    findings = rl.lint(root, "1.1.0", tag_probe=lambda t, r: False)
    assert _fails(findings) == []
    assert any(f.check == "C2-tag" and f.status == "warn" for f in findings)


# ---------------------------------------------------------------------------
# Teeth — one injected inconsistency per anchor/schema class -> FAIL.
# ---------------------------------------------------------------------------


def _set_hub_hooks_rev(spec, rev):
    for c in spec["carriers"]:
        if c["id"] == "precommit":
            c["target"]["hub_hooks"]["rev"] = rev


def _first_component(spec):
    return spec["components"][0]


@pytest.mark.parametrize(
    ("mutate", "expect_check"),
    [
        pytest.param(lambda s: s.update(methodology_version="9.9.9"),
                     "C1-spec", id="version-vs-filename"),
        pytest.param(lambda s: s.update(source_tag="v9.9.9"),
                     "C1-spec", id="tag-vs-version"),
        pytest.param(lambda s: _set_hub_hooks_rev(s, "v9.9.9"),
                     "C3-hub-hooks-rev", id="hub-hooks-rev-drift"),
        pytest.param(lambda s: s["anchors"].update(plugin_version="0.0.1"),
                     "C4-plugin-pin", id="plugin-pin-drift"),
        pytest.param(lambda s: s["anchors"].pop("plugin_version"),
                     "C4-plugin-pin", id="plugin-pin-missing"),
        pytest.param(lambda s: s["anchors"].update(floor_sha256="deadbeef" * 8),
                     "C5-floor-pin", id="floor-pin-drift"),
        pytest.param(lambda s: _first_component(s).update(status="removed"),
                     "C6-components", id="tombstone-before-P2"),
        pytest.param(lambda s: _first_component(s).update(status="deprecated"),
                     "C6-components", id="deprecated-before-P2"),
        pytest.param(lambda s: _first_component(s).update(carrier="no-such-carrier"),
                     "C6-components", id="unresolved-carrier-ref"),
        pytest.param(lambda s: _first_component(s).update(kind="banana"),
                     "C6-components", id="unknown-kind"),
        pytest.param(lambda s: _first_component(s).update(verify="vibes"),
                     "C6-components", id="unknown-verify-class"),
        pytest.param(lambda s: s["components"].append(dict(_first_component(s))),
                     "C6-components", id="duplicate-component-id"),
        pytest.param(lambda s: s.update(
            components=[c for c in s["components"] if c["carrier"] != "floor"]),
                     "C6-components", id="implemented-carrier-uncovered"),
        pytest.param(lambda s: s.pop("components"),
                     "C6-components", id="components-section-missing"),
        pytest.param(lambda s: s["doc_shapes"]["CLAUDE.md"].update(
            spine=["## Not the real spine"]),
                     "C7-doc-shapes", id="doc-shape-spine-drift"),
        pytest.param(lambda s: s["doc_shapes"]["VISION.md"].update(freshness_gated=False),
                     "C7-doc-shapes", id="freshness-gated-set-drift"),
        pytest.param(lambda s: s.pop("doc_shapes"),
                     "C7-doc-shapes", id="doc-shapes-section-missing"),
    ],
)
def test_injected_mismatch_fails_the_named_check(tmp_path, mutate, expect_check):
    root = make_root(tmp_path, mutate=mutate)
    findings = rl.lint(root, "1.1.0", tag_probe=_TAG_OK)
    assert expect_check in _checks_failing(findings), (
        f"expected {expect_check} to FAIL; failing: "
        f"{[(f.check, f.evidence) for f in _fails(findings)]}")
    assert rl.has_fail(findings)


def test_stale_floor_sidecar_fails(tmp_path):
    """Sidecar != recomputed template bytes (the floor-drift class) -> C5 FAIL."""
    root = make_root(tmp_path)
    tmpl = root / rl.FLOOR_TMPL_REL
    tmpl.write_bytes(tmpl.read_bytes() + b"\n# drifted floor content\n")
    findings = rl.lint(root, "1.1.0", tag_probe=_TAG_OK)
    assert "C5-floor-pin" in _checks_failing(findings)


def test_missing_manifest_fails(tmp_path):
    root = make_root(tmp_path)
    findings = rl.lint(root, "3.3.3", tag_probe=_TAG_OK)
    assert "C1-spec" in _checks_failing(findings)


# ---------------------------------------------------------------------------
# CLI exit codes.
# ---------------------------------------------------------------------------


# The tmp root is not a git repo, so the real tag probe reports the tag
# unresolved -> C2 WARN, which must not affect the exit code either way.


def test_cli_green_exit_0(monkeypatch, tmp_path):
    root = make_root(tmp_path)
    monkeypatch.setattr(rl, "_HUB_ROOT", root)
    result = CliRunner().invoke(rl.main, ["--version", "v1.1.0"])
    assert result.exit_code == 0, result.output
    assert "0 FAIL" in result.output


def test_cli_fail_exit_1(monkeypatch, tmp_path):
    root = make_root(tmp_path, mutate=lambda s: _set_hub_hooks_rev(s, "v9.9.9"))
    monkeypatch.setattr(rl, "_HUB_ROOT", root)
    result = CliRunner().invoke(rl.main, ["--version", "v1.1.0"])
    assert result.exit_code == 1
    assert "C3-hub-hooks-rev" in result.output
