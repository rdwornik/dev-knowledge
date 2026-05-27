---
type: execution-plan
scope: corp-ops universalization actions for dedicated corp-ops session
date: 2026-05-26
basis: 2026-05-26-corp-ops-audit-refresh.md
status: research artifact (consumed by separate corp-ops session)
contract: this plan does NOT execute changes; consumed by corp-ops session per Layer-2 invariant
---

# corp-ops Universalization Execution Plan — 2026-05-26

This plan closes the 9 findings in `2026-05-26-corp-ops-audit-refresh.md`. It is
**consumed by a separate corp-ops Claude Code session** with write access to
corp-ops; the `.dev-knowledge` session that produced this plan does not. Every
action cites the finding(s) it closes.

Finding IDs (CO-*) are defined in the audit refresh — read it first.

## Sequencing principle

corp-ops is a **creation** job (build the missing governance scaffold), not a
residue cleanup. Ordered: **create the three mandatory files first** (they are
the point; VISION before ARCHITECTURE before CLAUDE re-home so each can reference
the prior); **then deprecated-file removals**; **then hygiene polish**. This is a
**small–medium** session — the content seeds already exist in CLAUDE.md and
`pyproject.toml`.

## Pre-flight requirements

- corp-ops working tree **clean**, on a feature branch off `main`, HEAD `97c78ba`
  or later — if corp-ops has moved, re-verify the refresh's citations.
- The corp-ops session has read, from `.dev-knowledge`: `VISION.md`,
  `ARCHITECTURE.md`, `templates/ARCHITECTURE-template.md`, `corp-monorepo/CLAUDE.md`
  (the 12-section ADR-53 reference), `protocols/PLAYBOOK.md` §Root hygiene +
  §Codemap workflow + §VS Code workspace, and ADR-33/38-A5/49/51/53.
- corp-ops tests green at start (`py -m pytest`).
- **Operator decisions resolved** (see below) — README delete (CO-6) and the
  CHANGELOG→JOURNAL question (CO-4).

## Operator decisions captured (apply uniformly per cross-repo decisions table)

| Decision | Default | corp-ops application |
|---|---|---|
| README disposition | **Delete** | Action 5 — clearest delete of the four (README duplicates CLAUDE + the new VISION). |
| Codemap maintenance | **Hand-authored Mermaid** | Action 2 — hand-author; corp-ops has a clean 4-package graph, so a real graphical codemap (not text-only). No generator opt-in. |
| `.env.example` | **Remove** | Action 6 — clean (not referenced by any flow). |
| LESSONS scope-tag backfill | **Defer (optional)** | N/A — corp-ops has no LESSONS.md; creating one is optional. |
| Workspace tier-residue | **Separate `.dev-knowledge` change** | Out of scope; only the optional dot-prefixed workspace add (Action 7). |

---

## Actions (sequenced)

