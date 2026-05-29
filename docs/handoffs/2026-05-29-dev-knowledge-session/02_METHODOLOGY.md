# 02 · How we work

Methodology floor for `.dev-knowledge`. Authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Tier 1 (Sonnet)** — "do X the way we always do it": ≤5 files, one layer, an
  existing pattern, automated checks cover it.
- **Tier 2 (Opus)** — "figure out the right approach": new abstractions,
  cross-module work, unfamiliar APIs, security, architecture, judgment-heavy.
- **No AI** — trivial tasks (<60s of manual work).
- Standing operator rule: **never default to Sonnet for judgment-heavy work** —
  actively choose per task. `xhigh` effort is for hardest debugging / architecture
  / verification (burns more tokens than `high`).

## Prompt format (browser → Claude Code)

Every formal prompt opens with a `| Model | Mode | Effort |` table, then the
**8-section structure**: (1) Model/Mode/Effort table, (2) Title (imperative),
(3) Repo + Purpose (absolute path + one-sentence outcome), (4) Read first
(CLAUDE.md + gotchas always), (5) Git workflow (branch + commit cadence + merge),
(6) UNDERSTAND (problem / what could break / likely failure mode), (7) Steps with
COMMIT markers, (8) Final + What NOT to do (≥3 anti-patterns). Prompts are
**downloadable `.md` artifacts**, English-only, absolute paths. (This subsumes the
old v3.4 "Prompt Generation Card".)

**Meta-warning the sender flagged loudly:** the "generate a comprehensive prompt"
default is sometimes a way of outsourcing judgment to Claude Code. When Rob asks
for analysis grounded in audits, often the correct move is to **engage in chat
with file:line evidence**, not to emit a process-running prompt.

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** CLAUDE.md tells the LLM what to do; pre-commit
hooks, pytest, and Codex `/review` enforce mechanically. Don't put a rule in
CLAUDE.md that isn't backed by enforcement somewhere — it drifts. Executable rules
live in `~/.claude/` with `verify:` lines, not in this repo's prose.

Current `.dev-knowledge` pre-commit hooks: `normalize-dated-headers` +
`codemap-freshness`. **Note:** ruff is *documented* as a pre-commit hook but is
**not actually wired** here (open ecosystem-audit finding HK-1) — run `ruff check`
manually. `audit.py` health must stay **7/7** after every commit on every branch.

## AI Council process

Convene **AI Council** for architecture / ADR-level decisions — anything where the
choice itself is a recorded decision. The architect does not seek operator
validation on *technical* questions the operator can't adjudicate; the operator
owns constraints, priorities, scope. Council transcripts route back to
`docs/decisions/transcripts/`. Post-debate, the ADR is distilled and committed by
Claude Code. Full runbook: `protocols/AI_COUNCIL_PROCESS.md`.

## Conventions that bite

- **Commits:** Conventional Commits (`feat/fix/docs/chore/refactor`); imperative
  summary <72 chars; body required for non-trivial changes (git history *is* the
  changelog — there is no CHANGELOG.md).
- **Branches:** `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>`
  off `main`.
- **File naming:** UPPERCASE living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md`
  for dated artifacts; hyphen separator universal.
- **Append-only:** `LESSONS.md`, `TOKEN-LOG.md` (never edit), `JOURNAL.md`
  (newest-first prepend).
- **Immutable:** ADRs, transcripts, handoffs, audits — supersede with a new file
  or an append-only marker, **never edit in place** (ADR-39).
- **Layer-2 invariant:** `scripts/` holds read-only validators only — no
  orchestration. Mega-sessions run from Claude Code orchestrating per-repo, not
  from a `.dev-knowledge` script.
- **Output formatting:** plain markdown tables / bullets; **no Unicode
  box-drawing** (terminal-only, ~3× the tokens).
- **Parallel sessions (ADR-61):** different repos = safe; **same repo = requires
  `git worktree add`** (3+ races cost 1–2h cleanup each).

## Session lifecycle

Start: `/boot` → `git status` clean → read recent handoff + JOURNAL → pick **max 2
objectives** → never improvise. End: full test suite → clean tree → `/codex-review`
if 3+ files or 2+ packages touched (skipped cleanly for doc-only diffs) → prepend
JOURNAL entry (`Did/Result/Changes/Abandoned/Next`) → extract LESSONS.
