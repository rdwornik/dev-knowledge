# Corp-Monorepo ARCHITECTURE.md — Inspection Report

**Date:** 2026-05-19
**Inspector:** Claude Code (Sonnet 4.6)
**Purpose:** ADR-51-mandated read-only reference input for authoring `templates/ARCHITECTURE-template.md`.
**Contract:** Read-only per ADR-36. No files in `corp-monorepo/` were modified.

---

## 1. Front Matter / Metadata

No YAML frontmatter block. Metadata is inline at the top:

```
# Architecture Reference -- Corporate OS
> Living document. Updated after structural changes.
> Last updated: 2026-03-30 (dependency layers clarified)
```

- **File:** `corp-monorepo/ARCHITECTURE.md`
- **Length:** 429 lines
- **Scale tier:** Not explicitly declared in `ARCHITECTURE.md` itself. Scale is declared in `corp-monorepo/CLAUDE.md` (not inspected for this report, but corp-monorepo is a large production system — L tier by ecosystem convention).
- **Opening callout:** Points readers to `docs/diagrams/` for SVG diagrams before the narrative begins.

---

## 2. Section Outline

Headings reproduced verbatim, in order:

| # | Heading | Content note |
|---|---------|--------------|
| H1 | `Architecture Reference -- Corporate OS` | Title + living-doc metadata tagline |
| H2 | `System Overview` | One-paragraph bird's-eye description + callout to SVG diagram directory; names all five CLIs; references `system-context.svg` |
| H2 | `Source Layout` | Fenced directory tree of `src/corp/` — one line per package with parenthetical layer label |
| H2 | `Module Map` | Per-package module tables across six sub-headings (see below) |
| H3 | `Root-Level Modules` | Table: module → responsibility → key exports (24 rows) |
| H3 | `schema/ -- Taxonomy & Validation` | Table: module → responsibility (10 rows) |
| H3 | `extractor/ -- CKE (Knowledge Extraction Engine)` | Table: module → responsibility (28 rows) |
| H3 | `extraction/ -- Extraction Orchestration` | Table: module → responsibility (6 rows) |
| H3 | `ingest/ -- File Routing Pipeline` | Table: module → responsibility (9 rows) |
| H3 | `ops/ -- Operational Database` | Table: module → responsibility (3 rows) |
| H3 | `Other Modules` | Compressed three-column table covering `retrieve/`, `cleanup/`, `overnight/`, `project/`, `opportunity/`, `rfp/`, `cli/` |
| H2 | `Dependency Layers` | 4-layer model description + enforcement mechanism (Tach) |
| H3 | `Layer Assignments` | Bold-labeled blocks listing every module by layer |
| H3 | `Runtime vs Static Depth` | Explains accepted 9-level runtime chain; clarifies it does not violate 4-layer static model |
| H2 | `Database Schemas` | Three sub-sections covering all SQLite databases |
| H3 | `ops.db` | Table: 8 tables × columns/writer/purpose |
| H3 | `index.db` | Table: 6 tables × columns/writer/purpose, including FTS5 trigger note |
| H3 | `overnight_state.db` | Table: 3 tables × columns/writer/purpose |
| H2 | `Configuration Architecture` | Table: 11 config sources × format/loader/purpose + resolution-order note + key config classes |
| H2 | `CLI Reference` | Two sub-sections |
| H3 | `corp (main CLI -- 40+ commands)` | Table: 26 listed commands × handler/description |
| H3 | `Secondary CLIs` | Table: 4 CLIs × entry-point/commands |
| H2 | `Data Flow` | Numbered 9-step fenced ASCII pipeline from file arrival to FTS5 index; references `magistrala-pipeline.svg` |
| H2 | `Design Patterns` | Table: 11 pattern instances × where/quality/notes |
| H2 | `Architecture Assessment` | Three sub-sections |
| H3 | `What Works Well` | 7 bulleted strengths |
| H3 | `Violations & Technical Debt` | Table: 6 historical issues (5 resolved, 1 accepted) with severity/location/status/description |
| H3 | `Accepted Limitations` | Table: 3 non-defect intentional compromises |
| H3 | `Key Invariants` | 7 numbered invariants — the policy layer of the document |
| H3 | `OneDrive safety guards (hotfix 2026-04-21)` | Extended prose section: guard pattern, 4-site table, exception class location, related audit/ADR pointers |

