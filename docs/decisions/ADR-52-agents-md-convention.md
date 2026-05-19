# ADR-52: AGENTS.md Convention — Cross-Tool Agent-Instruction Contract

- **Status:** ~~Accepted~~ Superseded by ADR-53 (2026-05-19)
- **Date:** 2026-05-19
- **Amends:** —
- **Related:** ADR-28 (three-layer architecture), ADR-31 (authority model), ADR-38 (universal repo architecture baseline)
- **Decommission:** none
- **Source:** Rob's decision, 2026-05-19. Ratifies the extant convention in PLAYBOOK §"AGENTS.md — canonical per-repo governance contract"; surfaced via handoff-process conflation correction.

## Context

The AGENTS.md convention has been described in PLAYBOOK for some time, but no numbered ADR formally records it, making it non-citable. The gap surfaced when Claude-oriented browser-chat handoffs conflated AGENTS.md with repo-descriptive documents — treating it as an artifact the handoff narrates, summarizes, or manages.

The `agents.md` cross-tool standard (community, September 2025) provides an external baseline: a single canonical file read by all LLM-based agents rather than tool-specific configuration files.

## Decision

1. **AGENTS.md is the canonical per-repo cross-tool agent-instruction contract.** It is read by Claude Code, Codex, Cursor, Aider, and other LLM-based agents per the `agents.md` community standard. Claude Code auto-reads it at session start.

2. **Canonical structure:** The 10-section structure in `templates/AGENTS-md-template.md` is the conformant implementation: (1) Read first, (2) Repo identity, (3) Architecture, (4) Conventions, (5) Tools active, (6) Gotchas, (7) Binding ADRs, (8) Out of scope, (9) Session start checklist, (10) Do NOT.

3. **Authority hierarchy (unchanged):**
   - `.dev-knowledge/protocols/ESSENTIALS.md` + `PLAYBOOK.md` — universal rules
   - `{repo}/AGENTS.md` — per-repo specifics (agent-instruction contract)
   - `{repo}/CLAUDE.md` — thin pointer (≤200 lines) referencing both
   - `{repo}/.claude/` — runtime config

4. **AGENTS.md is an agent-instruction contract, not a repo-descriptive document.** It is outside the scope of what the Claude-oriented handoff process narrates or manages. The Claude-oriented handoff process must not narrate, summarize, or manage AGENTS.md as Claude-side repo-descriptive handoff content.

5. **Out of scope / not decided:** A convention where AGENTS.md becomes Codex-only and Claude Code stops reading it is explicitly **not** adopted. Such a change requires its own ADR. ADR-52 makes no authority-model change.

## Consequences

- The AGENTS.md convention gains a citable decision number.
- Handoffs are clarified: AGENTS.md is not narrated, summarized, or managed by the handoff workflow as Claude-side handoff content.
- No change to what AGENTS.md is, who reads it, or its authority position.

## Alternatives considered

- **Codex-only AGENTS.md** — Claude Code stops auto-reading it. Explicitly rejected; not decided here. Would require its own ADR.
- **No ADR — leave as PLAYBOOK section only** — Rejected because the lack of a citable decision record causes persistent conflation in prompts and handoffs.
