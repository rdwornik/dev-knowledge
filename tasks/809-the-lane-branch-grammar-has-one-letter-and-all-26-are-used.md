---
id: "[#809]"
title: "The lane branch grammar allows one batch letter and all 26 are spent; widen it, never recycle"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#809] [P1][S] **The lane branch grammar allows one batch letter and all 26 are spent; widen it, never recycle** - Operator ruling 2026-09-16, filed with `[#788]`/`[#804]` because it is the same root cause: **an identifier space with no allocator.** `validate_branch_naming.LANE_BRANCH_RE` is `^worktree-lane-[a-z]-\d+-...`: one letter. Every letter a-z has been used by a past batch (measured over merge subjects on all refs), and batch AA's `worktree-lane-aa-*` branches never matched, so under an OPEN manifest its merges would still have received NO ADR-110 exemption -- which is why `audit-health` fired on every intermediate commit of that integration. `gen_lane_contract emit` refuses the same slugs (`lane-ab-808-...` measured refused 2026-09-16), so batch AB had to emit with `--loose-slug`. **Recycling a letter is ruled out by name:** it reproduces the id-collision failure in branch names. · Done when: (1) the grammar admits a multi-letter batch token (at least `[a-z]{1,3}`) in `LANE_BRANCH_RE`, the single definition every consumer imports; (2) `gen_lane_contract` and the dispatch verbs accept it without `--loose-slug`; (3) RED-first: `worktree-lane-ab-808-guard-timeout` matches and receives the ADR-110 exemption under an open manifest; a recycled letter already present in history is refused where a batch token is allocated; (4) the batch token is allocated by the same mechanism as task ids (`[#804]`), not chosen by a seat · refs `scripts/validate_branch_naming.py`, `scripts/batch_manifest.py`, `scripts/gen_lane_contract.py`, `[#788]`, `[#804]`, `[#510]` (exemption scope) · kill-candidates: none -- `[#804]` owns the allocator; this row owns the grammar it allocates into · source: operator ruling 2026-09-16, batch AB manifest
