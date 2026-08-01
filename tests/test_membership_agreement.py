"""Tests for check_membership_agreement ([#462] clause 1 / [#383] wave 2).

The defect this organ exists for: the [#382] census censused `ecosystem/registry.md` ITSELF,
so a fleet member absent FROM that registry was invisible by construction. `terminal-setup`
sat declared in ADR-104 and VISION and present in zero machine surfaces for months, found
only because three nightly digests each re-noticed it by hand.

Firing tests: an undeclared member in ANY surface REDs and names both the repo and the
surface (the AC-4' perturbation, pinned permanently); a declared repo absent from the
deployed-versions anchor is reported as data at PASS, never WARN (an undispositioned WARN
REDs the ship-gate, and ADR-109 §2 rules the disagreement is "carried as model data, never a
load error"); a repo carried by NO surface at all is still named rather than silently
dropped; and the leg is hub-only by REPO IDENTITY so it cannot manufacture a consumer gap.

Plus the contract a constant-shaped declaration must not quietly lose: the inline registry
reader agrees with `desired_state_loader.parse_registry_md` on the live file, so the two
parsers cannot drift into disagreeing about who is registered.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as aud

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# --- the pure classifier ----------------------------------------------------

DECL = (".dev-knowledge", "ai-council", "corp-ops", "terminal-setup")


def _surfaces(**kw) -> dict[str, set[str]]:
    """Ordered surface map; every key defaults to empty so a test names only what it means."""
    base = {"registry-md": set(), "index-yaml": set(), "deployed-versions": set(),
            "parity-surfaces": set(), "onboarding-rulings": set(), "state-dirs": set()}
    base.update({k.replace("_", "-"): set(v) for k, v in kw.items()})
    return base


def test_undeclared_member_in_a_surface_reds_and_names_repo_and_surface():
    """AC-4': perturb one surface's membership -> the check names the repo AND the surface.

    This is the strong invariant. A repo the machine carries but the fleet never declared is
    a real divergence: either ADR-104 is stale or the surface is wrong, and both need a human.
    """
    out = aud.classify_membership(DECL, _surfaces(parity_surfaces=["ghost-repo"]))
    fails = [(s, e) for s, e in out if s == "fail"]
    assert len(fails) == 1
    assert "ghost-repo" in fails[0][1]
    assert "parity-surfaces" in fails[0][1]


def test_undeclared_members_are_reported_per_repo_per_surface():
    """One finding per (repo, surface) pair -- a single merged line hides which surface."""
    out = aud.classify_membership(
        DECL, _surfaces(registry_md=["ghost-a"], index_yaml=["ghost-a", "ghost-b"]))
    fails = [e for s, e in out if s == "fail"]
    assert len(fails) == 3
    assert sum("registry-md" in e for e in fails) == 1
    assert sum("index-yaml" in e for e in fails) == 2


def test_declared_but_not_deployed_is_pass_not_warn():
    """Ruled: declared-but-not-deployed is a PASS-state (ADR-109 §2/§8 -- surfaced, not fixed).

    Not WARN: an undispositioned WARN REDs the ship-gate, which would train the operator to
    disposition the organ -- the exact way a 46-day FAIL came to be ignored ([#460]).
    """
    out = aud.classify_membership(
        DECL, _surfaces(registry_md=DECL, deployed_versions=[".dev-knowledge", "ai-council"]))
    assert [s for s, _ in out] == ["pass"]
    evidence = out[0][1]
    assert "corp-ops" in evidence and "terminal-setup" in evidence


def test_a_repo_carried_by_no_surface_is_named_not_dropped():
    """The [#462] blind spot itself: absent everywhere must be LOUDER than absent from one."""
    out = aud.classify_membership(DECL, _surfaces(registry_md=[".dev-knowledge"],
                                                  deployed_versions=[".dev-knowledge"]))
    evidence = out[0][1]
    assert "terminal-setup [NO SURFACE]" in evidence


def test_fully_covered_declaration_reports_none_undeployed():
    out = aud.classify_membership(DECL, _surfaces(registry_md=DECL, deployed_versions=DECL))
    assert [s for s, _ in out] == ["pass"]
    assert "declared-but-not-deployed: none" in out[0][1]


def test_classifier_evidence_is_ascii_and_pipe_free():
    """cp1252 console discipline ([#470]) + markdown-table safety (the Finding contract)."""
    out = aud.classify_membership(DECL, _surfaces(registry_md=DECL, index_yaml=["ghost"]))
    for _, evidence in out:
        evidence.encode("ascii")
        assert "|" not in evidence


# --- the wrapper ------------------------------------------------------------


def test_leg_is_hub_only_and_na_off_hub(tmp_path):
    """Guard on REPO IDENTITY, never on artifact presence.

    Keying "adopted" off an `ecosystem/` folder would report FAIL on consumer repos that
    carry no hub registries -- a manufactured fleet gap (the
    enforcement-organs-are-not-homogeneous class, [#383] wave 1).
    """
    (tmp_path / "ecosystem").mkdir()
    finding = aud.check_membership_agreement(tmp_path)[0]
    assert finding.status == "n/a"


@pytest.mark.live_repo
def test_leg_passes_on_the_live_hub():
    findings = aud.check_membership_agreement(Path(aud._REPO_ROOT))
    assert [f.status for f in findings] == ["pass"], [f.evidence for f in findings]


@pytest.mark.live_repo
def test_live_hub_declaration_is_the_nine_of_adr_104():
    """9 governs (architect ruling 2026-08-01). The `5` seen elsewhere is a loader artifact
    of `resolve_fleet_members` keying on deployed-versions.yaml, not a ruled tree count --
    ADR-104 explicitly declined to rule which repos consolidate."""
    assert len(aud.ADR104_FLEET_DECLARATION) == 9
    assert "terminal-setup" in aud.ADR104_FLEET_DECLARATION


@pytest.mark.live_repo
def test_a_missing_surface_file_fails_rather_than_passes():
    """A coherence gate must not be satisfiable by deleting what it checks (terra ruling,
    carried by both tree-coherence gates)."""
    findings = aud.check_membership_agreement(
        Path(aud._REPO_ROOT), _surface_paths=(("registry-md", "ecosystem/does-not-exist.md"),))
    assert findings[0].status == "fail"
    assert "does-not-exist" in findings[0].evidence


@pytest.mark.live_repo
def test_state_dirs_are_read_from_repo_path_not_the_module_global(monkeypatch, tmp_path):
    """Every surface must be read from repo_path -- all six, not five.

    Regression: the first draft reused `discover_repos()`, which reads the module-global
    ECOSYSTEM_DIR. That made the state-dirs surface report a DIFFERENT repo than the other
    five whenever the two disagree, so a stray dir elsewhere REDs a check aimed here. Caught
    by test_health_ok_with_registered_repo, which monkeypatches exactly that global.
    """
    stray = tmp_path / "ecosystem" / "not-a-fleet-repo"
    stray.mkdir(parents=True)
    (stray / "state.yaml").write_text("name: not-a-fleet-repo\n", encoding="utf-8")
    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path / "ecosystem")

    findings = aud.check_membership_agreement(Path(aud._REPO_ROOT))
    assert [f.status for f in findings] == ["pass"], [f.evidence for f in findings]
    assert "not-a-fleet-repo" not in findings[0].evidence


def test_check_is_registered_as_a_ship_gate_leg():
    assert aud.check_membership_agreement in aud.ALL_CHECKS


@pytest.mark.live_repo
def test_inline_registry_reader_agrees_with_the_loader_parser():
    """The declaration is a constant, so the registry READER is the one place this check and
    `desired_state_loader` could silently disagree about who is registered. Pinned, because
    the reuse cost is paid here rather than by importing pydantic onto the pre-commit path."""
    dsl = _load("desired_state_loader")
    registry = Path(aud._REPO_ROOT) / "ecosystem" / "registry.md"
    loader_ids = set(dsl.parse_registry_md(registry.read_text(encoding="utf-8")))
    assert aud._read_registry_members(registry) == loader_ids
