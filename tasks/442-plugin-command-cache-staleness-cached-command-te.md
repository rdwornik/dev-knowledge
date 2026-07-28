---
id: "[#442]"
title: "Plugin command-cache staleness — cached command text can silently outlive a workflow change"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#442] [P2][M] **Plugin command-cache staleness — cached command text can silently outlive a workflow change** — witnessed 2026-07-28: a `/review-closures` invocation was served **pre-flip cached command text** (its step 4 still said to edit `BACKLOG.md`) after `52394caa` had already migrated the repo copy to the flipped source of truth; the executor followed the post-flip procedure **by judgment, not by mechanism** — nothing detected that the served text was stale, and nothing would have caught compliance with it. Scope is the MECHANISM, not this one command: cache invalidation on a command-file edit, or a version/HEAD-stamp check at load. **Class: gate-code — design review BEFORE build applies ([#438]).** · Done when: a stale cached command cannot be served unnoticed — invalidation on edit, or a load-time stamp comparison that surfaces a mismatch — with a test that seeds a stale copy · refs plugins/tier1-lifecycle/commands/review-closures.md, `52394caa`, #386 (the run that witnessed it), #438 · kill-candidates: none — a witnessed silent-staleness class in the Tier-1 command surface; no open row covers command-text delivery · serialize-group: settings-json
