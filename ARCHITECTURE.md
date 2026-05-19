---
scale: M
last_reviewed: 2026-05-19
status: active
owner: Rob
---

# Architecture — `.dev-knowledge`
<!-- scope: meta -->

> Living document. Updated after structural changes.
> Last updated: `2026-05-19` (ADR-51 + ADR-52 conformance rewrite)

## Purpose [CORE]

`.dev-knowledge` is the universal LLM-driven development guide and methodology framework for all `Dev/` projects. It is **Layer 2** of the ADR-28 three-layer ecosystem model — passive storage and governance authority, not an execution engine. It holds operational protocols, ADRs, handoffs, templates, and read-only validators; it prescribes conventions that child repos (corp-monorepo, ai-council, etc.) must follow; it is consulted as context by Claude Code, Codex, Cursor, Aider, and other agents. Nothing in this repo executes orchestration; everything here is read, consulted, or passively validated.

---

## Codemap [CORE]

The codemap is the canonical artifact answering *"what exists and how does it relate?"*. Transitional hand-maintained form — generator spec undecided (see BACKLOG Stream C and ADR-51 open questions).

> **Open item.** The codemap generator's output spec is undecided. This section is hand-maintained in the transitional text format until the generator ships.

<!-- CODEMAP:START -->
```
.dev-knowledge/
  VISION.md              universal brain mission statement (Layer 2, governance)
  ARCHITECTURE.md        this file — structural model (Layer 2, governance)
  README.md              entry point + file index (Layer 2, governance)
  CLAUDE.md              project contract for Claude Code (Layer 2, governance)
  CONTRIBUTING.md        branch/commit/validator conventions (Layer 2, governance)
  JOURNAL.md             per-session tactical log, append-only newest-first (Layer 2, record)
  LESSONS.md             append-only learning log (Layer 2, record)
  BACKLOG.md             cross-session pending items per ADR-41 (Layer 2, governance)
  protocols/             ESSENTIALS, PLAYBOOK, HANDOFF_PROCESS, SESSION_SETUP,
                           ENVIRONMENT — operational protocols (Layer 2, governance)
  logs/                  TOKEN-LOG.md — threshold-triggered snapshots (Layer 2, record)
  config/                requirements-dev.txt (Layer 2, config)
  docs/
    decisions/           ADR-NN-*.md + transcripts/ (Layer 2, record)
    handoffs/            per-session folder handoffs per ADR-32/42 (Layer 2, record)
    audits/              point-in-time analyses (Layer 2, record)
    research/            research-mode debates + external reports (Layer 2, record)
    tech-radar/          quarterly adoption snapshots (Layer 2, record)
  templates/             reusable boilerplate — CLAUDE-md, workspace
                           tiers, HANDOFF, prompt (Layer 2, governance)
  scripts/               read-only validators: audit.py, backlog_extract.py,
                           normalize_headers.py (Layer 2, validator)
  tests/                 pytest unit tests for validators (Layer 2, validator)
  ecosystem/             cross-repo ecosystem state snapshots (Layer 2, record)
  .claude/               project-level Claude Code config (Layer 2, config)
```
<!-- CODEMAP:END -->

---

## Layer Boundaries & Invariants [CORE]

### Layer model

`.dev-knowledge` is **Layer 2** of the ADR-28 ecosystem-level three-layer model (layers listed highest to lowest):

```
Browser chat (Layer 1, analysis)
        │ handoff → git commit
        ▼
.dev-knowledge (Layer 2, passive storage)
        │ read / pull as context
        ▼
Projects (Layer 3, execution)
        │ reflection → new browser chat
        └────────────────────────────────► (cycle closes at Layer 1)
```

**Enforcement tool:** advisory — the Layer 2 invariant is enforced by convention and the git-discipline rule.
**Config file:** `.claude/rules/git-discipline.md`
**Where enforced:** pre-commit (convention adherence); advisory in CLAUDE.md

### Module-to-layer assignment

| Ecosystem Layer | Role of this repo |
|----------------|-------------------|
| Layer 1 (Browser chat) | External — not in this repo |
| Layer 2 (`.dev-knowledge`) | **This repo** — passive storage, governance, prescription |
| Layer 3 (Projects) | External — corp-monorepo, ai-council, etc. |

Within Layer 2, directories by function:

| Function | Directories / files |
|----------|---------------------|
| Governance (living docs, protocols, templates) | `protocols/`, `templates/`, root `*.md` governance files |
| Record (dated artifacts, append-only logs) | `docs/`, `logs/`, `ecosystem/`, `JOURNAL.md`, `LESSONS.md` |
| Validators (read-only scripts + tests) | `scripts/`, `tests/` |
| Config | `config/`, `.claude/` |

Utility-exemption modules: none.

### Invariants

1. **Layer 2 never executes.** No script in `.dev-knowledge` orchestrates actions in other repos or drives state changes in Layer 3.
2. **Validators are read-only.** `scripts/` contains only passive inspection tools — they read, check, and report; they never write to other repos.
3. **`.dev-knowledge` is the prescriptive authority for all `Dev/` repos.** Prescriptions in PLAYBOOK and ADRs are binding on child repos; child repos may not override them locally.
4. **Append-only files are never edited.** `LESSONS.md` and `TOKEN-LOG.md` accept only appends — existing entries are never modified or deleted.
5. **Dated artifacts are immutable.** ADRs, transcripts, handoffs, and audits are superseded by new files or in-file markers, never edited in place.

→ Related decisions: `docs/decisions/ADR-28-three-layer-architecture.md`, `docs/decisions/ADR-39-file-lifecycle.md`

---

## Diagrams [M/L]

