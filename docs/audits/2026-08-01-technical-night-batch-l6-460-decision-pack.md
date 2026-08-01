# Night batch 2026-08-01 — L6: [#460] decision pack (open question R1)

**Status: PROPOSAL — a one-read consolidation for the operator's ruling. Neutral above, recommendation last.**

**Done-contract: MET**, with one honest caveat stated up front rather than buried (see §0).

**Row under decision:** `tasks/460-history-dailies-write-only-no-consumer.md` · P2/S · [E7] ·
story [S20] · `serialize-group: settings-json`. Status `open`; flagged in the 2026-08-01 handoff as
*{OPERATOR-RULED THIS SESSION: recommendation recorded, ruling open}*.

---

## §0 — Read-only verification statement (read this before trusting any date below)

`git branch -a`, `git for-each-ref`, `git reflog show --all`, and `git fsck --unreachable` in this
container all confirm **zero trace** of the `automation/fleet-audit` branch;
`git log … origin/automation/fleet-audit` returns `fatal: ambiguous argument … unknown revision`.
Per the batch's read-only rails, **no fetch was attempted**. The orchestrator additionally confirmed
this clone is **shallow** (373 commits; the parent of `e631e59` is absent), so deep-history claims
could not be re-derived here even for branches that *are* present.

**Consequence:** every claim about that branch's commit history below is **transcribed from documents
written by the 2026-07-31 night review session** (which did have branch access), not re-derived by
this lane. Flagged inline where it matters.

---

## §1 — What the night-routine dailies lane WAS

Three ADRs, chronologically:

- **ADR-76** (Accepted 2026-06-06) — the mechanism. Windows Task Scheduler →
  `python scripts/fleet_health.py` directly, no LLM. Task identity
  (`scripts/setup-fleet-scheduler.ps1:52-53,90-97,109`): `\DevKnowledge\fleet-baseline`, daily 09:00
  local, **system-resolved Python — not `uv run --locked`**, because it predates the uv rollout
  (ADR-106) by seven weeks. ADR-76 §5 said the parallel SessionStart trigger *"is removed once the
  scheduled task is confirmed reliable at n=1"* — **it never was**; `tasks/418-*.md:13` confirms both
  still fire independently, causing 0–10 commits/day multiplicity.
- **ADR-80** (Accepted 2026-06-07) — writer policy. Mutable pointer (`state.yaml`) gitignored; the
  **durable record** (`history/*.md`, digests, rollup) committed by the writer. This is the "ADR-80
  durable record" the row says silently stopped.
- **ADR-84** (Accepted 2026-06-13) — branch isolation. Output fully isolated to orphan branch
  `automation/fleet-audit`, never merged to `main`.

> **Load-bearing and easy to misread:** ADR-84's own "Fact 1" already states *"no hard consumer pins
> either output to `main`. The baseline has zero readers."* **The no-consumer condition is original
> to the design (2026-06-13), not a defect that developed later.**

