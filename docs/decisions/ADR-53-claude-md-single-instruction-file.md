# ADR-53: CLAUDE.md as Single Canonical Agent-Instruction File

- **Status:** Accepted
- **Date:** 2026-05-19
- **Amends:** —
- **Related:** ADR-52 (superseded), ADR-51 (unaffected), ADR-38 (universal repo architecture baseline)
- **Decommission:** none
- **Source:** Rob's decision, 2026-05-19. Based on empirical verification (codex-cli 0.131.0, sentinel test PASS). Evidence: `docs/audits/2026-05-19-cohort1-verification.md`.

## Context

ADR-52 established `AGENTS.md` as the canonical per-repo cross-tool agent-instruction contract, asserting it is read by Claude Code, Codex, Cursor, Aider, and other LLM-based agents. Subsequent empirical verification (2026-05-19) falsified the core premise:

- **Claude Code** reads `CLAUDE.md` natively at session start. It does **not** auto-read `AGENTS.md`.
- **Codex** reads `CLAUDE.md` when `project_doc_fallback_filenames = ["CLAUDE.md"]` is set in `~/.codex/config.toml` — confirmed PASS with codex-cli 0.131.0 (sentinel test, 2026-05-19).

The active toolset is Claude Code + Codex only. No third tool (Cursor, Aider) is currently active in this ecosystem. ADR-52 Decision 5 explicitly reserved a Codex-only AGENTS.md model for a future ADR; that reservation is now moot.

The false premise has already produced observable drift: ADR-52 Decision 1 asserts Claude Code auto-reads `AGENTS.md` (false); `ai-council/AGENTS.md` §2 contained a Purpose overclaim that was corrected separately (2026-05-19 cohort-1 conformance session). Two instruction files create ongoing divergence with no compensating benefit.

## Decision

1. **`CLAUDE.md` is the single canonical per-repo agent-instruction file.** ADR-52 is superseded.

2. **`AGENTS.md` as a separate per-repo file is retired.** Existing `AGENTS.md` files in `.dev-knowledge` and `ai-council` are to be removed and their content merged into each repo's `CLAUDE.md` (subsequent implementation chunk).

3. **The `AGENTS-md-template.md` template is to be retired.** `PLAYBOOK.md` and `ESSENTIALS.md` references to the AGENTS.md convention are to be updated to reflect CLAUDE.md as the single instruction file (subsequent implementation chunk).

4. **The per-repo agent-instruction file in the authority chain (ESSENTIALS+PLAYBOOK → per-repo file → `.claude/`) is `CLAUDE.md`, replacing `AGENTS.md`.** The hierarchy levels themselves are unchanged.

## Rationale

- `CLAUDE.md` covers both active tools — Claude Code natively, Codex via `project_doc_fallback_filenames` — making AGENTS.md redundant for the actual toolset.
- The two-file model already produced drift within days of ADR-52 ratification, evidenced by the false claim in ADR-52 Decision 1 and the ARCHITECTURE.md Purpose overclaim in `ai-council/AGENTS.md` §2.
- Future third-tool support (e.g., Cursor, Aider) is trivially addable via its own ADR when the need is real; over-engineering the file convention for hypothetical tools is not warranted.
- Superseding an ADR via a correcting ADR is the recognized lifecycle mechanism in this ecosystem (cf. ADR-07 → ADR-43 in `ai-council`).

## Consequences

- **Subsequent chunk:** `AGENTS.md` removed from `.dev-knowledge` and `ai-council`; content merged into each repo's `CLAUDE.md`.
- **Subsequent chunk:** `PLAYBOOK.md` and `ESSENTIALS.md` updated to remove AGENTS.md convention references; `templates/AGENTS-md-template.md` retired.
- **Codex configuration:** `project_doc_fallback_filenames = ["CLAUDE.md"]` is already set in `~/.codex/config.toml` (2026-05-19). No per-repo configuration needed.
- **ADR-51** (ARCHITECTURE.md convention) is unaffected.

## Alternatives considered

- **Keep AGENTS.md alongside CLAUDE.md, with CLAUDE.md as a thin pointer** — rejected: perpetuates the two-file drift problem without benefit; both tools read CLAUDE.md directly, making any pointer model unnecessary overhead.
- **Leave ADR-52 ratified, accept the false premise** — rejected: ADR-52 Decision 1's false claim that Claude Code auto-reads AGENTS.md will continue to misdirect future decisions and prompts; a correction ADR is the proper mechanism.
- **No ADR — leave as a conversational correction** — rejected: the false claim is in a ratified ADR (non-citable status); only a superseding ADR restores the decision record to accuracy.
