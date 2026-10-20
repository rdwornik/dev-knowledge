---
id: "[#1701]"
title: "A lane may kill only its own process group: the contract template says nothing about pkill"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1701] [P2][S] **A lane may kill only its own process group: the contract template says nothing about pkill** - a lane ran `pkill -f pytest`, which matches every session's pytest on the laptop (`to-browser/SESSION-e2-subst-gate-2.md` REPAIR 1 quotes the slip); `grep -rn pkill scripts templates tasks` finds nothing, and `scripts/gen_lane_contract.py` emits no do-not line about killing processes · owner: a contract-template lane · Done when: (1) RED first: a test that the contract `gen_lane_contract.py` emits carries a do-not line naming the rule (kill only your own process group or children by pid, never by name pattern such as `pkill -f` or `taskkill /im`); (2) the emitter and the lane do-not list carry the line; (3) real-use witness: the next generated lane contract quotes the line · touches: `scripts/gen_lane_contract.py`, `tests/test_gen_lane_contract.py` · kill-candidates: none -- no open row names process killing · refs `[#1675]` · decided-by: the operator, 2026-10-20, LEDGER v261 / RATIFICATION v2 (R167-R175), ruling (5), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-e2-subst-gate-2.md` REPAIR 1 (D1 pkill scope)
