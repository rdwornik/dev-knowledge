---
id: "[#978]"
title: "Transport file-kind registry, enforced by an adapter -- no more invented names or collisions"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#978] [P1][M] **Transport file-kind registry, enforced by an adapter -- no more invented names or collisions** - D19: invented transport file names, rename-to-superseded churn, and filename collisions recurred all window because no schema names the admitted file kinds (DECLARE, AMEND, BATCH, DIGEST, SESSION, RATIFICATION, ...) or who may write which · Done when: a registry of transport file kinds exists (naming grammar, allowed writers, allowed transitions e.g. `-vN-superseded`), enforced by a transport adapter that every writing organ calls; a command runs a named order by kind+name; a witness run refuses an invented, non-enumerated file kind · implements: ADR-120 · refs `to-cc/DECLARE-TRANSPORT-SCHEMA-2026-09-23.md`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row builds the transport-adapter/registry pair
