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

5. `04_RECENT` describes the **staleness-map incident**: a *verification artifact* (a
   sweep's staleness map) itself made an unverified claim about `ARCHITECTURE.md` that
   a grep disproved. **Apply the lesson to a hypothetical:** a sweep report hands you
   "subsystem X is documented in `ARCHITECTURE.md`." What do you do before acting on it,
   and how would simply trusting the report fail?

6. The sender tagged the `docs/machinery-inventory` branch's existence `recall` ("may
   still exist"), and Phase 2 found the branch no longer exists. Using the **four-tag
   definitions** (provided inline in `04_RECENT`), explain how the discipline turned a
   potential drift into a non-event — and what you'd do differently if a load-bearing
   claim arrived tagged `unknown` instead.

7. The bundle calls out two anti-patterns from the prior session:
   **new-folder-without-checking** (3 instances in 24h) and **easy-metric closure**
   (recurring failure mode). State your concrete pre-output check before emitting any
   prompt or response that proposes a new folder/naming/convention, AND state your
   closure metric for declaring a task done (what makes "done" hard-metric, not
   easy-metric).

## First move (fixed — keep verbatim)

8. **State your first action, why it is first, and what you will NOT touch.**

## Pass criterion

You pass when answers 1–4 are correct, 5–7 show you grasped the current work, and 8
states a concrete first move with an explicit not-touch list — not when you can
restate the files verbatim. **Each answer must cite its source (bundle file +
section); an uncited answer fails that answer** (v4.4 §C). If you are unsure of a
fact, say so rather than guessing; that is the correct behavior here.

===== FILE: 06_QUESTIONS — end =====
