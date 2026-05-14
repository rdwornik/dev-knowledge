# State of Play — .dev-knowledge (session-sync) 2026-05-14

<!-- scope: meta -->

---

## What was completed this session

The following work was completed and committed culminating in HEAD `ef7f66e` (with Stage 1 commit
at `ef7f66e` and prior session work in the lineage below):

**HANDOFF_PROCESS.md amended v3.3 → v3.3.1 (commit 556c8e1):**
Amendment added an Audience Awareness section to `HANDOFF_QUESTION_TEMPLATE.md` (the Stage 1
template). The amendment adds seven rules instructing the OLD chat to write Stage 2 responses for
the *new chat audience* that never sees Stage 1, plus a verification self-check appended to the
submit list. The seven rules address seven empirically observed gap patterns: self-referential
meta-framing, Stage 1 references, forward references without inline content, invisible
session-history references, in-flight work references, cross-reference burdens, and external
research citations. v3.3.1 scope is Stage 1 template only — no flow change, no new mechanism,
no escalation of the articulation gate in `00_first-message.md`.

**Council research transcript committed (commit 2f944a8):**
A three-model panel (Perplexity, Grok, Gemini; OpenAI Mini errored) reviewed the cross-session
handoff format. The transcript was committed to `docs/decisions/transcripts/`. Estimated cost ~$0.37,
duration 8m 43s, 81 sources. See RATIONALE for signal vs noise assessment.

**Stage 1 question regenerated under v3.3.1 (commits 8663a7c + ef7f66e):**
The stale v3.3 Stage 1 question was cleared and regenerated under v3.3.1 conventions. The new
`stage1-question.md` contains the full Audience Awareness section.

**Prior session lineage (same branch):**
- Four LESSONS promoted to ESSENTIALS invariants #1, #2, #6, #8 (epistemic markers, completion
  verification, validation routing, artifact generation direction) plus channel-discipline rule
  added directly from LESSON #10 (commit 0ae143e merged at 4cf2d9d).
- HANDOFF_PROCESS.md v3.3 minimum refinement merged (commit 4cf2d9d): plain-English section
  names in downstream 06/07 files, first-reference code glosses for status codes, Hard Constraints /
  Narrow Scope split for DO-NOT lists, mandatory articulation gate in `00_first-message.md`,
  ADR-45 demoted Accepted → Superseded.

---

## Current state

- **HEAD:** `ef7f66e623f43646d30df9b08b372e16ffa93947`
- **Branch:** `docs/2026-05-14-dev-knowledge-session-sync-stage1`
- **Working tree:** clean (Stage 3 commit includes stage2-response.md)
- **ESSENTIALS.md line count:** 323 lines (Stage 3 verified — architect had flagged as Unknown with estimates of 226 or 324; 323 is confirmed)
- **Handoff cycle status:** Stage 3 complete — bundle in `docs/handoffs/2026-05-14-dev-knowledge-session-sync/`
- **PLAYBOOK Section 8:** Stale (2026-04-28) — explicitly marked in file; points to HANDOFF_PROCESS.md as authority. Increasingly out of sync post-v3.3.1 amendment. Addressed via Stream C P1 PLAYBOOK additions BACKLOG entry.

---

## Decisions locked this session

**v3.3.1 scope decision:** Scope is template amendment only (Stage 1 template), not v3.4 escalation.
The articulation gate in `00_first-message.md` remains passive paraphrase per v3.3. This scope was
correct because: no flow change, no new mechanism — just rules enforcement for what the OLD chat
was supposed to do implicitly. For v3.4 to be warranted, empirical results from v3.3.1 must show
that audience-aware Stage 2 text still fails to close the internalization gap in the new chat.

**Council research weighting:** Concept-level signal is valid (theory-of-mind framing under context
saturation; active recall > passive paraphrase; self-containment as basic technical-writing principle).
Specific citation evidence is partially hallucinated. The research is useful for theoretical
reinforcement, not authoritative citation. See RATIONALE for full assessment.

**ADR-45 status:** Demoted to Superseded. Its 9-step migration plan was never tracked in BACKLOG and
is now moot; no BACKLOG cleanup required.

---

## Work in progress not yet captured

**Five primary failure patterns observed during extended session — NOT yet in LESSONS.md:**

1. **Documentation conflation** — architect treats decision ratification (ADR merged, lessons archived)
   as equivalent to operational change. Empirical pattern: ADR-45 v1 was marked Accepted on main
   while zero of its 9 migration steps had executed; handoff tool behavior was unchanged.
2. **Propose-then-verify pattern** — architect proposes architecture from inference about file/folder/
   convention state rather than from Witnessed grounding via actual file reads. Surfaced when operator
   file uploads revealed proposals were misaligned with actual repo content.
