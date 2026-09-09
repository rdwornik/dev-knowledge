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
