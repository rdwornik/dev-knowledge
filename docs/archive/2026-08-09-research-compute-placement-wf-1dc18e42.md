# Compute Placement & Remote Execution for a Solo-Operator LLM-Agent Fleet

## TL;DR
- **Fix the laptop first — most of this is a local defect, not a capacity limit.** Your own diagnostics already prove the suite is wait-bound (~14.6% CPU), that ~24% of the worktree slowdown is a fixable rglob defect, and that pytest-xdist already cut the suite from 1785.6s to ~539s. Windows Defender dev-folder exclusions, moving the repo onto the WSL2 native filesystem, Pylance `exclude`/`openFilesOnly`, git `fsmonitor`+`untrackedCache`, and a `.wslconfig` memory/CPU cap will recover most performance for $0. Do Stage 0 before spending a cent.
- **The smallest remote footprint that removes the biggest load is one CLI-provisioned Linux VPS acting as the always-available agent/test host — not a fleet, not a SaaS.** Hetzner (hcloud CLI, true hourly billing) is the best price/performance and CLI-first fit; your existing Hostinger subscription is viable (it has a real `hapi` CLI, an official Terraform provider, and an official MCP server) but bills only on multi-year prepay, so it fits a permanent box, not burst capacity.
- **The toolchain-pinning failure is the gating precondition, not an afterthought.** Any remote executor must reproduce the exact `uv`/hook toolchain from your lockfiles and *fail closed* if a gate did not run. Use `mise.lock` strict/locked mode + `uv sync --locked` + a "gates ran" attestation. What must NOT move remote: the interactive architect seat, the serial merge gate, and any secret that would land in a cloud-synced profile.

---

## Key Findings

1. **Your instrumentation already localizes the problem.** A wait-bound suite (~14.6% CPU), a named rglob defect responsible for ~24% of worktree scaling, four tests each burning a 20s language-server timeout, and an xdist win from 1785.6s→~539s all point to *software defects and I/O waits*, not a CPU-starved machine. Buying compute now would paper over a bug.
2. **The single biggest non-CPU lever on Windows is filesystem placement + Defender.** Files on `/mnt/c` cross the WSL2 9P boundary and run "10x or worse" slower for directory-walking workloads; Defender real-time scanning of dev trees adds measurable overhead — Microsoft's Panos Panay (Windows Developer Blog, June 1, 2023) stated Dev Drive with Defender performance mode "offers up to 30% file system improvement in build times for file I/O scenarios." Both are free to fix.
3. **The worktree model is defensible but over-provisioned.** Ten *full* checkouts multiply Pylance indexing and Defender/file-watch load. Partial clone (`--filter=blob:none`) + sparse-checkout shrinks each lane; but the cheaper win is simply excluding the worktree root from Pylance and Defender and capping concurrent lanes.
4. **CLI-first provisioning is a solved problem across every serious provider except that Hostinger's billing model is awkward.** Hetzner `hcloud`, DigitalOcean `doctl`, Fly.io `flyctl`, and Hostinger `hapi` are all first-class; Terraform/OpenTofu + cloud-init + `ansible-pull` gives fully UI-free, agent-drivable provisioning.
5. **Cloud agent sandboxes (Codex cloud, Copilot coding agent, Claude on the web) are exactly where your toolchain-pinning failure recurs** — they use their own base images and network-isolated sandboxes, and secrets are stripped before the agent phase, so hook-based gates silently break unless you pin explicitly.
6. **GitHub Actions is a legitimate remote executor, and its economics just shifted:** hosted-runner prices dropped up to 39% on Jan 1, 2026 (per GitHub Changelog: "price reductions of up to 39% for GitHub-hosted runners, depending on the machines they use" — e.g., Linux 2-core $0.008→$0.006/min, Linux 64-core arm64 $0.160→$0.098/min); a $0.002/min platform charge for self-hosted runners was announced Dec 16, 2025 and postponed within ~48 hours, with the would-be Mar 1, 2026 start date passing with no charge. Free private-repo minutes remain.

---

## Q1 — Diagnose before buying: how much is a fixable local defect?

