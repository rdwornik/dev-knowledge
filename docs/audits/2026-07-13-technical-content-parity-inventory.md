# Content-parity divergence inventory — hub · ai-council · corp-monorepo

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-13
- **Source-session:** exhaustive read-only comparison at `.dev-knowledge` `9b5c67e0`, `ai-council` `dd06c861`, and `corp-monorepo` `31f7f5de`
- **Status:** PROPOSAL-ONLY — no consumer file was edited; dispositions below are for operator ruling
- **Model:** Codex (GPT-5)

## Executive so-what

Thirty actionable divergence rows remain across the requested surfaces. The sharpest result is in the always-read contract: of the hub's eight `owner=hub` CLAUDE regions, three exist in both consumers but differ at logical-line level, while five have at least one missing consumer region (`.dev-knowledge/CLAUDE.md:18-190`; `ai-council/CLAUDE.md:17-156`; `corp-monorepo/CLAUDE.md:20-159`). The two consumer BACKLOGs both lack the hub's E-prefixed theme spine; corp also lacks S-prefixed stories (`.dev-knowledge/BACKLOG.md:3-20`; `ai-council/BACKLOG.md:3-31`; `corp-monorepo/BACKLOG.md:3-20`). The shared carrier artifacts are healthier: the two child floors, their sidecars and guard scripts, `/override`, and both root `INSTALL.md` copies are exact Git-blob matches to their applicable hub sources (`ai-council/.claude/CLAUDE-FLOOR.md:1-41`; `corp-monorepo/.claude/CLAUDE-FLOOR.md:1-41`; `.dev-knowledge/.claude/commands/override.md:1-57`; `ai-council/INSTALL.md:1-100`; `corp-monorepo/INSTALL.md:1-100`).

The economical ruling is one template split: universal wording is byte/logical-line identical and `owner=hub`; repository paths, commands, test gates, domain rules, and local machinery move into explicit `owner=repo` or `.methodology.yaml` declarations. That single rule resolves most of Classes A, B, and E without pretending project-local content should be identical.

## Scope and evidence protocol

Included: CLAUDE.md region/content/form; LESSONS format; full CONTRIBUTING semantics; JOURNAL header/preamble only; INSTALL/VISION; BACKLOG hierarchy and id space; the complete `.claude/` filesystem/tracked-tree surface; `.gitignore` and runtime caches; and `protocols/`.

Explicitly excluded as directed: `.github/`; `docs/audits/` casing policy; ruff configuration form; `.vscode/`; `docs/diagrams/`; and `docs/handoffs/`. A hook-roster omission caused by the already-executed casing ruling is recorded only as roster currency; the casing ruling itself is not reopened.

Positive content claims cite `repo/path:line`. A missing path has no possible source line, so every negative tree claim is tied instead to the immutable HEAD above and the reproducible census `git ls-files -- <path>` (tracked state) plus `Get-ChildItem -Force` (runtime-only state). Exact-equality claims use Git index blob ids, avoiding checkout CRLF/LF conversion noise. Logical-line comparison used UTF-8 text with line endings normalized but retained every authored line break, bullet, phrase, and section order.

## Confirmed parity — not divergence rows

- All three CLAUDE files retain sections 1–12 in the same order. The only section-title delta is hub §11's suffix “(last 5)” versus the consumers' unsuffixed title (`.dev-knowledge/CLAUDE.md:16-201`; `ai-council/CLAUDE.md:16-182`; `corp-monorepo/CLAUDE.md:19-179`).
- The global command surface is consistently `/session-summary` + `/codex-review`, and all three repos expose plugin `/review-closures` + `/ship` and repo `/override` (`.dev-knowledge/CLAUDE.md:115-125`; `ai-council/CLAUDE.md:86-96`; `corp-monorepo/CLAUDE.md:110-118`). The three `.claude/commands/override.md` blobs are identical (`.dev-knowledge/.claude/commands/override.md:1-57`; `ai-council/.claude/commands/override.md:1-57`; `corp-monorepo/.claude/commands/override.md:1-57`).
- The two child methodology floors, sidecars, and guard scripts are exact pairs (`ai-council/.claude/CLAUDE-FLOOR.md:1-41`; `corp-monorepo/.claude/CLAUDE-FLOOR.md:1-41`; `ai-council/.claude/check_floor_hash.py:1-47`; `corp-monorepo/.claude/check_floor_hash.py:1-47`).
- `INSTALL.md` content is exact across the hub canonical plugin source and both consumer roots (`.dev-knowledge/plugins/tier1-lifecycle/INSTALL.md:1-100`; `ai-council/INSTALL.md:1-100`; `corp-monorepo/INSTALL.md:1-100`). The remaining issue is distribution ownership, row C8.
- All three VISION files preserve the canonical order `Vision → Scope → Values → Relationships → Lifecycle → References`; hub alone inserts `Strategic emphasis` after Vision. Project substance is appropriately local (`.dev-knowledge/VISION.md:11-162`; `ai-council/VISION.md:12-55`; `corp-monorepo/VISION.md:10-156`). Ai is terse in Lifecycle, corp is close to the hub's full lifecycle contract, and corp alone lacks the scope tag (`ai-council/VISION.md:42-48`; `corp-monorepo/VISION.md:115-145`; `.dev-knowledge/VISION.md:115-152`). No content-convergence ruling is needed beyond retaining this skeleton.
- `.pytest_cache/` and `.mypy_cache/` are ignored in all three repos. Runtime state is hub: pytest present/mypy absent; ai: both present; corp: pytest present/mypy absent (`.dev-knowledge/.gitignore:1-6`; `ai-council/.gitignore:1-9`; `corp-monorepo/.gitignore:1-8`). No cache file is tracked.

