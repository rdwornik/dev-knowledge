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

5. The bundle's `04_RECENT` describes "cluster as diagnosis" as the structural
   insight that drove v3.4 → v4. **Apply this lens to a hypothetical:** an audit
   returns 5 findings in `scripts/audit.py` — three timing-related (false negatives
   on slow disk I/O), one config-related (wrong default value), one logic-related
   (off-by-one in array bounds). What does cluster-as-diagnosis suggest you do, and
   how would patching the 5 findings individually fail?

6. The sender tagged the `.ecosystem/` registry claim `unknown`, and Phase 2 found
   it was actually `ecosystem/` (no dot). Using the **four-tag definitions**
   (provided inline in `04_RECENT`), explain how the discipline turned a potential
   drift into a non-event — and what you'd do differently if a load-bearing claim
   arrived tagged `recall` instead.

7. The bundle calls out two anti-patterns from the prior session:
   **new-folder-without-checking** (3 instances in 24h) and **easy-metric closure**
   (recurring failure mode). State your concrete pre-output check before emitting any
   prompt or response that proposes a new folder/naming/convention, AND state your
   closure metric for declaring a task done (what makes "done" hard-metric, not
   easy-metric).

## Pass criterion

You pass when answers 1–4 are correct and 5–7 show you grasped the current work —
not when you can restate the files verbatim. If you are unsure of a fact, say so
rather than guessing; that is the correct behavior here.
