---
id: "[#657]"
title: "Orphan #33 — something outside the repo writes into it on a schedule the registry does not know"
status: open
priority: P1
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#657] [P1][S] **Orphan #33 — something outside the repo writes into it on a schedule the registry does not know** — the integrator witnessed seven `ecosystem/*/history/` files and one dated ecosystem-audit artifact appear and self-revert at about 01:00. The process census proves the repo contains no nightly Routine at all: zero `cron:` and zero `schedule:` declarations, and the one workflow present is push-triggered and report-only. So a writer outside the tree is editing the tree on a clock, and the census could not see it because the census reads the repo. This is the orphan class inverted — not a capability with no trigger, but a trigger with no declared capability · Done when: the writer is identified by name and host, its schedule is read from the scheduler rather than inferred from the artifacts, and it is either declared in the registry with its trigger or stopped · refs DECLARE-ORPHAN-DISPOSITION §6, the process-trigger census, `[#642]` · source: DECLARE-ORPHAN-DISPOSITION §6, filed by batch V lane V-4
