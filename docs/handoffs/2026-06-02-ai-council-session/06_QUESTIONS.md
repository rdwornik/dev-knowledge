# 06 · Comprehension check

Before you do any work, answer these from what you read in `01`–`05`. This is not a quiz
for its own sake — it confirms you can **apply** the bundle, not just paraphrase it. Answer
concisely. Rob will confirm before you proceed.

## Static (methodology + project)

1. What is Rob's model-selection rule — when do you use Sonnet vs Opus, and when should you
   use no AI at all?
2. When do you convene **AI Council** rather than deciding yourself (all conditions), and
   what is the hard cap on debates before implementation?
3. Name two **sacred files** in `ai-council` and the lifecycle rule that protects each
   (e.g. append-only, immutable, single-source-of-truth).
4. What does the **ADR-41 cross-repo ownership** rule forbid this session from doing, given
   that the bundle physically lives in `.dev-knowledge`?

## Tailored to recent work

5. **Apply the hard-metric-closure lens to a hypothetical:** you clear all 17 ruff errors,
   `ruff check src/ tests/` is clean, and the unit suite is green. The operator's task was
   "make ADR-67's gated loop work end-to-end." Are you done? Explain why "ruff clean + tests
   green" is an **easy-metric** here and what the **hard-metric** for that task actually is.

6. The bundle tags "407 unit tests pass" as **`recall`** but "17 ruff errors" as
   **`witnessed`**. Using the **four-tag definitions** (provided inline in `04_RECENT`),
   explain why those two tags differ and what you must do before relying on the `recall`
   claim — versus the `witnessed` one.

7. The bundle calls out two anti-patterns: **new-folder/convention-without-checking** and
   **easy-metric closure**. State (a) your concrete pre-output check before emitting any
   prompt or response that proposes a new file/folder/convention in ai-council, AND (b) your
   closure metric for declaring the "journal the unify" task done — what makes that
   hard-metric, not easy-metric?

## Pass criterion

You pass when answers 1–4 are correct and 5–7 show you grasped the current work — not when
you can restate the files verbatim. If you are unsure of a fact, say so rather than
guessing; that is the correct behavior here.
