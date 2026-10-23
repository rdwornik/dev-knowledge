---
id: "[#1583]"
title: "The fourteen `[#912]` known-reds entries have an owner before they expire red on 2026-10-31"
status: closed
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1583] [P2][S] **The fourteen `[#912]` known-reds entries have an owner before they expire red on 2026-10-31** - 14 `[#912]` registry entries expire 2026-10-31 with no owning row ('a lane may not file rows'); `[#1350]` is handled in the night close-out PART 4 (`to-browser/SESSION-lane-bu-863-prompts-guard.md:~48`; `to-browser/SESSION-integrator-bu-2026-10-15.md:136`) · Done when: RED first: a test over `logs/KNOWN-REDS-REGISTRY.json` asserts every entry expiring within 30 days names a row id that exists and is open; fails on 97bcd374 · touches: `logs/KNOWN-REDS-REGISTRY.json`, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1480]`, `[#1564]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8 · **CLOSED 2026-10-23** — evidence 1e17c2c8a · tests tests/test_known_reds_owner_rows.py::test_every_expiring_entry_names_an_open_row
