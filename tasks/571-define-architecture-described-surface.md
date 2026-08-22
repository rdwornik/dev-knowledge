---
id: "[#571]"
title: "Define \"architecture-described surface\" + the architecture-freshness check (intake #33 A1)"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: docs-gate
generates: BACKLOG.md
---

- [#571] [P2][M] **Define "architecture-described surface" + the architecture-freshness check (intake #33 A1)** — Intake #33 was ratified ACCEPTED (`disposition: active`) on 2026-08-21; this is the **single** row its A1 criterion calls for, and #33's Births section is explicit that Section A's row is born from the definition, not from the filing. Produce a written definition a grep can evaluate, then the check that flags a commit touching such a surface when `ARCHITECTURE.md` carries no matching delta and no explicit no-impact note. **Zero new organ families** (A1) and **zero new top-level directories** (A4) — both bind. The definition also discharges the three routed obligations A1 names: the `N1-D11`/G-7 consumer, the `N2-E1-1` W-wave referent, and the `N2-R2-07` re-peg decision. Q3 (advisory-only in v1?) is open and is answered by this row, not assumed. Sections B and C of #33 are **out of scope**: B is a belief repair owned alongside `[#420]`, C is a carrier-or-ADR decision that must declare which it is before any file is authored (A3). · Done when: the definition is written and grep-evaluable, the check exists and fires on a fixture where an architecture-described surface changed with no `ARCHITECTURE.md` delta, Q3's advisory-vs-blocking posture is recorded as a decision rather than a default, and the three routed obligations are each named as discharged · refs intake #33, `[#420]`, ADR-51, ADR-101 · kill-candidates: none — measured 2026-08-21: zero `tasks/` rows cite intake #33, and this row is what makes its ACCEPTED status lawful under P-2 · serialize-group: docs-gate
