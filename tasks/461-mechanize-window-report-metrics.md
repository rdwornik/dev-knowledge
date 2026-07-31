---
id: "[#461]"
title: "Mechanize the six window metrics — today they are hand-assembled per report"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#461] [P2][M] **Mechanize the six window metrics — today they are hand-assembled per report** — the [#382] close assembled them BY HAND from live state (evidence: the 2026-07-31 ladder-evidence audit, §Metrics): boot round-trips · net backlog delta · first-arc-execution · windows-to-cutoff · drift-report runs · paste/boot bytes vs budget. Most are derivable from committed state already (backlog delta from `validate_backlog` counts across the range; bytes from `audit.py health`), so the gap is a reporter, not instrumentation. Hand-assembly is the defect the metrics exist to catch: **a metric nobody computes is a claim, not a measurement** — this window's brief carried a net-delta figure that did not match the verified count. Windows-to-cutoff stays judgment-based: an input, not computed. · Done when: a read-only reporter emits the six for a named commit range, its consumer + consumption_path are declared per ADR-105, and one window report comes from it not by hand · refs docs/audits/2026-07-31-verification-382-ladder-evidence.md, ADR-105, #419, #460 · kill-candidates: none — [#460] rules one telemetry surface's fate; this builds the reporter · serialize-group: settings-json
