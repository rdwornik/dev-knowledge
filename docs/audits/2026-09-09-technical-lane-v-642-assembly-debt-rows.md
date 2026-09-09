# LANE v-642 assembly-debt-rows — end-of-lane artifact

**Consumers:** `[#642]` — the row this lane discharges; secondarily `[#640]` (its A.1 half),
`[#639]` and `[#605]` (the two items that resolved into existing rows instead of new ones).

<!-- Batch V, lane V-4. Frozen contract:
     `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-642-assembly-debt-rows.md`
     Branch `worktree-lane-v-642-assembly-debt-rows`, base `main` @ 40d40a2f.
     Commit-and-STOP: nothing here was merged, pushed, or journaled. -->

## Step 1 — the hold, discharged

The contract dispatched this lane **HELD**: *"HELD until `DECLARE-SITTING-2026-09-08` lands on
the transport. Sitting 1 fixes the `[#642]` items' final owners, and a row filed against a
guessed owner is the debt this row exists to end."*

`H:\...\to-cc\DECLARE-SITTING-2026-09-08.md` is present, **6,561 B**, and it is a real sitting:
eleven rulings in a table, a three-item ratification list, and a closing paragraph headed *"What
V-4 files, now released"*. The bytes were checked, not the directory listing — a Drive file is
visible before its bytes land. Hold discharged; no row here is filed against a guess.

## Step 2 — the three budgeted forks, and no fourth

The contract budgets exactly three decisions and makes a fourth a STOP. All three were taken and
none was escalated; the classes that would have escalated (curated-baseline touches, rule-versus-
ruling conflicts, fork classes with no standing ruling) did not arise.

| Fork | Decision | Ground |
|---|---|---|
| Row placement under themes | 20 rows placed across seven existing stories by subject; no new theme or story | `gen_task_tree` derives theme/story from manifest NODE POSITION, so each node was inserted as the last task of its intended story and the derived frontmatter was read back to confirm |
| PLAYBOOK section placement | Appended at end of file, unnumbered | The contract says APPENDED; two unnumbered sections already sit after the appendices. A numbered §22 between §21 and Appendix A is an insertion, not an append |
| Carrier value where Q-R2 is ambiguous | See the step-6 table — the two genuinely ambiguous values are the DAY and CLOSE batch contracts | R-P1 maps `BATCH-` to "their batch manifest on main"; neither of those two batches ever had one |

## Step 3 — the rows · Done-contract clause 2: **N = 11 → 0**

**N is the count of items in `DECLARE-REVIEWS-2026-09-07` plus `REVIEW-2026-09-08-plan-redteam-
followup` that had no owning row when this lane booted.** Enumerated rather than asserted:

| # | Unrowed item at boot | Source | Now owned by |
|---|---|---|---|
| 1 | R-2 · the 2026-08-29 deploy freeze, unasked for ten days | DECLARE-REVIEWS §B | `[#644]` |
| 2 | R-3 · `INSTALL.md` circular (carrier writes it, seal refuses it) | §B | `[#645]` |
| 3 | R-4 · ceremony ratio, 87 anchors + 145 merges of 407 commits | §B | `[#646]` |
| 4 | R-5 · the contract-corpus half (388 KB of contracts, 1.1 MB corpus) | §B | `[#647]` |
| 5 | R-6 · the six under-mechanised rules | §B | `[#648]` |
| 6 | R-7 · the funnel defect class / `orphan_census` clock | §B | `[#659]` |
| 7 | R-8 · 14 human points, 9 mechanisable | §B | `[#658]` |
| 8 | the harness has no single definition-of-done anywhere | followup §1 | the PLAYBOOK section (step 4) — an artifact, not a row |
| 9 | S-15 · the AJ tools-and-evals table, NEVER WRITTEN | followup §1 | `[#660]` |
| 10 | SDA-1 · a complete benchmark design that never ran | followup §1 | `[#661]` |
| 11 | INBOX-037's render pass has no `docs/intake/` file | followup §3 | `[#654]` |

**N = 11 → 0.**

**Three items in those two documents were NOT rowed, because a row that genuinely owns them
already exists.** The Done-contract's test is *"re-carried by a row that genuinely owns it"*, and
duplicating an owned item would have inflated the count while lowering its meaning:

- §A.1's FPG-1 narrowing → `[#640]`, whose Done-when is that narrowing recorded on a surface a
  lane reads. Step 5 lands its first half.
- R-5's organ-retirement half → `[#639]`, which already carries the DETECTOR/BACKSTOP
  classification and the seed measurement (five organs, zero true positives across T and U).
