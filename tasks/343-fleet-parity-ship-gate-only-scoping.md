---
id: "[#343]"
title: "fleet_parity ship-gate-only scoping"
status: closed
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#343] [P3][S] fleet_parity ship-gate-only scoping (RIDER 2 perf follow-up, operator-ruled 2026-07-18) — the [#337] promotion put the ~8s 3-repo fleet_parity walk inside `ALL_CHECKS`, which `audit.py health` runs on EVERY pre-commit (measured 8.3s in-process), so every hub commit now pays it, not just `ship-gate`. Scope the walk to the ship-gate path only, reusing the existing per-commit skip-flag pattern (`cmd_health` already flags the gate so `check_doc_claims` skips its expensive claim-3): `check_fleet_parity` returns a cheap `n/a`/`pass` under the health flag and runs the full walk only under `ship-gate`. NOT a redesign — the skip-flag mechanism already exists. · Done when: a hub pre-commit does not pay the fleet_parity walk (audit-health skips it) while `ship-gate` still runs + blocks on it, with a test proving both · refs scripts/audit.py (cmd_health flag + check_fleet_parity), scripts/fleet_parity.py, #337 · kill-candidates: none — operator-ruled RIDER 2 perf follow-up (no existing task subsumed) · serialize-group: audit-py · **CLOSED 2026-11-03** — evidence 432d0d1a295a4c7a544439c5ad02fac6332b5462
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-07-27 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
