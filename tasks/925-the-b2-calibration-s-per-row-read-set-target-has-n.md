---
id: "[#925]"
title: "The B2 calibration's per-row read-set target (<= ~60 KB including the boot base) has no owning row and no measurement against it"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#925] [P2][S] **The B2 calibration's per-row read-set target (<= ~60 KB including the boot base) has no owning row and no measurement against it** - BUILD MODE B2 step 2 calibrated this repo against three peer harnesses (maister, architekt-jutra-code, copilot-collections; `docs/audits/2026-09-18-census-b2-calibration-three-repos.md`). Measured: a `.dev-knowledge` build-list row costs 49-653 KB of prose on top of a 43 KB boot base (median ~186 KB), ~6x copilot-collections' typical task and ~1.7x maister's heaviest workflow, and the audit sets "Delete target for lane 1: a row's read set <= ~60 KB including the base". That target was ordered by the BUILD-LIST B2 decision, which carries no `[#id]`, so nothing owns it: B2 lane 1 cut `ARCHITECTURE.md` and `[#755]` carries the ARCHITECTURE <= 15 KB residue, but no row measures the per-ROW read set against 60 KB after the cut, and `[#766]` budgets the boot payload, not a row's read set · Done when: the per-row read set is re-measured by the same method (prose bytes a seat reads for one build-list row, including the boot base) after the B2 cuts, the median and worst case are recorded against the <= ~60 KB target, and each row still over it is either named with its largest contributor or the target is re-ruled with a reason · refs `docs/audits/2026-09-18-census-b2-calibration-three-repos.md`, `protocols/BUILD-LIST.md` (B2 step 2), `[#755]`, `[#766]`
