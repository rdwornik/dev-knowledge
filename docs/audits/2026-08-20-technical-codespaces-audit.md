# Codespaces performance + cost audit — decision memo for the substrate ruling

**Date:** 2026-08-20 · **Mode:** execute, read-only research · **Repo writes:** none · **Artifact:** this file only
**Contract of record:** `C:\Users\1028120\Downloads\TASK-codespaces-audit.md`
**Prior art read first:** `docs/audits/2026-08-19-technical-554-proof.md` (lane J, on `main`)
**Commit under test:** `1def12f6` — identical on the workstation and in the codespace
**Scope:** items 1-5 measured 2026-08-20 AM; **item 6 (the scaling ceiling) added the same day** after the
operator granted the `user` OAuth scope, which also filled in §1.3's quota tables.
**Resource hygiene:** two codespaces created across both passes, **both deleted and verified gone**
(`gh api user/codespaces` → `total_count: 0`). No branch created, pushed or deleted. No repo file changed.

---

## RULING — accepted 2026-08-20

**Status: LEAN v2 ACCEPTED VERBATIM as the ruling.** Architect accepted 2026-08-20. §4.5 is no longer a
recommendation; it is the decision of record, adopted as written and without amendment.

**Explicitly included in the acceptance:**

- **Step 0 — the free ceiling test** (§4.5 step 1; §6.6): set a **non-zero Codespaces spending limit** and
  immediately re-read `repos/rdwornik/dev-knowledge/codespaces/machines`. Setting a limit spends nothing.
  If the menu grows past `standardLinux32gb`, §6.4's projections become measurable and the ruling is
  re-run; if it does not, 4-core is the hard ceiling.
- **The never-meter-buy rule** (§6.5): **never purchase Codespaces overage.** Free-tier exhaustion sits at
  **30 h/month** and cost-parity with the CX53 at **~37 h/month**, so the window in which buying GitHub
  overage is the cheapest option is **seven hours wide**. Stay inside the free tier, or move host.

**Substrate framing, updated by this ruling:** **the commit-tax pain is gone on Codespaces** — the 207 s
tax is `audit.py health`, which runs in ~20 s on a 4-core codespace. The Hetzner CX53's case therefore
rests on **always-on operation and parallel lanes only**, not on making a 146-second suite shorter.
Scaling evidence does not argue for renting cores.

**Named as next-window items, not closed here:**

| Item | Class | Where |
|---|---|---|
| `.devcontainer/devcontainer.json`'s false comment — *"raising it forces a larger (billable) machine type"*; raising `storage` yields **no** machine, not a larger one | **hygiene** | §6.2 |
| **601 of 2 000 Actions minutes (30%) already spent this month** — makes the prebuild trigger *On configuration change* load-bearing rather than merely tidy | **settings** | §1.3, §3.2 |

**Operational decision recorded alongside the ruling:** the `gh` active account **stays `rdwornik`** for
the remainder of fleet work; the operator uses `ghw` when the corporate identity is needed. This settles
the open question §8 previously left to the operator.

