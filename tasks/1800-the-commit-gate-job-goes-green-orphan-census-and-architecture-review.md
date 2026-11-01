---
id: "[#1800]"
title: "The commit-gate job goes green: the 10 graph-orphan-census findings get true dispositions and ARCHITECTURE.md a real review"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1800] [P2][M] **The commit-gate job goes green: the 10 graph-orphan-census findings get true dispositions and ARCHITECTURE.md a real review** - on c6618dbb7 the commit-gate job is red on graph-orphan-census (10 findings: `.claude/commands/decide.md`, `.claude/commands/map.md`, `scripts/claim.py`, `scripts/harness_probes.py`, `scripts/read_gate.py`, `scripts/row_close.py`, `scripts/startup_probe.py`, `scripts/system_map.py`, `scripts/task_record.py`, `scripts/test_census.py`) and on audit-health canonical_freshness (`ARCHITECTURE.md` last_reviewed 2026-10-22 predates its 2026-10-27 commit 2946e6c01) · Done when: each of the 10 carries an `ORPHAN_DISPOSITIONS` row naming its real caller file (live organs are never retired; `scripts/harness_probes.py` names the pending operator GO), `test_the_live_orphan_census_reaches_zero_against_its_stated_class` passes, and `ARCHITECTURE.md` last_reviewed moves only after an end-to-end review; the tip's CI commit-gate job concludes success · touches: `scripts/graph_queries.py`, `ARCHITECTURE.md`, `tests/test_graph_spine.py`, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- no open row owns these ten census findings · refs [#1710], [#1711], [#1718] · source: to-cc/GO-E3.0.md, lane e30-commit-gate · decided-by: the operator, 2026-10-31, GO-E3.0 id grant
