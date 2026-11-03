---
id: "[#1005]"
title: "Path protection comes back as `permissions.deny` rules -- no process per PreToolUse call"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#1005] [P1][M] **Path protection comes back as `permissions.deny` rules -- no process per PreToolUse call** - S2 proposed row 5: `block-onedrive.ps1` (P0 exclusion zone) and the ADR-77 transcript guard have been off since 2026-09-17 with no expiry; only a Read-deny permission still binds, and Write/Edit/Bash into the zone are guarded by nothing but the model · Done when: `permissions.deny` rules for Edit, Write and NotebookEdit cover the OneDrive exclusion path ([#865] option c) and `docs/decisions/transcripts/**` (ADR-77), each witnessed by a refused call in a throwaway session; `~/.claude/rules/core-invariants.md` is changed in the same act; the Bash gap is stated in the rule; the operator has ruled on [#865] first · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-hook-architecture.md`, `docs/audits/2026-09-23-technical-hook-architecture-appendix.md`, `[#865]`, `~/.claude/rules/core-invariants.md` · kill-candidates: none -- no open row converts these two guards to permissions.deny rules
