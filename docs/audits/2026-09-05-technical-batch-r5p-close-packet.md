# BATCH R5P — THE CLOSE PACKET

> **This file IS the close act.** `scripts/batch_manifest.py` resolves an open batch as the
> conjunction of four facts: the manifest is tracked, `status: open`, `closed_by:` names a shape
> that CAN resolve, and **that path is ABSENT**. The manifest
> (`docs/audits/2026-09-05-technical-batch-r5p-manifest.md`) declares this path at its
> `closed_by:` line. Writing this file falsifies the fourth conjunct, so the batch closes without
> anyone editing the manifest — which is what an immutable genre requires. Nothing above is
> amended; no `status:` line is touched.
>
> Written by the integrator (INTEGRATOR-2, primary checkout) at batch close, 2026-09-06. The
> filename carries 2026-09-05 because the manifest declared that exact path at dispatch; the
> locator is the manifest's to choose, not the writer's.
>
> **WHEN THIS BECOMES IMMUTABLE, since the answer is not the obvious one.** The close takes
> effect when this file lands on `main` - at the MERGE, not at the branch-local commit that
> created it. Running `batch_manifest.open_batches` from the authoring branch reports R5P
> closed, but that reads the branch's tree; from `main` the batch stays open until the merge.
> So corrections made to this file BEFORE it lands are authoring, not amendment, and three
> were made (§6). Once it is on `main` this file is immutable like any audit, and a correction
> then rides as an appended marker - the shape used for the L4 lane packet's ERRATUM in §4,
> which had already landed and therefore could not be touched.

## 1. Rows closed — the hard metric

**ZERO. By design, and declared in advance.**

All three lanes carry the `000` no-row id. The manifest states it at dispatch: *"`000` is the
no-row id: none of the three lanes discharges a BACKLOG row, and none files one."*

Independently measured at close rather than asserted: `scripts/window_metrics.py` reports
`224 -> 224 rows; filed 0 (none); closed 0 (none)`.

This is the number the batch was built to produce, so it is reported as a success and not as a
shortfall. A batch that closes zero rows and said so beforehand is a different object from a batch
that closes zero rows and hoped for more.

## 2. Per-lane witnesses

Each lane is witnessed by the first-parent merge that landed it. L2 has no witness because it was
never booted.

```
L1  lane-r-000-docrot-arm2     MERGED 4a9ff8f0   code   delta A2 taken
L3  lane-r-000-bundle-gitlog   MERGED 74c111e6   code   delta A2 taken
L4  lane-r-000-zc-candidates   MERGED 14ddd724   docs   terra alone (docs-only re-scope)
L2  lane-r5p-docclaims-tier    REFUSED at the dispatch gate — never booted
    the manifest itself        MERGED 30c880ea
```

**L1 — doc_rot ARM 2 reports the corpus, not 72 separate rows.** A clean three-commit TDD arc: RED
witness first (`2b9582e7`), then the fix (`3752728d`), then the end-of-lane packet. The RED came
before the build code, which is what ADR-108 §B asks for and what lanes most often skip. Delta A2,
measured on the integrator's tree rather than read from the lane packet: `loci 77 -> 6`; arms
`backlog-row-length 72 -> 1`, `backlog-accretion 3 -> 3`, `section-history 1 -> 1`,
`grooming-cadence 1 -> 1`.

**L3 — one `git log` for all handoff bundles.** 87 subprocess spawns become 1. Two hunks in
`scripts/audit.py`, both where declared, plus 432 lines of tests. The contract carried an
ANTI-requirement — *"no other `audit.py` change"* — and it held exactly. That is the half of a
frozen contract lanes usually break, so it is recorded that this one did not. STOP was confirmed on
transcript BYTES over a 7m32s window with tips stable, not on commit count: an end-of-lane packet
commit is the contracted FINAL step, so a lane AT its packet looks identical to a lane GATE-BLOCKED
at its packet. Byte-stability separates them; a tip does not.

**L4 — two CANDIDATEs in the Z-C shape.** Landed as section AE of `protocols/STANDING_RULINGS.md`,
plus one appended ERRATUM to the lane packet. See §4 for the two rulings this lane forced.

