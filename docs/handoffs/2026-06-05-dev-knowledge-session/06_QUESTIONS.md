# 06 · Comprehension check

Before you do any work, answer these from what you read in `01`–`05`. This is not a quiz
for its own sake — it confirms you can **apply** the bundle, not just paraphrase it. Answer
concisely. Rob will confirm before you proceed.

## Static (methodology + project)

1. What is Rob's model-selection rule — when do you use Sonnet vs Opus, and when should you
   use no AI at all? (And the new twist: what model does an *unpinned* subagent run on, and
   why is that a bug?)
2. When do you convene **AI Council** rather than deciding yourself — and what is the one
   sequencing constraint on Council work *this* session?
3. Name two **sacred files** in this repo and the lifecycle rule that protects each (e.g.
   append-only, immutable).
4. What does the **ADR-41 cross-repo ownership** rule forbid this session from doing — and
   which artifact this arc lives on *another* repo, not this one?

## Tailored to recent work

5. The bundle teaches **drift-proofing precedence: source → gate → agent** (prefer the
   earliest tier a rule can live in). **Apply it to a hypothetical:** the docs keep
   re-drifting on "how many pre-commit hooks there are" — every few sessions a prose list
   says 6 when there are 8. Walk the precedence: what's the *source*-tier fix, what would a
   *gate* fix look like if source isn't possible, and why is hand-correcting the number each
   time the worst option? (This is exactly what BACKLOG `[#89]` is for.)

6. In `04_RECENT`'s Load-bearing facts table, the `block-onedrive matches Bash + PowerShell`
   claim is tagged **recall — not re-verified at Phase 2** (it lives in `~/.claude/`,
   out-of-repo). Using the **four-tag definitions** (inline in `04_RECENT`), explain what
   that tag obligates *you* to do before you rely on that claim — and how this differs from
   acting on a `witnessed` claim.

7. The bundle calls out two recurring anti-patterns: **new-folder/convention-without-checking**
   and **easy-metric closure** ("tests green" ≠ "issue closed"). State your concrete
   pre-output check before emitting any prompt/response that proposes a new
   folder/naming/convention, AND state your closure metric for declaring a Phase-D doc
   "done" (what makes it hard-metric — e.g. against the staleness map — not easy-metric).

## Pass criterion

You pass when answers 1–4 are correct and 5–7 show you grasped the current work — not when
you can restate the files verbatim. If you are unsure of a fact, say so rather than
guessing; that is the correct behavior here.
