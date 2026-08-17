> **What was asked:** a verified deployment plan for moving an LLM coding-agent fleet off the Windows laptop -- GPU verdict, substrate comparison with current (August 2026) pricing, VS Code control plane, repo synchronisation, provisioning that defeats the organ-executability traps, and scaling
> **Provenance:** BROWSER-PRODUCED external research, commissioned and landed 2026-08-17 from `compass_artifact_wf-fe444def-3bab-5d58-8077-760875b3cb2b_text_markdown.md`. Body is a BYTE-FAITHFUL copy of the source artifact -- this header is the only addition. Home derived per ADR-101 section 1 Tier-2 (`archive/` is in `SANCTIONED_GENRES`) + ADR-60 (`docs/archive/` = pending-classification holding zone); the ADR-101 Rule B audit-class enum has no class for an external research memo. Derivation recorded in full at `docs/audits/2026-08-17-technical-research-intake-lane-contract.md` section 2.
> **EXTERNAL EVIDENCE -- ADVISORY UNTIL RATIFIED. THIS DOCUMENT BINDS NOTHING.** It is not doctrine, not an ADR, not a ruling, and not this repo's own audit evidence. Nothing here becomes binding by virtue of having landed in the tree. Its ratification channel is the intake spine (`docs/intake/2026-08-17-tech-off-machine-agent-substrate.md`, currently `status: DRAFT`) -- DRAFT -> READY -> ACCEPTED, per `docs/intake/README.md` section 5.

# Off-Machine LLM Coding-Agent Fleet: Verified Deployment Plan (August 2026)

## TL;DR
- **Do NOT buy a GPU.** A coding-agent fleet that calls hosted APIs (Anthropic/OpenAI/Google) is I/O-bound (waiting on token streams, file I/O, git, tests), not GPU- or CPU-bound. A GPU only earns its keep if you run open-weight models locally — which in 2026 still trails frontier models by ~8–9 SWE-bench points and 5–20× on latency, and a usable 48 GB-VRAM box costs more per hour than an entire CPU VPS fleet.
- **Fastest path this week:** Day 1 = a `.devcontainer` proven on the Codespaces free tier (120 core-hours/mo free). Week 1 = one hourly **Hetzner CX53** shared-vCPU instance (16 vCPU / 32 GB / 320 GB NVMe, €29.49/mo cap, ~€0.0473/hr) driven by VS Code Remote Tunnel + tmux, N git worktrees, branch-per-lane pushed to origin. This offloads your Windows laptop with zero change to how you work — an intensive 8-hour batch costs about €0.38.
- **The internal audit was mostly RIGHT on architecture and directionally right on economics, but its Hetzner pricing is now STALE:** Hetzner raised cloud prices twice in 2026 (Apr 1 and Jun 15). The dedicated/shared-AMD lines it leaned toward jumped hardest — CCX rose 2.13×–2.73×, CPX rose 2.44×–2.75× — while the CX/CAX shared lines rose only ~1.3×–1.4×. The hourly÷~624 monthly-cap crossover model it relied on is still correct; the specific per-instance dollar figures are not. **Switch the spec to the CX shared line.**

## Key Findings

**1. GPU is not justified for API-based agents.** The workload is dominated by waiting on remote inference, file I/O, git, and test runs — confirmed by the audit's own measurement (~0.3 sustained cores + 1.5–2 GB RAM per lane) and by independent practitioners: "a single agent is I/O bound... it spends most of its wall-clock time reading files, calling APIs, and waiting on tool output — not burning CPU." A GPU sits idle. GPUs only enter the picture for **local open-weight inference** (Detail Q1).

**2. The three-plane architecture is sound and each plane is independently swappable — CONFIRM.** Control plane (VS Code Remote Tunnel/Remote-SSH), execution plane (one Linux host, N worktrees, N `claude` processes), orchestration (tmux + scripts). This maps cleanly onto verified 2026 tooling.

