# Stage 2 Response — .dev-knowledge (session-sync)

<!-- scope: meta -->

- Target repo: `.dev-knowledge`
- Slug: `2026-05-19-dev-knowledge-session-sync`
- Type: session-sync
- Stage 1 HEAD: `c4d7c8587b6d32ca68d19782009220a3daf45cd9`
- Stage 1 generated: 2026-05-19

<!--
ROB — instructions:
1. Take stage1-question.md → paste the PASTE_BOUNDARY block into the OLD
   browser chat for .dev-knowledge.
2. The old chat will respond with 5 sections (OBJECTIVE / REALITY /
   RATIONALE / DIRECTIVES / BOUNDARIES).
3. Copy that response and replace EVERYTHING below the marker line.
4. Save the file. Then in Claude Code: "complete handoff for dev-knowledge".

Alternative: in Claude Code say "save this response as stage 2 for
2026-05-19-dev-knowledge-session-sync" with the architect response in
the same turn; Claude Code will overwrite the placeholder block.
-->

═══ REPLACE EVERYTHING BELOW THIS LINE ═══

# .dev-knowledge Codemap Generator — Session Handoff

## 1. OBJECTIVE

This section assumes zero prior session knowledge.

Spec out the codemap generator + CI freshness check for the ARCHITECTURE.md canonical structural-context section, and produce ready-to-execute Claude Code prompts to build them in .dev-knowledge first. This completes the open implementation item from ADR-51 (architecture-documentation convention) and closes the ARCHITECTURE.md governance arc that ADR-51 opened and ADR-54 reinforced — the global Codex reviewer config explicitly directs Codex to read each repo's ARCHITECTURE.md for structural context, and that pointer is only as strong as ARCHITECTURE.md's freshness guarantees.

(architect inference) Why this and not another open BACKLOG item: ADR-53 and ADR-54 closed the agent-instruction-contract and Codex-tool-config concerns by establishing single canonical sources. The same anti-drift principle now needs to extend to ARCHITECTURE.md's machine-derivable parts (module list, dependency edges, layer assignments) — those should be generated, not hand-maintained, with CI catching drift. Lessons activation P1, ESSENTIALS additions for ADRs 35–41, and the ADR-38 self-compliance gap are each real but lower-leverage and less continuous with the recent arc. The codemap generator is the natural close and was explicitly named pending in ADR-51's open-item list.

Scope: spec + prompts only. Execution (building the tool) belongs in the session after this one, eating its own dogfood by running first against .dev-knowledge, then rolling out per ADR-51's size-tiered policy.

---

## 2. REALITY

This section assumes zero prior session knowledge.

Recent session arc completed. Three repos migrated to the CLAUDE.md v2.1 canonical agent-instruction contract (ADR-53); cross-repo stale-reference sweep done in live docs; ARCHITECTURE.md "known violations" list in .dev-knowledge reclassified to zero; ADR-54 authored to govern the Codex reviewer config as a global standard at ~/.codex/AGENTS.md, with the canonical source tracked at codex/AGENTS.md in .dev-knowledge and deployed to the user-home location. The global config carries the generic reviewer config (role, review checklist, output format) plus an explicit instruction to read each repo's ARCHITECTURE.md for structural context. HEAD reflects the ADR-54 merge.

No .dev-knowledge work in progress not visible at HEAD (architect inference, based on the clean working tree at Stage 1).

External dependency in play — corp-monorepo. corp-monorepo is independently retiring its own corp-monorepo/AGENTS.md on a corp-monorepo branch (the per-repo Codex config that the new global standard supersedes). This is external to .dev-knowledge's scope — the next .dev-knowledge session must not direct corp-monorepo work. The exact state of corp-monorepo's AGENTS.md at the time the next .dev-knowledge session opens is Unknown — Stage 3 should verify against the corp-monorepo repo if it matters for any downstream rollout, though for codemap-spec work it does not block.

**Constraints the next session must respect:**

- ADR-54 is just-merged — do not re-litigate. The global Codex reviewer config is the established model. Codemap generator work uses the ADR-54 model (Codex reads ARCHITECTURE.md per the global config) as a given input.
- ADR-51's size-tiered policy stands (architect inference, restating what ADR-51 mandates per the BACKLOG entry): M/L repos receive a graphical codemap; S repos (including .dev-knowledge itself) receive a text-only module overview, no diagrams. The generator must support both modes.
- .dev-knowledge is methodology, not orchestration (Layer 2 invariant). The generator is a content-producing tool — markdown out — and stays within Layer 2. Any cross-repo deployment orchestration that may emerge does not belong in .dev-knowledge.

**Unknown — Stage 3 should verify:**

- Whether .dev-knowledge already contains a partial ARCHITECTURE.md template or codemap section spec at HEAD c4d7c85, or whether the codemap section format must be authored from scratch. The first directive below resolves this gap explicitly before specification work begins.
- The exact current shape of .dev-knowledge's own ARCHITECTURE.md codemap section (or its absence).

---

## 3. RATIONALE

This section assumes zero prior session knowledge.

**Why corp-monorepo/AGENTS.md was treated as outside ADR-53's scope (Witnessed).** ADR-53 retired AGENTS.md in its role as the per-repo agent-instruction contract — the file Claude Code reads to learn how to behave in a repo — and made the CLAUDE.md v2.1 template the single canonical instruction contract for that role. corp-monorepo/AGENTS.md simultaneously served a different role: Codex's tool configuration, the file Codex reads to learn how to review. Same filename, two different tool-consumers, two different concerns. ADR-53 governed only the instruction-contract role; the tool-config role was a separate deferred concern that ADR-54 then governed.

