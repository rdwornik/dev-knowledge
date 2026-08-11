# W2 — lane-b-270-fleet-audit: execute [#270] (feature bucket; G-5 closing-commit metric)

## Dispatch
```
claude --worktree lane-b-270-fleet-audit --bg --model opus --effort high --permission-mode bypassPermissions "[dk · #270 · fleet-audit] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\W2-LANE-270-FLEET-AUDIT.md — its step 0 commits the contract of record; run the /lane-boot sequence from step 3 (seed) onward, commit-and-STOP."
```
Operator runs `dispatch W2-LANE-270-FLEET-AUDIT.md`. Authority: batch-4 GO `3b711e87`; parallel-with-W1 authorized by the operator's 2026-08-11 re-ruling (matrix-proven disjoint; record the re-rule per the note below).

| Model | Mode | Effort |
|---|---|---|
| opus | execute — this contract IS the plan | high |

## Purpose · row · bucket
`[#270]` — P1, idle 34+ days, unblocks three dependent rows; the batch's first FEATURE-bucket lane (quota three-way split). **The ROW IS THE SPEC:** this contract frames execution; the work scope comes verbatim from `tasks/270-*.md` plus its evidence sheet in the batch4-prep report (`docs/audits/`, merged at `7d1d332c`). Do not re-derive scope from this contract's title.

## Read first
`tasks/270-*.md` — frontmatter + Done-when verbatim · the `[#270]` evidence sheet + footprint entry in the batch4-prep report · PLAYBOOK Ch8 (your governing doctrine) · `STANDING_RULINGS` I-D (G-5: `[#270]` adopts the closing-commit metric — the row closes naming the commit that satisfies it) · the batch-4 manifest (your W2 row).

## UNDERSTAND (state back before step 1, quoting sources)
One paragraph in your packet preamble: the row's Done-when quoted · the three dependent rows it unblocks (ids from the evidence sheet) · your planned footprint vs the sheet's predicted footprint — name any file OUTSIDE the predicted footprint before touching it (that is a budget item, not a liberty). Satellites are LOCAL-only territory: if the row's work requires reading a satellite repo, do it read-only from this machine and record which; never mutate a satellite from this lane.

## Lane requirements (PLAYBOOK Ch8, verbatim obligations)
Frozen contract from the tree · V-2 budget stated back in one line before work · `uv run --locked` on every test invocation · `worktree_import_probe` once as proof · commit per step on the lane branch · JOURNAL entry ON THIS BRANCH ahead of the merge (allocate the next free day-letter, say so — W1 may allocate concurrently; if your letter races W1's, note it for the integrator instead of guessing) · commit-and-STOP with `git stash list` empty.

## Steps
0. **Contract of record (I-D3):** copy THIS file byte-identical from the prompts dir to the home beside the batch-4 manifest (the manifest's W2 row names the path) as the FIRST commit on this branch; flip the manifest W2 row from PENDING-CONTRACT to the committed path in the same commit. Include one register-echo line in the commit body: "operator re-ruling 2026-08-11: batch-4 sequential-by-default, pairwise-parallel where the disjointness matrix proves it and the operator approves the pair (W1∥W2 approved)." **COMMIT**
1. **Scope statement** per UNDERSTAND above (packet preamble, no commit).
2..n. **Execute `[#270]` per its own Done-when**, one commit per coherent step, tests-first where the row's clauses are mechanical. Any clause that proves unmeetable as written: STOP on that clause, record why with evidence, continue meetable clauses — never reinterpret silently (budget item c).
n+1. **Close the row** — `status: closed` with the G-5 closing-commit metric (the commit SHA that satisfies the Done-when, named in the row). Draft the three dependents' unblock note for the integrator (do NOT edit the dependent rows). **COMMIT**
n+2. **JOURNAL on the branch**, then **final:** `uv run --locked pytest -q` — expect only the known pre-existing REDs (`[#457]`-documented routine-consumers · sed-absent ×2 · linked-worktree context); anything NEW is yours until proven otherwise by revert-and-rerun, the proof standard. Packet per Ch8 + terra review request if ANY code/script/hook was touched (code-impact ⇒ review mandatory; docs-only ⇒ state so and the reviewer lane is waived with that one line). Commit-and-STOP.

## Decision budget (V-2)
Escalate only: (a) curated-baseline touches · (b) rule-vs-ruling conflicts · (c) an unmeetable or ambiguous Done-when clause · (d) any file outside the evidence sheet's predicted footprint. Else decide per contract, report in the packet.

## What NOT to do
No satellite mutations · no edits to the three dependent rows · no births · no self-merge · no scope beyond the row's Done-when · no `SKIP=`/`--no-verify`.

Library-first: governed by the row's own clauses; if the row calls for building machinery, run the stdlib→dependency→pattern search and record it in the packet before writing any.
