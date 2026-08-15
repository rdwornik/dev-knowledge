#!/usr/bin/env python
"""single_flight.py — [#530] SINGLE-FLIGHT dispatch guard: one execution of one contract at a time.

WHAT THIS REFUSES. Witnessed 2026-08-14 (`JOURNAL.md` entry (d)): three independent executions of
ONE contract were live at once, two of them independently allocating the same four BACKLOG ids.
They shared neither working tree nor machine. That last clause decides the mechanism — every
filesystem-lock candidate (`filelock`, `portalocker`, a stdlib `O_EXCL` lockfile) is single-host by
construction, so a guard built on one cannot see the collision that was actually observed.

THE MECHANISM — a git ref used as a distributed compare-and-swap:
    claim    git push --force-with-lease=refs/locks/<id>: <remote> HEAD:refs/locks/<id>
    release  git push <remote> :refs/locks/<id>
    inspect  git ls-remote <remote> refs/locks/<id>
The arbiter is the REMOTE — the only substrate two hosts share. The decisive property (research
evidence T2) is that a second clone which has NEVER FETCHED the lock ref is still refused, because
`--force-with-lease` is evaluated by the RECEIVING repo, not by the pusher. The racer does not need
to know the lock exists. No filesystem lock has that property.

THE TRAP THIS EXISTS TO AVOID (T4). A plain `git push <remote> HEAD:refs/locks/<id>` onto an
ALREADY-HELD ref, when both sessions sit at the same commit, prints `Everything up-to-date` and
exits **0**. A naive guard reads that as "lock won" — and same-base is not an edge case, it is the
normal batch-dispatch state where N lanes fork from one HEAD. `--force-with-lease=<ref>:` (empty
expect = "this ref must not exist") is therefore not a hardening detail; it is the whole mechanism.

WHY THE REF POINTS AT HEAD. Under ruling I-D3 a lane commits its contract of record before dispatch,
so HEAD at claim time IS that commit: `git show` on the claimed ref names the holder, its message
and its time. The lock is self-documenting from an artifact the protocol already requires — which
is also why a contract-of-record commit alone is NOT the lock (commits land on separate lane
branches and branches do not contend; three coexisted on 2026-08-11 without noticing each other).

THE LOCAL FAST LEG. `git update-ref --stdin` with the `create` verb gives cross-WORKTREE
single-flight on one clone with no network at all — a second `create` fails `cannot lock ref …:
reference already exists` with **exit 128** (note 128, not 1). `claim` runs it first, so a
same-clone collision is refused before any network call, and `--local-only` is the network-free
pre-check. Do NOT reach for `refs/worktree/…`: evidence T9 proves that namespace is per-worktree
and invisible to the primary — the exact opposite of what a lock needs.

EXIT CODES (`claim`): **0** claimed · **3** already in flight · **2** internal error.
`release` and `inspect` answer 0 / 2 only; neither reports contention, because neither contends.

FAIL **CLOSED** — an internal error exits 2 and the caller must not proceed. Same posture as
`block_ff_push` since the ADR-85 amendment 2026-08-03 §A6, and for the same recorded reason: a
guard that degrades to "allowing" makes a FAILED check indistinguishable from a CLEAN one and
silently auto-allows the exact thing it exists to refuse. Only a rejection git itself attributes to
the lock (`stale info` / `non-fast-forward` / `fetch first`) is read as contention; every other
non-zero is an internal error.

STALE-LOCK RESIDUAL, stated not hidden. **git has no ref TTL.** A lane that dies without releasing
leaves the ref held. This is the ruled option (a): the refusal message prints how to inspect the
holder and how to release it, so a stale lock is a short operator action with the holder's identity
visible — an escape that is loud rather than absent, matching how the repo already treats
`--no-verify`. No timestamp-and-age mechanism is built here.

HONEST LIMITS (per state-honest-enforcement-limits):
  * This is an ADVISORY library + CLI. It is wired into no hook and gates nothing by existing;
    a caller that never invokes it is not refused anything.
  * `claim` needs NETWORK. That is a new precondition on step 0, ruled and recorded on the row,
    not slipped in. `--local-only` degrades to same-clone-only protection and says so.
  * The window between the local create and the remote lease is not atomic. A remote refusal rolls
    the local ref back (guarded by its old value, so only this call's own ref is deleted), but a
    process killed inside that window leaves a local ref that `release` clears.
  * Two claimants of DIFFERENT contract ids never contend — one ref per id is the intended grain.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

CLAIMED = 0
INTERNAL_ERROR = 2
IN_FLIGHT = 3

LOCK_NAMESPACE = "refs/locks/"

# Git attributes a lock-ref rejection with one of these; anything else is an internal error and
# exits 2 (fail closed). `stale info` is the --force-with-lease refusal (T2/T4), `non-fast-forward`
# the plain-push refusal against a different commit (T3), `fetch first` its sibling wording.
_CONTENTION_MARKERS = ("stale info", "non-fast-forward", "fetch first")
# The local leg's own refusal, which arrives as exit 128 rather than 1 (T7) — with THIS wording.
# 128 is git's generic fatal, so both halves are required before a refusal is reported.
_LOCAL_HELD_EXIT = 128
_LOCAL_HELD_MARKER = "already exists"


class SingleFlightError(RuntimeError):
    """Internal failure. Raised, never swallowed — `main` turns it into exit 2."""


_LOCAL_ENV_NAMES: frozenset[str] | None = None


def _local_env_names() -> frozenset[str]:
    """The variables git itself declares repo-LOCAL, asked of git once per process."""
    global _LOCAL_ENV_NAMES
    if _LOCAL_ENV_NAMES is None:
        probe = subprocess.run(["git", "rev-parse", "--local-env-vars"],
                               capture_output=True, text=True, encoding="utf-8")
        if probe.returncode != 0:
            raise SingleFlightError(f"cannot enumerate git local env vars: {probe.stderr.strip()}")
        _LOCAL_ENV_NAMES = frozenset(probe.stdout.split())
    return _LOCAL_ENV_NAMES


def _scrubbed_env() -> dict[str, str]:
    """Child env with git's own repo-LOCAL variables removed.

    `GIT_DIR` overrides BOTH cwd and `-C`, so a value inherited from an invoking hook can point
    this guard at a repository other than the one it was handed — a lock claimed in the wrong repo
    is precisely the failure class here. The names are ENUMERATED BY GIT (`rev-parse
    --local-env-vars`), never blanket-stripped, so nothing outside git's own local set is touched.
    """
    env = {k: v for k, v in os.environ.items() if k not in _local_env_names()}
    # Deterministic message text for the marker match above — git's rejections are gettext-
    # translated, and a localized `stale info` would read as an internal error.
    env["LC_ALL"] = "C"
    # A gate must not hang on a credential prompt: no terminal auth, fail fast into exit 2.
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git(repo: Path, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run git in `repo` and hand back decoded text.

    BYTES ON THE WIRE, decoded here — deliberately, not incidentally. `subprocess.run(text=True)`
    wraps stdin in a TextIOWrapper with `newline=None`, which on Windows rewrites every `\\n` to
    `\\r\\n`; `git update-ref --stdin` then rejects the CR as `fatal: create <ref>: extra input`.
    Witnessed on this host while building the local leg below. Encoding the payload ourselves is
    the fix, and it costs nothing on the no-stdin calls.
    """
    proc = subprocess.run(["git", *args], cwd=str(repo), env=_scrubbed_env(), capture_output=True,
                          input=None if stdin is None else stdin.encode("utf-8"))
    return subprocess.CompletedProcess(proc.args, proc.returncode,
                                       proc.stdout.decode("utf-8", "replace"),
                                       proc.stderr.decode("utf-8", "replace"))


