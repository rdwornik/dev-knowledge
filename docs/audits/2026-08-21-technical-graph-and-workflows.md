# Dependency-graph organ (rustworkx) + reusable-workflows re-test

**Date:** 2026-08-22 · **Lane:** cloud, docs-only · **Base:** `origin/main` @ `70aa5f2`
**Contract:** `docs/audits/2026-08-21-technical-graph-and-workflows-lane-contract.md`
**Input of record:** `docs/audits/2026-08-21-technical-library-first-research.md` (Track 1 §1.2,
Track 2 §2.4) — this lane extends those two sections and re-derives neither.

**Carried rulings (not reopened here):** the consumer is named (dependency management), which
under ADR-105 clears activation; the library is ruled **rustworkx**, networkx not reconsidered.
Track B's two surviving rejection grounds — file distribution and offline operation — are not
reopened either.

---

## 0. Honest limits of this lane — read before the findings

1. **The predecessor's extractor was a scratch trial and is not in the tree.** §1.2 states its
   rule (repo-shaped `dir/.../file.ext` references over tracked `.md`, prose + backticks +
   links) but ships no code. This lane **reconstructed** it from that stated rule. The
   reconstruction is validated by the one invariant that matters: it returns **exactly 18
   nontrivial SCCs**, the predecessor's figure. Edge and node totals differ because the tree
   advanced (§1.1) — the SCC count did not.
2. **The tree moved between the two lanes.** Predecessor base `78267fd` / 1,952 tracked `.md`;
   this lane `70aa5f2` / **1,982**. Totals below are this lane's live measurement, not §1.2's.
3. **Track B's "zero orgs" premise is only half-verified.** Zero **outside collaborators** is
   verified live (below). Org membership is not enumerable from this lane's GitHub surface, so
   it is carried from the architect's premise — corroborated, not proven, by the repo being
   personally owned (`owner.type: "User"`).
4. **The 30%-of-2,000-minutes figure is operator-supplied.** This lane could not read the
   billing API. It is, however, **independently corroborated** by measurement — see §B2.
5. **No dependency was added.** rustworkx is the *recommended* library; the SCC computation here
   used a stdlib iterative Tarjan, so the numbers are reproducible with zero installs.

---

# TRACK A — the dependency-graph organ

## A1. The 18 nontrivial SCCs, enumerated

**Live extraction** (1,982 tracked `.md` sources, `70aa5f2`):

| | count |
|---|---|
| raw edges | 23,246 |
| unique `(source, target)` edges | 13,207 |
| nodes | 3,303 (2,505 `.md`) |
| dead targets (untracked) | 1,230 |
| **nontrivial SCCs** | **18** |
| self-loops | 0 |

### The size distribution is the first finding

The phrase "18 nontrivial SCCs" implies eighteen comparable cycles. It is one 338-node blob and
seventeen small ones:

| SCC | size | bucket composition |
|---|---|---|
| 1 | **338** | immutable 263 · actionable 46 · tasks 29 |
| 2 | 5 | immutable 4 · tasks 1 |
| 3 | 3 | immutable 3 |
| 4 | 3 | immutable 2 · tasks 1 |
| 5–18 (14 SCCs) | 2 each | immutable 2 each |

**SCCs 2–18 contain zero actionable nodes.** Every member is an immutable audit, an ADR, or a
`tasks/` row. By our own doctrine those files are never edited — `scan_undeclared_edges.py`
prunes exactly this set as "cannot take a `reconciled_with` line, so it is noise, not a
candidate" (its module docstring, pruning rule 1). A cycle among files nobody may edit is not a
defect anybody can act on.

### Table — all 18, with the closing edge and the read

