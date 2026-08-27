---
id: "[#329]"
title: "VS Code ownership visualization"
status: deferred
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#329] [P3][S] VS Code ownership visualization — folder icons/colors GENERATED from the #328 fleet_parity manifest (dependent, not hand-maintained): render each root entry's ownership {methodology | repo-local | ignored} as VS Code folder icons/colors derived from `ecosystem/parity-surfaces.yaml` + `.methodology.yaml`, so "open any repo, see what's methodology vs local" is visual. Generated-from-manifest only — no hand-edited `.vscode` ownership state (it would rot). · Done when: a generator emits `.vscode` folder icon/color config from the #328 manifest for ≥1 repo AND regenerates deterministically (no hand-edit) · refs docs/audits/2026-07-11-technical-fleet-parity-register.md §9, #322 · kill-candidates: none — operator-ruled register follow-up · serialize-group: settings-json · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
