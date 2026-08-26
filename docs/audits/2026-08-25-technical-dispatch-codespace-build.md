# DISPATCH-CODESPACE — build report · win-tooling · 2026-08-25

Built per `BUILD-DISPATCH-CODESPACE.md`. No hub repo was edited; `.dev-knowledge` was read
only. Everything below is measured on this machine today, not recalled.

---

## 0 · Verdict in one breath

**The transport is built, tested, deployed and live-exercised. It does not yet complete a lane,
and the reason is NOT the one Step 0 predicted.** Step 0 found the expected blocker — the hub's
devcontainer installs no Claude Code and offers it no credentials — but the live run never
reached it. It stopped one step earlier, on **SSH key authentication**, against a codespace whose
state was `Available`. That is a second, independent blocker, and it was invisible to every
surface until something actually tried to drive a codespace.

Three findings, in the order a fix has to take them:

| # | Blocker | Where | Owner |
|---|---|---|---|
| 1 | `gh` authenticates with a key the codespace has not authorized | this workstation's `~/.ssh` | operator (one decision, below) |
| 2 | Claude Code is not installed in the image | hub `.devcontainer/` | hub |
| 3 | No credential path for a session inside | hub `.devcontainer/` | hub |

---

## 1 · Step 0 — measured before building

### `gh` and auth

```
gh version 2.93.0 (2026-05-27)
github.com
  * Logged in to github.com account rdwornik (keyring)      <- ACTIVE
    Token scopes: 'admin:public_key', 'codespace', 'gist', 'read:org', 'repo', 'user', 'workflow'
  * Logged in to github.com account Robert-Dwornik_ghub (keyring)
    Token scopes: 'codespace', 'gist', 'read:org', 'repo', 'workflow'
```

Two accounts, `rdwornik` active. **`codespace` scope present on both**; no SSO re-auth was
demanded by any call made today. No credentials were entered at any point.

`gh codespace list` at session start: **empty** — no pre-existing codespaces, so nothing below
disturbed existing work.

### The destination's own definition (read-only)

**(a) Is Claude Code installed in the image or features? NO.**

```
grep -rc -i "claude" .devcontainer/*
  devcontainer.json:0   Dockerfile:0   provision.sh:0   provisioning.yaml:0
```

Zero occurrences across all four files. The only feature declared is
`ghcr.io/devcontainers/features/sshd:1` (`devcontainer.json:47-51`), and the `Dockerfile` adds
nothing but an apt repair (`Dockerfile:36-40`). There is no `npm i -g @anthropic-ai/claude-code`
step anywhere.

**(b) How would a session inside authenticate? IT COULD NOT.**

No `secrets`, no `containerEnv`, no `remoteEnv` key exists in `devcontainer.json`. The only
mentions of `containerEnv` are in a comment block explaining that it was **deliberately removed**
— `devcontainer.json:53-70`, verbatim in part:

