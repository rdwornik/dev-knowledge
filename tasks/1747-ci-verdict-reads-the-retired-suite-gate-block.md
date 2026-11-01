---
id: "[#1747]"
title: "`ci_verdict.py` reads the retired suite-gate block on its no-baseline path and reports registry members as new reds"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1747] [P2][M] **`ci_verdict.py` reads the retired suite-gate block on its no-baseline path and reports registry members as new reds** - `ci_verdict.py` reads the retired suite-gate block on its no-baseline path and so reports known-reds registry members as new reds · Done when: RED first: a test built from c6618dbb7's case (6 known-reds members) asserts 0 new reds; real-use witness: `ci_verdict.py --ref c6618dbb7` names exactly `commit-gate` as a new red (its job is genuinely red on main since 2026-10-17, row [#1800]) and none of the six known-red ids (two registry members, four [#664] witnesses) it reported on its no-baseline path. · touches: `scripts/ci_verdict.py`, its test · kill-candidates: none -- no open row owns the ci_verdict no-baseline path · refs `scripts/ci_verdict.py`, [#1800] · source: to-cc/GO-E3.0.md G2 · decided-by: the operator, 2026-10-31, GO-E3.0 id grant
