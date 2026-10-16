---
id: "[#1590]"
title: "Each of the 21 DEAD organs and 11 UNEXPLAINED files is used, wired or removed (R112)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1590] [P2][M] **Each of the 21 DEAD organs and 11 UNEXPLAINED files is used, wired or removed (R112)** - system map 88f1bc52 lists 21 DEAD organs (18 'no trigger (manual)': audit-health, audit-title-gate, check-seal-identity, coherence-nudge, decision-coverage, derived-copies-rebind, doc-counts-pytest-freshness, graph-edge-class-census, graph-orphan-census, graph-process-list, graph-rebuild, graph-task-coverage, lane-contract-check, normalize-dated-headers, prepend-order, ruff, toc-freshness-playbook, validate-backlog; 3 DISARMED: block-onedrive.ps1, surface-closures.ps1, claude-notify.ps1) and 11 UNEXPLAINED files (`.claude/agents/artifact-reader.md`, six `ecosystem/*baseline*`/registry files, `ecosystem/excluded-roots.yaml`, `ecosystem/substrate-registry.yaml`, two plugin files) (`docs/audits/2026-10-14-technical-how-work-runs.md` A4). `[#1533]` `[#781]` are the neighbours; the worktree-system-map branch did not land (no such ref on origin) · Done when: RED first: a test over the file-purpose graph asserts zero organs in state DEAD and zero UNEXPLAINED files, each former item either carrying a trigger, a wiring edge, or deleted by a ruling; fails on 97bcd374 · touches: `ecosystem/`, hooks config, per item · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1533]`, `[#781]`, `[#927]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
