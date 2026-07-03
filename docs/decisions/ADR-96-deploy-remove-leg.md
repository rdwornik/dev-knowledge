# ADR-96: Deploy remove leg — prune a status:removed component from a consumer (P2)

- **Status:** Accepted
- **Date:** 2026-07-04
- **Decision tier:** Architecture (Path A — architect delegation under the ADR-87 equilibrium; [#244] P2, plan-first/Opus, operator-gated)
- **Related:** ADR-91 (corpus versioning — the git-tag anchor this release bumps to v1.2.0), ADR-92 (deploy-runbook doctrine + the detect/apply/verify carrier contract + D9 this extends), ADR-93 (floor hash-guard — the refuse-on-drift precedent the prune hash-guard mirrors), ADR-81 (leg-e functional-proof standard: enforcement/removal *in-effect*, not merely deployed), #238 (deployed presence ≠ deployed enforcement — the doctrine P2 generalizes to *removal*)
- **Source:** [#244] essence-spec lifecycle epic, phase P2 (PRUNE). Operator decision D3 resolved: straight `active → removed`, 2-state, no `deprecated` tier.
- **Decommission:** none

## Context

The methodology-deploy engine (`deploy/`) was **add-only end to end**. `CarrierState` had no "present-but-should-be-absent" state; every carrier's `apply()`/`_ensure_*` wrote or bumped-in-place and never deleted; `tool.py` drove entirely off `carriers:` and never read a component's `status:`. So a consumer's live surface could only **accrete** — retired commands, stale roster lines, dead gotchas piled up with no way to shed them. The component schema reserved `status: active | removed` but `release_lint` C6 rejected anything but `active` ("tombstones unlock in P2, gated on operator decision D3").

#238 established that **deployed presence ≠ deployed enforcement** — a component can be present in a consumer yet not actually enforcing. P2 generalizes that doctrine to *removal*: the engine must be able to **remove** a component from a consumer, safely, and **prove it is gone** — not merely stop shipping it. This is declarative config-management removal (Terraform destroy-on-remove / Ansible `state: absent`), **not** an API deprecation window.

## Decision

Add a **remove leg** to the carrier contract, folded into the deploy converge:

1. **Contract (`deploy/contract.py`).** A `PruneState` enum (`ALREADY_ABSENT` / `PRESENT_CLEAN` / `PRESENT_MODIFIED`), a `PruneResult`, and three concrete-default `Carrier` methods — `detect_prune` / `prune` / `verify_pruned` — that raise `PruneUnsupported` in the base. Prune is **opt-in per carrier** (the "no big-bang" boundary): P2 lands the leg on exactly one carrier; an unsupported prune fails loud. `verify_pruned` is contractually **independent of `detect_prune`** (D9), mirroring verify/detect — its `ok` gates the record write, so the registry can never say success while a removed component is still present.

2. **Hash-guard (the copier deletion-propagation model, adopted — not the tool).** `detect_prune` compares the consumer artifact against the component's declared last-deployed shape. Byte-match → `PRESENT_CLEAN` (safe to remove); any divergence → `PRESENT_MODIFIED` → **REFUSE** (do not clobber the operator's local work; surface the conflict). Clean and modified are **both** exercised.

3. **2-state lifecycle (D3).** Straight `active → removed`; **no `deprecated` tier**. Rationale: we own the fleet, so a deprecation tier's only value is coordinating *uncontrolled* consumers we don't have, and its failure mode is precisely the add-only limbo P2 eliminates. `release_lint` C6 now allows `removed`, **requires** `removed_in:` on it, and **forbids** `removed_in:` on active.

4. **Converge-then-prune + destroy-confirm.** A `status: removed` component means "this should be absent"; `deploy <repo> --target 1.2.0 --execute` converges the active set **and** prunes the removed one (`assess` shows the prune plan read-only first). A present prune **requires an interactive confirmation** (Terraform destroy-confirmation shape); `--auto-approve` skips it for scripted runs; an add-only plan never prompts.

5. **Tombstone (append-only, pathology-split).** The audit trail is immutable; the live surface is prunable; the tombstone is itself an append. The **retained** `components:` entry (flipped to `status: removed` with `removed_in` + `reason`, never deleted) is the structured durable record; a JOURNAL `Changes:` line is the human trail; this ADR is the doctrine home. The Layer-2 tool **prints** the tombstone record — it never auto-writes hub living docs.

## The n=1 subject: why `ruff-gate`

The truth-maker requires flipping **one real component** to `removed` and pruning it from ai-council. No component is naturally dead, so the subject was chosen for **clean mechanism**, verified at recon depth (the "structurally clean" claim was itself verified, after the first candidate failed the same way):

- **`hub-toc-hooks` (rejected)** proved **structurally entangled**: its precommit `hub_hooks` entry *is* version-anchor-3, and in ai-council the two toc hooks are that entry's only content — so pruning empties it, the add-path can no longer identify it, and it re-creates on the next deploy (a tug-of-war). No manifest config yields "pruned + stays-pruned + anchor-3 GREEN + idempotent."
- **`ruff-gate` (chosen)** is a self-contained `- repo: …/ruff-pre-commit` block matched by exact URL (not by hook-id), carrying no anchor. Dropping `ruff` from `required_repos` is a clean list-drop, so the add-path never re-creates it; no tug-of-war, idempotent, golden-diff clean.

**Fleet-scope caveat (verbatim, load-bearing).** Marking `ruff-gate` removed in the fleet-shared manifest is **NOT** a real fleet retirement of ruff — a live, useful gate. The n=1 imperfection (a shared manifest marking a live gate `removed`) is **inherent to n=1, not subject-specific** — no naturally-dead component exists to prune. The `reason:` field records it verbatim: *"P2/[#244] n=1 prune truth-maker — demonstrates the remove-leg on ai-council. NOT a fleet retirement of ruff. Per-consumer scoping awaits D2 (divergence-allowlist); P6 fleet rollout MUST re-evaluate before propagating this removal."*

## Functional proof (ADR-81 leg-e — removal *in-effect*, not merely deployed)

Merged ≠ done. Proven on ai-council n=1 via a consumer-invoked deploy: `ruff-pre-commit` **pruned and verified ABSENT** (presence-checked, not "the code ran"); a **locally-modified target REFUSED** (no delete, no record); the non-pruned surface **byte-identical** (only the ruff entry removed + the legitimate `hub_hooks` `v1.1.0→v1.2.0` bump); the version record wrote `1.2.0`. release_lint reconciles all 5 anchors to `v1.2.0` GREEN.

## Consequences

- **General-case hash-guard nuance (out of scope for n=1).** `detect_prune` compares the consumer against the CURRENT manifest shape — correct for n=1 because ruff is unchanged `1.1.0→1.2.0` (unmodified-consumer == target → `PRESENT_CLEAN`). The general case — a component whose source **drifted** between its deploy and its prune — needs comparison against **last-deployed bytes** (a per-consumer sidecar, as the floor carrier already does; the copier model compares against last-rendered), not current source. Tier-3/fleet refinement, filed under FU-1.
- **Two follow-ups filed (not built — building them in P2 would breach the no-big-bang boundary):** **FU-1 (#245)** add-path status-awareness — the add-path is blind to `status: removed`; teaching it to honor removed (skip re-adding, threading the prune-sweep's removed-set into `apply`) is the general fix for anchor-coupled / identified-by-content entries. **FU-2 (#246)** — `hub-toc-hooks` cannot be cleanly pruned until FU-1 lands; gate any future toc-check retirement on FU-1.
- **Scope preserved.** Exactly one component, one consumer, one carrier's remove leg; fleet is P6, gated later.

## Alternatives considered

- **A `deprecated` tier before `removed`.** Rejected (D3): coordination value only for uncontrolled consumers we don't have; its failure mode is the add-only limbo being eliminated.
- **Prune as a separate `--prune` invocation.** Rejected: the declarative Terraform model is converge-on-remove; a present prune is gated by the destroy-confirm instead.
- **A separate `TOMBSTONES.md` log.** Rejected: no new files without cause; the retained manifest entry + JOURNAL + this ADR are the append-only record.
- **Keep `hub-toc-hooks` and accept the re-create churn.** Rejected: non-idempotent and spuriously re-adds a hook; fails the clean criterion-4/5 proof. Deferred to FU-1/FU-2.
