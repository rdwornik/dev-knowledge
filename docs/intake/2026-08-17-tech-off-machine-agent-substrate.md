---
intake-id: 39
status: DRAFT
origin: browser research artifact wf-fe444def, commissioned + landed 2026-08-17; converted to intake by lane R (unrostered, running alongside batch 7a)
note: Sections A-D are required by the lane-R contract of record (docs/audits/2026-08-17-technical-research-intake-lane-contract.md section 1). All eight ADR-98 template sections are present and carry them; Section C is the one added top-level section, because a doctrine-delta is neither a requirement nor an open question.
consumers: the technical-architect triage; no ADR and no backlog row has been born from this doc
---

# Off-machine agent fleet substrate — the re-priced, verified-August-2026 plan

## Problem / motivation

This is the only one of the five memos that **audits a prior in-repo artifact and finds part of
it stale**. Its subject is the compute-placement question already worked here: the memo
`docs/archive/2026-08-09-research-compute-placement-wf-1dc18e42.md` and the intake it fed,
**[#32] `2026-08-09-tech-compute-placement-and-remote-execution.md` (status ACCEPTED)**. The
verdict is mostly confirmation — *"The internal audit was mostly RIGHT on architecture and
directionally right on economics"* — with one correction that changes the hardware spec:
**Hetzner repriced twice in 2026 and the dedicated CCX line the prior plan leaned toward rose
2.13×–2.73×, while the CX shared line rose only ~1.3×–1.4×.** The recommendation flips from
CCX to CX.

Two things make this urgent rather than merely interesting. First, **[#32] is ACCEPTED**, so it
is a standing authority carrying a now-stale price basis, and `docs/intake/README.md` §5 is
explicit that an ACCEPTED doc "stays live and visible". Second, the memo carries a dated
external deadline that has essentially arrived: Oracle begins enforcing its reduced Always Free
limits **on 18 August 2026 — tomorrow relative to this doc** — automatically terminating
instances that exceed them.

### Section A — the artifact's own TL;DR, quoted

> - **Do NOT buy a GPU.** A coding-agent fleet that calls hosted APIs (Anthropic/OpenAI/Google) is I/O-bound (waiting on token streams, file I/O, git, tests), not GPU- or CPU-bound. A GPU only earns its keep if you run open-weight models locally — which in 2026 still trails frontier models by ~8–9 SWE-bench points and 5–20× on latency, and a usable 48 GB-VRAM box costs more per hour than an entire CPU VPS fleet.
> - **Fastest path this week:** Day 1 = a `.devcontainer` proven on the Codespaces free tier (120 core-hours/mo free). Week 1 = one hourly **Hetzner CX53** shared-vCPU instance (16 vCPU / 32 GB / 320 GB NVMe, €29.49/mo cap, ~€0.0473/hr) driven by VS Code Remote Tunnel + tmux, N git worktrees, branch-per-lane pushed to origin. This offloads your Windows laptop with zero change to how you work — an intensive 8-hour batch costs about €0.38.
> - **The internal audit was mostly RIGHT on architecture and directionally right on economics, but its Hetzner pricing is now STALE:** Hetzner raised cloud prices twice in 2026 (Apr 1 and Jun 15). The dedicated/shared-AMD lines it leaned toward jumped hardest — CCX rose 2.13×–2.73×, CPX rose 2.44×–2.75× — while the CX/CAX shared lines rose only ~1.3×–1.4%. The hourly÷~624 monthly-cap crossover model it relied on is still correct; the specific per-instance dollar figures are not. **Switch the spec to the CX shared line.**

*(The third bullet's "~1.3×–1.4%" is a typo in the source artifact; the body of the memo — Key
Finding 4 — reads "~1.3×–1.4×". Quoted verbatim above per the byte-faithful landing discipline,
and corrected here rather than silently in the quote.)*

## Scenarios (+1 view)

- **As the operator I** act on [#32]'s ACCEPTED plan and budget a 16-lane dedicated spec, **and
  then** pay roughly 3× what the plan assumed, because the plan's price basis predates two
  repricings it cannot know about.
- **As the operator I** dispatch a batch of 12 lanes on my Windows laptop, **and then** watch
  the machine saturate on RAM while the actual binding constraint turns out to be the Claude
  weekly rate limit — a ceiling more hardware does not raise.
- **As the operator I** provision a fresh container to run a lane, **and then** the lane runs
  with hooks unarmed for the first half of its session and its "clean" commits never passed a
  gate — the race this repo already knows as the relic-hooksPath / arming class.

### Section D — the smallest first build the artifact names

Quoted from the memo's own "The smallest first build (next 2 hours)":

> A `.devcontainer/devcontainer.json` + `provision.sh` that: (1) installs uv at the exact pinned version and **asserts** it; (2) runs `git fetch --unshallow`; (3) runs `pre-commit install` for commit+push hooks and **fails if not armed**; (4) gates the fleet-wide health check behind an env flag; then proves **one lane green (`audit.py health` + `pytest -m "not slow"`) on the Codespaces free tier.** The same file runs unchanged on the Hetzner VPS via `devcontainer up`.

Cost of that first build: **€0** (Codespaces free tier, 120 core-hours/month). It validates the
entire organ-executability surface before any money is spent, and the same file later runs
unchanged on the VPS.

## Functional requirements

### Section B — the decisions this would force on THIS repo

Six proposed rows. **NOTHING BELOW IS BORN.** No `BACKLOG.md` line, no `tasks/` file, and no id
is consumed; lane R holds no reserved id block.

```
PROPOSED ROW R24 - Re-base the compute plan onto the CX shared line
  Done-when: intake #32 carries an amendment or a superseded-by pointer naming this memo, and
             no live doc cites a CCX price as current; a grep for the stale figures returns
             only historical/quoted contexts.
  kill-candidates: none -- this AMENDS an ACCEPTED intake rather than adding scope; if the
             triage rules the amendment unnecessary, the row dies with a recorded reason

PROPOSED ROW R25 - .devcontainer + provision.sh that ASSERTS the three traps closed
  Done-when: on a clean container build, the uv version equals the pinned value, `git
             rev-parse --is-shallow-repository` returns false, and all three pre-commit hook
             types are armed -- and the BUILD FAILS if any assertion fails (assert, not log).
  kill-candidates: none -- arm_hooks.py closes the arming trap at SESSION start in the hub;
             this closes it at PROVISION time for a fresh host, which is a different moment

PROPOSED ROW R26 - Gate the fleet-wide checks behind an env flag so a single-repo lane is clean
  Done-when: `audit.py health` in a single-repo container SKIPS the sibling-repo-dependent
             checks cleanly (reporting them as skipped, never as passed) rather than FAILing;
             FLEET=1 restores them.
  kill-candidates: none -- and note the honest distinction this row must preserve: a skipped
             check is NOT a passed check, and rendering it green would be the dead-detector
             failure [#36] exists to prevent

PROPOSED ROW R27 - Prove ONE lane green off-machine at zero cost
  Done-when: `audit.py health` + the non-slow suite run green inside a Codespaces free-tier
             container, and the run is recorded with its wall-clock so later substrate
             claims are measured against it rather than estimated.
  kill-candidates: none -- this is the [#32] Stage-0 precondition made concrete

PROPOSED ROW R28 - Plan lane width against the RATE LIMIT, not the core count
  Done-when: a batch manifest's width declaration cites the rate-limit budget alongside the
             process-lane cap; a width that cannot be sustained by the account's allowance is
             refused at dispatch rather than discovered mid-batch.
  kill-candidates: extends the existing ex-ante process-lane cap declaration in the batch
             manifest (PLAYBOOK Ch8) -- propose one more line in that section, not a new gate

PROPOSED ROW R29 - Toolchain-pinning + gates-ran attestation as the cloud precondition
  Done-when: a lane executed off-machine emits an attestation naming the toolchain versions
             it ran and which gates fired; a merge from an off-machine lane without one is
             refused.
  kill-candidates: overlaps [#36]'s R9 (independent record of --no-verify/SKIP= usage) --
             propose ONE attestation record serving both, not two
```

- **Must:** R24. An ACCEPTED intake carrying a stale price basis is the highest-cost error
  available here, and correcting it costs nothing.
- **Should:** R25 and R27 — €0, and the memo rates them the smallest first build.
- **Could:** R26, R28, R29.

## Acceptance criteria (ex-ante)

1. No live document cites a Hetzner price as current that predates the June 2026 repricing.
2. A container cannot start a lane with an unpinned toolchain, a shallow clone, or unarmed
   hooks — the build fails first.
3. A skipped fleet-wide check reports as skipped, never as passed.
4. One lane has actually run green off-machine, with a recorded wall-clock, before any
   recurring spend is committed.

## Non-goals

- Buying or renting a GPU. The memo's verdict is unambiguous and flips only on a
  data-sovereignty mandate or sustained token spend above roughly $500–1,000/mo.
- Oracle Cloud Always Free. The memo names it a trap: the ARM allocation was halved effective
  15 June 2026 and enforcement (with automatic termination of over-entitlement instances)
  begins **18 August 2026**.
- GitHub Actions hosted runners as the fleet substrate — disqualified by the hard 6-hour job cap.
- Anthropic cloud sessions as the substrate. Beyond the memo's routing point, this repo's
  branch enum already admits `claude/<slug>` lanes, and memory records that the ADR-110 batch
  exemption never covers them.
- Any file-sync tool (Mutagen/Syncthing/rsync) between laptop and host. The memo: they "cause
  `.git` index divergence and race the agents."

## Section C — what this supersedes or contradicts in current doctrine (locators)

**SUPERSEDES — the one genuine supersession across all five landed memos:**

- The Hetzner price basis in `docs/archive/2026-08-09-research-compute-placement-wf-1dc18e42.md`
  and anything [#32] `2026-08-09-tech-compute-placement-and-remote-execution.md` (**status
  ACCEPTED**) carries forward from it. Specifically: **the dedicated-CCX spec is superseded by
  the CX shared line.** The *architecture* (three planes, worktree-per-lane, branch-per-lane,
  laptop-as-integrator) and the **hourly ÷ ~624 monthly-cap crossover model are CONFIRMED and
  survive intact** — the memo verifies CX53 at €0.0473/hr ÷ €29.49 ≈ 623 hours against the
  prior figure of ~624. Only the per-instance dollar figures fall.
  **This doc does not edit [#32].** ADRs, handoffs and audits are immutable (`CLAUDE.md` §5
  rule 3) and an ACCEPTED intake is a standing authority; amending it is R24's job under a
  ruling, not a lane's drive-by.

**CONFIRMS — including one trap this repo has already half-closed:**

- *"The hook-arming race is a genuine determinism bug and must be closed in provisioning."*
  This repo closes it at *session* start — `arm_hooks.py` is the "RF-2 hub self-arm —
  idempotent `pre-commit install` of the 3 hook types … asserted by `audit.py`
  check_hooks_armed" (`CLAUDE.md` §9). The memo wants it closed at *provision* time and wants
  the build to **fail** if hooks are not armed. Different moment, same defect; R25 covers the
  gap. This repo also knows the failure empirically: a relic `core.hooksPath` silently disarms
  the gates, witnessed twice.
- *"a branch can be checked out in only one worktree at a time — Git blocks a second checkout
  to prevent index corruption"*, and worktrees as "the correct isolation primitive for parallel
  agents". This is the live model: four worktrees are checked out for this batch, and
  `git worktree` isolation is what makes lanes a/b/c/R concurrent at all.
- *"Rate limits bind before hardware."* Not currently reflected in dispatch: the batch-7a
  manifest declares a process-lane cap against **width**, with no rate-limit term (R28).
- Codespaces/Actions shallow-clone default breaking history-dependent checks — directly
  relevant here, where `journal_spine_anchor`, `no_ff_merges` and the git-log detectors are all
  history-dependent and would silently misbehave on a shallow clone.
- *"a single-repo container can't discharge a health check expecting sibling repos"* — this is
  the known `fleet_parity`-mis-resolves-a-consumer class in commit context (R26).

**CORROBORATES a measurement, which is worth recording because the memo flags it as unverified:**

- The memo's caveat: *"The audit's baseline measurements (19.0 s health, 507.4 s pytest) are
  internal and were not independently reproducible online; they are plausible and internally
  consistent with an I/O-bound profile."* They are reproducible *here*: 507.4 s ≈ 8.5 min sits
  squarely on the ~9-minute isolated full-suite figure this repo measured on 2026-08-09. The
  memo could not verify it from outside; the repo can, and does.

## Impact sketch (4+1 lite)

- **Logical:** unchanged. The memo confirms the three-plane architecture rather than replacing it.
- **Process:** dispatch gains a rate-limit term (R28) and an off-machine attestation (R29);
  batch integration continues to happen on the Windows checkout.
- **Development:** a `.devcontainer/` tree and a provisioning script; R26 touches the health
  check's skip semantics.
- **Physical:** the only one of the five memos whose primary impact IS the physical view — a
  rented CX53 replacing the laptop as execution plane.

## Open questions

1. Does amending an **ACCEPTED** intake require an ADR, a new intake, or an in-file amendment
   marker? `CLAUDE.md` §5 rule 3 permits an in-file amendment marker for immutable artifacts
   and ADR-94 scopes the in-place exception to an ADR *status line* only. Which channel R24
   uses is a governance question this doc does not answer.
2. Is the Codespaces free tier available on this account, and is this repo's size compatible
   with 15 GB of storage?
3. What IS the current rate-limit headroom? R28 cannot be specified without it, and the memo
   notes Anthropic does not publish exact token counts.
4. If lanes move off-machine, does the ADR-110 merge-queue discipline still hold — the memory
   that the batch exemption never covers `claude/*` lanes suggests off-machine lanes may need
   their own anchoring rule before they are trusted.

## Cross-links to the four sibling intakes landed in the same arc

- **[#38] `2026-08-17-tech-fleet-config-standardization.md`** — strongest pair, and they
  converge independently. Both name `.devcontainer` + **a pinned-and-asserted uv version**;
  R25 here asserts the pin at container build, #38's R22 asserts it across consumers.
  **One pin definition should serve both**, and #38's `uv.lock`/`uv sync --check` is the
  mechanism R25's assertion would check against.
- **[#36] `2026-08-17-tech-repository-autonomy-and-gate-liveness.md`** — R25's "fail the build
  if hooks aren't armed" IS #36's gate-liveness thesis moved to provisioning time; R26's
  insistence that a skipped check never renders green is #36's dead-detector rule; and R29's
  attestation and #36's R9 bypass-record are one artifact, not two. #36's CI backstop and
  dead-man's-switch both need the compute this doc plans.
- **[#37] `2026-08-17-tech-machine-verifiable-done-when.md`** — the provisioning script is a
  worked example of #37's `kind: command` predicates: assert the uv version, assert history is
  unshallow, assert hooks armed, fail otherwise. #37's METR task-horizon finding (size tasks
  well under the 50% horizon; decompose file-disjoint) is the sizing rule behind R28's lane
  planning.
- **[#35] `2026-08-17-tech-agent-instruction-layers-and-distillation.md`** — same subject
  (unattended runs, concurrency ceilings, substrate economics) researched a second time. **This
  doc's pricing supersedes #35's**, which cites the pre-repricing figures; #35's memo says
  CCX63 rose to €853.49 while this one gives the current CX-line caps and the corrected
  recommendation. Prefer this doc on any price claim.

Directly amends **[#32] `2026-08-09-tech-compute-placement-and-remote-execution.md`
(ACCEPTED)** — see Section C. That amendment is proposed as R24 and is **not performed by this
document.**

## Status

**DRAFT** — landed 2026-08-17 by lane R, unratified. Not operator-approved; the
`docs/intake/README.md` §6 confirm-gate has not been cleared. Zero rows born; six proposed.
Carries the arc's only true supersession (the CCX price basis in [#32]) and one dated external
deadline (Oracle Always Free enforcement, 2026-08-18).
