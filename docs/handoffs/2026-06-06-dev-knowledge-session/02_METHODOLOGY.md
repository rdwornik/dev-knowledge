===== FILE: 02_METHODOLOGY — start =====

# 02 · How we work

Methodology floor for `.dev-knowledge`. The authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md` in `.dev-knowledge`; this is a
working extract generated from them at handoff time. When in doubt, the live files
win.

## Model selection

- **Tier 1 (Sonnet)** — ≤5 files, ≤1 layer, an existing pattern, automated checks
  cover it. "Do X the way we always do it."
- **Tier 2 (Opus)** — new abstractions, cross-module, unfamiliar APIs, security,
  judgment-heavy. "Figure out the right approach."
- **No AI** — trivial tasks (<60s manual). Don't burn a model on them.
- **xhigh effort** — hardest debugging / architecture / verification only; burns more
  tokens than high. Unpinned subagents inherit the main session model — pin them.

## Prompt format

Every formal Claude Code prompt opens with a `Model / Mode / Effort` header, then:
Title → "Read CLAUDE.md + gotchas" → Git workflow → **UNDERSTAND** (state the problem,
repos, blast radius) → numbered Steps with explicit COMMIT markers → "What NOT to do".
Name any relevant skill (e.g. `gotchas`) so CC auto-reads it. Run
`pytest -x --tb=short && ruff check && git status` after **every** step, not at the end.
Pre-flight the hooks/commands in play (which auto-fire vs which you invoke — see
PLAYBOOK §"Usage protocol: which command / hook, when"). **Build a STOP-after-UNDERSTAND
valve into every judgment-heavy prompt** — a prompt whose premise might be stale should
verify two named facts and HALT-with-options if either fails (this session, that valve
killed #86.2's dead machinery before it shipped).

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** Executable rules live in `~/.claude` with
`verify:` lines, never as prose hope. This repo's pre-commit auto-fires:
`normalize-dated-headers` · `codemap-freshness` · `ARCHITECTURE/PLAYBOOK TOC-freshness`
· `validate-backlog` (ADR-66) · `audit-health` (`audit.py health` — FAIL blocks the
commit) · `ruff` (lint gate — blocks on violations) · `backlog-id-on-close` (commit-msg:
require `[#id]` when a commit removes a backlog task). Session hooks:
`SessionStart → fleet_health.py` (Tier-2 daily cross-repo audit). The Tier-1 closure
loop runs via the `tier1-lifecycle` plugin (Stop → propose) + global L0 surfacing.

**Contract guarantees live on the EXECUTING path** (session doctrine, distilled to
LESSONS this session). A validator/marker that runs only on a path production does not
take is decoration. Counts and conformance facts must be computed by code, carried in a
machine-readable marker, and read by a parser that fails **CLOSED**. The nightly
conformance routine (cloud, schedule-triggered) is the methodology's immune system —
verifier fan-out → adversarial skeptic → READ-ONLY proposals → operator ratification.

Codex is a separate code-review CLI (ADR-54, `~/.codex/AGENTS.md`), not Claude Code —
a second pair of eyes on 3+ file or safety-critical **code** changes. It skips
doc-only/markdown diffs cleanly.

## AI Council process

Convene AI Council for **architecture/ADR-level decisions** — anything that changes
scope, conventions, or governance. The architect does NOT seek operator validation on
technical choices the operator can't adjudicate ("is this design better?"); the
operator owns constraints, priorities, scope. The escalation ladder (PLAYBOOK):
conversational → formal CC prompt → **scoped Dynamic Workflow** ("too big for one pass /
needs verification") → **AI Council** (heavy decision). Transcripts route to
`docs/decisions/transcripts/` when a debate names a target-project (ADR-43). ADRs are
distilled and committed by Claude Code — never hand-carried.

## Conventions that bite

- **Conventional Commits** — `type(scope): summary`, imperative, body for non-trivial
  changes (git history IS the changelog — no CHANGELOG.md). One logical change per commit.
- **Branch + merge `--no-ff` is universal** (operator ruling this session) — EVERY
  change, including one-line doc edits, goes branch → merge `--no-ff`; never
  direct-to-main. Branches off `main`: `feat/ fix/ docs/ chore/`.
- **Naming:** UPPERCASE living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` dated
  artifacts; kebab-case otherwise.
- **Append-only:** `LESSONS.md`, `logs/TOKEN-LOG.md`; `JOURNAL.md` newest-first prepend.
  **Immutable:** ADRs/transcripts/handoffs/audits — supersede, never edit in place.
  **JOURNAL corrections are NEW prepended entries**, never edits.
- **Output the operator copies into browser chat must be flat + code-fenced** — the TUI
  paints markdown pipe-tables as box-drawing glyphs at render time (~3× tokens when
  copied out). Flat `key: value`/bullets inside a triple-backtick fence renders raw
  (CLAUDE §4 render-layer fix).

## Four-tag discipline canonicity

Four-tag discipline (witnessed/recall/inferred/unknown) is canonical per
HANDOFF_PROCESS v4.3 Amendment A. The §3.1 three-tag text in the spec body is
**superseded** — amendment-precedence applies. The definitions appear in `04_RECENT.md`
of every generated bundle (so you don't need to read the spec to apply the discipline).
Enforced **syntactically** by `audit.py` check #9 — it verifies §3.1 enumerates the four
tags OR points to Amendment A. **Check #9 does NOT catch mis-labeled tags** (a
`witnessed` claim that should have been `recall` passes the lint). Semantic accuracy
requires sage discipline + Phase-2 verification cross-checking.

## Bundle maintenance during session

If you discover drift between this bundle and repo state during your work — flag
to Rob, JOURNAL the discovery, and amend the bundle's `04_RECENT.md` Load-bearing
facts table via append (don't rewrite). The bundle is living until the next
handoff. This implements the "handoff is back-and-forth, not unilateral guess" rule.

## Session lifecycle

Session start (load context: skills, memory, recent commits — the old `/boot`, archived
2026-06-05) → `git status` clean → read recent handoff/JOURNAL → pick **max 2
objectives** → work (test after each change) → end with full suite + clean tree +
JOURNAL prepend (`Did / Result / Changes / Abandoned / Next`) + lessons extract. Scope
is sacred; "improvise" is forbidden for CC.

===== FILE: 02_METHODOLOGY — end =====
