---
intake-id: 87
status: DRAFT
origin: browser architect seat, 2026-09-07 — `to-cc/INBOX-dev-knowledge-2026-09-07-035.md`, the operator's path-management proposal reviewed critically; merged into `to-cc/DECLARE-GRAPH-2026-09-07.md` §3 as node attributes on FPG-1
consumed-by:
---

# Half the identity layer exists (`#row`, `ADR-NN`, intake-id) and the other half — the resolver — was never built

## Problem / motivation

The operator's proposal: no hardcoded path anywhere; every repo manages paths through a data
structure that knows every file and folder, with a description per node, usage statistics, a score
for "probably unused", and a cheap daily routine reporting changes.

INBOX 035's review finds **the core right and already an industry pattern**, and names it:

- *No hardcoded paths* = **logical identifiers + a resolver** — Bazel labels, TypeScript `paths`,
  npm `exports`, Nix store paths, PURL/DOI for artifacts. **We already have half:** `intake-id`,
  `ADR-NN`, `[#row]`, `closed_by:`. **Missing:** the resolver, and the rule that docs and scripts
  reference ids rather than paths.
- *A structure that knows every file, with description and stats* = a **metadata catalog**
  (Backstage software catalog, DataHub, SBOM-style manifests). Ours is **the node table of the one
  graph** — nothing new is invented; FPG-1 gains attributes.
- *A cheap daily routine reporting deltas* = the nightly Routine + scorecard, where the report is a
  **graph diff** (new orphans, dropped in-degree, stale descriptions).
- *Identical layout everywhere* (#73) makes the resolver trivial and the schema single — one
  implementation, zero per-repo branches.

Today a file move breaks every prose citation of it, and nothing knows what a given file is *for*
without a human opening it. That is the itch; the shape is settled, the build is not.

## Scenarios (+1 view)

- As a seat, I move a doc to its #73-ruled home. Consumers cited its **id**, the registry maps
  id → path, one row changes and nothing else breaks.
- As the operator, I read the nightly `catalog report` — a graph diff of ≤ 5 KB: what gained a
  consumer, what lost one, which descriptions went stale against their locator. It feeds the
  ratification list; I rule; the retention grammar executes.
- As a link-check organ, I meet a commit citing a raw path where an id exists. I WARN during
  migration and FAIL after the cadence — the citation grammar converges instead of being decreed.
- As CC, I spot-check a sample of the weekly Gemini description pass against the locator each
  description carries, and fabrications are **counted**, not merely disliked.

## Functional requirements

- **Must:**
  - **Node attributes on FPG-1** (`DECLARE-GRAPH` §3): `path · id · genre (#73) · one-line
    description · last content commit · in-degree (citations) · trigger count (TRACE, L4) · owner
    row/ADR`.
  - **Generated, never hand-edited** — `gen_catalog.py` → `ecosystem/catalog.json` (or `.jsonl`).
    **Committed**, not gitignored: it is a derived copy registered in U4, and the daily report *is*
    its diff.
  - **Resolver `resolve(id) → path`.**
  - A **link-check organ** refuses a commit referencing a path where an id exists — **WARN first,
    FAIL after the cadence**.
  - `config/catalog-schema.yaml` — node attributes + edge types, the same file the graph ruling
    defines; the #73 grammar supplies genre → home.
  - **The "probably unused" score is mechanical and explainable:** in-degree = 0 ∧ no trigger in N
    days ∧ not in a genre allowlist ∧ last content commit older than the groom cadence → candidate.
    The formula lives in a table; the test seeds the cases.
- **Should:**
  - Weekly, batched, **reader-only** Gemini (agy) description pass: every description carries the
    locator it summarises; CC samples; fabrications counted.
  - Grey-zone ranking — nodes the formula cannot decide — returned as a **proposal**, never a
    verdict and never a deletion.
  - Carried by the manifest so consumers receive the schema identically.
- **Could:** the operator's personal filesystem under the same pattern — different repo
  (`win-tooling`), later.

## Acceptance criteria (ex-ante)

1. `resolve(id) → path` returns the live path for every `intake-id`, `ADR-NN` and `[#row]` in the
   tree; an id with no file, and a duplicate id, each **refuse** rather than return a guess.
2. The catalog is regenerable and **byte-stable** across two runs on an unchanged tree — a diff
   report whose generator is nondeterministic reports noise as change.
3. A file moved to a new path, with its id unchanged, produces **zero** citation breakage and
   exactly one changed catalog row.
4. The mechanical score is fixture-tested at each of its four clauses **independently** — a
   conjunction tested only in aggregate cannot show which clause fired.
5. The link-check organ WARNs on a path citation that has an id, and FAILs the same input after the
   cadence; both directions fixtured.
6. **No gate calls an LLM on its hot path** — asserted, not assumed. A description-refresh failure
   degrades the catalog's prose and nothing else.
7. Every generated description carries a resolvable locator; a sampled fabrication count is
   reported rather than hidden.

## Non-goals

- **Not a URL-management engine.** Once identity is the id and the layout is identical, the
  resolver is a dictionary and the cache is git itself — `git log` gives modification frequency for
  free, TRACE gives triggers. INBOX 035's correction 2, recorded so it is not relitigated.
- **Not an LLM inside every node.** Non-deterministic, costly per node, untestable. Judgment stays
  mechanical; the model is a reader in two bounded roles.
- **Not a new graph.** These are attributes on FPG-1 (intake #40's Done-when).
- **Not the operator's personal filesystem** — same pattern, different repo, later.

## Impact sketch (4+1 lite)

- **Logical:** node table + edge types on the one graph; a resolver function; a link-check organ.
- **Process:** nightly `catalog report` → ratification list → operator ruling → retention grammar.
- **Development:** `gen_catalog.py`, `config/catalog-schema.yaml`, a U4 registration, the
  path→id migration of existing citations.
- **Physical:** committed derived copy in `ecosystem/`; agy/Gemini batch weekly, off every hot path.

## Open questions

1. `catalog.json` or `.jsonl`? The diff is the daily report, so the format is chosen by **diff
   legibility**, not by parse convenience.
2. Where does `trigger count` come from before TRACE/L4 is populated — an absent column, or a
   declared zero? An absent column and a real zero must not render the same.
3. Does the link-check organ's migration cadence match ADR-41's 21 d, or does a citation migration
   deserve its own longer clock?
4. Genre allowlist home — #73 grammar file or `catalog-schema.yaml`? **Same fork as the
   `orphan_census` intake's question 3; decide once, for both.**
5. Does the resolver bind cross-repo ids (a consumer citing a hub ADR), or refuse at the repo
   boundary? Same fork as intake #40 open question 11 and intake #62 open question 3.

## Status

DRAFT — filed 2026-09-07 by filings-N3 from INBOX 035, folded into `DECLARE-GRAPH-2026-09-07` §3 as
migration step **W-G2**. Awaiting technical-architect triage and ratification. No carrier row
(ADR-111 §2).