---

## 3. Codemap Representation

**Is there a codemap?** Yes — two forms coexist.

### Form A: Hand-written directory tree (Source Layout section)

```
src/corp/
  schema/          Taxonomy, models, validation, path config (foundation)
  extractor/       CKE -- knowledge extraction engine (core)
  ...
```

- A fenced code block listing every first-level package under `src/corp/`, each with a parenthetical layer label.
- **Type:** Directory tree annotated with layer and one-phrase role.
- **Hand-written or generated?** Hand-written. No generation script, no CI freshness check.
- **Granularity:** Package level only (not file level) in this tree; file-level detail is carried by the Module Map tables.

### Form B: Per-package module tables (Module Map section)

Each major package has its own table listing every `.py` file with a Responsibility column (and Key Exports for root-level modules). These tables are also hand-written.

**ADR-51 open question — codemap-spec resolution:**
The existing codemap is a **hybrid**: a package-level directory tree (Form A) plus per-package module tables (Form B). There is no generated component. The C4 diagrams (SVGs) are a *graphical* complement but do not replace or duplicate the text codemap — they show higher-level structural views (system context, module map at container level, pipeline flow).

---

## 4. C4 Pipeline Wiring

### Source location

Three Mermaid source files in `docs/diagrams/`:

| Source file | Diagram |
|-------------|---------|
| `docs/diagrams/system-context.mermaid` | System context (Level 1 C4) |
| `docs/diagrams/container-module.mermaid` | Module map (C4 container-level) |
| `docs/diagrams/magistrala-pipeline.mermaid` | Pipeline data flow |

### Render mechanism

Script: `scripts/render-diagrams.ps1`

```powershell
# Usage: powershell scripts/render-diagrams.ps1
# Requires: npm install -g @mermaid-js/mermaid-cli
Get-ChildItem -Path $diagramDir -Filter "*.mermaid" | ForEach-Object {
    $svgPath = $_.FullName -replace '\.mermaid$', '.svg'
    & mmdc -i $_.FullName -o $svgPath -t neutral --backgroundColor transparent
}
```

- Tool: `mmdc` (Mermaid CLI), installed globally via npm.
- Theme: `neutral`, background transparent.
- **Manual only — no CI integration found.** No Makefile, no CI job was found that calls this script. The script is available but not automated.

### SVG output location

Co-located with source: `docs/diagrams/system-context.svg`, `docs/diagrams/container-module.svg`, `docs/diagrams/magistrala-pipeline.svg`.

All three SVG files are present (confirmed by directory listing).

### How referenced in `ARCHITECTURE.md`

Inline arrow-pointer lines at the bottom of the relevant sections:

```
→ System context diagram: `docs/diagrams/system-context.svg`
→ Module map diagram: `docs/diagrams/container-module.svg`
→ Pipeline diagram: `docs/diagrams/magistrala-pipeline.svg`
```

Also a section-opening callout:
```
> **Visual diagrams** live in `docs/diagrams/`. Open the `.svg` files directly in VS Code ...
```

### Breakage observed

None obvious from read-only inspection. SVG files exist alongside their Mermaid sources. No automation gap causes data loss, but the absence of CI means SVG staleness is undetected if `.mermaid` sources change without re-running the script. This is a known risk; ADR-51 addresses it via mandatory CI freshness check.

---

## 5. Layer Boundaries / Invariants

### Layer model (explicit, enforced)

The document defines a 4-layer dependency model enforced by Tach (`tach.toml`) via pre-commit and CI:

```
interface > orchestration > core > foundation
```

Each layer is assigned in a clearly labeled sub-section with every module listed by name. Two modules (`schema/`, `routing_types`) are explicitly marked as "utility†" and are exempted from layer ordering (importable from any layer).

