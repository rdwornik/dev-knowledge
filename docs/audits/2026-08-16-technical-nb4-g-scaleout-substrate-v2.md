# NB4-G scale-out v2 — control plane, execution plane, and a deployment plan that starts this week

> **EXTERNAL EVIDENCE — advisory until ratified, never doctrine by virtue of existing.**
> **STATUS: DRAFT.** Decides nothing, adopts nothing, births no BACKLOG row. No config file,
> dependency, hook, protocol or routing table was edited by the lane that produced it.
> **SUPERSEDES** `docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate.md` (v1 + AMENDMENTS
> 1–3). v1 is immutable and stays on disk as the record; **this file is the one to read.**

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-16 · **Slug:** nb4-g-scaleout-substrate-v2
- **Lane:** `claude/nb4-scaleout-substrate-f8fhi1` (Anthropic cloud session, Linux container)
- **Base:** `main` @ `43cd1ce` · **Model:** Opus 5 · web search permitted · evidence only
- **Goal, in the operator's words:** maximise deployment efficiency, take load off the local
  Windows machine, stay scalable, be fast to deploy, start small and pay hourly during intensive
  work, move to monthly only when hourly crosses it — and **drive it all from VS Code**.

---

## 0. Why there is a v2 — self-critique of v1

v1 answered the three questions it was asked and got the *economics* right. It got the *problem*
wrong in six specific ways. Naming them is the point of this section; each one changed something
downstream.

```
D1  ANSWERED PROCUREMENT, NOT SPEC. The brief said "the operator has hosting; what SPECS for
    N lanes". v1 produced a shopping list. -> §4.1 now leads with the spec.
D2  PRICED MONTHLY FOR AN ~80-HOUR-PER-MONTH WORKLOAD. A batch host is idle ~89% of the
    month. v1 never considered ephemeral or hourly provisioning. -> §6 is built on it.
D3  OMITTED GITHUB CODESPACES ENTIRELY. The most obvious VS-Code-native, hourly-billed,
    private-repo-safe option was not in the option set. It became visible only when the
    operator named VS Code -- which means v1's option set was shaped by the questions asked
    rather than by the problem. -> §5.3.
D4  NEVER ASKED WHAT THE CONTROL PLANE WAS. v1 optimised compute and priced ops burden, but
    the operator has to WATCH 16-32 lanes and read their output. The human interface was
    treated as free. It is not free, and §5.4 shows it inverts a v1 conclusion.
D5  STRUCTURE. Base plus three appended amendments is not a report. A reader cannot get the
    answer in one pass, and the corrections contradict the body without replacing it.
D6  MISWEIGHTED. Model routing (v1 §3) got the most words and is the least urgent question --
    it is gated on a corpus run that has not happened. Substrate + control plane are what is
    blocking work today. -> routing is condensed to §8 and stays gated.
```

**What v1 got right and is carried forward unchanged:** the measured baseline (§2), the finding
that compute is ~1% of a lane's cost (§2.4), the cloud-session/third-party-inference collision
(§8.1), and the organ-executability tax (§7.3). Those are evidence, not framing, and they survive.

**Honest limits of v2** (they bound every number below):
1. **Vendor pricing pages remain blocked by the egress proxy.** Anthropic and VS Code docs are
   PRIMARY; GitHub, Codespaces, Hetzner, Groq, Moonshot and Google figures are `[2°]` secondary
   and **must be re-checked on the vendor's own page before spending**. Aggregators contradict
   each other — on Hetzner, one reports €17/mo for 8 vCPU/16 GB and another €19.49/mo for
   2 vCPU/4 GB post-increase; both cannot describe the same catalogue.
2. **No currency conversion is performed.** EUR and USD figures are kept in their own units. An
   invented FX rate would make the crossover table look more precise than it is.
3. **No lane-duration telemetry exists** (`[#529]` unlanded), so "≈2.5 h/lane" and "≈80 h/month"
   are derived from the 3h30m batch cap and observed batch cadence, not measured. **This is the
   largest error term in §6 and §7.**
