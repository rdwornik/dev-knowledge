---
id: "[#986]"
title: "Architecture-level changes require ADR + matrix + debate + operator ratification, not a fast browser accept"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#986] [P1][M] **Architecture-level changes require ADR + matrix + debate + operator ratification, not a fast browser accept** - D28: the browser architect seat accepted a big decision (the original state-store shape) too fast and relayed an unchecked premise into the plan, because no gate distinguishes an architecture-level decision from a routine one · Done when: a decision gate exists: a change classified architecture-level (a new persistent store, a new execution substrate, a new protocol surface) must carry an ADR, a comparison matrix against at least one alternative, a recorded debate round (Claude vs Codex Astra per the routing table), and an explicit operator ratification line before it is treated as decided; ADR-121's own process is the first instance built under this gate · implements: ADR-120 · refs `to-cc/PLAN-WAVE5-2026-09-23.md` §1 (routing table, debate role), `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row defines the architecture-level decision gate
