---
id: "[#352]"
title: "Versioned `.vscode` region decoration"
status: open
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#352] [P3][S] Versioned `.vscode` region decoration (RULING-S human-facing half) — editor-side background decoration (grey = owner=hub, navy = owner=repo; dark theme) of the #312 methodology-boundary marker regions via a versioned `.vscode` config. P4a, shelf-life 2026-08-13 (revisit/kill if not advanced). · Done when: versioned `.vscode` region-decoration config (grey/navy) covers the owner=hub/repo regions of ≥1 governed file AND carries no hand-maintained ownership state · AMENDED (architect ruling, visible-boundary lane): the original generator clause is satisfied BY ELIMINATION, not built — the shipped config holds two regexes keyed on the #312 marker vocabulary and no per-region state, so region add/remove/reclassify needs no config change and it cannot rot; generating a static two-regex file is ceremony. #329 UNAFFECTED — its folder-level ownership genuinely needs generation from parity-surfaces.yaml; do not conflate. · refs #329, #312, RULING-S, docs/audits/2026-07-11-technical-fleet-boundary-marker-design.md · kill-candidates: none — pairing with #329 (folder-level vs in-file; neither subsumes the other) · serialize-group: settings-json