**Your own measurements (MEASURED/DOCUMENTED) already answer this more authoritatively than any web source:** the suite runs at ~14.6% CPU (wait-bound, not CPU-bound); the worktree scaling defect (rglob walking the worktree root because the skip-list omits it, while pytest's `norecursedirs` already excludes it) accounts for ~24% of the slowdown; four tests each burn a 20s language-server timeout; xdist already took the suite 1785.6s→~539s. This is a software-shaped problem.

**Standard Windows/WSL2 attribution toolkit (COMMUNITY PRACTICE + vendor docs):**

- **Discriminate wait-bound vs CPU-bound:** Resource Monitor (Disk → "Disk Queue Length" and per-process I/O; CPU tab shows true utilization vs. Task Manager's smoothed number); Process Explorer (per-process I/O bytes, "Delta" columns, thread stacks); **PerfMon counters** — `\Processor(_Total)\% Processor Time` vs `\System\Processor Queue Length` (a queue >~2×cores with low % Processor Time = CPU wait), `\PhysicalDisk(_Total)\Avg. Disk sec/Read` and `\...\Current Disk Queue Length` (disk-bound), `\Memory\Available MBytes` and `\Memory\Pages/sec` (page-cache/memory pressure). **WPR/WPA** (Windows Performance Recorder/Analyzer) for a full ETW trace when you need to see which driver (e.g., `WdFilter.sys` = Defender minifilter) is on the hot path. **Procmon** with a path filter shows Defender/AV scanning events on file writes.
- **Antivirus/Defender:** `Get-MpPreference` to read exclusions, `Add-MpPreference -ExclusionPath`, and `Get-MpComputerStatus`. Microsoft's guidance is to scope exclusions to build/source trees or use **Dev Drive + Defender "performance mode"** (delays scanning until after file ops; Panos Panay's "up to 30% file system improvement in build times for file I/O scenarios"). Community reports consistently describe "builds that felt inconsistent until I excluded the project directory." Microsoft cautions every exclusion is a protection gap — scope them to the repo/worktree/venv trees, not broad folders.
- **WSL2:** `wsl --status`, `free -h` inside the distro, and Task Manager's `vmmem`/`Vmmem.exe` for the VM's aggregate footprint. WSL2 defaults to **50% of host RAM or 8GB, whichever is smaller** (build ≥20175). Cap it in `%UserProfile%\.wslconfig` with `[wsl2] memory=`, `processors=`, `swap=`, and `[experimental] autoMemoryReclaim=gradual`. **The dominant WSL2 pitfall:** code on `/mnt/c` crosses the 9P bridge — "it's not unusual to see 10x or worse slowdowns on the most basic operations like `ls`, `git status`, or any tool that walks a directory tree." Fix = keep the repo on the Linux-native filesystem (`~/…`), not the Windows mount.
- **Git on many worktrees:** `git config core.fsmonitor true`, `core.untrackedCache true`, `core.preloadIndex true`, `feature.manyFiles true` (bundles fsmonitor+untrackedCache+index v4), plus `git commit-graph write --reachable --changed-paths` and `git maintenance start`. GitHub's own data shows fsmonitor+untrackedCache taking `git status` from seconds to ~150ms on large trees. Diagnose with `GIT_TRACE_PERFORMANCE=1` / `GIT_TRACE2_PERF=`. **Caveat (contested):** fsmonitor+untrackedCache can desync some shell prompt status plugins (documented powerlevel10k issue #2473) — verify after enabling.
- **Editor/indexer (Pylance):** the killer in a 10-worktree layout is that each worktree is a separate analyzer root. Set `python.analysis.exclude` to the worktree directory, `python.analysis.diagnosticMode: "openFilesOnly"` (Microsoft: "strongly recommended" for large projects), `python.analysis.indexing: false` or `userFileIndexingLimit`, and open the *subfolder* you're working in rather than the parent. Microsoft's own perf-tuning doc warns that in multi-root workspaces "with many folders (>10–20), the combined memory usage can exceed the Node.js heap limit."

**Realistic recovery before any migration (REPORT SYNTHESIS):** Given your measurements, the fixable-local ceiling is high. The rglob defect alone is ~24% of the worktree penalty and is a one-line skip-list fix. Filesystem relocation off `/mnt/c`, Defender exclusions, Pylance scoping, and git fsmonitor together address the *wait-bound* majority. My assessment: **you can likely recover the "2-hour prompt / machine hanging" pathology entirely with Stage 0**, and only *then* is the residual (eight concurrently-locked agent sessions competing for RAM and the model's own latency) a genuine capacity question worth remote compute.

---

## Q2 — Does the worktree model itself need changing?

**Cost profile per lane (REPORT SYNTHESIS from the sources):**

| Model | Disk/lane | Indexing cost | RAM | Isolation | Notes |
|---|---|---|---|---|---|
| **N full worktrees** (current) | Full corpus ×N (~20.8 MB ×10) — small on disk but ×N *file count* for indexers/AV/watchers | High (N analyzer roots) | High (N Pylance + N agents) | Strong (shared `.git`, separate working trees) | The file-count multiplication, not the megabytes, is what breaks Pylance/Defender/fsmonitor |
| **Partial clone + sparse-checkout** (`--filter=blob:none --sparse`) | Only needed paths + lazily-fetched blobs | Lower (fewer files on disk) | Lower | Same as worktree | Best when lanes touch disjoint subtrees; `git blame`/diffs get slow if blobs must be fetched one-by-one |
| **Containerized workspace per lane** | Full copy inside each container | Isolated per container | Highest (container overhead ×N) | Strongest | What heavier teams do; overkill for a solo op on a laptop |
| **Single checkout, serialized lanes** | 1× | Lowest | Lowest | None (lanes collide) | Defeats the parallel-agent purpose |

**What teams actually do in 2025–2026 (COMMUNITY PRACTICE):** Git worktrees are now the *canonical* pattern for parallel Claude Code / Codex / Gemini lanes. Anthropic ships native support — `claude` started in a worktree, `isolation: worktree` in subagent frontmatter, and the desktop app gives "every new session its own worktree automatically." Tools like `parallel-code` (johannesjo), `FleetCode`, and `spillwavesolutions/parallel-worktrees` orchestrate this. The **documented resource ceiling** is not raw compute but review/merge throughput and stateful-tool collisions: a widely-cited 2026 write-up (Developers Digest) notes "stateful [MCP servers] need one server instance per worktree" and that "fast parallel output shifts the bottleneck from generation to review — one branch at a time." One report describes 200+ subagents across 35 repos in a single session — so the model scales; the *human merge gate* does not.

**Recommendation:** Keep worktrees (they match your one-serial-merge-gate doctrine), but (a) **exclude the worktree root from Pylance and Defender** so N checkouts stop multiplying indexer/AV load, (b) **cap concurrent mutating lanes** to what your serial merge gate can actually absorb, and (c) evaluate `--filter=blob:none` sparse worktrees only if disk or fetch time later becomes the measured bottleneck. Changing the model is *not* your first lever; scoping the indexers is.

---

## Q3 — Workload taxonomy (placement invariants)

**Invariants that decide placement (REPORT SYNTHESIS):**
- The operator's **merge/integration gate must stay where he can see and drive it** (local) — it is the serial choke point by doctrine.
- **Interactive architect work stays local** — latency and context.
- **A bundle/handoff cut binds git state**, so it must run on the *final* tree at the moment of cutting — wherever the authoritative tree lives at that instant (local by default).
- **Anything that must enforce a gate must run in an environment with toolchain parity** (Q6) or it silently fails open.
- **Secrets must never enter a cloud-synced profile** — so any placement requiring long-lived credentials must inject them at runtime, not bake them.

*(Full placement table is in the deliverables section below.)*

---

## Q4 — Remote execution options, priced & compared

### (a) VPS

**Hostinger (your existing asset).** It genuinely satisfies the "no web UI" requirement at the control-plane level:
- **`hapi` CLI** — an official Go binary (`brew install hostinger`, or `go build` from `github.com/hostinger/api-cli`), generated from the OpenAPI spec. `hapi vps virtual-machines list/start/stop`, snapshots, firewall, post-install scripts, public keys, templates; `--format json` for scripting. API token from `hpanel.hostinger.com/api` (that token-generation step is the one unavoidable dashboard touch).
- **Official Terraform provider** (`hostinger/hostinger`) — create/delete VPS, SSH keys, post-install scripts, DNS; in-place updates; import.
- **Official MCP server** — Hostinger explicitly advertises connecting "AI tools like Claude or Cursor" to manage the VPS via the public API.
- **VPS tiers & pricing (as of Aug 9, 2026, from hostinger.com/vps-hosting; VENDOR pricing, changes often):**

| Plan | vCPU | RAM | NVMe | Bandwidth | Promo/mo | Renewal/mo |
|---|---|---|---|---|---|---|
| KVM 1 | 1 | 4 GB | 50 GB | 4 TB | $6.49 | $11.99 |
| KVM 2 | 2 | 8 GB | 100 GB | 8 TB | $8.79 | $14.99 |
| KVM 4 | 4 | 16 GB | 200 GB | 16 TB | $12.99 | $28.99 |
| KVM 8 | 8 | 32 GB | 400 GB | 32 TB | $25.99 | $49.99 |

  **Critical limitation:** Hostinger has **no hourly or monthly billing** — advertised rates require **2-year upfront prepayment**, and renewals are 140–232% higher. This makes it a fine *permanent* always-on box but a poor fit for burst/ephemeral capacity. For N parallel agent lanes + a test suite, **KVM 4 (4 vCPU / 16 GB) is the realistic floor; KVM 8 (8 vCPU / 32 GB) if you run 8 lanes concurrently.**

**Hetzner Cloud (best CLI-first price/performance).** `hcloud` CLI is first-class; **true hourly billing** with a monthly cap (pay ~50% for 15 days). Specs/prices (Hetzner press release; VENDOR, as of Aug 2026):
- CX32: 4 vCPU / 8 GB / 80 GB — €6.80/mo
- CX42: 8 vCPU / 16 GB / 160 GB — "€ 16.40 a month (€ 0.0273 per hour)" (~$18)
- CX52: 16 vCPU / 32 GB / 320 GB — "just € 32.40 per month (€ 0.0540 per hour)" (~$35)
- CPX32 (AMD EPYC): 4 vCPU / 8 GB / 160 GB — €0.0655/hr
- All include 20 TB traffic + 1 IPv4. **This is the strongest CLI-first, spin-up/tear-down fit for bursty agent work.** *(Pricing note: a Hetzner price adjustment is in effect in 2026; sources conflict on the exact date — one review cites April 1, 2026, while Hetzner Docs indicate June 15, 2026 for new orders/rescales. Confirm current rates before committing.)*

**Others (CLI-first quality):** DigitalOcean **`doctl`** — mature, per-second billing (60s/$0.01 minimum), droplets from $4/mo, best-in-class docs; slightly higher $/perf than Hetzner. Fly.io **`flyctl`** — Firecracker micro-VMs, Dockerfile-first, scale-to-zero, excellent for ephemeral/global but per-VM+bandwidth pricing is less predictable. Scaleway (`scw`), OVH (API/Terraform), AWS Lightsail (`aws lightsail`) all have CLIs; Lightsail is predictable but pricier per core than Hetzner. **Verdict: Hetzner for burst, Hostinger for a paid-for permanent box you already own.**

### (b) GitHub Actions as compute

- **Hosted runners:** standard Linux runner is 2-core/7 GB (free-tier includes 2,000–3,000 private-repo minutes/mo depending on plan). **Larger runners** up to 64 vCPU exist. Prices **dropped up to 39% on Jan 1, 2026** (Linux 2-core $0.008→$0.006/min; Linux 64-core arm64 $0.160→$0.098/min). Legitimately usable as a general remote executor via `workflow_dispatch` (manual/API-triggered jobs), not just CI.
- **Self-hosted runners on a VPS:** turns your Hetzner/Hostinger box into an Actions executor. A **$0.002/min platform charge** for self-hosted runners was announced Dec 16, 2025 and **postponed within ~48 hours** ("We're postponing the announced billing change… to take time to re-evaluate our approach"); the would-be Mar 1, 2026 start date passed with no charge. GHES is exempt.
- **Limits:** 6-hour max job (hosted), 35-day workflow cap, concurrency limits by plan, 90-day artifact retention, secrets via encrypted store/OIDC. **Best fit:** the full test suite, the gate mesh, mutation testing — batch, fire-and-forget, PR-triggered work with a natural "gates ran" audit trail.

### (c) Cloud/hosted agent sessions — **this is where your pinning failure lives**

- **Claude Code on the web / cloud sessions:** real in 2026 — assign from phone, `/teleport` to terminal, commits carry a `Claude-Session:` trailer linking back to the session; "self-hosted environments" and Remote Control shipped (per the Aug 2026 changelogs). Works against a private repo. **But** it runs in Anthropic's sandbox with its own environment; your hooks only run if the toolchain is reproduced there.
- **OpenAI Codex cloud:** clones the repo into a **network-isolated sandbox**, runs on a `universal` base image; you *can* "Set package versions" to pin Python/Node and add setup scripts — **but secrets are removed before the agent phase** (available only to setup scripts, per OpenAI's cloud-environments docs), and network isolation blocks lazy toolchain fetches.
- **GitHub Copilot coding agent (incl. Claude/Codex partner agents, public preview):** ephemeral env configured via `.github/workflows/copilot-setup-steps.yml`, with an integrated firewall you can customize/disable. Same ephemeral-image caveat.
- **What the toolchain-pinning problem means for all three:** exactly your prior incident — a pinned `uv` version unavailable in the base image silently disables hook-based gates (fail-open). **These environments are safe only after Q6 parity is enforced.** Until then, treat them for *read-mostly* or *proposal-only* work whose output re-enters through your local gate.

### (d) Google Colab / notebooks — **wrong shape (honest assessment)**

Colab is notebook-centric with an **ephemeral filesystem, session time limits, and no persistent git-worktree/CLI-agent model.** It is a poor fit for a repo-and-git, contract-driven, gate-enforced agent fleet. **The only legitimate niche:** a throwaway GPU/CPU scratchpad for a one-off data experiment or a heavy compute kernel that has *nothing to do with your git state or gates* — and even then a Hetzner box is cleaner. **Do not build fleet workflow on Colab.**

### (e) Dev-container / remote-development

- **VS Code Remote-SSH + devcontainers:** editor stays local, compute/filesystem remote — eliminates the WSL2 9P penalty and the N-analyzer laptop load in one move. Strong fit.
- **GitHub Codespaces:** $0.18/core-hour; personal (Free) accounts get **120 core-hours + 15 GB storage free/month** (GitHub Pro: 180 core-hours + 20 GB); storage $0.07/GB-month **even when stopped** (a default 2-core codespace with 32 GB ≈ $2.24/mo idle storage); prebuilds consume Actions minutes. GitHub-only. Good for spin-up-and-throw-away lanes; costs creep if left running.
- **Coder / code-server (self-hosted), JetBrains Gateway:** run the whole workspace on your VPS and observe locally; more setup, no per-seat SaaS fee.
- **Contested (present honestly):** whether remote dev environments *help solo developers* is genuinely debated — for a one-person shop the operational overhead can exceed the benefit, and community voices note self-hosted runners/dev boxes "come with significant operational overhead." The counter-argument: for *this* operator the laptop is already failing, so offloading the always-on agent host is justified where a generic solo dev's wouldn't be.

---

## Q5 — Provisioning without a UI (the hard requirement)

**State of the art (COMMUNITY PRACTICE + docs):** the canonical UI-free stack is **Terraform/OpenTofu (or the provider CLI) → cloud-init user-data → `ansible-pull` → Docker Compose / mise for the toolchain.** cloud-init handles first-boot truths (users, SSH keys, base packages); a `runcmd: ansible-pull -U <repo> site.yml` line hands off to idempotent Ansible with no central control node. Toolchain pinning inside that via **mise/asdf** (`mise.lock`) and **uv** (`uv python install`, `uv sync --locked`).

**Provider CLI/API maturity:** Hetzner (`hcloud` + Terraform), DigitalOcean (`doctl` + Terraform), Fly (`flyctl`), Hostinger (`hapi` + Terraform + MCP), Scaleway (`scw`), AWS (`aws`/Lightsail) are all fully API-first. **The only providers that effectively force dashboard use are shared/cPanel-style hosts** — not relevant here. **The one unavoidable UI touch** across providers is generating the initial API token (Hostinger's `hpanel.hostinger.com/api`, DO's token page, etc.); after that, everything is CLI/API.

**Can an LLM agent drive provisioning end-to-end?** Yes, increasingly: Hostinger ships an **MCP server** for exactly this; Red Hat ships an **Ansible Automation Platform MCP server** ("AI client → MCP gatekeeper → Ansible executor" with RBAC); Terraform + MCP patterns are emerging. **Security implications (flag):** giving an agent infrastructure credentials means a prompt-injection or a hallucinated `terraform destroy` can delete real servers and incur cost. Mitigations: scope the token to the minimum (a project/VPS-scoped token, not account-root), keep it **out of any cloud-synced profile** (per your doctrine — inject via env at runtime, store in an OS keychain or a `.env` that is git-ignored and profile-excluded), require a human confirm on destructive verbs, and prefer `plan`-then-human-`apply`. **This is the highest-risk item in the whole design.**

---

## Q6 — Toolchain parity & gate integrity remotely (the precondition)

**Root cause of your prior failure (MEASURED/DOCUMENTED, and mirrored by a real public incident):** a pinned tool version unavailable in the container caused a silent fallback that disabled hook-based gates — fail-open. This is not hypothetical: the `EvilBit-Labs/DaemonEye` project documents an almost identical class of failure where mise's pipx backend fell back to plain `pip`, which rejected a `uv`-only flag (`--uploaded-prior-to`) and killed the toolchain setup ("pip rejected the unknown option… exited 1 — failing the whole pipx install"). **The lesson: any fallback in the toolchain path is a silent-gate risk.**

**The correct parity stack (REPORT SYNTHESIS from sources):**
1. **Pin the runtime, not just the deps.** `uv python install <exact>` + commit `uv.lock`; run everything through `uv sync --locked` (or `--frozen`) so drift *fails loudly* instead of re-resolving silently ("switch CI to `uv sync --locked` so drift fails loudly instead of slipping through").
2. **Pin the *tools* with a lockfile that refuses to guess.** `mise.lock` with **`locked = true`** (enable via `mise settings locked=true` or `MISE_LOCKED=1`). Per mise docs, verbatim: "The locked setting enforces that all tools have pre-resolved URLs in the lockfile before installation. This prevents API calls to GitHub, aqua registry, etc., ensuring fully reproducible installations." Generate with `mise lock`; it pins exact versions, checksums, sizes, URLs, provenance.
3. **Kill the pre-commit version-drift gap.** pre-commit pins hook versions independently of `uv.lock`; use **`sync-with-uv`** to make `uv.lock` the single source of truth so local, remote, and CI run identical tool versions.
4. **Build the remote image *from* the lockfiles** (Dockerfile that runs `uv sync --locked` + `mise install` against committed locks), so the executor is bit-for-bit the local toolchain — or, for Codex cloud, pin package versions in the environment settings and verify.
5. **Attestation — refuse a run where a gate did not execute (fail-closed).** The pattern: each gate emits a signed/hashed receipt (e.g., writes a `gates-ran.json` with the hook IDs, tool versions, and a hash of the config it ran under); a final "gate mesh integrity" check *fails the run* if any expected receipt is missing or the tool-version hash doesn't match the lockfile. This inverts the default: instead of "hook absent ⇒ silently pass," you get "receipt absent ⇒ fail." Complement with a server-side **pre-receive hook** (rejects a push whose commits lack the attestation) so the guarantee is a *mechanism*, not an *instruction*. **Note:** pre-commit itself has no built-in "prove all hooks ran" mode and hooks are trivially bypassed with `--no-verify` or `SKIP=`, so the attestation must be enforced at a layer the agent cannot skip (server-side gate / CI required-check).

**Doctrine alignment:** this is "MECHANISMS are guarantees" applied literally — the remote executor is trusted only when it *proves* the gates ran under the pinned toolchain; otherwise it is treated as untrusted and its output re-enters through the local gate.

---

## Q7 — Observing & controlling remote work from chat/laptop/phone

**What people running always-on agent workers actually do in 2026 (COMMUNITY PRACTICE):**
- **Session persistence:** `tmux` (or `screen`) on the remote host so a session survives disconnects; reattach over SSH. **`mosh`** instead of SSH for flaky/mobile links (handles WiFi↔cellular handoff and phone sleep); together "mosh handles the flaky connection, tmux handles session persistence."
- **Private network:** **Tailscale/WireGuard** so the box is never exposed to the public internet — SSH in over the mesh. This also keeps the control plane off open ports.
- **Notifications & intervention:** **ntfy** (self-hosted or ntfy.sh) is the dominant pattern for "agent needs input / job finished" push to phone — tools like `tap-to-tmux` fire on Claude Code `Notification`/`Stop` hook events and deep-link back to the exact tmux pane (Blink Shell x-callback on iOS). `agentoast` does the macOS-menu-bar equivalent and can inject a reply into another agent's prompt by pane id. **Security note:** ntfy topic names are the shared secret — use a long unguessable topic or token auth, and never send sensitive data through a public topic.
- **Long-running jobs:** `systemd` service + `journalctl -f` for a supervised worker; or a background runner that pushes status to a small local dashboard/webhook.
- **Approve/stop/answer from phone:** Claude Code's own cloud/Remote-Control path (assign from phone, teleport to terminal) plus ntfy for the "needs input" ping is the lowest-friction combo; keep Claude in normal (ask-before-dangerous) mode on a non-disposable box.

---

## Q8 — The decision (staged plan)

### Stage 0 — Local fixes, $0 (do this first; expected to resolve the acute pathology)
1. **Fix the rglob defect** (add the worktree dir to the skip-list). Recovers the ~24% documented worktree penalty.
2. **Move the repo + worktrees onto the WSL2 native filesystem** (`~/…`, not `/mnt/c`). Eliminates the 9P "10x-or-worse" directory-walk tax.
3. **Windows Defender exclusions** for the repo/worktree/venv trees (or a **Dev Drive** with performance mode; "up to 30%" build I/O improvement). Verify with `Get-MpPreference`.
4. **Pylance scoping:** `python.analysis.exclude` the worktree root, `diagnosticMode: openFilesOnly`, `indexing: false` (or a `userFileIndexingLimit`). Stops N-analyzer heap blowups. Also fix the four 20s language-server-timeout tests.
5. **Git:** `feature.manyFiles true` (fsmonitor+untrackedCache+index v4), `commit-graph`, `git maintenance start`.
6. **`.wslconfig` caps:** set `memory=`, `processors=`, `autoMemoryReclaim=gradual` so `vmmem` can't starve Windows; size lanes to fit.
7. **Keep the xdist win** (1785.6s→~539s) and cap concurrent mutating lanes to what the serial merge gate absorbs.

**Trigger to proceed to Stage 1:** if, *after* Stage 0, concurrent agent sessions still saturate RAM or wall-clock, the residual is genuine capacity.

### Stage 1 — Smallest remote footprint that removes the biggest load
**Shape:** one CLI-provisioned Linux host acting as the **always-available agent + test executor**, with the laptop kept as the interactive architect seat and the serial merge gate.
- **Provider:** **Hetzner CX42 (8 vCPU / 16 GB, €16.40/mo ≈ $18)** for burst-friendly hourly billing and best price/perf — *or* use your **existing Hostinger KVM 4/8** if you'd rather consume a subscription you already pay for (accepting the 2-year-prepay, always-on model).
- **Provisioning:** Terraform/`hcloud`/`hapi` → cloud-init → `ansible-pull` → Docker image built from `uv.lock` + `mise.lock`. Fully UI-free except the one-time API-token generation.
- **Parity precondition (Q6) enforced before any gate-bearing work runs there.**
- **Control loop (Q7):** Tailscale + tmux + mosh + ntfy; Claude Code cloud/teleport for phone assignment.
- **CI role:** push the full test suite / gate mesh / mutation testing to **GitHub Actions** (free private minutes; PR-triggered; natural attestation surface).

### Monthly cost estimate (recommended shape, as-of Aug 2026; prices change)
- Hetzner CX42 always-on: **~$18/mo** (or ~$9 if you tear down nightly at ~50% cap). Hostinger KVM 4 alternative: **$12.99/mo promo (2-yr prepay) / $28.99 renewal.**
- GitHub Actions: **$0** within free private-repo minutes for the suite/gates.
- Codespaces (optional, ephemeral lanes): within **120 free core-hours/mo**, else $0.18/core-hr + $0.07/GB-mo storage.
- ntfy/Tailscale: **$0** (free tiers / self-host).
- **Total realistic: ~$15–25/mo** for a permanent remote agent/test host plus free CI, or near-$0 incremental if you lean on Hostinger + Actions free tiers.

### What triggers scaling up vs. reverting to local
- **Scale up** (bigger VPS / more lanes) if: post-Stage-0 the *measured* bottleneck is RAM/CPU on the remote box during concurrent lanes, or test wall-clock on the runner exceeds tolerance.
- **Revert to local / shrink** if: the remote box sits idle (Hetzner hourly makes this cheap to abandon), or if operational overhead (parity maintenance, credential hygiene) exceeds the time saved — the honest solo-dev counter-argument.

### What should NOT move remote (and why)
- **Interactive architect work** — latency and context live with the operator.
- **The serial merge/integration gate** — doctrine: the operator is the serial choke point and must see it.
- **The bundle/handoff cut** — it binds git state and must run on the authoritative final tree at cut time.
- **Any secret into a cloud-synced profile** — inject at runtime; never bake.
- **Gate-bearing agent work into a cloud sandbox that lacks toolchain parity** — until Q6 is enforced, those environments fail open (your prior incident).

---

## Deliverable (a) — Workload placement table

| Workload | Placement | Why (invariant) | Parity/secret notes |
|---|---|---|---|
| Interactive architect work | **Local** | Latency, context, operator judgment | — |
| Agent lanes that MUTATE the repo | **Local or Stage-1 VPS** | Must run under enforced gates; feed the serial merge | Requires Q6 parity if remote |
| Read-mostly lanes (audits, research, recon, evidence) | **Remote VPS / cloud agent OK** | No git-state binding; output re-enters via local gate | Lowest-risk remote candidate |
| Full test suite | **CI (GitHub Actions) or VPS** | Batch, parallelizable (xdist), natural attestation | Free private minutes |
| Gate mesh (41 checks, 11.66s) | **CI + local pre-push; server-side pre-receive** | Cheap; must be a *mechanism*, fail-closed | Attestation required |
| Mutation testing | **CI / VPS (off-peak)** | Heavy, batch, non-interactive | — |
| Handoff/bundle generation | **Local (authoritative tree)** | Binds git state at cut time | Never on a stale remote tree |
| Serial merge/integration | **Local, operator-driven** | Doctrine choke point | — |

## Deliverable (b) — Staged plan with costs
Stage 0 (local, **$0**) → Stage 1 (one CLI-provisioned host **~$15–25/mo** + free CI) → scale only on *measured* residual capacity limits. (Full detail above.)

## Deliverable (c) — "Do NOT move remote" list
1. Interactive architect seat.
2. Serial merge/integration gate.
3. Bundle/handoff cut (git-state-binding).
4. Secrets into any cloud-synced profile.
5. Gate-bearing work into any sandbox lacking enforced toolchain parity.

---

## Caveats & source-quality notes
- **MEASURED/DOCUMENTED vs VENDOR vs COMMUNITY:** your internal diagnostics (CPU %, rglob defect, xdist numbers) are the strongest evidence and drive the "fix local first" conclusion. VPS prices, Codespaces/Actions rates, and the "up to 30%"/"up to 39%" figures are **vendor claims** and **change frequently** — all dated as of Aug 2026. Remote-agent tooling (tap-to-tmux, agentoast, parallel-code, mise skills) is **community practice**, not vendor-guaranteed.
- **Contested points flagged in-text:** whether remote dev environments help solo devs; whether self-hosted runners are worth the maintenance; fsmonitor/prompt desync.
- **Conflicting data flagged:** the Hetzner 2026 price-adjustment date (April 1 per a review vs June 15 per Hetzner Docs); Hostinger bandwidth figures (official 4/8/16/32 TB vs some outdated third-party 1/2/4/8 TB) — official page is authoritative.
- **Web-UI touchpoints (your hard constraint):** the only unavoidable one is initial API-token generation on each provider's dashboard; everything else is CLI/API/agent-drivable.
- **Highest-risk design element:** giving an agent infrastructure credentials (Q5) — scope minimally, keep out of synced profiles, require human confirm on destructive ops.
- **The GitHub self-hosted-runner $0.002/min charge is currently postponed** (announced Dec 16, 2025; postponed ~48 hrs later; the Mar 1, 2026 date passed with no charge) — verify status before relying on "free" self-hosted compute.