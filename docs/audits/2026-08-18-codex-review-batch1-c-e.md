# Codex Review — batch-1 pre-merge terra review of branches C + E

**Date:** 2026-08-18
**Branch:** `worktree-lane-c-554-devcontainer`
**HEAD:** `5506f59aeb534d4dc0eab4a1edb856df87d9b349`
**Diff range:** `main..worktree-lane-c-554-devcontainer` (merge-base `328d1086` == `main` tip, so `..` ≡ `...`)
**Codex version:** codex-cli 0.145.0
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Reviewer lane:** H (`worktree-lane-h-554-codex-review`), contract of record `docs/audits/2026-08-18-technical-review-lane-contract.md` @ `9a2f6f29`
**Tally:** 0/1/4/0 <!-- Critical/High/Medium/Low, BRANCH C ONLY (this is the branch the header links to). Mapping to the contract's bands: P1=Critical, P2=High, P3=Medium; Low is unused. Branch E's tally is in its own section and is 0/0/1/0. -->

> **This one file is the whole output of lane H, per its contract's ONE-artifact rule.** It carries
> both branch reviews. The machine-readable header above describes **branch C**, because
> `check_review_artifact_coverage` reads one `**Branch:**` / `**HEAD:**` / `**Tally:**` triple per
> file (`scripts/audit.py:3149-3150`, `.search`, first match wins). See §0.3 — branch E's merge will
> WARN on that leg, and that WARN is a consequence of the one-artifact rule, not a missing review.

---

# 0. How this review was done

## 0.1 Instrument path — the contract's PRIMARY path was used, not the fallback

The contract says: *"via `/codex-review` (terra); if the skill cannot target a branch diff directly,
fall back to `codex exec` with the diff as input — record which path was used."*

**Path used: the skill.** `~/.claude/bin/codex-review.ps1` accepts `-DiffRange` and honours it
without checking the branch out (`codex-review.ps1:7,49-50,98`), so the fallback was **not**
needed and was **not** used. Two runs, both from the lane-H worktree, both `-Force`, neither
`-AutoCommit`:

```
& codex-review.ps1 -Topic laneh-c-devcontainer -DiffRange "main..worktree-lane-c-554-devcontainer" -Force -Focus <C focus>
& codex-review.ps1 -Topic laneh-e-mutmut       -DiffRange "main..worktree-lane-e-502-mutmut"       -Force -Focus <E focus>
```

The focus hints passed to each run were the contract's own per-branch focus items, expanded into
refutable questions. Both runs used `gpt-5.6-terra`.

The skill writes its own artifact per run (`docs/audits/2026-08-18-codex-laneh-{c-devcontainer,e-mutmut}.md`).
Committing those would have produced three artifacts against a contract that specifies one, so
**every codex finding is reproduced verbatim below** and the two intermediates were deleted
uncommitted. Nothing the instrument said is lost; §1.1 and §2.1 quote them in full.

## 0.2 What the reviewer verified independently

Codex is the instrument, not the verdict. Every finding below was re-derived or refuted against
live state before being kept, and the positive checks in §1.3 / §2.3 were run by this reviewer,
not read off the branch's own claims. Where a finding could not be verified in this environment
that is stated as a limit rather than papered over.

## 0.3 An integrator consequence this review is obliged to surface

`check_review_artifact_coverage` (`scripts/audit.py:3159`) links a review artifact to a merge by
**one** branch name or **one** in-range HEAD, parsed by `.search` — first match only. This file
therefore discharges the leg for **branch C's merge only**.

- **Branch E's merge will WARN** (`review_artifact_coverage`) despite having been reviewed here.
- **This lane's own branch must be merged before or with C**, because the leg reads the artifact
  from the working tree; if lane H lands after C, C's merge WARNs too.

Both are surfaced, not dispositioned — the fix (name the artifact in the merge subject, split the
file, or accept the WARN) is the integrator's call and outside this lane's authority.

---

# 1. BRANCH C — `worktree-lane-c-554-devcontainer` @ `5506f59a`

