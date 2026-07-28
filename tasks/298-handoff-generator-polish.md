---
id: "[#298]"
title: "Handoff-generator polish"
status: deferred
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
generates: BACKLOG.md
---

- [#298] [P3][S] Handoff-generator polish — three ruled enhancements (2026-07-08): (a) EPIC_BOOT auto-pulls the relevant BACKLOG slice into the FILL-IN as an AUTO-PULLED draft — root still reviews/freezes (scaffold authority unchanged, ADR-81); (b) `--epic-slug` whose leading id is NOT a live BACKLOG task emits a WARN (never refuse — greenfield slugs stay legal); (c) WARN when `--epic-slug` is passed in a mode that ignores it (architect/execution/functional). · Done when: (a) EPIC_BOOT renders an AUTO-PULLED BACKLOG-slice draft inside the FILL-IN, (b) a non-live `--epic-slug` leading id WARNs (not refuses), and (c) `--epic-slug` in an ignoring mode WARNs, each with a test · refs scripts/gen_handoff.py, templates/handoff/epic/EPIC_BOOT.md.tmpl, ADR-81, ADR-98 · DEFER — peg: next handoff-group pass
