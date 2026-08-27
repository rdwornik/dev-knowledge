---
id: "[#269]"
title: "Audit-index count-tiered shape + freshness hook"
status: deferred
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#269] [P3][S] Audit-index count-tiered shape + freshness hook (ADR-100 Q2) — apply the ADR-100 count-tiered shape to the generated `docs/audits/README.md` (fresh section = ~20 most recent; everything older → an archive **section of the index**, files never move; a `gen_audit_index.py` change) and repoint its header (currently names #212 as the open policy → ADR-100); the `audit-index-freshness` pre-commit hook (mirroring `roster-freshness` / `claude-rosters-freshness`) **LANDED EARLY 2026-07-08** per the fleet-census A-2 silent-rot ruling (the `--check` regen-and-diff is shape-agnostic, so it survives this later reshape) — this item now narrows to the count-tiered shape + header repoint. · Done when: `docs/audits/README.md` renders the count-tiered shape with the header repointed to ADR-100 (the freshness hook already landed) · refs ADR-100, scripts/gen_audit_index.py, docs/audits/README.md, docs/audits/2026-07-08-fleet-consistency-census.md A-2 · **HELD 2026-08-27** (K2 conditional, night-harvest adjudication; C4 census row 7) — the condition was tested and **does not hold**, so the row stays open. The census leaned CLOSE on *'both Done-when legs may be discharged'* and named the settling test: one read of `docs/audits/README.md`. Run: the generated header states verbatim that *'the count-tiered index shape ADR-100 also names is [#269] and is NOT built — this index groups by month'*. So **leg 1 (count-tiered shape rendered) is NOT met** — the generator itself says so. Leg 2 (header repointed to ADR-100) IS met: the header names ADR-100 and no longer names `#212`. One of two legs, therefore HOLD. Recorded so the cheapest verdict on the list is not re-run a third time. · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, X1). Peg: **building the ADR-100 count-tiered shape in `gen_audit_index.py`** — measured absent this session; `docs/audits/README.md`'s own generated header states it is NOT built. The header-repoint leg is already discharged, so this row is now one leg wide.
