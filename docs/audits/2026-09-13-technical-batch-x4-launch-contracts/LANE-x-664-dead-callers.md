# LANE lane-x-664-dead-callers — Remove the two dead call-site clusters safe_remove false-PASSed on -- provision.sh's six call sites of the retired cloud_provisioning.py and the e2e test's importlib load of the retired boundary_report.py -- restoring neither module, and file ONE row for what provisioning's history/ecosystem repair actually needs

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-x-664-dead-callers "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-x-664-dead-callers.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-x-664-dead-callers.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-x-664-dead-callers` — the name that produces `worktree-lane-x-664-dead-callers` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #664 · lane-x-664-dead-callers]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `sonnet` whatever any
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
manual fallback and adds a skip-if-`worktree-lane-x-664-dead-callers`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-x-664-dead-callers` -> branch `worktree-lane-x-664-dead-callers` -> contract `LANE-x-664-dead-callers.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **`.devcontainer/provision.sh`'s six call sites of the retired `scripts/cloud_provisioning.py`
   are REMOVED.** The module is **NOT restored** - git keeps its history (operator, ratification
   item 6: "if there are any dead modules, delete them").
2. **`tests/test_e2e_consumer_lifecycle.py:94`'s importlib load of the retired
   `scripts/boundary_report.py` is REMOVED.** That module is **NOT restored** either. Resolve the
   `:94` locator before acting on it - a line number in a contract is a claim, not evidence.
3. **The end-of-lane artifact states, per cluster, WHAT THE DEAD SITES WERE SUPPOSED TO DO.**
   This is the substantive half of the lane. Both clusters **silently did nothing** - that is
   why `safe_remove` false-PASSed on them, and it means provisioning has been quietly missing
   whatever those six calls were meant to provide, for as long as the module has been retired.
   Read the retired modules out of git history to answer this; do not guess from the call names.
4. **ONE row filed for what provisioning's history/ecosystem repair actually needs** - the real
   gap the six dead calls were standing in for, not a row that says "restore the module".
   `Done when:` in the **literal colon form** (a comma or an em dash reads as MISSING to the
   gate), and the filing commit carries a flush-left `kill-candidates:` line.
5. **RED-first where a test can hold it.** A test asserting `.devcontainer/provision.sh` invokes
   no retired module path - written failing, against the current file, before the removal.
6. Docs and code in English; hyphen-only names; logging rather than print; targeted tests green.

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

1. Resolve both locators and read the retired modules out of git history. Record verbatim what
   each of the six calls and the importlib load was supposed to accomplish. **COMMIT** (the
   record only - no removals yet)
2. RED-first: a test asserting `provision.sh` names no retired module path; watch it FAIL.
   **COMMIT**
3. Remove the six call sites from `.devcontainer/provision.sh`; the test goes green. **COMMIT**
4. Remove the importlib load in `tests/test_e2e_consumer_lifecycle.py`. If the surrounding test
   is left asserting nothing, say so and delete it with the reasoning in the commit body -
   a test that passes vacuously is worse than an absent one. **COMMIT**
5. File the ONE row. **COMMIT**
6. Final: targeted tests green, `git stash list` empty, end-of-lane artifact. **COMMIT, then
   STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## The trap this lane exists to close

`safe_remove.py` returned a false PASS on both of these, and the reason is worth carrying: the
call sites EXIST, so a reverse-dependency oracle sees referrers and reports the module still
used - while the module itself is gone, so the calls do nothing at runtime. **A referrer to a
non-existent module is worse than no referrer**: it satisfies the oracle and delivers nothing.
Removing the sites is therefore not tidying; it restores the oracle's ability to tell the truth
about the next candidate.

**Do NOT restore either module.** That is an explicit operator instruction, and it is the one
V-2 class (b) conflict this lane might otherwise talk itself into: a failing test that "wants"
`boundary_report` back is evidence for item 4's row, not licence to revert a retirement.

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
