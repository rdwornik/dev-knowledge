# LANE lane-x-664-delete-list-execution — Execute the ratified [#664] DELETE-LIST -- six ordered deletions behind a provisioned safe_remove oracle and a paired baseline/tip suite run, two TRIGGER rows wired RED-first one per commit, cost_usage_telemetry.py's stale disposition text corrected, and worktree_seed.py's ORPHAN_DISPOSITIONS row removed

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-664-delete-list-execution "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-x-664-delete-list-execution.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-x-664-delete-list-execution.md` **from the target repo root** — the ruled verb for a local
lane (PLAYBOOK Ch8's dispatch table, the sole literal-command site). The verb
reads this `## Dispatch` block and runs it **verbatim**, substituting exactly
one literal — `$env:CLAUDE_PROMPTS_DIR` — which is how a frozen contract
names its own location without hard-coding an absolute path. That spelling is
load-bearing: it is the only token the reader replaces, and any other
placeholder is passed through untouched into a real session's prompt.
The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-x-664-delete-list-execution` — the name that produces `worktree-lane-x-664-delete-list-execution` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #664 · lane-x-664-delete-list-execution]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `opus` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The verb refuses any other program — *"this script never runs an
arbitrary command from a contract file"* — so a contract's `## Dispatch` block
is not a place to name a helper. Until 2026-09-12 this generator emitted the
deprecated `Dispatch-Lane` alias here and **every contract it produced was
refused by the verb meant to launch it**. That alias still resolves as the
manual fallback and adds a skip-if-`worktree-lane-x-664-delete-list-execution`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-x-664-delete-list-execution` -> branch `worktree-lane-x-664-delete-list-execution` -> contract `LANE-x-664-delete-list-execution.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **The oracle is PROVISIONED and RUN BEFORE ANY DELETION.** `npm install` provisions
   `safe_remove.py`'s vendored pyright - the census returned `oracle-unavailable` for all nine
   candidates it tried, so this is the lane's own precondition, not an inherited state. Run
   `safe_remove.py` over all six DELETE candidates and record every verdict verbatim, including
   a second `oracle-unavailable` if it recurs.
2. **A SAFE verdict is necessary and NOT sufficient, and this lane is required to act as if it
   knows that.** ADR-89 declares the oracle static-only, and `scripts/desired_state_loader.py` is
   this repo's own witness: deleted on a SAFE verdict, the suite went RED, and it was restored
   whole. The paired suite run in item 3 is what carries the weight the oracle cannot.
3. **A paired baseline/tip suite run on GitHub Actions.** Baseline at this lane's base commit,
   tip after the last deletion - same workflow, same runner class, adjacent in time. Both run ids
   and both failure sets recorded. A failure present in BOTH readings is not this lane's; a
   failure present only at tip is, and it blocks.
4. **The six deletions, IN THE RATIFIED ORDER.** `scripts/gen_trend_dashboard.py` then
   `scripts/gen_north_star.py`; `scripts/window_metrics.py` then `scripts/failed_set.py`;
   `scripts/nopack_sandbox.py`; `scripts/trace_writer.py`. The two orderings are load-bearing and
   are not stylistic: `failed_set` is reachable only from `window_metrics:359`, and
   `gen_north_star`'s only code referrer is an `imports` edge from `gen_trend_dashboard`.
   Deleting either dependant first turns a clean removal into a broken import.
5. **The two TRIGGER rows wired RED-first, ONE ROW PER COMMIT.** `scripts/archive_row_body.py`
   onto the **pre-commit stage**, beside the row-lifecycle gates. `scripts/logs_retention.py`
   onto the **`SessionStart`/`Stop` path** that writes the logs it would retain. Each is: a
   failing test proving the trigger absent, then the wiring, then green. A test that proves a
   module works while scheduling nothing is not a trigger - that distinction is the whole reason
   `archive_row_body` is on this list.
6. **`scripts/cost_usage_telemetry.py`'s stale `ORPHAN_DISPOSITIONS` disposition text corrected.**
   The text reads as a DELETE; the ratified disposition is KEEP. `[#694]` records it PARTIALLY
   DISCHARGED - no longer inventory, with a real call site in `provider_router.py` that FPG-1
   confirms. It is untriggered only because its caller is, and it moves with that caller.
7. **`scripts/worktree_seed.py`'s `ORPHAN_DISPOSITIONS` entry DELETED - the MODULE STAYS.** It is
   reachable over `TRIGGER_KINDS`: `.pre-commit-config.yaml` fires `gen_lane_contract.py` (the
   `lane-contract-check` hook) and that module imports `worktree_seed`.
   `tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
   goes GREEN. **Two prior lanes declined this one-line edit as a V-2 class (a) curated-baseline
   touch. The operator has now ruled it (ratification item 5), so it is NO LONGER an escalation -
   make the edit.** Ignore the `.claude/settings.json` mention: that path sits inside a
   `"//worktree"` COMMENT key and the edge is spurious; the import edge is the real one.
8. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; targeted tests green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. `npm install` to provision the oracle. Run `safe_remove.py` over all six candidates and
   record every verdict - no deletion in this commit. **COMMIT**
2. Fire the Actions **baseline** run at this lane's base commit; record the run id and its
   failure set. **COMMIT**
3. Delete `scripts/gen_trend_dashboard.py`, then `scripts/gen_north_star.py` - in that order,
   and clear their `ORPHAN_DISPOSITIONS` rows with them. **COMMIT**
4. Delete `scripts/window_metrics.py`, then `scripts/failed_set.py` - in that order. **COMMIT**
5. Delete `scripts/nopack_sandbox.py` and `scripts/trace_writer.py` (inbound: none, of any
   kind). **COMMIT**
6. Fire the Actions **tip** run; record it beside the baseline and diff the two failure sets.
   **COMMIT**
7. `archive_row_body.py`: RED-first test, then the pre-commit wiring, then green. **COMMIT**
8. `logs_retention.py`: RED-first test, then the `SessionStart`/`Stop` wiring, then green.
   **COMMIT**
9. `cost_usage_telemetry.py`'s disposition text corrected; `worktree_seed.py`'s register row
   deleted. **COMMIT**
10. Final: targeted tests green, `git stash list` empty, end-of-lane artifact carrying the
    oracle verdicts, both Actions readings, and every V-2 decision taken rather than asked.
    **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Model - CORRECTED AT FREEZE, and the operator may reverse it

**The operator ordered `opusplan` for this lane. It is frozen and dispatched at `opus`.**

`opusplan` is a SPLIT tier that routes Opus to **plan mode**. Every dispatch constant puts a lane
on `--permission-mode bypassPermissions`, which never enters plan mode; with no plan phase there
is no Opus phase, and the tier collapses to its implement half - Sonnet. Nothing warns: the flag
is accepted, and the resolved line reads `--model opusplan` while the session runs Sonnet.

**Re-measured at THIS freeze on the installed CLI (2.1.270), not inherited.**
`claude --print --model opusplan --permission-mode bypassPermissions` produced a session
transcript whose every assistant message records `claude-sonnet-5`. The prior reading -
`docs/audits/2026-09-13-technical-batch-x3-manifest.md` section 6 finding 7, measured on 2.1.224
across 84 assistant messages of a real lane - therefore still holds on the current CLI.

Firing at `opusplan` would deliver Sonnet, a tier the operator did not name either, so there is
no faithful-literal option and **both** choices deviate. `opus` is the one matching intent: the
operator's own gloss for the tier is "Opus plans", and Ch8's routing matrix routes **gate and
organ code** - exactly this lane - to `opus`. This paragraph is the disclosure, not an
authorisation: deviation-with-disclosure does not authorise itself, the operator may reverse it,
and re-firing at another tier is one command.

## Expect these gates to fire - they are consequences of the diff, not defects

Deleting six modules moves several counted surfaces at once. Budget for it rather than
discovering it at commit 3:

- **`graph-orphan-census` / `graph-task-coverage` / `graph-process-list`** all read the persisted
  FPG-1 store, and this diff changes the process population by six. Regenerate what the hook
  names; do not hand-edit a generated surface.
- **`doc-counts-pytest-freshness`** moves if the test count moves. Adding the RED-first tests in
  steps 7-8 will move it.
- **`impacted-tests-guard`** refuses a changed `scripts/*.py` no test covers - relevant to the
  two TRIGGER wirings, and it names the RED-first test it wants.
- **Rows naming a deleted module** (`[#589]` `[#615]` `[#694]` `[#470]` `[#611]` `[#689]`
  `[#383]` `[#624]`) hold `implements` edges to files that will no longer exist. **Do not close
  or rewrite another lane's row to make a gate green.** Where a row is left naming a deleted
  file, say so in the end-of-lane artifact and leave it for the operator - `[#694]` is the
  declared owner of the telemetry decision and `[#664]` of the census.
- **`archive_row_body`'s trigger is already ORDERED by `[#664]`** in its own words - it wants
  execution, not a decision. `logs_retention`'s owner is `[#655]`, whose entire title is
  "`run_retention()` has no production caller".

## Batch context - X wave 4 (appended at freeze, part of the frozen contract)

**The GO.** `to-browser/RATIFICATION-2026-09-13.md`, the operator's words of 2026-09-13,
recorded the same turn. That file is this lane's authority and the scope bound: the GO covers
these four lanes and no lane outside them fires on it.

**Concurrency 4, no backfill.** All four lanes of this wave fire together. **No lane may wait on
the operator mid-run (AX27-1)** - a lane that would need him is mis-scoped, not brave. Everything
outside V-2 classes (a)/(b)/(c) is decided per contract defaults and REPORTED in the end packet.

**Hazards measured in wave 3 and carried here so they are not rediscovered at cost**
(`docs/audits/2026-09-13-technical-batch-x3-manifest.md` section 6):

- **`graph-rebuild` is NOT concurrency-safe, and this batch runs four concurrent lanes by
  design.** A commit can fail inside `graph_store.py::_swap_into_place` when a sibling lane
  commits at the same moment; the same rebuild run standalone a minute later succeeds. **Retry
  the commit. Do not "repair" the store, and do not read the traceback as a defect in your own
  diff** - its worst property is that it surfaces in an unrelated lane's commit.
- **`uv run --locked` on EVERY test invocation.** A bare `pytest` inside a worktree inherits
  `VIRTUAL_ENV` from the primary tree, imports the PRIMARY checkout's source, and reports green
  about code this lane did not touch - silently (STANDING_RULINGS D4; ADR-106 for the pin).
- **`git stash list` EMPTY at STOP.** `refs/stash` lives in the COMMON git directory, not the
  worktree's private ref space: a stash pushed here survives `git worktree remove`, the branch
  delete and every teardown step, and is findable only by someone who thinks to look.
- **Targeted tests only.** The full suite runs ONCE, at integration (`[#528]`). Run the tests
  covering this lane's diff - `uv run --locked python scripts/impacted_tests.py select --changed <paths>`
  names them.
- **A gate that blocks leaves files STAGED.** Fix the cause and re-commit; do not reach for
  `--no-verify`. Where a bypass is genuinely sanctioned it is ONE named hook, declared in the
  commit body.