**Why the Codex reviewer config was globalized to ~/.codex/AGENTS.md rather than left per-repo (Witnessed).** Codex's documented layering model places a global file beneath optional per-repo overrides — generic cross-project configuration belongs in the global file. The generic reviewer config (role definition, review checklist, output format) is cross-project: three per-repo copies would create exactly the drift surface ADR-53 was created to eliminate. Single source — global — removes that surface. Per-repo AGENTS.md files remain available for genuinely repo-specific review rules; whether any repo actually warrants one is a per-repo judgment rather than a fixed policy. Additionally, because Codex's project_doc_fallback_filenames mechanism loads only the CLAUDE.md fallback (not ARCHITECTURE.md), the global config carries an explicit "read the repo's ARCHITECTURE.md for structural context" instruction — that instruction is what routes Codex to the structural source, which is the load-bearing assumption for the codemap-generator work the next session will spec.

**Why the three CLAUDE.md v2.1 condensations (ADR list trimmed to last 5; scope tags reduced; per-file triggers dropped).** Unknown — no specific rationale witnessed in this session arc. Stage 3 verifies against the CLAUDE.md template doc or its originating ADR.

---

## 4. DIRECTIVES

This section assumes zero prior session knowledge.

Sequential actions for the next .dev-knowledge session. Each carries a verification step. (architect inference) Specific paths and the artifact-type choice (ADR amendment vs. sibling implementation spec) may need revision based on repo state — Stage 3 may revise.

1. **Verify the current state of the ARCHITECTURE.md canonical template in .dev-knowledge.** Read ADR-51 (in the bundle) and the template doc itself (Unknown path — locate at session open). Identify whether the codemap section format is already specified, partially specified, or absent. Verification: a one-paragraph gap statement in-session, naming which artifact holds the current template and what is missing.

2. **Author the codemap section formal spec.** Required fields (module list, dependency edges, layer assignments), canonical markdown format, size-tiered modes (S = text-only module overview, M/L = graphical codemap), and edge cases (orphan modules and circular dependencies must be surfaced, not silenced). Verification: spec doc committed to .dev-knowledge as either an ADR-51 amendment or a sibling implementation spec, per repo conventions — DIRECTIVE 1 informs the artifact-type choice.

3. **Specify the codemap generator tool.** Python per .dev-knowledge dev standards, Click CLI, input is a repo path, output is the formal codemap markdown ready for paste-or-write into ARCHITECTURE.md. Define failure modes (clear errors on missing source structure rather than silent skip). Verification: spec doc covers algorithm sketch, supported repo layouts, and edge-case handling.

4. **Specify the CI freshness check.** Pre-commit hook and/or CI workflow that re-runs the generator and fails when its output diverges from the committed ARCHITECTURE.md codemap section. Verification: spec doc covers integration points, failure messaging, and how the check is opted into per repo.

5. **Produce Claude Code prompts to build the generator and the CI check in .dev-knowledge first.** Per the standard prompt format (downloadable .md; Model/Mode/Effort table; UNDERSTAND + Plan Mode; sequential commits with verification steps; What-NOT-to-do block). Verification: prompts produced as downloadable artifacts ready to execute in a Claude Code session.

(Execution of the prompts — building the tool, then running it against .dev-knowledge's own ARCHITECTURE.md, then any cross-repo rollout — belongs in the session after this one. This session's OBJECTIVE is spec + prompts.)

---

## 5. BOUNDARIES

This section assumes zero prior session knowledge.

**Do not:**

- Do not direct corp-monorepo or ai-council work from this handoff. Cross-repo rollout (M/L graphical codemap to corp-monorepo, S text-only to ai-council) belongs in routing artifacts produced after .dev-knowledge has proven the tool against its own ARCHITECTURE.md. Per the Universal Self-Containment Rule, directives never target other repos.
- Do not re-litigate ADR-54. The global Codex reviewer config is just-merged and is the established model. Codemap generator work treats ADR-54's "Codex reads each repo's ARCHITECTURE.md" instruction as a given input; it does not re-open that decision.
- Do not introduce a new ADR for the codemap-generator spec without empirical N≥2 grounding. ADR-51 already provides the architectural cover for the architecture-documentation convention; the generator spec can live as an implementation spec, an amendment, or a sibling artifact per repo conventions. A new ADR is warranted only if a genuinely contested architectural choice surfaces during spec authoring.
- Do not edit immutable docs — ADRs (existing), transcripts, audits, handoff records.
- Do not edit append-only docs — LESSONS.md, TOKEN-LOG.md. New entries appended only.
- Do not place orchestration scripts in .dev-knowledge. The codemap generator is a content-producing tool (markdown out); it does not orchestrate cross-repo work. If cross-repo deployment scaffolding is needed, that lives elsewhere per the Layer 2 invariant.
- Do not delete content without explicit ask when touching existing template or spec docs. Condense and relocate are acceptable; removing rules or sections requires explicit confirmation.

**Fallback contingencies:**

- If DIRECTIVE 1's verification finds the template gap is not the codemap section (the template is either more complete or differently incomplete than the architect's inference): re-scope DIRECTIVE 2 to whatever the actual gap is before proceeding to generator and check spec. Do not invent a gap to fill.
- If the codemap section format proves contested during DIRECTIVE 2 (multiple defensible designs with no clear winner): pause spec authoring and route the design choice to AI Council before committing. The codemap section becomes a constraint on every downstream repo — design contest justifies the AI Council protocol.
