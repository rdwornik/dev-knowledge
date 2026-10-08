---
id: "[#1434]"
title: "ADR-129's 120-second handoff preflight bound does not hold on the operator's laptop"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1434] [P2][M] **ADR-129's 120-second handoff preflight bound does not hold on the operator's laptop** - Measured in the 2026-10-07 readiness dry run on the laptop (about 2.7 GB free of 27.7 GB): preflight 423 s (the live run 4 min 17 s), organ set 1,230 s, cut 1,537 s, probes 1,101 s, the `--filled` re-render 2,645 s. ADR-129 bounds the preflight at 120 s (readiness digest F14) · Done when: every cut receipt records each stage's wall time, and the bound is either met (the organ set made cheaper, e.g. P11's carriage resolution memoized) or restated from the measured figures by ruling · owner: ADR-129's owner (the architect seat rules the bound) · touches: `scripts/gen_handoff.py`, `scripts/verify_handoff_probes.py`, ADR-129 amendment · kill-candidates: `[#769]` -- a long gate with no cancel is the same cost seen from a lane · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
