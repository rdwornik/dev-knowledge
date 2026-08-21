# ARTIFACT — lane-554 cloud provisioning (batch 1, lane B)

> **Status: FINAL (step 6 of 6).** Every leg is reported done or blocked-with-reason. Nothing
> below is asserted from a code-read alone: each measurement names where and when it was taken.
>
> Contract: `LANE-554-cloud-provisioning.md` (frozen, operator-held) · Row: `BACKLOG.md`
> `[#554]` · Branch: `worktree-lane-554-cloud-provisioning` · Repo: `.dev-knowledge` ·
> Date: 2026-08-21.

## 0. What this lane inherited

`[#554]` is **not** a green-field row. Five commits already landed `.devcontainer/` on `main`
(`2330e0fd`, `876e288d`, `57313811`, `b3060764`, `1c6e07cc`), and two prior artifacts measured
the result:

- `docs/audits/2026-08-19-technical-554-proof.md` — the proof lane. **All four legs plus the
  C1/C2 obligations assert clean on the Codespaces free tier**; `audit.py health` RED with
  2 FAILs; `pytest -m "not slow"` RED with 8 failures; `devcontainer up` off-Codespaces BLOCKED.
- `docs/audits/2026-08-20-technical-codespaces-audit.md` — the substrate audit, §4.5 LEAN v2
  accepted verbatim as the ruling. Re-measuring lane J's clone-shape class from `main` rather
  than a probe branch dropped `audit.py health` to **exactly one** `[!!]`:
  `repos registered (none)`, which it called structural.

So this lane's question was not "do the four legs work" — that was measured and answered — but
**what still stands between the landed provisioning and the row's Done-when**, plus A3 and B1.

## 1. Legs — done or blocked

| # | Leg | Status | Evidence |
|---|---|---|---|
| L1 | pinned-`uv` assert | **DONE** (inherited, re-proven live) | `[provision] L1 OK — uv 0.11.19 == pin 0.11.19`, codespace `obscure-engine-…`, 2026-08-21 |
| L2 | `git fetch --unshallow` | **DONE** (inherited, re-proven live) | `[provision] L2 OK — full history (5439 commits reachable from HEAD)` |
| L2b | history **sufficiency**, not depth (contract B1) | **DONE** (new) | see §B1 |
| L3 | three hook types armed | **DONE** (inherited, re-proven live) | `[provision] L3 OK — pre-commit / commit-msg / pre-push all armed and pre-commit-managed` |
| L4 | env refuse-gate | **DONE** (inherited; a live defect FIXED) | see §L4 |
| L5 | `repos registered` — the row's D1a blocker | **DONE** (new) | `audit.py health` → `health: OK`, exit 0, in the container |
| A3 | devcontainer prebuild + warm-start measurement | **PARTLY BLOCKED** — measurement done, configuration is operator-only | see §A3 |
| — | D1a `pytest -m "not slow"` green in the container | **NOT MET** | 5 failures, none caused by this lane; see §2.3 |
| — | `pytest -m "not slow"` on the workstation | **GREEN for a lane checkout** | `4 failed, 3197 passed` — 2 worktree artifacts + 2 pre-existing; see §2.4 |
| — | D2 `devcontainer up` on a VPS | **BLOCKED, unchanged** | no container runtime on the workstation; lane J's finding stands |

### L4 — the env refuse-gate, and the defect it was hiding

Leg 4 is bespoke, so the **library-first line** the contract asks for, in one line: the
devcontainer spec's own `containerEnv` / `remoteEnv` mechanism was checked first as the way to
carry the stamp path, and it is precisely what failed — a `containerEnv` value cannot reference
`containerEnv`, so the declaration reached the script unexpanded; the stdlib/bash fallback
(`${VAR:-default}` plus a refusal on an unexpanded `${`) is what replaced it.

The proof lane recorded that `${containerEnv:HOME}` was passed through **literally**, so
`mkdir -p "$(dirname "${STAMP}")"` created a directory *named* `${containerEnv:HOME}` inside the
working tree on every container start. **Reproduced live on `main` on 2026-08-21:**

