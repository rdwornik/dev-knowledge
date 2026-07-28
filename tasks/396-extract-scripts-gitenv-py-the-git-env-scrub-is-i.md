---
id: "[#396]"
title: "Extract `scripts/gitenv.py` — the GIT_* env-scrub is in 3 places"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#396] [P3][S] **Extract `scripts/gitenv.py` — the GIT_* env-scrub is in 3 places** — the subprocess-git env scrub (the #355 GIT_DIR fix) is duplicated across `scripts/audit.py`, `scripts/fleet_parity.py`, `scripts/fleet_analytics.py` (#384 added the third). Extract to one `scripts/gitenv.py` all three import — one source, so a future GIT_* override class is fixed once. · Done when: the scrub lives in `scripts/gitenv.py` and all three import it, with a test · refs docs/audits/2026-07-22-verification-night-batch-integration-386-384.md §7, scripts/fleet_analytics.py · kill-candidates: none — DRY refactor of shared validator infra · serialize-group: audit-py
