---
id: "[#366]"
title: "`residual_completeness` scans the WORKING TREE, not the staged blob"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#366] [P2][S] **`residual_completeness` scans the WORKING TREE, not the staged blob** — codex HIGH 2026-07-19, verified by source read. `changed_bundle_files()` identifies changed paths via `git status --porcelain`, then `scan_file()` reads each path **from disk**. So a bundle staged unfilled and then filled without re-staging passes, and the commit that actually lands the placeholder is not refused — the gate's central guarantee is narrower than stated. Recorded as an `*Honest limit:*` clause in the protocol rule rather than left implied. · Done when: the check validates staged blob content at commit time (e.g. `git show :<path>`), with a regression test seeding staged-unfilled + working-filled, OR the limit is recorded as accepted-with-reason · refs scripts/validate_residual_completeness.py, protocols/HANDOFF_PROCESS.md, docs/audits/2026-07-19-codex-residual-rule-declaration.md · kill-candidates: none — a correctness gap in the gate itself; [#365] is the doc↔code edge, a different concern · serialize-group: audit-py
