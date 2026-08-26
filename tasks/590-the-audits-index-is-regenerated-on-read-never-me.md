---
id: "[#590]"
title: "The audits index is regenerated on read, never merge-resolved"
status: open
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
serialize-group: pre-commit-config
generates: BACKLOG.md
---

- [#590] [P2][S] **The audits index is regenerated on read, never merge-resolved** — `docs/audits/README.md` is touched 41 times per 300 commits — more than twice `BACKLOG.md` — because every lane that writes an artifact must regenerate it, and it is the file 6 of the last 20 merges conflicted on. Generated files are 7 of 7 conflicted merges: 100%. A generated index should never be a merge participant. · Done when: a lane no longer has to commit `docs/audits/README.md` for its artifact to be indexed, the index is derived at read/regen time, the freshness gate still refuses a stale committed index (or is retired with its reason recorded and the guarantee restated), and zero generated-file conflicts appear across the next 20 merges · refs docs/intake/2026-08-26-tech-append-only-surfaces-and-views.md (intake #49), docs/audits/2026-08-26-technical-hub-diagnostic.md section 5.2 and 5.3, scripts/gen_audit_index.py, .pre-commit-config.yaml, #132 · source: intake #49 (I1) + hub diagnostic section 5 — the concurrency defect, verified not assumed · kill-candidates: none — `[#132]` owns the ORGAN index generator, a different surface with its own gate; killing it would drop an inventory, not a duplicate · serialize-group: pre-commit-config
