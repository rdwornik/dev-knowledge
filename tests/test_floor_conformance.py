"""Layer-1 (hermetic, offline) tests for the #230 floor conformance harness (ADR-93).

Builds a SYNTHETIC consumer in a throwaway git repo, arms it with the REAL carriers
(FloorCarrier + PrecommitCarrier), then runs deploy/floor_conformance.py's functional
suite end-to-end. This proves the armed loop FUNCTIONS — the guard fails loud on a
poisoned floor at both legs, the git hook auto-arms, a real task flows through the
gate — not merely that files are present.

Offline + deterministic (plan C.5): the fixture's .pre-commit-config.yaml carries ONLY
the floor-hash-verify local hook (language: system — no env, no network); core.autocrlf
is off + a .gitattributes eol=lf pin; PRE_COMMIT_HOME is a per-run temp dir. No network,
no real consumer repos.

The operator-run Layer-2 pass against the REAL ai-council (the #226 hard-metric) is the
same suite via `python deploy/floor_conformance.py --consumer ../ai-council`; it is built
but NOT run here (step 5).
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_floor as cf  # noqa: E402
import carrier_precommit as cp  # noqa: E402
import floor_conformance as fc  # noqa: E402

pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("pre_commit") is None,
    reason="pre-commit not installed — the commit-time leg cannot be exercised offline",
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_MANIFEST = _REPO_ROOT / "deploy" / "manifest-v1.0.0.yaml"

_FLOOR_TARGET = {
    "floor_path": ".claude/CLAUDE-FLOOR.md",
    "sidecar_path": ".claude/CLAUDE-FLOOR.md.sha256",
}

# The floor-hash-verify local hook, sourced from the manifest (single source of truth).
_FLOOR_LOCAL_HOOK = next(
    h
    for c in yaml.safe_load(_MANIFEST.read_text(encoding="utf-8"))["carriers"]
    if c["id"] == "precommit"
    for h in c["target"]["required_local_hooks"]
    if h["id"] == "floor-hash-verify"
)
# Offline precommit target: ONLY the floor local hook (no ruff/hub — those need network).
_PC_LOCAL_TARGET = {
    "config_path": ".pre-commit-config.yaml",
    "required_local_hooks": [_FLOOR_LOCAL_HOOK],
}


def _git(args: list[str], cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    full = {**os.environ, **(env or {})}
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=full,
    )


@pytest.fixture
def armed_consumer(tmp_path: Path) -> Path:
    """A throwaway git repo armed by the real carriers + an initial committed state."""
    tree = tmp_path / "consumer"
    tree.mkdir()
    # Deterministic git: default branch main, an identity, autocrlf off, LF pin.
    _git(["-c", "init.defaultBranch=main", "init", "-q"], tree)
    _git(["config", "user.email", "conformance@example.com"], tree)
    _git(["config", "user.name", "Conformance"], tree)
    _git(["config", "commit.gpgsign", "false"], tree)
    _git(["config", "core.autocrlf", "false"], tree)
    (tree / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8", newline="\n")
    # A pre-existing CLAUDE.md so the @-include is inserted (not created bare).
    (tree / "CLAUDE.md").write_text(
        "---\nlast_reviewed: 2026-07-01\n---\n\n# CLAUDE.md — Consumer\nBody.\n",
        encoding="utf-8", newline="\n",
    )
    # Arm via the REAL carriers (this is what the deploy tool runs).
    cf.FloorCarrier(tree).apply(_FLOOR_TARGET)
    cp.PrecommitCarrier(tree).apply(_PC_LOCAL_TARGET)
    # Commit the armed (trackable) state so the floor is tracked for the commit legs.
    _git(["add", "-A"], tree)
    _git(["commit", "-q", "-m", "chore: arm floor"], tree)
    return tree


@pytest.fixture
def pc_env(tmp_path: Path) -> dict:
    """A per-run PRE_COMMIT_HOME so pre-commit's cache never pollutes ~ (total teardown)."""
    return {"PRE_COMMIT_HOME": str(tmp_path / ".pc-home")}


# ---------------------------------------------------------------------------
# The whole suite passes on a correctly-armed consumer.
# ---------------------------------------------------------------------------


def test_full_suite_passes_on_armed_consumer(armed_consumer, pc_env):
    passed = fc.run_conformance(armed_consumer, pc_env)
    assert len(passed) == 8  # every property proven, not just files-present


# ---------------------------------------------------------------------------
# Each property, isolated (so a failure names the exact broken leg).
# ---------------------------------------------------------------------------


def test_at_include_resolves_and_hashes(armed_consumer):
    fc.assert_at_include(armed_consumer)  # raises on failure


def test_clean_floor_passes_session_start(armed_consumer, pc_env):
    fc.assert_clean_pass(armed_consumer, pc_env)


