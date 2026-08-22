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

import os
import re
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


def _cli_env(repo, env, *args):
    """`_cli` with an EXPLICIT environment -- so a test can prove a property holds without the
    run-id variable, rather than inheriting whatever an earlier test exported."""
    return subprocess.run([sys.executable, str(_SCRIPT), *args, "--repo", str(repo)],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env=env)


def _claim(repo, remote="origin", **kw) -> str:
    """Claim and hand back the minted token, asserting the claim was WON.

    `claim_token` and not `claim`: the ownership token is minted per claim and cannot be pinned by
    a caller (a reusable capability is not a capability), so a test that needs to release later
    must capture what the module minted -- exactly as an operator reads it off claim's stdout.
    """
    code, token = single_flight.claim_token(CONTRACT, repo=repo, remote=remote, **kw)
    assert code == single_flight.CLAIMED
    assert token
    return token


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
    tok_A = _claim(a)

    _git(a, "push", "origin", f":{LOCK}")  # the operator's manual clear
    assert _remote_sha(a, "origin", LOCK) == ""

    assert single_flight.claim(CONTRACT, repo=b, remote="origin") == single_flight.CLAIMED
    b_holds = _remote_sha(b, "origin", LOCK)
    assert b_holds, "B must hold the lock before A cleans up"

    single_flight.release(CONTRACT, repo=a, remote="origin", token=tok_A)

    assert _remote_sha(a, "origin", LOCK) == b_holds, (
        "A's cleanup deleted B's LIVE lock -- the contract is now claimable twice over"
    )


@requires_git
def test_contention_refusal_names_the_live_holder_instead_of_denying_it_has_one(trio, capsys):
    """The refusal must not tell the operator a LIVE, tokenised lock "carries no run_id".

    Same trajectory as the ABA test above -- A claims, the lock is cleared by hand, B
    legitimately re-claims, A cleans up -- but this pins what A's refusal SAYS rather than
    only that B's lock survives.

    A's push carries `--force-with-lease` against its own stale expectation, so the lease is
    rejected and the contention branch runs. That branch used to pass `owner=None` to
    `_not_ours`, which prints "it carries no run_id (taken by hand, or before this guard
    tokenised locks)" -- false about B's lock, and it reads as "nobody owns this", which
    makes the `release: git push <remote> :<ref>` escape printed directly underneath look
    safe. Following it deletes B's LIVE lock. The guard's own message steering an operator
    into the race the guard exists to refuse is worse than no message.

    gpt-5.6-terra HIGH, carried out-of-lane by CLOUD-3 2026-08-22 and ruled out-of-band as
    live harm. The sibling call site in the same function already resolved the owner; this
    pins that the two now agree.
    """
    _bare, a, b = trio
    tok_A = _claim(a)

    _git(a, "push", "origin", f":{LOCK}")          # the operator's manual clear
    assert single_flight.claim(CONTRACT, repo=b, remote="origin") == single_flight.CLAIMED
    b_holds = _remote_sha(b, "origin", LOCK)
    assert b_holds, "B must hold the lock before A cleans up"

    capsys.readouterr()
    rc = single_flight.release(CONTRACT, repo=a, remote="origin", token=tok_A)
    err = capsys.readouterr().err

    assert rc == single_flight.NOT_OURS, err
    assert _remote_sha(a, "origin", LOCK) == b_holds, "B's live lock was deleted"
    # The fixture precondition that makes the assertion below mean something: B's lock IS
    # tokenised, so 'carries no run_id' is a false statement about it and not a fair report.
    assert single_flight._remote_lock_token(a, "origin", LOCK, b_holds) is not None, (
        "fixture precondition: B's lock must carry a token, or this test proves nothing")
    assert "carries no run_id" not in err, (
        "the refusal denies the live lock has an owner, which makes the printed release "
        "escape look safe: " + err)


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
        single_flight.release(CONTRACT, repo=nowhere, local_only=True, token="r")


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


# --- what proves ownership: the local ref, NOT run_id equality ------------------------------

