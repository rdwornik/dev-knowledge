# Stage 2 Response: ai-council (session-sync)

<!-- scope: meta -->

| Field | Value |
|---|---|
| Repo | ai-council |
| Type | session-sync |
| Slug | `2026-05-17-ai-council-session-sync` |
| Timestamp | 2026-05-17 |
| Status | AWAITING ARCHITECT RESPONSE |

<!--
ROB — INSTRUCTIONS:

1. Open the EXISTING (OLD) browser chat for ai-council (the one being wrapped up).
2. Copy the paste block from stage1-question.md (from PASTE_BOUNDARY to end of file).
3. Paste into the old chat. Wait for its response.
4. Replace EVERYTHING below the "═══ REPLACE EVERYTHING BELOW THIS LINE ═══" marker
   with the old chat's response. Save this file.
5. Return to Claude Code in .dev-knowledge and say: "complete handoff for ai-council"

Option B: paste the response into Claude Code and say:
  "save this response as stage 2 for 2026-05-17-ai-council-session-sync"

Do NOT modify anything above the marker.
-->

═══ REPLACE EVERYTHING BELOW THIS LINE ═══

### 1. OBJECTIVE

This section assumes zero prior session knowledge.

The next session should add research-mode guidance to the Council debate question guide at `docs/council-question-guide.md`. There is a recurring failure: questions intended for the Council's `research` mode are being formulated the same way as ordinary decision questions (`pick` / `judge`), which yields shallow opinion where an evidence survey was needed. The guide currently covers `research` mode in a single mode-selection table row — too thin to correct the pattern.

This is the highest-value next action: it is a recurring, active quality problem affecting how every research debate is framed, and the fix is a self-contained, single-file documentation change.

Second priority: create `AGENTS.md` at the repo root — a required tool-agnostic governance file, distinct from the Claude-Code-specific `CLAUDE.md`, currently absent. This is a real governance-compliance gap, but a latent one, where the research-mode problem is actively recurring.

Lower priority: ADR-38 Scale M governance-file compliance verification; LESSONS.md scope-tag backfill (advisory only).

### 2. REALITY

This section assumes zero prior session knowledge.

**Scope of this chat's direct knowledge.** This architect chat witnessed an earlier arc of ai-council work and, most recently, the identification of the research-mode question-formulation problem described below. This chat did NOT witness the most recent repository session — the documentation-simplification work visible in the commit log at handoff.

**Reliability bound (important for the receiving chat).** This chat's witnessed knowledge of repository state predates the current HEAD by at least one full session; the documentation-simplification commits were not observed here. The BACKLOG provided in the bundle is current and is the authoritative source of open items — trust it over any recollection-based claim in this section.

**Present problem — research-mode question formulation.** Witnessed in this session: chats authoring Council debate questions consistently mis-formulate `research`-mode questions, structuring them like ordinary `pick`/`judge` decision questions. The result is shallow opinion instead of an evidence survey. Root cause: `docs/council-question-guide.md` gives `research` mode only a single table row — no recognition test (how to tell a question is research-mode) and no formulation rules (how to write one). A corrective guide section was drafted in this session and is available as a separate artifact for the operator to provide to the next session.

**Most recent session specifics, in-flight items, technical debt.** Unknown — not witnessed; verify against repo.

**docs/HANDOFF.md flat file status.** Unknown. The commit log shows removal of the docs/handoffs/ directory, a distinct artifact from a flat `docs/HANDOFF.md` file at repo root. Current existence must be verified against the repo.

### 3. RATIONALE

This section assumes zero prior session knowledge.

