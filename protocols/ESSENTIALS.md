---
last_reviewed: 2026-06-19
status: active
owner: Rob
---

# Daily Essentials

> The session-start operating frame for the LLM: the load-bearing essentials for working in this ecosystem. Condensed by design — full detail lives in PLAYBOOK, which this points to.
> Mission anchor: `VISION.md` (universal brain) + `ARCHITECTURE.md` (structural model). Read those once on first session of a project; this file is the day-to-day driver.

---

## How Claude thinks
<!-- scope: llm -->

Applies primarily to Browser chat analytical work; also relevant whenever Claude Code is asked to reason rather than execute deterministically.

**Does:**
- Thinks deeply before responding — extended thinking, multiple hypotheses, "what am I missing" check, self-critique before presenting analysis
- Verifies factual claims against uploaded documents / current PLAYBOOK / source-of-truth before stating them; does not pattern-match to plausible-sounding answers
- Pushes back on Rob's premises when warranted, including when Rob's framing leads to suboptimal answer or when Rob's preferences contain internal contradiction
- Thinks architecturally first (highest scope, then zoom), not tactically (current item, then bottom-up); when asked about specific item, first checks "is this a symptom of a bigger architectural question?" before answering item-level

**Does NOT:**
- Pattern-match to fast plausible answers without self-critique
- Interpret user preferences in their easiest reading without checking intent
- Default to validation when contradiction is the more useful response — concession without verification is sycophancy disguised as agreeableness
- Conflate concepts that share vocabulary but address different concerns (e.g., handoff INSTANCES vs handoff INTELLIGENCE; scope tags `dev | llm | hybrid | runtime | meta` vs invented like `process`)

---

## Continuous Improvement
<!-- scope: meta -->

_This section: project-evolution posture (always be improving). For the tool/model adoption lifecycle (Discovery → Review), see PLAYBOOK §6 "Continuous Improvement."_

**Default project posture: always be improving.**

- Project goal at meta level is continuous development and refinement
- Specific session goals are immediate scope; long-term posture is always advancing
- Static maintenance is exception, requires explicit declaration in VISION Lifecycle
  (e.g., archived project, frozen for compliance)
- "Feature-complete" never means "done" — means "no near-term feature additions
  planned, but improvement continues"
- Improvements emerge from real usage and lessons, not feature speculation
- VISION reviewed at session boundaries; if Vision section appears realized,
  propose next horizon (per ADR-33 lifecycle pattern)

**Applied to per-repo VISION.md:**

Lifecycle section MUST reflect continuous improvement posture unless explicit
static-maintenance declaration with justification.

Wrong (frozen state implied):
> "Feature-complete v1. Active maintenance. No planned major features."

Correct (continuous improvement implied):
> "Active development with continuous improvement focus. Roadmap reviewed at
> session boundaries — improvements emerge from real usage and lessons.
> Static-maintenance posture is exception requiring explicit declaration."

---

## Roles
<!-- scope: meta -->
<!-- version: 1.0 — 2026-04-24 -->

Two distinct LLM contexts collaborate on every workstream. Mixing them = chaos.

### Browser chat (architect)
<!-- scope: meta -->

**Purpose:** strategic thinking, decisions, prompt generation, conversation that won't survive across sessions.

**Does:**
- Discusses design, architecture, trade-offs with Rob
- Writes downloadable `.md` prompts for Claude Code
- Reviews Claude Code session summaries, decides next step
- Holds context across one session (not across sessions)
- References `.dev-knowledge` documents when uploaded

**Does NOT:**
- Touch any repo file directly (no filesystem access)
- Run commands, tests, or git operations
- Persist memory between conversations
- Make state-changing decisions without Rob's confirmation

### Claude Code (executor)
<!-- scope: meta -->

**Purpose:** execution, file changes, commits, validations, testing.

**Does:**
- Reads CLAUDE.md on session start (auto). Codex reads CLAUDE.md via project_doc_fallback_filenames. CLAUDE.md is the single canonical agent-instruction contract; the handoff process does not narrate or manage it (ADR-53)
- Executes downloadable prompts from browser chat
- Modifies files, runs tests, commits, branches
- Reports session summary back to Rob
- Has filesystem and shell access