@requires_git
def test_release_without_a_token_refuses_rather_than_guessing(trio):
    """TERRA P1, 2026-08-21 -- and the correction of a fix that was briefly wrong here.

    The first version of this fix treated the LOCAL REF as proof of ownership, reasoning that
    `update-ref create` is exclusive within a clone. It is not proof, and it fails in precisely
    this repo's shape: refs live in the COMMON git dir, so every worktree of one clone shares
    them. Stale run A resolves the ref that run B created after a manual clear, deletes it, and
    hands B's OWN sha to the remote lease as its expectation -- which matches, so the lease waves
    it through and B's live lock dies. The ABA, reproduced THROUGH the fix meant to close it.

    So a release carrying no token refuses before touching anything. The child environment is
    scrubbed of the run-id variable, because the earlier version passed the pre-existing CLI test
    only by inheriting an id an earlier test had exported into the pytest process.
    """
    _bare, a, _b = trio
    env = {k: v for k, v in os.environ.items() if k != "DEV_KNOWLEDGE_TELEMETRY_RUN_ID"}

    claimed = _cli_env(a, env, "claim", CONTRACT)
    assert claimed.returncode == single_flight.CLAIMED, claimed.stdout + claimed.stderr
    held = _remote_sha(a, "origin", LOCK)

    released = _cli_env(a, env, "release", CONTRACT)
    assert released.returncode == single_flight.NOT_OURS, released.stdout + released.stderr
    assert "no ownership token was supplied" in released.stderr
    assert _remote_sha(a, "origin", LOCK) == held, "an unproven release must touch nothing"


@requires_git
def test_claim_emits_the_run_id_machine_readably(trio):
    """TERRA P1 (sixth pass), 2026-08-21: `claim` runs as a SHORT-LIVED SUBPROCESS in the live
    dispatch flow and the lane is launched afterwards by a separate command, so exporting the id
    inside the claim process reaches nothing. Unless the dispatcher can read the id back (or hand
    one in), the lock records one id and the lane's telemetry mints another.

    What this module owns is EMITTING it parseably; making the launcher consume it is the
    dispatcher's, and this module launches nothing. Both halves are asserted here.
    """
    _bare, a, _b = trio
    env = {k: v for k, v in os.environ.items() if k != "DEV_KNOWLEDGE_TELEMETRY_RUN_ID"}
    claimed = _cli_env(a, env, "claim", CONTRACT)

    emitted = next(ln.split("=", 1)[1].strip() for ln in claimed.stdout.splitlines()
                   if ln.startswith("single_flight: run_id="))
    assert emitted, "the run_id must be readable back by the dispatcher"
    assert single_flight._lock_run_id(a, _remote_sha(a, "origin", LOCK)) == emitted, (
        "what claim prints must be what the lock records, or propagating it is useless"
    )

    # ...and the hand-it-in direction, which is the other supported way to make them agree.
    _git(a, "push", "origin", f":{LOCK}")
    _git(a, "update-ref", "-d", LOCK)
    handed = _cli_env(a, env, "claim", CONTRACT, "--run-id", "dispatcher-owned-id")
    assert handed.returncode == single_flight.CLAIMED
    assert single_flight._lock_run_id(a, _remote_sha(a, "origin", LOCK)) == "dispatcher-owned-id"


@requires_git
def test_the_printed_release_command_keeps_the_claims_scope(trio):
    """TERRA P1 (ninth pass), 2026-08-21: a handoff command that is wrong for the claim it came
    from is worse than none.

    `_cli` always passes `--repo`, so a bare printed command would target the CURRENT repository's
    `origin` -- a different lock, or none, while the real one stays held. The printed command is
    run verbatim here rather than inspected, which is the only way to prove it works.
    """
    _bare, a, _b = trio
    env = {k: v for k, v in os.environ.items() if k != "DEV_KNOWLEDGE_TELEMETRY_RUN_ID"}
    claimed = _cli_env(a, env, "claim", CONTRACT)
    line = next(ln for ln in claimed.stdout.splitlines()
                if ln.startswith("single_flight: release it with: "))
    printed = line.split("release it with: ", 1)[1]

    assert f'--repo "{a}"' in printed, f"the claim's scope is missing from: {printed}"
    argv = [p.strip('"') for p in re.findall(r'"[^"]*"|\S+', printed)]
    released = subprocess.run([sys.executable, str(_SCRIPT), *argv],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env)
    assert released.returncode == single_flight.CLAIMED, released.stdout + released.stderr
    assert _remote_sha(a, "origin", LOCK) == ""


