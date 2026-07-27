---
id: "[#117]"
title: "Evaluate prompt/agent-based hooks"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
source: BACKLOG.md
derived: true
---

- [#117] [P3][S] Evaluate prompt/agent-based hooks (`type:"prompt"` Haiku-eval / `type:"agent"` multi-turn, experimental) — candidate: run the Tier-1 closure/triage eval in-session via a `type:"prompt"` hook instead of a Python shell-out; EXPERIMENTAL flag; GATED on the VF-1 auth check (add a trivial `type:"prompt"` PreToolUse returning approve, run any tool call, confirm NO auth error under the empty-key billing route) · Done when: VF-1 passes and a go/no-go on a prompt-hook Tier-1 eval is recorded · refs docs/audits/2026-06-07-platform-max-audit.md AD-2, VF-1, #8 · serialize-group: settings-json · DEFER — peg: #270
