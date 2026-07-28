---
id: "[#234]"
title: "Cross-repo probe validator"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#234] [P3][S] Cross-repo probe validator — give `.claude/` target paths full FAIL teeth — the #163 handoff-probe validator now resolves a cross-repo bundle's probes against the TARGET repo (landed 2026-07-02 with the first cross-repo bundle, `2026-07-02-ai-council-architect`), but a foreign `.claude/` target path (e.g. a floor-guard probe `python .claude/check_floor_hash.py`) degrades to WARN (`skipped`) because `_FALLBACK_EXCLUDE_DIRS` excludes `.claude` from resolution, and an ambiguous basename also WARNs — honest-partial, not full teeth. Harden so a cross-repo `.claude/<file>` target resolves against the target root (a scoped allow) → a genuinely-absent floor-guard probe FAILs (real teeth) while excluded-dir DUPLICATES stay pruned. · Done when: a cross-repo bundle whose floor-guard probe names a present `.claude/<file>` in the target PASSes and one naming an absent `.claude/<file>` FAILs, with tests · refs scripts/verify_handoff_probes.py, scripts/audit.py, #163, #221 · serialize-group: audit-py
