# ADR-82: HANDOFF_PROCESS v5 — CC-owned, primary-source-forced handoff (model C)

- **Status:** Proposed
- **Date:** 2026-06-11
- **Related:** ADR-62 (v4 handoff ratification — superseded by v5 *at promotion to canonical*, not now); ADR-79 (browser carrier bundle-only — v5's thin boot supersedes the heavy-bundle delivery it mandated, at promotion); ADR-28 (three-layer model — v5 inverts who *initiates*, not the layer invariants); ADR-41 (cross-repo decision routing — the Council route this ADR is pending on); #148 (the v5 redesign item), #124 (BUNDLE.md consolidation — superseded by the thin boot), #25 (deferred .tmpl refinements), #145 (codification-completeness — the pointer-integrity dependency)
- **Decommission:** none active while **Proposed**. On promotion to canonical (the Council-gated flip, tracked by the named successor backlog item), the following are decommissioned: (1) `templates/handoff/*.tmpl` → archived to `templates/archive/handoff-v4/`; (2) the 8-file teaching-bundle generation path in `/handoff`; (3) `audit.py` checks #8 `handoff_bundle_structure` / #9 `handoff_tag_canonicity` scoped/retargeted to historical v4 bundles. Nothing is removed by this ADR in its Proposed state.
- **Source:** Rob's decision, 2026-06-11 (CC prompt implementing model C); architecture routed to AI Council per #148 / ADR-41 — this ADR is the decision record Council ratifies before the flip.

<!-- Decommission: deferred to promotion — see Source; nothing active while Proposed. -->

> **Status update (in-place marker — the frozen header above is unchanged per the immutability
> convention): canonical since 2026-06-11.** HANDOFF_PROCESS v5 was **promoted to canonical (v5.2)** on
> 2026-06-11. The AI-Council ratification gate was **waived (#149)** — *not* passed — so this is
> **canonical by operator waiver, not Council-accepted**, and **no Council transcript exists**. Read the
> header/body "while Proposed" and "at promotion" qualifiers as historical (pre-promotion) context.

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

## Amendment 2026-06-16 (v5.1 — architect strategic supplement via interview extraction)

**What was incomplete.** v5 (this ADR) establishes that CC owns the handoff and the residual is the un-committed *why* — but the residual is **repo-derived**, and one class of *why* is **not** in the repo: the architect's strategic deliberation (intent, tensions weighed, options rejected) originates browser-side (Layer 1). v5.0 had no first-class carrier for it, so it leaned on operator-relay (human memory) — the same lossy channel the redesign set out to remove. The §13(d) operator-context beat was a partial inbound patch (one ask, off-repo only); it did not capture the *outgoing* architect's deliberation as a durable artifact.

**Resolution (HANDOFF_PROCESS v5.1, `Version: 5.1`).** Architect mode gains a **first-class advisory supplement produced by a structured interview**. On `/handoff … architect` CC emits a fixed 6-question *why*-only interview block (canonical schema: `templates/handoff/v5/SUPPLEMENT.md.tmpl`); the operator relays it to the outgoing browser; the browser's answers become `<bundle>/SUPPLEMENT.md` **verbatim** (no re-typing — the file-less browser cannot emit a file, so CC writes what it produced); `scripts/assemble_paste.py` folds `SUPPLEMENT.md` into `PASTE_THIS.md` (expected in architect mode, `[warn]` if absent). The interview **answers ARE the artifact** — carried 1:1, unlike v4's interview, which summarized and lost them. The §13(d) inbound beat is reconciled to the lighter "anything changed since the supplement?" check (Q6 captures off-repo context at handoff time) — kept, not duplicated.

**Intent preserved (amendment, not reopen).** The model-C decision is unchanged: CC owns and initiates; methodology is source-authoritative + mechanically enforced; the forced primary-source read keeps its teeth. The supplement is **advisory, never teeth-bearing** — it elicits ONLY non-re-derivable *why*, never repo state / methodology / task-state (those stay forced-read, §3/§5), and where any answer touches verifiable state the existing drift-checks catch staleness. `SUPPLEMENT.md` is a **per-session transient** (like RESIDUAL/PROBES), not a hand-maintained surface, so it does not re-create the v4 drift disease. **Scope: architect-mode-additive only**; execution mode and §§1–12 are untouched.

**Coupled atomic move.** A 5.0→5.1 *minor* bump keeps major = 5, so the major-keyed coherence surfaces (`CLAUDE.md`, `.claude/commands/handoff.md`) need no change; only the full-version stamp moves (`CONTRIBUTING.md` `stamp v5.0`→`v5.1`). `audit.py health` green (`handoff_version_stamp` + `amendment_coherence`) proves the atomic move.

**Cross-repo.** v5.1 stays `.dev-knowledge`-scoped — `/handoff` is repo-local and not yet parameterized across repos (the deferred #164 generator). The supplement schema is kept generic/portable (no repo-specific binding) so #164 can carry it unchanged.

**Status note.** This ADR's header remains `Proposed` (its original state); the spec it records was operator-ratified canonical at the #149 flip (2026-06-11) per `CONTRIBUTING.md`. This amendment records v5.1 against the operative v5 decision and does **not** alter the original decision text (ADR immutability — an append-only marker per the amend-vs-reopen convention).

## Amendment 2026-06-17 (v5.2 — supplement becomes an always-generated fillable file)

**What was incomplete.** The v5.1 amendment (above) made the supplement a first-class advisory artifact, but it became a durable file **only after** the outgoing browser answered an ephemeral terminal interview block. A cold / `/clear`ed handoff (no outgoing browser in context — the common case after a session reset) therefore produced **no `SUPPLEMENT.md` at all**: a missing-deliverable look, zero git tracking, and no lead-by-hand for the operator. The first v5.1 dogfood surfaced this immediately (2026-06-16 bundle `RESIDUAL.md` §2).

**Resolution (HANDOFF_PROCESS v5.2, `Version: 5.2`).** The supplement is now an **always-generated, self-documenting, fillable file**: CC writes `docs/handoffs/<slug>/SUPPLEMENT.md` unconditionally for every architect handoff (a QUESTIONS section for the outgoing chat + an empty ANSWERS section), commits it on the handoff branch for durable tracking, and `scripts/assemble_paste.py` folds the **ANSWERS region only, and only when non-empty** into the next `PASTE_THIS` (replacing the v5.1 whole-file fold + warn-if-absent). The **cold-handoff disposition** is now defined: an empty ANSWERS section is committed N/A (not a defect), not folded, and the incoming §13(d) beat fires full.

**Intent preserved (amendment, not reopen).** The model-C decision and the v5.1 advisory contract are unchanged — the supplement stays **advisory, why-only, never teeth-bearing**, and **CC never fabricates answers** (an unanswered supplement is committed empty, never synthesized — that would re-create the v4 disease). This is a mechanism + operator-flow refinement of the v5.1 supplement, not a new model. **Scope: architect-mode-additive only**; execution mode and §§1–12 are untouched.

**Coupled atomic move.** A 5.1→5.2 *minor* bump keeps major = 5, so the major-keyed coherence surfaces (`CLAUDE.md`, `.claude/commands/handoff.md`) need no change; only the full-version stamp moves (`CONTRIBUTING.md` `stamp v5.1`→`v5.2`). `audit.py health` green (`handoff_version_stamp` + `amendment_coherence`) proves the atomic move. #159 stays open (the real dogfood — a supplement filled with actual answers — is still owed); #164 must now emit the always-file form.