**3. Anthropic cloud sessions DO foreclose third-party routing — CONFIRM, with new detail.** Claude Code's docs confirm that a `CLAUDE_CODE_USE_*` provider variable, or an `ANTHROPIC_BASE_URL` pointing anywhere other than `api.anthropic.com`, disables Remote Control; cloud/web sessions require talking to the Anthropic API directly, and Remote Control is subscription-only (API keys not supported). Two additional traps surfaced: **teleport is one-way** (web→local only; you cannot push a local session up), and the **VS Code extension cannot attach as a thin client to a live remote background session** — it tries to spawn a local process and `--resume`, which fails when a bg agent already owns the session (GitHub issues #45535 and #60840). This strengthens the audit's conclusion: cloud sessions are a black box for a VS Code-centric, multi-provider operator.

**4. Hetzner pricing is STALE in the audit — the single biggest correction.** Per Northflank's 17 June 2026 breakdown, Hetzner's 2026 increases hit the lines unevenly: **CCX (dedicated vCPU) rose 2.13×–2.73×** in Germany/Finland (CCX13 €15.99→€42.99 = 2.69×; CCX33 €62.49→€138.49 = 2.22×; CCX53 €249.99→€533.49 = 2.13×), and **CPX (shared AMD) rose 2.44×–2.75×** (CPX42 €25.49→€69.49 = 2.73×; CPX52 €36.49→€100.49 = 2.75×). By contrast **CX/CAX (cost-optimized shared) rose only ~1.3×–1.4×.** Current verified caps (DE/FI, ex-VAT): **CX43** (8 vCPU/16 GB/160 GB) €15.99/mo; **CX53** (16 vCPU/32 GB/320 GB) €29.49/mo; CCX33 (8 dedicated/32 GB) €138.49/mo. **Recommendation: use the CX shared line, not CCX** — the audit's "16-lane dedicated spec" is now ~3× more expensive than when it was written.

**5. The hourly→monthly crossover model still holds — CONFIRM.** Hetzner bills hourly (rounded up) capped at the monthly price; per its billing FAQ: "We will bill you for the minimum amount, whether that is the monthly price cap or the hourly price multiplied by the number of hours you used the server." Crossover math for CX53: €0.0473/hr ÷ €29.49 cap ≈ **623 hours** — the audit's ~624h figure survives the repricing. EU locations include 20 TB/mo traffic; extra is charged per TB.

**6. The "organ-executability tax" is real — CONFIRM all three traps.** (a) `uv` honors a `required-version` pin in `pyproject.toml`/`uv.toml` and hard-errors if the running uv doesn't satisfy it; `astral-sh/setup-uv` reads that pin via `version-file`. (b) Shallow clones are the Codespaces/Actions default and break history-dependent checks; `git fetch --unshallow` fixes it. (c) The hook-arming race is a genuine determinism bug and must be closed in provisioning.

## Details

### Q1 — GPU verdict (priced)
**Workload classification: I/O-bound.** Renting a GPU (Lambda, RunPod, Vast.ai, Hetzner GPU) is only justified for **local open-weight inference**. The strongest self-hostable coding model in 2026 is **Qwen3-Coder-Next** (80B total, 3B active MoE, Apache 2.0, 256K context). Per its arXiv technical report it scores **70.6% (SWE-Agent), 71.1% (MiniSWE-Agent), and 71.3% (OpenHands) on SWE-bench Verified** — "Sonnet 4.5-level" per the same report.

