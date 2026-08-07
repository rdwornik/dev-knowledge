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

- [#509] [P3][S] **`Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`** — the dispatch convention landed 2026-08-07 (`protocols/PLAYBOOK.md` Ch8 "Dispatch prompts and the contract of record") writes a prompt path as `<PROMPTS_DIR>\<file>`, defaulting to `~/Downloads` and overridden by `$env:CLAUDE_PROMPTS_DIR`, so a dispatch line stays portable across machines. The wrapper joins its `-Prompt` arguments (`$promptText = $Prompt -join ' '`) and hands the string to `claude --bg` verbatim, so a `<PROMPTS_DIR>` token arrives at the session unexpanded and the operator expands it by hand — the convention has no resolver. **Cross-repo row: filed from `.dev-knowledge`, built in `win-tooling`; no hub code changes.** Either shape closes it — expand the token inside the prompt text, or take a `-Contract <file>` parameter resolved against the prompts dir. · Done when: the wrapper resolves `<PROMPTS_DIR>` / `$env:CLAUDE_PROMPTS_DIR` (default `~/Downloads`) in either shape, with a test, and a dispatch line written in the variable form launches unedited · refs win-tooling `scripts/dispatch/Invoke-Dispatch.ps1`, `protocols/PLAYBOOK.md` Ch8, [#505] clause 1, `docs/audits/2026-08-07-technical-batch-2-packet.md` §7 · kill-candidates: none — no open row owns the dispatch wrapper
