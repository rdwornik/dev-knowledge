# Lane packet — `lane-a-619-fm-coupling-repair` ([#619])

**Lane:** batch D, lane A · **Branch:** `worktree-lane-a-619-fm-coupling-repair`
**Contract:** `LANE-a-619-fm-coupling-repair.md` (frozen)
**Row:** `[#619]` — *"The FM-2 to FM-4 funnel-health coupling is dead — six fields, zero overlap"*
**Write-scope (frozen):** `scripts/gen_handoff.py` · `scripts/funnel_lifecycle.py` ·
`scripts/governance_health.py` · `tests/**` (this packet is the Step-1/Step-3 artifact the
contract's Steps mandate; it lands in `docs/audits/` per the ADR-101 filename enum rather than
at the repo root).

---

## 1. The starting state, witnessed rather than assumed

The contract's own witness command, run at lane boot on
`902b621b`:

```
$ python -c "import sys;sys.path.insert(0,'scripts');import gen_handoff as g;import funnel_lifecycle as f;print([a for _,a in g._FUNNEL_FIELDS]);print([x for x in dir(f.Measurement) if not x.startswith('_')])"
['intakes_consumed_unarchived', 'adrs_unexecuted', 'orphans_forward', 'orphans_backward', 'rows_closed_this_window', 'value_evidence_attached']
['archived_intakes', 'by_leg', 'detector', 'live_adrs', 'live_intakes', 'post_cutoff_rows', 'ready_intakes', 'rows', 'threshold_days', 'threshold_locator']
```

Six attributes read, ten exposed (plus `violations`, which `dir()` on the CLASS does not show
because it is a `field(default_factory=...)` and so exists only on an instance — the contract's
eleven counts it, and this lane confirms it is there on a real `Measurement`).
**Intersection: EMPTY.** Every one of FM-4's six fields renders `unavailable`, always, in every
bundle it has ever cut.

The consequence, and the row-owned RED:

```
$ uv run --locked pytest tests/test_governance_health.py tests/test_gen_handoff.py -q
FAILED tests/test_governance_health.py::test_shared_fields_equal_fm4_block_byte_for_byte
  AssertionError: intakes consumed-unarchived: resolved but rendered unavailable
1 failed, 103 passed in 47.18s
```

FM-5 *resolves* FM-4's emitter (the A1 ruling landed) and *does* import its values — the
coupling's plumbing works. What it imports is six `unavailable`s.

The live measurement, for the record — `funnel_lifecycle.measure(repo_root)` on this tree,
0.77 s:

```
live_intakes 55 · archived_intakes 10 · ready_intakes 19 · live_adrs 88
rows 349 · post_cutoff_rows 13 · threshold_days 30 (protocols/FUNNEL_LIFECYCLE.md:316)
leg a1 0 · leg a2 0 · leg b 0 · leg c 0 · leg d 1
```

---

## 2. THE RULING — field by field

The done-contract's binary: each of the six either renders a number **derived from
`funnel_lifecycle.Measurement`**, or is **REMOVED** by a ruling recorded here. No field is left
rendering `unavailable` by default. `[#619]` deliberately proposes no mapping; choosing it is
this lane's first ruled act.

### 2.1 `intakes consumed-unarchived` → **RE-MAPPED and RE-LABELLED**

**Mapped to** `len(m.by_leg("terminal-not-archived"))` (leg a1).

Leg a1 is the exact question the field was reaching for: an intake whose status is terminal and
which still sits at `docs/intake/` depth 1 instead of `docs/intake/archive/`.

**The label moves, and that is the ruling's substance.** Leg a1's predicate is
`TERMINAL_INTAKE_STATUSES = {CONSUMED, SUPERSEDED, REJECTED}` and `docs/intake/README.md` §5
relocates all three. Publishing a *terminal* count under a *consumed* label is the same class of
overclaim this whole batch exists to remove — a number that is true about a wider set than its
name admits. New label: **`leg a1 intakes terminal-unarchived`**.

