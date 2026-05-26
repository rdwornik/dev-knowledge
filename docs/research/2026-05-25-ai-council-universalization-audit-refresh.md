---
type: audit-refresh
scope: ai-council universalization vs .dev-knowledge baseline current state
date: 2026-05-25
basis: docs/audits/2026-05-23-ai-council-deep-audit.md (baseline) + standards merged 2026-05-23 → 2026-05-25
status: research artifact (input to execution plan)
contract: read-only on ai-council (Layer-2 invariant); writes confined to .dev-knowledge/docs/research/
---

# AI Council Universalization Audit Refresh — 2026-05-25

## Methodology

This is a **delta refresh**, not a re-audit. The 2026-05-23 ai-council deep audit
(`docs/audits/2026-05-23-ai-council-deep-audit.md`) is the baseline; this document
(a) re-checks the status of every baseline finding at the current ai-council HEAD,
and (b) surfaces NEW gaps created by `.dev-knowledge` standards that changed *after*
that audit. Every claim cites an ai-council `file:line` or a verified file-state fact
(read-only inspection; no ai-council file was modified, per the ADR-28/ADR-36 Layer-2
contract).

**Pivotal fact — ai-council HEAD is unchanged since the baseline audit.** The
2026-05-23 deep audit targeted HEAD `2a980ab` (2026-05-19). ai-council's current
HEAD is **still `2a980ab`** (`git -C ai-council log --oneline -1` → `2a980ab docs:
merge chunk4 — retire AGENTS.md…`). No ai-council commit has landed since the
baseline. **Consequence:** all seven baseline findings carry forward *verbatim* (none
could have been closed by ai-council work — there was none), and the entire delta in
this refresh comes from `.dev-knowledge` **standards** moving, not from ai-council
moving.

**Standards inventoried as the current basis** (read end-to-end for this refresh):

| Standard | Change | Date | Effect on ai-council |
|---|---|---|---|
| ADR-38 amendment A5 | Universal baseline; tier system deprecated; README deprecated; CHANGELOG struck; ARCHITECTURE universal | 2026-05-23 | New baseline; README now optional |
| ADR-33 amendment | VISION frontmatter: `tier`/`scale` removed; required keys `version`/`last_reviewed`/`owner`/`status` | 2026-05-23 | VISION carries residue + missing `status` |
| ADR-40 | DEPRECATED — tier algorithm retired | 2026-05-23 | All `Scale: M` declarations are residue |
| ADR-51 amendment | ARCHITECTURE.md mandatory universally (was M+L) | 2026-05-23 | ai-council already has one (conforms) |
| ADR-49 | CHANGELOG retired ecosystem-wide | 2026-05-17 | ai-council already CHANGELOG-free (conforms) |
| ADR-45 amendment | Supersession claim withdrawn; ADR-42 v3.2 / HANDOFF_PROCESS v3.3.3 canonical | 2026-05-25 | No gap — see below |
| PLAYBOOK Root hygiene (v1.0 2026-05-23 + pass-2 v1.1 2026-05-24) | Consolidate configs into pyproject; dot-prefix `.code-workspace`; do-not-create `.env.example` | 2026-05-23/24 | 2 new root-hygiene gaps |
| `templates/ARCHITECTURE-template.md` | `[CORE]`-only section tags; `scale`-free frontmatter; Mermaid codemap default | current | `scale:` + `[L-opt]` tags now residue |
| `scripts/audit.py` `check_vision_md` / `check_adr38_baseline` | governance-file baseline; required VISION keys include `status` | current | drives the `vision_md` WARN |

**Correction to a premise carried into this prompt.** The prompt's discovery note
recalled the baseline as "5 active (2 MEDIUM, 3 LOW)." The baseline §5 actually records
**7 active findings: 0 CRITICAL / 0 HIGH / 2 MEDIUM / 5 LOW**. This refresh uses the
correct count (7).

**Audit-tool note (read-only determination).** Running `scripts/audit.py repo ai-council`
in write mode would create files under `ecosystem/` and `docs/audits/` — outside this
prompt's `docs/research/`-only write contract — so it was **not** run. The three check
outcomes were determined statically by reading ai-council's files against the current
`audit.py` source. The committed `ecosystem/ai-council/state.yaml` (last_audit 2026-05-23)
records `vision_md: pass`, but that row is **stale**: it was written under the
pre-amendment check (frontmatter keys `[last_reviewed, owner, scale, tier, version]`,
no `status` required). The current `check_vision_md` requires `status`, so a re-run
today yields **WARN** (see AR-D1).

