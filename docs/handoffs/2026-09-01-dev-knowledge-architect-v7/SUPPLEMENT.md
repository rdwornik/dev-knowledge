# Architect strategic supplement — 2026-09-01-dev-knowledge-architect-v7

Repo: .dev-knowledge · Mode: architect · Date: 2026-09-01

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
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

**1. Strategic intent — flip the operating mode from PUSH to PULL.** The seat stops carrying
state and starts answering `/boot-session`'s proposals: **repo proposes** (frontier, priorities,
next batch), **browser rules**, **operator decides**. The next session's way-of-working goal: run
the FIRST window that opens with `/boot-session`, executes `[#632]`'s n=2 acceptance, tags
v1.5.0, and performs the monorepo instantiation **attended** — proving the engine **deploys**,
not just governs itself.

**2. Tensions weighed.**
- **(a) speed vs trust — resolved for TRUST.** Terra pre-merge on every lane (~11 min/pass),
  after measuring **9 of 17 merges unreviewed**.
- **(b) visible shrinkage vs honest blockers — resolved for HONESTY.** VISION and ESSENTIALS
  waited for real re-reads and a fleet census rather than fake stamps.
- **(c) codespace-now vs window-close — resolved by doctrine option 4 + a PARKED precondition.**
  Local lanes ran; the codespace proved transport+gates but stays **NON-DEFAULT** until the n=2
  long-run acceptance.
- **(d) operator visibility vs token cost — resolved by ORGANS** (ledger, atlas, OPERATOR ASKS
  with `re-asked` RED) instead of chat answers.

**3. Considered + rejected — DO NOT RELITIGATE.**
- LangGraph-class orchestration for the hub — Layer-2 never executes; the moat is gates and
  contracts (A6 record).
- Fibonacci / golden-ratio graph aesthetics.
- TFP-class probabilistic inference over a ~1k corpus — R-A: sqlite answers in 1–4 ms.
- Harbor adoption NOW — DM-1 measured **risk relocation**, not effort reduction.
- Deleting `codex/` or `conformance.html` — live consumers measured.
- Cost caps on codespace before any spend.
- A root `dashboard/` folder — `docs/dashboard/` ruled, universal via the docs-tree carrier.
- `ecosystem/dashboard` — hub-only, non-scalable.
- A `SKIP=`-based v7 bump — atomic-at-integration ruled instead.

**4. Open questions.**
- `[#632]` acceptance **n=2** (M-sonnet + S + fuse test) — the hang's root cause is still only
  **bounded, not named**.
- `[#628]` ESSENTIALS dissolution scope — 10 consumers, rides with v1.5.0.
- ROOT-R1 `config/` verdict — FILL vs DISSOLVE into `pyproject`; census dispatched, **unruled**.
- intake #66 ratification — operator's.
- the scoring model for `/boot-session` — the BOOT-R1 artifact landed, the model is **unpinned**.
- `[#617]` distiller Tier-L design — eval-loop precondition met, build **unscheduled**.
- the equilibrium-map + history-delta bundle sections — batch-G seed.

**5. Decomposition rationale.** Batches are **file-disjoint frozen lanes with ONE serial
integrator** (Monitor-Object) because every defect class measured —
*five-lanes-consistent-alone*, *root-copy-vs-executing-copy*, *amendment-cannot-subtract* — is
**only catchable at integration**. **Do NOT redo:** the seven-predicate validator, the manifest
`closed_by:` exemption, terra pre-merge, R-MODELS routing (sonnet workers), the four-option
substrate doctrine, optimum-6 / ceiling-12. **The next seat inherits a working machine; its job
is throughput and deployment, not re-architecture.**

**6. Off-repo intent — changed this window.**
- Priority order **hardened**: **monorepo deployment FIRST**, ai-council second, win-tooling
  receives migration **last** though it remains consumer #1.
- **Token economics matter**: enterprise/free quotas before Anthropic quota — **measured, not
  capped**.
- The **master's thesis is the AUTONOMY arc's North Star** — adversarial debate as decision
  mechanism, flip-conditions on every ADR.
- The operator wants **pull-mode urgently** — handoffs shrink to `/boot-session` + residual.
- **Codespace-as-default is a standing operator expectation**, gated only by the n=2 proof.

**7. Ratified-in-chat register — NOT yet in the repo.**
```
term                                   definition                                durable home
OPERATOR ASKS re-asked>=2 => RED       a twice-asked ask with no visible-fix      landed in #66 --
                                       and no named blocker renders RED           VERIFY the digest
                                                                                  renders it
boot-* prefix-first command naming     commands sort by boot-* prefix             census candidate;
                                                                                  commands+skills
                                                                                  census row
TRACE before VIEW                      the trailer/signal lands BEFORE any        recorded in #66
                                       panel renders it
equilibrium map + history delta        two GENERATED /boot-session sections       batch-G seed --
                                                                                  NEEDS A ROW ID
integration=LOCAL always /             the four-option substrate doctrine,        VERIFY the dispatch
read-only=CLOUD /                      one line per axis                          chapter carries all
execution=CODESPACE-on-green /                                                    four VERBATIM
local-execution=explicit-request
```
Everything else ratified this window is, to the operator's knowledge, already in tree with ids.

<!-- ANSWERS captured 2026-09-01 by the batch-F integrator from the operator's ruling message,
     recorded verbatim in substance. The three VERIFY items above are discharged in the same
     arc that lands this file; their results are in the JOURNAL entry, not edited into this
     immutable bundle artifact. -->

<!-- INTEGRATOR FOOTNOTE, appended after the ANSWERS were recorded; the operator's text above is
     unaltered. Two of the answers were DISCHARGED the same day by a concurrent seat, which is
     recorded here so the incoming session does not act on a condition that has already lifted:

     - §4 open question "[#632] acceptance n=2 (M-sonnet + S + fuse test) -- the hang's root
       cause is still only bounded, not named" -> **MET AND NAMED.** Two lanes, two codespaces,
       both end-to-end, both committing and pushing from inside (Lane A M/sonnet attached 863 s
       exit 0; Lane B S via -Detach). The hang is measured out: in-container suite 294.07 s real
       against 8 m 23 s user -- CPU proportional to wall-clock, the inverse of the 75-min/3-s
       signature. Root cause of the transport half NAMED: gh's `--` block was appended AFTER the
       operands, so `-- -O -i KEY` was never a passthrough -- the flags became file operands.
       Evidence: docs/audits/2026-09-02-technical-batch-f-close-packet.md AMENDMENT 3.
     - §6 off-repo intent "codespace-as-default is a standing operator expectation, gated only by
       the n=2 proof" -> the gate has LIFTED. `execution = CODESPACE` is now the default; the
       four axes in PLAYBOOK Ch8 Layer 1 carry it, and `local-execution = explicit-request` is
       what keeps that default honest.

     The remaining §4 open questions are untouched and still open. -->
