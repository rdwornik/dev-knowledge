---
intake-id: 112
status: SEED
origin: "to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md (the outcome scoreboard UC1-UC10 and the Codespace acceptance spec), base main b6161972"
consumed-by:
---

# SEED -- the outcome scoreboard and the Codespace acceptance spec name gaps the backlog does not carry

The scoreboard judges the harness by ten operator use cases, each with an executable acceptance test and a status taken from the existing digests and LANE-ENDs (no analysis re-run). The Codespace acceptance spec (UC5) splits "a lane runs in a Codespace end to end" into seven checks. Two independent adversaries (Codex gpt-5.6-sol, Grok grok-4.20) attacked both; their objections and the answers are in `to-browser/DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md`.

Gaps with no open carrier, each filed as a row: the per-phase heartbeat and six injected failures ([#1551], spec item 4); the credential lifetime register ([#1552], item 2); two-then-six concurrent Codespace lanes under a core-hour cap ([#1553], item 6); a duplicate ask refused at distill ([#1554], UC9); ADR-123 step 1, the carved harness package ([#1555], UC10 and item 7).

Not filed, with the reason: UC8's per-row cost line duplicates `[#893]` and `[#1536]` (Codex P7), so it is an amendment owed to `[#893]` at its next lane: one line per closed row summing each phase's tokens and USD per vendor plus Codespace core-hours, a vendor that exposes no price shown in its native unit with a reason and kept out of the USD total. Copilot and grok pins (draft P3) are `[#1537]` (4)'s. A scoreboard data file (draft P1) was refused by both adversaries as a second status register. Corp-monorepo's own lane (ADR-123 step 2) is the consumer's row, not the hub's (core invariant 1).

A row decides nothing (ADR-111).
