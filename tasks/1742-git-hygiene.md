---
id: "[#1742]"
title: "Git hygiene by mechanism"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1742] [P2][S] **Git hygiene by mechanism** - Git hygiene by mechanism: `seat_cycle run` removes the predecessor worktree and branch, `land_lane` teardown deletes the prep/parked branches it created, and `batch_janitor` gets a git-hygiene verb applying K1-STANDING -- stale worktrees, prep/parked branches and ancestor branches accumulate until a seat deletes them by hand (E1/E2 of 2026-10-26: worktrees and origin branches removed by hand); K1-STANDING (ruling E) is now a standing GO, so the cleanup belongs to the scripts that create the debris, not to a seat's memory · owner: integrator-e2-1 (`scripts/seat_cycle.py`, `scripts/land_lane.py`, `scripts/batch_janitor.py`) · Done when: (1) `seat_cycle run` removes the predecessor's worktree and branch only after BOUND and the verified stop, refusing when untracked files are present; (2) `land_lane` teardown deletes the prep/parked branches it created, tag first (`archive/<name>-<date>`, pushed) when the tip is not an ancestor of main; (3) `batch_janitor` has a `git-hygiene` verb applying K1-STANDING E1 (ancestors, `merge-base --is-ancestor` re-verified at delete time) and E2 (tag, push tag, delete), never `--force` over untracked work, never main, `automation/fleet-audit`, live-seat worktrees or unlanded lanes; (4) each has a RED test first and `gen_handoff.py --preflight-only` reports `git_hygiene` clean; (5) fate 2026-11-09: built-and-wired or removed (R121) · touches: `scripts/seat_cycle.py`, `scripts/land_lane.py`, `scripts/batch_janitor.py`, `tests/` · refs `[#1743]` · decided-by: the operator, 2026-10-26, RATIFICATION-2026-10-26.md rulings B and E (K1-STANDING) · source: `to-browser/RATIFICATION-2026-10-26.md`, `to-browser/e1-cleanup.log`; fate 2026-11-09 · filed by the integrator from the operator grant 1737-1743 (RATIFICATION-2026-10-26.md ruling B + D-ID; S-ID: no id beyond it)
