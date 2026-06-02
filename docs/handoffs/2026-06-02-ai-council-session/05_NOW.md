# 05 · What to do now

## Immediate objective

No code work is mid-flight — the 7-file unify is merged and the tree is clean. The two
pending items the operator named are **the ADR-67 implementation obligation** (tracked,
deferred) and **the 17 pre-existing ruff errors** (known debt). Neither is started; both
need an operator go-ahead before they become this session's scope. The one zero-judgment
loose end is **journaling the unify** (the JOURNAL's newest entry predates it). Scope of
likely next work: docs/process first, then optionally code housekeeping.

**Sage's recommendation (carry forward, not a forced rank):**
- **(a) Journal the unify — 5 min, do first.** Prepend a JOURNAL entry recording the 7-file
  canonical unify (`e91ba24`/`b4135e3`) + the D1 reversal, so the business record matches
  git. Pure hygiene, no decision required.
- **(b) ADR-67 downstream pieces (BACKLOG #9) — only on operator go-ahead.** `[P3][L]`:
  the `/council-question` template, the question-quality gate, deterministic
  `council.return_dir` I/O from `~/.claude`. Deferred until the canonical baseline settled
  (it now has) — but it is large and mirrors `.dev-knowledge` #70; confirm before building.
- **(c) Clear the 17 ruff errors — Sonnet/medium housekeeping.** Known debt, not a
  regression; `ruff check src/ tests/` enumerates them. Good debt-clearing pass before any
  larger work. Verify with `.\scripts\check.ps1` after.

## Top priorities (from BACKLOG)

- **[P1] Synthesizer refresh (#1→#2→#3):** score the Gemini synthesizer against ~15
  historical transcripts (#1), then execute the Phase-3 conditional — amend ADR-01 + ship
  Branch A (new synthesizer) or Branch B (keep Gemini) (#2, blocked on #1); codify the
  cost-optimization principle in the amendment (#3). This is the repo's only open P1 theme.
- **[P3][L] ADR-67 gated loop (#9)** — the operator-flagged pending obligation (see (b)).
- **[P2] Provider reliability (#5 openai_deep integration path) + naming automation (#7 CI
  check for ADR-34).** Full queue in `BACKLOG.md` — do not duplicate it here.

## In-progress branches & repo state

- `ai-council` has **only `main`** — no open feature branches. The unify branch
  (`chore/ecosystem-unify`) is already merged at `b4135e3` and gone.
- **`main` is ahead of `origin/main` by 186 commits** (local-first; not pushed). Normal for
  Rob's workflow — flag only if a push is expected.
- **Branch:** `main`  ·  **HEAD:** `b4135e3`  ·  **Working tree:** clean.
- (This bundle was generated read-only from `.dev-knowledge` worktree
  `chore/ai-council-handoff`; nothing was written to the ai-council tree.)

## Boundaries

- **Do NOT build ADR-67 (#9) without an operator go-ahead** — it is `[L]`, deferred by
  design, and mirrors an open `.dev-knowledge` item.
- **Do NOT treat the 17 ruff errors as "done" because tests pass** — they are open debt.
- **Do NOT merge `xai.py` and `deepseek.py`**, and do NOT change `_anonymize_responses()`
  shuffle without an ADR (blind-voting contract).
- **Do NOT hardcode** model strings/prompts/costs — they belong in `config/settings.yaml`.
- **Do NOT edit another repo** from here (ADR-41); **do NOT touch `OneDrive - Blue Yonder`**.
- Looks-wrong-but-intentional: the JOURNAL's newest entry says "D1 = Defer the BACKLOG
  migration" — that was **superseded by the unify**, which migrated it. Journal the reversal
  rather than reverting the migration.

## How to choose

If you face multiple candidate first-moves, **propose your choice with rationale** — don't
ask Rob to forced-rank. Operator energy is finite; reasoned pre-selection is your job. Rob
confirms or redirects.