5 commits, 8 files, +908/−2. Substrate: `.devcontainer/devcontainer.json` (72 lines) +
`.devcontainer/provision.sh` (340 lines); tree-seal lockstep in `scripts/validate_hermetization.py`,
`tests/test_validate_hermetization.py`, `docs/decisions/ADR-101-hermetization.md`,
`ecosystem/doc-counts.md`; and the lane's own contract-of-record audit file.

## 1.1 Findings

### C-1 · **P2** · `.devcontainer/devcontainer.json:52` — `waitFor` does not gate attachment on the re-assert path

**Codex reported this as HIGH. CONFIRMED, kept at P2.**

> **What:** `waitFor` waits for `postCreateCommand`, while the mandatory re-gate is in `postStartCommand`.
> **Why:** On container resume, a tool can attach before `--gate` completes or fails, defeating the claimed start-path refusal. The Dev Container spec waits only through the lifecycle command named by `waitFor`.
> **Fix direction:** Set `waitFor` to `postStartCommand` so both initial provisioning and every-start validation finish before connection.

**Independent verification.** Fetched the Dev Container reference and the published JSON schema:

- `waitFor` — *"An enum that specifies the command any tool should wait for before connecting."*
  Default `updateContentCommand`.
- Schema enum, verbatim: `["initializeCommand", "onCreateCommand", "updateContentCommand",
  "postCreateCommand", "postStartCommand"]` — so **`postStartCommand` is a legal value** and the
  proposed fix is a one-token change with nothing lost (on create, `postStartCommand` runs after
  `postCreateCommand`, so waiting for the later one still waits through the earlier).

**Why this is a defect and not a preference.** The branch makes the claim in two places, and both
are true on CREATE and false on every subsequent START:

- `devcontainer.json:49-51` — *"Do not report the container ready — or attach a session to it —
  until provisioning has actually finished."*
- `provision.sh:44-46` (HONEST LIMIT) — *"`\"waitFor\": \"postCreateCommand\"` is what stops a session
  attaching before provisioning has finished."*

On a **resume**, `postCreateCommand` does not re-run, so there is nothing for the tool to wait on
and it attaches immediately while `--gate` is still running. Resume is precisely the scenario
`postStartCommand`'s own comment names — *"A container resumed from a stale image, or one whose repo
has since moved its uv pin, is half-provisioned — and this refuses it"*. Leg 4 is the only leg that
fires on resume, and its attach-ordering guarantee is absent exactly there.

**Not P1:** the gate still executes and still fails loudly on resume; what is unguarded is the
ordering of attach against that failure, so the outcome is a lane that sees an error late rather
than a lane handed a silently vacuous environment.

### C-2 · **P3** · `.devcontainer/provision.sh:163` — `CHANGED` omits `sync_environment`, so "nothing changed" can print after real work

**Codex reported this as HIGH. CONFIRMED as a fact, DOWNGRADED to P3 — reasoning below.**

> **What:** `uv python install` and `uv sync --locked --group analytics` can install an interpreter or create/update `.venv`, but never increment `CHANGED`.
> **Why:** If other legs are already satisfied, the final line at 333 can state "nothing changed" after real environment work, violating the idempotency/status contract.
> **Fix direction:** Detect and count interpreter/environment changes, or avoid claiming "nothing changed" when these synchronization commands ran.

**Verified by reading.** `leg1_uv`, `leg2_unshallow` and `leg3_hooks` each increment `CHANGED`
(5 sites). `sync_environment()` (`provision.sh:163`) runs `uv python install` and
`uv sync --locked --group analytics` and touches `CHANGED` at no point, so `provision.sh:334` can
print `DONE — idempotent: nothing changed, all four legs were already satisfied (second run is a
no-op)` after building a venv from scratch — reachable on a FIRST run whose image already carries
the pinned uv, full history, armed hooks and the `.bashrc` marker.

