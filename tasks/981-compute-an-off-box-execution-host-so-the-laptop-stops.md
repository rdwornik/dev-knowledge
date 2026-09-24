---
id: "[#981]"
title: "Compute: an off-box execution host, so the laptop stops being the harness's substrate"
status: open
priority: P2
size: L
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#981] [P2][L] **Compute: an off-box execution host, so the laptop stops being the harness's substrate** - D22: the laptop cannot carry the harness at its current concurrency (repeated OOM, reaper kills, a 3 GB launch floor with at most 2 heavy seats); ADR-121 (Proposed, unmerged branch `worktree-lane-adr-state-store`) names a persistent Linux VM (16 vCPU / 64 GB) plus Actions large runners as the compute answer · Done when: the compute decision in ADR-121 (or its successor) is ratified by the operator (per `to-cc/PLAN-WAVE5-2026-09-23.md` §4 item 3) and at least one lane runs end-to-end on the off-box host, with laptop memory pressure during that run measured near 0 · implements: ADR-120 · refs branch `worktree-lane-adr-state-store` (ADR-121, unmerged), `to-cc/PLAN-WAVE5-2026-09-23.md`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row provisions an off-box execution host; depends on the operator's ADR-121 ratification
