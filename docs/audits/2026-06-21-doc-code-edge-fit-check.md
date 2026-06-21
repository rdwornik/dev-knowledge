# doc→code declared edge — Phase 0 fit-check findings (#194)

> **CC fit-check (plan-mode; investigate + report, no schema built).** Settles the
> design crux for the **#194 Track B** doc→code declared edge **before** the Phase 2
> schema build. The ADR-89 OQ1 ruling (ratified 2026-06-21) named two load-bearing
> mechanisms — explicit `{#id}` heading anchors, and "the existing codemap" for code
> targets — and this pass tests whether they actually hold in-repo. **Two do not.**
> Design only — **zero integration**: nothing here is wired into a hook, gate,
> pre-commit, or `ALL_CHECKS`; no validator lands in `scripts/` this pass. The
> deliverable is the four findings + the recommended Phase 2 shape below.

**Date:** 2026-06-21
**Scope:** this repo's doc↔code edge surface — markdown governance docs, the markdown
anchor toolchain (`scripts/toc/`), the codemap (`scripts/codemap/`, `ARCHITECTURE.md`),
the code-resolution oracle (`scripts/reverse_dep_oracle.py`), and the coherence-spine
validators (`scripts/validate_reconciliation.py`, `scripts/coherence_enumerator.py`).
**Binding doctrine:** ADR-88 (file-oriented dependency management — coherence-by-mechanism,
graph-in-repo, narrow-first) · ADR-89 (computed code-dependency edges — declare-what-you-can't /
compute-what-you-can, `broken_edge` hard-FAIL vs `staleness_signal` advisory, advisory-first).
**Operator decisions folded in:** doc-side identity = **explicit rule-ID tokens** (not `{#id}`),
**and amend the ratified ADR-89 OQ1 marker** to record the correction; **C1 kept apart**.

---

## Verdict — **build-ready, with two OQ1 mechanism corrections**

The doc→code edge is buildable on mechanisms that already exist, but **not the two OQ1 named**.
The `{#id}` anchor does not resolve in any in-repo toolchain and is used by zero real headings;
the codemap resolves only 2 of 30 code modules. Both are replaced by sturdier existing
machinery — **explicit rule-ID tokens** doc-side and **path + AST resolution** code-side — which
also give the clean deterministic `broken_edge` hard-FAIL the ruling requires. The two-edge-type
schema (`broken_edge` / `staleness_signal`) composes with #196's removal closure as one more
direct-boundary union member, no transitive walk introduced.

---

## Finding 1 — Anchor mechanism: OQ1's `{#id}` assumption is unsupported in-repo

- The **only** anchor-resolving toolchain in the repo is `scripts/toc/generator.py` —
  `_slugify` (lines 22–32) + `parse_headers` (lines 40–57). It mirrors github-slugger:
  it slugifies heading **text** to `#lower-hyphen`.
- It does **not** honor `{#id}`. `_slugify`'s `re.sub(r"[^\w\- ]", "", …)` strips `{`, `#`, `}`,
  so `## Foo {#bar}` becomes the slug `foo-bar` (the `{#bar}` is treated as visible text), never
  `bar`. GitHub-flavored markdown — the exact slug behaviour this generator mirrors — likewise
  ignores `{#id}` and renders it literally.
- A grep for real `## … {#id}` headings across all `*.md` returns **zero** live uses. The single
  `{#id}`-in-a-heading hit is the **title of "Proposal C"** in the OQ1 council transcript
  (`docs/decisions/transcripts/council-out-20260621_003655-…-adr89-oq1-doc-code-granularity.md:335`)
  — the proposal *naming* the idea, not an anchor in use anywhere.
- **Conclusion.** Honoring `{#id}` literally would require building a new resolver the repo does
  not have (and that GitHub rendering would not honor either). **Use explicit rule-ID tokens**
  (`<!-- rule: PB-07 -->` placed on/near the governed heading) as the doc-side stable identity:
  it matches #194's own "declared rule-ID scheme" wording, is greppable, toolchain-independent,
  and survives heading renames — a durable file fact (ADR-88 principle 3, graph-in-repo). The toc
  slugger remains available only as a secondary "does this heading still exist" sanity probe, not
  as the identity.

## Finding 2 — Code-side identity: the codemap is the wrong oracle

- The codemap (`ARCHITECTURE.md` CODEMAP block; generator `scripts/codemap/ast_walker.py:22–27`)
  enumerates **only directories containing `__init__.py`** — i.e. Python *packages*. There are
  exactly **two**: `scripts.codemap` and `scripts.toc`.
- All **28 flat modules** — `audit.py`, every `validate_*.py`, `coherence_enumerator.py`,
  `coherence_nudge.py`, `reverse_dep_oracle.py`, `scan_undeclared_edges.py`, etc. — plus the two
  packages' submodules are **not codemap nodes**. These are precisely the modules a doc→code rule
  edge most wants to name (a rule in a protocol pointing at the check that enforces it). The
  codemap cannot resolve any of them.
- The deterministic resolver already exists, in two layers:
  - **File target** → repo-relative path + `Path.exists()`; the resolvable universe is
    `scripts/**/*.py`.
  - **Symbol target** → `reverse_dep_oracle.resolve_symbol(name, file)` (lines 146–152), backed by
    `iter_definitions` (lines 105–134) — an AST walk of every `FunctionDef`/`AsyncFunctionDef`/
    `ClassDef` under `scripts/`. It returns **exactly-one** (resolved), **zero** (`symbol-not-found`),
    or **>1** (`ambiguous`, re-run with `--file`).
