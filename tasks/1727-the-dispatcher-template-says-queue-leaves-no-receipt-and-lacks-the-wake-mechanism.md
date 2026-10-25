---
id: "[#1727]"
title: "The dispatcher template says dispatch.py queue leaves no receipt, and carries no wake mechanism"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1727] [P1][S] **The dispatcher template says dispatch.py queue leaves no receipt, and carries no wake mechanism** - `templates/dispatcher-order-template.md` (What a launch leaves) claims a raw `claude --bg`, the PATH wrapper "and `dispatch.py queue` leave no such receipt", but a queue FIRE goes through `launch_lane`, which writes `logs/receipts/LAUNCH-<SLUG>.json`; seats believing the template bypassed the queue and launched one lane at a time by hand, and the template carries no wake mechanism for the operator's ORCH-1 (queue --watch as the launch path) · owner: lane template-wake-fix (`templates/dispatcher-order-template.md`, `tests/test_dispatcher_order_adopts_queue.py`) · Done when: (1) RED first: the extended `tests/test_dispatcher_order_adopts_queue.py` fails while the template says `dispatch.py queue` leaves no receipt or lacks the wake mechanism; (2) the template says a queue FIRE leaves `LAUNCH-<SLUG>.json` and names `queue --watch` as the ONE launch call, a Monitor on its FIRE / HOLD / HELD-FAILED output, a 10-minute cron (liveness -> repair, `transport_lint.py sweep`, `batch_janitor.py run`, `quota_watch.py check` before a box fire) and re-arming Monitor and cron on BIND; (3) the extended tests pass and the lane branch CI is green on both OS · touches: `templates/dispatcher-order-template.md`, `tests/test_dispatcher_order_adopts_queue.py` · kill-candidates: none -- this row corrects one template claim and adds one section; it removes no other row · refs `[#1721]`, RATIFICATION-2026-10-24 H1-X, ORCH-1 · decided-by: the operator, 2026-10-24, RATIFICATION-2026-10-24 amendment (b) H1-X, ORCH-1 · source: `templates/dispatcher-order-template.md`, `git show f246bced7`
