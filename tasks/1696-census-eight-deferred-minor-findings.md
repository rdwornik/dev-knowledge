---
id: "[#1696]"
title: "Eight deferred minor findings in the test census tool (collected-line filter, newline-pin, tests encoding, NO-OUTCOME substring, `_find_function`, `load_mutmut`, O(n^2) report, .devcontainer pins)"
status: open
priority: P3
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1696] [P3][M] **Eight deferred minor findings in the test census tool (collected-line filter, newline-pin, tests encoding, NO-OUTCOME substring, `_find_function`, `load_mutmut`, O(n^2) report, .devcontainer pins)** - Copilot minor x8, all deferred as pre-existing: the collected-line filter; the newline pin is cosmetic and the write is non-atomic; tests use the default encoding; the NO-OUTCOME 'patch' substring matches too much; `_find_function` is ambiguous; `load_mutmut` is not robust; the report is O(n^2); unrelated `.devcontainer` pins · owner: a census-tool lane · Done when: (1) each of the eight is fixed or recorded as a false positive with a test; (2) real-use witness: the census re-run on this repo completes with the report time recorded · touches: `scripts/test_census.py`, `tests/test_test_census.py` · kill-candidates: `[#1566]` -- the census tool; `[#1341]` -- newline · refs `[#1566]`, `[#1341]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: minor findings of Copilot (default model, nonce n68027384) in `to-browser/SESSION-e2-census-2.md` section V
