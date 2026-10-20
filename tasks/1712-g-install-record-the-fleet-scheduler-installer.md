---
id: "[#1712]"
title: "G-INSTALL: record setup-fleet-scheduler.ps1 as an installer, not a recurring process (R149)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1712] [P3][S] **G-INSTALL: record setup-fleet-scheduler.ps1 as an installer, not a recurring process (R149)** - the script registers the `fleet-baseline` scheduled task once; its fate is now `manual_until: 2026-11-09` with this id · owner: harness-fates lane · target batch: E2 · Done when: (1) RED first: a test shows an installer fate shape is refused today; (2) the installer is recorded as such; (3) real-use witness: `Get-ScheduledTask fleet-baseline` shows a run after the change (digest read it: ran 2026-10-18 09:00, result 0), and `logs/FLEET-HEALTH.md` is rewritten by it (last write 2026-10-15 15:58 was found stale) · touches: `ecosystem/harness.yaml`, `scripts/setup-fleet-scheduler.ps1` · kill-candidates: none -- no open row covers it · decided-by: R149 (operator, 2026-10-19) · source: G-INSTALL in `to-browser/DIGEST-E1-FATES-2026-10-19.md`
