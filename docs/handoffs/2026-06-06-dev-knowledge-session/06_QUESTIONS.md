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
2. When do you convene **AI Council** rather than deciding yourself — and where does a
   **scoped Dynamic Workflow** sit on the escalation ladder relative to it?
3. Name two **sacred files** in this repo and the lifecycle rule that protects each
   (e.g. append-only, immutable).
4. What does the **ADR-41 cross-repo ownership** rule forbid this session from doing —
   and how does **ADR-72** sharpen that for a cloud session?

## Tailored to recent work

5. The bundle's `04_RECENT` names **"contract guarantees live on the executing path"**
   as the doctrine that drove this arc's nightly-conformance fixes. **Apply this lens to
   a hypothetical:** a teammate adds a validator that recomputes the digest counts but
   wires it only into the *local* pre-commit hook, while the digest is actually produced
   by the *cloud* scheduled Routine. Why is that validator "decoration," and what would
   make it load-bearing instead?

6. This session, #86.2's UNDERSTAND step verified two facts that **killed its own
   premise** (the private hub makes plugin + URL-fetch inert in a clone-only cloud
   session), and the task STOPPED with options instead of shipping. Using the **four-tag
   definitions** (provided inline in `04_RECENT`), explain why a premise carried as
   `recall` into a contract is dangerous — and what you would do before encoding any
   `recall`/`unknown` claim into a prompt or amendment.

7. The bundle calls out two anti-patterns Rob watches for —
   **new-folder/convention-without-checking** and **easy-metric closure** (both recurring
   failure modes; see 01_ROLE › Standing preferences, and the #84 n=2 gate in 05_NOW).
   State your concrete pre-output check before emitting anything that proposes a new
   folder/naming/convention, AND state your closure metric for declaring #84 "done" (what
   makes it hard-metric, not easy-metric).

## First move (fixed — keep verbatim)

8. **State your first action, why it is first, and what you will NOT touch.**

## Pass criterion

You pass when answers 1–4 are correct, 5–7 show you grasped the current work, and 8
states a concrete first move with an explicit not-touch list — not when you can
restate the files verbatim. **Each answer must cite its source (bundle file +
section); an uncited answer fails that answer** (v4.4 §C). If you are unsure of a
fact, say so rather than guessing; that is the correct behavior here.

===== FILE: 06_QUESTIONS — end =====
