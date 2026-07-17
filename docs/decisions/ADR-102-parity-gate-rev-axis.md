# ADR-102: Parity-surfaces enforcement-gate-rev axis — gate rev modeled separately from corpus source_tag

**Status:** Proposed
**Date:** 2026-07-17
**Decision tier:** Architecture (Path A — direct operator ruling; drafted lane B under plan-first architect review, 2026-07-17; the lane never self-accepts, ADR-94)
**Related:** ADR-91 (deployed-versions durable record — the corpus `source_tag` authority this axis reads but never rewrites), ADR-101 (hermetization — deliberately NOT amended; governs tree structure/naming, not parity-schema semantics), ADR-28/36 (Layer-2 read-only, WARN-only posture the checker keeps), ADR-85 (advisory-then-hardening pattern), ADR-87 (equilibrium contract — this arc's authoring split), #328 (the parity mechanism this extends, designed in `docs/audits/2026-07-11-technical-fleet-parity-register.md §9`), #336 (this decision's backlog task), #316 (ownership classification — adopts the declaration grammar below), #337 (blocking-promotion, gated on the zero-WARN steady state this unblocks), #342 (deferred max-fidelity follow-up)

## Context

`fleet_parity` (the #328 read-only parity checker) carried exactly one standing WARN, and it was structurally **undeclarable**. corp-monorepo's `dev-knowledge` hub-block pre-commit pin sits at **`v1.3.1`** — a deliberate *gate uplift* (`block-ff-push` + `backlog-id-on-close`, the #318/#319 fixes) — while corp's deployed **corpus** body stays at **`v1.2.0`** (floor/scripts/plugin sha-verified unchanged). The `precommit-hub-block` surface is `tier: {consumer: MUST}` with a `precommit_remote` probe carrying `expected_rev_from: deployed-versions`, so the checker compares the pinned rev against corp's `source_tag` in `ecosystem/deployed-versions.yaml`, finds `v1.3.1 != v1.2.0`, and emits `WARN_UNDECLARED / SEV_ERROR` ("present but not carried faithfully"). MUST is **non-waivable** (`_row_waivable`), so no `.methodology.yaml` declaration clears it.

The three naive fixes are ruled **wrong** (#336; 2026-07-16 census §6): **record-stamp** over-claims the corpus (asserts a v1.3.1 corpus that was never deployed); **full redeploy** re-appends the codemap-freshness hook corp deliberately removed (#276 unlanded); **pin-revert** discards the wanted uplift. The gap is conceptual, not procedural: the model conflated **two independent revisions** — the *deployed corpus* and the *enforcement gate* — onto one `source_tag` axis.

## Decision

**Model the enforcement-gate revision as a first-class axis, separate from the corpus `source_tag`, so "the enforcement gate is legitimately uplifted ahead of a full corpus redeploy" becomes a durable, declarable state.** Hub-side only — corp's record and pin are untouched (operator-ruled leg-1 deferral; a real v1.3.1 corp redeploy remains a separate future path).

1. **Home — the manifest, not the registry.** The gate-ahead value + its justification are a **hub-owned `gate_rev_ahead` declaration** on the `precommit-hub-block` surface row in `ecosystem/parity-surfaces.yaml` (the hub already owns surface semantics + repo-specific expectations). `ecosystem/deployed-versions.yaml` stays the **corpus `source_tag` authority, byte-untouched** — adding a gate field there would blur or over-claim the ADR-91 deploy-verified corpus-release contract. A new register would duplicate the surface register without adding authority.

2. **A refinement of the MUST fidelity predicate — never a waiver.** The gate-ahead evaluation sits **inside the MUST branch, before the fidelity WARN**, and **never** routes through `_pass_or_declare`, `declared_divergence`, or any `.methodology.yaml` match — those remain unreachable for MUST fidelity (preserving the in-code invariant "remediation is FIX, never DECLARE"). The pass outcome holds only when every conjunct of:
   ```
   MUST_OK = present
     AND gate-declaration-shape-valid
     AND A == effective_gate_rev            (A = actual pin; effective_gate_rev = proven G, else corpus C)
     AND C ancestor-of G  AND  G ancestor-of hub HEAD  AND  G != C   (strictly ahead, real hub tags)
     AND required_hook_ids ⊆ configured_ids
   ```
   is true. A gate declaration may change `effective_gate_rev` from `C` to a **proven** `G`; it may NOT conjure presence, suppress missing hook-ids, match a `.methodology.yaml` divergence, mark an allowlist component consumed, or change `_row_waivable`. Every false conjunct falls through to the **existing** MUST error path. **The corp config-edit commit (`efe5bd1`) is consumer provenance, never used in the hub `C→G` ancestry** — that ancestry is computed only over the hub tags.

3. **Visibility — a distinct verdict `GATE_AHEAD_DECLARED` (SEV_INFO).** A proven gate-ahead is reported as its own state, visible in the summary line — NOT folded into bare `AT-PARITY`. Folding it in would relocate the *same corpus over-claim* the record-stamp fix was rejected for into the verdict layer: the summary line is the management surface #316/#329 consume, and a gate-ahead is genuinely *not* corpus parity. The verdict is at-parity *family* (informational, non-blocking) but explicitly **not** in the PASS-declared/waiver family.

4. **Self-invalidation + retirement.** No `review_date` time-box: the git predicates are self-invalidating — when the corpus catches up (`C == G`), the ahead-test `G != C` fails and the row reverts to a normal `AT-PARITY`, leaving the declaration inert. An inert `gate_rev_ahead` declaration is surfaced as a visible `STALE_DECLARATION` (WARN-family) prompting its removal. **Retirement rule (doctrine — not fully checkable):** simultaneously deleting the declaration AND reverting the pin to `C` reads green, because no checker can infer a deleted policy; therefore retire the declaration ONLY once the corpus has caught/overtaken the gate and the actual pin is reconciled.

5. **Reusable declaration grammar (grammar only — #316 adopts).** Every declarative axis uses one wrapper: `value` (mandatory, axis-specific scalar) · `reason` (mandatory, non-blank) · `provenance` (mandatory, non-empty **list**; each item `{kind, repo, ref}`). This is the shape #316 (ownership classification) reuses verbatim. **This ADR defines the grammar and stops there** — enumerating ownership categories (`{methodology | project | conditional}`) is #316 scope. Shared grammar, separate axes.

6. **A latent safety hole closed below the schema.** `_row_waivable` honored an explicit `waivable: true` override, so a MUST/INVERSE row *could* have been marked waivable. The manifest loader now **refuses** `waivable: true` on any MUST/INVERSE row (structural refusal, row skipped) — TOMBSTONE's legitimate `waivable: true` is unaffected.

## Why not amend ADR-101

ADR-101 governs the **sanctioned top-level set, per-class name grammar, and refusal gate** — filesystem *structure and naming*. Its later amendment merely sanctions `.methodology.yaml` as a root file; it does not own that file's or `parity-surfaces.yaml`'s **semantic schema**. A parity-schema-semantics change (a new declaration key + verdict logic) is taxonomically unrelated to hermetization. The parity mechanism (#328) was itself designed in an immutable audit, not an ADR, so a durable schema concept that #316 will build on is decision-worthy in its own right → a successor ADR, not an ADR-101 amendment. (Independently derived by CC and the sol adversarial lane.)

## Consequences

- The sole standing `fleet_parity` WARN clears **honestly** — declared-with-reason, without asserting corpus parity — reaching the zero-WARN steady state #337's blocking-promotion is gated on.
- A future undeclared gate drift (e.g. corp bumps the pin to `v1.4.0` without re-declaring) re-WARNs: `A != G` fails `MUST_OK`. Anti-regress teeth are preserved.
- The checker stays Layer-2 read-only, WARN-only (exit 0 always; exit 2 only on an unusable manifest / bad `--run-date`); this axis adds no blocking gate.
- `#342` carries the deferred max-fidelity items (verify the gate tag *exports* the required hook ids; refuse an ambiguous `precommit_remote` match; peeled-SHA pin in provenance) — out of #336's blast radius.

## Status / ratification

Proposed 2026-07-17 (Path A, plan-first architect-reviewed). Ratify by editing the `**Status:**` line in place (ADR-94) and dropping the `**Proposed** —` prefix from the `docs/decisions/README.md` index row.
