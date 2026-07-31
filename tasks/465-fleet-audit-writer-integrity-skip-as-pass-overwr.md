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

- [#465] [P2][M] **fleet-audit writer integrity — skips recorded as PASS, same-day overwrite deletes findings, hub-detection flap** — deep review of the branch dailies plus their superseded same-day git blobs: (1) skipped checks are emitted `pass` (live today in the baseline dailies) and status is inconsistent for identical no-op evidence, inflating pass counts; (2) a date's digest/history file is OVERWRITTEN by later same-day runs — two committed digests each silently dropped 14 WARNs present in their earlier same-day runs; (3) the hub intermittently resolved as not-the-hub (9 hub-only checks skipped-as-PASS on 6 of the final 8 fleet runs — the known commit-context class); (4) `handoff_tag_canonicity` self-disabled on the hub. An archive that drops findings and inflates passes cannot be ADR-80's durable record. · Done when: a skip is never emitted `pass` (with a test), same-day runs append/version or last-run-wins is recorded accepted, the flap has a root cause + regression test, and the tag-canonicity N/A is fixed or retired · refs scripts/audit.py, ADR-80, #460 · kill-candidates: none — [#460] rules the lane's fate; this is writer correctness · serialize-group: audit-py
