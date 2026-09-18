---
intake-id: 104
status: DRAFT
origin: operator night order, 2026-09-17 — `to-cc/AMEND-NIGHT-ORDER-CONSOLIDATED-2026-09-17.md` §9, filed by the primary CC session at step S5
consumed-by:
---

# What makes a seat use the organs

## Problem / motivation

We build a harness for using LLMs and do not use what we built. Nothing forces it today.
Library-first, use the organs, do not raw-scan — all of it is PROSE in `protocols/PLAYBOOK.md`,
and prose is a request, not a guarantee.

The sharper finding behind this intake is about the SHAPE of what we have built, not its
quantity: **all 34 mechanisms built so far are REFUSALS, and not one is an AFFORDANCE.** The two
have opposite failure economics. A refusal must be ~100% reliable to be worth anything, and when
it fails it takes the system down — the 2026-09-16/17 hook wedge cost a lost night, roughly six
wedged integrator hours and about 17 starved agent-hours. An affordance costs NOTHING when it
fails: the agent simply does what it would have done anyway. We built 34 of the expensive kind and
zero of the free kind.

Two live facts make the question urgent rather than theoretical, both measured at this intake's
filing:

1. **The one organ-steering refusal we have can be defeated by a pipe.** `deny_and_point` splits
   its command line on `|`, `&&`, `||` and `;`, and its sanctioned `# raw-needed: <reason>` escape
   lands only in the LAST segment. Re-derived first-hand on 2026-09-17: the bare governed search
   was DENIED; the same search with the escape appended was ALLOWED; the same search with the
   escape appended *behind a pipe* was DENIED again. A seat that pipes to `head` cannot declare its
   way out, and a seat that learns this learns to avoid the guard rather than to call the organ.
2. **A gate can go green on its own test while never reaching the case it exists for.** Measured
   the same day: `decision_coverage` RUNS and REFUSES (exit 1, six uncovered decisions — including
   the night order that commissioned this intake), but its trigger is `stages: [manual]`, so it
   never fires at a local commit; it runs only in conductor job `commit-gate`, whose required-check
   ruleset ships `enforcement: disabled`. The organ works. Nothing reads its verdict.

If this stays unaddressed, the corpus keeps growing mechanisms whose reach nobody measures, and
the ratio that actually matters — organ calls versus raw scans — stays unknown.

## Scenarios (+1 view)

- As a lane seat under time pressure, I need to know which tests cover a file I changed. I type
  `grep -rn` because it is one keystroke and I do not remember that `impacted_tests.py select`
  exists. Nothing tells me, and the answer I get is worse.
- As a lane seat, I hit a refusal I do not understand, so I append `| head -20` to shorten the
  output. The refusal fires again for a reason that now looks arbitrary. I work around the guard.
- As the architect seat, I freeze a lane to solve a problem that already has a P1 row, because the
  row was not in my briefing and the corpus is 368 open rows. Nobody can hold that in their head,
  and the browser seat carries no telemetry at all — so this failure does not even appear in the
  count that would reveal it.
- As the operator, I ask how often the organs are actually used and no surface can answer.

## Functional requirements

- **Must:** the answer reaches MOST calls, not a measured margin · its escape SURVIVES A PIPE · it
  CANNOT HANG (the 2026-09-16/17 wedge is the precedent) · it carries a COUNTER, so its reach and
  its catch rate are readable rather than asserted.
- **Should:** cost nothing when it fails — an affordance's failure mode is the seat doing what it
  would have done anyway.
- **Could:** extend to the browser seat, which today carries no telemetry and is therefore invisible
  to any count of organ usage.

## Acceptance criteria (ex-ante)

1. The organ-call-versus-raw-scan ratio is READABLE from a surface, per session, without anyone
   asking. Phase-1 evidence is the C1a number from batch AC.
2. Whatever mechanism is chosen carries a counter reporting what it caught, at what cost, over what
   window. **A gate with no catch in its window is REMOVED, not tuned.**
3. The escape path, if the mechanism has one, is proven to survive a pipe — by a test that fails if
   the segment-splitting defect returns.
4. The mechanism cannot wedge a session: a bounded execution time with a loud in-band record, or no
   blocking path at all.

## Non-goals

- **This intake does NOT rebuild `deny_and_point` as it was.** Restoring the previous shape is
  explicitly out of scope; it is one candidate among four and must earn its place.
- Building a telemetry EMITTER is out of scope for phase 1 — that would be a new organ, and the
  standing rule is no new organ until the counting is done from what exists.
- Nothing is BUILT from this intake in batch AC. This is a filing, not a lane.

## Impact sketch (4+1 lite)

- **Logical:** introduces the affordance/refusal distinction as a first-class design axis; today
  every mechanism sits on one side of it by default rather than by choice.
- **Process:** changes what a lane contract must carry — the `organs:` field naming the organ the
  lane must use is candidate (c) and is already in force for batch AC's seven contracts.
- **Development:** touches the PreToolUse hook surface, the permission-rule surface, the lane
  contract generator, and whatever carries the counter.
- **Physical:** none beyond the existing hook execution path — and a bound on it, since an unbounded
  hook is what wedged seven sessions.

## Open questions

Four options, recorded as options. **None is pre-decided, and the funnel decides — not this
document.**

- **(a)** A `PreToolUse` refusal with a sound escape. Must answer: how does the escape survive a
  pipe, and what bounds its execution time?
- **(b)** A permission `deny` rule. Must answer: `allow` and `ask` are INERT under
  `bypassPermissions`, which every lane uses — does `deny` reach the same calls?
- **(c)** The lane contract NAMING the organ. Must answer: what makes a seat read the field?
- **(d)** Measurement plus a counter, with NO refusal at all. Must answer: does visibility alone
  change behaviour, and over what window would we know?

**The standing default is (c) + (d).** (a) and (b) are refusals and must earn their place AGAINST A
COUNTER — the counter rule applied BEFORE the build rather than after. That default is itself
reviewable; it is recorded here so a later seat does not rediscover the reasoning.

Also open, and deliberately not answered here:
- Where does a per-session counter live, given that no telemetry emitter exists and building one is
  a non-goal for phase 1?
- The browser seat carries no telemetry. Is bringing it into the count part of this initiative or a
  separate one?
- Does the pipe-defeat get fixed regardless of which option wins, or only if (a) is chosen?

## Status

DRAFT — filed 2026-09-17 by the primary CC session at night-order §10 step S5. **NOTHING IS BUILT
FROM THIS TONIGHT.** This is the funnel the five owed intakes never went through: intake → ADR →
row → lane → merge → closure. An intake that never becomes a row is what produced 20 findings with
no owner.
