---
id: "[#332]"
title: "Fleet dependency-version parity"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#332] [P2][M] Fleet dependency-version parity — automated leg of the #328 fleet_parity checker: each consumer's venv/requirements verified against a hub-recommended set (a versioned dependency manifest carried with the methodology package; drift = WARN, never a hard block). Witnessed trigger: the ai-council d1 arc — pytest-xdist absent (`-n` unrecognized), suite silently degraded to serial. One-time manual alignment is permitted as bootstrap; routine manual checking is the anti-pattern this ticket exists to prevent. · Done when: a versioned dependency manifest ships with the methodology package AND an automated check WARNs a version-drifted consumer while an at-parity (or `.methodology.yaml`-declared) one does not, with a test · refs #328, intake #13 v4 Phase A1, JOURNAL 2026-07-12 (d1 arc) · kill-candidates: none — operator-witnessed parity gap (the ai-council serial-degradation) · ARC-A: corp pytest-xdist declared+installed (sanctioned one-time bootstrap; merge c450a3b, [#332] bracket-only) — STAYS OPEN, Done-when clause-1 (deploy carrier / ships-with-package) unbuilt · serialize-group: audit-py
