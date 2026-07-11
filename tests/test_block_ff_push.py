"""Tests for scripts/block_ff_push.py — #153 pre-push GATE (the PREVENT half of
core-invariant #5; validate_no_ff stays the WARN detector).

Closure metric (hard): a direct-to-main / true-FF push is REFUSED; a `--no-ff`
merge push PASSES — "the failure class can no longer land", proven by tests, not
"a hook exists". The four closure cases map 1:1 to the @requires_git E2E block,
which invokes the real block_ff_push.py as a subprocess against a throwaway bare
remote, feeding it the native pre-push stdin line a `git push` would. The pure
tests cover the range resolver (both wirings + edge shas). The exact native-stdin /
pre-commit-env ref format the resolver consumes is confirmed end-to-end by the
HANDOFF/verification live-wiring proof (Verification step 2) — these tests assume it.

Reuse-integrity: the gate imports its FF-signature from validate_no_ff (same
objects), so the detector and the gate can never disagree about what a violation IS.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import block_ff_push as bfp  # noqa: E402
import validate_no_ff as vnf  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "block_ff_push.py"
_ZERO = "0" * 40


# --- git tmp-repo helpers (mirror test_validate_no_ff) ----------------------

def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True, encoding="utf-8")


def _rev(repo, ref):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", ref],
                          check=True, capture_output=True, text=True,
                          encoding="utf-8").stdout.strip()


def _commit(repo, msg, adate=None, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _run(repo, "add", "-A")
    env = dict(os.environ)
    if adate:
        env["GIT_AUTHOR_DATE"] = adate
        env["GIT_COMMITTER_DATE"] = adate
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg],
                   check=True, capture_output=True, text=True, encoding="utf-8", env=env)


def _init_repo(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    # Root seed dated well before the baseline -> always grandfathered.
    _commit(repo, "seed", adate="2026-06-01T00:00:00", fname="seed.txt")
    _run(repo, "branch", "-M", "main")
    return repo


def _init_bare(tmp_path):
    bare = tmp_path / "remote.git"
    bare.mkdir()
    _run(bare, "init", "--bare", "-q")
    return bare


def _with_remote(tmp_path):
    """A repo whose `main` is already on a fresh bare remote; returns (repo, seed_sha)
    where seed_sha is what the remote currently has on main (the push's remote_sha)."""
    repo = _init_repo(tmp_path)
    bare = _init_bare(tmp_path)
    _run(repo, "remote", "add", "origin", str(bare))
    _run(repo, "push", "-q", "origin", "main")
    return repo, _rev(repo, "main")


def _invoke(repo, stdin_text, env_extra=None):
    """Run block_ff_push.py exactly as git's native pre-push hook would: as a
    subprocess in `repo` with the ref line(s) on stdin. PRE_COMMIT_* are scrubbed so
    a caller's stray env can't leak into the stdin-path tests."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("PRE_COMMIT_")}
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, str(_SCRIPT)], input=stdin_text,
                          capture_output=True, text=True, env=env, cwd=str(repo))


def _push_line(local_sha, remote_sha, ref="refs/heads/main"):
    return f"{ref} {local_sha} {ref} {remote_sha}\n"


# --- pure: range resolver (both wirings + edge shas) ------------------------

def test_range_from_stdin_main():
    lines = bfp.parse_stdin_lines(_push_line("LLLL", "RRRR"))
    assert bfp.resolve_push_range(lines, {}) == "RRRR..LLLL"


def test_range_ignores_non_main_ref():
    lines = bfp.parse_stdin_lines(_push_line("LLLL", "RRRR", ref="refs/heads/feat/x"))
    assert bfp.resolve_push_range(lines, {}) is None


def test_range_from_env_fallback():
    # pre-commit wiring: stdin already consumed -> refs arrive as PRE_COMMIT_* env.
    env = {"PRE_COMMIT_REMOTE_BRANCH": "refs/heads/main",
           "PRE_COMMIT_TO_REF": "LLLL", "PRE_COMMIT_FROM_REF": "RRRR"}
    assert bfp.resolve_push_range([], env) == "RRRR..LLLL"


def test_range_env_ignores_non_main():
    env = {"PRE_COMMIT_REMOTE_BRANCH": "refs/heads/automation/nightly",
           "PRE_COMMIT_TO_REF": "LLLL", "PRE_COMMIT_FROM_REF": "RRRR"}
    assert bfp.resolve_push_range([], env) is None


def test_range_delete_main_skipped():
    # Deleting main (local all-zeros) is out of scope -> skip.
    lines = bfp.parse_stdin_lines(_push_line(_ZERO, "RRRR"))
    assert bfp.resolve_push_range(lines, {}) is None


def test_range_new_remote_full_history():
    # New main on a fresh remote (remote all-zeros) -> scan the full local history.
    lines = bfp.parse_stdin_lines(_push_line("LLLL", _ZERO))
    assert bfp.resolve_push_range(lines, {}) == "LLLL"


def test_range_empty_local_skipped():
    # An empty PRE_COMMIT_TO_REF (a main delete on the env path) is out of scope ->
    # skip, NOT a half-open "RRRR.." range that git would resolve to RRRR..HEAD.
    assert bfp._range_for("", "RRRR") is None


def test_range_empty_remote_full_history():
    # An empty remote ref (fresh remote, no PRE_COMMIT_FROM_REF) -> full local history.
    assert bfp._range_for("LLLL", "") == "LLLL"


def test_parse_stdin_lines_multi_and_malformed():
    text = (_push_line("L1", "R1", ref="refs/heads/main")
            + "garbage line with three tok\n"
            + _push_line("L2", "R2", ref="refs/heads/feat/y"))
    parsed = bfp.parse_stdin_lines(text)
    assert parsed == [
        ("refs/heads/main", "L1", "refs/heads/main", "R1"),
        ("refs/heads/feat/y", "L2", "refs/heads/feat/y", "R2"),
    ]


def test_is_zero():
    assert bfp._is_zero("0" * 40)      # sha-1 null
    assert bfp._is_zero("0" * 64)      # sha-256 null
    assert not bfp._is_zero("a1b2c3d")  # real sha
    assert not bfp._is_zero("")         # empty is not the sentinel


# --- reuse-integrity: gate shares validate_no_ff's FF-signature -------------

def test_shares_validate_no_ff_signature():
    # ONE module object, and the gate delegates the whole SCAN to find_violations (not
    # just leaf helpers) -> the WARN detector and the BLOCK gate cannot drift apart.
    assert bfp._vnf is vnf
    assert bfp._vnf.find_violations is vnf.find_violations
    assert bfp._git is vnf._git
    assert bfp.format_one is vnf.format_one
    assert bfp.BASELINE_DATE == vnf.BASELINE_DATE


# --- E2E closure cases (bare remote, real subprocess) -----------------------

@requires_git
def test_direct_to_main_push_refused(tmp_path):
    repo, remote_sha = _with_remote(tmp_path)
    _commit(repo, "feat: oops direct on main", adate="2026-06-16T10:00:00", fname="a.txt")
    res = _invoke(repo, _push_line(_rev(repo, "main"), remote_sha))
    assert res.returncode == 1
    assert "oops direct on main" in res.stderr


@requires_git
def test_ff_merge_push_refused(tmp_path):
    # A fast-forward merge replays the feature commit ONTO main's first-parent spine
    # with no merge commit -> the gate must refuse the push.
    repo, remote_sha = _with_remote(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/y")
    _commit(repo, "feat: do y (ff'd onto main)", adate="2026-06-16T10:00:00", fname="y.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "--ff-only", "-q", "feat/y")
    res = _invoke(repo, _push_line(_rev(repo, "main"), remote_sha))
    assert res.returncode == 1
    assert "do y (ff'd onto main)" in res.stderr


@requires_git
def test_no_ff_merge_push_passes(tmp_path):
    # The sanctioned path: merge commit excluded (--no-merges), feature commit off the
    # first-parent spine -> no violation -> push allowed.
    repo, remote_sha = _with_remote(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/z")
    _commit(repo, "feat: do z", adate="2026-06-16T10:00:00", fname="z.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/z --no-ff", "feat/z")
    res = _invoke(repo, _push_line(_rev(repo, "main"), remote_sha))
    assert res.returncode == 0, res.stderr


@requires_git
def test_feature_branch_push_passes(tmp_path):
    # A non-main ref is untouched even when main itself carries a violation -> the gate
    # scopes to the pushed ref, not repo state.
    repo, _remote_sha = _with_remote(tmp_path)
    _commit(repo, "feat: direct on main (not being pushed)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: on feature branch", adate="2026-06-16T10:00:00", fname="x.txt")
    line = _push_line(_rev(repo, "feat/x"), _ZERO, ref="refs/heads/feat/x")
    res = _invoke(repo, line)
    assert res.returncode == 0, res.stderr


@requires_git
def test_automation_branch_push_passes(tmp_path):
    # automation/* (ADR-84) is a normal non-main ref -> untouched.
    repo, _remote_sha = _with_remote(tmp_path)
    _run(repo, "checkout", "-q", "-b", "automation/nightly")
    _commit(repo, "chore(routine/x): nightly", adate="2026-06-16T10:00:00", fname="n.txt")
    line = _push_line(_rev(repo, "automation/nightly"), _ZERO,
                      ref="refs/heads/automation/nightly")
    res = _invoke(repo, line)
    assert res.returncode == 0, res.stderr


@requires_git
def test_env_wiring_refused(tmp_path):
    # The pre-commit path: empty stdin + PRE_COMMIT_* env -> the gate still refuses.
    repo, remote_sha = _with_remote(tmp_path)
    _commit(repo, "feat: direct via env path", adate="2026-06-16T10:00:00", fname="a.txt")
    res = _invoke(repo, "", env_extra={
        "PRE_COMMIT_REMOTE_BRANCH": "refs/heads/main",
        "PRE_COMMIT_TO_REF": _rev(repo, "main"),
        "PRE_COMMIT_FROM_REF": remote_sha,
    })
    assert res.returncode == 1
    assert "direct via env path" in res.stderr


@requires_git
def test_fresh_remote_push_refused(tmp_path):
    # New main on a fresh remote (remote_sha all-zeros): full local history is scanned,
    # so a post-baseline direct commit is still caught.
    repo = _init_repo(tmp_path)
    _commit(repo, "feat: direct on brand-new main", adate="2026-06-16T10:00:00", fname="a.txt")
    res = _invoke(repo, _push_line(_rev(repo, "main"), _ZERO))
    assert res.returncode == 1
    assert "direct on brand-new main" in res.stderr


@requires_git
def test_failsoft_on_bad_range(tmp_path):
    # A git error inside detection degrades to [] (never wedge a legitimate push).
    repo = _init_repo(tmp_path)
    assert bfp.violations_in_range(repo, "nonexistent-a..nonexistent-b") == []


@requires_git
def test_pre_baseline_push_passes(tmp_path):
    # A direct commit dated before the baseline is grandfathered -> push allowed.
    repo, remote_sha = _with_remote(tmp_path)
    _commit(repo, "feat: early direct", adate="2026-06-05T10:00:00", fname="e.txt")
    res = _invoke(repo, _push_line(_rev(repo, "main"), remote_sha))
    assert res.returncode == 0, res.stderr


@requires_git
def test_gate_and_detector_agree(tmp_path):
    # The shared FF-signature: the gate's range scan and the detector's full-spine scan
    # surface the SAME violation for the same repo state.
    repo = _init_repo(tmp_path)
    seed = _rev(repo, "main")
    _commit(repo, "feat: direct on main", adate="2026-06-16T10:00:00", fname="a.txt")
    gate = bfp.violations_in_range(repo, f"{seed}..{_rev(repo, 'main')}", baseline="2026-06-10")
    det = vnf.find_violations(repo, baseline="2026-06-10")
    assert [v[2] for v in gate] == [v[2] for v in det] == ["feat: direct on main"]


# ============================================================================
# #318 — pre-commit adapter ref-stream edges (empty-remote initial + multi-ref)
# ============================================================================
# Under the REAL carrier block_ff runs as a pre-commit-managed pre-push hook: pre-commit
# CONSUMES the native pre-push stdin and re-exposes only ONE parsed ref pair via the
# PRE_COMMIT_* env vars (pre-commit 4.5.1 hook_impl.py). So block_ff's env path can miss
# `main` two ways it cannot express — a MULTI-REF push where main is not the forwarded
# ref, and an EMPTY-REMOTE INITIAL push (pre-commit's all_files shape sets
# PRE_COMMIT_REMOTE_BRANCH=refs/heads/main but neither PRE_COMMIT_TO_REF nor FROM_REF,
# and never the all-zeros sha). The fix reconstructs main's range from local git refs.
# Tier 1 drives the real script subprocess with the exact env pre-commit produces
# (deterministic — no dependence on git's stdin ordering); Tier 3 drives a real
# `git push` through the pre-commit pre-push adapter (closes the Codex-A3 "real adapter
# not asserted" coverage gap).


# --- Tier 1: behavioral RED->GREEN via the real script subprocess -----------

@requires_git
def test_precommit_multiref_hidden_main_refused(tmp_path):
    # Multi-ref push: pre-commit forwarded feat/x (empty stdin + PRE_COMMIT_* env), hiding
    # main. Current code returns 0 (miss); after the fix, main's range is reconstructed
    # from refs/remotes/origin/main..refs/heads/main and the direct commit is refused.
    repo, _seed = _with_remote(tmp_path)
    _commit(repo, "feat: oops direct on main (multiref)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: legit on feat/x", adate="2026-06-16T10:00:00", fname="x.txt")
    res = _invoke(repo, "", env_extra={
        "PRE_COMMIT_REMOTE_NAME": "origin",
        "PRE_COMMIT_REMOTE_BRANCH": "refs/heads/feat/x",
        "PRE_COMMIT_TO_REF": _rev(repo, "feat/x"),
        "PRE_COMMIT_FROM_REF": _ZERO,
    })
    assert res.returncode == 1, res.stderr
    assert "oops direct on main" in res.stderr


@requires_git
def test_precommit_empty_remote_initial_refused(tmp_path):
    # Empty-remote INITIAL push: pre-commit's all_files shape sets REMOTE_BRANCH=main but
    # NO TO_REF/FROM_REF (and never the all-zeros sha). Current code -> _range_for("","")
    # -> None -> 0 (miss); after the fix -> full local history -> the direct commit refused.
    repo = _init_repo(tmp_path)
    _commit(repo, "feat: direct on brand-new main (initial)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    res = _invoke(repo, "", env_extra={
        "PRE_COMMIT_REMOTE_NAME": "origin",
        "PRE_COMMIT_REMOTE_BRANCH": "refs/heads/main",
    })
    assert res.returncode == 1, res.stderr
    assert "direct on brand-new main" in res.stderr


# --- Tier 3: real pre-commit pre-push ADAPTER (closes Codex-A3 coverage gap) --
# A repo:local + language:system config wires the WORKING-TREE block_ff_push.py at the
# pre-push stage, so pre-commit runs the live script (not a hub clone-at-rev) through its
# real PRE_COMMIT_* adapter — RED/GREEN track the current working tree, no commit needed.

_HAS_PRECOMMIT = importlib.util.find_spec("pre_commit") is not None
requires_precommit = pytest.mark.skipif(
    not _HAS_PRECOMMIT or shutil.which("git") is None,
    reason="pre-commit or git not available",
)
_HUB = Path(__file__).resolve().parent.parent


def _pc_env(tmp_path):
    """Env with an ISOLATED pre-commit store so the E2E never contends the shared
    ~/.cache/pre-commit lock (the orphan-lock-hang gotcha)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("PRE_COMMIT_")}
    env["PRE_COMMIT_HOME"] = str(tmp_path / "pc-cache")
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _local_pre_push_config() -> str:
    """A repo:local pre-commit config wiring the WORKING-TREE block_ff_push.py at the
    pre-push stage (language: system -> pre-commit runs the live script, exercising the
    real PRE_COMMIT_* adapter against the current fix)."""
    hp = str(_HUB / "scripts").replace("\\", "/")
    return (
        "default_install_hook_types: [pre-push]\n"
        "repos:\n  - repo: local\n    hooks:\n"
        "      - id: block-ff-push\n        name: block-ff-push\n"
        f"        entry: python {hp}/block_ff_push.py\n"
        "        language: system\n        stages: [pre-push]\n        always_run: true\n"
        "        pass_filenames: false\n")


