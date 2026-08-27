---
intake-id: 60
status: READY
origin: architect ruling X8 taken 2026-08-27 over the 2026-08-26 night batch; the night-harvest consumption ledger section B (I-NIGHT). Mechanics measured in that night's own harvest rather than designed
consumers: `docs/audits/2026-08-27-technical-night-harvest-manifest.md` (the landed manifest, this intake's evidence and the shape's first instance); `docs/audits/2026-08-27-technical-night-harvest-consumption-ledger.md`; `protocols/PLAYBOOK.md` as the protocol's home; the `Dispatch-After` and `Harvest-Cloud` verbs in win-tooling; STANDING_RULINGS section X8
---

# The night batch is a working protocol that exists only as habit — name it

## Problem / motivation

The 2026-08-26 night ran four cloud sessions unattended, and every one of them delivered. The
mechanics worked: dispatch four read-only briefs, sleep, wake, harvest each session's report from
the Anthropic cloud API, write a manifest, adjudicate in the morning. Nothing was lost, and the
harvest was **read-only** — nothing was written to any repo by the cloud sessions themselves.

**But none of that is written down anywhere as a protocol.** It exists as an operator habit and as
the residue in one night's files. The consequences are already visible in that same night:

- The harvest verb has no name. It was performed by hand against
  `GET /v1/code/sessions/{id}/events`, paginated by `next_cursor` — mechanics that were
  **rediscovered**, not looked up.
- The dispatch-and-return verb has no name either. `Dispatch` exists as the operator's sole
  dispatch verb (register section V); the *deferred* form — dispatch now, collect later — does not.
- The manifest shape that made the harvest auditable (per-report file, byte count, first heading,
  top recommendation, a PENDING section, and a Verification section that records deviations rather
  than hiding them) was invented that night and will be reinvented the next.
- Two sessions' reports opened with a line of prose before the report heading, violating the
  "starts with its own heading" expectation. The **right** call was made — land verbatim, record
  the deviation in Verification — but that call was a judgement, not a rule.

**Ruling X8: the night protocol is doctrine** — dispatch, sentinel, harvest, manifest, morning
adjudication — and belongs in PLAYBOOK as a named protocol with its two missing verbs.

## Scenarios (+1 view)

- As the operator I want to spend the night's compute without spending the night. I dispatch N
  read-only briefs before bed and adjudicate a single packet in the morning. Today I can only do
  that by remembering how I did it last time.
- As the executor woken to harvest, I need to know: which assistant text **is** the report? Last
  night the answer was "the longest one, which was #2, immediately after the RECEIPT" — and the
  **last** text was Stop-hook backpressure noise from a container where `uv run --locked` could not
  start (uv 0.8.17 against the pinned 0.11.19). Taking the last text would have harvested garbage.
  That is a trap the protocol should disarm, not a lesson each seat relearns.
- As the morning adjudicator I need one file that tells me what came back, what did not, and what
  deviated — before I open four reports. The manifest is that file, and it is the artifact that
  makes an unattended night auditable.
- As a lost seat or a lost chat, I need the night's findings to survive me. A consumption ledger
  that lists every finding with its verdict and destination is the durability mechanism; the
  protocol should require one.

## Functional requirements

- **Must:** the five-phase protocol — **dispatch → sentinel → harvest → manifest → morning
  adjudication** — is named in `protocols/PLAYBOOK.md` with each phase's inputs, outputs and
  refusal conditions.
- **Must:** the **manifest shape** is specified: one block per dispatched session carrying file,
  byte count, first heading, and top recommendation; an explicit **PENDING** section (empty is a
  statement, not an omission); and a **Verification** section that records deviations verbatim
  rather than trimming the artifact to make a check pass.
- **Must:** the harvest is **read-only** and lands artifacts **byte-identical**. A cloud session's
  report is evidence; trimming it to fit a convention destroys the evidence and hides the
  deviation.
- **Must:** the report-selection rule is stated with its measured trap — the report is not
  reliably the last assistant text, because Stop-hook backpressure noise can follow it.
- **Should:** two verbs land in win-tooling (operator-owned): **`Dispatch-After`** — the deferred
  form of the existing `Dispatch` verb — and **`Harvest-Cloud`**, wrapping
  `GET /v1/code/sessions/{id}/events` with `next_cursor` pagination.
- **Should:** every night produces a **consumption ledger** — every finding, its verdict, and its
  destination, including rejected items with their reason — so the night survives the loss of the
  chat or seat that ran it.
- **Could:** a sentinel that reports which sessions are complete at wake time, so a second sleep is
  taken only when one is actually needed. Last night none was.

## Acceptance criteria (ex-ante)

1. `protocols/PLAYBOOK.md` carries a named night-batch protocol section enumerating all five
   phases, each with its inputs, outputs and refusal conditions.
2. The manifest shape is specified precisely enough that two different seats produce the same
   sections, and the 2026-08-27 landed manifest validates against it as the reference instance.
3. `Dispatch-After` and `Harvest-Cloud` exist as named win-tooling verbs, each with a usage line
   and its API surface recorded; `Dispatch-After` is documented as a **form of** the ruled
   `Dispatch` verb, not a rival to it.
4. The protocol states the byte-identical landing rule and the record-the-deviation rule, and the
   two C-reports that opened with prose are cited as the worked example.
5. The report-selection rule names the Stop-hook-noise trap explicitly.
6. A ledger is a **required** output of the protocol, not an optional one.

## Non-goals

- **Not a new dispatch verb.** Register section V rules `Dispatch` as the sole operator dispatch
  verb; `Dispatch-After` is its deferred form and must be documented as such or it reopens a
  settled ruling.
- Not a scheduler, a cron organ, or an autonomous night agent. The protocol describes an
  operator-initiated night, and the adjudication stays a morning human act.
- Not a change to what cloud sessions may **do**: they stay read-only, and nothing in this intake
  authorises a cloud session to write to a repo.
- Not a hub script. The two verbs are **win-tooling, operator-owned** — a hub script that drives
  state elsewhere would breach the Layer-2 invariant.
- Not a fix for the container's uv mismatch (0.8.17 vs the pinned 0.11.19). That is a real defect,
  it is named here as the source of the noise, and it belongs to the substrate axis.

## Impact sketch (4+1 lite)

- **Logical:** a named protocol with five phases and two verbs; no new enforcement organ.
- **Process:** the largest change — an unattended night becomes repeatable by a seat that was not
  there for the last one, and its output becomes a single adjudicable packet.
- **Development:** doc work in PLAYBOOK plus two win-tooling verbs; nothing in the hub's gate set.
- **Physical:** the cloud substrate, already in use and already ruled; no new dependency beyond the
  API surface the harvest already exercised.

## Open questions

- Where exactly in PLAYBOOK does this live — Ch8 "Session boundaries" beside the lane/batch
  protocol, or its own chapter? It is a session-boundary protocol by shape, which argues for Ch8.
- Should the ledger be a `docs/audits/` artifact by convention (as this night's is), or a handoff
  bundle? It is adjudicated once and then cited, which argues for audits.
- Is the sentinel worth building at all, given last night needed no second sleep? One clean night
  is n=1; the protocol can name the phase without mandating the organ.
- Does an unattended night need a stop-condition vocabulary of its own, or does the existing
  refusal grammar cover it?

## Status

READY — filed 2026-08-27 from the night-harvest consumption ledger section B. Ruling X8 (the night
protocol is doctrine) already taken; the mechanics are measured, not designed. First act is the
PLAYBOOK protocol section.
