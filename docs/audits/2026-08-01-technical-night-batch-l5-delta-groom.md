# Night batch 2026-08-01 — L5: delta-groom dossier ([#457]–[#466])

**Status: PROPOSAL — drafts the A-3 triage ruling. The architect rules; nothing here is decided.**

**Scope:** every task row filed or moved since merge `5eebee91` (2026-07-31 12:24:45 +0200), i.e.
`[#457]`–`[#466]` inclusive. Read-only: gather leg by a bounded fan-out agent (facts only, no
triage), triage column written by the orchestrator. `BACKLOG.md`, `tasks/`, and `docs/intake/`
were not modified.

**Window shape (verified):** ten rows filed, **zero closed**, zero deleted. All ten carry
`status: open` in their task-file frontmatter (verified directly, not inferred). 203 task files on
disk; highest id **466**; next free id **467**. Thirteen commits touched `tasks/` in the window;
all ten rows were filed 2026-07-31 between 14:09 and 22:31 — a single night's filing burst.

> **The headline the triage should not bury:** this window filed ten and closed none. Intake #22 §F
> ("backlog must shrink") enters at 2026-08-26. The architect's own supplement (§6) already flags
> that the next window "should expect that pressure and close more than it files." A triage that
> marks all ten live is therefore not a neutral outcome — it is a decision to carry +10.

---

## Triage summary table

Categories: **live** = do the work, it is real and unblocked · **awaiting-ruling** = the work cannot
start until a named decision lands · **dead** = propose closure without building.

