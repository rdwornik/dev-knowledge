# Architect strategic supplement — 2026-07-28-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-28

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

=== ANSWERS === (outgoing 2026-07-27/28 browser seat)

1. STRATEGIC INTENT — next session, way-of-working level.
Convert ratified structure into operating reality. The methodology goal:
governance moves from prose to GATES — this window proved the model (two
refusal gates armed; three live catches inside 24h, two of them against
their own builders' commits). Next window extends it: (i) FLIP as first
action once the word "Accepted" exists — blocked on a word, not on work;
(ii) run the first drain slice prep ([#356]+[#358]-[#361], review
2026-08-26) as the proof that the ratchet's pool actually shrinks; (iii)
pay the ratification debt: TWO owed sessions (intake #18 + intake #20) —
ratification sessions are first-class work, not admin. Execution-first
held all window and should hold again.

2. TENSIONS WEIGHED — and where they landed.
(a) Parallel-vs-serial: worktrees used exactly once, when two streams were
GENUINELY concurrent; after integration every remaining arc shared
serialize-group surfaces (audit.py, BACKLOG.md), so the shape became
serial-CC + parallel-CODEX. The real second lane is Codex, not a second CC.
(b) Fix-now vs file: CLOSES_RE defect FILED as [#437], not fixed in
passing — even though it self-reproduces (its own filing commit is now a
false-positive evidence sha). Scope discipline beat convenience.
(c) Baseline precision vs honesty: D4 landed detector-owned measurement
(silent-rule-v4, 428) over the unverifiable census 176. Architect-proposed,
operator-adopted, test-and-iterate. The 176 stays as historical reference.
(d) Converge-vs-stop: the 10-pass terra loop on [#436] was allowed to run
because findings were bounded and converging (5-3-2-3-2-2-1-1-1-0); the
lesson became [#438] (design review BEFORE build for gate-class), not a
mid-arc abort.
(e) Ratify-in-corridor vs evidence-first: #370 refused closure twice;
ruling parked behind a cheap evidence probe rather than taken on the spot.

3. CONSIDERED + REJECTED — do not relitigate.
Pre-commit hooks for BOTH gates (per-machine, --no-verify bypass, no merge
serialization — audit.py ship-gate legs won, twice). Closing #436/#434
inside build/recording arcs (closure is the operator's /review-closures
act, ADR-70 — held even when eligibility was obvious, and the re-verify
discipline caught a real false positive at #370). Silently pinning 176
(instant RED) or silently adopting the higher count (laundering). D3
option (b) fold-into-ADR after the sol review (cost inverted: edits+re-
review > ingest). Editing the date-stamped R12 status cell (dated
verification records are immutable; only the undated outcome line was
stale — that one was fixed). backlog.md-as-viewer, scrummd, rtk: rejected
last window, unchanged.

4. OPEN QUESTIONS — unresolved or deliberately deferred.
ADR-107 ratification: TWO conditional instructions carried no word this
window — the next seat should ask the question PLAIN, first message, not
as a conditional clause inside a prompt (conditionals demonstrably do not
elicit the word). #370: two-state vs third state (user-level ~/.claude);
probe-then-rule; clears #370+#400+#413. Lesson 7 "meta serves object":
the ONLY North Star item with no rule and no row — the question lives
inside intake #20 and MUST be ruled at its ratification session (operator
driver: nothing agreed gets lost). Viewer successor: PARKED EMPTY behind
the mechanical activation gate — re-entry criteria in ADR-107 §3; do not
reopen without them. [#382] desired-state pack: accumulating inputs by
design (7 schema findings + allocation surface); whether it becomes
build scope next window or keeps accumulating is an open sizing call.

5. DECOMPOSITION RATIONALE — what NOT to redo.
Every arc ran contract-first: frozen acceptance contract ex-ante, Codex
lane named, atomic merge, closure by operator act. Do NOT redo: the five
sol edits (folded at 2dca67a5), K1-K5 vocabulary, the viewer REJECT+park,
the declared narrow ADR-65 amendment, the [E8] row-2 amendment + full-pool
intent, D4 baseline semantics, the detector (silent-rule-v4 — changes are
contract changes), the gate mechanism choices, the teardown rule. The
task-graph shape (serial primary, at-launch worktree rule, Codex as the
parallel lane) is proven — inherit it.

6. OFF-REPO CONTEXT.
Operator driver, load-bearing: NOTHING AGREED GETS LOST — it drove the D3
delta review (result: zero items absent; consumption of the 2026-07-21
local doc was faithful; that local file is now safe to archive). Operator
intent recorded in [E8]: the FULL 428-rule pool gets dispositioned over
time — drained, mechanized, or deliberately retired; forgetting is not a
disposition. Operator chose wind-down over same-day flip — respect the
sequencing, don't treat it as drift. Session lesson about the browser
seat itself: twice a memory-based pointer lost to a mechanism (a relabel
script that was approved-but-never-built; a cleanup queued instead of
executed) — the next seat should verify pointers hardest, as the boot
contract already says.
