---
id: "[#460]"
title: "fleet-audit dailies — REVERSED on live evidence: the lane is ALIVE, the PUSH died; the defect is replication"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#460] [P2][S] **fleet-audit dailies — REVERSED on live evidence: the lane is ALIVE, the PUSH died; the defect is replication** — the prior recommendation (stop the branch, decommission the "dead" task) rested on a git-date read taken WITHOUT branch access; checked on the host, it is wrong. Task `\DevKnowledge\fleet-baseline` is State=Ready, LastTaskResult=0, 0 missed runs; the local branch holds 51 uninterrupted baseline commits 2026-07-17 → 2026-08-01. Nothing died on 07-16 but the one-shot MANUAL push, owned solely by [#254] — closed that evening on an existence-shaped Done-when (`origin/…` "exists and tracks"), which one push satisfied while its DURABILITY goal (baselines on one disk) went undischarged and now recurs. Easy-metric false closure; that goal folds here. ADR-106 divergence confirmed live: the task runs system `python.exe`, not `uv run --locked`. KEEP the writer; mechanize the push + a divergence alarm. · Done when: the push is mechanized and an alarm fires on divergence, or a ruling records local-only as accepted-with-reason · refs ADR-80, ADR-106, #254, #465 · kill-candidates: none — [#419] owns the class, [#426] its coverage · serialize-group: settings-json
