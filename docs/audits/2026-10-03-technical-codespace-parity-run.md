# Codespace parity — the first recorded run (2026-10-03)

Consumer and contract: `LANE-FOUNDATION-foundation-5-codespace-parity` (batch FOUNDATION), the row `[#1335]` (`tasks/1335-codespace-parity-a-lane-there-works-only-when-on.md`), and the definition `to-browser/CODESPACE-PARITY-DEFINITION-2026-10-03.md`. This record is the run the contract's Done-contract item 3 asks for; the check it ran is `scripts/codespace_parity.py`, covered by `tests/test_codespace_parity.py`. This lane does not close `[#1335]` and files no row.

## Verdict, one line per condition (run 2, after the one fix this lane could make)

```
FAIL    cond=1 environment  claude 2.1.288 local vs 2.1.272 Codespace; gh, codex, agy absent on the Codespace
FAIL    cond=2 gates        2 of 187 verdicts differ (one declared-by-nobody platform skip; one stale-local-main test)
NOT-RUN cond=3 landing      the push leg PASSED and the trees are identical; the merge leg is the integrator's act
FAIL    cond=4 transport    rclone is not installed on the Codespace (the secret IS delivered)
PASS    cond=5 cleanup      no Codespace and no branch left; 18.6 min wall, 0.62 core-hours
```

Not green: **three FAIL, one NOT-RUN, one PASS.** All five green is not required in this batch; what the batch needed is that nobody has to trust a Codespace on a lifecycle that merely completed, and that is now answered per condition. `[#1335]`'s Done-when ("GREEN before any Codespace lane is dispatched") is **not met**.

## What ran, where, and when

```
substrate       local worktree (Windows 11, AMD64) vs one GitHub Codespace (Linux x86_64, Debian GLIBC 2.36)
repository      rdwornik/dev-knowledge, branch worktree-foundation-5-codespace-parity
run 1 sha       6c41bf497d612c1196a484e45c705214aa71c404   (both sides; tree 7eebb42a1af3c77a0d5aa9cd70cde400bd6f1fea)
run 2 sha       20f2f59db7284f03855aae1b79226d22a947076f   (both sides; tree 4ea5fa38ba57c0940555d20e2a4c44b2238c27c7)
Codespace       foundation-5-parity-r6qv7v957c6jr, machine basicLinux32gb (2 cores, 8 GiB), prebuild ready
                created with --idle-timeout 30m --retention-period 24h -d foundation-5-parity
create call     2026-10-03T17:31:48Z    (state read Queued, then Available within about a minute)
delete call     2026-10-03T17:50:27Z
wall time       18.6 min    core-hours 0.62 (2 cores)      [codespace_regime.uptime_minutes x MACHINE_CORES]
quota           quota_watch.py check --projected-core-hours 2  -> exit 0, before the create
```

Container checks before any number was trusted (the known traps — a restarted Codespace can come back as a MUSL container without `uv`):
`ldd --version` → `ldd (Debian GLIBC 2.36-9+deb12u10) 2.36` (glibc, not musl); `uname -m` → `x86_64`; `command -v uv` → `/usr/bin/uv` (`uv 0.11.19 (x86_64-unknown-linux-musl)` is uv's own build target, not the container's libc); `git rev-parse HEAD` in `/workspaces/dev-knowledge` equalled the run sha and `git status --porcelain` was empty.

Commands (the Codespace was driven with plain `gh` primitives; no agent ran, so `dispatch.py codespace-exec` was not used, and neither driver — win-tooling's `Dispatch-Codespace` nor the hub's `dispatch.py` verbs — was moved or edited):

```
gh codespace list                                   # BEFORE (below)
git ls-remote --heads origin                        # BEFORE (below)
gh codespace create -R rdwornik/dev-knowledge -b worktree-foundation-5-codespace-parity --machine basicLinux32gb --idle-timeout 30m --retention-period 24h -d foundation-5-parity
gh codespace cp -c <name> -e run-parity.sh remote:/tmp/run-parity.sh          # a 3-line runner, one token over ssh
gh codespace ssh -c <name> -- bash -l /tmp/run-parity.sh                       # = cd /workspaces/dev-knowledge; uv run --locked python scripts/codespace_parity.py collect --side codespace --out /tmp/parity-remote.json --push-branch worktree-foundation-5-codespace-parity-cs
uv run --locked python scripts/codespace_parity.py collect --out local.json --via-gate   # local side, detached, through memory_admission_gate
uv run --locked python scripts/codespace_parity.py check --local local.json --codespace <name>   # reads the remote record with `ssh ... cat`, never `cp`
gh codespace delete -c <name> --force ; git push origin --delete worktree-foundation-5-codespace-parity-cs
uv run --locked python scripts/codespace_parity.py verify-cleanup --codespace <name> --branch worktree-foundation-5-codespace-parity-cs --created ... --deleted ... --machine basicLinux32gb --out cleanup.json
```

