# 02 · How we work

Methodology floor for `.dev-knowledge`. The authoritative sources are
`protocols/PLAYBOOK.md` and `protocols/ESSENTIALS.md`; this is a working extract
generated from them at handoff time. When in doubt, the live files win.

## Model selection

- **Sonnet:** ≤5 files, ≤1 layer, existing pattern, automated checks pass.
- **Opus:** new abstractions, cross-module work, unfamiliar APIs, security.
- **No AI:** anything a human would do in <60 seconds — don't spend a model on it.
- Heavy-decision work escalates to **AI Council**; heavy-execution / cross-repo /
  large-repo work escalates to a scoped **Dynamic Workflow** (the execution analog;
  the escalation rule is BACKLOG #74, to be written once #80 lands).

## Prompt format

Prompts to Claude Code follow the standard 8-section structure (objective, context,
files, steps, constraints, verification, output, stop-signs). Delivery: a single
copy-pasteable block. Pre-send checklist essentials:

- **Scope is one or two objectives** — never bundle.
- **Verification step is mandatory** — every step has a check; `pytest -x` + `ruff
  check` + `git status` between numbered steps, not only at the end.
- **Hooks/commands-in-play pre-flight line:** state which hooks will auto-fire on
  commit vs which commands you expect CC to invoke (see PLAYBOOK "Usage protocol:
  which command / hook, when"). This prevents surprise gate failures mid-run.

## Hooks & enforcement

**LLMs advise; hooks and tests enforce.** A rule that lives only in prose is a
suggestion; a rule with a `verify:` line or a pre-commit hook is enforced. Executable
rules live in `~/.claude/` with `verify:` lines, **not** in this repo's prose.

pre-commit auto-fires (FAIL blocks the commit):
`normalize-dated-headers` · `codemap-freshness` · `toc-freshness` (ARCHITECTURE +
PLAYBOOK) · `validate-backlog` · `audit-health` (`audit.py health`) · **`ruff`**
(version-pinned ≥0.15.5, gate mode `ruff check` — wired via BACKLOG #13, closed
2026-06-02) · `backlog-id-on-close` (commit-msg).

Session hooks (`.claude/settings.json`): `SessionStart → fleet_health.py` (Tier-2
daily cross-repo audit digest). The Tier-1 closure loop runs via the enabled
`tier1-lifecycle` **plugin** (`Stop → propose_closures.py`) plus the global
`~/.claude` `SessionStart → surface-closures.ps1` (L0 surfacing).

Codex is a separate code-review CLI (ADR-54, configured at `~/.codex/AGENTS.md`),
**not** Claude Code. A second pair of eyes on 3+ file or safety-critical changes —
distinct system, used in addition to CC's own work.

## AI Council process

Convene **AI Council** for architecture/ADR-level decisions — never decide them
unilaterally. The gated loop (ADR-67) is Frame → Generate → Gate → Run → Verdict →
Return; `/council-question` triggers it; transcripts archive to
`docs/decisions/transcripts/`. Council debates originate in the `ai-council` repo.
Operationalizing this loop end-to-end is BACKLOG #70 (now actionable).

## Conventions that bite

- **Commits:** Conventional Commits (`feat/fix/docs/chore/refactor`). When a commit
  finishes a backlog task, end the subject with `closes [#id]` — the finishing commit
  closes it (the `advances` vs `closes` distinction is load-bearing for the closure
  loop).
- **Branches:** `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>` off `main`.
- **Naming:** UPPERCASE living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for dated
  artifacts; kebab-case otherwise.
- **Append-only:** `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit); `JOURNAL.md`
  (newest-first prepend). **Immutable:** ADRs, transcripts, handoffs, audits —
  supersede with a new file, never edit in place.
- **Layer 2 never executes** — `scripts/` holds read-only validators only; no
  orchestration that drives state in child repos.
- **Output the operator copies back** must be **flat** (plain markdown / `key: value`
  / bullets, no column-padded tables) **and wrapped in a triple-backtick code fence**,
  so the TUI renders it raw and the copied text carries no box-drawing glyphs
  (CLAUDE §4 render-layer fix). The TUI *paints* borders client-side; banning Claude
  from writing them is a no-op.

## Four-tag discipline canonicity

Four-tag discipline (witnessed/recall/inferred/unknown) is canonical per
HANDOFF_PROCESS v4.3 Amendment A. The §3.1 three-tag text in the spec body is
**superseded** — amendment-precedence applies. Bundle generation (Phase 2) enforces
four tags; the definitions appear in `04_RECENT.md` of every bundle (so you don't
need the spec to apply the discipline). Enforced **syntactically** by `audit.py`
check #9 — the lint verifies §3.1 enumerates all four tags OR points to Amendment A.
**Check #9 does NOT catch mis-labeled tags** (a `witnessed` claim that should have
been `recall` passes). Semantic accuracy needs sage discipline + Phase-2 verification.

## Bundle maintenance during session

If you discover drift between this bundle and repo state during your work — flag to
Rob, JOURNAL the discovery, and amend `04_RECENT.md`'s Load-bearing facts table via
**append** (don't rewrite). The bundle is living until the next handoff. This is the
"handoff is back-and-forth, not unilateral guess" rule.

## Session lifecycle

`/boot` → confirm `git status` clean → read the most recent handoff + last 5 JOURNAL
entries → set scope (1–2 objectives) at the start → respect stop-signs → leave a
**clean working tree** at session end. Continuous improvement is the baseline
posture, not an option.
