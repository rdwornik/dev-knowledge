# Lane `lane-y-754-backlog-to-bar` — the trigger run to exhaustion, the groom discharged, and a refused disjunction

**Consumers:** row `[#754]` (filed by this lane and carrying its ruling); the batch Y merge
queue, `docs/audits/2026-09-14-technical-batch-y-manifest.md`, slot 3 of wave 1.
**Lane:** `lane-y-754-backlog-to-bar` · branch `worktree-lane-y-754-backlog-to-bar` ·
contract `docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-754-backlog-to-bar.md`
**Base:** `main` at `8a41c650`, synced forward to `e6acb23e` before the first commit.
**Commits:** `8968da76` (clause 1 + row filed) · `412506fb` (trigger + groom) ·
`e01582b5` (the ruling) · this artifact.

---

## 0 · The headline, stated before the evidence

**Clause 2's first sub-clause is structurally unreachable by the mechanism the contract
names, and the lane proved it rather than arguing it.** Sixty rows were relocated and
`BACKLOG.md` did not move by one byte. The other two sub-clauses — the lapsed groom and the
two-ceiling reconciliation — are delivered in full.

| clause 2 sub-clause | verdict |
|---|---|
| `BACKLOG.md` under 72,000 B | **NOT MET — refuted premise, measured.** See §2. Not deviated: the act named cannot produce the result named. |
| over-ceiling row COUNT falling, ceiling not rising | **NOT MET, and the ceiling did NOT rise.** The drain is exhausted: 148 → 148. See §2. |
| the lapsed groom runs | **MET.** §3. `grooming-cadence` cleared; doc-rot loci 7 → 5. |
| the two ceilings reconciled, ruling recorded | **MET.** §4. The disjunction is refused with reasons; the ruling lands at both declarations and on `[#754]`. |

---

## 1 · Clause 1 (ruling AY1-3) — the trigger IS live, so nothing was wired

The contract's first act was to verify, before touching a row, that
`scripts/archive_row_body.py`'s trigger is live on `main`. Its premise was refuted at
freeze: on 2026-09-13 the graph organ reported zero wiring consumers and the trigger commit
sat on an unmerged branch.

**Measured at this lane's base, on three independent probes:**

1. `.pre-commit-config.yaml:253` carries `row-archive-proof`, entry
   `uv run --locked python scripts/archive_row_body.py verify`. Present in `main`'s **tree**,
   not only in the worktree.
2. The trigger commit `de2f3e6e` (2026-09-13 17:17:31 +0200) is an ancestor of **both**
   local `main` and `origin/main`, landed via merge `6a0eeb89`.
3. The graph organ — the probe whose earlier NO produced AY1-3 — now agrees:

```
file_purpose_graph.py why scripts/archive_row_body.py
  consumers (9)
    - is implemented by  task:298 … task:731            [task-implements]
    - is triggered by    file:.pre-commit-config.yaml   [wiring]
```

Eight `task-implements` edges plus **one wiring edge**. At freeze there was none.

**No wiring act was performed.** Clause 1's conditional did not fire. Wiring an already-wired
trigger would have been the deviation, not the compliance.

---

## 2 · The trigger, run to exhaustion — and the premise it refutes

### 2.1 What was run

`archive_row_body.py relocate` over the **60** rows that were both above the 1320-char source
ceiling and carried a relocatable dated-amendment tail run:

```
rows relocated        60          (of the 61 `propose` returned)
clauses relocated     66
source chars        242,578  ->  224,471      18,107 drained
tasks/archive/           24  ->       84 records
archive_row_body.py verify   OK — 84 records, 84 byte-identity PROVEN (legs A/B/C/D/E)
```

The 61st, `[#666]`, measures 1284 chars and is **not** above the ceiling. The contract's scope
is "the rows above the ceiling", so it was left and is reported rather than quietly swept in.
Including it would not have moved the count either: a row already under the ceiling cannot
fall out of the over-ceiling set.

**The mechanism is now exhausted above the line.** A second `propose` returns exactly one
row — `[#666]` — itself already under the ceiling.

### 2.2 The view did not move. Zero bytes.

```
BACKLOG.md   91,514 B  before  ->  91,514 B  after
gen_task_tree.py --emit-source   "BACKLOG.md already current (322 task(s))"
```

