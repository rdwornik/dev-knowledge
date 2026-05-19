---
scale: <S | M | L>
last_reviewed: <YYYY-MM-DD>
status: <active | maintenance | archived>
owner: <Rob | other>
---

# Architecture — `<repo-name>`

> Living document. Updated after structural changes.
> Last updated: `<YYYY-MM-DD>` (`<short note on what changed>`)

## Applicability & conventions

**This template is the single canonical `ARCHITECTURE.md` for the `.dev-knowledge` ecosystem.** It is mandated by ADR-51 and inherited unchanged by every repo that adopts it. There are no per-tier template variants — scale-specific behaviour is handled by the inline conditionals below.

**Scale rules:**

- **L** — `ARCHITECTURE.md` is mandatory at repo root (ADR-38 A3). Use the full template; the L-scale optional sections (`Module Map`, `Design Patterns`, `Architecture Assessment`, etc.) are normally completed.
- **M** — `ARCHITECTURE.md` is mandatory at repo root (ADR-38 A3). Use the template; L-scale-optional sections are at author discretion.
- **S** — `ARCHITECTURE.md` is **exempt by default**. An S repo MAY voluntarily adopt this template; if it does, only the **CORE** sections (`Purpose`, `Codemap`, `Layer Boundaries & Invariants`) are completed, in *text-only* mode — no diagrams, no auto-generated codemap, the codemap section becomes a plain module overview.

**Section scale tags:** every `##` header carries a visible bracketed tag — `[CORE]`, `[M/L]`, `[L-opt]`, `[L]`. Authors keep the tags; delete only the sections that do not apply at their scale.

**Pointer convention (doc-wide).** Cross-references to other artifacts use a single line: `→ <description>: `<relative/path>`` (arrow + colon, backticked path). Used in §3 and §11 below as well as §4 Diagrams.

**Open item — codemap generator output specification.** ADR-51 mandates an auto-generated, CI-freshness-checked codemap, but the generator's output spec (directory tree vs package dependency graph vs CLI inventory) is **undecided**. Until that question is resolved, the `## Codemap` section is hand-maintained in the interim format described below. Tracked in `BACKLOG.md` Stream C and ADR-51 open questions.

→ Convention: `.dev-knowledge/docs/decisions/ADR-51-architecture-doc-convention.md`
→ Universal repo baseline: `.dev-knowledge/docs/decisions/ADR-38-universal-repo-architecture.md`

---

## Purpose [CORE]

`<One focused paragraph. Bird's-eye description of what this repo is, what it does, and who/what it serves. No preamble, no history, no roadmap — just the present-tense answer to "what is this codebase?".>`

---

## Codemap [CORE]

This codemap is the auto-generated **structural** artifact for the repo. A CI freshness check regenerates it on every commit and fails the build if the committed output differs from a fresh regeneration. The narrative invariants in §3 are **not** generated — only the structural map is.

> **Open item.** The codemap generator's output specification is undecided (directory tree vs package dependency graph vs CLI inventory — ADR-51 open question). Until the generator and its spec exist, the region below is **hand-maintained** in the interim format. Tracked in `.dev-knowledge/BACKLOG.md` Stream C.

**Interim hand-maintained format (M/L):** a package-level directory tree of the primary source namespace, each line annotated with a layer label and a one-phrase role.

<!-- CODEMAP:START -->
```
src/<package_name>/
  <module_a>/        <one-phrase role> (<layer>)
  <module_b>/        <one-phrase role> (<layer>)
  <module_c>/        <one-phrase role> (<layer>)
  (root-level)       <names of any package-root utility files>
```
<!-- /CODEMAP:START -->
<!-- CODEMAP:END -->

> **S-scale override.** If this template is voluntarily adopted by an S repo, replace the fenced block + CODEMAP markers above with a plain prose paragraph listing the modules and their roles. No machine region, no generator dependency.

---

## Layer Boundaries & Invariants [CORE]

### Layer model

`<Name the layers, in dependency order (lowest-to-highest or highest-to-lowest — pick one and be consistent). Cite the enforcement tool and its config file.>`

**Example only — adapt or replace:** corp-monorepo uses a 4-layer model `interface > orchestration > core > foundation` enforced by Tach via `tach.toml`. The example is illustrative — this template does **not** mandate any specific layer set, count, or enforcement tool. Each repo names its own layers.

**Enforcement tool:** `<e.g., Tach / import-linter / dependency-cruiser / custom AST check>`
**Config file:** `<e.g., tach.toml / .importlinter / depcruise.config.js>`
**Where enforced:** `<e.g., pre-commit hook + CI>`

### Module-to-layer assignment

| Layer | Modules |
|-------|---------|
| `<layer-1>` | `<module>, <module>, ...` |
| `<layer-2>` | `<module>, <module>, ...` |
| `<...>` | `<...>` |

Utility-exemption modules (importable from any layer): `<list, or "none">`.

### Invariants

Numbered, assertion-style statements — each one is testable in principle (a violation is detectable by inspecting code, a database, or a log). Not descriptions of behaviour; **claims** about behaviour.

1. `<assertion, e.g., "Module X is the SOLE writer of resource Y.">`
2. `<assertion>`
3. `<assertion>`
4. `<add as needed — 5-10 invariants is typical at L scale>`

→ Related decisions: `<docs/decisions/ADR-NN-...>` (one line per binding ADR)

---

## Diagrams [M/L]

Graphical complement to the text codemap. Diagrams **complement, not replace** the text codemap — the codemap is the canonical machine-readable view; diagrams are for human orientation.

