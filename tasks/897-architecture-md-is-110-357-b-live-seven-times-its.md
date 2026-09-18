---
id: "[#897]"
title: "ARCHITECTURE.md is 110,357 B live, about seven times its 15 KB target -- and its down-22-percent figure pointed the wrong way across five surfaces"
status: open
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#897] [P2][S] **ARCHITECTURE.md is 110,357 B live, about seven times its 15 KB target -- and its down-22-percent figure pointed the wrong way across five surfaces** - Measured at filing on `87638c8d`: `git cat-file -s HEAD:ARCHITECTURE.md` = **110,357 B**, the same as `wc -c`, against the <=15 KB target of `[#755]`/`[#760]`. The travelling "down 22 %" traces to `docs/audits/2026-09-14-technical-batch-y-launch-contracts/LANE-y-755-docs-cut-finish.md:63` ("100,800 B at freeze, already down 22 % from 129,213 B"), a true snapshot that later growth reversed. Live is +9.5 % over that snapshot and only 14.6 % under the pre-cut baseline, so the figure was not merely unsourced: it pointed the wrong way, and it travelled across five surfaces (ruling W6). The number was typed into prose, which is exactly the CLAUDE.md §4 failure "never restate a count -- cite the surface that computes it" · Done when: ARCHITECTURE.md's size, and the delta against its target, are COMPUTED by a surface every citer reads (a `doc-counts`-style generated figure or a `validate_doc_rot` budget entry; there is none today: `validate_doc_rot._FILE_SIZE_BUDGETS` holds only CLAUDE.md's 200 lines, so the 15 KB is a target that no surface checks). Every live surface that restates a byte figure or a percent for this file is replaced by a citation of that surface. `[#667]`'s docs-cut plan is re-baselined on the live figure · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §6 W6, `docs/audits/2026-09-18-technical-lane-ac-694-architecture-byte-count.md` (on `worktree-lane-ac-694-insurance-census` until merged), `scripts/validate_doc_rot.py` (`_FILE_SIZE_BUDGETS`), `scripts/gen_doc_counts.py`, `[#667]`, `[#755]`, `[#760]` · kill-candidates: `[#667]` -- if its render-from-source Done-when adopts the computed-size clause, this row folds into it
