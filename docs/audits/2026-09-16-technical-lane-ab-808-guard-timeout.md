# Lane ab-808 — the guards that wedged the seats were enforcing nothing

**Lane:** `lane-ab-808-guard-timeout` · **Branch:** `worktree-lane-ab-808-guard-timeout` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`) · **Date:** 2026-09-16

Consumers: [#808] [#811]

## The finding

```
PreToolUse prompts guard (fleet_health.py --prompts-guard)   573 recorded runs   477 timed out and PERMITTED the call (83%)
PreToolUse deny_and_point.py                                 182 recorded runs   182 timed out, judged NONE (100%)
```

**The guards behind ~20 hours of wedged seats were enforcing nothing.** The harness `timeout` fails
a hook OPEN, silently, and writes only a transcript attachment nobody read. AX15-1 ruled the prompts
guard fail-CLOSED; the guard did the opposite on most of its calls for days, and nothing counted
whether the ruling held. Source: `hook_cancelled` / `timedOut: true` attachments across every
`~/.claude/projects/*dev-knowledge*/*.jsonl` transcript (§1.3). A posture ruled without a counter is
not a mechanism, so the operator's ruling of 2026-09-17 makes the BYPASS RATE the signal (§8).

## 0 · Contract identity — the pin mismatch, diffed

```
pinned   25ece422...  manifest d0fe3865 (16:03); bytes recovered from .claude/jobs/62117afb/tmp/contracts/
ran      2e7d91a6...  prompts dir, mtime 19:41; this lane booted on it before 20:00
re-pin   2e7d91a6...  amendment 1, 6ab764fc (20:41) -- AFTER boot, and silent on what changed
diff     +13 lines, 0 removed: the "Model — why opus, and not sonnet" section (operator ruling
         2026-09-16, "every model justified"). Done-contract, Steps, What-NOT-to-do: byte-identical.
