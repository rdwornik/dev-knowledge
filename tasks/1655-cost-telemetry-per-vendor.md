---
id: "[#1655]"
title: "Cost telemetry per vendor in every phase receipt (R144)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1655] [P2][M] **Cost telemetry per vendor in every phase receipt (R144)** - R144: cost is measured per vendor from real use; track T2 wrote the baseline but nothing records it per phase · owner: E2 lane. target batch: E2.1 · Done when: (1) each PhaseReceipt carries vendor, tokens and USD, and a script totals them per vendor; (2) RED first: a test fails a receipt with a vendor and no cost; real-use witness: the E2.1 close digest prints USD per vendor from the batch's own receipts, agreeing with `scripts/quota_watch.py` · touches: `scripts/quota_watch.py`, the PhaseReceipt writer · kill-candidates: none -- no open row totals cost per vendor · refs `protocols/STANDING_RULINGS.md`, `to-browser/DIGEST-COST-BASELINE-2026-10-19.md`, `to-browser/RATIFICATION-2026-10-18.md` R144 · decided-by: R144 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
