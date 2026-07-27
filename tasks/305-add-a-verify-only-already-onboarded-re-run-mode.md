---
id: "[#305]"
title: "Add a verify-only / already-onboarded re-run mode to the onboarding runbook"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: architecture
source: BACKLOG.md
derived: true
---

- [#305] [P3][S] Add a verify-only / already-onboarded re-run mode to the onboarding runbook — the runbook's only path is the `deploy/tool.py --execute` converge, which requires a clean consumer tree and hits the prune-refusal on methodology-removed components. There is no "just re-verify, write nothing" mode, yet every future re-verify is verify-heavy. Document a verify-only re-run (assess + the #215 battery, no converge) and let the read-only assess run on a dirty tree. **DEFERRED 2026-07-25:** the doc half is writable now, but clause 2 is a CODE change — `git_tree_clean` sits inside `preflight()` (deploy/tool.py:275-278), which runs for assess AND execute, so a dirty tree raises `PreflightError` before any read-only plan prints. Closing the doc half alone leaves a half-true Done-when. · Done when: the runbook documents a verify-only re-run path AND assess runs on a dirty tree · refs protocols/REPO_ONBOARDING.md, deploy/tool.py, #215, #304 · kill-candidates: none — sibling #304 closed doc-only this arc; this did NOT fold in, because clause 2 needs code · serialize-group: architecture · DEFER — peg: a preflight split separating the assess gate from the execute gate