def test_poison_caught_at_session_start(armed_consumer, pc_env):
    fc.assert_tamper_caught_sessionstart(armed_consumer, pc_env)
    # the floor is restored after the assertion (subsequent legs see a clean tree)
    fc.assert_clean_pass(armed_consumer, pc_env)


def test_deleted_floor_caught_at_session_start(armed_consumer, pc_env):
    # FIX-1 coverage: a deleted-but-tracked floor fails loud via --require-present
    fc.assert_absent_caught_sessionstart(armed_consumer, pc_env)
    # restored afterwards -> clean tree still passes
    fc.assert_clean_pass(armed_consumer, pc_env)


def test_sessionstart_wiring_present(armed_consumer):
    # FIX-2: the carrier WROTE the SessionStart self-arm wiring into settings.json
    fc.assert_sessionstart_wired(armed_consumer)


def test_sessionstart_wiring_missing_fails_red(armed_consumer):
    # negative control (teeth): strip the SessionStart hook -> the assertion must FAIL
    # (a consumer whose settings.json didn't travel gets no false green on self-arm).
    settings = armed_consumer / ".claude" / "settings.json"
    data = json.loads(settings.read_text(encoding="utf-8"))
    data.get("hooks", {}).pop("SessionStart", None)
    settings.write_text(json.dumps(data), encoding="utf-8", newline="\n")
    with pytest.raises(fc.ConformanceError):
        fc.assert_sessionstart_wired(armed_consumer)


def test_sessionstart_wiring_absent_settings_fails_red(armed_consumer):
    # a clone with no settings.json at all (wiring did not travel) must FAIL red
    (armed_consumer / ".claude" / "settings.json").unlink()
    with pytest.raises(fc.ConformanceError):
        fc.assert_sessionstart_wired(armed_consumer)


def test_autoarm_installs_git_hook(armed_consumer, pc_env):
    hook = armed_consumer / ".git" / "hooks" / "pre-commit"
    assert not hook.exists()  # absent right after `git init` (never travels with a clone)
    fc.assert_autoarm(armed_consumer, pc_env)
    assert hook.exists()  # the SessionStart bootstrap leg created it


