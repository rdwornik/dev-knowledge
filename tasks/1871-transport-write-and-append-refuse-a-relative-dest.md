---
id: "[#1871]"
title: "transport write and append refuse a relative dest"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1871] [P2][S] **transport write and append refuse a relative dest** - audit A2 of 2026-11-04: a transport-path write landed inside a repo checkout (`to-browser/archive/2026-11/QUESTION-toy-1ba5eb09.md` untracked in the orchestrator-e3-0-cycle-4 worktree), because a relative `dest` given to `transport.write` / `transport.append` (`scripts/transport.py:306`, `scripts/transport.py:403`) resolves against the caller's cwd. Fix: both refuse a non-absolute dest, naming CLAUDE_PROMPTS_DIR; tests for both. Same content as the E3.1 grant NEW-v (`[#1829]`, reserved, never filed: no tasks/1829 file exists), filed now under a fresh id. · touches: scripts/transport.py, tests/test_transport.py · kill-candidates: none - [#1829] is a reservation with no row · refs ADR-140 (out-of-scope item A2), `scripts/transport.py` · Done when: a relative dest is refused by write and append, and no write from any cwd lands in a checkout (tests) · decided-by: night order N2(b) · source: P0 audit A2
