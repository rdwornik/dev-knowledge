---
id: "[#369]"
title: "Wire `boundary_headers.py --check` into pre-commit"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: pre-commit-config
source: BACKLOG.md
derived: true
---

- [#369] [P3][S] **Wire `boundary_headers.py --check` into pre-commit** — the generated-not-hand-maintained property of the reader-visible ownership headers currently rests on the **test suite alone**. That is not a hole today (the suite runs at ship-gate, so a hand-edited header is caught before merge), but it is **unenforced at commit time**, unlike every sibling generated surface (`codemap-freshness`, `toc-freshness-playbook`, `roster-freshness`, `claude-rosters-freshness`, `audit-index-freshness`, `intake-index-freshness`), each of which has its own regen-and-diff hook. Closing it makes the header set consistent with the rest of the generated corpus. Touches `.pre-commit-config.yaml`, `CLAUDE.md` §9, and `ecosystem/doc-counts.md` (gates **15 → 16**). Route to **W6**. · Done when: the hook is registered and blocks a hand-edited header, `CLAUDE.md` §9 lists it, and doc-counts reflects 16 gates · refs scripts/boundary_headers.py, .pre-commit-config.yaml, CLAUDE.md §9, ecosystem/doc-counts.md, #352 · kill-candidates: none — a commit-time enforcement gap on a surface that already has ship-time coverage; no open task covers it · serialize-group: pre-commit-config
