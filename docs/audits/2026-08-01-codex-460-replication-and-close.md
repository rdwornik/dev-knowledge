# Codex Review — 460-replication-and-close

**Date:** 2026-08-01
**Branch:** `feat/460-replication-and-close`
**HEAD:** `e4d3a920`
**Diff range:** `main..feat/460-replication-and-close`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### scripts/audit.py:3130 — Replication status relies on a remote-tracking ref that the new push does not maintain

**What:** The alarm reads `refs/remotes/origin/automation/fleet-audit`, but `_push_routine_branch` only pushes the remote ref and never fetches or otherwise refreshes that local tracking ref.  
**Why:** A successful push can leave the alarm reporting stale lag (eventually failing while replication is healthy); a first failed push with no tracking ref is reported as `n/a`, disabling the persistent backstop. The new fixture also pushes without establishing/fetching a tracking ref, so its expected green result is not valid.  
**Fix direction:** Establish and refresh the local tracking ref after a successful push, and treat a local durable branch with no expected remote-tracking ref as a replication problem rather than `n/a`.

## Medium

(none)

## Low

(none)