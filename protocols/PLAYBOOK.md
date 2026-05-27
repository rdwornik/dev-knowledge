# Dev Practice Playbook

> **Living document.** Repeatable processes for everything Rob does regularly with AI-assisted development.
> Last updated: 2026-05-14

---

## System Architecture
<!-- scope: meta -->

**`.dev-knowledge` is not a journal and not an orchestrator.** It is the passive storage layer in a three-layer architecture. This section describes what is — it does not decree new constraints.

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1 — BROWSER CHAT (Claude.ai)  │  Analytical          │
│  Analysis, synthesis, critical thinking, Council debates    │
│  Produces: handoffs, ADRs, session summaries, Council briefs│
└──────────────────────┬──────────────────────────────────────┘
                       │ handoff → git commit
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2 — .dev-knowledge            │  Passive storage     │
│  Templates, patterns, lessons, ADRs, playbook, handoffs     │
│  Read by humans, Claude Code, future browser chats          │
│  No scripts reside here. Library, not daemon.               │
└──────────────────────┬──────────────────────────────────────┘
                       │ read / pull as context
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 3 — PROJECTS (Claude Code)    │  Execution           │
│  corp-monorepo, ai-council, sca-time-automation, etc.       │
│  Read from Layer 2, run tests, generate artifacts           │
│  Reflections → back to Layer 1 as new browser chat          │
└──────────────────────┬──────────────────────────────────────┘
                       │ reflection → new browser chat
                       ▼
                  (cycle closes at Layer 1)
```

### Rules
<!-- scope: dev -->

- **Layer 2 never executes.** No scripts, no orchestrator, no active daemon residing in `.dev-knowledge/`. Read-only execution semantics.
- **Write-back via Layer 1 only.** Claude Code (Layer 3) does not directly edit `.dev-knowledge/` files. Reflections flow back through browser chat → handoff → commit.
- **Bidirectional, not read-only.** Layer 2 is updateable via handoffs/ADRs/lessons from Layer 1. The *execution* direction is one-way (Layer 2 → Layer 3).
- **Separate from Obsidian vault.** Vault = pre-sales domain knowledge (see Section 13). `.dev-knowledge` = dev methodology. Different domains, different audiences, different write paths.

### Cross-reference
<!-- scope: meta -->

Section 13 "Where Knowledge Lives" describes knowledge **domains** (what lives where). This section describes workflow **layers** (how information flows). Complementary views of the same ecosystem.

---

## CLAUDE.md as agent-instruction contract
<!-- scope: meta -->

**Purpose:** Each repo (corp-monorepo, ai-council, .dev-knowledge, future projects) has a `CLAUDE.md` at root. Auto-read by Claude Code on session start. Auto-read by Codex via `project_doc_fallback_filenames = ["CLAUDE.md"]` in `~/.codex/config.toml`. **Substantive single canonical per-repo agent-instruction file (≤200 lines).** Per ADR-53.

### Authority hierarchy
<!-- scope: meta -->

1. `.dev-knowledge/protocols/ESSENTIALS.md` + `protocols/PLAYBOOK.md` (this file) — universal rules across all Rob's work
2. `{repo}/CLAUDE.md` — per-repo agent-instruction contract (architecture, conventions, tools, ADRs, anti-patterns)
3. `{repo}/.claude/skills/`, `commands/`, `hooks/` — runtime config

### What CLAUDE.md is
<!-- scope: meta -->

- **Single canonical agent-instruction contract** for both Claude Code and Codex operating in this repo
- Repo identity, architecture pointer, conventions, tools active here
- Lists slash commands, skills, hooks ACTIVE in this repo
- Critical rules and anti-patterns specific to this repo
- Recent ADRs binding here

#### Content-distribution map

Where each class of per-repo content lives (v2.1 template, 12 sections):

| Content class | Home |
|---|---|
| Session read order / identity | §1 First read + §2 Repo identity |
| Architecture overview | `ARCHITECTURE.md` — §3 carries a one-line pointer (required, every repo, per ADR-51 as amended 2026-05-23) |
| Conventions (naming, commits, testing, linting) | §4 Conventions |
| Toolchain commands (test/lint invocations) | §4 Conventions |
| Out-of-scope for this repo | §4 Conventions ("Out of scope" sub-section) |
| Critical governance rules | §5 Critical rules |
| Session start checklist | §6 Session start protocol |
| Slash commands | §7 Slash commands available |
| Skills (including gotchas) | §8 Skills active |
| Toolchain enforcement (hooks, pre-commit) | §9 Hooks active |
| Anti-patterns / Do NOT | §10 Anti-patterns |
| Council decisions / ADRs | §11 Recent ADRs |

**Not in CLAUDE.md:** universal rules (`.dev-knowledge/`), architecture docs (`ARCHITECTURE.md`), decision rationale (`docs/decisions/ADR-NN-*.md`).

### What CLAUDE.md is NOT
<!-- scope: meta -->

- Universal rules — those live in `.dev-knowledge/`
- Architecture documentation — that's `docs/ARCHITECTURE.md`
- Decision rationale — that's `docs/decisions/ADR-NN-*.md`

### Why ≤200 lines
<!-- scope: meta -->

CLAUDE.md grows by accretion in most repos, ending as a 1000+ line dump that nobody reads. Cap at 200 lines — overflow goes to dedicated docs (ADRs, PLAYBOOK sections), not back into this file.

corp-monorepo CLAUDE.md (4KB, stale numbers like "24 Council Decisions" when there are 29) is exactly the failure mode this template prevents. <!-- intentional stale example illustrating anti-pattern; do not "fix" -->

### LLMs advise; hooks/tests enforce
<!-- scope: meta -->

CLAUDE.md tells the LLM what to do/avoid. Tach, pre-commit hooks, pytest, Codex /review enforce mechanically. Don't put rules in CLAUDE.md that aren't backed by enforcement somewhere — they'll drift.

### Template
<!-- scope: meta -->

See `templates/CLAUDE-md-template.md` for the canonical 12-section skeleton (≤200 lines).

### Update cadence
<!-- scope: meta -->

CLAUDE.md updates when:
- New ADR is binding (Recent ADRs section §11)
- New slash command adopted (Slash commands section §7)
- New skill adopted or gotcha promoted (Skills section §8)
- New hook added (Hooks section §9)
- New slash command, skill, or hook added (§7, §8, or §9 as applicable)
- PLAYBOOK.md restructure (update First read section §1 paths)

**Architecture changes go in `ARCHITECTURE.md`** — CLAUDE.md §3 is a static pointer that needs no edit when architecture changes.

**Stale CLAUDE.md = agents operating on outdated context every session.** Treat updates as part of the change that triggered them.

### Length notes
<!-- scope: meta -->

CLAUDE.md length scales with repo complexity (advisory, not gated): a small repo may need only 50-100 lines (less infrastructure); a larger repo with rich tooling and more binding ADRs approaches but does not exceed the 200-line cap.

If CLAUDE.md grows past 200 lines, split content to dedicated docs; only per-repo governance stays here.

### Handoff scope
<!-- scope: meta -->

CLAUDE.md is an agent-instruction contract, not a repo-descriptive document. The Claude-oriented handoff process must not narrate, summarize, or manage CLAUDE.md as Claude-side repo-descriptive handoff content. See ADR-53.

---

## Repo conventions
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-26 -->

Universal repo-level conventions binding across all Rob's repos. Each subsection has its own ADR (ADR-30 through ADR-34). Subsections marked `[TBD]` document planned work — placeholders are forward-references, not documentation gaps. Concrete enforcement happens via Claude Code, Codex, hooks, and reviewer judgment; this section is the source of truth.

### Default branch — `main`
<!-- scope: dev -->
<!-- version: 1.0 — 2026-04-26 -->

**Rule:** Every Rob's repo uses `main` as the default branch. No exceptions. Per ADR-30.

**New repos:**
- `git init -b main`, or set `init.defaultBranch = main` in `~/.gitconfig` so `git init` always lands on `main`
- When creating on GitHub UI, default already correct

**Existing repos still on `master`:**

Procedure (Phase 1 = file changes on feature branch; Phase 2 = destructive remote ops):

Phase 1:
1. Grep entire repo for hardcoded `master` in CI workflows, hooks, scripts, docs. Update any found alongside the rename
2. Update any docs naming the default branch by name (e.g. JOURNAL entries; CHANGELOG retired ecosystem-wide per ADR-49)

Phase 2 (destructive — explicit confirm before each):
3. Local rename: `git branch -m master main`
4. Push `main`: `git push -u origin main`
5. Set remote HEAD: `git remote set-head origin main`
6. Delete origin/master: `git push origin --delete master`
7. GitHub repo Settings → Branches → default branch = `main` (manual UI step if step 5 didn't cover it)

**Anti-patterns:**
- Phase 2 without grep step from Phase 1 → CI breaks post-rename
- Renaming on remote without local rename first → divergent state
- Skipping the GitHub default branch UI update → next PRs target the deleted ref

### File naming conventions
<!-- scope: meta -->

Per ADR-34 (ratified 2026-04-29, amended 2026-05-11). Canonical source: `docs/decisions/ADR-34-file-naming-convention.md`. Key rules: hyphen separator universal across filenames and foldernames; `ADR-NN-topic.md` for decisions; `council-out-YYYYMMDD-HHMMSS-topic.md` for Council CLI output; `DECISION_NN_*` legacy transcripts grandfathered; kebab-case + ISO date for audits/handoffs; UPPERCASE for living docs.

### Folder structure
<!-- scope: meta -->

Which `docs/` subfolders a repo carries (`decisions/`, `handoffs/`, `audits/`, `research/`) is a judgment call by repo complexity, not a gated tier prescription (repo-tier system deprecated 2026-05-23). Add a subfolder when its content class first appears; do not pre-create empty scaffolding. The universal governance baseline (ADR-38 amendment A5) covers the mandatory root files; everything under `docs/` is optional and added on first need.

### Root hygiene convention
<!-- scope: dev -->
<!-- version: 1.0 — 2026-05-23 -->

**Goal:** keep the repo root visually clean (low cognitive overhead) without breaking tooling defaults.

**Consolidate tool configs into `pyproject.toml`** where supported, instead of standalone files at root:

- `[tool.ruff]` (instead of `ruff.toml`)
- `[tool.pytest.ini_options]` (instead of `pytest.ini`)
- `[tool.mypy]` (instead of `mypy.ini`)
- `[tool.tach]` if Tach supports pyproject embedding (verify per Tach version); else keep `tach.toml` at root

> Caveat: only consolidate when a `pyproject.toml` already exists or the repo is a code project. A governance-only repo with no `pyproject.toml` should NOT create one solely to absorb a single `ruff.toml` — that adds a root file rather than removing one, defeating the goal. In that case keep the standalone config.

**Dot-prefix workspace files:** rename `<repo>.code-workspace` to `.<repo>.code-workspace` — hides it from default `ls` while preserving VS Code "Open Workspace" functionality.

**Files that MUST remain at root** (tooling defaults; moving creates friction):

- `pyproject.toml`, `.gitignore`, `.gitattributes`, `.pre-commit-config.yaml`, `.editorconfig`, `.git/`

**Files that CAN move to subfolders:**

- SVGs and rendered diagrams → `docs/diagrams/` or `_assets/`
- Standalone scripts → `scripts/`
- Test fixtures → `tests/fixtures/`

### Additional root hygiene rules (added 2026-05-24, root hygiene pass 2)
<!-- scope: dev -->
<!-- version: 1.1 — 2026-05-24 -->

**`.env.example` policy: do not create.** Standard practice in many projects is generating `.env.example` as a template for required environment variables. In this repo's workflow, this is unnecessary clutter — environment variable docs live in CLAUDE.md / ENVIRONMENT.md / VISION.md as appropriate. Do not auto-generate `.env.example` files.

**Dot-prefix where tool supports.** If a config file MUST live at root (tool defaults to root discovery), prefer dot-prefixed variant if the tool accepts both:
- Ruff: `.ruff.toml` (instead of `ruff.toml`) — supported per Ruff docs ✓ applied 2026-05-24
- pre-commit: `.pre-commit-config.yaml` — standard name, already dot-prefixed
- ESLint: `.eslintrc.json` (instead of `eslintrc.json`) — already dot-prefixed convention
- pytest: must be `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]` — no dot-prefix variant
- Tach: `tach.toml` — verify movability per tool version before assuming dot-prefix works

**`.env` placement.** If `.env` is required by tooling: stays at repo root (dot-prefixed convention preserved). If only used by scripts that accept configurable env-file path: prefer `.config/.env` or similar subfolder placement.

**No `files.exclude` to hide root config files.** Operator preference: VISIBILITY of what tools are configured matters. Do not use VS Code `files.exclude` settings to hide config files from Explorer — defeats the purpose of seeing what's configured. Apply dot-prefix instead where supported.

### Universal visual pattern (per ADR-59)
<!-- scope: dev -->
<!-- version: 1.0 — 2026-05-27 -->

Every repo root follows the ADR-59 universal visual pattern (read the ADR for the full standard). Three pillars, all audit-enforced via `scripts/audit.py`:

- **Dot-prefix discipline** — dot-prefix every root config the tool supports a dotted variant for (`.ruff.toml`, `.pre-commit-config.yaml`, `.{repo}.code-workspace`, standard dotfiles). Exceptions that MUST stay un-dotted (tool requires the exact name / ecosystem convention): `pyproject.toml`, `package.json`, `Cargo.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `Dockerfile`, `Makefile`, `LICENSE`, `tach.toml`, `README.md`.
- **ALL-CAPS canonical `.md` at root** — `VISION`/`CLAUDE`/`ARCHITECTURE`/`BACKLOG` mandatory everywhere; `JOURNAL`/`ENVIRONMENT`/`CONTRIBUTING` optional; `LESSONS`/`PLAYBOOK`/`ESSENTIALS`/`TOKEN-LOG` are `.dev-knowledge`-only (never required in a child repo).
- **Workspace sort settings** — `.{repo}.code-workspace` with `"explorer.sortOrder": "default"` + `"explorer.sortOrderLexicographicOptions": "upper"`. `upper` (not `default`) is what clusters ALL-CAPS files ahead of lowercase configs — verified 2026-05-27.

**Maintenance rule (adopting a new tool config):**
1. Check the tool's docs — or test empirically (as was done for `tach`: `.tach.toml` is NOT discovered by tach 0.34.0) — for dot-prefix support.
2. Supported → use the dotted name. Not supported → add the exact name to the ADR-59 exception list **and** the `scripts/audit.py` exception constant, and note it in the commit.
3. The exception list is the single source of truth, mirrored in the audit tool. `audit.py health` surfaces drift.

**Date-sorted folders** (`docs/audits/`, `docs/handoffs/`, transcripts): ISO `YYYY-MM-DD-` prefix only. VS Code has no native per-folder reverse sort (`explorer.sortOrderReverse` is not a real setting); dated content stays ascending. Navigate via scroll-to-bottom, `Ctrl+P`, or the workspace `open-latest-*` tasks.

### docs/ folder taxonomy (per ADR-60)
<!-- scope: meta -->
<!-- version: 1.0 — 2026-05-27 -->

Where ADR-59 makes every repo *look* the same, ADR-60 makes `.dev-knowledge`'s `docs/` *mean* the same: each subfolder serves **one** semantic role, so a file's location tells you what it is.

| Folder | Role | Contents |
|--------|------|----------|
| `audits/` | OUTPUTS | Audit reports, validation reports, refresh docs, forensics |
| `council-questions/` | INPUTS | Council debate question sets, evidence, set indexes |
| `decisions/` | OUTPUTS | ADRs + `transcripts/` (routed per ADR-43) |
| `handoffs/` | OUTPUTS | Per-session handoff bundles |
| `research/` | WORKING | Exploratory pre-decision scratchpad |
| `archive/` | ARCHIVED | Superseded, dormant, transient (incl. archived `tech-radar/`) |

**File lifecycle (always `git mv` — preserve history):**
- Exploratory work starts in `research/`; matures to `audits/` (finished audit) or `decisions/` (ADR).
- Council debate inputs land in `council-questions/`; transcripts route to `decisions/transcripts/`.
- Dormant/superseded → `archive/`.

