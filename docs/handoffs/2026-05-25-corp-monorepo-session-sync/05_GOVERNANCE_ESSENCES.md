# Governance Essences — 2026-05-25-corp-monorepo-session-sync

These are 2-4 sentence operational essences for ADRs whose rules directly drive actions in `07_ACTION_PLAN.md`. These are summaries only — not full ADR copies. Read the full ADR in the repo for complete rationale.

---

## .dev-knowledge ADR-33 — Vision Universalization

The tier/scale frontmatter fields (`tier:`, `scale:`) are deprecated ecosystem-wide as of 2026-05-23. Every living doc must carry `version`, `last_reviewed`, `owner`, and `status` frontmatter instead. Removing `tier:` and `scale:` from all corp-monorepo files is a P1 [governance-blocking] backlog item — do not skip, defer, or treat as optional.

Full ADR: `.dev-knowledge/docs/decisions/ADR-33_vision-universalization.md`

---

## .dev-knowledge ADR-34 — File Naming Convention

The hyphen separator (`-`) is universal for all repos and all file types. Obsidian vault files are the sole exception: they use underscores (`_`) because Obsidian's internal linking requires it. Corp-monorepo's `CLAUDE.md §4` does not yet disambiguate whether Obsidian vault references within corp-monorepo follow the underscore convention — this is an open PARTIAL finding that directive #4 resolves.

Full ADR: `.dev-knowledge/docs/decisions/ADR-34_file-naming-convention.md`

---

## .dev-knowledge ADR-38 — Universal Repo Architecture (Amendment A5, 2026-05-23)

Every repo in the ecosystem must have `VISION.md`, `ARCHITECTURE.md`, and `BACKLOG.md` at the repo root. `README.md` is optional. The tier system has been removed from the governance baseline — no repo declares a tier. New `src/corp/safety/` module work (if directive #1 reveals missing implementation) must respect the tach layer model: foundation layer, not interface or orchestration.

Full ADR: `.dev-knowledge/docs/decisions/ADR-38_universal-repo-architecture.md`

---

## .dev-knowledge ADR-40 — Scale/Tier Evaluation (DEPRECATED 2026-05-23)

This ADR is fully deprecated. The tier and scale evaluation framework no longer applies. All `tier:` and `scale:` frontmatter fields across the ecosystem must be removed; this is what directive #3 executes in corp-monorepo.

Full ADR: `.dev-knowledge/docs/decisions/ADR-40_scale-tier-evaluation.md`

---

## .dev-knowledge ADR-51 — ARCHITECTURE.md Convention

Every repo must have an `ARCHITECTURE.md` at the root. The codemap is embedded Mermaid between `CODEMAP:START` and `CODEMAP:END` markers — not a separate file. A per-repo opt-in pre-commit hook may enforce freshness. Read `ARCHITECTURE.md` before any structural changes to corp-monorepo (required by this ADR).

Full ADR: `.dev-knowledge/docs/decisions/ADR-51_architecture-doc-convention.md`

---

## corp-monorepo ADR-27 — Safety Invariants (OneDrive Guard Centralization + Vault Writer Narrowing)

ADR-27 mandates a 4-PR implementation plan: (1) centralized `src/corp/safety/onedrive.py` module at foundation layer as the single source of truth for all OneDrive path guards, (2) migration of 4 inline guard sites (`cleanup/disk.py`, `cleanup/executor.py`, `actions/_helpers.py`, `project/renderer.py`) to import from the central module, (3) AST-based CI scanner at `tests/safety/test_no_unguarded_writes.py` that blocks unguarded writes, (4) vault writer narrowing via explicit `VaultZone` enum whitelist. **Stage 3 verification confirmed that `src/corp/safety/` does not exist and `tests/safety/test_no_unguarded_writes.py` does not exist — the implementation is MISSING. Directive #1 of the action plan is to audit and confirm this status before any other P1 work.**

Full ADR: `corp-monorepo/docs/decisions/ADR-27-safety-invariants.md`
