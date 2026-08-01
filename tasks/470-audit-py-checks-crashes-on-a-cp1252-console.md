---
id: "[#470]"
title: "`audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#470] [P3][S] **`audit.py checks` crashes mid-listing on a cp1252 console — one U+2192 glyph** — REPRODUCED live this window, not inherited: `python scripts/audit.py checks` dies with `UnicodeEncodeError: 'charmap' codec can't encode character '→'`. `cmd_checks` echoes each check's FIRST docstring line via `click.echo`; enumerating every `ALL_CHECKS` docstring finds exactly ONE non-cp1252 character in that position — the `→` in `check_doc_code_edge` ("#194 doc→code declared-edge integrity"). The other non-ASCII first lines use `—` (0x97) and `§` (0xA7), both cp1252-encodable and harmless. Same defect class as the ASCII `->` swap already made once at `633e44a`; the earlier `PYTHONUTF8=1` probe workaround was moved to prose because an env-prefix broke probe parsing, so NO live mitigation is in place. · Done when: the U+2192 is ASCII-swapped and a regression asserts every `ALL_CHECKS` docstring first line is cp1252-encodable · refs scripts/audit.py cmd_checks, tests/test_doc_code_edge.py, #457 · kill-candidates: none — the existing cp1252 test covers Finding fields, not the `checks` listing path · serialize-group: audit-py