**Unchanged by acceptance:** the counterweight in §4.5 stands — `devcontainer up` on a host we control has
still never been executed (lane J's D2 remains BLOCKED), and the ruling deliberately puts that discharge
before any Hetzner spend.

---

## 0 · Verdicts up front

| Item | Verdict | One-line result |
|---|---|---|
| 1 · Entitlement, measured | **CLEAR** | Plan = **GitHub Free** (120 core-h / 15 GB-mo); **1.57 core-hours used in August, 1.3%**, never billed. The machine menu **stops at 4 cores**. |
| 2 · Pricing, primary sources | **CLEAR** | $0.090 **per core-hour, flat at every machine size**; 120 core-hrs + 15 GB-mo free (Free plan) / 180 + 20 (Pro). |
| 3 · Performance levers | **CLEAR** | The contract's premise is **refuted**: `provision.sh` is 13.8 s of a 110 s create. The slow leg is the **85 s container build**. |
| 4 · Head-to-head vs Hetzner CX53 | **CLEAR** | CX53 is ~7× cheaper per hour **and** 4× the cores. Codespaces wins only on ops burden and on being proven. |
| 5 · Measured data point | **CLEAR — and it is the headline** | Same commit, same suite: **local Windows 715 s · Codespaces 2-core 281 s · Codespaces 4-core 147 s.** |
| 6 · The scaling ceiling | **(a) CLEAR · (b) BLOCKED · (c) CLEAR · (d) CLEAR** | The 4-core cap is **account-level**, proven by elimination across 15 repos / 5 regions / both visibilities. `hostRequirements` can only SUBTRACT. Suite scales at **95.7%** through 4 cores; beyond is unmeasurable here. |

**The operator's premise is confirmed and understated.** Codespaces does not merely *feel* faster: on this
repo's own suite a **2-core** cloud container beats the 16-thread workstation by **2.5×**, and the 4-core
beats it by **4.9×** — while `ruff check .` runs **14.7× faster** and `audit.py health` (the dominant leg of
the 207 s commit tax) drops from **206 s to 19 s**.

**Therefore the decision is not "which machine to buy".** The workstation is not losing on core count — it has
16 logical cores against the container's 4. It is losing on per-core throughput for process-spawn- and
filesystem-heavy work, which is what this repo's gates almost entirely are. **Money spent on a bigger machine
buys much less than moving execution off Windows buys — and moving off Windows is already free.**

---

## 1 · Current entitlement, measured — **CLEAR** (quota state filled in after the operator granted `user` scope)

Measured live 2026-08-20 against `rdwornik`, with `GH_TOKEN=$(gh auth token -u rdwornik)` pinned on every
call — the active `gh` account on this workstation is `Robert-Dwornik_ghub`, and lane J §7.3 recorded the
active account flipping mid-session. Pinning is not optional here.

### 1.1 The machine menu — `gh api repos/rdwornik/dev-knowledge/codespaces/machines`

```
name                display_name                        cpus   memory   storage   prebuild_availability
basicLinux32gb      2 cores, 8 GB RAM, 32 GB storage       2    8 GiB    32 GiB    null
standardLinux32gb   4 cores, 16 GB RAM, 32 GB storage      4   16 GiB    32 GiB    null
total_count = 2
```

**This is the single most decision-relevant entitlement fact in the audit: the menu stops at 4 cores.**
GitHub's rate card runs 2 / 4 / 8 / 16 / 32 cores; this account is offered the first two and nothing else.

It is **not** our `devcontainer.json` doing this. `hostRequirements` is a **minimum** per the dev-container
spec — "only machine types that match or exceed the resources you've specified" — so our `cpus: 2,
memory: 8gb` can only hide machines *smaller* than 2-core. The truncation is account-level. GitHub's docs
concede that "the full range of machine types may not always be available" but document no personal-account
cap, so this is reported as **measured, cause undocumented**.

**Consequence for the operator's stated willingness to pay: on Codespaces, money buys HOURS, not SPEED.**
Past the free tier you buy more of the same 4-core box. The 8-core column in §2 is priced for completeness
and is **not purchasable on this account today**.

### 1.2 Other measured entitlement state

| Fact | Value |
|---|---|
| Codespaces existing at session start | **0** (`total_count: 0`) |
| Repo | `rdwornik/dev-knowledge`, **private**, 45.5 MB, default branch `main` |
| Billing owner confirmed at create | `Codespaces usage for this repository is paid for by rdwornik` |
| Default location / config path | `EuropeWest` / `.devcontainer/devcontainer.json` |
| Prebuild configured? | **No** — `prebuild_availability: null` on both machine types |
| GitHub Actions enabled? | **Yes** (`{"enabled":true,"allowed_actions":"all"}`) — the one hard prerequisite for prebuilds is already satisfied |

### 1.3 Plan and quota — **now CLEAR** (scope granted by the operator 2026-08-20, mid-audit)

The `user` OAuth scope was granted on `rdwornik` after the first pass. **Correcting the command this
artifact previously printed:** `gh auth refresh` has **no `-u` / `--user` flag`. It operates on the
*active* account only — its own help says so: *"If you have multiple accounts in `gh auth status` and
want to refresh the credentials for an inactive account, you will have to use `gh auth switch` to that
account first before using this command, and then switch back when you are done."* The working path,
used by the operator, is two commands:

```
gh auth switch --user rdwornik          # rdwornik was NOT the active account
gh auth refresh -h github.com -s user   # refreshes the ACTIVE account's scopes
```

Post-grant scopes on `rdwornik`: `codespace, gist, read:org, repo, user, workflow`.

**PLAN — measured, no longer inferred:**

```
$ gh api user --jq .plan
{"name":"free","collaborators":0,"private_repos":10000,"space":976562499}
```

**The account is GitHub Free.** The included allowance is therefore **120 core-hours + 15 GB-month**.
The Pro column is retained everywhere below as an *upgrade* scenario, not as an unknown.

**QUOTA CONSUMED — current cycle (2026-08), from `users/rdwornik/settings/billing/usage`:**

| SKU | Quantity | Unit | Gross | Discount | **Net billed** |
|---|---|---|---|---|---|
| Codespaces compute 2-core | 0.43267 | Hours | $0.077881 | $0.077881 | **$0.00** |
| Codespaces compute 4-core | 0.17670 | Hours | $0.063612 | $0.063612 | **$0.00** |
| Codespaces storage | 0.00726 | GigabyteHours | $0.000508 | $0.000508 | **$0.00** |

Note the unit: GitHub meters compute in **machine-hours** and prices per machine, while the *allowance*
is denominated in **core-hours**. Converting: `0.43267 × 2 + 0.17670 × 4` = **1.5721 core-hours**.

| | Compute used | of allowance | Remaining | Storage used | Remaining |
|---|---|---|---|---|---|
| **GitHub Free (actual)** | **1.5721 core-h** | **1.31%** | **118.43 core-h** | 0.0000099 GB-mo | ~all 15 GB-mo |
| GitHub Pro (if upgraded) | 1.5721 core-h | 0.87% | 178.43 core-h | 0.0000099 GB-mo | ~all 20 GB-mo |

**Every dollar of it was discounted to zero — the account has never been billed for Codespaces**
(`netAmount > 0` items across the whole usage report: **0**), which is consistent with no payment method
and the default $0 spending limit. That fact becomes load-bearing in §6.

**Two readings that matter, and one that does not:**

1. **The month's entire Codespaces history is lane J plus this audit.** 1.57 core-hours is 1.3% of the
   allowance. There is **no historical usage baseline to extrapolate from** — August 2026 is the first
   month this account has used Codespaces at all. Every profile in §2.4 is therefore a *scenario*, not a
   forecast, and §6.5's threshold rule is what should be applied once a real month has been observed.
2. **Storage is a non-issue, confirmed numerically.** 0.0000099 GB-month against a 15 GB-month allowance
   is six orders of magnitude of headroom. (The reported figure is lower than the ~0.7 GB-hours this
   audit alone should have accrued from a 2.2 GB codespace over ~19 minutes, so the storage line is
   probably lagging. It does not matter: even the un-lagged figure is negligible.)
3. **Actions minutes are NOT a non-issue, and this is new.** The same report shows **601 of 2 000
   included Actions minutes already used in August (30%)**, on `corp-monorepo`. §3 recommends prebuilds;
   prebuilds run on Actions. With the default *"Every push"* trigger they would compete for the 1 399
   minutes left. This is independent confirmation that the *"On configuration change"* trigger is the
   right setting, not merely the tidy one.

---

## 2 · Pricing, from primary sources — **CLEAR**

Sources fetched 2026-08-20: GitHub's billing-concepts page for Codespaces and the Codespaces billing doc.
The `github.com/features/codespaces` marketing page carries **no** rate table — only "free for individual use
up to 60 hours a month … 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage
each month", which is consistent with the doc figures and is quoted here as corroboration, not as the source.

### 2.1 Rates (USD, list)

```
2-core    $0.18 / hr          16-core   $1.44 / hr
4-core    $0.36 / hr          32-core   $2.88 / hr
8-core    $0.72 / hr          storage   $0.07 per GB-month
```

**The rate is exactly linear in cores — $0.090 per core-hour at every size.** This one fact governs §3's
machine-size recommendation, so it is worth stating plainly: **a machine twice as big costs twice as much per
hour and, if the work scales, runs in half the time — for the same money.** §5 measures how well it scales.

### 2.2 Included free each month (personal accounts only — orgs and enterprises get none)

```
GitHub Free    120 core-hours    15 GB-month
GitHub Pro     180 core-hours    20 GB-month
```

Metering, per the docs: compute is billed for the time a codespace is **active**, priced per processor core.
Storage is counted in **GB-hours, cumulative across the billing cycle**, and accrues for as long as the
codespace **exists** — a *stopped* codespace still consumes storage, and deleting one does not claw back
storage already accrued this cycle. With no valid payment method on file, usage is **blocked** once the quota
is spent rather than silently billed.

### 2.3 Free-tier ceiling expressed in wall-clock hours (what the operator actually feels)

```
                2-core        4-core        8-core*
GitHub Free     60 h / mo     30 h / mo     15 h / mo
GitHub Pro      90 h / mo     45 h / mo     22 h / mo
                                            (* not purchasable on this account — §1.1)
```

### 2.4 Monthly COMPUTE cost at the three profiles

Profile = wall-clock hours the codespace is **active**. Core-hours = hours × cores. Overage at $0.090/core-hour.

**GitHub Free — 120 core-hours included** ← **this is the account's actual plan** (§1.3)

| profile | wall-h | 2-core | 4-core | 8-core\* |
|---|---|---|---|---|
| light | 20 | **$0.00** (40 ch) | **$0.00** (80 ch) | $3.60 (160 ch) |
| medium | 60 | **$0.00** (120 ch) | $10.80 (240 ch) | $32.40 (480 ch) |
| heavy | 120 | $10.80 (240 ch) | $32.40 (480 ch) | $75.60 (960 ch) |

**GitHub Pro — 180 core-hours included** (upgrade scenario only)

| profile | wall-h | 2-core | 4-core | 8-core\* |
|---|---|---|---|---|
| light | 20 | **$0.00** (40 ch) | **$0.00** (80 ch) | **$0.00** (160 ch) |
| medium | 60 | **$0.00** (120 ch) | $5.40 (240 ch) | $27.00 (480 ch) |
| heavy | 120 | $5.40 (240 ch) | $27.00 (480 ch) | $70.20 (960 ch) |

\* priced for completeness; **not offered to this account** (§1.1).

### 2.5 Storage — measured, not assumed

The live codespace consumed **2.2 GB** of its 32 GB volume:

```
~/.cache/uv                 156 MB
/workspaces/dev-knowledge   245 MB   (of which .venv 173 MB)
base image + tooling        rest
df /workspaces:  32G total, 2.2G used, 28G avail  (8%)
```

At $0.07/GB-month that is **$0.15/month gross** — inside the 15 GB-month Free allowance by a factor of ~7,
even if a codespace were left in existence for a whole month. **Storage is not a cost lever for this repo.**
The single way it becomes one is prebuilds, and §3 says exactly how to stop that.

### 2.6 What one suite run actually costs

| Machine | Wall time (measured, §5) | Core-hours | Cost at list | Suite runs inside the Free 120 ch |
|---|---|---|---|---|
| 2-core | 281.21 s | 0.156 | $0.0141 | ~768 |
| 4-core | 146.92 s | 0.163 | $0.0147 | ~735 |

**The 4-core run costs ~4.5% more and finishes in 52% of the time.** That is §2.1's flat core-hour rate meeting
§5's near-linear scaling, and it is the cleanest economic result in this audit.

---

## 3 · Performance levers, each with what it buys — **CLEAR**

Every lever below is scored against this run's own `creation.log`, which is the first time the create legs
have been separated:

```
08:38:50.0   create requested (gh codespace create)
08:38:55.0   API returns the codespace name                                    +  5.0 s
08:38:59.3   "Creating container..."
08:40:24.6   devcontainer up finished  (base image + Dockerfile + sshd feature) + 85.4 s   <-- THE SLOW LEG
08:40:25.6   postCreateCommand starts (provision.sh)
   08:40:25.8    L1  install uv 0.11.19                      0.9 s
   08:40:26.7    L2  git fetch --unshallow (5399 commits)    8.6 s
   08:40:35.3        uv sync --locked                        3.2 s
   08:40:38.6    L3  arm 3 git hook types                    0.7 s
   08:40:39.4    C2  gate-liveness smoke + stamp             0.2 s
08:40:39.4   postCreateCommand done                                            + 13.8 s
08:40:39.5   postStartCommand (--gate re-assert)                               +  0.1 s
08:40:40.3   "Finished configuring codespace"                        TOTAL      110.3 s
```

(The API-polled `Available` transition was observed at t+117 s, at ±7 s poll granularity — consistent with
the log's 110.3 s.)

### 3.1 The contract's premise is refuted by measurement

The contract states "our devcontainer provision is the slow leg". **It is not.** `provision.sh` is
**13.8 s of a 110 s create — 12.5%.** The container build (base image pull + our apt-repair `Dockerfile` +
the `sshd` feature) is **85.4 s, or 77%.** Any optimisation aimed at `provision.sh` is chasing 13 seconds and
the four legs it asserts are worth far more than the seconds they cost.

### 3.2 Recommended settings for THIS repo

| Lever | What it buys | Recommend |
|---|---|---|
| **Stop, don't delete** | **117 s cold create → 37 s resume**, measured this run. Container, `.venv` and `~/.cache/uv` all survive a stop/start; only compute metering stops. Costs 2.2 GB-month ≈ $0.15 gross — free under the allowance (§2.5). | **YES, today.** Best win per unit of effort; zero config, zero code. |
| **Prebuilds** | Caches the image+features layer — precisely the 85 s leg. Permitted here: *"You can set up prebuilds in any repository owned by a personal account"*, and Actions is already enabled (§1.2). | **YES — but only with the three narrowing settings below.** |
| ↳ trigger = **"On configuration change"** | Default is **"Every push"**, which would fire an Actions prebuild on every push to `main` — many per day, for a `.devcontainer/` that changes ~never. | **YES.** This is what keeps prebuilds near-free in Actions minutes. |
| ↳ regions = **EuropeWest only**; template history = **1** | Defaults are *all regions* × *2 retained versions* — up to 8 stored prebuild images. Multi-GB × 8 is the one thing that can blow the 15 GB-month allowance §2.5 showed is otherwise slack. | **YES.** This is the only real storage risk in the whole model. |
| ↳ move `provision.sh` to `onCreateCommand` | Prebuilds execute `onCreateCommand` and `updateContentCommand`; **`postCreateCommand` runs only at codespace creation and is never prebuilt.** As configured, a prebuild caches the 85 s and leaves all 13.8 s of provisioning on the create path. | **OPTIONAL.** Worth 13.8 s. Do it only if prebuilds land; the `--gate` re-assert in `postStartCommand` must stay where it is. |
| **Machine size 2 → 4 core** | Measured same-container, same-commit (§5): **1.91× on `pytest -n auto`, 1.57× on `audit.py health`.** With $/core-hour flat, the run costs the same and finishes in half the time. | **YES — always create on `standardLinux32gb`.** Only price: free wall-hours halve, 60 → 30 h/mo. |
| **`uv` cache persistence** | `~/.cache/uv` is 156 MB, already survives stop/start, and `uv sync --locked` costs **3.2 s** even on a cold container. | **NO ACTION.** Already solved; there is nothing here to win. |
| **Idle timeout** | Default **30 min** (range 5–240). Every forgotten codespace burns 30 min × cores — on 4-core that is 2 core-hours, **1.7% of the Free monthly allowance for doing nothing**. | **YES — set 15 min.** `gh codespace create --idle-timeout 15m`, or the account default at github.com/settings/codespaces. |
| **Retention period** | Default **30 days** before an unused stopped codespace auto-deletes — 30 days of storage accrual for something forgotten. | **YES — set 7 days**; `--retention-period 1h` for throwaway probes (this audit used exactly that). |
| **`hostRequirements` in `devcontainer.json`** | It is a *minimum*, so today's `cpus: 2` correctly keeps the cheaper machine in the menu. Raising it to 4 would delete the 2-core option and also raise the floor for `devcontainer up` on a VPS, where the floor is what the clause is for. | **LEAVE AS IS.** Choose 4-core at create time, not in the file. |

### 3.3 The lever the contract did not ask about, and it is the largest one

`ruff check .` — an identical corpus, identical binary, no fleet, no network — runs in **114 ms** in the
container and **1 682 ms** on the workstation. That is **14.7×** on a pure CPU+filesystem workload with no
confound available to explain it away. Combined with §5's 4.9× on pytest, the honest reading is that **the
workstation has a large, general, per-operation tax on file and process work** — the classic candidates being
real-time AV scanning of the repo tree, NTFS small-file overhead, and sustained-clock throttling on a 15–28 W
mobile part.

**This is stated as a hypothesis, not a measurement — this audit did not test it.** But it is cheap to test
and, if true, it is free money that no substrate purchase can substitute for:

1. Add a Microsoft Defender exclusion for `C:\Users\1028120\Documents\Dev\` (and the `uv`/`pip` caches), then
   re-run `uv run --locked python -m ruff check .` and compare against the 1 682 ms baseline in §5.3.
2. Re-run `pytest -m "not slow" -n auto` on a quiet tree and compare against the 715.22 s baseline.

If those two numbers move materially, the substrate question changes shape entirely.

---

## 4 · Head-to-head vs Hetzner CX53 — **CLEAR**

Hetzner figures re-verified from Hetzner's own price-adjustment document (effective **15 June 2026**, all
prices **excl. VAT**). This independently confirms intake #39's numbers, so `[#561]`'s price basis stands:

```
CX53    16 vCPU / 32 GB RAM / 320 GB NVMe / 20 TB traffic
        EUR 0.0473 / hour          EUR 29.49 / month cap      (was 0.0360 / 22.49 before 15 Jun 2026)
        primary IPv4               EUR 0.50 / month
        hourly-to-cap crossover    623 h   ( = 29.49 / 0.0473 )
```

**Provenance, split honestly.** The **prices** above are from Hetzner's own price-adjustment document
and are first-party. The **hardware spec** (16 vCPU / 32 GB / 320 GB NVMe / 20 TB) is corroborated by three
consistent secondary sources — intake #39, Hetzner's CX-plans press release for the CX52 predecessor at the
identical spec, and search-surfaced Hetzner product copy — but **not** by a directly fetched Hetzner spec
page: those render their tables in JavaScript and return placeholders to a fetcher. Confirm the spec in the
Hetzner console before provisioning.

### 4.1 Monthly cost at the three profiles

| profile | wall-h | Codespaces 4-core, Free plan | Codespaces 4-core, Pro | Hetzner CX53 (+IPv4) |
|---|---|---|---|---|
| light | 20 | $0.00 | $0.00 | €0.95 + €0.50 = **€1.45** |
| medium | 60 | $10.80 | $5.40 | €2.84 + €0.50 = **€3.34** |
| heavy | 120 | $32.40 | $27.00 | €5.68 + €0.50 = **€6.18** |
| always-on | 730 | $252.00 — and **not purchasable as one box** | $246.60 | €29.49 + €0.50 = **€29.99** |

Currencies are deliberately **not** converted: GitHub bills USD, Hetzner bills EUR excl. VAT, and at every row
above the ordering is unambiguous without a rate. At light usage Codespaces is free and Hetzner is not; from
medium usage upward Hetzner is cheaper by a widening margin; at always-on the comparison stops being about
price and starts being about what is even available.

### 4.2 Ops burden

| | Codespaces | Hetzner CX53 |
|---|---|---|
| Provision | **Zero.** `gh codespace create`, 110 s, proven twice (lane J 2026-08-19; this audit 2026-08-20) | Build the host: OS, users, docker, tunnel, firewall. **Never yet exercised** — lane J's D2 is still BLOCKED (no container runtime on the workstation, no WSL distro, no admin rights) |
| Maintain | **Zero.** GitHub patches the host | Operator owns kernel/docker/security patching, disk, backups |
| Reach it | `gh codespace ssh` — needs this workstation's `~/.ssh/config` BOM worked around (§7) | VS Code Remote Tunnel + tmux, per intake #39 |
| Secrets / auth | Inherits the GitHub identity | Planted and rotated by hand |
| Witnessed failure mode | Silent **RECOVERY-container swap** (lane J §1.3) — looks `Available`, is not provisioned, says nothing | Unknown, unmeasured |
| Concurrency | Each lane is its own billed machine | N git worktrees on one flat-rate host |

### 4.3 What Hetzner gives that Codespaces cannot

1. **A genuinely bigger machine.** 16 vCPU / 32 GB — **4× the largest box this account can buy at any price**
   (§1.1). This is the literal answer to "willing to pay for a better machine": on Codespaces there is nothing
   better to pay for.
2. **Always-on with no hour metering.** A flat €29.99/mo covers all 730 h. The same wall time on Codespaces
   4-core is ~$252 and cannot be bought as a single machine.
3. **N concurrent lanes on one host** — intake #39's stage-2 model. Codespaces bills every parallel lane its
   own machine against the same core-hour pool, so parallel execution is where Codespaces cost goes non-linear.
4. **Persistent state with no retention clock**, and no 32 GB volume ceiling.

### 4.4 What Codespaces gives that Hetzner does not

1. It is the **only one of the two that has actually run this repo's gates**, now twice, and this audit
   reproduced lane J's result on a different branch and a different machine size.
2. **$0 at light usage**, and ~735 full suite runs a month inside the free tier (§2.6).
3. **No ops surface at all** — nothing to patch, nothing to secure, nothing to forget.
4. It fails *loudly enough to catch*: the one silent failure shape found (the recovery container) is now
   walled by lane J's `Dockerfile` repair, which this run confirms holds on `main`.

### 4.5 LEAN — **ACCEPTED VERBATIM AS THE RULING, 2026-08-20**

**This section was a recommendation when written; the architect accepted it verbatim on 2026-08-20 and it
is now the decision of record.** See the RULING block at the top of this artifact for what the acceptance
explicitly covers. The wording below is left exactly as it was ruled on — not rewritten after the fact.
*(Revised after §6. The shape did not move; the thresholds are now measured rather than assumed, and one
free step was added at the front.)*

**Do not buy a bigger Codespace — there isn't one, and the wall is account-level (§6.6). Take the free
4-core, tune it, and key the Hetzner move to a measured hours threshold rather than to a feeling.**

Concretely, and in this order:

1. **Test the ceiling for free, first.** Add a payment method and set a **non-zero** Codespaces spending
   limit, then immediately re-run `gh api repos/rdwornik/dev-knowledge/codespaces/machines`. Setting a
   limit spends nothing by itself, and it is the only untested hypothesis for why the menu stops at 4
   cores (§6.6). **If the list grows, every projection in §6.4 becomes measurable and this LEAN should be
   re-run.** If it does not, 4-core is the hard ceiling and steps 2–5 stand as written.
2. **Immediately, at €0:** always create on `standardLinux32gb` (4-core); set the account idle timeout to
   15 min and retention to 7 days; **stop rather than delete** between sessions (117 s → 37 s). This is a
   ~4.9× speedup over the workstation on the suite and takes the 207 s commit tax to **~20 s** — for no
   money and no ops. Keep `-n auto`: §6.4 measured it as the optimum, with `-n 8` on 4 cores **10.1%
   slower**.
3. **Within the free tier, cheaply:** enable prebuilds with trigger *On configuration change*, regions
   *EuropeWest only*, template history *1*. That attacks the 85 s container-build leg — the only genuinely
   slow one left. **The narrow trigger is now load-bearing, not fastidious:** §1.3 shows **601 of 2 000
   included Actions minutes already spent this month (30%)**, and the default *Every push* trigger would
   compete for the remaining 1 399.
4. **Measure one real month of wall-clock hours.** The account has used **1.57 core-hours ever** — August
   2026 is its first month on Codespaces at all (§1.3) — so there is still no usage baseline, only a
   floor. This remains the single missing input.
5. **Trigger for stage 2 — Hetzner CX53 — is any ONE of:**
   - measured monthly active hours exceed **30 h** (the Free-plan 4-core exhaustion point, `F/c`, now
     confirmed against the actual plan), *or*
   - a workload needs **more than 4 cores** — Codespaces cannot supply it at any price (§6.3), *or*
   - **two or more lanes routinely run in parallel**, where Codespaces cost goes non-linear per lane and
     the CX53's flat cap does not.

**One rule §6.5 adds, and it is sharp: never pay GitHub for Codespaces overage.** Cost-parity with the
CX53 sits at **~37 h/month** against free-tier exhaustion at **30 h/month**. The window in which buying
GitHub overage is the cheapest option is **seven hours wide**, and above it the CX53 is both cheaper *and*
four times the machine. Practically: stay inside the free tier, or move host — do not meter-buy.

**What §6 did NOT change, and it is worth saying plainly.** The scaling evidence does **not** strengthen
the case for renting more cores. The suite scales at 95.7% through the only doubling measurable, so bigger
hardware would convert — but at 4 cores the suite already runs in **146 s** and the commit tax in
**20 s**, so the operator's actual pain is gone. **The CX53's case rests on always-on operation, unmetered
hours, N parallel lanes and 4× RAM — not on making a 146-second suite shorter**, and §6.4 explicitly
declines to promise it would.

**The honest counterweight, stated rather than buried:** the Hetzner path's central clause — the *identical*
`devcontainer.json` + `provision.sh` running via `devcontainer up` on a host we control — **has still never
been executed.** Lane J's D2 is BLOCKED and this audit did not unblock it. Codespaces' `@devcontainers/cli
0.83.3` consuming the same two files is strong evidence and is not the same thing as proof. Ruling for
Hetzner before D2 is discharged buys a machine on an untested assumption; the LEAN above deliberately puts
that discharge before the money.
---

## 5 · The measured data point — **CLEAR**

One codespace, `cs-audit-2026-08-20-4gvp5j96775cv6g`, created from **`main` @ `1def12f6`** on
`standardLinux32gb`, then **resized in place to `basicLinux32gb`** so the 2-core and 4-core numbers come from
the *same container, same commit, same corpus* — which lane J's cross-day figure could not. Deleted at the end.

**Host:** `codespaces-7c783b`, AMD **EPYC 7763** 64-Core, Debian 12 (bookworm), 32 GB volume.
**Workstation comparator:** AMD **Ryzen 7 PRO 7840U**, 8 cores / **16 logical**, 27.7 GB RAM, Windows 11,
same commit, clean tree, **0 stray python processes**, 2 worktrees registered.

### 5.1 The three numbers

| Workload | Local Windows (16 threads) | Codespaces 2-core | Codespaces 4-core |
|---|---|---|---|
| `pytest -m "not slow" -n auto` | **715.22 s** (11 m 55 s) | **281.21 s** (4 m 41 s) | **146.92 s** (2 m 27 s) |
| `scripts/audit.py health` | **205.9 s / 222.5 s** (2 runs) | **29.6 s** | **18.8 s / 19.0 s** (warm) |
| `ruff check .` | **1 682 ms** | — | **114 ms** |

**Ratios:**

```
pytest    local -> 2-core    2.54x faster
          local -> 4-core    4.87x faster
          2-core -> 4-core   1.91x   (95.7% scaling efficiency on 2x cores)
health    2-core -> 4-core   1.57x
          local -> 4-core   ~11.3x   (CONFOUNDED — see 5.4)
ruff      local -> 4-core   14.75x   (clean: identical corpus, no fleet, no network)
```

### 5.2 Against lane J's baseline and the 207 s hook figure

| | Lane J, 2026-08-19 | This audit, 2026-08-20 |
|---|---|---|
| Machine | `basicLinux32gb` (2-core) | 4-core, then same container at 2-core |
| Source branch | probe branch `chore/554-sshd-probe` | **`main`** |
| Create → Available | ~125 s | **117 s** (log-derived total 110.3 s) |
| `audit.py health` | 14 s | **29.6 s** (2-core) / **18.8 s** (4-core) |
| `pytest -m "not slow"` | **273.80 s** on 2 cores | **281.21 s** on 2 cores / **146.92 s** on 4 cores |
| Suite counts | 8 failed / 3008 passed / 9 skipped / 1 xfailed | 10 failed / **3079 passed** / 9 skipped / 1 xfailed |
| `audit.py health` FAILs | **2** | **1** |

The 2-core pytest figures agree to within 2.7% across two different days and two different branches, against
a corpus that grew by ~2.4% — that is a **replication**, and it is the strongest single validation in this
audit that the substrate behaves reproducibly.

**The 207 s commit-tax figure resolves almost entirely to one check.** The workstation runs `audit.py health`
in **205.9 s**, and `audit-health` is a pre-commit gate. The commit tax and the health check are, to within
measurement noise, the **same number**. In a 4-core codespace that check is **18.8 s**. Read plainly:
**the commit tax the operator feels most is a ~19 s operation being run on the wrong machine.**

### 5.3 Create, resume and teardown timings

| Event | Measured |
|---|---|
| `gh codespace create` → API returns name | **5 s** |
| Create → `Available` (4-core, polled) | **117 s** (±7 s poll granularity; log total 110.3 s) |
| ↳ of which container build | **85.4 s** |
| ↳ of which `provision.sh` | **13.8 s** |
| ↳ of which `--gate` re-assert on start | **0.13 s** |
| Stop → `Shutdown` | **51 s** |
| **Resume (stopped) → interactive shell** | **37 s** |
| Delete → absent from account | immediate; verified `total_count: 0` |

### 5.4 Honest limits on these numbers

1. **The `health` local-vs-container ratio is confounded and must not be quoted as 11×.** The workstation has
   the sibling fleet repos present and passes `repos registered`; the container has one repo and FAILs it,
   which skips fleet-wide work. Self-audit check counts differ slightly too (local 40/78, container 38/79).
   The **pytest** and **ruff** ratios have no such confound and are the ones to rely on.
2. **The workstation had 2 worktrees registered**, not zero. Five tests `rglob` the repo root and read every
   markdown file in every worktree, so the 715.22 s figure carries a small unquantified inflation. It is a
   *real* number for the machine as it actually is, but it is not the theoretical floor.
3. Poll granularity on `Available` was ~7 s; the `creation.log` total (110.3 s) is the precise figure.
4. Each timing is one run except `health` (2 runs local, 3 in-container) — the variance seen there was <8%.
5. The 2-core pytest run followed a machine resize, so its page cache was cold where the 4-core run's was
   warm. That biases **against** the 4-core machine, so the 1.91× scaling figure is, if anything, conservative.

### 5.5 Suite failures — what reproduced, and what did not

Codespaces (both sizes, identical counts): **10 failed / 3079 passed / 9 skipped / 1 xfailed**.
Workstation, same commit: **2 failed / 3093 passed / 3 skipped / 1 xfailed**.

| Failure | Local | Codespaces | Reading |
|---|---|---|---|
| `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row` | FAIL | FAIL | **Pre-existing**, both platforms — the stale `1 → 3` pin lane J §4.2 already reported |
| `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | FAIL | FAIL | **Pre-existing**, both platforms — not a substrate finding |
| `test_reverse_dep_oracle.py::test_extract_dependents_excludes_declaration` | pass | FAIL | **Genuine Linux-only defect — REPRODUCED.** The URI→path converter eats `/w` as a drive letter (lane J §4.3) |
| `test_merge_serialization.py::test_index_lock_blocks_concurrent_merge` | pass | FAIL | **Genuine Linux-only defect — REPRODUCED.** Test pins Windows git's error wording (lane J §4.3) |
| `test_boundary_report`, `test_audit_parallel`, `test_audit::test_health_stays_ok_with_na_status`, `test_telemetry_wiring` ×3 | pass | FAIL | **Container-shape** — all six reach `cmd_health`, which is DEGRADED because a container holds one repo and no fleet |

**Both of lane J's Linux-only defects reproduced independently on a different branch and a different machine
size.** They are real, they are still open, and no Windows-only run can ever see them.

### 5.6 A finding lane J's clone shape hid

Lane J §3 reported **2** `health` FAILs and five clone-shape test failures, attributing them to a codespace
cloning "only the branch it was created from" — no local `main`, so `journal_spine_anchor` could not resolve
its floor and `test_validate_branch_naming` asserted `'main' in ['chore/554-sshd-probe']`.

Creating from **`main`** instead, this run measured:

```
$ git rev-parse --is-shallow-repository   ->  false
$ git rev-list --count HEAD               ->  5399
$ git branch -a
  * main
    remotes/origin/HEAD -> origin/main
    remotes/origin/automation/fleet-audit
    remotes/origin/main
```

**Every remote branch is present and `main` exists locally.** `journal_spine_anchor` passes,
`test_validate_branch_naming` passes, and `audit.py health` drops to **exactly one** `[!!]`:

```
[!!] repos registered  (none)
self-audit (.dev-knowledge) - 38/79 pass
```

So a meaningful share of lane J's §3 failure class was an artifact of **creating from a non-default branch**,
not a property of the substrate. **The remaining blocker for `[#554]`'s D1a Done-when is one check —
`repos registered (none)` — and it is structural**: a container holds one repo and the hub's check expects the
sibling fleet. That is a genuine design choice for the row's owner (lane J's options (a)/(b)/(c)), and it is
now the *only* one standing between this substrate and a green D1a. **This audit does not dispose of it.**

### 5.7 Cost of this measurement

**First pass (items 1-5):** ~18 minutes of active time (≈10.5 min at 4-core, ≈7 min at 2-core)
≈ **0.9 core-hours ≈ $0.08** at list rates. GitHub's own usage report subsequently confirmed this almost
exactly — 0.1767 machine-hours at 4-core is 10.6 min (§1.3).

**Second pass (§6's scaling sweep):** ~24 minutes on a 4-core machine ≈ **1.6 core-hours ≈ $0.14**.

**Whole audit ≈ 2.5 core-hours ≈ $0.22 at list — about 2% of the monthly Free allowance, and $0.00
actually billed.** Storage accrual is negligible in both passes. The `premiumLinux` / `largePremiumLinux`
probes in §6.3 created nothing and therefore cost nothing.

(GitHub's usage report lags: at the time of writing it still showed only the first pass. The second
pass's ~0.55 machine-hours will appear against `Codespaces compute 4-core` later, so §1.3's
**1.5721 core-hours** is a lower bound for the month — the true figure is ~3.2, still under 3%.)

---

## 6 · THE SCALING CEILING — why the menu stops at 4-core, and where scaling stops

### 6.1 (a) WHY the menu stops — five candidate causes, four eliminated by measurement

GitHub documents exactly three reasons a machine type may be unavailable (*Changing the machine type for
your codespace*): **"the full range of machine types may not always be available"**, **"a policy
configured for your organization"**, and **"a minimum machine type specification for your repository"**.
Each was tested, plus region and repository visibility. **Zero writes to `rdwornik/dev-knowledge` were
made for any of it.**

| Candidate cause | Test run | Result | Verdict |
|---|---|---|---|
| **Organization policy** | `gh api user/orgs` | `0` — the account belongs to no organization | **ELIMINATED** |
| **Region / location** | `codespaces/machines?location=` for `EastUs`, `WestUs2`, `SouthEastAsia`, `WestEurope`, `EuropeWest` | Identical 2-machine list in all five | **ELIMINATED** |
| **Repository visibility** | private `dev-knowledge` vs public `ai-council` | Identical 2-machine list | **ELIMINATED** |
| **Our own `hostRequirements`** | `corp-monorepo` and `ai-council`, both of which have **no `.devcontainer` at all** (`contents/.devcontainer` → 404) | Identical 2-machine list | **ELIMINATED** — a repo with no minimum spec hits the same ceiling |
| **Residual: account-level entitlement** | 14 third-party public repos swept | **Not one surfaces a machine above 4 cores or above 32 GB storage** | **THE CAUSE, by elimination** |

The third-party sweep is the strongest single piece of evidence, because the machine list follows the
**viewer's** account rather than the repository:

```
microsoft/TypeScript    basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
rust-lang/rust          basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
golang/go               basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
kubernetes/kubernetes   basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
facebook/react          basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
flutter/flutter         basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
apache/spark            basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
elastic/elasticsearch   basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
tensorflow/tensorflow   basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
pytorch/pytorch         basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
nodejs/node             basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
llvm/llvm-project       basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
godotengine/godot       basicLinux32gb(2c/32GB) standardLinux32gb(4c/32GB)
dotnet/runtime          (EMPTY — see 6.2, and it is the decisive case)
```

### 6.2 (a) The `hostRequirements` experiment — already run, on someone else's repo

The contract asked whether a `hostRequirements` block requesting 8 cores would change the menu. **It does
not need to be tried on our repo, because a public repo already runs exactly that experiment and the
answer is visible through this account's own token.**

`dotnet/runtime` declares:

```json
"hostRequirements": { "cpus": 4, "memory": "8gb", "storage": "64gb" }
```

and this account's machine list for it is:

```
$ gh api repos/dotnet/runtime/codespaces/machines
{"machines":[],"total_count":0}
```

**Empty.** The `storage: "64gb"` floor excludes both 32 GB machines, and the premium machines that *do*
carry 64 GB+ storage (`premiumLinux` and above) are **not substituted in — they are simply not visible to
this account.** GitHub's docs agree on the mechanism — *"you will only be able to select machine types
that match or exceed the resources you've specified"* — and concede the list can end up with *"no
available machine types for people to choose"*, which is precisely the state measured here. What the docs
do **not** describe is the resulting user experience; this measurement supplies it.

The positive control confirms the filter is live on this very token, and that it only ever subtracts:

```
github/docs       hostRequirements {cpus: "4", memory: "16gb"}  ->  standardLinux32gb ONLY
                  (the 4-core floor removed basicLinux32gb; nothing above 4-core appeared)
microsoft/vscode  hostRequirements {memory: "9gb"}              ->  standardLinux32gb ONLY
                  (the 9 GB floor removed the 8 GB machine)
```

**Conclusion, as strong as the evidence allows: `hostRequirements` can only SUBTRACT from the menu.
Raising ours to `cpus: 8` — or to `storage: "64gb"` — would not surface an 8-core machine. It would empty
our menu and make codespace creation impossible.**

**In-repo doc drift found in passing (reported, not fixed — this audit writes nothing).**
`.devcontainer/devcontainer.json` carries the comment:

> *"Storage is deliberately NOT declared: raising it forces a larger (billable) machine type, and stage 1
> is a €0 build."*

The instinct is right and the file is correct as written, but the stated *reason* is false for this
account: raising storage would force **no** machine at all, not a larger one. Worth a one-line correction
whenever `[#554]` is next touched.

### 6.3 (b) Measuring a >4-core machine — **BLOCKED, and the wall is hard**

No machine above 4 cores is creatable, through either door. Both refusals, verbatim:

```
$ gh codespace create -R rdwornik/dev-knowledge -b main -m premiumLinux
  ✓ Codespaces usage for this repository is paid for by rdwornik
error getting machine type: there is no such machine for the repository: premiumLinux
Available machines: [basicLinux32gb standardLinux32gb]
```

```
$ gh api -X POST repos/rdwornik/dev-knowledge/codespaces -f ref=main -f machine=premiumLinux
{"message":"Machine 'premiumLinux' is not available, Machine 'premiumLinux' is not allowed for this
 repository","documentation_url":"https://docs.github.com/rest/codespaces/codespaces#create-a-codespace-in-a-repository",
 "status":"400"}
```

`largePremiumLinux` (16-core) is refused identically. **No codespace was created by either probe**
(`gh api user/codespaces` → `total_count: 0` immediately afterwards), so hitting the wall costs nothing.

Since 6(c) needs a scaling curve and no bigger machine exists to measure, the curve was obtained a
different way — 6.4.

### 6.4 (c) WHERE SCALING STOPS — the flat-rate rule, then the measured curve

**The rule first, because it is the part that generalises.** Codespaces charges a flat **$0.090 per
core-hour at every machine size** (§2.1). The cost of one run is therefore just its **core-seconds**:

```
cost(run on c cores) = T(c) · c · p                       [ p = $0.090 per core-hour ]

           cost(c)          T(c) · c              1
        ─────────────  =  ─────────────  =  ───────────    where E(c) is parallel efficiency
        cost(c_ref)       T(cref)·cref         E(c)                    measured against c_ref
```

**The cost premium for buying a bigger machine is therefore exactly `1/E − 1`, and the wall-time gain is
`E · (c/c_ref)`.** Under perfect scaling, machine size would be *free*. This is the rule the whole
substrate decision turns on, and it reframes the operator's question: **on Codespaces you do not buy
speed with money, you buy it with efficiency — and you pay only for the efficiency you lose.**

**Then the measurement.** Because no machine above 4 cores is buyable (6.3), the curve was obtained by
sweeping **xdist worker count on one fixed 4-core machine** and cross-checking it against the two true
**machine** sizes already measured. That turned out to matter enormously: the two axes do *not* behave
the same way, and conflating them would have produced a badly wrong projection.

**Axis A — workers varied, cores fixed at 4** (same container, same commit, warm cache, one discarded
warm-up run first; every run produced identical counts: 10 failed / 3079 passed / 9 skipped / 1 xfailed):

| `-n` | Wall time | vs previous | vs `-n 1` |
|---|---|---|---|
| 1 | **307.60 s** | — | 1.00× |
| 2 | **163.02 s** | **1.887×** | 1.887× |
| 4 (`= -n auto`) | **145.38 s** | **1.121×** | 2.116× |
| 8 (oversubscribed 2:1) | **160.10 s** | **0.908× — 10.1% SLOWER** | 1.921× |

**Axis B — cores varied, workers fixed at 2:**

| Machine | `-n` | Wall time | Speedup from cores alone |
|---|---|---|---|
| `basicLinux32gb` (2 cores) | 2 | 281.21 s | — |
| `standardLinux32gb` (4 cores) | 2 | **163.02 s** | **1.725× (86.3% efficiency)** |

**Axis C — both together, i.e. how anyone actually runs it (`-n auto`):**

| Machine | Wall time | Speedup | Efficiency `E` | Cost premium `1/E − 1` |
|---|---|---|---|---|
| 2-core | 281.21 s | — | — | — |
| 4-core | 146.92 s / 145.38 s (two runs) | **1.914× / 1.934×** | **95.7%** | **+4.5%** |

**What the three axes together say — and it is not what a single axis would have said.**

1. **One worker cannot saturate four cores, but two can.** `-n 1` on the 4-core box (307.60 s) is
   *slower* than `-n 2` on the 2-core box (281.21 s), while `-n 2` on the 4-core box is **1.725×** faster
   than the same two workers on 2 cores. The suite's tests shell out constantly — git, `pre-commit`,
   `pyright` — so **each xdist worker occupies roughly two cores' worth of CPU** once its subprocess
   children are counted.
2. **The machine, not `-n`, is the binding constraint.** Doubling workers from 2 to 4 on fixed hardware
   bought only **12%**, because at `-n 2` the four cores were already ~89% consumed. Doubling the
   *cores* at fixed workers bought **72.5%**.
3. **Oversubscription is real and already measurable at 2:1.** `-n 8` on 4 cores is **10.1% slower** than
   `-n 4`. `-n auto` (= core count) remains the best setting measured, and is what the repo already does.
4. **Scaling has NOT stopped at 4 cores.** 95.7% efficiency across the only real machine doubling
   available means a bigger machine would still convert into wall time at near-full value, and — under
   the flat rate — for a **4.5% cost premium**.

**Where scaling stops: honestly, we cannot say, and here is why no number is offered.**

An Amdahl fit `T = Ts + Tp/n` over Axis A returns `Ts ≈ 73 s, Tp ≈ 227 s` (serial fraction 24%) with
residuals of **−2.5% / +14.3% / −10.7%** — a poor fit, and its projection to 8 and 16 *cores* is
**invalid**, because it was fitted on *workers*. Axis B proves those axes differ by a factor of ~2. A fit
on Axis B instead has only **two points for two parameters — zero degrees of freedom, no residual, no
validation** — and would project `T(8 cores) ≈ 80 s, T(16 cores) ≈ 46 s` on nothing but faith.

**So this audit reports the honest state: measured through 4 cores at 95.7% efficiency; unmeasured and
unprojectable beyond it.** The one thing Axis A does establish about larger machines is a *warning*: a
16-vCPU CX53 running `-n auto` would launch 16 workers each fanning out into subprocesses — the
oversubscription regime that already cost 10% at 4 cores. **A CX53 would need `-n` tuned below its core
count, and the gain over a 4-core Codespace is an open question, not a 4× given.**

**The decision consequence, which does not depend on the unmeasured part.** At 4 cores the suite runs in
**146 s** and `audit.py health` — the whole 207 s commit tax — runs in **19 s** (re-measured this sweep at
**20.0 s**, a fourth consistent reading). The operator's actual pain is already gone at the free tier's
top machine. **The marginal decision-value of cores 5 through 16 is therefore low**, whatever their
technical yield: the CX53's case rests on always-on, no metering, N parallel lanes and 4× RAM — not on
making a 146-second suite shorter.


### 6.5 The flat-rate breakeven against Hetzner — formula and computed threshold

```
Codespaces :  C_cs(H, c) = max(0, H·c − F) · p       F = included core-hours (120 Free / 180 Pro)
Hetzner    :  C_hz(H)    = min(H·r, K) + I           r = €0.0473/h, K = €29.49/mo cap, I = €0.50/mo IPv4

Setting them equal, in the regime H·c > F and H < K/r (= 623 h):

        (H·c − F)·p = (H·r + I)·x                    x = USD per EUR

                     F·p + I·x
        H*   =   ─────────────────
                     c·p − r·x
```

Computed, with the FX rate swung ±5% to show the threshold does not depend on it:

| Plan | Machine | Free-tier exhaustion `F/c` (currency-free) | Cost-parity `H*` at FX 1.05 / 1.10 / 1.15 |
|---|---|---|---|
| **Free (actual)** | **4-core** | **30 h/mo** | **36.5 / 36.9 / 37.2 h/mo** |
| Free | 2-core | 60 h/mo | 86.9 / 88.7 / 90.6 h/mo |
| Pro | 4-core | 45 h/mo | 53.9 / 54.4 / 54.9 h/mo |
| Pro | 2-core | 90 h/mo | 128.3 / 130.9 / 133.6 h/mo |

**FX sensitivity is negligible — 36.49 h to 37.22 h across a ±5% swing, a 2.0% spread** — so the
threshold is a property of the two price structures, not of the exchange rate, and can be quoted flat.

**The operative reading for the actual plan (Free, 4-core):**

- **Below 30 h/month** — Codespaces is **free**; Hetzner costs ~€1–3. Codespaces wins outright.
- **30 → 37 h/month** — Codespaces costs money but is still cheaper. **This window is only 7 hours wide.**
- **Above ~37 h/month** — **Hetzner is strictly cheaper, and it is simultaneously 4× the machine.** There
  is no usage level at which paying GitHub for additional 4-core hours beats renting the CX53 once the
  free tier is exhausted.

**Where the account actually sits today: 1.57 core-hours in August = 0.39 h/month of 4-core-equivalent
wall time — 1.3% of the allowance, roughly 77× below the free-tier exhaustion point.** On observed usage
the answer is unambiguous: **stay on the free tier.** But August 2026 is the first month this account has
used Codespaces at all (§1.3), so that is a floor, not a forecast — which is exactly why the decision
should be keyed to the threshold above rather than to today's number.

### 6.6 (d) The wall, verbatim, and what would unlock it

**The wall:** `Machine 'premiumLinux' is not available, Machine 'premiumLinux' is not allowed for this
repository` (HTTP 400), and from the CLI `there is no such machine for the repository: premiumLinux —
Available machines: [basicLinux32gb standardLinux32gb]`. It is **account-level**: it follows this token
across 15 repositories, 5 regions and both visibilities.

**What would unlock it — one leading hypothesis, testable for free.**

The account is `plan: free`, has **never been billed a cent for anything** (`netAmount > 0` items across
the entire usage report: **0**), and therefore carries the default **$0 spending limit with no payment
method**. GitHub's billing docs state that a personal account must set a **non-zero spending limit and a
payment method** before it can be billed for Codespaces at all. Every observation above is consistent
with the larger machine types being gated behind that billing enablement.

**This is a hypothesis and GitHub does not document it.** The docs list only three unavailability reasons
(§6.1), and billing state is not among them — but §6.1 eliminated all three, so the cause lies in the
undocumented residual, and billing state is the only account-level variable still standing.

**The test costs nothing and takes a minute** — setting a spending limit does not itself spend money:

1. Add a payment method and set a **non-zero** Codespaces spending limit at
   <https://github.com/settings/billing> .
2. Immediately re-run this, and diff against the two-machine baseline in §1.1:
   ```
   gh api repos/rdwornik/dev-knowledge/codespaces/machines --jq '[.machines[]|"\(.name) \(.cpus)c"]'
   ```
3. **If the list grows** past `standardLinux32gb`, the hypothesis holds and 6.4's extrapolation becomes
   directly measurable — re-run the sweep on 8-core and replace the projected row with a measured one.
   **If it does not grow**, the cap is something GitHub does not expose to users, and the remaining routes
   are **GitHub Support**, or **moving the repo into an organization on Team/Enterprise** (organizations
   get the full machine range plus explicit machine-type policies — at the price of losing the
   personal-account free allowance entirely, which §2.2 notes organizations do not receive).

**Neither step was taken by this audit**: both are billing changes, and the contract forbids paid-plan
changes.

---

## 7 · Environment defects that cost this audit time (unchanged from lane J §7 — still live)

1. **`~/.ssh/config` still carries a UTF-8 BOM.** Verified today: the first three bytes are `EF BB BF`, and
   every `ssh` invocation dies with `Bad configuration option: \357\273\277host` before it starts — which
   kills `gh codespace ssh`'s key selection. **The operator's ssh config is currently non-functional for all
   ssh use, not just Codespaces.** One-byte fix. This audit worked around it session-locally with a BOM-free
   copy passed as `ssh -F` and **did not modify the operator's file**.
2. **`rdwornik` still has no SSH public key registered** (`https://github.com/rdwornik.keys` is empty). A
   throwaway ed25519 keypair passed with `-i` works, because `gh` hands the chosen public key to the codespace.
3. **The `gh` active account moves, and it moved again during this audit.** It began as
   `Robert-Dwornik_ghub`; granting the `user` scope required `gh auth switch --user rdwornik` (§1.3), so it
   is now `rdwornik`. Every call here pinned `GH_TOKEN=$(gh auth token -u rdwornik)` regardless, and anyone
   scripting codespace work from this machine must do the same rather than trusting the active account.
4. **`gh api` needs `MSYS_NO_PATHCONV=1` in git-bash**, or leading-slash endpoints are rewritten into
   filesystem paths (`invalid API endpoint: "C:/Program Files/Git/user/codespaces"`). Not in lane J's list.
5. **The `${containerEnv:HOME}` stamp defect (lane J §2.1) reproduces on `main`.** The gate still prints the
   literal path, the stamp is absent from `$HOME`, and a directory literally named `${containerEnv:HOME}` is
   created **inside the working tree** on every container. Still open; still belongs to whoever disposes of
   `[#554]`.

---

## 8 · Resource hygiene

- Codespaces created: **2**, one per pass — `cs-audit-2026-08-20-4gvp5j96775cv6g` (items 1-5) and
  `cs-scaling-2026-08-20-q945j7g4w56h9jrp` (§6's sweep). **Both deleted**; each verified absent immediately
  afterwards via `gh api user/codespaces` → `{"names":[],"total":0}`.
- The §6.3 machine-type probes (`premiumLinux`, `largePremiumLinux`, via both CLI and REST) were **refused
  before creating anything** — `total_count: 0` was re-checked immediately after them. No orphan.
- §6's entitlement sweep touched **15 repositories read-only** (`codespaces/machines`, `contents/.devcontainer`)
  including 14 third-party public repos. Read-only API calls; nothing created, forked or starred.
- Branches created / pushed / deleted: **none.** The remote's branch list changed during the session only
  through other organs' activity (`claude/playbook-status-census-2026-08-20`,
  `docs/night-ab-gemini-2026-08-20` appeared); this audit touched no branch.
- Repo files changed: **none.** `git status --porcelain` was empty before the local comparator run and empty
  after it.
- `gh` active account: **changed by the operator, deliberately, mid-audit** — `gh auth switch --user rdwornik`
  was required to grant the `user` scope (§1.3), so the active account is now **`rdwornik`**, not
  `Robert-Dwornik_ghub`. This audit did not switch it and has not switched it back, and the
  **operator has since ruled that it stays `rdwornik`** for the remainder of fleet work, using `ghw` when the
  corporate identity is needed. It matters — lane J §7.3 recorded a live codespace appearing to vanish when
  the active account flipped underneath a session. Pin `GH_TOKEN` regardless.
- The operator's `~/.ssh/config` was **not modified**; a BOM-free copy and a throwaway keypair were created in
  the job's temp directory only.
- Nothing installed, no plan changed, no repo setting changed.
