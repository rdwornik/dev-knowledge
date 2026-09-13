# Census — the [#664] spine, MEASURED on the merged tree (lane `x-664-spine-armed`, X3 slot 5)

**Consumers:** `[#664]` · ADR-118 · intake #86 ·
`docs/audits/2026-09-13-technical-lane-x-664-spine-armed.md` (this lane's end-of-lane artifact)

**What this is.** Step 3 of the frozen contract: *"MEASURE and record the current numbers — do
not act on them."* Every number below is read from an organ on this tree at
`d5b70a93` (base `89a149ea`), never restated from a prior artifact. Where a number differs from
the one a previous lane recorded, both are printed and the difference is named.

**What this is NOT.** It is not a disposition list and it changes nothing. The operator-facing
delete / trigger / keep residue is the separate artifact
`to-browser/DELETE-LIST-2026-09-13.md`, and deletions are the operator's act.

---

## 1 · Method, so the numbers are reproducible rather than quoted

```
base            89a149ea  (main, fast-forwarded into the lane before any measurement)
tree            d5b70a93  (the lane's arming commit)
store           .git/worktrees/lane-x-664-spine-armed/fpg-graph/FPG.db
instrument      scripts/graph_store.py stats
                scripts/graph_queries.py {orphan-census, task-coverage, process-list,
                                          edge-class-census}
                the module functions called directly for the counts no CLI prints
```

Two properties make these readings trustworthy rather than merely printed. The store is opened
through `gs.ensure()`, which rebuilds when stale, so nothing here answers from yesterday's
graph. And every count is taken from the SAME open store in one process, so no two numbers
below straddle a rebuild.

## 2 · FPG-1, the persisted store

```
nodes   2618
edges   19839
kinds   15
```

Movement since lane `v-664` recorded `2560 / 19469 / 15` on its own tree: **+58 nodes,
+370 edges, kinds unchanged**. Corpus growth over four days of batch X, not a schema change —
the edge-kind count is the schema, and it has not moved.

## 3 · Refusal 1 — `orphan_census`

```
undispositioned orphans (the REFUSAL)      0
ORPHAN_DISPOSITIONS rows                  36
stale disposition rows (NOTE-only)         0
dispositioned BUT reported triggered       1   scripts/worktree_seed.py
```

**Zero refusals, and the zero is real** — no stale row is propping it up, which is the failure
mode a register like this has. `orphan_census` therefore holds `[#664]`'s Done-when clause
*"`orphan_census` reaches 0 against its stated node class after dispositions"* on this tree.

**The one non-zero number is a live defect, and it is NOT this lane's to repair.** See §8.1.

## 4 · Refusal 2 — `task_coverage`

```
refusals over an empty staged set          0
refusals over this lane's own 3 files      0
```

Zero FAIL on the merged tree — `[#664]`'s other Done-when clause. The second reading is the
one that matters for a lane: a gate that passes because nothing is staged has proven nothing,
so it is re-run against the actual diff this lane introduces.

## 5 — `process_list`

```
script    147 nodes   124 triggered    23 not
command    10 nodes     0 triggered    10 not
skill       2 nodes     0 triggered     2 not
TOTAL     159 nodes   124 triggered    35 not
dangling process references in ARCHITECTURE.md      0
```

Against lane `v-664`'s `158 / 119 / 39`: **+1 process, +5 triggered, −4 untriggered.** The
arrivals and departures are individually attributable and are listed in the residue artifact
rather than summed here.

**Zero commands and zero skills are triggered, and that is the census's finding rather than a
gap in this measurement.** Nothing in this repo fires a command or a skill; the seven acts the
process-trigger census rules a closed list are OPERATOR acts. All twelve are dispositioned.

## 6 · Refusal 3 — `edge_class_census`, armed by this lane

```
private          18
reconciled        3
migrated          0
not-an-edge       1

private by kind   citation 10 · script call-site 6 · template 1 · test 1 · generation 0
```

**N did not move, and that is the contract-required state rather than a shortfall.** `[#664]`'s
Done-when asks the eighteen to reach 0; ADR-118 §5 rules that migration **one organ per lane**
and rejects the big bang by name; this lane's contract says in as many words *"explicitly NOT
done: driving the numbers to zero."* What changed is that the number is now **held**: before
this lane it could grow silently, and it can no longer.

**`generation` is 0 and is printed anyway.** An absent kind is evidence — it says the class's
fifth member has no known private computation in this repo — and a table that drops its empty
rows cannot distinguish "none" from "not looked at".

### 6.1 The grandfathered population, measured because a bound that is not measured is an exemption

```
scripts/**/*.py modules                                    141
matching the shape predicate                                65
matching AND unverdicted -- NEVER refused by the ratchet     44
```

The ratchet refuses only a module that **newly** acquires the shape. Those 44 predate the
register and are admitted by construction, exactly as `decision_coverage` grandfathers its 112
accepted-but-unexecuted decisions. The number is recorded so the size of the exemption is
visible: it is 44 today, and any growth in it is a growth the ratchet did not stop and would be
this measurement's own falsification.

### 6.2 The 32-vs-20 cardinality gap — still ruled, re-confirmed not re-opened

The process-trigger census counted 32 orphans against a 20-item predicate. Lane `v-664` ruled
it by **widening the node class to every in-tree process file** and naming the 6 that live on
the operator's disk under `~/.claude/` as unrepresentable in a graph of this repo's corpus. That
ruling stands and this lane re-confirms rather than re-litigates it: 159 process nodes, 36
dispositions, 0 refusals. The gap is closed by construction, not by rounding.

## 7 · Cost, measured on this tree

```
graph-rebuild            17.7 s
graph-orphan-census       2.7 s
graph-edge-class-census   3.7 s   (new)
```

Against lane `v-664`'s 14.6 s rebuild at 2260 nodes: **+3.1 s at +358 nodes**, consistent with
a full rebuild scaling with corpus size. The new hook adds **3.7 s** to every commit — one
interpreter start, the `ensure()` mtime sweep every query pays to prove the store is fresh, and
an AST parse of the staged Python only. It does NOT scan the tree: the 65-module reading in
§6.1 is a measurement taken here, not work the hook does.

ADR-118's flip-condition 2 asks W-G1 to fix the rebuild cost against the gate budget. This
lane does not meet that condition and does not claim to; the number is recorded so the lane
that does has a second data point rather than one.

## 8 · Findings — two, neither taken, both reported

### 8.1 `scripts/worktree_seed.py` is dispositioned AND triggered — a live RED, owner ESCALATED

`tests/test_graph_spine.py::test_a_disposition_register_entry_cannot_manufacture_its_own_trigger`
is RED on this tree. **Proven foreign by a paired baseline run** — the lane's three changed
files were set aside, the test was run at the base alone and failed identically, and the changes
were restored. It is not this lane's doing.

The process is **genuinely** triggered, and the discriminator is worth recording because the
shorter reading is wrong. `.claude/settings.json` names the path, which is what
`file_purpose_graph.py why` reports first — but it names it inside a `"//worktree"` COMMENT
key, which is prose. The real edge is the transitive one: `.pre-commit-config.yaml` triggers
`scripts/gen_lane_contract.py` (the `lane-contract-check` hook) and that module **imports**
`worktree_seed`, and `TRIGGER_KINDS` spans `triggers` and `imports`. So the trigger survives
even if the comment were deleted.

The repair is therefore to **drop the `ORPHAN_DISPOSITIONS` row** — the process acquired a
trigger and a disposition for it now records a ruling about a condition that no longer holds.
That is a **curated-baseline touch**, V-2 class (a), which this lane's decision budget
escalates rather than takes. Lane `lane-x-000-trustworthy-suite` reached the same classification
independently (its evidence artifact, finding 1) and also reported rather than took it. Two
lanes declining the same edit on the same rule is the rule working, not a gap — it is one line
for whoever owns the baseline, and it is row 1 of the residue artifact.

### 8.2 A path in a JSON COMMENT key is read as wiring — latent, not the cause above

Separable from §8.1 and worth its own line because the next reader will otherwise merge them.
`.claude/settings.json` mentions `scripts/worktree_seed.py` only in a `"//worktree"` key, and
the wiring loader forms a `triggers` edge from it. A `//`-prefixed key is the JSON comment
convention this repo's settings file uses throughout, so a path discussed in a comment becomes
a trigger.

This is the **exact class** lane `v-664` fixed one input over: `ORPHAN_DISPOSITIONS` keys were
being read as call-site strings until executable position was made mechanical (*"a code string
counts only inside a `Call` and only when it is exactly a path"*). The JSON loader has the same
hole with no equivalent rule. It is harmless **today** — every settings.json comment path
measured here also has a real edge — and it is exactly the shape that makes an orphan census
report clean for the wrong reason later.

**Not taken here**, and the reason is a measurement rather than a preference: changing a wiring
input changes `triggers` edges repo-wide, so it can silently flip a process from triggered to
orphan and refuse commits in every tree. That needs its own RED-first lane with a before/after
edge diff, which is more than a footprint this lane has.

---

**Measured by:** lane `lane-x-664-spine-armed`, batch X wave 3 slot 5, 2026-09-13.
**Nothing in this file was acted on.** The residue that asks for an operator act is
`to-browser/DELETE-LIST-2026-09-13.md`.
