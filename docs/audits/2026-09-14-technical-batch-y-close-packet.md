# Batch Y close packet — technical

> **Written by the integrator seat at batch close, 2026-09-14.** Six lanes dispatched, five merged,
> one NOT RUN by its own frozen shape. Every count below names the instrument that produced it.

## Instrument discipline

**No number in this packet came from a recursive sweep.** `grep -r` from the primary descends into
every live lane worktree — measured at **5.0x** duplication with four lanes live during this batch —
and it also reads untracked `.venv/` code. Where a sweep was the only available shape, `git grep`
(index-based) was used and is named as such. Counts read from a single file, or from `tasks/` via a
generator, are not worktree-sensitive; only sweeps are.

**A count taken during a batch is not comparable with one taken outside it.** Every figure here was
taken at `ef1a91cb` with all five lane worktrees already torn down, except where stated.

## The seven numbers

### 1. Median merge minutes — 12.4 min, n=1, target 3.6 MET

```
median   12.4 min   (target 3.6: under 30 -> MET)
range    12.4 .. 12.4
n        1 complete, closed kind=merge receipt
```

Instrument: `merge_receipt.py median`. **n=1 is a small sample and this is what that one merge cost,
not an estimate of what a merge costs.** The tool says so itself and the packet does not launder it.

**Four `kind=merge` receipts were EXCLUDED, and only one exclusion is structural:**

- `merge-y-750` — missing `handback`, `merge`, `suite`, `teardown`. **Integrator error:** the Actions
  verdict was recorded under the default `actions` step instead of `--step suite`, and handback and
  merge were never timed.
- `merge-y-751` (the real merge, `b864e7d0`) — three failed non-suite steps. **Integrator error:**
  two malformed `time` invocations (`--step-class` where the option is `--class`; under click's
  `ignore_unknown_options` + `UNPROCESSED` the typo became the program name), plus a first teardown
  attempt that died on the husk described in `[#762]`.
- `merge-y-751` (the superseded held attempt) — correctly excluded, it carries no merge.
- `merge-y-754` — missing `teardown` ONLY. **The one structural exclusion:** `teardown` is in
  `REQUIRED_STEPS` but was sequenced as a batch-close act, and a CLOSED receipt cannot be amended
  because `logs/MERGE-RECEIPTS.jsonl` is append-only (ADR-29/39 class).

**The bar was reachable and the batch mostly missed it by my hand, not the tool's.** A belief carried
into this batch — that completeness is unreachable while `main`'s suite is PRE-EXISTING red — is
**RETRACTED**: the predicate excludes the `suite` step from its failed-steps check and judges that
leg on the verdict STATE per ruling AY1-1. That was true before `[#750]` landed `02bdbff3` and has
not been true since.

**What made `merge-y-752` complete was ORDER:** handback → merge → **teardown recorded inside the
still-open receipt** → suite → close. A teardown run after the receipt closes cannot retro-complete
it.

**Against the frozen 2026-09-12 baseline** (84 min wall = 11.3 targeted tests + 72.7 residual
ceremony): the baseline's own two itemised views read ~90 and ~63 min, disagreeing with each other
and with the 84 min wall figure, and **nothing was measured on the day it was frozen.** Any
improvement stated against it inherits that uncertainty, so none is claimed here.

### 2. Cost per lane and per model — USD 159.87 over five lanes

Instrument: `lane_cost.py close` per lane, then `lane_cost.py report`. **Every figure was RE-DERIVED
after `b864e7d0`**; nothing is carried from before that merge.

```
lane-y-750-merge-receipts       USD 49.59   322 calls    78,140,567 tokens
lane-y-751-cost-in-money        USD 40.29   249 calls    60,869,389 tokens
lane-y-752-declared-model-runs  USD 35.93   242 calls    55,774,785 tokens
lane-y-755-docs-cut-finish      USD 19.57   124 calls    26,398,565 tokens
lane-y-754-backlog-to-bar       USD 14.48   127 calls    21,717,653 tokens
                                ---------  ----------   -----------
per batch   Y                   USD 159.87
per model   claude-opus-5       USD 159.87  1,064 calls 242,900,959 tokens   (rates as_of 2026-06-24)
```

