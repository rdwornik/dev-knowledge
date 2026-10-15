---
id: "[#1593]"
title: "Handoff docs stop contradicting each other: v5/v6 prose, the R30 conflict, four seats, three queue verbs, dispatcher routing"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1593] [P2][M] **Handoff docs stop contradicting each other: v5/v6 prose, the R30 conflict, four seats, three queue verbs, dispatcher routing** - v5/v6 prose lingers (`PROCESS:58,289-305,932,964`; `README:32,85`); `README:130` contradicts `README:84` on whether the browser runs the gate at boot; 'four seats' vs one chat per window; three queue verbs across docs; `SEAT-BOOT-dispatcher.md:229-231` routes opus by default against R101; `scripts/seed_runbook.py` cited but absent; 6,324 of 12,972 B of the bundle boot repeat in all four bundles; 81 files changed since HANDOFF_BOOT's last change (`docs/audits/2026-10-14-technical-handoff-gaps.md` Q3; `docs/audits/2026-10-14-technical-phase0.md:150-153`). The `/handoff-verify` leg is done by the night close-out PART 3 · Done when: RED first: a test over `protocols/HANDOFF_PROCESS.md`, `docs/handoffs/README.md` and the SEAT-BOOT files asserts no v5/v6 gate prose, one queue verb, no opus default for the dispatcher, and no citation of an absent script; fails on 97bcd374 · touches: `protocols/HANDOFF_PROCESS.md`, `docs/handoffs/README.md`, seat boots, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1450]`, `[#1538]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
