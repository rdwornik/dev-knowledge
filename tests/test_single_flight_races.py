"""The two OPEN RACES on `[#530]`, closed test-first. Both were filed at phase-1 integration
(2026-08-15, R2) against the merged guard, and both are LATENT -- the module is wired to no hook,
so neither has bitten anything yet. That is exactly why they are cheap to close now.

  (a) THE ABA IN `release`. `claim` points the lock ref at HEAD, and the racers this guard exists
      for SHARE HEAD -- N lanes forking from one commit is the normal batch-dispatch state, and
      the module's own docstring says so. So the ref value cannot identify WHO holds the lock:
      after a stale lock is cleared by hand and a second lane legitimately re-claims, the first
      lane's cleanup deletes a lock it does not hold. `release`'s remote leg is a bare
      `git push <remote> :<ref>`, which carries no expectation at all, so it always wins.
      Ruling R6(d): release compares-and-swaps on `run_id`, never on the branch tip.

  (b) THE `rev-parse` CONFLATION. `_local_holder` maps ANY non-zero exit to "the ref is absent",
      so a repository git cannot read at all is reported as a FREE lock -- `inspect --local-only`
      prints FREE and `release --local-only` reports success, neither having read any state. A
      guard whose failure mode is indistinguishable from its clean state is the fail-OPEN shape
      this module's docstring rejects everywhere else. Ruling R6(d): resolve-once is SEPARATED
      from `rev-parse`, and that separation is the ruling on the conflation.

WHY (b) IS DRIVEN WITH A REAL DIRECTORY rather than a monkeypatched `_git`. A directory that is
not a repository makes git exit 128 for real, which is the same class of answer a corrupt repo
gives -- and it means the test would still hold if the module changed which git command it asks.
A monkeypatched return value would pin the test to today's implementation and prove less.

These tests are committed RED, before either fix, per the lane contract.
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

CONTRACT = "contract-race"
LOCK = f"refs/locks/{CONTRACT}"


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8")


def _commit(repo, msg, fname="f.txt"):
    (repo / fname).write_text(msg + "\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg)


def _identify(repo):
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")


def _cli(repo, *args):
    return subprocess.run([sys.executable, str(_SCRIPT), *args, "--repo", str(repo)],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _remote_sha(repo, remote, ref) -> str:
    out = _git(repo, "ls-remote", remote, ref).stdout.split()
    return out[0] if out else ""


@pytest.fixture
def trio(tmp_path):
    """A bare remote plus TWO clones of it, both sitting on the SAME commit -- the batch-dispatch
    state, and the state that makes the ref value useless as an identity."""
    seed = tmp_path / "seed"
    seed.mkdir()
    _git(seed, "init", "-q", "-b", "main")
    _identify(seed)
    _commit(seed, "seed", fname="seed.txt")

    bare = tmp_path / "remote.git"
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


# --- race (a): the ABA in release -----------------------------------------------------------

@requires_git
def test_the_racers_really_do_share_head(trio):
    """The premise the ABA rests on, asserted rather than assumed.

    If two clones at the same commit did NOT produce the same value, guarding the delete on the
    ref's value would already be enough and the run_id token would be unnecessary.
    """
    _bare, a, b = trio
    assert _git(a, "rev-parse", "HEAD").stdout.strip() == _git(b, "rev-parse", "HEAD").stdout.strip()


@requires_git
def test_release_after_a_manual_clear_must_not_delete_another_runs_live_lock(trio):
    """RACE (a), end to end, in the order it was witnessed.

    1. lane A claims the contract;
    2. the lock looks stale, so an operator clears it BY HAND -- the escape the module's own
       refusal message prints, and therefore a supported action, not an abuse;
    3. lane B legitimately claims the now-free contract;
    4. lane A finishes and releases.

    Step 4 must not touch B's lock. A's release deleting it would put two executions of one
    contract in flight -- precisely what this guard exists to refuse -- and it would do so
    THROUGH the guard rather than around it.
    """
    _bare, a, b = trio
    assert single_flight.claim(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED

    _git(a, "push", "origin", f":{LOCK}")  # the operator's manual clear
    assert _remote_sha(a, "origin", LOCK) == ""

    assert single_flight.claim(CONTRACT, repo=b, remote="origin") == single_flight.CLAIMED
    b_holds = _remote_sha(b, "origin", LOCK)
    assert b_holds, "B must hold the lock before A cleans up"

    single_flight.release(CONTRACT, repo=a, remote="origin")

    assert _remote_sha(a, "origin", LOCK) == b_holds, (
        "A's cleanup deleted B's LIVE lock -- the contract is now claimable twice over"
    )


@requires_git
def test_two_claims_of_one_contract_are_distinguishable(trio):
    """The token that makes (a) fixable: two claims must not be the same value.

    While the lock ref points at HEAD this is false by construction, which is why the row calls
    for a generation-unique token rather than a value guard.
    """
    _bare, a, b = trio
    assert single_flight.claim(CONTRACT, repo=a, remote="origin") == single_flight.CLAIMED
    first = _remote_sha(a, "origin", LOCK)
    _git(a, "push", "origin", f":{LOCK}")
    assert single_flight.claim(CONTRACT, repo=b, remote="origin") == single_flight.CLAIMED
    second = _remote_sha(b, "origin", LOCK)
    assert first and second and first != second, (
        "two independent claims produced the same lock value, so no CAS can tell them apart"
    )


# --- race (b): the rev-parse conflation ------------------------------------------------------

@requires_git
def test_release_local_only_refuses_when_the_repo_cannot_be_read(tmp_path):
    """RACE (b): "could not ask" must not be answered as "nothing was there".

    A directory that is not a repository makes git exit 128 for real. Today `_local_holder`
    flattens that to "" and `release --local-only` prints `is now free locally` and returns
    success -- a guard reporting a clean state it never read.
    """
    nowhere = tmp_path / "not-a-repo"
    nowhere.mkdir()
    with pytest.raises(single_flight.SingleFlightError):
        single_flight.release(CONTRACT, repo=nowhere, local_only=True)


@requires_git
def test_inspect_local_only_refuses_when_the_repo_cannot_be_read(tmp_path):
    """The same conflation on the read path: an unreadable repo must not print FREE."""
    nowhere = tmp_path / "not-a-repo"
    nowhere.mkdir()
    with pytest.raises(single_flight.SingleFlightError):
        single_flight.inspect(CONTRACT, repo=nowhere, local_only=True)


@requires_git
def test_the_cli_fails_closed_on_an_unreadable_repo(tmp_path):
    """Exit 2, the module's fail-CLOSED code -- asserted through the process boundary, because
    the exit code is what a step-0 gate reads."""
    nowhere = tmp_path / "not-a-repo"
    nowhere.mkdir()
    result = _cli(nowhere, "inspect", CONTRACT, "--local-only")
    assert result.returncode == single_flight.INTERNAL_ERROR, result.stdout + result.stderr
    assert "FREE" not in result.stdout


@requires_git
def test_a_genuinely_free_lock_still_reads_as_free(trio):
    """The other half, so the fix cannot be "refuse everything": in a readable repo with no lock
    ref, FREE is the correct answer and release stays idempotent."""
    _bare, a, _b = trio
    assert single_flight.inspect(CONTRACT, repo=a, local_only=True) == single_flight.CLAIMED
    assert single_flight.release(CONTRACT, repo=a, local_only=True) == single_flight.CLAIMED
