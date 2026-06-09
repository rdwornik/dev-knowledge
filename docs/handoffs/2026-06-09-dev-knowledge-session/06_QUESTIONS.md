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

5. `04_RECENT` carries the principle **"a high error rate is a signal — when fixes
   keep finding fixes, the machinery is heavier than the problem"** and the related
   **"build-ahead-of-need"** trap (the floor was the instance). **Apply this lens to a
   hypothetical:** you propose a new validator, and shipping it requires three
   consecutive fix-up commits to get the gate green. What do these two principles tell
   you to do — and how would "just push the third fix and move on" be the wrong call?

6. The sender tagged the **corp-sca floor hash** and **AI Council test-count** claims
   in a way that made Phase 2 carry them as *sender-reported* rather than asserting
   them (see `04_RECENT` › Load-bearing facts). Using the **four-tag definitions**
   (provided inline in `04_RECENT`), explain how the discipline kept a cross-repo claim
   from silently becoming "fact" — and what you'd do differently if a **load-bearing**
   claim arrived tagged `recall`.

7. The bundle calls out two anti-patterns from the prior session —
   **new-folder-without-checking** and **easy-metric closure** (both recurring failure
   modes; see `01_ROLE` › Standing preferences). State your concrete pre-output check
   before emitting any prompt/response that proposes a new folder/naming/convention,
   AND state your closure metric for declaring a task done (what makes "done"
   hard-metric, not easy-metric).

## First move (fixed — keep verbatim)

8. **State your first action, why it is first, and what you will NOT touch.**

## Pass criterion

You pass when answers 1–4 are correct, 5–7 show you grasped the current work, and 8
states a concrete first move with an explicit not-touch list — not when you can
restate the files verbatim. **Each answer must cite its source (bundle file +
section); an uncited answer fails that answer** (v4.4 §C). If you are unsure of a
fact, say so rather than guessing; that is the correct behavior here.

===== FILE: 06_QUESTIONS — end =====
