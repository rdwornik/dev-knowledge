# 06 · Comprehension check

Before you do any work, answer these from what you read in `01`–`05`. This is not a
quiz for its own sake — it confirms you can **apply** the bundle, not just paraphrase
it. Answer concisely. Rob will confirm before you proceed.

## Static (methodology + project)

1. What is Rob's model-selection rule — when do you use Sonnet vs Opus, and when
   should you use no AI at all?
2. When do you convene **AI Council** rather than deciding yourself?
3. Name two **sacred files** in this repo and the lifecycle rule that protects each
   (e.g. append-only, immutable).
4. What does the **ADR-41 cross-repo ownership** rule forbid this session from doing?

## Tailored to recent work

5. The session's organizing thesis was **"drift-proof at the source first; gate only
   what can't be made self-documenting; reserve agents for what neither covers."**
   **Apply it to a hypothetical:** a doc hardcodes "the audit has 12 checks" and keeps
   going stale every time a check is added. Which of the three layers (source / gate /
   agent) is the right fix, why — and what would be wrong with simply adding a
   pre-commit hook that greps for the number?

6. The hub now distributes its doc-tooling as pre-commit hooks. Rob expected "deploy
   once from the hub, all repos update." Explain **why that zero-touch model is
   impossible here**, what model we chose instead, and what single environmental fact
   makes the current `../.dev-knowledge` wiring work — and would silently break it.

7. The sender tagged "PLAYBOOK ~2710 lines" as **`recall`**, and Phase 2 found it was
   actually **2888**. Using the **four-tag definitions** (provided inline in
   `04_RECENT`), explain how the discipline turned a potential drift into a non-event —
   and what you'd do differently if that same number had arrived tagged `witnessed`.

8. The bundle calls out two failure modes from the prior session:
   **architecting-before-grounding** (the codemap-pilot premise that nearly destroyed a
   curated diagram) and **easy-metric closure** ("tests green" ≠ "issue closed"). State
   your concrete pre-action check before you encode an assumption about repo state into
   a prompt, AND state your closure metric for declaring a task done (what makes "done"
   hard-metric, not easy-metric).

## Pass criterion

You pass when answers 1–4 are correct and 5–8 show you grasped the current work — not
when you can restate the files verbatim. If you are unsure of a fact, say so rather
than guessing; that is the correct behavior here.
