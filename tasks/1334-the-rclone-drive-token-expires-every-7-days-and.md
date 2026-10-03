---
id: "[#1334]"
title: "The rclone Drive token expires every 7 days and nothing in the harness tracks it"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1334] [P2][M] **The rclone Drive token expires every 7 days and nothing in the harness tracks it** - R57 (operator, 2026-10-03): the OAuth app stays in Testing, so the rclone Drive token expires every 7 days and is refreshed when it expires; the expiry is tracked by the harness and raises a warning before it passes, as a quota does -- never left to anyone's memory. Today `scripts/quota_watch.py` reads quotas from `ecosystem/quotas.yaml` and warns on a crossing, and no organ records when the Drive token was issued or when it lapses; a lapse shows up as a failed transport read (`L4 rclone FAILED twice`) instead of a warning days earlier · Done when: a RED-first test shows a token recorded as lapsing inside the warning window makes the daily read emit a warning naming the remote and the date, and one past its expiry emits a distinct expired line; the recorded expiry lives in the per-user state directory (not a tracked file) and is rewritten by the refresh step, so the next window is warned about too · touches: `scripts/quota_watch.py`, `scripts/hooks/quota_daily.py`, `ecosystem/quotas.yaml`, tests · kill-candidates: none -- no open row tracks credential expiry (swept: credential, token, expiry) · refs `scripts/quota_watch.py`, `scripts/hooks/quota_daily.py`, `ecosystem/quotas.yaml`, `protocols/STANDING_RULINGS.md` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