**Why, structurally rather than as a shortfall.** `BACKLOG.md` has been a **one-line view**
since `[#589]` landed `128f5093` on 2026-08-26. A row line is
`- [#id] [P][size] title · tasks/<file>.md` and carries **no body**. The bodies live in
`tasks/`. `archive_row_body.py` relocates **body clauses**. There is no path by which it can
move the view, and sixty relocations moving zero bytes is that fact measured end to end.

Composition of the view, measured at the base, for whoever does own the bar:

```
total                    91,281 B        bar 72,000 B        over by 19,281 B
321 row lines            53,388 B  (58.5%)   mean 166 B/row   max 301 B   p50 163 B
non-row scaffolding      37,893 B  (41.5%)   theme/story headings and prose
rows over 200 B          65               total excess above 200 B: 2,189 B
```

Trimming every one of the 65 longest row lines to 200 B recovers **2,189 B of 19,281**. The
19,281 B is ~116 rows at the mean — **a mass-closure act on row COUNT**, which is `[#731]`'s
enforced closure budget and `[#730]`'s evidenced closure list, not a narration drain.

### 2.3 The over-ceiling count did not move either, and cannot

```
backlog-row-length   148 of 322 before  ->  148 of 322 after
```

Classified over the 148 over-ceiling rows (436,320 clause chars) with
`archive_row_body`'s **own** predicates — `is_structural`, `is_dated_narration` — rather than
by eye:

| class | chars | share | clauses | why it is unreachable |
|---|---|---|---|---|
| structural | 154,097 | 35.3% | 501 | `Done when:` / `refs ` / `kill-candidates:` / `depends-on:` / `· DEFER` / `serialize-group:` — **ineligible by design**; relocating a `· DEFER` clause would silently flip a deferred row to open |
| plain prose | 166,601 | 38.2% | 547 | carries no citation-blind past date, so it is not dated-amendment narration in B1's sense — **outside the predicate** |
| dated narration | 115,622 | 26.5% | 146 | eligible **only** as a contiguous tail run before the pointer; after this drain, none of it is |

**73.5% of the over-ceiling corpus is beyond the mechanism by construction**, and the
remaining 26.5% is now positionally unreachable. This reproduces at a larger scale the state
first recorded on 2026-08-29, when `propose` drained to empty against a 59-locus residual.

### 2.4 What DID move

```
backlog-accretion    5 findings  ->  4        ([#241] cleared)
row-length p75       2,642  ->  2,541 chars
row-length p90       3,621  ->  3,492 chars
longest row         13,744  -> 13,677 chars
source corpus      685,188  -> 673,480 chars
```

The corpus shrank by 18,107 chars. The **count** did not, because the ceiling now sits at the
median and draining tails does not move a median. That is §4's subject.

---

## 3 · The lapsed groom, discharged

`grooming-cadence` read *"last groom 2026-07-30, 46d ago (> 21d cadence, ADR-41)"*. The entry
spliced into the BACKLOG grooming log records **this** groom — the relocation above — and not
a bare date.

```
doc_rot loci   7  ->  5      grooming-cadence CLEARED, accretion 5 -> 4
```

Two mechanics worth recording because both are easy to get wrong:

* **Authored in `tasks/manifest.json`**, which is the source. `BACKLOG.md` is generated and
  the grooming-log line is view prose.
* **Spliced BEFORE the `Next quarterly:` marker.** `validate_doc_rot._latest_groom_date`
  truncates the line at that marker so a target date is never read as a completed groom — an
  entry appended after it is invisible to the cadence clock it is meant to reset.

**Cost, stated rather than netted.** The groom-log line is *in* the view, so recording the
groom **grew** `BACKLOG.md` by 632 B (91,514 → 92,146). A lane whose clause 2 asks the view to
shrink cannot also discharge the cadence without paying this.

---

## 4 · The ruling on the two ceilings

### R1 — Neither is retired, and the contract's inference is the defect

The contract reasons: they "do not measure the same corpus, **so** one is retired or
re-based". **Different corpora is a reason to keep both.** Retiring either drops a live
refusal to satisfy a sentence's grammar.

