# Lane aa-14 — resource lifecycle: two regimes, measured

Consumers: `[#792]` (the organ this evidence specifies), `[#791]` (intake 101's carrier — its
response measure names the four BEFORE figures below and says they come from this lane),
`ecosystem/quality-requirements.yaml` (the five upstream entries and the two reproduced ones
cite this file as their evidence), `[#746]` (the Codespace-substrate answer in §6).

**Lane:** `lane-aa-14-resource-lifecycle` · **Contract:** `LANE-aa-14-resource-lifecycle.md`,
frozen, superseding the withdrawn `LANE-aa-13-…` (verified at 0 commits ahead of `main`).
**Taken:** 2026-09-15, 12:20Z–12:40Z. **Box:** `HYB-zToF5wlOa8g`, Windows 11, 27.67 GB RAM.

> **What this file is.** Evidence, taken before anything was built, so that the mechanisms in
> `[#792]` are specified by measurement rather than by a plausible constant. Where a figure
> could not be taken it says so and names what would make it takeable. Three of the contract's
> own premises are **corrected** here — §2.3, §3.2, §5.3 — and one is **confirmed** (§4.1).

---

## 1. Conditions at the time of measurement

Stated first because every figure below is relative to them.

```
sampled          2026-09-15T12:33:05Z .. 12:33:58Z
total RAM        27.67 GB
free RAM          1.62 GB          <- the register's "1.4 GB free of 28 GB" condition, live
claude processes     62            holding 12.53 GB
  heavy class        31            mean 287.0 MB   (the session process)
  light class        31            mean 126.3 MB   (its helper)
non-Claude        13.52 GB         = 27.67 - 12.53 - 1.62
live worktrees       11            (1 primary + 10 lanes/agents)
```

The 31/31 split is exact and is the unit that matters: **one seat is one heavy process plus one
light one, 413.3 MB together.** A per-PROCESS figure (207.2 MB) would double the ceiling and be
wrong; the contract's "~392–400 MB per lane" is a per-SEAT figure and is confirmed at 413 MB.

Independent corroboration, found while auditing reap records: an unrelated live job's
`state.json` carries `"detail": "triaging F-mark failures, 62 claude.exe at 12.65GB"` — the same
count and 0.12 GB from the same total, sampled by a different seat.

---

## 2. The thesis, derived rather than asserted

The contract's thesis is that **context reclamation and session replacement are different
mechanisms**, because the growth they address has different drivers. That is a claim about two
quantities. Both were tested, each against the instrument that can see it.

### 2.1 Per-turn COST is driven by TURN COUNT, not by elapsed time

Corpus: 681 hub-slug session transcripts (≥ 40 turns, ≥ 200 KB) under `~/.claude/projects`,
92,743 priced turns, deduplicated on `message.id`. Cost is `usage` counts × the rates in
`ecosystem/provider-registry.yaml` resolved through `provider_registry.resolve_rate`; no rate
literal was used. Each turn is expressed as a ratio to **its own session's median turn cost**,
never to a fleet constant.

By elapsed session time:

```
elapsed (min)   n turns   median cost / own median   ctx tokens/call (median)
        0-15     19101                      0.722                    109,712
       15-30     13361                      0.892                    167,673
       30-60     20339                      1.005                    220,733
      60-120     19085                      1.103                    288,258
     120-240     12720                      1.139                    330,062
     240-480      4692                      1.205                    355,586
        480+      7074                      1.186                    340,158
```

By turn index, holding nothing:

```
turn index        n   median cost / own median   ctx tokens/call (median)
      0-25    16141                      0.701                    100,662
     25-50    15806                      0.868                    152,395
    50-100    22121                      0.987                    208,363
   100-200    23015                      1.118                    294,560
   200-400    14713                      1.156                    358,583
      400+     4629                      1.247                    350,757
```

**The discriminating leg** — turn index HELD in the band 50–100, elapsed allowed to vary. If
cost were time-driven, a slow session's 60th turn would cost more than a fast session's 60th:

```
elapsed at turn        n   median cost / own median   ctx tokens/call
      0-30 min      6274                      0.915           184,611
     30-90 min     12815                      1.004           214,856
    90-240 min      2379                      1.030           241,325
      240+ min       653                      1.003           247,238
```

Cost moves 0.915 → 1.003 across an eight-fold spread in elapsed time once turn count is held —
essentially flat past the first half-hour. Across turn index, unheld, it moves 0.701 → 1.247.

