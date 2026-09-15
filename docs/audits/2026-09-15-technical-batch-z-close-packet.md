# Batch Z close packet — the night of 2026-09-15

> **Integrator seat.** The closing half of `docs/audits/2026-09-15-technical-batch-z-manifest.md`
> (ADR-110 refuse-to-finish: *manifest/packet archived — two halves*). Immutable once landed;
> supersede with a new file or an in-file amendment marker.
>
> **Every figure here was derived fresh at close**, from the ledgers, the transcripts and the
> conductor — never restated from a session's memory. Where a figure could not be derived it says
> UNKNOWN and why, never zero. Three figures carried in the seat's own working notes were **wrong**
> and are corrected here by the instruments: receipt completeness (§3), the integrator's cost (§1)
> and the lane-z-0 merge SHA (§3). A packet that only confirms its author's notes has measured
> nothing.

## 1 · The six numbers the night is judged by

### (1) Organs that refused something real

**Fifteen organs refused, and the refusals separate into three kinds that must not be summed.**
A refusal that caught a defect is evidence the mesh works. A refusal that caught a missing
ceremonial line is evidence it is armed. A refusal to *guess* is neither, and is the most
valuable of the three.

**Refused a real defect — 11 organs, 24 refusals:**

```
seat_refusals lane-ceiling      1   16 lanes against a ceiling of 6 -- forced the re-cut at STEP 0
decision-coverage               1   4 accepted decisions no row implemented; blocked EVERY commit
                                    repo-wide until [#764] was filed
journal_spine_anchor            2   2 genuinely unanchored first-parent spine entries
                                    (0ee3d161, a7620dd0)
block-unanchored-push           1   a single-commit arc that cannot anchor its own merge
graph-task-coverage             2   an unclaimed intake file; a live receipt state-file staged
                                    by accident
gen_task_tree identity          3   a missing manifest node; TWO live id collisions
doc-counts / organ-index /      4   generated files stale on the merged tree
  audits-index freshness
deny-and-point ([#727])         2   raw greps over questions the repo graph already answers
test_generator_newlines         1   provider_bench.py:1072 writing text without pinning LF
release_lint C5 floor-pin       5   5 historical manifests pinning a superseded floor sha
SUITE-BASELINE-FREEZE rule      2   2 merges refused, 2 real defects behind them (see section 2)
```

**Refused a missing ceremony — 2 organs, 5 refusals:** `backlog-filing-backpressure` (3x, a merge
introducing a new id with no `kill-candidates:` line) and `backlog-id-on-close` (2x). Correct
behaviour; no defect behind it.

**Refused to GUESS rather than refusing an act — 2 organs, and these are the quiet ones.**
`lane_cost` reports a missing transcript as **UNKNOWN rather than zero**, and refuses to price an
unregistered model id — *"it cannot be priced, and it is not free"*. `provider_bench` sets
`usd_comparable: false` rather than dividing a subscription quota by a token count to manufacture
a rate. **A benchmark that guesses is worse than one that abstains**, and both abstained. Both
abstentions are load-bearing below: they are why numbers (2) and (4) are honest.

**One refusal was a safety check working against me, correctly:** `git branch -d` refused a branch
fully merged to HEAD because its **upstream ref still existed**. The fix is ordering — delete
origin first — never escalation to `-D`.

### (2) Cost, per lane and per model

Derived fresh at close from the transcripts, rates `as_of 2026-06-24`, priced by
`lane_cost.py lane`.

```
lane-z-4-non-claude-execution      USD  50.64   351 calls    80,261,133 tokens
lane-z-0-quality-requirements      USD  40.72   337 calls    66,106,211 tokens
lane-z-746-devcontainer-substrate  USD  40.19   271 calls    67,718,219 tokens
lane-z-10-aj-m04-first-pass        USD  28.67   208 calls    46,193,039 tokens
dispatch-z-manifest                USD  27.97   181 calls    43,914,934 tokens
integrator seat (session 9b8de937) USD  82.53             136,283,287 tokens
                                                   23:07Z -> 06:51Z
lane-z-11-three-repo-comparison    UNKNOWN -- CC CLOUD lane, no local session store
lane-z-14-management-map           UNKNOWN -- never produced a branch (see section 3)
                                   ---------
MEASURED TOTAL                     USD 270.72
```

