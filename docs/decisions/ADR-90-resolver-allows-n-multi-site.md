# ADR-90: Doc→code resolver allows N declared code sites per rule (resolver-allows-N)

<!-- scope: meta -->

**Status:** Accepted
**Date:** 2026-06-26
**Decision tier:** Mechanism (a reversible resolver-logic change under the ADR-87 equilibrium — a status-logic refinement to the `doc_code_edge` check, NOT a doctrine question; recorded as a Path-A direct ADR, no Council debate).
**Deliberation basis:** the decision was already taken and recorded before this ADR — PLAYBOOK §"Lifeline 2 — Coherence" code↔doc row (`#201 (resolver-allows-N, decided)`) + BACKLOG #201 "Done when" (which names *"resolver allows N code sites for one rule"* as one of the two accepted scheme options). This ADR is the **record** of that decision, not a fresh deliberation; it repoints PLAYBOOK §245 to cite this file (the 1a pointer discipline — rationale lives here, PLAYBOOK points).
**Related:** ADR-89 OQ1 (the doc→code rule-ID naming convention + the registry-scoped `declaration_docs`/`coverage_scope` mechanism this extends — the deferred-tail "two-organ #201" is exactly this edge); ADR-88 (file-oriented dependency management — the *declared-edge* paradigm; the per-rule expected count is a **declaration**, consistent with "declare what you cannot compute"); ADR-87 (the architect↔CC equilibrium under which this mechanism change is a CC-buildable, architect-pointed task).
**Decommission:** none.
**Source:** PLAYBOOK §245 + BACKLOG #201 (the decided scheme); `ecosystem/doc-code-edge.yaml` (the DEFERRED two-organ block this resolves).

## Context

The doc→code edge (ADR-89 OQ1) resolves a governance rule by matching its doc-side
`<!-- rule: ID -->` declaration to its code-side `# rule: ID` annotation. The Phase-A resolver
(`scripts/validate_doc_code_edge.py::resolve_edge`) is strictly **1:1**: a rule with more than one
code site is classified `ambiguous`, never `resolved`. That duplicate-guard is correct for the
common case — a second `# rule: ID` is almost always an accidental duplicated-ID bug — but it has
a structural gap.

**Some rules are legitimately enforced in more than one code organ.** The `code↔doc` edge is meant
to map *a governance rule* to *all the code that enforces it*, and several rules genuinely enforce
in two or three places (a detect organ + a prevent organ, or an adapter + its logic module). Under
the strict 1:1 guard such a rule can **never** reach `resolved` — so it cannot join
`coverage_scope`, and the coverage gate is frozen below 100% for as long as any multi-organ rule
exists. BACKLOG #201 records this: *"the 1:1 resolver returns `ambiguous` for >1 code site, so a
two-organ rule can never reach `resolved` and would freeze the coverage gate <100%."* It named
three blocked rules: `governance-no-ff`, `governance-child-floor`, `governance-backlog-leave`.

The real question was never "drop the duplicate-guard" (that would let accidental duplicate-ID bugs
resolve silently) — it was: **how does a rule say "I am legitimately enforced in N organs, and N is
correct"** so the resolver can tell intentional multiplicity from an accidental duplicate?

## Decision

**Adopt resolver-allows-N: a rule may declare its expected code-site count, and the resolver
resolves that rule iff it has exactly one doc site and exactly the declared number of code sites.**

1. **A declared `multi_site:` map** (`ecosystem/doc-code-edge.yaml`, sibling to `coverage_scope:`):
   `rule-ID → expected code-site count (int ≥ 2)`. A rule listed there is an *intentional*
   multi-organ rule; the integer is the number of organs that legitimately enforce it.

2. **Resolver logic.** `resolve_edge(..., multi_site: dict[str,int] | None = None)`:
   - A rule **in** `multi_site` resolves iff `len(doc_sites) == 1 and len(code_sites) ==
     multi_site[rule_id]`; **any** other count — including the declared count ±1 — is still
     `ambiguous`. The guard keeps its teeth: adding an unannounced fourth organ to a count-3 rule,
     or losing one, still flags.
   - A rule **not in** `multi_site` keeps the strict `len > 1 → ambiguous` duplicate-guard,
     unchanged. The default stays conservative; multiplicity is opt-in per rule.
   - The same `multi_site` threads into `scan_structural_integrity` / `build_edge_index` so a
     declared multi-site rule does not also raise a `duplicate_code` structural finding.

