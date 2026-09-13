---
intake-id: 94
status: ACCEPTED
origin: operator ratification, 2026-09-13, item 1 of `to-browser/RATIFICATION-2026-09-13.md` — answering the ONE structural ask of `docs/audits/2026-09-13-census-x-664-delete-list.md` §5
decided-by: operator ratification 2026-09-13 item 1
disposition: active
consumers: ADR-119, `[#664]`, `[#692]`
---

# Whether a command file counts as adoption, and what adoption is allowed to mean

## Problem / motivation

The `[#664]` orphan census answers the question *"what does nothing trigger?"* by reading five
wiring surfaces: `.pre-commit-config.yaml`, `.claude/settings.json`, the plugin `hooks.json`, the
registered scheduled task, and the CI workflows. A file under `.claude/commands/` is none of
them.

The consequence is not a rounding error. **Every operator-invoked organ in this repo reads as an
orphan by construction, whatever its real adoption.** On the 2026-09-13 census that is 21 of 37
disposition rows — §4.3 (three modules wired at four points of `lane-integrate`), §4.4 (sixteen
on-demand-by-operator acts), §4.5 (two operator-transport report generators) — a clear majority of
the register. The tail is not static either: it **grew by one during the census lane itself**,
when that lane wrote `propose_row_closures.py`, an operator-invoked organ, and had to dispose of
it as untriggered in the same act that created it.

So the register carries a standing majority that every future reader must be told to discount,
and the word "untriggered" does not mean what a reader would take it to mean. That is a defect in
the census's input list rather than a property of any module on it.

**But the naive repair buys the wrong thing.** Simply adding `.claude/commands/*.md` to the
surface list makes 21 rows disappear and asserts, of each, that it is adopted — when what a
command file actually proves is that *someone wrote down a way to call it*. A module named by a
command nobody runs is exactly as dead as a module named by nothing, and the register would have
been taught to say otherwise. The operator's framing at ratification is the load-bearing one:
what he is buying is **not a smaller register** but **the guarantee that Claude uses the organs it
builds**.

## Scenarios (+1 view)

- **As the census, today.** `scripts/merge_receipt.py` is wired at four points of
  `.claude/commands/lane-integrate.md` and is invoked at every integration. The census reports it
  untriggered. A reader repairing orphans reaches for a pre-commit hook — which is wrong on the
  merits, because a stopwatch has nothing to gate — and the census has actively misled them.
- **As the census, under a naive YES.** A lane writes `scripts/gen_ledger.py`, names it in a new
  command file, and never calls it again. The register reports it adopted, forever. The organ
  rots with a green light on it, which is worse than the tail it replaced.
- **As the operator, six months on.** He asks which organs the sessions actually use. Under
  today's rule the register cannot tell him — it counts mentions of hooks. Under a naive YES it
  tells him confidently and wrongly. He wants the question answered by **what ran**.
- **As a session, mid-task.** It reaches for `grep` where an organ exists. The `[#727]` guard
  already deny-and-points at that moment, and AX9-5 already proposes the counter — raw-search
  calls versus organ calls per session. **Adoption-by-invocation is the same counter**, read for a
  different question, which is why the operator tied the two together rather than commissioning a
  second instrument.

## Functional requirements

- **Must:** a command file may mark an organ adopted **only while real invocations are recorded**.
  Adoption decays: an organ no command has actually called within 30 days returns to the register.
- **Must:** adoption be readable as a **count of invocations**, not as the existence of a naming
  file. The register's answer to "is this adopted" must be derived from telemetry.
- **Must:** the register keep the distinction between *nothing can invoke this* and *nothing has
  invoked this lately* — they are different states with different repairs.
- **Should:** reuse AX9-5's counter rather than build a second telemetry path.
- **Should:** the census's surface list stop being an undeclared constant that a reader must
  discover from behaviour.
- **Could:** report the returning organs as a named cohort each window, since a return is the
  mechanism working and should read that way rather than as a regression.

## Acceptance criteria (ex-ante)

**The response measure — what number says this worked.**

