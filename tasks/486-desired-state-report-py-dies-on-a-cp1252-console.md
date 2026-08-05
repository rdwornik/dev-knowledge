---
id: "[#486]"
title: "`desired_state_report.py` dies on a cp1252 console — U+21C4 in its own HONEST LIMITS text"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#486] [P3][S] **`desired_state_report.py` dies on a cp1252 console — U+21C4 in its own HONEST LIMITS text** — reproduced live by the 2026-08-03 caches wave while executing the [#383] runs: `UnicodeEncodeError: 'charmap' codec can't encode character '⇄'`. Same class as [#470] (`audit.py checks`, U+2192) but a DIFFERENT script and a DIFFERENT glyph, so [#470]'s ASCII-swap does not cover it; both wave runs had to be forced under `PYTHONUTF8=1`, and the wave recorded the defect rather than fixing it (it does not own the script). Ruled the one honest-filing exception to this window's no-new-filings rule (Q2). · Done when: the U+21C4 is ASCII-swapped and a regression asserts every console-emitted line of `desired_state_report.py` is cp1252-encodable · refs scripts/desired_state_report.py, docs/audits/2026-08-03-technical-383-caches-wave-record.md §5.4, #470 · kill-candidates: none — [#470] owns `audit.py cmd_checks`, a different script and glyph
