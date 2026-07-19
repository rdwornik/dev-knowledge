# Codex `terra` lane — review of the consolidated night-audit report

- **Class:** codex (ADR-101 enum) · **Date:** 2026-07-19 · **Slug:** cycle-close-terra-review
- **Lane:** `terra` — adversarial doc-lane review. Model `gpt-5.6-terra` via `codex exec` (read-only reviewer per `codex/AGENTS.md`).
- **Under review:** `docs/audits/2026-07-19-technical-night-consolidated-cycle-close.md`.
- **terra's overall verdict (verbatim):** *"Needs fixes first; its recurrence and status-reconciliation mechanisms are not implementable as described, and several seeds misroute existing tickets."*
- **Disposition:** **all 7 findings judged legitimate and applied to the consolidated report before commit.** terra's line numbers reference the pre-fix consolidated. The applied version supersedes; this file preserves the review + disposition for the record (immutable-audit convention).

---

## Findings (terra's bands) + disposition

### HIGH — :12 · over-generalized "growth-side enforcement is sound"
- **terra:** the report generalizes growth-side enforcement as sound including `validate-backlog`, `block-ff-push`, floor-hash, but E1 proves fire only for the seeded `fleet_parity` row and `validate_hermetization`; no fire evidence for the other guards.
- **Disposition — APPLIED (truthfulness):** §0 narrowed to state E1 fire-proved **two** organs this run (two-tier gate + fleet_parity); the other guards are present/established but **not fire-tested this run** (floor-hash parity corroborated by S5's hash-match, not a fire test). §2 meta-finding #2 already scoped correctly ("E1 proves the two-tier gate and fleet_parity fire").

### HIGH — :37 · ADR-89 "effective Accepted" mischaracterized
- **terra:** the report calls ADR-89's README state "effective Accepted," but its README row carries no status — there is no machine-readable index status to reconcile, so the proposed #242 check cannot compare an absent value.
- **Disposition — APPLIED:** S3 row + seed 3 corrected — the README index has **no status column** (ADR-88's row textually says Accepted; ADR-89's row says nothing); the #242 check must first define a status field **or** compare the header against the ADR's own in-file amendment marker. (S3's source report already stated this precisely; the consolidated summary had over-generalized it.)

### HIGH — :45 · `coherence-nudge` cannot enforce "amendment requires companion edit"
- **terra:** `coherence-nudge` only notices a registered spec changed without a version bump; `_SPEC_REGISTRY` holds source paths, not required co-change dependencies — so "extend it to require a PLAYBOOK/ESSENTIALS companion edit" is not implementable as described.
- **Disposition — APPLIED:** S4 mechanism + seed 1 reframed to a **new/generalized staged-diff co-change checker** with explicit `ADR-36/41/101 → PLAYBOOK/ESSENTIALS` edges, explicitly **not** a drop-in `_SPEC_REGISTRY` addition.

### HIGH — :110 · #331 misrouted as the reconciliation/build ticket
- **terra:** #331's done-condition is only an operator adoption-vs-durable-divergence *ruling*; it does not own the parity-surface rows or the consumer script-divergence implementation.
- **Disposition — APPLIED:** seed 5 changed — #331 is a **prerequisite decision**; the manifest-row + `validate_backlog`-fork declaration is a **separate implementation seed** with `kill-candidates: none`.

### MEDIUM — :107 · "an ADR built on an intake" not machine-identifiable
- **terra:** the audit predicate has no machine-readable basis; the ADR-102/103 link is indirect through BACKLOG tickets, and ADR metadata doesn't encode provenance reliably enough.
- **Disposition — APPLIED:** S1 mechanism + seed 2 now state the **precondition** — define a required `Intake:` provenance field / traversal rule first (converges with sol#1's `validate_intake.py`), so the citation check has a machine-readable join.

### MEDIUM — :109 · #348 wrongly listed as kill-candidate for the grooming detector
- **terra:** #348 owns configured routines gated by #270; the S2 detector is supporting data/mechanism and does not subsume that routine ticket.
- **Disposition — APPLIED:** seed 4 → `kill-candidates: none`; #218/#348 demoted to **adjacent consumers**, not subsumed.

### MEDIUM — :114 · #270 both kill-candidate and prerequisite; lost WARN-first rule
- **terra:** a prerequisite cannot be closed by this seed; and the S9 gate must stay advisory (WARN-first) until two demonstrated runs per #270's load-gauge.
- **Disposition — APPLIED:** seed 9 → `depends-on: #270`, `kill-candidates: none`, and **WARN-first then FAIL after two demonstrated runs** restored.

---

## Net

terra found **no fabricated finding and no missed gap** — every defect was an **over-claim or a mis-routed kill-candidate in the consolidation layer**, not in the underlying stream evidence. All 7 are applied. The value of the lane here: it kept the consolidated report from over-stating what E1 proved (:12) and from filing seeds that would have tripped the fleet's own filing-backpressure / git-drift gates by claiming existing tickets as kill-candidates (:109/:110/:114). Post-fix, the consolidated report is sound as a foundational artifact. Independent coverage validation: `2026-07-19-codex-cycle-close-sol-adversarial-diff.md` (sol converged on all 8 domains).