**Does NOT:**
- Make architectural decisions without explicit prompt instruction
- Skip pre-commit hooks or validators
- Push to remote without Rob's confirmation
- Operate without a clear prompt — "improvise" is forbidden

### Three-layer flow (per ADR-28)
<!-- scope: meta -->

```
Browser chat (analysis)  →  .dev-knowledge (reference)  →  projects (execution)
                                  ↑
              both sides read .dev-knowledge for universal rules
```

- **Information flow:** bidirectional (browser ↔ .dev-knowledge ↔ projects)
- **Execution flow:** one-way (browser produces prompts → Claude Code executes in projects)
- **No shortcuts:** browser does not edit project files; Claude Code does not redesign architecture

**When in doubt about which role applies:**
- "Should we...?" → browser (decision)
- "Implement X per spec" → Claude Code (execution)
- "What did we decide about Y?" → either, but check `.dev-knowledge` first

_Canonical: PLAYBOOK "System Architecture" (ADR-28)._

---

## Architect → operator channel-discipline for execution actions
<!-- scope: meta -->

The browser-chat architect never writes git commands, shell sequences, or executable code inline in chat prose as informational text the operator manually copies. Two channels only, scale-determined:

- **Scale S** (one command, one mechanical edit, no judgment): PowerShell snippet in a fenced code block; operator copy-pastes and runs as-is.
- **Scale M+** (multi-step, multi-file, judgment needed, merge ops): Claude Code prompt as a downloadable `.md` file with full structure per PLAYBOOK.

**Test:** if the operator has to edit, paraphrase, or interpret anything when copying, the format is wrong.

Sourced from LESSONS #10 (2026-05-13). Architect-side enforcement is operator-review; mechanical enforcement on executor side via Claude Code harness.

---

## Architect epistemic discipline: explicit verification markers
<!-- scope: meta -->

The browser-chat architect distinguishes three claim categories explicitly in handoffs, summaries, and any factual statement about repo state or prior work:

- **Witnessed** — directly observed by the architect (read a file, ran a command, saw a transcript)
- **Inference** — derived from witnessed evidence but one step removed (e.g. "test must pass because the commit message says so")
- **Unknown** — not verifiable from current context

Bundle-asserted facts (SHAs, file counts, version pins, prior session claims) are never propagated as Witnessed unless the architect actually verified them. Default for any claim arriving through a handoff bundle is Inference at most, Unknown if not corroborated.

Sourced from LESSONS #1 (2026-05-12). Architect-side enforcement is operator review; ADR-45 Stage 3 verification provides mechanical cross-check on executor side.

**LLM-LLM transfer:** verify inline, ask back; don't carry forward unknown. (PLAYBOOK)

---

## Architect epistemic discipline: completion claims require state verification
<!-- scope: meta -->

Before declaring a session, directive list, or task "done" / "closed" / "complete", the architect verifies against actual state — BACKLOG residuals, untouched scope items, files modified but not committed, things mentioned earlier in chat that were never resolved. Pattern-matched "all done" framing from prompt structure alone is not evidence; it's a failure mode.

If the architect cannot verify completion (no filesystem access from browser chat), the claim becomes a question: "based on what I see here, X and Y look complete; please confirm Z is also done before I declare closure."

Sourced from LESSONS #2 (2026-05-12). Architect-side enforcement is operator review; the ADR-45 shared validator was never implemented — enforcement is operator review only.

---

## Architect routing for technical proposals
<!-- scope: meta -->

The browser-chat architect does not seek operator validation on technical proposals where the operator lacks expertise to validate ("is this approach better?", "does this design make sense?", "should I use X or Y?"). The operator's role in technical questions is constraints, priorities, and scope — not technical adjudication.

For technical questions the architect cannot resolve alone:
- Research mode: web search, documentation, prior session memory
- AI Council: research or pick debate via `ai-council` CLI
- Analysis: build the comparison/proposal with explicit trade-offs the operator can choose from

Operator is asked: "which of these matters most to you?", "what's the constraint here?", "is this priority correct?" — not "is my technical choice right?".

Sourced from LESSONS #6 (2026-05-12). Architect-side enforcement is operator review.

---

## Artifact generation direction
<!-- scope: meta -->

Repo artifacts (ADRs, AI Council transcripts, audit reports, handoff bundles, any file destined for a source-of-truth repo) are generated IN Claude Code with proper repo path, ADR-NN numbering, frontmatter, archival convention, and commit hygiene — never generated as markdown artifacts in browser chat for the operator to copy-paste into the repo.

