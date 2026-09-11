# LANE lane-w-684-pretooluse-guard-root — W-2 prime - the PreToolUse prompts guard fails closed and loud whenever it cannot evaluate

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `interactive` — this lane RESUMES an existing branch, so it is not started by
`Dispatch-Lane`.

```
Read <PROMPTS_DIR>\LANE-w-684-pretooluse-guard-root-prime.md and execute it exactly.
```

**Why not `Dispatch-Lane`, and why that is not a workaround.** AX15-3 rules that W-2'
**continues on the W-2 branch**. `worktree-lane-w-684-pretooluse-guard-root` and its
worktree already exist and carry eleven commits of review work.
`Dispatch-Lane`/`Start-DispatchLane` **refuse outright when the branch exists** — that
refusal is correct behaviour (a re-run must be a no-op, not a collision), so it cannot be
argued around. The verb set has **no resume mode**; that gap is recorded as a dispatcher
finding in this batch's manifest rather than worked around silently. Giving this lane a
fresh branch instead would contradict AX15-3 and strand the eleven commits.

**How it is started.** A background session is launched **with its working directory set
to the existing worktree**, and given the line above verbatim:

```
git worktree add .claude/worktrees/lane-w-684-pretooluse-guard-root worktree-lane-w-684-pretooluse-guard-root
cwd: .claude/worktrees/lane-w-684-pretooluse-guard-root
claude --bg --model opus --effort high --permission-mode bypassPermissions
```

**The worktree must be RE-ATTACHED first — it no longer exists.** Measured 2026-09-11 after
the freeze: the integrator closed batch W and removed
`.claude/worktrees/lane-w-684-pretooluse-guard-root`. The BRANCH
`worktree-lane-w-684-pretooluse-guard-root` is intact, **11 commits ahead of `main`, and is
NOT pushed to origin** — so those eleven commits exist in exactly one place, this clone.
AX15-3 is unaffected: it named the branch, and the branch is what survived. `git worktree add`
onto an EXISTING branch re-attaches rather than creating, which is why this is a re-attach and
not a provision.

Dispatch constants ride unchanged (`--permission-mode bypassPermissions`, `--bg`, the
board label `[.dev-knowledge · #684 · lane-w-684-pretooluse-guard-root]`). The model is
**explicit on the line** (`--model opus`), which is what AX7-5 asks for and what the
`local` shape's fence cannot express until `[#717]` lands.

**Step 0 for this lane is RE-ATTACH, then sync — not a provision.** The branch is eleven
commits ahead of `main` and `main` has moved under it (batch W closed, X-0 landed).
Re-attach the worktree with the line above, then `git fetch origin` and merge `main`,
before touching the guard. Do NOT create a new branch: that would strand the eleven
commits, which exist only in this clone.

## Worktree pairing

slug `lane-w-684-pretooluse-guard-root` -> contract `LANE-w-684-pretooluse-guard-root-prime.md`

This contract **creates no branch**, which is why the pairing above names none: the branch
`worktree-lane-w-684-pretooluse-guard-root` and its worktree ALREADY EXIST, carrying the
eleven commits of W-2 review work this lane continues (AX15-3). The 1:1 rule still holds in
substance — one lane, one contract file, one branch — but the branch is INHERITED rather
than provisioned, and a contract that named it as its own would claim an act it does not perform.

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The `PreToolUse` prompts-guard **FAILS CLOSED** for the matched class (filesystem-touching tools — the narrowed matcher STAYS) on every inability to evaluate: script missing, interpreter missing, crash, any rc other than 0. The refusal text NAMES the cause and the fix. A SessionStart check verifies interpreter + guard script once and reports loudly, so per-call refusals are the exception rather than the norm.
2. Two RED-first trip-tests, one per failure mode (script removed -> refused with message; interpreter broken -> refused with message); the M7 smoke still passes (a non-Claude CLI call is NOT refused); and a FRESH Codex review with **no unresolved HIGH** — the prior review returned HIGH:2, both fail-open, which is why W-2 was CARRIED. Per AX15-2 the hook and `scripts/fleet_health.py` ship together as ONE floor component; a consumer with the hook and without the script is a deploy defect caught by `fleet_parity`, not a silent permit.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md` (batch X wave 1 first set + the deletion lane), as amended by `to-cc/AMEND-BATCH-X-ROSTER-014.md` AX14-1 (fill to 6) and `-015.md` AX15-3 (slot 6 = W-2'). The GO covers every roster lane; no lane outside the roster fires on it (AX14-3).

AX12-1 binds this contract: the row's Done-when is carried **verbatim**, and so is every AX clause addressed to it, quoted with its AX id. This lane's FIRST COMMIT writes these clauses into its own row (the AW-2 / `[#680]` pattern) — nothing here stays SAID. Where a clause names a row this lane did not file, the lane files the clause against its own row and reports the untouched one in its end packet rather than editing a row it does not own.


### Row `[#684]` — Done-when, verbatim

> Done when: one non-Claude CLI smoke passes under the guard, a RED-first test fails when the fallback is removed


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX9-4` — verbatim

> - **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".


### `AX15-1` — verbatim

> - **AX15-1 · Guard design (technical ruling):** the PreToolUse prompts-guard FAILS CLOSED for the matched class (filesystem-touching tools — the narrowed matcher stays) whenever it cannot evaluate: script missing, interpreter missing, crash, any rc other than 0. The refusal text names the cause and the fix (the operator's rule: a deviation raises an exception that teaches). A SessionStart check verifies interpreter + guard script once and reports loudly, so per-call refusals are the exception. Rationale: a guard that permits when it cannot run is declared enforcement without enforcement.


### `AX15-2` — verbatim

> - **AX15-2 · Floor coupling:** the hook and `scripts/fleet_health.py` (its guard entry point) ship together as one floor component (AX4-1); a consumer with the hook and without the script is a deploy defect caught by `fleet_parity`, not a silent permit.


### `AX15-3` — verbatim

> - **AX15-3 · Lane W-2′ in the first set, slot 6** (replaces AX14-1's slot-6 interim): continues on the W-2 branch; Done-when = `[#684]`'s own + RED-first trip-tests for both failure modes (script removed → refused with message; interpreter broken → refused with message) + the M7 smoke still passes (a non-Claude CLI call is not refused) + a fresh Codex review with no unresolved HIGH. On merge it unblocks AX8-1 (read-only work to agy) and X1-4 routing.

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

1. Step 0 is a SYNC, not a provision — this worktree exists and is 11 commits ahead while `main` has moved under it (batch W closed, X-0 landed). `git fetch origin` then merge `main`. **COMMIT**
2. RED-first: both failure-mode trip-tests, FAILING against today's fail-open guard. **COMMIT**
3. Make the guard fail closed for the matched class; refusal text names cause and fix. **COMMIT**
4. SessionStart interpreter+script check; floor coupling with `fleet_health` per AX15-2. **COMMIT**
5. M7 smoke re-run + a FRESH Codex review; no unresolved HIGH. **COMMIT, then STOP.**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Step 0 — sync before anything else (MANDATORY until `[#716]` lands)

`[#716]` is open: `worktree.baseRef` is unset, so this lane branches from `origin/main`
and may start behind local `main`. **The step-0 sync is mandatory and may not be dropped
on the grounds that `[#716]` is being fixed** — it is retired only by the change that
makes that row's test green. A generator run against a base that lags `main` silently
DROPS rows that exist on `main`, and the dropped row looks like a clean regeneration.

```
git fetch origin
git merge origin/main        # or: git merge main, from the primary's ref
uv run --locked python -c "print('base synced')"
```

Then, and only then, run the lane's own steps.
