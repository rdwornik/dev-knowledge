# LANE v-664 delivery-spine — end-of-lane artifact

<!-- Batch V, lane V-664. Frozen contract:
     `docs/audits/2026-09-08-technical-batch-v-launch-contracts/LANE-v-664-delivery-spine.md`
     Branch `worktree-lane-v-664-delivery-spine`, base `main` @ 552997bb.
     Commit-and-STOP: nothing here is merged, pushed, or journaled. -->

> **Class:** technical · **Date:** 2026-09-09 · **Row:** `[#664]` · **ADR-118** · intake #40 ·
> intake #86 · `docs/audits/2026-09-08-technical-process-trigger-census.md`
> **Consumer:** `[#664]`, whose Done-when this artifact reports against, and the batch V
> integrator's close packet.
> **Posture:** this lane commits to its own branch and STOPs. No merge, no push, no JOURNAL.
> **Merge gate:** `HIGH raw=5 fixed=5 unresolved=0` — five Terra passes, the fifth returning
> nothing, which is the stopping rule. Full tally and per-finding disposition: *The Terra
> pre-merge review*, below.

## Step 1 — locators resolved, and the plan

### 1.1 Every locator the contract cites, resolved before it was trusted

| Locator | Verdict |
|---|---|
| `[#664]` | LIVE — `tasks/664-wire-fpg-1-as-the-delivery-spine-three-commit-tier.md`, `status: open`, filed at `3b50ea9f`. Read in full; it is this contract's own summary. |
| `[#644]` (named by DECLARE-RECOVERY) | NOT this row — the contract's warning is correct and is obeyed: `[#644]` is untouched. |
| `ADR-118` | `docs/decisions/ADR-118-one-graph-organs-are-views.md`, **Proposed**, 2026-09-07. Read in full. |
| intake #40 | `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md`. Done-when read **as amended by `ff103444`** (the five-kind narrowing). |
| intake #86 | `docs/intake/2026-09-07-tech-orphan-census-organ.md`, DRAFT. Read in full. |
| process-trigger census | `docs/audits/2026-09-08-technical-process-trigger-census.md`. The 32-orphan list read row by row. |
| `ff103444` | Resolves. `docs(intake): narrow intake #40's Done-when to corpus-structure edges, citing Z-C3 [#642]`. Quoted below rather than paraphrased. |
| `scripts/file_purpose_graph.py` | 997 lines, 5 inputs, 12 edge kinds, wired into no gate. |
| `ADR-118:34` (the 1922 / 12 664 / 12 baseline) | Resolves to the Context bullet. Live re-measurement below. |
| DECLARE-SPINE-2026-09-09 §3, DECLARE-REVIEWS-2026-09-07 §A.1–2, `to-browser/DIGEST-2026-09-07-repo-graph.md` | **NOT RESOLVABLE IN-TREE.** No file of any of those names exists in this repo, and `CLAUDE_PROMPTS_DIR` is unset in this lane's environment. Their substance reaches this lane only through the surfaces that absorbed it: `[#664]`'s row body (DECLARE-SPINE §3) and intake #40's 2026-09-09 amendment (DECLARE-REVIEWS §A.1). **Consequence, stated rather than worked around:** the digest's enumeration of *which* twelve organs compute edges privately is unavailable, so clause 3's N is **re-measured from the tree** rather than inherited from a list this lane cannot open. That is what clause 3 asks for; it is recorded here because the reason is an absence, not a preference. |

### 1.2 Baseline, re-measured on this tree

```
ADR-118:34 baseline (2026-09-07)   1922 nodes   12 664 edges   12 edge kinds
this tree    (2026-09-09, 552997bb) 2001 nodes   13 575 edges   12 edge kinds
delta                                 +79 nodes     +911 edges    0 kinds
```

Per input, live: `doc-code-edge` 45 · `audits-index` 936 · `consumer-at-landing` 12 102 ·
`tasks-depends-on` 438 · `deploy-manifest` 54. Per kind: `cites` 11 474 · `indexes` 936 ·
`consumed-by` 628 · `generated-from` 392 · `enforces` 29 · `archives` 24 · `carried-by` 23 ·
`depends-on` 22 · `declared-in` 16 · `ships` 13 · `carrier-source` 9 · `governed-by` 9.

