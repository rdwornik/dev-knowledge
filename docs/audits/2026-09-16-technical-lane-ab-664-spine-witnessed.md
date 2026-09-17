# LANE `ab-664-spine-witnessed` — end-of-lane artifact (PAUSED on a rule-vs-ruling conflict)

**Consumers:** `[#664]` · ADR-118 · `docs/audits/2026-09-16-technical-batch-ab-manifest-amendment-1.md` (integrator-AB)

**Lane:** `lane-ab-664-spine-witnessed` · branch `worktree-lane-ab-664-spine-witnessed` · batch AB · mode execute ·
**model ordered `opus` / ran `claude-opus-5`** · effort high · decision budget V-2 · base `f8ca1d40`, synced onto
`origin/main` at `a73da1ea`. The filename carries the contract's date (2026-09-16); the lane ran into 2026-09-17.

---

## 0 · The verdict, first

**PAUSED, not finished, and the pause is the contract's own instruction.** Mid-lane, operator ruling
`6e9f0bb8` (2026-09-17, *"strip the local commit gate to data-loss protection, move 31 hooks to the
conductor"*) landed on `main`. It moved all five `graph-*` hooks and `audit-health` to `stages: [manual]`,
where they run REPORT-ONLY in `.github/workflows/conductor.yml` job `commit-gate`. `[#664]`'s Done-when
still reads *"the three queries refuse at commit tier with a trip-test each"*. The row says one thing and
the ruling another. That is V-2 class **(b)**, and it is escalated here rather than decided.

| Done-when clause | State at the lane tip `a73da1ea` |
|---|---|
| edge computations re-measured under the five-kind class | **DONE**: 17 private sites, not the inherited 18 (§2) |
| … and driven to 0, every organ reading FPG-1 | **NOT DONE**: 17 → 16 by migration 1. Only one more (`validate_reconciliation`) is ruling-free (§3) |
| the three queries refuse at commit tier, a trip-test each | **REFUTED ON MAIN** by `6e9f0bb8`; the new witnesses are RED on the synced tree (§1) |
| `orphan_census` 0 against its stated class | **HOLDS**: `orphan-census: OK` at the tip |
| `task_coverage` 0 FAIL on the merged tree | the integrator's measurement. At this tip: OK over the lane's own 8 files |

## 1 · Step 2 — the commit-tier witnesses, and what they caught

`tests/test_graph_spine_commit_tier.py` (`618bfe86`) closes a gap the existing trip-tests left open. They
trip each query as a function and as a CLI; nothing drove a real `git commit` through the real hooks. The
witness:

- reads the four `graph-*` definitions out of the live `.pre-commit-config.yaml`, rewriting only the `uv`
  prefix and refusing if that prefix changes;
- installs them into a throwaway repo;
- asserts that a conforming commit lands and that each planted violation is refused by exactly its own hook;
- carries its own RED leg: the identical planted commit, with only that hook uninstalled, must land.

**RED-first, stated precisely.** The hooks were armed by lanes `v-664` and `x-664-spine-armed` before this
lane existed, so no pre-build RED run of the hooks was available. The disarmed leg is the RED run of the
commit tier.

```
at base f8ca1d40 (pre-ruling config)     4 passed   (180 s, -n 3)
at tip  a73da1ea (after 6e9f0bb8 sync)   4 FAILED   (114 s, -n 0)
  test_the_live_spine_is_ordered_rebuild_first_and_always_runs      graph-rebuild stage is [manual]
  test_the_refusal_blocks_a_real_commit...[graph-orphan-census]     did not refuse at commit tier
  test_the_refusal_blocks_a_real_commit...[graph-task-coverage]     did not refuse at commit tier
  test_the_refusal_blocks_a_real_commit...[graph-process-list]      did not refuse at commit tier
```

**The RED is correct, and it was NOT edited to pass.** Rewriting the witness to accept `stages: [manual]`
would weaken a frozen Done-when, which ADR-81 (amended 2026-06-24) forbids a lane to do. The witness
did what a trip-test is for: it caught a mechanism leaving the tier the row names, within hours. The
consequence is stated plainly: **this branch carries 4 RED tests until the conflict is ruled.** It should
not merge on a green-suite expectation.

**The ruling the operator owes, one of two:**
1. **Amend `[#664]`'s Done-when** from "commit tier" to "the conductor `commit-gate` tier". The witness is
   then rewritten against `conductor.yml` in the same act as the amendment, not before it.
2. **Return the three refusals to the local stage.** `6e9f0bb8`'s own header sets the bar: *"a hook
   returns to the local stage only with a counter showing what it caught, at what cost, over what
   window"*. None of the five `graph-*` hooks carries that counter today.

## 2 · Step 1 — the re-measurement (`e3976e9e`)

Full table: `docs/audits/2026-09-17-census-lane-ab-664-edge-class-remeasure.md`. All 65 shape-matching
modules were re-verdicted, not only the register's 21 rows.

```
private sites         17 in 16 modules   citation 14 · script call-site 3 · generation/template/test 0
measured OUT          8 registered private rows (4 clear, 4 lean)
measured IN           7 unregistered sites
blockers (overlap)    D unresolved target 8 · C consumer repo 4 · T other tree/ref 4 · G sub-file 3
ruling-free, S-sized  2 of 17
```

The register was **not** re-verdicted to match. A row flip without a code migration behind it is a
curated-register touch (V-2 class (a)); two earlier lanes declined the same class of edit on
`ORPHAN_DISPOSITIONS`. Those re-verdicts sit in census §4 as a proposal.

**The measurement's own finding:** 8 of 17 refuse on a target that does not exist — a probe naming a
file that is gone, a `@include` that resolves to nothing, a kill-candidate that closed. FPG-1 drops such
edges by construction (`PurposeGraph.add_edge`: *"a dangling or self edge is dropped, never invented"*),
so "read FPG-1 instead" presumes a representation of unresolved targets the graph deliberately refuses.
That is a ruling on FPG-1's semantics, ADR-118 flip-condition 1 territory, and it is a V-2 class (c)
fork with no standing ruling.

## 3 · Step 3 — migration 1 of W-G3 (`1fbaf7d3`)

**`batch_manifest.manifest_links` → FPG-1 input 3.** Before this commit, FPG-1's "reconciled"
consumer-at-landing input copied only the pool pass of `consumer_at_landing.measure`; the manifest-link
route was missing. Changes:

- **The parser** splits per linking surface (`manifest_link_surfaces`, keyed by the manifest or its
  `closed_by:` packet). `manifest_links` is now their union. Proven identical on the live tree by running
  the old function body against the new module: explicit 309, lane slugs 107, manifests equal.
- **FPG-1 input 3 imports the parser**, never re-deriving it, and writes each link as `consumed-by` FROM
  the surface that wrote it (detail `manifest link: explicit|lane-slug`). Attributing a closer's links to
  its manifest would have made "the close packet names the manifest" a self edge, which the graph drops.
- **Register row** `scripts/batch_manifest.py::manifest_link_surfaces` → reconciled. N moves:
  **private 18 → 17 · reconciled 3 → 4 · migrated 0 → 1** (pin updated in the same commit).

```
DIFF = 0 (tests/test_graph_migrations.py)
  fixture   organ-only {}   graph-only {}
  live      organ-only {}   graph-only {}   over 139 manifest-linked artifacts
RED first   5 failed before any code
FPG-1       consumed-by 708 -> 884 edges at the tip (the route, counted per linking surface)
```

**Why migration 2 was not started.** `validate_reconciliation` is S and ruling-free, and it is next in line.
But the clause the migrations serve (*"driven to 0"*) is unreachable without the class (c) ruling in §2,
and the lane is paused on class (b) regardless. Deviation-with-disclosure would be the wrong trade here.

## 4 · Step 4 — the census at the tip

```
orphan-census        OK (0 undispositioned)
task-coverage        OK over the lane's 8 files
process-list         168 processes · 134 triggered · 34 not · 0 dangling
edge-class-census    17 private · 4 reconciled · 1 migrated · 6 verdicted out · OK
FPG-1                2882 nodes · 21718 edges · 15 kinds
```

## 5 · Tests — targeted, and two failures proven foreign

The full suite was not run, per the contract. The box also ran out of memory: the harness killed three
background pytest runs and one background commit, so every run below is serial and in the foreground.

```
test_graph_spine + test_edge_class_census + test_graph_migrations      66 passed
test_file_purpose_graph                                                35 passed
test_manifest_link_route                                               15 passed
test_batch_manifest + test_consumer_at_landing                         90 passed, 1 FOREIGN
test_funnel_coverage + test_decision_coverage                         130 passed, 1 FOREIGN
test_graph_spine_commit_tier   base 4 passed · tip 4 FAILED (section 1, the escalation)
ruff check                                                            clean on every touched file
```

**The two foreign failures are live-corpus baseline drift:**
- `test_consumer_at_landing::test_the_live_corpus_measures_and_the_baseline_matches_it`
- `test_funnel_coverage::test_committed_baseline_agrees_with_a_live_measurement`

Other lanes have landed artifacts since 2026-09-06 that neither committed baseline lists. The one code
path this lane touches in them (`manifest_links`) is identical before and after (§3), and the only artifact
this lane adds to either set is its own census. Baselines are curated (V-2 class (a)), so they were left
untouched.

## 6 · Declared bypasses — named hooks only, no `--no-verify`

- `doc-counts-pytest-freshness` (`618bfe86`, `1fbaf7d3`): new tests move the GENERATED collected-test claim.
- `audit-health` (`1fbaf7d3`): its one FAIL was `journal_spine_anchor` on main's unanchored 2026-09-17
  merges, not this diff. A lane does not journal (P-1), and the ruling carried by those same merges makes
  `audit-health` manual on `main`.

## 7 · For the integrator and the operator

1. **Rule the class (b) conflict (§1)** before merging. The branch carries 4 RED witnesses by design.
2. **Rule the class (c) fork (§2): should FPG-1 represent unresolved targets?** Without it, 8 of 17
   computations cannot migrate and "driven to 0" cannot close.
3. **Rule the class (a) re-verdicts (census §4).** Applying them moves N without a migration, so they need
   an explicit word.
4. **Regenerate at the merge:** `ecosystem/doc-counts.md` (new tests), `docs/audits/README.md` (two new
   audits), and `BACKLOG.md` / `tasks/manifest.json` (row `[#664]` amended in `e3976e9e`).
5. **Next ruling-free migration:** `validate_reconciliation` → a `reconciled-with` edge kind on FPG-1 (S).
6. **`[#664]` stays OPEN.** No new task id was allocated; this lane's block `839-842` is unused.

---

## AMENDMENT 1 · 2026-09-17 · the operator's rulings, applied

> In-file amendment marker. The sections above are left as written. Where they conflict with
> this amendment, this amendment is current: §7 item 6's "block unused" and §0's "PAUSED" are
> both superseded below.

**(b) → option 1, with a condition.** `[#664]`'s Done-when moves from commit tier to the conductor
`commit-gate` tier. It is **satisfied only once CI enforcement is ON**. Today
`deploy/conductor-required-checks.ruleset.json` still arrives `enforcement: disabled`, and three red
pushes landed under it. The row now records the dependency in so many words: **conductor-tier refusal +
CI enforcement off = theatre** (`6b268a59`). The operator stated that the conflict came from their own
ruling `6e9f0bb8`, and that not weakening the frozen Done-when was right.

**Why the four commit-tier witnesses stay RED, by ruling.** `tests/test_graph_spine_commit_tier.py`
checks that the three refusals block a real `git commit`, and since `6e9f0bb8` they do not. Rewriting the
witness against `conductor.yml` now would turn it green on a tier that enforces nothing: a passing test
for exactly the theatre the amended row names. So the RED is the accurate reading of the tree. It stays RED
until one of two things happens:
- CI enforcement is ON, and the witness is re-pointed at the conductor tier in the same act;
- the refusals return to the local stage under `6e9f0bb8`'s counter bar.

The integrator merges knowing this. It is not a regression to fix at the merge.

**(c) → YES, filed as its own row.** The graph must represent a missing target as an explicitly dangling
edge rather than drop it. That is a design change to FPG-1, so it is **`[#839]`** (`81eecabb`, id reserved
from this lane's block via `id_allocator.py`), not absorbed here. In the same commit as (b), `[#664]`'s
*"driven to 0"* is re-scoped to *"every dangling edge is measured and carries a disposition"*. The 8 of 17
sites at absent targets are a finding, not a number to zero out.

**(a) → APPROVED, and each entry cites its measurement** (`f3ad827d`). Every row the census moved names
`docs/audits/2026-09-17-census-lane-ab-664-edge-class-remeasure.md` and the section behind it: §3 blocker,
§4 re-verdict, §5 reason. A test asserts the citation holds. One consequence was not in the census:
`decision_coverage` is reconciled but was born an FPG-1 reader, so `BORN_RECONCILED` keeps it out of
`migrated`.

```
edge-class-census    16 private · 5 reconciled · 1 migrated · 47 verdicted out · OK
tests (targeted)     test_edge_class_census + test_graph_migrations 31 passed · test_graph_spine 37 passed
ruff                 clean
```

**Integrator list, updated:** regenerate `BACKLOG.md` + `tasks/manifest.json`'s `generated_sha256` (rows
`[#664]` amended, `[#839]` filed, manifest node inserted under `[S3]`); also `ecosystem/doc-counts.md`
(two more tests) and `docs/audits/README.md`. Block `839-842`: 839 used, 840-842 unused. The lane hands
back here.