- Sitting ruling 7's one-flag consumer resolution → `[#605]`, named by the ruling itself.

Also not rowed, and deliberately: §A.3's lane ceiling and §C's six-lane cut are **discharged by
batch V itself**, §A.4's seal sequencing by lane V-3, and R-1 is an operator ratification act
that the contract pins out of this lane.

**Nine further rows** come from the sitting and from the browser's rulings on this batch's own
escalations — inside the contract's step-3 list and the sitting's *"What V-4 files"* paragraph,
outside the two documents N is measured over: `[#649]` ruling 2 · `[#650]` ruling 4 · `[#651]`
ruling 5 · `[#652]` ruling 8a · `[#653]` ruling 10 · `[#655]` `run_retention`'s caller · `[#656]`
the v1.5.0 drift-probe string · `[#657]` orphan #33 · `[#662]` the R6 handoff exception.

**Twenty rows total, `[#644]`–`[#663]`.** Every Done-when is the measured number its source
names. Where a source names a class and no number — §A.1 — no number was invented; see step 5.

## Step 4 — the harness definition · Done-contract clause 1's PLAYBOOK half

`protocols/PLAYBOOK.md` gains **"The harness — definition and closure per release"**, holding
HANDOVER-ARCHITECTURE §0's definition and §3's universalization *"done"* **verbatim**. Verbatim
was machine-checked rather than eyeballed: the appended blockquotes were unwrapped and matched as
substrings of the transport file — **599 chars and 161 chars, both VERBATIM OK**.

**The silent-rule ratchet fired on the paste, and was paid rather than bypassed.** The definition
contains exactly one scored token — *"so the repo is never wrong at rest"* — taking PLAYBOOK
222 → 223 and the corpus to `live 448 > baseline 447`, a hard FAIL on `audit-health`. The token
sits inside an operator-ruled verbatim quotation, so rewording it is the one repair unavailable
here. It was paid for by draining one genuine false positive elsewhere in the same file:

```
before:  it held one dormant entry and never ran on a real cadence
after:   it held one dormant entry and did not run on a real cadence
```

That sentence reports what a retired tech-radar folder did; it binds nobody, so it was never a
rule and the proxy was wrong to count it. Re-measured after the drain: **live 447 ≤ baseline 447**,
detector `silent-rule-v5`, 69 files in scope. `SKIP=audit-health` was available and was **not**
used: it would have left `main` above its own baseline and wedged every subsequent commit.

## Step 5 — intake #40 · Done-contract clause 4: **contradiction present → absent**

`docs/intake/2026-08-22-tech-document-dependency-graph-organ.md:650` before and after:

```
before:  12 separate edge computations -> 0; all organs read FPG-1.
after:   Every CORPUS-STRUCTURE edge computation -> 0; the organs that hold one read FPG-1
         instead. The class is exactly five kinds - citation, generation, template, test,
         script call-site. State gates are excluded and stay gates.
```

All three of §A.1's corrections landed, not just the headline: corpus-structure edges only;
two-tree gates cannot be views (the spine anchor compares spine against working tree, the
staged-ADD checks judge commit-time state); and the blanket `diff = 0` migration bar is withdrawn
for a per-organ contract naming its own proof, because the blanket bar is impossible for
`validate_backlog` **by design**.

**Z-C3 is cited with its scope stated** — the omission §A.1 calls void-making. Z-C3 declined a
graph library **as an organ** (ADR-105 §2 bars activation while no cycle/SCC consumer exists) and
R-A had already closed the library question; `rustworkx` is already declared and in-tree, so the
ruling uses what is declared and adds nothing.

**N was NOT replaced with a smaller integer.** 12 counted every edge computation in the tree,
state gates included, so it is not this Done-when's number — and §A.1 names a class, not a count.
Writing any replacement integer would repeat the defect the amendment repairs. The first
migration lane re-measures N under the five-kind class. This is the contract's *"the measured
number its source names, or STOP"* applied where the source names none.

## Step 6 — carriers · Done-contract clause 3: **P11 recipe short 7 → 0**

The pinned seven are the set `HANDOFF-VERIFY-2026-09-08-architect-2` measured: **25 decision
files, 18 resolve, 7 short — 2 with no flush-left key, 5 `OPEN` and unnamed in the residual.**

