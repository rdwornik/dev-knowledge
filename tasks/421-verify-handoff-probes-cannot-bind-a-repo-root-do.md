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

- [#421] [P2][S] **`verify_handoff_probes` cannot bind a repo-root dotfile — the tokenizer drops the leading dot** (surfaced 2026-07-25 cutting the `2026-07-25-ai-council-architect` bundle; mechanism VERIFIED against source, scope NARROWED from the first report): `_FILE_RE` (`scripts/verify_handoff_probes.py:54`) is `(?:[\w.-]+/)*[\w-]+\.(?:py|md|ya?ml|toml|json|sh|ps1)` — the *directory* alternation `[\w.-]+` admits a dot, but the **final segment** `[\w-]+` does not, so a backticked `` `.pre-commit-config.yaml` `` tokenizes as `pre-commit-config.yaml`, resolves nowhere, and the probe FAILs `anchor-missing` although the file exists. **Scope is the repo-root dotfile only** — verified empirically: `.claude/settings.json` and `scripts/audit.py` bind correctly, while `.pre-commit-config.yaml`, `.gitignore.yaml`, `.env.yaml` all lose the dot. So no probe in any bundle can currently anchor to a root dotfile, and `.pre-commit-config.yaml` is exactly the surface a gates/hooks probe wants to cite. Today's only workaround is to un-backtick the path, which costs the probe its anchor check · Done when: a probe row citing a backticked repo-root dotfile resolves and passes, with a test pinning `.pre-commit-config.yaml` (and a dot-directory path kept passing as a regression guard) · refs `scripts/verify_handoff_probes.py:54` `_FILE_RE`, `file_tokens`, protocols/HANDOFF_PROCESS.md §5 (the anti-bluff anchor contract this weakens) · kill-candidates: none — #404 is the other live `verify_handoff_probes` defect but is mode-blind SUPPLEMENT framing, a disjoint mechanism in a different file; no open task owns the tokenizer · serialize-group: handoff