- **VRAM class needed for a usable agent:** ~49 GB all-in-VRAM (2×24 GB, or a 96 GB+ Mac) for full speed; an 8 GB GPU + 32 GB RAM with llama.cpp expert-offload works but is "usable-but-not-snappy" (a couple tokens/sec). For a genuinely usable agent at long context, budget a **48 GB-class card**.
- **Current per-hour rental (on-demand, verified ranges):** RTX 6000 Ada (48 GB) ~$0.69–0.80/hr (Lambda); A100 80 GB ~$1.09–1.99/hr; H100 ~$2.19–3.29/hr. Marketplaces (Vast.ai) undercut ~40%.
- **Quality/latency gap:** Independent testing puts the frontier lead at ~8.6 SWE-bench points (Opus ~79.8% vs Qwen ~71.2%), and Qwen averages ~429 s per SWE-bench task vs 22–93 s for proprietary — "acceptable for async workflows and unacceptable for real-time pair programming."

**Verdict:** Not worth it now. A usable GPU box ($0.70–2/hr) costs more per hour than your entire CPU substrate while delivering weaker, slower agents. This flips **only** if (a) a data-sovereignty mandate forbids sending code to hosted APIs, or (b) sustained API/token spend at scale exceeds roughly $500–1,000/mo AND you can tolerate the quality/latency hit — at which point a reserved 48 GB box amortizes.

### Q2 — Fastest path this week (substrate comparison, current prices)

**GitHub Codespaces.** Free tier (confirmed by GitHub Changelog): "GitHub will provide each Free plan account 120 core hours, or 60 hours of run time for a 2 core codespace, plus 15 GB of storage"; **Pro gets 180 core-hours + 20 GB**. Paid overage: **$0.18/core-hour, no monthly cap**; storage $0.07/GB-month. Machines 2/4/8/16/32-core; 8-core (16 GB) and larger often require enabling bigger SKUs and are gated on Pro/Team. Idle timeout default 30 min (configurable 5 min–4 hours). Native devcontainer + VS Code (desktop or browser). Cost at 8-core ($1.44/hr): 40h=$57.60, 80h=$115, 160h=$230, 320h=$461. **Best as the Stage-1 proving ground and burst host; too expensive as an always-on multi-agent host** (no cap; ~4–8× Hetzner for equivalent hours).

**Hetzner Cloud (recommended VPS).** Verified caps (DE/FI, ex-VAT): CX43 8/16 €15.99; **CX53 16/32 €29.49**; CPX42 8/16 €69.49; CCX33 8-dedicated/32 €138.49. Hourly with monthly cap; 20 TB traffic included EU; hourly rate ≈ cap÷624. Cost for CX53 (€0.0473/hr): 40h≈€1.89, 80h≈€3.78, 160h≈€7.57, 320h capped at €29.49. **Best price/performance for the parallel-agent host.** Use CX (shared) — CCX dedicated is now premium-priced after the June increase.

**Other VPS.** Contabo = most RAM/disk per euro (8 GB/100 GB ~€5.50) but SATA SSD and CPU throttling under contention. Vultr/DigitalOcean = 3–5× Hetzner's price for equivalent EU specs but broader regions + managed services. **Oracle Cloud "Always Free" is now a trap:** the ARM Ampere A1 allocation was halved from 4 OCPU/24 GB to **2 OCPU/12 GB** (change took effect June 15, 2026 per InfoQ; entitlement cut from 3,000→1,500 OCPU-hours/mo), and Oracle's email states: "Beginning on August 18, 2026, Oracle will begin enforcing the updated Always Free compute limits. Compute instances that exceed the Always Free entitlement will be automatically terminated." Do not build on it.

**GitHub Actions.** Free minutes: 2,000/mo (Free), 3,000/mo (Pro), private repos. Standard Linux hosted runner $0.006/min; larger runners (Team/Enterprise only, no included minutes) 4-core $0.012, 8-core $0.022, 16-core $0.042/min. **Hard 6-hour job cap** ("If a job reaches this limit, the job is terminated and fails to complete"); 35-day workflow envelope; self-hosted runner job cap 5 days. Self-hosted runners are **free** (a proposed $0.002/min self-hosted charge announced Dec 2025 for Mar 1, 2026 was postponed per secondary reports). **Verdict: unsuitable for persistent multi-hour parallel sessions** on hosted runners — the 6-hour cap disqualifies it; fine only for CI gates or chained sub-6h jobs. Self-hosted runners just recreate the VPS problem.

