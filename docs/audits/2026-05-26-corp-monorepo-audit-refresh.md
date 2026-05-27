---
type: audit-refresh
scope: corp-monorepo universalization vs .dev-knowledge baseline current state
date: 2026-05-26
basis: docs/audits/2026-05-23-corp-monorepo-deep-audit.md (baseline) + standards delta 2026-05-23 → 2026-05-26
status: research artifact (input to execution plan)
contract: read-only on corp-monorepo; writes confined to .dev-knowledge/docs/audits/
---

# corp-monorepo Universalization Audit Refresh — 2026-05-26

## Methodology

This is a **delta refresh**, not a re-audit. The 2026-05-23 corp-monorepo deep
audit (`docs/audits/2026-05-23-corp-monorepo-deep-audit.md`) is the baseline;
this document (a) re-checks the status of every baseline finding at the current
corp-monorepo HEAD, and (b) surfaces NEW gaps from `.dev-knowledge` standards
that the baseline did not apply (chiefly the tier-deprecation amendments dated
the same day as the baseline, and root-hygiene pass-2 dated the day after).
Every claim cites a corp-monorepo `file:line` or verified file-state fact;
read-only per ADR-28/ADR-36 (no corp-monorepo file modified).

## Pivotal fact — HEAD moved 2 commits, none of them universalization work

The baseline targeted HEAD `32a47f8`. corp-monorepo's current HEAD is
**`f418c78`** ("Merge branch 'audit/adr27-status'"). The two commits between:

```
80ebf67 docs(audits): ADR-27 implementation status audit 2026-05-25
66d244a chore(journal): record ADR-27 audit session 2026-05-25
```

Both are documentation/audit additions internal to corp-monorepo. **No
universalization remediation landed.** Consequence: all 12 baseline findings
**carry forward verbatim** — none could have been closed (the relevant files
were untouched), and the delta in this refresh comes entirely from
`.dev-knowledge` **standards** the baseline didn't apply, not from
corp-monorepo moving.

**Standards inventoried as the current basis:**

| Standard | Change vs the baseline's view | Date | Effect on corp-monorepo |
|---|---|---|---|
| ADR-33 amendment | VISION `tier`/`scale` removed (baseline treated them as CONFORMS) | 2026-05-23 | `tier: standard` + `scale: L` now residue |
| ADR-40 deprecation | Tier algorithm retired | 2026-05-23 | CLAUDE.md `Scale:`/`Scale M+` prose now residue |
| ADR-51 amendment | ARCHITECTURE universal (was M+L) | 2026-05-23 | corp already has one — presence conforms; form does not (carry-forward A1/A2) |
| ADR-38 A5 | README deprecated from baseline | 2026-05-23 | README disposition decision (re-scopes F-README) |
| Root hygiene pass-2 | `.env.example` do-not-create; dot-prefix `.ruff.toml` | 2026-05-24 | 2 new root-hygiene gaps the baseline predates |

**Audit-tool note (determined statically; tool not run in write mode).**
`scripts/audit.py repo corp-monorepo` writes under `ecosystem/` + `docs/audits/`,
outside this session's contract, so it was not executed. Static reading of
corp-monorepo against the current checks:
- `check_vision_md` → **PASS** (VISION carries all 4 required keys —
  `version`, `last_reviewed`, `owner`, `status`; the extra `tier`/`scale` keys
  are *ignored* by the check, so the tier-residue does **not** trip the tool).
- `check_adr38_baseline` → **PASS** (VISION + ARCHITECTURE + BACKLOG all present).
- `check_claude_md` → **PASS** (present, non-empty).
This is the two-speed gap again: **3 PASS at the tool level, ~72% at the
full-standard level.** The tool sees none of the 17 findings below.

---

## Baseline carry-forward (from the 2026-05-23 corp-monorepo deep audit)

All 12 baseline findings are **STILL OPEN** at HEAD `f418c78` (verified
file-state). Re-id'd here with a `CM-CF` prefix for cross-reference.

