---
id: "[#231]"
title: "Consumer → hub feedback report"
status: deferred
priority: P3
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
source: BACKLOG.md
derived: true
---

- [#231] [P3][M] Consumer → hub feedback report — when a consumer session detects a methodology gap, ambiguity, or broken piece (including a failing #230 conformance self-test), it emits a STRUCTURED report destined for the hub so the hub can answer/fix, instead of the consumer guessing. Encodes the operating philosophy: when unsure, ask the hub and double-check; verification results flow back upstream. Sub-note (flag, do NOT do here): the philosophy line itself may belong in ESSENTIALS/PLAYBOOK — scope that when built, do not codify it in this item. · Done when: a consumer that hits a methodology gap/ambiguity/broken-piece emits a structured hub-destined report (schema + destination defined) rather than guessing · refs #230, #215, #221, ADR-41, protocols/ESSENTIALS.md, protocols/PLAYBOOK.md · DEFER — peg: first witnessed consumer-gap report
