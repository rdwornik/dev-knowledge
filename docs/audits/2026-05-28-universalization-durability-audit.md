---
last_reviewed: 2026-05-28
status: active
owner: Rob
---

# Universalization Durability + Template-Completeness Audit

**Date:** 2026-05-28
**Branch:** `docs/universalization-durability-audit-2026-05-28`
**Repo:** `.dev-knowledge`
**Trigger:** pre-handoff verification — confirm that today's universalization is encoded in template / PLAYBOOK / ESSENTIALS / ADRs / `audit.py` (DURABLE) versus only applied to current state (ONLY-APPLIED).

---

## Scope

Inventory built from JOURNAL entries 2026-05-27 → 2026-05-28 and the audits under `docs/audits/2026-05-27-*.md` + `docs/audits/2026-05-28-*.md`:

| # | Convention | Origin session(s) |
|---|---|---|
| 1 | Universal visual pattern (dot-prefix configs, ALL-CAPS canonical roots, workspace sort settings) | ADR-59 codification 2026-05-27 |
| 2 | `docs/` folder taxonomy + 2026-05-27 amendment (two-variant: `.dev-knowledge` vs child code repos) | ADR-60 codification 2026-05-27 |
| 3 | Mermaid dark-theme directive standard (v2 — base + themeVariables + `color:` on classDefs) | 2026-05-28 mermaid v2 |
| 4 | Git worktree for same-repo parallel CC sessions | ADR-61 codification 2026-05-28 |
| 5 | Ruff lenient config (corp-monorepo only) | ADR-32 — repo-local, pre-today |
| 6 | File placement: entry-scripts under `scripts/`; root-exception configs (`pyproject.toml` / `tach.toml` / `requirements.txt`) | ADR-60 + visual-pattern rollout |
| 7 | Handoff process v3.4 (Stage 1/2/3 + applied-task gate + structured ratification) | ADRs 55–58 + ADR-42 v3.3.3 |
| 8 | AI Council operational runbook (six-stage frame→close lifecycle) | `AI_COUNCIL_PROCESS.md` v1.0 2026-05-28 |
| 9 | Baseline-folder uniformity for child code repos (decisions/+audits/+archive/ always-present) | ADR-60 addendum 2026-05-28 |
| 10 | Process diagrams in `ARCHITECTURE.md` (C1 layer model, C2 workflow, C3 council, C4 handoff) | 2026-05-28 process-diagrams session |
| 11 | `audit.py` check #7 — mermaid theme directive enforcement | 2026-05-28 mermaid check #7 |

---

## Per-convention durability table

For each convention: where it is encoded, whether a new repo or fresh CC session would actually discover it, and whether it is mechanically enforced. **DURABLE** = encoded in a doc that gets read by future repos/sessions AND (ideally) audit-enforced. **PARTIAL** = encoded somewhere but not findable through the canonical reading path. **ONLY-APPLIED** = present in current state but not codified.

