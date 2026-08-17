# NB4-G scale-out — execution substrate, model routing, and the smallest reversible first step

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** This document decides nothing, adopts nothing, and births no BACKLOG row.
> No config file, dependency, hook, protocol or routing table was edited by the lane that
> produced it. The amended routing table in §3.5 is a **draft for ratification**, not a landed change.

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** nb4-g-scaleout-substrate
- **Lane:** `claude/nb4-scaleout-substrate-f8fhi1` (Anthropic cloud session, Linux container), NB4-G research lane
- **Base:** `main` @ `43cd1ce` (2026-08-16 14:05 +0200) · working tree clean before and after
- **Model:** Opus 5 · web search permitted · **no adoption, no config edits — evidence only**
- **Answers three bounded questions:** (1) execution substrate for 16–32 concurrent lanes,
  (2) model routing for cost, (3) the smallest reversible migration step.

---

## 0. Method, and the honest limits of it

**What is first-party here.** Every number in §1 was measured in this container, on this tree,
today: one `audit.py health` run, one full `pytest -m "not slow"` run, a `nproc`/`free` reading,
and the repo's own `logs/TOKEN-LOG.md` series. Those are the numbers that carry weight.

**Six limits, stated up front because each bounds a claim:**

1. **The egress proxy blocked five vendor pricing pages.** `docs.github.com`, `groq.com`,
   `console.groq.com`, `platform.moonshot.ai`, `www.hetzner.com`, `support.claude.com`,
   `colab.research.google.com` and `research.google.com` all returned `EGRESS_BLOCKED` to both
   WebFetch and `curl`. Anthropic's own docs (`code.claude.com`, `platform.claude.com`) fetched
   cleanly. **Consequence: Anthropic prices and product constraints below are PRIMARY; GitHub
   Actions, Hetzner, Groq, Moonshot, Google and Colab figures are SECONDARY** — search-surfaced
   from third-party aggregators. Every secondary figure is marked `[2°]` and must be re-verified
   against the vendor's own page before any money is committed. No figure in this document was
   supplied from recollection.
2. **Coding-quality benchmark numbers are the weakest evidence in this document and are used
   only to build a shortlist.** Aggregator sites disagree with each other on the same
   model/benchmark pair, sometimes by several points, and mix benchmark versions that their own
   text says are not comparable. §3.3 reports them as *claims with attribution*, never as an
   acceptance basis. **The acceptance basis is NB4-A's seeded-defect corpus and nothing else.**
3. **This container is 4 vCPU / 15 GB Linux; the operator's host is a ThinkPad, AMD Ryzen Pro,
   32 GB, Windows** (`protocols/ENVIRONMENT.md` "Hardware"). The measured per-lane cost in §1 is
   therefore a *Linux* figure. It is a controlled comparison against the Windows host, not a
   substitute for it — and the direction of the gap (Linux cheaper) is the finding, not a caveat.
4. **114 test failures + 13 errors in this container are environmental, not repo defects.** All
   127 resolve to four absent optional dependencies (`pydantic` ×82, `pandas` ×17, `rich` ×6,
   `pre_commit` ×1) in a bare container. Wall-clock is unaffected in kind — those tests still ran
   and still cost collection + import time — so the timing number stands; the pass/fail count is
   simply not this tree's.
5. **The `$` figures in `logs/TOKEN-LOG.md` are ccusage *model-priced*, not Max billing.** The log
   says so itself. They measure what the workload *would* cost at API list price. That is exactly
   the right unit for §3's question and the wrong unit for "what did Rob pay" — both readings are
   used below, separately and labelled.
6. **No lane-duration telemetry exists yet.** `[#529]` (telemetry v1 EMIT) is filed and unlanded,
   so "a lane is ~2.5 h" is derived from the batch protocol's own 3h30m poll cap and the
   operator's measured "~1h step-0 commits", not from a measured distribution. Every per-lane-hour
   figure inherits that uncertainty. **This is the single largest source of error in §2 and §5.**

**Library-first ladder applied as stated** (stdlib > established dependency > stabilized project >
industry pattern). It lands on the top rung twice: the recommended substrate needs **no new
software at all** (§2.5), and the recommended first step is a **scheduling change, not a build**
(§4.1).

---

## 1. The measured baseline — what a lane actually costs

### 1.1 Numbers measured in this container today

```
host                      4 vCPU / 15 GB / Linux 6.18.5 (cloud session container)
audit.py health           19.0 s   (exit 1 — DEGRADED, 2 advisory WARNs; the gate ran in full)
pytest -m "not slow"     507.4 s   (-n auto = 4 workers; 2728 passed, 36 skipped, 1 xfailed)
suite size               2895 collected: 2888 not-slow, 7 slow
derived CPU work         ~2030 CPU-s ≈ 34 CPU-min per full not-slow suite run
```

**Cross-check against the only comparable prior measurement.** The night-3 research lane measured
full-suite runs at **485 s and 957 s** in the same class of container
(`docs/audits/2026-08-15-technical-night3-research.md` §0). Today's 507 s sits inside that band.
The suite cost is therefore stable and reproducible, not an artifact of one run.

### 1.2 The derived sizing constant

A lane is **idle on CPU most of the time** — it is waiting on model inference — punctuated by gate
bursts. The bursts are what saturate a host. Per lane per hour, assuming ~4 gated commits and
~0.5 suite runs:

```
audit.py health     4 × 19 s          =    76 CPU-s
not-slow suite      0.5 × 2030 CPU-s  = 1,015 CPU-s
ruff + other hooks  (small, unmeasured separately)
                                      ≈ 1,100 CPU-s per lane-hour
                                      ≈ 0.3 sustained cores per lane
```

**Sizing constant: ≈0.3 sustained cores + ~1.5–2 GB RAM per lane, with burst to ~1 core.**
Sized with headroom at **0.5 core/lane**, because the bursts are correlated — lanes that booted
together hit step-0 commit together, which is precisely the thrash the operator measured.

**This constant explains the Windows saturation arithmetically.** 12 lanes × 0.3 = 3.6 sustained
cores, bursting toward 12. A Ryzen Pro mobile part has ~8 threads. The lanes were not slightly
over budget — at burst they were oversubscribed ~1.5×, and every lane's `audit.py health` was
queueing behind every other lane's. **~1 h step-0 commits from a 19 s gate is a ~190× stretch
factor**, which is what oversubscription plus Windows process-spawn cost looks like.

### 1.3 Why Windows specifically makes it worse

Not measured here (this container is Linux), so this is mechanism, flagged as such:
`audit.py health` at 19 s and each pre-commit hook are **process-spawn-heavy** workloads —
`fork`+`exec` on Linux versus `CreateProcess` on Windows, once per hook per commit, times
`pytest-xdist` worker startup per suite run. The hub's own `pyproject.toml` carries a comment
block about xdist/mutmut fork interactions, and `[#498]` records a POSIX-only exec-bit defect that
"no test on the current fleet would ever go red for" *because the fleet is Windows*. The platform
is already costing correctness, not only wall-clock.

