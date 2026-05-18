# Governance Essences

Operational summaries of ecosystem ADRs cited in directives.
Full ADR text lives in `.dev-knowledge/docs/decisions/`.

---

## ADR-38 — Universal Repo Architecture Baseline

**Status:** Active (amendments A1–A4)
**What it decides:** Mandatory file set and structural layout for all repos by Scale tier.

**Scale M mandatory files** (ai-council is Scale M):
- `src/{package}/`, `tests/`, `pyproject.toml`
- `README.md`, `VISION.md`, `CLAUDE.md`, `AGENTS.md`
- `BACKLOG.md`, `JOURNAL.md`, `LESSONS.md`
- `ARCHITECTURE.md` — **optional at Scale M, required at Scale L**

**A3 amendment (2026-05-11):** ARCHITECTURE.md MUST reside at the repository root
(`ARCHITECTURE.md`), not in a subdirectory (e.g., not `docs/ARCHITECTURE.md`).
This applies if the file exists; its presence is optional at Scale M.

**A4 amendment (2026-05-18):** Closes the corp-monorepo ARCHITECTURE.md root-placement
migration deferral. The deferral no longer applies; any ARCHITECTURE.md migration
pending elsewhere should be treated as a real compliance gap.

**Operational rule for Directive #4:**
Run the hyphen-filename compliance check. If ARCHITECTURE.md exists in ai-council,
verify it is at the repo root (not in docs/ or any subdirectory). If it is missing,
no action required — optional at Scale M.

---

## ADR-46 — Cross-Repo Dated-Entries Format

**Status:** DEMOTED — convention retained, enforcement withdrawn (2026-05-16)

**What it decided:** ISO 8601 dates, newest-first ordering, `### YYYY-MM-DD` header
form for JOURNAL.md, LESSONS.md, and audit files. Enforced via `check_dated_entries_format`
in `scripts/audit.py`.

**Demotion (Council Simplification 2026-05-16):**
- `check_dated_entries_format` audit check **WITHDRAWN** — removed from `scripts/audit.py`.
- `validate_scope_tags.py` **DELETED** — no longer exists anywhere in the ecosystem.
- `[scope: X]` tags in LESSONS.md entries are now **informal lightweight metadata** only.
  Authors may use them; nothing enforces them or audits drift.

**Remaining convention (still expected, just not auto-enforced):**
- ISO 8601 dates in headers
- Newest-first ordering in append-only files
- `### YYYY-MM-DD` header form (normalize_headers.py pre-commit hook still active)

**Operational rule for Directive #3:**
The [scope: X] backfill in LESSONS.md is cosmetically useful but has no automated
verification gate. There is no audit check to "pass." Verify by visual inspection:
scan LESSONS.md and confirm scope tags are present where expected. The prior directive
to "resolve WARN to clean" is not actionable — that check no longer exists.
