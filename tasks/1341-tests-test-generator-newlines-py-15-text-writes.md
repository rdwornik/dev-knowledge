---
id: "[#1341]"
title: "tests/test_generator_newlines.py: 15 text writes in scripts/ inherit platform newline translation, and the count is growing"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1341] [P2][S] **tests/test_generator_newlines.py: 15 text writes in scripts/ inherit platform newline translation, and the count is growing** - DCT D6. `test_every_text_write_in_scripts_pins_newline` finds 15 `write_text()` / `open(..., 'w')` sites without `newline=` (the AST sweep, no exemption list); the registry recorded 14. The 15th arrived in `scripts/dispatch.py` (1 -> 2 sites, 2cb47aee and 193e9007, merged at f70154b7); the first red is e580518b. On Windows each such site writes CRLF where a parser expects LF. **A real defect, still to be fixed**: held at 15 under a ceiling (AM2-3), owner `rob`, expiry 2026-10-17 · Done when: every text write in `scripts/` pins `newline="\n"`, the test is green on both CI legs, and the registry entry is removed · touches: `scripts/dispatch.py` and the other named write sites, `logs/KNOWN-REDS-REGISTRY.json` · kill-candidates: none -- no open row owns the newline sweep · refs `tests/test_generator_newlines.py`, `scripts/dispatch.py`, `logs/KNOWN-REDS-REGISTRY.json` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
