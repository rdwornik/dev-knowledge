---
id: "[#460]"
title: "fleet-audit dailies — REPLICATION MECHANIZED: push leg + divergence alarm live, origin current, [#254]'s durability goal discharged"
status: closed
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#460] [P2][S] **fleet-audit dailies — REPLICATION MECHANIZED: push leg + divergence alarm live, origin current, [#254]'s durability goal discharged** — the lane was never dead: the host check showed the task Ready, LastTaskResult=0, 0 missed runs, with 51 uninterrupted local commits. What was dead was the one-shot MANUAL push, owned solely by [#254] and closed on an existence-shaped Done-when (`origin/…` "exists and tracks") that a single push satisfied while its DURABILITY goal went unmet. **BUILT 2026-08-01: (a)** `_push_routine_branch`, called from `_commit_routine_outputs` right after `update-ref` — replication belongs to the act that creates the commit, not to a separate organ that can die alone (which is how the manual push died); LOUD at ERROR, never raises, non-interactive and timeout-bounded for the unattended lane. **(b)** `check_fleet_audit_replication` in ALL_CHECKS (36→37) as the persistence backstop — graduated 0 / 1–3 / >3, remote-tracking-ref only so it needs no network. RED-first (11 tests), and the alarm fired on the REAL 51-commit divergence before the fix. **Origin brought current in-arc: 98→149, ahead 0, behind 0.** [#254]'s undischarged durability goal is discharged HERE. · Done when: DONE — mechanism live, origin current, alarm RED-tested then GREEN · refs scripts/audit.py, ADR-80, ADR-84, #254, #465 · kill-candidates: none — closed · serialize-group: settings-json
