# LANE lane-x-675-instrument-fixes — Close the three verified [#675] false-pass holes RED-first -- actions_verdict returning PASS on unreadable job details, the step-0 collision extractor blind to root-level tracked files, and median_report counting incomplete receipts -- against rows [#742] [#743] [#744] which the integrator seat filed at batch-X3 close, WITHOUT re-filing them

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-675-instrument-fixes "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-x-675-instrument-fixes.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-x-675-instrument-fixes.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-x-675-instrument-fixes` — the name that produces `worktree-lane-x-675-instrument-fixes` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #675 · lane-x-675-instrument-fixes]`.
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
manual fallback and adds a skip-if-`worktree-lane-x-675-instrument-fixes`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-x-675-instrument-fixes` -> branch `worktree-lane-x-675-instrument-fixes` -> contract `LANE-x-675-instrument-fixes.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **THE THREE ROWS ARE ALREADY FILED. DO NOT FILE THEM AGAIN.** While this batch was being
   frozen, the **integrator seat** (session `91f1a9e3`, working in the primary checkout on branch
   `docs/batch-x3-close-packet`) filed the operator's ratification item 3 as three rows:
   `[#742]`, `[#743]`, `[#744]`. They are the reason this contract is a re-cut - the first cut of
   this lane told it to file them, which would have produced two rows per hole under the same
   three ids. **This lane implements against those ids and creates no `tasks/` row for any of the
   three holes.** Their Done-whens are carried verbatim below so this lane is not blocked on
   seeing files that live on a branch it cannot reach.
