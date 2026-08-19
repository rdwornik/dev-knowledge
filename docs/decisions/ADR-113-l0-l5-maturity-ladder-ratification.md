# ADR-113: The L0–L5 maturity ladder is ratified vocabulary — and it is one of three "L" namespaces, not the only one

- **Status:** Accepted (architect ruling 2026-08-19, the L-5 rulings block delivered to the S-1 night-adjudication seat)
- **Date:** 2026-08-19
- **Decided-by:** architect ruling **2026-08-19**, item `#494` of the eight-ruling L-5 block: *"RATIFY the L0–L5 ladder via a short ADR (load-bearing vocabulary in live rulings; retirement would orphan citations including N4's own carve-out classes). Draft the mini-ADR, land it, then CLOSE."* Executed by the S-1 seat under `docs/audits/2026-08-19-technical-s1-seat-arc-contract.md` act 7. Operator GO for the arc covers the act; the ratifying decision is the architect's, transcribed here rather than re-derived.
- **Decision tier:** Architecture
- **Related:** ADR-108 (decision-routing doctrine — `[#494]`'s re-routed home), ADR-109 (fleet desired-state contract — L0's mechanical surface), ADR-98 (intake → ADR traceability)
- **Intake:** #16 §1 (the layer table this ladder *is*) — the ladder was never authored as a proposal; it was used, and this ADR ratifies the use
- **Decommission:** none
- **Source:** `[#494]`; evidence pack `docs/audits/2026-07-31-verification-382-ladder-evidence.md`, which answered all six levels from `main` at `f7abe228` with a SHA or `file:line` per level

## Context

The ladder is used descriptively across session prose, contracts and rulings, and has never been
ratified. `[#494]` filed exactly that gap and attached an operative constraint that has been
binding since it was filed: *"Until ruled, nothing cites 'L2' as authority."* The row is therefore
not a tidy-up — it is a live gag on a vocabulary the fleet keeps reaching for.

Two options existed and both were real. **Retire it:** the levels were never voted on, so deleting
them costs nothing and removes an unearned authority. **Ratify it:** the levels are already
load-bearing in live rulings, and the N4 grooming sheet's own carve-out classes cite them — so
retirement orphans citations rather than removing an authority. The architect ruled ratification,
for that reason.

The gap this ADR closes is not really "is the ladder blessed". It is that **three unrelated `L`
namespaces are live in this repo at once**, and a bare `L2` does not say which one it means.

## Decision

**1. The L0–L5 maturity ladder is ratified as fleet vocabulary**, in intake #16 §1's layer table,
with the operator's half-steps. It describes how mature a capability is; it confers no obligation
by itself.

| level | name | what it measures |
|---|---|---|
| **L0** | structure as managed state | conformance is readable mechanically, not inferred |
| **L0.5** | recurrence on `main` | the reading actually runs, and on `main` rather than one machine |
| **L1** | dependency architecture | dependencies are declared and checkable |
| **L2** | methodology versioning + deployment | the methodology is versioned and reaches consumers |
| **L3** | full lifecycle | the loop closes end to end, not once |
| **L3.5** | the reconcile loop | the report runs on a cadence *and* its output is read by someone |
| **L4** | tech-currency | the stack's currency is tracked rather than discovered |
| **L5** | predictive | the corpus is mined to anticipate rather than to report |

**2. A level is a maturity claim, never an authority.** Citing `L2` states how mature a surface is.
It does not license, oblige or forbid anything. Whatever binds is the ADR, ruling or row that
binds — the level is a description of where the work stands, and `[#494]`'s "nothing cites L2 as
authority" constraint is therefore **ratified as a permanent property of the vocabulary**, not
lifted by this ADR. What is lifted is only the prohibition on citing the ladder *at all*.

**3. The three `L` namespaces are distinct and a bare `L<n>` is ambiguous.** All three are live:

- **the maturity ladder** — `L0`…`L5`, this ADR. Written `L0`–`L5`, no hyphen before the digit.
- **the distribution layer** — `ARCHITECTURE.md`'s organ table, where `L0` means the global
  `~/.claude` user layer (fleet-wide) as opposed to `hub` or a consumer. Same token, different axis:
  *where an organ lives*, not *how mature a capability is*.
- **`STANDING_RULINGS.md` section labels** — `L-1`…`L-11` under section **L**, the 2026-08-12
  adjudication-hour rulings. Hyphenated, and a section index rather than a scale.

**A citation names its namespace when the context does not.** "maturity L2", "the L0 user layer",
"register L-5" all resolve; a bare "L2" in prose that discusses organs does not. This clause is the
part of the ADR with actual teeth, because the collision is the reason a bare level reads as an
authority in the first place — `ARCHITECTURE.md`'s `L0` genuinely *is* a placement fact, and
borrowing its definiteness for a maturity claim is the confusion `[#494]` observed.

## Consequences

- `[#494]` closes: the ladder is ratified by ADR, which is its Done-when clause 1.
- **Clause 2 of `[#494]`'s Done-when is discharged by construction, not by a sweep** — it asks that
  any surface citing a level as authority *"either resolves to that ADR or drops the citation"*.
  Decision 2 above rules that no surface cites a level as authority, because a level cannot be one.
  Every existing citation is therefore descriptive and already lawful; none needs rewriting.
- The ladder **arms no gate and creates no obligation**, and nothing here schedules work at any
  level. `docs/audits/2026-07-31-verification-382-ladder-evidence.md` records the live position
  (L1 satisfied; L0/L3 partial; L0.5/L2/L3.5/L4 not done; L5 untouched) and this ADR does not
  re-measure it — that pack is a 2026-07-31 reading and is cited as one.

## Honest limits

- **This is a transcription ADR.** The decision is the architect's ruling of 2026-08-19; nothing
  here was decided by its author. Where this file elaborates — decision 3's namespace disambiguation
  — it does so because the ambiguity is what made the vocabulary read as authority, and the
  elaboration is stated as such rather than smuggled in as if ruled.
- **Nothing checks decision 3.** The namespace rule is a convention with no validator. A checker
  would have to distinguish a maturity claim from a placement fact in prose, which is the semantic
  pass no detector in this repo claims to do.
- **The level definitions are intake #16 §1's, quoted through the [#382] evidence pack**, not
  re-derived from the intake itself. If #16 §1 and the pack ever disagree, the intake is the source.
