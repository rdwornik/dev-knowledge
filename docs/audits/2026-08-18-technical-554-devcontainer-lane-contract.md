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
