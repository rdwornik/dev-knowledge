---
id: "[#558]"
title: "`VISION.md` still describes `scripts/` as read-only validators — the third site of a correction that landed twice"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
generates: BACKLOG.md
---

- [#558] [P3][S] **`VISION.md` still describes `scripts/` as read-only validators — the third site of a correction that landed twice** — the live `## Vision` section reads *"the conventions it defines, and the read-only validators in `scripts/`"* (`VISION.md:15`). That is the same descriptively-false claim `CLAUDE.md` already corrected at TWO sites this month: §5 rule 4 (v2.61, re-scoped from *"`scripts/` contains read-only validators only"*) and §3 (v2.62). **Both of those entries recorded fleet-wide drift on this claim as reaching 0 sites** — `VISION.md` is the evidence that the count was measured over `CLAUDE.md` alone, which is the reusable finding here: a drift sweep scoped to the file being edited will keep reporting zero. Roughly 23 scripts under `scripts/` mutate state and `scripts/audit.py` pushes to `origin`, so the Layer-2 invariant is about not driving a CHILD repo's state, not about read-only-ness; the v2.61/v2.62 wording is the ready-made target (hub-local validators, generators and gates are in scope). **`VISION.md` is freshness-stamped** (`last_reviewed: 2026-07-25`), so the edit carries a `last_reviewed` obligation that means a genuine end-to-end re-read, not a touch — which is why this is a row and not a one-line drive-by. Surfaced by probe **P1a** of the 2026-08-17 architect handoff gate, whose forced live read of `## Vision` is exactly what a summary would have rounded off. · Done when: `VISION.md`'s `## Vision` no longer claims `scripts/` holds only read-only validators, converging on the `CLAUDE.md` §5 rule 4 wording, and a fleet-wide re-measurement of the claim covers files beyond `CLAUDE.md`; `last_reviewed` is re-stamped only if the file was genuinely re-read · refs VISION.md, CLAUDE.md §3 + §5 rule 4, ADR-28, ADR-36, #533 · kill-candidates: none — the `CLAUDE.md` corrections are landed and their entries closed; no open row owns `VISION.md`'s copy of the claim · source: /handoff-verify P1a, 2026-08-17 architect gate
