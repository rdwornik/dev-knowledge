# W1 — lane-a-514-lane-regex: one lane grammar, one constant, scoped exemption (+ the I-D8 drive-by)

## Dispatch
```
claude --worktree lane-a-514-lane-regex --bg --model opus --effort high --permission-mode bypassPermissions "[dk · #514 · lane-regex-unification] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\W1-LANE-514-LANE-REGEX.md — its step 0 commits the contract of record; run the /lane-boot sequence from step 3 (seed) onward, commit-and-STOP."
```
Operator runs `dispatch W1-LANE-514-LANE-REGEX.md` — the helper executes the line above verbatim (PLAYBOOK Ch8, [#509] v2). Steps 1–2 of /lane-boot (name validation + provisioning) are discharged by this dispatch itself; the lane starts at step 3.

| Model | Mode | Effort |
|---|---|---|
| opus | execute — this contract IS the plan | high |

## Purpose · rows · bucket
`[#514]` (P1, merge-queue wedge): two rival `LANE_BRANCH_RE` constants — strict (`validate_branch_naming.py:85`, `\d+`) vs loose (`scripts/batch_manifest.py:91`) — disagree; the ADR-110 exemption keys on the loose one. `[#510]`: scope the R1 exemption to enumerated lanes — same `exempt()` function, ONE lane by ruling. Plus the **I-D8 drive-by**: `CLAUDE.md` §6 item 3 + byte-identical carrier `templates/claude-regions/session-start-protocol.md:4` still read "Read most recent handoff". G-4 discharges here. Bucket: hub-introspection (the batch's cap slot).

## Read first
PLAYBOOK Ch8 "The batch protocol" (your governing doctrine) · `tasks/514-*.md` + `tasks/510-*.md` Done-when verbatim · both regex sites · ADR-110 + its 2026-08-07 amendment (what the exemption grants and how the manifest keys it) · `STANDING_RULINGS` I-D8/I-D10 · the ARC-7 §1 fix pattern.

## UNDERSTAND (state before step 1)
Problem: two sources of truth for one grammar; the exemption rides the wrong one. Scope: unify to ONE importable strict constant, scope `exempt()` to it, fix the two "most recent" sites. Risk: LOOSENING instead of tightening silently blesses id-less names (the G-2 defect) — anything that stops matching is a finding, not a reason to widen. Forbidden: `CLAUDE.md` edits beyond §6 item 3 + version header.

## Lane requirements (PLAYBOOK Ch8, verbatim obligations)
Frozen contract (this file, from the tree) · V-2 budget stated back in one line before work · **`uv run --locked` on every test invocation** (a bare pytest reports green about the primary's source) · run `worktree_import_probe` once as proof · commit per step on the lane branch · **JOURNAL entry written ON THIS BRANCH ahead of the merge** (JOURNAL-rides-the-branch; sequential batch → allocate the next day-letter yourself and say so) · commit-and-STOP with `git stash list` empty.

## Steps
0. **Contract of record (I-D3, self-serve):** copy THIS file byte-identical from the prompts dir to the in-repo home beside the batch-4 manifest (the manifest's W1 row names the path; ADR-101 enum name) and make it the FIRST commit on this lane branch; update the manifest W1 row from PENDING-CONTRACT to the committed path in the same commit. **COMMIT**
1. **Unify the constant** — one strict `LANE_BRANCH_RE` defined once, imported everywhere; delete the rival. **COMMIT**
2. **Scope the exemption** — `exempt()`/`is_lane_merge` key on the single constant; R1 exemption applies only to enumerated-grammar branches per `[#510]`. **COMMIT**
3. **Tests, mechanical:** (a) exactly ONE definition exists (asserted); (b) accepts `worktree-lane-a-514-lane-regex`-shaped names, rejects id-less and legacy `worktree-<slug>` shapes; (c) `is_lane_merge` seeded both sides; (d) a seeded non-lane branch gets NO exemption. **COMMIT**
4. **I-D8 drive-by** — both "most recent" sites → the active-bundle-predicate citation, byte-identical; bump `CLAUDE.md` version header with a §12-style note citing I-D8. **COMMIT**
5. **Rows:** close `[#514]` and `[#510]` per their Done-when, closing commit named (G-5 pattern); G-4 discharge line drafted for the integrator. **COMMIT**
6. **JOURNAL on the branch**, then **final:** `uv run --locked pytest -q` (expect ONLY the standing `[#426]` RED; the linked-worktree RED is your context — prove it) · packet per Ch8: branch, commits, suite verdict, every budget decision · request terra review (code-impact lane — MANDATORY pre-merge). Commit-and-STOP.

## Decision budget (V-2)
Escalate only: (a) curated-baseline touches beyond §6+header · (b) rule-vs-ruling conflicts (e.g. something LIVE depends on the loose grammar) · (c) unruled forks. Everything else: decide per contract, report in the packet.

## What NOT to do
No grammar loosening · no branch renames · no edits outside named files+tests+rows · no births · no self-merge · no `SKIP=`/`--no-verify`.

Library-first: n/a — consolidating existing constants.
