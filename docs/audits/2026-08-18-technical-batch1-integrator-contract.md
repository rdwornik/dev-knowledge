# INTEGRATOR — BATCH 1 (2026-08-18): SERIAL MERGE + VERIFY + CLOSE + TEARDOWN

> **Contract of record (ADR-110).** Verbatim operator prompt for the batch-1 integrator seat,
> committed before any merge. The integrator's packet supersedes nothing here — this file is the
> frozen instruction, the packet is the outcome.

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**You run from the PRIMARY checkout on `main`. You are the ONLY writer once you start** (verify:
tree clean, no other active local session). Operator GO on this prompt authorizes the whole
serial queue; return to him only via STOP conditions or the END PACKET.
**Use `/lane-integrate` as the integration mechanism wherever it applies** (anchor + merge +
teardown); if its behavior diverges from this contract on any point, STOP and report — never
improvise around a repo command.
**ADR-110:** save this prompt as
`docs/audits/2026-08-18-technical-batch1-integrator-contract.md`, COMMIT first.

## QUEUE (merge order; each --no-ff; harvest each branch from git, never transcripts)
1. `worktree-lane-d-558-vision` @ 82fb0363
2. `worktree-lane-f-p10-evidence` (356232a, cb48ba2)
3. `worktree-lane-i-31-adoption-preflight` (05af91e4, a1a2ec67)
4. `worktree-lane-g-a9-trim` @ f1239f16
5. `worktree-lane-c-554-devcontainer` — **gated on H's verdict**
6. `worktree-lane-e-502-mutmut` @ c43351de — **gated on H's verdict**
7. `worktree-lane-a-533-leg2` — **gated on your in-arc terra review**
Plus H itself: `worktree-lane-h-554-codex-review` (9a2f6f29, 07628523) merges anywhere after
step 1 — it's docs-only.

## PRE-MERGE DUTIES (in order)
**P1 — branch grammar, BOTH constants ([#514]):** locate every `LANE_BRANCH_RE`-class constant
in the repo (there are two rival ones — [#514]'s finding). Test EVERY queued branch name against
BOTH. Any offender: `git branch -m` to a name passing both, record old→new. Evidence (both
patterns verbatim + per-branch results) goes in your artifact — it feeds [#514].
**P2 — read H's review artifact** (`07628523` → `docs/audits/2026-08-18-review-batch1-c-e.md`).
Honor its verdicts for C and E: MERGE-CLEAN → merge as queued; FIX-BEFORE-MERGE → apply ONLY the
itemized fixes as fixup commits on that lane branch, re-run that lane's targeted tests, then
merge; BLOCK → skip that branch entirely, report in packet.
**P3 — terra review of A** (mandatory pre-merge, A was frozen after H's scope closed): review
A's full diff vs main via `/codex-review` (terra); artifact
`docs/audits/2026-08-18-review-batch1-a.md`, severity tally in body, same three-verdict enum,
honored the same way as P2.

## MERGES
Per merge: targeted sanity on the lane's own surface (each lane's FINAL section named them),
then merge --no-ff with a spine message naming the lane + row ids. After ALL merges: **full
pytest once** (`-n auto`; the 2 OWNED REDs stand — `routine_consumers` and the doc_rot accretion
arm, list them, don't fix; the known reverse_dep_oracle xdist artifact re-runs `-n 0` before
counting as a failure). Any OTHER new RED → STOP.

## SEAT CLOSURE ACTS (post-merge, on main, generator-emitted only — this banks the ledger)
1. `[#556]`: repair #505's BACKLOG drift via `gen_task_tree --emit-source`; close #556.
2. `[#557]`: remove the 3 [stale] dispositions per ADR-75; close #557.
3. `[#558]`: close (lane D landed its Done-when; the two residual sites are the SEAT's follow-up
   candidate, not #558's scope).
4. `[#554]`: read lane C's STOP state — if its Done-when checklist is fully met (incl. the proof
   item or its authorized fork), close; if the proof fork was taken and Done-when literally
   requires the proof, LEAVE OPEN and report which item remains.
5. `[#502]`: transcribe the architect's ruling verbatim — "decision 6 = ADOPT; CI-only (Windows
   walls: POSIX resource, fork); report-only ratchet; baseline 1210 survivors on the
   fleet_analytics slice, direction no-growth; survivor triage deferred with trigger post-#533 /
   next audit-py batch" — into the intake #27 Tier-L adoption ledger + the row; close #502.
6. **A9 route (ii):** disposition "accepted, ruled [#532]/A9" for lane G's 3 REPORT-list rows AND
   for every remaining over-ceiling row in the live-lane excluded set whose length is
   doctrinally legitimate (start with [#533]). Target end-state: **0 undispositioned
   backlog-row-length WARNs**.
7. `[#536]`: read its Done-when; if lane G's execution + the dispositions above satisfy it,
   close; else report the gap.
8. Adjudication register transcription (architect's A13 verdicts): [#514] LIVE priority-up with
   your P1 evidence attached · [#535] add lane-E evidence note · [#457] note = the two OWNED
   suite REDs · [#348] owns the full 194-verdict grooming arc (batch-2 lane) · [#540]+[#539] own
   the dispatch/harvest systematization (next session). Row edits via the generator; NO births.
9. JOURNAL: one entry for the batch, every anchor SHA on ONE line.

## MEASUREMENT (the session's value proof)
- `audit.py ship-gate` before the first merge and after act 6: report the WARN delta by class.
- ONE quiet `audit.py health` timing after A's merge: the new commit-tax vs the 290.9 s baseline
  (A claimed 1.87–4.28x; verify on the merged result and record which measured factor holds).

## TEARDOWN (per merged branch)
`git worktree remove` -> `git worktree prune` -> `git branch -d` -> for E also
`git push origin --delete worktree-lane-e-502-mutmut` -> verify: no leftover worktree dirs, no
stale `.git/worktrees` locks (the 20.07 stale-lock gotcha), `git worktree list` shows primary
only. Push main; both pre-push gates must pass.

## STOP CONDITIONS
Any BLOCK verdict - any non-owned, non-artifact suite RED - a branch name unfixable under both
grammar constants - merge conflict you cannot resolve as a trivial disjoint-file artifact -
[#554] Done-when ambiguity beyond the fork described above.

## END PACKET (one block)
Per lane: merged sha - review verdict - targeted-test result. Then: full-suite result + owned
REDs - closures banked (list + count) vs births (0 this arc) - WARN delta by class - new
commit-tax number - matrix scoring against the 8-item green-list (mutmut pre-banked; #529/#530
explicitly NOT green — batch-2 work) - P1 grammar evidence summary - teardown verification -
every deviation.

## WHAT NOT TO DO
No births - no intake status flips (#35-#39 ratification is a separate seat act after this
packet) - no L2 (#529/#530) work - no fixes beyond FIX-BEFORE-MERGE items and trivial merge
artifacts - no `--no-verify` - no `git add -A` - no skipping teardown.