| | `gen_task_tree._VIEW_ROW_BYTE_CEILING` | `validate_doc_rot._BACKLOG_ROW_CEILING` |
|---|---|---|
| value / unit | 400 **bytes** | 1320 **chars** |
| corpus | `BACKLOG.md` — the one-line **view** (no body) | `backlog_source.canonical_text` — the reassembled **source body** |
| job | anti-re-inflation tripwire | declared per-row size contract |
| enforcement | `find_incoherences`, FAIL, every commit | one corpus-level WARN Finding |
| live state | longest view row **301 B** of 400; **never fired**; growth-proof | **148 of 322 over**; p50 1302 |

400 is not a tightening of 1320 and 1320 is not a relaxation of 400. They share a noun and
nothing else. **`_VIEW_ROW_BYTE_CEILING` is CONFIRMED and untouched** — it guards a regression
measured at 279,814 B and costs nothing.

That the conflation is easy to make is not hypothetical: **this lane's own frozen contract
made it**, and reasoned from it to a clause no act can satisfy.

### R2 — What is re-based is the 1320's ROLE, by record, not its value

`[#532]` (2026-08-16) declared it a stated contract rather than a rolling percentile, on the
stated ground that *"a percentile ALWAYS has members by construction, so no percentile turns a
ranker into a detector."* Three dated points:

```
2026-08-16   [#532], the declaration    197 rows    10 over     5%
2026-09-05   r5p arm-2 lane             224 rows    70 over    31%   p50 1259
2026-09-14   this lane                  322 rows   148 over    46%   p50 1302
```

**The median has crossed the ceiling.** A line 46% of the corpus is over, sitting 18 chars
above the median, is a percentile again — the exact state the amendment abolished.

**The value does not move, and that is a finding rather than a reluctance:**

* raising it is forbidden by this lane's contract by name — *"the over-ceiling row COUNT
  falling rather than the ceiling rising"*;
* the r5p arm-2 lane ruled it *"reported against, never changed"*;
* lowering it is arithmetically empty while 148 rows sit over it;
* and §2.3 proves the drain that would legitimately lower the count is **exhausted**.

**What is owed**, and it is an architect's call under the V-2 budget's class (a): a
re-declaration that means something — a value whose over-population is a minority of the
corpus, or the honest retirement of the word *ceiling* in favour of *reference line*, which is
what ARM 2 already **is** since r5p collapsed it to one corpus Finding carrying count,
p50/p75/p90 and trend. **The lane records it; it does not perform it.**

### Where the ruling lands

At **both declarations**, comment-only, no value and no behaviour changed — because the
declaration is where the next reader meets the number:

* `scripts/validate_doc_rot.py` — the decay table, the exhaustion evidence, what is owed and
  to whom, and a "not the same contract as `_VIEW_ROW_BYTE_CEILING`" clause.
* `scripts/gen_task_tree.py` — the mirror clause, so the conflation is blocked from the view
  side too, carrying the measured consequence (60 relocations, zero view bytes).

And on row **`[#754]`**, amended with §2's measurements in place of the estimates it was filed
with.

**NOT in `protocols/STANDING_RULINGS.md`, deliberately.** That register carries rulings
*ratified in chat* that agents apply silently. This is a lane's ruling; filing it there would
claim a ratification it does not have.

---

## 5 · Tests — the verdict state is PRE-EXISTING, per AY1-1

Targeted set over this lane's whole diff (14 modules covering `BACKLOG.md`, `tasks/`,
`tasks/archive/`, `gen_task_tree.py`, `validate_doc_rot.py`):

```
uv run --locked python -m pytest <14 modules> -q -n 6
444 passed, 3 failed in 119.80s
```

`-n 6` rather than `-n auto`: the full suite at `-n auto` is OOM-killed on this box and the
worker count changes the failure count. **All three failures are PRE-EXISTING ON MAIN**, each
attributed by measurement rather than by assertion:

**(1) `test_the_live_view_is_under_the_589_done_when_byte_bar`** — both figures, because only
the difference is attributable:

```
at base 8a41c650    91,281 B    19,281 B over the 72,000 B bar
at HEAD             92,146 B    20,146 B over
THIS LANE'S DELTA      +865 B  =  233 B (row [#754]'s view line)
                                + 632 B (the groom-log entry — §3's stated cost)
```