## 3. Delta A2

Two of the three lanes are code branches and carry delta A2 individually (§2). The batch-level
figures below are the integration measurement taken at close, on a stable tree, after the last
merge, with nothing else running.

```
full suite         21 failed · 4967 passed · 3 skipped · 1 xfailed      1310.50 s
audit.py health    35.2 s ± 0.15 (n=3: 35421 / 35134 / 35194 ms)        health: OK
journal_spine_anchor                                                    [OK]
```

An earlier full-suite run reporting 24 failed / 4964 passed is **discarded rather than reported
with a caveat**: two docs commits landed while it was in flight, so it is not a clean snapshot of
any tree. The three-failure difference is accounted for — two `test_gen_audit_index` failures and
one `test_trend_dashboard` failure cleared when the stale audits index was regenerated.

### Discharging the manifest's open measurement item

The manifest left one item explicitly open for the integrator: *"`audit.py health` wall-clock delta
printed"*, noting that the hook route makes that delta ~0 by construction, *"which is an answer, but
it is not a measurement."*

**Discharged as follows, with the distinction kept rather than collapsed.** The ABSOLUTE figure is
now measured and printed above: 35.2 s, stable to ±0.15 s across three consecutive idle-machine
runs. The DELTA remains **NOT MEASURABLE AT THIS SURFACE**, and not for want of trying: the
29-second `pytest --collect-only` never entered `audit.py`'s check set at all — the landed work put
it in a `files:`-filtered pre-commit hook instead. A delta of a check that was never added to a
surface cannot be measured on that surface. The honest close is the absolute number plus the reason
the delta is unavailable, rather than a `0` that would read as "measured, no change".

## 4. The two rulings L4 forced, and how they were discharged

The manifest handed both to the integrator explicitly — *"which disposition survives is the
integrator's ruling, not a lane's."*

**The collision.** `worktree-file-candidates` filed the SAME two items as BACKLOG rows
`[#635]`/`[#636]`; L4 filed them as CANDIDATEs, no rows — the opposite disposition. **The CANDIDATE
shape stood.** The colliding branch merged at `8ea8023a`; the two rows were dropped at `e3d2ac34`
on the operator's own recorded consent, on the ADR-111 ground that they were born bypassing the
funnel. The only route to a row is CANDIDATE → intake (ADR-98) → ratification, and the rows had not
taken it.

**The unlocatable premise.** The contract said *"reconciled against intakes #68/#69"*, and the
manifest recorded that those did not exist. That was TRUE when written and became false before the
lane landed: they are listed in `docs/intake/README.md` as #65–#70 — they were not on `main` at the
time of writing. Because the lane packet is an IMMUTABLE audit, the correction rides as an appended
ERRATUM rather than an in-place edit; the same correction was applied in place in section AE, which
is a LIVING register, under a named architect exception (dead author, factual corrections only).

Both findings were correct when authored. They are errata, not lane defects, and the packet says so
in those words.

## 5. CANDIDATE carried forward — the one the manifest named

The manifest recorded one gap as *"a CANDIDATE for the close packet, not a row filed here"*, and it
is carried here unchanged. **This is a CANDIDATE. It is not a row; it has no peg, no owner and no
size band; the only route from here is intake (ADR-98) → ratification (ADR-111).**

**R5P-C1 · A contract cannot state its own model.** `gen_lane_contract.py`'s `_DISPATCH_LINE_RE`
admits `-Effort` and **not** `-Model`, so a dispatch line carrying an explicit model fails the
contract check, while `Start-DispatchLane` defaults `-Model` to `opus`. A contract may therefore
state a model in its routing table that its own launch line structurally cannot carry. All three
R5P contracts were authored at `sonnet` and had to be re-stated to `opus`. This is the same
silent-`--model`-drop class PLAYBOOK Ch8 records for the raw form, surviving inside the checked
surface that replaced it.

## 6. SCORECARD (hand-filled)

