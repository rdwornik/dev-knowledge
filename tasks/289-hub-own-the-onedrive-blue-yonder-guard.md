---
id: "[#289]"
title: "Hub-own the OneDrive-Blue-Yonder guard"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#289] [P2][M] Hub-own the OneDrive-Blue-Yonder guard (`block-onedrive.ps1`) — the fleet-level P0 guard is per-machine ad-hoc in `~/.claude/hooks/`, hand-authored, now bigger than a string-match: the v3 three-tier design (baseline 136939a) — T0 allow+log hydration-free enumeration, T1 grant-gated content reads (grant list starts EMPTY), T2 absolute never write/delete, ambiguity falls stricter — gating Edit/Write/NotebookEdit/Read file_path plus command verbs. It binds every repo via core-invariants #1 but is owned nowhere: no canonical source, no deploy carrier, no Informant coverage. Bring it under hub ownership — a versioned canonical hook + policy doc (tier model, grant-list protocol, sanctioned-script read-source enum, matrix-proof), carried by the deploy manifest (ADR-91/92), measured by the Informant Organ. · Done when: the guard has a hub-canonical versioned source + policy doc, ships via a deploy manifest, and is Informant-covered · refs ~/.claude/hooks/block-onedrive.ps1, ~/.claude/rules/core-invariants.md #1, #188, #189, #236, ADR-91, ADR-92, ADR-75 · serialize-group: settings-json
