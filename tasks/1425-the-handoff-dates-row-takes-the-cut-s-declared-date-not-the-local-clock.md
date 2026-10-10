---
id: "[#1425]"
title: "The handoff Dates row takes the cut's declared date, not the local clock"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1425] [P1][S] **The handoff Dates row takes the cut's declared date, not the local clock** - `handoff_state.py:708` renders the Dates row as `now = today or _dt.date.today()` and the generator never passes the cut's `--date`, so a cut run with `--date 2026-10-06` recorded "as of 2026-10-07". BD-dates is LIVE-DRIFTS and the verifier fails any mismatch, and it is not in `_FILLED_REDERIVED_PROBES` (`gen_handoff.py:1066`), so a cut cannot be finalised with `--filled` or verified on any later local day: the 2026-10-07 dry run's re-render refused on it even with P13 masked (readiness digest F2, F16) · Done when: the Dates row is rendered from the cut's declared date (the `--date`, or the receipt's), so a re-derivation on any later day reproduces the recorded row; a RED-first test cuts with a fixed date and re-derives one day later · owner: the handoff generator · touches: `scripts/handoff_state.py`, `scripts/gen_handoff.py`, tests · kill-candidates: `[#1428]` -- folding BD-dates into the re-derived waiver set would also clear the re-render; the integrator keeps whichever fix is narrower · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md` · refs scripts/handoff_state.py, scripts/gen_handoff.py, ADR-129
