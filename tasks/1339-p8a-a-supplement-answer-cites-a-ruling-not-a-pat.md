---
id: "[#1339]"
title: "P8a: a SUPPLEMENT answer cites a ruling, not a path"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1339] [P3][S] **P8a: a SUPPLEMENT answer cites a ruling, not a path** - `protocols/HANDOFF_PROCESS.md` (P8's two legs) has leg P8a fail a bundle unless "each filled answer cites a FILE, a repo path or a transport path, not a chat turn". An answer that rests on a standing ruling (R41, R47.1) has a stable id in the register and no single file location, so the probe pushes the author to cite a path that merely contains the ruling. The citation that is both stable and checkable is the ruling id against `protocols/STANDING_RULINGS.md` · Done when: P8a accepts a register ruling id (`R<n>`) as a citation form and still refuses a chat-only citation; a RED-first test in `tests/test_gen_handoff.py` fails on a ruling-cited answer today and passes after, and the register lookup is resolved, not pattern-matched · touches: `scripts/verify_handoff_probes.py`, `protocols/HANDOFF_PROCESS.md`, `tests/test_gen_handoff.py` · kill-candidates: none -- no open row tracks the P8a citation form · refs `protocols/HANDOFF_PROCESS.md`, `scripts/verify_handoff_probes.py`, `tests/test_gen_handoff.py`, `protocols/STANDING_RULINGS.md` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