- Both layers give a clean, deterministic **`broken_edge` hard-FAIL** on an unresolvable target —
  exactly what OQ1 requires, just not from the codemap.
- **Conclusion.** Code-side target = **repo-relative file path, optionally `::symbol`**; resolve
  via filesystem existence + `resolve_symbol`, **not** the codemap. OQ1's phrase "via the existing
  codemap" is corrected to "via path + AST resolution (`reverse_dep_oracle.resolve_symbol`)."

## Finding 3 — Declaration location + footprint

- Existing precedents are split: per-file **frontmatter** (`reconciled_with: spec@ver`, with the
  `validate_reconciliation._SPEC_REGISTRY` single-source) vs. in-code **manifest**
  (`audit.py::_COUPLED_VERSION_SETS`, `validate_doc_rot.py::_FILE_SIZE_BUDGETS`).
- #194's task already prescribes the shape: edge declared at **both natural ends** + a **derived,
  rebuildable index** (no hand-maintained central manifest → nothing to drift; ADR-88 principles
  3 and 4):
  - **Doc side:** rule-ID token on/near the governed heading — `<!-- rule: ID -->`.
  - **Code side:** a structured comment annotation on the implementing check — e.g. `# rule: ID`.
  - **Index:** a read-only validator rebuilds the rule-ID ↔ check map on every run.
- **Files a Phase 2 build would touch** (decides #194's contention surface):
  - **NEW:** `scripts/validate_doc_code_edge.py` (read-only Layer-2 validator),
    `tests/test_doc_code_edge.py`, and a fixture dir (`tests/fixtures/doc-code-edge/…`) carrying
    intentional dangling / duplicate / missing rule-IDs.
  - **EDIT:** `scripts/audit.py` `ALL_CHECKS` (add the next check) — **`serialize-group: audit-py`**,
    contends with other audit.py work; `ARCHITECTURE.md` (validator-list bullet + collected/check
    counts — the codemap block is **unchanged**, no new package); `BACKLOG.md` (#194 close);
    `JOURNAL.md` (wrap).
  - **Advisory-first** (OQ1): **no** pre-commit gate this build → `.pre-commit-config.yaml` and
    `CLAUDE.md` §9 hook roster are **not** touched yet (instrument before any blocking promotion).
  - **No real annotations** on PLAYBOOK or live checks this build — the #194 done-when is a
    **fixture** proof ("flag a fixture's dangling/duplicate rule-IDs, tested"). So Phase 2 does
    **not** contend with PLAYBOOK.md (or any protocol doc) content edits. #194 already carries
    `serialize-group: code-edge`.

## Finding 4 — Closure composition with #196 / #195-2b: composes cleanly

- #195 Phase 2b's removal gate unions per-kind reverse-dependency units across 3 mechanisms — M1
  computed code→code (`reverse_dep_oracle`), M2 computed path/dotted-module refs, M3 declared prose
  (`reconciled_with`) — as a **direct cross-kind boundary, NOT a transitive-outward walk**
  (`docs/audits/2026-06-20-removal-closure-spike-findings.md`).
- The doc→code edge contributes **one more per-kind unit**: "which doc rule-IDs name this file /
  symbol being removed?" — answered by the same rebuildable index, queried for *direct* referrers
  of the removal target only.
- `broken_edge` / `staleness_signal` are the **edge-health** layer (L1, #194's DETECT-first scope):
  does the edge resolve, and has its target changed since review. The removal union (#195/#196) is
  a **separate consumer** that reads the edge's *resolved targets*. No transitive walk is
  introduced — the edge is never followed onward from the doc.
- **Conclusion.** The two-edge-type schema composes as a direct-boundary union member. The two
  layers are orthogonal and stack cleanly: edge-integrity (this build) under removal-closure
  (Track D, later).

---

## Recommended Phase 2 shape

- **Edge identity:** doc-side `<!-- rule: ID -->` token; code-side `# rule: ID` annotation. Code
  target resolves via `Path.exists()` (file) + `reverse_dep_oracle.resolve_symbol` (symbol).
- **Two validation classes** (ADR-89): `broken_edge` = unresolved doc rule-ID **or** unresolved
  code target → deterministic **hard-FAIL**; `staleness_signal` = referenced target changed since
  review → **advisory**.
- **Index:** derived / rebuildable on every run — no hand-maintained manifest.
- **Structural-integrity checks** (#194 L1, DETECT-first): dangling rule-ID (doc names a code
  target that doesn't resolve), duplicate rule-IDs, code annotation → nonexistent rule, missing IDs.
- **Rollout:** advisory-first — validator + one `audit.py` check, **no pre-commit gate yet**;
  instrument, then promote per the #181-style data-gated decision.
- **Done-when (from #194):** the scheme + structural check flag a fixture's dangling / duplicate
  rule-IDs, tested.

## Phase 1 (C1) — independent, kept apart

- The hardcode is `scripts/validate_doc_rot.py:57` → `_FILE_SIZE_BUDGETS = {"CLAUDE.md": 200}`.
- The de-hardcode reads CLAUDE.md's self-declared "≤200 lines" (prose, CLAUDE.md line 11) instead
  of the literal `200`. Separate branch/commit, ~10-minute change, no serialize-group contention
  with the code-edge work. **Not bundled.** It is itself a tiny doc→code de-hardcode (a check
  reading a doc's self-declared value), so it can cite ADR-89's "declare only what code cannot read
  directly," but it ships on its own arc.
