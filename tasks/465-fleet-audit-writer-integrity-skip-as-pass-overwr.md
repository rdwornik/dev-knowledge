---
id: "[#465]"
title: "fleet-audit writer integrity — skips recorded as PASS, same-day overwrite deletes findings, hub-detection flap"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#465] [P2][M] **fleet-audit writer integrity — skips recorded as PASS, same-day overwrite deletes findings, hub-detection flap** — from the dailies + superseded same-day git blobs: **(1)** skips emitted `pass`, inflating pass counts — **LIVE NOW (carve-out): it sits in `audit.py` and corrupts EVERY consumer of check results, so NOT sequenced behind [#460]**; **(2)** a date's digest/history is OVERWRITTEN by later same-day runs (two digests each dropped 14 WARNs); **(3)** the hub intermittently resolved as not-the-hub (9 hub-only checks skipped-as-PASS, 6 of the last 8 runs); **(4)** `handoff_tag_canonicity` self-disabled. Legs 2–4 UNBLOCKED: [#460] closed keeping the lane, so the writer stays and is fixable now. Evidence + 51-commit gap: L6 pack in refs. · Done when: a skip is never emitted `pass` (with a test), same-day runs append/version or last-run-wins is accepted on record, the flap has a root cause + regression, and tag-canonicity is fixed or retired · refs scripts/audit.py, docs/audits/2026-08-01-technical-night-batch-l6-460-decision-pack.md, #460 · kill-candidates: none — [#460] rules the lane; this is writer correctness · serialize-group: audit-py