**Per model: one model.** `claude-opus-5`, 100% of every measured seat. Ordered `opus`, ran
`claude-opus-5` on all six lane receipts — `merge_receipt models` reports `agree` every time.

**The integrator seat cost USD 82.53 — more than any single lane, and 30.5% of the measured
total.** That is the figure this batch should be least comfortable with, and it is stated on its
own rather than averaged into the lanes: **integration was not the cheap part.**

**A correction the instrument forced.** Asking `lane_cost` for the integrator seat by its
*directory* returns **USD 8,714.37 over 52,822 calls across six models** — the primary checkout's
**lifetime** total, every session ever run there, not tonight's. The session store is keyed
**per directory, not per lane**, so a seat sharing a directory with its own history cannot be
measured by slug alone. The USD 82.53 above is this session's transcript priced on its own.
**A per-directory tally reported as a per-lane cost would have overstated the night by 32x.**

**The cost ledger `logs/LANE-COSTS.jsonl` carries ZERO batch-Z rows** — 6 rows, all batch Y. No
batch-Z lane ran `lane_cost close`, so every figure above was recomputed at close from transcripts
rather than read from the ledger, and the ledger's own `report` verb still answers
*"USD 159.87 over n=5"* — **batch Y's number, to a question about batch Z**. A figure that must be
recomputed at close is not a ledger.

### (3) BACKLOG bytes and rows against 72,000

```
at the freeze SHA b5270d63 :  94,255 bytes   332 rows
at batch close             :  97,244 bytes   347 rows
the bar                    :  72,000 bytes
                              -------------
over the bar by            :  25,244 bytes   (135.1% of the bar)
moved this batch           :  +2,989 bytes   +15 net rows
```

**The batch moved the wrong way, by design.** Two of the six lanes existed to *find* things
(z-10's UNOWNED matrix, z-4's provider census), and a lane that finds things files rows. The bar
was already breached by 22,255 bytes before the night started; this batch added 2,989 more.
`[#754]` (backlog-to-bar) is batch Y's row for the bar itself and did not run tonight.

### (4) The non-Claude verdicts against the Opus price

**The question has two halves and they have opposite answers.** On *capability* the comparison was
made. On *price* it could not be, for every provider including the baseline against itself.

```
provider   outcomes  verdict          usd        why not comparable to Opus USD 0.217038 / 10
copilot      10/10   parity           UNPRICED   'mai-code-1.1-flash' not declared in the registry
codex        10/10   parity           UNPRICED   'gpt-5.6-terra' IS declared, carries no rates block
agy          10/10   parity           UNPRICED   no served model attested for the run
ollama        8/10   below-baseline   UNPRICED   'qwen2.5-coder:14b' not declared in the registry
gemini        0/10   unreachable      UNPRICED   no served model attested; refused at auth
claude       10/10   parity (base)    0.217038   own leg partial: one 959-token unregistered
                                                 claude-haiku-4-5-20251001 sub-call
```

**Three of five non-Claude providers reached parity with Opus on ten bounded outcomes.** Scope,
stated because the number is worthless without it: *ten bounded, self-contained, closed-form text
outcomes, ONE run each, from a neutral empty non-git directory, no tool use and no repo access* —
**not a measure of agentic work, long context, or anything run twice.**

**`usd_comparable` is false on all six rows, including the baseline against itself.** So the answer
to *"what do the non-Claude providers cost against Opus"* is **that the comparison cannot be
made**, with a named reason per provider — and that is a better answer than a ratio, because
**four of the six failures are registry failures, not vendor ones.** A rate-card gap and a vendor
that does not publish prices are different problems with different fixes, and a ratio would have
hidden which was which.

