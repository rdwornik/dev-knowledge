# Removal-closure computation — design spike findings (#196)

> **CC design spike (plan-mode; investigate + propose, no engine built).** Answers
> **the dependency-legibility brief's OQ1** — *how to compute a removal closure across
> heterogeneous artifact kinds* — the hardest unsolved piece blocking the safe-removal
> gate `#195-2b` (Track D-2b). This is **not** ADR-89 OQ1 (doc→code rule-ID granularity)
> and **not** ADR-89 OQ2 (oracle provenance, already RESOLVED by #193). Design only —
> **zero integration**: nothing here is wired into a hook, gate, pre-commit, or
> `ALL_CHECKS`; no engine lands in `scripts/`. The deliverable is the feasibility verdict
> below, sufficient to decide D-2b's build approach **or** to write the ADR-89 OQ3 ruling.

**Date:** 2026-06-20
**Scope:** this repo's artifact surface — Python `scripts/`, `tests/`, config (`.pre-commit-config.yaml`, `.claude/settings.json`, `pyproject.toml`/`tach.toml`), markdown governance docs, PowerShell hooks.
**Builds on (do not replace):** `scripts/reverse_dep_oracle.py` (#193, computed code→code) · `scripts/scan_undeclared_edges.py` (#179, declared prose-refs) · `scripts/propose_closures.py` (the slash-precision/`_CHURN_FILES` path-matching precedent).
**Binding doctrine:** ADR-89 (compute-what-you-can / declare-what-you-can't; static-Python + repo-scoped limits; provenance-on-every-answer; **OQ3 advisory→gate still open, data-gated**).

---

## Verdict — **GO for D-2b, scoped to a direct cross-kind reverse-dependency *boundary***

The removal closure **is computable to the degree a removal *gate* needs it.** Two
mechanisms — the computed code→code oracle (M1) and a computed path/module reverse-ref
resolver with slash-precision (M2) — form a **hard-gate-eligible direct cross-kind
reverse-dependency boundary**, under the fail-closed completeness/dirty preconditions in §5.
Everything dynamic / cross-language-by-meaning / string-keyed / sub-file / re-export-membership
/ star-import stays **advisory + human-signed** (the declared leg, M3) — which is exactly the
surface ADR-89's doctrine already assigns to humans. **The residual is not a gap in the
design; it is the declared leg working as intended.**

The one framing correction this spike makes: a removal gate needs a **boundary check, not a
transitive-outward graph walk** (§1). "Full transitive closure" over-reports for a pure
deletion. See **§7 Worst-case targets** and **§8 What stays declared** for where the verdict
stops.

---

## 1. What a "removal closure" *is* — a boundary, not a transitive graph

A removal closure is the set the gate must inspect to answer **"is it safe to delete X?"**
A removal is safe **iff nothing external to the removal set references the removal set.**

For a **pure deletion**, the breaking sites — the ones that will not compile/import because
they now name a missing artifact (a dangling reference) — are the **direct reverse-dependents**
of the removed set. Transitivity-outward does **not** add breakage: if `A` references `X` and
`B` references `A`, deleting `X` breaks `A` (it now references an undefined name) but does **not**
break `B` — `A`-the-symbol still exists. `B` would only break if `A`'s *behavior* changed, which
is a semantic/coherence judgment, not a deletion-breakage fact (and is the human's leg, §8).

So the gate-relevant object is a **direct cross-kind reverse-dependency *boundary*** — the union
of the direct reverse-dependents of every artifact in the removal set, minus the removal set
itself — **not** a transitive-outward reachability walk.

This **refines** BACKLOG #196's filed phrasing "traverse uniformly across artifact kinds": the
closure is *not* a uniform transitive traversal. The dependency **unit differs by kind** —
*symbol* for code, *file* for config/prose (ADR-89's "the unit of dependency differs by edge
type", `ADR-89:53-56`) — so the correct computation is a **heterogeneous direct-boundary union**,
each kind carrying its own compute-vs-declare posture. *(This divergence is surfaced for the
operator to reconcile on the #196 entry; this doc does not edit BACKLOG.)*

## 2. Five artifact kinds collapse into three mechanisms

| # | Mechanism | Covers (artifact kinds) | Posture | Built on |
|---|---|---|---|---|
| **M1** | Computed code→code reverse-deps | code symbols; **static** test→symbol (a test that `import audit` is just an oracle referencer) | **Computed / exact** | `reverse_dep_oracle.run_oracle()` (#193), one query per removed symbol; whole-file removal seeds *all* its symbols via `iter_definitions()` |
| **M2** | Computed path / dotted-module reverse-refs | config string-refs (`.pre-commit-config.yaml`, `.claude/settings.json`), cross-language hook-wiring (PS1/YAML/JSON), importlib-by-path, prose file-path mentions | **Computed / exact — with the precision rules in §4** | a thin new resolver generalizing `scan_undeclared_edges` Tier-1 (verbatim path), inheriting `propose_closures._PATH_RE` slash-precision |
| **M3** | Declared prose edges | prose coherence (markdown→spec/doc), `reconciled_with` registry edges | **Declared / human-confirmed (never auto-declare)** | `scan_undeclared_edges.scan()` + `validate_reconciliation._SPEC_REGISTRY` |

**There is no M4.** Inward dead-set expansion — finding orphans that become dead because they
were *only* used by the removal set, so they can be co-removed — needs *forward* dependency
resolution (`references()` is reverse-only, `reverse_dep_oracle.py:22`). This is **out of scope
for the gate**: the gate *refuses unsafe removals*; it does not *propose* co-removals. (If
inward expansion is ever wanted it is a separate forward-resolution build — `documentSymbol` /
`outgoingCalls` — not part of the safe-removal boundary.)

The five kinds named in the brief map cleanly: **code symbols** → M1; **tests→symbols** → a
*subset* of M1 (static imports computed; importlib-by-path falls to M2); **config/string-refs**
→ M2; **prose declared-edges** → M3; **cross-language** → M2 (path mentions across language
boundaries) for the *wiring*, M3/human for cross-language *meaning*.

## 3. The computed/declared split — the honest division of labor

This is just ADR-89's compute-what-you-can / declare-what-you-can't (`ADR-89:39-56`) and its
enforcement-leg-scaling (`ADR-89:75-91`) applied to removal.

**Computed + exact (hard-gate-eligible, under the §5 preconditions):**

- **M1 — direct code→code reverse-deps.** Pyright resolves references *semantically*, not
  textually (the benchmark's decisive signal: `main`, defined in 34 files, resolved to exactly
  **2** references, `2026-06-20-pyright-reverse-dep-oracle-findings.md`). `super()`/MRO
  resolution, decorator-application sites, and this repo's universal `try/except ImportError`
  dual-import idiom all surface correctly as references.
- **M2 — path / dotted-module refs with slash precision** (see §4 for why the precision rules
  are load-bearing).

**Declared + human-confirmed (advisory trigger + human signature — the weak-deterministic leg):**

- **Prose coherence (M3)** — never auto-declared; the human confirms every candidate. This is
  the load-bearing safety rule of the scan and is not weakened here.
- **Re-export / `__all__`-membership / `from x import *` deletions** — **these are NOT
  computed.** String-membership and star-imports are not symbol references, so a *symbol-seeded*
  oracle does not surface them. Concrete case in this repo: `scripts/codemap/__init__.py` does
  `from .generator import generate_codemap` then lists it in `__all__` (a list of string
  literals). Deleting the re-export *line* (shrinking the package surface) breaks
  `from scripts.codemap import generate_codemap` consumers, but that breakage is invisible to a
  symbol-seeded `references()` query. → declared leg.
- **Dynamic dispatch / `getattr`·`setattr` / string-keyed registries** — ADR-89's named
  permanent blind spot (`ADR-89:104-111`); the oracle is blind by construction.
- **Semantic / behavioral transitivity** — "removing `X` changes `A`'s output and `B` depends
  on that output." Uncomputable; this is the AI-verdict + human-signature leg.

## 4. M2 precision rules — the repo already paid for this lesson; inherit it

A naive "grep the repo for the removed file's name" floods, and the repo has already engineered
around exactly this:

- **Require the directory-component (slash) form.** Mirror `propose_closures._PATH_RE` (its
  comment names the rule: *requiring the slash is the precision lever*). **Basename-only matches
  (`cli.py`, or a bare `main`) are weak-tier/advisory, never gating** — the same flood ADR-89
  cites when it rejects textual grep, and the same reason `propose_closures._CHURN_FILES`
  excludes `BACKLOG.md`/`JOURNAL.md`/`LESSONS.md` from path-matching outright.
- **Normalize dotted-module → path.** `.pre-commit-config.yaml` invokes hooks as
  `python -m scripts.codemap.cli` and `python -m scripts.toc.cli` — **real, gating dependencies
  with no slash-path and no `.py` basename.** Without a `scripts.codemap.cli → scripts/codemap/cli.py`
  normalizer, M2 silently misses the *most* safety-critical config edges (deleting that file
  breaks pre-commit). This normalizer is mandatory, not optional.
- **Config-value vs markdown-fenced split.** `scan_undeclared_edges` deliberately *skips* fenced
  code blocks (a fenced `python scripts/x.py` in a markdown *example* is not a content
  dependency — `scan_undeclared_edges` reuses `coherence_enumerator._find_fenced_blocks` for
  this). But a YAML/JSON `entry:` *value* **is always a real dependency.** So M2 must treat
  config files as always-real and apply fenced-block skipping **only** on the markdown side.

## 5. Fail-closed soundness posture — `partial` is a lower bound, not "fewer deps"

The oracle can return `completeness: partial` when its readiness deadline is hit before two
stable reference counts (`reverse_dep_oracle.py:382`, `ADR-89:194-198`). A partial answer is a
**lower bound** on the reference set — *fewer* references than reality. A gate that says "safe to
remove" from a partial boundary is therefore **unsound**: it under-reports breakage and
greenlights an unsafe removal. The only sound posture:

- `completeness: complete` **and** `dirty=false` for the removed path and its referencers →
  the gate **may** issue a hard verdict.
- `completeness: partial` → **fail-closed** (abstain / route to human; never "safe").
- `status: oracle-unavailable` (`reverse_dep_oracle.py:441,473-478`) → **fail-closed**.
- `dirty=true` touching the removed path or its referencers → **fail-closed.** The
  working-tree caveat (`reverse_dep_oracle.py:78-82`) means the answer reflects *uncommitted*
  state — and a **rename/move is not a pure deletion**: against a dirty tree the oracle may
  already reflect the post-move world, so "who breaks" is computed against the wrong state.

## 6. The unified closure report — shape, not code

One answer envelope, modeled on `reverse-dep-oracle/v1`'s provenance discipline:

- `removed` — the seed set (symbols and/or files).
- `dependents[]` — each `{ path, line?, unit: symbol|file, edge_kind: code|test|config|prose|crosslang, source: computed|declared-candidate, tier? }`.
- `boundary_external[]` — computed dependents that lie *outside* the removal set (the gate's
  hard input).
- `declared_candidates[]` — M3 candidates + the §8 blind-spot candidates, each requiring human
  confirmation.
- `provenance` — the oracle block verbatim (`git_rev`, `dirty`, `dirty_files`, `completeness`)
  **plus per-kind coverage caveats** (M1 static-Python-only; M2 slash-precision /
  basename-advisory / dotted-module-normalized; M3 human-confirm).
- `verdict_input` — `{ computed_boundary_empty: bool, completeness_ok: bool, declared_candidates_present: bool }`.

**Gate logic D-2b consumes** this: refuse the removal if `boundary_external` is non-empty
**or** any §5 precondition fails; require a human sign-off when `declared_candidates` are present.

## 7. Worst-case removal targets — handled by *abstaining*, named honestly

- **A `_SPEC_REGISTRY` row** (a string-keyed dict entry, `validate_reconciliation.py:64-69`).
  M1 is blind (the key is a string, not a symbol reference). M2 is irrelevant (the *file* still
  exists; only a *key* was removed). And M3 **excludes already-declared edges by design** — the
  GAP-ONLY rule in `scan_undeclared_edges._declared_spec_ids` (`:134-148`) skips docs that
  already carry a `reconciled_with` for the spec, which is precisely the live dependent (e.g.
  `docs/handoffs/README.md`'s `reconciled_with: handoff-process@…`). So this removal target is
  invisible to all three mechanisms and **hard-falls to the human/declared leg.** This is the
  dynamic-dispatch blind spot fully realized; the gate must abstain and route to a human.
- **Sub-file structured removals** — a markdown *section*, a YAML *key*, a `tach.toml`/`pyproject`
  *entry* (the codemap hook watches `pyproject.toml`/`tach.toml`). Neither a Python symbol nor a
  whole file, so neither M1 (cannot seed) nor M2 (file persists) fires. → gate **abstains**
  (`not-computed`) → human leg.
- **Rename/move** staged in a dirty tree → the §5 dirty fail-closed posture.

## 8. What this means for ADR-89 OQ3 (advisory→gate) — *eligible*, not asserted

This spike does **not** resolve ADR-89 OQ3 by fiat. OQ3's advisory→gate promotion is
**data-gated on observed drift value** (`ADR-89:202-204`, the ADR-88 #181 pattern). The
defensible claim is narrower and is the one D-2b should build on:

> The **computed legs (M1 + M2-with-slash-precision) are *eligible*** to gate hard once data
> justifies promotion, **under the §5 fail-closed preconditions**. The **declared legs (M3 +
> the §8 blind spots) remain advisory + human-signed.**

So D-2b's recommended build path: ship the computed boundary-check **advisory first** (it
*reports* the boundary and the would-be verdict without blocking), accumulate firing data, and
promote to a hard gate per the OQ3 data-gate — never a hard gate by default (`ADR-89:160-161`).
This keeps the removal gate consistent with how the rest of the organ earns enforcement.

## 9. Reconciliation with BACKLOG #196 (filed framing)

- *"map tests→symbols"* → tests→symbols is a **subset of M1** (static imports computed;
  importlib-by-path falls to M2 string-ref). No separate mechanism needed.
- *"resolve config string-refs"* → **M2**, with the §4 slash-precision + dotted-module
  normalization rules.
- *"traverse uniformly across artifact kinds"* → **refined** to a **heterogeneous
  direct-boundary union** with per-kind units and per-kind compute/declare posture (§1) — *not*
  a uniform transitive traversal. **This is the one divergence from the filed framing; it is
  surfaced for the operator to reconcile on the #196 entry.**
- *"Done when: a design doc specifies how closure is computed across artifact kinds with a
  feasibility verdict"* → satisfied by this document (§§1–8 + the Verdict).

## Scope & honest limits (where this verdict stops)

- **Repo-scoped.** Like the oracle it builds on, every claim here is for *this* repo's artifact
  surface. A child repo (e.g. `corp-monorepo`) needs fresh measurement — the static-Python
  blind-spot ratio, the M2 false-positive rate, and the dotted-module surface all differ.
- **Static-Python permanent blind spot inherited from M1.** §3/§7/§8 name what M1 cannot see;
  the design does not pretend otherwise — those edges are the declared leg's job.
- **Design only.** No engine is built, nothing is wired. The build (the M2 resolver, the unified
  report assembler, the advisory check) is D-2b's scope, undertaken after this verdict is acted
  on.
