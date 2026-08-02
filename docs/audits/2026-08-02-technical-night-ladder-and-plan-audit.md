# Night batch 2026-08-02 — morning ladder report + repo-plan audit (INDEX)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-02 · **Slug:** night-ladder-and-plan-audit
- **Status:** **PROPOSAL — every lane below is for the morning architect to promote or reject.**
  Nothing was decided, filed, closed, renamed, or ratified overnight.
- **Base:** `main` = `a02dd111` — verified as the post-handoff window-close tip, carrying the
  eod-completion merge (`31c80714`) and the sealed bundle `2026-08-01-dev-knowledge-architect-2`.
  Open count **186**, as expected by the brief.
- **Lane reports:** L-B · L-C · L-D · L-E · L-F each have their own file under `docs/audits/`
  (linked in their section below). **L-A is here in full** — it is the report you read with coffee.

---

## EXECUTIVE SUMMARY

1. **The fleet plan is one row from unblocked.** [#382] closed and the contract, loader and
   divergence report all exist. **[#383] is now the single keystone** — L0 convergence, L2
   deployment and the whole L4 lane serialize behind it, and nothing blocks it.
2. **The window shipped a great deal of machinery and moved the needle zero.** A live divergence
   run tonight returns `conform: 185 · diverge: 3 · declared: 3 · n/a: 219` — **byte-identical to
   the 2026-07-31 baseline.** 22 merges, five new organs (`check_fleet_audit_replication`,
   `check_membership_agreement`, `check_intake_tree_coherence`, `window_metrics.py`,
   `gen_intake_tree.py`), same numbers. The machinery got better at *seeing*; nothing yet
   *converges*.
3. **The biggest finding of the night is in the fleet-audit lane.** [#465]'s legs (2) and (3) are
   not two bugs but **one**: the hub misresolves as not-the-hub, its hub-only checks skip, and
   their WARNs vanish from the day's record. Reproduced exactly — 16 WARNs at 00:51 collapsing to
   2 at 10:51, the missing 14 being precisely the three hub-only checks — and recurring on **8 of
   10 multi-commit days**.
4. **§F is being violated, and it has no number to be violated against.** The backlog went
   **183 → 186** (filed 5, closed 2), peaking at 194. At that rate the 2026-08-26 projection is
   **≈195–210 rows**, not fewer. §F states a direction ("must SHRINK") and no target — so the
   first thing owed is a number, not a plan.
5. **On AGENTS.md: hold.** This repo already ran the experiment — ADR-52 adopted AGENTS.md and
   **ADR-53 superseded it the same day on a sentinel test**. Claude Code still does not read it
   natively, and Codex already reads `CLAUDE.md` via a config knob. But one piece of the
   operator's question should be actioned regardless: **§12 is 45.4% of CLAUDE.md by bytes** while
   reading as 8% by lines.

**Also flagged (L-E):** the fleet's hand-rolled version comparator is **wrong in two directions** —
`0.15.5rc1` parses as `(0,15,51)`, comparing *greater* than its own release. Dormant only because
`ruff` is pinned exactly. `packaging` is already in the tree, so the fix costs no new dependency.

### §F trajectory to 2026-08-26

```
open at 2026-08-01      186   (157 open + 29 deferred — the headline hides the split)
this window             183 -> 186   filed 5, closed 2, net +3   (peak 194 mid-window)
days remaining          25
windows remaining       3-8    JUDGMENT INPUT, not computed — recent windows ran 2-11 days
                               (window_metrics.py refuses to derive this, by design)
projection at +3/window 195-210 rows at the cutoff — the requirement fails passively
to merely HOLD          closing must rise from 2 to 5 per window (2.5x)
to SHRINK               closes must exceed files every window
```

### Top three next-window moves

| # | Move | Why it is first |
|---|---|---|
| 1 | **Run [#383] wave 1 against one surface** | The only unblocked keystone. L0 convergence, L2 deploy and [#385]'s whole L4 lane all `depends-on` it. Wave-done is mechanical: zero undeclared divergence for that surface. |
| 2 | **Re-scope [#465] to one root cause and fix the hub self-misresolution** | It is one bug, not two (L-B). Until it is fixed, the fleet-audit surface silently loses ~14 WARNs on most days — so every "clean" reading from that lane is untrustworthy. |
| 3 | **Rule §F: set the number, or disposition the 29 deferred rows** | The backlog grew this window against a functional requirement that it shrink, and no target exists to gate against. The 29 deferred rows are the cheapest single lever available. |

---

## L-A — THE MORNING LADDER

### Step 1 — the definition source, quoted

The ladder is **repo nomenclature**, not general terminology. Levels L0–L5 are defined by the
**intake #16 §1 layer table** (`docs/intake/2026-07-21-func-fleet-north-star.md:48–55`), quoted
verbatim:

| Layer | Scope | Today |
|---|---|---|
| **L0** | Names + folder/file structure as managed state (caches, `.claude` surface incl. skills, archives-inside-each-folder, docs layout) | ~25% — fragments, 4 registries, no single contract |
| **L1** | Dependency architecture: doc2doc + doc2file edges, hooks, skills; rot detection from day one | ~45% — ADR-88/89, doc-code-edge.yaml, freshness checks live |
| **L2** | Methodology versioning + deployment: PLAYBOOK, CLAUDE.md, managed files, review system | ~40% — manifest/carriers half-built (editor-config `implemented:false`) |
| **L3** | Full lifecycle: intake → ADR → build → archive → real deletion; Q&A, looping, harness | harness ~80% (proven today); archive/safe_remove decided, unbuilt |
| **L4** | Tech-currency: research new Python tech/versions online → rule → **distribute** through the deploy channel | ~5% — one-offs only |
| **L5** *(new, 2026-07-21)* | **Predictive layer:** a local model that learns from how we work — logs, decisions, file traffic — so the fleet predicts dependencies, finds rot, flags risk ("the repo learns us") | 0% — designed below |

> **The "Today" column is the 2026-07-21 reading and is now 12 days stale.** It is quoted because
> it is the definition of record; every status line below is re-derived from live `main`, not
> carried from this column.

**The two half-steps are operator additions**, absent from the table above. Both are recorded in
`docs/audits/2026-07-31-verification-382-ladder-evidence.md` — the [#382] closure evidence pack,
which states its own scope as *"Ladder levels are intake #16 §1's layer table … with the
operator's half-steps L0.5 / L3.5 added"*:

- **L0.5** — the night / fleet-audit lane. Defined at that file's **line 35**:
  *"is the night lane RECURRING on main? · NO ON MAIN; machine-local only"*.
- **L3.5** — the reconcile loop. Defined at **line 139**:
  *"the reconcile loop (report runs on a cadence, output read by someone) · NOT DONE"*.

**No level is UNDEFINED-IN-REPO.** All eight carry a definition and an evidence anchor.

### Step 2 — status from live `main` (`a02dd111`)

> Divergence figures below come from a live run of `scripts/desired_state_report.py` executed
> tonight. **Caveat, per doctrine:** `uv run --locked` is unavailable in this container (the
> ADR-106 pin requires `uv==0.11.19`; the container has `0.8.17`), so the run used an isolated
> scratchpad venv. The *numbers* are live; the *environment* is not the locked gate environment.
> The working tree was verified byte-clean before and after.

---

**L0 — structure as managed state · PARTIAL, and unmoved**

- **Live:** `conform: 185 · diverge: 3 · declared: 3 · n/a: 219` — **identical to the 2026-07-31
  run at `f7abe228`.** The declaration layer sees the fleet; nothing converges it. "Conform" still
  means *no divergence declared*, not a probe result.
- **This window changed:** [#383] wave 1 split `docs/intake/` into per-item nodes + a residue
  carrier (`9a75777`, `597c81a`), discharging ADR-109 §4; `check_intake_tree_coherence` armed as a
  gate; `terminal-setup` registered as the 9th declared repo (`c7c2905`);
  `check_membership_agreement` landed ([#462], `d48ebd6`), diffing ADR-104's declaration against
  every machine surface — which is how "9 governs" became mechanically checkable.
- **Next action:** [#383] — converge **one** surface until the report shows zero undeclared
  divergence for it.
- **Remainder:** not separately estimated; L0 *is* the body of [#383].

**L0.5 — the night / fleet-audit lane · MATERIALLY ADVANCED**

- **Live:** the durability half is **done**. [#460] closed (`9faef8dd`) — replication mechanized,
  push leg + divergence alarm live, origin current — and `check_fleet_audit_replication` is now a
  registered check. Verified independently tonight: `origin/automation/fleet-audit` carries
  **exactly 51 commits** in 2026-07-17 → 08-01, tip `63b772fc`. The "unpushed, unread" era is over.
- **Still open:** no repo-declared scheduler. `.github/` does not exist and the GitHub API reports
  **0 workflows**. The recurring mechanism remains a machine-local Windows Task Scheduler entry
  running the **system** interpreter — an ADR-106 divergence, since the scheduled path sits
  outside the locked environment the fleet moved to.
- **This window changed:** the lane went from write-only telemetry nobody read to a replicated,
  alarmed surface — and lane L-B read all 51 for the first time (see below).
- **Next action:** consume L-B's triage into [#463]/[#464], then rule the scheduler question.
- **Remainder:** ~1 window for the scheduler declaration; the consumption is L-B's output, ready now.

**L1 — dependency architecture · TYPED, NOT QUERIED**

- **Live:** unchanged. Schema v1, loader and report all exist and are closed with [#382]. Edges are
  **rows**; there is no graph and no rot query. networkx stays deliberately absent until a consumer
  is named (ADR-105).
- **This window changed:** nothing on L1 itself — [#382] closed at the window's open.
- **Next action:** [#383] supplies the graph's named consumer.
- **Remainder:** gated by [#383].

**L2 — methodology versioning + deployment · NOT DONE, unmoved**

- **Live:** `deploy/manifest-v1.4.0.yaml` targets **1.4.0**. Actual recorded deployments:
  hub `null` · ai-council `1.3.1` · corp-monorepo `1.2.0` *(by design, ADR-102 — do not "fix")* ·
  corp-ops `null` · corp-sca-time-automation `null`. **Three of five have nothing deployed**, and
  the highest anywhere is one minor behind the target. The report renders this as the
  `corpus-version` row: diverge · declared · diverge · diverge.
- **This window changed:** nothing.
- **Next action:** build the consumer write-through for the v1.4.0 carrier (`implemented: false`).
- **Remainder:** **3–5 windows** (ladder pack §L2).

**L3 — full lifecycle · HARNESS PROVEN AGAIN; ARCHIVE STILL UNBUILT**

- **Live:** intake → ADR → build → closure ran end-to-end again this window (22 merges on the
  first-parent spine). Archive and **real deletion** remain decided-but-unbuilt (ADR-107 §7.3
  step 4).
- **This window changed:** [#461] mechanized the six window metrics (`scripts/window_metrics.py`,
  `0216acb`) — notable because it **computes four and refuses two**, printing "NOT COMPUTED" with a
  reason rather than laundering an estimate into a measurement. [S24] set the retire-not-delete
  precedent at **story** level. [#459] ruled the codemap source-root and named the ADR-109 organ
  class (`bf373b1`).
- **Next action:** the genre-lifecycle engine — archive + real deletion.
- **Remainder:** not estimated in the ladder pack; the harness half is ~80% and the archive half 0%.

**L3.5 — the reconcile loop · NOT DONE, but UNBLOCKED**

- **Live:** nothing schedules the report; it prints to stdout and writes no artifact. This is not
  an inference — `window_metrics.py` declares drift-report runs **NOT COMPUTED** precisely because
  *"a run leaves no committed trace to count"*.
- **This window changed:** **the blocker cleared.** The ladder pack recorded the cadence question
  as *"blocked behind [#460], because putting a second write-only producer on a timer before the
  first one's consumer question is answered would repeat the exact defect [#460] names."*
  [#460] closed this window. **L3.5 is now the cheapest unblocked step on the ladder.**
- **Next action:** give the report a durable artifact + a declared ADR-105 consumer, then wire a
  cadence.
- **Remainder:** **2–3 windows**, no longer gated.

**L4 — tech-currency · ONE OF THREE ITEMS MOVED**

| Item | Live status | Change this window |
|---|---|---|
| Library/venv lane (ADR-106) | Hub done (`uv` pinned, `uv.lock` committed). Fleet **not** — consumer tier stays LOCAL. | none. *Confirmed live tonight: the pin is real and enforcing — this container's `uv 0.8.17` was refused.* |
| Gemini activation | **Not started.** Zero hits across `scripts/`, `.claude/`, `ecosystem/*.yaml`, `tasks/`. | none |
| repomix distiller | **MEASURED and REJECTED** — [#467] filed **and closed**. | **moved.** `--compress` is a byte-identical no-op on markdown (0% on 13/13 `protocols/` files vs −35.5% on Python); the live `PASTE_THIS.md` re-renders **larger**. The 24 anti-bluff invariants "passed" only because nothing changed — **vacuous, not safe**. |

- **Next action:** [#385] is gated on [#383]'s apply channel — without it a version proposal has
  nowhere to land and degrades back into a one-off.
- **Remainder:** **4–7 windows** floor, serialized behind [#383], not parallel to it.

**L5 — predictive · UNTOUCHED**

- **Live:** `scripts/fleet_analytics.py` exists as the [#384] L5a reporter but records the D1
  deviation — **PyDriller deliberately absent**, `git log --numstat` used instead (~60× faster and
  not installed). No frames on a cadence, no consumer, no model.
- **This window changed:** nothing.
- **Next action:** none scheduled. L5 is downstream of everything above.
- **Remainder:** not estimated; L5b is explicitly gated on L5a frames showing signal.

### Step 3 — the ladder, read as one picture

The 2026-07-21 diagnosis said *"the hardest layer (harness) is the furthest along; the simplest
(L0 as a system) is nearest zero."* **That is still true, and this window did not change it.**
What the window did change is the *quality of the seeing*: five new organs, a metrics surface that
refuses to guess, and a fleet-audit lane that finally replicates. The convergence half — the part
that actually moves L0 — is entirely contained in [#383], which nothing blocks.

---

## L-B — the 51 fleet-audit commits

**Full report: `docs/audits/2026-08-02-technical-night-batch-lb-fleet-audit-commits.md`**

Premise **TRUE — exactly 51**, on `origin/automation/fleet-audit` (an ADR-84 orphan branch, never
merged by design — which is *why* they were invisible, not a fetch failure). Clone unshallowed
first, so **nothing in that lane is marked UNVERIFIED**.

- **[#463] CONFIRM (4/4)** and **[#464] CONFIRM (5/5)** — every named item byte-identical across
  the whole newly-visible window. **The finding is the flatness:** nine items, fifteen days, not
  one moved. That is the strongest available evidence for [#460]'s triage-gap thesis.
- **[#465] EXTEND** — legs (2) and (3) are **one mechanism**, reproduced exactly (16 WARNs → 2,
  the missing 14 being precisely the three hub-only checks), recurring on **8 of 10** multi-commit
  days, correlating with the un-retired parallel SessionStart trigger, and **hub-specific**
  (consumer repos stay stable the same day).
- **1 new candidate:** `silent_rule_ratchet` FAIL on the hub, first seen 2026-08-01 — no open row
  names it. Notably, that same daily contains **both** `pass` and `fail` for the check, so the
  writer's duplication symptom can concatenate *contradictory verdicts*.
- **External (ADR-41, queue-only here):** all of [#463] and [#464]. [#465] is hub work.

## L-C — universal AGENTS.md migration (ANALYSIS ONLY)

**Full report: `docs/audits/2026-08-02-technical-night-batch-lc-agents-md-analysis.md`**
*No file was renamed; no `AGENTS.md` was created; `CLAUDE.md` was read, never edited.*

- **Recommendation: hold.** ADR-52 adopted AGENTS.md and **ADR-53 superseded it the same day** on
  a sentinel test (codex-cli 0.131.0). Claude Code still does not read AGENTS.md natively (issue
  #6235 open since 2025-08-21). Codex already reads `CLAUDE.md` via
  `project_doc_fallback_filenames` — documented in PLAYBOOK three times.
- **The standard is real and converging** — donated to the Linux Foundation's Agentic AI
  Foundation 2025-12-09, with **Anthropic as a founding co-donor**; 60,000+ repos. That argues for
  *watching*, not migrating ahead of the tooling.
- **§12, measured: 20 lines (8.4%) but 19,383 bytes — 45.4% of CLAUDE.md.** Entries literally say
  they are "folded … to hold the section-history count at 11", i.e. the file optimises the metric
  the gate measures while the content grows. **Recommend relocating v2.31–v2.48 behind the
  existing git pointer** — authorised by ADR-49/65, needs no new ADR, and is independent of the
  AGENTS.md question. One precaution: a 15-entry uniqueness pass first.
- **Migration cost if pursued:** **255 occurrences across 72 files** hardcode `"CLAUDE.md"`,
  hub-side only. Two failure points are **silent** (`.vscode` filterFileRegex; release_lint's
  manifest mirror).
- **Governance needed: ADR-110**, with nine things it must rule — including whether it overturns
  ADR-53 on *preference* rather than evidence.

## L-D — currency & consistency

**Full report: `docs/audits/2026-08-02-technical-night-batch-ld-currency-audit.md`**

Six mechanical checks **PASS** — intake statuses coherent (#23 correctly SEED; it was filed
2026-08-01 and is one day old), ADR index reflects **both** ADR-109 amendments, audits index
current, `terminal-setup` in the registry, `doc-counts.md`'s **38 checks** verified against the
live registry, all seven generators clean. GitHub state **reachable** and confirms origin holds
exactly `main` + `automation/fleet-audit`, 0 workflows.

Three findings, all in hand-written prose describing organs that no longer exist:

- **D-1** `CONTRIBUTING.md:128–178` describes the retired nightly GitHub Action in the present
  tense. **Known** — `ARCHITECTURE.md:776–780` names it and defers it — but **unowned**: no
  backlog row exists. It also passed the `last_reviewed` freshness gate throughout.
- **D-2** `protocols/PLAYBOOK.md:1747` still teaches the deleted Action as **part 3 of 4** in how
  to deploy a nightly Routine, and `:1783` cites it as a live shallow-clone guard. **Not covered
  by the ARCHITECTURE deferral** — higher severity than D-1, because it carries no warning.
- **D-3** ADR-82 (`HANDOFF_PROCESS v5`) still reads `Status: Proposed` while the process runs at
  **v6.0.1**. [#242] owns ADR-88/89 but **not** ADR-82.

Two in-lane claims were **REFUTED** before reaching this report: an "`ALL_CHECKS` has 41" count
(it is 38) and an "ARCHITECTURE lists only 14 checks" drift claim (that list is explicitly
"**not an exhaustive inventory**").

## L-E — library-first sweep

**Full report: `docs/audits/2026-08-02-technical-night-batch-le-library-first.md`**

**No swaps performed.** 3 of 5 candidates fully measured; 2 left MEASURE-FIRST and recommended for
nothing. Network never limited the lane.

- **The headline is a defect, not a tidiness proposal.** The hand-rolled version comparator
  (`fleet_parity.py:821`) is **wrong in two directions**, verified live:
  `'0.15.5rc1' -> (0, 15, 51)` — suffix digits are *absorbed* into the patch component, so a
  release candidate compares **greater** than its own release; `'0.15.5-beta' -> (0, 15, 5)` —
  a non-numeric suffix is dropped and compares **equal**. *(This corrects the in-lane description,
  which called the suffix "silently dropped" — absorption is the worse failure.)* A second defect:
  compound specifiers (`>=1.0,<2.0`) are not parsed as ranges. Both are **dormant only because
  `ruff` is pinned at an exact release** — a `>=` floor is exactly where an `rc` build appears.
- **`packaging` SURVIVES and is already in the tree** (transitively via pytest), so the fix costs
  **no new dependency in the locked gate environment**. 6 sites.
- **networkx SURVIVES** (12/12 and 6/6, incl. self-loops and disjoint cycles) for 4 hand-rolled DFS
  cycle-detectors — one of them a **verbatim mirror** in the plugin floor, so a fix must land
  twice. **Recommendation: ride along with [#383]'s dependency-add**, not before — adding it early
  would install a library ahead of its ADR-105 named consumer.
- **`github-slugger` KEEP** — fidelity fine (1029/1030 real headers) but the library is
  **abandoned** (last release 2022-12-12). Deliverable is a why-not line in the code, not a swap.
- **One stale premise found and reconsidered, not overridden:** `fleet_parity.py:832` justifies the
  hand-rolled comparator as "(no packaging dep)". That premise is now false.

## L-F — backlog & tasks health

**Full report: `docs/audits/2026-08-02-technical-night-batch-lf-backlog-health.md`**

- **186 = 157 `open` + 29 `deferred`.** The disk↔manifest delta of 23 files is fully explained
  (22 `closed` + `README.md`) — **no orphans**; retire-not-delete working as designed.
- **Shape:** 113 of 186 are size-S, 95 are P3, and [E2] alone is 60 rows. This pool shrinks by
  *disposition* far faster than by execution.
- **The staleness scan failed, and that is the finding.** It returns 0 stale rows because commit
  `9bd0d719` created 174 task files in one migration, resetting every file's git date. File-mtime
  staleness is unusable here.
- **The auto-generated groom list did not survive review** — 4 of 4 spot-checked candidates had
  plainly unmet Done-whens. Reported as unreliable rather than forwarded, consistent with the
  2026-07-09 precedent where **39/39** auto-proposals were rejected at triage.
- **Two groom observations do survive:** [#463]/[#464]'s "unpushed and unread" evidence clause is
  now false (reword, not close), and the 29 deferred rows are an unexamined disposition class.
- **A propagating figure was killed:** a "+52.8 adds/week" rate derived from `git log
  --diff-filter=A` is a migration artifact (174 of ~211 adds came from one commit). The true rate
  is 5 filed per window.

---

## BLOCKING QUESTIONS FOR THE MORNING ARCHITECT

| # | Lane | Question | Decision shape |
|---|---|---|---|
| A-1 | L-A | [#383] is the only unblocked keystone. Which surface goes first? | name the surface |
| A-2 | L-A | L3.5 is now unblocked and cheap (2–3 windows). Take it before or after [#383] wave 1? | before / after / parallel |
| A-3 | L-A | The scheduled night task bypasses the ADR-106 locked environment. Fix the scheduler, or declare it out of scope? | fix / declare / retire the task |
| B-1 | L-B | [#465] legs (2)+(3) are one root cause. Re-scope to a single fix, or keep two legs? | re-scope / keep-split |
| B-2 | L-B | Retire the parallel SessionStart audit trigger now that it is named as the collapse source? | retire / keep / investigate-first |
| B-3 | L-B | File the `silent_rule_ratchet` FAIL at n=1, or wait for a second daily? | file-now / watch / fold-into-465 |
| B-4 | L-B | Two lineages record the same dailies (`main` vs `automation/fleet-audit`). Which is authoritative? | branch / main / reconcile |
| C-1 | L-C | Migrate to universal AGENTS.md, or hold at provider-fallback-config? | migrate / hold / additive-probe |
| C-2 | L-C | **Relocate §12 (45.4% of CLAUDE.md by bytes) behind the git pointer?** Independent of C-1. | relocate / keep / relocate-after-uniqueness-pass |
| C-3 | L-C | If migrating: does ADR-110 overturn ADR-53 on preference, or is a sentinel re-test run first? | re-test-first / overturn |
| C-4 | L-C | What happens to the three `@import` fragments, which have no portable equivalent? | inline / drop / keep-Claude-only |
| C-5 | L-C | Does a universal AGENTS.md supersede the live `codex/AGENTS.md` (ADR-54)? | supersede / coexist / re-scope |
| D-1 | L-D | File a row for the CONTRIBUTING "Nightly outcome management" reconciliation, or delete the section? | file-row / delete / keep-deferred |
| D-2 | L-D | PLAYBOOK "The envelope" teaches a four-part deployment whose part 3 is deleted. Rewrite to three? | rewrite / successor-planned / defer |
| D-3 | L-D | Extend [#242] to ADR-82, or rule v5 superseded-by-v6 without a status flip? | extend / supersede-ruling / leave |
| E-1 | L-E | Swap the 6 version-compare sites to `packaging`? It is a **defect fix**, not tidiness, and costs no new dependency. | swap-now / file-a-row / keep |
| E-2 | L-E | The two version defects are dormant today. Fix now, or file and wait for a prerelease to bite? | fix-now / file / accept-with-reason |
| E-3 | L-E | Collapse the 4 DFS sites onto networkx **as part of** [#383]'s dependency-add, or keep them hand-rolled? | ride-along / keep / separate-row |
| E-4 | L-E | Spend a future lane measuring markdown-it-py and the `_git()` wrappers, or close them as KEEP now? | measure / close-as-keep |
| F-1 | L-F | **What is the §F target number at 2026-08-26?** Direction alone cannot be gated. | a number / "directional only" |
| F-2 | L-F | Do the 29 `deferred` rows count against the §F number? | yes / no / re-disposition as a batch |
| F-3 | L-F | Is a filing-rate cap wanted, given filing outran closing 5:2? | cap / no cap / cap P3-S only |

---

## BATCH INTEGRITY

**Rails observed.** Read-only over all governed content. No governed file edited; no rename; no
`CLAUDE.md`/`AGENTS.md` created or renamed (lane L-C was analysis only); no status flips; no
`BACKLOG.md` or `tasks/` writes; no deletions; no new top-level paths. All output is new files
under `docs/audits/`. Never merged; `main` never touched.

**Branch deviation — flagged, not silent.** The brief names `chore/night-batch-2026-08-02`. This
cloud session is hard-bound by its harness to the lane branch
**`claude/night-batch-audit-2026-08-02-84a0dh`**, and that is where this work is pushed. The
substance of the rail is met (one branch, never `main`, never merged), and `claude/<slug>` is a
sanctioned machine-produced lane prefix under CLAUDE.md §4 (v2.47, the Anthropic cloud-lane
enum entry). Renaming is the architect's call.

**Two read-only git operations were performed** and are disclosed because they changed the local
clone: `git fetch --unshallow` (history to 2026-03-30) and a fetch of
`origin/automation/fleet-audit` into remote refs. Neither touched the working tree, and both were
necessary — without them L-B could not have settled its premise and would have had to mark the
whole lane UNVERIFIED.

**Cloud caveats, honoured.** The shallow-clone caveat was **lifted** by unshallowing rather than
worked around. The uv-shadowing caveat is **live**: `uv run --locked` is unavailable here
(`uv==0.11.19` required, `0.8.17` present), so the divergence report ran in an isolated scratchpad
venv — live numbers, unlocked environment. **Container gate verdicts are not verdicts** and none
is offered as one.

**Suite — run once, and the delta accounted for.** `pytest` is absent from this container's system
interpreter, so the suite ran from an isolated scratchpad venv (`click`, `rich`, `pydantic`,
`ruamel.yaml`, `jsonschema`, `packaging` installed there to reach collection):

```
32 failed · 2084 passed · 32 skipped   (591s)
```

That sits at the stated **~33-failure container baseline**. **Exactly one failure was attributable
to this batch** — `tests/test_gen_audit_index.py::test_live_index_is_fresh`, made stale by the six
new reports. The sanctioned audits-index regen was run (`gen_audit_index.py --write`; diff is
`+7/−1`, the sole deletion being the count line `359 → 365`) and the test now passes **11/11**.
**No unexplained failure-set delta.**

Per doctrine this is **not** offered as a gate verdict — it is an unlocked environment. The
dispositive non-mutation evidence is direct and stronger: `git diff --stat HEAD` reported **zero
modified tracked files** at every checkpoint before the sanctioned regen, and the only tracked
change in the final commit is the generated index.

---

*Read-only night batch, unattended, 2026-08-02. Morning review promotes or rejects per lane.*