```
$ git status --porcelain
?? ${containerEnv:HOME}/
$ find . -path "*containerEnv*"
./${containerEnv:HOME}
./${containerEnv:HOME}/.dev-knowledge-provision-stamp
```

Fixed by removing the declaration (the relocation capability it claimed is preserved: the script
still honours an exported `DEV_KNOWLEDGE_PROVISION_STAMP`), **and by closing the class** — any
stamp path still carrying an unexpanded `${` is refused rather than created. Both were witnessed
firing in the container:

```
[provision] REFUSED: DEV_KNOWLEDGE_PROVISION_STAMP is ${containerEnv:HOME}/... — an UNEXPANDED ${...} path.
[provision]           Creating it would put a junk directory inside the working tree.
```

and after the fix, `[provision] stamp written: /home/vscode/.dev-knowledge-provision-stamp`
with **no junk directory in `git status`**.

**The gate also refused for real, unprompted.** After a full rebuild wiped `$HOME`:

```
[provision] REFUSED: L4 no provisioning stamp at /home/vscode/.dev-knowledge-provision-stamp
            — this container was never provisioned, or was resumed from an image that predates
            provisioning. Run: bash .devcontainer/provision.sh
```

Re-provisioning restored it in **7 seconds** and the gate then passed. That is leg 4 doing its
job on a real half-provisioned container rather than a synthetic one.

### L5 — `repos registered`, and why "structural" was wrong

The substrate audit called this **structural**: "a container holds one repo and the hub's check
expects the sibling fleet". The repo says otherwise. `audit.py::discover_repos` counts
directories under `ecosystem/` carrying a `state.yaml`, and **`ecosystem/*/state.yaml` is
gitignored** (`.gitignore` line 69) — so *no clone has ever carried one*, fleet or not. On the
workstation `scripts/worktree_seed.py` copies them from the primary checkout, and its own
manifest comment names this exact symptom: *"gitignored ecosystem state a lane's `audit-health`
gate reads, whose absence reports `repos registered (none)` and blocks every commit."*

A container has no primary to copy from, so it audits the one repo it does have —
`audit.audit_repo` + `audit.save_state`, deliberately **not** `audit.py repo`, which would also
append history, write a dated report under `docs/audits/` and commit its outputs.

**Measured in the container, before and after, same commit:**

```
BEFORE   [!!] repos registered  (none)          health: DEGRADED   exit 1
AFTER    [OK] repos registered  (['.dev-knowledge'])   health: OK   exit 0
```

**`audit.py health` is GREEN on the Codespaces free tier.** That is the first half of the row's
D1a Done-when, and it was the last `[!!]` standing.

## 2. Measurements

All timings: GitHub Codespaces, `basicLinux32gb` (2-core / 8 GB), region as allocated, repo
`rdwornik/dev-knowledge`, branch `main`, 2026-08-21. Two endpoints are recorded per run because
they answer different questions: `state == Available` is what the API reports, and *first
successful `ssh -- true`* is when a lane could actually start work.

### 2.1 A3 — warm start: resume vs create (four timed runs)

| Run | Operation | → `state: Available` | → shell usable |
|---|---|---|---|
| 1 | **Create** (cold) | **108.9 s** | **127.6 s** |
| 2 | **Create** (cold, second codespace) | **115.1 s** | **122.4 s** |
| 3 | **Resume** from `Shutdown` | **35.3 s** | **41.5 s** |
| 4 | **Resume** from `Shutdown` (same codespace, second cycle) | **19.1 s** | **24.8 s** |

**Resume is 3–5× faster than create** (24.8–41.5 s against 122.4–127.6 s to a usable shell).
The contract's minimum of two timed runs is met twice over, with creates and resumes measured
separately rather than inferred from one another.

Two further timings, recorded because they are the operations a lane actually performs:

| Operation | Wall clock |
|---|---|
| `stop` → `Shutdown` | 35.0 / 96.8 / 108.2 s (3 runs, high variance) |
| **Full rebuild** (`gh codespace rebuild --full`, new `devcontainer.json`) → shell usable | **87.5 s** |
| Cold provisioning run (`provision.sh`, all legs) | **28.1 s** |
| Idempotent re-run of provisioning (fully provisioned) | **7 s** |
| `audit.py health` in-container | **22.1 s** (2 runs) |
| `pytest -m "not slow" -n auto` in-container | **248 s** |