`.dev-knowledge` has no Mermaid diagrams currently. The three-layer architecture diagram in `## Layer Boundaries & Invariants` is inline ASCII and serves as the primary orientation aid.

When Mermaid diagrams are added, source files go under `docs/diagrams/` as `.mermaid` + `.svg` pairs per the template convention.

---

## Key conventions

- **Scope tags (ADR-27, informal).** `<!-- scope: X -->` tags (`dev | llm | hybrid | runtime | meta`) exist in living files as informal lightweight metadata. Enforcement withdrawn 2026-05-16 per ADR-48; existing tags remain in place. New sections do not need tags.
- **Append-only files.** LESSONS.md, TOKEN-LOG.md — never edit old entries. JOURNAL.md uses newest-first prepend.
- **Living files.** README, CLAUDE.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT, VISION, ARCHITECTURE — updated in place when reality shifts.
- **Immutable dated artifacts.** ADRs, transcripts, handoffs, audits, research — supersession via new file or in-file marker, never edit.
- **Filename conventions.** `ADR-NN-topic.md` for decisions (per ADR-34); `DECISION_NN_snake_case.md` for legacy transcripts (grandfathered); Council CLI output uses `council-out-YYYYMMDD-HHMMSS-topic.md`; kebab-case + ISO date for dated artifacts; ALLCAPS for top-level governance markdown.

---

## Authority and governance

Per ADR-31. `.dev-knowledge` is the **binding source of cross-repo prescriptions** (Authority model 1B — Prescriptive with conformance audit).

- **Scale tier:** M, with one L-tier artifact: this `ARCHITECTURE.md`.
- **Enforcement:** out-of-band, centralized, read-only audit tool (`scripts/audit.py` — pending full implementation per ADR-31). Reads sibling repos via explicit manifest; emits audit report. Manual invocation; no commit gating in downstream repos.
- **Content layout:** prescriptions live in PLAYBOOK + ADRs; dedicated `cross-repo/` subfolder deferred until prescription count exceeds ~10 or navigation becomes painful.
- **Baseline rule (ADR-31):** audit tool must run green on first invocation. One known violation remains open: corp-monorepo AGENTS.md exists and has not been removed (pending next-chunk work per ADR-53 Decision 2).

---

## Validators and enforcement (executable, here)

Per ADR-28 invariant: `.dev-knowledge` may host **read-only** validators (Layer 2 does not orchestrate, but it may verify itself).

- `scripts/audit.py` — cross-repo conformance audit; manual invocation.
- `scripts/backlog_extract.py` — backlog extraction utility; read-only.
- `scripts/normalize_headers.py` — dated-log header normalization; invoked by pre-commit hook.
- `tests/` — pytest unit tests for validators. Run: `pytest -x --tb=short`.
- **Pre-commit:** ruff (`ruff check --fix`) + normalize_headers.py hook.

---

## Governing ADRs

- **ADR-27** — scope tagging architecture (vocabulary; enforcement retired ADR-48; tags survive as informal metadata)
- **ADR-28** — three-layer architecture (descriptive)
- **ADR-29** — LESSONS.md grandfathering under scope tagging; scope-tag mechanics now informal per ADR-48; append-only invariant remains binding via CLAUDE.md and ADR-39
- **ADR-30** — default branch = `main` for all repos
- **ADR-31** — authority model: Prescriptive with conformance audit (1B); Scale M + ARCHITECTURE.md
- **ADR-32** — handoff format: folder-based, 9-section HANDOFF.md, manifest.json, point-in-time governance copies
- **ADR-33** — VISION.md universalization: mandatory at ≥1 dependent; Standard/Lite tiers
- **ADR-34** — file naming convention: UPPERCASE living docs, `ADR-NN-topic` for decisions, `YYYY-MM-DD-slug` for dated artifacts
- **ADR-35** — lessons base activation: push retrieval via SessionStart hook, pull via `lessons query`
- **ADR-36** — audit tool architecture: `.dev-knowledge` as ecosystem auditor; read-only, manually invoked
- **ADR-37** — session boundary protocol: two-phase handoff overlay (Current State + Future State)
- **ADR-38** — universal repo baseline: mandatory files per scale tier (S/M/L)
- **ADR-39** — file lifecycle governance: 6-element pattern (purpose/trigger/owner/grooming/boundaries/enforcement)
- **ADR-40** — scale tier evaluation: logarithmic Maintainability Index pattern; 3 signals; transition procedures
- **ADR-41** — cross-session backlog architecture: BACKLOG.md mandate at M+ tier
- **ADR-42** — handoff format v3: amends ADR-32; folder-based handoffs with invariant/session separation
- **ADR-43** — cross-project transcript routing: Council CLI dual-writes to `ai-council/output/` (operational) and `.dev-knowledge/docs/decisions/transcripts/` (curated)
- **ADR-46** — cross-repo dated-entries format: convention retained (demoted from audit-enforced 2026-05-16)
- **ADR-47** — cross-repo BACKLOG.md organization: convention retained (demoted from audit-enforced 2026-05-16)
- **ADR-48** — trim documentation governance: retired scope-tag and hybrid-ratio enforcement; structural enforcement only
- **ADR-49** — consolidate past-recording documentation files: governs record consolidation patterns
- **ADR-50** — machine-document encoding standard: governs how machine-written content is encoded and marked
- **ADR-51** — ARCHITECTURE.md convention: mandates this repo's ARCHITECTURE.md form and CORE sections
- **ADR-52** — AGENTS.md convention (superseded by ADR-53)
- **ADR-53** — CLAUDE.md as single canonical agent-instruction file: supersedes ADR-52

Reference `docs/decisions/README.md` for full index. Council debate transcripts in `docs/decisions/transcripts/`.

---

**Maintained by:** Rob
