# Verification — four ruled dispositions, and the conformance digest gap

- **Class:** verification (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** ruled-dispositions-and-digest-gap
- **Arc:** ARC-5, night-batch archive. Hub primary checkout, integration branch
  `docs/arc5-night-batch-archive`, `main` from `e67fb8db`.
- **Why this file exists:** two obligations the night batch surfaced and could not itself discharge
  — supplement-update §A7 items 2 and 3. Item 2 asks that four recorded dispositions be **verified,
  not assumed**, to have executed; item 3 asks that the digest gap be **established as broken or
  deliberate and reported**, not silently repaired.
- **Standing this file claims:** it reports measurements. It closes no row, rules on nothing, and
  merges nothing. §2's verdict is deliberately a report to the operator rather than an act.

---

## 1. Four ruled dispositions — verified, not assumed

The ruling was recorded; the execution was unconfirmed. **An unverified "it landed" is precisely
the class lane N-B measured last night** — 2 of its 24 claims were REFUTED and both were *inherited*
claims while every *measured* claim held. So each of the four was re-derived from the tree rather
than read from the ruling that ordered it.

**Method.** For each: locate the receiving document, read the landed text, confirm the shape matches
the ruled shape (amendment vs. scope note vs. own intake), and establish the commit that landed it
is an ancestor of `main`. A locator that resolves is the evidence; the ruling's own wording is not.

### Result — 4 of 4 LANDED. Zero not-landed.

| # | Disposition as ruled | Verdict | Locator |
|---|---|---|---|
| 1 | dependency-graph commission → intake #29, as an **amendment** | **LANDED** | `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md:87` |
| 2 | telemetry commission → intake #29, as an **amendment** | **LANDED** | `docs/intake/2026-08-08-func-multi-model-execution-and-distillation.md:48` |
| 3 | multi-provider-portability commission → a **W-wave scope note** | **LANDED** | `docs/intake/2026-08-05-func-simplification-distribution-wave.md:96` |
| 4 | cloud-compute commission → **its own intake** | **LANDED** | `docs/intake/2026-08-09-tech-compute-placement-and-remote-execution.md` (intake-id **32**) |

**All four landed in ONE commit: `6a4a1d78`** — *"docs(intake): ARC-2 Phase D — the three orphan
commissions homed: 1 new intake, 2 amendments, 1 scope note"*. Confirmed an ancestor of `main`
(`git merge-base --is-ancestor 6a4a1d78 main` → true), reaching `main` through merge `7e024317`
(ARC-2). Its diffstat touches exactly the three intake bodies plus the two generated intake
surfaces — `docs/intake/README.md` and `docs/intake/manifest.json` — i.e. the generator pair a
correct intake add requires, both refreshed in the same commit.

### Per-item evidence

**1 — dependency graph, and 2 — telemetry.** Both fold into intake #29 under one shared heading at
line 41: *"AMENDMENT 2026-08-09 (ARC-2 consolidation, architect amendment 3) — two commissions fold
in here"*, whose framing paragraph states the reason (*"Rather than file two more intakes … they
fold in here, because this is already the measurement/instrumentation intake"*) and the constraint
(*"Zero births by this amendment; the S3a MEASURE-FIRST precondition binds both folds"*). The two
folds are separately headed and separately sourced:

- **Fold A — agent instrumentation & telemetry** (line 48), memo `wf-02c940ef`.
- **Fold B — the dependency/ontology graph** (line 87), memo `wf-f6851745`, with the fold's own
  justification stated in one line: *"Folded here because a graph is a measurement surface, not a
  new domain."*

The ruled shape was **an amendment to intake #29**, and an amendment is what landed — not a new
intake, not a BACKLOG row. 85 lines added to that file by `6a4a1d78`.

**3 — multi-provider portability.** Landed as a **SCOPE NOTE**, not an amendment, and the
distinction is honoured in the landed text: `docs/intake/2026-08-05-func-simplification-distribution-wave.md:96`
— *"SCOPE NOTE 2026-08-09 (ARC-2 consolidation, architect amendment 3) — the portability commission
folds into W-9(a)"*, opening *"**Adds no W-item, changes no verdict, births nothing.**"* The receiving
W-item exists and is live in the same file (W-9 at line 37; the note attaches the memo's evidence to
W-9(a)'s already-owned decision and states it **confirms** that mechanism on external grounds).
51 lines added. This is the W-wave scope note as ruled.

**4 — cloud compute.** Landed as **its own intake**, `intake-id: 32`, whose own subtitle carries the
reason it is not part of the other five: *"Sole owning intake for the compute-placement commission —
the sixth research commission, and the one that is **not** part of the other five. Commissions 1–5
decompose a single question … this one is an independent capacity problem and must not be presented
as part of that programme."* Its frontmatter additionally records why the id is 32 rather than 30:
30/31 were **RESERVED** for two authored-but-unfiled drafts, and taking 30 would have collided with
a permanent join key. Both reservations were subsequently honoured — intake #30 and #31 are now
filed (`036385a6`, ARC-3) — so the gap that commit reported rather than silently closed did close
correctly.

### What this verification does NOT establish

- **It checks execution, not merit.** That the four commissions are *homed* says nothing about
  whether their content is right; all four receiving documents are `status: DRAFT` or carry
  DRAFT-editability, and their triage rides the batch-4 planning GO.
- **It does not re-verify the ruling itself.** The question asked was whether the ruled acts
  executed. They did.

---

## 2. The conformance digest gap — VERDICT: a broken step, and the step is named

### 2.1 The measurement, re-derived locally

N-C's finding reproduces exactly against the local tree.

- **`main`'s digest stream stops at `2026-08-02`.** `git ls-tree -r --name-only main` returns
  `docs/audits/2026-08-01-conformance-nightly-digest.md` and `-08-02-` as the newest two; there is
  no `2026-08-03` or later digest anywhere under `main`.
- **Six digests exist only on unmerged branches**, one commit each:

| Date | Branch | Tip | On `main`? |
|---|---|---|---|
| 2026-08-03 | `origin/claude/conformance-2026-08-03` | `5693919b` | no |
| 2026-08-04 | `origin/claude/conformance-2026-08-04` | `3d083660` | no |
| 2026-08-05 | `origin/claude/conformance-2026-08-05` | `19fc2371` | no |
| **2026-08-06** | **— none —** | — | **no branch at all** |
| 2026-08-07 | `origin/claude/conformance-2026-08-07` | `cee4472b` | no |
| 2026-08-08 | `origin/claude/conformance-2026-08-08` | `f18419fc` | no |
| 2026-08-09 | `origin/claude/conformance-2026-08-09` | `ad1822c9` | no |

### 2.2 The verdict: BROKEN, not deliberate

**Deliberate is refuted on the evidence, not merely doubted.** Three independent checks:

1. **Nothing suppresses the merge.** The only written protection `claude/conformance-*` carries is
   in `.claude/rules/git-discipline.md`, and it protects them from **deletion**, not from being
   merged: *"MERGE IS ATOMIC … Exceptions exist only by EXPLICIT PROTECTION (currently
   `claude/conformance-*`)"*, with the verify line reading *"`git branch --merged main` lists
   nothing but `main` and explicitly protected branches"*. That clause exists precisely because
   these branches **are** merged and then kept — the opposite of a hold.
2. **The routine did not stop and its output did not change shape.** Six digests were produced on
   the nights they were due, in the same format, one carrying an amendment of its own
   (`f18419fc`, *"amend 2026-08-08 conformance digest — all 5 findings killed by skeptic"*). The
   producer is healthy; only the consumer is absent.
3. **The absorb step ran regularly right up to the gap and then simply stopped.** It is visible on
   `main`'s first-parent spine as an explicit, repeated act.

### 2.3 The step, named

**The missing step is the manual, operator-authorized "absorb the nightly conformance digest"
merge**, which in its landed form is two commits:

1. `git merge --no-ff claude/conformance-<date>` into `main` — subject *"absorb the nightly
   conformance digest (preserve-then-delete)"*;
2. a follow-on index-regen commit, because the digest is a new `docs/audits/` file and
   `docs/audits/README.md` is generated and gate-checked.

Its last five executions, from `main`'s spine:

```
24882f8c  Merge branch 'claude/conformance-2026-08-02' — absorb the nightly conformance digest (preserve-then-delete)
25e9dc7d  Merge branch 'chore/absorb-conformance-index' — audits index regen + JOURNAL 2026-08-02 (e)
c7af2c03  Merge branch 'claude/conformance-2026-08-01' — nightly conformance digest 2026-08-01 (preserve-then-delete, operator-authorized 2026-08-01)
bd08f343  Merge branch 'claude/conformance-2026-07-31' — nightly conformance digest 2026-07-31 (preserve-then-delete, operator-authorized 2026-07-31)
61757e82  Merge branch 'claude/conformance-2026-07-30' — nightly conformance digest 2026-07-30 (preserve-then-delete, operator-authorized 2026-07-31)
bb217819  Merge branch 'claude/conformance-2026-07-29' — nightly conformance digest 2026-07-29 (preserve-then-delete, operator-authorized 2026-07-31)
```

**`24882f8c` (2026-08-02) is the last execution.** The step has not run in the eight days since.

**Why it is a *step* and not an *organ*: it was never automated, and nothing notices its absence.**
Three properties, each verified:

- **No trigger.** Every execution above carries `operator-authorized <date>` in its own subject. The
  step fires when a human decides to run it; there is no schedule, hook, or command that performs
  or proposes it. Its cadence was a habit, and a habit is exactly what a window boundary drops.
- **No gate sees it.** The `routine_consumers` audit check gates ADR-105's `consumer` /
  `consumption_path` fields, but **only on BACKLOG rows carrying a `· routine:` marker** — its own
  docstring states the boundary: *"Green does NOT mean the fleet's routines have consumers."* The
  nightly conformance routine is not a BACKLOG row, carries no marker, and is therefore not
  checked. It ran **[OK]** on this arc's baseline while six of this routine's digests sat unread.
- **ADR-105 predicted this exact failure by name.** Its §1 says of the field it introduced:
  *"`consumption_path` names the **mechanism** by which the output reaches a decision — the field
  **the conformance routine would have failed**, since branches nobody opens are a path in name
  only."* The routine was never held to that bar, because the bar binds at activation and this
  routine predates it. The retrofit is filed and OPEN: **[#426]**, which counted 30 live routines
  (12 session hooks · 15 commit-time gates · 3 scheduled/remote) of which the check governs one.

### 2.4 This is a recurrence, at identical width

The class is already filed and still OPEN. **[#419]** *"We run routines whose output nobody
consumes"* — P2/M — was born from the **identical** event: *"six branches (`claude/conformance-2026-07-21`
… `-26`) sit unmerged and unread, and the single High finding among them … was fixed on `main` by
`037d9f08` on 07-23 by a session that never opened the branch that found it."*

So the ledger reads: first instance six branches (07-21…07-26), row filed, row framed the defect
correctly, absorb habit resumed for five nights (07-29…08-02) — and then **second instance, also
six branches (08-03…08-09), same routine, same cause.** [#419]'s Done-when (*"every standing routine
has a named consumer and a consumption path, and unconsumed output is surfaced rather than silently
accumulating"*) is unmet, and this recurrence is the measurement proving it unmet rather than an
argument that it is.

One coincidence worth recording without reading meaning into it: `check_journal_spine_anchor`'s
ADR-85 disposition floor is `24882f8cc` — the last absorb merge. The anchoring floor and the last
consumed digest are the same commit.

### 2.5 2026-08-06 — undetermined from the repo, and stated as such

No branch exists for that date, so the repo cannot distinguish **(a)** the routine did not run that
night from **(b)** it ran and did not push. Both are consistent with every artifact available here.
This is **not** reported as "the routine skipped a night" — that would be the inherited-claim class
N-B measured. What would settle it is the routine's run history in the cloud scheduler, which is not
a repo artifact and was not reachable from this arc.

### 2.6 What this arc deliberately did NOT do

**The six digests were not merged.** The instruction was explicit — establish and report, do not
merge on the integrator's judgement — and it is the right call independently: absorbing six nights
of findings is a **consumption** act (each digest carries High/Medium findings that route to
decisions), and consumption without an operator is how the first instance produced a High finding
fixed by a session that never read the branch that found it. **No conformance branch was touched,
merged, reaped, or proposed for deletion by this arc.**

**Open for the operator, stated as options and not as a recommendation dressed as one:** whether to
absorb the six now as a batch, whether the absorb step should become an organ (which is [#419]'s and
[#426]'s territory, not a fresh row), and whether 2026-08-06 warrants a scheduler-side check.
