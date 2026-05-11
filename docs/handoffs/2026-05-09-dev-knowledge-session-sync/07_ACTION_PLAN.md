# 07_ACTION_PLAN.md — Future State

Handoff: 2026-05-09-dev-knowledge-session-sync
Type: session-sync
Stage 3 generated: 2026-05-09 (night)

---

## Goal

**Primary: Refinement-partner session.**

Apply the press-back framework to each of the 9 strategic priorities added
to BACKLOG tonight. Output per item: concrete first step, dependencies,
Council-vs-conversational classification, hidden compound items, scope
boundary (IN/OUT). Result: BACKLOG with each strategic item turned from
fuzzy intent into actionable sub-item with defined first step. No code
changes. No major decisions. Clarification only.

**Definition of done:**
- All 9 Cross-stream strategic priorities in BACKLOG.md have refined entries
  with required sub-fields (first step, deps, debate classification, scope)
- Council-debate-required items flagged with proposed debate question
- Next-after-next session has clear top-priority pick
- CHANGELOG + JOURNAL updated

**Architect recommendation:** REST before heavy work.
Today was a marathon session (~9 ADRs + infrastructure + end-to-end test).
Picking a heavy P1 (audit tool implementation, sacred-files enforcement design)
risks degraded execution on important architectural work. If next session
starts and energy is low, treat rest as legitimate session output.

---

## Directives

*Source: Stage 2 architect, 2026-05-09 night. Verification steps added/confirmed by Stage 3.*

### Primary path — Refinement-partner session (recommended)

**1. Orient.** Read tonight's CHANGELOG + JOURNAL + LESSONS entries for context.
   - Verify: no surprises in tonight's deltas; confirm Stage 3 bundle matches
     current repo state (git rev-parse HEAD should match `01_MANIFEST.md`).
   - ~10 minutes. Do not begin refinement until orientation is complete.

**2. Apply press-back framework to each of the 9 Cross-stream strategic priorities.**
   For each item in BACKLOG.md (Council decisions management consolidation,
   Sacred-files maintenance enforcement, Hooks audit + consolidation, Skills
   universalization, Ecosystem standards audit, Kimi K2 evaluation, Scale tier
   re-evaluation, Large repo migration prep, VS Code productivity):

   Document per item:
   - **Concrete first step:** smallest reversible action that makes progress
   - **Dependencies:** what must be done/decided before this item can start
   - **Council-vs-conversational:** does this require a Council debate, or is it
     a conversational clarification? (Scope/architecture changes = Council;
     clarifications and emphasis shifts = conversational)
   - **Hidden compound items:** if this item is actually 2-3 items, name them
   - **Scope boundary:** what is explicitly IN for the next session attempt,
     and what is explicitly OUT

   Update BACKLOG.md with refined sub-fields under each item.
   Commit: `chore(backlog): refine strategic priorities — first steps, deps, scope bounds`
   Verify: BACKLOG has 9 refined items with required sub-fields.

**3. Identify Council-debate-required items** from refined BACKLOG.
   For each item classified as Council-debate-required in step 2:
   - Draft a Council debate question in plain language
   - Save drafts to a new file: `docs/decisions/pending-council-questions.md`
     (or wherever current convention places pending Council items — verify path
     against repo before creating)
   Commit: `docs(decisions): draft Council debate questions for refined strategic priorities`
   Verify: questions are specific enough to run as Council debates.

**4. Update CHANGELOG and JOURNAL.**
   - JOURNAL: prepend entry for this session (Did/Result/Next format, newest-first)
   - CHANGELOG: append entry under today's date
   Commit: `chore: JOURNAL + CHANGELOG for refinement-partner session`
   Verify: entries dated correctly, reference refined BACKLOG.

**5. Stop.** Do not begin implementing any refined item. Session value is
   clarification, not execution. Resist the urge to execute even well-scoped items.

### Secondary path — Low-effort batch (only if cognitive energy permits after primary)

