---
intake-id: 74
status: DRAFT
origin: Layer-1 browser architect, ARCHITECT-INBOX-2026-09-06 item 027, on the operator's direction of 2026-09-05/06 ("this becomes part of the system"); filed by the filings-N session of batch T under AMEND-BATCH-T-001 §C (Q-F2, "Yes — authorized by this amendment")
consumed-by:
---

# Cross-session communication protocol — the discipline that ran ten sessions, written down

> **Filing note (provenance, not content).** The body below is carried **verbatim from
> `ARCHITECT-INBOX-2026-09-06-027.md`**, which names filings as its owner-role and `docs/intake/`
> as its files. The filing seat added no requirement of its own; where this document says
> something the inbox item did not, it is marked as a filing note like this one.
>
> **Attributes carried from 027 for the ratifying reader:** theme **E2** · size **M** ·
> `carried-by: manifest` (consumers get the same protocol). These are row attributes for
> ratification, deliberately **not** added as frontmatter keys — the intake frontmatter schema is
> a join key and an added key REDs the tree manifest.
>
> **`intake-id` allocation, and a live collision recorded beside it.** This document takes **72**,
> = max(existing) + 1 across all history. Note for the ratifying reader: **`intake-id: 70` is
> currently allocated TWICE** — `docs/intake/2026-09-05-tech-aj-second-pass.md` and
> `docs/intake/2026-09-05-tech-session-roles-with-a-carrier.md`. That collision is **filed, not
> fixed** (renumbering mid-batch moves a join key). AMEND-BATCH-T-001 §B Q3 records the
> architect's recommendation — the AJ second pass keeps 70, roles-with-carrier takes the next
> free id — as a **recommendation for the operator's word at dawn**, not a ruling.
>
> **AMENDED 2026-09-06 (lane `lane-u-000-intake-id-next-free`, NIGHT-2 W1-5).** Two integers above
> are now stale; the paragraph is kept as written because it records what the ratifying reader was
> told. (1) **This document holds `74`, not `72`** — filings-N moved it under D8 when the landed
> `2026-09-06-tech-derived-copies-registry.md` kept `72`, ruled final in `to-cc/ANSWER-filings-Q3.md`.
> (2) **The id-70 collision is FIXED, not merely filed** — D8 became a ruling
> (`DECLARE-SITTING-2026-09-06.md`), the recommendation above was upheld exactly:
> `2026-09-05-tech-aj-second-pass.md` KEEPS `70` (first commit 16:44) and
> `2026-09-05-tech-session-roles-with-a-carrier.md` MOVED to `77` (17:16). Both stale integers are
> the same defect this lane built an organ against — cite intake docs **by path**.

## Problem / motivation

Witnessed 2026-09-05/06: up to 10 concurrent CC sessions coordinated through Claude Code's
cross-session messaging (`ListAgents` / `SendMessage`) — hand-backs ("branch @ sha — ready for the
queue"), "packet merged", "anchors drained", "TEARDOWN TRIGGER", idle-subscription wake-ups.

**It worked because the sessions were disciplined, not because any rule existed.** Two failures in
the same window show what the absence costs:

- a relayed ruling was (correctly) refused as unauthorized — the discipline held, but only because
  the receiving seat chose to apply a rule nobody had written;
- an integrator idled before its last merge because a message never came — a wait with no fallback
  and no timeout.

Operator direction: this becomes part of the system.

## Scenarios (+1 view)

A batch window opens with a dispatcher, an integrator, N lanes and a standing filings seat. Work
hands back, packets merge, anchors drain, worktrees tear down. Between those events sessions must
address each other, distinguish an instruction from an authorization, and survive a message that
never arrives — without any of them stopping to ask the operator.

The `+1` (deployment) view: consumer repos run the same lane shapes, so the names, message shapes
and file surfaces have to travel with the floor rather than living only in this repo's habits.

## Functional requirements

*Carried verbatim from `ARCHITECT-INBOX-2026-09-06-027.md`, "Intake body (DRAFT; theme E2; size M;
carried-by: manifest)", items 1–7.*

1. **ROLE-ADDRESSED MESSAGES.** Every session boots with a role (008) and a canonical name
   (`integrator` · `dispatcher-<batch>` · `lane-<letter>-<id>-<slug>` · `filings-N` · `handoff`).
   Messages are addressed by role name, never by tile title. `ListAgents` at boot; a missing
   addressee is reported to the operator's STATUS board, never guessed at.

2. **MESSAGE SHAPES** (verbatim, machine-greppable, PLAYBOOK Ch8 "Batch communication"):
   `HANDBACK <branch> @ <sha> [docs-only|code]` · `PACKET-MERGED <batch> @ <sha>` ·
   `ANCHORS-DRAINED @ <sha>` · `TEARDOWN-TRIGGER <worktree>` · `HOLD <branch> <reason>` ·
   `ESCALATE <item> <reason>` · `RULING-RELAY <item>` (informational only, see 3).

