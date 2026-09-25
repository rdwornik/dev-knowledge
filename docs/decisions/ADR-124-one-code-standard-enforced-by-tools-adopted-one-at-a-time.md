# ADR-124: One code standard, enforced by existing tools adopted one at a time; every ADR carries its quality attributes

- **Status:** Proposed
- **Date:** 2026-09-25
- **Decision tier:** Architecture (Path A — the architect's technical proposal under ADR-108 §A, drafted by
  `lane-adr-drafts` on `LANE-5B2-11-adr-drafts.md`, batch WAVE5B-N2 row 11). **Stays Proposed until the operator
  ratifies.** The functional questions are in §Operator decision options, not decided here.
- **Amends:** none. **Extends** ADR-108 §B ("clean architecture — layer model as specification, mechanized check")
  and §B-4 (functional-first, dataclasses, PEP 8 — "arms no gate") by naming the tools that arm them. **Would
  amend** `templates/ADR-template.md` and `scripts/validate_adr_status.py` (D5) — in a build lane, not here.
- **Related:** ADR-28 (the layer model a boundary tool would enforce), ADR-89 (the vendored Pyright pin),
  ADR-106 (uv pinned exactly; a uv bump is its own change), ADR-123 (the artefact that would carry the shared
  configuration), ADR-120 (spine stage 6, library-first).
