---
id: "[#361]"
title: "ADR-immutability's real coverage is declared only in code, never in the protocol"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#361] [P3][S] **ADR-immutability's real coverage is declared only in code, never in the protocol** — `protocols/AI_COUNCIL_PROCESS.md:350` and `templates/claude-regions/critical-rules-records.md:3` assert ADRs, transcripts, handoffs and audits are all immutable, but `scripts/hooks/block_immutable_edits.py:83` scopes the guard to `/docs/decisions/transcripts/` only and states "Deliberately NOT `docs/decisions/` — ADRs are out of v1 scope". The exclusion lives in the hook source, so a reader of either protocol cannot tell that three of the four classes are ungated. Routes to W6. · Done when: the protocol states the guard's real scope, or the guard widens to match the claim · refs protocols/AI_COUNCIL_PROCESS.md, templates/claude-regions/critical-rules-records.md, scripts/hooks/block_immutable_edits.py · kill-candidates: none — a declaration-locus defect distinct from [#358]–[#360] · serialize-group: audit-py
