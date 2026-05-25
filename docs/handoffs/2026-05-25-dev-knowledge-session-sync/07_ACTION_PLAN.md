# Action Plan — 2026-05-25-dev-knowledge-session-sync

<!-- scope: hybrid -->

Future State per ADR-37 [session-boundary protocol]. Source: Stage 2 architect
OBJECTIVE / DIRECTIVES / BOUNDARIES answers, reconciled against repo state at
Stage 3.

## Next session goal

The single highest-priority objective is to **obtain an operator decision on
whether to pursue handoff-bundle structural consolidation** (the 11→N question),
and — paired in the same session — to **formalize how AI Council outputs return
into the workflow for persistent, chat-retrievable retrieval** (BACKLOG P1
"Council decisions management consolidation").

These pair naturally: if consolidation is pursued, the AI Council debate on the
bundle question becomes a live proving ground for the Council-workflow return
mechanism — one decision exercises the other. If consolidation is shelved, the
Council-workflow formalization proceeds standalone.

If the operator shelves consolidation immediately, pivot to the next P1:
**codifying the scrum-master review authority pattern** (N=3 grounding reached;
this unblocks the cross-repo tier-deprecation rollout sessions).

## Action plan

1. **Obtain operator decision on handoff-bundle consolidation.**
   - *Pursue:* frame an AI Council debate around four questions — (a) does the
     ADR-45 [handoff v4, rolled back] rollback rationale still apply; (b) can the
     VISION/PLAYBOOK/ESSENTIALS invariant copies be replaced by a single anchor
     or pointer without breaking the Self-Containment Rule; (c) is the SHA-256
     manifest essential or risk-acceptably removable; (d) what are *real*
     per-bundle token measurements in this repo (not generic research). Schedule
     the Council session, capture output, draft an ADR (new, or an ADR-45
     amendment).
   - *Shelve:* add a BACKLOG entry capturing the decision, rationale, and
     revisit-criteria, then proceed to action 2.
   - **Verify:** decision documented as a drafted ADR (if pursued) or a BACKLOG
     entry (if shelved). Commit on feature branch.

2. **Codify the scrum-master review authority pattern (BACKLOG P1).** N=3
   empirical grounding reached (architect inference — verify against repo before
   choosing mechanism). Path: new ADR or amendment to the relevant existing ADR.
   Output: an authority reference that cross-repo rollout sessions can invoke.
   - **Verify:** ADR drafted/amended; `pytest` green; `python scripts/audit.py
     health` OK; commit on feature branch.

3. **Council decisions management consolidation (BACKLOG P1) — define sub-items:**
   a contradiction-detection mechanism for ADR evolution; an ownership model
   (which decisions evolve via amendment vs supersession ADR vs frozen); a
   chat-retrievable, machine-readable index of recent decisions. Scope to
   single-session capacity; partial completion + a BACKLOG sub-item for the
   remainder is acceptable.
   - **Verify:** decisions index built and tested with a representative query;
     ownership model documented; commit on feature branch.

4. **Capture three operator-stated strategic items as BACKLOG entries (P3 each):**
   remote + nightly batch on schedule (overnight session continuation); Chinese
   model adoption strategy (GLM, Kimi K2 — cost-optimized inference); continuous
   token optimization as a meta-concern.
   - **Verify:** three BACKLOG entries committed with rationale + acceptance
     criteria + effort fields.

5. **Cheap quick wins (opportunistic, non-blocking):**
   - `CLAUDE.md` §4 cites a stale known-failing test
     (`test_audit_run_passes_structural_checks_on_synthetic_repo`) — the suite is
     green (Stage 3 verified: 72 passed). Remove the false-flag clause (one line).
   - `protocols/SESSION_SETUP.md:209` still says "append JOURNAL + CHANGELOG" —
     CHANGELOG retired per ADR-49. Strike CHANGELOG (one line). *(Stage 3 verified
     both still present.)*
   - **Verify each:** edit applied; tests green; audit health OK.

6. **Apply pending user-instructions update** (operator UI action — Claude
   settings → Profile → User preferences). Not in-repo executable; affects future
   chats only (architect inference).
   - **Verify:** operator confirms applied. No in-repo verification.

7. **Skills review (BACKLOG P2).** Inventory active skills in `.claude/skills/`
   (and user-level); per skill decide keep / promote / consolidate / deprecate.
   - **Verify:** inventory + dispositions logged; commits per disposition.

