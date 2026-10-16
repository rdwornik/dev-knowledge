---
id: "[#1594]"
title: "Phase-0 residuals: R48 last-ran print, `lane_report.py`, stale ADR-121/ADR-125, Actions-minutes gauge and heartbeat timezone label"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1594] [P3][S] **Phase-0 residuals: R48 last-ran print, `lane_report.py`, stale ADR-121/ADR-125, Actions-minutes gauge and heartbeat timezone label** - no R48 registry/last-ran print; `lane_report.py` MISSING; ADR-121 and ADR-125 Proposed and stale; `quota_watch` still reports Actions 11,805 of 3,000 min (393.5%) against a historical private-repo allowance though the repo is public; lane b heartbeats label local time `Z` (`docs/audits/2026-10-14-technical-phase0.md:60,69,90-110`; `docs/audits/2026-10-15-technical-verified-harness-map.md:147,211`) · Done when: RED first: one test each: the R48 print exists, `lane_report.py` imports, ADR-121/125 carry a non-stale status, `quota_watch` marks the Actions row informational on a public repo, and a heartbeat timestamp parses as local time; fails on 97bcd374 · touches: per item, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#689]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