**6. Fix HANDOFF_FOLDER_TEMPLATE 07_ACTION_PLAN DoD wording.**
   *Stage 3 clarification:* The DoD bug ("5 required sections" vs ADR-33 Lite
   spec's 4 required sections) exists in the *generated*
   `docs/handoffs/2026-05-09-ai-council-audit-sync/07_ACTION_PLAN.md:9`,
   not in `HANDOFF_FOLDER_TEMPLATE.md` itself (template has no pre-populated
   DoD text). Fix approach: (a) audit how the "5 required sections" wording
   appeared in the generated file — was it hardcoded in a now-deleted Stage 3
   prompt, or in a template spec? (b) fix the generated file for archival
   accuracy; (c) ensure future Stage 3 generation uses tier-aware section
   count language.
   Commit: `fix(handoffs): correct DoD section count in ai-council audit-sync action plan`
   Verify: ADR-33 Lite tier spec says 4 sections (Vision, Scope, Relationships, Lifecycle).

**7. PLAYBOOK content additions for ADRs 36/37/40/41.**
   Add PLAYBOOK.md sections for each ADR's operational workflow:
   - ADR-36: audit tool usage workflow (when to trigger, what to expect)
   - ADR-37: two-phase handoff format quick reference
   - ADR-40: tier transition procedures (S→M, M→L triggers + steps)
   - ADR-41: BACKLOG grooming workflow (per-handoff lightweight + quarterly deep)
   Update PLAYBOOK header version/date.
   Commit: `docs(playbook): add ADR-36/37/40/41 operational sections`
   Verify: no contradiction between PLAYBOOK additions and canonical ADR content;
   ESSENTIALS still summarizes where it overlaps (no duplication).

**8. Update CHANGELOG / JOURNAL** for batch fixes if executed.

### Tertiary path — Defer to dedicated future sessions

**9. Defer entirely** (one item per dedicated session minimum — do not bundle):
   Audit tool P1 implementation, sacred-files enforcement design, hooks audit,
   skills universalization, ecosystem standards audit, Kimi K2 evaluation,
   scale tier re-evaluation, large repo migration prep, VS Code productivity.

---

## Boundaries

*Source: Stage 2 architect, 2026-05-09 night.*

### Do NOT

- **DO NOT execute any of the 9 strategic priorities.** Next session output is
  updated BACKLOG entries, not implementations. Today's session demonstrated scope
  creep from "fix" to "fix + implementation" repeatedly. (witnessed by architect)

- **DO NOT add new BACKLOG items during refinement** beyond hidden compound items
  surfaced from existing entries. New items come from work, not from refinement.

- **DO NOT restructure BACKLOG architecture** (sections, streams, priority schema).
  If structure feels wrong, flag for future Council debate; do not unilaterally change.

- **DO NOT push to remote** without explicit Rob confirmation.

- **DO NOT initiate Council debates from refinement session.** Drafting questions
  is fine (Directive 3); running a Council debate requires its own session with
  bandwidth for synthesis.

- **DO NOT touch VISION.md** beyond minor clarification edits. Strategic emphasis
  was added tonight; let it settle at least one session before iterating.

- **DO NOT assume cross-repo state.** Target repos live independently and change
  without coordination. Verify via Claude Code in target repo context if needed.

- **DO NOT mark Stage 2 / synthesis / report claims as "witnessed"** when they're
  "reported by another agent" or "inferred." Distinguish carefully. Anti-pattern
  surfaced live in Stage 2 exchange. (new learning from this handoff)

- **DO NOT proceed with refinement if energy is low.** Rest is legitimate session
  output after a historic session.

### Anti-patterns to actively avoid (emerged from today)

| Anti-pattern | Mitigation |
|---|---|
| Prescriptive choice without grounding — recommending specifics without verification | Verify, then recommend |
| Witnessed vs reported vs inferred confusion — marking secondhand knowledge as firsthand | Explicit category per claim |
| Format requirements buried = ignored — critical instructions at end of long prompts | Critical requirements at top |
| Design without empirical contact — protocols designed in isolation accumulate gaps | Test end-to-end before declaring complete |
| Scope creep from fix to fix + implementation — small corrective scope expands mid-execution | Explicit scope statement at start; refuse to expand during execution |
| Methodology debt accumulation past circuit-breaker threshold — repeating patterns in long sessions | Consolidation pause every N debt instances or explicit session-length boundary |

### Items requiring Council debate (not unilateral action)

- Kimi K2 adoption level (research / production / experimental)
- Scale tier system fate (formalize / replace / deprioritize)
- Whether "iterujemy do skutku" mode warrants formal documentation with entry/exit criteria
- Whether velocity should be explicit VISION value (vs implicit consequence of continuous improvement)
- Sacred-files enforcement approach: reactive (CI check) vs proactive (session-end skill)

### Special instruction: press-back partner posture

The next chat receiving this bundle should act as Rob's **refinement partner**,
not just executor. For each BACKLOG item, challenge vague scope, surface
dependencies, classify debate vs conversational, identify compound items.

Reference: Browser-3 receiver-side review catching DoD typo is the precedent.
That posture — reading critically, flagging what doesn't add up — is the target.

---

## Success criteria

The next session succeeds if:
1. BACKLOG has 9 refined strategic items with first step + deps + debate classification + scope boundary
2. Council-debate-required items have drafted questions saved
3. CHANGELOG + JOURNAL updated
4. No implementation of refined items began
5. Session ends clean: git status clean, validators passing, branch ready for merge