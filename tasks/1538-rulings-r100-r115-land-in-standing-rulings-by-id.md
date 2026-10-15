---
id: "[#1538]"
title: "Rulings R100-R115 land in STANDING_RULINGS by id, each from its own source file (twin of [#1446])"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1538] [P1][S] **Rulings R100-R115 land in STANDING_RULINGS by id, each from its own source file (twin of [#1446])** - `protocols/STANDING_RULINGS.md` ends at §AT (R93-R99), whose source note (:6307) says "There is no R100"; R100 was given afterwards (`RATIFICATION-2026-10-13.md:42`). No ratification carries an R103 heading. RATIFICATION-2026-10-14 v7 lands R101, R102 and R104-R115 with BUILD-1 L5 but carries only R111 (amended) and R113-R115 itself; R102 and R104-R110, R112 survive only in its `-superseded` versions (v1, v3-v6). `[#1446]` (closed) and `[#1378]` (verification only) cannot carry them · Done when: RED first: (1) a new section in the §AT shape lands every existing heading R100-R102 and R104-R115, each from the file and lines that hold its text (the superseded version is named as the source of record where v7 says "unchanged"), with a verbatim block `tests/test_standing_rulings_sources.py` diffs, each carried by a row or a written "no implementation required"; R111 and R113 carry the BUILD-1 CHALLENGE disposition as their carrier note; (2) R103 is recorded as "no such ruling", and the new section states that §AT's "There is no R100" was true at its landing and is superseded here (append, never an edit of §AT); (3) `uv run --locked python scripts/decision_coverage.py rulings` reports 0 unlanded among them; (4) the simulation refuses on the base · touches: `protocols/STANDING_RULINGS.md`, `tests/test_standing_rulings_sources.py` · kill-candidates: none -- no open row lands R100-R115 (grep over tasks/ 2026-10-15) · refs `[#1446]`, `[#1378]`, `docs/intake/2026-10-15-tech-build1-owed-rows.md` · source: design Q1 (`to-browser/DIGEST-DESIGN-OUTER-LOOP-2026-10-15.md` §9); `to-cc/BATCH-BUILD1-PREP-2026-10-15.md` step 2
