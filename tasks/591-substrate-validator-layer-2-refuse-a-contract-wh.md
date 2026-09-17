---
id: "[#591]"
title: "Substrate validator, layer 2 — REFUSE a contract whose substrate contradicts its own content"
status: closed
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: architecture
depends-on: "#582"
generates: BACKLOG.md
---

- [#591] [P2][M] **Substrate validator, layer 2 — REFUSE a contract whose substrate contradicts its own content** — A contract declares a substrate and nothing checks the declaration against what the contract then asks for. This is the REFUSE layer, and it comes FIRST of I4's three because refusing is cheaper than detecting drift after the fact. · Done when: the validator REFUSES a contract naming a substrate with no live verb, REFUSES cloud plus a gate in its Done-when, REFUSES codespace/cloud plus an operator-disk path, and WARNs on a second local writer in one checkout; an override is an explicit RECORDED deviation and never a silent pass; each refusal names the rule it fired on; and a fire-test proves each of the four legs actually fires · refs docs/intake/2026-08-26-tech-dispatch-consolidation-remainder.md (intake #52), docs/intake/2026-08-24-tech-substrate-router.md, scripts/gen_lane_contract.py, protocols/PLAYBOOK.md Ch8, #582 · source: intake #52 (I4), the substrate-VALIDATOR act — first of three · kill-candidates: none — `[#582]` owns the router ARC that this validator is a precondition of; killing it would remove the consumer, not a duplicate · serialize-group: architecture · depends-on: #582 · **CLOSED 2026-09-16** — evidence 8e832523
