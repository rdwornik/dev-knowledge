---
id: "[#99]"
title: "FLEET-HEALTH digest names the failing check per red repo"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
generates: BACKLOG.md
---

- [#99] [P3][S] FLEET-HEALTH digest names the failing check per red repo — today the digest shows `corp-monorepo !! 1 fail` with no check name; the operator needs a second command (`audit.py repo <name>`) to learn WHAT is red · Done when: a red repo's digest line carries the failing check name(s) · refs ADR-76, #85, ADR-36
