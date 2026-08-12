# Architect strategic supplement — 2026-08-12-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-12

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

### CC-observed addenda — this window's carried items

> These are **CC observations from the closing arc, not chat answers.** They are placed here so the
> outgoing architect chat can confirm, correct, or add the "why" behind each; they do **not**
> pre-empt the ANSWERS region below, which stays EMPTY until the operator fills it. CC never
> fabricates an outgoing chat's answers.

**A. The two night artifacts ride UNADJUDICATED — the incoming seat's first order of business.**
`night-1` (truth audit + handoff numbers) and `night-2` (lessons, governance, strategy) are merged
to `main` and ratify nothing. Landing them made their content reviewable in the tree; it accepted
none of it. Ask the outgoing chat what it *intended* each to bind, because the artifacts themselves
state findings rather than decisions.

**B. OPEN RULING carried — the I-D6 working-set reading.** I-D6 defines the working set as
SEED/DRAFT/READY; the BRIEF one day later applies DRAFT-only. Measured at the cut the two readings
differ by **11** (definition-reading 14 against a ceiling of 6; applied 3). Not reconcilable by
evidence — two different rules, and the choice is the operator's. **It gates the consolidation-intake
filing**, so it is upstream of item C.

**C. The consolidation intake is mis-scoped as drafted.** Night-1 verified the three GAPs
negatively: GAP-1 is real; GAP-2's archive leg is owned by `[#420]` under a live do-not-touch order;
GAP-3 is W-9(a) inside an ACCEPTED intake with a recorded `AGENTS.md` collision hazard. Filing
GAP-1+2+3 as one intake would re-derive two owned scopes — the failure its own brief names.

**D. The VS Code incident closed during the arc.** Root cause was a `terminal.integrated.env.windows`
`"Path"` member that REPLACES the terminal PATH — **not ours**, present in every settings backup
back to 2026-07-12, now removed. 26 dead `pytest-of-*` PATH entries cleaned (1286 → 4168 → 1322
chars). The test-isolation defect that **was** ours is fixed (the suite wrote the real
`HKCU:\Environment` key; an autouse conftest tripwire now fails the offending test and restores the
value). Merged `win-tooling@1f8b300`, pushed.

**E. The night lanes ran LOCALLY — a deviation with a near-miss.** Both ran against the primary
checkout rather than one worktree per lane. A commit was silently re-targeted onto the other lane's
branch between `git add` and `git commit`, sweeping in that lane's untracked artifact; repaired
non-destructively and nothing was lost. **`git add` then `git commit` is not atomic against a
concurrent branch switch in a shared tree.** The shared index also made `audit-index-freshness`
unsatisfiable from inside a lane — that generator defect is now fixed (tracked-files-only).

**F. The organ index relocated and the gate-shape hole closed.** `docs/ORGAN-INDEX.md` →
`ecosystem/organ-index.md` (operator ruling A; register `STANDING_RULINGS` **K-1**), plus **Rule C**
in `validate_hermetization.py`. The finding worth carrying is *why* it landed loose: ADR-101's gate
read the top level and the `docs/<genre>/` level and stopped, so Rule A was silent **by its own
literal spec** — and a test asserted that silence. Rule C reads the rest of the path; Rule A is
untouched.

**G. Architect-model note — how to boot this seat.** Per PLAYBOOK **Ch8**, the architect seat
**boots Opus**. **Fable is reserved for adversarial passes** (the plan-review / red-team role), not
for the primary architect seat — booting it here would spend the adversarial reserve on ordinary
adjudication and leave nothing independent to check the result.


===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# SUPPLEMENT — ANSWERS from the outgoing architect (seat 27, browser) · 2026-08-12
Paste everything below into the ANSWERS region of SUPPLEMENT.md, then tell CC `supplement filled`.

**1. Strategic intent.** The next session's way-of-working goal is a single flip: **adjudicate-then-execute**. This window (and the two before it) produced a planning SURPLUS — two night reports, a ratification batch, a brief, three instruments answered — and the surplus is now the risk: every unadjudicated draft is a page someone will re-derive. The next session converts the surplus into law in ONE morning act (the adjudication hour), and then the seat's job for the rest of the week is **execution only**: no new planning artifacts, no new instruments, no new intakes beyond the one re-scoped filing below, until batch-4 truly closes. The operator has said this in his own words; treat it as the window's contract.

