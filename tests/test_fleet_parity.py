"""Hermetic tests for scripts/fleet_parity.py -- the #328 checker.

Every fixture is a THROWAWAY temp git repo (the test_enforcement_coverage idiom);
manifests/baselines/registries are tmp files. Zero network, zero clones, zero writes
to any real repo. The ruled pack's ex-ante acceptance criteria are pinned here:

  AC-1  undeclared divergence -> exactly one WARN naming repo+surface; declaring it
        flips PASS-declared with no code change
  AC-2  missing pinned dep (pytest-xdist) -> WARN with expected-vs-actual; at-parity
        and declared consumers -> no WARN                                (#332)
  AC-5  d1 identity: one canonical id, three local names, corp skip-set reads as a
        declared divergence, zero byte-diff noise
  AC-6  tombstone teeth: undeclared re-add of status:removed WARNs; a mis-addressed /
        ambiguous component pointer REFUSES, never proposes an action
  AC-9  one declaration cannot suppress two concerns; bare-id/substring match is
        rejected; an orphaned declaration surfaces stale
  S4    effect-probe teeth: a .gitignore pattern textually present but semantically
        inert (inline comment) is caught by git check-ignore, where a text grep
        would false-pass
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import fleet_parity as fp  # noqa: E402


# ---------------------------------------------------------------------------
# Fixture helpers (hermetic temp git repos -- the _init_consumer idiom).
# ---------------------------------------------------------------------------


def _git(args, cwd):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _init_repo(root: Path, files: dict[str, str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    r = _git(["init", "-q", "-b", "main"], root)
    if r.returncode != 0:
        _git(["init", "-q"], root)
    for cfg in (["core.autocrlf", "false"], ["user.email", "fp@example.com"],
                ["user.name", "Fleet Parity Test"], ["commit.gpgsign", "false"]):
        _git(["config", *cfg], root)
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8", newline="\n")
    _git(["add", "-A"], root)
    _git(["commit", "-q", "-m", "init"], root)
    return root


def _write_yaml(path: Path, data: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8",
                    newline="\n")
    return path


# ADR-103: a valid default ownership block. Ownership is MANDATORY on every row, so the
# fixtures auto-inject this into any row that does not set its own -- keeping the pre-#316
# tests fixture-compatible. The ownership axis tests pass inject_ownership=False to control
# presence/shape exactly.
_OWN_OK = {"value": "methodology-generic", "reason": "test ownership",
           "provenance": [{"kind": "backlog", "repo": "hub-r", "ref": "#316"}]}


def _manifest(fleet: dict, surfaces: list, version: str = "1.0.0",
              inject_ownership: bool = True) -> dict:
    if inject_ownership:
        surfaces = [({**s, "ownership": _OWN_OK}
                     if isinstance(s, dict) and "ownership" not in s else s)
                    for s in surfaces]
    return {"version": version, "fleet": fleet, "surfaces": surfaces}


_DEPLOY_TOMBSTONE = {"components": [
    {"id": "ruff-gate", "kind": "hook", "status": "removed", "removed_in": "1.2.0",
     "waivable": True},
    {"id": "live-comp", "kind": "hook", "status": "active", "waivable": True},
]}

_BASE_FILES = {"VISION.md": "v\n"}


def _decl(components: list[str], review_date: str = "2099-01-01") -> str:
    entries = [{"component": c, "reason": f"declared {c} for test",
                "review_date": review_date} for c in components]
    return yaml.safe_dump({"sanctioned_divergences": entries}, sort_keys=False)


def _run(manifest: dict, baseline: dict, repos: dict[str, Path], hub_id: str,
         run_date: str = "2026-07-13", allow_override: dict | None = None,
         deploy: dict | None = None):
    """Drive the engine directly (load -> facts -> verdicts) against temp repos."""
    refusals = manifest.pop("_refusals", [])
    targets = []
    for repo_id in sorted(manifest["fleet"]):
        role = manifest["fleet"][repo_id]["role"]
        root = repos.get(repo_id)
        targets.append(fp.RepoTarget(repo_id, role, root,
                                     "" if root else "unresolved: test"))
    facts, allow = {}, {}
    hub_root = repos[hub_id]
    for t in targets:
        if t.root is not None and t.role != "pre-deploy":
            facts[t.repo_id] = fp.collect_facts(t, manifest, baseline, hub_root,
                                                Path("nonexistent-registry.yaml"))
            allow[t.repo_id] = fp.ec.read_allowlist(t.root)
    if allow_override:
        allow.update(allow_override)
    findings, consumed = fp.verdicts(manifest, baseline, targets, facts, allow,
                                     deploy or _DEPLOY_TOMBSTONE, run_date)
    return refusals + findings, targets, facts, allow, consumed


def _loaded(tmp_path: Path, fleet: dict, surfaces: list, inject_ownership: bool = True):
    path = _write_yaml(tmp_path / "parity-surfaces.yaml",
                       _manifest(fleet, surfaces, inject_ownership=inject_ownership))
    manifest, refusals = fp.load_manifest(path)
    manifest["_refusals"] = refusals
    return manifest


_EMPTY_BASELINE = {"dependencies": []}


# ---------------------------------------------------------------------------
# Manifest validation -> refusal findings (refused, never guessed).
# ---------------------------------------------------------------------------


def test_manifest_refusals_skip_bad_rows_keep_good(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [
        {"id": "good", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked", "path": "VISION.md"}},
        {"id": "bad-tier", "kind": "path", "tier": {"hub": "MUSTY"},
         "probe": {"type": "path_tracked", "path": "x"}},
        {"id": "bad-key", "kind": "path", "tier": {"nonrepo": "MUST"},
         "probe": {"type": "path_tracked", "path": "x"}},
        {"id": "no-probe", "kind": "path", "tier": {"hub": "MUST"}},
        {"id": "good", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked", "path": "dup-id"}},
        {"id": "tomb-nojoin", "kind": "tombstone-join", "tier": {"hub": "TOMBSTONE"},
         "probe": {"type": "precommit_remote", "repo_token": "x"}},
    ]
    manifest = _loaded(tmp_path, fleet, surfaces)
    refusals = manifest["_refusals"]
    assert {f.verdict for f in refusals} == {fp.REFUSED}
    assert len(refusals) == 5
    assert [r["id"] for r in manifest["surfaces"]] == ["good"]
    # ambiguous tombstone pointer refuses with NO action proposal
    tomb = next(f for f in refusals if f.surface_id == "tomb-nojoin")
    assert "refusing" in tomb.evidence.lower() or "ambiguous" in tomb.evidence.lower()
    assert "no action proposed" in fp._ACTIONS[fp.REFUSED]


def test_manifest_unreadable_raises(tmp_path):
    import pytest
    with pytest.raises(fp.ManifestUnreadable):
        fp.load_manifest(tmp_path / "absent.yaml")
    bad = tmp_path / "bad.yaml"
    bad.write_text("just: a scalar\n", encoding="utf-8")
    with pytest.raises(fp.ManifestUnreadable):
        fp.load_manifest(bad)
    # invalid UTF-8 is the exit-2 class too, never a raw UnicodeDecodeError crash
    # (codex 2026-07-13)
    binary = tmp_path / "binary.yaml"
    binary.write_bytes(b"version: 1.0.0\nfleet: {\x80\xff}\n")
    with pytest.raises(fp.ManifestUnreadable):
        fp.load_manifest(binary)


def test_probe_missing_required_field_is_refusal_not_crash(tmp_path):
    # codex 2026-07-13: a malformed path_tracked row must REFUSE at load, never
    # reach probe["path"] and crash the facts collector.
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [
        {"id": "no-path", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked"}},
        {"id": "ok-row", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked", "path": "VISION.md"}},
    ]
    manifest = _loaded(tmp_path, fleet, surfaces)
    refusals = manifest["_refusals"]
    assert len(refusals) == 1 and "missing required field" in refusals[0].evidence
    assert [r["id"] for r in manifest["surfaces"]] == ["ok-row"]
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    assert any(f.surface_id == "ok-row" and f.verdict == fp.AT_PARITY
               for f in findings)


def test_duplicate_tombstone_join_is_refused(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    rows = [dict(_TOMB_ROW, id="tomb-1", tier={"hub": "TOMBSTONE"}),
            dict(_TOMB_ROW, id="tomb-2", tier={"hub": "TOMBSTONE"})]
    manifest = _loaded(tmp_path, fleet, rows)
    refusals = manifest["_refusals"]
    assert len(refusals) == 1 and "ambiguous join" in refusals[0].evidence
    assert [r["id"] for r in manifest["surfaces"]] == ["tomb-1"]


def test_hooks_armed_warns_when_config_present_but_stages_dead(tmp_path):
    # FR-6 installed+armed: a carried .pre-commit-config.yaml with no armed stages is
    # the relic-hooksPath silence class -- one WARN per repo, declaration-waivable.
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".pre-commit-config.yaml": _precommit_cfg("some-hook")}))
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    armed = [f for f in findings if f.surface_id == "hooks-armed"]
    assert len(armed) == 1 and armed[0].verdict == fp.WARN_UNDECLARED
    assert "NOT armed" in armed[0].evidence
    # a repo with NO pre-commit config has no arming expectation
    bare = _init_repo(tmp_path / "bare", dict(_BASE_FILES))
    manifest2 = _loaded(tmp_path / "m2", fleet, [])
    findings2, *_ = _run(manifest2, _EMPTY_BASELINE, {"hub-r": bare}, "hub-r")
    assert not [f for f in findings2 if f.surface_id == "hooks-armed"]


def test_duplicate_waiver_component_is_structural_refusal(tmp_path):
    # The structural half of AC-9: two rows sharing one waiver_component would let a
    # single declaration suppress two concerns -> the second row is refused.
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [
        {"id": "row-a", "kind": "path", "tier": {"hub": "LOCAL"},
         "waiver_component": "shared-comp",
         "probe": {"type": "path_tracked", "path": "a.txt"}},
        {"id": "row-b", "kind": "path", "tier": {"hub": "LOCAL"},
         "waiver_component": "shared-comp",
         "probe": {"type": "path_tracked", "path": "b.txt"}},
    ]
    manifest = _loaded(tmp_path, fleet, surfaces)
    assert len(manifest["_refusals"]) == 1
    assert "waiver_component" in manifest["_refusals"][0].evidence
    assert [r["id"] for r in manifest["surfaces"]] == ["row-a"]


# ---------------------------------------------------------------------------
# AC-1 -- undeclared divergence WARNs once; declaring flips with no code change.
# ---------------------------------------------------------------------------


def test_acceptance_1_undeclared_divergence_then_declared(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    surfaces = [{"id": "canonical-doc-vision", "kind": "path",
                 "tier": {"hub": "MUST", "consumer": "MUST"},
                 "probe": {"type": "path_tracked", "path": "VISION.md"}}]
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    cons = _init_repo(tmp_path / "cons",
                      dict(_BASE_FILES, **{"straydir/file.txt": "x\n"}))
    manifest = _loaded(tmp_path, fleet, surfaces)

    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                        "hub-r")
    warns = [f for f in findings if f.verdict == fp.WARN_UNDECLARED]
    assert len(warns) == 1, [str(f) for f in warns]  # EXACTLY one WARN
    assert warns[0].repo_id == "cons" and "straydir" in warns[0].evidence

    # Declare it (data change only -- no code change) -> PASS-declared.
    (cons / ".methodology.yaml").write_text(_decl(["straydir"]), encoding="utf-8")
    findings2, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                         "hub-r")
    assert not [f for f in findings2 if f.verdict == fp.WARN_UNDECLARED]
    declared = [f for f in findings2 if f.verdict == fp.PASS_DECLARED]
    assert len(declared) == 1 and declared[0].waiver_component == "straydir"


# ---------------------------------------------------------------------------
# AC-2 / #332 -- dependency leg.
# ---------------------------------------------------------------------------


_DEP_BASELINE = {"version": "1.0.0", "dependencies": [
    {"name": "pytest-xdist", "recommended": ">=3.8",
     "applies_to": ["hub", "consumer"], "status": "active"}]}


_DEP_PYPROJECT = '[dependency-groups]\ndev = ["pytest-xdist>=3.8"]\n'


def test_acceptance_2_dep_missing_warns_with_expected_vs_actual(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    hub = _init_repo(tmp_path / "hub",
                     dict(_BASE_FILES, **{"pyproject.toml": _DEP_PYPROJECT}))
    cons = _init_repo(tmp_path / "cons", dict(_BASE_FILES))
    (hub / ".venv/Lib/site-packages/pytest_xdist-3.8.0.dist-info").mkdir(parents=True)
    manifest = _loaded(tmp_path, fleet, [])

    findings, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub, "cons": cons}, "hub-r")
    dep = [f for f in findings if f.surface_id == "dep-pytest-xdist"]
    by_repo = {f.repo_id: f for f in dep}
    assert by_repo["hub-r"].verdict == fp.AT_PARITY   # declared AND installed -> ok
    w = by_repo["cons"]
    assert w.verdict == fp.WARN_UNDECLARED                    # missing -> WARN
    assert "expected pytest-xdist >=3.8" in w.evidence        # expected...
    assert "installed: absent" in w.evidence                  # ...vs actual
    assert "block" not in w.verdict.lower()                   # WARN, never a block


def test_dep_installed_but_undeclared_warns(tmp_path):
    # codex 2026-07-13: installed-only satisfaction was a false green -- an
    # undeclared dep vanishes on the next clean env rebuild (#332 contract is
    # DECLARED + installed).
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    (hub / ".venv/Lib/site-packages/pytest_xdist-3.8.0.dist-info").mkdir(parents=True)
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub}, "hub-r")
    f = [x for x in findings if x.surface_id == "dep-pytest-xdist"][0]
    assert f.verdict == fp.WARN_UNDECLARED
    assert "UNDECLARED" in f.evidence and "installed: 3.8.0" in f.evidence


def test_acceptance_2_declared_consumer_does_not_warn(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    hub_sp = hub / ".venv/Lib/site-packages/pytest_xdist-3.8.0.dist-info"
    hub_sp.mkdir(parents=True)
    cons = _init_repo(tmp_path / "cons",
                      dict(_BASE_FILES, **{".methodology.yaml":
                                           _decl(["dep-pytest-xdist"])}))
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub, "cons": cons}, "hub-r")
    dep = {f.repo_id: f for f in findings if f.surface_id == "dep-pytest-xdist"}
    assert dep["cons"].verdict == fp.PASS_DECLARED
    assert "installed: absent" in dep["cons"].evidence  # evidence NOT erased (FR-05)


def test_dep_declared_pin_below_baseline_warns(tmp_path):
    # codex delta re-review 2026-07-13: a declaration pinned BELOW the baseline
    # (==3.1) with a satisfying env (3.8 installed) false-passed -- it regresses on
    # a clean rebuild. An unpinned declaration (presence, no floor) stays accepted.
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES,
        **{"pyproject.toml": '[dependency-groups]\ndev = ["pytest-xdist==3.1"]\n'}))
    (hub / ".venv/Lib/site-packages/pytest_xdist-3.8.0.dist-info").mkdir(parents=True)
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub}, "hub-r")
    f = [x for x in findings if x.surface_id == "dep-pytest-xdist"][0]
    assert f.verdict == fp.WARN_UNDECLARED
    assert "DECLARED pin does not satisfy" in f.evidence
    # unpinned declaration + satisfying install -> AT-PARITY (presence declared)
    (hub / "pyproject.toml").write_text(
        '[dependency-groups]\ndev = ["pytest-xdist"]\n', encoding="utf-8")
    findings2, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub}, "hub-r")
    f2 = [x for x in findings2 if x.surface_id == "dep-pytest-xdist"][0]
    assert f2.verdict == fp.AT_PARITY
    # codex round-3: an upper-bound/compound specifier must never read as unpinned --
    # refused-to-assume -> WARN ('<4' cannot prove the >=3.8 floor on a clean rebuild)
    for spec in ("pytest-xdist<4", "pytest-xdist>=3.8,<4"):
        (hub / "pyproject.toml").write_text(
            f'[dependency-groups]\ndev = ["{spec}"]\n', encoding="utf-8")
        findings3, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub}, "hub-r")
        f3 = [x for x in findings3 if x.surface_id == "dep-pytest-xdist"][0]
        assert f3.verdict == fp.WARN_UNDECLARED, spec
        assert "DECLARED pin does not satisfy" in f3.evidence


def test_refused_tombstone_join_never_stale_decorates(tmp_path):
    # codex delta re-review 2026-07-13: a refused (unevaluable) join must not ALSO
    # propose pruning the component's declaration as stale in the same run.
    fleet = {"hub-r": {"role": "hub"}}
    row = dict(_TOMB_ROW, tier={"hub": "TOMBSTONE"},
               join={"manifest_component": "ruff-gato"})  # mis-addressed
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".pre-commit-config.yaml": _RUFF_CFG,
                        ".methodology.yaml": _decl(["ruff-gate"])}))
    manifest = _loaded(tmp_path, fleet, [row])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    assert [f for f in findings if f.verdict == fp.REFUSED]
    assert not [f for f in findings if f.verdict == fp.STALE_DECLARATION]


def test_dep_version_drift_warns(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    (hub / ".venv/Lib/site-packages/pytest_xdist-3.1.0.dist-info").mkdir(parents=True)
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub}, "hub-r")
    dep = [f for f in findings if f.surface_id == "dep-pytest-xdist"][0]
    assert dep.verdict == fp.WARN_UNDECLARED
    assert "installed: 3.1.0" in dep.evidence


# ---------------------------------------------------------------------------
# AC-5 -- d1 identity across names (canonical id, local names, declared skip-set).
# ---------------------------------------------------------------------------


def _precommit_cfg(hook_id: str) -> str:
    return yaml.safe_dump({"repos": [{"repo": "local", "hooks": [
        {"id": hook_id, "name": hook_id, "entry": "python x.py",
         "language": "system"}]}]}, sort_keys=False)


def test_acceptance_5_one_canonical_id_three_local_names(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "ai-like": {"role": "consumer"},
             "corp-like": {"role": "consumer"}}
    surfaces = [{
        "id": "audit-casing-r4", "kind": "precommit-hook",
        "tier": {"hub": "MUST", "consumer": "MUST"},
        "probe": {"type": "precommit_hook", "hook_id": "validate-audit-casing"},
        "local_names": {"hub-r": "validate-hermetization"},
        "declared_divergence": {"corp-like": "11-name grandfather skip-set"},
    }]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".pre-commit-config.yaml":
                        _precommit_cfg("validate-hermetization")}))
    ai = _init_repo(tmp_path / "ai", dict(
        _BASE_FILES, **{".pre-commit-config.yaml":
                        _precommit_cfg("validate-audit-casing")}))
    corp = _init_repo(tmp_path / "corp", dict(
        _BASE_FILES, **{".pre-commit-config.yaml":
                        _precommit_cfg("validate-audit-casing"),
                        ".methodology.yaml": _decl(["audit-casing-r4"])}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE,
                        {"hub-r": hub, "ai-like": ai, "corp-like": corp}, "hub-r")
    row = {f.repo_id: f for f in findings if f.surface_id == "audit-casing-r4"}
    # one canonical id resolves all three local names -- zero byte-diff noise
    assert row["hub-r"].verdict == fp.AT_PARITY
    assert row["ai-like"].verdict == fp.AT_PARITY
    assert row["corp-like"].verdict == fp.PASS_DECLARED       # skip-set reads declared
    assert "skip-set" in row["corp-like"].evidence
    assert not any(f.verdict in (fp.WARN_UNDECLARED, fp.MUST_ABSENT)
                   for f in row.values())


def test_acceptance_5_expected_divergence_missing_declaration_warns(tmp_path):
    # The corp-like repo WITHOUT its skip-set declaration must WARN (the divergence
    # is real; only the declaration makes it sanctioned).
    fleet = {"hub-r": {"role": "hub"}, "corp-like": {"role": "consumer"}}
    surfaces = [{
        "id": "audit-casing-r4", "kind": "precommit-hook",
        "tier": {"hub": "MUST", "consumer": "MUST"},
        "probe": {"type": "precommit_hook", "hook_id": "validate-audit-casing"},
        "local_names": {"hub-r": "validate-hermetization"},
        "declared_divergence": {"corp-like": "11-name grandfather skip-set"},
    }]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".pre-commit-config.yaml":
                        _precommit_cfg("validate-hermetization")}))
    corp = _init_repo(tmp_path / "corp", dict(
        _BASE_FILES, **{".pre-commit-config.yaml":
                        _precommit_cfg("validate-audit-casing")}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "corp-like": corp},
                        "hub-r")
    corp_f = [f for f in findings if f.repo_id == "corp-like"
              and f.surface_id == "audit-casing-r4"][0]
    assert corp_f.verdict == fp.WARN_UNDECLARED


# ---------------------------------------------------------------------------
# AC-6 -- tombstone teeth.
# ---------------------------------------------------------------------------


_TOMB_ROW = {
    "id": "ruff-gate", "kind": "tombstone-join",
    "tier": {"hub": "TOMBSTONE", "consumer": "TOMBSTONE"},
    "waivable": True,
    "probe": {"type": "precommit_remote", "repo_token": "ruff-pre-commit"},
    "join": {"manifest_component": "ruff-gate"},
}

_RUFF_CFG = yaml.safe_dump({"repos": [
    {"repo": "https://github.com/astral-sh/ruff-pre-commit", "rev": "v0.15.5",
     "hooks": [{"id": "ruff"}]}]}, sort_keys=False)


def test_acceptance_6_undeclared_readd_of_tombstone_warns(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    cons = _init_repo(tmp_path / "cons",
                      dict(_BASE_FILES, **{".pre-commit-config.yaml": _RUFF_CFG}))
    manifest = _loaded(tmp_path, fleet, [dict(_TOMB_ROW)])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                        "hub-r")
    row = {f.repo_id: f for f in findings if f.surface_id == "ruff-gate"}
    assert row["cons"].verdict == fp.TOMBSTONE_VIOLATED       # S3 machine-caught
    assert "removed" in row["cons"].evidence
    assert row["hub-r"].verdict == fp.AT_PARITY               # absent = honored
    assert "absent-by-design" in row["hub-r"].evidence


def test_acceptance_6_declared_readd_passes(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    cons = _init_repo(tmp_path / "cons", dict(
        _BASE_FILES, **{".pre-commit-config.yaml": _RUFF_CFG,
                        ".methodology.yaml": _decl(["ruff-gate"])}))
    manifest = _loaded(tmp_path, fleet, [dict(_TOMB_ROW)])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                        "hub-r")
    cons_f = [f for f in findings if f.repo_id == "cons"
              and f.surface_id == "ruff-gate"][0]
    assert cons_f.verdict == fp.PASS_DECLARED                 # re-activate KNOWINGLY


def test_acceptance_6_misaddressed_pointer_refuses_never_proposes(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub",
                     dict(_BASE_FILES, **{".pre-commit-config.yaml": _RUFF_CFG}))
    # (a) pointer to a component the deploy manifest does not know
    row = dict(_TOMB_ROW, join={"manifest_component": "ruff-gato"})
    manifest = _loaded(tmp_path, fleet, [row])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    ref = [f for f in findings if f.verdict == fp.REFUSED]
    assert len(ref) == 1 and "mis-addressed" in ref[0].evidence
    assert "no action proposed" in ref[0].evidence or "no action" in ref[0].action
    # (b) join mismatch: parity says tombstone, deploy says the component is ACTIVE
    row2 = dict(_TOMB_ROW, join={"manifest_component": "live-comp"})
    manifest2 = _loaded(tmp_path, fleet, [row2])
    findings2, *_ = _run(manifest2, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    ref2 = [f for f in findings2 if f.verdict == fp.REFUSED]
    assert len(ref2) == 1 and "mismatch" in ref2[0].evidence
    # neither refusal proposes carry/prune/re-activation
    for f in ref + ref2:
        for verb in ("carry", "prune", "re-activate", "delete", "install"):
            assert verb not in f.evidence.lower()


# ---------------------------------------------------------------------------
# AC-9 -- declaration precision (one concern, exact-id, stale decoration).
# ---------------------------------------------------------------------------


def test_acceptance_9_one_declaration_cannot_suppress_two(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [
        {"id": "local-x", "kind": "path", "tier": {"hub": "LOCAL"},
         "probe": {"type": "path_tracked", "path": "x.txt"}},
        {"id": "local-y", "kind": "path", "tier": {"hub": "LOCAL"},
         "probe": {"type": "path_tracked", "path": "y.txt"}},
    ]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{"x.txt": "x\n", "y.txt": "y\n",
                        ".methodology.yaml": _decl(["local-x"])}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    by_sid = {f.surface_id: f for f in findings if f.surface_id.startswith("local-")}
    assert by_sid["local-x"].verdict == fp.PASS_DECLARED
    assert by_sid["local-y"].verdict == fp.WARN_UNDECLARED    # second concern survives


def test_acceptance_9_bare_id_and_substring_match_rejected(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    # declarations 'stray' (prefix) and 'straydir-extra' (superstring) must NOT match
    # the sweep divergence 'straydir'
    cons = _init_repo(tmp_path / "cons", dict(
        _BASE_FILES, **{"straydir/file.txt": "x\n",
                        ".methodology.yaml": _decl(["stray", "straydir-extra"])}))
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                        "hub-r")
    stray = [f for f in findings if "straydir" in f.evidence
             and f.surface_id == "root-sweep"]
    assert len(stray) == 1 and stray[0].verdict == fp.WARN_UNDECLARED


def test_acceptance_9_orphaned_declaration_surfaces_stale(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [{"id": "local-x", "kind": "path", "tier": {"hub": "LOCAL"},
                 "probe": {"type": "path_tracked", "path": "x.txt"}}]
    # x.txt ABSENT -> surface at parity -> the declaration decorates STALE
    hub = _init_repo(tmp_path / "hub",
                     dict(_BASE_FILES, **{".methodology.yaml": _decl(["local-x"])}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    stale = [f for f in findings if f.verdict == fp.STALE_DECLARATION]
    assert len(stale) == 1
    assert stale[0].waiver_component == "local-x"
    assert "stale" in stale[0].evidence


def test_unmapped_declaration_is_inert_not_warn(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [{"id": "canonical-doc-vision", "kind": "path",
                 "tier": {"hub": "MUST"},
                 "probe": {"type": "path_tracked", "path": "VISION.md"}}]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".methodology.yaml": _decl(["something-unknown"])}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, targets, facts, allow, consumed = _run(
        manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    assert not [f for f in findings
                if f.verdict in (fp.WARN_UNDECLARED, fp.STALE_DECLARATION)]
    unmapped = fp.unmapped_declarations(manifest, targets, allow, consumed)
    assert "something-unknown (no v1 surface)" in unmapped["hub-r"]


# ---------------------------------------------------------------------------
# S4 -- gitignore effect probe (check-ignore semantics, never text-grep).
# ---------------------------------------------------------------------------


def test_s4_inline_comment_pattern_fails_effect_probe(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [{"id": "ignore-hypothesis", "kind": "gitignore-effect",
                 "tier": {"hub": "IGNORE"},
                 "probe": {"type": "check_ignore", "candidate": ".hypothesis/x"}}]
    # The S4 trap: the trailing inline comment becomes PART of the pattern -> the
    # line is textually present but semantically inert.
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".gitignore": ".hypothesis/   # cache dir\n"}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    f = [x for x in findings if x.surface_id == "ignore-hypothesis"][0]
    assert ".hypothesis/" in (hub / ".gitignore").read_text(encoding="utf-8")  # text-grep would pass
    assert f.verdict == fp.WARN_UNDECLARED                    # the effect probe does not
    assert "effect probe" in f.evidence


def test_s4_own_line_comment_passes_effect_probe(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [{"id": "ignore-hypothesis", "kind": "gitignore-effect",
                 "tier": {"hub": "IGNORE"},
                 "probe": {"type": "check_ignore", "candidate": ".hypothesis/x"}}]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{".gitignore": "# cache dir\n.hypothesis/\n"}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    f = [x for x in findings if x.surface_id == "ignore-hypothesis"][0]
    assert f.verdict == fp.AT_PARITY


# ---------------------------------------------------------------------------
# section 9b -- expired review_date is ADVISORY, not drift.
# ---------------------------------------------------------------------------


def test_expired_review_date_is_advisory_rewarn(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [{"id": "local-x", "kind": "path", "tier": {"hub": "LOCAL"},
                 "probe": {"type": "path_tracked", "path": "x.txt"}}]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{"x.txt": "x\n",
                        ".methodology.yaml": _decl(["local-x"],
                                                   review_date="2020-01-01")}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r",
                        run_date="2026-07-13")
    f = [x for x in findings if x.surface_id == "local-x"][0]
    assert f.verdict == fp.ADVISORY_REWARN
    assert f.severity == fp.SEV_WARN
    assert "EXPIRED" in f.evidence
    # ...and with a future run_date the same declaration is simply valid.
    findings2, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r",
                         run_date="2019-12-31")
    f2 = [x for x in findings2 if x.surface_id == "local-x"][0]
    assert f2.verdict == fp.PASS_DECLARED


# ---------------------------------------------------------------------------
# Sweep branches + inverse + hub-as-member + fidelity.
# ---------------------------------------------------------------------------


def test_sweep_tracked_ephemera_warns_distinctly(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub",
                     dict(_BASE_FILES, **{".pytest_cache/junk.txt": "x\n"}))
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    eph = [f for f in findings if f.verdict == fp.TRACKED_EPHEMERA]
    assert len(eph) == 1 and ".pytest_cache" in eph[0].evidence


def test_inverse_rule_and_hub_as_member(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    surfaces = [
        {"id": "src-dir", "kind": "path",
         "tier": {"hub": "INVERSE", "consumer": "LOCAL"}, "declared_by": "intake-12",
         "probe": {"type": "dir_tracked", "path": "src"}},
        {"id": "docs-handoffs-dir", "kind": "path",
         "tier": {"hub": "MUST", "consumer": "INVERSE"},
         "probe": {"type": "dir_tracked", "path": "docs/handoffs"}},
    ]
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{"src/x.py": "x = 1\n", "docs/handoffs/h.md": "h\n"}))
    cons = _init_repo(tmp_path / "cons", dict(
        _BASE_FILES, **{"src/y.py": "y = 1\n", "docs/handoffs/h.md": "h\n"}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                        "hub-r")
    by_key = {(f.repo_id, f.surface_id): f for f in findings}
    # hub is walked as a fleet member and its own inverse violation surfaces
    assert by_key[("hub-r", "src-dir")].verdict == fp.MUST_ABSENT
    assert by_key[("hub-r", "src-dir")].severity == fp.SEV_ERROR
    assert by_key[("hub-r", "docs-handoffs-dir")].verdict == fp.AT_PARITY
    # consumer: src is settled-template LOCAL (no declaration needed), handoffs forbidden
    assert by_key[("cons", "src-dir")].verdict == fp.AT_PARITY
    assert "intake #12" in by_key[("cons", "src-dir")].evidence
    assert by_key[("cons", "docs-handoffs-dir")].verdict == fp.MUST_ABSENT


def test_hub_block_rev_fidelity_present_not_carried(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    surfaces = [{"id": "precommit-hub-block", "kind": "precommit-hook",
                 "tier": {"consumer": "MUST"},
                 "probe": {"type": "precommit_remote", "repo_token": "dev-knowledge",
                           "expected_rev_from": "deployed-versions",
                           "ancestry": True,
                           "required_hook_ids": ["backlog-id-on-close",
                                                 "block-ff-push"]}}]
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    _git(["tag", "v1.0.0"], hub)
    cfg = yaml.safe_dump({"repos": [
        {"repo": "https://github.com/x/dev-knowledge", "rev": "v9.9.9",
         "hooks": [{"id": "block-ff-push"}]}]}, sort_keys=False)
    cons = _init_repo(tmp_path / "cons",
                      dict(_BASE_FILES, **{".pre-commit-config.yaml": cfg}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    registry = _write_yaml(tmp_path / "reg.yaml", {"repos": {
        "hub-r": {"source_tag": None}, "cons": {"source_tag": "v1.0.0"}}})

    def _cons_finding():
        targets = [fp.RepoTarget("cons", "consumer", cons, "")]
        facts = {"cons": fp.collect_facts(targets[0], manifest, _EMPTY_BASELINE, hub,
                                          registry)}
        findings, _ = fp.verdicts(manifest, _EMPTY_BASELINE, targets, facts, {},
                                  _DEPLOY_TOMBSTONE, "2026-07-13")
        return [x for x in findings if x.surface_id == "precommit-hub-block"][0]

    f = _cons_finding()
    assert f.verdict == fp.WARN_UNDECLARED
    assert "present != carried" in f.evidence and "v9.9.9" in f.evidence
    # rev aligned but a required hook id missing -> still not carried faithfully
    # (intake #12: fidelity = rev + hook IDS)
    (cons / ".pre-commit-config.yaml").write_text(
        cfg.replace("v9.9.9", "v1.0.0"), encoding="utf-8")
    f_ids = _cons_finding()
    assert f_ids.verdict == fp.WARN_UNDECLARED
    assert "backlog-id-on-close" in f_ids.evidence
    assert "rev + hook ids" in f_ids.evidence
    # aligned rev + full required id set + real tag -> AT-PARITY with ancestry note
    cfg_ok = yaml.safe_dump({"repos": [
        {"repo": "https://github.com/x/dev-knowledge", "rev": "v1.0.0",
         "hooks": [{"id": "backlog-id-on-close"}, {"id": "block-ff-push"}]}]},
        sort_keys=False)
    (cons / ".pre-commit-config.yaml").write_text(cfg_ok, encoding="utf-8")
    f2 = _cons_finding()
    assert f2.verdict == fp.AT_PARITY and "ancestor" in f2.evidence


# ---------------------------------------------------------------------------
# ADR-102: enforcement-gate-rev axis (gate legitimately ahead of corpus).
# The hub fixture carries two REAL tags: v1.2.0 (corpus, ancestor) and v1.3.1
# (gate, descendant) -- ancestry is genuine, never hand-shaped (LESSONS 2026-06-05).
# ---------------------------------------------------------------------------


def _gate_hub(tmp_path):
    """Temp hub with v1.2.0 (commit 1) as a strict ancestor of v1.3.1 (commit 2 = HEAD)."""
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    _git(["tag", "v1.2.0"], hub)                       # corpus tag at commit 1
    (hub / "gate.txt").write_text("g\n", encoding="utf-8", newline="\n")
    _git(["add", "-A"], hub)
    _git(["commit", "-q", "-m", "gate uplift"], hub)
    _git(["tag", "v1.3.1"], hub)                       # gate tag at commit 2 (descendant)
    return hub


def _gate_row(*, declare=True, gate_tag="v1.3.1"):
    row = {"id": "precommit-hub-block", "kind": "precommit-hook",
           "tier": {"consumer": "MUST"},
           "probe": {"type": "precommit_remote", "repo_token": "dev-knowledge",
                     "expected_rev_from": "deployed-versions", "ancestry": True,
                     "required_hook_ids": ["backlog-id-on-close", "block-ff-push"]}}
    if declare:
        row["gate_rev_ahead"] = {"cons": {
            "gate_tag": gate_tag,
            "reason": "gate uplifted ahead of corpus for test (#318/#319)",
            "provenance": [{"kind": "git-tag", "repo": ".dev-knowledge", "ref": gate_tag},
                           {"kind": "backlog", "repo": ".dev-knowledge", "ref": "#336"}]}}
    return row


def _gate_cons(tmp_path, *, pin="v1.3.1", hooks=("backlog-id-on-close", "block-ff-push"),
               config=True, methodology=None):
    files = dict(_BASE_FILES)
    if config:
        files[".pre-commit-config.yaml"] = yaml.safe_dump({"repos": [
            {"repo": "https://github.com/x/dev-knowledge", "rev": pin,
             "hooks": [{"id": h} for h in hooks]}]}, sort_keys=False)
    if methodology is not None:
        files[".methodology.yaml"] = methodology
    return _init_repo(tmp_path / "cons", files)


def _gate_finding(tmp_path, hub, cons, row, *, corpus="v1.2.0", allow=None):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    manifest = _loaded(tmp_path, fleet, [row])
    registry = _write_yaml(tmp_path / "reg.yaml", {"repos": {
        "hub-r": {"source_tag": None}, "cons": {"source_tag": corpus}}})
    targets = [fp.RepoTarget("cons", "consumer", cons, "")]
    facts = {"cons": fp.collect_facts(targets[0], manifest, _EMPTY_BASELINE, hub,
                                      registry)}
    findings, _ = fp.verdicts(manifest, _EMPTY_BASELINE, targets, facts, allow or {},
                              _DEPLOY_TOMBSTONE, "2026-07-13")
    return next(x for x in findings if x.surface_id == "precommit-hub-block")


def test_gate_ahead_declared_when_proven_ahead(tmp_path):
    # ACCEPTANCE #1: gate ahead + full declaration + all predicates -> GATE_AHEAD_DECLARED,
    # zero WARN. The pin is a proven strict descendant of the corpus source_tag.
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path)
    f = _gate_finding(tmp_path, hub, cons, _gate_row())
    assert f.verdict == fp.GATE_AHEAD_DECLARED
    assert f.severity == fp.SEV_INFO
    assert "v1.3.1" in f.evidence and "v1.2.0" in f.evidence and "ADR-102" in f.evidence


def test_gate_ahead_undeclared_split_still_warns(tmp_path):
    # NEGATIVE (a): the SAME ahead-state with NO gate_rev_ahead declaration still WARNs.
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path)
    f = _gate_finding(tmp_path, hub, cons, _gate_row(declare=False))
    assert f.verdict == fp.WARN_UNDECLARED and f.severity == fp.SEV_ERROR
    assert "present != carried" in f.evidence and "v1.3.1" in f.evidence


def test_gate_ahead_declared_tag_mismatch_warns(tmp_path):
    # NEGATIVE (a'): declared gate_tag != the actual pin -> A != G -> WARN (anti-regress).
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path, pin="v1.3.1")
    f = _gate_finding(tmp_path, hub, cons, _gate_row(gate_tag="v1.2.0"))
    assert f.verdict == fp.WARN_UNDECLARED


def test_gate_ahead_missing_hook_id_warns(tmp_path):
    # NEGATIVE (a'): an ahead gate that DROPS a required hook id is not carried faithfully.
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path, hooks=("block-ff-push",))  # missing backlog-id-on-close
    f = _gate_finding(tmp_path, hub, cons, _gate_row())
    assert f.verdict == fp.WARN_UNDECLARED


def test_gate_ahead_pin_revert_behind_corpus_warns(tmp_path):
    # NEGATIVE (b): a pin-revert (gate BEHIND corpus) is not "ahead" -> WARN, never blessed.
    # corpus source_tag = v1.3.1 (descendant); pin = v1.2.0 (ancestor) -> C is NOT an
    # ancestor of the pin, so corpus_is_ancestor_of_rev is False.
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path, pin="v1.2.0")
    f = _gate_finding(tmp_path, hub, cons, _gate_row(gate_tag="v1.2.0"), corpus="v1.3.1")
    assert f.verdict == fp.WARN_UNDECLARED


def test_gate_ahead_absent_surface_still_must_absent(tmp_path):
    # NEGATIVE (b): a gate_rev_ahead declaration cannot CONJURE presence -- an absent
    # hub-block is still MUST_ABSENT.
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path, config=False)  # no .pre-commit-config.yaml at all
    f = _gate_finding(tmp_path, hub, cons, _gate_row())
    assert f.verdict == fp.MUST_ABSENT and f.severity == fp.SEV_ERROR


def test_gate_ahead_methodology_declaration_cannot_clear(tmp_path):
    # NEGATIVE (b): a .methodology.yaml waiver does NOT clear a gate mismatch -- the MUST
    # row stays non-waivable and the waiver channel is unreachable for it.
    assert fp._row_waivable(_gate_row(), "MUST") is False
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path)  # ahead pin, but NO manifest gate_rev_ahead declaration
    allow = {"cons": fp.ec.read_allowlist(
        _gate_cons(tmp_path / "declared", methodology=_decl(["precommit-hub-block"])))}
    f = _gate_finding(tmp_path, hub, cons, _gate_row(declare=False), allow=allow)
    assert f.verdict == fp.WARN_UNDECLARED   # NOT PASS_DECLARED -- waiver does not apply


def test_gate_ahead_inert_declaration_surfaces_stale(tmp_path):
    # RETIREMENT: once the corpus catches up (source_tag == pin), the ahead expectation is
    # self-invalidated -> a visible STALE_DECLARATION, not a false pass.
    hub = _gate_hub(tmp_path)
    cons = _gate_cons(tmp_path, pin="v1.3.1")
    f = _gate_finding(tmp_path, hub, cons, _gate_row(), corpus="v1.3.1")
    assert f.verdict == fp.STALE_DECLARATION and f.severity == fp.SEV_WARN
    assert "caught up" in f.evidence and "PRUNE" in f.evidence


def test_waivable_true_on_must_row_is_loader_refusal(tmp_path):
    # ADR-102 loader refusal: a necessary condition can never be marked waivable.
    fleet = {"hub-r": {"role": "hub"}}
    surfaces = [
        {"id": "good", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked", "path": "VISION.md"}},
        {"id": "waivable-must", "kind": "path", "tier": {"hub": "MUST"}, "waivable": True,
         "probe": {"type": "path_tracked", "path": "x"}},
        {"id": "waivable-inverse", "kind": "path", "tier": {"consumer": "INVERSE"},
         "waivable": True, "probe": {"type": "path_tracked", "path": "y"}},
    ]
    manifest = _loaded(tmp_path, fleet, surfaces)
    refusals = manifest["_refusals"]
    refused_ids = {f.surface_id for f in refusals if f.verdict == fp.REFUSED}
    assert {"waivable-must", "waivable-inverse"} <= refused_ids
    assert [r["id"] for r in manifest["surfaces"]] == ["good"]   # good row survives
    assert any("never waivable" in f.evidence for f in refusals)


def test_gate_ahead_schema_does_not_break_registry_crosscheck(tmp_path):
    # NEGATIVE (c): the both-directions registry cross-check is unaffected by the v1.1.0
    # gate_rev_ahead schema -- a surface-row field cannot touch the fleet<->registry keys.
    manifest_path = _write_yaml(tmp_path / "m.yaml", _manifest(
        {"hub-r": {"role": "hub"}, "extra": {"role": "consumer"}},
        [_gate_row()], version="1.1.0"))
    manifest, _ = fp.load_manifest(manifest_path)
    registry = _write_yaml(tmp_path / "reg.yaml",
                           {"repos": {"hub-r": {}, "missing": {}}})
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    _, findings = fp.resolve_fleet(manifest, hub, registry, tmp_path, {})
    ev = " ".join(f.evidence for f in findings)
    assert "missing" in ev and "extra" in ev
    assert all(f.verdict == fp.REFUSED for f in findings)


def test_gate_ahead_alias_tag_same_commit_still_warns(tmp_path):
    # terra HIGH (2026-07-17): two DIFFERENTLY-NAMED tags on the SAME commit are EQUAL,
    # never ahead -- `merge-base --is-ancestor` is REFLEXIVE, so tag-name inequality alone
    # must NOT bless. Requires the strict predicate (C anc G AND G NOT anc C).
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    _git(["tag", "v1.2.0"], hub)
    _git(["tag", "v1.2.0-alias"], hub)          # SAME commit, different name
    cons = _gate_cons(tmp_path, pin="v1.2.0-alias")
    f = _gate_finding(tmp_path, hub, cons, _gate_row(gate_tag="v1.2.0-alias"),
                      corpus="v1.2.0")
    assert f.verdict == fp.WARN_UNDECLARED       # equal-by-commit, not strictly ahead


def test_gate_rev_ahead_malformed_declaration_is_loader_refusal(tmp_path):
    # terra HIGH (2026-07-17): a malformed gate_rev_ahead is refused at LOAD -- it never
    # crashes collect_facts and never blesses a MUST mismatch without reason+provenance.
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    probe = {"type": "precommit_remote", "repo_token": "dev-knowledge",
             "expected_rev_from": "deployed-versions"}
    good = {"id": "ok", "kind": "path", "tier": {"hub": "MUST"},
            "probe": {"type": "path_tracked", "path": "VISION.md"}}

    def _row(gra):
        return {"id": "precommit-hub-block", "kind": "precommit-hook",
                "tier": {"consumer": "MUST"}, "probe": dict(probe),
                "gate_rev_ahead": gra}

    ok_prov = [{"kind": "git-tag", "repo": ".dev-knowledge", "ref": "v1"}]
    cases = [
        "not-a-mapping",                                              # truthy non-dict (crash guard)
        {"cons": {"gate_tag": "v1", "reason": "r", "provenance": [{}]}},   # bad provenance item
        {"cons": {"reason": "r", "provenance": ok_prov}},                 # missing gate_tag
        {"cons": {"gate_tag": "v1", "reason": " ", "provenance": ok_prov}},  # blank reason
        {"ghost": {"gate_tag": "v1", "reason": "r", "provenance": ok_prov}},  # key not in fleet
        {"cons": {"gate_tag": "v1", "reason": "r", "provenance": "not-a-list"}},  # provenance not a list
        {"cons": {"gate_tag": "v1", "reason": "r",
                  "provenance": [{"kind": "  ", "repo": "r", "ref": "x"}]}},  # whitespace field
        {"cons": {"gate_tag": "v1", "reason": "r",
                  "provenance": [{"kind": 1, "repo": "r", "ref": "x"}]}},     # non-string field
        {"cons": {"gate_tag": 1.3, "reason": "r", "provenance": ok_prov}},    # non-string gate_tag
    ]
    for i, gra in enumerate(cases):
        m = _loaded(tmp_path / f"case{i}", fleet, [_row(gra), good])
        assert any(f.verdict == fp.REFUSED for f in m["_refusals"]), gra
        assert [r["id"] for r in m["surfaces"]] == ["ok"]   # bad row skipped, good survives


# ---- ADR-103 ownership axis --------------------------------------------------------

def _own_prov():
    return [{"kind": "backlog", "repo": "hub-r", "ref": "#316"}]


def test_ownership_wellformed_loads_clean(tmp_path):
    # ADR-103: a well-formed ownership block loads with no refusal; the classification is
    # readable off the surviving row.
    fleet = {"hub-r": {"role": "hub"}}
    row = {"id": "t", "kind": "path", "tier": {"hub": "MUST"},
           "probe": {"type": "path_tracked", "path": "VISION.md"},
           "ownership": {"value": "project", "reason": "repo-local product dir",
                         "provenance": _own_prov()}}
    m = _loaded(tmp_path, fleet, [row], inject_ownership=False)
    assert m["_refusals"] == []
    assert [r["id"] for r in m["surfaces"]] == ["t"]
    assert m["surfaces"][0]["ownership"]["value"] == "project"


def test_ownership_missing_is_loader_refusal(tmp_path):
    # ADR-103: ownership is MANDATORY -- a row without it is refused (row skipped), the
    # good row survives.
    fleet = {"hub-r": {"role": "hub"}}
    bad = {"id": "nope", "kind": "path", "tier": {"hub": "MUST"},
           "probe": {"type": "path_tracked", "path": "VISION.md"}}          # no ownership
    good = {"id": "ok", "kind": "path", "tier": {"hub": "MUST"},
            "probe": {"type": "path_tracked", "path": "VISION.md"}, "ownership": _OWN_OK}
    m = _loaded(tmp_path, fleet, [bad, good], inject_ownership=False)
    assert any(f.verdict == fp.REFUSED for f in m["_refusals"])
    assert [r["id"] for r in m["surfaces"]] == ["ok"]


def test_ownership_malformed_declaration_is_loader_refusal(tmp_path):
    # ADR-103: the malformed-ownership refusal table -- value/reason/provenance grammar,
    # mirroring the gate_rev_ahead table (the two share _declaration_bad).
    fleet = {"hub-r": {"role": "hub"}}
    good = {"id": "ok", "kind": "path", "tier": {"hub": "MUST"},
            "probe": {"type": "path_tracked", "path": "VISION.md"}, "ownership": _OWN_OK}
    ok_prov = _own_prov()

    def _row(own):
        return {"id": "tgt", "kind": "path", "tier": {"hub": "MUST"},
                "probe": {"type": "path_tracked", "path": "VISION.md"}, "ownership": own}

    cases = [
        "not-a-mapping",                                                     # truthy non-dict
        {"value": "wrong", "reason": "r", "provenance": ok_prov},            # value not in enum
        {"value": 1, "reason": "r", "provenance": ok_prov},                 # non-string value
        {"reason": "r", "provenance": ok_prov},                            # missing value
        {"value": "project", "reason": " ", "provenance": ok_prov},         # blank reason
        {"value": "project", "provenance": ok_prov},                       # missing reason
        {"value": "project", "reason": "r", "provenance": "not-a-list"},     # provenance not a list
        {"value": "project", "reason": "r", "provenance": []},             # empty provenance
        {"value": "project", "reason": "r", "provenance": [{}]},           # provenance item empty
        {"value": "project", "reason": "r",
         "provenance": [{"kind": "  ", "repo": "r", "ref": "x"}]},          # whitespace field
        {"value": "project", "reason": "r",
         "provenance": [{"kind": 1, "repo": "r", "ref": "x"}]},             # non-string field
    ]
    for i, own in enumerate(cases):
        m = _loaded(tmp_path / f"own{i}", fleet, [_row(own), good], inject_ownership=False)
        assert any(f.verdict == fp.REFUSED for f in m["_refusals"]), own
        assert [r["id"] for r in m["surfaces"]] == ["ok"], own            # bad skipped, good survives


def test_ownership_and_gate_share_declaration_grammar_no_fork(tmp_path):
    # ADR-102/ADR-103: BOTH axes validate reason+provenance through the ONE _declaration_bad
    # predicate. For a battery of shared-wrapper shapes, the gate row and the ownership row
    # (differing ONLY in the axis-specific value: gate_tag vs ownership value) are
    # refused-or-accepted IDENTICALLY -- the grammar cannot fork.
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    ok_prov = _own_prov()
    shapes = [
        ({"reason": "r", "provenance": ok_prov}, False),                   # well-formed
        ({"reason": " ", "provenance": ok_prov}, True),                    # blank reason
        ({"reason": "r", "provenance": []}, True),                         # empty provenance
        ({"reason": "r", "provenance": [{}]}, True),                       # bad provenance item
        ({"reason": "r", "provenance": "x"}, True),                        # provenance not a list
    ]
    for i, (wrapper, expect_bad) in enumerate(shapes):
        # the shared predicate directly
        assert (fp._declaration_bad(wrapper) is not None) == expect_bad, wrapper
        # gate_rev_ahead row (axis value = gate_tag)
        gate_row = {"id": "precommit-hub-block", "kind": "precommit-hook",
                    "tier": {"consumer": "MUST"},
                    "probe": {"type": "precommit_remote", "repo_token": "dev-knowledge",
                              "expected_rev_from": "deployed-versions"},
                    "gate_rev_ahead": {"cons": {"gate_tag": "v1", **wrapper}},
                    "ownership": _OWN_OK}
        gm = _loaded(tmp_path / f"gate{i}", fleet, [gate_row], inject_ownership=False)
        gate_refused = any(f.verdict == fp.REFUSED for f in gm["_refusals"])
        # ownership row (axis value = ownership category)
        own_row = {"id": "tgt", "kind": "path", "tier": {"hub": "MUST"},
                   "probe": {"type": "path_tracked", "path": "VISION.md"},
                   "ownership": {"value": "project", **wrapper}}
        om = _loaded(tmp_path / f"own{i}", fleet, [own_row], inject_ownership=False)
        own_refused = any(f.verdict == fp.REFUSED for f in om["_refusals"])
        assert gate_refused == own_refused == expect_bad, wrapper


def test_gate_ahead_ok_rejects_malformed_provenance_no_fork(tmp_path):
    # terra HIGH (2026-07-17): the RUNTIME predicate _gate_ahead_ok must route
    # reason+provenance through the SAME _declaration_bad as the loader -- a malformed
    # provenance item cannot bless GATE_AHEAD_DECLARED even for a direct engine caller
    # that bypasses load_manifest. All ancestry conjuncts held true; only the grammar varies.
    target = fp.RepoTarget("cons", "consumer", tmp_path, "")
    res = {"rev": "v1.3.1", "tag_exists_in_hub": True, "tag_is_ancestor": True,
           "gate_strictly_ahead": True, "missing_hook_ids": []}
    ok_prov = [{"kind": "git-tag", "repo": ".dev-knowledge", "ref": "v1.3.1"}]

    def _row(entry):
        return {"gate_rev_ahead": {"cons": entry}}

    good = _row({"gate_tag": "v1.3.1", "reason": "r", "provenance": ok_prov})
    assert fp._gate_ahead_ok(good, target, res) is True
    # malformed provenance item -> _declaration_bad fails -> no bless (the fork is closed)
    assert fp._gate_ahead_ok(
        _row({"gate_tag": "v1.3.1", "reason": "r", "provenance": [{}]}), target, res) is False
    # blank reason likewise rejected by the shared predicate
    assert fp._gate_ahead_ok(
        _row({"gate_tag": "v1.3.1", "reason": " ", "provenance": ok_prov}), target, res) is False
    # empty provenance list rejected
    assert fp._gate_ahead_ok(
        _row({"gate_tag": "v1.3.1", "reason": "r", "provenance": []}), target, res) is False


def test_ownership_tally_and_line(tmp_path):
    # ADR-103: the ownership tally + [fleet-parity]-prefixed line (the management surface
    # #329 reads; harvested by the ship-gate surface too).
    fleet = {"hub-r": {"role": "hub"}}
    rows = [
        {"id": "a", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked", "path": "VISION.md"},
         "ownership": {"value": "methodology-generic", "reason": "r",
                       "provenance": [{"kind": "adr", "repo": "hub-r", "ref": "ADR-103"}]}},
        {"id": "b", "kind": "path", "tier": {"hub": "MUST"},
         "probe": {"type": "path_tracked", "path": "ARCHITECTURE.md"},
         "ownership": {"value": "project", "reason": "r", "provenance": _own_prov()}},
    ]
    m = _loaded(tmp_path, fleet, rows, inject_ownership=False)
    assert fp.ownership_tally(m) == {"methodology-generic": 1, "project": 1}
    line = fp.ownership_line(m)
    assert line.startswith("[fleet-parity] ownership")
    assert "1 methodology-generic" in line and "1 project" in line
    assert line.isascii()


def test_live_manifest_loads_with_zero_refusals():
    # ADR-103 frozen contract: the real, fully-classified manifest loads with ZERO refusals
    # (mandatory ownership on every row) -- no partially-classified manifest lands on main.
    root = Path(__file__).resolve().parents[1]
    manifest, refusals = fp.load_manifest(root / "ecosystem" / "parity-surfaces.yaml")
    assert refusals == [], [(f.surface_id, f.evidence) for f in refusals]
    assert manifest["surfaces"], "no surfaces survived the load"
    assert all(s.get("ownership", {}).get("value") in
               ("methodology-generic", "project", "conditional")
               for s in manifest["surfaces"])


def test_ruff_config_form_is_representation_only(tmp_path):
    # W3-14 / intake #12 Tier-3 convergence candidate: the FORM is evidence, never a
    # verdict -- pyproject vs .ruff.toml both read AT-PARITY with the form named.
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    row = {"id": "ruff-config-home", "kind": "path",
           "tier": {"hub": "LOCAL", "consumer": "LOCAL"}, "declared_by": "intake-12",
           "probe": {"type": "ruff_config_form"}}
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{"pyproject.toml": "[tool.ruff]\nrequired-version = '>=0.15.5'\n"}))
    cons = _init_repo(tmp_path / "cons",
                      dict(_BASE_FILES, **{".ruff.toml": "[lint]\n"}))
    manifest = _loaded(tmp_path, fleet, [row])
    findings, *_ = _run(manifest, _EMPTY_BASELINE, {"hub-r": hub, "cons": cons},
                        "hub-r")
    forms = {f.repo_id: f for f in findings if f.surface_id == "ruff-config-home"}
    assert forms["hub-r"].verdict == fp.AT_PARITY
    assert "pyproject [tool.ruff]" in forms["hub-r"].evidence
    assert forms["cons"].verdict == fp.AT_PARITY
    assert ".ruff.toml" in forms["cons"].evidence


def test_pre_deploy_rendered_and_unavailable_surfaced(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "pre": {"role": "pre-deploy"},
             "ghost": {"role": "consumer"}}
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    manifest = _loaded(tmp_path, fleet, [])
    findings, *_ = _run(manifest, _EMPTY_BASELINE,
                        {"hub-r": hub, "pre": None, "ghost": None}, "hub-r")
    verdicts_by_repo = {f.repo_id: f.verdict for f in findings
                        if f.surface_id == "fleet-membership"}
    assert verdicts_by_repo["pre"] == fp.SKIPPED_PRE_DEPLOY   # rendered, not silent
    assert verdicts_by_repo["ghost"] == fp.UNAVAILABLE        # never a silent skip


def test_fleet_registry_crosscheck_refuses_both_directions(tmp_path):
    manifest_path = _write_yaml(tmp_path / "m.yaml", _manifest(
        {"hub-r": {"role": "hub"}, "extra": {"role": "consumer"}}, []))
    manifest, _ = fp.load_manifest(manifest_path)
    registry = _write_yaml(tmp_path / "reg.yaml",
                           {"repos": {"hub-r": {}, "missing": {}}})
    hub = _init_repo(tmp_path / "hub", dict(_BASE_FILES))
    targets, findings = fp.resolve_fleet(manifest, hub, registry, tmp_path, {})
    ev = " ".join(f.evidence for f in findings)
    assert "missing" in ev and "extra" in ev
    assert all(f.verdict == fp.REFUSED for f in findings)


# ---------------------------------------------------------------------------
# Determinism + digest hygiene.
# ---------------------------------------------------------------------------


def test_determinism_two_runs_identical(tmp_path):
    fleet = {"hub-r": {"role": "hub"}, "cons": {"role": "consumer"}}
    surfaces = [{"id": "canonical-doc-vision", "kind": "path",
                 "tier": {"hub": "MUST", "consumer": "MUST"},
                 "probe": {"type": "path_tracked", "path": "VISION.md"}}]
    hub = _init_repo(tmp_path / "hub",
                     dict(_BASE_FILES, **{"pyproject.toml": _DEP_PYPROJECT}))
    # a fixture .venv keeps the dep probe off the runner's own environment
    # (hermeticity: codex 2026-07-13)
    (hub / ".venv/Lib/site-packages/pytest_xdist-3.8.0.dist-info").mkdir(parents=True)
    cons = _init_repo(tmp_path / "cons",
                      dict(_BASE_FILES, **{"straydir/f.txt": "x\n"}))
    manifest = _loaded(tmp_path, fleet, surfaces)
    f1, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub, "cons": cons}, "hub-r")
    f2, *_ = _run(manifest, _DEP_BASELINE, {"hub-r": hub, "cons": cons}, "hub-r")
    assert f1 == f2


def test_digest_is_ascii_and_atomic(tmp_path):
    fleet = {"hub-r": {"role": "hub"}}
    hub = _init_repo(tmp_path / "hub", dict(
        _BASE_FILES, **{"stråydir/f.txt": "x\n"}))  # non-ASCII divergence name
    manifest = _loaded(tmp_path, fleet, [])
    findings, targets, facts, allow, consumed = _run(
        manifest, _EMPTY_BASELINE, {"hub-r": hub}, "hub-r")
    digest = fp.render_digest(findings, targets, facts, "2026-07-13",
                              {"checker": "t", "manifest": "t", "baseline": "t"},
                              fp.unmapped_declarations(manifest, targets, allow,
                                                       consumed))
    assert digest.isascii()
    out = tmp_path / "logs" / "FLEET-PARITY.md"
    fp._atomic_write(out, digest)
    assert out.read_text(encoding="utf-8") == digest
    fp._atomic_write(out, digest + "x\n")
    assert out.read_text(encoding="utf-8").endswith("x\n")


def test_walk_returns_walkresult_shape():
    """[#337] walk() is the in-process seam reused by main() + audit.check_fleet_parity."""
    r = fp.walk("2026-07-18")
    assert isinstance(r, fp.WalkResult)
    assert r.findings and r.targets
    assert all(hasattr(f, "verdict") for f in r.findings)


def test_cli_main_emits_surface_line_after_walk_extract():
    """[#337] smoke: the walk()-extract main() still emits the surface_line and exits 0
    (proves the extract preserved main()'s output contract)."""
    root = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / "fleet_parity.py"),
         "--run-date", "2026-07-18", "--no-write", "--no-events"],
        capture_output=True, text=True, cwd=str(root))
    assert proc.returncode == 0, proc.stderr
    assert any(ln.startswith("[fleet-parity] ") and "repo(s) walked" in ln
               for ln in proc.stdout.splitlines())


