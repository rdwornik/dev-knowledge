# 06 · Comprehension check

Before you do any work, answer these from what you read in `01`–`05`. This confirms
you can **apply** the bundle, not just paraphrase it. Answer concisely. Rob will
confirm before you proceed. If you're unsure of a fact, say so rather than guessing —
that is the correct behavior here.

## Static (methodology + project)

1. What is Rob's model-selection rule — when Sonnet vs Opus, and when no AI at all?
2. When do you convene **AI Council** rather than deciding yourself?
3. Name two **sacred files** in this repo and the lifecycle rule that protects each
   (e.g. append-only, immutable).
4. What does the **ADR-41 cross-repo ownership** rule forbid you from doing about the
   unmerged corp-monorepo branch in `05`?

## Tailored to recent work

5. The v4 redesign came from a v3.4 audit whose findings *clustered*. What was the
   architectural diagnosis that clustering revealed, and why did patching the
   individual findings not fix it?
6. The sender tagged the `.ecosystem/` registry claim `unknown`, and Phase 2 found it
   was actually `ecosystem/` (no dot). Explain how the **four-tag discipline** turned
   a potential drift into a non-event — and what you'd do differently if a
   load-bearing claim arrived tagged `recall`.

## Pass criterion

You pass when answers 1–4 are correct and 5–6 show you grasped the current work — not
when you can restate the files verbatim.