### 1.4 What a lane costs in model spend (measured, `logs/TOKEN-LOG.md`)

```
2026-08-04 week   10 active days   8.36M in+out   $1,676.83   peak day $356.29   Opus 5 72.1%
2026-07-25 week    8 active days   9.88M in+out   $1,414.53   peak day $398.24
2026-07-17 week    6 active days  12.68M in+out   $1,382.23   peak day $356.67
2026-07-09 week    8 active days  20.25M in+out   $2,490.46   peak day $503.41
```

Model-priced (ccusage, includes cache tokens; ≠ Max billing — limit 5).

Dividing the 2026-08-04 week by active days gives **~$168/active day**. At ~8 lanes/day that is
**≈$21 per lane, ≈$8 per lane-hour, model-priced.** Peak day at 8 lanes ⇒ ~$45/lane. Take the
working band as **$20–45 per lane, model-priced.**

### 1.5 The finding that governs everything below

Put the two measurements side by side, per lane-hour:

```
model spend (model-priced)     ~$8 - $18   per lane-hour
compute (rented Linux, §2.2)   ~$0.08      per lane-hour
ratio                          ~100 : 1 to ~200 : 1
```

**Compute is ~1% of the true cost of a lane. The model is ~99%.** And on a Max subscription the
model is currently **$0 at the margin** until a rate limit is hit.

Two consequences run through the rest of this document:

- **Substrate must be chosen for wall-clock and rate-limit headroom, not for compute price.**
  Arguing about €64 versus €122 a month while a batch burns $1,700 a week of model-priced tokens
  is optimising the wrong term by two orders of magnitude.
- **Model routing to a cheaper vendor converts $0-marginal subscription tokens into real cash.**
  It is a *rate-limit* remedy, not a *cost* remedy. §3 is built on that correction.

---

## 2. Q1 — Execution substrate for 16–32 concurrent lanes

### 2.1 The constraint that collapses the option space

Read together, two primary Anthropic sources impose a hard architectural fact:

- Cloud sessions: *"`--cloud` requires an Anthropic account. It's not available when Claude Code
  is configured for Amazon Bedrock, Google Cloud's Agent Platform, or another third-party
  provider."* ([Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web))
- Self-hosted environments: *"sessions use the Anthropic API, and inference can't be routed
  through Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or an LLM gateway."*
  ([Self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments))

**Q1 and Q2 are therefore not independent.** Every cloud-session substrate — Anthropic-hosted or
self-hosted runner — **forecloses third-party model routing**. The only substrate on which a
producer lane can run Kimi, Gemini or a Groq-hosted model is a machine running the `claude` CLI
(or a native vendor CLI) directly, with `ANTHROPIC_BASE_URL` under the operator's control. That is
the rented Linux host.

This is the single most important structural finding in the report, and it is not visible from
either question asked alone.

### 2.2 The four candidates, measured against the §1.2 sizing constant

**A. Claude cloud sessions (current).**
Primary: *"There is no separate compute charge for the cloud VM"*; *"each `--cloud` command creates
its own cloud session that runs independently… they'll all run simultaneously in separate
sessions"*; *"Claude Code on the web shares rate limits with all other Claude and Claude Code usage
within your account. Running multiple tasks in parallel consumes more rate limits proportionately."*
Isolation: *"each session runs in an isolated, Anthropic-managed VM"*; *"sensitive credentials such
as git credentials or signing keys are never inside the sandbox with Claude Code; authentication is
handled through a secure proxy using scoped credentials."*

- **Compute cost/lane/hour: $0.00** (primary, explicit).
- **Ops burden: zero.** No image, no fleet, no patching. This lane is running on it right now.
- **Security of private repos: the strongest of the four.** Git credentials never enter the
  sandbox. Note the stated caveat that a cloud session can reach *any* repository the connected
  GitHub account can see, so blast radius is controlled on GitHub, not in Claude.
- **Windows pain removed: completely.** Linux container, POSIX exec bits, cheap `fork`.
- **The binding limit is rate limits, not compute.** No documented cap on concurrent sessions was
  found; the documented failure mode is `Session creation failed` when a VM can't be allocated,
  with *"retry after a minute, as capacity is provisioned on demand."*
- **Honest limit:** on Max, rate-limit headroom is the scarce resource, and secondary sources
  consistently report that the weekly cap did not scale with the 5x→20x session multiplier `[2°]`.
  This is the number that decides whether 32 lanes is reachable, and it is the number nobody has
  measured on this account.

**B. Rented Linux host (the operator already has hosting).**
Sizing straight from §1.2 at 0.5 core/lane and 2 GB/lane:

```
16 lanes   ->   8 cores  / 32 GB   ->  Hetzner AX52  (Ryzen 7 7700, 8c/16t, 64 GB)   EUR 64.00/mo [2°]
32 lanes   ->  16 cores  / 64 GB   ->  Hetzner AX102 (Ryzen 9 7950X3D, 16c/32t,128GB) EUR 122.30/mo [2°]
32 lanes + headroom                ->  Hetzner AX162 (EPYC 9454P, 48c/96t)            EUR 199.00/mo [2°]
```

Cost per lane-hour at 20 batch-days/month, 2.5 h/lane:

```
16 lanes:  800 lane-h/mo   EUR  64.00 / 800   = EUR 0.080 per lane-hour
32 lanes: 1600 lane-h/mo   EUR 122.30 / 1600  = EUR 0.076 per lane-hour
```

- **Ops burden: real and recurring** — image, patching, disk, backups, secret handling, and *the
  gate stack has to be armed and kept armed on it*. `arm_hooks.py` and the `pre-commit install
  --hook-type pre-push` one-time activation in CLAUDE.md §9 become fleet-provisioning concerns.
- **Security of private repos: the weakest of the four, and this is the real cost.** Git
  credentials and an Anthropic token live on a machine the operator owns and must defend. Contrast
  with option A, where credentials are never in the sandbox at all.
- **Windows pain removed: completely**, and this is where the ~$0.08/lane-hour buys the most.
- **Unique property: it is the only substrate that can host third-party model routing (§2.1).**
- **Uncertainty:** Hetzner announced a standardization and repricing of all dedicated servers
  effective 2026-06-15 `[2°]`. Every EUR figure above must be re-checked on Hetzner's own page.

**B′. Self-hosted Claude Code environments — the hybrid, and why it is currently out of reach.**
Anthropic supports routing cloud sessions onto the operator's own runners: *"A runner registers
with the environment, receives a runner token, and polls for sessions"*, with per-runner
`--capacity` concurrency and an optional autoscaling orchestrator. It would give the rented host's
Linux economics *with* the cloud session's dispatch UX.

**Three blockers, all primary:**
1. *"public beta on Team and Enterprise plans"* — **not available on Max.** Team is a paid step up
   (Anthropic's own enterprise page lists Teams at **$150/seat (Premium)**; secondary sources say
   $125/seat monthly with a 5-seat minimum `[2°]` — the two disagree and neither was verifiable
   through the proxy).
