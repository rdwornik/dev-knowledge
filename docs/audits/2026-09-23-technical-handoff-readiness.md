# DIGEST — handoff readiness (the one file the architect reads)

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source:
> `to-browser/DIGEST-HANDOFF-READINESS-2026-09-23.md`. This is the row driving LANE-5A-5's own
> Done-contract: its §5 (landing list) and §6 (17 standing requests) are the direct source for the
> rows this lane files, and its P9/P11 findings are the ones this lane's validation step re-checks.
> Companions: `2026-09-23-technical-state-of-the-harness.md` (full was/is),
> `2026-09-23-technical-opus55-harness.md` (S1), `2026-09-23-technical-hook-architecture.md` (S2).
> Carrier rows: S3 §6's ten rows (O-2a, O-2b, O-2d, O-4a, O-4b, O-4c, R-09-19-3, R-09-19-7,
> R-09-19-10, D-backbone) filed by `lane-landing-window`; §5's landing list is discharged via
> `carried-by:` edits to the named transport files (this lane's P11 step) and via
> `STANDING_RULINGS.md` (this lane's rulings step).

carried-by: OPEN
lands-via: the architect's handoff cut and the next window's landing step; no repo change made here
date: 2026-09-23
from: postwave-state (POSTWAVE CHAIN S3, job 60a4eb17, Opus 5.5), read-only, main @ 4667f731 == origin/main
companions: STATE-OF-THE-HARNESS-2026-09-23.md (full was/is) · DIGEST-OPUS55-HARNESS-2026-09-23.md (S1) · DIGEST-HOOK-ARCHITECTURE-2026-09-23.md (S2)

# DIGEST — handoff readiness (the one file the architect reads)

**Verdict: the handoff is NOT ready to cut as-is.**
- The active bundle (`2026-09-19-dev-knowledge-architect`) passes its structural probes 15/15, but in report-only mode two rows FAIL:
  - **P9:** `validate_backlog` reports 10 hard-fails.
  - **P11:** 32 decision files are OPEN and not named in RESIDUAL.
- The paste is 34,998 B against its own 20,000 B ceiling.
- The dispatch table no longer describes how lanes launch.
- 10 of the 17 standing operator requests have no home at all.

## 1 · S1 in one page (Copilot first)

```
Part A  Copilot producer on two real rows   NOT RUN -- blocked by provider-registry `admission: unevaluated`
        rows 0 · review tally n/a · tests n/a · credits 0 · wall n/a · memory n/a
Part B  /changelog-review                    DONE: 77 claude-code + ~30 codex versions; 3 ADOPT (intake 105), 0 obsolete
        branch worktree-postwave-changelog @ 66a616a9, pushed, NOT merged (HANDBACK in S1)
Part C  Opus 5.5                             orchestrate/plan only candidate; A/B designed, not run; no routing change
```

**Correction S3 makes to S1: the Copilot admission DOES trace; the registry never recorded it.** S1 says "no
2026-09-17 admission anywhere" and reads `copilot-collections` as only a repo name. That is wrong.
- The batch-AB lanes ab-828 and ab-832 were produced by Copilot (served `gpt-5.6-luna`) and reviewed by Codex
  (`gpt-5.6-terra`).
- They were launched by `to-cc/run-lane-copilot.ps1` on 2026-09-16 at 21:18/21:20.
- Receipts: `receipts/lane-ab-8{28,32}-*/HANDBACK.json` and `copilot-usage.json` (1 premium request each).
- JOURNAL.md:1113 reads "closure-census (Copilot producer + Codex reviewer)", and :962 reads "A non-Claude lane
  (Copilot co-author)". ab-832 merged at `88dc48f4`.
- **The real defect** is that the admitted *invocation* is a transport script outside the repo, while
  `ecosystem/provider-registry.yaml` still says `unevaluated` / NOT ADMITTED. Two sources of truth disagree,
  and the router obeys the registry.
- The RATIFICATION's "3/3 correct, 0.46 credits, 14 s" is in no repo file (INHERITED from chat).
- S1's refusal to spend was correct under the registry. The fix is a landing act: registry admission plus an
  in-repo producer verb. It needs no fresh trial.

## 2 · S2 in one page

- **Boot:** 8 SessionStart interpreters start in parallel. p50 per hook in-session is 7-16 s, against 1-4 s in
  isolation. `surface_triage` timed out on 23 of about 31 boots. **The W4B-0 re-arm evidence (isolated runs)
  did not predict in-session cost.**
- **Operator rule** (a start hook reads, an event hook triggers background work, heavy work runs isolated): 6 of
  11 session hooks violate it. `lane_end_guard.py` is the model to copy (claim → detached worker → receipt → reaper).
- **P0 path protection is off:** block-onedrive and the ADR-77 guard have been off since 09-17 with no expiry.
  Only a Read deny binds.
- **The 2026-09-25 hook verdict is unsafe:** the counter store is per-checkout, lane rows die at teardown, and 4
  armed hooks show 0 runs. Zero runs must read UNMEASURED, not REMOVE. **Time-critical: 2 days.**
- **The banner lies:** 7 re-armed hooks print "DECLARED BROKEN".
- **Proposals:** 8 rows plus an ADR draft (four hook classes: READER / TRIGGER / PATH GUARD / GATE; one
  stdlib entry per event). Nothing filed.

## 3 · Self-test on main, headline (was 09-20 → is 09-23)

```
audit.py health                  OK, 0 [!!]                  -> OK, 0 [!!] (258 WARN, 62 OK)
ship-gate                        RED 357 WARN / 269 undisp / 3 stale -> RED 407 / 319 undisp / 0 stale, 0 [!!]
  consumer_at_landing            121 -> 170
  funnel_coverage                 83 -> 120
  proof_layer                     44 -> 69
gates.py JSON verdict (main)     n/a -> RED, red=[ship-gate] only; health/ruff/impacted ok; per-organ findings present
audit checks                     55 -> 56 (last organ_truth)
where the loop stops             spine stage 7 -> moment merge/gates (+ batch-close digest); whole-loop test strict xfail
connection walk -n 2             n/a -> 21 pass / 1 strict xfail / 18m59s (INHERITED WAVE4B, same SHA; S3's run reaped)
organ census 30 d (175 obs.)     n/a -> CALLED 78 / UNOBSERVED 80 / UNREACHABLE 17 (+14 not observable)
moments query                    n/a -> 23 declared at a moment, 166 nowhere (REFUSED)
orphan-census                    5 -> 14 (9 are scripts harness.yaml DOES run: the stage/moment edge is still missing)
graph nodes / edges              3,010 / 22,232 -> 3,103 / 22,669
files unknown to the graph       1,080 -> 1,094 (coverage 70.6 % -> 71.0 %); Causes D/E still open
no_leftovers (slug-less)         n/a -> CLEAN (no husk)
handoff probes (structural)      15/15 -> 15/15
handoff probes (report-only)     n/a -> P0a-P5, P7, P8a PASS · P8b 1 file PASS · P9 FAIL · P11 FAIL · P6 PASS (7,364 = 7,364)
open backlog rows                390 -> 441
STANDING_RULINGS lines           4,373 -> 4,602 (section AJ landed 7 decision files)
09-20 homeless rulings homed     0/11 -> 0/11
```

## 4 · Stale statements (location · stale · evidence · replacement)

```
1 PLAYBOOK.md:2884 Ch8 "dispatch table -- the SOLE literal-command site" (cited by HANDOFF_BOOT forms §1, lane-boot.md:124)
  stale: only dispatch / Dispatch-Local / -Cloud / -Codespace / Harvest-Codespace
  evidence: wave 4/4b lanes launched with `uv run --locked python scripts/dispatch.py launch --batch <B> <CONTRACT>.md`;
            repairs ran bare `claude --bg ... "Read REFUSED-<lane>.md"`; dispatch_drift only checks that listed verbs
            resolve (4/4 do), never completeness
  new: add the scripts/dispatch.py launch row as THE lane launcher; mark the PowerShell verbs ad-hoc/operator
2 HANDOFF_PROCESS.md:1020 "The loop closes at the root, always."
  evidence: 4B merged in an integration worktree off origin/main, root main fast-forwarded only when green (B6 MET);
            lane-merge-path deferred, so this is a hand procedure
  new: target = verified integration worktree -> ff root; today manual per INTEGRATOR-STANDING-ORDER-WAVE4B
3 HANDOFF_PROCESS.md:330 "assembled paste has a 20,000-byte ceiling"
  evidence: PASTE_THIS.md = 34,998 B; assemble_paste.py:563 only WARNs
  new: "soft ceiling, WARN-only, currently 75 % over" -- or make it a gate
4 bundle HANDOFF_BOOT forms §1-3 (dispatch / worktree / /lane-integrate)
  evidence: same as 1 and 2; the integrator seat's mechanics are carried by AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION (OPEN)
  new: render from the corrected Ch8; carry the 4B integrator procedure
5 HANDOFF_PROCESS.md:60-62 three-layer seat table (CC / browser / operator)
  evidence: 4 standing seats run (architect, dispatcher, integrator, lane) with seat_registry bind --role and standing orders
  new: name the four seats; point to their orders until they land (DECLARE-TRANSPORT-SCHEMA)
6 docs/handoffs/README.md:~33 "current bundles also carry a PLAN.md"
  evidence: the active bundle has none
  new: scope to the era that had it, or drop
7 bundle DECISION_LEDGER.md (23.5 KB) presents as the ledger
  evidence: to-browser/LEDGER-dev-knowledge.md (09-23) is the live one, waves 0-4B
  new: pointer to the live ledger; fold forward at cut
8 CLAUDE.md §9 "two run -- SessionStart arm_hooks; Stop backpressure" + methodology-roster.md:33 "hard block"
  evidence: settings.json has 8 SessionStart + 2 Stop; backpressure is advisory by its own docstring
  new: regenerate the roster; §9 says 8 + 2 and points at S2's inventory (S2 A6 has 6 more)
9 organ-index.md:100 "PreToolUse: block-onedrive.ps1 ... ARMED"
  evidence: ~/.claude/settings.json has only Notification hooks and disableAllHooks: true
  new: DISARMED since 2026-09-17, owner [#865]
10 bundle RESIDUAL.md names 5 OPEN files; 32 more exist (P11 FAIL)
  new: the next cut's RESIDUAL lists every OPEN file of 09-19..23, or they land first (§5)
```

**Boot byte budget.** `protocols/HANDOFF_BOOT.md` is 17,987 B against an 18,000 B gate, so 13 B of headroom.
The paste is 34,998 B against a 20,000 B ceiling. Paste parts: bundle HANDOFF_BOOT 12,844 · SUPPLEMENT 14,616 ·
RESIDUAL 10,402 · PROBES 8,512.

**SHED:**
- SUPPLEMENT inlined wholesale becomes a JIT pointer (−13.5 KB).
- RESIDUAL narrative becomes drift-flags + OPEN list + pointer to the live ledger (−8 KB).
- Forms §1-3 in the bundle boot become one rendered Ch8 row (−2 KB).
- DECISION_LEDGER is not pasted today; keep it out.

**ADD** (~1.5 KB):
- a harness.yaml pointer (ADR-120 moments);
- the corrected launcher line;
- the 4-seat line;
- a guards-off line (block-onedrive, ADR-77, no expiry).

**Result:** about 11-13 KB, under the ceiling. The 13 B on `protocols/HANDOFF_BOOT.md` is the binding constraint
for AMEND-HANDOFF-BOOT-INTEGRATOR: it lands in the bundle or by pointer, never inline.

## 5 · Landing list — transport decision files 2026-09-19..23 still `carried-by: OPEN`

**Rulings and requests with no repo citation** (`git grep -F` over the repo excluding handoffs: 0 hits):

```
DECLARE-MODEL-AGNOSTIC-2026-09-23         -> ADR-120 stage-13 amendment + router row (O-4b)
DECLARE-COPILOT-TRIAL-2026-09-23          -> provider-registry admission (evidence §1) + routing row
RATIFICATION-2026-09-23-copilot (O-3/O-4) -> STANDING_RULINGS + the rows in §6
DECLARE-NIGHT-AUTONOMY-2026-09-23         -> STANDING_RULINGS + first serial lane of next batch
DECLARE-OFFBOX-PORTABILITY-2026-09-23     -> ADR-120 amendment (portability precondition) + lanes
DECLARE-TRANSPORT-SCHEMA-2026-09-23       -> transport-adapter lane; boot role section by pointer
DECLARE-WINDOW-DEFECTS-2026-09-23         -> one row per item via LANE-5A-5 (D1-D29)
DECLARE-WAVE5A-VERIFICATION-2026-09-23    -> wave-5a contracts (PROVISIONAL until the cross-check)
DECLARE-STATE-STORE-LEARNING-2026-09-23   -> superseded by the state-store ADR (BATCH-ADR-STATE-STORE)
AMEND-ADR-STATE-STORE-2026-09-23          -> same ADR
```

**Homed but not marked:**

```
RATIFICATION-2026-09-22 (O-1/O-2)         -> cited by settings.json, tasks/956 and the rearm audit; O-2's exit conditions 1-2 unrowed
DECLARE-WAVE4B-DIRECTION-2026-09-22       -> tasks 955/957/958/961 carry it; mark carried-by
AMEND-HANDOFF-BOOT-INTEGRATOR-SECTION-0920 -> cited in STANDING_RULINGS; the boot section itself NOT landed (13 B)
DECLARE-SPINE-AND-B3-2026-09-19           -> tasks 915-920 + JOURNAL; mark carried-by
```

**Orders** (BATCH-*, INTEGRATOR-*, *-COMMON, PLAN-*, POSTWAVE-*): 31 files. They need no repo home once
executed. Mark each `carried-by: CLOSED (executed, receipt <file>)` so P11 stops failing on them.
`BATCH-map-verification-2026-09-20` has no `carried-by` line at all.

## 6 · Standing operator requests with no row (17 found; 4 with an OPEN row; 10 with no home)

```
O-2a walk clean on main, xfail removed          -> row: "BUILD MODE exit 1" -- Done when the connection walk is green
                                                    on main with EXPECTED_STOPS empty and the strict xfail deleted
O-2b one real row through the whole loop         -> row: "BUILD MODE exit 2" -- Done when one non-toy OPEN row goes
                                                    row->merge with operator touches = task + GO, from receipts
O-2d re-arm every BUILD-MODE guard at exit       -> row: Done when each guard BUILD MODE disabled is re-armed with a
                                                    live test that a legit lane passes; 2026-11-18 backstop cited
O-4a Copilot is a routine producer               -> row: land the admission (§1 evidence) in provider-registry.yaml
                                                    and an in-repo producer verb; Done when one batch routes >= 1 lane to Copilot by the table
O-4b launcher picks provider/model from routing  -> row: Done when a contract names role+size only, plan_lint refuses a
                                                    model name in a Dispatch block, dispatch.py launch resolves the model
O-4c every operator request is a row same day    -> row: Done when a check lists every RATIFICATION/ANSWER/DECLARE
                                                    "Operator:" item of the window without a citing row, and the boot prints the count (target 0)
R-09-19-3 ARCHITECTURE.md KEPT + exit condition  -> STANDING_RULINGS entry (it lives only in BUILD-LIST, expiry 11-18)
R-09-19-7 lane count by need, not the 6-ceiling  -> STANDING_RULINGS entry
R-09-19-10 the dispatcher dispatches             -> covered by NIGHT-AUTONOMY once it lands; row with it
D-backbone "backbone is code; prose is intent"   -> STANDING_RULINGS doctrine (DECLARE-WINDOW-DEFECTS preamble)
```

**Have an OPEN row:** O-1 → [#944] · O-2c → [#954] · O-2e → [#956] (done by W4B-0; the row can close).

**Adjacent but not matching:**
- D-cap "no cap may ever stop a task" vs [#908] "hard token cap at launch": **these contradict; the architect must
  rule** which one stands.
- The state-store ADR gate runs as a transport order only.

## 7 · Time-critical, in order

```
1. 2026-09-24 -- the 09-17 emergency-disable expiry: re-dated or closed? (the SessionStart eight are re-armed; the
   prompts guard, ADR-77, logs_retention and block-onedrive sit in neither track -- S2 §3)
2. 2026-09-25 -- the counter/expiry verdict on 13 commit hooks: move the counter store first, or read 0 runs as UNMEASURED
3. Before the cut -- land or list the 32 OPEN decision files (P11), and shed the paste to <= 20 KB
4. Merge S1's branch worktree-postwave-changelog @ 66a616a9 (changelog-review, tool-versions bump)
```

DONE 2026-09-23T20:38Z
