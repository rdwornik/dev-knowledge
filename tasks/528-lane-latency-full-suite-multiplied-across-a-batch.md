---
id: "[#528]"
title: "Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: environment
generates: BACKLOG.md
---

- [#528] [P1][M] **Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost** — witnessed 2026-08-14: full suite 1001 s (16:41), and a 4-leg batch lane pays that cost roughly once per lane plus once per merge — ~50 min wall-clock for one 4-leg lane. Three legs, all required: (1) **adopt pytest-xdist in the gate runs** — already a dev dependency (`pyproject.toml` `pytest-xdist>=3.8`, #256/#317 lineage), but stray xdist workers were witnessed outside the tuned `verify` skill path, so gate-run call sites (not just `verify`) need the same `-n auto --dist worksteal` discipline; (2) **codify the tiered-suite law** — targeted suite in-lane, ONE full suite at integration only, already partially practiced (the W4a–d lane contracts ran targeted files) but never written down as doctrine; (3) **emit `test_run` duration via the 2026-08-14 telemetry leg** (intake #29 Fold A) so the trend is measured, not felt. Sibling of #317 (verify-cadence parallel default) and #278 (impacted-test selection) — narrower than both: this is the GATE-MESH multiplication cost across a whole batch lane, not one command's invocation shape. · Done when: (1) gate-run call sites use `-n auto --dist worksteal` (or a recorded reason one does not), (2) the tiered-suite rule is written in PLAYBOOK/ESSENTIALS, and (3) `test_run` duration events land via the telemetry leg — each with evidence in the closing commit · refs pyproject.toml, #256, #317, #278, docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md · kill-candidates: none — #317 owns the verify-skill single-command shape and #278 owns impacted-test selection; neither owns the batch-wide gate-mesh multiplication cost · serialize-group: environment
