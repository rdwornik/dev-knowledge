---
intake-id: 27
status: DRAFT
origin: "2026-08-06 operator-directed retrospective + tech-adoption audit, browser seat of the sealed 2026-08-05/06 window; consolidates and SUPERSEDES-as-ledger the adoption-status view of intake #24 (tech-currency wave 1) and intake #25 (simplification & distribution wave); landed verbatim by operator instruction"
note: "Parents: intake #24 · intake #25 · ADR (parallel-execution way-of-working, successor Phase 2). Landed VERBATIM by operator instruction (ARC-2 S-batch contract 1) — body unedited. The source frontmatter carried an off-schema `parents:` key (README §3 schema); its value is preserved here as prose rather than dropped. ERRATUM 2026-08-06 (architect-ruled, batch-1 night audit): the verbatim body carried two references to a section §D that this document does not contain — its sections are §A/§B/§C/§F. Both pointed at the four NEW EVAL candidates, which live in §A as items 33–36 (`pytest-xdist`, `jsonc-parser`, `check-jsonschema`, `mise`) and which §F already names by that number range. Repaired in place to `§A items 33–36` (WHY line) and `§A item 35` (row 18, check-jsonschema reshaping W-6) — a locator repair only; no status, priority class, evidence or item text changed, and no §D/§E section was created. This is the ONLY departure from verbatim. ERRATUM 2026-08-08 (morning integrate-and-cut arc, operator-directed): while `status: DRAFT` this ledger is editable — the same standing the 2026-08-06 §D repair above relied on — and four ledger-truth edits landed. (1) SPENT PEG: rows 13/14/15/16/21/24 all read `DEFERRED(batch 2 …)`, but batch 2 ran and closed with ZERO W-items, so those six statuses were locators pointing at a finished event; re-pegged to `DEFERRED(W-wave batch — after intake #25 acceptance + births)`, each row's own recorded collision/hazard qualifier preserved verbatim. (2) §9 of `docs/audits/2026-08-08-technical-library-research.md` applied — two ADDITIONS as new §A rows 37 (`Closes:` git trailer) and 40 (`sys.path` substrate / pytest `pythonpath`), and two AMENDMENTS landing in the shapes the memo proposed rather than as rows: item 38 folded into §A item 35, item 39 into the Sequencing note as an explicitly unratified proposal. (3) ANNOTATIONS: item 34 carries a maintenance flag (jsonc-parser cold since v3.3.1, 2024-06, plus the npm-runtime cost) and item 36 carries the recurrence evidence (THREE organs silenced by the uv pin, the third an unbidden fail-open Stop hook) with the memo's divergence question quoted. NO status, priority class or item text was changed except as listed; ZERO BACKLOG rows born, zero closed, no §A row removed, and the 38/39 numbering gap is documented in §A rather than left silent. ERRATUM 2026-08-09 (ARC-1 consolidation hygiene): two §A rows had gone FALSE against live state and were amended on measurement, under the same `status: DRAFT` editability the two errata above relied on. (1) ROW 33 (`pytest-xdist`) read `NEW EVAL candidate` targeting `410s` while the tool is ADOPTED AND HOLDING — `addopts = \"-n auto\"` landed at d11dda35, authorized in ADR-110's decision table, eval record STANDING_RULINGS E1; both of the cell's premises were dead, since the measured serial baseline is 1785.61s (never 410s) and the suite is 2716 passing (never 2362). Amended to ADOPTED with the adoption measurement (serial 1785.61s vs -n auto 358.77s/330.15s, ~5.2x) and the live wall clock (539.12s) cited inline; the class column is marked P-B SPENT because an adopted tool cannot be the P-B item a gap-week consumes. The as-landed cell text is quoted inside the amended cell rather than deleted. (2) ROW 36 (`mise`) carried a P-B gap-week class while the uv-pin class recurred a FOURTH time, fleet-wide: on 2026-08-09 all five night lanes ran with NO executable gate mesh (uv 0.8.17 against the ADR-106 ==0.11.19 pin; .git/hooks/ samples only), which is why those five reports had to be re-verified locally after the fact. The class change (gap-week eval -> cloud-channel precondition) is recorded as PROPOSED, NOT RULED — no operator ruling covers it — and the row's own honest counter (mise would not have fixed that night, because the missing thing was a specific uv version) is explicitly preserved as unanswered. NO other row, status, priority class or item text changed; ZERO BACKLOG rows born, zero closed, no row removed. Sec C's P-B enumeration is left standing as the as-landed record with a dated parenthetical noting 33 is spent and 36 is proposed-only — the same shape the WHY paragraph's counts use."
---