### 2.2 `ADRs unexecuted` → **REMOVED**

FM-2's only ADR leg is (b) `adr-terminal-not-archived`: an ADR whose `Status` is terminal that
still sits in `docs/decisions/` rather than `docs/decisions/archive/`. That is a *location*
question. "Unexecuted" is an *implementation* question — Accepted, but the decision was never
carried out — and **FM-2 measures nothing about implementation**.

Mapping leg (b) onto this label is available, cheap, and would have produced a green test. It is
refused: it is precisely the guessed mapping the row exists to prevent. The label is removed and
leg (b)'s number is rendered under **leg (b)'s own name** (§2.7).

### 2.3 `orphans forward (object -> consumer)` → **REMOVED**

No leg of FM-2 asks whether a governed object has a consumer, and `funnel_lifecycle.py`'s own
header says so in as many words: the organ that asks it is **`consumer_at_landing` (`[#595]`)**,
a different check over `docs/audits/`, whose pool includes `docs/intake/` and `tasks/` "as
CITERS — never as subjects".

Deriving this from FM-2 is impossible. Deriving it from `consumer_at_landing` would make FM-4 a
**two-source** block, which is outside the done-contract's binary and would re-open, at the level
of the tuple, the "two answers to one question" defect the FM batch was built to close. Removed;
named here as the one field whose loss is a real loss, and as a candidate for a later row.

### 2.4 `orphans backward (open row -> resolving source)` → **RE-MAPPED and RE-LABELLED**

**Mapped to** `len(m.by_leg("row-provenance-unresolved"))` (leg c).

Leg (c) *is* "a row that cannot resolve back to a source": it takes each row, reads its
`· refs …` provenance clause, and fails the row when the clause is absent or when no token in it
resolves against the ref universe.

**Two narrowings the old label hid, now carried in the new one:**

1. Leg (c) is scoped to rows that landed **on/after `ARM_DATE`**. Older rows are grandfathered —
   and grandfathered *by measured birth date from git*, never by assumption. A label promising
   "open rows" while the number covers 13 of 349 is a 26× overclaim.
2. Leg (c) does **not** filter open-vs-terminal. It reads every post-cutoff row.

New label: **`leg c rows post-cutoff, provenance unresolved`**, rendered beside its denominator
`rows post-cutoff` (§2.7) — because `0` violations out of `0` rows and `0` out of `13` are
different facts and a bare zero cannot tell them apart.

### 2.5 `rows closed this window` and 2.6 `value evidence attached` → **BOTH REMOVED from FM-4**

Ruled together because they share one reason. Neither is FM-2's. Both are **FM-5's own derivations**, and `governance_health.py`'s module
doctrine already rules the split in writing:

> `FM5_OWNED_FIELDS  rows closed this window · value evidence attached` → *computed here,
> EXPORTED for FM-4 to import*

`rows closed this window` needs a git window (`window_base_sha` + a `git log` walk);
`value evidence attached` needs the close-packet corpus parsed. `Measurement` carries neither and
should not — FM-2 is a lifecycle detector, not a window reporter.

**The alternative was considered and is refused:** have FM-4 import FM-5's two derivations, so
the bundle block keeps them.

- `_FUNNEL_FIELDS` is *defined*, in FM-4's own comment, as "(rendered label, attribute on FM-2's
  measurement)". A second source inside that tuple reopens the two-answers defect at the level of
  the tuple, which is where this lane found it.
- It would put a `git log` walk and the whole `docs/audits/` packet parse on the **bundle-cut**
  path, for two numbers a bundle reader can get from `audit.py governance-health`.
- FM-4 → FM-5 is already a live import edge in the other direction; adding the reverse edge makes
  it mutual and the resolution lazy on both sides.

**Nothing is lost by the removal.** Both fields have rendered `unavailable` in every bundle FM-4
has ever cut, and **FM-5's report keeps both**: `FM5_OWNED_FIELDS` is unchanged and
`SHARED_FIELDS = FM4_OWNED_FIELDS + FM5_OWNED_FIELDS` still carries them.

