# Action Plan — .dev-knowledge

<!-- scope: meta -->

Future State per ADR-37. Sources: Stage 2 architect OBJECTIVE + DIRECTIVES
+ BOUNDARIES answers.

## Next session goal

Spec out the **codemap generator + CI freshness check** for the
`ARCHITECTURE.md` canonical structural-context section, and produce
ready-to-execute Claude Code prompts to build them in `.dev-knowledge`
first. This completes the open implementation item from
ADR-51 [architecture-documentation convention] and closes the
`ARCHITECTURE.md` governance arc that ADR-51 opened and
ADR-54 [codex-reviewer-global-standard] reinforced — the global Codex
reviewer config explicitly directs Codex to read each repo's
`ARCHITECTURE.md` for structural context, and that pointer is only as
strong as `ARCHITECTURE.md`'s freshness guarantees.

(architect inference) Why this and not another open BACKLOG item:
ADR-53 and ADR-54 closed the agent-instruction-contract and Codex-tool-
config concerns by establishing single canonical sources. The same
anti-drift principle now needs to extend to `ARCHITECTURE.md`'s
machine-derivable parts (module list, dependency edges, layer
assignments) — those should be generated, not hand-maintained, with CI
catching drift. Lessons activation P1, ESSENTIALS additions for ADRs
35–41, and the ADR-38 self-compliance gap are each real but lower-
leverage and less continuous with the recent arc. The codemap generator
is the natural close and was explicitly named pending in ADR-51's
open-item list.

**Scope:** spec + prompts only. Execution (building the tool) belongs
in the session after this one, eating its own dogfood by running first
against `.dev-knowledge`, then rolling out per ADR-51's size-tiered
policy.

## Action plan

Each item: action verb + target + verification step.
(architect inference) Specific paths and the artifact-type choice (ADR
amendment vs. sibling implementation spec) may need revision based on
repo state — Stage 3 may revise.

1. **Verify the current state of the ARCHITECTURE.md canonical template
   in `.dev-knowledge`.** Read ADR-51 (essence in `05_GOVERNANCE_ESSENCES.md`,
   full text in repo) and the template document itself. Stage 3 located
   the template at `templates/ARCHITECTURE-template.md` (verified via
   `git ls-files`). Identify whether the codemap section format is
   already specified, partially specified, or absent. **Verification:**
   a one-paragraph gap statement in-session, naming which artifact holds
   the current template and what is missing.

2. **Author the codemap section formal spec.** Required fields (module
   list, dependency edges, layer assignments), canonical markdown format,
   size-tiered modes (S = text-only module overview, M/L = graphical
   codemap), and edge cases (orphan modules and circular dependencies
   must be surfaced, not silenced). **Verification:** spec doc committed
   to `.dev-knowledge` as either an ADR-51 amendment or a sibling
   implementation spec, per repo conventions — DIRECTIVE 1 informs the
   artifact-type choice.

3. **Specify the codemap generator tool.** Python per `.dev-knowledge`
   dev standards, Click CLI, input is a repo path, output is the formal
   codemap markdown ready for paste-or-write into `ARCHITECTURE.md`.
   Define failure modes (clear errors on missing source structure rather
   than silent skip). **Verification:** spec doc covers algorithm
   sketch, supported repo layouts, and edge-case handling.

4. **Specify the CI freshness check.** Pre-commit hook and/or CI
   workflow that re-runs the generator and fails when its output
   diverges from the committed `ARCHITECTURE.md` codemap section.
   **Verification:** spec doc covers integration points, failure
   messaging, and how the check is opted into per repo.

5. **Produce Claude Code prompts to build the generator and the CI
   check in `.dev-knowledge` first.** Per the standard prompt format
   (downloadable .md; Model/Mode/Effort table; UNDERSTAND + Plan Mode;
   sequential commits with verification steps; What-NOT-to-do block).
   **Verification:** prompts produced as downloadable artifacts ready
   to execute in a Claude Code session.

*Execution of the prompts — building the tool, running it against
`.dev-knowledge`'s own `ARCHITECTURE.md`, then any cross-repo rollout —
belongs in the session AFTER this one. This session's OBJECTIVE is
spec + prompts.*

## Hard Constraints

Critical for the next step. Violating any of these blocks the session's
primary work.

- **Do not direct corp-monorepo or ai-council work from this handoff.**
  Cross-repo rollout (M/L graphical codemap to corp-monorepo, S text-only
  to ai-council) belongs in routing artifacts produced AFTER
  `.dev-knowledge` has proven the tool against its own `ARCHITECTURE.md`.
  Per the Universal Self-Containment Rule in `03_PLAYBOOK.md`,
  directives never target other repos.
- **Do not re-litigate ADR-54.** The global Codex reviewer config is
  just-merged and is the established model. Codemap-generator work
  treats ADR-54's "Codex reads each repo's `ARCHITECTURE.md`" instruction
  as a given input.
- **Do not introduce a new ADR for the codemap-generator spec without
  empirical N≥2 grounding.** ADR-51 already provides the architectural
  cover for the architecture-documentation convention; the generator
  spec can live as an implementation spec, an amendment, or a sibling
  artifact per repo conventions. A new ADR is warranted only if a
  genuinely contested architectural choice surfaces during spec
  authoring.

## Narrow scope rules

Scope refinements — important, but not blocking primary work.

- Do not edit immutable docs (existing ADRs, transcripts, audits,
  handoff records).
- Do not edit append-only docs (LESSONS.md, TOKEN-LOG.md). New entries
  appended only.
- Do not place orchestration scripts in `.dev-knowledge`. The codemap
  generator is a content-producing tool (markdown out); it does not
  orchestrate cross-repo work. If cross-repo deployment scaffolding is
  needed, that lives elsewhere per the Layer 2 invariant.
- Do not delete content without explicit ask when touching existing
  template or spec docs. Condense and relocate are acceptable; removing
  rules or sections requires explicit confirmation.

## Fallback contingencies

- **If DIRECTIVE 1's verification finds the template gap is not the
  codemap section** (template is either more complete or differently
  incomplete than the architect's inference): re-scope DIRECTIVE 2 to
  whatever the actual gap is before proceeding to generator and check
  spec. Do not invent a gap to fill.
- **If the codemap section format proves contested during DIRECTIVE 2**
  (multiple defensible designs with no clear winner): pause spec
  authoring and route the design choice to AI Council before committing.
  The codemap section becomes a constraint on every downstream repo —
  design contest justifies the AI Council protocol.

## Success criteria

- DIRECTIVE 1: gap statement committed to a session note or scratchpad,
  unambiguously identifying current template state.
- DIRECTIVES 2-4: spec doc(s) committed to `.dev-knowledge` covering
  codemap section format, generator tool design, and CI freshness check.
- DIRECTIVE 5: Claude Code prompt(s) produced as downloadable .md
  artifacts, ready to paste into a subsequent Claude Code session in
  `.dev-knowledge`.
- BACKLOG entry "Codemap generator output specification (ADR-51 open
  item)" can be updated from `open` to `spec complete — execution
  queued` (or the spec-and-prompts equivalent).
- No cross-repo content in any committed artifact (Universal
  Self-Containment Rule).
