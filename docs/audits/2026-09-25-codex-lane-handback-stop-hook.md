# Codex Review — lane-handback-stop-hook

**Date:** 2026-09-25
**Branch:** `worktree-lane-handback-stop-hook`
**HEAD:** `e1a30321`
**Diff range:** `1c9fbf4d..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/2/0/0 <!-- Critical/High/Medium/Low. Every finding below was fixed; see Disposition. -->

**Disposition:** all 3 findings fixed. CRITICAL (persistent block re-creates the ADR-85 cap): `main()` now gates every block on `stop_hook_active == False` (a fresh stop attempt), reading it from the Stop-hook's own stdin JSON (`_read_stop_hook_active`, matching `session_end_backpressure.py`'s established contract) with a structural floor that stays silent when the field can't be read at all — fire-once, not scope alone, the same mechanism that hook already uses for its advisories. HIGH ("last candidate wins" not implemented): `classify()` rewritten to track exactly one running verdict overwritten by every candidate found, in document order, instead of letting any earlier clean match win outright. HIGH (multiline inline-code handbacks accepted as clean): code-span detection is no longer a per-line backtick substring check; it walks the real `markdown_it` inline token stream (`_prose_and_code_chunks`), so a `code_inline` span that itself crosses a physical line break (CommonMark converts its internal newline to a space) is still caught as code, never as a bare unwrapped line. All three fixes are covered by new tests in `tests/test_lane_handback_gate.py` (fire-once: retry/unknown/fresh-again; last-candidate-wins downgrade case; the crossing-line-break code span).

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- correctness of classify() in scripts/lane_handback_gate.py: the fence/backtick/malformed detection logic and the last-candidate-wins closing-line semantics
- whether the {"decision":"block","reason":...} Stop-hook JSON contract is used correctly and consistently with session_end_backpressure.py's own documented contract
- whether scoping the block to lane sessions only (resolve_lane) genuinely avoids the ADR-85 block-cap exhaustion failure mode that retired session_end_backpressure.py's own hard leg
- fail-soft correctness: does any path let an exception escape main() and produce a non-zero exit or a raw traceback that a Stop hook would misread
- test coverage and whether the tests actually exercise the real subprocess entry point, not just the pure functions

---

## Findings
## CRITICAL

### [CRITICAL] scripts/lane_handback_gate.py:187 — Missing handback blocks every lane Stop, recreating ADR-85 cap exhaustion

**What:** Any lane Stop without a handback emits a persistent `decision:block`; `resolve_lane()` only identifies lane sessions, not an actual completion attempt.  
**Why:** Lane sessions can stop repeatedly while working, so this reaches the host’s consecutive-block cap and is silently auto-bypassed—the exact failure mode the new scope claims to avoid.  
**Fix direction:** Enforce at a non-exhaustible completion boundary, or add a reliable completion-attempt signal rather than treating every lane Stop without a line as a handback failure.

## HIGH

### [HIGH] scripts/lane_handback_gate.py:131 — “Last candidate wins” is not implemented

**What:** `classify()` returns `ok` whenever any earlier clean candidate exists, even if a later candidate is malformed or backtick-wrapped; the test at `tests/test_lane_handback_gate.py:114` locks in this opposite behavior.  
**Why:** A stale valid line can mask the actual closing line, allowing an invalid final handback through.  
**Fix direction:** Track the classification of each candidate in scan order and return the final candidate’s status and line.

### [HIGH] scripts/lane_handback_gate.py:124 — Multiline inline-code handbacks are accepted as clean

**What:** Inline-code detection only checks for a backtick on the candidate’s own line; CommonMark inline code spans may cross lines, leaving the `HANDBACK` line itself backtick-free.  
**Why:** A handback inside a multiline inline code span can be accepted and trigger the lane-end flow despite being non-machine-readable prose.  
**Fix direction:** Use parsed inline-token/source-span information, or otherwise detect code-span ranges across source lines; add a subprocess-backed regression case.

## MEDIUM

(none)

## LOW

(none)