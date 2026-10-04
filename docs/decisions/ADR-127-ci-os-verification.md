# ADR-127: CI on Windows and Linux is the verification verdict; the harness and its consumers are OS-agnostic, checked

- **Status:** Accepted
- **Date:** 2026-09-27
- **Decision tier:** Path A — operator ratification of a producer's technical proposal under ADR-108 §A (R11, `RATIFICATION-2026-09-25` v9/v10, superseded-unchanged through v14).
- **Amends:** replaces R9 (interim O2). **Builds on** AK-8 (off-box portability, Drive stays the bus), AK-10 (CI as the gate, provisional), AL-B B8 ("required checks on, after the baseline is honest and the commit-gate is diff-scoped"), STANDING_RULINGS `:2910` ("base failed-set is PER SUBSTRATE").
- **Related:** ADR-110 (serial `--no-ff` integrator), ADR-120 (dispatch), ADR-121 (state-store event log — the git outbox ref D9 defers to), ADR-124 D5 (this ADR's own section shape), ADR-126 D2 ("full-suite merge verdict → CI").
- **Decommission:** the local full-suite obligation in `.claude/commands/lane-integrate.md` refuse-to-finish item 2, once D6 is armed (row L6, `lane-arm-ci` — not yet merged as of this ADR).
- **Source:** operator ratification (R11), recorded in `to-browser/RATIFICATION-2026-09-25-v9-superseded.md`; provenance `to-cc/BATCH-DECISION-CI-VERIFICATION-2026-09-26.md` (operator GO, 2026-09-26 ~21:30), after the withdrawn R10. Written from `to-browser/PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md` (decisions D1–D9), whose Step 5 records the process that produced it. Landed in-repo by `lane-portability-requirement` (batch WAVE5B-N4, row L9); `protocols/STANDING_RULINGS.md` §AN is the ruling-by-ruling in-repo ledger this ADR's Decision section summarizes.

## Context

**Why the harness did not use GitHub Actions fully.** Not because Actions could not carry it —
on this public repository the standard runners are free and unlimited (`ubuntu-latest` and
`windows-latest` both 4 vCPU / 16 GB, Pro allows 40 concurrent jobs), and the full suite ran in
570 s on a runner vs 4,935 s locally (run `36234959090`). Five things blocked it: (1) the base
was red on both OSes (61 shared failures on `5ba272ae`, 54 of the last 60 conductor runs
`failure`), so a gate refusing a red base refused every merge; (2) the landing protocol merges
locally with `--no-ff` and pushes, and a required status check refuses a pushed sha with no
passing status, while the receipt commit that follows the merge is a second unchecked tip;
(3) CI ran on `main` only, so lanes and integration branches were judged only by hand-dispatched
runs whose checkout lacked a local `main` (4 artefact reds); (4) `report-only-wall.yml` still
said "private on the Free tier" after the repo went public 2026-09-15, and the ruleset shipped
`enforcement: disabled`; (5) AK-10's rows and a Team-plan proposal were filed but not executed.

**Is the harness OS-agnostic?** Partly, and unchecked before this decision. Done: hooks off
PowerShell, every `os.name` site in `scripts/` had a POSIX arm (not all proven working), the
devcontainer, `[#632]`'s n=2 proof. Missing: CI never ran Windows; 27 Linux-only test failures
and 5 Windows-only ones existed at measurement time, the Drive transport bus had no off-Windows
client in use, and dispatch/harvest lived in a PowerShell module on an unmerged branch. The
requirement existed for the hub's own off-box path (AK-8) but not as "Windows and Linux alike
for the harness and every consumer", and nothing enforced it.

## Decision

- **D1 — The verification verdict is CI, on both OSes.** `conductor.yml`'s suite runs on
  `strategy.matrix.os: [ubuntu-latest, windows-latest]`, triggered by push to `main`,
  `worktree-**`, `epic/**` and the integrator's integration branches (`fail-fast: false`,
  `shell: bash` on both, checkout `fetch-depth: 0` plus a local `main` ref). The integrator's
  merge evidence is that run on the sha it will push, both legs; a lane gets the same run on its
  own push (advisory). **Landed** (row L1, `lane-ci-matrix`, merged `316d3205`).
- **D2 — One known-reds registry, keyed by OS, with failure signatures.** A member records node
  id and a failure signature (exception type + first failing assertion line); a changed
  signature, an unattributed member, or a non-member failure is a regression. The registry may
  only shrink without an operator ruling. **Shape landed** (`scripts/known_reds.py`,
  `logs/KNOWN-REDS-REGISTRY.json`; row L2, `lane-known-reds-signatures`).
- **D3 — Arm now on what is green, ratchet the rest in.** Required contexts: `pytest
  (ubuntu-latest)`, `pytest (windows-latest)`, `ruff`, `seal`, plus D4's two server-side
  equivalents; `pytest` passes when D2 finds no regression. Arming happens only after D5's probe
  picks the landing path. **Not yet armed** (row L6, `lane-arm-ci`).