**Conclusion: cost per turn tracks accumulated context, not wall-clock age.** A session that
sits idle does not become more expensive per turn. So clearing context genuinely reclaims cost,
and **context reclamation is aimed at the right quantity.**

### 2.2 Process MEMORY is driven by session AGE, not by turn count

The transcripts cannot answer this, and §3.2 records why. It was measured live instead, on the
heavy (session) process class, n=31, one cross-sectional sample:

```
process age      n    mean RSS    max      min
  0  - 0.5 h    21     255.6 MB   266.4    246.9
  0.5- 1   h     4     383.0 MB   393.6    377.7
  1  - 2   h     2     351.8 MB   393.9    309.7
  2  - 4   h     1     381.0 MB   381.0    381.0
  4  - 8   h     3     303.7 MB   386.5    251.1

pearson r (all 31)           0.264    slope  8.7 MB/h
pearson r (age < 4.5 h, n=30) 0.440   slope 21.4 MB/h
```

The 0–0.5 h band is remarkably tight — 21 processes inside a 19.5 MB spread — and the step to
0.5–1 h is a **50% rise, 255.6 → 383.0 MB**, after which it plateaus at roughly 350–385 MB.
The rise is FRONT-LOADED: it happens inside the first hour and does not continue linearly.

**So the two quantities have different drivers, and the thesis holds with a derivation behind
it: cost is context-based, memory is age-based. One mechanism cannot address both.**

### 2.3 CORRECTION: the unbounded idle growth is NOT reproduced on this box

The digest's §1 reports idle sessions reaching ~15 GB each over 18 hours. **Nothing resembling
that was observed here.** The largest single claude process across 62 was 393.9 MB; the oldest
(11.83 h) was at 161.6 MB; the 4–8 h band averages 303.7 MB and is *below* the 0.5–1 h band.

This does not refute the upstream reports — a different Claude Code version, a different
workload, or a condition not present today would all explain it. It refutes the inference that
the shape is currently live here. **The mechanism in `[#792]` is therefore specified against the
measured plateau (~385 MB) and not against 15 GB**, and the plateau is what its threshold uses.

Recorded so that a future seat reading "idle sessions reach 15 GB" against this repo's own
surfaces finds the measurement that disagreed, rather than re-deriving it.

---

## 3. The two thresholds: one derived, one reported underivable

### 3.1 DERIVED — the context-reclamation trigger

The contract asks for a trigger on "cost per turn rising against the seat's OWN median". Stated
as a rule — *a turn at ≥ X × the session's own running median (over its first 20 turns and
after), sustained 5 consecutive turns* — and counted against all 681 sessions:

```
    X     fires in         %      median first fire
 1.10   575 / 681      84.4 %     turn 37, elapsed 21 min
 1.20   475 / 681      69.8 %     turn 51, elapsed 30 min
 1.30   357 / 681      52.4 %     turn 68, elapsed 43 min
 1.50   149 / 681      21.9 %     turn 83, elapsed 53 min
 2.00     6 / 681       0.9 %     turn 60, elapsed 38 min
```

**Derived value: X = 1.30.** The derivation is the shape of that table, not a preference.
X = 1.10 fires in 84% of sessions — it is not a signal, it is the normal curve, and a trigger
that fires almost always reclaims at random. X = 2.00 fires in 0.9% and is a rule that never
runs. X = 1.30 is the knee: it separates half the corpus, and its median first fire (turn 68,
43 min) sits where §2.1's own-median curve has crossed 1.0 and is still climbing, so the trigger
fires while the cost it names is still rising rather than after it has plateaued.

**Honest limit, stated because the contract asks for it.** The trigger's specification says
"while the work class is unchanged"; **work class is not controlled for in this derivation**,
because no transcript field carries it. The confound is real: a session's late turns may be
genuinely more expensive work. What makes the number survivable anyway is §2.1's held leg —
holding turn index flat removes almost all of the rise, which is what a context-accumulation
explanation predicts and a work-class explanation does not. A seat that wants to remove the
confound entirely must record a work-class tag per turn, which nothing does today.

### 3.2 REPORTED UNDERIVABLE — the RSS threshold, from transcripts

The contract states the RSS threshold is "computable from the transcripts we hold" and directs
that it be computed rather than guessed. **It is not computable from them, for two independent
reasons, and both were checked rather than assumed.**