| File | Carrier now | Ground |
|---|---|---|
| `DECLARE-BOOT-REVIEW-2026-09-08` | `protocols/HANDOFF_PROCESS.md` | R-P1: its product is the 7.1.0 declaration. Its HTML comment stated a carrier where P11's anchored key cannot see it; the comment is left untouched |
| `AMEND-037-001` | `BACKLOG.md` — `[#654]` | R-P1 wanted the 037 intake filed first; `docs/intake/` is outside the footprint, so `[#654]` owns filing it and the value takes the intake path when it lands |
| `DECLARE-REVIEWS-2026-09-07` | `BACKLOG.md` — the seven §B rows | R-P1: "the rows lane V-4 files for them" |
| `DECLARE-R6-HANDOFF-EXCEPTION` | `BACKLOG.md` — `[#662]` | R-P1, same clause |
| `BATCH-2026-09-06-DAY-CONTRACTS` | `BACKLOG.md` — `[#610]` | Sitting ruling 1: the DAY window never had a manifest, was never OPEN under AMEND-BATCH-V-002 §5a, and its lane count is history for `[#610]` |
| `BATCH-2026-09-06-NIGHT-2-CONTRACTS` | `docs/audits/2026-09-06-technical-batch-u-manifest.md` | NIGHT-2 **is** batch U — verified, not assumed: `batch: U` / `dispatched: 2026-09-06` in that manifest's frontmatter, and its close packet opens *"Batch U close packet — the 2026-09-06 NIGHT-2 batch"* |
| `BATCH-2026-09-07-CLOSE-CONTRACTS` | `JOURNAL.md` | The 2026-09-08 (d) entry is this batch's only landed record; no manifest and no close packet was ever cut for the CLOSE window |
| `HANDOVER-ARCHITECTURE-2026-09-08` | `protocols/PLAYBOOK.md` | R-P6 names the new section as this file's home and resolves its `OPEN` carrier to it |

**Re-run of the recipe, after the writes.** Leg 1, `head -6 "$f" | grep -m1 -E '^carried-by:'`
over the live `to-cc/` decision set: **47 files, 0 with no flush-left key.** Leg 2, each value's
carrier resolved against `git ls-tree -r --name-only main`: **44 resolve, 3 literal `OPEN`, 0
short.** The pinned seven are all in the resolving set — **7 → 0**.

**The three remaining `OPEN`s are not part of the seven and are not this lane's to close:**
`DECLARE-DISPATCH-SEAM-AND-ENTERPRISE-2026-09-08`, `DECLARE-HARNESS-IS-PROCESS-2026-09-08` and
`DECLARE-HARNESS-PROVENANCE-2026-09-08`. All three were written after the measurement that pinned
the seven, all three are correctly-`OPEN` by their own text, and P11 discharges an `OPEN` by the
next bundle's residual naming it. **That naming is owed at the next handoff cut**, and it is
recorded here so it is not discovered after the cut for a third consecutive bundle — which is
exactly the defect `[#643]` exists for.

**A measurement caveat, stated so nobody re-derives it wrongly.** A first-token reading of the
carrier value under-counts: `DECLARE-F-2-2026-09-07` and `DECLARE-SITTING-2026-09-06` open their
values with prose (*"all eight sB rows resolve…"*, *"per-row, because this file is 15 rulings…"*)
and carry their resolving paths further in. Both PASS — the seat's own measurement lists them
among the 18 — and both are counted as resolving above. The leg ORDER is load-bearing and the
value's SHAPE is not uniform; a probe that reads only the first token will report a false 2.

## Ratification-list condition, checked because the sitting asked CC to check it

The sitting ratifies `#86` (`orphan_census`) *"one condition: CC confirms the intake names the
census's trigger."* Checked, and the answer is **half**: the intake does name triggers — *"Runs in
the nightly Routine and at ship-gate"* — and the ship-gate leg is real, but the process census
proves the repo declares no schedule of any kind, so the nightly Routine is a plan written as a
fact. Filed as `[#659]` rather than answered here, because the ratification is the operator's.

## Verification

**Targeted set** — the modules covering this lane's diff (`BACKLOG.md`, `tasks/`,
`protocols/PLAYBOOK.md`, `docs/intake/`):

```
uv run --locked pytest -q tests/test_backlog_source.py tests/test_export_backlog_view.py
  tests/test_gen_intake_index.py tests/test_gen_intake_tree.py tests/test_gen_task_tree.py
  tests/test_silent_rule_ratchet.py tests/test_task_tree_gate.py tests/test_toc.py
  tests/test_validate_backlog.py tests/test_validate_backlog_twin_parity.py
  tests/test_validate_doc_rot.py
-> 3 failed, 415 passed in 45.79s
```