## Ruling Class A — make every `owner=hub` CLAUDE region one canonical body

### A1 — `first-read`

- **Surface:** CLAUDE `id=first-read`.
- **Hub state:** Five-item order; hub-local protocol paths; full v5 handoff boot/runbook wording; fallback if ESSENTIALS/PLAYBOOK are unavailable (`.dev-knowledge/CLAUDE.md:18-28`).
- **ai-council state:** Marked `owner=hub`, but uses sibling protocol paths and shortens handoff item 4; otherwise preserves the five-item shape and fallback (`ai-council/CLAUDE.md:17-27`).
- **corp state:** Marked `owner=hub`, adds item 6 (`VISION.md`) and replaces the fallback with “Skip if not applicable”; handoff wording is corp-specific (`corp-monorepo/CLAUDE.md:20-31`).
- **Classification:** OWNER-HUB-DIVERGENT.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — keep one universal sequence and move path/repo additions into an adjacent `owner=repo` block.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A2 — `conventions-commit-branch`

- **Surface:** CLAUDE commit and branch phrasing.
- **Hub state:** Compact type list and four branch prefixes with placeholders, explicitly off `main` (`.dev-knowledge/CLAUDE.md:56-59`).
- **ai-council state:** Rephrases commits as `type(scope): summary`, changes `<issue>/<scope>` to `<topic>`, and drops “off main” (`ai-council/CLAUDE.md:48-51`).
- **corp state:** Uses colon-suffixed commit types, adds `test` and `refactor`, removes placeholders, and adds the direct-main prohibition (`corp-monorepo/CLAUDE.md:55-58`).
- **Classification:** OWNER-HUB-DIVERGENT.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — rule one branch-prefix/type sentence here; project-only exceptions belong outside this region.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A3 — `conventions-output-formatting`

- **Surface:** CLAUDE render-layer copy-out discipline.
- **Hub state:** A dedicated `owner=hub` region requires flat, triple-fenced copy-out and explains why bare tables are TUI-painted (`.dev-knowledge/CLAUDE.md:73-75`).
- **ai-council state:** No region or equivalent rule between local conventions and §5 (`ai-council/CLAUDE.md:45-60`; tracked-tree census at `dd06c861`).
- **corp state:** No region or equivalent rule between local conventions and §5 (`corp-monorepo/CLAUDE.md:52-69`; tracked-tree census at `31f7f5de`).
- **Classification:** GAP.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A4 — `critical-rules-records`

- **Surface:** CLAUDE append-only/immutable-record rules.
- **Hub state:** Three canonical rules cover LESSONS/TOKEN-LOG, newest-first JOURNAL, and ADR/transcript/handoff/audit immutability including the ADR-94 status-line exception (`.dev-knowledge/CLAUDE.md:80-84`).
- **ai-council state:** Region exists but contains only renumbered LESSONS and ADR rules; JOURNAL, TOKEN-LOG, transcripts/handoffs/audits, and ADR-94 wording are absent (`ai-council/CLAUDE.md:65-68`).
- **corp state:** Region is missing; §5 contains only project rules (`corp-monorepo/CLAUDE.md:69-89`; tracked-tree census at `31f7f5de`).
- **Classification:** GAP (with ai also text-divergent).
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — identical universal rules first, project rules in a separate local sequence.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A5 — `critical-rules-consistency`

- **Surface:** CLAUDE ESSENTIALS↔PLAYBOOK consistency rule.
- **Hub state:** Dedicated `owner=hub` region says ESSENTIALS summarizes rather than copies PLAYBOOK (`.dev-knowledge/CLAUDE.md:87-89`).
- **ai-council state:** Missing between its record rules and remaining project rules (`ai-council/CLAUDE.md:65-71`; tracked-tree census at `dd06c861`).
- **corp state:** Missing throughout §5 (`corp-monorepo/CLAUDE.md:69-89`; tracked-tree census at `31f7f5de`).
- **Classification:** GAP.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A6 — `critical-rules-no-leftovers`

- **Surface:** CLAUDE provision→cleanup round-trip rule.
- **Hub state:** Dedicated `owner=hub` region requires cleanup and verification even on abort (`.dev-knowledge/CLAUDE.md:92-94`).
- **ai-council state:** Missing from §5 (`ai-council/CLAUDE.md:60-71`; tracked-tree census at `dd06c861`).
- **corp state:** Missing from §5 despite an empty runtime worktree directory now existing (`corp-monorepo/CLAUDE.md:69-89`; runtime census at `31f7f5de`).
- **Classification:** GAP.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A7 — `session-start-protocol`

- **Surface:** CLAUDE session-start sequence and failure posture.
- **Hub state:** Six steps include BACKLOG and test discovery, followed by stop-on-failure and post-update reconciliation clauses (`.dev-knowledge/CLAUDE.md:98-110`).
- **ai-council state:** Six steps omit BACKLOG and both trailing clauses, add a merge-time `check.ps1` step, and change test flags (`ai-council/CLAUDE.md:73-81`).
- **corp state:** Five steps omit BACKLOG, test discovery, both trailing clauses, and place JOURNAL reading outside/inside different surfaces (`corp-monorepo/CLAUDE.md:91-105`).
- **Classification:** OWNER-HUB-DIVERGENT.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — identical session-start invariant; repo-specific test/merge commands move to `owner=repo`.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