| # | size | members (abbreviated) | edge that closes the cycle | read |
|---|---|---|---|---|
| 1 | 338 | 263 immutable + the whole `protocols/` canon, `docs/intake/**`, `templates/**`, 29 `tasks/` | 81 actionable→immutable bridges, e.g. `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md:18 → docs/audits/2026-07-27-verification-handoff-process-audit.md` (an `Evidence base:` line), closed by audits citing `protocols/PLAYBOOK.md` | **BENIGN — a citation blob, not a cycle.** Living docs cite immutable evidence (ADR-98 requires `decided-by:` provenance); immutable evidence cites living canon. Fused into one SCC by construction. Decomposes on pruning — see A2 |
| 2 | 5 | 3 audits + ADR-109 + `tasks/383-execution-waves-per-surface.md` | `ADR-109 → …-382-registry-prep-dossier.md → tasks/383 → …-383-caches-wave-record.md → …-intake-split-generality-discharge.md → ADR-109` | **BENIGN** — an ADR citing its prep dossier, the dossier citing the task, the task citing its wave record. Decision-provenance chain |
| 3 | 3 | `2026-07-28-codex-437-closure-design` · `-diff` · `2026-07-28-technical-437-closure-token-design` | `technical-437-closure-token-design → codex-437-closure-design → …-token-design` | **BENIGN** — three same-day artifacts of one closure design cross-referencing each other |
| 4 | 3 | gemini-ab lane-contract · results · `tasks/491-gemini-scanning-lane…` | `…-gemini-ab-lane-contract → …-gemini-ab-results → …-lane-contract` | **BENIGN** — contract↔output pair plus its task row |
| 5 | 2 | `2026-04-24-council-28-29-consolidated-actions` ↔ `2026-04-24-stream-a-gap-report` | mutual | **BENIGN** — peer audits of one session |
| 6 | 2 | `2026-08-03-technical-night-lb-groom` ↔ `ADR-82-handoff-process-v5-model-c` | mutual | **BENIGN** — a groom citing the ADR it grooms against; the ADR citing the groom record |
| 7 | 2 | `2026-08-18-census-adoption-preflight` ↔ `…-technical-adoption-preflight-lane-contract` | mutual | **BENIGN — lane protocol** |
| 8 | 2 | `2026-08-18-census-p10-grooming-evidence` ↔ `…-technical-p10-regen-lane-contract` | mutual | **BENIGN — lane protocol** |
| 9 | 2 | `2026-08-18-technical-502-mutmut-attribution` ↔ `…-502-mutmut-lane-contract` | mutual | **BENIGN — lane protocol** |
| 10 | 2 | `2026-08-19-technical-554-proof` ↔ `…-554-proof-lane-contract` | mutual | **BENIGN — lane protocol** |
| 11 | 2 | `2026-08-19-technical-c2-review-profiles` ↔ `…-contract` | mutual | **BENIGN — lane protocol** |
| 12 | 2 | `2026-08-19-technical-c3-grooming-wave2` ↔ `…-contract` | mutual | **BENIGN — lane protocol** |
| 13 | 2 | `2026-08-19-technical-c4-ruling-prework` ↔ `…-contract` | mutual | **BENIGN — lane protocol** |
| 14 | 2 | `2026-08-19-technical-c6-telemetry-readpath` ↔ `…-contract` | mutual | **BENIGN — lane protocol** |
| 15 | 2 | `2026-08-19-technical-n1-529-530-wiring-spec` ↔ `…-n1-wiring-spec-contract` | mutual | **BENIGN — lane protocol** |
| 16 | 2 | `2026-08-19-technical-n2-seam-worksheet` ↔ `…-contract` | mutual | **BENIGN — lane protocol** |
| 17 | 2 | `2026-08-19-technical-n5-codification-pack` ↔ `…-contract` | mutual | **BENIGN — lane protocol** |
| 18 | 2 | `2026-08-20-technical-grok-ab-results-2` ↔ `…-grok-ab-lane-contract-2` | mutual | **BENIGN — lane protocol** |

**Split: 0 REAL / 18 BENIGN.**

### The finding that decides the gate question

**13 of the 18 SCCs (4, 7–18) are the same shape: a lane contract and its output artifact citing
each other.** That pair is *mandated* — a dispatch stamp names its output of record, and the
output cites the contract it was dispatched under. The lane protocol manufactures one SCC per
lane executed.

**This lane manufactures SCC #19 — verified, not predicted.** The contract committed as this
lane's first commit names `docs/audits/2026-08-21-technical-graph-and-workflows.md`; this file
names the contract in its header. Re-running the extraction with both files staged:

```
tracked .md sources : 1983   (was 1982)
NONTRIVIAL SCCs     : 19     (was 18)

--- SCC 19 (size 2) ---
    docs/audits/2026-08-21-technical-graph-and-workflows-lane-contract.md
    docs/audits/2026-08-21-technical-graph-and-workflows.md
```

The cycle exists because the protocol was followed correctly.

That inverts the metric's sign: **nontrivial-SCC count is not a rot gauge, it is a throughput
gauge.** It rises with lanes executed. A gate on it would fire more the more work gets done.

## A2. What survives pruning — the decisive measurement

Pruning the immutable corpus is not an invention for this report; it is the pruning
`scan_undeclared_edges.py` already performs. Applied to the SCC query, three ways:

| corpus | edges | nodes | nontrivial SCCs |
|---|---|---|---|
| everything (as measured above) | 13,207 | 3,303 | **18** |
| actionable only | 663 | 328 | **2** |
| actionable + `tasks/` | 1,120 | 579 | **2** |
| everything except immutable artifacts | 1,629 | 814 | **2** |

The result is stable at **2** regardless of how `tasks/` and the append-only files are treated —
and the 338-node blob is revealed as an artifact of the immutable corpus, not a structural
property of the doctrine.

**SCC A (16 nodes) — the doctrine core:** `protocols/PLAYBOOK.md`, `ESSENTIALS.md`,
`HANDOFF_PROCESS.md`, `HANDOFF_BOOT.md`, `DEFINITION_OF_DONE.md`, `STANDING_RULINGS.md`,
`AI_COUNCIL_PROCESS.md`, `docs/intake/README.md` + 2 intakes, and 6 `templates/` files.

