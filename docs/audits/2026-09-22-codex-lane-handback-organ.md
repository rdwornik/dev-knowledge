# Codex Review — lane-handback-organ

**Date:** 2026-09-22
**Branch:** `worktree-lane-handback-organ`
**HEAD:** `f5b790c0`
**Diff range:** `origin/main..worktree-lane-handback-organ`
**Codex version:** codex-cli 0.155.0
**Mode:** review (diff computed by the model, `--base`/custom-prompt combination is refused by `codex exec review`)
**Tally:** 4/6/0/0 <!-- Critical/High/Medium/Low, counted from the Findings section below. -->

**Consumer:** `[#958]` — the row this review served (Wave 4b lane 2, `lane-handback-organ`): its Done-when item 6 requires
the terra review of the handback organ alongside the sol adversarial pass (`2026-09-22-codex-lane-handback-organ-sol-adversary.md`).

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- `scripts/handback.py` / `scripts/handback_schema.py`: the new handback organ, the trust boundary every lane's
  handback goes through — self-check integrity, artifact publication ordering, path/lane-slug handling.
- `scripts/handback_schema.py`: the HANDBACK/STATE/LANE-END/REFUSED schema and its round-trip guarantee against
  `audit.py handback`.

## Findings

### Critical

1. **`scripts/handback.py:96` — Branch-purity check accepts foreign commits that were linearized.** The check only
   rejects merge commits with a non-base second parent; a lane can cherry-pick, rebase, or otherwise linearize another
   lane's commits and pass. Produces a mergeable HANDBACK despite violating the stated "only this lane's own commits"
   purity rule.
2. **`scripts/handback.py:347` — Caller-controlled `--base` can neutralize purity and ship-gate comparison.** `--base`
   was accepted verbatim for both `base..HEAD` and the ship-gate baseline; `--base HEAD` makes purity empty and makes
   any current ship-gate failures baseline failures. A lane could obtain a passing self-check for an impure or
   ship-gate-failing HEAD.
3. **`scripts/handback.py:357` — Checks were not bound to the commit later handed back.** The checks ran against moving
   `HEAD`, but the SHA was fetched only after report generation and all checks. A concurrent/local `HEAD` change could
   cause the organ to append a mergeable HANDBACK for an unchecked commit (TOCTOU).
4. **`scripts/handback.py:360` — A refused run leaves pre-existing manually written HANDBACK lines live.** On failure,
   the organ writes only a refusal and does not inspect, invalidate, or supersede an existing session HANDBACK.
   `lane_end_guard` consumes the last session HANDBACK line. A lane can manually append a valid HANDBACK first, run
   this organ knowing it will refuse, and still trigger a lane-end flow from the pre-existing line.

### High

1. **`scripts/handback.py:243` — Branch-naming validates an asserted string, not the checked-out branch.** No equality
   check tied `--branch` to the repository's actual `HEAD`.
2. **`scripts/handback.py:363` — Clean LANE-END report was written before final artifact validation.** A malformed
   code-review argument left a delivered report while the organ returned internal failure.
3. **`scripts/handback.py:286` — SESSION file append follows symlinks and is neither atomic nor verified.**
   `append_session_block()` opened the existing `SESSION-<lane>.md` directly for append, with no resolved-path
   containment check, lock, atomic replacement, or read-back.
4. **`scripts/handback.py:257` — Transport-write check can be bypassed by content, nesting, or timing.** The check only
   scans immediate `to-cc` filenames containing the lane string; it ignores contents, nested paths, differently named
   files, and writes made after the scan.
5. **`scripts/handback_schema.py:254` — LANE-END schema validates a minimal forged "clean" report.**
   `LaneEndReport.validate()` requires only a heading and an enum verdict, despite the schema claiming a Commits
   section and rendering Changed files, Session summary, and Receipts.
6. **`scripts/handback_schema.py:97` — `parse().validate()` could accept raw input the raw validator rejects.**
   `HandbackLine.parse()` collapsed duplicate review tokens to `reviewer=None`; rendering that parsed object could turn
   an invalid raw line (duplicate `review=` tokens) into a valid no-review docs-only line — a lossy round-trip that
   could bless malformed transport input if any consumer used `parse().validate()` rather than `validate_handback_line()`.

