---
last_reviewed: 2026-07-05
reconciled_with: handoff-process@5.5
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.27 — 2026-07-04 -->

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
- **File lifecycle:** Append-only: `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file; an ADR *status line* is editable in place on ratification per §5 item 3 / ADR-94). Living: `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` (update in place).
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
3. **ADRs, transcripts, handoffs, and audits are immutable** — supersede with a new file or an in-file amendment marker; never edit in place. **ADR ratification exception (ADR-94):** an ADR's *status line* MAY be edited in place on ratification (e.g. Proposed → Accepted) — the status line is metadata, not decision content. This exception is ADR-specific and covers the status line only; ADR decision content, and transcripts / handoffs / audits in full, remain immutable.
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
Deployed methodology commands — `/review-closures`, `/ship`, `/override` — are enumerated in the generated roster (§9, `@`-imported); governance stays at canonical homes: ADR-70 Tier-1 + §8 / `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" ([#76] — the hub uses the plugin's, not a hub-local duplicate) for `/review-closures` + `/ship` (the `/ship` worktree-refusal is the seed-state `LESSONS.md` 2026-06-19 lesson); ADR-85 §4 (explicit + logged, no auto-bypass — the gate's only escape) for `/override`.

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
- `roster-freshness` — regen-and-diff gate for `.claude/methodology-roster.md` vs `deploy/manifest-v*.yaml` (`gen_methodology_roster.py --check`; blocks a hand-edited or manifest-stale roster); HUB-ONLY (n=1), [#244] P3
- `validate-backlog` — BACKLOG.md story-map schema (ADR-66)
- `audit-health` — self-conformance gate: `audit.py health` (FAIL blocks the commit, WARN informs); added by [#69]
- `ruff` — lint gate: `ruff check` (gate mode; blocks on violations); version-pinned >=0.15.5 via `pyproject.toml`; `language: system` (no mismatch); added by [#13]
- `coherence-nudge` — **non-blocking** forgotten-version-bump nudge: a registered spec (`_SPEC_REGISTRY`) changed-without-a-version-bump prints a stdout nudge + logs `logs/coherence-nudge.log`; always exits 0 (a nudge, not a gate); pairs with the `reconciled_versions` audit check
- `backlog-id-on-close` (commit-msg) — require `[#id]` when a commit removes a backlog task
- `block-ff-push` (pre-push) — the PREVENT half of core-invariant #5 ([#153]): refuses a push that would put a non-merge commit on main's first-parent spine (a direct-to-main commit or a true FF merge); a `--no-ff` merge passes. `scripts/block_ff_push.py`, HUB-ONLY, fail-soft to exit 0 on any git error, bypass `git push --no-verify` (the `no_ff_merges` audit WARN stays the post-hoc backstop). Delegates the scan to `validate_no_ff.find_violations` (one shared FF-signature). **One-time local activation: `pre-commit install --hook-type pre-push`** (the config's `default_install_hook_types` only wires it on a fresh install). `validate_no_ff` stays the detect-and-surface WARN; this is the distinct prevent organ (separate file, so validate_no_ff's never-gates contract is preserved).

Session hooks (`.claude/settings.json`, project-level — merges with, does not replace, the `~/.claude` hooks): `SessionStart` surfacing (`fleet_health.py` Tier-2 fleet digest [#72] + `surface_triage.ps1` nightly-triage + `billing_leak_sentinel.ps1` [#101] + `changelog_sentinel.py` [#113]), a `Stop` backpressure hook (`session_end_backpressure.py`), and the ADR-77 `PreToolUse` transcript-immutability guard (`block_immutable_edits.py`) — each fail-soft (surfacing) or fail-closed (the guard) per its row. **Full live organ inventory (trigger × layer × failure posture) → `ARCHITECTURE.md` Ch2 Organ map.** The Tier-1 closure loop runs via the enabled `tier1-lifecycle` plugin (`Stop → propose_closures.py`; detect-and-propose, never mutates BACKLOG) + the global `~/.claude` `surface-closures.ps1` L0 surfacing — not hub-local `settings.json` (the 5c convergence; ARCHITECTURE "Tier-1 self-enforcing lifecycle").

Rules (`.claude/rules/`):
- `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end

### Methodology-deployed roster (generated — do not hand-edit)

The deployed methodology corpus (the commands / hooks / config the deploy tool ships to a consumer) is machine-generated from `deploy/manifest-v*.yaml` `components:[].roster` and `@`-imported below — regenerated-from-source, not review-stamped (deliberately OUT of the freshness gate; regenerate: `python scripts/gen_methodology_roster.py --write`). §7–§9 stay hand-authored for the hub-LOCAL surface (items with no manifest entry). Drift-gated by the `roster-freshness` pre-commit hook.

@.claude/methodology-roster.md

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

- ADR-93: Floor provisioning model A — the consumer **commits** its ADR-78 methodology floor (tracked via a `.gitignore` negation, not gitignored) behind a **two-leg hash-guard** (a SessionStart guard + the commit-time `floor-hash-verify` hook, both running `.claude/check_floor_hash.py`), so floor drift fails loud; supersedes PLAYBOOK §20's prior "local-only" framing; armed + conformance-proven (#226/#230)
- ADR-94: ADR status line mutable on ratification (decision content frozen) — an ADR's *status line* MAY be edited in place on ratification (Proposed → Accepted); the exception is **ADR-status-line-only** (ADR decision content + transcripts/handoffs/audits stay fully immutable); standardizes go-forward on Pattern B (ADR-92) over ADR-88/89's frozen-header Pattern A; narrows CLAUDE.md §5 item 3 + §File-lifecycle; the header↔README coherence check is filed **#242**, not built (Fable consult #1, operator-signed)
- ADR-95: AI-council query lane-split — "architect frames the question, CC mechanically expands"; the ai-council-query specialization of ADR-87's equilibrium contract applied to the ADR-67 loop's Frame step; **record-only**, no `/council` wiring built (Fable consult #1)
- ADR-96: Deploy remove leg — the add-only deploy engine gains prune: `detect_prune`/`prune`/`verify_pruned` on the carrier contract (opt-in per carrier; `verify_pruned` gates the record, D9), hash-guarded (a locally-modified target is **REFUSED**, never clobbered), **2-state** `active → removed` (no `deprecated` tier, D3), converge-then-prune with destroy-confirm; tombstone = the retained manifest entry + JOURNAL + the ADR. Functional-proof (ADR-81 leg-e) on ai-council n=1: `ruff-gate` pruned + verified ABSENT; corpus v1.2.0
- ADR-97: Tree orchestration — architect-root + epic-chat lanes: **root** (exactly one) owns ADRs / backlog structure / parallelism rulings / ALL merges (serial `--no-ff`) / worktree lifecycle / closure; **epic lanes** (one browser chat + one worktree per epic, branch `epic/<slug>`) commit-and-STOP inside an explicit FILE-BOUNDARY, never merge/self-provision; 2–3-lane cap; every lane boots from a §14a EPIC handoff and closes with a §14b EPIC RETURN (`gen_handoff.py --mode epic`); formalizes the 2026-07-04 lived precedent, extends PLAYBOOK §8 + ADR-87

## 12. Section history
<!-- scope: meta -->

> _Entries v1.0–v2.17 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.18–v2.24 (2026-06-12 → 2026-06-25, condensed 2026-07-05 per ADR-49/65, operator-granted — full entries: `git log --follow -p -- CLAUDE.md`): §1 first-read #4 repointed to the bundle's `HANDOFF_BOOT.md` + the canonical operator runbook (v2.18); ESSENTIALS joined the freshness gate / `_FRESHNESS_FILES` (v2.19); §9 gained the `block-ff-push` pre-push prevent organ, core-invariant #5 (v2.20); §11 rotated 76–80→85–89 + §7 reconciled to the live command set incl. `/changelog-review`/`/override`/`/ship` (v2.21); §12 v1.0–v2.17 condensed to the git pointer, clearing doc_rot + file-budget WARNs (v2.22); ADR-88/89 ratified Proposed→Accepted + §8 repo-skills refresh (v2.23); §8 user-level-verify self-contradiction fixed — live `verify` is hub-local (v2.24). Each landed with its genuine re-read + `last_reviewed` re-stamp.
- v2.25 (2026-07-02) — §11 "last 5" rotated **85–89 → 89–93** (the deferral carried since v2.19–v2.21, now closed for the deploy cohort): genuine reads of ADR-90/91/92/93 (all Accepted — the ARCHITECTURE-currency arc [#222]/[#223]/[#224]); dropped 85–88 (retained in `docs/decisions/README.md` + ARCHITECTURE Governing-ADRs), added the resolver-allows-N / corpus-versioning / deploy-runbook / floor-model-A quartet. Fixed the stale version comment (**2.23** while v2.24 had already landed → **2.25**). Companion genuine end-to-end re-read confirmed §1–§10 current; `last_reviewed` re-stamped 2026-07-02.
- v2.26 (2026-07-03) — Fable consult #1 ruling #3 landed (operator-signed): §5 item 3 narrowed — the "ADRs/transcripts/handoffs/audits immutable" rule gains an **ADR-status-line-only** ratification exception (ADR-94: an ADR's *status line* is editable in place on Proposed→Accepted; decision content + transcripts/handoffs/audits stay fully immutable), standardizing go-forward on Pattern B (ADR-92) over ADR-88/89's frozen-header Pattern A; §"File lifecycle" (L55) reconciled to match; §11 "last 5" rotated **89–93 → 91–95** (dropped 89/90, added the new ADR-94 + the consult's ADR-95 lane-split). The header↔README status-coherence check is filed **#242** (not built); ADR-88/89 retro-normalization deferred. Companion end-to-end re-read confirmed §1–§10 current; `last_reviewed` re-stamped 2026-07-03.
- v2.27 (2026-07-04) — [#244] P3 generated-roster currency (Fable R3): the deployed methodology corpus (commands / hooks / config) is now machine-generated from `deploy/manifest-v*.yaml` `components:[].roster` into `.claude/methodology-roster.md`, `@`-imported via a new §9 "Methodology-deployed roster (generated)" subsection — so it can no longer be hand-maintained and thus cannot rot. §7 trimmed of the three deployed commands (`/review-closures`/`/ship`/`/override`), replaced by a pointer note that keeps every non-enumeration rationale at its verified canonical home (ADR-70 + §8/ARCHITECTURE [#76]; the `/ship` worktree-refusal `LESSONS.md` 2026-06-19; ADR-85 §4). §9 gains the blocking `roster-freshness` regen-and-diff hook. The generated file is deliberately OUT of `DEFAULT_FRESHNESS_FILES` (currency = regen); CLAUDE.md STAYS in (100% hand-prose, gated). `@import` sanctioned: the ADR-45 / 2026-05-26-council `@path` ban is browser-handoff-delivery-scoped, NOT local session-boot (quoted at review; the live `@.claude/CLAUDE-FLOOR.md` precedent corroborates). Methodology version HELD (hub-only n=1 tooling; consumer rollout is P6). Hub-local items stay hand-authored (no machine source; follow-up filed). Genuine end-to-end re-read confirmed §1–§11 current; `last_reviewed` re-stamped 2026-07-04.
- v2.28 (2026-07-05) — handoff-process 5.3→5.4 reconciliation (overnight-run Block D): frontmatter `reconciled_with` re-stamped @5.4 after site-enumeration (the §1/§7 handoff references are major-level and unaffected — the v5.4 change is additive-only: §5 structural anti-bluff + §13 generator note, documenting the `9d5ebe5` mechanism). Genuine end-to-end review basis: full-file read at session boot + §7/§8/§9 claims exercised live through the night's work; `last_reviewed` re-stamped 2026-07-05.
- v2.29 (2026-07-05) — handoff-process 5.4→5.5 reconciliation completed at Wave-1 root integration: the frontmatter `reconciled_with` @5.5 re-stamp itself landed IN-GRANT on the Epic 2 branch (`489c51f`, the 5-edge atomic move — its compressed check-against-spec sweep verdicted all 49 CLAUDE.md sites: only L3 stale; §1/§7 v5 refs major-level fine, §12 historical entries fine); this §12 entry is the recorded ARCHITECT-REVIEW-PENDING content edit **beyond that grant**, applied by root at integration per ADR-97 (v2.28-precedent style). Companion §11 "last 5" rotated **91–95 → 93–97** after genuine reads of ADR-96 (deploy remove leg) + ADR-97 (tree orchestration — the v5.5 decision record); dropped 91/92 (retained in `docs/decisions/README.md` + ARCHITECTURE Governing-ADRs). Genuine end-to-end re-read basis: full-file read at root-lane boot + §5/§7/§9 claims exercised live through the three Wave-1 merges (JOURNAL prepend-resolution, /override gate, pre-commit roster); `last_reviewed` 2026-07-05 stands (same-day arc rule).

---

**Last updated:** 2026-07-05
**Maintained by:** Rob