4. **Nothing here has been run on the target substrate.** Every deployment time in §6 is an
   estimate, labelled as such.

---

## 1. Requirements, restated as testable statements

Seven, from the operator's brief. Each is checkable, so §9 can score the design against them
rather than asserting success.

```
R1  Take load off the local Windows machine          measurable: local CPU during a batch
R2  Scale to 16-32 concurrent lanes                  measurable: lanes completed per batch
R3  Fast to deploy                                   measurable: hours to first green lane
R4  Start small; pay hourly during intensive work    measurable: first month's invoice
R5  Move to monthly ONLY when hourly crosses it      measurable: a stated crossover rule
R6  Drive and observe everything from VS Code        measurable: one window, all lanes visible
R7  Scalable + clean architecture                    measurable: swap one plane, others unchanged
```

**R5 is the requirement that shapes the answer**, and it turns out to have a vendor whose pricing
model implements it for free (§7.2).

---

## 2. The measured baseline (carried from v1, unchanged)

Measured in this container, on this tree, today — 4 vCPU / 15 GB / Linux:

```
audit.py health           19.0 s      (the pre-commit gate, on EVERY commit)
pytest -m "not slow"     507.4 s      (-n auto = 4 workers; 2895 tests collected)
derived CPU work        ~2030 CPU-s  ~= 34 CPU-min per full suite run
cross-check              night-3 lane measured 485 s and 957 s in the same container class
```

**Sizing constant: ≈0.3 sustained cores + ~1.5–2 GB RAM per lane, bursting to ~1 core.**

**Why the local machine saturates, arithmetically:** 12 lanes × 0.3 = 3.6 sustained cores bursting
toward 12, on a Ryzen Pro mobile part with ~8 threads. At burst that is ~1.5× oversubscribed, and
every lane's 19 s gate queues behind every other lane's. A 19 s gate stretching to ~1 h is a ~190×
factor — that is oversubscription plus Windows `CreateProcess` cost, not a mystery. **R1 is
therefore not a preference; it is the fix for a measured resource exhaustion.**

### 2.4 The economic fact that governs every decision below

```
model spend per lane-hour     ~$8 - $18   (model-priced, from logs/TOKEN-LOG.md)
compute per lane-hour         ~EUR 0.08   (hourly VPS, §7)
ratio                         ~100:1 to ~200:1
```

**Compute is ~1% of a lane's true cost.** Optimising the substrate for price is optimising the
wrong term. Optimise it for **wall-clock, rate-limit headroom, and operator visibility** — which
is exactly what R1/R2/R6 ask for, so the requirements and the economics agree.

---

## 3. Clean architecture — three planes, independently swappable

The design fault in v1 was treating this as one question ("where do lanes run"). It is three, and
separating them is what makes R7 satisfiable.

```
CONTROL PLANE     what the operator sees and steers
                  VS Code (Remote-SSH or Tunnel) + Claude Code extension + terminals
                  -> swappable for: browser claude.ai, mobile app, plain ssh+tmux

EXECUTION PLANE   where lanes actually run
                  ONE Linux host, N git worktrees, N `claude` processes
                  -> swappable for: Codespaces, Anthropic cloud sessions, a bigger host

ORCHESTRATION     what decides which lane runs what, and merges the result
                  the EXISTING batch protocol: contracts, /lane-boot, /lane-integrate,
                  single-flight guard [#530], grammar gate, merge queue
                  -> UNCHANGED. This is the asset; the other two planes serve it.
```

**Three invariants that keep the planes separate** (each is the reason a future swap stays cheap):

1. **The orchestration plane never learns where it runs.** Contracts, gates and the merge queue
   are substrate-agnostic today and must stay so. Nothing in §6 edits them.
2. **The environment is a portable artifact, not a host.** A `devcontainer.json` +
   provisioning script is the unit of reproducibility. The same definition runs in Codespaces, on
   a rented host, and locally — which is what makes §6's day-1 step non-throwaway.
