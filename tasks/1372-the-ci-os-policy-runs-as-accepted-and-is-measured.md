---
id: "[#1372]"
title: "The CI OS policy runs as accepted and is measured before and after, and reverted if any measure worsens"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1372] [P1][L] **The CI OS policy runs as accepted and is measured before and after, and reverted if any measure worsens** - R72 (operator, 2026-10-04): the policy is accepted, with verification. Lane pushes run Linux with impacted tests only; the integration sha runs the full suite on both operating systems with Windows sharded; a push to `main` reuses that verdict once it is proven to be the same sha. Minutes per merge, Windows wall time and verdict correctness are measured before and after, and the change is reverted if any of the three gets worse. · Done when: a test over `.github/workflows/` shows the three rules (Linux impacted-only on lane pushes; both operating systems with Windows sharded on the integration sha; reuse on `main` only when the sha is identical); a recorded table gives minutes per merge, Windows wall time and verdict correctness for at least five merges before and five after; a worsening in any column is recorded together with the revert; the reuse test fails when the shas differ · owner: wave B2 W2: a CI-policy lane · touches: `.github/workflows/`, the verdict-reuse script, tests · kill-candidates: none -- `[#966]` makes CI's verdict the merge gate; the OS split and the sharding are not in its Done-when · refs `docs/decisions/ADR-127-ci-os-verification.md`, `[#966]`, `protocols/STANDING_RULINGS.md` section AR (R72) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R72 in `to-browser/RATIFICATION-2026-10-04.md R72`
