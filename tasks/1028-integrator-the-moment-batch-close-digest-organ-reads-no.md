---
id: "[#1028]"
title: "integrator: the moment:batch-close digest organ reads no receipt, treating a whole batch as one lane"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1028] [P3][S] **integrator: the moment:batch-close digest organ reads no receipt, treating a whole batch as one lane** - WAVE5B-N1 close: `moment:batch-close` exits 0 but its `lane_digest` reports "receipt could not be read" for every launch job, memory-gate receipt and pairing registry -- it is fed the batch as ONE lane rather than per-lane. · Done when: the batch-close digest organ reads each lane's own receipt and reports per-lane, RED-first witnessed on a fixture batch of 2+ lanes · refs `logs/receipts/MOMENT-BATCH-CLOSE-DIGEST.json`, DIGEST-WAVE5B-N1-2026-09-25, `scripts/lane_digest.py`, `docs/audits/2026-09-26-technical-lane-rows-owed-2-provenance.md` · kill-candidates: none -- no open row tracks this organ gap
