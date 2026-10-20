---
id: "[#1677]"
title: "`read_rehearsal` and `ci_red_age` call `gh` directly instead of through the shared reader (H2)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1677] [P3][S] **`read_rehearsal` and `ci_red_age` call `gh` directly instead of through the shared reader (H2)** - `scripts/merge_path.py:419` `read_rehearsal` and `scripts/ci_red_age.py:88` each shell out to `gh run list` with their own argv, a second reader of the same CI state beside the verdict readers · owner: a ci-verdict lane · Done when: (1) RED first: a test shows two gh call sites with different failure handling for the same run; (2) both read through ONE function; (3) real-use witness: `merge_path` rehearsal and `ci_red_age` agree on a real run id · touches: `scripts/merge_path.py`, `scripts/ci_red_age.py` · kill-candidates: `[#1427]` -- verdict readers · refs `[#1427]`, `[#742]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: H2 in `DIGEST-HARNESS-MAP-2026-10-20-ANNEX` C3