Its twelve mutual pairs, with the live lines:

| pair | the two lines |
|---|---|
| `PLAYBOOK:1189` ↔ `HANDOFF_PROCESS:124` | PLAYBOOK: *"Authoritative spec: `protocols/HANDOFF_PROCESS.md` v6.2.0 … **This is a pointer, not a duplicate**"* / HANDOFF_PROCESS: *"live at `protocols/PLAYBOOK.md` Ch8"* |
| `HANDOFF_BOOT:11` ↔ `HANDOFF_PROCESS:80` | boot names its spec; spec names its boot core |
| `DEFINITION_OF_DONE:16` ↔ `HANDOFF_BOOT:224` | DoD: *"Injected into the orchestrator at session-start via `protocols/HANDOFF_BOOT.md`"* / BOOT: *"The canon is `protocols/DEFINITION_OF_DONE.md`"* |
| `AI_COUNCIL_PROCESS:413` ↔ `ESSENTIALS:55` | delegation to the "Repo artifacts" rule, and back |
| `AI_COUNCIL_PROCESS:412` ↔ `PLAYBOOK:3534` | thresholds delegated out; lifecycle delegated back |
| `PLAYBOOK:1660` ↔ `STANDING_RULINGS:276` | PLAYBOOK cites ruling Q2; the ruling cites PLAYBOOK Ch8 |
| `PLAYBOOK:664` ↔ `templates/prompt-template:12` | *"Template: `templates/prompt-template.md`"* / *"governed by `protocols/PLAYBOOK.md`"* |
| `PLAYBOOK:4493` ↔ `templates/scrum-master-cover-letter:9` | procedure names template; template names procedure |
| `STANDING_RULINGS:278` ↔ `templates/prompt-template:60` | ruling register ↔ the template that applies it |
| `docs/intake/README:8` ↔ `templates/intake-template:2` | README names the skeleton; skeleton points to README §3 |
| `docs/intake/README:246` ↔ `STANDING_RULINGS:1037` | anti-orphan rule P-2 ↔ the §7 survival metric it fires |
| `intake-#27` ↔ `STANDING_RULINGS:388` | intake ↔ `Source of record:` line |

**Every one is a deliberate bidirectional pointer between peer canon — and it is CLAUDE.md §5
rule 6 that creates them.** Rule 6 forbids duplicating content between files; the prescribed
alternative is a pointer. Two files that both need to reference each other's authority
therefore *must* form a 2-cycle. `PLAYBOOK:1189` says so in as many words: *"This is a pointer,
not a duplicate."*

Breaking these cycles would mean inlining the content — the exact drift failure rule 6 exists to
prevent. **The cycle is the compliant state.**

**SCC B (2 nodes):** `docs/intake/2026-07-21-func-fleet-north-star.md` ↔
`docs/intake/2026-07-28-north-star-delta-review.md` — a proposal and its delta review. Benign;
grows to 3 with `tasks/382-desired-state-data-model-intake-adr.md` in the `tasks/`-inclusive run.

**So: on the corpus a gate could legitimately act on, there are 2 cycles, both benign, both
mandated by doctrine.**

## A3. Organ spec (spec only — nothing built)

### Where the edge extraction lives

`scripts/doc_graph/extract.py`, a new PEP 420 namespace sub-package under `scripts/` (matching
`scripts/audit_checks/`, which deliberately carries no `__init__.py`).

**Reused, not reinvented** (per contract):

| borrowed from | what |
|---|---|
| `docs/audits/2026-08-21-technical-library-first-research.md` §1.2 | the extraction rule itself: repo-shaped `dir/.../file.ext` over tracked `.md`, prose + backticks + links; the four-bucket taxonomy (actionable / `tasks/` / append-only / immutable) |
| `scripts/scan_undeclared_edges.py` (docstring, pruning rule 1) | the immutable/append-only prune set **and its allowlist** for living files inside immutable trees (the two READMEs) — reuse the predicate, do not re-derive it |
| `scripts/coherence_enumerator.py` `fenced_line_idx` | fenced-code-region skipping, already reused once by `scan_undeclared_edges` ("one regex, N consumers") |
| `docs/audits/2026-06-26-corpus-graph-justify-or-retire.md` | the archive-by-design exclusion, already ruled: 786 of 1003 files were excluded from rot scope on this same reasoning |

Extraction must capture the `:LINE` suffix as an edge **attribute**, not drop it — that is the
column `[#534]`'s gate reads.

### Query split — SQL vs rustworkx

Per §1.2's benchmark, unchanged:

| query | engine | measured (§1.2) | consumer |
|---|---|---|---|
| impact-of-move (reverse reachability) | **SQL** recursive CTE | 4.36 ms | dependency management — "what breaks if I move this doc" |
| orphan detection (in-degree 0) | **SQL** | 1.04 ms | dependency management |
| degree / fan-in ranking | **SQL** | 0.93 ms | dependency management |
| dead-target listing (`:LINE` resolution) | **SQL** | — | `[#534]` |
| **SCC / cycles** | **rustworkx** | 2.52 ms (SQL: 6,677 ms *and wrong shape*) | **none demonstrated — see A4** |
| **pagerank centrality** | **rustworkx** | 1.48 ms (SQL: in-degree only) | **none demonstrated** |

**The honest reading of this table is the report's most important line.** The named consumer —
dependency management — is served **entirely by the SQL half**, at zero new dependency.
rustworkx's two exclusive queries are exactly the two with no demonstrated yield: SCC, measured
at 0 real findings out of 18 (A1), and pagerank, for which nobody has asked a question.

This is not a re-litigation of rustworkx-vs-networkx, which is ruled. It is the answer to the
contract's own question — *"the evidence that decides whether the organ is worth building at
all"* — applied at leg granularity: **the organ is worth building; its graph-library leg is
not yet.**

### CLI shape

```
python -m scripts.doc_graph build              # extract -> .cache/doc-graph.sqlite (gitignored)
python -m scripts.doc_graph impact <path>      # reverse reachability: what cites this, transitively
python -m scripts.doc_graph orphans [--bucket actionable]
python -m scripts.doc_graph dead [--with-lines]   # dead targets; --with-lines is [#534]'s feed
python -m scripts.doc_graph degree [--top N]
python -m scripts.doc_graph cycles [--bucket actionable]   # PHASE 2, rustworkx
python -m scripts.doc_graph centrality [--top N]           # PHASE 2, rustworkx
```

`--format {text,json}` on every subcommand; `--bucket` defaults to `actionable` on every
subcommand that can be scoped, because A2 shows the unpruned answer is the misleading one.

### Output contract

Reuse `scripts/audit_checks/_common.Finding` — `Finding(check_name, status, message)`, the
shape every existing check emits (`check_vision_md.py` is the 38-line reference implementation).
JSON mode emits `{"query": …, "bucket": …, "results": [...], "counts": {...}}`. Exit 0 always
in report mode (matching `validate_reconciliation` / `validate_no_ff`, which never gate by exit
code); non-zero only if wired to a gate leg, which A4 recommends against for cycles.

### Where it plugs in

**Standalone command, not an `audit.py` check — for phase 1.** Reasons, in order:

1. `audit.py health` is a pre-commit gate (`audit-health`, §9). Its runtime is on the commit
   path — measured at **22 s** in `report-only-wall`'s run 106. A full-corpus extraction over
   1,982 files adds to every commit for a query nobody makes at commit time.
2. The `CHECK_ORDER` registry is a **byte-identical output contract** that git hooks depend on
   (`scripts/audit_checks/registry.py` docstring). Adding a check perturbs it.
3. The dependency-management consumer is *interactive* — "what breaks if I move this" is asked
   before a move, not on every commit.

**The `dead --with-lines` subcommand is the exception**, and it is `[#534]`'s, not this organ's:
that one query belongs in `audit.py health` as `[#534]` already specifies, reading this organ's
edge table as its substrate. §1.2's ADR-105 consumer table already names exactly this pairing.

### LOC estimate

| module | LOC |
|---|---|
| `extract.py` — regex, `:LINE` capture, normalization, fenced skip, bucket taxonomy, prune reuse | 140–180 |
| `store.py` — sqlite schema, build, staleness stamp | 60–80 |
| `queries_sql.py` — impact / orphans / dead / degree (recursive CTEs) | 80–110 |
| `cli.py` — argparse subcommands, text + JSON rendering | 90–120 |
| **Phase 1 subtotal (zero new dependency)** | **370–490** |
| `queries_graph.py` — rustworkx SCC / cycles / pagerank | 60–80 |
| **Phase 2 subtotal** | **430–570** |

**Estimate: ~370–490 LOC for the SQL organ; ~430–570 with the rustworkx leg.** The extractor is
~35% of it and is the part that has to be right — everything downstream inherits its errors.

### Failure modes

1. **Regex false positives are the dominant risk, and they are already witnessed.** §1.1
   measured our `[#430](a)` citation grammar parsing as CommonMark link syntax — 6 of 6 of
   lychee's actionable findings. A path-shaped regex has the same exposure: version strings
   (`v1.3.1`), dotted identifiers (`audit.py::ALL_CHECKS`), and `owner/repo/.github/workflows/x.yml`
   references all match "has a slash and an extension". Mitigation: extraction must be
   fixture-tested against a probe file in the shape of §1.1's Trial C, not eyeballed.