def lock_ref(contract_id: str, repo: Path | str = ".") -> str:
    """`refs/locks/<contract-id>`, validated by git itself rather than by a hand-rolled charset."""
    ref = f"{LOCK_NAMESPACE}{contract_id}"
    if _git(Path(repo), "check-ref-format", ref).returncode != 0:
        raise SingleFlightError(f"not a valid ref name: {ref}")
    return ref


def _refusal(ref: str, holder: str, remote: str | None) -> None:
    """The refusal message. It prints how to INSPECT and how to RELEASE, because git has no TTL
    and the ruled residual (option (a)) is that a stale hold is cleared by a visible operator
    action rather than by a timer."""
    where = f"held by {holder[:8]}" if holder else "held"
    if remote is None:
        inspect_cmd, release_cmd = f"git show {ref}", f"git update-ref -d {ref}"
    else:
        inspect_cmd = f"git fetch {remote} {ref} && git show FETCH_HEAD"
        release_cmd = f"git push {remote} :{ref}"
    print(f"SINGLE-FLIGHT REFUSAL: {ref} already {where} — this contract is already in flight.\n"
          f"  inspect: {inspect_cmd}\n"
          f"  release: {release_cmd}\n"
          f"  (git has no lock TTL. A lane that died without releasing leaves the ref held; the\n"
          f"   two lines above name the holder and clear it.)", file=sys.stderr)