def _pc_consumer(tmp_path):
    """A consumer repo whose single seed commit (pre-baseline -> grandfathered) already
    carries the local pre-push carrier, with an isolated store and the pre-push hook
    armed. Seeding the config INTO the grandfathered commit keeps main's baseline clean
    (a separate post-baseline config commit would itself be a violation)."""
    repo = tmp_path / "consumer"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "c@c.c")
    _run(repo, "config", "user.name", "c")
    _run(repo, "config", "commit.gpgsign", "false")
    (repo / "seed.txt").write_text("seed", encoding="utf-8")
    (repo / ".pre-commit-config.yaml").write_text(_local_pre_push_config(), encoding="utf-8")
    _run(repo, "add", "-A")
    env0 = dict(os.environ)
    env0["GIT_AUTHOR_DATE"] = env0["GIT_COMMITTER_DATE"] = "2026-06-01T00:00:00"
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "seed"],
                   check=True, capture_output=True, text=True, encoding="utf-8", env=env0)
    _run(repo, "branch", "-M", "main")
    env = _pc_env(tmp_path)
    inst = subprocess.run([sys.executable, "-m", "pre_commit", "install",
                           "--hook-type", "pre-push"], cwd=str(repo),
                          capture_output=True, text=True, env=env)
    assert inst.returncode == 0, inst.stderr
    return repo, env


