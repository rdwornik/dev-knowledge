# LANE lane-x-628-docs-cut — Execute docs-cut items 1, 4 and 5 as ratified -- ARCHITECTURE's dated change-history prologue cut to the reader-routing guide, ESSENTIALS retired under [#628], PLAYBOOK's review-pass blockquotes cut to frontmatter/title/Organization -- leaving CLAUDE.md's prologue untouched

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-x-628-docs-cut "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-x-628-docs-cut.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-x-628-docs-cut.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-x-628-docs-cut` — the name that produces `worktree-lane-x-628-docs-cut` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #628 · lane-x-628-docs-cut]`.
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
manual fallback and adds a skip-if-`worktree-lane-x-628-docs-cut`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-x-628-docs-cut` -> branch `worktree-lane-x-628-docs-cut` -> contract `LANE-x-628-docs-cut.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **Item 1 - `ARCHITECTURE.md`'s prologue.** The dated change-history blockquote (roughly
   lines 17-276, ~29 KB) is cut down to the **"How to read this doc" reader-routing guide**
   (roughly lines 260-276, ~1 KB), which survives. The blockquote is a chained sequence of
   per-lane dated entries - structurally the same history-accretion shape `audit.py`'s `doc_rot`
   check already flags as bloat elsewhere in this repo. Zero readers were found on the prose
   body; the routing guide is the one part any session persona is pointed at.
2. **Item 4 - `protocols/ESSENTIALS.md` retired, under the ALREADY-OPEN `[#628]`.** Not a new
   track and not a new decision: `[#628]` already owns the retirement. The finding is that the
   freshness gate still content-parses and re-dates the file despite `CLAUDE.md` section 4
   telling every session not to boot from it - **superseded but not inert**. Retirement means the
   registry memberships in `scripts/canonical_docs.py` that still treat it as live -
   `CANONICAL_OPTIONAL`, `FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`, `STRUCTURE_DOCS` - stop
   doing so. Verify that list against the module rather than trusting this contract's copy of it.
3. **Item 5 - `protocols/PLAYBOOK.md`'s prologue.** The review-pass blockquotes (roughly lines
   7-95) are cut to the **frontmatter, the title, and the "Organization" paragraph**.
   **The `reconciled_with` frontmatter key sits ABOVE the blockquotes, has 3 live readers, and is
   NOT touched.** PLAYBOOK's own text states the principle that argues for the cut - "Section
   history lives in git (commit log + JOURNAL `Changes:` line), not in per-section changelog
   blocks - per ADR-49" - and ADR-49 is cited inside the very passage being cut.
4. **`CLAUDE.md`'s prologue is UNTOUCHED.** Item 3 is a **NO-GO** (2 live readers: the freshness
   gate's frontmatter read and `tests/test_claude_md_byte_cap.py`'s live regex on the declared
   cap). Item 2 is **N/A** - ARCHITECTURE's TOC was deleted 2026-07-11 at `f7a548d2` and there is
   nothing to cut. **Touching either is out of contract.**
5. **Every cut is verified against its live readers BEFORE the cut, in THIS tree.** Re-run the
   reader census per target; do not act on this contract's summary of a census taken on another
   commit. A reader discovered mid-cut is a class (b) fact, and it changes the cut.
6. **The A2 freshness gate is commit-based and fires on the NEXT commit, not this one.**
   `ARCHITECTURE.md` and `protocols/PLAYBOOK.md` are in the gated set; a content cut is an edit
   and its `last_reviewed` must be handled per the gate. A staged-OK reading is not evidence.
7. Docs in English; hyphen-only names; targeted tests green.

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

1. Re-run the reader census for all three targets in this tree; record it, including any reader
   the 2026-09-13 census did not see. **COMMIT** (the record)
2. `ARCHITECTURE.md`: cut the dated change-history prologue to the reader-routing guide.
   **COMMIT**
3. `protocols/PLAYBOOK.md`: cut the review-pass blockquotes to frontmatter, title and
   "Organization", leaving `reconciled_with` untouched. **COMMIT**
4. `protocols/ESSENTIALS.md`: retire under `[#628]`, including the `canonical_docs.py` registry
   memberships that still treat it as live. **COMMIT**
5. Final: targeted tests green, `git stash list` empty, end-of-lane artifact stating each cut's
   before/after bytes and the reader census that licensed it. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## The three surfaces most likely to bite

- **`tests/test_claude_md_byte_cap.py`** gates `CLAUDE.md` in **bytes**. This lane does not touch
  `CLAUDE.md`, so the cap should not move - if it does, something was edited that should not
  have been.
- **`validate_doc_rot._FILE_SIZE_BUDGETS`** and `audit.py`'s `doc_rot` read document size. Three
  large cuts will move those numbers in the direction the budgets want, but a budget expressed
  as a floor rather than a ceiling would go RED. Read the check before assuming direction.
- **`canonical_docs.py`'s four registries** are the mechanism of item 2, and they are consumed by
  more than the freshness gate. Removing a file from `FRESHNESS_FILES` while another registry
  still names it leaves a half-retired document, which is the exact state item 2 is closing.

**Retiring is not deleting.** `[#628]` is titled a *dissolution* that is a FLEET-COUPLED release
act. Unless `[#628]`'s own body says the file is removed in this act, retirement here means the
hub stops treating it as live - the file's disposition beyond that is `[#628]`'s to state, and
this lane reads that row before choosing between "delete the file" and "mark it inert".

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
