# Changelog review — 2026-07-07

**Tools + ranges reviewed:**
- **claude-code:** 2.1.201 → **2.1.202** (one CHANGELOG header; installed 2.1.202). Source: raw `anthropics/claude-code/main/CHANGELOG.md`.
- **codex:** last-reviewed **0.142.5** (2026-07-06). Newest STABLE is still 0.142.5; everything newer is `0.143.0-alpha.*` (pre-releases, skipped per rubric). **Nothing new to review** — state unchanged.

**Bucket counts (claude-code 2.1.202, 18 entries):** ADOPT 1 · OBSOLETES-WORKAROUND 0 · STALE-NAMES 0 · VERIFY 1 (resolved) · NOISE 16.

This is the FIRST changelog-review run with the ADR-98 §7 SEED-feed wired (#268). The one ADOPT below is fed to `intake/2026-07-07-changelog-review-seeds.md` (intake-id 5, SEED).

## ADOPT (1)

- **Dynamic-workflow-size `/config` setting** (2.1.202) — a new `/config` control for how large Claude makes dynamic workflows (small / medium / large agent counts; advisory guideline, not an enforced cap). UNDERUSED-NATIVE: we drive multi-agent orchestration through the Workflow tool but set no default size, so fan-out breadth is per-invocation ad hoc. **Value:** a fleet-default lever on workflow agent-count — directly relevant to token discipline and the operator-load theme. **Candidate home:** #155 (loops architecture) or a PLAYBOOK workflow-doctrine note; ties to #270 (operator-load gauge). Decision is the architect's — flagged, not queued.

## OBSOLETES-WORKAROUND (0)

None — no 2.1.202 native feature retires one of our scripts/hooks/shims/conventions.

## STALE-NAMES (0)

None. The `/review` reversion (below) was the only naming risk; checked and clean.

## VERIFY (1 — resolved this run)

- **`/review <pr>` reverted to a fast single-pass review; the multi-agent review is now `/code-review <level> <pr#>`** (2.1.202). Risk: our docs describing the multi-agent review under the wrong command. **Check run:** grep of `protocols/`, `CLAUDE.md`, `.claude/` for `/review` vs `/code-review`. **Outcome: NO drift** — our live docs already name `/code-review ultra` for the cloud multi-agent review (`ENVIRONMENT.md:21`, `PLAYBOOK.md:3298-3299`); the bare `/review` hits are Codex's reviewer (`PLAYBOOK.md:352`) or drift-class examples (`HANDOFF_PROCESS.md:51`, `.claude/commands/handoff.md:33`), none claiming Claude Code's `/review` is multi-agent. No edit needed.

## NOISE (16 — counted, not itemized)

Interactive/TUI fixes (Ctrl+R history search, `/workflows` list layout), Remote-Control / mobile fixes (×4: unknown-command, uncaptioned media drop, wrong permission mode, `/rename` revert), enterprise/transport (mTLS cert-rotation handshake, proxy/installer retry, SSH sign-in URL wrap), voice dictation retry loop, MCP config error-message clarity, and bugfixes to surfaces we DO use — auto-applied on 2.1.202, no action: re-invoking a loaded skill no longer duplicates its instructions in context (token win for our skill-heavy sessions), workflow scripts with unicode-quote escapes no longer corrupt before parsing (+ parse errors now show the offending line), `claude agents` chat-open crash/respawn loop fixed (hardens the Arc-5-adopted cockpit), and resume-by-name / resume-picker no longer slow + memory-heavy in repos with many git worktrees (relevant to our worktree-heavy epic-lane workflow).

## Operator routing

One item wants an architect decision: **the dynamic-workflow-size `/config` setting (ADOPT)** — seeded to `intake/2026-07-07-changelog-review-seeds.md` (id 5). Everything else is NOISE or resolved. Codex quiet.
