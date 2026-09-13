# lane-x-628-docs-cut — reader census re-run (Step 1)

> This lane's Done-contract item 5: "Every cut is verified against its live readers BEFORE
> the cut, in THIS tree. Re-run the reader census per target; do not act on this contract's
> summary of a census taken on another commit. A reader discovered mid-cut is a class (b)
> fact, and it changes the cut." This is that re-run, against `docs/audits/2026-09-13-census-docs-cut-manifest-measurement.md`
> (commit `6dcda4fd`), for the three targets this lane executes: ARCHITECTURE.md's prologue,
> PLAYBOOK.md's prologue, and `protocols/ESSENTIALS.md`'s registry memberships.

## Confirmed unchanged from the 2026-09-13 manifest census

- **ARCHITECTURE.md's prologue (lines 17–276 at that census, re-measured here as 17–259 —
  the census's own line-260 boundary for the surviving "How to read this doc" guide is
  correct and unchanged):** frontmatter (`last_reviewed`, `reconciled_with`) is read by
  `scripts/canonical_freshness_gate.py` (the file is in `canonical_docs.FRESHNESS_FILES`)
  and by `scripts/audit.py`'s `doctrine_table`. Zero readers found on the prose body itself.
  Re-verified in this tree: still true.
- **`protocols/ESSENTIALS.md`:** exactly four `scripts/canonical_docs.py` registry
  memberships still treat it as live — `CANONICAL_OPTIONAL` (:150), `FRESHNESS_FILES`
  (:166), `SECTION_HISTORY_DOCS` (:252), `STRUCTURE_DOCS` (:259) — plus the derived literal
  fallback in `scripts/canonical_freshness_gate.py:52` (`DEFAULT_FRESHNESS_FILES`), which
  `tests/test_canonical_docs.py::test_freshness_gate_consumer_fallback_equals_the_registry`
  pins equal to `canonical_docs.FRESHNESS_FILES` — so retiring the registry membership
  requires updating this fallback literal too, or the equality test breaks. Re-verified:
  `CONFORMANCE_V2_SCAN` (a fifth site the [#628] row's body once worried about) was
  **already** dropped — its own comment at `canonical_docs.py:269` records this as done
  "pending [#628]" — so it is not part of this lane's footprint.
- **PLAYBOOK.md's prologue prose body (the dated review-pass blockquotes):** zero readers
  found on the narrative prose itself — `toc-freshness-playbook` only scans `## ` headings,
  the first of which is well past the prologue.

## A reader the 2026-09-13 census did not see (class (b) fact — changes the cut)

**PLAYBOOK.md's prose `> **Last updated:** <date>` line is a live-read surface, distinct
from the `reconciled_with:` frontmatter key the prior census checked.** `scripts/audit.py`'s
`parse_declared_freshness` / `_PROSE_STAMP_RE` extracts this exact line as the file's
declared freshness date under `SURFACE_PROSE` (PLAYBOOK is *the* file `doctrine_table`'s own
docstring names as "the case that names the problem" — a prose-only stamp no gate parses,
Done-contract item 4 of a different, earlier arc). It is pinned live by
`tests/test_canonical_docs.py::test_the_live_playbook_doctrine_row_shows_its_reconciled_spec_and_a_derived_date`
(`@pytest.mark.live_repo`), which asserts `row.surface == aud.SURFACE_PROSE` and
`row.doc_class == aud.CLASS_UNGATED_FRESH` against the actual tree.

Cutting the review-pass blockquotes verbatim (lines 7–96, frontmatter/title/Organization
only) deletes this line along with the narrative and flips the live test to
`row.surface == 'none'` — confirmed by running it against the bare cut before this fix
landed. **This changes the cut per item 5's own rule:** the surviving prologue keeps one
single, non-narrative stamp line — `> **Last updated:** 2026-09-13` plus a one-sentence
reason for the cut, no chained history — immediately after the title. This is the file's
own established mechanism (documented in the very blockquote text being cut: "the stamp
line moves with the last edit rather than being written once at the top of the lane"),
applied once, not restarted as a new accretion chain.

**PLAYBOOK.md is confirmed NOT a member of the real, currently-live A2-gated
`canonical_docs.FRESHNESS_FILES` set** — `tests/test_audit.py::test_freshness_includes_hub_only_protocol_docs`
asserts `"protocols/PLAYBOOK.md" not in aud._FRESHNESS_FILES  # deferred, not yet stamped`.
The Done-contract's "surfaces most likely to bite" section states PLAYBOOK is "in the gated
set" for A2 purposes alongside ARCHITECTURE.md — that claim does not hold in this tree for
PLAYBOOK (only for ARCHITECTURE.md); the informational, *ungated* `doctrine_table`/
`derive_doc_freshness` surface above is what actually reads PLAYBOOK's stamp, and it is
advisory, not a commit-blocking FAIL.

## A2 gate handling for the file that IS genuinely gated: ARCHITECTURE.md

`ARCHITECTURE.md` is a real `canonical_docs.FRESHNESS_FILES` member and its `last_reviewed:
2026-09-12` frontmatter predates this lane's edit. Per Done-contract item 6, `last_reviewed`
is bumped to `2026-09-13` in the frontmatter as part of the item-1 commit — with **no** new
blockquote narrative added, since the entire point of the cut is to stop that accretion
mechanism. The bump reflects that this pass re-read the file's structure and prologue
end-to-end for the purpose of this cut; it does not claim a full six-chapter doctrinal
re-read (an honest limit, consistent with every prior `last_reviewed` bump on this file).

## Net effect on the Done-contract

No item's substance changes. Item 3's exact wording ("cut to the frontmatter, the title,
and the Organization paragraph") gains one additional line — a single dateless-history
stamp — because a live test depends on it; this is reported here rather than silently
absorbed, per the decision budget's disclosure duty (Q10).
