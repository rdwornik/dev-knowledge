---
id: "[#1653]"
title: "ADR-delta PhaseReceipt contract: role, effort, USD, usage, findings (R141, P3)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1653] [P1][M] **ADR-delta PhaseReceipt contract: role, effort, USD, usage, findings (R141, P3)** - R141: ADR-delta fixes the PhaseReceipt contract; track T1 found role, effort and USD missing and usage never filled, so the E2.2 queue runner has no honest receipt to read · owner: E2 lane. target batch: E2.1 (before the E2.2 queue runner) · Done when: (1) an ADR-delta draft names every PhaseReceipt field and its writer; (2) RED first: a test fails a receipt missing role, effort, usd or usage; real-use witness: one E2.1 lane's PhaseReceipt carries all four, filled by the harness and not by hand · touches: `docs/decisions/` (ADR-delta), the PhaseReceipt writer · kill-candidates: none -- no open row defines the PhaseReceipt fields · refs `protocols/STANDING_RULINGS.md`, `to-browser/DIGEST-PHASERECEIPT-ASIS-2026-10-19.md`, `to-browser/RATIFICATION-2026-10-18.md` R141 · decided-by: R141 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