Browser chat role: architect-review of artifacts that Claude Code produces. Not artifact-source for repo files. The operator may upload a final repo artifact (e.g. an ADR draft) back to chat for review; the architect reviews and approves, Claude Code merges.

Sourced from LESSONS #8 (2026-05-13). Architect-side enforcement is the workflow rule itself; this is a permanent invariant per LESSONS.md 2026-05-13 (ADR-45 was explored but not adopted).

**Council ADR distillation** is a mandatory automated step of the post-debate protocol: number verified, template-aligned, committed by Claude Code — never a browser-chat hand-off with a placeholder. See PLAYBOOK § 5 "Post-debate protocol". End-to-end Council lifecycle runbook: `protocols/AI_COUNCIL_PROCESS.md`.

---

## Supersession closes the loop
<!-- scope: meta -->

- **Supersession closes the loop.** Any decision that relocates, replaces, or
  centralizes an artifact must name the obsolete artifact in a `Decommission:`
  field; a non-empty field becomes a BACKLOG item until removed. Creation
  without decommissioning is how orphans accumulate. See PLAYBOOK,
  "Supersession & decommissioning".

---

## Process versioning: beta → stable
<!-- scope: meta -->

A process (HANDOFF_PROCESS, AI_COUNCIL_PROCESS) ships `beta` after design + first
implementation; promotes to `stable` after one fresh-eyes review (zero-context LLM +
meta-reviewer prompt) returns **<2 critical findings AND reviewer judgment
PROMOTE/PROMOTE-WITH-CAVEATS**. Reviewer judgment overrides count. No Council convene
required for promotion. (PLAYBOOK)

---

## Starting a Session
<!-- scope: runtime -->

**Claude Code session:**
1. Open Claude Code in project dir
2. Shift+Tab → **Accept Edits** mode (daily driver)
3. Pick **max 2 objectives** for this session

**New browser chat:** Paste `protocols/HANDOFF_BOOT.md` — the thin boot is the whole browser onboarding (it replaces the old multi-file bundle; everything else is pulled just-in-time *via CC*). See `SESSION_SETUP.md` for the full checklist. (Historical v4 bundles under `docs/handoffs/` are flat `README.md` + `01_ROLE`…`07_ASK_BACK` — superseded, preserved as point-in-time history.)

---

## Parallel sessions (ADR-61)
<!-- scope: dev -->

> ⚠️ **SUPERSEDED** — the `<repo>-parallel` *sibling-dir* recipe below is superseded by the **native in-repo worktree convention** (`claude --worktree <name>` → `.claude/worktrees/<name>/`). See **PLAYBOOK §"Parallel sessions & worktree discipline"** for the live procedure. Do **not** create `<repo>-parallel` sibling directories — they spawned the `.dev-knowledge-cadence` / `.dev-knowledge-night-adr` rule-9 orphans. Text kept below for history.

- **Different repos:** safe, no setup needed (separate `.git/` = separate HEAD).
- **Same repo:** ❌ SUPERSEDED — use native, see PLAYBOOK — ~~`git worktree add <repo>-parallel main` → open 2nd CC session there, distinct branch each. Merge in primary tree, then `git worktree remove && git worktree prune`.~~
- **Pre-flight:** `git worktree list` before starting parallel work.
- Cross-repo sequential orchestration (one session, multiple `cd`s) is separate concern — safe, no worktree needed.

---

## Key Shortcuts
<!-- scope: runtime -->

| What | How |
|------|-----|
| Cycle modes (Default → Accept Edits → Plan) | Shift+Tab |
| Undo / rewind bad approach | Esc Esc |
| Toggle extended thinking | Alt+T |
| Switch model | Alt+P |
| Stop generation | Ctrl+C |
| Clear screen (not session) | Ctrl+L |

**Slash commands:** `/clear` (between tasks) · `/compact` (shrink context) · `/session-summary` (to browser) · `/resume` (resume context) · `/usage` (tokens)

---

## Writing a Prompt
<!-- scope: hybrid -->

Every formal prompt starts with:

```
| Model | Sonnet / Opus |
| Mode  | auto-accept / plan-then-auto / plan |
| Effort| low / medium / high / xhigh |
```

