# Architect strategic supplement — 2026-07-31-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-31

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================

**1. Strategic intent.** Next window should *use* v6 and report how it behaved, then take
**[#382]** — whose pull-forward was declined last window and is now due. The mechanism arc is
finished; extending it further without live evidence would be building on one dry run.

**2. Tensions weighed.** (a) *Literal instruction vs. working mechanism* — the build brief said
"remove `exist_ok=True`", which would have broken two legitimate re-render paths; I guarded
creation instead and said so. Landed, and the reviewer did not dispute it. (b) *Emitter vs. gate
for the byte budget* — split by site, because a warning nobody must clear is how the paste crept
36.5→59 KB. (c) *Hiding a bad token vs. refusing it* — the sharpest one; see Q3.

**3. Considered + rejected.** Suppressing `..` in the probe tokenizer (F4 attempt 1): **rejected
after it was written**, because it converted an escaping locator's FAIL into a silent PASS. A
pre-existing test caught it; nothing in the review did. Also rejected: exempting the new
`boot_byte_budget` check from the doc→code registry (dishonest — HANDOFF_PROCESS is already a
declaration doc, so a real edge existed); and trimming a neighbouring BACKLOG row to make the
closure clauses fit (condensed the served build narrative instead).

**4. Open questions.** (a) Does the `Destination` row mean *boot destination* or *lane*? This
bundle's own field reads `main`, which is not a sanctioned lane shape — first live evidence, see
`RESIDUAL.md` §4. (b) The night branch's ADR-105 consumption — a decision, not a task. (c) The
08-26 cluster's §3.2-vs-[#364]-4(a) cap conflict, and the split-or-not first call. (d) P0c is
narrowed to a name-match (amendment A2); whether a *serves*-judgment ever gets a mechanical form
is open.

**5. Decomposition rationale.** The arc ran worst-first, one commit per FR, frozen tests re-run
after each — so any regression had exactly one candidate cause. The v6 version bump was held to
LAST deliberately: nothing reaches `main` claiming a contract the build has not shipped.

**6. Off-repo context.** The operator was the serial gate throughout and authorized the merge
explicitly; nothing merged on my judgment. Two review lanes were needed because the skill's
path-guard reviews only the code subset of a mixed diff — budget for both next time.

**7. Ratified-in-chat register.** Three items ratified in this window's chats, **verified live as
NOT in the repo** (grep, not recall) — each is capture-only debt, recorded here and enumerated
with target homes in `RESIDUAL.md` §4:
- **GREEN-on-branch vs GREEN-on-main honesty split** — a claim of green names *where* it is green;
  branch-green is not done. Target: **PLAYBOOK Ch8** or a LESSONS one-liner.
- **Authorized integration act** — merging is an operator-authorized act, not an agent judgment
  call, and the authorization is per-act. Target: **PLAYBOOK Ch4 + HANDOFF_PROCESS §13**.
- **Closure polarity** — a new owning row exists BEFORE the absorbed row closes. Target: the
  **[#447] row** (currently only the ratchet/bootstrap-deadlock family; `tasks/447-*.md` is open
  and does not mention polarity).

**Also recorded here because this window falsified it:** the [#446] seal claimed intake **A6 was
not built**. It was — at `a39f8405`, before the arc. The first live v6 bundle exposed it by
generating a SUPPLEMENT with seven questions. The intake record is corrected in place, and two
stale `6-question` claims in `.claude/commands/handoff.md` (one written during this arc) are
fixed. Using the mechanism falsified what reading it had not.

<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
