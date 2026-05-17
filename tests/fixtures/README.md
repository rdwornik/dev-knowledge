# tests/fixtures — Audit Test Fixtures

This directory contains synthetic mini-repos used as controlled inputs for
the `scripts/audit.py` test suite.

`audit.py` scans a repository for structural health; testing it requires
repos to scan. These fixtures stand in for real repos, each constructed to
exercise a specific audit outcome.

## Naming convention

Each fixture directory is named for what it exercises — not for the files it
contains. The name says *why it exists*, e.g. a repo where all current
structural checks pass, or a repo missing `VISION.md` to verify that check
fails correctly.

## Inventory

| Fixture | Represents | Tests / checks |
|---|---|---|
| `repo-with-structural-checks` | A fully compliant repo — all three current structural checks pass (`vision_md`, `adr38_baseline`, `claude_md`). Contains `VISION.md` with valid frontmatter, `pyproject.toml`, `src/`, `README.md`, `CLAUDE.md`, `LESSONS.md`, and `BACKLOG.md`. | `test_audit_run_passes_structural_checks_on_synthetic_repo` (`test_audit.py:355`) |

## Maintenance rule

Fixtures track the audit's checks. When an audit check is added, changed,
or removed, the affected fixture(s) **MUST** be updated, renamed, or removed
in the same change.

A stale fixture — e.g. the former `repo-with-all-five-checks` fixture after
the 5→3 check trim — is a `Decommission:` item per the supersession
discipline in `protocols/PLAYBOOK.md`. Do not leave orphaned fixtures in
this directory.
