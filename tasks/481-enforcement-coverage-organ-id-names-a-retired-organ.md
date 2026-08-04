---
id: "[#481]"
title: "`enforcement_coverage` organ id names a retired organ"
status: closed
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#481] [P3][S] **`enforcement_coverage` organ id names a retired organ** — `0c8647c2` repointed the ADR-85 probe at `block_unanchored_push` (pre-push) but deliberately kept `organ_id = "session_end_backpressure"`, so the id names a Stop-hook script while the probe measures a different organ at a different stage. A name that does not describe the measured thing is the seed of the exact class that window closed — a reader infers the wrong organ from the mesh output, digest and roster. Scope is the rename PLUS every keyed consumer: `deploy/manifest-v*.yaml` roster rows, `deploy/carrier_mesh.py` (`SEB_REL`, `_STOP_SENTINEL`, `_HUB_SEB`), `.claude/methodology-roster.md`, the fleet/enforcement digests — coordinated, not a string swap. · Done when: the organ id names the organ actually probed and every keyed consumer moves in lockstep, with a test, OR the mismatch is recorded permanent-defer-with-reason · refs scripts/enforcement_coverage.py, deploy/carrier_mesh.py, ADR-85, #240 · kill-candidates: none — no open row owns organ-id/organ-measured agreement; #240 owns the regression teeth, not the naming · serialize-group: audit-py