2. **Extraction drift is silent.** If the regex quietly stops matching a form, edges vanish and
   every query gets *quieter* — orphan counts fall, impact sets shrink. A shrinking finding
   count reads as improvement. Mitigation: assert a floor on total edges extracted, and stamp
   the corpus size in the store.
3. **Stale cache.** A gitignored sqlite file goes stale the moment a doc is edited. Mitigation:
   stamp the tree SHA on build; every query refuses on mismatch rather than answering from
   stale data.
4. **The bucket taxonomy is load-bearing and hand-maintained.** A2 shows the answer changes by
   9× (18 → 2) depending on the prune. A new `docs/<genre>/` folder silently defaults to
   `actionable` and pollutes results. Mitigation: derive the prune set from
   `scan_undeclared_edges`'s live predicate rather than copying its literals — a second copy
   drifts (CLAUDE.md §5 rule 6, the same failure the doctrine cycles exist to avoid).
5. **rustworkx install path is UNVERIFIED under our pinned `uv`** — §0.1 of the input of record
   applies unchanged. `required-version = "==0.11.19"`; every Python candidate in that report
   was trialled outside it. First act of any phase-2 adoption is that one-command check.
6. **Windows unverified.** Same §0 limit — rustworkx ships wheels, but no Windows run was done,
   and the repo is Windows-developed.

## A4. The gate question

**Recommendation: REPORT-ONLY COMMAND. Not FAIL, not WARN.** The architect rules.

The reason is measured, not stylistic:

- **A WARN leg would arm at a baseline of 18 findings, 0 of them actionable.** Contrast the one
  gate this fleet armed on library-first evidence: lychee, `[#573]`, armed *because* its
  measured baseline was **exactly 0** — "the cheapest possible moment to arm a gate: it can only
  ever fire on new rot." The SCC leg is the mirror image of that argument.
- **The baseline grows with throughput, not with rot** (A1). 13 of 18 are lane contract↔output
  pairs; this lane adds #19. A WARN that increments every time a lane executes correctly trains
  the operator to ignore it — and an ignored WARN is the ADR-105 §2 failure `[#419]` names,
  *"we run routines whose output nobody consumes."*
- **Even scoped to the actionable corpus, where the count is a tractable 2, both findings are
  compliant states** (A2). A gate that fires on CLAUDE.md §5 rule 6 being obeyed is a gate
  against our own doctrine.
- **FAIL is unavailable on the merits and would be unenforceable anyway** — see §B1: the
  server-side surface cannot carry a required check, and a client-side FAIL on a benign
  baseline of 18 would simply be `--no-verify`'d.

The constructive form: `cycles` ships as a subcommand the operator runs when asking a structural
question, with `--bucket actionable` as the default so the answer is 2 rather than 18. If a
cycle class ever *is* judged real, that is the moment to revisit arming — with a baseline that
has been deliberately driven to zero first, lychee-style.

## A5. Row / intake shape, and the relation to `[#534]`

**Complements `[#534]`. Does not supersede it.** They are disjoint classes, and §1.0 of the
input of record already drew the line: `[#534]` is about a **prose `path:LINE` locator resolving
to its named construct** — a semantic claim about a line number. The graph organ is about **edge
topology** — which files cite which. The organ cannot tell you whether `scripts/audit.py:4751`
still points at the scope list; it can only tell you the edge exists and the file does.

The relation is substrate, not overlap, and §1.2's own ADR-105 table already states it: the
sqlite3 edges table's named consumer **is** the `[#534]` gate. So:

- **`[#534]` stays open, unchanged, and gains a dependency**, not a replacement. Its ~80 LOC
  (recommendation 4 of the input of record) becomes ~40 if it reads this organ's edge table
  instead of building its own — but it must not *block* on the organ, because `[#534]` is P2 and
  this is not.
- **Shape needed: one new `[P3][M]` BACKLOG row** for the phase-1 SQL organ. `M` not `S`: the
  LOC estimate is 370–490 with a fixture-tested extractor. `P3` not `P2`: the named consumer is
  interactive dependency management, not a gate, and `[#534]` carries the urgent half.
  `kill-candidates:` would be `none` — no row owns doc-graph topology; `[#534]` owns prose
  locator resolution, which this does not cover, and `[#573]` owns markdown-link rot, which it
  also does not.
- **Phase 2 (rustworkx) needs an intake, not a row** — it adds a dependency to a repo in the
  fleet's distribution path, which is the ADR-112 **Tier L** bar (evaluate before adopting),
  not Tier S (try and keep or delete). It should also carry A3's failure mode 5 as its opening
  question: install-path-under-pinned-`uv` is unverified.
- **The disposition on intake #16 §3 recorded on 2026-08-22** (recommendation 2 of the input of
  record) is *not* contradicted by this lane. That disposition rested on "no consumer exists";
  the architect has since named one. This lane's finding is narrower and compatible: the named
  consumer is served by the SQL half, so the **filing** is warranted and the **graph-library
  activation** still lacks a query with demonstrated yield.

