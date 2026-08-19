# [#554] D1/D2 proof — Codespaces stage-1 run and the off-Codespaces wall

**Lane:** J (worktree `worktree-lane-j-554-proof`) · **Date:** 2026-08-19 · **Mode:** execute,
commit-and-STOP · **Contract of record:** `docs/audits/2026-08-19-technical-554-proof-lane-contract.md`
(commit `b60b5528`, first commit of the lane, per ADR-110).

**Row closure is NOT this lane's act.** What follows are the measured D1 and D2 states and the
artifact changes the measurement forced. `[#554]` is left open; nothing here closes it.

---

## 0. Verdicts, up front

| Leg | Verdict | One-line reason |
|---|---|---|
| D1 provisioning (the four legs + C1/C2) | **GREEN** | `provision.sh --gate` self-asserted `uv 0.11.19, full history, three hook types armed, stamp current` in a clean (non-recovery) container |
| D1 `audit.py health` | **RED (exit 1)** | 2 FAILs, both artifacts of a fresh single-branch, single-repo clone — not governance gaps |
| D1 `pytest -m "not slow"` | **RED (exit 1)** | 8 failed / 3008 passed / 9 skipped / 1 xfailed — 5 clone-shape, 1 pre-existing, **2 genuine Linux-only defects** |
| D1 as the row's Done-when reads it | **NOT MET** | the Done-when says *both* green; neither is, and one reason is structural (see §4) |
| D2 `devcontainer up` off-Codespaces | **BLOCKED** | no container runtime on the workstation; wall captured verbatim in §5 |

**The headline is not the two REDs.** It is that the substrate *worked* — a lane provisioned
correctly off this machine on the free tier — and that running the suite off Windows for the
first time immediately surfaced **two cross-platform defects that the Windows suite cannot see**
(§4.3). That is the stage-1 result the substrate decision needs.

---

## 1. What had to be fixed before D1 could run at all

D1 was unreachable as landed. Three codespaces were consumed establishing why.

### 1.1 The symptom
A codespace built from the landed `.devcontainer/devcontainer.json` comes up `Available` and is
then reachable **only from a browser**. Both CLI doors refuse, identically:

```
gh codespace ssh  -> error getting ssh server details: failed to start SSH server:
                     Please check if an SSH server is installed in the container.
gh codespace logs -> (same error — `logs` is transported over the same ssh channel)
```

Reproduced twice on codespace `stunning-train-54r7jgp54xvfv46v`. With no shell and no log
channel, an agent lane cannot be driven on the substrate and the provisioning that
`provision.sh` asserts cannot even be read.

### 1.2 The root cause — one upstream defect, two blast radii
From the creation log of `fuzzy-space-spork-w95qprj5wxqc9jq7`, verbatim:

```
#12 0.885 Err:4 https://dl.yarnpkg.com/debian stable InRelease
#12 0.885   The following signatures couldn't be verified because the public key is not
            available: NO_PUBKEY 62D54FD4003F6525
#12 2.314 E: The repository 'https://dl.yarnpkg.com/debian stable InRelease' is not signed.
#12 2.315 ERROR: Feature "SSH server" (ghcr.io/devcontainers/features/sshd) failed to install!
```

The pinned base image `mcr.microsoft.com/devcontainers/python:1-3.12-bookworm` ships an apt
source for the yarn Debian repo whose signing key is no longer in the image keyring, so
**`apt-get update` inside the container exits non-zero**. That single defect walls two separate
things:

1. **Codespaces' own on-demand SSH installer.** `/workspaces/.codespaces/.persistedshare/installSSH.sh`
   line 125 reads `if ! aptSudoIf "update"; then` — it aborts, which is the *entire* reason
   `gh codespace ssh` reports "no SSH server". Nothing about our devcontainer asked for this;
   Codespaces installs sshd on demand and simply could not.
2. **Every devcontainer FEATURE install.** The first repair attempt — declaring
   `ghcr.io/devcontainers/features/sshd:1` — hit the same apt failure, exited 100, failed
   `docker buildx build`, and Codespaces **silently replaced the container with an alpine
   RECOVERY container**.

