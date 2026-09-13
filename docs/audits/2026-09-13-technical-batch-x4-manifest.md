---
batch: X4
seq: 4
status: open
closed_by: docs/audits/2026-09-13-technical-batch-x4-close-packet.md
---

# Batch X wave 4 — manifest (dispatch half) · 2026-09-13

**Seat:** dispatcher · **Batch:** X, wave 4 · **Ceiling:** ADR-110, six lanes
**Base at fire:** `main` = `dbac84b8` for **all four lanes**, and for the re-cut of slot 3 — a
single shared base, unlike wave 3, whose four openers straddled two (§6 finding 5 there).
**Status:** **FOUR CONTRACTS FROZEN, FOUR FIRED. SLOT 3 WAS STOPPED AND RE-CUT MID-BATCH** —
§4.2 and §6 finding 2.

**Consumers:** `[#664]` · `[#675]` · `[#628]` — plus `[#694]`, `[#655]` and `[#742]`/`[#743]`/
`[#744]` as the owners of individual clauses. Every contract named in §2 is copied in-tree into
`docs/audits/2026-09-13-technical-batch-x4-launch-contracts/`.

---

## 1 · The GO, recorded

This section IS the GO record. `to-browser/RATIFICATION-2026-09-13.md` — the operator's words of
2026-09-13, recorded the same turn — is the authority for every lane below. It answers the seven
asks of `DELETE-LIST-2026-09-13`, `CLOSURE-VERDICTS-2026-09-13` and `DOCS-CUT-LIST-2026-09-13`.

The four clauses this batch executes:

> **2 · DELETE-LIST — ALL AS PROPOSED.** 6 DELETE (ordered: `window_metrics` before `failed_set`;
> `gen_trend_dashboard` before `gen_north_star`), 2 TRIGGER (`archive_row_body` on the pre-commit
> stage; `logs_retention` on the SessionStart/Stop path), 28 KEEP with `cost_usage_telemetry.py`'s
> stale disposition text corrected.

> **3 · `[#675]` — NO-GO.** Stays open; the three verified false-pass holes … become rows.

> **5 · `scripts/worktree_seed.py` register row — GO.** Delete the `ORPHAN_DISPOSITIONS` entry …

> **6 · The two `safe_remove` false-PASS instances — REMOVE THE DEAD CALLERS, do not restore the
> modules.** … One row files what provisioning's history/ecosystem repair actually needs, since
> those call sites silently did nothing.

> **7 · Docs cuts — GO on items 1, 4 and 5** … CLAUDE.md's prologue stays (item 3, live readers).
> Item 2 is N/A.

**Scope bound:** the GO covers these four lanes and no lane outside them fires on it. Ratification
item 4 (`[#734]` NO-GO, the 16 UNKNOWN) is explicitly **not** in this batch. Ratification item 1
is not a lane at all — it is routed through the decision engine, §5.

## 2 · THE LANES — four, frozen 2026-09-13

```
slot  row     slug                                model   effort  state
1     #664    lane-x-664-delete-list-execution    opus *  high    FIRED 13:20:28  session 9757fac2
2     #664    lane-x-664-dead-callers             sonnet  high    FIRED 13:20:34  session c5139e47
3     #675    lane-x-675-instrument-holes         opus *  high    STOPPED 13:26 -- superseded, §4.2
3'    #675    lane-x-675-instrument-fixes         opus *  high    FIRED 13:30:11  session d12e4c7f
4     #628    lane-x-628-docs-cut                 sonnet  high    FIRED 13:20:46  session 90a457c1
```

`*` **Slots 1 and 3 fire at `opus`, not the `opusplan` the operator ordered.** Re-measured at this
freeze rather than inherited — §6 finding 1. Each contract carries the correction and the
disclosure in its own body, so the contract and the dispatched line agree.

**Concurrency 4, no backfill.** Four lanes, four slots, so there is no queue: all four fire
together and nothing waits. `sleeping-poll` therefore reports 0 declared waits, and that is the
honest reading rather than a skipped check — the wave-3 merges were already on `main` at
`dbac84b8`, the tree was clean, and zero `lane-x-*` worktrees were registered, each read off the
ref surface directly.

