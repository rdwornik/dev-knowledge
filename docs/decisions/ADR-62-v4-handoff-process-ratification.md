# ADR-62: v4 HANDOFF_PROCESS Ratification (post-hoc)

<!-- scope: meta -->

- **Status:** Accepted (post-implementation ratification; decision already made + implemented + validated)
- **Date:** 2026-05-30
- **Related:** ADR-42 (Handoff Format v3 — superseded by v4, append-only note carried), ADR-45 (explored-not-adopted "Handoff Architecture v4" — see naming note below), ADR-55/56/57/58 (v3.4 amendment trail, superseded by v4), ADR-39 (file lifecycle governance — append-only discipline preserved), `protocols/HANDOFF_PROCESS.md` (v4.3.1, stable)
- **Decommission:** the v3.4 architecture (13–14 hand-maintained files, JSON manifest, separate claims/scope/gate-probe artifacts, multi-stage Stage 1/2/3 ratification) — preserved at `protocols/archive/HANDOFF_PROCESS_v3.4.md`, no longer the live process
- **Source:** Operator decision (Rob, 2026-05-30) — **Path A** (direct ADR, no AI Council convene). Grounds: v4 was already designed (operator + browser-architect), implemented, run end-to-end three times, and validated by an independent fresh-eyes Opus 4.8 review returning PROMOTE WITH CAVEATS. This ADR is the retroactive provenance record, not a fresh design debate. No Council transcript.

## Context

The repo's prior handoff process (v3.4) was over-engineered: 13–14 hand-maintained
files per bundle, a multi-stage Stage 1/2/3 relay, a JSON manifest sidecar, a
placeholder-resolution dance, a separate claims artifact, and a scope-declaration
artifact. Its first real end-to-end test (2026-05-29) **aborted at Stage 3** when the
architect produced a fabricated claims structure; the operator chose ABORT over
ratifying an UNVERIFIED handoff.

An empirical process audit of that run returned **13 findings** (2 critical, 4 high,
6 medium, 1 low) — `docs/audits/2026-05-29-handoff-v3.4-process-audit.md`. Its
meta-observation §7 named the structural disease as **multi-surface fragility**:
patching the 13 findings individually would have left the next 13 inevitable. (This
is the empirical seed of the LESSONS "cluster-as-diagnosis" entry, 2026-05-30.)

A standing operator preference holds that *architecture decisions go through AI
Council, not unilateral edits*. v4 was nonetheless implemented unilaterally across
the 2026-05-29/30 marathon arc (operator + browser-architect design discussion,
fatigue, Council debate budget exceeded). The operator later decided (v4.3.1 PLAYBOOK
"Process versioning" rule) that **Council is not required for stable promotion** —
promotion is the operator's call gated on independent fresh-eyes review. This ADR is
the retroactive ratification consistent with that rule, closing the provenance gap
that left v4 "winning on conflict" against ADRs 42/55/56/57/58 by spec assertion
alone (BACKLOG Cross-stream P2, `handoff-v4-2026-05-29`).

### Naming note — two distinct "v4"s

**ADR-45 is titled "Handoff Architecture v4" but was explored-not-adopted** (a frozen
2026-05-13 design: a two-file `MANIFEST` + `NEXT` payload with `@path` invariant
imports and a defense-in-depth hook triple). Its supersession claim over ADR-42 was
formally withdrawn (ADR-45 Amendment 2026-05-25). **That v4 and the v4 ratified here
are different things that share a version label by coincidence.** The v4 ratified by
this ADR is `protocols/HANDOFF_PROCESS.md` v4 — the 2026-05-29 radical
simplification (8-file bundle, two-phase generation). ADR-45 remains
explored-not-adopted and supersedes nothing; this ADR does not revive it. The two
designs did *converge* on the same diagnosis (separate invariant from session state,
shrink the payload, drop decoder-required vocabulary); v4 landed at an 8-file middle
ground rather than ADR-45's 2-file floor, retaining the bundle structure the
2026-05-12 audit found empirically valuable.

## Decision

Ratify **v4 HANDOFF_PROCESS** — the v4 + v4.2 + v4.3 + v4.3.1 amendments taken
**collectively as a single architectural decision** — as the **canonical handoff
architecture for `.dev-knowledge`**. Status: **stable** as of 2026-05-30 (v4.3.1
amendment; stamp source-of-truth `version=4.3.1`/`status=stable` in
`.claude/commands/handoff.md` Phase-2 defaults).

The ratified architectural pattern:

- **8 files** per bundle (`README` + `01_ROLE` … `07_ASK_BACK`), not 13–14.
- **Two-phase** generation (Phase 1 interview → Phase 2 consolidate), not a
  multi-stage Stage 1/2/3 ratification relay.
- **Files generated from source at handoff time** — extracted from
  PLAYBOOK/ESSENTIALS/CLAUDE.md plus a narrative synthesized from the architect's
  interview answers — not persistently hand-maintained between sessions.
- **Sage→apprentice** teaching frame for the Phase 1 interview (operator preference:
  a concrete metaphor carries design intent better than bare ADR numbers in
  human↔LLM dialogue).
