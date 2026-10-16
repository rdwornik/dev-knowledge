---
id: "[#1581]"
title: "CI jobs report what they ran: a not-run job is not success, and the heartbeat, handoff-manifest and commit-gate jobs are green on main"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1581] [P1][M] **CI jobs report what they ran: a not-run job is not success, and the heartbeat, handoff-manifest and commit-gate jobs are green on main** - job `terra` is 'NOT RUN -- no provider credential' yet reports success; substrate-heartbeat `devcontainer build + L1 marker verify` fails; handoff-manifest fails `BD-manifest 5 file(s) differ`; commit-gate refuses (orphan-census 15, task-coverage 9) (`docs/audits/2026-10-15-technical-verified-harness-map.md:45-48,86`). `[#1441]` `[#1343]` `[#1422]` cover the pytest reds, the orphan census and the ruleset · Done when: RED first: (1) a test over `conductor.yml` asserts a job whose credential step is skipped ends neutral/skipped, never success; (2) a fixture of main's job results asserts each of the three named jobs success; fails on 97bcd374 · touches: `.github/workflows/conductor.yml`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1441]`, `[#1343]`, `[#1422]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