def _head_sha(repo: Path) -> str:
    r = _git(repo, "rev-parse", "HEAD")
    if r.returncode != 0:
        raise SingleFlightError(f"cannot resolve HEAD: {r.stderr.strip()}")
    return r.stdout.strip()


def _local_holder(repo: Path, ref: str) -> str:
    r = _git(repo, "rev-parse", "--verify", "--quiet", ref)
    return r.stdout.strip() if r.returncode == 0 else ""


def _remote_holder(repo: Path, remote: str, ref: str) -> str:
    r = _git(repo, "ls-remote", remote, ref)
    if r.returncode != 0:
        raise SingleFlightError(f"cannot read {remote} {ref}: {r.stderr.strip()}")
    out = r.stdout.split()
    return out[0] if out else ""


def claim(contract_id: str, repo: Path | str = ".", remote: str = "origin",
          local_only: bool = False) -> int:
    """Claim the contract. 0 = claimed · 3 = already in flight · raises on internal failure."""
    repo = Path(repo)
    ref = lock_ref(contract_id, repo)
    sha = _head_sha(repo)

    # Leg 1 — local, network-free, cross-worktree within this clone (T6/T7).
    local = _git(repo, "update-ref", "--stdin", stdin=f"create {ref} {sha}\n")
    if local.returncode == _LOCAL_HELD_EXIT and _LOCAL_HELD_MARKER in local.stderr.lower():
        _refusal(ref, _local_holder(repo, ref), remote=None)
        return IN_FLIGHT
    if local.returncode != 0:
        # 128 is also git's generic fatal, so the MARKER decides, not the code. Reading 128 alone
        # as contention was a live defect here: a malformed `--stdin` payload exits 128 too, and
        # the guard reported a lock that no one held.
        raise SingleFlightError(f"local claim failed: {local.stderr.strip()}")
    if local_only:
        print(f"single_flight: claimed {ref} at {sha[:8]} (LOCAL ONLY — this clone, no remote "
              f"arbitration; a second clone is not refused)")
        return CLAIMED

    # Leg 2 — the remote compare-and-swap. The empty expect after `=<ref>:` means "must not exist";
    # a plain push here would return 0 on the same-HEAD race (T4).
    push = _git(repo, "push", f"--force-with-lease={ref}:", remote, f"HEAD:{ref}")
    if push.returncode == 0:
        print(f"single_flight: claimed {ref} at {sha[:8]} on {remote}")
        return CLAIMED

    # Refused or broken — either way this clone does not hold the lock, so undo leg 1. The old-value
    # argument means only the ref this call created is deleted; a failed rollback is SAID, not
    # swallowed, because the leftover local ref would refuse the next honest claim.
    rollback = _git(repo, "update-ref", "-d", ref, sha)
    if rollback.returncode != 0:
        print(f"single_flight: WARNING — could not roll back the local {ref}: "
              f"{rollback.stderr.strip()} (clear it with: git update-ref -d {ref})", file=sys.stderr)
    blob = f"{push.stderr}\n{push.stdout}".lower()
    if any(marker in blob for marker in _CONTENTION_MARKERS):
        _refusal(ref, _remote_holder(repo, remote, ref), remote)
        return IN_FLIGHT
    raise SingleFlightError(f"remote claim failed: {push.stderr.strip() or push.stdout.strip()}")


