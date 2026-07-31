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

- [#465] [P2][M] **fleet-audit writer integrity — skips recorded as PASS, same-day overwrite deletes findings, hub-detection flap** — fleet-audit deep review 2026-07-31 (full read of the latest 14 digests + their superseded same-day git blobs): (1) skipped checks are emitted `pass` — live today (`ecosystem/win-tooling/history/2026-07-31.md`: `hooks_armed | pass | hub-only — … skipped`), and status is inconsistent for identical evidence (`handoff_version_stamp` PASS vs `handoff_tag_canonicity` N/A on the same "nothing to validate"), so pass counts are inflated; (2) a date's digest/history file is OVERWRITTEN by later same-day runs — the committed 07-13 and 07-16 digests each silently dropped 14 WARNs present in their earlier same-day runs; (3) the hub intermittently resolved as not-the-hub on the branch (9 hub-only checks skipped-as-PASS on 6 of 8 final fleet runs; correct 07-08/07-09 and today) — the known GIT_DIR/commit-context class in a new habitat; (4) `handoff_tag_canonicity` self-disabled on the hub the whole window and today ("§3.1 section not found (consolidated?)"). An archive that drops findings and inflates passes cannot be ADR-80's durable record. · Done when: a skip is never emitted as `pass` (with a test), same-day runs append/version rather than overwrite or last-run-wins is recorded accepted, the hub-resolution flap has a root cause + regression test, and the tag-canonicity N/A is fixed or retired · refs scripts/audit.py, ADR-80, #460, ecosystem/win-tooling/history/2026-07-31.md · kill-candidates: none — [#460] rules the lane's fate; this is the writer's correctness, no open row covers it · serialize-group: audit-py