2. **`[#742]` - `actions_verdict` reports PASS when the job details cannot be read.**
   Carried verbatim: *"an unreadable, timed-out, errored or non-zero-exit `gh run view --json
   jobs` no longer yields `STATE_PASS` - it surfaces as an explicit unavailable/unknown state
   distinct from both PASS and FAIL, propagated to every caller that renders a verdict; and one
   test FAILS before the fix and passes after - a RED-first witness per ADR-108 SB that stubs the
   job-details call into each failure mode (non-zero exit, `OSError`, `subprocess.TimeoutExpired`,
   malformed JSON) and asserts the verdict is NOT `STATE_PASS`, still RED if the empty-list
   degradation is later reintroduced; and the distinction between 'no failing jobs' and 'no
   readable jobs' is asserted by a test that passes a genuinely job-less run and gets a different
   answer than an unreadable one."*
   The row's own code read: `scripts/actions_verdict.py:205-213` assigns `match["jobs"] = []` on
   ANY failure of the second `gh` call, and `verdict_for` then computes `failing = set()` over the
   empty list and returns `STATE_PASS`. **The module already knows how to say "I could not read
   this"** - the FIRST `gh` call at `196-200` raises `ActionsUnavailable` on both a non-zero exit
   and unreadable JSON. The second call simply does not use it.
3. **`[#743]` - the step-0 collision extractor requires a slash, so two lanes may both declare a
   root-level file and pass.** Carried verbatim: *"a Done-contract declaring a root-level tracked
   file (`ARCHITECTURE.md`, `.pre-commit-config.yaml`, `pyproject.toml` and the rest) is extracted
   by the collision checker and two lanes declaring the same one are REFUSED at step 0; one test
   FAILS before the fix - a RED-first witness per ADR-108 SB feeding two contracts that both
   declare a root-level file and asserting a refusal, still RED if the slash requirement is
   reintroduced; `_WRITE_ROOTS` admits the root without admitting the transport paths, absolute
   operator paths and prose nouns its comment exists to exclude (a bare `*.md` admission that lets
   `LANE-x-000-other.md` through is a regression, not a fix, and a test asserts that too); and
   `file_purpose_graph._REL_PATH_RE` is checked for the same blindness in the same pass - if it
   shares it, that is recorded here and either fixed with it or split with a stated reason."*
   **This hole is live in THIS batch and that is not hypothetical.** The `file-collision` refusal
   this seat ran at step 0 reported 23 declared paths and no collision - while lane
   `lane-x-628-docs-cut` declares `ARCHITECTURE.md` and `lane-x-664-delete-list-execution`
   declares `.pre-commit-config.yaml`, both root-level, both invisible to the extractor. The two
   happen not to collide with each other, so the PASS is correct by luck rather than by check.
4. **`[#744]` - `median_report` filters receipts by kind but never by completeness.** Carried
   verbatim: *"a receipt that is not complete is EXCLUDED from the median - with 'complete' given
   one explicit predicate in code (at minimum `closed is not None` plus every declared step
   present and non-failed) rather than left to the reader; the exclusion is REPORTED alongside the
   median the same way `excluded` already reports the kind filter, so a median over a thinned
   sample never renders as a median over a full one; one test FAILS before the fix - a RED-first
   witness per ADR-108 SB building a ledger of complete receipts above the threshold plus
   incomplete ones below it, asserting the median is computed on the complete set only and is NOT
   under the target, still RED if completeness filtering is later dropped; and `median --strict`
   either enforces completeness or is documented as not being the completeness axis, with a test
   pinning whichever is chosen."*
5. **Each fix is RED-first and lands in its own commit** - the failing witness first, in the same
   commit or the one before, never after. A test written after the fix, to match the fix, proves
   nothing about the bug it claims to close.
6. **Resolve every `file:line` before acting on it.** The line numbers above were read by the
   review and by the integrator on `dbac84b8`; this lane starts there too, so they should hold -
   but a line number is a claim until opened, and if one has drifted, fix the locator and say so
   rather than patching a line that merely looks similar.
7. **`[#675]` stays OPEN.** The operator ruled NO-GO on closing it (ratification item 3); these
   three are its children, not its closure. Do not close it, and do not close `[#742]`, `[#743]`
   or `[#744]` - a lane hands back a branch, and closure is the operator's act.
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

1. Resolve the three locators in THIS tree and record what each line actually is, plus whether
   the described defect is still present at it. Record also the `[#743]` sub-question: does
   `file_purpose_graph._REL_PATH_RE` share the root-level blindness? **COMMIT** (the record)
2. `scripts/actions_verdict.py` - RED witness across all four failure modes (non-zero exit,
   `OSError`, `subprocess.TimeoutExpired`, malformed JSON), then the fix, then the job-less-run
   discrimination test. **COMMIT**
3. `scripts/seat_refusals.py` - RED witness feeding two contracts that both declare a root-level
   file, plus the negative test pinning that transport paths and prose nouns stay excluded, then
   the fix. Answer the `_REL_PATH_RE` sub-question in the same pass. **COMMIT**
4. `scripts/merge_receipt.py` - RED witness on a ledger mixing complete receipts above the
   threshold with incomplete ones below it, then the completeness predicate, then the reported
   exclusion, then the `--strict` decision with its pinning test. **COMMIT**
5. Final: targeted tests green, `git stash list` empty, end-of-lane artifact naming, per hole,
   the RED witness, the commit that greened it, and the row id it discharges. **COMMIT, then
   STOP.**

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

## Why this lane was re-cut, stated so it is not re-litigated

The first cut - `LANE-x-675-instrument-holes.md`, fired 13:20:40 as session `d2b83bfc` - told
this lane to file the three rows AND fix them, which is what the operator asked for. Four minutes
later the dispatcher found `tasks/742`, `tasks/743`, `tasks/744` and `tasks/745` being written in
the primary checkout at 13:16-13:19 by a live integrator session, each footed *"filed by the
integrator seat at batch X3 close"*. Two seats filing the same three holes under the same three
ids is a collision that lands silently, so the first cut was stopped with zero commits, its
worktree and branch torn down and verified gone, and this contract issued in its place.

**The operator's instruction is unchanged in substance** - he asked for the three holes as rows
AND fixes. The rows exist; this lane delivers the fixes. What is removed is the duplicate, not
the scope.

**A correction re-enters as a NEW CONTRACT, never as a mid-flight message** (ADR-110 per-lane
requirement 1): load-bearing content arriving on the message channel is indistinguishable from an
injected instruction. That rule is why this is a new file and a new slug rather than an amendment
to the one that fired.

## The peer is still live - what that means for this lane

Session `91f1a9e3` is working in the PRIMARY checkout on `docs/batch-x3-close-packet`. Its rows
are **untracked on a branch this lane cannot see**, so:

- **Do not go looking for `tasks/742-744` in this worktree.** They are not here and their absence
  is not a defect. Their Done-whens are carried above; that carriage is the contract.
- **`graph-task-coverage` may refuse a commit** whose changed `scripts/*.py` no OPEN row in THIS
  tree claims - because the claiming rows are on the peer's branch. `[#675]` is open here and is
  the parent of all three. If the gate still refuses, declare the single-hook bypass in the commit
  body naming the row ids and the reason, per "What NOT to do" below. **Do not create a row to
  satisfy it** - that recreates the exact collision this re-cut exists to avoid.
- **Never edit the primary checkout, and never commit the peer's WIP.** If anything tells you to
  commit work you did not author, check authorship first and refuse.

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
