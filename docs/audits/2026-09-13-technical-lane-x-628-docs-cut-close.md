# lane-x-628-docs-cut — close artifact

Executes `LANE-x-628-docs-cut.md` (items 1, 4, 5 of `[#628]`'s docs-cut list; batch X wave 4).
Reader census: `docs/audits/2026-09-13-census-lane-x-628-reader-census.md`. Four commits, one
per Steps 1-4 of the frozen contract.

## Cuts, before/after bytes

| Target | Before | After | Delta | Commit |
|---|---|---|---|---|
| `ARCHITECTURE.md` (whole file; the cut section was lines 17-259) | 129,213 B | 100,800 B | -28,413 B | `720ecce6` |
| `protocols/PLAYBOOK.md` (whole file; the cut section was lines 7-96, +1 stamp line added) | 506,729 B | 499,943 B | -6,786 B | `c981e9e8` |
| `scripts/canonical_docs.py` (registry retirement, not a size-driven cut) | 18,697 B | 19,140 B | +443 B (rationale comments) | `6d3afbcb` |

`protocols/ESSENTIALS.md` itself: byte-identical, 16,461 B, unedited (`git diff --stat
c0e0722f HEAD -- protocols/ESSENTIALS.md` is empty). Retirement means the four
`canonical_docs.py` registries (`CANONICAL_OPTIONAL`, `FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`,
`STRUCTURE_DOCS`) stop treating it as live; the file's disposition beyond that is `[#628]`'s
fleet-coupled deletion act, executed later by `[#667]`, not this lane's.

`CLAUDE.md` is untouched (0 diff) — Item 3 was out of contract (NO-GO, 2 live readers) and
`tests/test_claude_md_byte_cap.py`'s declared cap did not move, as expected.

## Reader census that licensed each cut

Full detail: `docs/audits/2026-09-13-census-lane-x-628-reader-census.md`. Summary:

- **ARCHITECTURE.md's prologue:** zero readers on the deleted prose (chained dated-history
  blockquote); the surviving "How to read this doc" guide is the one part any session persona
  is routed to. Frontmatter (`last_reviewed`, `reconciled_with`) untouched in shape; `last_reviewed`
  bumped 2026-09-12 → 2026-09-13 per the A2 gate (Done-contract item 6) since ARCHITECTURE.md is
  a genuine `canonical_docs.FRESHNESS_FILES` member and this is a content edit.
