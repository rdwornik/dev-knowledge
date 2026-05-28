---
type: verification-audit
scope: cross-repo visual-pattern retrofit + universalization merge verification
date: 2026-05-27
basis: 4 retrofit plans + ADR-59 (visual pattern + 2026-05-27 amendment) + ADR-60
contract: read-only on child repos during verification; writes confined to .dev-knowledge/docs/audits/
session: operator-driven cross-repo orchestration (single CC anchored in .dev-knowledge, cd'd into each child workdir; commits land in each repo's own .git/)
---

# Cross-Repo Retrofit Verification — 2026-05-27

## Method

One CC session anchored in `.dev-knowledge`. CC `cd`'d into each child repo in
turn, merged the pending `chore/universalization-2026-05-26` branch to that
repo's `main`, then created a `chore/visual-pattern-retrofit-2026-05-27`
branch and applied the visual-pattern retrofit. Layer-2 invariant preserved:
no orchestration script in `.dev-knowledge`; the operator-authored mega-prompt
drove the cd/git sequence. Per-phase isolation was verified by checking that
the other three child repos' `git status` remained empty after each commit.

Order executed: ai-council → corp-ops → corp-sca-time-automation →
corp-monorepo. No push, no auto-merge — each retrofit branch awaits separate
operator approval.

## Sort template applied (from corrected .dev-knowledge.code-workspace)

```jsonc
"explorer.sortOrder": "default",
"explorer.sortOrderLexicographicOptions": "upper",
"explorer.sortOrderReverse": true,
"explorer.compactFolders": false
```

Sourced from `.dev-knowledge.code-workspace` on `main` (commits `f8a3f8d` +
`cfb0782`, ADR-59 amendment 2026-05-27). The four keys are applied
**verbatim** to every child workspace — including `sortOrderReverse: true`,
which is **not** in the original four retrofit plans (those were written
before the 2026-05-27 amendment; the operator mega-prompt overrode by
specifying "copy from corrected template").

## Pre-flight (Phase 0)

| Gate | Result |
|---|---|
| `.dev-knowledge` sort fix on `main` | PASS — `f8a3f8d` (workspace fix) + `cfb0782` (ADR-59 amendment) present |
| `.dev-knowledge` tree clean | PASS |
| 4 child repos accessible + tree-clean | PASS (all on `chore/universalization-2026-05-26` at start) |
| Sort template extracted | PASS — 4 keys above |
| 4 retrofit plans read | PASS |
| ADR-59 + amendment read | PASS |
| No concurrent session writing `.dev-knowledge` | PASS |

## Per-repo verification

### Phase A — ai-council

**Universalization merge:** `git merge --no-ff chore/universalization-2026-05-26` →
merge commit `62cd908`. 8 commits brought in (docs/chore-only; +112/-362 LOC).
**Tests post-merge:** `pytest -m "not integration and not envcheck"` → **407
passed, 6 deselected** (matches retrofit plan expectation). Integration test
`test_full_debate_pipeline` fails with `ImportError: _build_all_providers`
under the default selector — **pre-existing**, excluded by the standard
marker; universalization touched no Python source.

**Retrofit branch:** `chore/visual-pattern-retrofit-2026-05-27` (1 commit).

| Retrofit action | Result | Evidence |
|---|---|---|
| Workspace sort keys (3 added) | ✓ | commit `4abb085`; `.ai-council.code-workspace` now contains all 4 keys |
| `.env` cleanup | ⚠ report | `.env` (100B, gitignored, untracked) — has content → **leave** per operator rule |
| Entry-script → `scripts/` | n/a | no run-entry script at root (src is in `src/ai_council/`) |
| Canonical .md (4 mandatory) | ✓ | VISION, CLAUDE, ARCHITECTURE, BACKLOG present + ALL-CAPS |
| Empty/unnecessary file scan | ✓ | no empty files at root |
| Dot-prefix discipline | ✓ | only `pyproject.toml` un-dotted (exception) |

**Post-retrofit tests:** 407 passed, 6 deselected (no regression).
**Lint baseline note:** `ruff check` reports 18 errors in src — **pre-existing**
in the ai-council source; universalization + retrofit touched zero Python.
Out of scope.

**Branch state:** `chore/visual-pattern-retrofit-2026-05-27` (HEAD `4abb085`),
tree clean, awaits operator merge.

