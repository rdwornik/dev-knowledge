---
id: "[#166]"
title: "doctrine_enforcement_coherence check"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#166] [P3][M] doctrine_enforcement_coherence check — a read-only `audit.py` check flagging any ADR/amendment whose status still contains `PROPOSED` / `NOT RATIFIED` while its implementing task is closed (or its enforcement is already live in a gate) — i.e. live enforcement running ahead of its doctrine (the #156 gap this session reconciled by hand) · Done when: the check ships read-only with fixtures + tests, folds into `audit.py health`, and flags a seeded enforcement-ahead-of-doctrine case · refs #11 (amendment_coherence — version-straggler sibling), #153 (enforcement-completeness), ADR-65 (done-items-leave), this #156 gap · serialize-group: audit-py · DEFER — peg: n=2 witnessed doctrine-mismatch
