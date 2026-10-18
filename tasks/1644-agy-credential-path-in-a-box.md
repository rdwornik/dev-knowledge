---
id: "[#1644]"
title: "agy signs in non-interactively in a box"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1644] [P1][M] **agy signs in non-interactively in a box** - agy (Antigravity, which serves Gemini) works in the CLI on the laptop and not in a Codespace: it has no headless sign-in there today (antigravity-cli issue #223), so in a box Copilot's staged adapter reads instead. R135 rules this a defect to fix, not a limit to accept · owner: E2 lane (research and the seeded credential); the operator signs in once. target batch: E2 · Done when: (1) `to-browser/DIGEST-AGY-BOX-AUTH-<date>.md` records antigravity-cli #223's current state and the chosen credential path (a token file seeded from the operator's secrets folder, never a repo file, R13), each claim with its source; (2) RED first: a pre-launch probe runs `agy` non-interactively in a box and fails closed on a missing credential or an empty output file (`[#1327]`: agy reports success without an output file); real-use witness: one box lane whose reads ran through agy, its harvested transcript showing the agy call, the served model id and the read nonce (R59) · touches: see the body · kill-candidates: `[#1537]` -- its R110 sign-in-link half: decide whether the seeded credential path replaces the link · refs `[#1537]`, `[#1327]`, `[#1376]`, `to-browser/RATIFICATION-2026-10-18.md` R135 · decided-by: R135 (E1 lane e1-rows) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