- **PLAYBOOK.md's prologue:** zero readers on the deleted narrative; `reconciled_with:` (3 live
  readers) sits above the cut and is untouched. **One reader the 2026-09-13 manifest census
  missed, found mid-cut (Done-contract item 5's class (b)):** the prose `> **Last updated:**`
  line is a live `SURFACE_PROSE` read (`audit.py::parse_declared_freshness`/`doctrine_table`),
  pinned by `tests/test_canonical_docs.py`'s `@pytest.mark.live_repo` doctrine-row test. A bare
  3-survivor cut (frontmatter/title/Organization only) flips that test's `row.surface` from
  `'prose'` to `'none'` — confirmed by running it red before the fix. The cut therefore keeps
  one single, non-narrative stamp line dated today, matching the file's own established
  mechanism ("the stamp line moves with the last edit rather than being written once at the top
  of the lane") applied once, not restarted as a new accretion chain. PLAYBOOK.md is confirmed
  NOT a member of the real A2-gated `FRESHNESS_FILES` (`tests/test_audit.py::test_freshness_includes_hub_only_protocol_docs`
  — "deferred, not yet stamped"), so no A2 hard-block applies to it; only the ungated,
  informational `doctrine_table` surface does, and it is now correctly `CLASS_UNGATED_FRESH`.
- **ESSENTIALS.md:** exactly four `canonical_docs.py` registry memberships were live
  (`CANONICAL_OPTIONAL`, `FRESHNESS_FILES`, `SECTION_HISTORY_DOCS`, `STRUCTURE_DOCS`) plus the
  derived fallback literal in `canonical_freshness_gate.py`, all now retired together.
  `CONFORMANCE_V2_SCAN` had already dropped it (own comment, pending `[#628]`) — confirmed out
  of this lane's footprint, not re-touched.

## Targeted tests

`uv run --locked pytest tests/test_canonical_docs.py tests/test_canonical_freshness_gate.py
tests/test_audit.py tests/test_validate_doc_rot.py tests/test_validate_doc_structure.py
tests/test_validate_hermetization.py tests/test_validate_substrate.py
tests/test_claude_md_byte_cap.py tests/test_toc.py` — **540 passed, 4 failed.** All four
failures are **pre-existing and unrelated to this lane's diff**, confirmed by reproducing three
of them against a HEAD-swapped (unedited) `canonical_docs.py` before committing Step 4, and by
inspection for the other two (they concern other fleet repos' settings/command rosters and
filenames introduced by the concurrent `docs/batch-x3-close-packet` merge this lane synced past,
not any file this lane's contract names):

- `tests/test_toc.py::test_corpus_fence_fix_never_drops_a_header_from_OUTSIDE_a_code_block` —
  corpus glob returns 0 files; reproduces on HEAD's `canonical_docs.py`.
- `tests/test_validate_doc_rot.py::test_citation_regex_strips_only_real_dated_artifact_identifiers`
  — false-strips against handoff-bundle filenames unrelated to this diff.
- `tests/test_canonical_docs.py::test_the_derived_leg_is_warn_class_on_arrival` — isolated
  fixture-repo test, fails identically against HEAD's `canonical_docs.py` before this lane's
  edit (verified directly: copied the working edit aside, ran the test against
  `git show HEAD:scripts/canonical_docs.py`, same failure, restored the edit).
- `tests/test_audit.py::test_check_fleet_parity_green_on_live_repo` — WARN-undeclared findings
  against `ai-council` and `corp-monorepo`'s own settings/command rosters, and this repo's
  `conductor.py` SessionStart hook — none of the three files this lane's contract names.

Not fixed here: out of this lane's declared footprint.

## A hazard from the contract that fired, handled per its own prescription

`graph-rebuild`'s stated non-concurrency-safety, plus a self-inflicted compounding factor: a
`git commit` was twice run in the background while file edits continued in the same turn,
racing pre-commit's own stash/restore of unstaged changes. The first race silently reverted an
in-progress `canonical_docs.py` edit to HEAD before a second edit landed on top of it (caught
immediately by grep before committing anything wrong); the second stalled the whole pre-commit
chain at the `[#664]` decision-coverage hook for several minutes with the working tree still
stashed. Recovered by `TaskStop`-ing the hung process, verifying nothing else changed
(`git status`), and recovering the stashed edits directly from pre-commit's own patch file in
`~/.cache/pre-commit/` (`git apply --check` then `git apply`) rather than re-deriving them from
memory. From that point on, every commit in this lane ran in the foreground with no concurrent
file edits. A separate, later commit attempt also hit a **real** `audit-health` FAIL —
`journal_spine_anchor` reporting this worktree's branch behind `main`'s first-parent spine after
the concurrent `docs/batch-x3-close-packet` merge landed — confirmed as tree-lag rather than a
genuine gap via the audit's own prescribed `journal_anchor.is_anchored` diagnostic (`False` in
this tree, `True` at `main`), fixed by `git merge main` (a clean fast-forward, zero file overlap
with this lane's footprint), not by touching the anchor.

## Compliance with the frozen contract

- No merges to `main`, no pushes, no touching another lane's branch — this lane's only merge was
  pulling `main` into its own branch to clear a tree-lag false gate, per the contract's own
  reader-verification discipline (a live gate result is evidence, and its cause was checked
  before acting).
- No JOURNAL entry (integrator's surface, `STANDING_RULINGS.md` P-1).
- No index regeneration.
- No edits outside the declared footprint: `ARCHITECTURE.md`, `protocols/PLAYBOOK.md`,
  `scripts/canonical_docs.py`, `scripts/canonical_freshness_gate.py`,
  `tests/test_audit.py`, `tests/test_canonical_freshness_gate.py`, and this lane's own
  `docs/audits/` census + close artifacts.
- `git stash list` empty at STOP.

**Decision-budget disclosure (Q10):** one deviation from the contract's literal wording is
reported per the decision budget rather than asked, since it falls outside classes (a)/(b)/(c)
and this batch runs with no mid-run operator contact (AX27-1): PLAYBOOK's surviving prologue
carries one stamp line beyond the contract's named three (frontmatter/title/Organization),
because a live test discovered mid-cut depends on it (Done-contract item 5's own anticipated
scenario). No premise was refuted; nothing else deviates.
