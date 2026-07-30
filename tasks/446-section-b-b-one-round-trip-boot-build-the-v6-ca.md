---
id: "[#446]"
title: "§B(b) one-round-trip boot build — the v6 carrier arc"
status: closed
priority: P2
size: L
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#446] [P2][L] **§B(b) one-round-trip boot build — the v6 carrier arc** — intake #19 §B(b), ADOPTED at intake #18 ratification ([#435]): one CC-side command → one evidence block → one operator paste. Built to a RED-first frozen contract (`tests/test_v6_frozen_contract.py`, 9 items, frozen at `1e93c746` before any build code), then codex+terra reviewed with all 8 findings fixed RED-first. · Done when: the boot ships one-round-trip, each leg lands with a test or is re-deferred by ruling, and the spec stamps v6 with its `reconciled_with` edges swept — **MET** · refs intake #19 §B(b), intake #18 (A4/A7/A10/A11), #435, #421, #301, `docs/audits/2026-07-31-technical-v6-open-rulings.md` (+A1/A2) · kill-candidates: none · serialize-group: handoff · **CLOSED 2026-07-31** (architect-adjudicated, merge `7f8a0473`): frozen 9/9, v6.0 IN EFFECT on main, 6 edges swept, ship-gate GREEN-on-main, dry-run witnessed; first LIVE exercise = this window's closing handoff. Carried out unbuilt + named: A11 staged-diff guard → [#448]; intake #18 A6 → its intake owner.
