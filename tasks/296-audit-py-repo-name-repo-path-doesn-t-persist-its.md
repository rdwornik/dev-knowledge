---
id: "[#296]"
title: "`audit.py repo <name> --repo-path` prints a report path that isn't there"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#296] [P3][S] `audit.py repo <name> --repo-path` prints a report path that isn't there (ai-council pilot G6) — the command exits 0 and prints `Report: …docs/audits/<date>-<name>-audit.md`, while `--help` claims "Same state.yaml / history / report writes as `run`". **Live repro 2026-08-06 CONFIRMS a misleading locator, not a lost report** — that path does NOT exist in the working tree and `git status` stays clean, but the report is real: it lands as a commit on `automation/fleet-audit` (ADR-80 replication), beside the `ecosystem/ai-council/history/` daily. So the printed path misleads any caller who looks where it points, and the row's original guess (a suppressed write or swallowed exception) is refuted. Row stays OPEN, re-aimed at the locator rather than at a missing write. · Done when: the command writes the report where it says, or prints where it actually lands, with a test · refs scripts/audit.py, #215 · serialize-group: audit-py
