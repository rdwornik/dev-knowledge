---
id: "[#399]"
title: "`templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class)"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: handoff
generates: BACKLOG.md
---

- [#399] [P2][S] **`templates/handoff/v5/README.md.tmpl` — phantom source claim (the [#359] class)** — `protocols/HANDOFF_PROCESS.md:481` declares `docs/handoffs/README.md` is idempotently rendered "from one source" (the v5 `.tmpl`), but NO script reads the `.tmpl`: `seed_runbook.py:85/:106` generalizes from the already-RENDERED hub README; grep of scripts/ for the tmpl filename is null. A spec claiming machinery that does not exist actively misleads (phantom-enforcement class, #359). Fix one of three ways: build it (seeder/generator actually renders from the .tmpl), correct HANDOFF_PROCESS:481 to name the real source, or record accepted-with-reason — and decide the `.tmpl`'s fate (live source vs archived) in the same pass. · Done when: the claim and the mechanism agree (built, corrected, or recorded) and the `.tmpl`'s status is explicit · refs docs/audits/2026-07-22-technical-hygiene-pre-handoff-inventory.md §3, protocols/HANDOFF_PROCESS.md:481, scripts/seed_runbook.py, #359, #367 · kill-candidates: none — a #359-class instance on a different rule; #359 owns the class disposition, not this site · serialize-group: handoff