**Reason 1: transcripts record no memory figure at all.** Every key on every record type in a
5,577-record transcript was enumerated. The record types are `agent-setting`, `mode`,
`permission-mode`, `file-history-snapshot`, `system`, `atis-latch`, `attachment`, `user`,
`last-prompt`, `assistant`, `ai-title`, `agent-name`, `queue-operation`, `cost-state`,
`file-history-delta`. The `usage` block carries `input_tokens`, `cache_creation_input_tokens`,
`cache_read_input_tokens`, `output_tokens`, `output_tokens_details`, `server_tool_use`,
`service_tier`, `cache_creation`, `inference_geo`, `iterations`, `speed`. **No RSS, no heap, no
process-memory field exists.** The `rss` / `heap` / `memory` substrings that do appear are
English inside message content.

**Reason 2: the prescribed proxy has no signal.** The contract's derivation method is "the point
where per-turn latency rises measurably against the session's own median". That was computed —
latency taken as the gap between a `tool_result` user record and the assistant record that
answers it, which is model time with no human in it (24 gaps over 600 s excluded as stalls):

```
elapsed (min)   n turns   median latency / own median    p75     p90
        0-15     18409                        0.995    1.700   3.353
       15-30     13149                        1.001    1.797   3.249
       30-60     19885                        0.999    1.745   3.073
      60-120     18422                        0.994    1.725   3.004
     120-240     11972                        0.999    1.767   2.948
     240-480      4384                        1.041    1.864   2.955
        480+      6522                        1.025    1.723   2.653
```

**Flat to eight hours and beyond, at the median, p75 and p90 alike.** There is no point at which
latency rises measurably, so there is no point to locate a threshold at. The digest's §1 item 3
("long sessions degrade over ~30 minutes") is **not observable in 92,743 turns on this box** by
this instrument.

**Where the evidence stops.** The instrument sees MODEL response latency. If the degradation is
client-side — UI responsiveness, the whole-file transcript read of §5, tool dispatch — this
measurement cannot see it and does not claim to. The correct statement is: *no server-side
latency degradation with session age*, not *no degradation*.

**What IS supportable, and what would make the real figure takeable.** §2.2's live sample gives
a cross-sectional RSS-vs-age curve with a knee at ~0.5 h and a ~385 MB plateau. That is one
snapshot of 31 different sessions doing different work — it is not a longitudinal trace of one
session, and a snapshot cannot distinguish "processes grow" from "older processes are a
different population". **What would make it takeable is a sampler that records (pid, seat, RSS,
turn count) on a fixed interval**, so the same process is followed across its own life. That
sampler is `resource_lifecycle.py sample`, and this lane builds it — but a sampler that has not
yet run has no history, so the threshold it will support does not exist today and is not
claimed. The retirement predicate therefore ships with its **lifetime** and **merge-count** legs
derived (§3.3) and its **RSS** leg set to the measured plateau with its provenance recorded as
cross-sectional, to be re-derived from the sampler's own history once there is any.

This is the contract's "if the transcripts cannot support a threshold, say so and report what
they can support", answered as asked.

### 3.3 DERIVED — the session-lifetime leg

Session spans across the same 657 sessions:

```
median                88.0 min
p90                  477.3 min   (7.96 h)
max                15739.4 min   (262.3 h = 10.9 days, 75 turns)
over  2 h      256 sessions
over  6 h       77
over 12 h       36
over 24 h        8
```

**The contract says "the dispatcher has run 24 hours in one session. That is the shape this
closes." The measured shape is worse: 8 sessions over 24 h, and the longest is 262 hours** — an
eleven-day session carrying 75 turns, which is the idle-holding shape rather than a working one.

**Derived lifetime bound: 4 hours.** Derivation: §2.2's RSS curve reaches its plateau inside the
first hour and the 4–8 h band is the first in which the sample thins to n=3 and the mean falls,
i.e. the first band where the population stops being comparable. Below 4 h, 30 of 31 live
processes sit on a single interpretable curve. Above it, the evidence is three processes. **A
bound should be set where the evidence still supports it**, and 4 h is the last point where it
does. p90 of actual session spans is 7.96 h, so the bound retires roughly the top decile.

---

## 4. LOCAL regime — the allocation ceiling as arithmetic

### 4.1 The ceiling, recomputed from §1 and CONFIRMING the contract

