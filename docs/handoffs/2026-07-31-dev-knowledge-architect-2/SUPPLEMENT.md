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

**1. Strategic intent.** Boot THROUGH v6 live and report how it behaved — the window opens by
producing the mechanism's first real evidence, including the `Destination=main` question it already
surfaced. Then ratify the ingested operator intake **§A (decision routing)** + **§B (standing
standards)** as XS rulings — they codify the boundary the operator enforced mid-window, so
ratification is **transcription, not debate**. Then **[#382]** under **§E**'s functional
requirement, ratified alongside, so the chain closes against operator intent, not only technical
Done-whens. Way-of-working goal: **the operator states functional requirements; the harness
implements.**

**2. Tensions weighed.** (a) *Literal instruction vs working mechanism* — "remove `exist_ok=True`"
would have broken two sanctioned re-render paths; guarded creation landed, declared, undisputed.
(b) *Emitter vs gate for the byte budget* — split by site; a warning nobody must clear is how the
paste once crept 36.5→59 KB. (c) *Suppress vs refuse for bad tokens* — the sharpest: suppression
converts FAIL into silent PASS; refusal at resolution landed. (d) *Executor-drafted vs
architect-authored judgment artifacts* — surfaced by this supplement's own first fill; ruled:
**judgment artifacts are architect-authored, the executor supplies verified facts.** Register
item 5.

**3. Considered + rejected.** Suppressing `..` in the tokenizer — rejected *after* being written: a
**pre-existing test, not the review, caught it** (the lattice out-earned the reviewer). Exempting
`boot_byte_budget` from the doc→code registry — dishonest; a real edge existed. Trimming a
neighbouring BACKLOG row to fit closure clauses — condensed own narrative instead. Treating the
night dossier's "not genuinely open" verdicts as authority — every ruling was still pinned against
live sources; **INPUT-NOT-AUTHORITY held under pressure.**

**4. Open questions.** (a) `Destination` row: **boot destination or lane?** This bundle's own field
reads `main` — not a sanctioned lane shape; first live v6 evidence, `RESIDUAL.md` §4. (b) Night
branch **ADR-105 consumption** — a decision, not a task. (c) **08-26 entry gate**
(§3.2-vs-[#364]-4(a)) + the split call, now with intake **§F** ("backlog must shrink") arriving as
the cluster's pending functional requirement. (d) **P0c**: narrowed to name-match (A2); whether a
*serves*-judgment ever gets a mechanical form stays open. (e) **Intake ratification batch** + **§D**
research rows (repomix / pyadr / copier — **grep-first**) + **§C/§H**: the grok shadow and the
portability probe are **ONE first arc**.

**5. Decomposition rationale.** Worst-first, one commit per FR, frozen set re-run after each — one
candidate cause per regression; the version bump held to **LAST** so nothing reached `main` claiming
an unshipped contract. **Do NOT redo or re-decide:** R1–R7 with amendments **A1/A2**, the **F1–F8**
fix set, closures **[#446]/[#421]**, the intake's **§I sequencing** (re-affirmed by the outgoing
seat, zero amendments), and the **A6 correction** — it is now repo fact.

**6. Off-repo context.** The operator was the serial gate throughout; every merge **per-act
authorized**, none on agent judgment. Mixed diffs need **BOTH Codex lanes** (skill path-guard = code
subset only) — budget both. The operator's design input is **ingested as SEED this close**; its
§A/§B mirror rulings the operator already exercised live in this window. The **supplement-authorship
defect happened HERE and was operator-caught**: the close instruction delegated the fill to the
executor; corrected by wholesale re-authoring — **codification owed** (register item 5).

**7. Ratified-in-chat register** — verified live as **NOT in repo**; capture-only debt with target
homes:
1. **GREEN-on-branch vs GREEN-on-main honesty split** — a claim of green names *where*; branch-green
   is not done. → **PLAYBOOK Ch8** or **LESSONS**.
2. **Authorized integration act** — merging is operator-authorized, **per-act**, never agent
   judgment. → **PLAYBOOK Ch4 + HANDOFF_PROCESS §13**.
3. **Closure polarity** — the new owning row exists **BEFORE** the absorbed row closes. → the
   **[#447] row** (currently ratchet-family only; polarity unmentioned).
4. **Decision-routing boundary** — operator rules functional, architect decides-records-reverts
   technical, Council distills contested. → **ratifies via the ingested intake §A**.
5. **Supplement authorship** — SUPPLEMENT answers are **architect-authored**; the executor supplies
   **verified facts only**. → **HANDOFF_PROCESS §13 one-liner + PLAYBOOK**.

Also on record: the **A6 claim was falsified by first live use** (built at `a39f8405`; the intake
record and two stale `6-question` claims corrected) — **using the mechanism falsified what reading
it had not.**