```

The lane executed the pinned substance, which was luck, not a property of the freeze. Nothing compares
the contract a lane boots on with the committed pin, and the pinned bytes survived only in another
seat's job scratch dir. Filed as `[#811]`, id reserved by push from this lane's block.

## 0.1 · PAUSE (Q10) — main refuted part of this lane's premise mid-lane

**The fact.** `33246c0a` / `426b9cac` (operator emergency order, 2026-09-17 10:14) landed on main
after this lane's build commit. It removes every PreToolUse hook and `billing_leak_sentinel.ps1`, and
records a measurement this lane did not have:

- 20 orphaned hook interpreters, aged up to 47 h.
- Each one's parent shell was DEAD, with 0 s CPU, no image path, and its single thread in
  Wait/Suspended: **created suspended and never resumed; the script never ran a line**.
- Re-enable bar: a bounded, fail-open, loudly recorded execution time **and** "only once the
  suspended-at-creation cause is identified".

**What it confirms here.** §1.2 g2 is the harness side of that wedge. A dead parent plus a live
descendant holding the pipe is the case the harness `timeout` does not bound, and it leaves no
record.

**What it refutes here.** §1.6 argues that `bounded_hook.py` closes that gap. It does so only when
the process that hangs is a **descendant of the wrapper**, because such a process holds the
wrapper's pipe and the wrapper stops waiting at its bound. The orphans the operator measured are the
**first** interpreter the hook shell starts. For a wrapped hook, that interpreter is the wrapper
itself: `bash → python bounded_hook.py`. A wrapper created suspended never runs a line of its own
timer, so it bounds nothing. Wrapping also adds one interpreter start per hook, and so one more
exposure to the same unexplained cause.

**What was done, and what was NOT decided.**
- The sync merge `9bb77676` takes the operator's order wherever it reaches: PreToolUse `[]`, no
  billing sentinel.
- The Stop hook and the eight remaining SessionStart hooks are still wrapped **as this branch had
  them before the fact arrived**. They were not re-decided in either direction.
- E-1 / E-2 (§2.1) are moot while those hooks are disabled, but they return with any re-enable.

**Asked of the integrator/operator before merging this branch:**
1. **Merge the wiring (`.claude/settings.json`) or only the module?** Given the suspended-at-creation
   evidence, this lane recommends landing `scripts/hooks/bounded_hook.py`, its tests and the record /
   surface / check **without** the settings wiring until the cause is identified. That is the
   operator's own re-enable condition, applied to every hook, not only the disabled ones.
2. **The instrument the cause needs is not this wrapper.** A hook command that is never scheduled
   runs none of its own code. It has to be observed from outside: the process's creation flags,
   parent chain and thread state at the moment of the hang, or the harness's spawn path. That is new
   work; the lane's id block (`[#811]`–`[#814]`) is untouched, and filing it is left to the operator.

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

## 2 · Posture per hook, and the class (b) escalation

The code carries the posture and its reason: `scripts/hooks/bounded_hook.py::POSTURES`, one entry per
registered hook. `bounded_hook.py check` refuses any hook without an entry. Summary:

```
hook                         event         posture     wrapped  bound / harness timeout   reason (short)
prompts-guard                PreToolUse    ESCALATED   no       — / 10 s                   AX15-1 fail-CLOSED; harness already fails it open, 83%  [REMOVED on main 2026-09-17]
immutable-edits-guard        PreToolUse    ESCALATED   no       — / 600 s (was implicit)   ADR-77 fail-CLOSED in-zone  [REMOVED on main 2026-09-17]
session-end-backpressure     Stop          fail-open   yes      15 s / 35 s                advisory in full (ADR-85 A5)
fleet-health-session-start   SessionStart  fail-open   yes      60 s / 80 s                SessionStart cannot refuse
surface-triage               SessionStart  fail-open   yes      10 s / 30 s                surfacing only
billing-leak-sentinel        SessionStart  fail-open   yes      10 s / 30 s                sentinel; cannot refuse  [REMOVED on main 2026-09-17]
changelog-sentinel           SessionStart  fail-open   yes      20 s / 40 s                local nudge
arm-hooks                    SessionStart  fail-open   yes      60 s / 80 s                idempotent; check_hooks_armed backstop
conductor-session-start      SessionStart  fail-open   yes      25 s / 45 s                surfacing
logs-retention               SessionStart  fail-open   yes      20 s / 40 s                next session repeats it
resource-lifecycle           SessionStart  fail-open   yes      30 s / 50 s                surfacing; admission is separate
codespace-regime             SessionStart  fail-open   yes      15 s / 35 s                surfacing
hook-bypass-surface (new)    SessionStart  fail-open   no       — / 10 s                   reads one file, spawns nothing
```

Every wrapped hook's `--bound` is its old harness timeout, so the hook's own time budget is
unchanged. The harness timeout rises by 20 s (`HARNESS_HEADROOM_S`). Step 1 measured interpreter
start at up to ~20 s on this box, and without that headroom the harness could cancel the wrapper
before it writes the record.

### 2.1 · ESCALATED, class (b): the two PreToolUse guards

These are the only hooks on the tool-call path, which is where both wedges happened. They are the two
this lane may **not** decide.

**E-1 — the prompts guard (`fleet_health.py --prompts-guard`).**
- **Rule:** `[#808]` asks for every hook to fail OPEN past its bound, loudly.
- **Ruling:** AX15-1 (2026-09-11) makes this guard fail CLOSED on any inability to evaluate. A guard
  that has not finished inside its bound has not evaluated.
- **Measured fact that sharpens the conflict:** the harness already fails this guard OPEN, silently,
  on **477 of 573** recorded calls. AX15-1's posture holds today only on the calls that finish
  inside 10 s.
- **The fork:** (i) wrap it `--posture open`, which records and announces each bypass, the status
  quo made visible; or (ii) wrap it `--posture closed`, which refuses on timeout. At the measured
  83% rate that refuses most tool calls on a loaded box: the 2026-09-06 wedge class, with a teaching
  message instead of silence. Both are one flag; nothing is wired.
- **Left as is:** the command is byte-identical (`tests/test_prompts_guard_hook_wiring.py` still
  pins it).

**E-2 — the ADR-77 transcript guard (`block_immutable_edits.py`).**
- **Rule:** as E-1.
- **Ruling:** ADR-77, fail-closed in-zone.
- **Measured fact:** no timeout field, so the default applied: 600 s of holding every
  `Edit|Write|MultiEdit|NotebookEdit` call, then failing open.
- **What was written:** an explicit `"timeout": 600`, the same value. That satisfies Done 2 without
  deciding anything.
- **The fork:** whether it may fail open sooner, and whether to wrap it at all.

### 2.2 · Unblocked, not done: the deny-and-point guard (`[#727]`)

`//deny-and-point-DISABLED` in `.claude/settings.json` sets its re-enable condition: "a BOUNDED
EXECUTION TIME and FAILS OPEN on that timeout with a LOUD RECORD". `bounded_hook.py run
--posture open` is now that mechanism. Re-enabling is still an operator ruling this lane does not
take, and step 1 adds a fact against doing it as-is: **182 of its 182 recorded runs timed out**, so
it has never judged a call on this box. Wrapped, it would record a bypass on nearly every matched
call.

## 3 · What changed

```
8f562b29  docs   step 1 -- the measurement (§1)
2cf3b380  test   step 2 -- 13 RED-first witnesses, tests/test_bounded_hook.py (13/13 FAIL on that commit's code)
84b359c8  merge  sync with main for the journal anchor (lane lag: split diagnostic mine [f8ca1d40], main [])
b9a2c1a6  feat   step 3 -- scripts/hooks/bounded_hook.py; .claude/settings.json wiring; .gitignore; test_logs_retention
917a076a  docs   step 4 -- posture table and class (b) escalation (§2)
9bb77676  merge  sync onto main's emergency hook disable (§0.1)
(this)    fix+docs step 5 -- taskkill fired not awaited; this section; the PAUSE (§0.1)
```

- **`scripts/hooks/bounded_hook.py`** (stdlib, system interpreter):
  - `run`: bound, fail-open, record, in-band `systemMessage`.
  - `surface`: SessionStart print of the last 72 h of bypasses.
  - `check`: refuses a hook with no `timeout`, a `--bound` without 20 s headroom, or a hook with no
    posture.
  - `POSTURES`: posture and reason per hook.
- **`.claude/settings.json`:**
  - Stop and nine SessionStart hooks wrapped; harness timeouts raised by 20 s.
  - New `surface` SessionStart hook.
  - ADR-77 guard given an explicit 600 s.
  - A `//bounded-hooks` note with the measurement.
- **`.gitignore`:** `logs/HOOK-BYPASSES.jsonl`.
- **`tests/test_logs_retention.py`:** the ADR-106 prefix assertion reads the command *inside* the
  wrapper. The same `uv run --locked` prefix is required, no weaker.

**Done-contract, item by item:**
1. **Met.** A stand-in that would exit 2 sleeps past a 2 s bound. It exits 0, the call proceeds, and
   one record lands in `logs/HOOK-BYPASSES.jsonl` with hook id, bound, elapsed time and session id.
   RED on `2cf3b380`, GREEN from `b9a2c1a6`. The real harness agrees (§4).
2. **Met.** Every hook in `.claude/settings.json` has an explicit `timeout`. `bounded_hook.py check`
   refuses one without it (witness `test_the_check_refuses_a_hook_registration_without_an_explicit_bound`).
   It is a CLI plus a test, **not** a pre-commit hook: wiring one would mean editing
   `.pre-commit-config.yaml` and the CLAUDE.md §9 roster, outside this lane's footprint.
3. **Met.** `bounded_hook.py surface` is registered at SessionStart and is silent with no record.
4. **Met for the fail-open hooks.** The two fail-CLOSED guards are named and escalated, not decided
   (§2.1).
5. **Met.** English and hyphen-only ids. `logging` for diagnostics; the relayed streams and reports
   are the hook protocol's own stdout. Targeted pytest green (§5).

## 4 · Measured before / after

**Real harness, child sessions (Claude Code 2.1.273):**

```
shape                                  before (unwrapped, §1.2)                     after (wrapped)
sleeper past bound (bound 5 s)         hook_cancelled, NO record on our surface     record reason=timeout elapsed 6.6 s; hook_system_message shown; tool proceeded
descendant holds the pipe (bound 20/25) waited 90 s past a 20 s bound, NO record    record reason=pipe-held-after-exit elapsed 25.0 s; harness saw hook end at 29.5 s; tool proceeded
```

**Hook latency.** Five interleaved pairs through Git Bash with a SessionStart payload, `--bound 60`,
this box under batch load:

```
changelog-sentinel      direct median 8.09 s [8.83 9.92 8.09 5.67 5.55]   wrapped median 8.06 s [13.83 8.88 8.06 7.86 6.73]
billing-leak-sentinel   direct median 5.62 s [5.62 6.78 5.66 3.86 4.09]   wrapped median 4.92 s [12.28 17.95 4.92 4.14 4.84]
surface (new hook)      median 2.39 s [1.98 2.45 2.20 2.39 3.52]
bare `python -c pass` through bash, for scale: median 2.73 s
```

**No measurable median cost under this load.** The noise between pairs is larger than one extra
interpreter start, which is what the wrapper theoretically adds (~2.5 s here). The wrapped legs
did show the two worst outliers (12.3 s, 18.0 s). Read that as a possible tail cost, n=5, not a
settled number. The new `surface` hook adds one interpreter start per boot. SessionStart hooks run
concurrently, so the boot wall clock is set by the slowest hook, not the sum.

## 5 · Tests

- **Targeted set:** `tests/test_bounded_hook.py`, `tests/test_logs_retention.py`,
  `tests/test_prompts_guard_hook_wiring.py`.
  - 66 passed at `-n 0` and in 4 of 5 runs at `-n 4`.
  - The fifth run had 2 failures. One was `test_hook_command_refuses_a_bare_exit_2_with_a_message_that_teaches`
    hitting `subprocess.TimeoutExpired` on Git Bash. That test and the command it pins are unchanged
    by this lane: a load flake. The second was cut off in the captured tail and **is not identified**.
    Two further runs were fully green.
- **Defect found by that load, fixed before this commit:** the held-pipe witness took 18.3 s against
  its 8 s ceiling at `-n 4`, because the wrapper waited on its own `taskkill /T`. The kill is now
  fired and not awaited (`_kill_tree`), and the grace is 1 s. The witness was not relaxed.
- **Wider settings-reading set (30 files, 1,538 tests):**
  - 13 failed at the build tip.
  - A paired baseline run of the failing ids on HEAD's files had 9 of them failing already:
    fleet parity, deny-and-point wiring (RED by design), the `sed`-less handoff probes, the v6 R6
    contract, the anchor-gate probe, backlog-view readers and health.
  - **Two were this lane's.** `test_logs_retention` is fixed. `test_generate_organ_index::test_live_committed_index_is_the_generated_bytes`
    stays RED until the integrator regenerates `ecosystem/organ-index.md` (one new SessionStart row).
- The full suite was **not** run (operator constraint, batch AB).

## 6 · What the integrator owes

1. **Regenerate** `ecosystem/doc-counts.md` (`pytest_collected` moved) and `ecosystem/organ-index.md`
   (the new `bounded_hook.py` SessionStart row). Both hooks were skipped by name in `2cf3b380` /
   `b9a2c1a6` and in this commit.
2. **`graph-task-coverage` was skipped in `b9a2c1a6` for `.gitignore`.** No claim can satisfy it for
   a root dotfile: `_REL_PATH_RE` needs a directory segment, and `IMPLEMENTS_ROOT_SUFFIXES` needs a
   suffix. That is a gate gap, a candidate for a row from the integrator's block.
3. **Contract pin mismatch (§0):** compare the pinned and dispatched bytes of the contract.

## 7 · Open items

- **E-1, E-2 (class b, §2.1):** the posture past its bound for the prompts guard and the ADR-77
  guard. The prompts guard is the one on every tool call, so the wedge exposure on the tool path
  stays until this is ruled.
- **User-level `~/.claude/hooks/block-onedrive.ps1`** matches `Bash|PowerShell|Edit|Write|NotebookEdit|Read`
  with **no `timeout`** (600 s default) and is unwrapped. It sits outside this repo's footprint, and
  global-infra edits need their own ruling (core invariant 6). It was live on the `Bash` path at
  both wedges.
- **Which descendant held the pipe in the two real wedges is not identified (§1.4).** The wrapper
  closes the mechanism for every wrapped hook. The unwrapped tool-path hooks remain exposed.
- **In-band notice on `pipe-held-after-exit`:** the command reached a verdict, so its own stdout is
  relayed and no `systemMessage` is added, since a JSON-emitting guard's output would be corrupted.
  That case is recorded and surfaced at the next SessionStart, not announced mid-session.
- **An abandoned descendant keeps running** after a `pipe-held-after-exit`. It is recorded but not
  killed, because its parent is gone and `taskkill /T` cannot reach an orphan. A Windows Job Object
  would; not built.
- **`deny_and_point` re-enable (§2.2):** the mechanism now exists, but its measured 100% timeout
  rate argues against re-enabling it as-is.
- **Leftovers outside the tree, not deleted without asking:** child-session transcripts under
  `~/.claude/projects/C--Users-1028120--claude-jobs-810dac9e-tmp-rig*` (14 directories from the
  probes). The rig directories themselves live in the job tmp dir and go with the job.