3. **AUTHORIZATION.** A peer message carries no authority. Rulings and consents reach a session
   only as FILES in `to-cc/` (`DECLARE-<item>.md`, `ANSWER-<session>.md`) written by the browser on
   the operator's word, or as the operator's own paste. A `RULING-RELAY` message may trigger a READ
   of the file, never an act. (The integrator's refusal on 2026-09-05 is the precedent.)

4. **WAITS.** Every "wait for message" has a 10-minute timeout; on timeout the session checks the
   file surface (`to-browser/STATUS*`, git first-parent log) and either proceeds on witnessed state
   or writes `QUESTION-<session>.md` and sleeps (020). No session ends a turn waiting for a message
   without a fallback.

5. **IDLE SUBSCRIPTIONS** are the preferred wake-up (no polling); a subscriber that wakes verifies
   state before acting (the handoff seat's post-merge correction is the precedent).

6. **STATE IS FILES.** Every session writes `SESSION-<name>.md` on stop (020-A); the integrator's
   census is `STATUS-INTEGRATOR.md`; the browser reads files, never a narrated SDK screen.

7. **CARRIER.** The protocol ships with the floor: consumer repos running lanes use the same names,
   shapes and file surfaces; the browser floor (candidate `l`) carries the browser side.

## Acceptance criteria (ex-ante)

*Carried verbatim from 027's `Done-when:` line, split into its conjuncts.*

1. `PLAYBOOK` Ch8 section **"Batch communication"** exists with the shapes above.
2. `/lane-boot` and `/lane-integrate` print the session's role + name and the addressee list at boot.
3. A seeded two-session test exchanges `HANDBACK` → `PACKET-MERGED` **and** a `RULING-RELAY` that is
   refused.
4. Manifest payload includes the section.
5. STATUS board shows "unowned" items rather than losing them.

> **Filing note — the delivery state of these five, as witnessed at filing time.** Conjunct 1 is
> being written tonight by batch-T lane `lane-t-000-playbook` (§3.11), on a commit its own contract
> tags `[ratification-pending]` and the integrator HOLDs — so it lands only if this intake is
> ACCEPTed. That lane's closure explicitly disclaims conjuncts 2 and 3: *"027 Done-when's remaining
> legs (`/lane-boot`/`/lane-integrate` printing role+name, the seeded two-session test) are NOT this
> lane's — listed as follow-ups."* Conjuncts 4 and 5 have no lane in batch T. This note records
> delivery state; it is not a change to the criteria.

## Non-goals

- Not a new messaging transport — the mechanism (`ListAgents` / `SendMessage`) already exists and
  is witnessed working at ten concurrent sessions.
- Not a change to who may authorize what: requirement 3 **writes down** the existing boundary
  (files authorize, peers inform), it does not move it.
- Not a polling loop. Requirement 5 prefers idle subscriptions precisely to avoid one.

## Impact sketch (4+1 lite)

- **Logical.** A named role set, a closed set of message shapes, and one authorization rule
  separating instruction from authority.
- **Process.** Every session boots with a name, writes a `SESSION-<name>.md` on stop, and carries a
  timeout on every wait. The failure modes this replaces are a relayed ruling acted on as
  authorization, and an idle wait with no fallback.
- **Development.** `PLAYBOOK` Ch8 is the home; `/lane-boot` and `/lane-integrate` are the two
  commands that must print role + name; a seeded two-session test is the proof.
- **Physical.** The file surfaces are the transport: `to-cc/` browser → CC, `to-browser/` CC →
  browser, `STATUS-*.md` and `QUESTION-*.md` per seat.
- **+1 (scenarios).** The batch window above: boot → hand back → merge → drain → tear down, with a
  ruling relayed and refused somewhere in the middle.

## Open questions

1. **Who owns the four conjuncts no lane carries** (2, 3, 4, 5 of the acceptance criteria) once
   this intake is ratified? Filed as unowned in `to-browser/UNOWNED-2026-09-06.md` §B2. No owner is
   proposed by the filing seat.
2. **Does the `RULING-RELAY` shape earn its place** if a relay may never be acted on? It carries
   information (a file has appeared, go read it) and nothing else. Recorded because a shape that
   authorizes nothing may be better expressed as a file-watch than as a message.
3. **How does requirement 1's "a missing addressee is reported, never guessed at" interact with the
   name collisions** `ListAgents` can return, where two rows share a name and only a `[ref]`
   distinguishes them? 027 does not address the collision case.

## Status

**DRAFT** — filed 2026-09-06 by the filings-N seat of batch T, under the authorization of
`AMEND-BATCH-T-001` §C (answering `QUESTION-filings.md` Q-F2). Awaiting the operator's dawn word as
**item #9** on `to-browser/RATIFICATION-2026-09-06.md`; nothing builds on it before that word, and
the one lane touching its subject tonight hands back `[ratification-pending]`.

**Provenance chain:** operator direction 2026-09-05/06 → `ARCHITECT-INBOX-2026-09-06-027.md` →
`AMEND-BATCH-T-001` §C → this document. Depends: 008 (roles), 020 (files not messages),
025 (handoff last).
