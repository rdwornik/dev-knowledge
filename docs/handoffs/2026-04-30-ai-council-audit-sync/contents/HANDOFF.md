# Handoff — ai-council audit sync (2026-04-30)

**Type:** audit handoff (STRONG enforcement)
**Format:** ADR-37 two-phase overlay on ADR-32 v2.0
**Source:** .dev-knowledge browser session, 2026-04-30
**Target:** ai-council browser-2 session

---

## Current State

**Verified at handoff generation:**
- ai-council HEAD: `c821157fcfa957bc6612c74667d70c8c9a88ef5c`
- ai-council branch: `main`
- ai-council working tree: clean (no uncommitted changes)

**MUST verify before acting (per ADR-37 STRONG enforcement):**
1. `git rev-parse HEAD` in ai-council MUST return `c821157fcfa957bc6612c74667d70c8c9a88ef5c`
2. `git status --porcelain` MUST be empty
3. If either check fails, STOP and report drift to Rob — do not proceed

**Architectural state:**
- ADR-38 compliance achieved (5/5 checks pass) via 5-commit migration
  earlier today. `src/ai_council/` package namespace established,
  `[build-system]` added to pyproject.toml, pytest config consolidated.
- 310 unit tests pass (baseline maintained through migration).
- `council` CLI works, package installs editable.

**Audit findings (8 total):**
- 2 P1 actionable (tier-independent): F-01 VISION.md, F-02 lessons config
- 2 P2 DEFERRED (tier-dependent): F-03 BACKLOG.md, F-04 ARCHITECTURE.md
- 3 P3 informational: F-05 ADR naming, F-06 test count, F-07 module count
- 1 calibration concern: F-08 ADR-40 algorithm (ecosystem-wide)

**Tier classification (transparent):**
- Per current ADR-40: tier=L (score 0.0, clamped from -9.0 raw)
- Calibration concern: all ecosystem repos clamp to L. Algorithm
  not differentiating. Recalibration DEFERRED to audit tool P1
  multi-repo data collection.
- L-specific obligations (BACKLOG.md, ARCHITECTURE.md) DEFERRED
  pending calibration.

For full findings, see `audit-report.md` in this handoff folder.

---

## Future State

**Browser-2 priority actions (in order):**

### Action 1: F-01 — Create ai-council VISION.md (P1, tier-independent)

Create `ai-council/VISION.md` per ADR-33 universalization schema.

**Frontmatter:**
```yaml
---
version: 1.0
tier: M          # NOTE: per current ADR-40 algorithm tier is L,
                 # but calibration concern flagged. Use M as practical
                 # working classification; revise post-calibration.
                 # Flag for Rob review if uncertain.
owner: rob
last_reviewed: 2026-04-30
scale: M
---
```

**Required sections (per ADR-33):**
- Mission — what ai-council is for
- Scope — what's in/out
- Methodology — how work happens
- Lifecycle — when/how repo evolves, audit posture
- Relationships — cross-repo dependencies (especially
  .dev-knowledge governance)

Reference ADR-33 in this handoff folder for full schema details.

**Verification after creation:**
- File parseable as YAML frontmatter + markdown
- Sections match ADR-33 mandate
- `git status` shows new VISION.md staged

### Action 2: F-02 — Configure lessons discovery (P1, tier-independent)

Update `ai-council/CLAUDE.md` to reference `DEV_KNOWLEDGE_PATH` env var
per ADR-35.

**Specific edits:**
1. Add section or update existing "Environment" section in CLAUDE.md
   noting:
   ```
   ## Lessons Discovery (per .dev-knowledge ADR-35)

   The DEV_KNOWLEDGE_PATH environment variable should point to the
   `.dev-knowledge` repository for cross-repo lessons retrieval.

   On Windows: set in PowerShell `$PROFILE` to
   `C:\Users\1028120\Documents\Dev\.dev-knowledge`.

   Note: ADR-35 P1 implementation (lessons-index.json + retrieval
   tooling) pending in .dev-knowledge. Configuration documented now;
   functionality activates post-implementation.
   ```

2. Optional: consider whether `ai-council/tasks/lessons.md` (project-
   local lessons) should be migrated/merged into .dev-knowledge
   LESSONS.md, OR remain ai-council-local. Flag for Rob; do not
   silently migrate.

Reference ADR-35 in this handoff folder.

### Actions DEFERRED (do not execute):

- F-03 BACKLOG.md creation — DEFER pending ADR-40 calibration
- F-04 ARCHITECTURE.md creation — DEFER pending ADR-40 calibration
- F-08 ADR-40 calibration — separate work item in .dev-knowledge BACKLOG

### Informational (no action required):

- F-05 ADR naming kebab-case — grandfathered per ADR-29; future ADRs
  should use ADR-NN_topic_with_underscores.md convention
- F-06 test count discrepancy — ADR-38 already specifies pytest
  collect-only as canonical method; manual grep was approximation
