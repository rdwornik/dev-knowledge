---
id: "[#296]"
title: "`audit.py repo <name> --repo-path` doesn't persist its report"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#296] [P3][S] `audit.py repo <name> --repo-path` doesn't persist its report (ai-council pilot G6) — `python scripts/audit.py repo <name> --repo-path <consumer>` exits 0 and prints `Report: …docs/audits/<date>-<name>-audit.md`, but the file is NOT created and no state.yaml/history/report is written, while the `--help` claims "Same state.yaml / history / report writes as `run`" — so a hub-side per-repo `floor_integrity` verdict can't be captured to disk under the `--repo-path` override (likely the override path suppresses the report write, or an exception is swallowed). · Done when: `audit.py repo <name> --repo-path <path>` writes the report it prints (or the `--help` is corrected to state it doesn't), with a test · refs scripts/audit.py, #215 · serialize-group: audit-py
