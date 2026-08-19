# LANE M — [#486] `desired_state_report.py` cp1252 crash fix — contract of record

- **Date:** 2026-08-19
- **Class:** technical (ADR-101 §2 audit grammar)
- **Lane:** micro-lane, local worktree channel — branch `worktree-lane-m-486-cp1252`
- **Mode:** execute — frozen contract, no plan-mode. Commit-and-STOP: no merge, no push to main.
- **Governing row:** `[#486]` — its Done-when governs (U+21C4 ASCII-swapped + a regression
  asserting every console-emitted line of the tool is cp1252-encodable)
- **Scope:** `scripts/desired_state_report.py` + its test file ONLY. `[#470]` (same defect class in
  `audit.py checks`, U+2192) is EXPLICITLY OUT — the `audit-py` serialize-group belongs to lane L2.
- **ADR-110 requirement:** this file IS the frozen dispatch prompt, landed as the FIRST COMMIT of the
  lane, before any other work

## Dispatch prompt, verbatim

```markdown
# LANE M — [#486] `desired_state_report.py` cp1252 CRASH FIX (micro-lane)

| Model | Mode | Effort |
|---|---|---|
| default | execute — frozen contract, NO plan-mode | low |

**Worktree lane, commit-and-STOP.** Governing row: `[#486]` — read it first; its Done-when
governs. The defect: `desired_state_report.py` dies on a cp1252 console (U+21C4 class) — a
Windows-operator-facing tool that crashes on the operator's own console.
**ADR-110:** commit this prompt first as
`docs/audits/2026-08-19-technical-486-cp1252-lane-contract.md`.

Scope: `scripts/desired_state_report.py` + its test file ONLY. (Its sibling `[#470]` — the
same defect class in `audit.py checks` — is EXPLICITLY OUT: `audit-py` serialize-group is lane
L2's; note the shared root cause in your packet so the seat can link the rows.)

STEPS: (0) contract commit → (1) test-first: a test reproducing the crash under a cp1252-like
encoding (monkeypatch stdout encoding — new test file or the tool's existing one; never
tests/test_audit.py) → (2) fix at the OUTPUT layer (encode with replacement or ASCII-safe glyph
map — the repo may already have a precedent for console-safe output: grep for it and REUSE the
pattern if it exists, library-first) → (3) green, run the tool end-to-end capturing exit 0.
FINAL: targeted tests `-n 0`, commit-and-STOP; packet = root cause line, fix pattern used (and
whether a precedent was reused), shas.

NOT: no audit.py touches · no wide refactor · no new files beyond the test · no merge.
```
