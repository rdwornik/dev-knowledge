# Night-2 research — single-flight guards, pytest-xdist on Windows, and the [#527] anti-direct-to-main hook

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** This document decides nothing, adopts nothing, and births no BACKLOG row.
> No config file, dependency, hook or protocol was edited by the lane that produced it.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-14
- **Lane:** `claude/night2-research-d30vhu` (Anthropic cloud session, Linux container), night2-D research lane
- **Base:** `main` @ `7bbb067` · working tree clean before and after
- **Model:** Opus 5 · web search permitted · **no adoption, no config edits — evidence only**
- **Answers three bounded questions.** Each carries: recommended approach · current version ·
  Windows/uv compatibility · minimal integration sketch · do-not-adopt alternatives with the
  one-line reason.

---

## 0. Method, and the honest limits of it

**Library-first ladder applied as stated:** stdlib > established dependency > stabilized project >
industry pattern. Where a recommendation steps *down* the ladder, §1–§3 give the measured reason
for the demotion rather than a preference.

**What is first-party here.** Eleven git experiments (T1–T10, E1–E5, W1) were run live in this
container against throwaway repos, and their verbatim output is in §4. They are the load-bearing
evidence for §1 and §3 — not citations, not recollection. Four upstream source files were read
directly from `raw.githubusercontent.com` rather than summarised from docs, because the
Q2 finding lives in a `Popen` call, not in prose.

**Four limits, stated up front because each bounds a recommendation:**

1. **This lane runs on Linux.** Every Windows claim in §2 is derived from upstream *source* and
   from an upstream Windows bug report, not from a Windows run. Nothing in §2 was reproduced on
   the operator's host, and the report says so at each point.
2. **The §1 git-lock mechanism was verified against a local bare remote**, not against GitHub.
   The compare-and-swap is git protocol, not a GitHub feature, so it should hold — but §5 names
   the exact one-line probe that would close this, and it is deliberately not run here, because
   it would create and delete a ref on the shared `origin` and this lane is evidence-only.
3. **`readthedocs.io` is blocked by this container's egress proxy.** Upstream docs were read from
   GitHub raw instead. No claim in this report rests on a source that could not be reached.
