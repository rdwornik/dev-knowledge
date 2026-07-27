---
id: "[#423]"
title: "The integration sequence runs on prose every time, never mechanized"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
source: BACKLOG.md
derived: true
---

- [#423] [P2][M] **The integration sequence runs on prose every time, never mechanized** — landing an arc takes eight steps, each earned from an incident: live-session enumeration across ALL `~/.claude/projects` dirs (a subset scan gave a false LIVE) · merge-subject scan (bracket `[#id]`, closes-set == true id set-difference, `^kill-candidates:`, no close-verb by an open id) · `--no-ff` · JOURNAL anchor on its OWN branch (a wrap commit after a merge lands direct-to-main) · exit codes read DIRECTLY, never via a pipe · push · teardown `-d` only. `/ship` automates three (merge, push, delete) and checks NO precondition, so the rest stay prose the operator re-types. Evidence: this arc lost two round-trips to prose defects — a dirty index called non-blocking when git refuses outright, and a `-d` refusal called an unmerged-work detector without its HEAD-on-main precondition. · Done when: `/ship` carries the sequence with each precondition checked mechanically, not remembered, or the gap is recorded permanent-defer-with-reason · refs plugins/tier1-lifecycle/commands/ship.md, ADR-70, #405, #414, #417 · kill-candidates: none — #405 owns leftovers, #414 self-acting-on-main
