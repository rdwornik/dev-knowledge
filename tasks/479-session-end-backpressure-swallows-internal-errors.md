---
id: "[#479]"
title: "`session_end_backpressure` swallows internal errors — a broad `except: return 0` lets a crash masquerade as a pass"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#479] [P2][S] **`session_end_backpressure` swallows internal errors — a broad `except: return 0` lets a crash masquerade as a pass** — the ADR-85 session-end gate is an ENFORCEMENT organ, and an enforcement organ that cannot distinguish “nothing to report” from “I failed to look” is advisory in the one case that matters. The [#475] precedent is the ruled-correct shape: `check_seal_identity` exits 2 on internal error, so an error BLOCKS and never silently passes. VERIFIED NOT currently masking anything (2026-08-03 night batch) — this row is about the SHAPE, not a live incident, and must not be written up as one. · Done when: an internal error in the gate exits non-zero and names itself, with a test injecting a failure and asserting the session is BLOCKED rather than released · refs scripts/session_end_backpressure.py, ADR-85, #475, scripts/check_seal_identity.py · kill-candidates: none — [#475] shipped the fail-loud shape for the seal gate, not for this one