@requires_git
def test_claim_prints_the_token_its_release_requires(trio):
    """The contract that keeps the refusal above workable: the token is handed over IN FULL, and
    with the command that uses it, so a caller is never left guessing."""
    _bare, a, _b = trio
    env = {k: v for k, v in os.environ.items() if k != "DEV_KNOWLEDGE_TELEMETRY_RUN_ID"}
    claimed = _cli_env(a, env, "claim", CONTRACT)

    token = next(ln.split("=", 1)[1].strip() for ln in claimed.stdout.splitlines()
                 if ln.startswith("single_flight: token="))
    assert len(token) >= 8 and f"--token {token}" in claimed.stdout

    released = _cli_env(a, env, "release", CONTRACT, "--token", token)
    assert released.returncode == single_flight.CLAIMED, released.stdout + released.stderr
    assert _remote_sha(a, "origin", LOCK) == ""


@requires_git
def test_an_exported_run_id_correlates_but_does_not_authorise(trio):
    """The dispatcher's path, and the line between the two identifiers.

    An exported `$DEV_KNOWLEDGE_TELEMETRY_RUN_ID` is inherited by the claim and recorded in the
    lock, which is what makes the lock and that run's telemetry events join up. It does NOT
    authorise the release -- every sibling inherits the same value, so treating it as a capability
    would be treating a broadcast as a secret. The per-claim token still does that job.
    """
    _bare, a, _b = trio
    env = {**os.environ, "DEV_KNOWLEDGE_TELEMETRY_RUN_ID": "dispatch-run-77"}

    claimed = _cli_env(a, env, "claim", CONTRACT)
    assert claimed.returncode == single_flight.CLAIMED
    assert single_flight._lock_run_id(a, _remote_sha(a, "origin", LOCK)) == "dispatch-run-77"

    assert _cli_env(a, env, "release", CONTRACT).returncode == single_flight.NOT_OURS

    token = next(ln.split("=", 1)[1].strip() for ln in claimed.stdout.splitlines()
                 if ln.startswith("single_flight: token="))
    assert token != "dispatch-run-77", "the capability must not be the broadcast id"
    assert _cli_env(a, env, "release", CONTRACT, "--token", token).returncode == \
        single_flight.CLAIMED
    assert _remote_sha(a, "origin", LOCK) == ""


@requires_git
def test_a_release_retried_after_a_failed_remote_leg_still_succeeds(trio):
    """TERRA P1 (second pass), 2026-08-21: a partial release must not strand its own owner.

    The first version deleted the local ref BEFORE pushing. A transient network or auth failure
    then left the remote lock standing and the local evidence gone, and the retry -- with the same
    valid token -- read the remote lock as somebody else's and refused forever. The contract would
    be permanently blocked for the run that legitimately owned it.

    The local ref is removed here to stage exactly that aftermath, and the retry must complete.
    """
    _bare, a, _b = trio
    tok_A = _claim(a)
    _git(a, "update-ref", "-d", LOCK)          # the aftermath of a push that failed mid-release
    assert _remote_sha(a, "origin", LOCK), "the remote lock is still standing"

    assert single_flight.release(CONTRACT, repo=a, remote="origin", token=tok_A) == \
        single_flight.CLAIMED
    assert _remote_sha(a, "origin", LOCK) == "", "the owner must be able to finish its cleanup"


@requires_git
def test_a_lost_acknowledgement_retry_does_not_wedge_the_clone(trio):
    """TERRA P1 (fourth pass), 2026-08-21: the OTHER lost-message shape, and it is the dangerous one.

    The server accepts the remote delete and the client never sees the acknowledgement, so the
    local ref survives for a retry. VERIFIED against git rather than assumed: deleting an absent
    remote ref while carrying a non-empty lease expectation reports
    `! (delete) [rejected] (stale info)` -- not "remote ref does not exist" -- so the retry looks
    exactly like contention. Classifying it as contention returns without clearing the local ref,
    and every later claim in this clone then reports IN_FLIGHT against a lock nobody holds: the
    clone wedged by its own cleanup, with no lock anywhere to explain it.
    """
    _bare, a, _b = trio
    tok_A = _claim(a)
    _git(a, "push", "origin", f":{LOCK}")      # the delete the server accepted
    assert _remote_sha(a, "origin", LOCK) == ""
    assert _git(a, "rev-parse", "--verify", "--quiet", LOCK, check=False).returncode == 0, \
        "the local ref must survive, which is what makes this a retry"

    assert single_flight.release(CONTRACT, repo=a, remote="origin", token=tok_A) == \
        single_flight.CLAIMED
    assert _git(a, "rev-parse", "--verify", "--quiet", LOCK, check=False).returncode != 0, \
        "the stale local ref must be cleared, or the clone is wedged"
    _claim(a)     # a later claim in this clone must not be refused by a ghost lock


