---
id: "[#1424]"
title: "W2 carries FOUNDATION lane 12: the commit-time hooks R66 moved to CI run as CI jobs"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
implements: "AMEND-BATCH-FOUNDATION-5-2026-10-03"
generates: BACKLOG.md
---

- [#1424] [P2][M] **W2 carries FOUNDATION lane 12: the commit-time hooks R66 moved to CI run as CI jobs** - FOUNDATION lane 12 `foundation-12-hooks-to-ci` (R66 A3/A4: hooks with no measured catches leave commit time and run as CI jobs, each verdict visible on push) was WAITING at FOUNDATION's close (`to-browser/STATE-BATCH-FOUNDATION.md:4`), and `to-cc/BATCH-B2-W1-2026-10-04.md:152` said it "joins the next wave, after W1-2 merges". It never launched in B2-W1, it is not in the W2 draft, and no row carried it, so `AMEND-BATCH-FOUNDATION-5` stayed partly unexecuted with no owner -- the 2026-10-07 readiness dry run found it (D12). The AMEND's other night lanes are carried: 8, 9, 10, 11 and 13 merged; lane 7 re-carried by b2-ci-poll e2ff4802 with its Done item 4 in [#1383] · implements: AMEND-BATCH-FOUNDATION-5-2026-10-03 · Done when: a fresh W2 contract re-checks the frozen contract's premises (`LANE-FOUNDATION-foundation-12-hooks-to-ci.md` N1-N6) at origin/main -- `dispatch-conformance` was retired 2026-10-05, so the moved set is restated with its evidence -- and meets that contract's Done items 1-5 (each moved check runs as a visible CI job; none runs at the pre-commit or commit-msg stage; commit time measured before and after; impacted-tests-guard records whether each block is real; close-out), with its merge on main · owner: the W2 render (a fresh lane contract) · touches: `.pre-commit-config.yaml`, `.github/workflows/conductor.yml`, `scripts/check_commit_message_type.py`, `scripts/impacted_tests.py`, tests · kill-candidates: none -- no open row carries lane 12 (`git grep -n -i hooks-to-ci -- tasks` = 0 before this row) · refs `LANE-FOUNDATION-foundation-12-hooks-to-ci.md`, `to-cc/AMEND-BATCH-FOUNDATION-5-2026-10-03.md`, R66 in `to-browser/RATIFICATION-2026-10-03.md`, `[#1383]` · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