**Serialisation groups: none.** No two lanes declare the same file (§3), and no two touch the
persisted graph store in the way wave 3's slots 2 and 5 did.

## 3 · STEP 0 refusals

| check | result |
|---|---|
| `lane-ceiling --check-worktrees` | **PASS** — 4 lanes ≤ 6, checked before any worktree existed. It passed here where it refused twice in wave 3, for one reason: this seat's freeze worktree did not yet exist at step 0. The absent discriminator wave 3 filed is unfixed; this batch simply did not trip it. |
| `carried-by` | **REFUSED, once, on a file this seat did not author** — `DECLARE-BATCH-V-CLOSE-2026-09-09.md` carries `carried-by: BACKLOG.md`, which names neither a repo path nor `OPEN`. A batch-V transport declaration, four days old. Reported, not edited: it is another seat's frozen declaration and this batch writes no DECLARE-/AMEND-/BATCH- file of its own. |
| `file-collision` | **PASS** — 4 contracts, 23 declared paths, no file claimed twice. Re-run on the corrected set after the slot-3 re-cut: 21 paths, still no collision. **This PASS is correct by luck, not by check** — see §6 finding 3. |
| `sleeping-poll` | **PASS** — 0 declared waits (see §2). |
| `dryrun-step0` | **PASS** — 4 of 4 contracts DryRun on the last line of step 0. |

## 4 · Receipts

### 4.1 Dry runs and fires

All five contracts (four openers plus the slot-3 re-cut) were DryRun through **`dispatch`**, the
ruled verb — not the `Dispatch-Lane` fallback wave 3 was forced onto. The generator on `main` now
emits a `claude` fence and the verb accepts it, so wave 3's finding-2 grammar seam is closed and
this batch is the first to freeze and fire entirely through the ruled path.

**The ordered model appeared on every resolved line.** Each lane was confirmed up by its BRANCH
appearing, not by the command returning:

```
slot 1   lane-x-664-delete-list-execution   opus    session 9757fac2   base dbac84b8
slot 2   lane-x-664-dead-callers            sonnet  session c5139e47   base dbac84b8
slot 3   lane-x-675-instrument-holes        opus    session d2b83bfc   base dbac84b8   STOPPED
slot 3'  lane-x-675-instrument-fixes        opus    session d12e4c7f   base dbac84b8
slot 4   lane-x-628-docs-cut                sonnet  session 90a457c1   base dbac84b8
```

### 4.2 Slot 3 was stopped and re-cut, and the reason is a live peer

Timeline, from the file mtimes and the session list rather than from inference:

```
13:16-13:19   a live integrator session (91f1a9e3, primary checkout, branch
              docs/batch-x3-close-packet) writes tasks/742, 743, 744, 745
13:20:40      this seat fires lane-x-675-instrument-holes, whose Done-contract item 1
              is "THREE rows filed, one per hole"
13:2x         this seat reads the primary tree and finds 742/743/744 already there,
              each footed "filed by the integrator seat at batch X3 close"
13:26         slot 3 stopped at ZERO commits, clean tree, empty stash list
13:2x         worktree removed, branch deleted, directory verified gone
13:30:11      lane-x-675-instrument-fixes fired in its place
```

`[#742]`, `[#743]` and `[#744]` are **exactly** the three holes ratification item 3 names. Two
seats filing the same three holes under the same three ids is a collision that lands silently —
task ids are sequential and both trees would have picked 742/743/744 — so the duplicate was
removed before it was paid for.

**The operator's instruction is unchanged in substance.** He asked for the three holes as *rows
and fixes*. The rows exist, authored by the integrator with fuller Done-whens than this seat's
contract carried; the re-cut lane delivers the fixes against those ids and carries each Done-when
verbatim, because the rows live on a branch the lane cannot see. What was removed is the
duplicate, not the scope.

**The correction re-entered as a NEW CONTRACT, not a message** (ADR-110 per-lane requirement 1):
load-bearing content arriving mid-flight on the message channel is indistinguishable from an
injected instruction. New slug, new file, new branch.