1. **Invocation counter, per organ, per window.** The primary measure is AX9-5's counter: organ
   calls per session, attributed to the organ invoked. Adoption is a reading off this counter and
   nothing else. A register that reports adoption while this counter reports zero for the same
   organ is a failed build, not a tuned one.
2. **Register composition, not register size.** The ~21 rows leave the untriggered register and
   enter a distinct **adopted-by-invocation** tier that names its evidence (last invocation,
   count in window). Size alone is explicitly not the measure: a smaller register achieved by
   admitting mentions is the failure this doc exists to prevent.
3. **Returns are observable.** At least one organ returning to the register on the 30-day decay
   must be visible as a return, with the date of its last recorded invocation, before this is
   called done. A decay rule that has never fired is not evidence of health; it is an untested
   branch.
4. **A RED-first witness** per ADR-108 §B: an organ named by a command file with no recorded
   invocation inside the window reads as UNTRIGGERED, and the test is RED before the decay rule
   exists.

**The flip condition — what would make us reverse this.**

Reverse to the status quo (command files are not a wiring surface) if, over **two consecutive
30-day windows**, organs marked adopted-by-command show **zero recorded invocations and do not
return to the register**. That is the signature of telemetry that is not measuring real
invocation, and under it the admission is laundering orphans rather than counting adoption —
which is strictly worse than the 21-row tail, because the tail was at least honest.

A second, softer flip: if the invocation telemetry cannot be made to attribute a call to an organ
without instrumenting every call site by hand, the cost has exceeded the defect and the register
should instead carry the 21 rows in a **declared** on-demand tier (alternative D in ADR-119) —
honest, cheap, and no worse than today.

## Non-goals

- **Not a general adoption metric for the repo.** This scopes to what the `[#664]` census counts
  as a wiring surface, and to organs a command file names.
- **Not a change to what the other five surfaces mean.** A pre-commit hook, a settings hook, a
  plugin hook, a scheduled task and a CI workflow stay triggers, unconditionally.
- **Not a licence to add hooks to make counts fall.** Three of the modules in question
  (`merge_receipt`, `actions_verdict`, `review_packet`) have no sensible hook, and the census's
  own §4.3 says so on the merits.
- **Not a decision about skills.** `[#664]`'s anti-pattern list already rules that repair
  separately: *a skill's mandate becomes a HOOK, never a graph row*. The two skill rows in §4.4
  are out of scope here.

## Impact sketch (4+1 lite)

- **Logical:** "triggered" splits into two predicates — *invocable by an event* and *invoked in
  fact*. The register today conflates the absence of both.
- **Process:** the orphan census stops carrying a majority tail its reader must discount; a
  returning organ becomes a routine signal rather than a new finding.
- **Development:** one new surface in the census's input list, one decay rule, and a read against
  the AX9-5 counter. The counter itself is the dependency and is not free.
- **Physical:** telemetry must persist per-organ invocation with a timestamp across sessions —
  the 30-day window cannot be answered from a single session's transcript.

## Open questions

- **What counts as "a real invocation"?** A session running the organ inside a command, plainly
  yes. A session running it directly at the CLI outside any command — does that sustain adoption
  attributed to the command file? Technical-architect question; not answered here.
- **Where does the counter live**, and does it survive a worktree teardown? The nine husks found
  during batch X4 are a warning that per-worktree state does not.
- **Is 30 days the right window** for an organ invoked once per batch close? A quarterly organ
  would decay and return on every cycle and read as noise. The operator set 30; whether it needs
  a per-organ cadence is open.
- **Does the plugin copy of a derived organ inherit its source's adoption?** `review_closures.py`
  exists twice (§4.4) and only one copy is what a command actually calls.

## Status

**ACCEPTED** — operator ratification 2026-09-13 item 1, disposition `active`. The operator's
answer is **YES with adoption-by-invocation**, and he explicitly routed the ruling through the
decision engine (`[#692]`, on `main` at `a77e3302`) rather than settling it in chat: intake →
alternatives → response measure → flip condition → ADR, with the ratification as input. That ADR
is **ADR-119**, which carries the alternatives weighed and the decision; this doc carries the
requirement and the measures it must be judged against.