**Why P3 and not P2.** The obligation the lane contract actually states is C1, *"a second run is a
no-op AND SAYS SO"*. On a genuine second run `uv sync --locked` **is** a no-op, so `CHANGED == 0` is
truthful and C1 is met. The false statement is reachable only on a first run against a pre-baked
toolchain, and its consequence is a misleading console line — no environment is left wrong. It is
listed rather than waived because a status line that overstates what was proven is the exact class
of failure this row exists to close.

### C-3 · **P3** · `.devcontainer/provision.sh:116` — remote installer executed without integrity verification

**Codex reported this as CRITICAL. Kept as a real finding, DOWNGRADED to P3 — reasoning below.**

> **What:** The pinned URL is fetched with `curl | sh` without a checksum or signature check.
> **Why:** A compromised installer endpoint/CDN can execute arbitrary code in the container with access to the workspace and user environment.
> **Fix direction:** Use a digest-pinned uv image/artifact or verify a repository-pinned checksum/signature before executing it.

**The trust edge is real and it is new**: `curl -LsSf "https://astral.sh/uv/${want}/install.sh" | …
sh` runs unreviewed remote code in a container that then arms this repo's git hooks and syncs its
dependency tree.

**Why not Critical.** The URL is **version-pinned** (`/uv/0.11.19/install.sh`, read from the
ADR-106 pin, never `latest`) and served over TLS; that is astral's documented install channel and
the same channel ADR-106's pin already presumes. No hash for it is published anywhere in this repo,
so there is nothing in-tree to check against — the gap is an absent supply-chain convention, not a
logic defect this branch introduced. No exploit path is demonstrated. Actionable alternatives if
the operator wants it closed: `pip install uv==0.11.19` with a `--require-hashes` pin, or a
digest-pinned devcontainer feature. **This is a standing decision for the operator, not a lane fix.**

### C-4 · **P3** · `.devcontainer/provision.sh:240-247` — the gate-liveness smoke proves the VALIDATOR is live, not that the HOOK dispatches

Codex reported nothing here. This is a reviewer finding against the contract's explicit
*"gate-liveness smoke honesty"* focus item.

**What the smoke genuinely proves — verified, and the branch's claim about it is TRUE.**
`provision.sh:245` runs `uv run --locked python scripts/validate_backlog.py`, byte-identical to
`.pre-commit-config.yaml:163`'s `validate-backlog` entry. And the no-args form is **not vacuous**:
`validate_backlog.py` takes no arguments at all and always reads the repo's `BACKLOG.md` from a
module-level constant (`scripts/validate_backlog.py:53`, `main()` at `:360`), returning 1 on any
hard-fail. The anti-pattern the repo warns about — *"running validators with no args → vacuous
pass"* — **does not apply to this validator**, and the file's claim *"this proves the same command
line the hook will run — not a lookalike"* is accurate.

**The honest narrowing.** It proves one validator executes under `uv run --locked`. It does not
prove `pre-commit` itself can build its hook environments and dispatch — a distinct member of the
same silently-vacuous-gate class the file's own header names. L3 asserts the shims are present and
not stale-bound; nothing asserts dispatch. `pre-commit run validate-backlog --all-files` would close
the residue in one line.

**Sub-note (cosmetic).** `provision.sh:247` prints `head -n 1` of the captured output. Because
`validate_backlog.py` prints every `WARN` line **before** its `OK` summary, that first line is a
WARN whenever warnings exist, so the displayed evidence is not the pass line. The assertion itself
is on the exit code and is correct.

### C-5 · **P3** · `.devcontainer/devcontainer.json:37` — `${containerEnv:HOME}` is unverified, and the fallback in `provision.sh` cannot rescue it

`containerEnv` sets `DEV_KNOWLEDGE_PROVISION_STAMP` to `${containerEnv:HOME}/.dev-knowledge-provision-stamp`.
If `HOME` is absent from the image environment at resolution time, the value becomes
`/.dev-knowledge-provision-stamp` — and because the variable is then **set**, `provision.sh:59`'s
`${DEV_KNOWLEDGE_PROVISION_STAMP:-${HOME}/…}` fallback does **not** engage. With `remoteUser: vscode`
the write in `write_stamp` would then fail.

