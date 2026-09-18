---
id: "[#908]"
title: "A token budget written in a prompt caps nothing -- enforce a hard cap where the agent is launched"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "BUILD MODE B2 integration order 2026-09-18"
generates: BACKLOG.md
---

- [#908] [P1][M] **A token budget written in a prompt caps nothing -- enforce a hard cap where the agent is launched** - BUILD MODE B2 (2026-09-18): the subagents used **1,194,094 tokens against an ordered 400,000**, and every lane blew its stated budget. The budget lived only as prose in the lane prompt, and nothing at launch read it. The architect has written a prompt-side budget four times running; each time it was prose posing as a mechanism (`a-token-budget-in-a-lane-prompt-is-not-enforced`). The cap has to live where the agent is started -- the dispatch verb, the Agent/Workflow launch, the `claude -p` child -- and it has to stop or refuse on overrun, not report after the fact · Done when: every launch surface this hub uses for a lane or subagent takes a numeric token cap from the lane contract and enforces it (it kills or refuses the run at the cap) rather than restating it; a witness run with a deliberately small cap is stopped at the cap and records ORDERED vs RAN tokens; any launch surface that cannot enforce a cap is named with the reason and barred from lane dispatch until it can; and no lane prompt carries a budget sentence the launcher does not enforce · implements: BUILD MODE B2 integration order 2026-09-18 · refs `[#907]` (spend by seat kind), `[#909]` (route read-only work off Claude first), `[#892]` (ordered != ran), `scripts/lane_cost.py` · kill-candidates: none -- no open row enforces a cap at launch; [#907] measures spend, this bounds it
