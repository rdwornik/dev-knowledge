# Execution Evidence

<!-- scope: meta -->

## Purpose

This file is populated by the receiving chat as it executes the directives in `07_ACTION_PLAN.md`. Record each directive's outcome here before marking it complete.

---

## Directive Execution Log

### Directive 1 — Add research-mode section to `docs/council-question-guide.md`

**Status:** Complete ✓

**Result (FACT):** New "Research-mode questions" section inserted in `docs/council-question-guide.md` immediately after the mode-selection table, covering the full 3-part spec (recognition test / formulation rules / breadth-over-depth trap). +53 lines. Commit `53de121` — `docs(council): add research-mode formulation guide` (branch `docs/research-mode-guide-and-agents-md`, merged into `main` at `11e0399`).

**Verification:** Section present in guide, covers 3-part spec (recognition test / formulation rules / breadth-over-depth trap), commit recorded.

---

### Directive 2 — Create `AGENTS.md` at repo root

**Status:** Complete ✓

**Result (FACT):** `AGENTS.md` created at `ai-council/AGENTS.md` (158 lines), built from the **live `.dev-knowledge/templates/AGENTS-md-template.md`** (template version `2026-04-24`). Repo identity filled (Scale M, active, owner Rob); architecture, conventions, ADR list, and pre-commit hooks verified against `pyproject.toml`, `.pre-commit-config.yaml`, and `docs/decisions/README.md`. Commit `7065834` — `docs: add AGENTS.md cross-tool agent governance file` (branch `docs/research-mode-guide-and-agents-md`, merged into `main` at `11e0399`).

**Template ↔ repo discrepancies resolved:**
- **Gotchas path** — template assumed `.claude/skills/gotchas/SKILL.md`, but this repo uses `.claude/rules/` with three files (`code-standards.md`, `python-env.md`, `testing.md`) and has **no** `.claude/skills/gotchas/` directory. §6 was pointed at the actual `.claude/rules/` layout; CLAUDE.md "Gotchas" section is cited as the authoritative trap list.
- **Stale tool examples** — the template's illustrative `validate_scope_tags.py` pre-commit hook and `tach.toml` enforcement do not exist in this repo. §5 records that the only active pre-commit hook is `normalize-headers`, that no Tach is used, and that scope-tag enforcement was withdrawn under the ADR-46 demotion (Council Simplification 2026-05-16) — `validate_scope_tags.py` has been deleted and must not be re-introduced. The §10 "Do NOT" list captures this explicitly.
- **`docs/handoffs/`** — embedded-template §9 step 4 referenced `docs/handoffs/*.md`, which does not exist in this repo (handoffs centralized in `.dev-knowledge` per ADR-42). §9 step 4 was rewritten to point at `.dev-knowledge/docs/handoffs/`.

**Verification:** File exists at repo root, covers cross-tool LLM agent governance per ecosystem standard (Council #28).

---

### Directive 3 — Verify header-normalizer pre-commit hook

**Status:** Complete ✓

**Result (FACT):** `pre-commit run --all-files` exited 0. Output: `Normalize dated-log entry headers...Passed`. No files modified. Baseline is clean.

**Verification:** `pre-commit run --all-files` exits 0 with no normalizer errors.

---

### Directive 4 — Confirm ADR-38 Scale M governance-file compliance

**Status:** Complete ✓

**Result (FACT):** All six required root governance files present: `README.md`, `VISION.md`, `BACKLOG.md`, `LESSONS.md`, `JOURNAL.md`, `CLAUDE.md`. `CHANGELOG.md` is absent (correct per ADR-49). `ARCHITECTURE.md` is absent (optional for Scale M — not created).

**Verification:** Required root governance files present; any gap flagged.

---

### Directive 5 — Determine `docs/HANDOFF.md` status

**Status:** Complete ✓ — confirmed absent, no action needed.

**Result (FACT):** `git ls-files | grep -i handoff` returned no output at HEAD `1bcc6ab`. `docs/HANDOFF.md` does not exist in the repo. Stage 3 pre-resolution confirmed.

**Verification:** File confirmed absent; no action required unless repo state has changed.

---

### Directive 6 — Backfill scope tags in LESSONS.md (advisory)

**Status:** superseded — skipped

**Result (FACT):** Scope-tag enforcement was withdrawn under the ADR-46 demotion (Council Simplification 2026-05-16); `validate_scope_tags.py` and its pre-commit hook have been deleted, consistent with ADR-48. Backfilling tags for a check that no longer exists serves no purpose. `LESSONS.md` was not touched.

**Verification:** Entries carry scope tag; no existing entry content altered beyond tag insertion.

---

## Pre-commit Hook Results

```
[INFO] Initializing environment for local.
[INFO] Installing environment for local.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
Normalize dated-log entry headers........................................Passed
```

Exit code: 0. No files modified.

## Additional Findings (not in original directives)

- **pytest:** 362 passed, 6 deselected, 24 warnings (pre-existing `datetime.utcnow()` deprecation warnings in gemini_research.py and grok_research.py). No failures.
- **ruff:** 17 pre-existing E501 (line too long) errors — all in `tests/test_runner.py`. No Python was changed in this prompt; these are pre-existing and out of scope.
- **Directive 6 (scope-tag backfill):** Per prompt instructions, this directive is closed as obsolete — superseded by ADR-46 demotion (Council Simplification 2026-05-16). Status to be updated in Prompt B.

---

## Notes

*(Any unexpected findings, deferred items, or scope changes observed during execution)*
