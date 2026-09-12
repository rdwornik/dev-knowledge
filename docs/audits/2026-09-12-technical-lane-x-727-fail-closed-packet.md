# LANE `lane-x-727-fail-closed` — end-of-lane packet

> Deny-and-point's three allow-on-failure paths, flipped to refuse instead of permit,
> per AX24-2 (batch X wave 2 GO, F1). `[#727]`'s Done-when carries the fail-posture
> clause and it is now green -- `[#727]` itself stays open, closure is the operator's
> word under AX24-5.
>
> Contract: `LANE-x-727-fail-closed.md` (Google Drive prompt dir).
> Row: `[#727]`. Branch: `worktree-lane-x-727-fail-closed`. Commit-and-STOP; no merge,
> no push to `main`.

## 1 - What changed

Three commits, in contract order (Steps 1-3; step 4 is this packet):

| # | Commit | Step | Surface |
|---|---|---|---|
| 1 | `4de6bf6d` | 1 - Done-when amendment | `tasks/727-*.md` |
| 2 | `3a1fda9e` | 2 - RED-first trip-tests | `tests/test_deny_and_point.py`, `ecosystem/doc-counts.md` |
| 3 | `035db9e0` | 3 - the fix | `scripts/hooks/deny_and_point.py` |

### Step 1 - the Done-when amendment (verbatim, not paraphrased)

Appended to `[#727]`'s Done-when: *"the deny-and-point hook refuses its matched class
when it cannot evaluate (script missing, interpreter missing, crash, unexpected rc),
each refusal naming cause and fix, with a RED-first trip-test per failure mode; the
three allow-on-failure paths are the lane's target and the declared `# raw-needed`
escape stays; `[#727]` does not close until that clause is green."* `BACKLOG.md` needed
no regeneration -- it only projects the row's title and file pointer, not its body.

### Step 2 - four failure modes, RED-first (ADR-108 SS B)

Each asserts BOTH refusal and that the refusal names cause and fix:

| Failure mode | Simulated as | Site (9136f133) |
|---|---|---|
| script missing | `load_processes` raising `ModuleNotFoundError` (the `graph_store` dependency) | L645 |
| interpreter missing | `load_processes` raising `sqlite3.OperationalError` (the store's engine unreachable) | L645 |
| crash | `decide()` raising `RuntimeError` mid-evaluation | L651 |
| unexpected rc | `decide()` returning a verdict outside `{allow, block}` | new check |

Plus the wire-level L660 site (malformed stdin JSON), which the amendment's "cannot
evaluate" language covers directly. A fifth, pre-existing test
(`test_an_unreadable_store_ALLOWS_rather_than_wedging`) turned out to assert against
this **tree's own live, populated store** rather than a simulated absent one, so `rg
gen_task_tree` was legitimately being blocked by real data and the test's own premise
was wrong -- fixed (renamed, now mocks `load_processes` to return `{}`) rather than
left red for the wrong reason. Two confirmation tests were added for clauses 4-5 (the
raw-needed escape and ordinary searching stay unaffected by the flip). Committed
failing, before any production-code change, per ADR-108 SS B. `ecosystem/doc-counts.md`
regenerated in the same commit (`pytest_collected` 6141 -> 6148; a pre-commit gate,
`doc-counts-pytest-freshness`, refuses otherwise).

### Step 3 - the fix

`decide_with_store`'s two `except Exception` blocks and `main()`'s JSON-parse
`except` now return `("block", <cause-and-fix message>)` instead of `("allow", ...)`.
A new `_cannot_evaluate(cause, fix, exc)` helper builds the refusal text, parallel in
spirit to `_pointer()`: it names what went wrong, how to fix the underlying cause, and
the in-session escape (`# raw-needed: <reason>` on a Bash/PowerShell command; the Grep
tool has no comment syntax, so the message says to switch tools). `decide_with_store`
also now refuses if `decide()` ever returns a verdict outside `{"allow", "block"}` --
defensive against a future typo silently reading as permission, since no live code path
produces that today. The module's top docstring's "FAIL POSTURE" section is rewritten
to state the new posture rather than the old one.

