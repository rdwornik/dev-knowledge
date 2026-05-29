# 02 · How we work

Methodology floor for `.dev-knowledge`. Authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Sonnet (Tier 1)** — ≤5 files, one layer, existing pattern, automated checks.
  "Do X the way we always do it."
- **Opus (Tier 2)** — new abstractions, cross-module, unfamiliar APIs, security,
  architecture. "Figure out the right approach." `xhigh` effort for the hardest
  debugging / architecture / verification.
- **No AI** for anything <60s of manual work.

## Prompt format

Formal prompts open with a `Model / Mode / Effort` table, then:
Title → Read CLAUDE.md + gotchas → Git workflow → UNDERSTAND → Steps with COMMIT
markers → What NOT to do. Name any relevant skill (e.g. `gotchas`). After EVERY
step: `pytest -x --tb=short && ruff check && git status`.

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** Pre-commit runs `ruff check --fix` +
dated-header normalization + codemap-freshness. Executable rules live in
`~/.claude/` with `verify:` lines, not in repo prose. A convention without a gate
drifts — this is the repo's structural lesson (ML-2, see `04`).

Codex is a separate code-review CLI (per ADR-54, configured globally at
`~/.codex/AGENTS.md`), not Claude Code. Use it as a second pair of eyes on 3+ file
or safety-critical changes — distinct system, used in addition to your own work.
Doc-only / markdown diffs are skipped cleanly by its path-guard.

## AI Council process

Convene **AI Council** for architecture/ADR-level decisions — they are **not** made
unilaterally. Council debates run via the `ai-council` CLI; transcripts return to
`docs/decisions/transcripts/` (currently by manual archival; auto-routing pending).
Standing rule: when you find yourself about to make a structural call, ask whether
it belongs in Council first.

## Conventions that bite

- **Conventional Commits** — `feat/fix/docs/chore/refactor(scope): summary`
  (imperative, specific; body for any non-trivial change — git log IS the changelog,
  no CHANGELOG since 2026-05-16). One logical change per commit.
- **Branches** off `main`: `feat/<topic>`, `fix/<issue>`, `docs/<scope>`,
  `chore/<scope>`.
- **Naming:** UPPERCASE for top-level living docs; `ADR-NN-topic.md`;
  `YYYY-MM-DD-slug.md` for dated artifacts; kebab-case otherwise. Date everything.
- **Append-only:** `LESSONS.md`, `TOKEN-LOG.md` (never edit old entries);
  `JOURNAL.md` (newest-first prepend). **Immutable:** ADRs, transcripts, handoffs,
  audits — supersede with a new file/amendment, never edit in place (ADR-39).
- **Visual pattern (ADR-59):** dot-prefix configs where supported; ALL-CAPS
  canonical `.md` at root. **docs/ taxonomy (ADR-60):** one semantic role per
  subfolder; `.dev-knowledge` carries `decisions/audits/handoffs/archive/`.
- **No Unicode box-drawing** in reports/summaries — plain markdown tables or bullets
  (box-drawing costs ~3× the tokens).
- **Validators need args** — `audit.py` with `--all` or a specific path; no-arg runs
  pass vacuously.

## Bundle maintenance during session

If you discover drift between this bundle and repo state during your work — flag to
Rob, JOURNAL the discovery, and amend this bundle's `04_RECENT.md` Load-bearing
facts table via append (don't rewrite). The bundle is living until the next handoff.
This implements the "handoff is back-and-forth, not unilateral guess" rule below.

## LLM-LLM transfer is back-and-forth

When transferring context across LLM boundaries (handoff, chat-to-chat,
browser-to-CC, CC-to-Codex), the sender verifies load-bearing claims inline rather
than carrying forward "unknown" or "I think this was true earlier"; the receiver
asks back before unilateral interpretation. **Verify inline, ask back; don't carry
forward unknown.** (Now a PLAYBOOK methodology rule, codified this session.)

## Session lifecycle

`/boot` (loads skills, memory, recent commits) → `git status` clean → read recent
handoff + last JOURNAL entries → pick **max 2 objectives** → work with per-step
tests → at end: full suite green, clean tree, prepend JOURNAL entry
(`Did/Result/Changes/Abandoned/Next`), extract LESSONS. Stop-signs: decision fatigue
(~3h), recursive planning, scope creep — recognize and act.
