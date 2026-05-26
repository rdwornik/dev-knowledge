# Handoff Methodology — Council Debate Question Set 2026-05-25

> **Type:** Research artifact — index for an AI Council debate question set.
> **Status:** Prepared for operator review. NOT a methodology change. No ADR, protocol, template, or child-repo file was modified by this work.
> **Provenance:** grounded in `docs/research/2026-05-25-handoff-failures-evidence.md`.

## Why this set exists

The 2026-05-23 → 2026-05-25 session arc produced empirical evidence that the current handoff methodology (ADR-42 v3 / HANDOFF_PROCESS v3.3.3) does not reliably achieve its primary purpose — continuing work with discipline in a fresh chat — despite delivering the full bundle as specified. The failure crossed all three actors: the OLD sender chat logged N=7 verification-misses while generating prompts (including a hallucinated file-map); two separate NEW receiver chats each passed the articulation gate and then failed to operationalize the bundle one turn later (evidence file `:20-99`).

The operator's read of this is that the problem is **methodology-level and requires architectural deliberation, not incremental tuning** (evidence `:103-114`). Per the ecosystem rule "architecture decision = AI Council," this set prepares the debate inputs. Each file is one independently-decidable architectural concern, written to the discipline in `ai-council/docs/council-question-guide.md`.

## Question selection rationale

An architectural concern (in scope) is one where multiple reasonable designs exist and the choice shapes the future system. An implementation concern (out of scope) is how to operationalize a settled design; those become BACKLOG items, not Council questions.

The evidence decomposes the handoff lifecycle into seven sub-areas: (1) sender produces the bundle; (2) bundle carries content; (3) bundle is structured/delivered; (4) receiver reads and internalizes; (5) internalization is verified; (6) receiver does substantive work including prompt generation; (7) whether the abstraction is right overall. Five of these are genuinely architectural and independently decidable; they map to the five questions below. The structural sub-area (3) is folded into Q5 (delivery is the same decision as custody). The meta-abstraction sub-area (7) is carried by Q5 rather than split out as a separate mega-question — a standalone "is the handoff the right abstraction" debate would conflate the others, which the council-question-guide and this prompt both forbid; instead Q5 frames the abstraction at the delivery/custody layer, and the radical options inside Q1 (regenerate-on-failure) and Q4 (defer to executor) let the set collectively reach an abstraction-level conclusion if warranted.

**Why five and not three or four.** Each of the five admits radically different designs, each is grounded in distinct evidence, and each can be approved/deferred/modified without forcing the others. Collapsing any pair would conflate independent decisions. Two candidates were considered and **not** given their own files:

- *Standalone "is document-handoff the right abstraction" question* — dropped as a separate file because it would re-debate the components; carried inside Q5 instead (see above).
- *Standalone bundle-file-count / structural-consolidation question* — folded into Q5, because file count, full-copy-vs-pointer, and where-invariants-live are one delivery/custody decision (the ADR-45 territory), not two.

## Format note (judgment call — operator should be aware)

The originating prompt sketched a per-file template (evidence summary / hypothesis space / disambiguating signals / out-of-scope / usable-answer). The prompt also stated that where its sketch conflicts with `council-question-guide.md`, **the guide wins**. The guide's decision-mode format is: YAML frontmatter → one-sentence problem-framed `## Question` → `### Current State` (facts) → `### Questions` (A/B/C/D sub-questions) → `### Constraints` (option-eliminating). Each file therefore follows the guide's format. The prompt's extra intent is preserved as guide-compatible additions, clearly labelled for operator review: an `### Adjacent concerns` section (which sibling owns what — also aids panel scoping), an `### Evidence base` provenance block (file:line refs for verification, explicitly marked "not panel instructions"), and a `### What a usable answer looks like` note (decision form). Each file's status-quo position appears as option A in its sub-questions, and an escape option ("a different approach — panel names it") is present where the option set could otherwise be closed, per the guide's choice-set-bias rule.

## Questions (suggested debate order — operator may re-sequence)

1. **Receiver internalization assurance** — what mechanism confirms a fresh chat internalized the bundle (not just paraphrased it) before working.
   `2026-05-25-handoff-council-Q1-internalization-assurance.md`
2. **Bundle content composition** — which content types the bundle carries, and whether the set is fixed or selected per session (the PLAYBOOK/ESSENTIALS vs skills/gotchas/JOURNAL tension).
   `2026-05-25-handoff-council-Q2-bundle-content-composition.md`
3. **Procedural-competence transfer** — how prompt-generation procedure (decision algorithm, model selection, structure) reaches a fresh chat when shipping the docs has not reproduced it.
   `2026-05-25-handoff-council-Q3-procedural-competence-transfer.md`
4. **Sender-side verification symmetry** — whether verification discipline should be symmetric across actors, and who reviews the receiver's articulation.
   `2026-05-25-handoff-council-Q4-sender-verification-symmetry.md`
5. **Delivery / custody abstraction** — whether invariants and discipline stay in a self-contained document bundle or move to a stateful/harness-mediated layer (the ADR-45 reopen; carries the abstraction-level concern).
   `2026-05-25-handoff-council-Q5-delivery-custody-abstraction.md`

Suggested order rationale: Q1 and Q2 isolate the two most-cited symptoms (gate fakability, content tension); Q3 and Q4 address the sender/producer side; Q5 is last because its outcome (keep vs change the delivery abstraction) is best decided after the component debates have surfaced whether the problems are fixable within the current abstraction.

## Cross-question integrity (verified before finalizing)

- **No scope leak:** one overlap was found and fixed — Q2's "layered core + on-demand" option duplicated Q5's "condensed anchor" delivery-form option; Q2 sub-question 1 was reframed to the selection-principle axis so the delivery axis lives only in Q5 (committed separately).
- **Constraints agree:** no question debates anything another pins as fixed. The 3-stage relay is a fixed constraint in Q1/Q3/Q4 and is not debated in Q2/Q5; Q5 debates delivery *within* the relay (ADR-45 itself preserved the relay). Self-Containment and the Layer-2 no-scripts invariant are cited consistently across files.
- **Out-of-scope partition is coherent:** every concern one file defers is explicitly claimed by exactly one sibling. No orphaned concern.

## What is NOT debated in this set

- **Already-resolved hygiene** from the 2026-05-20 audit (version-string skew M-1, ADR-45 status M-2, CHANGELOG-in-Stage-3 M-3, thinness check M-5) — these were resolved 2026-05-25; not architectural.
- **Implementation tuning** — exact regex/validator syntax, specific wording of a gate prompt, etc. These become BACKLOG items after a debate sets direction.
- **The 3-stage relay itself, SHA-256 manifest, HEAD-pin, epistemic markers, filesystem state tracking** — the evidence lists these under "what's not broken" (evidence `:134-142`); they are constraints, not questions.
- **Cross-repo / workspace-template universalization** — a corp-monorepo concern surfaced in the same arc but out of scope for this handoff-methodology set; belongs to its own session/Council debate.

## Process forward

1. Operator reviews each question file; approves, defers, or modifies independently.
2. Approved questions are copied **manually** by the operator to `ai-council/council_inbox/` (this work does not write there).
3. AI Council runs each debate per its own process; transcripts return to `.dev-knowledge/docs/decisions/transcripts/` (per the `target-project: .dev-knowledge` frontmatter and evidence `:158`).
4. Each completed debate is distilled into an ADR (new ADR or ADR-45 amendment) in `docs/decisions/`, per the council-question-guide's "distil to ADR" step. Those are separate, later prompts — not part of this preparation work.
