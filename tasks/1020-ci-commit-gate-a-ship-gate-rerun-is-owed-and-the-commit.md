---
id: "[#1020]"
title: "ci-commit-gate: a ship-gate rerun is owed, and the commit-gate job's first live reds need triage"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1020] [P2][S] **ci-commit-gate: a ship-gate rerun is owed, and the commit-gate job's first live reds need triage** - Lane ci-commit-gate's own fix now makes the job run the repo-wide pre-commit hooks instead of skipping (DIGEST-WAVE5B-N1-2026-09-25 FINDING), which surfaces the repo's pre-existing reds on CI for the first time -- owed: the rerun and a triage of what it finds. · Done when: `scripts/audit.py ship-gate` is rerun on a fresh CI pass of the commit-gate job and its first live reds are each named (already-known vs new) · refs `.github/workflows/`, `scripts/audit.py`, DIGEST-WAVE5B-N1-2026-09-25 ROWS-OWED (ci-commit-gate) · kill-candidates: none -- no open row tracks this rerun · evidence 2026-10-03 (foundation-1-honest-green, DCT J2): the commit-gate job has been red since 6e9f0bb8 -- orphan-census 10, task-coverage 9, and audit-health `handoff_probes` "BD-ci toothless" -- on every main push run since; the registry's `audit-health` hook entry is tied to this row (owner `rob`, expiry 2026-10-31)
