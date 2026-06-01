<!-- scope: meta -->

# Retrospective: past commit messages vs the new backlog-id convention (read-only)

> **Read-only — no commit was rewritten, rebased, or re-messaged** (CONTRIBUTING/ADR-65: the index is forward-only; git history is immutable). Branch `docs/backlog-migration-adr64-2026-06-01`, Step 8. Sample: last 60 commits as of `a1cd68e`.

## Findings

| Signal | Last-60 | Reading |
|---|---|---|
| Conventional-commit `type(scope):` prefix | **41/60** | Strong baseline; the misses are merge commits + a marathon-arc cluster using bare-scope subjects (`backlog:`, `lessons:`, `audits:`) instead of a `type` (should be `docs(backlog):` etc.). |
| References an ADR (`ADR-NN`) | **12/60** | The *decision-index* half of the convention is **already in de-facto use** — ADR numbers are the working index for decision work. |
| References a backlog id (`[#N]`) | **0/60** | Expected — ids did not exist before 2026-06-01 (Step 6). The convention starts now; the past is covered by SHAs embedded in retired entries (preserved in the Step-5 JOURNAL map). |

## Assessment

- **ADR refs need no change** — they already work; keep citing `ADR-NN` for decision commits.
- **Backlog-id refs are net-new and forward-only.** This branch's own commits (Steps 0-5) predate the ids (assigned in Step 6), so they do **not** carry `[#id]` — correct, not a defect. From the *next* session onward, a commit that closes a backlog item should carry `closes [#N]`, and one that advances an item `[#N]`.
- **Minor historical style drift** (bare-scope marathon-arc subjects) is **left as-is** — rewriting immutable history is forbidden (ADR-65); the now-explicit CONTRIBUTING convention prevents recurrence going forward.

## Where the convention pays off (going forward)

- `git log --grep 'closes \[#N\]'` locates the closing commit for retired item N without embedding a SHA in the entry — exactly the forward-index ADR-65 specifies.
- A removed backlog item is reconstructable from (a) the `closes [#N]` commit and (b) `git revert` of the removal — two independent paths, no archive file.
- Pairs with the validator's `id:`-required rule: every live item has a stable handle a future commit can reference.

## Constraints honored

- No `git rebase`, no `--amend`, no `filter-branch`, no re-message — purely a read of `git log`.
- No backlog item edited in this step.
