---
id: "[#190]"
title: "General intra-file duplication detector"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#190] [P3][M] General intra-file duplication detector — a read-only WARN-only `audit.py` check for the "resident-copy drift WITHIN a file" class (a rule/disposition stated authoritatively in two places in one doc — the failure class this repo is named to kill). Deferred from #140: the `doc_rot` checker shipped the history-accretion / file-bloat / grooming-cadence categories and explicitly did NOT build intra-file duplication. #157 is the concrete CLAUDE.md §4/§5 file-lifecycle instance; this is the general detector (deterministic near-duplicate-block first; semantic/LLM dedup stays out per ADR-88 Principle 5 do-not-build). · Done when: a read-only check flags a seeded intra-file duplicated block (WARN, with tests), or it is explicitly closed as not-mechanizable · refs #140, #157, ADR-49, ADR-88 · serialize-group: audit-py · DEFER — peg: n=2 witnessed intra-file dup
