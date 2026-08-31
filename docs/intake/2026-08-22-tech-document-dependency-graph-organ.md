---
intake-id: 40
status: DRAFT
origin: cloud-graph lane artifact docs/audits/2026-08-21-technical-graph-and-workflows.md (Track A), routed here by the wave-close funnel table docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md lines I1/I2; architect ruling A5 of 2026-08-22 approved the R-A scoping and directed execution to ride this intake
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
note: Filed as an intake rather than as a backlog row BECAUSE the source lane asked for a row directly and ADR-111 section 2 forbids that — the only path from a finding to a row runs through intake and ratification. The lane's specified shape is carried below rather than re-derived, so ratification loses nothing by the detour.
---

**NOTE 2026-08-29 (TYPED MULTI-LAYER GRAPH — the scope this intake gains; still NO carrier row):**
operator direction of 2026-08-29 extends the organ from a **document** dependency graph to a
**typed, multi-layer** one. **Layers:** code · docs · backlog · intake/ADR · **L0** (the global
`~/.claude` and per-repo `.claude/` surfaces — see intake **#62**, filed the same day, which
cross-references this doc rather than duplicating it). **Cross-layer edges are first class**, not
a later join. **Architectural attributes become node metadata:** performance, availability,
reliability, security, maintainability, extendability, modularity, reusability, readability,
testability — the operator's thesis vocabulary, recorded here as the attribute set rather than as
a schema. **Library-first binds Open question 1 rather than answering it:** three named candidates
— **GitNexus**, **repo-graph**, **Code-Graph-RAG** — enter as **ADR-112 Tier L** adoptions, so each
is **fit-assessed against the existing measurement BEFORE any adoption**. None of the three
appears anywhere in this tree today (grep: zero hits), so this is a first naming, not a
re-litigation; and the already-ruled `rustworkx`-not-`networkx` choice (R-A) is untouched, because
that question is *which* and this one is *whether*.

**The first slice already exists.** Wave-2 lane M shipped `scripts/file_purpose_graph.py` with a
working `why` verb (`docs/audits/2026-08-29-technical-nb2-m-packet.md`), and both its own
candidates C-1/C-2/C-3 and the wave-close packet's cross-layer finding route to *"lane M's next
slice"*. The multi-layer extension therefore has a running base, not a blank page.

**NO CARRIER ROW IS BORN HERE, deliberately.** This doc's own Status section records its carrier
as unborn under ruling D5 — *"birth priority (2) when it ratifies"* — and P-2's anti-orphan rule
binds at ACCEPTED. Birthing one now would invert the exact ratification order this file exists to
respect.

**A conflation, recorded rather than corrected in place.** The brief carrying this direction cited
*"FPG-1 / `[#383]`"* as one object. They are two: `[#383]` is **Execution waves per surface**
(parity-surface convergence over `kind: gitignore-effect` rows) and FPG-1 is lane M's file-purpose
graph. Intake #23's P3 line *"networkx STANDS for `[#383]` v1"* carries the same conflation — its
subject is the graph in `[#382]`, which is closed.

# A document dependency-graph organ for this corpus

## Problem / motivation

Nobody can answer "what breaks if I move this document?" without reading the corpus by
hand. The repo has 1,982 tracked `.md` files carrying 13,207 unique repo-shaped
references between them, and **1,230 of those reference targets do not exist** — but the
only thing that has ever produced that number is a scratch script in a cloud lane that is
not in the tree. Three standing needs currently have no substrate:

- **Dependency management** — the named consumer. Before moving or renaming a doc, know
  what cites it, transitively.
- **Orphan detection** — which actionable documents nothing points at any more.
- **Dead-target listing** — `[#534]` needs exactly this feed, and today would have to
  build its own extractor to get it.

The itch is sharpest at rename time, and this window produced a live example: ADR-114
priced a `VISION.md` → `README.md` substitution and had to establish by grep that **0 of
1,956 references are markdown links**, which is why nothing can currently detect a stale
canonical-doc reference. That measurement was hand-rolled for one decision and is not
repeatable by anyone else.

If this stays unaddressed, every structural question about the doc corpus stays a one-off
grep whose method dies with the session that ran it.

## Scenarios (+1 view)