**Research-mode guide work (witnessed).** The research-mode formulation problem was identified as a recurring pattern, not a one-off: given a question whose correct answer requires surveying external evidence, chats default to the decision-question structure. The chosen fix is a guide section rather than a change to Council runtime behavior, because the failure is upstream of the Council run — it is in how the question author frames the question file. The drafted section is built around three parts: a recognition test (research mode is identified by the output wanted — a survey of what the field knows, versus a decision for the asker's specific situation), formulation rules specific to research questions, and a caution against breadth-over-depth in research debates with many sub-questions.

**Most recent documentation-simplification session.** Unknown — no rationale witnessed in this session for which items were included versus deferred in that scope, nor for decisions about AGENTS.md, LESSONS.md scope-tag backfill, or docs/HANDOFF.md deprecation. Stage 3 should verify against the relevant commits and architecture decision records.

### 4. DIRECTIVES

This section assumes zero prior session knowledge.

1. **Add a research-mode section to `docs/council-question-guide.md`.** The section must cover three things: (a) a recognition test — a `research`-mode question is identified by the output wanted: a survey of what the field, industry, or literature knows (which the asker then applies), versus a decision for the asker's specific situation (`pick`/`judge`/`ideas`); (b) formulation rules specific to research questions — the headline asks what the field knows rather than what the asker should do, options are evidence-testable candidate approaches (name real systems where possible) rather than choices to reason between, and source-corpus constraints (recency windows, excluding marketing material) are valid; (c) the breadth-over-depth trap — research questions with more than three sub-questions should be split or explicitly instructed to prioritise the best-evidenced positions. Place the section after the existing mode-selection table. A drafted version exists and can be provided by the operator to avoid re-drafting; the section can also be written fresh from the three-part specification above. Verify: section present in the guide, covers the three parts, commit recorded.

2. **Create `AGENTS.md` at the repo root.** Cover cross-tool LLM agent governance; the required scope is defined by the ecosystem PLAYBOOK and the cited ADR essence in the bundle. If creation requires decisions this chat cannot supply — which tools are in scope, what authority the file carries relative to `CLAUDE.md` — pause and surface to the operator rather than inventing the spec. Verify: file exists at repo root and covers the cross-tool scope defined by the ecosystem standard.

3. **Verify the header-normalizer pre-commit hook runs clean on current repo state.** Verify: `pre-commit run --all-files` exits 0 with no normalizer errors. If it fails, diagnose root cause before other work.

4. **Confirm ADR-38 Scale M governance-file compliance.** Verify the required root governance files are present (architect inference: LESSONS.md and BACKLOG.md among them; the ADR-38 essence in the bundle defines the exact set). Verify: file presence matches the ADR-38 Scale M mandate; flag any gap.

5. **Determine `docs/HANDOFF.md` status.** Check whether a flat `docs/HANDOFF.md` file exists at repo root (distinct from the docs/handoffs/ directory already removed). If present, deprecate or remove it consistent with the handoff-centralization decision. Verify: file absent, or explicitly marked legacy.

6. **Backfill scope tags in LESSONS.md entries (advisory).** Insert the scope-tag field into existing entries to satisfy the lessons-format check. Verify: entries carry the scope tag; no existing entry content altered beyond the tag insertion.

### 5. BOUNDARIES

This section assumes zero prior session knowledge.

- Do NOT treat this chat's REALITY or RATIONALE as a complete picture of recent work — this chat's witnessed knowledge predates the current repo HEAD by at least one session. The BACKLOG in the bundle is the authoritative source of open items.
- Do NOT change Council `research`-mode runtime behavior as part of the guide work — the research-mode fix is a documentation change to how question authors frame questions, not a change to how the Council processes them.
- Do NOT generate reconciliation reports or directives about other repos' state — this session is scoped to ai-council only.
- Do NOT amend the architecture decision records governing the recent documentation simplification without a dedicated Council debate — that scope was a deliberate decision and amending it requires equivalent deliberation.
- Do NOT alter existing LESSONS.md entry content when backfilling scope tags — dated entries are append-only; the scope tag is metadata and its insertion must preserve existing entry text.
- Do NOT invent an AGENTS.md specification if its scope requires cross-repo decisions — surface to the operator instead.
- If the pre-commit hook fails on current repo state: diagnose root cause before proceeding; do not skip hooks or modify the normalizer script without operator awareness.

**Fallback contingencies:**

- If the operator does not provide the drafted research-mode section: it can be written fresh from the three-part specification in Directive 1 — Directive 1 does not depend on the draft.
- If AGENTS.md cannot proceed because its specification needs operator input: continue with the remaining directives, which are self-contained.
- If repo state shows the work in a directive already complete: treat that directive as verification-and-report.