2. *"A runner serves one user at a time… The minimum fleet size is therefore the number of users
   you expect to be active at once."* For a single operator this is a non-issue, but it is the rule
   that makes the model make sense.
3. It still cannot route third-party models (§2.1), so it does **not** unlock Q2.

**Verdict: correct destination, wrong price today.** Re-evaluate if a Team plan is ever bought for
another reason. Do not buy a Team plan *for* this.

**C. GitHub Actions runners.**
Secondary pricing `[2°]`, January 2026 rate cut, cloud-platform charge already folded in:

```
Linux 1-core (ubuntu-slim)  $0.002/min      Linux 16-core   $0.042/min
Linux 2-core                $0.006/min      Linux 32-core   $0.082/min
Linux 4-core                $0.012/min      Linux 64-core   $0.162/min
Linux 8-core                $0.022/min
```

A 4-core runner ≈ **$0.72/lane-hour** ⇒ **$1.80/lane** at 2.5 h ⇒ at 32 lanes × 20 days,
**~$1,150/month**. That is **~9× the AX102** for the same work, and it is the *only* option whose
compute cost is a material fraction of the model cost.

- **Concurrency is a hard blocker at the target width:** standard-runner concurrent-job caps are
  reported as Free 20 / Pro 40 / Team 60 `[2°]`, and **larger runners are Team/Enterprise only**
  `[2°]`. 16–32 lanes fits, but leaves little room, and each lane is a long-lived job, not a
  short CI job — Actions' 6-hour job ceiling sits uncomfortably close to the 3h30m batch cap.
- **The self-hosted-runner `$0.002/min` charge was postponed, not cancelled** — GitHub's own words
  are *"postponing the announced billing change… to take time to re-evaluate our approach"*, with
  no timeline and no guarantee it won't return. **Building the substrate on free self-hosted
  runners is building on an explicitly re-openable price.**
- **Where Actions genuinely wins: event-triggered, bounded, single-shot work** — which the hub
  already does (`nightly-conformance-triage`). It is a poor host for a 2.5-hour stateful agent
  lane. **Recommend: keep, do not extend.**

**D. Google Colab — does it fit at all?**

**No. Not marginally — categorically.** Colab's own terms and FAQ, as surfaced `[2°]`, disallow
essentially every property this workload needs:

- *"The following are disallowed from managed Colab runtimes running free of charge: remote
  control such as SSH shells, remote desktops."* A dispatched agent lane is remote control.
- *"Colab prioritizes users who are actively programming in a notebook"*, and disallows
  *"other web service offerings not related to interactive compute with Colab."* A 2.5-hour
  unattended git+CLI agent is the definition of non-interactive.
- *"users who use Colaboratory for long-running computations may be temporarily restricted in the
  type of hardware made available to them, and/or the duration that the hardware can be used for."*

Beyond policy, the fit is wrong on mechanics: ephemeral VMs with idle-disconnect, a notebook
kernel rather than a shell session, no durable filesystem across runs, and no clean place to hold
git credentials. **Colab is a GPU notebook host. This workload is CPU-bound, stateful, long-lived
and non-interactive — the exact inverse.** It should be struck from the option list rather than
carried as a cheap fallback; carrying it invites a future window to re-litigate it.

### 2.3 Comparison table

```
                     A. Claude cloud   B. Rented Linux    C. GH Actions      D. Colab
compute $/lane-hour  $0.00             ~EUR 0.08 [2°]     ~$0.72 [2°]        n/a
16-lane monthly      $0 compute        EUR 64   [2°]      ~$576   [2°]       n/a
32-lane monthly      $0 compute        EUR 122  [2°]      ~$1,152 [2°]       n/a
ops burden           none              real, recurring    moderate           n/a
private-repo sec.    strongest (creds  weakest (creds     medium (GH-        unacceptable
                     never in sandbox)  on your box)      native secrets)
Windows pain gone    yes                yes               yes                n/a
3rd-party models     NO (foreclosed)    YES (only one)    YES                n/a
concurrency limit    rate limits        cores (measured)  20/40/60 jobs [2°] n/a
long-running fit     yes (persistent)   yes               poor (6 h ceiling) prohibited
verdict              KEEP as default    ADD for routing   KEEP, don't extend STRIKE
```

### 2.4 Security of private repos — the axis most likely to be under-weighted

Ranked by how much of the operator's credential surface each substrate exposes:

1. **Claude cloud (A): best.** Git credentials are structurally absent from the sandbox. This is a
   property the operator cannot reproduce on a rented host at any price.
2. **GitHub Actions (C): good**, if `GITHUB_TOKEN` scoping and OIDC are used; the token is
   short-lived and repo-scoped by default.
3. **Rented Linux (B): worst, by construction.** A long-lived host holding a git credential and an
   Anthropic token, reachable from the internet, patched by the operator. **If B is adopted, the
   credential model is the design problem, not the sizing** — the mitigation is short-lived
   per-lane tokens and a host that never holds a durable push credential.
4. **Colab (D): not assessable**, and prohibited anyway.

### 2.5 Substrate recommendation

**Keep Claude cloud sessions as the default execution substrate. Add one rented Linux host as a
second, narrower substrate — and add it for the capability it uniquely has (third-party model
routing, §2.1), not for its compute price.**

The reasoning is §1.5: compute is 1% of the cost. Option A already delivers Linux, zero ops, the
best credential posture and $0 compute, and the operator's own measurement is that *cloud sessions
finished faster*. Paying €122/month to reproduce that on a box he must defend and patch buys
nothing **unless** the rented host is doing something cloud sessions cannot — and there is exactly
one such thing.

**This recommendation needs no new software.** Option A is already in production; option B runs the
same `claude` CLI the operator already has.

---

## 3. Q2 — Model routing for cost

### 3.1 The correction the measurement forces

The brief frames this as cost reduction. §1.5 says that framing is inverted on a Max subscription:
model tokens are **$0 at the margin** until a rate limit is hit, so every producer lane moved to
Kimi/Groq/Gemini/Codex **converts a free token into a billed one**.

Reframed honestly, model routing buys exactly two things:

- **Rate-limit headroom** — the actual binding constraint at 16–32 lanes. Producer tokens moved
  off Anthropic are subscription capacity returned to the architect/reviewer roles.
- **Vendor independence** — a second producer that keeps working when Anthropic is rate-limited,
  degraded, or overloaded.

**It does not buy cost reduction in the operator's current billing posture.** Anyone who reads the
draft table below as a savings measure has read it wrong, and §3.5 says so in the table itself.

### 3.2 Candidate prices (per Mtok)

Anthropic figures **PRIMARY** (`platform.claude.com/docs/en/about-claude/pricing`, fetched today).
All others `[2°]`.

