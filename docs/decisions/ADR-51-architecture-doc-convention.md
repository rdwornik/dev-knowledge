# ADR-51: Architecture Documentation Convention for the `.dev-knowledge` Ecosystem

- **Status:** Accepted
- **Date:** 2026-05-18
- **Amends:** —
- **Decommission:** none
- **Source:** AI Council debate (`pick` mode, 4-model panel + synthesizer, 2026-05-18). Transcript: `docs/decisions/transcripts/council-out-20260518_215241-pick-2026-05-18_council-debate-architecture-doc.md`

## Context

The `.dev-knowledge` ecosystem is maintained by a single developer across repositories of varying scale (`Project Scale: S / M / L`, declared in each repo's `CLAUDE.md`). Re-orientation after weeks away from a repository is slow and unsupported, and architecture documentation today is inconsistent — `corp-monorepo` has an `ARCHITECTURE.md`, most repositories have none.

A prior manual-upkeep document — a single-file handoff — went roughly five weeks stale before being retired. This establishes the dominant constraint: any convention that relies on remembered manual updates has already been empirically falsified in this ecosystem.

An AI Council debate was run to settle a standard convention. This ADR records its outcome.

## Decision

1. **Coverage.** A dedicated `ARCHITECTURE.md` is mandatory for **M-** and **L-scale** repositories. **S-scale** repositories are exempt; an S repo may add an optional "Architecture" section to its `README.md` if re-entry friction appears.

2. **Artifact.** The document is a dedicated `ARCHITECTURE.md` at the repository root. Architecture content is **not** folded into `CLAUDE.md` — agent instructions and human re-orientation remain separate artifacts with disjoint contracts (`README.md` = what this is; `CLAUDE.md` = how to work with it; `ARCHITECTURE.md` = what exists and why; `docs/decisions/` = decision history).

3. **Template and depth.** A single canonical template lives in `.dev-knowledge` — no per-repository copies (ADR-36/38). It defines a mandatory core that every covered repository completes, plus optional sections larger repositories add. Optional sections are expected mainly at L scale.

4. **Mandatory minimum content.** Every covered `ARCHITECTURE.md` contains: a bird's-eye purpose statement; a codemap (named modules/directories and how they relate); and explicit layer boundaries and architectural invariants.

5. **Staleness control — hybrid.** The structural codemap is **auto-generated** from the codebase; only narrative (purpose, invariants) is hand-written. A **CI check** regenerates the codemap and fails if the committed output differs — enforced from day one. The weekly `/evolve` review aggregates these checks and reviews whether hand-written invariants still match the current architecture.

6. **Graphical depth — tiered.** M- and L-scale repositories use a **graphical** codemap (diagram). Where an S-scale repository documents architecture at all, it uses a **text-only** general module overview — no diagram.

## Consequences

- The ecosystem commits to building and maintaining two shared tools in `.dev-knowledge`: a codemap generator and a CI freshness check. Because the codemap is part of the mandatory minimum (Decision 4), the generator is **load-bearing** — it must exist before any M/L repository can satisfy the convention.
- Hand-written invariants remain the human-authored heart of the document. The codemap is the *map*; the invariants are the *policy*. Generation never overwrites the invariants — a generated map would otherwise normalise architectural drift by drawing a breach as truth.
- Each covered repository's `CLAUDE.md` gains a one-line pointer to `ARCHITECTURE.md`.
- Initial rollout targets the current M/L repositories: `corp-monorepo`, `ai-council`, `corp-ops`.
- S repositories receive less structured re-entry support; this is accepted because an S repo is small enough that the README and the code itself are the document, and a near-empty `ARCHITECTURE.md` rots fastest and trains the author to ignore the file.

## Open questions — not settled by this ADR

- **Codemap generator output spec.** The debate did not define what the generated codemap should contain — directory tree, package graph, CLI/module inventory. Under-generation fails orientation; over-generation produces noise. This needs a separate design pass.
- **The existing `corp-monorepo` `ARCHITECTURE.md`.** `corp-monorepo` already has an `ARCHITECTURE.md` and a C4 Mermaid→SVG pipeline; neither was inspected during the debate. Both should be reviewed as input to the template and the generator before either is authored.
- **Shared-tooling versioning.** How repositories consume the `.dev-knowledge` generator and linter safely (pinning by tag/SHA) is undefined.
- **Pilot criteria.** Pilot duration, success metrics (did re-orientation get faster? did CI catch drift?), and revert conditions are not defined.

## Alternatives considered

- **Universal coverage** — `ARCHITECTURE.md` in every repository regardless of scale. Rejected: S repos are single-purpose; a near-empty document rots fastest and erodes trust in the convention.
- **Architecture content inside `CLAUDE.md`.** Rejected: conflates agent-instruction and human-re-orientation audiences, bloats agent context, and complicates drift detection.
- **Manual upkeep only** (with or without link-checking). Rejected: directly falsified by the five-week-stale handoff precedent.
- **Per-tier templates** (separate S/M/L documents). Rejected: triples the maintenance surface in `.dev-knowledge` for marginal benefit; incompatible with the single-canonical-template rule.
- **One-time codemap generation without ongoing CI.** Rejected: recreates the staleness problem in slower motion.

---

## Amendment 2026-05-22 — Codemap generator output specification

**Scope.** This amendment closes BACKLOG Stream C P2 ("Codemap generator output specification"). It specifies the codemap section's canonical output form, the generator tool interface, the freshness-check mechanism, edge case handling, Layer 2 invariant treatment, per-repo adoption model, and cross-reference to the operator-facing workflow documentation. The original Decision 6 example (external SVG reference) is superseded by the embedded Mermaid form defined here.

**Canonical target form.** The codemap section of every M/L `ARCHITECTURE.md` is an auto-generated fenced Mermaid block between `<!-- CODEMAP:START -->` and `<!-- CODEMAP:END -->` markers. The block is written in place by `scripts/codemap/cli.py` using the `--write` flag. VS Code 1.121 (released 2026-05-20) and GitHub render Mermaid natively with panning and zooming; no SVG generation step is required. The prior canonical-target example (`<img src="docs/diagrams/codemap.svg" alt="codemap" />`) in `templates/ARCHITECTURE-template.md` is replaced by an embedded Mermaid example (updated in the same commit arc as this amendment).

**Required content.** The generated block contains: top-level Python packages as nodes (one node per package directory under the repo's configured source root); intra-source-root import edges as directed arrows; layer assignments read from `tach.toml` (if present) as `classDef` color mappings; and click directives per node pointing to each package's source directory for navigation.

**Edge cases — surfaced, not silenced.** The generator does not suppress anomalies; it classifies them visually and emits warnings to stderr:

- *Orphan modules* (zero in/out edges): assigned `:::orphan` class (dashed border); generator emits stderr warning to prompt operator investigation.
- *Circular dependencies*: nodes involved assigned `:::cycle` class (red border); edges in the cycle styled red; generator emits stderr warning. A circular dependency is an architectural smell — the right response is to investigate import structure, not to silence the signal.
- *Missing source root* (the configured `--source-root` directory does not exist): generator returns an empty package list with a stderr warning; the inline block is updated to `(no Python packages detected at <source_root>)`.
- *Missing `tach.toml`*: degraded mode — codemap generated without layer color assignments; generator continues without warning. Adding `tach.toml` post-hoc restores layer colors on the next generation.
- *Missing `ARCHITECTURE.md` or CODEMAP markers*: generator fails with an operator-actionable error message. Resolution: create `ARCHITECTURE.md` from `templates/ARCHITECTURE-template.md` and ensure both markers are present before re-running.

**Generator tool.** The tool lives at `scripts/codemap/` in `.dev-knowledge` — a stdlib-only Python package (no pip install required in consumer repos). CLI interface:

```
python -m scripts.codemap.cli generate <repo_path> [--source-root <path>] [--write]
python -m scripts.codemap.cli check <repo_path> [--source-root <path>]
```

`generate` without `--write` prints the generated Mermaid block to stdout for inspection. `generate --write` rewrites `ARCHITECTURE.md` in place between the CODEMAP markers. `check` regenerates in memory, diffs against the committed ARCHITECTURE.md content, and exits non-zero with a unified diff on any drift. Default `--source-root` is `src/`; repos with non-standard layout (e.g., `.dev-knowledge` itself uses `scripts/`) supply `--source-root <path>` explicitly.

**Layer 2 invariant treatment — addresses Codex CRITICAL from Prompt 1 review.** The codemap generator's `--write` path mutates `ARCHITECTURE.md`. ADR-28 and ADR-36 establish the Layer 2 read-only-validators invariant: audit and check tools in `.dev-knowledge` must not mutate state in other repos. This ADR-51 amendment explicitly clarifies the boundary: **the codemap generator is a distinct category from Layer 2 validators**. A validator reads state and reports findings; a generator writes the canonical form of a derived artifact from a declared source of truth (here: Python import graph → Mermaid codemap). The `check` subcommand IS a validator and remains Layer 2-compliant (read-only, non-mutating). The `generate --write` subcommand is the generator role; it mutates only `.dev-knowledge`'s own `ARCHITECTURE.md` when run on `.dev-knowledge` itself, or a child repo's `ARCHITECTURE.md` when a child repo operator invokes it locally. This distinction does NOT require amending ADR-28 or ADR-36 — both remain unchanged and fully in force. Future generator-category tools (e.g., a `.gitignore` synthesizer, a formatter) inherit this same boundary clarification without additional ADR amendments.

**CI freshness gate.** Each repo that adopts the generator opts in via a local hook entry in `.pre-commit-config.yaml` invoking `codemap check`. The hook fires when Python source files, `pyproject.toml`, `tach.toml`, or `ARCHITECTURE.md` itself change (configurable `files:` regex). A hook failure blocks the commit until the operator runs `generate --write` and stages the updated `ARCHITECTURE.md`. The specific hook entry form is documented in `protocols/PLAYBOOK.md` § Codemap workflow.

**Per-repo adoption — opt-in, not mandatory.** ADR-51 Decision 4 mandates that every M/L `ARCHITECTURE.md` contain a codemap section. This amendment specifies the canonical generated form of that section. However, ADR-51 does NOT mandate generator-based maintenance — a repo may satisfy Decision 4 with a hand-maintained transitional codemap until it opts in to the generator. Adopting the generator and freshness gate is a per-repo commitment made by that repo's operator. `.dev-knowledge` opts in via this amendment (dogfooded in the same commit arc). Other repos (corp-monorepo, ai-council) opt in independently in future sessions per Hard Constraint #1 (do not touch child repos in this session).

**Operator workflow reference.** The step-by-step generation cadence, manual invocation commands, edge case handling guidance, per-repo opt-in checklist, and troubleshooting notes live in `protocols/PLAYBOOK.md` § Codemap workflow (added in the same commit arc as this amendment).

**Backlog status.** Stream C P2 ("Codemap generator output specification") is CLOSED by this amendment.

---

## Amendment 2026-05-23 — ARCHITECTURE.md mandatory universally (tier-conditional removed)

**Scope.** Reconciles Decision 1 (coverage) and Decision 6 (graphical depth)
with the ecosystem-wide tier deprecation (operator decision 2026-05-23). This
amendment is **distinct from** the 2026-05-22 codemap amendment above, which is
unaffected and remains fully in force (canonical Mermaid form, CODEMAP markers,
generator/`check` interface, Layer 2 boundary clarification, opt-in adoption).

**Delta — Decision 1 generalized to universal.** The tier-conditional coverage
mandate ("mandatory for M- and L-scale; S-scale exempt") is generalized: a
dedicated `ARCHITECTURE.md` at repo root is now **mandatory for every covered
repo regardless of scale**. The S-scale exemption and the README-section
fallback are withdrawn. Cross-references [[ADR-38]] amendment A5 (same date),
which adds `ARCHITECTURE.md` to the universal governance baseline and scopes
the audit's `check_adr38_baseline` to it. Root-placement (ADR-38 A3) is
unchanged.

**Delta — Decision 6 depth note.** With tiers removed, the "graphical for M/L,
text-only for S" split no longer gates on a declared tier. Graphical
(generated Mermaid) codemap remains the canonical form per the 2026-05-22
amendment; a repo too small for a meaningful package graph MAY use a text-only
module overview as a transitional form (judgment call by the repo operator),
but this is no longer tier-determined.

**Consequence for the original "Alternatives considered."** The "Universal
coverage" alternative — previously rejected on the grounds that a near-empty
`ARCHITECTURE.md` in a tiny repo rots fastest — is now adopted. The operator
accepts that trade-off: a single universal structural artifact is preferred
over per-tier branching, and the codemap freshness check (2026-05-22
amendment) mitigates rot for repos that opt into the generator.

- **Decision tier:** Conversational (reconciliation of an already-decided
  operator directive; supersedes only the tier-conditional clause of
  Decision 1).

## Amendment 2026-05-28 — Mermaid dark-theme directive standard

**Scope.** Every Mermaid block in every covered repo — generator-produced
(via `scripts/codemap/cli generate --write`) and hand-authored
(layer/process diagrams in `ARCHITECTURE.md`, examples in templates) —
MUST begin with `%%{init: {'theme':'dark'}}%%` as the first line inside
the triple-backtick fence, immediately before the `flowchart`/`graph`
declaration.

**Rationale.** Rob's VS Code uses a black background. Mermaid's default
(light) theme renders body text in dark gray, which is unreadable on
black. The built-in `'dark'` theme uses light text on mid-gray fills and
is readable across all current diagrams in the ecosystem.

**Implementation.** The codemap generator (`scripts/codemap/mermaid_emit.py`)
emits the directive automatically; regenerating any repo's codemap
preserves the standard. Hand-authored blocks in `ARCHITECTURE.md` carry
the directive in-file. The canonical example in
`templates/ARCHITECTURE-template.md` includes the directive so new repos
inherit it.

**Out of scope.** Immutable dated artifacts (audits, transcripts,
handoffs, ADRs) with embedded Mermaid blocks are NOT retrofitted —
per ADR-39 they are point-in-time records and stay as written. New
immutable artifacts authored after this date SHOULD include the
directive going forward.

**Variant.** If `'theme':'dark'` ever proves insufficient (fills too
close to black on a specific diagram), the custom-base form
(`'theme':'base'` + `themeVariables`) is the documented fallback —
deviating from the standard requires a per-block justification comment.

**Verification.** `grep -c "theme':'dark'"` in each `ARCHITECTURE.md`
should equal `grep -c '\`\`\`mermaid'`. Operator does the final visual
render check in VS Code on black background.

**Decision tier:** Conversational (style standard; no semantic change
to diagram content or generator interface).

## Amendment 2026-05-28 (v2) — Mermaid high-contrast custom-theme standard (supersedes bare 'dark')

**Scope.** Supersedes the bare `%%{init: {'theme':'dark'}}%%` directive
mandated by the prior 2026-05-28 amendment. That standard turned out to
work only for diagrams whose `classDef` rules already pinned an explicit
`color:` (e.g., the .dev-knowledge layer model). For diagrams whose
`classDef` rules set a light-pastel `fill:` but omitted `color:`, the
bare dark theme inherited a near-white default text color, producing
light text on light pastel fills — unreadable on black. The three
process diagrams in `.dev-knowledge/ARCHITECTURE.md` (workflow, council,
handoff) exhibited the failure mode; the codemap and layer-model blocks
did not.

**New standard.** Every Mermaid block — generator-produced and
hand-authored — MUST begin with the following directive (one line,
inside the triple-backtick fence):

```
%%{init: {'theme':'base', 'themeVariables': {'darkMode':true,'background':'#1a1a1a','primaryColor':'#2d2d3d','primaryTextColor':'#f0f0f0','primaryBorderColor':'#8a86ff','lineColor':'#a0a0ff','textColor':'#f0f0f0','mainBkg':'#2d2d3d','secondaryColor':'#3d2d3d','tertiaryColor':'#22323a','clusterBkg':'#222232','clusterBorder':'#555577','edgeLabelBackground':'#1a1a1a','titleColor':'#f0f0f0','nodeBorder':'#8a86ff'}}}%%
```

**Companion rule — explicit-color override (CRITICAL).** Every
`classDef` and inline `style` statement that sets a light-pastel `fill:`
MUST also set an explicit dark `color:` (`color:#000` for medium/strong
pastels; `color:#222` for very-light fills / gray / soft pastels).
Omitting `color:` causes the directive's `primaryTextColor` / `textColor`
default (light) to inherit, which on a light pastel `fill:` is
invisible. This is the root cause of the v1 dark-theme regression.

Mapping used across the ecosystem (apply uniformly when adding new
classDefs with these palette anchors):

| Fill | Text color |
|---|---|
| `#bde0fe`, `#a5d8ff`, `#74c0fc` (light/medium blue) | `color:#000` |
| `#e8e8e8` (light gray) | `color:#222` |
| `#fff3bf` (light yellow) | `color:#222` |
| `#d8f5a2` (light green) | `color:#222` |
| `#ffe3e3`, `#fff5f5` (very-light red/near-white) | `color:#222` |
| `#ffd8a8` (peach) | `color:#222` |

**Implementation.** The codemap generator (`scripts/codemap/mermaid_emit.py`)
now emits the new directive and the color-pinned `_ALL_CLASS_DEFS`
block; regenerating any repo's codemap preserves the standard. Hand-
authored blocks in `ARCHITECTURE.md` and the canonical example in
`templates/ARCHITECTURE-template.md` were updated in the same commit
arc as this amendment.

**Out of scope.** Immutable dated artifacts (audits, transcripts,
handoffs, ADRs) are NOT retrofitted, per ADR-39.

**Verification.** `grep -c "theme':'base'"` in each `ARCHITECTURE.md`
should equal `grep -c '\`\`\`mermaid'`; every `classDef` with `fill:#...`
should also contain `,color:#...`. Operator does the final visual render
check in VS Code on a black background — all diagrams (not just the
layer model) must show readable node text and edge labels.

**Decision tier:** Conversational (style standard; no semantic change
to diagram content or generator interface).

## Enforcement note 2026-05-28 — v2 standard now audit-enforced

`check_mermaid_theme_directive` added to `scripts/audit.py` as check #7. Scans
`ARCHITECTURE.md` and `templates/ARCHITECTURE-template.md` in every audited repo;
excludes immutable dated artifacts (`docs/audits/`, `docs/decisions/ADR-*`,
`JOURNAL.md`, `docs/archive/`). Violations cause `audit health` to degrade.
BACKLOG P3 "audit.py check — Mermaid high-contrast theme + explicit `color:` present"
closed 2026-05-28.
