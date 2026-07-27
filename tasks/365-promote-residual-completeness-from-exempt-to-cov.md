---
id: "[#365]"
title: "Promote `residual_completeness` from `exempt:` to `coverage_scope`"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#365] [P3][S] **Promote `residual_completeness` from `exempt:` to `coverage_scope`** — the doc-side rule now EXISTS (`protocols/HANDOFF_PROCESS.md`, "Residual completeness — the FILL-IN contract"), so the original exemption reason is discharged. It stays exempt only because a resolvable edge needs the doc marker `<!-- rule: handoff-residual-filled -->` **plus TWO** `# rule:` code markers — the `audit.py` adapter AND the validator logic — **plus** `multi_site: handoff-residual-filled: 2`, matching the Tier-3 two-site pattern (`handoff-probes-bind`). One marker leaves the real logic unbound; two without `multi_site` go `ambiguous` (codex MEDIUM 2026-07-19). Witnessed: the doc marker alone yields `broken_edge (doc 1, code 0)`, a WARN that reds the ship-gate. · Done when: doc marker + both code markers + `multi_site: 2` land in ONE commit, the edge resolves, the row moves to `coverage_scope:`, and ship-gate holds at the baseline · refs ecosystem/doc-code-edge.yaml, protocols/HANDOFF_PROCESS.md, #359 · kill-candidates: none — discharges the temporary exemption this arc declared rather than left silent · serialize-group: audit-py
