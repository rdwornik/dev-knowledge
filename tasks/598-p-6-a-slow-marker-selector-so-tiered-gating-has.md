---
id: "[#598]"
title: "P-6 — a slow-marker selector so tiered gating has something to select on"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#598] [P3][S] **P-6 — a slow-marker selector so tiered gating has something to select on** — Tiering needs a mechanical selector or it becomes a hand-maintained list that rots. Mark the slow tests and let the tier select on the marker rather than on a roster someone must remember to update. · Done when: slow tests carry a marker applied from measured durations rather than by guess, a selector runs the fast set and the full set as distinct invocations, the marker set is regenerable from a `--durations` run so it cannot silently rot, and the fast set's coverage gap versus the full set is STATED rather than implied · refs docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md (intake #54), docs/audits/2026-08-26-verification-batch-1-close-packet.md section 8, pyproject.toml, conftest.py, #597 · source: intake #54 (I-PERF), row P-6 · kill-candidates: none — this is P-4's selector and neither absorbs the other; no open row owns test markers · serialize-group: audit-py
