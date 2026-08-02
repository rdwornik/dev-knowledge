# Night batch 2026-08-03 - lane L-F - ruling inputs: B-2, B-3, B-4, and the Section F numeric target

- **Class:** technical (ADR-101 enum) - **Date:** 2026-08-03 - **Slug:** night-lf-rulings-prep
- **Status:** PROPOSAL - read-only night batch, unattended. Nothing was filed, closed, reworded,
  regenerated or fixed. Every option below is an INPUT to an operator ruling, never a ruling.
- **Base:** HEAD = `c7628a3e` on `claude/night-batch-2026-08-03-k8djp8` (174 commits ahead of local
  `main` = `65a549bf`; `origin/main` also resolves to `c7628a3e`). Evidence branch
  `origin/automation/fleet-audit` = `38a73323`. Working tree verified clean throughout.
- **Method:** read-only. Git history and both lineages queried, never mutated; no generator run with
  `--write`/`--fix`; the source digests were re-read from disk and quoted, not paraphrased from the
  brief. `uv run --locked` is unavailable in this container (ADR-106 pins `uv==0.11.19`, the box has
  `0.8.17`), so the two python probes ran in an isolated scratchpad venv - **no container result is
  offered as a gate verdict.**
- **Scope constraint, stated up front:** for Section F this report presents candidate DEFINITIONS
  and their gating shapes only. **No number is recommended, and no definition is recommended.**

---

## Verdict

B-2's premise has changed under it: the WARN collapse it blames on the parallel trigger was a
resolution seam, fixed on 2026-08-02 by `56f82aaf`, and the lane record shows the 09:00 scheduled
task has not fired since 2026-07-23 - so the trigger is currently the only producer, not the defect.
B-3 is now n=1 with five clean observations after it; the ruling is what a single unreproduced
plumbing FAIL justifies, and the evidence has moved toward "watch". B-4 is genuinely doctrinal and
the brief's premise needs correcting: the "lossless union" unified three RUNS of one day inside the
lane, not the two LINEAGES - which remain near-disjoint (16 dates main-only, 45 lane-only, 1 shared
and unequal). Section F carries two refuted figures and still has no number; four candidate
definitions are laid out with their gating shapes, and none is recommended.

---

## B-2 - retire the parallel SessionStart audit trigger?

**The question, verbatim** (`docs/audits/2026-08-02-technical-night-batch-lb-fleet-audit-commits.md:160`):

> | B-2 | Retire the parallel SessionStart audit trigger now that it is named as the collapse source? | retire / keep / investigate-first |

### Current state

**Five SessionStart hooks are live**, all five scripts present on disk
(`.claude/settings.json:26-55`; mirrored in `CLAUDE.md` section 9):

|entry|command|on disk|
|---|---|---|
|1|`uv run --locked python .../scripts/fleet_health.py` (timeout 60)|23915 B|
|2|`powershell -File .../scripts/surface_triage.ps1` (timeout 10)|5390 B|
|3|`powershell -NoProfile -File .../scripts/billing_leak_sentinel.ps1` (timeout 10)|1219 B|
|4|`uv run --locked python .../scripts/changelog_sentinel.py` (timeout 20)|4397 B|
|5|`uv run --locked python .../scripts/arm_hooks.py` (timeout 60)|4720 B|

**The one proposed for retirement is entry 1, `fleet_health.py`** - it is the only SessionStart hook
that runs the audit. `scripts/fleet_health.py:4-6`: *"Session-start-throttled: run at most once per
calendar day. On boot: - If logs/FLEET-HEALTH.md is missing or stale (run_date != today) -> run the
full cross-repo audit (audit.py run), write a fresh digest."* The subprocess is
`scripts/fleet_health.py:441-444` (`[sys.executable, scripts/audit.py, "run"]`), and `audit.py run`
is what appends the dailies (`scripts/audit.py:404-414`, file opened in append mode `"a"`) and
commits them to `automation/fleet-audit` (`scripts/audit.py:3508`, `:3615`).

**The retirement clause is a standing, undischarged ADR obligation.** `ADR-76:53`:

> The existing SessionStart-throttled `fleet_health.py` invocation (ADR-74) remains active during the
> validation period and is removed once the scheduled task is confirmed reliable at n=1 (the current
> gate). Both paths are non-destructive and non-conflicting.

**L-B's stated ground for retiring it** (`...-lb-fleet-audit-commits.md:97-99`):

> **Correlates with the un-retired parallel trigger.** The high/correct count matches the 09:00
> scheduled run; the collapse follows same-day from the parallel SessionStart trigger that ADR-76
> said would be "removed once the scheduled task is confirmed reliable" - it never was.

**Two live findings materially change that ground.**

*(a) The root cause was found and fixed AFTER the L-B report was written.* L-B's base was
`a02dd111`; `56f82aaf` (2026-08-02 14:32:03 +0200) is later on the same spine:

