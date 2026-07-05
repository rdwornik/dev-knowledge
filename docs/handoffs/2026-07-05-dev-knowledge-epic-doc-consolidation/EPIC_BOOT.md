# EPIC HANDOFF — doc-consolidation · 2026-07-05
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | 2026-07-05-dev-knowledge-epic-doc-consolidation |
| **Mode** | **epic** — one epic end-to-end, inside a root-provisioned worktree (ADR-97; HANDOFF_PROCESS §14a) |
| **Repo** | .dev-knowledge |
| **Date** | 2026-07-05 |
| **Epic branch** | `epic/doc-consolidation` (root-provisioned; bundle generated on `docs/2026-07-05-wave2-prep`) |

## Boot (epic lane)

You are an **EPIC-CHAT lane** (HANDOFF_PROCESS §14a; ADR-97). The root architect owns ADR
acceptance, backlog structure, parallelism rulings, and ALL merges to main. On load reply:
"Epic lane doc-consolidation booted — worktree + boundary acknowledged."

## Worktree + branch

Worktree `epic-doc-consolidation` (root-provisioned — never self-provisioned) · branch
`epic/doc-consolidation`. **RELATIVE PATHS ONLY** (the absolute-path-bypasses-worktree lesson is a
hard rule). Commit-per-story; **commit-and-STOP** — no merges to main.

## Epic scope (the BACKLOG slice)
<!-- FILL-IN:scope START — ROOT authors: epic id · stories in order · done-when per story -->
Epic id **[#258]** (BACKLOG · Canonical-file integrity · "Epic 3 — doc-consolidation"). Stories in order:

1. **S1 — ESSENTIALS back to charter**: a true 1–2-page session frame; every detail lives ONCE in PLAYBOOK (pointer, not copy); SUPERSEDED-inline sections and duplicated blocks removed. **The full deletion list travels in the EPIC RETURN for operator approval BEFORE merge** (never-delete-without-ask). Done when: ESSENTIALS ≤ its charter length with zero canonical detail duplicated against PLAYBOOK (spot-checkable).
2. **S2 — PLAYBOOK absorbs orphaned canonical detail**: anything S1 removes that lives nowhere else lands in PLAYBOOK first. Done when: no canonical detail is lost (each removal is a pointer to its PLAYBOOK home or an operator-approved deletion).
3. **S3 — CLAUDE.md generability phase 1** (2026-07-05 Tier-3 draft): derive the derivable ~35–40% via the roster @import seam; hand-synced ADR/command lists → generated. Done when: phase-1 sections are generated-not-authored.
4. **S4 — #220 (semantic-currency)**: advance ONLY if it falls out naturally from S1–S3; else leave untouched.
<!-- FILL-IN:scope END -->

## Epic done-contract (ex-ante, immutable to this lane)
<!-- FILL-IN:done-contract START — the hard closure metric for the WHOLE epic -->
ESSENTIALS ≤ its charter length with **zero canonical detail duplicated against PLAYBOOK** (spot-checkable), generability phase-1 sections **generated-not-authored**, gates green on branch. Closure is claimed on this metric — never on "docs edited" or "committed". The S1 deletion list is operator-approved via the EPIC RETURN before any merge.
<!-- FILL-IN:done-contract END -->

## FILE-BOUNDARY (hard)
<!-- FILL-IN:boundary START — may-touch / may-NOT-touch; disjoint from every concurrent epic -->
**May touch:** `protocols/ESSENTIALS.md` · `protocols/PLAYBOOK.md` · hub `CLAUDE.md` (**generability seam only**) · new generator script if needed under `scripts/` · own BACKLOG block ([#258] checkboxes only) · `JOURNAL.md` (append).
**May NOT touch:** `ARCHITECTURE.md` · `scripts/audit.py` · `templates/` · `deploy/**` · `ecosystem/doc-counts.md` (**FORBIDDEN** — the root regenerates it once at integration).
A needed file outside the boundary → STOP, escalate — don't touch. 3 lanes = the ADR-97 cap ceiling — this lane spawns no sub-work outside its worktree.
<!-- FILL-IN:boundary END -->

## Escalation
<!-- FILL-IN:escalation START — epic-specific triggers beyond the standing set -->
Epic-specific: (1) **any deletion beyond the S1 list mechanism** — deletions ship ONLY via the EPIC-RETURN-approved list, never inline; (2) a PLAYBOOK restructure beyond absorbing S1's orphaned detail (renumbering chapters, moving sections — collides with #213's serialized scope) → STOP, return to root; (3) a generability seam that would require touching `deploy/manifest-v*.yaml` or the roster generator's contract → escalate. Standing set (always): ADR-worthy fork · boundary-breach need · cross-epic dependency discovered → STOP, return to the root. Everything intra-epic is the lane's own judgment.
<!-- FILL-IN:escalation END -->

## Refusals (standing — not editable by the lane)

No merge to main · no ADRs · no backlog structure (checkboxes inside this epic's own block
only) · no worktree lifecycle ops · no new top-level folders · no content deletion without
operator ask.

## EPIC RETURN (required before any merge)

Close the lane by filling `EPIC_RETURN.md` in this bundle (§14b): commits + branch state ·
contract-vs-outcome per story · self-adjudications · proposed BACKLOG delta ·
merge-readiness. The root reviews the return against this contract → serial `--no-ff` merge →
applies the backlog delta → declares closure → tears down the worktree.

## Probes

Boot on `PROBES.md` (this bundle) — live-state probes scoped to this epic's boundary
(HANDOFF_PROCESS §5 contract: question + source-locator + command, **never the answer**).

> **Operator note.** Paste THIS file + `PROBES.md` into the fresh epic chat. Epic mode
> assembles no `PASTE_THIS.md` — the v5 paste manifest is architect/execution-shaped
> (requires `RESIDUAL.md`); the EPIC_BOOT scope-contract IS the paste.
