---
id: "[#393]"
title: "corp-sca rot review — confirm-live-or-retire 3 candidates"
status: closed
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S26] Mine our own history before predicting anything"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#393] [P3][S] **corp-sca rot review — confirm-live-or-retire 3 candidates** — the first fleet_analytics run flagged 3 rot candidates in `corp-sca-time-automation` (review queue, NOT a verdict): `config/category_mapping.yaml` (204d, inbound 3), `requirements.txt` (199d, inbound 5), `config/excluded.yaml` (203d, inbound 2). Discharges part of #384's done-when ("rot findings become tickets"). Consumer-repo work — routes via corp-sca. · Done when: each of `config/category_mapping.yaml`, `requirements.txt` and `config/excluded.yaml` in `corp-sca-time-automation` carries a recorded confirmed-live or retired verdict, and a subsequent `fleet_analytics` run no longer flags the retired ones · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §5, #384 · kill-candidates: none — discharges #384's rot-findings done-when · serialize-group: audit-py · **CLOSED 2026-11-02** — evidence a062d59d28fe553cd7941717f9da2cc7e45330b0
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-07-27 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