**Mitigation, and why this is P3 not P2:** it fails **loud**. Under `set -euo pipefail` the failed
redirect aborts `postCreateCommand`, which surfaces as a failed create. It cannot produce a false
green. **Unverifiable here** — see §1.2; flagged as a first-boot watch item.

## 1.2 Verification coverage — what has and has not been executed

The lane discloses this itself (contract-of-record §3.1/§4), and this review confirms the
disclosure is accurate. It is recorded here because it is the reason C-1 and C-5 could not have
been caught by running the thing.

**Exercised on the workstation** (per the lane, spot-checked by this review): `bash -n`, the
`--help` path, the `read_uv_pin` awk against the real `pyproject.toml`, two `--gate` refusal cases
(no stamp; stamp recording `uv_pin=0.8.17`), `pytest tests/test_validate_hermetization.py -n 0`
→ 45 passed, `ruff check` clean.

**Never executed — no container runtime was available to that session:** `leg1_uv`'s install branch,
`leg2_unshallow`, `sync_environment`, `smoke_gate_liveness`, `write_stamp`, and the entire
`devcontainer.json` lifecycle. **The provisioning path has not run end-to-end anywhere.** That is
disclosed, not concealed, and it is a coverage fact rather than a defect.

The lane's L3 refusal on this workstation was independently checked and is **not** a script defect:
`arm_hooks._armed` counts a shim bound to a sibling worktree's venv as unarmed, which is a known
property of one-hooks-dir-per-repo against one-venv-per-worktree, and the lane correctly declined to
turn the refusal green by rewriting the shared checkout's hooks.

## 1.3 Positive verifications — run by this reviewer, not read off the branch

- **ADR-106 uv-pin fidelity — PASS.** Replayed `read_uv_pin`'s awk verbatim against the live
  `pyproject.toml`: returns `==0.11.19`, and the section scoping correctly steps past
  `[tool.ruff]`'s `required-version = ">=0.15.5"` (the trap a naive grep falls into). A non-`==`
  spec is refused by construction, so "a range is not a pin" is enforced, not asserted.
- **No secrets or host paths in `devcontainer.json` — PASS.** Full read. The only value-bearing
  tokens are the image tag, the stamp env var, `hostRequirements`, `remoteUser`, and two extension
  ids. No credential, token, or absolute host path.
- **Tree-seal lockstep — PASS, by execution.** Loaded branch C's `validate_hermetization.py` and
  ran it over **all 2238 tracked paths on the branch**: **0 Rule A violations, 0 Rule C violations**.
  (137 Rule B hits are pre-existing grandfathered legacy audit filenames — Rule B is
  prospective-only on staged ADDs — and none are attributable to this branch.)
- **The ADR's counterfactual is TRUE, not decorative — PASS.** Removing `.devcontainer` from
  `_HOME_PATTERNS` while keeping the Tier-1 sanction makes Rule C refuse **both** substrate files.
  The amendment's stated reason for needing the home entry is therefore correct.
- **Rule C depth discipline — PASS.** `.devcontainer/scripts/extra.sh` and
  `.devcontainer/sub/nested/x.sh` are both refused, matching the bare-literal (not `*`/`**`) intent
  and the branch's own test.
- **ADR-101 amendment shape — PASS.** The hunk is `@@ -219,3 +219,11 @@`, 8 added lines, **zero
  deletions** — a pure append carrying its own `## Amendment — 2026-08-18` marker. That is the
  in-file-amendment-marker route CLAUDE.md §5 rule 3 sanctions, not an in-place edit.
- **`doc-counts` arithmetic — PASS.** 2974 → 2976 is exactly the two added test functions.
- **Line endings and mode — PASS.** `provision.sh` is committed LF-only (0 CR bytes in 16350) at
  mode `100755`; `devcontainer.json` is LF-only. A CRLF blob authored on this Windows workstation
  would have broken the script inside a Linux container; it did not happen.