### A8 — `antipatterns-universal`

- **Surface:** CLAUDE universal anti-pattern region.
- **Hub state:** Six `owner=hub` bullets cover append-only edits, Layer-2 orchestration, retired AGENTS, resident copies, executable-rule placement, and vacuous validators (`.dev-knowledge/CLAUDE.md:182-190`).
- **ai-council state:** Only an `owner=repo` anti-pattern region is present (`ai-council/CLAUDE.md:136-156`).
- **corp state:** Only an `owner=repo` anti-pattern region is present (`corp-monorepo/CLAUDE.md:150-159`).
- **Classification:** GAP.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — universal block plus retained local block.
- **Blast radius:** 2 files — both consumer `CLAUDE.md` files.

## Ruling Class B — normalize the CLAUDE shell and roster schemas; keep project facts local

### B1 — shell metadata, marker coverage, and section naming

- **Surface:** CLAUDE frontmatter/import/title/boundary note/section-heading shell.
- **Hub state:** Has `reconciled_with`, scope/version comments, no child-floor import, no human boundary note, and §11 “last 5”; its marker baseline is eight hub + seven repo regions (`.dev-knowledge/CLAUDE.md:1-18`; `.dev-knowledge/CLAUDE.md:192-215`).
- **ai-council state:** Has the floor import and boundary note, but no `reconciled_with`, version comment, or scope comments; it carries four hub + eight repo regions and unsuffixed §11 (`ai-council/CLAUDE.md:1-17`; `ai-council/CLAUDE.md:158-192`).
- **corp state:** Has floor import, scope/version comments, and boundary note but no `reconciled_with`; it carries three hub + eight repo regions and unsuffixed §11 (`corp-monorepo/CLAUDE.md:1-20`; `corp-monorepo/CLAUDE.md:161-189`).
- **Classification:** LOCAL-UNMARKED — the shell around the marked bodies itself has no owner boundary.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — define an identical 12-section shell; mark the child-floor import and repo title as local/conditional; choose one §11 title.
- **Blast radius:** 3 `CLAUDE.md` files.

### B2 — project-local prose outside any owner region