def _push(repo, env, *refs):
    return subprocess.run(["git", "-C", str(repo), "push", "origin", *refs],
                          capture_output=True, text=True, env=env)


@requires_precommit
def test_precommit_adapter_empty_remote_initial_refuses(tmp_path):
    # Real adapter, empty-remote INITIAL push: fresh bare origin (no main yet). A
    # post-baseline direct commit on main + the first `git push origin main` -> REFUSED.
    repo, env = _pc_consumer(tmp_path)
    bare = _init_bare(tmp_path)
    _run(repo, "remote", "add", "origin", str(bare))
    _commit(repo, "feat: direct on main (initial adapter)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    push = _push(repo, env, "main")
    out = push.stdout + push.stderr
    assert push.returncode != 0, f"empty-remote initial direct-to-main push should be refused:\n{out}"
    assert "REFUSED" in out.upper() or "local 'main'" in out, out


@requires_precommit
def test_precommit_adapter_multiref_dirty_main_stays_refused(tmp_path):
    # Real adapter, MULTI-REF push: origin/main established, a post-baseline direct commit
    # on main, then `git push origin feat/x main`.
    # NOTE (empirical, this git version): git feeds `refs/heads/main` FIRST in the pre-push
    # stream regardless of argv/HEAD/branch-name, so pre-commit forwards MAIN and the env
    # path catches the violation directly — the multi-ref miss is NOT reproducible as a
    # real push here (it is git/remote-helper-order-dependent). This test therefore asserts
    # the end-to-end INVARIANT (a multi-ref push carrying a direct-to-main commit is
    # refused), passing before AND after the fix. The deterministic RED->GREEN proof for
    # the multi-ref code path is test_precommit_multiref_hidden_main_refused (Tier 1),
    # which exercises the case where the adapter forwards a NON-main ref first.
    repo, env = _pc_consumer(tmp_path)
    bare = _init_bare(tmp_path)
    _run(repo, "remote", "add", "origin", str(bare))
    _push(repo, env, "main")  # establish origin/main (grandfathered seed -> passes)
    _commit(repo, "feat: oops direct on main (adapter multiref)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: legit on feat/x", adate="2026-06-16T10:00:00", fname="x.txt")
    push = _push(repo, env, "feat/x", "main")
    out = push.stdout + push.stderr
    assert push.returncode != 0, f"multi-ref push carrying a direct-to-main commit should be refused:\n{out}"
    assert "REFUSED" in out.upper() or "local 'main'" in out, out


@requires_precommit
def test_precommit_adapter_feature_only_clean_main_passes(tmp_path):
    # Precision guard (real adapter): a feature-only push with a CLEAN main is never
    # refused, even though reconstruction runs (origin/main..main is empty).
    repo, env = _pc_consumer(tmp_path)
    bare = _init_bare(tmp_path)
    _run(repo, "remote", "add", "origin", str(bare))
    _push(repo, env, "main")  # clean main established on origin
    _run(repo, "checkout", "-q", "-b", "feat/y")
    _commit(repo, "feat: do y", adate="2026-06-16T10:00:00", fname="y.txt")
    push = _push(repo, env, "feat/y")
    assert push.returncode == 0, f"feature push with clean main must pass:\n{push.stdout}\n{push.stderr}"


# --- Tier 2: helper units, precision guards, native-suppression, attribution -

def test_under_precommit_flag():
    assert bfp._under_precommit({"PRE_COMMIT_REMOTE_NAME": "origin"})
    assert bfp._under_precommit({"PRE_COMMIT_FROM_REF": "x"})
    assert not bfp._under_precommit({})
    assert not bfp._under_precommit({"PATH": "/usr/bin", "HOME": "/home/x"})


@requires_git
def test_reconstruct_multiref_hidden_main(tmp_path):
    # tracking ref present -> range is remote-tracking-main..local-main, and the scan
    # surfaces exactly the post-baseline direct commit.
    repo, seed = _with_remote(tmp_path)
    _commit(repo, "feat: direct on main", adate="2026-06-16T10:00:00", fname="a.txt")
    main_sha = _rev(repo, "main")
    rng = bfp._reconstruct_main_range(repo, {"PRE_COMMIT_REMOTE_NAME": "origin"})
    assert rng == f"{seed}..{main_sha}"
    assert [v[2] for v in bfp.violations_in_range(repo, rng)] == ["feat: direct on main"]


@requires_git
def test_reconstruct_empty_remote_initial(tmp_path):
    # no remote-tracking ref -> full local history (just the local main sha).
    repo = _init_repo(tmp_path)
    _commit(repo, "feat: direct", adate="2026-06-16T10:00:00", fname="a.txt")
    main_sha = _rev(repo, "main")
    rng = bfp._reconstruct_main_range(repo, {"PRE_COMMIT_REMOTE_NAME": "origin"})
    assert rng == main_sha
    assert [v[2] for v in bfp.violations_in_range(repo, rng)] == ["feat: direct"]


@requires_git
def test_reconstruct_missing_tracking_ref_no_crash(tmp_path):
    # tracking ref deleted -> full-history fallback, no crash (fail-soft).
    repo, _seed = _with_remote(tmp_path)
    _run(repo, "update-ref", "-d", "refs/remotes/origin/main")
    main_sha = _rev(repo, "main")
    assert bfp._reconstruct_main_range(repo, {"PRE_COMMIT_REMOTE_NAME": "origin"}) == main_sha


@requires_git
def test_reconstruct_no_local_main_skips(tmp_path):
    # no local main ref -> None (nothing to protect), never a crash.
    repo = _init_repo(tmp_path)
    _run(repo, "branch", "-M", "trunk")  # rename main away
    assert bfp._reconstruct_main_range(repo, {"PRE_COMMIT_REMOTE_NAME": "origin"}) is None


@requires_git
def test_precommit_feature_push_clean_main_passes(tmp_path):
    # Precision guard (subprocess): reconstruction RUNS on a feature-ref pre-commit push,
    # but local main advanced only by a proper --no-ff MERGE (excluded by --no-merges) ->
    # no violation -> rc 0. A clean repo is never refused.
    repo, _seed = _with_remote(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feat/z")
    _commit(repo, "feat: do z", adate="2026-06-16T10:00:00", fname="z.txt")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/z --no-ff", "feat/z")
    _run(repo, "checkout", "-q", "-b", "feat/w")
    _commit(repo, "feat: do w", adate="2026-06-16T10:00:00", fname="w.txt")
    res = _invoke(repo, "", env_extra={
        "PRE_COMMIT_REMOTE_NAME": "origin",
        "PRE_COMMIT_REMOTE_BRANCH": "refs/heads/feat/w",
        "PRE_COMMIT_TO_REF": _rev(repo, "feat/w"),
        "PRE_COMMIT_FROM_REF": _ZERO,
    })
    assert res.returncode == 0, res.stderr


@requires_git
def test_native_feature_push_does_not_reconstruct(tmp_path):
    # The `not lines` guard: a NATIVE feature push carries a ref line, so even with a dirty
    # local main we must NOT reconstruct (native stdin already saw every ref) -> rc 0.
    repo, _remote_sha = _with_remote(tmp_path)
    _commit(repo, "feat: direct on main (dirty, not pushed)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: on feat/x", adate="2026-06-16T10:00:00", fname="x.txt")
    line = _push_line(_rev(repo, "feat/x"), _ZERO, ref="refs/heads/feat/x")
    res = _invoke(repo, line)  # native stdin present, PRE_COMMIT_* scrubbed
    assert res.returncode == 0, res.stderr


@requires_git
def test_reconstructed_refusal_attributes_to_local_main(tmp_path):
    # The reconstructed-path refusal must attribute the violation to LOCAL main + this push
    # (so a consumer pushing a feature branch understands why the refusal names main).
    repo, _seed = _with_remote(tmp_path)
    _commit(repo, "feat: direct on main (attribution)",
            adate="2026-06-16T10:00:00", fname="a.txt")
    _run(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: legit", adate="2026-06-16T10:00:00", fname="x.txt")
    res = _invoke(repo, "", env_extra={
        "PRE_COMMIT_REMOTE_NAME": "origin",
        "PRE_COMMIT_REMOTE_BRANCH": "refs/heads/feat/x",
        "PRE_COMMIT_TO_REF": _rev(repo, "feat/x"),
        "PRE_COMMIT_FROM_REF": _ZERO,
    })
    assert res.returncode == 1, res.stderr
    assert "local 'main'" in res.stderr
    assert "surfaced by this push" in res.stderr


@requires_git
def test_normal_env_path_refusal_omits_reconstruction_note(tmp_path):
    # A refusal via the ordinary env path (main forwarded, valid TO/FROM) is NOT the
    # reconstructed path -> it must NOT carry the local-main attribution note.
    repo, remote_sha = _with_remote(tmp_path)
    _commit(repo, "feat: direct via env path", adate="2026-06-16T10:00:00", fname="a.txt")
    res = _invoke(repo, "", env_extra={
        "PRE_COMMIT_REMOTE_BRANCH": "refs/heads/main",
        "PRE_COMMIT_TO_REF": _rev(repo, "main"),
        "PRE_COMMIT_FROM_REF": remote_sha,
    })
    assert res.returncode == 1, res.stderr
    assert "surfaced by this push" not in res.stderr
