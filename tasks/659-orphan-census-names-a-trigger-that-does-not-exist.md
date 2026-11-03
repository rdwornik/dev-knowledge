---
id: "[#659]"
title: "The `orphan_census` intake names two triggers and one of them does not exist"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S6] Know what depends on code before removing it (ADR-89 computed edges)"
generates: BACKLOG.md
---

- [#659] [P2][S] **The `orphan_census` intake names two triggers and one of them does not exist** — the first sitting will ratify intake `#86` on one condition: that the intake names the census's own trigger, because an `orphan_census` with no trigger is itself an orphan under the harness definition. Read against the tree the condition is half met. The intake does name triggers — *runs in the nightly Routine and at ship-gate* — and the ship-gate leg is real. The nightly Routine is not: the process census proves the repo declares no schedule of any kind, so half the stated trigger is a plan written as a fact. DECLARE-REVIEWS finding R-7 adds the 21-day clock and the add-time consumer edge the same organ owes · Done when: intake `#86` names only triggers that exist, or names the missing one as a dependency with its own row, and the ratification condition is answered against that text rather than against the intake's intent · refs DECLARE-SITTING ratification list, DECLARE-REVIEWS §B R-7, the orphan-census intake (`#86`), `[#642]` · source: the sitting's ratification condition, checked and filed by batch V lane V-4 · **CLOSED 2026-11-03** — evidence 5f63605ae7efd04f077fdf03b65646187b43aced
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-09 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