- As the operator, I am about to move `protocols/HANDOFF_PROCESS.md`, and I ask what cites
  it transitively **before** the move rather than discovering it from a broken locator in
  an immutable handoff bundle three weeks later.
- As the architect, I ask which actionable documents nothing references any more, and get
  a list scoped to the corpus a human may actually edit — not one dominated by immutable
  audits nobody may touch.
- As `[#534]`, I need every `path:LINE` locator whose file does not exist, and I read it
  off an existing edge table instead of building a second extractor that will drift from
  the first.
- As a reviewer of this repo's structure, I ask whether the doctrine files form reference
  cycles — and get an answer scoped to the files a cycle could actually be a problem in.

## Functional requirements

- **Must:** answer reverse-reachability ("what cites this, transitively") over the tracked
  `.md` corpus; list orphans; list dead targets; be scoped by corpus bucket, with the
  **actionable** corpus as the default on every query that can be scoped.
- **Must:** capture the `:LINE` suffix as an edge attribute rather than discarding it —
  that is the column `[#534]`'s gate reads, and dropping it makes the organ useless to its
  first consumer.
- **Must:** derive its prune predicate from the live `scan_undeclared_edges.py` rule rather
  than copying its literals. A second copy drifts, which is the failure `CLAUDE.md` §5
  rule 6 exists to prevent — and the very failure the doctrine cycles in this corpus exist
  to avoid.
- **Should:** be a standalone operator-invoked command, not an `audit.py health` check. The
  consumer is interactive (asked before a move), `audit.py health` sits on the commit path
  at a measured ~22 s, and the `CHECK_ORDER` registry is a byte-identical output contract
  that git hooks depend on.
- **Should:** refuse to answer from a stale cache — stamp the tree SHA at build time and
  refuse on mismatch, rather than answering confidently from yesterday's corpus.
- **Could:** offer cycle/SCC and centrality queries — see Open question 1. These are the
  only two queries that need a graph library, and they are explicitly **not** required by
  the named consumer.

## Acceptance criteria (ex-ante)

1. `impact <path>` returns the transitive reverse-reachable set for a document whose citers
   are known by hand, and the set matches.
2. `dead --with-lines` emits `path:LINE` pairs for targets that do not exist, in a form
   `[#534]` can consume without re-parsing prose.
3. `orphans --bucket actionable` excludes immutable audits, ADRs and append-only files, and
   a fixture proves the prune came from the live `scan_undeclared_edges` predicate rather
   than a copied literal — changing that predicate changes this answer.
4. The extractor is **fixture-tested against a probe file in the shape of the Trial-C
   fixture**, not eyeballed. It must not match version strings (`v1.3.1`), dotted
   identifiers (`audit.py::ALL_CHECKS`), or `owner/repo/.github/workflows/x.yml`
   references — all of which "have a slash and an extension". This is not hypothetical: the
   `[#430](a)` citation grammar already parsed as CommonMark link syntax and produced 6 of
   6 of lychee's actionable findings.
5. A **floor assertion on total edges extracted** fails the build if extraction silently
   stops matching a form. Without it, a regex that quietly breaks makes every query
   *quieter* — orphan counts fall, impact sets shrink — and a shrinking finding count reads
   as improvement.
6. Every query refuses rather than answers when the store's tree SHA does not match the
   working tree.

## Non-goals

- **Not a gate.** Ruling A5 approved report-only scoping; funnel line R3 records the
  measured rejection of arming a WARN or FAIL leg on cycle count, and that rejection is not
  reopened here.
- **Not a replacement for `[#534]`.** Disjoint classes: `[#534]` asks whether a prose
  `path:LINE` locator resolves to its named construct — a semantic claim about a line
  number. This organ knows only that an edge exists. It is `[#534]`'s substrate, and
  `[#534]` must **not** block on it.
- **Not markdown-link rot** — that is `[#573]`'s lychee gate, on a corpus where 0 of the
  references are links at all.
- **Not a reordering or rewriting of any document.** Read-only over the corpus.

## Impact sketch (4+1 lite)

- **Logical:** a new `scripts/doc_graph/` namespace sub-package (matching
  `scripts/audit_checks/`, which deliberately carries no `__init__.py`); a gitignored
  sqlite store; no change to any existing organ.