# ---------------------------------------------------------------------------
# [#355] Commit-context repo resolution: GIT_DIR must never override cwd.
# ---------------------------------------------------------------------------


def test_collect_facts_ignores_inherited_git_dir(tmp_path, monkeypatch):
    """[#355] Under pre-commit, git exports GIT_DIR (+ GIT_INDEX_FILE) for the HUB, and
    GIT_DIR OVERRIDES the ``cwd=`` we pass (it beats ``-C`` too). Every probe in
    collect_facts would then read the HUB's index while labelling the facts with the
    CONSUMER's repo_id -- the exact inversion in #355: corp-monorepo reported as lacking
    INSTALL.md (it has one) and carrying docs/handoffs/ (it has none), both being the hub's
    own facts. Drives the REAL probe seam (collect_facts -> _git); the _run() helper above
    hand-builds RepoTarget and never stresses it, which is why the bug survived.

    Two-sided on purpose: asserting only "consumer file present" would still pass if facts
    were a union, and asserting only "other file absent" would pass on an empty snapshot.
    """
    # Both repos MUST be built before the monkeypatch -- this module's own _git helper is
    # unscrubbed, so an inherited GIT_DIR would break the fixture construction itself.
    consumer = _init_repo(tmp_path / "consumer", {"CONSUMER_ONLY.md": "c\n"})
    other = _init_repo(tmp_path / "other", {"OTHER_ONLY.md": "o\n"})

    # Exactly what pre-commit leaks into the hook environment.
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(other / ".git" / "index"))

    manifest = _loaded(tmp_path, {"consumer-r": {"role": "consumer"}}, [])
    manifest.pop("_refusals", None)
    target = fp.RepoTarget("consumer-r", "consumer", consumer, "")
    facts = fp.collect_facts(target, manifest, _EMPTY_BASELINE, consumer,
                             tmp_path / "nonexistent-registry.yaml")

    assert facts["git_error"] == ""
    assert "CONSUMER_ONLY.md" in facts["top_level_tracked"]
    assert "OTHER_ONLY.md" not in facts["top_level_tracked"]