| # | Convention | ADR | PLAYBOOK | ESSENTIALS | Template | `audit.py` | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Visual pattern | ADR-59 ✓ + amendment | §"Universal visual pattern" L240–244 ✓ | §"Repo visual pattern (ADR-59)" L261–264 ✓ | workspace-S/M/L templates **STALE** (April 25, no `sortOrderLexicographicOptions: upper`, no `sortOrderReverse: true`) | checks `dot_prefix_discipline` + `canonical_md_visibility` + `workspace_settings` ✓ | **DURABLE** for existing repos via audit + governance docs; **PARTIAL** for new-repo scaffolding (workspace templates would seed a non-conformant workspace) |
| 2 | docs/ folder taxonomy | ADR-60 ✓ + 2026-05-27 amendment + 2026-05-28 addendum | §"docs/ folder taxonomy (per ADR-60 + 2026-05-27 amendment)" L257–287 ✓ | §"docs/ taxonomy (ADR-60)" L268–271 ✓ | n/a — would only need a `docs/` skeleton; child repos seeded via `chore/baseline-template-2026-05-28` branches | no folder-semantics check (P3 in BACKLOG per ADR-60) | **DURABLE** governance-wise; enforcement gap is acknowledged (BACKLOG P3) |
| 3 | Mermaid theme directive v2 | ADR-51 ✓ amendment v2 2026-05-28 | **MISSING** — codemap workflow §L2758+ does not reference the theme-directive requirement | **MISSING** — no ESSENTIALS line for "every new mermaid block needs the directive" | ARCHITECTURE-template ✓ embeds the directive in canonical codemap example | check #7 `mermaid_theme_directive` ✓ enforces it on `ARCHITECTURE.md` + template | **PARTIAL** — DURABLE for `ARCHITECTURE.md` (audit-enforced) but a future hand-authored mermaid block elsewhere (audit.py scope is just ARCHITECTURE.md + template) won't be caught, and PLAYBOOK never tells you to add the directive. **CLOSEABLE GAP — add cross-ref in PLAYBOOK Codemap workflow + ESSENTIALS line.** |
| 4 | Git worktree pattern | ADR-61 ✓ | §"Same repo in parallel: REQUIRES `git worktree`" L797–825 ✓ | §"Parallel sessions" L216–218 ✓ | n/a | n/a (procedural) | **DURABLE** |
| 5 | Ruff lenient (corp-monorepo) | corp-monorepo-local ADR (pre-today, not in scope of today's universalization) | n/a (repo-local) | n/a | n/a | repo-local | **DURABLE** at repo scope |
| 6 | File placement: scripts/ + root-exception configs | ADR-60 ✓ (root-exception list in amendment); ADR-59 ✓ (un-dotted exceptions list) | §"docs/ folder taxonomy" mentions root-exception configs ✓; §"Universal visual pattern" lists dot-prefix exceptions ✓ | §"docs/ taxonomy (ADR-60)" mentions entry-scripts in `scripts/`, root-exception configs ✓ | ARCHITECTURE-template references convention via §"Codemap" `--source-root` examples | `dot_prefix_discipline` check enforces the exception list ✓ | **DURABLE** |
| 7 | Handoff process v3.4 | ADR-42 (v3.3.3) + ADR-55 (applied-task gate) + ADR-56 (prompt card) + ADR-57 (two-layer bundle) + ADR-58 (structured claims verification) ✓ | §"Operational authority: `protocols/HANDOFF_PROCESS.md`" L1915 ✓ + multiple references | §"Browser chat checkpoint: see HANDOFF_PROCESS.md" L328 ✓ | `templates/HANDOFF_FOLDER_TEMPLATE.md` ✓ + `HANDOFF_QUESTION_TEMPLATE.md` ✓ | n/a (procedural) | **DURABLE** — HANDOFF_PROCESS.md owns the runbook, ADRs own the decisions, PLAYBOOK + ESSENTIALS point at the runbook |
| 8 | AI Council process | ADR-43 (transcript routing) + governance ✓ | §5 lead-in L1536 cross-refs `protocols/AI_COUNCIL_PROCESS.md` ✓ | "Council ADR distillation" line L184 cross-refs runbook ✓ | n/a | n/a (procedural) | **DURABLE** |
| 9 | Baseline-folder uniformity (child repos) | ADR-60 addendum 2026-05-28 ✓ | covered by §"docs/ folder taxonomy" amendment + addendum reference | covered by §"docs/ taxonomy (ADR-60)" two-variant line | n/a — child repos seeded by branch (corp-ops + corp-sca branches awaiting merge) | no audit check for baseline-folder presence | **DURABLE** governance; **PARTIAL** enforcement — a future child repo created from scratch (no scaffolding tool) could miss the baseline. Not a closeable cross-ref gap; flagged as judgment item. |
| 10 | Process diagrams (C1–C4) | ADR-51 owns the convention; the four diagrams in `ARCHITECTURE.md` are the instances | n/a — instance-level, not protocol | n/a | ARCHITECTURE-template ✓ includes the diagrams' structure as guidance | check #7 enforces theme directive on them | **DURABLE** in this repo. Child repos do NOT inherit the same four diagrams (they shouldn't — different processes); the convention they DO inherit (mermaid + theme) is item #3. |
| 11 | `audit.py` mermaid check #7 | ADR-51 enforcement note 2026-05-28 ✓ | n/a | n/a | n/a | `check_mermaid_theme_directive` ✓ in `scripts/audit.py` | **DURABLE** for `.dev-knowledge`. Child repos: each carries their own `audit.py`? **JUDGMENT GAP** — read-only audit script lives only in `.dev-knowledge`; child repos do not currently run an analogous check. |

