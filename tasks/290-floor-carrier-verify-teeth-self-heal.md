---
id: "[#290]"
title: "Floor-carrier verify-teeth + self-heal"
status: closed
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
generates: BACKLOG.md
---

- [#290] [P3][S] Floor-carrier verify-teeth + self-heal (residual of #275b) — the v1.3.x arm-command fix landed the 3-stage constant + tests only; two follow-ups remain: (a) give `carrier_floor.py` `detect`/`verify` teeth that ASSERT the 3-stage arm (today they pass on a 1-stage arm — verify checks only the verify leg); (b) relax `_ensure_settings` so a re-deploy against an already-armed 1-stage consumer self-heals the stale arm. Deferred deliberately: a DRIFTED verdict without the self-heal reports drift `apply` can't repair, and no consumer deploys from that lane — ships with the next real deploy. · Done when: `carrier_floor.verify` FAILs a 1-stage-armed consumer AND a re-deploy self-heals it to 3 stages, with tests · refs deploy/carrier_floor.py, deploy/release-v1.3.x-contract.md, scripts/arm_hooks.py, #131
