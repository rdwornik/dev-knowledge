# Stage 2 Response — dev-knowledge (session-sync)

<!-- scope: hybrid -->

| Field | Value |
|---|---|
| Target repo | `.dev-knowledge` |
| Type | session-sync |
| Slug | `2026-05-25-dev-knowledge-session-sync` |
| Stage 1 timestamp | 2026-05-25 |

<!--
ROB — INSTRUCTIONS:
1. Take stage1-question.md to the OLD browser chat for .dev-knowledge (the chat
   being wrapped up). Copy from its PASTE_BOUNDARY line to end-of-file.
2. The old chat answers the 5 pipeline questions (OBJECTIVE / REALITY /
   RATIONALE / DIRECTIVES / BOUNDARIES).
3. Replace EVERYTHING below the marker line below with the architect's response.
   Save this file.
4. Back in Claude Code, say: "complete handoff for dev-knowledge" → Stage 3.

Do NOT edit anything above the marker line.
-->

═══════════════ REPLACE EVERYTHING BELOW THIS LINE ═══════════════

### **1. OBJECTIVE**

This section assumes zero prior session knowledge.

The next session's single highest-priority objective is to obtain an operator decision on whether to pursue handoff bundle structural consolidation, and — paired in the same session — to formalize how AI Council outputs (decisions, drafted ADRs, debate rationale) return into the workflow for persistent retrieval. If consolidation is pursued, the AI Council debate itself becomes the proving ground for the Council-workflow formalization (real architectural question, real Council output, real test of the return-path mechanism). If shelved, the workflow formalization proceeds standalone against the BACKLOG P1 "Council decisions management consolidation" framing.

Rationale for ranking this above other P1 items: the handoff consolidation question is the explicit unclosed architectural thread from the recent session arc; resolving it (either decisively shelve or formally pursue) clears it from the open-thread queue. The Council-workflow formalization addresses an operator-stated recurring concern — that Council decisions return into chat-retrievable state — which is foundational for sustainable architectural deliberation across the ecosystem. Concurrent treatment uses one to test the other.

If operator chooses to shelve consolidation immediately: pivot to codifying the scrum-master review authority pattern as the next P1 (N=3 empirical grounding reached in recent work, codification unblocked, prerequisite for cross-repo tier-deprecation rollout sessions).

### **2. REALITY**

This section assumes zero prior session knowledge.

**Witnessed state at session-arc close (work landing 2026-05-23 through 2026-05-25):**

Substantial governance work merged to main covering: repo-tier system fully deprecated (task-sizing Scale S/M/L preserved as orthogonal authoring aid); ARCHITECTURE.md mandate universalized across all repos regardless of size; README.md deprecated from baseline; root hygiene convention added (`.env.example` no-create policy, dot-prefix-where-supported pattern); audit tool unified to governance-docs-only baseline check; self-audit completed against amended standards (15 findings fixed including operator-flagged tier residue in ARCHITECTURE.md, a live "Project Scale Tiers" section in ESSENTIALS.md that sat past a naive grep hit-cap, and a `[L+M]` tag caught only by post-remediation tag-specific re-grep).

BACKLOG audit completed during the arc (witnessed: ~48 entries categorized; bookkeeping lag surfaced — four items closed in repo reality but still "open" in BACKLOG, caught only by live-state check, not commit-name match). One framing assumption was refuted during this audit: the AI Council pipeline was previously assumed undefined / ad-hoc, but PLAYBOOK §5 already documents the trigger → debate → ADR-draft → archive → return flow in full. (architect inference) The Council-workflow operator concern is therefore not about defining the pipeline; it is about decision retrieval and management AFTER the pipeline runs — contradiction detection, ownership model, chat-retrievable index of recent decisions.

