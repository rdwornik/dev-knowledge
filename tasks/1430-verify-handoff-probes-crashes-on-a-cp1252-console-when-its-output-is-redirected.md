---
id: "[#1430]"
title: "verify_handoff_probes crashes on a cp1252 console when its output is redirected"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1430] [P2][S] **verify_handoff_probes crashes on a cp1252 console when its output is redirected** - The detail print at `verify_handoff_probes.py:2034` raises UnicodeEncodeError on Windows (cp1252) for the probe texts' `·` and `—` unless PYTHONIOENCODING or PYTHONUTF8 is set, so a redirected run dies mid-list (readiness digest F13) · Done when: the CLI writes its output as UTF-8 whatever the console encoding (`sys.stdout.reconfigure` or an explicit encoder); a test runs it with cp1252 stdout redirected · owner: `scripts/verify_handoff_probes.py`'s owner · touches: `scripts/verify_handoff_probes.py`, tests · kill-candidates: none -- [#470] and [#486] fixed the same class in two other CLIs, both closed · source: `to-browser/RATIFICATION-2026-10-08.md` (R90 + the seat's P13 rulings and the tooling-defect table), evidence `to-browser/DIGEST-HANDOFF-READINESS-2026-10-07.md`
