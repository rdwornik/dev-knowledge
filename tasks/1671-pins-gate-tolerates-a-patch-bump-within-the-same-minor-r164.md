---
id: "[#1671]"
title: "The pins gate tolerates a patch bump within the same major.minor with a recorded line; a minor or major bump still refuses (R164, interim)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1671] [P2][M] **The pins gate tolerates a patch bump within the same major.minor with a recorded line; a minor or major bump still refuses (R164, interim)** - Seven CLI pin skews in the E2 night each blocked a box launch until a hand pin edit (`to-browser/DIGEST-E2-0-CLOSE-2026-10-20.md`, the pin skew row); the operator ruled a patch bump within the same major.minor is tolerated with a recorded line · owner: a codespace_parity lane · Done when: (1) RED first: a test shows the gate refusing a patch-only skew today; (2) the change tolerates a patch bump within the same major.minor and writes ONE recorded line (where: the `codespace-exec` receipt) and still refuses a minor or major bump; (3) real-use witness: the next `codespace-exec` after a CLI patch update passes the pins step with the line in the receipt; (4) the systemic alternative (no committed pins; `codespace-exec` passes the laptop's exact versions to the box) is judged by the harness map, not built · touches: `scripts/codespace_parity.py` · kill-candidates: `[#1664]` -- same gate for the claude CLI patch bump, one fix may close both; `[#1659]` -- same gate for agy · refs `[#1664]`, `[#1659]`, `protocols/STANDING_RULINGS.md` · decided-by: the operator, 2026-10-20, R164 (RATIFICATION-2026-10-20 v1), INTERIM under R166 -- to be graded by the harness map · source: lane e2-rows-r164 (`BATCH-E2-NIGHT-2026-10-19` v3)
