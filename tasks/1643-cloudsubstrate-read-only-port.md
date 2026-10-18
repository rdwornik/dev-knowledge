---
id: "[#1643]"
title: "CloudSubstrate: a read-only cloud port in the hub"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1643] [P2][M] **CloudSubstrate: a read-only cloud port in the hub** - The hub Substrate protocol gets a read-only CloudSubstrate, so a cloud lane for a read-only task is launched through `dispatch.py`, never through win-tooling (R132: cloud is not a build substrate but is used for read-only tasks). Today the only cloud entry is win-tooling `Dispatch-CloudBrief`, outside the hub · owner: E2 lane after `[#1632]` lands the Substrate protocol; the operator's GO for `[#1634]`'s cloud deletion stays there. target batch: E2 · Done when: RED first: (1) `dispatch.py launch --substrate cloud` with a code-kind contract exits non-zero naming R132, and with a read-only contract runs plan, provision, launch, observe, harvest and teardown and writes a launch receipt naming `dispatch.py` as the caller; (2) a test fails when any hub path for cloud calls `Dispatch-CloudBrief`; real-use witness: one read-only track of a batch after E2 runs on the cloud substrate and its harvest lands in `to-browser/` · touches: see the body · kill-candidates: none -- no open row ports cloud into the hub; the only row naming `Dispatch-CloudBrief` is `[#1634]`, a deletion row · refs `[#1632]`, `[#1634]`, `to-browser/RATIFICATION-2026-10-18.md` R132 · decided-by: R132 (E1 lane e1-rows) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
