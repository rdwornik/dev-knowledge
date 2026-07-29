---
id: "[#447]"
title: "Ratchet-raise ↔ local-hook bootstrap deadlock"
status: open
priority: P3
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: gates
generates: BACKLOG.md
---

- [#447] [P3][S] **Ratchet-raise ↔ local-hook bootstrap deadlock** — a gate whose threshold is *raised* by a commit cannot be satisfied by that same commit when the raising hook is only armed locally: the pre-commit run reads the OLD threshold from the installed hook, so the commit that lands the raise is judged by the value it replaces. Symmetrically, a commit that *lowers* a ratchet passes locally under the old-permissive value and only bites the next session. The deadlock is structural, not a one-off: `pre-commit install` arms hooks from the config at install time, so config-carried thresholds and hook-carried thresholds drift for exactly one commit — the one that matters. Scope is the MECHANISM, not any individual threshold: either the threshold moves to a data surface the hook re-reads per run (so a raise takes effect in its own commit), or the arming step is made part of the ratchet-raise contract and asserted. Witnessed as the reason a raise has to be split across two commits by hand. · Done when: a single commit can raise a ratchet and be judged by the raised value, with a test that seeds a raise + runs the gate in one transaction · refs `.pre-commit-config.yaml`, `scripts/arm_hooks.py`, `audit.py check_hooks_armed` · kill-candidates: none — no open row owns hook-arming vs threshold-currency; the arming organs are asserted but their bootstrap ordering is unowned · serialize-group: gates
