===== FILE: 02_METHODOLOGY — start =====

# 02 · How we work

Methodology floor for `.dev-knowledge`. The authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Sonnet (Tier 1)** — "do X the way we always do it": ≤5 files, ≤1 layer, an
  existing pattern, automated checks. Mechanical, low-novelty work.
- **Opus (Tier 2)** — "figure out the right approach": new abstractions, cross-module
  changes, unfamiliar APIs, anything security-sensitive or architectural.
- **Effort** `xhigh` for the hardest debugging / architecture / verification — burns
  more tokens than `high`; reserve it.
- **No AI** for trivial work (<60s by hand). Don't reach for a model to rename a var.
- This "model tier" is a distinct axis from the **Tier-1 lifecycle** (ADR-70 closure
  machinery) and the **fleet tiers** (current/partial/cold) in `04`/`05` — same word,
  three meanings.

## Prompt format (browser → Claude Code contract)

Every formal prompt opens with the table — embedded **verbatim**, never paraphrased:

```
| Model | Sonnet / Opus | / | Mode | auto-accept / plan-then-auto / plan | / | Effort | low / medium / high / xhigh |
```

Then the **8-section structure** (PLAYBOOK §"Writing prompts for Claude Code"):
1. Model/Mode/Effort table  2. Title (imperative)  3. Repo + Purpose (absolute path +
one-sentence outcome)  4. Read first (CLAUDE.md, gotchas, relevant docs)  5. Git
workflow (branch + commit cadence + merge)  6. UNDERSTAND (problem / what could break /
likely failure mode)  7. Steps with COMMIT markers  8. Final + What NOT to do (≥3
anti-patterns). Scale L (3+ files / architectural) → prefer `plan-then-auto` for a
review checkpoint after Step 1.

- **Delivery:** downloadable `.md` artifact, not an inline block.
- **Absolute paths**, **English only**, **explicit out-of-scope** ("Do NOT touch X").
- **Pre-flight the hooks/commands in play** — which auto-fire vs which to invoke
  (PLAYBOOK §"Usage protocol: which command / hook, when").
- **Checkable > aspirational:** phrase each rule so compliance is a yes/no check
  against a number, an enumerable set, or a named artifact — not a feeling.

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** Don't put a rule in prose that isn't backed by
enforcement somewhere — it drifts. Precedence **source → gate → agent**: prefer making
a fact self-documenting (derived from code/auto-generated); add a gate (pre-commit
hook / test / `verify:` line) only when it can't be self-documented; an agentic review
only when it can't be gated.

pre-commit auto-fires (this repo): `normalize-dated-headers`, `codemap-freshness`,
`toc-freshness`, `toc-freshness-playbook`, `validate-backlog`, `audit-health`
(`audit.py health` — **FAIL blocks the commit**), `ruff` (lint gate — blocks on
violations), `backlog-id-on-close` (commit-msg). Executable rules live in `~/.claude`
with `verify:` lines, not in repo prose.

Codex is a separate code-review CLI (ADR-54, configured at `~/.codex/AGENTS.md`), used
in addition to CC on 3+ code files or safety-critical changes — **code review only**;
doc-only diffs are skipped cleanly by the path-guard.

## AI Council process

Architecture / ADR-level decisions are **not** made unilaterally. For technical
questions the architect can't resolve alone: research mode, or convene **AI Council**
(`ai-council` CLI). The operator is asked for constraints/priorities/scope — not
"is my technical choice right?". The canonical transcript stays in `ai-council/output/`
and **auto-routes** a copy to a target's `docs/decisions/transcripts/` when the debate
names a `target-project` (ADR-43). The v5 redesign (`05_NOW`) is a Council debate.

## Conventions that bite

- **Conventional Commits** — `type(scope): summary` (`feat/fix/docs/refactor/test/chore`),
  imperative, specific, body for any non-trivial change (git log IS the changelog — no
  CHANGELOG since 2026-05-16).
- **Branches** off `main`: `feat/ fix/ docs/ chore/`. Every change — even a one-line
  doc edit — goes branch → merge `--no-ff` (never direct-to-main).
- **File naming:** UPPERCASE living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug` for
  dated artifacts; `council-out-YYYYMMDD-HHMMSS-topic.md`; kebab-case otherwise.
- **Append-only:** `LESSONS.md`, `logs/TOKEN-LOG.md`; `JOURNAL.md` newest-first prepend.
  **Immutable:** ADRs, transcripts, handoffs, audits — supersede, never edit in place.
- **Output the operator copies into browser chat** must be **flat** (plain markdown /
  `key: value` / bullets, no column-padded tables) **and wrapped in a triple-backtick
  fence** — else the TUI paints box-drawing glyphs that cost ~3× the tokens on copy
  (CLAUDE §4 render-layer).

## Four-tag discipline canonicity

Four-tag discipline (witnessed/recall/inferred/unknown) is canonical per HANDOFF_PROCESS
v4.3 Amendment A; the §3.1 three-tag spec body is **superseded** (amendment precedence).
The definitions appear inline in `04_RECENT.md` of every bundle (so you apply the
discipline from the bundle alone). Enforced **syntactically** by `audit.py` check #9
(verifies the enumeration/pointer exists) — it does **NOT** catch mis-labeled tags;
semantic accuracy needs sage discipline + Phase-2 cross-checking.

## Bundle maintenance during session

If you find drift between this bundle and repo state mid-work — flag to Rob, JOURNAL
the discovery, and **append** to `04_RECENT.md`'s Load-bearing facts table (don't
rewrite). The bundle is living until the next handoff. ("Handoff is back-and-forth,
not a unilateral guess.")

## Session lifecycle

Start: clean `git status`, read the most recent handoff + last JOURNAL entries, pick
**max 2 objectives**, never improvise. End: full test pass, clean tree, prepend a
JOURNAL entry (`Did / Result / Changes / Next`), extract lessons to `LESSONS.md`.
Browser-chat checkpoint at ~2h (before the decision-fatigue threshold) → handoff.

===== FILE: 02_METHODOLOGY — end =====