```
total                        27.67 GB
non-Claude (measured)        13.52 GB
reserve                       3.00 GB   (the contract's figure, carried not re-derived)
-------------------------------------
Claude budget                11.15 GB
per seat (measured)           0.413 GB  (287.0 heavy + 126.3 light)
-------------------------------------
CEILING                      27 seats
```

The contract's arithmetic was 9.6 GB / ~400 MB = 24 seats. Measured today: 11.15 GB / 413 MB =
27. **The difference is entirely in the non-Claude figure** (13.52 GB measured against ~15.6 GB
assumed); the per-seat figure is confirmed within 5%. The ceiling is therefore recorded as a
**computed value with its inputs**, not as the integer 24 or 27 — a ceiling typed into prose is
stale at the next commit, and this one moves whenever the non-Claude load does.

### 4.2 The refusal condition is LIVE right now

At the moment of measurement: **31 seats against a 27-seat ceiling, and 1.62 GB free against a
3.00 GB reserve.** The reserve is already breached and the box is 4 seats over. ADR-110's stated
lane ceiling is 4–6; `seat_refusals.py`'s `lane-ceiling` reads a COUNT and no memory, so nothing
on this box noticed either fact. This is QR-RES-001's "the attribute the operator described as
the least discretionary is the one with no organ at all", observed in the act.

### 4.3 The corroborating incident record

Six of 76 jobs with a surviving `timeline.jsonl` carry a reap or OOM mention. Two are load-bearing:

- job `9b8de937`, 2026-09-15T01:02:21Z — *"OOM reaper killed merge; repo safe; ollama holding
  8.2 GB; retrying merge"*. **This is a commit killed by the OOM reaper, in batch Z, and it
  names an 8.2 GB non-Claude consumer** that no ceiling accounted for.
- job `d14f5e04`, 2026-09-14T22:58:09Z — *"Killed 18 orphaned processes (688.6 MB) including a
  46.8-hour bash poller stuck on deleted lane `lane-x-689-conductor-e-proof` … box is not
  orphan-bound but dispatcher-bound — 25 live lanes"*. The contract's 46.8-hour orphan, with the
  seat count that night (25) close to today's 31.

---

## 5. The four BEFORE measurements

### 5.1 Lanes completed per hour

Source `logs/MERGE-RECEIPTS.jsonl`, 11 `kind=merge` rows with both timestamps.

```
batch   merges   queue span   lanes/hour   per-merge wall (median/min/max)
  Y          5      3.83 h         1.30      12.6 / 5.9 / 53.0  min
  Z          6      4.94 h         1.21      28.2 / 5.8 / 80.3  min
```

**Conditions.** This is the integrator's merge-queue rate, not lane execution time; a lane
counts as completed when its receipt closes. Lanes that ran and handed back nothing never reach
this ledger, so the figure is an **upper bound on throughput** and is silent about the failure
mode the contract's item 4 names. Batch Z's per-merge wall is 2.2× batch Y's on one more merge.

**A caveat that disqualifies the receipts as a fine-grained instrument:** `unrecorded_seconds`
is **90.1% of batch Y's merge wall time and 98.2% of batch Z's**. Almost all merge work happens
outside the steps the receipt times — the receipts' own step text says so in words ("these
seconds badly UNDERSTATE merge wall time"). The span-based rate above is therefore the usable
figure and the per-step breakdown is not.

### 5.2 Cost per lane

Source `logs/LANE-COSTS.jsonl`, 6 rows, all `claude-opus-5`.

```
$49.59  Y  lane-y-750-merge-receipts
$40.29  Y  lane-y-751-cost-in-money
$35.93  Y  lane-y-752-declared-model-runs
$19.57  Y  lane-y-755-docs-cut-finish
$18.82  Y  lane-y-751-cost-in-money        (second close of the same slug)
$14.48  Y  lane-y-754-backlog-to-bar

n=6   median $27.75   mean $29.78   min $14.48   max $49.59   total $178.69
```

**Conditions.** A client-side estimate — list rates × counted tokens, `lane_cost.py`'s own
declared limit — not a bill. The population is **6 lanes of one batch**, not the fleet; batch Z
closed no cost rows at all. One slug appears twice, which the append-only ledger permits and
which means "cost per lane" here is cost per *close*, not per lane.

