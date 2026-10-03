---
id: "[#1347]"
title: "Three tests fail on both CI legs with a symptom and an unread cause: anchor probe, plugin paths, archive records"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1347] [P2][S] **Three tests fail on both CI legs with a symptom and an unread cause: anchor probe, plugin paths, archive records** - `tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` ("pre-push organ REFUSED an anchored push too (exit 1) -- it does not discriminate"), `plugins/tier1-lifecycle/tests/test_plugin_paths.py::test_propose_operates_on_host_repo_not_plugin` ("no proposals written to host logs/") and `tests/test_archive_row_body.py::test_every_committed_record_still_proves_out` ("assert 81 == 86"). Each is red on every recent run of both legs and was registered pre-freeze with no owner or cause; the reasons above are the symptom only, grouped because none has been diagnosed · Done when: each of the three is diagnosed (its cause written into this row), then fixed or dispositioned by ruling, and passes on both CI legs · touches: `tests/test_enforcement_coverage.py`, `plugins/tier1-lifecycle/tests/test_plugin_paths.py`, `tests/test_archive_row_body.py` · kill-candidates: none -- no open row tracks these three · refs `tests/test_enforcement_coverage.py`, `plugins/tier1-lifecycle/tests/test_plugin_paths.py`, `tests/test_archive_row_body.py` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
