# Step-4 witness — `-Model` reaches the dispatch line, and reaches the line that RUNS

Consumers: `[#627]` (this lane's precedent row) · intake #75 (the `-Model`/provider selector
reaching the dispatch line is one of the two mechanism requirements D15 names for the `offload`
seat).

> **Class:** technical · **Date:** 2026-09-09 · **Lane:** `lane-v-000-offload-admission`
> **Mode:** WITNESSED, not read off the code. The contract's own words: *"Do not infer
> `-Model` arrival from a code read — witness it live."*

## 1 · Why a `-DryRun` alone is not the witness

`Start-DispatchLane` (alias `Dispatch-Local` / `Dispatch-Lane`) builds the argv array **and**
prints a separate human-readable line:

```powershell
$claudeArgs = @('--bg', '--model', $Model, '--effort', $resolvedEffort,
                '--permission-mode', $PermissionMode, '--worktree', $Slug, $prompt)
...
if ($DryRun) {
    Write-Host "[lane] DRY RUN -- would run: claude --bg --model $Model ..."
    return
}
& claude @claudeArgs
```

The `DRY RUN` text is a **string interpolation, not the array**. The two are written
independently, so they can agree in the printed line and disagree in the executed one — which
is exactly the declared-but-unbacked shape this lane exists to test, and the same class as the
`gen_lane_contract` → `dispatch` seam that AMEND-BATCH-V-002 §1 rules on. A `-DryRun`
transcript is therefore **necessary and not sufficient**, and this witness has two legs.

**Module under witness, identified rather than assumed.** The deployed copy is what runs, not
the `win-tooling` source:

```
Get-Module -ListAvailable DispatchHelpers
  C:\Users\1028120\.dispatch-helpers\Modules\DispatchHelpers\DispatchHelpers.psd1  v1.6.0
SHA256(DispatchHelpers.psm1)
  EA8B1A0701A035FCF2BF76DB03CE2517B4B8A99BD44A77F88629D33112B68579
(Get-Command Dispatch-Local).ResolvedCommand.Name -> Start-DispatchLane
parameters -> Slug, File, Extra, Effort, Model, PermissionMode, WaitSeconds, DryRun, ...
```

## 2 · Leg A — the printed dispatch line carries the value it was given

Three `-DryRun` invocations from the lane worktree, each with a different `-Model`, all against
a contract path that exists. Verbatim:

```
### W1 default (no -Model)
[lane] slug=probe-model-witness-a branch=worktree-probe-model-witness-a model=opus effort=medium permission-mode=bypassPermissions
[lane] DRY RUN -- would run: claude --bg --model opus --effort medium --permission-mode bypassPermissions --worktree probe-model-witness-a <prompt>

### W2 -Model sonnet -Effort high
[lane] slug=probe-model-witness-b branch=worktree-probe-model-witness-b model=sonnet effort=high permission-mode=bypassPermissions
[lane] DRY RUN -- would run: claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree probe-model-witness-b <prompt>

### W3 -Model claude-opus-5 -Effort max
[lane] slug=probe-model-witness-c branch=worktree-probe-model-witness-c model=claude-opus-5 effort=max permission-mode=bypassPermissions
[lane] DRY RUN -- would run: claude --bg --model claude-opus-5 --effort max --permission-mode bypassPermissions --worktree probe-model-witness-c <prompt>
```

W1 establishes the default is `opus` and W2/W3 establish it is overridable — so the value in
the line is the value passed, and not a constant that happens to match.

## 3 · Leg B — the value reaches the argv that is ACTUALLY EXECUTED

`claude` was shadowed on `PATH` by a stub that records its own argv and exits 0, and
`Start-DispatchLane` was then run **without** `-DryRun`. This exercises the `& claude
@claudeArgs` line itself, which is the one leg A cannot see.

```
resolved claude -> C:\Users\1028120\.claude\jobs\37e9c154\tmp\stub\claude.cmd

Dispatch-Local probe-model-live-d <contract> -Model gpt-5.6-terra -Effort xhigh -WaitSeconds 1

[lane] slug=probe-model-live-d branch=worktree-probe-model-live-d model=gpt-5.6-terra effort=xhigh permission-mode=bypassPermissions
[lane] waiting up to 1s for branch 'worktree-probe-model-live-d' to appear...
[lane] WARNING -- 'worktree-probe-model-live-d' did not appear within 1s.

### recorded argv the executed command actually received:
STUB-CLAUDE-NOT-REAL --bg --model gpt-5.6-terra --effort xhigh --permission-mode bypassPermissions --worktree probe-model-live-d "Read and execute the frozen contract at ...LANE-v-000-offload-admission.md"
```

`gpt-5.6-terra` is deliberately a value nothing on this path could produce by accident — it is
neither the parameter default (`opus`) nor a token appearing anywhere in the function.

**VERDICT: `-Model` reaches the dispatch line, and reaches the argv that runs.** Both legs
hold, on the deployed module, on this host, today.

## 4 · Cleanliness of the witness — no leftovers

The stub exits 0, so `claude` never ran and no lane was launched. Verified after the run:

```
git branch --list 'worktree-probe-*'   -> (empty)
git worktree list                      -> the five batch-V worktrees, no probe entry
git status --short                     -> (clean)
git stash list                         -> (empty)
```

## 5 · Two honest limits, and one note that is NOT a defect

- **The stub proves argv, not behaviour.** It establishes that `claude` is invoked with
  `--model <the value passed>`. Whether the real `claude` then honours that flag is a
  different claim about a different program, and this witness does not make it.
- **`-Effort` rode along and was witnessed with it**, because it sits in the same array. The
  contract asks only about `-Model`; the effort evidence is recorded because it was free, not
  because it was requested.
- **`$LASTEXITCODE` is 1 after a `-DryRun`.** This is *not* a failure of the dispatch: the
  guard `git show-ref --verify --quiet refs/heads/<branch>` exits 1 when the branch correctly
  does not exist, and nothing resets the variable before the function returns. Recorded so a
  later seat scripting around this verb does not read a healthy dry run as a failed one.
