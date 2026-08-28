---
last_reviewed: 2026-08-28
reconciled_with: handoff-process@6.3.0
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.67 — 2026-08-28 -->

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

- **Chapter pointers** (`ARCHITECTURE.md` is a six-chapter map; jump to the topic — doctrine lives there + the cited ADRs, never resident here): cloud/nightly Routine + spec-orchestration + t-shirt model routing → **Ch3 Automation axes**, the nightly outcome loop → **Ch6 Verification mesh**; which organ fires when (hooks/skills/commands/agents/gates) → **Ch2 Organ map**; what's distributed where (carriers / child floor / browser bundle) → **Ch4 Distribution & transfer**. **The daily working mode is NOT in ARCHITECTURE** — parallel worktree lanes, lane dispatch and the ADR-110 batch protocol live in `protocols/PLAYBOOK.md` **Ch8 "Session boundaries"**.
<!-- methodology:end id=repo-architecture -->

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs (`VISION.md`, `CLAUDE.md`, etc.); `ADR-NN-topic.md` for decisions; `YYYY-MM-DD-slug.md` for dated artifacts; `council-out-YYYYMMDD_HHMMSS-topic.md` for Council CLI output; kebab-case otherwise
> **[HUB - methodology]** region `conventions-commit-branch` - single-sourced from the hub; do not edit these lines here.
<!-- methodology:start id=conventions-commit-branch owner=hub -->
- **Commits & branches:** Branch prefixes are `feat/ fix/ docs/ chore/` (author-chosen branches — these four only), **plus four machine-produced lane prefixes: `worktree-<name>` (native parallel-session worktrees, `claude --worktree` / EnterWorktree), `epic/<slug>` (root-provisioned epic lanes, §14a), `claude/<slug>` (Anthropic cloud-session lanes), and `automation/<slug>` (organ-produced replication lanes — admitted 2026-08-06 by architect ruling, register `protocols/STANDING_RULINGS.md` B5). Lane branches are never self-merged and never author-invented — a brief that names a lane branch names it in one of these shapes; a new machine-produced lane prefix enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface.** Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.
<!-- methodology:end id=conventions-commit-branch -->
- **Testing:** `uv run --locked pytest -x --tb=short` (ADR-106 §4 — the gate set runs through the locked env; a bare `pytest` resolves nothing on a clean checkout). In a lane the per-step cadence is the **targeted** files covering that lane's diff; the **full suite runs once, at integration** ([#528]; PLAYBOOK Ch5)
- **Linting:** `uv run --locked ruff check --fix` (manual / via `/save`); `ruff check` is also enforced as a pre-commit gate (see §9) — violations block commits
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal only; not enforced (ADR-27; enforcement withdrawn per ADR-48)
- **File lifecycle:** Append-only: `LESSONS.md` (never edit; a contiguous older block MAY relocate byte-identical to `LESSONS-legacy-<span>.md` — ADR-29 2026-07-17 chronological-archival exception), `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file; an ADR *status line* is editable in place on ratification per §5 item 3 / ADR-94). Living (update in place): `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`. **Generated: `BACKLOG.md`** — **never hand-edit it**; edit `tasks/`, then run `uv run --locked python scripts/gen_task_tree.py --emit-source` (source-of-truth flip ADR-107 §7.2, [#439], 2026-07-28; `audit.py::check_task_tree_coherence` gates it).
- **Freshness cadence:** the stamped set is **computed, not restated here** — `scripts/canonical_docs.py::FRESHNESS_FILES` (the portable base a consumer inherits) plus `audit.py::_HUB_ONLY_FRESHNESS_FILES` (the hub-only `protocols/` extras). A `last_reviewed` stamp means *re-read end-to-end and confirmed accurate (or drift filed)* — **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last edit (edited-but-not-re-reviewed) and warns past a 30-day backstop. Bump only after a genuine review. See PLAYBOOK "Canonical-file freshness cadence".
- **Never restate a count or roster in prose** — cite the surface that computes it (`uv run --locked python scripts/audit.py checks`, `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, the manifest `carriers:` block). A number typed into a doc is stale at the next commit: ARCHITECTURE Ch2's pre-commit gate list proved it **three times** before the enumeration was retired in favour of its pointer (2026-08-23), and the Freshness-cadence line directly above restated a 5-file set against a live 9 until 2026-08-23.
- **Resolve a locator before you act on it** — a `file:line`, heading, SHA, branch or `[#id]` you have not opened is a claim, not evidence; run **`/preflight`** over any contract, brief or handoff first. This is the most-recorded executor failure in the 2026-08-21 governance-drift audit, and that audit's own replacement locator for `validate_doc_claims.py` was itself off by one — the rule binds the auditor too.
- **TDD — a build-arc standard, not a blanket mandate; both halves are live.** ADR-108 §B binds *every build arc*: "RED-first witnesses, failing tests before build code, frozen after freeze", as "expectations the harness enforces, not per-arc negotiations". The **ex-ante** half — the architect authors and freezes the executable pass/fail criterion *before* the build; CC may strengthen it, **never weaken** it — is the ADR-81 amendment 2026-06-24, mirrored at PLAYBOOK Ch12.1 "Definition of shipped". What is **not** live is a blanket mandate: Council rejected "Mandatory TDD" (`protocols/ENVIRONMENT.md` Rejected list) and nothing reinstated it. Say partial when it is partial.
- **Spec-driven development.** ADR-108 §B: "rule-first, spec before build, acceptance contract ex-ante". Live mechanisms, not aspiration: the `check-against-spec` skill (enumerates the reconciliation sites when a spec version advances), the non-blocking `coherence-nudge` pre-commit hook over `_SPEC_REGISTRY`, the `reconciled_versions` audit check, and the `reconciled_with:` frontmatter stamp this file carries.
- **Dependencies (ADR-106).** The environment is *declared* by `pyproject.toml` + `uv.lock` + `.python-version` and rebuilt by `uv sync --locked`; `uv` itself is pinned **exactly**, and a uv bump is its own gated change — never incidental. Every gate invokes `uv run --locked …`, so a bare `python`/`pytest` in a doc or runbook is a defect, not a shorthand. Fleet-facing rows live in `ecosystem/dependency-baseline.yaml` (only deps a consumer needs to *operate a methodology mechanism*); the code-edge axis is ADR-88/ADR-89 + `scripts/scan_undeclared_edges.py` / `scripts/reverse_dep_oracle.py`.
- **Decision funnel (ADR-111).** Every audit finding is triaged into **exactly one** of OWNED (an open row covers it — attach evidence, birth nothing) / DISCHARGED (already done or ruled — record the locator, and it must resolve) / CANDIDATE (needs a decision — becomes an intake) / REJECTED (reason recorded, not relitigated). "A finding may not become a backlog row without triage": the only path is CANDIDATE → intake (ADR-98) → ratification, and "a triage pass that routes most items to (c) has not triaged". Question routing is ADR-108 §A — the operator rules **functional** questions, the architect rules **technical** ones (revertability, not escalation), AI Council distils contested technical ones.

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
7. **Executable rules live in `~/.claude/` with `verify:` lines** — that is the fleet-wide home (ADR-54), and this repo authors no new rule class outside it. **Carve-out, recorded rather than left contradicting itself:** `.claude/rules/` IS a live repo-local rule home — `git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES) and is rostered at §9. The old absolute wording forbade at §5 exactly what §9 lists approvingly; re-scoped on the v2.61 rule-4 precedent (converge on the accurate site).
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
Repo-level (`./.claude/commands/` — machine-enumerated from command-file frontmatter, generated like §9's roster; regenerate: `uv run --locked python scripts/gen_claude_rosters.py --write`):

@.claude/generated/commands-repo.md
<!-- methodology:end id=commands-repo-roster -->

`/handoff` generates a handoff per `HANDOFF_PROCESS.md` v6 (ADR-82); `/handoff-verify` is its check-time counterpart — one CC-side run of the whole live gate, one evidence block (v6 §5; R1). Deployed methodology commands — `/review-closures`, `/ship`, `/override` — are enumerated in the generated roster (§9, `@`-imported); governance stays at canonical homes: ADR-70 Tier-1 + §8 / `ARCHITECTURE.md` "Tier-1 self-enforcing lifecycle" ([#76] — the hub uses the plugin's, not a hub-local duplicate) for `/review-closures` + `/ship` (the `/ship` worktree-refusal is the seed-state `LESSONS.md` 2026-06-19 lesson); ADR-85 §4 for `/override` — **but note the ADR-85 amendment 2026-08-03 §A2 RETIRED that local-token path**: `/override` no longer discharges the ADR-85 obligation (the Stop hook is advisory in full and has nothing to override), and the sole escape for the pre-push hard leg is `git push --no-verify`, made non-silent by the `journal_spine_anchor` audit backstop. (When to invoke each + auto-vs-manual for hooks: PLAYBOOK §"Usage protocol: which command / hook, when".)

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls)

(The `verify` skill is **not** user-level — the live copy is hub-local, listed under Repo-level below. And `boot`/`session-summary`/`handoff`/`save` are **commands**, not skills — see §7; current Claude Code also surfaces commands in its skill picker, but their files live under `commands/`, not `skills/`.)

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

The deployed methodology corpus (the commands / hooks / config the deploy tool ships to a consumer) is machine-generated from `deploy/manifest-v*.yaml` `components:[].roster` and `@`-imported below — regenerated-from-source, not review-stamped (deliberately OUT of the freshness gate; regenerate: `uv run --locked python scripts/gen_methodology_roster.py --write`). §7–§9 stay hand-authored for the hub-LOCAL surface (items with no manifest entry). Drift-gated by the `roster-freshness` pre-commit hook.

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

Machine-enumerated (last 5 by number, from `docs/decisions/ADR-*.md` headers; regenerate: `uv run --locked python scripts/gen_claude_rosters.py --write`). Editorial one-liners live in `docs/decisions/README.md`; full governance list in `ARCHITECTURE.md`.

@.claude/generated/recent-adrs.md
<!-- methodology:end id=recent-adrs-roster -->

## 12. Section history
<!-- scope: meta -->
> **[REPO - local]** region `section-history` - this repo owns these lines.
<!-- methodology:start id=section-history owner=repo -->

> _Entries v1.0–v2.64 condensed to git history per ADR-49/65 (info-preserving — full prior history: `git log --follow -p -- CLAUDE.md`)._

- v2.65 (2026-08-23, governance-drift discharge — lane `lane-docs-governance`, R1 top-10 item 10) — **the file buys headroom and spends it on the two rules the 2026-08-21 audit showed would have prevented its most-recorded failures.** **Landed:** §4 gains **M2** (never restate a count or roster — cite the computing surface) and **M1** (resolve a locator before acting; run `/preflight`); §4's File-lifecycle line moves `BACKLOG.md` out of *Living / update in place* into **Generated** — the audit's highest-operator-impact finding, wrong since the ADR-107 §7.2 flip of 2026-07-28 and the one surface of three that still told the executor to hand-edit it; §5 rule 7 is re-scoped to record the `.claude/rules/` carve-out it had been forbidding at §5 while §9 rostered it; §3's chapter pointers finally name **PLAYBOOK Ch8** for lanes/worktrees/batch dispatch, which neither this file nor ARCHITECTURE referenced despite a JOURNAL that is overwhelmingly lane work. **DEVIATION, stated because it is the one instruction this lane did not execute where it was told to:** the contract put M1 in **§10**, and §10 is a HUB-single-sourced Form-A region (`antipatterns-universal`) whose body must stay **byte-identical** to `templates/claude-regions/antipatterns-universal.md` (the v2.39/v2.42 discipline `boundary_headers.py` documents, and that template is inside `silent_rule_ratchet`'s scope while this file is not). Editing §10 alone would break fleet parity and the line would never reach a consumer; editing the template is outside this lane's contract. So M1 landed in §4 (repo-owned) instead — **if the rule is meant to be universal it still owes a lockstep §10 + template act, which this lane did not take.** **Budget arithmetic, measured with the file's own checker** (`validate_doc_rot.scan_file_budget`, which excludes comment-only lines): opened at **197/200** — not the 198 the audit measured, nor the headroom-4 v2.64's own bullet claims; condensing the three oldest bullets (v2.59, v2.60–v2.62, v2.63) into the git pointer freed **6** counted lines (3 bullets + their blank separators) on the v2.59/v2.62/v2.64 precedent — ADR-49 and ADR-65 §1 both name git as the destination; spent **4** (M1, M2, and this bullet with its separator), C1 / rule 7 / the §3 pointer being in-place rewrites at zero net. Closes at **195/200, headroom 5** — real headroom, per v2.64's ruling that the file buy rather than shave. No content lost: all three condensed bullets stay recoverable verbatim via `git log --follow -p -- CLAUDE.md`. L10 version 2.64→2.65. Genuine full-file end-to-end re-read from disk this session (all 12 sections). **Still knowingly left, unchanged from v2.64:** §10's *“Narrating or managing AGENTS.md”* anti-pattern remains false doctrine after ruling A2 — `[#577]` owns that correction in the same commit as the file it describes, and it is inside the same hub region this lane may not touch, so the reason it stands is now twofold rather than one.

- v2.66 (2026-08-23, LANE-L5 `docs-actual-state`, M6) — **the file finally describes the working process, and stops restating a roster three lines under the rule forbidding it.** **Landed:** §4 gains four bullets — **TDD** (ADR-108 §B binds every build arc RED-first; the ADR-81 2026-06-24 ex-ante frozen criterion is the other half; a *blanket* mandate is **not** live — Council rejected it and nothing reinstated it, so the bullet says partial), **spec-driven development** (ADR-108 §B + the live `check-against-spec` / `coherence-nudge` / `reconciled_versions` / `reconciled_with:` mechanisms), **dependencies** (ADR-106 — `pyproject.toml` + `uv.lock` + `.python-version`, `uv` pinned exactly, `ecosystem/dependency-baseline.yaml`, ADR-88/89), and the **decision funnel** (ADR-111's four outcomes, CANDIDATE → intake → ratification as the only path to a row; ADR-108 §A routing). **Corrections:** every bare `python`/`pytest`/`ruff` invocation in this file is prefixed `uv run --locked` — ADR-106 §4 moved the gate set there, and a bare `python scripts/audit.py checks` **provably fails on a clean checkout** (`ModuleNotFoundError: click`), so four of this file's own pointers named a command that does not run; §4's Freshness-cadence line restated a **5-file** set against a live **9** (`canonical_docs.FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`) and is now a pointer — an M2 violation sitting one line above M2 itself, which the M2 bullet now records as its second witness. **DELIBERATELY NOT converted:** §9's pre-commit roster. It *is* the surface `validate_doc_claims`'s `precommit_hook_roster` leg checks against `.pre-commit-config.yaml`, one line per hook by construction (`extract_claimed_hooks` takes each bullet's leading backtick token), so collapsing it would disarm the gate and register as a silent `anchor-missing` WARN — a restated roster a gate verifies is not M2's failure class. **Budget, measured with `validate_doc_rot.scan_file_budget`:** opened **195/200**; reclaimed **6** (the v2.64 bullet condensed into the git pointer per ADR-49/65 — the v2.59/v2.60-62/v2.63 precedent v2.65 itself invoked; §8's two parentheticals merged; §7's usage-protocol parenthetical folded up); spent **6** (four process bullets + this bullet and its separator); C-01..C-05 and the three regen pointers are in-place rewrites at zero net. Closes **195/200, headroom 5** — bought, not shaved. **Hub regions untouched:** all 8 `owner=hub` bodies stay byte-identical to `templates/claude-regions/*.md`, verified live. Two stale claims found *inside* them are handed on rather than half-fixed: §6 step 5's bare `pytest --collect-only` (same ADR-106 defect, needs a lockstep template edit), and §10's AGENTS.md anti-pattern, **still knowingly left** — `[#577]` owns it, unchanged from v2.64/v2.65. L10 version 2.65→2.66. Genuine full-file end-to-end re-read from disk this session (all 12 sections). Full census, verdicts and arithmetic: `docs/audits/2026-08-23-technical-lane-docs-actual-state.md`.

<!-- methodology:end id=section-history -->

- v2.67 (2026-08-28, closure-harvest lane act 5) — **coupled-move only: the `reconciled_with` edge follows HANDOFF_PROCESS to v6.3.0** (role residency — the assembler emits a 3-line ROLE PIN instead of inlining `protocols/HANDOFF_BOOT.md`; measured 50,852 → 34,624 B on a real cut). This file's BODY is unchanged — no rule added, removed or reworded — so the bullet records a stamp, not a doctrine change. **Stamp semantics:** `last_reviewed` moves because the file was re-read end-to-end from disk this session before the edge was bumped. **Re-confirmed still-owed, both inside hub-single-sourced Form-A regions this lane may not touch alone:** §6 step 5's bare `pytest --collect-only` (the ADR-106 defect — needs a lockstep `templates/claude-regions/session-start-protocol.md` act), and §10's *“Narrating or managing AGENTS.md”* anti-pattern, now **provably** false doctrine rather than arguably so: **ADR-115** (Accepted 2026-08-25) supersedes ADR-53 Decision 2 and amends ADR-101 §1 to admit `AGENTS.md`. `[#577]` owns that correction. Budget, measured with the file's own checker (`validate_doc_rot.scan_file_budget`): opened **195/200**, spent 2 (this bullet + its separator), closes **197/200, headroom 3**.

---

**Last updated:** 2026-08-28
**Maintained by:** Rob
