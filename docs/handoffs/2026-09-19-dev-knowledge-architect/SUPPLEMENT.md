# Architect strategic supplement — 2026-09-19-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-19

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
6. **Off-repo context — changed INTENT only.** Intent, priorities and decisions that moved
   this window and are not in the repo. **Not** the operator's interface mechanics — file
   exchange through Downloads, `.md` uploads because a large inline paste arrives empty,
   shipping the exact start command, reports travelling as files. Those are constants, they
   live at `protocols/OPERATOR-INTERFACE.md`, and the incoming bundle's forms card already
   carries them; one of them being wrong is a defect report about that file, not an answer
   here.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo, **and interface BEHAVIORS you relied on that
   are not yet named in `protocols/OPERATOR-INTERFACE.md`** — e.g. a copy-ready block
   substituting for a described action, a paste arriving as a `.md` upload rather than inline
   text, reliance on the `PASTE_THIS.md` END sentinel to detect a truncated paste, or a
   Downloads-directory fallback for file exchange. For either kind: the verbatim term/behavior ·
   a one-line definition (or what relying on it looked like) · its intended durable home
   (BACKLOG id / ADR / LESSONS / PLAYBOOK §, or `OPERATOR-INTERFACE.md` for an interface
   behavior). "None" is a valid answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

answers-to: to-browser/HANDOFF-SUPPLEMENT-2026-09-19.md (7 questions, verbatim from
templates/handoff/v5/SUPPLEMENT.md.tmpl; schema HANDOFF_PROCESS v7.1.0 §13)
authored-by: 2026-09-17-dev-knowledge-architect (Layer-1 browser seat, SEQ 1) — architect-authored,
CC transcribes verbatim and authors nothing here
date: 2026-09-19
scope: strategic WHY only — no repo state, no counts, no SHAs, no methodology restatement

# SUPPLEMENT ANSWERS — .dev-knowledge · architect · 2026-09-19

## 1. Strategic intent

**Stop making the architect knowledgeable; make the system answerable.**

A window's context expires and the next seat starts from nothing. Knowledge held in a seat does not
transfer; a query does. Every hour this window spent re-deriving what the repo already knew is the
cost of getting that backwards.

The concrete way-of-working goal: **the task graph comes from the program, not from the architect's
memory.** The spine runs, stops at the first stage that is missing or miswired, and names it. That
STOP is the queue. The next session should fix that one thing, re-run, and take the next STOP —
not re-plan a wave from a list it authored.

The second goal, equal in weight: **the operator is currently the status board and the copy-paste
relay.** He is asked ten times a day what is running, and he moves files between surfaces by hand.
That is a design defect, not a workload preference. Removing it is a way-of-working objective.

## 2. Tensions weighed

**Understand the whole system first, versus make it answerable.** Landed on answerable. The spine
passed several stages knowing nothing about the corpus, which proves comprehension is not a
precondition for connection. But the reverse also held: you cannot connect what you cannot name, so
coverage of the self-description graph is a real constraint and roughly half the corpus is outside
it.

**Delete, segregate by pointer, or inject.** Landed on inject. Deleting prose was refuted against a
peer repo that holds far more prose and hands over far less. Pointers were refuted by a
retrieval-discipline test written before the conversion. What survived measurement is the mechanism
nobody designed: descriptions that the harness injects into every session are consumed, while
pointers to files are not.

**The distiller as a gate versus as an injection.** Landed on injection. A refusal inside the
agent's tool loop hung a session for half a day; injection changes what the model sees before it
starts and cannot wedge. This is the single most consequential architectural choice of the window
and it rests on a hook property that is only partly verified.

**Build versus wire.** Landed on wire, and the inventory forced it: nothing on the build list was
genuinely absent. Everything planned already existed, unwired or uncalled.

**Speed versus truthfulness at the gate.** Landed on truthfulness, at the cost of this window's
handoff bundle. The gate offered a sanctioned escape whose own documentation says using it would
falsify the record; it was refused. A bundle cut over a gate cleared by fiat is worth less than no
bundle.

## 3. Considered and rejected — do not relitigate

**Deleting documentation to shrink context.** Refuted by measurement against the peer repos: they
segregate what is handed over, they do not hold less.

**Replacing preloaded content with pointers.** Refuted by a test written before the change. A small
model follows a bare pointer a minority of the time.

**A preloaded prose architecture map.** Refuted by its own pre-registered test, twice, on both a
prediction leg and a reads leg. The existing architecture document is KEPT by operator ruling, with
his stated exit condition: it is needed only while the executor cannot view the repository
holistically. Its removal is a deliberate spine-document supersession, never a delete.

**Adopting a code repo-map tool now.** Deferred, not rejected. A standing ruling defers it until a
consumer demonstrably hurts; the consumer that would use it already works without it; and it reads
code only, while this corpus is overwhelmingly prose. Its evaluation is done and recorded — do not
re-run it.

**Adopting the peer harness plugin.** Rejected on a head-to-head on an identical task: same verdict,
same defect count, an order of magnitude more cost and time. Our own lane contract won. This is the
answer to "they do it better than us" — measured, they do not.

**Byte targets as acceptance criteria.** Rejected three times over, each time after producing a
worse artifact. Acceptance is the question an artifact answers, never its size. A large
well-organised file is valuable; a small chaotic one is not.