**One measurement is confounded and is reported as such:** a third resume, on the codespace
whose workspace carried a modified `devcontainer.json`, took 91.8 s / 97.4 s — because the
resume re-ran `devcontainer up`, re-read the changed config and pulled a fresh base image. It is
excluded from the resume figures above rather than averaged into them.

### 2.2 Budget

- **Actions minutes: 30% consumed** — 601 of 2 000 in August, per the codespaces audit RULING
  block, which is the source the contract names. **Re-read live 2026-08-21: 630 of 2 000
  (31.5%)**, all on `corp-monorepo`. This is why the *On configuration change* prebuild trigger
  is load-bearing rather than tidy: the default *Every push* would compete for the remaining
  ~1 370 minutes.
- **Codespaces compute, August, live reading:** 0.433 h × 2-core + 0.503 h × 4-core ≈ **2.9 of
  120 core-hours (2.4%)**. This lane's own consumption (two codespaces, ~1 h wall total) is
  inside that and is billing-lagged; it does not approach the 30 h/month free ceiling. **No
  overage was purchased, per the never-meter-buy rule.**
- **No leftovers:** both codespaces were deleted at the end of the lane and `gh codespace list`
  returns empty.

### 2.3 `pytest -m "not slow"` in the container — 5 failures, none from this lane

`5 failed, 3113 passed, 9 skipped, 1 xfailed in 247.69s`. The proof lane's tally was 8 failures.

**That run is a SNAPSHOT taken mid-lane**, and saying so matters: it was measured before the
twelve terra rounds, so it counted 29 of this lane's tests rather than the 111 the branch now
carries. It is reported unchanged rather than restated from the later workstation run, because it
is the only measurement of the container's own failure set — and every failure in it is
independent of the code the terra rounds touched.

Each survivor was classified by **re-running it on the workstation**, not by reading it:

