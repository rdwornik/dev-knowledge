---
id: "[#1699]"
title: "The R160 merge gate has no recorded-exception mechanism, so its one bootstrap exception was a chat decision"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1699] [P2][S] **The R160 merge gate has no recorded-exception mechanism, so its one bootstrap exception was a chat decision** - `merge_path.py land` with the R160 gate (`scripts/subst_gate.py:335` `handback_problems`) refused lane e2-subst-gate-2, the lane that builds the gate, because it was only ever started by the pre-gate `dispatch.py repair`, which wrote no LAUNCH receipt; the operator ruled one bootstrap exception (land under main's pre-gate `merge_path`, lane e2-subst-gate-2 only), and nothing in the gate can express or audit such an exception (`to-browser/SESSION-integrator-e2-0-2026-10-18.md` LAND e2-subst-gate-2 REFUSED, FINDING gate-defect) · owner: a subst_gate lane · Done when: (1) RED first: a test shows a lane with no LAUNCH receipt refused even when an operator ruling exempts it; (2) the gate reads an exception from data (one entry per exception: lane slug, ruling id, expiry date, reason) and accepts only a matching, unexpired entry, printing the ruling id in its verdict; an expired or unmatched entry still refuses; (3) real-use witness: one `merge_path.py land` whose verdict quotes an exception entry, and one refused after its expiry · touches: `scripts/subst_gate.py`, `scripts/merge_path.py`, one data file under `ecosystem/` · kill-candidates: `[#1670]` -- the substitution gate row; one change may serve both · refs `[#1670]`, `[#1666]` · decided-by: the operator, 2026-10-20 (answer to the integrator's gate-defect question, option A bounded), INTERIM under R166 -- to be graded by the harness map · source: `to-browser/SESSION-integrator-e2-0-2026-10-18.md` item RULING e2-subst-gate-2 bootstrap exception
