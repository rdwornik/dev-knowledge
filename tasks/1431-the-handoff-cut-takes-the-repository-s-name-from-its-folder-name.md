---
id: "[#1431]"
title: "The handoff cut takes the repository's name from its folder name"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1431] [P2][S] **The handoff cut takes the repository's name from its folder name** - `gen_handoff.preflight_rows` sets `repo_name = _main_checkout(repo_root).name` (`gen_handoff.py:1939`) and the ledger row reads `LEDGER-{repo_name.lstrip('.')}.md` (`:1297`), so a checkout in any other folder -- the readiness scratch clone named `clone` -- looks for `LEDGER-clone.md` and fails (readiness digest F10) · Done when: the repository's identity comes from data (the hub marker or a declared name), and a test cuts from a checkout folder with another name · owner: the handoff generator · touches: `scripts/gen_handoff.py`, tests · kill-candidates: `[#1436]` -- the readiness command clones into a scratch folder and needs this first · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
