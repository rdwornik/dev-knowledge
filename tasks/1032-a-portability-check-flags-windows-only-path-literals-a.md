---
id: "[#1032]"
title: "a portability check flags Windows-only path literals ([A-Z]:\\\\, $env:, powershell) in scripts/hooks/templates -- distinct from [#980]'s adapter build"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1032] [P2][M] **a portability check flags Windows-only path literals ([A-Z]:\\, $env:, powershell) in scripts/hooks/templates -- distinct from [#980]'s adapter build** - SESSION-lane-precut-landing rows-owed item 6: `[#980]` builds the path layer + Drive API/rclone adapter + container CI job, but names no lint/audit that actually FAILS on a Windows-drive-letter path, a `$env:` reference or a `powershell` invocation inside `scripts/`, `.claude/hooks/` or `templates/` -- the verification half `[#980]`'s own Done-when does not cover. Overlaps `[#980]`'s scope in intent only; file just the check. · Done when: a check (script or `audit.py` leg) fails when any of `[A-Z]:\\`, `$env:`, or a bare `powershell ` invocation appears in `scripts/`, `.claude/hooks/` or `templates/`, RED-first witnessed on a fixture; `[#980]` is referenced, not duplicated · refs `[#980]`, `to-cc/DECLARE-OFFBOX-PORTABILITY-2026-09-23.md` · kill-candidates: none -- `[#980]` builds the adapter, not this check