### Action 1 — Create VISION.md
- **What:** Create `corp-ops/VISION.md` from the `.dev-knowledge` VISION shape.
  Frontmatter = `version`, `owner`, `last_reviewed`, `status` (no tier/scale).
  Seed: corp-ops is a "Standalone operational toolbox … OneDrive management,
  Google Drive backup, sync, and ecosystem health checks" (CLAUDE.md +
  `pyproject.toml:8`). Sections: Vision, Scope, Relationships (note: "Operates
  under `.dev-knowledge` methodology"; corp-ops is standalone — "No other repos
  depend on it directly" per CLAUDE.md "Integration points"), Lifecycle. A small
  repo may keep sections to a few lines.
- **Where:** `corp-ops/VISION.md` (new).
- **Why:** CO-1 [HIGH] (ADR-38 A5 / ADR-33; clears `vision_md` FAIL).
- **Verification:** from `.dev-knowledge` `python scripts/audit.py repo corp-ops`
  → `vision_md` PASS; frontmatter keys == `{version, owner, last_reviewed, status}`.
- **Dependencies:** none. **Do first** (ARCHITECTURE + CLAUDE reference it).
- **Commit suggestion:** `docs: add VISION.md (ADR-33 / ADR-38 A5 universalization)`.

### Action 2 — Create ARCHITECTURE.md (with hand-authored Mermaid codemap)
- **What:** Create `corp-ops/ARCHITECTURE.md` from
  `templates/ARCHITECTURE-template.md`. Frontmatter `last_reviewed`/`status`/`owner`.
  Complete the three CORE sections: **Purpose** (operational toolbox); **Codemap**
  — hand-author an inline Mermaid graph of `src/corp_ops/` (`auth`, `common`,
  `onedrive`, `gdrive` packages + `config.py`, with `tools/` CLI wrappers and
  `scripts/` PowerShell as separate nodes/notes), between `<!-- CODEMAP:START/END -->`
  markers; **Layer Boundaries & Invariants** — corp-ops has no Tach config, so
  name the informal layering (auth ← common ← onedrive/gdrive; tools/scripts are
  thin wrappers) and state invariants (e.g. "all destructive OneDrive ops require
  explicit user confirmation", "Graph API cannot delete in BY tenant — cookie
  auth only", both from CLAUDE.md "Key constraints"). Add a short Module Map if
  useful. No generator opt-in.
- **Where:** `corp-ops/ARCHITECTURE.md` (new).
- **Why:** CO-2 [HIGH] (ADR-51 universal; clears part of `adr38_baseline` FAIL).
- **Verification:** `adr38_baseline` advances; the three CORE sections present;
  CODEMAP block is a `mermaid` fence that renders.
- **Dependencies:** Action 1 (VISION exists to cross-reference). **No generator.**
- **Commit suggestion:** `docs: add ARCHITECTURE.md with Mermaid codemap (ADR-51)`.

### Action 3 — Create BACKLOG.md
- **What:** Create `corp-ops/BACKLOG.md` from the `.dev-knowledge` BACKLOG shape
  (header citing "ADR-41 as relaxed by ADR-47"; entry form `### [P{N}] [open]
  <title>` + What/Why/Added/Status). corp-ops has no in-repo issue list, so it
  can start as a near-empty scaffold ("no items currently — populate as work
  arises") per the `.dev-knowledge` Stream-A precedent.
- **Where:** `corp-ops/BACKLOG.md` (new).
- **Why:** CO-3 [HIGH] (ADR-41 / ADR-38 A5; clears the rest of `adr38_baseline` FAIL).
- **Verification:** `adr38_baseline` PASS (VISION + ARCHITECTURE + BACKLOG all
  present); header cites ADR-47.
- **Dependencies:** none (independent of Actions 1–2; do in the same arc).
- **Commit suggestion:** `docs: add BACKLOG.md scaffold (ADR-41 / ADR-47)`.

### Action 4 — Re-home CLAUDE.md into the ADR-53 template
- **What:** Restructure `corp-ops/CLAUDE.md` into the 12-section canonical form
  (use `corp-monorepo/CLAUDE.md` as the reference). Add §1 session-start "Read
  first" ordering (this file → VISION → ARCHITECTURE → recent commits) now that
  VISION + ARCHITECTURE exist. **Preserve** the substantive existing content
  (package structure → migrate to a §3 pointer to ARCHITECTURE; auth model, key
  constraints, dev standards → keep). Add the §pointer to ARCHITECTURE.md.
- **Where:** `corp-ops/CLAUDE.md` (restructure).
- **Why:** CO-5 [MEDIUM] (ADR-53 canonical form). Also fixes CO-8 (drop/repoint
  the dangling `../ECOSYSTEM.md` link while editing "Related repos").
- **Verification:** CLAUDE.md follows the template section set; §1 names the
  read order; `../ECOSYSTEM.md` link removed or repointed; `check_claude_md`
  still PASS.
- **Dependencies:** Actions 1–2 (so §1 can point to real VISION/ARCHITECTURE).
- **Commit suggestion:** `docs: re-home CLAUDE.md into ADR-53 canonical template`.

### Action 5 — Delete README.md
- **What:** `git rm corp-ops/README.md`. Its content (purpose + install/run)
  is now covered by VISION (purpose) + CLAUDE.md (how to work) — the redundancy
  was the audit's basis for the clearest delete.
- **Where:** `corp-ops/README.md` (`git rm`).
- **Why:** CO-6 [MEDIUM] (ADR-38 A5 — README deprecated, internal repo).
- **Verification:** `git -C corp-ops ls-files | grep -x README.md` → nothing; no
  doc instructs reading README.
- **Dependencies:** Actions 1, 4 (purpose/run content lives in VISION + CLAUDE
  before README is removed — verify destination per the "verify destination
  before drop" rule).
- **Commit suggestion:** `docs: delete deprecated README (ADR-38 A5; internal)`.

### Action 6 — Remove `.env.example`
- **What:** `git rm corp-ops/.env.example` (not referenced by any flow — corp-ops
  auth is cookie/token, not env-var).
- **Where:** `corp-ops/.env.example` (`git rm`).
- **Why:** CO-7 [LOW] (PLAYBOOK:227 do-not-create).
- **Verification:** `git -C corp-ops ls-files | grep env.example` → nothing.
- **Dependencies:** none.
- **Commit suggestion:** `chore: remove .env.example (root hygiene)`.

### Action 7 (optional) — Add dot-prefixed workspace + optional CHANGELOG→JOURNAL
- **What:** (a) **Optional:** add `.corp-ops.code-workspace` from the
  `.dev-knowledge` workspace pattern (dot-prefixed per root hygiene). (b)
  **CO-4 resolution:** retire `CHANGELOG.md` (`git rm`). Because ADR-49's record
  model is "git history + JOURNAL `Changes:` line" and corp-ops has no JOURNAL.md,
  pair the removal with either adding a minimal `JOURNAL.md` (repo-specific,
  optional) or accepting git history as the sole record. **Operator decides.**
- **Where:** `.corp-ops.code-workspace` (new, optional); `corp-ops/CHANGELOG.md`
  (`git rm`); optional `corp-ops/JOURNAL.md` (new).
- **Why:** CO-9 [LOW] (workspace) + CO-4 [MEDIUM] (CHANGELOG retire).
- **Verification:** no `CHANGELOG.md`; workspace (if added) is dot-prefixed.
- **Dependencies:** none.
- **Commit suggestion:** `chore: retire CHANGELOG (ADR-49); add dot-prefixed workspace`.

---

## Verification gates (between phases)

- **After Actions 1–3 (governance scaffold):** from `.dev-knowledge`
  `python scripts/audit.py repo corp-ops` → `vision_md` PASS + `adr38_baseline`
  PASS + `claude_md` PASS (the two hard FAILs cleared). corp-ops tests still green.
- **After Action 4 (CLAUDE re-home):** CLAUDE.md is template-form; §1 read order
  resolves to real files; no dangling `../ECOSYSTEM.md`.
- **Whole-plan exit:** corp-ops `git status` clean; `py -m pytest` green;
  `py -m ruff check src/ tools/ tests/` clean; no `README.md`, no `CHANGELOG.md`,
  no `.env.example`; VISION/ARCHITECTURE/BACKLOG present.

## Risk register

- **Creation vs cleanup.** corp-ops needs files *built*, not edited — the seed
  content is in CLAUDE.md + pyproject, but the new VISION/ARCHITECTURE must
  describe the *actual* toolbox, not a templated placeholder (a near-empty
  ARCHITECTURE rots fastest — ADR-51's own rejected-alternative warning). Invest
  in real content; corp-ops is small enough to document fully.
- **README delete before content migration (Action 5 ordering).** Verify VISION +
  CLAUDE actually carry the README's purpose/run content before `git rm` (the
  "verify destination before drop" rule).
- **CHANGELOG→JOURNAL gap (Action 7b).** Retiring CHANGELOG without a JOURNAL
  leaves git history as the sole narrative record — fine per ADR-49, but confirm
  the operator accepts no JOURNAL rather than silently dropping the record.
- **Codemap form.** corp-ops has a real package graph → graphical Mermaid is
  right (unlike corp-sca's flat modules). Do not default to text-only.

## What this plan does NOT include

- **Methodology codification** — `.dev-knowledge` standards work.
- **Migrating corp-ops to a new dependency model** or touching `src/`/scripts
  code — universalization is governance-doc creation only.
- **Cross-repo modifications** outside corp-ops.
- **A proceed/no-proceed recommendation** — the operator decides after reading.

## Estimated execution scope

- **Required actions:** 6 (Actions 1–6). **Optional:** Action 7 (workspace +
  CHANGELOG→JOURNAL — CO-4 is required, its JOURNAL pairing is the optional part).
- **Estimated commits:** 6–8.
- **Estimated session size:** **small–medium.** Three new governance files +
  one CLAUDE re-home + three removals. No source-code changes. The clean
  underlying structure makes this the most mechanical of the three full audits.
- **Findings closed at completion:** all 9 (CO-9 optional).

## Operator decisions required before execution

1. **README disposition (Action 5).** Delete (default; clearest of the four) or keep?
2. **CHANGELOG → JOURNAL (Action 7b).** Add a JOURNAL.md alongside retiring
   CHANGELOG, or accept git history as the sole record?
3. **Workspace (Action 7a).** Add a dot-prefixed `.code-workspace` now, or defer?
4. **VISION `status` value (Action 1).** `active` expected — confirm.

## Lessons forward (to corp-sca-time-automation)

- **corp-sca is the same creation shape** (missing VISION/ARCHITECTURE/BACKLOG,
  CHANGELOG + README present, no tier residue) — the Action 1→6 sequence transfers
  directly. Two differences: corp-sca's `.env.example` **is** referenced
  (`cp .env.example .env`) so removal needs care; and corp-sca is **flat-module**
  so its codemap is the **text-only override**, not a graphical Mermaid.
- **Seed content lives in CLAUDE.md** — corp-sca's CLAUDE.md is even richer
  (inline data-flow + module table + "Known issues" list), so its
  ARCHITECTURE.md and BACKLOG.md have ready-made seeds.

---

**Contract preserved:** this plan executes nothing; it is consumed by a separate
corp-ops session. The `.dev-knowledge` session that authored it made zero changes
to corp-ops and wrote only to `.dev-knowledge/docs/audits/`.
