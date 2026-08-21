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

THE TRAP THIS EXISTS TO AVOID (T4), AND HOW MUCH FURTHER IT GOES THAN RECORDED. A plain
`git push <remote> HEAD:refs/locks/<id>` onto an ALREADY-HELD ref, when both sessions sit at the
same commit, prints `Everything up-to-date` and exits **0**. A naive guard reads that as "lock won"
— and same-base is not an edge case, it is the normal batch-dispatch state where N lanes fork from
one HEAD.

**MEASURED HERE, 2026-08-15, git 2.55.0.windows.3: `--force-with-lease=<ref>:` DOES NOT CLOSE THAT
CASE ON ITS OWN.** The lease is genuinely evaluated when the pushed value differs from the held one
(`! [rejected] … (stale info)`, exit 1 — the recorded T2/T3 behaviour, reproduced), but when the
racer's HEAD *equals* the held value git short-circuits to `= [up to date]` and exit **0** before
the lease decides. The design sketch's own exit-code test (`if r.returncode == 0: return 0`)
therefore greenlights the same-HEAD race — the exact race it was written against.

So the mechanism here is the lease PLUS a machine-readable verdict: the push runs with
`--porcelain`, and a claim counts as WON only when git reports the flag `*` (`[new reference]`) for
the lock ref. `=` (`[up to date]`) means somebody already holds it at this value and is refused;
`!` carrying a lock-attributable reason is refused; anything else is an internal error. The exit
code is not the verdict — the status flag is. Flags are single characters git does not translate,
so this survives a localized git in a way prose matching does not.

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
`release`: **0** free · **4** held by a DIFFERENT run, left standing · **2** internal error.
`inspect` answers 0 / 2 only — it does not contend, and the answer is the printed line.

