---
id: "[#963]"
title: "State store ADR -- where the harness holds its operational state, which part is the truth, and where it executes"
status: open
priority: P1
size: L
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#963] [P1][L] **State store ADR -- where the harness holds its operational state, which part is the truth, and where it executes** - provenance ADR-120 (stages 13-16 read and write this state); order `to-cc/BATCH-ADR-STATE-STORE-2026-09-23.md` v3 + `to-cc/AMEND-ADR-STATE-STORE-2026-09-23.md` (ARCHITECT), answering the proposal `to-cc/DECLARE-STATE-STORE-LEARNING-2026-09-23.md`. Carrier row for the records of `lane-adr-state-store` (branch `worktree-lane-adr-state-store`): the draft `docs/decisions/ADR-121-operational-state-is-a-single-writer-event-log-on-a-git-state-ref.md` (Status: Proposed), the research record `docs/audits/2026-09-23-technical-state-store-research.md` (A1 state measurements, A2 git as an agentic tool), the compute record `docs/audits/2026-09-23-technical-compute-substrate.md` (Part B) and the debate record `docs/audits/2026-09-23-technical-state-store-debate.md` (Claude vs Codex `gpt-6-astra`, ai-council from its front door, the moderator record, the `gpt-6-sol` independent check). The row carries the records only; it builds nothing, and the ADR's migration steps become rows when the seat reads it · Done when: 1. The four records above are on `main`. 2. The operator has answered the ADR's one functional question (may a seat act on locally-saved, not-yet-pushed state?) and ADR-121's status line is edited on ratification (ADR-94) or the ADR is marked `Explored, not adopted`. 3. The ADR's migration steps 1-4 are filed as rows, each citing ADR-121 and carrying its exit criteria verbatim. 4. `to-browser/SESSION-lane-adr-state-store.md` exists and its landing is confirmed · refs ADR-120, ADR-118, ADR-110, ADR-108, `to-cc/DECLARE-TRANSPORT-SCHEMA-2026-09-23.md`, `to-cc/DECLARE-WAVE5A-VERIFICATION-2026-09-23.md`, `to-cc/DECLARE-OFFBOX-PORTABILITY-2026-09-23.md`, `[#929]`, `[#960]` · kill-candidates: none -- the row is the carrier for a decision record that no open row owns; `[#929]` (the loop evaluation behind ADR-120) and `[#960]` (lane-side verification) are neighbours it cites and does not absorb
