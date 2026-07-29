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

- [#447] [P3][S] **Ratchet-raise ↔ local-hook bootstrap deadlock** — a commit that *raises* a gate's threshold cannot satisfy it while the hook is armed locally: `pre-commit install` arms from the config at install time, so the run reads the OLD threshold and the raising commit is judged by the value it replaces. Symmetric on the way down: a *lowering* commit passes under the old value and bites only next session. Structural: config- and hook-carried thresholds drift for exactly one commit — the one that matters. Scope is the MECHANISM, not any single threshold: either it moves to a data surface the hook re-reads per run (a raise then takes effect in its own commit), or arming joins the ratchet-raise contract and is asserted. Witnessed: a raise must be split across two commits by hand. · Done when: one commit can raise a ratchet and be judged by the raised value, with a test seeding a raise + running the gate in one transaction · refs `.pre-commit-config.yaml`, `scripts/arm_hooks.py`, `audit.py check_hooks_armed` · kill-candidates: none — no open row owns hook-arming vs threshold-currency; arming organs are asserted but their bootstrap ordering is unowned · serialize-group: gates
