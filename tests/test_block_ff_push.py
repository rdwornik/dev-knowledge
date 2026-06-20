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
    # SAME objects -> the WARN detector and the BLOCK gate cannot drift apart.
    assert bfp.filter_violations is vnf.filter_violations
    assert bfp.parse_log is vnf.parse_log
    assert bfp.format_one is vnf.format_one
    assert bfp._git is vnf._git
    assert bfp._FMT == vnf._FMT
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
