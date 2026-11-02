---
id: "[#934]"
title: "Wave 3 lane E (lane-repo-housekeeping) -- the gate reports only what is real"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#934] [P1][S] **Wave 3 lane E (lane-repo-housekeeping) -- the gate reports only what is real** - filed by LANE-W3-A per `to-cc/DECLARE-WAVE3-CONNECT-2026-09-21.md` hard precondition 2 (every wave row is filed before any other wave-3 lane fires); frozen contract `LANE-W3-E-repo-housekeeping.md`, branch `worktree-lane-repo-housekeeping`, a lane of the loop `[#929]` evaluated. Value: A gate that is always red teaches everyone to ignore red. Two of the documentation counts are simply stale, nineteen warnings are cheap to settle honestly, and three dispositions have expired. After this lane the gate's red means something again. · Done when: carried verbatim from the frozen contract — 1. **Doc counts are true:** regenerate with `scripts/gen_doc_counts.py --write`; record the before and after of every claim that moved. 2. **Sixteen WARNs dispositioned** — the eight Codex records from last night (`docs/audits/2026-09-20-codex-l*.md`), each ACTIONED with an evidence locator and cited from the row or register that consumes it. 3. **Three stale dispositions** (`warn-review-artifact-lane-c-504-no-tally`, `warn-doc-rot-accretion-backlog-241`, `warn-doc-rot-grooming-cadence-hold`): each renewed with fresh evidence or removed, with the reason recorded. 4. **Measured:** ship-gate before and after; the WARN delta is reported and every change is accounted for. No hard-fail is introduced. 5. **Tests:** the disposition register still parses and its validator passes; doc-counts matches the live counts. 6. **Codex terra review** recorded; **handback** per common rules. · refs `to-cc/WAVE3-COMMON-2026-09-21.md`, `to-cc/DECLARE-WAVE3-CONNECT-2026-09-21.md`, `[#929]` · kill-candidates: none -- each wave-3 lane wires an organ that already exists; no open row is absorbed
