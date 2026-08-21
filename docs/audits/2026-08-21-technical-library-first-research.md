# Library-first research — the four scaling surfaces

**Date:** 2026-08-21 · **Lane:** cloud, read-mostly, docs-only · **Base:** `origin/main` @ `78267fd`
**Contract:** `docs/audits/2026-08-21-technical-library-first-research-lane-contract.md`
**Verdict vocabulary (per contract):** ADOPT / REJECT-WITH-MEASURED-DIVERGENCE / DEFER. Never
"we already built it".

**Standing constraint this answers:** *it must scale to N repos without our line count scaling
with it.*

---

## 0. Honest limits of this lane — read before the verdicts

Four limits bound every number below. None is fatal; all three of the material ones are
recorded so a later reader does not over-trust the trial.

1. **The trials did NOT run under our pinned `uv`.** `pyproject.toml:25` pins
   `required-version = "==0.11.19"`; this cloud container ships `uv 0.8.17`, and
   `uv sync --locked` **refuses**:
   `error: Required uv version '==0.11.19' does not match the running version '0.8.17'`.
   Every Python candidate was therefore trialled in a throwaway `python -m venv` under
   `$SCRATCH`, on CPython 3.11.15. **Install-path-under-our-pinned-uv is UNVERIFIED for every
   Python candidate in this report.** That is a one-command check on the operator's host, and
   it is the first thing any adoption must do.
2. **Linux only.** Windows support is reported from publisher claims and released artifact
   targets (probed live, HTTP 302 → asset present), not from a Windows run. The repo is
   Windows-developed, so this matters.
3. **The brief's Track-1 premise contains a conflation, corrected in §1.0.** `doc_rot`'s 20
   WARNs are not link findings. Everything downstream of that in Track 1 is re-derived from
   measurement, not from the premise.
4. **The brief says `deploy/` has "four carriers". It has six.** `docs`, `precommit`, `floor`,
   `plugin`, `global-config`, `mesh`. The Track-2 mapping covers all six.

---

# TRACK 1 — doc→doc / file→doc edges and locator rot

## 1.0 The premise correction, first — because it changes the whole track

The brief groups three things as one surface: `scan_undeclared_edges.py` (19 WARNs), the 6.9%
locator rot, and `doc_rot` (20 WARNs). **They are three disjoint classes with zero overlap**,
and only one of them is a link problem at all.

| Our organ | LOC | What it actually finds | Live count | Is it a *link* class? |
|---|---|---|---|---|
| `scan_undeclared_edges.py` | 314 | A doc that references a registered **spec** in prose but declares no `reconciled_with:` edge | **19** candidates + 4 weak signals | **No** — semantic, undeclared, prose-tier |
| `validate_reconciliation.py` `_SPEC_REGISTRY` | 356 | A **declared** edge whose version is behind the spec's live version | 2 specs registered; 120 `reconciled_with:` lines in-tree | **No** — version drift on a declared edge |
| the 6.9% locator rot (`[#534]`) | *no organ exists* | `scripts/audit.py:4751` style `path:LINE` locators, in **prose**, that no longer resolve to the named construct | 6 dead/drifted across 5 rows = 6.9% of 72 git-silent BACKLOG rows | **No** — bare prose token, not markdown link syntax |
| `validate_doc_rot.py` | 378 | Accretion / row-length / grooming-cadence | **20** = 19 × `backlog-row-length` + 1 × `grooming-cadence` | **No — not one link finding** |

Verified live:

```
$ python scripts/scan_undeclared_edges.py | head -1
scan_undeclared_edges: 19 candidate(s), 4 weak signal(s)

$ python scripts/validate_doc_rot.py | head -3
validate_doc_rot: 20 doc-rot locus(es) past threshold:
  backlog-row-length  BACKLOG#547  ->  2099 chars (declared ceiling 1320)
  backlog-row-length  BACKLOG#530  ->  1871 chars (declared ceiling 1320)
...
    grooming-cadence  BACKLOG#grooming-cadence  ->  last groom 2026-07-30, 22d ago (> 21d cadence, ADR-41)
```

**So the honest question is not "does lychee subsume our scanners" — it is "does lychee find
anything at all in a class nobody currently guards".** Measured below: it does, and the class
is currently empty, which is a different and cheaper kind of win than the brief anticipated.

## 1.1 lychee — trial, on a throwaway clone

`lychee 0.24.2`, Rust, single static binary, **18.9 MiB**, `Apache-2.0 OR MIT`. Latest release
**2026-05-01** (crates.io `updated_at`; 178,285 downloads). Windows/macOS/Linux binaries every
release (`lychee-x86_64-pc-windows-msvc.zip` probed live → HTTP 302, asset present). Install
path: **no `uv` involvement at all** — it is a downloaded binary or a pre-commit hook, so limit
(1) above does not bind it. That is a real advantage over every Python candidate here.

**Trial A — `docs/` + `protocols/` + root canon, offline, fragments on:**

```
$ lychee --offline --include-fragments --no-progress --format json \
    ARCHITECTURE.md VISION.md CLAUDE.md CONTRIBUTING.md BACKLOG.md 'docs/**/*.md' 'protocols/**/*.md'
real 0m0.251s
total 1406 | unique 1241 | successful 925 | excludes 349 | errors 132 (across 37 files)
```

132 errors. **126 of the 37 error-bearing files are `docs/audits/` (30) and `docs/handoffs/`
(6) — immutable artifacts.** By our own doctrine (`scan_undeclared_edges.py` prunes exactly
this set as "cannot take a `reconciled_with` line, so it is noise, not a candidate") those are
un-actionable: an ADR, audit or handoff is superseded, never edited.

**Trial B — the ACTIONABLE corpus only** (immutable + fixture trees excluded):

```
$ lychee --offline --include-fragments --exclude-path docs/audits --exclude-path docs/handoffs \
    --exclude-path docs/decisions --exclude-path docs/archive --exclude-path tests/fixtures ...
total 274 | successful 268 | errors 6
  protocols/STANDING_RULINGS.md  L380 L542 L551 L554
  JOURNAL.md                     L7270 L7283
```

**All 6 are FALSE POSITIVES, and they are the same false positive.** Read the source:

```
protocols/STANDING_RULINGS.md:380   when [#429](b) makes it structural.
protocols/STANDING_RULINGS.md:542   - **Two instances in this batch alone.** [#430](a), below. ...
JOURNAL.md:7270                     the [#430](a) conftest question, as verified fact. ...
```

Our BACKLOG-id citation grammar `[#430]` followed by a parenthetical sub-clause `(a)` **is
byte-identical to markdown link syntax** `[text](target)`. lychee — correctly, per CommonMark —
resolves `a` as a relative file and reports it missing. This is our grammar colliding with
CommonMark, not rot.

**Fairness test — is it configurable away?** Yes, in one flag:

