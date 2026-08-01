---
id: "[#465]"
title: "fleet-audit writer integrity — leg 1 DONE, legs 2-4 open"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#465] [P2][M] **fleet-audit writer integrity — leg 1 DONE, legs 2-4 open** — **(1) DONE** (`80e743aa`): a skip is no longer emitted `pass`. 16 sites retagged to `n/a`/`unavailable`; a STRUCTURAL RED-first test sweeps all `ALL_CHECKS` so a new pass-with-skip is caught on landing. Exposed + fixed two couplings: `enforcement_coverage` CLASSIFIED organs on the buggy `pass`+hub-only signal, and a blanket retag flattened `reconciled_versions`, whose Finding is conditional (matched edges = a true pass). **REMAINING — (2)** a date's digest/history is OVERWRITTEN by later same-day runs (two digests each dropped 14 WARNs); **(3)** the hub intermittently resolves as not-the-hub (9 hub-only checks were skipped-as-PASS, 6 of the last 8 runs) — leg 1 makes the flap VISIBLE, not fixed; **(4)** `handoff_tag_canonicity` self-disabled. · Done when: same-day runs append/version or last-run-wins is accepted on record, the flap has a root cause + regression, and tag-canonicity is fixed or retired · refs scripts/audit.py, docs/audits/2026-08-01-technical-night-batch-l6-460-decision-pack.md, #460 · kill-candidates: none — [#460] rules the lane; this is writer correctness · serialize-group: audit-py
