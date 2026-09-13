# LANE `x-664-spine-armed` — end-of-lane artifact

**Consumers:** `[#664]` · ADR-118 · intake #86 · `[#694]` · `[#655]` · `[#734]`

**Lane:** `lane-x-664-spine-armed` · branch `worktree-lane-x-664-spine-armed` · **slot 5** of
`docs/audits/2026-09-13-technical-batch-x3-manifest.md` · mode `execute` · effort high ·
decision budget V-2 · **serialised behind `lane-x-000-trustworthy-suite` (AX27-3)**, which had
handed back and whose worktree was gone before this lane touched the store.

**Model, recorded because the manifest ordered a correction:** the frozen contract states
`opusplan`; the dispatcher fired this slot at `opus` instead, on the measured finding that
`opusplan` silently resolves to Sonnet on a `--bg` lane (manifest §6 finding 7). This lane
neither re-decided that nor relied on it.

**Base.** Step-0 sync ran before anything else. `main` was `81c0a4c9` when the worktree was
cut and moved three times during the lane; each move was taken as a sync merge rather than
worked around. Final merge-base: **`34daf06a`**. The lane's own tip carries five files and no
more:

```
.pre-commit-config.yaml
scripts/graph_queries.py
tests/test_edge_class_census.py
docs/audits/2026-09-13-census-x-664-spine-armed-measurement.md
docs/audits/2026-09-13-census-x-664-delete-list.md
```

---

## 1 · The Done-contract, clause by clause

### Clause 1 — the three refusals EXIST and REFUSE, each with a RED-first trip-test

**Two of the three were already live and are re-verified rather than re-built.** `orphan_census`
and `task_coverage` landed in lane `v-664` with their trip-tests
(`tests/test_graph_spine.py::test_orphan_census_cli_exits_non_zero_on_a_refusal` and
`::test_task_coverage_cli_exits_non_zero_on_a_refusal`), wired to `graph-orphan-census` and
`graph-task-coverage`. Both exercised on this tree: §2.

**The third is the one the contract names that nobody had armed — the five-kind edge class.**
It is NOT `process_list` (which was already armed, and is a fourth refusal): the contract's own
words are *"`orphan_census`, `task_coverage`, and the five-kind edge class"*, and the five-kind
class is `[#664]`'s Done-when half that lane `v-664` measured and left unheld —
*"the corpus-structure edge computations … re-measured under §A.1's five-kind class and driven
to 0."*

Built here as `graph_queries.py edge-class-census`, wired to `graph-edge-class-census`, with
**24 RED-first witnesses** in `tests/test_edge_class_census.py`. The RED was recorded before
any module existed: collection failed with `module 'graph_queries' has no attribute
'EdgeComputation'` at `fff922b8`, and the arming commit `d5b70a93` turned them green.

**It is a RATCHET, not a bar, and that is the load-bearing design decision.** Eighteen private
computations are live and owe their W-G3 migration **one organ per lane** (ADR-118 §5, which
rejects the big bang by name). A gate refusing all eighteen would refuse every commit in the
repo on a defect no single committer can legally repair — the unbounded-refusal shape
`decision_coverage.ARM_DATE` already exists to avoid. So the set may **shrink** and may not
**grow**:

- **leg 1, the ratchet** — a module under `scripts/` that NEWLY acquires the shape (an add, or
  an edit giving it a shape its HEAD version lacked) and that the register does not verdict;
- **leg 2, the rot guard** — a register row naming a file, or a symbol, that is gone.

Both legs carry both directions, because a test that passes on conforming input is not a
trip-test. The permissive direction —
`test_edge_class_census_admits_a_module_that_ALREADY_had_the_shape_at_HEAD` — is what makes
the gate landable at all, and `test_edge_class_census_refuses_a_module_that_NEWLY_acquires_the_shape`
is why an add-only reading was rejected: it would miss every module that grows the shape, which
is the likelier of the two.

