---
id: "[#650]"
title: "ADR-117 sits at `Proposed` while a gate already enforces it"
status: open
priority: P2
size: S
theme: "[E4] Decision management"
story: "[S12] Close the small ADR cross-reference + registry amendments"
generates: BACKLOG.md
---

- [#650] [P2][S] **ADR-117 sits at `Proposed` while a gate already enforces it** — the first sitting ruled ADR-117 **Accepted**: P11's carriage predicate implements it, the predicate runs on the live transport, and every decision file on that transport obeys it. An ADR a gate enforces is not Proposed. The sitting also refused the two alternatives on the record — admitting `DRAFT` to the status enum creates a third state between intake and ADR, which the census forbids, and 'it should not have landed' relitigates an enforced decision. The flip was assigned to this lane and is **not performed here**: `docs/decisions/` is outside this lane's frozen footprint, and a status flip re-derives the ADR index and the generated recent-ADRs fragment, which the same contract pins to the integrator · Done when: ADR-117's status line reads `Accepted` with the sitting cited as the ratifying act, and the ADR index plus `.claude/generated/recent-adrs.md` are regenerated in the same commit · refs DECLARE-SITTING ruling 4, ADR-117, ADR-94 (status-line exception), `[#642]` · source: DECLARE-SITTING ruling 4, filed by batch V lane V-4
