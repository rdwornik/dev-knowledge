---
id: "[#1003]"
title: "Closure proposals run once per new commit, with a reader, not once per turn"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1003] [P1][M] **Closure proposals run once per new commit, with a reader, not once per turn** - S2 proposed row 3: `propose_closures.py` (plugin Stop hook) does its work inline on every turn end, timing out 33 of 208 recorded runs, and its output has no wired reader (`surface-closures.ps1` is not wired anywhere) · Done when: the plugin Stop hook claims per HEAD SHA and hands the work to a detached worker (so the parity MUST `settings-plugin-tier1` stays green); its in-session cost is under 1s; `logs/PROPOSALS-*.md` has a wired reader, or the operator rules the producer retired · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-hook-architecture.md`, `docs/audits/2026-09-23-technical-hook-architecture-appendix.md`, `plugins/tier1-lifecycle/hooks/hooks.json` · kill-candidates: none -- no open row makes closure proposals a per-commit trigger with a reader