**2. Tensions weighed.** (a) Measure-first vs the operator's tempo — held in governance (ruff behind hotspots, providers behind the corpus, refactors behind §D) and broken once by drift in tooling (the dispatch saga: four tempo-fixes before the mechanism class was questioned); the repair was mechanization, not apology (`fb52bf6`, `-Check`). (b) Research consumption vs the birth cap — resolved amendment-over-birth (`[#513]`), ledger held at 2+1. (c) Honest-red vs green optics — chosen every time it mattered: W1/W2 refused to close rows over blank legs; the untestable count is reported as NOT fallen; the §B dashboard shipped at 0🟢. (d) Sequential vs parallel — settled as sequential-by-default with matrix-proven, operator-approved pairs; the matrix is the law, not caution.

**3. Considered + rejected (do not relitigate).** Building a prompt-distiller (backlog verdict PARTIALLY — every axis owned, `[#412]` lead; library-first says measure CC-native agents/skills first) · Fable as the architect seat (Ch8 routing; Fable stays the adversarial reserve) · "merge W4/W6 before W1" (rejected for ids-before-contract + W6 drop) · `protocols/` as the organ-index home (ruling A: `ecosystem/`, generated-artifact pattern; register K-1) · immediate ruff-family adoption (behind churn×complexity hotspots, unrun) · graph-DB/server storage (dead list) · retiring Codex before Grok passes the corpus (admit-then-retire) · backlog bankruptcy (per-row argued removal instead).

**4. Open questions (deliberate, each with its gate).** (i) **I-D6 working-set reading** — operator's word; gates the intake filing. (ii) **The consolidation intake's FINAL scope** — night-1 falsified the draft scoping: GAP-2's archive leg is OWNED by `[#420]` under a live do-not-touch order, GAP-3 is W-9(a) inside an ACCEPTED intake with a recorded AGENTS.md collision hazard; the filing therefore covers **GAP-1 (architecture-freshness mechanism) + the ontology/graph attach + ONLY the genuinely unowned legs of taxonomy/portability, cross-referencing [#420] and W-9(a) as owners instead of re-scoping them**. (iii) The strict live-id `depends-on` predicate (parked; interim strip-law covers operations). (iv) §B clauses 1/5 falsifiability-from-tree (22% of the finish line). (v) The OneDrive read-only rule (operator TAK/NIE pending). (vi) Bake-off timing vs the corpus-reconciliation gate (11/12 verdicts pinned to `extend-select = []`).

**5. Decomposition rationale — what must NOT be redone.** Batch-4's shape stands: W1/W2/W5/W-521 merged, W3 carried because it shared freshness-gated CLAUDE.md with live W1 (unblocked at `0136cec6`), W4 carried because a lane without a row id is the defect W1 exists to prevent (G-2: ids-before-contract), W6 dropped (cap + ARCHITECTURE collision + no id). The next-session order 1–8 is gate-derived, not preference: adjudication unlocks removals, lessons and I-D6 at once; W4 outranks W3 because repairing 72 existing rows beats protecting future ones on the under-100 axis; everything later sits behind a named gate (intake←I-D6; bake-offs←corpus reconciliation; style←hotspots; telemetry←two windows of data). Do NOT re-derive: the disjointness matrix, the census classes (95/72/23/8), the G-register resolutions, or the night reports' evidence — adjudicate them, don't re-measure them.

**6. Off-repo context.** The operator's declared week-goal: **execution only** — calibrate expectations: the adjudication hour is the one non-execution act and it is the unlock, not a detour. Transport: the browser paste channel degraded mid-window; the standing practice is FILE UPLOAD for anything longer than a line. Tooling: `dispatch <contract>.md` works in every shell (PATH command, `-Check`-guarded); VS Code is healthy (root cause pre-dated us, removed); the machine owes nothing. The three instrument answers (execution challenge, consumption challenge, interrogation) are committed or riding the closing addendum — they are the window's self-account and the fastest way for the incoming seat to calibrate against reality. Calendar: `[#492]` Grok re-check **2026-08-17 (this week)** · intake #10 disposition rides the adjudication · `[#322]`/`[#360]` dated reviews 2026-09-09.