def test_git_location_env_covers_gits_own_local_env_var_list():
    """Codex review [HIGH]: the first hand-written scrub tuple omitted 8 of git's 15
    repo-local vars (GIT_CONFIG, GIT_CONFIG_PARAMETERS, GIT_GRAFT_FILE, GIT_SHALLOW_FILE,
    GIT_IMPLICIT_WORK_TREE, GIT_NO_REPLACE_OBJECTS, GIT_REPLACE_REF_BASE, GIT_CONFIG_COUNT)
    -- each able to redirect config/worktree/object-graph state and so re-open #355 by a
    different door. git PUBLISHES the authoritative list, so the set is derived from it;
    this locks that contract and would catch a regression to hand-maintenance.

    Also pins the deliberate NON-scrubs: identity/transport/global-config vars a blanket
    `startswith("GIT_")` strip would have silently eaten.
    """
    scrub = fp._git_location_env()

    r = subprocess.run(["git", "rev-parse", "--local-env-vars"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode == 0:
        canonical = {ln.strip() for ln in r.stdout.split() if ln.strip()}
        assert canonical <= scrub, f"not scrubbed: {sorted(canonical - scrub)}"

    # Repo-scoping vars git does not class as local-env, but which still redirect discovery.
    assert {"GIT_CEILING_DIRECTORIES", "GIT_NAMESPACE"} <= scrub
    # The pinned fallback must itself stay a superset-in-spirit if git ever vanishes.
    assert set(fp._GIT_LOCATION_ENV_FALLBACK) <= scrub
    # Deliberately PRESERVED -- scrubbing these would break identity, transport, and the
    # config isolation that test harnesses and CI rely on.
    for keep in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_DATE", "GIT_COMMITTER_NAME",
                 "GIT_COMMITTER_DATE", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
                 "GIT_SSH_COMMAND", "GIT_TERMINAL_PROMPT"):
        assert keep not in scrub, f"{keep} must NOT be scrubbed"


# ---------------------------------------------------------------------------
# PEP 440 version comparison (intake #23 library-first; night-batch lane L-E S3).
#
# The hand-rolled _version_tuple() stripped non-digits from each dot-separated
# token, which broke prerelease ordering in FOUR distinct shapes -- witnessed live
# before the swap, not inferred:
#
#   '0.15.5'      -> (0, 15, 5)
#   '0.15.5rc1'   -> (0, 15, 51)   GREATER than the release it precedes
#   '0.15.5-beta' -> (0, 15, 5)    EQUAL to the release
#   '1.0.post1'   -> (1, 0, 1)  \  post and dev collapse to the SAME tuple,
#   '1.0.dev1'    -> (1, 0, 1)  /  and both read as '1.0.1'
#
# Dormant today only because the fleet pins ruff at an exact release -- and a
# `>=` floor is exactly where an rc build shows up. packaging implements PEP 440
# ordering and is already resolved in uv.lock (transitively via pytest), so the
# swap adds no distribution to the locked gate environment.
# ---------------------------------------------------------------------------


def test_prerelease_sorts_below_its_release():
    """The headline defect: an rc must never satisfy a floor at its own release."""
    assert fp._satisfies("0.15.5", ">=0.15.5") is True
    assert fp._satisfies("0.15.5rc1", ">=0.15.5") is False
    assert fp._satisfies("0.15.5-beta", ">=0.15.5") is False
    assert fp._satisfies("0.15.5a1", ">=0.15.5") is False


def test_post_and_dev_releases_order_correctly():
    """post > release > dev. The tuple parser collapsed all three to (1, 0, 1)."""
    assert fp._satisfies("1.0.post1", ">=1.0") is True
    assert fp._satisfies("1.0.dev1", ">=1.0") is False
    assert fp._satisfies("1.0", ">=1.0.dev1") is True


def test_operator_semantics_are_preserved():
    """The swap fixes ordering only -- >=, ==, and bare-as-minimum keep their meaning."""
    assert fp._satisfies("3.9", ">=3.8") is True
    assert fp._satisfies("3.7", ">=3.8") is False
    assert fp._satisfies("3.8", "==3.8") is True
    assert fp._satisfies("3.9", "==3.8") is False
    assert fp._satisfies("3.9", "3.8") is True      # bare == minimum
    assert fp._satisfies(None, ">=3.8") is False


def test_unparseable_version_refuses_rather_than_raises():
    """WARN-only reporter contract: garbage must never crash the fleet walk."""
    assert fp._satisfies("not-a-version", ">=1.0") is False
    assert fp._satisfies("1.0", ">=not-a-version") is False


def test_compound_specifier_is_still_refused_not_evaluated():
    """A DELIBERATE contract, not a defect -- guard it through the swap.

    _declared_ok documents it: "v1 EVALUATES single >=/==/~=/> constraints only; any
    other specifier shape (upper bounds, compounds, unparseable) is REFUSED-to-assume
    -> not ok -> WARN (codex round-3: '<3.8' must never read as unpinned)". Lane L-E
    read this as "compound specifiers silently mangled"; it is refuse-to-assume, which
    is the safe direction. Widening it to a SpecifierSet would silently overturn a
    reviewed decision, so the swap deliberately leaves it alone.
    """
    assert fp._declared_ok("foo>=1.0,<2.0", ">=1.0") is False
    assert fp._declared_ok("foo<3.8", ">=3.8") is False
    assert fp._declared_ok("foo>=3.8", ">=3.8") is True
    assert fp._declared_ok("foo", ">=3.8") is True        # unpinned: presence only
