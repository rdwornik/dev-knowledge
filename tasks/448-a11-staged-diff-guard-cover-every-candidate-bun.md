---
id: "[#448]"
title: "A11 staged-diff guard — cover EVERY candidate bundle, not just the active one"
status: closed
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#448] [P2][S] **A11 staged-diff guard — cover EVERY candidate bundle, not just the active one** — sol acceptance item 10, carried out of [#446] unbuilt: the gate verifies only `_select_active_bundle`'s pick, so an uncovered staged-diff candidate passes silently. Additive to the selector; erases no selector outcome. · Done when: a staged diff containing two candidate bundles fails the guard when either is uncovered, with a test · refs scripts/audit.py check_handoff_probes, docs/audits/2026-07-30-technical-v6-spec-sol-draft.md §6, #446 · kill-candidates: none — [#446] shipped its other A11 legs and does not own this one · serialize-group: audit-py · **CLOSED 2026-11-03** — evidence fc393ef3a7e860472e1d5d837ceacca993f891ff
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-07-30 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
