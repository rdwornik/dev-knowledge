# Changelog review — 2026-06-15

**Push trigger** (#113). Operator-invoked review of tool changelogs since last review. Classification done in-session against our stack (Windows · markdown governance repo · Claude Code hooks/skills/commands/subagents/plugins/workflows · codex only via `/codex-review` on staged code diffs).

## Ranges reviewed

- **claude-code:** `2.1.169` → `2.1.177` (last reviewed `2.1.168`; installed `2.1.177`). Source: raw GitHub CHANGELOG.md.
- **codex:** `0.138.0` + `0.139.0` stable (last reviewed `0.137.0`; installed `0.136.0`). Source: `gh release view` (stable only; alphas skipped per contract). 0.139.0 is current Latest.

## Bucket counts

- ADOPT: 3 (all low/medium priority)
- OBSOLETES-WORKAROUND: 0
- STALE-NAMES: 0 (live docs)
- VERIFY: 0
- NOISE: ~96 claude-code + ~27 codex (curated sections; codex raw PR firehose not separately itemized)

## ADOPT

**1. Fable 5 is now GA — t-shirt routing doctrine doesn't account for it (UNDERUSED-NATIVE).**
- 2.1.170 introduced Fable 5 (Mythos-class, general use); 2.1.173/2.1.177 added `[1m]`-suffix auto-normalization and an **auto-mode fallback to Fable 5 when Opus 4.8 is unavailable**.
- Our routing doctrine (`ARCHITECTURE.md:323`, Appendix B / ADR-70) pins fan-out as **S=Haiku · M=Sonnet · L/judgment=Opus** — Fable 5 is absent. Whether Fable 5 earns a routing tier (e.g. a cheaper general-use M-alternative, or the documented Opus-unavailable fallback) is an **architect decision**.
- Note: the platform's *auto-mode* Opus→Fable fallback is session-level and does **not** conflict with our "no `fallbackModel` on a pinned stage" rule (ADR-80) — that rule governs pinned fan-out stages, a different mechanism. Worth stating explicitly if Fable 5 is added to the doctrine so the two aren't conflated.
- Candidate home: `ARCHITECTURE.md` Ch3 / Appendix B (model routing). **Do not implement — architect call.**

**2. Sub-agents can spawn their own sub-agents, up to 5 levels deep (2.1.172).**
- Relevant to our fan-out harnesses (`conformance-hub`, `deep-research`, Workflow patterns), which currently assume single-level subagent fan-out. A capability we don't reference in the methodology.
- Candidate home: `PLAYBOOK.md` workflow-patterns section. Low priority — our current harnesses don't obviously need depth.

**3. `disableBundledSkills` setting hides bundled skills/workflows/slash commands (2.1.169).**
- We define our own skills/commands; bundled ones add picker noise. Low-cost ergonomic adoption if the picker is cluttered.
- Candidate home: `.claude/settings.json`. Low priority.

## OBSOLETES-WORKAROUND

None. No new native feature in this range retires one of our scripts, hooks, shims, or conventions.

## STALE-NAMES

None in **live** docs/config. Checks performed:
- Hook `if`-condition fix (2.1.177) is **N/A** — our hooks use `matcher`, not `if` (`.claude/settings.json:5,17,28`). No drift.
- Model-name references (124 file hits) are confined to immutable transcripts/audits/handoffs (supersede-not-edit lifecycle, not "wrong live name"). The one live routing reference (`ARCHITECTURE.md:323`) uses generic family names (Haiku/Sonnet/Opus) that remain valid — the Fable 5 gap is the ADOPT item above, not a rename drift.
- `availableModels`/`enforceAvailableModels` managed settings (2.1.174/2.1.175) — we don't configure model allowlists. N/A.

## VERIFY

None. (Workflow `Date.now()`/`Math.random()` validation hardening in 2.1.172 is moot — our workflow scripts are inline/ephemeral, none stored in-repo to drift against.)

## NOISE (counted, not itemized)

- **claude-code (~96):** Bedrock/GovCloud/Vertex/Foundry credential & region handling; enterprise managed-settings & MCP-policy enforcement; Remote Control pairing/disconnect; background daemon/session lifecycle & auto-update; tmux/SSH/WSL/VSCode-terminal/Linux-sandbox fixes; OTEL metrics; idle-CPU & long-conversation perf; plugin-marketplace search/navigation; UI cosmetics (cursor/footer/spinner/contrast); `/cd`, `--safe-mode`, self-hosted-runner `post-session` hook; memory team-stores in remote sessions; misc Windows daemon internals.
- **codex (~27 curated):** `/app` Desktop handoff (macOS/Windows); `/goal` multiline-paste & idle-turn fixes; multi-agent v2; plugin-marketplace `--json` & cached-catalog; sandbox/proxy networking; image-edit path routing; code-mode standalone web search; `codex doctor` env reporting; `oneOf`/`allOf` tool-schema support; v8 toolchain bump; AGENTS.md discovery (we retired AGENTS.md, ADR-53). None intersect our `/codex-review`-only usage.

## Operator routing

One item wants an architect decision: **ADOPT #1 (Fable 5 in the t-shirt routing doctrine)** — flag for the operator + browser-chat architect. ADOPT #2 (subagent depth) and #3 (`disableBundledSkills`) are low-priority capture-only; no decision pressure. Nothing else queued. No BACKLOG edits made — this digest is the artifact.
