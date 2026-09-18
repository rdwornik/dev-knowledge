---
id: "[#904]"
title: "The branch-name validator rejects a recovered/ prefix -- does recovery work get a sanctioned prefix, or ride an author prefix"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
implements: "DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18"
generates: BACKLOG.md
---

- [#904] [P3][S] **The branch-name validator rejects a recovered/ prefix -- does recovery work get a sanctioned prefix, or ride an author prefix** - Architect declaration 2026-09-18 (`to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md` §4 W11). A recovery of unreachable commits (I2, batch AC close) could not be named `recovered/...`, because `scripts/validate_branch_naming.py` classifies it `unknown`, non-conforming (`classify('recovered/aa-13-790')` -> `unknown`). So it landed as `feat/790-runtime-resource-recovered` (`serial-arc`). A feature prefix on a branch that adds no feature misstates what it is. **This row files the question; it does not add the prefix.** Adding a prefix to the closed enum (`SERIAL_ARC_PREFIXES`, `LANE_PREFIXES`) is its own ruling, per PLAYBOOK Ch3 "Branch prefixes -- the closed enum" · Done when: a recorded ruling either (a) admits a recovery prefix, with its lifecycle (merge, or delete once the ruling on the recovered work is made), and `validate_branch_naming.py` plus the PLAYBOOK enum and core-invariant #5 are updated together; or (b) rules that recovery rides an existing prefix and names which one, recorded where the enum is documented · implements: DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18 · refs `scripts/validate_branch_naming.py`, `protocols/PLAYBOOK.md` Ch3, `[#508]` (closed); transport: `to-cc/DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md` §4 W11 · source: architect declaration 2026-09-18 · kill-candidates: none -- no open row governs the branch-prefix enum; `[#508]` is closed
