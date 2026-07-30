---
id: "[#447]"
title: "Self-referential gate family — the committing act cannot satisfy the gate's own precondition"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: gates
generates: BACKLOG.md
---

- [#447] [P3][S] **Self-referential gate family — the committing act cannot satisfy the gate's own precondition** — (1) *ratchet-raise ↔ local-hook bootstrap*: `pre-commit install` arms from the config at install time, so a commit *raising* a threshold is judged by the value it replaces; a *lowering* one bites next session instead. The carriers drift for exactly one commit — the one that matters; raises get hand-split across two commits. (2) *ADR-85 JOURNAL-anchor recursion*: the anchor commit can never self-anchor; session-end gate looped to the 9-block cap 2026-07-30 (evidence: 51ab04e2). Scope is the MECHANISM: either the datum moves to a surface the gate re-reads per run, or the arming/anchoring step joins the contract and is asserted. Closure polarity: the new owning row exists BEFORE the absorbed row closes. · Done when: one commit can raise a ratchet and be judged by the raised value, and a wrap commit can satisfy its own anchor gate, with tests · refs `.pre-commit-config.yaml`, `scripts/arm_hooks.py`, `audit.py check_hooks_armed`, `scripts/session_end_backpressure.py` · kill-candidates: none — no open row owns self-referential gate preconditions · serialize-group: gates
