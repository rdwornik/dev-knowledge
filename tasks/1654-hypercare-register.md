---
id: "[#1654]"
title: "Hypercare register: a defect found in real use becomes a row (R143)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1654] [P2][S] **Hypercare register: a defect found in real use becomes a row (R143)** - R143: while E2 is in hypercare every defect found in real use is registered and filed as a row, not left in a digest · owner: E2 lane. target batch: E2.1 · Done when: (1) a register file lists each hypercare finding with its row id and status; (2) RED first: a test fails a register entry that has no `[#id]`; real-use witness: the nine defects of LEDGER v238 appear in it, each with its row from this lane · touches: a register file under `to-browser/` or `docs/`, one checker · kill-candidates: none -- no open row keeps a hypercare register · refs `protocols/STANDING_RULINGS.md`, `to-cc/BATCH-E2-0-2026-10-18.md` section 6, `to-browser/RATIFICATION-2026-10-18.md` R143 · decided-by: R143 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
