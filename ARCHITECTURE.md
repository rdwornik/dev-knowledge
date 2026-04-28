---
version: 1.0
last_reviewed: 2026-04-28
owner: Rob
status: active
---

# ARCHITECTURE — .dev-knowledge
<!-- scope: meta -->

> **Purpose:** Document the structural model of `.dev-knowledge` — what it
> is, what's where, and which conventions bind. The "why" lives in ADRs;
> the "how Rob works" lives in PLAYBOOK; this file answers "how is the
> repo put together?" Required by ADR-31 (`.dev-knowledge` as Scale M
> with one L-tier artifact: ARCHITECTURE.md).

## Three-layer architecture

Per ADR-28 (descriptive). `.dev-knowledge` is **Layer 2** — passive
storage. No scripts execute orchestration here. Information flows
bidirectionally; execution flows one-way (Layer 2 → Layer 3).

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

PLAYBOOK § "System Architecture" carries the canonical diagram and the
invariant "Layer 2 never executes."

## Repository layout

```
(root)
├── VISION.md              ← universal brain mission (this layer)
├── ARCHITECTURE.md        ← this file
├── README.md              ← entry point + file index
├── CLAUDE.md              ← project contract for Claude Code
├── CONTRIBUTING.md        ← branch/commit/validator conventions
├── CHANGELOG.md           ← append-only, newest-first
├── JOURNAL.md             ← per-session tactical log, newest-first
├── LESSONS.md             ← append-only learning log
├── protocols/             ← operational protocols (ESSENTIALS, PLAYBOOK,
│                            HANDOFF_PROCESS, SESSION_SETUP, ENVIRONMENT)
├── logs/                  ← TOKEN-LOG (threshold-triggered snapshots)
├── config/                ← requirements-dev.txt
├── docs/
│   ├── decisions/         ← ADR-NN_*.md + transcripts/
│   ├── handoffs/          ← per-session folder handoffs (per ADR-32)
│   ├── audits/            ← point-in-time analyses
│   ├── research/          ← research-mode debates + external reports
│   └── tech-radar/        ← quarterly adoption snapshots
├── templates/             ← reusable boilerplate (CLAUDE-md, AGENTS-md,
│                            workspace-{S,M,L}, HANDOFF, prompt)
├── scripts/               ← validators (read-only — Layer 2 invariant)
├── tests/                 ← pytest unit tests for validators
└── .claude/               ← project-level Claude Code config
```

PLAYBOOK § "Documentation file types and session continuity" carries
the per-file taxonomy (purpose, format, cadence, audience, ordering)
and the Scale tier presence matrix.

## Key conventions

- **Scope tags (ADR-27).** Every section in living files carries a
  `<!-- scope: X -->` tag (`dev | llm | hybrid | runtime | meta`).
  Pre-commit hook enforces. File-level tag substitutes for per-section
  tags when all sections share a scope (per ADR-29 for LESSONS.md).
- **Hybrid ratio ≤25% (ADR-27).** Repo-wide hybrid section ratio
  delta-enforced — commits that regress past the ceiling are blocked.
- **Append-only files.** LESSONS.md, CHANGELOG.md, TOKEN-LOG.md,
  JOURNAL.md (with newest-first prepend for the latter three).
- **Living files.** README, CLAUDE.md, AGENTS.md (where applicable),
  PLAYBOOK, ESSENTIALS, ENVIRONMENT, VISION, ARCHITECTURE — updated
  in place when reality shifts.
- **Immutable dated artifacts.** ADRs, transcripts, handoffs, audits,
  research — supersession via new file or in-file marker, never edit.
- **Filename conventions.** `ADR-NN_topic.md` for decisions;
  `DECISION_NN_snake_case.md` for legacy transcripts (Council CLI
  output uses `YYYYMMDD_HHMMSS_topic.md` — naming consolidation
  pending, see `docs/decisions/transcripts/`); kebab-case + ISO date
  for dated artifacts; ALLCAPS for top-level governance markdown.

## Authority and governance

Per ADR-31. `.dev-knowledge` is the **binding source of cross-repo
prescriptions** (Authority model 1B — Prescriptive with conformance
audit).

- **Scale tier:** M, with one L-tier artifact: this `ARCHITECTURE.md`.
- **Enforcement:** out-of-band, centralized, read-only audit tool
  (`tools/audit.py` — pending implementation per ADR-31). Reads
  sibling repos via explicit manifest; emits `AUDIT.md` report.
  Manual invocation; no commit gating in downstream repos.
- **Content layout:** prescriptions live in PLAYBOOK + ADRs;
  dedicated `cross-repo/` subfolder deferred until prescription
  count exceeds ~10 or navigation becomes painful.
- **Baseline rule (ADR-31):** audit tool must run green on first
  invocation. Three known violations (ai-council AGENTS.md missing,
  ai-council CLAUDE.md ≤200-line trim, corp-monorepo AGENTS.md
  template) must be remediated before audit ships.

## Validators and enforcement (executable, here)

Per ADR-27 invariant: `.dev-knowledge` may host **read-only**
validators (Layer 2 does not orchestrate, but it may verify itself).

- `scripts/validate_scope_tags.py` — section-tag presence + hybrid
  ratio delta enforcement. Invoked by pre-commit hook on every commit.
- `tests/test_validate_scope_tags.py` — pytest unit tests for the
  ratio enforcement logic.
- Future: `tools/audit.py` per ADR-31 (cross-repo conformance audit).

## Governing ADRs

- **ADR-27** — scope tagging architecture (vocabulary, hook, hybrid ceiling)
- **ADR-28** — three-layer architecture (descriptive)
- **ADR-29** — LESSONS.md grandfathering under scope tagging
- **ADR-30** — default branch = `main` for all repos
- **ADR-31** — authority model (Prescriptive with conformance audit;
  Scale M + ARCHITECTURE.md)
- **ADR-32** — handoff format and browser/agent role split