- F-07 module count vs package-level files — ADR-38 module definition
  correctly excludes package-level files; surfaced for ADR amendment
  research in .dev-knowledge BACKLOG

### Session closure (browser-2):

After completing F-01 and F-02:
1. Run ai-council pytest to verify nothing broke
2. Update ai-council CHANGELOG.md, JOURNAL.md
3. Generate session handoff for next ai-council session (per ADR-32 +
   ADR-37 two-phase format if .dev-knowledge templates updated; else
   v2.0 ADR-32 format with note that v3.0 update is P1 in
   .dev-knowledge BACKLOG)
4. Report to Rob: actions completed, any blockers, next session
   recommendations

---

## Detailed Context (per ADR-32 9-section structure)

### 1. Charter recap

ai-council is a CLI multi-model debate system in the .dev-knowledge
ecosystem. Phase 1 governance (ratified 2026-04-28 through 2026-04-30
in .dev-knowledge) established 9 ADRs covering universal architecture,
file lifecycle, scale tier evaluation, audit tool architecture,
session boundary protocol, and cross-session backlog architecture.

ai-council is in immediate Phase 2 universalization cohort per ADR-33.
This audit handoff is the first per-repo application of Phase 1
governance.

### 2. Decisions made (this audit cycle)

- ADR-38 structural compliance migration (5 commits, validated 5/5
  checks). Decision: migrate now, before tier classification audit.
- Path 3 strategy for calibration concern: continue audit cycle with
  current algorithm classification, defer recalibration to audit tool
  P1 multi-repo data.
- Tier-independent findings (F-01, F-02) actionable now; tier-
  dependent (F-03, F-04) deferred.

### 3. Work completed (this audit cycle)

- Faza A1 discovery (pre-migration ai-council state)
- ADR-38 compliance migration (browser-2 architect designed prompt;
  Claude Code in ai-council executed 5 commits)
- Faza A1 re-discovery (post-migration state)
- Faza A2 findings report (this handoff folder cites)
- Faza A3 handoff folder generation (this artifact)

### 4. Pending — see .dev-knowledge BACKLOG.md

Per ADR-41 + ADR-37 integration: pending items live in `.dev-knowledge
BACKLOG.md`, not duplicated here. Cross-stream "Phase 1 validation"
P1 item tracks this audit cycle. ai-council-specific items emerging
from this handoff (after browser-2 completes F-01/F-02): contribute
to .dev-knowledge BACKLOG "Stream B: ai-council" section OR ai-council
own BACKLOG.md if calibration confirms M+ tier.

### 5. Risks / blockers

- ADR-40 calibration: all repos classify L. Recalibration deferred.
  Risk: heavy L-mandates would burden ai-council if applied without
  calibration. MITIGATED: F-03/F-04 deferred in this handoff.
- ai-council `tasks/lessons.md` vs .dev-knowledge LESSONS.md
  unification: open question, flag for Rob, do not silently migrate.
- VISION.md tier value (M vs L): manual judgment required if
  calibration uncertainty matters to repo owner.

### 6. Environment / setup notes

ai-council post-migration:
- Python package: `ai_council` at `src/ai_council/`
- Editable install: `pip install -e .`
- CLI entry: `council` (and `ai-council`) → `ai_council.cli:main`
- Tests: `pytest -x --tb=short`
- Lint: `ruff check src/ tests/`
- Type: `mypy src/`

Pre-existing issues (NOT new from migration):
- 17 ruff errors (pre-existing, verified)
- 4 mypy errors in 2 files (identical to main, verified)

### 7. References

- All ADRs in `relevant-decisions/` folder of this handoff
- Audit report: `audit-report.md` in this handoff
- .dev-knowledge repo: `C:/Users/1028120/Documents/Dev/.dev-knowledge`
- ai-council repo: `C:/Users/1028120/Documents/Dev/ai-council`

### 8. Notes for next session (after F-01 + F-02 complete)

- Phase 1 validation cycle complete from `.dev-knowledge` side
- Next ai-council work likely: VISION.md content refinement, lessons
  unification decision, await calibration outcome for F-03/F-04
- Or: address pre-existing ruff/mypy errors (out of audit scope)

### 9. Open questions

- Should ai-council `tasks/lessons.md` merge into .dev-knowledge
  LESSONS.md or stay ai-council-local? (Rob decision)
- VISION.md tier value: declare M based on intuitive judgment (calibration
  pending) or L per current algorithm? (Rob decision)
- Post-VISION.md creation, does ai-council Phase 2 universalization
  cohort work begin or pause for calibration? (Rob decision)

---

**End of HANDOFF.md.**

Browser-2: see `relevant-decisions/` for ADR full texts, `audit-report.md`
for findings detail, `manifest.json` for machine-readable summary, and
`tree.txt` for ai-council file inventory at handoff generation.