Handoff process audit residuals resolved (witnessed: six medium findings closed per the relevant audit's recommendations section; 12-file bundle structure structurally preserved; `_in_progress/` → `in-progress/` directory rename landed; residual CHANGELOG references struck from Stage 3 procedure per ADR-49 retirement). Workspace combo iterated to stable state (multi-root with dated-artifact aliases at bottom, `explorer.sortOrder: default` plus `sortOrderReverse: true` plus `compactFolders: false`; six canonical-file workspace tasks added — `open-vision`, `open-journal`, `open-backlog`, `open-architecture`, `open-lessons`, `open-claude-md`).

**Unclosed decision threads requiring operator call before related work proceeds:**

Handoff bundle structural scope (11→N consolidation): a prior consolidation proposal was rejected on broken premise during recent work. (witnessed) The proposal's file-mapping table named source-side files that do not exist in the repository; verification against a live bundle plus the relevant structural audit showed the real 12-file inventory includes invariant copies of VISION, PLAYBOOK, and ESSENTIALS plus a SHA-256 manifest in `01_manifest.json` — none of which the consolidation mapping mentioned. Mechanically executing it would have dropped these silently, which is materially the direction ADR-45 explored and rolled back the same night it was attempted. Operator chose "audit fixes only" for the immediate cleanup. The substantive question — whether bundle structure should change — remains open and requires AI Council deliberation per the "architecture decision = AI Council" rule.

ADR-45 status: supersession-of-ADR-42 claim withdrawn during the recent audit residuals work (witnessed: strikethrough on the original `Supersedes:` header preserving the historical record, annotated References line, Amendment 2026-05-25 documenting the withdrawal). ADR-42 v3 plus accumulated amendments remains the live convention. No further ADR-45 action pending unless consolidation is pursued, which would re-open it.

**Operator-stated future strategic items not yet captured in BACKLOG:**

Remote + nightly batch on schedule (overnight session continuation pattern — when a session resets at night, scheduled batch can continue work). Chinese model adoption strategy (GLM, Kimi K2) for cost-optimized inference. Continuous token optimization as ongoing concern. These belong as new BACKLOG entries (P3 each — strategic direction, not immediate execution).

**Work in progress not reflected in committed state:**

User instructions update is prepared but pending operator UI action (Claude settings → Profile → User preferences, manual paste of corrected text). Affects future chats only, not in-repo executable. Corrections from this session: CHANGELOG line removed per ADR-49 retirement (was stale in operator's existing preferences); model selection criteria added (Sonnet mechanical / Opus judgment-heavy, actively choose, never default); verify-before-claiming pattern added to communication style; matrix-before-experimenting pattern added as new "Architectural thinking" section; dev standards tightened (project-specific tool conventions moved to project CLAUDE.md / PLAYBOOK).

Pre-existing drift flagged during recent cleanup but not in scope of that work: `protocols/SESSION_SETUP.md:209` still references "append JOURNAL + CHANGELOG" — same M-3 drift class as already-resolved findings, one-line strike, BACKLOG entry warranted.

Unmerged audit branches retained with status unknown: `docs/audit-ai-council-2026-05-23-deep`, `docs/audit-corp-monorepo-2026-05-23-deep`. (architect inference) The audit reports themselves exist on main (verified during BACKLOG audit work which referenced both); these branches are likely redundant artifacts safe to delete after diff verification, but operator confirmation required before deletion. A third branch `chore/workspace-sort-default-2026-05-24` is a confirmed superseded intermediate of the workspace sort iteration; safe to delete.

**Verification-miss pattern as active risk for next session:**

The recent session arc demonstrated N=7 verification-miss instances (witnessed): factual claims about ADR contents that the cited ADR did not actually state, hallucinated file-mapping tables in a substantive refactor prompt, missed file existence ("frontmatter mechanism" proposed where the system actually uses a Registry mechanism), claims about merge state contradicted by repo log, a CHANGELOG mandate line inserted into proposed user preferences while ADR-49 retirement was simultaneously being codified. The LESSONS.md entry codifying this pattern is recorded, but the underlying mechanism is behavioral, not knowledge: confidence is itself a signal to verify harder, not a license to skip. The next session should treat this as active risk: for any substantive prompt referencing existing-system state, mandatory pre-flight pass to read live files end-to-end and cited ADRs in full before design begins.

**Constraints next session must respect:**

Append-only files: LESSONS.md, TOKEN-LOG.md (never edit in place). Immutable files: ADRs accept appended amendment blocks only (no in-place rewrite of original Decision/Rationale blocks); transcripts, handoff bundles, and audits carrying `status: immutable` frontmatter accept no content changes. The 12-file bundle structure is load-bearing (invariant copies realize Self-Containment Rule; SHA-256 manifest provides integrity verification); do not collapse without explicit ADR-45 re-opening. Layer-2 invariant: orchestration belongs to humans and Claude Code, not to scripts. Cross-repo isolation: corp-monorepo and ai-council work happens in dedicated sessions targeted at those repos.

### **3. RATIONALE**

This section assumes zero prior session knowledge.

Three reasoning chains witnessed in the recent session arc that the next session should understand:

**Why the 11→N handoff bundle consolidation was rejected without substantive deliberation, deferred instead:**

The surface failure was a fabricated file map — names that did not exist in the repository. The deeper issue exposed by verification: invariant copies of VISION, PLAYBOOK, and ESSENTIALS in the bundle plus the SHA-256 manifest are precisely the mechanism by which the Self-Containment Rule is operationally realized. A receiving chat opens with these in-bundle and does not need to load the source repository or perform any external retrieval to operate. Removing them is not a file-count optimization; it is an architectural shift that changes what the bundle is. ADR-45 explored exactly this direction (bundle collapse, mechanical gates rewrite) and rolled back the same night it was attempted. The structural audit's own recommendations section never proposed consolidation — only six audit-endorsed hygiene findings.

Therefore: the consolidation question is genuinely real (token cost concerns, ceremony-decay evidence from healthcare-handoff implementation research, community pattern comparison showing this approach is at the heavy end of the spectrum) but the answer requires AI Council deliberation grounded in real bundle inventory plus an explicit decision on whether to re-open ADR-45. Not routine refactoring; not a single-prompt scope.

**Why ADR-45's supersession-of-ADR-42 claim was withdrawn rather than kept:**

ADR-45 had carried a `Supersedes: ADR-42` header from its initial drafting. Its v4 mechanical-gates rewrite was explored and rolled back same-night. If ADR-45's substantive decision did not stick, it cannot supersede ADR-42. The audit residuals fix (M-2): strikethrough on the original supersession header (preserves the record that the claim was once made), annotated References line, Amendment 2026-05-25 documenting the withdrawal. No original decision content rewritten — the Status line had already been clarified in prior work; this fix reconciled the supersession header with that already-corrected Status. ADR-42 v3 + amendments remains the live convention.

**Why the audit residuals were split from the consolidation into a separate scope:**

Audit findings (M-1, M-2, M-3, M-5, M-6, L-3) were each explicitly recommended in the relevant audit's own §8 recommendations — each described as "delete/add < 10 lines" hygiene against the protocol's v3.0 → v3.3.3 version evolution. Risk profile: low, audit-endorsed, structure-preserving.

Consolidation (11→N) had neither audit endorsement nor a reality-based design. Risk profile: high architectural impact, requires Council deliberation, would re-open rolled-back territory.

Splitting these scopes preserved the safe-and-endorsed work as immediately executable while flagging the substantive-and-architectural work for proper deliberation. Operator made this split explicitly when the broken premise was flagged before execution rather than after.

### **4. DIRECTIVES**

This section assumes zero prior session knowledge.

Sequential actions for the next session:

1. **Obtain operator decision on handoff bundle consolidation.** Two paths possible:
   - Pursue consolidation: frame AI Council debate around four specific questions — (a) does the ADR-45 rollback rationale still apply, given any state changes since the rollback; (b) can invariant copies of VISION / PLAYBOOK / ESSENTIALS be replaced with a single anchor file or pointer mechanism without breaking the Self-Containment Rule; (c) is the SHA-256 manifest essential for integrity OR risk-acceptably removable; (d) what are real token measurements per bundle creation (Stage 1 + Stage 3 actual costs in this repo's recent bundles), not generic research findings extrapolated from other contexts. Schedule the Council session; capture debate output; draft an ADR (new or ADR-45 amendment) embodying the decision.
   - Shelve consolidation: add a BACKLOG entry capturing the decision, rationale, and revisit-criteria, then proceed directly to directive #2.

   Verification: operator decision documented either as drafted ADR (if pursued) or as BACKLOG entry (if shelved). Commit on feature branch.

2. **Codify the scrum-master review authority pattern (BACKLOG P1).** (architect inference) N=3 empirical grounding reached in the recent session arc through ai-council 2026-05-12 deep audit, corp-monorepo 2026-05-23 deep audit, and ai-council 2026-05-23 re-pass — codification is unblocked. Codification path: new ADR or amendment to the relevant existing ADR (verify scope against repo state before choosing). Output: an authority reference that subsequent cross-repo rollout sessions can invoke when applying patterns from this repo to corp-monorepo and ai-council.

   Verification: ADR drafted or amended; tests green; audit health OK; commit on feature branch.

3. **Council decisions management consolidation (BACKLOG P1) — sub-items to define:** a contradiction-detection mechanism for ADR evolution, an ownership model documenting which decisions evolve via amendment vs which evolve via supersession ADR vs which are frozen, and a chat-retrievable index of recent decisions (machine-readable, queryable). Scope realistically against single-session capacity; if the full set is too large, partial completion plus a BACKLOG sub-item capturing remainder is acceptable.

   Verification: decisions index built and tested with a representative query (e.g., recall the status of a recent ADR by name); ownership model documented; commit on feature branch.

4. **Capture operator-stated future strategic items as BACKLOG entries.** Three new entries to add: remote + nightly batch on schedule (overnight session continuation pattern); Chinese model adoption strategy (GLM, Kimi K2 — for cost-optimized inference paths); continuous token optimization as ongoing meta-concern. P3 each — strategic direction, not immediate execution, but capture-before-forget.

   Verification: three BACKLOG entries committed with rationale + acceptance criteria + effort estimate fields populated.

5. **Cheap quick wins available throughout — opportunistic, do not block other directives:**
   - `CLAUDE.md` §4 cites a stale known-failing test name (`test_audit_run_passes_structural_checks_on_synthetic_repo`) but the test suite is green. One-line edit to remove the false-flag.
   - `protocols/SESSION_SETUP.md:209` still references "append JOURNAL + CHANGELOG" — same drift class as already-resolved findings, CHANGELOG retired per the relevant ADR. One-line strike.

   Verification for each: edit applied, tests green, audit health OK.

6. **Apply pending user instructions update** (operator UI action, not in-repo executable). The corrected preferences text is prepared from the recent session; operator pastes into Claude settings → Profile → User preferences. (architect inference) Affects future chats only.

   Verification: operator confirms update applied; no in-repo verification possible.

7. **Skills review (operator focus area, BACKLOG P2).** Inventory skills currently in active use within this repo's `.claude/skills/`; for each skill, decide: keep, promote to user-level (`~/.claude/skills/`), consolidate with adjacent skill, or deprecate. Output: skills inventory + per-skill disposition + relevant BACKLOG updates.

   Verification: inventory completed; dispositions logged; commits applied per disposition.

8. **Hooks audit and consolidation (operator focus area, BACKLOG P2).** Current `.claude/hooks/` usage inventory across SessionStart, SessionStop, pre-commit. (architect inference) SessionStop hook is currently absent per recent BACKLOG context. Identify workflow-automation patterns and expansion opportunities; produce consolidation plan.

   Verification: hooks inventory committed; plan documented; commit on feature branch.

**Branch hygiene cleanup** (low-friction, before substantive work):

9. Resolve unmerged branch status: `docs/audit-ai-council-2026-05-23-deep` and `docs/audit-corp-monorepo-2026-05-23-deep` — check diff against main; if audit reports are already on main (verified during BACKLOG audit work), delete branches. `chore/workspace-sort-default-2026-05-24` — confirmed superseded intermediate, delete safely. Operator confirmation before each deletion.

**Sequence rationale:**

Directive 1 first because it unblocks the architectural-vs-execution split for everything downstream. Directive 2 because it unblocks the cross-repo tier-deprecation rollout sessions which represent the major next ecosystem-wide work. Directive 3 because it pairs naturally with 1 (the Council workflow is exercised by Directive 1's real Council question, making 3 partially self-validating). Directive 4 because operator-stated items need capture before they're lost to the open-thread queue. Directive 5 because cheap and immediately revertible. Directive 6 because it is operator-side independent. Directives 7-8 because operator focus areas are explicit but not blocking. Directive 9 because branch cleanup is hygiene best done before opening new branches.

### **5. BOUNDARIES**

This section assumes zero prior session knowledge.

The next session MUST NOT:

1. **Collapse the handoff bundle structure** — drop the full VISION / PLAYBOOK / ESSENTIALS invariant copies, drop the SHA-256 manifest at `01_manifest.json`, or otherwise reduce the 12-file bundle inventory — without an explicit operator-approved decision to re-open ADR-45. The bundle structure is architecturally load-bearing for the Self-Containment Rule, not ceremony. Prior consolidation was rolled back same-night; subsequent consolidation proposal was rejected on broken premises. Treat as fenced architectural territory until Directive 1 resolves.

2. **Edit append-only files in place.** LESSONS.md and TOKEN-LOG.md accept new entries appended only; existing entries are not modified or deleted under any circumstance.

3. **Edit immutable files in place.** ADRs accept amendment blocks appended (never in-place rewrite of original Decision or Rationale blocks); transcripts, handoff bundles in `docs/handoffs/{slug}/`, and audits carrying `status: immutable` frontmatter accept no content changes.

4. **Add orchestration scripts.** Layer-2 invariant: scripts execute mechanical work only; orchestration — sequencing, decision-routing, workflow control, branch-and-merge logic — belongs to humans and Claude Code, never to scripts. If a script would need to "decide what to do next," it is the wrong abstraction.

5. **Generate cross-repo reconciliation reports from this repo's own work.** Cross-repo audits (corp-monorepo, ai-council) happen in dedicated sessions targeted at those repos. This repo can host the audit reports under `docs/audits/` but cannot perform cross-repo file modifications. Universalization work (applying patterns from this repo to corp-monorepo and ai-council) likewise happens in those repos' own sessions, after the scrum-master review pattern is codified here (Directive 2).

6. **Default to Sonnet for substantive prompts.** Model selection per task is explicit: Sonnet for mechanical / single-file / well-specified / pattern-matched implementation work; Opus for audit / review / synthesis / architecture / judgment-heavy / severity-calibration / subtle-pattern-recognition work. Actively choose per task. Recent session demonstrated N=2+ instances where Opus surfaced architect-level issues a Sonnet pass would have missed; this is not coincidence. Verification: each substantive prompt names its model selection in the standard Model / Mode / Effort table at top.

7. **Generate prompts referencing existing-system state without pre-flight verification.** Mandatory pre-flight protocol before designing changes to existing templates / ADRs / configs / file structures: read the live files end-to-end, read all cited ADRs in full, verify the proposed mechanism against the system's actual conventions (e.g., does the system use frontmatter or a Registry for the lifecycle pattern being modified). Recent session demonstrated N=7 verification-miss instances including a hallucinated file-mapping table for a substantive refactor prompt. The lesson is recorded in LESSONS.md; the operational mechanism is behavioral — "I'm confident" is itself the signal to verify harder, not a license to skip.

8. **Touch corp-monorepo or ai-council** files from this session. Read-only contract on child repos. Audit reports about them may be hosted here; modifications to them happen in their own sessions.

9. **Push or auto-merge** without explicit operator approval. Branches stay local; merge command stated, operator executes.

10. **Treat the 4-file bundle proposal as routine refactoring.** It is methodology change, not hygiene. If the Council debate (Directive 1, path a) concludes that a leaner bundle is justified, the resulting decision is an ADR — likely either an ADR-45 amendment re-opening the question with new evidence, or a new ADR superseding ADR-42 with explicit rationale. Either way, the deliverable is a formal decision artifact, not a template edit.

**Fallback contingencies:**

- If operator unavailable for the consolidation decision (Directive 1) → proceed directly to Directive 2 (scrum-master codification); defer the consolidation question to its own session, do not attempt unilateral resolution.
- If AI Council is not invokable in this session (operator constraints, model availability, etc.) → defer all Council-requiring decisions and execute mechanical / hygiene work (directives 5, 6, 9). Do not approximate Council deliberation by single-model reasoning for architectural decisions.
- If the verification-miss pattern recurs in this new session — premature closure declarations, factual claims contradicted by repo state, hallucinated structure, reactive patching instead of architectural thinking — flag a handoff opportunity per established triggers (chat > 40 messages combined with measurable quality degradation signals). Do not push through silently; the cost compounds.
- If scope cannot complete in a single session → end-of-session handoff via the validated 12-file bundle process. Do not invent shortcut variants; the bundle structure is what carries Self-Containment.