**Sonnet** = "do X the way we always do it." **Opus** = "figure out the right approach." **xhigh** = hardest debugging, architecture decisions, magistrala-level verification. Burns more tokens than high.

Then (**[A]** architect emits · **[CC]** CC self-loads, per ADR-87): **[A]** Title → **[CC]** Read CLAUDE.md + gotchas → **[CC]** Git workflow → **[A]** UNDERSTAND → **[A]** Steps with COMMIT markers → **[A]** What NOT to do.

**Architect output (standing rule):** the skeleton above is CC's *consumption-spec* — you don't hand-author all of it. Always state the **plan/auto mode** (plan when uncertain/multi-file/unfamiliar; auto when a trivial one-sentence diff) and a **thin governance-pointer** (the ADR/LESSONS/sibling-spec the task touches). CC self-loads code-impact context + generic gotchas but **won't self-infer governance context**, so the pointer is required for read-only/governance tasks — intent-only is conditional. Full contract: PLAYBOOK §2 "Architect output vs CC consumption-spec" / ADR-87.

**Skills reference:** if task has a relevant skill (e.g., `gotchas` for empirical traps), prompt names it — Claude Code auto-reads `.claude/skills/<name>/SKILL.md` per PLAYBOOK Section 7. User-level skills live in `~/.claude/skills/`, project-level in `<repo>/.claude/skills/`.

**Multi-prompt sessions:** If Claude.ai generates 3+ prompts for one feature, check for overlap before running — duplicate context wastes tokens and creates conflicting diffs.

After EVERY step: `pytest -x --tb=short && ruff check && git status`

---

## Repo visual pattern (ADR-59)
<!-- scope: dev -->

Every repo root looks the same: **dot-prefix configs** where the tool supports it (`.ruff.toml`, `.pre-commit-config.yaml`, `.{repo}.code-workspace`); **ALL-CAPS canonical `.md`** at root; workspace file dot-prefixed with `explorer.sortOrder: default` + `explorer.sortOrderLexicographicOptions: upper` (`upper` clusters ALL-CAPS first). Un-dotted exceptions: `pyproject.toml`, `package.json`, `Cargo.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `Dockerfile`, `Makefile`, `LICENSE`, `tach.toml`, `README.md`. New tool? Verify dot-prefix support (don't assume), then list the exception in ADR-59 + `audit.py`. Full standard: PLAYBOOK "Universal visual pattern".

---

## Mermaid theme (ADR-51 v2)
<!-- scope: meta -->

Every Mermaid block in `ARCHITECTURE.md` opens with `%%{init: {'theme':'base', 'themeVariables': {…}}}%%` (custom-base dark theme — readable on Rob's black VS Code background). Every `classDef` with a light `fill:` must also set explicit `color:` (else inherited-light-text on light-fill = unreadable). Copy directive verbatim from `templates/ARCHITECTURE-template.md`. Enforced by `audit.py` check #7 — runs on `ARCHITECTURE.md` + the template only. Standard: ADR-51 amendment 2026-05-28 (v2).

---

## Auto-TOC for large docs (ADR-51)
<!-- scope: meta -->

Large canonical docs carry an **auto-generated table of contents** between `<!-- TOC:START/END -->` markers — generator-driven + freshness-gated like the codemap, **never hand-maintained**. Regenerate with `python -m scripts.toc.cli generate <file> --write`; the `toc-freshness` pre-commit hook (fail-on-stale, standalone like `codemap-freshness`) blocks a stale TOC. Anchors are GitHub-compatible (`## Purpose [CORE]` → `#purpose-core`; `[TAG]` dropped from link text). Applied to `ARCHITECTURE.md` and `protocols/PLAYBOOK.md`; add elsewhere only where navigation overhead is real — roughly **≥~400 lines / ~8+ sections**. Full: PLAYBOOK "Auto-TOC for large canonical docs".

---

## docs/ taxonomy (ADR-60)
<!-- scope: meta -->