The bar is `[#589]`'s own Done-when and `[#589]` is an **open P1 row**. Raising the constant to
go green is the act that row exists to forbid, so the RED is not this lane's to clear and was
not cleared.

**(2) `test_citation_regex_strips_only_real_dated_artifact_identifiers`** — paired
baseline/tip run of the test's **own** predicate over the base corpus, reassembled from git
objects:

```
BASE 8a41c650   685,188 chars   5 false strips
TIP  HEAD       673,480 chars   5 false strips
introduced by this lane: NONE        cleared by this lane: NONE
```

Identical sets — `2026-07-07-allowlist-v1.ps1`, `2026-07-08-emptygrant-v2.ps1`,
`2026-09-05-009`, `2026-09-08-architect-2.md`, `2026-09-10-architect.md` — living in rows
`[#690]` `[#715]` `[#643]` `[#686]` `[#689]`, none authored here.

No throwaway worktree was created for this: `lane-ceiling --check-worktrees` refuses on
worktree **presence**, so one would have refused a sibling wave's batch.

**(3) `test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export`** — this
lane changed **two** scripts, neither of them `graph_queries.py` or `export_backlog_view.py`.
The reference the test fails on is present at the base commit, and is **self-defeating**:

```
8a41c650:scripts/graph_queries.py:325:    "scripts/export_backlog_view.py": Disposition(
8a41c650:scripts/graph_queries.py:326:        reason="ORPHAN BY DESIGN: tests/test_export_backlog_view.py::test_no_gate_hook_or_"
```

The orphan-census disposition that exempts the export must **name** it to exempt it, and
naming it is what the test refuses. Pre-existing, unrelated to this lane, and reported here
because nobody appears to own it yet.

`ruff check` clean on both touched modules.

---

## 6 · Open items — handed on, not carried

1. **`[#754]` awaits an architect ruling** on the 1320 re-declaration (§4 R2). Curated-baseline,
   V-2 class (a).
2. **The 72,000 B view bar is `[#589]`'s**, red on main and diverging. §2.2 gives the
   arithmetic whoever takes it will need. The lawful drains are row **count** (`[#731]`,
   `[#730]`) or the scaffolding, not narration.
3. **`[#666]`** is the one row left with a relocatable run; it is already under the ceiling and
   was out of this contract's scope.
4. **The self-defeating export-orphan pair** (§5 item 3) is unowned as far as this lane could
   see.
5. **Four `backlog-accretion` findings remain** — `[#82]` `[#267]` `[#285]` `[#297]` — whose
   dates sit inside structural clauses the drain refuses by design. Not drainable work.

## 7 · Declared bypasses

`SKIP=audit-health` on all four commits — **one named hook**, never `--no-verify`, each
declared in its commit body. Cause, re-checked before each commit and unchanged:
`audit-health` FAILs on spine entry `e6acb23e`, the integrator's `docs/y-manifest-anchor`
merge on `main`, unanchored and **unexempt** because `docs/<slug>` does not match
`validate_branch_naming.LANE_BRANCH_RE` (verified by calling the regex).

This branch introduces no merge (`git log --merges main..HEAD` → 0) and a lane does not write
JOURNAL entries (P-1), so the gap is the integrator's to drain. The discriminator was run
first and split the two findings the gate originally reported: `8a41c650` read
tree-False/main-True — **tree lag** — and was cleared by the recorded remedy, a fast-forward
`git merge main` touching `JOURNAL.md` only.

## 8 · Footprint

```
126 files changed, 2,763 insertions(+), 63 deletions(-)

  tasks/archive/*.md          60 new records (the relocated narration, byte-identical)
  tasks/*.md                  60 rows drained + [#754] filed + [#754] amended
  tasks/manifest.json         [#754] node at the [S14] position; grooming-log entry
  BACKLOG.md                  regenerated (322 rows)
  scripts/validate_doc_rot.py comment-only — the ruling at the declaration
  scripts/gen_task_tree.py    comment-only — the mirror clause
  docs/audits/…-evidence.md   this artifact
```

No index was regenerated — the integrator is gate-of-record (Q1). No merge, no push, no
JOURNAL entry, no row closed, no ceiling constant changed.
