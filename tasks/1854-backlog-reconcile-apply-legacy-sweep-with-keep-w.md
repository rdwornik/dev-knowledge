---
id: "[#1854]"
title: "backlog_reconcile apply: legacy-sweep with KEEP witnesses K1-K3, R-1/R-2 and a byte-identical --revert"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1854] [P1][M] **backlog_reconcile apply: legacy-sweep with KEEP witnesses K1-K3, R-1/R-2 and a byte-identical --revert** - `scripts/backlog_reconcile.py` `apply` closes only what `load_ruling` names and edits `status:` only, leaving the manifest node that `gen_task_tree.py` `_scan_source` refuses for a closed task; the night sweep needs a SEPARATE `--sweep` path (the five-evidence-class apply is unchanged): rows whose git ADD-DATE is before 2026-10-01 close as `legacy-sweep` unless a KEEP witness holds (K1 protected, K2 alive in code in the last 30 days, K3 both step-1 families LINE P1/P2 agreed), rows filed since take step 2's R-1..R-3 from the step-1 table, every close goes through `close_row_plan` plus one `sweep-close:` line, and `apply --revert <class|ids>` restores task files and manifest nodes byte for byte from a tracked ledger · Done when: (1) tests/test_backlog_reconcile.py carries `test_sweep_a` .. `test_sweep_r` and passes on the lane tip's conductor.yml run; (2) the sweep commit regenerates BACKLOG.md and `generated_sha256` with `gen_task_tree.py --emit-source` and `gen_task_tree.py --check` exits 0 on it, the receipt line `SWEEP closed=<n> ... protected-closed=0 ... revert-check=byte-identical` is present · touches: `scripts/backlog_reconcile.py`, `tests/test_backlog_reconcile.py`, `tests/fixtures/backlog_reconcile/`, `docs/audits/2026-11-02-technical-backlog-night-sweep/`, `tasks/manifest.json`, `BACKLOG.md` (sweep status edits and node removals of `tasks/*.md`) · kill-candidates: none -- it extends the organ of [#1749] and closes no other open row by design · refs `scripts/backlog_reconcile.py` `load_ruling`, `apply_action`, `scripts/gen_task_tree.py` `close_row_plan` · source: to-browser/DIGEST-BACKLOG-NIGHT-SWEEP-2026-11-01.md; to-browser/DIGEST-BACKLOG-REVIEW-STEP2-2026-11-01.md section 3; to-browser/DIGEST-RULING-Q-SW-1-2026-11-02.md · decided-by: the operator, night sweep (pre-authorized) and architect ruling Q-SW-1 2026-11-02
