"""Tests for the [#530] single-flight dispatch guard (`scripts/single_flight.py`).

These are WITNESS tests: every one of them drives real `git` against a local bare remote and two
clones of it, because the properties under test are git's, not the script's. The script is only
correct if git behaves as the night-2 research evidence (T1-T10) recorded, so the evidence is
re-run here rather than cited.

The lettered names below are that evidence's:

  T1  a claim against a ref that does not exist succeeds
  T2  a SECOND CLONE THAT NEVER FETCHED the lock ref is still refused -- the property that makes
      this work across machines, and the one no filesystem lock has
  T3  a plain push of a DIFFERENT commit onto a held lock ref is rejected (non-fast-forward)
  T4  THE TRAP -- a plain push of the SAME commit onto a held lock ref prints `Everything
      up-to-date` and exits 0. Same-base is the normal batch-dispatch state, so a guard built on
      plain push greenlights exactly the race it was deployed against. The lease is the mechanism,
      and this test is here to fail loudly if that is ever traded for a plain push
  T5  release, then re-claim
  T6/T7 the local fast leg: `git update-ref --stdin` `create` succeeds once and then fails with
      `reference already exists`, exit 128 -- across WORKTREES of one clone, since refs live in the
      common git dir

A local bare remote is a faithful stand-in for `origin` here because the compare-and-swap is git
protocol, not a hosting feature. What it does NOT establish is the behaviour of the real remote,
and that is deliberately not claimed: the contract's step 3 demonstrates T2/T4 against the real
`origin` and the transcript lives in the lane packet.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import single_flight

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "single_flight.py"

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

CONTRACT = "contract-x"
LOCK = f"refs/locks/{CONTRACT}"


# --- real-git helpers (mirror test_merge_serialization / test_block_ff_push) ---

def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8")


def _blob(proc) -> str:
    return f"{proc.stdout}\n{proc.stderr}".lower()


def _commit(repo, msg, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg + "\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg)


def _identify(repo):
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")


def _cli(repo, *args):
    """Invoke the guard the way an operator or a step-0 gate would -- as a process, so the EXIT
    CODE is what is asserted, not a return value."""
    return subprocess.run([sys.executable, str(_SCRIPT), *args, "--repo", str(repo)],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def _ref_exists(repo, ref) -> bool:
    return _git(repo, "rev-parse", "--verify", "--quiet", ref, check=False).returncode == 0


def _remote_has(repo, remote, ref) -> bool:
    return bool(_git(repo, "ls-remote", remote, ref).stdout.strip())


@pytest.fixture
def trio(tmp_path):
    """A bare remote plus TWO clones of it, both sitting on the same commit -- the batch-dispatch
    state the guard exists for. Returns (bare, clone_a, clone_b)."""
    seed = tmp_path / "seed"
    seed.mkdir()
    _git(seed, "init", "-q", "-b", "main")
    _identify(seed)
    _commit(seed, "seed", fname="seed.txt")

    bare = tmp_path / "remote.git"
    # `-b main` on the BARE matters: without it the bare's HEAD keeps the host's default branch
    # name, which the pushed `main` never creates. `git clone` then only WARNS about the dangling
    # HEAD and still exits 0, handing back a clone with no HEAD at all -- a green setup step that
    # produced an unusable fixture.
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(bare))
    _git(seed, "remote", "add", "origin", str(bare))
    _git(seed, "push", "-q", "-u", "origin", "main")

    clones = []
    for name in ("a", "b"):
        target = tmp_path / f"clone_{name}"
        _git(tmp_path, "clone", "-q", str(bare), str(target))
        _identify(target)
        clones.append(target)
    return bare, clones[0], clones[1]


# --- T1: claim against a ref that does not exist -----------------------------

@requires_git
def test_t1_claim_new_lock_succeeds(trio):
    _, a, _b = trio
    assert single_flight.claim(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED
    assert _remote_has(a, "origin", LOCK), "the claim must leave the lock ref on the remote"
    assert _ref_exists(a, LOCK), "the holder also keeps the local ref (the fast leg)"


@requires_git
def test_t1_the_lock_ref_names_the_claimant_head_and_the_run(trio):
    """`git show <lock>` names the holder -- which under I-D3 is the contract-of-record commit.

    UPDATED 2026-08-21 by `[#530]` race (a) / ruling R6(d): the ref no longer IS HEAD, it is a
    lock object PARENTED on HEAD and carrying the run's `[#565]` id. The old shape -- ref == HEAD
    -- is exactly what made the ABA unfixable, because racers share HEAD and two locks were
    therefore the same value. The self-documenting property this test was written for is intact
    and wider: the contract-of-record commit is still reachable, and the run is now named too.
    """
    _, a, _b = trio
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    head = _git(a, "rev-parse", "HEAD").stdout.strip()
    lock_sha = _git(a, "ls-remote", "origin", LOCK).stdout.split()[0]

    assert lock_sha != head, "a lock that IS HEAD cannot identify which run holds it"
    assert _git(a, "rev-parse", f"{lock_sha}^").stdout.strip() == head, (
        "the lock object must be parented on the contract-of-record commit")
    body = _git(a, "cat-file", "commit", lock_sha).stdout
    assert CONTRACT in body and "run_id: " in body


# --- T2: the racer that never fetched is still refused -----------------------

@requires_git
def test_t2_unfetched_second_clone_is_refused_by_raw_git(trio):
    """The evidence itself: the expectation is evaluated by the RECEIVING repo, so clone B is
    refused with `stale info` and exit 1 without ever having heard of the ref."""
    _, a, b = trio
    _commit(a, "a-advances")           # the holder claims at a value B does not have
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    assert not _ref_exists(b, LOCK), "clone B must not have fetched the lock ref"

    raw = _git(b, "push", f"--force-with-lease={LOCK}:", "origin", f"HEAD:{LOCK}", check=False)
    assert raw.returncode == 1
    assert "stale info" in _blob(raw)


@requires_git
def test_t2_the_lease_alone_does_not_refuse_a_same_value_racer(trio):
    """MEASURED 2026-08-15, git 2.55.0.windows.3 — the finding this lane returns.

    The recorded design says `--force-with-lease=<ref>:` IS the mechanism because it refuses the
    same-HEAD racer that a plain push waves through. It does not, on its own: when the racer's
    value EQUALS the held one, git short-circuits to `[up to date]` and exit 0 before the lease
    decides, and both parties read exit 0 as "lock won" — in exactly the batch-dispatch state where
    N lanes fork from one HEAD.

    So the guard reads the `--porcelain` status FLAG, not the exit code. This test pins the raw
    behaviour that makes that necessary; if a future git starts rejecting here, this fails and the
    guard can be simplified deliberately rather than by accident.

    SETUP CHANGED 2026-08-21, and only the setup: A's side is now a RAW push of HEAD onto the lock
    ref rather than a `single_flight.claim`. Since race (a) / R6(d), a claim points the ref at a
    run_id-bearing object, so two claims no longer produce the same value and the module can no
    longer stage this scenario. What is under test here is GIT's behaviour, not the module's, so
    the setup is git's too -- and it must stay reachable: the porcelain-flag discrimination in the
    guard is only justified while this remains true of git."""
    _, a, b = trio
    _git(a, "push", "origin", f"HEAD:{LOCK}")     # raw, so the held value IS a HEAD both share
    assert _git(a, "rev-parse", "HEAD").stdout == _git(b, "rev-parse", "HEAD").stdout

    raw = _git(b, "push", "--porcelain", f"--force-with-lease={LOCK}:", "origin", f"HEAD:{LOCK}",
               check=False)
    assert raw.returncode == 0, "the lease does NOT refuse the same-value racer by exit code"
    assert "[up to date]" in raw.stdout
    assert raw.stdout.splitlines()[1].startswith("="), "the porcelain flag is what tells them apart"


@requires_git
def test_a_won_claim_is_reported_by_git_as_a_new_reference(trio):
    """The other half of the discrimination above: a genuine first claim carries the `*` flag."""
    _, a, _b = trio
    raw = _git(a, "push", "--porcelain", f"--force-with-lease={LOCK}:", "origin", f"HEAD:{LOCK}")
    assert raw.returncode == 0
    assert raw.stdout.splitlines()[1].startswith("*")
    assert "[new reference]" in raw.stdout


@requires_git
def test_t2_unfetched_second_clone_is_refused_by_the_guard(trio):
    _, a, b = trio
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    assert single_flight.claim(CONTRACT, repo=b, remote="origin") == single_flight.IN_FLIGHT


@requires_git
def test_t2_a_refused_claim_leaves_no_local_ref_behind(trio):
    """The local fast leg runs first, so a remote refusal must roll it back -- otherwise the loser
    of the race is left holding a lock that would refuse its own next honest attempt."""
    _, a, b = trio
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    single_flight.claim(CONTRACT, repo=b, remote="origin")
    assert not _ref_exists(b, LOCK)


@requires_git
def test_t2_refusal_message_names_how_to_inspect_and_release(capsys, trio):
    """git has no lock TTL, so the refusal carries the stale-hold escape (ruled option (a))."""
    _, a, b = trio
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    capsys.readouterr()
    single_flight.claim(CONTRACT, repo=b, remote="origin")
    err = capsys.readouterr().err
    assert "SINGLE-FLIGHT REFUSAL" in err
    assert f"git fetch origin {LOCK}" in err
    assert f"git push origin :{LOCK}" in err
    assert "no lock TTL" in err


# --- T3 / T4: why the lease is the mechanism ---------------------------------

@requires_git
def test_t3_plain_push_of_a_different_commit_is_rejected(trio):
    """A plain push is refused when the value it offers is not a fast-forward of the held one. The
    holder advances first, so B's HEAD is an ANCESTOR of the lock — pushing backwards. (Had B
    committed on top of the shared base instead, its push would be a legitimate fast-forward and
    would be ACCEPTED, which is its own reason not to build the guard on a plain push.)"""
    _, a, b = trio
    _commit(a, "a-advances")
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    raw = _git(b, "push", "--porcelain", "origin", f"HEAD:{LOCK}", check=False)
    assert raw.returncode == 1
    assert raw.stdout.splitlines()[1].startswith("!")
    # git 2.55 words this `fetch first` (the remote holds objects B lacks) where the recorded
    # evidence saw `non-fast-forward`; both are lock-attributable, and the guard reads either.
    assert any(marker in _blob(raw) for marker in single_flight._CONTENTION_MARKERS)


@requires_git
def test_t4_the_trap_plain_push_of_the_same_commit_returns_zero(trio):
    """THE TRAP. Both clones sit at one commit -- the normal batch-dispatch state -- and a plain
    push onto the held lock ref reports success. If this test ever fails, git changed; if the
    guard is ever rewritten to use a plain push, this is the evidence that it greenlights the
    race.

    SETUP CHANGED 2026-08-21 for the reason given on the T2 same-value case above: A's side is a
    RAW push, because since race (a) / R6(d) a claim no longer puts a shared HEAD on the ref. The
    trap itself is untouched and still witnessed."""
    _, a, b = trio
    _git(a, "push", "origin", f"HEAD:{LOCK}")     # raw, so the held value IS a HEAD both share
    assert _git(a, "rev-parse", "HEAD").stdout == _git(b, "rev-parse", "HEAD").stdout

    raw = _git(b, "push", "origin", f"HEAD:{LOCK}", check=False)
    assert raw.returncode == 0, "the trap: a plain push reads as a win"
    assert "everything up-to-date" in _blob(raw)


@requires_git
def test_t4_the_guard_refuses_the_same_commit_racer(trio):
    """The same state as the trap above, through the guard: refused, exit 3."""
    _, a, b = trio
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    assert _cli(b, "claim", CONTRACT).returncode == single_flight.IN_FLIGHT


# --- T5: release, then re-claim ----------------------------------------------

@requires_git
def test_t5_release_then_reclaim(trio):
    _, a, b = trio
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    assert single_flight.release(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED
    assert not _remote_has(a, "origin", LOCK)
    assert not _ref_exists(a, LOCK)
    # The lock is genuinely free again -- for the OTHER clone, which is the point of releasing.
    assert single_flight.claim(CONTRACT, repo=b, remote="origin") == single_flight.CLAIMED


@requires_git
def test_t5_release_is_idempotent(trio):
    """Releasing a lock nobody holds is a success, so a re-run after a partial failure is safe."""
    _, a, _b = trio
    assert single_flight.release(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED


# --- T6 / T7: the local fast leg, across worktrees of ONE clone ---------------

@requires_git
def test_t6_local_leg_claims_without_a_remote(trio):
    _, a, _b = trio
    assert single_flight.claim(CONTRACT, repo=a, local_only=True) == single_flight.CLAIMED
    assert _ref_exists(a, LOCK)
    assert not _remote_has(a, "origin", LOCK), "--local-only must not touch the remote"


@requires_git
def test_t7_local_leg_refuses_a_second_worktree_of_the_same_clone(tmp_path, trio):
    """Refs live in the COMMON git dir, so two worktrees of one clone contend correctly. This is
    the same-machine half the network leg does not need to be woken for."""
    _, a, _b = trio
    wt = tmp_path / "wt"
    _git(a, "worktree", "add", "-q", "--detach", str(wt), "HEAD")
    try:
        assert single_flight.claim(CONTRACT, repo=a, local_only=True) == single_flight.CLAIMED
        assert _ref_exists(wt, LOCK), "the worktree sees the primary's lock ref"
        assert single_flight.claim(CONTRACT, repo=wt, local_only=True) == single_flight.IN_FLIGHT
    finally:
        _git(a, "worktree", "remove", "--force", str(wt))
        _git(a, "worktree", "prune")
    assert not wt.exists(), "no leftovers -- the probe worktree is removed and removal verified"


@requires_git
def test_t7_raw_second_create_fails_128_with_reference_already_exists(trio):
    """The evidence's exact signature: exit 128, NOT 1 -- which is why the guard reads the message
    and not the code alone (128 is also git's generic fatal)."""
    _, a, _b = trio
    head = _git(a, "rev-parse", "HEAD").stdout.strip()
    first = subprocess.run(["git", "-C", str(a), "update-ref", "--stdin"],
                           input=f"create {LOCK} {head}\n".encode(), capture_output=True)
    assert first.returncode == 0
    second = subprocess.run(["git", "-C", str(a), "update-ref", "--stdin"],
                            input=f"create {LOCK} {head}\n".encode(), capture_output=True)
    assert second.returncode == 128
    assert "already exists" in second.stderr.decode("utf-8", "replace").lower()


# --- inspect, and the fail-CLOSED posture ------------------------------------

@requires_git
def test_inspect_reports_free_then_held_without_contending(capsys, trio):
    _, a, _b = trio
    assert single_flight.inspect(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED
    assert "is FREE" in capsys.readouterr().out
    single_flight.claim(CONTRACT, repo=a, remote="origin")
    capsys.readouterr()
    assert single_flight.inspect(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED
    out = capsys.readouterr().out
    assert "is HELD" in out and f"git push origin :{LOCK}" in out


@requires_git
def test_an_internal_error_exits_2_not_0_and_not_3(trio):
    """Fail CLOSED. An unusable contract id is an internal error, and the caller must be refused
    rather than waved through -- the posture block_ff_push was corrected to in ADR-85 amendment
    2026-08-03 SS-A6, where 'degraded -- allowing' silently auto-allowed the very thing the organ
    existed to refuse."""
    _, a, _b = trio
    result = _cli(a, "claim", "bad..id")
    assert result.returncode == single_flight.INTERNAL_ERROR
    assert "internal error" in result.stderr.lower()


@requires_git
def test_an_unreachable_remote_is_an_internal_error_not_a_claim(trio):
    """A gate that cannot reach its arbiter has NOT won the lock. It exits 2, and it leaves no
    local ref implying otherwise."""
    _, a, _b = trio
    result = _cli(a, "claim", CONTRACT, "--remote", str(a.parent / "nope.git"))
    assert result.returncode == single_flight.INTERNAL_ERROR
    assert not _ref_exists(a, LOCK)


@requires_git
def test_the_cli_claims_and_releases_end_to_end(trio):
    """The operator-facing path, exercised as a process: 0 on claim, 3 on the racer, 0 after
    release."""
    _, a, b = trio
    assert _cli(a, "claim", CONTRACT).returncode == single_flight.CLAIMED
    assert _cli(b, "claim", CONTRACT).returncode == single_flight.IN_FLIGHT
    assert _cli(a, "release", CONTRACT).returncode == single_flight.CLAIMED
    assert _cli(b, "claim", CONTRACT).returncode == single_flight.CLAIMED
