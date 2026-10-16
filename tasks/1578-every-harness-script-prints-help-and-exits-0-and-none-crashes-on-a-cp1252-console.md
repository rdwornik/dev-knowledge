---
id: "[#1578]"
title: "Every harness script prints `--help` and exits 0, and none crashes on a cp1252 console"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1578] [P2][S] **Every harness script prints `--help` and exits 0, and none crashes on a cp1252 console** - `handoff_state.py:852` and `boot_frontier.py:315` raise UnicodeEncodeError on U+2192; `transport_report.py --help` prints help then 'NOT delivered' and exits 1; `fleet_health.py --help`, `validate_reconciliation.py --help` and `dodo.py --help` print nothing (`docs/audits/2026-10-15-technical-verified-harness-map.md:60-61,64,194,78`). `[#1430]` covers `verify_handoff_probes` only · Done when: RED first: a parametrized test runs each named script with `--help` under `PYTHONIOENCODING=cp1252` and asserts exit 0 and non-empty usage; fails on 97bcd374 · touches: the five scripts above, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1430]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
