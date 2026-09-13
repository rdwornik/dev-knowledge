# ADR-119: A command file counts as a `[#664]` wiring surface only while invocations are recorded — adoption decays, it is not conferred

- **Status:** Accepted
- **Date:** 2026-09-13
- **Decision tier:** Architecture (Path A. The operator ruled the functional question — ADR-108 §A routes functional questions to him — and routed the ruling itself through the decision engine rather than settling it in chat.)
- **Amends:** the `[#664]` orphan census's wiring-surface input list, which today reads five surfaces and admits a sixth by this decision **under a condition the other five do not carry**.
- **Related:** ADR-98 (the intake spine this arrived on), ADR-108 §A (functional questions are the operator's) and §B (RED-first), ADR-111 (the funnel: no finding becomes a row without triage), ADR-89 (the static-only oracle, whose "necessary but not sufficient" shape this decision reuses), ADR-110 (the batch protocol the affected organs serve)
- **Intake:** **#94** — `docs/intake/2026-09-13-tech-command-files-as-a-wiring-surface.md` (`ACCEPTED`), which carries the requirement, the response measure and the flip condition this ADR is judged against.
- **Source:** the ONE structural ask of `docs/audits/2026-09-13-census-x-664-delete-list.md` §5, answered by `to-browser/RATIFICATION-2026-09-13.md` item 1.
- **Decommission:** none.
- **Births:** `[#747]` — the implementing row. ADR-111 guard (i) is discharged by it: this decision requires a build (the counter read, the decay rule, the census surface), so it does not stand accepted with nothing scheduled.

## 1. Context — the census's answer is majority-wrong, by construction

The `[#664]` census answers *"what does nothing trigger?"* over five wiring surfaces:
`.pre-commit-config.yaml`, `.claude/settings.json`, the plugin `hooks.json`, the registered
scheduled task, and the CI workflows. `.claude/commands/*.md` is not among them.

So **every operator-invoked organ reads as an orphan whatever its real adoption** — 21 of the
37 disposition rows on the 2026-09-13 census (§4.3 three modules, §4.4 sixteen acts, §4.5 two
report generators). The tail grew by one *during the census lane*, when that lane wrote
`propose_row_closures.py` and had to dispose of its own new organ as untriggered.

Two properties make this worse than a miscount:

- **It misdirects repair.** `merge_receipt.py` is invoked at every integration, from four points
  of `.claude/commands/lane-integrate.md`. Reported untriggered, it invites a pre-commit hook —
  which is wrong on the merits, since a stopwatch has nothing to gate. Likewise
  `actions_verdict.py`, whose hook would query a run for a merge SHA that does not exist at
  commit time.
- **It is monotonic.** The tail grows by one every time a lane writes an operator-invoked organ,
  and nothing shrinks it.

## 2. The question, and what the operator was actually buying

**Should `.claude/commands/*.md` count as a `[#664]` wiring surface?**

The operator answered **YES**, and attached the reason the answer is not a simple admission:

> what he is buying is **not a smaller register** but the guarantee that **Claude uses the organs
> it builds**. So adoption is ADOPTION-BY-INVOCATION: a command file makes an organ *adopted*
> only while telemetry records real invocations; an organ no command has actually called in 30
> days returns to the register. This is the same counter as AX9-5.

That distinction is the whole decision. A naive YES optimises the metric and destroys the
question: it asserts adoption of 21 modules on the evidence that *somebody wrote down a way to
call them*, which is not evidence of use.

## 3. Alternatives weighed

**A — NO. Command files are not a wiring surface (status quo).**
Honest and free. Keeps a standing 21-row tail every future reader must be told to discount, keeps
"untriggered" meaning something other than what it says, and keeps growing by one per
operator-invoked organ. **Rejected:** it is the state the census itself filed as a defect in its
own input list, and it misdirects repair (§1).

**B — YES, unconditional. A command file naming an organ marks it adopted.**
Removes the tail in one edit; requires no telemetry. **Rejected, and it is the dangerous option
precisely because it is the cheap one.** It converts an honest 21-row tail into 21 false
negatives: a module named by a command nobody runs reads green forever, and the register has been
taught to lie in the direction that stops anyone looking. The census's own cautionary witness —
`desired_state_loader.py`, deleted on a SAFE oracle verdict, suite RED, restored whole — is the
same shape: a static signal treated as sufficient.

**C — YES with adoption-by-invocation. A command file confers adoption only while telemetry
records real invocations; 30 days without one returns the organ to the register.** **ACCEPTED.**
It answers the question the register is actually asked, it makes adoption decay rather than
accrue, and it reuses a counter already proposed for a neighbouring question (AX9-5: raw-search
calls versus organ calls per session). Its cost is real and is stated at §5: it needs
cross-session per-organ telemetry, which does not exist yet.

**D — Widen the list but keep a separate declared "operator-invoked" tier, not counted as
triggered.** Cheap, honest, and strictly better than A: the 21 rows stop reading as *nothing can
invoke this* and start reading as *an operator invokes this*, with no telemetry required.
**Rejected as the primary, retained as the fallback** — it records the shape of adoption without
ever measuring it, so it cannot answer the operator's actual question. Intake #94's soft flip
routes here if C's telemetry proves unbuildable at proportionate cost.

## 4. Decision

1. **`.claude/commands/*.md` is admitted as a sixth wiring surface** to the `[#664]` census.
2. **It is a CONDITIONAL surface, and the only one.** The other five confer *triggered*
   unconditionally, because an event fires them. A command file confers **adopted** only while
   telemetry records at least one real invocation of the named organ within a rolling **30-day**
   window.
3. **Adoption decays.** An organ whose window closes with no recorded invocation **returns to the
   register**, and the return is reported as a return — with the date of its last recorded
   invocation — not as a new finding.
4. **The register keeps two distinct states.** *Nothing can invoke this* (no surface names it) and
   *nothing has invoked this lately* (a command names it; the counter is cold) are different
   conditions with different repairs, and the census must not collapse them.
5. **One counter, not two.** The invocation reading is AX9-5's counter — organ calls per session —
   read for this question. No second telemetry path is commissioned.
6. **This decision does not authorise adding hooks to lower a count.** For `merge_receipt`,
   `actions_verdict` and `review_packet` a hook is wrong on the merits (§1); the census's §4.3
   reasoning stands.
7. **Skills are out of scope.** `[#664]`'s anti-pattern list already rules that repair — *a
   skill's mandate becomes a HOOK, never a graph row*.

## 5. Consequences, including the ones that cost

- **~21 rows leave the untriggered register** and enter an adopted-by-invocation tier that names
  its evidence. Register *size* is explicitly not the success measure; composition is (intake #94,
  acceptance criterion 2).
- **The telemetry is the dependency, and it is not free.** Per-organ invocation with a timestamp
  must persist **across sessions** — a 30-day window cannot be answered from one transcript. Where
  it lives, and whether it survives a worktree teardown, is intake #94's open question, sharpened
  by the nine husk directories batch X4 found in `.claude/worktrees/`.
- **A decay rule that never fires is an untested branch.** At least one observed return is
  required before this is called done.
- **`[#675]`'s three modules stop reading as unadopted** once the counter is live — but not
  before. Until then the census's reading of them is unchanged, and lane
  `lane-x-675-instrument-fixes` is explicitly forbidden from wiring a hook to change it.
- **Two report generators (`gen_ledger.py`, `propose_row_closures.py`) resolve without a further
  decision**, which is what the census predicted a YES would do.

## 6. How this will be judged, and what would reverse it

Both are specified ex-ante in intake #94 and are repeated here because an ADR that cannot be
falsified is a preference.

**Response measure.** The primary reading is the invocation counter per organ per window; a
register reporting adoption while that counter reads zero for the same organ is a failed build.
Secondary: register *composition*, and at least one observed return with its last-invocation date.
A RED-first witness per ADR-108 §B: an organ named by a command file with no recorded invocation
in the window reads UNTRIGGERED, and the test is RED before the decay rule exists.

**Flip condition.** Revert to alternative A if, over **two consecutive 30-day windows**, organs
marked adopted-by-command show **zero recorded invocations and do not return to the register**.
That is the signature of telemetry not measuring real invocation, under which the admission
launders orphans — strictly worse than the tail it replaced, because the tail was honest.
**Soft flip:** if attribution cannot be obtained without hand-instrumenting every call site, fall
back to alternative D — a declared on-demand tier, no worse than today and considerably cheaper.

## Flip-condition

> **If, over TWO CONSECUTIVE 30-DAY WINDOWS, organs marked adopted-by-command show ZERO recorded
> invocations AND do not return to the register, this decision reverts to alternative A — command
> files are not a wiring surface.**

That is the signature of telemetry that is not measuring real invocation. Under it the admission is
**laundering orphans** rather than counting adoption, which is strictly worse than the 21-row tail it
replaced, because the tail was at least honest. Both legs are required: zero invocations alone is a
healthy decay signal, and it is the *failure to return* that says the decay rule is not running.

**Soft flip, to alternative D rather than to A.** If per-organ invocation cannot be attributed
without hand-instrumenting every call site, the cost has exceeded the defect: fall back to a
**declared on-demand tier** — the 21 rows stop reading as *nothing can invoke this* and start reading
as *an operator invokes this*, with no telemetry at all. Honest, cheap, and no worse than today.

**Either flip is a recorded act, not a quiet abandonment.** The measure that would trigger it is
intake #94's, written ex-ante, and `[#747]` carries both conditions in its own body so the row cannot
be closed by a build that satisfies neither.

## 7. Why this went through the engine rather than into a row

The operator could have answered YES in one word and had a lane execute it. He routed it through
`[#692]` instead, and the reason generalises: **this is a decision about what a measurement
means**, and a measurement changed by a row is a measurement nobody can audit later. The engine's
sequence — intake, alternatives, response measure, flip condition, ADR — is what makes the
alternative B failure mode visible *before* it is implemented rather than after 21 rows have gone
quiet.

It also keeps the decision out of the hands of the seats it affects. Three of batch X4's four
lanes touch modules whose orphan status this answer changes; a lane that could move its own census
reading is the wrong seat to decide what the census counts.
