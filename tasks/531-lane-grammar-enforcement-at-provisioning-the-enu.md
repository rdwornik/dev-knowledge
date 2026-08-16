---
id: "[#531]"
title: "Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: gates
generates: BACKLOG.md
---

- [#531] [P2][S] **Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it** — `scripts/validate_branch_naming.py` transcribes the branch/worktree enum and is wired into NO gate (its own docstring: "READ-ONLY, AND WIRED INTO NO GATE"); `/lane-boot` step 1 calls it, but a lane dispatched straight through `claude --worktree <name>` never reaches `/lane-boot`. THIRD OCCURRENCE: batch-4 W4/W6 (resolved by dropping both lanes from the roster), batch-4 `lane-a-514-lane-regex`, and batch-5 lanes S (`worktree-lane-s-w20-draft-landing`, id slot reads `w20`) + R (`worktree-lane-r-gateclose-drain8`, no id slot) — where `batch_manifest.is_lane_merge` REFUSED both, silently forfeiting the ADR-110 exemption and surfacing as a would-be `check_journal_spine_anchor` FAIL at merge #1 of 7 (batch-5 packet §1a, resolved by anchoring, not by renaming). The defect is not either name: an off-enum name is freely creatable and loses the exemption without saying so. Wire the EXISTING validator at the one point every provisioning path crosses — the `reference-transaction` git hook at the `prepared` stage, measured to refuse `worktree-lane-w20-draft-landing` while admitting `worktree-lane-a-505-batch-protocol` and leaving ordinary commits untouched (evidence: `docs/audits/2026-08-15-verification-night3-warn-ledger.md` §3.2). · Done when: creating a `refs/heads/worktree-lane-*` branch whose name is off-grammar is REFUSED at creation with the reason, a conforming name is unaffected, non-lane ref updates are untouched, the escape is explicit and non-silent, and `/lane-boot` step 1 is stated as the friendly pre-check rather than the enforcement point · refs scripts/validate_branch_naming.py, scripts/batch_manifest.py, .claude/commands/lane-boot.md, ADR-110, #505 · kill-candidates: none — [#505] owns batch hygiene AFTER the fact (`check_stale_worktrees`, WARN-tier by ruling) and [#527] owns direct-to-main at commit time; neither covers name conformance at provisioning, and the packet's W3 states no row exists · serialize-group: gates
