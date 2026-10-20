---
id: "[#1686]"
title: "`claude --json-schema` rejects the `PhasePayload` schema because `--payload-schema` prints a `$schema` key (P2)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1686] [P3][S] **`claude --json-schema` rejects the `PhasePayload` schema because `--payload-schema` prints a `$schema` key (P2)** - `run_phase.py --payload-schema` prints a schema with `$schema: https://json-schema.org/draft/2020-12/schema`; `claude --json-schema` answers 'not a valid JSON Schema: no schema with key or ref', and the first run FAILED until `$schema` was stripped by hand · owner: a run_phase lane · Done when: (1) RED first: the printed schema is passed to `claude --json-schema` in a test double and fails today; (2) the printer omits `$schema` for the claude path; (3) real-use witness: a claude phase runs on the first attempt · touches: `scripts/run_phase.py` · kill-candidates: `[#1653]` -- same file, served model · refs `[#1653]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: DEFECT 2 (P2) in `to-browser/SESSION-e2-distill-pilot.md`
