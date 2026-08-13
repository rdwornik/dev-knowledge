---
id: "[#506]"
title: "Whole-set P10 grooming arc — the open set is unreconciled"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#506] [P2][M] **Whole-set P10 grooming arc — the open set is unreconciled** — the P10 probe contract binds a successor to groom **the whole open set** at boot ("no open `#id` may pass unreconciled"); measured this window: **189 of 200 open rows uncovered** since the last whole-set dossier, the latest window's grooming having reached **11 open ids**. That bounded discharge is lawful per the STANDING_RULINGS C clause only *on the condition that the detection limit is named at seal* — this row IS that limit, named as work. **Split by who can do it:** evidence-sheet generation is READ-ONLY and may run parallel to any batch; the verdict per id is architect adjudication and serializes. · Done when: a `docs/audits/` sheet carries one row per `status: open` task with its last-touch date and closing-merge cross-check (count matching the live open count at generation time), each id carries a live / dead / awaiting-ruling verdict, and every id verdicted dead is closed per ADR-65 or named as deferred · footprint: `tasks/`, `BACKLOG.md`, one `docs/audits/` sheet · refs P10 probe contract, `docs/audits/2026-07-31-technical-p10-grooming-dossier.md`, ADR-65, #348 · kill-candidates: none — [#348] owns the grooming CADENCE as configuration, not the whole-set discharge
