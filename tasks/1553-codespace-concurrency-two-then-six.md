---
id: "[#1553]"
title: "Codespace lanes run two, then six at once, each monitored, inside a declared core-hour cap"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1553] [P2][M] **Codespace lanes run two, then six at once, each monitored, inside a declared core-hour cap** - UC5 spec item 6 (concurrency) and R6's "three or four projects can be worked in parallel in the cloud". Never run. Budget at 2026-10-14: 130.62 of 180 core-hours left (quota line, DIGEST-VERIFIED-HARNESS-MAP-2026-10-15); six 4-core boxes cost 24 core-hours per wall hour; GitHub documents no numeric per-user concurrency default for personal accounts, so it is measured · Done when: a bounded episodic probe: `dispatch.py queue` routes 2, then 6 Codespace lanes at once, each with its own heartbeat and observe loop (`[#1551]`); before each launch `quota_watch.py check` refuses a projection past the 180-hour quota, and the probe stops at its declared cap (15 core-hours unless the operator raises it); each lane's fate is recorded (partial success is a result, not a pass); every box is harvested and deleted with parity C5 PASS; the record states the concurrency limit actually met · starts after: `[#1551]` merged and one green R63 run (`[#1453]`) · touches: `scripts/dispatch.py`, `scripts/quota_watch.py`, tests · kill-candidates: none -- no open row measures Codespace concurrency · refs `[#1551]`, `[#1453]`, `[#1366]`, `docs/intake/2026-10-15-tech-outcome-scoreboard-rows.md` · source: `to-cc/BATCH-DEFINE-OUTCOMES-2026-10-15.md` §2 item 6; `to-browser/DIGEST-OUTCOME-SCOREBOARD-2026-10-15.md`
