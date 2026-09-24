---
id: "[#987]"
title: "Batch close regenerates the ledger from the state store -- it stops going stale for days"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#987] [P2][M] **Batch close regenerates the ledger from the state store -- it stops going stale for days** - D29: `to-browser/LEDGER-dev-knowledge.md` went unupdated for 3 days this window because updating it is a prose duty with no trigger · Done when: the batch-close step regenerates the ledger from ADR-121's state store (D25) rather than by hand; a witness batch close produces a ledger update in the same commit/act as the close, with no operator prompt required · implements: ADR-120 · refs `to-browser/LEDGER-dev-knowledge.md`, branch `worktree-lane-adr-state-store` (ADR-121), `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row wires ledger regeneration to batch close; depends on D25's state store landing
