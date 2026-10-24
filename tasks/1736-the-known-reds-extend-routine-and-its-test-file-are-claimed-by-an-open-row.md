---
id: "[#1736]"
title: "The known-reds extend routine and its test file are claimed by an open row (H1-X (a))"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1736] [P2][S] **The known-reds extend routine and its test file are claimed by an open row (H1-X (a))** - the lane known-reds-extend adds `scripts/known_reds.py extend` (a ratified, recorded, code-applied expiry extension) and `tests/test_known_reds_extend.py`; a staged file no OPEN row claims fails `graph-task-coverage` and the live orphan census, and a lane cannot register its own row (`[#1733]`), so the integrator files this claiming row from the granted block 1736-1738 (orchestrator-e2-1-cycle-2, 2026-10-25), admitted by RATIFICATION-2026-10-24 amendment (b) H1-X (a) · owner: lane known-reds-extend · Done when: (1) `uv run --locked pytest -n0 tests/test_known_reds_extend.py` passes; (2) KR-1 is applied by `known_reds.py extend --write` (every 2026-10-31 entry to cap 2026-11-09, each with its `extended` record) and `unrecorded_expiry_moves(base, head)` is empty; (3) the owed gate wiring of `unrecorded_expiry_moves` and of the ratification-id resolution stays an OPERATOR-ACTION until a row owns it · touches: `scripts/known_reds.py`, `tests/test_known_reds_extend.py`, `logs/KNOWN-REDS-REGISTRY.json` · refs `[#1733]` · decided-by: the operator, 2026-10-24, RATIFICATION-2026-10-24 amendment (b) KR-1 and H1-X (a) · source: `docs/audits/2026-10-25-technical-known-reds-extension-table.md`, `to-browser/RATIFICATION-2026-10-24.md`
