---
id: "[#1687]"
title: "`run_phase.py run` never passes `cli_record`/`model_requested`, so `served_model` is always null, and `--stdout` merges stderr into the CLI JSON (P3)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1687] [P2][M] **`run_phase.py run` never passes `cli_record`/`model_requested`, so `served_model` is always null, and `--stdout` merges stderr into the CLI JSON (P3)** - `build_receipt` is called without the CLI record so `served_model`/`model_reported` are null in every receipt, and `--stdout` captures stderr into the same stream, corrupting the JSON (a stray `'m' is not recognized` line appears in every claude run) · owner: a run_phase lane · Done when: (1) RED first: a receipt from a fake CLI record has a non-null served_model; (2) stdout and stderr are captured separately; (3) real-use witness: a real phase receipt shows the served model id · touches: `scripts/run_phase.py` · kill-candidates: `[#1653]` -- served model; `[#1600]` -- conductor dogfood · refs `[#1653]`, `[#1600]`, `[#1535]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: DEFECT 3 (P3) in `to-browser/SESSION-e2-distill-pilot.md`
