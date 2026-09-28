# Landing probe — pre-checked sha, receipt tip, bypass actor, each measured on a throwaway ruleset (LANE-5B4-6, proposal row L0)

carried-by: lane-landing-probe (WAVE5B-N4, repair 1)
date: 2026-09-27
contract: `LANE-5B4-6-landing-probe.md`
authorization: `to-browser/RATIFICATION-2026-09-25.md` R19 (full text in `-v12-superseded.md`) — the lane may create a
temporary ruleset on `automation/landing-probe-**`, throwaway branches on that pattern, run the three probe cases and
the full cycle, and delete both before handback, without a further operator act. Bypass actor: the operator's own
account (`rdwornik`).
basis: `to-browser/PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md` Decision D5, row **L0**
no-consumer: a decision-input measurement for lane-arm-ci (L6), which has not yet filed a backlog row; the choice it feeds is carried as ROWS-OWED below, not a row of its own
method: every mutation below ran as a live `gh api` call (or a real `git push`, called out where it is one) against
`rdwornik/dev-knowledge`, scoped to a ruleset matching only `refs/heads/automation/landing-probe-**`; every commit
pushed is a zero-diff empty commit (no file content, same tree as `origin/main`) built via the Git Data API / local
`git commit-tree` plumbing — no worktree of this lane was ever checked out to build them. Nothing outside the ruleset,
the throwaway branches, and this file was created or changed.

## L0's Done-when, verbatim

> the three cases (pre-checked sha direct push; receipt tip; bypass actor) each have a recorded accept/refuse with the
> `gh api` response; ruleset list back to `[]`

## Before: ruleset list

```
$ gh api repos/rdwornik/dev-knowledge/rulesets
[]
```

## The ruleset (id 24078122, `automation/landing-probe-**` only)

```json
{
  "name": "landing-probe-temp",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["refs/heads/automation/landing-probe-**"], "exclude": [] } },
  "rules": [{
    "type": "required_status_checks",
    "parameters": {
      "strict_required_status_checks_policy": false,
      "do_not_enforce_on_create": false,
      "required_status_checks": [{ "context": "pytest" }, { "context": "ruff" }, { "context": "seal" }]
    }
  }]
}
```

Mirrors `deploy/conductor-required-checks.ruleset.json`'s rule shape (3 contexts), scoped to the throwaway pattern
instead of `main`, `enforcement: active` (the real file ships `disabled` — this one had to be `active` to be
measurable at all). `conductor.yml` does not trigger on `automation/**` (only `main`, `worktree-**`, `epic/**` —
confirmed by reading the file after `lane-ci-matrix` merged, sha `316d3205`), so each case's "pre-checked" state was
produced with the Commit Statuses API directly, standing in for a completed CI run on that exact SHA — the object
under test is the ruleset's own enforcement mechanism, not `conductor.yml`'s contents (L1 already measured that).

## Case 1 — pre-checked sha, direct push: **ACCEPTED**

A commit was created via `POST git/commits` (empty, parent = `origin/main` `316d3205`), then given three green
statuses via `POST statuses/{sha}` (`pytest`, `ruff`, `seal`), then pushed as a new ref:

```
$ gh api -X POST repos/rdwornik/dev-knowledge/git/refs \
    -f ref=refs/heads/automation/landing-probe-1 -f sha=034de8159348d1751578b50227728d2cc5002de7
{"ref":"refs/heads/automation/landing-probe-1", ...,
 "object":{"sha":"034de8159348d1751578b50227728d2cc5002de7","type":"commit", ...}}
```

Exit 0. A SHA carrying all three required statuses is accepted on direct push (ref creation), even though
`do_not_enforce_on_create: false`.

## Case 2 — receipt tip (unchecked), direct push: **REFUSED**

A second commit (parent = case 1's SHA, no status of its own — the receipt-commit shape named in the ADR's Context
§Q1.2: "the receipt commit that follows the merge push is a second unchecked tip") was pushed as a ref update:

```
$ gh api -X PATCH repos/rdwornik/dev-knowledge/git/refs/heads/automation/landing-probe-1 \
    -f sha=e118a05e3554c0f81518ad0c242834a87f8a3ec5 -F force=false
{"message":"Repository rule violations found\n\n3 of 3 required status checks are expected.\n\n",
 "documentation_url":"https://docs.github.com/rest/git/refs#update-a-reference","status":"422"}
```

Exit 1, HTTP 422. **A receipt commit with no status of its own is refused**, even though its parent was fully
checked — GitHub required-status-checks enforce per-SHA, not per-ancestor.

## Case 3 — bypass actor: **ACCEPTED**

The ruleset was updated (`PUT rulesets/24078122`) to add `rdwornik` (actor id `36505769`) as a bypass actor,
`bypass_mode: always` (`current_user_can_bypass` read back as `"always"`). The exact case-2 push (same unchecked SHA,
same command) was retried:

```
$ gh api -X PATCH repos/rdwornik/dev-knowledge/git/refs/heads/automation/landing-probe-1 \
    -f sha=e118a05e3554c0f81518ad0c242834a87f8a3ec5 -F force=false
{"ref":"refs/heads/automation/landing-probe-1", ...,
 "object":{"sha":"e118a05e3554c0f81518ad0c242834a87f8a3ec5", ...}}
```

