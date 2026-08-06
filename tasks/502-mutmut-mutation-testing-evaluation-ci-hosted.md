---
id: "[#502]"
title: "mutmut 3.7.0 mutation-testing evaluation — CI-hosted"
status: open
priority: P3
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: environment
generates: BACKLOG.md
---

- [#502] [P3][M] **mutmut 3.7.0 mutation-testing evaluation — CI-hosted** — the suite's assertion *quality* is unmeasured; mutation testing measures it. Both decisive questions are favourable: 3.7.0 is scopeable via a `[tool.mutmut] paths` array in `pyproject.toml` and is incremental, so it runs on a slice. **HOST RULED: CI-only** — mutmut needs `fork()` (upstream: Windows requires WSL) and WSL is out by operator constraint, so this is **BLOCKED ON [#501]** — until that wall exists there is nowhere to host the eval. Pilot-slice evidence is [#392], the `fleet_analytics` rename-alias defect — a real correctness bug in a tested module, exactly the class a mutation run should catch. **`mutmut` under `uv run --locked` is NOT VERIFIED**, the one remaining unknown; settle it by running the pilot, not by more reading. · Done when: a scoped pilot runs on CI, the `uv run --locked` question is answered from a real run, and the result is a recorded ADOPT/REJECT with measured divergence · footprint: `pyproject.toml`, `tests/test_fleet_analytics*`, the [#501] workflow · refs #501, #392 · kill-candidates: none — no row owns assertion-quality measurement · serialize-group: environment
