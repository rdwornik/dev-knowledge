---
id: "[#1386]"
title: "The cut generator names every OPEN carrier in RESIDUAL.md, and a superseded decision file needs no carrying"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1386] [P2][M] **The cut generator names every OPEN carrier in RESIDUAL.md, and a superseded decision file needs no carrying** - The night dry cut (2026-10-04) failed P11 leg 2 with 125 OPEN carriers that RESIDUAL.md did not name, and the only way to clear it was to list them by hand. The architect ruled (2026-10-05, OPERATOR-ACTION 6): at the cut the generator names the OPEN carriers in RESIDUAL.md (R70), not a person; `-superseded` files need no carrying · Done when: (1) `gen_handoff.py` writes every OPEN carrier into the cut's RESIDUAL.md from code, and P11 leg 2 passes on a cut with no hand-written list; (2) a `-vN-superseded` decision file is outside every carriage population that a cut gates, including P13 and `decision_coverage` as well as P11 and the paste (`[#1332]` covers those two); (3) RED-first tests pin both · kill-candidates: none -- `[#1332]` covers superseded files only for P11 and the paste; the RESIDUAL naming has no row · refs `scripts/gen_handoff.py`, `scripts/verify_handoff_probes.py`, `scripts/decision_coverage.py`, `[#1332]` · source: B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (DECIDED-BY-SEAT 4); `to-browser/DIGEST-NIGHT-2026-10-04-leg4-handoff.md` blocker 2
