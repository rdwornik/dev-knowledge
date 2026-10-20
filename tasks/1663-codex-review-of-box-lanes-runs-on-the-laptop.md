---
id: "[#1663]"
title: "Codex review of a box lane runs on the laptop against the pushed branch (defect 2; R151)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1663] [P2][S] **Codex review of a box lane runs on the laptop against the pushed branch (defect 2; R151)** - Codex `-s read-only` cannot run in a Codespace (bwrap); R151 (proposed 2026-10-19, to be landed from RATIFICATION v6): the review runs on the laptop against the pushed branch, with no new sandbox exception for boxes · owner: E2 lane. target batch: E2.1 · Done when: (1) the review step of a box lane is routed to the laptop and a contract that asks for Codex in a box is refused; (2) RED first: a test fails a box contract whose review role has substrate = codespace; real-use witness: one box lane's Codex review runs on the laptop against its pushed branch and its record carries the served model id · touches: `ecosystem/provider-registry.yaml`, contract lint · kill-candidates: none -- no open row routes the box review · refs `protocols/STANDING_RULINGS.md`, `to-browser/LEDGER-dev-knowledge.md` v238 defect 2 and R151 · decided-by: R143. Defect N9: a box lane reported VENDOR-FAIL (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`). Defect H27: R151 is not taught (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
