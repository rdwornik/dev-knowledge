---
id: "[#1340]"
title: "tests/test_boot_retrieval.py: the tracked boot base is 41,174 B against a 40,000 B ceiling and still growing"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1340] [P2][S] **tests/test_boot_retrieval.py: the tracked boot base is 41,174 B against a 40,000 B ceiling and still growing** - DCT D5. `test_repo_tracked_boot_base_is_under_its_ceiling` sums `CLAUDE.md`, `AGENTS.md`, `.claude/methodology-roster.md`, `.claude/generated/recent-adrs.md` and `.claude/rules/git-discipline.md`: 41,174 B at 2e7fa5f2 against `REPO_BOOT_CEILING = 40_000`. It first went red at 2a62d7d0 (40,980 B), was registered at 40,544 B and has grown 630 B since (6415639c, fd9d6e49, 511073f9, 06778a15, c4a095c3, 5abf6106). **A real defect, still to be fixed**: the registry holds it at 41,174 B under a ceiling the compare enforces (AM2-3), owner `rob`, expiry 2026-10-17 -- a further byte fails CI, a lower value lowers the ceiling · Done when: the boot base is at or under 40,000 B by the PLAN-CI-BASELINE boot cuts (not by raising `REPO_BOOT_CEILING`), the test is green on both CI legs, and the registry's ceiling entry is removed · touches: `CLAUDE.md`, `AGENTS.md`, `.claude/rules/git-discipline.md`, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- no open row owns the boot-base ceiling (the registry entry carried none) · refs `tests/test_boot_retrieval.py`, `logs/KNOWN-REDS-REGISTRY.json`, `CLAUDE.md`, `AGENTS.md` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