> Merge branch 'fix/465-hub-only-warn-drop' - [#465] legs 2+3: the hub recognises itself from any
> checkout / Root cause was a resolution seam, not a check: audit_repo was handed the absolute path
> COMMITTED in ecosystem/.dev-knowledge/state.yaml while every hub-only check gated on the live
> _REPO_ROOT.

`BACKLOG.md:266` now reads `**(2)+(3) DONE**`, and records the residual explicitly: *"NOT fixed: the
same-day file collision - a cross-tree run still last-run-wins, now non-lossy."* The fix is visible
in `scripts/audit.py:417-427` (`resolve_repo_path`). Live confirmation on the lane - every run block
since 2026-08-01 carries **zero** "not the hub repo" lines, and all five 2026-08-02 blocks (13:01,
13:04, 16:59, 21:03, 21:04) report an identical `warn=15 fail=0 n/a=4`:

```
2026-07-23T09:00:49  warn=21  not-the-hub=0     <- scheduled run, correct
2026-07-23T11:01:08  warn=2   not-the-hub=10    <- the collapse
2026-07-23T14:47:05  warn=2   not-the-hub=10
2026-08-01 (2 runs)  warn=15,21  not-the-hub=0
2026-08-02 (5 runs)  warn=15 x5  not-the-hub=0
```

*(b) The scheduled task has not fired since 2026-07-23.* Recovering every run timestamp from every
superseded lane commit (not just the tip, which holds only the day's last run):

```
07-16 no-0900   07-17 HAS-0900   07-18 HAS-0900   07-19 HAS-0900   07-20 HAS-0900
07-21 no-0900   07-22 no-0900    07-23 HAS-0900   07-24 no-0900    07-25 no-0900
07-26 no-0900   07-27 no-0900    07-28 no-0900    07-29 no-0900    07-30 no-0900
07-31 no-0900   08-01 no-0900    08-02 no-0900
```

Cross-checked on a consumer repo (`ecosystem/ai-council/history/`): 07-23 carries `T09:00:53`, and
07-25 / 07-29 / 08-01 carry none - so this is fleet-wide, not a hub-file artifact. **Ten consecutive
days with no 09:00 run.** The ADR-76 gate ("confirmed reliable at n=1") is therefore not merely
un-discharged; the current evidence runs the other way.

*A precision correction to L-B, offered without diminishing its finding:* L-B's headline
reproduction day, 2026-07-21, has **no 09:00 run at all** (runs at 00:09, 00:44, 00:45, 00:47,
00:51, 00:52, 10:51 x2, 15:43, 23:50). The "high count matches the 09:00 scheduled run" correlation
is exactly reproduced on 07-23 and holds on the four other HAS-0900 days, but it is not the shape of
the day L-B reproduces in detail. The mechanism (tree identity, not clock time) survives intact.

**What stops firing if entry 1 is removed** - split into two groups, because they are separable:

- *Write legs (would stop):* the once-per-day `audit.py run`; the `ecosystem/<repo>/history/<date>.md`
  dailies; `ecosystem/<repo>/state.yaml` refresh; the `docs/audits/*-ecosystem-audit.md` rollup; the
  `automation/fleet-audit` lane commit and its origin push; the `logs/FLEET-HEALTH.md` digest refresh.
- *Surfacing legs (would ALSO stop, but need no audit run):* the >48h stale-digest line
  (`fleet_health.py:505-508`), the overdue-quarterly-groom escalation (`:509-516`), and the digest
  one-liner (`:517`). `main()` already prints all three on the no-run path (`:489-497`), so they are
  independent of the write legs.
- *Unaffected:* entries 2-5. They are separate command entries; removing one does not touch the others.

### Options

**Option RETIRE - delete the `fleet_health.py` SessionStart entry.**
- Cost to do: discharges the ADR-76 section 5 obligation and removes same-day multiplicity, which is
  the surface of the still-open leg-2 collision. One `settings.json` edit plus a `CLAUDE.md` section 9
  and `ARCHITECTURE.md` Ch2 lockstep.
- Cost of doing it: on today's evidence there is **no other producer** - the 09:00 task has missed 10
  consecutive days. The fleet-audit lane would go silent, and the check that would notice
  (`fleet_audit_replication`, `scripts/audit.py:3129`) measures replication LAG, not production, so a
  lane producing nothing reports `pass` at 0 commits ahead. Silence would look like health.
- What breaks: L0.5 (the ladder's "MATERIALLY ADVANCED" level) reverts to no recurring producer; the
  three surfacing lines disappear with it unless separately preserved.

**Option KEEP - leave all five entries as they are.**
- Cost to do: zero.
- Cost of not acting: ADR-76 section 5's clause stays undischarged and continues to read as a pending
  obligation; the un-fixed same-day cross-tree collision (`BACKLOG.md:266`) keeps its exposure surface,
  and the 2026-08-02 manual union (`55733ea4`) is the precedent for what that costs when it bites.
- What breaks: nothing today - but the scheduler's 10-day outage stays unowned, and nothing in the
  repo currently alarms on it.

**Option INVESTIGATE-FIRST - keep the entry; make the scheduler's firing record a checkable fact
before ruling.**
- Cost to do: one attended check of the Windows `\fleet-baseline` task (registered by
  `scripts/setup-fleet-scheduler.ps1`, default `-At 09:00`, `ExecutionTimeLimit` 15 min) plus,
  optionally, a small production-freshness check so "no daily written today" becomes visible.
- Cost of doing it: defers the ruling by one window; the ADR-76 clause stays open a little longer.
- What breaks: nothing.

**Option SPLIT (not in L-B's enum; named because it is separable) - keep `fleet_health.py` at
SessionStart in surface-only mode, move the audit run wholly to the scheduler.**
- Cost to do: a flag or a second entry point; the three surfacing legs already run without the audit.
- Cost of doing it: only defensible AFTER the scheduler is confirmed firing - otherwise it is Option
  RETIRE with extra steps and the same silent-lane outcome.
- What breaks: nothing structurally; it is the shape ADR-76 section 5 actually describes.

### Recommendation

**INVESTIGATE-FIRST.** The question's premise (the trigger is the collapse source) was falsified by
`56f82aaf`, and the lane shows the scheduled task has not run in 10 days - so retiring the trigger
today would remove the only live producer.

---

## B-3 - file the ratchet FAIL at n=1?

**The question, verbatim** (`...-lb-fleet-audit-commits.md:161`):

> | B-3 | File the `silent_rule_ratchet` FAIL at n=1, or wait for a second daily? | file-now / watch / fold-into-465 |

### Current state

**What "ratchet" means here.** It is not a general term - it is the `[#436]` silent-rule ratchet, a
registered `audit.py` check that gates the GROWTH of the silently-unenforced rule pool.
`scripts/audit.py:2854-2857`: *"[#436] silent-rule ratchet - gate the GROWTH of the silently-unenforced
rule pool. Registered in ALL_CHECKS, so it is a ship-gate leg by construction."* Its committed baseline
is `ecosystem/silent-rule-baseline.yaml` (`scripts/silent_rule_detector.py:99`), whose own header states
the invariant: *"`baseline` may be LOWERED or held. It may NOT be raised. ... There is no code path that
raises it: lowering is a reviewed commit, raising is an operator ruling."*

**What "n=1" means here.** Two distinct senses live in the repo and the ruling turns on the first:

1. *Observation count* - the sense in B-3. The FAIL was seen on exactly one day.
   `...-lb-fleet-audit-commits.md:126-128`: *"`pass` on 07-28, 07-29, 07-30, 07-31 ('live N <= baseline
   N'); **`fail` for the first time on 08-01**, the window's last day, so persistence is n=1 and cannot
   be extended further from this evidence."*
2. *Instance count* - `CLAUDE.md:165` marks `roster-freshness` as `HUB-ONLY (n=1)`, meaning one
   instance of the mechanism exists fleet-wide. Same notation, different question. Six other hub gates
   carry a bare `HUB-ONLY` (`CLAUDE.md:166-170, 176-177`).

**The finding, verbatim** (`...-lb-fleet-audit-commits.md:119-132`):

> **`silent_rule_ratchet` FAIL on the hub, first seen 2026-08-01.**
> `silent_rule_ratchet | fail | raise-guard INDETERMINATE: the baseline on the integration ref
> exists but is unreadable or malformed, so a raise cannot be ruled out (live 439, committed 441)`
> ... **No open row names this check** (`grep silent_rule_ratchet BACKLOG.md` -> nothing). **Hub
> work.** Too fresh to distinguish a real infrastructure problem from a one-off blip, but the FAIL
> text ("unreadable or malformed") describes a plumbing fault, not a policy breach.

**Verified independently, and the evidence has moved since.**

- The FAIL text matches the `ref_state == "invalid"` branch exactly (`scripts/audit.py:2802-2808`) -
  it fires when a `git show <ref>:ecosystem/silent-rule-baseline.yaml` lookup or parse fails against
  `origin/main` or `main` (`_BASELINE_REFS`, `scripts/audit.py:2662`). It is a read-path fault, not a
  measurement of the pool. The pool itself was BELOW baseline in the same file (`live 439, committed 441`).
- The 2026-08-01 daily contains both verdicts, 5 minutes apart:
  `11:32:11 -> pass ("live 439 <= baseline 441 ... 2 below baseline - ratchet-down available")`,
  `11:37:27 -> fail (raise-guard INDETERMINATE)`. L-B's second-order observation is confirmed.
- **Five subsequent observations, all `pass`.** Every 2026-08-02 run block (13:01:37, 13:04:35,
  16:59:21, 21:03:22, 21:04:20) reports `silent_rule_ratchet | pass | live 441 <= baseline 441 under
  detector silent-rule-v4 (56 file(s) in scope)`. **n is still 1, and there are now five clean
  observations after it, not zero.**
- `grep -c silent_rule_ratchet BACKLOG.md` -> **0**. Still no open row names the check.

### Options

**Option FILE-NOW - open a row for the indeterminate raise-guard read.**
- Cost to do: one P3-size-S row, plus a `kill-candidates:` line (the `backlog-filing-backpressure`
  commit-msg hook BLOCKS an add without one, `CLAUDE.md:176`). Files against Section F, which the same
  night's L-F lane reports as already being violated 5:2.
- Cost of doing it: on the current evidence the row would describe a transient that has not recurred
  in five subsequent runs - the 2026-07-09 precedent (39/39 auto-proposals rejected at triage) and
  L-F's own 4/4 groom rejections both name filing-on-thin-evidence as the local failure mode.
- What breaks: nothing mechanically. The cost is precedent: n=1 becomes a sufficient filing bar.

**Option WATCH - do not file; re-read the check's verdicts at the next window and file only on n>=2.**
- Cost to do: zero now. Needs a named place to look, or it degrades into forgetting - the honest
  version is one line in the window's report, not an unrecorded intention.
- Cost of not filing: if the read fault is real and intermittent, a FAIL on this check is a ship-gate
  blocker (`Registered in ALL_CHECKS, so it is a ship-gate leg by construction`), so it will announce
  itself loudly rather than rot silently. That is the argument that watching is cheap here.
- What breaks: nothing. The check is self-surfacing; deferral does not hide it.

**Option FOLD-INTO-465 - treat it as texture on the writer-integrity row.**
- Cost to do: nothing new is filed. But `[#465]` is about the fleet-audit WRITER (what gets recorded);
  this is a READER fault inside one check's raise-guard (`audit.py:2721-2762`). Different subsystem.
- Cost of doing it: mis-scopes `[#465]`, whose Done-when is *"last-run-wins is accepted on record and
  tag-canonicity is fixed or retired"* (`BACKLOG.md:266`) - unrelated to this failure.
- What breaks: the row's closure test would then depend on evidence it does not name.

**The doctrinal question underneath, stated plainly.** What does a mechanism with a single observed
instance justify? This repo already answers it in one direction and its own precedents in the other:
ADR-76 section 5 makes n=1 a sufficient bar to RETIRE a redundant mechanism; ADR-93 and the [#244]
arc treat n=1 as sufficient to PROVE a built mechanism; L-F's groom review and the 39/39 precedent
treat n=1 as insufficient to FILE a defect. Those are consistent only if the bar is read as
asymmetric by consequence, not by count: n=1 proves a capability (one witnessed success is
existence), and n=1 does not establish a pattern (one witnessed failure is not a rate). The ruling
is whether to write that asymmetry down as doctrine, or to keep deciding it case by case.

### Recommendation

**WATCH.** The FAIL is a read-path transient with five clean observations after it, and the check is
a ship-gate leg that will re-announce itself if it is real - so filing now buys nothing the mechanism
does not already do.

---

## B-4 - lineage authority

**The question, verbatim** (`...-lb-fleet-audit-commits.md:162`):

> | B-4 | Two lineages record the same dailies (`main` vs `automation/fleet-audit`). Which is authoritative? | branch-authoritative / main / reconcile |

**Source paragraph** (`...-lb-fleet-audit-commits.md:151-153`):

> One reconciliation item, out of this probe's scope: a smaller HEAD-only lineage
> (`d16f7120`/`0ed63e4f`) independently recorded some of the same 07-31 dailies on `main` and is
> **not** an ancestor of `automation/fleet-audit`. Two lineages record overlapping days.

### Current state

**The brief's premise needs correcting before the ruling is framed.** The brief states the lineage
mechanism "now gates nothing after the Act-1 lossless union". The phrase "Act-1 lossless union" does
not appear in the repo (`grep -i lossless` over `docs/` returns no such phrase) - **UNVERIFIABLE as
quoted**. Its referent is identifiable: commit `55733ea4` (2026-08-02 19:30:50), *"restore the
2026-08-02 dailies as the lossless UNION of all three runs"*, recorded in `JOURNAL.md:62-93` as the
2026-08-02 (e) entry. Read live, that commit unified **three RUNS of one day inside the lane** (the
13:01 and 13:04 lane copies plus the 16:59 worktree copy), not the two LINEAGES:

> Union, chronological, strictly additive -- each entry byte-preserved in canonical LF space:
> .dev-knowledge : 13:01:37 + 13:04:35 (lane) + 16:59:21 (worktree)  13464 -> 20197 B
> diffstat       : 54/0 and 43/0 -- zero deletions

`JOURNAL.md:73` records where it landed: *"Committed to `automation/fleet-audit` only (lane
ownership, ADR-80/84)"*. **So the union did not touch the main-side lineage and did not merge the two.
The B-4 split is exactly as it was.**

**The two lineages are near-disjoint, not overlapping.** Set-diff of
`ecosystem/.dev-knowledge/history/` between `HEAD` and `origin/automation/fleet-audit`:

|lineage|dates|count|
|---|---|---|
|HEAD (main-side) only|2026-05-15, 05-16, 05-23, 06-02 .. 06-14|16|
|lane only|2026-06-15 .. 08-02 (with gaps)|45|
|both|2026-07-31|1|

Totals: 17 tracked on HEAD, 46 on the lane. **Neither lineage alone is the complete record** - the
main side is the sole holder of everything before 2026-06-15.

**The one shared date is not equal.** `ecosystem/.dev-knowledge/history/2026-07-31.md`:
HEAD blob `418ae3d9` (12292 B, two run blocks: 10:26:21, 11:55:35); lane blob `81b76acb` (18437 B,
three: 10:26:21, 11:55:35, **12:34:25**). The lane copy is a strict superset. Adopting main as
authoritative for that date would silently drop a run.

**Does lineage gate anything today? Verified: no.** Every mechanism that touches the lane reads the
lane against ITSELF or against origin, and none consults `main`:

- `scripts/audit.py:3129-3184` `check_fleet_audit_replication` compares
  `refs/remotes/origin/automation/fleet-audit` against `refs/heads/automation/fleet-audit`. It never
  reads `main`. Its own docstring names the honest limit: *"it measures lag against the last-known
  origin, so a very stale fetch understates it."*
- `scripts/session_end_backpressure.py:354-379` `_on_lane()` blob-compares a working-tree daily
  against `_LANE_REFS = ("automation/fleet-audit", "origin/automation/fleet-audit")`. Also never `main`.
- The dailies have no reader at all. `ADR-84:19` states it as a ratified fact: *"no hard consumer pins
  either output to `main`. The baseline has zero readers (`audit.py` writes but never reads a prior
  baseline; `docs/audits` is excluded from its checks)."* `scripts/scan_undeclared_edges.py:77,99`
  excludes `ecosystem/*/history/` from prose-edge scanning as well.

So the brief's conclusion is right for the wrong reason: lineage gates nothing - but it gated nothing
before the union too, and the union is not why.

**This is a doctrinal ruling, not a mechanical one.** Nothing is currently broken and no gate is
waiting on an answer. What is at stake is what the durable record MEANS: ADR-80 section (b) commits
the writer to a *"durable record (`history/*.md`, digests, the `docs/audits/*-ecosystem-audit.md`
rollup)"*, and a record split across two non-ancestral lineages with one unequal shared date has no
single answer to "what did the fleet look like on date D". The question is which artifact a future
reader is entitled to trust, before a reader exists to be misled.

### Options

**Option BRANCH-AUTHORITATIVE - `automation/fleet-audit` is the record of account.**
- Cost to do: a one-line doctrine statement (ADR-80/84 amendment or a CLAUDE.md line). Matches every
  live mechanism, which already reads only the lane. Matches ADR-84's orphan-branch design.
- Cost of doing it: the 16 main-only dates (2026-05-15 .. 06-14) become an orphaned record that the
  doctrine does not cover. They stay on `main` as tracked files with no declared status.
- What breaks: nothing mechanically. The exposure is the pre-06-15 era's provenance.

**Option MAIN - `main` is the record of account.**
- Cost to do: would require back-porting 45 lane-only dates onto `main`, reversing ADR-84's writer
  isolation, and re-dirtying the tree that ADR-80's writer policy exists to keep clean.
- Cost of doing it: contradicts three landed ADRs (80, 84, and the [#476] lane-ownership fix in
  `session_end_backpressure.py`), and re-opens the stash-ship-pop problem ADR-80 decommissioned.
- What breaks: the `_on_lane()` exclusion and `check_fleet_audit_replication` both lose their meaning.

**Option RECONCILE - declare the lane authoritative from a stated date and absorb the main-only era
into it (or explicitly retire the main-side copies as superseded).**
- Cost to do: one commit on the lane adding the 16 main-only dates, plus a ruling on the 2026-07-31
  duplicate (the lane copy is already the superset, so "keep the lane copy" is lossless there). The
  `55733ea4` union is the working precedent for how to do it additively with zero deletions.
- Cost of doing it: touches immutable-class durable records; needs the same byte-preservation
  discipline the union used, and the operator's explicit word before any lane write.
- What breaks: nothing, if done additively. Done carelessly it destroys records - which is exactly the
  failure the union commit was written to avoid.

### Recommendation

**BRANCH-AUTHORITATIVE, with the 16 main-only dates explicitly dispositioned in the same ruling.**
Every live mechanism already reads only the lane, so this ratifies what is true rather than building
anything - and naming the pre-06-15 era in the same sentence is what stops it becoming a silent orphan.

---

## Section F -- numeric target (no number recommended)

> **CONSTRAINT, stated explicitly and binding on this section: this report does NOT recommend a
> number, and does NOT recommend a definition. The number is the operator's ruling alone. What
> follows is (1) what the night ladder established, including both refuted figures, and (2)
> candidate ways to DEFINE what a number would measure, each with the gate that would enforce it.**

### What the night ladder established

**The requirement, verbatim** (`docs/intake/2026-07-30-func-operator-decision-routing-and-standards.md:75-80`):

> ## F. Backlog equilibrium (raise the 08-26 cluster's rank)
> The backlog must SHRINK - that is a functional requirement, not a review item. The 08-26 cluster
> (scoring/Fibonacci scale, drain, D-queue, caps-as-equilibrium incl. file-size legs) is the
> mechanism; its entry gate stays the section 3.2-vs-[#364]-4(a) reconciliation. tasks/ in root:
> confirmed good.

Intake #22 was ratified by ADR-108 for **sections A and B only** (`ADR-108` header: *"Intake: #22 ...
- **§A and §B only**"*); section F is listed at `ADR-108:62` as still-unratified material. So section
F is an operator functional statement, not yet ADR-borne.

**The ladder's finding** (`docs/audits/2026-08-02-technical-night-ladder-and-plan-audit.md:30-33`):

> **§F is being violated, and it has no number to be violated against.** The backlog went **183 ->
> 186** (filed 5, closed 2), peaking at 194. At that rate the 2026-08-26 projection is **≈195-210
> rows**, not fewer. §F states a direction ("must SHRINK") and no target - so the first thing owed is
> a number, not a plan.

**Live re-derivation tonight (2026-08-03), independent of the report:**

```
tasks/manifest.json task nodes                   186
BACKLOG.md rows matching ^- [#N]                 186   (window_metrics.count_backlog_rows)
  of which carry the DEFER marker                 29
  therefore open                                 157
priority   P1 5 / P2 86 / P3 95
size       S 113 / M 67 / L 6
tasks/*.md files on disk                         213   (was 209 at a02dd111; 4 more closed since)
```

Every L-F distribution figure reproduces exactly. The two independent counters agree at 186.

### The two refuted figures

**REFUTED FIGURE 1 - "+52.8 adds/week".** Quoted from
`docs/audits/2026-08-02-technical-night-batch-lf-backlog-health.md:120-126`:

> **REFUTED - a figure that must not propagate.** A rate of "+52.8 adds/week, backlog growing at
> +52.2/week" was derived in-lane from `git log --diff-filter=A -- tasks/` over the last four weeks.
> It is an **artifact of the ADR-107 migration**: of ~211 file-adds in that span, **174 came from the
> single commit `9bd0d719`**, which generated the tasks/ tree rather than filing work. The true
> filing rate is 5 per window. Recording the refutation here because intake #16 §5 lesson 6 ("Verify
> numbers before they propagate") names exactly this failure class, and the 10-20-repo incident is
> its precedent.

*Why it was refuted:* the measurement instrument (file-add dates in `tasks/`) does not measure the
thing (rows filed). One migration commit created 174 of ~211 adds, so the rate measured a one-time
tree generation. The same defect independently invalidates the staleness scan
(`...-lf-backlog-health.md:77-87`: *"That result is **vacuous, not clean**"*) - `9bd0d719` reset every
task file's git date, so nothing in `tasks/` can appear older than 2026-07-27.

**REFUTED FIGURE 2 - "target 150 rows (25% reduction)".** Quoted from `...-lf-backlog-health.md:128-129`:

> Likewise **refuted**: a "target 150 rows (25% reduction)" figure. No such target exists in §F or
> anywhere else in the repo. It was invented in-lane. **Do not adopt it.**

*Why it was refuted:* it has no source. Verified live tonight - the only in-repo 2026-08-26 references
are `BACKLOG.md:329` (the silent-rule drain `review_date`) and rows `[#348]` / `[#426]`, and
`...-lf-backlog-health.md:131-133` states their character: *"These are gates *at* the date, not a
count target."* Section F's own text names a mechanism (the 08-26 cluster) and no figure.

**The shape of the two refutations differs and both shapes matter to the ruling.** Figure 1 was a
real measurement of the wrong thing; figure 2 was not a measurement at all. A definition ruling must
survive both failure modes: it must name an instrument that measures rows-as-work (not files-as-artifacts),
and its number must have a stated source rather than a plausible-looking derivation.

### Candidate target definitions, and how each would be gated

Four candidates. **None is recommended.** Each is stated as: what it measures - where the gate lives -
what it asserts - what failure looks like - what it costs.

**CANDIDATE 1 - gross row count (what "186" means today).**
- *Measures:* every `^- [#N]` row in `BACKLOG.md`, deferred included. Today 186.
- *Gate:* a new registered `audit.py` check against a committed baseline file, modelled directly on
  `check_silent_rule_ratchet` (`scripts/audit.py:2854`) + `ecosystem/silent-rule-baseline.yaml`.
  Registration in `ALL_CHECKS` makes it a ship-gate leg by construction, and `audit.py health` is
  already a pre-commit gate where FAIL blocks the commit (`CLAUDE.md:172`).
- *Asserts:* `live_rows <= baseline`, ratchet-down-only - the baseline may be lowered or held by a
  reviewed commit and may never be raised by one (`silent_rule_detector.validate_transition`), with
  the same raise-guard read against `origin/main`/`main`.
- *Failure looks like:* `backlog_equilibrium | fail | backlog GREW: live 189 > baseline 186 (+3) -
  close rows or record an operator ruling; the baseline does not rise on a commit`. The commit that
  files the 187th row is blocked at `audit.py health`.
- *Costs:* the simplest and cheapest to build; both counters already agree at 186. But it makes
  filing a new row a gate event, which collides with `backlog-filing-backpressure`'s existing
  proposals-only posture, and it counts 29 deferred rows that no one intends to execute.

**CANDIDATE 2 - open-row count (deferred excluded).**
- *Measures:* rows without the `· DEFER` marker (`gen_task_tree._DEFER_MARKER`,
  `scripts/gen_task_tree.py:106,224`). Today 157. Computable from `BACKLOG.md` alone - no `tasks/`
  dependency - because the marker is in the row text.
- *Gate:* identical host and mechanics to candidate 1; only the counting function differs.
- *Asserts:* `live_open <= baseline_open`, ratchet-down-only.
- *Failure looks like:* the same FAIL line, keyed to the open count.
- *Costs:* it answers F-2 by construction (deferred stops counting) - and thereby creates the loophole
  the operator must price: **marking a row `· DEFER` becomes a legal way to satisfy the gate.** A
  batch deferral of 29 rows would read as a 29-row shrink. Any adoption needs a companion constraint
  on the defer transition itself, or the metric is trivially gameable.

**CANDIDATE 3 - per-window flow invariant (equilibrium, not a level).**
- *Measures:* not a target count at all, but `closed >= filed` across a window range.
  `scripts/window_metrics.backlog_delta` already computes filed / closed / net across a git range and
  reports them separately.
- *Gate:* a ship-gate or session-end leg asserting `net <= 0` over the declared window range, rather
  than an `audit.py` per-commit check.
- *Asserts:* no window may end having filed more rows than it closed.
- *Failure looks like:* the window cannot close - the ship or wrap step refuses while `net > 0`.
- *Costs:* it directly targets the observed defect (filing outran closing 5:2) and needs no invented
  number. But it requires a machine-readable window BOUNDARY, and `window_metrics.py` explicitly
  refuses to supply one: *"windows-to-cutoff - a judgment INPUT, not an observation ([#461]). A
  computed-looking number here would launder an estimate into a measurement"* (`:11-16`). Adopting
  this means first ruling how a window boundary becomes a committed fact.

**CANDIDATE 4 - dated target with no standing gate (directional-only, the explicit null option).**
- *Measures:* a count at a date, checked by a human at 2026-08-26.
- *Gate:* none. The existing `BACKLOG.md:329` `review_date: 2026-08-26` pattern is precisely this
  shape, and `...-lf-backlog-health.md:131-133` already characterises those as *"gates at the date,
  not a count target."*
- *Asserts:* nothing mechanically.
- *Failure looks like:* nothing fires. Detection is a person reading a number on a date.
- *Costs:* zero to build and impossible to game. But it reproduces the status quo the ladder calls a
  passive failure, and it is the option F-1 names as *"an explicit 'directional only, no gate'"* -
  which is a legitimate ruling, not an absence of one, provided it is recorded as chosen.

**A gating fact that binds all four.** Whatever definition is chosen, the ratchet template's own
header states the discipline it would inherit (`ecosystem/silent-rule-baseline.yaml:10-18`): the
committed artifact must be *"a NUMBER plus the DETECTOR ID that produced it"*, because *"counts from
two different detector contracts are not commensurable; the check refuses to compare them rather than
silently reporting drift."* Refuted figure 1 is exactly that failure. A Section F baseline without a
pinned counting contract would reproduce it.

**The operator's three questions, unchanged and unanswered here**
(`...-lf-backlog-health.md:181-183`):

|#|Question|Decision shape|
|---|---|---|
|F-1|What is the §F target number at 2026-08-26? Direction alone cannot be gated.|A number, or an explicit "directional only, no gate"|
|F-2|Do `deferred` rows (29) count against the §F number?|Yes / No / re-disposition them as a batch|
|F-3|Is a filing-rate cap wanted, given filing outran closing 5:2?|Cap / no cap / cap only on P3-size-S|

---

## Coverage

**Verified live, with the probe named.**

- All four source findings located and quoted from disk, not from the brief. B-2 / B-3 / B-4 are
  `...-lb-fleet-audit-commits.md:160-162` (section 7 table) and are mirrored at
  `...-night-ladder-and-plan-audit.md:340-342`. The Section F material is
  `...-lf-backlog-health.md` sections 1 and 5 and `...-night-ladder-and-plan-audit.md:30-33, 44-55`.
  **Nothing was un-locatable; no finding was reconstructed or inferred.**
- SessionStart roster: `.claude/settings.json` read in full; all five scripts confirmed present on
  disk with byte counts; `CLAUDE.md` section 9 cross-checked and consistent.
- The [#465] legs 2+3 fix: commit message, `BACKLOG.md:266`, and `scripts/audit.py:417-427` all read
  directly.
- The WARN-collapse mechanism and its disappearance: reconstructed from every superseded lane commit
  (not just the tip), for 2026-07-21, 07-23, 07-26, 07-27, 08-01, 08-02, cross-checked on ai-council.
- The 09:00 scheduler gap: enumerated for all 18 days 2026-07-16 .. 08-02 by replaying each
  superseded commit's file content; cross-checked on a second repo.
- The ratchet: `pass`/`fail` verdicts read from the committed dailies for 08-01 and all five 08-02
  blocks; `grep -c silent_rule_ratchet BACKLOG.md` = 0 re-confirmed.
- Lineage split: `git ls-tree` set-diff HEAD vs `origin/automation/fleet-audit`; both blobs of the one
  shared date compared by hash, size and heading list.
- Backlog counts: re-derived two ways (task manifest nodes; `window_metrics.count_backlog_rows` over
  live `BACKLOG.md`), plus the DEFER-marker split. Both agree at 186 / 157 / 29.

**Could not verify.**

- **The phrase "Act-1 lossless union" is not in the repo.** UNVERIFIABLE as quoted; the referent was
  identified (commit `55733ea4`, JOURNAL 2026-08-02 (e)) and the brief's inference from it is
  corrected in B-4 rather than repeated.
- **Whether the Windows `\fleet-baseline` scheduled task is registered or enabled.** Machine-local
  state, not reachable from this container. UNVERIFIABLE - only its OUTPUT (the 09:00 run rows) was
  checked, and the 10-day gap is an absence of output, which is consistent with a disabled task, a
  changed trigger time, or a machine that was off. **The ruling should not treat "no 09:00 rows" as
  proof the task is broken.**
- **Gate verdicts.** `uv run --locked` is unavailable here (ADR-106 pins `uv==0.11.19`; the box has
  `0.8.17`), so the two python probes ran in an isolated scratchpad venv. Container results are not
  gate verdicts and none is offered as one. `pytest` was not run.
- **Why the 2026-08-01 11:37 raise-guard read failed.** The FAIL branch is identified exactly
  (`ref_state == "invalid"`, `scripts/audit.py:2802-2808`) but the transient git condition that
  produced it on that run is not recoverable from committed state.

**Deviations from the brief, disclosed.**

- **Frontmatter.** The brief asks for YAML frontmatter matching sibling files. The 2026-08-02
  night-batch siblings (`-lb-`, `-lc-`, `-ld-`, `-le-`, `-lf-`) carry **no YAML frontmatter** - they
  use an H1 followed by a bold-key bullet block (Class / Date / Slug / Status / Base / Method). This
  file matches the siblings, since "match sibling files exactly" and "add YAML frontmatter" cannot
  both hold. 47 older `docs/audits/*.md` do use YAML; the night-batch class does not.
- **ASCII.** Authored prose is ASCII. **Verbatim quotes preserve their source characters** (including
  em dashes, middle dots and section signs) - transliterating a quote would make it not a quote. No
  box-drawing glyph appears anywhere in this file; tables are unpadded.
- **FILENAME - this file's own path violates ADR-101 Rule B and will be BLOCKED at commit.** The
  brief mandated `docs/audits/2026-08-03-night-lf-rulings-prep.md`, and it was written there as
  instructed. Verified against the live validator:
  `validate_hermetization.rule_b_violation('docs/audits/2026-08-03-night-lf-rulings-prep.md')` returns
  *"class: ... has no CLOSED-enum <class> token after the date (ADR-101 R3:
  technical/functional/qa/census/verification/ecosystem-audit/conformance-nightly-digest/changelog-review/codex/fresh-eyes/incident-evidence)"*.
  `night` is not in `AUDIT_CLASS_ENUM` (`scripts/validate_hermetization.py:89-100`). The
  `validate-hermetization` pre-commit hook fires on staged ADDs under `docs/audits/`, so this file
  cannot be committed at this name without `--no-verify`. **Remedy, verified to pass:** rename to
  `docs/audits/2026-08-03-technical-night-lf-rulings-prep.md` (`rule_b_violation` -> `None`), which
  also matches the sibling naming exactly.
- **The generated audits index is now stale.** `docs/audits/README.md` is regen-and-diff gated by the
  `audit-index-freshness` pre-commit hook and by `tests/test_gen_audit_index.py::test_live_index_is_fresh`.
  Adding this file makes both fail until `python scripts/gen_audit_index.py --write` is run. That is a
  `--write` invocation and was therefore **not** run here, per this lane's read-only rails. The
  2026-08-02 batch hit the same condition and ran the sanctioned regen at integration time.

**Rails observed.** Read-only over all governed content. No existing file was edited; no commit,
checkout, merge or stage; no generator run with `--write`/`--fix` (`gen_task_tree.py --check` only,
which reported `check ok`); no branch, ref or working-tree mutation. Exactly one file was created -
this one. `git status --porcelain` was clean at entry and shows only this new untracked file at exit.

---

*Read-only night batch, unattended, 2026-08-03. Every section above is a ruling INPUT; the operator
rules. Section F contains no recommended number and no recommended definition, by design.*

---

> **Editor's note (wrap, lane L-A) — this file was RENAMED before commit.** It was written to
> the brief's mandated path `docs/audits/2026-08-03-night-<lane>.md` and is committed as
> `docs/audits/2026-08-03-technical-night-<lane>.md`. Reason: the mandated pattern is refused
> by this repo's own `validate-hermetization` Rule B — `night` is not a member of the ADR-101
> R3 closed class enum (`scripts/validate_hermetization.py:89-98`). Inserting the `technical`
> class token is what every 2026-08-01/02 night-batch sibling already does. **The gate was not
> weakened, bypassed or amended.** Any occurrence of the old `2026-08-03-night-...` form below
> is preserved deliberately as the evidence that produced this finding — it is a quotation of
> the blocked name, not a live path. Verified post-rename: `rule_a_violation` and
> `rule_b_violation` both return `None` for all seven artifacts of this batch.