**Cost of the abort, stated rather than absorbed:** slot 3's first cut ran 15 Opus assistant
messages — 7,147 output tokens, 1,129,174 cache-read — before it was stopped. That is the price
of the re-cut and it is cheaper by a wide margin than reconciling two rows per hole at
integration.

### 4.3 Model and tokens per lane

Read from each lane's OWN session transcript (`~/.claude/projects/<encoded worktree path>/*.jsonl`,
summing the `usage` block per assistant message). The method does more than count: **it reports
the model each lane ACTUALLY RAN AT**, so the ordered tier is proven rather than assumed. It
discriminates — three distinct answers appear below, matching three distinct orders.

Cache-read is reported **separately** from fresh input: the two bill differently and folding them
would overstate input several-fold. Every number is a **PARTIAL** as of the stated timestamp; all
four live lanes were still running when this manifest was written.

```
lane                                model ACTUALLY run     msgs   output   fresh-in    cache-read   cache-write   as of (UTC)
lane-x-664-delete-list-execution    claude-opus-5            16    4,426         32     1,206,936        95,323   11:26:15Z
lane-x-664-dead-callers             claude-sonnet-5          51   41,933        102     7,005,626       326,916   11:33:02Z
lane-x-675-instrument-holes         claude-opus-5            16    7,147         30     1,129,174       103,117   11:26:31Z  (STOPPED)
lane-x-675-instrument-fixes         claude-opus-5             7    1,461         14       458,728        86,590   11:33:18Z
lane-x-628-docs-cut                 claude-sonnet-5          66   73,200        132     9,380,089       503,641   11:32:51Z
```

**Every lane is running the tier this seat ordered.** That is the point of the reading: the two
`opus` corrections are confirmed as Opus rather than hoped to be, and the two `sonnet` lanes are
Sonnet, so the instrument is discriminating and not printing one answer.

## 5 · Ratification item 1 is NOT a lane

**Should `.claude/commands/*.md` count as a `[#664]` wiring surface?** The operator answered YES,
with a condition — ADOPTION-BY-INVOCATION — and **routed it through the decision engine
(`[#692]`, on `main` at `a77e3302`) rather than ruling it in chat**: intake → alternatives →
response measure → flip condition → ADR, with the ratification as its input.

That filing is this seat's own act, not a lane's, and it is `docs/intake/2026-09-13-command-files-as-a-wiring-surface.md`
plus the ADR the engine produces. It deliberately does not ride any of the four lanes: three of
them touch modules whose orphan status the answer would change, and a lane that could move its own
census reading is the wrong seat to decide what the census counts.

**Slot 3' is told this explicitly** — `merge_receipt.py` and `actions_verdict.py` are both wired
to `.claude/commands/lane-integrate.md`, and its contract forbids adding a hook to either to make
an orphan count fall.

## 6 · Findings

1. **`opusplan` IS STILL INERT ON A `--bg` LANE ON THE CURRENT CLI, AND THIS SEAT MEASURED IT
   RATHER THAN INHERITING IT.** Wave 3 filed this (§6 finding 7, measured on CLI 2.1.224 across
   84 assistant messages). The installed CLI is now **2.1.270**, so the claim was re-run before
   deviating from an operator instruction on its strength:
   `claude --print --model opusplan --permission-mode bypassPermissions` produced a transcript
   whose every assistant message records `claude-sonnet-5`. The cause is structural and unchanged
   — `opusplan` routes Opus to PLAN MODE, and every dispatch constant puts a lane on
   `bypassPermissions`, which never enters plan mode; with no plan phase there is no Opus phase.

   The operator ordered `opusplan` for slots 1 and 3. Firing it would have delivered Sonnet — a
   tier he did not name either — so there was no faithful-literal option and **both** choices
   deviate. `opus` is the one matching intent: his own gloss for the tier is "Opus plans", and
   Ch8's routing matrix routes gate and organ code to `opus`. **Unlike wave 3, the correction is
   in the frozen contract as well as on the line**, so the two cannot disagree and the lane reads
   the disclosure itself. §4.3 confirms both lanes actually ran Opus. The operator may reverse
   this; re-firing is one command.

