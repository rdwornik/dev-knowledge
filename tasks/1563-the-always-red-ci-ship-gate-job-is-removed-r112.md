---
id: "[#1563]"
title: "The always-red CI ship-gate job is removed with its never-matching handoff reader (R112, BUILD-2a slot 1, after the operator's GO)"
status: closed
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1563] [P1][S] **The always-red CI ship-gate job is removed with its never-matching handoff reader (R112, BUILD-2a slot 1, after the operator's GO)** - The `ship-gate` job (`.github/workflows/conductor.yml:577-624`) is advisory at job level, yet red on every run (66 s and 70 s, runs 38656374259 and 38725590391), and `ci_verdict` counts any non-success job as failing (`scripts/ci_verdict.py:535-550`), so it turns every merge verdict into PRE-EXISTING or REGRESSED. Its one reader, `gen_handoff._whole_repo_verdict`, never matches its anchored regex (`scripts/gen_handoff.py:813`; three receipts say "emitted no verdict line"). The integrator's ship-gate on the merged tree (`scripts/gates.py:176-181`) stays the verdict · Done when: RED first: (1) a test over `conductor.yml` finds no job running `audit.py ship-gate`; (2) `gen_handoff`'s ship-gate reader leg is gone and its handoff receipt carries no ship-gate field, with its tests updated; (3) a merge-verdict fixture shaped like run 38725590391 without the job yields no failing job from it; (4) `gates.py`'s per-merge ship-gate is untouched; (5) the tests fail on `b6161972` · touches: `.github/workflows/conductor.yml`, `scripts/gen_handoff.py`, tests · kill-candidates: none -- `[#1427]` records the BD-ci problem and stays open (grep `ship-gate job` over tasks/ 2026-10-15) · refs `[#1427]`, R112, `docs/intake/2026-10-15-tech-test-strategy-rows.md`. Defect H9: CI legs are defined in two workflows (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q3; the operator's GO is OQ3 · **CLOSED 2026-10-21** — carried by [#1672] (R165; operator GO 2026-10-21, LEDGER v271)