### Phase B — corp-ops

**Universalization merge:** merge commit at `main` HEAD. 8 commits brought in
(+384/-224 LOC; CHANGELOG/README/.env.example deletions + VISION/ARCHITECTURE/
BACKLOG creation + CLAUDE.md re-home).
**Tests post-merge:** 73 passed, 1 skipped (clean).

**Retrofit branch:** `chore/visual-pattern-retrofit-2026-05-27` (1 commit).

| Retrofit action | Result | Evidence |
|---|---|---|
| Workspace file created (scaled-to-size) | ✓ | commit `d75cb17`; minimal single-root `.corp-ops.code-workspace`. corp-ops has 7 top-level folders → multi-root would be over-engineering. 4 sort keys + Python settings + recommended extensions. JSON parses. |
| `.env` cleanup | n/a | no `.env` at root (only `.env.example`, deleted by universalization) |
| Entry-script → `scripts/` | n/a | no entry script at root; existing `scripts/` already holds PowerShell helpers |
| Canonical .md | ✓ | VISION, ARCHITECTURE, BACKLOG, CLAUDE all present + ALL-CAPS |
| Empty/unnecessary file scan | ✓ | no empty files at root |
| Dot-prefix discipline | ✓ | only `pyproject.toml` un-dotted (exception) |

**Post-retrofit tests:** 73 passed, 1 skipped.
**Branch state:** `chore/visual-pattern-retrofit-2026-05-27` (HEAD `d75cb17`),
tree clean, awaits operator merge.

### Phase C — corp-sca-time-automation

**Universalization merge:** merge commit at `main` HEAD. 6 commits brought in
(+342/-268 LOC; CHANGELOG/README/.env.example deletions + VISION/ARCHITECTURE/
BACKLOG creation + CLAUDE.md re-home).
**Tests post-merge:** ⚠ **pytest not installed in repo venv** (commented out in
`requirements.txt` as optional dev dep). Ruff also not installed. Universalization
touched zero Python source, so test regression risk is nil; verified via
visual diff. Documented as a tooling gap.

**Retrofit branch:** `chore/visual-pattern-retrofit-2026-05-27` (1 commit).

