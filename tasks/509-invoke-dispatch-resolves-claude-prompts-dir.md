---
id: "[#509]"
title: "`Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#509] [P3][S] **`Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`** — the dispatch convention (`protocols/PLAYBOOK.md` Ch8) writes a prompt path as `<PROMPTS_DIR>\<file>` (default `~/Downloads`, override `$env:CLAUDE_PROMPTS_DIR`), but the wrapper hands `-Prompt` to `claude --bg` verbatim with no resolver — the token arrives unexpanded and the operator expands it by hand. **Cross-repo: filed from `.dev-knowledge`, built in `win-tooling`; no hub code changes.** Either expand the token in the prompt text or add a `-Contract <file>` param. · Done when: the wrapper resolves `<PROMPTS_DIR>` / `$env:CLAUDE_PROMPTS_DIR` (default `~/Downloads`) in either shape, with a test, and a dispatch line in variable form launches unedited · refs win-tooling `scripts/dispatch/Invoke-Dispatch.ps1`, `protocols/PLAYBOOK.md` Ch8, [#505] clause 1, `docs/audits/2026-08-07-technical-batch-2-packet.md` §7 · kill-candidates: none — no open row owns the dispatch wrapper
