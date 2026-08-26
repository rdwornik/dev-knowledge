---
intake-id: 53
status: READY
origin: endgame governance session, 2026-08-26; WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII I5
consumers: HANDOFF_PROCESS (the operator-interface contract + the supplement duty); the bundle boot pointer
---

# The handoff process has no operator-interface contract — and two duties nothing carries

## Problem / motivation

Two facts were **proven absent** this window, and each cost real work:

1. **The supplement is the OUTGOING seat's duty.** Nothing said so. It was nearly skipped — the
   9th absent fact of this window's tally.
2. **The operator-interface contract is carried by nothing.** Launch pattern, bypass-always, model
   taken from the contract header: none of it is written anywhere a seat would find it. That is
   **why ~30 seats invented their own procedure** — the 10th absent fact.

The second is the more expensive, and Part VII records why: a seat **authored an operator launch
procedure** because none was findable. The rule that follows is *"zero invented procedures —
unfindable means measure and STOP, never design"*, and it can only bind if the thing being sought
actually exists to be found.

Related and already measured: **16 of 16 architect errors this window were
asserted-instead-of-measured** — now 18 of 18 with errors #18 and #19 appended to `LESSONS.md` on
2026-08-26. The consequence for this intake is structural: **bundles shrink as repo mechanisms
grow.** A contract should name the command, never restate the fact — because a restated fact rots
where a named command resolves.

## Scenarios (+1 view)

- **As an outgoing seat**, the process tells me the supplement is mine, so it does not depend on
  my noticing.
- **As an incoming seat**, one pointer in the bundle tells me how the operator launches work,
  which permissions posture applies, and where my model comes from — so I never design a
  procedure.
- **As the operator**, I stop receiving a different launch procedure from each seat.

## Functional requirements

- **Must:** `HANDOFF_PROCESS` states that **authoring the supplement is the outgoing seat's duty**,
  in a place the outgoing seat reads at the time it applies.
- **Must:** `HANDOFF_PROCESS` carries the **operator-interface contract** — the launch pattern
  (interactive/primary-checkout sessions: `claude`, then one line, *"Read `<path>` and execute it
  exactly."*; local lanes: the ruled verb over a contract), **bypass permissions always**, and
  **model/effort come from the contract header, never from the CLI default**.
- **Must:** the **bundle carries the pointer** to that contract rather than a copy of it — this is
  the shrink-as-mechanisms-grow rule applied to the mechanism that states the rule.
- **Should:** a probe that fails when the pointer does not resolve, so the bundle cannot ship
  naming a contract that has moved.
- **Could:** the same pointer discipline applied to the other facts bundles currently restate.

## Acceptance criteria (ex-ante)

1. A seat can answer *"how does the operator launch a lane, and where does my model come from?"*
   from `HANDOFF_PROCESS` **alone**, with no prior window's context.
2. The supplement duty appears in the outgoing seat's own checklist, and the close refuses without
   it — a mechanism, not an intention.
3. A bundle whose pointer does not resolve **fails a probe** rather than shipping.
4. Measured, not asserted: the next bundle is **smaller** than the current one on the same work
   class, because restated facts became pointers.
5. No seat in the next window authors a launch procedure. *(The operator judges; it is the same
   acceptance shape as I4's zero-questions test.)*

## Non-goals

- Redesigning the handoff bundle format or the v6 probe gate.
- Documenting substrate routing — that is I4's, and duplicating it here would recreate the
  four-voices defect this intake exists to prevent.
- Any change to `~/.claude/` runtime config, which is L0 and outside this repo.

## Impact sketch (4+1 lite)

- **Logical:** the operator interface becomes a named contract with one home.
- **Process:** two duties become explicit; bundles get smaller as the repo gets more mechanical.
- **Development:** a pointer-resolution probe; no new organ class.
- **Physical:** nothing.

## Open questions

1. Does the operator-interface contract belong in `HANDOFF_PROCESS`, in PLAYBOOK Ch8 (which owns
   the literal commands after I4's act 3), or in one with a pointer from the other? **Two homes is
   the defect**, so this must be answered before either is written.
2. Is "bypass permissions always" a handoff-process fact or a standing ruling that the handoff
   process merely cites? It is already ruling 4 in section V of the register.
3. What is the measurable definition of "bundles shrink" — bytes, probe count, or restated-fact
   count? Without one, criterion 4 is a vibe.

## Status

READY — filed 2026-08-26 by the endgame governance session. Evidence:
WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII I5 and Part VII, the 2026-08-26 `LESSONS.md` harvest
(ten rows plus architect errors #18 and #19), and
`docs/audits/2026-08-25-technical-dispatch-surface-measured.md` (L1) for the ~30-seat measurement.