---

## Baseline carry-forward (from the 2026-05-23 ai-council deep audit)

All seven baseline findings are **STILL OPEN** at HEAD `2a980ab` (verified file-state,
not inferred). The 2026-05-23 audit had already closed all ten 2026-05-11 findings;
those remain closed and are not re-listed.

| Baseline ID | Sev | Finding | Status now | Evidence (current file-state) |
|---|---|---|---|---|
| A1 | MEDIUM | Codemap in transitional ASCII form + false "Open item" note | STILL OPEN | `ai-council/ARCHITECTURE.md:21` note verbatim; `:23` opens a plain ```` ``` ```` ASCII tree, not ```` ```mermaid ```` |
| A2 | LOW | Layer model rendered as prose+table, not inline Mermaid | STILL OPEN | `ai-council/ARCHITECTURE.md` Layer Boundaries section (no `mermaid` fence) |
| B | MEDIUM | Two docs prescribe underscore ADR naming "per ADR-34" (opposite of ADR-34); ADR-08 symptom | STILL OPEN | `ai-council/CLAUDE.md:32` (`ADR-NN_topic.md`); `ai-council/docs/decisions/README.md:3` ("underscore naming per ADR-34"); `ai-council/docs/decisions/ADR-08_research-degradation-alarm.md` (underscore filename) |
| D | LOW | BACKLOG header cites superseded ADR-41 schema, not ADR-47 | STILL OPEN | `ai-council/BACKLOG.md:3` `<!-- schema: ADR-41 \| grooming: … -->` |
| F1 | LOW | README test count stale (362) | STILL OPEN (now disposition-gated — see AR-D5) | `ai-council/README.md:234` "362 unit tests"; actual `def test_` count = **405** |
| F2 | LOW | README self-contradicts on default synthesizer | STILL OPEN (disposition-gated) | `ai-council/README.md:152` table default `claude` vs `:175` "default synthesizer is **Gemini**" |
| F3 | LOW | README "Related repos" lists obsolete repo names | STILL OPEN (disposition-gated) | `ai-council/README.md:294-298` (corp-by-os / corp-os-meta / corp-knowledge-extractor / corp-rfp-agent) |

**Re-contextualization of F1/F2/F3 by the new standard.** At baseline these were
"fix the README" items. ADR-38 A5 (2026-05-23) deprecated README from the mandatory
baseline (now optional, external-audience only). They are therefore now **gated on the
README disposition decision** (AR-D5): if the README is deleted, F1/F2/F3 are moot; if
it is kept (ai-council's README reads as external/product copy — plausibly
open-source-facing), they must be fixed. No baseline finding was *closed* by a standards
change; three were re-scoped.

---

## Delta gaps — standards changes 2026-05-23 → 2026-05-25 vs ai-council current state

### Standard: README.md deprecated (ADR-38 Amendment A5, 2026-05-23)
- **ai-council current:** `README.md` present at root (`git ls-files` → `README.md`). Content is external-audience/product prose ("You have a hard architectural decision to make…", `README.md:3`).
- **Gap:** YES — **AR-D5 [MEDIUM]**. README is now OPTIONAL (external-audience repos only). ai-council needs an explicit keep/delete decision rather than silent retention; this decision *gates* F1/F2/F3. `.dev-knowledge` itself deleted its root README under this amendment.
- **Evidence:** `README.md` present; ADR-38 A5 post-2026-05-23 baseline table (README = OPTIONAL).

### Standard: VISION frontmatter — no tier/scale, must carry `status` (ADR-33 Amendment, 2026-05-23)
- **ai-council current:** `VISION.md:1-7` frontmatter = `version: "1.0"`, `tier: M`, `owner: rob`, `last_reviewed: "2026-05-12"`, `scale: M`. **No `status` key.**
- **Gap:** YES — **AR-D1 [MEDIUM]**. Two faults: (1) deprecated `tier: M` + `scale: M` residue (ADR-33 amendment removed both); (2) missing required `status` key. The amended `check_vision_md` requires `{version, last_reviewed, owner, status}` → **WARN: missing keys ['status']**. This is the exact WARN the BACKLOG P1 item "Apply tier-deprecation to ai-council" names.
- **Evidence:** `ai-council/VISION.md:1-7`; `scripts/audit.py:155` required-key set.