3. **Git mutations stay serial in one thread.** The merge queue and `/lane-integrate` are not
   parallelised by this design and must not be. Parallel writers on one tree corrupt each other
   (PLAYBOOK), and `[#530]`'s guard arbitrates on `origin`.

---

## 4. Execution plane — the spec, then the host

### 4.1 The spec (this is what the brief actually asked for — D1)

From §2's measured constant, at 0.5 core/lane sizing headroom and ~2 GB/lane:

```
16 lanes   ->   8 physical cores / 32 GB RAM / NVMe / Linux
32 lanes   -> 16 physical cores / 64 GB RAM / NVMe / Linux
```

**NVMe is not a luxury here.** The workload is process-spawn and file IO (2,895 tests, hooks per
commit, worktree checkouts), not compute. Spinning or network storage would undo the gain.

**Check the host you already have against this first.** If it clears the 16-lane row, R4's answer
is €0 and §6 skips straight to provisioning.

### 4.2 One big host beats many small ones — and R6 is why

v1 never compared these because it never priced the control plane (D4):

```
                        ONE host, N worktrees        N separate instances/codespaces
VS Code (R6)            ONE window, N terminals       N windows -- unmanageable at 16-32
shared pip/uv cache     yes -- built once             no -- N times the setup cost
merge queue             local, serial, no network     cross-host coordination needed
cost                    one instance, hourly          N instances
failure blast radius    all lanes on one box          isolated per lane
```

**R6 decides it.** "One pane of glass over 16–32 lanes" is reachable with one host and a terminal
multiplexer; it is not reachable with 32 VS Code windows. The isolation advantage of N instances
is real but is already provided at the right layer — **git worktrees**, which the batch protocol
already uses.

---

## 5. Control plane — VS Code (R6)

### 5.1 The two ways to point VS Code at a remote host

Both are first-party and free; the difference is the network model.

```
Remote-SSH        VS Code opens an SSH connection to a host you control. "If you need raw
                  speed and network control, go with SSH" [2deg]. Needs a reachable SSH
                  port and key management.
Remote Tunnels    Run the VS Code CLI on the remote machine, authenticate with GitHub;
                  traffic goes through Microsoft dev tunnels. "without opening inbound
                  firewall ports or maintaining VPN profiles" [2deg]. Also reachable from
                  vscode.dev in a browser -- so the same host is steerable from a machine
                  with no VS Code installed.
```

**Recommendation: start with Remote Tunnels, keep Remote-SSH as the fallback.** Tunnels remove
the inbound-port and key-distribution problem entirely, which is the part most likely to burn a
day of R3's budget. If throughput disappoints, Remote-SSH is a config change, not a redesign —
that is invariant 1 doing its job.

### 5.2 What the operator actually sees

```
VS Code window (Remote Tunnel -> the batch host)
  |- Explorer            all N worktrees, one tree, real files
  |- Terminals           one per lane (tmux/screen-backed so they survive a disconnect)
  |- Claude Code ext.    side-by-side diff viewer, tabbed session history, prompt history,
  |                      docked in the secondary sidebar [2deg]
  |- Source Control      per-worktree git state
  '- Output/logs         per-lane log files, greppable in one place
```

The Claude Code extension is what makes this a *control* plane and not just a file browser: it
gives per-change accept/reject diffs and session history in the same window as the code `[2°]`.

**Terminals must be multiplexer-backed.** A VS Code terminal dies with the connection; a 2.5-hour
lane must not. This is one `tmux new-session -d -s lane-<x>` per lane in the provisioning script —
cheap, and the difference between "observable" and "lost on a Wi-Fi blip".

### 5.3 GitHub Codespaces — the option v1 omitted (D3)

The most VS-Code-native option available, and it was missing from v1's option set.

