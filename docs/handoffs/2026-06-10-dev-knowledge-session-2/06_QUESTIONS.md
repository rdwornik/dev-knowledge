===== FILE: 06_QUESTIONS — start =====

# 06 · Comprehension check

Before you do any work, answer these from what you read in `01`–`05`. This is not a
quiz for its own sake — it confirms you can **apply** the bundle, not just paraphrase
it. Answer concisely. **Every answer must name the bundle file + section it draws
from** (e.g. "04_RECENT › Load-bearing facts") — an answer with no source reference
fails, however well it reads (v4.4 §C). Rob will confirm before you proceed.

## Static (methodology + project)

1. What is Rob's model-selection rule — when do you use Sonnet vs Opus, and when
   should you use no AI at all?
2. When do you convene **AI Council** rather than deciding yourself?
3. Name two **sacred files** in this repo and the lifecycle rule that protects each
   (e.g. append-only, immutable).
4. What does the **ADR-41 cross-repo ownership** rule forbid this session from doing?

## Tailored to recent work

5. The bundle holds that **migration rides on v4.4 §G validation** while **#148/v5 is a
   parallel enhancement.** A teammate says: *"We can't migrate the children until v5
   ships — v5 is the architecture the migration depends on."* **Explain why that is
   wrong**, and name the one repo-state fact the audit established that makes the
   migration available *now*.

6. The sender could have pulled the fleet inventory from memory and tagged it
   `witnessed`; instead the apprentice insisted CC verify it against state. Using the
   **four-tag definitions** (inline in `04_RECENT`), explain how that avoided a drift —
   and what you would do differently if a load-bearing claim reached you tagged
   `recall` instead of `witnessed`.

7. The bundle calls out two recurring anti-patterns — **new-folder/convention-without-
   checking** and **easy-metric closure** (see `01_ROLE` › Standing preferences). State
   your concrete pre-output check before emitting anything that proposes a new
   folder/naming/convention, AND state what makes "done" hard-metric (not easy-metric)
   for promoting v4.4 beta→stable.

## First move (fixed — keep verbatim)

8. **State your first action, why it is first, and what you will NOT touch.**

## Pass criterion

You pass when answers 1–4 are correct, 5–7 show you grasped the current work, and 8
states a concrete first move with an explicit not-touch list — not when you can
restate the files verbatim. **Each answer must cite its source (bundle file +
section); an uncited answer fails that answer** (v4.4 §C). If you are unsure of a
fact, say so rather than guessing; that is the correct behavior here.

===== FILE: 06_QUESTIONS — end =====