### Standard: ARCHITECTURE.md mandatory universally + Mermaid codemap (ADR-51 Amendment 2026-05-23 + 2026-05-22)
- **ai-council current:** `ARCHITECTURE.md` present at root; CORE sections complete; CODEMAP markers present. Frontmatter `ARCHITECTURE.md:2` carries `scale: M`. Section tags include seven `[L-opt]` tags (`:99,:125,:136,:154,:170,:184,:202`). Codemap is transitional ASCII (A1).
- **Gap:** Presence CONFORMS (mandatory-universal satisfied). But two residue gaps:
  - **AR-D2 [LOW]:** `scale: M` in frontmatter — the current `templates/ARCHITECTURE-template.md` frontmatter is `last_reviewed`/`status`/`owner` only (no `scale`). The `.dev-knowledge` reference `ARCHITECTURE.md` dropped `scale:` on 2026-05-24.
  - **AR-D3 [LOW]:** seven `[L-opt]` section tags — the current template uses **only `[CORE]`**; non-core sections carry *no* tag and are kept/deleted by judgment. `[L-opt]` is tier-residue (the "L" is a deprecated scale letter).
- **Evidence:** `ai-council/ARCHITECTURE.md:2`, `:99,125,136,154,170,184,202`; `templates/ARCHITECTURE-template.md:1-5,20`.

### Standard: tier system deprecated — no `Scale:` prose (ADR-40 deprecated; ADR-38 A5; ADR-33 amendment)
- **ai-council current:** `CLAUDE.md` carries tier-conditional prose in three places: `:20` "**Scale:** `M` (per … PLAYBOOK Project Scale Tiers)"; `:28` "required at Scale M+, per ADR-51"; `:129` "ADR-51: ARCHITECTURE.md convention (Scale M+)".
- **Gap:** YES — **AR-D4 [MEDIUM]**. The tier system is deprecated ecosystem-wide; "Project Scale Tiers" no longer exists as a live PLAYBOOK construct, and ADR-51 is now universal (not "M+"). **Note:** the BACKLOG P1 item names only VISION + ARCHITECTURE *frontmatter*; CLAUDE.md prose is an under-specified addition this refresh surfaces.
- **Evidence:** `ai-council/CLAUDE.md:20,28,129`.

