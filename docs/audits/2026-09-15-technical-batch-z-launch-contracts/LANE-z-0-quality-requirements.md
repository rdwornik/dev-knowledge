# LANE lane-z-0-quality-requirements -- Create ecosystem/quality-requirements.yaml as a registered artifact, render it into ONE ARCHITECTURE section, and declare it floor MUST

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` -- a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-z-0-quality-requirements "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-z-0-quality-requirements.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-z-0-quality-requirements.md` **from the target repo root** -- the ruled verb for a local
lane (PLAYBOOK Ch8's dispatch table, the sole literal-command site). The verb
reads this `## Dispatch` block and runs it **verbatim**, substituting exactly
one literal -- `$env:CLAUDE_PROMPTS_DIR` -- which is how a frozen contract
names its own location without hard-coding an absolute path. That spelling is
load-bearing: it is the only token the reader replaces, and any other
placeholder is passed through untouched into a real session's prompt.
The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-z-0-quality-requirements` -- the name that produces `worktree-lane-z-0-quality-requirements` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · lane-z-0-quality-requirements · lane-z-0-quality-requirements]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `opus` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The verb refuses any other program -- *"this script never runs an
arbitrary command from a contract file"* -- so a contract's `## Dispatch` block
is not a place to name a helper. Until 2026-09-12 this generator emitted the
deprecated `Dispatch-Lane` alias here and **every contract it produced was
refused by the verb meant to launch it**. That alias still resolves as the
manual fallback and adds a skip-if-`worktree-lane-z-0-quality-requirements`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-z-0-quality-requirements` -> branch `worktree-lane-z-0-quality-requirements` -> contract `LANE-z-0-quality-requirements.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE -- the flag takes the bare lane
name.

## Done-contract (immutable)

1. `ecosystem/quality-requirements.yaml` exists and is READ BY A GATE, not merely present: one entry per requirement carrying `id`, `statement`, `organ` (the thing that enforces it), `metric`, and `trip_test` (the test proving the enforcement REFUSES). Entries seeded from AN2-2's four MEASURED attributes carry `status: measured`; everything else carries `status: candidate` and NO organ field -- a candidate that names an enforcement it cannot prove is the failure this register exists to prevent.
2. A test asserts, for every `status: measured` entry: the named organ resolves to a file that exists, and the named trip-test EXISTS AND FAILS when the requirement is violated (RED-first witness, ADR-108 Sec.B). A `measured` entry whose trip-test passes unconditionally is a REFUSAL, not a pass. Plus: one generated ARCHITECTURE section renders the whole register in one screen, freshness-gated like the other generated indices, and the floor declares the register MUST.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 -- this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license -- the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. File or amend this lane's own BACKLOG row FIRST (operator standing order: every lane's first commit files or amends its own row). **COMMIT**
2. Author `ecosystem/quality-requirements.yaml`. Seed the four MEASURED attributes from AMEND-NIGHT-PLAN-002 AN2-2, each with its measured incident: performance (five OOM-killed full-suite attempts at 1.4 GB free of 28 GB; graph-rebuild 14.5s/13.6s wall at 50 MB peak and audit-health 16.0s/16.5s wall at **768 MB peak**, both measured on a quiet box 2026-09-15 -- note AN1-3 named BOTH as the heaviest local operation, but only audit-health is memory-heavy, 15x graph-rebuild; record the correction), availability/reliability, resource control (the memory floor), observability. File every other requirement this window produced as prose as `status: candidate`. **COMMIT**
3. Seed the register's availability/reliability entries with TONIGHT'S measured findings, each as its own entry: (i) killing a job does not kill its process tree -- job 100297d3 `state.json` reapedMidWorkAt 2026-09-14T22:43:32Z, the subtree outlived the reap by ~8 minutes and a GRANDCHILD outlived the parent that had just been killed; (ii) SIGKILL on a background session does NOT reclaim it -- the daemon rehydrates it from `~/.claude/daemon/roster.json` under the SAME session-id at `attempt: 2`, twice witnessed 2026-09-15, and `claude stop <id>` is the only verb that deregisters; (iii) a Stop hook resolved its repo root to an already-torn-down worktree and WROTE there (`logs/2026-09/DETECTOR-ERROR-2026-09-13.md`, preserved in this batch's manifest); (iv) a Codespace whose devcontainer build fails is SILENTLY replaced by a bare recovery container, so its gates are vacuous rather than absent. **COMMIT**
4. Write the trip-tests -- one per `measured` entry, each proving the named organ REFUSES. Where no organ yet enforces a requirement, DOWNGRADE the entry to `candidate` rather than inventing enforcement it cannot prove. **COMMIT**
5. Render the register into ONE ARCHITECTURE section (generated, freshness-gated), declare it floor MUST, and name the register's TRIGGER (the commit-tier gate now; the lane-5 log-review routine when it lands) and its named CONSUMER (the ARCHITECTURE section and the floor). An organ with no trigger and no named consumer is refused at freeze. **COMMIT**
6. Final: targeted tests for THIS lane's diff (`uv run --locked pytest`), one end-of-lane artifact (what changed - proposed diffs - open items), `git stash list` EMPTY, **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch -- commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry -- that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration -- the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
