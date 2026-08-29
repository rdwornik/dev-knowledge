---
id: "[#622]"
title: "Promote README.md into the ADR-38 canonical mandatory set"
status: open
priority: P3
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#622] [P3][M] **Promote README.md into the ADR-38 canonical mandatory set** — ADR-114 `Decommission` item **(c)**: the *"README.md is optional (deprecated from the baseline)"* docstring in `scripts/audit_checks/check_adr38_baseline.py`. **Decommissioned 2026-08-29** by `[#614]` lane-b; the check's BEHAVIOUR was left unchanged on purpose. **Residual:** `README.md` sits in `canonical_docs.CANONICAL_OPTIONAL` and reaches `SANCTIONED_TIER1_FILES` as a **literal** (the ADR-115 `AGENTS.md` precedent), not through `CANONICAL_MANDATORY` — so it is *canonical at the hub, optional to the fleet*, a split nothing has ruled permanent. Promotion is blocked on two measured facts: six of the eight ADR-104 children carry no root README, and three test pins assert the current membership (`tests/test_canonical_docs.py:53`, `tests/test_audit.py:193-194` and `:323-329`). · Done when: promotion lands with the fleet migration, or the hub-canonical/fleet-optional split is ruled permanent and recorded where the split is readable · refs docs/audits/2026-08-29-technical-614-consumer-enumeration.md, #614, #621 · source: ADR-114 Decommission (c)
