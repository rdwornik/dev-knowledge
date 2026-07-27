# Adversarial review — ADR-107 (Codex sol) — verdict: RATIFIABLE AFTER EDITS

**Reviewer:** Codex `sol` — direct exec, independent-derivation-first method
**Date:** 2026-07-27
**Subject:** `docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md` (Status: Proposed)
**Reviewed at:** `main` @ `fa3f10a3` (the post-BUILD merge — [#436] ratchet BUILT + [#433] C1
gate armed), the state ADR-107 was authored against plus the armed coherence gate.
**Verdict:** **RATIFIABLE AFTER EDITS** — the five edits below (E1–E5), folded verbatim into
ADR-107 by the commit immediately following this artifact on the same branch
(`docs/adr107-sol-review-fold`). Ratification remains a separate operator act; the ADR's
status stays **Proposed**.
**Cross-links:** ADR-107 (target; its Source line references this artifact) · [#433] (the
carrier — per E5, it does NOT close on the ADR alone) · spike evidence
`docs/audits/2026-07-27-verification-433-schema-spike.md`.

> Filename note: the requested slug `adversarial-review-adr-107-sol` is carried after the
> `codex` class token — `adversarial-review` is not in the closed ADR-101 R3 audit-class
> enum, and `codex` is the established class for sol-lane reviews (precedent:
> `2026-07-19-codex-cycle-close-sol-adversarial-diff.md`).

---

## The five edits (verbatim, as ruled)

### E1 (§4, after §4.4) — INSERT new §4.5

> 5. Mechanical activation gate. While the viewer slot is EMPTY, no viewer is active. A
> future viewer adoption does not take effect until the same change lands (a) a
> machine-readable declaration of package, exact version, read-only command surface, and
> external install-prefix requirement, and (b) an `audit.py` `task_viewer_contract`
> ship-gate leg that FAILs unless the installed version matches the declaration, the prefix
> resolves outside the repository, the K1–K5 verification artifact identifies that exact
> version, and a viewer probe leaves `BACKLOG.md` and `tasks/` byte-clean. Prose evidence
> alone cannot activate a viewer.

### E2 (§5, finding 7) — REPLACE with

> 7. Directory-as-id-counter: substrate built, allocation rule not built. The tree supplies
> one filesystem representation per live id and duplicate-id refusal, but no next-free
> calculation, retirement-completeness rule, or concurrent-allocation probe was built.
> [#382] must therefore receive allocation-ledger completeness, retirement semantics,
> duplicate-id enforcement, and concurrent-branch collision behavior as explicit
> desired-state contract inputs. Section 6.3 may rule this surface's local mechanism, but
> it does not absorb or discharge this seventh [#382] input.

### E3 (§6.3 opening + retained-file rule) — REPLACE with

> 6.3 Obligation 3 — RULED, NOT YET STRUCTURALLY DISCHARGED; narrow ADR-65 amendment
> required. For the post-flip task store, ADR-107 explicitly amends ADR-65: a task leaves
> the active queue, but a minimal allocation record retaining its opaque id and terminal
> status remains within the lifecycle-managed `tasks/` tree. Git and JOURNAL remain the
> full technical and business records. This retained allocation record is a narrow
> exception to ADR-65's no-archive-file and no-new-per-item-write rules. Commission H is
> structurally discharged only when retire-not-delete behavior and the duplicate-id ship
> gate are implemented and witnessed.

Also update the ADR's supersession/amendment header to declare: "Amends ADR-65 (narrow:
retained allocation record in tasks/)."

### E4 (§3, viewer slot) — REPLACE the reader-surface claim with

> No viewer search is scheduled, and the slot is PARKED EMPTY behind the re-entry criteria
> below. This does not claim that the requested top-five ready-set or overdue-ruling read
> surface already exists: `gen_task_tree.py` currently supplies generation, coherence
> checking, round-trip verification, and pruning only. The graph / `READY.md` reader
> surface remains separately owned work and must name its consumer before activation under
> ADR-105.

### E5 (§7.5 opening) — REPLACE with

> [#433] does not close on this ADR alone. This ADR records the generalization acceptance
> clause and assigns its second-surface proof, but §6.2 correctly states that the proof
> does not yet exist. [#433] remains open until that obligation is demonstrated, or until
> the operator explicitly amends [#433]'s Done-when; an explicit non-discharge is a
> disposition, not a discharge.