2. **A live peer invalidated a frozen contract's premise four minutes after it fired.** Full
   timeline in §4.2. The structural lesson is not "check for peers" — it is that **`git status` on
   the primary checkout was the cheapest possible detector and this seat only ran it incidentally,
   while verifying its own worktrees**. A dispatcher opening a batch should read the primary tree's
   branch and untracked set at step 0: a peer mid-write is visible there and nowhere else, and it
   is the one input a frozen contract cannot carry.

   Related and worth its own line: **the primary checkout was on `docs/batch-x3-close-packet`, not
   `main`**, and this seat's session-start context recorded it as `main`. A snapshot taken at boot
   is stale the moment another seat moves.

3. **`file-collision` PASSED this batch by luck, and the hole is one of the three the batch is
   fixing.** `[#743]` — filed by the integrator, adopted by slot 3' — says the step-0 collision
   extractor requires a slash and therefore cannot see root-level tracked files, naming
   `ARCHITECTURE.md` and `.pre-commit-config.yaml` explicitly. **This batch declares both**:
   `lane-x-628-docs-cut` writes `ARCHITECTURE.md`, `lane-x-664-delete-list-execution` writes
   `.pre-commit-config.yaml`. Neither appears in the extractor's 23 declared paths, and had two
   lanes declared the *same* root-level file the check would have passed anyway. They happen not
   to collide, so the batch is safe — verified by hand, not by the organ.

4. **`dispatch … -DryRun` no longer exits 1.** Wave 3's finding 4 recorded every DryRun leaking
   exit 1 from an internal branch-exists probe. Measured here on all five contracts:
   `$LASTEXITCODE` is 0 and `$Error.Count` does not increment. That finding was taken on the
   `Dispatch-Lane` fallback; the ruled `dispatch` verb does not carry it. The wave-3 finding is not
   wrong, it is **path-specific**, and the distinction matters to anything wrapping either verb.

5. **`'m' is not recognized as an internal or external command` still prints on every fire** —
   wave 3 finding 6, unfixed, and it reproduces on the ruled `dispatch` verb as well as the
   fallback. Cosmetic: all five lanes came up and their branches appeared. It also prints on
   `claude agents` and `claude stop`, so it is in the shared output path, not the dispatch verb.
   It will mislead whoever next greps a dispatch log for errors.

6. **`claude stop` does not release the worktree; `claude rm` does.** Stopping slot 3 left the
   worktree *retained and git-locked* (`fatal: cannot remove a locked working tree, lock reason:
   claude session … (pid 47528)`), so `git worktree remove` and `git branch -D` both refused. The
   CLI's own `claude rm <session>` removed worktree, branch and directory together, verified
   individually afterwards. A seat that reaches for git first — the obvious move — gets two
   refusals and may conclude the teardown is stuck.

7. **`isolate_step0` makes the step-0 heading placement load-bearing, and the refusal message does
   not say so.** `dryrun-step0` refused with `dryrun-absent` against a file whose DryRun lines were
   plainly present: the check isolates the section under the *first* heading matching `step 0` and
   stops at the next heading of any depth. A file titled `# STEP 0 — …` with sections beneath it
   therefore isolates to its own title block and reads as empty. The remedy is to make the
   step-0-named heading the LAST section and end the file on a DryRun line. Correct behaviour by
   its own docstring (terra HIGH, 2026-09-09); the refusal text says "carries no `-DryRun` line"
   when the truth is "carries none *in the isolated section*", which sends the reader to the wrong
   repair.

8. **Nine worktree HUSKS from earlier waves sit in `.claude/worktrees/`** — `dispatch-x14-freeze`,
   `dispatch-x3-freeze`, `lane-x-000-docs-cut-manifest`, `lane-x-000-trustworthy-suite`,
   `lane-x-664-spine-armed`, `lane-x-683-three-small-fixes`, `lane-x-689-conductor-e-proof`,
   `lane-x-691-routing-half-a`, `lane-x-730-one-command-closure` — each holding a `logs` directory
   and registered in **no** `git worktree list`. They are unregistered directories, so the ADR-110
   "No leftovers" round-trip did not complete for any of those lanes. Four of the corresponding
   sessions are still listed as `idle` rather than removed. Not this batch's to clean — it did not
   create them, and removing another seat's directory is not a dispatcher act — but the provision→
   cleanup round-trip is demonstrably not closing, and `claude rm` (finding 6) is the verb that
   would have closed it.

