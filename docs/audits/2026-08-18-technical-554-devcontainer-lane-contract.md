# Lane C — [#554] devcontainer + provisioning (NB4-G stage 1) — contract of record

- **Date:** 2026-08-18
- **Class:** technical (ADR-101 §2 audit grammar)
- **Lane:** C — worktree branch `worktree-lane-c-554-devcontainer`, cut from `main`
- **Mode:** execute — contract-is-the-plan, commit-and-STOP, never merge, never push `main`
- **Governing row:** `[#554]` (`tasks/554-devcontainer-provisioning-script-nb4-g-stage-1.md`) — the row's
  Done-when governs; the prompt below only frames it
- **Detail carrier:** intake #39 `docs/intake/2026-08-17-tech-off-machine-agent-substrate.md` (status DRAFT)
- **ADR-110 requirement:** this file IS the frozen prompt, landed before any lane work, per the contract's
  own STEP 0

## Operator approval of record (D6)

> **Operator approval D6 for the new `.devcontainer/` path was granted at GO.**

That sentence is recorded here and in this artifact's commit message because `.devcontainer/` is a **new
Tier-1 top-level directory**, which `scripts/validate_hermetization.py` Rule A refuses by construction
(ADR-101 §1: the top level is a closed set, grown only by an ADR-101 amendment or an explicit operator
ruling). The D6 approval is that operator ruling; the ADR-101 in-file amendment is the channel that makes it
machine-checkable, on the four standing precedents (`.methodology.yaml` 2026-07-13, `uv.lock` +
`.python-version` 2026-07-27, `tasks/` 2026-07-27, `.github/` 2026-08-06). **Any other new path → STOP.**

## The frozen prompt, verbatim

