---
last_reviewed: 2026-06-25
reconciled_with: handoff-process@5.3
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.23 — 2026-06-23 -->

> **Session contract for Claude Code in this repo.** Read on every session start (auto). Single canonical agent-instruction file (≤200 lines). Per ADR-53.
>
> **For universal rules:** read `protocols/ESSENTIALS.md` and `protocols/PLAYBOOK.md`.

## 1. First read (session start)
<!-- scope: meta -->

In order, read:
1. This file (you're here)
2. `protocols/ESSENTIALS.md` — Rob's universal working style
3. `protocols/PLAYBOOK.md` — universal protocols (only sections relevant to current task)
4. Most recent `docs/handoffs/*/` bundle — start with its `HANDOFF_BOOT.md` (v5 bundles' operator session entry: slug · purpose · mode; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
5. Last 5 entries of `JOURNAL.md`

If ESSENTIALS or PLAYBOOK are unavailable, proceed with this file alone but flag it.

## 2. Repo identity
<!-- scope: meta -->

- **Name:** `.dev-knowledge`
- **Complexity:** medium (informal; repo-tier system deprecated 2026-05-23 — no declared tier)
- **Status:** active
- **Purpose:** Universal LLM-driven development guide and methodology framework; governs all projects under `Dev/`; Layer 2 of the ADR-28 three-layer ecosystem model
- **Owner:** Rob
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`, `ARCHITECTURE.md`
- **Related locations:** `~/.claude/` (Claude Code runtime config); `.claude/` (project-level config); `ObsidianVault/` (pre-sales, do not mix); `Dev/` (child repos, each has own `CLAUDE.md`)

## 3. Architecture
<!-- scope: meta -->

See `ARCHITECTURE.md` for the structural model; read it before structural changes (required for every repo, per ADR-51 as amended 2026-05-23). NOT a code project — markdown governance files + read-only validators only.

- **Chapter pointers** (`ARCHITECTURE.md` is a six-chapter map; jump to the topic — doctrine lives there + the cited ADRs, never resident here): cloud/nightly Routine + spec-orchestration + t-shirt model routing → **Ch3 Automation axes**, the nightly outcome loop → **Ch6 Verification mesh**; which organ fires when (hooks/skills/commands/agents/gates) → **Ch2 Organ map**; what's distributed where (carriers / child floor / browser bundle) → **Ch4 Distribution & transfer**.

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs (`VISION.md`, `CLAUDE.md`, etc.); `ADR-NN-topic.md` for decisions; `YYYY-MM-DD-slug.md` for dated artifacts; `council-out-YYYYMMDD_HHMMSS-topic.md` for Council CLI output; kebab-case otherwise
- **Commits:** Conventional Commits — `feat/fix/docs/chore/refactor`
- **Branches:** `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>` off `main`
- **Testing:** `pytest -x --tb=short`
- **Linting:** `ruff check --fix` (manual / via `/save`); `ruff check` is also enforced as a pre-commit gate (see §9) — violations block commits
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal only; not enforced (ADR-27; enforcement withdrawn per ADR-48)
- **File lifecycle:** Append-only: `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file). Living: `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` (update in place).
- **Freshness cadence:** the living docs `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/ESSENTIALS` carry a `last_reviewed` frontmatter stamp meaning *re-read end-to-end and confirmed accurate (or drift filed)* — **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last edit (edited-but-not-re-reviewed) and warns past a 30-day backstop. Bump `last_reviewed` only after a genuine review. See PLAYBOOK "Canonical-file freshness cadence".

**Out of scope for this repo:**
- Code-level implementation → child repos (corp-monorepo, ai-council, etc.)
- Client/product/domain knowledge → Obsidian vault
- Project-specific CLAUDE.md content → each repo owns its own
- Claude Code runtime config → `~/.claude/`
- Council debate transcripts originate in `ai-council/`; they archive here in `docs/decisions/transcripts/`

- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables (`| col | col |`) as Unicode borders (`┌─┬─┐ │ └─┴─┘`) **client-side at render time**. So a bare table looks clean in the terminal but copies into browser chat as costly border glyphs (~3× the tokens), and a rule that merely bans Claude from *writing* box-drawing is a no-op (Claude already doesn't). The working fix is at the render layer: any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, which makes the TUI render it raw/un-painted so the copied text carries no borders. Same fenced-block discipline already used for Scale-S snippets (ESSENTIALS) and downloadable prompts (§2). Persistent diagrams in `ARCHITECTURE.md` are mermaid (ADR-51/ADR-59), out of scope. Full rationale + `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat".

## 5. Critical rules
<!-- scope: meta -->

1. **`LESSONS.md` and `logs/TOKEN-LOG.md` are append-only** — never edit old entries; only append (ADR-29, ADR-39)
2. **`JOURNAL.md` is append-only newest-first** — prepend at session wrap or workday close
3. **ADRs, transcripts, handoffs, audits are immutable** — supersede with a new file or in-file marker; never edit in place
4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md` deleted 2026-05-23 (deprecated per ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo) — do not recreate it.
6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
7. **No executable rules in this repo** — those go in `~/.claude/` with `verify:` lines
8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + JOURNAL `Changes:` line replace CHANGELOG
9. **No leftovers** — any automated or scratch-creating process (parallel-session worktree, night-agent run per ADR-68, temp file) removes **and verifies removal of** everything it created before it counts as done; cleanup fires even on abort. The provision→cleanup round-trip must leave the tree identical. See PLAYBOOK §Session-boundaries "No leftovers" (the `.dev-knowledge-*` orphans are the failure it prevents)

## 6. Session start protocol
<!-- scope: runtime -->

1. `/boot` (archived 2026-06-05 Phase-C3, archive path: `~/.claude/archive/2026-06-05-machinery-c3/`; loads skills, memory, recent commits)
2. `git status` — clean working tree?
3. `git log --oneline -5` — recent context
4. Read most recent handoff if continuing prior session
5. Check `BACKLOG.md` for in-progress items
6. `pytest --collect-only` — test discovery sanity check
7. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ESSENTIALS ↔ PLAYBOOK alignment; ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.

## 7. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`):
- `/session-summary` — generate token-efficient session summary + handoff
- `/boot` (archived 2026-06-05 Phase-C3, archive path: `~/.claude/archive/2026-06-05-machinery-c3/`) — load context (skills, memory, recent commits)
- `/evolve` (archived 2026-06-05 Phase-C3, archive path: `~/.claude/archive/2026-06-05-machinery-c3/`) — evolution audit: promote/prune/graduate learned rules (weekly / ~10 sessions)
- `/codex-review` — invoke Codex review on a staged **code** diff (code only)

Repo-level (`./.claude/commands/`):
- `/save` — commit workflow with full body per git-discipline rule
- `/handoff` — generate/complete handoff per `HANDOFF_PROCESS.md` v5 (ADR-82)
- `/changelog-review` — operator-invoked review of tool changelogs (claude-code + codex) since last review; classify per the audit rubric, write a digest, bump the state file (PUSH-triggered; never implements adoptions)
- `/override` — bypass the ADR-85 session-end hard gate for this HEAD; explicit + logged, no auto-bypass (the gate's only escape — ADR-85 §4)

Plugin-provided (`tier1-lifecycle@dev-knowledge-methodology`, §8):
- `/review-closures` — review the session-end closure proposals + execute ONLY operator-approved closures (ADR-70 Tier-1; human-gated, done-items-leave). Fleet-wide via the plugin; the hub-local duplicate command was dropped so the hub uses the plugin's like the child repos ([#76]).
- `/ship` — merge the current feature branch to `main` via `--no-ff`, push, and auto-delete the merged branch (git-finish); **refuses inside a worktree** — integrate from the primary checkout (seed-state-yaml lesson).

(When to invoke each + auto-vs-manual for hooks: PLAYBOOK §"Usage protocol: which command / hook, when".)

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls)

(The `verify` skill is **not** user-level — it was archived 2026-06-05 to `~/.claude/archive/2026-06-05-machinery-c3/skills/verify/`; the live copy is hub-local, listed under Repo-level below.)

(`boot`/`session-summary`/`handoff`/`save` are **commands**, not skills — see §7; current Claude Code also surfaces commands in its skill picker, but their files live under `commands/`, not `skills/`.)

Repo-level (`./.claude/`):
- `.claude/skills/` holds `verify` (ecosystem verification scripts, run after `pytest`) + `check-against-spec` (spec-reconciliation site enumerator). Repo-specific empirical patterns also live in `LESSONS.md` (append-only) — read it before structural changes; universal gotchas are the user-level `gotchas` skill above. A repo-specific gotchas skill, if added, goes under `.claude/skills/gotchas/`.

Plugin:
- `tier1-lifecycle@dev-knowledge-methodology` is **enabled** (`.claude/settings.json`) and drives the Tier-1 closure loop here — its `Stop` hook runs `propose_closures.py` and it ships the `/review-closures` + `/ship` commands (§7/§9). The hub is the marketplace source the child repos install from; full distribution model in `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" + `plugins/tier1-lifecycle/INSTALL.md`.

## 9. Hooks active
<!-- scope: runtime -->

Pre-commit (`.pre-commit-config.yaml`):
- `normalize-dated-headers` — dated-log header normalization
- `codemap-freshness` — ARCHITECTURE codemap vs `scripts/` staleness check
- `toc-freshness` — ARCHITECTURE.md TOC vs its own headers staleness check (ADR-71 source-repo pattern)
- `toc-freshness-playbook` — PLAYBOOK.md TOC staleness check (same `scripts/toc/` tool, PLAYBOOK target)
- `validate-backlog` — BACKLOG.md story-map schema (ADR-66)
- `audit-health` — self-conformance gate: `audit.py health` (FAIL blocks the commit, WARN informs); added by [#69]
- `ruff` — lint gate: `ruff check` (gate mode; blocks on violations); version-pinned >=0.15.5 via `pyproject.toml`; `language: system` (no mismatch); added by [#13]
- `coherence-nudge` — **non-blocking** forgotten-version-bump nudge: a registered spec (`_SPEC_REGISTRY`) changed-without-a-version-bump prints a stdout nudge + logs `logs/coherence-nudge.log`; always exits 0 (a nudge, not a gate); pairs with the `reconciled_versions` audit check
- `backlog-id-on-close` (commit-msg) — require `[#id]` when a commit removes a backlog task
- `block-ff-push` (pre-push) — the PREVENT half of core-invariant #5 ([#153]): refuses a push that would put a non-merge commit on main's first-parent spine (a direct-to-main commit or a true FF merge); a `--no-ff` merge passes. `scripts/block_ff_push.py`, HUB-ONLY, fail-soft to exit 0 on any git error, bypass `git push --no-verify` (the `no_ff_merges` audit WARN stays the post-hoc backstop). Delegates the scan to `validate_no_ff.find_violations` (one shared FF-signature). **One-time local activation: `pre-commit install --hook-type pre-push`** (the config's `default_install_hook_types` only wires it on a fresh install). `validate_no_ff` stays the detect-and-surface WARN; this is the distinct prevent organ (separate file, so validate_no_ff's never-gates contract is preserved).

Session hooks (`.claude/settings.json`, project-level — merges with, does not replace, the `~/.claude` hooks): `SessionStart` surfacing (`fleet_health.py` Tier-2 fleet digest [#72] + `surface_triage.ps1` nightly-triage + `billing_leak_sentinel.ps1` [#101] + `changelog_sentinel.py` [#113]), a `Stop` backpressure hook (`session_end_backpressure.py`), and the ADR-77 `PreToolUse` transcript-immutability guard (`block_immutable_edits.py`) — each fail-soft (surfacing) or fail-closed (the guard) per its row. **Full live organ inventory (trigger × layer × failure posture) → `ARCHITECTURE.md` Ch2 Organ map.** The Tier-1 closure loop runs via the enabled `tier1-lifecycle` plugin (`Stop → propose_closures.py`; detect-and-propose, never mutates BACKLOG) + the global `~/.claude` `surface-closures.ps1` L0 surfacing — not hub-local `settings.json` (the 5c convergence; ARCHITECTURE "Tier-1 self-enforcing lifecycle").

Rules (`.claude/rules/`):
- `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->

- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Narrating or managing AGENTS.md** — AGENTS.md is retired (ADR-53); CLAUDE.md is the single instruction file
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->

Brief one-liners. Full list in `docs/decisions/README.md`; full governance list in `ARCHITECTURE.md`.

- ADR-85: Session-lifecycle enforcement — deterministic session-end Stop-gate (4-model Council): hard block on the un-gameable JOURNAL commit-SHA anchor, advisory nudge on the BACKLOG leg (promoted when the traceability-spine lands, R1); demotes ARCHITECTURE/VISION/LESSONS/CONTRIBUTING to "update when materially affected"; escape only via logged HEAD-bound `/override`; single-source `protocols/DEFINITION_OF_DONE.md` (amended 2026-06-19: per-session SHA anchor — push→session boundary fix)
- ADR-86: Conformance-dashboard location — `ecosystem/conformance.md` as an ADR-80 committed-generated zone (a read-only validator generates + commits its own output, Layer-2-safe); the surface ADR-85 R2's ungated-doc staleness signal lands in; the ARCHITECTURE Ch2 pointer lands with the build (#171), not before
- ADR-87: Architect↔CC equilibrium contract — conditional intent-only prompting: CC self-loads reliably only for code-impact tasks, so the architect emits intent · closure · anti-patterns · plan/auto mode · a thin per-task governance-pointer (GAP-3) and CC owns code-impact context · generic gotchas · the skeleton (now its consumption-spec) · model/effort; GAP-2 backstop filed-not-built (#185), empirical close #184
- ADR-88: File-oriented dependency management (markdown as a design pattern) — repo files are the dependency unit; coherence across declared edges (`reconciled_with`/`serialize-group`/`depends-on`) held by machinery, not memory; five principles incl. narrow-first + do-not-build-is-doctrine; v1 proof = the #172 coherence spine, extends via the `coherence` group #179–#182
- ADR-89: Computed code-dependency edges (the computed-edge sibling to ADR-88) — "declare what you cannot compute; compute what you can": code→code computed via a Pyright reverse-dependency oracle (a custom code graph rejected for this repo), the benchmark's three limits (repo-scoped / static-Python-only / call-hierarchy warm-up) bound as normative + provenance required on every answer; doctrine only, no tooling wired (Track A)

## 12. Section history
<!-- scope: meta -->

> _Entries v1.0–v2.17 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.18 (2026-06-12) — §1 "First read" #4 repointed again (the v2.17 fix pointed at the bundle's `README.md`, which the new bundle shape no longer carries): v5 bundles drop the per-bundle README, so the pointer now reads the bundle's `HANDOFF_BOOT.md` (operator session entry) then the new **canonical operator runbook** `docs/handoffs/README.md`. Part of the canonical-runbook collapse (HANDOFF_PROCESS §13; #164): the stable operator boilerplate moved to one per-repo runbook, now itself freshness-gated (`audit.py` check #10). Genuine end-to-end re-read confirmed the rest current; `last_reviewed` re-stamped 2026-06-12.
- v2.19 (2026-06-19) — ESSENTIALS brought under the freshness gate (doc-currency seal): §4 freshness-cadence list `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING` → `…/ESSENTIALS` (ESSENTIALS gains `last_reviewed` frontmatter + joins `audit.py` `_FRESHNESS_FILES`, so its drift is now check-#10-detectable; PLAYBOOK §"freshness cadence" mirrored). Companion genuine end-to-end re-read confirmed the rest current; deferred to a separate focused groom (drift filed here, not pulled into this ripple): §11 "last 5" rotation toward ADR-84–88 (still lists 76–80; v2.17 deferral precedent) and a §7 `/override` command entry (the ADR-85 gate's escape hatch). `last_reviewed` re-stamped 2026-06-19.
- v2.20 (2026-06-20) — pre-push prevent organ landed (#153 advance): §9 pre-commit list gains the `block-ff-push` (pre-push) hook — the PREVENT half of core-invariant #5 (`scripts/block_ff_push.py`; companion ARCHITECTURE §Validators bullet + `pre-commit gates` count 9→10 + collected 739→760), keeping `validate_no_ff` as the detect-and-surface WARN. Required doc-sync (the new hook tripped `doc_claims`: hook-count, CLAUDE §9 roster, pytest-collected — all now reconciled so ship-gate is GREEN). Targeted same-day edit; the §11 "last 5" rotation toward ADR-84–88 stays deferred (v2.17/v2.19 precedent); `last_reviewed` re-stamped 2026-06-20. Scope-boundary + methodology-reach (#153 done-when) remain open.
- v2.21 (2026-06-21) — overnight ops/task audit, auto-apply lane (the deferral carried since v2.19/v2.20): §11 "last 5" rotated 76–80 → **85–89** after a genuine read of ADR-85–89 (two are **Proposed** — ADR-88/89 — annotated as such); §7 reconciled to the live command set — added repo-level `/changelog-review` + `/override` (the deferred ADR-85-escape entry) and plugin `/ship`, with the §8 plugin-command mention synced; fixed the stale version comment (was **2.19** while a v2.20 entry had already landed → **2.21**). Genuine end-to-end re-read confirmed the rest current; `last_reviewed` re-stamped 2026-06-21. **Surfaced to `docs/audits/2026-06-21-audit-ops-findings.md`, not pulled in:** this §12 section-history is itself an `audit.py` `doc_rot` WARN (now 23 entries ≥ the 12-entry condense threshold, ADR-49/65) — condensation is an operator-gated removal.
- v2.22 (2026-06-21) — §12 condensed: v1.0–v2.17 rolled into the `git log --follow -p -- CLAUDE.md` pointer above (ADR-49/65, info-preserving — no history lost), clearing both the `doc_rot` section-history WARN (had reached 23 ≥ 12 entries) and the file-budget WARN (the v2.21 §11 ADR-76–80→85–89 rotation had pushed the file to 201 > the self-declared 200-line budget). Operator-approved condensation, landed with the 2026-06-21 three-audit consolidation; targeted same-day edit, `last_reviewed` unchanged.
- v2.23 (2026-06-23) — corpus-drift cleanup (2026-06-23 fidelity audits): §11 ratified ADR-88/89 from **Proposed** → Accepted (911b561; status-prefix dropped per the index convention) and §8 refreshed the repo-skills inventory ("no skills dir yet" → `.claude/skills/` holds `verify` + `check-against-spec`). Companion genuine end-to-end re-read confirmed the rest current; `last_reviewed` re-stamped 2026-06-23.
- v2.24 (2026-06-25) — §8 self-contradiction fixed (2026-06-25 process-trigger audit): the user-level (`~/.claude/skills/`) list no longer claims a `verify` skill — it was archived 2026-06-05 (machinery-c3); the live `verify` is hub-local and was already (correctly) listed under Repo-level, so §8 contradicted itself. Replaced the stale bullet with a one-line pointer to the archive + the live hub-local copy. Companion end-to-end re-read confirmed the rest current; `last_reviewed` re-stamped 2026-06-25.

---

**Last updated:** 2026-06-25
**Maintained by:** Rob