4. **Scratch hygiene (core-invariant #9):** every probe repo and every probe worktree created by
   this lane was removed and removal verified (§4, W1 and the closing check). The tree is
   identical to how the lane found it apart from this file and the regenerated audit index.

---

## 1. SINGLE-FLIGHT guard for duplicate contract executions

### 1.1 The failure this has to stop

Witnessed 2026-08-14 (`JOURNAL.md` entry (d)): **three independent executions of one contract were
live at once** — a `local_agent` on `docs/packet-close-v2` in its own isolated worktree, a resumed
agent with no verifiable result, and the session that recorded it. Two of them independently
allocated `[#526]`–`[#529]` for the same four filings. The executions did not share a working tree,
and at least one pair did not share a machine.

That last clause is the whole problem. **Every filesystem-lock library in the candidate set is
single-host by construction.** A guard that only works on one machine does not address the
collision that was actually observed.

### 1.2 Behaviour of each candidate across worktrees and across machines

Stated explicitly, as the brief asks. "Cross-worktree" means two worktrees of one clone;
"cross-machine" means the cloud container and the operator's Windows host.

| candidate | cross-worktree (same clone) | cross-machine (cloud + local) | why |
|---|---|---|---|
| `filelock` `FileLock` | **works, with care** | **no** | `fcntl.flock` / `msvcrt.locking` are kernel-local. Works across worktrees only if the lock path is a shared absolute path — worktrees have separate working dirs, so a repo-relative path silently gives each worktree its *own* lock |
| `filelock` `SoftFileLock` | works | **no** | existence-marker on a filesystem; the two hosts share no filesystem |
| `portalocker` `Lock` | **works, with care** | **no** | same kernel-local primitives, same shared-path caveat |
| `portalocker` `RedisLock` | works | yes | but only by standing up a Redis server — new always-on infrastructure |
| atomic `O_EXCL` lockfile (stdlib) | **works, with care** | **no** | same shared-path caveat; blind past the local filesystem |
| **git ref as lock, pushed to `origin`** | **works** | **works** | the arbiter is the remote, which is the only substrate both hosts share |
| `git update-ref` (local only) | **works** | **no** | refs live in the *common* git dir, so worktrees of one clone contend correctly — but never across clones |
| step-0 contract-of-record commit alone | **no** | **no** | see 1.3 — this is the candidate the brief names, and it is the one that does not work |

### 1.3 Why the step-0 contract-of-record commit is *not* the lock (and what to do about it)

The brief asks whether the existing step-0 commit (ruling `I-D3`, `protocols/STANDING_RULINGS.md:973`
— "a batch-4 lane contract is COMMITTED to the repo before dispatch") can serve as the mutex.
**It cannot, and the JOURNAL already records the counter-example.** On 2026-08-11 (entry (j)) three
lanes each committed their contract of record — `e0de6bba`, `d4d814e7`, `93c96471` — onto *their own
lane branches*. Branches do not contend. Three contract-of-record commits for one batch coexisted
without any of them noticing the others.

The fix is small and keeps I-D3 intact: **keep the commit, and add one shared ref that the commit
claims.** A commit is a fact; a ref is a name, and a name is the only thing two parties can fight
over. The ref then *points at* the claiming lane's contract-of-record commit, so `git show
refs/locks/<id>` names the holder, its message, and its time — the lock is self-documenting from the
artifact I-D3 already requires.

### 1.4 Recommended approach

**A git ref used as a distributed compare-and-swap, claimed with `--force-with-lease=<ref>:`
(empty expect = "the ref must not already exist"), pushed to `origin`.**

Proven live, §4 T1–T5. The decisive property is **T2**: a second clone that has *never fetched the
lock ref* is still refused, because the expectation is evaluated by the receiving repo, not by the
pusher. The racer does not need to know the lock exists. That is what makes it work across machines,
and it is the property no filesystem lock has.

**The trap that makes this a real finding rather than an obvious one — T4.** A plain
`git push origin HEAD:refs/locks/<id>` onto an already-held lock, *when both sessions sit at the same
commit*, returns `Everything up-to-date` and **exit 0**. A naive implementation reads that as "lock
won". And same-base is not an edge case — it is the normal batch-dispatch state, where N lanes fork
from one HEAD. Verbatim output in §4. `--force-with-lease=<ref>:` is therefore not a hardening detail;
it is the entire mechanism.

**Current version:** none — this is `git` itself. Verified on **git 2.43.0**. The empty-expect form
of `--force-with-lease` is long-standing; the repo's floor is whatever git the fleet already runs.
**Zero new dependencies**, which is the top rung of the ladder ahead of both `filelock` and
`portalocker`.

**Windows/uv compatibility:** nothing to install, nothing to resolve, no `uv.lock` change, no
`ecosystem/dependency-baseline.yaml` row. `git push` behaves identically on Git-for-Windows. The one
genuine cost is that **step 0 now needs network** — true for both the cloud lane and the local host
today, but it is a new precondition on a gate, and a gate with a new failure mode should be ruled
on, not slipped in.

### 1.5 Minimal integration sketch (18 lines of body)

```python
# scripts/single_flight.py — step-0 gate. 0 = claimed, 3 = already in flight, 2 = internal error.
import subprocess, sys

def claim(contract_id: str, remote: str = "origin") -> int:
    ref = f"refs/locks/{contract_id}"
    # `--force-with-lease=<ref>:` with an EMPTY expect means "this ref must not exist".
    # Plain `git push` is NOT equivalent: it exits 0 on a same-commit race (see T4).
    r = subprocess.run(["git", "push", f"--force-with-lease={ref}:", remote, f"HEAD:{ref}"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return 0
    if "stale info" in r.stderr or "non-fast-forward" in r.stderr:
        held = subprocess.run(["git", "ls-remote", remote, ref],
                              capture_output=True, text=True).stdout.split()
        print(f"SINGLE-FLIGHT REFUSAL: {ref} already held by {held[0][:8] if held else '?'}\n"
              f"  inspect: git fetch {remote} {ref} && git show FETCH_HEAD\n"
              f"  release: git push {remote} :{ref}", file=sys.stderr)
        return 3
    print(f"single_flight: internal error — {r.stderr.strip()}", file=sys.stderr)
    return 2   # fail CLOSED, matching block_ff_push's posture since ADR-85 amend. 2026-08-03 §A6

if __name__ == "__main__":
    raise SystemExit(claim(sys.argv[1]))
```

Release is `git push origin :refs/locks/<contract-id>` (T5 proves delete-then-reclaim works).
Fail-closed on internal error is chosen deliberately: `block_ff_push` was changed to exit 2 on
internal error precisely because "degraded — allowing" silently auto-allowed the thing it existed
to refuse (`CLAUDE.md` §9).

**Stale-lock residual, stated not hidden.** A lane that dies without releasing leaves the ref held.
There is no TTL in git. Two honest options, neither adopted here: (a) the refusal message already
prints how to inspect and release, so a stale lock is a 10-second operator action with the holder's
identity visible; (b) if that proves too manual, embed a claim timestamp in the ref's target commit
and let the gate print the age. Option (a) is the smaller mechanism and matches how the repo already
handles `--no-verify` — an escape that is loud rather than absent.

**Optional same-machine fast leg.** If a network-free pre-check is wanted, `git update-ref --stdin`
with the `create` verb gives cross-worktree single-flight on one clone with no network at all
(T6/T7: the second `create` from a *worktree of the same clone* fails with `fatal: cannot lock ref
… reference already exists`, **exit 128** — note 128, not 1). Do **not** reach for
`refs/worktree/…`: T9 proves that namespace is per-worktree and invisible to the primary, which is
the exact opposite of what a lock needs.

### 1.6 Do-not-adopt, with the one-line reason

- **`filelock` (3.32.3, 2026-08-13, Python ≥3.10)** — process-lifetime kernel lock on one host; it
  cannot see a peer on another machine, and a step-0 gate is not a long-lived process to hold it.
  *(Worth knowing: `filelock 3.32.0` is **already in `uv.lock`** transitively, so it is free if a
  same-machine need ever appears — and it is what pytest-xdist's own how-to recommends for
  cross-worker fixture coordination, §2.5.)*
- **`filelock.SoftFileLock`** — its portability comes from being a mere existence marker on a shared
  filesystem; there is no shared filesystem between the cloud container and the Windows host.
- **`portalocker` (4.1.0, 2026-08-02, Python ≥3.10)** — same single-host ceiling as `filelock`, plus
  it wants `pywin32` for shared locks on Windows; nothing gained for a new dependency.
- **`portalocker.RedisLock`** — genuinely cross-machine, but stands up an always-on Redis server to
  arbitrate three lanes, and a Layer-2 repo that "never executes" (ADR-28/36) should not acquire a
  service dependency for a governance gate.
- **Bare `O_EXCL` lockfile** — correct, stdlib, and already used well in
  `scripts/fleet_health.py:730` (three recorded refinement passes of hard-won commentary), but it is
  blind past the local filesystem and so cannot see the collision that was actually witnessed.
- **Plain `git push` of a lock ref (no lease)** — T4 proves it returns exit 0 on the same-HEAD race,
  which is exactly the batch-dispatch case it would be deployed into.
- **`git update-ref` alone** — local-only; correct across worktrees, never across clones.
- **GitHub Actions `concurrency:` group** — arbitrates CI jobs; the collision happened between agent
  sessions, entirely outside CI.
- **A BACKLOG/manifest "claimed" marker or naming convention** — advisory, not atomic; the witnessed
  failure is precisely two parties each concluding they may proceed.

---

## 2. pytest-xdist on Windows

### 2.1 Worker leaks — the root cause, read from upstream source

This is the finding this section exists for, and it is not in any changelog. **execnet launches every
worker with a bare `Popen`:**

```python
# execnet/gateway_io.py — Popen2IOMaster.__init__
self.popen = p = execmodel.subprocess.Popen(args, stdout=PIPE, stdin=PIPE)
```

There is **no `CREATE_NEW_PROCESS_GROUP`, no Windows Job Object, and no `start_new_session`.** The
worker is an ordinary orphan-able child. Cleanup runs only on the graceful path —
`xdist/workermanage.py` `NodeManager.teardown_nodes()` → `execnet.Group.terminate(EXIT_TIMEOUT)` with
`EXIT_TIMEOUT = 10`, which joins each gateway and calls `gw._io.kill()` (i.e. `Popen.kill()`) on
timeout.

Two consequences, both Windows-specific in effect:

- **If the controller never reaches teardown — closed terminal, `TaskStop`, Ctrl-C in a git hook, an
  external gate timeout — nothing kills the workers at all.** Windows does not tear down a process
  tree when a parent dies. The workers survive holding open pipes.
- Even on the graceful path, `Popen.kill()` on Windows is `TerminateProcess` against **that one
  process** — it does not reach anything the worker itself spawned. This suite spawns real `git` and
  `pre-commit` subprocesses under the `slow` marker (`pyproject.toml:102`), so a killed worker can
  still leave grandchildren.

### 2.2 Worker *multiplication* — why the count reaches 19

`--max-worker-restart` is not off by default. From `xdist/dsession.py`:

```python
def get_default_max_worker_restart(config) -> int | None:
    result_str = config.option.maxworkerrestart
    if result_str is not None:      result = int(result_str)
    elif config.option.numprocesses: result = config.option.numprocesses * 4
    else:                            result = None
```

**The default restart budget is `numprocesses × 4`**, and each crash prints `replacing crashed worker
gwN` and clones a fresh one. A suite running `-n auto` on a 5-physical-core host carries a silent
budget of 20 replacements on top of the 5 originals. **19 stray workers is squarely inside what this
default permits** — it does not require anything exotic, only a hang plus the default.

Corroborated upstream on Windows: **pytest-xdist issue #1094** (open, filed 2024-06-10; win32,
Python 3.11.6, xdist 3.6.1, pytest-timeout 2.2.0, 6 workers with `loadgroup`) reports the worker
count climbing 6 → 8 via `replacing crashed worker`, then the run stalling ~30 minutes with workers
alive and blocked in `work_queue.get(block=True)` and execnet socket reads. Same shape, smaller
numbers.

### 2.3 Strays are exactly identifiable — do not sweep by image name

execnet's bootstrap line is a constant, so a stray xdist worker has a unique, greppable command line:

```
popen_bootstrapline = "import sys;exec(eval(sys.stdin.readline()))"
# argv: <python> -u [-B] -c "import sys;exec(eval(sys.stdin.readline()))"
```

That means a precise detection sweep is possible, and a blunt one is unnecessary and dangerous
(a `taskkill /IM python.exe` would take out the operator's live Claude Code session interpreter):

```powershell
# DETECT (read-only)
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Where-Object { $_.CommandLine -like '*exec(eval(sys.stdin.readline()))*' } |
  Select-Object ProcessId, CreationDate, CommandLine
# CLEAN (per-PID, with the tree, only after reading the list above)
#   taskkill /F /T /PID <pid>
```

`/T` matters: it takes the descendants the `slow` tests spawn, which `Popen.kill()` would leave.

### 2.4 tmp-path races

**Largely a non-hazard *if* the fixtures are used, and a real one if they are bypassed.**
`tmp_path_factory.mktemp()` embeds the worker id and numbers directories, and pytest configures a
per-run `basetemp` for xdist subprocesses, so `tmp_path` / `tmp_path_factory` cannot collide across
workers.

Two things that *do* race, and both are live in this repo:

- **Session-scoped fixtures run once per worker, not once per run.** xdist has no built-in
  single-execution guarantee; its own how-to prescribes a `FileLock` around the expensive half, with
  the losers reading the winner's file. Relevant only if a session-scoped fixture here builds shared
  state — worth a targeted grep before the [#528] rollout, not assumed either way by this lane.
- **Tests that assert against the live repo tree.** The `live_repo` marker
  (`pyproject.toml:101`) marks exactly the tests whose "shared temp directory" is the actual working
  tree, and no `tmp_path` machinery helps there. `--dist loadfile` (or `loadgroup` + an
  `xdist_group` marker) keeps such tests on one worker. This is the specific class the [#528]
  rollout should tier rather than parallelise blindly.

There is already one measured instance of the class on record: `test_linked_worktrees_reader_
excludes_the_primary` is documented in `JOURNAL.md` (2026-08-14 (d)) as failing in a worktree-isolated
run and not in a primary-checkout run.

### 2.5 Coverage integration

**Currently a non-issue here, and that is a first-party check, not an assumption:** `pytest-cov`,
`coverage` and `psutil` are all **absent from `uv.lock`**. Record it as a precondition for whenever
coverage is added rather than as a present hazard: pytest-cov detects xdist workers and combines
their data automatically at the end of the run, *provided* `parallel = true` is set in the coverage
config so each worker writes its own suffixed data file. Without it the numbers come out deflated
rather than erroring — a silently wrong gate, which is the worst failure shape for this repo.

### 2.6 Settings that make xdist safe in a git-hook / gate context

Ordered by how much each one buys.

1. **`--max-worker-restart=0`** — the single highest-value setting. A crashed worker ends the
   session with `worker gwN crashed and worker restarting disabled` instead of being silently
   replaced up to `4N` times. It converts quiet proliferation into a loud, bounded failure, which is
   the only honest posture for a *gate*: a gate that quietly restarts workers is a gate that reports
   a verdict it did not earn.
2. **Do not run the full suite inside a commit hook at all.** [#528] leg 2 already names the right
   shape — targeted suite in-lane, one full suite at integration. xdist inside a pre-commit hook is
   the multiplication risk, not the cure. This is a doctrine point [#528] owns; nothing here
   displaces it.
3. **`--maxprocesses=N`** — caps `-n auto` so a high-core host does not pay N full suite imports
   inside a gate. Note `-n auto` means **physical** cores (falling back to 1 if undeterminable);
   `-n logical` needs `psutil`, which is not installed.
4. **`-n 0` for anything running inside a forking parent** — already ruled and measured in-repo
   (`pyproject.toml:83-91`, the mutmut interaction). Cited as the confirming precedent, not
   re-derived. The paired lesson there is equally load-bearing: **`-p no:xdist` is not a way to force
   serial**, because it unloads the plugin that supplies the `-n` that `addopts` already passes, and
   pytest exits 4 before collecting.
5. **`--dist loadfile` / `loadgroup` for the `live_repo` and `slow` tiers** — keeps tests that share
   the real tree on one worker. (`--dist worksteal`, the repo's current choice, is the right default
   for the *balanced* remainder: xdist 3.7.0 made its internal `steal` command atomic.)
6. **`-p no:cacheprovider` in hook context** — minor; avoids `.pytest_cache` writes landing while a
   commit is mid-staging.
7. **A detection leg, because no setting covers the killed-controller case.** §2.3's read-only
   PowerShell probe, reported at `SessionStart` or at the tail of `verify`, would have surfaced the
   19 strays at the moment they appeared rather than whenever they were noticed.
8. **Treat `pytest-timeout` + xdist on Windows as suspect** — issue #1094 is open and is precisely
   that interaction. Prefer bounding the whole run externally over per-test thread timeouts inside
   workers.

**Current version:** pytest-xdist **3.8.0** (2025-06-30, Python ≥3.9); locked here at **3.8.0** with
**execnet 2.1.2**, pytest **9.1.1**. The repo's `pytest-xdist>=3.8` floor is already at the current
upstream release — **no upgrade is available and none is needed**; the leak is a design property of
the `Popen` call, not a bug awaiting a fix.

**Windows/uv compatibility:** pure-Python wheel, nothing to compile, `uv sync --locked` reproduces it
on Windows unchanged. The only optional native piece is `psutil` (for `-n logical`), which is absent
and not recommended below.

### 2.7 Do-not-adopt, with the one-line reason

- **`-p no:xdist` to force serial** — measured in-repo: it removes the `-n` that `addopts` supplies,
  so pytest exits 4 before collecting a single test, and the run looks green while measuring nothing.
- **Raising `--max-worker-restart`** — treats the symptom by buying a larger budget for the exact
  proliferation being complained about.
- **`--dist each`** — runs every test in every worker; it is a multi-environment matrix mode, not a
  speed mode.
- **`-n logical` as the default** — buys hyperthread workers at the cost of adding `psutil` and more
  resident memory per worker; the repo's own precedent is to measure before adopting (`-n auto` was
  adopted on a measured 5.2×), so this should be measured, not assumed.
- **`pytest-parallel` / `pytest-forked`** — unmaintained and fork-based; `fork` does not exist on
  Windows, which is the platform in question.
- **A blanket `taskkill /F /IM python.exe` sweep** — would kill the operator's other Python processes
  including the live session's own interpreter; §2.3's command line makes precision free.
- **Waiting for an upstream fix to the orphan behaviour** — the `Popen` call has no process-group or
  Job-Object handling by design across both xdist and execnet; there is no pending fix to wait for.

---

## 3. A local pre-commit hook refusing commits on `main` ([#527])

### 3.1 What [#527] asks for, and the one word in it that decides the answer

The row asks for "a **pre-commit** local hook refusing a **non-merge** commit whose current branch is
`main`", armed via the existing `arm_hooks.py` / `check_hooks_armed` mechanism. **"Non-merge" is
load-bearing**, because this repo's own convention is `branch → --no-ff merge`, and that merge commit
is created *while HEAD is `main`*. So the first question is not which library to use — it is whether
a branch-name refusal would block the repo's own integration workflow.

### 3.2 The measured answer: clean merges are safe, conflicted merges are not

Run live, §4 E1–E5, with a faithful transcription of upstream's predicate:

| case | pre-commit hook fires? | outcome |
|---|---|---|
| **E1** ordinary commit on `main` | yes | **refused** (exit 1) — the witnessed incident, closed |
| **E2** ordinary commit on `feat/x` | yes | allowed |
| **E3** **clean `--no-ff` merge run while HEAD is `main`** | **NO — hook never fires** | merge lands, two-parent commit created |
| **E4** **conflicted merge finished by `git commit` on `main`** | **yes** | **refused** — `MERGE_HEAD` present |
| **E5** `git commit --amend` on `main` | yes | refused — `MERGE_HEAD` absent |
| **W1** commit in a worktree on `feat/z` while the primary is on `main` | yes | allowed — `HEAD` is per-worktree |

**E3 is the good news and E4 is the catch.** Git does not invoke the `pre-commit` hook for a clean
`git merge`, so `/ship`'s `--no-ff` merges pass untouched with no carve-out at all. But a *conflicted*
merge is completed with an explicit `git commit`, which does run the hook — and this repo conflicts
on integration routinely: `JOURNAL.md` records "every generated-file conflict resolved by
REGENERATION, never by hand — nine index collisions" in a single batch, plus recurring `JOURNAL.md`
prepend collisions and generated-index collisions at merge time.

So a stock branch-name refusal would force `git commit --no-verify` on essentially every batch
integration merge — and `--no-verify` is not surgical: it skips **the entire pre-commit stack**
(`ruff`, `audit-health`, `validate-backlog`, all four freshness gates). That trades a narrow gap for
a wide one, on the exact commits that most need gating.

**E4 also hands over the discriminator for free:** `MERGE_HEAD` is present exactly when the commit
being created is a merge, and `git rev-parse --git-path MERGE_HEAD` resolves it per-worktree. That is
[#527]'s "non-merge" predicate, in one line, worktree-correct by construction.

### 3.3 Recommended approach

**Adopt upstream `no-commit-to-branch`'s design — `git symbolic-ref HEAD` against a protected set —
as a `local` pre-commit hook carrying one added `MERGE_HEAD` carve-out.**

This is a deliberate one-rung step down the ladder (industry pattern over established dependency),
and the measured reason is §3.2: the stock hook has no merge awareness, and this repo's workflow puts
conflicted merge completions on `main` as routine events. The design is still not invented here —
upstream's implementation is the reference to copy, and it is 30 lines:

```python
# pre_commit_hooks/no_commit_to_branch.py (upstream, verbatim core)
def is_on_branch(protected, patterns=frozenset()):
    try:
        ref_name = cmd_output('git', 'symbolic-ref', 'HEAD')
    except CalledProcessError:
        return False
    chunks = ref_name.strip().split('/')
    branch_name = '/'.join(chunks[2:])
    return branch_name in protected or any(re.match(p, branch_name) for p in patterns)
```

Note the `except CalledProcessError: return False` — **detached HEAD is allowed**. That is
correct-by-construction here (a detached worktree is not on `main`), and is recorded as a stated hole
rather than a defect.

**If the operator prefers zero local code**, the stock hook is a legitimate choice with a known cost:
pin `pre-commit/pre-commit-hooks` at **`rev: v6.0.0`** with `args: ['--branch', 'main']`, and accept
`--no-verify` on conflicted merges. The repo already pins one external hook repo this way
(`astral-sh/ruff-pre-commit` @ `v0.15.5`), so the pattern is established. The recommendation above is
the one this lane would take, and §3.6 states the trade in one line.

**Current versions:** `pre-commit-hooks` **6.0.0** (2025-08-09, Python ≥3.9) · `pre-commit` **4.6.2**
(2026-08-10, Python ≥3.10); locked here at **4.6.1**, declared floor `pre-commit>=4.5`.

**Windows/uv compatibility:** a `local` hook with `language: system` and a `uv run --locked` entry is
exactly the shape all 20-odd existing hub hooks already use, so it inherits the repo's proven Windows
+ uv path with nothing new. (The stock-hook variant would use `language: python`, which makes
pre-commit build its own isolated environment outside `uv.lock` — a second, unpinned resolution path
on the operator's Windows host, and a further small reason to prefer local.)

### 3.4 Minimal integration sketch

```yaml
# .pre-commit-config.yaml — under the existing `repo: local` block.
# `default_stages: [pre-commit]` already applies; no stages: override needed.
      - id: block-commit-on-main
        name: Refuse a non-merge commit on main ([#527])
        entry: uv run --locked python scripts/block_commit_on_main.py
        language: system
        always_run: true
        pass_filenames: false
```

```python
# scripts/block_commit_on_main.py — exit 0 allow, 1 refuse, 2 internal error (fail CLOSED).
import subprocess, sys
from pathlib import Path

PROTECTED = {"main"}

def main() -> int:
    try:
        head = subprocess.run(["git", "symbolic-ref", "HEAD"],
                              capture_output=True, text=True)
        if head.returncode != 0:
            return 0                                    # detached HEAD — not on main
        branch = "/".join(head.stdout.strip().split("/")[2:])
        if branch not in PROTECTED:
            return 0
        # [#527] says NON-MERGE. MERGE_HEAD is present exactly for a merge commit,
        # and --git-path resolves it per-worktree. Verified live: E3/E4.
        merge_head = subprocess.run(["git", "rev-parse", "--git-path", "MERGE_HEAD"],
                                    capture_output=True, text=True).stdout.strip()
        if merge_head and Path(merge_head).exists():
            return 0                                    # finishing a conflicted merge — allowed
        print(f"REFUSED: direct commit on '{branch}'. Branch first, then --no-ff merge.\n"
              f"  (CLAUDE.md §4; the 2026-08-13 incident this closes: [#527])", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"block_commit_on_main: internal error — {exc!r}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
```

**Arming — no change needed, and one precondition to check first.** `.pre-commit-config.yaml` already
declares `default_install_hook_types: [pre-commit, commit-msg, pre-push]`, and `arm_hooks.py` installs
all three idempotently at `SessionStart`, asserted by `audit.py::check_hooks_armed`. A new
`pre-commit`-stage entry needs no arming work at all — it rides the existing mechanism, which is
exactly what [#527]'s Done-when asks for.

**The precondition:** `arm_hooks.py`'s own docstring records that pre-commit **refuses to install
when `core.hooksPath` is set** (`[ERROR] Cowardly refusing to install hooks with 'core.hooksPath'
set`, even when set to the default) and that "this checkout has it set". Verified in this container:
`core.hooksPath` is **not** set here (`git config --get core.hooksPath` → exit 1), which matches the
docstring's "a fresh clone does not". **On the operator's Windows checkout this is unverified by this
lane and should be checked before relying on the arming leg** — `git config --get core.hooksPath`.
`arm_hooks.py` already handles refusal by reporting and exiting 0, so the failure mode is a silently
un-armed gate rather than a loud one.

### 3.5 Interaction with git worktrees — the hooks-path question, answered

Probed live in this repo and in a throwaway repo (§4, worktree probe and W1):

- **`git rev-parse --git-path hooks` inside a worktree resolves to the *common* dir** —
  `/home/user/dev-knowledge/.git/hooks`, not the worktree's own
  `.git/worktrees/<name>/`. **Hooks are shared across all worktrees of a clone**, so a single
  `pre-commit install` in the primary arms every present *and future* worktree automatically. This is
  the answer to "hooks path resolution per worktree", and it is the same for a stock hook, a local
  hook, and a hand-rolled one.
- **`HEAD` is per-worktree, so the refusal is correctly scoped.** W1: with the primary on `main`, a
  commit in a worktree on `feat/z` is allowed. The hook refuses only in whichever worktree is
  actually sitting on `main`.
- **A fresh worktree checks out `.pre-commit-config.yaml` with the rest of the tree**, so the config
  the shared shim reads is present per-worktree with no seeding step. (`scripts/worktree_seed.py
  --plan` remains the authority on what a worktree *does* need seeded — untracked
  `ecosystem/*/state.yaml` and the env; hooks are not on that list and this finding is why.)
- **Detached-HEAD worktrees are allowed through** (`git symbolic-ref HEAD` fails → allow), which is
  correct here, and is the stated hole from §3.3.

### 3.6 Do-not-adopt, with the one-line reason

- **Stock `no-commit-to-branch` unmodified** — it has no merge awareness, so conflicted integration
  merges on `main` would each require `--no-verify`, which skips the *entire* gate stack, not just
  this one hook. *(Still the right pick if zero local code outweighs that; §3.3.)*
- **Hand-rolled `.git/hooks/pre-commit`** — un-versioned, undeployable to consumers, and it collides
  with the shim `pre-commit` already owns at that exact path; a `local` hook entry is the same code
  as a committed, shippable artifact.
- **`core.hooksPath` pointing at a committed hooks directory** — pre-commit refuses to install at all
  when it is set, so this trades the new gate for every existing one.
- **A `commit-msg`-stage hook** — fires later than necessary; `pre-commit` is the earliest refusal
  point and is what the row names.
- **Server-side branch protection** — that is [#153]'s scope (push-time/server-side), explicitly
  distinct per [#527]'s own kill-candidates line, and the repo's GitHub tier was already recorded as
  unable to host it.
- **Extending `block_ff_push.py` to cover this** — it is a *pre-push* organ; [#527] exists precisely
  because push-time is too late, after the commits exist and after recovery needs history rewriting.
- **`receive.denyCurrentBranch` / push-remote config tricks** — none of them refuse a *local commit*,
  which is the whole gap.
- **Re-implementing branch detection from scratch** — upstream's 30 lines are the reference; copy the
  predicate, add only the carve-out the measurement forced.

---

## 4. First-party evidence — verbatim

All run in this container, git **2.43.0**, against throwaway repositories under the session
scratchpad. Every probe repo and worktree was removed afterwards and removal verified.

### 4.1 Worktree path resolution (against this repo, read-only + one removed probe worktree)

```
$ git rev-parse --git-path hooks                    # primary
.git/hooks
--- inside a probe worktree ---
git-dir:              /home/user/dev-knowledge/.git/worktrees/wt-probe
git-common-dir:       /home/user/dev-knowledge/.git
--git-path hooks:     /home/user/dev-knowledge/.git/hooks      <-- COMMON dir: hooks are shared
--git-path index.lock: /home/user/dev-knowledge/.git/worktrees/wt-probe/index.lock  <-- per-worktree
branch --show-current: ''                                       (detached probe)
$ git worktree remove --force … && git worktree prune && git worktree list
/home/user/dev-knowledge  7bbb067 [claude/night2-research-d30vhu]      <-- removal verified
```

### 4.2 T1–T5 — git ref as a cross-machine lock (two clones of one bare remote)

```
===== T1: A claims lock (ref does not exist) =====
$ git push --force-with-lease=refs/locks/contract-x: origin HEAD:refs/locks/contract-x
 * [new reference]   HEAD -> refs/locks/contract-x
exit=0

===== T2: B claims SAME lock, B has NEVER fetched (the real racer) =====
 ! [rejected]        HEAD -> refs/locks/contract-x (stale info)
error: failed to push some refs to '…/remote.git'
exit=1

===== T3: plain push of a DIFFERENT commit onto the existing lock ref =====
 ! [rejected]        HEAD -> refs/locks/contract-x (non-fast-forward)
exit=1

===== T4: THE TRAP — plain push of the SAME commit onto the existing lock ref =====
Everything up-to-date
exit=0        <-- a racer at the same base commit reads this as "lock won"

===== T5: release + re-claim =====
$ git push origin :refs/locks/contract-x                  delete exit=0
$ git push --force-with-lease=refs/locks/contract-x: …    reclaim exit=0
```

### 4.3 T6–T10 — `update-ref` create-only, across worktrees of one clone

```
T6  create refs/locks/local-x   from primary        -> exit=0
T7  create refs/locks/local-x   from a WORKTREE     -> fatal: cannot lock ref 'refs/locks/local-x':
                                                       reference already exists     exit=128
T8  ref visible from the worktree                   -> yes (refs live in the common dir)
T9  create refs/worktree/locks/w from the worktree  -> exit=0, but the PRIMARY cannot see it
                                                       ("fatal: Needed a single revision")
T10 update-ref -d from the worktree                 -> exit=0 (release works from either side)
```

### 4.4 E1–E5 / W1 — does a merge invoke the `pre-commit` hook?

Hook = faithful transcription of upstream `no_commit_to_branch.py`'s predicate, plus a `MERGE_HEAD`
probe for diagnosis.

```
=== E1: ordinary commit ON main ===                       exit=1        (REFUSED)
=== E2: ordinary commit on feat/x ===
[hook] FIRED on branch 'feat/x'                           exit=0        (allowed)
=== E3: CLEAN --no-ff merge, run WHILE HEAD is main ===
merge exit=0
e2e1011 b62fff4 3819676 Merge branch 'feat/x'             <-- two parents, and NO [hook] line:
                                                              the pre-commit hook NEVER FIRED
=== E4: CONFLICTED merge finished with 'git commit' on main ===
CONFLICT (content): Merge conflict in f.txt
[hook] FIRED on branch 'main'; MERGE_HEAD=present
[hook] REFUSE                                             exit=1        (REFUSED)
  … same commit with --no-verify                          exit=0        (succeeded)
  bb5cef4 parents=[bfdc85a 8adc78c] Merge branch 'feat/y'
=== E5: git commit --amend on main ===
[hook] FIRED on branch 'main'; MERGE_HEAD=absent
[hook] REFUSE                                             amend exit=1  (REFUSED)
=== W1: primary on main, commit inside a worktree on feat/z ===
worktree commit exit=0                                    (allowed — HEAD is per-worktree)
hooks dir seen from worktree: …/R/.git/hooks              (shared — one install arms all)
```

### 4.5 Locked versions in this repo (read from `uv.lock`, not assumed)

```
execnet        2.1.2          pytest         9.1.1        python pin     3.12.10
pytest-xdist   3.8.0          pre-commit     4.6.1
filelock       3.32.0  (already present, transitively)
portalocker    -- ABSENT --   pytest-cov  -- ABSENT --   coverage -- ABSENT --   psutil -- ABSENT --
```

### 4.6 Gate state for this lane's own commit

Recorded because it is not clean, and a lane that reports "gates passed" without saying which ones
could not run is reporting something it did not check.

**Ran and passed** (docs-only diff): `validate_hermetization.py` on the new path — exit 0, the
filename satisfies ADR-101 R3/R4 (`<date>-technical-<slug>`, lowercase kebab) and `docs/audits/` is
an allowlisted home · `gen_audit_index.py --write` then `--check` — exit 0, index regenerated
504 → 505 · `normalize_headers.py` on the new file — exit 0, rewrote nothing.

**Could not run in this container, and why:** every hook entry invokes `uv run --locked`, and the
container ships **uv 0.8.17** against the repo's exact pin `==0.11.19` (`pyproject.toml`), which
`uv self update 0.11.19` cannot reach here. Git hooks are also **not armed** in this clone. Gates
were therefore run through a scratch venv instead of through pre-commit, and **this commit lands
un-gated by the hook stack** — the full set fires on the operator's host at integration.

**`audit.py health` → `DEGRADED`, exit 1 — pre-existing, ZERO net-new.** Measured rather than
asserted: the FAIL set was captured with the change applied and again at bare HEAD with the change
stashed, and the two are **byte-identical** (4 FAILs both sides). All four are container artifacts,
not repo state introduced here: `repos registered (none)` (untracked `ecosystem/*/state.yaml` not
seeded), `hooks_armed` (unarmed clone), `journal_spine_anchor` (**shallow clone** — 318 commits, and
the disposition floor `24882f8cc` is simply not in this container's history), plus a
`canonical_freshness` 6-stale FAIL that is live repo state predating this lane. Nothing in this
lane's diff touches any of them.

> **AMENDMENT 2026-08-14 (same lane, post-commit — appended per CLAUDE.md §5 rule 3; the text
> above is left exactly as written).** Two corrections to the paragraph above, both found after
> `757077f` landed, when the container's uv was brought to the pinned `0.11.19` and the real
> toolchain became runnable.
>
> **A1 — the `canonical_freshness` characterisation above is WRONG.** It calls that FAIL "live
> repo state predating this lane". It is a **shallow-clone artifact**, the same class as the other
> three. Evidence: all six flagged files attribute their "last edit" to one merge, `4bef950`
> (2026-08-09); `git log --oneline -- VISION.md` returns **that merge and nothing else**; and
> `4bef950^1` is `fatal: bad revision` — the merge's parents are outside this clone's 318-commit
> graft (boundary `01410f9`). With parents truncated git cannot simplify history, so it attributes
> the file to the merge and the check reads a date no content edit produced. **Honest limit: this
> establishes that the container cannot answer the question, NOT that the six stamps are fine** —
> the real last-edit dates need a full clone. Do not read this amendment as a clean bill for those
> six files; read it as "the number measured here is not evidence either way".
>
> **A2 — the hook stack was subsequently RUN, and the applicable gates PASS.**
> `pre-commit run --from-ref HEAD~1 --to-ref HEAD` against this lane's own commit:
> **Passed (3)** — `normalize-dated-headers`, `audit-index-freshness`, `validate-hermetization`,
> i.e. every hook that actually inspects this diff · **Skipped (10)** — file-scoped to surfaces
> this diff does not touch · **Failed (1)** — `audit-health`, on the four pre-existing FAILs above
> and nothing else. The paragraph's load-bearing claim is unaffected and re-confirmed with the real
> toolchain: **ZERO net-new, the FAIL set byte-identical to bare HEAD.**

---

## 5. Residuals — what this lane did not establish

1. **The §1 lock is unverified against GitHub specifically.** One command closes it, and it is left
   for the operator because it writes to the shared remote:
   `git push --force-with-lease=refs/locks/probe: origin HEAD:refs/locks/probe` (expect exit 0), then
   the same command from a second clone (expect exit 1, `stale info`), then
   `git push origin :refs/locks/probe`.
2. **No §2 claim was reproduced on Windows.** The mechanism is established from upstream source and
   an upstream Windows report; the *count* of 19 was not reproduced and its exact `-n` value is not
   known to this lane. The §2.3 read-only probe is the cheapest way to convert the mechanism into a
   local measurement.
3. **Session-scoped-fixture exposure in this suite was not surveyed** (§2.4). It is a grep, not a
   judgement, and it belongs to whoever executes [#528].
4. **`core.hooksPath` on the operator's Windows checkout is unverified** (§3.4). If it is set,
   [#527]'s "armed via the existing `arm_hooks.py`/`check_hooks_armed` mechanism" clause has a
   precondition that must be resolved first — and `arm_hooks.py` fails soft, so the symptom would be
   a silently un-armed gate.
5. **Nothing here is ruled.** Each of the three answers is a recommendation with its trade stated;
   none was adopted, no config was edited, and no BACKLOG row was born or closed.

---

## Sources

Upstream source read directly (`raw.githubusercontent.com`): `pytest-dev/execnet`
`src/execnet/gateway_io.py`, `src/execnet/multi.py`; `pytest-dev/pytest-xdist`
`src/xdist/plugin.py`, `src/xdist/dsession.py`, `src/xdist/workermanage.py`, `CHANGELOG.rst`,
`docs/how-to.rst`; `pre-commit/pre-commit-hooks` `pre_commit_hooks/no_commit_to_branch.py`,
`.pre-commit-hooks.yaml`; `tox-dev/filelock` `docs/index.rst`.

- [filelock · PyPI](https://pypi.org/project/filelock/)
- [portalocker · PyPI](https://pypi.org/project/portalocker/)
- [pytest-xdist · PyPI](https://pypi.org/project/pytest-xdist/)
- [pre-commit · PyPI](https://pypi.org/project/pre-commit/)
- [pre-commit-hooks · PyPI](https://pypi.org/project/pre-commit-hooks/)
- [pytest-xdist issue #1094 — stuck replacing workers (Windows)](https://github.com/pytest-dev/pytest-xdist/issues/1094)
- [pytest-xdist issue #70 — workers crash on win64, "Not properly terminated"](https://github.com/pytest-dev/pytest-xdist/issues/70)
- [pre-commit issue #1198 — core.hooksPath causes "Cowardly refusing to install"](https://github.com/pre-commit/pre-commit/issues/1198)
- [pre-commit issue #3630 — clarify the core.hooksPath clash and workarounds](https://github.com/pre-commit/pre-commit/issues/3630)
- [pytest — how to use temporary directories and files](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
- [pytest-cov · PyPI](https://pypi.org/project/pytest-cov/)
- [pre-commit/pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
- [tox-dev/filelock](https://github.com/tox-dev/filelock)

In-repo locators cited above: `protocols/STANDING_RULINGS.md:973` (I-D3) · `scripts/fleet_health.py:730`
(`O_EXCL` precedent) · `pyproject.toml:79-91` (mutmut/xdist interaction), `:100-103` (markers),
`:140` (`addopts = "-n auto"`) · `.pre-commit-config.yaml:8,17` · `scripts/arm_hooks.py` docstring ·
`CLAUDE.md` §4, §9 · `BACKLOG.md` [#527], [#528] · `JOURNAL.md` 2026-08-14 (d), 2026-08-11 (j).
