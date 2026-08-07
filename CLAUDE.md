---
last_reviewed: 2026-08-07
reconciled_with: handoff-process@6.1.0
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.53 — 2026-08-07 -->

> **Session contract for Claude Code in this repo.** Read on every session start (auto). Single canonical agent-instruction file (≤200 lines). Per ADR-53.
>
> **For universal rules:** read `protocols/ESSENTIALS.md`; consult `protocols/PLAYBOOK.md` on demand (the universal-protocols reference, not a boot-time read — §1).

## 1. First read (session start)
<!-- scope: meta -->
> **[HUB - methodology]** region `first-read` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=first-read owner=hub -->

In order, read:
1. This file (you're here)
2. The hub methodology protocol `ESSENTIALS.md` — Rob's universal working style (read at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer)
3. Most recent `docs/handoffs/*/` bundle — start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
4. Last 5 entries of `JOURNAL.md`

`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (ESSENTIALS carries the always-on subset; a consumer never copies PLAYBOOK). If ESSENTIALS — or a PLAYBOOK section a task needs — is unavailable, proceed with the other available first-read sources and flag the gap.
<!-- methodology:end id=first-read -->

## 2. Repo identity
<!-- scope: meta -->
> **[REPO - local]** region `repo-identity` - this repo owns these lines.
<!-- methodology:start id=repo-identity owner=repo -->

- **Name:** `.dev-knowledge`
- **Complexity:** medium (informal; repo-tier system deprecated 2026-05-23 — no declared tier)
- **Status:** active
- **Purpose:** Universal LLM-driven development guide and methodology framework; governs all projects under `Dev/`; Layer 2 of the ADR-28 three-layer ecosystem model
- **Owner:** Rob
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`, `ARCHITECTURE.md`
- **Related locations:** `~/.claude/` (Claude Code runtime config); `.claude/` (project-level config); `ObsidianVault/` (pre-sales, do not mix); `Dev/` (child repos, each has own `CLAUDE.md`)
<!-- methodology:end id=repo-identity -->

## 3. Architecture
<!-- scope: meta -->
> **[REPO - local]** region `repo-architecture` - this repo owns these lines.
<!-- methodology:start id=repo-architecture owner=repo -->

See `ARCHITECTURE.md` for the structural model; read it before structural changes (required for every repo, per ADR-51 as amended 2026-05-23). NOT a code project — markdown governance files + read-only validators only.

- **Chapter pointers** (`ARCHITECTURE.md` is a six-chapter map; jump to the topic — doctrine lives there + the cited ADRs, never resident here): cloud/nightly Routine + spec-orchestration + t-shirt model routing → **Ch3 Automation axes**, the nightly outcome loop → **Ch6 Verification mesh**; which organ fires when (hooks/skills/commands/agents/gates) → **Ch2 Organ map**; what's distributed where (carriers / child floor / browser bundle) → **Ch4 Distribution & transfer**.
<!-- methodology:end id=repo-architecture -->

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs (`VISION.md`, `CLAUDE.md`, etc.); `ADR-NN-topic.md` for decisions; `YYYY-MM-DD-slug.md` for dated artifacts; `council-out-YYYYMMDD_HHMMSS-topic.md` for Council CLI output; kebab-case otherwise
> **[HUB - methodology]** region `conventions-commit-branch` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-commit-branch owner=hub -->
- **Commits & branches:** Branch prefixes are `feat/ fix/ docs/ chore/` (author-chosen branches — these four only), **plus four machine-produced lane prefixes: `worktree-<name>` (native parallel-session worktrees, `claude --worktree` / EnterWorktree), `epic/<slug>` (root-provisioned epic lanes, §14a), `claude/<slug>` (Anthropic cloud-session lanes), and `automation/<slug>` (organ-produced replication lanes — admitted 2026-08-06 by architect ruling, register `protocols/STANDING_RULINGS.md` B5). Lane branches are never self-merged and never author-invented — a brief that names a lane branch names it in one of these shapes; a new machine-produced lane prefix enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface.** Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.
<!-- methodology:end id=conventions-commit-branch -->
- **Testing:** `pytest -x --tb=short`
- **Linting:** `ruff check --fix` (manual / via `/save`); `ruff check` is also enforced as a pre-commit gate (see §9) — violations block commits
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal only; not enforced (ADR-27; enforcement withdrawn per ADR-48)
- **File lifecycle:** Append-only: `LESSONS.md` (never edit; a contiguous older block MAY relocate byte-identical to `LESSONS-legacy-<span>.md` — ADR-29 2026-07-17 chronological-archival exception), `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file; an ADR *status line* is editable in place on ratification per §5 item 3 / ADR-94). Living: `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` (update in place).
- **Freshness cadence:** the living docs `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS` carry a `last_reviewed` frontmatter stamp meaning *re-read end-to-end and confirmed accurate (or drift filed)* — **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last edit (edited-but-not-re-reviewed) and warns past a 30-day backstop. Bump `last_reviewed` only after a genuine review. See PLAYBOOK "Canonical-file freshness cadence".

**Out of scope for this repo:**
- Code-level implementation → child repos (corp-monorepo, ai-council, etc.)
- Client/product/domain knowledge → Obsidian vault
- Project-specific CLAUDE.md content → each repo owns its own
- Claude Code runtime config → `~/.claude/`
- Council debate transcripts: the in-hub archive `docs/decisions/transcripts/` was **deleted 2026-07-22** (operator ruling — council-in-ADR output retired; decisions live in the ADRs, git history retains the raw transcripts; ADR-77 guard stays armed). Do not recreate it.

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
4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md` deleted 2026-05-23 (deprecated per ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo) — do not recreate it.
> **[HUB - methodology]** region `critical-rules-consistency` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=critical-rules-consistency owner=hub -->
6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
<!-- methodology:end id=critical-rules-consistency -->
7. **No executable rules in this repo** — those go in `~/.claude/` with `verify:` lines
8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + JOURNAL `Changes:` line replace CHANGELOG
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
3. Read most recent handoff if continuing prior session
4. Check `BACKLOG.md` for in-progress items
5. `pytest --collect-only` — test discovery sanity check
6. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ESSENTIALS ↔ PLAYBOOK alignment; ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.
<!-- methodology:end id=session-start-protocol -->

## 7. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`):
- `/session-summary` — generate token-efficient session summary + handoff
- `/codex-review` — invoke Codex review on a staged **code** diff (code only)

> **[REPO - local]** region `commands-repo-roster` - this repo owns these lines.
<!-- methodology:start id=commands-repo-roster owner=repo -->
Repo-level (`./.claude/commands/` — machine-enumerated from command-file frontmatter, generated like §9's roster; regenerate: `python scripts/gen_claude_rosters.py --write`):

@.claude/generated/commands-repo.md
<!-- methodology:end id=commands-repo-roster -->

`/handoff` generates a handoff per `HANDOFF_PROCESS.md` v6 (ADR-82); `/handoff-verify` is its check-time counterpart — one CC-side run of the whole live gate, one evidence block (v6 §5; R1). Deployed methodology commands — `/review-closures`, `/ship`, `/override` — are enumerated in the generated roster (§9, `@`-imported); governance stays at canonical homes: ADR-70 Tier-1 + §8 / `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" ([#76] — the hub uses the plugin's, not a hub-local duplicate) for `/review-closures` + `/ship` (the `/ship` worktree-refusal is the seed-state `LESSONS.md` 2026-06-19 lesson); ADR-85 §4 for `/override` — **but note the ADR-85 amendment 2026-08-03 §A2 RETIRED that local-token path**: `/override` no longer discharges the ADR-85 obligation (the Stop hook is advisory in full and has nothing to override), and the sole escape for the pre-push hard leg is `git push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop.

(When to invoke each + auto-vs-manual for hooks: PLAYBOOK §"Usage protocol: which command / hook, when".)

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls)

(The `verify` skill is **not** user-level — the live copy is hub-local, listed under Repo-level below.)

(`boot`/`session-summary`/`handoff`/`save` are **commands**, not skills — see §7; current Claude Code also surfaces commands in its skill picker, but their files live under `commands/`, not `skills/`.)

> **[REPO - local]** region `skills-repo-roster` - this repo owns these lines.
<!-- methodology:start id=skills-repo-roster owner=repo -->
Repo-level (`./.claude/`):
- `.claude/skills/` holds `verify` (ecosystem verification scripts, run after `pytest`) + `check-against-spec` (spec-reconciliation site enumerator). Repo-specific empirical patterns also live in `LESSONS.md` (append-only) — read it before structural changes; universal gotchas are the user-level `gotchas` skill above. A repo-specific gotchas skill, if added, goes under `.claude/skills/gotchas/`.

Plugin:
- `tier1-lifecycle@dev-knowledge-methodology` is **enabled** (`.claude/settings.json`) and drives the Tier-1 closure loop here — its `Stop` hook runs `propose_closures.py` and it ships the `/review-closures` + `/ship` commands (§7/§9). The hub is the marketplace source the child repos install from; full distribution model in `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" + `plugins/tier1-lifecycle/INSTALL.md`.
<!-- methodology:end id=skills-repo-roster -->

## 9. Hooks active
<!-- scope: runtime -->
> **[REPO - local]** region `hooks-repo-roster` - this repo owns these lines.
<!-- methodology:start id=hooks-repo-roster owner=repo -->

Pre-commit (`.pre-commit-config.yaml`):
- `normalize-dated-headers` — dated-log header normalization
- `codemap-freshness` — ARCHITECTURE compact-text codemap vs `scripts/` staleness check (format-agnostic regen-and-diff; the codemap is compact text since the ADR-51 amendment 2026-07-05, gate retained)
- `toc-freshness-playbook` — PLAYBOOK.md TOC staleness check (same `scripts/toc/` tool, PLAYBOOK target)
- `roster-freshness` — regen-and-diff gate for `.claude/methodology-roster.md` vs `deploy/manifest-v*.yaml` (`gen_methodology_roster.py --check`; blocks a hand-edited or manifest-stale roster); HUB-ONLY (n=1), [#244] P3
- `claude-rosters-freshness` — regen-and-diff gate for the two `@`-imported CLAUDE.md fragments `.claude/generated/{commands-repo,recent-adrs}.md` vs disk (`gen_claude_rosters.py --check`; fires on the command files / ADR headers / the fragments); HUB-ONLY, [#258] phase-2
- `audit-index-freshness` — regen-and-diff gate for the generated `docs/audits/README.md` index vs `docs/audits/*.md` (`gen_audit_index.py --check`; shape-agnostic — survives the #269 count-tiered reshape); guards against silent index rot (census A-2 ruling); HUB-ONLY
- `validate-hermetization` (#306, HUB-ONLY) — ADR-101 tree-seal refusal gate, prospective-only on staged ADDs (existing files grandfathered): Rule A blocks a new unsanctioned Tier-1 top-level dir/file-class or `docs/<genre>/` folder; Rule B blocks an off-grammar/mis-cased/off-enum `docs/audits/*.md` name (ADR-101 R3/R4, name-shape only); `scripts/validate_hermetization.py`, bypass `--no-verify`
- `intake-index-freshness` (#307, HUB-ONLY) — regen-and-diff gate for the generated status-grouped Contents block in `docs/intake/README.md` vs `docs/intake/*.md` frontmatter `status:` (`gen_intake_index.py --check`; fires on any intake status-change/add/remove or the generator; never moves a file); guards against silent index rot
- `check-seal-identity` ([#475], HUB-ONLY) — bundle seal-identity gate at commit time: runs `gen_handoff.verify_seal_identity` (reused, not reimplemented) over the bundle dir of every staged `docs/handoffs/**` file, so a hand-renamed directory / edited Slug row / copied bundle whose internal slug names a DIFFERENT directory cannot become an immutable committed artifact (the [#473] seal-time refusal covered only the machine generation path). Fires only when such files are staged; exit 0 clean / 1 violation / 2 internal error (an error BLOCKS, never a silent pass); `scripts/check_seal_identity.py`, bypass `--no-verify`. Honest limit: catches the Slug row vs directory, not a stale P0c/P3/P8 locator inside a correctly-labelled bundle
- `validate-backlog` — BACKLOG.md story-map schema (ADR-66)
- `audit-health` — self-conformance gate: `audit.py health` (FAIL blocks the commit, WARN informs); added by [#69]
- `ruff` — lint gate: `ruff check` (gate mode; blocks on violations); fleet-canonical pinned-rev hook (`astral-sh/ruff-pre-commit` @ v0.15.5, matching both consumers), rev == the `pyproject.toml` `[tool.ruff]` required-version floor (>=0.15.5); added by [#13]
- `coherence-nudge` — **non-blocking** forgotten-version-bump nudge: a registered spec (`_SPEC_REGISTRY`) changed-without-a-version-bump prints a stdout nudge + logs `logs/COHERENCE-NUDGE.log`; always exits 0 (a nudge, not a gate); pairs with the `reconciled_versions` audit check
- `backlog-id-on-close` (commit-msg) — require `[#id]` when a commit removes a backlog task
- `backlog-filing-backpressure` (commit-msg) — the add-side sibling of `backlog-id-on-close` (filing-backpressure doctrine, 2026-07-08 ruling; PLAYBOOK §10): a commit that ADDS a new BACKLOG task id must carry a `kill-candidates:` line (≥1 existing `#id`, or `none — <reason>`) — BLOCK if absent; also emits the advisory ADR-98 intake-id WARN on a new L-sized new-feature epic (#279). `scripts/check_backlog_filing.py`; HUB-ONLY; proposals only (never auto-removes); fail-open-loud on git error.
- `block-ff-push` (pre-push) — the PREVENT half of core-invariant #5 ([#153]): refuses a push that would put a non-merge commit on main's first-parent spine (a direct-to-main commit or a true FF merge); a `--no-ff` merge passes. `scripts/block_ff_push.py`, HUB-ONLY, **fails CLOSED (exit 2) on internal error** since the ADR-85 amendment 2026-08-03 §A6 — it previously printed `degraded — allowing push` and returned 0, silently auto-allowing the exact push it exists to refuse; bypass `git push --no-verify` (the `no_ff_merges` audit WARN stays the post-hoc backstop). Delegates the scan to `validate_no_ff.find_violations` (one shared FF-signature). **One-time local activation: `pre-commit install --hook-type pre-push`** (the config's `default_install_hook_types` only wires it on a fresh install). `validate_no_ff` stays the detect-and-surface WARN; this is the distinct prevent organ (separate file, so validate_no_ff's never-gates contract is preserved).
- `block-unanchored-push` (pre-push, HUB-ONLY) — **the ADR-85 HARD leg** (amendment 2026-08-03 §A5): refuses a push targeting `main` whose range carries first-parent spine entries with **no JOURNAL anchor**. Discharge is range-level — a JOURNAL entry naming ≥1 SHA the range **introduced** (a merge cannot name its own hash, so the entry names a commit it brings in). It lives at pre-push and not at `Stop` because a Stop hook's unit is a model-turn boundary that the host force-ends after N consecutive blocks — **an organ that can be exhausted cannot carry teeth** (witnessed 2026-08-03: nine identical firings, zero enforcement pressure, silent auto-bypass). `scripts/block_unanchored_push.py`; **fails CLOSED (exit 2)**; sole escape `git push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop (a gap is a **FAIL**, not a WARN). Shares its range resolver with `block_ff_push` and its anchoring predicate with the backstop via `scripts/journal_anchor.py`, so the organs cannot drift. **One-time local activation: `pre-commit install --hook-type pre-push`.**

Session hooks (`.claude/settings.json`, project-level — merges with, does not replace, the `~/.claude` hooks): `SessionStart` surfacing (`fleet_health.py` Tier-2 fleet digest [#72] + `surface_triage.ps1` nightly-triage + `billing_leak_sentinel.ps1` [#101] + `changelog_sentinel.py` [#113]) plus `arm_hooks.py` (RF-2 hub self-arm — idempotent `pre-commit install` of the 3 hook types; asserted by `audit.py` check_hooks_armed), a `Stop` backpressure hook (`session_end_backpressure.py` — **advisory in full** since the ADR-85 amendment 2026-08-03 §A5; it has no hard leg and cannot block a turn, and its outer error is now loud rather than a silent `return 0`), and the ADR-77 `PreToolUse` transcript-immutability guard (`block_immutable_edits.py`) — each fail-soft (surfacing) or fail-closed (the guard) per its row. **Full live organ inventory (trigger × layer × failure posture) → `ARCHITECTURE.md` Ch2 Organ map.** The Tier-1 closure loop runs via the enabled `tier1-lifecycle` plugin (`Stop → propose_closures.py`; detect-and-propose, never mutates BACKLOG) + the global `~/.claude` `surface-closures.ps1` L0 surfacing — not hub-local `settings.json` (the 5c convergence; ARCHITECTURE "Tier-1 self-enforcing lifecycle").

**logs/ artifact naming (ruled 2026-07-22, [#395]):** UPPERCASE-KEBAB stem for every `logs/` artifact; the extension stays honest to the format — `.md` human-readable digests, `.log` line-append streams, `.jsonl` event streams (an extension is a format claim, so `.log`/`.jsonl` are not restyled to `.md`). Dot-prefixed one-shot tokens (`.session-override-token`) are exempt from the stem rule — hidden-file semantics outrank the visual convention. Conformed 2026-07-22: `COHERENCE-NUDGE.log`, `PARITY-EVENTS.jsonl`; every other artifact already conforms (`TOKEN-LOG.md`, `PROPOSALS-*.md`, the UPPERCASE digests).

Rules (`.claude/rules/`):
- `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end

### Methodology-deployed roster (generated — do not hand-edit)

The deployed methodology corpus (the commands / hooks / config the deploy tool ships to a consumer) is machine-generated from `deploy/manifest-v*.yaml` `components:[].roster` and `@`-imported below — regenerated-from-source, not review-stamped (deliberately OUT of the freshness gate; regenerate: `python scripts/gen_methodology_roster.py --write`). §7–§9 stay hand-authored for the hub-LOCAL surface (items with no manifest entry). Drift-gated by the `roster-freshness` pre-commit hook.

@.claude/methodology-roster.md
<!-- methodology:end id=hooks-repo-roster -->

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->
> **[HUB - methodology]** region `antipatterns-universal` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=antipatterns-universal owner=hub -->

- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record (a *byte-identical* chronological relocation of an older block into `LESSONS-legacy-<span>.md` is NOT an edit — the ADR-29 2026-07-17 archival exception; any content change still is)
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Narrating or managing AGENTS.md** — AGENTS.md is retired (ADR-53); CLAUDE.md is the single instruction file
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
<!-- methodology:end id=antipatterns-universal -->

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->
> **[REPO - local]** region `recent-adrs-roster` - this repo owns these lines.
<!-- methodology:start id=recent-adrs-roster owner=repo -->

Machine-enumerated (last 5 by number, from `docs/decisions/ADR-*.md` headers; regenerate: `python scripts/gen_claude_rosters.py --write`). Editorial one-liners live in `docs/decisions/README.md`; full governance list in `ARCHITECTURE.md`.

@.claude/generated/recent-adrs.md
<!-- methodology:end id=recent-adrs-roster -->

## 12. Section history
<!-- scope: meta -->
> **[REPO - local]** region `section-history` - this repo owns these lines.
<!-- methodology:start id=section-history owner=repo -->

> _Entries v1.0–v2.48 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.53 (2026-08-07, PRE-2 arc) — **the fourth enum site is closed.** v2.52 below left
  `~/.claude/rules/core-invariants.md` §5 standing at "three" because core-invariant #6 bars a
  unilateral global-infra edit; the architect ruled that specific edit in the PRE-2 brief, so it
  landed and fleet-wide enum drift is now **0 sites**. No content change in this file — v2.52's
  text is accurate as the record of what v2.52 did, and is left alone rather than rewritten,
  which is the same append-not-amend discipline STANDING_RULINGS B6 landed for JOURNAL anchors
  in this same window. L10 version 2.52→2.53; `last_reviewed` unchanged at 2026-08-07 (the
  genuine end-to-end re-read behind it happened this morning and no §-content moved since).
- v2.52 (2026-08-07) — §4's branch-prefix enum says **four** machine-produced lane prefixes, admitting `automation/<slug>` alongside the three. This is drift repair, not a decision: the ruling was made 2026-08-06 and executed the same night at `3879d28b`, which landed the fourth member into `scripts/validate_branch_naming.py` (`LANE_PREFIXES`, `KIND_AUTOMATION_LANE`, an ORDER-pinning test) and recorded it at `protocols/STANDING_RULINGS.md` B5 — the register entry the enum's own governing clause demands. What that commit did *not* do is update the prose that states the enum, so the canonical instruction file spent one night asserting "three" while the validator accepted four. Caught by this morning's integration spot-check of that very commit, which is the [#503] failure class ("the thing it describes moved underneath it") arriving in the file that boots every session. Repaired at all three in-repo sites in one commit, source-of-truth first: the hub carrier `templates/claude-regions/conventions-commit-branch.md`, this file's `conventions-commit-branch` region (byte-coupled to the carrier by `test_hub_region_bodies_still_byte_match_the_templates`), and `CONTRIBUTING.md` "Branch naming". A FOURTH site is knowingly left standing — `~/.claude/rules/core-invariants.md` §5 still says three — because core-invariant #6 makes global-infra edits exception-with-ruling and no ruling covers this one; it is filed to the operator rather than fixed. Phrased with no new normative keyword, so `silent_rule_ratchet` holds at 441 ≤ 441. L10 version 2.51→2.52. Genuine full-file end-to-end re-read from disk this session (all 12 sections confirmed accurate; §9's roster was exercised live by this morning's own commits — `audit-health`, `backlog-id-on-close`, `backlog-filing-backpressure` and `validate-hermetization` each fired against them — and §4's enum count is the one defect the re-read surfaced); `last_reviewed` re-stamped 2026-08-07.
- v2.51 (2026-08-03) — ADR-85 amendment 2026-08-03 built. §9 gains `block-unanchored-push` (the ADR-85 HARD leg, pre-push, scoped to main) and records `block-ff-push`'s posture change to **fail-CLOSED** (it silently auto-allowed on any internal error until this arc). The `Stop` backpressure row now says **advisory in full** — it has no hard leg and cannot block a turn. DRIFT FOUND AND FIXED BY THIS RE-READ: §7 still described ADR-85 §4 `/override` as "the gate's only escape", which the amendment §A2 retired — corrected in place, since the sole escape is now `git push --no-verify` backed by the `journal_spine_anchor` FAIL backstop. L10 version 2.50→2.51. Genuine full-file end-to-end re-read from disk this session (all 12 sections confirmed accurate; §9's roster exercised live against the shipped hooks and the §7 staleness above is the one defect it surfaced); `last_reviewed` re-stamped 2026-08-03.
- v2.50 (2026-08-02) — §9 pre-commit roster gains `check-seal-identity` ([#475]): commit-time seal-identity gate over staged `docs/handoffs/**` bundles, reusing `gen_handoff.verify_seal_identity` (the [#473] seal-time refusal's commit-time twin). Roster addition only — no doctrine moved; ARCHITECTURE Ch2 gate list updated in lockstep. L10 version 2.49→2.50.
- v2.49 (2026-08-02) — §12 condensed to its authorized home (pre-authorized relocation; needs no new ADR, and none was written). The v2.18–v2.48 block had reached 19,017 bytes across 11 bullets — 44.6% of the file — re-read in full at every session boot. Both cited ADRs name the SAME destination and foreclose the alternative: ADR-49 — “The change record is git history (descriptive commits)”; ADR-65 §1 — “Technical record = git… **No archive file** (CLAUDE.md §5; ADR-47 ‘no ceremonial archive’)”. So the block was condensed to the git pointer §12 has used since v2.22, **not** moved into a new file — which would have violated the very ADRs authorizing the move. No content loss: nothing is deleted, every entry stays recoverable verbatim at `c30af862:CLAUDE.md` and via `git log --follow -p -- CLAUDE.md` (19,017 bytes out, byte-counted before and after). The `owner=repo` `section-history` region markers and the §12 heading are RETAINED — they are the boundary substrate `boundary_report.py` / `boundary_headers.py` key on by region `id`, not history. Also corrected the stale footer “Last updated” (2026-07-30, while v2.48 landed 07-31 — the v2.41 stale-footer precedent). L10 version 2.48→2.49. Genuine full-file end-to-end re-read from disk this session (all 12 sections confirmed accurate; §4/§5/§7/§9 claims exercised live through this morning's commits); `last_reviewed` re-stamped 2026-08-02.
<!-- methodology:end id=section-history -->

---

**Last updated:** 2026-08-07
**Maintained by:** Rob
