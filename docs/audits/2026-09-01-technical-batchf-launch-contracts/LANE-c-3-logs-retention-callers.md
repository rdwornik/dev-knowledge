# LANE lane-c-3-logs-retention-callers — re-point the three PROPOSALS globbers at bucketed paths, then retire the retention exemption that makes the rule a no-op

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-c-3-logs-retention-callers LANE-c-3-logs-retention-callers.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-c-3-logs-retention-callers · lane-c-3-logs-retention-callers]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `sonnet`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-c-3-logs-retention-callers` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-c-3-logs-retention-callers` -> branch `worktree-lane-c-3-logs-retention-callers` -> contract `LANE-c-3-logs-retention-callers.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `scripts/logs_retention.py`
- `scripts/propose_closures.py`
- `scripts/review_closures.py`
- `tests/test_logs_retention.py`
- `tests/test_propose_closures.py`
- `tests/test_review_closures.py`

## Done-contract (immutable)

1. **All three flat globbers resolve a BUCKETED path as well as a flat one**, with a test per
   caller: `propose_closures.py:302` (`find_last_proposals_head`), `:341` (`resolve_window`) and
   `review_closures.py:199` (`latest_proposals`) — each currently
   `logs_dir.glob("PROPOSALS-*.md")`, non-recursive.
2. **The two prefix exemptions are REMOVED** from `logs_retention.py:71`
   `EXCLUDED_NAME_PREFIXES`, with its fire-test updated, and a live run RELOCATES the accumulated
   files. `logs/TOKEN-LOG.md` stays excluded ABSOLUTELY (ADR-29/39) — that exclusion is not this
   lane's to touch.
3. **Before/after counts are recorded** — how many files sat flat in `logs/` and how many are
   bucketed after — because the row's whole finding is that the mechanism's dry run is a NO-OP.
   `git status` clean afterwards.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Re-point the three callers FIRST and prove them green. The row states this sequencing risk
   itself: retiring the exemption before the callers resolve buckets breaks the closure loop the
   moment files move. **COMMIT**
2. Retire `EXCLUDED_NAME_PREFIXES`' two prefixes and update the fire-test. **COMMIT**
3. Run the relocation live; record before/after counts. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
