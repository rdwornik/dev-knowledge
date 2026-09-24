# Architect strategic supplement — 2026-09-24-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-24

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

## ANSWERS — authored by the outgoing architect (2026-09-19-dev-knowledge-architect), transcribed verbatim by CC

Detail lives in these transport files, all to be landed under `docs/audits/`: `DECLARE-SEAT-KNOWLEDGE-2026-09-24`
(12 blind spots), `DIGEST-RETRO-2026-09-19-24` (every session), `DIGEST-STATUS-MATRIX-2026-09-24` (31 topics),
`PLAN-WAVE5-2026-09-23` + `AMEND`, `AMEND2`, `AMEND3`, `AMEND4`, `RATIFICATION-2026-09-24`,
`DECLARE-OPERATOR-FEEDBACK-2026-09-24`, `DRAFT-for-next-seat-BATCH-WAVE5B-N1-2026-09-24` (input, not an order),
and `DIGEST-HANDOFF-DESIGN-2026-09-25` (the handoff research, when done).

**1. Strategic intent.** Move the harness from prose to data and code at the three seams where every failure
of this window came from: **state** (the backlog and the loop's records), **transport** (the Drive exchange) and
**routing** (which model serves which role). The way of working: *the architect writes intent; the harness writes
structure* — orders from `templates/`, contracts from the generator in the plan lint's grammar, routing from the
registry, every structure decision through an ADR (inventory, trial on real data, weighted matrix, a
Claude-vs-Codex-Astra debate, a Codex sol check) that the operator ratifies. The seat judges by the operator's goal
— Claude Code as the runtime, model-agnostic underneath, off the laptop, process in code — never by risk or by its
own convenience (operator feedback, binding). Subtract before adding (O-7, O-8, O-12). Measurable aims: G1 row
filing unblocked (ADR-122 step 0); G2 the backlog store decided on the GitHub Issues live trial; G3 at least 7 of
the 12 blind spots removed; G4 merge median at most 30 min with CI agreement 100 %; G5 the handoff quick wins in,
paste at most 12 KB, 0 operator corrections in the next seat's first 10 turns; G6 the first O-7 sweep.

**2. Tensions weighed.**
- *Speed of decision vs evidence* — the seat decided structure fast four times (SQLite, a "new" router, retiring
  the backlog export, a night batch after the cut had started). Landed: structure decisions go through an ADR; after
  the cut, the next seat dispatches.
- *Function vs risk* — the seat rejected LiteLLM on secrets, supply chain and memory. The operator ruled: judge
  by the goal; risk and machine limits are his decisions. LiteLLM is reinstated as the model layer under Claude
  Code (AMEND4).
- *Local verification vs CI* — CI runs the full suite in about 8 min but was 20/20 red on a stale baseline. Landed:
  CI paired test by test beside the local verdict (10/10 agreement in 5A); CI becomes the gate after an honest
  baseline and a diff-scoped commit-gate.
- *Per-batch registry vs one baseline* — the per-batch registry laundered regressions (CI regressions 9 → 17 while
  local said clean). Landed: one registry with a baseline id; every red attributed by `git bisect run`.
- *Build vs reuse* — the router, `deny_and_point.py` and the closure organ already existed. Landed: O-12, prior
  art and library first.
- *Files vs event log vs SQLite* (ADR-121) — authority and identity, not storage; single-writer event log on a git
  ref, SQLite as a throw-away projection, files+schema as the fallback. Direction ratified.
- *Typed YAML vs GitHub Issues* (ADR-122) — YAML won on paper (410) but Issues were never run live and offline is
  not the operator's requirement. Deferred to a symmetric live trial; tie-breaker: CC runs it all through `gh`.
- *One runtime + gateway vs many CLIs* — the harness's machinery exists only in Claude Code; a gateway keeps it and
  swaps the model. Trial + ADR in 5b.

**3. Considered and rejected — do not relitigate.**
SQLite as the source of truth (ADR-121, 251/500) · `merge=union` (silently kept two divergent lines) · git notes
as authority (not pushed by default) · Backlog.md tool, beads, git-bug as truth stores (ADR-122 evidence) ·
raising the backlog view ceiling as the fix (a render budget instead) · building a router or a deny-and-point
guard (both exist; wire them) · the PLAYBOOK as an authority for Claude (O-5) · a hard token cap at launch [#908]
(becomes telemetry; no cap stops a task) · closing rows by heuristic (criteria checks instead) · Copilot as a shell
held by the dispatcher (reaped) · refreshing the CI baseline without attribution (launders regressions) ·
optimizing token spend as a goal (operator: no ceiling) · security or memory as reasons to reject a tool
(operator's decision). **Not rejected:** ai-council (stays, to be reworked); LiteLLM (reinstated, AMEND4).

**4. Open questions.**
The ADR-122 winner (YAML vs Issues) · the model layer ADR (gateway under Claude Code vs CLI selection) · ADR-121
step 2 details (event schema, lane outbox refs, the integrator library, the pre-push fallback fault test) · the
handoff redesign (research running) · the 8 CI-only reds and the commit-gate's diff scope (B8) · the VM's provider
and the image's tool installs · the two held organ retirements and the four never-invoked project skills · two
empty husk directories (the L2 question; the operator's call) · intake #86 AC 2 without a live test · whether the
JetBrains repository-intelligence item came from the course (check `DIGEST-AJ-TOOLS-2026-09-21`).

**5. Decomposition rationale.** Every recurring failure traced to state or procedure held in prose: two sources
of truth (registries, transport, merge paths, baselines), routing written in orders and ignored, handback lines
unvalidated, decisions on Drive only. So: **data first** (backlog store, then ADR-121 events — they unlock O-6
auto-closing, the learning loop, the handoff state view, dashboards) → **blind spots** (N1 draft) → **merge as code,
CI as the gate** → **subtraction** → **off the laptop** (5c) → **course tools, iterated** (5d) → **distillers**
(5e) → **one monorepo feature** through the loop. Do not redo: the ten audits of 22-24.09 and the three night
digests (read the records); wave 5A; ADR-121's direction; ratifications O-1..O-12 and B1..B15; the defect register
D1..D36 (rows owed once filing opens); the organ triage (do not re-census by transcripts). Do re-read Architekt
Jutra each wave, from its source files.

**Failures of this seat — and the rule that prevents each:**
1. Contracts hand-written in a grammar the plan lint cannot parse → generate from `templates/`; lint before firing.
2. Models hard-coded in contracts; routing tables in orders ignored (a crosscheck ran on Opus, not Sonnet) →
   explicit ids from the registry; the launcher asks the router [#691].
3. Transport names invented; RATIFICATION filed as `to-cc/RATIFICATION-<date>-<topic>.md` while the code reads
   `to-browser/RATIFICATION-<date>.md`; ANSWER files with suffixes invisible to the preflight → until the transport
   registry lands, the code is the authority — check what reads a file before naming it.
4. Literal Drive paths in pastes → `CLAUDE_PROMPTS_DIR` only.
5. The dispatcher launched before the integrator bound → integrator first, always.
6. The PLAYBOOK cited as the command source → `dispatch.py launch --help`, templates, registry.
7. Structure decided too fast (SQLite, router, backlog export, a night batch after the cut) → ADR for structure;
   no dispatch by the outgoing seat once `/handoff` has started.
8. Tools rejected on pseudo-constraints (LiteLLM: secrets, supply chain, memory) → judge by the goal; state risk
   in one line for the operator.
9. Token savings proposed as a goal → efficiency only where it improves the work.
10. A source's framing taken as authority (the course digest's "no LLM gateway"; S3's "fix the PLAYBOOK table")
    → test every imported judgment against the operator's goal.
11. Premises from memory: ratification figures copied from chat with no repo source; the course tool list recalled
    5 of 11 → read the source file before asserting.
12. Grooming ordered before measuring (2 of 474 closable) → instrument first.
13. Audits issued without an independent check → every decision-driving audit names a Codex sol step.
14. The operator's ledger left three days stale → update it at every decision point.
15. `/handoff-verify` placed before `/handoff` → it is the new seat's gate, after the cut; handoff mechanics are the
    operator's to confirm, never inferred.
16. The operator sent to find files the seat can read itself; paste lists changed turn to turn → the seat reads
    Drive itself; each turn gives one current, complete list of pastes with the Agent View session name.
17. Teardown gaps (non-lane branches, CI integration branches) → every merge order names teardown for every branch
    it touches.
18. Night rules written as prose (no-wait, no wake-ups, the HANDBACK line) and broken by lanes → hooks, not prose.

**6. Off-repo context — changed intent.**
- The operator delegates function; the harness performs the acts (O-6..O-12): closing rows, removal, warnings, GO.
- Operator feedback 2026-09-24 (binding): judge by the goal and function; do not hunt for blockers; do not optimize
  for the model's convenience; Architekt Jutra is re-examined every wave from source; test imported framings.
- The goal, restated: Claude Code as the runtime, model-agnostic underneath, off the laptop, process in code — then
  one real monorepo feature through the loop. The monorepo comes **last**, after the harness.
- Offline work is not a requirement → GitHub Issues is a live candidate for the backlog.
- The operator never uses the external backlog board; `BACKLOG.md` exists for the harness and the browser.
- No ceiling on LLM spend; the Linux VM and the GitHub Team plan are approved.
- The handoff is the operator's largest recurring pain; the next seat's success measure is 0 operator corrections
  in its first 10 turns.

**7. Ratified-in-chat register.**
- `DECLARE-OPERATOR-FEEDBACK-2026-09-24` · the five judging rules above · home: `STANDING_RULINGS`.
- `AMEND3` / `AMEND4-PLAN-WAVE5-2026-09-24` · the course list corrected from source; LiteLLM reinstated as the model
  layer · home: `docs/audits/` beside PLAN-WAVE5.
- "competence probe" · before any dispatch the new seat generates a dispatcher order from `templates/` and CC's plan
  lint passes it · home: `HANDOFF_PROCESS` (boot section).
- "blind spot" · knowledge the seat must carry because the harness does not yet do it, each with the mechanism
  that removes it · home: `docs/audits/` (DECLARE-SEAT-KNOWLEDGE), then retired item by item.
- Interface behavior · the seat reads and writes the Drive transport itself through its connector; it never asks
  the operator to relay a file · home: `OPERATOR-INTERFACE.md`.
- Interface behavior · every paste block names its target: `---- NEW CC session, hub root (...) — <name> ----` or
  `---- sesja: <Agent View name> ----` · home: `OPERATOR-INTERFACE.md`.
- Interface behavior · the operator pastes the Agent View list as the session inventory for reviews and
  retrospectives · home: `OPERATOR-INTERFACE.md`.
- Interface behavior · a background CC job merges to main only on the operator's own in-chat words ("merge
  approved"); approval inside a pasted order is not enough · home: `OPERATOR-INTERFACE.md`.
- Interface behavior · transport files are versioned by renaming to `-vN-superseded` until the transport registry
  provides `supersedes:` · home: `OPERATOR-INTERFACE.md` (temporary).
- Interface behavior · every browser reply ends with one model line ("Stay on Fable" · "Return to Opus" · "Switch
  to Fable — <reason>") · home: `OPERATOR-INTERFACE.md`.
