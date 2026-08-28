---
id: "[#533]"
title: "Decompose the `audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#533] [P2][M] **Decompose the `audit.py` check monolith into `scripts/audit_checks/` — one module per check plus an ordered registry** — `scripts/audit.py` carries every `check_*` inline in one ~5000-line module, and the cost stopped being theoretical on 2026-08-16: the phase-2 batch-6 pre-dispatch matrix REFUSED to dispatch two hub lanes because both had to edit that one file — lane y's `check_hooks_armed` (`:1625`) and lane l's `check_stale_worktrees` (`:1221`) — a collision with nothing to do with either lane's subject and everything to do with module topology. Two unrelated checks cannot be worked in parallel because they share a file, so the monolith is now a throughput constraint on the batch protocol itself, not merely a legibility complaint. Ruled **D-1v2** (2026-08-16) as the STRUCTURAL fix for that class in preference to a per-batch scheduling workaround. `audit.py` becomes a THIN FACADE: the CLI, `ALL_CHECKS` and every public entrypoint keep working unchanged, because the git hooks call it and nothing outside it may need editing. The extraction is MECHANICAL — zero logic change — so the proof is a byte-comparison, not a judgement. · Done when: every mechanically-extractable check lives in `scripts/audit_checks/<check_name>.py` with the module named for the check, an ordered registry preserves today's `ALL_CHECKS` order AND count, `audit.py` retains every public entrypoint and CLI verb byte-compatibly, `audit.py health` output on an unchanged tree is BYTE-IDENTICAL before and after, targeted tests for every touched surface are green, and any check that resists mechanical extraction is LEFT IN THE FACADE and REPORTED rather than redesigned mid-lane · refs `scripts/audit.py`, `tests/test_audit.py`, D-1v2, `docs/audits/2026-08-16-technical-batch-6-manifest.md`, `docs/audits/2026-08-16-technical-533-audit-decompose-lane-contract.md`, [#531], [#505] · kill-candidates: none — no row owns check-code structure; [#505]/[#527]/[#531] own runtime gates, not module topology · serialize-group: audit-py · **Archived annotations:** `tasks/archive/533.md`
