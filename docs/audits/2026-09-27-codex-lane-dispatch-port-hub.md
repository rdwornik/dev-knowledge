# Codex Review — lane-dispatch-port-hub

**Date:** 2026-09-27
**Branch:** `worktree-lane-dispatch-port-hub`
**HEAD:** `2cb47aee`
**Diff range:** `main..worktree-lane-dispatch-port-hub`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review (9 rounds, iterate-until-clean)
**Tally:** 0/13/0/0 <!-- Critical/High/Medium/Low. Verified against the Findings section below: thirteen High across rounds 1-8 (3+1+2+1+2+2+1+1), zero Critical/Medium/Low, round 9 clean. -->

**Model used:** `gpt-5.6-terra`
**Review profile:** code

---

## Focus

Consumer: `H:\My Drive\CLAUDE PROMPT DIR\LANE-5B4-10-dispatch-port-hub.md` (contract) — WAVE5B-N4
lane-dispatch-port-hub (proposal row L8, R17).
Diff: `scripts/dispatch.py` (codespace create/exec/harvest/stop/delete legs, ported from
`DispatchHelpers.psm1`'s `Invoke-CodespaceGh` / `Start-DispatchCodespace` / `Save-CodespaceLaneHarvest`
/ `Stop-DispatchCodespace`), `tests/test_dispatch_codespace.py` (new), `ARCHITECTURE.md` (the "Layer 2
never executes" invariant, amended), plus the necessary knock-on edits `tests/test_dispatch_py.py`,
`tests/test_dispatch_launch.py`, `templates/dispatch-shim.ps1` (each recorded `DECIDED-BY-LANE` in the
handback, not in "Files you own").
Each round ran `codex exec review --uncommitted --title lane-dispatch-port-hub-recheckN < /dev/null`,
fixed every P1 finding, re-ran the targeted suite + ruff + `audit.py health`, then re-reviewed.

---

## Findings

## Critical

(none)

## High

### Round 1

1. **`scripts/dispatch.py::codespace_exec`** — the runner's argv carried the **local** contract path
   in its prompt string (`"Read and execute the frozen contract at <LOCAL path>"`), never rewritten
   to the path the contract is actually shipped to inside the codespace. **Fix:** rewrite every
   occurrence of `str(contract)` in `head_argv` to `f"{workdir}/{contract.name}"` before generating
   the runner script.
2. **`scripts/dispatch.py::codespace_exec`** — an empty `head_argv` produced a redirection-only shell
   command (`> run.log 2>&1`) that exits 0 and writes a success receipt having run no agent at all.
   **Fix:** refuse immediately when `head_argv` is empty.
3. **`scripts/dispatch.py::run_gh`** — an unrunnable `gh` (missing binary) raised an uncaught
   `FileNotFoundError` out of every codespace command instead of the function's own documented
   refusal path. **Fix:** catch `OSError` and return a `GhResult(ok=False, exit_code=127, ...)`.

### Round 2

4. **`scripts/dispatch.py::codespace_delete`** — `verify_harvest_manifest` never checked that the
   manifest's own `name` field matched the codespace about to be deleted, so a stale manifest from a
   prior lane's harvest would authorize deleting an unrelated, unharvested codespace. **Fix:** add
   `expected_name` and refuse with "refusing to authorize deleting a different codespace" on a
   mismatch.

### Round 3

5. **`scripts/dispatch.py::codespace_exec`** — returned early on a failed `ssh` run before pulling the
   receipt back, discarding exactly the evidence a failed lane most needs kept. **Fix:** always
   attempt the receipt `cp` regardless of the runner's own exit status.
6. **`scripts/dispatch.py::codespace_exec`** — a receipt reporting `is_error: true` /
   `status: "error_during_execution"` was still read as `ExecResult(ok=True, ...)` because only the
   `ssh` transport's own exit code gated success. **Fix:** gate on the receipt's own `is_error`/
   `status` fields too.

### Round 4

7. **`scripts/dispatch.py::codespace_exec`** — `workdir` (`/workspaces/dispatch`) is not the checkout
   `gh codespace create` produces and nothing created it, so the first `cp` into it failed on every
   fresh codespace. **Fix:** `ssh -- mkdir -p <workdir>` before any `cp`.

### Round 5

8. **`scripts/dispatch.py::codespace_exec`, `codespace_plan`** — the codespace's NAME was
   re-derived via `gh codespace list --json` matched by display name, which is not unique across a
   stale, stopped codespace from a prior run of the same slug — ambiguous, and a codespace this call
   just created (and is now billing) would be orphaned untracked on a list failure or a match miss.
   **Fix:** read the name directly from `gh codespace create`'s own stdout (measured,
   `DIGEST-2026-09-15-codespaces-reference.md:182-183`: `fmt.Fprintln(a.io.Out, codespace.Name)`) —
   never reconstructed.

