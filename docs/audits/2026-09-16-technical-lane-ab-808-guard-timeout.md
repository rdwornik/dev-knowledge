# Lane ab-808 — what a hook `timeout` actually bounds, and the gap a bounded wrapper closes

**Lane:** `lane-ab-808-guard-timeout` · **Branch:** `worktree-lane-ab-808-guard-timeout` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`) · **Date:** 2026-09-16

Consumers: [#808]

## 0 · Contract identity — a pin mismatch, disclosed

The manifest pins `LANE-ab-808-guard-timeout.md` at `25ece422…ea031d2`. The file read at boot hashes
`2e7d91a6…610afa1` (no CR bytes, so not a line-ending artefact). Its mtime is 2026-09-16 19:41, after
the manifest commit `d0fe3865` (16:03). `LANE-ab-810` was re-emitted in the same minute; `LANE-ab-804`
was not and still matches its pin. The contract carries a "Model — why opus" section citing the
operator ruling of 2026-09-16 "every model justified", which is the likely edit. The pinned bytes are
not recoverable from this seat, so the diff is **unverified**. The lane executes the dispatched file.
The integrator should compare the two before merging.

## 1 · Step 1 — the premise, measured before anything was built

**Question (contract step 1):** `.claude/settings.json` already sets `timeout` on hooks, and seats
wedged anyway. What does that field bound on this platform (Windows, hook commands through Git Bash)?

### 1.1 · Instrument

Throwaway child sessions: a scratch directory holding only `.claude/settings.local.json`,
`claude -p --setting-sources local --model claude-haiku-4-5-20251001 --permission-mode bypassPermissions`,
prompt on stdin. The prompt asks for one Bash call that writes a timestamp. One `PreToolUse` hook on
`Bash` per variant. Evidence comes from three places: marker files the hook and its descendants write,
the tool's own timestamp file, and the child transcript's `attachment` records. No live session was
wired, and no probe ran in this worktree. Claude Code 2.1.273.

The Bash tool itself took about 50 s to start after the hook finished on this loaded box. v4 shows it
with no timeout in play: hook end 742.6, tool 792.6. Tool timestamps below are read with that offset.

### 1.2 · Results

```
variant                                   bound  hook behaviour                      harness result
v1  bash `sleep 30`                       5 s    start logged, no end marker         hook_cancelled timedOut=true durationMs=6960; tool PROCEEDED
g1  foreground python sleep 90            20 s   python pid written, never finished  hook_cancelled timedOut=true durationMs=22634; python GONE; tool PROCEEDED
g2  bash exits at +7 s, detached python   20 s   python finished its 90 s sleep      NO attachment at all; tool ran 2 m 41 s after tool_use
    still holding stdout, sleeps 90
v4  bash `sleep 20`, no timeout field     —      ran to completion (24.5 s)          no attachment; tool proceeded
g3  bash `sleep 75`, no timeout field     —      ran to completion (78.9 s)          no attachment; tool proceeded
```

**Verdict.** The harness bound is real, and it bounds the hook's top process only.

- **While the top process is alive, it works.** At the bound the harness kills the process tree
  (g1's native `python.exe` grandchild did not survive), writes `hook_cancelled` with
  `timedOut: true`, and **fails open**: the tool call runs.
- **Once the top process has exited, it does not bound anything.** g2's shell exited at +7 s, leaving
  a descendant that had inherited the stdout pipe. The harness waited for that pipe to close, 90 s
  against a 20 s bound, and **wrote no record**. With a descendant that never exits, the wait never
  ends.

### 1.3 · Real transcripts agree

`~/.claude/projects/*dev-knowledge*/*.jsonl` was scanned for hook attachments and for a `tool_use`
followed by more than 15 minutes of silence (files touched since 2026-09-09).

**Two wedges, both with no hook record:**

```
2026-09-15T12:53:12  lane-aa-12-enforced-routing  Bash  silent 1209 min, next entry a user message
2026-09-15T13:34:37  primary (integrator)         Bash  silent  341 min, next entry the operator: "wedged ~6 hours ... inside PreToolUse hooks"
```

Neither has a `hook_cancelled` attachment. That is g2's signature, not v1's or g1's. A bound that had
fired would have written one, as it did 1,400+ times elsewhere in the same corpus.

**The harness bound fires constantly, and it is a silent fail-open every time:**

```
PreToolUse prompts-guard (fleet_health.py --prompts-guard, timeout 10)   573 runs, 477 timedOut (83%), max 27.1 s
PreToolUse deny_and_point.py (timeout 10, now disabled)                  182 runs, 182 timedOut (100%), max 22.0 s
SessionStart surface_triage.ps1 (timeout 10)                            1003 runs, 607 timedOut, max 146.7 s
SessionStart fleet_health.py (timeout 60)                                833 runs, 393 timedOut
SessionStart billing_leak_sentinel.ps1 (timeout 10)                       40 runs,  39 timedOut
Stop session_end_backpressure.py (timeout 15)                           1611 runs,  96 timedOut
```

Two facts follow, and both matter more than the wedge:

1. **`deny_and_point` never judged a single call.** Every one of its 182 invocations was cancelled
   at its bound. It cost 10–22 s per matched call and refused nothing.
2. **The prompts guard, ruled fail-CLOSED by AX15-1, has failed OPEN on 83% of its calls.** The
   harness makes that choice on timeout, silently, below the hook command's own refusal logic. See §2.

### 1.4 · Where the evidence stops

- The wedges show the missing record the held-pipe mechanism predicts. **Which descendant held the
  pipe was not identified.** The prompts guard reads the registry in-process and spawns nothing on
  that path. `deny_and_point.py` spawns no subprocess. No `core.fsmonitor` daemon is configured. The
  user-level `block-onedrive.ps1` hook, which also matches `Bash`, sets **no** `timeout`, and its
  descendants were not examined.
- The block record says nothing about which hook was running at the wedge, beyond the `Bash` matcher
  set of that day.

### 1.5 · Default bound probe — a hook with no `timeout` field

```
d1  bash `sleep 700`, no timeout field    hook_cancelled timedOut=true timeoutMs=600000 durationMs=706003; tool PROCEEDED
```

The default is **600 s**. It was read from the harness's own record, not from documentation. The
wall time (706 s) includes this box's shell-start overhead. A hook registered without a `timeout`,
like the ADR-77 transcript guard in `.claude/settings.json` or the user-level `block-onedrive.ps1`,
can hold every matching tool call for ten minutes before failing open. That applies only while its
top process lives; §1.2 g2 still applies after it exits.

### 1.6 · Why this is not a PAUSE

The contract says to PAUSE if "the harness bound already works and the wedge is elsewhere". Neither
half holds. The bound works only while the top process lives. The wedge sits in the one case it does
not cover, at the hook stage, with no record. A wrapper whose children inherit **its** pipes, never
the harness's, and which stops waiting at its own bound, closes exactly that gap. It is not a rival
to the harness timer. It also gives the fail-open a durable record, which the harness never writes.

## 2 · Class (b) escalation — the guards whose ruling says fail CLOSED

_Filled at step 4._