3. **The expected count is declared, not inferred — and that is the whole point.** The resolver
   cannot tell, from the annotations alone, whether a second `# rule: ID` is a real second
   enforcement organ or a copy-paste bug. The declared integer is the human fact that separates
   them. This is ADR-88's *declare what you cannot compute* applied to multiplicity: how many organs
   *should* enforce a rule is a property of the enforcement design, not derivable from the code.

## Rejected alternative — canonical-organ-only

BACKLOG #201's other option was *canonical-organ-only*: annotate exactly one (the "canonical")
organ of a multi-organ rule and ignore the rest. **Rejected.** It would leave real enforcement
sites *unmapped* — the doc→code edge would report a rule as covered while N−1 of its enforcing
organs carry no edge at all. That defeats the completeness goal the whole #201→#202→#203 chain
exists for: #203's coverage drift-guard maps the `ALL_CHECKS` enforcement surface, and an
un-annotated enforcement organ is precisely the silent-escape it must catch. resolver-allows-N maps
**every** organ of a rule; canonical-organ-only maps one and hides the others.

## Scope — what this enables, and its limits

- **v1 consumers:** the three governance rules BACKLOG #201 named — `governance-no-ff` (detect +
  prevent, count 3), `governance-child-floor` (detect adapter + emit-gate, count 2),
  `governance-backlog-leave` (in-file marker + git-drift + audit adapter, count 3) — each verified
  genuinely multi-organ (no fake residual), plus the retro `coherence-spec-reconciled` (count 2).
  The #202 Tier-3 rules (an `audit.py` adapter + its `validate_*`/`verify_*` logic module) also
  consume it at count 2.
- **The count is exact, not a floor.** `multi_site[rid] = 3` means *exactly* three — this is a
  duplicate-guard variant, not a "≥1" relaxation. A rule that legitimately grows a fourth organ
  bumps its declared count in the same change that adds the organ; until then the new organ flags.
- **Doc side stays 1:1.** A rule still declares at exactly one authoritative doc site (ADR-89 OQ1:
  declare at the source, never in a summary). Only the *code* side may be N. `len(doc_sites) != 1`
  is `ambiguous` regardless of `multi_site`.
- **Fail-soft loader.** `multi_site:` is read with the same fail-soft → `{}` contract as
  `coverage_scope`/`declaration_docs`; a missing/malformed map degrades every rule to the strict
  1:1 guard (conservative — it can only *narrow* what resolves, never silently widen it). The
  hard-gate-promotion forward-flag (ADR-89 OQ3: WARN-on-missing/malformed-config) applies here too.

## Consequences

- The coverage gate can reach 100% over a scope that includes multi-organ rules — the #201→#203
  completeness chain is unblocked.
- The duplicate-guard is **preserved**, not weakened: undeclared multiplicity, and declared-count
  mismatch in either direction, still flag `ambiguous`. Opt-in per rule, conservative by default.
- The `multi_site:` map is a small, hand-edited, durable declaration (the `doc-code-edge.yaml`
  precedent — one concern per file, `yaml.safe_load`, Layer-2 read-only). It is the *only* new
  declaration burden, and it is bounded by the count of genuinely multi-organ rules (a handful).
- **resolver-allows-N is reversible.** Recorded here so a future revision (e.g. moving to
  canonical-organ-only, or a different multiplicity model) is a conscious, documented change rather
  than silent drift.

## Links

- PLAYBOOK §"Lifeline 2 — Coherence" (the code↔doc row) — points here for the rationale.
- BACKLOG #201 — the decided scheme + the three blocked governance rules.
- ADR-89 OQ1 — the doc→code rule-ID naming convention + registry mechanism this extends.
- ADR-88 — file-oriented dependency management (the declared-edge paradigm; the expected count is a
  declaration under it).
- `ecosystem/doc-code-edge.yaml` — the `multi_site:` map (build site) + the DEFERRED two-organ block
  this resolves.
- `scripts/validate_doc_code_edge.py::resolve_edge` — the resolver the `multi_site` parameter
  threads through.
