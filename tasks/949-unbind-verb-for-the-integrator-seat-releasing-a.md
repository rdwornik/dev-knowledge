---
id: "[#949]"
title: "Unbind verb for the integrator seat -- releasing a batch's integrator binding is currently a no-op path"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#949] [P2][S] **Unbind verb for the integrator seat -- releasing a batch's integrator binding is currently a no-op path** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-WAVE4A-2026-09-22.md` "Deferred to wave 4b". Value: `[#833]` refuses a lane into a batch with no live integrator, which requires a bind; there is no matching unbind, so a finished batch or a seat that needs replacing has no clean release and the binding can only go stale, not close. · Done when: an `unbind` verb exists, refuses while lanes are still open against the batch, and a live batch close exercises it end to end. · refs `to-cc/DECLARE-WAVE4A-2026-09-22.md`, `[#833]` · kill-candidates: none -- no open row covers integrator unbind · **CLOSED 2026-11-03** — evidence 5f63605ae7efd04f077fdf03b65646187b43aced
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-22 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