| ID | Baseline | Sev | Finding | Status now | Evidence (current file-state) |
|---|---|---|---|---|---|
| CM-CF1 | A1 | HIGH | ARCHITECTURE.md does not adopt canonical template form (no frontmatter, no `[CORE]` tags, CORE names diverge) | STILL OPEN | `ARCHITECTURE.md:1` `# Architecture Reference -- Corporate OS` (no YAML frontmatter); `:6` `## System Overview` (not `Purpose [CORE]`) |
| CM-CF2 | A2 | HIGH | Codemap not in embedded-Mermaid form; CODEMAP markers absent | STILL OPEN | `grep -c CODEMAP:START ARCHITECTURE.md` → **0**; codemap is hand-written tree + SVG pointer |
| CM-CF3 | A4 | HIGH | ARCHITECTURE.md stale (now ~8+ weeks) | STILL OPEN | `ARCHITECTURE.md:4` "Last updated: 2026-03-30"; predates ADR-30/31/53/54, VISION/BACKLOG additions |
| CM-CF4 | F-VISION | HIGH | VISION §Values "one routing authority / single source of truth" aspirational; routing is code-distributed | STILL OPEN | `VISION.md` §Values claim vs distributed routing across `src/corp/extraction/routing.py`, `ingest/router.py`, `intent_router.py`, `llm_router.py` |
| CM-CF5 | A3 | MEDIUM | ADR-51 conformance gate the prior corp audit cited is now closed (status refresh — not a defect) | INFO | generator shipped (`.dev-knowledge/scripts/codemap/cli.py`); corp may opt in at will |
| CM-CF6 | F-CONTRIBUTING | MEDIUM | CONTRIBUTING stale facts (ADR count "26" vs actual ~30; Phase-1 block describes completed work as pending) | STILL OPEN | `CONTRIBUTING.md:119` "(26 decisions)"; `:105-114` Phase-1-pending block |
| CM-CF7 | F-README | MEDIUM | README stale test total + wrong install-extras group | STILL OPEN (now disposition-gated — CM-D-README) | `README.md:18` "Total **2,412**" (cols sum 2,153; latest run higher); `README.md:28` `pip install -e ".[dev,llm]"` (`llm` not a real extras group) |
| CM-CF8 | A5 | LOW | Layer model rendered as ASCII, not inline Mermaid | STILL OPEN | `ARCHITECTURE.md` layer section ASCII `interface > orchestration > core > foundation` |
| CM-CF9 | B | LOW | Legacy `docs/archive/` UPPERCASE_TYPE underscore filenames | STILL OPEN | `docs/archive/*` `YYYY-MM-DD_TYPE_descriptor.md` form |
| CM-CF10 | D | LOW | BACKLOG header cites ADR-41 strict schema, not ADR-47 | STILL OPEN | `BACKLOG.md:3-5` cites "Schema per ADR-41 … `[P{N}]` priority" |
| CM-CF11 | E | LOW | ADR-namespace collision; CLAUDE §11 mixes corp/`.dev-knowledge` namespaces unprefixed | STILL OPEN | `CLAUDE.md` §11 ADR list mixes namespaces |
| CM-CF12 | F-ruff | LOW | `ruff.toml` (lenient `E,F,I`) silently overrides `pyproject.toml [tool.ruff]` (stricter) | STILL OPEN | `ruff.toml:2` `select = ["E","F","I"]`; `pyproject.toml:69-73` `[tool.ruff]` + `[tool.ruff.lint]` |

**Re-contextualization of CM-CF7 (README) by the new standard.** At baseline this
was "fix the README counts." ADR-38 A5 (2026-05-23) deprecated README from the
mandatory baseline (optional, external-audience only). It is therefore now
**gated on the README disposition decision** (CM-D-README): if README is deleted,
CM-CF7 is moot; if kept, the count + extras-group must be fixed.

---

## Delta gaps — standards the baseline didn't apply, vs corp-monorepo current state

