---
type: audit-refresh
scope: corp-ops universalization vs .dev-knowledge baseline current state
date: 2026-05-26
basis: no prior baseline audit — this is an INITIAL audit; standard = .dev-knowledge ADRs/templates/PLAYBOOK at main @ 907c4c7
status: research artifact (input to execution plan)
contract: read-only on corp-ops; writes confined to .dev-knowledge/docs/audits/
---

# corp-ops Universalization Audit Refresh (Initial) — 2026-05-26

## Methodology

**Initial audit — there is no prior baseline.** Unlike corp-monorepo and
ai-council, corp-ops has never been deep-audited against `.dev-knowledge`
standards (no `docs/audits/*corp-ops*` exists, and corp-ops has no `docs/`
directory of its own). Every finding below is therefore a **delta gap** against
the current universal standard; there is nothing to carry forward. The "refresh"
framing is kept for cross-repo-doc consistency, but methodologically this
establishes the corp-ops baseline.

Read-only inspection of corp-ops at HEAD `97c78ba` ("chore: Scripts → Dev path
migration"); every claim cites a `file:line` or verified file-state fact. No
corp-ops file modified (ADR-28/ADR-36 Layer-2 contract).

## Pivotal fact — corp-ops predates universalization entirely

corp-ops is a clean, small **code project** (47 tracked files; `src/corp_ops/`
package + PowerShell scripts) that was never brought into the universalization
program. It carries **none** of the tier/scale residue corp-monorepo and
ai-council show — verified: `grep -ni "scale\|tier" corp-ops/CLAUDE.md` returns
nothing. Its gap is the **absence of the governance scaffold** (VISION,
ARCHITECTURE, BACKLOG) plus a pre-ADR-53 CLAUDE.md and two deprecated files
(CHANGELOG, README), **not** residue removal. This makes it a cleaner — but
larger-by-creation — conversion than corp-monorepo's residue cleanup.

**Audit-tool note (determined statically; tool not run in write mode).**
Static reading against the current `scripts/audit.py` checks:
- `check_vision_md` → **FAIL** ("VISION.md absent at repo root", `audit.py:141`).
- `check_adr38_baseline` → **FAIL** ("Missing required: ['VISION.md',
  'ARCHITECTURE.md', 'BACKLOG.md']", `audit.py:173-179`).
- `check_claude_md` → **PASS** (present, non-empty).
This is the one repo of the four where the audit tool itself goes **red** —
two hard FAILs. The tool *does* surface corp-ops's core gap (unlike the
residue-only repos, where it stayed green).

---

## Delta gaps — current standard vs corp-ops state

### Standard: VISION.md mandatory at root (ADR-38 A5; ADR-33)
- **corp-ops current:** **absent** (`git ls-files` — no `VISION.md`).
- **Gap:** YES — **CO-1 [HIGH]**. Mandatory governance file missing; trips
  `vision_md` FAIL + contributes to `adr38_baseline` FAIL. Seed content exists:
  corp-ops's purpose is well-described in `CLAUDE.md` ("Standalone operational
  toolbox: Python package + PowerShell scripts for OneDrive management, Google
  Drive backup, sync, and ecosystem health checks") and `pyproject.toml:8`
  ("Operational toolbox for Corporate OS ecosystem").
- **Evidence:** absence; `scripts/audit.py:141`.

### Standard: ARCHITECTURE.md mandatory at root (ADR-51 amendment 2026-05-23)
- **corp-ops current:** **absent**.
- **Gap:** YES — **CO-2 [HIGH]**. Mandatory universally. Seed content exists:
  `CLAUDE.md` "Package structure" block documents `src/corp_ops/` with four
  sub-packages (`auth/`, `common/`, `onedrive/`, `gdrive/`) + `config.py`, plus
  `tools/`, `scripts/`, `config/`, `tests/`. This is a clean package graph →
  a graphical Mermaid codemap is appropriate (not the text-only override).
- **Evidence:** absence; `corp-ops/CLAUDE.md` Package-structure block.

### Standard: BACKLOG.md mandatory at root (ADR-41; ADR-38 A5)
- **corp-ops current:** **absent**.
- **Gap:** YES — **CO-3 [HIGH]**. Mandatory governance file missing; contributes
  to `adr38_baseline` FAIL. corp-ops has no obvious in-repo backlog source (no
  "Known issues" section, unlike corp-sca) — the initial BACKLOG can start as a
  near-empty scaffold ("no items currently") per the `.dev-knowledge` Stream-A
  precedent.
