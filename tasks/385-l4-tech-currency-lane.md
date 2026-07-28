---
id: "[#385]"
title: "L4 tech-currency lane"
status: open
priority: P3
size: M
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S27] Make tech-currency a distributed rule, not a one-off"
serialize-group: architecture
depends-on: "383"
generates: BACKLOG.md
---

- [#385] [P3][M] **L4 tech-currency lane** — nightly research on new Python tech/versions → version-bump proposals written **into the desired-state contract** → ruled → distributed via the apply channel (intake #16 §6 step 6). L4 is ~5% today, one-offs only. **Gated on the apply channel existing** — the contract + regenerate/apply path from [#383]; without it a proposal has nowhere to land and degrades back into a one-off. Proposals only: the lane never mutates the contract directly. · Done when: one proposal flows contract → ruling → deploy end-to-end · refs docs/intake/2026-07-21-func-fleet-north-star.md §1 (L4), §6 step 6 · depends-on: 383 · serialize-group: architecture