---

## Three durability questions

### 1. New-repo inheritance

**Scenario:** an operator scaffolds a brand-new child code repo. Without manual reference to today's audits, do they inherit the conventions?

| Convention | Inherits if templates/ are used? | What they would miss |
|---|---|---|
| Visual pattern (workspace sort settings) | **NO** — workspace-S/M/L last touched 2026-04-25 (pre-ADR-59). New repo would seed a workspace WITHOUT `explorer.sortOrderLexicographicOptions: upper` or `explorer.sortOrderReverse: true`, and possibly with un-dotted name. | The two sort settings + the dot-prefix workspace filename. The audit would then fail `workspace_settings` on first run — caught only by running `audit.py` in the new repo, which is not standard new-repo onboarding. |
| Visual pattern (dot-prefix configs) | partially — no scaffolding tool; the convention is documented in ADR-59 + PLAYBOOK but not embodied in a "starter pack" | the operator has to read ADR-59 |
| docs/ folder taxonomy | **NO template scaffold** — operator reads ADR-60 + PLAYBOOK and creates folders by hand or copies a child-repo baseline | the variant choice + the seeded READMEs |
| Mermaid theme directive | yes — `ARCHITECTURE-template.md` includes the directive in the canonical codemap example | nothing missing on the template side |
| Worktree | n/a — procedural, lives in operator's PLAYBOOK |  |
| CLAUDE.md content | **NO** — `templates/CLAUDE-md-template.md` was last updated 2026-05-19 (v2.1). It does NOT reference visual pattern, taxonomy, mermaid theme, worktree, HANDOFF_PROCESS, or AI_COUNCIL_PROCESS. A new repo's CLAUDE.md created from this template would be missing 6+ months of conventions. | All of: §3 Architecture (mermaid theme awareness), §4 Conventions (visual pattern + taxonomy), §5 Critical rules (worktree pre-flight), §7 Slash commands (handoff command), references to HANDOFF_PROCESS / AI_COUNCIL_PROCESS. **Largest single durability gap of today's audit.** |
| Handoff / AI Council protocol | DURABLE — protocol docs live in `.dev-knowledge/protocols/`; child repos point at them | n/a |

**Net new-repo inheritance verdict:** **PARTIAL**. ADR-59, ADR-60, and the mermaid-theme convention are governance-DURABLE but new-repo-FRAGILE because the two template assets that actually scaffold a new repo (`templates/CLAUDE-md-template.md` and `templates/workspace-S/M/L.code-workspace`) pre-date today's universalization.

### 2. Fresh-session competence

**Scenario:** a fresh Claude Code session boots in `.dev-knowledge` or a child repo and reads only the canonical chain — CLAUDE.md → ESSENTIALS.md → PLAYBOOK.md → recent JOURNAL — without diving into individual ADRs or audits. Does it know enough to work?

