---
last_reviewed: 2026-08-29
reconciled_with: handoff-process@6.3.0
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.69 — 2026-08-29 -->

> **Session boot contract for Claude Code in this repo** — auto-read at session start (ADR-53, as re-pointed by ADR-115). **Genre:** a rule lives here only if a session needs it *before it can act*; rationale, history and per-organ detail live at the home each line cites.
>
> **Budget — bytes bind. ≤24,576 B**, gated by `tests/test_claude_md_byte_cap.py`. ADR-53's ≤200 lines is kept, not replaced (`validate_doc_rot._FILE_SIZE_BUDGETS`, WARN-only) — but a line count is gameable by density, and bytes are what a session pays.
>
> **Universal rules:** `protocols/ESSENTIALS.md` (always-on); `protocols/PLAYBOOK.md` is the on-demand reference, never a boot-time read (§1).

## 1. First read (session start)
<!-- scope: meta -->
> **[HUB - methodology]** region `first-read` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=first-read owner=hub -->

In order, read:
1. This file (you're here)
2. The hub methodology protocol `ESSENTIALS.md` — Rob's universal working style (read at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer)
3. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
4. Last 5 entries of `JOURNAL.md`

`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (ESSENTIALS carries the always-on subset; a consumer never copies PLAYBOOK). If ESSENTIALS — or a PLAYBOOK section a task needs — is unavailable, proceed with the other available first-read sources and flag the gap.
<!-- methodology:end id=first-read -->

## 2. Repo identity
<!-- scope: meta -->
> **[REPO - local]** region `repo-identity` - this repo owns these lines.
<!-- methodology:start id=repo-identity owner=repo -->

- **Name:** `.dev-knowledge` · **Owner:** Rob · **Status:** active, no declared tier (repo-tier system deprecated 2026-05-23)
- **Purpose:** the universal LLM-driven development guide and methodology framework governing every project under `Dev/` — Layer 2 of the ADR-28 three-layer ecosystem model
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `README.md`, `VISION.md`, `ARCHITECTURE.md`
- **Related:** `~/.claude/` (L0 runtime config) · `.claude/` (project config) · `ObsidianVault/` (pre-sales — do not mix) · `Dev/` child repos, each owning its own `CLAUDE.md`
- **Portable layer:** root `AGENTS.md` carries the build/test/landing facts every provider reads (ADR-115, superseding ADR-53 Decision 2); this file keeps the Claude-runtime remainder and imports it below. No fact is duplicated across the two — the importer preserves ADR-53's substance

@AGENTS.md
<!-- methodology:end id=repo-identity -->

## 3. Architecture
<!-- scope: meta -->
> **[REPO - local]** region `repo-architecture` - this repo owns these lines.
<!-- methodology:start id=repo-architecture owner=repo -->

`ARCHITECTURE.md` is the structural model — read it before any structural change (ADR-51 as amended 2026-05-23). NOT a code project: markdown governance files plus hub-local validators, generators and gates; no script drives state in a child repo (§5 rule 4).

- **Where to jump:** **Ch2** organ map — which organ fires when, and how it fails · **Ch3** automation axes — cloud/nightly Routine, spec-orchestration, model routing · **Ch4** distribution — carriers, child floor, browser bundle · **Ch6** verification mesh — the nightly outcome loop.
- **The daily working mode is NOT in ARCHITECTURE.** Parallel worktree lanes, lane dispatch and the ADR-110 batch protocol are `protocols/PLAYBOOK.md` **Ch8 "Session boundaries"**.
<!-- methodology:end id=repo-architecture -->

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for dated artifacts, `docs/audits/` names also carrying a closed-enum class (`validate_hermetization.AUDIT_CLASS_ENUM`); `logs/` artifacts UPPERCASE-KEBAB, extension honest to the format ([#395]); kebab-case otherwise
> **[HUB - methodology]** region `conventions-commit-branch` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-commit-branch owner=hub -->
- **Commits & branches:** Branch prefixes are `feat/ fix/ docs/ chore/` (author-chosen branches — these four only), **plus four machine-produced lane prefixes: `worktree-<name>` (native parallel-session worktrees, `claude --worktree` / EnterWorktree), `epic/<slug>` (root-provisioned epic lanes, §14a), `claude/<slug>` (Anthropic cloud-session lanes), and `automation/<slug>` (organ-produced replication lanes — admitted 2026-08-06 by architect ruling, register `protocols/STANDING_RULINGS.md` B5). Lane branches are never self-merged and never author-invented — a brief that names a lane branch names it in one of these shapes; a new machine-produced lane prefix enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface.** Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.
<!-- methodology:end id=conventions-commit-branch -->
- **Testing:** `uv run --locked pytest -x --tb=short` — a bare `pytest` resolves nothing on a clean checkout (ADR-106 §4). In a lane run the **targeted** tests for that lane's diff; the **full suite runs once, at integration** ([#528])
- **Linting:** `uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal, not enforced (ADR-27/ADR-48)
- **File lifecycle:** append-only `LESSONS.md` + `logs/TOKEN-LOG.md`; newest-first-prepend `JOURNAL.md`; immutable ADRs / transcripts / handoffs / audits; living `README.md`, `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md` — rules and exceptions at §5. **`BACKLOG.md` is generated:** edit `tasks/`, then `gen_task_tree.py --emit-source`
- **Freshness cadence:** the stamped set is **computed, not restated here** — `canonical_docs.py::FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`. A `last_reviewed` stamp means *re-read end-to-end and confirmed accurate, or drift filed*, never merely "touched"
- **Never restate a count or roster in prose** — cite the surface that computes it (`audit.py checks`, `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, the manifest `carriers:` block). A number typed into a doc is stale at the next commit
- **Resolve a locator before you act on it** — a `file:line`, heading, SHA, branch or `[#id]` you have not opened is a claim, not evidence; run **`/preflight`** first. The most-recorded executor failure in the 2026-08-21 governance-drift audit, and it binds the auditor too
- **TDD — a build-arc standard, not a blanket mandate.** ADR-108 §B binds every build arc: RED-first witnesses, failing tests before build code, frozen after freeze; the architect freezes the pass/fail criterion *before* it, and CC may strengthen but **never weaken** it (ADR-81 amend. 2026-06-24). A blanket mandate is **not** live — Council rejected "Mandatory TDD". Say partial when it is partial
- **Spec-driven development (ADR-108 §B)** — spec before build, acceptance contract ex-ante. Live: the `check-against-spec` skill, `coherence-nudge` over `_SPEC_REGISTRY`, the `reconciled_versions` check, this file's `reconciled_with:` stamp
- **Dependencies (ADR-106):** declared by `pyproject.toml` + `uv.lock` + `.python-version`, rebuilt by `uv sync --locked`, `uv` pinned **exactly** — a uv bump is its own gated change. Every gate runs `uv run --locked …`, so a bare `python`/`pytest` in a doc is a defect, not a shorthand
- **Decision funnel (ADR-111):** every audit finding is triaged into **exactly one** of OWNED / DISCHARGED / CANDIDATE / REJECTED — no finding becomes a backlog row without triage, and the only path is CANDIDATE → intake (ADR-98) → ratification. Question routing is ADR-108 §A: the operator rules **functional** questions, the architect **technical** ones

**Out of scope:** code-level implementation → child repos · client/product/domain knowledge → the Obsidian vault · runtime config → `~/.claude/`. The in-hub Council transcript archive was **deleted 2026-07-22** by operator ruling — do not recreate it; the ADR-77 guard stays armed.

> **[HUB - methodology]** region `conventions-output-formatting` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-output-formatting owner=hub -->
- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables (`| col | col |`) as Unicode borders (`┌─┬─┐ │ └─┴─┘`) **client-side at render time**. So a bare table looks clean in the terminal but copies into browser chat as costly border glyphs (~3× the tokens), and a rule that merely bans Claude from *writing* box-drawing is a no-op (Claude already doesn't). The working fix is at the render layer: any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, which makes the TUI render it raw/un-painted so the copied text carries no borders. Same fenced-block discipline already used for Scale-S snippets (ESSENTIALS) and downloadable prompts (§2). Persistent diagrams live on the separate human-facing visualization surface (ADR-59; the ADR-51 amendment 2026-07-05 moved Mermaid out of canonical `ARCHITECTURE.md` — its codemap is now compact text), out of scope. Full rationale + `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat".
<!-- methodology:end id=conventions-output-formatting -->

## 5. Critical rules
<!-- scope: meta -->

> **[HUB - methodology]** region `critical-rules-records` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=critical-rules-records owner=hub -->
1. **`LESSONS.md` and `logs/TOKEN-LOG.md` are append-only** — never edit old entries; only append (ADR-29, ADR-39). **LESSONS.md-only exception (ADR-29 amend. 2026-07-17):** a contiguous *older* block MAY be relocated **byte-identical** into a dated `LESSONS-legacy-<span>.md` (sanctioned chronological archival — the sole way an entry leaves the active file; edits/deletes still forbidden); `logs/TOKEN-LOG.md` stays strict
2. **`JOURNAL.md` is append-only newest-first** — prepend at session wrap or workday close
3. **ADRs, transcripts, handoffs, and audits are immutable** — supersede with a new file or an in-file amendment marker; never edit in place. **ADR ratification exception (ADR-94):** an ADR's *status line* MAY be edited in place on ratification (e.g. Proposed → Accepted) — the status line is metadata, not decision content. This exception is ADR-specific and covers the status line only; ADR decision content, and transcripts / handoffs / audits in full, remain immutable.
<!-- methodology:end id=critical-rules-records -->
4. **Layer 2 never executes** — no orchestration scripts: no script drives state in a child repo (ADR-28, ADR-36). Hub-local validators, generators and gates are in scope.
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md`, deleted 2026-05-23 (ADR-38 A5), was **RECREATED 2026-08-29**: ADR-114 supersedes A5 in that one respect, making `README.md` a sanctioned Tier-1 file and this repo's canonical front door. `VISION.md` is retained, marked superseded and still tracked — the fleet-wide filename migration is a sequenced program, not a consequence of this line ([#614]).
> **[HUB - methodology]** region `critical-rules-consistency` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=critical-rules-consistency owner=hub -->
6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
<!-- methodology:end id=critical-rules-consistency -->
7. **Executable rules live in `~/.claude/` with `verify:` lines** — the fleet-wide home (ADR-54); this repo authors no new rule class outside it. **Carve-out:** `.claude/rules/` IS a live repo-local rule home — `git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES).
8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + the JOURNAL `Changes:` line replace CHANGELOG
> **[HUB - methodology]** region `critical-rules-no-leftovers` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=critical-rules-no-leftovers owner=hub -->
9. **No leftovers** — any automated or scratch-creating process (parallel-session worktree, temp file, scratch dir) removes **and verifies removal of** everything it created before it counts as done; cleanup fires even on abort. The provision→cleanup round-trip must leave the tree identical. See PLAYBOOK §Session-boundaries "No leftovers"
<!-- methodology:end id=critical-rules-no-leftovers -->

## 6. Session start protocol
<!-- scope: runtime -->
> **[HUB - methodology]** region `session-start-protocol` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=session-start-protocol owner=hub -->

1. `git status` — clean working tree?
2. `git log --oneline -5` — recent context
3. Read the **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves; same predicate as §1 item 3, so the two boot instructions select the same bundle — if continuing prior session
4. Check `BACKLOG.md` for in-progress items
5. `pytest --collect-only` — test discovery sanity check
6. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ESSENTIALS ↔ PLAYBOOK alignment; ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.
<!-- methodology:end id=session-start-protocol -->

## 7. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`): `/session-summary` — session summary + handoff · `/codex-review` — Codex review of a staged **code** diff (code only).

> **[REPO - local]** region `commands-repo-roster` - this repo owns these lines.
<!-- methodology:start id=commands-repo-roster owner=repo -->
Repo-level (`./.claude/commands/`, machine-enumerated from command-file frontmatter; regenerate: `gen_claude_rosters.py --write`):

@.claude/generated/commands-repo.md
<!-- methodology:end id=commands-repo-roster -->

`/handoff` generates a handoff per `HANDOFF_PROCESS.md` v6 (ADR-82); `/handoff-verify` is its check-time counterpart — one run of the whole live gate, one evidence block (v6 §5). `/review-closures` and `/ship` are governed by ADR-70 Tier-1 + `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle"; `/override` by ADR-85 §4, **whose local-token path the ADR-85 amendment §A2 RETIRED** — it discharges no gate. Which command when → PLAYBOOK §"Usage protocol".

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`): `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls). `verify` is **not** user-level; the live copy is hub-local, below. `boot` / `session-summary` / `handoff` / `save` are **commands** (§7), not skills, however the picker surfaces them.

> **[REPO - local]** region `skills-repo-roster` - this repo owns these lines.
<!-- methodology:start id=skills-repo-roster owner=repo -->
Repo-level (`./.claude/skills/`): `verify` (ecosystem verification, run after `pytest`) + `check-against-spec` (spec-reconciliation site enumerator). Repo-specific empirical patterns live in `LESSONS.md` — append-only; read it before structural changes.

Plugin `tier1-lifecycle@dev-knowledge-methodology` is **enabled** and drives the Tier-1 closure loop here: its `Stop` hook runs `propose_closures.py`, and it ships `/review-closures` + `/ship`. The hub is the marketplace source the children install from → `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle".
<!-- methodology:end id=skills-repo-roster -->

## 9. Hooks active
<!-- scope: runtime -->
> **[REPO - local]** region `hooks-repo-roster` - this repo owns these lines.
<!-- methodology:start id=hooks-repo-roster owner=repo -->

> **A roster, not a manual.** Per-hook rationale, exit codes and **honest limits** live in each module's docstring under `scripts/`; **failure posture** in `ARCHITECTURE.md` Ch2 and its "Validators and enforcement" chapter; the full organ inventory in the generated `ecosystem/organ-index.md`. Read those, never a copy here.

<!-- Machine-read: validate_doc_claims.extract_claimed_hooks takes the leading backtick id of every bullet from this header to the first non-bullet line. Keep it complete and contiguous. -->
Pre-commit (`.pre-commit-config.yaml`) — HUB-ONLY unless the row says otherwise:
- `normalize-dated-headers` — dated-log header normalization
- `codemap-freshness` — ARCHITECTURE codemap vs `scripts/`, regen-and-diff
- `toc-freshness-playbook` — PLAYBOOK TOC staleness
- `roster-freshness` — `.claude/methodology-roster.md` vs the deploy manifest
- `claude-rosters-freshness` — the two `@`-imported `.claude/generated/` fragments
- `audit-index-freshness` — generated `docs/audits/README.md`
- `organ-index-freshness` — generated `ecosystem/organ-index.md`; a stale index is worse than none
- `validate-hermetization` — ADR-101 tree-seal refusal on staged ADDs: top-level/genre seal, audit-name grammar, home allowlist
- `intake-index-freshness` — generated Contents block in `docs/intake/README.md`
- `check-seal-identity` — handoff-bundle seal identity at commit time
- `block-commit-on-main` — core-invariant #5 PREVENT at commit time
- `lane-contract-check` — shape gate for a generator-emitted lane contract
- `provider-registry-agreement` — the nine provider/model seams vs `ecosystem/provider-registry.yaml`
- `validate-backlog` — BACKLOG story-map schema (ADR-66)
- `audit-health` — `audit.py health`; FAIL blocks the commit, WARN informs
- `ruff` — lint gate, pinned rev == the `pyproject.toml` required-version floor
- `coherence-nudge` — **non-blocking**: registered spec changed without a version bump; always exits 0
- `backlog-id-on-close` (commit-msg) — `[#id]` required when a commit removes a task
- `backlog-filing-backpressure` (commit-msg) — a commit ADDING a task id needs a flush-left `kill-candidates:` line
- `block-ff-push` (pre-push) — refuses a non-merge commit onto main's first-parent spine; **fails CLOSED**
- `block-unanchored-push` (pre-push) — **the ADR-85 hard leg**: refuses a push to `main` whose range carries no JOURNAL anchor; **fails CLOSED**, sole escape `git push --no-verify`

**Arm the two pre-push hooks once per clone:** `pre-commit install --hook-type pre-push` — `default_install_hook_types` wires them only on a fresh install; `SessionStart`'s `arm_hooks.py` then does it idempotently.

Session hooks (`.claude/settings.json`, project-level — merges with, never replaces, the `~/.claude` set): `SessionStart` surfacing + `arm_hooks.py`; a `Stop` backpressure hook (`session_end_backpressure.py`, **advisory in full** since the ADR-85 amendment §A5 — no hard leg, cannot block a turn); the ADR-77 `PreToolUse` transcript-immutability guard, fail-closed.

Rules (`.claude/rules/`): `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end.

### Methodology-deployed roster (generated — do not hand-edit)

What the deploy tool ships to a consumer, generated from `deploy/manifest-v*.yaml` and `@`-imported below (`gen_methodology_roster.py --write`; drift-gated by `roster-freshness`). §7–§9 stay hand-authored for the hub-LOCAL surface — the items with no manifest entry.

@.claude/methodology-roster.md
<!-- methodology:end id=hooks-repo-roster -->

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->
> **[HUB - methodology]** region `antipatterns-universal` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=antipatterns-universal owner=hub -->

- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record (a *byte-identical* chronological relocation of an older block into `LESSONS-legacy-<span>.md` is NOT an edit — the ADR-29 2026-07-17 archival exception; any content change still is)
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Copying `CLAUDE.md` wholesale into `AGENTS.md`** — ADR-115 admits `AGENTS.md` as the portable instruction layer, superseding ADR-53 Decision 2; a wholesale copy measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently — carry the portable half only, and leave the Claude-runtime remainder in `CLAUDE.md`
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
<!-- methodology:end id=antipatterns-universal -->

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->
> **[REPO - local]** region `recent-adrs-roster` - this repo owns these lines.
<!-- methodology:start id=recent-adrs-roster owner=repo -->

Machine-enumerated, last 5 by number (`gen_claude_rosters.py --write`). Editorial one-liners live in `docs/decisions/README.md`; the full governance list is in `ARCHITECTURE.md`.

@.claude/generated/recent-adrs.md
<!-- methodology:end id=recent-adrs-roster -->

## 12. Section history
<!-- scope: meta -->
> **[REPO - local]** region `section-history` - this repo owns these lines.
<!-- methodology:start id=section-history owner=repo -->

> _Entries v1.0–v2.68 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.69 (2026-08-29, batch-D lane c `lane-c-000-claude-md-regenre`) — **the re-genre: reference manual → boot contract, budgeted in bytes.** The file met its `≤200 lines` claim by *density* — 240 lines but 39,588 B, **165 B/line** against this corpus's ~117 — so the cost every session pays went unbudgeted. A **24,576 B** ceiling now gates it (`tests/test_claude_md_byte_cap.py`); ADR-53's line bound is **kept, not replaced**. Every removal is a relocation to a named, verified destination. The ledger, the measurements and the owed follow-ups: `docs/audits/2026-08-29-technical-claude-md-regenre.md`.

<!-- methodology:end id=section-history -->

---

**Last updated:** 2026-08-29
**Maintained by:** Rob
