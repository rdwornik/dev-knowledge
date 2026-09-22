---
id: "[#958]"
title: "Wave 4b lane 2 (lane-handback-organ) -- a lane hands back through one organ that checks it first"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#958] [P1][M] **Wave 4b lane 2 (lane-handback-organ) -- a lane hands back through one organ that checks it first** - filed by LANE-W4B-0 per `to-cc/WAVE4B-COMMON-2026-09-22.md` rule 1; frozen contract `LANE-W4B-2-handback-organ.md`, branch `worktree-lane-handback-organ`. Depends on lane 0 (`[#956]`); runs in parallel with lanes 3-5 after lane 0 merges. Value: five of wave 4's problems share one cause -- lanes hand-write artifacts that machines then parse, from specs that live in three places. After this lane a lane calls one organ; the organ checks the lane and writes every artifact from one schema, or refuses with a receipt. The integrator stops being the first place a lane learns it was not ready. · implements: ADR-120 · Done when: 1. **FR2 as written in the plan**, in full: the self-check (ship-gate hard-fails introduced by the branch, ratchet, review-record consumer, branch purity against `origin/main`, transport-write check), the artifacts (LANE-END report with a `Commits` section, session file at the canonical name, HANDBACK and STATE lines), and refusal with a receipt. 2. **One schema:** typed dataclasses for HANDBACK line, STATE line, LANE-END report and REFUSED order, with a validator; `transport_report.py` and `lane_end_guard.py` use it. The existing `audit.py handback` form and the organ's form agree -- show both accept the same line. 3. **Lane-end fix:** the guard finds the session file by worktree slug; the embedded guard receipt ends `ok` or `failed`, never `running`. 4. **Acceptance tests of FR2** from the plan, red first, one per refusal cause plus the clean case. 5. **Live proof:** hand this lane back by calling its own organ; paste its receipt. 6. **Codex sol adversarial pass** on the organ (it is the new trust boundary) plus the terra review, both with consumer cited; **self-check and purity**; **handback** · refs `LANE-W4B-2-handback-organ.md`, `to-cc/WAVE4B-COMMON-2026-09-22.md`, `to-cc/PLAN-WAVE4B-SESSION-2026-09-22.md` (FR2 and its acceptance tests), `to-cc/DECLARE-WAVE4B-DIRECTION-2026-09-22.md` (RC3), `[#955]` (the epic this row implements) · kill-candidates: none -- no open row covers the handback organ
