---
id: "[#460]"
title: "`ecosystem/*/history/` dailies + `automation/fleet-audit` — RECOMMENDATION recorded: stop the branch lane, keep the digest, add persistence-triage; decision stays the operator's"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#460] [P2][S] **`ecosystem/*/history/` dailies + `automation/fleet-audit` — RECOMMENDATION recorded: stop the branch lane, keep the digest, add persistence-triage; decision stays the operator's** — deep review 2026-07-31 (all 98 branch commits / 36 digests 2026-06-15→07-16 scanned; findings absorbed into #463/#464/#465): the lane DID detect real defects and their value died twice — the branch is unread (corp-sca `canonical_freshness` FAIL visible daily since 06-15, unactioned 46 days) and the branch-commit leg is ALREADY DEAD (last commit 2026-07-16; the local writer still runs — today's dailies exist — so ADR-80's "durable record" silently stopped 15 days ago and nothing noticed). Recommendation: (1) STOP the branch-commit lane and formally decommission the dead scheduled task, recording the ADR-80 divergence; (2) keep the SessionStart baseline + `logs/FLEET-HEALTH.md` as the sole live surface; (3) add a persistence-triage leg — a finding live >N days auto-files/refreshes a queue row (that queue is the named consumer + consumption_path ADR-105 requires); (4) the SYSTEM-python oddity (ADR-106) dies with the task if stopped. Writer-correctness defects found in the same review are [#465], not this row. · Done when: the operator accepts or amends the recommendation and the accepted shape is executed with both original divergences dispositioned · refs scripts/audit.py, ADR-80, ADR-105, ADR-106, #419, #426, #463, #464, #465 · kill-candidates: none — [#419] owns the general class, [#426] its coverage · serialize-group: settings-json
