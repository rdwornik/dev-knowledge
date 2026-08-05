---
id: "[#493]"
title: "B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#493] [P2][S] **B-2 investigation — the scheduled fleet-baseline task has been silent 10+ days** — read-only diagnosis, findings only; the fix is a separate decision. Silence is the failure mode that looks identical to health, which is why this is filed rather than watched: nothing in the surfacing path distinguishes "ran clean" from "never ran". Scope is why it stopped and what evidence would have shown it stopping sooner. · Done when: the cause is identified with evidence, and the report names the signal that would have surfaced the silence within one cadence · refs scripts/fleet-baseline.task.xml, scripts/setup-fleet-scheduler.ps1, scripts/fleet_health.py · kill-candidates: none — no open row owns the scheduled-task liveness question