One capability finding outweighs the price half: copilot served **two different models**
(`gpt-5.6-luna`, `mai-code-1.1-flash`) to *identical* invocations, so **a copilot result is not
reproducible from the command line alone.**

### (5) Did Actions run a lane end to end?

**No lane ran on Actions. The conductor ran on every merge.** Different claims; the question
deserves both halves.

- **`lane-z-15-actions-lane` was among the ten lanes DEFERRED** in the 16-to-6 re-cut. The Actions
  substrate was never exercised as a lane host tonight.
- **The conductor ran 12 times on 2026-09-15**, once per push, each executing
  `phase-gate -> pytest -> ruff -> seal -> terra`. **All 12 concluded `failure`**, every one on
  `pytest` alone — ruff, seal, terra and the phase gate passed in all 12.

So Actions **verified every merge end to end and hosted no lane**. A green conductor run did not
occur tonight and is not claimed.

### (6) Rows filed versus rows closed

```
filed   : 16   (763 764 765 766 767 768 769 770 771 772 780 781 782 783 784 785)
removed :  0
closed  :  1   ([#782], and it is `superseded`, not `closed`)
net     : +15
```

**Two of the sixteen are renumbers, not findings.** `[#784]` and `[#785]` are the *same* two
findings under new ids after the collisions in section 4. Counting them as discoveries inflates
the filed figure by two; the honest count of distinct findings filed is **14**.

**The one closure was a duplicate, not an achievement.** `[#782]` is `superseded` into `[#765]` and
deliberately NOT `closed` — the work is not done. **The ratio is 16:1 against.** Batch Z was a
finding batch, and a finding batch that closes nothing is honest only if it says so.

## 2 · The freeze judged six merges, refused two, and found three real defects

`logs/SUITE-BASELINE-FREEZE.md` froze **51** conductor failures at `b5270d63` (roster re-parsed at
close: 51 members, file 14,487 B). Membership is tested **by node id, never by count.**

```
merge                      run           failed  outside 51  departed  verdict
4f4186a6  z-746            34923007619     51        0          0      clean -- identical set
70356500  docs arc         34925873604     52        1          0      REFUSED
2830d3d6  z-0              34929184598     59        8          0      REFUSED
a9b41529  debts            34930659346     58        7          0      1 cleared
73789d49  z-10             34933836238     58        7          0      --
5bbc3be6  z-4  (CLOSE)     34935949858     59        8          0      3 of 8 fixed, unmerged
```

**The close measurement, re-derived member-by-member at close:** 59 failed, **8 outside the frozen
set, 0 departed**. The eight are 2x `test_gen_audit_index`, 1x `test_generator_newlines`, and
**5x `test_release_lint`**. The first three are the index-and-newline debts already fixed in
`708864bd`; **the five `release_lint` failures are the whole remainder**, and they are governed by
intake 100 rather than patched.

**`0 departed` is the expected result, not a failed predicate.** `[#763]` requires that *every
cause whose lane merged must have left the set*, naming C8 (lane 7), C5 (lanes 2 and 3) and C2
(lane 1). **None of those four lanes ran** — all were in the deferred ten. The predicate has no
live subject this batch, which is a different finding from a predicate tested and failed, and the
distinction is the whole point of judging by member rather than by count.

**Defect one — the first refusal found something nobody had recorded.** `70356500` is all digits,
and `preflight_contract` **silently skips an all-digit short SHA**: it reads as a number, not a
locator. The tree was innocent; the hash was not. Reproduced against four inputs varying one
thing. **Consequence: the baseline is not fully reproducible** — the same tree measures 51 or 52
depending on the SHA it is measured at, about one commit in forty-four. Filed **intake 99**; the
freeze carries an appended amendment.

