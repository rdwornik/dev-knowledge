---
id: "[#1616]"
title: "Start-up context cut 1: `CLAUDE.md` carries only what a session needs before it can act (hooks roster and conventions detail move on demand)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1616] [P1][M] **Start-up context cut 1: `CLAUDE.md` carries only what a session needs before it can act (hooks roster and conventions detail move on demand)** - measured 2026-10-16: a fresh `claude -p` in the repo loads 55,634 tokens against 30,231 in an empty folder; `CLAUDE.md` is 24,100 B (about 6.3 k tokens) plus imports `AGENTS.md` 6,057 B, methodology roster 2,994 B, generated rosters 3,625 B (baseline: the Tokens section of `to-browser/DIGEST-NIGHT-CLOSEOUT-2026-10-15.md`, measured with `claude -p` usage blocks) · Done when: RED first: (1) a test asserts `CLAUDE.md` <= 14,000 B and that section 9's hooks roster is a pointer to the generated organ index; (2) witness: the same `claude -p "Reply with OK." --output-format json --model claude-sonnet-5-5` run in the repo root reports input+cache_creation+cache_read <= 52,000 (baseline 55,634 at a3d0ae31); fails on a3d0ae31 · touches: `CLAUDE.md`, `AGENTS.md`, `tests/test_claude_md_byte_cap.py` · kill-candidates: none -- new row; the dedupe search found no covering row beyond the refs · refs `[#1575]`, R112, `docs/intake/2026-10-16-tech-process-matrix-and-token-baseline.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8/9/10 (AMEND-2, AMEND-3); process matrix empty cell or memory-diag row
