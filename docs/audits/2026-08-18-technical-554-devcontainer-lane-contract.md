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
