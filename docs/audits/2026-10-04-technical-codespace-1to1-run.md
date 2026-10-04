# Codespace 1:1 — the run that shows a fresh Codespace carries every model CLI and C1 proves the models served (2026-10-04)

Consumer and contract: `LANE-B2-W1-b2-codespace-1to1` (batch B2-W1, lane W1-7; ADR-126 D2, R59, R61, R63; row [#1335]). This record is the run its Done-item 5 asks for. The check is `scripts/codespace_parity.py` (run records: `docs/audits/2026-10-03-technical-codespace-parity-run.md`, `docs/audits/2026-10-04-technical-codespace-toolset-run.md`). This lane files and closes no row; it claims C1 and C4 as the contract states them and reports C2, C3 and C5 exactly as the check printed them.

## Verdict, one line per condition

```
PASS    cond=1 environment   except named auth items: codex, grok, agy  (claude served claude-sonnet-5 on BOTH sides, = registry)
FAIL    cond=2 gates         1 of 354 verdicts differs: a test that skips on Windows and passes on Linux -- not claimed
NOT-RUN cond=3 landing       the push leg PASSED (same base and tree); the merge leg is the integrator's act -- not claimed
PASS    cond=4 transport     read PASS (290 entries) and write PASS (written, read back identical, deleted, absent afterwards)
PASS    cond=5 cleanup       no Codespace, no run branch left; 71.7 min wall, 4.78 core-hours (4 cores)
```

The three auth items are the OPERATOR-ACTION below, not failures: a Codespace holds no ChatGPT, xAI or Google login and no secret can carry one (no API keys — the standing auth ruling). C1 names each, says what step clears it, and does not pass a CLI it could not probe.

## What ran, where, and when

```
substrate       local worktree (Windows 11, AMD64) vs one GitHub Codespace (Linux x86_64)
repository      rdwornik/dev-knowledge, branch worktree-b2-codespace-1to1
sha             6be0629bf45276a0e9f3a3d7a20f7e2c7f5a606f (both sides; tree f1752718782e770bd3ee1028e45ccdb361ec9963)
Codespace       b2-codespace-1to1-rr65q4vw4qp2xr5r
machine type    standardLinux32gb  (4 cores, 16 GB RAM, 32 GB storage)  -- the dispatch.py default, not a flag typed here
idle timeout    240m (--idle-timeout 240m --retention-period 24h; both are the dispatch.py defaults)
create call     2026-10-04T12:46:34Z   (create-call window 12:46:29Z-12:46:35Z; the create argv came from dispatch.codespace_plan)
delete call     2026-10-04T13:58:16Z   (gh codespace delete --force, exit 0)
wall time       71.7 min   core-hours 4.78
quota           uv run --locked python scripts/quota_watch.py check --projected-core-hours 16
                -> OK: 0.85 used + 16.00 projected = 16.85 of 180 core-hours, 163.15 would remain   (before the first create)
creates         TWO, in sequence (never two live at once) -- see Attempt 1
```

Deletion shown: after `gh codespace delete`, `gh codespace list` printed nothing; `git ls-remote --heads origin worktree-b2-codespace-1to1-cs` printed nothing; `verify-cleanup` wrote `codespace_listed_after: false`, `branch_listed_after: false` and C5 PASSed on it (below).

### Attempt 1 — refused, and the refusal became a RED test

`b2-codespace-1to1-vgrj967r45xhwwpx`, created 2026-10-04T12:35:25Z, deleted about 12:45:45Z (about 10 min, 0.7 core-hours). The agy leg printed `REFUSED: L-F5 the Antigravity installer failed`: the vendor installer's body arrived compressed and was piped straight into `bash`. The container fell into the Codespaces recovery container, so nothing downstream was a measurement. Fix, RED-first: `94c52403` (RED, `test_a_vendor_installer_is_fetched_checked_to_be_a_script_and_never_piped_into_bash_blind`) then `6676a243` (`fetch_installer`: `--compressed`, retries, a `#!` check, a first-bytes diagnostic, then `bash <file>`). Attempt 2 provisioned clean: `DONE — 12 leg(s) acted; all four legs assert clean and a real gate ran here`, `gate OK`. The codex review then caught the same pipe-into-bash on the claude pin leg; fixed in `6a723c54`.

### The final collect

Attempt 2 was provisioned at `6676a243`; the branch then moved to the final tip with `git pull` on the Codespace, and the collect re-ran there at `6be0629b` (`collect-exit=0`) so that both records, local and Codespace, are of the same sha and tree. The local record was taken twice at that tip (via the memory gate). The first local record read `audit.py health` as `fail` while the same command exits 0 standalone and again in a second collect; that one-off is not explained and is reported, not hidden. The check printed below is the second local record against the one saved Codespace record.

## The check, in full (third `check` call; `--cleanup` supplied)

```
PASS cond=1 environment except named auth items: codex, grok, agy
    platform: declared OS-specific (the operating system and CPU architecture differ by definition between a Windows workstation and a Linux container) -- local={'machine': 'AMD64', 'system': 'Windows'} codespace={'machine': 'x86_64', 'system': 'Linux'}
    python: local=3.12.10 codespace=3.12.10
    uv: local=0.11.19 codespace=0.11.19
    uv_lock_sha256: local=43c532c135883ed39ad5608c71dc28caee8a404b562b075fd3ede53455ef8216 codespace=43c532c135883ed39ad5608c71dc28caee8a404b562b075fd3ede53455ef8216
    uv sync --locked exit (local)=0
    uv sync --locked exit (codespace)=0
    claude version local=2.1.289 codespace=2.1.289
    gh version local=2.93.0 codespace=2.93.0
    codex version local=0.155.0 codespace=0.155.0
    grok version local=1.0.44 codespace=1.0.44
    agy version local=1.2.16 codespace=1.2.16
    hook set local=['commit-msg', 'pre-commit', 'pre-push'] codespace=['commit-msg', 'pre-commit', 'pre-push']
    served model claude local=claude-sonnet-5 registry=claude-sonnet-5 (roles.implement, provider anthropic)
    served model codex local=gpt-5.6-terra registry=gpt-5.6-terra (roles.review, provider openai)
    served model grok local=grok-4.7 registry=grok-4.7 (roles.review, provider xai)
    served model agy local=gemini-3.8-flash-high registry=gemini-3.8-flash (models row of provider antigravity)
    served model claude codespace=claude-sonnet-5 registry=claude-sonnet-5 (roles.implement, provider anthropic)
    served model codex codespace: not probed -- login missing (a named auth item)
    served model grok codespace: not probed -- login missing (a named auth item)
    served model agy codespace: not probed -- login missing (a named auth item)
    AUTH-ITEM codex: codespace=unauthenticated local=authenticated -- needs `codex login --device-auth` run once in the Codespace (ChatGPT device sign-in; no Codespaces secret holds it)
    AUTH-ITEM grok: codespace=unauthenticated local=authenticated -- needs `grok login --device-auth` run once in the Codespace (xAI device sign-in for a headless host; no Codespaces secret holds it)
    AUTH-ITEM agy: codespace=unauthenticated local=authenticated -- needs an `agy` sign-in: run `agy` once in the Codespace (`gh codespace ssh`), open the Google URL it prints in a browser and complete the sign-in (no login subcommand, no Codespaces secret; its model call is what shows the login)
FAIL cond=2 gates 1 verdict(s) differ: tests.test_codespace_admission::test_present_but_not_executable_is_treated_as_absent (local=skipped codespace=passed)
    compared 354 verdicts; 1 differ, 0 declared case(s)
NOT-RUN cond=3 landing merge leg NOT-RUN: a lane cannot merge: the local --no-ff merge, the integrator's own re-run of the outcome test and the CI push verdict are the integrator's acts, not this check's
    base sha local=6be0629bf45276a0e9f3a3d7a20f7e2c7f5a606f codespace=6be0629bf45276a0e9f3a3d7a20f7e2c7f5a606f
    tree sha local=f1752718782e770bd3ee1028e45ccdb361ec9963 codespace=f1752718782e770bd3ee1028e45ccdb361ec9963
    pushed branch worktree-b2-codespace-1to1-cs on origin at 6be0629bf45276a0e9f3a3d7a20f7e2c7f5a606f; codespace HEAD 6be0629bf45276a0e9f3a3d7a20f7e2c7f5a606f
PASS cond=4 transport
    read: PASS (exit 0, 290 entries; local 290)
    write: PASS (PROBE-b2-codespace-1to1.txt: write exit 0, read-back identical, delete exit 0, absent afterwards True)
PASS cond=5 cleanup
    wall time 71.7 min on standardLinux32gb; core-hours 4.78 (4 cores)
    codespace b2-codespace-1to1-rr65q4vw4qp2xr5r and branch worktree-b2-codespace-1to1-cs both gone
exit=1
```

## Evidence by Done-item

```
1  RED  tests/test_dispatch_codespace.py: 2 failed, 1 passed (basicLinux32gb vs standardLinux32gb), recorded before the edit;
        test and code landed together in a707ab37 (the RED run, not a RED commit, is the witness); dry-run assertion 787dc007
2  RED  85144b42: 10 failed in tests/test_provision_sh.py (grok has no leg or pin, agy unpinned)  ->  c9dcb23e
        real Codespace: claude 2.1.289, gh 2.93.0, codex 0.155.0, grok 1.0.44, agy 1.2.16, uv 0.11.19 all resolved in a login shell, same as local
3  RED  86c9e7af (+ 6c822c39, 6ba5e7a3 making the witnesses real)  ->  218d9d23; review fixes RED e6991460 -> 6a723c54
        C1 above prints "served model <cli> <side>=<id> registry=<id> (<where>)" per CLI; a mismatch or a missing id is a FAIL naming both
4  every login-needing item is one OPERATOR-ACTION (below) and C1 prints it as AUTH-ITEM with the exact step
5  this record
```

## OPERATOR-ACTION — three logins, once per Codespace, none in a file

```
codex   gh codespace ssh -c <name>, then:  codex login --device-auth      (ChatGPT device sign-in; no Codespaces secret holds it)
grok    gh codespace ssh -c <name>, then:  grok login --device-auth       (xAI device sign-in for a headless host)
agy     gh codespace ssh -c <name>, then:  agy   -- open the Google URL it prints in a browser and complete the sign-in
claude  already served: the CLAUDE_CODE_OAUTH_TOKEN Codespaces secret
gh      already served: the token Codespaces issues
```

After the three sign-ins, C1 on that Codespace probes codex, grok and agy and compares each served id with the registry; until then it reports them as named auth items. Not done in this run: a login is the operator's act and was not worked around.