## Run 1 — RED first, before any fix (sha `6c41bf49`)

```
FAIL cond=1 environment claude version skew (local=2.1.288 codespace=2.1.272); gh absent on codespace; codex absent on codespace; agy absent on codespace
    python 3.12.10 = 3.12.10 ; uv 0.11.19 = 0.11.19 ; uv.lock sha256 43c532c1...ef8216 = same ; uv sync --locked exit 0 / 0
    hook set ['commit-msg','pre-commit','pre-push'] = same
FAIL cond=2 gates 4 verdict(s) differ:
    tests.test_codespace_admission::test_present_but_not_executable_is_treated_as_absent (local=skipped codespace=passed)
    tests.test_provision_legs::test_history_check_exits_0_on_this_repo (local=failed codespace=passed)
    tests.test_provision_sh::test_leg_pc_login_path_persists_precommit_onto_a_fresh_shells_path (local=failed codespace=passed)
    tests.test_provision_sh::test_self_digest_actually_distinguishes_a_replaced_script (local=failed codespace=passed)
    compared 187 verdicts (7 pre-commit hooks, audit.py health, 179 pytest nodes); 4 differ, 0 declared cases
NOT-RUN cond=3 landing merge leg NOT-RUN: a lane cannot merge ...
    base sha and tree sha equal; pushed branch ...-cs on origin at the Codespace HEAD
FAIL cond=4 transport rclone absent on the Codespace
    read: FAIL (exit None, None entries; local 274) ; write: NOT-RUN
NOT-RUN cond=5 cleanup no cleanup record supplied
exit=1
```

## The fix, and run 2 (sha `20f2f59d`)

Two of the four gate differences were this machine's PATH, not the code: `shutil.which("bash")` returns `...\WindowsApps\bash.EXE` — the WSL launcher with no distribution installed, UTF-16 output, exit 1 — ahead of Git Bash, so `test_leg_pc_login_path_persists_precommit_onto_a_fresh_shells_path` and `test_self_digest_actually_distinguishes_a_replaced_script` failed here and passed in the Codespace. `tests/test_provision_sh.py` now resolves a bash that actually runs (`_working_bash`: each PATH hit probed, then the bash beside git; none working is a loud `AssertionError`, not a skip). Shown FAIL on run 1, PASS on run 2 (`tests/test_provision_sh.py` 10 passed through `memory_admission_gate.py run`).

Full output of `check --local local.json --codespace <name>` for run 2, verbatim (the Codespace was still alive and the teardown had not happened, so condition 5 had no cleanup record):

```
FAIL cond=1 environment claude version skew (local=2.1.288 codespace=2.1.272); gh absent on codespace; codex absent on codespace; agy absent on codespace
    platform: declared OS-specific (the operating system and CPU architecture differ by definition between a Windows workstation and a Linux container) -- local={'machine': 'AMD64', 'system': 'Windows'} codespace={'machine': 'x86_64', 'system': 'Linux'}
    python: local=3.12.10 codespace=3.12.10
    uv: local=0.11.19 codespace=0.11.19
    uv_lock_sha256: local=43c532c135883ed39ad5608c71dc28caee8a404b562b075fd3ede53455ef8216 codespace=43c532c135883ed39ad5608c71dc28caee8a404b562b075fd3ede53455ef8216
    uv sync --locked exit (local)=0
    uv sync --locked exit (codespace)=0
    claude version local=2.1.288 codespace=2.1.272
    gh version local=2.93.0 codespace=None
    codex version local=0.155.0 codespace=None
    agy version local=1.2.16 codespace=None
    hook set local=['commit-msg', 'pre-commit', 'pre-push'] codespace=['commit-msg', 'pre-commit', 'pre-push']
FAIL cond=2 gates 2 verdict(s) differ: tests.test_codespace_admission::test_present_but_not_executable_is_treated_as_absent (local=skipped codespace=passed); tests.test_provision_legs::test_history_check_exits_0_on_this_repo (local=failed codespace=passed)
    compared 187 verdicts; 2 differ, 0 declared case(s)
NOT-RUN cond=3 landing merge leg NOT-RUN: a lane cannot merge: the local --no-ff merge, the integrator's own re-run of the outcome test and the CI push verdict are the integrator's acts, not this check's
    base sha local=20f2f59db7284f03855aae1b79226d22a947076f codespace=20f2f59db7284f03855aae1b79226d22a947076f
    tree sha local=4ea5fa38ba57c0940555d20e2a4c44b2238c27c7 codespace=4ea5fa38ba57c0940555d20e2a4c44b2238c27c7
    pushed branch worktree-foundation-5-codespace-parity-cs on origin at 20f2f59db7284f03855aae1b79226d22a947076f; codespace HEAD 20f2f59db7284f03855aae1b79226d22a947076f
FAIL cond=4 transport rclone absent on the Codespace
    read: FAIL (exit None, None entries; local 274)
    write: NOT-RUN -- the write leg was not exercised: a write probe would create a transport path no contract names, so only the read leg is measured
NOT-RUN cond=5 cleanup no cleanup record supplied (run `verify-cleanup` after teardown)
exit=1
```

