# Codex sol adversarial pass over the handback organ (LANE-W4B-2, Done-contract 6)

> **Status:** record. Lane `lane-handback-organ`, branch `worktree-lane-handback-organ`. Carrier: LANE-W4B-2. This is the
> adversarial pass on `scripts/handback.py` / `scripts/handback_schema.py`, which the contract names as the new TRUST
> BOUNDARY (every lane's handback goes through it); the terra diff review is `2026-09-22-codex-lane-handback-organ.md`.

**Consumer:** `[#958]` — the row this review served (Wave 4b lane 2, `lane-handback-organ`): its Done-when item 6 requires
"Codex sol adversarial pass on the organ ... plus the terra review, both with consumer cited", and this file is that pass.

## How it was run

```
codex exec -m gpt-5.6-sol -o codex-sol-last.txt - < adversarial-prompt.txt
```

`--base origin/main` could not be combined with a custom prompt (`codex exec review` refuses `--base` together with a
`[PROMPT]` argument); the prompt instead told sol to run `git diff origin/main..HEAD -- scripts/handback.py
scripts/handback_schema.py tests/test_handback.py tests/test_handback_schema.py` itself before reviewing. Requested
model: `gpt-5.6-sol`. Exit 0; stdin was the prompt file, never a TTY.

**Prompt:** told sol the organ is the new trust boundary and to attack it as an adversary: find a way a lane could get a
mergeable HANDBACK line, a clean LANE-END report, or a passing self-check written to the transport WITHOUT actually
satisfying branch purity, a clean ship-gate delta, the ratchet, review-consumer citation, or branch-naming conformance —
naming TOCTOU, starved/short-circuited checks, fail-open exception paths, a `validate()` that accepts what `render()`/
`parse()` would reject, ambiguous subprocess/timeout exit codes, and anything that could corrupt the append-only
`SESSION-<lane>.md`. Required file:line, severity, and an explicit "none found" at any empty severity.

## The findings, verbatim

**CRITICAL `scripts/handback.py:320` — branch purity cannot prove commits belong to the lane.** `branch_purity_check()`
examines only multi-parent commits and accepts every ordinary single-parent commit. A lane can rebase/cherry-pick foreign
commits, or fast-forward onto foreign history, and still receive a passing branch-purity result.

**CRITICAL `scripts/handback.py:356` — checks and emitted artifacts do not attest one immutable repository snapshot.** The
changed-file list and checks run first, the report is generated later, and `HEAD` is resolved again at line 380; nothing
prevents commits, ref movement, or worktree changes between these operations. An attacker can let checks pass on one
state, mutate the repository, and have the HANDBACK and LANE-END artifacts describe a different, unchecked state.

**CRITICAL `scripts/handback.py:243` — supplied branch name is never tied to the checked-out branch.** Branch-naming
conformance validates only the caller-controlled `--branch` string, while all repository checks operate on `HEAD`. A lane
on a forbidden or unrelated branch can supply a conforming name and receive a mergeable HANDBACK falsely naming that
conforming branch.

**CRITICAL `scripts/handback.py:222` — review-consumer checking fails open when the changed-file inventory is
incomplete.** Absence of an audit in `changed` is treated as proof that no review artifact exists. The supplied list comes
from `_tr.changed_files()` at line 356, whose helper returns an empty list on Git failure/timeout and caps results. A lane
can hide an undeclared review artifact beyond the cap, or induce an ambiguous Git result, and the organ reports "no new
docs/audits artifact" before emitting a mergeable handback.

**CRITICAL `scripts/handback.py:151` — ship-gate delta collapses findings to check names.** The comparison uses
`head - baseline` over `check_name` values only. If `origin/main` already has one finding from check X, the lane may add
more or worsen that same check and X remains classified as entirely pre-existing.

**HIGH `scripts/handback.py:363` — a clean LANE-END artifact is published before final handback validation.**
`transport_report` writes/replaces `LANE-END-<lane>.md` before the HANDBACK and STATE objects are validated and before
the session append succeeds. Later failures return `EXIT_INTERNAL` without retracting or invalidating that report.

**HIGH `scripts/handback.py:282` — lane-derived session paths lack containment validation.** `session_path()` interpolates
the unvalidated `lane` directly into a filesystem path. Values containing path separators or `..` can redirect the append
outside `to-browser`, potentially corrupting another append-only session or Markdown file.

**HIGH `scripts/handback.py:291` — session appends are neither locked nor transactionally verified.** The session block is
appended with a plain text handle, with no inter-process lock, atomic append protocol, durable flush, or read-back
verification. Concurrent lane/organ writes can interleave or be partially persisted while the organ reports success.

**MEDIUM.** No additional medium-severity findings; trust-boundary defects above have runtime/integrity impact and are
ranked Critical or High.

**LOW.** No low-severity findings.

## Dispositions (recorded by the lane)

Every claim was checked against the tree before it was accepted or dispositioned. Five fixed, one accepted-and-fixed
partially (the report-ordering leg of the TOCTOU finding), two dispositioned as honest limits matching the rule as
written or the existing house convention — recorded, not silently dropped.

| # | Verdict | What was done | Commit | Witness |
|---|---|---|---|---|
| Branch purity (cherry-pick/rebase) | DISPOSITION — honest limit | Matches WAVE4B-COMMON rule 2 as written ("`origin/main..HEAD` holds only this lane's own commits and merges of `origin/main`"); distinguishing a cherry-picked/rebased commit from the lane's own needs a commit-provenance mechanism this contract does not ask for and this lane does not invent | — | module docstring, this file |
| TOCTOU (checks vs. published snapshot) | ACCEPT — fixed | HEAD is resolved ONCE at the top of `run()`, used for the HANDBACK line, and re-verified immediately before publish; a moved HEAD refuses with a `head-pinned` check naming the drift | `f5b790c0` | `test_head_moving_between_checks_and_publish_refuses_rather_than_publishing` (shown red under a mutation) |
| `--branch` not tied to checked-out branch | ACCEPT — fixed | `branch_naming_check(branch, repo)` cross-checks `--branch` against `git rev-parse --abbrev-ref HEAD` when a real repo is given; a mismatch refuses | `f5b790c0` | `test_branch_naming_check_with_repo_flags_a_mismatch_against_the_checked_out_branch` (real git) |
| review-consumer fails open on an incomplete changed-file list | ACCEPT — fixed | New `changed_files_or_raise(repo, base)` fails CLOSED (raises `ChangedFilesUnknown`) instead of `_tr.changed_files()`'s best-effort `[]`; `run_self_check` turns that into a failing `review-consumer` leg | `f5b790c0` | `test_changed_files_or_raise_raises_rather_than_returning_empty_on_git_failure`, `test_run_self_check_turns_an_unresolvable_changed_files_into_a_failing_review_consumer_leg` |
| ship-gate delta by check name only | DISPOSITION — matches the composed tool's own grain | `audit.py ship-gate`'s own human-facing report is organized by check/organ name (`"N hard-fail organ(s)"`); this organ's own docstring commits to "cannot drift from what `audit.py ship-gate` would print" — a finer-grained diff would be a second, independently-drifting notion of ship-gate the organ does not own | — | `scripts/handback.py` ship-gate leg docstring, this file |
| LANE-END published before HANDBACK/STATE validate | ACCEPT — fixed | `run()` reordered: `HandbackLine`/`StateLine` are constructed and validated BEFORE `transport_report.main()` is ever called; a validation failure now writes no report at all | `f5b790c0` | `test_a_malformed_handback_line_writes_no_lane_end_report` |
| `session_path()` lacks containment validation | ACCEPT — fixed | `run()` validates `lane` against `transport_report._LANE_RE` (the same slug-safety regex `transport_report.main()` already enforces for its own paths) before ANY path is built, including the REFUSED-<lane>.md path | `f5b790c0` | `test_a_lane_slug_with_a_path_separator_is_refused_before_any_path_is_built` |
| session appends lack a lock / atomic verify | DEFER | A real fix (exclusive lock, atomic replace-and-verify) is a bigger design change than this Done-contract's scope and the append target predates this organ (`lane_end_guard.py`'s own consumption of "the last HANDBACK-shaped line"); filed for a future lane rather than hand-rolled here under time pressure | — | this file (residual, stated below) |

**Residual, stated.** The append-only session file itself still has no lock or symlink containment beyond the lane-slug
check above; a concurrent writer to the SAME session file could still interleave. This organ narrows the blast radius (a
bad `lane` string can no longer redirect the write) but does not add locking. A lane that hand-writes a HANDBACK line
into its own session file BEFORE ever running this organ, then lets the organ refuse, still leaves that hand-written line
as the "last HANDBACK-shaped line" `lane_end_guard.py` reads — a pre-existing trust assumption in `lane_end_guard.py`
this organ does not change (see the terra review's parallel finding and its disposition).
