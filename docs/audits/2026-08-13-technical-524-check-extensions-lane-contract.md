# CODEX-524 v2 — Four ruled check extensions (Codex PRODUCER, CC verifier) · wave-1 roster

## Dispatch
```
claude --bg --model sonnet --effort medium --worktree lane-l-524-check-extensions --permission-mode bypassPermissions "[dk · #524 · check-extensions] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\CODEX-524-v2.md — step 0 commits the contract of record; run the /lane-boot sequence from step 3 onward, commit-and-STOP."
```
**Dispatch only after W3 (lane-c) is merged to `main`** (ARC2b step-7 OVERLAP verdict) **and with the W4 wave GO** — roster arithmetic: width 5 (4 conversion lanes + this), hub-introspection occupants 1, permitted 1 → **within the G-8 cap**.

## Repo + Purpose
`.dev-knowledge`. Purpose: implement `[#524]`'s four Done-when clauses — E4-02 (JOURNAL whole-file day-letter check), E4-03 (`validate_backlog` body-date scan), L5 (`journal_anchor` anchored-by-mention WARN), L12 (`check_hooks_armed` pre-push hook-type assert) — **Codex as PRODUCER, CC as verifier**. This is the ruled §B clause-6 discharge (E1-6): a real bounded build with a provenance line, not ceremony.

## Boot check — the repin guard (v2 addition, mandatory before any edit)
W3's merge moved the check registry: **read the live `len(ALL_CHECKS)` and verify all 6 count-pin sites read that same number** (expected 42 post-W3). If any pin disagrees with live, STOP and batch — that is the recorded silent-merge hazard (each lane alone goes green; merged pins drift without a git conflict). After this lane's own addition, re-pin all 6 sites to the new count (expected 43) **in the same commit** as the registry change.

## Division of labor
- **Codex (`codex exec`, model terra) produces:** the four implementations + tests, against `[#524]`'s clauses quoted verbatim in the delegation prompt. Bounded; no design latitude beyond the row.
- **CC verifies:** full suite `uv run --locked`; line-by-line diff review against the four clauses; WARN-vs-RED semantics per clause (L5, E4-03 = WARN; E4-02 REDs `audit.py health` on the seeded defect); no scope creep beyond `scripts/audit.py`, `scripts/validate_backlog.py`, `scripts/journal_anchor.py` + tests + the 6 pin sites. Defective production goes BACK to `codex exec` with the finding — CC fixes nothing silently.

## Review — role independence
Terra produced → terra cannot review. **Reviewer = sol, pre-merge, mandatory; artifact persisted ON DISK with the severity tally in-body — the packet names the artifact path.** Judgment stated: role independence outranks the default terra-reviews routing when terra is the producer.

## Lane discipline
Step 0 self-serve (contract commit, I-D3; letter check) · V-2 budget stated back · JOURNAL on the lane branch · commit-and-STOP, never self-merge · questions batched · no births · no edits outside the named file set · seeded-defect tests clean up after themselves · expected-REDs as a class with revert-proof duty.

## Done-when (frozen)
(1) All four `[#524]` clauses pass with named tests (≥ 6 new); (2) pins: 6/6 sites read the live post-change count, verified by grep in the packet; (3) full suite green except the standing owned RED class; (4) sol artifact on disk, path named, tally in-body; (5) provenance line: Codex-produced diffs vs CC-touched lines (the §B clause-6 evidence); (6) packet: shas · test counts · budget report.