| Question a fresh session would face | Findable in canonical chain? |
|---|---|
| Naming conventions (kebab-case, UPPERCASE living docs, dated artifacts) | yes — CLAUDE.md §4 ✓ |
| docs/ folder taxonomy + which variant applies to this repo | yes — PLAYBOOK §"docs/ folder taxonomy" + ESSENTIALS §"docs/ taxonomy" ✓ |
| Dot-prefix discipline + workspace filename | yes — PLAYBOOK §"Universal visual pattern" + ESSENTIALS §"Repo visual pattern" ✓ |
| When to add `%%{init: {'theme':'base', ...}}%%` to a new mermaid block | **NO** — neither PLAYBOOK §"Codemap workflow" nor ESSENTIALS mention the directive; a fresh session writing a new diagram outside the codemap block would skip it and find out only at `audit.py` run-time | **CLOSEABLE GAP** |
| Parallel sessions / worktree rule | yes — PLAYBOOK §"Session boundaries" + ESSENTIALS §"Parallel sessions" ✓ |
| Handoff trigger + process | yes — PLAYBOOK §"Handoff governance" + ESSENTIALS §"Browser chat checkpoint" both point at HANDOFF_PROCESS.md ✓ |
| AI Council routing + when to debate | yes — PLAYBOOK §5 cross-refs AI_COUNCIL_PROCESS.md ✓ |
| File placement (scripts/, root-exception configs) | yes — PLAYBOOK + ESSENTIALS via taxonomy section ✓ |