8. **Hooks audit and consolidation (BACKLOG P2).** Inventory `.claude/` hook usage
   across SessionStart / SessionStop / pre-commit (SessionStop absent —
   architect inference). Identify workflow-automation patterns + expansions.
   - **Verify:** hooks inventory committed; plan documented.

9. **Branch hygiene (low-friction, before opening new branches).** Resolve
   unmerged status of `docs/audit-ai-council-2026-05-23-deep` and
   `docs/audit-corp-monorepo-2026-05-23-deep` (diff vs main; delete if reports
   already on main); `chore/workspace-sort-default-2026-05-24` is a confirmed
   superseded intermediate. **Operator confirmation before each deletion.**

**Sequence rationale:** Action 1 first — it unblocks the architecture-vs-execution
split for everything downstream. Action 2 unblocks cross-repo rollout. Action 3
pairs with 1 (the Council workflow is exercised by 1's real debate). 4 captures
items before they're lost. 5 is cheap and revertible. 6 is operator-side. 7-8 are
named operator focus areas but non-blocking. 9 is hygiene best done first.

## Hard Constraints

Violating any of these blocks the session's primary work — treat as fenced.

1. **Do NOT collapse the handoff bundle** — do not drop the full
   VISION/PLAYBOOK/ESSENTIALS invariant copies or the `01_manifest.json` SHA-256
   manifest, or otherwise reduce the bundle inventory, **without an explicit
   operator-approved decision to re-open ADR-45**. The structure is
   architecturally load-bearing for the Self-Containment Rule, not ceremony.
2. **Do NOT edit append-only files in place** — `LESSONS.md`, `TOKEN-LOG.md`
   accept appends only.
3. **Do NOT edit immutable files in place** — ADRs accept appended amendment
   blocks only (no rewrite of original Decision/Rationale); transcripts, handoff
   bundles, and `status: immutable` audits accept no content changes.
4. **Do NOT add orchestration scripts** — Layer-2 invariant (ADR-28): scripts do
   mechanical work only; sequencing/decision-routing/workflow control belong to
   humans and Claude Code.
5. **Do NOT push or auto-merge without explicit operator approval** — branches
   stay local; state the merge command, operator executes.

## Narrow scope rules

- **Do NOT touch corp-monorepo or ai-council files** from this session
  (read-only contract). Audit reports about them may be hosted here under
  `docs/audits/`; modifications happen in those repos' own sessions. Do not
  generate cross-repo reconciliation reports from this repo's own work.
- **Do NOT default to Sonnet for substantive prompts.** Choose per task: Sonnet
  for mechanical/single-file/well-specified work; Opus for
  audit/review/synthesis/architecture/judgment-heavy work. Name the model in the
  Model/Mode/Effort table at the top of each substantive prompt.
- **Do NOT generate prompts referencing existing-system state without a
  pre-flight verification pass** — read live files end-to-end and cited ADRs in
  full before designing changes. (Recent arc: N=7 verification-miss instances,
  incl. a hallucinated file-map. "I'm confident" is the signal to verify harder.)
- **Do NOT treat a leaner-bundle proposal as routine refactoring** — it is
  methodology change; the deliverable is a formal ADR, not a template edit.

## Fallback contingencies

- **Operator unavailable for the consolidation decision (action 1)** → proceed to
  action 2 (scrum-master codification); defer consolidation to its own session.
  Do not resolve it unilaterally.
- **AI Council not invokable this session** → defer all Council-requiring
  decisions; execute mechanical/hygiene work (actions 5, 9). Do not approximate
  Council deliberation with single-model reasoning for architecture decisions.
- **Verification-miss pattern recurs** (premature closure, claims contradicted by
  repo state, hallucinated structure) → flag a handoff opportunity per established
  triggers; do not push through silently.
- **Scope cannot complete in one session** → end-of-session handoff via the
  validated bundle process. Do not invent shortcut variants.

## Success criteria

- Operator decision on bundle consolidation is recorded (drafted ADR or BACKLOG
  entry) — action 1 closed.
- Any code/doc edits leave `pytest` green and `python scripts/audit.py health` OK.
- All work committed on feature branch(es); nothing pushed/merged without operator
  approval; working tree clean at session end.
- Any deferred scope captured as a BACKLOG entry rather than left implicit.