# INTAKE DRAFT — tech-adoption consolidation ledger (38 items, successor-facing)

## WHY — what this intake is and is not

The fleet decides fast and executes through one serial channel; ~21 of the 36 tracked adoption items are IN-FLIGHT behind that channel. This intake is the **single durable ledger** of all 36 so the vision cannot be lost between windows — every item has a status, an owner-or-gap, and a recommended priority class. It is **not** a new proposal wave: it births at most the four NEW EVAL rows (§A items 33–36); everything else already has a home and this document only makes the queue visible and sequenceable. Rulings referenced here are settled — this intake carries them, it does not reopen them.

> _(The two counts in the paragraph above are the ledger **as landed 2026-08-06** and are left standing as that record. The ledger is **38 items** as of 2026-08-08 — rows 37 and 40 were added by the erratum in this file's frontmatter; the in-flight count was not re-measured, because neither new row is in flight. Birth accounting is unchanged: still at most four, still zero assigned.)_

## §A — Ledger (status vocabulary: ADOPTED-live / EVAL-RUN(result) / SCHEDULED(where) / UNPLACED / REFUTED / DEFERRED(trigger) / DORMANT)

| # | Item | Status | Evidence / locator | Priority class (§C) |
|---|---|---|---|---|
| 1 | Gemini CLI lane [#491] | SCHEDULED(batch-2 grooming) | supplement C3(a) | P-A |
| 2 | Grok lane [#492] | SCHEDULED(peg ≥2026-08-07; seeded-defect list unwritten) | supplement C3(b) | P-A |
| 3 | Copilot Free as Grok channel | DEFERRED(opens with #2) | intake #24 P6 | P-A |
| 4 | sol/terra/luna routing table | ADOPTED-live | R-6 ruling; terra owed on [#504] | — |
| 5 | Actions report-only recorder [#501] | SCHEDULED(batch 1) | row e7c0b70e; YAML in night packs c55c7e51 | P-A |
| 6 | Scheduled runs + dead-man ([#493], P2 folded) | DEFERRED(no date) — B-2 still silent | FR-3 fold ruling | P-C |
| 7 | gh findings-as-Issues (P3) | UNPLACED(reshaped: batch-per-run) | night finding 5 (rate limits, ~150→403) | P-C |
| 8 | mutmut [#502] | EVAL-RUN(pass) + SCHEDULED(behind [#501], CI-only) | night research; B2→B1 dependency edge | P-A |
| 9 | CONTRIBUTING currency [#503] | SCHEDULED(batch 1, ×6 claims + DoD + override.md) | Lane D + night finding 7 | P-A |
| 10 | vale (P6) | REFUTED | commit 5125dd6 + JOURNAL (b) 616f4814 | — |
| 11 | commitlint / gitlint (P6) | EVAL-RUN(LEAVE) | night packs 81cf13b | — |
| 12 | lychee (P6) | EVAL-RUN(ADOPT-candidate, --include-fragments) | night packs 81cf13b | P-B |
| 13 | copier living-template (W-1) | DEFERRED(W-wave batch — after intake #25 acceptance + births) | R-i pre-naming | P-A |
| 14 | kernel/lab check tiering (W-2) | DEFERRED(W-wave batch — after intake #25 acceptance + births; pyproject collision recorded) | Lane C ledger | P-A |
| 15 | pre-commit native distribution (W-3) | DEFERRED(W-wave batch — after intake #25 acceptance + births; reconcile [#497] @ carrier_mesh.py:75 FIRST) | mega-packet collision | P-A |
| 16 | reusable kernel.yml (W-4) | DEFERRED(W-wave batch — after intake #25 acceptance + births; .github/workflows/ single-owner = [#501]) | Lane C ledger | P-A |
| 17 | pytest-testmon (W-5) | SCHEDULED(batch-2 ledger per rider R-ii; targets 410s/run) | supplement rider R-ii | P-A |
| 18 | schema-as-code (W-6) | DEFERRED(floats behind W-5) — reshaped by §A item 35 | rider R-ii | P-B |
| 19 | sphinx-needs study (W-7) | UNPLACED | intake #25 heading only | P-D |
| 20 | local-vs-reference matrix (W-8) | UNPLACED(intake prose) — candidate for a one-line register ruling | intake #25 W-8 | P-B |
| 21 | AGENTS.md + thin shim (W-9a) | DEFERRED(W-wave batch — after intake #25 acceptance + births) + HAZARD: collides with existing codex/AGENTS.md | mega-packet hazard | P-A |
| 22 | VISION→README (W-9b) | UNPLACED (S, gap-week) | — | P-B |
| 23 | .claude/skills ↔ .agents/skills symlink (W-9d) | UNPLACED (S, gap-week) | — | P-B |
| 24 | routing-table-as-config (W-10) | DEFERRED(W-wave batch — after intake #25 acceptance + births) | intake #25 | P-A |
| 25 | standing-rulings register (V-2) | ADOPTED-live (applied silently; 4 lessons + B2 label land in successor Phase 2) | protocols/STANDING_RULINGS.md, 90351bd0 | — |
| 26 | risk-tiered ceremony + plan-mode-by-exception (V-3) | ADOPTED-live | templates/prompt-template.md v1.6, 12dbb65a; precedence repair adf85c4a | — |
| 27 | first V-1 worktree batch | GO-GIVEN, runs as successor Phase 4 | predecessor approve + plan §2 | P-A |
| 28 | worktree hygiene prune (V-5) | SCHEDULED(mechanized in [#429] slim, successor Phase 3) | plan §2 P3 | P-A |
| 29 | seal velocity metrics (V-6) | PARTIAL(qualitative only; hard numbers = batch-1 packet) | retro RS-3 | P-A |
| 30 | [#408] three-layer sync spec | DESIGN-LANDED(c55c7e51, fingerprint trigger); build = OWN ARC, unplaced | row pointer per rider R-iii | P-C |
| 31 | Fibonacci estimate binding | UNPLACED ([#488] scope; backlog still has no ranking function) | audit row 31 | P-D |
| 32 | R1–R4 retirement ranking | DORMANT since [#487] engine refutation | 2026-08-06 grooming used live-peg evidence instead | P-D |
| 33 | **pytest-xdist** (`-n auto`) | **ADOPTED AND HOLDING — amended 2026-08-09** (as landed, this cell read *"NEW EVAL candidate — immediate 410s relief, orthogonal to W-5"*). Not a candidate: `addopts = "-n auto"` landed at `d11dda35`, is authorized in ADR-110's decision table, and its eval record is `protocols/STANDING_RULINGS.md` E1. **Both premises in the as-landed text are dead** — "410s" was never the serial baseline (the measured one is **1785.61s**), and "2362 tests" has moved to 2716 passing. The gap-week slot this row reserved is spent | Adoption measurement (`pyproject.toml` comment block): serial **1785.61s** → `-n auto` **358.77s** / **330.15s**, ~5.2×, identical pass/fail/skip across all three runs. Live full-suite wall clock on merged main: **539.12s (0:08:59)** for `1 failed, 2716 passed, 3 skipped, 1 xfailed` — `docs/audits/2026-08-08-technical-batch-3-packet.md:46`, re-measured `docs/audits/2026-08-09-technical-night-n3-performance-instrumentation.md:94`. The stale-410s class was already named for row 17 in `docs/audits/2026-08-08-technical-successor-prep.md:61` ("the 410s premise moved") | P-B — **SPENT** (the eval landed; no gap-week slot remains to consume) |
| 34 | **jsonc-parser (Microsoft)** as merge engine | NEW EVAL candidate — replaces hand-rolled JsoncMerge.ps1 (196 lines) — **MAINTENANCE FLAG 2026-08-08: cold, not abandoned.** Latest release v3.3.1, 24 June 2024; no 2025 or 2026 releases. A stable parser for a frozen format can legitimately sit still, but the row's premise is *replacing a bug source*, and swapping a maintained-by-us one for a two-years-quiet dependency is a trade, not a win. Second friction, fleet-shaped rather than package-shaped: it is an **npm** package, so adopting it means a Node runtime in the win-tooling lane | 2 latent bugs bit in one week (win-tooling lane); maintenance flag + npm-runtime cost measured in `docs/audits/2026-08-08-technical-library-research.md` §8a | P-B |
| 35 | **check-jsonschema** (pre-commit hook) | NEW EVAL candidate — reshapes W-6 from build to adopt — **AMENDED 2026-08-08 (memo §9 item 38):** the eval now has a **concrete first target that needs no build** — `.github/workflows/report-only-wall.yml`, born this window with `[#501]` — which `check-github-workflows` covers out of the box with no schema to author. Scope is **2 uncovered surfaces, not 3**: the six `deploy/manifest-v*.yaml` files and that workflow; `ecosystem/schema/` is pydantic (ADR-109) and validates itself, so the hook adds nothing there | W-6 stalled as a build; 0.37.4 released 2026-06-29, healthy by every signal checked — `docs/audits/2026-08-08-technical-library-research.md` §8b | P-B |
| 36 | **mise** (per-repo toolchain pinning) | NEW EVAL candidate — durable fix for the uv-pin class. **CLASS CHANGE PROPOSED, NOT RULED (2026-08-09): P-B gap-week eval → precondition for the cloud execution channel.** Proposed on recurrence count alone, and stated as a proposal because no operator ruling covers it: the class has now been witnessed **four times**, the fourth being fleet-wide rather than incidental. On 2026-08-09 **all five night lanes ran with no executable gate mesh at all** — uv `0.8.17` in the cloud container against the ADR-106 `required-version = "==0.11.19"` pin makes every `uv run --locked` hook entry refuse before doing any work, and `.git/hooks/` held only samples (JOURNAL 2026-08-09 (c); the five reports were merged and re-verified locally *after the fact* precisely because nothing verified them at authoring time). That is the reason for the proposed class change: a gap-week eval is something you do when there is slack, whereas this now sits upstream of whether the cloud channel can be trusted to gate its own output at all. **The row's own honest counter (below) still stands and is not answered by the recurrence** — mise would not have fixed that night either, because the missing thing was a specific uv version. Recurrence raises the priority of *answering the divergence question*; it does not answer it — **EVIDENCE ADDED 2026-08-08: the class recurred, and the count is THREE organs, not two.** In the night-cloud container `pyproject.toml` pins `required-version = "==0.11.19"` while the container shipped uv `0.8.17`, and `uv self update 0.11.19` returns *"version 0.11.19 was not found for the app uv"* — so every hook whose entry is `uv run --locked …` was unrunnable. Two were pre-commit hooks routed around by invoking their scripts directly; the third was the **`Stop` session-end backpressure hook, which fired unbidden at the boundary and failed open** — an unrunnable Stop hook is indistinguishable from a passing one to anyone reading the session. Divergence question, verbatim from the memo: *"would a `mise.toml` pinning uv `0.11.19` have produced a runnable gate mesh in a fresh cloud container tonight — i.e. can mise fetch a uv release that `uv self update` cannot?"* The honest counter the row should carry: **`mise` would not have fixed tonight** — the missing thing was a *specific uv version*, and a tool that manages uv still has to be able to fetch it | 3 organs silent from one cause; night fix ephemeral by design. Recurrence: `docs/audits/2026-08-08-technical-library-research.md` §8c; JOURNAL 2026-08-07 (o); STANDING_RULINGS D1 | P-B |
| 37 | **`Closes:` git trailer as the closure convention** | NEW EVAL candidate — git-native, zero deps, kills the `CLOSES_RE` false-positive class outright; the repo already writes git-parseable trailers (`kill-candidates:` on 7 of 52 first-parent commits), so the convention is present and only the closure key is missing. **The migration is the whole cost:** over `origin/main`'s 52 first-parent commits `CLOSES_RE` fires on 8 (7 ids) while `Closes:`/`Fixes:` trailers appear on ZERO, so a pure trailer matcher would lose 100% of the live signal | `git interpret-trailers --parse` over the exact false-positive merge `25ff8ec37` returns zero `Closes:` trailers; current matcher precision on its own firing set 7/8 — `docs/audits/2026-08-08-technical-library-research.md` §1 | P-B |
| 40 | **`sys.path` substrate — adopt pytest `pythonpath` (shape B)** | NEW EVAL candidate, **or fold into `[#502]`** — 100 `sys.path.insert` occurrences across 92 files, no `conftest.py`, and the class grew ~6× since its last measurement with no ruling. Shape B is one config block; shape A is ruled permitted-not-mandated (STANDING_RULINGS F5); shape C reverses `package = false` and needs an ADR. Three shapes costed, **no pick made** | `docs/audits/2026-08-08-technical-library-research.md` §5 (substrate measured live, same numbers as successor-prep §5.6) | P-B, escalating to an ADR only if shape C is chosen |

> **Numbering note (2026-08-08).** The memo's §9 proposed four items — 37, 38, 39, 40 — but two of
> them were proposed *as amendments rather than as rows*, and they landed that way: **38**
> (`check-jsonschema` first target) is folded into **item 35** above, and **39** (order `[#396]`
> before `[#512]`) is a register-shaped sequencing statement and landed in the **Sequencing note**
> at the foot of this file. The 38/39 gap in this table is therefore deliberate, not a dropped row.
> Applying all four births **zero** BACKLOG rows — §F's capacity law is untouched, and none of the
> four is assigned.

## §B — Do-not-relitigate carried (from #24, #25, and the sealed window)

vale-as-ratchet (refuted with citation) · commitlint/gitlint (LEAVE) · hand-rolled batch orchestration (native /batch exists) · web-UI-outside-VS-Code as primary surface · tmux/WSL · Copilot-gated Agents window · Backlog.md-as-engine (pattern donor only) · public repos for CI minutes · P2 as its own row (folded into [#493]) · name-match closes · equalizing work-lane vs epic-lane ceilings · agent-orchestration frameworks (LangGraph/CrewAI class — wrong layer) · standalone worktree managers (native + hygiene organ cover) · external SaaS dead-man services.

## §C — Priority classes (recommendation to the receiving architect; operator ratifies)

- **P-A — the batch-2 unlock class (~14 items):** everything queued behind the wide batch. No per-item decisions needed; the decision is *run batch 2 with [#490] inside* (retro RS-7). Items 13–16/21/24 additionally need the recorded collision reconciliations BEFORE births.
- **P-B — gap-week S-evals (~11 items):** cheap, independent, one sitting each (12, 18, 20, 22, 23, 33–36, and 37/40 added 2026-08-08). Recommended standing rule: every gap-week consumes ≥1 P-B item; measured-divergence bar applies — an eval that says NO (like vale) is a full success.
  _(**2026-08-09.** The enumeration above is the list **as landed** and is left standing as that record, per the same convention the WHY paragraph's counts use. Two of its members have since moved, and their §A rows carry the evidence: **33 is SPENT** — `pytest-xdist` is adopted, so it can no longer be the P-B item a gap-week consumes — and **36 has a class change PROPOSED** (gap-week eval → cloud-channel precondition), which is a proposal awaiting a ruling, not a re-class already made. Read against §A, the live consumable P-B set is ~10, not ~11.)_
- **P-C — own arcs (3):** [#493] dead-man (B-2 is still silent — the oldest unwatched failure mode in the fleet), [#408] build (design landed, do not let it rot), P3-reshaped Issues loop. Sequence after batch 2 proves the channel.
- **P-D — dormant, deliberate (4):** W-7, Fibonacci/[#488], R1–R4. Re-enter only via a named trigger, not ambition.

## §F — capacity honesty

This intake births **at most 4 rows** (items 33–36, and only if the receiving architect prefers rows over a standing gap-week rule; a register one-liner "gap-weeks consume P-B evals" would birth ZERO). Everything else is already owned. The close engine question does not arise — this is a ledger, not a wave.

**2026-08-08 addendum.** The ledger grew to **38 items** (33–36 plus 37 and 40; see the numbering note in §A) and the birth accounting is **unchanged at zero**: nothing here has been assigned, and the standing gap-week rule already landed as STANDING_RULINGS **E1** ("gap-weeks consume P-B evals"), which is the register one-liner this section names as the zero-birth path. The cap above governs *births*, not ledger width — a candidate recorded and unassigned costs nothing but the line it occupies.

## Sequencing note (not binding)

Batch 1 (P4) → batch 2 wide with [#490] (P-A unlock) → P-B evals fill gap-weeks throughout → P-C arcs after the channel is proven. The single risk this intake exists to prevent: the 36-item vision fragmenting back into chat memory. Its counter-mechanism is this file itself — versioned, statused, and small enough to re-read at every window boot.

**Added 2026-08-08 (memo §9 item 39) — one ordering statement, unratified.** Land **[#396] before
[#512]**. Neither row says so, and the order is not free: `[#512]` builds the `GIT_DIR` scrub, and
landing it first produces **five copies of one scrub** (four scrub sites are live today and
`batch_manifest.py:140` is a fifth with none), whereas landing `[#396]` first gives `[#512]` a
single place to call. Evidence: `docs/audits/2026-08-08-technical-library-research.md` §4.
**Status: proposal, not a ruling.** The memo proposed it as a one-line register entry;
`protocols/STANDING_RULINGS.md` carries rulings *ratified in chat*, and this one has not been —
so it is recorded here, in a note this file already labels *not binding*, rather than self-issued
into the register. Ratifying it is one line and is the operator's.

## Ratification amendment — 2026-08-08 (batch-3 GO)

Appended rather than folded: every section above stays exactly as written. These lines record what
the 2026-08-08 GO ratified against directives this file carries, so each ratification survives the
seat that took it.

- **Process-lane cap — denominator ratified (operator, 2026-08-08).** The 2026-08-06 process-lane
  cap (≤1/4 of a batch's lanes targeting methodology / hub-process surfaces) is evaluated against
  **dispatched width**; the end-of-batch packet reports the **close-width delta**. Doctrinal home:
  `protocols/PLAYBOOK.md` Ch8, "The batch protocol". ADR-110's routing-table row for the cap
  (§ "Amendment — 2026-08-06", the directive table) carries a matching amendment note rather than
  an in-place edit.
- **Sequencing statement `[#396]` before `[#512]` — RATIFIED (operator, 2026-08-08).** The
  "Added 2026-08-08 (memo §9 item 39)" paragraph in the Sequencing note above records this
  ordering under `Status: proposal, not a ruling`. That status line is superseded: the ordering
  was ratified at the batch-3 GO and now carries a register entry at
  `protocols/STANDING_RULINGS.md` **G1**. The paragraph itself is left as written (appended-to,
  not folded); the reasoning and evidence citation it carries are unchanged.
