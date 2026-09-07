# Erratum — the AJ second pass's 6.4× / 16.2× headline

<!-- scope: meta · class: technical · drafted by: filings-N2, 2026-09-06 NIGHT-2 batch ·
     landed and independently re-verified by: lane-u-000-erratum-aj-second-pass (batch U, W2-F5), 2026-09-07 ·
     commissioned by: DECLARE-F-2026-09-06 F-5 · subject: docs/audits/2026-09-05-technical-research-aj-second-pass.md:107
     THIS FILE DOES NOT EDIT THAT AUDIT. Audits are immutable (CLAUDE.md §5 rule 3); an erratum is a
     new dated artifact that supersedes a claim, which is the form DECLARE-F F-5 specifies. -->

**Subject claim**, `docs/audits/2026-09-05-technical-research-aj-second-pass.md:107`:

> **The headline: 6.4× the wall-clock and 16.2× the cost, for the same verdict on the same task.**

## 0 · Landing note — provenance, and what this seat checked itself

This erratum was **drafted by `filings-N2`** on 2026-09-06 and carried in the transport; the seat
that wrote it went offline before it could land. The landing seat did **not** redraft it, because a
seat reading only the commission would have reached a thinner result: the draft's §2 corrections were
found by reading the operator's disk, which the commission does not ask for and a later seat would
not have thought to do.

**What the landing seat re-verified independently, at `c371b856`, before landing** — every figure
below was re-read from its source file rather than accepted from the draft:

- The five `*.timing.txt` files: `WALL_CLOCK_SECONDS` = 1225 / 523 / 116 / 2751 / 7809. **All five
  match the draft exactly.**
- The five result JSONs: `total_cost_usd` = 3.001441 / 2.110091 / 0.512956 / 21.8585621 / 48.531487.
  **All five match**, to one added digit of precision (the draft printed the init cost as
  `21.858562`; the file carries `21.8585621`. The rounding is immaterial and the published `$21.86`
  is right).
- The four ratios, recomputed from those primitives: 16.169× · 6.375× · 24.326× · 9.142×. **Reproduce.**
- The subject headline **is** at line 107 of the named audit, quoted correctly.
- `git ls-files | grep -icE 'FR2|legM|legD'` → **0**, re-measured at `c371b856` (the draft measured 0
  at `498064c9`; the finding survives four days of merges).
- The off-tree directory holds **89 files**, as the draft states.

