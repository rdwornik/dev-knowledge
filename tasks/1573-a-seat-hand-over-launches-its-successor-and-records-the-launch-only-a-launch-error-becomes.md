---
id: "[#1573]"
title: "A seat hand-over launches its successor and records the launch; only a launch error becomes an OPERATOR-ACTION"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1573] [P1][M] **A seat hand-over launches its successor and records the launch; only a launch error becomes an OPERATOR-ACTION** - no harness command starts a successor integrator or dispatcher; the seats record `GAP "seat successor is not auto-started (US-5/R94)"` (to-browser/SESSION-integrator-bu-2026-10-15.md:17-20,50; `to-browser/SESSION-dispatcher-bu-2026-10-15.md:19`); `[#1421]` covers cycle teardown, not start. The templates half lands in the night close-out PART 3; this row owns the recorded launch · Done when: RED first: a test over `seat_registry` asserts a hand-over writes a `successor-launched` event with the successor session id, and that an injected launch error is the only path that emits an OPERATOR-ACTION; fails on 97bcd374 · touches: `scripts/seat_registry.py`, `templates/integrator-order-template.md`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1421]`, `[#689]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