def release(contract_id: str, repo: Path | str = ".", remote: str = "origin",
            local_only: bool = False) -> int:
    """Delete the lock ref, locally and (unless local_only) on the remote. IDEMPOTENT: releasing a
    lock that is not held is a success, so a re-run after a partial failure is safe."""
    repo = Path(repo)
    ref = lock_ref(contract_id, repo)
    held = _local_holder(repo, ref)
    if held:
        local = _git(repo, "update-ref", "-d", ref, held)
        if local.returncode != 0:
            raise SingleFlightError(f"local release failed: {local.stderr.strip()}")
    if local_only:
        print(f"single_flight: released {ref} locally")
        return CLAIMED
    push = _git(repo, "push", remote, f":{ref}")
    if push.returncode != 0:
        blob = f"{push.stderr}\n{push.stdout}".lower()
        if "remote ref does not exist" not in blob:
            raise SingleFlightError(f"remote release failed: {push.stderr.strip()}")
        print(f"single_flight: {ref} was not held on {remote} — nothing to release")
        return CLAIMED
    print(f"single_flight: released {ref} on {remote}")
    return CLAIMED


def inspect(contract_id: str, repo: Path | str = ".", remote: str = "origin",
            local_only: bool = False) -> int:
    """Report the holder without contending for it. Exits 0 whether held or free — the answer is
    the printed line, not the code, because inspecting is not claiming."""
    repo = Path(repo)
    ref = lock_ref(contract_id, repo)
    if local_only:
        holder = _local_holder(repo, ref)
        scope, show_cmd, release_cmd = "locally", f"git show {ref}", f"git update-ref -d {ref}"
    else:
        holder = _remote_holder(repo, remote, ref)
        scope = f"on {remote}"
        show_cmd, release_cmd = f"git fetch {remote} {ref} && git show FETCH_HEAD", f"git push {remote} :{ref}"
    if not holder:
        print(f"single_flight: {ref} is FREE {scope}")
        return CLAIMED
    print(f"single_flight: {ref} is HELD {scope} by {holder[:8]}\n"
          f"  show:    {show_cmd}\n"
          f"  release: {release_cmd}")
    return CLAIMED


_VERBS = {"claim": claim, "release": release, "inspect": inspect}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="single_flight.py",
        description="[#530] single-flight dispatch guard — claim/release/inspect refs/locks/<id>.")
    parser.add_argument("verb", choices=sorted(_VERBS))
    parser.add_argument("contract_id", help="the contract id; the lock is refs/locks/<contract_id>")
    parser.add_argument("--repo", default=".", help="repository to operate in (default: cwd)")
    parser.add_argument("--remote", default="origin", help="remote acting as arbiter (default: origin)")
    parser.add_argument("--local-only", action="store_true",
                        help="skip the remote leg — same-clone protection only, no network")
    args = parser.parse_args(argv)
    try:
        return _VERBS[args.verb](args.contract_id, repo=args.repo, remote=args.remote,
                                 local_only=args.local_only)
    except SingleFlightError as exc:
        print(f"single_flight: internal error — {exc}", file=sys.stderr)
        return INTERNAL_ERROR
    except OSError as exc:  # git missing, unreadable cwd — still a refusal, never a silent allow
        print(f"single_flight: internal error — {exc}", file=sys.stderr)
        return INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
