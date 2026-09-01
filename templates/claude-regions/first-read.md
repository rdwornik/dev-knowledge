
In order, read:
1. This file (you're here)
2. `protocols/ESSENTIALS.md` — **SUPERSEDED, pending `[#628]`.** Not a boot read; skip it. The always-on subset is this file, and the live boot frame is `CLAUDE.md` + FUNNEL HEALTH + north-star
3. The **active** `docs/handoffs/*/` bundle — **newest by git add-date**, which is what `audit.py::_select_active_bundle` resolves and what `verify_handoff_probes`, `check_handoff_probes` and `validate_residual_completeness` already reuse; a day with more than one handoff produces `<slug>`, `<slug>-2`, … siblings and lexical order is not the rule. Start with its `HANDOFF_BOOT.md` (v5/v6/v7 bundles' operator session entry: slug · purpose · mode · destination; older bundles use `README.md`), then the canonical operator runbook `docs/handoffs/README.md` — if continuing prior session
4. Last 5 entries of `JOURNAL.md`

`PLAYBOOK.md` (hub `.dev-knowledge/protocols/`) is the universal-protocols **reference**, not a boot-time read — consult the relevant section on demand when a task needs it (this file carries the always-on subset; a consumer never copies PLAYBOOK). If a PLAYBOOK section a task needs is unavailable, proceed with the other available first-read sources and flag the gap.