THE LOCK REF POINTS AT A run_id-BEARING OBJECT, NOT AT HEAD ([#530] race (a), ruling R6(d)). It
pointed at HEAD until 2026-08-21, and that was the defect: the racers this guard exists for SHARE
HEAD, so two claims produced the same ref value and no compare-and-swap could tell them apart.
`claim` now builds a commit carrying `[#565]`'s `run_id` (parented on HEAD, so `git show <ref>`
still names the contract-of-record commit AND now the run that took the lock), and `release`
compares-and-swaps on it — locally via `update-ref -d <ref> <sha>`, remotely via
`--force-with-lease=<ref>:<sha>` on the DELETE. A lock that cannot be proven ours is refused and
left standing rather than deleted on the way past.

**`release` REQUIRES THE PER-CLAIM TOKEN** (`--token`, printed by `claim`; no environment
fallback). This is not ceremony — it is the only thing that can prove ownership. Refs live in the
COMMON git dir, so every WORKTREE of one clone shares them, and a release that trusted the local
ref would delete a sibling worktree's live lock after a manual clear and a re-claim: the ABA
again, through the guard. Nothing this module could persist would help, since any such file is
equally clone-wide and equally overwritten by the next claim; and an env var would be inherited by
every sibling, which is the same sharing. A capability is held, not broadcast.

The lock object also records `[#565]`'s `run_id`, which is a DIFFERENT job: correlation, so a lock
and the telemetry events of the run that took it join up. Ownership is the token; correlation is
the run_id. Using one for both was a defect (terra, 2026-08-21) — a dispatcher exporting one
run_id around a batch gives every sibling the same value.

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
import importlib.util
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

# `[#565]`'s run_id is the generation-unique token race (a) needs, and reusing it rather than
# minting a second one is what makes a lock and the telemetry events of the run that took it
# correlate. Loaded BY PATH for the reason `telemetry_emit` states about `gitenv.py`: `import
# telemetry_emit` and `from scripts import telemetry_emit` each have a shadow hole, and ordering
# them only moves it. Unconditional at import, like that precedent -- the two modules ship
# together in `scripts/`, telemetry_emit has no third-party dependency, and a guard that silently
# minted its own id would put two id namespaces in one store.
_te_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_telemetry_emit", Path(__file__).resolve().with_name("telemetry_emit.py"))
_te = importlib.util.module_from_spec(_te_spec)
_te_spec.loader.exec_module(_te)

CLAIMED = 0
INTERNAL_ERROR = 2
IN_FLIGHT = 3
#: `release` refused: the lock is held by a DIFFERENT run. Distinct from 2 on purpose -- this is a
#: policy refusal, not a crash, and this module already argues (see `block_ff_push._emit_verdict`)
#: that conflating the two inflates every "what did this gate refuse" count with the gate's own
#: bugs. `[#530]` race (a).
NOT_OURS = 4

LOCK_NAMESPACE = "refs/locks/"

#: The `[#565]` correlation id, embedded in the lock object so a lock and the telemetry events of
#: the run that took it join up. Read back with `_lock_run_id`; matched at the start of a line.
_RUN_ID_FIELD = "run_id: "

#: The OWNERSHIP token, embedded beside it and minted PER CLAIM. Separate from `run_id` on
#: purpose, and the separation is a correction (terra review, 2026-08-21): a dispatcher that
#: exports one `run_id` around a whole batch gives every sibling the SAME id, so a run_id-based
#: ownership check cannot tell two siblings apart and the ABA reopens between them. A run_id
#: identifies a RUN; releasing a lock requires proving you are the CLAIM. A per-claim nonce is
#: still the generation-unique token R6(d) calls for -- it is the generation part of it.
_TOKEN_FIELD = "token: "

#: What a lock field value may contain. The lock message is line-oriented `key: value`, so a
#: value carrying a newline (or a colon) can forge a second field -- see `_reject_unsafe_field`.
_SAFE_FIELD = re.compile(r"[A-Za-z0-9._-]{1,128}")

#: Identity for the lock OBJECT. Fixed, so a lock is a machine artifact rather than a record of
#: whoever happened to hold it: `commit-tree` fails outright where `user.email` is unset (a hook
#: on a fresh CI checkout), and a lock that cannot be taken because git has no name for you is a
#: guard that refuses honest work.
_LOCK_IDENTITY = ("-c", "user.name=single-flight", "-c", "user.email=single-flight@localhost")

# `git push --porcelain` prints one `<flag>\t<from>:<to>\t<summary>` line per ref. The flag is a
# single untranslated character, which is why the verdict is read from it and not from the exit
# code or the prose: `*` new reference (the claim is WON), `=` already at this value (held — the
# same-HEAD race, which exits 0), `!` rejected.
_PUSH_NEW, _PUSH_UP_TO_DATE, _PUSH_REJECTED = "*", "=", "!"
# Reasons a `!` is attributable to the lock rather than to something broken; anything else is an
# internal error and exits 2 (fail closed). `stale info` is the --force-with-lease refusal (T2),
# `non-fast-forward` the plain-push refusal against a different commit (T3), `fetch first` its
# sibling wording.
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


def _scope_flags(repo: Path, remote: str, local_only: bool) -> str:
    """The claim's non-default scope, rendered as flags, so the printed release command targets
    what was actually claimed.

    Terra P1, 2026-08-21: a claim made with `--repo`/`--remote`/`--local-only` printed a bare
    release command, and following it operates on the CURRENT repository's `origin` -- a different
    lock, or none, while the real one stays held. A handoff command that is wrong for the claim it
    came from is worse than no handoff command.
    """
    parts = []
    if str(repo) not in (".", ""):
        parts.append(f' --repo "{repo}"')
    if local_only:
        parts.append(" --local-only")
    elif remote != "origin":
        parts.append(f" --remote {remote}")
    return "".join(parts)


def _claim_announce(contract_id: str, token: str, run_id: str, scope: str = "") -> None:
    """Hand the caller the token its `release` will require, IN FULL and machine-readably.

    Printed rather than persisted, because persisting it is the trap: any file this module could
    write would live in the clone, be shared by every worktree, and be overwritten by the next
    claim -- so it would vouch for the wrong claim, which is the ABA again. The capability belongs
    to the claim, so the claim's caller is the only thing that can carry it.

    THE run_id IS EMITTED TOO, machine-readably, and that is a fix rather than decoration (terra,
    2026-08-21). `claim` runs as a SHORT-LIVED SUBPROCESS in the live dispatch flow, and the lane
    is launched afterwards by a separate command -- so exporting the id inside the claim process
    reaches nothing. Unless the dispatcher makes the two agree, the lock records one id and the
    lane's telemetry mints another, and the lock-to-telemetry correlation is silently lost. Two
    ways to make them agree, both supported here and NEITHER of them wired by this module (which
    launches nothing):

        # (a) the dispatcher owns the id and hands it to both
        single_flight.py claim <id> --run-id $RUN && DEV_KNOWLEDGE_TELEMETRY_RUN_ID=$RUN <lane>
        # (b) the dispatcher reads back what the claim minted
        RUN=$(single_flight.py claim <id> | sed -n 's/^single_flight: run_id=//p')
    """
    print(f"single_flight: token={token}")
    print(f"single_flight: run_id={run_id}")
    print(f"single_flight: release it with: release {contract_id} --token {token}{scope}")


def _no_token(ref: str, contract_id: str, remote: str | None) -> None:
    """`release` refusing because the caller carried no run token. `[#530]` race (a).

    Refusing here rather than falling back to the local ref is the whole correction: worktrees of
    one clone SHARE refs, so the local ref cannot tell "the lock I took" from "the lock a sibling
    worktree took after mine was cleared". Deleting on that basis is the ABA.
    """
    scope = "" if remote is None else f" {remote}"
    print(f"SINGLE-FLIGHT REFUSAL: not releasing {ref}{scope} — no ownership token was supplied, "
          f"so ownership cannot be proven.\n"
          f"  A lock is released by the CLAIM that took it. `claim` prints that claim's token; "
          f"pass it back:\n"
          f"    single_flight.py release {contract_id} --token <token>\n"
          f"  There is deliberately no environment fallback: an env var is inherited by every\n"
          f"  sibling, and a shared capability proves nothing.\n"
          f"  (Worktrees of one clone SHARE refs, so the local ref is not proof of ownership\n"
          f"  either — releasing on it can delete a sibling's live lock.)", file=sys.stderr)


def _not_ours(ref: str, holder: str, owner: str | None, remote: str | None) -> None:
    """`release` refusing to delete a lock this run does not hold. `[#530]` race (a).

    Prints WHY it is not ours -- a different run_id, or none at all -- because "refused" without
    that is indistinguishable from the guard being broken, and an operator who cannot tell the
    two apart clears the lock by hand and reopens the race.
    """
    if owner is None:
        whose = "it carries no run_id (taken by hand, or before this guard tokenised locks)"
    else:
        whose = f"it belongs to run {owner[:8]}"
    if remote is None:
        inspect_cmd, release_cmd = f"git show {ref}", f"git update-ref -d {ref}"
    else:
        inspect_cmd = f"git fetch {remote} {ref} && git show FETCH_HEAD"
        release_cmd = f"git push {remote} :{ref}"
    print(f"SINGLE-FLIGHT REFUSAL: not releasing {ref} at {holder[:8]} — {whose}, not this run.\n"
          f"  The lock is LEFT STANDING. Deleting another run's lock would put two executions of\n"
          f"  one contract in flight, which is what this guard exists to refuse.\n"
          f"  inspect: {inspect_cmd}\n"
          f"  release: {release_cmd}   (only if you have established it is dead)", file=sys.stderr)


def _push_status(stdout: str, ref: str) -> tuple[str, str]:
    """The `--porcelain` status flag and summary for `ref`, or ('', '') if git reported none.

    An absent line is NOT read as success anywhere above — a claim requires the `*` flag, so a
    missing status falls through to the internal-error path and exits 2.
    """
    for line in stdout.splitlines():
        fields = line.split("\t")
        if len(fields) >= 3 and fields[1].endswith(f":{ref}"):
            return fields[0].strip(), fields[2]
    return "", ""


def _head_sha(repo: Path) -> str:
    r = _git(repo, "rev-parse", "HEAD")
    if r.returncode != 0:
        raise SingleFlightError(f"cannot resolve HEAD: {r.stderr.strip()}")
    return r.stdout.strip()


def _reject_unsafe_field(name: str, value: str) -> None:
    """Refuse a field value that could forge the lock object's `key: value` encoding.

    Terra P1, 2026-08-21, and it is a real forgery rather than a tidiness rule: the lock message
    is line-oriented, so a `run_id` of `x\\ntoken: injected` writes a `token:` line ABOVE the real
    one. `_lock_token` reads the first match, so it returns `injected`, and the legitimate token
    `claim` printed is then refused at release -- the contract stays locked until somebody clears
    it by hand. `run_id` is attacker-adjacent in the way that matters here: it comes from an
    environment variable and a CLI flag.

    Refusing beats escaping. The values this module mints are hex; anything a caller supplies is
    an identifier, and an identifier with a newline (or a space, or a colon) in it is a defect at
    the source rather than something to encode around.
    """
    if not value or not _SAFE_FIELD.fullmatch(value):
        raise SingleFlightError(
            f"unsafe {name} {value!r}: expected a non-empty identifier matching "
            f"{_SAFE_FIELD.pattern} -- the lock object's fields are line-oriented, so a value "
            f"carrying a newline or a colon can forge another field"
        )


def lock_object(repo: Path, contract_id: str, run_id: str, token: str) -> str:
    """Build the object the lock ref points at: a commit carrying `run_id`, parented on HEAD.

    `[#530]` race (a), ruling R6(d) -- "release compares-and-swaps on run_id, never on branch
    tip". THE REF USED TO POINT AT HEAD, and that is the whole defect: the racers this guard
    exists for share HEAD (N lanes forking from one commit is the normal batch-dispatch state,
    and this module's own docstring says so), so the ref value could not identify WHO held the
    lock. Two claims produced the same value and no compare-and-swap could tell them apart.

    A commit whose message carries the run_id is generation-unique -- different run_id, different
    message, different sha (verified 2026-08-21) -- so the ref value BECOMES the identity, and
    `--force-with-lease` can then guard the delete as well as the create.

    The self-documenting property the old shape had is kept and widened rather than traded away:
    the lock commit is parented on HEAD, so `git show <ref>` still names the contract-of-record
    commit, its message and its time, and now also names the run that took the lock.
    """
    head = _head_sha(repo)
    _reject_unsafe_field("run_id", run_id)
    _reject_unsafe_field("token", token)
    message = (f"single-flight lock: {contract_id}\n\n"
               f"{_RUN_ID_FIELD}{run_id}\n{_TOKEN_FIELD}{token}\n")
    r = _git(repo, *_LOCK_IDENTITY, "commit-tree", f"{head}^{{tree}}", "-p", head, "-m", message)
    if r.returncode != 0:
        raise SingleFlightError(f"cannot build the lock object: {r.stderr.strip()}")
    sha = r.stdout.strip()
    if not sha:
        raise SingleFlightError("git commit-tree returned no object")
    return sha


def _lock_field(repo: Path, sha: str, field: str) -> str | None:
    """One `<field>: <value>` line out of the lock object at `sha`, or `None` if it carries none.

    `None` is NOT read as "mine" anywhere. A ref pointing at something this module did not write
    -- a lock taken by the pre-`[#530]`-fix shape, or by hand -- cannot be proven ours, and the
    fail-closed answer is to refuse and let the operator clear it with the two commands the
    refusal message prints.
    """
    r = _git(repo, "cat-file", "commit", sha)
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        if line.startswith(field):
            return line[len(field):].strip() or None
    return None


def _lock_run_id(repo: Path, sha: str) -> str | None:
    """The `[#565]` correlation id in the lock object -- what it is FOR, not what proves it ours."""
    return _lock_field(repo, sha, _RUN_ID_FIELD)


def _lock_token(repo: Path, sha: str) -> str | None:
    """The per-claim OWNERSHIP token in the lock object. This is the one `release` compares."""
    return _lock_field(repo, sha, _TOKEN_FIELD)


def resolve_ref_once(repo: Path, ref: str) -> str | None:
    """Resolve `ref` to a sha, ONCE, as a TRI-STATE. `[#530]` race (b), ruling R6(d).

    `<sha>` -> held. `None` -> genuinely absent. Anything else RAISES, and that third branch is
    the entire point: the previous `_local_holder` mapped every non-zero exit onto "absent", so a
    repository git could not read at all was reported as a FREE lock. `inspect --local-only`
    printed FREE and `release --local-only` reported success, neither having read any state --
    a guard whose failure mode is indistinguishable from its clean state, which is the fail-OPEN
    shape this module rejects everywhere else.

    R6(d) rules that resolve-once is SEPARATED from `rev-parse`, and this function is that
    separation: the git call is an implementation detail behind a three-valued answer, and every
    caller resolves ONCE and passes the value down rather than re-asking.

    WHY `rev-parse --verify --quiet` AND NOT `show-ref --verify`, measured 2026-08-21 on git
    2.55.0.windows.3 rather than assumed -- the obvious alternative re-introduces the bug:

        rev-parse --verify --quiet  existing -> 0   missing -> 1     unreadable -> 128
        show-ref  --verify          existing -> 0   missing -> 128   unreadable -> 128

    `show-ref` answers "missing" and "unreadable" with the SAME code, so a tri-state built on it
    would collapse right back into the conflation it was written to fix.
    """
    r = _git(repo, "rev-parse", "--verify", "--quiet", ref)
    if r.returncode == 0:
        sha = r.stdout.strip()
        if not sha:
            raise SingleFlightError(f"git reported {ref} as resolvable but returned no sha")
        return sha
    if r.returncode == 1:
        return None
    raise SingleFlightError(
        f"cannot resolve {ref} in {repo}: git exited {r.returncode} "
        f"({r.stderr.strip() or 'no stderr'}). Refusing to report a lock state that was never "
        f"read -- 'could not ask' is not 'nothing was there'"
    )


def _remote_lock_token(repo: Path, remote: str, ref: str, sha: str) -> str | None:
    """The ownership token inside the lock object the REMOTE holds, fetching it if absent here.

    The retry path needs this: once a partial release has removed the local ref, the only way to
    tell "my own lock, still standing after a failed push" from "somebody else's" is to read the
    object. `None` means unidentified, and unidentified is never treated as ours.
    """
    owner = _lock_token(repo, sha)
    if owner is not None:
        return owner
    fetch = _git(repo, "fetch", "--quiet", remote, ref)
    if fetch.returncode != 0:
        raise SingleFlightError(
            f"cannot read the lock object {sha[:8]} from {remote}: {fetch.stderr.strip()}")
    return _lock_token(repo, sha)


def _remote_holder(repo: Path, remote: str, ref: str) -> str:
    r = _git(repo, "ls-remote", remote, ref)
    if r.returncode != 0:
        raise SingleFlightError(f"cannot read {remote} {ref}: {r.stderr.strip()}")
    out = r.stdout.split()
    return out[0] if out else ""


def claim(contract_id: str, repo: Path | str = ".", remote: str = "origin",
          local_only: bool = False, run_id: str | None = None) -> int:
    """`claim_token()` discarding the token — the CLI's entry point, where the token reaches the
    caller on stdout. A programmatic caller that needs to release later wants `claim_token()`."""
    return claim_token(contract_id, repo=repo, remote=remote, local_only=local_only,
                       run_id=run_id)[0]


def claim_token(contract_id: str, repo: Path | str = ".", remote: str = "origin",
                local_only: bool = False, run_id: str | None = None) -> tuple[int, str | None]:
    """Claim the contract, returning `(exit_code, token)`. 0 = claimed · 3 = already in flight ·
    raises on internal failure. `token` is `None` unless the claim was WON.

    THE TOKEN IS ALWAYS MINTED HERE AND IS NOT CALLER-PINNABLE, which is the point of returning
    it rather than accepting it (terra, 2026-08-21). A `token=` parameter would let a caller reuse
    one value across two claims, and two claims sharing a token are indistinguishable to
    `release` — the shared-clone ABA again, arriving through the supported API. A capability that
    the holder can duplicate is not a capability. The CLI never sees this function: it uses
    `claim()`, and the token reaches the operator on stdout, which is the one channel that hands
    it to the claimer and nobody else.

    TWO IDENTIFIERS, doing two different jobs — conflating them was a defect (terra, 2026-08-21):

      * `run_id` — `[#565]`'s CORRELATION id, so the lock and the telemetry events of the run that
        took it join up. Defaults to `current_run_id()`, which inherits
        `$DEV_KNOWLEDGE_TELEMETRY_RUN_ID`. Supplying it explicitly also EXPORTS it, so telemetry
        emitted later in this process tree carries the id the lock records rather than a second
        one — otherwise the correlation this field exists for is silently broken for exactly the
        callers who were most explicit about it.
      * the returned `token` — the per-claim OWNERSHIP capability `release` requires. Minted
        fresh here every time. It is NOT the run_id, because a dispatcher exporting one run_id
        around a batch gives every sibling the same value, and an ownership check that cannot
        tell two siblings apart is the ABA again.
    """
    repo = Path(repo)
    ref = lock_ref(contract_id, repo)
    if run_id:
        # VALIDATE BEFORE EXPORTING. The export makes this the ambient id for everything
        # downstream, so exporting first and validating later leaves a rejected value in the
        # environment where the NEXT claim inherits it and fails on somebody else's bad input.
        # (Caught by the tokenless-release test, which was poisoned by a sibling case's hostile
        # value in exactly this way.) Truthiness, not `is not None`: an empty string means "not
        # supplied" everywhere else here.
        _reject_unsafe_field("run_id", run_id)
        os.environ[_te.RUN_ID_ENV] = run_id
    run_id = run_id or _te.current_run_id()
    token = uuid.uuid4().hex
    # The object carrying both. NOT HEAD — see `lock_object`.
    sha = lock_object(repo, contract_id, run_id, token)

    # Leg 1 — local, network-free, cross-worktree within this clone (T6/T7).
    local = _git(repo, "update-ref", "--stdin", stdin=f"create {ref} {sha}\n")
    if local.returncode == _LOCAL_HELD_EXIT and _LOCAL_HELD_MARKER in local.stderr.lower():
        _refusal(ref, resolve_ref_once(repo, ref) or "", remote=None)
        return IN_FLIGHT, None
    if local.returncode != 0:
        # 128 is also git's generic fatal, so the MARKER decides, not the code. Reading 128 alone
        # as contention was a live defect here: a malformed `--stdin` payload exits 128 too, and
        # the guard reported a lock that no one held.
        raise SingleFlightError(f"local claim failed: {local.stderr.strip()}")
    if local_only:
        print(f"single_flight: claimed {ref} at {sha[:8]} (LOCAL ONLY — this clone, no remote "
              f"arbitration; a second clone is not refused)")
        _claim_announce(contract_id, token, run_id,
                        _scope_flags(repo, remote, local_only=True))
        return CLAIMED, token

    # Leg 2 — the remote compare-and-swap. The empty expect after `=<ref>:` means "must not exist".
    # The claim is won ONLY on the porcelain flag `*`: exit 0 also covers `= [up to date]`, which is
    # the same-HEAD race arriving as a success (measured, see the module docstring).
    push = _git(repo, "push", "--porcelain", f"--force-with-lease={ref}:", remote, f"{sha}:{ref}")
    flag, summary = _push_status(push.stdout, ref)
    if push.returncode == 0 and flag == _PUSH_NEW:
        print(f"single_flight: claimed {ref} at {sha[:8]} on {remote}")
        _claim_announce(contract_id, token, run_id,
                        _scope_flags(repo, remote, local_only=False))
        return CLAIMED, token

    # Refused or broken — either way this clone does not hold the lock, so undo leg 1. The old-value
    # argument means only the ref this call created is deleted; a failed rollback is SAID, not
    # swallowed, because the leftover local ref would refuse the next honest claim.
    rollback = _git(repo, "update-ref", "-d", ref, sha)
    if rollback.returncode != 0:
        print(f"single_flight: WARNING — could not roll back the local {ref}: "
              f"{rollback.stderr.strip()} (clear it with: git update-ref -d {ref})", file=sys.stderr)
    contended = flag == _PUSH_UP_TO_DATE or (
        flag == _PUSH_REJECTED and any(m in summary.lower() for m in _CONTENTION_MARKERS))
    if contended:
        _refusal(ref, _remote_holder(repo, remote, ref), remote)
        return IN_FLIGHT, None
    raise SingleFlightError(f"remote claim failed: {push.stderr.strip() or push.stdout.strip()}")


def release(contract_id: str, repo: Path | str = ".", remote: str = "origin",
            local_only: bool = False, token: str | None = None) -> int:
    """Release the lock THIS RUN holds. 0 = free · 4 = held by a different run · raises on error.

    IDEMPOTENT where it should be: releasing a lock nobody holds is still a success, so a re-run
    after a partial failure is safe. What is no longer a success is deleting SOMEBODY ELSE'S
    lock, which is `[#530]` race (a).

    THE ABA, and why a value guard alone never closed it. The witnessed order is: A claims; the
    lock looks stale so an operator clears it BY HAND (the escape this module's own refusal
    message prints, so a supported action); B legitimately re-claims; A finishes and cleans up.
    A's cleanup was a bare `git push <remote> :<ref>` — an unguarded delete that carries no
    expectation and therefore always wins — so it deleted B's LIVE lock and put two executions of
    one contract in flight THROUGH the guard rather than around it. Guarding on the ref's value
    would not have helped either, because while the ref pointed at HEAD both locks HAD the same
    value: the racers share HEAD by construction.

    THE FIX, per R6(d): the ref points at a run_id-bearing object (`lock_object`), so the ref
    VALUE is the run's identity, and the delete compares-and-swaps on it:

      * remote — `push --force-with-lease=<ref>:<sha> <remote> :<ref>`, where `<sha>` is the lock
        object THIS clone put there. Verified 2026-08-21 that the lease guards a DELETE and not
        only a create: a wrong expectation yields `! [rejected] (stale info)` with the remote ref
        INTACT, the right one yields `- [deleted]`. This is the leg that closes the ABA — after
        the manual clear the remote holds B's object, our expectation names A's, and git refuses;
      * local — `update-ref -d <ref> <sha>`, value-guarded, so only the ref this clone created is
        removed.

    WHAT PROVES OWNERSHIP: the per-claim TOKEN, carried by the caller from claim to release.
    Nothing else can, and three tempting shortcuts were tried here and all three are wrong:

      * "the run_id proves it" — FALSE when it matters most. A dispatcher that exports one
        `$DEV_KNOWLEDGE_TELEMETRY_RUN_ID` around a batch gives every sibling the SAME id, so an
        ownership check on it cannot tell two siblings apart and the ABA reopens between them.
        `run_id` identifies a RUN; releasing requires proving you are the CLAIM. So the lock
        object carries both and they are compared for different purposes. (terra, 2026-08-21.)

      * "the local ref proves it" — FALSE, and it is false in exactly this repo's shape. Refs live
        in the COMMON git dir, so every worktree of one clone shares them. Run A holding a stale
        local ref, an operator clearing the lock, and run B re-claiming in a sibling worktree
        leaves A's release resolving B's ref, deleting it, and then handing B's OWN sha to the
        remote lease as its expectation — which matches, so the lease waves it through and B's
        live lock dies. That reproduces the ABA THROUGH the fix meant to close it. (Found by the
        terra review of this lane, 2026-08-21, after this function had been written that way.)
      * "mint one if absent" — worse: it invents an identity and then measures ownership against
        it, which is the same as not checking.

    So a release with NO token is REFUSED (exit 4) before anything is touched, and the refusal
    prints how to supply one. `claim` prints the token and the exact release command for that
    reason. It is deliberately a required ARGUMENT with no environment fallback: an env var is
    inherited by every sibling of the process that set it, which is precisely the sharing that
    makes an ownership check meaningless. A capability is held, not broadcast.

    A lock this module cannot prove is ours is REFUSED and left standing (exit 4), never deleted
    on the way past. The stale-lock residual is unchanged and still the ruled option (a): git has
    no TTL, so a genuinely dead lock is cleared by a visible operator action, and the refusal
    prints the two commands that do it.
    """
    repo = Path(repo)
    ref = lock_ref(contract_id, repo)
    # A token the caller HANDED OVER, and nothing else. No env fallback (siblings would share it)
    # and nothing minted here (that would invent an identity and then measure ownership against
    # it, which is the same as not checking).
    declared = token.strip() if isinstance(token, str) and token.strip() else None

    local_held = resolve_ref_once(repo, ref)  # tri-state: raises rather than guessing (race (b))

    # NOTHING HELD is an idempotent SUCCESS, and it needs no token. Terra P1, 2026-08-21: the
    # token authorises a DELETION, so demanding one when there is nothing to delete turns
    # "already clean" into "cleanup failed" -- which breaks this function's documented
    # re-runnability and the plain `release <id>` path an operator uses after the fact. The token
    # is required from here on, where a real lock exists to be removed.
    if local_held is None and (local_only or not _remote_holder(repo, remote, ref)):
        where = "locally" if local_only else f"on {remote}"
        print(f"single_flight: {ref} is already free {where}")
        return CLAIMED

    if declared is None:
        _no_token(ref, contract_id, None if local_only else remote)
        return NOT_OURS

    if local_held is not None:
        owner = _lock_token(repo, local_held)
        if owner != declared:
            _not_ours(ref, local_held, owner, None if local_only else remote)
            return NOT_OURS

    if local_only:
        if local_held is not None:
            local = _git(repo, "update-ref", "-d", ref, local_held)
            if local.returncode != 0:
                raise SingleFlightError(f"local release failed: {local.stderr.strip()}")
        print(f"single_flight: {ref} is now free locally")
        return CLAIMED

    # THE REMOTE LEG RUNS FIRST, and the local ref is cleared only after it succeeds. Terra P1,
    # 2026-08-21: deleting locally first destroys the very evidence a retry needs. A transient
    # network or auth failure on the push would leave the remote ref standing and the local one
    # gone, and the retry -- with the SAME valid token -- would then read the remote lock as
    # somebody else's and refuse forever, blocking the contract for the run that legitimately
    # owns it. Ordering the legs this way makes the documented "safe to re-run after a partial
    # failure" true rather than aspirational.
    expected = local_held
    if expected is None:
        # No local ref to swap against -- a prior partial release, or an operator who cleared it.
        # Ask the remote, and PROVE ownership from the object itself rather than assuming either
        # way: absent is the idempotent success, ours is a legitimate retry, anyone else's is
        # refused.
        remote_sha = _remote_holder(repo, remote, ref)
        if not remote_sha:
            print(f"single_flight: {ref} is now free on {remote}")
            return CLAIMED
        owner = _remote_lock_token(repo, remote, ref, remote_sha)
        if owner != declared:
            _not_ours(ref, remote_sha, owner, remote)
            return NOT_OURS
        expected = remote_sha

    push = _git(repo, "push", "--porcelain", f"--force-with-lease={ref}:{expected}", remote,
                f":{ref}")
    if push.returncode != 0:
        blob = f"{push.stderr}\n{push.stdout}".lower()
        if "remote ref does not exist" in blob:
            pass                                    # already gone; the local ref still comes off
        elif any(m in blob for m in _CONTENTION_MARKERS):
            # The lease refused, which has TWO causes and they need different answers. Terra P1,
            # 2026-08-21, verified against git rather than assumed: deleting an ABSENT remote ref
            # while carrying a non-empty expectation reports `! (delete) [rejected] (stale info)`
            # -- NOT "remote ref does not exist". So the lost-ack retry (the server accepted the
            # delete, the client saw a network failure, the local ref survived for the retry)
            # arrives here looking exactly like contention. Reading it as contention returns
            # without clearing the local ref, and every later claim in this clone then reports
            # IN_FLIGHT against a lock nobody holds -- the clone wedged by its own cleanup.
            still_held = _remote_holder(repo, remote, ref)
            if still_held:
                # Genuine contention: somebody else's lock is standing and stays that way, and
                # ours is left alone too -- said loudly rather than reported as a clean release.
                _not_ours(ref, still_held, None, remote)
                return NOT_OURS
            # Absent: the goal state is reached however it got there. Fall through and clear the
            # local ref, which is the half that would otherwise strand.
        else:
            raise SingleFlightError(f"remote release failed: {push.stderr.strip()}")

    if local_held is not None:
        local = _git(repo, "update-ref", "-d", ref, local_held)
        if local.returncode != 0:
            raise SingleFlightError(f"local release failed: {local.stderr.strip()}")
    # "is now free", not "released": a delete of a ref that was never held reports `- [deleted]`
    # and exit 0 against GitHub (measured 2026-08-15), so the outcome is knowable and the action
    # is not. The freed state is what the caller acts on, so that is what gets claimed.
    print(f"single_flight: {ref} is now free on {remote}")
    return CLAIMED


def inspect(contract_id: str, repo: Path | str = ".", remote: str = "origin",
            local_only: bool = False) -> int:
    """Report the holder without contending for it. Exits 0 whether held or free — the answer is
    the printed line, not the code, because inspecting is not claiming."""
    repo = Path(repo)
    ref = lock_ref(contract_id, repo)
    if local_only:
        holder = resolve_ref_once(repo, ref) or ""
        scope, show_cmd, release_cmd = "locally", f"git show {ref}", f"git update-ref -d {ref}"
    else:
        holder = _remote_holder(repo, remote, ref)
        scope = f"on {remote}"
        show_cmd, release_cmd = f"git fetch {remote} {ref} && git show FETCH_HEAD", f"git push {remote} :{ref}"
    if not holder:
        print(f"single_flight: {ref} is FREE {scope}")
        return CLAIMED

    # NAME THE GUARDED PATH FIRST. Until 2026-08-21 this printed only the raw delete, and a raw
    # delete is exactly what race (a) is about: it carries no expectation, so it removes whatever
    # is there -- including a lock somebody else took after this one looked stale. Since `release`
    # now compares-and-swaps, the guarded path is the correct one whenever the claim's token is to
    # hand, and the raw delete is demoted to what it always was: the ruled stale-lock ESCAPE
    # (option (a)), for when the claimant is gone and its token with it.
    owner_run = _lock_run_id(repo, holder) if local_only else None
    whose = f" (run {owner_run})" if owner_run else ""
    scope_flags = _scope_flags(repo, remote, local_only)
    print(f"single_flight: {ref} is HELD {scope} by {holder[:8]}{whose}\n"
          f"  show:    {show_cmd}\n"
          f"  release: single_flight.py release {contract_id} --token <the claim's token>"
          f"{scope_flags}\n"
          f"  ESCAPE:  {release_cmd}\n"
          f"           (unguarded — removes whatever is there, including a lock a DIFFERENT run\n"
          f"            took after this one looked stale. Use only once you have established the\n"
          f"            holder is dead and its token is unrecoverable.)")
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
    parser.add_argument("--run-id", default=None,
                        help="claim only: the [#565] CORRELATION id to record in the lock and "
                             "export, so this lock and the run's telemetry events join up "
                             "(default: $DEV_KNOWLEDGE_TELEMETRY_RUN_ID, else a fresh one)")
    parser.add_argument("--token", default=None,
                        help="release only: the per-claim OWNERSHIP token printed by claim. "
                             "REQUIRED, with no environment fallback, because an env var is "
                             "inherited by every sibling and a shared capability proves nothing. "
                             "claim always mints its own and cannot be handed one")
    args = parser.parse_args(argv)
    kwargs = {"repo": args.repo, "remote": args.remote, "local_only": args.local_only}
    if args.verb == "claim":
        kwargs["run_id"] = args.run_id
    elif args.verb == "release":
        kwargs["token"] = args.token
    try:
        return _VERBS[args.verb](args.contract_id, **kwargs)
    except SingleFlightError as exc:
        print(f"single_flight: internal error — {exc}", file=sys.stderr)
        return INTERNAL_ERROR
    except OSError as exc:  # git missing, unreadable cwd — still a refusal, never a silent allow
        print(f"single_flight: internal error — {exc}", file=sys.stderr)
        return INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