def test_arm_step_installs_all_three_hook_stages(armed_consumer, pc_env):
    """#275b trip-test: the SessionStart arm command the floor carrier WROTE installs all
    three managed git-hook stages (pre-commit / commit-msg / pre-push), not just pre-commit.
    Runs the exact settings.json command verbatim; a regression to a 1-stage `pre_commit
    install` leaves commit-msg / pre-push absent and fails here (standalone — NOT part of the
    run_conformance suite, so it does not perturb the len()==8/==9 count assertions)."""
    settings = json.loads(
        (armed_consumer / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    cmds = [h["command"] for g in settings["hooks"]["SessionStart"] for h in g["hooks"]]
    arm = next(c for c in cmds if "pre_commit install" in c)
    argv = arm.split()
    assert argv[0] == "python"
    argv[0:1] = [sys.executable]  # run under this interpreter, not a bare `python` on PATH
    hooks = armed_consumer / ".git" / "hooks"
    for name in ("pre-commit", "commit-msg", "pre-push"):
        (hooks / name).unlink(missing_ok=True)  # prove install-from-absent
    r = subprocess.run(
        argv, cwd=str(armed_consumer), capture_output=True, text=True,
        encoding="utf-8", errors="replace", env={**os.environ, **pc_env},
    )
    assert r.returncode == 0, r.stderr
    for name in ("pre-commit", "commit-msg", "pre-push"):
        assert (hooks / name).exists(), f"{name} hook not installed (#275b regression)"


def test_poison_blocked_at_commit_time(armed_consumer, pc_env):
    fc.assert_autoarm(armed_consumer, pc_env)  # arm the git hook first
    fc.assert_tamper_caught_commit(armed_consumer, pc_env)
    # HEAD unmoved + floor restored -> a clean commit still works afterwards
    (armed_consumer / "AFTER.md").write_text("after\n", encoding="utf-8", newline="\n")
    _git(["add", "AFTER.md"], armed_consumer, pc_env)
    r = _git(["commit", "-m", "chore: after tamper"], armed_consumer, pc_env)
    assert r.returncode == 0


def test_real_task_flows_through_gate(armed_consumer, pc_env):
    fc.assert_autoarm(armed_consumer, pc_env)
    fc.assert_task_flow(armed_consumer, pc_env)
    # the merge landed on the first-parent spine as a --no-ff merge commit
    fp = _git(["log", "--first-parent", "--oneline", "-3"], armed_consumer, pc_env).stdout
    assert "conformance task-flow" in fp


# ---------------------------------------------------------------------------
# Negative controls — the harness FAILS loud when the loop is actually broken.
# ---------------------------------------------------------------------------


def test_suite_fails_when_guard_script_missing(armed_consumer, pc_env):
    (armed_consumer / fc.GUARD_REL).unlink()  # remove the guard the legs run
    with pytest.raises(fc.ConformanceError):
        fc.assert_tamper_caught_sessionstart(armed_consumer, pc_env)


def test_at_include_fails_when_include_absent(armed_consumer):
    (armed_consumer / "CLAUDE.md").write_text("# no include\n", encoding="utf-8", newline="\n")
    with pytest.raises(fc.ConformanceError):
        fc.assert_at_include(armed_consumer)


# ---------------------------------------------------------------------------
# Layer-2 teardown guard — "no leftovers" without blast radius.
# ---------------------------------------------------------------------------


def test_rmtree_guard_refuses_outside_temp_root(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(fc.ConformanceError):
        fc._rmtree_guarded(outside, tmp_path / "some_other_root")


def test_rmtree_guard_deletes_within_temp_root(tmp_path):
    root = tmp_path / "root"
    (root / "sub").mkdir(parents=True)
    (root / "sub" / "f.txt").write_text("x", encoding="utf-8")
    fc._rmtree_guarded(root, tmp_path)
    assert not root.exists()


# ---------------------------------------------------------------------------
# Layer-2 PATH regression — run_against_consumer's clone (Fix A: -c autocrlf=false)
# + faithful scope (Fix B: assert the real config carries floor-hash-verify, then scope
# past a clone-UNRESOLVABLE consumer config). Guards the two step-5 Gate-3 fixes.
# ---------------------------------------------------------------------------


@pytest.fixture
def committed_consumer_ai_council_like(tmp_path):
    """A COMMITTED consumer mirroring ai-council: armed floor, FORCE-TRACKED settings.json
    (so the SessionStart wiring travels on a clone), and a FULL .pre-commit-config.yaml =
    the real floor-hash-verify hook PLUS an unrelated, clone-UNRESOLVABLE relative-path repo
    (like ai-council's `../.dev-knowledge` hub-hooks). run_against_consumer must scope the
    unrelated repo out and still prove the floor hook blocks a commit."""
    tree = tmp_path / "consumer"
    tree.mkdir()
    _git(["-c", "init.defaultBranch=main", "init", "-q"], tree)
    _git(["config", "user.email", "c@e.c"], tree)
    _git(["config", "user.name", "C"], tree)
    _git(["config", "commit.gpgsign", "false"], tree)
    (tree / "CLAUDE.md").write_text("# Consumer\n", encoding="utf-8", newline="\n")
    cf.FloorCarrier(tree).apply(_FLOOR_TARGET)
    full_cfg = {"repos": [
        {"repo": "local", "hooks": [_FLOOR_LOCAL_HOOK]},
        # an unrelated repo that CANNOT resolve from a temp clone (ai-council-like) — the
        # exact shape (relative-path repo) that broke Gate 3 before the Fix-B scope.
        {"repo": "../nonexistent-sibling-hub", "rev": "v1.0.0", "hooks": [{"id": "unrelated"}]},
    ]}
    (tree / ".pre-commit-config.yaml").write_text(
        yaml.safe_dump(full_cfg, sort_keys=False), encoding="utf-8", newline="\n")
    _git(["add", "-A"], tree)
    _git(["add", "-f", ".claude/settings.json"], tree)  # force-track, like ai-council
    _git(["commit", "-q", "-m", "arm floor (ai-council-like: settings tracked, full config)"], tree)
    return tree


def test_layer2_path_scopes_unresolvable_repo_and_passes(committed_consumer_ai_council_like):
    """Fix A + Fix B regression: run_against_consumer clones (LF checkout, no unstaged-
    config error), asserts the real config carries floor-hash-verify, scopes out the
    clone-unresolvable unrelated repo, and the full suite passes 9/9 — so Leg 2b works
    despite an ai-council-like config pre-commit could not otherwise resolve in a clone."""
    passed = fc.run_against_consumer(committed_consumer_ai_council_like)
    assert len(passed) == 9  # 1 faithful config check + 8 conformance properties
    assert "real config carries floor-hash-verify" in passed[0]


def test_layer2_path_fails_red_when_floor_hook_absent(committed_consumer_ai_council_like):
    """Property 0 has teeth: a consumer whose committed config LACKS floor-hash-verify
    FAILS run_against_consumer (no false green on a missing commit-time arming)."""
    cfg = committed_consumer_ai_council_like / ".pre-commit-config.yaml"
    cfg.write_text("repos: []\n", encoding="utf-8", newline="\n")
    _git(["add", ".pre-commit-config.yaml"], committed_consumer_ai_council_like)
    _git(["commit", "-q", "-m", "strip floor hook"], committed_consumer_ai_council_like)
    with pytest.raises(fc.ConformanceError):
        fc.run_against_consumer(committed_consumer_ai_council_like)
