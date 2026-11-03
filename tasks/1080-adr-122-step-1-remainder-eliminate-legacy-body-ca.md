---
id: "[#1080]"
title: "ADR-122 step 1 remainder: eliminate legacy_body carriers (671/671 live rows, 86/86 archive records)"
status: open
priority: P3
size: M
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
implements: "ADR-122"
generates: BACKLOG.md
---

- [#1080] [P3][M] **ADR-122 step 1 remainder: eliminate legacy_body carriers (671/671 live rows, 86/86 archive records)** - the corpus run measured 100% legacy_body carriage in both corpora: D1-D9 names no typed field for the near-universal `refs` clause on a live row, and no event/clause-typed shape for a `tasks/archive/*.md` row-body-archival record, so every converted record keeps its unclassified remainder verbatim rather than reaching the step-1 exit bar of zero carriers · Done when: a live row carrying only a refs-shaped clause converts with `legacy_body is None` -- `python -c "import sys; sys.path.insert(0,'scripts'); import task_record as tr; d=chr(183); b='- [#1] [P1][S] **x** - y '+d+' Done when: z '+d+' refs some/file.md'; r=tr.convert_row(1, b, theme=None, story=None, frontmatter_status=None); sys.exit(0 if r.legacy_body is None else 1)"` · implements: ADR-122 · refs docs/decisions/ADR-122-a-task-is-a-typed-record-in-git-every-backlog-view-is-a-projection.md, scripts/task_record.py · kill-candidates: none -- filed as this lane's own step-1 remainder (ADR-122 Done-contract item 4 UNMET line)