### 1.3 The recovery-container trap (the worst failure shape here)
The recovery container reports `state: Available` through the API and answers ssh once sshd is
present, but it is a *different image*: no `uv`, no `.venv`, `git rev-parse --is-shallow-repository`
still `true`, and no provisioning stamp. **`provision.sh` never ran, and nothing said so.** This
is precisely the failure shape `[#554]` exists to close — an environment that looks up and whose
gates are vacuous — arriving through a door the four legs do not watch, because the legs run
*inside* a container that was never built. Recorded as a substrate property, not as a script bug:
`waitFor` cannot gate a container that was replaced.

### 1.4 The fix that worked
`.devcontainer/Dockerfile` (new, commit `1c6e07cc`) — drop any apt source pointing at the
unsigned yarn repo, then re-run `apt-get update` as the assert so a build fails loudly instead of
handing a lane an unreachable container. `devcontainer.json` builds it rather than using the
image directly; **the pinned tag is unchanged**, moved verbatim into the `BASE_IMAGE` arg, so the
file still carries exactly one version token. Checked live against the MCR tag list on
2026-08-19: the `1-3.12` line offers only `bookworm` and `bullseye`, so moving tags was not an
available fix. The `sshd` feature is kept (commit `b3060764`) — with apt healthy it builds, and it
makes ssh deterministic at build time instead of dependent on Codespaces' on-demand installer.
Both changes are portable: `devcontainer up` on a VPS builds the same Dockerfile.

**Authorization note:** the operator was asked before any of this landed and chose *"push a probe
branch, run D1"*. The probe branch `chore/554-sshd-probe` was pushed to `rdwornik/dev-knowledge`,
used as the codespace source, and **deleted at the end** (verified: the remote now lists only
`automation/fleet-audit`, `claude/n4-grooming-wave1-audit-ahltfa`, `main`,
`worktree-lane-x-539-cloud-briefs`). `main` was never touched.

---

## 2. D1 — machine, timings, provisioning evidence

Codespace `super-duper-chainsaw-9q5gr74w9q9hp67r`, created from `chore/554-sshd-probe`.

| Measurement | Value |
|---|---|
| Machine type (smallest offered) | `basicLinux32gb` — 2 cores, 8 GB RAM, 32 GB storage |
| Machine types offered at all | `basicLinux32gb`, `standardLinux32gb` only |
| Billing line printed by `gh` | `Codespaces usage for this repository is paid for by rdwornik` |
| Create → API returns name | ~6 s (three creations: 6 s, 6 s, 5 s) |
| Create → state `Available`, **image only** (no Dockerfile, no features) | **~101 s** |
| Create → state `Available`, **Dockerfile + sshd feature** | **~144 s** |
| Create → state `Available`, final (build + feature + provision.sh) | **~125 s** |
| `audit.py health` wall time | **14 s** |
| `pytest -m "not slow"` wall time | **274 s (4 m 34 s)** on 2 cores |
| Host | `codespaces-a9646a`, Debian GNU/Linux 12 (bookworm), 7943 MB |

Provisioning evidence, verbatim from `/workspaces/.codespaces/.persistedshare/creation.log`:

```
bash .devcontainer/provision.sh --gate
[provision] gate: re-asserting the four legs against ${containerEnv:HOME}/.dev-knowledge-provision-stamp
[provision] L3 resolved hooks dir: /workspaces/dev-knowledge/.git/hooks
[provision] gate OK — uv 0.11.19, full history, three hook types armed, stamp current
Outcome: success User: vscode WorkspaceFolder: /workspaces/dev-knowledge
devcontainer process exited with exit code 0
```

and independently re-measured from inside the container:

```
uv: uv 0.11.19 (x86_64-unknown-linux-gnu)
uv pin (pyproject [tool.uv] required-version): "==0.11.19"      <- L1 holds, ADR-106
python pin (.python-version): 3.12.10
python in venv: 3.12.10                                          <- exact interpreter
shallow: false   commits: 5329                                   <- L2 holds
hooks: commit-msg pre-commit pre-push                            <- L3 holds
```

**All four legs + the C1/C2 obligations assert clean on the Codespaces free tier.** That part of
the row's Done-when is met and is the substantive stage-1 result.