| Failure | Attribution |
|---|---|
| `test_gen_task_tree.py::test_the_live_view_is_under_the_589_done_when_byte_bar` | **THIS LANE'S** — see the deviation below |
| `test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers` | **Pre-existing.** Named in `to-cc/SUITE-BASELINE-CODESPACES-2026-09-08.log` line 1224 |
| `test_toc.py::test_corpus_fence_fix_never_drops_a_header_from_OUTSIDE_a_code_block` | **Structural to any worktree, content-independent.** Its `_SKIP_PARTS` contains the bare name `worktrees`, and a lane tree lives under `.claude/worktrees/<lane>/`, so `worktrees` is a part of the root itself. Measured here: `rglob("*.md")` returns **2,603** files and the skip filter keeps **0**. No edit in this lane could cause or clear it |

Other gates: `validate_backlog` OK (9 themes, 26 stories, 251 tasks, 2 pre-existing warnings) ·
`validate_doc_rot` no new locus, `backlog-row-length` trend **+0 (78 → 78)**, no new accretion ·
`audit.py health` **OK** · `toc.cli check protocols/PLAYBOOK.md` fresh · `git stash list` empty ·
working tree clean at STOP.

## Deviations, disclosed rather than absorbed

**1 · The `[#589]` byte bar is breached, and this lane did not clear it.** `BACKLOG.md` went
**71,911 → 75,367 B** against a **72,000 B** bar — 89 B of headroom before, 20 rows at a mean
173 B. The bar is `[#589]`'s own Done-when and its docstring names the two lawful answers: groom
first, or re-baseline deliberately on the architect's ruling. Neither was taken. Grooming is a
closure act and closures are the operator's (`/review-closures`); raising the bar to fit the first
rows that ever hit it is precisely the act `[#589]` exists to forbid. **The arithmetic says no
trim recovers 3,367 B**, so this is not effort, it is a decision — and it is the operator's.
The row-level ceiling that gates every commit (`_VIEW_ROW_BYTE_CEILING`, 400 B) and the 100,000 B
per-commit gate are both respected; only the point-in-time total bar is over.

**2 · Sitting ruling 4 assigns the ADR-117 status flip to V-4, and this lane rowed it instead.**
`docs/decisions/` is outside the frozen footprint, and a status flip re-derives the ADR index and
`.claude/generated/recent-adrs.md` — coupled regeneration the same contract pins to the
integrator. `[#650]` carries the flip with its coupled surfaces named.

**3 · R-P1 would have had this lane file the 037 intake before citing it.** `docs/intake/` is
outside the footprint for anything but intake #40, and an intake add drives two generators.
`[#654]` carries the filing; `AMEND-037-001`'s carrier moves to the intake path when it lands.

**4 · One word of `protocols/PLAYBOOK.md` outside the new section.** The false-positive drain in
step 4. The contract pins out PLAYBOOK **Ch8** by name and states no other lane writes PLAYBOOK,
so it conflicts with nothing; it is reported because the alternative cost the integrator more.

**5 · The PLAYBOOK "Last updated" stamp was NOT moved.** Moving it claims an end-to-end re-read of
6,329 lines this lane did not perform. `canonical_freshness` reports the file **ungated** on the
derived leg, so nothing is evaded by leaving it.

## What this lane did NOT do, by contract

SDA-1 was **not run** and S-15 was **not written** — both rowed (`[#661]`, `[#660]`), as the
contract's *"What NOT to do"* requires. No JOURNAL entry. No index regeneration. No merge, no
push, no branch but its own. `docs/audits/README.md` is left **stale on purpose** — the
`audit-index-freshness` hook was narrowed by `[#590]` precisely so a lane does not touch it, and
the integrator regenerates once on the merged result.

## Owed by the integrator

1. Regenerate `docs/audits/README.md` and `ecosystem/doc-counts.md` on the merged result.
2. Decide the `[#589]` byte bar — groom or a ruled re-baseline. Until then the suite carries one
   named RED whose cause is this lane's twenty rows.
3. Carry the three still-`OPEN` transport carriers into the next bundle's residual by name.

## Commits

| SHA | Step |
|---|---|
| `ff798a1a` | 3 — twenty rows, `BACKLOG.md` + `tasks/` regenerated from source |
| `b3adbb5e` | 4 — the PLAYBOOK harness section, pasted verbatim, ratchet paid |
| `ff103444` | 5 — intake #40 narrowed to corpus-structure edges, citing Z-C3 |
