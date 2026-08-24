---
intake-id: 43
status: READY
origin: integrator, 2026-08-24 batch close; measured by cloud lane C2 (docs/audits/2026-08-23-technical-ruling-provenance-audit.md)
---

# Rulings are made and then land nowhere — the register stopped absorbing on 2026-08-15

## Problem / motivation

`protocols/STANDING_RULINGS.md` is the designated register of standing rulings. Lane C2
audited ruling provenance across the corpus and measured that it has **stopped functioning as
one**:

- **24 of 39 ruling sets are absent from the register.**
- **4 ruling sets landed nowhere in the repo at all** — C2's rows 17, 20, 21 and 39. Their
  source of record is off-repo (e.g. `MORNING-ADJUDICATION-2026-08-15.md`), so the repo cannot
  answer what was ruled.
- **Zero register entries carry the dates 2026-08-15, 2026-08-17, 2026-08-18, 2026-08-21 or
  2026-08-23.** The absorption stopped on 2026-08-15 and has not resumed.

There is a second, independent measurement that makes this expensive rather than merely untidy.
Lane C3 measured that **38 open backlog rows — 18% of the whole open set — carry a Done-when
whose only branch is *"…or `STANDING_RULINGS.md` carries a section naming `[#nnn]`"*.** Those
rows are waiting on a mechanism that stopped running two weeks ago. Two lanes measured opposite
ends of the same break without either being able to see the other.

One contributing cause has already been removed. Until 2026-08-24 the silent-rule ratchet
counted `STANDING_RULINGS.md` in scope, so **writing a ruling down where it could be found
raised the metric** — the register was penalised for doing its job, against a baseline with zero
headroom. RULING R12 excluded it (`scripts/silent_rule_detector.py`, detector `silent-rule-v5`).
**That removes a disincentive; it does not create a mechanism.** Nothing yet forces a ruling
into the register, which is what this intake is about.

## Scenarios (+1 view)

- The architect rules ten items in a morning adjudication. Four are cited somewhere in-repo, six
  are not. Six weeks later nobody can say what was ruled, and the only record is a file outside
  the repository.
- An executor's row says it closes when the register names its `[#nnn]`. The register has not
  absorbed anything since 2026-08-15, so the row cannot close no matter what the executor does.
- A wave closes. Its rulings live in the wave's own audit artifact, which is immutable and
  correct — but nothing walks those artifacts into the register, so the register drifts further
  behind with every wave that closes cleanly.

## Functional requirements

- **Must:** a ruling made in a window is present in the register, or its absence is refused
  visibly at a boundary the window cannot cross silently.
- **Must:** the mechanism works for rulings whose source of record is off-repo — the four
  landed-nowhere sets are precisely that case.
- **Should:** the backlog's 38 register-dependent Done-whens become dischargeable again.
- **Could:** a back-fill pass over C2's 24 absent sets, sequenced after the mechanism exists.

## Acceptance criteria (ex-ante)

1. A wave/batch cannot close with an unabsorbed ruling without that being **stated** — either a
   gate refuses, or a required close-step produces a listed exception.
2. Re-running C2's provenance method after the mechanism is live yields a **smaller** absent
   count, and the number is reported rather than asserted.
3. At least one of C2's four landed-nowhere sets is either in the register or explicitly
   dispositioned as unrecoverable, with the reason recorded.

## Non-goals

- Changing what a standing ruling **is**, or the register's format.
- Back-filling all 24 absent sets as part of this decision. The mechanism comes first;
  back-fill is a separate sized act.

## Impact sketch (4+1 lite)

- **Logical:** the register is the repo's memory of decisions; a register two weeks stale is
  worse than none, because rows are written against it as if it were live.
- **Process:** adds an obligation at wave close, wherever the fork lands.
- **Development:** either a hook/check, or a named seat in the close checklist.
- **Physical:** `protocols/STANDING_RULINGS.md`, plus whatever organ enforces it.

## Open questions

- **Fork: a hook that forces a ruling into the register, or a transcription seat as a required
  wave-close step.** A hook is checkable but cannot detect a ruling made off-repo — it can only
  refuse a close that fails to *assert* absorption. A seat catches the off-repo case but is a
  human step with no teeth. A pairing (seat performs, hook asserts the assertion exists) is the
  obvious third option and is not costed here.
- Is an off-repo adjudication file a legitimate source of record at all, or must a ruling be
  in-repo to be standing? C2's rows 17/20/21/39 make this concrete.
- Should the 38 register-dependent Done-whens be re-written to a dischargeable predicate
  instead, independent of how this resolves?

## Status

READY — filed by the integrator at the 2026-08-24 batch close. Fork named, no row banked.