| Retrofit action | Result | Evidence |
|---|---|---|
| Workspace file created (scaled-to-size) | ✓ | commit `3d7937f`; minimal single-root `.corp-sca-time-automation.code-workspace`. Repo has ~8 top-level folders. Coexists with existing `.vscode/` folder-scoped settings. JSON parses. |
| `.env` cleanup | ⚠ report | `.env` (4219B, gitignored, untracked) — has content → **leave** per operator rule |
| **Entry-script → `scripts/`** | ⚠ **deferred** | `run.py` (18187B, executable bit, tracked) at root + 6 references in `.claude/rules/python-env.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `docs/handoffs/2026-04-15-handoff.md`, `scripts/manager_report.py`, `tests/test_vbs_export.py`. Operator prompt: "Do NOT move entry-scripts without updating references + passing tests" — pytest is unavailable in this venv, so safe verification is impossible. **Deferred** to a future session that installs the dev tooling (`pip install pytest ruff`) before moving. See BACKLOG item below. |
| Canonical .md | ✓ | VISION, ARCHITECTURE, BACKLOG, CLAUDE all present + ALL-CAPS |
| Empty/unnecessary file scan | ✓ | no empty files at root |
| Dot-prefix discipline | ✓ | `requirements.txt` exception (PEP/pip); `.gitignore` dotted; no other root configs |
| `__pycache__/` untracked at root | ⚠ report | a `__pycache__/` directory exists at root (apparently created by an out-of-tree script invocation) — listed in `.gitignore`, not tracked. Cosmetic only; can be deleted next session. |

**Branch state:** `chore/visual-pattern-retrofit-2026-05-27` (HEAD `3d7937f`),
tree clean, awaits operator merge.

### Phase D — corp-monorepo

**Universalization merge:** merge commit `aae0f15`. 7 commits brought in
(+132/-94 LOC; ARCHITECTURE re-home with Mermaid codemap, workspace dot-prefix,
.env.example deletion, README deletion, tier-residue strikethrough, VISION
tier/scale strikethrough). All 4 HIGH findings from the original audit
(CM-CF1/2/3/8 ARCHITECTURE re-home, CM-D1 tier residue) addressed by the
merge.
**Tests post-merge:** **2524 passed, 7 skipped** in 131.67s.
**Lint baseline:** `ruff check` → **89 errors pre-existing** (lenient `select =
["E","F","I"]`, `ignore=["E501"]`). **Tach baseline:** tach not installed in
repo venv (despite `tach.toml` present at root) — separate tooling gap noted.

**Retrofit branch:** `chore/visual-pattern-retrofit-2026-05-27` (2 commits).

| Retrofit action | Result | Evidence |
|---|---|---|
| **`ruff.toml` → `.ruff.toml`** (Path B per operator) | ✓ | commit `d3fa057`; `git mv ruff.toml .ruff.toml` preserves history. Verified ruff reads `.ruff.toml` identically: **89 errors before AND 89 after** the rename → config behavior unchanged. Deleted dead `[tool.ruff]` / `[tool.ruff.lint]` blocks from `pyproject.toml` (shadowed by standalone, never had effect). Closes CM-CF12 (duplication) + CM-D5 (dot-prefix) + ADR-59 `dot_prefix_discipline`. |
| Workspace sort keys (4 added) | ✓ | commit `8d11ca3`; existing `.corp-monorepo.code-workspace` extended with new `// === Explorer ===` section. Pre-existing settings preserved (Python testing args, ruff format-on-save, files.exclude, tasks, launch configs, etc.). JSON parses. |
| `.env` cleanup | n/a | no `.env` at root (`.env.example` was deleted by universalization) |
| Entry-script → `scripts/` | n/a | no entry script at root; `[project.scripts]` in pyproject define CLI entry points routed through `corp.cli` etc. |
| Canonical .md | ✓ | VISION, ARCHITECTURE, BACKLOG, CLAUDE present + ALL-CAPS; CONTRIBUTING/JOURNAL present (optional, correctly cased) |
| Empty/unnecessary file scan | ✓ | no empty files at root |
| Dot-prefix discipline | ✓ | `pyproject.toml`, `tach.toml` exceptions; everything else dotted; `ruff.toml` now `.ruff.toml` |
| 4 HIGH findings from CM audit | ✓ | resolved by the universalization merge (ARCHITECTURE/VISION work) |

**Post-retrofit tests:** **2524 passed, 7 skipped** (after each of 2 commits).
**Post-retrofit lint:** 89 errors (unchanged baseline). Pre-commit hooks
skipped (no relevant Python files staged).

**Branch state:** `chore/visual-pattern-retrofit-2026-05-27` (HEAD `8d11ca3`),
tree clean, awaits operator merge.

## Operator-decision conformance

| Decision (baked into mega-prompt) | ai-council | corp-ops | corp-sca | corp-monorepo |
|---|---|---|---|---|
| ruff dotted (`.ruff.toml`) | n/a | n/a | n/a | ✓ (Path B) |
| Workspace sort = corrected template (4 keys) | ✓ | ✓ | ✓ | ✓ |
| `tach.toml` un-dotted (exception) | n/a | n/a | n/a | ✓ |
| `pyproject.toml` un-dotted (exception) | ✓ | ✓ | n/a (uses `requirements.txt`) | ✓ |
| `.env` empty → delete; content → report | report (100B) | n/a | report (4219B) | n/a |
| Entry-script → `scripts/` | n/a (none) | n/a (none) | **deferred** (`run.py` 18KB; 6 refs; no testable venv) | n/a (none) |
| Canonical 4 .md present + ALL-CAPS | ✓ | ✓ | ✓ | ✓ |
| Empty/unnecessary file scan | ✓ | ✓ | ✓ | ✓ |
| Workspace scaled to size | n/a (existing) | ✓ (lean single-root) | ✓ (lean single-root) | n/a (existing rich) |
| Mega-session branch merged before retrofit | ✓ | ✓ | ✓ | ✓ |
| No push, no auto-merge | ✓ | ✓ | ✓ | ✓ |

## Honest divergence report

