---
intake-id: 93
status: DRAFT
origin: DECLARE-BATCH-X-ROSTER-2026-09-11 (the roster) with AMEND-BATCH-X-ROSTER-001 (AX1-1..AX1-8, the file that FREEZES the roster) and AMEND-BATCH-X-ROSTER-002 (AX2-1..AX2-2, X1-6's premise corrected) -- outgoing browser seat 2026-09-10-dev-knowledge-architect, the operator's dispatch of 2026-09-11; carried into the repo 2026-09-11 by batch X lane lane-x-000-batch-x-roster-lands from the operator's transport at to-cc/, LF throughout: DECLARE-BATCH-X-ROSTER-2026-09-11.md (6,244 B, sha256 64e7fc470fa6a0ebebd7d760f640f61c8044f8bd75b5d3683a47ab2c506143b0), AMEND-BATCH-X-ROSTER-001.md (2,543 B, sha256 825cad543568b0cb1747e4dd51a287364a21d677911e5e24ed4eff484b432aed), AMEND-BATCH-X-ROSTER-002.md (972 B, sha256 d0aea9586c51c971fe2bca973acab88dbcd13ae6c7fda796f89ad41f1f8f17d1). Each body below is byte-identical to its source -- only the transport's carried-by line is excluded, as transport metadata whose named successor IS this file, and every line this lane added is inside a marked LANE-ADDED block beside the carried text, never inside it
consumed-by:
---

# Batch X roster -- the four things that make an unattended night SAFE, frozen by AMEND-001 and corrected by AMEND-002
<!-- carried 2026-09-11 by lane lane-x-000-batch-x-roster-lands (branch worktree-lane-x-000-batch-x-roster-lands), TEXT-ONLY: it lands this roster and files the rows the roster marks NEW. It builds none of the mechanisms named here. -->

<!-- LANE-ADDED BEGIN: reading order -->
## 0 · How to read this file (lane's own addition)

Three transport files are carried below, each between explicit `CARRIED BEGIN` / `CARRIED END` markers so the carried bytes stay extractable:

- **Part 1** is the roster (`DECLARE-BATCH-X-ROSTER-2026-09-11`). It is FROZEN by Part 2 and is not reordered, rewritten or improved here.
- **Part 2** is `AMEND-BATCH-X-ROSTER-001`. Where it changes the roster, **the amendment governs** and the roster's superseded text is carried anyway -- this repo's amendment discipline marks a supersession, it does not swap the text out.
- **Part 3** is `AMEND-BATCH-X-ROSTER-002`, which corrects X1-6's premise.
- **Part 4** is the supersession map: which carried lines Parts 2 and 3 govern, written by the lane so a reader is not left to diff three files by eye.
- **Part 5** records what this file does **not** carry, and why that matters to whoever reads it next.
<!-- LANE-ADDED END -->

## Part 1 · DECLARE-BATCH-X-ROSTER-2026-09-11 -- the roster, carried verbatim

<!-- CARRIED BEGIN: DECLARE-BATCH-X-ROSTER-2026-09-11.md sha256=64e7fc470fa6a0ebebd7d760f640f61c8044f8bd75b5d3683a47ab2c506143b0 -->

# DECLARE — batch X roster (draft for outgoing-seat check) · seat 2026-09-10-dev-knowledge-architect

<!-- browser seat · sources: to-browser/DIGEST-2026-09-10-decisions.md (F1–F3, §b census, §c backlog, §f process map), to-browser/LEDGER-OPERATOR-EXPECTATIONS-2026-09-10.md (A–H), AMEND-SESSION-PLAN-006/008/009, REVIEW-…-redteam-3, batch W results · rule: every item is a row (existing id or NEW filed through this intake per ADR-111) — a decided thing with no row is not on this roster · ceiling ADR-110 = 6 lanes per wave, so X runs as X1 then X2 -->

## 0 · What X is for (value, not features)

The operator's target is a night of 8–10 lanes that merge themselves, with no orphaned decision, task or process, and tests that write themselves. Batch W delivered the guard, per-file tests and three decisions as rows. X delivers the four things that make an unattended night SAFE: (1) no decision can be lost, (2) a merge costs minutes not an hour, (3) work runs on GitHub Actions, not on the operator's laptop, (4) a task knows where it is. Everything else waits or is refused.

## 1 · Preconditions (hard)

- HP-X1 batch W integrated: W-8's three rows on `main` (they are lanes X1-1, X1-3, X1-4 below), W-7's selector on `main` (X1-2 depends on it), W-4 on `main` (tag v1.5.0 unblocked).
- HP-X2 operator words: D1 ROOT-CONTRACT (LIFT/KEEP), D8 intake #75 bar, D12 closures, D13 byte bar — packet `to-browser/QUESTION-operator-decisions-2026-09-10.md`.
- HP-X3 this roster checked row-by-row by the outgoing seat against its LEDGER; every SAID item is here as a row or as a written refusal.

## 2 · Wave X1 — six lanes, in value order

| Lane | Row | Value for the operator | Done-when (frozen at dispatch from the row; NEW = to be filed) |
|---|---|---|---|
| X1-1 | W-8 row `decision_coverage` (id at merge) | a decision without a task is refused at commit and at onboarding; never again "decided, scheduled nowhere". Requires the task field the census found missing (F2): `implements:` in `tasks/` frontmatter, structured, validated | row's own (AMEND-009 A9-1..A9-3) + NEW clause: frontmatter key `implements: [ADR-n \| intake-n \| DECLARE-…]`, validated, FPG-1 edge decision→task |
| X1-2 | `[#675]` merge cost | a merge drops from 12–60 min to minutes: W-7's selector wired into `/lane-integrate` (targeted set + tier A per merge; full suite once per batch, not per lane) | `[#675]` verbatim + NEW: integration runs the impacted set per lane; one full suite per batch; measured before/after in the receipt |
| X1-3 | W-8 row conductor E | lanes run on GitHub Actions; required checks (Pro, now live) gate `main`; the laptop is no longer the runner | row's own (DECLARE-CONDUCTOR-DECISION §6 numbers) |
| X1-4 | W-8 row provider routing | scans go to the cheapest admitted model by default; Claude only when no other; the tally names who answered | row's own + NEW: read-only scans default to the cheapest admitted provider |
| X1-5 | `[#664]` spine, clauses 1–3 | `task_coverage` at OPEN, `orphan_census`, three commit-tier refusals — "no orphans" as a mechanism | `[#664]` verbatim (spine only; step D artifact column → X2) |
| X1-6 | `[#687]` four spine keys (ex-W-6) | "where is this task now" answered from the row; hook-written, seat-read-only (A7-1) | row's own + A7-1 writer text |

## 3 · Wave X2 — six lanes

| Lane | Row | Value | Done-when |
|---|---|---|---|
| X2-1 | NEW: closure detector fix (F1: 275 proposals = the whole queue; `surface-closures.ps1` dead since the month-bucket move; 99-runs cap fired) | closure proposals mean something again; the operator sees only STRONG ones | detector discriminates (proposals ≠ queue), surfacing hook alive, cap error gone, RED-first each |
| X2-2 | `[#589]` byte bar + `archive_row_body.py` wired | BACKLOG under its bar by mechanism, not by re-baseline; 30 relocatable bodies moved | `[#589]` verbatim + archive on a cadence (trigger named) |
| X2-3 | `[#669]` conductor (state machine; library-first check first) | phases fire from state; retries increment `attempts`; C-2 derived flags | `[#669]` verbatim |
| X2-4 | `[#664]` step D + organ-map reconcile (`process-list` 158 vs Ch2 64) | one process map with trigger AND artifact; 40 trigger-less processes each get a trigger or leave | artifact column exists; Ch2 renders from the same source; count reconciled |
| X2-5 | `[#667]` docs (ARCHITECTURE ≤ 15 KB rendered, PLAYBOOK by chapter, dispatch split, ESSENTIALS gone) | every new session reads the architecture whole | `[#667]` verbatim |
| X2-6 | NEW: telemetry trigger-or-remove (4 modules, A6-2) + `[#685]` GO as artifact | no inventory pretending to be process; GO leaves a file dispatch reads | modules wired or deleted; dispatch refuses without the GO file, trip-tested |

## 4 · Rows only (filed, not lanes this batch)

`[#686]` P11 predicate · `[#242]` ADR status-transition gate · `[#616]` flip-condition in 91 ADRs (thesis lack #1) · NEW: intake #70 (AJ second pass) zero-row → its practices rowified · NEW: M03 leg-1a re-run (agy, stdout, tracked audit) · NEW: codespace detached-lane ZERO WORK · NEW: SEAT-BOOT render per-merge-GO defect + three-grammar collision + amendment-vs-control-surface ruling (AW5-4) · NEW: review fallback when Codex is on quota (C5) · NEW: nightly routines (B7, zero `schedule:`) — after X1-3 · NEW: W-7's owed MED (empty-selection hardening) · ledger A6 (CLAUDE.md §7–§9 generated), A8 (doc congruence).

## 5 · Written refusals / no implementation required

The 16 legacy Accepted ADRs (27…95, all pre-2026-07-04) with zero rows: disposition "legacy doctrine, implemented by the corpus as it stands" recorded per ADR by X1-1's mechanism, not 16 rows. `boot_frontier` rows #581, #625 (organ-adding) refused; #528 folded into X1-2's measurement. AI Council: out.

## 6 · Trial night (from red-team 2, A7-4)

After X1 merges: one night at the current ceiling, auto-merge ON only for serialize-group-disjoint lanes with a green targeted suite, integrator present read-only, halt on RED. It measures N7 (conflict), N9 (revert), N10 (resources) before the ceiling is lifted in Y.

=== END OF DECLARE ===

<!-- CARRIED END: DECLARE-BATCH-X-ROSTER-2026-09-11.md -->

## Part 2 · AMEND-BATCH-X-ROSTER-001 -- carried verbatim; **with this file Part 1 is FROZEN**

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-001.md sha256=825cad543568b0cb1747e4dd51a287364a21d677911e5e24ed4eff484b432aed -->

# AMEND — batch X roster, 001 (outgoing-seat row-by-row check folded; roster FROZEN)

<!-- browser seat · source: to-browser/REVIEW-2026-09-11-batch-x-roster.md (34/37 carried, 2 MISSING, 1 mis-scoped, 1 unrostered act) · every change accepted · with this file the roster DECLARE-BATCH-X-ROSTER-2026-09-11 is frozen -->

- **AX1-1 · X1 order:** X1-1 decision_coverage · **X1-2 conductor E** · **X1-3 merge cost** · X1-4 routing · X1-5 spine · X1-6 keys. Reason: the merge-cost lane optimises the integration path conductor E replaces; landing it first spends a lane on a path the next lane deprecates and makes `[#675]`'s before/after incomparable across the substrate boundary.
- **AX1-2 · decision_coverage `implements:`** accepts only identifiers that RESOLVE — an ADR number present in `docs/decisions/`, an intake number present in `docs/intake/`, a transport decision filename that exists; free text is refused. RED-first fixture: this window's own backlog — at least one existing decision with no task FAILS the check before the lane fixes it.
- **AX1-3 · merge cost Done-when adds:** (a) the full suite runs once at the END of the batch on the merged result, and a RED full suite is a batch-level HALT, not a report; (b) the receipt records minutes-to-merge split into test time and ceremony time; (c) `backlog-filing-backpressure` stops refusing merge commits (diff-scoped; the merge re-presents rows as new) — the ceremony cause named in LEDGER E2. Precondition before dispatch: W-7's owed MED is fixed — an empty selection FAILS closed (runs everything), never passes as "nothing impacted".
- **AX1-4 · §4 gains a row:** NEW `propose_closures` writes ONE file overwritten per run (LEDGER D5); paired with X2-1.
- **AX1-5 · A8 (doc congruence 34/113) moves into X2-4** as a clause — one traversal, two reports.
- **AX1-6 · §5 gains:** the PowerShell dispatch retirement act (`DECLARE-DISPATCH-RETIREMENT`) is batch Y, unblocked by X1-2 (conductor E); its ordering condition ("new hands hold before old hands let go") becomes satisfiable when X1-2 merges.
- **AX1-7 · §0 gains one sentence:** X makes the night safe; it ships nothing to a consumer — bytes to corp-monorepo stay zero until the v1.5.0 tag and `[#670]`.
- **AX1-8 · Recorded:** C4 model-agnosticism is NOT closed by X1-4 (routing ≠ agnosticism); aliases, unified contract, `MODEL_ENUM` source and churn insulation stay with `[#568]` / `[#582]`, batch Y.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-001.md -->

## Part 3 · AMEND-BATCH-X-ROSTER-002 -- carried verbatim

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-002.md sha256=d0aea9586c51c971fe2bca973acab88dbcd13ae6c7fda796f89ad41f1f8f17d1 -->

# AMEND — batch X roster, 002 (X1-6 premise corrected)

<!-- browser seat · source: dispatcher report 2026-09-11 on W-3 (74990bf3): W-3 produced a per-guard identity (Guard.key = module::target), not a writer callable; A7-1's "skipped_gates' writer is W-3's output" was narrower than it read -->

- **AX2-1 · X1-6 builds the `skipped_gates` writer itself:** an event-fired hook that, when a guard's `skipif` fires, appends that guard's `Guard.key` (W-3's identity) to the row's `skipped_gates`. W-3 is a dependency (the key), not the writer. A7-1's other three keys unchanged. RED-first test: write `skipped_gates` by hand; the next skipif fire overwrites it.
- **AX2-2 · Recorded, not a defect:** thirteen guards in `tests/test_review_artifact_coverage.py` still carry `requires_git`; they are individually dispositionable, which is what `[#638]` asked; the module is not unskippable.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-002.md -->

<!-- LANE-ADDED BEGIN: supersession map -->
## Part 4 · Supersession map (lane's own addition, beside the carried text)

Every entry below points at carried text that a later carried file governs. **Nothing in Parts 1-3 was edited to produce this map** -- it is the marker, and the superseded wording stays where it was written.

- **Part 1 §2, the X1 lane ORDER is superseded by AX1-1.** The roster's table runs X1-1 decision_coverage, X1-2 merge cost, X1-3 conductor E, X1-4 routing, X1-5 spine, X1-6 keys. AX1-1 reorders to X1-1 decision_coverage · **X1-2 conductor E** · **X1-3 merge cost** · X1-4 routing · X1-5 spine · X1-6 keys. The lane labels in Part 1's table are therefore stale for X1-2 and X1-3 and the AMEND's order governs. Reason carried in AX1-1: landing the merge-cost lane first spends it optimising the integration path conductor E replaces.
- **Part 1 §2 X1-1's Done-when is extended by AX1-2.** `implements:` accepts only identifiers that RESOLVE -- an ADR number present in `docs/decisions/`, an intake number present in `docs/intake/`, a transport decision filename that exists; free text is refused. The RED-first fixture is this window's own backlog.
- **Part 1 §2 X1-2's (merge cost) Done-when is extended by AX1-3**, clauses (a) full suite once at batch END and a RED full suite is a batch-level HALT, (b) the receipt splits minutes-to-merge into test time and ceremony time, (c) `backlog-filing-backpressure` stops refusing merge commits. AX1-3 also adds a PRECONDITION before dispatch: W-7's owed MED is fixed -- an empty selection FAILS closed.
- **Part 1 §2 X1-6's premise is corrected by AX2-1.** The roster's X1-6 rests on A7-1 reading W-3's output as the `skipped_gates` writer. W-3 produced a per-guard IDENTITY (`Guard.key = module::target`), not a writer callable, so **X1-6 builds the writer itself** and W-3 is a dependency, not the writer. A7-1's other three keys are unchanged.
- **Part 1 §4 gains a row from AX1-4:** NEW `propose_closures` writes ONE file overwritten per run (LEDGER D5), paired with X2-1.
- **Part 1 §4's A8 (doc congruence) is superseded by AX1-5** -- it is no longer a row of its own; it moves into X2-4 as a clause, one traversal producing two reports.
- **Part 1 §5 gains an entry from AX1-6:** the PowerShell dispatch retirement act (`DECLARE-DISPATCH-RETIREMENT`) is **batch Y**, unblocked by conductor E; it is a written deferral, not a row.
- **Part 1 §0 gains one sentence from AX1-7:** X makes the night safe and ships nothing to a consumer -- bytes to corp-monorepo stay zero until the v1.5.0 tag and `[#670]`.
- **Recorded by AX1-8, and it closes nothing:** C4 model-agnosticism is NOT closed by X1-4 (routing is not agnosticism); aliases, the unified contract, the `MODEL_ENUM` source and churn insulation stay with `[#568]` / `[#582]` in batch Y.
- **Recorded by AX2-2, and it is not a defect:** thirteen guards in `tests/test_review_artifact_coverage.py` still carry `requires_git`; they are individually dispositionable, which is what `[#638]` asked, and the module is not unskippable.
<!-- LANE-ADDED END -->

<!-- LANE-ADDED BEGIN: not carried -->
## Part 5 · What this file does NOT carry (lane's own addition)

**Three further amendments to this roster exist on the operator's transport and are NOT carried here.** They are recorded rather than folded, because folding them would be a deviation the lane is not authorised to make -- and leaving them unnamed would make this file a carrier that silently drops payloads which name it as their carrier.

`to-cc/AMEND-BATCH-X-ROSTER-003.md`, `-004.md` and `-005.md` each carry the line `carried-by: docs/intake/2026-09-11-tech-batch-x-roster.md` -- **this file** -- and each POSTDATES the freeze this file was written against:

```
12:43  DECLARE-BATCH-X-ROSTER-2026-09-11   carried here as Part 1
13:00  AMEND-001  (roster FROZEN)          carried here as Part 2
13:13  AMEND-002                           carried here as Part 3
13:24  lane contract created
13:26  AMEND-003                           NOT carried -- 37s before the
13:26  lane contract last written           contract's final write
13:29  AMEND-004                           NOT carried
13:34  AMEND-005                           NOT carried
```

The lane's frozen contract names exactly three sources and freezes the NEW-row set against them, so this file carries three. What the uncarried three contain, stated so the next reader can size the gap without re-reading the transport:

- **AMEND-003** (self-review, four misses): the Codespace committing-lane ruling as a STANDING ruling rather than a workaround; conductor E ships to consumers as a floor component; the **docs cut moves into X1 replacing X1-6**, which moves to X2; a logs lane in X2; prompt distiller `[#617]` heads X2; token use recorded honestly.
- **AMEND-004** (the hub IS the floor): `floor: MUST | hub-only` mandatory on every row and lane contract, applied retroactively to batch W's outputs; model and cost declared per lane by `gen_lane_contract.py`; docs are floor components; four read-only facts owed before X1 dispatches.
- **AMEND-005** (management map): telemetry moves from X3 into X1 as a clause of X1-4; a NEW **management map** row in X2; a path-registry fact owed, with a NEW row conditional on the answer.

**What this does and does not change about the rows filed under this intake.** Every row the frozen roster marks NEW still exists under 003-005 -- those amendments re-assign WAVES and add FURTHER rows; they retire none of the rows filed here. Wave assignment is not this intake's surface. So the filed set is correct and incomplete rather than wrong, and the delta is additive: the docs-cut row, the management-map row, the conditional path-registry row, the `floor:` declaration clause and the per-lane model/cost clause are **owed to a follow-up act**, not silently lost.

Landing them is a decision for the operator or the next architect seat, not for this lane: carrying them would have changed a NEW-row enumeration that the lane's contract froze **specifically so the lane could not over-file by judgment**.
<!-- LANE-ADDED END -->

=== END ===
