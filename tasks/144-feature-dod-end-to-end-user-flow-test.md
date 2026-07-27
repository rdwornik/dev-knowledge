---
id: "[#144]"
title: "Feature DoD = end-to-end / user-flow test"
status: deferred
priority: P3
size: M
theme: "[E3] Lessons feedback loop"
story: "[S10] Codify recurring patterns into the methodology"
source: BACKLOG.md
derived: true
---

- [#144] [P3][M] Feature DoD = end-to-end / user-flow test — sharpen ADR-81 (d) "deployed": a feature is not done until an automated test exercises the WHOLE sequence as a user would, not only unit tests. The general acceptance-contract requirement landed (ADR-81 amendment 2026-06-24 + PLAYBOOK Ch12.1, A2); REMAINING: the E2E/user-flow-specific clause + VERIFY-FIRST — does "in the cloud" mean CI / GitHub Action or cloud CC sessions? (sets where the E2E test runs) · Done when: ADR-81 (d) carries an explicit E2E/user-flow clause (or deferral) AND the "in the cloud" target is resolved · refs ADR-81 amendment, PLAYBOOK Ch12.1, #143 · origin: 2026-06-10 worktree-codification deferral · DEFER — peg: first witnessed "deployed" dispute
