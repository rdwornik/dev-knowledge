# ACT ONE, PRESERVED — the refused half of DC-3, kept as `[#628]`'s input artifact

- **Class:** technical · **Date:** 2026-09-01 · **Consumed by:** `[#628]`, `[#614]`
- **Source commit:** `6f226b3408b939fc7ac168b7b880261d439d192d` on the now-deleted branch `worktree-lane-b-3-claude-md-genre`
- **Author of the source:** the batch-E DC-3 lane · **Preserved by:** CC (Opus 5, orchestrator)

---

## Why this file exists

`[#628]` names this diff as its **input artifact**: the refused lane's report IS the
specification, and its guard-tracing research narrows that arc's scope from the A3 census's ten
breaking consumers to a measured set.

**A branch is a teardown target, not storage** (architect's ruling, batch-F cut). The commit lived
on a branch kept alive purely to hold it, which is the one thing branches must not be for — an
unmerged branch is invisible to every gate, survives on no schedule, and is one `gc` from gone.
So the content moves into an immutable, indexed, citable artifact and the branch is deleted
locally and on origin in the same act.

**WHAT IS DELIBERATELY NOT REPRODUCED HERE.** The commit deletes `protocols/ESSENTIALS.md`
(185 lines). Those 185 lines are **unchanged on `main`** at blob `02228ab28737`
— reproducing them as 185 `-` lines would preserve nothing and bury the part that matters.
The deletion act is exactly `git rm protocols/ESSENTIALS.md`. Everything else is below, verbatim.

**Which hunks are Act One** is settled in `docs/audits/2026-09-01-technical-dc3-split.md` §2,
hunk by hunk. Acts TWO and THREE from this same commit were reconstructed on a fresh branch and
merged at `ec5f5507`; the CLAUDE.md and PLAYBOOK.md diffs below therefore contain **both** the
refused Act-One hunks and the accepted Act-TWO/THREE ones, in their original lane wording. The
ledger is the key.

## The commit message, verbatim — the guard-tracing research

This is the highest-value part and the reason a `git show` after deletion would not do.

```
docs(claude-md): ESSENTIALS dissolved, CLAUDE.md's genre purified [#614]

Batch-e-b-2 (DC-23, CUT-3(a)): ACT ONE dissolves protocols/ESSENTIALS.md,
ACT TWO purifies CLAUDE.md's genre, ACT THREE removes the now-conditional
VISION lines (DC-1 confirmed merged 2026-08-31, JOURNAL.md 2026-08-31 (d)).

ACT ONE. protocols/ESSENTIALS.md archived (git history) after confirming
it was ~95% pointers back to PLAYBOOK.md already -- every section but one
already cited its PLAYBOOK canonical home. The sole exception, "How Claude
thinks" (VISION.md defers to it, "no duplication"), relocated to PLAYBOOK
Ch8. Deletion-safety researched exhaustively first: every canonical_docs.py
registry membership (CANONICAL_OPTIONAL, FRESHNESS_FILES, SECTION_HISTORY_
DOCS, STRUCTURE_DOCS, CONFORMANCE_V2_SCAN) is consumed by code with an
explicit exists()/try-except guard or pure string comparison -- confirmed
by reading each consumer and running the live suite (33/33 essentials-
scoped tests green at baseline). Five stale "ESSENTIALS summarizes
PLAYBOOK" clauses in CLAUDE.md removed/repurposed to the still-true
hub-region<->template byte-match concern. ~20 stale ESSENTIALS citations
in PLAYBOOK.md itself corrected in passing (file-type tables, browser
resumption steps, dangling "ESSENTIALS keeps the pointer" footnotes).

ACT TWO. The branch-prefix enum and the TUI output-formatting rationale
(both hub regions) shrank to point-of-use bullets; full provenance moved
to PLAYBOOK Ch3 "Branch prefixes -- the closed enum" (new) and Ch8's
existing "Output the operator copies into browser chat" (which already
called the CLAUDE.md bullet "the point-of-use rule" -- CLAUDE.md just
wasn't one yet). Both ObsidianVault/ mixing-advisory clauses deleted per
ruling CUT-2 (repo-owned, zero fleet consequence).

ACT THREE. VISION.md dropped from CLAUDE.md's critical-paths and file-
lifecycle lists -- DC-1 already retired it from CANONICAL_MANDATORY.

Byte cap: 24,387 B -> 24,223 B (ceiling 24,576 B, `tests/test_claude_md_
byte_cap.py` re-verified green). PLAYBOOK TOC regenerated (one new H3).
Discovered and fixed in-flight: the floor template's own edit introduced
a false same-repo pointer match ("PLAYBOOK.md") that broke
test_floor_integrity_valid_floor_passes -- reverted to the non-triggering
form before it could regress a test outside this lane's write-scope.

Targeted suite: 675 relevant tests across test_claude_md_byte_cap,
test_boundary_headers, test_canonical_docs, test_audit, test_generate_
floor, test_deploy_floor, test_gen_methodology_roster, test_validate_
doc_rot, test_validate_doc_structure -- all green except three
pre-existing, unrelated FAILs already on main before this lane started:
journal_spine_anchor (four 2026-09-01 batch-E merges carry no JOURNAL
anchor -- other lanes' commits) and the calendar-driven backlog-accretion
arm on BACKLOG#267 (51-53d spans crossing the 30d threshold unedited).
ruff clean. No file touched outside the frozen write-scope.

Owed, named per REFUSE-TO-PROCEED discipline rather than routed around:
templates/child-methodology-floor.sha256 is now stale against its .tmpl
source (regenerate via the hub generator at next deploy -- the sidecar
itself is outside this lane's write-scope); VISION.md:46 and README.md's
citations of the dissolved `protocols/ESSENTIALS.md "How Claude thinks"`
are stale (both files outside this lane's write-scope).

kill-candidates: none -- no BACKLOG row closed or opened by this lane.

Claude-Session: https://claude.ai/code/session_01K6XUJ8xQznTxEzcxKoYTsj
```

## The diff, verbatim (ESSENTIALS.md deletion excluded, per above)

```diff
diff --git a/CLAUDE.md b/CLAUDE.md
index 5c14e6a8..462682bf 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -7,13 +7,13 @@ owner: Rob
 
 # CLAUDE.md — Dev Knowledge
 <!-- scope: meta -->
-<!-- version: 2.70 — 2026-09-01 -->
+<!-- version: 2.71 — 2026-09-01 -->
 
 > **Session boot contract for Claude Code in this repo** — auto-read at session start (ADR-53, as re-pointed by ADR-115). **Genre:** a rule lives here only if a session needs it *before it can act*; rationale, history and per-organ detail live at the home each line cites.
 >
 > **Budget — bytes bind. ≤24,576 B**, gated by `tests/test_claude_md_byte_cap.py`. ADR-53's ≤200 lines is kept, not replaced (`validate_doc_rot._FILE_SIZE_BUDGETS`, WARN-only) — but a line count is gameable by density, and bytes are what a session pays.
 >
-> **Universal rules:** `protocols/ESSENTIALS.md` (always-on); `protocols/PLAYBOOK.md` is the on-demand reference, never a boot-time read (§1).
+> **Universal rules:** this file carries the always-on subset; `protocols/PLAYBOOK.md` is the on-demand reference, never a boot-time read (§1).
 
 ## 1. First read (session start)
 <!-- scope: meta -->
@@ -22,11 +22,10 @@ owner: Rob
 
 In order, read:
 1. This file (you're here)
-2. The hub methodology protocol `ESSENTIALS.md` — Rob's universal working style (read at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer)
-3. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
-4. Last 5 entries of `JOURNAL.md`
+2. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
+3. Last 5 entries of `JOURNAL.md`
 
-`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (ESSENTIALS carries the always-on subset; a consumer never copies PLAYBOOK). If ESSENTIALS — or a PLAYBOOK section a task needs — is unavailable, proceed with the other available first-read sources and flag the gap.
+`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (this file and the methodology floor carry the always-on subset). If a PLAYBOOK section a task needs is unavailable, proceed with the other available first-read sources and flag the gap.
 <!-- methodology:end id=first-read -->
 
 ## 2. Repo identity
@@ -36,8 +35,8 @@ In order, read:
 
 - **Name:** `.dev-knowledge` · **Owner:** Rob · **Status:** active, no declared tier (repo-tier system deprecated 2026-05-23)
 - **Purpose:** the universal LLM-driven development guide and methodology framework governing every project under `Dev/` — Layer 2 of the ADR-28 three-layer ecosystem model
-- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `README.md`, `VISION.md`, `ARCHITECTURE.md`
-- **Related:** `~/.claude/` (L0 runtime config) · `.claude/` (project config) · `ObsidianVault/` (pre-sales — do not mix) · `Dev/` child repos, each owning its own `CLAUDE.md`
+- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `README.md`, `ARCHITECTURE.md`
+- **Related:** `~/.claude/` (L0 runtime config) · `.claude/` (project config) · `Dev/` child repos, each owning its own `CLAUDE.md`
 - **Portable layer:** root `AGENTS.md` carries the build/test/landing facts every provider reads (ADR-115, superseding ADR-53 Decision 2); this file keeps the Claude-runtime remainder and imports it below. No fact is duplicated across the two — the importer preserves ADR-53's substance
 
 @AGENTS.md
@@ -60,12 +59,12 @@ In order, read:
 - **Naming:** UPPERCASE for top-level living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for dated artifacts, `docs/audits/` names also carrying a closed-enum class (`validate_hermetization.AUDIT_CLASS_ENUM`); `logs/` artifacts UPPERCASE-KEBAB, extension honest to the format ([#395]); kebab-case otherwise
 > **[HUB - methodology]** region `conventions-commit-branch` - single-sourced from the hub; do not edit these lines here.
 <!-- methodology:start id=conventions-commit-branch owner=hub -->
-- **Commits & branches:** Branch prefixes are `feat/ fix/ docs/ chore/` (author-chosen branches — these four only), **plus four machine-produced lane prefixes: `worktree-<name>` (native parallel-session worktrees, `claude --worktree` / EnterWorktree), `epic/<slug>` (root-provisioned epic lanes, §14a), `claude/<slug>` (Anthropic cloud-session lanes), and `automation/<slug>` (organ-produced replication lanes — admitted 2026-08-06 by architect ruling, register `protocols/STANDING_RULINGS.md` B5). Lane branches are never self-merged and never author-invented — a brief that names a lane branch names it in one of these shapes; a new machine-produced lane prefix enters this enum only via a recorded ruling (never silently); the enum stays the checkable surface.** Commit **types** follow Conventional Commits and additionally include `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.
+- **Commits & branches:** Branch prefixes are a closed enum — author-chosen `feat/ fix/ docs/ chore/`, plus four machine-produced lane prefixes `worktree-<name>`, `epic/<slug>`, `claude/<slug>`, `automation/<slug>` (each admitted only by a recorded ruling, never invented in passing — full provenance: PLAYBOOK Ch3 "Branch prefixes — the closed enum"). Commit **types** follow Conventional Commits plus `refactor` and `test` — commit types are **not** branch prefixes. Never commit directly to `main`: branch → `--no-ff` merge.
 <!-- methodology:end id=conventions-commit-branch -->
 - **Testing:** `uv run --locked pytest -x --tb=short` — a bare `pytest` resolves nothing on a clean checkout (ADR-106 §4). In a lane run the **targeted** tests for that lane's diff; the **full suite runs once, at integration** ([#528])
 - **Linting:** `uv run --locked ruff check --fix`; `ruff check` is also a pre-commit gate (§9) and blocks
 - **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal, not enforced (ADR-27/ADR-48)
-- **File lifecycle:** append-only `LESSONS.md` + `logs/TOKEN-LOG.md`; newest-first-prepend `JOURNAL.md`; immutable ADRs / transcripts / handoffs / audits; living `README.md`, `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md` — rules and exceptions at §5. **`BACKLOG.md` is generated:** edit `tasks/`, then `gen_task_tree.py --emit-source`
+- **File lifecycle:** append-only `LESSONS.md` + `logs/TOKEN-LOG.md`; newest-first-prepend `JOURNAL.md`; immutable ADRs / transcripts / handoffs / audits; living `README.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md` — rules and exceptions at §5. **`BACKLOG.md` is generated:** edit `tasks/`, then `gen_task_tree.py --emit-source`
 - **Freshness cadence:** the stamped set is **computed, not restated here** — `canonical_docs.py::FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`. A `last_reviewed` stamp means *re-read end-to-end and confirmed accurate, or drift filed*, never merely "touched"
 - **Never restate a count or roster in prose** — cite the surface that computes it (`audit.py checks`, `ecosystem/doc-counts.md`, `ecosystem/organ-index.md`, the manifest `carriers:` block). A number typed into a doc is stale at the next commit
 - **Resolve a locator before you act on it** — a `file:line`, heading, SHA, branch or `[#id]` you have not opened is a claim, not evidence; run **`/preflight`** first. The most-recorded executor failure in the 2026-08-21 governance-drift audit, and it binds the auditor too
@@ -74,11 +73,11 @@ In order, read:
 - **Dependencies (ADR-106):** declared by `pyproject.toml` + `uv.lock` + `.python-version`, rebuilt by `uv sync --locked`, `uv` pinned **exactly** — a uv bump is its own gated change. Every gate runs `uv run --locked …`, so a bare `python`/`pytest` in a doc is a defect, not a shorthand
 - **Decision funnel (ADR-111):** every audit finding is triaged into **exactly one** of OWNED / DISCHARGED / CANDIDATE / REJECTED — no finding becomes a backlog row without triage, and the only path is CANDIDATE → intake (ADR-98) → ratification. Question routing is ADR-108 §A: the operator rules **functional** questions, the architect **technical** ones
 
-**Out of scope:** code-level implementation → child repos · client/product/domain knowledge → the Obsidian vault · runtime config → `~/.claude/`. The in-hub Council transcript archive was **deleted 2026-07-22** by operator ruling — do not recreate it; the ADR-77 guard stays armed.
+**Out of scope:** code-level implementation → child repos · runtime config → `~/.claude/`. The in-hub Council transcript archive was **deleted 2026-07-22** by operator ruling — do not recreate it; the ADR-77 guard stays armed.
 
 > **[HUB - methodology]** region `conventions-output-formatting` - single-sourced from the hub; do not edit these lines here.
 <!-- methodology:start id=conventions-output-formatting owner=hub -->
-- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables (`| col | col |`) as Unicode borders (`┌─┬─┐ │ └─┴─┘`) **client-side at render time**. So a bare table looks clean in the terminal but copies into browser chat as costly border glyphs (~3× the tokens), and a rule that merely bans Claude from *writing* box-drawing is a no-op (Claude already doesn't). The working fix is at the render layer: any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, which makes the TUI render it raw/un-painted so the copied text carries no borders. Same fenced-block discipline already used for Scale-S snippets (ESSENTIALS) and downloadable prompts (§2). Persistent diagrams live on the separate human-facing visualization surface (ADR-59; the ADR-51 amendment 2026-07-05 moved Mermaid out of canonical `ARCHITECTURE.md` — its codemap is now compact text), out of scope. Full rationale + `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat".
+- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables as Unicode borders **client-side at render time**, so a bare table looks clean in the terminal but copies into browser chat at ~3× the tokens. Any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, so the TUI renders it raw/un-painted. Full rationale, the Mermaid/diagram carve-out and `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat" (this bullet is the point-of-use rule; that subsection is the rationale authority).
 <!-- methodology:end id=conventions-output-formatting -->
 
 ## 5. Critical rules
@@ -94,7 +93,7 @@ In order, read:
 5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md`, deleted 2026-05-23 (ADR-38 A5), was **RECREATED 2026-08-29**: ADR-114 supersedes A5 in that one respect, making `README.md` a sanctioned Tier-1 file and this repo's canonical front door. `VISION.md` is retained, marked superseded and still tracked — the fleet-wide filename migration is a sequenced program, not a consequence of this line ([#614]).
 > **[HUB - methodology]** region `critical-rules-consistency` - single-sourced from the hub; do not edit these lines here.
 <!-- methodology:start id=critical-rules-consistency owner=hub -->
-6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
+6. **Keep files consistent** — a hub region's body in `CLAUDE.md` stays byte-identical to its `templates/claude-regions/*.md` source; divergence breaks deploy parity
 <!-- methodology:end id=critical-rules-consistency -->
 7. **Executable rules live in `~/.claude/` with `verify:` lines** — the fleet-wide home (ADR-54); this repo authors no new rule class outside it. **Carve-out:** `.claude/rules/` IS a live repo-local rule home — `git-discipline.md` carries three `verify:` lines plus two standing operator orders (MERGE IS ATOMIC; WORKTREE TEARDOWN IS TWO BRANCHES).
 8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + the JOURNAL `Changes:` line replace CHANGELOG
@@ -199,7 +198,7 @@ What the deploy tool ships to a consumer, generated from `deploy/manifest-v*.yam
 - **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record (a *byte-identical* chronological relocation of an older block into `LESSONS-legacy-<span>.md` is NOT an edit — the ADR-29 2026-07-17 archival exception; any content change still is)
 - **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
 - **Copying `CLAUDE.md` wholesale into `AGENTS.md`** — ADR-115 admits `AGENTS.md` as the portable instruction layer, superseding ADR-53 Decision 2; a wholesale copy measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently — carry the portable half only, and leave the Claude-runtime remainder in `CLAUDE.md`
-- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
+- **Duplicating content between files** — a hub region restated by hand instead of relocated, or PLAYBOOK detail copied verbatim elsewhere; drift is the failure mode
 - **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
 - **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
 <!-- methodology:end id=antipatterns-universal -->
@@ -225,6 +224,8 @@ Machine-enumerated, last 5 by number (`gen_claude_rosters.py --write`). Editoria
 
 - v2.70 (2026-09-01, night window) — §9 gains `audit-title-gate`. The hook was live and unclaimed: 21 named here against 22 in `.pre-commit-config.yaml`, a divergence only the ship-tier `doc_claims` would have seen. Re-read end-to-end at the same commit — every §4/§5 rule was exercised by that window's own work, so the stamp is a review, not a touch.
 
+- v2.71 (2026-09-01, batch-e-b-2 `lane-b-3-claude-md-genre`) — **ESSENTIALS dissolved, CLAUDE.md's genre purified.** `protocols/ESSENTIALS.md` archived (git history) — ~95% pointers back to PLAYBOOK already; its one section with no home elsewhere, "How Claude thinks", relocated to PLAYBOOK Ch8. Five stale "ESSENTIALS summarizes PLAYBOOK" clauses removed or repurposed to the still-true hub-region↔template byte-match concern (header, §1, §5, §10). The branch-prefix enum and TUI output-formatting rationale (§4) shrank to point-of-use bullets; full provenance moved to PLAYBOOK Ch3 / §8. Both `ObsidianVault/` mixing-advisory clauses deleted per ruling CUT-2 (§2, §4). VISION.md dropped from §2/§4 (DC-1 merged). 24,387 B → 23,257 B. Owed: the floor template's `.sha256` sidecar is now stale (regenerate at next deploy); VISION.md:46 / README.md still cite the dissolved `ESSENTIALS.md "How Claude thinks"` (both out of this lane's write-scope).
+
 <!-- methodology:end id=section-history -->
 
 ---
diff --git a/protocols/PLAYBOOK.md b/protocols/PLAYBOOK.md
index 1e1ee8f2..79dc30d3 100644
--- a/protocols/PLAYBOOK.md
+++ b/protocols/PLAYBOOK.md
@@ -39,6 +39,7 @@ reconciled_with: handoff-process@6.3.0
   - [Default branch — `main`](#default-branch--main)
   - [File naming conventions](#file-naming-conventions)
   - [Commit message standard](#commit-message-standard)
+  - [Branch prefixes — the closed enum](#branch-prefixes--the-closed-enum)
   - [Folder structure](#folder-structure)
   - [Root hygiene convention](#root-hygiene-convention)
   - [Additional root hygiene rules (added 2026-05-24, root hygiene pass 2)](#additional-root-hygiene-rules-added-2026-05-24-root-hygiene-pass-2)
@@ -188,6 +189,7 @@ reconciled_with: handoff-process@6.3.0
   - [What the v5 handoff carries](#what-the-v5-handoff-carries)
   - [How to hand off — which mode, what to type (operator runbook)](#how-to-hand-off--which-mode-what-to-type-operator-runbook)
   - [Roles](#roles)
+  - [How Claude thinks (analytical work)](#how-claude-thinks-analytical-work)
   - [Architect epistemic discipline: explicit verification markers](#architect-epistemic-discipline-explicit-verification-markers)
   - [Architect epistemic discipline: completion claims require state verification](#architect-epistemic-discipline-completion-claims-require-state-verification)
   - [Architect routing for technical proposals](#architect-routing-for-technical-proposals)
@@ -326,7 +328,7 @@ Section 13 "Where Knowledge Lives" describes knowledge **domains** (what lives w
 ### Authority hierarchy
 <!-- scope: meta -->
 
-1. `.dev-knowledge/protocols/ESSENTIALS.md` + `protocols/PLAYBOOK.md` (this file) — universal rules across all Rob's work
+1. `.dev-knowledge/protocols/PLAYBOOK.md` (this file) — universal rules across all Rob's work
 2. `{repo}/CLAUDE.md` — per-repo agent-instruction contract (architecture, conventions, tools, ADRs, anti-patterns)
 3. `{repo}/.claude/skills/`, `commands/`, `hooks/` — runtime config
 
@@ -659,7 +661,7 @@ axis.)
 ### Commit message standard
 <!-- scope: dev -->
 
-Git history IS the changelog (no CHANGELOG.md since 2026-05-16) — commit messages carry the load CHANGELOG used to. (Moved from ESSENTIALS 2026-07-05, [#258] — ESSENTIALS keeps the pointer.)
+Git history IS the changelog (no CHANGELOG.md since 2026-05-16) — commit messages carry the load CHANGELOG used to. (Moved from ESSENTIALS 2026-07-05, [#258]; ESSENTIALS itself dissolved 2026-09-01, [#614] batch-e-b-2 — this is now the sole home.)
 
 - **Conventional Commits.** `type(scope): summary` — types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Scope is optional but use the file/folder slug when it clarifies.
 - **Summary line.** Imperative mood, specific, describes WHAT changed. Under ~72 chars. **Never** "wip", "fix", "updates", "stuff", "various changes".
@@ -668,6 +670,26 @@ Git history IS the changelog (no CHANGELOG.md since 2026-05-16) — commit messa
 
 `/save` follows this standard. See CONTRIBUTING.md for live examples and the pre-commit hook list.
 
+### Branch prefixes — the closed enum
+<!-- scope: dev -->
+
+Branch prefixes are a closed enum, not free text. Four are author-chosen: `feat/ fix/ docs/
+chore/`. Four more are machine-produced lane prefixes, each admitted by a recorded ruling
+rather than invented in passing: `worktree-<name>` (native parallel-session worktrees,
+`claude --worktree` / EnterWorktree), `epic/<slug>` (root-provisioned epic lanes, Ch8 "Tree
+orchestration"), `claude/<slug>` (Anthropic cloud-session lanes), and `automation/<slug>`
+(organ-produced replication lanes — admitted 2026-08-06 by architect ruling, registered
+`protocols/STANDING_RULINGS.md` B5).
+
+Lane branches are never self-merged and never author-invented — a brief that names a lane
+branch names it in one of these eight shapes. A new machine-produced lane prefix enters the
+enum only via a recorded ruling, never silently; the enum itself is the checkable surface
+(`scripts/validate_branch_naming.py`, batch-freeze predicate 5's `LANE_BRANCH_RE` import).
+
+Canonical rule, point-of-use: **CLAUDE.md §4 "Commits & branches"** — that bullet keeps the
+enum's literal values; this subsection is the provenance. (Moved from CLAUDE.md 2026-09-01,
+[#614] batch-e-b-2.)
+
 ### Folder structure
 <!-- scope: meta -->
 
@@ -739,7 +761,7 @@ Standardize location of `.secrets/` (today: a single absolute path under the ope
 
 **[TBD — Stream C session 3, ADR-34]**
 
-File and folder casing rules. Currently mixed: `LESSONS.md` ALLCAPS, `docs/` lowercase, `ESSENTIALS.md` ALLCAPS, kebab-case for dated files. Decision on what casing applies where, and whether existing files migrate.
+File and folder casing rules. Currently mixed: `LESSONS.md` ALLCAPS, `docs/` lowercase, `CLAUDE.md` ALLCAPS, kebab-case for dated files. Decision on what casing applies where, and whether existing files migrate.
 
 ### Rule-ID naming convention (doc to code edge)
 <!-- scope: meta -->
@@ -749,7 +771,7 @@ How an enforced rule is named so the `doc_code_edge` advisory check (ADR-89 OQ1)
 - **Form:** `<domain>-<slug>` — lowercase kebab, charset `[A-Za-z0-9_.-]+`, **semantic not numeric** (the ID reads as *what the rule governs*, not an opaque counter). Doc side: `<!-- rule: <domain>-<slug> -->`; code side: `# rule: <domain>-<slug>` (a real comment token, never inside a string). The ID is the identity on both sides, so the edge is **move-safe** — the resolver re-finds the code token by content; moving the file does not fire `broken_edge`.
 - **`<domain>` = a cited theme/source, NEVER a location.** The allowed tokens each cite an existing source (a BACKLOG serialize-group / theme / ADR domain): `seal`, `coherence`, `canonical`, `governance`, `handoff`, `dep`, `tooling`. **Extend by cited append** — add a token that cites a source; "do not invent domains" means "cite a source," not "never add one" (no ADR rewrite to extend).
 - **Only a rule with live code enforcement gets an ID** (the edge presupposes a code site). **IDs are unique and never reused** after retirement — a retired ID stays burned, like a departed BACKLOG id.
-- **Declare at the authoritative source, never in a summary.** The doc-side token lives where the rule is *authoritatively declared*, never on a doc that merely *summarizes* it (e.g. `seal-journal-anchor` is declared in `DEFINITION_OF_DONE.md` — ADR-85's single-source — not in the ESSENTIALS summary of it). The scanned declaration docs are an include-list registry, `ecosystem/doc-code-edge.yaml` (`declaration_docs:`); a doc joins it when it first authoritatively declares an enforced rule (the same cited-append extensibility as the domain namespace).
+- **Declare at the authoritative source, never in a summary.** The doc-side token lives where the rule is *authoritatively declared*, never on a doc that merely *summarizes* it (e.g. `seal-journal-anchor` is declared in `DEFINITION_OF_DONE.md` — ADR-85's single-source — not in a summary of it elsewhere). The scanned declaration docs are an include-list registry, `ecosystem/doc-code-edge.yaml` (`declaration_docs:`); a doc joins it when it first authoritatively declares an enforced rule (the same cited-append extensibility as the domain namespace).
 - **Illustrative vs live (the self-trip guard):** every example token in teaching prose uses the angle-bracket placeholder form `<!-- rule: <domain>-<slug> -->`. `<` / `>` are outside the ID charset, so a placeholder cannot match as a live edge — this section cannot self-trip the scan. Live tokens sit only at a rule's authoritative doc site + its code site.
 
 Full doctrine + reversibility: **ADR-89 OQ1 "NAMING CONVENTION — ADOPTED"**. Advisory-first; a hard-gate promotion is a later data-gated arc.
@@ -770,7 +792,7 @@ Without standard structure, prompts diverge:
 - Different naming for same fields (Model vs LLM, Effort vs Difficulty)
 - Inconsistent COMMIT markers — Claude Code can't tell when to commit
 - Missing UNDERSTAND section → Claude Code makes wrong assumptions
-- Polish prompts → Claude Code outputs Polish (per ESSENTIALS line 25, prompts are English-only)
+- Polish prompts → Claude Code outputs Polish (prompts are English-only)
 - Inline code blocks → can't be saved as artifact, breaks asynchronous workflow
 
 Vibe Code 4 (2026-04-22) established the standard structure during Stream A. This section codifies it as PLAYBOOK protocol.
@@ -811,7 +833,7 @@ Why: pasted-as-text is fine, but file form preserves structure for re-use, audit
 ### Architect → operator channel-discipline (execution actions)
 <!-- scope: meta -->
 
-The browser-chat architect never writes git commands, shell sequences, or executable code inline in chat prose as informational text the operator manually copies. Two channels only, scale-determined (moved from ESSENTIALS 2026-07-05, [#258] — ESSENTIALS keeps the frame + pointer):
+The browser-chat architect never writes git commands, shell sequences, or executable code inline in chat prose as informational text the operator manually copies. Two channels only, scale-determined (moved from ESSENTIALS 2026-07-05, [#258]; ESSENTIALS itself dissolved 2026-09-01, [#614] batch-e-b-2 — this is now the sole home):
 
 - **Scale S** (one command, one mechanical edit, no judgment): PowerShell snippet in a fenced code block; operator copy-pastes and runs as-is.
 - **Scale M+** (multi-step, multi-file, judgment needed, merge ops): Claude Code prompt as a downloadable `.md` file with full structure per this chapter.
@@ -833,7 +855,7 @@ operator-authorized act, granted per-act, not agent judgment.
 
 Before delivering a prompt to Claude Code, verify:
 
-- [ ] **English only** — no Polish in prompt body (Rob speaks Polish; prompts are English per ESSENTIALS)
+- [ ] **English only** — no Polish in prompt body (Rob speaks Polish; prompts are English regardless)
 - [ ] **Model/Mode/Effort table** present at top — embedded **verbatim** from the non-negotiable spec, never paraphrased (#25)
 - [ ] **Absolute paths** for all repo/file references (not relative — Claude Code's CWD varies)
 - [ ] **Read first** lists CLAUDE.md and gotchas (always) plus task-relevant docs
@@ -1192,7 +1214,7 @@ Two related questions: **what does each documentation file do** (Gap #4) and **w
 |------|---------|--------|---------|----------|-------|-------|
 | `README.md` | User-first navigation, what is this repo | Prose + folder layout | When repo state shifts notably | Rob, future contributors | Living (rewrite) | Per-repo |
 | `CLAUDE.md` | Single canonical agent-instruction contract for Claude Code + Codex; per-repo specifics (architecture, conventions, active tools, binding ADRs, anti-patterns) ≤200 lines | 10-section template | When ADRs, tools, architecture, or gotchas change | Claude Code (auto-read), Codex (via project_doc_fallback_filenames) | Living (sections updated) | Per-repo |
-| `ESSENTIALS.md` | Rob's daily cheat sheet, universal | Sectioned, scope-tagged | When Rob's working style evolves | Rob + every browser/Claude Code session | Living (sections updated) | Universal (`.dev-knowledge` only) |
+| `ESSENTIALS.md` | RETIRED 2026-09-01 ([#614] batch-e-b-2) — dissolved into `CLAUDE.md` + the methodology floor (always-on subset) and this file (reference); it was already ~95% pointers back here. Row kept for legacy context | Sectioned, scope-tagged | n/a | — | n/a | Removed |
 | `PLAYBOOK.md` | Universal protocols, this file | Sectioned, scope-tagged, versioned | Per Stream B implementation gaps | Rob + Claude (browser + Code) | Living + section history | Universal (`.dev-knowledge` only) |
 | `JOURNAL.md` | Tactical per-session log | Append-only, dated entries: Did/Failed/Next | Every Claude Code session | Future Claude Code (last 5 entries on startup) | Newest-first prepend | Per-repo (optional; kept when a repo benefits from a per-session log) |
 | `CHANGELOG.md` | RETIRED ecosystem-wide (ADR-49) — git history + JOURNAL `Changes:` line replace it; row kept for legacy context | Newest-first dated entries | n/a | — | n/a | Removed |
@@ -1222,7 +1244,7 @@ File presence is no longer gated per tier (repo-tier system deprecated 2026-05-2
 | `docs/decisions/`, `docs/audits/`, `docs/archive/` | universal under the 2026-05-27 ADR-60 amendment (see taxonomy above) |
 | `docs/handoffs/` | `.dev-knowledge` only (canonical home for handoff bundles) |
 | `docs/diagrams/` | child code repos, where architecture diagrams exist |
-| `ESSENTIALS.md`, `PLAYBOOK.md`, `LESSONS.md`, `logs/TOKEN-LOG.md` | n/a per-repo — live in `.dev-knowledge` only |
+| `PLAYBOOK.md`, `LESSONS.md`, `logs/TOKEN-LOG.md` | n/a per-repo — live in `.dev-knowledge` only |
 
 Optional files are added by judgment of repo complexity; no tier makes them mandatory.
 
@@ -1230,7 +1252,7 @@ Optional files are added by judgment of repo complexity; no tier makes them mand
 <!-- scope: meta -->
 <!-- rule: canonical-freshness -->
 
-The living docs `VISION / ARCHITECTURE / CLAUDE / CONTRIBUTING / ESSENTIALS` carry a `last_reviewed` frontmatter date. **`last_reviewed` means "re-read end-to-end and confirmed accurate (or the drift filed)" on that date — NOT merely "touched".** Bump it only after a genuine review, never reflexively.
+The living docs `VISION / ARCHITECTURE / CLAUDE / CONTRIBUTING` carry a `last_reviewed` frontmatter date. **`last_reviewed` means "re-read end-to-end and confirmed accurate (or the drift filed)" on that date — NOT merely "touched".** Bump it only after a genuine review, never reflexively.
 
 `scripts/audit.py` check #10 (`canonical_freshness`, in `ALL_CHECKS` → runs in `audit health` and `audit run`) enforces two signals:
 
@@ -1377,7 +1399,7 @@ Per Token-LOG flip 2026-04-24:
 
 - **Newest-first (prepend):** TOKEN-LOG, JOURNAL (CHANGELOG retired — §14). Rationale: logs optimize for current-state scanning. (JOURNAL flipped 2026-04-27 — original Stream B Gap #4 spec had oldest-top; amended for consistency with TOKEN-LOG/CHANGELOG.) **JOURNAL write cadence — the unit is the shipped merge** (operator ruling 2026-08-03): one entry per merged-and-pushed unit, not per session and not per commit. Mid-arc churn *within* one unit is the anti-pattern; a wrap-only entry across a multi-merge session is the opposite error and leaves shipped commits unanchored. Full statement and both failure modes: LESSONS 2026-08-03 "journal at wrap, not mid-arc".
 - **Append-only, newest-first (prepend):** LESSONS — new entries at the top of the Entries section, per the file's own header and ADR-29. Rationale: append-only preserves "what we learned when"; newest-first optimizes the scan, same as the logs above. (Corrected 2026-07-30 — this line read "oldest top" until the intake #18 A10 / RM-1 sweep, which fixed `HANDOFF_PROCESS.md` §15 and missed this sibling; the file itself has been newest-first throughout.)
-- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK, ESSENTIALS, ENVIRONMENT. Rationale: not logs; current state matters more than history.
+- **Living (in-place updates):** README, CLAUDE.md, PLAYBOOK, ENVIRONMENT. Rationale: not logs; current state matters more than history.
 - **Immutable (dated):** ADRs, transcripts, handoffs, audits, research. Rationale: point-in-time records; supersession via new file or in-file marker.
 
 **Generator determinism is a property of the input set, not of the code.** A generator that walks the filesystem rather than the *tracked* set emits different bytes per checkout, so its regen-and-diff gate is armed everywhere and satisfiable only on the machine that last regenerated — it stops describing committed state, which is the thing it claims to check. Three instances, one of them live and unfixed when this was written: an untracked `.claude/commands/*.md` rendered as a row in the organ index; `--probe-user-level` reporting four present session hooks as *"declared but absent"* because it inventoried files; and `scripts/gen_audit_index.py:57` reading `audits_dir.glob("*.md")` unfiltered, where a sibling session's untracked audit rendered as an index row and moved the count 487 → 489. The repair that generalizes: route every collector through `git ls-files`, pinned by a test that builds a real git repo containing an untracked file of the collected type.
@@ -1506,7 +1528,7 @@ While useful for some context, this stacked 4 layers of meta-work before any gap
 When opening a new session that continues prior work:
 
 **Browser chat resumption:**
-1. Upload `ESSENTIALS.md` (always)
+1. Upload `CLAUDE.md` (always) — carries the always-on subset ESSENTIALS used to, before its 2026-09-01 dissolution ([#614])
 2. Upload most recent `docs/handoffs/*.md` (if any)
 3. Upload PLAYBOOK.md (if doing dev work — large file, but contains all protocols)
 4. Upload task-specific docs (specific ADRs, Stream B mapping if continuing Stream B, etc.)
@@ -3562,7 +3584,7 @@ This section defines the lifecycle: from "I saw something on Twitter" to "we ado
 ### Project-evolution posture (always be improving)
 <!-- scope: meta -->
 
-Distinct from the tool-adoption lifecycle below: the default posture for every project. (Moved from ESSENTIALS 2026-07-05, [#258] — ESSENTIALS keeps the one-liner + pointer.)
+Distinct from the tool-adoption lifecycle below: the default posture for every project. (Moved from ESSENTIALS 2026-07-05, [#258]; ESSENTIALS itself dissolved 2026-09-01, [#614] batch-e-b-2 — this is now the sole home.)
 
 - Project goal at meta level is continuous development and refinement; specific session goals are immediate scope, the long-term posture is always advancing.
 - Static maintenance is the exception and requires explicit declaration in VISION Lifecycle (e.g., archived project, frozen for compliance).
@@ -4919,7 +4941,7 @@ contract, branch `epic/278-test-suite-hygiene`), `PROBES.md`, and `EPIC_RETURN.m
 ### Roles
 <!-- scope: meta -->
 
-Canonical: the architect↔CC **division** is the equilibrium table in **"The two lifelines" § Lifeline 1** (ADR-87); the v5 actor table / browser operating role are `protocols/HANDOFF_PROCESS.md` §1 / §7. The fuller **Does/Does-NOT** lists + three-layer flow (ADR-28) live below — moved from ESSENTIALS 2026-07-05 ([#258]); ESSENTIALS keeps the day-to-day frame + pointer.
+Canonical: the architect↔CC **division** is the equilibrium table in **"The two lifelines" § Lifeline 1** (ADR-87); the v5 actor table / browser operating role are `protocols/HANDOFF_PROCESS.md` §1 / §7. The fuller **Does/Does-NOT** lists + three-layer flow (ADR-28) live below — moved from ESSENTIALS 2026-07-05 ([#258]); ESSENTIALS itself dissolved 2026-09-01, [#614] batch-e-b-2, so this is now the sole home.
 
 Two distinct LLM contexts collaborate on every workstream. Mixing them = chaos.
 
@@ -4967,6 +4989,23 @@ Browser chat (analysis)  →  .dev-knowledge (reference)  →  projects (executi
 
 **When in doubt about which role applies:** "Should we...?" → browser (decision) · "Implement X per spec" → Claude Code (execution) · "What did we decide about Y?" → either, but check `.dev-knowledge` first.
 
+### How Claude thinks (analytical work)
+<!-- scope: llm -->
+
+Applies primarily to browser-chat analytical work; also relevant whenever Claude Code is asked to reason rather than execute deterministically. (Moved from ESSENTIALS 2026-09-01, [#614] batch-e-b-2 — ESSENTIALS dissolved; this was its one section with no canonical home elsewhere, per `docs/audits/2026-08-27-technical-doc-diet-plan.md`. VISION.md and README.md still cite `protocols/ESSENTIALS.md "How Claude thinks"`; both are out of this lane's write-scope — the pointer is stale until a lane touching them re-points here.)
+
+**Does:**
+- Thinks deeply before responding — extended thinking, multiple hypotheses, "what am I missing" check, self-critique before presenting analysis
+- Verifies factual claims against uploaded documents / current PLAYBOOK / source-of-truth before stating them; does not pattern-match to plausible-sounding answers
+- Pushes back on Rob's premises when warranted, including when Rob's framing leads to a suboptimal answer or when Rob's preferences contain an internal contradiction
+- Thinks architecturally first (highest scope, then zoom), not tactically; when asked about a specific item, first checks "is this a symptom of a bigger architectural question?"
+
+**Does NOT:**
+- Pattern-match to fast plausible answers without self-critique
+- Interpret user preferences in their easiest reading without checking intent
+- Default to validation when contradiction is the more useful response — concession without verification is sycophancy disguised as agreeableness
+- Conflate concepts that share vocabulary but address different concerns (e.g., handoff INSTANCES vs handoff INTELLIGENCE; scope tags `dev | llm | hybrid | runtime | meta` vs invented ones like `process`)
+
 ### Architect epistemic discipline: explicit verification markers
 <!-- scope: meta -->
 
@@ -5065,7 +5104,7 @@ Canonical rule: **CLAUDE.md §4 "Output formatting (render-layer)"**. This subse
 5. Quick project health check (test suite, lint, stale branches)
 6. Update ENVIRONMENT.md if any config changed
 
-(The retired self-evolution step was dropped 2026-06-19; corrections now auto-promote via the `corrections.jsonl` Stop hook — see ESSENTIALS "Feedback Loop".)
+(The retired self-evolution step was dropped 2026-06-19; corrections now auto-promote via the `corrections.jsonl` Stop hook.)
 
 ---
 
diff --git a/templates/child-methodology-floor.md.tmpl b/templates/child-methodology-floor.md.tmpl
index a98a9785..2ecb2a53 100644
--- a/templates/child-methodology-floor.md.tmpl
+++ b/templates/child-methodology-floor.md.tmpl
@@ -38,4 +38,4 @@ Before any **structural** change (architecture, governance, a multi-file refacto
 
 ## Depth escape-hatches (optional — not required for a normal session)
 - This repo's own `CLAUDE.md`, `VISION.md`, `ARCHITECTURE.md` — repo-specific authority.
-- The methodology hub (`.dev-knowledge`) — full protocols (PLAYBOOK / ESSENTIALS). Depth only; this floor is self-sufficient for a normal session.
+- The methodology hub (`.dev-knowledge`) — full protocols (PLAYBOOK). Depth only; this floor is self-sufficient for a normal session.
diff --git a/templates/claude-regions/antipatterns-universal.md b/templates/claude-regions/antipatterns-universal.md
index 6f2e5110..a4cb718d 100644
--- a/templates/claude-regions/antipatterns-universal.md
+++ b/templates/claude-regions/antipatterns-universal.md
@@ -2,6 +2,6 @@
 - **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record (a *byte-identical* chronological relocation of an older block into `LESSONS-legacy-<span>.md` is NOT an edit — the ADR-29 2026-07-17 archival exception; any content change still is)
 - **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
 - **Copying `CLAUDE.md` wholesale into `AGENTS.md`** — ADR-115 admits `AGENTS.md` as the portable instruction layer, superseding ADR-53 Decision 2; a wholesale copy measures 43.50 KiB against Codex's 32 KiB `project_doc_max_bytes` cap and truncates silently — carry the portable half only, and leave the Claude-runtime remainder in `CLAUDE.md`
-- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
+- **Duplicating content between files** — a hub region restated by hand instead of relocated, or PLAYBOOK detail copied verbatim elsewhere; drift is the failure mode
 - **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
 - **Running validators with no args** — vacuous pass; always pass `--all` or specific paths
diff --git a/templates/claude-regions/critical-rules-consistency.md b/templates/claude-regions/critical-rules-consistency.md
index b84ae012..0564f98d 100644
--- a/templates/claude-regions/critical-rules-consistency.md
+++ b/templates/claude-regions/critical-rules-consistency.md
@@ -1 +1 @@
-6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
+6. **Keep files consistent** — a hub region's body in `CLAUDE.md` stays byte-identical to its `templates/claude-regions/*.md` source; divergence breaks deploy parity
diff --git a/templates/claude-regions/first-read.md b/templates/claude-regions/first-read.md
index f9323563..bd2d1c03 100644
--- a/templates/claude-regions/first-read.md
+++ b/templates/claude-regions/first-read.md
@@ -1,8 +1,7 @@
 
 In order, read:
 1. This file (you're here)
-2. The hub methodology protocol `ESSENTIALS.md` — Rob's universal working style (read at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer)
-3. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
-4. Last 5 entries of `JOURNAL.md`
+2. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
+3. Last 5 entries of `JOURNAL.md`
 
-`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (ESSENTIALS carries the always-on subset; a consumer never copies PLAYBOOK). If ESSENTIALS — or a PLAYBOOK section a task needs — is unavailable, proceed with the other available first-read sources and flag the gap.
+`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (this file and the methodology floor carry the always-on subset). If a PLAYBOOK section a task needs is unavailable, proceed with the other available first-read sources and flag the gap.
```
