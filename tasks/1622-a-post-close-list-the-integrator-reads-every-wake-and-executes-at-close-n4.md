---
id: "[#1622]"
title: "A POST-CLOSE list the integrator reads every wake and executes at batch close (night contract N4)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1622] [P1][M] **A POST-CLOSE list the integrator reads every wake and executes at batch close (night contract N4)** - work that must happen after a batch closes ("land these branches", "start part 5") was left as a hope that someone would notice; two branches stayed unlanded for 8 h (`to-cc/DECLARE-NIGHT-RUN-CONTRACT-2026-10-16.md` N4) · Done when: RED first: a test over `templates/integrator-order-template.md` asserts a step that reads the POST-CLOSE list on every wake and executes it at close, and a test over the chosen transport kind asserts a POST-CLOSE entry round-trips through `transport.py` and the lint; fails on main · touches: `templates/integrator-order-template.md`, the existing transport kind or its registry entry, tests · refs `[#1573]`, `[#689]` · source: BATCH-RESUME-NIGHT-2026-10-16 PART A step 1