The run-2 remote record was read live by `check --codespace` and **was not saved before the Codespace was deleted** — a gap the run found in the check itself. `check --save-remote FILE` now keeps it (tested). Condition 5's PASS below was computed afterwards by `compare_cleanup` on the record `verify-cleanup` wrote; the two outputs are two invocations, not one.

**The check was hardened after these runs** (the review's findings, `docs/audits/2026-10-03-codex-foundation-5-codespace-parity.md`): a cleanup record without read evidence is refused, `--remote` with `--codespace` is refused, a gates record whose hooks or `audit.py health` never ran is refused, a bare declared OS case forgives nothing, and the landing push reads the exact ref. Run 1 and run 2 above were produced by the earlier code; none of those changes alters a verdict printed above (every record carried hook and health verdicts, no OS case was declared, the pushed ref was the first line), and the cleanup record was **re-read after teardown with the hardened `verify-cleanup`** (it now carries `listing_exit: 0` and `ls_remote_exit: 0`; the Codespace was still not listed and the branch still not on origin).

## Per condition — what is true, with evidence

**1. Environment — FAIL.** What matched: Python 3.12.10, `uv` 0.11.19, the `uv.lock` hash, `uv sync --locked` exit 0 on both sides, the installed hook set. What did not: `claude` is 2.1.272 on the Codespace and 2.1.288 locally (the image carries an older install; nothing pins either); `gh` is not installed in the Codespace (`command -v` over ssh; `provision.sh` and `devcontainer.json` name no `gh`, `codex`, `agy` or `rclone`); `codex` and `agy` likewise. Whether a Codespace lane **needs** `gh`/`codex`/`agy` is a functional question — `codespace_admission.py` already treats `gh` absence as non-gating — and `LANE_TOOLS` in the script counts all four, as the definition lists them. Declared OS-specific entry: `platform` only.

**2. Gates — FAIL.** 7 armed pre-commit hooks and `audit.py health` gave the same verdict on both sides; 175 of 179 pytest nodes agreed on run 1, 177 on run 2. Remaining differences: `test_present_but_not_executable_is_treated_as_absent` is skipped on Windows (`os.access(..., X_OK)` is a no-op there; the platform skip is real but has no row — `DECLARED_OS_CASES` is empty on purpose); `test_history_check_exits_0_on_this_repo` fails in this lane worktree with `history: ref 'main' is BEHIND origin/main (ce6ecb084)` — a lane worktree's local `main` is pinned at the base until the integrator's close, so the live-repo smoke test is red in any lane after `origin/main` moves, and green in a fresh clone.

**3. Landing — NOT-RUN, by design.** Same base sha, same tree, both clean; the Codespace pushed a throwaway branch from a login shell and `git ls-remote` read it back at the Codespace's HEAD. The merge leg (local `--no-ff`, the integrator's re-run of the outcome test, the CI push verdict) is the integrator's act, so the condition is never PASS from a lane.

**4. Transport — FAIL.** The secret `RCLONE_CONFIG_GDRIVE_TOKEN` **is** delivered (presence read as a boolean; no value is in any record or this file) — but `rclone` is not installed on the Codespace, so the read leg cannot run. Local side: `rclone lsf gdrive: --max-depth 1` exit 0, 274 entries. The write leg is NOT-RUN (a write probe would create a transport path no contract names).

**5. Cleanup and cost — PASS.**