### 2.1 Defect found in passing: the stamp path is never expanded
The gate line above prints its stamp path as the **literal** string
`${containerEnv:HOME}/.dev-knowledge-provision-stamp`. Codespaces does not expand
`${containerEnv:HOME}` in `containerEnv` (a variable cannot reference the block it is being
defined in), so `DEV_KNOWLEDGE_PROVISION_STAMP` reaches `provision.sh` unexpanded. The script's
`mkdir -p "$(dirname "${STAMP}")"` then creates a directory *named* `${containerEnv:HOME}` — and
because provisioning runs with the repo as cwd, it lands **inside the working tree**:

```
stray dirs in worktree:
?? ${containerEnv:HOME}/
```

Consequences, stated honestly: the stamp still works (write and read agree on the same wrong
path, so `--gate` is not fooled), but every container starts with an untracked junk directory in
the repo, and the stamp does not survive to `$HOME` as the comment in `devcontainer.json` says it
does. **Not fixed by this lane** — it is a live defect in the row's own artifact and belongs to
whoever disposes of `[#554]`, not to a proof lane. The one-line fix is to drop the
`containerEnv` declaration and let `provision.sh` keep its `${HOME}/...` default, which already
resolves correctly.

---

## 3. D1a — `audit.py health` = RED (exit 1), both FAILs environmental

`health: DEGRADED`, self-audit 38/74 pass. Exactly two `[!!]`:

```
[!!] repos registered  (none)
[!!] journal_spine_anchor: backstop could not complete (AnchorError('disposition floor 24882f8cc
     is not an ancestor of main: git merge-base --is-ancestor 24882f8cc main exited 128:
     fatal: Not a valid object name main')) -- an unknown anchoring state is not a clean one (ADR-85 §A6)
```

plus a related WARN:

```
[~~] review_artifact_coverage: could not scan: AnchorError("git log --first-parent --format=%H %ct
     main exited 128: fatal: ambiguous argument 'main': unknown revision or path not in the working tree.")
```

Both FAILs are properties of the **clone shape**, not of the repo's health:

1. `repos registered (none)` — the hub's operational check expects the *fleet* (sibling consumer
   repos) to exist beside it. A container holds one repo. Structurally unsatisfiable in a
   single-repo substrate.
2. `journal_spine_anchor` — a codespace clones **only the branch it was created from**, so there
   is no local `main` ref and the anchoring predicate cannot resolve its floor. It then fails
   CLOSED, exactly as ADR-85 §A6 requires. Correct behaviour, wrong premise.

**This is the load-bearing finding for the row's Done-when.** `git fetch --unshallow` (leg 2)
restores *depth* but not *branches*: 5329 commits are reachable, and `main` still does not exist
as a ref. Leg 2's own rationale — "the gates read history; on a shallow clone they are vacuous" —
turns out to have a second half nobody measured: a single-branch clone makes the branch-reading
gates *error* rather than pass vacuously. Deliberately **not** fixed here, because the fix is a
design choice between at least three options and belongs to the row's owner:
(a) provision.sh fetches all branches (`git fetch origin +refs/heads/*:refs/remotes/origin/*` plus
a local `main`), (b) the checks tolerate a missing `main` in a container, or (c) D1's green
predicate is re-scoped to something a single-repo container can satisfy. Note that (a) alone does
**not** turn D1a green — `repos registered (none)` survives it.

---

## 4. D1b — `pytest -m "not slow"` = RED (exit 1)

```
8 failed, 3008 passed, 9 skipped, 1 xfailed in 273.80s (0:04:33)
```

Every failure was classified, and the ambiguous ones were **re-run on the Windows workstation at
the identical commit** to split "the container did this" from "this was already broken".

