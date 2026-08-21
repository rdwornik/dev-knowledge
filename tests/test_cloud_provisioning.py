"""[#554] tests for the cloud-lane provisioning guard.

The history tests build REAL git repositories rather than mocking `subprocess`: the whole
finding this module exists for — that a clone can carry full depth and still not resolve `main` —
is a property of git's ref layout, and a mock of git cannot be wrong about it in the same way git
is. Each test therefore constructs the exact clone shape the proof lane measured and asserts the
guard's verdict on it.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import cloud_provisioning as cp  # noqa: E402


# --- fixtures: real repositories, real clone shapes ---------------------------------------


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"git {' '.join(args)} failed: {r.stderr}"
    return r


def _commit(root: Path, name: str) -> None:
    (root / name).write_text(name, encoding="utf-8")
    _git(root, "add", name)
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", name)


@pytest.fixture
def origin(tmp_path: Path) -> Path:
    """An upstream repo with a few commits on `main` and one other branch."""
    root = tmp_path / "origin"
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    for n in ("a", "b", "c"):
        _commit(root, n)
    _git(root, "branch", "worktree-lane-probe")
    return root


def _config(tmp_path: Path, **history: object) -> Path:
    """Write a minimal, schema-valid declaration and return its path."""
    body: dict[str, object] = {
        "schema": cp.CONFIG_SCHEMA,
        "history": {"disposition": "repair", "required_refs": ["main"], **history},
        "ecosystem": {"self_register": True, "self_name": ".dev-knowledge"},
        "prebuild": {
            "configured": False, "trigger": "on_configuration_change",
            "regions": ["EuropeWest"], "template_history": 1, "repository": "o/r",
        },
    }
    path = tmp_path / "provisioning.yaml"
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    return path


# --- config ---------------------------------------------------------------------------------


def test_load_config_reads_every_block(tmp_path: Path) -> None:
    cfg = cp.load_config(_config(tmp_path))
    assert cfg.history.disposition == "repair"
    assert cfg.history.required_refs == ("main",)
    assert cfg.ecosystem.self_register is True
    assert cfg.prebuild.regions == ("EuropeWest",)
    assert cfg.prebuild.template_history == 1


def test_load_config_refuses_a_foreign_schema(tmp_path: Path) -> None:
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump({"schema": "something/else"}), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match="schema"):
        cp.load_config(path)


def test_load_config_refuses_an_off_enum_disposition(tmp_path: Path) -> None:
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["history"]["disposition"] = "ignore"
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match="disposition"):
        cp.load_config(path)


@pytest.mark.parametrize(("block", "key"), [
    ("ecosystem", "self_register"),
    ("prebuild", "configured"),
])
@pytest.mark.parametrize("bad", ["false", "no", "0", 0, 1, None])
def test_load_config_refuses_a_non_boolean_where_a_boolean_is_meant(
        tmp_path: Path, block: str, key: str, bad: object) -> None:
    """`bool("false")` is True (terra HIGH round 4, 2026-08-21).

    A declaration written `configured: "false"` — quoted by hand, or by a generator that
    stringifies — silently meant the opposite. On `self_register` that authorises a tree
    mutation; on `configured` it inverts the prebuild verdict. Refusing to read the file is the
    lesser harm, and it is a could-not-look, so it raises.
    """
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body[block][key] = bad
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    with pytest.raises(cp.ProvisioningError, match=key):
        cp.load_config(path)


def test_load_config_accepts_real_yaml_booleans(tmp_path: Path) -> None:
    """The discrimination, not just the refusal: genuine booleans still load."""
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["ecosystem"]["self_register"] = False
    body["prebuild"]["configured"] = True
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    cfg = cp.load_config(path)
    assert cfg.ecosystem.self_register is False
    assert cfg.prebuild.configured is True


def test_load_config_refuses_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(cp.ProvisioningError, match="not found"):
        cp.load_config(tmp_path / "absent.yaml")


def test_the_live_declaration_loads() -> None:
    """The declaration this repo actually ships must satisfy its own loader."""
    cfg = cp.load_config()
    assert cfg.history.disposition in cp.DISPOSITIONS
    assert "main" in cfg.history.required_refs
    # Every enumerated spine walker is a file that exists — an enum naming a deleted script
    # would make `disposition: exclude` unfalsifiable.
    for instrument in cfg.history.spine_walking_instruments:
        assert (cp.REPO_ROOT / instrument).exists(), instrument


# --- history: the measured clone shapes ---------------------------------------------------


def test_full_clone_from_the_default_branch_is_already_sufficient(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "full"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert report.ok
    assert report.shallow is False
    assert report.refs["main"] == 3


def test_a_shallow_clone_is_refused(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", "file://" + str(origin).replace("\\", "/"), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("SHALLOW" in v for v in report.violations)


def test_the_measured_failure_full_depth_but_no_local_main(tmp_path: Path, origin: Path) -> None:
    """THE finding: depth is restored, `main` still does not resolve, so a spine walker errors.

    This is the shape `docs/audits/2026-08-19-technical-554-proof.md` §3 recorded — 5329 commits
    reachable and `fatal: Not a valid object name main`. Leg 2 alone reports such a clone clean.
    """
    clone = tmp_path / "branch-only"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    assert cp.is_shallow(clone) is False           # leg 2's predicate is satisfied ...
    report = cp.assess_history(clone, cfg)
    assert not report.ok                            # ... and the clone is still unusable
    assert report.refs["main"] is None
    assert any("does not resolve" in v for v in report.violations)


def test_repair_restores_the_missing_ref(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "repairable"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.repair_history(clone, cfg)
    assert report.ok, report.violations
    assert report.refs["main"] == 3
    assert any("refs/heads/main" in a for a in report.actions)


def test_repair_is_idempotent_and_says_so(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "twice"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    cp.repair_history(clone, cfg)
    second = cp.repair_history(clone, cfg)
    assert second.ok
    assert second.actions == []


def test_repair_of_a_shallow_clone_deepens_it(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "deepen"
    _git(tmp_path, "clone", "-q", "--depth", "1", "file://" + str(origin).replace("\\", "/"), str(clone))
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.repair_history(clone, cfg)
    assert report.ok, report.violations
    assert "git fetch --unshallow" in report.actions
    assert report.refs["main"] == 3


def test_a_clone_with_no_remote_cannot_be_repaired_and_that_is_exit_2(
        tmp_path: Path, origin: Path) -> None:
    """"Nothing to repair from" is could-not-look, not drift (terra HIGH, 2026-08-21).

    The first version appended a violation here, so the CLI answered 1 — telling a caller the
    clone is wrong when the honest answer is that this environment gave the guard nothing to
    work with. The 1/2 split exists precisely to keep those apart.
    """
    clone = tmp_path / "orphan"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    _git(clone, "remote", "remove", "origin")
    path = _config(tmp_path)

    with pytest.raises(cp.ProvisioningError, match="origin"):
        cp.repair_history(clone, cp.load_config(path).history)
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history", "--repair"]) == cp.EXIT_UNAVAILABLE


def test_an_unknown_required_ref_is_a_violation_not_a_crash(tmp_path: Path, origin: Path) -> None:
    """A ref no reachable clone carries IS positively observed — exit 1, not 2."""
    clone = tmp_path / "unknown-ref"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    path = _config(tmp_path, required_refs=["main", "no-such-branch"])

    report = cp.repair_history(clone, cp.load_config(path).history)
    assert not report.ok
    assert any("no-such-branch" in v for v in report.violations)
    assert report.refs["main"] == 3          # the ref that IS present still reports its length
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history", "--repair"]) == cp.EXIT_VIOLATION


# --- history: the look-alike and the stale ref ---------------------------------------------


def test_a_tag_named_main_does_not_satisfy_the_required_ref(tmp_path: Path, origin: Path) -> None:
    """`git rev-parse main` resolves a TAG called `main`; the instruments mean the BRANCH.

    Accepting the look-alike would run a spine walk over whatever that tag points at and report
    clean — the vacuous-gate class this module exists to close (terra HIGH, 2026-08-21).
    """
    clone = tmp_path / "tagged"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    _git(clone, "tag", "main", "HEAD")
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("does not resolve" in v for v in report.violations)


def test_a_stale_local_main_is_a_violation_and_repair_fast_forwards_it(
        tmp_path: Path, origin: Path) -> None:
    """A branch left behind its remote hides every spine entry in between."""
    clone = tmp_path / "stale"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _git(clone, "update-ref", "refs/heads/main", "HEAD~2")     # rewind the local branch only
    _commit(origin, "d")                                       # and move the upstream on
    _git(clone, "fetch", "-q", "origin")
    cfg = cp.load_config(_config(tmp_path)).history

    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("BEHIND" in v for v in report.violations)

    repaired = cp.repair_history(clone, cfg)
    assert repaired.ok, repaired.violations
    assert repaired.refs["main"] == 4                           # a, b, c and the new d


def test_currency_is_reported_as_UNCOMPARED_when_there_is_no_remote_tracking_ref(
        tmp_path: Path, origin: Path) -> None:
    """No remote-tracking ref means not-compared, which is not the same fact as compared-clean."""
    clone = tmp_path / "local-only"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "remote", "remove", "origin")
    path = _config(tmp_path)

    report = cp.assess_history(clone, cp.load_config(path).history)
    assert report.ok                      # present and walkable — no violation is claimed
    assert report.uncompared == ["main"]  # ... and the limit of the check is stated
    # ... and the CLI says "could not look", not "clean" (terra HIGH round 2, 2026-08-21):
    # a stale local branch is indistinguishable from a current one when there is no remote.
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history"]) == cp.EXIT_UNAVAILABLE


def test_repair_fetches_the_remote_tracking_ref_so_currency_becomes_checkable(
        tmp_path: Path, origin: Path) -> None:
    """A `--single-branch` clone carries no `origin/main`; without this the repair would fetch
    the branch and leave currency permanently UNCOMPARED, so the check could never say clean."""
    clone = tmp_path / "single"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    path = _config(tmp_path)

    report = cp.repair_history(clone, cp.load_config(path).history)
    assert report.ok, report.violations
    assert report.uncompared == []
    # The tracking ref is refreshed as a convenience for the lane; the guard's own currency
    # answer comes from `ls-remote`, which is why the check below can succeed either way.
    assert cp.remote_ref(clone, "main") is not None
    assert cp.main(["--root", str(clone), "--config", str(path), "history"]) == cp.EXIT_OK


def test_a_DIVERGED_local_main_is_refused_and_never_force_updated(
        tmp_path: Path, origin: Path) -> None:
    """THE data-loss guard (terra CRITICAL, 2026-08-21).

    An earlier version asked only "is the remote an ancestor of local?" and treated every no as
    BEHIND, then force-fetched over it. A clone carrying an unpushed commit on local `main` would
    have lost the only reference to it the moment `origin/main` also advanced.
    """
    clone = tmp_path / "diverged"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _git(clone, "checkout", "-q", "main")
    _commit(clone, "local-only-work")                 # an unpushed commit on local main
    local_tip = _git(clone, "rev-parse", "refs/heads/main").stdout.strip()
    _git(clone, "checkout", "-q", "worktree-lane-probe")
    _commit(origin, "upstream-work")                  # and the upstream advances too
    _git(clone, "fetch", "-q", "origin")
    cfg = cp.load_config(_config(tmp_path)).history

    assert cp.ref_status(clone, "main", cp.remote_ref(clone, "main")) == cp.REF_DIVERGED
    report = cp.repair_history(clone, cfg)
    assert not report.ok
    assert any("DIVERGED" in v for v in report.violations)
    # The commit is still reachable: the repair refused rather than clobbering the ref.
    assert _git(clone, "rev-parse", "refs/heads/main").stdout.strip() == local_tip


def test_the_READ_ONLY_check_detects_a_stale_clone_without_fetching_anything(
        tmp_path: Path, origin: Path) -> None:
    """THE gate's soundness (terra HIGH round 4, 2026-08-21).

    Upstream advances; the clone never fetches, so its local `main` AND its cached
    `origin/main` are stale together — comparing the two finds them equal and reports clean.
    `--gate` runs exactly this read-only path on every container start, so a cache-based
    currency check meant a resumed container could pass while the spine walkers missed every
    commit added since. The comparison now asks the remote itself.
    """
    clone = tmp_path / "cached-stale"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "worktree-lane-probe")
    _commit(origin, "d")
    _commit(origin, "e")

    # The clone has fetched nothing: both of its refs still say three commits.
    assert cp.spine_length(clone, "main") == 3
    assert cp.remote_ref(clone, "main") == _git(clone, "rev-parse", "refs/heads/main").stdout.strip()

    path = _config(tmp_path)
    cfg = cp.load_config(path).history
    report = cp.assess_history(clone, cfg)            # read-only, and it still catches it
    assert not report.ok
    assert any("BEHIND" in v for v in report.violations)
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history"]) == cp.EXIT_VIOLATION

    repaired = cp.repair_history(clone, cfg)
    assert repaired.ok, repaired.violations
    assert repaired.refs["main"] == 5


def test_an_unreachable_origin_is_exit_2_not_a_missing_branch(
        tmp_path: Path, origin: Path) -> None:
    """A transport failure is could-not-look; only `ls-remote` saying so means "no such branch".

    Before round 3 ANY failed fetch was reported as "origin has no such branch", so an auth
    failure, a DNS failure or an unreachable host all became exit 1 — a positively observed
    configuration violation asserted from a network error.
    """
    clone = tmp_path / "unreachable"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    _git(clone, "remote", "set-url", "origin", str(tmp_path / "does-not-exist"))
    path = _config(tmp_path)

    with pytest.raises(cp.ProvisioningError):
        cp.repair_history(clone, cp.load_config(path).history)
    assert cp.main(["--root", str(clone), "--config", str(path),
                    "history", "--repair"]) == cp.EXIT_UNAVAILABLE


def test_a_remote_tip_reachable_only_via_a_SECOND_parent_is_refused_not_called_current(
        tmp_path: Path, origin: Path) -> None:
    """Generic ancestry is not first-parent coverage (terra HIGH round 5, 2026-08-21).

    Local `main` MERGES the upstream tip as a second parent, so `merge-base --is-ancestor` says
    it is contained — while `git log --first-parent main`, which is what every instrument in
    `spine_walking_instruments` runs, never traverses it. Reporting that clean is precisely the
    vacuous-gate condition this module exists to prevent.
    """
    clone = tmp_path / "second-parent"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "checkout", "-q", "-b", "side")
    _commit(clone, "side-work")
    _commit(origin, "upstream-work")
    _git(clone, "fetch", "-q", "origin")
    upstream_tip = _git(clone, "rev-parse", "refs/remotes/origin/main").stdout.strip()
    # Rebuild local main as: side-work, then a merge whose SECOND parent is the upstream tip.
    _git(clone, "branch", "-f", "main", "side")
    _git(clone, "checkout", "-q", "main")
    _git(clone, "-c", "user.name=t", "-c", "user.email=t@t",
         "merge", "--no-ff", "-q", "-m", "merge upstream", upstream_tip)
    _git(clone, "checkout", "-q", "side")

    assert cp._is_ancestor(clone, upstream_tip, "refs/heads/main")          # contained ...
    assert not cp._on_first_parent_chain(clone, "refs/heads/main", upstream_tip)  # ... off-spine
    assert cp.ref_status(clone, "main", upstream_tip) == cp.REF_OFF_SPINE

    cfg = cp.load_config(_config(tmp_path)).history
    report = cp.assess_history(clone, cfg)
    assert not report.ok
    assert any("SECOND parent" in v for v in report.violations)


def test_a_local_main_AHEAD_of_origin_is_current_not_a_violation(
        tmp_path: Path, origin: Path) -> None:
    """Ahead is the normal workstation state and hides nothing from a spine walk."""
    clone = tmp_path / "ahead"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _commit(clone, "extra")
    cfg = cp.load_config(_config(tmp_path)).history

    assert cp.ref_status(clone, "main", cp.remote_ref(clone, "main")) == cp.REF_CURRENT
    assert cp.assess_history(clone, cfg).ok


# --- history: the exclusion disposition ---------------------------------------------------


def test_exclude_disposition_repairs_nothing_and_exits_clean(tmp_path: Path, origin: Path,
                                                             caplog: pytest.LogCaptureFixture) -> None:
    clone = tmp_path / "excluded"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    path = _config(tmp_path, disposition="exclude",
                   spine_walking_instruments=["scripts/validate_no_ff.py"])

    rc = cp.main(["--root", str(clone), "--config", str(path), "history", "--repair"])
    assert rc == cp.EXIT_OK
    assert "OUT OF SCOPE" in caplog.text
    assert "scripts/validate_no_ff.py" in caplog.text
    assert not cp.ref_resolves(clone, "main")     # it really did not repair


# --- exit codes: looked-and-failed vs could-not-look --------------------------------------


def test_history_check_exits_1_on_a_real_violation(tmp_path: Path, origin: Path) -> None:
    clone = tmp_path / "violation"
    _git(tmp_path, "clone", "-q", "--single-branch", "--branch", "worktree-lane-probe",
         str(origin), str(clone))
    path = _config(tmp_path)
    assert cp.main(["--root", str(clone), "--config", str(path), "history"]) == cp.EXIT_VIOLATION


def test_an_unreadable_declaration_exits_2_not_1(tmp_path: Path) -> None:
    """Could-not-look and looked-and-failed must not share an exit code (F4)."""
    assert cp.main(["--config", str(tmp_path / "absent.yaml"), "history"]) == cp.EXIT_UNAVAILABLE


def test_history_check_exits_0_on_this_repo() -> None:
    """The live checkout satisfies its own precondition — the guard is not vacuously red."""
    assert cp.main(["--quiet", "history"]) == cp.EXIT_OK


# --- ecosystem -----------------------------------------------------------------------------


def test_registered_repos_counts_state_yaml_directories(tmp_path: Path) -> None:
    eco = tmp_path / "ecosystem"
    (eco / "alpha").mkdir(parents=True)
    (eco / "alpha" / "state.yaml").write_text("name: alpha\n", encoding="utf-8")
    (eco / "beta").mkdir()                       # a directory with no state.yaml does not count
    (eco / "schema").mkdir()
    assert cp.registered_repos(tmp_path) == ["alpha"]


def test_registered_repos_on_a_tree_with_no_ecosystem_dir(tmp_path: Path) -> None:
    assert cp.registered_repos(tmp_path) == []


def test_ecosystem_check_reports_the_containers_symptom(tmp_path: Path) -> None:
    """A fresh clone: nothing registered, and `--check` says so rather than repairing."""
    (tmp_path / "ecosystem").mkdir()
    path = _config(tmp_path)
    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem"]) == cp.EXIT_VIOLATION


def test_ecosystem_check_passes_when_something_is_registered(tmp_path: Path) -> None:
    eco = tmp_path / "ecosystem" / ".dev-knowledge"
    eco.mkdir(parents=True)
    (eco / "state.yaml").write_text("name: .dev-knowledge\n", encoding="utf-8")
    path = _config(tmp_path)
    assert cp.main(["--root", str(tmp_path), "--config", str(path), "ecosystem"]) == cp.EXIT_OK


def test_ecosystem_repair_success_path_registers_and_is_idempotent(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The path that ACTUALLY fixes a fresh container, exercised end to end (terra HIGH).

    Previously only detection, already-registered and self_register:false were covered, so
    deleting the code that writes `ecosystem/<name>/state.yaml` would have left the suite green
    while every fresh Codespace still failed provisioning. The seeder is stubbed to keep the test
    off a full `audit_repo` run; what it stands in for is pinned by the test below.
    """
    (tmp_path / "ecosystem").mkdir()
    seeded: list[Path] = []

    def _fake_seed(root: Path, name: str) -> str:
        target = root / "ecosystem" / name / "state.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"name: {name}\n", encoding="utf-8")
        seeded.append(target)
        return str(target)

    monkeypatch.setattr(cp, "seed_self_registration", _fake_seed)
    path = _config(tmp_path)

    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem", "--repair"]) == cp.EXIT_OK
    assert (tmp_path / "ecosystem" / ".dev-knowledge" / "state.yaml").exists()
    assert cp.registered_repos(tmp_path) == [".dev-knowledge"]

    # Second run: already registered, so the seeder is not called again.
    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem", "--repair"]) == cp.EXIT_OK
    assert len(seeded) == 1


