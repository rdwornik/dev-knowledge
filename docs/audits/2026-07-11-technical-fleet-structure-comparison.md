# Fleet structure comparison — `.dev-knowledge` vs `ai-council` vs `corp-monorepo`

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-11
- **Source-session:** operator-requested L1/L2/L3 structural comparison; inventory gathered by three parallel Explore agents (one per repo), files+folders only, no code reads
- **Status:** complete
- **Model:** claude-opus-4-8[1m]

## Executive so-what

Same skeleton, three body types. All three repos share an identical canonical-doc spine
(VISION / ARCHITECTURE / CLAUDE / JOURNAL / LESSONS / BACKLOG + `docs/{audits,decisions,intake}`
+ `.claude/` + pre-commit) — that shared spine **is** the methodology the hub enforces fleet-wide.
They diverge on **role**, not skeleton:

```
.dev-knowledge = SOURCE  -> Layer-2 governance hub. NO app code (validators only,
                            "Layer 2 never executes"). Adds deploy/ ecosystem/ plugins/
                            templates/ .claude-plugin/; ships hooks (.pre-commit-hooks.yaml);
                            no INSTALL.md / .methodology.yaml (it is the source, not a consumer).
ai-council     = CONSUMER (small app) -> src/ai_council/ (~15 modules); transcript-heavy
                            (output/ ~238 + council_inbox/archive/ ~298 dominate file count).
corp-monorepo  = CONSUMER (large app) -> src/corp/ with ~13 domain subpackages; only repo
                            with CI (.github/); tach.toml module boundaries; data/ eval/ models/.
```

## Findings

### L1 — root files

```
COMMON TO ALL THREE (canonical living-doc spine + shared tooling):
  ARCHITECTURE.md · BACKLOG.md · CLAUDE.md · CONTRIBUTING.md · JOURNAL.md · LESSONS.md
  VISION.md · pyproject.toml · .pre-commit-config.yaml · .gitignore · .gitattributes
  .<repo>.code-workspace
  (JOURNAL size: dev ~1.3MB · corp ~129KB · ai ~63KB)

CHILDREN ONLY (absent in the hub):
  INSTALL.md            install steps — the hub is not "installed"
  .methodology.yaml     CONSUMER marker — hub has none because it IS the source

HUB ONLY (source / distributor role):
  .pre-commit-hooks.yaml   hook SOURCE (it ships hooks to the children)
  .claude-plugin/ + package.json + package-lock.json   plugin-marketplace / node
  .worktreeinclude         worktree config
  .ruff.toml               ruff config

CORP ONLY:
  tach.toml            module-boundary enforcement (unique to the big monorepo)
  .ruff.toml           lint config

AI-COUNCIL ONLY:
  .env                          root-level env secrets
  assets/ruff-pre-commit.yaml   ruff config lives here instead of a root .ruff.toml
```

### L1 — root folders

```
COMMON TO ALL THREE:   .claude/  docs/  logs/  scripts/  tests/  config/
HUB + AI (not corp):   protocols/            universal working-style docs (corp has none)
CHILDREN (not hub):    src/                  application code — hub has NONE by invariant

HUB ONLY:   deploy/ (carrier + manifest tooling)  ecosystem/ (fleet registry, one folder
            per child)  plugins/ (tier1-lifecycle)  templates/  .claude-plugin/  codex/
            config/  node_modules/  temp/  .vscode/
AI ONLY:    council_inbox/  assets/  output/ (~238 transcript files)
CORP ONLY:  data/  eval/  models/  output/  .github/  (ONLY repo with CI workflows)
```

### L2 / L3 — where the shapes diverge

```
docs/ (all three governance-shaped; hub is biggest):
  hub    archive/ audits/(~223) decisions/(~78 ADRs, to ADR-101) handoffs/(~70 dated
         session folders) intake/ runbooks/
  ai     archive/ audits/(~22) decisions/(~12 ADRs) intake/
  corp   archive/ audits/(~65) decisions/(~30 ADRs + transcripts/) diagrams/ intake/
  -> only CORP has docs/diagrams/ (mermaid/svg); only HUB has docs/handoffs/ + runbooks/.

scripts/ (diverge sharply by role):
  hub    ~45 validators/generators (validate_*, gen_*, audit.py, fleet_health.py)
         + subpkgs codemap/ hooks/ toc/  — a VALIDATION toolkit, no state-drivers
  ai     ~7 mixed py/ps1 gate + council-ask helpers
  corp   ~35 py/ps1 audit/eval/extraction utilities + archive/  — app-support scripts

src/ (the clearest divide):
  hub    NONE
  ai     ai_council/ ~15 modules + providers/ research/ subpackages
  corp   corp/ ~24 modules + ~13 domain subpackages (extraction, extractor, ingest,
         opportunity, ops, overnight, project, retrieve, rfp, schema, cleanup, cli,
         actions) — the true "monorepo" spine

tests/ (scale tracks app size):
  hub    ~72 test_*.py (mirror the validators) + fixtures/
  ai     ~19 test_*.py
  corp   ~20 top-level + ~20 domain test subfolders (extractor/ alone ~58 tests) — deepest tree

config-as-data (corp only):
  corp   config/ holds per-domain YAML trees (extractor/, project/, rfp/, opportunity/)
  hub    config/ = one requirements file
  ai     config/ = loader + settings.yaml

.claude/ (children carry a hash-guarded floor replica; the hub is the origin):
  hub    richest: agents/ commands/(4) generated/ rules/ skills/(check-against-spec, verify)
         workflows/ worktrees/ + methodology-roster.md ; NO CLAUDE-FLOOR.md (it's the origin)
  ai     commands/(override.md) rules/(3) + CLAUDE-FLOOR.md replica
  corp   commands/(override.md) skills/(gotchas) workflows/ worktrees/ + CLAUDE-FLOOR.md replica
```

## Recommendations / routing

No action requested beyond persisting this comparison as an evidence record. Nothing here is
a filing, close, or kill. If the divergences are later treated as parity gaps, that is an
intake concern (ADR-98), not an audit output — this document is evidence *about* current state.

## Scope / method

- **Covered:** file + folder structure of the three repos at L1 (root, most detailed), L2
  (inside each root folder), and L3 (inside each L2 subfolder). One-word gist per root file.
- **Not covered:** file contents / code (structural inventory only, no code reads); depths
  beyond L3; `.git/` internals; generated/cache dirs descended (`.venv`, `node_modules`,
  `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.hypothesis` — named only).
- **Method:** three parallel Explore subagents (one per repo) ran directory listings / Glob;
  large same-kind clusters were summarized with an approximate count rather than enumerated.
- **UNVERIFIED:** all file/folder counts are **approximate** (`~N`) as reported by the
  inventory agents at 2026-07-11; they are a point-in-time snapshot, not an exact census.