- **The lane-contract audit file grew across 4 commits — NOT a violation.** Every touch is a pure
  append (0 deletions) under its own `# STEP N` / `# STOP packet` heading, which is the sanctioned
  amendment-marker shape and the established lane-record pattern in this repo.

## 1.4 Severity tally — branch C

| Severity | Count | Items |
|---|---|---|
| **P1** | **0** | — |
| **P2** | **1** | C-1 |
| **P3** | **4** | C-2, C-3, C-4, C-5 |

Machine-readable equivalent (Critical/High/Medium/Low, per the header): **0/1/4/0**.

## 1.5 Verdict — branch C

> ## `FIX-BEFORE-MERGE (itemized)`

**Itemized — one blocking item:**

1. **C-1** — set `"waitFor": "postStartCommand"` in `.devcontainer/devcontainer.json:52`.

**Explicitly NOT blocking:** C-2, C-3, C-4, C-5. C-3 is an operator standing decision, not a lane
fix. C-2 and C-4 are honesty refinements worth filing. C-5 is a first-boot watch item.

Rationale for blocking on a one-token change: the branch states a guarantee twice that the
configuration does not deliver in the one scenario the guarantee exists for, the substrate has never
been booted so nothing depends on merging it quickly, and the correction carries no behavioural
risk. Fixing it after merge would mean landing a documented claim known to be false.

---

# 2. BRANCH E — `worktree-lane-e-502-mutmut` @ `c43351de`

*(Recorded for linkage even though `check_review_artifact_coverage` reads only the header's branch —
see §0.3.)*
**Branch:** `worktree-lane-e-502-mutmut`
**HEAD:** `c43351de8134e9a5c040e3c4e5af099688b9a33d`
**Diff range:** `main..worktree-lane-e-502-mutmut` (merge-base `328d1086` == `main` tip)

4 commits, 5 files, +396/−2. Code surface is exactly two files: `tests/test_fleet_analytics.py`
(+19/−2) and `pyproject.toml` (+22/−0). `scripts/fleet_analytics.py` is **not** touched.

## 2.1 Codex findings — verbatim

> No Critical or High findings.
>
> ## Critical
> (none)
> ## High
> (none)
> ## Medium
> (none)
> ## Low
> (none)
>
> `pyproject.toml` is comment-only. The dotted registration and pre-exec ordering are correct for
> mutmut and `@dataclass`; both aliases share one object when `_load()` runs first. A bare-first
> custom collection could retain an earlier module reference, but the scoped mutation run collects
> only `test_fleet_analytics.py`, so this is not a Critical/High defect.

Codex additionally recorded that it *"verified the mutmut 3.7.0 implementation directly: it builds
keys from the repository-relative source path and records trampoline hits from
`orig_func.__module__`"* — i.e. the branch's central factual claim was checked against the tool, not
taken from the branch's prose.

## 2.2 Reviewer finding

### E-1 · **P3** · `tests/test_fleet_analytics.py:43-45` — the alias comment's "always" is collection-order dependent

The retained-alias comment says `tests/test_gitenv.py`'s bare `import fleet_analytics` *"is what
that import has always resolved to"*. Precisely: `fa = _load()` runs at module scope
(`test_fleet_analytics.py:51`), and in a whole-suite collection `test_fleet_analytics.py` is
imported before `test_gitenv.py`, so the claim holds **there**. Run `pytest tests/test_gitenv.py`
alone and the bare import resolves through `sys.path` to a distinct module object instead.

**Behaviour is correct either way** — both objects are built from the same source file and
`test_gitenv.py` binds `fa` at its own import time regardless. This is a precision nit on a comment,
with no functional consequence. Reported so the review does not read as having found literally
nothing.

## 2.3 Positive verifications — run by this reviewer