Per the contract, nothing above is filed, ruled, or edited by this lane — these are shapes named
for the architect.

---

# TRACK B — reusable workflows under the corrected premise

## B0. What was verified live

| premise | status | evidence |
|---|---|---|
| personal account, not org-owned | **VERIFIED** | `rdwornik/dev-knowledge` → `"owner": {"type": "User"}` |
| zero outside collaborators | **VERIFIED** | `list_repository_collaborators(affiliation=outside)` → `{"items": []}` |
| zero orgs | **CARRIED, not verified** | no org-enumeration surface in this lane; corroborated by `owner.type: "User"` |
| repo is private | **VERIFIED** | `"private": true, "visibility": "private"`, `forks_count: 0` |
| private→private `uses:` is permitted with the access policy opened | **ACCEPTED** (architect's correction) | not flipped from this lane — an outward-facing settings change, and this lane is docs-only |

**The "outside collaborator" warning is confirmed inert.** The count is zero, and there is no
org through which indirect access could be granted. That ground of the previous rejection is
correctly withdrawn.

## B1. Scoping the survivor — which gates could actually run in Actions

Of the 20 pre-commit hooks in CLAUDE.md §9 plus the deployed roster, the split is:

| class | count | gates | why |
|---|---|---|---|
| **HUB-ONLY — not fleet gates at all** | 9 | `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `organ-index-freshness`, `intake-index-freshness`, `validate-hermetization`, `check-seal-identity`, `lane-contract-check`, `toc-freshness-playbook` | each is marked HUB-ONLY in §9 and guards a hub-local generated file. No consumer has the surface |
| **Prevent organs that DEGRADE to detect if moved** | 5 | `block-ff-push`, `block-unanchored-push`, `block-commit-on-main`, `backlog-id-on-close`, `backlog-filing-backpressure` | all are `pre-push` or `commit-msg`. Their entire value is refusing *before* the commit or push exists. In Actions the push has already landed — you get a record, not a refusal. `block-unanchored-push` was moved to pre-push *precisely because* an organ that cannot carry teeth is worthless (§9: *"an organ that can be exhausted cannot carry teeth"*) |
| **Genuinely CI-runnable fleet gates** | 6 | `ruff`, `audit-health`, `validate-backlog`, `floor-hash-verify`, `canonical_freshness`, `codemap-freshness` | operate on the consumer's own committed tree; no local-only state |
| **Pointless in CI** | 1 | `coherence-nudge` | non-blocking stdout nudge by design; a CI copy has no reader |

**Needs Windows:** none of the six *requires* it, but the repo is Windows-developed, so a gate
whose behaviour is path-separator- or encoding-sensitive would need a `windows-latest` matrix
leg to be trustworthy — at **2× the minute rate** (Linux 1×, Windows 2×, macOS 10×).

**Needs the hub tree:** `audit-health` and `codemap-freshness` both execute hub `scripts/`
against the consumer's tree. This is the structural problem §B3 exposes.

### And then the ground that ends it

Our own CI file records it, in its opening comment:

> *"No required check is armed by this file — and none can be: **the repo is private on the Free
> tier, so required checks are unavailable.** This is REPORT-ONLY FOREVER, not a gate awaiting
> promotion."* — `.github/workflows/report-only-wall.yml:2–5`

Branch protection — and therefore required status checks — is not available for private repos on
the Free plan. **So the survivor scope the contract asked me to test ("FLEET-WIDE CI GATES") does
not exist on the current plan.** Every one of the six runnable checks would be report-only in
Actions, exactly as `report-only-wall.yml` already is. A fleet-wide CI *gate* that cannot block
is a fleet-wide CI *record*.

That is not a reason to stop the analysis — a server-side record has genuine value that no
client-side hook can supply (§B4). It is a reason to price it as a record.

## B2. Cost — measured on our own runs, not assumed

**Measured from `report-only-wall.yml`, run 106 (`70aa5f2`), the live jobs API:**

| job | wall clock | **billed** |
|---|---|---|
| `record` | 5 m 21 s | 6 min |
| `changes` | **10 s** | **1 min** |
| `mutation-pilot` | skipped | 0 min |
| **total** | **5.42 min** | **7 min** |

**The `changes` job is the whole cost argument in one row.** It does ten seconds of work and
bills a full minute, because GitHub bills **per job, rounded up to the nearest minute**. Job
splitting is not free — and a reusable-workflow call *is* a job split. That is measured in our
own repository, not quoted from documentation.

**Push frequency, measured:** runs 77–106 span 2026-08-16 → 2026-08-22 = **30 runs / 7 days ≈
4.3 pushes to `main` per day**. Mean wall clock over those 30 runs: 6.07 min.

**Corroboration of the operator's 30% figure:** 22 elapsed days of August × 4.3 pushes × 7
billed min = **662 min ≈ 33% of the 2,000-minute Free-tier private-repo allowance.** The
operator-supplied 30% is independently reproduced. At the current rate the hub alone finishes
the month near **930 min (~47%)**.

**The model.** Active repos: the hub plus the two deployed consumers (ai-council @ 1.3.1,
corp-monorepo @ 1.2.0) = 3. Assume the six runnable gates from B1, ~30 s of real work each, and
the measured ~13 s per-job setup floor (set up job 1 s + checkout 7 s + install pinned uv 2 s +
`uv sync --locked` 3 s).

| shape | per push | 3 repos × 4.3/day × 30 days = 387 pushes |
|---|---|---|
| **six reusable-workflow calls** (six jobs, six round-ups) | 6 × ceil(13 s + 30 s) = **6 min** | **2,322 min/month** |
| six steps in **one** job (the incumbent shape) | ceil(13 s + 6×30 s) = **4 min** | 1,548 min/month |
| add the hub's existing report-only-wall | — | + ~660 min |

- Remaining allowance after the measured 30%: **1,400 min.**
- Reusable-workflow shape: **2,322 min — 166% of what remains, and 149% of the entire 2,000-minute monthly allowance before the existing wall is counted at all.**
- Even the cheap single-job shape (1,548 + 660 = 2,208) overruns the allowance.
- A `windows-latest` leg doubles whichever figure applies.

**The decomposition premium is the part attributable to reusable workflows specifically: +2 min
per push, +774 min/month, ~+50% — for zero additional checking.** Those minutes buy job
isolation, not coverage.

**Verdict on cost: it exceeds the benefit, and not marginally.** The benefit is bounded above by
"a report", because required checks are unavailable (B1). The cost is the entire Actions
allowance plus overage. Overage on the Free plan requires a spending limit to be raised —
billed minutes beyond the allowance are chargeable — so this is a real invoice, not a soft cap.

## B3. The setup, concretely

**Settings path (called repo = the hub):**
`https://github.com/rdwornik/dev-knowledge` → **Settings → Actions → General → Access** →
select *"Accessible from repositories owned by the user **rdwornik**"* (default is *"Not
accessible"*).

**`gh api` equivalent:**

```bash
# read the current policy
gh api /repos/rdwornik/dev-knowledge/actions/permissions/access

# open it to the owner's other repos  (access_level: none | user | organization)
gh api --method PUT /repos/rdwornik/dev-knowledge/actions/permissions/access \
  -f access_level=user
```

`organization` is not applicable here — the repo is user-owned (B0).

**Called workflow** (`.github/workflows/fleet-gate.yml` in the hub) must declare the trigger:

```yaml
on:
  workflow_call:
    inputs:
      source-root: {type: string, default: src}
```

**Caller form** (in each consumer):

```yaml
jobs:
  fleet-gate:
    uses: rdwornik/dev-knowledge/.github/workflows/fleet-gate.yml@v1.3.1
```

Limits that bind: **10 nesting levels**, **50 unique reusable workflows per caller file** —
neither is close to binding at fleet size.

### The structural finding this setup exposes

**Opening the access policy makes the workflow CALLABLE. It does not make the hub TREE
READABLE.** `uses:` resolves the workflow *definition* only. Inside a called workflow,
`actions/checkout` defaults to the **caller's** repository, and the auto-provisioned
`GITHUB_TOKEN` is scoped to the caller repo — it cannot clone the hub. So any gate that executes
hub `scripts/` (B1: `audit-health`, `codemap-freshness` — the two that carry the most fleet
value) requires:

```yaml
- uses: actions/checkout@v4
  with:
    repository: rdwornik/dev-knowledge
    ref: v1.3.1
    token: ${{ secrets.HUB_READ_PAT }}    # a PAT per consumer, rotated, stored as a secret
```

**A PAT becomes mandatory in every consumer**, with the rotation and blast-radius burden that
implies. The ADR-71 pre-commit hook layer has no equivalent requirement: `pre-commit` clones the
hub repo over the developer's own git credentials, which already work.

**Versioning vs the deployed-versions record.** `uses: …@v1.3.1` pins by tag — the *same* tags
ADR-71 already publishes (`v1.0.0 v1.2.0 v1.3.0 v1.3.1`, confirmed live). That is the problem,
not the solution: it becomes a **second, independent pin of the same tag in a different file**,
with no assertion that the two agree. Today `precommit-hub-block` probes the hook pin with
`expected_rev_from: deployed-versions` **and `ancestry: true`** (a `git merge-base --is-ancestor`
against the hub tag). A `uses:` line has no such probe. Matching it would require a new
`workflow_call_pin` probe type in `_PROBE_REQUIRED_FIELDS` plus its `fleet_parity.py`
implementation — and per §3.2 of the input of record, a rule of a **new kind** is the expensive
column: "Python probe + `_PROBE_REQUIRED_FIELDS` entry + test".

**Net: the workflow layer adds Python, and adds a second version pin that needs guarding.** It
moves against the standing constraint the whole research arc exists to serve — *scale to N repos
without our line count scaling with it*.

## B4. Verdict against the incumbent hook layer

**Honest answer: NO — the workflow layer adds nothing the hook layer does not already give us,
with one genuine exception that is already claimed by a different incumbent.**

| capability | pre-commit remote hooks (ADR-71, adopted) | reusable workflows |
|---|---|---|
| pin by hub tag | yes — `v1.0.0`–`v1.3.1`, live | yes — same tags, second pin, unguarded |
| ancestry assertion on the pin | **yes** — `precommit-hub-block`, `ancestry: true` | no — needs a new probe kind |
| blocks the developer before the mistake lands | **yes** (`pre-commit`, `commit-msg`, `pre-push`) | **no** — post-hoc only |
| can be a required check | n/a | **no** — Free tier + private (B1) |
| works offline | after first clone | **no** |
| delivers files to the consumer tree | via the copy carriers (out of scope, unchanged) | no — and `uses:` does not deliver the tree either (B3) |
| credentials needed | developer's existing git creds | **a PAT per consumer** |
| marginal minute cost | zero | **+774 min/month over the allowance (B2)** |
| **survives `git push --no-verify`** | **no** | **yes** ← the one genuine addition |

**The one genuine addition is server-side execution that a local bypass cannot erase.** That is
real, and it is exactly what `report-only-wall.yml` was built for — its own header says so:
*"every hard gate in this repo is client-side, so `git push --no-verify` erases any RED without
a trace. A push-triggered run that re-executes those same checks server-side leaves a record no
local bypass reaches."*

**So the incumbent for this job is not the hook layer at all — it is `report-only-wall.yml`, and
it already exists.** The real question reduces to: *reusable* workflows versus copying that one
workflow file into the consumers. On that question:

| | reusable workflow | copy the workflow file |
|---|---|---|
| avoids duplicating ~400 lines of YAML into 2 consumers | **yes** | no |
| minute cost | 6 min/push (six job splits) | 4 min/push (one job) |
| PAT per consumer | **required** | not required for consumer-local checks |
| access-policy change | required | none |
| new `fleet_parity` probe kind | required | none — `carrier_docs` is *"already fully manifest-driven source→dest copy"* (§2.3) |
| offline | no | no (same) |

**Recommendation: REJECT reusable workflows again — on new grounds, not the withdrawn one.**
The private-repo access ground is correctly withdrawn and is not why this fails. It fails on
three independently sufficient grounds, all measured in this lane:

1. **The gate class does not exist.** Required checks are unavailable on Free + private, so the
   "fleet-wide CI gate" survivor is a fleet-wide CI *record* (B1, our own file).
2. **The cost overruns the whole allowance** — 2,322 min/month against 1,400 remaining, with the
   decomposition premium (+774 min) buying zero coverage (B2).
3. **It needs a PAT per consumer and a new parity probe kind**, because `uses:` delivers the
   workflow but not the tree our gates execute (B3).

**The constructive alternative, if server-side recording is wanted in the consumers:** ship
`report-only-wall.yml` through the existing `carrier_docs` manifest as one more source→dest copy.
Zero new mechanism, zero PAT, zero access-policy change, one job per push instead of six, and it
lands on the side of the §2.4 boundary that section already draws correctly — *"everything that
must survive an isolated clone must be copied."* A workflow file that must exist in the
consumer's own `.github/` to fire on the consumer's own push is, by that test, copy material.

---

## Appendix — reproducing this lane

All analysis ran read-only, in-tree, on `70aa5f2`. Scratch scripts lived under the session
scratchpad and are not part of this repo (CLAUDE.md §5 rule 9); no dependency was installed.

```
# Track A — edge extraction + SCC (stdlib iterative Tarjan, no rustworkx installed)
#   sources: git ls-files '*.md'  ->  1982
#   regex:   (?<![\w./~-])((?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9]{1,6})(?![\w/-])
#   -> 23246 raw / 13207 unique edges / 3303 nodes / 18 nontrivial SCCs / 0 self-loops
#   pruned to the actionable corpus -> 663 edges / 328 nodes / 2 nontrivial SCCs

# Track A — live baselines re-confirmed from the input of record
python scripts/scan_undeclared_edges.py     # pruning predicate reused, not re-derived

# Track B — GitHub facts, read live
#   repo:            private=true, visibility=private, owner.type=User, forks=0
#   collaborators:   affiliation=outside  ->  []
#   tags:            v1.0.0 v1.2.0 v1.3.0 v1.3.1  (+ archive/drafts-2026-07-07)
#   workflow runs:   report-only-wall.yml, 106 runs; runs 77-106 span 7 days
#   run 106 jobs:    record 5m21s -> 6 billed, changes 10s -> 1 billed, pilot skipped -> 0
```
