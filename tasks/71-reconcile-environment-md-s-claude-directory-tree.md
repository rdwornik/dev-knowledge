---
id: "[#71]"
title: "Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents"
status: deferred
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
serialize-group: environment
generates: BACKLOG.md
---

- [#71] [P3][S] Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents (commands = codex-review + session-summary only — boot/evolve archived 2026-06-05 Phase-C3, target re-scoped 2026-06-07 groom; skills = gotchas + verify; agents/hooks already match); **+ folded from #119:** ENVIRONMENT.md's "No Codex CLI / Rejected" lines (243/255) contradict the live `/codex-review` command + `codex-review` skill (Codex installed 0.141.0) — reconcile in the same pass · Done when: the ENVIRONMENT `~/.claude/` tree matches `ls ~/.claude/{commands,skills}` and the Codex/Rejected lines are reconciled to live state · refs G6 process-hardening sweep · serialize-group: environment · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