```
billing        $0.18 per core-hour + $0.07 per GB-month storage [2deg]
               -> 2-core = $0.36/h ; 4-core = $0.72/h ; 8-core = $1.44/h
free tier      120 core-hours + 15 GB/month on personal accounts [2deg]
               -> 60 h/month on a 2-core machine, free
gotcha         STORAGE BILLS WHILE STOPPED. A forgotten codespace costs money doing nothing.
start-up       prebuilds cut creation time "by up to 95%"; GitHub's own guidance is that a
               repo taking >2 min to create a codespace benefits from prebuilds [2deg]
security       GitHub-native private-repo access; no credential of the operator's on a box
               he must patch
VS Code        native -- desktop or browser, no tunnel or SSH setup at all
```

**Verdict: the fastest possible R3, and the wrong steady state for R4.** At ~80 h/month a 4-core
codespace is ~$57.60 + storage against ~€3–6 for the equivalent hourly VPS (§7.1) — roughly an
order of magnitude. But it needs **zero** infrastructure work, which makes it the right *day-1*
substrate (§6.1). The free tier alone (60 h/month on 2 cores) covers a proof run at zero cost.

### 5.4 The finding that inverts a v1 conclusion

v1 §2.2 scored Anthropic-hosted cloud sessions "ops burden: **zero**" and recommended them as the
default. Under R6 that score is wrong, for a reason v1 could not see because it never asked D4:

**Anthropic cloud sessions have no VS Code control plane over the running lane.** They are steered
from claude.ai, the mobile app, or `claude -p --cloud <id>`; `--teleport` pulls a session into a
local terminal, but that is a *handoff*, not a live pane of glass over 32 concurrent lanes. For
R6, a host the operator can point VS Code at is a **capability**, not a convenience.

This does not make cloud sessions bad — they remain the best on credential security and cost $0
compute. It means **they are not sufficient alone**, and the rented host earns its place on a
second independent ground beyond the third-party-routing capability v1 identified (§8.1).

---

## 6. Deployment plan — start this week (R3, R4)

Three stages. **Each is independently useful, and each is reversible without touching the
orchestration plane.**

### 6.1 Stage 1 — day 1, cost ≈ €0, effort ~2–4 h

**Goal: prove one lane runs green off the local machine, with the fewest moving parts.**

```
1. Write `.devcontainer/devcontainer.json` + a provisioning script. THIS IS THE DELIVERABLE
   of stage 1 -- it is the portable artifact (invariant 2) that stages 2 and 3 reuse
   unchanged. It must, in this order:
     a. install the PINNED uv (pyproject.toml [tool.uv] required-version) and assert
        `uv --version` matches AND no earlier PATH entry shadows it
     b. clone with FULL history, or `git fetch --unshallow`
     c. `uv sync` the dev group; `pre-commit install -t pre-commit -t commit-msg -t pre-push`
     d. run `python scripts/audit.py health` and RECORD its wall-clock
2. Open the repo in a GitHub Codespace (free tier, 2-core). Zero infrastructure.
3. Run ONE real lane end to end. Measure: gate wall-clock vs the Windows figure.
```

**Why Codespaces first:** it removes every variable except the devcontainer itself. If stage 1
fails, the failure is in the definition, not in a host, a firewall or an SSH key.

**Exit criterion:** one lane green, `audit.py health` wall-clock recorded, devcontainer committed.

### 6.2 Stage 2 — week 1, cost ≈ €3–10/month, effort ~2–4 h

**Goal: the real execution plane, at the 16-lane spec, driven from VS Code.**

```
1. Create ONE hourly cloud instance at the §4.1 16-lane spec (8 cores / 32 GB / NVMe).
2. Run the SAME provisioning script from stage 1. Nothing is rewritten.
3. Install the VS Code CLI and start a Remote Tunnel; connect from the desktop VS Code.
4. Provision N worktrees, one tmux session per lane.
5. Run a REAL batch at width 8-12 -- the width already proven -- not at 32.
6. SNAPSHOT the instance. Every later boot is minutes, not hours.
```

**Exit criterion:** a full batch completes on the host, observed end to end from one VS Code
window, with the local machine idle.

### 6.3 Stage 3 — month 1, widen and decide

```
1. Widen to 16, then 32 lanes, measuring wall-clock and failure rate at each width.
2. Apply the §7.2 crossover rule to the first invoice.
3. ONLY THEN consider model routing (§8) -- and only if rate limits are the binding
   constraint, which is still unmeasured.
```

