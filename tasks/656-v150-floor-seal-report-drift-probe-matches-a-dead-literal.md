---
id: "[#656]"
title: "The v1.5.0 carrier's `floor-seal-report` drift probe matches a literal the command no longer has"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#656] [P2][S] **The v1.5.0 carrier's `floor-seal-report` drift probe matches a literal the command no longer has** — the manifest probes for the string `--report`; lane V-3 shipped a Click sub-command `report`, which is the correct shape under the dev standards. The browser ruled the probe string wrong, not the command: fix the probe. The class matters more than the instance and the ruling says so — a drift probe that matches a literal is itself a declared edge nothing verifies, so it fails silently in the direction that looks green · Done when: the `floor-seal-report` probe matches the shipped sub-command, a test fails if the command's invocation shape changes without the probe moving, and every other literal-matching probe in the manifest is read once and either re-anchored or recorded as deliberately literal · refs DECLARE-BATCH-V-MERGE §3, `deploy/manifest-v1.5.0.yaml`, `[#642]` · source: browser ruling on lane V-3's escalation, filed by batch V lane V-4