### 5.3 Commits killed by the OOM reaper per batch — CANNOT BE TAKEN AS SPECIFIED

The contract states this figure is "currently NON-ZERO". **It is non-zero — §4.3 names one, in
batch Z — but it cannot be counted, and the reason is structural rather than an omission.**

- There is **no structured reap field anywhere**. 302 job directories were scanned; 77 have a
  `state.json` and 76 a `timeline.jsonl`. A key-level scan for any key containing `reap` across
  every timeline record returns **zero keys**. Every reap fact is free English inside a `detail`
  or `text` string.
- `QR-AVAIL-005` cites `reapedMidWorkAt 2026-09-14T22:43:32Z` in job `100297d3`'s `state.json`.
  **That key is not in the file today.** `state.json` is a live, mutable, per-turn-rewritten
  file — the same job's `state.json` now reads `"detail": "triaging F-mark failures, 62
  claude.exe at 12.65GB"`. **The register's own evidence was overwritten by the file that held
  it.** The entry is not wrong; its citation is no longer re-verifiable, and that is a finding
  about where evidence is kept, not about the entry.
- Even with a reap counted, "killed a COMMIT" is a further claim nothing records. A reap
  timestamp says a session died; nothing says whether its index was dirty when it did.

**What would make it takeable:** a reap record written to an append-only surface carrying the
session's last commit SHA and its index state, so a reap that left staged-but-uncommitted work
is distinguishable from one that landed cleanly. Until that exists the honest BEFORE figure is
**"at least 1 in batch Z, uncountable in general"**, and a number would be manufactured.

### 5.4 Codespace minutes paid per batch

**Zero recorded.** The full key set of `logs/MERGE-RECEIPTS.jsonl` is `baseline_split_minutes,
batch, by_class_seconds, closed, concurrent_seats, host, kind, merge_sha, opened, ordered_model,
ran_model, recorded_seconds, serial_seconds, slug, steps, suite_verdict, unrecorded_seconds,
wall_seconds` — no uptime or minutes key on any row.

**Zero recorded is not zero paid.** It is the absence §6 closes, and the AFTER figure for this
one is the only one of the four that can be a clean comparison, because there is nothing to
compare against.

---

## 6. CODESPACE regime — the substrate question, ANSWERED

### 6.1 Was a container provisioned and verified since `[#746]` merged? NO.

`[#746]`'s repair landed at `4f4186a6` (merge) / `0dcdb153` (fix), 2026-09-15, and is an
ancestor of `origin/main` at `5b880b03`. Before this lane, `gh codespace list` held exactly one
codespace: `suite-baseline-2026-09-08-…`, created **2026-09-08**, `Shutdown`, i.e. seven days
older than the repair. **No container had been created since it merged.** So a probe was
provisioned, as the contract directs.

### 6.2 The probe, and the evidence distinguishing OUR container from the recovery substitute

`lane-aa-14-probe-q945j7g4rjwc4wjj`, `basicLinux32gb` (2 cores / 8 GB), branch `main`,
idle-timeout 30 m. Created 2026-09-15T12:20:40Z, deleted 12:32:38Z — **11.97 minutes of metered
uptime, the whole cost of this answer.**

The platform reporting `Available` is **not** part of the evidence below, deliberately: the
substrate reported healthy while broken before, which is the whole reason this question is asked
that way.

**Negative evidence — what a recovery container says about itself, counted in
`/workspaces/.codespaces/.persistedshare/creation.log` (98,751 bytes):**

```
"Creating recovery container"   0
"Container creation failed"     0
"postCreateCommand failed"      0
"failed with exit code"         0
"[provision] REFUSED"           0
```

Those are the exact strings that appeared in `lane-z-substrate-probe`'s log on 2026-09-14 when
it died into a recovery container. **Their count is zero.**

**Positive markers — each one a thing only our devcontainer produces, paired with what a
recovery container yields instead:**