- **Evidence:** absence; `scripts/audit.py:173`.

### Standard: CHANGELOG retired (ADR-49)
- **corp-ops current:** `CHANGELOG.md` present (`# Changelog — corp-ops`, last
  entry `[1.0.0] — 2026-03-15`).
- **Gap:** YES — **CO-4 [MEDIUM]**. ADR-49 retired CHANGELOG ecosystem-wide
  (record = git history + JOURNAL `Changes:` line). corp-ops has no JOURNAL.md —
  so retiring CHANGELOG should pair with either adding a minimal JOURNAL.md or
  accepting git history as the sole record (operator decision; JOURNAL is
  repo-specific, not part of the universal baseline).
- **Evidence:** `corp-ops/CHANGELOG.md:1-3`.

### Standard: CLAUDE.md canonical single instruction file (ADR-53)
- **corp-ops current:** CLAUDE.md present but **pre-ADR-53 free-form** — it has
  no session-start "Read first" ordering, no §pointers to VISION/ARCHITECTURE
  (which don't exist yet), and does not follow the 12-section template. It is
  substantive and accurate (package structure, auth model, constraints) but not
  the canonical form.
- **Gap:** **CO-5 [MEDIUM]**. ADR-53 makes CLAUDE.md the single canonical
  instruction file; the corp-monorepo CLAUDE.md (148-line, 12-section template)
  is the reference. corp-ops's CLAUDE.md should be re-homed into the template,
  adding §1 session-start reading order (VISION → ARCHITECTURE) once those exist.
- **Evidence:** `corp-ops/CLAUDE.md` (free-form headings, no session-start §).

### Standard: README deprecated from baseline (ADR-38 A5)
- **corp-ops current:** README present; internal toolbox doc that **heavily
  overlaps** CLAUDE.md "What this repo does" (same opening sentence almost
  verbatim) and the install/run commands.
- **Gap:** **CO-6 [MEDIUM]** — README is now OPTIONAL (external-audience only).
  corp-ops is internal (no external audience), and its README duplicates CLAUDE +
  the future VISION → **delete** per the baked-in default; the redundancy makes
  this the clearest delete of the four.
- **Evidence:** `corp-ops/README.md:1-3` (mirrors `CLAUDE.md` opening).

### Standard: `.env.example` do-not-create + dot-prefix (Root hygiene)
- **corp-ops current:** `.env.example` present at root; **not referenced** by
  CLAUDE.md or README (auth is cookie/token-based per `CLAUDE.md` "Auth model",
  not env-var-based).
- **Gap:** **CO-7 [LOW]** (PLAYBOOK:227 do-not-create). Clean removal — nothing
  relies on it.
- **Evidence:** root `.env.example`; `CLAUDE.md` Auth-model section.

### Standard: canonical pointers must resolve
- **corp-ops current:** `CLAUDE.md` "Related repos" and `README.md` both link
  `[ECOSYSTEM.md](../ECOSYSTEM.md)` — but `Dev/ECOSYSTEM.md` **does not exist**
  (verified: `ls Dev/ECOSYSTEM.md` → not found). Also links `../corp-by-os/` and
  `../corp-os-meta/` (status of those repos unverified — cross-ref the
  `.dev-knowledge` BACKLOG "Undiscovered repos confirmation" item).
- **Gap:** **CO-8 [LOW]** — dangling pointer. Fix when re-homing CLAUDE.md /
  resolving README (remove or repoint the dead `../ECOSYSTEM.md` link).
- **Evidence:** `corp-ops/CLAUDE.md` "Related repos"; `corp-ops/README.md` footer.

### Standard: workspace file (recommended, PLAYBOOK §VS Code workspace)
- **corp-ops current:** no `.code-workspace` file.
- **Gap:** **CO-9 [LOW]** — a `.code-workspace` is recommended (not mandatory).
  If added, dot-prefix it (`.corp-ops.code-workspace`) per root hygiene. Optional.
- **Evidence:** absence.

### Explicit CONFORMS (no action)
- **Tool-config consolidation** ✓ — `pyproject.toml` carries `[tool.ruff]` +
  `[tool.pytest.ini_options]`; **no** standalone `ruff.toml` (`pyproject.toml:30`).
- **No tier/scale residue** ✓ — zero hits in CLAUDE.md.
- **AGENTS.md absent** ✓ (ADR-53).
- **Clean src package graph** ✓ — `src/corp_ops/{auth,common,onedrive,gdrive}` +
  `config.py`, codemap-friendly.
- **`.claude/rules/`** present (`code-standards.md`, `python-env.md`,
  `testing.md`) — repo-level runtime config, fine.

---

## Operator-stated concerns — mapping to corp-ops state

### Concern: "architecture, backlog, journal, lessons, vision, bez readme, z kropkami na workspace, w odpowiedniej kolejności"
- **Current state:** ARCHITECTURE/BACKLOG/VISION **all absent** (CO-1/2/3) —
  the core conversion. README **present** ("bez readme") → CO-6 delete. No
  `.code-workspace` ("z kropkami na workspace") → CO-9 optional add (dot-prefixed).
  JOURNAL/LESSONS absent — JOURNAL pairs with CHANGELOG retirement (CO-4);
  LESSONS is repo-specific and optional. "diagrams" → ARCHITECTURE's codemap
  (CO-2) will be the first diagram (graphical Mermaid; corp-ops has a clean graph).
- **Maps to:** the full governance-scaffold creation (CO-1/2/3) + README delete
  (CO-6) + CHANGELOG retire (CO-4) + workspace (CO-9).

### Concern: "one maximal template, select elements by judgment"
- **Implication:** corp-ops's new ARCHITECTURE.md completes the three CORE
  sections (Purpose, Codemap, Layer Boundaries & Invariants) and adds only what
  a small operational toolbox needs — likely just CORE + a short Module Map. No
  tier gating; element selection by judgment of corp-ops's modest complexity.

## Findings summary table

| ID | Source | Sev | Category | Evidence (corp-ops) | Status |
|---|---|---|---|---|---|
| CO-1 | Delta (ADR-38 A5 / ADR-33) | HIGH | Missing governance file | VISION.md absent | gap → `vision_md` FAIL |
| CO-2 | Delta (ADR-51 universal) | HIGH | Missing governance file | ARCHITECTURE.md absent | gap → `adr38_baseline` FAIL |
| CO-3 | Delta (ADR-41 / ADR-38 A5) | HIGH | Missing governance file | BACKLOG.md absent | gap → `adr38_baseline` FAIL |
| CO-4 | Delta (ADR-49) | MEDIUM | Deprecated file present | `CHANGELOG.md:1` | gap |
| CO-5 | Delta (ADR-53) | MEDIUM | CLAUDE.md form | `CLAUDE.md` (free-form, pre-template) | gap |
| CO-6 | Delta (ADR-38 A5) | MEDIUM | README disposition | `README.md:1-3` (overlaps CLAUDE) | decision (default: delete) |
| CO-7 | Delta (Root hygiene pass-2) | LOW | Root hygiene | `.env.example` present | gap |
| CO-8 | Delta (pointer integrity) | LOW | Doc quality | `CLAUDE.md`/`README.md` `../ECOSYSTEM.md` dangling | gap |
| CO-9 | Delta (PLAYBOOK workspace) | LOW | Tooling | no `.code-workspace` | optional |

**Distribution:** 0 CRITICAL · **3 HIGH** (CO-1, CO-2, CO-3) · **3 MEDIUM**
(CO-4, CO-5, CO-6) · **3 LOW** (CO-7, CO-8, CO-9) · **9 total** (all delta — no
carry-forward).

## Conformance estimate

**~45% against the current standard.** corp-ops conforms on the *technical*
hygiene axis (config consolidation, no tier residue, clean package graph, no
AGENTS.md, compliant naming) but is missing **three of the four mandatory
governance files** and carries two deprecated files. The audit tool goes **red**
here (2 hard FAILs) — the only repo of the four where the tool surfaces the core
gap rather than under-reporting it. Once VISION/ARCHITECTURE/BACKLOG are created
and README/CHANGELOG resolved, corp-ops jumps to near-full conformance (its
underlying structure is already clean).

**Two-speed conformance — inverted here.** For the residue repos the tool was
green while the standard-level was ~70-80%. For corp-ops the tool is **red** and
the standard-level is ~45% — the two roughly agree, because the gap is *missing
files* (which the tool checks) rather than *residue in present files* (which it
doesn't).

---

**Contract preserved:** zero `corp-ops/` files modified (read-only per
ADR-28/ADR-36). All writes confined to `.dev-knowledge/docs/audits/`.
