---
id: "[#444]"
title: "Release tier1-lifecycle 0.1.11 — ship the [#437] quoting fix to the version-keyed plugin cache"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#444] [P2][S] **Release tier1-lifecycle 0.1.11 — ship the [#437] quoting fix to the version-keyed plugin cache** — the fixed Stop-hook scanner reaches NO live session (hub included) until a plugin release: the cache is version-keyed (`~/.claude/plugins/cache/…/tier1-lifecycle/0.1.10/`) and release-lint C4 pins `anchors.plugin_version` in every manifest against live `plugin.json` (the suite lints historic v1.1.0/v1.2.0 too), so a bare bump reds 5 tests — discovered in the [#437] arc, bump reverted there as a release act. Steps: bump `plugin.json` + current-manifest anchor + historic-manifest test reconciliation, then marketplace update + per-repo `claude plugin update --scope project` (hub, corp-monorepo, ai-council) + restart. · Done when: live sessions run a plugin version carrying `closure_ids` (cache shows the new version, hub + both consumers) AND release-lint is green · refs plugins/tier1-lifecycle/.claude-plugin/plugin.json, deploy/release_lint.py:223, deploy/manifest-v1.4.0.yaml:100, tests/test_release_lint.py:64, #437 · kill-candidates: none — the [#437] fix is inert in every live session until released · serialize-group: audit-py
