---
id: "[#471]"
title: "Generators inherit platform newline translation — a Windows regen silently EMPTIES the intake carrier"
status: closed
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#471] [P2][S] **Generators inherit platform newline translation — a Windows regen silently EMPTIES the intake carrier** — witnessed live during the intake #23 filing: `gen_intake_index.py` wrote through `Path.write_text()` in text mode, so a Windows run rewrote `docs/intake/README.md` to CRLF; `gen_intake_tree.py` splits on `\n` and matches its INTAKE-INDEX markers by EXACT equality, so a trailing `\r` makes `in_block` never fire and the residue carrier regenerates with **ZERO item nodes**. Caught only by the item-set integrity leg added after the 2026-07-31 codex-review HIGH — the exact hole it was built for, firing on its first real load. AST sweep found **11** such sites across 8 scripts (`gen_task_tree.py`/`generate_floor.py` already LF-safe — confirmed, not assumed). Second symptom: every Windows regen produced a whole-file phantom diff. · Done when: every text-mode write in `scripts/` pins `newline`, and a regression asserts it so the next generator cannot reintroduce it · refs scripts/gen_intake_index.py, scripts/gen_intake_tree.py, generate_floor._write_text_lf, #383 · kill-candidates: none — no open row owns generator write hygiene · serialize-group: audit-py
