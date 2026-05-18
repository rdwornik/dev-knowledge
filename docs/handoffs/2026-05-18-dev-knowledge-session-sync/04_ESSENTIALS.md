# Daily Essentials

> Daily cheat sheet. Keep under 1 page.
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
- Reads CLAUDE.md, AGENTS.md on session start (auto)
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

---

## Architect → operator channel-discipline for execution actions
<!-- scope: meta -->

The browser-chat architect never writes git commands, shell sequences, or executable code inline in chat prose as informational text the operator manually copies. Two channels only, scale-determined:

- **Scale S** (one command, one mechanical edit, no judgment): PowerShell snippet in a fenced code block; operator copy-pastes and runs as-is.
- **Scale M+** (multi-step, multi-file, judgment needed, merge ops): Claude Code prompt as a downloadable `.md` file with full structure per PLAYBOOK.

**Test:** if the operator has to edit, paraphrase, or interpret anything when copying, the format is wrong.

Sourced from LESSONS #10 (2026-05-13). Architect-side enforcement is operator-review; mechanical enforcement on executor side via Claude Code harness (per ADR-45).

---

## Architect epistemic discipline: explicit verification markers
<!-- scope: meta -->

The browser-chat architect distinguishes three claim categories explicitly in handoffs, summaries, and any factual statement about repo state or prior work:

- **Witnessed** — directly observed by the architect (read a file, ran a command, saw a transcript)
- **Inference** — derived from witnessed evidence but one step removed (e.g. "test must pass because the commit message says so")
- **Unknown** — not verifiable from current context

Bundle-asserted facts (SHAs, file counts, version pins, prior session claims) are never propagated as Witnessed unless the architect actually verified them. Default for any claim arriving through a handoff bundle is Inference at most, Unknown if not corroborated.

Sourced from LESSONS #1 (2026-05-12). Architect-side enforcement is operator review; ADR-45 Stage 3 verification provides mechanical cross-check on executor side.

---

## Architect epistemic discipline: completion claims require state verification
<!-- scope: meta -->

Before declaring a session, directive list, or task "done" / "closed" / "complete", the architect verifies against actual state — BACKLOG residuals, untouched scope items, files modified but not committed, things mentioned earlier in chat that were never resolved. Pattern-matched "all done" framing from prompt structure alone is not evidence; it's a failure mode.

If the architect cannot verify completion (no filesystem access from browser chat), the claim becomes a question: "based on what I see here, X and Y look complete; please confirm Z is also done before I declare closure."

Sourced from LESSONS #2 (2026-05-12). Architect-side enforcement is operator review; ADR-45 `/save` validator provides mechanical session-end gate on executor side.

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

Sourced from LESSONS #8 (2026-05-13). Architect-side enforcement is the workflow rule itself; ADR-45 architect-compliance path makes this a permanent invariant.

**Council ADR distillation** is a mandatory automated step of the post-debate protocol: number verified, template-aligned, committed by Claude Code — never a browser-chat hand-off with a placeholder. See PLAYBOOK § 5 "Post-debate protocol".

---

## Supersession closes the loop
<!-- scope: meta -->

- **Supersession closes the loop.** Any decision that relocates, replaces, or
  centralizes an artifact must name the obsolete artifact in a `Decommission:`
  field; a non-empty field becomes a BACKLOG item until removed. Creation
  without decommissioning is how orphans accumulate. See PLAYBOOK,
  "Supersession & decommissioning".

---

## Starting a Session
<!-- scope: runtime -->

**Claude Code session:**
1. Open Claude Code in project dir
2. Type `/boot` — verifies rules, loads memory, checks trends
3. Shift+Tab → **Accept Edits** mode (daily driver)
4. Pick **max 2 objectives** for this session

**New browser chat:** Upload `protocols/ESSENTIALS.md` + most recent handoff folder from `docs/handoffs/` (drag-drop the `contents/` subfolder, paste `first-message.md`). See `SESSION_SETUP.md` for full checklist.

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

