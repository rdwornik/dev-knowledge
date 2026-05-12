# Action Plan — 2026-05-12-ai-council-session-sync

<!-- scope: meta -->

Source: Stage 2 OBJECTIVE + DIRECTIVES + BOUNDARIES (architect response from OLD chat).

---

## OBJECTIVE

The next ai-council session's highest-priority action is **Step 5 smoke test execution**
(operator-driven) — score current Gemini synthesizer on ~15 recent debate transcripts
per `docs/synthesis-quality-rubric.md` to determine whether synthesizer refresh is
justified or current configuration meets the bar at lower cost. This unblocks Step 6
(Phase 3 conditional ADR-01 amendment codifying the cost-optimization principle).

If next session is architect-focused rather than operator-focused: there is **no
actively-blocked architect work**. AGENTS.md addition (P3, deferred) is the only
carryover backlog item attributable to this session. The .dev-knowledge BACKLOG items
shown require reconciliation against actual ai-council state before any are executed —
most P1/P2 items are already complete.

**Finish:** Step 5 smoke test (small, mechanical scoring exercise; unlocks Step 6)
**Defer:** AGENTS.md (low urgency; bundle with future maintenance pass)
**Defer:** ARCHITECTURE.md (optional at Scale M per ADR-38; CLAUDE.md Architecture section serves equivalent purpose unless scale escalates to L)

---

## DIRECTIVES

**⚠️ CRITICAL:** The default BACKLOG proposal in this handoff (ADR-34 CLI migration,
BACKLOG.md creation, LESSONS.md addition, etc.) is **stale** — these are already done.
See BOUNDARIES and 06_STATE_OF_PLAY.md verification summary before acting.

1. **Reconcile .dev-knowledge BACKLOG against ai-council actual state.**
   Cross-check each P1/P2 BACKLOG item against ai-council git log + current file state;
   produce reconciliation report flagging which items are already complete (most), which
   remain open (AGENTS.md, codify scrum-master review authority N=2 trigger).
   Verify: reconciliation artifact produced and routed back to .dev-knowledge browser
   chat for BACKLOG cleanup.

2. **Step 5 smoke test execution** (operator-driven).
   Score CURRENT Gemini synthesizer output on ~15 recent debate transcripts in `output/`
   per `docs/synthesis-quality-rubric.md` 5-point checklist. Aggregate pass rate per
   criterion.
   Verify: scoring artifact captures per-transcript pass/fail per criterion; aggregate
   decision (≥80% pass → no flip recommended; <80% → cost-tier escalation triggered).

3. **Step 6 Phase 3 conditional implementation** (gated on Step 5 data).
   If Step 5 passes: formal Claude Code prompt for ADR-01 amendment recording Council
   debate + smoke test data + **cost-optimization principle codified** ("synthesizer
   selection prefers lowest-cost model meeting quality rubric; Opus tier reserved for
   last resort"). If Step 5 fails: separate escalation test session in cost order
   (Sonnet → GPT → Opus).
   Verify: ADR-01 amendment merged; cost-optimization principle present in governance
   docs; .dev-knowledge BACKLOG P1 entry closed.

4. **AGENTS.md addition** (P3, BACKLOG-tracked).
   Reference ADR-28 + PLAYBOOK AGENTS.md template (.dev-knowledge has the template at
   `templates/AGENTS-md-template.md`). Low urgency; bundle with future maintenance cycle
   or do standalone in light session.
   Verify: file present at root; canonical cross-tool governance points to it (Codex,
   Cursor, Aider operating contexts referenced).

5. **Push to origin** (operator timing decision).
   ~74 commits ahead at handoff (architect inference: number grows each session; backup
   risk grows with it).
   Verify: `git push` to remote; commits-ahead count drops to 0.

*(Architect inference on directive 1 reconciliation format: likely a simple markdown
artifact routed via paste-back to .dev-knowledge. Stage 3 has not located a specific
format requirement — architect judgment call.)*

---

## BOUNDARIES

**Do NOT:**

- Execute .dev-knowledge BACKLOG items as written without first reconciling against
  ai-council actual state — most P1/P2 items are stale (ADR-34 CLI migration,
  BACKLOG.md creation, LESSONS.md addition, HANDOFF.md flat file deletion, `_archive`
  rename) **ALREADY DONE** this session
- Force synthesizer flip to Claude Opus 4.7 based on Council debate alone — Council
  recommendation had cost-optimization blind spot caught mid-session by operator;
  smoke test (Step 5) must be cost-tier-aware (test current first; escalate only if
  needed in cost order: Sonnet → GPT → Opus as last resort)
- Codify any cross-repo handshake protocol requiring >1 round trip — operator principle
  established this session: well-formed requests close in one round
- Defend "local config" or "by-design per CLAUDE.md" as justification when convention
  divergence is flagged — Lesson A applies symmetrically to architect; default response
  must be "evaluate against ecosystem baseline"
- Create artifacts following 4-turn cross-repo protocol — superseded by single-round-trip
  principle
- Generate Turn 4 delivery reports for routine cross-repo cycle completion — git log +
  CHANGELOG = sufficient audit trail
- Push to origin without explicit operator authorization
- Touch files in `.dev-knowledge` repo from ai-council architect role (boundary discipline:
  ai-council work in ai-council; .dev-knowledge work routes via artifacts to .dev-knowledge
  browser chat)
- Add timeline qualifiers to recommendations ("this week," "next session," "end of day,"
  "heavy-work window")
- Pre-emptively flag context degradation based on message count rather than measurable
  quality issues
- Skip Codex `/review` on formal-prompt-scale PRs (3+ files per Playbook §15)
- Use UPPERCASE letters in any new filenames — ADR-34 = lowercase + hyphens; ADR prefix
  grandfathered. Architect's own fresh violation (`SYNTHESIS-QUALITY-RUBRIC.md`) is
  empirical evidence the convention is easy to slip; double-check during prompt drafting
- Combine ADR amendment work with feature shipping in same prompt without clear section
  separation
- Treat any .dev-knowledge methodology proposal as ai-council work — those route to
  .dev-knowledge browser chat

**Fallback contingencies:**

- If Step 5 smoke test scores are inconclusive (e.g., ambiguous quality, pass rate near
  threshold): expand sample size (30 transcripts instead of 15) before escalating
- If Codex `/review` surfaces a blocker requiring `.dev-knowledge` input mid-implementation:
  opens new cross-repo conversation; not part of single-round-trip cycle
- If new feature work surfaces ADR drift mid-PR: invoke ADR audit step inline; architect
  judgment call until .dev-knowledge decision on methodology proposal
- If .dev-knowledge BACKLOG reconciliation surfaces disagreement: produces a new cross-repo
  conversation; do not auto-resolve unilaterally
- If operator declares scope creep mid-session: stop, summarize completed work, propose
  handoff or scope contraction

---

## Success criteria

- Step 5 smoke test complete with scoring artifact
- If Step 5 fails: escalation path decided (Sonnet tested next)
- If Step 5 passes: ADR-01 amendment drafted or merged
- BACKLOG reconciliation artifact routed to .dev-knowledge
- Working tree clean; tests passing