**Anthropic Claude Code cloud / OpenAI Codex cloud.** Cloud sessions = $0 compute but no VS Code control plane over a running session and (confirmed) forecloses third-party routing. Codex cloud runs tasks in managed containers with a per-session container fee (third-party measured ~$0.03–$1.92 per 20-min session) plus token credits. **Both are complements (fire-and-forget lanes), not the substrate.**

### Q3 — VS Code control plane (verified)
- **Remote Tunnel (`code tunnel`) — recommended.** `curl` the VS Code CLI on the host, run `code tunnel`, authenticate via GitHub, then connect from desktop VS Code (Remote-Tunnels extension) or `vscode.dev` in any browser incl. phone/tablet. No inbound SSH/firewall config. Microsoft states the VS Code Server is single-user and hosting it as a shared service is not permitted — fine for a solo operator.
- **Remote-SSH** — equivalent live experience but requires managing SSH keys/ingress. Both give live terminals and auto-reconnect after laptop sleep/network drop.
- **Seeing N parallel lanes:** neither extension natively renders N live agent panes. The verified pattern is **tmux on the host** (one window/pane per worktree lane), attached from a single VS Code integrated terminal — reconnects cleanly and is phone-monitorable via `vscode.dev`.
- **Claude Code specifics:** Remote Control steers a locally/remotely-running session from phone/web (Pro/Max only, no API keys). But `claude --teleport` is **one-way (web→local)** and the **VS Code extension can't attach to a live remote bg session** (#45535/#60840). So: drive the remote host via Tunnel + tmux; treat Remote Control/teleport as mobile glances, not the control plane.

### Q4 — Keeping remote work synchronized with the local repo
**Correct pipeline: git-native, branch-per-lane, no file-sync tools.** Each lane = one worktree on the host on its own branch, pushed to `origin` continuously. Collect via PRs (or `git fetch` from your Windows checkout). Keep the **Windows checkout as the integration/merge point** by fetching all lane branches and merging locally.
- **Worktree gotcha (verified):** a branch can be checked out in only one worktree at a time — Git blocks a second checkout to prevent index corruption; commits are instantly shared across worktrees (shared object DB) while working files stay isolated. This makes worktrees the correct isolation primitive for parallel agents.
- **Do NOT use Mutagen/Syncthing/rsync/VS Code file-sync** to mirror the whole repo between two machines — they cause `.git` index divergence and race the agents. Let git be the sync layer; only push/pull.
- **Two-machine editing rule:** never edit the same branch on laptop and host simultaneously; the laptop integrates, the host executes.

### Q5 — Provisioning script / devcontainer (defeats the three traps)
Design (reused verbatim on Codespaces AND a plain VPS via the devcontainer CLI):
- **Pin and assert uv.** Put `[tool.uv] required-version = "==0.11.19"` in `pyproject.toml`. In `postCreateCommand`, install uv via the standalone installer with an explicit version env (NOT `uv self update`, which fails when the image ships an older uv), then **assert**: `uv --version | grep -q 0.11.19 || exit 1`. In Actions, use `astral-sh/setup-uv` with `version-file`.
- **Full history.** Codespaces/Actions clone shallow by default → run `git fetch --unshallow` (and `git fetch --tags origin`) in `postCreateCommand` before any history-dependent audit check.
- **Arm hooks deterministically.** Run `pre-commit install --install-hooks && pre-commit install --hook-type pre-push` in `postCreateCommand` and **fail the build if hooks aren't armed** before any agent starts — closing the "gate absent for half a session" race.
- **Features + prebuilds.** Use devcontainer Features for Python/uv/git; enable Codespaces prebuilds for fast first-boot. `hostRequirements` sets cpus/memory/storage. On a VPS, `devcontainer up` runs the identical config in Docker.
- **Fleet-wide checks:** a single-repo container can't discharge a health check expecting sibling repos — clone siblings in provisioning, or gate that check behind a `FLEET=1` env so single-repo lanes skip it cleanly.

