---
id: "[#1576]"
title: "The transport janitor treats `-withdrawn` like `-superseded` and never moves a file that tracked code cites by name"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1576] [P2][S] **The transport janitor treats `-withdrawn` like `-superseded` and never moves a file that tracked code cites by name** - `transport.py:538 _SUPERSEDED_RE` and `:1084` match only 'superseded'; three `-withdrawn` files stay; the janitor moves `AMEND-HANDOFF-BOOT-DISPATCH-SECTION-...SUPERSEDED-wrong-command.md` that `STANDING_RULINGS.md:4575` cites; six stale `LANE-14xx-*.CLAIMED-*` markers need a release (`docs/audits/2026-10-15-technical-token-burn-and-handoff-inventory.md` B2/B3) · Done when: RED first: a test over a temp transport tree asserts a `-withdrawn` file is moved to the archive month folder and a file cited by name from a tracked path is excluded and reported; fails on 97bcd374 · touches: `scripts/transport.py`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1539]`, `[#1454]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md`. Defect H38: the transport janitor has no run that clears transport files (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
