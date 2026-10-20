---
id: "[#1685]"
title: "ADR-101 hermetization has no admissible home for a phase receipt, so the chain's own output cannot be committed (P1)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1685] [P2][M] **ADR-101 hermetization has no admissible home for a phase receipt, so the chain's own output cannot be committed (P1)** - `logs/phase-receipts/...` and `logs/receipts/LANE-*/rN/` are both refused by the hermetization seal, so a `run_phase` receipt can only be committed with `--no-verify` · owner: a hermetization lane · Done when: (1) RED first: a staged phase receipt is refused today; (2) the seal allowlist names one receipt home; (3) real-use witness: a lane commits its phase receipts with hooks on · touches: `scripts/validate_hermetization.py` · kill-candidates: `[#345]` -- hermetization · refs `[#345]`, `[#300]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: DEFECT 1 (P1) in `to-browser/SESSION-e2-distill-pilot.md`
