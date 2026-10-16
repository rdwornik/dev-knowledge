---
id: "[#1564]"
title: "The night batch opens only on a live known-reds registry, and ship_gate_diff runs once on the final tip and records what it catches (R119 night, BUILD-2a slot 1)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1564] [P1][S] **The night batch opens only on a live known-reds registry, and ship_gate_diff runs once on the final tip and records what it catches (R119 night, BUILD-2a slot 1)** - One registry entry expires 2026-10-19 and any expired entry makes the whole registry refuse (`scripts/known_reds.py:259-269`), so a night started on it lands nothing and says why only in a CI log. `ship_gate_diff` averaged 899 s over its last 10 runs, all `fail`, and its events hold only organ, outcome and duration (`MERGE-PATH-RUN-EVENTS.jsonl`, `scripts/merge_path.py:69-81`), so what it catches is unrecorded; with ship-gate red on every base it is the only gate that sees a new failure · Done when: RED first: (1) the night runbook's first step loads the registry at base and, on any expired entry, STOPS before the first land with an `OPERATOR-ACTION` line naming the entry; (2) `ship_gate_diff` runs once on the night's final tip, not per merge, and its run event carries `catches`: the introduced `(check, status, evidence)` triples; (3) a seeded witness on a throwaway branch adds a NEW FAIL to a check already failing on base, and the record shows whether `ship_gate_diff`, ship-gate and CI each caught it; (4) the morning digest prints the night's `catches` and each land's wall time; (5) the tests fail on `b6161972` · touches: `scripts/ship_gate_diff.py`, `scripts/merge_path.py`, `.claude/commands/lane-integrate.md`, tests · kill-candidates: none -- R37.2's batch-close move was withdrawn (`protocols/STANDING_RULINGS.md:5263-5271`) and no open row records its catches · refs R112, R119, `docs/intake/2026-10-15-tech-test-strategy-rows.md` · source: `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q2/Q4; Codex objections C11, C20
