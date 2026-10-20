---
id: "[#1632]"
title: "One Substrate protocol; pre-launch for every substrate"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1632] [P1][L] **One Substrate protocol; pre-launch for every substrate** - One Substrate protocol (plan, provision, launch, observe, harvest, teardown) with Local and Codespace implementations; pre-launch runs for every substrate. After ADR-gamma. Today `SUBSTRATES` is a bare tuple (`dispatch.py:137`), the Codespace path skips `moment:pre-launch`, `queue` routes it away, the account hard-caps running Codespaces at 2 (`HTTP 400 too many codespaces running`, 2026-10-18) and the pin gate refuses a launch when the laptop CLI moved · owner: D1 lane after the operator ratifies ADR-gamma. target batch: D1 · Done when: RED first: a Codespace launch runs `moment:pre-launch` and a launch beyond the box cap WAITS (R122) rather than failing; real-use witness: the next batch's lanes launch only through `dispatch.py launch --substrate` and each shows on the P1 picture · touches: see the body · kill-candidates: `[#582]` -- substrate router: decide whether this subsumes it · refs `[#582]`, `[#803]`, `[#810]`, `[#981]`, `to-cc/PLAN-HARNESS-2026-10-18.md` ADR-gamma · decided-by: R132, R122 (retro-ratification, D8). Defect H4: the plan sequence and the exec sequence are separate lists (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`). Defect H5: `observe` and the state fetchers read lane state through separate paths (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`). Defect C5: `repair` skips the `moment:pre-launch` checks that `launch` runs and writes no LAUNCH receipt (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
