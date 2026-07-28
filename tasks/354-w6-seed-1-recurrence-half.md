---
id: "[#354]"
title: "W6 seed-1 recurrence half"
status: open
priority: P2
size: M
theme: "[E8] ARC-5 execution"
story: "[S21] Discharge the ARC-5 carried items that no wave has yet absorbed"
serialize-group: playbook
generates: BACKLOG.md
---

- [#354] [P2][M] W6 seed-1 **recurrence half** — build the staged-diff CO-CHANGE checker with explicit ADR-36/41/101 → PLAYBOOK/ESSENTIALS edges, so a doctrine amendment cannot land without its companion operational text. `coherence-nudge` **cannot serve this**: it only detects a *registered spec changed without a version bump*, which is a different signal (terra ruled the extension not implementable). Seed-1's **legibility half already landed** at merge `8c913a6a` (the four ARC-4 rulings inoculated into PLAYBOOK + ESSENTIALS); this is the **unbuilt enforcement half** — the reason the four rulings can silently drift back out. · Done when: a staged amendment to ADR-36/41/101 lacking a companion PLAYBOOK/ESSENTIALS edit is flagged by the checker, with a test · refs docs/audits/2026-07-19-technical-night-consolidated-cycle-close.md §3 seed 1, docs/audits/2026-07-19-codex-cycle-close-terra-review.md, scripts/coherence_nudge.py, ADR-36, ADR-41, ADR-101, 8c913a6a · kill-candidates: none — the enforcement half of seed 1; the legibility half is already merged and closes nothing here · serialize-group: playbook