**Raising the silent-rule baseline a second time.** Rejected. The first raise was accepted as a
one-off and explicitly not a precedent; raising it again would have made that sentence false and
turned a ratchet into a counter. The prose was removed instead — and that removal is NOT a fix,
because the underlying rule remains unenforced.

## 4. Open questions

**Does a registered command with an injected description actually get called unprompted?** The first
measurement scored zero. The whole line "the harness knows, so the architect needn't remember" rests
on this. Until it is answered, treat that line as unproven — not as a foundation.

**Does the rule forbidding any session from launching a lane survive its falsified premise?** It was
ratified on the belief that a nested session gets no visible row; that belief is contradicted twice,
once in a container and once on the host. The operator has been firing lanes by hand because of it.

**What makes a temporary measure expire by itself?** An emergency order marked temporary ran for
days because nothing expired it and nothing reported it. Every dated exception now proposed inherits
this question.

**Can a spend cap be enforced at launch rather than observed after the fact?** Today it is polled, so
a lane spends whatever it can between polls. Every budget this window set was exceeded, several
times over.

**Should the two gates that refuse forever be narrowed, and in what expiring form?** One counts
headings in an append-only file where correction-by-addition is the only correction its own
invariants permit; the other refuses on an immutable dated artifact that has already run. Both are
scoping defects rather than debt — but narrowing a gate touches every future session and the
operator's condition is that any such change be temporary by construction, with a test proving the
uncorrected case still fails.

**Can the distiller carry a real payload at prompt-submit time?** The hook survey answered part of
it; a distiller-sized injection is untested.

## 5. Decomposition rationale — and what NOT to redo

The wave shape is settled and should not be re-derived: disjoint surfaces, one worktree per lane,
a failing test before any code, cross-provider review before handback, commit-and-STOP, and a single
integrator that merges and never builds. It worked unattended, including a lane that refused to
weaken a check it inherited and one that surfaced a genuine conflict in its own contract rather than
resolving it.

**The important shift is where the graph comes from.** Earlier waves were decomposed by the
architect from a list. The last one was not: the spine named its own next failure. The next session
should NOT open by planning a wave. It should run the spine, read the STOP, fix that, and re-run.

Do not redo: the four refuted beliefs in §3; the census that replaced a binary with three states
(observed / reachable-but-unobserved / unreachable) and dissolved a number that had misled this
project three times; the split that keeps the hub shipping executable code while the caller runs it,
which satisfies both the operator's ruling and the layer invariant without suspending either; and
the decision that the architecture document stays.

Do not re-open the peer-repo comparison or the repo-map evaluation. Both are done, recorded, and
their conclusions are in §3.

## 6. Off-repo context — changed intent

**Dependencies are a consequence of library-first, not a question.** The operator overruled a request
for per-dependency consent as stalling. His condition replaced it and is stronger: a library is not
adopted until it has been run live and its output pasted. A library added without ever being
executed is declared, not adopted — and he named this as the central failure mode of LLM-driven
work.

**The window's purpose changed mid-course to consolidation.** No new execution; conclusions, cleanup,
handoff preparation.

**The dispatcher is expected to dispatch.** The operator firing a lane himself was recorded by him as
an exception, not the design. He said this before we discovered the rule that forced it rests on an
unmeasured premise.

**Lane count comes from logic and need, not from a ceiling.** The ceiling was a prosthesis for an
integration problem that is now only partly fixed.

**The operator's frustration is itself intent and should be read as a requirement.** Being the status
board, relaying files by hand, and being asked to remember what the system should know are named as
defects to remove, not as inconveniences to tolerate.

## 7. Ratified in chat, not yet in the repo

**Terms and rulings:**

- **"The STOP is the work queue."** A spine stage with no command — or one whose command was never
  actually invoked — is a disconnection made visible, and an uninvoked command is indistinguishable
  from a miswired one until called. Durable home: the spine's own doctrine section in PLAYBOOK.
- **"Declared is not adopted."** A dependency, or any library, counts as adopted only once it has
  been run and its output recorded. Home: the contract's library-first field specification.
- **"prior-art is a citation, not a sentence — and it searches our own archive before the world."**
  Ruled in chat; still only prose. Repeatedly this window the answer already existed in our own
  audits and was paid for again. Home: the contract field specification plus the gate that reads it.
- **"A ratchet drop that removes prose is not a fix."** Recorded in one row body today; it is
  doctrine and belongs where metrics are defined.
- **"Temporary is only safe when its expiry is a mechanism."** From an emergency order that outlived
  its own label. Home: LESSONS, and as a precondition on every dated exception.
- **"Acceptance is the question the artifact answers, never its size."** Three byte targets, three
  worse artifacts. Home: the contract's done-when specification.

**Interface behaviours relied on and not yet named in the operator-interface doc:**

- **The supplement round-trip over the transport.** Questions written to the browser-bound folder,
  answers authored by the browser seat and written back to the agent-bound folder, with the operator
  handing the executor one line naming the file. This was invented in this window specifically to
  stop the operator being a copy-paste relay in both directions. It needs a durable home.
- **The browser seat writing its own ledger and ratification records directly to the transport**,
  rather than asking the operator to relay them. Both were owed all window and were only written
  when a gate refused for their absence.
- **The session list of the agent console used as the fleet status board**, because no
  "where is this lane right now" surface exists. This is a workaround standing in for a candidate
  that was costed weeks ago and never consumed.
