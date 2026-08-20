---
id: "[#568]"
title: "Provider config as code — `.dev-knowledge` as source of truth, machine-global dirs as junctions"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#568] [P2][M] **Provider config as code — `.dev-knowledge` as source of truth, machine-global dirs as junctions** — Generalize the pattern that already works for `.claude`: the machine-global provider config directories become **junctions into this repo**, so `.claude`, `.gemini`, `.grok` and `.codex` are versioned, diffable and reviewable instead of living as unversioned machine state no gate can see. The forcing evidence is this window's own: three provider clients were exercised across two A/B runs and each carried its own undocumented config surface, with client behaviour — a silently substituted model id, an effort flag that ignores short forms — turning out to be the thing that decided a run. **Second half, and it is what makes this more than tidying:** the routing table reads from **one model registry** rather than from per-provider prose, so a model id, its effort enum and its admission status have exactly one home. Scope is config and registry only — **no dispatch mechanics** (that is `[#539]`/Ch8) and **no admission verdicts**. · Done when: the four provider config dirs resolve to junctions into tracked paths in this repo, with the link topology asserted by a test that FAILs on an un-linked dir; one model registry file carries every model id with its effort enum and admission status; the routing table derives from it rather than restating it; and a test FAILs on a routed model absent from the registry · refs protocols/STANDING_RULINGS.md Q8/Q9, protocols/PLAYBOOK.md, #539, #491, #492 · kill-candidates: none — no open row owns provider configuration; `[#539]` owns contract EMISSION and reads the routing matrix rather than owning it
