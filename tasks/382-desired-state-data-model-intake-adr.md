---
id: "[#382]"
title: "Desired-state data model: intake → ADR"
status: closed
priority: P1
size: M
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S24] Declare desired state once, as data, instead of as N registries"
serialize-group: architecture
generates: BACKLOG.md
---

- [#382] [P1][M] **Desired-state data model: intake → ADR** — build the intake #16 §2 architecture (the Terraform **model**, not the tool): ONE schema-versioned desired-state contract in `ecosystem/` dissolving the 4-registry sprawl (**pydantic**); the dependency graph as doc2doc/doc2file/hooks/skills edges with rot as a graph query (**networkx**); the divergence report as surface × repo × {conform/diverge/declared} (**pandas**). `terraform apply` maps to the EXISTING regenerate-and-diff machinery + carriers; state = `deployed-versions.yaml` + the per-consumer version pin. The methodology layer (ADR lifecycle, handoff harness, census, JOURNAL gates) stays custom and sits ON TOP of the schema, never beside it. **The [#381] gate is DISCHARGED** (ADR-104, accepted at `92fabb51`). **Receives the pilot's schema findings** — the restructure pilots the pattern on ONE surface BEFORE this contract is declared (ruling 2026-07-26, `docs/decisions/README.md`); [#433] carries it. · Done when: an ADR is accepted AND schema v1 is committed · refs docs/intake/2026-07-21-func-fleet-north-star.md §2, §5 · serialize-group: architecture
