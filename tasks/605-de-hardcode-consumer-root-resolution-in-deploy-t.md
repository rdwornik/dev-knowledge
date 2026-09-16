---
id: "[#605]"
title: "De-hardcode consumer-root resolution in `deploy/tool.py` and `scripts/audit.py`"
status: closed
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#605] [P2][M] **De-hardcode consumer-root resolution in `deploy/tool.py` and `scripts/audit.py`** — on any substrate that is not the operator's laptop there is no sibling tree, so neither instantiation nor measurement of a consumer is reachable; the recon session hit exactly this and could observe nothing about its target repo. This is first in the recon's ranked build order because every other wave-3 act runs through one of these two entrypoints. **One premise corrected at HEAD, so the lane does not hunt a bug that is not there:** `deploy/tool.py:207-214` is **unconditional** — it returns `hub_root.parent / repo` with no escape. `scripts/audit.py::resolve_repo_path` is **not** the same defect: it honours a stored per-repo path first and only falls back to the sibling. But that stored path lives in a machine-specific, **gitignored** state file, so on a fresh checkout the fallback is all there is and the outcome is identical. Both need the fix; only one is unconditional. **ARCHITECT DECISION, RULED AND RECORDED HERE:** this is the same defect class as `[#294]` in a **different module**, and it is **KEPT SEPARATE**. The fold question is **preserved, not decided by silence** — if the two ever converge on one resolver that is a deliberate act with its own reason. · Done when: both modules accept an **explicit** consumer root with the sibling layout kept as the default fallback, a test proves a non-sibling layout resolves, and `audit repo <name>` runs from a checkout with no sibling tree · refs docs/audits/2026-08-26-technical-w3prep-recon.md (blocker B3, build order 1st), docs/intake/2026-08-26-tech-wave3-wintooling.md (intake #56), deploy/tool.py, scripts/audit.py, #294 · source: intake #56, recon row W3-3 · kill-candidates: none — `[#294]` is ruled KEPT SEPARATE above and owns a different module, so killing it would drop the validator carrier rather than a duplicate resolver · serialize-group: audit-py · **CLOSED 2026-09-16** — evidence 79d5707b
