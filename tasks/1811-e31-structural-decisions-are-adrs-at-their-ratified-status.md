---
id: "[#1811]"
title: "E3.1's structural decisions are ADRs at their ratified status"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
implements: "ADR-134, ADR-135, ADR-136, ADR-137, ADR-138, ADR-139"
generates: BACKLOG.md
---

- [#1811] [P1][M] **E3.1's structural decisions are ADRs at their ratified status** - land the four v3 ADRs (stage-phase, git-memory, browser-surface, read-format) at Accepted, flip ADR-133 to Accepted with its ratified open-point rulings, and carry the two /decide ADRs (record and isolation; task state) to the operator at Proposed · Done when: `uv run --locked python scripts/validate_adr_status.py --all` exits 0 and `uv run --locked python scripts/decide_checks.py adr-sections <ADR>` reports 0 defects for each of the six ADRs this row adds; real-use witness: the E3.1 wave-1 build lanes cite the landed ADR numbers. · implements: ADR-134, ADR-135, ADR-136, ADR-137, ADR-138, ADR-139 · touches: `docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md`, `docs/decisions/ADR-135-main-first-parent-merges-are-the-journal-one-trailer-writer.md`, `docs/decisions/ADR-136-r99-browser-economy-is-enforced-by-code.md`, `docs/decisions/ADR-137-agent-facing-reports-are-a-tsv-read-projection.md`, `docs/intake/2026-11-01-tech-adr-124-carrier-ruff-families.md`, `docs/intake/2026-11-01-tech-adr-124-carrier-tach.md`, `docs/intake/2026-11-01-tech-adr-124-carrier-pyright-ci.md`, `docs/intake/2026-11-01-tech-adr-124-carrier-d5-quality-attributes-check.md`, `docs/audits/2026-11-01-technical-design-record-and-isolation.md`, `docs/audits/2026-11-01-technical-design-task-state.md`, `docs/decisions/ADR-138-the-record-is-revision-bound-and-isolation-is-measured.md`, `docs/decisions/ADR-139-a-task-has-one-state-file-and-a-resume-verb.md`, `docs/decisions/README.md`, `docs/decisions/ADR-133-the-system-view.md`, `.claude/generated/recent-adrs.md`, `tests/test_e30_view_adr.py`, `tests/test_validate_adr_status.py`, `tasks/1837-decide-independent-adjudication-as-code.md`, `tasks/1838-one-id-one-ruling.md` · kill-candidates: none -- no open row owns landing the E3.1 ADRs · refs `docs/decisions/ADR-134-the-lines-eight-stages-are-data-each-stage-writes-one-record.md` · source: to-cc/GO-E3.1.md · decided-by: the operator, 2026-11-01, GO-E3.1 id grant
