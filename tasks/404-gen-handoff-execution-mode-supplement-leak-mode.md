---
id: "[#404]"
title: "gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)"
status: open
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#404] [P2][S] **gen_handoff execution-mode SUPPLEMENT leak (mode-blind framing + P8 row)** — `_tokens()` picks `SUPPLEMENT_BANNER`/`P1_GATE_NOTE` by fill-state only and `PROBES.md.tmpl` P8 unconditionally binds a bundle SUPPLEMENT path, so every execution render carries architect framing for a file the mode never writes and P8 FAILs `verify_handoff_probes` → ship-gate `handoff_probes` RED. First surfaced 2026-07-23 cutting the execution bundle (prior generator renders were all architect-mode); that bundle was hand-corrected to the §13 shape (sanctioned — hand-authored bundles stay bound by the §5 gate). Fix: mode-aware framing tokens (execution = no-supplement + beat-fires-FULL), a mode-conditional P8 row, a per-mode render test through `verify_handoff_probes`. · Done when: an execution-mode render passes `verify_handoff_probes` with zero SUPPLEMENT references, pinned by a per-mode test · refs scripts/gen_handoff.py, templates/handoff/v5/PROBES.md.tmpl, protocols/HANDOFF_PROCESS.md §13, docs/handoffs/2026-07-23-dev-knowledge-execution/, #298 · kill-candidates: none — witnessed defect; #298 (polish, DEFERred) covers WARNs, not this broken render · serialize-group: handoff
