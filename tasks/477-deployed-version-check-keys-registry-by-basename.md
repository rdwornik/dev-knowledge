---
id: "[#477]"
title: "`deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `dev-knowledge` cannot find `.dev-knowledge`"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#477] [P2][S] **`deployed_methodology_version` keys the registry by repo-root BASENAME — a clone named `dev-knowledge` cannot find `.dev-knowledge`** — `scripts/audit.py:2300` computes `repo_key = _git_repo_root_name(repo_path) or Path(repo_path).name` and looks it up in `ecosystem/deployed-versions.yaml`, whose hub row is keyed `.dev-knowledge`. A GitHub clone lands as `dev-knowledge`, so the hub cannot resolve its OWN row and the check reports `not listed` — witnessed in the 2026-08-03 night-batch container. Identical shape to [#465] legs 2+3 fixed at `56f82aaf` (“the hub recognises itself from any checkout”): that fix bound `_is_hub()` to the live tree, but this check still compares NAMES. Same defect class, unfixed surface. · Done when: the check resolves the hub's row from a checkout whose directory name differs from the registry key, with a test seeding a differently-named root · refs scripts/audit.py, ecosystem/deployed-versions.yaml, #465, 56f82aaf · kill-candidates: none — [#465] shipped the hub-identity legs and its open leg 4 is the fleet-audit writer, not this check · serialize-group: audit-py
