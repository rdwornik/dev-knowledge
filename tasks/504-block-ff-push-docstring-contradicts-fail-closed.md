---
id: "[#504]"
title: "`block_ff_push` docstring still claims fail-soft after the fail-closed flip"
status: closed
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: architecture
generates: BACKLOG.md
---

- [#504] [P2][S] **`block_ff_push` docstring still claims fail-soft after the fail-closed flip** — `scripts/block_ff_push.py:39` states *Fail-soft: any git error → return 0*, which the ADR-85 amendment §A6 reversed: the organ now **fails CLOSED (exit 2)** on internal error, and the code says so at `:129` and `:194-195`. The module's own summary contradicts its behaviour — the worst place for it, since a reader checking the posture reads the docstring first. **Fold in `ARCHITECTURE.md:327`** (*fail-soft to exit 0 on any git error*), the same claim at doc level, unfiled by #497. **WARNING: do NOT "fix" `:153` or `:169`** — those fail-soft descriptions are CORRECT; `_rev_parse` and `_reconstruct_main_range` legitimately degrade to `''`/`None` rather than raising, only the module-level posture changed. Code-impact: **terra review owed before merge**. · Done when: `:39` and `ARCHITECTURE.md:327` state the fail-closed posture, `:153`/`:169` are untouched, and a terra review artifact records the diff · footprint: `scripts/block_ff_push.py`, `ARCHITECTURE.md` · refs ADR-85, #497 · kill-candidates: none — [#497] owns the class at other sites, not these · serialize-group: architecture