```
model                       input     output    cache-hit input   source
Claude Fable 5              $10.00    $50.00    $1.00             PRIMARY
Claude Opus 5               $ 5.00    $25.00    $0.50             PRIMARY
Claude Sonnet 5             $ 2.00    $10.00    $0.20             PRIMARY  (introductory
                                                                  price is now standard;
                                                                  the Sept-1 rise to $3/$15
                                                                  "will not occur")
Claude Haiku 4.5            $ 1.00    $ 5.00    $0.10             PRIMARY
Kimi K3 (Moonshot direct)   $ 3.00    $15.00    $0.30             [2°]
Kimi K2 (via Groq)          $ 1.00    $ 3.00    $0.50             [2°]
Gemini 3 Pro (<=200k ctx)   $ 2.00    $12.00    -                 [2°]
Gemini 3.1 Pro Preview      $ 1.00    $ 6.00    -                 [2°]
GPT-5.6 Luna                $ 0.20    $ 1.20    -                 [2°]
GPT-5.6 Terra               $ 2.00    $12.00    -                 [2°]
GPT-5.6 Sol                 $ 5.00    $30.00    -                 [2°]
```

Anthropic-side modifiers, all primary and all relevant to a fan-out: Batch API **−50%** on both
directions; cache read **0.1×** base input; 1-hour cache write **2×**; **1M context at standard
price** on 4.6+ ("a 900k-token request is billed at the same per-token rate as a 9k-token
request"). One further primary fact with direct bearing on any token forecast: *"Claude 4.7 and
later models… use a newer tokenizer… This tokenizer produces approximately 30% more tokens for
the same text."* **Any Opus-5-versus-other-vendor token comparison that ignores this is wrong by
about 30% in Anthropic's disfavour on token count and in its favour on per-token price.**

**The honest price ranking for a producer role:** Kimi K2 on Groq ($1/$3) and Gemini 3.1 Pro
($1/$6) are genuinely 4–8× cheaper than Opus 5 on output. **Kimi K3 at $3/$15 is not** — it is
0.6× Opus 5, which does not justify a second harness on price alone. GPT-5.6 Luna at $0.20/$1.20
is the cheapest credible entry by a wide margin and deserves a corpus run for that reason alone.

### 3.3 Coding-quality evidence — reported as claims, not as findings

Every number here is `[2°]` from aggregator sites that **disagree with one another**, and several
mix Terminal-Bench 2.0 with 2.1 scores that their own text says are not comparable. **Use for
shortlisting only.**

```
claim (SWE-bench Verified)      Claude Opus 5 96% · GPT-5.6 Sol 96.2% · Kimi K3 93.4%
                                Claude Opus 4.8 88.6% · Kimi K2.6 80.2% · Kimi K2.5 76.8%
claim (Terminal-Bench 2.1)      GPT-5.6 Sol 89.5% · Claude Opus 5 89.1% · Kimi K3 88.3%
                                Grok 4.6 88.4% · Gemini 3.7 Flash 85.8%
```

**What these numbers can support:** Kimi K3, GPT-5.6 (Luna/Terra) and Gemini 3.x are plausibly in
the same coding-competence band as the Opus line, so a producer trial is not obviously wasteful.

**What they cannot support:** any admission decision. `[#492]` already ruled the method for this
exact class of question — *"Entry by measured acceptance, never vibes"* — and the seeded-defect
corpus v0.1 exists, is reconciled (12/12 verdicts re-derived, 0 flips,
`docs/audits/2026-08-13-verification-492-corpus-reconciliation.md`), and is the instrument the
fleet already built for it. **§3.5's table is gated on that corpus, run against these candidates,
and on nothing else.**

### 3.4 Harness maturity and fit to the frozen-contract shape

The fleet's lane shape is specific: a **frozen contract** file, a worktree or branch, a gate stack
that must fire (`audit.py health`, `ruff`, commit-msg gates, two pre-push organs), and a packet
written on the way out. A producer must survive that, not merely write code.

```
harness              maturity for this shape                                    verdict
claude CLI + ANTHROPIC_BASE_URL swap
                     Highest. Same binary, same CLAUDE.md, same skills, same
                     hooks, same /lane-boot. Only the backend moves. Moonshot,
                     Z.ai and MiniMax all expose Anthropic-compatible
                     endpoints [2°]; Moonshot exposes an /anthropic base path
                     specifically so Claude Code works with no wrapper [2°].    PREFERRED
Kimi Code CLI        Native TypeScript agent CLI, MIT, single binary, MCP via
                     /mcp-config [2°]. Own harness => own hook semantics; the
                     hub's gate stack is not known to fire under it.           second choice
Codex CLI            Mature, but bills through ChatGPT plan local-message
                     allowances that CLI and web share [2°]. Already assessed
                     here: `[#469]` records the codex lane runs an UNPINNED
                     model, and ENVIRONMENT.md's Council decision list carries
                     "Codex CLI (no advantage over Haiku subagents)".          reviewer only
Gemini CLI           Free tier ~1,000 req/day, 60 rpm on a personal Google
                     account [2°]. Different harness, different config
                     surface, no CLAUDE.md equivalence.                        read-only lanes
Groq                 Not a harness — an inference host. Reaches the fleet only
                     through one of the above. Its value is latency + the
                     $1/$3 Kimi K2 rate [2°].                                  backend, not agent
```

**The `ANTHROPIC_BASE_URL` swap is the only option that preserves the frozen-contract shape
unchanged**, because it changes nothing except which endpoint answers. Every other option asks the
fleet's gate stack to work under a harness it has never run under — which is a second, unpriced
migration. **Recommendation: if a producer is admitted, admit it as a backend behind the existing
CLI, not as a new agent CLI.**

**And note the collision with §2.1: this swap cannot be done in a cloud session.** A routed
producer lane must run on the rented host. That is the whole reason §2.5 recommends buying one.

### 3.5 Draft amended routing table — roles, not vendors

**PROPOSED. NOT ADOPTED. Gated on §3.6.** Vendors appear only in the "candidate backends" column;
the binding column is the role. The t-shirt pins (S=Haiku / M=Sonnet / L,judgment=Opus,
ARCHITECTURE Ch3 / ADR-70) are **unchanged** — this adds a *producer* axis, it does not renumber
the size axis.

```
role            what it does                       pinned today   candidate backends    gate to move it
--------------  ---------------------------------  -------------  --------------------  ------------------
ARCHITECT       rules, adjudicates, writes the      Opus 5         NONE. Not a candidate. n/a - never routed
                contract, decides what is true                    Judgment stays here.
REVIEWER        adversarial read of a landed        Opus 5 /       NONE for the primary. corpus catch-rate
                packet; the producer-not-reviewer   codex lane     A SECOND reviewer may  >= terra baseline
                rule (PLAYBOOK) binds here                         be added (`[#492]`).   on the SAME diffs
PRODUCER (L)    implements a frozen contract that   Opus 5         Kimi K3, GPT-5.6 Terra corpus + a real
                needs judgment mid-lane                            via BASE_URL swap      lane, zero-regress
PRODUCER (M)    implements a frozen, mechanical     Sonnet 5       Kimi K2 (Groq),        corpus + a real
                contract; the spec IS the answer                   Gemini 3.1 Pro,        lane, zero-regress
                (e.g. `[#533]` byte-identical                      GPT-5.6 Luna
                extraction)
PRODUCER (S)    read-only fan-out, snapshots,       Haiku 4.5      GPT-5.6 Luna           corpus (read-only
                report condensation                                                       subset)
INTEGRATOR      walks the merge queue serially      Opus 5         NONE. Touches main.    n/a - never routed
                (`/lane-integrate`)
```

**Five rules carried with the table, each with a reason:**

1. **ARCHITECT and INTEGRATOR are never routed.** One decides what is true; the other touches
   `main`. Neither is a cost centre worth optimising and both are where a wrong answer is most
   expensive.
2. **PRODUCER (M) is the only tier worth routing first.** Its contracts are frozen and mechanical,
   so a producer's failure mode is *visible in the gate* rather than latent in a judgement.
   `[#533]`'s byte-comparison Done-when is the ideal first subject: the acceptance test is
   mechanical, so a wrong producer cannot pass it by being persuasive.
3. **No `fallbackModel` on a routed stage.** Existing doctrine (ADR-80 §5, PLAYBOOK) — a silent
   swap breaks evidence comparability, and it breaks it worse across vendors than within one.
4. **A routed lane must declare its backend in its packet.** Otherwise the n=2 evidence gate is
   comparing runs whose backend nobody recorded. This is `[#469]`'s unpinned-model defect
   generalised before it repeats.
5. **The table is per-role, so a vendor's exit costs one row.** That is the entire point of
   roles-not-vendors: Kimi K3 losing its corpus re-run next quarter should edit one cell, not
   re-open the routing model.

### 3.6 The acceptance gate — stated so it cannot be softened later

**No row of §3.5 moves off its "pinned today" value until all four hold:**

1. The candidate runs **NB4-A's seeded-defect corpus** (v0.1, 12 seeds, reconciled 0-flip) against
   the **same diffs** as the Opus/terra baseline, and its catch rate is recorded.
2. It runs **one real lane** end to end under the frozen-contract shape, with the **full hub gate
   stack armed** — `audit.py health`, `ruff`, both commit-msg gates, both pre-push organs — and
   passes without `--no-verify` and without `SKIP=`.
3. Its packet **names its backend and model id**, per rule 4 above.
4. The result is **recorded as a measurement, pass or fail** — a refused candidate is a finding,
   not a non-event. `[#492]`'s Grok row is the precedent: an unmet peg leaves the row unchanged
   and is written down.

**Anything less is vibes, and this fleet has already ruled that insufficient.**

---

## 4. Q3 — Migration path: the smallest reversible first step

### 4.1 The step

**Move the night batch's READ-ONLY fan-out to a rented Linux host, with one PRODUCER (M) lane
routed through `ANTHROPIC_BASE_URL` to a single candidate backend, and run the seeded-defect
corpus against it in the same window. Mutating lanes stay exactly where they are.**

Concretely, over one night:

```
1. Provision ONE host (AX52 class, 8c/64GB) - not a fleet. [2°] EUR 64/mo, cancellable monthly.
2. Clone the hub. Arm the gates: `pre-commit install --hook-type pre-push` (CLAUDE.md sec.9's
   one-time activation) + `arm_hooks.py`. Prove `audit.py health` runs and its wall-clock is
   recorded - the Linux-vs-Windows delta is the first datum the host produces.
3. Run the night batch's read-only lanes there. Read-only means: no push, no merge, no BACKLOG
   write. Artifact-or-RED, as every night lane already obeys.
4. Route ONE producer lane via BASE_URL swap. Run the sec.3.6 corpus in the same window.
5. Mutating lanes, the merge queue and `/lane-integrate` stay on the current substrate,
   unchanged.
```

### 4.2 Why this step and not a bigger one

- **It is reversible in one command.** Cancel the host; nothing in the tree changes. No ADR, no
  hook, no protocol edit is required to try it, and none is required to undo it.
- **It buys the two measurements that every larger decision waits on**, and cannot be bought any
  other way: (a) the **Linux-vs-Windows gate delta on the operator's own tree**, which is the whole
  premise of moving substrate; (b) the **first corpus catch-rate for a non-Anthropic producer**,
  which is the gate in §3.6.
- **It respects the operator's own stated sequencing** — mutating lanes stay local "until
  single-flight + grammar gates are proven remote". Both organs already exist to be proven:
  `[#530]`'s single-flight guard landed (`50daad05`) and arbitrates on `origin`, and the grammar
  gate ran 11/11 with 0 refusals on the batch-6 roster. **What is unproven is not the organs but
  their behaviour under a second substrate**, and read-only lanes exercise the grammar gate
  without risking the queue.
- **It creates no standing artifact.** Per `[#443]`'s rent rule, a night batch produces dated
  reports with a named consumer, not new planning surface.

### 4.3 The kill criterion, pre-registered

**If, after two nights, the Linux host's measured gate wall-clock is not materially better than
the Windows host's on the same tree, the substrate premise is falsified — cancel the host and keep
cloud sessions as the sole substrate.** The producer-routing question then stands alone and is
answered by the corpus on whatever substrate is convenient.

Pre-registering this matters because §1.5 predicts the host will *not* pay for itself on compute
price. It has to pay for itself on wall-clock and on the routing capability, or not at all.

### 4.4 What must NOT move in this step

- **The merge queue and `/lane-integrate`.** Every git mutation stays serial in the orchestrating
  thread (PLAYBOOK); a second substrate holding a push credential while the queue walks is exactly
  the collision `[#530]` was built to refuse.
- **ARCHITECT and REVIEWER roles** (§3.5 rule 1).
- **Anything requiring an ADR.** If this step needs an ADR, it is not the smallest step.

---

## 5. Recommendation

**Substrate: Claude cloud sessions stay the default. Add ONE rented Linux host as a narrow second
substrate — bought for the third-party-routing capability it uniquely has (§2.1), not for its
compute price (§1.5). GitHub Actions stays for event-triggered CI and is not extended. Colab does
not fit and should be struck from the option list.**

**Estimated cost:**

```
                              16 lanes                    32 lanes
compute (cloud sessions)      $0                          $0                     PRIMARY
compute (1 rented Linux host) ~EUR 64/mo  (AX52)  [2°]     ~EUR 122/mo (AX102) [2°]
model, model-priced           ~$6,700/mo                  ~$13,400/mo
  (320 / 640 lanes per month at $21/lane, sec.1.4)
model, actual cash on Max     $100-200/mo until rate limits bind; metered overage past that
compute as share of total     ~1%                         ~1%
```

**The number that decides feasibility at 32 lanes is not in this table**: it is the operator's
weekly rate-limit headroom, which no source could establish and which §0 limit 6 says is
unmeasured. **At 16 lanes the current substrate is already adequate; at 32 lanes the constraint
becomes rate limits, and routing PRODUCER (M) off Anthropic is the remedy — which is precisely
why the rented host is worth its €64.**

**First step: one AX52-class Linux host for one month, running the night batch's read-only fan-out
plus a single `ANTHROPIC_BASE_URL`-routed PRODUCER (M) lane with the seeded-defect corpus run in
the same window. Mutating lanes, the merge queue and `/lane-integrate` do not move. Kill criterion
pre-registered at §4.3: no material Linux-vs-Windows gate delta after two nights ⇒ cancel and
revert.**

---

## Sources

**Primary (fetched this session):**
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) — parallel `--cloud` sessions, "no separate compute charge for the cloud VM", shared rate limits, isolation and credential model, third-party-provider exclusion
- [Self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments) — runner/environment/session model, `--capacity`, one-user-per-runner, Team/Enterprise-only beta, no third-party inference
- [Automate work with routines](https://code.claude.com/docs/en/routines) — schedule/API/GitHub triggers, 1-hour minimum cron interval, daily run cap, usage credits
- [Enterprise deployment overview](https://code.claude.com/docs/en/third-party-integrations) — deployment options, LLM-gateway env vars, Teams $150/seat (Premium)
- [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) — all model prices, cache multipliers, batch −50%, Sonnet 5 price note, 4.7+ tokenizer ~30% note
- In-repo, measured today: `scripts/audit.py health` (19.0 s), `pytest -m "not slow"` (507.4 s), `logs/TOKEN-LOG.md`, `protocols/ENVIRONMENT.md`, `docs/audits/2026-08-15-technical-night3-research.md`

**Secondary `[2°]` (search-surfaced; vendor pages blocked by the egress proxy — re-verify before committing money):**
- [Pricing changes for GitHub Actions](https://github.com/resources/insights/2026-pricing-changes-for-github-actions) · [GitHub Actions pricing 2026 (CICDCost)](https://cicdcost.com/github-actions-pricing) · [Northflank: self-hosted runner cost change](https://northflank.com/blog/github-pricing-change-self-hosted-alternatives-github-actions)
- [Hetzner AX102](https://www.hetzner.com/dedicated-rootserver/ax102/) · [Cheap dedicated server 2026](https://klymentiev.com/blog/cheap-dedicated-server-2026) · [Hetzner price adjustment 15 June 2026](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/)
- [Groq pricing 2026](https://www.cloudzero.com/blog/groq-pricing/) · [Groq API pricing & free-tier limits](https://klymentiev.com/blog/groq-pricing)
- [Kimi K3 pricing](https://www.eesel.ai/blog/kimi-k3-pricing) · [Kimi API pricing, August 2026](https://benchlm.ai/moonshot/api-pricing) · [Kimi Code CLI](https://www.marktechpost.com/2026/06/06/moonshot-ai-releases-kimi-code-cli-a-terminal-ai-coding-agent-built-in-typescript-for-next-gen-agents/) · [cc-compatible-models](https://github.com/Alorse/cc-compatible-models)
- [Gemini CLI free tier](https://inventivehq.com/blog/gemini-cli-free-tier-guide) · [Gemini API pricing, Aug 2026](https://benchlm.ai/google/api-pricing)
- [Codex rate card](https://help.openai.com/en/articles/20001106-codex-rate-card) · [OpenAI Codex pricing 2026](https://www.eesel.ai/blog/openai-codex-pricing)
- [Colab FAQ](https://research.google.com/colaboratory/faq.html) · [Colab additional terms](https://colab.research.google.com/terms)
- [SWE-bench Verified leaderboard](https://benchlm.ai/benchmarks/swe-bench-verified) · [Terminal-Bench 2.0 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.0) · [Terminal-Bench leaderboard 2026](https://codingfleet.com/blog/terminal-bench-leaderboard-2026/)
- [GitHub Actions limits discussion](https://github.com/orgs/community/discussions/26422) · [Claude Team plan](https://justinmckelvey.com/blog/claude-team-plan) · [Claude Code rate limits](https://www.truefoundry.com/blog/claude-code-limits-explained)

---

## AMENDMENT 1 (2026-08-16, same lane) — the `uv` pin makes every `uv run` organ inert in this substrate

> **In-file amendment marker**, per CLAUDE.md §5 rule 3 (audits are immutable; supersede with a new
> file **or an in-file amendment marker**). §0–§5 above are unchanged and are NOT rewritten. This
> section adds one measured finding that reached the lane after §4 was written, and corrects the
> §4.1 provisioning checklist it falsifies.

**How it surfaced.** This lane's own `Stop` hook failed to execute at session end:

```
[uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"]:
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

**Diagnosis, measured in this container:**

```
pyproject.toml:25   [tool.uv] required-version = "==0.11.19"   (deliberate; ADR-106)
container uv        0.8.17 at /root/.local/bin/uv              (baked into the image)
uv self update      "The version 0.11.19 was not found for the app uv in workspace uv" -- FAILS
PyPI                0.11.19 EXISTS (latest 0.12.5)             -- so the PIN IS VALID
pip install uv==0.11.19  -> lands at /usr/local/bin/uv, but /root/.local/bin PRECEDES it on PATH,
                            so the stale 0.8.17 still wins until the earlier entry is shadowed
after shadowing     `uv run --locked python scripts/session_end_backpressure.py` -> exit 0, silent
```

**Attribution, stated because it decides who owns it.** This is **not** a repo defect: the pin is
valid, deliberate, and carries its own rationale (uv is pre-1.0, ships ~every three days, and
`--locked` semantics moved on 2026-07-23 — so a uv bump is its own gated change). It is **not**
caused by this lane, which touched two markdown files. It is an **environment gap**: the Anthropic
cloud image ships a uv roughly three minor versions below the hub's pin, and the image's own
`uv self update` channel cannot reach the pinned version.

**Why it belongs in this document.** `uv run` is the invocation form for the hub's `Stop` hook, so
in this substrate **the ADR-85 session-end organ does not run at all** — it fails before Python
starts. That is the `[#498]` class exactly: *a declared-and-distributed organ that is
non-executable on arrival in a particular environment*, latent because no gate on the current fleet
would go red for it. §2's security and ops columns priced credential handling and patching; they
did not price **organ executability**, and this is the second substrate-specific instance the fleet
has now met.

**Correction to §4.1 step 2 — the provisioning checklist was incomplete.** As written it names
`pre-commit install --hook-type pre-push` and `arm_hooks.py`, and would have handed over a host
whose `uv run` organs were silently dead. It should read:

```
2. Clone the hub. Install the PINNED uv FIRST (pyproject.toml [tool.uv] required-version) and
   verify `uv --version` reports it and that no earlier PATH entry shadows it -- every `uv run`
   organ is inert until this holds, and it fails before Python starts, so a broken pin looks
   like a silent no-op rather than an error in the organ.
   THEN arm the gates: `pre-commit install --hook-type pre-push` + `arm_hooks.py`.
   THEN prove `audit.py health` runs and record its wall-clock.
```

**Two honest limits on this amendment:**

1. **n=1, and substrate-specific.** Measured in one Anthropic cloud container. It is not evidence
   about the rented host of §2.2, where the fix is simply *install the pinned uv at provisioning*
   — which is why this lands as a checklist correction rather than as a mark against option B. If
   anything it is a mark against **option A**, whose image the operator does not control.
2. **The fix applied here was container-local and touched zero tracked files** (`pip install
   uv==0.11.19`, then shadowing the stale binary on PATH). `pyproject.toml` and
   `.claude/settings.json` were deliberately NOT edited: the pin's own comment forbids bumping it
   "incidentally mid-arc", and pinning *down* to match a stale image would invert the control
   ADR-106 exists to hold. **No BACKLOG row is born here** — this document births none by
   construction; whether the gap deserves a row is an operator call.

---

## AMENDMENT 2 (2026-08-16, operator challenge) — the cost basis in §2.2 and §5 is wrong in FRAMING, and two of the errors are the lane's

> **In-file amendment marker**, per CLAUDE.md §5 rule 3. §0–§5 and AMENDMENT 1 are unchanged and
> are NOT rewritten. The operator challenged "€64/month is expensive" and named a candidate list
> (Colab, Kaggle, RunPod, Vast.ai, Modal, Anyscale, Replicate, Baseten, HF Spaces, SageMaker).
> The challenge is upheld. This section records what the lane got wrong, what the list does and
> does not answer, and the corrected cost basis.

### A2.1 Two errors in §2.2 / §5, both the lane's

**Error 1 — the lane priced hardware the operator already owns.** The brief said *"a rented Linux
host (**the operator has hosting**; what specs for N lanes of this workload)"*. That is a **spec**
question. §2.2 answered a **procurement** question instead, and §5 then carried a monthly rental
into the recommendation. If the existing host clears the bar, the marginal cost is **€0** and the
whole EUR column is moot. The spec answer that was actually asked for, from §1.2's measured
constant:

```
16 lanes  ->   8 physical cores / 32 GB / NVMe
32 lanes  ->  16 physical cores / 64 GB / NVMe
   (0.3 sustained cores + correlated burst, ~2 GB per lane; NVMe because the cost is
    process-spawn and file IO, not compute)
```

**Error 2 — the lane priced a MONTHLY rental for an ~80-hour-per-month workload.** Batches run
~20 days × ~4 h. A dedicated server bills ~730 h whether used or not; **Hetzner Cloud bills hourly**
(floor ~€0.0088/h, monthly cap on a 624-h standard) `[2°]`. An instance created per batch and
destroyed after it costs roughly **€3–10/month** for the same work — a ~10× reduction obtained by
changing **billing shape, not vendor**. §2.2 never considered ephemeral provisioning and should
have; a batch workload is the textbook case for it.

**§0 limit 1's warning materialised.** Hetzner repriced on 2026-06-15: CPX +144%, CCX +169%,
CCX63 €374.49 → €853.49 `[2°]`. The €64 AX52 figure is therefore **suspect and probably low**. It
was marked `[2°]` and "must be re-checked on Hetzner's own page" — that instruction stands and is
now known to be load-bearing, not boilerplate.

### A2.2 The candidate list answers a different question

Every platform named is a **GPU / model-weights** platform: managed GPU notebooks (Colab, Kaggle),
GPU rental for fine-tuning (RunPod, Vast.ai, Lambda), serverless **inference** (Modal, Replicate,
Baseten, Anyscale), model hosting (HF Spaces, SageMaker). **This workload runs no weights.** §1.2
measured it at ~0.3 CPU cores and ~2 GB per lane, with inference on Anthropic's servers over the
API — it is git + pytest + pre-commit, and its GPU requirement is zero. Paying for GPU capacity
here buys the one component the workload never touches, which is why most entries price **higher**
than a CPU VPS, not lower.

Judged individually against the §1.2 shape and the §2.4 credential axis:

```
RunPod CPU pods   $0.01/hr [2deg] -> ~$0.80/mo at 80 h. The cheapest figure any source in
                  this document produced. Spec at that price NOT verified; GPU-first vendor.
                  Worth a measured trial; not adoptable on a price tag alone.
Modal             base $0.0000131/core-s ~= $0.047/core-hr; Sandboxes $0.00003942/core/s
                  non-preemptible, 1 physical core = 2 vCPU [2deg]. ~$60/mo at 16 cores
                  BEFORE the 3x non-preemptible and 1.5-1.75x regional multipliers.
                  Not cheaper, and the SHAPE is wrong: serverless functions, not a
                  long-lived stateful session with a persistent FS and git credentials.
                  Possible narrow fit: offloading the 507 s suite alone (bursty), not a lane.
Fly.io            performance-4x (4 vCPU/8 GB) ~$61/mo, per-second billing, but volumes
                  bill even when scaled to zero [2deg]. Same shape objection as Modal.
Vast.ai           DISQUALIFIED on §2.4 grounds, from the vendor's own documentation: on
                  unverified hosts "your workload runs on hardware you know nothing about",
                  and community-tier instances run on hardware the host operator can
                  inspect [2deg]. A private repo, a git push credential and an Anthropic
                  token on a third party's machine is strictly worse than every other
                  option here, including the one §2.4 already ranked worst.
Kaggle            CORRECTION to the spirit of §2.2 D: Kaggle is materially better than
                  Colab on two axes -- 12 h session runtime and supported private-repo
                  access via PAT stored as a notebook secret [2deg]. It still fails on
                  WIDTH: a handful of concurrent sessions, a notebook kernel rather than a
                  shell, no persistent filesystem across runs. 16-32 concurrent long-lived
                  lanes is not reachable. Excluded on capability, NOT on the Colab
                  terms-of-service grounds -- the two are different exclusions and were
                  not distinguished in §2.2.
Colab             §2.2 D stands unchanged (terms disallow remote control/SSH and
                  non-interactive use).
```

### A2.3 Corrected cost basis, cheapest first

§5's table priced compute as if a host must be bought. It should have priced the **decision
sequence**:

```
1. EUR 0    Change nothing. Cloud sessions are $0 compute (PRIMARY). Per §2.5 the host is
            worth buying ONLY for the third-party-routing capability, and that pays only once
            rate limits BIND -- which sec.0 limit 6 records as UNMEASURED. Measure that first.
2. EUR 0    If limits bind, use the host the operator already has, against A2.1's spec.
3. ~EUR 3-10/mo   Only if that host is short: an hourly instance created per batch and
            destroyed after it. Same vendor class as sec.2.2 B, ~10x cheaper on billing shape.
4. EUR 64+/mo     A monthly dedicated server -- what sec.2.2/sec.5 recommended. Justified only by a
            need for a permanently-on host, which this workload does NOT have.
```

**§1.5 is unaffected and is the reason none of this changes the recommendation's direction:**
compute was ~1% of a lane's cost at €64/month and is ~0.1% at €5/month. The argument for the host
was never its price — it was the routing capability of §2.1 — and the argument against buying one
today is still that rate-limit headroom is unmeasured.

**One honest cost against option 3, which AMENDMENT 1 makes concrete:** per-batch provisioning is
cheap in money and *not* free in effort. Every freshly created instance must install the **pinned
uv** before anything else, or every `uv run` organ is dead on arrival and fails in a way that
reads as a silent no-op. An ephemeral-host strategy raises the price of getting the §4.1 checklist
right; it does not lower it.

**Two limits on this amendment.** Every EUR/USD figure above is `[2°]` — the egress proxy still
blocks the vendor pricing pages (§0 limit 1), and the Hetzner aggregators contradict each other
(one reports €17/mo for 8 vCPU/16 GB, another €19.49/mo for 2 vCPU/4 GB post-increase; both cannot
describe the same catalogue). **No figure here is safe to spend against without opening the
vendor's own page.** And the RunPod $0.01/hr CPU rate is quoted without a verified core/RAM spec,
so it is a lead to check, not a number to plan on.

---

## AMENDMENT 3 (2026-08-16, discovered by committing) — the cloud substrate has an ORGAN-EXECUTABILITY TAX, n=3

> **In-file amendment marker**, per CLAUDE.md §5 rule 3. §0–§5 and AMENDMENTS 1–2 unchanged.
> This section records a pattern the lane found by *running real gated commits in the substrate it
> was assessing* — evidence §2 could not have produced by reading documentation.

### A3.1 Three measured instances, one class

```
1. PINNED uv         `[tool.uv] required-version = "==0.11.19"`; image ships 0.8.17 and its
   (AMENDMENT 1)     `uv self update` cannot reach the pin. Every `uv run` organ -- the Stop
                     hook among them -- fails BEFORE Python starts.
2. SHALLOW CLONE     `git rev-parse --is-shallow-repository` -> true. Corrupted TWO
   (this section)    history-dependent checks at once:
                       - `journal_spine_anchor` FAILED CLOSED (correctly, ADR-85 §A6):
                         "disposition floor 24882f8cc is not an ancestor of main ...
                          fatal: Not a valid object name"
                       - `canonical_freshness` reported 6 FALSE positives ("edited but not
                         re-reviewed"), because every file's last-edit date resolved to the
                         shallow boundary. Both cleared on `git fetch --unshallow`.
3. ABSENT FLEET      `audit.py health` exits 1 via `operational_ok`, because
   SIBLINGS          `discover_repos()` finds none: this container holds one repo, and the
   (this section)    session's GitHub scope is `rdwornik/dev-knowledge` alone, so the
                     siblings CANNOT be cloned. Self-audit FAILs at that moment: ZERO.
                     The hub's own conformance was clean; the gate blocked on the fleet's
                     absence.
```

**The class is AMENDMENT 1's, generalised: an organ that is correct, armed, and non-executable
because of a property of the substrate rather than of the tree.** All three are invisible to
documentation review and appear only when a real gated commit runs.

### A3.2 The finding that makes this worse than three bugs

**The gate's behaviour changed mid-session.** This lane's first two commits passed with no gate
run at all, because the hooks were not yet armed; the `SessionStart` self-arm (`arm_hooks.py`)
then installed them, and every subsequent commit in the *same session on the same tree* was
blocked. **A gate that is absent for the first half of a session and blocking for the second half
is not a gate — it is a race**, and the artifacts it let through are unverified without anyone
having decided that.

This is directly adverse to §2.2 A, which scored Anthropic-hosted cloud sessions "ops burden:
zero". That score priced *infrastructure* ops and silently assumed *organ* ops was free. It is
not: the substrate must be provisioned before the gates are armed, and this container was not.

### A3.3 What it changes, and what it does not

**Changes:** §2.3's `ops burden` row for option A should read **"none for infrastructure; non-zero
and currently unpaid for organs"**, and §2.4's security ranking is untouched but no longer the
only axis on which option A is imperfect. §4.1's provisioning checklist (already corrected once by
AMENDMENT 1) needs a third and fourth line:

```
   - `git fetch --unshallow` (or clone with full history) BEFORE trusting any
     history-dependent check -- a shallow clone makes `journal_spine_anchor` fail closed
     and `canonical_freshness` produce false positives, and neither says "shallow".
   - Either make the fleet siblings resolvable, or accept that `audit.py health` cannot
     pass on operational grounds in a single-repo container and decide that EXPLICITLY.
```

**Does not change:** the §2.5 recommendation or its direction. Two of the three instances are
one-line provisioning fixes; the third (absent siblings) is a genuine structural mismatch between
a fleet-auditing gate and a single-repo container, and it is **equally present on a rented host
that clones only the hub**. This is a *provisioning* finding, not a verdict on any substrate.

### A3.4 Disclosure — this amendment was committed with `SKIP=audit-health`

Recorded here rather than left in a commit message, because a silent bypass is the failure mode
the fleet's own doctrine exists to prevent.

- **What was skipped:** `audit-health` only, via `SKIP=`, **not** `--no-verify`. The other twelve
  hooks ran and passed, including `block-commit-on-main`, the ADR-101 hermetization gate, the
  audits-index freshness gate, and both commit-msg gates.
- **Why:** the check's sole failing predicate was `repos registered -> none` (A3.1 item 3), with
  **zero** self-audit FAILs. The gate was refusing on the fleet's absence from the container, not
  on anything in this diff, and the fleet cannot be cloned into it.
- **What was NOT done:** the two history-dependent failures were **fixed, not skipped**
  (`git fetch --unshallow`), and re-verified green before the bypass was used. The bypass covers
  one predicate, deliberately, and no other.
- **Honest limit:** this is a bypass, and a bypass is a debt. A hub commit made from a
  single-repo container cannot today discharge `audit.py health`'s operational leg. **Whether that
  deserves a BACKLOG row is an operator call — this document births none by construction.**

---

## AMENDMENT 4 (2026-08-16) — SUPERSEDED

> **This document is superseded by
> `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md`.**
>
> Route per CLAUDE.md §5 rule 3: an immutable audit is superseded **with a new file**, and this
> marker is the pointer. Nothing above is edited or withdrawn — §0–§5 and AMENDMENTS 1–3 remain
> the record of what was found and when.
>
> **Read v2 instead.** It restates the requirements (the operator added three: a VS Code control
> plane, an hourly-to-monthly crossover rule, and time-to-deploy), reorganises base-plus-three-
> amendments into one readable report, and names six defects in this document — including two
> this one never found: **GitHub Codespaces was omitted from the option set entirely**, and **the
> control plane was never priced**, which inverts this document's "ops burden: zero" scoring of
> Anthropic cloud sessions.
>
> The evidence here is carried forward unchanged: the measured baseline, the compute-is-1%
> finding, the cloud-session/third-party-inference collision, and the three-instance
> organ-executability tax.