```
marker                                   observed                          recovery would give
[provision] lines in creation.log        48                                0
provision DONE line                      "2 leg(s) acted; all four legs    absent
                                          assert clean and a real gate
                                          ran here"
provision gate line                      "gate OK — uv 0.11.19, full       absent
                                          history + spine refs, ecosystem
                                          registered, three hook types
                                          armed, stamp current"
uv                                       0.11.19 == pyproject pin          no uv at all
                                         ("required-version = ==0.11.19")
claude CLI                               2.1.272, /home/vscode/.local/bin  absent (no feature)
git history                              7685 commits, shallow=false       shallow or absent
local `main` ref                         resolves, 0 behind origin/main    absent (the 2026-08-19
                                                                            container had none)
.venv python                             3.12.10 == .python-version        no venv
git hooks armed                          commit-msg, pre-commit, pre-push  none armed
ecosystem/.dev-knowledge/state.yaml      present                           absent — the glob is
                                                                            gitignored, so it can
                                                                            ONLY come from leg L5
provision.sh on disk                     carries the [#746] re-exec guard  n/a
                                         and self_digest()
gh codespace view --json prebuild        true                              n/a
```

**The single strongest marker is `ecosystem/.dev-knowledge/state.yaml`.** `ecosystem/*/state.yaml`
is gitignored, so it cannot arrive by clone. Its presence in a fresh container is producible by
exactly one thing — provision leg L5 having run — and a recovery container runs no legs.

**VERDICT: the Codespace substrate is LIVE.** Not "it came up": eleven independent positive
markers, four recovery-container phrases at count zero, and one marker (L5's state.yaml) that no
path other than our provisioning can produce.

### 6.3 FIRST REAL-CONTAINER WITNESS of the `[#746]` repair — with its limit stated

The creation log carries, at 12:21:20.704Z:

```
[provision] freshness: 'main' is behind origin/main by 53 commit(s) — 4f4186a6 -> 5b880b03
[provision] freshness: OK — now at origin/main (5b880b03)
```

**That is the exact shape that killed `lane-z-substrate-probe` on 2026-09-14** — a prebuild image
serving a stale tree, fast-forwarded mid-run. There it produced two `can't open file
'.../cloud_provisioning.py'` errors, `[provision] REFUSED: B1`, and a recovery container. **Here
the run continued to completion:** B1 OK, L5 OK, L3 OK, gate OK, `DONE`. This lane is the first
real-container witness that the repaired path survives a stale-snapshot fast-forward.

**The limit, stated so the witness is not over-read.** The `[#746]` fix has two halves: the image
carrying the repaired script, and the `self_digest()` + `exec` hand-over for when it does not.
**Only the first half is witnessed.** The prebuild image was baked at 02:55–02:58Z today from
`4f4186a6` — which already contains the repair — so `provision.sh`'s bytes did not change across
the fast-forward and **the re-exec guard never needed to fire.** Its presence on disk is
verified (`DEV_KNOWLEDGE_PROVISION_REEXEC` and `self_digest` both found); **its firing is not.**
Witnessing that requires a container whose image predates a `provision.sh` change, which is
producible only by changing `provision.sh` without touching `devcontainer.json` or its Dockerfile.

### 6.4 Uptime, idle and build — the three figures §3 asks for

The creation log spans both the prebuild bake and this creation, separated by a 33,761-second gap:

```
SEGMENT 1 — PREBUILD BAKE           02:55:46 -> 02:58:22   = 155.8 s
  docker buildx build               02:56:02 -> 02:57:24   =  82.1 s
  onCreateCommand (8 legs acted)    02:57:27 -> 02:58:22   =  55.0 s

SEGMENT 2 — THIS CREATION           12:21:02 -> 12:21:37   =  34.1 s
  postCreateCommand (2 legs acted)  12:21:09 -> 12:21:35   =  25.9 s
  postStartCommand gate             12:21:35 -> 12:21:36   =   1.4 s

create API call returns                                    =  12.0 s
create call -> "Finished configuring"  12:20:40 -> 12:21:37 =  57.0 s
probe lifetime (created -> deleted)    12:20:40 -> 12:32:38 =  11.97 min
```

**Container build time: 82.1 s image build + 55.0 s full provisioning = 136.9 s cold.** Off a
prebuild: **34.1 s**, of which 25.9 s is the two legs that cannot be baked.

**Idle time paid for.** The probe's own idle time was ~11 min of its 11.97 (the work inside it
took under a minute). More significant: `suite-baseline-2026-09-08` has existed **since
2026-09-08 in `Shutdown` state** — seven days. Shutdown codespaces do not bill compute but do
bill **storage**, continuously, and its `retentionPeriodDays` is 30. It is the "left warm in
case" shape the contract's idle policy forbids, and it is live today.

### 6.5 RULING: do prebuilds pay for themselves at our batch frequency?