3. **Over-conclusion on open questions** — architect treats audit's marked "open questions" as
   established failures and builds proposals around fixing them. Example: ADR-45 v1's "60% bloat"
   headline rested on the audit's open question about bundle weight in practice, treated as if measured.
4. **Internalization-vs-delivery** — a file's presence in the handoff bundle does not guarantee the
   architect internalizes its content. Empirical case: VISION.md was in the bundle yet had to be
   uploaded twice during the session because the architect was operating without role guidance
   internalized.
5. **Role grounding via VISION** — meta-cause underlying the four above. An architect that doesn't
   internalize VISION doesn't know its role in the ecosystem, drifts to work from later phases when
   current phase isn't done.

**Three secondary observations:**
6. **Iterative file-load pattern** (operator loading files one-message-per-cluster) empirically
   grounds architect understanding faster than a bundle dump.
7. **Archive value of 08_TREE.txt is distinct from regeneration value** — operator paste-to-architect
   during debug is a real use case that the "it's regenerable" critique misses.
8. **Over-agreement under pressure as defensive sycophancy** — architect should hold position when
   challenged; concession without verification is sycophancy disguised as agreeableness.

These eight observations are captured for LESSONS.md in directive #2.

---

## Deferred items

Open BACKLOG items are tracked in `BACKLOG.md`. Relevant open items for this session:

- **[P1] PLAYBOOK content additions for ADRs 36/37/40/41** — methodology debt since 2026-04-30
- **[P1] Audit tool P1 implementation** — build `.dev-knowledge` audit tool per ADR-36
- **[P2] Lessons activation P1 implementation** — lessons-index.json + retrieval hook + CLI per ADR-35
- **[P2] ESSENTIALS.md cheat-sheet additions for ADRs 35-41** — under 1-page constraint requires pruning decisions
- **[P3] ADR-39 amendment** — add BACKLOG.md lifecycle entry
- **[P3] ADR-39 registry decision** — 5 unregistered template files

---

## Rationale (architect judgment)

**Why v3.3.1 was scoped as template amendment, not v3.4:**
Same conceptual frame as v3.3 (template-level discipline for self-containment), extended to the
upstream Stage 1 template. v3.3 had explicitly excluded Stage 1 template from refinement scope —
v3.3.1 corrects that scope error. Escalation paths if v3.3.1 is insufficient after empirical
measurement: grounded Q&A gate (specific questions with right/wrong answers tied to bundle text),
simulation gate (apply Hard Constraint X to scenario Y), or Stage 3 LLM-as-judge auditor. Each
adds complexity. Test minimum first.

**Council research signal vs noise:**
Real signal: theory-of-mind framing under context saturation; active recall over passive paraphrase;
self-containment as basic technical-writing principle. These concepts are valid regardless of citation
quality. Noise: some arxiv IDs in non-standard format suggesting LLM-fabricated references;
convergence of three models partly attributable to question framing that pre-enumerated the seven
gaps (anchored framing is not independent validation); one vendor blog (mem0.ai) cited with visible
commercial bias; one model (Gemini) recapitulated the ADR-45 v1 direction of dropping full invariants
from the bundle — that direction was empirically rejected because the full 11-file bundle's drift
detection caught a real architect fabrication in the 2026-05-09 ai-council handoff (Grok model-string
vs timeout case, per the 2026-05-12 audit). How to weight: useful for concept-level reinforcement
and theoretical framing; not authoritative as research citation.

**BACKLOG priority decision (this session):**
PLAYBOOK additions take priority over Audit tool P1 for the next session because: PLAYBOOK is
documentation-shaped work (one file, additions to existing structure, low context-load per directive),
while Audit tool is code-shaped work (multiple files, design decisions, requires its own dedicated
session). PLAYBOOK additions also close the methodology gap that ADR-36 codifies — PLAYBOOK must
reflect the audit tool workflow before Audit tool implementation begins.

---

## Stage 3 verification summary

Architect provided **witnessed** claims classified as follows:
- **7 verified against repo state:** commit 556c8e1 exists (HANDOFF_PROCESS v3.3.1 amendment); commit 2f944a8 exists (Council transcript); commit 8663a7c exists (stale Stage 1 cleared); commit ef7f66e exists (Stage 1 v3.3.1); PLAYBOOK Section 8 stale marker verified (reads "Stale (2026-04-28)"); ESSENTIALS.md line count 323 (architect flagged Unknown with estimates 226/324; Stage 3 measured 323); stage2-response.md populated with substantive content.
- **3 unverifiable from repo (conversation history):** The five primary and three secondary failure patterns are observed in-session events; cannot verify from repo state.
- **2 architect-flagged inferences (preserved):** Council research signal assessment; PLAYBOOK v3.3.1 out-of-sync characterization.
- **1 architect-flagged unknown resolved:** ESSENTIALS.md line count — Stage 3 verified: 323 lines.
- **0 verification failures:** No witnessed claim contradicted by repo state.
