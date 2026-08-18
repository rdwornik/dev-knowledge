---
id: "[#557]"
title: "Three `[stale]` dispositions match no live WARN — the ADR-75 decoration-rule review"
status: closed
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
generates: BACKLOG.md
---

- [#557] [P3][S] **Three `[stale]` dispositions match no live WARN — the ADR-75 decoration-rule review** — `audit.py ship-gate` prints three `[stale]` lines, each an `ecosystem/disposition-register.yaml` entry whose WARN no longer fires: `warn-preflight-backlog-ids-310-292`, `warn-review-artifact-387b794a-repin-close`, and `warn-review-artifact-d62796ad-boot-acts`. ADR-75's decoration rule is that a disposition DECORATES a live warning; once the warning is gone the entry is dead weight, and the failure mode is specific rather than cosmetic — **a reader cannot distinguish a disposition that is holding something from one that is holding nothing**, so the register's apparent coverage silently overstates itself and every future "is this WARN already dispositioned?" question gets a less trustworthy answer. Each of the three needs a verdict, and the two verdicts are not the same act: a WARN that was genuinely FIXED means the entry is removed, whereas a WARN that merely MOVED or was renamed means the entry is re-pointed — removing a re-pointable entry would silently un-disposition a live finding. · Done when: `audit.py ship-gate` prints zero `[stale]` disposition lines, with each of the three either removed or re-pointed and the reason recorded in the register entry itself · refs ecosystem/disposition-register.yaml, ADR-75, scripts/audit.py, #241, #556 · kill-candidates: none — [#241] grooms UNDECLARED edges, which is the opposite direction (a finding carrying no disposition); nothing owns the inverse, a disposition carrying no finding · source: /handoff-verify P7, 2026-08-17 architect gate
