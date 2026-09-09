---
id: "[#652]"
title: "A gate that passes when its precondition is ABSENT is the empty-rows shape, and the receipt check has it"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#652] [P2][S] **A gate that passes when its precondition is ABSENT is the empty-rows shape, and the receipt check has it** — a batch-U lane asked whether a `gh auth status` check that gates on OK also gates on the command being absent. The first sitting ruled **absent = FAIL**: a gate that passes on absence reports green for the state it exists to detect, which is the same defect P11's empty-rows leg was repaired for one day earlier. The ruling is narrow in its example and general in its class — every precondition probe in the receipt and dispatch path has the same hole until each one is read · Done when: the auth precondition returns FAIL on absence with a fixture proving both directions, and every other precondition probe on the receipt and dispatch path is read once and recorded as either FAIL-on-absent or deliberately not · refs DECLARE-SITTING ruling 8a, `to-cc/LANE-u-000-dispatch-receipt-is-work.md`, `[#642]` · source: DECLARE-SITTING ruling 8a, filed by batch V lane V-4
