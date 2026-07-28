---
id: "[#391]"
title: "Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter"
status: open
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S26] Mine our own history before predicting anything"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#391] [P3][S] **Wire fleet_analytics into a nightly lane, or narrow #384 to a manual reporter** — #384 claims "runs as a nightly lane" but nothing invokes `scripts/fleet_analytics.py` (manual CLI only; terra 2026-07-22). Either wire it into the Tier-2 nightly surface (fail-soft), or narrow #384 to a manual reporter + file scheduling separately. If nightly, the [S20] load-gauge discipline applies. · Done when: fleet_analytics fires nightly OR #384 is narrowed to manual + scheduling filed separately · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §4, #384, #270 · kill-candidates: none — completes #384's nightly-lane claim · serialize-group: audit-py
