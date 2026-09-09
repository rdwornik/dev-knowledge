---
id: "[#648]"
title: "Two of R-6's six under-mechanised rules are still prose: locator staleness and dispatcher liveness gate nothing"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#648] [P2][M] **Two of R-6's six under-mechanised rules are still prose: locator staleness and dispatcher liveness gate nothing** — DECLARE-REVIEWS finding R-6 named six rules that failed in batches T and U and ruled that each becomes a refusal. Four have landed: the lane ceiling and the reviewer-model mismatch as `SeatRefusal` raisers in `scripts/seat_refusals.py`, intake-id allocation as `gen_intake_index.py --next-free`, and no-leftovers as the `stale_worktrees` organ. The remaining two are implemented and inert — `scripts/preflight_contract.py` computes both locator resolution and dispatcher liveness, and it appears in no `.pre-commit-config.yaml` entry and no `audit_checks` registry import, so `/preflight` is adoption-first by its own frontmatter. R-6's locator half was measured at 4 stale locators of 9 · Done when: locator staleness and dispatcher liveness each refuse from a wired gate stage, each with a trip-test that fails the moment the refusal stops raising and a passing-path test so it cannot satisfy the trip-test by refusing everything · refs DECLARE-REVIEWS §B R-6, `scripts/preflight_contract.py`, `scripts/seat_refusals.py`, `.claude/commands/preflight.md`, `[#642]` · source: DECLARE-REVIEWS R-6, filed by batch V lane V-4
