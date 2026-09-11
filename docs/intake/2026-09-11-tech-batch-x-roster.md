---
intake-id: 93
status: DRAFT
origin: DECLARE-BATCH-X-ROSTER-2026-09-11 (the roster) with AMEND-BATCH-X-ROSTER-001 (AX1-1..AX1-8, the file that FREEZES the roster), AMEND-BATCH-X-ROSTER-002 (AX2-1..AX2-2, X1-6's premise corrected) and AMEND-BATCH-X-ROSTER-006 (AX6-1..AX6-5, the domain census and folder-as-domain), AMEND-BATCH-X-ROSTER-007 (AX7-1..AX7-5, the decision engine, the path registry, catalog shape and the dispatcher defects), AMEND-BATCH-X-ROSTER-008 (AX8-1..AX8-5, interim routing, the log-review routine, test-baseline debt and the torn-down-cwd hazard), AMEND-BATCH-X-ROSTER-009 (AX9-1..AX9-5, the model must use the organs it builds), AMEND-BATCH-X-ROSTER-010 (AX10-1..AX10-3, the backlog shrinks by mechanism: evidenced bulk closure at every batch close), AMEND-BATCH-X-ROSTER-011 (AX11-1..AX11-4, two operator ratifications honoured and cleanup made an act) and, as the intake body of the path row AX7-3 files, QUESTION-path-registry-2026-09-11 with AMEND-PATH-REGISTRY-001 -- outgoing browser seat 2026-09-10-dev-knowledge-architect, the operator's dispatch of 2026-09-11; the first three are the lane contract's named source set, and AMEND-006 was added by the operator instruction of 2026-09-11 relayed to the lane after its first commit ("X-0 applies AMEND-BATCH-X-ROSTER-006 (rows: visualization, packet D14, W-4 residue) -- follow-up commit if already committed"), and AMEND-007 plus the two path-registry files by a second operator instruction the same day; AMEND-010 and AMEND-011 arrived by a further operator instruction the same day, after this lane had already committed its close packet, and are folded here rather than into a new intake because both declare carried-by: THIS file. Carried into the repo 2026-09-11 by batch X lane lane-x-000-batch-x-roster-lands from the operator's transport at to-cc/, LF throughout: DECLARE-BATCH-X-ROSTER-2026-09-11.md (6,244 B, sha256 64e7fc470fa6a0ebebd7d760f640f61c8044f8bd75b5d3683a47ab2c506143b0), AMEND-BATCH-X-ROSTER-001.md (2,543 B, sha256 825cad543568b0cb1747e4dd51a287364a21d677911e5e24ed4eff484b432aed), AMEND-BATCH-X-ROSTER-002.md (972 B, sha256 d0aea9586c51c971fe2bca973acab88dbcd13ae6c7fda796f89ad41f1f8f17d1), AMEND-BATCH-X-ROSTER-006.md (2,809 B, sha256 f53a5369d607d7da615610b6d34cd33800801e595d7f075a441b8077fda05a48), AMEND-BATCH-X-ROSTER-007.md (2,961 B, sha256 ce9fbb2eb28b0cda4112f7920b1388573a2606c9f12c043790a0ccc8e1647912), QUESTION-path-registry-2026-09-11.md (2,883 B, sha256 9d78522da72537b8a719732549dd67b703b15d453eb7eedeac218050c2e51b37), AMEND-PATH-REGISTRY-001.md (2,269 B, sha256 8893a0235a3edfd31a551d85daf0ad9d0c588d35e348e26f2e4cd3af0cbd2fd8), AMEND-BATCH-X-ROSTER-008.md (2,141 B, sha256 84d5b28a775e5f5399e229a14a0cbc97f6b2c0e8201e0a89c6dc9c9278a76538), AMEND-BATCH-X-ROSTER-009.md (2,850 B, sha256 31b802d23aca38364d2610b3426efd48084d546a747e608fdf9f0e0e2fe8b6ac), AMEND-BATCH-X-ROSTER-010.md (1,446 B, sha256 6a241cbf184745d63305ae16acca2e786dbff5a35e208a26f2b9f46e10b44ebe), AMEND-BATCH-X-ROSTER-011.md (1,739 B, sha256 27653345b0cd42c9a4fce5baeed159822262acfa91960dfaf642a31f769e7a86). Each body below is byte-identical to its source -- only the transport's carried-by line is excluded, as transport metadata whose named successor IS this file, and every line this lane added is inside a marked LANE-ADDED block beside the carried text, never inside it
consumed-by:
---

# Batch X roster -- the four things that make an unattended night SAFE, frozen by AMEND-001, corrected by AMEND-002, extended by AMEND-006, AMEND-007, AMEND-008 and AMEND-009
<!-- carried 2026-09-11 by lane lane-x-000-batch-x-roster-lands (branch worktree-lane-x-000-batch-x-roster-lands), TEXT-ONLY: it lands this roster and files the rows the roster marks NEW. It builds none of the mechanisms named here. -->

<!-- LANE-ADDED BEGIN: reading order -->
## How to read this file (lane's own addition, not part of the roster)

Nine transport files are carried below, each between explicit `CARRIED BEGIN` / `CARRIED END` markers so the carried bytes stay extractable:

- **Part 1** is the roster (`DECLARE-BATCH-X-ROSTER-2026-09-11`). It is FROZEN by Part 2 and is not reordered, rewritten or improved here.
- **Part 2** is `AMEND-BATCH-X-ROSTER-001`. Where it changes the roster, **the amendment governs** and the roster's superseded text is carried anyway -- this repo's amendment discipline marks a supersession, it does not swap the text out.
- **Part 3** is `AMEND-BATCH-X-ROSTER-002`, which corrects X1-6's premise.
- **Part 4** is `AMEND-BATCH-X-ROSTER-006`, added by operator instruction after this file's first commit. **It depends on `AMEND-005`, which is NOT carried** -- see Part 13, which names the dangling references precisely.
- **Part 5** is `AMEND-BATCH-X-ROSTER-007`, added by a second operator instruction the same day: the decision engine, the path registry, catalog shape and the dispatcher defects.
- **Parts 6 and 7** are `QUESTION-path-registry-2026-09-11` and `AMEND-PATH-REGISTRY-001`. They are not roster amendments -- together they are the **intake body of the path row** AX7-3 files (`[#715]`), carried here because APR-5 routes the decision through this intake. **The amendment governs where the two differ**, and APR-1 differs from the QUESTION on its central claim.
- **Part 8** is `AMEND-BATCH-X-ROSTER-008`: interim routing, the log-review routine, test-baseline debt, templates as floor components, and the torn-down-worktree cwd hazard.
- **Part 9** is `AMEND-BATCH-X-ROSTER-009`: the model must USE the organs it builds -- deny-and-point, organ skills, queries as tools, exists-before-build.
- **Part 10** is `AMEND-BATCH-X-ROSTER-010`: the backlog shrinks by MECHANISM -- evidenced bulk closure at every batch close, the X2 backlog lane's two added clauses, and backlog management as a floor MUST.
- **Part 11** is `AMEND-BATCH-X-ROSTER-011`: two operator ratifications this window breached, honoured -- committing lanes run local OVERNIGHT ONLY, and the operator never types a path -- plus cleanup as an ACT rather than a note.
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

## Part 4 · AMEND-BATCH-X-ROSTER-006 -- carried verbatim (added by operator instruction, 2026-09-11)

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-006.md sha256=f53a5369d607d7da615610b6d34cd33800801e595d7f075a441b8077fda05a48 -->

# AMEND — batch X roster, 006 (domain census; folder = domain; the managements the seat forgot)

<!-- browser seat · trigger: operator 2026-09-11 — the seat's seven managements missed ecosystem, logs/garbage, protocols-as-process, visualization/dashboard, scripts, templates; his model: every folder is a domain with an owning process, process management on top; his fear: many implemented processes are orphans nobody remembers; use cheap models for the census · sources already measured: 40/158 untriggered processes, 39 orphan files, 4 unwired telemetry modules, 16 zero-row ADRs, 485 log files -->

- **AX6-1 · Lane X-C "domain census", read-only, text-only output, dispatch NOW (parallel to batch W integration; no repo write beyond one audit file).** One page per top-level folder — `protocols/` `docs/` `ecosystem/` `scripts/` `tests/` `templates/` `tasks/` `logs/` `deploy/` `.claude/` — starting with PLAYBOOK and JOURNAL: for every organ/script/doc/template in it: what triggers it (hook · gate · command · schedule · NOTHING), who reads its output (organ · seat · NOBODY), last touched, verdict LIVE / UNTRIGGERED / UNREAD / GARBAGE-CANDIDATE. Sources first, never re-derived: `ecosystem/organ-index.md`, `graph_queries.py process-list`, the 2026-09-08 census, `file_purpose_graph.py`, git log. Output `docs/audits/2026-09-11-technical-domain-census.md` (date-slug; authorization: this ruling) + a MANIFEST of counts per folder. Model: cheapest admitted — Claude subagents until W-2 merges, agy stdout-only after. No deletion, no rename; GARBAGE-CANDIDATE is a proposal for the operator's GO.
- **AX6-2 · Management map (AX5-2) gains rows:** ecosystem · logs · protocols/docs · visualization · scripts · templates · tasks — one row per folder-domain, owner-process named or DEAD.
- **AX6-3 · NEW row, X2: visualization.** Task flow charts (open/closed per week, lanes per batch, merge minutes, cost per lane) rendered from the same telemetry the tally feeds (AX5-1); library-first — Maister's dashboard plugin studied for SHAPE, not copied; the existing chaotic dashboard/conformance.html folded in or deleted (intake #42 MIGRATE-not-delete).
- **AX6-4 · Operator packet gains D14:** folder-as-domain — rename `docs/` → `process/`? one owning process per folder? decided AFTER X-C's census, with its per-folder verdicts as the input; the seat recommends no rename before the census.
- **AX6-5 · W-4 close residue (integrator):** regenerate the organ index (64 → 63), fix `CLAUDE.md:138`, re-derive the ship-gate WARN delta; `graph_queries.py` ORPHAN_DISPOSITIONS' 2026-09-07 "keep /override as retirement notice" line is superseded by AW6-1 — updated at batch close as a row.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-006.md -->

## Part 5 · AMEND-BATCH-X-ROSTER-007 -- carried verbatim (added by operator instruction, 2026-09-11)

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-007.md sha256=ce9fbb2eb28b0cda4112f7920b1388573a2606c9f12c043790a0ccc8e1647912 -->

# AMEND — batch X roster, 007 (decision engine; path registry; catalog shape; dispatcher defects)

<!-- browser seat · trigger: operator 2026-09-11 — architectural decisions must not be the browser's thought exercise: browser proposes → intake → an algorithm built on his thesis produces the decision table and the ADR → ruling → backlog; folders are the LAST aspect, path management first; ITIL process owner; Backstage catalog shape, library-first · plus four dispatcher findings from X-C's dispatch -->

- **AX7-1 · X1-1 becomes the DECISION ENGINE, two halves, one lane.** (a) BIRTH: the intake template carries the thesis scenario (bodziec · źródło · odpowiedź · miara odpowiedzi · środowisko · artefakt), closed questions, alternatives with benefits/trade-offs, flip condition; `gen_adr.py` renders the decision table and the sensitivity re-run (all answers NIE → does the recommendation flip) into the ADR; the ADR gate refuses any ADR missing a field; the ruling per ADR-108 §A. Library-first: MADR as the template shape (Decision Drivers · Considered Options · Pros and Cons) + the three thesis fields MADR lacks (response measure, flip condition, sensitivity). Absorbs `[#616]` (flip condition) and `[#242]` (status transitions). (b) EXECUTION: `decision_coverage` and `implements:` as in AX1-2 / AX4-1. Done-when: this window's own DECLAREs replayed through the engine as the RED-first fixture — at least one is refused for a missing field before the lane fixes it.
- **AX7-2 · Docs cut moves to X2 head** (operator: naming and structure are the last aspect; decisions first). X1 = decision engine · conductor E · merge cost · routing+telemetry · spine `[#664]` · `[#687]` keys.
- **AX7-3 · Path registry row is X2, not conditional:** one source of governed paths read by generators and verbs; a path not in it is refused. Evidence: three instances in one day — contracts written to `to-cc/` while `Dispatch-Lane` reads the prompts root; the generator-carried line omits `-Model` so a sonnet contract runs at opus; `worktree.baseRef` unset so lanes branch two merges behind local `main`. Each is a row (FILE) with a RED-first test; the step-0 sync stays mandatory until baseRef is fixed.
- **AX7-4 · Catalog shape, library-first:** `ecosystem/organ-index` entries validated against Backstage's `catalog-model` Component JSON schema (owner · lifecycle · system · dependsOn) by our own gate; no Backstage runtime. Portal revisited only if X-C's census shows a scale that needs browsing. X-C's `owner` and `lifecycle` columns are the first fill.
- **AX7-5 · Recorded from X-C's dispatch:** `config/` and `plugins/` were missing from AX6-1's folder list (added); "cheapest admitted" resolves to sonnet — haiku is not in `provider-registry.yaml`'s admission (a routing-lane fact); `-Model` must be explicit until AX7-3 lands.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-007.md -->

## Part 6 · QUESTION-path-registry-2026-09-11 -- carried verbatim; the intake body of `[#715]`, **superseded on its central claim by Part 7**

<!-- CARRIED BEGIN: QUESTION-path-registry-2026-09-11.md sha256=9d78522da72537b8a719732549dd67b703b15d453eb7eedeac218050c2e51b37 -->

# QUESTION — path registry: proposal for decision (thesis decision table), 2026-09-11

<!-- browser seat · a PROPOSAL, not a ruling — per the operator's rule that architectural decisions pass through intake and the thesis method, not the browser's head · lands as an intake via X-0's row (AX7-3), decided by the engine once X1-1 exists, or by the current ADR process with this table until then -->

**Scenario (thesis framing).** Stimulus: a generator writes a governed path and a verb reads it. Source: any script in the hub or win-tooling. Environment: hub + every consumer (floor). Artifact: lane contracts, transport files, worktrees, manifests. Response: both resolve the same location from one declaration; a path outside it is refused. **Response measure:** zero path mismatches per batch (today: 3 in one day — contracts `to-cc/` vs prompts root; launch line without `-Model`; `worktree.baseRef` unset → lanes two merges behind `main`), and a folder rename = one registry value.

**Closed questions:** Q1 Must Python generators and PowerShell verbs read the same declaration? Q2 Must a gate refuse a governed path written as a literal? Q3 Will folders be renamed after the census (D14)? Q4 Must it ship in the floor to every consumer?

| Option | Q1 same source | Q2 gate | Q3 rename cost | Q4 floor | Build cost |
|---|---|---|---|---|---|
| **A · registry file + one resolver per language + literal-path gate** | yes | yes (lint refuses literals of governed paths) | one value | yes | medium |
| B · environment variables per root (extend `CLAUDE_PROMPTS_DIR`) | partly — per machine | weak (env use is hard to lint) | every machine | fragile | low |
| C · fix the three defects only | no | per-defect tests only | hunt every literal | n/a | lowest |

**Recommendation: A**, with C's three fixes as its first three RED-first commits (they are needed under any option): (1) the generator writes lane contracts to the location the verb reads — one key; (2) the launch line is rendered from the contract's `Model` row, and a test asserts they match; (3) `worktree.baseRef` points at local `main` (CC verifies the setting name), and a test asserts a lane's base equals `main` HEAD at dispatch.
**Format sub-question (library-first):** YAML is the house convention (`provider-registry.yaml`, `parity-surfaces.yaml`); PowerShell reads YAML only with a module, JSON natively. CC checks whether win-tooling already carries a YAML reader → YAML; else JSON.
**Flip condition:** A flips to B if the census and DIGEST-2026-09-11-floor-and-cost show fewer than ~10 governed roots, all already behind environment variables.
**Sensitivity (thesis §REVIEW):** answer Q3 NO (no renames ever) and Q4 NO → C wins on cost; with Q3 YES (D14 is on the operator's packet) A holds.

`disposition: OPEN — decided via intake after X-0 lands the row`

=== END OF QUESTION ===

<!-- CARRIED END: QUESTION-path-registry-2026-09-11.md -->

## Part 7 · AMEND-PATH-REGISTRY-001 -- carried verbatim; **governs Part 6 where they differ**

<!-- CARRIED BEGIN: AMEND-PATH-REGISTRY-001.md sha256=8893a0235a3edfd31a551d85daf0ad9d0c588d35e348e26f2e4cd3af0cbd2fd8 -->

# AMEND — path registry question, 001 (no new registry: FPG-1 IS the registry; roots are config)

<!-- browser seat, Fable · corrects to-cc/QUESTION-path-registry-2026-09-11.md, which proposed a registry beside the one that exists · witnesses: FPG-1 armed in batch V (216-file census, edges triggers/imports/implements, queries why/stats); ARCHITECT-INBOX-2026-09-05-009 candidates (c) derived-copies registry, (j) freshness registry, per-consumer registry — filed, never decided -->

- **APR-1 · The registry the operator describes exists: FPG-1.** path · purpose · trigger · edges · query. Option A of the QUESTION is withdrawn as a new build; it becomes "FPG-1 completed": (1) a `writes` edge / artifact column (`[#664]` step D); (2) last-touched and how — read from git at query time, never stored twice; (3) FPG-1 wired as the spine so it is called, not re-read (`[#664]` clauses 1–3). No second graph.
- **APR-2 · Roots are configuration, one declaration.** The three defects (contracts in `to-cc/` vs prompts root; `-Model` dropped from the launch line; `worktree.baseRef` unset) are about ROOT locations, not file purpose. One root declaration (transport root, worktree base, prompts dir, outputs) read by FPG-1's loaders AND by the PowerShell verbs; the literal-path lint refuses a governed root written inline. Library-first: `platformdirs` for OS-standard dirs (config/cache/data); git for history; nothing hand-rolled beyond the declaration itself.
- **APR-3 · The three fixes ship first, each RED-first** (unchanged from the QUESTION): generator writes where the verb reads; launch line rendered from the contract's Model row with a match test; lanes branch from local `main` HEAD.
- **APR-4 · Inbox-009's candidates (c), (j), per-consumer registry are re-filed as clauses of this row**, not as separate registries: derived-copy = an FPG-1 edge kind; freshness = a query over last-touched; per-consumer = the same graph per repo root, joined by the floor manifest.
- **APR-5 · Decision route:** this amendment and the QUESTION are the intake body; the decision is made by the engine (X1-1) with the thesis table — the browser proposes, it does not rule.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-PATH-REGISTRY-001.md -->

## Part 8 · AMEND-BATCH-X-ROSTER-008 -- carried verbatim (added by operator instruction, 2026-09-11)

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-008.md sha256=84d5b28a775e5f5399e229a14a0cbc97f6b2c0e8201e0a89c6dc9c9278a76538 -->

# AMEND — batch X roster, 008 (cheap models now; log review as self-healing; tests; templates; cwd hazard)

<!-- browser seat · trigger: operator 2026-09-11 — token optimisation not visible; logs must feed a self-healing review; tests and templates not mentioned · plus the dispatcher's torn-down-cwd finding -->

- **AX8-1 · Interim routing, effective when W-2 is on `main`:** every read-only digest, census or scan defaults to `agy` (stdout-only, serialised ≤ 1, CC verifies every locator); Claude only when agy refuses or the task commits. Recorded per run in the receipt (model, tokens). X1-4 routing replaces this interim rule with the registry.
- **AX8-2 · NEW row, X2: log-review routine (self-healing).** Scheduled (daily; every 3 days until E is live) on the cheapest admitted model: reads logs + telemetry, flags anomalies — a model that does not deliver (failed/empty legs per provider), a stuck or zero-work lane, a cost spike, a gate firing on empty — writes one digest and files each anomaly as a row. Depends on C2 telemetry (X1-4) and B7 nightly routine (after X1-2). Folded with the logs lane (AX3-4).
- **AX8-3 · NEW row, X2: test-baseline debt.** The 26 permanently RED tests on the Windows baseline are each fixed or dispositioned with a reason; a baseline that stays red hides new failures. Plus the xdist frozenset-identity pollution (`test_manifest_link_route`) as its own row. Test management = B1 impacted selection · B2 refusal without a test · B3 one full suite per batch · this row.
- **AX8-4 · Templates are floor components** (the new-project starter): covered by X-C's census (`templates/`), declared MUST under AX4-1, rendered from the same source as the docs after the cut.
- **AX8-5 · NEW row (FILE, RED-first): a session whose worktree was torn down silently resolves to the primary checkout** — a write from it lands on the integrator's branch. Teardown must end or refuse sessions on that worktree; the Stop hook detects cwd-not-a-worktree and refuses writes. Witness: dispatcher session, 2026-09-11.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-008.md -->

## Part 9 · AMEND-BATCH-X-ROSTER-009 -- carried verbatim (added by operator instruction, 2026-09-11)

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-009.md sha256=31b802d23aca38364d2610b3426efd48084d546a747e608fdf9f0e0e2fe8b6ac -->

# AMEND — batch X roster, 009 (the model must use the organs it builds: deny-and-point, organ skills, queries as tools, exists-before-build)

<!-- browser seat, Fable · trigger: operator 2026-09-11 — CC builds tools it never calls, greps instead of querying, creates orphans; is this known, what defends against it, what do Anthropic / Maister / AJ say · research: Anthropic hooks/skills/MCP docs; community finding "Claude Code ignores its own tools" (fix: PreToolUse deny with a pointer); Maister: orchestrator state drives phases so the model does not choose; AJ: harness = process · four rows, all mechanisms; one metric -->

- **AX9-1 · NEW row, X1 (joins X1-1's lane or its own — dispatcher's call on serialize-groups): deny-and-point hook.** A `PreToolUse` hook on `Bash`/`Grep`: a raw search (`grep`, `rg`, `find`, `Select-String`) over governed questions — what is this file, who triggers it, where does X live, which tests cover Y, is there already an organ for Z — is DENIED with the exception text naming the organ to run (`graph_queries.py why|process-list`, the impacted-test selector, organ-index). RED-first: a trip-test sends a raw grep and asserts the denial and the pointer. Precondition: CC verifies on this version that a PreToolUse deny on Bash actually blocks (a known upstream issue reported the opposite); if it does not, the same rule lives in `UserPromptSubmit`/skill hooks. Floor: MUST.
- **AX9-2 · NEW row, X2: organ skills, generated.** Every organ in `ecosystem/organ-index.md` that answers a question gets a skill whose description states WHEN to invoke it, rendered from the index (never hand-written) — progressive disclosure means the description is what the model matches. This is `[#617]` prompt distiller's simplest form and its first deliverable.
- **AX9-3 · NEW row, X2: FPG-1 queries exposed as tools (MCP, library-first).** A minimal stdio MCP server exposing `why`, `process-list`, `stats` and the test selector, so they sit in CC's tool list next to Grep; Codex/agy can reach the same server. No new query logic — the server calls the existing scripts.
- **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".
- **AX9-5 · Metric (telemetry, X1-4): raw-search calls vs organ calls per session, and organs never called in 30 days.** The log-review routine (AX8-2) flags regressions. Value: the operator sees in one number whether the model uses the harness or rebuilds it.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-009.md -->

## Part 10 · AMEND-BATCH-X-ROSTER-010 -- carried verbatim (added by operator instruction, 2026-09-11)

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-010.md sha256=6a241cbf184745d63305ae16acca2e786dbff5a35e208a26f2b9f46e10b44ebe -->

# AMEND — batch X roster, 010 (backlog shrinks by mechanism: evidenced bulk closure per batch)

<!-- browser seat · trigger: operator 2026-09-11 — the backlog is huge, tasks are never archived, when does it get smaller; the fix must be systemic and universal · witnesses: 80 KB / 275 open rows; births 2.4× closures; 101 rows over 1,320 chars; 30 bodies relocatable by archive_row_body.py; closure detector proposes the whole queue; closing a row is the operator's act and nobody hands him closures in bulk -->

- **AX10-1 · Evidenced bulk closure at every batch close.** The close packet lists every row whose Done-when the batch's merges witnessed — row id · Done-when verbatim · the merged SHA and the test/gate that proves it — and asks the operator for ONE word to close them all. A row with no witness is not listed. First application: batch W (#683 `/override`, #638 proof layer, #278 test selection, #688 harness definition, #684 guard if merged).
- **AX10-2 · The X2 backlog lane (`[#589]` + `archive_row_body.py`) adds:** narration relocates to `tasks/archive/` on a trigger (at each batch close), not by hand; the closure budget "close before filing" is enforced — a batch that files more rows than it closes reports the overdraft in its close packet.
- **AX10-3 · Floor: MUST.** Backlog management is identical in every consumer repo.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-010.md -->

## Part 11 · AMEND-BATCH-X-ROSTER-011 -- carried verbatim (added by operator instruction, 2026-09-11)

<!-- CARRIED BEGIN: AMEND-BATCH-X-ROSTER-011.md sha256=27653345b0cd42c9a4fce5baeed159822262acfa91960dfaf642a31f769e7a86 -->

# AMEND — batch X roster, 011 (two operator ratifications this seat breached; cleanup becomes an act)

<!-- browser seat · source: to-browser/RATIFICATION-2026-09-10.md (the outgoing seat's, 4,332 B — unread by this seat until now; the seat's own same-named file was renamed RATIFICATION-2026-09-10-architect.md to end the name collision) · the operator's challenge 2026-09-11: this seat only adds, never deletes -->

- **AX11-1 · Ratification #7 honoured — AX3-1 amended:** committing lanes run LOCAL **overnight only**; during working hours a committing lane waits for the night (or for conductor E). Today's daytime local lanes and integrator suites breached #7; recorded, not repeated.
- **AX11-2 · Ratification #5 honoured:** the operator never types a path and the browser never composes a boot line. CC copies the current bundle's `SEAT-BOOT-*.md` renders to the transport's `to-browser/`, replacing the stale batch-V copies; a new seat is booted by pasting that file's content. The browser names only the file.
- **AX11-3 · Cleanup is an act, not a note.** From the domain census (248 items: 197 LIVE, 24 UNTRIGGERED, 10 UNREAD, 1 GARBAGE-CANDIDATE, 16 UNKNOWN): the 35 non-live items get a proposal each — DELETE (git keeps history) · TRIGGER (named hook/gate/schedule) · KEEP with a one-line reason — delivered as one file for one operator GO; the 16 UNKNOWN are resolved by a second pass, not left. Deletions execute in one lane after the GO.
- **AX11-4 · Net rows reported honestly:** this window files more rows than it closes; the batch W close packet reports the overdraft and the evidenced closures (AX10-1) that offset it.

=== END OF AMEND ===

<!-- CARRIED END: AMEND-BATCH-X-ROSTER-011.md -->

<!-- LANE-ADDED BEGIN: supersession map -->
## Part 12 · Supersession map (lane's own addition, beside the carried text)

Every entry below points at carried text that a later carried file governs. **Nothing in Parts 1-11 was edited to produce this map** -- it is the marker, and the superseded wording stays where it was written.

### From AMEND-001 (the freezing amendment)

- **Part 1 §2, the X1 lane ORDER is superseded by AX1-1.** The roster's table runs X1-1 decision_coverage, X1-2 merge cost, X1-3 conductor E, X1-4 routing, X1-5 spine, X1-6 keys. AX1-1 reorders to X1-1 decision_coverage · **X1-2 conductor E** · **X1-3 merge cost** · X1-4 routing · X1-5 spine · X1-6 keys. The lane labels in Part 1's table are therefore stale for X1-2 and X1-3 and the AMEND's order governs. Reason carried in AX1-1: landing the merge-cost lane first spends it optimising the integration path conductor E replaces, and makes `[#675]`'s before/after incomparable across the substrate boundary.
- **Part 1 §2 X1-1's Done-when is extended by AX1-2.** `implements:` accepts only identifiers that RESOLVE -- an ADR number present in `docs/decisions/`, an intake number present in `docs/intake/`, a transport decision filename that exists; free text is refused. The RED-first fixture is this window's own backlog.
- **Part 1 §2, the merge-cost lane's Done-when is extended by AX1-3**, clauses (a) the full suite runs once at batch END and a RED full suite is a batch-level HALT, (b) the receipt splits minutes-to-merge into test time and ceremony time, (c) `backlog-filing-backpressure` stops refusing merge commits. AX1-3 also adds a PRECONDITION before dispatch: W-7's owed MED is fixed -- an empty selection FAILS closed (runs everything), never passes as "nothing impacted".
- **Part 1 §4 gains a row from AX1-4:** NEW `propose_closures` writes ONE file overwritten per run (LEDGER D5), paired with X2-1.
- **Part 1 §4's A8 (doc congruence) is superseded by AX1-5** -- it is no longer a row of its own; it moves into X2-4 as a clause, one traversal producing two reports.
- **Part 1 §5 gains an entry from AX1-6:** the PowerShell dispatch retirement act (`DECLARE-DISPATCH-RETIREMENT`) is **batch Y**, unblocked by conductor E; it is a written deferral, not a row.
- **Part 1 §0 gains one sentence from AX1-7:** X makes the night safe and ships nothing to a consumer -- bytes to corp-monorepo stay zero until the v1.5.0 tag and `[#670]`.
- **Recorded by AX1-8, and it closes nothing:** C4 model-agnosticism is NOT closed by the routing lane (routing is not agnosticism); aliases, the unified contract, the `MODEL_ENUM` source and churn insulation stay with `[#568]` / `[#582]` in batch Y.

### From AMEND-002

- **Part 1 §2 X1-6's premise is corrected by AX2-1.** The roster's X1-6 rests on A7-1 reading W-3's output as the `skipped_gates` writer. W-3 produced a per-guard IDENTITY (`Guard.key = module::target`), not a writer callable, so **X1-6 builds the writer itself** and W-3 is a dependency, not the writer. A7-1's other three keys are unchanged.
- **Recorded by AX2-2, and it is not a defect:** thirteen guards in `tests/test_review_artifact_coverage.py` still carry `requires_git`; they are individually dispositionable, which is what `[#638]` asked, and the module is not unskippable.

### From AMEND-006

- **AX6-1 is a LANE, not a row of this intake.** Lane X-C "domain census" was dispatched in parallel with batch W integration (branch `worktree-lane-x-000-domain-census`) and writes one artifact, `docs/audits/2026-09-11-technical-domain-census.md`. This lane filed **no row** for it: a dispatched lane with a named output is not an unscheduled decision, and a row would duplicate it.
- **AX6-2 adds seven domains to the MANAGEMENT MAP's row set** -- ecosystem · logs · protocols/docs · visualization · scripts · templates · tasks, one per folder-domain with the owner-process named or DEAD. **These are rows of the rendered map, not `tasks/` rows**, because AX5-2 defines the management map as one page rendered from `ecosystem/organ-index.md` and never hand-maintained -- so its "rows" are table rows in a generated artifact. This lane filed **no task row** for AX6-2. It is a clause extending the management-map row, **and that row lives in AMEND-005, which this file does not carry** (Part 6). The clause is owed to the management-map row whenever AMEND-005 lands.
- **AX6-3 is a NEW row** (visualization) and is filed by this lane.
- **AX6-4 is a NEW row** (the operator packet gains D14, folder-as-domain) and is filed by this lane. Its own text sequences it: decided AFTER lane X-C's census, with the per-folder verdicts as input, and the seat recommends no rename before the census.
- **AX6-5 is a NEW row** (W-4 close residue) and is filed by this lane **as a row, not as work**. AX6-5 says so in its own words -- "updated at batch close as a row" -- and the acts it names (regenerate the organ index 64 -> 63, fix `CLAUDE.md:138`, re-derive the ship-gate WARN delta, supersede the `ORPHAN_DISPOSITIONS` `/override` line per AW6-1) are the integrator's at batch close. This lane is TEXT-ONLY and regenerated no index.

### From AMEND-007

- **AX7-1 supersedes X1-1's scope: it becomes the DECISION ENGINE, and it is NOT a new row.** Two halves in one lane -- BIRTH (the intake template carries the thesis scenario, closed questions, alternatives with benefits and trade-offs and a flip condition; `gen_adr.py` renders the decision table and the sensitivity re-run into the ADR; the ADR gate refuses an ADR missing a field) and EXECUTION (`decision_coverage` and `implements:` as in AX1-2 / AX4-1). Library-first is named in the amendment: MADR as the template shape plus the three thesis fields MADR lacks.
- **AX7-1 ABSORBS `[#616]` (flip condition in 91 ADRs) and `[#242]` (ADR status transitions), and this lane filed NO new rows for them.** Both are EXISTING ids listed in Part 1 section 4, and the roster's own rule is that a NEW: clause against an existing row is not a new row. The absorption is recorded HERE, which is where a future lane reads it; the two rows are not renumbered, not edited and not closed by this lane -- closing them is the engine lane's act once the engine subsumes them.
- **AX7-2 re-orders X1 again, superseding AX1-1's order AND AMEND-003's AX3-3.** X1 is now: decision engine · conductor E · merge cost · routing+telemetry · spine `[#664]` · `[#687]` keys, with the docs cut moved to the HEAD of X2. The operator's reason is carried: naming and structure are the last aspect, decisions first. Note this supersedes an ordering set by AMEND-003, which this file does not carry -- so the ordering here is current and its immediate predecessor is not visible in this file (Part 9).
- **AX7-3 makes the path registry row X2 and NOT conditional**, superseding AX5-3's conditional filing (AMEND-005, uncarried). Its evidence is three measured instances in one day, and AX7-3 states that **each is a row (FILE) with a RED-first test** -- filed here as `[#718]`, `[#717]`, `[#716]`. The path row itself is `[#715]`. **`[#716]` carries AX7-3's standing consequence: the step-0 sync stays MANDATORY until `worktree.baseRef` is fixed.**
- **AX7-4 is a NEW row** (`[#719]`): `ecosystem/organ-index` entries validated against Backstage `catalog-model`'s Component JSON schema by our own gate, with no Backstage runtime, and the portal revisited only if lane X-C's census shows a scale that needs browsing.
- **AX7-5 is RECORDED and is not a row.** `config/` and `plugins/` were missing from AX6-1's folder list and were added to lane X-C at dispatch; "cheapest admitted" resolves to **sonnet** because haiku carries no admission row in `ecosystem/provider-registry.yaml` -- a clause on the routing lane rather than a row of its own; and `-Model` must be explicit until `[#717]` lands.

### From AMEND-008

- **AX8-1 is an INTERIM routing rule with an expiry written into it**, filed as `[#708]`: effective when W-2 is on `main`, every read-only digest, census or scan defaults to `agy` (stdout-only, serialised at most 1, with CC verifying every locator), and Claude is used only when agy refuses or the task commits, with model and tokens recorded per run in the receipt. **X1-4 routing REPLACES this interim rule with the registry** -- so the row is written to be retired by the routing lane rather than to persist.
- **AX8-2 is a NEW row** (`[#709]`): a scheduled log-review routine -- daily, and every three days until conductor E is live -- on the cheapest admitted model, reading logs and telemetry and flagging a model that does not deliver, a stuck or zero-work lane, a cost spike, and a gate firing on empty; it writes one digest and FILES each anomaly as a row. It depends on C2 telemetry (`[#694]`) and on the B7 nightly routine (`[#702]`), and AX3-4 folds it with the logs lane.
- **AX8-3 is TWO rows, because its own text says so.** `[#710]` is the test-baseline debt: the 26 permanently RED tests on the Windows baseline each fixed or dispositioned with a reason, because a baseline that stays red hides new failures. `[#711]` is the xdist frozenset-identity pollution in `test_manifest_link_route`, which AX8-3 explicitly directs to be filed "as its own row". AX8-3 also names the shape of test management: B1 impacted selection, B2 refusal without a test, B3 one full suite per batch, and this row.
- **AX8-4 is a CLAUSE and this lane filed no row for it.** Templates are floor components -- the new-project starter -- covered by lane X-C's census of `templates/`, declared MUST under AX4-1, and rendered from the same source as the docs after the cut. **The row it is a clause OF does not exist in this file**: AX4-1's `floor: MUST | hub-only` declaration lives in AMEND-004, which is not carried (Part 13). The clause is recorded here and is owed to the floor-declaration row whenever AMEND-004 lands. This is the same shape as AX6-2 over AX5-2.
- **AX8-5 is a NEW row** (`[#712]`), FILE and RED-first: a session whose worktree was torn down silently resolves to the PRIMARY checkout, so a write from it lands on the integrator's branch. Teardown must end or refuse sessions on that worktree, and the Stop hook must detect cwd-not-a-worktree and refuse writes. Witnessed on the dispatcher session, 2026-09-11.

### From AMEND-009

- **AX9-1 is a NEW row** (`[#727]`): a `PreToolUse` deny-and-point hook on `Bash` / `Grep`, where a raw search over a GOVERNED question is denied with exception text naming the organ to run instead. **Its stated precondition was discharged by this lane rather than deferred** -- AX9-1 asks CC to verify on this version that a PreToolUse deny on Bash actually blocks, because an upstream report said otherwise. It does: this lane's own session was denied Bash calls several times by the worktree-isolation `PreToolUse` guard, each with a refusal message that reached the model and stopped the call. The fallback to `UserPromptSubmit` / skill hooks is therefore NOT needed on this version, and the row records the evidence.
- **AX9-2 is a NEW row** (`[#728]`): every organ in `ecosystem/organ-index.md` that answers a question gets a SKILL whose description states WHEN to invoke it, rendered from the index and never hand-written -- because progressive disclosure means the description is what the model matches. AX9-2 names it as `[#617]`'s simplest form and first deliverable.
- **AX9-3 is a NEW row** (`[#729]`): a minimal stdio MCP server exposing FPG-1's `why`, `process-list` and `stats` plus the test selector, so the queries sit in the model's tool list beside Grep and Codex/agy can reach the same server. **No new query logic** -- the server calls the existing scripts, which is what keeps it library-first rather than a second implementation.
- **AX9-4 is a CLAUSE and no row was filed for it.** Exists-before-build: a contract CREATING an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need, and a NEW organ without that quote is refused at the contract gate. It is a clause on the DECISION ENGINE (AX7-1, which is X1-1's scope rather than a row -- carried in Part 5) and on the FLOOR DECLARATION (AX4-1, in the uncarried AMEND-004). Neither is a filed row in this intake, so the clause is recorded here and owed to both.
- **AX9-5 is a CLAUSE on the telemetry row and was folded INTO `[#694]` rather than filed separately**, since that row is this lane's own and unlanded: raw-search calls versus organ calls per session, and organs never called in 30 days, with the log-review routine (`[#709]`) flagging regressions. It is the one number that says whether the model uses the harness or rebuilds it.

### From AMEND-PATH-REGISTRY-001, over the QUESTION it corrects

Parts 6 and 7 are the intake body of `[#715]`, and **Part 7 governs Part 6 where they differ.** The difference is not a detail -- it is the QUESTION's central claim:
- **APR-1 withdraws the QUESTION's Option A as a NEW BUILD.** The QUESTION's recommendation reads "registry file + one resolver per language + literal-path gate"; APR-1 rules that **the registry the operator describes already exists -- it is FPG-1** (path · purpose · trigger · edges · query). Option A becomes "FPG-1 completed": a `writes` edge / artifact column (`[#664]` step D), last-touched read from git at query time and never stored twice, and FPG-1 wired as the spine so it is CALLED rather than re-read. **No second graph.** `[#715]` is written so it cannot be read as a new registry.
- **APR-2 narrows what is actually new to ROOTS AS CONFIGURATION** -- one declaration (transport root, worktree base, prompts dir, outputs) read by FPG-1's Python loaders AND by the PowerShell verbs, with a literal-path lint refusing a governed root written inline. Library-first: `platformdirs` for OS-standard directories, git for history, nothing hand-rolled beyond the declaration.
- **APR-4 re-files three inbox-009 candidates as CLAUSES of `[#715]`, not as registries**: derived-copies becomes an FPG-1 edge kind, freshness becomes a query over last-touched, and per-consumer becomes the same graph per repo root joined by the floor manifest. **No separate rows were filed for them**, which is APR-4's explicit instruction.
- **APR-5 sets the decision route, and it is why `[#715]` lands OPEN.** The QUESTION and this amendment are the intake BODY; the decision is made by the engine (AX7-1) with the thesis table. The browser proposes, it does not rule -- so `[#715]`'s disposition says OPEN rather than carrying the QUESTION's recommendation as though it were decided.
- **Recorded, not a defect:** `QUESTION-path-registry-2026-09-11.md` carries **no** `carried-by:` line, unlike every other file carried here. It routes to this intake through AX7-3 and through its own sentence "lands as an intake via X-0's row" rather than through a transport header, so its carriage is declared in prose instead of in metadata. Carried on that basis.

### From AMEND-010

- **Part 1 §4 and the X2 backlog lane are extended by AX10-2**, two clauses: narration RELOCATES to `tasks/archive/` on a trigger (each batch close) rather than by hand, and the closure budget "close before filing" becomes ENFORCED -- a batch that files more rows than it closes reports the OVERDRAFT in its close packet. The host is `[#589]` plus `archive_row_body.py`, both of which exist and predate this lane, so the clauses are filed as `[#731]` rather than edited into `[#589]`: this lane does not edit rows it did not file. `[#731]` names `[#589]` as its fold target.
- **AX10-1 is NEW, not a supersession**, and it is worth separating from the closure-detector rows it sits beside. `[#277]`, `[#487]` and `[#693]` are all about repairing the DETECTOR -- a machine proposing closures from its own signal. AX10-1 is a different act on a different evidence base: the CLOSE PACKET lists rows whose Done-when the batch's own MERGES witnessed, each with the merged SHA and the test or gate that proves it, and asks for ONE operator word. A row with no witness is not listed. Filed as `[#730]`.
- **AX10-3 (`Floor: MUST`) has no host row in this repo** and is recorded rather than filed, the same disposition AX8-4 and AX9-4 received: the floor-declaration row lives in AX4-1, inside the uncarried AMEND-004 (Part 13). It is carried as a clause INSIDE `[#731]` so that it is reachable, and owed to the floor row when that row exists.

### From AMEND-011

- **AX3-1 is AMENDED by AX11-1, and the amended text is NOT carried here.** AX3-1 lives in AMEND-003, which no instruction has ever named (Part 13). So this file carries the amendment without its target: committing lanes run LOCAL **overnight only**, and during working hours a committing lane waits for the night or for conductor E. Filed as `[#732]` with the rule stated in full, precisely because the text it amends is absent -- a reader of this intake alone would otherwise see a correction to nothing.
- **AX11-1 records a breach by the seat that carried it, and this lane is inside that breach.** Its own words: *"Today's daytime local lanes and integrator suites breached #7; recorded, not repeated."* This lane is a committing local lane that ran through 2026-09-11 daytime, so it is one of the lanes named. It is recorded here rather than argued: the ratification is the operator's, the breach is today's, and the amendment itself scopes the exemption to today.
- **AX11-2 does not supersede `[#698]`; it sits beside it.** `[#698]` is a CARDINALITY defect in the SEAT-BOOT-integrator render (a GO per merge where the canon grants one per batch). AX11-2 is about DELIVERY -- the renders are copied to the transport's `to-browser/`, replacing the stale batch-V copies, so the operator never types a path and the browser names only a file. Same artifact, different failure. Filed as `[#733]`.
- **AX11-3 does not supersede `[#706]`.** `[#706]` is a packet-CONTENT decision (D14, folder-as-domain) that cannot be made before the census returns. AX11-3 is what happens AFTER it returns: each of the 35 non-live items gets a DELETE / TRIGGER / KEEP proposal, delivered as one file for one operator GO, with the 16 UNKNOWN resolved by a second pass rather than left. Filed as `[#734]`.
- **AX11-4 is an obligation on a close packet this lane does not write.** It directs the BATCH W close packet to report the window's net-row overdraft alongside AX10-1's evidenced closures. Batch W's packet is the integrator's artifact, so no row is filed for it here; the enforcement half of the same idea is `[#731]`'s overdraft clause, and this is owed to the integrator.
<!-- LANE-ADDED END -->

<!-- LANE-ADDED BEGIN: not carried -->
## Part 13 · What this file does NOT carry (lane's own addition)

**`AMEND-BATCH-X-ROSTER-003`, `-004` and `-005` exist on the operator's transport and are NOT carried here.** They are recorded rather than folded, because folding them would be a deviation the lane is not authorised to make -- and leaving them unnamed would make this file a carrier that silently drops payloads which name it as their carrier. All three carry `carried-by: docs/intake/2026-09-11-tech-batch-x-roster.md` -- **this file**.

```
12:43  DECLARE-BATCH-X-ROSTER-2026-09-11   carried, Part 1
13:00  AMEND-001  (roster FROZEN)          carried, Part 2
13:13  AMEND-002                           carried, Part 3
13:24  lane contract created
13:26  AMEND-003                           NOT carried
13:26  lane contract last written          (37s after AMEND-003)
13:29  AMEND-004                           NOT carried
13:34  AMEND-005                           NOT carried
13:42  AMEND-006                           carried, Part 4 -- by operator
                                           instruction, after this file's
                                           first commit
14:05  AMEND-007                           carried, Part 5 -- second
                                           operator instruction
14:10  QUESTION-path-registry              carried, Part 6 ([#715] body)
14:16  AMEND-PATH-REGISTRY-001             carried, Part 7 (governs Part 6)
14:29  AMEND-008                           carried, Part 8 -- third
                                           operator instruction
14:36  AMEND-009                           carried, Part 9 -- fourth
                                           operator instruction
15:45  AMEND-010                           carried, Part 10 -- fifth
                                           operator instruction, AFTER
                                           this lane's close packet
15:49  AMEND-011                           carried, Part 11 -- same
                                           instruction
```

The lane's frozen contract names three sources and freezes the NEW-row set against them; four later operator instructions added AMEND-006, then AMEND-007 with the two path-registry files, then AMEND-008, then AMEND-009 -- each **by name** and each naming the rows wanted from it. None of the four instructions reaches 003, 004 or 005. What the uncarried three contain, stated so the next reader can size the gap without re-reading the transport:

- **AMEND-003** (self-review, four misses): the Codespace committing-lane ruling as a STANDING ruling rather than a workaround; conductor E ships to consumers as a floor component; the **docs cut moves into X1 replacing X1-6**, which moves to X2; a logs lane in X2; prompt distiller `[#617]` heads X2; token use recorded honestly.
- **AMEND-004** (the hub IS the floor): `floor: MUST | hub-only` mandatory on every row and lane contract, applied retroactively to batch W's outputs; model and cost declared per lane by `gen_lane_contract.py`; docs are floor components; four read-only facts owed before X1 dispatches.
- **AMEND-005** (management map): telemetry moves from X3 into X1 as a clause of the routing lane (AX5-1); a NEW **management map** row in X2 (AX5-2); a path-registry fact owed, with a NEW row conditional on the answer (AX5-3).

### The dangling references the carried amendments hold, named precisely

Part 4 is carried verbatim and therefore carries its own unresolved dependencies into this file. A reader who follows them lands nowhere, so they are named here rather than discovered:

1. **AX6-2 says "Management map (AX5-2) gains rows".** AX5-2 is in AMEND-005 and is not carried, so the management map this file references **is defined nowhere in this file**. AX6-2's seven folder-domains are an extension of a specification that has not landed.
2. **AX6-3 says the charts render "from the same telemetry the tally feeds (AX5-1)".** AX5-1 is in AMEND-005 and is not carried. The filed visualization row therefore names its telemetry source as the roster's own X2-6 trigger-or-remove row, which IS carried and IS filed, and records the AX5-1 reference as owed.
3. **AX7-1 cites AX4-1**, whose `floor: MUST | hub-only` declaration is in AMEND-004 and is not carried. The decision engine's EXECUTION half is specified as "`decision_coverage` and `implements:` as in AX1-2 / AX4-1" -- AX1-2 IS carried (Part 2), AX4-1 is not, so half that specification resolves here and half does not.
4. **AX7-2 supersedes an ordering that AMEND-003 set** (AX3-3 moved the docs cut INTO X1; AX7-2 moves it to the head of X2). The current ordering is carried and correct; its immediate predecessor is not in this file, so a reader diffing the orderings sees AX1-1 then AX7-2 with a step missing between them.
5. **AX7-3 supersedes AX5-3's CONDITIONAL filing of the path row.** AMEND-005 filed it conditional on a fact being answered; AX7-3 makes it unconditional and X2. Only the unconditional form is carried, which is the operative one -- recorded so the change is not read as the original state.
6. **AX8-4 makes templates a floor component "declared MUST under AX4-1"** -- and AX4-1 is in AMEND-004 and is not carried, so the row AX8-4 is a clause of does not exist in this file. Recorded as owed; no row filed. Same shape as AX6-2 over AX5-2.
7. **AX8-2 folds the log-review routine "with the logs lane (AX3-4)"** -- AX3-4 is in AMEND-003 and is not carried, so the lane it folds INTO is not defined here. `[#709]` is filed on AX8-2's own terms, and the fold is recorded as owed.
8. **AX9-4 is a clause on TWO things, one of which is uncarried.** The decision engine (AX7-1) IS carried, in Part 5; the floor declaration (AX4-1) is in AMEND-004 and is not. So half of AX9-4's attachment resolves in this file and half does not -- the same split AX7-1 itself has.
9. **AX10-3 (`Floor: MUST`) attaches to the same missing AX4-1** -- the third clause in this file to do so, after AX8-4 and AX9-4. Three separate amendments now point at one uncarried row, which is itself the argument for landing AMEND-004: the cost of not carrying it is no longer a single dangling clause but a pattern.
10. **AX11-1 AMENDS AX3-1, which is in AMEND-003 and is not carried** -- so this file holds an amendment whose TARGET is absent, the inverse of the usual shape. The rule is therefore written out in full in `[#732]` rather than as a delta, because a delta against absent text is unreadable.

**What this does and does not change about the rows filed under this intake.** Every row the frozen roster marks NEW still exists under 003-005 -- those amendments re-assign WAVES and add FURTHER rows; they retire none of the rows filed here. Wave assignment is not this intake's surface. So the filed set is correct and incomplete rather than wrong, and the delta is additive: the docs-cut row, the management-map row, the conditional path-registry row, the `floor:` declaration clause (now pointed at by THREE amendments) and the per-lane model/cost clause are **owed to a follow-up act**, not silently lost.

Landing them is a decision for the operator or the next architect seat, not for this lane: carrying them would have changed a NEW-row enumeration that the lane's contract froze **specifically so the lane could not over-file by judgment**. The operator's AMEND-006 instruction is the precedent for how they land when they land -- named explicitly, with the rows wanted from them named too.
<!-- LANE-ADDED END -->

<!-- LANE-ADDED BEGIN: close packet -->
## Part 14 · This lane's close packet (lane's own addition)

The filing lane's end-of-lane artifact -- what changed, every row id it minted and what each is for, the folds it made and declined, its declared deviations and the acts it leaves owed to the integrator -- is `docs/audits/2026-09-11-technical-x0-batch-x-roster-close-packet.md`. Read it beside this file: this file is WHAT was carried, and that one is WHY the filed set looks the way it does.
<!-- LANE-ADDED END -->

=== END ===
