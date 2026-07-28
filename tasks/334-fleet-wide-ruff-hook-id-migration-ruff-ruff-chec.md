---
id: "[#334]"
title: "Fleet-wide ruff hook id migration `ruff` → `ruff-check`"
status: open
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: pre-commit-config
generates: BACKLOG.md
---

- [#334] [P3][S] Fleet-wide ruff hook id migration `ruff` → `ruff-check` (upstream `ruff-pre-commit` deprecation; flagged by codex-review, refuted-for-now on parity grounds — `id: ruff` is a working legacy alias all three repos currently share, so keeping it was correct at the `chore/ruff-hub-pin` pin) — ONE coordinated arc across hub + corp-monorepo + ai-council, never per-repo drift; includes the three `.pre-commit-config.yaml` edits (`id: ruff` → `ruff-check`, `args: []` retained) + roster currency (CLAUDE §9 ruff-line, doc-counts). · Done when: all three repos use `ruff-check` and the legacy `ruff` alias is gone, witnessed per repo (a staged violating `.py` BLOCKED under the new id) · refs hub JOURNAL 2026-07-12 (ruff-hub-pin, merge 6de45b47), docs/audits/2026-07-12-codex-ruff-hub-pin.md, .pre-commit-config.yaml · kill-candidates: none — upstream-deprecation follow-up (operator-directed fleet-parity item); no existing task subsumed · serialize-group: pre-commit-config