**7. Ratified-in-chat, not yet in repo.** (a) The **OneDrive read rule** — proposed "read-only under declared diagnostic need, disclosed in-report; writes absolutely denied"; PENDING the operator's word → home: STANDING_RULINGS line when ruled. (b) The operator's **execution-only-week intent** → home: this supplement (now recorded). (c) The **paste-completeness / file-upload transport practice** — browser-seat working rule, no repo home needed (not doctrine, a channel fact). Otherwise: none — every other in-chat ruling of this window was landed with a locator (I-D3, I-D8, AM-5, K-1, strip-law, anchor-law, re-ruling on pairs) or is listed in (4) as deliberately open.

---

## THE PLAN (short-term → session → week → horizon)

**SESSION 1 of the new window (the adjudication hour, then dispatch).**
1. Boot per bundle (Opus; Fable held adversarial). Read: night-1 report · night-2 report · BRIEF · this supplement. No re-derivation.
2. **Operator adjudication batch (one picker set, ≤30 min):** I-D6 reading (rec: DRAFT+READY) · lessons table TAK/NIE per line (19 items, ratchet-clean drafts ready) · removal sheet KEEP/RETIRE/FOLD per row + intake #10 · intake→ADR promotions (per night-2's fork-test arguments) · the re-scoped consolidation-intake filing decision (per §4.ii above) · OneDrive rule.
3. **Execute the adjudication's mechanical tail the same arc:** removals per TAK, lessons→LESSONS/PLAYBOOK, promotion drafts opened, register lines.
4. **Dispatch W3** (`lane-c-513-landing-predicate`, skeleton ready in night-2 E5) — the organ that ends the ruled-but-unlanded class.
5. **Mini-GO: birth the W4 row** (conversion campaign, mechanical Done-when over the census P1/P2 drafts) → dispatch W4 wave 1.
Mechanical success condition (D6 of the interrogation): after step 3, the register holds a disposition for 100% of both night drafts' items — grep-countable, zero lines without a verse.

**THE WEEK (execution only).** W3 merge → W4 waves (the single biggest under-100 lever: 72 rows) → removal executions land → `[#492]` re-check on 2026-08-17 via the corpus (reconciliation first — the pin gate) → batch-4 CLOSES with its packet (checklist items 1+3 finally checkable) → if capacity remains: ARCHITECTURE Ch2/Ch6 organ rows + the `[#514]`/`[#510]` remaining legs. No new intakes, no new instruments, no new planning artifacts this week.

**THE HORIZON (windows 3–8).** Under-100 in ~2–4 execution windows (conditional: W4 fires, net ≤ 0 holds); zero-untestable in ~3–5 — the constraint that moves the finish line most. The consolidation intake (as re-scoped) lands the architecture-freshness mechanism and the ontology recon. Provider table settled by MEASUREMENT: Gemini `[#491]` and Grok `[#492]` on the corpus, Codex sunsets only after a pass, Copilot as the third probe. Code-style stack enters after the hotspot baseline; telemetry reads after two windows of data. **Satellite re-entry:** the feature/satellite quota bucket exists and the fleet gauge (`[#270]`) now watches the satellites — schedule the first satellite-serving lane within two windows so the hub's outputs start paying rent outside the hub (this is the one soft blind spot the plans kept deferring). Monorepo: parked by the operator's own consolidate-first sentence until §B v1.0.

**Blind-spot check, honestly:** (1) the consolidation-intake mis-scope — CAUGHT by night-1, corrected above; (2) satellite consumption — named above with a two-window deadline; (3) the calendar items are in §6; beyond these, no unplanned known work remains: every theme from the operator's strategy dump, the six research commissions, and three instruments maps to a row, an intake, a register line, or a dated gate. The planning is DONE. The week is for the plan.

---
CORRECTION ADDENDUM (incoming seat, 2026-08-12, gate INH-3): §6's calendar line carried "[#322]/[#360] dated reviews 2026-09-09". The [#360] leg is struck — its 2026-09-09 review was WITHDRAWN by operator ruling on 2026-08-11 (see tasks/360-*.md, RE-ANCHORED note; I-1 superseded by census evidence). [#322]'s 2026-09-09 review stands. Original text preserved above per primary-source discipline.