@requires_git
def test_a_retry_still_refuses_a_lock_that_is_not_ours(trio):
    """The other half: recovering from a partial release must not become a way to delete anyone's
    lock. With no local ref, ownership is proven from the REMOTE object's run_id, not assumed."""
    _bare, a, b = trio
    _claim(b)
    b_holds = _remote_sha(b, "origin", LOCK)

    assert single_flight.release(CONTRACT, repo=a, remote="origin",
                                 token="a-token-this-lock-never-carried") == \
        single_flight.NOT_OURS
    assert _remote_sha(a, "origin", LOCK) == b_holds


@requires_git
def test_the_shared_worktree_aba_is_refused(trio):
    """TERRA P1 driven through the exact geometry it named: ONE clone, refs shared.

    A claims; the operator clears the lock locally AND remotely (both commands the refusal prints);
    B re-claims in the same clone; A releases with its own token. A must not delete B's lock, and
    the local-ref shortcut is what would have let it.
    """
    _bare, a, _b = trio
    tok_A = _claim(a)

    _git(a, "push", "origin", f":{LOCK}")          # operator clears the remote
    _git(a, "update-ref", "-d", LOCK)              # ...and the local ref, in the same clone

    _claim(a)                                     # the sibling's claim, in the SAME clone
    b_holds = _remote_sha(a, "origin", LOCK)

    assert single_flight.release(CONTRACT, repo=a, remote="origin", token=tok_A) == \
        single_flight.NOT_OURS
    assert _remote_sha(a, "origin", LOCK) == b_holds, (
        "run A released run B's live lock from a SHARED local ref -- the terra P1 exactly"
    )


@requires_git
def test_a_lock_taken_under_another_token_is_refused(trio):
    """Ownership is the per-claim token, and a mismatch is refused (exit 4) with the lock LEFT
    STANDING rather than deleted on the way past."""
    _bare, a, _b = trio
    tok_one = _claim(a)
    held = _remote_sha(a, "origin", LOCK)

    assert single_flight.release(CONTRACT, repo=a, remote="origin",
                                 token="a-different-token") == \
        single_flight.NOT_OURS
    assert _remote_sha(a, "origin", LOCK) == held, "the other run's lock must be left standing"

    assert single_flight.release(CONTRACT, repo=a, remote="origin", token=tok_one) == \
        single_flight.CLAIMED
    assert _remote_sha(a, "origin", LOCK) == ""


@requires_git
def test_the_lock_object_carries_both_the_run_and_the_claim(trio):
    """Two identifiers, two jobs. `run_id` correlates the lock with `[#565]`'s telemetry; `token`
    proves ownership. Conflating them was the defect terra found: a dispatcher exporting one
    run_id around a batch gives every sibling the same value.
    """
    _bare, a, _b = trio
    tok_x = _claim(a, run_id="deadbeefcafe")
    held = _remote_sha(a, "origin", LOCK)
    assert single_flight._lock_run_id(a, held) == "deadbeefcafe"
    assert single_flight._lock_token(a, held) == tok_x


@requires_git
def test_siblings_sharing_one_run_id_still_cannot_release_each_other(trio):
    """TERRA P1 (third pass): the case a run_id-based ownership check cannot see.

    One dispatcher, one exported run_id, two claims of the same contract separated by a manual
    clear -- the ABA between SIBLINGS. Their run_ids are identical by construction, so only the
    per-claim token tells them apart.
    """
    _bare, a, _b = trio
    shared = "one-dispatch-run"
    claim_1 = _claim(a, run_id=shared)
    _git(a, "push", "origin", f":{LOCK}")
    _git(a, "update-ref", "-d", LOCK)
    _claim(a, run_id=shared)                      # the sibling claim, under the SAME run_id
    live = _remote_sha(a, "origin", LOCK)

    assert single_flight._lock_run_id(a, live) == shared, "the siblings do share a run_id"
    assert single_flight.release(CONTRACT, repo=a, remote="origin", token=claim_1) == \
        single_flight.NOT_OURS
    assert _remote_sha(a, "origin", LOCK) == live, "claim 1 released claim 2's live lock"


