# 02 · How we work

Methodology floor for `ai-council`. The authoritative sources are
`.dev-knowledge/protocols/PLAYBOOK.md` and `.dev-knowledge/protocols/ESSENTIALS.md`; this
is a working extract generated from them at handoff time. ai-council-specific enforcement
(hooks, test markers) is layered in below. When in doubt, the live files win.

## Model selection

- **Sonnet (Tier 1)** — "do X the way we always do it": ≤5 files, existing pattern,
  automated checks pass. Mechanical execution.
- **Opus (Tier 2)** — "figure out the right approach": new abstractions, cross-module,
  unfamiliar APIs, security, architecture.
- **xhigh effort** — hardest debugging / architecture / verification; burns more tokens.
- **No AI** — anything <60s by hand.

Think architecturally first (highest scope, then zoom). When asked an item-level question,
first check "is this a symptom of a bigger architectural question?" before answering. Don't
pattern-match to fast plausible answers without self-critique.

## Prompt format

Every formal prompt to Claude Code starts with the model/mode/effort header:

```
| Model | Sonnet / Opus |
| Mode  | auto-accept / plan-then-auto / plan |
| Effort| low / medium / high / xhigh |
```

Then: Title → Read CLAUDE.md + gotchas → Git workflow → UNDERSTAND → Steps with COMMIT
markers → What NOT to do. Name any relevant skill (CC auto-reads
`.claude/skills/<name>/SKILL.md`). After EVERY step in ai-council:
`pytest -x --tb=short && ruff check src/ tests/ && git status`. If you generate 3+ prompts
for one feature, check for overlap before running.

## Hooks & enforcement (ai-council)

**LLMs advise; hooks/tests enforce.** Convention without enforcement drifts. In ai-council,
the enforcement layer is different from `.dev-knowledge`:

- **Pre-commit** (`.pre-commit-config.yaml`): `normalize-headers` only — normalizes
  dated-log headers in `LESSONS.md`/`JOURNAL.md`. There is **no** ruff/mypy/pytest hook.
- **Manual pre-merge gate:** `.\scripts\check.ps1` (pytest + mypy + ruff) — run before
  **every** merge. It is the real quality gate; pre-commit does not substitute for it.
- **Tests:** `pytest tests/ -m "not integration and not envcheck" -v` is the unit suite
  (no API keys); `asyncio_mode = auto` in `pyproject.toml`. Integration tests make live
  paid API calls — do not run in CI.

Executable rules live in `~/.claude/` with `verify:` lines, not in prose. Codex is a
separate code-review CLI (ADR-54, `~/.codex/AGENTS.md`) — a second pair of eyes on 3+ file
or safety-critical changes; threshold 3+ files for a full review.

## AI Council process — when and how

`ai-council` IS the Council tool, but the **process** of convening it is the same floor.
**When to convene** (ALL must hold): architectural impact AND multi-ADR ripple AND reversal
cost > 1 hour. Everything else → single-model + critic loop. Hard cap: **max 2 Council
debates before implementation**. For a *post-hoc record* of an already-validated outcome,
skip Council and write the ADR directly (Path A).

**How to ask (stateless API models):** the brief must be self-contained — Council models
have zero repo context. State the problem in **one sentence**, no candidate answer in the
headline, no asker-leakage, no false dichotomy, no loaded terms. Self-check: *if a fast
unanimous agreement wouldn't surprise you, the question is leading.* Curated transcripts
archive to `.dev-knowledge/docs/decisions/transcripts/`. Full spec:
`.dev-knowledge/protocols/AI_COUNCIL_PROCESS.md`.

## Conventions that bite

- **Conventional Commits** — `type(scope): summary`, imperative, body required for
  non-trivial changes (git history IS the changelog; no CHANGELOG per ADR-49).
- **Branches** — `feat/fix/docs/chore/<topic>` off `main`.
- **Naming** — snake_case Python; kebab-case markdown; `ADR-NN-topic.md` for future ADRs
  (existing ADRs hyphen-named per ADR-34); `YYYY-MM-DD-slug.md` for dated artifacts.
- **Append-only** — LESSONS (never edit); JOURNAL (newest-first prepend).
  **Immutable** — ADRs, transcripts, handoffs, audits (supersede with a new file).
- **Config strings** (models, prompts, personas, timeouts) live in `config/settings.yaml`
  — never hardcode (CLAUDE §5 critical rule 6).
- Output the operator copies back is flat + code-fenced so the TUI doesn't paint
  box-drawing (~3× the tokens).

## Four-tag discipline canonicity

Four-tag discipline (witnessed/recall/inferred/unknown) is canonical per HANDOFF_PROCESS
v4.3 Amendment A; the §3.1 three-tag spec body is **superseded**. Definitions appear inline
in `04_RECENT.md` (so you apply them without reading the spec). Enforced **syntactically**
by `.dev-knowledge/scripts/audit.py` check #9 — it verifies enumeration, NOT tag accuracy
(a mis-labeled `witnessed` passes the lint). Semantic accuracy needs sage discipline +
Phase-2 cross-check.

## Bundle maintenance during session

If you discover drift between this bundle and ai-council repo state during your work — flag
to Rob, JOURNAL the discovery, and amend `04_RECENT.md`'s Load-bearing facts table via
append (don't rewrite). The bundle is living until the next handoff.

## Session lifecycle

Start: `/boot` (rules + memory + trends) → `git status` clean → read recent handoff + last
JOURNAL entries → pick **max 2 objectives**. Parallel same-repo sessions need
`git worktree add` (ADR-61). End: clean working tree, JOURNAL prepend, commit. Run
`.\scripts\check.ps1` before merging. "Claude.ai challenges, Claude Code executes."