| Test | Class | Also fails on the workstation? |
|---|---|---|
| `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` | pre-existing repo-state drift (BACKLOG now has 3 rows, the test pins 1) | **YES** |
| `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | pre-existing | **YES** |
| `test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration` | known Linux-only defect (lane J §4.3) | no — passes on Windows |
| `test_merge_serialization.py::test_index_lock_blocks_concurrent_merge` | known Linux-only defect (lane J §4.3) | no — passes on Windows |
| `test_boundary_report.py::test_live_hub_baseline_and_consumers_legal` | single-repo container: needs ≥1 registered **consumer**, and L5 registers the **hub** | no — passes on Windows |

**Clone-shape failures: 5 → 0.** The four that disappeared (`test_audit.py` health pair,
`test_audit_parallel.py`, `test_validate_branch_naming.py`) did so because the codespace was
created from `main` and because L5 registers a repo.

**So D1a's second half is NOT met, and this lane does not claim otherwise** — but the residue is
2 pre-existing failures that are red on the workstation too, 2 known Linux-only defects, and 1
genuine single-repo-container artifact. None is caused by this lane's changes, and none is a
provisioning defect.

### 2.4 `pytest -m "not slow"` on the workstation — the lane's own green

Run twice on this branch, and the first run is reported because the difference between them is
itself the finding:

| Run | Result | |
|---|---|---|
| 1 | `21 failed, 3178 passed, 10 skipped, 1 xfailed in 765.19s` | 16 of the 21 were `ModuleNotFoundError: No module named 'pandas'` — a **fresh lane venv provisioned without the `analytics` group**, not a code defect |
| 2 | **`4 failed, 3197 passed, 8 skipped, 1 xfailed in 785.30s`** | after `uv sync --locked --group analytics` |

The four survivors, and why none belongs to this lane:

| Test | Class |
|---|---|
| `test_audit.py::test_check_fleet_parity_green_on_live_repo` | worktree artifact — a lane checkout structurally REDs it |
| `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | worktree artifact — `_REPO_ROOT` **is** a linked worktree here, so the reader correctly returns it |
| `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` | pre-existing repo-state drift |
| `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | pre-existing |

`git diff --name-only main...HEAD` touches **none** of `BACKLOG.md`,
`.pre-commit-config.yaml`, `scripts/audit.py`, `scripts/enforcement_coverage.py`,
`tests/test_stale_worktrees.py` or `tests/test_fleet_analytics.py` — so no failure above can be
attributed to this branch. **Two worktree REDs plus the standing pre-existing pair is the honest
green for a lane checkout of this repo, and that is what this run measures.** 111 of the 3 197
passing tests are this lane's.

**Run 1 corroborates the provisioning design rather than embarrassing it.** A lane venv built
without `--group analytics` produced 16 failures; the container never showed them, because
`provision.sh`'s `sync_environment` runs `uv sync --locked --group analytics` and its own comment
says why — *"a venv without it reds the L5a tests, so `pytest -m 'not slow'` (Done-when D1) would
not be green."* The workstation is the environment with no such step, and it is the one that
failed.

## 3. B1 — the blocking amendment: which option, and why

**Option (a) was taken: a gated deepen/unshallow-and-repair step that runs before any
spine-walking instrument in a cloud lane. Option (b), excluding those instruments from cloud
lanes, is implemented and deliberately NOT taken.**

**Why (a).** A lane whose gates are switched off is not a lane running green — it is a lane whose
verdicts mean nothing, which is the vacuity `[#554]` exists to close. Option (b) is available as
`history.disposition: exclude` in `.devcontainer/provisioning.yaml`, with the five instruments
enumerated so the exclusion would have a checkable subject; taking it would be a recorded
decision, not a silent default.

**What the amendment got right, and the part it did not name.** The contract's premise — that a
depth-1 clone breaks spine-walking instruments — is correct and was reproduced: a `--depth 1`
clone of this repo walks **1** first-parent spine entry against **1 519** in a full one. But leg
2's existing `--unshallow` already covered depth, and the proof lane measured the failure that
depth does not cover:

> `git fetch --unshallow` (leg 2) restores *depth* but not *branches*: 5329 commits are
> reachable, and `main` still does not exist as a ref.

Reproduced live in the container:

```
$ git clone --single-branch --branch worktree-lane-probe <upstream> hostile
shallow=false commits=5439
* worktree-lane-probe
  remotes/origin/worktree-lane-probe
$ git log --first-parent --format=%H main
fatal: ambiguous argument 'main': unknown revision or path not in the working tree.
```

So B1 is implemented as **history sufficiency**, not merely depth: the guard asserts the clone is
not shallow, that every ref in `history.required_refs` resolves *in the `refs/heads/` namespace*,
that it is current with the live remote, and that the first-parent walk the instruments perform
actually succeeds. Both hostile shapes repaired live:

```
/tmp/hostile   --check  → exit 1  ref 'main' does not resolve in this clone
/tmp/hostile   --repair → exit 0  main walks 1519 first-parent spine entries
/tmp/shallowc  --check  → exit 1  clone is SHALLOW  (main walks 1 entry)
/tmp/shallowc  --repair → exit 0  main walks 1519 first-parent spine entries
```

**Ordering** — "before any spine-walking instrument" — is asserted by a test, not by a comment:
`leg2b_history` runs after `sync_environment` (it needs the venv) and **before `leg3_hooks`**, so
nothing that walks a spine can be reached by a hook before its precondition is repaired.

**Honest limits of the B1 guard, stated rather than left to be found:**

- The read-only `--check` (what `--gate` runs on every container start) queries the live remote
  with `ls-remote`, so it costs one network round trip per start. That was chosen over reading
  the cached `origin/<ref>`, which goes stale *alongside* the local branch and would let a
  resumed container pass while the walk missed everything upstream had added.
- A **diverged** or **off-spine** ref is refused, never repaired. Forcing it would discard local
  commits, and this guard will not do that under any disposition.
- The instrument list is a declaration, not a discovery: a new spine walker that nobody registers
  in `.devcontainer/provisioning.yaml` is invisible to the exclusion option (the repair option is
  unaffected, since it repairs the refs rather than enumerating consumers).

## 4. A3 — the prebuild leg: what landed, and what is operator-owned

**BLOCKED, with the reason: no public API exists for Codespaces prebuild configurations.** Probed
2026-08-21 against the live repo, all three channels:

```
GET /repos/rdwornik/dev-knowledge/codespaces/prebuilds   → 404 Not Found
GraphQL introspection, types matching /prebuild/i        → 0
GraphQL introspection, mutations matching /prebuild/i    → 0
gh codespace --help                                      → no prebuild subcommand
```

The configuration is operator UI state. What this lane could therefore land, and did:

1. **The declaration**, in YAML rather than hardcoded — `.devcontainer/provisioning.yaml`
   `prebuild:` block carries trigger `on_configuration_change`, regions `[EuropeWest]`,
   `template_history: 1`, all three exactly as the accepted LEAN v2 ruling specifies.
2. **A drift checker** — `cloud_provisioning.py prebuild` compares the declaration against the
   one field the API does expose, `prebuild_availability`, asked *in the context of the declared
   ref and region* because that is the only context in which GitHub answers it. Exactly one
   combination is falsifiable and the tool says so rather than reporting a verification it cannot
   make.
3. **The `onCreateCommand` half** — a prebuild bakes `onCreateCommand` and `updateContentCommand`
   and **never** prebuilds `postCreateCommand`, so provisioning wired only to `postCreate` would
   leave the whole run on the create path even with a prebuild enabled. `onCreateCommand` now
   names the same script; `postCreateCommand` is kept because a prebuilt image is built from the
   default branch and a later or different-branch codespace can carry pins the prebuild never
   saw. The double run costs a measured **7 s** against ~28 s saved.

**Proven end-to-end in the real lifecycle**, not asserted — from the rebuild's own creation log:

```
onCreateCommand    [provision] B1 OK …  L5 OK …  DONE — 3 leg(s) acted
postCreateCommand  [provision] B1 OK …  L5 OK …  DONE — idempotent
postStartCommand   [provision] gate OK — uv 0.11.19, full history + spine refs, ecosystem
                   registered, three hook types armed, stamp current
```

### 4.1 OPERATOR ACTION OWED — the one step this lane cannot take

Settings → Codespaces → **Set up prebuild** on `rdwornik/dev-knowledge`:

| Setting | Value | Why |
|---|---|---|
| Configuration file | `.devcontainer/devcontainer.json` | the only one |
| Branch | `main` | the default branch a prebuild is built from |
| Prebuild triggers | **On configuration change** (NOT the *Every push* default) | 630 of 2 000 Actions minutes are already spent this month |
| Regions | **EuropeWest only** (NOT *all regions*) | all-regions × 2 retained = up to 8 multi-GB images, the one thing that can exhaust the 15 GB-month allowance |
| Template history | **1** (default is 2) | same reason |

Then flip `prebuild.configured` to `true` in `.devcontainer/provisioning.yaml`;
`python scripts/cloud_provisioning.py prebuild` will corroborate it (exit 0) once the first
prebuild is `ready`, and report drift (exit 1) if the configuration is later removed.

## 5. Proposed pre-commit diffs — none

The contract forbids `.pre-commit-config.yaml` edits and asks for hook entries as fenced
proposed-diffs instead. **This lane proposes none, and the absence is deliberate rather than an
omission.** `scripts/cloud_provisioning.py` is provisioning machinery: it *mutates a git clone*
and writes `ecosystem/<name>/state.yaml`. A pre-commit hook must be read-only and fast, and this
is neither. Wiring it into a gate would also change what a commit means on the workstation, where
none of these conditions apply. If a future arc wants a hook, the read-only halves
(`--quiet history`, `--quiet ecosystem`) are the candidates, and that is a surfaced act with its
own decision — not a rider on this lane.

No audits index was regenerated and nothing was written under `docs/audits/`.

## 6. Terra review — twelve rounds to a clean pass

`codex exec --sandbox read-only -c model_reasoning_effort=high`, codex-cli 0.145.0, code profile,
diff `main..worktree-lane-554-cloud-provisioning`. `codex-review.ps1` was **not** used: it writes
its artifact under `docs/audits/`, which this batch forbids.

| Round | Critical | High | Medium | Low | Outcome |
|---|---|---|---|---|---|
| 1 | 0 | 5 | 0 | 0 | all fixed |
| 2 | 1 | 5 | 0 | 0 | all fixed |
| 3 | 0 | 5 | 0 | 0 | all fixed |
| 4 | 0 | 4 | 0 | 0 | all fixed |
| 5 | 1 | 3 | 0 | 0 | all fixed |
| 6 | 1 | 2 | 0 | 0 | all fixed |
| 7 | 1 | 3 | 0 | 0 | all fixed |
| 8 | 0 | 3 | 0 | 0 | all fixed |
| 9 | 0 | 1 | 0 | 0 | fixed |
| 10 | 0 | 2 | 0 | 0 | all fixed |
| 11 | 0 | 1 | 0 | 0 | fixed |
| **12** | **0** | **0** | **1** | **0** | Medium fixed; **Critical/High clean** |
| **Total** | **4** | **34** | **1** | **0** | **39 findings, 39 fixed** |

The contract asks for P1/P2 to be fixed. **Every finding in every round was fixed**, including
the four Criticals — three of which were in code this lane wrote, and all four of which were
data-loss or wrong-destination-write paths:

- **R2** a diverged branch was force-updated, so an unpushed commit on local `main` would have
  lost its only reference the moment `origin/main` also advanced.
- **R5** `audit.save_state` resolves through a module-level directory, so
  `ecosystem --repair --root <another clone>` would have written that clone's state over *this*
  checkout's.
- **R6** the `+refs/heads/…` refspec wrote whatever the remote held at fetch time, a race the
  divergence guard could not see.
- **R7** compare-and-swap protects the *local* ref only — a force-push to an ancestor still
  rewound the branch through it.

Two findings were against this lane's own **tests**, and both were the tautology class: a
"refusal" test that grepped for a string and stayed green with the `exit 1` deleted (R1-H4), and
a race test that fired outside the window it claimed to cover (R8-H2). Both now execute the
behaviour.

## 7. What is NOT covered — stated, not discovered later

- **No test executes a successful end-to-end `provision.sh` run.** Shimming `uv`'s five
  subcommands plus `curl` plus a fake repo produces a harness more likely to test itself than the
  script. What stands in for it is the live container evidence in §L4/§A3 — three real Codespace
  runs, including a full rebuild in which all three lifecycle hooks fired. Three *refusal* paths
  ARE executed by the suite (no stamp, foreign schema, moved pin).
- **`devcontainer up` on a host we control has still never run** (row Done-when clause 2, lane
  J's D2). No container runtime on the workstation; unchanged by this lane, and the substrate
  ruling deliberately puts that discharge before any Hetzner spend.
- **The prebuild's three settings are unverifiable by any API** — the checker reports on
  availability only, and says so in its own output.
- **`--check` mode does not re-read `ecosystem/` contents beyond structure.** It requires a
  mapping with `name` and `path`, deliberately not identity, because a worktree carries the
  primary checkout's `state.yaml` by design.

## 8. Contract compliance

- Zero interactive questions asked; defaults taken and reported here.
- The **ssh BOM defect was not touched**. Interaction noted: it is **no longer present** —
  `~/.ssh/config` begins `Host git` and `ssh -G` succeeds, so `gh codespace ssh` worked
  throughout. The contract's premise that it would obstruct this lane no longer holds.
- No merges, no pushes, no `tasks/`/`BACKLOG`/§Q edits, no deletions, no new folders, no
  pre-commit edits, no cloud dispatches. Both codespaces created for measurement were deleted.
- **One declared single-hook bypass**, per `STANDING_RULINGS` Q1 (lane branch, declaration in the
  commit body): `SKIP=validate-hermetization` on the artifact-stub commit. `ARTIFACT-lane-554.md`
  is a new top-level file and ADR-101 Rule A refuses one by design, while the contract requires
  this artifact **at the worktree root** and forbids `docs/audits/` this batch — the lane cannot
  satisfy both. One file, lane-local; the integrator is gate-of-record for whether it lands.