- **`pyproject.toml` is comment-only — PROVEN, not read.** This is the contract's *"byte-diff the
  TOML values"* item, discharged with a hard check: both blobs parsed with `tomllib.loads` compare
  **equal across the entire parse tree** (`t1 == t2` → `True`), and of the 22 added/removed diff
  lines, **0 are non-comment**. No key, value, ordering or type moved.
- **Blast radius — bounded to exactly one other importer.** Grepped every `.py` on the branch for
  `fleet_analytics`. The single import that resolves through `sys.modules` under the changed name is
  `tests/test_gitenv.py:41` (`import fleet_analytics as fa`), and the bare alias
  `sys.modules["fleet_analytics"]` is **retained** pointing at the same object, so it is unchanged.
  Every other hit is a comment, a docstring, a filename string, an AST source read, or a subprocess
  probe: `scripts/audit.py:193`, `scripts/gitenv.py:11,55`, `tests/test_gitenv.py:108,142,187,190,253,259`,
  `tests/test_fleet_analytics.py:492`. **No `from scripts import fleet_analytics` exists anywhere.**
- **The fix actually does what it claims — verified by execution.** Because
  `scripts/fleet_analytics.py` is byte-identical on both branches, the loader was replayed
  in-process both ways against the live file: under the old name `Config.__module__ ==
  "fleet_analytics"`; under `_MODNAME` it is `"scripts.fleet_analytics"` — which is exactly the
  prefix mutmut's trampoline compares against its path-derived mutant keys. The alias `is` the same
  object.
- **`sys.modules` registration is correct.** Register-before-exec ordering is right for
  module-level `@dataclass` resolving `cls.__module__`; both keys are bound before `exec_module`.
- **The dotted key with no parent package is benign, and its side effect PRE-DATES this change.**
  `scripts/__init__.py` does not exist, so `scripts` can only ever be an implicit namespace package.
  Executing the module creates `sys.modules['scripts']` — but this was verified to happen **on main
  too**, via `scripts/fleet_analytics.py:111 import audit` → `scripts/audit.py:94 from scripts import …`.
  Branch E introduces no new side effect here.
- **Dual-identity risk is REDUCED, not increased.** Before the change a later
  `import scripts.fleet_analytics` would have constructed a second module object from the same file
  — the hazard `scripts/block_ff_push.py:73` explicitly warns about. After it, that import resolves
  to the one object the test already loaded.
- **No relative-import or `__package__` sensitivity.** `scripts/fleet_analytics.py` contains no
  relative imports and never reads `__package__`, so `spec.parent = "scripts"` changes nothing about
  how it resolves `import audit` / `import gitenv`.

**Not re-verified (contract: no re-running their suites beyond what review needs):** the artifact's
own pilot numbers — 2291/2291 mutants checked, 1210 survived, 4/4 keys matching. Those are the
lane's measurements; this review checked the *mechanism* that makes them possible, not the counts.

## 2.4 Severity tally — branch E

| Severity | Count | Items |
|---|---|---|
| **P1** | **0** | — |
| **P2** | **0** | — |
| **P3** | **1** | E-1 |

Machine-readable equivalent: **0/0/1/0**.

## 2.5 Verdict — branch E

> ## `MERGE-CLEAN`

E-1 is a comment-precision nit and blocks nothing. The change is two files, one of which is proven
comment-only by parse-tree equality; the other's blast radius is a single other importer whose
behaviour is preserved by a deliberately retained alias.

---

# 3. Combined summary

| Branch | HEAD | P1 | P2 | P3 | Verdict |
|---|---|---|---|---|---|
| C — `worktree-lane-c-554-devcontainer` | `5506f59a` | 0 | 1 | 4 | **FIX-BEFORE-MERGE (itemized)** — 1 item: C-1 |
| E — `worktree-lane-e-502-mutmut` | `c43351de` | 0 | 0 | 1 | **MERGE-CLEAN** |

**Scope honoured:** branches A, F, G and D were not reviewed. Nothing on either reviewed branch was
modified — this lane wrote only this artifact and its contract of record.
