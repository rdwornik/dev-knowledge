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

Three commits on `worktree-lane-a-619-fm-coupling-repair`, off `902b621b`.

**`6883564d`** — this packet, §1–§3: the ruling recorded *before* any code change, per the
done-contract's first item.

**`78486293`** — the implementation.

### `scripts/gen_handoff.py`

- `_FUNNEL_FIELDS` becomes `(label, kind, key)` triples over the ruled rule, eleven entries.
- `_load_funnel_measure` now returns the **module** alongside the callable, so
  **`_funnel_leg_names`** can validate every leg key against FM-2's own `LEG_*` constants at
  **render time**. This is a defect the ruling found while implementing it and is worth naming
  separately: `Measurement.by_leg` *filters a list*, so it answers `[]` for a leg name it has
  never heard of — indistinguishable from `[]` for a leg with no violations. Without the guard,
  a leg renamed on FM-2's side would make this block publish a confident **`0`**: a false clean,
  strictly worse than `unavailable`, and the same failure class as `[#619]` itself. Unresolvable
  leg keys now degrade to `unavailable` and say so in the block's `source:` note.
- The block's header comment claimed *"THE COUPLING IS UNPROVEN AS SHIPPED … FM-2 (lane I) had
  not landed"*. Lane I landed; the comment stayed. It is replaced with what actually happened
  and a pointer to §2 of this packet.

### `scripts/governance_health.py`

- `FM4_OWNED_FIELDS` re-pointed to FM-4's eleven labels, **copied verbatim** — the standing A1
  ruling (the source names its fields; a consumer that renames them is the drift) is untouched
  and re-stated in place, with the retired roster recorded beside it.
- `FM5_OWNED_FIELDS` and `SHARED_FIELDS` are **unchanged**. FM-5's report still carries all
  thirteen numbers; only FM-4's bundle block stops rendering the two it could never derive.
- Module docstring corrected: it described a four-field FM-4 roster and *"a fifth"* that never
  existed, and it asserted an `unavailable` is a true answer without noting that it is not a
  *passing* one — the precise gap `[#619]` lived in.

### `scripts/funnel_lifecycle.py` — **UNCHANGED, and that is part of the ruling**

It is in the frozen write-scope and was deliberately not touched. FM-2 is the **source of
record**; FM-4 is the consumer that drifted. Every alternative that would have edited FM-2 —
adding `intakes_consumed_unarchived` as an alias, say — would have made the detector carry a
second vocabulary for one caller's benefit.

### `tests/`

Four new cases. The three under **ANTI-DRIFT** import the **live** FM-2 module, and the section
comment now records why that matters: every shape test in the file passed for the entire life of
the dead coupling, because a fake measurement answers to whatever names the fake was given.

| test | what it refuses |
|---|---|
| `test_funnel_fields_cover_fm2s_whole_int_and_leg_surface` | set equality **both ways** vs. the live module — a field added to, removed from, or renamed on FM-2 |
| `test_funnel_fields_intersect_fm2` | the witnessed empty intersection, pinned unreachable |
| `test_funnel_health_renders_no_unavailable_against_the_live_repo` | the done-contract's "no field left rendering `unavailable`" |
| `test_a_renamed_leg_renders_unavailable_and_never_a_false_zero` | the render-time false-`0` above |

Existing cases updated rather than replaced: the golden literals, the `fm2` fake (now module-
shaped, carrying `LEG_*` constants as literals — never imported from the module under test), the
`_load_funnel_measure` 3-tuple, and the banned-vocabulary list in
`test_no_fm4_owned_field_is_derivable_from_this_module`, re-pointed to the new labels while
keeping the retired words.

**The anti-drift tests were trip-tested, not asserted.** `LEG_C` renamed and a `brand_new_number:
int` field added to `Measurement`: `test_funnel_fields_cover_fm2s_whole_int_and_leg_surface` and
`test_funnel_health_renders_no_unavailable_against_the_live_repo` both RED, and the leg rendered
`unavailable` rather than `0`. Mutation reverted; `scripts/funnel_lifecycle.py` is byte-identical
to `902b621b`.

## 5. Result

```
BEFORE (902b621b): 103 passed, 1 failed  — test_shared_fields_equal_fm4_block_byte_for_byte
AFTER  (78486293): 108 passed, 0 failed  — 104 existing + 4 new
uv run --locked ruff check <the four files>: All checks passed
```

Done-contract, item by item:

1. **Mapping ruled and recorded before any code change** — §2, committed as `6883564d` ahead of
   the implementation commit. Two fields re-mapped, four removed, eleven rendered; every removal
   carries its reason and the alternative it refused.
2. **A test fails if the two surfaces drift apart again** — three cases, trip-tested above.
3. **`test_shared_fields_equal_fm4_block_byte_for_byte` is GREEN** — the row-owned RED, fixed by
   the row's own lane. **No other RED was touched**; the baseline carried exactly one and it was
   this one.
4. English, hyphen-only names, no `print` added, no CLI warranted, `pytest` green on the targeted
   set.

### Open items — handed to the integrator, not decided here

- **`orphans forward (object -> consumer)` is a real loss, and the only one.** It named a
  question worth asking that FM-2 cannot answer; the organ that can is `consumer_at_landing`
  (`[#595]`), over a different corpus. Wiring it in would make FM-4 a two-source block — outside
  this lane's done-contract and its write-scope. **Candidate for a row**, not filed here (filing
  backpressure: a lane does not birth rows for the integrator).
- **The bundle's `FUNNEL_HEALTH.md` no longer carries `rows closed this window` or `value
  evidence attached`.** Both had rendered `unavailable` in every bundle ever cut, so nothing that
  ever worked stopped working, and `audit.py governance-health` still reports both. Named because
  it is a visible change to a browser-adjacent artifact, not because it is contested.
- **The full suite was not run** — lane cadence is the targeted files covering the diff; the full
  suite runs once, at integration (`[#528]`, PLAYBOOK Ch5). The two files run here are the ones
  that cover it, and `governance_health` / `gen_handoff` have no other test-side callers
  (`grep -rn "_FUNNEL_FIELDS\|funnel_health_block\|FM4_OWNED_FIELDS\|SHARED_FIELDS" tests/`
  returns these two files only).
- **No JOURNAL entry, no index regeneration, no merge** — all the integrator's, per the contract.
  `docs/audits/README.md` is left stale on purpose (`[#590]` narrowed that hook; a batch lane
  regenerating it is the defect).
- **No V-2 escalation was triggered.** No curated baseline was touched, no rule-vs-ruling
  conflict arose, and no fork lacked a standing ruling — the two judgement calls this lane made
  (relabelling two fields, and completing the block to all five legs rather than leaving three
  unreported) are decided per contract defaults and reported in §2 rather than asked.
