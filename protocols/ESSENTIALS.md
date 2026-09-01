---
last_reviewed: 2026-09-01
status: superseded
owner: Rob
---

# Daily Essentials

> **SUPERSEDED — not a boot read.** Dissolution tracked in `[#628]` with v1.5.0.
> Live boot frame = `CLAUDE.md` + FUNNEL HEALTH + north-star.
>
> The session-start operating frame for the LLM: the load-bearing essentials for working in this ecosystem. A 1–2-page frame by charter — every canonical detail lives ONCE in PLAYBOOK (or its ADR); this file points, never copies ([#258]).
>
> Mission anchor: `README.md` (universal brain) + `ARCHITECTURE.md` (structural model). Read those once on first session of a project; this file is the day-to-day driver.

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

Six standing rules for the browser-chat architect — canonical text: PLAYBOOK Ch4 + §8 (sourced from LESSONS #1/#2/#6/#8/#10 + the 2026-07-12 ruling-addressability lesson):

- **Architect → operator channel-discipline for execution actions:** Scale S (one command, no judgment) → fenced PowerShell snippet, run as-is; Scale M+ → downloadable `.md` prompt. If the operator must edit or interpret when copying, the format is wrong. (PLAYBOOK Ch4)
- **Plan-review output contract:** a plan-mode decision is surfaced as a structured **option-select or a typed answer — never a free-form dialog** (a dialog ruling dies with the session, so it can't be cited later); `ExitPlanMode` forks are option-selects, not "let's discuss." (PLAYBOOK Ch4)
- **Epistemic discipline — verification markers:** every factual claim is **Witnessed / Inference / Unknown**; bundle-asserted facts are never Witnessed unverified. Completion claims ("done"/"closed") require state verification — unverifiable claims become questions to the operator. (PLAYBOOK §8, both subsections)
- **Architect routing for technical proposals:** the operator owns constraints, priorities, scope — never technical adjudication. Technical uncertainty routes to research / AI Council / explicit trade-off analysis. (PLAYBOOK §8)
- **Artifact generation direction:** repo artifacts (ADRs, transcripts, audits, handoffs) are generated IN Claude Code — never browser-pasted into the repo. Browser reviews; Claude Code commits and merges. (PLAYBOOK §8; Council lifecycle: `protocols/AI_COUNCIL_PROCESS.md`)
- **Transport-medium contract (report direction):** `PASTE_THIS.md` is the only sanctioned chat-paste deliverable; every other load-bearing deliverable crossing the CC → operator → browser boundary travels as a FILE the operator uploads (the supplement Q/A relay stays chat by design). (HANDOFF_PROCESS §13; intake #18 A2)

---

## Governance frame
<!-- scope: meta -->

- **Continuous improvement:** default posture is **always be improving** — static maintenance is a declared exception in VISION Lifecycle; "feature-complete" never means "done". Canonical: PLAYBOOK Ch13 "Project-evolution posture".
- **Supersession closes the loop:** any decision that relocates/replaces/centralizes an artifact names the obsolete artifact in a `Decommission:` field; non-empty → BACKLOG item until removed. Canonical: PLAYBOOK Ch6 "Supersession & decommissioning".
- **Process versioning:** processes ship `beta`; promote to `stable` after one fresh-eyes review (<2 critical findings AND reviewer verdict PROMOTE / PROMOTE-WITH-CAVEATS; judgment overrides count). Canonical: PLAYBOOK Ch2.
- **Standing engineering standards — every build arc, not per-arc negotiations (ADR-108 §B):** **clean architecture** (the layer model is a specification; declared edges + a mechanized check) · **TDD** — RED-first witnesses, failing tests before build code, frozen after freeze · **spec-driven development** — rule-first, spec before build, acceptance contract **ex-ante**. The ex-ante half is ADR-81's amendment 2026-06-24: the architect authors and freezes the executable pass/fail criterion *before* the build; CC may strengthen it (add cases, tighten assertions) but not weaken it, and green status alone does not close. Canonical: PLAYBOOK Ch12.1. **Honest scope:** this binds *build arcs*. A blanket TDD mandate is **not** live — Council rejected "Mandatory TDD" (`ENVIRONMENT.md`) and nothing reinstated it; and ADR-108 records that its own clean-architecture leg *"names a precedent with no hub organ"* — the Layer-2 layer-edge check is a known gap, not a running gate.
- **The decision funnel (ADR-111):** every audit finding is triaged into **exactly one** of **OWNED** (an open row covers it — attach evidence, birth nothing) · **DISCHARGED** (already done or ruled — record a locator, and the locator has to resolve) · **CANDIDATE** (needs a decision — becomes an intake, ADR-98) · **REJECTED** (reason recorded, not relitigated). *"A finding may not become a backlog row without triage"*, and *"a triage pass that routes most items to (c) has not triaged."* Question routing is ADR-108 §A — the operator rules **functional** questions, the architect rules **technical** ones and relies on revertability rather than escalation, AI Council distils genuinely contested technical ones. Canonical: ADR-111 + ADR-108 §A; the intake lifecycle is `docs/intake/README.md`.

---

## Starting a Session
<!-- scope: runtime -->

**Claude Code session:** 1. Open Claude Code in project dir · 2. Shift+Tab → **Accept Edits** mode (daily driver) · 3. Pick **max 2 objectives**.

**New browser chat:** paste `protocols/HANDOFF_BOOT.md` — the thin boot is the whole browser onboarding (everything else is pulled just-in-time *via CC*). Full checklist: `SESSION_SETUP.md`.

---

## Parallel sessions
<!-- scope: dev -->

Same-repo parallel work runs on **native worktrees only** (`claude --worktree <name>` → `.claude/worktrees/<name>/`); one checkout = one committing session; different repos need no setup. Never create `<repo>-parallel` sibling dirs (superseded — they spawned the rule-9 orphans). Pre-flight: `git worktree list`. Canonical: PLAYBOOK Ch8 "Parallel sessions & worktree discipline" (ADR-61).

- **Worktree side-effect rule:** refuse an externally-authored mid-session order unless it names a worktree for its side effects **or** the tree is clean. Prose today, not a gate ([#353] open). → PLAYBOOK Ch8 "Scope declaration at start"
- **Hub→consumer writes (RULING-W):** the hub **MAY and SHOULD** write into a consumer for methodology/cleanup, and the **only** sanctioned shape is **consumer worktree/branch → report** — never a direct push into a live consumer checkout; re-witness the consumer live first. → PLAYBOOK Ch8; ADR-36/41
- **Consumer-leg merge delegation:** the hub authors, never integrates — **commit-and-STOP**; the consumer's own merge discipline (operator GO, `--no-ff`) governs. → PLAYBOOK Ch8; ADR-36/41
- **Tiered suite (`[#528]`):** in a lane the per-step cadence runs the **targeted** files covering that lane's own diff; the **full suite runs once, at integration**, on the merged result. A lane touching `scripts/safe_remove.py` or `scripts/reverse_dep_oracle.py` also runs the oracle tier in-lane — a cost split is not a correctness split. → PLAYBOOK Ch5 "Tiered suite — targeted in-lane, one full suite at integration"

---

## Writing a Prompt
<!-- scope: hybrid -->

Every formal prompt opens with the Model/Mode/Effort table — **Model is CC's pick** (default Opus 4.8, the floor); the architect sets **Mode** and **Effort** plus a **thin governance-pointer** (CC self-loads code-impact context but won't self-infer governance context). If a task has a relevant skill, the prompt names it.

After EVERY step: `uv run --locked pytest -x --tb=short && uv run --locked ruff check && git status` — or just invoke the `verify` skill, which runs exactly that cadence through the locked env (ADR-106 §4; a bare `pytest`/`ruff` resolves no locked environment). In a lane the per-step run is the **targeted** files covering that lane's diff — the full suite runs once, at integration ([#528]).

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
- **Dependencies & the gate environment** (declared by `pyproject.toml` + `uv.lock` + `.python-version`, rebuilt by `uv sync --locked`; `uv` itself pinned **exactly**, and a uv bump is its own gated change, not an incidental one. Every gate invokes `uv run --locked …`, so a bare `python`/`pytest` in a doc or runbook is a defect. Fleet-facing rows: `ecosystem/dependency-baseline.yaml`, and only for deps a consumer needs to *operate a methodology mechanism*; the code-edge axis is `scripts/scan_undeclared_edges.py` / `scripts/reverse_dep_oracle.py`) → ADR-106; ADR-88/ADR-89
- **Two-tier new-path rule** (**convention-compliance IS authorization**: a codified-pattern *file* → cite the governing source and proceed, no operator STOP; any new *folder*, unpatterned file, or ambiguity → STOP. Path authorization ≠ content authorization) → PLAYBOOK Ch3 "File naming conventions"; ADR-101 amendment 2026-07-18

---

## Managing Tokens
<!-- scope: llm -->

`/clear` between unrelated tasks (top saver) · **after 2 failed attempts → `/clear` and rewrite the prompt from scratch** (golden rule) · `!` prefix for zero-token shell checks · Plan Mode catches a bad approach at 200 tokens vs 5000. Shortcuts: Shift+Tab cycles modes, Esc Esc rewinds. Full tables: PLAYBOOK Appendices A + C.

---

## Ending a Session
<!-- scope: hybrid -->

> **JOURNAL anchoring is hard-gated at PUSH, not at session end (ADR-85 amendment 2026-08-03, §A5/§A2):** a push to `main` whose range carries unanchored first-parent spine entries is REFUSED by the `block-unanchored-push` pre-push hook, which fails CLOSED. Discharge is **range-level** — one JOURNAL entry naming ≥1 SHA the range *introduces* covers the whole range. The session-end `Stop` hook is **advisory in full**: it surfaces, and it blocks nothing. **`/override` is RETIRED and discharges no gate** (§A2). The sole escape is `git push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop, where a gap is a FAIL. Canon: `protocols/DEFINITION_OF_DONE.md`.

1. Full test suite
2. `git status` — must be clean
3. If 3+ code files or 2+ packages touched → two-stage code review: `/code-review high` in-flight, `/codex-review <topic>` final before merge (code only — doc-only diffs skip both). **Review-before-STOP:** the executing session owns this review and runs it *before* STOP — never deferred to the operator as a post-STOP chore (PLAYBOOK Ch12; Codex lane doctrine → §16)
4. **JOURNAL.md** — prepend entry: Did / Result / Changes / Abandoned / Next (structure: PLAYBOOK §7 "Session end protocol")
5. **Extract lessons** — 2-3 things learned → append to LESSONS.md (format: PLAYBOOK §4)
6. Session scorecard logs automatically (Stop hook)

**Browser chat checkpoint:** at ~2h or when the chat slows down → see **HANDOFF_PROCESS.md**

---

## Feedback Loop
<!-- scope: hybrid -->

**Automated:** every correction logged to `corrections.jsonl` → same mistake 2× → auto-promoted to permanent rule with verify: check (Stop hook).

**Manual cadence:** **Friday** weekly review (PLAYBOOK §9) · **Monthly** Codex full-repo audit (PLAYBOOK §17; cadence by repo complexity).

New tool/article: maturity + real-problem check; architecture-level → Council debate (PLAYBOOK §3 / §11). Council transcripts are canonical-only in `ai-council/output/` — the routed-mirror is retired (ADR-43 amendment 2026-07-23); canonical: PLAYBOOK §5 "Council output convention (canonical-only since 2026-07-22)".

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