**The delta is corpus growth, not a graph change.** Two days of batch V landings — twenty
`[#64x]` rows from lane V-4, the batch V contract bundle, this batch's audits — add nodes and,
because `consumer-at-landing` contributes a citation edge per (artifact, governance object)
pair, add citation edges superlinearly against them. Zero edge kinds were added or removed
between the two measurements, which is the part that would signal a graph change rather than a
tree change. Build cost measured at **5.25 s** on this tree — the number ADR-118's
flip-condition 2 asks to be fixed at W-G1, recorded here against the commit gate's budget.

### 1.3 The shape this lane builds

**Persistence.** `scripts/graph_store.py` — stdlib `sqlite3`, WAL, following the
`logs/TELEMETRY.db` precedent exactly (same pragmas, same "the durable signal is what a reader
derives from it, not the file" posture). `rebuild()` builds FPG-1 once and writes `nodes` /
`edges` tables; every query then reads **back from the store**, never from an in-memory build,
which is clause 1's explicit bar.

**Where the store lives — a departure with its reason.** Not `logs/GRAPH.db`: that needs a
`.gitignore` line, and `.gitignore` is **not in this lane's footprint**. The store therefore
lives under the resolved git dir (`git rev-parse --absolute-git-dir`), which is outside the
working tree by construction — so it can never dirty `git status`, never trip session-end
backpressure, and never need an ignore rule. In a worktree that resolves per-worktree, which is
the correct granularity: each worktree has its own tree and therefore its own graph.

**Two new inputs on FPG-1, not a second graph** (ADR-118 §1 — *"a new edge kind is added to
FPG-1, never to a script"*):

- **Input 6, `wiring`** → `triggers` and `imports` edges. Roots are the seven wiring surfaces
  the census names; the script call graph is closed transitively over `scripts/` by `ast`,
  package-qualified, docstrings excluded — the census's own method, moved from a one-time
  audit into the graph where it belongs.
- **Input 7, `task-implements`** → `implements` edges from an **OPEN** `tasks/` row to the
  files it names, and from a file to the OPEN row **its own text names**. Both directions are
  real coverage: a row that names a file claims it, and a module whose docstring names `[#N]`
  is claimed by it. This repo's every script already carries the latter, so the edge is
  computed from a convention that exists rather than imposed as a new one.

**Node classes are DERIVED, never declared.** The row names nodes `script · hook · command ·
skill · task · intake · ADR · file`. `task`, `intake`, `adr` and `file` are existing FPG-1 node
kinds; `script`, `hook`, `command` and `skill` are **not minted as rival node kinds** — a
script *is* a file, and a second vertex for one file is precisely the defect
`PurposeGraph.node_for_path` was built to prevent (Terra pre-merge finding 5, in that method's
own docstring). The process class is a **derivation from kind and path**, which is intake #40
§1's standing rule for exactly this situation: *"layer is DERIVED from kind and path, never
hand-declared on a node"*.

**Three queries, three refusals, three pre-commit hooks.** They are hooks rather than
`ALL_CHECKS` members, and that follows from the footprint rather than from taste: `scripts/audit.py`
and `ecosystem/doc-code-edge.yaml` are both **outside** this lane's declared footprint, and an
`ALL_CHECKS` member needs an edit to each (registration, plus the `# rule:` annotation
`check_doc_code_coverage_drift` requires of every member). The contract hands this lane
`.pre-commit-config.yaml` *"ONLY to add the hooks the three queries need"*, which is the same
answer read from the other side.

| Hook | Refuses when | Trip-test |
|---|---|---|
| `graph-rebuild` | the store cannot be built or read back | corrupt store → non-zero |
| `graph-orphan-census` | a process node has in-degree 0 over `triggers` and is not dispositioned | plant an untriggered script → FAIL |
| `graph-task-coverage` | a **staged** file has no inbound `implements` edge from an OPEN row | stage a file no open row claims → FAIL |
| `graph-process-list` | `ARCHITECTURE.md` names a process the graph lacks (`dangling_reference`) | plant a prose reference to a nonexistent script → FAIL |

Clause 2's bar is read literally in both halves: *"a query that reports without refusing does
not discharge this clause, and a test that passes on conforming input is not a trip-test."*
Each trip-test asserts the **non-zero exit on planted non-conforming input**, and each is
written RED before its query exists (step 2).

**`task_coverage` is a gate that consults a view, and says so.** DECLARE-REVIEWS §A.1
correction 2 rules that two-tree gates cannot be views. The staged-file set is commit-time
state and stays a gate; the `implements` relation is corpus structure and is a query. The hook
is the join, and it is named as a hybrid here rather than mis-filed as a pure view.

### 1.4 The 32-vs-20 gap — ruled (clause 4)

**Ruling: widen the node class to every in-repo process file; the 6 out-of-tree rows are named
with their owner and are unreachable by construction.**

| Census population | Count | Disposition |
|---|---|---|
| A · `scripts/` + plugin scripts | 20 | **In class.** `scripts/**/*.py`, `scripts/**/*.ps1`, `plugins/**/scripts/*.py`. |
| C · commands + skills, in-repo | 6 | **In class, widened.** `.claude/commands/*.md` (`/changelog-review`, `/override`, `/preflight`, `/save`) and `.claude/skills/*/SKILL.md` (`check-against-spec`, `verify`). |
| B · L0 hooks under `~/.claude/hooks/` | 3 | **OUT — unrepresentable.** Three `block-onedrive.SUPERSEDED*.ps1` copies on the operator's disk. Not tracked by this repo, so they are not nodes in a graph of this repo's corpus. Owner: **the operator** — the census already rules this (*"a file deletion in an exclusion-adjacent directory and is the operator's call, not a lane's"*), and the global OneDrive rule makes it doubly not a lane's act. |
| C · commands + skills, L0 | 3 | **OUT — unrepresentable.** `~/.claude/commands/codex-review.md` and the two `~/.claude/skills/gotchas/` files. Owner: **the operator** (L0 is `~/.claude/`, ADR-54's home; this repo authors no rule there). |

**32 = 26 in class + 6 out of tree.** The contract's warning is met head-on: *"32 → 0 against a
20-item predicate is unreachable by construction"* — so the predicate is widened to 26 rather
than the number rounded, and the 6 that a corpus graph of *this repo* cannot see are named with
their owner instead of being silently dropped. Widening is chosen over "give the other 12 their
own queries" because the other 12 split 6/6 across in-repo and out-of-tree: a second query
would still not reach the out-of-tree 6, so it would buy a surface without buying an answer.

**How the 26 reach 0.** Each carries a disposition with a reason and an owner, and any process
node **not** in that register FAILs the commit. That is intake #86's cadence made commit-tier:
the register is the WARN-shape the repo already uses, so no new surface is born. The register
lives in the query module rather than in `ecosystem/disposition-register.yaml` for one reason
and it is the footprint: `ecosystem/` is not this lane's to write. **Follow-up, owed and named:
relocate the register to `ecosystem/disposition-register.yaml` in a lane whose footprint
includes it.**

### 1.5 Clause 3, and what it can honestly reach here

Clause 3 asks the five-kind class (citation · generation · template · test · script call-site)
to be re-measured and driven toward 0. **ADR-118 §5 rules the migration one organ per lane**
(*"twelve lanes is the cost of having twelve proofs"*), and its Alternatives section rejects
the big bang by name. So this lane **measures N and migrates none**, prints N-before and
N-after, and names every remaining site with its owner — which is exactly the branch the
contract writes for the case where 0 is not reachable here. The measurement is step 5.

### 1.6 What this lane will not do

Pinned out and untouched: `BACKLOG.md`, `tasks/`, `tasks/manifest.json`,
`docs/audits/README.md`, `ecosystem/organ-index.md`, `ecosystem/doc-counts.md`, `JOURNAL.md`,
`ecosystem/organ-registry.yaml` (**no rows written into it — that is the defect this lane
exists to end**), `ARCHITECTURE.md` prose, and every other lane's branch. No merge, no push,
no index regeneration; the single-hook bypass a lane is permitted is declared in the commit
body where it is used.

## Steps 2–5 — what landed, and what it measures

### 2.1 The commits

| Commit | Step | What |
|---|---|---|
| `e4cae91f` | 1 | locators resolved, baseline re-measured, plan frozen |
| `6d161e8f` | 2 | RED-first witnesses — a collection error at that commit, which is the witness |
| `da4d1ec9` | 3 | `graph_store.py`, two new inputs on FPG-1, the `graph-rebuild` hook |
| `dd161577` | 4 | `graph_queries.py`, three refusal hooks, the 32-vs-20 ruling |
| `26c9e729` | 4 rider | three defects the spine found by firing, plus one concurrency defect |
| `549f64bd` | — | sync merge: main into the lane tree, clearing the tree-lag anchor gap |
| `874feec3` | 5 | the five-kind re-measurement, and this artifact |
| `cc9b5555` | terra 1 | a waiter must never unlink a lock it does not hold |
| `e7bcb630` | terra 2 | release the ACQUISITION, never the lock filename |
| `d2cfe7c2` | terra 3 | a claim in the TREE is not a claim in the COMMIT |
| `bedae758` | terra 4 | a store that EXISTS is not a store that is FRESH (+ a leaked reader) |

### 2.2 Clause 1 — the graph is persisted, and the counts are read back

```
store    : <resolved git dir>/fpg-graph/FPG.db
nodes    : 2426
edges    : 18590
kinds    : 15
```

Read back by `graph_store.py stats`, which opens the file and answers from it — and
`rebuild()` itself returns `open_store(path).counts()`, so even the writer's own report is a
read-back. Against ADR-118's baseline and this lane's own step-1 measurement:

```
ADR-118:34 (2026-09-07)          1922 nodes   12 664 edges   12 kinds
this tree at step 1 (552997bb)   2001 nodes   13 575 edges   12 kinds
this tree at step 5              2426 nodes   18 590 edges   15 kinds
```

**Both deltas are explained rather than reported.** ADR-118 → step 1 is two days of corpus
growth at ZERO kind change, which is the part that would have signalled a graph change rather
than a tree change. Step 1 → step 5 is this lane's own two inputs: **+3 kinds** — `triggers`
43, `imports` 255, `implements` 4745 — and a node rise that is the process files which now
have a vertex whether or not another input names them. Under DECLARE-REVIEWS §A.1's narrowed
class all three new kinds are corpus-structure: a wiring surface fires a process, a module
calls a module, a row owns a file. **No state gate was migrated into the graph** — the spine
anchor and the staged-ADD checks compare two trees and stay gates, as §A.1 correction 2
requires.

**Cost, measured, and it is the flip-condition's own number.** Rebuild 17.5 s wall / 13.0 s of
graph build, against the 5.25 s five-input baseline. Per loader: `consumer-at-landing` 4.0 s ·
`implements` 3.9 s · `wiring` 3.3 s · `doc-code-edge` 0.9 s · `tasks` 0.8 s. A store read is
~1.5 s, nearly all of it interpreter start — which is why three refusals ride one commit
instead of three builds. Open item 1 below.

### 2.3 Clause 2 — three refusals, live

```
orphan-census : OK   (157 processes, 39 orphans, 39 dispositioned, 0 undispositioned)
task-coverage : OK
process-list  : OK   (118 triggered, 39 not, 0 dangling references)
```

All four hooks ran on this lane's own step-4 commit and passed — the mechanism's first
witnessed firing is its own landing. Each refusal carries a trip-test that plants
non-conforming input and asserts the **non-zero exit**, and a conforming-input test beside it:
a gate that can only fail is not a gate, and one that can only pass is not a refusal.

### 2.4 Clause 4 — the 32-vs-20 gap, ruled and then MEASURED

The step-1 ruling stands — widen the node class, name what is unrepresentable — but the number
it predicted was 26 and **the measurement is 39**. The prediction is corrected here rather than
quietly kept, and every unit of the difference is accounted for:

| | count | note |
|---|---|---|
| census orphans, 2026-09-08 | 32 | 20 script · 3 L0 hooks · 9 commands and skills |
| of those, out of tree | −6 | three `~/.claude/hooks/block-onedrive.SUPERSEDED*.ps1`, `~/.claude/commands/codex-review.md`, two `~/.claude/skills/gotchas/` files. **Owner: the operator.** Not tracked by this repo, so not nodes in a graph of its corpus |
| in-repo, as the census counted | 26 | |
| commands and skills the census ruled ON-DEMAND | +13 | the seven-acts list is a RULING, not a computation — **nothing in a tree fires a command** — so the mechanism finds every in-repo command and skill, and each of the eight the census ruled on-demand is dispositioned with the act it maps to |
| arrivals after the census's cut | +1 | `scripts/gen_ledger.py`, landed 2026-09-09 by lane V-000 |
| found by this query, missed by the census | +1 | `scripts/single_flight.py` — **a finding against the census**, intake #86 AC 2 |
| no longer an orphan | −1 | `scripts/file_purpose_graph.py` acquired the `graph-rebuild` trigger. This row's headline landing, arriving as a dropped row rather than as a claim |
| **measured** | **39** | 39 dispositioned, 0 undispositioned, asserted by a test |

**`orphan_census` reaches 0 against its stated node class after dispositions** — the row's
Done-when. `test_the_live_orphan_census_reaches_zero_against_its_stated_class` is the
assertion, and any process not in the register FAILs the commit.

### 2.5 Clause 3 — the five-kind edge computations, RE-MEASURED

**The digest's enumeration is not in this tree** (§1.1), so N is measured from the tree under a
stated predicate rather than inherited. `ff103444` is explicit that this is owed: *"Whoever
opens the first migration lane re-measures N under the five-kind class and records it with the
measurement."* **The integer 12 is NOT inherited** — the amendment withdraws it because it
counted state gates the class excludes.

**Predicate, stated so the number is reproducible:** a module that **discovers** a
corpus-structure relation of one of the five kinds — citation · generation · template · test ·
script call-site — **by scanning source text**, independently of FPG-1. *Discovery*, not
declaration-following: a generator that reads a registry its input declares is following an
edge rather than computing one, and asking it to query FPG-1 for its own input list would be
circular. Shortlisted mechanically (a module that walks the tree **and** compiles ≥2 regexes),
then verdicted per module.

| Site | Kind | Verdict |
|---|---|---|
| `consumer_at_landing.py` | citation | **RECONCILED** — is FPG-1 input 3; the graph consumes it rather than rivalling it |
| `validate_doc_code_edge.py` | citation | **RECONCILED** — is FPG-1 input 1 |
| `gen_audit_index.py` | citation | **RECONCILED** — its output is FPG-1 input 2 |
| `funnel_coverage.py` | citation | private |
| `funnel_lifecycle.py` | citation | private |
| `validate_doc_rot.py` | citation | private |
| `preflight_contract.py` | citation | private |
| `verify_handoff_probes.py` | citation | private |
| `validate_reconciliation.py` | citation | private |
| `scan_undeclared_edges.py` | citation | private |
| `batch_manifest.py` | citation | private |
| `archive_row_body.py` | citation | private |
| `audit.py::check_doc_claims` | citation | private |
| `codemap/ast_walker.py` | script call-site | private — **closest overlap with this lane's `imports`** |
| `audit.py::check_import_edges` | script call-site | private — same overlap |
| `enforcement_coverage.py` | script call-site | private |
| `reverse_dep_oracle.py` | script call-site | private |
| `generate_organ_index.py` | script call-site | private — **closest overlap with this lane's `triggers`** |
| `dispatch_drift.py` | script call-site | private |
| `proof_layer.py` | test | private |
| `gen_handoff.py` | template | private |

```
N-before   18 private computations (21 sites, 3 already reconciled as FPG-1 inputs)
N-after    18
migrated    0
```

**N did not move here, and the reason is a rule rather than an omission — stated twice over.**
ADR-118 §5 rules the migration **one organ per lane** (*"twelve lanes is the cost of having
twelve proofs"*) and its Alternatives section rejects the big bang by name. Independently, this
lane's frozen footprint is `scripts/file_purpose_graph.py` plus new modules, and **every one of
the 18 sites lives in a file this lane may not edit**. The contract writes exactly this branch:
*"if it cannot reach 0 here, print N-before and N-after and name every remaining site with its
owner."* Owner for all 18: **a W-G3 migration lane, one per organ, each naming its own proof** —
the blanket `diff = 0` bar is withdrawn by §A.1 correction 3.

**What this lane DID move is the precondition.** Three of the five kinds now have an answer in
the graph that no organ had before. `generate_organ_index` and `codemap/ast_walker` can now be
migrated against a relation FPG-1 **holds**, rather than against one a migration lane would
first have to grow — which is the difference between a migration lane and a design lane.

## What the mechanism found by firing

Five defects, every one surfaced by a refusal that fired where it should not have, or by a
test that failed for a real reason. They are recorded because each is a lesson about a class,
not only about an instance.

1. **The disposition register manufactured its own triggers.** `ORPHAN_DISPOSITIONS` is a dict
   whose KEYS are exact process paths; the wiring loader read them as call-site strings, so the
   register that RECORDS "this has no trigger" CREATED one for every row in it — 25
   dispositioned scripts came back triggered and the census's own 20 reported clean. This is
   the process-trigger census's recorded error 1 in a new dress, and an orphan census that
   reports clean is the worst failure it has. Fixed by making *executable position* mechanical:
   a code string counts only inside a `Call` **and** only when it is exactly a path.
2. **A row file is its own claim.** `task_coverage` refused ten staged `tasks/NNN-*.md` rows for
   having no `implements` edge from an open row. `tasks/665-*.md` IS `[#665]`.
3. **A merge is transport, not authorship.** The gate refused a sync merge over files main's own
   commits brought in. Carved out on `MERGE_HEAD` — the precedent `block_commit_on_main` already
   sets — and scoped the same way: the carve-out binds only the git-derived staged set, so a
   merge is a carve-out rather than a hole.
4. **The store's writer was not concurrency-safe.** Five xdist workers collided on one
   `.rebuilding` temp name (`WinError 32`) and paid five concurrent 17 s builds. Concurrency is
   this store's normal condition, so the writer was fixed rather than the callers made careful:
   per-process temp file, a retrying swap (Windows `os.replace` fails while a reader holds the
   destination), and a cheap exclusive-create rebuild lock with a TTL, so a dead builder costs
   one wait and never a wedge.
5. **`rebuild()` leaked a reader on every call.** Clause 1 requires the counts be read back
   from the artifact, and `open_store(path).counts()` did exactly that — and never closed the
   connection. WAL keeps `-wal`/`-shm` open, so each rebuild left a handle that blocked the
   **next** rebuild's swap with `WinError 32`. Invisible in a one-shot hook and fatal in
   anything long-lived. Surfaced only because the Terra pass-4 tests are the first in this
   suite to rebuild the same store twice in one process — *a defect can be latent because
   nothing has yet asked the second question.*

## The Terra pre-merge review

```
HIGH raw=5 fixed=5 unresolved=0
```

Five passes of `codex exec review -m gpt-5.6-terra --base main`, read-only, run to the
contract's stopping rule — *stop when a pass returns nothing*, not *stop after one pass*.
Passes 1–4 returned findings; pass 5 returned **"No critical or high-severity regressions
were identified"**, which is what ended the loop.

| Pass | Finding | Site | Disposition |
|---|---|---|---|
| 1 | a waiter that outlasts the TTL rebuilds **without** the lock, then unlinks the live builder's | `graph_store.ensure` | fixed `cc9b5555` |
| 2 | the release side is unconditional — an overrun builder deletes its **successor's** lock | `graph_store.ensure` | fixed `e7bcb630` |
| 3 | subject set from the INDEX, `implements` relation from the WORKING TREE — a bypass | `graph_queries.task_coverage` | fixed `d2cfe7c2` |
| 4 | a waiter serves a store because it is READABLE, not because it is fresh | `graph_store.ensure` | fixed `bedae758` |
| 4 | `_open` rebuilds only when the file is ABSENT, so every query can answer stale | `graph_queries._open` | fixed `bedae758` |
| 5 | — nothing — | | loop ends |

**Every finding was a real defect and none was argued down.** They fall into one class,
which is worth naming because the class is the lesson: *a property read off the filesystem
that the filesystem does not answer.* A lock file's **existence** does not identify its
holder (passes 1 and 2). A store's **presence** does not mean it is current (pass 4). And a
file's **working-tree bytes** are not the bytes a commit writes (pass 3). Each was written
as though the cheap check were the real one.

**One further defect came out of the tests written for pass 4, not from Terra**: `rebuild()`
ended with `open_store(path).counts()` and never closed the connection, so WAL held
`-wal`/`-shm` and every rebuild left a handle that blocked the **next** rebuild's swap. It is
counted in "what the mechanism found by firing" below rather than in the tally above, because
the tally is a review tally and this was not a review finding. `_swap_into_place` was hardened
in the same pass: clearing the old store's WAL sidecars moved *inside* the retry loop, since
it was the one contended act being performed outside it.

**What the review cost, in the honest direction.** Closing pass 4's second finding means each
query hook now proves the store is fresh instead of assuming it. Re-measured end to end:
`graph-rebuild` 14.6 s, `orphan-census` 2.0 s, `task-coverage` 3.2 s, `process-list` 2.2 s —
**21.9 s for the chain**, up from ~17.5 s. That is a correctness cost paid deliberately; the
alternative on offer was an `--assume-fresh` flag, which is the same hole with a switch on it.
It also moves open item 1 further past ADR-118 flip-condition 2, which is stated there rather
than absorbed here.

## Departures from the contract, each declared

1. **`ORPHAN_DISPOSITIONS` lives in `scripts/graph_queries.py`**, not
   `ecosystem/disposition-register.yaml`. Footprint: `ecosystem/` is not this lane's to write.
   Owed follow-up, open item 2.
2. **The store lives under the resolved git dir**, not `logs/`. A `logs/` store needs a
   `.gitignore` line and `.gitignore` is not in the footprint; the git dir is outside the
   working tree by construction.
3. **Process classes are DERIVED from path, not minted as node kinds.** The row names nodes
   `script · hook · command · skill`; a second vertex for one file is the defect
   `PurposeGraph.node_for_path` exists to prevent, and intake #40 §1's standing rule is that
   layer is derived from kind and path, never hand-declared.
4. **Three pre-commit hooks bypassed across the lane, each named in the commit that used it.**
   `doc-counts-pytest-freshness` and `organ-index-freshness` are generated surfaces the contract
   pins out and routes to the integrator ([#590]). `audit-health` was bypassed on two commits
   for a **proven-false** tree-lag anchor gap — the check's own diagnostic was run, not guessed
   (`anchored in this tree: False`, `anchored at main: True`) — and after the sync merge
   `audit.py health` returns **OK**, which is the verification the bypass promised.
5. **One sync merge of `main` into the lane branch.** Not an integration act and not a merge to
   `main`: it is the recorded fix for the tree-lag class, and the lane still ends
   commit-and-STOP.

## Open items

1. **The four-hook chain costs 21.9 s on every commit** — 14.6 s of rebuild plus 7.4 s across
   three query hooks, each of which now pays an mtime sweep to prove the store is fresh (the
   Terra pass-4 fix; it was ~17.5 s before). ADR-118 flip-condition 2 names the threshold in
   exactly these terms — *"if FPG-1's build time on the live tree crosses the ship-gate's budget
   … the answer becomes a cached/incremental store, i.e. a different design"* — and asks W-G1 to
   fix it against the then-current gate budget. Measured and recorded rather than tuned quietly;
   the dominant costs are three full-corpus sweeps. The named remedy is an incremental rebuild
   keyed on `git diff --cached`, which is a different design and therefore a ruling.
2. **Relocate `ORPHAN_DISPOSITIONS` to `ecosystem/disposition-register.yaml`.** The shape already
   matches; the move is mechanical and needs a footprint that includes `ecosystem/`.
3. **`ARCHITECTURE.md` Ch2 is not yet rendered from `process-list --render`.** The renderer
   exists and the `dangling_reference` refusal is armed; the prose rewrite is pinned out of this
   lane and is step D of the recovery plan.
4. **Two coupled generated surfaces are stale and are the integrator's to regenerate** ([#590]):
   `ecosystem/organ-index.md` (this lane adds four pre-commit hooks) and `ecosystem/doc-counts.md`
   (this lane adds tests and hooks). One test is RED until then —
   `test_generate_organ_index.py::test_live_committed_index_is_the_generated_bytes`.
5. **One inherited RED, not this lane's:**
   `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent`.
   Verified by swapping this lane's `.pre-commit-config.yaml` for `HEAD:`'s and re-running —
   identical failure, so it predates the diff.
6. **The `imports` edge set is not yet proved a superset of `codemap/ast_walker`'s.** That proof
   belongs to the W-G3 migration lane, and it is the one migration this lane's work makes cheap.