9. **The `[#630]` manifest/contract agreement predicate is EITHER VACUOUS OR WRONG, and this seat
   measured both halves.** `gen_lane_contract.py::_check_manifest_contract_agreement` resolves its
   open batches with `batch_manifest.open_batches()`, which reads the **committed** tree
   (`git show HEAD:<manifest>`), then requires set equality with **every** batch it finds.

   - **One commit carrying manifest AND contracts — the shape the check's own comment says it
     guards** (*"a freeze commit stages its contracts UNDER `docs/audits/<batch>-launch-contracts/`,
     so they are in-tree and still compared"*) — is checked against **ZERO** batches. The
     manifest declaring the batch is not in `HEAD` yet, so `open_batches()` returns `[]` and the
     adapter logs *"no open batch — 0 checked"*. **Measured here, on this batch's own files.** The
     batch-E defect it was built to catch is exactly a freeze-time slug divergence, and at freeze
     time the check cannot see the batch.
   - **Split into manifest-then-contracts, it fires — against every open batch, including ones it
     does not own.** With X3 still open in this tree (its close packet was committed on
     `docs/batch-x3-close-packet` at `e0761575` and not yet merged here), staging X4's five
     contracts refused against **X3's** manifest: *"contract(s) [...] are named by no manifest
     row"*. Two open batches is the normal state at a wave handover, not an edge case.

   **What this seat did about it.** It synced to `origin/main` — which closed X3 in this tree, the
   same act that cleared finding 10's phantom spine block — and then committed **manifest first,
   contracts second**, which is the one ordering under which the predicate both fires and fires
   against the right batch. That is more work than landing them together and it is the reason:
   landing them together would have passed, unchecked, and the pass would have meant nothing.
   `--no-verify` was available at every step and was not used.

   **The fix belongs in the adapter:** compare a contract against the batch that CLAIMS it —
   resolvable from the contract's own path, `docs/audits/<batch>-launch-contracts/` — rather than
   against every open manifest, and read the staged tree rather than `HEAD` so a freeze commit is
   checkable at freeze time. It is `[#630]`'s to own.

10. **A phantom spine block cost one commit, and the gate's own diagnostic settled it in one
    command.** `audit-health` FAILed on `journal_spine_anchor`: *"1 first-parent spine entry above
    the disposition floor carries no JOURNAL anchor: `c0e0722f`"*. The discriminator the refusal
    prints — `journal_anchor.is_anchored` read in this tree versus at `main` — returned
    **False here, True at main**, which is the recorded signature of tree lag rather than a real
    gap. `git merge origin/main` cleared it. Worth recording not as a new defect but as the
    check working exactly as designed: the refusal carried its own discriminator, the
    discriminator was decisive, and the prescribed remedy was correct on the first attempt. The
    lag was real — this tree was branched at `dbac84b8` while the integrator merged X3 to
    `c0e0722f` underneath it.

## 7 · What this seat did NOT do

- **No non-Claude producer was ordered.** Nothing in this batch routes work to Grok, Copilot or
  Codex.
- **No peer work was touched.** The integrator's four untracked rows, its modified
  `scripts/graph_queries.py`, and the branch it is working on were left exactly as found. This
  seat read the primary tree and wrote nothing into it.
- **No husk was cleaned** (finding 8) — nine directories belonging to other seats' sessions, four
  of them still listed.
- **`carried-by`'s one refusal was not repaired** (§3) — a batch-V transport declaration this seat
  did not author.
- **Ratification item 4 (`[#734]`, the 16 UNKNOWN) was not scheduled.** The operator ruled it
  NO-GO and named it the next lane's scope; the integrator has filed `tasks/745` for it.