@requires_git
def test_an_explicit_run_id_becomes_the_ambient_one(trio, monkeypatch):
    """TERRA P1 (third pass), the correlation half: `claim(run_id=X)` must EXPORT X, or telemetry
    emitted afterwards carries a different id and the lock-to-telemetry join the field exists for
    is silently broken for the callers who were most explicit about it.

    `monkeypatch` scopes the environment mutation to this case -- `claim` writes a process global
    by design, and leaking it would pin later cases to one id.
    """
    _bare, a, _b = trio
    monkeypatch.setattr(single_flight._te, "_RUN_ID", None)
    monkeypatch.delenv("DEV_KNOWLEDGE_TELEMETRY_RUN_ID", raising=False)

    single_flight.claim(CONTRACT, repo=a, remote="origin", run_id="explicit-corr-id")
    assert os.environ.get("DEV_KNOWLEDGE_TELEMETRY_RUN_ID") == "explicit-corr-id"
    assert single_flight._te.current_run_id() == "explicit-corr-id"


@requires_git
@pytest.mark.parametrize("hostile", [
    "x\ntoken: injected",          # forge a token field ABOVE the real one
    "x\nrun_id: forged",
    "has space",
    "has:colon",
])
def test_a_run_id_that_could_forge_a_lock_field_is_refused(trio, hostile):
    """TERRA P1 (eighth pass), 2026-08-21: field injection into the lock object.

    The lock message is line-oriented `key: value`, and `run_id` arrives from an environment
    variable and a CLI flag. A value of `x\\ntoken: injected` writes a `token:` line above the
    real one; `_lock_token` reads the first match, returns `injected`, and the legitimate token
    `claim` printed is refused at release -- the contract stays locked until somebody clears it
    by hand. Refused at the source rather than escaped: these are identifiers, and an identifier
    containing a newline is a defect where it was produced.
    """
    _bare, a, _b = trio
    before = os.environ.get("DEV_KNOWLEDGE_TELEMETRY_RUN_ID")
    with pytest.raises(single_flight.SingleFlightError, match="unsafe run_id"):
        single_flight.claim(CONTRACT, repo=a, remote="origin", run_id=hostile)
    assert _remote_sha(a, "origin", LOCK) == "", "a refused claim must leave no lock"
    assert os.environ.get("DEV_KNOWLEDGE_TELEMETRY_RUN_ID") == before, (
        "a REJECTED run_id must not be exported -- the next claim would inherit it and fail on "
        "somebody else's bad input (this is how the tokenless-release case got poisoned)"
    )


@requires_git
def test_a_lock_carrying_no_run_id_is_refused_not_deleted(trio):
    """A ref taken by hand, or by the pre-fix shape, cannot be proven ours.

    Fail-closed: refuse and print how to clear it, rather than delete something unidentified on
    the way past. This is the case that keeps the stale-lock residual an OPERATOR action.
    """
    _bare, a, _b = trio
    _git(a, "push", "origin", f"HEAD:{LOCK}")      # a hand-taken lock: no lock object, no run_id
    _git(a, "fetch", "-q", "origin", f"{LOCK}:{LOCK}")
    assert single_flight.release(CONTRACT, repo=a, remote="origin", token="mine") == \
        single_flight.NOT_OURS
    assert _remote_sha(a, "origin", LOCK), "an unidentified lock must be left standing"


@requires_git
def test_a_tokenless_release_of_an_already_free_lock_succeeds(trio):
    """TERRA P1 (tenth pass), 2026-08-21: the token authorises a DELETION, so requiring one when
    there is nothing to delete turns "already clean" into "cleanup failed".

    That regressed both the documented idempotency and the plain `release <id>` path an operator
    reaches for after the fact. The token stays mandatory wherever a real lock exists -- asserted
    in the same case so the relaxation cannot quietly widen.
    """
    _bare, a, _b = trio
    env = {k: v for k, v in os.environ.items() if k != "DEV_KNOWLEDGE_TELEMETRY_RUN_ID"}

    free = _cli_env(a, env, "release", CONTRACT)
    assert free.returncode == single_flight.CLAIMED, free.stdout + free.stderr
    assert "already free" in free.stdout

    _claim(a)                                     # now a real lock exists
    held = _cli_env(a, env, "release", CONTRACT)
    assert held.returncode == single_flight.NOT_OURS, "a HELD lock still requires the token"
    assert _remote_sha(a, "origin", LOCK), "and it is left standing"


@requires_git
def test_a_genuinely_free_lock_still_reads_as_free(trio):
    """The other half, so the fix cannot be "refuse everything": in a readable repo with no lock
    ref, FREE is the correct answer and release stays idempotent."""
    _bare, a, _b = trio
    assert single_flight.inspect(CONTRACT, repo=a, local_only=True) == single_flight.CLAIMED
    assert single_flight.release(CONTRACT, repo=a, local_only=True,
                                 token="r") == single_flight.CLAIMED