### Standard: VISION frontmatter — no `tier`/`scale` (ADR-33 Amendment 2026-05-23)
- **corp-monorepo current:** `VISION.md:1-8` frontmatter = `version: 1.0`,
  `tier: standard`, `scale: L`, `owner: rob`, `status: active`,
  `last_reviewed: 2026-05-18`.
- **Gap:** YES — **CM-D1 [MEDIUM]**. `tier: standard` + `scale: L` are residue
  (ADR-33 amendment removed both). The baseline's Category C treated this
  frontmatter as CONFORMS — it was written under the pre-amendment view. Unlike
  ai-council, `status` is **already present**, so the only fix is *removing* two
  keys (the `vision_md` check already PASSES and will continue to).
- **Evidence:** `corp-monorepo/VISION.md:1-8`; `scripts/audit.py:155`.

### Standard: tier system deprecated — no `Scale:` prose (ADR-40 deprecated; ADR-51 universal)
- **corp-monorepo current:** CLAUDE.md carries tier-conditional prose in three
  places: `:25` "**Scale:** `L` (per `.dev-knowledge/protocols/PLAYBOOK.md`
  Project Scale Tiers)"; `:30` "required at Scale M+, per ADR-51"; `:136`
  "ADR-51: ARCHITECTURE.md convention … (Scale M+)".
- **Gap:** YES — **CM-D2 [MEDIUM]**. The tier system is deprecated ecosystem-wide;
  "Project Scale Tiers" no longer exists as a live PLAYBOOK construct, and ADR-51
  is now universal (not "M+"). Same three-file tier-residue pattern ai-council
  showed (VISION frontmatter CM-D1 + CLAUDE prose CM-D2); corp-monorepo's
  ARCHITECTURE has no frontmatter at all, so its frontmatter-residue is folded
  into CM-CF1 (template adoption) rather than a separate finding.
- **Evidence:** `corp-monorepo/CLAUDE.md:25,30,136`.

