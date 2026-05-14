# Action Plan — ai-council (session-sync, 2026-05-14)

<!-- scope: meta -->

Next session goal, directives, and boundaries for ai-council.
Derived from Stage 2 architect response (OBJECTIVE + DIRECTIVES + BOUNDARIES).

---

## Next session goal

The next session closes a governance gap in ai-council's ADR documentation. The
highest-value item is operational: score the current default synthesizer (Gemini)
against the synthesis quality rubric to determine whether a synthesizer refresh
is empirically justified. This scoring exercise unblocks codification of a
cost-optimization principle — synthesizer selection prefers lowest-cost model
meeting the quality rubric; higher-cost tiers reserved for cases where lower
tiers fail — into ADR-01 [synthesizer selection]. The principle exists in
`LESSONS.md` but is not yet codified in any ADR.

A governance cluster provides parallel work: AGENTS.md addition (cross-tool LLM
agent governance per PLAYBOOK), ADR-38 [universal repo architecture] Scale M
compliance spot-check, and hyphen-only filename compliance verification. If
operator engagement for the manual scoring exercise is not immediately available,
these governance items are quick wins that can fill the session.

---

## Action plan

Each action: **action verb + target + verification step.**

1. **Score current default synthesizer against synthesis quality rubric.**
   Operator-driven manual scoring exercise. Select approximately 15 representative
   recent debate transcripts from `output/`. Apply the 5-point checklist in
   `docs/synthesis-quality-rubric.md` (position representation, no hallucinated
   consensus, scannability, faithfulness, verbosity proportionality) to each
   transcript's synthesis section. Aggregate per-criterion pass rate.
   *Verify: scoring artifact produced (markdown table format recommended);
   aggregate decision documented (≥80% pass per criterion → no synthesizer
   refresh recommended; <80% → escalation testing required in cost order).*

2. **Amend ADR-01 to codify cost-optimization principle (gated on Directive 1).**
   Formal Claude Code prompt for ADR-01 amendment. Amendment text: synthesizer
   selection prefers lowest-cost model meeting synthesis quality rubric; higher-cost
   tiers (Sonnet → GPT → Opus, in cost order) are reserved for cases where lower
   tiers demonstrably fail the rubric. If Directive 1 indicates current default
   fails rubric, run escalation testing first and include the chosen tier.
   *Verify: ADR-01 amended in `docs/decisions/`; principle text searchable;
   BACKLOG entry for cost-optimization codification closed; CHANGELOG entry recorded.*

3. **Add AGENTS.md at repo root.**
   Reference `.dev-knowledge/templates/AGENTS-md-template.md` as scaffold.
   Operator delivers template content as artifact if not directly accessible.
   Cover: cross-tool LLM agent governance (Codex, Cursor, Aider), project
   context, do-not lists for AI agents. Mark sections "Unknown — operator
   confirms" where specifics are unclear; do not fabricate governance rules.
   *Verify: file present at root; references `CLAUDE.md`; covers required
   cross-tool surfaces.*

4. **Spot-check ADR-38 [universal repo architecture] Scale M compliance.**
   Run `git ls-files | grep -E '^(BACKLOG|LESSONS|VISION|README|CHANGELOG|JOURNAL)\.md$'`.
   Confirm all six files present at root. `ARCHITECTURE.md` absence is expected
   at Scale M (optional; `CLAUDE.md` Architecture section serves equivalent purpose).
   *Verify: command output matches expectation; document any drift.*

5. **Spot-check hyphen-only filename compliance.**
   Run `git ls-files | grep -E '_[A-Z]+'` filtered to `docs/` and `src/`. Flag
   any UPPERCASE-with-underscore patterns. Exempt: ADR-prefixed files
   (grandfathered), historical transcripts (preserved pre-decision),
   `council_inbox/archive/` ISO timestamp data files.
   *Verify: no unexpected matches in scope-applicable directories; document
   any drift for follow-up.*

6. **Push to `origin` (operator timing decision).**
   Approximately 74 commits ahead at handoff (architect inference; verify via
   `git rev-list --count origin/main..main`). Backup risk grows with each session.
   *Verify: `git push origin main`; ahead count drops to zero.*

---

## Hard Constraints

- **Do NOT flip synthesizer default based on Council debate alone.** Empirical
  scoring data (Directive 1) is required. Council recommendation had a cost-blind
  spot; scoring gates the change.

- **Do NOT write to `.dev-knowledge` files from within this ai-council session.**
  ADR-36 [audit tool architecture] read-only contract is absolute. Operator
  hand-carries cross-repo artifacts if needed.

- **Do NOT push to `origin` without explicit operator authorization.**

- **Do NOT defend "local config" or "by-design per CLAUDE.md"** when a convention
  divergence is flagged — default response must be "evaluate against ecosystem
  baseline."

- **Do NOT generate reconciliation reports about other repos' BACKLOG or tracking
  state.** Do NOT treat staleness observations about another repo's tracking as an
  action item. Per ADR-41, each repo manages its own BACKLOG; cross-repo work
  flows via operator-carried routing artifacts.

---

## Narrow scope rules

- Do not modify `routing.py`, CLI configuration loading, or cross-repo routing logic — that work shipped recently and is stable.
- Do not implement a cross-repo audit tool from ai-council — that is a `.dev-knowledge` concern.
- Do not start corp-monorepo Phase 2 work from this session — separate visit after ai-council gaps are closed.
- Do not codify the scrum-master review authority pattern into a formal ADR yet — empirical grounding is N=1; await N=2 (second instance on a different repo).
- Do not recreate `docs/HANDOFF.md` — already deleted; handoffs live in `docs/handoffs/` per ADR-42.
- Do not fabricate AGENTS.md governance rules — mark Unknown sections; operator confirms.
- Do not combine ADR amendment work with feature shipping in the same Claude Code prompt without clear section separation.
- Do not skip Codex `/review` on PRs touching three or more files (PLAYBOOK section 15).
- Do not add timeline qualifiers to recommendations ("this week," "next session").
- Do not pre-emptively flag context degradation based on message count alone.
- Do not codify cross-repo handshake protocols requiring more than one round trip.
- Do not use UPPERCASE letters in new filenames — ADR-34 mandates lowercase plus hyphens (ADR prefix grandfathered).

---

## Fallback contingencies

- If Directive 1 scoring is inconclusive (pass rate near 80% threshold, or scores ambiguous across criteria): expand sample size (30 transcripts instead of 15) before escalating to higher-cost tier testing.
- If Codex `/review` surfaces a blocker requiring `.dev-knowledge` input mid-implementation: open a new cross-repo conversation (one round trip principle applies); not a continuation of routine PR completion.
- If new feature work surfaces ADR drift mid-PR: invoke ADR audit step inline; architect judgment call on whether to update affected ADRs in the same PR or capture as BACKLOG follow-up.
- If operator declares scope creep mid-session: stop, summarize completed work, propose handoff or scope contraction. Do not deepen ceremony as response.
- If AGENTS.md template at `.dev-knowledge/templates/AGENTS-md-template.md` is inaccessible to ai-council session: operator hand-carries template content as artifact; do not fabricate substitute structure.

---

## Success criteria

- Scoring artifact for Directive 1 produced; decision documented.
- If scoring triggers escalation: escalation testing complete; ADR-01 amended.
- AGENTS.md present at root with cross-tool surfaces covered.
- ADR-38 Scale M compliance confirmed (6 root files present).
- Hyphen compliance spot-check complete; drift documented or none found.
- Push to `origin` executed (if operator authorizes).
- CHANGELOG and JOURNAL updated for work done.
