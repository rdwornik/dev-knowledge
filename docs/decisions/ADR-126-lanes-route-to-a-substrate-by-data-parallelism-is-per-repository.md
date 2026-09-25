# ADR-126: Lanes route to a substrate by data; parallelism runs across repositories, capped by measured limits

- **Status:** Proposed
- **Date:** 2026-09-25
- **Decision tier:** Architecture (Path A — the architect's technical proposal under ADR-108 §A, drafted by
  `lane-adr-drafts` on `LANE-5B2-11-adr-drafts.md`, batch WAVE5B-N2 row 11). **Stays Proposed until the operator
  ratifies.** Every purchase and every spending limit is his; the functional questions are in §Operator decision options.
- **Amends:** none. **Builds on** the 2026-08-20 Codespaces ruling (LEAN v2: stay in the free tier, never buy
  overage) and the 2026-09-23 compute-substrate record (a persistent VM executes, Actions runners test), and puts
  both into one routing table with the Anthropic cloud beside them.
- **Related:** ADR-110 (lanes, serial `--no-ff` merge, the lane ceiling), ADR-120 (stage 13 RUN needs a substrate),
  ADR-121 (verdicts with a baseline id), ADR-123 (consumer lanes need the harness in the clone), ADR-106 (uv pin).
- **Provenance:** `PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25` §5 ADR-D and §3.2 ("compute is not the limit,
  integration is"), §2 W4 (quota watch before the first multi-repository night). **Intake:** none — born from a
  batch order.
- **Decommission:** none.
- **Source (in-repo):** `docs/audits/2026-09-23-technical-compute-substrate.md` (§2 laptop, §3 the Codespace
  stalls, §4 comparison, §5 recommendation); `docs/audits/2026-08-20-technical-codespaces-audit.md` (§0, §1.1
  machine menu, §2 pricing, §4 Hetzner CX53, §5.3 timings, §6.5-§6.6 breakeven and the 4-core wall, the
  2026-09-15 AMENDMENT); `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate.md:69` (the cloud container,
  measured); `ecosystem/substrate-registry.yaml` (four substrates; `cloud.admits_gate_dependent_work: false`;
  codespace "2-4 concurrent"); `.devcontainer/devcontainer.json:322-325` (`hostRequirements`, a floor);
  `deploy/conductor-required-checks.ruleset.json` (required checks, `enforcement: disabled`);
  `ecosystem/quality-requirements.yaml` QR-AVAIL-010 (the idle-timeout finding). **Source (transport, in
  addition):** `to-browser/SESSION-lane-research-codespaces-scale.md` (C2: limits, costs, merge queue, Claude
  concurrency — sources dated 2026-09-25); `to-browser/SESSION-lane-legs-cloud.md` §2.1-§2.3 (a cloud clone:
  ambient uv 0.8.17 against the 0.11.19 pin, hooks unarmed, shallow history); `to-cc/PLAN-HARNESS-CONSOLIDATE-DEPLOY-2026-09-25.md` §3.2, §4 P5.

## Context

1. **The target is ~15 lanes a night across 3-4 repositories** (plan §4 P5: ≥ 12 merged across ≥ 3 repositories,
   0 operator inputs, a cost line).
2. **Integration binds before compute.** A local merge took a median 50 min, one lane at a time; 15 lanes in one
   repository would queue ~12 h (plan §3.2). GitHub's merge queue is **not available** on personal-account
   repositories at any plan (C2 §8, first-party page read 2026-09-25); rulesets with required status checks are —
   on public repositories under Free, on private ones from Pro (C2 §8, secondary source).
3. **Every candidate host has a measured or published number, and each has a different wall** (the table below).
   No option is excluded before the matrix.
4. **One ceiling is shared by every host:** Claude Code usage. Cloud sessions "share rate limits with all other
   Claude and Claude Code usage within your account"; no concurrent-session number is published (C2 §9). The only
   public signal is an unverified report of 429s at ~6 concurrent *desktop* sessions.

### The options, with their numbers

| Substrate | Cores / memory | Cost | Concurrency | Quota / wall | Source |
|---|---|---|---|---|---|
| **Local workstation** | 16 logical cores; 27.7 GB RAM, 3-6 GB free (this session's start: 3.17 GB free, 9 seats) | $0 marginal | ≤ 4 heavy lanes (WAVE5B-N2 W5), ≤ 2 by the 2026-09-23 operator cap; memory gate 413 MB/seat | RAM: `-n auto` OOM-killed five suite runs; suite **715 s** | compute §2; codespaces §0 |
| **GitHub Codespaces** | **4-core / 16 GB / 32 GB disk max** on this account (2-core / 8 GB also offered); account-level wall | $0.090 per core-hour flat ($0.36/h at 4-core); storage $0.07/GB-month | undocumented cap; 8 created in one batch without refusal (2026-09-14/15); registry assumes 2-4 | **120 core-h/month (Free) = 30 wall-h at 4-core**; $0 spending limit → exhaustion **blocks**; 37.7 core-h used by 2026-09-15; 15 × 4-core exhausts a month in **2 h**; idle stop max 240 min; suite **147 s** at 4-core | codespaces §1.1, §2, §5, AMENDMENT; C2 §5, §7 |
| **Anthropic cloud (Claude Code on the web)** | **4 vCPU / 15 GB** (measured 2026-08-16) | "no separate compute charge"; draws the subscription's usage | none published; ~6 (desktop, unverified) | the account's shared rate limit; Pro/Max/Team required; **not admitted for gate-dependent work**: no hooks armed, unpinned uv, shallow clone, no operator disk; not-slow suite **507 s** at `-n 4` | nb4-g audit :69; C2 §9; registry; legs-cloud §2 |
| **Persistent VM** (Hetzner CX53 / Azure D16s_v5) | 16 vCPU / 32 GB (CX53); 16 vCPU / 64 GiB (D16s_v5) | CX53 €0.0473/h, **cap €29.49/month** + €0.50 IPv4; D16s_v5 ≈ $0.768/h | N worktrees on one host; ≈ 140 seats of memory headroom at 64 GB (413 MB/seat); ADR-110's lane ceiling governs | none of its own; **never provisioned**; `devcontainer up` never executed; operator owns patching and secrets | codespaces §4; compute §4-§5 |
| **GitHub Actions larger runners** | 16- or 32-core Linux | 16-core $0.042/min, 32-core $0.082/min; needs Team/Enterprise; standard runners on public repos not billed (1,889 min in Sept at $0.00) | per-plan job concurrency | ephemeral per job — no persistent worktree; suite **~8 min** on a 4-vCPU standard runner | compute §4; codespaces AMENDMENT |
| **Serverless sandboxes** (Modal, Daytona) | per-sandbox limits | Modal ≈ $0.14/core-h, Daytona ≈ $0.05/vCPU-h (vendor, unverified) | high (vendor claims) | lifetime limits per sandbox; no git-worktree-native model; a new API surface | compute §4 |

## Decision

- **D1 — Routing is data.** `ecosystem/substrate-registry.yaml` gains capacity fields per substrate (cores,
  memory, concurrency cap, quota source, cost basis, each with `measured_at` and a source) and a routing table keyed
  on lane attributes (`gate_dependent`, `needs_operator_disk`, `read_only`, `heavy_suite`). The launcher reads it
  (WAVE5B-N2 lane 9 makes the launch queue code); no number lives in prose.
- **D2 — Initial routing rules.**
  - read-only research, no gates → **Anthropic cloud** (the P0 research lanes ran there);
  - needs the operator's disk (transport, vendor CLIs) → **local**;
  - gate-dependent build lanes → the **persistent VM** once it exists; until then **local** up to the memory gate and
    **Codespaces** up to the quota headroom (4-core, idle timeout 240 min, W1-proven);
  - the full-suite merge verdict → **CI** (standard runner now; a larger runner only after a plan change), with
    ADR-121's baseline id.
- **D3 — Parallelism is per repository.** One integrator per repository, lanes spread across repositories; each
  repository merges through a CI-gated path — ruleset required checks (the payload exists, disabled) — because a
  merge queue is not available to personal repositories.
- **D4 — Caps are computed at launch from measured limits.** Codespaces: min(registry cap, remaining core-hours ÷
  (4 × expected lane hours)), with remaining core-hours read by the quota watch (WAVE5B-N2 lane 6) before every
  create. Local: the memory admission gate. Cloud: start at 4 and raise only by a measured ramp. VM: seats by memory
  and ADR-110's ceiling. The Claude rate limit caps them all and is read by the same quota watch.
- **D5 — Two measurements before any 15-lane night:** a controlled Codespaces ramp toward 8 concurrent, recording
  where GitHub refuses; and a cloud-session ramp under the quota watch, recording the first 429.

## Quality attributes

- **Quality attribute(s):** Performance (throughput, primary), Availability (unattended nights).
- **Scenario (six parts):**
  - *Source:* the dispatcher.
  - *Stimulus:* a night of ~15 lanes across 3 repositories.
  - *Environment:* routing data current; quota watch live (plan W4); no operator present.
  - *Artifact:* the router and the substrates of D2.
  - *Response:* each lane runs where its attributes route it; none is refused for capacity mid-batch; each
    repository merges its lanes through its CI-gated path.
  - *Response measure:* **≥ 12** lanes merged across **≥ 3** repositories, **0** operator inputs, **0** lanes lost to an
    idle stop or a quota block, a cost line present (plan P5 gate).
- **Decision evidence:** the options table (Context) and the matrix below.

## Decision matrix

**Scope and scoring rule.** Ranks the **host for gate-dependent build lanes** at the P5 target (the other lane
kinds are routed by D2's attributes). Each option is scored 1-5 per criterion (5 best); total = Σ(weight × score),
maximum 500. Scores come from the options table; no option was removed before scoring.

Criteria (weights sum to 100): **E1** throughput per lane on this repository's gates (15) · **E2** parallel
capacity without refusal (20) · **E3** unattended reliability — persistent, no idle stop, no re-provision (20) ·
**E4** gate-dependent work admitted — hooks, pinned uv, full history (15) · **E5** cost and quota headroom at ~15
lanes a night (10) · **E6** set-up and ops burden from today, 5 = in place (10) · **E7** independent of the laptop (10).

| Option | E1 | E2 | E3 | E4 | E5 | E6 | E7 | Total |
|---|---|---|---|---|---|---|---|---|
| Local workstation | 1 | 1 | 3 | 5 | 5 | 5 | 1 | 280 |
| GitHub Codespaces (4-core, Free) | 4 | 2 | 2 | 3 | 1 | 4 | 5 | 285 |
| Anthropic cloud | 3 | 3 | 3 | 1 | 4 | 4 | 5 | 310 |
| **Persistent VM running the repo's devcontainer** | 5 | 5 | 5 | 5 | 4 | 2 | 5 | **460** |
| Actions larger runners as execution host | 5 | 4 | 2 | 4 | 3 | 3 | 5 | 365 |
| Serverless sandboxes | 4 | 5 | 2 | 2 | 4 | 1 | 5 | 330 |

**Reading.** The VM leads by 95 over Actions runners, whose ephemeral jobs cannot hold a lane's worktree (E3) —
they stay the **test host** of D2, not the execution host. Codespaces scores 285 today: fastest per core but capped
at 4 cores, quota-blocked in 2 h at 15-wide, and its E4 is held at 3 until W1 passes 3/3. The Anthropic cloud's 310
is capacity without gates (E4 = 1). **Sensitivity:** the VM's only weak cell is E6 (never provisioned); it keeps the
lead even at E6 = 1. **If the operator buys no VM,** the VM row leaves the table and D2's interim mix stands — local
for disk and gates, Codespaces within quota, the cloud for read-only lanes — with the caps of D4.

## Flip-condition

- **Codespaces rises** if a non-zero spending limit unlocks ≥ 8-core machines (the 2026-08-20 audit §6.6 test) *and*
  the D5 ramp reaches ≥ 8 concurrent without refusal: E1 and E2 then move to 5 and 4 for burst nights.
- **The Anthropic cloud is admitted for gate-dependent lanes** if a cloud setup step arms the hooks, installs uv at
  the pin and fetches full history, *and* the D5 ramp shows ≥ 6 concurrent sessions without a 429: E4 moves to 4.
- **The VM is demoted** if, once provisioned, `devcontainer up` does not reproduce the gate set or the full suite at
  `-n 16` is not under 4 min (the 2026-09-23 record's own exit criterion).
- **Parallelism is capped below the substrates** if the quota watch shows the Claude rate limit binding first — then
  the night's size is set by it, whatever the hosts allow.

## Alternatives considered

- **Local workstation** — gates, disk and no cost, but 3-6 GB free RAM and OOM kills; it cannot carry 15 lanes and
  ties the night to the laptop (plan §1 outcome 1).
- **Codespaces as the parallel host** — proven fastest per core and hub-native; rejected for 15-wide nights by the
  2-hour quota exhaustion, the undocumented concurrency cap and the idle-stop class (QR-AVAIL-010). Kept for proven
  single lanes and short bursts within quota.
- **Anthropic cloud for build lanes** — no compute charge and zero ops, but no gates run there today; kept for
  read-only lanes.
- **Actions larger runners as execution host** — no persistent worktree, and a plan change; kept as the test host.
- **Serverless sandboxes** — capacity on paper, but no git-worktree model and a new API surface to build.
- **A merge queue** — unavailable to personal repositories (C2 §8); a ruleset's required checks are the reachable form.

## Consequences

- The router, not a seat, decides where a lane runs; a number in the registry changes behaviour without an edit to prose.
- The fastest route to 15 lanes costs a purchase (a VM) or a spending limit — both the operator's; without either,
  the night is capped by the laptop's RAM and 30 wall-hours of 4-core Codespaces a month.
- Two ramps (D5) must run before the first large night; both are create/read probes with teardown.
- Per-repository integrators multiply integrator sessions; the Claude rate limit is read, not assumed.

## Operator decision options

These are functional (ADR-108 §A) or purchases; the technical routing above stands as proposed unless he rules otherwise.

1. **Ratify routing-as-data and per-repository parallelism** — Accept · Accept, but one repository at a time until
   the ramps are measured · Return.
2. **A persistent VM** — buy one (Hetzner CX53, ≈ €30/month cap; or Azure D16s_v5, ≈ $0.77/h) · not now (the interim
   mix of D2 stands).
3. **Codespaces spending** — keep the $0 limit and the never-buy-overage ruling (2026-08-20) · set a non-zero limit to
   run the >4-core test (exhaustion then bills instead of blocking).
4. **GitHub plan** — stay Free · Pro (rulesets on private repositories, 180 core-hours) · Team (larger runners).
5. **Night size** — ~15 lanes across 3-4 repositories as planned · a smaller first night (e.g. 6) until D5's ramps are in.
6. **Unattended nights** — allowed on the VM and the cloud · also on Codespaces (idle timeout 240 min) · attended only.
