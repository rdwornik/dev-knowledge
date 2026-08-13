---
id: "[#415]"
title: "Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#415] [P2][S] **Tests must bind fixtures, not live mutable repo content (heuristic-behaviour tests)** — `test_live_backlog_no_spurious_dup_warn` asserted the dedup heuristic's SPECIFICITY against the LIVE `BACKLOG.md`, so a legitimate near-duplicate filing (the ruled #409/#410/#411 night-batch triple) turned the suite red — a guard that drifts with production content. Re-pointed to a `_dupN` fixture this arc (`test_dedup_specificity_holds_on_a_distinct_fixture`). Scope: a BOUNDED read-only audit of whether sibling tests share the pattern — a `live_repo`/live-file test asserting heuristic BEHAVIOUR (not repo-validity); the marker spans ~10 test files, and `test_live_backlog_passes_inplace_check` is a same-file sibling (a repo-validity smoke-test, plausibly justified — distinguish the two classes). Enumerate, do not fix here. · Done when: an audit artifact enumerates every test reading live repo content, and each enumerated test is either re-pointed to a committed fixture or listed in that artifact as an intentional integration smoke test with its reason; **or** `protocols/STANDING_RULINGS.md` carries a section naming `[#415]` and the blanket reason · refs tests/test_validate_backlog.py, scripts/validate_backlog.py, #187 · kill-candidates: none — no open task owns the live-content-coupled-test pattern · serialize-group: audit-py
