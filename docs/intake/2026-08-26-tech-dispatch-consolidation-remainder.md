---
intake-id: 52
status: READY
origin: endgame governance session, 2026-08-26; WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII I4
consumers: wave-2 rows for the substrate validator, the dispatch drift organ, and Layer-3 router adoption
---

# Dispatch consolidation — the remainder: one voice, one verb, and organs that refuse

## Problem / motivation

A single act — launching a lane — had **four documented commands**, which made every seat
"correctly informed and wrong". The measurement that ended it is landed
(`docs/audits/2026-08-25-technical-dispatch-surface-measured.md`, L1) along with the five-act plan
(`…-technical-dispatch-consolidation-plan.md`, L2) and the transport build
(`…-technical-dispatch-codespace-build.md`, L3).

**Acts 2 and 3 of that plan are DONE and are recorded here as done, not re-proposed.** Lane RL
executed them: `/lane-boot` now emits the ruled verb `dispatch <contract-path>` where it previously
emitted a raw `claude --worktree … --bg …` form that silently dropped `--model` and `--effort`, so
the most-invoked boot surface in the repo ran lanes at whatever the CLI defaulted to rather than at
the routing their contract declared; and PLAYBOOK Ch8 is now the single literal-command site, with
the other sites reduced to pointers. **This intake owns only what remains.**

What remains is the part that makes the fix **structurally unrecurrable** rather than merely
currently-correct. Three things, in this order:

1. **The substrate VALIDATOR — first, because it refuses.** A contract today names a substrate and
   nothing checks that the substrate exists, that its gates can run there, or that its paths are
   reachable from it.
2. **The drift organ — second, because it detects.** A doc naming a dead or rival command is how
   the four voices arose; nothing notices when a page drifts from the machine.
3. **Layer-3 router adoption — third, because it depends on both.**

**The stated limitation that must travel with the rule.** `dispatch` is **LOCAL-ONLY**. It does not
read a contract's `Substrate` field and cannot route: today the substrate is chosen by *which verb
the operator types*, and a contract's Substrate line is documentation. This limitation went
unstated once and **misled a seat** — Part VII records it as the "rule without a boundary" class.
Until Layer 3 lands, **Ch8 must state the local-only limitation in the same sentence that names
the verb.**

## Scenarios (+1 view)

- **As a contract author**, I declare `Substrate: cloud` and put a gate in my Done-when; the
  validator **refuses** the contract instead of a lane discovering mid-run that gates cannot run there.
- **As the operator**, a doc that names a command my machine no longer has goes **RED at commit**,
  so the page cannot drift from the machine again.
- **As a person who has never seen this fleet**, I dispatch one lane on each substrate using
  **only PLAYBOOK Ch8**, and ask zero questions. *(This is the acceptance test; the operator judges.)*

## Functional requirements

- **Must — substrate registry + validator, REFUSE-shaped:** refuse a contract naming a substrate
  with **no live verb**; refuse **cloud + a gate in its Done-when**; refuse **codespace/cloud + an
  operator-disk path**; **WARN** on a second local writer in one checkout. An override is an
  **explicit recorded deviation**, never a silent pass.
- **Must — drift organ:** every literal command in Ch8 resolves via `Get-Command` on the
  operator's machine at commit time, and `/lane-boot` contains the ruled verb.
- **Must — the substrate decision tree in Ch8:** Q1 gate-dependent → never cloud · Q2
  operator-disk or operator-gated → local · Q3 read-only fan-out → cloud · Q4 else → codespace,
  with concurrency ceilings (local: one writer per checkout, parallel only across worktrees;
  codespace: 2–4; cloud: effectively unlimited; **batch ceiling 4–6 regardless**).
- **Must — Layer 3:** `dispatch` becomes a real **router** — reads the contract's Substrate field
  and delegates, **refusing** when the field is missing or names a substrate with no live verb.
- **Should:** verbs stay named by **substrate** (ruling 3); version-named verbs remain aliases.
- **Should:** two one-line doc debts the measurement surfaced — the 2026-08-20 session-creation
  amendment that never landed, and the session-id prefix trap documented hub-side.

## Acceptance criteria (ex-ante)

1. A contract declaring cloud **plus** a gate in its Done-when is **refused**, with the reason named.
2. A doc naming a command absent from the operator's machine turns the drift check **RED**, proven
   by a fire-test that plants one.
3. `dispatch` routes a contract to each of the three substrates from the Substrate field alone, and
   **refuses** a missing or unbacked field.
4. **Q4 of the decision tree is not priced as available until the Codespaces chain is proven** —
   the close packet's §11 smoke run reached neither `Ok=True` nor `RemoteExitCode=0`, and this
   batch contains **no successful devcontainer execution at all**.
5. The zero-questions acceptance test passes with a reader who has not seen this fleet.

## Non-goals

- Re-litigating acts 2 and 3 — **done**, recorded above.
- The win-tooling half (the table-shape reconcile, the wrappers, the terminal profiles). That repo
  is **operator-owned**; this intake does not schedule work in it.
- Changing how the operator receives contracts. The Downloads flow stays; the gate moves to the
  point of use.

## Impact sketch (4+1 lite)

- **Logical:** substrate becomes a declared, validated property of a contract instead of an
  operator habit.
- **Process:** one act, one documented command; every other site a pointer.
- **Development:** one validator, one drift check, one router — each small, each refusing.
- **Physical:** three substrates, one interface.

## Open questions

1. Where does the substrate registry live so both the validator and the router read one source —
   `ecosystem/`, or beside the contract generator?
2. The drift organ runs `Get-Command` on the operator's machine, so it is **machine-dependent by
   design**. How should it behave in CI or a container, where the answer is legitimately different
   — `info`, or scoped out? (It must not report green-by-skip.)
3. Does making `dispatch` a router belong in win-tooling (where the verb lives) while the contract
   schema lives in the hub — and if so, what carries the schema across?

## Status

READY — filed 2026-08-26 by the endgame governance session. Acts 2–3 recorded **done** (Lane RL).
Evidence: `docs/audits/2026-08-25-technical-dispatch-surface-measured.md` (L1),
`…-technical-dispatch-consolidation-plan.md` (L2),
`…-technical-dispatch-codespace-build.md` (L3),
`…-technical-research-operator-dispatch-playbook.md` (L6), and
`docs/audits/2026-08-26-verification-batch-1-close-packet.md` §11.
