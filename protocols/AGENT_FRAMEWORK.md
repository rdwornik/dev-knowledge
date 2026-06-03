<!-- scope: meta -->

# Agent Framework — v0.1 stub

**Status:** v0.1 stub, NOT implemented. Anchored here to track operator's strongest structural signal from the 2026-05-29 marathon session, so it isn't lost between sessions.

## The problem

Operator's exact words (2026-05-29, late session): *"musimy zbudować agent framework, który pewne rzeczy, żebym nie musiał po prostu powtarzać."*

The pattern: advisory rules in CLAUDE.md / PLAYBOOK / ESSENTIALS / ADRs that need enforcement, but operator has to repeat them across sessions because there's no gate. Examples observed in 2026-05-29 session alone:

- "Verify existing convention before emitting new folder name" — 3× violated in 24h (`docs/strategic/`, `_scratch/`, two-cluster interview design)
- "Choose model per task; never default to Sonnet for judgment-heavy work" — default-Sonnet pattern recurred multiple times
- "Sage tagging: witnessed vs recall distinction" — witnessed-conflation drift caught by Phase 2 verification (aborted-folder claim)
- "Hard-metric closure, not easy-metric" — recurring failure mode named in ecosystem audit ML-2

## Design constraints (informal, captured for future)

The framework, when designed, must:

- **Pre-flight check before CC prompts** — agent layer between architect (browser chat) and CC that verifies structural conventions, naming patterns, model-selection rationale BEFORE prompt reaches CC
- **Tag-lint at handoff time** — automated check that sage interview answers tag claims consistently with the four-tag discipline (extends `audit.py` check #9)
- **Structural-convention verification** — automated check that proposed paths/folders exist in established conventions OR carry explicit operator approval
- **Not orchestration** — Layer-2 invariant remains; agent framework is validation/lint, not autonomous execution
- **Read-only enforcement layer** — informs architect, doesn't act unilaterally

## Future work pointer

This stub is a placeholder. Actual agent framework requires:

1. **AI Council debate** on architecture: scope, layer, where it runs (Layer 1 pre-prompt vs Layer 2 lint vs new layer in `~/.claude/` runtime config)
2. **Pilot implementation** likely as `scripts/agent_check.py` (read-only validator) or `~/.claude/` hook
3. **Integration** with `audit.py` health gate (a new check appended to `ALL_CHECKS` — run `py scripts/audit.py checks` for the live set, so this count can't re-drift)
4. **Eval suite** validating the agent layer catches the named anti-patterns

Not yet a discrete `BACKLOG.md` item — this stub is the anchor until the framework is scoped (related open items: `[#1]` triangulation-to-every-handoff, which names the agent-framework as one surface; `[#8]` lifecycle hooks). Promote to a discrete backlog task when an AI Council debate sets its scope.

## Why this is only a stub now (2026-05-29)

v4.3 stable-readiness requires the v4 process to land without further iteration. The agent framework is a separate, larger architectural decision (Council scope). Documenting it as a stub:

- Anchors operator's signal so it isn't lost between sessions
- Provides a single home for the design constraints captured to date
- Does not commit v4.3 to implementing the framework
- Surfaces the gap honestly: enforcement layer is half-built (audit.py checks #7/#8/#9), agent framework is not yet started

The convergence test for v4.3 is bundle-quality (fresh-eyes review). The convergence test for the agent framework is a separate, future effort.