Exit 0. **A designated bypass actor overrides required status checks entirely** — the identical push that case 2
refused is accepted once the operator's account is the pushing identity and is listed as a bypass actor.

## Item 2 — the full merge → JOURNAL anchor → receipt commit → push cycle

Built as real commit objects (`git commit-tree`, no checkout): a feature leg, a 2-parent merge commit (mirrors
`git merge --no-ff`), a JOURNAL-anchor-shaped commit, and a receipt-shaped commit, stacked in that order, all
zero-diff. The bypass actor was removed first (`PUT` back to the no-bypass ruleset) so this run measured
required-status-checks alone, not bypass.

- The whole 4-commit chain was landed on GitHub via a plain push to a non-branch ref (`refs/probe/...`, outside the
  ruleset's `refs/heads/**` scope — used only to transfer the objects, deleted with everything else below).
- Three green statuses (`pytest`, `ruff`, `seal`) were set on the **receipt tip** (the last commit, not the merge
  commit) — i.e., the whole stack was checked as one unit, the way an integration-branch CI run would check it.
- The receipt tip was then pushed with a real `git push` (not the Git Data API) directly to
  `automation/landing-probe-2`:

```
$ git push origin f7a954213269baa673229b489d78c92c5fe22135:refs/heads/automation/landing-probe-2
 * [new branch]        f7a954213269baa673229b489d78c92c5fe22135 -> automation/landing-probe-2
```

Exit 0. **When the receipt-inclusive tip itself carries the required statuses, the real `git push` of the whole
merge→anchor→receipt stack succeeds directly** — this is the "the receipt can ride inside the checked range" branch
of D5.

## What this measures, against the flip condition

D5's flip condition: *"A4 replaces A7's landing if D5's probe shows a pre-checked sha or the receipt tip cannot be
pushed directly."*

- A pre-checked sha **is** accepted directly (case 1).
- **As `lane-integrate.md:158-174` currently sequences the cycle** (check the merge sha, push, *then* append the
  receipt commit unchecked), the receipt tip **cannot** be pushed directly — case 2 reproduces exactly that shape and
  is refused. Taken alone, this fires the flip condition.
- But the flip condition's own second clause — "the receipt can ride inside the checked range" — **is achievable**:
  item 2 shows that when the check runs on the tip that already includes the receipt commit (not on the merge sha
  alone), the direct push of that tip succeeds via a real `git push`. This means the fix is a **sequencing change**
  in `lane-integrate.md` (check after assembling the receipt, not before), not necessarily a move to PRs.
- The bypass actor (case 3) is a second, independent way to land a push that lacks its own status — orthogonal to
  the sequencing question, and already the mechanism R19 uses for this very lane's own throwaway pushes.

**This lane does not decide between "resequence the receipt-then-check" and "move to PRs" — that choice is
`lane-arm-ci`'s (L6) to make when it arms D3's required contexts on `main`, and the proposal's own operator decision
option 2 (landing preference) names it as functional, not this lane's ruling.** The measured fact this probe owed is:
direct push stays viable in principle, conditional on `lane-integrate.md`'s receipt step moving inside the checked
range; ROWS-OWED below.

## Cleanup: ruleset list back to `[]`, throwaway refs gone

```
$ gh api -X DELETE repos/rdwornik/dev-knowledge/rulesets/24078122 -i
HTTP/2.0 204 No Content
...

$ git push origin --delete automation/landing-probe-1 automation/landing-probe-2
 - [deleted]           automation/landing-probe-1
 - [deleted]           automation/landing-probe-2

$ git push origin --delete refs/probe/landing-probe-rehearsal
 - [deleted]           refs/probe/landing-probe-rehearsal

$ gh api repos/rdwornik/dev-knowledge/rulesets
[]

$ git ls-remote origin 'refs/heads/automation/landing-probe-*'
(empty)

$ git ls-remote origin 'refs/probe/*'
(empty)
```

## What is NOT claimed here

- **`main` and `deploy/conductor-required-checks.ruleset.json` were never touched** — the temporary ruleset only ever
  matched `refs/heads/automation/landing-probe-**`; `gh api repos/rdwornik/dev-knowledge/rulesets` read `[]` both
  before this lane ran and after it finished.
- **No decision is armed by this file.** L0 removes K6 by measuring, not by arming; `lane-arm-ci` (L6) still owns
  arming required checks and choosing PRs vs. direct-push-resequenced on the strength of the finding above.
- **`conductor.yml`'s real CI is not what was exercised.** It does not trigger on `automation/**`; the statuses used
  here were set directly via the Commit Statuses API to isolate the ruleset's own enforcement behavior, which is what
  row L0 asks this lane to measure.

## ROWS-OWED

- `lane-arm-ci` (L6): resequence `lane-integrate.md`'s receipt-commit step to land inside the CI-checked range (push
  the receipt-inclusive tip to the integration branch, check that, then push that same tip directly) as the
  direct-push-preserving alternative to moving landing to PRs — `docs/audits/2026-09-27-technical-landing-probe.md`
  (this file) — runnable check: repeat this file's item-2 rehearsal against the real `pytest`/`ruff`/`seal` contexts
  once `deploy/conductor-required-checks.ruleset.json` is armed.