### Standard: CHANGELOG retired (ADR-49)
- **ai-council current:** No `CHANGELOG.md` (`git ls-files` confirms absent). `CLAUDE.md:109` explicitly forbids recreating it.
- **Gap:** **NO — CONFORMS.** (Carried over from baseline; the un-amended ADR-38 table row was the upstream `.dev-knowledge` inconsistency, §7 #1 of the baseline, not an ai-council gap.)

### Standard: dot-prefix workspace + config consolidation + no `.env.example` (PLAYBOOK Root hygiene, 2026-05-23 / pass-2 2026-05-24)
- **ai-council current:**
  - Tool configs: **consolidated** — `pyproject.toml` carries `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.ruff.format]`, `[tool.pytest.ini_options]`, `[tool.mypy]`, `[tool.coverage.*]`. No standalone `ruff.toml`/`pytest.ini`/`mypy.ini`/`tach.toml` at root. **CONFORMS.**
  - Workspace file: `ai-council.code-workspace` present at root, **not dot-prefixed**.
  - `.env.example` present at root.
- **Gaps:**
  - **AR-D6 [LOW]:** `.env.example` present — pass-2 rule "**`.env.example` policy: do not create**" (PLAYBOOK:227). Env-var docs belong in CLAUDE.md/VISION.
  - **AR-D7 [LOW]:** `ai-council.code-workspace` should be `.ai-council.code-workspace` (PLAYBOOK:211 dot-prefix rule).
- **Evidence:** `pyproject.toml:38,54,60,64,67`; root `ai-council.code-workspace`, `.env.example`; `protocols/PLAYBOOK.md:211,227`.

### Standard: ADR-45 supersession claim withdrawn (ADR-45 Amendment 2026-05-25)
- **ai-council current:** No ai-council *governance* doc claims ADR-45 superseded anything. The only ADR-45 references are in untracked `council_inbox/2026-05-25-*` working files (inputs to the *current* `.dev-knowledge` Council debate, not ai-council governance), and they already state the withdrawal correctly.
- **Gap:** **NO.** Listed for completeness per the discovery target.

### Standard: governance-docs-only audit baseline (`scripts/audit.py`)
- **ai-council current (determined statically; tool not run in write mode):**
  - `check_vision_md` → **WARN** (missing `status`; tier/scale present but ignored) = AR-D1.
  - `check_adr38_baseline` → **PASS** (VISION + ARCHITECTURE + BACKLOG all present).
  - `check_claude_md` → **PASS** (present, non-empty).
- **Gap:** the single WARN is AR-D1. **Resolution-of-the-tool caveat:** the audit tool checks only file presence + four VISION keys + CLAUDE non-emptiness. It does **not** detect tier-residue prose, `[L-opt]` tags, root-hygiene, README disposition, codemap form, or naming. So "audit-tool green-ish" (2 PASS + 1 WARN) substantially **overstates** full-standard conformance — most gaps in this refresh are below the tool's resolution.

### Standard: canonical files at root, correct set (ADR-38 A5 post-amendment baseline)
- **Required (universal):** VISION ✓, CLAUDE ✓, ARCHITECTURE ✓, BACKLOG ✓. README OPTIONAL (present — AR-D5). CHANGELOG removed (absent ✓).
- **Repo-specific present:** JOURNAL ✓, LESSONS ✓. CONTRIBUTING absent (not in universal baseline — not a gap).
- **Gap:** none on *presence* beyond the README disposition (AR-D5). The mandatory set is complete.

---

## Operator-stated concerns — mapping to ai-council state

### Concern: "metodologia pracy z diagramami, architecture, backlog, cloud, journal, lessons, vision, bez readme, z kropkami na workspace, w odpowiedniej kolejności"
- **Current state:** ARCHITECTURE/BACKLOG/JOURNAL/LESSONS/VISION all present at root. README **still present** (concern says "bez readme") → AR-D5. Workspace file **not** dot-prefixed ("z kropkami na workspace") → AR-D7. "diagrams" → the codemap is still ASCII, not the Mermaid default (A1/A2). "cloud" has no current ai-council artifact (no `cloud`-named file/dir tracked) — read as an aspiration for a future canonical surface, not an existing gap.
- **Gap:** README disposition (AR-D5) + workspace dot-prefix (AR-D7) + Mermaid codemap (A1/A2) are the concrete items this concern maps to.

### Concern: workspace template tier-residue (operator flagged "jeden complex workspace template, scale-adaptive content, NOT scale-different templates")
- **Verification (done):** `ai-council.code-workspace` is a flat single-folder settings JSON bootstrapped from the **medium-richness** template (extension set `ms-python.python`, `charliermarsh.ruff`, `eamodio.gitlens`, `usernamehw.errorlens`, `gruntfuggly.todo-tree` = the PLAYBOOK "medium repos" set). **It carries no tier-conditional content inside the file** — there is no `tier:`/`scale:` marker to remove.
- **Gap:** The tier-residue the operator flagged lives in the **`.dev-knowledge` template framework** (three separate `templates/workspace-{S,M,L}.code-workspace` files; PLAYBOOK §VS Code workspace:418 still says "pick the one matching the repo's complexity"). That is a `.dev-knowledge` *standards* concern and is **out of scope** for this rollout (methodology codification — see the execution plan's exclusions). For ai-council specifically, the only workspace action is the dot-prefix (AR-D7), plus optional convergence to the `.dev-knowledge.code-workspace` pattern (multi-root, `compactFolders: false`, canonical-file open tasks) — optional, not a gap.

### Concern: "robimy najbardziej złożony możliwy szablon i go dopasowujemy i wybieramy elementy w zależności od skali projektu" (one maximal template, select elements by complexity)
- **Implication:** ai-council's ARCHITECTURE.md should match the single canonical template, completing CORE sections and keeping/deleting the rest by judgment — **not** by a tier-keyed `[L-opt]` tag.
- **Current divergence:** ARCHITECTURE.md uses `[L-opt]` tags on seven sections (AR-D3) — the *old* tier-keyed selection model. The element-selection model the operator describes is exactly the current template's `[CORE]`-only convention: convert `[L-opt]` → untagged (kept by judgment) and remove the `scale:` frontmatter (AR-D2). No new sections need adding; the sections present are appropriate for ai-council's complexity.

---

## Findings summary table

Severity scale per baseline: CRITICAL · HIGH · MEDIUM (real, deferrable) · LOW (polish).

| ID | Source | Sev | Category | Evidence (ai-council) | Status |
|---|---|---|---|---|---|
| AR-CF1 | Baseline A1 | MEDIUM | Architecture/codemap | `ARCHITECTURE.md:21`,`:23` | open (carry-forward) |
| AR-CF2 | Baseline A2 | LOW | Architecture/visual | `ARCHITECTURE.md` layer section | open (carry-forward) |
| AR-CF3 | Baseline B | MEDIUM | Naming | `CLAUDE.md:32`; `docs/decisions/README.md:3`; `ADR-08_research-degradation-alarm.md` | open (carry-forward) |
| AR-CF4 | Baseline D | LOW | BACKLOG | `BACKLOG.md:3` | open (carry-forward) |
| AR-CF5 | Baseline F1 | LOW | Doc quality | `README.md:234` (362 vs 405) | open — disposition-gated (AR-D5) |
| AR-CF6 | Baseline F2 | LOW | Doc quality | `README.md:152` vs `:175` | open — disposition-gated (AR-D5) |
| AR-CF7 | Baseline F3 | LOW | Doc quality | `README.md:294-298` | open — disposition-gated (AR-D5) |
| AR-D1 | Delta (ADR-33 Am.) | MEDIUM | Frontmatter/audit | `VISION.md:1-7` (tier/scale residue + missing `status`) | gap → `vision_md` WARN |
| AR-D2 | Delta (ADR-51/template) | LOW | Frontmatter | `ARCHITECTURE.md:2` (`scale: M`) | gap |
| AR-D3 | Delta (template) | LOW | Section tags | `ARCHITECTURE.md:99,125,136,154,170,184,202` (`[L-opt]`) | gap |
| AR-D4 | Delta (ADR-40 deprec.) | MEDIUM | Tier-residue prose | `CLAUDE.md:20,28,129` | gap |
| AR-D5 | Delta (ADR-38 A5) | MEDIUM | README disposition | `README.md` present (external-audience) | decision required |
| AR-D6 | Delta (Root hygiene pass-2) | LOW | Root hygiene | `.env.example` present | gap |
| AR-D7 | Delta (Root hygiene) | LOW | Root hygiene | `ai-council.code-workspace` (no dot) | gap |

**Distribution:** 0 CRITICAL · 0 HIGH · **5 MEDIUM** (AR-CF1, AR-CF3, AR-D1, AR-D4, AR-D5) · **9 LOW** · **14 total** (7 carry-forward + 7 delta).

**Explicit CONFORMS (no action):** CHANGELOG absent (ADR-49); ARCHITECTURE present at root (ADR-51 universal + A3); tool configs consolidated in `pyproject.toml` (root hygiene); `adr38_baseline` + `claude_md` audit checks PASS; no stale ADR-45 supersession claim in ai-council governance; mandatory root file set complete.

---

## Conformance estimate vs current baseline

**Baseline (2026-05-23) stated ~90%** against the standard *as it stood that day*.

**Against the current (2026-05-25) standard: ~70%.** The drop is not regression in
ai-council (its HEAD never moved) — it is the **standard moving underneath a frozen
repo**. Three documents (VISION, ARCHITECTURE, CLAUDE) now carry tier-residue that did
not exist as a defect on 2026-05-22; README flipped from mandatory-and-buggy to
optional-and-undecided; and root-hygiene pass-2 added two new conventions ai-council
predates. Rationale for ~70% rather than lower: the structural baseline is intact
(all mandatory files present and correctly placed, configs consolidated, CHANGELOG
correctly absent, audit `adr38_baseline`/`claude_md` PASS); the debt is concentrated in
frontmatter/prose residue and polish, none CRITICAL or HIGH.

**Two-speed conformance — important for interpretation.** At the **audit-tool** level
ai-council is near-green (2 PASS + 1 WARN). At the **full-standard** level it is ~70%.
The gap between the two numbers is itself a finding: the audit tool does not see
tier-residue, root-hygiene, README disposition, codemap form, or naming, so tool-green
must not be read as standard-conformant. The execution plan closes the full-standard
gap; the audit tool will confirm only the `vision_md` WARN's resolution.

---

**Contract preserved:** zero `ai-council/` files modified (read-only per ADR-28/ADR-36).
All writes confined to `.dev-knowledge/docs/research/`.
