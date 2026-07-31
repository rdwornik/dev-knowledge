---
id: "[#460]"
title: "fleet-audit dailies — RECOMMENDATION recorded: stop the branch lane, keep the digest, add persistence-triage; decision stays the operator's"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#460] [P2][S] **fleet-audit dailies — RECOMMENDATION recorded: stop the branch lane, keep the digest, add persistence-triage; decision stays the operator's** — deep review of all 98 `automation/fleet-audit` commits (findings absorbed into #463/#464/#465): the lane finds real defects and their value dies twice — the branch is unread (one FAIL sat visible daily for 46 days, unactioned) and its commit leg is ALREADY DEAD since mid-July while the local writer still runs: the ADR-80 "durable record" silently stopped. Recommendation: (1) STOP the branch lane, decommission the dead scheduled task, record the ADR-80 divergence; (2) keep the SessionStart baseline + `logs/FLEET-HEALTH.md` as the sole live surface; (3) add persistence-triage: a finding live >N days auto-files a queue row (the consumer ADR-105 requires); (4) the ADR-106 system-python oddity dies with the task. Writer correctness is [#465]. · Done when: the operator accepts or amends the recommendation and the accepted shape is executed, both original divergences dispositioned · refs ADR-80, ADR-105, ADR-106, #419, #426, #463, #464, #465 · kill-candidates: none — [#419] owns the class, [#426] its coverage · serialize-group: settings-json
