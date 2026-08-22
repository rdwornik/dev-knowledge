---
last_reviewed: 2026-08-22
reconciled_with: handoff-process@6.2.0
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.64 — 2026-08-22 -->

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
3. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
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

See `ARCHITECTURE.md` for the structural model; read it before structural changes (required for every repo, per ADR-51 as amended 2026-05-23). NOT a code project — markdown governance files plus hub-local validators, generators and gates; no script drives state in a child repo (§5 rule 4).

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
4. **Layer 2 never executes** — no orchestration scripts: no script drives state in a child repo (ADR-28, ADR-36). Hub-local validators, generators and gates are in scope.
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
3. Read the **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves; same predicate as §1 item 3, so the two boot instructions select the same bundle — if continuing prior session
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
- `organ-index-freshness` ([#132], HUB-ONLY) — regen-and-diff gate for the generated `ecosystem/organ-index.md` organ inventory (relocated there 2026-08-12 from `docs/ORGAN-INDEX.md` by operator ruling A of 2026-08-11, register `protocols/STANDING_RULINGS.md` K-1) (`generate_organ_index.py --check`), mirroring `audit-index-freshness` / `claude-rosters-freshness`; fires on every organ source the generator reads (`.claude/{agents,commands,skills,workflows,rules}`, the hook config, `ecosystem/organ-registry.yaml`). It guards the surface that replaces *operator-as-registry*, which is why a stale index is worse than none. Landed by batch-4 W5; this roster row was scoped to the INTEGRATOR by the execution plan's C-narrow decision (§4.3) so the lane stayed out of this collision file, and W5's packet named it as owed
- `validate-hermetization` (#306, HUB-ONLY) — ADR-101 tree-seal refusal gate, prospective-only on staged ADDs (existing files grandfathered): Rule A blocks a new unsanctioned Tier-1 top-level dir/file-class or `docs/<genre>/` folder; Rule B blocks an off-grammar/mis-cased/off-enum `docs/audits/*.md` name (ADR-101 R3/R4, name-shape only); **Rule C** blocks an added file whose home directory is outside the allowlist derived from the live taxonomy — message *"new path outside allowlisted homes — operator approval required"* (operator ruling A of 2026-08-11, register `protocols/STANDING_RULINGS.md` K-1; the leg that reads the rest of the path, since Rule A seals the top level and the `docs/<genre>/` level and stops there). Honest limit: Rule C polices the HOME of an added file, and the two open homes (`docs/handoffs/**`, `tests/fixtures/**`) admit arbitrary depth by design; `scripts/validate_hermetization.py`, bypass `--no-verify`
- `intake-index-freshness` (#307, HUB-ONLY) — regen-and-diff gate for the generated status-grouped Contents block in `docs/intake/README.md` vs `docs/intake/*.md` frontmatter `status:` (`gen_intake_index.py --check`; fires on any intake status-change/add/remove or the generator; never moves a file); guards against silent index rot
- `check-seal-identity` ([#475], HUB-ONLY) — bundle seal-identity gate at commit time: runs `gen_handoff.verify_seal_identity` (reused, not reimplemented) over the bundle dir of every staged `docs/handoffs/**` file, so a hand-renamed directory / edited Slug row / copied bundle whose internal slug names a DIFFERENT directory cannot become an immutable committed artifact (the [#473] seal-time refusal covered only the machine generation path). Fires only when such files are staged; exit 0 clean / 1 violation / 2 internal error (an error BLOCKS, never a silent pass); `scripts/check_seal_identity.py`, bypass `--no-verify`. Honest limit: catches the Slug row vs directory, not a stale P0c/P3/P8 locator inside a correctly-labelled bundle
- `block-commit-on-main` ([#527], HUB-ONLY) — the PREVENT half of core-invariant #5 at COMMIT time, the pre-commit sibling of `block-ff-push`: refuses a direct non-merge commit while `HEAD` is on `main`, so the branch → `--no-ff` merge discipline is enforced where the commit is made rather than only where it is pushed. A conflicted merge is carved out via `MERGE_HEAD` and a clean `--no-ff` merge never fires `pre-commit` at all, so a merge queue is unaffected either way. `scripts/block_commit_on_main.py`, bypass `--no-verify`. **Honest limit, and it is the module's own documented one:** `current_branch()` returns `None` on ANY non-zero `git symbolic-ref`, so a genuine git failure silently ALLOWS the commit — a stated hole copied from upstream `no_commit_to_branch`, and internally inconsistent with sibling `merge_in_progress()`, which RAISES on git failure by explicit design. Client-side hooks are bypassable regardless; `block-ff-push` stays the real teeth.
- `lane-contract-check` ([#539], HUB-ONLY) — shape gate for a **generator-emitted** lane contract (Q6): every mandatory section present, the dispatch line and the routing row agreeing on the tier, and the worktree⇄file pairing self-consistent with the `worktree-` prefix applied exactly once; `scripts/gen_lane_contract.py check`, bypass `--no-verify`. **Scope is a ruling, not a default** (architect, 2026-08-21): `files:` matches the generator's own emitted name shape `LANE-<slug>.md`, NOT the contract-of-record home — the eleven batch-1 contracts at `docs/audits/2026-08-21-*-lane-contract.md` predate the generator, fail this check 11-for-11, and are grandfathered as records of an already-executed batch (retro-fitting them would falsify what was actually dispatched). Honest limit, the generator's own: it checks SHAPE, never whether a contract's footprint claims are true.
- `provider-registry-agreement` (CLOUD-4 v2, HUB-ONLY) — agreement gate for the nine table-edit provider/model seams (R2 §3.2) against `ecosystem/provider-registry.yaml`: the `.md` frontmatter pin (S9), the `.js` object-literal pins (S10), the `.md` prose tier binding (S17), the JSON marketplace host path (S26), the durable tool-versions identity half (S8) and the two provenance attributions (S29/S30). `scripts/check_provider_registry.py`, exit 0/1/2 (an error BLOCKS), bypass `--no-verify`. **Honest limit, the module's own:** it asserts AGREEMENT, not correctness — frontmatter and a JS literal cannot read a YAML file, so the coupling is detection, and nothing here says the pinned model is the right one (routing is doctrine, and its canonical table `~/.claude/ROUTING.md` is **L0, outside this repo** — ruled 2026-08-22, `ARCHITECTURE.md` Ch3). **S10 asserts the pin COUNT, not only the values** — a *deleted* pin passed clean until 2026-08-22 (gpt-5.6-terra), which is the defect class the gate exists to refuse.
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

> _Entries v1.0–v2.58 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.64 (2026-08-22, cloud-wave close — ruling I5) — **§9's pre-commit roster gains `provider-registry-agreement`, and the file buys real headroom rather than shaving under the cap.** Roster addition only; no doctrine moved. Owed to the integrator by the `[#539]`/batch-4-W5 precedent that v2.60 and v2.63 both record — CLOUD-4 v2 shipped the gate as a fenced diff because its contract reserved `.pre-commit-config.yaml`, so the wiring and this row land at the merge, where the gate is live. **The row states the count leg because the obvious gate was measurably insufficient:** `check_s10` returned clean whenever the pins it *found* agreed, so deleting two of three Stage-1 `model:` pins passed while the artifact claimed it asserted "all three" — found by the pre-merge `gpt-5.6-terra` pass this window ran on the lane's behalf, fixed with a mutation-checked deletion test. The gate **arms green** (verified live via `pre-commit run --all-files`), the v2.63 state. **Budget, and the ruling is explicit about it:** the architect directed *file the roster line WITH consolidation — do not shave under the cap*, so rather than condensing the minimum, the v2.60/v2.61/v2.62 arc — three bullets that are one continuous story about §5 rule 4 and its §3 duplicate — is **merged into a single bullet**, which is the overlapping-entry merge the size-cap doctrine asks for rather than a chronological drop. Headroom restored to 4, not 0. No content lost: all three remain recoverable verbatim via `git log --follow -p -- CLAUDE.md`. L10 version 2.63→2.64. Genuine full-file end-to-end re-read from disk this session (all 12 sections; §9's roster was exercised live against this window's own spine — `organ-index-freshness` and `claude-rosters-freshness` both forced a regen before their commits, and `audit-health` gated every one, exactly as their rows say). **The defect the re-read surfaced is KNOWINGLY LEFT, with its owner named:** §10's first anti-pattern still reads *"Narrating or managing AGENTS.md — AGENTS.md is retired (ADR-53)"*, which ruling A2 of the same day made **false doctrine** — `AGENTS.md` is ADMITTED. It is not corrected here because `[#577]`'s Done-when explicitly owns that correction *"in the same commit"* as the file it describes; inverting it now would leave the anti-pattern pointing at a file that does not yet exist, and would widen a scoped act — the v2.55/v2.61 file-it-do-not-sweep-it precedent.

- v2.63 (2026-08-21, batch-1 integration — the owed roster row) — **§9's pre-commit roster gains `lane-contract-check`.** Roster addition only; no doctrine moved. Owed to the integrator by the same design v2.57 and v2.60 record: `[#539]` shipped the gate as a *fenced proposed diff* because its contract reserves `.pre-commit-config.yaml`, so the wiring — and this row — land at the merge, where the gate is actually live. **The row states a ruled scope because the obvious scope was tested and refused everything.** Wiring the hook at the contract-of-record home was tried first and REJECTED ALL ELEVEN live contracts, including `library-first-research-lane-contract.md`, the one contract in batch 1 that satisfied Q6 at dispatch unprompted; an emitted probe checks `rc=0`, so the generator is sound and the corpus is simply a different object. The architect ruled the same session: generator shape authoritative from batch 2 onward, the eleven never retro-fitted, hook scoped to `LANE-<slug>.md`. Zero tracked files match the glob, so the gate **arms clean rather than arming red** — the state `[#539]`'s own artifact warned about from the other side. `doc_claims` had been carrying the WARN naming the missing entry (`precommit_hook_roster@CLAUDE.md`, plus `precommit_hook_count` 19≠20); both clear with this edit and the `gen_doc_counts.py --write` regen. Ch8 carries the cutover line in the same commit as the hook. L10 version 2.62→2.63. Genuine full-file end-to-end re-read from disk this session (all 12 sections; §9's roster was exercised live against this batch's own spine — `organ-index-freshness` BLOCKED the hook commit until the new organ was registered, and `audit-health` gated every commit in the pass, exactly as their rows say); the stale `Last updated: 2026-08-16` footer is the one defect the re-read surfaced, corrected here. **Budget: the three oldest bullets (v2.56–v2.58) condensed into the git pointer** on the v2.59/v2.62 precedent — ADR-49 and ADR-65 §1 both name git as the destination — so the +1 roster row and this bullet land net-zero at 198/200, holding headroom at 2 rather than at the edge. No content lost: all three recoverable verbatim via `git log --follow -p -- CLAUDE.md`.

- v2.60–v2.62 (2026-08-15/16, phase-1 + phase-2 + batch-6 wrap — **one arc, merged at v2.64 per the size-cap doctrine's overlapping-entry rule**) — the §5 rule-4 correction and its second site, start to finish. v2.60 added §9's `block-commit-on-main` roster row (owed to the integrator by lane O, whose own terra finding is the row's stated honest limit: `current_branch()` fails OPEN on a git error while its sibling `merge_in_progress()` raises) and **knowingly left §5 rule 4 standing** though descriptively false — *"`scripts/` contains read-only validators only"* while ~23 scripts mutate state and `audit.py` pushes to `origin` — because the phase-1 architect ruled R3 that the drift is carried, not smoothed. v2.61 then re-scoped rule 4 onto §10's already-accurate wording as a standalone Position-0 act, and **its own re-read found §3 line 49 carrying the identical falsity**, filed rather than swept in because widening a scoped act is how it stops being checkable. v2.62 closed that second site in its own act with its own full re-read, taking fleet-wide drift on the claim to **0 sites**. The invariant never changed in substance: what Layer 2 may not do is drive a CHILD repo's state; hub-local validators, generators and gates were always in scope and now say so. Full text: `git log --follow -p -- CLAUDE.md`.

- v2.59 (2026-08-15, morning-adjudication boot-acts) — **the file is back inside its own ≤200-line budget, and the L10 version sentinel is corrected.** `doc_rot`'s `file-budget CLAUDE.md#size` had been firing at 203 counted lines against the self-declared 200 (ADR-53); ruled D1.3 of the 2026-08-15 morning adjudication as *"a trim, not a disposition"*. Executed on the v2.49 precedent — the oldest contiguous block (v2.49–v2.53) condensed into the git pointer above, not moved to an archive file, because ADR-49 and ADR-65 §1 both name git as the destination and ADR-65 forecloses an archive file. No content loss: every condensed entry stays recoverable verbatim via `git log --follow -p -- CLAUDE.md`. Condensing five bullets rather than the minimum four is deliberate — the minimum lands the file exactly ON 200, where the next single-line edit re-reds the gate. **DRIFT FOUND AND FIXED BY THIS RE-READ:** line 10 read `version: 2.57` while §12's newest entry was v2.58 and the footer read 2026-08-12 — v2.58's bullet claims *"L10 version 2.57→2.58"* but the sentinel was never actually bumped, so the prose recorded a bump that did not happen. Corrected here to 2.59 (skipping a cosmetic 2.58 restamp, since the entry documenting 2.58 is present and accurate about everything else). L10 version 2.57→2.59. Genuine full-file end-to-end re-read from disk this session (all 12 sections confirmed accurate; §9's roster was exercised live against this arc's own commits — `audit-health`, `ruff`, `validate-hermetization`, `audit-index-freshness`, `backlog-id-on-close` and `backlog-filing-backpressure` each fired, and both pre-push organs passed — and the stale L10 sentinel is the one defect the re-read surfaced); `last_reviewed` re-stamped 2026-08-15.

<!-- methodology:end id=section-history -->

---

**Last updated:** 2026-08-22
**Maintained by:** Rob
