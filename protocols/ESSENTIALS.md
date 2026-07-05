---
last_reviewed: 2026-07-05
status: active
owner: Rob
---

# Daily Essentials

> The session-start operating frame for the LLM: the load-bearing essentials for working in this ecosystem. A 1–2-page frame by charter — every canonical detail lives ONCE in PLAYBOOK (or its ADR); this file points, never copies ([#258]).
> Mission anchor: `VISION.md` (universal brain) + `ARCHITECTURE.md` (structural model). Read those once on first session of a project; this file is the day-to-day driver.

---

## How Claude thinks
<!-- scope: llm -->

Applies primarily to Browser chat analytical work; also relevant whenever Claude Code is asked to reason rather than execute deterministically.

**Does:**
- Thinks deeply before responding — extended thinking, multiple hypotheses, "what am I missing" check, self-critique before presenting analysis
- Verifies factual claims against uploaded documents / current PLAYBOOK / source-of-truth before stating them; does not pattern-match to plausible-sounding answers
- Pushes back on Rob's premises when warranted, including when Rob's framing leads to suboptimal answer or when Rob's preferences contain internal contradiction
- Thinks architecturally first (highest scope, then zoom), not tactically; when asked about a specific item, first checks "is this a symptom of a bigger architectural question?"

**Does NOT:**
- Pattern-match to fast plausible answers without self-critique
- Interpret user preferences in their easiest reading without checking intent
- Default to validation when contradiction is the more useful response — concession without verification is sycophancy disguised as agreeableness
- Conflate concepts that share vocabulary but address different concerns (e.g., handoff INSTANCES vs handoff INTELLIGENCE; scope tags `dev | llm | hybrid | runtime | meta` vs invented like `process`)

---

## Roles
<!-- scope: meta -->

Two distinct LLM contexts collaborate on every workstream. Mixing them = chaos.

- **Browser chat (architect):** strategic thinking, decisions, prompt generation. No filesystem access — never touches repo files, never runs commands, doesn't persist across sessions.
- **Claude Code (executor):** file changes, tests, commits, branches. Never improvises without a clear prompt; never pushes to remote without Rob's confirmation.
- **When in doubt:** "Should we…?" → browser (decision) · "Implement X per spec" → Claude Code (execution) · "What did we decide about Y?" → either, but check `.dev-knowledge` first.

Canonical: the architect↔CC division is PLAYBOOK "The two lifelines" § Lifeline 1 (ADR-87); the full Does/Does-NOT lists + three-layer flow (ADR-28) are PLAYBOOK §8 "Roles".

---

## Architect disciplines
<!-- scope: meta -->

Four standing rules for the browser-chat architect — canonical text: PLAYBOOK Ch4 + §8 (sourced from LESSONS #1/#2/#6/#8/#10):

- **Architect → operator channel-discipline for execution actions:** Scale S (one command, no judgment) → fenced PowerShell snippet, run as-is; Scale M+ → downloadable `.md` prompt. If the operator must edit or interpret when copying, the format is wrong. (PLAYBOOK Ch4)
- **Epistemic discipline — verification markers:** every factual claim is **Witnessed / Inference / Unknown**; bundle-asserted facts are never Witnessed unverified. Completion claims ("done"/"closed") require state verification — unverifiable claims become questions to the operator. (PLAYBOOK §8, both subsections)
- **Architect routing for technical proposals:** the operator owns constraints, priorities, scope — never technical adjudication. Technical uncertainty routes to research / AI Council / explicit trade-off analysis. (PLAYBOOK §8)
- **Artifact generation direction:** repo artifacts (ADRs, transcripts, audits, handoffs) are generated IN Claude Code — never browser-pasted into the repo. Browser reviews; Claude Code commits and merges. (PLAYBOOK §8; Council lifecycle: `protocols/AI_COUNCIL_PROCESS.md`)

---

## Governance frame
<!-- scope: meta -->

- **Continuous improvement:** default posture is **always be improving** — static maintenance is a declared exception in VISION Lifecycle; "feature-complete" never means "done". Canonical: PLAYBOOK Ch13 "Project-evolution posture".
- **Supersession closes the loop:** any decision that relocates/replaces/centralizes an artifact names the obsolete artifact in a `Decommission:` field; non-empty → BACKLOG item until removed. Canonical: PLAYBOOK Ch6 "Supersession & decommissioning".
- **Process versioning:** processes ship `beta`; promote to `stable` after one fresh-eyes review (<2 critical findings AND reviewer verdict PROMOTE / PROMOTE-WITH-CAVEATS; judgment overrides count). Canonical: PLAYBOOK Ch2.

---

## Starting a Session
<!-- scope: runtime -->

**Claude Code session:** 1. Open Claude Code in project dir · 2. Shift+Tab → **Accept Edits** mode (daily driver) · 3. Pick **max 2 objectives**.

**New browser chat:** paste `protocols/HANDOFF_BOOT.md` — the thin boot is the whole browser onboarding (everything else is pulled just-in-time *via CC*). Full checklist: `SESSION_SETUP.md`.

---

## Parallel sessions
<!-- scope: dev -->

Same-repo parallel work runs on **native worktrees only** (`claude --worktree <name>` → `.claude/worktrees/<name>/`); one checkout = one committing session; different repos need no setup. Never create `<repo>-parallel` sibling dirs (superseded — they spawned the rule-9 orphans). Pre-flight: `git worktree list`. Canonical: PLAYBOOK Ch8 "Parallel sessions & worktree discipline" (ADR-61).

---

## Writing a Prompt
<!-- scope: hybrid -->

Every formal prompt opens with the Model/Mode/Effort table — **Model is CC's pick** (default Opus 4.8, the floor); the architect sets **Mode** and **Effort** plus a **thin governance-pointer** (CC self-loads code-impact context but won't self-infer governance context). If a task has a relevant skill, the prompt names it.

After EVERY step: `pytest -x --tb=short && ruff check && git status`

Canonical: PLAYBOOK §2 "Creating a Claude Code Prompt" (incl. "Architect output vs CC consumption-spec") + Ch4 "Writing prompts for Claude Code" + ADR-87.

---

## Conventions (canonical homes)
<!-- scope: meta -->

- **Repo visual pattern** (dot-prefix configs, ALL-CAPS canonical `.md`, workspace sort `upper`) → ADR-59; PLAYBOOK Ch3 "Universal visual pattern"
- **docs/ taxonomy** (one semantic role per subfolder; two repo-type variants; immutable records never rewritten on move) → ADR-60; PLAYBOOK Ch3
- **Commit messages** (Conventional Commits; git history IS the changelog — WHAT in summary, WHY in body, one logical change per commit) → PLAYBOOK Ch3 "Commit message standard"
- **Rule-IDs** (`<domain>-<slug>` at doc + code side; declare at the authoritative source, never in a summary) → PLAYBOOK Ch3; ADR-89 OQ1
- **Mermaid theme** (re-scoped to the human-facing visualization surface as guidance — canonical `ARCHITECTURE.md` carries no Mermaid, audit check #7 retired) → PLAYBOOK "Codemap workflow"; ADR-51 amendment 2026-07-05
- **Auto-TOC** (generator-driven between `<!-- TOC:START/END -->`, freshness-gated, never hand-maintained) → PLAYBOOK "Auto-TOC for large canonical docs"; ADR-51

---

## Managing Tokens
<!-- scope: llm -->

`/clear` between unrelated tasks (top saver) · **after 2 failed attempts → `/clear` and rewrite the prompt from scratch** (golden rule) · `!` prefix for zero-token shell checks · Plan Mode catches a bad approach at 200 tokens vs 5000. Shortcuts: Shift+Tab cycles modes, Esc Esc rewinds. Full tables: PLAYBOOK Appendices A + C.

---

## Ending a Session
<!-- scope: hybrid -->

> **JOURNAL is hard-gated at session-end (ADR-85, C1):** a session with commits must name ≥1 commit SHA from *this session* or the Stop-hook blocks turn-end; `/override [reason]` is the only escape. Canon: `protocols/DEFINITION_OF_DONE.md`.

1. Full test suite
2. `git status` — must be clean
3. If 3+ code files or 2+ packages touched → two-stage code review: `/code-review high` in-flight, `/codex-review <topic>` final before merge (code only — doc-only diffs skip both)
4. **JOURNAL.md** — prepend entry: Did / Result / Changes / Abandoned / Next (structure: PLAYBOOK §7 "Session end protocol")
5. **Extract lessons** — 2-3 things learned → append to LESSONS.md (format: PLAYBOOK §4)
6. Session scorecard logs automatically (Stop hook)

**Browser chat checkpoint:** at ~2h or when the chat slows down → see **HANDOFF_PROCESS.md**

---

## Feedback Loop
<!-- scope: hybrid -->

**Automated:** every correction logged to `corrections.jsonl` → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook).

**Manual cadence:** **Friday** weekly review (PLAYBOOK §9) · **Monthly** Codex full-repo audit (PLAYBOOK §17; cadence by repo complexity).

New tool/article: maturity + real-problem check; architecture-level → Council debate (PLAYBOOK §3 / §11). Council transcripts auto-route per `target-project:` — canonical: PLAYBOOK §5 "Council output convention (current state)".

---

## Backlog (ADR-64/65/66)
<!-- scope: meta -->

`BACKLOG.md` = open/in-progress `.dev-knowledge` work only; story-map schema machine-checked; **done items leave** on close (no archive). Close via `closes [#id]` on the finishing commit → end-of-session proposals → `/review-closures` (`advances [#id]` does **not** close). Canonical: PLAYBOOK §10.

---

## Three Homes for Knowledge
<!-- scope: meta -->

| What | Where |
|------|-------|
| Client/product/domain intel | Obsidian vault |
| How I work (processes, lessons) | `Dev/.dev-knowledge/` |
| Rules Claude Code executes | `~/.claude/` |

When a lesson becomes a rule: PLAYBOOK §4. **Data sanitization:** strip client names/schemas/tools/endpoints → `[client]` placeholders before writing lessons here; specifics belong in Obsidian. Canonical: PLAYBOOK §13.

---

## Repo complexity (informal)
<!-- scope: meta -->

The formal repo-tier system was retired 2026-05-23; the universal governance baseline (ADR-38 A5/A6, seven-file canonical set) applies to every repo. S/M/L survive only as informal calibration descriptors. Canonical: PLAYBOOK Ch5 "Project complexity bands".

---

## The 5 Rules That Matter Most
<!-- scope: hybrid -->

1. **Test after each change.** Not at the end.
2. **Verify, don't trust.** If AI says "done" in a long session — check the filesystem.
3. **Scope is sacred.** 1-2 objectives. Everything else is backlog.
4. **Claude.ai challenges, Claude Code executes.** Browser = critical thinking. Terminal = action.
5. **Date everything.** Filename or frontmatter. No undated artifacts.
