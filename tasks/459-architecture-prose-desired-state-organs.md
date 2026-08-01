---
id: "[#459]"
title: "ARCHITECTURE desired-state organ class NAMED + codemap source-root RULED (B: out of scope, cost stated)"
status: closed
priority: P3
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S24] Declare desired state once, as data, instead of as N registries"
serialize-group: architecture
generates: BACKLOG.md
---

- [#459] [P3][S] **ARCHITECTURE desired-state organ class NAMED + codemap source-root RULED — CLOSED 2026-08-01** — Ch2 now names the ADR-109 organ class as one class in three parts (`ecosystem/schema/` the typed contract, `desired_state_loader.py` the loader, `desired_state_report.py` the divergence report), all read-only and operator-invoked per ADR-109 §8, with the membership-narrowing (§2 resolves toward deployed-versions) stated so the report's matrix is not misread as the fleet's size. **Codemap-scope question RULED B** (operator, 2026-08-01): `ecosystem/schema/` stays OUTSIDE `--source-root scripts` — the codemap maps executables, the contract lives with the data it governs (ADR-109 §9). **Cost accepted and stated in the prose, not hidden:** the schema package and the loader->schema edge do not appear in the structural map. Answer A was rejected as a prose leg in disguise — `--source-root` takes ONE directory (`ast_walker.py:15`), so widening needs multi-root support in the codemap tool or moving the schema under `scripts/`, which ADR-109 §9 explicitly rejected. Reopening requires NEW evidence as a NEW row, never preference. `last_reviewed` re-stamped on a genuine end-to-end re-read of all 831 lines. · Closed when: all three Done-when clauses met in one edit · refs ARCHITECTURE.md, ADR-109, ecosystem/schema/, scripts/desired_state_loader.py, scripts/desired_state_report.py · serialize-group: architecture
