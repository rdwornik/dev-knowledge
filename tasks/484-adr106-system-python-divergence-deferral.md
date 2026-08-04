---
id: "[#484]"
title: "ADR-106 system-Python divergence — named deferral, not an open build"
status: open
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: environment
generates: BACKLOG.md
---

- [#484] [P3][M] **ADR-106 system-Python divergence — named deferral, not an open build** — ADR-106 pins the toolchain via `uv`, but the machine still runs work through a SYSTEM Python alongside the locked one: the cp1252 console failures this window hit (`audit.py checks` at U+2192, [#470]; `desired_state_report.py` at U+21C4, found running the caches wave) are that divergence surfacing as encoding defects rather than as a version mismatch. Filed as a **named deferral, scope ~1 window**, rather than left as unowned drift: it is a fleet-wide environment change wanting its own window, not a corner of one. NOT a request to re-open ADR-106's ruling, which stands. · Done when: the system-vs-locked Python divergence is either closed on the operator's machines or recorded permanent-defer-with-reason, and the cp1252 console class is either fixed at the source or declared out of scope with a stated workaround · refs ADR-106, #470, scripts/desired_state_report.py · kill-candidates: none — [#470] owns ONE glyph in ONE script; this owns the environment divergence underneath it · serialize-group: environment
