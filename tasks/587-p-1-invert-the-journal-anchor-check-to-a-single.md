---
id: "[#587]"
title: "P-1 — invert the journal-anchor check to a single pass"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#587] [P1][M] **P-1 — invert the journal-anchor check to a single pass** — The anchoring predicate re-derives per candidate commit, so the cost grows with range length on a check every push pays. Invert it to ONE pass over the range. Measure-first: record the before and after with the same command, because a speedup nobody measured is a claim. · Done when: `scripts/journal_anchor.py`'s predicate walks the range once, `block_unanchored_push` and the `journal_spine_anchor` audit backstop still share it (no second implementation), the before/after wall-times are recorded in the commit from the same invocation, and the shared-organ tests stay green with no assertion weakened · refs docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md (intake #54), scripts/journal_anchor.py, scripts/block_unanchored_push.py, scripts/audit.py, ADR-85 · source: intake #54 (I-PERF), row P-1 · kill-candidates: none — no open row owns anchor-check cost; `[#153]` asks which rules lack an organ, not what an existing organ costs · serialize-group: audit-py
