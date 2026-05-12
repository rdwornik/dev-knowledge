---
audit: hooks-discovery-resolution
date: 2026-05-12
scope: ecosystem
status: complete
related: 2026-05-12-hooks-discovery
---

# Hooks Discovery — Resolution

<!-- scope: meta -->

## Reference

Resolves the `/review` name conflict identified in `docs/audits/2026-05-12-hooks-discovery.md` (user-defined `~/.claude/commands/review.md` Codex wrapper collides with built-in Claude Code `/review` skill, "Review a pull request").

## Resolution

User-defined `~/.claude/commands/review.md` renamed to `codex-review.md`. New slash command form: `/codex-review`. Aligns with wrapper script name `codex-review` in `~/.claude/bin/` and with PLAYBOOK § 15 shell-command form.

## Shadowing behavior observed (pre-rename)

<!-- scope: meta -->

Both `/review` registrations (user-defined Codex wrapper + built-in PR review skill) were separately visible in the Claude Code system-reminder skills list simultaneously — `review: /review — Invoke Codex review` and `review: Review a pull request` appeared as distinct entries. This indicates **disambiguation / both registered** rather than one silently winning. Empirical interactive test (typing `/review` at prompt) not performed — inference from system-reminder observation. Marker: Architect inference (Witnessed from context).

## References updated

<!-- scope: meta -->

- `~/.claude/commands/review.md` → `~/.claude/commands/codex-review.md` (Witnessed — in-place Rename-Item; `~/.claude/` not git-tracked)
- `~/.claude/commands/codex-review.md` heading — `# /review` → `# /codex-review` (Witnessed)
- `protocols/ESSENTIALS.md:189` — `slash: /review` → `slash: /codex-review` (Witnessed)
- `protocols/PLAYBOOK.md:940` — `/review — invoke Codex review` → `/codex-review — invoke Codex review` (Witnessed)
- `protocols/PLAYBOOK.md:2071` — `slash command: /review` → `slash command: /codex-review` (Witnessed)

## References intentionally NOT updated

<!-- scope: meta -->

The following references to `/review` are frozen historical records or refer to the built-in PR-review sense — left unchanged per audit:

- `CHANGELOG.md` — append-only historical log; historical Codex `/review` mentions accurate at their recorded date
- `JOURNAL.md` — append-only; journal entry 2026-05-12 accurately records pre-rename state
- `LESSONS.md` — append-only; never editable
- `docs/audits/2026-05-12-hooks-discovery.md` — immutable point-in-time audit; records pre-rename state
- `docs/audits/2026-04-25-claude-code-features-inventory.md` — frozen audit; `/review` references accurate at audit date
- `docs/handoffs/` (all subfolders) — point-in-time snapshots; preserve historical state
- `docs/handoffs/archive/` — legacy frozen records
- `protocols/PLAYBOOK.md:1125` — section history entry for v1.0 accurately records that v1.0 had `/review`
- `~/.claude/cache/changelog.md` — system cache, not operator-managed
- `~/.claude/plugins/` — third-party plugin marketplace files; not operator-controlled

## Verification

<!-- scope: meta -->

Post-rename: system-reminder confirms `/codex-review` invokes Codex wrapper (description updated to `# /codex-review — Invoke Codex review`). Built-in `/review` skill ("Review a pull request") remains registered separately. Name collision eliminated.

Scope tag validator: pass (17% hybrid, within ADR-27 ceiling).

## Unknowns

<!-- scope: meta -->

- **`~/.claude/` git tracking:** Not git-tracked — rename performed as in-place `Rename-Item`. No commit history for the file rename itself. Noted as Unknown-by-design.
- **Interactive shadowing behavior:** System-reminder evidence strongly suggests both were registered simultaneously (disambiguation scenario), but this was not confirmed by typing `/review` at an interactive Claude Code prompt. Marker: Architect inference, not empirical test.
- **`~/.claude/plans/proud-prancing-cerf.md`:** Grep surfaced a `/review` hit in this plan file. Not inspected — plans are ephemeral operator working notes, not governance docs. Classified as out-of-scope for this rename; no update performed.

## N=2 codification gate

This resolution is Shape (a) — single-config-dir, N=1 for the scrum-master review propagation pattern remains intact. ADR-44 codification gate untouched.
