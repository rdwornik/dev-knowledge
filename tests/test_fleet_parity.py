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


def _manifest(fleet: dict, surfaces: list, version: str = "1.0.0") -> dict:
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


def _loaded(tmp_path: Path, fleet: dict, surfaces: list):
    path = _write_yaml(tmp_path / "parity-surfaces.yaml", _manifest(fleet, surfaces))
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
