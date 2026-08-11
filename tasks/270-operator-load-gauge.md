---
id: "[#270]"
title: "Operator-load gauge"
status: closed
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#270] [P1][M] Operator-load gauge — the gating FIRST element of any Tier-2 nightly layer (standing operator ruling; filed by #268 Arc-2): a funnel-count `[load]` section in the existing `fleet_health.py` SessionStart digest (open nightly-triage Issues · pending closure proposals · disposition-register rows · ARCHITECT-REVIEW-PENDING markers · open BACKLOG by priority) + a gitignored `logs/OPERATOR-LOAD.csv` row per run, per the build-ready plan-only design (its ex-ante success metric + pre-registered kill criterion ARE this item's contract) · Done when: the `[load]` line renders in the SessionStart digest from live counts AND the CSV appends per run AND the ex-ante metric + kill criterion are recorded in the closing commit · refs docs/audits/2026-07-05-draft-tier2-nightly-layer.md, docs/audits/2026-07-04-fable-architecture-review.md §5, scripts/fleet_health.py, #123 · **CLOSED 2026-08-11 — closing commit `7e4d503e`** (G-5 closing-commit metric, `STANDING_RULINGS.md` I-D10: this row adopts the convention, so it closes NAMING the commit that satisfies its Done-when). All three legs verified at that commit: (1) the `[load]` line renders in the SessionStart digest from live counts, each cross-checked against its own producer (triage 15 == the same session's `surface_triage.ps1` line; dispositions 27; backlog 7/91/100; review-pending 2); (2) `logs/OPERATOR-LOAD.csv` appends exactly one row per digest run, header-stable, pinned through the real `refresh()` path; (3) the ex-ante metric + kill criterion are recorded in the closing commit. Hardened by five `gpt-5.6-terra` passes (16 HIGH, all fixed or dispositioned; artifact `docs/audits/2026-08-11-codex-lane-b-270-load-gauge.md`). Landed by batch-4 lane W2, contract `docs/audits/2026-08-11-technical-batch-4-w2-lane-contract.md`; closed in the integrator's remit per operator ruling 2026-08-11, which also strips the inbound `depends-on: #270` clauses of [#271] and [#348] in the same commit (precedents 79047095, 40ce3189).
