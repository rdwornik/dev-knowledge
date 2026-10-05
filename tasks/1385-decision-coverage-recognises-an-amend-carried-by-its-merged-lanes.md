---
id: "[#1385]"
title: "decision_coverage recognises an AMEND as carried when every lane it adds has merged"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1385] [P2][M] **decision_coverage recognises an AMEND as carried when every lane it adds has merged** - `decision_coverage.py check` and handoff probe P13 refuse a transport `AMEND-` that has no implementing row and no hand-written entry in `DECISION_DISPOSITIONS`. An AMEND that adds lanes to a batch is carried by those lanes' merges, but the gate cannot see that, so at B2-W1 it refused 11 AMENDs, most of them already carried. The architect ruled (2026-10-05, OPERATOR-ACTION 7): an AMEND whose lanes have merged is carried by those merges; its disposition names each merge sha; this row makes the gate recognise that · Done when: (1) `decision_coverage.py check` and P13 accept an AMEND when every lane it names has a merge commit on `main`, citing each merge sha, with no hand entry; (2) the gate still refuses an AMEND with a lane that has not merged (N1: nothing weakened); (3) a RED-first test pins both on a fixture; (4) on the live transport, the B2-W1 AMENDs whose lanes have all merged leave P13 · kill-candidates: none -- no open row covers AMEND-to-lane carriage · refs `scripts/decision_coverage.py`, `scripts/verify_handoff_probes.py` (P13), `[#692]`, `[#1332]` · source: B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (DECIDED-BY-SEAT 3, the per-AMEND dispositions)
