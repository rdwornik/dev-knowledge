---
id: "[#555]"
title: "Closing campaign batch 1 + kill-candidates instrument"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#555] [P1][M] **Closing campaign batch 1 + kill-candidates instrument** — the detector-fed batch whose output is CLOSED OR KILLED ROWS rather than new findings, plus the instrument that makes the kill half real: a `kill-candidates:` assertion is forced at BIRTH and never REVISITED, so a row born naming its rivals is never weighed against them — the instrument is that collection step. Three live denominators disagree (194 open · 218 bullets incl. deferred · a `SessionStart` gauge agreeing with neither), so the first act is to name ONE predicate and make the gauge use it. · Done when: the first batch closes **net-negative** — closures strictly greater than births — measured against the live denominator at that batch's close, with the before/after figures both re-derived rather than carried · refs docs/audits/2026-08-16-census-nb4-closing-campaign.md, docs/intake/2026-08-17-tech-fleet-config-standardization.md, #277, #552, #534, #348, #270 · kill-candidates: none — the campaign IS the kill mechanism, so a row proposing it cannot be dispatched by it; [#552] owns audit disposition and [#348] grooming CADENCE, neither of which closes a backlog row · source: the removed prose (NB4-E class census, denominator arithmetic) is carried in full by `docs/audits/2026-08-16-census-nb4-closing-campaign.md`