**One finding the draft understates, added here by the landing seat.** The draft corrects the init
*footnote* (m1's `≈ 732 s`) and notes that the *cost* row omits setup. Both hold. But the audit says
something stronger and separately wrong at **line 231**:

> | Leg M init (the run that counts) | **not exposed** — its wrapper was OOM-killed, so no JSON was written. ≈732 s derived from artifact mtimes. **No dollar figure is estimated** |

`FR2-legM-01-init.json` **exists**, and carries `total_cost_usd: 21.8585621` and `num_turns: 60`.
So the defect is not only that a number is wrong by 3.76×; it is that **the audit reports the
evidence as absent when it is present.** The two errors have different repairs — a wrong number is
corrected, but a wrong claim about what evidence exists misdirects the next reader away from the
file that would have settled it. That is why it is called out separately rather than folded into §2.

The landing seat records **no disagreement** with any finding in §1–§6 below.

## Verdict — three parts, and the middle one is not what was expected

1. **The headline is arithmetically CORRECT for the scope it names.** Re-derived from the CLI's own
   JSON: cost `48.531487 / 3.001441 = 16.169×`; wall-clock `7809 / 1225 = 6.375×`. Rounded, 16.2×
   and 6.4×. Nothing in the ratio is wrong.
2. **The scope it names is not the whole run, and the audit's own footnote for the missing part is
   wrong by 3.76×.** Corrected below. Counting the setup the comparison required, the ratio is
   **24.3× the cost and 9.1× the wall-clock** — the published headline **understates** leg M by
   **$24.48**.
3. **The evidence is NOT in the commit tree — and it is not gone.** 89 files survive off-tree. The
   integrator's HIGH and the memo's ES-03 are both correct that nothing is in git; both correctly
   stopped there, because neither seat had disk access. This seat did.
   **But read §4 before quoting any number above.** The reproduction is *verified by a seat with
   disk access and unreproducible from the repository* — the corrections in part 2 are exactly as
   uncheckable by a later reader as the original headline was.

## 1 · What the claim rests on

**Zero of the arc's evidence files are tracked.** `git ls-files | grep -i 'FR2\|legM\|legD'` returns
**0**, re-measured at `c371b856`. That is the whole of the in-tree finding, and it is what
`docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md` §4.3 (ES-03)
and the integrator's HIGH both record.

**The surviving evidence is on the operator's disk**, where §4.3 predicted it would be —
`C:\Users\1028120\Downloads\aj-scratch\second-pass-evidence\`, **89 files** (§4.3 said 64; the
directory has grown or was counted differently — the discrepancy is noted, not explained). It is
outside the repo, outside any backup this repo controls, and outside every gate. Both legs' result
JSONs, both `WALL_CLOCK_SECONDS` timing files, both suite-AFTER captures and both terra reviews are
there.

## 2 · The measurement, re-run

Every number below is read from a file in that directory. Nothing is estimated or re-modelled.

```
invocation                            wall-clock s    total_cost_usd   turns   exit
FR2-legD-01-lane                              1225        3.001441       51    0
FR2-legM-01-init-ATTEMPT1-429                  523        2.110091       24    1   (429, failed)
FR2-legM-01-init-ATTEMPT2-refused              116        0.512956        2    0   (refused)
FR2-legM-01-init                              2751       21.8585621      60    0
FR2-legM-02-development                       7809       48.531487      123    0
```

**The correction.** The audit's m1 row carries the setup as a parenthetical: *"(+ `/maister:init`
≈ 732 s beforehand)"*. The init that preceded the run that counts took **2751 s** —
`FR2-legM-01-init.timing.txt`, `WALL_CLOCK_SECONDS=2751`. The published figure is low by a factor
of **3.76**. The cost row (m10) carries no setup figure at all: **$21.86 of the run's spend appears
in no cell of the comparison table** — and, per §0, the audit states that figure was never captured,
when in fact it was.

**Both framings, so the reader picks the scope rather than inheriting one:**

```
                      leg M        leg D     ratio
development only     $48.53        $3.00     16.2x     <- the published headline
                      7809 s       1225 s     6.4x
all invocations      $73.01        $3.00     24.3x
                     11199 s       1225 s     9.1x
```

**Which is right depends on a question the audit did not ask:** is `/maister:init` a one-time
per-repo setup, amortised across every later task, or part of the cost of this task? The first is a
defensible reading — and it is *not* the reading the audit took, because m1 adds init to wall-clock
while m10 omits it from cost. **The asymmetry is the defect, not the choice.** A comparison must
apply one scope to both rows.

## 3 · An anomaly this seat could not resolve — stated, not explained

The recorded epochs of the init and the development run **overlap by 1971 s**:

```
FR2-legM-01-init          START 1788628655 (19:17:36)   END 1788631406 (20:03:26)
FR2-legM-02-development   START 1788629435 (19:30:36)   END 1788637244 (21:40:45)
```

Development starts ~33 minutes before init's timer stops. This seat does not know the cause — a
timer wrapping a process that outlived its useful work is one explanation, a genuinely concurrent
setup is another, and they have different consequences for the wall-clock figure. **This is where
the evidence stops.** It does not disturb the leg M / leg D comparison: those two are cleanly
sequential (`M dev` ends 21:40:45; `D` starts 21:46:58), which is the audit's own sequencing claim
and it holds.

## 4 · The status of this reproduction — and it is NOT "verified" without qualification

**State this before the numbers are quoted anywhere.** Every figure in §2 was read from a file that
is **not in the repository, not citable by the browser seat, not reachable by any cloud seat, and
not durable.** `C:\Users\1028120\Downloads\aj-scratch\second-pass-evidence\` is one directory on one
operator's disk, protected by no gate and no backup this repo controls.

So the honest status of the headline is not *verified*. It is:

> **verified by a seat with disk access — and unreproducible from the repository.**

That distinction is the whole point of the finding rather than a hedge on it. A later reader of this
erratum — the browser, a cloud lane, a consumer repo, this repo six months from now — **cannot check
the strongest claim it makes.** The corrections in §2 are exactly as checkable as the original
headline was, which is to say not at all. The erratum has moved the claim from *uncheckable and
possibly wrong* to *uncheckable and probably right*, which is an improvement in confidence and **no
improvement at all in reproducibility.**

**What would make it reproducible** — the commission's third element, answered concretely:

1. **Land the 89 files under a tracked sibling directory.** The shape already exists in-tree:
   `docs/audits/2026-09-05-technical-627-readjudication-artifacts/` is a tracked artifacts directory
   beside its audit. The parallel path is
   `docs/audits/2026-09-05-technical-research-aj-second-pass-artifacts/`. The two result JSONs and
   the five `*.timing.txt` files alone (7 files, small) would make every number in §2 checkable by
   anyone with the repo — **the full 89 are not required for reproducibility.**
2. **Then re-derive from the tracked copies**, and this erratum becomes checkable rather than
   trusted.
3. **Restate the comparison under ONE scope**, applied to both the clock row and the cost row.

**This is RELOCATE-PROPOSED, not an act.** C-8 bars this seat from moving operator files, the
directory is large and unreviewed, and the nine consumer repos are read-only tonight. The operator
rules it. **Until he does, every citation of the 24.3× figure should carry the qualifier above** —
including the ones in `RATIFICATION-2026-09-07.md` §5.3 and in this seat's STATUS board, which do.

## 5 · What would verify the headline — the check that was run

The check itself: both result JSONs read for `total_cost_usd` and `num_turns`, both
`*.timing.txt` files read for `WALL_CLOCK_SECONDS`, and the four ratios recomputed from those
primitives rather than from any figure the audit published. The published ratios reproduce; the
init footnote does not. §4 states what that reproduction is and is not worth.

**Re-run by the landing seat**, independently, on 2026-09-07 — same primitives, same four ratios,
same result (§0). Two seats have now reproduced §2 from the files; neither reproduction is checkable
from the repository, and a second agreeing seat does not change that. **Reproducibility is a property
of the evidence's location, not of the number of seats that have read it.**

## 6 · What this erratum does NOT do

- It does not edit `2026-09-05-technical-research-aj-second-pass.md`. That audit is immutable.
- It does not retract the headline. The headline is correct as scoped; it is **incomplete**, and one
  of its two footnotes is wrong — in both its number and its claim that the evidence was never
  captured (§0).
- It does not disturb `DECLARE-F`'s §0 rulings. §4.3 already recorded that the headline is **not
  load-bearing** anywhere in the deployment-model memo, which rests entirely on in-tree locators.
  **Nothing in DECLARE-F changes because of this erratum**, and F-5's ACCEPT of the AJ second-pass
  intake stands: the deliverable exists, is consumed, and now verifies.
- It reads only §0.1–0.5 and §4.3 of the thesis memo. DECLARE-F reserves §1–§4 for a later
  deliberate browser read; §4.3 was opened because it is the commissioned subject, and **no new row
  is born from it here**.
- It does not claim the headline is now *verified* without qualification, and §4 exists to stop that
  reading. The evidence remains off-tree and ungated; **relocating it is proposed, not done.**

## 7 · The intake this discharges — cited by path, deliberately

**Consumer:** intake #70 — `docs/intake/2026-09-05-tech-aj-second-pass.md` — under ruling F-5 of
`DECLARE-F-2026-09-06.md`. That intake is this erratum's governance surface: it is moved to
`status: ACCEPTED` in the same commit, and its `consumers:` key names this file back.

The commissioning intake is **`docs/intake/2026-09-05-tech-aj-second-pass.md`**, moved to
`status: ACCEPTED` in the same commit as this erratum.

**Why the id appears here and the path everywhere else.** The line above carries `#70` because the
`consumer_at_landing` gate requires an id-shaped token and will not accept a bare path — an
artifact landing after 2026-08-27 must name a `[#id]` row, an `ADR-<n>`, a `STANDING_RULINGS`
section or an `intake #<n>`. Writing `#70` is safe **only because** W1-5's D8 renumbering has
already landed (verified below); before `948911cd` the same token would have been ambiguous. The
substantive citation stays the path, for the reason in the next paragraph.

**It is cited by path and not by id on purpose.** `intake-id: 70` was allocated twice in the live
tree. W1-5 resolved the collision under ruling D8 (`DECLARE-SITTING-2026-09-06.md`) — verified on
`origin/main` by the landing seat at `948911cd`, an ancestor of `c371b856`:

```
KEPT   70 -> docs/intake/2026-09-05-tech-aj-second-pass.md
MOVED  70 -> 77  docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md
```

So `#70` now resolves unambiguously. The path is used anyway, because **any citation of this arc
written before `948911cd` points at the wrong document**, and a reader cannot tell from the id alone
which side of the renumbering it was written on. A path cannot go ambiguous that way.

**Both halves of F-5's ruling, stated together:** the intake is ACCEPTED because *its deliverable
exists and is consumed by the memo* — **and** an erratum was owed on its headline because *the
evidence is not in the tree*. This file is that erratum. The acceptance is not a clean bill: the
deliverable stands, and its headline needs the qualifier in §4 every time it is quoted.

**Before → after:** `6.4x/16.2x headline: unverifiable in-tree (0 arc evidence files tracked, re-measured at c371b856) -> reproduced off-tree by two seats (NOT reproducible from the repo), init footnote corrected 732 s -> 2751 s, the "no JSON was written" claim at :231 refuted ($21.86 / 60 turns captured), all-in ratio stated (24.3x cost / 9.1x clock), 7 files named as the minimum relocation that would make it checkable; intake docs/intake/2026-09-05-tech-aj-second-pass.md DRAFT -> ACCEPTED`.