def test_ecosystem_repair_reports_a_seed_that_did_not_land(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A seeder that returns a path but writes nothing must not be reported as success."""
    (tmp_path / "ecosystem").mkdir()
    monkeypatch.setattr(cp, "seed_self_registration", lambda root, name: "nowhere/state.yaml")
    assert cp.main(["--root", str(tmp_path), "--config", str(_config(tmp_path)),
                    "ecosystem", "--repair"]) == cp.EXIT_VIOLATION


def test_seed_self_registration_writes_under_the_REQUESTED_root(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The destination is forced, not assumed (terra CRITICAL round 5, 2026-08-21).

    `audit.save_state` resolves through the module-level `audit.ECOSYSTEM_DIR`, derived from
    `audit.py`'s own location — and `import audit` returns whatever `sys.modules` already holds.
    So `--root <another clone>` would have written that clone's audit state over THIS checkout's
    `state.yaml`, while the function returned a root-relative path claiming otherwise.

    `save_state` is deliberately NOT stubbed here: stubbing the writer would test the claim
    rather than the write.
    """
    sys.path.insert(0, str(cp.REPO_ROOT / "scripts"))
    import audit  # noqa: PLC0415

    root = tmp_path / "other-clone"
    (root / "scripts").mkdir(parents=True)
    monkeypatch.setattr(
        audit, "audit_repo",
        lambda name, path, run_date: audit.RepoState(
            name=name, path=str(path), last_audit=run_date.isoformat(), findings=[]))
    hub_state = audit.ECOSYSTEM_DIR

    written = cp.seed_self_registration(root, ".dev-knowledge")

    assert Path(written) == root / "ecosystem" / ".dev-knowledge" / "state.yaml"
    assert (root / "ecosystem" / ".dev-knowledge" / "state.yaml").exists()
    assert audit.ECOSYSTEM_DIR == hub_state          # restored, not left pointing elsewhere


def test_seed_self_registration_refuses_when_the_state_did_not_land(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A return value is a claim; the file's existence is the proof."""
    stub = types.ModuleType("audit")
    stub.ECOSYSTEM_DIR = tmp_path / "ecosystem"
    stub.audit_repo = lambda name, path, run_date: object()
    stub.save_state = lambda state: None             # writes nothing at all
    monkeypatch.setitem(sys.modules, "audit", stub)
    (tmp_path / "scripts").mkdir()

    with pytest.raises(cp.ProvisioningError, match="did not land"):
        cp.seed_self_registration(tmp_path, ".dev-knowledge")


def test_seed_self_registration_uses_audit_repo_and_save_state_only(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Pins the REUSE claim: `audit_repo` + `save_state`, and none of `audit.py repo`'s extras.

    `audit.py repo` also appends history, writes a dated report under `docs/audits/` and commits
    its outputs — three things a provisioning step must never do to a container's tree. The
    module docstring says so; this asserts it.
    """
    calls: list[str] = []
    fake_state = object()

    def _save(state: object) -> None:
        calls.append("save_state")
        target = stub.ECOSYSTEM_DIR / ".dev-knowledge" / "state.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("name: .dev-knowledge\n", encoding="utf-8")

    stub = types.ModuleType("audit")
    stub.ECOSYSTEM_DIR = tmp_path / "ecosystem"
    stub.audit_repo = lambda name, path, run_date: (calls.append("audit_repo"), fake_state)[1]
    stub.save_state = _save
    for forbidden in ("append_history", "generate_report", "write_report",
                      "_commit_routine_outputs"):
        stub.__dict__[forbidden] = lambda *a, **k: calls.append(forbidden)
    monkeypatch.setitem(sys.modules, "audit", stub)

    (tmp_path / "scripts").mkdir()
    written = cp.seed_self_registration(tmp_path, ".dev-knowledge")

    assert calls == ["audit_repo", "save_state"]
    assert written.endswith("state.yaml")


def test_ecosystem_repair_refuses_when_self_register_is_off(tmp_path: Path) -> None:
    (tmp_path / "ecosystem").mkdir()
    path = _config(tmp_path)
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["ecosystem"]["self_register"] = False
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    assert cp.main(["--root", str(tmp_path), "--config", str(path),
                    "ecosystem", "--repair"]) == cp.EXIT_VIOLATION


# --- prebuild -------------------------------------------------------------------------------


def _declare_configured(path: Path, value: bool) -> Path:
    body = yaml.safe_load(path.read_text(encoding="utf-8"))
    body["prebuild"]["configured"] = value
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    return path


def test_prebuild_has_exactly_one_falsifiable_quadrant(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The whole verdict table, asserted as a table so the asymmetry cannot drift back."""
    cases = [
        # (declared configured, availability values, expected exit)
        (True,  ["ready"], cp.EXIT_OK),
        (False, ["ready"], cp.EXIT_VIOLATION),      # the ONLY exit-1 quadrant
        (True,  ["none"], cp.EXIT_UNAVAILABLE),
        (False, ["none"], cp.EXIT_UNAVAILABLE),
        (True,  [None], cp.EXIT_UNAVAILABLE),
        (False, [None], cp.EXIT_UNAVAILABLE),
    ]
    for declared, values, expected in cases:
        monkeypatch.setattr(cp, "_gh_machines", lambda repo, ref, loc, v=values: [
            {"prebuild_availability": item} for item in v])
        path = _declare_configured(_config(tmp_path), declared)
        assert cp.main(["--config", str(path), "prebuild"]) == expected, (declared, values)


def test_prebuild_not_configured_is_INDETERMINATE_not_clean(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A null availability cannot confirm "no prebuild is configured" (terra HIGH, 2026-08-21).

    The endpoint answers availability for a branch and region; an unrun or expired prebuild
    reads null too. Exiting 0 here would report a verification the reading cannot support.
    """
    monkeypatch.setattr(cp, "_gh_machines", lambda repo, ref, loc: [
        {"name": "basicLinux32gb", "prebuild_availability": "none"}])
    path = _declare_configured(_config(tmp_path), False)
    assert cp.main(["--config", str(path), "prebuild"]) == cp.EXIT_UNAVAILABLE


def test_prebuild_declared_configured_and_available_is_clean(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cp, "_gh_machines", lambda repo, ref, loc: [
        {"name": "basicLinux32gb", "prebuild_availability": "ready"}])
    path = _declare_configured(_config(tmp_path), True)
    assert cp.main(["--config", str(path), "prebuild"]) == cp.EXIT_OK


def test_prebuild_declared_NOT_configured_but_available_is_drift(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The quadrant round 1 missed: availability PROVES a configuration exists, so a declaration
    denying one is observed drift (exit 1), not an unanswerable question (exit 2)."""
    monkeypatch.setattr(cp, "_gh_machines", lambda repo, ref, loc: [
        {"name": "basicLinux32gb", "prebuild_availability": "ready"}])
    path = _declare_configured(_config(tmp_path), False)
    assert cp.main(["--config", str(path), "prebuild"]) == cp.EXIT_VIOLATION


def test_prebuild_none_availability_can_never_refute_a_configuration_claim(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`none` is about AVAILABILITY, so it refutes nothing (terra HIGH round 5, 2026-08-21).

    An earlier version returned exit 1 for declared-configured + `none` — asserting observed
    drift from a reading the module's own docstring says cannot support it, since a configured
    prebuild that has not run or has expired reads `none` too.
    """
    monkeypatch.setattr(cp, "_gh_machines", lambda repo, ref, loc: [
        {"name": "basicLinux32gb", "prebuild_availability": "none"}])
    for declared in (True, False):
        path = _declare_configured(_config(tmp_path), declared)
        assert cp.main(["--config", str(path), "prebuild"]) == cp.EXIT_UNAVAILABLE


def test_prebuild_query_carries_the_declared_ref_and_region(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`prebuild_availability` is answered in the context of a ref and a location; asking
    without them asks a different question, so the declared values must reach the call."""
    seen: dict[str, str] = {}

    def _spy(repo: str, ref: str, loc: str) -> list[dict]:
        seen.update(repo=repo, ref=ref, loc=loc)
        return [{"prebuild_availability": "ready"}]

    monkeypatch.setattr(cp, "_gh_machines", _spy)
    cp.main(["--config", str(_declare_configured(_config(tmp_path), True)), "prebuild"])
    assert seen == {"repo": "o/r", "ref": "main", "loc": "EuropeWest"}


def test_prebuild_cannot_look_exits_2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(repo: str, ref: str, loc: str) -> list[dict]:
        raise cp.ProvisioningError("`gh` is not on PATH")

    monkeypatch.setattr(cp, "_gh_machines", _boom)
    path = _declare_configured(_config(tmp_path), True)
    assert cp.main(["--config", str(path), "prebuild"]) == cp.EXIT_UNAVAILABLE


@pytest.mark.parametrize(("values", "expected"), [
    (["ready", "none"], cp.PREBUILD_CONFIRMED),        # any confirming machine settles it
    (["in_progress"], cp.PREBUILD_CONFIRMED),          # building IS a configuration
    (["none", "none"], cp.PREBUILD_NONE),              # every machine says unavailable
    ([None, "none"], cp.PREBUILD_UNKNOWN),             # `null` is not an answer
    ([None], cp.PREBUILD_UNKNOWN),
    (["something-new"], cp.PREBUILD_UNKNOWN),          # an unrecognised value is not evidence
    ([], cp.PREBUILD_UNKNOWN),                         # no machines: nothing was read
])
def test_prebuild_state_parses_the_documented_enum(
        values: list, expected: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """GitHub's enum is `none` / `ready` / `in_progress` / null (terra HIGH round 3, 2026-08-21).

    The first version treated ANY non-null value as available, so `none` — the clearest possible
    negative — read as a prebuild being present. Earlier tests used the fictional value `"blob"`,
    which is exactly why they could not catch it.
    """
    monkeypatch.setattr(cp, "_gh_machines",
                        lambda repo, ref, loc: [{"prebuild_availability": v} for v in values])
    assert cp.prebuild_state("o/r", "main", "EuropeWest") == expected


def test_prebuild_null_availability_is_indeterminate_whatever_is_declared(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`null` must not become drift: configured + null was exiting 1 before round 3."""
    monkeypatch.setattr(cp, "_gh_machines",
                        lambda repo, ref, loc: [{"prebuild_availability": None}])
    for declared in (True, False):
        path = _declare_configured(_config(tmp_path), declared)
        assert cp.main(["--config", str(path), "prebuild"]) == cp.EXIT_UNAVAILABLE


# --- the shipped devcontainer surface ------------------------------------------------------


def _uncommented(text: str, marker: str) -> str:
    """`text` with whole-line comments dropped.

    Both files below explain the defect they closed by QUOTING it, so a naive substring search
    finds the retired declaration in the prose that records its retirement. Stripping comment
    lines is what makes these assertions about the code rather than about the commentary.
    """
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith(marker))


def _devcontainer() -> dict:
    """The shipped `devcontainer.json`, parsed. JSONC: whole-line `//` comments are stripped.

    Parsing rather than grepping is the point — a structurally invalid file is a container that
    never builds, and no string search notices that.
    """
    text = (cp.REPO_ROOT / ".devcontainer" / "devcontainer.json").read_text(encoding="utf-8")
    return json.loads(_uncommented(text, "//"))


def test_devcontainer_json_is_valid_and_wires_every_lifecycle_stage() -> None:
    """The execution surface, pinned (terra HIGH round 2, 2026-08-21).

    The only devcontainer assertion before this one checked that a RETIRED declaration was
    absent — so deleting every lifecycle hook, or breaking the JSONC, left the suite green while
    a fresh Codespace and `devcontainer up` both provisioned nothing at all.
    """
    d = _devcontainer()
    # onCreateCommand is the half a prebuild bakes; postCreateCommand is the half it never does.
    assert d["onCreateCommand"] == "bash .devcontainer/provision.sh"
    assert d["postCreateCommand"] == "bash .devcontainer/provision.sh"
    # The refusal runs on EVERY start, and `waitFor` is what stops a session attaching before it.
    assert d["postStartCommand"] == "bash .devcontainer/provision.sh --gate"
    assert d["waitFor"] == "postStartCommand"
    # The reachability leg: without sshd, `gh codespace ssh` and `logs` both refuse.
    assert "ghcr.io/devcontainers/features/sshd:1" in d["features"]


def test_devcontainer_json_no_longer_declares_the_unexpandable_stamp() -> None:
    """The `${containerEnv:HOME}` defect: a self-referencing containerEnv value that Codespaces
    passed through literally, so provisioning created a directory of that name inside the tree.
    """
    text = (cp.REPO_ROOT / ".devcontainer" / "devcontainer.json").read_text(encoding="utf-8")
    code = _uncommented(text, "//")
    assert "containerEnv" not in code
    assert "DEV_KNOWLEDGE_PROVISION_STAMP" not in code


def _usable_bash() -> str | None:
    """A bash that actually RUNS, not merely one that resolves.

    `shutil.which("bash")` on Windows happily returns the WindowsApps app-execution alias, which
    exists as a file and then fails (or opens the Store) when invoked — so a which-only skipif
    turned a host-configuration quirk into a red suite (terra HIGH round 3, 2026-08-21). This
    probes once and caches nothing: the cost is one process.
    """
    found = shutil.which("bash")
    if found is None:
        return None
    try:
        r = subprocess.run([found, "-c", "exit 0"], capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return found if r.returncode == 0 else None


def test_provision_sh_actually_refuses_an_unexpanded_stamp_path(tmp_path: Path) -> None:
    """EXECUTES the refusal instead of grepping for it (terra HIGH, 2026-08-21).

    The first version of this test searched `provision.sh` for two strings, so deleting the
    `exit 1` from the case branch left it green while the script happily created the junk
    directory again. This runs the script with the poisoned variable and asserts the two things
    that actually matter: a non-zero exit, and NOTHING created on disk.
    """
    bash = _usable_bash()
    if bash is None:
        pytest.skip("no usable bash on PATH")
    stamp = "${containerEnv:HOME}/.dev-knowledge-provision-stamp"
    env = {**os.environ, "DEV_KNOWLEDGE_PROVISION_STAMP": stamp, "HOME": str(tmp_path)}
    r = subprocess.run(
        [bash, str(cp.REPO_ROOT / ".devcontainer" / "provision.sh")],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=120,
    )
    assert r.returncode != 0, r.stdout
    assert "UNEXPANDED" in r.stderr
    # The whole point: the poisoned path is refused BEFORE anything is created from it.
    assert not list(tmp_path.iterdir()), sorted(p.name for p in tmp_path.iterdir())


def _run_provision(tmp_path: Path, *args: str, stamp: str | None = None) -> subprocess.CompletedProcess:
    bash = _usable_bash()
    if bash is None:
        pytest.skip("no usable bash on PATH")
    env = {**os.environ, "HOME": str(tmp_path)}
    env.pop("DEV_KNOWLEDGE_PROVISION_STAMP", None)
    if stamp is not None:
        env["DEV_KNOWLEDGE_PROVISION_STAMP"] = stamp
    return subprocess.run(
        [bash, str(cp.REPO_ROOT / ".devcontainer" / "provision.sh"), *args],
        cwd=cp.REPO_ROOT, env=env, capture_output=True, text=True, timeout=300,
    )


def test_the_gate_EXECUTES_and_refuses_a_container_with_no_stamp(tmp_path: Path) -> None:
    """`--gate`'s first refusal, run rather than described (terra HIGH round 4, 2026-08-21).

    This is the shape a RESUMED container takes when the image predates provisioning, and it is
    the one that fired for real in a Codespace on 2026-08-21 after a full rebuild wiped `$HOME`.
    It reaches no `uv` call, so it needs no shims.
    """
    r = _run_provision(tmp_path, "--gate")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "no provisioning stamp" in r.stderr


def test_the_gate_EXECUTES_and_refuses_a_stamp_from_a_foreign_schema(tmp_path: Path) -> None:
    (tmp_path / ".dev-knowledge-provision-stamp").write_text(
        "schema=some-other-tool/9\nuv_pin=0.0.0\npython_pin=0.0\n", encoding="utf-8")
    r = _run_provision(tmp_path, "--gate")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "stamp schema" in r.stderr


def test_the_gate_EXECUTES_and_refuses_a_stamp_whose_pin_has_moved(tmp_path: Path) -> None:
    """THE staleness leg: the repo's uv pin moved and this container still runs the old one."""
    (tmp_path / ".dev-knowledge-provision-stamp").write_text(
        "schema=dev-knowledge-provision/1\nuv_pin=0.0.1-not-the-pin\npython_pin=3.12.10\n",
        encoding="utf-8")
    r = _run_provision(tmp_path, "--gate")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "the pin moved" in r.stderr


# NOT COVERED HERE, and stated rather than left for a reader to discover: no test executes a
# SUCCESSFUL end-to-end provisioning run. Doing so needs shims for `uv` (five subcommands),
# `curl` and a whole fake repo, and a harness that elaborate is more likely to test itself than
# the script. What stands in for it is live evidence, not an assumption: ARTIFACT-lane-554.md
# records three real Codespace runs, including a full rebuild in which `onCreateCommand`,
# `postCreateCommand` and `postStartCommand` each fired and each leg printed its own OK line.


def test_provision_sh_help_still_works_so_the_refusal_is_not_a_blanket_abort(tmp_path: Path) -> None:
    """The guard must refuse a poisoned path, not every invocation. Pins the discrimination."""
    bash = _usable_bash()
    if bash is None:
        pytest.skip("no usable bash on PATH")
    env = {**os.environ, "HOME": str(tmp_path)}
    env.pop("DEV_KNOWLEDGE_PROVISION_STAMP", None)
    r = subprocess.run(
        [bash, str(cp.REPO_ROOT / ".devcontainer" / "provision.sh"), "--help"],
        cwd=cp.REPO_ROOT, env=env, capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, r.stderr
    assert "--gate" in r.stdout


def _guard_invocations() -> list[list[str]]:
    """Every `cloud_provisioning.py ...` argument list `provision.sh` actually runs."""
    text = (cp.REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8")
    calls = []
    for line in _uncommented(text, "#").splitlines():
        _, sep, tail = line.partition("scripts/cloud_provisioning.py")
        if not sep:
            continue
        # Cut the shell's own tail: `|| CHANGED=...`, `|| rc=$?`, a line-continuation backslash.
        tail = tail.split("||", 1)[0].rstrip().removesuffix("\\")
        calls.append(tail.split())
    return calls


def test_every_guard_invocation_in_provision_sh_parses() -> None:
    """WITNESSED 2026-08-21, in the container: the gate called `... history --quiet`, argparse
    put `--quiet` on the PARENT parser, and the gate died with `unrecognized arguments: --quiet`
    and REFUSED a perfectly good container. A gate that fails closed on its own typo is worse
    than no gate, and no unit test caught it because every test called `main()` with a hand-written
    argument list. This one reads the argument lists the shell actually uses.
    """
    calls = _guard_invocations()
    assert len(calls) >= 4, calls
    parser = cp.build_parser()
    for argv in calls:
        parser.parse_args(argv)          # SystemExit here IS the failure


def test_the_gate_never_syncs_the_environment_it_is_asserting() -> None:
    """`uv run` SYNCS by default, so the assert-only gate would silently build the very venv it
    exists to refuse — and the venv it built need not carry the `analytics` group (terra HIGH
    round 2, 2026-08-21). Every `uv run` in the file must therefore be `--no-sync`, and the gate
    must assert the environment read-only with `uv sync --check` first.
    """
    code = _uncommented(
        (cp.REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8"), "#")
    assert "uv run --locked" not in code
    assert code.count("uv run ") == code.count("uv run --no-sync ")
    gate_body = code.split("gate() {", 1)[1]
    assert "uv sync --locked --group analytics --check" in gate_body
    assert gate_body.index("uv sync --locked --group analytics --check") < \
           gate_body.index("uv run --no-sync")


def test_environment_repairs_are_counted_by_c1() -> None:
    """A container that rebuilt a missing `.venv` still printed "nothing changed"."""
    code = _uncommented(
        (cp.REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8"), "#")
    body = code.split("sync_environment() {", 1)[1]
    assert "uv python find" in body
    assert "uv sync --locked --group analytics --check" in body
    assert body.count("CHANGED=$((CHANGED + 1))") >= 2


def test_provision_sh_asks_before_repairing_so_c1_accounting_stays_honest() -> None:
    """A run that repairs must not report itself idempotent.

    Witnessed 2026-08-21: the first live container run seeded a state.yaml and still printed
    "DONE — idempotent: nothing changed". Each new leg now runs the read-only check first and
    bumps CHANGED on its verdict.
    """
    text = (cp.REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8")
    code = _uncommented(text, "#")
    for subcommand in ("history", "ecosystem"):
        assert f"cloud_provisioning.py --quiet {subcommand} || CHANGED=" in code
        assert code.index(f"cloud_provisioning.py --quiet {subcommand}") < \
               code.index(f"cloud_provisioning.py {subcommand} --repair")


def test_provision_sh_runs_the_history_repair_before_arming_hooks() -> None:
    """B1's ordering claim is checkable, so it is checked rather than asserted in prose."""
    text = (cp.REPO_ROOT / ".devcontainer" / "provision.sh").read_text(encoding="utf-8")
    body = _uncommented(text.split("main() {", 1)[1], "#")
    calls = [ln.strip() for ln in body.splitlines() if ln.strip().startswith("leg")
             or ln.strip() in ("sync_environment", "smoke_gate_liveness", "write_stamp")]
    # The FULL sequence, not just the two new legs (terra HIGH round 3, 2026-08-21): the earlier
    # version asserted only relative order, so deleting `leg1_uv`, `leg2_unshallow` or
    # `write_stamp` from main() left the suite green while a fresh container provisioned nothing.
    assert calls == [
        "leg1_uv", "leg2_unshallow", "sync_environment", "leg2b_history", "leg5_ecosystem",
        "leg3_hooks", "smoke_gate_liveness", "write_stamp",
    ]
    # Honest limit, stated so nobody reads more into this than it does: this asserts the CALL
    # LIST, not the behaviour of each leg. Executing the whole script needs git, curl and uv
    # shims; what stands in for that here is the live container evidence in ARTIFACT-lane-554.md,
    # where every one of these legs is shown firing in a real Codespace lifecycle.
