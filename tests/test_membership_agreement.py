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
    """Every finding is a pass on the live hub — the census verdict AND, since [#472], the
    declaration-agreement leg. Asserted as "all pass" rather than "exactly one finding": the
    old form pinned the check's finding COUNT, which is incidental structure, so adding a
    legitimate second verdict read as a regression."""
    findings = aud.check_membership_agreement(Path(aud._REPO_ROOT))
    assert findings, "no findings at all"
    assert all(f.status == "pass" for f in findings), [f.evidence for f in findings]
    assert any("declaration source" in f.evidence for f in findings), \
        "the [#472] declaration-agreement leg did not run on the live hub"


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
    # "all pass", not "exactly one finding" — the count is incidental structure, and since
    # [#472] a second (declaration-agreement) verdict is legitimately present.
    assert all(f.status == "pass" for f in findings), [f.evidence for f in findings]
    assert not any("not-a-fleet-repo" in f.evidence for f in findings)


@pytest.mark.live_repo
def test_unreadable_state_dir_scan_fails_rather_than_raising(monkeypatch):
    """terra HIGH 2026-08-01: an unguarded iterdir() aborts the whole `audit.py health` run.

    Failing this check is the contract; taking down every OTHER check's verdict with it is
    not -- so the state-dirs read is guarded exactly like the five file surfaces.
    """
    real_iterdir = Path.iterdir

    def _boom(self):
        if self.name == "ecosystem":
            raise PermissionError(13, "Permission denied")
        return real_iterdir(self)

    monkeypatch.setattr(Path, "iterdir", _boom)
    findings = aud.check_membership_agreement(Path(aud._REPO_ROOT))
    assert findings[0].status == "fail"
    assert "ecosystem/<repo>/" in findings[0].evidence


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


# ---------------------------------------------------------------------------
# [#472] — the declaration-agreement leg. ADR-104's anchored block is the SOURCE;
# ADR104_FLEET_DECLARATION is the mirror the leg checks. Both directions pinned.
# ---------------------------------------------------------------------------

_ADR_REL = "docs/decisions/ADR-104-fleet-repository-shape.md"
_ANCHOR_ID = "adr104-fleet-members"


def _adr_with(ids, *, start=True, end=True, duplicate=False) -> str:
    """A minimal ADR-104 stand-in carrying the anchored declaration block."""
    block = "\n".join(ids)
    s = f"<!-- declaration:start id={_ANCHOR_ID} v=1 -->"
    e = f"<!-- declaration:end id={_ANCHOR_ID} -->"
    body = "# ADR-104 (fixture)\n\nprose above\n\n"
    if start:
        body += f"{s}\n"
    body += f"```\n{block}\n```\n"
    if end:
        body += f"{e}\n"
    if duplicate:
        body += f"\n{s}\n```\n{block}\n```\n{e}\n"
    return body + "\nprose below\n"


def _hub_tree(tmp_path: Path, adr_text: str) -> Path:
    """A tmp tree `_is_hub` accepts, carrying only what the declaration leg reads.

    The surfaces are deliberately absent: the leg is attached BEFORE the surfaces loop, so a
    declaration/constant disagreement must still be reported when a later surface read fails.
    That ordering is part of the contract, not an accident of the fixture.
    """
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    (tmp_path / _ADR_REL).write_text(adr_text, encoding="utf-8", newline="\n")
    # `_is_hub` keys on repo identity; give the tree the hub's marker files.
    (tmp_path / "CLAUDE.md").write_text("# CLAUDE.md\n", encoding="utf-8")
    (tmp_path / "protocols").mkdir(exist_ok=True)
    return tmp_path


def _decl_findings(repo: Path) -> list:
    return [f for f in aud.check_membership_agreement(repo)
            if "declaration" in f.evidence.lower()]


def test_declaration_leg_passes_when_the_adr_matches_the_constant(tmp_path, monkeypatch):
    """Baseline: the anchored block and the module constant agree -> a pass leg is emitted."""
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, _adr_with(aud.ADR104_FLEET_DECLARATION))
    out = _decl_findings(repo)
    assert out, "no declaration leg was emitted at all"
    assert all(f.status != "fail" for f in out), [f.evidence for f in out]


def test_declaration_leg_catches_an_id_MISSING_from_the_adr(tmp_path, monkeypatch):
    """Direction 1 — the ADR is stale. Someone edits the constant and not the amendment."""
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    short = tuple(r for r in aud.ADR104_FLEET_DECLARATION if r != "win-tooling")
    repo = _hub_tree(tmp_path, _adr_with(short))
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "a constant carrying an id the ADR lacks did not FAIL"
    assert "win-tooling" in fails[0].evidence
    assert "constant only" in fails[0].evidence.lower()


def test_declaration_leg_catches_an_id_ADDED_to_the_adr(tmp_path, monkeypatch):
    """Direction 2 — the constant is stale. Someone amends the ADR and not the code.

    Both directions are asserted separately and BY NAME: a leg that only caught one would be
    green for exactly the half of the drift nobody happened to test.
    """
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    longer = (*aud.ADR104_FLEET_DECLARATION, "new-repo")
    repo = _hub_tree(tmp_path, _adr_with(longer))
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "an ADR carrying an id the constant lacks did not FAIL"
    assert "new-repo" in fails[0].evidence
    assert "amendment only" in fails[0].evidence.lower()


