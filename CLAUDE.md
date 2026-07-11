---
last_reviewed: 2026-07-11
reconciled_with: handoff-process@5.7
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.35 — 2026-07-11 -->

> **Session contract for Claude Code in this repo.** Read on every session start (auto). Single canonical agent-instruction file (≤200 lines). Per ADR-53.
>
> **For universal rules:** read `protocols/ESSENTIALS.md` and `protocols/PLAYBOOK.md`.

## 1. First read (session start)
<!-- scope: meta -->
<!-- methodology:start id=first-read owner=hub -->

In order, read:
1. This file (you're here)
2. `protocols/ESSENTIALS.md` — Rob's universal working style
3. `protocols/PLAYBOOK.md` — universal protocols (only sections relevant to current task)
4. Most recent `docs/handoffs/*/` bundle — start with its `HANDOFF_BOOT.md` (v5 bundles' operator session entry: slug · purpose · mode; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
5. Last 5 entries of `JOURNAL.md`

If ESSENTIALS or PLAYBOOK are unavailable, proceed with this file alone but flag it.
<!-- methodology:end id=first-read -->

## 2. Repo identity
<!-- scope: meta -->
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
<!-- methodology:start id=repo-architecture owner=repo -->

See `ARCHITECTURE.md` for the structural model; read it before structural changes (required for every repo, per ADR-51 as amended 2026-05-23). NOT a code project — markdown governance files + read-only validators only.

- **Chapter pointers** (`ARCHITECTURE.md` is a six-chapter map; jump to the topic — doctrine lives there + the cited ADRs, never resident here): cloud/nightly Routine + spec-orchestration + t-shirt model routing → **Ch3 Automation axes**, the nightly outcome loop → **Ch6 Verification mesh**; which organ fires when (hooks/skills/commands/agents/gates) → **Ch2 Organ map**; what's distributed where (carriers / child floor / browser bundle) → **Ch4 Distribution & transfer**.
<!-- methodology:end id=repo-architecture -->

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs (`VISION.md`, `CLAUDE.md`, etc.); `ADR-NN-topic.md` for decisions; `YYYY-MM-DD-slug.md` for dated artifacts; `council-out-YYYYMMDD_HHMMSS-topic.md` for Council CLI output; kebab-case otherwise
<!-- methodology:start id=conventions-commit-branch owner=hub -->
- **Commits:** Conventional Commits — `feat/fix/docs/chore/refactor`
- **Branches:** `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>` off `main`
<!-- methodology:end id=conventions-commit-branch -->
- **Testing:** `pytest -x --tb=short`
- **Linting:** `ruff check --fix` (manual / via `/save`); `ruff check` is also enforced as a pre-commit gate (see §9) — violations block commits
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal only; not enforced (ADR-27; enforcement withdrawn per ADR-48)
- **File lifecycle:** Append-only: `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file; an ADR *status line* is editable in place on ratification per §5 item 3 / ADR-94). Living: `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` (update in place).
- **Freshness cadence:** the living docs `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS` carry a `last_reviewed` frontmatter stamp meaning *re-read end-to-end and confirmed accurate (or drift filed)* — **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last edit (edited-but-not-re-reviewed) and warns past a 30-day backstop. Bump `last_reviewed` only after a genuine review. See PLAYBOOK "Canonical-file freshness cadence".

**Out of scope for this repo:**
- Code-level implementation → child repos (corp-monorepo, ai-council, etc.)
- Client/product/domain knowledge → Obsidian vault
- Project-specific CLAUDE.md content → each repo owns its own
- Claude Code runtime config → `~/.claude/`
- Council debate transcripts originate in `ai-council/`; they archive here in `docs/decisions/transcripts/`

<!-- methodology:start id=conventions-output-formatting owner=hub -->
- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables (`| col | col |`) as Unicode borders (`┌─┬─┐ │ └─┴─┘`) **client-side at render time**. So a bare table looks clean in the terminal but copies into browser chat as costly border glyphs (~3× the tokens), and a rule that merely bans Claude from *writing* box-drawing is a no-op (Claude already doesn't). The working fix is at the render layer: any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, which makes the TUI render it raw/un-painted so the copied text carries no borders. Same fenced-block discipline already used for Scale-S snippets (ESSENTIALS) and downloadable prompts (§2). Persistent diagrams live on the separate human-facing visualization surface (ADR-59; the ADR-51 amendment 2026-07-05 moved Mermaid out of canonical `ARCHITECTURE.md` — its codemap is now compact text), out of scope. Full rationale + `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat".
<!-- methodology:end id=conventions-output-formatting -->

## 5. Critical rules
<!-- scope: meta -->

<!-- methodology:start id=critical-rules-records owner=hub -->
1. **`LESSONS.md` and `logs/TOKEN-LOG.md` are append-only** — never edit old entries; only append (ADR-29, ADR-39)
2. **`JOURNAL.md` is append-only newest-first** — prepend at session wrap or workday close
3. **ADRs, transcripts, handoffs, and audits are immutable** — supersede with a new file or an in-file amendment marker; never edit in place. **ADR ratification exception (ADR-94):** an ADR's *status line* MAY be edited in place on ratification (e.g. Proposed → Accepted) — the status line is metadata, not decision content. This exception is ADR-specific and covers the status line only; ADR decision content, and transcripts / handoffs / audits in full, remain immutable.
<!-- methodology:end id=critical-rules-records -->
4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md` deleted 2026-05-23 (deprecated per ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo) — do not recreate it.
<!-- methodology:start id=critical-rules-consistency owner=hub -->
6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
<!-- methodology:end id=critical-rules-consistency -->
7. **No executable rules in this repo** — those go in `~/.claude/` with `verify:` lines
8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + JOURNAL `Changes:` line replace CHANGELOG
<!-- methodology:start id=critical-rules-no-leftovers owner=hub -->
9. **No leftovers** — any automated or scratch-creating process (parallel-session worktree, night-agent run per ADR-68, temp file) removes **and verifies removal of** everything it created before it counts as done; cleanup fires even on abort. The provision→cleanup round-trip must leave the tree identical. See PLAYBOOK §Session-boundaries "No leftovers" (the `.dev-knowledge-*` orphans are the failure it prevents)
<!-- methodology:end id=critical-rules-no-leftovers -->

## 6. Session start protocol
<!-- scope: runtime -->
<!-- methodology:start id=session-start-protocol owner=hub -->

1. `/boot` (archived 2026-06-05 Phase-C3, archive path: `~/.claude/archive/2026-06-05-machinery-c3/`; loads skills, memory, recent commits)
2. `git status` — clean working tree?
3. `git log --oneline -5` — recent context
4. Read most recent handoff if continuing prior session
5. Check `BACKLOG.md` for in-progress items
6. `pytest --collect-only` — test discovery sanity check
7. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ESSENTIALS ↔ PLAYBOOK alignment; ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.
<!-- methodology:end id=session-start-protocol -->

## 7. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`):
- `/session-summary` — generate token-efficient session summary + handoff
- `/boot` (archived 2026-06-05 Phase-C3, archive path: `~/.claude/archive/2026-06-05-machinery-c3/`) — load context (skills, memory, recent commits)
- `/evolve` (archived 2026-06-05 Phase-C3, archive path: `~/.claude/archive/2026-06-05-machinery-c3/`) — evolution audit: promote/prune/graduate learned rules (weekly / ~10 sessions)
- `/codex-review` — invoke Codex review on a staged **code** diff (code only)

<!-- methodology:start id=commands-repo-roster owner=repo -->
Repo-level (`./.claude/commands/` — machine-enumerated from command-file frontmatter, generated like §9's roster; regenerate: `python scripts/gen_claude_rosters.py --write`):

@.claude/generated/commands-repo.md
<!-- methodology:end id=commands-repo-roster -->

`/handoff` generates a handoff per `HANDOFF_PROCESS.md` v5 (ADR-82). Deployed methodology commands — `/review-closures`, `/ship`, `/override` — are enumerated in the generated roster (§9, `@`-imported); governance stays at canonical homes: ADR-70 Tier-1 + §8 / `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" ([#76] — the hub uses the plugin's, not a hub-local duplicate) for `/review-closures` + `/ship` (the `/ship` worktree-refusal is the seed-state `LESSONS.md` 2026-06-19 lesson); ADR-85 §4 (explicit + logged, no auto-bypass — the gate's only escape) for `/override`.

(When to invoke each + auto-vs-manual for hooks: PLAYBOOK §"Usage protocol: which command / hook, when".)

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls)

(The `verify` skill is **not** user-level — it was archived 2026-06-05 to `~/.claude/archive/2026-06-05-machinery-c3/skills/verify/`; the live copy is hub-local, listed under Repo-level below.)

(`boot`/`session-summary`/`handoff`/`save` are **commands**, not skills — see §7; current Claude Code also surfaces commands in its skill picker, but their files live under `commands/`, not `skills/`.)

<!-- methodology:start id=skills-repo-roster owner=repo -->
Repo-level (`./.claude/`):
- `.claude/skills/` holds `verify` (ecosystem verification scripts, run after `pytest`) + `check-against-spec` (spec-reconciliation site enumerator). Repo-specific empirical patterns also live in `LESSONS.md` (append-only) — read it before structural changes; universal gotchas are the user-level `gotchas` skill above. A repo-specific gotchas skill, if added, goes under `.claude/skills/gotchas/`.

Plugin:
- `tier1-lifecycle@dev-knowledge-methodology` is **enabled** (`.claude/settings.json`) and drives the Tier-1 closure loop here — its `Stop` hook runs `propose_closures.py` and it ships the `/review-closures` + `/ship` commands (§7/§9). The hub is the marketplace source the child repos install from; full distribution model in `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" + `plugins/tier1-lifecycle/INSTALL.md`.
<!-- methodology:end id=skills-repo-roster -->

## 9. Hooks active
<!-- scope: runtime -->
<!-- methodology:start id=hooks-repo-roster owner=repo -->

Pre-commit (`.pre-commit-config.yaml`):
- `normalize-dated-headers` — dated-log header normalization
- `codemap-freshness` — ARCHITECTURE compact-text codemap vs `scripts/` staleness check (format-agnostic regen-and-diff; the codemap is compact text since the ADR-51 amendment 2026-07-05, gate retained)
- `toc-freshness` — ARCHITECTURE.md TOC vs its own headers staleness check (ADR-71 source-repo pattern)
- `toc-freshness-playbook` — PLAYBOOK.md TOC staleness check (same `scripts/toc/` tool, PLAYBOOK target)
- `roster-freshness` — regen-and-diff gate for `.claude/methodology-roster.md` vs `deploy/manifest-v*.yaml` (`gen_methodology_roster.py --check`; blocks a hand-edited or manifest-stale roster); HUB-ONLY (n=1), [#244] P3
- `claude-rosters-freshness` — regen-and-diff gate for the two `@`-imported CLAUDE.md fragments `.claude/generated/{commands-repo,recent-adrs}.md` vs disk (`gen_claude_rosters.py --check`; fires on the command files / ADR headers / the fragments); HUB-ONLY, [#258] phase-2
- `audit-index-freshness` — regen-and-diff gate for the generated `docs/audits/README.md` index vs `docs/audits/*.md` (`gen_audit_index.py --check`; shape-agnostic — survives the #269 count-tiered reshape); guards against silent index rot (census A-2 ruling); HUB-ONLY
- `validate-hermetization` (#306, HUB-ONLY) — ADR-101 tree-seal refusal gate, prospective-only on staged ADDs (existing files grandfathered): Rule A blocks a new unsanctioned Tier-1 top-level dir/file-class or `docs/<genre>/` folder; Rule B blocks an off-grammar/mis-cased/off-enum `docs/audits/*.md` name (ADR-101 R3/R4, name-shape only); `scripts/validate_hermetization.py`, bypass `--no-verify`
- `intake-index-freshness` (#307, HUB-ONLY) — regen-and-diff gate for the generated status-grouped Contents block in `docs/intake/README.md` vs `docs/intake/*.md` frontmatter `status:` (`gen_intake_index.py --check`; fires on any intake status-change/add/remove or the generator; never moves a file); guards against silent index rot
- `validate-backlog` — BACKLOG.md story-map schema (ADR-66)
- `audit-health` — self-conformance gate: `audit.py health` (FAIL blocks the commit, WARN informs); added by [#69]
- `ruff` — lint gate: `ruff check` (gate mode; blocks on violations); version-pinned >=0.15.5 via `pyproject.toml`; `language: system` (no mismatch); added by [#13]
- `coherence-nudge` — **non-blocking** forgotten-version-bump nudge: a registered spec (`_SPEC_REGISTRY`) changed-without-a-version-bump prints a stdout nudge + logs `logs/coherence-nudge.log`; always exits 0 (a nudge, not a gate); pairs with the `reconciled_versions` audit check
- `backlog-id-on-close` (commit-msg) — require `[#id]` when a commit removes a backlog task
- `backlog-filing-backpressure` (commit-msg) — the add-side sibling of `backlog-id-on-close` (filing-backpressure doctrine, 2026-07-08 ruling; PLAYBOOK §10): a commit that ADDS a new BACKLOG task id must carry a `kill-candidates:` line (≥1 existing `#id`, or `none — <reason>`) — BLOCK if absent; also emits the advisory ADR-98 intake-id WARN on a new L-sized new-feature epic (#279). `scripts/check_backlog_filing.py`; HUB-ONLY; proposals only (never auto-removes); fail-open-loud on git error.
- `block-ff-push` (pre-push) — the PREVENT half of core-invariant #5 ([#153]): refuses a push that would put a non-merge commit on main's first-parent spine (a direct-to-main commit or a true FF merge); a `--no-ff` merge passes. `scripts/block_ff_push.py`, HUB-ONLY, fail-soft to exit 0 on any git error, bypass `git push --no-verify` (the `no_ff_merges` audit WARN stays the post-hoc backstop). Delegates the scan to `validate_no_ff.find_violations` (one shared FF-signature). **One-time local activation: `pre-commit install --hook-type pre-push`** (the config's `default_install_hook_types` only wires it on a fresh install). `validate_no_ff` stays the detect-and-surface WARN; this is the distinct prevent organ (separate file, so validate_no_ff's never-gates contract is preserved).

Session hooks (`.claude/settings.json`, project-level — merges with, does not replace, the `~/.claude` hooks): `SessionStart` surfacing (`fleet_health.py` Tier-2 fleet digest [#72] + `surface_triage.ps1` nightly-triage + `billing_leak_sentinel.ps1` [#101] + `changelog_sentinel.py` [#113]), a `Stop` backpressure hook (`session_end_backpressure.py`), and the ADR-77 `PreToolUse` transcript-immutability guard (`block_immutable_edits.py`) — each fail-soft (surfacing) or fail-closed (the guard) per its row. **Full live organ inventory (trigger × layer × failure posture) → `ARCHITECTURE.md` Ch2 Organ map.** The Tier-1 closure loop runs via the enabled `tier1-lifecycle` plugin (`Stop → propose_closures.py`; detect-and-propose, never mutates BACKLOG) + the global `~/.claude` `surface-closures.ps1` L0 surfacing — not hub-local `settings.json` (the 5c convergence; ARCHITECTURE "Tier-1 self-enforcing lifecycle").

Rules (`.claude/rules/`):
- `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end

### Methodology-deployed roster (generated — do not hand-edit)

The deployed methodology corpus (the commands / hooks / config the deploy tool ships to a consumer) is machine-generated from `deploy/manifest-v*.yaml` `components:[].roster` and `@`-imported below — regenerated-from-source, not review-stamped (deliberately OUT of the freshness gate; regenerate: `python scripts/gen_methodology_roster.py --write`). §7–§9 stay hand-authored for the hub-LOCAL surface (items with no manifest entry). Drift-gated by the `roster-freshness` pre-commit hook.

@.claude/methodology-roster.md
<!-- methodology:end id=hooks-repo-roster -->

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->
<!-- methodology:start id=antipatterns-universal owner=hub -->

- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Narrating or managing AGENTS.md** — AGENTS.md is retired (ADR-53); CLAUDE.md is the single instruction file
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
<!-- methodology:end id=antipatterns-universal -->

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->
<!-- methodology:start id=recent-adrs-roster owner=repo -->

Machine-enumerated (last 5 by number, from `docs/decisions/ADR-*.md` headers; regenerate: `python scripts/gen_claude_rosters.py --write`). Editorial one-liners live in `docs/decisions/README.md`; full governance list in `ARCHITECTURE.md`.

@.claude/generated/recent-adrs.md
<!-- methodology:end id=recent-adrs-roster -->

## 12. Section history
<!-- scope: meta -->
<!-- methodology:start id=section-history owner=repo -->

> _Entries v1.0–v2.17 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.18–v2.26 (2026-06-12 → 2026-07-03, condensed 2026-07-05/2026-07-11 per ADR-49/65, operator-granted — full entries: `git log --follow -p -- CLAUDE.md`): §1 first-read #4 repointed to the bundle's `HANDOFF_BOOT.md` + the canonical operator runbook (v2.18); ESSENTIALS joined the freshness gate / `_FRESHNESS_FILES` (v2.19); §9 gained the `block-ff-push` pre-push prevent organ, core-invariant #5 (v2.20); §11 rotated 76–80→85–89 + §7 reconciled to the live command set incl. `/changelog-review`/`/override`/`/ship` (v2.21); §12 v1.0–v2.17 condensed to the git pointer, clearing doc_rot + file-budget WARNs (v2.22); ADR-88/89 ratified Proposed→Accepted + §8 repo-skills refresh (v2.23); §8 user-level-verify self-contradiction fixed — live `verify` is hub-local (v2.24); §11 rotated 85–89→89–93 + the stale version comment fixed (v2.25); the ADR-94 ADR-status-line ratification exception landed — §5 item 3 narrowed, §11 rotated 89–93→91–95 (v2.26). Each landed with its genuine re-read + `last_reviewed` re-stamp.
- v2.27 (2026-07-04) — [#244] P3 generated-roster currency (Fable R3): the deployed methodology corpus (commands / hooks / config) is now machine-generated from `deploy/manifest-v*.yaml` `components:[].roster` into `.claude/methodology-roster.md`, `@`-imported via a new §9 "Methodology-deployed roster (generated)" subsection — so it can no longer be hand-maintained and thus cannot rot. §7 trimmed of the three deployed commands (`/review-closures`/`/ship`/`/override`), replaced by a pointer note that keeps every non-enumeration rationale at its verified canonical home (ADR-70 + §8/ARCHITECTURE [#76]; the `/ship` worktree-refusal `LESSONS.md` 2026-06-19; ADR-85 §4). §9 gains the blocking `roster-freshness` regen-and-diff hook. The generated file is deliberately OUT of `DEFAULT_FRESHNESS_FILES` (currency = regen); CLAUDE.md STAYS in (100% hand-prose, gated). `@import` sanctioned: the ADR-45 / 2026-05-26-council `@path` ban is browser-handoff-delivery-scoped, NOT local session-boot (quoted at review; the live `@.claude/CLAUDE-FLOOR.md` precedent corroborates). Methodology version HELD (hub-only n=1 tooling; consumer rollout is P6). Hub-local items stay hand-authored (no machine source; follow-up filed). Genuine end-to-end re-read confirmed §1–§11 current; `last_reviewed` re-stamped 2026-07-04.
- v2.28 (2026-07-05) — handoff-process 5.3→5.4 reconciliation (overnight-run Block D): frontmatter `reconciled_with` re-stamped @5.4 after site-enumeration (the §1/§7 handoff references are major-level and unaffected — the v5.4 change is additive-only: §5 structural anti-bluff + §13 generator note, documenting the `9d5ebe5` mechanism). Genuine end-to-end review basis: full-file read at session boot + §7/§8/§9 claims exercised live through the night's work; `last_reviewed` re-stamped 2026-07-05.
- v2.29 (2026-07-05) — handoff-process 5.4→5.5 reconciliation completed at Wave-1 root integration: the frontmatter `reconciled_with` @5.5 re-stamp itself landed IN-GRANT on the Epic 2 branch (`489c51f`, the 5-edge atomic move — its compressed check-against-spec sweep verdicted all 49 CLAUDE.md sites: only L3 stale; §1/§7 v5 refs major-level fine, §12 historical entries fine); this §12 entry is the recorded ARCHITECT-REVIEW-PENDING content edit **beyond that grant**, applied by root at integration per ADR-97 (v2.28-precedent style). Companion §11 "last 5" rotated **91–95 → 93–97** after genuine reads of ADR-96 (deploy remove leg) + ADR-97 (tree orchestration — the v5.5 decision record); dropped 91/92 (retained in `docs/decisions/README.md` + ARCHITECTURE Governing-ADRs). Genuine end-to-end re-read basis: full-file read at root-lane boot + §5/§7/§9 claims exercised live through the three Wave-1 merges (JOURNAL prepend-resolution, /override gate, pre-commit roster); `last_reviewed` 2026-07-05 stands (same-day arc rule).
- v2.30 (2026-07-05) — [#258] S3 generability phase 1 (Epic-3 lane, seam grant): the two hand-synced lists become generated-not-authored via the [#244] `@`-import seam — §7's repo-level command list (from `.claude/commands/*.md` frontmatter → `.claude/generated/commands-repo.md`) and §11's last-5 ADR list (from `docs/decisions/ADR-*.md` headers → `.claude/generated/recent-adrs.md`), both rendered by the new disk-truth generator `scripts/gen_claude_rosters.py` (kept separate from the manifest-driven roster generator — different sources of truth). §11's curated one-liners retire from this surface (the mechanical list replaces them; editorial depth stays in `docs/decisions/README.md` + the ADRs — ends the hand-rotation toil of v2.21/v2.25/v2.26/v2.29). §9's pre-commit list is deliberately NOT generated (the `doc_claims` check window-anchors it in this file's raw text; retiring that leg needs its own arc per the Tier-3 draft) and §8 skills stay hand-prose. Regen-and-diff pre-commit hooks for the new fragments are proposed in the EPIC RETURN (out of lane boundary). Fragments OUT of `DEFAULT_FRESHNESS_FILES`; CLAUDE.md stays in. Genuine same-day arc basis: full-file read at lane boot; `last_reviewed` 2026-07-05 stands.
- v2.31 (2026-07-06) — handoff-process 5.5→5.6 reconciliation (overnight-mission Block 0b, architect-approved CH-1): frontmatter `reconciled_with` re-stamped @5.6 after the check-against-spec sweep (41 sites enumerated; only the frontmatter stamp stale — the v5.6 change is additive §14a-only: the mandatory execution-MODE item, the plan-mode corrective). Also fixed the stale L10 version comment (**2.27** while v2.30 had landed → **2.31**, the v2.25-precedent defect class). Genuine end-to-end review basis: full-file read at mission boot (system-context copy verified against disk); `last_reviewed` re-stamped 2026-07-06.
- v2.32 (2026-07-07) — handoff-process 5.6→5.7 reconciliation (Arc-2 intake-scene build, #268 / ADR-98): frontmatter `reconciled_with` re-stamped @5.7 after the check-against-spec sweep (44 sites enumerated; only the frontmatter stamp stale — the v5.7 change is additive: new §16 functional mode + one §14 developer-alias sentence; the §1/§7 handoff refs are major-level and unaffected, §12 history entries immutable). L10 version comment bumped in the same edit (the v2.25 defect class). Genuine end-to-end review basis: system-context copy verified against disk at session boot + §4/§5/§7/§9 claims exercised live through the Arc-2 build (intake/ creation, gen_handoff modes, the atomic reconciliation commit); `last_reviewed` re-stamped 2026-07-07.
- v2.33 (2026-07-07) — §9 pre-commit roster reconciliation (architect-handoff wrap `2026-07-08-dev-knowledge-architect`, clearing the standing `doc_claims` drift to ship-gate GREEN): added the **`audit-index-freshness`** hook line — the census-triage arc (2026-07-07) wired the hook (census A-2 silent-rot ruling) but left the §9 roster + `ecosystem/doc-counts.md` un-reconciled (the drift the outgoing architect flagged "small, #269-adjacent" — SUPPLEMENT Q4.7). `doc-counts.md` regenerated the same arc (12→13 gates, 1396→1397 tests). L10 version comment 2.32→2.33 (the v2.25 defect class). Additive §9-only edit; genuine basis: full-file system-context read verified against disk at session boot + the §9 roster ↔ `.pre-commit-config.yaml` set-match (what `doc_claims` gates) exercised live; `last_reviewed` 2026-07-07 stands (same-day arc).
- v2.34 (2026-07-07) — §9 pre-commit roster reconciliation (cadence-teeth arc, filing-backpressure ruling 2026-07-08): added the **`backlog-filing-backpressure`** hook line — a new commit-msg gate (`scripts/check_backlog_filing.py`, add-side sibling of `backlog-id-on-close`) requiring a `kill-candidates:` line when a commit ADDS a new BACKLOG task id (proposals only, never auto-removes; PLAYBOOK §10 doctrine paragraph landed the same arc), and emitting the advisory ADR-98 intake-id WARN on new L-epics (#279). `doc-counts.md` regenerated (13→14 gates, 1403→1422 tests — the two new test files). L10 version comment 2.33→2.34 (the v2.25 defect class). Additive §9-only edit; genuine basis: frontmatter + §9 + §12 read against disk on the main-based branch (identical to session-boot copy) + the §9 roster ↔ `.pre-commit-config.yaml` set-match exercised live at ship-gate; `last_reviewed` 2026-07-07 stands (same-day arc).
- v2.35 (2026-07-11) — #312-child Form-A boundary grandfathering (LANE-D): the operator-ruled fleet methodology-boundary markers (design `docs/audits/2026-07-11-technical-fleet-boundary-marker-design.md`, Form A + floor) wrap this hub `CLAUDE.md` as `<!-- methodology:start/end id=… owner=hub|repo -->` fenced regions — the canonical diff **baseline** the read-only fleet boundary-reporter (`scripts/boundary_report.py`, built this arc) aligns consumers against by region `id`. Owner set (design §6 pt 2): `owner=hub` = §1/§6, the universal subset of §5 (records 1–3, consistency 6, no-leftovers 9), §10, + §4 sub-spans (commits+branches, output-formatting); `owner=repo` = §2/§3/§12 + the §7/§8/§9/§11 roster spans. **§1–§11 body prose byte-identical** — markers are additive render-invisible HTML comments; the sanctioned non-marker diff is this entry (+ the v2.25/v2.26 fold), the L10 version bump, and the `last_reviewed` re-stamp. Hub asymmetry: hub carries `owner=hub` regions but no floor `@import`. The markers pushed the file past the ADR-53 200-line budget, resolved by excluding comment-only lines from the doc-rot count (prose-rot backpressure preserved; operator-ruled, LESSONS 2026-07-10). Genuine end-to-end re-read to place every region; `last_reviewed` re-stamped 2026-07-11.
<!-- methodology:end id=section-history -->

---

**Last updated:** 2026-07-07
**Maintained by:** Rob