**Mechanism, read directly from source this session:** `_history_path` (`scripts/audit.py:367-368`)
writes `ecosystem/<repo>/history/<date>.md`; `append_history` (`:387`) appends a
check/status/evidence table; `cmd_run` (`:3429-3431`) runs `ALL_CHECKS` per repo then calls
`_commit_routine_outputs` (`:3282-3416`), which snapshots durable-scope paths onto
`refs/heads/automation/fleet-audit` via a **separate git index** + `read-tree`/`add`/`write-tree`/
`commit-tree`/`update-ref` plumbing (main's HEAD/index/working tree never touched), tagged
`Routine: fleet-audit`.

**No push-to-origin call exists in that code path** — pushing is a separate, apparently manual act.

Six registered repos have `ecosystem/*/history/` on disk: `.dev-knowledge`, `ai-council`,
`win-tooling`, `corp-ops`, `corp-monorepo`, `corp-sca-time-automation`. Note `win-tooling` is absent
from `ecosystem/deployed-versions.yaml` (grep-confirmed) — that is what [#463]'s ADR-91 WARN is about.

**Not the same thing:** the newer [#382]/ADR-109 desired-state divergence report
(`scripts/desired_state_report.py`) is a separate, human-invoked-only artifact with no scheduler and
no consumer. See §7.

---

## §2 — Evidence the branch-commit lane is DEAD

**Claim under test:** *"its branch-commit leg has been dead since 2026-07-16 and nothing noticed."*

Sources:
1. `tasks/418-*.md:13` — filed **before** the deep review (cites only ADR-76/84/#417): *"none since
   2026-07-16."* Appears to be an earlier, independent observation.
2. `JOURNAL.md:194-224` (2026-07-31 entry (u)) — *"98 commits / 36 digests / 185 files,
   **2026-06-15 → 07-16**"*: first commit 2026-06-15, last 2026-07-16, 98 commits over 32 days.
3. `JOURNAL.md` entry 2026-07-31 (s) — *"its output trail stops 2026-07-16."*
4. `docs/audits/2026-07-31-verification-382-ladder-evidence.md:46-63` (§L0.5) — quotes live Task
   Scheduler state (Ready, DaysInterval 1, StartBoundary 2026-06-06T09:00) and states *"Last
   `ecosystem/*/history/*.md` on `origin/automation/fleet-audit` = 2026-07-16.md"*. Notes that
   `Get-ScheduledTaskInfo` returned "cannot find the file specified" — **that session's evidence was
   also entirely git-date-based**, the same limitation this lane has.

**Verdict: UNVERIFIED BY THIS LANE.** Sources 2–4 are one night session's output and likely share a
single underlying git-log read. Source 1 is earlier-dated and appears independent.

**Gap length, computed here:** 2026-07-16 → 2026-08-01 = **16 days** (the sources say "15", accurate
when written on 07-31, now one day stale).

### Do not conflate the two "46 days"

- `tasks/460-*.md:13` — *"one FAIL sat visible daily 46 days"* — about a specific FAIL on the
  fleet-audit branch (likely the corp-sca-time-automation finding [#464] calls its longest-running).
- `docs/audits/2026-07-30-conformance-nightly-digest.md:50` — a **different** 46-day gap, about
  cadence on the **different** `automation/conformance-digest` branch.

Both are 46 by coincidence.

### Root cause of the stoppage: NOT ESTABLISHED ANYWHERE

The row says the commit leg is dead *"while the local writer still runs"* — but the code
(`cmd_run` unconditionally calls `_commit_routine_outputs`) does not obviously separate those two
things. Plausible, unconfirmed: the Scheduled Task registration is gone entirely (consistent with the
"cannot find the file specified" response); or local commits still happen but were never pushed (the
code has no auto-push); or an environment change broke the chain before the commit step.

> **This is a real blocker for Decision A's literal action.** "Decommission the dead scheduled task"
> may be targeting a component that is already gone. A live machine-side check is needed that no
> repo-bound lane can perform.

### What "nothing noticed" means mechanically

`scripts/fleet_health.py:42-44` **already has a staleness alarm** (`_STALE_AFTER_HOURS = 48`) — but
it reads `logs/FLEET-HEALTH.md`, which the SessionStart hook itself refreshes every time a session
boots and finds it stale. **So the one detector that exists is structurally blind to this exact
failure:** the SessionStart leg keeps the local digest looking fresh regardless of whether the
Task-Scheduler path is alive.

A full grep (`docs/audits/2026-07-31-verification-382-ladder-evidence.md:66-74`) found **zero code
anywhere that reads a daily's content**. Detection depended entirely on a human choosing to read 98
commits by hand — which happened once, on explicit operator authorization.

---

## §3 — Evidence the lane still produces VALUE

**Nine live external defects**, absorbed into two rows:

- **[#463] win-tooling (4 items)** — `config.yaml` not dot-prefixed (ADR-59) FAIL; VISION+ARCHITECTURE
  edited-then-never-re-reviewed FAIL; workspace sort settings absent WARN; absent from
  `deployed-versions.yaml` WARN. **Identical evidence from 2026-07-11 admission through 2026-07-31**
  (~20 days unchanged).
- **[#464] corp-*/ai-council (5 items)** — corp-sca-time-automation CLAUDE.md never-re-reviewed FAIL
  (the lane's longest-running finding) + 3 more past-cadence docs; corp-ops 4 canonical docs past
  cadence; corp-monorepo VISION past cadence + malformed CONTRIBUTING; ai-council `unknown-spec` edge.
  **Live 15–46 days, surfaced daily, zero consumption.** None of this is visible to the hub's own
  gates, which are hub-scoped.

**[#465] is a different and more interesting class.** Four **writer-integrity bugs**, found by diffing
the branch's *superseded same-day git blobs*: skips emitted as `pass` (inflating pass counts); two
committed digests silently overwritten, each dropping 14 WARNs; the hub misresolving as not-itself on
6 of the last 8 runs; `handoff_tag_canonicity` self-disabled.

> **That class is detectable only because the lane is git-history-backed.** A single-mutable-state
> design would hide it permanently. This is the strongest argument in the pack *for* the lane's
> architecture, and it is easy to lose while arguing about the scheduler.

**Without the lane:** all nine [#463]/[#464] findings would be invisible to every other mechanism
cited in any source read, plus the four [#465] bugs findable only by forensic history diff.

---

## §4 — What the recorded recommendation actually CHANGES — three separable decisions

The recommendation is "stop the branch lane, keep the SessionStart digest, add a persistence-triage
consumer (ADR-105)." Item (4) on the row (*"the ADR-106 system-python oddity dies with the task"*) is
**not a fourth decision** — it is a free consequence of A (the task invokes plain `python`, not
`uv run --locked`).

- **Decision A — stop the branch, decommission the task, record the ADR-80 divergence.**
  *Cost:* machine-side unregister (outside repo/agent reach) + one doc/ADR edit.
  *Breaks:* branch stops growing; no history rewrite proposed.
  *Retires:* the false-assurance risk — ADR-80 currently still formally promises a record that has
  been silently absent 16+ days.
  *Blocked on:* the §2 root-cause gap. Decommissioning the wrong component fixes nothing.

- **Decision B — keep the SessionStart digest + `logs/FLEET-HEALTH.md`.**
  *Cost:* zero, already running.
  *Does NOT discharge ADR-105 for this surface* — it is a cached, passively-surfaced current-state
  digest, structurally the same "surfaced but not necessarily consumed" pattern ADR-105's own Context
  section names as the precipitating defect.

- **Decision C — persistence-triage (a finding live > N days auto-files a BACKLOG row).**
  *Cost:* a real build.
  *Design gap the row does not address:* **the branch's daily history was the only place "N
  consecutive days live" was computable.** If A stops the branch, C needs an independent persistence
  store (e.g. a first-seen field in the currently-gitignored `state.yaml`). It also needs a named
  consumer for the auto-filed rows — see §5.

---

## §5 — What the ADR-105 persistence-triage consumer would CONSUME

ADR-105 §1 fixes six fields (`trigger · scope · consumer · consumption_path · verified_by ·
review_date`); §2 gates only **ACTIVATION** — filing without `consumer`/`consumption_path` is
explicitly permitted (live precedent: [#409]–[#411]).

| field | fillable for persistence-triage? |
|---|---|
| `trigger` | Depends which surface A/B leave running — not finalizable until §4 is ruled. |
| `scope` | Depends on N (unspecified) **and** on where "consecutive days" gets computed once the branch may stop (§4 gap). |
| `consumer` | **NOT HONESTLY FILLABLE YET.** The natural candidate is BACKLOG grooming — but [#348] is decomposed, holds only piece (b), and `depends-on: #270`, which is itself OPEN/P1/unbuilt (confirmed live in `BACKLOG.md` today). Naming it would name a non-functioning mechanism — exactly what ADR-105 exists to prevent (*"branches nobody opens are a path in name only"*). |
| `consumption_path` | Same blocker. One real, currently-live alternative: `PROBES.md` **P10**, which mechanically grooms the whole open BACKLOG at every architect-mode handoff boot — real, but cadence-irregular (every few days to a week, not daily). |
| `verified_by` | Fillable in principle (a test seeding an N-day-old finding and asserting a row gets filed); not built — acceptable to leave open at filing. |
| `review_date` | Trivially fillable (sibling rows use `2026-08-26`). |

**Bottom line: two of six fields cannot be honestly filled today** without either landing
`#270`/`#348` first, or accepting the weaker P10 handoff-boot pass as an interim path. `trigger` and
`scope` additionally wait on §4. This argues for **filing** C's row now (ADR-105 §2-sanctioned) but
**not activating** it in the same stroke as A/B.

---

## §6 — Cost of each option (neutral)

- **(a) Status quo.** Zero implementation cost. Scheduled task stays in an unexplained failure state;
  the [#383]/L3.5 lane stays blocked by the sequencing constraint; nothing improves.
- **(b) Recommendation as recorded (A+B now, C later).** A is low-cost but blocked on the root-cause
  check; B is a free no-op; C is a real build gated on §5. Retires the false-record risk immediately
  via A; the "unread despite existing" risk retires only once C actually activates.
- **(c) Stop the whole lane (branch AND SessionStart digest).** *Not* the recorded recommendation;
  included for completeness. Removes the **only** currently-live automated cross-repo visibility
  mechanism; [#463]/[#464]-class drift would stop being found by anything. Materially larger step
  back than (b).
- **(d) Keep everything, add branch-staleness alerting only.** Smallest real fix — extend the existing
  `_STALE_AFTER_HOURS` pattern to the branch's own last-commit age. Would have caught the 07-16
  stoppage within ~48 h instead of 16+ days. But does **not** touch the larger defect: findings
  sitting unactioned *while the branch is alive* is a reading gap, not a liveness gap.

---

## §7 — The sequencing constraint, and why it binds beyond this row

`RESIDUAL.md` §4 item 2 and the ladder-evidence pack's L3.5 both state: **"rule [#460] before putting
the divergence report on any cadence."** The recorded reasoning: *"putting a second write-only
producer on a timer before the first one's consumer question is answered would repeat the exact
defect [#460] names."*

The [#382] desired-state divergence report is today **structurally identical to the fleet-audit lane
at its own inception** — no consumer, human-invoked only. Ruling [#460] *in either direction* is what
unblocks L3.5 (2–3 windows) and the downstream [E9] reconcile-loop work. **It is not scoped to this
one lane.**

Within the backlog it also gates [#461] (mechanize the six window metrics — same
`serialize-group: settings-json`) and [#465] (writer integrity — fixing a writer that may be
decommissioned).

---

## §8 — RECOMMENDATION

**Rule Decisions A and B now.** They are nearly free, and A retires a real, currently-active
false-assurance risk: ADR-80 has silently promised a durable record that has been absent 16+ days.

**Before executing A**, have a live session confirm on the actual host machine whether the Scheduled
Task registration is gone, erroring, or silently producing unpushed local commits (§2) — target
whatever is actually there, not what the row's wording assumes.

**Do not rule Decision C as bundled with A/B.** ADR-105 permits filing without a named consumer, but
the obvious consumer (BACKLOG grooming) is itself gated behind the still-open [#270] load-gauge. File
C's row now with the four fillable fields set and `consumer`/`consumption_path` explicitly open
(ADR-105 §2-sanctioned), and treat **activation** as a follow-on gated on `#270`/`#348` — or, as an
explicitly weaker interim, on the already-real P10 handoff-boot grooming pass. Activating it
prematurely by hand-waving a consumer into place would recreate, in miniature, the exact defect this
review exists to name.

**One thing worth preserving in whatever is ruled:** the git-history-backed design is what made
[#465]'s writer bugs findable at all. If A stops the branch, that forensic capability goes with it —
which may be an acceptable price, but it should be paid knowingly rather than as a side effect.