def test_declaration_leg_catches_a_duplicated_id(tmp_path, monkeypatch):
    """Set equality alone would miss this: the ids must agree in COUNT as well as membership."""
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    dupe = (*aud.ADR104_FLEET_DECLARATION, "win-tooling")
    repo = _hub_tree(tmp_path, _adr_with(dupe))
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "a duplicated id inside the anchor did not FAIL"


def test_declaration_leg_fails_when_the_anchor_is_deleted(tmp_path, monkeypatch):
    """A gate satisfiable by deleting what it checks is not a gate -- the check's own rule."""
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, "# ADR-104 (fixture)\n\nno anchor here\n")
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "a missing anchor did not FAIL"
    assert "not found" in fails[0].evidence.lower()


def test_declaration_leg_fails_on_a_duplicated_anchor(tmp_path, monkeypatch):
    """Two blocks means two answers; exactly one is required."""
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, _adr_with(aud.ADR104_FLEET_DECLARATION, duplicate=True))
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "a duplicated anchor did not FAIL"
    assert "2 times" in fails[0].evidence or "appears" in fails[0].evidence


def test_declaration_leg_fails_on_an_unterminated_pair(tmp_path, monkeypatch):
    """A start with no end: the block has no boundary, so its content is undefined."""
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, _adr_with(aud.ADR104_FLEET_DECLARATION, end=False))
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "an unterminated anchor pair did not FAIL"
    assert "end marker" in fails[0].evidence.lower()


def test_declaration_leg_is_hub_only(tmp_path):
    """A consumer has no ADR-104; it must report n/a, never FAIL (the not-homogeneous rule)."""
    out = aud.check_membership_agreement(tmp_path)
    assert [f.status for f in out] == ["n/a"], [f.evidence for f in out]


@pytest.mark.live_repo
def test_live_hub_adr_anchor_agrees_with_the_constant():
    """The lockstep, on the real files: ADR-104's anchored block == ADR104_FLEET_DECLARATION."""
    root = Path(__file__).resolve().parent.parent
    ids = aud.read_adr104_declaration(root / _ADR_REL)
    assert tuple(ids) == tuple(aud.ADR104_FLEET_DECLARATION), (ids, aud.ADR104_FLEET_DECLARATION)
    assert len(ids) == 9


def test_declaration_anchor_rejects_a_PREFIX_id(tmp_path, monkeypatch):
    """terra HIGH 2026-08-04: `\b` after the id is not an id boundary.

    `-` is a NON-word character, so `id=adr104-fleet-members-v2` satisfied `\b` and matched
    this anchor -- a differently-versioned block would have been read as if it were this one,
    silently, and could even PASS if its contents happened to match the constant.
    """
    body = ("# ADR-104 (fixture)\n\n"
            "<!-- declaration:start id=adr104-fleet-members-v2 v=1 -->\n"
            "```\nghost-repo\n```\n"
            "<!-- declaration:end id=adr104-fleet-members-v2 -->\n")
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, body)
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "a -v2 anchor was accepted as this declaration"
    assert "not found" in fails[0].evidence.lower(), fails[0].evidence


def test_declaration_anchor_ignores_a_marker_shown_inside_a_code_fence(tmp_path, monkeypatch):
    """A marker demonstrated as an EXAMPLE is documentation, not the declaration.

    The dangerous shape is not two anchors (that FAILs loudly as a duplicate) but the real
    anchor ABSENT while a fenced example is present: the parser would then read the example
    and report agreement or a wrong id list instead of 'anchor not found'.
    """
    body = ("# ADR-104 (fixture)\n\nHow to write the anchor:\n\n"
            "```\n"
            f"<!-- declaration:start id={_ANCHOR_ID} v=1 -->\n"
            "example-repo\n"
            f"<!-- declaration:end id={_ANCHOR_ID} -->\n"
            "```\n\nthe real anchor was deleted\n")
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, body)
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails, "a fenced EXAMPLE marker was read as the real declaration"
    assert "not found" in fails[0].evidence.lower(), fails[0].evidence


def test_declaration_anchor_ignores_a_marker_mentioned_mid_sentence(tmp_path, monkeypatch):
    """Markers must own their line; prose quoting one inline is not an anchor."""
    body = ("# ADR-104 (fixture)\n\n"
            f"The anchor is written <!-- declaration:start id={_ANCHOR_ID} v=1 --> inline here.\n")
    monkeypatch.setattr(aud, "_is_hub", lambda _p: True)
    repo = _hub_tree(tmp_path, body)
    fails = [f for f in _decl_findings(repo) if f.status == "fail"]
    assert fails and "not found" in fails[0].evidence.lower(), [f.evidence for f in fails]


@pytest.mark.live_repo
def test_declaration_leg_works_under_package_mode_invocation():
    """`python -m scripts.audit health` must reach the declaration leg (terra HIGH round 2).

    Script mode puts scripts/ on sys.path; PACKAGE mode puts the repo root there. The bare
    `from toc.generator import ...` resolved in package mode only because another imported
    script inserts scripts/ as a SIDE EFFECT — incidental, not a contract, so a future import
    reshuffle could turn this hub check into a ModuleNotFoundError mid-run. Exercised as a real
    subprocess rather than by reasoning about sys.path.
    """
    import subprocess

    root = Path(aud._REPO_ROOT)
    r = subprocess.run([sys.executable, "-m", "scripts.audit", "health"],
                       cwd=str(root), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    assert "ModuleNotFoundError" not in (r.stdout + r.stderr), (r.stdout + r.stderr)[-400:]
    assert "declaration source" in r.stdout, r.stdout[-400:]
