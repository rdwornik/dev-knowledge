---
type: execution-plan
scope: corp-sca-time-automation universalization actions for dedicated corp-sca session
date: 2026-05-26
basis: 2026-05-26-corp-sca-time-automation-audit-refresh.md
status: research artifact (consumed by separate corp-sca-time-automation session)
contract: this plan does NOT execute changes; consumed by corp-sca session per Layer-2 invariant
---

# corp-sca-time-automation Universalization Execution Plan — 2026-05-26

This plan closes the 8 findings in
`2026-05-26-corp-sca-time-automation-audit-refresh.md`. It is **consumed by a
separate corp-sca Claude Code session** with write access to corp-sca; the
`.dev-knowledge` session that produced this plan does not. Every action cites
the finding(s) it closes.

Finding IDs (CS-*) are defined in the audit refresh — read it first.

## Sequencing principle

Like corp-ops, corp-sca is a **creation** job. Ordered: **create the three
mandatory files** (VISION → ARCHITECTURE → BACKLOG), **moving** the architecture
content out of CLAUDE.md into ARCHITECTURE.md (CS-2 + CS-5 coordinate); **then
the `.env.example` + README resolution** (they share the `cp .env.example .env`
reference, so resolve together); **then CHANGELOG retire + optional workspace**.
**Small–medium** session — richer seeds than corp-ops mean faster ARCHITECTURE +
a populated BACKLOG.

## Pre-flight requirements

- corp-sca working tree **clean**, on a feature branch off `main`, HEAD `d6dfb15`
  or later — if corp-sca has moved, re-verify the refresh's citations.
- The corp-sca session has read, from `.dev-knowledge`: `VISION.md`,
  `ARCHITECTURE.md`, `templates/ARCHITECTURE-template.md` (esp. the **text-only
  codemap override** note at `:68`), `corp-monorepo/CLAUDE.md` (ADR-53 reference),
  `protocols/PLAYBOOK.md` §Root hygiene + §VS Code workspace, and
  ADR-33/38-A5/49/51/53.
- corp-sca tests green at start (`python -m pytest`).
- **Operator decisions resolved** (see below) — at minimum the `.env.example`
  resolution (CS-7) and README disposition (CS-6).

## Operator decisions captured (apply uniformly per cross-repo decisions table)

| Decision | Default | corp-sca application |
|---|---|---|
| README disposition | **Delete** | Action 5 — internal; coordinate with the `.env.example` reference it carries. |
| Codemap maintenance | **Hand-authored Mermaid** | Action 2 — but corp-sca is **flat-module**, so use the **text-only codemap override** (prose module overview, no CODEMAP markers, no generator), not a Mermaid graph. |
| `.env.example` | **Remove** | Action 4 — **exception case**: it is referenced (`cp .env.example .env`). Migrate env-var docs into CLAUDE.md + drop the `cp` instruction, *then* remove — OR keep with a noted exception. Operator decides. |
| LESSONS scope-tag backfill | **Defer (optional)** | N/A — corp-sca has no LESSONS.md; creating one is optional. |
| Workspace tier-residue | **Separate `.dev-knowledge` change** | Out of scope; only the optional dot-prefixed workspace add (Action 6). |

---

## Actions (sequenced)

### Action 1 — Create VISION.md
- **What:** Create `corp-sca/VISION.md` from the `.dev-knowledge` VISION shape.
  Frontmatter = `version`, `owner`, `last_reviewed`, `status` (no tier/scale).
  Seed: "Automates weekly time entry submission to SharePoint SCA Time Tracker
  from Outlook calendar exports" (CLAUDE.md). Sections: Vision, Scope,
  Relationships ("Operates under `.dev-knowledge` methodology"; corp-sca is
  "fully standalone" but shares `Project_Codes.xlsm` with corp-opportunity-manager
  per CLAUDE.md "Integration points"), Lifecycle. Keep small-repo-short.
