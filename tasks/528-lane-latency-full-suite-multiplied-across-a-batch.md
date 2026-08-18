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

- [#528] [P1][M] **Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost** — witnessed 2026-08-14: full suite 1001 s, and a 4-leg batch lane pays that roughly once per lane plus once per merge, ~50 min wall-clock. Three legs, all required: (1) adopt pytest-xdist at the gate-run call sites, not just the tuned `verify` path; (2) codify the tiered-suite law — targeted in-lane, ONE full suite at integration; (3) emit `test_run` duration via the telemetry leg so the trend is measured, not felt. · Done when: (1) gate-run call sites use `-n auto --dist worksteal` (or a recorded reason one does not), (2) the tiered-suite rule is written in PLAYBOOK/ESSENTIALS, and (3) `test_run` duration events land via the telemetry leg — each with evidence in the closing commit · refs pyproject.toml, #256, #317, #278 · kill-candidates: none — #317 owns the verify-skill single-command shape and #278 impacted-test selection; neither owns the batch-wide gate-mesh cost · serialize-group: environment · **INTEGRATION 2026-08-15 (R7) — legs 1+2 merged `7d1f6ce0`; LEG 3 OWED after [#529]**, and `PLAYBOOK.md` L844/L866 still call the two night-2 audits unmerged drafts · source: docs/audits/2026-08-15-technical-528-legs12-packet.md (the six declined items) + the phase-1 packet (R5/R7)