---

### 2.7 THE OTHER HALF OF THE RULING — what FM-4 now renders

Two survivors is not a repair. A block headed **FUNNEL HEALTH** that shows 2 of FM-2's 5 failure
legs is a *false report* in a second way: a reader sees two zeros and concludes the funnel is
clean while leg (d) carries a violation. And the two survivors have no denominators, so their
zeros are unreadable.

So the mapping is ruled as a **rule**, not as a hand-kept list — which is what makes the
anti-drift test mechanical rather than a second list to maintain:

> **FM-4 renders every `int`-typed field of `funnel_lifecycle.Measurement`, plus one count per
> `LEG_*` constant. Nothing else, nothing less.**

Yielding eleven fields, in this order (the order IS the contract; a golden test pins it):

| # | label | source |
|---|---|---|
| 1 | `intakes live` | `Measurement.live_intakes` |
| 2 | `intakes archived` | `Measurement.archived_intakes` |
| 3 | `intakes READY` | `Measurement.ready_intakes` |
| 4 | `ADRs live` | `Measurement.live_adrs` |
| 5 | `rows` | `Measurement.rows` |
| 6 | `rows post-cutoff` | `Measurement.post_cutoff_rows` |
| 7 | `leg a1 intakes terminal-unarchived` | `by_leg(LEG_A1)` |
| 8 | `leg a2 intakes ACCEPTED, every named row terminal` | `by_leg(LEG_A2)` |
| 9 | `leg b ADRs terminal-unarchived` | `by_leg(LEG_B)` |
| 10 | `leg c rows post-cutoff, provenance unresolved` | `by_leg(LEG_C)` |
| 11 | `leg d READY intakes past threshold` | `by_leg(LEG_D)` |

**What the rule EXCLUDES, and why each exclusion is honest rather than convenient:**

- **`detector`** (`str`) — not a number. It is already published, on the block's `source:` line.
- **`threshold_days`** (`int | None`) and **`threshold_locator`** (`str | None`) — the annotation
  is not `int`. These are leg (d)'s *parameters*, not funnel numbers, and a `None` would render
  `unavailable` **by default**, which the done-contract bars outright. The NOT-ARMED case they
  describe is already reported, at its own tier, by `funnel_lifecycle.findings`.
- **`violations`** (`list[Violation]`) — rendered as the five per-leg counts instead. A single
  total would hide which leg moved, which is the only thing the number is read for.
- **`by_leg`** — a method, and the reader of `violations`.

The `int`-vs-`int | None` discriminator is not a runtime `isinstance` guess: it is read from
`typing.get_type_hints(Measurement)`, where the six survivors resolve to `<class 'int'>` and
`threshold_days` resolves to `int | None`. That is what makes the rule checkable.

---

## 3. Anti-drift (done-contract item 2)

The zero-intersection state must not be silently re-reachable. Three tests, all in
`tests/test_gen_handoff.py`:

1. **`test_funnel_fields_cover_fm2s_whole_int_and_leg_surface`** — set equality **both ways**
   against the live FM-2 module: `{attr keys} == {int-annotated dataclass fields}` and
   `{leg keys} == {values of the LEG_* constants}`. A field added to FM-2, removed from it, or
   renamed REDs FM-4. This is the guard that the six-vs-eleven drift could not have survived.
2. **`test_funnel_fields_intersect_fm2`** — the witnessed starting state pinned as unreachable:
   the intersection of what FM-4 reads and what FM-2 exposes is non-empty and complete.
3. **`test_funnel_health_renders_no_unavailable_against_the_live_repo`** — the done-contract's
   "no field is left rendering `unavailable` by default", asserted against the real tree rather
   than a fake measurement.

---

## 4. What changed

*(completed at Step 3 — see §5)*

## 5. Result

*(completed at Step 3)*