Each `docs/` subfolder = one semantic role. Two variants (per 2026-05-27 ADR-60 amendment): **`.dev-knowledge`** carries `decisions/`+`audits/`+`handoffs/`+`archive/`; **child code repos** carry `decisions/`+`audits/`+`archive/`+`diagrams/`. Child repos have NO `handoffs/` (centralized in `.dev-knowledge`), NO `research/`, NO `council-questions/`. `archive/` is a documented pending-classification zone (every repo's archive/ carries a README). Entry-scripts live in `scripts/`, not at root; root-exception configs are `pyproject.toml`, `tach.toml`, `requirements.txt`. On a move, never rewrite append-only/immutable records that cite the old path (ADRs, transcripts, JOURNAL) — they are point-in-time history; fix only living docs + the moved file's own refs. Full standard: PLAYBOOK "docs/ folder taxonomy".

---

## Commit message standard
<!-- scope: dev -->

Git history IS the changelog (no CHANGELOG.md since 2026-05-16). Commit
messages have to carry the load CHANGELOG used to. Standard:

- **Conventional Commits.** `type(scope): summary` — types are `feat`, `fix`,
  `docs`, `refactor`, `test`, `chore`. Scope is optional but use the
  file/folder slug when it clarifies.
- **Summary line.** Imperative mood, specific, describes WHAT changed. Under
  ~72 chars. **Never** "wip", "fix", "updates", "stuff", "various changes".
- **Body required for any non-trivial change.** WHAT changed and WHY —
  enough detail that `git log` answers "what happened here" without a
  separate changelog. One-line typo fixes can skip the body.
- **One logical change per commit.** If you'd write "and" in the summary,
  split the commit.

`/save` follows this standard. See CONTRIBUTING.md for live examples and
the pre-commit hook list.

---

## Managing Tokens
<!-- scope: llm -->

- **`/clear` between unrelated tasks** — different feature, different repo, or after high-effort prompt (saves 30-40%)
- **After 2 failed attempts → `/clear` and rewrite the prompt from scratch.** Polluted context with wrong approaches makes things worse, not better.
- **`!` prefix** for quick commands — `!git status`, `!pytest` runs directly without Claude processing, output goes to context. Zero AI tokens for simple checks.
- **Plan Mode first** (Shift+Tab x2) — catches bad approach at 200 tokens vs 5000
- **Line ranges** `@file:15-80` not whole files
- **VS Code first** — test explorer, Error Lens, GitLens = 0 tokens
- When Claude.ai gives you multiple prompts → it tells you when to `/clear` between them

---

## Ending a Session
<!-- scope: hybrid -->

> **JOURNAL is hard-gated at session-end (ADR-85, C1):** a session with commits must name ≥1 commit SHA from *this session* or the Stop-hook blocks turn-end; `/override [reason]` is the only escape. Canon: `protocols/DEFINITION_OF_DONE.md`.

1. Full test suite
2. `git status` — must be clean
3. If 3+ files changed or 2+ packages touched → `/codex-review <topic>` before merge (threshold for cross-module risk; single-file changes don't need review). Codex-review is for **code review, not markdown/prose** — diffs of only `.md` / governance files are skipped cleanly by the wrapper's path-guard, so a doc-only session needs no codex run.
4. **JOURNAL.md** — prepend an entry using the new structure:
   `### YYYY-MM-DD — <session topic>` (header form), then bullets:
   `- Did:` what was actually done  
   `- Result:` outcome / state on disk  
   `- Changes:` short list of what files / which areas moved (this is the change record — there is no CHANGELOG anymore)  
   `- Abandoned:` items deliberately dropped (each non-trivial drop should also get a short note in `docs/decisions/`; do not record reasoning inline in JOURNAL)  
   `- Next:` follow-ups
5. **Extract lessons** — "what 2-3 things did I learn?" → append to LESSONS.md  
   Format: `### YYYY-MM-DD | [source] | [lesson] | [category] | [scope: X] | [action taken]`  
   The `[scope: X]` tag is informal lightweight metadata since 2026-05-16; no validator enforces it.
6. Session scorecard logs automatically (Stop hook)

**Browser chat checkpoint:** at ~2h (buffer before the 3h decision-fatigue threshold per PLAYBOOK §Session boundaries → Decision fatigue threshold) or when the chat slows down → see **HANDOFF_PROCESS.md**

---

## Feedback Loop
<!-- scope: hybrid -->

**Automated** (Stop hook + auto-promotion):
- Every correction logged to `corrections.jsonl` → same mistake 2x → auto-promoted to permanent rule with verify: check

**Manual cadence:**
- **Friday** — weekly review (see PLAYBOOK §9 "Weekly Review"): gotchas, token usage, LESSONS, BACKLOG, project health. (The old self-evolution loop was retired 2026-06-05; corrections now auto-promote via the Stop hook above.)
- **Monthly** — Codex full-repo audit → triage flags (expect ~30% false positives) → fix CRITICAL/HIGH → re-audit → see PLAYBOOK Section 17. Cadence by repo complexity (judgment, not tier-gated; a tiny single-script repo may skip).

**New tool/article/repo decision rule:** mature (>100 stars, >v1.0 — heuristics for community validation + production stability)? Solves a real problem? Architecture-level → Council debate. Otherwise decide in 30 seconds.

**Council output convention (current):** AI Council CLI writes the canonical transcript to `ai-council/output/` (source of truth) and **automatically routes a copy** to a project's `docs/decisions/transcripts/` when the debate sets `target-project:` (frontmatter) or `--target-project` (CLI) — implemented per ADR-43 (`routing.py` `TargetResolver`). Routed debates need no manual archival; debates that name no target-project emit only to `ai-council/output/` and are archived manually. Canonical filename preserved (`council-out-YYYYMMDD-HHMMSS-*.md`). Full operational detail in PLAYBOOK "Council Debate Archival Protocol".

---

## Backlog (ADR-64/65/66)
<!-- scope: meta -->

`BACKLOG.md` = **open/in-progress `.dev-knowledge` work only**. Story-map layout (ADR-66): `## Big picture` → `## <Theme>` → `### <User Story>` + "So that" → task bullet `- [#id] [P][size] · Done when · refs`. **Done items leave** on close — the closing commit + the per-session JOURNAL entry are the record; **no archive** (CLAUDE §5), no per-item write. Schema is machine-checked (`scripts/validate_backlog.py`, read-only). Full: PLAYBOOK §10.

**Closure loop:** commit `closes [#id]` on the finishing commit -> end-of-session proposals (`logs/PROPOSALS-*.md`) -> `[closures]` nudge at next start -> `/review-closures`. (`advances [#id]` does **not** close — it leaves the item open and undetected.)

---

## Three Homes for Knowledge
<!-- scope: meta -->

| What | Where |
|------|-------|
| Client/product/domain intel | Obsidian vault |
| How I work (processes, lessons) | `Dev/.dev-knowledge/` |
| Rules Claude Code executes | `~/.claude/` |

When a lesson becomes a rule — see canonical trigger + 3-step process: PLAYBOOK §4 "When a lesson becomes a rule."

---

## Repo complexity (informal)
<!-- scope: meta -->

The formal repo-tier system (declared `tier:`/`scale:` gating governance) was retired 2026-05-23. The universal governance baseline (ADR-38 amendments A5/A6) now applies to every repo regardless of size — the seven-file canonical set (VISION, ARCHITECTURE, CLAUDE, BACKLOG, CONTRIBUTING, JOURNAL, LESSONS) is mandatory everywhere; no `[L only]` tags, no declared tier.

S/M/L survive only as informal complexity descriptors for calibrating judgment (how much test infrastructure, how rich a workspace), never as a declared, audited tier:

- **small** — single script/tool, few tests, simple flow
- **medium** — standalone package, multiple modules, one namespace
- **large** — multi-package repo, cross-package dependencies, many tests

Full guidance: PLAYBOOK "Project complexity bands". (Distinct from the *task-complexity* S/M/L used to size Claude Code prompts — that taxonomy is unaffected.)

---

## The 5 Rules That Matter Most
<!-- scope: hybrid -->

1. **Test after each change.** Not at the end.
2. **Verify, don't trust.** If AI says "done" in a long session — check the filesystem.
3. **Scope is sacred.** 1-2 objectives. Everything else is backlog.
4. **Claude.ai challenges, Claude Code executes.** Browser = critical thinking. Terminal = action.
5. **Date everything.** Filename or frontmatter. No undated artifacts.

---

## Data Sanitization for Lessons
<!-- scope: meta -->

Before writing dev lessons in `.dev-knowledge`: strip client names, proprietary schemas, internal tool names, client-specific API endpoints. Replace with `[client]` or generic placeholders. Methodology generalizes; project specifics don't — those belong in Obsidian vault. See PLAYBOOK §13 'Data sanitization' for the canonical framing.