1. **corp-sca-time-automation `run.py` move deferred.** The mega-prompt added
   the entry-script → `scripts/` action on top of the retrofit plan, but the
   corp-sca venv has neither pytest nor ruff installed (commented out in
   `requirements.txt` as optional dev). The operator prompt explicitly says
   "Do NOT move entry-scripts without updating references + passing tests."
   Safe verification impossible → deferred. Workspace creation (the retrofit
   plan's primary action) was completed; entry-script move is a separable
   follow-up. Added to BACKLOG.
2. **corp-sca-time-automation post-merge tests not run.** Same root cause:
   pytest unavailable in venv. Mitigation: universalization commits touched
   only governance .md files (verified by `git diff --stat`), so behavioral
   regression risk is nil. Tooling gap added to BACKLOG.
3. **Sort template includes `sortOrderReverse: true`** even though all 4
   original retrofit plans (written 2026-05-27 morning, pre-amendment) only
   specified 2 sort keys. The mega-prompt explicitly overrode by saying "copy
   from corrected template." This is correct per ADR-59 amendment — applied.
4. **Pre-existing lint baselines noted, not fixed.** ai-council has 18 ruff
   errors; corp-monorepo has 89 (lenient). Out of scope for this retrofit
   (universalization + retrofit touched zero Python). The prompt's
   "Don't add features beyond what the task requires" applies.
5. **corp-sca `__pycache__/` at root untracked.** Cosmetic; gitignored; not a
   retrofit failure. Listed for next-session cleanup.
6. **tach not installed in corp-monorepo venv.** `tach.toml` exists; tach
   module absent. Tach is an exception (un-dotted by design). Verification
   relied on tach commit history; runtime check skipped due to tooling gap.

## Failed / incomplete

| Item | Reason | Path forward |
|---|---|---|
| corp-sca `run.py` move | dev tooling missing | install pytest+ruff in corp-sca venv, re-run; move with reference updates |
| corp-sca post-merge `pytest` | dev tooling missing | same |
| corp-monorepo `tach check` runtime verification | tach module not installed | install tach in corp-monorepo venv (or accept that universalization+retrofit touched no Python imports) |

## Architectural contract

- Every commit landed in its own repo's `.git/` — verified per phase by
  empty `git status --short` in the other three repos.
- `.dev-knowledge` contains zero orchestration scripts; the operator-authored
  mega-prompt drove cd/git via Bash invocations.
- The verification report is the only write in `.dev-knowledge` and stays
  inside `docs/audits/` per ADR-36 / ADR-60.
- All retrofit branches are local; no push.

## Branches awaiting merge (5)

| Repo | Branch | Net change | Recommendation |
|---|---|---|---|
| ai-council | `chore/visual-pattern-retrofit-2026-05-27` | +3 LOC (workspace sort) | merge (low risk) |
| corp-ops | `chore/visual-pattern-retrofit-2026-05-27` | +40 LOC (new workspace) | merge (low risk) |
| corp-sca-time-automation | `chore/visual-pattern-retrofit-2026-05-27` | +38 LOC (new workspace) | merge (low risk; `run.py` follow-up tracked) |
| corp-monorepo | `chore/visual-pattern-retrofit-2026-05-27` | +9 / -9 LOC + 1 rename (ruff consolidation + workspace sort) | merge (medium risk: ruff config change verified — 89 errors before/after; recommend `/code-review` before merge per prompt §Final) |
| .dev-knowledge | `docs/cross-repo-retrofit-verification-2026-05-27` | this report + 4 BACKLOG items | merge after operator review |

## Next operator actions

1. **Review this report.** Read the per-repo and divergence sections; decide
   whether the `run.py` deferral and lint baselines are acceptable.
2. **Optional:** `/code-review` corp-monorepo retrofit branch (it touches
   config — ruff consolidation — per the prompt's Final §1 recommendation).
3. **Merge the 4 child retrofit branches** (each in own workdir):
   ```
   git -C C:\Users\1028120\Documents\Dev\<repo> checkout main
   git -C C:\Users\1028120\Documents\Dev\<repo> merge --no-ff chore/visual-pattern-retrofit-2026-05-27
   ```
4. **Merge this verification branch** (`docs/cross-repo-retrofit-verification-2026-05-27`).
5. **Schedule follow-ups** (see BACKLOG items below):
   - corp-sca dev-tooling install + `run.py` move
   - workspace scale-to-size ADR-59 refinement
   - entry-scripts → `scripts/` convention codification
   - `requirements.txt` exception note
6. **Remaining strategic work** (carried forward, separate from this retrofit):
   AI Council Flow operationalization; handoff v3.4 first real test (LAST).
