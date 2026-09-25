---
id: "[#1010]"
title: "A Stop hook refuses to end a lane session without a machine `HANDBACK <branch> @ <sha> <kind>` line"
status: closed
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1010] [P1][S] **A Stop hook refuses to end a lane session without a machine `HANDBACK <branch> @ <sha> <kind>` line** - WAVE5A finding: the handback line's grammar is not enforced at write time; two handbacks reached the integrator 2-4 h late (test-selection: swallowed by orphaned poll loops; provider-registry: the HANDBACK line sat inside backticks, invisible to a caret-anchored poll), and one lane (`lane-one-registry-ci`) handed back with a `## HANDBACK` heading instead of the machine line entirely (`to-browser/SESSION-integrator-wave5a-2026-09-23.md`) · Done when: a Stop hook parses the session's own session file for the exact machine line before the session is allowed to end, and refuses (with a named reason) when it is absent, backtick-wrapped, or malformed; a witness run demonstrates the refusal on a synthetic malformed handback and passes on a clean one · implements: ADR-120 · refs `docs/audits/2026-09-24-technical-digest-wave5a.md` (MORNING > Findings (for rows; not filed tonight), 1st bullet -- "Two handbacks reached me late"), `to-browser/SESSION-integrator-wave5a-2026-09-23.md`, `[#971]` (the liveness watchdog this row complements -- that row flags a lane idle without a HANDBACK from the outside; this row blocks the lane's own Stop from completing without one), `[#958]` (the handback organ this hook sits beside) · kill-candidates: none -- no open row gates session end on the machine HANDBACK line's grammar · **CLOSED 2026-09-25** — evidence e1a30321
