---
id: "[#1595]"
title: "The cloud and interactive substrates have a launcher or are removed (R112)"
status: open
priority: P3
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1595] [P3][M] **The cloud and interactive substrates have a launcher or are removed (R112)** - `dispatch.py --help` exposes no cloud verb; the interactive substrate has `start: none` (`docs/audits/2026-10-15-technical-verified-harness-map.md:84-85`; outcome scoreboard G12). The cloud verb is BUILD-2b with no row id · Done when: RED first: a test over `ecosystem/provisioning.yaml` asserts every substrate it lists has a launcher reachable from `dispatch.py --help` or is absent from the registry; fails on 97bcd374 · touches: `scripts/dispatch.py`, `ecosystem/provisioning.yaml`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#669]`, `[#1537]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