```markdown
# LANE C — #554: DEVCONTAINER + PROVISIONING (NB4-G STAGE 1)

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — contract-is-the-plan, NO plan-mode | medium |

> Fresh CC session (`/clear`). Worktree lane — commit-and-STOP, never merge.

**Worktree (STEP 0):** `git worktree add ../worktree-lane-c-554-devcontainer -b worktree-lane-c-554-devcontainer main`
**Governing row:** `[#554]` — read `tasks/554-*.md` verbatim FIRST; its Done-when governs this
lane, this prompt only frames it. Detail carrier: intake #39 (off-machine agent fleet substrate);
substrate direction is operator-confirmed: **Codespaces free tier = stage 1** (Hetzner is stage 2,
NOT this lane).
**ADR-110:** save this prompt as
`docs/audits/2026-08-18-technical-554-devcontainer-lane-contract.md`, COMMIT first.
**Rule C:** `.devcontainer/` is a new top-level path — **operator approval granted at batch GO
(D6)**; record that sentence in your contract commit. Any OTHER new path → STOP.

## PINNED-BY-TESTS
- `tests/test_validate_hermetization.py` Rule C pins — you add `.devcontainer/` under the D6
  approval and nothing else anywhere.
- ADR-106 uv pin: the repo pins `uv ==0.11.19` and the cloud channel died on `0.8.17` (NB7-C §9,
  a fourth organ silenced). The devcontainer MUST provision the pinned uv version — that mismatch
  is half the reason this row exists.

## UNDERSTAND
- Problem: cloud/remote lanes run on unprovisioned substrates — wrong uv, missing toolchain,
  silent gate non-execution (intake #32's fail-closed concern).
- Scope: `.devcontainer/devcontainer.json` (+ Dockerfile only if the row demands it), one
  idempotent provisioning script at the row's named home, one smoke assertion.
- Failure mode to avoid: a devcontainer that builds but provisions an environment whose gates
  don't execute — green-looking, untrusted.

## STEPS
**STEP 0** — worktree + contract commit. `COMMIT`
**STEP 1** — quote `[#554]`'s Done-when + intake #39's stage-1 clauses into the lane artifact;
derive the checklist this lane must satisfy — the row's list, not an invented one. `COMMIT`
**STEP 2** — `.devcontainer/devcontainer.json`: pinned uv (ADR-106 version), Python per
`pyproject.toml`, `postCreateCommand` → the provisioning script. Config values declared, never
duplicated (single source: read pins from the repo files where feasible). `COMMIT`
**STEP 3** — provisioning script (idempotent — second run is a no-op, and says so): toolchain
install, `uv sync --locked`, pre-commit install, and a **gate-liveness smoke**: run one cheap real
gate (e.g. `validate_backlog`) and assert exit 0 — provisioning that cannot prove its gates run
is the intake-#32 failure shape. `COMMIT`
**STEP 4** — proof (the at-risk matrix item): boot the devcontainer where you can actually prove
it — local `devcontainer build`/CLI or a Codespaces boot — and capture the log (build OK +
provisioning OK + smoke OK) into the lane artifact. **Fork (report):** if no boot channel is
available from this session, deliver everything else and STOP-report the proof as the one open
acceptance item — do not fake a log. `COMMIT`

## FINAL
Targeted tests `-n 0` (any test the row's Done-when names; hermetization suite). Commit-and-STOP.
STOP packet: Done-when checklist with per-item state · proof log or the fork report · files added.

## WHAT NOT TO DO
No Hetzner/stage-2 work · no CI workflow edits · no new paths beyond `.devcontainer/` + the row's
named script home · no uv version drift from the ADR-106 pin · no merge.
```

## STEP-0 deviation, recorded rather than smoothed over

The contract's STEP 0 names `git worktree add ../worktree-lane-c-554-devcontainer -b
worktree-lane-c-554-devcontainer main`. This session was launched with the `--worktree` flag, which had
**already** provisioned the lane at `.claude/worktrees/lane-c-554-devcontainer` on branch
`worktree-lane-c-554-devcontainer`. The **branch name matches the contract exactly** and is on the
CLAUDE.md §4 machine-produced lane enum (`worktree-<name>`); only the on-disk directory differs, and it sits
under the repo's own standard `.claude/worktrees/` home. No second worktree was provisioned: a branch is
checkable out in exactly one worktree, so the contract's literal command would have been refused, and
provisioning a second tree would have left a leftover to clean up (§5 rule 9).

## Steps 1–4

Filled in by the sections appended below as each step lands: STEP 1 the Done-when checklist derived from the
row, STEP 2/3 what landed, STEP 4 the proof log or the fork report. This artifact is the lane's single
record.

---

# STEP 1 — the governing text, quoted, and the checklist derived from it

## 1.1 `[#554]`'s Done-when, quoted verbatim

From `tasks/554-devcontainer-provisioning-script-nb4-g-stage-1.md`:

> - [#554] [P2][M] **Devcontainer + provisioning script (NB4-G stage 1)** — the reproducible container plus
>   provisioning script that lets a lane run OFF this machine, so batch width stops being bounded by one
>   workstation's measured admission ceiling of 6 concurrent lanes. Four legs, each a measured failure mode:
>   a pinned-`uv` assert, `git fetch --unshallow` (the gates read history; on a shallow clone they are
>   vacuous), deterministic `pre-commit install` for all three hook types, and an env gate that refuses to
>   start on a half-provisioned environment. The substrate is operator-decided and not this row's question.
>   · Done when: one lane runs green (`audit.py health` **and** `pytest -m 'not slow'`) on the Codespaces
>   free tier, and the *identical* script is runnable via `devcontainer up` on a VPS · refs
>   docs/intake/2026-08-17-tech-off-machine-agent-substrate.md, #541, #453, #528 · kill-candidates: none — no
>   row owns off-machine provisioning; [#541] owns the substrate DECISION and [#453] the cloud-container
>   PREFLIGHT for an already-provisioned session, a two-of-four-leg overlap whose second lander discharges by
>   pointing at the first · source: intake #39
>   `docs/intake/2026-08-17-tech-off-machine-agent-substrate.md`, which carries the four-leg rationale and
>   the substrate pricing in full

## 1.2 Intake #39's stage-1 clauses, quoted verbatim

**Section D — "the smallest first build the artifact names":**

> A `.devcontainer/devcontainer.json` + `provision.sh` that: (1) installs uv at the exact pinned version and
> **asserts** it; (2) runs `git fetch --unshallow`; (3) runs `pre-commit install` for commit+push hooks and
> **fails if not armed**; (4) gates the fleet-wide health check behind an env flag; then proves **one lane
> green (`audit.py health` + `pytest -m "not slow"`) on the Codespaces free tier.** The same file runs
> unchanged on the Hetzner VPS via `devcontainer up`.

**Proposed row R25** (the row this lane executes; NOT born as a backlog id — `[#554]` is):

> ```
> PROPOSED ROW R25 - .devcontainer + provision.sh that ASSERTS the three traps closed
>   Done-when: on a clean container build, the uv version equals the pinned value, `git
>              rev-parse --is-shallow-repository` returns false, and all three pre-commit hook
>              types are armed -- and the BUILD FAILS if any assertion fails (assert, not log).
>   kill-candidates: none -- arm_hooks.py closes the arming trap at SESSION start in the hub;
>              this closes it at PROVISION time for a fresh host, which is a different moment
> ```

**Acceptance criteria (ex-ante) 2 and 4**, the two that bind a provisioning script:

> 2. A container cannot start a lane with an unpinned toolchain, a shallow clone, or unarmed hooks — the
>    build fails first.
> 4. One lane has actually run green off-machine, with a recorded wall-clock, before any recurring spend is
>    committed.

## 1.3 The checklist — the row's list, not an invented one

Six items. **L1–L4 are the row's own four legs**, verbatim in kind; **D1–D2 are the row's own Done-when
clause, split at its `and`.** Nothing here is added by this lane.

| # | Source | Requirement | Lane state |
|---|---|---|---|
| L1 | row leg 1 | a pinned-`uv` assert — the provisioned uv equals the ADR-106 pin `==0.11.19`, asserted, not logged | see STEP 3 |
| L2 | row leg 2 | `git fetch --unshallow` — the gates read history; on a shallow clone they are vacuous | see STEP 3 |
| L3 | row leg 3 | deterministic `pre-commit install` for **all three** hook types (`pre-commit`, `commit-msg`, `pre-push`), asserted armed | see STEP 3 |
| L4 | row leg 4 | an env gate that **refuses to start** on a half-provisioned environment | see STEP 3 |
| D1 | Done-when a | one lane runs green — `audit.py health` **and** `pytest -m 'not slow'` — on the Codespaces free tier | STEP 4 proof; at risk |
| D2 | Done-when b | the *identical* script is runnable via `devcontainer up` on a VPS | STEP 4 proof; at risk |

**Two derived obligations the contract adds on top of the row** (recorded as the contract's, not the row's,
so the provenance stays checkable):

| # | Source | Requirement |
|---|---|---|
| C1 | contract STEP 3 | the script is **idempotent** — a second run is a no-op *and says so* |
| C2 | contract STEP 3 | a **gate-liveness smoke**: run one cheap real gate (`validate_backlog`) and assert exit 0 — provisioning that cannot prove its gates run is the intake-#32 failure shape |

## 1.4 One divergence between the row and the intake, resolved in the row's favour

Intake #39's Section-D clause **(4)** reads *"gates the fleet-wide health check behind an env flag"* — that
is the intake's **proposed row R26** (`audit.py health` in a single-repo container SKIPS sibling-repo checks
cleanly rather than FAILing, `FLEET=1` restores them). The **row's** leg 4 is a different mechanism: *"an env
gate that refuses to start on a half-provisioned environment"* — a refusal in the provisioning script, not a
skip-semantics change in `audit.py`.

**The row governs** (contract: "its Done-when governs this lane, this prompt only frames it"), so leg 4 is
implemented as the row states it. R26 is rated *Could* by the intake, is a separate unborn row, and would
require editing `scripts/audit.py` — outside this contract's declared scope (`devcontainer.json`, one
provisioning script, one smoke assertion). **It is therefore NOT done here, and is named as an open
dependency rather than silently folded in.** Practical consequence for D1: if `audit.py health` in a
single-repo container FAILs on sibling-repo-dependent checks, that is R26's gap surfacing, not a defect in
this lane's script — and it is called out in the STEP 4 report rather than papered over.

## 1.5 Overlap discharge required by the row

The row names a *"two-of-four-leg overlap"* with `[#453]` (cloud-container PREFLIGHT for an
already-provisioned session) *"whose second lander discharges by pointing at the first"*. `[#453]` is
**open** and has **not** landed, so `[#554]` is the first lander on those legs and the discharge obligation
falls on `[#453]`, not here. Recorded so the second lander can find it.

---

# STEPS 2–3 — what landed, and how each leg is asserted

## 2.1 Files added (the complete footprint of this lane)

| Path | Role |
|---|---|
| `.devcontainer/devcontainer.json` | the spec file — image, wiring, the env-gate knob |
| `.devcontainer/provision.sh` | the one idempotent provisioning script; all six asserts live here |

**No other new path exists in this lane.** Four *existing* files were modified, all of them the lockstep the
D6 approval requires or a generated count: `docs/decisions/ADR-101-hermetization.md` (amendment appended),
`scripts/validate_hermetization.py` (Rule A + Rule C entries), `tests/test_validate_hermetization.py` (two
pins), `ecosystem/doc-counts.md` (regenerated), plus this artifact and `docs/audits/README.md`.

## 2.2 The tree-seal lockstep

`.devcontainer/` is a new Tier-1 top-level directory and `scripts/validate_hermetization.py` refuses those by
construction. Landed in one commit on the four standing precedents (`.methodology.yaml`, `uv.lock` +
`.python-version`, `tasks/`, `.github/`): the ADR-101 in-file amendment, `SANCTIONED_TIER1_DIRS +=
".devcontainer"` (Rule A), `_HOME_PATTERNS += ".devcontainer"` (Rule C), and two test pins.

**Rule C needed its own entry, and this is not a formality.** Rule A seals the top level only; Rule C reads
the rest of the path against a home allowlist derived from the live taxonomy. Sanctioning the directory
without adding the home would have refused the very file the approval sanctions —
*"new path outside allowlisted homes"* — and would have redded
`test_rule_c_admits_every_tracked_path_in_the_live_repo` the moment the file was tracked. The home is the
**bare literal**, not `.devcontainer/*` or `.devcontainer/**`: two files at one level, so a sub-directory
stays a surfaced act. The added pin asserts exactly that (`.devcontainer/scripts/extra.sh` is still refused).

## 2.3 Single source of pins — the discipline, concretely

`devcontainer.json` is static JSON and cannot read a file, so **no pin is restated in it**. Every version is
read at provision time from the home it already has:

| Pin | Home | Read by |
|---|---|---|
| uv `0.11.19` | `pyproject.toml` `[tool.uv] required-version` (ADR-106) | `read_uv_pin()` |
| interpreter `3.12.10` | `.python-version` | `read_python_pin()` |
| dependencies | `uv.lock` | `uv sync --locked` |

`read_uv_pin()` is **section-scoped awk**, not a grep, and that is load-bearing: `[tool.ruff]` carries a
`required-version` too (`>=0.15.5`), and a naive line match would read the ruff floor as the uv pin. It also
**refuses a non-`==` spec** — leg 1 is *"a pinned-`uv` assert"*, and a range is not a pin. Verified against
the live file: it returns `==0.11.19`, not `>=0.15.5`.

The base-image tag is the one version token `devcontainer.json` carries, and it is a **floor, not the pin**:
uv installs the exact `.python-version` interpreter for the project venv and the script asserts the result,
so the image's own Python never decides what the gates run on, and bumping `.python-version` needs no edit
to the spec file.

## 2.4 The checklist, leg by leg

| # | Requirement | How it is satisfied | State |
|---|---|---|---|
| L1 | pinned-`uv` assert | installs from the **version-pinned** astral URL (`astral.sh/uv/<pin>/install.sh` — never `latest`, which is how a cloud channel drifted onto `0.8.17`), then asserts `uv --version` **equals** the pin. The install is not the leg; the assert is. | **done** |
| L2 | `git fetch --unshallow` | guarded by `git rev-parse --is-shallow-repository` (so it is a no-op on a full clone, where `--unshallow` would error), then asserts the repo is no longer shallow and prints the reachable commit count. Adds `safe.directory` check-then-add first, since a bind-mounted tree is otherwise untrusted by git. | **done** |
| L3 | all three hook types armed | delegates the install to `scripts/arm_hooks.py` (**reuse**, one predicate not two) and then asserts hard via that module's own `_hooks_dir` + `_armed`, which resolve through `core.hooksPath` and reject a shim bound to a stale interpreter. `arm_hooks` is fail-**soft** by design — correct at SessionStart, wrong at provision time — so the **refusal is this script's**, per intake #39 §D(3) *"fails if not armed"*. | **done** |
| L4 | env gate refusing a half-provisioned start | `--gate` mode, wired to `postStartCommand`. Refuses when the stamp is absent, when its schema is wrong, when the **repo's pins have moved since it was written**, or when any live assert (uv version / not shallow / hooks armed) fails. Stamp path is `DEV_KNOWLEDGE_PROVISION_STAMP`, declared in `containerEnv`. | **done** |
| C1 | idempotent, and says so | every leg is check-then-act; a `CHANGED` counter drives the closing line, which reads *"idempotent: nothing changed, all four legs were already satisfied"* when nothing acted. | **done** |
| C2 | gate-liveness smoke | runs `uv run --locked python scripts/validate_backlog.py` — **the invocation `.pre-commit-config.yaml`'s `validate-backlog` hook uses, verbatim**, so it proves that command line rather than a lookalike — asserts exit 0 and echoes its first output line, because a passing gate that printed nothing is indistinguishable from one that no-oped. | **done** |
| D1 | one lane green on Codespaces free tier | **open — see STEP 4** | at risk |
| D2 | identical script via `devcontainer up` on a VPS | **open — see STEP 4** | at risk |

## 2.5 Two honest limits, stated rather than left to be discovered

**(a) "Refuses to start" is as strong as the devcontainer spec allows.** There is no hook that hard-aborts a
container mid-start. A non-zero `postStartCommand` is the strongest refusal available: the runtime surfaces
a failed start, and `"waitFor": "postCreateCommand"` prevents a session attaching before provisioning
finishes. L4 blocks the session's start path loudly; it does not kill the container process. Nor is any of
this server-side — an operator can still run the tools by hand.

**(b) `arm_hooks._armed` is worktree-hostile, and this was measured, not reasoned about.** Git gives every
worktree of a clone the **same** hooks directory while `uv sync` gives each its **own** venv, so on a host
running N worktrees at most one satisfies L3 and the rest are refused as *"bound to a stale interpreter"*.
Reproduced on this workstation while testing (§3.2 below). Inside a container it cannot arise — one
checkout, one venv — but **intake #39's own stage-2 model is "N git worktrees" on the VPS**, so anyone
extending this to stage 2 inherits it. The limit belongs to `arm_hooks._stale_interpreter`, not to this
script, and is deliberately left there: a softened private copy of the predicate would give the repo two
answers to one question.

# STEP 3 — verification actually performed on this workstation

## 3.1 What could be exercised here, and what could not

This is a Windows workstation with no container runtime available to this session, so the **container** is
unproven (that is STEP 4's fork). What *was* exercised is the script's own logic, against the live repo:

| Check | Command | Result |
|---|---|---|
| shell syntax | `bash -n .devcontainer/provision.sh` | **OK** |
| usage path | `bash .devcontainer/provision.sh --help` | prints the three modes, exit 0 |
| pin reader vs the real file | the `read_uv_pin` awk against `pyproject.toml` | returns `==0.11.19` — correctly **ignores** `[tool.ruff]`'s `required-version = ">=0.15.5"` |
| L4 refuses an unprovisioned env | `provision.sh --gate` with no stamp | **REFUSED**, exit 1: *"no provisioning stamp … this container was never provisioned"* |
| L4 refuses a **moved pin** | `--gate` against a stamp recording `uv_pin=0.8.17` | **REFUSED**, exit 1: *"stamped uv pin 0.8.17 != repo pin 0.11.19 — the pin moved; re-provision"* |
| L4 live asserts run | `--gate` against a current stamp | proceeded past every stamp check to the live asserts, and refused on L3 — see §3.2 |
| hermetization suite | `pytest tests/test_validate_hermetization.py -n 0` | **45 passed** |
| lint | `ruff check` on both changed Python files | clean |

The `0.8.17` case is worth naming: that is the exact drift the lane contract calls *"half the reason this
row exists"*, and the gate refuses it.

## 3.2 The L3 refusal on this workstation is a real finding, not a script defect

`--gate` with a current stamp cleared uv (`0.11.19`) and the shallow check (`false`), then refused:

```
[provision] L3 resolved hooks dir: C:\Users\1028120\Documents\Dev\.dev-knowledge\.git\hooks
hooks present but NOT pre-commit-managed or bound to a stale interpreter
[provision] REFUSED: L4 git hooks are not armed
```

Diagnosed rather than assumed. All three shims exist and carry the pre-commit signature; the cause is the
interpreter binding:

```
INSTALL_PYTHON='...\.claude\worktrees\lane-e-502-mutmut\.venv\Scripts\python.exe'
uv run python -> ...\.claude\worktrees\lane-c-554-devcontainer\.venv\Scripts\python.exe
```

The shim is bound to a **sibling lane's** venv, so `_stale_interpreter` is True and `_armed` is False. This
is limit (b) above, reproduced. **The arming path was deliberately NOT run to make it green**: in a worktree
that would rewrite the shared primary checkout's hooks and rebind them away from whatever session is using
them. Turning a refusal green by mutating shared state that other live sessions depend on is not
verification.
