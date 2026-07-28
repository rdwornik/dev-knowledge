---
id: "[#393]"
title: "corp-sca rot review — confirm-live-or-retire 3 candidates"
status: open
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S26] Mine our own history before predicting anything"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#393] [P3][S] **corp-sca rot review — confirm-live-or-retire 3 candidates** — the first fleet_analytics run flagged 3 rot candidates in `corp-sca-time-automation` (review queue, NOT a verdict): `config/category_mapping.yaml` (204d, inbound 3), `requirements.txt` (199d, inbound 5), `config/excluded.yaml` (203d, inbound 2). Discharges part of #384's done-when ("rot findings become tickets"). Consumer-repo work — routes via corp-sca. · Done when: each of the 3 is confirmed-live or retired · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §5, #384 · kill-candidates: none — discharges #384's rot-findings done-when · serialize-group: audit-py