| id | P/size | theme | proposed triage | one-line rationale |
|---|---|---|---|---|
| [#457] | P2/S | [E2] | **live** | Two named failing tests, both reproduced this batch; the fix is a decision about which definition of green is canonical. |
| [#458] | P3/S | [E3] | **live** | A one-paragraph PLAYBOOK append with no dependency; cheapest close on the board. |
| [#459] | P3/S | [E9] | **awaiting-ruling** | Narrowed to organ-class prose, but carries an embedded codemap source-root ruling the row cannot self-answer. |
| [#460] | P2/S | [E7] | **awaiting-ruling** | Explicitly the architect's R1; recommendation recorded, ruling open. Blocks [#461] and the divergence-report cadence. |
| [#461] | P2/M | [E7] | **awaiting-ruling** | Sequenced behind [#460] — mechanizing metrics for a lane whose fate is unruled would build the wrong consumer. |
| [#462] | P2/S | [E9] | **live (split)** | Clause 1 is data-only and satisfiable today; clause 2 needs a declaration source that does not exist. Split the row. |
| [#463] | P2/S | [E7] | **live (external)** | Real, verified, unchanged ~20 days — but every fix lands in `win-tooling`, not here. |
| [#464] | P2/S | [E7] | **live (external)** | Same class: five real findings, all fixed in consumer repos, none in this tree. |
| [#465] | P2/M | [E7] | **awaiting-ruling** | Writer-integrity bugs are real, but whether to fix the writer depends on whether [#460] keeps the lane. |
| [#466] | P3/S | [E9] | **dead-for-now** | Deliberately not built per an architect ruling; it is a tripwire, not a task. Propose park-or-close. |

**Net proposal:** 4 live (2 of them landing outside this repo) · 4 awaiting-ruling, all four
resolvable by **one** decision each · 1 split · 1 park. **[#460] is the keystone** — ruling it
alone converts three rows (`#460`, `#461`, `#465`) from blocked to actionable.

---

## Per-row detail

### [#457] — two live-repo tests fail on main against green gates
`tasks/457-inherited-live-repo-test-failures.md` · P2/S · [E2] · `serialize-group: audit-py`

- **Status:** open. Filed `19d7e25`, merged `356841a`.
- **Liveness — strong, and re-verified by this batch.** The two ids are
  `test_audit.py::test_check_fleet_parity_green_on_live_repo` and
  `test_audit.py::test_routine_consumers_live_backlog_governs_exactly_one_row`. **Both were
  observed failing in this batch's own suite run** (see the L-index verification section) — the row
  is not stale.
- The 2026-08-01 `RESIDUAL.md` §1 names them as *"left RED and UNMARKED by standing operator ruling
  — no skip, no xfail, no deselect. Expect them; they are owned, not forgotten."*
- **Proposed triage: LIVE.** The substance is a genuine design question the row already states —
  the gate and the suite encode two different definitions of "green" (the disposition register is
  visible to `audit.py ship-gate` but invisible to a test that calls the check directly). Fixing it
  means ruling which definition is canonical, then making the other conform.
- **Note for the architect:** this row's `serialize-group: audit-py` collides with `[#465]`, which
  also targets `audit.py`. If both are scheduled they serialize; that is correct behaviour, but it
  means [#465]'s blocked state (below) also delays [#457]'s merge window if they are batched.

### [#458] — PLAYBOOK note: gates and commits never run concurrently in one tree
`tasks/458-playbook-note-gates-never-race-commits.md` · P3/S · [E3] · `serialize-group: playbook`

- **Status:** open. Filed `d62acf3`.
- **Liveness:** the lesson is already recorded in JOURNAL prose from the [#382] arc; the row exists
  only to move it into PLAYBOOK where it is consultable.
- **Proposed triage: LIVE, and the cheapest close available.** No dependency, no ruling needed, no
  code. One PLAYBOOK append plus its ToC regen (`toc-freshness-playbook` gate).
- **Recommendation:** if the morning wants a visible close to offset the +10 filing, this is it.

### [#459] — ARCHITECTURE.md prose for the ADR-109 desired-state organ class
`tasks/459-architecture-prose-desired-state-organs.md` · P3/S · [E9] · `serialize-group: architecture`

- **Status:** open. Filed `005c26e`, condensed `ce49d2b` (row had exceeded the 1200-char cap on
  filing and was trimmed the same day).
- **Liveness:** partially discharged already — the ADR-currency leg landed 2026-07-31 (`2689740`:
  Purpose line now reads through ADR-109; Governing ADRs gained ADR-108/ADR-109 bullets). What
  remains is narrower than the row's title suggests.
- **Why awaiting-ruling, not live:** `RESIDUAL.md` §4 item 3 states the residue is not trivial —
  `ecosystem/schema/` sits **outside** the codemap's `--source-root scripts` scope, so the same
  edit must rule *whether the source-root widens or the schema package is declared out-of-codemap
  with a reason*. That is a ruling, and the row cannot answer it from inside.
- **Proposed triage: AWAITING-RULING.** One sentence from the architect ("widen the source-root" /
  "declare out-of-codemap because X") converts it to live and small.

### [#460] — fleet-audit dailies: stop the branch lane, keep the digest, add persistence-triage
`tasks/460-history-dailies-write-only-no-consumer.md` · P2/S · [E7] · `serialize-group: settings-json`

- **Status:** open, and explicitly flagged in the handoff as *{OPERATOR-RULED THIS SESSION:
  recommendation recorded, ruling open}*. It is open question **R1**.
- **Liveness: maximal.** This is the keystone row of the window. It was rewritten `8c1c935` from an
  open question into a concrete recommendation after the night deep review.
- **Proposed triage: AWAITING-RULING — and rule it first.** See the L6 decision pack
  (`2026-08-01-technical-night-batch-l6-460-decision-pack.md`) for the consolidated one-read
  version, including a verified caveat: the "dead since 2026-07-16" date could **not** be
  independently re-derived from git in this container (the `automation/fleet-audit` ref is absent
  and the clone is shallow), and the root cause of the stoppage is **not established anywhere** —
  which matters, because "decommission the dead scheduled task" may be targeting a component that
  is already gone.
- **Blocking radius:** [#461] and [#465] directly; the ADR-109 divergence-report cadence
  indirectly, via the standing sequencing constraint (*"rule [#460] before putting the divergence
  report on any cadence"*).

### [#461] — mechanize the six window metrics
`tasks/461-mechanize-window-report-metrics.md` · P2/M · [E7] · `serialize-group: settings-json`

- **Status:** open. Filed `d47c94a`.
- **Liveness:** the six-metric window report is a *standing operator commitment* (supplement §6:
  "report every window"), currently hand-assembled per report. So the need is real and recurring.
- **Why awaiting-ruling:** it shares `serialize-group: settings-json` with [#460] and would consume
  the same producer surface whose fate [#460] decides. Building a metrics consumer against a lane
  that may be stopped is the exact defect [#460] names.
- **Proposed triage: AWAITING-RULING (behind [#460]).** Note it is the only **M** among the
  awaiting-ruling set — it is the one that will cost real time once unblocked.

### [#462] — terminal-setup declared fleet but absent from every machine membership surface
`tasks/462-terminal-setup-absent-from-every-machine-member.md` · P2/S · [E9] · `serialize-group: architecture`

- **Status:** open. Filed `79deb96`.
- **Liveness: strong and independently corroborated** — two separate conformance digests (07-30 N4,
  07-31 S3) found it independently and both proposed the same cheap fix ("add a registry row"). The
  row deliberately **overrides** that fix on ADR-109 §2 grounds (`registry.md` loses authority).
- **Proposed triage: LIVE, but SPLIT.** L7's pre-analysis
  (`2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md`) establishes the row has two clauses
  with very different costs:
  - **Clause 1** (terminal-setup appears in the wave-1 member set) — **data-only, satisfiable in
    schema v1 as shipped, zero schema change.**
  - **Clause 2** (the census mechanically diffs the declaration against machine surfaces) — **not
    satisfiable today**: there is no loadable source representing "the ADR-104/VISION declaration,"
    so there is nothing to diff against. Building one collides with ADR-109 §9's explicit rejection
    of a new persisted desired-state file in v1.
- Splitting lets clause 1 close cheaply now and keeps clause 2 honest as wave-2 scope.

### [#463] — win-tooling onboarding debt, unchanged since admission
`tasks/463-win-tooling-onboarding-debt-unchanged-since-admi.md` · P2/S · [E7] · `serialize-group: environment`

- **Status:** open. Filed `8c1c935` from the fleet-audit deep review.
- **Liveness: verified real** — 2 FAILs + 2 WARNs (config.yaml not dot-prefixed per ADR-59;
  VISION+ARCHITECTURE edited-then-never-re-reviewed; workspace sort settings absent; absent from
  `deployed-versions.yaml`), evidence identical from 2026-07-11 admission through 2026-07-31.
- **Proposed triage: LIVE, but EXTERNAL.** Every fix lands in the `win-tooling` repo, not here.
  This repo can only hold the *tracking* row. Flagging because a triage that counts it as hub work
  will mis-schedule it — and because the hub cannot close it unilaterally.

### [#464] — corp-*/ai-council governance drift, five findings live 15–46 days
`tasks/464-corp-consumer-governance-drift-live-weeks-unacti.md` · P2/S · [E7] · `serialize-group: environment`

- **Status:** open. Filed `8c1c935`.
- **Liveness: verified real** — five findings across corp-sca-time-automation, corp-ops,
  corp-monorepo, ai-council; the longest live 46 days. Invisible to the hub's own gates because
  those are hub-scoped.
- **Proposed triage: LIVE, EXTERNAL** — same class as [#463]. Consider merging [#463] and [#464]
  into one consumer-drift tracking row; they share a triage, a blocker, and a `serialize-group`,
  and neither is closable from this tree. That merge would be a legitimate `kill-candidates:` entry.

### [#465] — fleet-audit writer integrity: skips recorded as PASS, same-day overwrite
`tasks/465-fleet-audit-writer-integrity-skip-as-pass-overwr.md` · P2/M · [E7] · `serialize-group: audit-py`

- **Status:** open. Filed `8c1c935`.
- **Liveness: real and the most interesting of the three deep-review rows.** Four writer bugs found
  by diffing the branch's *superseded same-day git blobs*: skips emitted as `pass` (inflating pass
  counts); two committed digests silently overwritten, each dropping 14 WARNs; the hub misresolving
  as not-itself on 6 of the last 8 runs; `handoff_tag_canonicity` self-disabled. **This class was
  detectable only because the lane is git-history-backed.**
- **Why awaiting-ruling:** the bugs are in the writer for the lane [#460] may stop. Fixing a writer
  that is about to be decommissioned is waste; *not* fixing it while the lane survives is a
  correctness hole. The order is forced.
- **Proposed triage: AWAITING-RULING (behind [#460]) — with one carve-out.** The "skips recorded as
  PASS" bug is in `audit.py` itself and affects **every** consumer of the check results, not just
  the fleet-audit lane. If the architect agrees, that sub-item is separable and **live now**,
  independent of [#460]'s fate. Worth checking before parking the whole row.

### [#466] — intake flip? post-discharge, mirrors [#439]
`tasks/466-intake-flip-candidate-post-discharge.md` · P3/S · [E9] · `serialize-group: architecture`

- **Status:** open. Filed at the tail of the window.
- **Liveness: deliberately suppressed.** The gather leg records it as *deliberately not built* per
  an architect ruling 2026-07-31: it mirrors the [#439] decision but the governance semantics
  differ, and it only becomes real after [#383] wave-1 discharge proves split-only works — which
  landed this window.
- **Proposed triage: DEAD-FOR-NOW / park.** This is a tripwire, not a task: it encodes "revisit
  when condition X holds." Two honest dispositions, architect's pick:
  1. **Park with an explicit trigger** — convert to a deferred row carrying the condition, so it
     stops appearing in live grooming counts; or
  2. **Close it** and let the [#383] wave record carry the note, since the discharge it waits on has
     now happened.
  Either way it should not sit in the open count as an actionable P3.

---

## Two cross-cutting observations for the architect

**1. One ruling unblocks three rows.** [#460] gates [#461] and [#465] directly. Rule it — in either
direction — and the awaiting-ruling set drops from four to one ([#459], which needs its own
one-sentence codemap ruling). That is the highest-leverage five minutes available in the morning.

**2. Two of the ten cannot be closed from this repository at all.** [#463] and [#464] track drift in
`win-tooling`, `corp-*`, and `ai-council`. They are correctly filed here (the hub is the auditor)
but they will never close through hub work, and counting them as hub backlog will distort the §F
shrink metric that starts biting 2026-08-26. The architect may want a distinct disposition class for
*externally-actioned tracking rows* — that is a methodology question this window surfaced, not a
task, and it is offered as an observation rather than a proposed row.

---

## Method note

Gather leg: read-only fan-out agent, facts only, forbidden from proposing triage. Per-row frontmatter
re-read directly by the orchestrator (all ten confirmed `status: open`). Git provenance from
`git log --diff-filter=A` per path. **Container caveat:** this clone is shallow (373 commits, parent
of `e631e59` absent) and the `automation/fleet-audit` ref is not present, so claims requiring deep
history or that branch were marked unverified rather than repeated as fact. Triage column is the
orchestrator's proposal and carries no authority.
