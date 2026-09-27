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
| `repo-with-structural-checks` | A fully compliant repo — all three current structural checks pass (`vision_md`, `adr38_baseline`, `claude_md`). Contains `VISION.md` with valid frontmatter, `pyproject.toml`, `src/`, `README.md`, `CLAUDE.md`, `LESSONS.md`, and `BACKLOG.md`. Every `_FRESHNESS_FILES` member is present with a fresh `last_reviewed` stamp ([#621] lane-g-621-c7 closure 3: `docs/handoffs/README.md`, `protocols/ESSENTIALS.md`, `protocols/SESSION_SETUP.md`, `protocols/AI_COUNCIL_PROCESS.md`, `protocols/DEFINITION_OF_DONE.md` added — absence now FAILs `canonical_freshness` instead of skipping). | `test_audit_run_passes_structural_checks_on_synthetic_repo` (`test_audit.py:355`) |
| `subagent_session` | NOT a mini-repo (the one exception to this file's own framing) — a synthetic Claude Code PROJECT-DIRECTORY: `main.jsonl` (a session transcript) plus its sibling `main/subagents/agent-<id>.jsonl` + `.meta.json`, shaped exactly as measured on this host (subagents nest under a directory of the SAME STEM as the session `.jsonl`, not a directory shared across a project's sessions). Consumer is `scripts/lane_cost.py` / `scripts/routing_agreement.py`, not `audit.py`. No real transcript content — every field is synthetic. | `test_lane_cost.py`, `test_routing_agreement.py` (`lane-subagent-cost`, `[#Context 5]`) |

## Maintenance rule

Fixtures track the audit's checks. When an audit check is added, changed,
or removed, the affected fixture(s) **MUST** be updated, renamed, or removed
in the same change.

A stale fixture — e.g. the former `repo-with-all-five-checks` fixture after
the 5→3 check trim — is a `Decommission:` item per the supersession
discipline in `protocols/PLAYBOOK.md`. Do not leave orphaned fixtures in
this directory.