> THE ENV GATE ([#554] leg 4) IS NOT DECLARED HERE, AND THE ABSENCE IS THE FIX.

That removal was correct for its own reason (a self-referential `${containerEnv:HOME}` was
creating a junk directory on every start) but it means there is no mechanism at all by which an
`ANTHROPIC_API_KEY` or an OAuth token reaches a session inside. **This is the deeper of the two
hub-side blockers**: (a) is an install step, (b) is a secret-management decision.

**(c) Does the image ship `gh`, `uv`, and the pinned toolchain?**

- **`uv` — YES, and pinned.** `provision.sh` reads `pyproject.toml [tool.uv] required-version`,
  requires it to be an exact `==` pin, installs that version and asserts the result
  (`provision.sh:100-151`). It refuses a mismatch rather than logging one.
- **Python — YES, exact.** `uv python install` provisions the `.python-version` interpreter
  (`3.12.10`) so the base image's own Python never decides what the gates run on
  (`provision.sh:198-213`).
- **`gh` — NOT INSTALLED BY THIS REPO.** Nothing in `.devcontainer/` installs it; the base
  `mcr.microsoft.com/devcontainers/python:1-3.12-bookworm` is the only possible source and the
  repo asserts nothing about it. **Immaterial to this transport** — `gh` runs on the *host*, not
  inside the container — but worth knowing before a contract assumes it.

---

## 2 · What was built

### `Start-DispatchCodespace` (alias `Dispatch-Codespace`)

In `config/dispatch-helpers/DispatchHelpers.psm1`, following the module's own conventions:
guard clauses, `[codespace]`-prefixed narration, a result object, `-DryRun`, and the same
receipt discipline `Start-DispatchCloudV2` uses.

```
Start-DispatchCodespace -Contract <path> [-Slug <name>] [-Repo <owner/repo>] [-Branch <b>]
                        [-Machine basicLinux32gb] [-IdleTimeout 30m] [-Retention 24h]
                        [-IdentityFile <path>] [-DryRun] [-GhInvoker <sb>]
```

Flow, and what each step refuses:

1. **Guards** — contract resolves (same `$env:CLAUDE_PROMPTS_DIR` resolver the other two
   transports use); `gh` on PATH; `gh auth status` exits 0. **The contract check runs first, and
   a test pins that `gh` is not touched until it passes** — provisioning a machine to discover a
   typo costs minutes and quota, and the machine bills while you work out what happened. An
   absent auth is a REFUSAL naming the fix; this function never enters credentials.
2. **Create** — `gh codespace create -R <repo> -b <branch> --machine <m> --idle-timeout <t>
   --retention-period <r> -d <slug>`.
3. **Resolve the NAME** — from `gh codespace list --json name,displayName`. The name is not the
   display name and is the only form `-c` accepts; a list that comes back without our display
   name is a hard stop, not a guess at row 0.
4. **Ship in + run** — the contract goes in as a FILE, and so does the command. See below.
5. **Receipt gate** — `receipt.json` is pulled back; success is reported ONLY with it in hand.

**Every flag above was read off `gh codespace <cmd> --help` on 2026-08-25.** None was recalled.
`--machine basicLinux32gb` was additionally probed against the live repo:

```
GET repos/rdwornik/dev-knowledge/codespaces/machines
  basicLinux32gb     2 cores, 8 GB RAM, 32 GB storage
  standardLinux32gb  4 cores, 16 GB RAM, 32 GB storage
```

`basicLinux32gb` is the smallest machine satisfying the floor the hub's own
`devcontainer.json:112-115` declares (`"cpus": 2, "memory": "8gb"`) — so it is both correct and
the cheapest correct choice.

### The prompt never crosses a shell boundary

A PowerShell string reaching a bash login shell through gh's ssh transport is parsed **twice**.
This is the same failure class that forced the historical cloud path onto brief-on-branch. So:

- the contract is copied in as a file;
- a small runner script is **generated locally with LF endings** and copied in;
- the only thing on the ssh command line is `bash <path>` — one token, no quotes.

A test asserts the ssh argv contains no quote, no prompt text, and no `-p`. The LF detail is not
fussiness: a CRLF shebang makes the kernel look for an interpreter literally named `/bin/bash\r`
and report "bad interpreter", which reads as a missing bash rather than as line endings.

### `Stop-DispatchCodespace` (alias `Stop-Codespace`)

`gh codespace stop`. **Stopping is not deleting.** Compute billing ends; storage keeps counting
against quota until the retention period expires. `gh codespace delete` is **deliberately not
wrapped** — deletion is destructive and stays an operator act. A test asserts no executable line
in the module composes a `delete` argument.

Cost inputs are printed on **every** dispatch including `-DryRun`.

### The verb family, renamed by substrate

| Canonical | Substrate | Function |
|---|---|---|
| `Dispatch-Local` | this workstation | `Start-DispatchLane` |
| `Dispatch-Cloud` | Anthropic-hosted | `Start-DispatchCloudV2` |
| `Dispatch-Codespace` | the repo's own devcontainer | `Start-DispatchCodespace` |

**Deprecated but fully working:** `Dispatch-Lane`, `Dispatch-CloudV2`, `Dispatch-CloudBrief`,
`Archive-CloudSession`. Nothing was removed and nothing is a shim — same alias layer, same
targets. The **function** names are unchanged too: they are the approved-verb layer, they are
what the test suite calls, and renaming them would be churn on a surface no operator types.

---

## 3 · Verification

- **26 new tests** in `tests/test_dispatch_helpers_codespace.py`. Every `gh` call in the domain
  routes through one seam (`Invoke-CodespaceGh -Invoker`), driven by a recording scriptblock, so
  argument boundaries are **measured** rather than read off a printed line. **No test creates,
  copies to, ssh's into or stops a real codespace.**
- One test cross-checks the applier's `$ExportedAls` roster against the module's `Set-Alias`
  block in both directions — a name in one and not the other does not resolve in a fresh shell,
  and that is exactly the trap a rename walks into.
- Module deployed at **v1.2.0** (MINOR: the surface only grew). Applier run, SHA-256 compared,
  and every operator-facing name proven to resolve in a fresh `pwsh -NoProfile` with nothing
  imported by hand:

```
Alias Dispatch-Codespace 1.2.0 DispatchHelpers
Alias Dispatch-Local     1.2.0 DispatchHelpers
Alias Dispatch-Cloud     1.2.0 DispatchHelpers
```

---

## 4 · The live end-to-end run — what actually happened

Contract: `~/Downloads/CS-SMOKE-audit-check-count.md`, written for this run. Read-only by
construction: print the audit check count, print `uv`/`python` versions, print branch and HEAD,
**write nothing, commit nothing, stop**.

```
[codespace] repo=rdwornik/dev-knowledge branch=main machine=basicLinux32gb idle-timeout=30m retention=24h
[codespace] creating (this provisions a machine and starts the clock)...
[codespace] created in 6s.
[codespace] name=cs-smoke-audit-check-count-4gvp5j9679jc695 (display 'cs-smoke-audit-check-count')
[codespace] FAILED -- copying the contract in exited 1.
```

Reproduced by hand against the same codespace, in state `Available`:

```
$ gh codespace cp <contract> remote:/workspaces/dev-knowledge/<file> -c cs-smoke-...
vscode@localhost: Permission denied (publickey,password,keyboard-interactive).
/usr/bin/scp: Connection closed
shell closed: exit status 255
```

### The cause, isolated

```
$ gh codespace ssh --config -c cs-smoke-...
  IdentityFile C:\Users\1028120\.ssh/codespaces.auto

$ ls ~/.ssh
  config  id_ed25519  id_ed25519.pub  known_hosts        <- NO codespaces.auto

$ gh api user/keys
  (empty)
```

**gh names `~/.ssh/codespaces.auto` as the identity it intends to use, and that file does not
exist.** gh's documented key preference puts *"first valid key pair in ssh config (according to
`ssh -G`)"* **above** creating its own automatic key, and `ssh -G` here resolves an existing
`~/.ssh/id_ed25519`. So gh authenticated with a key the codespace has never authorized, against
a codespace that was up and healthy. **The devcontainer's `sshd` feature is not at fault — sshd
answered; it refused the key.**

### Measurements

| | |
|---|---|
| Provision (create returned) | **6 s** |
| Create → `Available` | under 2 min (observed; not instrumented to the second) |
| Run wall-time | **n/a — never reached** |
| Receipt | **none** |
| Machine | `basicLinux32gb`, 2 cores |
| Billed window | created 16:51:06, stopped by hand ~11 min later ≈ **0.4 core-hours** of the 120/month allowance |
| Final state | `Shutdown`, `retention_period_minutes=1440` (the `-Retention 24h` flag verified live) |

The codespace was stopped through the new verb, which is also that function's live witness:

```
[codespace] stopped cs-smoke-... -- compute billing ends; STORAGE still counts against quota.
```

It is **stopped, not deleted** — deletion is left to the operator. It self-deletes at 24h.

### Two defects in my own wrapper, found by that run and fixed

1. **It reported an exit code and named nothing.** The first live failure said only `cp contract
   exited 1`; the actual cause, `Permission denied (publickey)`, was in gh's output and was being
   swallowed. Every gh failure now prints gh's own words. *An exit code without the message is a
   wrong diagnosis waiting to happen.*
2. **No way to name the key.** Added `-IdentityFile <path>`, passed through to scp/ssh as
   `-- -i <path>` — the documented escape, and first in gh's own preference order. It is
   threaded onto all four transport calls, positioned **before** the remote command (gh's usage
   is `ssh [<flags>...] [-- <ssh-flags>...] [<command>]`; put it after and `-i` stops being an
   ssh flag and becomes part of what runs on the far side).

**This module does not create, install or modify an SSH key.** A private key in the operator's
home is theirs; a dispatch helper writing one is exactly the kind of silent act that should never
come from a transport wrapper. Hence a parameter, not a fix.

---

## 5 · What the operator has to decide next

**1. The SSH key (blocker 1, yours, one decision).** Either:
   - let gh create its own — `ssh-keygen -t ed25519 -N "" -f ~/.ssh/codespaces.auto`, then
     `Dispatch-Codespace` works unchanged (gh then finds the key it already says it wants); or
   - point at an existing authorized key — `Dispatch-Codespace <contract> -IdentityFile <path>`.

   I did not do either: both write to or read from your `~/.ssh`, and that is your call.

**2. Claude Code in the image (blocker 2, hub).** One feature or one `RUN` line in
   `.devcontainer/Dockerfile`. Until then the runner script this transport ships in will detect
   the absence and write a receipt saying so rather than failing silently — that guard is already
   in place and will be what the *next* live run returns.

**3. Credentials for a session inside (blocker 3, hub).** The real design question, and the one
   that should not be answered casually: a Codespaces secret carrying `ANTHROPIC_API_KEY` is the
   obvious route, but it puts a long-lived key in an environment a lane can read. Worth a ruling
   rather than a commit.

**Nothing here is blocked on win-tooling.** The transport, its guards, its tests, its cost
controls and its deployment are done. All three remaining items are one decision each, and two
of them belong to the hub.

---

## 6 · What was NOT done (stated, not implied)

- **No hub repo edits.** `.dev-knowledge` was read only.
- **No credential entry**, no key generated, no `~/.ssh` write.
- **No existing codespace deleted.** None existed; the one created is stopped and self-deletes.
- **No old command name removed.** Every previously resolving name still resolves.
- **No `gh` flag invented.** Each was read from that command's `--help` today.
- **No hub rows or backlog edits.**
- **One RED in the suite, pre-existing and NOT from this work** —
  `test_worktree_hygiene.py::test_installer_whatif_registers_nothing`. It runs the hygiene
  installer with `-WhatIf` and asserts the scheduled task is ABSENT, failing with *"-WhatIf
  registered a real scheduled task"*. That message is a **false attribution**: measured,
  `Get-ScheduledTask 'win-tooling worktree hygiene report'` returns `State=Ready` with
  `LastRunTime 2026-08-24 11:05` — the task was really installed before this session and ran
  yesterday. `-WhatIf` registered nothing. `git diff HEAD -- scripts/worktrees/ config/worktrees/
  tests/test_worktree_hygiene.py` is empty.

  The pattern is worth naming: **a test that asserts the ABSENCE of machine-global state passes
  only until someone installs that state for real.** It shipped green two commits ago and was
  guaranteed to turn red the moment the feature it guards got adopted — the very success it
  exists to support. The fix is to record whether the task pre-existed and assert `-WhatIf` did
  not CHANGE it. Left for you: widening a Codespaces commit into someone else's test is how two
  arcs stop being reviewable.

- Suite verified **per-file**, not in one run: `test_dev_terminals_check_mode` alone takes 6m51s
  and `test_dev_terminals_path_command` 5m31s, which outlives a single run's timeout.
  **203 passed, 1 failed** (the RED above) across 15 files; `ruff` clean.

- The `Dispatch-Codespace` **success** path is proven by tests against a recorded seam, **not**
  by a live green run — no live run has yet gotten past blocker 1. Said plainly rather than left
  to be inferred from a green test count.

---

## 7 · Live end-to-end run 2 — SSH identity in place · 2026-08-25 18:01

Re-run after the operator generated `~/.ssh/codespaces.auto`. Same contract, same cost guards
(`basicLinux32gb`, `-IdleTimeout 30m`, `-Retention 24h`).

### Result: STILL BLOCKED AT THE SAME LEG — and section 4's diagnosis was WRONG

**The expected outcome did not happen.** The cp/ssh legs did **not** start authenticating, the
run did **not** reach the Claude-Code-absent guard, and **no receipt was written**. Section 4
attributed the failure to the *absence* of `codespaces.auto`. That file now exists, is loaded,
and is offered — and the codespace still refuses it. **That hypothesis is falsified**, and the
real cause is one layer further in.

### One deviation from the brief, and why

`-Slug cs-smoke-2` was passed. The contract's filename derives the slug
`cs-smoke-audit-check-count`, which is the display name run 1's codespace still carries. The
function resolves a name via `Where-Object displayName -eq $Slug` and takes `[0]` — with two
matches it could have addressed the **old, Shutdown** machine and reported a measurement against
the wrong codespace. A distinct slug removed the ambiguity. Cost guards unchanged.

**This is a real defect in `Start-DispatchCodespace`, found before it could corrupt a
measurement:** display names are not unique, and `[0]` is exactly the "guess at row 0" the
function refuses everywhere else. **Not fixed** — the brief said record and stop. The fix is
small and belongs in its own commit: match on display name **and** refuse when more than one
matches, naming both, rather than silently picking one.

### Measured timings

| Leg | Wall-time | Absolute |
|---|---|---|
| T0 → guards done | 2.1 s | 18:01:10.8 → 18:01:12.9 |
| `gh codespace create` returns | **6.1 s** | 18:01:12.9 → 18:01:19.0 |
| `gh codespace list` → name resolved | 1.3 s | 18:01:19.0 → 18:01:20.3 |
| **`gh codespace cp` (contract in) — FAILED** | **71.3 s** | 18:01:20.3 → 18:02:31.5 |
| ssh run leg | **never reached** | — |
| receipt cp-back | **never reached** | — |
| **Total** | **80.7 s** | 18:01:10.8 → 18:02:31.5 |

State transitions, polled independently every 3 s:

```
18:01:50  state=Provisioning
18:02:19  state=Available          <- time-to-Available: ~62 s from create
```

**Note the ordering, because it matters:** the codespace reached `Available` at 18:02:19 and the
`cp` leg still failed 12 s later at 18:02:31. This is not a readiness race — the machine was up
and healthy when the key was refused.

### Receipt

**None.** `C:\Users\1028120\AppData\Local\Temp\receipt-cs-smoke-2.json` does not exist; the run
never reached the runner script. The receipt gate behaved correctly: `Ok=False`,
`Failure=cp contract exited 1`, and the codespace name was reported so it could be stopped.

There is no receipt to quote verbatim. Recording that plainly rather than substituting the
console output for one.

### Cost

| | |
|---|---|
| Machine | `basicLinux32gb`, 2 cores |
| Created | 18:01:17 |
| Stopped | ~18:06 (by `Stop-DispatchCodespace`) |
| Running window | ~5 min → **~0.17 core-hours** |
| Run 1 + run 2 combined | **~0.6 of the 120 free core-hours/month** |
| Final state | `ShuttingDown` → Shutdown, `retention_period_minutes=1440` |

Both codespaces are **stopped, not deleted**, and self-delete at 24 h.

### The actual evidence, and what it now points at

`gh codespace ssh -c <name> -- -v` against the live codespace:

```
debug1: identity file C:\Users\1028120\.ssh\codespaces.auto type 2
debug1: Will attempt key: ...\codespaces.auto ED25519 SHA256:Uz+1S9LptvKMlBQezKg60qnYli1qKCkXdZ99Ylg+29U explicit
debug1: Offering public key:  ...\codespaces.auto ED25519 SHA256:Uz+1S9LptvKMlBQezKg60qnYli1qKCkXdZ99Ylg+29U explicit
vscode@localhost: Permission denied (publickey,password,keyboard-interactive).
```

The key **is** found, loaded and offered. **The codespace rejects it.** So the problem was never
key *selection* on this side — it is that nothing has authorized this key on the far side.

One measured fact is the strongest lead:

```
gh api user/keys  ->  0
```

**The GitHub account has zero SSH keys registered.** The `admin:public_key` scope is present, so
registering one is possible — it simply has never been done.

**Stated as a hypothesis, not a conclusion, because the last one was wrong:** the container's
`authorized_keys` for `vscode` is populated from a source that is currently empty, so no offered
key can succeed. The competing explanation is an interaction with the devcontainer's
`ghcr.io/devcontainers/features/sshd:1` feature — it runs its own sshd, and gh's per-session key
injection may target a different authorized_keys than the one that sshd reads. **Both are
hub/account-side; neither is a win-tooling defect**, and distinguishing them needs a shell inside
the container, which is precisely what is blocked.

Diagnosis was stopped here rather than continued on a billing clock.

### What would settle it, cheapest first

1. **Register an SSH key on the account** — `gh ssh-key add ~/.ssh/codespaces.auto.pub -t codespaces`
   — then re-run. Costs one command and ~90 s of quota, and if the theory holds the run proceeds
   to the Claude-Code guard. *(Not done: it modifies your GitHub account, which is yours.)*
2. **If that fails**, open the codespace in the browser (no SSH needed) and read
   `~/.ssh/authorized_keys` and `sudo sshd -T | grep -i authorizedkeys`. That distinguishes the
   two hypotheses directly.
3. Only then is the devcontainer's `claude`/credential gap (blockers 2 and 3) reachable.

### Standing corrections to earlier sections

- **Section 4's cause is superseded.** "gh falls back to a key the codespace has not authorized
  because `codespaces.auto` is absent" is wrong. `codespaces.auto` is present and offered, and is
  still refused. The blocker is far-side authorization, not near-side key choice.
- `-IdentityFile` remains a correct and useful parameter, but it is **not** the fix for this — the
  key it would name is the key already being offered.
- Blocker 1 in section 0's table should read: *"the codespace authorizes no key this client can
  offer"*, owner **operator/hub**, not "this workstation's `~/.ssh`".

---

## 8 · Live end-to-end run 3 — key registered · name-lookup fixed · 2026-08-25 18:17

Pre-flight, as asked:

```
gh api user/keys  ->  1
  id=161289824  title=codespaces  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEcF...
local:  SHA256:Uz+1S9LptvKMlBQezKg60qnYli1qKCkXdZ99Ylg+29U  (ED25519)
```

The registered key is byte-for-byte the one that was offered and refused in run 2 — same
fingerprint. So the registration did land on the right key.

### Result: STILL blocked at `cp` — but the failure MOVED, and that moved it onto the real cause

`Ok=False`, `Failure=cp contract exited 1`, no receipt. **Same leg, same message.** But the
verbose trace changed in one word, and that word is the whole finding:

```
run 2:  Offering public key: ...codespaces.auto ED25519 SHA256:Uz+1S9...
        vscode@localhost: Permission denied (publickey,password,keyboard-interactive).

run 3:  Offering public key: ...codespaces.auto ED25519 SHA256:Uz+1S9...
        Server accepts key:  ...codespaces.auto ED25519 SHA256:Uz+1S9...   <- NEW
        vscode@localhost: Permission denied (publickey,password,keyboard-interactive).
```

**`Server accepts key` is new.** Registering the key fixed *authorization* — the far side now
recognises it. Authentication still fails at the step after: the client must SIGN with the
private key, and that is what does not happen.

### ROOT CAUSE — reproduced locally, no codespace required

```
$ ssh-keygen -y -P "" -f ~/.ssh/codespaces.auto
Load key "~/.ssh/codespaces.auto": incorrect passphrase supplied to decrypt private key
```

**The private key is passphrase-protected.** `gh codespace cp` / `ssh` run non-interactively,
so nothing can supply the passphrase; the key cannot be decrypted, no signature is produced, and
the server denies the attempt **after** having accepted the public key. That is exactly the
signature of the trace above.

This diagnosis costs nothing to re-verify and does not need a running codespace — which is what
distinguishes it from the two that came before it.

**Why runs 1 and 2 pointed elsewhere: two independent blockers were stacked.** With the key
unregistered, the connection never reached the signing step, so the passphrase problem was
invisible behind the authorization problem. Peeling off the first revealed the second. Both of my
earlier hypotheses were wrong, and both were wrong for the same structural reason — I was
diagnosing the *outermost* failure each time and treating it as the only one.

### The fix (one command, yours to run)

```powershell
ssh-keygen -t ed25519 -N '""' -f $HOME\.ssh\codespaces.auto -C codespaces   # NO passphrase
gh ssh-key delete 161289824 --yes
gh ssh-key add $HOME\.ssh\codespaces.auto.pub -t codespaces
```

`-N ""` is the load-bearing part. Alternatively keep the passphrase and load the key into a
running `ssh-agent` — signing then happens in the agent and needs no prompt — but for an
unattended dispatch substrate a passphrase-less key scoped to codespaces is the simpler shape.

*(Not done here: it replaces a key in your `~/.ssh` and deletes a key from your GitHub account.)*

### Measured timings

| Leg | Wall-time | Absolute |
|---|---|---|
| T0 → guards done | 2.2 s | 18:17:42.1 → 18:17:44.3 |
| `gh codespace create` returns | **6.0 s** | 18:17:44.3 → 18:17:50.3 |
| `gh codespace list` → name resolved | 1.3 s | 18:17:50.3 → 18:17:51.6 |
| **`cp` (contract in) — FAILED** | **72.2 s** | 18:17:51.6 → 18:19:03.8 |
| ssh run leg | never reached | — |
| receipt cp-back | never reached | — |
| **Total** | **81.7 s** | 18:17:42.1 → 18:19:03.8 |

State transitions, polled independently every 3 s:

```
18:17:51  state=Queued
18:17:56  state=Provisioning
18:18:50  state=Available        <- time-to-Available: ~60 s from create
```

`cp` failed at 18:19:03 — **13 s after Available.** As in run 2, not a readiness race.

**Consistency across three runs** is itself a result: create returns in 6 s every time
(6.1 / 6.1 / 6.0), time-to-Available lands at ~60 s (62 / 59), and the `cp` leg burns ~72 s
before giving up. These are stable numbers for this devcontainer on `basicLinux32gb`, and they
are the D1 wall-time evidence the consolidation plan wanted — for the provisioning half. The
in-container half is still unmeasured, because nothing has yet run in there.

### Receipt

**None.** `receipt-cs-smoke-3.json` does not exist. Nothing to quote verbatim; recording that
rather than substituting console output for a receipt.

### Cost

| | |
|---|---|
| Machine | `basicLinux32gb`, 2 cores |
| Created / stopped | 18:17:48 / ~18:22 |
| Running window | ~4.5 min → **~0.15 core-hours** |
| **All three runs** | **~0.75 of the 120 free core-hours/month** |

All three codespaces are **stopped, not deleted**; each self-deletes at its 24 h retention.

### The name-lookup defect is fixed in this same commit

`Start-DispatchCodespace` no longer takes `[0]` of a display-name match. It **refuses** when more
than one codespace shares the slug, printing every candidate with its state, and says plainly
that a machine was created by that call and is billing:

```
[codespace] REFUSED -- 2 codespaces share the display name 'lane-cs-fixture'.
[codespace]   old-dead-one-111  state=Shutdown
[codespace]   fluffy-space-fishstick-abc123  state=Available
[codespace] this function will NOT guess which one it just created.
[codespace] NOTE: a codespace WAS created by this call and is billing -- it is one of the above.
```

An unparseable `gh codespace list` is now its own named refusal too; it previously fell through
to the "no codespace" message, naming the wrong cause for a real failure. **6 new tests** (32 in
the file), including one that pins the refusal lands *before* any cp/ssh leg — a refusal after
the damage is not a guard.

Run 3 used `-Slug cs-smoke-3` for the same reason run 2 used `cs-smoke-2`: earlier runs' machines
still hold the other display names.

### Standing corrections

- **Section 7's lead hypothesis ("the account has zero registered keys") is superseded.** It was
  a real gap and registering the key did change the trace — but it was not the blocker; it was
  hiding the blocker.
- Blocker 1 in section 0 now reads correctly as: **the client cannot sign, because the private
  key is passphrase-protected and the transport is non-interactive.** Owner: operator, one
  command.
- Blockers 2 and 3 (no Claude Code in the image, no credential path) remain **unmeasured** — no
  run has yet reached inside the container.

---

## 9 · Live end-to-end run 4 — THE TRANSPORT WORKS · 2026-08-25 18:42

Pre-flight:

```
ssh-keygen -y -P "" -f ~/.ssh/codespaces.auto
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICHz95NI05XaeGq+BmRmmFLG5tDaRDSWwU+cetHfF+kv
  -> decrypts with an EMPTY passphrase. This is what runs 1-3 could not do.

gh api user/keys
  id=161289824  title=codespaces        AAAAC3NzaC1lZDI1NTE5AAAAIEcF...   (old, passphrased)
  id=161292121  title=codespaces-auto   AAAAC3NzaC1lZDI1NTE5AAAAICHz...   (new, matches local)
```

### Result: every leg completed, and the receipt is the one this run existed to produce

```
[+  7.6s] created in 5s.
[+  8.9s] name=cs-smoke-4-g5rvj4w64763w5qw (display 'cs-smoke-4')
[+ 83.3s] running headless (up to 3600s)...
[+ 89.1s] run returned 1 after 6s.
[+ 89.1s] shell closed: exit status 91
[+ 95.3s] OK -- receipt in hand (57 chars)
[+ 95.3s] provision=5s run=6s machine=basicLinux32gb
```

`exit status 91` is the runner script's **own** guard code for "claude absent" — not a generic
failure. The transport reached inside the container, ran the script it shipped there, and brought
its output back.

### The receipt, verbatim

```json
{"error":"claude is not installed in this devcontainer"}
```

57 bytes, at `C:\Users\1028120\AppData\Local\Temp\receipt-cs-smoke-4.json`.

**This is blocker 2 from section 0, measured for the first time rather than inferred.** Section 1
predicted it from `grep -rc -i claude .devcontainer/* -> 0`. The container now says it in its own
words.

### Every leg, timed

| Leg | Wall-time | Status |
|---|---|---|
| Guards | 2.2 s | ok |
| `gh codespace create` | **5.4 s** | ok |
| `gh codespace list` → name | 1.2 s | ok |
| `cp` contract in + `cp` runner in | **74.4 s** | **ok — the leg that failed 3x** |
| `ssh` headless run | **5.9 s** | ran; exit 91 (guard fired) |
| `cp` receipt back | **6.2 s** | ok |
| **Total** | **95.3 s** | |

```
18:42:36  state=Queued
18:42:41  state=Provisioning
18:43:35  state=Available     <- ~60 s from create
```

The `cp` leg spans Available (18:42:36 → 18:43:50): it blocks until the container is up, then
transfers. That is why it costs ~74 s and why it was never a readiness race — in runs 2 and 3 it
reached the container fine and was refused at the key.

### Four runs, one table

| | run 1 | run 2 | run 3 | run 4 |
|---|---|---|---|---|
| `codespaces.auto` present | no | yes | yes | yes |
| key registered on account | no | no | yes | yes |
| key decrypts non-interactively | — | no | no | **yes** |
| `Server accepts key` | — | no | yes | yes |
| `cp` in | FAIL | FAIL | FAIL | **ok** |
| ssh run | — | — | — | **ok (exit 91)** |
| receipt | none | none | none | **57 bytes** |
| create returns | 6.1 s | 6.1 s | 6.0 s | 5.4 s |
| time-to-Available | ~62 s | ~62 s | ~59 s | ~60 s |

Provisioning is stable at **~5-6 s to create, ~60 s to Available**. With the transport working,
the in-container half is now measurable too: **~6 s** to ship a script in, run it and get output
back on a warm container.

### Cost

| | |
|---|---|
| Run 4 window | 18:42:33 → ~18:45, ~2.5 min → **~0.08 core-hours** |
| **All four runs** | **~0.85 of the 120 free core-hours/month** |

All four codespaces are **stopped, not deleted**; each self-deletes at its 24 h retention.

### One semantic gap this run exposes — NOT fixed, flagged

The function returned **`Ok=True`** with a receipt that says the lane could not run. That is the
receipt gate behaving exactly as specified — *"success is a receipt in hand"* — and for a
transport that is the right contract: it delivered, executed and retrieved. But a caller
branching on `Ok` alone would read this as a lane that worked.

**`Ok` means the transport succeeded, not that the work did.** The two are different questions and
this run is the first time they have had different answers. Worth an explicit second field (an
`ExitCode` from the remote run, which is already known — 91) so a caller can tell them apart
without parsing the receipt. Left alone: the brief said run once, record, stop.

### Status of the three blockers

| # | Blocker | Status |
|---|---|---|
| 1 | SSH auth | **CLEARED.** Passphrase-less key, registered. Transport works. |
| 2 | No Claude Code in the image | **CONFIRMED BY THE CONTAINER ITSELF** — the receipt above. Hub-side: one feature or one `RUN` line. |
| 3 | No credential path for a session inside | **STILL UNMEASURED** — unreachable until 2 is fixed. Deserves a ruling, not a commit: a Codespaces secret holding a long-lived key is readable by any lane that runs there. |

### Standing corrections

- Sections 4, 7 and 8 each named a cause that turned out to be a layer of the same stack:
  key *absent* (4, wrong), key *unregistered* (7, real but not the blocker), key *passphrased*
  (8, correct). Only the last one, reproduced locally with `ssh-keygen -y`, actually predicted
  the fix — and this run confirms it.
- Section 0's "does not yet complete a lane" now needs one qualification: **the transport
  completes; the lane cannot, and the container says why.**