### Q6 — Scaling and orchestration (hours→months)
- **Concurrency ceiling.** At ~0.3 sustained cores + 1.5–2 GB per lane: a 16 vCPU/32 GB CX53 comfortably runs ~16 lanes (RAM binds first: 32 GB ÷ 2 GB ≈ 16). For 32 lanes, step to 32 vCPU/64+ GB (CCX53 dedicated €533.49/mo cap, or two CX53s). Beyond ~5 agents, coordination overhead — not hardware — becomes the real bottleneck.
- **Orchestration.** For a solo operator, **tmux + a launch script + git worktrees** is the right tool; native Claude Code subagents (documented ceiling 16 concurrent, `--worktree` flag) or experimental Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, needs tmux/iTerm2) cover most fan-out. Session managers (ccmanager, dmux) add a TUI over the same tmux+worktree substrate. Skip heavyweight platforms.
- **Rate limits bind before hardware.** Claude Code on Pro/Max shares one allowance across claude.ai, Claude Code, and Desktop, governed by a 5-hour rolling window + a weekly cap; Anthropic doubled the 5-hour limits on May 6, 2026 and does not publish exact token counts. Running many parallel lanes on one Max subscription will hit the weekly cap; **API-key billing removes the cap but meters per-token.** Plan lane count around the rate limit, not the CPU.
- **Copilot can offload a lane class cheaply.** Copilot Pro ($10/mo) includes the autonomous "Copilot cloud agent" (opens PRs) and Copilot CLI, plus unlimited completions and a bundled monthly AI-credit allowance. As of June 1, 2026 Copilot moved to usage-based "AI Credits" billing (1 credit = $0.01); Business includes 1,900 credits/user, Enterprise 3,900. The **Free tier does NOT include the cloud agent**, so **$10 Pro is the practical entry point** to offload a bounded volume of async PR-style lanes essentially for free. Note cloud-agent runs also draw GitHub Actions minutes.
- **Snapshot/spin-down discipline.** After a green batch, take a Hetzner snapshot (€0.0143/GB-mo) so a host reboots in minutes; then **delete** the server (Hetzner bills until deletion, not power-off). Hourly billing means an intensive 8-hour CX53 batch costs ~€0.38.

## Recommendations

**Stage 0 — next 2 hours (~€0):** Create `.devcontainer/devcontainer.json` + `provision.sh` implementing the Q5 design (uv pin+assert, `git fetch --unshallow`, deterministic hook arming, fleet-check env gate). Prove ONE lane green on the **Codespaces free tier**. This is the smallest first build and validates the entire "organ-executability" surface for free.

**Stage 1 — this week (~€2–8 for the week):** Spin up ONE **Hetzner CX53** (16 vCPU/32 GB), run `devcontainer up` with the identical script, start `code tunnel`, create N worktrees, one tmux pane per lane, run a real batch at width 8–12. Push branch-per-lane to origin; integrate on your Windows checkout. Snapshot, then delete the server when done.

**Stage 2 — month 1:** Measure wall-clock and failure rate at 16 lanes on CX53. Widen to 32 only if the arithmetic and rate-limit headroom justify it (step to a dedicated CCX53 or a second CX53). Add a $10 Copilot Pro seat to offload async PR-style lanes off your Anthropic allowance.

**Benchmarks that change the plan:**
- Single batch regularly exceeds ~200 wall-clock hours/month on one host → the monthly cap already applies; consider a permanent monthly instance.
- Claude weekly rate-limit blocks you before CPU saturates → move overflow lanes to API-key billing or Copilot/Codex, not to bigger hardware.
- Data-sovereignty mandated or token spend >$500–1,000/mo → re-price a reserved 48 GB GPU box for local Qwen3-Coder-Next.

## Decision Table (scored against the seven requirements)