### 4.1 Clone-shape failures (5) — same cause as §3
```
tests/test_boundary_report.py::test_live_hub_baseline_and_consumers_legal
    E   AssertionError: expected >=1 registered consumer / assert []
tests/test_audit.py::test_health_ok_with_registered_repo               assert 1 == 0
tests/test_audit.py::test_health_stays_ok_with_na_status               (health DEGRADED dump)
tests/test_audit_parallel.py::test_health_accepts_the_parallel_flags_and_defaults_to_serial
tests/test_validate_branch_naming.py::test_local_branches_reads_the_live_repo
    E   AssertionError: assert 'main' in ['chore/554-sshd-probe']
```
The last one is the cleanest statement of the whole class: the container's git simply has one
branch. The three `test_audit*` ones fail because they invoke `cmd_health`, which is RED for §3's
reasons.

### 4.2 Pre-existing, not a substrate finding (1)
```
tests/test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row
    E   AssertionError: assert '1 declared routine row' in '3 declared routine row(s) name a
        consumer and a consumption_path (live hooks/schedules out of scope — [#426])'
```
**Verified to fail identically on Windows** at the same commit (`1 failed, 2 passed in 9.38s`).
A stale pin: the test's docstring says the number moving means the ADR, the docstring and
`[#426]` move with it, and it has moved 1 → 3. Reported, not fixed — out of this lane's scope.

### 4.3 Genuine Linux-only defects (2) — the finding the substrate bought
Both **PASS on Windows** at the same commit and **FAIL on Linux**. Neither is visible to any run
on the current workstation.

```
tests/test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration
    E   At index 0 diff: {'file': '../../:orkspaces/dev-knowledge/scripts/audit.py', 'line': 312}
                      != {'file': 'scripts/audit.py', 'line': 312}
```
The URI→path conversion assumes a Windows drive letter: given `file:///workspaces/...` it eats
`/w` as the drive and produces the corrupted `:orkspaces`. The reverse-dependency oracle
therefore reports garbage paths on any non-Windows host.

```
tests/test_merge_serialization.py::test_index_lock_blocks_concurrent_merge
    E   AssertionError: assert 'index.lock' in ('fatal: Unable to write index.\n' + '')
```
The test pins git's *Windows* error text; Linux git words the same condition differently, so the
assertion cannot match.

**Interpretation for the substrate decision:** the first off-machine run of this suite paid for
itself immediately. Two platform assumptions had been invisible because every run to date has
been on one Windows workstation — which is the exact monoculture `[#554]`/`[#541]` exist to end.

---

## 5. D2 — `devcontainer up` off-Codespaces = **BLOCKED**, wall recorded

Attempted per the contract's authorized fork. The devcontainer CLI leg is satisfiable with no
install (`npx` fetch, no system change, nothing added to the repo):

```
$ npx --yes @devcontainers/cli@latest --version
0.88.0
```

The runtime leg is not:

```
$ npx --yes @devcontainers/cli@latest up --workspace-folder .
[2026-08-19T12:44:50.884Z] @devcontainers/cli 0.88.0. Node.js v25.2.1. win32 10.0.26200 x64.
Error: Exectuable 'docker' not found on PATH '...'          <- upstream's typo, quoted verbatim
{"outcome":"error","message":"Exectuable 'docker' not found on PATH ...",
 "description":"An error occurred setting up the container."}
```

Corroborating probes, so the wall is characterised rather than asserted:

- `docker`, `podman`, `nerdctl` — **none on PATH**.
- `C:\Program Files\Docker`, `C:\Program Files\RedHat\Podman`,
  `%LOCALAPPDATA%\Programs\Docker` — **none exist**; no runtime is installed but unlinked.
- WSL2 is present and is the default version, but `wsl -l -v` reports
  **"Windows Subsystem for Linux has no installed distributions"** — there is no Linux to host a
  daemon.
- `Get-WindowsOptionalFeature -Online -FeatureName Containers` → **"The requested operation
  requires elevation"**; the session has no admin rights to inspect, let alone enable, the
  container features.

Per the contract, **no container runtime was installed system-wide to force this**.

**D2's remaining path is unchanged and now sharper.** The identical-script clause is *partly*
discharged already: the same two files were consumed on Codespaces by `@devcontainers/cli 0.83.3`
running `devcontainer up` — that is the same CLI and the same spec path a VPS uses, just driven
by GitHub's agent. What is untested is a host we control end to end. Feeding today's
Enterprise probe, the two candidates are unchanged: a Hetzner CX VPS (intake #39 §"fastest path"
prices CX53 at ~€0.0473/hr, €29.49/mo cap) or an Enterprise codespace. §2's numbers are the
inputs to that comparison — 2 cores is what the free tier gives, and it runs the suite in 4 m 34 s.