### 6.4 Time-to-deploy, honestly

Estimates, not measurements (limit 4):

```
stage 1   ~2-4 h   dominated by writing the devcontainer, not by infrastructure
stage 2   ~2-4 h   provisioning + tunnel + worktrees; near-zero afterwards via snapshot
stage 3   ongoing  measurement, not building
```

**Total to a working off-machine batch: roughly one working day, spread over a week.** The single
biggest risk to that estimate is the provisioning script's step (a) — the pinned-uv trap in §7.3,
which cost this lane a blocked commit and would otherwise cost a confusing afternoon.

---

## 7. Cost model and the crossover rule (R4, R5)

### 7.1 Cost at realistic usage

Batch usage estimated at ~20 batch-days × ~4 h ≈ **80 host-hours/month** (limit 3). Table given
across a range because that estimate is the weakest input.

```
hours/month                40h      80h      160h     320h     624h+
Hetzner Cloud, ~EUR 25/mo cap    EUR 1.60  3.21     6.41    12.82    25.00 (CAPPED)
Hetzner Cloud, ~EUR 50/mo cap    EUR 3.21  6.41    12.82    25.64    50.00 (CAPPED)
Codespaces 2-core ($0.36/h)      $ 14.40  28.80    57.60   115.20   224.64  (+storage)
Codespaces 4-core ($0.72/h)      $ 28.80  57.60   115.20   230.40   449.28  (+storage)
Anthropic cloud sessions            $0       $0       $0       $0       $0   (rate limits only)
```

All EUR/USD figures `[2°]`; no conversion performed (limit 2). Hetzner hourly derived as
monthly ÷ 624 from their stated billing standard `[2°]`.

### 7.2 The crossover rule — and the vendor that implements it for you

R5 asks for "hourly until it exceeds monthly, then monthly". The rule is arithmetic:

```
hourly is cheaper while:   H  <  P_monthly / P_hourly
```

**Hetzner Cloud already applies this automatically.** Their hourly rate is the monthly price
÷ 624 with a monthly cap `[2°]`, so the crossover sits at **624 hours/month (~85% of the month)**
and you are billed the lower of the two **without making a decision or migrating anything**.

**This is the strongest single argument in the report for that vendor class**, and it is an
architectural property, not a discount: R5 is satisfied by construction, so there is no rule to
remember, no invoice to watch, and no migration to schedule. At the estimated 80 h/month the host
costs ~13% of its own monthly price.

**Codespaces has no cap**, so its crossover must be watched manually — and at any realistic usage
it is already past it. That is why §6 uses it for stage 1 and then leaves.

**Explicit trigger for the one decision that remains:** if measured usage exceeds **~500 h/month**
(approaching the cap and therefore approaching a permanently-on host), stop treating the instance
as ephemeral and buy the dedicated box — at that point a dedicated server gives more hardware per
euro than a capped cloud instance.

### 7.3 The cost line nobody budgets — organ executability

Three measured instances, all found by running real gated commits in a cloud container:

```
1. PINNED uv        image ships 0.8.17 vs the repo's ==0.11.19; `uv self update` cannot reach
                    the pin. Every `uv run` organ -- the Stop hook included -- fails BEFORE
                    Python starts, so it reads as a silent no-op rather than an error.
2. SHALLOW CLONE    corrupted TWO history-dependent checks at once: journal_spine_anchor
                    failed closed (correctly, ADR-85 §A6) and canonical_freshness produced
                    6 FALSE "edited but not re-reviewed" positives. Both cleared on
                    `git fetch --unshallow`.
3. ABSENT SIBLINGS  `audit.py health` exits 1 via operational_ok because discover_repos()
                    finds none -- with ZERO self-audit FAILs. A single-repo container cannot
                    discharge the fleet leg of the hub's own health gate.
```