**Defect two — the second refusal found lane z-0's floor-repin blast radius.** Three of the eight
were index debts the lane had declared by name and the seat paid; five are `release_lint` C5
across five historical manifests (v1.1.0 to v1.4.0) still pinning a superseded floor sha.
**`release_lint` contradicts itself within one run:** C7 calls a non-current manifest
*"released/historical, not compared to live constants"* while C5 compares its floor pin to the
live sidecar. Filed **intake 100** and **deliberately NOT resolved** — choosing between re-pinning
the history and making C5 version-aware decides what a tagged manifest *means*, and as the **first
floor-template change ever**, the answer becomes the precedent. An operator's question, not an
integrator's.

**Defect three — found at close, in the comparison mechanism itself.** A parametrized node id whose
parameter contains a **space** (the `test_head_token_normalises_the_way_the_reader_normalises`
case, parametrized on a `C:/Program Files` path) is truncated at a different point by
whitespace-delimited extraction than by the freeze file's own rendering. It therefore appears as
**both a regression and a departure** in a naive diff — one spurious entry on each side, which
cancel, leaving the *totals* right while both *rosters* are wrong. **`[#763]` mandates comparison
by node id, and this is the id class on which that comparison silently breaks.** It was caught only
because 8-outside/1-departed was implausible enough to check by hand. Belongs to `[#763]`.

**Nothing was absorbed into the frozen set.** Absorbing a failure would convert a live defect into
an accepted one by the act of noticing it — precisely the failure mode a freeze with an expiry
exists to prevent.

## 3 · Lanes, merges, and receipt completeness — where the seat's own notes were wrong

Six lanes fired. **Five landed. One produced nothing.**

```
lane                              lane merge   receipt              complete?          review
lane-z-11-three-repo-comparison   b81c5548     merge-z-11           NO  -- teardown    none (docs)
z-manifest (dispatcher)           8d029783     merge-z-manifest     yes                --
lane-z-746-devcontainer-substrate 4f4186a6     merge-z-746          NO  -- teardown    codex clean
  its packet                      a7620dd0     merge-z-746-packet   n/a (kind=arc)     --
lane-z-0-quality-requirements     2830d3d6     merge-z-0            yes                codex 2 HIGH
lane-z-10-aj-m04-first-pass       73789d49     merge-z-10           NO  -- teardown x2 none (0 code)
lane-z-4-non-claude-execution     5bbc3be6     merge-z-4            NO  -- teardown x3 codex 3 CRIT
```

**Only 2 of 6 batch-Z merge receipts are COMPLETE, and the seat's working notes claimed four.**
`merge_receipt median` is the instrument that caught it. **Every one of the four exclusions is a
failed `teardown` step — seven failed teardown attempts across four lanes — and not one is a suite
or a review failure.** On Windows `git worktree remove` loses to an OS file lock held by a live
shell, and the lane that fought hardest (z-4) recorded three failures rather than one success it
could not honestly claim.

**This is the batch's most under-weighted finding.** Teardown is the step everyone treats as
janitorial, and it is the sole reason two thirds of the night's receipts cannot enter the median.
The median consequently runs over **n=3 across all batches** and reports 18.3 min (range
12.4 to 67.9) — a number too thin to mean much, and thin *because of teardown alone*.

**AY1-1 is working correctly and must not be confused with the above.** Every batch-Z receipt also
carries a failed `actions` step, because the conductor's exit code is non-zero while the suite
verdict is `PRE-EXISTING`. The median **does not** exclude on that — completeness is judged on the
suite step's verdict STATE, not the exit code. `merge-z-manifest` and `merge-z-0` both carry a
failed `actions` step and are complete. Exactly as ruled.

**`merge-z-0`'s receipt closed at `b0a6b79c`, not at the lane merge `2830d3d6`** — `b0a6b79c` is
the follow-on `docs/z-0-release-lint-regression` merge. The lane merge and the receipt's
`merge_sha` are therefore different commits, which is worth knowing before anyone joins the two
ledgers on that field.

