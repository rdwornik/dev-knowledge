# ADR-82: HANDOFF_PROCESS v5 — CC-owned, primary-source-forced handoff (model C)

- **Status:** Proposed
- **Date:** 2026-06-11
- **Related:** ADR-62 (v4 handoff ratification — superseded by v5 *at promotion to canonical*, not now); ADR-79 (browser carrier bundle-only — v5's thin boot supersedes the heavy-bundle delivery it mandated, at promotion); ADR-28 (three-layer model — v5 inverts who *initiates*, not the layer invariants); ADR-41 (cross-repo decision routing — the Council route this ADR is pending on); #148 (the v5 redesign item), #124 (BUNDLE.md consolidation — superseded by the thin boot), #25 (deferred .tmpl refinements), #145 (codification-completeness — the pointer-integrity dependency)
- **Decommission:** none active while **Proposed**. On promotion to canonical (the Council-gated flip, tracked by the named successor backlog item), the following are decommissioned: (1) `templates/handoff/*.tmpl` → archived to `templates/archive/handoff-v4/`; (2) the 8-file teaching-bundle generation path in `/handoff`; (3) `audit.py` checks #8 `handoff_bundle_structure` / #9 `handoff_tag_canonicity` scoped/retargeted to historical v4 bundles. Nothing is removed by this ADR in its Proposed state.
- **Source:** Rob's decision, 2026-06-11 (CC prompt implementing model C); architecture routed to AI Council per #148 / ADR-41 — this ADR is the decision record Council ratifies before the flip.

<!-- Decommission: deferred to promotion — see Source; nothing active while Proposed. -->

## Context

The v4 handoff (current v4.4, `protocols/HANDOFF_PROCESS.md`) treats a handoff as onboarding a new chat with a heavy 8-file teaching bundle, pasted into a fresh browser chat. The 2026-06-10 LESSONS entry diagnosed the load-bearing failure: a handoff that *points* at the methodology but does not *force* the receiver to open it lets the new session work from the lossy in-context **compaction summary** — a SECONDARY source — instead of the methodology files on disk (the PRIMARY source). The v4 comprehension questions are answerable from the bundle itself, so the forced-read is vacuous: "fake-green, like a test that passes without the behavior." The bundle also re-transmits methodology already encoded in the repo, which drifts from its source (the proven `/review` vs `/codex review` drift class).

Three forces motivate a redesign (#148): (a) the forced primary-source read needs **teeth** — verification whose answer exists only in the live primary file/state, not bluffable from a summary; (b) task-state should be a **lean pointer** to the BACKLOG (the spec; items are tickets), not re-narrated IDs; (c) `/handoff` should be **self-updating** — always pull the current process + methodology pointers, never hand-copy.

The three-layer model (ADR-28) is unchanged in its invariants (Layer 2 never executes; execution one-way). What changes is *who initiates*: the browser (Layer-1 architect) has no file access; CC (Layer-3) holds repo state. Making the browser assemble and verify a handoff inverts the natural information gradient.

## Decision

Adopt **model C: CC owns and initiates the handoff; the browser is a thin reactive partner.**

- **CC generates the handoff from inside the repo** and emits only the **residual** — un-committed session reasoning, pointers (paths), and **drift-flags where reality and the written record disagree (the headline, not an afterthought)**. It runs the existing read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus its state read; it does **not** re-transmit methodology or state the repo already encodes.
- **A thin browser boot (~3-line core) replaces the heavy multi-file bundle:** identity ("critical architect; CC is your junior"), one meta-rule ("do not act unilaterally on anything methodology governs — route through CC or ask"), first-move ("read CC's handoff"). The browser's **operating role travels with the boot** (resident, not left only in a CC-held file) so it cannot silently fail to arrive. Everything else is pulled just-in-time via CC.
- **Methodology is enforced mechanically** (hooks / checks / skills) and referenced thinly — never re-stated as prose per session. Heavy *enforcement*, thin *prose*.
- **The teeth-y forced primary-source read** is a probe manifest whose answers exist only in live state — built from the existing read-only validators (`audit.py checks`, `validate_doc_claims`, `validate_git_backlog`) plus quote-grounded probes against live primary files. CC runs the probes at the comprehension gate; a probe answerable from the compaction summary is, by construction, excluded. The empirical proof that the teeth bite (bluff each probe from the summary; all must fail) is a promotion gate, not a review opinion.
- **Browser role:** reactive partner + filter over CC's output (surface only errors and decisions needing human judgment, keeping the operator at feature/epic/user-story level) + research + exception-handler + launch-config support **for genuine forks only** (routine model/effort/autonomy is handled by CC's own opusplan and auto mode; the browser does not review routine plans). The browser's plan-review output is constrained to **one of three forms** — the exact CC option to select, exact paste-ready English feedback, or a plain "approve" — never prose the operator must translate into CC actions.
- **Verification split:** the browser verifies the handoff *artifact* (internal coherence + alignment with architectural intent — file-free, fresh-eyes); CC verifies *state fidelity* (claims vs live disk/git). Each checks what it is positioned to check.
- **Adjudication is bidirectional:** the browser corrects CC's errors AND pulls missing context — not one-shot.

**Rollout is parallel-ship, not big-bang.** v5 ships first as a beta file (`protocols/HANDOFF_PROCESS_v5.md`) while v4.4 stays canonical and live; promotion to canonical is a single atomic flip gated on (1) AI Council ratification of this ADR and (2) one fresh-eyes review meeting the established beta→stable criterion (v4.3.1 §B: <2 critical findings AND a PROMOTE / PROMOTE-WITH-CAVEATS verdict, reviewer judgment overriding count) plus the empirical teeth dogfood. The flip moves the spec's `Version:` and its four coupled surfaces (`CLAUDE.md`, `.claude/commands/handoff.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`) together, which `audit.py`'s coupling gates force to be atomic.

## Consequences

- **Easier:** the new session reads PRIMARY sources by construction (the teeth exclude summary-bluffable answers); the handoff stops re-transmitting drift-prone methodology copies (pointers + mechanical enforcement replace prose); task-state is one pointer, not re-narrated IDs; the operator stays at feature/epic level because the browser filters CC output to only judgment-needing items; the browser's plan-review is directly actionable (three constrained forms), removing the operator's translation step.
- **Harder / cost:** the inversion concentrates state-fidelity responsibility on CC (the only file-access actor), so the browser's value depends on the residual+drift-flag artifact being faithful — a faithfulness the fresh-eyes gate, not a unit test, must confirm; the teeth's non-bluffability is a semantic property (proven by dogfood, not regex); a parallel-ship period carries two handoff descriptions until the flip.
- **Relation to prior ADRs:** at promotion, v5 supersedes ADR-62 (v4 ratification) and the heavy-bundle delivery ADR-79 mandated; the ADR-28 layer invariants are untouched (Layer 2 stays validators-only; the probe manifest reuses read-only validators and adds no orchestration).

## Alternatives considered

- **Evolve v4 in place (layer the three #148 mechanisms onto the 8-file bundle).** Rejected: the bundle's re-transmission of methodology is itself a drift source, and a teeth-y read bolted onto a summary-shaped artifact still invites summary-bluffing; the inversion is the point.
- **Browser owns and assembles the handoff.** Rejected: the browser has no file access, so it would assemble from its own lossy summary — exactly the SECONDARY-source failure #148 guards against.
- **Immediate supersede (v5 takes the canonical name now).** Rejected: the spec's `Version:` line is coupled by `audit.py` to four other surfaces; bumping it to 5.0 forces an irreducible multi-surface commit up front, before v5 is reviewed — a big-bang on load-bearing infrastructure. Parallel-ship defers that atomic commit to after review.
