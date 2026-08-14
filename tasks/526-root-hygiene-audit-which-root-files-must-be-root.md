---
id: "[#526]"
title: "Root-hygiene audit — which root files MUST be root, which are movable"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: architecture
generates: BACKLOG.md
---

- [#526] [P3][S] **Root-hygiene audit — which root files MUST be root, which are movable** — census pass over ADR-101 §1's sanctioned Tier-1 root set: for every current root file/dir, name the tool convention that pins it to the repo root (`uv`/`pyproject.toml`, `.pre-commit-config.yaml`, git's `.gitignore`/`.gitattributes`, etc.) versus one that could legally move under `docs/`/`config/`/`scripts/` without breaking its consuming tool. Read-only census only — no moves executed here; a move is its own later, surfaced act under ADR-101 §1's own refusal-gate doctrine, never a drive-by. · Done when: an audit artifact enumerates every sanctioned Tier-1 root entry with a MUST-be-root/movable verdict and the tool-convention citation backing each · refs ADR-101 §1, docs/decisions/ADR-101-hermetization.md, #345 · kill-candidates: none — #345 externalizes the ADR-101 pattern registry (which class a NEW path matches), a different question from WHY each EXISTING root entry is pinned there; neither open row covers this census · serialize-group: architecture
