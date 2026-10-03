---
id: "[#1343]"
title: "The graph-spine orphan census names .claude/commands/decide.md, which no wiring surface reaches"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1343] [P2][S] **The graph-spine orphan census names .claude/commands/decide.md, which no wiring surface reaches** - DCT D8. `test_the_live_orphan_census_reaches_zero_against_its_stated_class` fails with ".claude/commands/decide.md: command reached by no wiring surface over triggers/imports"; the registry recorded `.claude/skills/aj-scan/SKILL.md` as the first orphan. `decide.md` arrived at c12e72d9 (2026-09-28); the census has been red since 7b585263 (2026-09-19). `[#707]` is related and does not name `decide.md`. Honest limit: the short summary carries only the FIRST orphan, so a second one can sit behind it unseen. **A real defect, still to be fixed**: held by exact signature (any other first orphan reads as a changed failure), owner `rob`, expiry 2026-10-17 · Done when: `.claude/commands/decide.md` is wired to a trigger, retired, or carries a disposition with a reason and an owner in `ORPHAN_DISPOSITIONS`; the census test is green on both CI legs; and the registry entry is removed · touches: `.claude/commands/decide.md`, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- [#707] is the organ-index residue and does not name this command · refs `tests/test_graph_spine.py`, `.claude/commands/decide.md`, [#707], [#664] · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
