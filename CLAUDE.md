---
last_reviewed: 2026-09-17
reconciled_with: handoff-process@7.1.0
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.77 — 2026-09-08 -->

> **Session boot contract for Claude Code in this repo** — auto-read at session start (ADR-53, as re-pointed by ADR-115). **Genre:** a rule lives here only if a session needs it *before it can act*; rationale, history and per-organ detail live at the home each line cites.
>
> **Budget — bytes bind. ≤24,576 B**, gated by `tests/test_claude_md_byte_cap.py`. ADR-53's ≤200 lines is kept, not replaced (`validate_doc_rot._FILE_SIZE_BUDGETS`, WARN-only) — but a line count is gameable by density, and bytes are what a session pays.
>
> **Universal rules:** this file carries the always-on subset; `protocols/PLAYBOOK.md` is the on-demand reference, never a boot-time read (§1). `protocols/ESSENTIALS.md` was **deleted 2026-09-14** (`[#628]`) — its doctrine lives in PLAYBOOK; do not look for it.

## 1. First read (session start)
<!-- scope: meta -->
> **[HUB - methodology]** region `first-read` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=first-read owner=hub -->

In order, read:
1. This file (you're here)
2. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6/v7 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
3. Last 5 entries of `JOURNAL.md`

`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (this file carries the always-on subset; a consumer never copies PLAYBOOK). If a PLAYBOOK section a task needs is unavailable, proceed with the other available first-read sources and flag the gap.
<!-- methodology:end id=first-read -->

## 2. Repo identity
<!-- scope: meta -->
> **[REPO - local]** region `repo-identity` - this repo owns these lines.
<!-- methodology:start id=repo-identity owner=repo -->

- **Name:** `.dev-knowledge` · **Owner:** Rob · **Status:** active, no declared tier (repo-tier system deprecated 2026-05-23)
- **Purpose:** the universal LLM-driven development guide and methodology framework governing every project under `Dev/` — Layer 2 of the ADR-28 three-layer ecosystem model
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `README.md`, `ARCHITECTURE.md`
- **Related:** `~/.claude/` (L0 runtime config) · `.claude/` (project config) · `Dev/` child repos, each owning its own `CLAUDE.md`
- **Portable layer:** root `AGENTS.md` carries the build/test/landing facts every provider reads (ADR-115, superseding ADR-53 Decision 2); this file keeps the Claude-runtime remainder and imports it below. No fact is duplicated across the two — the importer preserves ADR-53's substance

@AGENTS.md
<!-- methodology:end id=repo-identity -->

## 3. Architecture
<!-- scope: meta -->
> **[REPO - local]** region `repo-architecture` - this repo owns these lines.
<!-- methodology:start id=repo-architecture owner=repo -->
`ARCHITECTURE.md` is the structural model — read it before any structural change (ADR-51). NOT a code project: markdown governance plus hub-local validators, generators and gates; no script drives state in a child repo (§5 rule 4). The daily working mode (worktree lanes, ADR-110 batch protocol) is `protocols/PLAYBOOK.md` Ch8 "Session boundaries".
<!-- methodology:end id=repo-architecture -->

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for dated artifacts, `docs/audits/` names also carrying a closed-enum class (`validate_hermetization.AUDIT_CLASS_ENUM`); `logs/` artifacts UPPERCASE-KEBAB, extension honest to the format ([#395]); kebab-case otherwise
> **[HUB - methodology]** region `conventions-commit-branch` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-commit-branch owner=hub -->
- **Commits & branches:** Branch prefixes are a closed enum — author-chosen `feat/ fix/ docs/ chore/`, plus four machine-produced lane prefixes `worktree-<name>`, `epic/<slug>`, `claude/<slug>`, `automation/<slug>` (each admitted only by a recorded ruling, never invented in passing — full provenance: PLAYBOOK Ch3 "Branch prefixes — the closed enum"). Commit **types** follow Conventional Commits plus `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.
<!-- methodology:end id=conventions-commit-branch -->
- **Testing:** `uv run --locked pytest -x --tb=short` — a bare `pytest` resolves nothing on a clean checkout (ADR-106 §4). In a lane run the **targeted** tests for that lane's diff; the **full suite runs once, at integration** ([#528])
- **Linting:** `uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal, not enforced (ADR-27/ADR-48)
- **File lifecycle:** append-only `LESSONS.md` + `logs/TOKEN-LOG.md`; newest-first-prepend `JOURNAL.md`; immutable ADRs / transcripts / handoffs / audits; living `README.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md` — rules and exceptions at §5. **`BACKLOG.md` is generated:** edit `tasks/`, then `gen_task_tree.py --emit-source`
- **Freshness cadence:** the stamped set is **computed, not restated here** — `canonical_docs.py::FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`. A `last_reviewed` stamp means *re-read end-to-end and confirmed accurate, or drift filed*, never merely "touched"
- **Never restate a count or roster in prose** — cite the surface that computes it (`audit.py checks`, `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, the manifest `carriers:` block). A number typed into a doc is stale at the next commit
- **Resolve a locator before you act on it** — a `file:line`, heading, SHA, branch or `[#id]` you have not opened is a claim, not evidence; run **`/preflight`** first. The most-recorded executor failure in the 2026-08-21 governance-drift audit, and it binds the auditor too
- **TDD — a build-arc standard, not a blanket mandate.** ADR-108 §B binds every build arc: RED-first witnesses, failing tests before build code, frozen after freeze; the architect freezes the pass/fail criterion *before* it, and CC may strengthen but **never weaken** it (ADR-81 amend. 2026-06-24). A blanket mandate is **not** live — Council rejected "Mandatory TDD". Say partial when it is partial
- **Spec-driven development (ADR-108 §B)** — spec before build, acceptance contract ex-ante. Live: the `check-against-spec` skill, `coherence-nudge` over `_SPEC_REGISTRY`, the `reconciled_versions` check, this file's `reconciled_with:` stamp
> **[HUB - methodology]** region `conventions-library-first` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-library-first owner=hub -->
- **Library-first:** before any build — stdlib > established dependency > stabilized project > industry pattern; hand-roll only on a MEASURED divergence on this repo, recorded so it is not relitigated. Every plan names its library-first check or gives a one-line reason for its absence.
<!-- methodology:end id=conventions-library-first -->
- **Dependencies (ADR-106):** declared by `pyproject.toml` + `uv.lock` + `.python-version`, rebuilt by `uv sync --locked`, `uv` pinned **exactly** — a uv bump is its own gated change. Every gate runs `uv run --locked …`, so a bare `python`/`pytest` in a doc is a defect, not a shorthand
- **Decision funnel (ADR-111):** every audit finding is triaged into **exactly one** of OWNED / DISCHARGED / CANDIDATE / REJECTED — no finding becomes a backlog row without triage, and the only path is CANDIDATE → intake (ADR-98) → ratification. Question routing is ADR-108 §A: the operator rules **functional** questions, the architect **technical** ones