### Standard: README.md deprecated from baseline (ADR-38 Amendment A5, 2026-05-23)
- **corp-monorepo current:** README present at root; product-facing ("Corporate
  OS Monorepo … pre-sales engineering", module/CLI/test-count table).
- **Gap:** **CM-D-README [MEDIUM]** — README is now OPTIONAL (external-audience
  only). Needs an explicit keep/delete decision; this decision *gates* CM-CF7.
  **Note:** of the four child repos, corp-monorepo's README is the most
  plausibly external/product-facing — flagged for explicit operator confirmation
  rather than silent deletion (see Operator decisions in the execution plan).
- **Evidence:** `README.md:1-18` (product framing + module table).

### Standard: `.env.example` do-not-create (Root hygiene pass-2, 2026-05-24)
- **corp-monorepo current:** `.env.example` present at root (396 bytes).
- **Gap:** YES — **CM-D3 [LOW]** (PLAYBOOK:227 "do not create `.env.example`";
  env-var docs belong in CLAUDE.md/VISION). Postdates the baseline (pass-2 was
  2026-05-24). Confirm no contributor flow relies on it before removing.
- **Evidence:** root `.env.example`; `protocols/PLAYBOOK.md:227`.

### Standard: dot-prefix workspace + config (Root hygiene)
- **corp-monorepo current:** `corp-monorepo.code-workspace` present, not
  dot-prefixed; `ruff.toml` present at root, not dot-prefixed.
- **Gaps:**
  - **CM-D4 [LOW]:** `corp-monorepo.code-workspace` → `.corp-monorepo.code-workspace`
    (PLAYBOOK:211 dot-prefix).
  - **CM-D5 [LOW]:** the `ruff.toml` dot-prefix rule (PLAYBOOK:230 `.ruff.toml`)
    is **mooted by the correct fix to CM-CF12** — consolidating ruff config into
    `pyproject.toml [tool.ruff]` (deleting `ruff.toml`) removes the file entirely,
    so there is nothing left to dot-prefix. Do not dot-prefix-then-delete.
- **Evidence:** root `corp-monorepo.code-workspace`, `ruff.toml`;
  `protocols/PLAYBOOK.md:211,230`.

### Standard: CHANGELOG retired (ADR-49) / AGENTS.md retired (ADR-53)
- **corp-monorepo current:** no `CHANGELOG.md` (✓), no `AGENTS.md` (✓).
- **Gap:** **NONE — CONFORMS.** (Per ADR-30 corp retired CHANGELOG; AGENTS.md
  removed under ADR-54 follow-up. Listed for completeness.)

### Standard: ARCHITECTURE.md mandatory universally (ADR-51 Amendment 2026-05-23)
- **corp-monorepo current:** ARCHITECTURE.md present at root.
- **Gap:** **presence CONFORMS** (mandatory-universal satisfied). Form does not —
  that is CM-CF1 + CM-CF2 + CM-CF3 + CM-CF8 (carry-forward).

### Standard: canonical files at root, correct set (ADR-38 A5)
- **Required (universal):** VISION ✓, CLAUDE ✓, ARCHITECTURE ✓, BACKLOG ✓.
  README OPTIONAL (present — CM-D-README). CHANGELOG removed (absent ✓).
- **Repo-specific present:** JOURNAL ✓, CONTRIBUTING ✓. LESSONS absent **by
  design** (cross-repo lessons route to `.dev-knowledge/LESSONS.md` per corp
  CLAUDE.md §4 — not a gap).
- **Gap:** none on presence beyond README disposition. Mandatory set complete.

---

## Operator-stated concerns — mapping to corp-monorepo state

### Concern: "metodologia … architecture, backlog, journal, lessons, vision, bez readme, z kropkami na workspace, w odpowiedniej kolejności"
- **Current state:** VISION/ARCHITECTURE/BACKLOG/JOURNAL/CONTRIBUTING present at
  root (correct set + order). README **still present** ("bez readme") →
  CM-D-README. Workspace **not** dot-prefixed ("z kropkami na workspace") →
  CM-D4. "diagrams" → codemap still hand-written tree + SVG, not the embedded
  Mermaid default (CM-CF2/CM-CF8). LESSONS intentionally absent (routes upward).
- **Maps to:** README disposition (CM-D-README) + workspace dot-prefix (CM-D4) +
  embedded-Mermaid codemap (CM-CF2/CM-CF8).

### Concern: "one maximal template, select elements by complexity/judgment"
- **Implication:** corp-monorepo's ARCHITECTURE.md should adopt the single
  canonical template, completing the three CORE sections and keeping the rest by
  judgment — corp's content is already L-grade (the baseline rated it high
  quality), so this is a structural **re-home**, not a rewrite (CM-CF1).
- **Current divergence:** the doc predates ADR-51 entirely (no frontmatter, no
  `[CORE]` tags, no CODEMAP markers). The fix is exactly the template adoption +
  codemap-marker insertion the baseline §6 step 1 already sequenced.

## Findings summary table

