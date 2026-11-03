---
id: "[#1051]"
title: "AJ C-5: \"true throughput\" / DXI is blocked -- flagged, not built, pending the retired trend dashboard"
status: closed
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1051] [P3][S] **AJ C-5: "true throughput" / DXI is blocked -- flagged, not built, pending the retired trend dashboard** - Architekt Jutra candidate (DIGEST-AJ-DELTA-2026-09-25 C-5), explicitly in tension with `gen_trend_dashboard.py`'s retirement (confirmed: `c9ea3b07 feat(x-664): retire gen_trend_dashboard, then gen_north_star`). Filed as a flag only, per the digest's own instruction -- not to be built until that tension is resolved. · Done when: the tension between a DXI/true-throughput metric and the retired dashboard is resolved by ruling (build a successor, or explicitly decline) · refs `docs/audits/2026-09-21-technical-aj-all-front.md`, commit `c9ea3b07` · kill-candidates: none -- blocked, filed as a flag per the digest · **CLOSED 2026-11-03** — evidence 432d0d1a295a4c7a544439c5ad02fac6332b5462
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-25 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