- **Surface:** Local convention/rule prose interleaved around marked regions.
- **Hub state:** Naming/testing/linting/lifecycle/out-of-scope text and hub-only critical rules sit outside owner markers (`.dev-knowledge/CLAUDE.md:52-93`).
- **ai-council state:** Naming/testing/linting/out-of-scope and most project rules are unmarked (`ai-council/CLAUDE.md:45-71`).
- **corp state:** Naming/testing/config/methodology/engagement, all project rules, and the post-§6 session-end/handoff prose are unmarked (`corp-monorepo/CLAUDE.md:52-89`; `corp-monorepo/CLAUDE.md:100-105`).
- **Classification:** LOCAL-UNMARKED.
- **Proposed disposition:** DECLARE-LOCAL — wrap contiguous local blocks `owner=repo` (or declare them through the #328 ownership manifest) without changing their project semantics.
- **Blast radius:** 3 `CLAUDE.md` files plus the future #328 manifest.

### B3 — commands-available roster form

- **Surface:** CLAUDE §7 plus `.claude/commands/` disk truth.
- **Hub state:** User-level commands are hand-listed; four repo commands are generator-imported; deployable/plugin commands are a second generated roster (`.dev-knowledge/CLAUDE.md:112-127`; `.dev-knowledge/.claude/generated/commands-repo.md:1-13`; `.dev-knowledge/.claude/methodology-roster.md:19-21`).
- **ai-council state:** Manually lists user, repo `/override`, and plugin commands inline; only `override.md` exists locally (`ai-council/CLAUDE.md:83-96`; `ai-council/.claude/commands/override.md:1-57`).
- **corp state:** Same three classes but compressed to one plugin line; only `override.md` exists locally (`corp-monorepo/CLAUDE.md:107-118`; `corp-monorepo/.claude/commands/override.md:1-57`).
- **Classification:** SCHEMA — command availability is semantically aligned where universal, but ordering, generation, descriptions, and local-command presentation differ.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — one order (`user → repo → plugin`) and one description per shared command; hub-only `/handoff`, `/save`, and `/changelog-review` remain declared local.
- **Blast radius:** 2 consumer `CLAUDE.md` files; optional consumer roster generator/carrier if chosen.

### B4 — skills versus rules taxonomy

- **Surface:** CLAUDE §8 and `.claude/{skills,rules}/`.
- **Hub state:** Correctly distinguishes user `gotchas`, repo skills `verify`/`check-against-spec`, and repo rule `git-discipline` (`.dev-knowledge/CLAUDE.md:129-145`; `.dev-knowledge/CLAUDE.md:170-171`; `.dev-knowledge/.claude/skills/verify/SKILL.md:1-10`; `.dev-knowledge/.claude/rules/git-discipline.md:1-12`).
- **ai-council state:** Its “Skills active” region lists three `.claude/rules/` files and has no repo skill directory (`ai-council/CLAUDE.md:98-112`; `ai-council/.claude/rules/code-standards.md:1-10`; `ai-council/.claude/rules/python-env.md:1-8`; `ai-council/.claude/rules/testing.md:1-7`).
- **corp state:** Claims an automatically loaded `verify`, has a repo `gotchas` skill, and has no repo rules directory; the claimed verify provenance is not named (`corp-monorepo/CLAUDE.md:120-131`; `corp-monorepo/.claude/skills/gotchas/SKILL.md:1-4`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — separate user skills, built-in/plugin skills, repo skills, and repo rules; every item names its on-disk or plugin provenance.
- **Blast radius:** 2 consumer `CLAUDE.md` files; no skill/rule copy is implied.

### B5 — hooks-active roster currency

- **Surface:** CLAUDE §9 claims versus live `.pre-commit-config.yaml` and `.claude/settings.json`.
- **Hub state:** The 15 pre-commit ids are fully listed, but SessionStart prose omits the live `arm_hooks.py` command (`.dev-knowledge/CLAUDE.md:151-168`; `.dev-knowledge/.claude/settings.json:26-57`; `.dev-knowledge/.pre-commit-config.yaml:22-153`).
- **ai-council state:** The roster omits one active local pre-commit id; SessionStart/Stop settings are otherwise described (`ai-council/CLAUDE.md:114-134`; `ai-council/.pre-commit-config.yaml:10-54`; `ai-council/.claude/settings.json:14-44`).
- **corp state:** The roster likewise omits one active local pre-commit id; settings hooks are otherwise described (`corp-monorepo/CLAUDE.md:133-148`; `corp-monorepo/.pre-commit-config.yaml:16-80`; `corp-monorepo/.claude/settings.json:2-41`).
- **Classification:** GAP — this row documents roster currency only; the excluded audit-casing and ruff rulings are not reopened.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — regenerate or set-match each §9 roster from live config while retaining repo-local hook sets.
- **Blast radius:** 3 `CLAUDE.md` files; optional shared roster generator.

## Ruling Class C — one root-governance document shell, local substance below it

### C1 — LESSONS preamble and future-entry schema

- **Surface:** LESSONS header, preamble, heading fields, and body convention.
- **Hub state:** Canonical one-line six-field heading, newest-first instruction, last-updated line, and a split-trigger note (`.dev-knowledge/LESSONS.md:1-12`); PLAYBOOK defines the same six fields (`.dev-knowledge/protocols/PLAYBOOK.md:2454-2460`).
- **ai-council state:** Preamble declares the six-field future format but all current grandfathered entries use a two-field heading plus `CONTEXT/MISTAKE/RULE` bullets (`ai-council/LESSONS.md:1-14`; `ai-council/LESSONS.md:16-44`).
- **corp state:** Uses six-field headings but adds free-standing explanatory paragraphs after each heading (`corp-monorepo/LESSONS.md:1-17`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB for future entries only; explicitly grandfather every existing entry because LESSONS is append-only.
- **Blast radius:** 2 consumer LESSONS preambles/templates; 0 historical entries.

### C2 — JOURNAL header and preamble

- **Surface:** JOURNAL header/preamble only; entry content excluded.
- **Hub state:** Scope tag plus a 14-line semantic preamble defining purpose, bold-field shape, newest-first order, distinctions, and update protocol; it incorrectly calls LESSONS “oldest-top” while the LESSONS preamble says new entries go at the top (`.dev-knowledge/JOURNAL.md:1-20`; `.dev-knowledge/LESSONS.md:4-6`).
- **ai-council state:** H1 is followed immediately by the first entry; no scope tag, preamble, or separator precedes it (`ai-council/JOURNAL.md:1-5`).
- **corp state:** Has a leading note, but prescribes bullet fields (`- Did:` etc.) rather than the hub/ai bold-field form; CLAUDE also says “Append entry” while the fleet convention is newest-first prepend (`corp-monorepo/JOURNAL.md:1-16`; `corp-monorepo/CLAUDE.md:100-102`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — shared purpose/order/field preamble with only the repo name parameterized; no entry rewrite.
- **Blast radius:** 2 consumer `JOURNAL.md` preambles; 0 entries.

### C3 — CONTRIBUTING shell and audience

- **Surface:** Frontmatter, H1, scope tag, audience, and section skeleton.
- **Hub state:** Carries `reconciled_with`, generic H1/scope/audience, and nine top-level operational sections (`.dev-knowledge/CONTRIBUTING.md:1-14`; `.dev-knowledge/CONTRIBUTING.md:27-200`).
- **ai-council state:** Near the hub shell but lacks `reconciled_with` and has seven operational sections (`ai-council/CONTRIBUTING.md:1-16`; `ai-council/CONTRIBUTING.md:21-65`).
- **corp state:** Project-specific H1, no scope/audience block, and a local development/Tach-heavy section map (`corp-monorepo/CONTRIBUTING.md:1-19`; `corp-monorepo/CONTRIBUTING.md:39-129`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB for shell/order; retain project name and local operational appendices.
- **Blast radius:** 2 consumer `CONTRIBUTING.md` files.

### C4 — CONTRIBUTING branch and commit contract

- **Surface:** Branch prefixes, mainline posture, merge form, and Conventional-Commit grammar.
- **Hub state:** Four prefixes (`feat/fix/docs/chore`), `type(scope)`, and “never direct main; branch → commit → merge” (`.dev-knowledge/CONTRIBUTING.md:14-41`).
- **ai-council state:** Same four prefixes and `type(scope)`, explicitly requires `--no-ff`, and adds a shell-quoting caveat (`ai-council/CONTRIBUTING.md:16-25`).
- **corp state:** Adds `refactor/`, uses unscoped `type:`, includes `ci`, and says “Squash or merge as appropriate,” which conflicts with the fleet no-FF path (`corp-monorepo/CONTRIBUTING.md:9-33`; `corp-monorepo/CLAUDE.md:55-58`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — one prefix/type/`--no-ff` rule; shell quoting and domain exceptions remain local.
- **Blast radius:** 4 files — both consumer `CONTRIBUTING.md` + both consumer CLAUDE commit/branch regions.

### C5 — CONTRIBUTING backlog-id and closure semantics

- **Surface:** Touch/advance/close syntax, hook teeth, and history query.
- **Hub state:** Distinguishes `[#id]`, `advances`, and `closes`; documents done-item removal, the commit-msg gate, installation, and the implementation-history query (`.dev-knowledge/CONTRIBUTING.md:43-74`).
- **ai-council state:** One paragraph covers only `closes`, query, and done-items-leave (`ai-council/CONTRIBUTING.md:27-32`).
- **corp state:** The same compact paragraph, with no touch/advance distinction or hook install (`corp-monorepo/CONTRIBUTING.md:35-37`).
- **Classification:** GAP.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — shared closure grammar; repository id namespace is separately ruled in D2.
- **Blast radius:** 2 consumer `CONTRIBUTING.md` files.

### C6 — CONTRIBUTING gates, validators, and local operations

- **Surface:** Pre-commit setup, active-hook roster, validators, nightly/local workflows, and project-specific development guidance.
- **Hub state:** Detailed setup/validator table and hub-only nightly outcome section; its table still names the removed ARCHITECTURE ToC hook and does not list all current hook ids (`.dev-knowledge/CONTRIBUTING.md:76-170`; `.dev-knowledge/.pre-commit-config.yaml:22-153`).
- **ai-council state:** Compact setup and manual/external validator sections; its hook list is a subset of live config (`ai-council/CONTRIBUTING.md:34-53`; `ai-council/.pre-commit-config.yaml:10-54`).
- **corp state:** Development flow and a long Tach-local appendix but no complete live hook roster or generic validator section (`corp-monorepo/CONTRIBUTING.md:39-119`; `corp-monorepo/.pre-commit-config.yaml:16-80`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — generated/set-matched hook roster + common gate semantics, followed by clearly local nightly/Tach sections. Excluded ruff-form decisions remain untouched.
- **Blast radius:** 3 `CONTRIBUTING.md` files plus an optional roster generator.

### C7 — CONTRIBUTING ADR and definition-of-done pointers

- **Surface:** ADR lifecycle and session-close authority.
- **Hub state:** Has an ADR process plus a pointer-only deterministic definition-of-done section (`.dev-knowledge/CONTRIBUTING.md:172-184`; `.dev-knowledge/CONTRIBUTING.md:196-200`).
- **ai-council state:** Has a local/ecosystem ADR distinction but no definition-of-done section (`ai-council/CONTRIBUTING.md:55-65`).
- **corp state:** Has neither an ADR-process section nor a definition-of-done pointer before its final handoff section (`corp-monorepo/CONTRIBUTING.md:121-129`).
- **Classification:** GAP.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — common immutable-record and DoD pointers; local ADR namespaces/details remain local.
- **Blast radius:** 2 consumer `CONTRIBUTING.md` files.

### C8 — INSTALL ownership and carrier

- **Surface:** Root `INSTALL.md` versus hub canonical source/distribution.
- **Hub state:** No root copy; canonical content lives at `plugins/tier1-lifecycle/INSTALL.md`, and #315 specifies it as the source for a root doc-artifact carrier (`.dev-knowledge/plugins/tier1-lifecycle/INSTALL.md:1-100`; `.dev-knowledge/BACKLOG.md:187`).
- **ai-council state:** Root copy is exact to the hub source (`ai-council/INSTALL.md:1-100`).
- **corp state:** Root copy is exact to the hub source (`corp-monorepo/INSTALL.md:1-100`).
- **Classification:** GAP — content parity is complete; durable carrier ownership is not.
- **Proposed disposition:** DEFER+ticket #315 — build the manifest doc carrier instead of maintaining manual copies.
- **Blast radius:** At least 2 hub carrier/manifest files; consumer content changes only on a later source revision.

## Ruling Class D — adopt one BACKLOG hierarchy and resolve identifier scope

### D1 — E/S/task story-map hierarchy

- **Surface:** BACKLOG theme/epic, story, task schema, and validator teeth.
- **Hub state:** 7/7 themes carry `[E<n>]`, 20/20 stories carry `[S<n>]`, and 106 tasks carry `[#id] [P][size] … Done when`; representative canonical shape is at the first theme/story/task (`.dev-knowledge/BACKLOG.md:3-20`; full census `.dev-knowledge/BACKLOG.md:1-224`).
- **ai-council state:** 0/6 themes carry E ids; 9/9 stories carry S ids; 19 tasks carry the task shape; no schema validator hook is present (`ai-council/BACKLOG.md:3-31`; full census `ai-council/BACKLOG.md:1-103`; `ai-council/.pre-commit-config.yaml:10-54`).
- **corp state:** 0/5 themes carry E ids; 0/5 stories carry S ids; 13 tasks carry the task shape; no schema validator hook is present (`corp-monorepo/BACKLOG.md:3-20`; full census `corp-monorepo/BACKLOG.md:1-74`; `corp-monorepo/.pre-commit-config.yaml:16-80`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — execute the operator's #331 direction: E-prefix themes, S-prefix stories, unchanged task ids, and ship `validate_backlog` with the migrations (`.dev-knowledge/BACKLOG.md:174`; `.dev-knowledge/protocols/PLAYBOOK.md:3091-3122`).
- **Blast radius:** At least 8 files — 2 BACKLOGs, 2 pre-commit configs, 2 CLAUDE/CONTRIBUTING roster updates, and hub carrier/manifest source.

### D2 — unqualified `[#id]` collision surface

- **Surface:** Identifier allocation across repos and every unqualified cross-repo reference.
- **Hub state:** Uses its own historical sequence through #332; live ids overlap ai on #4/#19 and corp on #4 (`.dev-knowledge/BACKLOG.md:106`; `.dev-knowledge/BACKLOG.md:126`; `.dev-knowledge/BACKLOG.md:174`).
- **ai-council state:** Uses a per-repo counter beginning at #1; live #1–#11 collide with corp, and #4/#19 collide with live hub tasks (`ai-council/BACKLOG.md:31-48`; `ai-council/BACKLOG.md:85-92`).
- **corp state:** Uses a per-repo counter #1–#13; live #1–#11 collide with ai and #4 with hub (`corp-monorepo/BACKLOG.md:19-31`; `corp-monorepo/BACKLOG.md:40-63`).
- **Classification:** SCHEMA.
- **Proposed disposition:** DEFER+ticket #331/#328 — choose either a global allocator or mandatory repo-qualified references (`hub#4`, `ai#4`, `corp#4`) before automating fleet joins. Collision consumers include commit `closes` queries, closure proposals, audits, handoffs, and cross-repo prose (`.dev-knowledge/CONTRIBUTING.md:43-74`; `ai-council/CONTRIBUTING.md:27-32`; `corp-monorepo/CONTRIBUTING.md:35-37`).
- **Blast radius:** Fleet-wide and high: all 3 BACKLOG/CONTRIBUTING contracts plus closure tooling and every cross-repo reference producer.

## `.claude/` complete listing snapshot

Tracked files at the three evidence HEADs:

```text
.dev-knowledge
.claude/agents/artifact-reader.md
.claude/commands/{changelog-review,handoff,override,save}.md
.claude/generated/{commands-repo,recent-adrs}.md
.claude/methodology-roster.md
.claude/rules/git-discipline.md
.claude/settings.json
.claude/skills/check-against-spec/SKILL.md
.claude/skills/verify/{SKILL.md,verify.py}
.claude/workflows/conformance-hub.js

ai-council
.claude/{CLAUDE-FLOOR.md,CLAUDE-FLOOR.md.sha256,check_floor_hash.py}
.claude/commands/override.md
.claude/rules/{code-standards,python-env,testing}.md
.claude/settings.json
.claude/settings.local.json

corp-monorepo
.claude/{CLAUDE-FLOOR.md,CLAUDE-FLOOR.md.sha256,check_floor_hash.py}
.claude/commands/override.md
.claude/settings.json
.claude/skills/gotchas/{SKILL.md,gotchas.md}
.claude/workflows/conformance-corp.js
```

Runtime-only additions: hub has ignored `settings.local.json`, `scheduled_tasks.lock`, and an empty `worktrees/`; ai has no runtime-only `.claude` addition; corp has ignored `settings.local.json`, `scheduled_tasks.lock`, and empty `worktrees/cm-deep-vault/`. Positive file roles are anchored in the corresponding roster/config sources (`.dev-knowledge/CLAUDE.md:119-178`; `ai-council/CLAUDE.md:84-134`; `corp-monorepo/CLAUDE.md:108-148`).

Matching-name semantic diff: child floor + sidecar are exact; child guard scripts are exact; all three overrides are exact; `settings.json` differs by role/local hooks; all three `settings.local.json` bodies differ; the two scheduled-task lock values differ and are runtime state. No other relative filename occurs in two trees.

## Ruling Class E — declare `.claude` ownership and remove misleading local-state asymmetry

### E1 — unique agents/generated/rules/skills/workflows subtrees

- **Surface:** `.claude` files with no same-name peer.
- **Hub state:** Owns artifact reader, generated rosters, methodology roster, git discipline, two skills, and `conformance-hub` (`.dev-knowledge/.claude/agents/artifact-reader.md:1`; `.dev-knowledge/.claude/generated/commands-repo.md:1-13`; `.dev-knowledge/.claude/rules/git-discipline.md:1-12`; `.dev-knowledge/.claude/skills/verify/SKILL.md:1-10`; `.dev-knowledge/.claude/workflows/conformance-hub.js:1-15`).
- **ai-council state:** Owns three project rules and no agent/generated/skill/workflow files (`ai-council/.claude/rules/code-standards.md:1-10`; `ai-council/.claude/rules/python-env.md:1-8`; `ai-council/.claude/rules/testing.md:1-7`; tracked-tree census at `dd06c861`).
- **corp state:** Owns one gotchas skill and `conformance-corp`, with no agent/generated/rules files (`corp-monorepo/.claude/skills/gotchas/SKILL.md:1-4`; `corp-monorepo/.claude/workflows/conformance-corp.js:1-15`; tracked-tree census at `31f7f5de`).
- **Classification:** LOCAL-UNMARKED.
- **Proposed disposition:** DECLARE-LOCAL through #328; do not copy project organs merely for filename parity.
- **Blast radius:** 3 `.methodology.yaml` declarations/ownership-manifest entries; machinery files remain unchanged.

### E2 — `settings.json` common baseline versus local hook blocks

- **Surface:** Project Claude settings.
- **Hub state:** Common plugin/marketplace + Stop hook, plus hub-only PreToolUse, five SessionStart hooks, Workflow permission, and auto-mode settings (`.dev-knowledge/.claude/settings.json:1-81`).
- **ai-council state:** Common plugin/marketplace + Stop hook, plus child floor guard and hook-arm SessionStart pair (`ai-council/.claude/settings.json:1-45`).
- **corp state:** Same child baseline plus local conformance surfacing (`corp-monorepo/.claude/settings.json:1-56`).
- **Classification:** LOCAL-UNMARKED — shared carrier content and local hooks are mixed in one unowned JSON object.
- **Proposed disposition:** DECLARE-LOCAL — manifest the common carried keys and separately declare each repo-owned hook block; preserve settings content.
- **Blast radius:** Future #328 ownership manifest + 3 `.methodology.yaml` files; no settings rewrite required.

### E3 — `settings.local.json` is tracked only in ai-council

- **Surface:** Local permission file tracking posture.
- **Hub state:** File exists but is ignored explicitly; it contains hub-local allow entries (`.dev-knowledge/.gitignore:15-20`; `.dev-knowledge/.claude/settings.local.json:1-16`).
- **ai-council state:** File is tracked despite the blanket `.claude/*` ignore and carries machine-local allow entries (`ai-council/.gitignore:28-32`; `ai-council/.claude/settings.local.json:1-12`; tracked-tree census at `dd06c861`).
- **corp state:** File exists and is ignored; it contains corp-local allow entries (`corp-monorepo/.gitignore:28-29`; `corp-monorepo/.gitignore:52-70`; `corp-monorepo/.claude/settings.local.json:1-8`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — remove ai's local settings from tracking while retaining it on disk/ignored; shared permissions belong in `settings.json`, not a `local` file.
- **Blast radius:** 1 tracked path in ai-council; `.gitignore` already supplies the ignore rule.

### E4 — worktrees and scheduled-task lock/runtime log surface

- **Surface:** `.claude/worktrees/` and scheduled-task runtime state (the observed filename is `scheduled_tasks.lock`; no literal `schedule-task-log` file exists).
- **Hub state:** Empty ignored worktrees dir; ignored lock with one session/pid/timestamp record (`.dev-knowledge/.gitignore:15-20`; `.dev-knowledge/.git/info/exclude:8`; runtime census at `9b5c67e0`).
- **ai-council state:** Neither worktrees dir nor lock exists at the evidence HEAD/runtime census (`ai-council/.gitignore:28-32`; runtime census at `dd06c861`).
- **corp state:** Ignored lock plus an empty, unregistered `worktrees/cm-deep-vault/`; `git worktree list` reports only the primary checkout (`corp-monorepo/.gitignore:52-70`; runtime census at `31f7f5de`).
- **Classification:** LOCAL-UNMARKED.
- **Proposed disposition:** DECLARE-LOCAL as runtime ephemera; separately remove the empty corp orphan after operator approval under the no-leftovers rule.
- **Blast radius:** 0 tracked files; one local empty directory cleanup if approved.

## Ruling Class F — standardize generic ignore/genre shells; retain project payloads

### F1 — `.claude` ignore/tracking policy

- **Surface:** `.gitignore` rules governing project Claude configuration.
- **Hub state:** Tracks project config by default and ignores only `settings.local.json` and `worktrees/` in-repo (`.dev-knowledge/.gitignore:15-20`).
- **ai-council state:** Blanket-ignores `.claude/*`, re-includes only floor/sidecar/checker and `/override`; already-tracked rules/settings survive but future peer files are hidden by default (`ai-council/.gitignore:28-32`; `ai-council/.gitignore:46-50`).
- **corp state:** Blanket-ignores, then re-includes floor/sidecar/checker, `/override`, settings, skills, and workflows; rules remain hidden by default (`corp-monorepo/.gitignore:28-29`; `corp-monorepo/.gitignore:50-70`).
- **Classification:** SCHEMA.
- **Proposed disposition:** TEMPLATE-SYNC-TO-HUB — one explicit tracked-config policy with named local/runtime exclusions; conditional re-includes generated by the carrier rather than accumulated ad hoc.
- **Blast radius:** 2 consumer `.gitignore` files plus carrier tests/template.

### F2 — project-specific ignore payloads

- **Surface:** Non-generic ignore rules after Python/env/editor/cache basics.
- **Hub state:** Ignores fleet reports/state, proposal/override/coherence logs, vendored `node_modules`, and temp scratch (`.dev-knowledge/.gitignore:22-69`).
- **ai-council state:** Ignores Council output/history/inbox/data/logs (`ai-council/.gitignore:34-51`).
- **corp state:** Ignores data/extraction outputs, Hypothesis state, staging, sandbox, and logs (`corp-monorepo/.gitignore:31-70`).
- **Classification:** LOCAL-UNMARKED.
- **Proposed disposition:** DECLARE-LOCAL — retain all project payload rules; only the generic prefix and `.claude` policy synchronize.
- **Blast radius:** 3 ownership declarations; ignore payloads unchanged.

### F3 — `protocols/` mandated genre and in-folder ownership split

- **Surface:** Protocol genre presence, README pointer, and local marking.
- **Hub state:** Eleven methodology protocol files but no `protocols/README.md`; #327 requires the README/interface-genre shell (`.dev-knowledge/CLAUDE.md:39`; `.dev-knowledge/BACKLOG.md:159`; `.dev-knowledge/BACKLOG.md:171`; tracked-tree census at `9b5c67e0`).
- **ai-council state:** Four files: a README explicitly marks three Council-domain docs local and points methodology readers to the hub; this already satisfies the hub-pointer/local-marked split (`ai-council/protocols/README.md:1-22`; `ai-council/protocols/COUNCIL_INVOCATION_CONTRACT.md:1-12`; `ai-council/CLAUDE.md:155`).
- **corp state:** `protocols/` is absent despite the fleet-wide mandate (`.dev-knowledge/BACKLOG.md:159`; `.dev-knowledge/BACKLOG.md:171`; tracked-tree census at `31f7f5de`).
- **Classification:** GAP.
- **Proposed disposition:** DEFER+ticket #314/#327 — seed the canonical README genre definition, a hub pointer, and at least one corp-local interface document; add the same README shell at the hub.
- **Blast radius:** At least 3 new files — hub `protocols/README.md`, corp `protocols/README.md`, and one corp interface protocol; ai content can remain.

## Count summary

- **30 divergence rows total.**
- Classification: **3 OWNER-HUB-DIVERGENT · 10 GAP · 6 LOCAL-UNMARKED · 11 SCHEMA**.
- Proposed disposition: **22 TEMPLATE-SYNC-TO-HUB · 5 DECLARE-LOCAL · 3 DEFER+ticket**.
- Ruling-class distribution: **A 8 · B 5 · C 8 · D 2 · E 4 · F 3**.
- Confirmed/no-row parity: 12-section CLAUDE order; global/shared command baseline; `/override`; child floor/sidecar/guard; INSTALL content; VISION six-heading spine; pytest/mypy ignore behavior.

## Top 5 highest-reading-friction items

1. **CLAUDE owner=hub drift:** the operator cannot read the same eight universal regions across repos; five are missing somewhere and the surviving three are rephrased (`A1–A8`; `.dev-knowledge/CLAUDE.md:18-190`; `ai-council/CLAUDE.md:17-156`; `corp-monorepo/CLAUDE.md:20-159`).
2. **Branch/merge contract conflict:** corp says squash or merge as appropriate while the fleet contract requires branch + `--no-ff`; branch/type vocab also differs across CLAUDE and CONTRIBUTING (`A2`, `C4`; `.dev-knowledge/CONTRIBUTING.md:14-41`; `ai-council/CONTRIBUTING.md:16-25`; `corp-monorepo/CONTRIBUTING.md:9-33`).
3. **BACKLOG hierarchy + id ambiguity:** three visual schemas and 11 live ai↔corp task-id collisions make an unqualified `[#id]` unsafe in cross-repo prose (`D1–D2`; `.dev-knowledge/BACKLOG.md:1-224`; `ai-council/BACKLOG.md:1-103`; `corp-monorepo/BACKLOG.md:1-74`).
4. **Commands/skills/rules/hooks roster taxonomy:** the same daily sections mix generated versus manual rosters, rules under Skills, ambiguous verify provenance, and live hooks absent from prose (`B3–B5`; `.dev-knowledge/CLAUDE.md:112-178`; `ai-council/CLAUDE.md:83-134`; `corp-monorepo/CLAUDE.md:107-148`).
5. **LESSONS/JOURNAL entry-form split:** one-line lesson headings versus bullet/body forms, and no ai JOURNAL preamble versus corp's bullet-shape note, force a context switch at every repo boundary (`C1–C2`; `.dev-knowledge/LESSONS.md:1-12`; `ai-council/LESSONS.md:1-14`; `corp-monorepo/LESSONS.md:1-17`; `.dev-knowledge/JOURNAL.md:1-20`; `ai-council/JOURNAL.md:1-5`; `corp-monorepo/JOURNAL.md:1-16`).

## Proposed ruling sequence

1. Rule Class A once: universal regions are exact; path/test/project facts are local blocks.
2. Rule Classes B/C next: one 12-section CLAUDE shell and one root-governance shell, with generated rosters where state is machine-enumerable.
3. Execute #331's BACKLOG hierarchy direction, but settle D2 identifier scope before fleet automation consumes ids.
4. Use #328 to record legitimate `.claude`/ignore payload locality; do not copy local organs for cosmetic parity.
5. Finish the already-filed carriers: #315 for INSTALL and #314/#327 for protocols.

## Read-only close

The evidence phase modified no file in any of the three repositories. This audit is the sole authored file for the requested branch/commit. The generated audit index is intentionally not updated because the operator constrained the transaction to exactly one file; that index follow-up is outside this commit's authorized blast radius.
