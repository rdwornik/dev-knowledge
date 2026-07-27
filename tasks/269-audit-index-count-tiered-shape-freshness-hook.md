---
id: "[#269]"
title: "Audit-index count-tiered shape + freshness hook"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
source: BACKLOG.md
derived: true
---

- [#269] [P3][S] Audit-index count-tiered shape + freshness hook (ADR-100 Q2) — apply the ADR-100 count-tiered shape to the generated `docs/audits/README.md` (fresh section = ~20 most recent; everything older → an archive **section of the index**, files never move; a `gen_audit_index.py` change) and repoint its header (currently names #212 as the open policy → ADR-100); the `audit-index-freshness` pre-commit hook (mirroring `roster-freshness` / `claude-rosters-freshness`) **LANDED EARLY 2026-07-08** per the fleet-census A-2 silent-rot ruling (the `--check` regen-and-diff is shape-agnostic, so it survives this later reshape) — this item now narrows to the count-tiered shape + header repoint. · Done when: `docs/audits/README.md` renders the count-tiered shape with the header repointed to ADR-100 (the freshness hook already landed) · refs ADR-100, scripts/gen_audit_index.py, docs/audits/README.md, docs/audits/2026-07-08-fleet-consistency-census.md A-2
