---
intake-id: 40
status: DRAFT
origin: cloud-graph lane artifact docs/audits/2026-08-21-technical-graph-and-workflows.md (Track A), routed here by the wave-close funnel table docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md lines I1/I2; architect ruling A5 of 2026-08-22 approved the R-A scoping and directed execution to ride this intake
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
note: Filed as an intake rather than as a backlog row BECAUSE the source lane asked for a row directly and ADR-111 section 2 forbids that — the only path from a finding to a row runs through intake and ratification. The lane's specified shape is carried below rather than re-derived, so ratification loses nothing by the detour.
---

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