| ID | Source | Sev | Category | Evidence (corp-monorepo) | Status |
|---|---|---|---|---|---|
| CM-CF1 | Baseline A1 | HIGH | Architecture/template form | `ARCHITECTURE.md:1,6` | open (carry-forward) |
| CM-CF2 | Baseline A2 | HIGH | Architecture/codemap form | `ARCHITECTURE.md` (0 CODEMAP markers) | open (carry-forward) |
| CM-CF3 | Baseline A4 | HIGH | Architecture/staleness | `ARCHITECTURE.md:4` | open (carry-forward) |
| CM-CF4 | Baseline F-VISION | HIGH | Doc quality (aspirational) | `VISION.md` §Values | open (carry-forward) |
| CM-CF5 | Baseline A3 | MEDIUM | Architecture/gate-closed | n/a (status refresh) | INFO (not a defect) |
| CM-CF6 | Baseline F-CONTRIBUTING | MEDIUM | Doc quality | `CONTRIBUTING.md:119,105-114` | open (carry-forward) |
| CM-CF7 | Baseline F-README | MEDIUM | Doc quality | `README.md:18,28` | open — disposition-gated (CM-D-README) |
| CM-CF8 | Baseline A5 | LOW | Architecture/visual | `ARCHITECTURE.md` layer section | open (carry-forward) |
| CM-CF9 | Baseline B | LOW | Naming | `docs/archive/*` | open (carry-forward) |
| CM-CF10 | Baseline D | LOW | BACKLOG | `BACKLOG.md:3-5` | open (carry-forward) |
| CM-CF11 | Baseline E | LOW | Cross-repo governance | `CLAUDE.md` §11 | open (carry-forward) |
| CM-CF12 | Baseline F-ruff | LOW | Config | `ruff.toml:2` vs `pyproject.toml:69-73` | open (carry-forward) |
| CM-D1 | Delta (ADR-33 Am.) | MEDIUM | Frontmatter | `VISION.md:1-8` (`tier`/`scale` residue) | gap (audit `vision_md` still PASS) |
| CM-D2 | Delta (ADR-40 deprec.) | MEDIUM | Tier-residue prose | `CLAUDE.md:25,30,136` | gap |
| CM-D-README | Delta (ADR-38 A5) | MEDIUM | README disposition | `README.md` present (product-facing) | decision required |
| CM-D3 | Delta (Root hygiene pass-2) | LOW | Root hygiene | `.env.example` present | gap |
| CM-D4 | Delta (Root hygiene) | LOW | Root hygiene | `corp-monorepo.code-workspace` (no dot) | gap |
| CM-D5 | Delta (Root hygiene) | LOW | Config/hygiene | `ruff.toml` (no dot) | gap — **mooted by CM-CF12 fix** |

**Distribution:** 0 CRITICAL · **4 HIGH** (CM-CF1, CM-CF2, CM-CF3, CM-CF4) ·
**5 MEDIUM** (CM-CF5*, CM-CF6, CM-CF7, CM-D1, CM-D2, CM-D-README — note CM-CF5 is
INFO not a defect, so 5 actionable MEDIUM) · **8 LOW** · **17 total** (12
carry-forward + 5 delta; CM-D5 mooted by CM-CF12).

**Explicit CONFORMS (no action):** CHANGELOG absent (ADR-49); AGENTS.md absent
(ADR-53); ARCHITECTURE present at root (ADR-51 universal + A3); BACKLOG present;
`adr38_baseline` + `vision_md` + `claude_md` audit checks PASS; mandatory root
file set complete; naming compliant apart from legacy `docs/archive/` (CM-CF9).

## Conformance estimate vs current baseline

**Baseline (2026-05-23) stated ~80%** against the standard *as the baseline
applied it that day* — but the baseline did **not** apply the ADR-33/ADR-40
tier-deprecation amendments (same-day) and predates root-hygiene pass-2
(2026-05-24).

**Against the current (2026-05-26) standard: ~72%.** The ~8-point drop is not
regression in corp-monorepo (its relevant files never moved) — it is the
**standard the baseline didn't count**: tier-residue surfaced as two new MEDIUM
findings (CM-D1, CM-D2), and root-hygiene pass-2 added three LOW findings (CM-D3,
CM-D4, CM-D5). Rationale for ~72% rather than lower: the structural baseline is
intact (all mandatory files present + placed, audit checks PASS, CHANGELOG and
AGENTS.md correctly absent); the debt is concentrated in **one artifact**
(ARCHITECTURE.md — four of the four HIGH/near-HIGH items) plus frontmatter/prose
residue and doc-quality polish, none CRITICAL.

**Two-speed conformance.** Audit-tool level: **3 PASS** (near-green). Full
standard: **~72%**. The tool sees none of the 17 findings — tier-residue,
template form, codemap form, README disposition, root-hygiene, and naming are all
below its resolution. Tool-green must not be read as standard-conformant.

---

**Contract preserved:** zero `corp-monorepo/` files modified (read-only per
ADR-28/ADR-36). All writes confined to `.dev-knowledge/docs/audits/`.
