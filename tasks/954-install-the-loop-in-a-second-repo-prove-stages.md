---
id: "[#954]"
title: "Install the loop in a second repo -- prove stages 1-16 are not `.dev-knowledge`-specific"
status: closed
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#954] [P2][M] **Install the loop in a second repo -- prove stages 1-16 are not `.dev-knowledge`-specific** - filed by LANE-W4-5 (landing-decisions) per `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` E6 "Deferred to wave 5". Value: every stage of the loop so far has been built and proven against this hub; a second-repo install is the test that the loop is portable methodology (ADR-28's Layer 2/Layer 3 boundary) rather than hub-local plumbing that only looks general. · Done when: a second repo runs at least one real task through stages 1-16 with no hub-specific path or assumption uncovered mid-run, or the attempt names exactly what did not port and files that as its own row. · refs `to-cc/DECLARE-EQUILIBRIUM-2026-09-21.md` (E6), ADR-28 · kill-candidates: none -- no open row proves a second-repo install · **CLOSED 2026-11-03** — evidence 5f63605ae7efd04f077fdf03b65646187b43aced
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-22 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
