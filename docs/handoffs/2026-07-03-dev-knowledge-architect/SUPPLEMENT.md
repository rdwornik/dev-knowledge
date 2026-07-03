# Architect strategic supplement — 2026-07-03-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-03

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- CC-observed session-specific addenda (advisory; answer only if an outgoing chat holds the why): -->
A. **Essence-spec P1 merge intent** — was `feat/essence-spec-p1` committed-and-stopped to await
   *architect design review* (the absorb-not-pair spec-path + release-lint preflight placement), or
   just to serialize integration? What is the intended verdict on those two surfaced decisions?
B. **Mesh-model consult status** — is the Fable consult #2 on the mesh-transfer model (A/B/C) still
   an open design question, or did the Informant Organ's fleet-map (freshness+seb local /
   `doc_claims`+`git_backlog_drift` hub-scoped) already settle it as model-C-by-measurement?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->


SUPPLEMENT — outgoing architect answers (essence-transfer epic [#244], resume at P2)

=== 1. Strategic intent (way-of-working goal) ===
Build the methodology's LIFECYCLE-MANAGEMENT system: make the methodology a governed, versioned,
PRUNABLE artifact across repos — not an add-only pile. Concretely: close the "only-adds-never-
removes" gap so the live consumer-facing surface (CLAUDE.md rosters, gotchas, active
organs/commands/skills) stays current BY MECHANISM, not by a human catching rot by eye. Epic
[#244]. Resume at P2 (PRUNE — the first deleting phase).

=== 2. Tensions weighed — where we landed + why ===
- Spec representation (separate file vs in-place manifest evolution): landed IN-PLACE (evolve
  manifest-v1.1.0.yaml). Absorb-not-pair (F1): a separate methodology-spec.yaml recreates the
  drift-twin the analysis rejected; a v1.2.0 file is untagged -> preflight refuses -> live
  golden-diff undemonstrable. In-place keeps behavior byte-identical + provable.
- PRUNE vs Layer-2 autonomy-no invariant (how does the hub remove things from a consumer without
  an autonomous cross-repo write): landed on consumer-invoked deploy ONLY, staged-not-committed,
  hash-guarded (locally-modified = conflict-REFUSE, surfaced not deleted). Nothing autonomous
  deletes.
- Append-only vs prune: landed on the PATHOLOGY SPLIT — the audit trail (LESSONS/JOURNAL/ADRs)
  stays append-only/immutable; the live surface (CLAUDE.md/gotchas/active organs) gets pruned; a
  tombstone is itself an append to the audit trail.
- Conformance shape (one organ vs two): landed on ONE — extend the Informant
  (enforcement_coverage.py), three tiers (fire / presence / essence-conformance); firing and shape
  never conflated.
- Version granularity: landed on ONE methodology semver; component-level status:/removed_in: gives
  granularity without ~5x version-anchor drift.
- CLAUDE.md roster home: LEANING separate @-included generated file (keeps CLAUDE.md 100% human
  prose so the freshness gate keeps its teeth undiluted) — but this is operator decision D1 (open).

=== 3. Considered + rejected (do NOT relitigate) ===
- Separate methodology-spec.yaml — rejected (drift-twin, F1; absorb into the manifest).
- v1.2.0 file for P1 — rejected (untagged -> preflight refuse -> golden-diff undemonstrable).
- copier-LITERAL (adopt as a dependency) — rejected (templating doesn't fit organs with firing
  acceptance; the carriers are proven). Adopt the copier MODEL (deletion-propagation), not the tool.
- Renovate/Dependabot/Backstage/OPA as mechanisms — rejected (no cross-repo PR infra on local
  sibling repos; conformance is better-fitted in the Informant). Their SHAPE confirms the pattern
  (pinned versions + surfaced drift + gated update); we additionally have a demonstrated-firing
  standard they lack.
- Two conformance organs — rejected (duplicates the Informant's fleet plumbing + clone harness).
- Big-bang "solve everything in one pass" — rejected (PRUNE = deletion; autonomous deletion is
  forbidden; phased with a demonstrable per-phase acceptance is the discipline).
- Per-component semver — rejected (5x anchor-drift surface for no decision the operator would make
  differently).
- CI-as-guarantee for enforcement — rejected earlier (corp-ops has NO git remote -> a universal CI
  gate is structurally impossible fleet-wide; local-carrier + central-detection is the model).

=== 4. Open questions (deferred / unresolved) ===
- D1 — roster home: separate @-included generated file (rec) vs a marked block inside CLAUDE.md
  (ADR-53 doctrine call). Needed for P3.
- D2 — divergence-allowlist home: consumer-side .claude/methodology.yaml (rec) vs hub-side registry.
- D3 — grace state: a "deprecated" warning tier between active/removed, or straight active->tombstone
  (rec: no grace state at n=4).
- Global vs local conformance coverage: MUST cover BOTH ~/.claude (global gotchas/skills) AND
  per-repo (local) surfaces. Fable inventoried global; local per-repo coverage to be designed at
  P4 / Informant-Tier-3.
- release-lint wiring into preflight — behavior-changing, deferred to a later phase (manual-only today).
- #236 depends-on removal from #238/#240 — verify it actually unblocked them (flagged, unconfirmed).

=== 5. Decomposition rationale (why this shape; what NOT to redo) ===
Dependency order P1 -> P2 -> {P3, P4} -> P5 -> P6, each phase with a DEMONSTRABLE acceptance
(a mechanism that FIRES / a prune that REMOVES + verifies-absent), ai-council n=1 throughout before
any fleet step. P1 first because it's behavior-preserving (golden-diff) — the safe foundation that
establishes the self-model with zero risk. P2 (prune) is the crux + first DELETING phase -> Opus,
plan-first, gated on D1-D3. Fleet (P6) only after prune proven on n=1.
MUST NOT redo/re-decide: the corpus inventory (Fable did it — re-derive from the live repo, never
re-analyze from a summary); the essence-spec schema (built in P1); the in-place spec-path decision;
the mesh carrier (built + proven, Model D); the mesh-model A/B/C question (MOOT — see B).

=== 6. Off-repo context (not in the repo) ===
- CONTINUOUS-CONFORMANCE vision (operator's own contribution — do NOT lose): an ongoing nightly
  hygiene routine that reads the corpus FILE-BY-FILE for rot ("does this reference something
  obsolete / is this no longer needed"). Shape (validated; maps to Anthropic orchestrator+subagents):
  architect/Opus DECOMPOSES -> cheap Sonnet observer-agents do the per-file BINARY rot-check
  (zero/one: rotted y/n) -> surface. This is the continuous-conformance layer ABOVE P4/P5, and where
  release-lint (manual today) gets wired. Cost-appropriate + scalable. Home = [#244].
- Model routing: Fable's architecture job is DONE — do NOT re-invoke it for build phases; reserved
  for a genuinely-new contested fork only. P2 = Opus, plan-first. Mechanical phases + the
  observer-agents = Sonnet.
- Standing debts: P1 merge feat/essence-spec-p1 -> main (primary, --no-ff); ai-council CLAUDE.md
  GENUINE re-stamp (the deployed freshness gate is blocking ai-council's next commit on a live A2 —
  this is the first live-drift firing of the transferred organ; do a real re-read, NEVER a date-bump).

=== A. Essence-spec P1 merge intent + verdict on the two surfaced decisions ===
feat/essence-spec-p1 was committed-and-stopped for BOTH: architect review of the two surfaced
decisions AND to serialize integration (operator merges from primary). Verdicts:
- Spec-path (in-place absorb-not-pair): APPROVED. Fable chose a third option over the two offered,
  and it is the correct one (endorsed at review). methodology_version stays 1.1.0 for P1 (same
  version, richer representation, behavior identical); the next bump = P2 -> v1.2.0 tagged then
  (behavior-changing prune).
- release-lint preflight placement: DEFERRED — correctly OUT of P1. Preflight-wiring is
  behavior-changing; keep release-lint manual until a later phase that owns that behavior change.
Action: --no-ff merge to main from primary.

=== B. Mesh-model consult status ===
RESOLVED + MOOT — do NOT spin up a Fable consult #2 on the mesh-transfer model. The A/B/C question
was settled by RESEARCH (git-hooks: local-advisory vs central-enforcement) + LIVE RECON (corp-ops
has no git remote -> CI-as-universal-guarantee structurally impossible -> local-carrier +
central-detection is the model) + BUILD (the mesh carrier shipped as Model D and FIRED
enforcing-local x2 on ai-council). The Informant fleet-map settled WHICH organs are portable
(Group A canonical_freshness/reconciled = portable-local; Group C seb = ported-local; Group B
doc_claims/git_backlog_drift = hub-scoped by construction), feeding the carrier scope. So:
settled-by-measurement-and-build, not awaiting a consult. The Fable window was instead spent on the
essence-transfer architecture (the larger question), which subsumed the propagation question.