**Unchanged, on purpose:** an ABSENT or EMPTY store (`load_processes` returning `{}`
without raising -- a fresh clone, never committed) stays `ALLOW`. That is "not governed
yet", not a failure to evaluate, and clause 2 does not touch it. The declared
`# raw-needed: <reason>` escape and ordinary non-governed searching are both unaffected
(clauses 4-5): neither reaches the fail-closed paths, since the escape and the "not a
search" check both resolve before `load_processes()` is ever called.

## 2 - The disclosed interpretation of "script missing" / "interpreter missing"

The frozen amendment names four failure modes; the contract's own decision budget
pre-decides the footprint as the three named `except` sites in this one module plus
its tests ("which of the three except sites to change (all of them -- clause 2)"),
confirmed independently by the batch X2 manifest GO record ("the three allow-on-failure
paths are the lane's target"). Two readings of "script missing" / "interpreter
missing" exist:

- **In-module (what this lane implements):** a dependency this module's own code needs
  -- the `graph_store` import, the SQLite engine that opens the persisted store --
  becoming unavailable. Testable and closable entirely within `decide_with_store`.
- **At the wrapper (not touched):** `.claude/settings.json`'s shell command around
  `deny_and_point.py` --
  `if [ -f "$G" ]; then python "$G"; else exit 0; fi` -- still exits 0 (allows) if the
  script file itself is missing, and inherits `python`'s own exit code (127 if the
  interpreter is absent) with no wrapper-level cause-and-fix framing, unlike the sibling
  prompts-guard wrapper (AX15-1) it is textually compared to.

This lane implements the first reading only, per the footprint the contract itself
narrowed to. The wrapper-level gap is a residual, not a silent narrowing -- it is named
here for whoever next touches `.claude/settings.json`'s `Bash|PowerShell|Grep` block,
should AX24-2's parity with AX15-1 be read as extending there too. No test in this
lane's file exercises it (the existing `test_the_wired_command_FAILS_OPEN_when_the_
project_dir_is_unset` still asserts the OLD wrapper-level fail-open behaviour and is
unchanged, since the wrapper itself is unchanged).

## 3 - Verification

- `uv run --locked python -m pytest tests/test_deny_and_point.py -n 0 -q` -> **123
  passed** (118 pre-existing + 5 new/updated for this lane's failure modes).
- `uv run --locked ruff check scripts/hooks/deny_and_point.py
  tests/test_deny_and_point.py` -> clean.
- `uv run --locked python scripts/impacted_tests.py select --changed
  scripts/hooks/deny_and_point.py` -> `tests/test_deny_and_point.py` (the changed
  script is covered).
- The file remains pure ASCII (grepped for non-ASCII bytes; none found), preserving the
  module's own cp1252-console invariant.
- The clause-4/5 invariants (raw-needed escape, ordinary searching) are proven by tests
  in the same commit as the fix, not merely assumed to still hold.

Full suite was not run in this lane (targeted-tests-in-lane, full-suite-at-integration
per `AGENTS.md`/`CLAUDE.md` SS4 conventions); the integrator runs it at merge.

## 4 - Environment note (not a code finding)

This machine ran under sustained system-wide memory pressure during this lane (as low
as ~1.5 GB free of ~29 GB, with several concurrent `claude` process trees and at least
one other active worktree lane, `lane-x-734-retire-stage-2`, observed running its own
work in the shared primary checkout). Five consecutive `git commit` attempts for step 2
were killed by the harness for low memory; each killed attempt left an orphaned
`nohup -> uv -> pytest -n 4` process tree behind (the `audit-health` pre-commit hook's
own detached background job, confirmed orphaned by checking that its controlling parent
process had exited). These were identified and terminated between retries once
diagnosed, which is what let step 2's commit eventually land. No repo state was at risk
at any point -- `git status` showed the same staged content across every attempt, and
nothing was committed until a full pre-commit run completed successfully. Recorded here
in case the pattern recurs for a later lane on this machine.

## 5 - Open items

- **Wrapper-level fail-open residual** (SS2 above): `.claude/settings.json`'s
  `Bash|PowerShell|Grep` command still exits 0 on a missing script file or a missing
  interpreter, with no cause-and-fix framing. Not this lane's footprint; flagged for
  whoever next revisits that block.
- **`[#727]` stays OPEN.** Its Done-when's fail-posture clause is now green on this
  branch; closure remains the operator's word under AX24-5 once this lane's commits
  reach `main`.
- No merge, no push, no JOURNAL entry, no index regeneration -- all integrator acts per
  this lane's "What NOT to do".
