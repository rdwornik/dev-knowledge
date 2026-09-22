---
id: "[#943]"
title: "Contracts generated from rows -- the spine writes the skeleton, the architect writes only Done-when and decision budget"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#943] [P2][M] **Contracts generated from rows -- the spine writes the skeleton, the architect writes only Done-when and decision budget** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-WAVE4A-2026-09-22.md` "Deferred to wave 4b" and `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` E2/E6.3. Value: this window's architect seat hand-wrote fifteen contracts while the generator that exists produced none -- ADR-87's amendment names this "the architect is a manual generator" failure and ends it as a doctrine; this row ends it in code. · Done when: a task row carrying Done-when + a decision budget produces a runnable contract file through the existing generator, using this window's 15 hand-written contracts as its seed fixtures; one generated contract runs a real lane to a green merge (DECLARE-EQUILIBRIUM E6.3's proof condition). · refs `to-cc/DECLARE-WAVE4A-2026-09-22.md`, `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` (E2, E6.3), `scripts/gen_lane_contract.py` · kill-candidates: none -- no open row covers row-to-contract generation
