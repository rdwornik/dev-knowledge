---
id: "[#117]"
title: "Evaluate prompt/agent-based hooks"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#117] [P3][S] Evaluate prompt/agent-based hooks (`type:"prompt"` Haiku-eval / `type:"agent"` multi-turn, experimental) — candidate: run the Tier-1 closure/triage eval in-session via a `type:"prompt"` hook instead of a Python shell-out; EXPERIMENTAL flag; GATED on the VF-1 auth check (add a trivial `type:"prompt"` PreToolUse returning approve, run any tool call, confirm NO auth error under the empty-key billing route) · Done when: VF-1 passes and a go/no-go on a prompt-hook Tier-1 eval is recorded · refs docs/audits/2026-06-07-platform-max-audit.md AD-2, VF-1, #8 · serialize-group: settings-json · UN-DEFERRED 2026-08-11 (operator ruling): peg `#270` MET at `7e4d503e` — the operator-load gauge landed and `[#270]` closed at `679d8eca`. Same treatment ARC-2 gave `[#293]` and `[#298]` when their pegs were met: un-defer, do not close — the work itself is untouched.
