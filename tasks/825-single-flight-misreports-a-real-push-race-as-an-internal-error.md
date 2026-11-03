---
id: "[#825]"
title: "single_flight.py misreports a real push race as an internal error (exit 2), not in flight (exit 3)"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#825] [P2][S] **single_flight.py misreports a real push race as an internal error (exit 2), not in flight (exit 3)** - Measured by lane ab-804 while building the push-reservation allocator: when two claims push the same lock ref genuinely simultaneously, the loser's create-only push fails with `reference already exists`, a rejection string `single_flight.py` does not recognise. It exits **2, "internal error"**, instead of **3, "in flight"**. Nothing is granted twice -- the server's atomic create still holds -- but the operator is told the guard broke when it worked, and a caller that retries on 2 and backs off on 3 does the wrong thing. · Done when: RED-first, a witness that races two claims against a local bare `origin` (never the real remote) shows the loser exits 3 and names the holder; every create-only rejection form the allocator recognises (`scripts/id_allocator.py`) is recognised by `single_flight.py` from one shared parser rather than two copies · refs `scripts/single_flight.py`, `scripts/id_allocator.py`, `tests/test_single_flight.py`, `docs/audits/2026-09-16-technical-lane-ab-804-id-allocator.md` · kill-candidates: none -- `[#530]` (closed) built the guard; this is its exit-code contract under a real race · source: operator order 2026-09-16, from lane ab-804's measured finding · **CLOSED 2026-11-03** — evidence 5f63605ae7efd04f077fdf03b65646187b43aced
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-16 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