### Round 6

9. **`scripts/dispatch.py::_codespace_runner_script`** — the runner `cd`'d into `workdir` (its own
   scratch directory for the contract/runner/receipt files, never containing the repo) to run the
   dispatched agent, so the agent could read its contract but never touch, test, commit, or push the
   checkout the contract asks it to work in — contradicting the sanctioned exception's premise that
   this drives "THIS repo's own contract." **Fix:** `cd` into `checkout_dir`
   (`/workspaces/<repo-name>`, derived from `repo`), keep `run.log`/`receipt.json` in `workdir` by
   absolute path.
10. **`scripts/dispatch.py::run_gh`** — `stderr` was folded into `stdout` (`(proc.stdout or "") +
    (proc.stderr or "")`) despite `GhResult` exposing a separate `stderr` field. A successful `create`
    that also writes progress/warnings to stderr would corrupt the one-line NAME every later `-c`
    call keys on; a harvested `cat`'s stderr would be hashed into the manifest as if it were the
    file's own content. **Fix:** keep `stdout`/`stderr` separate on the real subprocess path.

### Round 7

11. **`scripts/dispatch.py::codespace_exec`** — the documented flow is `plan --substrate codespace`
    (which resolves the contract to **absolute** before embedding it in the prompt) then
    `codespace-exec --argv-json <that plan's argv>` with whatever contract argument the caller typed
    — often relative. `str(contract)` left unresolved never matched the absolute path already baked
    into `head_argv`'s prompt, so the Round 1 rewrite silently did nothing and the local absolute path
    leaked into the runner. **Fix:** `contract = Path(contract).resolve()` at the top of
    `codespace_exec`, matching `plan`'s own resolution.

### Round 8

12. **`_codespace_runner_script`'s embedded receipt-writer** — the reverse scan over `run.log` (which
    also carries stderr, folded in by the runner's own `2>&1`) `break`s unconditionally after the
    first (i.e. last) non-empty line, JSON or not — a trailing non-JSON diagnostic after the agent's
    real final JSON result stopped the scan before reaching it, and a zero process exit was then read
    as success even when the real last JSON result reported an error. **Fix:** continue scanning
    backward past a line that fails to parse, or parses to something other than a `dict`; only break
    on a genuine dict-shaped JSON line.
13. **`scripts/dispatch.py::run_gh`** — no timeout on the real `subprocess.run(["gh", ...])` call: a
    stalled `gh` (an interactive auth prompt with no TTY to answer it, a hung network request) blocked
    every codespace command indefinitely, never reaching the documented refusal path. **Fix:** a
    generous bound (`GH_TIMEOUT_SECONDS = 900`), converting `subprocess.TimeoutExpired` into a failed
    `GhResult` (`exit_code=124`).

### Round 9

Clean — "No critical or high-confidence high-severity defects were identified in the reviewed
changes."

## Medium

(none)

## Low

(none)

---

## Non-Codex finding: live-`gh` discovery

Not a Codex finding — surfaced only by actually running the real end-to-end proof (Done-when row L8)
against a live, authenticated `gh` and a real, disposable Codespace, since no `invoker`-faked unit
test can validate a real CLI's flag grammar:

- **`retention: str = "1d"`** (the default in `codespace_plan`, `codespace_exec`, and the
  `codespace-exec` CLI's `--retention` option) — `gh codespace create --retention-period` parses Go's
  `time.Duration` grammar (`h`/`m`/`s` units only; no `d`), and `"1d"` failed every real call with
  `invalid argument "1d" ... unknown unit "d" in duration "1d"`. **Fix:** `"24h"` (all three sites),
  plus a regression test (`test_retention_defaults_are_valid_go_durations_not_a_day_suffix`) asserting
  the Go-duration grammar on all three defaults so this cannot silently drift back.

After the fix, the full real pipeline ran clean end to end: `codespace_exec` (create, mkdir, cp
contract, cp runner, ssh run, cp receipt — all real `gh`) → `codespace_harvest` (real `ssh ... cat`,
manifest written with matching sha256) → `verify_harvest_manifest` (verified) →
`codespace_delete` (allowed, `gh codespace delete` exit 0). `gh codespace list` afterward: empty — no
lingering billable resource.
