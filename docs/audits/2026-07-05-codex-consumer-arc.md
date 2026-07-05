# Codex Review — consumer-arc

**Date:** 2026-07-05
**Branch:** `feat/consumer-arc`
**HEAD:** `49d46d6`
**Diff range:** `feat/lived-sandbox-slice-b..feat/consumer-arc`
**Codex version:** codex-cli 0.141.0
**Mode:** diff-review

---

## Focus

(none specified)

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH deploy/lived_sandbox/cli.py:141 — expected live-run failures escape as tracebacks

**What:** `cmd_observe_consumer()` calls `run_consumer_arc()` without handling expected failures from auth loading, manifest loading, clone setup, or child `claude` spawn.  
**Why:** A bad consumer path, missing key, clone failure, timeout, or oracle error will crash the operator CLI instead of returning the documented controlled exit/report behavior.  
**Fix direction:** Catch the expected sandbox/oracle/runtime exceptions at the CLI boundary, print a concise stderr error, return a nonzero exit code, and add CLI tests for those failure paths.

## MEDIUM

(none)

## LOW

(none)