- **Process:** an operator-invoked query, asked before a structural move. Nothing fires it
  on a schedule or a gate, by design.
- **Development:** ~370–490 LOC for the SQL-only phase, of which the extractor is ~35% and
  is the part that has to be right — everything downstream inherits its errors.
- **Physical:** zero new dependencies in phase 1. Phase 2 is where that changes, which is
  why the phases are separated at all (Open question 1).

## Open questions

1. **Does the graph-library phase happen at all, and on what evidence?** The source lane's
   own measurement is the awkward one, and it is recorded rather than softened: the named
   consumer (dependency management) is served **entirely by the SQL half** at zero new
   dependency, and the two queries only a graph library can serve — SCC and pagerank — are
   exactly the two with **no demonstrated yield**. SCC measured **0 real findings out of
   18**; for pagerank nobody has asked a question. Under ADR-112 this is a **Tier L**
   adoption (a library in the fleet's distribution path, evaluated on numbers), so it needs
   a demonstrated query before it earns its dependency. The library choice is already
   ruled — **rustworkx**, networkx not reconsidered — so this question is about *whether*,
   never *which*.
2. **Is rustworkx installable under the pinned `uv`?** `pyproject.toml` pins
   `required-version = "==0.11.19"` and **every Python candidate in the source research was
   trialled outside it**. This is the first act of any phase-2 adoption, and it is a
   one-command check, not a study.
3. **Does it work on Windows?** Unverified. rustworkx ships wheels, but no Windows run was
   done, and this repo is Windows-developed.
4. **How is the bucket taxonomy kept honest as the tree grows?** The answer changes by **9×
   (18 → 2)** depending on the prune, so the taxonomy is load-bearing, and a new
   `docs/<genre>/` folder would silently default to `actionable` and pollute every result.
   Requirement 3 names the mitigation; whether it is sufficient is a technical-architect
   question and is deliberately not answered here.
5. **Does the `dead --with-lines` leg belong in `audit.py health` as `[#534]` specifies,
   even though the rest of the organ deliberately does not?** The source lane says yes and
   treats it as `[#534]`'s leg rather than this organ's. Recorded, not settled.

## Status

DRAFT — filed 2026-08-22 from the cloud-graph lane's Track A findings under funnel lines
I1/I2, per architect ruling A5 (direction approved as scoped by R-A: SQL keeps
reachability, orphans and degree; the library must **earn** cycles and SCC). Awaiting
technical-architect triage. **Its carrier row is deliberately unborn** — ruling D5 lists it
as birth priority (2) *"when it ratifies"*, and P-2's anti-orphan rule binds only at
`ACCEPTED`, so filing a carrier now would invert the ratification order this intake exists
to respect.

## AMENDMENT — 2026-08-31: THE TYPED MULTI-LAYER DESIGN — layers, node metadata, cross-layer edges

> **Source:** batch-E lane DM-3 (`worktree-lane-g-7-typed-multi-layer-graph`), frozen as a
> **DRAFTING lane** by the batch cut precisely because this intake is `status: DRAFT` and carries
> no carrier row — ADR-111 §2 forbids a lane birthing one. **This amendment builds nothing, births
> no row and changes no status.** DRAFT BINDS NOTHING; the design below is recorded for
> ratification, and ratification is the operator's act.
>
> **The lane's own row citation was REFUTED at freeze, and the refutation is recorded here because
> this file is the subject's real home.** The batch brief routed DM-3 to `[#615]`. `[#615]` is
> **MODEL ATTRIBUTION** — a model+version commit trailer, from intake #50 — and is a different
> subject. No `tasks/` row mentions FPG, typed layers or architectural attributes at all; the graph
> has no backlog row in any form, deliberately. Full finding:
> `docs/audits/2026-08-31-technical-batche-launch-contracts/PLAN.md` U-13.

### 0 · The finding that reframes the design: the graph is ALREADY cross-layer

The 2026-08-29 note above states *"cross-layer edges are first class, not a later join"* as the
scope this intake gains. Measured against the live tree, that is not a scope gain — it is a
**description of what lane M already shipped**.

Measured 2026-08-31 in this lane, `scripts/file_purpose_graph.py` over the working tree
(`python scripts/file_purpose_graph.py stats`, plus a throwaway layer-partition script re-runnable
from the layer function in §1):

- **1,758 nodes · 11,309 edges** across the five inputs.
- Applying §1's layer function: **9,873 of 11,309 edges (87.3%) already cross a layer boundary.**
  Only 1,436 do not.

So the design act is **not** adding cross-layer edges. It is adding a **type** — the graph carries
the edges and cannot name the layer, so every layer-shaped question ("what in the docs layer does
the backlog depend on", "what in code is governed by a doctrine file") is answerable only by
re-deriving the layer from the path at each call site. **This amendment inverts the note's own
framing, and records the inversion rather than smoothing it.**

**One honesty caveat, stated because it changes what the number means.** 9,475 of the 11,309 edges
(83.8%) are a single kind — `cites`, from the `consumer-at-landing` input — and they run
`docs -> backlog` (5,816) and `docs -> intake/ADR` (3,761). The graph is cross-layer, but it is not
yet cross-layer **broadly**: the entire code<->docs axis is 45 edges (`enforces` 29, `declared-in`
16), a ratio of roughly 1:130 against the docs->backlog axis. The code layer's problem is not only
missing nodes (§2); it is the near-total absence of a whole **class** of cross-layer edge.

### 1 · The layer function — DERIVED, never declared

The operator's five layers map onto the seven node kinds `file_purpose_graph.py` already defines
(`NODE_FILE`, `NODE_RULE`, `NODE_TASK`, `NODE_ADR`, `NODE_INTAKE`, `NODE_CARRIER`,
`NODE_COMPONENT`) plus one path predicate. No new node kind is required:

- **backlog** <- `NODE_TASK`
- **intake/ADR** <- `NODE_ADR`, `NODE_INTAKE`
- **code** <- `NODE_FILE` whose path is under `scripts/` or `tests/`
- **L0** <- `NODE_FILE` whose path is under `.claude/` (in-repo), and — subject to §4's boundary
  and intake #62 open question 3 — under `~/.claude` (out-of-repo)
- **docs** <- every other `NODE_FILE`

**Layer is DERIVED from kind and path, never hand-declared on a node.** A `layer:` key written onto
a node is a second copy of a fact the node already carries, and a second copy drifts — the failure
`CLAUDE.md` §5 rule 6 exists to prevent, and the same failure this intake's own **requirement 3**
already guards against for the prune predicate. The layer function is code, single-sited and
fixture-tested, on exactly requirement 3's precedent: *changing the derivation changes the answer.*

**Two node kinds do not fit the operator's five, and that is a finding rather than an oversight.**

- **`NODE_RULE` is the join object, not a layer.** A rule is `declared-in` a doc and `enforces`-ed
  by code; it is a cross-layer edge reified as a vertex. Typing it as a layer of its own would
  collapse the distinction the graph exists to show. **Proposed: rules are not a layer.** Recorded
  as **open question 6**.
- **`NODE_CARRIER` / `NODE_COMPONENT` are a sixth layer, and it is the one that WRITES into L0.**
  Intake #62's 2026-08-31 amendment names deploy carriers as the derivation path for its directed
  shape *"hub authors, L0 derives"*. A layer model that cannot see the carrier cannot model that
  claim at all. **Proposed: admit `carrier` as a sixth layer.** The operator named five, so a sixth
  is a scope change and is the operator's to accept — recorded as **open question 7**, not taken.

### 2 · The measured hole the typing exposes: the code layer is 21 nodes

`git ls-files` against the governed set (a path is governed iff at least one of the five inputs
names it), measured 2026-08-31 in this lane:

- `scripts/` — **21 of 130** governed (16%)
- `tests/` — **0 of 204**
- `ecosystem/` — **0 of 104**, including `ecosystem/doc-code-edge.yaml`, which is **itself one of
  the five inputs** and is invisible as a node
- `.claude/` — **1 of 18** (see §4)
- `templates/` — 2 of 47 · `deploy/` — 2 of 26 · `protocols/` — 5 of 16 · `docs/` — 986 of 1,827 ·
  `tasks/` — 379 of 382
- **overall: 1,403 of 2,796 tracked files (50.2%)**

None of this is new information — `file_purpose_graph.py`'s own module docstring states it
honestly (*"most of `scripts/` and all of `tests/` are UNKNOWN to this graph, and `why` refuses
them"*), and calls the refusal the finding. **What the layer typing adds is that the refusal stops
being a per-file event and becomes a per-layer completeness number.** That is the first thing the
typed graph buys which the untyped one cannot, and it is one verb:

- **`coverage --by-layer`** — for each layer, governed nodes over candidate paths. It needs no new
  input, no new edge and no new dependency; it is the layer function plus a `git ls-files` walk.

**This is also where the typed graph and intake #62 meet, and the meeting point is one sentence:
you cannot govern a layer you cannot count.** #62's acceptance criterion 2 requires each of
skills / commands / settings / hooks to be assigned an ownership class with none left unassigned.
Today the graph sees exactly **one** `.claude/` file.

### 3 · Architectural attributes as node metadata — the shape, and what must NOT be built

The ten attributes carried by the 2026-08-29 note: **performance · availability · reliability ·
security · maintainability · extendability · modularity · reusability · readability ·
testability.** Re-verified 2026-08-31: `grep -ril "extendability\|GitNexus\|Code-Graph-RAG\|
repo-graph"` over the tree returns exactly one file — this intake. Both the attribute vocabulary
and the three library candidates remain a **first naming**, bound to no measurement and no
adoption.

An attribute is a **claim about a node**, and this corpus has exactly one standing rule about
claims: *a number typed into a doc is stale at the next commit* (`CLAUDE.md` §4, "never restate a
count or roster in prose — cite the surface that computes it"). The attribute schema must obey it
rather than route around it. Three design constraints follow, and they are the substance of this
section:

1. **An attribute is a POINTER to the surface that measures it, never a hand-typed grade.** The
   stored row is `{node, attribute, measuring_surface, value, measured_at}`, and
   `measuring_surface` is required. `security: <no measure>` is a legitimate value and is today
   the **common** one; `security: high` with no surface behind it is precisely the drift class this
   repo already refuses everywhere else.
2. **The vocabulary is OPEN, the schema is CLOSED.** The ten names are the operator's thesis
   vocabulary and may grow; the store knows only the row shape and nothing about which ten. An
   eleventh attribute is a data row, never a migration.
3. **Most cells will be empty, and the empty cells ARE the deliverable of the first slice.** The
   honest first act is not to populate the attributes — it is the **empty-cell census**: for each
   of the ten, name the live surface in this tree that could measure it, or record `none`. That
   census is what tells the operator whether this is a ten-attribute organ or a three-attribute
   one, and it is cheap.

**The attribute half therefore inherits THE METRIC's ordering, exactly as intake #62's admission
gate does and for exactly the same reason.** #62's 2026-08-31 amendment records it in one line:
*"an admission gate built before the harness that scores it would be a gate with nothing to
read."* The same sentence, read from this side: **an attribute column built before its measuring
surface is a column with nothing to read.** The coupling to batch E's **DM-1 (EVAL)** and to the
north-star arc **THE METRIC** is not incidental — it is the same dependency reached from a second
direction, which is itself evidence that the ordering is real.

### 4 · Cross-layer edges to intake #62's L0 layer — NO new node kind, NO new edge kind

Intake #62's amendment names three governed `.claude` surfaces (L0 `~/.claude` · hub `.claude` ·
consumer `.claude`) and one derivation mechanism (deploy carriers). Expressed as graph edges in
`file_purpose_graph.py`'s existing direction convention — **every edge runs consumer -> consumed** —
each one already has a registered kind in `EDGE_KINDS`:

- `L0 file --carried-by--> carrier` — "hub authors, L0 derives" (#62 layer 1). `EDGE_CARRIED_BY`
  exists and fires 19 times today, on no `.claude/` path.
- `consumer .claude file --carried-by--> carrier` — and **the ABSENCE of that edge is the answer**
  to #62's layer-3 clause, which requires that a consumer skill being *floor-carried* vs
  *locally-authored* be **readable from the artifact rather than inferred**. Provenance is edge
  presence. **No new metadata, no new provenance field, no new file format** — a result worth
  stating plainly, because the obvious alternative design (stamp a `provenance:` key on every
  consumer skill) is a hand-written claim of exactly the class §3 constraint 1 refuses.
- `agreement-check code --enforces--> rule --declared-in--> hub declaration doc` — the
  `[#592]`/`[#613]` drift-organ shape #62 names as the drift organ. Three existing edge kinds, and
  it is the exact two-hop chain `file_purpose_graph.py`'s docstring calls out as the query *"the
  five separate surfaces cannot answer at all"*.
- `hub declaration doc --governs--> L0 file` — the inward render of `EDGE_GOVERNED_BY`, which
  exists and fires 9 times.

**Consequence, stated plainly: L0 needs one new INPUT and nothing else.** A reader over `.claude/`.
Every node kind, every edge kind and the whole query surface are already built. L0 is the cheapest
of the five layers to admit and it is currently the emptiest — which is the inversion worth
recording, since it is also the layer #62 says carries *"a large share of the fleet's live
behaviour"*.

**The single L0 node, quoted because it is the sharpest fact this lane found.** The graph's one
`.claude/` node is `.claude/commands/override.md`, and it is present for exactly one reason: the
deploy manifest declares an `override-command` component that `ships` it. One edge, from the
`deploy-manifest` input. **The L0 layer exists in the graph today by accident of a manifest entry,
not by design** — and the command it points at is `/override`, which ADR-85's 2026-08-03 amendment
§A2 **retired**. Seventeen of the eighteen tracked `.claude/` files are invisible to the graph.

**The boundary is stated as a CONDITIONAL rather than assumed.** Reading `~/.claude` is not
editing it, but that distinction is precisely #62's **open question 3** — whether "hub authors, L0
derives" is compatible with core-invariant #6 — and **this design does not answer it, does not
assume it, and authorises no edit to any `~/.claude` path.** What it can do is make the ruling
cheap to land late:

- If #62 q3 permits a read, the L0 input is an in-repo reader with an out-of-repo scan root.
- If it does not, the L0 layer is scoped to in-repo `.claude/` and the graph reports the
  out-of-repo half as **unmodelled by ruling**, never as missing data — a distinction the graph
  already draws elsewhere, in `UnknownFile.exists`.

Both shapes are the **same code with a different scan root**, so the ruling can land after the
build with no rework. That property is a design choice and is recorded as one.

### 5 · What this changes in the requirements and open questions ABOVE

**Acceptance criterion 5 is STRENGTHENED, not replaced.** It requires *"a floor assertion on total
edges extracted"* so that a silently-broken regex cannot make every query quieter. Under typed
layers a **single global floor cannot do that job**: one layer's extractor can die while another
grows and the total holds. Criterion 5 becomes a **per-layer floor**, one assertion per layer.
This is a strengthening of a frozen ex-ante criterion, which ADR-81 (as amended 2026-06-24) permits
— CC may strengthen, never weaken — and it is recorded as an amendment to criterion 5 rather than
as a new criterion, so the count of criteria is unchanged.

**Open questions 2 and 3 are DISCHARGED by events, and should be marked so.** Both ask about
rustworkx: q2 *"is rustworkx installable under the pinned uv"*, q3 *"does it work on Windows"*.
Lane M shipped `scripts/file_purpose_graph.py` **on rustworkx**, and its module docstring records
the measurement: *"measured in-lane 2026-08-29 under the pinned uv 0.11.19 / CPython 3.12.10 /
win_amd64, rustworkx 0.18.1 installs from a PREBUILT hash-pinned wheel"*, so R-A's sqlite/stdlib
fallback was not taken. Both questions were answered by the build that happened after they were
written. **Recorded as discharged with evidence, not silently dropped.**

**Open question 1 is NOT discharged — but the typing changes its terms.** The question is whether
the graph-library phase earns its dependency, and its evidence was that SCC measured **0 real
findings out of 18** and pagerank had no asked question. That measurement was over the **global,
untyped** graph. A **layer-scoped** SCC — *"do the doctrine files cycle within the docs layer"* — is
a different query with a different denominator, and this intake's own fourth scenario asks exactly
that scoped form. Note also that the dependency question is now partly moot in the direction
nobody predicted: **rustworkx is already a declared dependency**, landed through the ADR-106 path
in its own commit by lane M. Open question 1 therefore narrows from *"does the library phase
happen"* to *"is there a layer-scoped query with demonstrated yield"* — **re-framed, not answered.**

**Open question 4 gets worse, and is re-pegged rather than re-answered.** It records that the
bucket taxonomy is load-bearing because a new `docs/<genre>/` folder silently defaults to
`actionable`. Under §1's layer function the same defect has a larger blast radius: a **new
top-level tree** silently defaults into the `docs` layer and pollutes every layer-scoped answer,
including `coverage --by-layer`. Same mitigation (requirement 3's derive-don't-copy rule, applied
now to the layer function), larger surface. Recorded, not settled.

### 6 · New open questions (continuing 1–5 above)

6. **Is `rule` a layer, or the join object?** §1 proposes the join object. If it becomes a layer,
   every `enforces`/`declared-in` edge stops being code<->docs and the code layer loses its only
   substantial cross-layer axis.
7. **Is `carrier` a sixth layer?** The operator named five. §1 argues yes, because it is the layer
   that writes into L0 and is therefore the one intake #62's directed shape runs through. A sixth
   layer is a scope change and is the operator's to accept.
8. **Where does the layer function live** — inside `file_purpose_graph.py`, or beside it in the
   `scripts/doc_graph/` namespace this intake's impact sketch proposes? It must be **single-sited**
   either way; the question is only which module owns it, and it interacts with whether the two
   organs (FPG-1 and this intake's document graph) stay two or converge into one.
9. **Do FPG-1 and this intake describe ONE organ or two?** Not asked before, and it should have
   been. FPG-1 answers `why <path>` over five governed inputs; this intake specifies `impact`,
   `orphans` and `dead` over the tracked `.md` corpus. They share a node namespace, a direction
   convention and now a layer function, and they differ in corpus (governed-only vs all-tracked)
   and in store (in-memory rustworkx vs the proposed sqlite). **Recorded as a question, because
   answering it either way is a scoping act the operator owns** — and because building the typed
   layers without answering it first is how a fleet ends up with two graphs that disagree.

### 7 · Readiness — REPORTED, not acted on

The done-contract for this lane requires that readiness be **reported** and never acted on, so:

**Ready, in this sense:** the design names its layers, its node-metadata shape, its cross-layer
edges and its build order, and it required **no new node kind, no new edge kind and no new
dependency**. Three of its four L0 edge shapes are already-registered kinds that already fire.

**Not ready, in this sense:** the attribute half has no measuring surfaces and inherits THE
METRIC's ordering (§3); open question 9 (one organ or two) is unanswered and is upstream of the
build order; and open questions 6 and 7 are scope calls the operator owns.

**Build order if ratified**, cheapest-first and each slice independently useful:

1. **Layer function + `coverage --by-layer`** over the existing five inputs. Pure addition, no new
   input, no new dependency. This is the slice that turns §2's numbers into a standing metric.
2. **The L0 input** (`.claude/` reader), scoped by intake #62 open question 3, written so the scan
   root is the only thing the ruling changes (§4).
3. **The code-layer input** — where the 21-of-130 hole closes and where the missing cross-layer
   edge *class* comes from.
4. **Attributes, last**, behind the empty-cell census, behind DM-1/THE METRIC.

**ZERO ROWS BORN HERE**, on this intake's own standing precedent and intake #62's: the carrier row
stays deliberately unborn under ruling D5's *"birth priority (2) when it ratifies"*, and the path
from a CANDIDATE to a row runs through intake and ratification (ADR-98, ADR-111 §2). This
amendment records direction and design. **Status is unchanged: DRAFT. DRAFT BINDS NOTHING.**

### What this amendment does NOT do

- **No build.** No script, no test, no schema, no store. This was a drafting lane.
- **No row born**, no status change, no folder created, no index regenerated.
- **No edit to any `~/.claude` path**, and no authorisation of one. Core-invariant #6 stands, and
  intake #62 open questions 1, 3 and 4 remain the operator's and the architect's to rule.
- **No supersession** of ruling A5, of R-A's `rustworkx`-not-`networkx` choice, or of funnel line
  R3's measured rejection of arming a gate leg on cycle count. This organ is still **not a gate**.
- **No answer** to open questions 1 or 4 — both are re-framed above and explicitly left open.