The accepted runtime depth exception (9-level chain via lazy imports) is documented inline with an explicit acceptance rationale.

### Key Invariants (7 numbered, all explicit)

1. `corp (ingest/)` is SOLE vault writer — narrowed by ADR-27
2. CKE (`extractor/`) is PURE extraction — no vault writes, no DB writes
3. Forward slashes everywhere in databases and stored paths
4. API keys in env vars — never in config
5. OneDrive exclusion — cleanup/audit NEVER touch "OneDrive - Blue Yonder" paths
6. WAL mode on all SQLite databases
7. Record-before-move — ops.db logged BEFORE filesystem operations

The OneDrive invariant has an extended enforcement section (hotfix 2026-04-21) detailing four mutation sites, guard patterns, exception classes, and related ADR/audit pointers.

---

## 6. Observations for ADR-51 Template Authoring

### What corp-monorepo does that the template should encode

| Observation | Template implication |
|-------------|---------------------|
| **Bird's-eye purpose leads the document** — System Overview is the first substantive section, one focused paragraph, no preamble | Template should mandate a "Purpose" section as H2 #1 |
| **Codemap is two-tier** — directory tree (package level) then per-package module tables | Template should allow/expect a directory tree *plus* optional detailed tables; not just one artifact |
| **Layer model is named and numbered** — every module assigned, enforcement tool cited | Template should require layer boundaries to be machine-verifiable (tool + config file citation), not just narrative |
| **Invariants are numbered and policy-complete** — each is a testable assertion, not a description | Template "Key Invariants" section should prompt numbered, assertion-style statements |
| **Violations/Technical Debt is a living section** — historical resolved issues retained with strikethrough | Optional but valuable; template could include as optional section |
| **Design Patterns table** — patterns catalogued with quality assessment | Optional at M scale; likely expected at L scale |
| **Assessment section** (What Works Well / Violations / Accepted Limitations) | Optional at M scale; L-scale repos benefit from explicit quality self-assessment |
| **OneDrive / safety-guard detail** is repo-specific — not generalizable | Template should NOT include this; it's an ecosystem-invariant sidebar, not a structural section |
| **References to other docs inline** (ADR-27, audit files) — uses `→` pointer convention | Template should define a standard pointer syntax for cross-references |
| **Database Schemas and Configuration Architecture sections** — deep implementation detail | These are optional, repo-specific; template should mark them as optional L-scale additions |
| **CLI Reference** — full command inventory | Optional; included in corp-monorepo as an orientation aid for a 40+-command surface |

### Discrepancies from ADR-51 mandatory core

| ADR-51 requirement | Corp-monorepo state | Finding |
|--------------------|---------------------|---------|
| Bird's-eye purpose statement | **Present** — System Overview section | Satisfied |
| Codemap (named modules/directories and how they relate) | **Present** — Source Layout tree + Module Map tables | Satisfied |
| Explicit layer boundaries | **Present** — Dependency Layers section with 4-layer model | Satisfied |
| Architectural invariants | **Present** — Key Invariants (7, numbered) | Satisfied |
| Auto-generated codemap (ADR-51 §5) | **Absent** — all content is hand-written | **Discrepancy.** ADR-51 mandates a CI-checked auto-generated codemap. Corp-monorepo's codemap is entirely manual with no CI freshness check. This is corp-monorepo's own compliance gap to resolve per ADR-36; recorded as finding only. |
| CI freshness check (ADR-51 §5) | **Absent** — render script is manual, no CI job | **Discrepancy.** Same root cause as above. Recorded as finding only. |

### Summary verdict

Corp-monorepo's `ARCHITECTURE.md` satisfies the *content* requirements of ADR-51's mandatory minimum (purpose, codemap, layers, invariants) and is a high-quality reference for the template's structure and depth. The primary gap is the **automation layer**: ADR-51 requires auto-generation + CI; the existing doc is hand-maintained. The template should be designed so that a hand-written doc can be progressively migrated to the auto-generated model once the codemap generator tool exists.