**Source format:** Mermaid (`.mermaid` files under `docs/diagrams/`).
**Render pipeline:** Mermaid source → SVG. Any Mermaid-to-SVG renderer is acceptable (e.g., `mmdc` via npm); the specific tool is a repo-level choice and lives in a render script under `scripts/` or a CI job. **No specific tool is mandated by this template.**
**Output location:** SVGs co-located with their `.mermaid` sources (`docs/diagrams/*.svg`).
**Freshness check intent:** the CI codemap freshness check should be extended (or paired with a separate hook) to detect `.mermaid` sources that have changed without a corresponding SVG regeneration. Pending implementation — tracked alongside the codemap generator open item.

**Standard diagram set (recommended starting point — add or omit as the repo needs):**

| Diagram | Source | Output | Inline reference |
|---------|--------|--------|------------------|
| System context (C4 L1) | `docs/diagrams/system-context.mermaid` | `docs/diagrams/system-context.svg` | placed at the end of §1 Purpose |
| Module map (C4 container) | `docs/diagrams/module-map.mermaid` | `docs/diagrams/module-map.svg` | placed at the end of §2 Codemap or §5 Module Map |
| Pipeline / data flow | `docs/diagrams/pipeline.mermaid` | `docs/diagrams/pipeline.svg` | placed at the end of §6 Data Flow |

**Inline reference format:** at the end of each relevant section, add one line — `→ <diagram name>: `docs/diagrams/<file>.svg``. Per the pointer convention defined in the header.

---

## Module Map [L-opt]

> **Optional** — L-scale typically uses this section; M discretionary; S omits.

Per-package tables listing every file (or every public module) with a one-line responsibility. This is the **hand-written semantic complement** to the auto-generated structural codemap in §2 — `§2` answers *what exists and how it nests*; `§5` answers *what each piece is responsible for*.

### `<package_a>/`

| Module | Responsibility | Key exports |
|--------|----------------|-------------|
| `<file.py>` | `<one-line responsibility>` | `<symbol, symbol>` |
| `<...>` | `<...>` | `<...>` |

### `<package_b>/`

| Module | Responsibility |
|--------|----------------|
| `<file.py>` | `<one-line responsibility>` |
| `<...>` | `<...>` |

`<repeat per top-level package>`

---

## Data Flow [L-opt]

> **Optional** — completed when the repo has a non-trivial end-to-end pipeline worth orienting around.

End-to-end pipeline as numbered steps or an ASCII flow diagram.

```
1. <entry point — what arrives, where>
       |
2. <next stage — what it does>
       |
3. <...>
       |
N. <terminal state — where the data ends up>
```

→ Pipeline diagram: `docs/diagrams/pipeline.svg` (if `## Diagrams` is populated)

---

## Database Schemas [L-opt]

> **Optional** — repo-specific. Complete when the repo owns one or more persistent stores worth documenting at the schema level.

### `<db-name>`

**Location:** `<path or environment-resolved location>` (`<mode notes, e.g., WAL, foreign keys ON>`)

| Table | Key columns | Writer | Purpose |
|-------|-------------|--------|---------|
| `<table>` | `<col, col, col>` | `<module that writes it>` | `<one-line purpose>` |
| `<...>` | `<...>` | `<...>` | `<...>` |

`<repeat per database>`

---

## Configuration Architecture [L-opt]

> **Optional** — repo-specific. Complete when configuration is spread across multiple sources and a single map is useful.

| Source | Format | Loader | Purpose |
|--------|--------|--------|---------|
| `<config/file.toml>` | `<TOML / YAML / dotenv>` | `<module.func()>` | `<purpose>` |
| `<...>` | `<...>` | `<...>` | `<...>` |

**Resolution order:** `<e.g., environment variable > config file > default>`.

**Key config classes:**
- `<ConfigClass>` — `<brief description, frozen / mutable, lifecycle notes>`

---

## CLI Reference [L-opt]

> **Optional** — orientation aid for command-heavy repos. Complete when the repo exposes a substantial CLI surface and a top-level index aids re-entry.

### `<primary-cli>`

| Command | Handler | What it does |
|---------|---------|--------------|
| `<cli verb args>` | `<module/file>` | `<one-line description>` |
| `<...>` | `<...>` | `<...>` |

### Secondary CLIs

| CLI | Entry point | Commands |
|-----|-------------|----------|
| `<cli>` | `<module.path:fn>` | `<short list>` |

---

## Design Patterns [L]

> **L-scale only.**

Catalog of architectural patterns the repo employs, with an honest quality assessment. The point of this section is to make pattern choices auditable: if a pattern is rated "good" and is later found to be a maintenance pain, the rating itself becomes a signal worth re-reading.

| Pattern | Where | Quality | Notes |
|---------|-------|---------|-------|
| `<pattern name>` | `<module / package>` | `<Excellent / Good / Adequate / Problematic>` | `<one-line note>` |
| `<...>` | `<...>` | `<...>` | `<...>` |

---

## Architecture Assessment [L]

> **L-scale only.** Honest self-assessment of the codebase. Not marketing copy.

### What Works Well

- `<one-line bullet — a specific strength, not a generality>`
- `<...>`

### Violations & Technical Debt

| Issue | Severity | Location | Status | Description |
|-------|----------|----------|--------|-------------|
| `<issue>` | `<High / Medium / Low>` | `<module / file>` | `<OPEN / IN PROGRESS / RESOLVED / ACCEPTED>` | `<one-line description>` |
| `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Resolved items may be retained with `~~strikethrough~~` and status `**RESOLVED**` for institutional memory.

### Accepted Limitations

| Item | Rationale |
|------|-----------|
| `<intentional compromise>` | `<why it is accepted, not a defect to fix>` |
| `<...>` | `<...>` |

→ Related audits / reviews: `<docs/audits/YYYY-MM-DD-...md>` (one line per binding artifact)

---

**Maintained by:** `<Rob | other>`
