# W4d — Done-when conversions, group D (16 rows)

## Dispatch
```
claude --bg --model sonnet --effort medium --worktree lane-k-conversions-w4d --permission-mode bypassPermissions "[dk · w4d · conversions] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\W4D-conversions.md — step 0 commits the contract of record; run the /lane-boot sequence from step 3 onward, commit-and-STOP."
```
**Dispatch only after W3 (lane-c) is merged to `main` and the operator gives the wave GO.**

## Assigned ids (16 — group D of the 2026-08-13 partition print, minus [#508] (CLOSED in ARC2b) and [#513] (W3-carried, in integration))
425, 428, 430, 438, 443, 453, 456, 463, 464, 484, 487, 491, 493, 502, 506, 511

## Repo + Purpose
`.dev-knowledge`. Purpose: convert each assigned row's Done-when from prose to its mechanically-testable form, applying the ready census P1/P2 conversion DRAFTS verbatim-with-adaptation. This is `[W4]` wave-1 work — the biggest under-100/zero-untestable lever. The census drafts are the spec; this lane designs nothing.

## Hard laws pinned in-contract
- **G-6:** any recorded-reason surface is `STANDING_RULINGS` — not relitigated in-lane.
- **L14** (LESSONS.md) applies to this lane — read it at boot and obey.
- **Regenerate, never hand-merge:** `BACKLOG.md` + `tasks/manifest.json` are regenerated via the generator at close; never hand-edited.
- File footprint: `tasks/<id>-*.md` for assigned ids ONLY, + regeneration outputs + own contract/JOURNAL. Nothing else.

## Steps
1. **Step 0 self-serve:** commit this contract (I-D3) + manifest amendment marker; confirm worktree letter free; **verify each assigned id is `status: open` live — a closed/in-flight id is SKIPPED with a one-line note, never converted, never failed on.** → COMMIT
2. Per id: apply its census conversion draft to the row's Done-when; where the draft is missing or stale against the live row, SKIP with note (batched, never dripped). Commit in batches of ~5 rows. → COMMIT ×N
3. Regenerate BACKLOG + manifest; verify `validate_backlog` OK. → COMMIT
4. JOURNAL on the lane branch. → COMMIT

## Lane discipline
V-2 decision budget stated back in one line · commit-and-STOP, never self-merge · questions batched in the packet · no births, no closes, no `CLAUDE.md`/`ARCHITECTURE.md`/`scripts/` edits · ratchet ≤ 441 (Done-when wording is declarative by construction) · expected-REDs: none — any suite change is a defect, report it.

## Review
**Terra: waived — docs/data-only lane, no code impact** (one-line waiver).

## Done-when (frozen)
(1) Every assigned OPEN id's Done-when is mechanically testable per its draft — grep over the assigned set shows zero remaining prose-only Done-when except SKIPPED ids; (2) every SKIP carries its one-line reason; (3) regeneration clean, `validate_backlog` OK; (4) lane packet: shas · converted/skipped counts · decision-budget report.
