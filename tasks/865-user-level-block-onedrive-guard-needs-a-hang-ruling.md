---
id: "[#865]"
title: "The user-level block-onedrive.ps1 PreToolUse guard launches powershell per call and can hang the same way -- it needs a ruling"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#865] [P2][S] **The user-level block-onedrive.ps1 PreToolUse guard launches powershell per call and can hang the same way -- it needs a ruling** - Operator order 2026-09-17. The emergency disable (`33246c0a`) removed every PreToolUse hook in the REPO `.claude/settings.json`, and it **deliberately left untouched** the user-level `~/.claude/settings.json` guard `powershell -ExecutionPolicy Bypass -File ~/.claude/hooks/block-onedrive.ps1` (matcher `Bash|PowerShell|Edit|Write|NotebookEdit|Read`, **no `timeout` declared**). It spawns a fresh powershell on every matched call, which is the spawn shape that produced the suspended orphans in `[#863]`, so it is exposed to the same wedge on every repo on the machine, not only this one. It is ALSO the enforcement leg of core-invariant #1 (the OneDrive exclusion zone). Removing it trades a wedge risk for a data-loss risk, and that trade is not the seat's to make. It is recorded here so it is not forgotten. **State at filing (census 2026-09-17 ~11:35):** zero suspended or orphaned `block-onedrive.ps1` processes observed, so exposure is by shape, not yet by incident. · Done when: the operator rules one of: (a) keep it as-is until `[#863]`'s watchdog lands and covers user-level hooks too; (b) bound it under `[#808]`, with its fail posture on timeout stated, since fail-OPEN on an exclusion-zone guard is itself a ruling; or (c) replace the per-call powershell spawn with a cheaper form (e.g. a `permissions.deny` rule for the tool classes it can express, alongside the existing `Read(...OneDrive - Blue Yonder...)` deny). The ruling is recorded with its reason, and any edit to the hook edits `~/.claude/rules/core-invariants.md` in the same act (rule and hook MUST agree) · refs `~/.claude/settings.json`, `~/.claude/hooks/block-onedrive.ps1`, `~/.claude/rules/core-invariants.md` section 1, `[#289]` (deferred: hub-own the guard), `[#863]`, `[#808]` · kill-candidates: none -- `[#289]` is ownership of the guard, this is its hang exposure; a ruling here may fold into `[#289]` when it is un-deferred · source: operator order 2026-09-17