- **Operator escalation ladder** replaces bare `role confirmed` ratification (Tier 1
  re-paste → Tier 2 CC verify → Tier 3 abort).
- **Phase 2 verification** cross-checks the sender's load-bearing claims against
  actual repo state at generation time.
- **Four-tag sage discipline** (witnessed / recall / inferred / unknown) with
  definitions inlined in `04_RECENT` of every v4.3+ bundle.
- **Triangulation** (insider + independent outsider review) as the quality gate for
  process **versioning** (beta→stable promotion), **not** for every routine artifact.

## Trade-offs accepted

1. **Council not convened during implementation.** Operator's call (marathon-arc
   fatigue; Council debate budget exceeded). Formalized later: the v4.3.1 PLAYBOOK
   rule states Council is not required for stable promotion. This ADR is the
   retroactive record consistent with that rule — accepted, not litigated.

   This trade-off is a textbook instance of the ML-2 pattern that ADR-63 codifies (a
   documented guard drifting under load): the standing "Architecture decisions = AI
   Council" rule drifted under marathon-arc fatigue, and the response was to **relax
   the guard** (amend the rule via v4.3.1 PLAYBOOK so the bypass wasn't a violation)
   rather than **gate it harder** (e.g., codify Council-or-defer as a hard rule). The
   choice was deliberate: post-hoc Council adds limited value to architectural decisions
   already implemented + validated by fresh-eyes review; Council debate cost (~30–45 min
   per convene + ADR distillation) is high relative to retroactive-ratification
   value-add. **ADR-63 takes the opposite cure for the same disease — gating via
   codification — because that pattern's cost/value calculus inverts: operator visual
   review is fast, and empirical catch-value is high.** No paired principle is
   articulated for when guards should be relaxed vs. gated; that reconciling question is
   tracked as a future LESSONS/ADR candidate (see BACKLOG).

2. **Spec growth via amendments.** `protocols/HANDOFF_PROCESS.md` grew to **504
   lines** (v4 body + Amendment A at v4.2, v4.3, v4.3.1) under ADR-39 append-only
   discipline. Consolidation into a fresh budget-compliant spec is deferred to v5
   (Council scope, future). Accepted: append-only preserves the decision trail at the
   cost of length.

3. **Synthesis imperfection accepted at Phase 2.** v4.3 explicitly reframed v4 as a
   hybrid (extracted invariant parts + synthesized narrative), not pure mechanical
   generation. Per-generation imperfections drive template/skill improvement via a
   use→review→refine→re-validate cycle, **not** bundle re-maintenance. Accepted.

4. **Triangulation honestly scoped.** Per v4.3.1 Amendment §A, triangulation guards
   process *versioning* at the promotion gate; routine handoffs ride on Phase-2
   self-verification + operator visual check. An adversarial per-artifact review for
   routine handoffs is deferred to BACKLOG P1 (the agent-framework extension). This is
   a known coverage limit, accepted and tracked — not hidden.

5. **§3.1-vs-Amendment-A supersedence.** The spec body §3.1 (an earlier three-tag
   system) is preserved unchanged; Amendment A (four-tag canonical) supersedes it via
   the amendment-precedence rule, and `audit.py` check #9 enforces the cross-reference
   **syntactically** (it verifies the pointer/enumeration is present, not that tags
   are semantically correct). Clean consolidation is deferred to v5. Accepted.

## Alternatives considered

1. **Patch v3.4 (keep the 13/14-file multi-stage architecture, fix the 13
   findings).** Rejected: cluster-as-diagnosis (now a LESSONS entry) showed the 13
   findings were one structural disease (multi-surface fragility), not 13 independent
   bugs. Patching would have left the next 13 inevitable.

2. **Fully automated mechanical generation.** Rejected as aspirational. The v4.3
   fresh-eyes review caught that the "generated from source" claim was hybrid in
   practice; v4.3 honestly sharpened it to "ephemeral per-handoff generation +
   per-generation verification, accepting synthesis-time imperfection."

3. **Single-file handoff document.** Rejected: insufficient teaching sequence for a
   fresh apprentice — role, methodology, project, recent, next, check, and ask-back
   are distinct knowledge layers warranting separate files.

4. **Pure mechanical promotion criterion (`<2 critical → promote`, count only).**
   Rejected after the v4.3 second fresh-eyes review identified it as an easy-metric
   trap (it violated the bundle's own hard-metric-over-easy-metric rule). v4.3.1
   restated the criterion as **judgment-augmented**: mechanical `<2 critical` AND a
   reviewer Stage-3 verdict of PROMOTE / PROMOTE-WITH-CAVEATS, with reviewer judgment
   overriding the count when they differ.

5. **ADR-45's two-file MANIFEST + NEXT design.** Already explored-not-adopted
   (2026-05-13) because it dropped the full invariants and 11-file bundle the
   2026-05-12 audit found empirically load-bearing. v4 is the converged middle ground;
   this ADR does not revive ADR-45's floor.

## Empirical grounding

- **Triangulation empirically validated.** On the v4.2 bundle, the insider review
  (architect/sage who built it) caught **1 of 4** critical findings that a zero-context
  independent Opus 4.8 fresh-eyes review then caught (~25% insider vs ~100% outsider).
  Curse-of-knowledge observed empirically (n=1 bundle; directionally consistent with the insider-blindness pattern, but single data point — replication pending) (LESSONS 2026-05-30). Codified as the
  beta→stable promotion gate (v4.3) and restated judgment-augmented (v4.3.1).
- **Convergence trend across three preserved bundles:** v4.1 first-run (7
  refinement-level issues, no architectural defects) → v4.2 re-run (4 critical found
  by fresh-eyes) → v4.3 first-run (0 new critical; PROMOTE WITH CAVEATS) → stable.
  All three bundles preserved as historical evidence under `docs/handoffs/`.
- **`audit.py` health gate** grew 6/6 → **9/9** across the arc (check #7 mermaid theme
  directive, #8 stamped v4 bundle structure, #9 tag-canonicity lint).
- **Test suite** grew to **103 passing** (audit checks + fixtures + tests).
- **ADR-39 append-only discipline** held across the four spec amendments and the
  amendment-note ADRs (42/45/55/56/57/58) — each verified insertions-only by
  `git numstat`.
- **11 LESSONS entries** (2026-05-30 batch) capture the arc's patterns
  (curse-of-knowledge, triangulation scoping, cluster-as-diagnosis, easy-metric
  closure, prompt-level convention drift, multi-step intermediate-state verification,
  honest no-op over fabricated commit, sage-tagging three-iteration convergence,
  hand-maintained-surface-count as the fragility metric, new-folder-without-checking
  N+3 sharpening, meta-level curse-of-knowledge recursion).

## Consequences

- **v4 is canonical** for `.dev-knowledge`. Future handoff-process changes require a
  new amendment (v4.4+) or a major version bump (v5 — Council scope).
- **Routine handoffs ride on Phase-2 self-verification + operator visual check** — NOT
  triangulation. Honestly scoped per v4.3.1 Amendment §A; the residual blind spot is
  tracked as BACKLOG P1.
- **Process-versioning gates** (beta→stable) require independent fresh-eyes review
  under the judgment-augmented criterion, enforced by the PLAYBOOK "Process
  versioning" rule.
- **Spec consolidation at v5** (Council scope, future) folds the v4 body + amendments
  into a fresh budget-compliant spec and resolves the §3.1 supersedence cleanly.
- **Agent-framework full implementation** (BACKLOG P1, `protocols/AGENT_FRAMEWORK.md`
  v0.1 stub) tracks toward the "adversarial routine handoff" gap — the operator's
  strongest structural signal from the marathon arc.
- **Cross-repo handoff patterns** (corp-monorepo, ai-council) may adopt the v4
  architecture, each on its own variant track in its own repo; nothing here mandates
  cross-repo adoption.
- **Apprentices** (future Claude.ai chats receiving a bundle) get four-tag definitions
  inline, a standard verification table, role disambiguation, and the
  operator-runs-the-review clarification — the process documentation is self-contained.

## References

- `protocols/HANDOFF_PROCESS.md` (v4.3.1, stable; 504 lines)
- `protocols/PLAYBOOK.md` — "Process versioning" (judgment-augmented beta→stable
  criterion) + the LLM↔LLM handoff back-and-forth
- `protocols/ESSENTIALS.md` — one-line methodology rules
- `protocols/AGENT_FRAMEWORK.md` — v0.1 stub (operator's strongest structural signal)
- `.claude/commands/handoff.md` — Phase 1 + Phase 2 generation logic; stamp
  source-of-truth (`version=4.3.1`, `status=stable`)
- `templates/handoff/*.md.tmpl` — the 8 bundle templates
- `scripts/audit.py` — checks #7/#8/#9 enforcing v4 structure (health 9/9)
- ADR-39 (file lifecycle governance — append-only discipline preserved across all v4
  amendments)
- ADR-42 (Handoff Format v3 — superseded by v4, append-only supersession note)
- ADR-45 (explored-not-adopted "Handoff Architecture v4"; supersedes nothing — see
  Naming note)
- ADR-55 / ADR-56 / ADR-57 / ADR-58 (v3.4 amendment trail; carry v4 supersession
  notes)
- `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` (13-finding empirical audit;
  meta-observation §7 = multi-surface fragility)
- `docs/handoffs/2026-05-29-dev-knowledge-session/` (v4.1 first-run bundle, historical)
- `docs/handoffs/2026-05-29-dev-knowledge-session-v4.2-rerun/` (v4.2 re-run bundle,
  historical — the bundle audit check #8 currently validates)
- `docs/handoffs/2026-05-30-dev-knowledge-session/` (v4.3 first-run bundle, the
  reviewed PROMOTE-WITH-CAVEATS bundle)
- `LESSONS.md` — 2026-05-30 marathon-arc batch (11 entries)
- BACKLOG Cross-stream P2 "AI Council debate → ADR formalizing HANDOFF_PROCESS v4"
  (closed by this ADR via Path A)
