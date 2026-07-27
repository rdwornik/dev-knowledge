---
id: "[#112]"
title: "adr_amend helper + ADR immutable-zone extension"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: claude-md
depends-on: "#23"
source: BACKLOG.md
derived: true
---

- [#112] [P2][M] adr_amend helper + ADR immutable-zone extension — `scripts/hooks/adr_amend.py` becomes the ONLY sanctioned writer of an Amendment/status line on an existing ADR (canonical format from ADR-68 + HANDOFF v4.3 Amendment A); extend `block_immutable_edits.py` to deny every OTHER in-place ADR edit (fail-closed); resolve the CLAUDE.md §5 self-contradiction ("supersede with a new file or in-file marker; never edit in place" → "append-only via the helper"); includes the CLAUDE.md end-to-end re-read + `last_reviewed` restamp · absorbs #105 (ADR-edit PreToolUse guard, fail-closed) + #157 (§4/§5 file-lifecycle collapse) · Done when: an in-place ADR edit NOT routed through the helper is blocked, a helper-written Amendment passes, and CLAUDE.md §5 is de-contradicted + restamped · Design caveat (live): a native `permissions.deny` path-glob on the transcripts/ADR zones is **defense-in-depth ONLY** — never a replacement for the PreToolUse guards (deny-globs are bypassable and cannot express exists-deny/new-allow; native OS sandbox is not available on native Windows, so the guards stay) · refs ADR-77, #105, #23, ADR-68 · depends-on: #23 · serialize-group: claude-md