- **D4 — Governance gates get server-side equivalents before arming**: a first-parent/no-FF
  spine check and the ADR-85 JOURNAL-anchor check run as CI jobs, so `--no-verify` no longer
  erases them. **Not yet built** (row L5, `lane-server-governance`).
- **D5 — The landing path is decided by a probe, not on paper.** A throwaway ruleset-protected
  pattern (never `main`) proves a full merge → anchor → receipt → push cycle end to end before
  any ruleset touches `main`. If a pre-checked sha is accepted and the receipt rides inside the
  checked range, landing stays local-merge + direct push; otherwise it moves to PRs. **Not yet
  run** (row L0, `lane-landing-probe`).
- **D6 — Local verification shrinks to what only the laptop can see.** Lanes keep targeted tests
  + `audit.py health` (R9's lane half, unchanged); the integrator reads CI and runs no local full
  suite, with a memory-gated bounded-wait fallback only when CI is unavailable, recorded as a
  fallback and never typed green. **Not yet armed** — R9 stays the interim standard until this
  lands (see §AN's R9 entry).
- **D7 — OS-agnostic is a requirement, scoped honestly.** *Hub:* every harness organ runs on
  Windows and Linux, enforced by D1 + D2 + a platform-skip ratchet (row L4) + host-witness
  isolation (row L3). *Consumers:* the deploy manifest ships a consumer CI template with the same
  OS matrix and a floor check that the consumer declares its supported platforms and runs CI on
  each; a consumer is compliant when its matrix is present and green-or-ratcheted. **This ADR's
  own lane (row L9) builds the consumer half of D7**: `templates/consumer-ci-matrix.yml` (the
  template) and `scripts/audit_checks/check_platform_matrix.py` (the floor check, registered in
  `audit.py`'s `ALL_CHECKS`) — both landed with this ADR.
- **D8 — Transport: one adapter, two backends.** `scripts/transport.py` gets a backend interface:
  the local Drive mount (Windows) and rclone (Linux) with the operator's own OAuth client, token
  as a user-level Codespaces secret. CI outputs travel as Actions artifacts; no repository
  secret. **Not yet built** (row L7, `lane-transport-rclone`).
- **D9 — Orchestration: one Python CLI, portable, in the hub (R11 answer 3).** The Codespace
  exec/harvest/After/Stop legs move from PowerShell to Python, living in `scripts/dispatch.py`
  (continuing the operator-ruled wave2 MOVE); the "Layer 2 never executes" wording is amended by
  the lane that ports it. The cloud leg stays on its current undocumented endpoint until an
  R2-compatible documented path exists. **Not yet built** (row L8, `lane-dispatch-port-hub`).

## Consequences

- The integrator stops running an 82-minute local suite once D6 arms; merge evidence becomes a
  URL. Laptop memory stops being the verification bottleneck.
- Two CI legs per push (16 lanes × 2 OS = 32 jobs, under the 40-job Pro concurrency cap); a
  second concurrent batch queues.
- Tests that read the operator's disk become explicit host witnesses (row L3); some verification
  of the operator host stays local — the price of honesty, not an oversight.
- A consumer with no declared platform matrix now FAILs its `audit.py` run (D7, this ADR's own
  row L9) — a new, real gate on every consumer repo, not only the hub.
- Risks carried forward with named trip-tests (from the proposal's evaluator round): a same-repo
  branch editing the workflow that judges it (the required contexts are read from `main`'s
  ruleset; D4's spine check refuses workflow edits without a named ruling); signature masking
  (D2's RED-first witness); artifact leakage (D8's Actions artifacts carry no transport
  credentials, tested by grep); an R2 or Layer-2-invariant rejection stopping D8/D9 while D1–D7
  proceed independently.

## Flip-condition

The Windows leg becomes a smoke tier (not the full suite) if its measured duration on
`windows-latest` exceeds 40 minutes — the sensitivity bound the decision matrix names (A7 falls
below A4's score past that point). Landing reverts from direct-push to PR-based (A4) if D5's
probe ever shows a pre-checked sha cannot be pushed directly, or the receipt commit cannot ride
inside the checked range. Org transfer + a merge queue (A6) is reconsidered if concurrent
integrators across repositories (ADR-126 D3) start colliding on `main`. D8's rclone backend is
replaced by a Drive API client (B3) if the operator declines rclone in the Codespace container.
None of D1, D2, D3, D6 or D7 (the verdict, registry, arming posture, local-verification
shrinkage, or the consumer floor) has an identified flip — they are measured wins on every
scored axis and reversing any of them would mean reverting to the pre-decision state this ADR
exists to replace.

## Alternatives considered

Scored in the proposal's decision matrix (weights: fidelity 25, portability 20, throughput 20,
cost 10, modifiability 10, observability 15; area scores on a 5-point scale):

- **A1 — today's local Windows-only suite (R9/O2).** Score 1.80. Kept as the interim standard
  until this ADR's mechanisms arm (see §AN R9); rejected as the destination because it never
  measures Linux and costs the full local suite on every merge.
- **A2 — CI Linux red-set only (the withdrawn R10).** Score 3.50 but explicitly fails the
  portability requirement this ADR exists to satisfy — a Linux-only verdict cannot prove the
  harness is OS-agnostic, only that one OS works.
- **A3 — matrix + direct-push landing, arm after burn-down.** Score 3.40. Waiting for a fully
  green base before arming is the R10-in-disguise failure mode the pre-mortem named; D3 arms on
  the green set now instead.
- **A4 — matrix + PR landing.** Score 3.55; the fallback D5's flip-condition names if direct push
  is not viable. Not chosen as the default because it changes the landing protocol before there
  is evidence the change is needed.
- **A5 — a self-hosted runner on a VM.** Score 3.05, and Linux-only (public-repo self-hosted
  runners execute pushed code — a real security exposure a hosted runner does not carry).
- **A6 — organisation transfer + Team plan + merge queue.** Score 3.15; a repo move and seat cost
  for a queue the serial `--no-ff` integrator already provides (ADR-110). Reconsidered only if
  concurrent cross-repo integrators start colliding (see Flip-condition).
- **A7 — matrix + signature registry, armed now on the green set (D1–D6, chosen).** Score 3.90,
  the highest of the area-A options — it arms immediately rather than waiting on a green base,
  the pre-mortem's most likely failure mode for every other option.
- **Transport (area B):** B1 (today, 2.20) and B4 (a lane report committed in git, 2.60 —
  contradicts the transport registry and needs git auth in the container) were rejected; B2
  (rclone, 3.85, chosen) edges B3 (a Drive API client, 3.75) by one Modifiability point — a
  binary vs. two pip dependencies and wrapper code; B3 is the named fallback if rclone is
  declined. B5 (GitHub replaces Drive) and B6 (Drive MCP) were rejected for needing a live
  connector or browser consent neither available headless.
- **Orchestration (area C):** C1 (today, 2.45) and C2 (pwsh 7 on Linux as-is, 2.95) were
  rejected as deployed-branch drift accumulators; C3 (Python port in the hub, chosen, 3.10) and
  C7 (the same port in win-tooling, 3.10) scored within 0.05 of each other and of C6 (Actions as
  orchestrator, 3.15) — the matrix could not decide between them, so D9 records the operator's
  Layer-2 ruling (R11 answer 3: the hub) as the deciding input rather than a scored one. C5
  (Managed Agents cloud leg, 3.00) stays gated on an R2 credential ruling.

## AMENDMENT 1 — 2026-10-04, what D1, D3, D4, D5 and D6 are as built (lane `foundation-4-merge-gate`, batch FOUNDATION)

> In-file amendment marker. The Decision section above is unchanged; where it says "Not yet
> built", "Not yet armed" or "Not yet run", this section is the current state.

- **D4 — landed.** The server-side spine and ADR-85 anchor checks, plus the seal, run as CI jobs
  for every push: merge `119c8fc8` (`lane-server-governance`). As built they judge a push to an
  **integration branch** as a push to `main` (stdin `refs/heads/main <tip> refs/heads/main
  <origin/main sha>`), so a creation, an update, a fast-forward-shaped and an unanchored push are
  each refused there exactly as they are on `main` (`scripts/merge_path.py target-line`).
- **D5 — run.** The landing probe is merge `2baecfca` (`lane-landing-probe-2`, record
  `docs/audits/2026-09-27-technical-landing-probe.md`): a pre-checked sha **is** accepted by a
  direct push, and a receipt tip that follows the merge as a second unchecked commit is **not**.
  The path built on that result is integration-branch-first, not PRs: `scripts/merge_path.py land`
  pushes the merge to `worktree-integrate-<batch>`, waits for CI on that sha, re-checks that
  `origin/main` is still the base, and pushes the SAME sha to `main`. A non-merge commit that
  follows (receipt ledger, audits index) is a second unchecked tip and rides with the next merge.
- **D1 — as built.** The verdict is one function, `ci_verdict.verdict_for`, which delegates the
  classification to `actions_verdict.verdict_for`: push runs only, completed runs only, and
  IN-PROGRESS, CANCELLED, a poll timeout and GH-UNAVAILABLE fail closed. A pytest leg is compared
  **test by test, per OS**, against the registry read at the baseline sha
  (`known_reds.compare_to_base`), so a new red inside an already-red job is a regression
  (`424d6c72` shape). The merge is recorded in two halves, split at the push
  (`merge_receipt`: `integration_branch`, `pushed_sha`, per-stage minutes).
- **D3 — as built, still not armed.** `deploy/conductor-required-checks.ruleset.json` carries six
  required contexts — `pytest (ubuntu-latest)`, `pytest (windows-latest)`, `ruff`, `seal`,
  `spine`, `anchor` — no bypass actor, `refs/heads/main`, `enforcement: disabled`. Applying it is
  the operator's act (`merge_path.py ruleset apply`, a dry run until `--execute`) and refuses
  unless both pytest legs are green on a rehearsal sha first (G1).
- **D6 — unchanged.** The integrator's local suite stays in the walk: removing it needs a
  ratification that records Q7(a), and none did at the time of this amendment.
