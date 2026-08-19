---
id: "[#534]"
title: "`scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#534] [P2][S] **`scripts/audit.py:<line>` locators on four open rows died at the `[#533]` decomposition** — `audit.py` went 5243 → 4271 lines when 16 of 43 checks moved to `scripts/audit_checks/`, and every row pinning it by line number now points somewhere else. Measured live: `[#417]` pins `:4751-4760`, **past EOF**, for a scope list that actually sits at `:3779-3788`; `[#477]` pins `:2300` for `repo_key = _git_repo_root_name(...)`, now `:1862`; `[#357]` pins `:363` for `discover_repos`, now `:490`; `[#358]` pins `:2425` for the blocking `ALL_CHECKS` registration, now `:3405`. Nothing detects this, and `[#417]` is simultaneously proposed NOW-CLOSABLE by the closing campaign, so a dead locator is about to be ratified as met. · Done when: each of `[#357]` `[#358]` `[#417]` `[#477]` cites its construct by anchor text (or by a locator that resolves live), and a check FAILs on a `scripts/*.py:<line>` locator in `tasks/` that does not resolve to its named construct · refs scripts/audit.py, scripts/audit_checks/, tasks/357-*, tasks/358-*, tasks/417-*, tasks/477-*, #533, #483, docs/audits/2026-08-19-technical-n4-grooming-wave1.md §10 (independent corroboration on a FRESH population: 6 dead-or-drifted locators across 5 rows, 6.9% of 72 git-silent rows — [#422]×2, [#431], [#317], [#496], [#170]; [#431] is the dangerous shape, its cited line still resolves but now sits inside a section headed RETIRED) · kill-candidates: none — `[#483]`'s preflight leg surfaces stale locators in contracts, not in BACKLOG rows; `[#533]` owns the move, not its fallout · source: docs/audits/2026-08-16-verification-nb6-backlog-truth.md §1.8
