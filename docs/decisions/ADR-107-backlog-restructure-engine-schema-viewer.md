# ADR-107: BACKLOG restructure — build-thin engine, fleet-owned schema, viewer as a replaceable part (slot declared empty)

**Status:** Proposed
**Date:** 2026-07-27
**Decision tier:** Architecture (Path A — authored by CC from on-disk evidence only, on the strength of the operator-delegated tool ruling recorded in `BACKLOG.md` [#433]; **ratification is a separate operator act** and is NOT performed here)
**Related:** [#433] (the carrier — per §7.5 it does not close on this ADR alone) · [#382] (receiver of §5's schema findings) · [#383], [#385] (downstream waves) · [#424] (the `depends-on` bare-vs-hash distinction this schema must preserve raw) · [#429] (worktree provisioning — owner of the concurrent-allocation residual in §6.3) · [#436] (parallel-eligible ratchet build, disjoint files) · ADR-64 / ADR-65 / ADR-66 (the BACKLOG architecture this restructures — none superseded here) · ADR-98 (intake genre) · ADR-101 + its 2026-07-27 amendment (`tasks/` sanctioned as a derived Tier-1 tree) · ADR-104 (fleet repository shape — **landed, not reopened**) · ADR-105 (the gate-at-activation-not-at-filing precedent reused in §3 and §7)
**Intake:** #17 (`docs/intake/2026-07-25-tech-consolidation-decision.md` — D1 and D5 land here; §3 Fibonacci and §4 scoring are named as this ADR's content by intake §5 and are **carried forward, not ruled here**, per §7.4)
**Amends:** ADR-65 (narrow: retained allocation record in tasks/).
**Decommission:** none. Nothing is removed by this decision. `BACKLOG.md` remains the source of truth until the separately-contracted flip (§7).
**Source:** Operator-delegated tool ruling 2026-07-27 recorded verbatim in the `BACKLOG.md` [#433] row (ENGINE = build-thin · VIEWER = Backlog.md piloted as a replaceable part · scrummd rejected as a dependency); pilot-precedes-contract ruling of 2026-07-26 with its three obligations (`docs/decisions/README.md` § "Restructure pilots the pattern before the fleet contract"); genre-lifecycle second leg (`docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` §2(g) and §5 wave 3(b)); spike evidence `docs/audits/2026-07-27-verification-433-schema-spike.md` §1–§5. Adversarial
review: `docs/audits/2026-07-27-codex-adversarial-review-adr-107-sol.md` (Codex sol, 2026-07-27,
reviewed at `fa3f10a3` — verdict RATIFIABLE AFTER EDITS; its five edits E1–E5 are folded into
this document verbatim).

## Context

**The root cause is a data-structure defect, not a size defect.** Recorded verbatim in
`docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` §1:

> BACKLOG.md is not too big, it is the WRONG DATA STRUCTURE. One file serves five workloads
> (work queue, dependency graph, archive, decision register, evidence store). Every defect of
> this window maps to that: the 1200-char ceiling blocks records because EVIDENCE does not
> belong in a queue row; the [E8] R-table rotted because DECISIONS do not belong in a queue
> file; nothing is ever deleted because closing means editing a 170KB file; id collisions
> because the counter is prose, not a directory.

**The 1200-char ceiling collisions are this ADR's own evidence, recorded not compressed
around (n=3, one window).** `docs/handoffs/2026-07-27-dev-knowledge-architect/SUPPLEMENT.md`
Q2, verbatim: *"three 1200-char collisions this window ([#431] twice, [#434] fork ruling
relocated to docs/decisions/README.md decision notes). Ruled: no more compression heroics —
the ceiling is the restructure's own evidence, fix is the format."* A fourth instance is
resident in the spike report itself (`docs/audits/2026-07-27-verification-433-schema-spike.md`
§1 placement disposition): the K1–K5 definitions could not be recorded on the [#433] row —
measured at **1189/1200 characters, 11 characters of headroom** — and overflowed entirely to
the audit report. A queue row that cannot hold the definition of its own acceptance criteria
is the defect stated as plainly as it can be.

**One correction to how those collisions should be read, verified live:** intake #17 §3.2 ruled
the per-file cap to **1597** ("was 1200 — same protective intent, one family"). That ruling has
**not landed** — `scripts/validate_doc_rot.py:58` still reads `_BACKLOG_GROSS_CHARS = 1200`. So
some part of the n=3 pressure is an unlanded-ruling artifact rather than pure format failure,
and a ratifying operator should read it that way. It does not change the structural argument:
raising a row ceiling relocates evidence pressure, it does not remove evidence from a queue row.
Landing (or withdrawing) the 1597 change is **not** in this ADR's scope and belongs to whoever
owns intake #17 §3.

**What is already built and committed (witnessed live at `b4dd3e48`, this session):**
`scripts/gen_task_tree.py` parses `BACKLOG.md` into a lossless per-line model and emits
`tasks/` — 172 task files + `README.md` + `manifest.json` — byte-identically reconstructible
back to the source. The proofs are recorded in the spike §2 (round-trip asserted inside the
parser, a disk round-trip test, a committed-tree coherence test, `--check` regen-and-diff, and
12/12 independent verbatim spot-check probes). The tree is **DERIVED**; `BACKLOG.md` is the
source of truth.

**Witnessed this session, and load-bearing for §7: the coherence gate is NOT armed, and the
tree has already drifted.** `scripts/gen_task_tree.py --check` on `main` (`b4dd3e48`) FAILs
with six problems: task files for **[#435] and [#436] missing**, **[#428] and [#434] content
differs**, `manifest.json` differs, and full-tree reassembly no longer matches the source. The
cause is structural, not accidental: as `ARCHITECTURE.md` Ch5 already records, `--check` is a
*mode* — no pre-commit hook and no `audit.py` check invokes it, so coherence rests entirely on
`tests/test_gen_task_tree.py::test_committed_tree_coherent_with_backlog`, and a `BACKLOG.md`
edit that skips the suite leaves the tree stale at commit time. That is what happened. This
is the empirical basis for making the armed gate a **precondition** of the flip (§7.2), not a
follow-up to it — a derived tree can be stale and merely wrong; a *source-of-truth* tree that
is stale is a corrupted record.

**Fleet shape is settled and is not reopened.** ADR-104 (Accepted 2026-07-24) ruled PARTIAL
fold with corp-monorepo outside it; nothing here depends on or revisits that.

**Evidence base — repo-resident sources only.** This ADR cites only artifacts committed in
this repository. Two named provenance gaps are recorded rather than papered over:

1. **The operator-held 2026-07-21 document is NOT citable.** Its disposition (ingest / fold /
   non-citable) is recorded as an **open** operator question —
   `docs/handoffs/2026-07-27-dev-knowledge-architect/SUPPLEMENT.md` Q4, final bullet. Until it
   resolves, nothing in it is evidence here. (The four `docs/audits/2026-07-21-*` night audits
   are different, repo-resident artifacts and are unaffected by this exclusion.)
2. **Intake #17's own provenance gap**, stated in that document's "Provenance gap, stated
   plainly": the Backlog.md / build-thin / projen comparison and the ETH context-file reading
   were authored in the **v1** brief, which was never ingested. So intake #17's prior-art rows
   cite a source that is not in the repo. This ADR therefore rests the engine choice on the
   **operator ruling** (which is resident) and on the **pilot evidence** (which is resident) —
   never on v1's comparison.
3. **The A–J methodology-intake commissions document is not repo-resident.** Commission H is
   known here only through the pilot-obligations record's own gloss ("id-space and
   decision-record hygiene"), which is what §6.3 discharges. One consequence is flagged in
   §6.3: that record's cross-reference to "the [#427] collision class" does not resolve — the
   live [#427] row is about repo-position-dependent region-template paths, and the A–J map
   that would reconcile it (`D=[#427]`) is not in the repo.

## Decision

### 1. Vocabulary — K1–K5 and SCHEMA COMPOSABILITY are adopted as this ADR's terms

The six criteria defined in spike §1 (operator paste of 2026-07-27; SCHEMA COMPOSABILITY from
the operator-ratified S3d of 2026-07-26) are adopted **verbatim as written there** and are the
vocabulary every later viewer evaluation uses:

- **K1** viewer operates over/beside our files WITHOUT forcing its folder taxonomy (its tree
  confinable to a path we choose, or absent).
- **K2** `[#N]` identity survives byte-exact — no task-N rewrite, no renumbering.
- **K3** foreign frontmatter keys (`serialize-group`, `verified_by`) survive its read AND write
  byte-stable.
- **K4** works on Windows (the fleet's actual host).
- **K5** read surface scriptable (JSON/CLI) consumable without importing its code.
- **SCHEMA COMPOSABILITY** a task record must be expressible as one typed row inside a declared
  desired-state model — identity, status, dependencies surviving as fields among others —
  without requiring its own parallel store.

Spike §1 remains the canonical in-repo record of these definitions (they do not fit on the
[#433] row — see Context). This section binds them as ADR vocabulary so a future evaluation
does not re-derive them.

### 2. ENGINE — build-thin, with a fleet-owned schema (the landed ruling, recorded not re-derived)

The engine decision is **already ruled** and is cited, not re-argued: operator-delegated
ruling 2026-07-27, recorded on the `BACKLOG.md` [#433] row — *"ENGINE = build-thin (per-task
frontmattered `.md`, fleet-owned schema, directory as id counter, validators as enforcement)"*
— and restated as LANDED in `docs/handoffs/2026-07-27-dev-knowledge-architect/SUPPLEMENT.md`
Q2 ("ENGINE build-thin (fleet-owned schema), VIEWER as replaceable part") and Q3 ("Engine
ruling (build-thin) is LANDED"). Reopening it requires quoting the ruling it overturns.

What this ADR adds is the **schema statement** the ruling implies, so that "fleet-owned" is a
checkable fact rather than an adjective. The schema is:

- **Filename** `<id>-<slug>.md`, one file per task id.
- **Frontmatter** carries `id: "[#N]"` **byte-exact** (an opaque string, never a normalized
  integer), plus the derived `status` / `priority` / `size` / `theme` / `story` /
  `serialize-group` / `depends-on` fields; `depends-on` is carried **raw and never
  normalized** (the [#424] bare-vs-hash distinction is live semantic signal).
- **Body** is the task's own text, **verbatim**.
- **Residue carrier**: `manifest.json` holds every non-task prose line in order plus the
  source `sha256`, which is what makes one-file→many-files reversible.
- **Provenance**: every emitted file carries `source:` + `derived: true`, which is what makes a
  marker-gated deletion path safe.

Composability (S3d) is satisfied **on this schema, viewer-independently** — spike §3, final
row: 172 heterogeneous rows all fit one row shape with no parallel store. Whether any viewer
can host that row is a separate question, answered next.

### 3. VIEWER — Backlog.md REJECTED; the slot is a replaceable part and is declared EMPTY

**Backlog.md (MrLesk), pinned `backlog.md@1.48.0`, is REJECTED as the viewer** on the labelled
K1/K2/K3 evidence of spike §3 (piloted against a byte-copy of the real `tasks/` tree in a
scratch prefix outside the repo; the real repo verified byte-clean throughout):

- **K1 FAIL** — `backlog task list --plain` over our root `tasks/` returns `No tasks found.`
  (rc=0) and `backlog config list` exposes no key to point it at another tree. Its footprint is
  confinable (one `backlog/` dir) but it operates only on its own tree in its own schema: it
  cannot operate *over* our files at all.
- **K2 FAIL** — our schema files copied *into* `backlog/tasks/` are still invisible to it; its
  native id grammar is `task-N` with a **read-only** prefix. Adopting it as the viewer would
  require exactly the forbidden task-N rewrite.
- **K3 FAIL** — `serialize-group` and `verified_by` injected into one of its native files are
  **dropped** by a single viewer write (`task edit -s`): it re-serializes from its internal
  model and discards unknown frontmatter.
- K4 PASS (Windows), K5 PASS with a recorded limit (`--plain` text, **no JSON flag anywhere**).

**This is the cheap valid result the split was designed to buy.** Because the engine is ours
either way (§2), the viewer bet could lose at zero architectural cost — and it did. The loss
costs the architecture nothing, which is the whole point of separating the layers.

**Successor decision, made here rather than deferred outside this ADR: no viewer is adopted,
and the slot is declared EMPTY — not vacant-pending-search.** Basis, all on disk: Backlog.md
FAILs three criteria (above); **scrummd is REJECTED as a dependency** (bus factor 1, 0.2.x-dev
— pattern reference only; `docs/handoffs/2026-07-27-dev-knowledge-architect/SUPPLEMENT.md` Q3),
and the open question intake #17 §4 raised about its GPL-3.0 + single-author risk is thereby
moot; no third candidate has any evidence in this repo. No viewer search is scheduled, and the slot is
PARKED EMPTY behind the re-entry criteria below. This does not claim that the requested
top-five ready-set or overdue-ruling read surface already exists: `gen_task_tree.py` currently
supplies generation, coherence checking, round-trip verification, and pruning only. The graph /
`READY.md` reader surface remains separately owned work and must name its consumer before
activation under ADR-105.

**Re-entry criteria (a candidate enters only by satisfying all four):**
(a) passes **K1, K2, K3** and **SCHEMA COMPOSABILITY** against a scratch copy of the real tree,
by the spike §3 method, recorded in a dated verification artifact; (b) passes K4, with any K5
limit stated; (c) accepts the swap-out contract of §4 in full; (d) names its **consumer** — the
ADR-105 activation rule applied to viewers: a viewer whose output nobody reads is [#419] with a
dependency attached. A candidate failing any of these is recorded as rejected with its evidence
and does not enter.

### 4. SWAP-OUT CONTRACT — what the gate must pin so the viewer stays replaceable at zero cost

Adopted from spike §3 (hazard inventory) and §4, and binding on any future adoption:

1. **Version pin.** Any adopted viewer is installed at an **exact** version, in a prefix
   **outside the repo**; the pin is recorded in the adopting ADR and re-verified by the K1–K5
   probes on **every** bump. (Precedent: `backlog.md@1.48.0` in this pilot.)
2. **Write bar — the viewer is READ-ONLY over `tasks/`.** Basis: K3 witnessed. Until a viewer
   proves unknown-key round-trip byte-stability, its write verbs are barred. Named hazard
   organs from the spike's inventory: `edit` (re-serializes), `doctor` ("safely repair
   duplicate task IDs" — an id-rewriting organ), `cleanup` (age-based file moves — taxonomy
   forcing), `autoCommit` (off by default, but it *can* commit), `init --check-branches
   --include-remote`, and the default-on agent-instruction writers.
3. **The gate is ours, with an honest scope split.** `gen_task_tree.py --check` (regen-and-diff
   plus full disk reassembly) and the byte-identity suite RED any drift of the tree **relative
   to the current source**. They do **not** detect a consistent rewrite of source and tree
   together, because `--check` derives its expectations from the current source. Source
   integrity is therefore a **separate contract leg**: a viewer run must leave `git status`
   clean on the source file (the independent committed baseline the spike itself used), and
   `manifest.json`'s `source_sha256` pins which source bytes the committed tree derives from.
   The schema of §2 is fleet-owned: a viewer consumes it as-is or is not the viewer.
4. **Replacement procedure.** Swap the scratch-prefix install; re-run the K1–K5 probes against
   a scratch copy of the real tree (~30 min by the §3 method); record verdicts in a dated
   verification artifact. **The engine, tests, tree, and this ADR need zero changes** — that
   independence is the definition of "replaceable at zero architectural cost", and it is the
   clause a future session should test this decision against.
5. Mechanical activation gate. While the viewer slot is EMPTY, no viewer is active. A future
   viewer adoption does not take effect until the same change lands (a) a machine-readable
   declaration of package, exact version, read-only command surface, and external
   install-prefix requirement, and (b) an `audit.py` `task_viewer_contract` ship-gate leg
   that FAILs unless the installed version matches the declaration, the prefix resolves
   outside the repository, the K1–K5 verification artifact identifies that exact version,
   and a viewer probe leaves `BACKLOG.md` and `tasks/` byte-clean. Prose evidence alone
   cannot activate a viewer.

### 5. Seven schema findings routed to [#382] — owed either way

The findings of spike §5 are hereby **routed to [#382]** (Desired-state data model: intake →
ADR) as inputs to the fleet desired-state contract. **This routing is owed regardless of
whether or when this ADR is ratified**: it discharges pilot obligation 1, which binds on the
pilot having *happened*, not on this ADR's status. If this ADR is rejected or superseded,
[#382] still receives all seven, and this section is the record that it must.

1. **Identity is an opaque, byte-exact string field** (`"[#433]"`) — never a normalized integer
   or tool-native id. The contract's identity column must be declared *preserve-verbatim*.
   (Witnessed limit, kept: Backlog.md *ignores* `[#N]` records; the re-keying is a consequence
   of adopting its schema, not an in-place re-key that was observed.)
2. **Unknown-key survival is a WRITE-path property and must be an explicit contract clause** —
   a consumer that serializes from an internal model drops what it does not know (K3). Per
   surface, the contract says either "consumers round-trip unknown keys byte-stable" or
   "third-party writers barred". Silence here is silent data loss.
3. **Typed-row composability holds on real data**, precisely stated: a **frontmatter-typed row
   over a verbatim body, with a manifest carrying document residue** — not a frontmatter-only
   representation. [#382] should model all three parts.
4. **Preserve-raw beats normalize-at-ingest** — `depends-on: "270"` vs `"#270"` is live
   semantic signal ([#424]). Carry values verbatim and validate in a separate lane, or the
   migration itself becomes an undetected behavior change.
5. **Provenance markers enable safe lifecycle mechanics** — `derived: true` + `source:` are what
   made a marker-gated retirement path safe. The contract should standardize a provenance field
   pair for **every** derived surface. (Second leg of the same finding, from spike §7.4: a
   derived surface must be invisible to prose-edge organs **as a class**, or every derived tree
   re-mints every declared edge — witnessed as 12 double-reported `undeclared_edges` WARNs,
   fixed structurally by excluding the derived dir, not by 12 register rows.)
6. **A split needs a residue carrier** — the manifest (ordering + non-member prose + source
   hash) is what makes one-file→many-files reversible and gateable. Any [#383] wave that
   decomposes a monolith surface budgets the same artifact, or reversibility is lost at step one.
7. Directory-as-id-counter: substrate built, allocation rule not built. The tree supplies one
   filesystem representation per live id and duplicate-id refusal, but no next-free
   calculation, retirement-completeness rule, or concurrent-allocation probe was built. [#382]
   must therefore receive allocation-ledger completeness, retirement semantics, duplicate-id
   enforcement, and concurrent-branch collision behavior as explicit desired-state contract
   inputs. Section 6.3 may rule this surface's local mechanism, but it does not absorb or
   discharge this seventh [#382] input.

### 6. Pilot obligations — dispositions, one by one

The three obligations of the pilot-precedes-contract ruling (`docs/decisions/README.md`
§ "Restructure pilots the pattern before the fleet contract", operator ruling 2026-07-26) are
folded here with an honest status each.

**6.1 Obligation 1 — feed schema findings into [#382]: DISCHARGED** by §5 above (seven
findings, routed, owed either way).

**6.2 Obligation 2 — the generalization clause ("the pattern must be *shown* to extend to at
least one other governed surface. Shown, not asserted"): NOT DISCHARGED, and deliberately not
asserted.** One surface has been piloted end-to-end; a second has not. This ADR does not claim
generality it has not earned. Discharge criteria, fixed here so the obligation is checkable
rather than remembered:

- **What counts:** a *second* governed surface split by the same engine pattern — per-item
  frontmattered `.md` files with byte-exact identity, a residue manifest, and a green
  regen-and-diff round-trip — demonstrated by a committed round-trip proof, not by argument.
- **Named candidates, in order of cheapness:** `docs/intake/*.md` (already frontmattered with a
  `status:` enum and already carrying a generated status-grouped index) and the `[E8]`
  ruling/decision register (the surface whose rot in a queue file is a named motivation for
  this restructure).
- **Owner and sequencing:** the [#383] execution waves ("converge each L0/L2 surface … one wave
  at a time"), whose first wave should be chosen to satisfy this clause. **This obligation is
  NOT a precondition of the §7 flip** — the flip's preconditions are exactly the two in §7.2 —
  but it **is** a precondition of [#382] declaring the fleet contract *general*, which is the
  form the original ruling gave it.

**6.3 Obligation 3 — RULED, NOT YET STRUCTURALLY DISCHARGED; narrow ADR-65 amendment
required.** For the post-flip task store, ADR-107 explicitly amends ADR-65: a task leaves the
active queue, but a minimal allocation record retaining its opaque id and terminal status
remains within the lifecycle-managed `tasks/` tree. Git and JOURNAL remain the full technical
and business records. This retained allocation record is a narrow exception to ADR-65's
no-archive-file and no-new-per-item-write rules. Commission H is structurally discharged only
when retire-not-delete behavior and the duplicate-id ship gate are implemented and witnessed.

**Witnessed live this session, on `main` at `b4dd3e48`:**

- highest id present in `tasks/` = **434**; highest bracketed id in `BACKLOG.md` = **436** —
  the tree already lags the source (§Context: the unarmed gate).
- highest bracketed id across **all** git history = **777**, which is a **known synthetic
  trip-test artifact** that a prior session had to exclude by hand (recorded in that session's
  own commit message: *"synthetic [#777] in trip-test prose excluded as false positive"*).
  Excluding it, the true maximum is **436** and next-free is **437**.

The second witness is the point: **the prose/history scan is already defeatable, and has
already had to be defeated by hand.** That is the concrete form of the "counter is prose" defect.

**The rule (normative):** `next_free = max(id parsed from tasks/<id>-<slug>.md) + 1`, valid
**only** while the directory is a complete ledger of every id ever allocated. It is not complete
today, for one structural reason: ADR-65's done-items-leave, realized by the generator's
marker-gated `--write --prune`, **removes a retired task's file**, so a closed id vanishes from
the directory and becomes re-allocable. Therefore:

- **Duplicate-id detection is the enforcement**, and it already partly exists: the generator
  refuses duplicate ids at parse. At the flip, a `tasks/`-level duplicate-id check makes a
  collision a **gate failure at merge time** rather than a silent one.

**Residual hole, stated rather than claimed away:** a directory counter does **not prevent** two
concurrent branches allocating the same next-free id — both read the same maximum and each
writes a differently-slugged filename, so git merges them cleanly with a duplicate id. What the
directory buys is (a) a deterministic, greppable counter that cannot rot in prose and needs no
hand-maintained pointer, and (b) a collision that is **detectable by a gate** instead of
discovered later. Prevention of concurrent allocation is **not** claimed by this ADR and is left
with the worktree/session-provisioning lane ([#429] and the filed-not-built HEAD-swap
mechanisms enumerated in the 2026-07-27 SUPPLEMENT Q6 carried debt).

**Cross-reference defect, flagged for the ratifying operator:** the pilot-obligations record
cites "the [#427] collision class", but the live [#427] row is about repo-position-dependent
region-template paths, and the A–J methodology-intake map that would reconcile it (`D=[#427]`,
per the 2026-07-26 SUPPLEMENT §5) is **not repo-resident**. The obligation is discharged above
on its substance; the citation is recorded as unresolvable in-repo rather than silently
repeated.

### 7. Strangler scope — what this ADR does NOT authorize

Intake #17 D5 fixed the migration sequence: **verbatim split → byte-stable round-trip proven →
source-of-truth flip → then prose relocation.** Steps 1–2 are built and committed. This ADR
rules the architecture; it authorizes **no execution**.

**7.1 What is already done.** Steps 1–2 (`scripts/gen_task_tree.py`, the derived `tasks/` tree,
the byte-identity proofs) landed with the spike. `BACKLOG.md` is the source of truth today.

**7.2 Step 3 — THE FLIP is a SEPARATE CONTRACTED EXECUTION.** The flip is: `tasks/` becomes the
source of truth, `BACKLOG.md` becomes generated, and the gates flip read direction. It is
**conditional on both** of the following, and on nothing less:

- **(i) this ADR is Accepted** — by an operator act, in a separate session; and
- **(ii) the `tasks/` coherence gate is ARMED** — an `audit.py` ship-gate leg invoking
  `gen_task_tree --check`. As witnessed in Context, this gate **does not exist today** and the
  tree is **already drifted**, which is precisely why arming precedes flipping: a stale derived
  tree is merely wrong, whereas a stale source-of-truth tree is a corrupted record. Arming is
  itself a code arc, separately contracted, and is not authorized by this ADR.

**7.3 Step 4 — prose relocation is EXPLICITLY DEFERRED to post-flip, owner = a later arc.** The
944→≤233-character body relocation (intake #17 D5 + §3.2's Fibonacci-family target) runs as
ordinary edits on the new format, **after** the flip, via the **propose-only migration lane**:
an LLM receives each over-length body and proposes a three-way split (stays under the ceiling /
relocate as an evidence link / dead candidate), each proposal quoting its source; a
**deterministic verifier confirms the quoted text exists**; the **operator ratifies in batches**
(`docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` §2(f), which applies intake
#17 §2's propose-only doctrine to the migration — the LLM does what grep structurally cannot and
can break nothing). The genre-lifecycle second leg (§2(g) of the same record; named as the
restructure's SECOND LEG) belongs to this post-flip phase: one schema for every genre, `status`
in frontmatter ⇄ folder, a validator that FAILs the mismatch, and a command that moves the
file — mechanizing the 2026-07-22 archive-inside-each-folder ruling, which is correct but manual
and therefore never runs. The record's own warning is adopted as this ADR's position: **per-task
files WITHOUT this leg would be the same rot in smaller packages.** Its ADR-transition half may
use `pyadr` off the shelf; that is a later evaluation, not a decision here.

**7.4 Carried forward, not ruled here.** Intake #17 §3 (the Fibonacci doctrine and its stated
non-applications) and §4 (the scoring form, `unblock_count` as its own exact column,
event-driven re-scoring, sticky operator override, `verified_by` mandatory) are named by intake
§5 as this ADR's content. They are **schema-compatible with §2 and unruled here**: they describe
*fields and their semantics*, which land when the fields land — at the flip and in the graph/
`READY.md` layer that follows it — and ruling them now would authorize scope this session is
explicitly denied. A ratifying operator who wants them bound in this ADR should say so; the
alternative is a short successor ADR at the flip.

**7.5 [#433]'s closure language.** [#433] does not close on this ADR alone. This ADR records
the generalization acceptance clause and assigns its second-surface proof, but §6.2 correctly
states that the proof does not yet exist. [#433] remains open until that obligation is
demonstrated, or until the operator explicitly amends [#433]'s Done-when; an explicit
non-discharge is a disposition, not a discharge. **The remaining steps are NOT [#433]'s and must be
carried by their own tickets:** (a) arm the `tasks/` coherence gate — condition (ii) above;
(b) the flip itself — step 3; (c) prose relocation via the propose-only lane — step 4;
(d) the genre-lifecycle engine — the second leg; (e) the generalization clause's second surface
— §6.2, sequenced inside [#383]; (f) the graph / `READY.md` / boot-probe layer that the intake's
exit test actually measures. None of (a)–(f) is authorized by this ADR.

## Consequences

**Easier.** The evidence/queue conflation stops being a wall: an evidence-bearing record no
longer has to fit in a 1200-character queue row, which is the defect this window hit four times.
Identity becomes a filesystem fact rather than a prose scan, and the [#777]-style hand-exclusion
disappears. A viewer becomes disposable — a losing bet costs the architecture nothing, which is
what let this pilot fail cheaply. Closing a task stops meaning editing a single 204,415-byte
file (measured this session; 201,468 bytes at the spike, so the source is still growing).

**Harder / newly owed.** Two coupled surfaces must stay coherent, and the *only* thing making
that true today is a test — the gate is unarmed and the tree is already drifted, so arming is
now a precondition rather than a nicety. A retained-retirement rule (§6.3) means `tasks/` grows
without bound, deliberately: it is an id ledger, and a ledger with holes is not one. The
concurrent-allocation hole is *narrowed and made detectable*, not closed. And per-task files
without the genre-lifecycle leg would relocate the rot rather than remove it, so the second leg
is load-bearing rather than optional.

**Cost of being wrong.** The engine is **459 lines** (`scripts/gen_task_tree.py`) plus **244
lines** of tests — the smallest thing that could have produced this evidence. If the schema is wrong, `manifest.json` +
byte-identity make the split reversible to the source bytes. That reversibility is the actual
deliverable of steps 1–2, and it is what makes ratifying this ADR a low-consequence act.

## Alternatives considered

- **Adopt Backlog.md as the engine.** Rejected on evidence, not preference: K1/K2/K3 FAIL
  (§3). It cannot read our schema in place or in its own directory, its id grammar is `task-N`
  with a read-only prefix, and its write path drops foreign keys. Kept as a **pattern donor**
  (per-ticket file, directory-as-counter), which is how intake #17 already classified it.
- **scrummd as an imported dependency.** Rejected: bus factor 1, 0.2.x-dev (`SUPPLEMENT.md`
  2026-07-27 Q3) — pattern reference only. Intake #17's open GPL-3.0 question is moot as a
  result.
- **Adopt no viewer but keep the slot "pending a search".** Rejected as decoration: an open
  slot with no candidate, no criteria, and no scheduled search is a recurring re-litigation.
  §3 declares it **empty with re-entry criteria** instead — a state a future session can test
  against rather than reopen.
- **Big-bang migration** (all 172 rows at once). Rejected by intake #17's adoption of the
  strangler pattern; the four-step sequence with a proven byte-stable round-trip is the whole
  reason the tree can exist on `main` today without risking the source.
- **Flip now, arm the gate afterwards.** Rejected on this session's own witness: the tree
  drifted while it was merely derived. Flipping first would make that same drift a corrupted
  source of truth.
- **A managed id-counter file.** Rejected upstream ("a managed id-counter file (the directory is
  the counter)", 2026-07-26 SUPPLEMENT §3) and not reopened; §6.3 supplies what the directory
  needs to actually be that counter.
- **Terraform as the tool.** Rejected upstream (pattern yes, tool no — git is the state store);
  the desired-state *model* is [#382]'s, and §5 feeds it.