- **Where:** `corp-sca/VISION.md` (new).
- **Why:** CS-1 [HIGH] (ADR-38 A5 / ADR-33; clears `vision_md` FAIL).
- **Verification:** from `.dev-knowledge` `python scripts/audit.py repo
  corp-sca-time-automation` → `vision_md` PASS; frontmatter keys ==
  `{version, owner, last_reviewed, status}`.
- **Dependencies:** none. **Do first.**
- **Commit suggestion:** `docs: add VISION.md (ADR-33 / ADR-38 A5 universalization)`.

### Action 2 — Create ARCHITECTURE.md (text-only codemap) by moving CLAUDE.md content
- **What:** Create `corp-sca/ARCHITECTURE.md` from
  `templates/ARCHITECTURE-template.md`. Frontmatter `last_reviewed`/`status`/`owner`.
  Complete the three CORE sections by **moving** the architecture content
  currently inline in CLAUDE.md: **Purpose** (time-entry automation); **Codemap** —
  use the **text-only override** (a prose module overview listing the flat `src/`
  modules and their roles; **no** CODEMAP markers, **no** generator — corp-sca's
  flat layout has no package graph worth a Mermaid diagram); **Layer Boundaries &
  Invariants** — name the pipeline stages (loader → mapper → overlap → aggregator
  → gap_filler → excel_writer → sharepoint) and state invariants (e.g. "highest
  priority wins per hour slot", "gap_filler fills to 40h", "sharepoint upload is
  idempotent per week"). Add **Data Flow** (the CLAUDE.md data-flow block) and a
  **Module Map** (the CLAUDE.md "Key modules" table — ~16 modules).
- **Where:** `corp-sca/ARCHITECTURE.md` (new); content sourced from
  `corp-sca/CLAUDE.md` `## Architecture` section.
- **Why:** CS-2 [HIGH] (ADR-51 universal). The text-only override is explicitly
  permitted for repos too small/flat for a meaningful package graph
  (`templates/ARCHITECTURE-template.md:68`).
- **Verification:** `adr38_baseline` advances; three CORE sections present; codemap
  is the prose override (no orphaned empty CODEMAP markers).
- **Dependencies:** Action 1. Coordinates with Action 3 (CLAUDE re-home removes
  the now-migrated architecture section).
- **Commit suggestion:** `docs: add ARCHITECTURE.md (text-only codemap; content from CLAUDE.md) (ADR-51)`.

### Action 3 — Create BACKLOG.md (populated from CLAUDE.md "Known issues")
- **What:** Create `corp-sca/BACKLOG.md` from the `.dev-knowledge` BACKLOG shape
  (header citing "ADR-41 as relaxed by ADR-47"). **Populate** it from the CLAUDE.md
  "Known issues" list — each becomes an entry (`### [P{N}] [open] <title>` +
  What/Why/Added/Status): dead `models.py` TypedDicts, duplicated
  `NO_OPPORTUNITY_ID_CATEGORIES` + `CATEGORY_MAP`, misnamed `aggregate_entries()`,
  thin pytest coverage, deprecated `detect_client_from_comment()`, unverified
  `split_multiday_events()`.
- **Where:** `corp-sca/BACKLOG.md` (new).
- **Why:** CS-3 [HIGH] (ADR-41 / ADR-38 A5; clears the rest of `adr38_baseline`
  FAIL). Bonus: relocates tech-debt from a prose CLAUDE.md list into the tracked
  BACKLOG where it belongs (remove the duplicate from CLAUDE.md in Action… —
  optional; keep a short pointer).
- **Verification:** `adr38_baseline` PASS; header cites ADR-47; entries trace the
  Known-issues items.
- **Dependencies:** none (do in the same arc). If pruning the CLAUDE.md
  "Known issues" duplicate, coordinate with Action … (CLAUDE re-home).
- **Commit suggestion:** `docs: add BACKLOG.md populated from Known-issues (ADR-41 / ADR-47)`.

### Action 4 — Re-home CLAUDE.md into the ADR-53 template
- **What:** Restructure `corp-sca/CLAUDE.md` into the 12-section canonical form
  (reference `corp-monorepo/CLAUDE.md`). Add §1 session-start "Read first" order
  (this file → VISION → ARCHITECTURE → recent commits). **Remove** the `##
  Architecture` section (moved to ARCHITECTURE.md in Action 2 — replace with a §3
  pointer) and optionally the "Known issues" list (moved to BACKLOG.md in Action
  3 — replace with a pointer). **Preserve** quick-start, API-keys, dev-standards,
  key-commands, integration-points. **Handle the `.env.example` reference at
  `:15`** as part of Action 5's `.env.example` resolution.
- **Where:** `corp-sca/CLAUDE.md` (restructure).
- **Why:** CS-5 [MEDIUM] (ADR-53 canonical form).
- **Verification:** CLAUDE.md follows the template; §1 read order resolves; no
  embedded `## Architecture` (now a pointer); `check_claude_md` PASS.
- **Dependencies:** Actions 1–3 (so pointers target real files).
- **Commit suggestion:** `docs: re-home CLAUDE.md into ADR-53 template; move architecture to ARCHITECTURE.md`.

### Action 5 — `.env.example` + README resolution (coordinated)
- **What:** These share the `cp .env.example .env` reference, so resolve together.
  (a) **`.env.example` (CS-7):** migrate the required env-var names
  (`ONEDRIVE_PATH`, `GRAPH_ACCESS_TOKEN`, `GEMINI_API_KEY`, Azure IDs) into
  CLAUDE.md (e.g. a §setup/env note), drop the `cp .env.example .env` instruction
  from CLAUDE.md:15, then `git rm .env.example` — **OR** keep `.env.example` with
  a noted exception if the operator prefers (PLAYBOOK:227 allows the contributor-
  reliance exception). (b) **README (CS-6):** `git rm corp-sca/README.md` (internal;
  duplicates CLAUDE + the new VISION). The README's `:31` `cp .env.example .env`
  reference dies with the file.
- **Where:** `corp-sca/.env.example` (rm or keep-with-note), `corp-sca/CLAUDE.md:15`
  (drop `cp` instruction if removing), `corp-sca/README.md` (`git rm`).
- **Why:** CS-7 [LOW] (`.env.example` exception case) + CS-6 [MEDIUM] (README
  deprecated).
- **Verification:** if removing `.env.example`, `git -C corp-sca ls-files | grep
  env.example` → nothing and no `cp .env.example` instruction remains anywhere
  (`grep -rn "env.example" corp-sca/` → nothing); README absent; env-var names
  documented in CLAUDE.md.
- **Dependencies:** Action 4 (CLAUDE.md is being re-homed anyway — fold the `:15`
  edit into that pass to avoid stale line numbers). Verify env-var docs landed in
  CLAUDE before deleting `.env.example` ("verify destination before drop").
- **Commit suggestion:** `chore: resolve .env.example (migrate env docs); delete README (ADR-38 A5)`.

### Action 6 (optional) — CHANGELOG retire + dot-prefixed workspace
- **What:** (a) **CS-4:** retire `CHANGELOG.md` (`git rm`). Pair with a minimal
  `JOURNAL.md` (repo-specific, optional) or accept git history as the sole record
  (ADR-49). corp-sca already has `docs/handoffs/` — a JOURNAL is a reasonable add
  given the repo keeps session docs. **Operator decides.** (b) **CS-8:**
  optionally add `.corp-sca-time-automation.code-workspace` (dot-prefixed);
  lower-value since `.vscode/` already exists.
- **Where:** `corp-sca/CHANGELOG.md` (`git rm`); optional `corp-sca/JOURNAL.md`;
  optional `.corp-sca-time-automation.code-workspace`.
- **Why:** CS-4 [MEDIUM] (CHANGELOG retire) + CS-8 [LOW] (workspace, optional).
- **Verification:** no `CHANGELOG.md`; workspace (if added) dot-prefixed.
- **Dependencies:** none.
- **Commit suggestion:** `chore: retire CHANGELOG (ADR-49); optional workspace + JOURNAL`.

---

## Verification gates (between phases)

- **After Actions 1–3 (governance scaffold):** from `.dev-knowledge`
  `python scripts/audit.py repo corp-sca-time-automation` → all 3 checks PASS (the
  two hard FAILs cleared). corp-sca tests still green.
- **After Action 4 (CLAUDE re-home):** CLAUDE.md template-form; §1 read order
  resolves; no embedded `## Architecture`.
- **Whole-plan exit:** corp-sca `git status` clean; `python -m pytest` green;
  `python -m ruff check src/` clean; no `README.md`, no `CHANGELOG.md`;
  `.env.example` resolved (removed-with-migrated-docs or kept-with-note);
  VISION/ARCHITECTURE/BACKLOG present.

## Risk register

- **`.env.example` reliance (Action 5a).** Unlike corp-ops, corp-sca *uses*
  `.env.example`. Do **not** blind-`git rm` it — first migrate the env-var names
  into CLAUDE.md and drop both `cp .env.example .env` references
  (`CLAUDE.md:15` + `README.md:31`), or keep it with a noted exception. A silent
  removal breaks the documented setup flow.
- **Architecture content move (Actions 2 + 4).** The architecture content moving
  out of CLAUDE.md into ARCHITECTURE.md must not be lost or duplicated — move,
  don't copy-and-leave. Verify the CLAUDE.md `## Architecture` section becomes a
  pointer, not a stale duplicate.
- **Text-only codemap, not Mermaid.** corp-sca's flat `src/` has no package graph
  — use the text-only override. Do not author empty CODEMAP markers (they would
  fail a future generator check and imply a graph that doesn't exist).
- **CHANGELOG→JOURNAL gap (Action 6a).** As with corp-ops, confirm the operator
  accepts git history as the record if no JOURNAL is added.
- **No pyproject.toml.** corp-sca runs on `requirements.txt`; do **not** create a
  pyproject just to consolidate config (out of scope, and it would add a root file).

## What this plan does NOT include

- **Migrating corp-sca to `pyproject.toml`** (code-project decision, out of scope).
- **ADR-42 handoff-format migration** of `docs/handoffs/` (handoff-process concern,
  separate from universalization).
- **Internal code-correctness fixes** for the "Known issues" items — those become
  BACKLOG entries (Action 3), not fixes in this session.
- **Methodology codification** — `.dev-knowledge` standards work.
- **Cross-repo modifications** outside corp-sca.
- **A proceed/no-proceed recommendation** — the operator decides after reading.

## Estimated execution scope

- **Required actions:** 5 (Actions 1–5). **Optional:** Action 6 (CHANGELOG retire
  is required; the JOURNAL + workspace pairing is optional).
- **Estimated commits:** 6–8.
- **Estimated session size:** **small–medium.** Richer seeds than corp-ops
  (architecture + Known-issues already drafted) speed ARCHITECTURE + BACKLOG; the
  `.env.example` migration is the one fiddly step. No source-code changes.
- **Findings closed at completion:** all 8 (CS-8 optional).

## Operator decisions required before execution

1. **`.env.example` resolution (Action 5a).** Migrate env docs + remove, or keep
   with a noted exception? (corp-sca *uses* it — this is the exception case.)
2. **README disposition (Action 5b).** Delete (default) or keep?
3. **CHANGELOG → JOURNAL (Action 6a).** Add a JOURNAL.md (corp-sca keeps
   `docs/handoffs/`, so plausible) or accept git history as the sole record?
4. **VISION `status` value (Action 1).** `active` expected — confirm.

## Lessons forward / back

- **Same creation shape as corp-ops** — Actions 1→4 mirror corp-ops Actions 1→4.
  Run corp-ops first (cleaner `.env.example`, graphical codemap) to validate the
  creation sequence, then apply to corp-sca with the two adaptations (text-only
  codemap + `.env.example` migration).
- **Richer CLAUDE.md = faster scaffold** — corp-sca's inline architecture + Known-
  issues mean ARCHITECTURE and BACKLOG are largely a move/re-home, not authoring
  from scratch.

---

**Contract preserved:** this plan executes nothing; it is consumed by a separate
corp-sca-time-automation session. The `.dev-knowledge` session that authored it
made zero changes to corp-sca and wrote only to `.dev-knowledge/docs/audits/`.
