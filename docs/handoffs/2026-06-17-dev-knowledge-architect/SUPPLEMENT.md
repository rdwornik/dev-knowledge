# Architect strategic supplement — 2026-06-17-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-17

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
>
> **FILLED post-generation (the first real #159 dogfood).** This bundle was *generated* cold
> (a fresh CC session; the v5.2 arc it hands off was a *prior* session), but the operator then
> obtained real architect answers and filled the ANSWERS section below — the first time a
> supplement carried a browser-authored strategic *why* rather than a repo-reconstruction.
> `assemble_paste.py` folds the ANSWERS region (below the divider) into the next session's
> `PASTE_THIS`. The answers are the operator-relayed architect's, committed verbatim — CC did
> not author or edit them.

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->
A. **The hybrid handoff is shipped + hardened (v5.2) but the *value* is STILL un-dogfooded.**
   v5.1 answered the design question; v5.2 closed the cold-handoff gap (always-generated
   fillable file + defined cold disposition + ANSWERS-only fold). But no supplement has ever
   been filled with *real answers* and folded into a live `PASTE_THIS`. Is the value considered
   proven now that the mechanism is shipped + hardened, or is the first real fill-and-fold run
   still owed? (#159 — the only-remaining clause; this handoff is again cold.)
B. **PLAYBOOK Move 2 — maintainability, not parallelism (Council-bound).** The structural
   split → thin `§N`-index + per-section modules is justified on maintainability (~84k
   tokens, ~3.5× the read-cap, frequently edited), not parallelism. The `§N`-index design
   is a genuine fork: the §1–§19 spine is the consumer API (ESSENTIALS / CLAUDE.md reference
   by §N), so the split must preserve §N addressability. Still the priority, and does the
   `§N`-index approach hold? (#39 / the playbook serialize-group.)

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

1. **Strategic intent — the way-of-working goal.**
This arc crossed from *building* enforcement to *discovering its two structural gaps*: imprecision and dependency-incoherence. Three mechanisms shipped — a deterministic session-lifecycle Stop-gate, the architect strategic supplement (v5.1 → v5.2), and a fix for the Stop-gate's own auto-bypass loop — and the moment they were in place, the deepest gap surfaced: **nothing catches "a process changed, so its dependent files must update."** A process was edited, a dependent runbook went partially stale, and nothing flagged it — coherence rode on the operator's memory.

So the next session's goal, at the methodology level, is: **make the methodology's own internal dependencies machine-legible and self-enforcing.** Treat this repo as a new kind of program — files are the objects, the AI agent is the runtime — and give it the equivalent of a compiler/linker for its *prose* dependencies. That is the "file-oriented dependency management" thread (now in external research). It is not a side quest; it is the systemic fix for the failure class this whole session kept hitting: coherence-by-memory.

The principle under all of it: **the methodology must practice its own doctrine.** This session caught the enforcement gate violating the anti-bypass rule it exists to enforce, and caught the architect (me) declaring "all verified" with no mechanism to verify. Close that reflexivity gap — enforcement that enforces itself, coherence that depends on no one remembering.

2. **Tensions weighed — and where I landed.**
- **Strict enforcement vs false-positive friction** (the central tension). A gate too eager fires on *correct* states, then loops or trains the operator to bypass it — which is worse than no gate, because it discredits enforcement. Landed: **hard-gate only what is un-gameable AND always-warranted; everything else stays advisory until a precise anchor exists.** The hard JOURNAL leg qualifies (a session must name a real commit — un-gameable). The BACKLOG leg stays advisory because "did this session finish a task?" is not yet mechanically knowable. Resisting early hardening is the right call; hardening an imprecise check is exactly how you manufacture the loop.
- **Carry vs re-derive across the handoff.** The supplement carries the *why* (it originates in the browser; the repo structurally cannot hold it). Repo *state* is never carried — it is forced-read via probes against live state. The dividing line is **re-derivability**: if a fact can drift and can be re-derived from its source, re-derive it, never transmit it. This is what stops the handoff from rotting (the old "v4 disease" was a maintained summary surface that silently drifted).
- **Always-generate the supplement file vs generate-on-answer.** v5.1 only wrote the file *after* answers came back, so a cold/cleared handoff produced nothing. Landed: **always generate the fillable file**, commit it regardless, fold it forward only if it has answers. The artifact's existence is decoupled from whether anyone was present to fill it.
- **Deterministic mechanism vs AI judgment** (the newest tension, deliberately left open for the research). A dependency check must be deterministic so it can't be argued away — but the coherence judgment ("does this doc still *accurately describe* the process?") is semantic, which an AI can assess and a linter cannot. The landing-in-progress: **deterministic trigger/gate, AI semantic assessment inside it.** Do not collapse to either pole.

3. **Considered + rejected — do not relitigate.**
- **Hardening the BACKLOG advisory leg now** — rejected. It is imprecise until the traceability spine (#170) exists; hard-gating it manufactures the false-positive loop we spent a day fixing. It stays advisory; #168 is the promotion and correctly depends-on #170.
- **Fire-once via `stop_hook_active` on the *hard* leg** — rejected outright. Making the hard gate allow-on-retry *is* the persistence-beats-policy antipattern the gate exists to forbid. Fire-once is for *advisory* legs only; the hard leg blocks until genuine compliance.
- **Structural-floor-only for the Stop-hook fix (drop standalone nudges entirely)** — considered, rejected for fire-once + floor-as-backstop, to keep the nudge when `stop_hook_active` is present (it is, at this runtime — verified live).
- **A git-touch heuristic for dependency coherence** ("the process changed but file X didn't → flag") — pre-emptively rejected. It false-positives whenever X *legitimately* needs no change — the exact BACKLOG-advisory failure, generalized. The research is steered toward *precise* detection (version-coupling / content-hash / declared contract), never touch-heuristics.
- **Restating the supplement mechanism in the playbook or instruction files** — rejected by the no-restate invariant. Those surfaces *defer* to the spec; adding the mechanism there would *be* the drift the invariant prevents (this was proven historically by a hand-copied command-name that drifted).
- **Fabricating a marker or a date to silence an advisory** — never. An advisory firing on a correct no-action state is a defect in the *check*, not a prompt to manufacture a marker.
- **Reopening the Stop-gate's shape or the hybrid-handoff design** — off the table. Both landed (the gate is under a scope-freeze through ~2026-07-14; the hybrid became v5.1/v5.2). Forward work is the hardenings, the generator, and the dependency mechanism — not re-deciding settled designs.

4. **Open questions — unresolved or deliberately deferred.**
- **File-dependency coherence (the top open thread).** No mechanism catches "process changed → dependents must update." Now in external online research, framed as *file-oriented dependency management*: classic dependency management (build DAGs, referential integrity, schema migration/semver, docs-as-code single-sourcing, observer/DI patterns) in a prose substrate with an AI executor. My own lean — **deliberately kept out of the research brief so it isn't anchored** — is version-stamp coupling: generalize the existing version-stamp check so every *declared* dependent of a process must carry a matching process-version stamp, forced to re-stamp (after a genuine re-read) on a bump. Weigh that against what the field actually has; there may be a named pattern I don't know. **This is the systemic fix for the failure that interrupted this very handoff — treat it as load-bearing.**
- **The answers-only fold (test it with THIS supplement).** The assembler folds the *answers* (not the questions) into the next session's paste, assuming answers are self-labeling. This is the first real test. I wrote these to be self-contained for exactly that reason — judge whether, read without the questions, they hold. If under-labeled, switch to folding question+answer pairs.
- **The traceability spine (#170 → #168)** — the keystone for precision. Sub-question surfaced this arc: it must recognize **closure-by-deletion** (a task closed by *removing* its line is invisible to an added-marker check). Key it on the issue-ID in the commit, so a closure is legible whether the task line was updated *or* deleted.
- **The generator (#164)** — the last machinery item; everything is hand-assembled until it lands. Open sub-decisions: the runbook sync key, cross-repo v4 routing, the always-file supplement emission, and a freshness gate on the assembled paste against its sources. **New, from the README failure: it must seed/update each repo's runbook idempotently — per-repo runbook drift is now a demonstrated live risk.**
- **PLAYBOOK Move 2** — Council-bound, deferred on maintainability (not parallelism). Any structural split must preserve the §N addressability that the consumer surfaces depend on.
- **Smaller deferred:** the architect actor-vs-mode vocabulary collision (#162 — resolve it, don't leave it live), a shared probe-core (#161), the ASCII-vs-diagram selection rule (#165, awaiting ratification), a doctrine-enforcement-coherence check (#166), the multi serialize-group parser (#167).

5. **Decomposition rationale — what NOT to redo.**
The graph is **two independent build chains, a keystone, and an emerging top thread.** #170 → #168 (spine → hard BACKLOG leg) and #171 → #169 (conformance dashboard → ungated-doc staleness) run parallel to each other and to the handoff group. The **handoff group serializes** — the handoff-touching tasks (generator, probe-core, vocab) share surfaces, so they must not co-schedule. #164 is the last big item; Move 2 dissolves the playbook serialize-group when it lands.

Do **not** re-decide: the hard precedence edges (#168 depends-on #170, #169 depends-on #171) are durable in the task graph — trust them, and do not try to harden the BACKLOG leg before the spine exists. The hard-vs-advisory split, the supplement model, and the Stop-gate's shape are all settled.

One integration to weigh, not redo: the file-dependency-coherence mechanism (coming from the research) likely **connects to or subsumes #169** — both mechanically detect doc incoherence. Before building #169 standalone, check whether the dependency mechanism is its parent. Re-derive the *soft* parallel/unblock judgment against the live backlog; trust the *hard* edges.

6. **Off-repo context — intent, priorities, findings not in the repo.**
- **The operator's mode this arc: fix it properly, in-session — don't defer.** When I recommended deferring the Stop-hook fix to a later session, he overruled it: a defect that misfires at *every* session-end cannot ride to "later." Default to fixing-in-session over deferring.
- **The process must lead the operator by the hand.** The v5.2 supplement-file redesign came directly from his frustration that the handoff was not a clear, structured, *pulled-by-the-hand* flow. Optimize the operator's *path*, not only the mechanism's correctness.
- **The biggest shift is a paradigm reframe.** The README failure (a process dependency nothing caught) led him to reframe the whole methodology as **a new programming paradigm — "file-oriented dependency management"**: Markdown files as objects, an AI agent as runtime, and a need for OOP-grade dependency mechanisms (inheritance/composition/observer analogs) adapted to prose. This is not a local fix; it reframes what the repo *is*. Hold this lens: the methodology is software, the files are its objects, and their dependencies must be managed like a real dependency graph.
- **Verify-first was validated in real time, three times this arc.** A verbatim cap-override message overruled a confident code-read; the live runtime overruled a doc-summary read; the README overruled my own "all verified." The lesson, now empirically hardened: **when a confident read — yours, the executor's, or a documentation summary — contradicts witnessed behavior, the behavior wins; dig until they reconcile.** Treat every report (including the executor's, including your own) as a claim to verify, not a fact.
- **A trust note for you, the incoming architect.** The operator's trust in "all verified" claims was rightly shaken this arc by my overconfidence. Earn it back not with reassurance but by verifying surfaces yourself — and because you are file-less, that means routing verification through the executor's *live* reads and the probes, never through a summary. Do not declare "done" on the easy metric (tests pass / the executor says so); declare it on the hard one (the end state actually meets the goal, checked).
- **Working mode.** The operator relays between this browser (the Layer-1 architect) and the coding agent (the Layer-3 executor); large paradigm questions go to a separate research session. The supplement you are reading is the first real transmission of architect *why* rather than a repo-reconstruction — its quality is the proof-of-concept for the entire v5.1/v5.2 supplement mechanism. Make it worth reading, then make it routine.