**On moving a file, do NOT rewrite append-only or immutable records that reference it** — ADRs, transcripts, handoffs, and existing `JOURNAL.md`/`LESSONS.md` entries are point-in-time history (critical rules #2/#3). Update only living docs (BACKLOG, PLAYBOOK, HANDOFF_PROCESS, READMEs) and the moved file's own internal cross-refs. Date-prefixed naming (`YYYY-MM-DD-{slug}.md`) for time-sequenced artifacts.

### Secrets storage path
<!-- scope: meta -->

**[TBD — Stream C session 3, ADR-33]**

Standardize location of `.secrets/` (currently `C:\Users\1028120\Documents\.secrets\.env` per Rob's environment, not yet PLAYBOOK-documented as standard). Rule covers: path convention, what kinds of repos use this, whether per-repo `.env` is allowed, how the global PowerShell profile auto-loads relate.

### Capitalization conventions
<!-- scope: meta -->

**[TBD — Stream C session 3, ADR-34]**

File and folder casing rules. Currently mixed: `LESSONS.md` ALLCAPS, `docs/` lowercase, `ESSENTIALS.md` ALLCAPS, kebab-case for dated files. Decision on what casing applies where, and whether existing files migrate.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-26) — initial. Default branch subsection filled per ADR-30. Subsections 2–5 reserved as forward-references to ADR-31 through ADR-34, populated in Stream C sessions 2, 3, and Cluster 2.

---

## Writing prompts for Claude Code
<!-- scope: meta -->

**Purpose:** Standardize prompts that browser chat produces for Claude Code execution. Per ADR-28 (three-layer architecture): browser is architect, Claude Code is executor — prompts are the contract between them.

### Why standard format
<!-- scope: meta -->

Without standard structure, prompts diverge:
- Different naming for same fields (Model vs LLM, Effort vs Difficulty)
- Inconsistent COMMIT markers — Claude Code can't tell when to commit
- Missing UNDERSTAND section → Claude Code makes wrong assumptions
- Polish prompts → Claude Code outputs Polish (per ESSENTIALS line 25, prompts are English-only)
- Inline code blocks → can't be saved as artifact, breaks asynchronous workflow

Vibe Code 4 (2026-04-22) established the standard structure during Stream A. This section codifies it as PLAYBOOK protocol.

### Standard structure (8 sections)
<!-- scope: meta -->

1. **Model/Mode/Effort table** — `| Model | Sonnet | / | Mode | plan-then-auto | / | Effort | medium |`
2. **Title** (imperative, what gets accomplished)
3. **Repo + Purpose** (absolute path + one-sentence outcome)
4. **Read first** (CLAUDE.md, gotchas, relevant docs)
5. **Git workflow** (branch + commit cadence + merge command)
6. **UNDERSTAND** (problem, what could break, most likely failure mode)
7. **Steps with COMMIT markers** (numbered, each ends with conventional commit message)
8. **Final + What NOT to do** (verification + merge + anti-patterns)

Template: `templates/prompt-template.md`

### Per-Scale guidance
<!-- scope: meta -->

- **Scale S** (single file, <50 lines change): use minimal version — Title + Steps + What NOT to do. Skip UNDERSTAND if change is mechanical.
- **Scale M** (multi-file): full template, but UNDERSTAND can be 1-2 sentences.
- **Scale L** (3+ files, architectural): full template required, prefer `plan-then-auto` mode for review checkpoint after Step 1.

### Delivery format
<!-- scope: meta -->

Prompts are **downloadable `.md` artifacts**, not inline code blocks. Browser chat outputs them as fenced markdown blocks; Rob saves as file, then pastes file content into Claude Code's prompt field.

Why: pasted-as-text is fine, but file form preserves structure for re-use, audit, and handoff.

### Pre-send checklist
<!-- scope: meta -->

Before delivering a prompt to Claude Code, verify:

- [ ] **English only** — no Polish in prompt body (Rob speaks Polish; prompts are English per ESSENTIALS)
- [ ] **Model/Mode/Effort table** present at top
- [ ] **Absolute paths** for all repo/file references (not relative — Claude Code's CWD varies)
- [ ] **Read first** lists CLAUDE.md and gotchas (always) plus task-relevant docs
- [ ] **Git workflow** specifies branch name, commit cadence, merge command
- [ ] **UNDERSTAND section** answers: what's the problem? what could break? most likely failure mode?
- [ ] **Steps numbered** with imperative titles ("Create X" not "Creating X")
- [ ] **COMMIT markers** end each step (or explicit "no commit" if grouping)
- [ ] **What NOT to do** lists at least 3 anti-patterns specific to this task
- [ ] **Final** has concrete verification commands and merge command
- [ ] **Out-of-scope items explicit** (e.g., "Do NOT touch corp-monorepo")
- [ ] **No `!` shortcuts** for state-changing git operations (per Vibe Code 4 protocol)
- [ ] **Versioning if applicable** — sections in repo files include `<!-- version: X.Y -->` for amendment tracking

Skip checklist items only when not applicable to specific task type. If unsure, include them.

### Anti-patterns
<!-- scope: meta -->

- **Polish prompts** — even if Rob asks in Polish, prompt body is English
- **Inline `!` git commits** — Claude Code commits via explicit Bash steps, not shortcuts
- **Missing UNDERSTAND** — Claude Code without context makes wrong assumptions, especially on Scale L
- **Unclear out-of-scope** — Claude Code expands work; explicit "Do NOT touch X" prevents
- **Relative paths** — break when CWD shifts between repos

### Update cadence
<!-- scope: meta -->

Prompt format updates when:
- New common failure mode discovered → add to "What could break" guidance
- New repo with different conventions → may require template variant
- ADR amendment changes prompt protocol (e.g., new git workflow standard)

This section's history is in PLAYBOOK CHANGELOG entries (search for "prompt template" or "Gap #2").

---

## Project complexity bands
<!-- scope: dev -->

> **Repo-tier system DEPRECATED 2026-05-23.** The formal S/M/L tier system — a declared `tier:`/`scale:` per repo that gated governance baselines — is deprecated ecosystem-wide (operator decision 2026-05-23; see ADR-33 amendment, ADR-38 amendment A5, ADR-40 deprecation). Repos no longer **declare** a tier, and no governance obligation is gated on one. The universal governance baseline (ADR-38 A5) applies to every repo regardless of size.

The S/M/L labels below survive only as **informal complexity descriptors** — shorthand for "how big is this repo" used to calibrate judgment (how much test infrastructure, how rich a workspace), not as a declared, audited tier:

- **large** — multi-package repo, hundreds+ of tests, cross-package dependencies.
- **medium** — standalone package, dozens-to-hundreds of tests, multiple modules.
- **small** — single script or tool, few tests, simple flow.

These are bands on a continuum, applied by judgment. Guidance below that references them is advisory calibration, not a tier mandate. (Distinct from the *task-complexity* S/M/L sizing used to size Claude Code prompts in `templates/prompt-template.md` — that taxonomy is unaffected by this deprecation.)

### Testing rules (scaled by repo complexity)
<!-- scope: dev -->
<!-- version: 1.1 — 2026-05-23 -->

Test infrastructure scales with project size. Over-investing in test infra on a tiny single-script repo wastes effort; under-investing on a large repo creates fragility. The bands below are advisory calibration (per the complexity descriptors above), not tier mandates.

| Repo size | Minimum | Coverage target | Test types | Run command |
|-------|---------|-----------------|------------|-------------|
| **small** (<50 tests) | optional | n/a — coverage measurement overhead exceeds value | smoke tests at most | `pytest` (single run) |
| **medium** (50-500 tests) | required | ≥60% on source, no untested public API | pytest unit + selective integration | `pytest -x --tb=short` |
| **large** (500+ tests) | required | ≥80% on source, comprehensive public API coverage, integration suite for critical paths | pytest unit + integration + e2e where applicable | `pytest -x --tb=short` per step + `pytest --collect-only` for sanity |

> Coverage targets (60%/80%) are guidelines from observed practice, not enforced thresholds. See Section history note for basis.

#### Reading the table
<!-- scope: dev -->

- **required** — tests must exist and pass before merge; CI/CD enforces
- **optional** — tests welcomed but not blocking; useful when complexity warrants
- **n/a** — measurement overhead exceeds practical value at this scale

#### Per-step test cadence (any repo with a test suite)
<!-- scope: dev -->

Per `templates/prompt-template.md` and PLAYBOOK "Writing prompts for Claude Code" section:

After every numbered step in a Claude Code prompt:
1. `pytest -x --tb=short` — fail fast, short tracebacks
2. `ruff check src/ tests/ --fix` — autofix lint issues
3. `git status` — verify expected file scope

This cadence catches regressions early and keeps each commit's diff sane to review.

#### Test types and when
<!-- scope: dev -->

- **Unit tests:** any repo with non-trivial logic. Mock external dependencies. Fast feedback (<10s per file).
- **Integration tests:** for critical paths on larger repos (e.g. data pipeline, auth flow). Real dependencies, isolated DB, slower (1-30s per test).
- **E2E tests:** for top user journeys on larger repos. Real environment, optional in standard CI (run nightly or pre-release).
- **Smoke tests:** minimum bar for a small repo — "did basic flow break?" Single-file pytest, optional CI.

#### Anti-patterns
<!-- scope: dev -->

- **Coverage chasing on a tiny repo** — measuring coverage on a <50-test repo wastes 30+ min per session for diminishing return
- **Skipping tests on a large repo** — "this commit is small" + large repo = recipe for hidden regression
- **Integration-only on a large repo** — slow feedback discourages running tests; unit tests are the foundation

#### Section history
<!-- scope: dev -->

- v1.0 (2026-04-25) — initial. Coverage targets are guidelines, not enforced thresholds.

### VS Code workspace
<!-- scope: dev -->
<!-- version: 1.1 — 2026-05-23 -->

Each repo has a `.code-workspace` file at root that VS Code uses for project-specific settings and recommended extensions. Three templates of increasing richness ensure baseline consistency without preventing repo-specific customization — pick the one matching the repo's complexity (the S/M/L suffixes are richness levels, not declared tiers).

**Templates location:** `.dev-knowledge/templates/workspace-{S,M,L}.code-workspace`

**Bootstrap workflow:**
1. Copy the template matching repo complexity: `cp .dev-knowledge/templates/workspace-S.code-workspace <repo>/<repo-name>.code-workspace`
2. Rename to match repo name (e.g. `corp-monorepo.code-workspace`)
3. Edit `folders` array if multi-folder workspace needed (rare)
4. Add repo-specific settings/extensions on top of template baseline
5. Commit `.code-workspace` to repo root (yes, commit it — workspace config is part of dev environment)

#### Minimal (small repos)
<!-- scope: dev -->

For small repos (<50 tests, single script/tool, simple flow):

**Settings:**
- Python interpreter via `.venv/`
- Ruff format-on-save with import organization
- Trailing whitespace cleanup, final newline
- Editor rulers at 88 (Ruff default) and 120

**Extensions:**
- ms-python.python — Python language support
- charliermarsh.ruff — linter + formatter

That's it. No testing infra, no git tooling, no diagram support — a small repo doesn't need them.

#### + testing & git tooling (medium repos)
<!-- scope: dev -->

For medium repos (50-500 tests, standalone package, multiple modules):

**Adds to the minimal set:**
- pytest test discovery (`python.testing.pytestEnabled`)
- GitLens (eamodio.gitlens) — git history, blame
- Error Lens (usernamehw.errorlens) — inline diagnostics
- TODO Tree (gruntfuggly.todo-tree) — surfaces TODO/FIXME comments

**Why these:** on a medium repo, test infrastructure is worthwhile (per Testing rules subsection above), and git/error tooling becomes worth setup cost.

#### Full stack (large repos)
<!-- scope: dev -->

For large repos (500+ tests, multi-package monorepo):

**Adds to the medium set:**
- mypy type checking (`python.analysis.typeCheckingMode: "basic"`)
- mypy type checker extension (ms-python.mypy-type-checker)
- TOML support (tamasfe.even-better-toml) — for tach.toml, pyproject.toml, etc.
- Spell checker (streetsidesoftware.code-spell-checker)
- Mermaid diagram preview (bierner.markdown-mermaid)
- TODO Tree extended tag list

**Real example:** `corp-monorepo.code-workspace` (a large repo, currently active) reflects this template with corp-monorepo-specific additions.

**Why these:** on a large repo, architecture diagrams (Mermaid) and type discipline (mypy) become high-leverage. TOML editing matters for Tach, pyproject.toml monorepo-wide configs.

#### Customization
<!-- scope: dev -->

Template is starting point, not contract. Repos may:
- Add project-specific extensions (e.g. corp-monorepo adds Tach extension if available)
- Tighten settings (e.g. require strict type checking instead of basic)
- Override interpreter path for non-standard venv locations
- Add custom tasks, debug configurations, multi-folder workspaces

**Don't:** remove template baseline without rationale — that's diverging from baseline, not customizing on top of it.

#### Section history
<!-- scope: dev -->

- v1.0 (2026-04-25) — initial. Three richness-tiered templates grounded in `corp-monorepo.code-workspace` actual contents. Will refine based on extension marketplace evolution.
- v1.1 (2026-05-23) — de-tiered: S/M/L reframed as richness levels (repo-tier system deprecated).

### Tier transition procedures (ADR-40) — DEPRECATED 2026-05-23
<!-- scope: meta -->

> **Obsolete.** This subsection described tier-upgrade procedures (S→M→L) keyed
> to ADR-40's Composite Tier Score. ADR-40 is deprecated (2026-05-23) and the
> tier system is removed ecosystem-wide. There is no tier to transition between
> and no score is computed. The universal governance baseline (ADR-38 amendment
> A5) applies to every repo from the start — there are no tier-gated obligations
> to acquire on growth. Retained as a marker so the removed procedures are not
> silently re-introduced.
>
> Cross-refs: ADR-40 (deprecated), ADR-33 amendment, ADR-38 amendment A5, ADR-36 (audit tool — Section 18).

---

## Documentation file types and session continuity
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

Two related questions: **what does each documentation file do** (Gap #4) and **which files a repo carries** (Gap #18; file presence is now universal, not tier-gated — see below). Combined here because they answer "when I need to write something down, where does it go?"

### File type taxonomy
<!-- scope: meta -->

| File | Purpose | Format | Cadence | Audience | Order | Scope |
|------|---------|--------|---------|----------|-------|-------|
| `README.md` | User-first navigation, what is this repo | Prose + folder layout | When repo state shifts notably | Rob, future contributors | Living (rewrite) | Per-repo |
| `CLAUDE.md` | Single canonical agent-instruction contract for Claude Code + Codex; per-repo specifics (architecture, conventions, active tools, binding ADRs, anti-patterns) ≤200 lines | 10-section template | When ADRs, tools, architecture, or gotchas change | Claude Code (auto-read), Codex (via project_doc_fallback_filenames) | Living (sections updated) | Per-repo |
| `ESSENTIALS.md` | Rob's daily cheat sheet, universal | Sectioned, scope-tagged | When Rob's working style evolves | Rob + every browser/Claude Code session | Living (sections updated) | Universal (`.dev-knowledge` only) |
| `PLAYBOOK.md` | Universal protocols, this file | Sectioned, scope-tagged, versioned | Per Stream B implementation gaps | Rob + Claude (browser + Code) | Living + section history | Universal (`.dev-knowledge` only) |
| `JOURNAL.md` | Tactical per-session log | Append-only, dated entries: Did/Failed/Next | Every Claude Code session | Future Claude Code (last 5 entries on startup) | Newest-first prepend | Per-repo (optional; kept when a repo benefits from a per-session log) |
| `CHANGELOG.md` | RETIRED ecosystem-wide (ADR-49) — git history + JOURNAL `Changes:` line replace it; row kept for legacy context | Newest-first dated entries | n/a | — | n/a | Removed |
| `LESSONS.md` | Process lessons learned | Append-only with `[scope: X]` inline (per ADR-29) | When new lesson emerges (auto-promote at 2× repeat) | Rob, future Claude | Append-only | Universal (`.dev-knowledge` only) |
| `TOKEN-LOG.md` | Claude usage snapshots | Threshold-triggered (7-day) via /session-summary | Auto when stale | Rob | Newest-first (prepend) | Universal (`.dev-knowledge` only) |
| `ENVIRONMENT.md` | Tooling state, what's installed | Sectioned, scope-tagged | When tool adopted/deprecated | Rob, Claude Code | Living (sections updated) | Per-repo |
| `docs/decisions/ADR-NN-*.md` | Architectural decisions | Michael Nygard format | When decision binds | Rob, future contributors | Numbered, immutable (amend in-place per ADR-29) | Per-repo |
| `docs/decisions/transcripts/DECISION_NN_*.md` | Raw Council debate outputs | Multi-model debate transcript | When Council debate concludes (per PLAYBOOK 5.N archival) | Reference for ADR rationale | Numbered, immutable | Per-repo |
| `docs/handoffs/YYYY-MM-DD-*.md` (legacy) or `docs/handoffs/YYYY-MM-DD-*/` (folder, since 2026-04-27) | Chat-to-chat session summary | Single-file legacy OR folder-format (upload-instructions + first-message + contents/) | When session boundary requires continuity | Next browser chat | Dated, immutable | Per-repo |
| `docs/audits/YYYY-MM-DD-*.md` | Point-in-time analyses | Free-form audit | When deep analysis needed | Reference for follow-up work | Dated, immutable (mark SUPERSEDED if redone) | Per-repo |
| `docs/research/YYYY-MM-DD-*.md` | Research outputs (Council research mode, standalone reports) | Free-form research | When research generates value | Reference for design decisions | Dated, immutable | Universal (`.dev-knowledge` only — research is methodology) |

### File presence (universal baseline)
<!-- scope: meta -->

File presence is no longer gated per tier (repo-tier system deprecated 2026-05-23). The universal governance baseline (ADR-38 amendment A5) applies to every repo regardless of size:

| File | Status |
|------|--------|
| `VISION.md` | mandatory (ADR-33, amended frontmatter) |
| `CLAUDE.md` | mandatory (ADR-31 / ADR-53) |
| `ARCHITECTURE.md` | mandatory (ADR-51 amended 2026-05-23; root placement per ADR-38 A3) |
| `BACKLOG.md` | mandatory (ADR-41) |
| `README.md` | optional — external-audience repos only (deprecated from baseline) |
| `CHANGELOG.md` | removed — superseded by ADR-49 |
| `JOURNAL.md` | optional — kept when a per-session log helps |
| `ENVIRONMENT.md` | optional — kept when tooling state is worth tracking |
| `docs/decisions/`, `docs/handoffs/`, `docs/audits/`, `docs/research/` | optional — added on first need (see Folder structure above) |
| `ESSENTIALS.md`, `PLAYBOOK.md`, `LESSONS.md`, `TOKEN-LOG.md` | n/a per-repo — live in `.dev-knowledge` only |

Optional files are added by judgment of repo complexity; no tier makes them mandatory.

### Common confusions resolved
<!-- scope: meta -->

**JOURNAL vs handoff:**
- JOURNAL = within-repo, per-session tactical log. Continuity across Claude Code sessions in same repo.
- handoff = across-context, browser-chat-to-browser-chat session summary. Continuity when switching chats.
- Both can coexist. Larger repos typically use both; smaller repos usually one or the other (often handoffs).

**LESSONS vs ADR:**
- LESSONS = process lessons (how Rob works, anti-patterns, what tooling drift looked like). Append-only.
- ADR = architectural decisions (technical commitments). Amendable per ADR-29 pattern.
- Process generalization → LESSONS. Technical commitment → ADR.

**CHANGELOG vs JOURNAL:**
- CHANGELOG = strategic, what user/contributor needs to know about repo evolution. Newest-first.
- JOURNAL = tactical, what Claude Code did session-by-session. Append-only, newest-first prepend (amended 2026-04-27 from oldest-top per Rob's preference; matches TOKEN-LOG/CHANGELOG convention).
- Same commit might warrant entries in both — different abstraction levels.

**audits vs research:**
- audits = backward-looking analysis of current state (per-repo, dated)
- research = forward-looking exploration (universal in `.dev-knowledge`, dated)
- Council research-mode debates → research/. Council pick-mode debates → transcripts/.

### Supersession & decommissioning
<!-- scope: meta -->

Decisions are additive by default — they describe the new state, not the
teardown of the old. This is how orphans accumulate: a structure is relocated
or replaced, the new location is recorded, the old one is left behind and
forgotten. A presence-checking audit will never catch it.

Rule: any decision — ADR or decision-note — that relocates, replaces, or
centralizes an artifact MUST name what becomes obsolete in a `Decommission:`
field. A non-empty `Decommission:` field becomes a BACKLOG item and stays open
until the obsolete artifact is removed.

The decommission action is part of the decision, not an optional follow-up. A
decision that supersedes something is not complete until its `Decommission:`
items are removed or tracked in BACKLOG.

### Handoff format spec (since 2026-04-27)
<!-- scope: meta -->

Two formats coexist in `docs/handoffs/`:

**Legacy (before 2026-04-27)** — single `.md` file, dated `YYYY-MM-DD-slug.md`. Content: free-form session summary. Preserved as-is — do not migrate.

**New (since 2026-04-27, per Topic 2 + Research synthesis)** — folder per session:

```
docs/handoffs/{date}-{slug}/
├── upload-instructions.md   (top — drag-drop guidance)
├── first-message.md         (top — paste verbatim into new browser chat)
└── contents/                (single drag-drop target)
    ├── HANDOFF.md           (session state — decisions, pending, references)
    ├── manifest.json        (context orchestration: layers, reading order, refs)
    ├── tree.txt             (repo structure snapshot for browser orientation)
    ├── ESSENTIALS.md        (point-in-time copy)
    ├── PLAYBOOK.md          (point-in-time copy)
    ├── JOURNAL.md           (point-in-time copy)
    └── CLAUDE.md            (point-in-time copy)
```

**When to use new format:** session boundaries with substantive state to preserve (decisions, pending work, cross-stream context). Default to new format for Stream-level handoffs.

**When legacy still acceptable:** quick single-session summary with no need for point-in-time copies (rare since cleanup).

**Validator interaction:** `contents/*.md` files under `docs/handoffs/` are excluded from pre-commit scope checks — no duplicate-tag concerns.

**First instance:** `docs/handoffs/2026-04-27-stream-c-session-1-final/` — Stream C session 1 close.

**Rationale:** point-in-time copies prevent drift between session intent and live state at resume time. Manifest + tree.txt give browser deterministic upload index + structural orientation. No repo-root `HANDOFF.md` (per Topic 2 decision: source of truth lives in session folder, not at root).

### Order conventions
<!-- scope: meta -->

Per Token-LOG flip 2026-04-24:

- **Newest-first (prepend):** TOKEN-LOG, CHANGELOG, JOURNAL. Rationale: logs optimize for current-state scanning. (JOURNAL flipped 2026-04-27 — original Stream B Gap #4 spec had oldest-top; amended for consistency with TOKEN-LOG/CHANGELOG.)
- **Append-only (oldest top):** LESSONS. Rationale: chronological narrative for grandfathered learning patterns; order preserves "what we learned when" per ADR-29.
- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT. Rationale: not logs; current state matters more than history.
- **Immutable (dated):** ADRs, transcripts, handoffs, audits, research. Rationale: point-in-time records; supersession via new file or in-file marker.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial. 12-file taxonomy + Scale matrix + 4 common confusions + order conventions. Will refine after live use.
- v1.1 (2026-05-23) — Scale matrix replaced by universal file-presence baseline (repo-tier system deprecated; ADR-38 amendment A5).
- v1.1 (2026-04-27) — JOURNAL ordering amended oldest-top → newest-first prepend per Rob's preference; aligns with TOKEN-LOG/CHANGELOG. LESSONS retains oldest-top (ADR-29 grandfathering). Light-touch amendment, no ADR.
- v1.2 (2026-04-27) — Handoff format spec added: folder-format introduced (since 2026-04-27) per Topic 2 + Research synthesis. Legacy single-file format preserved. File taxonomy row updated to reflect both formats. First folder-format instance: `docs/handoffs/2026-04-27-stream-c-session-1-final/`.

---

## Session boundaries
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

Browser chats and Claude Code sessions have natural quality limits. Pushing past them produces decisions that look fine in the moment but read poorly the next day. This section codifies recognition signals and stop-protocols.

### Scope declaration at start
<!-- scope: meta -->

Every session opens with explicit scope. If Rob doesn't state it, browser chat asks before proceeding.

**Format (one sentence each):**
- **In scope:** what this session aims to accomplish
- **Out of scope:** what this session deliberately defers
- **Success criterion:** what makes the session "done" (commit merged? decision documented? specific artifact produced?)

**Why explicit:** without scope declaration, every passing thought becomes a candidate detour. Scope is the contract for "is this proposal in scope or scope creep?"

**Example (good):**
> In scope: implement Gap #13 in PLAYBOOK. Out of scope: per-repo PLAYBOOK rollout, other gaps. Success: new section merged with v1.0 marker.

**Example (bad):**
> Let's work on .dev-knowledge today. (No scope = unbounded session = guaranteed creep)

### Stop-signs (recognize and act)
<!-- scope: meta -->

These signals indicate a session should stop or refocus, NOT push through:

- **Decision fatigue:** >3 hours active session AND >3 architectural decisions made. Each subsequent decision is statistically lower quality.
- **Recursive planning** (anti-pattern, see below) — three consecutive turns producing plans/audits/specs without execution
- **Scope creep accumulation:** more than 2 "while we're at it" expansions in one session — even if individually small
- **Re-explanation loops:** Rob explaining the same protocol/context to Claude more than once in a session — signal that earlier context is gone or wasn't applied
- **"Just one more thing"** at end of natural stopping point — usually the wrong call; the next thing deserves fresh start
- **Quality regression:** finding errors in prompts/decisions that wouldn't have happened earlier in session

When stop-sign appears, ACTION:
1. Generate handoff (per HANDOFF_PROCESS.md)
2. Identify the specific stop-sign that triggered (helpful for next session retrospective)
3. Stop. Resume with fresh head.

### Decision fatigue threshold
<!-- scope: meta -->

**Numeric guideline:** >3h elapsed + >3 architectural decisions made = wrap-up zone.

This isn't a hard limit. Session may legitimately need to push past it (e.g., critical fix, time-bound deliverable). But entering wrap-up zone shifts default from "continue" to "wrap up unless reason to continue."

**Why these numbers:** observed empirically from 2026-04-24 session. Quality of decisions visibly degraded after these thresholds — including by the "decider's" own self-assessment in retrospect.

**Counter-indicator:** if session is execution-heavy (running prompts, watching Claude Code commit) rather than decision-heavy, threshold is generous. The fatigue is decision-specific, not pure clock time.

### Recursive planning anti-pattern
<!-- scope: meta -->

**Detection:** session produces plans/audits/specs about plans/audits/specs without producing any actual artifact change.

**In-vivo example (2026-04-24):** during Stream A→B transition, browser chat repeatedly proposed:
- "Let's audit what we have"
- "Let's audit again with mapping"
- "Let's create reference doc for the gaps"
- "Let's plan the implementation order"

While useful for some context, this stacked 4 layers of meta-work before any gap was implemented. Pattern only broke when Rob explicitly said "implementacja, nie planowanie" — and even then, it took conscious resistance.

**Symptoms:**
- Proposing "audit" when implementation is the next logical step
- Proposing "plan" when a plan already exists
- Proposing "framework" or "specification" before MVP attempt exists
- Each output describes what to do, not what was done

**Counter-protocol:**
- After 2 consecutive planning/audit outputs, FORCE next output to be implementation prompt
- If implementation feels too risky → spike (4h throwaway branch) instead of more planning
- Watch for rationalizing: "we need to audit because..." Almost always: we don't.

### Session resumption protocol
<!-- scope: meta -->

When opening a new session that continues prior work:

**Browser chat resumption:**
1. Upload `ESSENTIALS.md` (always)
2. Upload most recent `docs/handoffs/*.md` (if any)
3. Upload PLAYBOOK.md (if doing dev work — large file, but contains all protocols)
4. Upload task-specific docs (specific ADRs, Stream B mapping if continuing Stream B, etc.)
5. First message states: scope (in/out), success criterion, what was last session's stopping point

**Claude Code resumption:**
1. Read CLAUDE.md (auto on session start)
2. `git status` and `git log --oneline -5`
3. Read most recent handoff if exists
4. Read JOURNAL.md last 5 entries (if the repo keeps one)
5. Wait for prompt — never improvise

**Anti-pattern:** opening new session with bare prompt "continue what we were doing" — without uploading context, both sides reconstruct from memory (browser) or scratch (Claude Code). Quality drops fast.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — initial. 5 subsections: scope declaration, stop-signs, decision fatigue threshold, recursive planning anti-pattern, session resumption protocol. Codifies patterns observed in 2026-04-24 sessions. Will refine after live use.

---

## Continuous Improvement
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

New tools, models, agents, and patterns emerge constantly in 2025-2026 LLM dev (Claude Code releases, OpenAI Codex updates, Chinese models like GLM/Qwen, MCP servers, multi-agent frameworks, Spec Kit/Kiro). Without explicit process, adoption thrashes (re-evaluating same tool quarterly), forgets context (why did we reject MCP memory?), or misses signals (relevant tool sat in tech-radar chat unread for weeks).

This section defines the lifecycle: from "I saw something on Twitter" to "we adopted/rejected/deferred."

### Pipeline overview
<!-- scope: meta -->

Six stages, executed in order. Stages can be implicit (skipped/quick) for low-stakes evaluations; explicit (full ceremony) for high-stakes ones.

```
Discovery → Triage → Evaluation → Decision → Implementation → Review
```

- **Discovery:** something new shows up
- **Triage:** is it worth evaluating?
- **Evaluation:** does it actually solve our problem?
- **Decision:** adopt / reject / defer
- **Implementation:** if adopt — execute via standard pipeline (ADR + work)
- **Review:** periodic re-check that adopted things still earn their keep

### Stage 1: Discovery
<!-- scope: meta -->

**Sources to monitor:**
- Anthropic engineering blog
- OpenAI engineering blog (for Codex / GPT-5.x)
- Karpathy (Twitter)
- Simon Willison (blog)
- Latent Space podcast / blog
- Cursor / Aider / Claude Code release notes
- agents.md / Spec Kit / Kiro initiatives
- Chinese model releases (GLM, Qwen, DeepSeek)

**Cadence:** weekly informal scan. No formal time box.

**Capture:** when something looks interesting, drop a one-liner into the next quarterly tech-radar entry under "discovered, not yet triaged" — don't wait for full evaluation.

### Stage 2: Triage
<!-- scope: meta -->

**Criteria for "worth evaluating":**
- **Maturity:** v1.0+, ≥100 GitHub stars, or backed by recognized org
- **Addresses real problem:** maps to existing Rob pain point or unblocks identified gap
- **Scale fit:** works for solo developer (not team-only)
- **Platform fit:** runs on Windows/PowerShell (or has portable equivalent)
- **Cost-bounded:** trial cost <$50 OR API trial available

If 4+ criteria met → proceed to Evaluation (majority-of-6 threshold; ≤3 = not worth evaluation cost). If 3 or fewer → mark "deferred" with reason in tech-radar.

**Anti-pattern:** evaluating every novelty. The job of triage is saying no.

### Stage 3: Evaluation
<!-- scope: meta -->

Three evaluation modes — pick by stakes:

**Quick check (Scale S decision):**
- Browser chat reads docs / community feedback
- ~30 min reading + thinking
- Output: yes/no/defer with one-paragraph rationale

**Spike (Scale M decision):**
- Throwaway branch, install tool, attempt real task
- ≤4 hours
- Output: works/fails/uncertain with concrete observation

**Research debate (Scale L decision):**
- AI Council research-mode debate (4 models, 1-2 rounds, ~$0.30-$0.50)
- 30-60 min from brief to synthesis
- Output: archived to `docs/research/YYYY-MM-DD-{topic}.md` per PLAYBOOK 5.N

Decision threshold for which mode: per PLAYBOOK Section 5 "When to run Council vs single-model + critic."

### Stage 4: Decision
<!-- scope: meta -->

Three outcomes:

- **Adopt:** triggers Implementation (Stage 5)
- **Reject:** record in tech-radar with reason; closed unless evidence changes
- **Defer:** record in tech-radar with explicit reopen trigger (e.g., "if cost drops below X" or "after solo→team transition")

**Document the decision:** even rejection deserves a paragraph. Future self asks "why didn't we adopt MCP memory?" — answer must exist.

### Stage 5: Implementation (only for "Adopt")
<!-- scope: meta -->

Standard pipeline:
1. **ADR if architectural impact** (per Section 5 gating) — module boundaries, dependencies, data model
2. **Brief Stream B-style gap entry** if it requires multiple changes across files
3. **Updates to:** CLAUDE.md (Slash commands §7, Skills §8, or Hooks §9 as applicable), ENVIRONMENT.md (if env-level), JOURNAL entries
4. **Hooks/tests/CI** if enforcement needed (LLMs advise; mechanism enforces, per Council #28)

Cross-link from tech-radar entry to the ADR + implementation commits.

### Stage 6: Review (periodic)
<!-- scope: meta -->

**Cadence:** quarterly tech-radar snapshot (`docs/tech-radar/YYYY-Q.md`).

**Per quarter, for each Adopted item:**
- Still earning its keep? (concrete value vs cost/maintenance)
- Configuration drift? (deprecated flags, version skew)
- Replacement candidate emerged?

**Per quarter, for each Deferred item:**
- Reopen trigger met?
- Still relevant or made obsolete by adoption of alternative?

**Per quarter, for each Rejected item:**
- Re-check if rejected for "wrong reason at the time" (rare but happens)

**Output:** updated tech-radar quarterly entry. NOT each time something changes — quarterly batch keeps cost down.

### Tech radar folder
<!-- scope: meta -->

Location: `docs/tech-radar/`

**File pattern:** `YYYY-Q.md` for quarterly snapshots; `YYYY-MM-DD-{tool}.md` for per-tool deep-dives when warranted (e.g. Spec Kit eval).

**Distinct from `docs/research/`:**
- `docs/research/` — research-mode debate outputs (point-in-time, rich content)
- `docs/tech-radar/` — quarterly inventory of what's adopted/rejected/deferred (snapshot)

A tool might appear in BOTH (research debate evaluating it; tech-radar entry recording the decision and tracking subsequent review).

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial. 6-stage pipeline, source list, evaluation modes by stake, tech-radar folder convention. Codifies organic 2026-Q1/Q2 adoption practice (Codex, Tach, Opus 4.7, ccusage, Perplexity, MCP-memory-deferred, GLM/Qwen-deferred, Spec Kit-evaluated).

---

## Claude Code internals
<!-- scope: runtime -->
<!-- version: 1.0 — 2026-04-24 -->

Claude Code (Anthropic's terminal-based agentic coding tool) has four extension mechanisms with confusingly similar names. Rob and Claude have repeatedly conflated them in 2026 sessions. This section establishes canonical definitions, locations, use cases, and the existing examples in Rob's ecosystem.

### Quick disambiguation
<!-- scope: runtime -->

| Mechanism | What it is | Where it lives | Trigger |
|-----------|-----------|----------------|---------|
| **Skill** | Progressive-disclosure knowledge module | `.claude/skills/<name>/SKILL.md` | Read on-demand by Claude Code when topic matches |
| **Slash command** | Custom invokable command | `.claude/commands/<name>.md` | Rob types `/<name>` |
| **Hook** | Lifecycle automation | `.claude/settings.json` OR `.pre-commit-config.yaml` | Auto-fires on event (PreToolUse, pre-commit, PostToolUse) |
| **Subagent** | Separate Claude instance with narrow focus | `.claude/agents/` | Invoked via Task tool from main agent |

**User-level vs project-level:**
- User-level: `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/settings.json` — applies across all repos
- Project-level: `<repo>/.claude/skills/`, `<repo>/.claude/commands/`, etc. — applies only in that repo
- Both can coexist; project-level takes precedence when names collide

### 7a. Skills (progressive-disclosure knowledge modules)
<!-- scope: runtime -->

**What:** Knowledge modules Claude Code reads on demand when context matches a trigger pattern. Designed for content too large for CLAUDE.md but reusable across sessions.

**Structure:**
```
<repo>/.claude/skills/<skill-name>/
  SKILL.md          # main file, <500 lines, trigger description + instructions
  references/       # additional content loaded only when needed (progressive disclosure)
  scripts/          # auxiliary executables if applicable
  examples/         # concrete examples Claude can study
```

**SKILL.md format (top of file):**
```
---
name: <skill-name>
trigger: <when does Claude Code load this — e.g. "before making changes to module X" or "when user asks about Y">
---

# <Skill Title>

[content]
```

**When to use:**
- Empirical patterns ("things this repo gets wrong" — see Rob's `gotchas` skill)
- Domain-specific knowledge that recurs across sessions
- Workflows too long for CLAUDE.md (which has ≤200 lines target per Council #28)

**When NOT to use:**
- Knowledge that fits in CLAUDE.md (≤200 lines budget) — keep there for auto-read
- Universal Rob rules — those go in `.dev-knowledge/protocols/PLAYBOOK.md`
- One-off task — slash command may fit better

**Real example in Rob's ecosystem:**
- `corp-monorepo/.claude/skills/gotchas/SKILL.md` — empirical patterns this repo has stumbled on (Trigger/Symptom/Fix/verify pattern)

**Anti-patterns:**
- **Skill files >500 lines** — defeats progressive disclosure; split to references/
- **Skills with no trigger description** — Claude Code can't know when to read it
- **Universal content as project skill** — should live in `.dev-knowledge/protocols/PLAYBOOK.md` instead

### 7b. Slash commands (custom invokable commands)
<!-- scope: runtime -->

**What:** Markdown files defining commands Rob can invoke by typing `/<name>` in Claude Code. Each command is a templated prompt Claude Code executes.

**Structure:**
```
~/.claude/commands/<name>.md   # user-level (cross-repo)
<repo>/.claude/commands/<name>.md   # project-level
```

**File format:** Just markdown. Body is the prompt Claude Code follows when command invoked. May contain `$ARGUMENTS` placeholder for command-line args.

**When to use:**
- Repeated workflow Rob runs >3× across sessions
- Multi-step procedures that benefit from consistent prompt
- Operations crossing multiple files/tools (e.g. session summary, /boot context loading)

**When NOT to use:**
- One-off task — write inline prompt instead
- Knowledge lookup — use skill instead
- Content best fits CLAUDE.md auto-read

**Real examples in Rob's ecosystem (user-level, `~/.claude/commands/`):**
- `/session-summary` — generate handoff for current session, include TOKEN-LOG snapshot if stale (renamed from `/handoff` 2026-04-24 to avoid trigger-word collision)
- `/boot` — load context: skills, recent commits, JOURNAL entries
- `/evolve` — promote learned patterns to skills/rules
- `/codex-review` — invoke Codex review on staged changes

**Anti-patterns:**
- **Commands without clear naming** — `/x` or `/do` are unmemorable
- **Trigger-word collisions** — `/handoff` matched user typing "handoff" in conversation; renamed to `/session-summary` (lesson 2026-04-24)
- **Treating commands as skills** — commands are invoked actions; skills are read-on-demand knowledge

### 7c. Hooks (lifecycle automation)
<!-- scope: runtime -->

**What:** Automated actions firing on Claude Code lifecycle events or git lifecycle events. LLMs advise; hooks enforce (per Council #28 community finding).

**Two flavors:**

**Claude Code hooks** — fire on tool/agent lifecycle:
- Location: `.claude/settings.json` (user or repo)
- Events: PreToolUse, PostToolUse, others per Claude Code docs
- Use case: enforce rules before/after Claude takes specific actions

**Pre-commit hooks** — fire on git commit:
- Location: `.pre-commit-config.yaml` (repo root)
- Framework: pre-commit.com (Python tool, cross-platform)
- Use case: enforce rules before code/docs land in repo

**When to use:**
- Mechanical enforcement of governance rules (scope tags, lint, test pass)
- Safety nets — block accidental violations LLM advice alone might miss
- Cost: hooks run on every commit; keep fast (<5 seconds typical)

**When NOT to use:**
- Rules best left as LLM advice (subjective conventions where context matters)
- Heavy validation (>30s) — moves to CI/CD instead
- Ambiguous rules — hooks fail loudly; vague rule = constant friction

**Real examples in Rob's ecosystem:**
- `.dev-knowledge/.pre-commit-config.yaml` — runs `normalize_headers.py` + codemap-freshness check (scope-tag enforcement withdrawn per ADR-48)
- corp-monorepo pre-commit (likely): ruff format, pytest collection check (verify per repo)

**Anti-patterns:**
- **Hooks bypassed with `--no-verify`** — defeats the safety net; should never be habit
- **Hooks slower than 5s** — incentivizes bypass; move to CI
- **Validator/hook divergence** — both tools must enforce identically (see ADR-27 amendment 2026-04-25, lesson re: invocation semantics)

### 7d. Subagents (separate Claude instances)
<!-- scope: runtime -->

**Amendment 2026-04-25 (subagents factually active):** Original v1.0 section called subagents "DEFERRED — no active subagents in Rob's ecosystem." This was incorrect. Verification 2026-04-25 confirmed two active user-level subagents exist at `~/.claude/agents/`. Section now describes actual subagents (Anthropic docs framing preserved as conceptual context). Per Gap #19 amendment-vs-reopen protocol: prescription drift, intent (disambiguation of 4 mechanisms) preserved.

**What (per Anthropic docs + Council #28 research):** Subagents are spawned Claude instances with narrow focus and fresh context window, invoked via main agent's Task tool. Designed for "read-heavy, write-light" delegation (per Cognition's June 2025 warning against subagents-as-code-generation-peers).

**Where they live:** `~/.claude/agents/<name>.md` (user-level, cross-repo) OR `<repo>/.claude/agents/<name>.md` (project-level).

**File format:** Markdown files describing the subagent's role, trigger conditions, and instructions. Main agent invokes them via Task tool.

**When to use:**
- Read-heavy operations (code search across large codebase, log analysis, doc lookups)
- Tasks benefiting from fresh context window (avoid main agent's context bloat)
- Operations that should not write/modify (per Cognition warning — subagents as readers, not collaborators)

**When NOT to use:**
- Code generation peers (anti-pattern per Cognition June 2025)
- Tasks that need main agent's full context (e.g. complex refactoring with cross-file knowledge)
- One-off operations — slash command may fit better

**Real examples in Rob's ecosystem (user-level, `~/.claude/agents/`):**
- `ecosystem-snapshot.md` — read-only point-in-time snapshot generator across all Corporate OS repos (git status, recent commits, test counts, dirty files); Haiku model; outputs facts only, refuses analysis
- `report-generator.md` — read-only structured report builder for weekly ecosystem reports and data condensation; Haiku model; markdown tables with source paths, escalates architectural reasoning back to main session

**Anti-patterns:**
- **Subagents as code-generation peers** — they diverge, conflict, waste tokens (Cognition's "Don't Build Multi-Agents" warning, June 2025)
- **Heavy write operations in subagents** — main agent loses sight of state changes; coordination breaks
- **Overusing subagents** — main agent + skills + slash commands sufficient for most workflows; subagents are specialist tool, not default

**For deeper guidance:**
- Anthropic Claude Code subagents documentation
- Cognition "Don't Build Multi-Agents" (cognition.ai blog, June 2025)
- Stream B Gap #10 (Adoption protocol) — applies to subagent additions/changes

### Adoption protocol — when Claude Code proposes a new skill/command/hook/subagent
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

When Claude Code observes a recurring pattern and suggests adding a skill, slash command, hook, or subagent, this protocol decides scope (user-level vs project-level), validates the addition, and ensures it's documented in the right places. Companion to subsections 7a-7d above (what they are) — this is "how to add one safely."

**Distinct from PLAYBOOK Section 6 Continuous Improvement** — that covers external tool/model adoption (Codex, Tach, ccusage). This subsection covers Claude Code's own extension mechanisms.

#### Triage: is the proposal worth adopting?
<!-- scope: meta -->

Adopt when ALL apply:
- **Pattern recurs** — Rob has done the same thing ≥3 times across sessions, OR Claude Code recognizes it'll save ≥5 prompts in next month
- **Stable interface** — what the skill/command/hook does won't change drastically next month
- **Clear scope** — fits one of the four mechanisms (Gap #7a-d) without forcing
- **Documentable** — Rob can explain in one sentence what it does and when

Reject if any:
- One-off pattern unlikely to recur
- Interface still evolving (premature to codify)
- Hybrid of multiple mechanisms (might be 2 separate additions instead)
- Better solved by updating CLAUDE.md or PLAYBOOK directly (not all knowledge needs an extension mechanism)

Defer if:
- Pattern looks valuable but Rob hasn't tried it manually enough times to validate friction is real
- Reopen trigger: after N more occurrences (set explicit count)

#### Decision: user-level vs project-level
<!-- scope: meta -->

**User-level** (`~/.claude/<mechanism>/`) when:
- Pattern applies across all repos Rob works in (.dev-knowledge, corp-monorepo, ai-council, future)
- Universal Rob workflow (e.g. `/session-summary`, `/boot`)

**Project-level** (`<repo>/.claude/<mechanism>/`) when:
- Pattern is repo-specific (corp-monorepo Tach layers, ai-council debate framework)
- Sensitive content shouldn't leak to other repos
- Repo's CLAUDE.md needs to reference it explicitly

When unclear: start project-level (lower blast radius), promote to user-level if pattern proves universal across 2+ repos.

#### Validation: does it actually work?
<!-- scope: meta -->

Before "adopted":
1. **Smoke test** — invoke the mechanism in its intended scenario; verify behavior matches description
2. **Side-effect check** — does it interfere with existing workflows? (e.g. trigger-word collision: `/handoff` → `/session-summary` rename 2026-04-24 happened because trigger phrase matched user typing)
3. **Speed check** — hooks <5s; skills/commands <50KB SKILL.md; subagents fresh-context appropriate
4. **Failure mode** — what happens when mechanism fails? Graceful or noisy?

If any fails: reject or iterate before adopting.

#### Install: where the file lands
<!-- scope: meta -->

Per mechanism (cross-reference subsection 7a-7d for full structure):

| Mechanism | User-level path | Project-level path |
|-----------|-----------------|---------------------|
| Skill | `~/.claude/skills/<name>/SKILL.md` | `<repo>/.claude/skills/<name>/SKILL.md` |
| Slash command | `~/.claude/commands/<name>.md` | `<repo>/.claude/commands/<name>.md` |
| Hook (Claude Code) | `~/.claude/settings.json` | `<repo>/.claude/settings.json` |
| Hook (pre-commit) | n/a (always project-level) | `<repo>/.pre-commit-config.yaml` |
| Subagent | `~/.claude/agents/<name>.md` | `<repo>/.claude/agents/<name>.md` |

#### Document: where to link
<!-- scope: meta -->

After install, link from:
- **CLAUDE.md** (Slash commands §7, Skills §8, or Hooks §9 as applicable) — for project-level adoptions; keeps Codex aware of active governance
- **CLAUDE.md** — for project-level Claude Code-specific behavior (per Gap #5 template Slash commands, Skills, and Hooks sections)
- **JOURNAL.md entry** for the session that adopted it
- **CHANGELOG.md entry** for repo-visible adoptions
- **tech-radar 2026-Q?.md** Adopted (active inventory) section if user-level (per Gap #17 Continuous Improvement Section 6)

User-level adoptions don't need per-repo CLAUDE.md updates (they apply everywhere automatically) but do warrant tech-radar entry for periodic value review.

#### Anti-patterns
<!-- scope: meta -->

- **Adoption without triage** — every Claude proposal becomes a new file; ecosystem bloats
- **Project-level when should be user-level** — duplicates same skill across 3 repos; one source of truth lost
- **User-level when should be project-level** — leaks repo-specific knowledge into universal scope
- **Skip validation** — broken hook/command/skill propagates and fails silently for weeks
- **Forget documentation step** — Codex/Cursor never learn about the new tool; cross-tool awareness breaks

#### Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — initial. 5-stage pipeline (Triage → Decision → Validation → Install → Document) with cross-reference to Gap #17 (broader tool adoption). Anti-patterns from observed practice. Will refine after live use.

### Cross-reference to CLAUDE.md tools sections
<!-- scope: meta -->

When a repo has any of the above active (skills, slash commands, hooks, subagents), they get listed in the relevant CLAUDE.md sections: Slash commands (§7), Skills (§8), or Hooks (§9). Specifically:

- **Code review:** Codex configuration → see `templates/codex-review-config-template.md`
- **Architecture enforcement:** Tach configuration if used
- **Pre-commit hooks:** list active hooks with purpose
- **Skills:** list active skills with paths
- **Subagents:** list if any are active (per Rob's ecosystem currently: ecosystem-snapshot, report-generator at user-level)

This keeps Codex aware of the same governance Claude Code operates under.

### Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial. 4 subsections: skills, slash commands, hooks, subagents (deferred). Disambiguation table at top. Real examples from corp-monorepo (gotchas skill), user-level (/session-summary, /boot, /evolve, /review), .dev-knowledge (scope tag pre-commit hook). Subagents documented from Anthropic docs + Council #28 research, no Rob ecosystem instance.

---

## 1. Starting a New Project
<!-- scope: dev -->

**Every project begins with CLAUDE.md, not code.** If you can't describe what the project does in 3 sentences, you don't understand it yet. For architectural decisions (new database? new package? new integration?), run an AI Council debate before writing a single line.

### Scaffold
<!-- scope: dev -->

```bash
mkdir -p my-project/src/my_package my-project/tests my-project/config my-project/scripts
touch my-project/{CLAUDE.md,README.md,CHANGELOG.md,pyproject.toml,.gitignore}
touch my-project/src/my_package/{__init__.py,cli.py}
touch my-project/tests/conftest.py
```

### CLAUDE.md template (minimum viable)
<!-- scope: dev -->

```markdown
# CLAUDE.md — project-name

## What this project does
[3 sentences max]

## Architecture
[Folder layout table]

## Dev standards
- Python 3.11+, type hints
- pyproject.toml for deps
- ruff for linting, pytest for testing
- Click for CLI, Rich for output
- Logging not print, dataclasses not dicts
- Config in YAML not hardcoded

## Key commands
[How to run, test, lint]

## What NOT to do
- Do not create files outside src/, tests/, config/, scripts/
- Do not hardcode paths
- Do not commit output/generated data
- Do not skip tests between changes

## Folder governance
- docs/: project-level governance, handoffs, decision records, architecture
- output/: gitignored, disposable
- Every generated .md file needs a date (filename or frontmatter)

## Global skills
Before modifying code, read ~/.claude/skills/gotchas/gotchas.md
```

### First commit, then dev loop
<!-- scope: dev -->

```bash
git init && git add -A && git commit -m "feat: scaffold project-name"
```

Then for each feature:
1. Branch: `git checkout -b feat/feature-name`
2. Write test stub FIRST (even `def test_thing_exists(): assert hasattr(module, 'thing')`)
3. Implement
4. Test: `pytest -x --tb=short`
5. Lint: `ruff check src/ tests/ --fix`
6. Commit: `git commit -m "feat: description"`
7. Merge: `git checkout main && git merge feat/feature-name`
8. Delete branch, update CHANGELOG.md if files changed

---

## 2. Creating a Claude Code Prompt
<!-- scope: hybrid -->

**Rob's prompt format is non-negotiable.** Front-loading the full spec in the first message eliminates 2-3 discovery turns. Every prompt starts with a summary table that determines execution parameters.

### Summary table (required at top of every formal prompt)
<!-- scope: hybrid -->

```
| Parameter | Value                               |
| --------- | ----------------------------------- |
| Model     | Sonnet / Opus                       |
| Mode      | auto-accept / plan-then-auto / plan |
| Effort    | low / medium / high / xhigh         |
```

### How to choose Model
<!-- scope: llm -->

- **Sonnet** for: mechanical work ("apply this fix"), single-file edits, well-specified implementation, pattern-matched code, boilerplate, file renames, config updates, code-and-test loops where the spec is detailed.
- **Opus** for: audit / review / synthesis tasks; architecture decisions and clause-level reasoning; judgment-heavy work (severity calibration, ambiguity resolution); long-context comparison across multiple inputs; subtle pattern recognition (security review, gotcha identification); multi-package changes; complex debugging; novel logic design.

Rule of thumb: if the task is "do X the way we always do it" → Sonnet. If the task is "figure out the right approach, then do it" → Opus.

**Actively choose per task; do NOT default to Sonnet.** There is no budget ceiling per the LLM-spend rule. When uncertain, lean Opus — Sonnet's failure modes (missed nuance, factual misses) cost more than Opus's overhead.

### How to choose Mode
<!-- scope: runtime -->

- **auto-accept** — read-only tasks, mechanical changes with clear spec, file moves/renames, formatting. You know exactly what should happen, Claude just executes
- **plan-then-auto** — design decisions embedded in a prompt. Start in plan mode for the UNDERSTAND + PLAN phases, review the plan, then switch to auto-accept for execution. This is the default for most multi-step prompts
- **plan** (manual approval each step) — risky operations touching production data, OneDrive paths, database migrations, anything with blast radius. Also for learning/exploration where you want to see each step

### How to choose Effort
<!-- scope: hybrid -->

- **low** — single file, <30 min, no architectural decisions. Example: "add a CLI flag", "fix this test", "rename this variable across the file"
- **medium** — 2-5 files, 30-90 min, may involve design choices within known patterns. Example: "add a new CLI command", "refactor this module to use dataclasses"
- **high** — 5+ files or 2+ packages, 90+ min, requires UNDERSTAND phase, potential blast radius. Example: "implement search federation", "migrate classifier to new taxonomy"
- **xhigh** — hardest debugging, end-to-end pipeline verification, Council-level analysis. Opus only. Example: "find why magistrala silently drops events", "verify boundary enforcement across all packages"

### Structure
<!-- scope: hybrid -->

```
| Parameter | Value  |
| --------- | ------ |
| Model     | [pick] |
| Mode      | [pick] |
| Effort    | [pick] |

TITLE: What we're doing
REPO: Which repo/package
PURPOSE: Why (1 sentence)

→ Read CLAUDE.md + relevant gotchas
→ Git workflow (branch, commit per step, pytest between)

UNDERSTAND:
- What's the problem?
- What's the scope? (which files, which packages)
- What are the risks?
- What does failure look like?

STEPS:
1. [action] — COMMIT: "feat: description"
2. [action] — COMMIT: "feat: description"
...

FINAL: Run full test suite, merge to main

WHAT NOT TO DO:
- [explicit anti-patterns for this task]
```

### Quick-reference examples
<!-- scope: hybrid -->

| Task                              | Model  | Mode           | Effort |
| --------------------------------- | ------ | -------------- | ------ |
| Fix typo in config                | Sonnet | auto-accept    | low    |
| Add CLI flag to existing command  | Sonnet | auto-accept    | low    |
| Write tests for untested module   | Sonnet | auto-accept    | medium |
| Refactor module to dataclasses    | Sonnet | plan-then-auto | medium |
| New extraction pipeline step      | Opus   | plan-then-auto | high   |
| Cross-package schema migration    | Opus   | plan           | high   |
| Debug flaky test (unknown cause)  | Opus   | plan           | medium |
| Full data rebuild from scratch    | Opus   | plan           | high   |
| Batch file renames across project | Sonnet | plan-then-auto | medium |
| New package scaffolding           | Sonnet | auto-accept    | low    |

### Decision scope for when to write a formal prompt
<!-- scope: hybrid -->

- **1 file change** → conversational ("hey, fix X in Y") — no summary table needed
- **2-3 files** → conversational + paste context — summary table optional
- **3+ files or 2+ packages** → formal prompt with summary table (required)
- **Architecture decision** → AI Council debate first, then formal prompt

### Key rules
<!-- scope: hybrid -->

- Git workflow section is non-negotiable in EVERY prompt, even for non-repo changes (explain why not needed)
- "What NOT to do" section prevents Claude from over-engineering
- Include `pytest -x --tb=short && ruff check && git status` after each step, not just at the end
- Include `git status must show clean between each numbered step`
- CHANGELOG.md entry required in FINAL section if files changed
- Bypass permissions (no approval) → almost never, only for trivial read-only operations

### Prompt Generation Card maintenance rule (per ADR-56, Council Q3)
<!-- scope: hybrid -->

The handoff bundle ships an inline **Prompt Generation Card** in
`00_first-message.md` (the operational extract a fresh browser chat uses to
generate Claude Code prompts, since it cannot read the filesystem). This PLAYBOOK
section remains the rationale and edge-case authority; the card is the
point-of-use procedure. The two are an intentional duplication.

**Any change to prompt conventions (model/mode/effort criteria, the summary
table, the mandatory skeleton, hook guidance) MUST update BOTH:**

1. this PLAYBOOK rationale, and
2. the inline card in `templates/HANDOFF_FOLDER_TEMPLATE.md` `### 00_first-message.md`.

Drift between the two is a process bug — the card is the point-of-use authority,
PLAYBOOK is the maintenance source. The card has a ≤200-line size budget; if it
overflows, restructure into card + appendix rather than relocating authority.

---

## 3. Absorbing New Information
<!-- scope: hybrid -->

**Papers, repos, articles, tools → evaluate → extract actionable items → implement or reject.** Don't let "interesting" become "installed."

### Evaluation flow
<!-- scope: hybrid -->

1. **Quick triage (30 seconds):** Is this relevant to my work? Is it at my level or below?
   - Tutorial-level content (below Rob's level) → bookmark for reference only, skip
   - New tool with <100 GitHub stars and v0.1 → too early, revisit in 3 months
2. **Extract (5 minutes):** What are 2-3 actionable items from this?
3. **Decide:** Implement now, add to backlog, or reject with reason
4. **Log:** Add entry to LESSONS.md with category and action taken

### Council debate threshold
<!-- scope: hybrid -->

- Tactical choices (which library, which formatter) → decide yourself
- Architectural decisions (new database, new integration pattern, new package) → AI Council
- When in doubt: if reverting would take >1 hour, it's architectural

---

## 4. Extracting Lessons from Any Session
<!-- scope: llm -->

**Lessons die in chat history if not extracted.** Every session — browser chat, Claude Code terminal, Council debate, article analysis — potentially contains lessons. Without an explicit extraction step, they vanish.

### When to extract
<!-- scope: llm -->

- **End of every browser chat** that involved decisions, debugging, or new insights
- **End of every Claude Code session** (via LESSONS.md entry if applicable)
- **After every Council debate** (decisions are binding, but the reasoning often contains lessons)
- **After reading an article/repo/tool** that changed how you think about something

### How to extract (2 minutes, no more)
<!-- scope: llm -->

Ask yourself: **"What 2-3 things did I learn that I didn't know before this session?"**

For each, write one entry in LESSONS.md:
```
### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]
```

Categories: `prompt-craft` / `token-optimization` / `architecture` / `tooling` / `process` / `gotcha`  
Scope: `dev | llm | hybrid | runtime | meta` (ADR-29 — applies to new entries only; existing 123 entries are grandfathered)

### What qualifies as a lesson
<!-- scope: llm -->

- Something that surprised you (expectation ≠ reality)
- A mistake that cost >10 minutes
- A technique that saved significant time
- A decision rationale you want to remember
- A tool/article insight that changed your approach

### What does NOT qualify
<!-- scope: llm -->

- Things you already knew (no "learned that tests are important")
- Pure factual information (that goes to vault or ~/.claude/)
- Decisions without reasoning (those are ADRs, not lessons)

### When a lesson becomes a rule
<!-- scope: meta -->

If you find yourself writing a lesson that sounds like "always do X" or "never do Y" — it might be a rule, not a lesson. Write the lesson in LESSONS.md for context, then also add it to `~/.claude/` (gotchas, rules/, or learned-rules.md) with a verify: line. Cross-reference both.

---

## 5. Running an AI Council Debate
<!-- scope: llm -->

**Council debates are valuable but can become procrastination.** Hard rule: max 2 debates before implementation starts. Full format guide lives in the council project's docs/ folder.

### When to use Council vs. decide yourself
<!-- scope: llm -->

- **Council:** New package creation, database choice, integration pattern, tool adoption, major refactor, knowledge organization
- **Self:** Library version, config format, variable naming, test strategy for single feature
- **Rule of thumb:** If reverting would take >1 hour, it's architectural → Council

### Debate question format (summary)
<!-- scope: llm -->

A Council debate is NOT a Claude Code prompt. No Model/Mode/Effort, no UNDERSTAND, no Steps, no "What NOT to do." It's a question with options.

```markdown
---
models: claude,gemini,deepseek,grok
synthesizer: openai
rounds: 2
---

## Question: [one clear sentence]

### Current State
[concrete facts — numbers, problems, what exists today]

### Questions
1. **[sub-question]?**
   - A: [option with trade-off in one sentence]
   - B: [option with trade-off]
   - C: [option with trade-off]

### Constraints
- [hard boundary that eliminates options]
```

**Key rules:**
- Question = one sentence. If you can't, split into two debates.
- Current State = facts and numbers, not narrative or opinions
- Options = 2-4 per question, genuinely different approaches, trade-off baked into each
- Constraints = only hard boundaries that eliminate options. "ADHD" eliminates manual daily discipline. "Zero plugins" eliminates plugin solutions.
- Total file: 40-80 lines. Over 100 = too much narrative, trim.

### Running the debate
<!-- scope: llm -->

```bash
# Process debates from inbox
council-cli --inbox

# Direct question
council-cli "REST vs GraphQL?" --full --rounds 2
```

> Exact CLI syntax depends on the council tool — see its CLAUDE.md for current commands.

### Post-debate protocol
<!-- scope: llm -->

1. Decision is BINDING once synthesized
2. **Distill the verdict into a committed ADR** — this is a mandatory, automated step, never a manual hand-off. Run a Claude Code prompt that: (a) verifies the next ADR number against the `docs/decisions/ADR-*.md` sequence, (b) aligns the draft to `templates/ADR-template.md`, (c) writes `docs/decisions/ADR-{NN}-{topic}.md` (hyphens per ADR-34), and (d) commits it. The browser layer drafts ADR content; it never hands over a file with a placeholder number (`NN`) or manual TODOs. A debate is not done until its ADR is committed.
3. Archive transcript → `docs/decisions/transcripts/` (commit separately or together with ADR)
4. Add the ADR row and traceability entry to `docs/decisions/README.md` in the same commit
5. Never reopen a decided topic unless new evidence appears

### Council Debate Archival Protocol
<!-- scope: llm -->

Every Council debate output MUST be archived immediately after the debate completes. Skip this and the debate is effectively lost. Retroactive archive 2026-04-24 recovered 5 debates that sat in `ai-council/output/` for weeks.

> **Current state (updated 2026-05-26 — ADR-43 routing implemented):** Cross-project transcript routing now ships in `ai-council` (`routing.py` `TargetResolver`, ADR-43 amendment cycle 1). When a debate names a `target-project:` (frontmatter) or `--target-project` (CLI), the CLI writes the transcript to `<dev_root>/<target>/docs/decisions/transcripts/` automatically on completion — for `.dev-knowledge`-targeted debates that is `docs/decisions/transcripts/`, with **no manual archival step**. The canonical copy still lands in `ai-council/output/`; mirror writes are best-effort (a failure logs a warning, the canonical write still succeeds). Routing is **opt-in per invocation**: the manual pipeline below remains the fallback for debates that do **not** set a target-project.

**Pipeline (3 steps, ~5 min):**

1. **Identify target location** within .dev-knowledge:
   - Debate about .dev-knowledge itself (pick/judge mode) → `docs/decisions/transcripts/council-out-YYYYMMDD-HHMMSS-topic.md`
   - Research-mode debate → `docs/research/YYYY-MM-DD-slug.md`
   - Debate about another repo (e.g., corp-monorepo architecture) → `docs/research/YYYY-MM-DD-council-NN-slug-REPO.md`
     - Suffix with `-REPO` indicates decision applies elsewhere
     - Future work: mirror to that repo's transcripts/ folder

2. **Copy** `ai-council/output/council-out-YYYYMMDD-HHMMSS-topic.md` to target:
   - Decisions: keep filename as-is (`council-out-YYYYMMDD-HHMMSS-topic.md`)
   - Research: `YYYY-MM-DD-kebab-case-slug.md`
   - Byte-exact copy, preserve original in ai-council/output/

3. **Commit** with message: `docs: archive Council #NN — [topic]`

**Optional follow-up (separate commit):**
- Pick-mode with clear decision → write ADR in `docs/decisions/` referencing transcript
- Research-mode → no ADR, transcript/report suffices
- Judge-mode → depends on verdict

**Anti-pattern:** Accumulating 2+ un-archived debates in `ai-council/output/`. If detected, run retroactive archive before the next Council session.

**Future enforcement:** possible pre-commit hook checking ai-council/output/ for files >7 days old not present in any repo's archive locations.

### Council output convention (current state)
<!-- scope: meta -->

AI Council CLI writes the canonical transcript to `ai-council/output/` and, when a debate sets a
`target-project:` (frontmatter) or `--target-project` (CLI), **also routes a copy automatically**
to `<target>/docs/decisions/transcripts/` per ADR-43 (`routing.py` `TargetResolver`; `settings.yaml`
`target_projects` lists `.dev-knowledge`). Routed debates need **no manual archival** — the routed
copy is the transcript file only (no `_metrics.json`), preserving the canonical
`council-out-YYYYMMDD-HHMMSS-*.md` filename. Source of truth remains `ai-council/output/`.

Routing is **opt-in per invocation** — a debate that does not name a target-project still emits only
to `ai-council/output/` and is archived via the manual pipeline above ("Council Debate Archival
Protocol"). Mirror writes are best-effort (failure logs a warning; the canonical write always
succeeds), and routing depends on `settings.yaml` naming the target with a resolvable `dev_root`
(see ADR-43; routing-fragility noted in the 2026-05-25 pipeline audit, finding D2).

### When to run Council vs single-model + critic
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

Per Council #28 community research finding: AI Council debate (4-model panel, 2 rounds, ~$0.50, ~5min) is overkill for normal implementation decisions. Reserve Council for truly ADR-worthy questions; use single-model + critic loop for the rest.

#### Gate Council to ADR-worthy decisions
<!-- scope: meta -->

Council debate is justified when ALL apply:
- **Architectural impact** — affects module boundaries, layer taxonomy, dependencies, data model
- **Multi-ADR ripple** — decision touches 2+ existing ADRs or creates new binding constraint
- **Reversal cost > 1 hour** — backing out the decision means meaningful rework
- **Multiple plausible options** — at least 2 genuinely different approaches exist (not "do or skip")

If any criterion fails, prefer single-model + critic loop.

#### Single-model + critic alternative
<!-- scope: meta -->

For decisions outside the Council gate:
1. **Browser chat (architect)** drafts the decision (option choice + rationale)
2. **Codex review** (or analogous critic) checks the drafted decision for risks, edge cases, missed alternatives
3. **Rob** approves, rejects, or iterates
4. **Outcome** lands as: ADR (if binding), JOURNAL entry (if tactical), or just commit message (if local)

Cost: ~$0.05 + 2min vs Council's $0.50 + 5min. Significantly cheaper for the >70% of decisions that don't need 4-model debate.

#### Examples (2026-04 sessions)
<!-- scope: meta -->

| Decision | Path used | Reason |
|----------|-----------|--------|
| Scope tagging architecture (Option A) | Council #27 | Affected entire `.dev-knowledge` repo, 3 plausible options, multi-week reversal cost |
| ADR-29 LESSONS grandfathering format | Council #27 (companion) | Bound to scope tagging decision, multi-format alternatives |
| TOKEN-LOG cadence (per-session vs threshold) | Browser + Rob | Two clear options, low reversal cost, browser-architect sufficient |
| TOKEN-LOG order convention (newest-first) | Browser + Rob | Two options, consistent with CHANGELOG, no architectural ripple |
| Validator/hook H3 divergence fix | Browser + Rob | Implementation bug, single correct fix, no debate needed |
| CLAUDE.md template structure (10 sections) | Browser + Rob | Well-known community pattern (Council #28 research), no need to re-debate |

#### Anti-patterns
<!-- scope: meta -->

- **Council habit-formation** — running Council because "it's how we decide" without checking the gate. Costs add up fast ($0.50 × N decisions).
- **Single-model laziness** — choosing single-model path when criteria genuinely apply (architectural ripple), then later reopening as Council = wasted first decision.

### Amendment vs Reopen Decision Protocol
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

When validator/tooling reality contradicts an ADR's prescription, two paths exist: amend in place (preserve intent, update prescription) or reopen the decision (intent itself was wrong). This protocol decides which.

**Pattern emerged organically 2026-04-24** — used 3 times in sequence:
1. ADR-27 amendment: delta rule replaced flat-threshold enforcement (validator built differently than ADR prescribed)
2. ADR-29 amendment: H1 placement for LESSONS file-level tag (collided with validator's 3-line H1 detection window)
3. ADR-27 amendment: heading levels H2+H3 explicit, invocation semantics clarified (silent vacuous-pass discovered)

#### Decision tree
<!-- scope: meta -->

**Amend in place** if:
- Validator/tooling implementation diverged from ADR prescription, but original intent still correct
- Real-world use revealed prescription was unclear/incomplete; clarification preserves intent
- New edge case discovered; addressing it doesn't change the decision's core
- Implementation detail correction (e.g., regex pattern, file path, threshold value tweak)

**Reopen the decision** (full Council or browser+critic per gating above) if:
- Original intent itself was wrong (not just prescription)
- Context changed materially: new constraints, new tools available, new evidence contradicting decision premise
- Multiple ADRs affected by the change (cascading impact)
- Stakeholder expectations shifted (e.g., adding non-dev contributors changes decision economics)

#### Amendment mechanics
<!-- scope: meta -->

When amending in place:
1. Add **Amendment YYYY-MM-DD** block at end of ADR file (do not rewrite original decision text)
2. Block structure:

   > **Amendment YYYY-MM-DD ([brief topic]):** [What was wrong/unclear in original prescription]. Resolution: [what the prescription now says]. Intent preserved: [why this is amendment not reopen].

3. Update validator/tool/process to match amendment
4. Add LESSONS.md entry (per ADR-29 format) describing what was discovered
5. CHANGELOG entry: "ADR-NN amended YYYY-MM-DD — [topic]"

#### Reopen mechanics
<!-- scope: meta -->

When reopening:
1. Mark original ADR with **Status: Reopened YYYY-MM-DD** at top
2. Run Council per gating criteria above (full Council if architectural; browser+critic if not)
3. Outcome lands as new ADR (e.g., ADR-NN with "Supersedes ADR-MM" reference)
4. Original ADR retains content (history preserved), but new ADR governs

#### Anti-patterns
<!-- scope: meta -->

- **Amending intent, not prescription** — if you find yourself rewriting the original decision text to "what we should have said," that's a reopen, not amendment. Don't conflate.
- **Reopen for prescription drift** — if validator just needs a regex tweak, that's amendment. Reopen ceremony wastes effort.
- **No amendment record** — silently changing tool to match new behavior without an amendment block in the ADR. Future Claude sees ADR vs reality mismatch with no trail.

#### Examples (2026-04-24)
<!-- scope: meta -->

| ADR | Trigger | Decision | Reason |
|-----|---------|----------|--------|
| ADR-27 (scope tagging) | Validator built with delta-rule enforcement, not flat threshold | Amend | Original intent (≤25% hybrid ceiling, blocking) preserved; mechanism (when to block) clarified |
| ADR-29 (LESSONS grandfathering) | H1 file-level tag collided with validator's H1 detection window | Amend | Original intent (file-level tag for LESSONS, not per-section) preserved; placement (H1 not `## Entries`) clarified |
| ADR-27 (scope tagging) | Validator silently passed when called without args; H2 vs H3 ambiguous | Amend | Original intent (every section header tagged) preserved; level scope (H2+H3) and invocation semantics (auto-scan IN_SCOPE_FILES) explicit |

### Codex review archival protocol
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-25 -->

Codex code review (OpenAI's read-only reviewer) produces findings in terminal output during a session. Without explicit archival, findings disappear when the session ends. This protocol captures Codex output as a durable artifact — analogous to Council Archival Protocol above.

**Pattern parallel to Council Archival:** Council debates → `docs/decisions/transcripts/`. Codex reviews → `docs/audits/YYYY-MM-DD-codex-{slug}.md`.

#### Trigger
<!-- scope: meta -->

Archive Codex review when ANY apply:
- Review found ≥1 Critical or High severity finding
- Review precedes a non-trivial merge (3+ files OR safety-critical paths)
- Findings reference future work (e.g. "this should be refactored later" with concrete pointer)
- Rob explicitly requests "archive this Codex output"

Skip archival when:
- Review found only Low severity polish issues addressed in same session
- Trivial commits (typo fix, dependency bump, single-file refactor)
- Review explicitly inconclusive ("could not parse changeset")

#### Target path
<!-- scope: meta -->

`{repo}/docs/audits/YYYY-MM-DD-codex-{slug}.md`

Where:
- `YYYY-MM-DD` — date of review
- `{slug}` — kebab-case identifier (feature, branch, or commit topic)

Example: `docs/audits/2026-04-22-codex-handoff-process-rewrite.md`

#### Format
<!-- scope: meta -->

```markdown
# Codex Review — {topic}

**Date:** YYYY-MM-DD
**Branch:** {branch-name}
**Commit (HEAD at review):** {short SHA}
**Reviewer:** Codex (OpenAI)
**Mode:** {full review | diff review | targeted}

## Severity breakdown

| Severity | Count |
|----------|-------|
| Critical | N |
| High     | N |
| Medium   | N |
| Low      | N |

## Findings

### [SEVERITY] file:line — short description

**What:** One sentence.
**Why:** One sentence.
**Fix direction:** One sentence.
**Action:** [resolved in this session / queued / deferred / dismissed with reason]

(Repeat per finding. Group by severity. Omit empty sections.)

## Resolution summary

What was fixed in this session vs queued for later. Cross-link to JOURNAL entry and commits.

## Notes

Reviewer's narrative observations beyond per-finding (e.g. "consistent error handling pattern across module"), if any.
```

#### Linking from other docs
<!-- scope: meta -->

After archival, cross-link FROM:
- **JOURNAL.md entry** for that session: "Codex review archived: docs/audits/YYYY-MM-DD-codex-{slug}.md (N findings, M resolved)"
- **Commit message** of the resolution merge: "fix(scope): address Codex Critical/High findings — see docs/audits/YYYY-MM-DD-codex-{slug}.md"
- **CHANGELOG.md** if findings affected user-visible behavior

#### Anti-patterns
<!-- scope: meta -->

- **Archive everything** — low-severity polish findings don't warrant an audit document; archive only when trigger criteria match
- **Archive without resolution tracking** — review without clear "what was fixed / what's deferred" loses accountability
- **Codex output rot** — letting findings linger across sessions without resolution status creates ambiguity over what's still open

#### Section history
<!-- scope: meta -->

- v1.0 (2026-04-25) — initial. Manual archival protocol mirroring Council Archival pattern. Future enhancement: pre-commit hook checking for un-archived Codex sessions older than N days.

---

## 6. Code Review with Claude Code
<!-- scope: dev -->

**Code review stays on Sonnet — security boundary, never Haiku.** This is a Council-binding decision.

### Process
<!-- scope: dev -->

1. Specify scope: which files, which changes, what to focus on
2. Ask Claude Code to read the diff first, report what it sees
3. Focus areas: security, edge cases, error handling, test coverage
4. Never auto-apply suggested changes — review each one

---

## 7. Managing a Long Claude Code Session
<!-- scope: hybrid -->

**Sessions longer than ~4 hours should be split.** Context degradation is not linear — it accelerates.

### Session start protocol
<!-- scope: hybrid -->

1. Review recent CHANGELOG.md entries
2. Read CLAUDE.md
3. Check gotchas
4. `git status` (must be clean)
5. Define 1-2 objectives for this session — everything else is backlog

### During session
<!-- scope: hybrid -->

- `/clear` between unrelated tasks (saves 30-40% input tokens)
- Commit after each logical change
- Test after each change (not at the end)
- If scope creeps: "Adding to OPEN_DECISIONS.md, not doing today"
- Use Plan Mode before implementation (catches bad approach at 200 tokens vs 5000)
- Use line ranges (`@file:15-80`) instead of whole files

### When context gets heavy
<!-- scope: hybrid -->

- `/compact` at 40% (aggressive, Council-approved)
- `/session-summary` before switching to Claude.ai for architecture consulting
- If Claude says "it's done" on a complex operation — VERIFY with filesystem commands

### Session end protocol
<!-- scope: hybrid -->

1. Run full test suite
2. Update CHANGELOG.md if files changed
3. Update project handoff doc (if exists)
4. `git status` (must be clean — if "27 modified files", STOP and commit)
5. Write 3-line handoff note

---

## 8. Handing Off Between Sessions
<!-- scope: meta -->

Operational authority: `protocols/HANDOFF_PROCESS.md` (ADR-32 v2.0 + ADR-37 two-phase overlay). This section summarizes handoff governance. For handoff generation, follow HANDOFF_PROCESS.md.

Cross-refs: ADR-37, ADR-32, ADR-42 (handoff format v3)

### Two-phase structure (ADR-37)
<!-- scope: meta -->

Every handoff has two authoritative top-level sections that appear above the ADR-32 9-section Detailed Context:

**Current State** (maps to `06_STATE_OF_PLAY.md`): verified factual status, decisions made this session, open questions, last verified commit SHA + timestamp.

**Future State** (maps to `07_ACTION_PLAN.md`): next session goal (1–3 session horizon, not multi-quarter), recommended actions in priority order, dependencies, BACKLOG.md references (Section 10).

**Canonicality rule:** Top-level Current/Future State = authoritative operational state. ADR-32 Detailed Context = reference layer. If they contradict, top-level wins.

Mandate by handoff type:
- **Session handoffs:** Future State required. `Future state: undetermined` valid only with written justification (cognitive exhaustion / scope mismatch / unresolved dependency). Unjustified absence = invalid.
- **Audit handoffs** (generated by audit tool per Section 18): STRONG mandate — validator rejects folder if Future State missing.

### Roles
<!-- scope: meta -->

- **Claude Code (terminal):** reads files, runs commands, edits code, verifies state, runs tests. Trusts filesystem, not memory.
- **Claude.ai (browser):** architecture consulting, strategic decisions, critical thinking. Questions the approach, identifies risks. Never rubber-stamps.

> **See ESSENTIALS § Roles for canonical definition (Does/Does NOT lists, Three-layer flow per ADR-28).**

### Handoff paths
<!-- scope: meta -->

**Path A — Claude Code → Browser:** `/session-summary` in Claude Code → paste into Claude.ai. Discuss architecture/strategy; decisions return as prompts (Section 2 format).

**Path B — Browser → New Browser:** Say `wygeneruj handoff`. Claude generates the folder-format handoff per HANDOFF_PROCESS.md — Rob makes zero formatting decisions. Trigger at ~2 hours while context is still fresh. Generate → Copy → Paste. No archiving step.

**Path C — Browser → Claude Code:** Claude.ai writes prompts in Section 2 format (Model/Mode/Effort table). Prefer questions over commands. Let Claude Code discover actual state, then propose actions.

### Token log cadence
<!-- scope: meta -->

Every /session-summary run checks TOKEN-LOG.md staleness. If latest entry >7 days old, a new short-format snapshot is appended via `ccusage --json`. Otherwise skipped.

**Trigger:** /session-summary staleness check; conditional execution (not every session).

**Source:** `ccusage --json` (reads local Claude Code usage data — see ENVIRONMENT.md)

**Threshold:** 7 days. Most recent entry's date extracted from first `## YYYY-MM-DD` header line in TOKEN-LOG.md.

**Format (short, sustainable):**

```
## YYYY-MM-DD (since YYYY-MM-DD delta)

Cost: $X.XX | Sessions: N | Active days: N
Tokens (in+out): X.XM
Top models: Model-A X%, Model-B Y%, Model-C Z%
Peak day: $X.XX on YYYY-MM-DD
Notable: [1-2 line signal e.g. "Opus 4.7 adoption curve", "Haiku routing shift"]
```

**Order convention:**
- TOKEN-LOG.md and CHANGELOG.md: newest-first (prepend). Rationale: logs optimize for current-state scanning.
- LESSONS.md: append-only (oldest-first). Rationale: chronological narrative; order preserves "what we learned when".

New TOKEN-LOG entries go at the top (after file header, before previous newest entry). /session-summary reads the first matching `## YYYY-MM-DD` header for the staleness check.

**Cache tokens** excluded from in+out for cross-period comparability. Note cache only when notable.

**Rationale:**
- Per-session cadence rejected: ~$0.02/run overhead wasteful for weekly-sufficient data
- Manual weekly ritual rejected: forgetting risk (4 weeks stale before ccusage adoption)
- Threshold-based: amortized ~$0.006/run, auto-triggers on staleness, zero forgetting risk
- Short format keeps entries scannable over months; full format reserved for migrations

---

## 9. Weekly Review (Friday)
<!-- scope: hybrid -->

**Friday consolidation — 30 minutes max, not a project.**

1. Run `/evolve` in Claude Code — review corrections, observations, propose rule promotions/pruning
2. Review gotchas added this week — any patterns?
3. Review token usage — `ccusage --json` → append snapshot to TOKEN-LOG.md. Is Opus verbosity still the main drain?
4. Review LESSONS.md entries from this week — anything to change in PLAYBOOK?
5. Review OPEN_DECISIONS.md — anything stale? Anything urgent?
6. Quick project health check (test suite, lint, stale branches)
7. Update ENVIRONMENT.md if any config changed

---

## 10. BACKLOG Grooming Workflow
<!-- scope: meta -->

`BACKLOG.md` is the single canonical source for ALL pending items across sessions. Handoffs reference BACKLOG items by pointer (stream + title), never duplicate the queue. Per-handoff and quarterly grooming prevent the write-only graveyard anti-pattern.

**Mandate:** `BACKLOG.md` is part of the universal governance baseline (ADR-38 amendment A5, 2026-05-23; ADR-41) — mandatory for every repo regardless of size. (Previously gated to M+ repos; the repo-tier system is deprecated.)

### Schema
<!-- scope: meta -->

```
## Stream {name}

### [P{1-3}] [Status] Item title
- **What:** brief description
- **Why:** rationale / triggering context
- **Vision ref:** (optional) link to VISION.md section if strategic
- **Added:** YYYY-MM-DD by {browser-1 | audit-tool | rob}
- **Status:** open | in-progress | blocked | done
```

P1 = critical/blocking other work. P2 = important/next 1–3 sessions. P3 = wishlist/when capacity allows.

Anti-pattern: do NOT mutate this template structure during edits. Rigid schema + audit checks prevent formatting drift. LLMs left to themselves drift; the template is the guardrail.

### Per-handoff grooming (~2 min, mandatory for M+)
<!-- scope: meta -->

Browser 1 (departing) runs at handoff generation:

1. Read current BACKLOG.md state
2. Mark stale items (no progress in 3+ sessions) for review
3. Prune obvious dead items (completed, no longer relevant)
4. Add new items surfaced this session
5. Update Status on completed items to `done`
6. Future State in handoff references BACKLOG items by stream + title (pointers, not copy-paste)

Light P1 items MAY be copy-pasted inline into Future State (acceptable at P1 only — Council Risk #2 mitigation).

### Quarterly deep grooming (~30 min, scheduled)
<!-- scope: meta -->

Rob reviews full BACKLOG once per quarter (first review: 2026-07-01):

1. Archive all `done` items to `BACKLOG-archive/YYYY-Q{N}.md`
2. Re-prioritize P1/P2/P3 based on current ecosystem state
3. Remove items that no longer align with VISION
4. Groom each stream: still active? Items still actionable?

**Write-only graveyard prevention:** speculative or distant ideas route to VISION.md, not BACKLOG.md. Strict curation — actionable items only.

### Split-brain prevention
<!-- scope: meta -->

BACKLOG.md is the single source of truth. Handoffs must NOT duplicate the pending queue:
- Handoff Future State (per ADR-37, Section 8) = which BACKLOG items THIS session targets — not a parallel queue
- ADR-32 v2.0 §4 "Pending — next session candidates": deprecated in favor of "Pending items: see BACKLOG.md" pointer

Browser 2 (incoming) at session start: read handoff Current + Future State → read BACKLOG.md for full context → validate Future State items against BACKLOG.md (drift check per ADR-37) → act on prioritized items.

Cross-refs: ADR-41, ADR-37 (Section 8), ADR-38 amendment A5 (universal baseline — BACKLOG mandatory every repo)

---

## 11. Evaluating a New Tool/Framework/Model
<!-- scope: hybrid -->

**Check maturity before investing time.** Fresh repos with <100 stars and v0.1 = too early.

### Quick eval checklist
<!-- scope: hybrid -->

1. GitHub stars, last commit date, release cadence
2. Does it solve a problem I actually have? (not "might have someday")
3. Does it integrate with my existing stack? (Python, Click, YAML config)
4. What does adoption cost? (learning curve, migration, dependencies)
5. Is there a simpler alternative I'm already using?

### Decision framework
<!-- scope: hybrid -->

- **Obvious yes:** Solves real pain, mature, good docs, easy to adopt → just do it
- **Maybe:** Interesting but not urgent → bookmark, revisit in 2 weeks
- **Council debate:** Would change architecture or replace an existing tool
- **Hard no:** Pre-v1, no community, solves a problem I don't have

---

## 12. Multi-Project Rules
<!-- scope: dev -->

**Package boundaries are sacred.** Projects/packages should never import directly from each other — they communicate via CLI subprocess, shared schema packages, or well-defined interfaces.

### Principles
<!-- scope: dev -->

- Designate one package as the **source of truth** for shared data models, taxonomy, naming, and validation. Other packages depend on it — never duplicate a schema.
- Orchestrator pattern: one central project calls others via subprocess or API. Tools stay stateless; the orchestrator owns state.
- Document the architecture in the project's CLAUDE.md, not here. This playbook covers methodology, not project-specific design.

### Config hierarchy (most specific wins)
<!-- scope: dev -->

```
~/.claude/CLAUDE.md              ← Global rules (all projects)
~/.claude/skills/gotchas/        ← Global traps
Dev/CLAUDE.md                    ← Workspace rules
Dev/{project}/CLAUDE.md          ← Project rules
Dev/{project}/packages/X/CLAUDE.md  ← Package rules
```

---

## 13. Where Knowledge Lives
<!-- scope: meta -->

**Three domains, three homes, zero overlap.** Council Decision #23 (2026-03-29, unanimous 4-0).

> See also "System Architecture" section — domains (this section) and layers (that section) are complementary frames.

| Domain                     | Location              | Tool                       | Purpose                                                  |
| -------------------------- | --------------------- | -------------------------- | -------------------------------------------------------- |
| Pre-sales work knowledge   | `ObsidianVault/`      | Obsidian                   | Clients, products, domains, competitive intel, demo prep |
| Dev practice methodology   | `Dev/.dev-knowledge/` | VS Code workspace          | How I build software: processes, lessons, setup state    |
| Claude Code runtime config | `~/.claude/`          | Claude Code auto-discovery | Rules, commands, hooks, agents, memory, gotchas          |

### "Where does this go?" decision rule
<!-- scope: meta -->

- Is it about a **client, product, or domain**? → Obsidian vault
- Is it about **how I work** (process, methodology, lesson learned)? → `.dev-knowledge/`
- Is it a **rule Claude Code must execute** (gotcha, verify check, command, hook)? → `~/.claude/`

### When a lesson becomes a rule
<!-- scope: meta -->

A lesson in LESSONS.md is human context (why, what happened). A rule in `~/.claude/` is machine-executable (verify: line, gotcha check). When a lesson matures into a rule:
1. Keep the lesson entry in LESSONS.md (provenance)
2. Add the rule to `~/.claude/rules/`, `gotchas.md`, or `learned-rules.md` with verify: line
3. Cross-reference both with file path

### Data sanitization
<!-- scope: meta -->

If a client engagement generates a dev lesson, strip all client names, proprietary schemas, and identifying details before writing to `.dev-knowledge/`.

### Migration triggers
<!-- scope: meta -->

- **`.dev-knowledge/` navigation overhead emerges** (cross-file search starts feeling slow; new files don't slot into an obvious folder) → evaluate creating a dedicated Obsidian DevVault
- **LESSONS.md becomes hard to navigate by topic** → split into topic files
- Rob opens Obsidian to search for dev methodology → immediate signal DevVault is needed

> Triggers, not caps. See LESSONS.md 2026-04-28 entry "Distinguish triggers from limits."

---

## 14. Markdown Governance
<!-- scope: dev -->

> **STALE — Handoff and Snapshots/reports rows.** Handoff row predates folder format; see `protocols/HANDOFF_PROCESS.md` v2.0 (folder convention per ADR-32). Snapshots/reports row's "delete after 90 days" lifecycle does not match practice (audits kept indefinitely). Substantive rewrite deferred to its own session.

**Every markdown file in the project falls into exactly one category.** If you're about to create a .md file and it doesn't fit any category below — it probably shouldn't exist.

| Category          | Location        | Naming                                         | Lifecycle                      |
| ----------------- | --------------- | ---------------------------------------------- | ------------------------------ |
| Project docs      | Root            | CLAUDE.md, README.md, CHANGELOG.md             | Living, never delete           |
| Decision records  | docs/decisions/ | ADR-{NN}_{topic}.md                            | Frozen, never edit             |
| Handoff           | docs/           | HANDOFF.md                                     | Living, update in place        |
| Snapshots/reports | docs/archive/   | {YYYY-MM-DD}_{TYPE}_{topic}.md                 | Frozen, delete after 90 days   |
| Eval data         | eval/           | eval_history.jsonl                             | Append-only, keep indefinitely |
| Ephemeral prompts | Not in repo     | PROMPT_{topic}.md                              | Delete after execution         |

**Two date rules, no exceptions:**
- Frozen/snapshot files → date in filename: `2026-03-28_CLEANUP_PLAN.md`
- Living files → date in YAML frontmatter: `last_updated: 2026-03-28`

### Project governance folder
<!-- scope: dev -->

Use `docs/` for project-level governance. Define its allowed contents in CLAUDE.md. Standard layout:

```
docs/
  HANDOFF.md                   ← living, update in place
  decisions/                   ← ADRs + Council transcripts, frozen
  archive/                     ← frozen snapshots, 90-day TTL
  staging/                     ← gitignored, disposable
```

Keep it tight. If something doesn't fit one of these categories, it goes somewhere specific — don't let `docs/` become a dumping ground.

---

## 15. Anti-Patterns — What NOT to Do
<!-- scope: hybrid -->

**"I'll organize later"** — If you create a file without knowing where it belongs, you'll never organize it. Know the category BEFORE creating.

**"Let's put it in docs/ for now"** — `docs/` is not a staging area. It has defined categories: handoff, archive, decisions. If it doesn't fit one, it doesn't belong there.

**"Let's name it descriptively"** — `ARCHITECTURE_REVIEW.md` is useless without a date. `2026-03-21_ARCHITECTURE_REVIEW.md` is findable.

**"We can consolidate these output folders later"** — Output dirs grow exponentially. Set a single canonical output path at project creation.

**"The AI will remember"** — It won't. Not after 4 hours. Not across sessions. Not after compaction. Write it down in CHANGELOG.md or CLAUDE.md.

**"We'll add tests later"** — Later never comes. Write the test stub before the implementation.

**"Let's rename/restructure everything"** — Every rename has blast radius (env vars, configs, DBs, venvs, caches). Never rename without full impact analysis FIRST, and never in the same session as feature work.

---

## The 10 Commandments
<!-- scope: hybrid -->

1. **CLAUDE.md first, code second.** Define the project before building it.
2. **Date everything.** Filename or frontmatter. No undated artifacts.
3. **Test after each change.** Not at the end. After EACH step.
4. **One home per file type.** Decisions → docs/decisions/. Reports → docs/archive/. No exceptions.
5. **Commit after each logical change.** Git status must be clean between tasks.
6. **Log changes continuously.** CHANGELOG entry when files change, LESSONS entry when something was learned.
7. **Scope is sacred.** 1-2 objectives per session. Everything else is backlog.
8. **Verify with Claude Code, plan with Claude.ai.** Don't let Claude.ai generate filesystem commands from memory.
9. **Output dirs are disposable.** Canonical location, gitignored, size-monitored, regularly cleaned.
10. **If the AI says "it's done" — verify.** The longer the session, the less you should trust it.

---

## 16. Cross-Tool Review
<!-- scope: dev -->

**When:** Feature branch touches 3+ files OR 2+ packages OR safety-critical paths (vault writes, OneDrive ops, cleanup/delete)
**Skip when:** Single-file fix, test-only changes, documentation updates

(Gated by change size and risk, above — not by any repo tier; the repo-tier system was deprecated 2026-05-23.)

### Review Tools
<!-- scope: dev -->

Two options for code review (A/B test both, then standardize):

**Option A — /ultrareview (Claude Code built-in):**
Cloud-based multi-agent review. Run without arguments (current branch) or with PR number. No second terminal needed.

**Option B — Codex CLI (automated, single command):**
`/codex-review <topic>` wraps `codex exec --output-last-message`. Produces dated, frontmatter-wrapped audit at `docs/audits/YYYY-MM-DD-codex-{topic}.md`. Read-only sandbox. Opt-in `-AutoCommit`. Requires ChatGPT Plus subscription. See `~/.claude/bin/codex-review.README.md`.

**Code-only rule (per-change codex-review):** codex-review is for code review, not markdown/prose. The wrapper enforces a path-guard against an extension allowlist (`.py .ps1 .sh .ts .tsx .js .jsx .go .rs .rb .java .cs .cpp .c .h .sql .toml .yaml .yml .json .ini`). Mixed diffs are filtered to the code subset before invoking codex. Markdown-only or empty diffs exit cleanly without invoking codex. Mechanically enforced in `~/.claude/bin/codex-review.ps1`.

Both satisfy S15 review requirement. Choose based on quality of findings after 2-week A/B test.

Codex/ultrareview reviews. Claude Code builds. Never reverse the roles.

**Codex reviewer config:** The global reviewer config (role, checklist, output format) lives at `~/.codex/AGENTS.md`; canonical source tracked in `.dev-knowledge/codex/AGENTS.md` (ADR-54). Per-repo `AGENTS.md` adds only repo-specific rules — it does not repeat the global config.

---

## 17. Code Quality Audit Process
<!-- scope: dev -->

**When:** Periodic full audit (cadence by repo complexity — larger/more-active repos more often) · On-demand before major refactors · a tiny single-script repo may skip entirely. Judgment call, not tier-gated.
**Tool:** Codex CLI or Codex Desktop (independent reviewer — no authorship bias)
**Cycle:** Read-only audit → triage by severity → fix by severity → re-audit

**Scope distinct from per-change codex-review:** the monthly full-repo audit is deliberately whole-repo (within `src/`) and is **unchanged** by the per-change diff-scoping rules in §16. The code-only path-guard applies here too (no review of markdown files inside `src/`), but the audit's whole-`src/` scope is preserved.

### Severity tiers
<!-- scope: dev -->
- **CRITICAL** — data loss, security, broken imports that fail at runtime
- **HIGH** — wrong dependency direction, missing tests on public API, type errors
- **MEDIUM** — style violations, redundant code, unclear naming
- **LOW** — suggestions, nitpicks, debatable patterns

### Process
<!-- scope: dev -->
1. Run audit (read-only): `codex "Audit this repo against CLAUDE.md rules. Output findings by severity. Do not fix anything."`
2. Triage output manually — expect ~30% false positives. Demote miscalibrated patterns in CLAUDE.md.
3. Fix CRITICAL and HIGH first. One commit per logical group.
4. Re-run audit. Confirm flags resolved.
5. Update ARCHITECTURE.md if module boundaries or dependency direction changed.

### Rules
<!-- scope: dev -->
- Audit-first, fix-second. Never fix while auditing.
- Claude Code fixes. Codex audits. Never reverse the roles.
- Structural changes with N>5 call sites: shim first, migrate incrementally, remove shim last.
- Any session touching module boundaries must produce or update ARCHITECTURE.md (mandatory every repo per ADR-51 as amended 2026-05-23).

### Post-Structural-Change Documentation
<!-- scope: dev -->

After any change that moves, renames, or reorganizes files or modules, update documentation that describes the changed structure:

- Always update `ARCHITECTURE.md` (mandatory every repo per ADR-51 as amended 2026-05-23).
- On a larger repo, also update affected module READMEs under `src/*/`.

This is not optional. Stale structural documentation is worse than no documentation — it actively misleads.

---

## 18. Ecosystem Audit Tool Workflow
<!-- scope: meta -->

`scripts/audit.py` is the ecosystem conformance checker per [ADR-36](docs/decisions/ADR-36-audit-tool-architecture.md). It reads child repos under `Dev/` and writes only to `.dev-knowledge` paths — never touches child repo files. Audit is advisory: findings surface non-compliance; remediation is manual.

Cross-refs: [ADR-31](docs/decisions/ADR-31-authority-model.md) (authority model), [ADR-36](docs/decisions/ADR-36-audit-tool-architecture.md) (tool architecture), [ADR-33](docs/decisions/ADR-33-vision-md-standard.md) (VISION.md), [ADR-38](docs/decisions/ADR-38-repo-architecture-baseline.md) (ADR-38 baseline), [ADR-53](docs/decisions/ADR-53-claude-md-canonical.md) (CLAUDE.md canonical)

### Active checks
<!-- scope: meta -->

Three checks active as of commit `deedc10` (P2 checks `backlog_organization` and `dated_entries_*` were removed in that trim; this documents current state):

| Check | ADR | What it verifies | FAIL | WARN | PASS |
|---|---|---|---|---|---|
| `vision_md` | ADR-33 (amended 2026-05-23) | VISION.md exists at repo root with valid YAML frontmatter containing `version`, `last_reviewed`, `owner`, `status` (tier/scale removed) | absent or frontmatter unparseable | frontmatter valid but missing required keys | all required keys present |
| `adr38_baseline` | ADR-38 (A5, 2026-05-23) | universal governance baseline at repo root: `VISION.md`, `ARCHITECTURE.md`, `BACKLOG.md` present (README optional; src/tests/pyproject not checked — governance baseline, not code-structure) | any required item missing | — | all present |
| `claude_md` | ADR-53 | CLAUDE.md exists at repo root and is non-empty | absent or empty | — | present with content |

### CLI commands
<!-- scope: meta -->

Invoke via:

```
python scripts/audit.py <command>
```

**`health`** — pre-flight check, no file writes. Verifies `click` and `pyyaml` importable, `ecosystem/` directory exists, at least one repo registered. Exits 0 on OK, 1 on DEGRADED.

```
python scripts/audit.py health
```

Example output:
```
  [OK] click importable
  [OK] pyyaml importable
  [OK] ecosystem/ exists
  [OK] repos registered  (['ai-council', '.dev-knowledge'])
health: OK
```

**`run`** — full ecosystem audit. Runs all checks on every registered repo, saves `state.yaml`, appends to `history/YYYY-MM-DD.md`, writes report to `docs/audits/`. Exits 1 if any check fails.

```
python scripts/audit.py run
```

Bootstrap a not-yet-registered repo in the same pass (creates `state.yaml` first, then runs):

```
python scripts/audit.py run --repo-path ../corp-monorepo
```

**`repo <name>`** — audit a single repo by name. Same state/history/report writes as `run`, but scoped to one repo. Report saved as `docs/audits/YYYY-MM-DD-{name}-audit.md`.

```
python scripts/audit.py repo ai-council
```

Override path (bootstrap or ad-hoc):

```
python scripts/audit.py repo corp-monorepo --repo-path ../corp-monorepo
```

**`registry update`** — regenerate `ecosystem/index.yaml` from current `state.yaml` files. Run after manually adding or removing `ecosystem/<name>/state.yaml`. No audit checks run; no reports written.

```
python scripts/audit.py registry update
```

### ecosystem/ folder layout
<!-- scope: meta -->

```
ecosystem/
├── .dev-knowledge/
│   ├── state.yaml          ← current audit state for this repo
│   └── history/
│       └── YYYY-MM-DD.md   ← append-only per-day log (multiple runs append headers)
└── ai-council/
    ├── state.yaml
    └── history/
        └── YYYY-MM-DD.md
ecosystem/index.yaml        ← derived rollup (regenerated by `registry update`)
docs/audits/
└── YYYY-MM-DD-ecosystem-audit.md   ← full-run report
└── YYYY-MM-DD-{name}-audit.md      ← single-repo report
```

`state.yaml` holds the repo's last audit result (name, path, last_audit date, findings list). `history/YYYY-MM-DD.md` is append-only: each run appends a `## YYYY-MM-DD — <timestamp>` header + findings table. Multiple runs on the same day produce multiple headers in the same file.

`ecosystem/index.yaml` is a rollup snapshot; it is derived and regenerated on demand — do not edit manually.

### ecosystem/index.yaml — rollup index
<!-- scope: meta -->

`ecosystem/index.yaml` is the audit infrastructure's aggregate index. It consolidates the last-known state of every registered repo into a single file, giving operators (and future tooling) a quick read on ecosystem health without opening per-repo `state.yaml` files.

**Path:** `ecosystem/index.yaml` — nested inside the `ecosystem/` folder (moved from root 2026-05-24, root hygiene pass 2).

**Schema:**

| Field | Type | Description |
|---|---|---|
| `generated` | ISO 8601 timestamp string | When `registry update` last ran (e.g. `2026-05-23T14:32:07`) |
| `repos` | list of repo entries | One entry per registered repo |
| `repos[].name` | string | Repo name (matches `ecosystem/<name>/` folder) |
| `repos[].path` | string | Absolute filesystem path stored at registration time |
| `repos[].last_audit` | ISO date string or `null` | Date of last `run`/`repo` invocation; `null` if never audited |
| `repos[].findings` | list of finding entries | Findings from last audit pass |
| `repos[].findings[].check_name` | string | Check identifier (e.g. `vision_md`, `adr38_baseline`, `claude_md`) |
| `repos[].findings[].status` | string | `pass` \| `fail` \| `warn` \| `unavailable` |
| `repos[].findings[].evidence` | string | Human-readable explanation of the check result |

**Example (3-repo ecosystem):**

```yaml
generated: '2026-05-23T14:32:07'
repos:
- findings:
  - check_name: vision_md
    evidence: 'VISION.md present; frontmatter keys: [...]'
    status: pass
  - check_name: adr38_baseline
    evidence: All ADR-38 universal governance baseline files present
    status: pass
  - check_name: claude_md
    evidence: CLAUDE.md present (4821 chars)
    status: pass
  last_audit: '2026-05-23'
  name: .dev-knowledge
  path: C:\Users\1028120\Documents\Dev\.dev-knowledge
- findings:
  - check_name: vision_md
    evidence: 'VISION.md present; frontmatter keys: [...]'
    status: pass
  - check_name: adr38_baseline
    evidence: All ADR-38 universal governance baseline files present
    status: pass
  - check_name: claude_md
    evidence: CLAUDE.md present (3102 chars)
    status: pass
  last_audit: '2026-05-23'
  name: ai-council
  path: C:\Users\1028120\Documents\Dev\ai-council
- findings:
  - ...
  last_audit: '2026-05-23'
  name: corp-monorepo
  path: C:\Users\1028120\Documents\Dev\corp-monorepo
```

**Generation:** `python scripts/audit.py registry update` reads every `ecosystem/<name>/state.yaml` that exists, merges them into the index structure, and writes `ecosystem/index.yaml`. Implementation: `audit.py` `cmd_registry` + `regenerate_index()`.

**Maintenance policy:** Do not edit `ecosystem/index.yaml` manually. `registry update` overwrites the entire file on each invocation — manual edits will be silently lost on the next run. The per-repo `state.yaml` files are the source of truth; the index is always derivable from them.

**When it is written:**
- After `registry update` (explicit invocation — the only write path)
- It is NOT written automatically by `run --repo-path` or `run` or `repo` commands
- It is NOT written by `health`

**Relationship to state.yaml:** `ecosystem/index.yaml` is a derived rollup; `ecosystem/<name>/state.yaml` is the source of truth per repo. If the index is lost or corrupted, `registry update` regenerates it completely from the state.yaml files. The reverse is not true — state.yaml cannot be reconstructed from the index alone.

**Additional `registry update` behavior:** does not run any audit checks, does not write history files, does not generate reports. It is a pure read-from-state-yaml → write-index operation.

### Registering a new repo
<!-- scope: meta -->

Registration means creating `ecosystem/<name>/state.yaml`. Two paths:

**Option A — bootstrap via `run --repo-path`** (preferred for first audit):

```
python scripts/audit.py run --repo-path ../corp-monorepo
python scripts/audit.py registry update
```

Step 1 (`run --repo-path`) creates `ecosystem/corp-monorepo/state.yaml`, runs all checks, writes history + report, and permanently registers the repo for subsequent `run` invocations. It does **not** update `ecosystem/index.yaml`.

Step 2 (`registry update`) regenerates `ecosystem/index.yaml` from all current `state.yaml` files. Required after any new registration to keep the rollup index current (see `ecosystem/index.yaml — rollup index` subsection below).

**Option B — manual state.yaml creation**, then `registry update`:

1. Create `ecosystem/<name>/` directory.
2. Create `ecosystem/<name>/state.yaml` with at minimum:
   ```yaml
   name: corp-monorepo
   path: /absolute/path/to/corp-monorepo
   last_audit: null
   findings: []
   ```
3. Run `python scripts/audit.py registry update` to regenerate `ecosystem/index.yaml`.
4. Run `python scripts/audit.py repo corp-monorepo` to perform first audit.

**Verify registration:**

```
python scripts/audit.py health
```

The repos line should list the new name. If not, check that `ecosystem/<name>/state.yaml` exists.

**Path note:** `state.yaml` stores the absolute path used at registration time. If the repo moves, update the `path:` field in `state.yaml` manually or re-register with `--repo-path`.

### Interpreting audit reports
<!-- scope: meta -->

Each report in `docs/audits/` is a markdown file. Per-repo section structure:

```
## {repo-name} — PASS|FAIL|UNAVAILABLE

| Check | Status | Evidence |
|---|---|---|
| `vision_md` | PASS | VISION.md present; frontmatter keys: [...] |
| `adr38_baseline` | FAIL | Missing required: ['src', 'pyproject.toml'] |
| `claude_md` | PASS | CLAUDE.md present (N chars) |
```

**Status values:**
- `PASS` — check fully satisfied
- `WARN` — partial compliance (e.g. missing optional keys, missing optional files)
- `FAIL` — check condition not met; requires remediation
- `UNAVAILABLE` — repo path not found on filesystem (stale registration or path moved)

Repo-level summary: `FAIL` if any check is FAIL; `UNAVAILABLE` if path not found; `PASS` otherwise. `run` exits 1 if any failure across all repos.

Audit is read-only and advisory. Findings are remediated manually in the child repo by its operator — audit.py never modifies child repo files.

History in `ecosystem/<name>/history/YYYY-MM-DD.md` preserves per-run findings indefinitely (append-only). Reports in `docs/audits/` are point-in-time files; do not edit manually (header: `*Report generated by scripts/audit.py. Do not edit manually.*`).

### Troubleshooting
<!-- scope: meta -->

**`health: DEGRADED` — `[!!] repos registered  (none)`**
No `ecosystem/<name>/state.yaml` files found. Register at least one repo (see above).

**`health: DEGRADED` — `[!!] ecosystem/ exists`**
The `ecosystem/` directory is missing. Create it: `mkdir ecosystem`.

**`health: DEGRADED` — click or pyyaml not importable**
Dependencies missing. Install: `pip install click pyyaml` (or per `pyproject.toml` if present).

**`UNAVAILABLE` finding in report**
The path stored in `ecosystem/<name>/state.yaml` doesn't exist. Update `path:` in `state.yaml` to the current absolute location, then re-run.

**Known self-compliance gap:** `.dev-knowledge` itself FAILs `adr38_baseline` on every self-audit because it has no `src/` directory or `pyproject.toml` (it is a documentation repo, not a Python package). This is expected and tracked in BACKLOG Stream C P2. Operators running `run` will see `.dev-knowledge — FAIL` and exit code 1 as a result; this is not a tool bug.

---

## 19. Scrum-Master Review Propagation
<!-- scope: meta -->

**When:** `.dev-knowledge` (or any ecosystem-meta repo) audits a target repo against universal conventions (ADR-34 naming, ADR-38 architecture, ADR-41 backlog, etc.) and finds non-conformities to route. Distinct from § 15 Cross-Tool Review (within-repo Codex audit) and § 16 Code Quality Audit Process (within-repo audit cycle).

**Skip when:** target repo audits itself internally (no cross-repo routing needed).

### Three-stage flow
<!-- scope: meta -->

**Stage 1 — Audit (strażnik produces report)**

- Strażnik (`.dev-knowledge` or other ecosystem-meta repo) runs read-only audit against target repo's working tree against universal conventions.
- Produces dated artifact: `docs/audits/YYYY-MM-DD-<target-repo>-scrum-master-review.md`
- Findings grouped by severity (CRITICAL / HIGH / MEDIUM / LOW per § 16 convention).
- Audit is internal to strażnik repo; not yet routed.

**Stage 2 — Route (operator routes with cover letter)**

- Operator copies `templates/scrum-master-cover-letter.md`, fills placeholders, pastes cover letter + audit report contents to target repo architect (separate chat or browser session).
- Cover letter sets expectation: single round trip, architect implements in own repo, no delivery turn back.

**Stage 3 — Implement (target architect produces changes in own repo)**

- Target repo architect reviews findings and implements changes in target repo.
- Implementation evidence: commits + CHANGELOG entry in target repo. No browser-to-browser turn back to strażnik expected.
- Strażnik may verify (read-only) target repo CHANGELOG / commits at next session start — informational, not gated.

### Addendum mechanism
<!-- scope: meta -->

If strażnik catches additional gaps after Stage 2 routing (audit gaps surfaced post hoc), produce a supplementary artifact rather than regenerating the full report:

- Naming: `docs/audits/YYYY-MM-DD-<target-repo>-scrum-master-review-addendum.md`
- Content: supplemental findings only; references the original audit by name.
- Routing: operator routes addendum alongside (or shortly after) the main cover letter.
- Addendum supplements; it does not supersede.

**Empirical reference:** ai-council scrum-master review 2026-05-11 produced 10 findings + addendum covering I7 (tasks/lessons.md location accepted-as-by-design) and I8 (underscore-prefix archive folder not flagged for rename). Addendum mechanism prevented full report regeneration.

### Distinction from cross-repo amendment handshake
<!-- scope: meta -->

| Aspect | Cross-repo amendment handshake (ADR-43 pattern) | Scrum-master review propagation (this section) |
|--------|--------------------------------------------------|------------------------------------------------|
| Nature | **Bilateral** — shared concern across two repos | **Unilateral** — strażnik recommends, target implements |
| Initiator | Either repo (concern emerges) | Strażnik repo (audit surfaces non-conformity) |
| Round trips | 1 (per "handshake = 1 round trip" principle) | 1 (per same principle) |
| Pushback handling | Continues in same handshake | Opens new conversation as separate handshake |
| Empirical example | ADR-34 propagation to ai-council 2026-05-11 | ai-council scrum-master review 2026-05-11 |

### Single-round-trip framing
<!-- scope: meta -->

Both patterns share the operator principle "handshake = 1 round trip". Cover letter explicitly states no Turn 2/3/4 expected. If target architect pushes back on a finding (disagreement, scope mismatch, by-design justification):

- Pushback does NOT continue the original routing thread.
- Pushback opens a **new conversation** framed as a separate handshake.
- Multi-turn ceremony for S-scale findings = over-engineering (per BOUNDARY in 2026-05-12 handoff: "do NOT generate multi-turn handshake ceremony for S-scale cross-repo changes").

### Cover-letter template
<!-- scope: meta -->

Use `templates/scrum-master-cover-letter.md`. Operator fills placeholders for target repo, review type, severity counts, top-3 findings, expected-response framing. Template cites first empirical instance (ai-council 2026-05-11) as reference.

### Rules
<!-- scope: meta -->

- Audit before route; never route before audit completes.
- Strażnik produces; operator routes; target architect implements. Never reverse roles.
- Strażnik does NOT directly edit target repo files. Cross-repo changes route via target architect.
- Pushback opens new handshake. Pushback does not extend the original routing.
- Addendum is for post-routing gap discovery; not for finding revisions (revisions = re-audit).

### Section history
<!-- scope: meta -->

- v1.0 (2026-05-12) — initial. Codifies propagation process at N=1 (ai-council scrum-master review 2026-05-11). ADR-44 authority codification deferred pending N=2 (corp-monorepo scrum-master review).

---

## Appendix A: Claude Code Shortcuts
<!-- scope: runtime -->

### Permission Modes (Shift+Tab cycles)
<!-- scope: runtime -->

- **Default** — asks permission for everything. For sensitive/unfamiliar work.
- **Accept Edits** (Shift+Tab x1) — auto-saves files, asks before shell. **Daily driver.**
- **Plan Mode** (Shift+Tab x2) — read-only. Use when you don't know the approach.

### Keyboard
<!-- scope: runtime -->

| Shortcut  | What it does                        |
| --------- | ----------------------------------- |
| Shift+Tab | Cycle permission modes              |
| Esc Esc   | Rewind/undo to previous checkpoint  |
| Alt+T     | Toggle extended thinking            |
| Alt+P     | Switch model                        |
| Ctrl+C    | Stop generation                     |
| Ctrl+L    | Clear terminal screen (not session) |
| Ctrl+G    | Open prompt in external editor      |
| Ctrl+V    | Paste image                         |

### Slash Commands
<!-- scope: runtime -->

| Command            | When to use                                       |
| ------------------ | ------------------------------------------------- |
| `/boot`            | Session start — load memory, verify rules         |
| `/clear`           | Between repos/tasks — #1 token saver              |
| `/compact`         | Mid-session when context heavy                    |
| `/compact [focus]` | Compress with focus ("focus on API changes")      |
| `/evolve`          | Weekly Friday — review corrections, promote rules |
| `/session-summary` | Before switching to Claude.ai browser             |
| `/stats`           | Check token usage (interactive TUI; use `ccusage --json` for scriptable export) |
| `/plan [prompt]`   | One-shot plan mode without cycling Shift+Tab      |
| `/model`           | Change model mid-session                          |
| `/effort`          | Change effort level                               |
| `/context`         | See what's using context window                   |
| `/resume`          | Resume previous session                           |

### CLI Flags
<!-- scope: runtime -->

```
claude --permission-mode plan      # start in plan mode
claude --permission-mode acceptEdits  # start in accept edits
claude -p "prompt"                 # headless non-interactive
claude -r "session-name"           # resume named session
```

### The ! Prefix
<!-- scope: runtime -->

Type `!` before any command to run it directly in shell without Claude processing:
```
!git status          # output goes to context, zero AI tokens
!pytest -x --tb=short  # see test results without asking Claude to run them
!cat src/config.py   # show file to Claude without a read request
```
Use for quick checks where you don't need Claude to interpret — just inject output into context.

---

## Appendix B: Model Routing Table
<!-- scope: llm -->

From ~/.claude/ROUTING.md — deterministic, no judgment calls.

| Task                              | Model          | Examples                                                           |
| --------------------------------- | -------------- | ------------------------------------------------------------------ |
| No AI needed                      | —              | .gitignore edits, git ops, file moves, config tweaks (<60s manual) |
| Reports, snapshots                | Haiku subagent | Test summaries, doc condensation, ecosystem snapshots              |
| Implementation, debugging, review | Sonnet         | All code review (security boundary), test creation, refactoring    |
| Architecture, cross-repo design   | Opus           | Ecosystem reasoning, complex debugging, novel logic                |
| Large doc extraction              | Gemini Flash   | Domain-specific extraction pipelines (PPTX/MP4/PDF)                |
| Council synthesis                 | Gemini         | Cost: $0.04 vs Claude $0.23/debate                                 |

### Time-Shifting Schedule
<!-- scope: llm -->

| CET Time    | Activity                           | Rationale                                                         |
| ----------- | ---------------------------------- | ----------------------------------------------------------------- |
| 08:00-09:00 | Planning in Plan Mode (Opus)       | Fresh mind + off-peak ET                                          |
| 09:00-13:00 | Heavy implementation (Opus/Sonnet) | Off-peak ET (3-7AM). Golden window.                               |
| 13:00-14:00 | Break                              | Before peak begins                                                |
| 14:00-20:00 | Light work only                    | Peak ET. Code review (Sonnet), Haiku reports, manual coding, docs |
| 20:00-22:00 | Optional overflow                  | Off-peak resumes. Only if energy allows                           |

---

## Appendix C: Token Optimization Techniques
<!-- scope: llm -->

Ranked by impact/effort (Council-approved):

1. **`/clear` between tasks/repos** — 30-40% input tokens saved. Highest leverage. Build the habit.
2. **Front-load full spec** in first message — eliminates 2-3 discovery turns (15-25% fewer round-trips). Use prompt template from Section 2.
3. **Plan Mode before implementation** — catches bad approach at 200 tokens vs 5000.
4. **Line-range reads** `@file:15-80` — 10-15% savings on read-heavy sessions. Know your codebase.
5. **ROUTING.md enforcement** — Haiku for reports, no AI for trivial edits (15-20% total).
6. **`/compact` at task boundaries** — 12-18% context savings. Config: compaction at 40%.
7. **Batch related changes** in single prompt — fewer turns = less context repetition.
8. **VS Code first** — test explorer, Error Lens, GitLens = 0 tokens for informational queries.
9. **`!` prefix for quick commands** — `!git status`, `!pytest` run directly in shell, output goes to context without Claude processing. Zero AI tokens for simple checks.

### Golden Rule
<!-- scope: llm -->

**After 2 failed attempts at something → `/clear` and rewrite the prompt from scratch.** A fresh context with a clear prompt almost always works better than a polluted context full of failed approaches. Don't keep hammering — reset.

### CLAUDE.md size limit
<!-- scope: runtime -->

Keep CLAUDE.md under 200 lines per file. Instruction adherence drops above that. Use `.claude/rules/` for domain-specific rules and `.claude/skills/gotchas/` for institutional memory — these load separately and don't bloat the main prompt.

---

## Codemap workflow
<!-- scope: meta -->

The codemap section of every M/L `ARCHITECTURE.md` is an auto-generated embedded Mermaid block showing the repo's top-level Python packages, their import relationships, and their layer assignments (if `tach.toml` is present). VS Code 1.121 and GitHub render Mermaid natively — the diagram is clickable and navigable without a separate SVG pipeline. Governing authority: ADR-51 Decision 6 + amendment 2026-05-22.

### When the generator runs
<!-- scope: meta -->

A pre-commit hook (`codemap-freshness`) fires whenever Python source files, `pyproject.toml`, `tach.toml`, or `ARCHITECTURE.md` itself change. If the committed codemap block differs from a fresh generation, the hook exits non-zero and blocks the commit. The operator runs `generate --write` and re-stages `ARCHITECTURE.md` before retrying. The generator can also be invoked manually at any time for inspection.

### Manual invocation
<!-- scope: meta -->

```bash
# Dry-run — print generated Mermaid block to stdout (does not modify ARCHITECTURE.md)
python -m scripts.codemap.cli generate . --source-root <path>

# Write — replace CODEMAP-bounded region in ARCHITECTURE.md in place
python -m scripts.codemap.cli generate . --source-root <path> --write

# Check freshness — exit non-zero + unified diff if committed block is stale
python -m scripts.codemap.cli check . --source-root <path>
```

Default `--source-root` is `src/`. Repos with non-standard layout supply an explicit override:
- `.dev-knowledge` uses `scripts/` → `--source-root scripts`
- corp-monorepo uses `src/` → default applies

### Edge case handling
<!-- scope: meta -->

**Orphan modules** (zero in/out edges): the generator assigns the `:::orphan` class (dashed border) and emits a stderr warning. Investigate whether the package is legitimately unused (deletion candidate) or has runtime-only invocation (re-classification candidate). Orphans do not block commit.

**Circular dependencies**: nodes in the cycle get `:::cycle` class (red border); edges in the cycle are styled red. A circular dependency is an architectural smell — investigate import structure; common resolution is to extract a shared interface to a foundation layer.

**Missing `tach.toml`**: generator degrades gracefully — codemap is generated without layer color assignments. No warning emitted. Adding `tach.toml` post-hoc and re-generating restores layer colors.

**Missing `ARCHITECTURE.md` or CODEMAP markers**: generator fails with an operator-actionable error. Resolution: create `ARCHITECTURE.md` from `templates/ARCHITECTURE-template.md`, ensure both `<!-- CODEMAP:START -->` and `<!-- CODEMAP:END -->` markers are present, then re-run.

### Per-repo opt-in checklist
<!-- scope: meta -->

For an M/L repo to adopt generator-based codemap maintenance:

1. **Template instantiation.** Ensure `ARCHITECTURE.md` exists at repo root and contains `<!-- CODEMAP:START -->` and `<!-- CODEMAP:END -->` marker comments in the `## Codemap` section.
2. **Hook entry.** Add a local hook entry to `.pre-commit-config.yaml`:
   ```yaml
     - repo: local
       hooks:
         - id: codemap-freshness
           name: Codemap freshness check
           entry: python -m scripts.codemap.cli check . --source-root <path>
           language: system
           files: '(\.py$|^pyproject\.toml$|^tach\.toml$|^ARCHITECTURE\.md$)'
           pass_filenames: false
   ```
   Replace `<path>` with the repo's source root (`src` by default; override as needed).
3. **First generation.** Run `python -m scripts.codemap.cli generate . --source-root <path> --write` and inspect the diff.
4. **Commit.** Stage `ARCHITECTURE.md` and commit — the hook should now pass on all future relevant changes.

Authority reference: ADR-51 amendment 2026-05-22 § Per-repo adoption — opt-in, not mandatory.

### Troubleshooting
<!-- scope: meta -->

**Freshness check blocks an unrelated commit:** the hook fires on Python source changes even when the developer didn't intend to change the codemap. Run `generate --write` first, then retry the commit.

**Non-deterministic output across runs:** sort order, locale, or file encoding drift. Check that file discovery uses a sorted glob and that the generator's output is locale-independent. The codemap generator uses sorted package discovery to ensure determinism.