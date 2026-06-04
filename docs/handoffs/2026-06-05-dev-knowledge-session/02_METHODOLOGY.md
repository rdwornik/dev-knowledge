# 02 · How we work

Methodology floor for `.dev-knowledge`. The authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Tier 1 (Sonnet)** — "do X the way we always do it": ≤5 files, ≤1 layer, an
  existing pattern, automated checks cover it.
- **Tier 2 (Opus)** — "figure out the right approach": new abstractions, cross-module
  work, unfamiliar APIs, security, judgment-heavy decisions.
- **Trivial (<60s manual)** → no AI at all.
- **Subagent/fan-out routing (t-shirt doctrine, new this arc):** S=Haiku, M=Sonnet,
  L/judgment=Opus. **Pin every agent explicitly.** An *unpinned* subagent inherits the
  **main session model** (currently Opus 4.8) on both the Agent-tool and
  workflow-engine paths — so an unpinned fan-out is a cost bug, not a default.

## Prompt format (browser → CC contract)

Every formal prompt is a **downloadable `.md` artifact** (not an inline block), opening
with a `| Model | Mode | Effort |` table, then the **8 sections**: (1) Model/Mode/Effort
table, (2) Title (imperative), (3) Repo + Purpose (absolute path + one-sentence
outcome), (4) Read first (CLAUDE.md + gotchas + task docs), (5) Git workflow (branch +
commit cadence + merge), (6) UNDERSTAND (problem / what could break / likely failure
mode), (7) Steps with COMMIT markers, (8) Final + What NOT to do (≥3 anti-patterns).
Scale S may use the minimal version; Scale L requires the full template + `plan-then-auto`.

Pre-send essentials: English only · absolute paths · "Read first" always names CLAUDE.md
+ gotchas · COMMIT marker per step · explicit out-of-scope ("Do NOT touch X") · name any
relevant skill so CC auto-loads it · state which **hooks auto-fire vs which commands you
invoke** (PLAYBOOK "Usage protocol: which command / hook, when").

## Hooks & enforcement

**LLMs advise; hooks/tests enforce.** Don't put a rule in prose that isn't backed by
enforcement somewhere — it drifts. The **precedence** for where a rule should live
(prefer the earliest tier):

1. **Source** — make the fact self-documenting so it has nothing to drift from
   (derive from code, e.g. `audit.py checks` reads `ALL_CHECKS`; auto-generate codemap/TOC).
2. **Gate** — if it can't be self-documenting, add an active gate (pre-commit hook,
   test, `verify:` line) — a gate fires every commit; an advisory lesson may not load.
3. **Agent** — for semantic/judgment/prose drift neither covers, an agentic review is
   the safety net (ADR-70 Tier-3 / BACKLOG #81 conformance workflow).

Pre-commit auto-fires (this repo): `normalize-dated-headers`, `codemap-freshness`,
`validate-backlog`, `audit-health` (`audit.py health` — FAIL blocks the commit),
`ruff check` (now a **gate**, not manual — corrected this arc), `backlog-id-on-close`,
plus the two `toc-freshness` hooks. Executable rules live in `~/.claude/` with
`verify:` lines, not in this repo's prose.

Codex is a separate code-review CLI (ADR-54, `~/.codex/AGENTS.md`) — a second pair of
eyes on 3+ file or safety-critical **code** changes. Doc-only diffs are skipped cleanly.

## AI Council process

The architect does **not** seek operator validation on technical proposals the operator
lacks expertise to adjudicate ("is this design better?"). For technical questions you
can't resolve alone: research mode (web/docs/memory), **AI Council** (research or pick
debate via the `ai-council` CLI), or build an explicit trade-off comparison Rob chooses
from. Architecture/ADR-level decisions are convened, not decided unilaterally;
transcripts route back to `docs/decisions/transcripts/`. Ask Rob about constraints,
priorities, and scope — not "is my technical choice right?".

## Conventions that bite

- **Conventional Commits** (`feat/fix/docs/chore/refactor(scope): summary`), imperative,
  body required for non-trivial changes — git history IS the changelog (no CHANGELOG.md).
- **Branches** off `main`: `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>`.
  Merge `--no-ff`.
- **File naming:** UPPERCASE living docs (`VISION.md`, `CLAUDE.md`…); `ADR-NN-topic.md`;
  `YYYY-MM-DD-slug.md` for dated artifacts; kebab-case otherwise.
- **Append-only:** `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit); `JOURNAL.md`
  (newest-first prepend). **Immutable:** ADRs, transcripts, handoffs, audits (supersede
  with a new file, never edit in place).
- **Output the operator copies back to browser chat must be flat + code-fenced.** The CC
  TUI paints plain markdown pipe-tables into Unicode box-drawing at render time; a fenced
  block renders raw so the copied text carries no costly border glyphs (CLAUDE §4).

## Four-tag discipline canonicity

Four-tag discipline (witnessed / recall / inferred / unknown) is canonical per
HANDOFF_PROCESS v4.3 Amendment A; the §3.1 three-tag body text is **superseded**. Phase 2
enforces four tags; the definitions appear in `04_RECENT.md` of every bundle (so you
apply the discipline without reading the spec). `audit.py` check #9 enforces this
**syntactically** at lint time — it verifies §3.1 enumerates all four tags or points to
Amendment A. **It does NOT catch mis-labeled tags** (a `witnessed` claim that should be
`recall` passes); semantic accuracy needs sage discipline + Phase-2 cross-checking.

## Bundle maintenance during session

If you discover drift between this bundle and repo state during your work — flag to Rob,
JOURNAL the discovery, and **append** to `04_RECENT.md`'s Load-bearing facts table
(don't rewrite). The bundle is living until the next handoff ("handoff is back-and-forth,
not unilateral guess").

## Session lifecycle

CC session: `/boot` (loads rules/memory/commits) → `git status` clean → read recent
handoff + JOURNAL → pick **max 2 objectives** → work. End: full test suite → clean tree
→ JOURNAL prepend (`Did/Result/Changes/Abandoned/Next`) → extract LESSONS. New browser
chat: upload `ESSENTIALS.md` + the most recent handoff bundle, follow its README paste
sequence.
