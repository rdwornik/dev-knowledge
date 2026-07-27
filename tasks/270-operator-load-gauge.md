---
id: "[#270]"
title: "Operator-load gauge"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
source: BACKLOG.md
derived: true
---

- [#270] [P1][M] Operator-load gauge — the gating FIRST element of any Tier-2 nightly layer (standing operator ruling; filed by #268 Arc-2): a funnel-count `[load]` section in the existing `fleet_health.py` SessionStart digest (open nightly-triage Issues · pending closure proposals · disposition-register rows · ARCHITECT-REVIEW-PENDING markers · open BACKLOG by priority) + a gitignored `logs/OPERATOR-LOAD.csv` row per run, per the build-ready plan-only design (its ex-ante success metric + pre-registered kill criterion ARE this item's contract) · Done when: the `[load]` line renders in the SessionStart digest from live counts AND the CSV appends per run AND the ex-ante metric + kill criterion are recorded in the closing commit · refs docs/audits/2026-07-05-draft-tier2-nightly-layer.md, docs/audits/2026-07-04-fable-architecture-review.md §5, scripts/fleet_health.py, #123