```
$ lychee --offline --include-fragments --exclude '/[a-z]$' --exclude-path ... <actionable corpus>
total 274 | successful 268 | excludes 6 | errors 0
```

**Correctly configured, lychee finds ZERO genuine broken links in our actionable corpus.**

**Trial C — the divergence, proven on a purpose-built fixture.** Eight probe forms, one file:

| # | Probe form in the fixture | Extracted by lychee? | Verdict |
|---|---|---|---|
| 1 | bare prose `scripts/audit.py:4751` (**our 6.9% rot class**) | **no** | invisible |
| 2 | backticked `` `protocols/NOPE_DOES_NOT_EXIST.md` ``, no link syntax | **no** | invisible |
| 3 | `[missing](./gone.md)` | yes | **File not found** ✓ |
| 4 | `[real](./real.md)` | yes | pass ✓ |
| 5 | `[bad frag](./real.md#no-such-heading)` | yes | **Cannot find fragment** ✓ |
| 6 | `[good frag](./real.md#a-heading-that-exists)` | yes | pass ✓ |
| 7 | prose section cite `ARCHITECTURE.md "Ch2 Organ map"` | **no** | invisible |
| 8 | `[lineloc](./real.md:3)` | yes | reported missing — **false positive on our `path:LINE` convention** |

`total 5, successful 2, errors 3` from 8 probe forms. **lychee extracts markdown link syntax.
Our locator rot lives in prose and backticks.** Forms 1, 2 and 7 are exactly what `[#534]` is
about, and lychee sees none of them.

**Does lychee subsume the locator-rot leg? No. It finds 0 of 6 of the measured 6.9% class.**

## 1.2 The graph question — answered on measurement

**Our actual edge count**, measured live over 1,952 tracked `.md` files (repo-shaped
`dir/.../file.ext` references, prose + backticks + links):

| Source bucket | edges | dead target | with `:LINE` |
|---|---|---|---|
| actionable (root canon, `protocols/`, `ecosystem/`, `templates/`, live `docs/`) | 1,876 | 176 (9.4%) | 63 |
| `tasks/` | 761 | 30 (3.9%) | 49 |
| append-only (`JOURNAL`, `LESSONS`, `logs/`) | 3,065 | 277 (9.0%) | 88 |
| immutable (audits, handoffs, decisions, archive, fixtures) | 15,177 | 2,154 (14.2%) | 2,097 |
| **TOTAL** | **20,879** | **2,637 (12.6%)** | **2,297** |

Deduplicated: **11,684 unique (source, target) edges over 2,591 nodes.** Declared edges are a
separate, tiny layer: **120 `reconciled_with:` lines**, 2 registered specs.

**So: ~1.9k actionable edges, ~11.7k unique edges repo-wide.** That is a small graph.

### Benchmark — the four query classes, all three options, on OUR real graph

11,684 edges / 2,591 nodes, mean of 5 runs (2–3 for the expensive ones), same process:

| Query class | (a) stdlib `sqlite3` | (b) `networkx` 3.6.1 | (c) `rustworkx` 0.18.1 |
|---|---|---|---|
| build cost (load + index) | 15.06 ms | 9.32 ms | 6.17 ms |
| impact-of-move (reverse reachability from `protocols/PLAYBOOK.md`) | **4.36 ms** (recursive CTE) → 1,111 | 3.90 ms → 1,110 | **0.13 ms** → 1,110 |
| orphan detection (in-degree 0) | **1.04 ms** | 0.84 ms | 0.28 ms |
| centrality | 0.93 ms (in-degree only) | 0.85 ms degree · **pagerank needs `scipy`** | 1.48 ms pagerank, no scipy |
| **cycles / SCC** | **6,677 ms** — and **WRONG SHAPE**: a depth≤4 CTE returns 3,267 "closing walks", not cycles | 4.23 ms full SCC → 18 nontrivial · `simple_cycles(≤4)` 540 ms → 589 | **2.52 ms** full SCC → 18 |

**The crossover is NOT an edge count. It is a query class, and we have already crossed it.**

- **Reachability, orphan, degree: SQL wins on cost-of-adoption and ties on speed** (1–4 ms).
  At 11.7k edges — and at 10× that — a recursive CTE is the correct answer. Zero new
  dependency, `sqlite3` is stdlib.
- **Cycles / SCC: SQL loses today, by ~1,600×, and gives a different answer.** Unbounded SCC
  is not expressible in SQL without application code; the bounded-depth CTE that approximates
  it took 6.7 seconds and produced a walk count (3,267), not a cycle count (589) or an SCC
  count (18). This is a *correctness* gap, not a *performance* gap.
- **networkx pagerank silently requires `scipy`** (it is in networkx's `default` extra, not its
  core). Trial output, verbatim: `ModuleNotFoundError: No module named 'scipy'`. That is a
  large transitive addition for one query. `networkx` core is 19 MB on disk; `rustworkx` is
  7.1 MB and needs only `numpy`, with pagerank built in.

**Recommendation:** (a) stdlib `sqlite3` for everything except cycle/SCC. If and only if a
cycle or SCC query is actually wanted, **`rustworkx` over `networkx`** — smaller, faster,
Apache-2.0, no scipy, released 2026-07-30 vs networkx's 2025-12-08.

### ADR-105 consumers (required at ACTIVATION, permitted absent at filing)

| Option | Consumer | Consumption path |
|---|---|---|
| (a) `sqlite3` edges table | the `[#534]` locator-rot gate | a `tasks/` row citing a `scripts/*.py:<line>` that does not resolve → FAIL in `audit.py health`, at commit |
| (b)/(c) graph library | *none nameable today* | **no query we run needs cycles or SCC.** Under ADR-105 §2 that means a graph-library routine **may not activate** — filing is permitted, activation is not |

That is the evidence answer to intake #16's graph proposal: **the library is not the blocker;
the missing consumer is.** 18 nontrivial SCCs exist in our doc graph and nobody has ever asked.

## 1.3 Native doc-dependency-graph tools — surveyed, nothing fits

Three categories exist and none is our shape:

- **Docs-as-code site generators** (MkDocs, Docusaurus, Sphinx `-n` nitpick): maintain a link
  graph, but only over *rendered link syntax* — the same class as lychee, with a whole site
  build attached. Strictly worse than lychee for us.
- **Code knowledge-graph tools** (Graphify, CodeGraph MCP, RepoDoc): build queryable graphs
  over code + docs for impact analysis. LLM-oriented exploration tools, not deterministic
  gates; none has a versioned declared-edge concept.
- **Requirements-traceability tools** — the closest genuine match. **Sphinx-Needs**,
  **Doorstop**, **sphinx-graph**, **StrictDoc** maintain typed, ID'd, version-controlled object
  graphs, and **sphinx-graph tracks "suspect links" — forcing review when a linked item is
  modified**, which is precisely `reconciled_with:` semantics. But all four require our corpus
  to *become* their object model: Doorstop stores items as one-item-per-YAML-file in a DAG;
  Sphinx-Needs requires Sphinx and `:need:` directives. We would be converting 1,952 markdown
  files into a requirements database to reuse one predicate.

