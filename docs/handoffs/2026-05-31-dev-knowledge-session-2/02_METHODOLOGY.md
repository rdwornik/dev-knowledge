# 02 · How we work

Methodology floor for `.dev-knowledge`. The authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Sonnet (Tier 1)** — "do X the way we always do it": ≤5 files, existing pattern,
  automated checks pass. Mechanical execution.
- **Opus (Tier 2)** — "figure out the right approach": new abstractions, cross-module,
  unfamiliar APIs, security, architecture.
- **xhigh effort** — hardest debugging / architecture / magistrala-level verification;
  burns more tokens than high.
- **No AI** — anything <60s by hand.

Think architecturally first (highest scope, then zoom). When asked an item-level
question, first check "is this a symptom of a bigger architectural question?" before
answering. Don't pattern-match to fast plausible answers without self-critique.

## Prompt format

Every formal prompt to Claude Code starts with the model/mode/effort header:

```
| Model | Sonnet / Opus |
| Mode  | auto-accept / plan-then-auto / plan |
| Effort| low / medium / high / xhigh |
```

Then: Title → Read CLAUDE.md + gotchas → Git workflow → UNDERSTAND → Steps with
COMMIT markers → What NOT to do. Name any relevant skill (CC auto-reads
`.claude/skills/<name>/SKILL.md`). After EVERY step: `pytest -x --tb=short &&
ruff check && git status`. If you generate 3+ prompts for one feature, check for
overlap before running.

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** Convention without enforcement drifts. Executable
rules live in `~/.claude/` with `verify:` lines, not in prose. In this repo, pre-commit
runs `ruff check --fix` + `normalize_headers.py` (dated-log header normalization) +
codemap-freshness. `scripts/audit.py health` is the structural gate (9/9 checks,
including #8 handoff-bundle structure and #9 four-tag canonicity).

Codex is a separate code-review CLI (ADR-54, configured globally at
`~/.codex/AGENTS.md`), not Claude Code. A second pair of eyes on 3+ file or
safety-critical changes — distinct system, used in addition to CC's own work.

## AI Council process — when and how (operator-requested operational note)

**When to convene** (ALL must hold): architectural impact (module boundaries, layer
taxonomy, data model) AND multi-ADR ripple (touches 2+ ADRs or creates a new binding
constraint) AND reversal cost > 1 hour. Everything else → single-model + critic loop;
Council overhead (~$0.50, ~5 min, operator attention) is wasted on non-ADR decisions.
Hard cap: **max 2 Council debates before implementation** (more is procrastination).

**vs Path A (direct ADR):** when a decision is a *post-hoc record* of an
empirically-validated outcome (the thing already works), skip Council and write the
ADR directly — Council would be ceremony, not validation. This arc used Path A for
ADR-62/63 deliberately. Reserve Council for *forward-looking* decisions with genuine
optionality.

**How to ask (stateless API models):** the brief must be self-contained — Council
models have zero repo context. State the problem in **one sentence**, no candidate
answer in the headline, no asker-leakage ("I think…", "obviously…"), no false
dichotomy, no loaded terms. Self-check: *if a fast unanimous agreement wouldn't
surprise you, the question is leading.* Flow is 6 stages (frame → brief → route →
debate → review verdict → author ADR → close); transcripts archive to
`docs/decisions/transcripts/`. Full spec: `protocols/AI_COUNCIL_PROCESS.md`.

## Conventions that bite

- **Conventional Commits** — `type(scope): summary`, imperative, <72 chars, body
  required for non-trivial changes (git history IS the changelog; no CHANGELOG since
  2026-05-16). One logical change per commit.
- **Branches** — `feat/fix/docs/chore/<topic>` off `main`.
- **Naming** — UPPERCASE living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for
  dated artifacts. Date everything.
- **Append-only** — LESSONS, TOKEN-LOG (never edit); JOURNAL (newest-first prepend).
  **Immutable** — ADRs, transcripts, handoffs, audits (supersede with a new file).
- **No Unicode box-drawing** in reports — plain markdown tables; box-drawing costs ~3×
  the tokens.

## Four-tag discipline canonicity

Four-tag discipline (witnessed/recall/inferred/unknown) is canonical per
HANDOFF_PROCESS v4.3 Amendment A; the §3.1 three-tag spec body is **superseded**.
Definitions appear inline in `04_RECENT.md` (so you apply them without reading the
spec). Enforced **syntactically** by `audit.py` check #9 — it verifies enumeration,
NOT tag accuracy (a mis-labeled `witnessed` passes the lint). Semantic accuracy needs
sage discipline + Phase-2 cross-check.

## Process versioning + bundle maintenance

A process ships `beta` after design + first impl; promotes to `stable` after one
fresh-eyes review returns **<2 critical findings AND reviewer verdict
PROMOTE/PROMOTE-WITH-CAVEATS** (judgment overrides count; no Council needed).
**The operator runs the fresh-eyes review** in a separate chat — the architect does
NOT spawn its own (echo chamber). If you find bundle/repo drift during work: flag to
Rob, JOURNAL it, and append (don't rewrite) to `04_RECENT`'s Load-bearing facts table.

## Session lifecycle

Start: `/boot` (rules + memory + trends) → `git status` clean → read recent
handoff + last JOURNAL entries → pick **max 2 objectives**. Parallel same-repo
sessions need `git worktree add` (ADR-61). End: clean working tree, JOURNAL prepend,
commit. "Claude.ai challenges, Claude Code executes."
