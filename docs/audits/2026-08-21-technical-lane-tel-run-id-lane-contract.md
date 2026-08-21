# LANE-TEL — telemetry chain [#565] → [#529] → [#530] (batch 1, lane E)

| Model | Mode | Effort |
|---|---|---|
| opus (default) | execute — no plan mode | high |

**Worktree ⇄ file:** slug `lane-tel-run-id` → branch `worktree-lane-tel-run-id` →
`LANE-TEL-run-id.md`. **Repo:** `.dev-knowledge`. **Purpose:** the felt-performance item
(operator demand: felt speed) — run_id emit + telemetry read page, then the [#529] four legs
and [#530] two races. Dependency-chained ⇒ ONE lane, internal order fixed: #565 → #529 →
#530. Governed by the R6 pre-ruling in [#565]'s body (the seat lands it — READ IT FIRST; if
absent, STOP and report, do not derive your own).

**Done-contract (immutable):**
1. [#565]: run_id emitted per its row; telemetry read page produced (the operator-facing
   "what ran, how long" view its row describes). **COMMIT**
2. [#529]: all four legs per its row, under R6(a) stdlib-first (measured-gap note either
   way) and R6(c) `git rev-parse --show-toplevel` at call time. **COMMIT** per leg.
3. [#530]: both races closed TEST-FIRST — failing test reproducing the race committed before
   the fix; release compares-and-swaps on run_id per R6(d). **COMMIT** per race.
4. WAL store path .gitignore'd — you do NOT edit .gitignore: ship the entry as a fenced
   proposed-diff in the artifact (integrator applies). Same for any pre-commit hook entry.
5. Terra review (`/codex-review`) on the full diff, severity tally INTO
   `ARTIFACT-lane-tel.md` (worktree root), P1/P2 fixed. **COMMIT**
6. pytest green; config in YAML not hardcoded; logging not print; artifact lists: what a
   user of the repo now SEES that they didn't before (release-notes line for A4).
   **COMMIT, then STOP.**

**What NOT to do:** no .gitignore/pre-commit edits (fenced diffs only) · no tasks//BACKLOG/§Q
edits · no docs/intake or docs/audits writes · no merges · no scope growth beyond the three
rows. **Decision budget:** zero questions; unresolvable ambiguity in a row ⇒ execute the
other rows, report the blocked one.
