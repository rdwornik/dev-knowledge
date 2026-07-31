---
id: "[#453]"
title: "Cloud night-run runbook — the container gaps that silently degrade an unattended session"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: environment
generates: BACKLOG.md
---

- [#453] [P2][M] **Cloud night-run runbook — the container gaps that silently degrade an unattended session** — the 2026-07-31 cloud night batch hit three environment gaps, each recorded not skipped. (1) The container arrived a **SHALLOW CLONE**, grafted mid-window, which made `canonical_freshness` hard-FAIL on `VISION.md` because the graft point looked like its last edit; `git fetch --unshallow` cleared it, and the closure scan needed a full-history re-run — a freshness organ that LIES on a shallow checkout is the trap, not the FAIL. (2) The container shipped uv 0.8.17 against the ADR-106 `==0.11.19` pin and `uv self update` could not reach the pinned version. (3) `audit-health` exits 1 on `repos registered (none)` because the sibling repos are absent, forcing a recorded `--no-verify` commit; every CONTENT gate passed. · Done when: a cloud-session runbook records all three gaps with their workarounds AND the unshallow + uv-pin legs are mechanized as a session preflight, or each is recorded accept-as-is with reason · refs ADR-106, scripts/audit.py, protocols/SESSION_SETUP.md · kill-candidates: none — no open task owns cloud-container preflight · serialize-group: environment