- **Provenance:** `PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25` §5 ADR-B and §3.4 ("the enforcement is free and
  library-first … research names the exact set and measures today's repositories against it"). **Intake:** none —
  born from a batch order.
- **Decommission:** none. `templates/ruff-config-block.toml`'s REPO-PERSONAL `select` examples become UNIVERSAL
  keys when D3 lands; nothing is deleted.
- **Source (in-repo):** `pyproject.toml:25` (uv `==0.11.19`), `:31` (ruff `==0.15.5` dev pin), `:99-113` and
  `[tool.deptry]` (deptry adopted), `:349-358` (`[tool.ruff]` universal keys; `extend-select = []`);
  `.pre-commit-config.yaml:19-30` (the 2026-09-17 strip: 34 hooks, ~244 s mean commit wall, "a hook returns to the
  local stage only with a counter") and `:842-852` (the managed ruff hook, `stages: [manual]`);
  `templates/ruff-config-block.toml` (the fleet block, gated by `fleet_parity`); `package.json` (`pyright 1.1.410`,
  vendored for `scripts/reverse_dep_oracle.py`, ADR-89); `templates/ADR-template.md` (Alternatives considered and
  Flip-condition already REQUIRED, citing thesis T-04); `scripts/validate_adr_status.py:198`
  (`FLIP_GRANDFATHER_MAX_ADR = 116`) and `:560` (`REQUIRED_SECTIONS`);
  `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md` §3 (T-01…T-12).
  **Source (transport, in addition):** `to-browser/SESSION-lane-research-python-standard.md` (C3: the toolchain,
  versions read 2026-09-25, the gap against today); `to-browser/DIGEST-THESIS-ARCH-PROCESS-2026-09-25.md` (L4:
  the thesis's quality-attribute process and the proposed ADR-template delta).

## Context

1. **The hub enforces almost nothing about code shape.** Measured by C3 at `da11291b`: ruff pinned at 0.15.5 with
   `extend-select = []` (only ruff's defaults E4/E7/E9/F); no type checker; no import-boundary tool; no complexity
   limit; no CVE scan; no dead-code tool beyond F401/F841; `hypothesis` absent from `uv.lock` (the two `git grep`
   hits in `tests/` are false positives). deptry 0.25.1 is adopted but runs at `stages: [manual]`.
2. **The standard already exists as prose.** ADR-108 §B asks for a layer model with a "mechanized check"; §B-4 rules
   functional-first with dataclasses and PEP 8, and says of itself that it "arms no gate".
3. **The last attempt at many gates was reverted.** On 2026-09-17 the commit gate (34 hooks, ~244 s mean wall) was
   stripped because no hook carried a counter of what it caught (`.pre-commit-config.yaml:19-30`). A hook returns
   only with a counter; the live pattern is `telemetry_emit.py wrap` with an expiry — "0 catches in-window →
   REMOVE, never tune".
4. **Sharing one configuration across repositories has a known shape here.** Ruff has no implicit config merge and
   no `extend` by URL (C3: astral-sh/ruff#12352, open); pre-commit has no inheritance. The hub already chose a
   template block plus a parity gate (`templates/ruff-config-block.toml`, `fleet_parity`), for three keys only.
5. **The thesis's architecture process is not in the ADR template.** L4: the thesis selects quality attributes from
   a closed set of ten (ch.6 :6-7), writes a six-part scenario with a response measure per attribute
   (`tex/5-projektowanie-architektury-krok-po-kroku.tex:200-249`), fills a tactic questionnaire, and decides per
   attribute. The hub template already absorbed two thesis items (Alternatives considered and Flip-condition,
   T-04/T-07); the quality-attribute fields are the remaining delta.

## Decision

- **D1 — The toolchain (C3's measured set, exact).**

  | Tool | Version (C3, read 2026-09-25) | Configuration | Enforces |
  |---|---|---|---|
  | ruff | pinned **0.15.5** (latest 0.16.9; the bump is its own gated change) | `extend-select = ["B","SIM","C90","PL","RET","PERF","FURB","PTH","N","UP","ARG","ERA","TRY","FBT","RUF"]`; `[tool.ruff.lint.mccabe] max-complexity = 10` | bugs, simplification, complexity, perf, pathlib, naming, dead params, commented code, exception shape, boolean traps, mutable defaults (RUF008/RUF012/RUF009) |
  | tach | **0.35.1** | `tach.toml` seeded by `tach sync` from today's import graph; tags = the ADR-28 layers | import boundaries / layer contract |
  | pyright (CI) | reuse the **1.1.410** pin already in `package.json` (ADR-89) — one pin, not two | `[tool.pyright] typeCheckingMode = "standard"` | static types |
  | ty (editor only, not a gate) | **0.0.84** (beta; no plugin system) | editor LSP | fast type feedback |
  | deptry | **0.25.1** (adopted) | unchanged | declared vs used dependencies |
  | pip-audit | current (C3 did not pin a number) | `pip-audit` over `uv export`; `uv audit` deferred until confirmed on uv 0.11.19 | known CVEs |
  | vulture | **2.16** | `vulture scripts/ --min-confidence 80` | unreachable code |
  | hypothesis | not confirmed by C3 (fetch failed) | opt-in per module, `@given` on pure functions | properties of pure functions |

- **D2 — One tool per lane, each with a counter and an expiry.** Adoption order: (1) ruff `extend-select` + C90
  (no new dependency; auto-fixes that keep tests green, violations counted before/after — batch WAVE5B-N2 lane 14
  `lane-python-standard-1` measures the hub baseline); (2) tach; (3) pyright in CI; (4) pip-audit; (5) vulture;
  hypothesis opt-in. Each lands through `telemetry_emit.py wrap` with an expiry; 0 catches in its window removes
  it. No tool enters the local commit stage without that counter (the 2026-09-17 rule).
- **D3 — One shared configuration.** Until ADR-123's artefact exists: the rule families, `max-complexity` and the
  tool configs move from REPO-PERSONAL to UNIVERSAL in `templates/ruff-config-block.toml`, gated by
  `fleet_parity`, divergence declared in `.methodology.yaml`. After ADR-123: the artefact carries the configuration
  as package data, materialised into the consumer and pointed at by ruff's path `extend`, drift-gated by
  `harness check`.
- **D4 — Existing code: a ratchet.** A new violation is refused; the counted baseline may only shrink. No
  conversion pass is scheduled (ADR-108 §B-4 stays prospective). The functional choice between ratchet and
  prospective-only is option 2 below.
- **D5 — Every ADR carries its quality attributes, checked.** A new REQUIRED section `## Quality attributes`, same
  enforcement shape as `## Flip-condition` (FAIL above a new grandfather mark = 126, WARN at or below):
  - **Quality attribute(s)** — one or more of the thesis's closed set of ten: Availability, Deployability,
    Integrability, Modifiability, Performance, Security, Safety, Testability, Usability, Energy efficiency.
  - **Scenario (six parts)** — Source, Stimulus, Environment, Artifact, Response, **Response measure** (required,
    non-empty, a number or an observable).
  - **Decision evidence** — a table or log (matrix, questionnaire, measurement), not restated prose.

  ADR-123, ADR-125, ADR-126 and this ADR carry the section already, as its first four instances.

## Quality attributes

- **Quality attribute(s):** Modifiability (primary), Testability.
- **Scenario (six parts):**
  - *Source:* a lane writing Python in any governed repository.
  - *Stimulus:* it commits a function with McCabe complexity 14 and a mutable default argument.
  - *Environment:* the repository at a pinned configuration, the tool's lane landed, commit or CI time.
  - *Artifact:* the gate set of D1-D2.
  - *Response:* the change is refused, naming the rule (`C901`, `B006`); the counter records a catch.
  - *Response measure:* refused in **100 %** of seeded cases (a RED-first witness per tool); each tool's added
    wall time recorded; a tool with **0** catches over its window is removed.
- **Decision evidence:** C3's gap table (Context 1) and the matrix below.

## Decision matrix

**Scoring rule.** Each option is scored 1-5 per criterion (5 best); total = Σ(weight × score), maximum 500.

Criteria (weights sum to 100): **Q1** enforceable coverage of "clean, functional-style" — share of C3's
tool-enforceable list that is gated (25) · **Q2** library-first — established tools, nothing hand-rolled (15) ·
**Q3** commit-wall cost and friction, 5 = no added wall (20) · **Q4** measured, counted adoption (15) · **Q5** one
shared configuration with a parity gate (15) · **Q6** effort and risk to existing code (10).

| Option | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Total |
|---|---|---|---|---|---|---|---|
| S0 status quo (ruff defaults, deptry manual) | 1 | 5 | 5 | 2 | 4 | 5 | 340 |
| S1 C3's whole toolchain in one lane | 5 | 5 | 1 | 1 | 3 | 1 | 290 |
| **S2 C3's toolchain, one tool per lane, counter + expiry (D1-D4)** | 5 | 5 | 4 | 5 | 4 | 3 | **445** |
| S3 ruff only, maximal rule set, no other tools | 3 | 5 | 4 | 3 | 4 | 2 | 355 |
| S4 as S2 with mypy strict + import-linter | 5 | 5 | 3 | 5 | 4 | 2 | 415 |
| S5 a course or book first, tools later | 1 | 2 | 5 | 1 | 1 | 5 | 235 |

**Reading.** S2 leads S4 by 30 (mypy's slower runs and strict mode on untyped code; hand-written contracts versus
`tach sync`) and S3 by 90 (no types, no boundaries, no CVE scan). **Sensitivity:** S2 − S0 = 4·w_Q1 + 3·w_Q4 − w_Q3 −
2·w_Q6 = 105; S0 overtakes only if w_Q3 + 2·w_Q6 exceeds 4·w_Q1 + 3·w_Q4 — commit cost and effort would have to weigh
more than coverage and counting together, several times over.

## Flip-condition

- **Remove a tool** when its counter shows 0 catches over its window (the standing expiry rule) — the decision is
  per tool, not all-or-nothing.
- **Replace pyright by ty** when ty leaves `0.0.x` and passes the typing conformance suite at least as well as
  pyright (C3: pyright ~98 %).
- **Replace tach by import-linter** if `tach sync` cannot express the ADR-28 layers without more than a handful of
  hand-written exceptions, or tach stops being maintained.
- **Stop at ruff (S3)** if the first two tools' combined added commit wall exceeds the operator's budget for it — the
  measure is the counter, recorded per tool.
- **D5 flips to WARN-only** if more than one in three new ADRs needs a waiver for the section within 60 days — the
  fields then do not fit the decisions this repository takes.

## Alternatives considered

- **S0 status quo** — breaks nothing and costs nothing; enforces none of §B-4, so the standard stays prose.
- **S1 everything at once** — the full toolchain in one lane repeats the shape reverted on 2026-09-17: many gates,
  no counters, a wall nobody can attribute.
- **S3 ruff only** — the cheapest high-signal step and D2's step 1; alone it leaves types, boundaries and CVEs unchecked.
- **S4 mypy strict + import-linter** — mature and deeper in plugins, but slower, and hand-written contracts where
  `tach sync` derives a passing baseline from the graph the repository already has.
- **S5 a course or book first** — the plan's pushback §3.4; C3 names Ousterhout's *A Philosophy of Software Design*
  for the judgment no tool computes (purity, whether a boundary is the right one), as a later option, not a start.
- **Shared config by ruff `extend = <URL>`** — not supported (astral-sh/ruff#12352 open); by copier — the drift class
  ADR-123 rejects. Kept: the template block + parity gate now, the artefact later.
- **radon/xenon (0.9.3)** — ruff `C90` already computes the McCabe number; a second dependency adds maintainability
  indices nobody has asked for.

## Consequences

- The §B-4 stance becomes checkable where a tool can check it; what no tool computes — whether a function is pure,
  whether a boundary is the right one — stays review work, named as such (C3 "What no tool can enforce").
- Five tool lanes, each small; the hub's first measured baseline arrives from lane 14 of this batch.
- A second pin to keep current per tool; pyright reuses the one already vendored.
- D5 adds one section to every ADR and one rule to `validate_adr_status.py`; the four ADRs of this batch show its cost.

## Operator decision options

These are functional (ADR-108 §A); the technical choice above stands as proposed unless he rules otherwise.

1. **Ratify the standard** — Accept S2 (one tool per lane, counted) · Accept ruff only for now (S3) · Return.
2. **Existing code** — ratchet (new violations refused, the baseline only shrinks — proposed) · prospective only
   (new files only, as ADR-108 §B-4 reads today) · a scheduled conversion pass.
3. **Scope** — every repository including the five employer-heavy private ones · the hub and the three named consumers
   first · the hub only until ADR-123's artefact exists.
4. **ADR quality-attribute section (D5)** — required and checked for every new ADR · recommended, not checked.
5. **A book or course** — not now (proposed; tools first) · buy Ousterhout now (his purchase, an
   `OPERATOR-ACTION`).