**Slash commands:** `/boot` (start) · `/clear` (between tasks) · `/compact` (shrink context) · `/session-summary` (to browser) · `/recap` (resume context) · `/evolve` (Friday) · `/stats` (tokens)

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

Then: Title → Read CLAUDE.md + gotchas → Git workflow → UNDERSTAND → Steps with COMMIT markers → What NOT to do.

**Skills reference:** if task has a relevant skill (e.g., `gotchas` for empirical traps), prompt names it — Claude Code auto-reads `.claude/skills/<name>/SKILL.md` per PLAYBOOK Section 7. User-level skills live in `~/.claude/skills/`, project-level in `<repo>/.claude/skills/`.

**Multi-prompt sessions:** If Claude.ai generates 3+ prompts for one feature, check for overlap before running — duplicate context wastes tokens and creates conflicting diffs.

After EVERY step: `pytest -x --tb=short && ruff check && git status`

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

1. Full test suite
2. `git status` — must be clean
3. If 3+ files changed or 2+ packages touched → `codex-review -Topic <topic>` (slash: `/codex-review`) before merge (threshold for cross-module risk; single-file changes don't need review)
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

**Browser chat checkpoint:** przy ~2h (buffer before 3h decision-fatigue threshold per PLAYBOOK Section 4) lub gdy chat zwalnia → see **HANDOFF_PROCESS.md**

---

## Feedback Loop
<!-- scope: hybrid -->

**Automated** (Stop hook + auto-promotion):
- Every correction logged to `corrections.jsonl` → same mistake 2x → auto-promoted to permanent rule with verify: check

**Manual cadence:**
- **Friday** — `/evolve` → review corrections, promote/prune rules, check trends
- **Monthly** — Codex full-repo audit → triage flags (expect ~30% false positives) → fix CRITICAL/HIGH → re-audit → see PLAYBOOK Section 17 [L+M]

**New tool/article/repo decision rule:** mature (>100 stars, >v1.0 — heuristics for community validation + production stability)? Solves a real problem? Architecture-level → Council debate. Otherwise decide in 30 seconds.

**Council output convention (current):** AI Council CLI emits to `ai-council/output/` only. Project-side transcripts (`.dev-knowledge/docs/decisions/transcripts/`, etc.) are populated by **manual archival** — this is the current process, not an edge case. Cross-project routing feature is pending (see BACKLOG Cross-stream P1 "AI Council cross-project transcript routing"). Until the feature lands: maintain manual archival discipline; canonical filename preserved (`council-out-YYYYMMDD-HHMMSS-*.md`); source of truth remains `ai-council/output/`. Full operational detail in PLAYBOOK.

---

## Three Homes for Knowledge
<!-- scope: meta -->

| What | Where |
|------|-------|
| Client/product/domain intel | Obsidian vault |
| How I work (processes, lessons) | `Dev/.dev-knowledge/` |
| Rules Claude Code executes | `~/.claude/` |

When a lesson becomes a rule → write rationale in LESSONS.md, write executable rule in `~/.claude/` with verify: line.

---

## Project Scale Tiers
<!-- scope: meta -->

Every project declares its scale in CLAUDE.md. Playbook sections tagged [L only] or [L+M] apply only to matching tiers.

- **S** — single script/tool, <50 tests, simple flow
- **M** — standalone package, 50-500 tests, multiple modules, one namespace
- **L** — multi-package monorepo, 500+ tests, ARCHITECTURE.md, per-module READMEs, AGENTS.md

Full matrix (testing rules, doc requirements, session continuity per tier) in PLAYBOOK Section "Project Scale Tiers".

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

Before writing dev lessons in `.dev-knowledge`: strip client names, proprietary schemas, internal tool names, client-specific API endpoints. Replace with `[client]` or generic placeholders. Methodology generalizes; project specifics don't — those belong in Obsidian vault. Detailed examples in PLAYBOOK.