**And the sharpest one: the gate changed behaviour mid-session.** This lane's first two commits
ran no gate at all (hooks unarmed); `arm_hooks.py` then installed them and every later commit
blocked — same session, same tree. **A gate absent for half a session and blocking for the other
half is a race, not a gate.**

**Consequence for §6:** items 1 and 2 are one-line fixes *in the provisioning script* and cost
nothing once written — which is precisely why stage 1's deliverable is the script and not a host.
Item 3 is a genuine structural mismatch between a fleet-auditing gate and a single-repo host, it
is **equally present on a rented host**, and it needs an explicit operator decision rather than a
workaround.

---

## 8. Model routing — condensed, and still gated (D6)

### 8.1 The structural fact that ties routing to substrate

Primary, from Anthropic's docs: cloud sessions are *"not available when Claude Code is configured
for … another third-party provider"*, and self-hosted environments *"use the Anthropic API, and
inference can't be routed through … an LLM gateway"*. **Every cloud-session substrate forecloses
third-party model routing.** Only a host the operator controls can run a producer lane on a
different backend via `ANTHROPIC_BASE_URL`. The §6 host therefore earns its place twice: once for
R6 (§5.4), once for routing optionality.

### 8.2 The correction that matters more than any price table

On a Max subscription, model tokens are **$0 at the margin** until a rate limit is hit. Routing a
producer to Kimi/Groq/Gemini **converts a free token into a billed one**. Routing buys
**rate-limit headroom and vendor independence — not cost reduction.** Anyone reading it as a
savings measure has it backwards.

### 8.3 Prices, and the gate

Anthropic PRIMARY; all others `[2°]`. Per Mtok, input/output:

```
Claude Opus 5   $5 / $25      Kimi K3 (Moonshot)  $3 / $15   (cache hit $0.30)
Claude Sonnet 5 $2 / $10      Kimi K2 (Groq)      $1 / $3
Claude Haiku    $1 / $5       Gemini 3.1 Pro      $1 / $6
                              GPT-5.6 Luna        $0.20 / $1.20
```

Kimi K3 at 0.6× Opus 5 does not justify a second harness on price. The genuinely cheap producers
are Kimi K2 on Groq, Gemini 3.1 Pro and GPT-5.6 Luna.

**Roles, not vendors. ARCHITECT and INTEGRATOR are never routed** (one decides what is true, the
other touches `main`). **PRODUCER (M)** — frozen, mechanical contracts — is the only tier worth
routing first, because a wrong producer fails visibly in the gate rather than latently in a
judgement.

**Gate, unchanged and not softenable:** a candidate moves only after it (1) runs NB4-A's
seeded-defect corpus on the **same diffs** as the baseline with its catch rate recorded, (2)
completes one real lane under the full armed gate stack with no `--no-verify` and no `SKIP=`,
(3) names its backend and model id in its packet, and (4) has its result recorded pass **or** fail.
`[#492]`'s ruling already governs this: *entry by measured acceptance, never vibes*.

---

## 9. Self-assessment — scoring this design against §1, and what would falsify it

```
R1 off-load local        MET by construction (stage 2). Verify: local CPU idle during a batch.
R2 16-32 lanes           MET at spec (§4.1) on the §2 constant. UNVERIFIED above width 12 --
                         §6.3 widens incrementally rather than assuming.
R3 fast to deploy        ~1 working day, ESTIMATED not measured (limit 4). Stage 1 is
                         deliberately zero-infrastructure so a slip is diagnosable.
R4 start small / hourly  MET: stage 1 ~EUR 0 (free tier), stage 2 ~EUR 3-10/month.
R5 crossover rule        MET, and better than asked: the Hetzner-class 624-h cap applies it
                         automatically. Explicit manual trigger at ~500 h/month for the
                         dedicated-box decision.
R6 VS Code control       MET via Remote Tunnel + Claude Code extension + tmux-backed
                         terminals. THE WEAKEST-EVIDENCED CLAIM HERE -- see below.
R7 clean / scalable      MET by the three-plane split; orchestration is untouched by every
                         stage, which is the test.
```

### 9.1 The three things most likely to be wrong

