---
id: "[#466]"
title: "Intake flip? — post-discharge, mirrors [#439]"
status: closed
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S25] Converge surfaces in waves, with a mechanical done-signal"
serialize-group: architecture
generates: BACKLOG.md
---

- [#466] [P3][S] **Intake flip? — post-discharge, mirrors [#439]** — [#383] wave 1 discharged ADR-109 §4 with a SPLIT-ONLY round-trip on `docs/intake/`: README.md stays the source of truth, `manifest.json` is derived. Surface 1 later FLIPPED ([#439]); this asks whether intake follows. **Filed, deliberately not built** (architect ruling 2026-07-31): §4 needed the round-trip proof, not a flip, and flipping would move README's doctrine prose into a JSON carrier and supersede the `intake-index-freshness` hook's contract. Decide on evidence from living with the split. **RULED 2026-08-01 (architect): split-only is TERMINAL for `docs/intake/` — the Done-when's second branch. A future flip is a NEW filing with its own contracted arc, not a revival of this row; this is a tripwire discharged, not a task abandoned.** · Done when: an operator ruling either flips the surface (its own contracted arc, mirroring [#439]) or records split-only as terminal for `docs/intake/` · refs ADR-109 §4 amendment, scripts/gen_intake_tree.py, #383, #439 · kill-candidates: none — no open row owns this surface's direction; [#383] owns wave execution, not this follow-on · serialize-group: architecture