**Out of scope:** code-level implementation → child repos · runtime config → `~/.claude/`. The in-hub Council transcript archive was **deleted 2026-07-22** by operator ruling — do not recreate it; the ADR-77 guard stays armed.

> **[HUB - methodology]** region `conventions-output-formatting` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-output-formatting owner=hub -->
- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables as Unicode borders **client-side at render time**, so a bare table looks clean in the terminal but copies into browser chat at ~3× the tokens. Any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, so the TUI renders it raw/un-painted. Full rationale, the Mermaid/diagram carve-out and `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat" (this bullet is the point-of-use rule; that subsection is the rationale authority).
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
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md`, deleted 2026-05-23 (ADR-38 A5), was **RECREATED 2026-08-29**: ADR-114 supersedes A5 in that one respect, making `README.md` a sanctioned Tier-1 file and this repo's canonical front door. `VISION.md` is retained, marked superseded, and relocated to `docs/archive/VISION.md` at the hub ([#614] lane-e-5) — still tracked; the fleet-wide migration remains sequenced.
> **[HUB - methodology]** region `critical-rules-consistency` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=critical-rules-consistency owner=hub -->
6. **Keep files consistent** — a hub region's body in `CLAUDE.md` stays byte-identical to its `templates/claude-regions/*.md` source; divergence breaks deploy parity
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
3. Read the **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves; same predicate as §1 item 2, so the two boot instructions select the same bundle — if continuing prior session
4. Check `BACKLOG.md` for in-progress items
5. `pytest --collect-only` — test discovery sanity check
6. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.
<!-- methodology:end id=session-start-protocol -->

## 7. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`): `/session-summary` — session summary + handoff · `/codex-review` — Codex review of a staged **code** diff (code only).

> **[REPO - local]** region `commands-repo-roster` - this repo owns these lines.
<!-- methodology:start id=commands-repo-roster owner=repo -->
Repo-level commands are machine-enumerated in `.claude/generated/commands-repo.md` — read it, or list `.claude/commands/`, when picking a command. Which command when → PLAYBOOK §"Usage protocol".
<!-- methodology:end id=commands-repo-roster -->

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`): `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls). `verify` is **not** user-level; the live copy is hub-local, below. `boot` / `session-summary` / `handoff` / `save` are **commands** (§7), not skills, however the picker surfaces them.

