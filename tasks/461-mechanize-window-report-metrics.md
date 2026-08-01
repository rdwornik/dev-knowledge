---
id: "[#461]"
title: "Six window metrics MECHANIZED — computed from committed state, with the two non-derivable ones declared NOT COMPUTED"
status: closed
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#461] [P2][M] **Six window metrics MECHANIZED — CLOSED 2026-08-01** — `scripts/window_metrics.py`, read-only, emits the six for a named commit range; first mechanized report committed as proof at `docs/audits/2026-08-01-technical-window-metrics.md`. **4 of 6 computed** from committed state (boot round-trips from the HANDOFF_PROCESS major; net backlog delta from row counts across the range; arcs from first-parent merges; boot/paste bytes vs budget). **2 declared NOT COMPUTED with the reason, deliberately** — windows-to-cutoff is a judgment INPUT (a computed-looking number would launder an estimate into a measurement), and drift-report runs is **not-instrumented**: `desired_state_report.main()` prints to stdout and writes no artifact, so a run leaves no committed trace; printing `0` would read as "measured none" when the truth is "nobody counts". `value is None` means not-computed and never renders as zero — pinned by tests. **The row's own defect reproduced and fixed:** the brief's "+6" conflated three questions, so `backlog_delta` reports filed / closed / net SEPARATELY (this window: 189 -> 188, filed 0, closed 1 = net -1). · routine: trigger=on-demand (window close) · scope=a named commit range · consumer=the operator's window report · consumption_path=docs/audits/YYYY-MM-DD-technical-window-metrics.md · verified_by=tests/test_window_metrics.py · review_date=2026-09-01 · **Honest limit:** a CLOSED row leaves BACKLOG.md, so this declaration is retained in the task file and the module docstring but is NOT visible to `check_routine_consumers`, which scans open rows only — flagged, not papered over. · evidence 9faef8dd..HEAD report + RED-first tests · refs docs/audits/2026-07-31-verification-382-ladder-evidence.md, ADR-105, #419, #460 · serialize-group: settings-json
