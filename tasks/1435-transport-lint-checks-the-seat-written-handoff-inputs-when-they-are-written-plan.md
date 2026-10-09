---
id: "[#1435]"
title: "transport_lint checks the seat-written handoff inputs when they are written: PLAN-HANDOFF section 4, the LEDGER token, RATIFICATION names"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1435] [P1][M] **transport_lint checks the seat-written handoff inputs when they are written: PLAN-HANDOFF section 4, the LEDGER token, RATIFICATION names** - The seat-written inputs of a handoff cut are checked only at the last step: the five SUPPLEMENT labels by `assert_supplement_fixed_slots` inside the `--filled` re-render (`gen_handoff.py:2402`, `:3397`), the LEDGER `refreshed` token and the RATIFICATION date by the preflight. `transport_lint` checks names, folders and `carried-by` heads only, and the registry admits any `RATIFICATION-*.md`. PLAN-HANDOFF v4's labels failed at the cut, and the cut-day files were found stale at the cut (readiness digest F6, F8; the tooling-defect row "seat-input formats are checked only at the last step" and fix (c) of R90, filed as one row because the fix is the defect's whole remedy) · Done when: `transport_lint check` and the transport write hook fail (1) a `PLAN-HANDOFF-*.md` whose section 4 lacks the exact heading or any of the five labels, judged by gen_handoff's own fixed-slot function, never a copy; (2) a `LEDGER-<repo>.md` with no anchored `refreshed YYYY-MM-DD` token in its head (`_LEDGER_REFRESHED_RE`); (3) a `RATIFICATION-*.md` whose name is not `RATIFICATION-YYYY-MM-DD` plus an optional `-...-superseded` suffix, whose name date differs from its `date:` head, or that is a second live file for one date; a test per leg · owner: `scripts/transport_lint.py`'s owner · touches: `scripts/transport_lint.py`, `ecosystem/transport-registry.yaml`, tests · kill-candidates: `[#1371]` -- it owns the transport grammar; these three checks extend it · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` · refs scripts/transport_lint.py, ecosystem/transport-registry.yaml
