# CLOUD LANE — LIBRARY-FIRST RESEARCH: THE FOUR SCALING SURFACES · frozen contract of record · 2026-08-21

**FROZEN CONTRACT OF RECORD.** Saved verbatim as the FIRST COMMIT of the lane, before any
reading or drafting work, per ADR-110 (contract-as-first-commit). Content arriving later in
the session is not load-bearing — a correction re-enters as a new contract, never as a
mid-flight message (`protocols/STANDING_RULINGS.md` D2).

- **Lane:** cloud — library-first research across the four hand-rolled scaling surfaces
- **Channel:** claude cloud (Anthropic cloud-session lane)
- **Branch:** `docs/library-first-research-2026-08-21`
- **Base:** `origin/main` @ `78267fd`
- **Mode:** execute — research + ONE artifact; docs-only. No adoption, no dependency added,
  no rulings, no row edits, no JOURNAL writes (a lane never journals), no index regeneration.
- **Output artifact:** `docs/audits/2026-08-21-technical-library-first-research.md`

**Receipt (per the brief's receipt-first instruction):** brief = 81 lines; final line verbatim —
`artifact.`

---

## Contract, verbatim

# CLOUD LANE — LIBRARY-FIRST RESEARCH: THE FOUR SCALING SURFACES

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — research + ONE artifact; docs-only | high |

Cloud lane (read-mostly, docs-only). FIRST COMMIT = dispatch-stamp (this prompt as
`docs/audits/2026-08-21-technical-library-first-research-lane-contract.md`). Fresh branch off
origin/main. No index regeneration, no JOURNAL, no row edits, no rulings.

WHY: four surfaces are hand-rolled and each grows with fleet size — `fleet_parity.py` (2,049
LOC), `deploy/` (7,460 LOC), the doc-edge scanners, and tech-currency. The operator's standing
constraint: **it must scale to N repos without our line count scaling with it.** Per the
library-first stance, each track ends in ADOPT / REJECT-WITH-MEASURED-DIVERGENCE / DEFER —
never "we already built it".

## METHOD (all tracks)
For each candidate: current release + maintenance signal (last release date, issue velocity),
licence, Windows + Linux support, install path under our pinned `uv`, what it replaces in OUR
tree by file:line and LOC, what it CANNOT do that our code does (the divergence), and a
30-minute-or-less trial where feasible on a THROWAWAY clone in TEMP (never our tree). Record
commands and raw output. No adoption, no wiring, no pyproject edits.

## TRACK 1 — doc→doc / file→doc edges and locator rot
Ours today: `scan_undeclared_edges.py` (WARN-only, 19 live WARNs), `reconciled_versions` +
`validate_reconciliation.py` `_SPEC_REGISTRY` (declared edges, FAIL leg), 6.9% measured locator
rot, `doc_rot` at 20 WARNs.
- **lychee** (Rust, static binary, `--offline`, anchor-fragment checking, JSON output, cache):
  trial on our `docs/` + root canon; report findings count vs our scanners' 19, overlap, and
  what each finds that the other misses. State whether it subsumes the locator-rot leg.
- **The graph question, answered on evidence, not on intake #16's word:** count our actual
  edges (declared + scanned). Then compare THREE options for the rot query: (a) stdlib
  `sqlite3` + recursive CTE over an edges table (zero new dependency — the default), (b)
  `networkx`, (c) `rustworkx`. Give the crossover: at what edge count / which query classes
  (cycles, impact-of-move, orphan detection, centrality) does a graph library beat a SQL join?
  Name the consumer each option would need per ADR-105.
- Also survey: any tool that maintains a doc-dependency graph natively (docs-as-code
  ecosystems) — report honestly if nothing fits.

## TRACK 2 — methodology deployment to consumer repos
Ours today: `deploy/tool.py` + four carriers, 7,460 LOC, PLAYBOOK §20 runbook, one proven run,
`deployed-versions.yaml`, hash-guarded floor (ADR-93).
- **copier** (git-tagged templates, `.copier-answers.yml` in the consumer, `copier update`
  three-way merge, `skip_if_exists`, conditional includes) — already the named-but-unbuilt
  library in intake #25.
- **cruft** (cookiecutter + `cruft check --exit-code` as a CI drift gate; scheduled-Action
  auto-PR pattern).
- Map OUR four carriers onto each tool: which carrier becomes template material, which stays
  bespoke (expect: the hash-guarded floor and the version record). Give the honest LOC estimate
  of what `deploy/` would shrink to, and the migration cost for the already-deployed consumers
  (ai-council @1.3.1, corp-monorepo @1.2.0).
- Include the **fleet-wide alternative**: hub-published **reusable GitHub Actions workflows**
  and **pre-commit remote hook repos** — consumers REFERENCE the hub by version instead of
  receiving copies. Compare "copy + update" vs "reference by version" as strategies, including
  what breaks offline and what breaks for private repos.

## TRACK 3 — fleet parity / conformance as data, not as Python
Ours today: `fleet_parity.py` 2,049 LOC + parity surfaces + `desired_state_report.py`
(conform 190 / diverge 3).
- Evaluate policy-as-code over our already-typed YAML: **conftest/OPA (Rego)**,
  **check-jsonschema**, **pydantic** (already in baseline), **deepdiff** for state-vs-declared.
- The property to measure: **cost of adding one new conformance rule** — today (Python function
  + test + registry entry) vs each candidate (a policy file). Show a worked example: express ONE
  real existing parity check in each candidate's syntax.
- Verdict must state the divergence honestly: which of our checks are NOT expressible
  declaratively (they justify the Python that remains).

## TRACK 4 — tech currency and dependency freshness
Ours today: `changelog_sentinel.py` (armed, fires), no distribution half, `[#385]`/`[#495]`.
- **Renovate** vs **Dependabot** for the fleet: which handles our pinned-`uv` + pre-commit rev
  exact-match discipline, and whether either can drive template/copier updates as PRs.
- One-paragraph honest read on whether this replaces or complements the sentinel.

## OUTPUT
ONE artifact `docs/audits/2026-08-21-technical-library-first-research.md`: per track, a
candidate table (candidate · what it replaces here · LOC it would remove · divergence · verdict
LEAN), then a single ORDERED recommendation list across all four tracks with the cheapest
highest-leverage first, each carrying the intake-or-row it would need. Commit, push, STOP
packet with the four LEANs in one line each.
NOT: no adoption, no dependency added, no rulings, no row edits, no changes outside the one
artifact.