**One model only.** Every lane ran `claude-opus-5`; there is no second row to compare against, which
is exactly the gap `[#753]` exists to close and which this batch did not run.

**EXCLUDES the integrator seat's own spend.** The integrator works in the primary checkout, whose
session-store directory holds every primary-checkout session rather than this seat's alone, so
attributing it to batch Y would over-count. It is not estimated here.

**Why re-derivation was required, stated narrowly.** The pre-fix `lane_cost` carried three CRITICALs.
**None of them had fired** — the ledger held exactly one row, correctly keyed and correctly priced,
the full slug matched exactly one directory, and no short slug was ever run. The defects were
**LATENT**. The reason to re-derive is that the surviving figure was **STALE**: measured mid-lane and
a floor by construction (`$18.82` at 128 calls against `$40.29` at 249 by the lane's end).

**The append-only fix is demonstrated live in the ledger.** `logs/LANE-COSTS.jsonl` holds **6 lines**
including the superseded `$18.82` row — not one byte was rewritten — while the aggregate reads
**n=5** by last-wins-per-slug. Under the pre-fix reader the same file would have totalled `$178.69`.

### 3. BACKLOG bytes against the 72,000 bar — 94,255 B, OVER by 22,255; over-ceiling rows: 0

Instrument: byte length of `BACKLOG.md`; rows via `gen_task_tree.task_row_lines`.

```
BACKLOG.md                       94,255 B
[#589] test bar (test_gen_task_tree.py:1187, assert < 72_000)   OVER by 22,255
generator ceiling (_VIEW_BYTE_CEILING = 100,000)                UNDER
row lines                        332
over _VIEW_ROW_BYTE_CEILING (400 B, on task_row_lines)          0
longest row                      301 B
```

**The view PASSES its generator and FAILS its test** — a 28 kB disagreement between two bounds on one
file. **The over-ceiling row count is ZERO, not 33.** An earlier integrator figure of 33 was produced
by `splitlines()` over the whole file rather than `task_row_lines`, contradicted lane `[#754]` with a
worse instrument, and is **RETRACTED**.

**The bar itself is REFUTED rather than missed, per operator ruling, and is not acted on here.** Row
`[#754]` carries the refutation and stays OPEN: the two ceilings measure disjoint corpora in
disjoint units (`_VIEW_ROW_BYTE_CEILING` = bytes on a one-line view projection;
`validate_doc_rot._BACKLOG_ROW_CEILING` = 1320 CHARACTERS on reassembled `tasks/` bodies), the
per-row tripwire is confirmed untouched, and what has decayed is the 1320's declared ROLE — measured
at 148 of 322 rows over it, p50 1302, **the median having crossed its own ceiling**, which is the
percentile state its amendment abolished. The drain is exhausted: the `archive_row_body` trigger over
60 rows moved the count 148 → 148 and `BACKLOG.md` 91,514 B → 91,514 B.

### 4. ARCHITECTURE bytes — 100,845 B

Instrument: `wc -c ARCHITECTURE.md` (single file, not worktree-sensitive).

**Y-6's 15 KB target is NOT met and is NOT reported as met.** By operator ruling it leaves this batch
as an X3 row, **`[#760]`**, carrying lane `[#755]`'s 11-chapter byte measurement as its starting
point. The render premise was refuted three ways: no renderer in `file_purpose_graph.py`, no script
writes `ARCHITECTURE.md`, and `[#664]`'s own body puts step D in wave X3.

### 5. Is `ESSENTIALS.md` gone? — YES, with three named remainders

Instrument: `git ls-files --error-unmatch` plus a filesystem check; references via `git grep`.

`protocols/ESSENTIALS.md` is absent from the index and from disk, deleted at `e791cffc`.

- **6 stale `doc_shapes:` keys**, one each in `deploy/manifest-v1.1.0.yaml` through `v1.5.0.yaml`
  (the live one at `:1321`). **INERT to `deploy/tool.py` by that file's own declaration** — *"INERT
  TO deploy/tool.py, exactly as `components:` and `doc_shapes:` are — the tool reads only
  `carriers:`"*. **Zero `carriers:` entries**, verified by locating each reference's enclosing
  top-level section rather than assuming. **No deploy leg is broken.**
- **17 tracked paths still match the NAME**, all a different artifact class: 16 handoff-bundle
  `04_ESSENTIALS.md` section files (May 2026, immutable under critical rule 3) and one test fixture.
- `CLAUDE.md` and `ARCHITECTURE.md` both carry a correct tombstone.

**`[#628]` does NOT close, by operator ruling.** The deletion is discharged; its Done-when also
demands the floor sidecar and every pinned manifest, which is a release act. Recorded as discharged,
row stays OPEN.

### 6. The non-Claude trial score — NOT RUN

**Not an omission.** `[#753]` owns this number and the batch deliberately did not dispatch it. From
the row's own frozen text: the contract is `shape: interactive`, it "must never run unattended", it
is "deliberately not in batch Y's fired set and is launched by the operator when present", it runs in
the PRIMARY checkout the integrator holds for the batch, and it does not open
`ecosystem/provider-registry.yaml` until `[#751]` has landed on `main` — which it now has, so the
sequencing precondition is satisfied for whenever the operator launches it.

Its admission bar, unchanged: **>= 8/10 green on first review**.

### 7. Open-row count — 280

Instrument: `boot_frontier.load_open_rows`, which mirrors `gen_task_tree._cmd_rank`'s read path and
IS the definition of "open". 332 task rows total.

**Do NOT use the boot banner's backlog figure** — it triple-counts DEFER'd rows.

## The merge ledger

```
b779616e   lane y-755 @ 09a5cebd   ESSENTIALS.md deleted, [#628] stays OPEN by ruling
02bdbff3   lane y-750 @ a65f9493   the receipt tool lands with its own false pass closed
2d7cc200   lane y-754 @ b4cdb3e2   the backlog bar is REFUTED, not missed
b864e7d0   lane y-751 @ 211e248a   cost in money; HELD on 3 verified CRITICALs, merged after RED-first fixes
ef1a91cb   lane y-752 @ 1ee32564   ordered/ran model on receipts; merged with NO handback ever received
NOT RUN    lane y-753              interactive shape, operator-launched
```

**Every merge's suite verdict is `PRE-EXISTING`** — COMPLETE with the state named under ruling AY1-1,
and **not a statement that any run was green.** `pytest` is red on `main` and was red at every
baseline; the other four Actions jobs (`ruff`, `terra`, `phase-gate`, `seal`) were green throughout.
Each baseline was DERIVED from the merge's own first parent, never typed.

**`merge_receipt`'s actions reader records a standing gap:** *"this runner has no `index-regen` job,
so index regeneration did NOT run on Actions. Target 3.2 asks for both halves; a green run here
covers the suite only."*

## Rulings recorded this batch

- **B8 (ratified 2026-09-14)** — the JOURNAL anchor rides INSIDE each merge commit, replacing
  one-anchor-per-batch. The reason is a joint unsatisfiability, not a preference: B2
  ("JOURNAL-rides-the-branch") and P-1 ("JOURNAL.md is the integrator's surface") leave the
  lane-merge case with **no sanctioned shape**, and one-anchor-per-batch and one-receipt-per-merge
  cannot both hold — a single end-of-batch push yields ONE Actions run, so every intermediate merge
  reads `NO-RUN` → unreadable → refused. Reconciliation of P-1 and the DEFINITION_OF_DONE wording is
  filed as `[#757]`.
- **AY1-1** — suite state PASS or PRE-EXISTING is COMPLETE with the state named; REGRESSED or
  unreadable is INCOMPLETE and refuses the merge.
- **The two-step merge is mechanically load-bearing, not stylistic.** `git merge --no-ff` runs 2
  hooks; `git merge --no-commit --no-ff` followed by `git commit` runs 31, because git fires
  `pre-merge-commit` (uninstalled here) for a machine-completed merge and `pre-commit` (installed)
  for one finished by `git commit`. Every merge in this batch used the two-step form and every one
  ran the full registry armed.

## Rows filed this batch

`[#757]` reconcile B8 with B2/P-1 · `[#758]` `[#675]` target 3.2 was never satisfiable by this walk ·
`[#759]` `range_is_anchored` vs `unanchored_on_spine` disagree on scope · `[#760]` X3 ARCHITECTURE to
15 KB behind the step-D render · `[#761]` the edge-class census prices its own false positive as
cheap while paying it is a V-2 escalation class · `[#762]` a worktree teardown races the departing
session's Stop hook and the no-leftovers check cannot see what it leaves.

Filing a row is **THREE acts** — the `tasks/` file, a manifest node at the RIGHT section, and the
regen. Four rows were initially filed with two, which emits nothing.

## Remainders carried out of batch Y

1. **`pre-merge-commit` is not armed.** Remediation is TWO lines (`default_install_hook_types` AND
   `default_stages`, pinned `[pre-commit]` at line 17) and affects **28 of 33 hooks** (5 carry
   explicit `stages:`). The two-step merge is a zero-config mitigation and is what B8 rides on.
2. **The integrator seat is the one seat `LANE_BRANCH_RE` can never exempt** — an *inverted* blind
   spot, aimed precisely at the commits carrying the anchoring obligation.
3. **The merge median is structurally capped while `teardown` is in `REQUIRED_STEPS`** — it is a
   batch-close act, so it is only recordable while a receipt is still open.
4. **The receipt sidecar is not gitignored**, so an open receipt reads as a dirty tree and the
   session-end hook orders it committed — which is how transient state reached origin at `2d7cc200`
   and had to be removed at `237526c9`.
5. **`[#751]` ran a 2,253 s full suite on this box** against R-G-A2, invisible to both `lane-ceiling`
   and `concurrent_seats` (which counts lane WORKTREES — *"A COUNT, NOT A LOAD MEASUREMENT"*).
   Correlation with the OOM window is flagged; **causation is not claimed.**
6. **`[#751]`'s declared 2-file vs actual 13-file footprint** weakens every `file-collision` refusal
   the freeze step makes — a PASS means "no DECLARED collision".
7. **`test_seal_repo_profile.py:32-35` overwrites `sys.modules`**, causing an order-dependent failure.
8. **Three false premises in the frozen roster** — mechanism-vs-bar confusions.
9. The five remainders inherited from batch X4.

## What the integrator got wrong, recorded so the next seat inherits the correction

- **"33 BACKLOG rows over the 400 B ceiling" — RETRACTED.** `splitlines()` over the whole file; the
  gate reads `task_row_lines`. True count **0 of 332**. Lane `[#754]` was right.
- **A latent defect reported as realised — RETRACTED by append in JOURNAL entry (k).** Entry (j) and
  `b864e7d0`'s commit message say `[#751]`'s containment defect misattributed this lane's spend. It
  never fired. A reviewer's CRITICAL establishes that a defect EXISTS; whether it FIRED needs
  separate evidence. Writing the stronger claim into an append-only record makes it permanent.
- **A truncated listing faked an absence.** An ESSENTIALS sweep piped through `head -40` filled the
  window with `LESSONS.md`; two files were wrongly cleared, and the review found exactly those two.
- **A stale diff base nearly produced an accusation.** Against the frozen base, lane `[#754]` showed
  `JOURNAL.md +73`; against the real `git merge-base` it touches no JOURNAL. Those lines were the
  integrator's own entry, inherited through a fast-forward sync that leaves no merge commit.
- **`git add -A` committed transient state** to origin at `2d7cc200`, removed at `237526c9`. Every
  merge since stages EXPLICIT paths.
- **Two malformed `merge_receipt.py time` invocations** permanently blocked `merge-y-751` from ever
  being COMPLETE. `rc=None` means nothing ran.