**Net fresh-session competence verdict:** **DURABLE except mermaid theme directive.** Single closeable gap (item #3 in the table above).

### 3. Handoff carry

**Scenario:** a handoff is generated per `HANDOFF_PROCESS.md`. The governance floor (Stage 1 packaging) pulls a defined doc set. Does that set actually carry today's conventions?

`HANDOFF_PROCESS.md` Stage 1 pulls: CLAUDE.md + ESSENTIALS + PLAYBOOK + HANDOFF_PROCESS itself + recent ADRs index. Going convention by convention:

| Convention | Lives where? | Carried by handoff? |
|---|---|---|
| 1 Visual pattern | ADR-59 + PLAYBOOK + ESSENTIALS + audit | **YES** (PLAYBOOK + ESSENTIALS in floor; ADR-59 indexed) |
| 2 Taxonomy | ADR-60 + PLAYBOOK + ESSENTIALS | **YES** |
| 3 Mermaid theme v2 | ADR-51 amendment + audit | **PARTIAL** — only ADR carries it; PLAYBOOK/ESSENTIALS silent → handoff bundle carries the ADR but the reader has to know to look (→ closeable by the PLAYBOOK/ESSENTIALS cross-ref below) |
| 4 Worktree | ADR-61 + PLAYBOOK + ESSENTIALS | **YES** |
| 6 File placement | ADRs 59/60 + PLAYBOOK + ESSENTIALS | **YES** |
| 7 Handoff v3.4 | HANDOFF_PROCESS.md itself + ADRs 55-58 | **YES** (self-carrying) |
| 8 AI Council | AI_COUNCIL_PROCESS.md + PLAYBOOK + ESSENTIALS | **YES** |
| 9 Baseline uniformity | ADR-60 addendum + PLAYBOOK taxonomy reference | **YES** (governance) |
| 10 Process diagrams | `ARCHITECTURE.md` itself (in repo) | **YES** (repo-local; readable) |
| 11 Audit check #7 | `scripts/audit.py` + ADR-51 enforcement note | **YES** (script in repo; readable) |

**Conventions that live ONLY in `docs/audits/` (i.e. NOT in CLAUDE/ESSENTIALS/PLAYBOOK/ADR — would be missed by the handoff floor):** none found. Every convention has at least one home in the governance docs that are pulled by the handoff floor.

**Net handoff-carry verdict:** **DURABLE except mermaid theme directive cross-ref** (closeable in this session).

---

## corp-monorepo P1 findings — branch deletion gate

The prompt asks whether the verify findings on `corp-monorepo:verify/codex-p1-findings` are captured in current governance so the branch can be safely deleted. Branch content surveyed: 7 commits, 6 analysis files under `.audit/verify-*`.

| Finding | Severity | Captured in current main? | Where | Gate verdict |
|---|---|---|---|---|
| P1-1: OneDrive overlap deletion (executor.py) | P1 | **YES** | (a) Global `~/.claude/hooks/block-onedrive.ps1` (PreToolUse hook); (b) global `~/.claude/CLAUDE.md` hard exclusion: *"NEVER touch OneDrive - Blue Yonder paths"*; (c) `corp-monorepo/src/corp/cleanup/executor.py` `_guard_onedrive()` already present on main; (d) corp-local `ADR-27` documents the OneDrive guard centralization | safe to delete (multi-layer enforcement) |
| P1-2: Path traversal via `moves.yaml` (executor.py:68/85) | P1 | **NO** | (a) No `Path.is_relative_to(mywork_root)` guard at executor.py:68 or :85 (verified in `verify-p1-2.md` against main); (b) no schema/validator for `moves.yaml` `..` segments; (c) zero traversal-targeted tests in `tests/test_cleanup/test_executor.py`; (d) corp-local ADR-27 covers OneDrive guard only — does **not** address traversal; (e) global OneDrive hook does not block traversal to non-OneDrive paths | **GATE FAIL** — DO NOT delete the verify branch until the analysis is extracted to corp-monorepo `BACKLOG.md` (or an ADR/hotfix). Losing the analysis file would lose the only existing record of the vulnerability scope (call chain, exploit prose, recommended fix scope). |
| P1-3: archive onedrive path | P1 | **YES** | Same multi-layer OneDrive enforcement as P1-1. The path-specific finding is a subset; not separately captured but covered by global guard. | safe (covered) |
| P2: Vault single-writer invariant violation | P2 | **YES** | `corp-monorepo/docs/decisions/ADR-27-safety-invariants.md` Decision 2 narrowed the invariant; `tests/safety/test_vault_writer_invariant.py` enforces it via AST walk + zone whitelist (CI test on main) | safe to delete (governance + mechanical enforcement) |

**Branch-deletion gate verdict:** **HOLD.** The `verify/codex-p1-findings` branch cannot be deleted without first extracting **P1-2** (path traversal) to corp-monorepo `BACKLOG.md` or fixing it. Operator must extract before running `git branch -D verify/codex-p1-findings` (and the parent `feature/dead-code-audit` which contains the same `.audit/verify-p1-2.md` history). Recommended extraction line for corp-monorepo BACKLOG:

> [P1] Path traversal in `src/corp/cleanup/executor.py:68` (and parallel `:85`) — untrusted join `mywork_root / source_rel` accepts `..` segments; `Path.__truediv__` does not normalize, `_guard_onedrive()` only blocks OneDrive prefix. Exploit: approved `moves.yaml` entry with `source: "../../../../etc/passwd"` reaches `source.unlink()` (delete) or `shutil.move()` (overwrite). Fix scope: `source.resolve().is_relative_to(mywork_root)` gating + dataclass schema for moves.yaml entries with validator rejecting `..` + absolute paths at load time. Original analysis: `verify/codex-p1-findings:.audit/verify-p1-2.md`.

---

## Gap list

### CLEAR gaps — closed in this audit (additive cross-refs only)

| # | Gap | Where | Close action |
|---|---|---|---|
| C1 | PLAYBOOK §"Codemap workflow" does not tell a fresh session that every new mermaid block needs the v2 theme directive | `protocols/PLAYBOOK.md` §"Codemap workflow" | add one cross-ref line referencing ADR-51 amendment v2 + audit check #7 |
| C2 | ESSENTIALS has no mermaid line | `protocols/ESSENTIALS.md` | add one cheat-sheet line under existing "Repo visual pattern" or as its own bullet |
| C3 | `.dev-knowledge/CLAUDE.md` §11 "Recent ADRs binding here" lists ADRs 49–53; missing 54–61 | `CLAUDE.md` | rotate to the most-recent 5 (ADRs 57–61) per the file's own "(last 5)" header |

### JUDGMENT gaps — flagged for operator (NOT closed)

These are not safe to close in a docs/cross-ref audit — they require operator decision:

| # | Gap | What it would take to close |
|---|---|---|
| J1 | `templates/CLAUDE-md-template.md` is at v2.1 (2026-05-19) and predates ADRs 54–61. A new repo scaffolded from it would inherit a CLAUDE.md with no visual pattern, no taxonomy, no mermaid theme awareness, no worktree pre-flight, no HANDOFF_PROCESS / AI_COUNCIL_PROCESS references | author v2.2 (or v3.0) of the template — substantive content decision, not a mechanical update |
| J2 | `templates/workspace-S.code-workspace`, `workspace-M.code-workspace`, `workspace-L.code-workspace` last touched 2026-04-25. None include `explorer.sortOrderLexicographicOptions: upper` or `explorer.sortOrderReverse: true` (per ADR-59 + corrected 2026-05-27 amendment) or guidance on the dot-prefixed workspace filename | refresh all three or consolidate into a single `workspace.code-workspace` template — operator decision |
| J3 | No audit check for `docs/` folder semantics (e.g. inputs in `audits/`, outputs in `decisions/`) — ADR-60 enforcement is governance-only. Already-tracked: `BACKLOG.md` P3 entry from 2026-05-27 | extend `audit.py` with a folder-semantics check; pre-existing BACKLOG item |
| J4 | Mermaid theme directive audit check scope is `ARCHITECTURE.md` + `templates/ARCHITECTURE-template.md` only. Hand-authored mermaid blocks added in other files (e.g. future protocols/* diagrams, READMEs) are not enforced | widen the audit scope OR accept the current scope as sufficient — operator decision |
| J5 | Child code repos (corp-monorepo, corp-ops, corp-sca, ai-council) do not run an `audit.py` analogue, so `.dev-knowledge`-side checks (visual pattern + mermaid theme) do not enforce in child repos. Today's branches `chore/baseline-template-2026-05-28` (corp-ops + corp-sca) seed baseline folders but not the audit script | operator decision: (a) port `audit.py` per repo; (b) add a cross-repo `audit.py` runner in `.dev-knowledge`; (c) accept governance-only enforcement for child repos |
| J6 | No canonical "starter pack" or scaffolding tool — a new repo is created by hand, copying conventions ad-hoc. Templates address only ARCHITECTURE / CLAUDE / workspaces; there is no template for `BACKLOG.md` / `JOURNAL.md` / `LESSONS.md` / `docs/decisions/README.md` / `docs/audits/README.md` / `docs/archive/README.md` | operator decision whether to author a child-repo scaffolding template (Layer-2 invariant must remain — read-only validators only, no orchestration) |

---

## Verification

- `git status` clean at audit start; on branch `docs/universalization-durability-audit-2026-05-28` off `main`
- `python scripts/audit.py health` → 7/7 PASS, operational checks green
- `pytest -x --tb=short` deferred to commit verification step
- corp-monorepo working tree confirmed clean after read-only inspection of `verify/codex-p1-findings`

---

## Summary verdict

- **7 of 11** conventions are fully DURABLE (encoded in governance + enforced or self-explanatory)
- **3 of 11** are PARTIAL — mermaid theme directive (closeable here), template scaffolding (judgment), child-repo audit (judgment)
- **0 of 11** are ONLY-APPLIED — every convention has at least one durable home

**Branch-deletion gate (`verify/codex-p1-findings`):** **HOLD** until P1-2 path traversal is extracted to corp-monorepo BACKLOG.

**Operator action items after this audit merges:**
1. Decide J1–J6 (judgment gaps above) — separate sessions, not this audit.
2. Extract P1-2 to corp-monorepo BACKLOG, then `git branch -D verify/codex-p1-findings` + `feature/dead-code-audit`.
3. Resume the queued cross-repo retrofits + first real handoff under v3.4.