**On time, the arithmetic is measured and the answer is yes-but-trivially.** A prebuild saves
`155.8 − 34.1 = 121.7 s ≈ 2.0 minutes` per codespace creation. Our measured creation frequency
is **2 creations in the 8 days from 2026-09-08 to 2026-09-15** (`suite-baseline`, and this
probe; batch Z's two Codespace lanes were dispatched detached and produced nothing — QR-AVAIL-003).
At that frequency a prebuild saves **about 4 minutes per week.**

**On money, the figure cannot be taken today and I will not substitute one.** The cost side of a
prebuild is Actions minutes for each bake plus continuous storage for the prebuild image, and
neither is readable from here: `gh api user/settings/billing/shared-storage` returns 404 on this
account, and `repos/.../codespaces/prebuilds` likewise. **What would make it takeable:** the
Codespaces billing page's monthly storage line, or an org-level billing endpoint.

**So the ruling, at the precision the evidence supports:** *four minutes of saved wall time per
week is not a defensible reason to hold a prebuild image in continuous paid storage, and the
recommendation is to DISABLE prebuilds unless Codespace creations rise above roughly one per
day, at which point the saving crosses 15 minutes a week and the question should be re-asked
against the storage line.* This is stated as a recommendation with its threshold and its
missing input named, **not as a ruling**, because a prebuild ruling made without the storage
figure would be exactly the "answer it in principle" the contract forbids.

One measured fact does cut the other way and is recorded rather than suppressed: the prebuild is
what made `[#746]`'s repair reach this container at all — `on_configuration_change` fired on
`0dcdb153`'s `devcontainer.json` edit and baked a repaired image. Without a prebuild every
creation runs the tree's own current `provision.sh`, which removes the stale-snapshot failure
class entirely rather than repairing it. **That is an argument for disabling prebuilds, not
against.**

### 6.6 Idle policy, as measured rather than as preference

- Attached while a lane runs; **torn down at handback**, not stopped. This probe was deleted
  11.97 minutes after creation, and the deletion is the evidence.
- **Stopped is not free.** A `Shutdown` codespace bills storage for up to
  `retentionPeriodDays` (30 here). `suite-baseline-2026-09-08` has been doing so for 7 days.
- `--idle-timeout` is a backstop and not the policy: it was set to 30 m on this probe and would
  have paid 30 minutes of compute for a lane that finished in one.

---

## 7. What this lane did NOT do, named plainly

- **The `NODE_OPTIONS` heap cap is not wired.** It is in this lane's contract, but
  `scripts/gen_seat_boot.py` is the sole-owned file of `[#789]` (filed on branch
  `worktree-aa-runtime-resource-intake`), which is rewriting that exact render surface so a
  declared value cannot reach an HTML comment. Opening it here would be a second undeclared claim
  on a file being restructured — the same disposition `lane_cost.py` records against
  `merge_receipt.py`. The seam is left as a proposed diff in `[#792]` rather than applied, and
  **it is not claimed as done.**
- **The re-exec half of `[#746]` is verified present, not witnessed firing** (§6.3).
- **The RSS retirement leg is not derived from a longitudinal trace** (§3.2); it ships against a
  cross-sectional plateau with that provenance recorded.
- **No substrate heartbeat receipt was written.** `validate_substrate` leg 8 arms 2026-09-16 and
  wants `scripts/substrate_heartbeat.py probe --substrate codespace --write-receipt`. That script
  is unmerged, on `worktree-lane-aa-1-substrate-provenance` (`f0681233`), and is another lane's
  sole-owned file. **§6.2's evidence is exactly the input such a receipt would carry**, and the
  writer's owner can mint it from this file without re-provisioning.
- **The prebuild ruling is a recommendation, not a ruling** (§6.5) — the storage figure is missing
  and is named.

---

## 8. Where the evidence stops

Every figure here is from **one box, one day**. §2.1's cost curve rests on 681 sessions and is
the strongest claim in the file; §2.2's RSS curve rests on 31 processes in a single snapshot and
is the weakest. The latency refutation (§3.2) is strong for what it measures — 92,743 turns — and
silent about client-side behaviour it cannot see. The Codespace figures are one container.

Reproduce with: `scripts/resource_lifecycle.py sample` for §1/§2.2,
`scripts/resource_lifecycle.py ceiling` for §4, `scripts/context_reclamation.py derive` for
§2.1/§3.1.
