# 06 · Comprehension check

Before you do any work, answer these from what you read in `01`–`05`. This is not a
quiz for its own sake — it confirms you can **apply** the bundle, not just paraphrase
it. Answer concisely. Rob will confirm before you proceed.

## Static (methodology + project)

1. What is Rob's model-selection rule — when do you use Sonnet vs Opus, and when
   should you use no AI at all?
2. When do you convene **AI Council** versus writing an ADR directly via **Path A**?
   Give the criterion, not just an example.
3. Name two **sacred files** in this repo and the lifecycle rule that protects each
   (e.g. append-only, immutable).
4. What does the **ADR-41 cross-repo ownership** rule forbid this session from doing —
   and which sender claims did Phase 2 therefore leave unverified?

## Tailored to recent work

5. **Apply cluster-as-diagnosis.** This session's defining event: a 3-case skill fix
   passed every check, then broke on a 4th invocation state. Suppose you're now asked
   to add a 6th invocation case to the handoff matrix. What does cluster-as-diagnosis
   tell you to do *before* writing the patch, and how would adding just the 6th case
   in isolation repeat the original failure?

6. The sender tagged the ecosystem-registry and ADR-count claims `inferred`, and
   Phase 2 found `ecosystem/` (no dot) is a *static snapshot*, not a process, and that
   "63 ADRs" is really 36 files numbered to ADR-63. Using the **four-tag definitions**
   (inline in `04_RECENT`), explain how the discipline turned these into non-events —
   and what you'd do differently if a load-bearing claim arrived tagged `recall`.

7. The bundle calls out two anti-patterns: **new-folder-without-checking** (3× this
   arc) and **partial-fix / easy-metric closure** (the saga's core lesson). State your
   concrete pre-output check before emitting anything that proposes a new
   folder/convention, AND your closure metric for declaring a task done (what makes
   "done" hard-metric, not "tests green").

## Pass criterion

You pass when answers 1–4 are correct and 5–7 show you grasped the current work —
not when you can restate the files verbatim. If you are unsure of a fact, say so
rather than guessing; that is the correct behavior here.
