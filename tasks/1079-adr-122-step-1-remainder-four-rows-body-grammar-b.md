---
id: "[#1079]"
title: "ADR-122 step 1 remainder: 4 rows' non-canonical Done-when separator breaks the converter"
status: open
priority: P3
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
implements: "ADR-122"
generates: BACKLOG.md
---

- [#1079] [P3][S] **ADR-122 step 1 remainder: 4 rows' non-canonical Done-when separator breaks the converter** - `scripts/task_record.py`'s corpus run (this lane, job tmp) found rows #514, #781, #783, #832 use `-` or `.**` before "Done when:" instead of the corpus's usual "· Done when:", so `convert_row` emits zero criteria for them instead of a classified or unresolved one · Done when: all four rows use the canonical "· Done when:" separator -- `python -c "import pathlib,sys; files=['tasks/514-two-rival-lane-branch-re-constants-reconcile-them.md','tasks/781-one-management-map-rendered-from-the-organ-index-with-trigger-less-organs-rendered-dead.md','tasks/783-the-carried-to-resolved-leg-of-decision-coverage-has-never-been-exercised.md','tasks/832-copilot-collections-comparison-rerun.md']; sys.exit(0 if all(chr(183)+' Done when:' in pathlib.Path(f).read_text(encoding='utf-8') for f in files) else 1)"` · implements: ADR-122 · refs docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md, scripts/task_record.py · kill-candidates: none -- filed as this lane's own step-1 remainder (ADR-122 Done-contract item 4 UNMET line)
