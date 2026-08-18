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

- [#531] [P2][S] **Lane-grammar enforcement at PROVISIONING — the enum is checkable but nothing checks it** — `scripts/validate_branch_naming.py` transcribes the branch/worktree enum and is wired into NO gate; `/lane-boot` step 1 calls it, but a lane dispatched straight through `claude --worktree <name>` never reaches `/lane-boot`. THIRD OCCURRENCE (batches 4–5), where `batch_manifest.is_lane_merge` REFUSED two off-enum lane names and silently forfeited the ADR-110 exemption. Wire the EXISTING validator at the one point every provisioning path crosses — the `reference-transaction` git hook at the `prepared` stage. · Done when: creating a `refs/heads/worktree-lane-*` branch whose name is off-grammar is REFUSED at creation with the reason, a conforming name is unaffected, non-lane ref updates are untouched, the escape is explicit and non-silent, and `/lane-boot` step 1 is stated as the friendly pre-check rather than the enforcement point · refs scripts/validate_branch_naming.py, scripts/batch_manifest.py, ADR-110, #505 · kill-candidates: none — [#505] owns batch hygiene AFTER the fact and [#527] direct-to-main at commit time; neither covers name conformance at provisioning · serialize-group: gates · source: docs/audits/2026-08-15-verification-night3-warn-ledger.md §3.2