> **[REPO - local]** region `skills-repo-roster` - this repo owns these lines.
<!-- methodology:start id=skills-repo-roster owner=repo -->
Repo-level skills live in `.claude/skills/<name>/SKILL.md` — list that directory when a skill-shaped task arises; run `verify` after `pytest`. Repo-specific empirical patterns live in `LESSONS.md` — append-only; read it before structural changes. Plugin `tier1-lifecycle@dev-knowledge-methodology` is enabled (its `Stop` hook runs `propose_closures.py`; it ships `/review-closures` + `/ship`).
<!-- methodology:end id=skills-repo-roster -->

## 9. Hooks active
<!-- scope: runtime -->
> **[REPO - local]** region `hooks-repo-roster` - this repo owns these lines.
<!-- methodology:start id=hooks-repo-roster owner=repo -->

Gates block: a FAIL is fixed, never bypassed. Pre-commit (`.pre-commit-config.yaml`) hook ids — a hook's one-line purpose is its `name:` there, its rationale, exit codes and honest limits are its `scripts/` module docstring, and the armed-vs-`stages: [manual]` state is that file's header and `ecosystem/organ-index.md`:
- `normalize-dated-headers`
- `codemap-freshness`
- `toc-freshness-playbook`
- `roster-freshness`
- `claude-rosters-freshness`
- `audit-index-freshness`
- `organ-index-freshness`
- `doc-counts-pytest-freshness`
- `validate-hermetization`
- `audit-title-gate`
- `intake-index-freshness`
- `check-seal-identity`
- `block-commit-on-main`
- `lane-contract-check`
- `derived-copies-rebind`
- `provider-registry-agreement`
- `validate-backlog`
- `row-archive-proof`
- `graph-rebuild`
- `graph-orphan-census`
- `graph-task-coverage`
- `graph-process-list`
- `impacted-tests-guard`
- `decision-coverage`
- `graph-edge-class-census`
- `quality-requirements-freshness`
- `prepend-order`
- `dispatch-conformance`
- `audit-health`
- `ruff`
- `coherence-nudge`
- `backlog-id-on-close` (commit-msg)
- `backlog-filing-backpressure` (commit-msg)
- `commit-message-type-prefix` (commit-msg)
- `block-ff-push` (pre-push)
- `block-unanchored-push` (pre-push)

Session hooks and their wiring: `.claude/settings.json` (`SessionStart` `arm_hooks.py` arms the pre-push hooks; `Stop` backpressure, advisory). Rules: `.claude/rules/git-discipline.md` — mandatory commit after every file edit; clean working tree at session end.

For deploy/manifest work — which commands, hooks and config a deployed consumer receives — read `.claude/methodology-roster.md`.
<!-- methodology:end id=hooks-repo-roster -->

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->
> **[HUB - methodology]** region `antipatterns-universal` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=antipatterns-universal owner=hub -->

- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record (a *byte-identical* chronological relocation of an older block into `LESSONS-legacy-<span>.md` is NOT an edit — the ADR-29 2026-07-17 archival exception; any content change still is)
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Copying `CLAUDE.md` wholesale into `AGENTS.md`** — ADR-115 admits `AGENTS.md` as the portable instruction layer, superseding ADR-53 Decision 2; a wholesale copy measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently — carry the portable half only, and leave the Claude-runtime remainder in `CLAUDE.md`
- **Duplicating content between files** — a hub region restated by hand instead of relocated, or PLAYBOOK detail copied verbatim elsewhere; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
<!-- methodology:end id=antipatterns-universal -->

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->
> **[REPO - local]** region `recent-adrs-roster` - this repo owns these lines.
<!-- methodology:start id=recent-adrs-roster owner=repo -->
Last 5 ADRs by number: `.claude/generated/recent-adrs.md`; editorial one-liners in `docs/decisions/README.md`.
<!-- methodology:end id=recent-adrs-roster -->

## 12. Section history
<!-- scope: meta -->
> **[REPO - local]** region `section-history` - this repo owns these lines.
<!-- methodology:start id=section-history owner=repo -->
History of this file's revisions: `docs/audits/2026-09-05-technical-claude-md-section-history-ledger.md`.
<!-- methodology:end id=section-history -->

---

**Last updated:** 2026-09-17
**Maintained by:** Rob