| Substrate | Off-loads laptop | 16–32 lanes | Fast to deploy | Hourly billing | Hourly→monthly crossover | VS Code control | Clean architecture |
|---|---|---|---|---|---|---|---|
| **Hetzner CX53 (shared)** | ✅ | ✅ (16; 32 needs bigger) | ✅ (~30 min) | ✅ | ✅ (~624h cap) | ✅ Tunnel/SSH | ✅ |
| Hetzner CCX dedicated | ✅ | ✅ 32 | ✅ | ✅ | ✅ | ✅ | ✅ (but pricey post-June) |
| GitHub Codespaces | ✅ | ⚠️ (gated SKUs) | ✅✅ (instant) | ✅ per core-hr | ❌ (no cap) | ✅ native | ✅ |
| GitHub Actions (hosted) | ✅ | ⚠️ | ✅ | ✅ per-min | ❌ | ❌ | ❌ (6h cap) |
| Anthropic cloud sessions | ✅ | ✅ | ✅ | n/a ($0 compute) | n/a | ❌ (no live control) | ❌ (forecloses routing) |
| OpenAI Codex cloud | ✅ | ✅ | ✅ | ⚠️ container fee | n/a | ⚠️ | ⚠️ |
| Oracle Free tier | ✅ | ❌ (2 OCPU/12 GB) | ⚠️ (capacity) | ❌ | n/a | ✅ | ⚠️ |
| GPU box (Lambda etc.) | ✅ | ❌ (overkill) | ⚠️ | ✅ | ❌ | ✅ | ❌ for API agents |

## The smallest first build (next 2 hours)
A `.devcontainer/devcontainer.json` + `provision.sh` that: (1) installs uv at the exact pinned version and **asserts** it; (2) runs `git fetch --unshallow`; (3) runs `pre-commit install` for commit+push hooks and **fails if not armed**; (4) gates the fleet-wide health check behind an env flag; then proves **one lane green (`audit.py health` + `pytest -m "not slow"`) on the Codespaces free tier.** The same file runs unchanged on the Hetzner VPS via `devcontainer up`.

## GPU verdict (one paragraph)
A GPU is **not justified** for this fleet. LLM coding agents that call hosted APIs are I/O-bound — they spend their wall-clock time waiting on remote token streams, reading files, and running tests, leaving a GPU idle; the audit's own ~0.3-cores / 1.5–2 GB per-lane profile confirms this. The only scenario that needs a GPU is running open-weight models locally, and in 2026 the best self-hostable coder (Qwen3-Coder-Next, ~71% SWE-bench Verified) still trails frontier models by ~8–9 points and 5–20× on latency, while a usable 48 GB-VRAM box ($0.70–2/hr) costs more per hour than your entire CPU substrate. Rent CPU, keep calling hosted APIs, and revisit a reserved GPU only if a privacy mandate or sustained >$500–1,000/mo token spend changes the math.

## Caveats
- Individual Copilot per-tier AI-credit dollar amounts (Pro ~$15, Pro+ ~$70, Max ~$200) are from secondary aggregators; GitHub's docs confirm only Business (1,900 credits) and Enterprise (3,900). The self-hosted-runner $0.002/min charge "postponement" is reported by secondary sources, not GitHub docs.
- Hetzner prices are ex-VAT, DE/FI region; US/Singapore differ and traffic allowances shrink outside the EU (Singapore overage ~€7.40/TB vs €1/TB EU/US).
- The audit's baseline measurements (19.0 s health, 507.4 s pytest) are internal and were not independently reproducible online; they are plausible and internally consistent with an I/O-bound profile.
- Claude/OpenAI rate-limit token counts are not officially published; all such figures are third-party estimates.
- GPU rental prices vary hourly by availability; marketplace (Vast.ai) quality is inconsistent.
- Oracle's free-tier enforcement date (Aug 18, 2026) is essentially now — treat that provider as unavailable for this use.