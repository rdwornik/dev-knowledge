# Terra pre-merge review — batch-1 lane L2 (`lane-b-608-journal-tiling-seam`)

- **Reviewer:** `gpt-5.6-terra` via `codex exec` (codex-cli 0.145.0)
- **Lane:** L2 — the `[#608]` journal rotation seam under ruling X5 ("rotate the FILE, not
  the PREDICATE"). Contract cites `[#587]`; see the locator correction below.
- **Diff reviewed:** the lane's staged diff, supplied INLINE
- **Date:** 2026-08-28

## TALLY (as returned by the reviewer)

```
TALLY: critical=0 high=2 medium=0 low=0
```

## Property check the reviewer returned

```
P1  zero bytes move with no legacy tiles     HOLDS   (`if len(parts) == 1: return parts[0]`)
P2  both the working-tree and the rev path   HOLDS   (dual branches, iterdir / ls-tree)
P3  ONE predicate, no second implementation  HOLDS   (tiling contained in journal_text)
P4  a missing tile errors, never omits       FAILS   (see HIGH-1)
```

## Findings, with the lane's disposition

### HIGH-1 — a DELETED legacy tile is silently omitted

> *"A rotated journal file is removed or missing from a revision, and an entry anchored only
> in that tile is reported as an unanchored gap instead of causing the gate to fail loudly."*

**Disposition: ACCEPTED as a real limit, NOT fixed here, and now documented in the code.**

The distinction matters and the lane's original docstring blurred it. A tile that exists and
**cannot be read** does raise — that half was already true. A tile that was rotated out and
then **deleted** is undetectable, because nothing declares which tiles ought to exist.
Closing it requires a **declared tile manifest**, which is a design act with a governance
cost; `[#608]` is scoped to a seam that moves **zero bytes** and takes no governance act, so
building one here would widen a frozen lane.

The docstring now states the limit in the code rather than in a review nobody re-reads,
including its direction: the failure shrinks the anchoring universe and produces a **false
gap**, which is the safe direction but still wrong. **Handed to the integrator as a
CANDIDATE** (declared tile manifest for rotation).

### HIGH-2 — legacy-tile recognition accepted any prefix/suffix match

> *"A stray `JOURNAL-legacy-notes.md` containing a SHA is swept into the anchoring universe
> and can falsely mark a spine entry anchored."*

**Disposition: VALID. FIXED in this lane.**

This one is a genuine defect and the worst direction of failure — a **false GREEN on the
ADR-85 hard leg**, where a stray file makes a spine entry look anchored that nothing
anchors. The original `startswith`/`endswith` pair also left the docstring's claim that
"a plain lexical sort IS date order" **unearned**, since a non-ISO name sorts anywhere.

Recognition is now `_LEGACY_RE = ^JOURNAL-legacy-\d{4}(?:-\d{2}){0,2}[A-Za-z0-9._-]*\.md$`.
Enforcing the ISO prefix fixes the finding **and** earns the ordering claim, so one change
closes both. Pinned by `test_a_legacy_lookalike_without_an_iso_span_is_not_swept_in`, which
asserts the accepted set and that it equals its own sort.

## Also raised, and acted on

Terra noted the tests omitted the git-rev path. Correct — added
`test_tiling_covers_the_rev_path_not_only_the_working_tree`, asserting the rev read includes
tiles and **agrees with the working-tree read**. That agreement is the property that keeps
the pre-push HARD leg and the audit backstop from disagreeing about what is anchored. The
test builds its own repo rather than skipping when a fixture is absent, per **Z-G4** — a
check that cannot compute its ground truth FAILs, it does not skip.

## Locator correction (contract defect D2, carried to the integrator)

The frozen contract's L2 block cites `[#587]` for the tiling seam. `[#587]` is the
anchor-check **single-pass inversion**; the seam is `[#608]`, whose body carries this lane's
work verbatim ("rotate the FILE, not the PREDICATE", "moves zero bytes", X5/C3). `[#608]`
also carries `depends-on: "#587"`, and **`[#587]` is still open** — the dependency is
unmet. The lane executed `[#608]`'s mechanism per CLAUDE.md M1 (resolve a locator before
acting) and reports both facts rather than silently picking one.

## Verdict

**MERGE-ELIGIBLE.** No critical findings. HIGH-2 fixed and pinned by a test; HIGH-1 accepted,
documented in the code, and carried as a candidate. Zero bytes of journal content moved.
