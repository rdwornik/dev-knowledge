# MICRO-LANE — THE RULED --parallel FLIP (audit hook)

| Model | Mode | Effort |
|---|---|---|
| default | execute — frozen contract, NO plan-mode | low |

**Worktree lane, commit-and-STOP.** ADR-110: commit this prompt first as
`docs/audits/2026-08-20-technical-parallel-flip-lane-contract.md`.

RULING (architect, 2026-08-20, from the §2.6 bar report — items 1–4 PASS): the flip is APPROVED.
This lane executes bar item 5 exactly.

THE CHANGE — one line, `.pre-commit-config.yaml:172` (verify the line number on your tree):
`uv run --locked python scripts/audit.py health` → `uv run --locked python scripts/audit.py health --parallel`

COMMIT BODY MUST RECORD (bar item 5's contract, values from the bar report):
- measured quiet median: 96.536 s (5 runs, spread 1.77%, main @ 1def12f6)
- parity digest: 758a3203a61e928f0ac381e0350d4cf1 (78 findings); full-stdout md5 e0c23b6af1abd910324eed712f0681a2
- revert line: the exact one-line diff above, reversed.

VERIFY: run the hook entry once post-change (expect ~97 s, health: OK), targeted tests
`tests/test_audit_parallel* tests/test_journal_anchor.py -n 0`. Commit-and-STOP.
NOT: no other config edits, no timing re-measurement campaign, no doc updates (the codification
lane owns those).