**Honest report: nothing fits.** The one genuinely transferable idea is sphinx-graph's *suspect
link* — a name for what `reconciled_with` already does, not a tool to adopt.

## Track 1 candidate table

| Candidate | What it replaces here | LOC it would remove | Divergence | Verdict |
|---|---|---|---|---|
| **lychee** 0.24.2 | nothing — no organ guards markdown-link rot | **0** | Extracts CommonMark link syntax only. Blind to bare prose paths (#1), backticked paths (#2), prose section cites (#7). False-positives our `[#id](a)` grammar (6/6 of its actionable findings) and our `path:LINE` convention. Finds **0 of 6** of the measured 6.9% class | **DEFER→ADOPT** as a *new* zero-baseline regression gate, not as a replacement |
| **(a) stdlib `sqlite3`** | the not-yet-built `[#534]` rot query | 0 (adds ~80) | Cannot do unbounded SCC/cycles; the depth-bounded CTE is 6.7 s and answers a different question | **ADOPT** (the default; zero new dependency) |
| **(b) `networkx`** 3.6.1 | (a), for cycle/SCC only | 0 | pagerank needs `scipy`; 19 MB; last release 2025-12-08; no consumer exists (ADR-105 §2 bars activation) | **REJECT-WITH-MEASURED-DIVERGENCE** — strictly dominated by (c) |
| **(c) `rustworkx`** 0.18.1 | (a), for cycle/SCC only | 0 | Same missing-consumer bar. Needs `numpy`. Wins on every measured axis vs (b) | **DEFER** — the right library *if* a cycle/SCC consumer is ever named |
| Sphinx-Needs / Doorstop / sphinx-graph / StrictDoc | `validate_reconciliation.py` (356) in principle | 0 in practice | Requires converting 1,952 markdown files into their object model | **REJECT-WITH-MEASURED-DIVERGENCE** |

---

# TRACK 2 — methodology deployment to consumer repos

## 2.0 What we actually have

`deploy/` = **7,460 Python LOC** (verified: `find deploy -name '*.py' | xargs wc -l`). It is
not one thing:

| Component | LOC | Role |
|---|---|---|
| `deploy/tool.py` | 1,336 | the runbook driver — preflight, ordering, version-record write |
| `carrier_precommit.py` | 976 | pinned pre-commit hooks + rev ancestry |
| `carrier_floor.py` | 946 | floor body + **sha256 sidecar** + `check_floor_hash.py` + `CLAUDE.md` include + `.gitignore` negation + `settings.json` arm leg |
| `release_lint.py` | 463 | release-shape lint |
| `floor_conformance.py` | 443 | floor conformance |
| `carrier_plugin.py` | 390 | `claude plugin` CLI, judged from resulting state |
| `carrier_mesh.py` | 296 | ports two fail-closed organs into the consumer |
| `carrier_docs.py` | 278 | **fully manifest-driven** source→dest doc copy |
| `contract.py` | 214 | `CarrierState` / `ApplyResult` / `VerifyResult` |
| `carrier_globalconfig.py` | 213 | `~/.codex/AGENTS.md` — **user-machine scoped, not repo scoped** |
| **`lived_sandbox/` (7 files)** | **1,905** | **clone-the-consumer-in-isolation verification harness — not a carrier at all** |

## 2.1 copier — trial, end to end

`copier 9.17.2`, MIT, `python>=3.10`, released **2026-08-19 — two days before this lane**.
Deps: `colorama, dunamai, funcy, jinja2, jinja2-ansible-filters, packaging`. Pure Python →
Windows + Linux. Actively maintained; Renovate ships a **native `copier` manager** (see §2.4).

**Trial: build a template → generate a consumer → consumer edits locally → hub ships a rev bump
→ `copier update`.**

```
template v1.4.0:  .pre-commit-config.yaml.jinja (ruff rev v0.15.5)
                  .claude/CLAUDE-FLOOR.md.jinja
                  CLAUDE.md.jinja   (_skip_if_exists)
                  {{_copier_conf.answers_file}}.jinja

$ copier copy --trust --defaults --data repo_name=ai-council --vcs-ref v1.4.0 ./tmpl consumer
$ cat consumer/.copier-answers.yml
_commit: v1.4.0
_src_path: .../tmpl
methodology_version: 1.4.0
repo_name: ai-council

# consumer hand-tunes its config (args: ["--fix"] + a local comment), commits
# hub ships v1.5.0 (ruff rev v0.15.5 -> v0.16.0)

$ copier update --trust --defaults
Updating to template version 1.5.0

$ cat consumer/.pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.0            <-- HUB CHANGE APPLIED
    hooks:
      - id: ruff
        args: ["--fix"]     <-- CONSUMER EDIT PRESERVED
# methodology corpus 1.4.0
# LOCAL: consumer-owned extra hook   <-- CONSUMER EDIT PRESERVED
```

**The three-way merge does exactly what it claims.** `_commit` advanced `v1.4.0 → v1.5.0` — and
that field **is** `deployed-versions.yaml`, per consumer, living in the consumer.

**Two real gotchas found in the trial, both worth recording:**

1. **`.copier-answers.yml` is not automatic.** It exists only because the template ships a
   `{{_copier_conf.answers_file}}.jinja` file. Omit it and you get a consumer with no version
   record and no updatable state — the failure is *silent* (trial run 1: no answers file, no
   warning).
2. **An answer is not a template ref.** `methodology_version` stayed `1.4.0` across the update
   to `v1.5.0`, because `--defaults` re-uses recorded answers rather than re-reading the new
   default. Any corpus-version string must come from `_commit`, never from an answer.

**The hash-guarded floor (ADR-93) — tested directly.** `_tasks` can regenerate the sidecar:

```
_tasks:
  - "python -c \"...sha256(CLAUDE-FLOOR.md)... -> CLAUDE-FLOOR.md.sha256\""

$ copier copy --trust ... consumer2
 > Running task 1 of 1: python -c "..."
$ cat consumer2/.claude/CLAUDE-FLOOR.md.sha256
d36ed4170968c1656a3f4d3e8c667fb0e41b9c326927fd060c52edb1a0c98785
```

So the floor **is** expressible. **But without `--trust` copier refuses the whole render:**

```
$ copier copy --defaults ... consumer3
Template uses potentially unsafe feature: tasks.
If you trust this template, consider adding the `--trust` option ...
exit code = 4    # and the destination tree is EMPTY — fail-closed, nothing half-written
```

That is the right failure mode (nothing half-armed), but it means **every consumer must pass
`--trust` on every copy and every update**, forever, or the floor never renders.

**copier's real gap: there is no drift CHECK.** `copier update --pretend` exits **0 whether or
not the consumer is behind**:

```
$ copier update --trust --defaults --pretend    # consumer at v1.6.0, template at v1.7.0
Updating to template version 1.7.0
exit=0                                          # tree unchanged, rev still v0.16.0
```

You can compare `_commit` to the template's newest tag yourself in ~5 lines, but there is no
`copier check`.

## 2.2 cruft — trial, and the maintenance signal that decides it

`cruft 2.16.0`, MIT — **released 2024-12-25. Twenty months stale as of this lane.** Deps:
`click, cookiecutter, gitpython, toml, typer`.

The trial works, and its differentiator is real:

```
$ cruft check          # in sync
SUCCESS: Good work! Project's cruft is up to date and as clean as possible :).
exit=0

# hub ships a rev bump

$ cruft check          # drifted
FAILURE: Project's cruft is out of date! Run `cruft update` to clean this mess up.
exit=1                 # <-- the CI-gateable check copier does NOT have

$ cruft update         # applies the diff
    rev: v0.16.0
```

`cruft check --exit-code` is genuinely the thing copier lacks. But it rides cookiecutter (no
native 3-way merge — cruft reconstructs one from a git diff), it has no `_tasks` equivalent for
the floor sidecar, and **a 20-month-old release on a tool that sits in the fleet's distribution
path is the disqualifying signal.** Reimplementing `cruft check` on top of copier is a ~5-line
`_commit`-vs-newest-tag comparison; recovering an unmaintained dependency is not a 5-line job.

## 2.3 Carrier-by-carrier mapping — the honest split

| Carrier | LOC | Under copier | Why |
|---|---|---|---|
| `carrier_docs` | 278 | **template material** — pure win | Already fully manifest-driven source→dest copy. This is literally what a template subdirectory is |
| `carrier_precommit` | 976 | **mostly template**, ~150–200 LOC stays | `.pre-commit-config.yaml.jinja` renders trivially. But `expected_rev_from: deployed-versions` + `ancestry: true` (a `git merge-base --is-ancestor` on the hub tag) is not templating |
| `carrier_floor` | 946 | **template + `_tasks`**, ~150 LOC stays | Body/`CLAUDE.md`/`.gitignore`/`settings.json` all template cleanly; sidecar via `_tasks` (proven above). The **verify** leg — re-read and confirm armed at full stage cardinality — has no copier equivalent |
| `carrier_globalconfig` | 213 | **stays bespoke** | Target is `~/.codex/AGENTS.md`, **outside the consumer repo**. copier renders into one destination directory |
| `carrier_plugin` | 390 | **stays bespoke** | Shells out to `claude plugin`, then judges from `claude plugin list --json` + `settings.json` — deliberately never from the CLI's self-report. Not a file operation |
| `carrier_mesh` | 296 | **template material**, ~50 LOC stays | Byte-copies two scripts + one command file. The arming half is `carrier_precommit`'s |
| `contract.py` | 214 | **deleted** | `CarrierState`/`ApplyResult`/`VerifyResult` is the abstraction copier replaces |
| `tool.py` | 1,336 | **~400 stays** | Preflight, ordering, `deployed-versions.yaml` write. `_commit` subsumes the version record; the ADR-102 `gate_rev_ahead` declaration does not |
| `release_lint` + `floor_conformance` | 906 | **stays** | Hub-side release-shape lint; not a deploy mechanism |
| `lived_sandbox/` | 1,905 | **stays, entirely** | Clone-consumer-in-isolation verification. copier has no verification concept whatsoever |

**Honest LOC estimate: 7,460 → ~3,700–4,000.** A ~3,500-LOC removal, ~47%. **Not 90%**, and the
reason is structural: **copier is a renderer, not a reconciler.** Our carriers implement
detect → apply → **verify**; copier implements render → 3-way-merge. The verify half — the half
that catches "the plugin says installed but is not enabled", "the arm leg names only 2 of 3
stages", "the floor bytes are right but the sidecar is stale" — has no library equivalent and
is where `lived_sandbox`'s 1,905 LOC and much of the carriers' bulk actually lives.

**Migration cost for the two deployed consumers.** Both are *retrofits*, not greenfield —
copier's designed-for path is `copier copy` into an empty tree.

- **ai-council @ 1.3.1** — the full-corpus consumer. Cost: author the template at a tag matching
  what ai-council already has; hand-write `.copier-answers.yml` with `_commit: v1.3.1`; run
  `copier update --trust` to v1.4.0 and resolve conflicts. Every file copier now owns that
  ai-council edited locally becomes a merge conflict **once**, then never again. Estimate: one
  session, mechanical, with a real conflict tail.
- **corp-monorepo @ 1.2.0** — materially harder, and the reason is already documented in
  `parity-surfaces.yaml`. corp's corpus is `1.2.0` while its hub-block gate pin is `v1.3.1`
  (ADR-102 `gate_rev_ahead`), **and corp removed the `codemap-freshness` hook (#276 unlanded)**.
  Under copier both are template drift. `_skip_if_exists` covers a file corp owns entirely; it
  does **not** express "this hook was deliberately removed from a file the template owns". That
  needs either a conditional include keyed on an answer, or a permanent conflict on every
  update. **The ADR-102 declared-divergence model has no copier representation.** That is the
  single biggest migration risk in this track.

## 2.4 "Copy + update" vs "reference by version" — and what we already do

**We are already doing "reference by version", and it is already the smaller half.**
`.pre-commit-hooks.yaml` exists (ADR-71) and publishes **6 hook ids** — `codemap-freshness`,
`codemap-generate`, `toc-freshness`, `toc-generate`, `backlog-id-on-close`, `block-ff-push`.
Consumers pin the hub by `rev:`. Tags live: `v1.0.0 v1.2.0 v1.3.0 v1.3.1`. The
`precommit-hub-block` parity surface probes exactly this, with `ancestry: true`.

| Axis | Copy + update (copier/cruft/our carriers) | Reference by version (remote hooks / reusable workflows) |
|---|---|---|
| LOC that scales with N repos | zero for us; the consumer holds a merge burden | zero for both |
| Consumer can locally diverge | **yes** — the point of 3-way merge | **no** — take it or unpin it |
| Update propagation | pull, per consumer, one PR each | instant on rev bump; but consumers pin, so still a PR each |
| **Offline** | **works** — files are in the tree | **breaks**: `pre-commit` clones the hook repo on first use; a reusable workflow resolves at run time on GitHub |
| **Private repos** | works — copier over `git+ssh` fine | **the sharp edge**: a reusable workflow in a private repo needs that repo's Actions **Access policy** explicitly opened to the caller repos, and doing so gives outside collaborators on caller repos indirect access. Limits: 10 nesting levels, 50 unique reusable workflows per file |
| Failure mode | stale silently | **breaks loudly** — a deleted tag breaks every consumer at once |
| Fits `carrier_floor` | yes | **no** — the floor must be a file in the consumer tree; `check_floor_hash.py` must travel with the clone (ADR-93's whole point) |
| Fits `carrier_mesh` | yes | **no** — the fire_test clones the consumer in isolation; every script an organ invokes must physically exist there |

**The strategies are not competitors — the boundary is already drawn correctly and for a
recorded reason.** Enforcement *pins* reference by version (6 hooks today). Everything that
must survive an isolated clone — floor, mesh, docs, plugin — must be copied. Nothing in this
research argues for moving either across the line. **We have no `.github/` CI beyond
`report-only-wall.yml`**, so reusable workflows would be a new surface with no existing caller
— and, under ADR-105, no consumer.

## Track 2 candidate table

| Candidate | What it replaces here | LOC it would remove | Divergence | Verdict |
|---|---|---|---|---|
| **copier** 9.17.2 | `carrier_docs`, most of `carrier_precommit`/`carrier_floor`/`carrier_mesh`, `contract.py`, ~⅔ of `tool.py` | **~3,500 of 7,460 (~47%)** | No verify concept (leaves `lived_sandbox` 1,905 + verify legs). No drift check (`--pretend` exits 0 regardless). `_tasks` needs `--trust` on every run or nothing renders. **No representation for ADR-102 declared divergence** (corp's `gate_rev_ahead` + removed hook). Can't reach `~/.codex/` or drive `claude plugin` | **ADOPT — but scoped**, greenfield-first, corp retrofit last |
| **cruft** 2.16.0 | same surface as copier | similar | Cookiecutter-based, no native 3-way merge, no `_tasks`. **Last release 2024-12-25 — 20 months stale.** Its one advantage (`check --exit-code`) is ~5 lines on top of copier's `_commit` | **REJECT-WITH-MEASURED-DIVERGENCE** — maintenance signal decides it |
| **reusable GH Actions workflows** | nothing today | 0 | Breaks offline; private-repo access policy leaks indirect access to outside collaborators; cannot carry the floor or mesh (must survive an isolated clone). No caller repo exists (`.github/` holds one workflow) | **REJECT-WITH-MEASURED-DIVERGENCE** |
| **pre-commit remote hook repos** | — | 0 | **Already adopted** (ADR-71, 6 hook ids, tags `v1.0.0`–`v1.3.1`). Breaks offline on first clone. Structurally cannot carry floor/mesh | **ADOPT — already done**; the boundary is correct, extend only to hooks that need no local file |

---

# TRACK 3 — fleet parity / conformance as data, not as Python

## 3.0 The premise is already half-true — and that changes the verdict

`fleet_parity.py` is **not** "one Python function per conformance rule". It is a **probe engine
over a declarative manifest**:

- `ecosystem/parity-surfaces.yaml` — **998 lines, 83 declared surfaces, 9 surface kinds, 9 fleet
  members**, `version: 1.4.0`
- `scripts/fleet_parity.py` — 2,049 LOC, 50 functions, implementing **17 probe types**
  (`_PROBE_REQUIRED_FIELDS`, `scripts/fleet_parity.py:224`)
- `ecosystem/schema/desired_state.py` — **650 LOC of pydantic** (ADR-109). **pydantic is already
  adopted**, at `>=2.0,<3`

So **the measured cost of adding one conformance rule today is already ONE YAML ROW**, provided
its probe type exists. The Python bulk is not rules — it is `_eval_row` (210), `collect_facts`
(201), `load_manifest` (159), `resolve_fleet` (77), rendering and event emission.

**The real cost question is therefore: what does a rule of a NEW KIND cost?** That is where the
candidates get evaluated, and it is a much narrower target than the brief assumed.

## 3.1 Worked example — one REAL surface, in all four syntaxes

Surface: **ruff pre-commit gate** — `.pre-commit-config.yaml` must carry
`astral-sh/ruff-pre-commit` at `rev: v0.15.5` with hook id `ruff`. Run against the live hub
config (clean) and a `rev: v0.14.0` mutation (drifted).

**Ours today (`parity-surfaces.yaml`), ~10 lines, no code:**

```yaml
- id: precommit-ruff-gate
  kind: precommit-hook
  tier: {hub: MUST, consumer: MUST}
  probe: {type: precommit_hook, hook_id: ruff}
  ownership: {value: methodology-generic, reason: ..., provenance: [...]}
```

**(a) conftest / OPA Rego** — `conftest 0.69.0` / `OPA 1.19.0`, Apache-2.0, **69.5 MiB** Go
binary, Windows/Linux/macOS assets (probed → 302). Latest release 2026-08-03.

```rego
package main
surfaces := [{"id": "precommit-ruff-gate",
              "repo": "https://github.com/astral-sh/ruff-pre-commit",
              "rev": "v0.15.5", "hook_ids": ["ruff"], "tier": "MUST"}, ...]

repo_by_url(url) := r if { some r in input.repos; r.repo == url }
hook_ids(r) := {h.id | some h in r.hooks}

deny contains msg if { some s in surfaces; s.repo; not repo_by_url(s.repo)
  msg := sprintf("%s: MUST — repo %v absent", [s.id, s.repo]) }
deny contains msg if { some s in surfaces; r := repo_by_url(s.repo); r.rev != s.rev
  msg := sprintf("%s: rev pinned %v, declared %v", [s.id, r.rev, s.rev]) }
deny contains msg if { some s in surfaces; r := repo_by_url(s.repo)
  some want in s.hook_ids; not hook_ids(r)[want]
  msg := sprintf("%s: hook id %v absent", [s.id, want]) }
```

```
$ conftest test --policy policy hub-precommit.yaml   -> 3 tests, 3 passed        exit 0
$ conftest test --policy policy drifted.yaml
FAIL - drifted.yaml - main - precommit-ruff-gate: rev pinned v0.14.0, declared v0.15.5
                                                  3 tests, 2 passed, 1 failure   exit 1
```

39 LOC of Rego covers 2 surfaces. Message quality is **excellent** — surface id + expected +
actual, matching our `ParityFinding` shape.

**(b) check-jsonschema** 0.38.0, Apache-2.0, released 2026-08-09. Deps: `ruamel.yaml`,
`jsonschema`, `regress`, `requests`, `click`.

```json
{"type":"object","required":["repos"],"properties":{"repos":{"type":"array","contains":{
  "type":"object","required":["repo","rev","hooks"],"properties":{
    "repo":{"const":"https://github.com/astral-sh/ruff-pre-commit"},
    "rev":{"const":"v0.15.5"},
    "hooks":{"type":"array","contains":{"required":["id"],"properties":{"id":{"const":"ruff"}}}}}}}}}
```

```
$ check-jsonschema --schemafile precommit.schema.json hub-precommit.yaml   exit 0
$ check-jsonschema --schemafile precommit.schema.json drifted.yaml         exit 1
Schema validation errors were encountered.
  drifted.yaml::$.repos: [{'repo': 'local', 'hooks': [ ...THE ENTIRE 18-HOOK ARRAY... ]}]
      does not contain items matching the given schema
```

19 lines, 1 surface — **and the error message is unusable.** `contains` reports only that the
array failed; it dumps ~2 KB of unrelated config and never names the rev, the surface, or the
constraint. Compare conftest's one precise line. Our findings carry an action per surface; this
carries none.

**(c) pydantic** 2.13.4, MIT — **already in `[dependency-groups] dev`**.

```python
class PreCommit(BaseModel):
    repos: list[Repo]
    @field_validator("repos")
    @classmethod
    def ruff_gate(cls, v):
        m = [r for r in v if r.repo == "https://github.com/astral-sh/ruff-pre-commit"]
        if not m: raise ValueError("precommit-ruff-gate: MUST - ruff-pre-commit absent")
        if m[0].rev != "v0.15.5":
            raise ValueError(f"precommit-ruff-gate: rev pinned {m[0].rev}, declared v0.15.5")
        if "ruff" not in {h.id for h in m[0].hooks}:
            raise ValueError("precommit-ruff-gate: hook id ruff absent")
        return v
```

```
pydantic  clean    -> PASS
pydantic  drifted  -> FAIL: precommit-ruff-gate: rev pinned v0.14.0, declared v0.15.5
```

22 LOC, 1 surface. Message quality equals conftest. **But this is Python-per-rule — the exact
shape the track set out to escape.** pydantic is the right tool for the *schema* of
`parity-surfaces.yaml` (which is what ADR-109 already uses it for) and the wrong tool for the
*rules inside it*.

**(d) deepdiff** 9.1.0, MIT, released 2026-05-15. Deps add `cachebox`, `orderly-set`.

```python
declared = {"repos": {"https://github.com/astral-sh/ruff-pre-commit":
                      {"rev": "v0.15.5", "hooks": ["ruff"]}}}
def project(doc): ...   # hand-written, per surface KIND
DeepDiff(declared, project(doc), ignore_order=True)
```

```
deepdiff  clean    -> PASS (empty diff)
deepdiff  drifted  -> {'values_changed':
  {"root['repos']['https://github.com/...ruff-pre-commit']['rev']":
     {'new_value': 'v0.14.0', 'old_value': 'v0.15.5'}}}
```

6 LOC — **but only after a hand-written projection function per surface kind**, and the
projection is where all the work lives. deepdiff diffs two dicts; it cannot produce the
"live" dict. Excellent message quality once you have it.

## 3.2 Cost of adding one rule — measured

| | Adding a rule of an EXISTING kind | Adding a rule of a NEW kind |
|---|---|---|
| **Today** | **1 YAML row (~10 lines), no code, no test** | Python probe + `_PROBE_REQUIRED_FIELDS` entry + test |
| conftest/Rego | 1 entry in a `surfaces` data array | ~8–12 lines of Rego **if the fact is in a parsed file**; **impossible if not** |
| check-jsonschema | 1 schema fragment | same, plus an unusable error message |
| pydantic | 1 validator method (~10 LOC Python) | same — no improvement over today |
| deepdiff | 1 declared-dict entry | a new projection function (Python) |

**Nothing here beats "1 YAML row".** The candidates compete only on the *new-kind* column, and
there conftest is the only real contender — bounded by what it can see.

## 3.3 The divergence, stated honestly — which of our checks are NOT declarative

Rego (and every other candidate here) evaluates **parsed structured documents**. It cannot run a
process. Of our 17 probe types, these are **not expressible declaratively**, with the surfaces
that use them:

1. **`check_ignore`** (9 surfaces, all `gitignore-effect`) — requires `git check-ignore`.
   `.gitignore` is a *program*: negations, precedence, per-directory files. Text-matching it
   is exactly the "never text-grep where an effect probe exists" anti-pattern FR-6 forbids.
2. **`precommit_remote` with `ancestry: true`** (`precommit-hub-block`) — `expected_rev_from:
   deployed-versions` resolves a version from a *different file in a different repo*, then
   asserts **git tag ancestry** (`merge-base --is-ancestor`). Two facts and a git operation
   conftest cannot reach from one input document.
3. **`plugin_enabled`** — the truth is `claude plugin list --json` plus the consumer's
   `settings.json`, and `carrier_plugin.py` exists precisely because the CLI's self-report is
   untrustworthy. An external process.
4. **`path_tracked` / `dir_tracked` / `glob_tracked`** (52 `path` surfaces — **63% of all
   surfaces**) — "tracked" means `git ls-files`, not "exists". No parsed document contains it.
5. **`commands_roster` / `claude_subtrees` / `settings_local_blocks` / `ruff_config_form`** —
   filesystem enumeration and cross-file joins.
6. **The whole declaration layer** — `gate_rev_ahead` (ADR-102), `ownership` (ADR-103), waivers,
   `declared_divergence`, and `_declaration_bad`'s shared reason+provenance grammar. This is
   where "diverge" becomes "declared". Rego could validate the *grammar*; the *semantics* —
   "self-invalidates once `deployed source_tag` reaches `gate_tag_raw`" — is a cross-file join
   over live git state.

**Bluntly: at least 5 of 9 surface kinds and ~63% of surfaces rest on `git` or a subprocess.
They justify the Python that remains, and the Python that remains is most of the 2,049 lines.**

## Track 3 candidate table

| Candidate | What it replaces here | LOC it would remove | Divergence | Verdict |
|---|---|---|---|---|
| **conftest / OPA (Rego)** | the *evaluation* half for parsed-file surfaces only (`precommit-hook`, some `doc-marker`) | **~150–250 of 2,049**, and adds a 69.5 MiB binary + Rego as a second policy language | Cannot run `git check-ignore`, resolve tag ancestry, call `claude plugin list`, or `git ls-files`. Blind to ≥5 of 9 surface kinds and ~63% of surfaces. Would **split** one manifest into YAML + Rego — two sources of truth for one contract | **REJECT-WITH-MEASURED-DIVERGENCE** |
| **check-jsonschema** | validation of `parity-surfaces.yaml`'s own shape | ~0 (pydantic already does this) | `contains` produces unactionable errors (dumps the whole array, names no constraint). Adds `requests` + `ruamel.yaml` + `jsonschema` + `regress` | **REJECT-WITH-MEASURED-DIVERGENCE** |
| **pydantic** 2.13.4 | — | — | **Already adopted** (`>=2.0,<3`), already carrying `ecosystem/schema/desired_state.py` (650 LOC). Extending it to *rules* re-introduces Python-per-rule | **ADOPT — already done**; do not extend to rules |
| **deepdiff** 9.1.0 | the *comparison* step inside `_eval_row` | **~50–100**, honestly | Needs a hand-written projection per surface kind — the projections are the work, and they stay Python. Adds `cachebox` + `orderly-set` | **DEFER** — real but small; revisit only if a state-vs-declared diff report is actually wanted |

---

# TRACK 4 — tech currency and dependency freshness

## 4.0 What the sentinel actually watches — and why it decides the verdict

`scripts/changelog_sentinel.py` (120 LOC) compares **installed agent-tool versions**
(`claude --version`, `codex --version`) against `ecosystem/tool-versions.yaml`
`last_reviewed_version`. It is **LOCAL ONLY, no network, fail-soft**, wired to `SessionStart`.
The fetch happens only in the operator-invoked `/changelog-review` (push trigger).

**`claude --version` is not a manifest.** No bot on earth reads it. Renovate and Dependabot read
*committed dependency files*. Our manifests: `uv.lock`, `pyproject.toml`,
`.pre-commit-config.yaml`, `package.json`, `package-lock.json`, plus
`ecosystem/dependency-baseline.yaml` (our own, unknown to both bots).

**These are orthogonal axes.** The sentinel watches *the tools we drive*; the bots watch *the
libraries we depend on*. Neither replaces the other.

## 4.1 Renovate vs Dependabot against our specific discipline

| | Renovate | Dependabot |
|---|---|---|
| `uv.lock` | supported | supported (uv among 30+ ecosystems) |
| pre-commit `rev:` | supported — **`pre-commit` manager is disabled by default**, must be opted in | supported **since 2026-03-10** (parses `.pre-commit-config.yaml`, PRs the `rev:`) |
| exact-pin discipline (`ruff==0.15.5` ↔ `rev: v0.15.5` ↔ `required-version`) | **`packageRules` + `groupName` can force all three into ONE PR** — the only way our exact-match invariant survives an automated bump | **no cross-manifest grouping** — three PRs, and merging one alone **breaks the invariant** and reddens the hub |
| `required-version = "==0.11.19"` (uv itself) | custom manager (regex on `pyproject.toml`) | not a dependency it models |
| **copier / cruft template updates** | **native `copier` manager** — matches `.copier-answers(\..+)?\.ya?ml`, reads `_commit`, opens the "template moved" PR | **none** |
| Self-hosting | yes (also a GitHub App) | GitHub-native only |

**Renovate wins on all three axes that matter to us**, and the third is decisive: **it closes
Track 2's missing half at zero LOC.** copier has no drift check; Renovate's copier manager *is*
the drift check, delivered as a PR per consumer, fleet-wide, maintained by someone else.

**One constraint, stated plainly:** we have essentially no CI (`.github/workflows/` holds one
file, `report-only-wall.yml`). Both bots produce **pull requests**, and this fleet's workflow is
local `--no-ff` merges with `block-ff-push` armed. An automated PR that nobody reviews is
exactly the ADR-105 §2 failure — `[#419]`, *"we run routines whose output nobody consumes"*.
**Under ADR-105 a Renovate lane may not ACTIVATE without a named `consumer` and
`consumption_path`.** That is precisely what `[#495]` already exists to rule.

## 4.2 Replace or complement — the one-paragraph read

**Complement, unambiguously, and the two halves do not touch.** The sentinel answers *"has the
tool I drive shipped a changelog I have not read?"* — a question about **agent tooling
semantics**, resolved by a human reading release notes, whose durable output is a reviewed-version
stamp and a digest. Renovate answers *"is a pinned library behind its upstream?"* — a question
about **dependency versions**, resolved by a bot opening a PR. Renovate cannot read
`claude --version` off the operator's machine; the sentinel cannot see `uv.lock`. Adopting
Renovate would leave `changelog_sentinel.py` untouched at 120 LOC and would supply the
**distribution half `[#385]` names as missing** — proposals landing as PRs against the pinned
manifests, exactly the "research → proposal → ruled → distributed" path, with Renovate as the
mechanical producer and the operator's merge as the ruling. It does **not** supply `[#385]`'s
research half (new-tech discovery), and `[#495]`'s cadence question is answered by config
(`schedule:`), not by adoption.

## Track 4 candidate table

| Candidate | What it replaces here | LOC it would remove | Divergence | Verdict |
|---|---|---|---|---|
| **Renovate** | nothing — supplies `[#385]`'s missing distribution half | **0** (adds a `renovate.json`, ~40 lines of config) | Produces PRs; we merge locally with `block-ff-push`. Cannot see `claude --version` (the sentinel's axis). Needs `groupName` or the exact-pin trio breaks. **ADR-105 bars activation without a named consumer + consumption path — `[#495]`'s open question** | **ADOPT — gated on `[#495]` ruling the cadence + consumer** |
| **Dependabot** | same surface | 0 | **No cross-manifest grouping** → the `ruff==0.15.5` / `rev: v0.15.5` / `required-version` trio splits into 3 PRs and merging one alone reddens the hub. **No copier manager** — cannot drive Track 2's updates | **REJECT-WITH-MEASURED-DIVERGENCE** |
| **`changelog_sentinel.py`** (keep) | — | — | Watches a different axis entirely. Nothing here replaces it | **KEEP — complement, not replace** |

---

# ORDERED RECOMMENDATIONS — cheapest highest-leverage first

Ordered by (leverage ÷ cost), each carrying the intake-or-row it needs.

**1. lychee as a zero-baseline markdown-link gate on the ACTIONABLE corpus.**
Cost: one `.pre-commit-config.yaml` block, one `lychee.toml`, no Python, no `uv` exposure, no
LOC. Leverage: guards a real class nobody guards, from a **measured baseline of exactly 0
errors** — the cheapest possible moment to arm a gate. Requires `--exclude '/[a-z]$'` for the
`[#id](a)` grammar collision and the five `--exclude-path` entries for immutable trees; both are
config, both proven above. Honest scope: this is **not** `[#534]`.
→ **needs: a new [P3][S] BACKLOG row.** kill-candidates: none — no row owns markdown-link rot.

**2. Ruling that intake #16's graph library is not adopted, on this evidence.**
Cost: zero — a disposition, not a build. Leverage: closes a standing question with measurement
instead of assertion. The finding: at 11,684 edges, stdlib `sqlite3` answers reachability,
orphan and degree in 1–4 ms; a graph library wins **only** on cycles/SCC (~1,600× — a
correctness gap, not just speed); and **no consumer for a cycle/SCC query exists**, so ADR-105
§2 bars activation regardless. If one is ever named, it is `rustworkx`, not `networkx`.
→ **needs: a disposition on intake #16 §3.** No new row.

**3. Renovate, with the exact-pin trio grouped — gated on `[#495]`.**
Cost: `renovate.json` (~40 lines), zero LOC. Leverage: supplies `[#385]`'s missing distribution
half, **and** delivers the drift check copier lacks via the native `copier` manager, so it pays
off twice. Must use `packageRules`/`groupName` to keep `ruff==0.15.5` ↔ `rev: v0.15.5` ↔
`required-version` in one PR. **Blocked until `[#495]` rules the cadence and names the ADR-105
consumer + consumption path** — that is exactly what `[#495]` is for.
→ **needs: `[#495]` (open, DEFER, peg: rules with the `[#385]` arc). No new row.**

**4. `[#534]`'s `path:LINE` locator gate, built on stdlib `sqlite3` — not on any library here.**
Cost: ~80 LOC, zero dependencies. Leverage: closes the measured 6.9% rot on a real, dangerous
class (a dead locator about to be ratified as met). Confirmed by trial: **no surveyed tool
finds this class** — lychee scores 0 of 6, and requirements-traceability tools would require
converting 1,952 markdown files into their object model.
→ **needs: `[#534]` (open). No new row.** This report is the library-first negative result its
build was owed.

**5. copier, scoped: greenfield-first, corp-monorepo last.**
Cost: one session to author the template; a real conflict tail per retrofit. Leverage: **~3,500
of 7,460 LOC (~47%)**, and the line count stops scaling with N. Sequence: (a) template + a
greenfield consumer; (b) ai-council retrofit at `_commit: v1.3.1`; (c) **corp-monorepo last**,
because ADR-102 `gate_rev_ahead` + the removed `codemap-freshness` hook have **no copier
representation** and that is the migration's single biggest risk. Verify halves stay ours:
`lived_sandbox/` (1,905), `carrier_plugin` (390), `carrier_globalconfig` (213). Requires
`--trust` on every copy and update, forever, or the floor never renders.
→ **needs: intake #25 (copier is already the named-but-unbuilt library there) — promoted with
the ADR-102 representation gap recorded as an open question.**

**6. deepdiff inside `_eval_row`'s comparison step — DEFER, revisit only on demand.**
Cost: 2 new transitive deps (`cachebox`, `orderly-set`). Leverage: honestly ~50–100 LOC. Do not
do this on its own merits; revisit only if a state-vs-declared **diff report** is wanted, since
the per-kind projections that make it work stay Python either way.
→ **needs: nothing today.** Recorded here so it is not re-researched.

**Explicitly NOT recommended, with the measurement that kills each:** cruft (last release
2024-12-25, 20 months stale, in the fleet's distribution path); conftest/OPA (blind to ≥5 of 9
surface kinds and ~63% of surfaces — all the `git`-backed ones — and would split one manifest
into two sources of truth); check-jsonschema (`contains` errors name no constraint and dump the
whole array); Dependabot (no cross-manifest grouping breaks our exact-pin invariant; no copier
manager); reusable GitHub Actions workflows (breaks offline, private-repo access policy leaks
indirect access, and structurally cannot carry the floor or mesh); Sphinx-Needs / Doorstop /
sphinx-graph / StrictDoc (would require converting 1,952 markdown files into a requirements
object model to reuse one predicate).

---

## Appendix A — every tool trialled, with its maintenance signal

| Tool | Version trialled | Released | Licence | Windows | Install path | Deps added |
|---|---|---|---|---|---|---|
| lychee | 0.24.2 | 2026-05-01 | Apache-2.0 OR MIT | yes (msvc asset, probed 302) | static binary / pre-commit — **no `uv`** | none |
| conftest | 0.69.0 (OPA 1.19.0) | 2026-08-03 | Apache-2.0 | yes (asset probed 302) | 69.5 MiB binary | none (new language) |
| copier | 9.17.2 | **2026-08-19** | MIT | yes (pure Python) | `uv` — **UNVERIFIED, see §0.1** | colorama, dunamai, funcy, jinja2, jinja2-ansible-filters, packaging |
| cruft | 2.16.0 | **2024-12-25** | MIT | yes (pure Python) | `uv` — UNVERIFIED | click, cookiecutter, gitpython, toml, typer |
| networkx | 3.6.1 | 2025-12-08 | BSD-3-Clause | yes | `uv` — UNVERIFIED | none core; **pagerank needs `scipy`**; 19 MB |
| rustworkx | 0.18.1 | 2026-07-30 | Apache-2.0 | yes (wheels) | `uv` — UNVERIFIED | numpy; 7.1 MB |
| check-jsonschema | 0.38.0 | 2026-08-09 | Apache-2.0 | yes | `uv` — UNVERIFIED | ruamel.yaml, jsonschema, regress, requests, click |
| pydantic | 2.13.4 | 2026-05-06 | MIT | yes | **already adopted** `>=2.0,<3` | — |
| deepdiff | 9.1.0 | 2026-05-15 | MIT | yes | `uv` — UNVERIFIED | cachebox, orderly-set |
| Renovate | hosted / self-hosted | continuous | AGPL-3.0 (self-hosted) | n/a (service) | `renovate.json` | none |
| Dependabot | GitHub-native | continuous | n/a | n/a (service) | `.github/dependabot.yml` | none |

## Appendix B — reproducing the trials

All trials ran on **throwaway copies under `$SCRATCH`**, never in the tree. The clone:
`git clone --depth 1 file:///home/user/dev-knowledge dk` @ `700e677`. Python trials ran in a
plain `python -m venv` (CPython 3.11.15) — **not** under our pinned `uv`; see §0.1.

```
# Track 1 — our live baselines (read-only, run in-tree)
python scripts/scan_undeclared_edges.py     # -> 19 candidate(s), 4 weak signal(s)
python scripts/validate_doc_rot.py          # -> 20 loci: 19 backlog-row-length + 1 grooming-cadence

# Track 1 — lychee
curl -sSL -o lychee.tar.gz \
  https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz
lychee --offline --include-fragments --no-progress --format json \
  ARCHITECTURE.md VISION.md CLAUDE.md CONTRIBUTING.md BACKLOG.md 'docs/**/*.md' 'protocols/**/*.md'
lychee --offline --include-fragments --exclude '/[a-z]$' \
  --exclude-path docs/audits --exclude-path docs/handoffs --exclude-path docs/decisions \
  --exclude-path docs/archive --exclude-path tests/fixtures <actionable corpus>

# Track 1 — graph benchmark (11,684 edges / 2,591 nodes, mean of 5)
#   sqlite3 recursive CTE vs networkx vs rustworkx over the live edge set

# Track 2 — copier / cruft
copier copy --trust --defaults --data repo_name=ai-council --vcs-ref v1.4.0 ./tmpl consumer
copier update --trust --defaults           # 3-way merge; --pretend exits 0 regardless
cruft check                                # exit 0 clean / exit 1 drifted

# Track 3 — conftest / check-jsonschema / pydantic / deepdiff
conftest test --policy policy hub-precommit.yaml      # exit 0
conftest test --policy policy drifted.yaml            # exit 1, names surface + expected + actual
check-jsonschema --schemafile precommit.schema.json drifted.yaml   # exit 1, unactionable message
```

Scratch state (throwaway clone, venv, four trial dirs, two downloaded binaries) is confined to
the session scratchpad and is not part of this repo — **no leftovers in the tree** (CLAUDE.md
§5 rule 9): `git status` clean apart from this artifact and the lane contract.