**Leg 2 BLOCKS where `stale_dispositions()` only NOTES, and the asymmetry is reasoned.** A
stale orphan disposition is harmless on its own terms — the file is gone, so the orphan is gone,
and refusing would punish the deletion. A stale edge-computation row is a migration obligation
leaving the register silently, which moves N with nobody ruling that it moved.

**It is NOT a view, and it says so rather than mis-filing itself.** The other three refusals are
SELECTs over FPG-1. This one joins commit-time state (the staged set, plus a HEAD comparison) to
a **curated register**, because *"this module computes an edge privately"* is a ruling about a
module's design, which no graph holds and none should. What is computed mechanically is only
the SHAPE of one module's source — never a relation between two corpus files — so nothing
re-derives what FPG-1 already answers, which is `[#664]`'s first anti-pattern. Calling it a
query would be exactly the mis-filing DECLARE-REVIEWS §A.1 correction 2 forbids.

### Clause 2 — the current numbers are MEASURED and reported

`docs/audits/2026-09-13-census-x-664-spine-armed-measurement.md`, taken at `5e280b05` and
summarised at §2 below.

### Clause 3 — the residue, one file for one GO

`docs/audits/2026-09-13-census-x-664-delete-list.md`, delivered as
`to-browser/DELETE-LIST-2026-09-13.md` with the OPERATOR-INTERFACE copy header naming its
source blob (`…@4d5ca7d0`). 37 rows: **6 DELETE · 2 TRIGGER · 28 KEEP · 1 escalated register
row**, each with its evidence read from FPG-1 rather than from a grep.

### Clause 4 — explicitly NOT done: driving the numbers to zero

**Held.** N is 18 before and 18 after. No module was deleted, no disposition was dropped, no
orphan was wired. The two rows that would have required it — §3.1's register correction and
§3.3's wiring-surface ruling — are escalated, not taken.

### Clause 5 — English, hyphen-only names, logging over print, `pytest` green

English and hyphen-only throughout. `logging` is used on the module's diagnostic path and
`print` on the CLI's report path, matching the three refusals that were already there — a
report a hook's operator reads is stdout, not a log record. Click is not introduced: this is a
subcommand on an existing `argparse` CLI, and converting that CLI is a different act. Suite
status is §4.

---

## 2 · The numbers, in one place

```
FPG-1                 2618 nodes · 19839 edges · 15 kinds        (v-664: 2560 / 19469 / 15)
orphan_census         0 refusals · 36 disposition rows · 0 stale
task_coverage         0 refusals, empty staged set AND this lane's own diff
process_list          159 processes · 124 triggered · 35 not · 0 dangling refs
edge_class_census     18 private · 3 reconciled · 0 migrated · 1 verdicted out of the class
  by kind             citation 10 · script call-site 6 · template 1 · test 1 · generation 0
grandfathered         141 modules · 65 shape-matching · 44 matching-and-unverdicted
cost                  rebuild 17.7 s · orphan census 2.7 s · edge-class census 3.7 s
```

Post-sync (after `lane-x-730` merged mid-lane): 160 processes, 36 untriggered, 37 disposition
rows. Both readings are printed in the residue artifact; the measurement artifact stands as
taken, because a dated measurement is not a live roster.

**`generation` is 0 and is printed anyway** — an absent kind is evidence, and a table that drops
its empty rows cannot distinguish "none" from "not looked at".

**The 44 is the size of the exemption, measured because a bound that is not measured is an
exemption.** Growth in it would falsify this measurement rather than pass unnoticed.

---

## 3 · What the mechanism found by firing — four findings, none absorbed

### 3.1 `scripts/worktree_seed.py` — dispositioned AND triggered. ESCALATED (V-2 class (a))

`tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
is RED. **Proven foreign by a paired baseline run** before anything was concluded: this lane's
files were set aside, the test failed identically at the base alone, and they were restored.

The process is genuinely triggered, and **the shorter diagnosis is wrong in a way worth
recording.** `.claude/settings.json` names the path, which is what `why` reports first — but it
names it inside a `"//worktree"` COMMENT key. The real edge is transitive:
`.pre-commit-config.yaml` triggers `gen_lane_contract.py`, which **imports** `worktree_seed`,
and `TRIGGER_KINDS` spans `triggers` and `imports`. The trigger survives whatever happens to the
comment.

The repair is a one-line curated-baseline edit, which V-2 class (a) escalates.
`lane-x-000-trustworthy-suite` classified it identically and also reported rather than took it.
**Two lanes declining the same edit under the same rule is the rule working**, and it is now
row 1 of the residue list so it reaches the operator rather than a third lane.

### 3.2 A path in a JSON COMMENT key is read as wiring — latent, separable, not taken

`.claude/settings.json` mentions `worktree_seed` only in a `"//"` key and the loader forms a
`triggers` edge from it. `//`-prefixed keys are this file's comment convention throughout, so a
path *discussed* becomes a path *fired*.

This is the **exact class** lane `v-664` fixed one input over — `ORPHAN_DISPOSITIONS` keys were
read as call-site strings until executable position was made mechanical (*"a code string counts
only inside a `Call` and only when it is exactly a path"*). The JSON loader has the same hole
with no equivalent rule. Harmless today (every settings.json comment path measured here also
has a real edge) and exactly the shape that makes an orphan census report clean for the wrong
reason later.

**Not taken, for a measured reason rather than a preference:** changing a wiring input moves
`triggers` edges repo-wide and can silently flip a process from triggered to orphan, refusing
commits in every tree. That needs its own RED-first lane with a before/after edge diff.

### 3.3 The wiring-surface list is why 21 of 37 residue rows exist — an ASK, not a row

The census reads five wiring surfaces and `.claude/commands/*.md` is not one, so **every
operator-invoked organ reads as an orphan by construction, whatever its real adoption.** That is
21 of the 37 rows — a clear majority — and it grew by one during this lane
(`propose_row_closures.py`, landed by `lane-x-730`). One ruling disposes of more of the list
than every row above it combined. §5 of the residue artifact puts it to the operator with both
consequences stated.

### 3.4 Lane `v-664`'s stated shortlist predicate does not reproduce its own table

`v-664` §2.5 states its shortlist as *"a module that walks the tree and compiles ≥2 regexes"*.
Measured against the twenty-one rows that table holds, **four fail it**: `validate_doc_rot.py`
and `dispatch_drift.py` walk no tree; `codemap/ast_walker.py` and `reverse_dep_oracle.py`
compile no regex at all. Inheriting the stated predicate would have armed a gate over a
different population from the one the register records.

Repaired rather than inherited: the predicate here is `EXTRACT and (SCAN or READ)`, with
`ast.parse` a first-class extraction signal, and **all twenty register files clear it** — pinned
by `test_every_register_row_actually_HAS_the_shape_it_is_registered_for`, so the two can never
drift apart silently again.

### 3.5 The ratchet's first catch was itself, and the register grew a third status

The armed hook **refused the very commit that armed it**: `graph_queries.py` gained an `ast`
walk in that change and matched its own predicate. Admitting it as `private` would have been a
lie — its subject is a module's SHAPE, never a relation between two corpus files — and would
have inflated N, handed a W-G3 lane a migration that does not exist, and made the one number
this query reports untrue.

So `REGISTER_STATUSES` gained `not-an-edge`: **the register must be able to say no.** A
recall-favouring predicate will keep finding modules that read source text for something other
than corpus structure, and without a negative verdict the only way to admit one is a false
`private` row. Pinned by `test_a_NEGATIVE_verdict_is_expressible_and_admits_the_module`, which
also asserts such a row does **not** count toward N.

---

## 4 · Suite status — targeted, and every failure proven foreign

`[#528]`: the full suite runs once, at integration. This lane ran the **impacted set**, selected
by the repo's own organ (`impacted_tests.py select --changed scripts/graph_queries.py`) plus
`tests/test_file_purpose_graph.py`.

```
pytest <18 impacted files> -n 4      1040 passed, 1 skipped, 9 failed   in 519 s
pytest tests/test_edge_class_census.py -n 0       24 passed
ruff check                                        clean on every touched file
```

**All nine failures are PRE-EXISTING, and each is proved rather than asserted:**

- **six** are the set `lane-x-000-trustworthy-suite` measured **on a clean tree at its own
  start** and recorded as not absorbed — `test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
  plus five in `tests/test_gen_handoff.py` (`assert 15 == 13`, `assert 6 == 5`, the suffixed-bundle
  and funnel-health probes);
- **one** of those (`worktree_seed`) was independently re-proved here by a paired baseline run;
- **three** were not in that lane's targeted set and are proved here by a **paired baseline run
  of their own** — the lane's five files reverted to `34daf06a`, the three run, all three
  failing identically, the files restored and the footprint re-verified:
  `test_canonical_docs.py::test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date`,
  `::test_the_derived_leg_is_warn_class_on_arrival`, and
  `test_v6_frozen_contract.py::test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped`.

None is in this lane's contract and none is absorbed.

---

## 5 · Declared bypasses — named hooks, in the commit bodies, no `--no-verify`

`--no-verify` was not used at any point. Three hooks were skipped by name, each declared in the
commit that skipped it:

- **`doc-counts-pytest-freshness`** — 24 new tests move the collected-test claim in the
  GENERATED `ecosystem/doc-counts.md`;
- **`audit-index-freshness`** — two new audits move the generated `docs/audits/README.md`;
- **`organ-index-freshness`** — the fifth `graph-*` hook moves the generated
  `ecosystem/organ-index.md`.

All three are **generated indices**, and the contract puts their single regeneration with the
integrator at the merge (Q1). Every other pre-commit, commit-msg and pre-push hook ran and
passed on every commit — **including the new one**, which refused a commit of its own (§3.5).

**One gate refused twice for a reason that was not this lane's work.**
`journal_spine_anchor` blocked on the integrator's freshly-merged, not-yet-anchored spine
entries (`78823b05`, then `83961dde`). Diagnosed with the check's own discriminator, **not
repaired** — a lane does not journal (P-1) — and drained by waiting: a bounded poll (60 s
interval, 15-tick bound, predicate re-read from the ref each tick) cleared on tick 3 both times.
Had the bound been exhausted it would have reported rather than extended.

---

## 6 · For the integrator

1. **Regenerate three indices at the merge** — `gen_doc_counts.py --write`,
   `gen_audit_index.py --write`, `generate_organ_index.py --write`. That is the whole of the
   declared bypass.
2. **`CLAUDE.md` §9 rosters four `graph-*` hooks and there are now five.** Out of this lane's
   footprint and following an established precedent: after `v-664` armed its four, the organ
   index was regenerated separately (`c3bdee3c`) and §9 was updated by a later lane's close
   packet (`a525c97e`). The new row: *"`graph-edge-class-census` — a NEW private five-kind edge
   computation ([#664] Done-when)"*. Floor: **hub-only**, same one-line reason as the other four.
3. **`to-browser/DELETE-LIST-2026-09-13.md` is delivered and waits on ONE operator word.** Its
   §5 structural ask is worth more than any single row in it.
4. **`scripts/worktree_seed.py` still needs removing from `ORPHAN_DISPOSITIONS`** — now declined
   by two lanes under the same rule. It REDs `tests/test_graph_spine.py` for anyone who runs it.
5. **`[#664]` stays OPEN.** Clause 1 is now discharged in full — three refusals, three
   trip-tests — and what keeps the row open is unchanged: the eighteen private computations owe
   their W-G3 migration one organ per lane, and step D (the `ARCHITECTURE.md` Ch2 render) is
   X3's other half. The row's status paragraph wants the `edge_class_census` sentence adding;
   that is a `tasks/` edit and a successor's act.