No additional Medium findings.
No additional Low findings.

## Dispositions (recorded by the lane)

| # | Verdict | What was done | Commit | Witness |
|---|---|---|---|---|
| Critical 1 (linearized foreign commits) | DISPOSITION — honest limit, converges with sol | Matches WAVE4B-COMMON rule 2 as written; no commit-provenance mechanism is in scope for this contract | — | sol-adversary file's parallel disposition |
| Critical 2 (`--base` caller-controlled) | ACCEPT — fixed | `--base` is no longer a CLI flag; a real invocation only ever gets `DEFAULT_BASE = "origin/main"`. `base` stays a `run()`/check-function parameter reachable only from tests/the Python API | `f5b790c0` | `test_the_cli_does_not_expose_a_base_override` |
| Critical 3 (TOCTOU) | ACCEPT — fixed | HEAD pinned once, re-verified before publish, converges with sol's parallel finding | `f5b790c0` | `test_head_moving_between_checks_and_publish_refuses_rather_than_publishing` |
| Critical 4 (stale manual HANDBACK on refusal) | DISPOSITION — pre-existing trust model, out of this contract's scope | `lane_end_guard.py`'s "last HANDBACK-shaped line" trust model predates this organ; a lane could always hand-write a fake line before this organ existed. This organ centralizes WRITING a HANDBACK line, it was never scoped to cryptographically seal the session file against hand-edits made outside it. Filed as residual, not fixed under this contract | — | this file (residual, stated below) |
| High 1 (branch-naming vs. checked-out branch) | ACCEPT — fixed, converges with sol | `branch_naming_check(branch, repo)` cross-check | `f5b790c0` | `test_branch_naming_check_with_repo_flags_a_mismatch_against_the_checked_out_branch` |
| High 2 (report before validation) | ACCEPT — fixed, converges with sol | `run()` reordered: HANDBACK/STATE validate before the report is written | `f5b790c0` | `test_a_malformed_handback_line_writes_no_lane_end_report` |
| High 3 (session append: symlink/lock/verify) | PARTIAL — lane-slug containment fixed; lock/atomic-verify DEFERRED | `lane` is validated against `transport_report._LANE_RE` before any path is built (closes the path-redirection half); no lock or read-back verification was added — a bigger design change than this Done-contract's scope, filed for a future lane | `f5b790c0` | `test_a_lane_slug_with_a_path_separator_is_refused_before_any_path_is_built`; residual below |
| High 4 (transport-write filename-only) | DISPOSITION — matches house convention | Filename-based matching is the existing convention this check composes into (WAVE4B-COMMON rule 3's own wording: "carries nothing naming this lane"); content/nesting/timing hardening is a scope expansion beyond what this leg was asked to check | — | this file |
| High 5 (LaneEndReport under-validates) | DEFER | Strengthening `validate()` to require all sections needs `LaneEndReport.parse()` to preserve "section absent" vs. "section present, empty" — a change to a dataclass field `lane_digest.py` and other consumers already read, so it is deferred rather than risked under this lane's diff budget | — | this file |
| High 6 (duplicate review= tokens round-trip) | ACCEPT — fixed | `HandbackLine.parse()` now returns `None` (refuses to parse) on >1 `review=` token instead of collapsing to `reviewer=None`, matching `audit.review_handback_verdict`'s own refusal | `f5b790c0` | `test_handback_line_parse_rejects_ambiguous_duplicate_review_tokens` |

**Residual, stated.** Two items are DEFERRED rather than fixed: session-append locking/atomic-verify (High 3, partial),
and `LaneEndReport.validate()`'s section-completeness (High 5). Both are real hardening opportunities that this lane's
Done-contract does not require and that risk a wider blast radius (a shared append path; a schema field several
consumers already read) than this diff should carry. Filed here rather than silently dropped, per the fixed-file
disposition convention this repo requires. Critical 4 (a lane bypassing the organ entirely by hand-writing a session
line) is a pre-existing `lane_end_guard.py` trust assumption this organ was never scoped to close.
