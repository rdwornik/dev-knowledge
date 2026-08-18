---
id: "[#553]"
title: "`docs/decisions/README.md`'s ADR census is hand-maintained, ungated, and currently wrong in two places"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#553] [P3][S] **`docs/decisions/README.md`'s ADR census is hand-maintained, ungated, and currently wrong in two places** — its "Measured at declaration" counts are stale by one, uncounted since ADR-111. **A second claim in the same block is false independently:** it calls it a measured defect that `ADR-61` *"carries no parsable status line at all"*, but that file's YAML `status:` IS parsable — it is the corpus's only THIRD-format status line. **A number swap is the WRONG fix:** the sentence is a *dated* measurement, so overwriting its figures would falsify its own provenance. · Done when: the ADR census figures are either machine-generated with a regen-and-diff gate on the `audit-index-freshness` model, or carry a dated re-measurement matching a live count; and the ADR-61 claim states the three-format parser hazard instead of asserting an absent status line · refs docs/decisions/README.md, docs/decisions/ADR-61-git-worktree-parallel-sessions.md, scripts/gen_audit_index.py, #242, #269, #552 · kill-candidates: none — [#242] owns per-ADR header-versus-README STATUS coherence and [#269] the audits index; nothing owns this index's aggregate figures · source: docs/audits/2026-08-16-census-nb6-archive-sweep.md §2.2, which carries the census arithmetic and the silent-rot classification