```
gh codespace list  -- BEFORE the create        (empty; exit 0)
gh codespace list  -- AFTER the delete         (empty; exit 0; `gh api user/codespaces --jq .total_count` -> 0)
gh codespace list  -- re-read about 2 min later (19:52 local; empty; total_count 0)
git ls-remote --heads origin  -- BEFORE:  automation/fleet-audit, main, worktree-foundation-3-handoff-boot, worktree-foundation-5-codespace-parity, worktree-foundation-6-ci-speed
git ls-remote --heads origin  -- run branch present:  worktree-foundation-5-codespace-parity-cs @ 20f2f59d
git push origin --delete worktree-foundation-5-codespace-parity-cs   -> [deleted]
git ls-remote --heads origin  -- AFTER:   automation/fleet-audit, main, worktree-foundation-3-handoff-boot, worktree-foundation-5-codespace-parity, worktree-foundation-6-ci-speed
verify-cleanup record: codespace_listed_after false, branch_listed_after false, listing_exit 0, ls_remote_exit 0, created 17:31:48Z, deleted 17:50:27Z, basicLinux32gb
compare_cleanup -> PASS cond=5 cleanup: wall time 18.6 min on basicLinux32gb; core-hours 0.62 (2 cores)
```

`worktree-foundation-5-codespace-parity` is the lane's handback branch and stays; the `-cs` branch was the run's own.

## Typed failure observed live (R59)

After the delete, `check --codespace <name>` read nothing and refused — exit 3, no PASS printed:

```
FAILURE RemoteUnavailable: gh codespace ssh exited 1 reading /tmp/parity-remote.json: getting full codespace details: HTTP 404: Not Found (...)
NOT-RUN cond=1 environment remote side unavailable -- nothing was compared
NOT-RUN cond=2 gates remote side unavailable -- nothing was compared
NOT-RUN cond=3 landing remote side unavailable -- nothing was compared
NOT-RUN cond=4 transport remote side unavailable -- nothing was compared
NOT-RUN cond=5 cleanup remote side unavailable -- nothing was compared
exit=3
```

## ROWS-OWED (this lane files none; the integrator carries them)

- `ROWS-OWED: the Codespace image carries claude 2.1.272 against the workstation's 2.1.288, and no gh, codex or agy — docs/audits/2026-10-03-technical-codespace-parity-run.md §1 — uv run --locked python scripts/codespace_parity.py check --local <local.json> --codespace <name>` (needs a pin policy and an operator ruling on which tools a Codespace lane needs; installing them is a new dependency — OPERATOR-ACTION).
- `ROWS-OWED: rclone is not installed on the Codespace although its secret is delivered, so a Codespace lane cannot read the Drive transport — docs/audits/2026-10-03-technical-codespace-parity-run.md §4 — uv run --locked python scripts/codespace_parity.py check --local <local.json> --codespace <name>` (install in the devcontainer is a new dependency — OPERATOR-ACTION; or a ruling that Codespace lanes hand back by git only).
- `ROWS-OWED: test_history_check_exits_0_on_this_repo is red in every lane worktree whose local main trails origin/main — docs/audits/2026-10-03-technical-codespace-parity-run.md §2 — uv run --locked pytest tests/test_provision_legs.py::test_history_check_exits_0_on_this_repo -n0` (run from a lane worktree after origin/main moved).
- `ROWS-OWED: the Windows skip of test_present_but_not_executable_is_treated_as_absent has no declared OS-case row, so gate parity cannot be PASS — docs/audits/2026-10-03-technical-codespace-parity-run.md §2 — uv run --locked python scripts/codespace_parity.py check --local <local.json> --remote <remote.json>` (file the row, then name it in `DECLARED_OS_CASES`).
- `ROWS-OWED: the landing merge leg and the transport write leg of Codespace parity need an integrator-run Codespace lane to exercise — docs/audits/2026-10-03-technical-codespace-parity-run.md §3, §4 — uv run --locked python scripts/codespace_parity.py check --local <local.json> --remote <remote.json> --cleanup <cleanup.json>`.

## Decisions taken in the lane

- `DECIDED-BY-LANE`: the Codespace was driven with plain `gh` primitives, not `dispatch.py codespace-exec` — no agent runs in a parity check, so no model tokens are spent and neither driver is touched.
- `DECIDED-BY-LANE`: no append to the tracked `logs/CODESPACE-RECEIPTS.jsonl` (not an owned path); the numbers above use the one uptime formula, `codespace_regime.uptime_minutes`.
- `DECIDED-BY-LANE`: deleted with `gh codespace delete --force`, not `dispatch.py codespace-delete`, whose manifest gate protects a lane's harvest — this run's evidence is the two records and the check output, already local.
- `DECIDED-BY-LANE`: the "real task" is the check's own gate leg (7 hooks, `audit.py health`, the 5-file pytest selection) on the lane's own sha (N4's default).
- `DECIDED-BY-LANE`: only the test file was changed to fix the bash resolution; `scripts/provision_legs.py`, `scripts/codespace_admission.py`, `scripts/codespace_regime.py`, `.devcontainer/*` were read and left unedited — each remaining failure is either a dependency decision or a functional one.
