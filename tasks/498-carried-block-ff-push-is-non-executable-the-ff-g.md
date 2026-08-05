---
id: "[#498]"
title: "Carried `block-ff-push` is non-executable — the FF gate is declared, distributed, and inert on arrival"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#498] [P1][S] **Carried `block-ff-push` is non-executable — the FF gate is declared, distributed, and inert on arrival** — `.pre-commit-hooks.yaml` declares `block-ff-push` with `entry: scripts/block_ff_push.py` + `language: script`, which requires the executable bit; git records the file **100644**, missing `git update-index --chmod=+x` when it landed at `94652fdf`. The other five carried `language: script` hooks are all 100755 — one file, not a platform blindness. The hub never noticed because it runs the same script through a DIFFERENT declaration: `.pre-commit-config.yaml:164` uses `language: system`, which needs no exec bit, so the defect exists only on the distributed path. Blast radius: a consumer on an exec-bit-honouring filesystem gets a pre-push hook that exits 1 on EVERY push — loud rather than silent, but a total block rather than a selective FF refusal. Latent today only because the fleet is Windows; the catching organ (`tests/test_carrier_hooks_source.py`) fires only on POSIX, so no test on the current fleet would ever go red for this. Same declared-but-undelivered class as the 2026-06-19 ADR-85 pattern. · Done when: the exec bit is set AND a structural test asserts every `language: script` entry in `.pre-commit-hooks.yaml` points at a 100755 target — the structural form, so the next carried script cannot repeat it · refs .pre-commit-hooks.yaml, scripts/block_ff_push.py, .pre-commit-config.yaml:164, tests/test_carrier_hooks_source.py, docs/audits/2026-08-05-technical-night-batch-morning-report.md §5.1, #481 · kill-candidates: none — no open row owns carried-hook executability
