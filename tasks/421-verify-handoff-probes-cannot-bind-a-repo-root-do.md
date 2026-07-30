---
id: "[#421]"
title: "`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the leading dot"
status: closed
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#421] [P2][S] **`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the leading dot** — ABSORBED into [#446] as R7 Option B (intake #18 A11), BOTH variants: `_FILE_RE` dropped the dot in the FINAL path segment, and `header_tokens` mis-read a backticked `#id` as a markdown anchor. · Done when: a probe row citing a backticked repo-root dotfile resolves and passes, with a test pinning `.pre-commit-config.yaml` and a dot-directory regression guard — **MET** · refs `scripts/verify_handoff_probes.py` `_FILE_RE`/`header_tokens`, protocols/HANDOFF_PROCESS.md §5, #446 · kill-candidates: none · serialize-group: handoff · **CLOSED 2026-07-31** (architect-adjudicated, merge `7f8a0473`), pointing at the two RED-first frozen tests `test_fr7_v1_file_re_binds_repo_root_dotfiles` + `test_fr7_v2_header_tokens_ignores_a_bare_id`. Hardened past original scope by codex F4: whole-token boundary + the resolver's `..` fallback guard.
