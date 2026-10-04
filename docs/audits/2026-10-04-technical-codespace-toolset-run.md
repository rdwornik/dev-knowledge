# Codespace toolset — the run that shows a fresh Codespace carries the local toolset (2026-10-04)

Consumer and contract: `LANE-FOUNDATION-foundation-13-codespace-toolset` (batch FOUNDATION, night lane; R63 step 1; added by `to-cc/AMEND-BATCH-FOUNDATION-5-2026-10-03.md`). This record is the run its Done-contract items 1–3 ask for. The check it ran is `scripts/codespace_parity.py` (lane 5's organ, run record `docs/audits/2026-10-03-technical-codespace-parity-run.md`). This lane does not close `[#1335]`, files no row, and claims **R63 step 1 only** — conditions 2, 3 and 5 are reported as the check printed them, not claimed.

## Verdict, one line per condition

```
PASS    cond=1 environment   except named auth items: codex, agy
FAIL    cond=2 gates         2 of 287 verdicts differ (the same two as lane 5's run 2; neither is a toolset matter) -- not claimed
NOT-RUN cond=3 landing       the push leg PASSED, same base and tree; the merge leg is the integrator's act -- not claimed
PASS    cond=4 transport     read PASS (281 entries) and write PASS (written, read back identical, deleted, absent afterwards)
PASS    cond=5 cleanup       no Codespace, no run branch left; 7.0 min wall, 0.23 core-hours -- not claimed (computed after teardown)
```

Versus lane 5's run 2 on `origin/main`: **cond 1** was `FAIL claude 2.1.288 local vs 2.1.272 Codespace; gh, codex, agy absent on the Codespace`; **cond 4** was `FAIL rclone is not installed on the Codespace` with the write leg NOT-RUN. Those two are what this lane changes.

## What ran, where, and when

```
substrate       local worktree (Windows 11, AMD64) vs one GitHub Codespace (Linux x86_64, Debian GLIBC 2.36)
repository      rdwornik/dev-knowledge, branch worktree-foundation-13-codespace-toolset
sha             aec1d23a39750771fdef791f9db42e3727837675 (both sides; tree 2a450d5c6494fa697746f8e875cb94e911f6185b); RED commit 56bfcc09 precedes it
Codespace       foundation-13-toolset-g5rvj4w64gg2wqjx, machine basicLinux32gb (2 cores, 8 GiB), created --idle-timeout 30m --retention-period 24h
create call     2026-10-04T01:27:25Z   (Queued -> Provisioning -> Available in about 90 s)
delete call     2026-10-04T01:34:24Z
wall time       7.0 min    core-hours 0.23     [codespace_regime.uptime_minutes x MACHINE_CORES]
creates         ONE. No §0a retry was needed.
quota           uv run --locked python scripts/quota_watch.py check --projected-core-hours 2
                -> OK: 0.62 used + 2.00 projected = 2.62 of 180 core-hours, 177.38 would remain   (exit 0, before the create)
```

Before the create: `gh codespace list` was empty. Container checks before any number was trusted: `ldd --version` → `ldd (Debian GLIBC 2.36-9+deb12u10) 2.36` (glibc, not musl); `git rev-parse HEAD` in `/workspaces/dev-knowledge` equalled `aec1d23a…`.

Commands (plain `gh` primitives, as lane 5 did; no agent ran, so neither driver — win-tooling's `Dispatch-Codespace`, nor the hub's `dispatch.py` verbs — was touched):

```
gh codespace create -R rdwornik/dev-knowledge -b worktree-foundation-13-codespace-toolset --machine basicLinux32gb --idle-timeout 30m --retention-period 24h -d foundation-13-toolset
gh codespace cp -c <name> -e run-parity.sh remote:/tmp/run-parity.sh           # a 3-line runner
gh codespace ssh -c <name> -- "nohup bash -l /tmp/run-parity.sh > /tmp/run-parity.log 2>&1 &"
    # = cd /workspaces/dev-knowledge; uv run --locked python scripts/codespace_parity.py collect --side codespace --out /tmp/parity-remote.json --push-branch worktree-foundation-13-codespace-toolset-cs --probe-write PROBE-foundation-13-codespace-toolset.txt
uv run --locked python scripts/codespace_parity.py collect --out local.json --via-gate     # local side, detached
uv run --locked python scripts/codespace_parity.py check --local local.json --codespace <name> --save-remote remote.json
gh codespace delete -c <name> --force ; git push origin --delete worktree-foundation-13-codespace-toolset-cs
uv run --locked python scripts/codespace_parity.py verify-cleanup --codespace <name> --branch ...-cs --created ... --deleted ... --machine basicLinux32gb --out cleanup.json
uv run --locked python scripts/codespace_parity.py check --local local.json --remote remote.json --cleanup cleanup.json
```

## Done item 1 — the legs' output from the fresh Codespace

`/workspaces/.codespaces/.persistedshare/creation.log`, the toolset lines (one provisioning pass at creation; the log carries one `L-F5` pass, with every leg installing):

```
[provision] L-F1 ok — claude present (2.1.272 (Claude Code))        <- what the claude-code feature delivered (the latest at its install)
[provision] L-F1 ok — node present (v24.21.0)
[provision] L-F5 installing claude 2.1.289 over whatever the feature delivered
[provision] L-F5 OK — claude pinned at 2.1.289, auto-update off
[provision] L-F5 installing gh 2.93.0
[provision] L-F5 OK — gh 2.93.0
[provision] L-F5 installing codex 0.155.0
[provision] L-F5 OK — codex 0.155.0
[provision] L-F5 installing rclone 1.73.2
[provision] L-F5 OK — rclone 1.73.2
[provision] L-F5 installing agy (the vendor installer, latest — it takes no version)
[provision] L-F5 OK — agy present
[provision] DONE — 11 leg(s) acted; all four legs assert clean and a real gate ran here
Outcome: success
```

The same versions in a LOGIN shell (`bash -lc`, the shell the parity check and the admission test use), read after provisioning: `claude --version` → `2.1.289 (Claude Code)`; `gh --version` → `gh version 2.93.0 (2026-05-27)`; `codex --version` → `codex-cli 0.155.0`; `agy --version` → `1.2.16`; `rclone --version` → `rclone v1.73.2`. Login-shell resolution: claude → `/home/vscode/.local/bin/claude`, gh → `/usr/local/bin/gh`, codex → `/usr/local/share/nvm/current/bin/codex`, agy → `/home/vscode/.local/bin/agy`, rclone → `/usr/local/bin/rclone`. `~/.claude/settings.json` in the container: `{"env": {"DISABLE_AUTOUPDATER": "1"}}`.

The pin is `claude --version` on the workstation at this lane's step 0: **2.1.289**, written once in `.devcontainer/provisioning.yaml` `tools:` and read by the leg with `provision_legs.py tools get claude`. It is equal to the container's (check output below: `claude version local=2.1.289 codespace=2.1.289`).

## Done item 2 — the check's full output (`check --local local.json --codespace <name>`, run while the Codespace was alive)

```
PASS cond=1 environment except named auth items: codex, agy
    platform: declared OS-specific (the operating system and CPU architecture differ by definition between a Windows workstation and a Linux container) -- local={'machine': 'AMD64', 'system': 'Windows'} codespace={'machine': 'x86_64', 'system': 'Linux'}
    python: local=3.12.10 codespace=3.12.10
    uv: local=0.11.19 codespace=0.11.19
    uv_lock_sha256: local=43c532c135883ed39ad5608c71dc28caee8a404b562b075fd3ede53455ef8216 codespace=43c532c135883ed39ad5608c71dc28caee8a404b562b075fd3ede53455ef8216
    uv sync --locked exit (local)=0
    uv sync --locked exit (codespace)=0
    claude version local=2.1.289 codespace=2.1.289
    gh version local=2.93.0 codespace=2.93.0
    codex version local=0.155.0 codespace=0.155.0
    agy version local=1.2.16 codespace=1.2.16
    hook set local=['commit-msg', 'pre-commit', 'pre-push'] codespace=['commit-msg', 'pre-commit', 'pre-push']
    AUTH-ITEM codex: codespace=unauthenticated local=authenticated -- needs `codex login` (ChatGPT sign-in) or an API-key Codespaces secret
    AUTH-ITEM agy: codespace=unprobed local=unprobed -- needs an `agy` login; it has no non-interactive status command, so it cannot be probed
FAIL cond=2 gates 2 verdict(s) differ: tests.test_codespace_admission::test_present_but_not_executable_is_treated_as_absent (local=skipped codespace=passed); tests.test_provision_legs::test_history_check_exits_0_on_this_repo (local=failed codespace=passed)
    compared 287 verdicts; 2 differ, 0 declared case(s)
NOT-RUN cond=3 landing merge leg NOT-RUN: a lane cannot merge: the local --no-ff merge, the integrator's own re-run of the outcome test and the CI push verdict are the integrator's acts, not this check's
    base sha local=aec1d23a39750771fdef791f9db42e3727837675 codespace=aec1d23a39750771fdef791f9db42e3727837675
    tree sha local=2a450d5c6494fa697746f8e875cb94e911f6185b codespace=2a450d5c6494fa697746f8e875cb94e911f6185b
    pushed branch worktree-foundation-13-codespace-toolset-cs on origin at aec1d23a39750771fdef791f9db42e3727837675; codespace HEAD aec1d23a39750771fdef791f9db42e3727837675
PASS cond=4 transport
    read: PASS (exit 0, 281 entries; local 281)
    write: PASS (PROBE-foundation-13-codespace-toolset.txt: write exit 0, read-back identical, delete exit 0, absent afterwards True)
NOT-RUN cond=5 cleanup no cleanup record supplied (run `verify-cleanup` after teardown)
exit=1
```

The exit is 1 because of condition 2, which is not this lane's. Condition 4's evidence: the secret `RCLONE_CONFIG_GDRIVE_TOKEN` is delivered (presence read as a boolean; no value is in any record or here); the read leg is `rclone lsf gdrive: --max-depth 1` (281 entries on both sides); the write leg writes `PROBE-foundation-13-codespace-toolset.txt`, reads it back and compares the bytes, runs `rclone deletefile`, and lists the remote with `--include` to prove it gone. The transport is `gdrive:` = the Google Drive `CLAUDE PROMPT DIR`; the Drive token's refresh may expire about 2026-10-10 (R57) — it did not here.

### Condition 2 — why it is red, and why this lane does not claim it

Both differing verdicts are lane 5's ROWS-OWED and unchanged by this lane: `test_present_but_not_executable_is_treated_as_absent` is a Windows skip with no `DECLARED_OS_CASES` row; `test_history_check_exits_0_on_this_repo` fails in any lane worktree whose local `main` trails `origin/main` (`history: ref 'main' is BEHIND origin/main (864b0b9f6)`) and passes in a fresh clone. This lane's own new tests were among the 287 compared and agreed on both sides.

## Done item 3 — teardown, verified

```
gh codespace list  -- BEFORE the create          []        (exit 0)
gh codespace list  -- BEFORE the delete          [{"name":"foundation-13-toolset-g5rvj4w64gg2wqjx","state":"Available"}]
gh codespace delete -c foundation-13-toolset-g5rvj4w64gg2wqjx --force      -> exit 0
git push origin --delete worktree-foundation-13-codespace-toolset-cs       -> [deleted]
gh codespace list  -- AFTER the delete           []        (exit 0; `gh api user/codespaces --jq .total_count` -> 0)
git ls-remote --heads origin -- AFTER: automation/fleet-audit, epic/foundation-int-foundation-4-merge-gate, epic/foundation-int-foundation-5-codespace-parity, main, worktree-foundation-13-codespace-toolset, worktree-foundation-4-merge-gate, worktree-foundation-8-test-isolation
rclone lsf gdrive: --files-only --include PROBE-foundation-13-codespace-toolset.txt   -> (empty; exit 0)      the probe file is absent from the transport
Test-Path "$env:CLAUDE_PROMPTS_DIR\PROBE-foundation-13-codespace-toolset.txt"         -> False                  absent on the mounted Drive too
verify-cleanup record: codespace_listed_after false, branch_listed_after false, listing_exit 0, ls_remote_exit 0, created 2026-10-04T01:27:25.367Z, deleted 2026-10-04T01:34:24.162Z, basicLinux32gb
check --local local.json --remote remote.json --cleanup cleanup.json (offline, after teardown):
    PASS cond=5 cleanup: wall time 7.0 min on basicLinux32gb; core-hours 0.23 (2 cores); codespace ... and branch ...-cs both gone
```

`worktree-foundation-13-codespace-toolset` is the lane's handback branch and stays; the `-cs` branch was the run's own.

## Auth items — named exactly (N4)

No secret, token or login was created, copied or widened. What the Codespace lacks, and what showed it:

| tool | state in the Codespace | the command that showed it | what it needs |
|---|---|---|---|
| `claude` | **authenticated** (`authMethod: oauth_token`) | `claude auth status` → `"loggedIn": true` | already delivered: the `CLAUDE_CODE_OAUTH_TOKEN` Codespaces secret |
| `gh` | **authenticated** | `gh auth status` → `Logged in to github.com account rdwornik (GITHUB_TOKEN)` | already delivered: the token Codespaces issues |
| `codex` | **not authenticated** | `codex login status` → `Not logged in` (exit 1) | a `codex login` (ChatGPT sign-in) or an API-key Codespaces secret |
| `agy` | **unknown** — it cannot be probed | `agy --help` lists no `login`/`auth`/`status` subcommand; the check records `unprobed` | an `agy` login; there is no non-interactive status command to read it back |

The same table is `OPERATOR-ACTION` lines in the handback.

## Decisions taken in the lane

- `DECIDED-BY-LANE`: the C4 write leg is exercised by a new opt-in `collect --probe-write NAME`; a record without it prints exactly what lane 5's check printed (write NOT-RUN). The contract's scope note allows edits to `codespace_parity.py` only for C1's auth items, but item 2 requires C4 PASS with the write leg exercised and the check as it stood could never print C4 PASS. The probe name must be one plain file name, so a probe never addresses a path.
- `DECIDED-BY-LANE`: `agy` is **unpinned** — its vendor installer (`https://antigravity.google/cli/install.sh`) accepts `--dir` and no version, so the leg installs the vendor's latest and asserts presence; the version it served (1.2.16) equalled the workstation's by coincidence, and a future skew will surface as a C1 FAIL naming `agy`. The `tools:` row says so (`version: null` with a required `reason`).
- `DECIDED-BY-LANE`: the pin leg is a new leg (`leg_f5_claude_pin`), not an edit of `leg_f1_claude`, because `tests/test_substrate_heartbeat.py` (not owned) pins that leg to "installs nothing". The `claude-code` feature stays declared; the pin is applied over it by the documented native installer form `bash -s <version>`, and the updater is switched off by `DISABLE_AUTOUPDATER` in `~/.claude/settings.json` `env` (code.claude.com/docs/en/setup).
- `DECIDED-BY-LANE`: neither `.devcontainer/Dockerfile` nor `.devcontainer/devcontainer.json` changed. The five tools install in provisioning, where the existing comments say a tool can survive (N1).
- `DECIDED-BY-LANE`: the workstation's `claude` moved 2.1.288 → 2.1.289 between the contract's render and step 0; the pin is the step-0 value, as N2 says.
- `DECIDED-BY-LANE`: no append to `logs/CODESPACE-RECEIPTS.jsonl` (not an owned path); the cost uses the one formula, `codespace_regime.uptime_minutes`.

## ROWS-OWED (this lane files none; the integrator carries them)

- `ROWS-OWED: codex and agy are not logged in inside a Codespace, so a Codespace lane cannot review with codex or read with agy — docs/audits/2026-10-04-technical-codespace-toolset-run.md §Auth items — uv run --locked python scripts/codespace_parity.py check --local <local.json> --codespace <name>` (needs the operator to provide a login or secret per tool; this lane creates none).
- `ROWS-OWED: agy cannot be pinned (its installer takes no version) or probed for login — docs/audits/2026-10-04-technical-codespace-toolset-run.md §Decisions — uv run --locked python scripts/provision_legs.py tools check --only agy --login` (revisit if the vendor adds a version argument or a status command).
- Carried from lane 5 and unchanged: the Windows skip with no declared OS case, and `test_history_check_exits_0_on_this_repo` red in a lane worktree behind `origin/main` (condition 2).
