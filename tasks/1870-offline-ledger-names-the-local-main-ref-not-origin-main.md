---
id: "[#1870]"
title: "Offline LEDGER names the local main ref, not origin/main"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1870] [P2][S] **Offline LEDGER names the local main ref, not origin/main** - audit A6 of 2026-11-04 (to-browser/DIGEST-AUDIT-SEAT-WORKTREE-CONSEQUENCES-2026-11-04.md): `gen_ledger.py --offline` writes `main:` from `git rev-parse main` (`scripts/gen_ledger.py:220`), the LOCAL ref, which the primary leaves behind origin/main (the operator's read surface said ac13bf33d while origin/main was 33005b8c2). Fix: offline mode reads the last fetched `origin/main` (no network) and labels it, or states `main: not read (offline)`; a test pins that a stale local main never appears as main. · touches: scripts/gen_ledger.py, tests/test_gen_ledger*.py · kill-candidates: none - no open row owns the ledger's main field · refs ADR-140 (out-of-scope item A6), `scripts/gen_ledger.py` · Done when: an offline LEDGER generated from a checkout whose local main lags origin/main names no stale sha as main (test) · decided-by: night order N2(b), DIGEST-RULING-Q-SEAT-1-AND-NIGHT-ORDER-2026-11-04 · source: P0 audit A6