1. **R6 is designed, not demonstrated.** No one has driven 16–32 tmux-backed lanes through one VS
   Code Remote Tunnel window. The failure mode is not cost — it is a window that becomes unusable
   somewhere between 8 and 32 terminals. **Stage 2 runs at width 8–12 specifically to find this
   before committing to 32**, and the fallback (plain `ssh` + `tmux`, logs greppable in one place)
   is deliberately kept alive.
2. **Every price is secondary-sourced, and one vendor just repriced hard.** Hetzner raised cloud
   prices on 2026-06-15 (CPX +144%, CCX +169%) `[2°]`, which is exactly the class of movement that
   invalidates a table. **The 624-h cap is a pricing-model property and survives a price change;
   the absolute numbers may not.** Re-check before spending.
3. **~80 h/month is an estimate on top of an estimate.** If real usage is 300 h/month, stage 2
   costs ~€12–26 instead of ~€3–6 — still trivial against §2.4's model spend, so the *decision*
   is robust even where the *number* is not. That asymmetry is the reason to proceed now rather
   than measure first.

### 9.2 Pre-registered kill criteria

```
STAGE 1 fails   if one lane cannot run green in a Codespace from the devcontainer alone.
                -> the definition is wrong; fix it before renting anything.
STAGE 2 fails   if the host's gate wall-clock is NOT materially better than Windows on the
                same tree, after two batches. -> the substrate premise is falsified; keep
                Anthropic cloud sessions and drop the host. R6 alone does not justify it.
STAGE 3 fails   if failure rate rises with width. -> the ceiling is the batch protocol, not
                the host, and more hardware will not fix it.
ROUTING fails   if a candidate misses the corpus baseline. -> record the refusal and stop.
```

### 9.3 What this document deliberately does not do

It **births no BACKLOG row**, adopts nothing, and edits no config, hook or protocol. §8's routing
table is a draft for ratification. The one item genuinely needing an operator word is §7.3 item 3
— whether a single-repo host is allowed to skip `audit.py health`'s fleet leg, or whether the
fleet must be resolvable wherever the hub is committed from. **That is a governance question, not
an infrastructure one, and it is the only thing in this report that cannot be settled by
measurement.**

---

## Sources

**Primary (fetched this session):**
[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) ·
[Self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments) ·
[Routines](https://code.claude.com/docs/en/routines) ·
[Enterprise deployment overview](https://code.claude.com/docs/en/third-party-integrations) ·
[Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) ·
[VS Code Remote Tunnels](https://code.visualstudio.com/docs/remote/tunnels) ·
in-repo measured: `scripts/audit.py health` (19.0 s), `pytest -m "not slow"` (507.4 s),
`logs/TOKEN-LOG.md`, `protocols/ENVIRONMENT.md`,
`docs/audits/2026-08-15-technical-night3-research.md`

**Secondary `[2°]` — re-verify on the vendor's page before spending:**
[Codespaces pricing](https://toolradar.com/tools/github-codespaces/pricing) ·
[Codespaces prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds) ·
[Hetzner cloud price increases 2026](https://northflank.com/blog/hetzner-cloud-server-price-increases) ·
[Hetzner price adjustment 15 June 2026](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) ·
[Hetzner AX102](https://www.hetzner.com/dedicated-rootserver/ax102/) ·
[GitHub Actions 2026 pricing](https://github.com/resources/insights/2026-pricing-changes-for-github-actions) ·
[Remote-SSH vs Tunnels](https://www.codegenes.net/blog/what-is-the-difference-between-vscode-remote-ssh-and-remote-tunnel-connections/) ·
[Claude Code VS Code extension guide](https://www.eesel.ai/blog/claude-code-vs-code-extension) ·
[Groq pricing](https://www.cloudzero.com/blog/groq-pricing/) ·
[Kimi K3 pricing](https://www.eesel.ai/blog/kimi-k3-pricing) ·
[Gemini API pricing](https://benchlm.ai/google/api-pricing) ·
[Codex rate card](https://help.openai.com/en/articles/20001106-codex-rate-card)