---

## 6. Artifact changes this lane made, and what it deliberately did not touch

Landed on `worktree-lane-j-554-proof`, each with its rationale in the commit body:

| Commit | Change |
|---|---|
| `b60b5528` | contract of record (ADR-110 first commit) |
| `c53b6190` | sync-merge of `main` — cleared lane tree-lag that FAILed `journal_spine_anchor` on the S-1 arc's spine entry `7e793eca`; no `SKIP=` used for it |
| `b3060764` | `.devcontainer/devcontainer.json` declares the `sshd` feature |
| `1c6e07cc` | `.devcontainer/Dockerfile` repairs the base image's apt; `devcontainer.json` builds it |

**Not touched, on purpose:** the `${containerEnv:HOME}` stamp defect (§2.1), the single-branch
clone gap (§3), the stale `routine_consumers` pin (§4.2), and the two Linux-only defects (§4.3).
Each is reported with its evidence; each is a disposition, and dispositions are the seat's act.
`BACKLOG.md` is unchanged and `[#554]` is left open. No JOURNAL entry: a lane does not journal,
the integrator anchors the arc (`STANDING_RULINGS` §P-1).

**Gate honesty.** Three commits carry a declared `SKIP=audit-health`, and the reason is foreign to
this lane: `fleet_audit_replication` FAILs because `automation/fleet-audit` is 5 commits ahead of
origin (`760da0f8 9b4a7511 44b75818 7c2a2b25 c2fcd451`, all `chore(routine/fleet-audit): record
2026-08-19 baseline` from today's organ run) — a branch this lane never touched, on a
tree-independent check. It was the only `[!!]` in each run; `journal_spine_anchor` passed once the
sync-merge landed. No `--no-verify` was used anywhere, and both pre-push organs passed on the
probe-branch pushes.

---

## 7. Environment defects worth recording (not `[#554]`'s, but they cost this lane time)

1. **`~/.ssh/config` carries a UTF-8 BOM.** Every `ssh` invocation on the workstation dies with
   `Bad configuration option: \357\273\277host`, which also kills `gh codespace ssh`'s key
   selection (`ssh -G`) before it starts. Worked around session-locally with a PATH shim over a
   BOM-free copy; **the user's file was not modified**. Worth a one-byte fix by the operator —
   the config is currently non-functional for all ssh use, not just this lane's.
2. **`rdwornik` has no SSH public key registered** (`https://github.com/rdwornik.keys` is empty),
   so gh's normal key path has nothing to fall back on. A throwaway keypair passed with `-i`
   works, because gh hands the chosen public key to the codespace.
3. **The `gh` active account flipped underneath this session** more than once — a concurrent
   process switched it back to `Robert-Dwornik_ghub`, which made a live codespace appear to
   vanish (`gh codespace list` empty, then a 404). Every later call pinned
   `GH_TOKEN=$(gh auth token -u rdwornik)` explicitly. Anyone scripting codespace work from this
   machine should do the same rather than trusting `gh auth switch`.
4. **Unexplained, and left unexplained:** the first codespace `silver-lamp-j47pvjw95v5fpvqg`
   reached `Available` at 11:45:45Z and was absent from the account by 11:49Z, with no delete
   issued by this lane. It is recorded as an anomaly; no cause is asserted for it.

---

## 8. Resource hygiene

- Codespaces created: 3 (`silver-lamp-j47pvjw95v5fpvqg`, `stunning-train-54r7jgp54xvfv46v`,
  `super-duper-chainsaw-9q5gr74w9q9hp67r`). **All gone** — `gh codespace list` returns empty.
- Probe branch `chore/554-sshd-probe`: pushed, used, **deleted**; verified absent from the remote
  branch list.
- `gh` active account restored to `Robert-Dwornik_ghub` (the account active at lane start).
- Nothing was installed system-wide; the `npx` fetch touched only the npm cache.
