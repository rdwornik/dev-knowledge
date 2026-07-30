---
id: "[#451]"
title: "CA layer-edge check — port the ai-council layer-edge review as the missing Layer-2 organ"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#451] [P2][M] **CA layer-edge check — port the ai-council layer-edge review as the missing Layer-2 organ** — operator ruling 2026-07-31 (ADR-108, intake #22 §B): **Clean Architecture stays a standing standard as written** — the layer model is specification, with declared edges and a mechanized check. The ruling is settled; **the gap is the enforcement organ**. §B names the **ai-council layer-edge review as the precedent to port**, but no Layer-2 organ exists in this repo today, so the standard is upheld by review and habit rather than by a gate — a green gate set says nothing about layer conformance. Scope is the port: identify what the ai-council review actually checks, decide what a hub-side equivalent asserts over declared edges, and land it read-only first per the Layer-2 contract (validators only, ADR-28/36). · Done when: a layer-edge check exists and runs in the hub gate set, its honest scope is stated (what it does NOT catch), and ADR-108's "mechanized check" clause cites it · refs ADR-108, ADR-28, ADR-36, docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md §B · kill-candidates: none — no open row owns layer-edge enforcement · serialize-group: audit-py
