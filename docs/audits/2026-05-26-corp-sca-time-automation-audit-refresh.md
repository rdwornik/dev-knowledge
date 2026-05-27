---
type: audit-refresh
scope: corp-sca-time-automation universalization vs .dev-knowledge baseline current state
date: 2026-05-26
basis: no prior baseline audit — this is an INITIAL audit; standard = .dev-knowledge ADRs/templates/PLAYBOOK at main @ 907c4c7
status: research artifact (input to execution plan)
contract: read-only on corp-sca-time-automation; writes confined to .dev-knowledge/docs/audits/
---

# corp-sca-time-automation Universalization Audit Refresh (Initial) — 2026-05-26

## Methodology

**Initial audit — there is no prior baseline.** corp-sca-time-automation has
never been deep-audited against `.dev-knowledge` standards (no
`docs/audits/*corp-sca*` exists; the repo's own `docs/` holds only `archive/`
and `handoffs/`). Every finding is a **delta gap** against the current universal
standard; nothing to carry forward.

Read-only inspection at HEAD `d6dfb15` ("docs: add verified handoff doc for
2026-04-15 session"); every claim cites a `file:line` or verified file-state
fact. No corp-sca file modified (ADR-28/ADR-36 Layer-2 contract).

## Pivotal fact — same "creation" shape as corp-ops, two notable differences

corp-sca is a small **code project** (55 tracked files) that, like corp-ops,
predates universalization and carries **no** tier/scale residue (verified:
`grep -ni "scale\|tier" corp-sca/CLAUDE.md` returns nothing). Its gap is the
**absence of the governance scaffold**, not residue removal. Two differences from
corp-ops shape the plan:

1. **`.env.example` is actively referenced** — `CLAUDE.md:15` and `README.md:31`
   both instruct `cp .env.example .env`. Removal is **not** a clean delete (the
   contributor-reliance exception case).
2. **Flat-module source** — `src/` holds flat modules (`config.py`, `loader.py`,
   `mapper.py`, …; no package namespace), so its codemap is the **text-only
   override**, not a graphical Mermaid package graph.

corp-sca's CLAUDE.md is unusually **rich** — it carries an inline data-flow
diagram, a "Key modules" table, a "Config files" list, and a "Known issues"
section. These are ready-made seeds for ARCHITECTURE.md (data flow + module map)
and BACKLOG.md (the "Known issues" list).

**Audit-tool note (determined statically; tool not run in write mode).**
Static reading against the current `scripts/audit.py`:
- `check_vision_md` → **FAIL** ("VISION.md absent", `audit.py:141`).
- `check_adr38_baseline` → **FAIL** ("Missing required: ['VISION.md',
  'ARCHITECTURE.md', 'BACKLOG.md']", `audit.py:173`).
- `check_claude_md` → **PASS** (present, non-empty).
Two hard FAILs — the tool surfaces the core gap (as with corp-ops).

---

## Delta gaps — current standard vs corp-sca state

### Standard: VISION.md mandatory at root (ADR-38 A5; ADR-33)
- **Current:** **absent.**
- **Gap:** YES — **CS-1 [HIGH]**. Trips `vision_md` FAIL. Seed: corp-sca's
  purpose is well-stated in `CLAUDE.md` ("Automates weekly time entry submission
  to SharePoint SCA Time Tracker from Outlook calendar exports").
- **Evidence:** absence; `scripts/audit.py:141`.

### Standard: ARCHITECTURE.md mandatory at root (ADR-51 amendment 2026-05-23)
- **Current:** **absent** — but architecture content already lives **inline in
  CLAUDE.md** (an `## Architecture` section with a fenced data-flow block and a
  "Key modules" table of ~16 modules).
- **Gap:** YES — **CS-2 [HIGH]**. Mandatory universally. **Codemap form:**
  corp-sca's `src/` is flat (no package graph), so the **text-only override**
  (prose module overview, no CODEMAP markers, no generator) is the appropriate
  transitional form per `templates/ARCHITECTURE-template.md:68`. The CLAUDE.md
  data-flow block + module table re-home directly into the CORE sections.
- **Evidence:** absence; `corp-sca/CLAUDE.md` `## Architecture` section;
  flat `src/*.py` layout.

### Standard: BACKLOG.md mandatory at root (ADR-41; ADR-38 A5)
- **Current:** **absent** — but CLAUDE.md "Known issues" lists ~8 concrete
  tech-debt items (dead code, duplicated constants, misnamed function, thin test
  coverage) that are ready BACKLOG seeds.
- **Gap:** YES — **CS-3 [HIGH]**. Contributes to `adr38_baseline` FAIL. Unlike
  corp-ops, corp-sca's initial BACKLOG can be **populated** from the Known-issues
  list rather than near-empty.
- **Evidence:** absence; `corp-sca/CLAUDE.md` "Known issues" section.

### Standard: CHANGELOG retired (ADR-49)
- **Current:** `CHANGELOG.md` present.
- **Gap:** YES — **CS-4 [MEDIUM]**. Retire per ADR-49. corp-sca has `docs/`
  (with `handoffs/`) but no JOURNAL.md — same CHANGELOG→JOURNAL question as
  corp-ops (operator decision; JOURNAL is repo-specific/optional).
- **Evidence:** `corp-sca/CHANGELOG.md`.

### Standard: CLAUDE.md canonical single instruction file (ADR-53)
- **Current:** CLAUDE.md present, substantive, but **pre-ADR-53 free-form** — no
  session-start "Read first" ordering, no §pointers to VISION/ARCHITECTURE, not
  the 12-section template. It also currently *holds* the architecture content
  that ADR-51 says belongs in ARCHITECTURE.md.
- **Gap:** **CS-5 [MEDIUM]**. Re-home into the template; **move** the architecture
  section out to ARCHITECTURE.md (Action coordinates with CS-2) and replace it
  with a §3 pointer. Keep the operational content (quick start, API keys, dev
  standards, key commands).
- **Evidence:** `corp-sca/CLAUDE.md` (free-form; embeds `## Architecture`).

### Standard: README deprecated from baseline (ADR-38 A5)
- **Current:** README present ("Internal use only — Blue Yonder Pre-Sales" per
  CLAUDE.md license note); overlaps CLAUDE.md install/run content; references
  `.env.example` at `README.md:31`.
- **Gap:** **CS-6 [MEDIUM]** — README is OPTIONAL (external-audience only).
  corp-sca is internal → **delete** per default. Coordinate with the
  `.env.example` decision (CS-7) since the README is one of the two `cp
  .env.example .env` references.
- **Evidence:** `corp-sca/README.md:31`; "Internal use only" license note.

### Standard: `.env.example` do-not-create (Root hygiene pass-2)
- **Current:** `.env.example` present **and actively referenced** —
  `CLAUDE.md:15` (`cp .env.example .env  # then fill in ONEDRIVE_PATH,
  GRAPH_ACCESS_TOKEN, GEMINI_API_KEY`) and `README.md:31` (`Copy .env.example to
  .env and fill in:`).
- **Gap:** **CS-7 [LOW]** — but the **contributor-reliance exception case**
  (PLAYBOOK:227 says do-not-create; the ai-council plan's risk note covers the
  "if a contributor genuinely relies on it" exception). Resolution is **not** a
  clean `git rm`: either (a) migrate the required env-var names
  (`ONEDRIVE_PATH`, `GRAPH_ACCESS_TOKEN`, `GEMINI_API_KEY`, Azure IDs) into
  CLAUDE.md, drop the `cp` instruction, then remove `.env.example`; or (b) keep
  `.env.example` with a noted exception. **Operator decision.**
- **Evidence:** `corp-sca/CLAUDE.md:15`; `corp-sca/README.md:31`;
  `protocols/PLAYBOOK.md:227`.

### Standard: workspace file (recommended, PLAYBOOK §VS Code workspace)
- **Current:** `.vscode/` present (tracked); no `.code-workspace`.
- **Gap:** **CS-8 [LOW]** — a `.code-workspace` is recommended (not mandatory);
  if added, dot-prefix it. corp-sca already has a `.vscode/` dir, so a workspace
  file is lower-value here. Optional.
- **Evidence:** `.vscode/` tracked; no `.code-workspace`.

### Out of scope / INFO (not findings)
- **No `pyproject.toml` (uses `requirements.txt`).** Config consolidation (ruff /
  pytest into pyproject) is **N/A** without a pyproject; creating one is a
  **code-project** decision, out of universalization-governance scope. Surfaced,
  not planned.
- **`docs/handoffs/` flat handoff docs.** ADR-42 handoff-format adoption is a
  handoff-process concern (cross-ref `.dev-knowledge` BACKLOG "docs/HANDOFF.md
  flat file deprecation"), not a universalization-baseline gap. Out of scope.

### Explicit CONFORMS (no action)
- **No tier/scale residue** ✓ (zero hits in CLAUDE.md).
- **AGENTS.md absent** ✓ (ADR-53).
- **No `ruff.toml`/config duplication** ✓ (no tracked config — runs on defaults).
- **`.claude/`** present (repo-level runtime config) — fine.

---

## Operator-stated concerns — mapping to corp-sca state

### Concern: "architecture, backlog, journal, lessons, vision, bez readme, z kropkami na workspace, w odpowiedniej kolejności"
- **Current state:** ARCHITECTURE/BACKLOG/VISION **all absent** (CS-1/2/3) — the
  core conversion. README **present** ("bez readme") → CS-6 delete. No
  `.code-workspace` ("z kropkami na workspace") → CS-8 optional add. JOURNAL/LESSONS
  absent — JOURNAL pairs with CHANGELOG retirement (CS-4); LESSONS optional.
  "diagrams" → ARCHITECTURE's codemap (CS-2), here **text-only** (flat modules).
- **Maps to:** governance-scaffold creation (CS-1/2/3) + README delete (CS-6) +
  CHANGELOG retire (CS-4) + `.env.example` resolution (CS-7).

### Concern: "one maximal template, select elements by judgment"
- **Implication:** corp-sca's new ARCHITECTURE.md completes the three CORE
  sections; given a flat module set it adds a Module Map + Data Flow (both
  already drafted in CLAUDE.md) and uses the **text-only codemap override**. No
  tier gating; element selection by judgment of a small flat-structured repo.

## Findings summary table

| ID | Source | Sev | Category | Evidence (corp-sca) | Status |
|---|---|---|---|---|---|
| CS-1 | Delta (ADR-38 A5 / ADR-33) | HIGH | Missing governance file | VISION.md absent | gap → `vision_md` FAIL |
| CS-2 | Delta (ADR-51 universal) | HIGH | Missing governance file | ARCHITECTURE.md absent (content inline in CLAUDE) | gap → `adr38_baseline` FAIL |
| CS-3 | Delta (ADR-41 / ADR-38 A5) | HIGH | Missing governance file | BACKLOG.md absent (Known-issues seeds exist) | gap → `adr38_baseline` FAIL |
| CS-4 | Delta (ADR-49) | MEDIUM | Deprecated file present | `CHANGELOG.md` present | gap |
| CS-5 | Delta (ADR-53) | MEDIUM | CLAUDE.md form | `CLAUDE.md` (free-form; embeds architecture) | gap |
| CS-6 | Delta (ADR-38 A5) | MEDIUM | README disposition | `README.md:31` (internal; refs .env.example) | decision (default: delete) |
| CS-7 | Delta (Root hygiene pass-2) | LOW | Root hygiene (exception case) | `CLAUDE.md:15` + `README.md:31` `cp .env.example .env` | decision required |
| CS-8 | Delta (PLAYBOOK workspace) | LOW | Tooling | `.vscode/` present, no `.code-workspace` | optional |

**Distribution:** 0 CRITICAL · **3 HIGH** (CS-1, CS-2, CS-3) · **3 MEDIUM**
(CS-4, CS-5, CS-6) · **2 LOW** (CS-7, CS-8) · **8 total** (all delta — no
carry-forward).

## Conformance estimate

**~45% against the current standard** — the same band as corp-ops (both are
unconverted code projects missing three of four mandatory governance files). The
audit tool goes **red** here too (2 hard FAILs), in rough agreement with the
standard-level estimate because the gap is *missing files*, not *residue*. Two
factors make corp-sca's conversion slightly different from corp-ops's: richer
seed content (faster ARCHITECTURE + populated BACKLOG) pulls effort down, while
the `.env.example` reliance + text-only codemap judgment add small decision
points. corp-sca jumps to near-full conformance once the scaffold is created.

**Two-speed conformance — agrees here.** Tool **red**, standard ~45% — the
missing-file gap is visible to the tool, unlike the residue repos where tool-green
overstated conformance.

---

**Contract preserved:** zero `corp-sca-time-automation/` files modified
(read-only per ADR-28/ADR-36). All writes confined to
`.dev-knowledge/docs/audits/`.