**`lane-z-14-management-map` is EXPLICITLY ABANDONED** (the ADR-110 checklist requires the word).
The manifest records it dispatched to CC CLOUD with a session id and `G1/G2/G3 OK`. It produced
**no branch on origin, no commits, no artifact**. Its row `[#781]` stays OPEN. **A cloud session
that reports its gates green and lands nothing is indistinguishable, from the integrator's side,
from one that never started** — the same could-not-look-versus-looked-and-fine shape this batch
found in five other places (section 6).

**`merge-z-746-packet` is receipted `kind=arc`, not `kind=merge`, deliberately** — a trailing
artifact landing with near-zero ceremony would drag the merge median toward it and flatter the
very figure the ledger exists to keep honest. Its verdict is `UNATTRIBUTED` and cannot be
otherwise: `a7620dd0` was pushed *inside* the range `4f4186a6..70356500`, and the conductor runs on
the range head. **Per-merge verdicts exist only for merges pushed individually.**

## 4 · Three id collisions, and all three were the integrator's fault

`[#763]` was allocated **from the integrator seat while six lanes were running**. It was already
taken by lane z-10, which renumbered `[#763]` to `[#765]` — straight into lane z-0's id — and then
to `[#784]`. Lane z-4 independently collided on `[#772]` with lane z-10's P1 and went to `[#785]`.

**The defect is the seat, not the lanes.** A lane cannot see a branch that does not exist yet, so
two seats drawing from one free space collide silently. `[#785]`'s renumber touched **9 files and
114 references**, 96 of them the `row:` provenance field on every recorded bench measurement —
leaving those would have pointed every measurement at another lane's credentials row.

**The renumber then failed silently and was caught by an organ, not by the seat.** The first
rewrite script skipped all 13 files and reported success: `Path.read_text()` takes no `newline=`
kwarg, and a blanket `except Exception: continue` swallowed all 13 `TypeError`s. Only
`gen_task_tree`'s identity refusal caught it. **A bare `except` around a file rewrite converts a
total failure into a clean run.**

## 5 · What the reviewer produced, separated by whether it fired

**Lane z-0 — 2 HIGH, both confirmed in source.** `requirements()` silently drops a non-dict
register row instead of refusing it; and the register's `trip_test` is verified as a **FILE** and
never as a **TEST**, so an entry citing `tests/x.py::does_not_exist` resolves clean. **Neither
needed a new row** — `[#765]`'s own Done-when already requires the trip-test to resolve to a test
that exists and passes. **The open row already named the gap**, which is why it stays open rather
than spawning a sibling.

**Lane z-4 — 3 CRITICAL, all confirmed in code, ALL LATENT.** A non-zero exit can score as a pass
(*realised: 0 of 11 such rows*); missing token counts are priced as a free run (*realised: 0 rows
at `usd == 0.0`*); and a 9-of-10 total can compare as complete — where **the function's own
docstring states the opposite rule**, so the invariant is documented and unenforced (*not
realised: every non-Claude provider is wholly unpriced, never partially*).

**That none fired is a property of tonight's data, not of the harness.** Recorded as latent rather
than realised on purpose: **a latent defect written up as realised defames the instrument**, and
*the instrument was right tonight* is not the same claim as *the instrument is trustworthy*.

## 6 · The recurring shape this batch found in six places

**Could-not-look reported as looked-and-fine** — independently, by four sessions, in six organs:

1. `preflight_contract` on a shallow clone (lane z-11)
2. the devcontainer B1 history guard, exit 2 (lane z-746)
3. `preflight_contract` again, on an all-digit SHA (the freeze rule, intake 99)
4. the quality register's trip-test citation (lane z-0, via codex)
5. `provider_bench`'s non-zero-exit and missing-token paths (lane z-4, via codex)
6. lane z-14's cloud session reporting `G1/G2/G3 OK` and landing nothing (section 3)

**Six sightings is not a coincidence, it is a class.** **Not one of the six was found by the organ
that owned it**; every one was found from outside.

## 7 · Refuse-to-finish checklist (ADR-110)

