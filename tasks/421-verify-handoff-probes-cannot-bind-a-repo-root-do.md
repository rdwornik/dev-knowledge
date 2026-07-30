---
id: "[#421]"
title: "`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the leading dot"
status: open
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#421] [P2][S] **`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the leading dot** — **ABSORBED into [#446] as a leg** (intake #18 A11); this row tracks the defect until that arc lands or re-defers it by ruling. Mechanism (VERIFIED): `_FILE_RE` (`scripts/verify_handoff_probes.py:54`) admits a dot in its directory alternation but not in the final segment, so a backticked `` `.pre-commit-config.yaml` `` tokenizes dot-stripped and the probe FAILs `anchor-missing` though the file exists. Scope is the repo-root dotfile ONLY — a dot-*directory* path binds. A second variant (a backticked `#id` parsing as a header anchor via `header_tokens`) rides the same absorption · Done when: a probe row citing a backticked repo-root dotfile resolves and passes, with a test pinning `.pre-commit-config.yaml` and a dot-directory regression guard — OR the leg is re-deferred by ruling inside [#446] · refs `scripts/verify_handoff_probes.py:54` `_FILE_RE`, `file_tokens`, `header_tokens`, protocols/HANDOFF_PROCESS.md §5, #446 · kill-candidates: none — #404 is a disjoint defect; no open task owns the tokenizer · serialize-group: handoff
