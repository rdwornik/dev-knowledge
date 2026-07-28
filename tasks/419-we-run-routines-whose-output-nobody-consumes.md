---
id: "[#419]"
title: "We run routines whose output nobody consumes"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#419] [P2][M] **We run routines whose output nobody consumes** — the nightly conformance routine emits a digest every night and nobody reads it: six branches (`claude/conformance-2026-07-21` … `-26`) sit unmerged and unread, and the single High finding among them (07-21 F1 — ARCHITECTURE "four carriers" contradicted by five in `deploy/tool.py`) was fixed on main by `037d9f08` on 07-23 by a session that never opened the branch that found it; F1's ADR-92 half went unfixed as a direct result. Framed as the operator framed it: **the defect is that we run routines whose output nobody consumes** — the scope is how routine output reaches a decision, NOT branch cleanup (touch no branch). **Rule + gate landed 2026-07-26** (ADR-105 + its `audit.py` check); remaining live-routine coverage pegged to [#426]. STAYS OPEN. · Done when: every standing routine has a named consumer and a consumption path, and unconsumed output is surfaced rather than silently accumulating · refs #270, #271, #348, #409, #410, #411, ADR-80, the five conformance branches · kill-candidates: none — #270 gauges operator LOAD, not whether output is ever read · serialize-group: settings-json
