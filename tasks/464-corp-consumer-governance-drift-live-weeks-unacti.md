---
id: "[#464]"
title: "corp-*/ai-council governance drift — five findings live 15–46 days, surfaced daily, zero consumption"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: environment
generates: BACKLOG.md
---

- [#464] [P2][S] **corp-*/ai-council governance drift — five findings live 15–46 days, surfaced daily, zero consumption** — fleet-audit deep review, all five confirmed identical in today's baseline dailies (`ecosystem/*/history/`): corp-sca-time-automation CLAUDE.md edited-then-never-re-reviewed (canonical_freshness FAIL, the lane's longest-running finding) plus three docs past the 30d cadence · corp-ops four canonical docs past cadence · corp-monorepo VISION past cadence + CONTRIBUTING `reconciled_with` malformed · ai-council CONTRIBUTING `unknown-spec` edge (declares handoff-process with no local spec to resolve against). Consumer-repo work — ADR-41, queue-only here; the persistence itself is [#460]'s triage-gap evidence. EVIDENCE GAP: 51 further baseline commits (2026-07-17 → 2026-08-01) exist LOCALLY ONLY — unpushed and unread; these five are confirmed only to the 07-16 cutoff. · Done when: each of the five is fixed in its repo or recorded accept-with-reason · refs ecosystem/, #367, #335, #460 · kill-candidates: none — #282/#320/#393 queue other consumer classes; none owns these five · serialize-group: environment