1. **Every lane branch merged or explicitly abandoned** — five merged; `lane-z-14-management-map`
   explicitly abandoned in section 3. DONE
2. **Full suite once on the merged result** — conductor run `34935949858` on `5bbc3be6`, read from
   Actions. **NFR-1 / AN1-6 honoured: the integrator ran NO local suite at any point tonight** —
   every verdict in this packet comes from the conductor and the receipts. DONE
3. **`git worktree list` == primary only** — DONE. `git ls-remote --heads origin` carries only
   `main` and the permanently-protected `automation/fleet-audit`; two merged branches
   (`worktree-dispatch-z-manifest`, `claude/lane-z-11-three-repo-comparison`) were found alive on
   origin **at close, after a commit body had already claimed teardown was complete**, verified
   `--is-ancestor` and deleted. **One empty, OS-locked husk directory survives** for lane z-4:
   deregistered from git, branch deleted in both places, three teardown attempts recorded FAILED
   rather than reported done. PARTIAL
4. **Manifest and packet archived, two halves** — manifest at `8d029783`; this file is the second
   half. DONE
5. **`git stash list` empty** — DONE

## 8 · What the next batch inherits

- **`[#763]` re-measures this freeze — by node id, never by count**, and now also owns the
  space-in-parametrized-id defect that breaks that very comparison (section 2, defect three). Its
  recorded discrepancy verdict: the ordering cited two causes as known, a missing optional
  dependency (~17) and module-shadowing (~5), and **both are absent from the conductor
  measurement** (0 matches for `ModuleNotFoundError` / `ImportError` / `No module named`). If those
  figures were real they came from a local Windows run — a different baseline on a different
  substrate, and not this one.
- **intake 99** (all-digit SHA) and **intake 100** (floor-repin precedent) are CANDIDATES awaiting
  ratification. **Intake 100 blocks a clean close**: five failures sit outside the frozen 51 and
  will still sit there tomorrow.
- **`[#765]` stays OPEN** — the organ landed; its Done-when did not.
- **`[#772]`** is P1 with a blast radius outside this repo: every dispatched lane inherits the whole
  secret environment. Its packet says it worsens while it sits.
- **`[#781]`** stays open for lane z-14, which never arrived.
- **Teardown is the batch's real cost centre** (section 3): 7 failed attempts, 4 of 6 receipts
  spoiled, the median starved to n=3. Worth a row before the next batch, not after.
- **The batch manifest carries no frontmatter**, so `batch_manifest.open_batches()` returned `[]`
  all night and the **ADR-110 declared-integration-arc exemption never fired once**. It fails
  closed, so it cost nothing visible — the batch simply ran its whole queue believing it had a
  mechanism it did not. The fix belongs in the NEXT manifest; this one is immutable.
- **Two organs disagree about `logs/<month>/`, and the disagreement makes one of them uncommittable.**
  Found at close, by walking into it. The `logs_retention` organ relocates dated log artifacts into a
  month bucket **automatically, at SessionStart** — it moved `PROVIDER-CENSUS-2026-09-15.json` and
  `PROVIDER-TRAPS-2026-09-15.json` into `logs/2026-09/` without being asked. `validate-hermetization`
  then **refuses that very path**: *"`logs/2026-09/` is not an admissible home for a new file … a
  genuinely new one is an operator decision recorded as a ruling, not a drive-by add."*
  `graph-task-coverage` refuses the same two files for a second, independent reason (no OPEN row
  claims them). **So an organ performs a move that no one can then commit** — the tree is left dirty
  by design, the session-end backpressure hook reports it as the operator's mess, and the only
  landing paths are `--no-verify` (prohibited) or an operator ruling admitting the home. Neither
  organ is wrong on its own terms; they have simply never been run against each other. The
  relocation was **reverted rather than forced** in this arc. This needs a ruling, not a patch:
  either `logs/<month>/` joins the admissible homes, or retention stops moving tracked files.
- **Never allocate an id from the integrator seat while lanes run.** Three collisions, one cause.
