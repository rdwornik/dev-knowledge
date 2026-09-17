# Lane ab-808 — hooks time out unseen, and the rate that proves it was first mis-counted here

**Lane:** `lane-ab-808-guard-timeout` · **Branch:** `worktree-lane-ab-808-guard-timeout` ·
**Batch:** AB (`docs/audits/2026-09-16-technical-batch-ab-manifest.md`) · **Date:** 2026-09-16

Consumers: [#808] [#811]

## The finding — RETRACTED AND RESTATED (2026-09-17)

**This lane reported, and the operator's ruling quoted, that the prompts guard "timed out and PERMITTED
477 of 573 calls (83%)" and that `deny_and_point` "timed out on all 182 of its calls, judging none".
Both numbers are wrong, and the conclusion drawn from them — "the guards were enforcing nothing" — does
not hold.** They counted transcript *attachments* as calls. A hook that passes silently writes no
attachment, so the denominator held almost only the failures. The error surfaced while building the
rate the ruling ordered (§8), and was confirmed per call by joining every guard attachment to its
`tool_use` id:

```
per call, all time    prompts guard    1,016 timed out / 8,046 matched calls in sessions it recorded in   13%
                                       (e.g. session 9b8de937: 565 matched calls, 3 attachments, all timeouts)
                      deny_and_point     161 timed out / 3,626 matched calls                                4%
the 573 and 182       attachments of ONE command variant; silent passes absent by construction
```

**What is measured instead — week to 2026-09-17, every dev-knowledge transcript, runs estimated as the
firings of each hook's event between its first and last record (§8.3):**

```
hook                                 bypassed / runs   rate   bar (10%)
surface_triage.ps1  SessionStart        252 / 262      96%    OVER
surface-closures.ps1 (user-level)       145 / 252      58%    OVER
fleet_health.py     SessionStart        107 / 263      41%    OVER
codespace_regime.py SessionStart         15 / 45       33%    OVER
resource_lifecycle  SessionStart         16 / 63       25%    OVER
billing_leak_sentinel.ps1                45 / 205      22%    OVER
conductor.py        SessionStart         34 / 199      17%    OVER
propose_closures.py (plugin) Stop       112 / 737      15%    OVER
changelog_sentinel  SessionStart         27 / 263      10.3%  OVER
session_end_backpressure Stop            58 / 725       8%    within
prompts guard       PreToolUse        1,066 / 17,047    6%    within  (13% in the sessions that recorded it)
logs_retention      SessionStart          9 / 144       6%    within
deny_and_point      PreToolUse          182 / 9,382     2%    within
```

**What stands.** The harness `timeout` fails a hook OPEN, silently, and nothing counted it: AX15-1's
fail-CLOSED guard was skipped on roughly one matched call in eight to one in sixteen, for days, with no
counter. Nine hooks are over the operator's bar, and one of them is `fleet_health.py`, the hook every
boot's digest rides on. **What does not stand:** that the guards enforced nothing. They judged most
calls. The wedges that cost the seats (§1.3) are a different failure again: they wrote no record at all,
so **no bypass rate can see them** (§8.5).

A posture ruled without a counter is not a mechanism — and a counter whose denominator is not verified
is not one either. That second half is this lane's own lesson.

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

**RULED 2026-09-17 (operator, item 1): merge the module, its tests, surface and check — NOT the
settings wiring.** Done in the ruling commit: `.claude/settings.json` and `tests/test_logs_retention.py`
are byte-identical to main, every `POSTURES` entry is `wrapped=False`, and the surface prints from
inside `fleet_health.py`'s existing SessionStart hook, in-process, so no interpreter is added (§3).
The two questions as they were asked, kept for the record:

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

> **RETRACTED 2026-09-17 — read "runs" in the table above as "attachments".** A hook that passes
> silently writes none, so these are not rates. The two facts that followed here were wrong as
> stated: ~~`deny_and_point` never judged a single call~~ (it timed out on 4% of its matched calls);
> ~~the prompts guard failed OPEN on 83% of its calls~~ (13% per call in the sessions that recorded
> it, 6% across the window). The per-call join and the corrected table are in "The finding" above;
> the estimator is §8.3. What survives: both guards failed OPEN at their bound, silently, with no
> counter, and the harness makes that choice below the hook command's own refusal logic (§2).

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
hook                         event         posture     wrapped  harness timeout   reason (short)
prompts-guard                PreToolUse    ESCALATED   no       10 s              AX15-1 fail-CLOSED; harness fails it open, 6-13% per call  [REMOVED on main 2026-09-17]
immutable-edits-guard        PreToolUse    ESCALATED   no       600 s (implicit)  ADR-77 fail-CLOSED in-zone  [REMOVED on main 2026-09-17]
deny-and-point               PreToolUse    fail-open   no       10 s              [#727] nudge  [REMOVED on main 2026-09-15]
session-end-backpressure     Stop          fail-open   no       15 s              advisory in full (ADR-85 A5)
fleet-health-session-start   SessionStart  fail-open   no       60 s              SessionStart cannot refuse
surface-triage               SessionStart  fail-open   no       10 s              surfacing only
billing-leak-sentinel        SessionStart  fail-open   no       10 s              sentinel; cannot refuse  [REMOVED on main 2026-09-17]
changelog-sentinel           SessionStart  fail-open   no       20 s              local nudge
arm-hooks                    SessionStart  fail-open   no       60 s              idempotent; check_hooks_armed backstop
conductor-session-start      SessionStart  fail-open   no       25 s              surfacing
logs-retention               SessionStart  fail-open   no       20 s              next session repeats it
resource-lifecycle           SessionStart  fail-open   no       30 s              surfacing; admission is separate
codespace-regime             SessionStart  fail-open   no       15 s              surfacing
```

**No hook is wrapped** (ruling item 1). The fail-open postures are what each hook takes IF it is ever
routed through `bounded_hook.py run`, whose `--bound` would be the old harness timeout with the harness
timeout raised by 20 s (`HARNESS_HEADROOM_S`: step 1 measured interpreter start at up to ~20 s, and
without that headroom the harness could cancel the wrapper before it writes the record). `check`
enforces that pairing if wiring ever lands. The branch's earlier wrapped wiring is in `b9a2c1a6`.

### 2.1 · ESCALATED, class (b): the two PreToolUse guards

These are the only hooks on the tool-call path, which is where both wedges happened. They are the two
this lane may **not** decide.

**E-1 — the prompts guard (`fleet_health.py --prompts-guard`).**
- **Rule:** `[#808]` asks for every hook to fail OPEN past its bound, loudly.
- **Ruling:** AX15-1 (2026-09-11) makes this guard fail CLOSED on any inability to evaluate. A guard
  that has not finished inside its bound has not evaluated.
- **Measured fact that sharpens the conflict:** the harness already fails this guard OPEN, silently,
  on ~~477 of 573 recorded calls~~ **6–13% of its matched calls** (corrected 2026-09-17, see "The
  finding"). AX15-1's posture holds only on the calls that finish inside 10 s.
- **The fork:** (i) wrap it `--posture open`, which records and announces each bypass, the status
  quo made visible; or (ii) wrap it `--posture closed`, which refuses on timeout — at the corrected
  rate, one matched tool call in eight to sixteen refused on a loaded box, with a teaching message.
  Both are one flag; nothing is wired.
- **Ruled past 2026-09-17 (item 2):** neither — the bypass rate is the signal, and a hook over the bar
  is declared broken (§8). The guard is removed from the settings file by the emergency order.

**E-2 — the ADR-77 transcript guard (`block_immutable_edits.py`).**
- **Rule:** as E-1.
- **Ruling:** ADR-77, fail-closed in-zone.
- **Measured fact:** no timeout field, so the default applied: 600 s of holding every
  `Edit|Write|MultiEdit|NotebookEdit` call, then failing open.
- **What was written:** an explicit `"timeout": 600`, the same value, in `b9a2c1a6`. Superseded: the
  emergency order removed the guard from the settings file, and ruling item 1 returned the file to
  main's bytes.
- **The fork:** whether it may fail open sooner, and whether to wrap it at all.

### 2.2 · Unblocked, not done: the deny-and-point guard (`[#727]`)

`//deny-and-point-DISABLED` in `.claude/settings.json` sets its re-enable condition: "a BOUNDED
EXECUTION TIME and FAILS OPEN on that timeout with a LOUD RECORD". `bounded_hook.py run
--posture open` is now that mechanism. Re-enabling is still an operator ruling this lane does not
take. ~~Step 1 adds a fact against doing it as-is: 182 of its 182 recorded runs timed out~~ —
**retracted**: 182 timeouts over 9,382 matched calls in the week, 2%, within the bar (§8.4). What
argues against re-enabling it as-is is not its rate but the wedges: they left no record, so a rate
under the bar does not clear it (§8.5), and the wiring is held (ruling item 1).

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
   *(Ruling 2026-09-17: the registration is removed; the same surface now prints from inside
   `fleet_health.py`'s SessionStart hook — §3.1.)*
4. **Met for the fail-open hooks.** The two fail-CLOSED guards are named and escalated, not decided
   (§2.1).
5. **Met.** English and hyphen-only ids. `logging` for diagnostics; the relayed streams and reports
   are the hook protocol's own stdout. Targeted pytest green (§5).

### 3.1 · After the operator's ruling (2026-09-17)

```
9dc8f413  docs   [#811] filed -- the contract pin mismatch (ruling item 3, §0)
888e859c  merge  sync with main (lane lag on journal_spine_anchor)
(next)    feat   rulings 1 + 2 -- wiring held, bypass rate and DECLARED BROKEN, the retraction
```

- **Ruling 1 — wiring held.** `.claude/settings.json` and `tests/test_logs_retention.py` are main's
  bytes. `POSTURES` are all `wrapped=False`, the `hook-bypass-surface` entry is gone, and a
  `deny-and-point` entry is added so its transcript rate reads under a stable id.
  `fleet_health.hook_bypass_lines()` calls `bounded_hook.surface_lines()` in-process, beneath the
  guard preflight, fail-soft. The witness that a separate `surface` hook was registered is replaced by
  one that `fleet_health.main()` calls the line, plus a fail-soft witness.
- **Ruling 2 — the bypass rate.** `run` writes a row for every outcome (`ok` included, so the rate has
  a denominator), and refuses to start a DECLARED BROKEN hook. It records `declared-broken` instead,
  and that row is not a run. New in `bounded_hook.py`: `scan_transcripts`, `compute_rates`,
  `declare`, `surface_lines`, and the `reinstate` verb. All are specified in §8.
- **`.gitignore`:** widened to `logs/HOOK-BYPASSES*` (record, scan cache, declarations).
- **Ruling 5:** the 14 child-session transcript directories from the step 1 probes are deleted.
- **Ruling 4:** `~/.claude/hooks/block-onedrive.ps1` is untouched. It belongs to the user-level
  disable ordered in the merge session.

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

**Ruling commit (2026-09-17).**
- **RED first.** The rulings' witnesses failed before the build: 10 failed and 10 passed. Two failed
  for the ruling's reasons rather than for missing names: the within-bound run wrote no `ok` row, and
  the live-settings check refused hooks still stated as wrapped against unwired settings. Two later
  REDs came from the live run: the silent-pass denominator (10 attachments, below the 20-run floor)
  and the script-basename id.
- **Targeted set.** Ran `tests/test_fleet_health.py`, `tests/test_bounded_hook.py`,
  `tests/test_logs_retention.py` and `tests/test_prompts_guard_hook_wiring.py` at `-n 4`: 249 passed,
  20 failed. `test_bounded_hook.py` alone: 20/20 at `-n 0`.
- **The 20 failures are main's.** Every one is in `test_prompts_guard_hook_wiring.py` ("expected
  exactly one prompts-guard hook, found 0"), because the emergency order removed that hook. A detached
  checkout of main, run alone, gives the same 20 failed. Neither that test file nor the settings this
  lane now carries differs from main at the base it merged.

## 6 · What the integrator owes

1. **Regenerate** `ecosystem/doc-counts.md` (`pytest_collected` moved) and `ecosystem/organ-index.md`
   if it is stale. The SessionStart registration that added an organ-index row is gone under ruling
   1, but the index was generated against the wired tree, so read the gate rather than assume either
   way. Both hooks were skipped by name in this lane's commits.
2. **`graph-task-coverage` for `.gitignore`** (operator: the integrator's item). No row claim can
   satisfy it for a root dotfile: `_REL_PATH_RE` needs a directory segment, and
   `IMPLEMENTS_ROOT_SUFFIXES` needs a suffix.
3. ~~Contract pin mismatch (§0)~~ **Done by this lane under ruling item 3:** diffed, and filed as
   `[#811]`.

## 7 · Open items

- **E-1, E-2 (class b, §2.1):** the posture past its bound for the prompts guard and the ADR-77 guard.
  Both are removed from the settings file by the emergency order, so neither is live. They return
  with any re-enable, and ruling item 2 now gives them a bar (§8).
- **User-level `~/.claude/hooks/block-onedrive.ps1`:** untouched (ruling item 4). It belongs to the
  user-level disable ordered in the merge session.
- **Which descendant held the pipe in the two real wedges is not identified (§1.4).** Nor is the
  cause of the suspended-at-creation interpreters (§0.1). No rate sees either (§8.5).
- **In-band notice on `pipe-held-after-exit`:** the command reached a verdict, so its own stdout is
  relayed and no `systemMessage` is added, since a JSON-emitting guard's output would be corrupted.
  That case is recorded and surfaced at the next SessionStart, not announced mid-session.
- **An abandoned descendant keeps running** after a `pipe-held-after-exit`. It is recorded but not
  killed, because its parent is gone and `taskkill /T` cannot reach an orphan. A Windows Job Object
  would; not built.
- ~~Leftovers outside the tree~~ **Deleted under ruling item 5:** the 14 child-session transcript
  directories.

## 8 · The bypass rate is the signal (operator ruling 2026-09-17, item 2)

### 8.1 · The stated bar

```
BROKEN_RATE      0.10   strictly greater declares
RATE_WINDOW_H    168    seven days, a working week
BROKEN_MIN_RUNS  20     below it the rate is printed and called a thin sample, never declared
```

All three are constants in `scripts/hooks/bounded_hook.py`, each with its reason beside it. One
constant changes the bar.

### 8.2 · The mechanism

- **Sources.** Rows written by `bounded_hook.py run`, one per outcome, `ok` included. Transcript hook
  attachments cover every hook the wrapper did not run. A wrapped command's attachments are skipped,
  so no run is counted twice.
- **Bypass.** Only `timeout` counts as a bypass. `pipe-held-after-exit` is a run whose verdict stood.
  `declared-broken` is not a run at all, so the declaration cannot feed itself.
- **Declaration.** A hook over the bar is written to `logs/HOOK-BYPASSES-BROKEN.json` under the
  primary checkout. The entry carries its runs, bypasses, rate, bar, window, sources, and a draft
  backlog row with the numbers.
- **Sticky.** A disabled hook produces no runs. A declaration that lapsed with its rate would re-arm a
  broken guard by itself, so it stays until `bounded_hook.py reinstate --id <id>` clears it. The count
  then restarts from the reinstatement, and the window that condemned the hook cannot re-declare it.
- **Disabled automatically.** `run` does not start a declared hook. It records `declared-broken` and
  tells the seat in-band, and it fails open whatever the posture: refusing in the name of a check that
  does not happen would wedge the seat.
- **Surfaced at SessionStart** by `fleet_health.py`, in-process. Each boot prints the recent skips,
  then one `[hook-rate]` line per hook with a bypass in the window, then one `[hook-BROKEN]` line per
  declaration. Each `[hook-BROKEN]` line says whether the disable actually reaches that hook.

### 8.3 · The estimator — attachments are not runs

This is the error behind the retracted 83%, and the estimator exists to avoid it.

- **Silent passes leave nothing.** A hook that passes silently writes no transcript attachment, on
  every event. Measured: 8,046 prompts-guard-matched calls carried 1,112 attachments. `arm_hooks.py`
  attached in 109 of 263 SessionStart firings, and every one of those had output.
- **Runs are the event's firings.** Between the first and last hour a hook left any record, each
  firing of its event counts as one run: a distinct `toolUseID` for SessionStart and Stop, a
  `tool_use` of a tool the hook was seen matching for PreToolUse. The attachment count is the floor.
- **Why across every session.** A firing in a checkout that did not register the hook still counts as
  a run, so the error can only lower a rate, never declare. The same guard counted only in the
  sessions that recorded it reads 13%, against 6% across the window. For an automatic disable, the
  estimator errs toward not declaring (X-3 below).
- **Incremental.** Per-file byte offsets live in `logs/HOOK-BYPASSES-SCAN-CACHE.json`. Only whole
  lines are consumed, and a file modified before the window is skipped unread.
- **Time-boxed.** The scan gets 2 s per boot. A partial scan says so and declares nothing.
- **Named ids.** A hook with no `POSTURES` entry is named `cmd:<script basename>`.

### 8.4 · Live result, and its cost

Against the real store (1.4 GB, 1,036 files), with the record pointed at a scratch directory so
nothing landed in `logs/`, the result is the table in "The finding": nine hooks declared, including
the user-level `surface-closures.ps1` and the plugin's `propose_closures.py`.

Measured at a 4 s budget, before it was lowered:
- Cold boots 1 and 2: 5.8 s and 5.2 s, the first partial.
- Every boot after: about 2 s through `uv run`, and 0.33 s in-process, which is what `fleet_health`
  pays.

The budget is now 2 s, so the cold catch-up spreads over more boots.

### 8.5 · What no bypass rate can see

- **The wedges.** Both multi-hour wedges (§1.3) and the operator's suspended interpreters (§0.1) wrote
  **no attachment**. A hook that never returns and is never cancelled is neither a run nor a bypass
  in this count. A rate under the bar does not clear a hook of wedging; `deny_and_point` is the
  example (2%, and it wedged seats).
- **The host's own failures.** `fleet_health.py`, the hook this surface rides in, timed out on 41% of
  boots in the window. On those boots the surface is not seen, and nothing else prints it.
- **No host at all, right now.** Main `bc8ddda5` (2026-09-17, after this lane's rulings) sets
  `disableAllHooks: true` in the repo and user-level settings, re-enabling only under `[#863]`. Until
  then no SessionStart hook runs, so the surface prints nowhere. The declarations still land if
  `bounded_hook.py surface` is run by hand, and it is read-only apart from its own `logs/` state. Once
  hooks return, a rate over their pre-disable week is what the first boot will show.

### 8.6 · Escalated

- **X-1 — class (b), ruling vs ruling: "disabled automatically" (item 2) vs "NOT the settings.json
  wiring" (item 1).**
  - **Why they conflict.** The only per-hook disable Claude Code offers from this repo is the tracked
    settings file: `settings.local.json` cannot cancel a project hook, and `disableAllHooks` is
    all-or-nothing (measured 2026-09-15). The one automatic switch that exists is `run`, and with
    the wiring held it reaches no hook. Today every declaration truthfully prints "Disabled: NO".
  - **The fork.**
    - (i) Keep the wiring held and have a human act on each declaration by editing
      `.claude/settings.json`, with the declaration's numbers in the commit body.
    - (ii) Wire the declared-healthy hooks through `run`, so the switch reaches them. That is the
      interpreter cost ruling item 1 refused.
    - (iii) A hook script reads the declaration itself and exits at once. That still pays the
      interpreter start the timeouts come from, so it stops the judging but not the cost.
  - **This lane built nothing past the switch in `run`.**
- **X-2 — class (c): "filed as a row" from a SessionStart hook.** Filing needs an id reservation, a
  branch and a commit. A hook in the primary checkout, which sits on main, may do none of these, and
  an untracked `tasks/` file wedges every commit. So the row is **drafted** into the declaration, and
  the surface says "Row NOT filed". Who files drafted rows, and from which id block, is unruled.
- **X-3 — class (c): which estimator the declaration uses.** The whole-window estimator errs toward
  not declaring, and it puts the prompts guard at 6%, within the bar. The per-session estimator puts
  it at 13%, over the bar. The ruling names a fraction and a window, not a denominator. This lane
  chose the one that cannot falsely disable a guard; one function flips it.
- **X-4 — class (c): the bar declares the surface's own host.** `fleet_health.py` is over the bar at
  41%. If any disable ever reached it, the declarations would disappear with it. A carve-out or a
  different host is unruled.
- **X-5 — same class as ruling item 4: user-level and plugin hooks.** `surface-closures.ps1` (58%)
  and `propose_closures.py` (15%) are declared, and nothing in this repo can stop them. Each
  declaration says so. They belong with the user-level disable in the merge session.