**Every number is marked for its provenance.** `organ-computed` means a script produced it and the
command is named. `hand-counted` means the integrator counted it over the session span and no organ
computes it — those are tallies of recorded events, not metrics, and they are not to be cited as if
a surface maintained them. The distinction is the point of this section: a hand count presented as
computed is the drift class this repo keeps having to repair.

Session span = `3200757d..HEAD` (the primary checkout's HEAD at session start, to close).

```
rows closed                        0       organ-computed   window_metrics.py
net backlog delta                  0       organ-computed   window_metrics.py (224 -> 224)
paste / boot bytes vs budget   17364       organ-computed   window_metrics.py (96% of 18000)
audit checks                      54       organ-computed   gen_doc_counts.py --check
pre-commit hooks                  23       organ-computed   gen_doc_counts.py --check
pytest collected                4992       organ-computed   gen_doc_counts.py --check
suite result            21F / 4967P        organ-computed   pytest -q, 1310.50 s, idle tree
audits corpus                    897       organ-computed   gen_audit_index.py (incl. this file)

boot round-trips            NOT COMPUTED   organ-declared   handoff spec major v7 unmapped
windows to cutoff           NOT COMPUTED   organ-declared   judgment INPUT, not an observation
drift-report runs           NOT COMPUTED   organ-declared   not instrumented; leaves no trace

spine merges landed               43       hand-counted     git log --first-parent 3200757d..HEAD
of those, touching code           28       hand-counted     per-merge diff-tree filter
R5P lanes merged                   3       hand-counted     of 4 dispatched; 1 refused at the gate
audit.py health wall-clock      35.2 s     hand-counted     3 timed runs; the command prints
                                                            no timing, so the mean and the
                                                            +/- 0.15 s are the integrator's
JOURNAL entries by this seat      10       hand-counted     2026-09-05 (m)-(u) = 9, of which 8
                                                            carry the INTEGRATOR-2 tag, plus
                                                            2026-09-06 (a)
worktrees torn down                2       hand-counted     zc-candidates, filings-3
directory husks remaining         13       hand-counted     against 2 registered worktrees
terra rounds spent on AF           5       hand-counted     4 with findings, the 5th CLEAN
```

**Three SCORECARD corrections were caught in review and are recorded rather than silently
fixed. They are not all the same kind of error, and saying so precisely matters more than the
tidier confession.** ONE was a provenance mislabel: the `audit.py health` wall-clock was
marked `organ-computed` when that command prints no timing at all - the mean and the spread
are the integrator's, from three timed runs, and the row is now `hand-counted` with its method
named. That one is exactly the drift this section warns about, produced by the person writing
the warning. The other TWO were wrong VALUES under labels that were already correct: the
audits corpus read 896 where the regenerated index says 897, because the packet had not
counted itself; and the JOURNAL tally read 8 against a span holding 9. Calling all three
provenance errors would overstate the fault and blur the very distinction this section
exists to draw.

**`window_metrics.py` reads `origin/main..HEAD`, and reported 0 arcs when this scorecard was
measured.** It was run at a moment when `HEAD` equalled `origin/main` — every merge of the day
already pushed — so its range contained no merge commits. That zero is CORRECT for the range the
organ declares; it simply is not a description of the batch, whose merges had all left the range
by being pushed. Note the reason is the measurement conditions, not a standing property: read
from an unpushed branch the same range is non-empty, and this packet was itself authored on such
a branch. The 43 is hand-counted for that reason and stays in the hand-counted block rather than
being substituted into the organ's row.

## 7. REDs at close — attributed, not totalled

21 failures on a stable tree. A total is not an attribution, so each cluster is placed.

```
7  test_governance_health.py      PRE-EXISTING. Neither scripts/governance_health.py nor its tests
                                  were touched in this session; last changed at 28bb3002, an
                                  earlier batch. Attributed by provenance, not by assumption.
2  test_reverse_dep_oracle.py     PRE-EXISTING; not touched this session.
2  test_cloud_provisioning.py     PRE-EXISTING; not touched this session.
1  test_consumer_at_landing.py    KNOWN AND EXPLAINED. Not closeable from a ledger row: that organ
                                  asks whether a governance POOL file cites the artifact, and
                                  docs/audits/ is not in POOL_DIRS. A mechanism limit, not debt.
1  test_batch_manifest.py         NOT THIS BATCH. The assertion fails on the H0-PREP batch, whose
                                  name fails .isalnum() on its hyphen. R5P passes that check.
                                  Closing R5P does not fix it, and no such claim is made.
1  test_validate_doc_rot.py       Calendar-driven accretion locus; the known cost of B8/B10,
                                  dispositioned to B6/[#612] rather than smoothed here.
1 each — test_routing_agreement, test_preflight_freeze_predicates, test_manifest_link_route,
         test_gen_north_star, test_enforcement_coverage, test_desired_state_report,
         test_canonical_docs                              PRE-EXISTING; not touched this session.
```

**No RED in this list is attributed to an R5P lane.** The two a reader might reasonably suspect are
named and cleared explicitly: `consumer_at_landing` is a construction limit with its mechanism
stated, and `batch_manifest` belongs to a different batch entirely.

## 8. What this packet does NOT claim

- It does not claim the batch closed rows. It closed zero, as designed (§1).
- It does not claim the suite is green. It is not; 21 REDs are listed and placed (§7).
- It does not claim the `audit.py health` delta was measured. It was not, and §3 says why.
- It does not claim R5P-C1 is filed. It is a CANDIDATE and owes intake (§5).
- It does not claim the `worktree-filings-3` directory husk was removed. Registration, local branch
  and origin branch are all clean and verified at zero refs; the directory refused with
  `Permission denied` while a process held it, and only that process can free it.

---

## ERRATUM 1 — two corrections, appended because this file is now on `main` (2026-09-06)

*The packet's own header states the boundary: corrections before landing are authoring, corrections
after landing ride as an appended marker. This file landed at `b76806e4`, so both corrections below
are appended and nothing above is edited. The header predicted this shape; this is it being used.*

**§3 — "taken at close, on a stable tree, after the last merge" is imprecise about WHICH merge.**
The batch-level figures were measured on `main` at `3a2391fb`, which was the last merge *at the
time of measurement*. The close-packet merge `b76806e4` followed. A close packet structurally cannot
measure a tree that already contains its own landing, so the gap is unavoidable — but the sentence
as written implies otherwise, and the honest statement is the basis SHA.

**Re-verified after `b76806e4` rather than assumed away**, on the organs a newly added audit file
could plausibly move: `test_gen_audit_index` PASSES, `test_funnel_coverage` PASSES, and
`test_consumer_at_landing`, `test_validate_doc_rot` and `test_batch_manifest` fail exactly as §7
records — same three, same reasons. **The 21 / 4967 figure therefore stands for the landed tree**,
and this erratum records the check rather than the assumption.

**§4 — the intake range `#65–#70` cites an id that resolves to TWO documents.**
Reported by the R5P dispatcher and verified here against `main`:
`docs/intake/README.md` carries `#70` twice —
`2026-09-05-tech-aj-second-pass.md` and `2026-09-05-tech-session-roles-with-a-carrier.md`.
Maximum id is 71.

This matters beyond tidiness: an intake number is the citation handle the whole ADR-111 funnel uses
(CANDIDATE → intake `#n` → ratification), so a collided id means "intake #70" no longer names one
thing, and a pattern matching `intake #<n>` will match either. **The §4 correction still stands** —
the two documents L4 could not find do now exist and resolve; it is only the last id of the cited
RANGE that is ambiguous.

**It also revises a rule this packet relied on.** The dispatcher's derivation — intake number =
ordinal position in `docs/intake/` sorted by name, plus 10 — held against two live citations when
it was made, and a duplicate proves the number is **not** a pure positional function. Whoever files
next should **read the maximum id from the index and check for collisions**, not compute an ordinal.
The dispatcher volunteered this correction against its own earlier finding, unprompted and after
its batch had closed.

**Filed as a CANDIDATE, not a row** — R5P-C2, alongside R5P-C1 in §5, and subject to the same
route: intake (ADR-98) → ratification (ADR-111). No row is created here, and the collision is left
unrepaired on purpose: renumbering a live citation handle is not an integrator's unilateral act at
batch close.
