---
id: "[#459]"
title: "ARCHITECTURE.md prose for the ADR-109 desired-state organ class"
status: open
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S24] Declare desired state once, as data, instead of as N registries"
serialize-group: architecture
generates: BACKLOG.md
---

- [#459] [P3][S] **ARCHITECTURE.md prose for the ADR-109 desired-state organ class** — NARROWED 2026-07-31 (conformance-absorption lane): the Purpose line now reads "through ADR-109" and the Governing ADRs section carries ADR-108 + ADR-109 bullets, so ADR-currency is no longer this row's scope. What remains is the ORGAN-CLASS prose: ARCHITECTURE.md still says nothing about `ecosystem/schema/` (the contract) or the loader/report pair as organs. The codemap covers the two scripts/ modules; `ecosystem/schema/` sits OUTSIDE its `--source-root scripts` scope — the prose leg also rules whether the source-root widens or the schema package is declared out-of-codemap with a reason. · Done when: ARCHITECTURE names the organ class (likely Ch2 organ map or Ch6 mesh) citing ADR-109, the codemap-scope question is ruled in the same edit, and `last_reviewed` rides a genuine re-read · refs ARCHITECTURE.md, ADR-109, ecosystem/schema/, scripts/desired_state_loader.py, scripts/desired_state_report.py · kill-candidates: none — no open row owns ARCHITECTURE currency for the E9 organs · serialize-group: architecture
