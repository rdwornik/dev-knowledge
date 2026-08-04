---
class: technical
date: 2026-08-04
slug: 480-ruling-input-pack
Status: "UNVERIFIED-UNTIL-LOCAL — INPUT, NOT AUTHORITY"
producer: claude-code-night-batch
lane: claude/night-batch-review-prep-k1f2yr
anchor_sha: b9190b3a
consumer: incoming 2026-08-05 dev-knowledge architect session
consumption_path: "branch -> local re-verification -> architect rules FR-5(a)/(b) at morning review"
scope: "evidence assembly for the [#480] ruling ONLY — no recommendation, no ruling, no build"
---

> **Status: UNVERIFIED-UNTIL-LOCAL. INPUT, NOT AUTHORITY.** Cloud night-batch lane: no merge, no
> canon edit, no closure, no ruling. This pack **assembles evidence and lays out an option space**.
> It deliberately contains **no recommendation** — FR-5(a) (refuse vs surface) and FR-5(b)
> (durability) are the architect's to rule. Where a prior exists it is labelled a prior, not
> evidence. Every count below carries the command that produced it, run at the anchor SHA.

# [#480] ruling-input pack — wrapper tally, artifact durability, refuse-vs-surface

`[#480]` is the window's highest-value open item. Two questions to rule, one build to emit:

- **(a) Refuse or surface?** Is a code-impact merge without a review artifact *refused* (hard
  organ) or *surfaced* (advisory + backstop)?
- **(b) Durability.** The `0/0/0/0` tally was transient terminal output with no committed trace.
  What must persist, and in what shape, for the verdict to be auditable after the fact?

---

## 1 · The measured defect: wrapper tally vs artifact bodies

### 1.1 What the wrapper reported

The codex-review wrapper's severity tally read `0/0/0/0` on **every** run of the 2026-08-02→04
window, while the artifact bodies carried a CRITICAL and a substantial HIGH count. The tally is
computed by the wrapper and printed to the terminal; it is **not** derived from the artifact it
just wrote.

Two run counts are both on record and they are **not a contradiction** — they differ by counting
window, and each is true at its own read time:

| Figure | Meaning | Read time |
|---|---|---|
| 10 | session-attributed artifacts (excludes 3 files predating the session) | verify-time (IC-8) |
| 12 | seal-count, "12-for-12" | seal-time |

**The load-bearing property is neither integer.** It is: *the tally read `0/0/0/0` while the bodies
carried ≥1 CRITICAL and ≥21 HIGH.* That holds under both counts. Any future citation of a severity
total must name its counting method or point at an evidence block (IC-9: the `1 CRITICAL + 24 HIGH`
figure is the dual-dialect section-aware count).

### 1.2 Provenance (durable, quotable)

- `docs/handoffs/2026-08-04-dev-knowledge-architect/RESIDUAL.md:96-99` — "across 12 review runs the
  wrapper's severity tally read `0/0/0/0` **every single time**, over 1 CRITICAL and 21 HIGH in the
  bodies. Not a bad run — a mechanism that reports a verdict about something it is not measuring,
  which is the same class as every defect the window closed."
- `JOURNAL.md:717` — "**The wrapper tally printed `0/0/0/0` all four times** over 1 CRITICAL and
  3 HIGH — read from the body every time; `[#480]` owns that gap."
- `tasks/480-code-impact-merge-without-review-artifact.md` — the row itself, carrying
  `evidence n=6` and a pointer rather than the evidence.

### 1.3 IC-11 — the non-durability finding

The tally was **transient terminal output with no committed trace**. Nothing in the repository
recorded what the wrapper claimed, so the claim could be neither audited nor refuted after the run
ended. This is the same unfalsifiability class as the defect that opened `[#480]`: the 2026-08-02
W2 report recorded "terra review: zero findings on both arcs" while **no artifact existed anywhere**
— the claim was never refuted, it was *unrefutable*.

IC-11 makes durability part of `[#480]`'s definition, not an aside: a mechanism that persists the
tally into the review artifact is what makes the verdict auditable after the fact.

---

## 2 · The three TODAY counter-examples — NC4 applied immediately

NC4 required the tally-persistence property be applied at once rather than deferred to `[#480]`'s
ruling. All three of today's code-impact arcs did so. **These are the counter-examples: the tally
was visible in the artifact body, and in every case findings were accepted and fixed pre-merge.**

| Arc | Artifact | Tally (C/H/M/L) | Findings disposition |
|---|---|---|---|
| FR-1 `[#481]` | `2026-08-04-codex-481-organ-id-rename.md` | 0/0/1/2 | all three ACCEPTED, fixed pre-merge |
| FR-2 `[#482]` | `2026-08-04-codex-482-glob-engine-true-glob.md` | 0/1/0/0 | the single HIGH ACCEPTED, fixed pre-merge |
| FR-3b `[#483]` | `2026-08-04-codex-483-preflight-discrimination.md` | 0/2/0/0 | both HIGHs ACCEPTED, reproduced, fixed pre-merge |

**Two of the three (`[#482]`, `[#483]`) had HIGH-severity findings fixed pre-merge**; `[#481]`'s
were MEDIUM/LOW and also fixed. In all three the artifact records "No finding deferred or
dispositioned away."

**Arithmetic re-verified at this anchor** — each tally matches the artifact's own declared counting
method:

```
$ grep -cE '^## \[(CRITICAL|HIGH|MEDIUM|LOW)\]'  docs/audits/2026-08-04-codex-481-organ-id-rename.md        -> 3   (tally 0/0/1/2 = 3) OK
$ grep -cE '^\*\*Severity:\*\*'                  docs/audits/2026-08-04-codex-482-glob-engine-true-glob.md   -> 1   (tally 0/1/0/0 = 1) OK
$ grep -cE '^### (Critical|High|Medium|Low) —'   docs/audits/2026-08-04-codex-483-preflight-discrimination.md -> 2  (tally 0/2/0/0 = 2) OK
```

### 2.1 The finding this pack adds — persistence is not yet machine-auditability

The three artifacts use **three different finding-heading conventions**, each declaring its own
counting method in prose. Each tally is internally honest; **no single mechanical counter can
verify all three.** Measured across the whole window at this anchor:

```
$ ls docs/audits/2026-08-0[234]-codex-*.md | wc -l          -> 16 artifacts
$ (tally-table regex ^\| d \| d \| d \| d \| d \|)          -> 3 of 16 carry a machine-readable tally
$ (three finding-heading shapes tried against each file)    -> 9 of 16 match NO recognised shape
```

Breakdown by shape (whole-window, this anchor; 4+1+2+9 = 16, sum-checked):

| Convention | Example | Artifacts using it |
|---|---|---|
| `## [SEVERITY] path — title` | `[#481]`, arc2/arc3, adr85-integration | 4 |
| `**Severity:** High` | `[#482]` | 1 |
| `### High — path` | `[#483]` ×2 | 2 |
| none recognised (findings in prose) | the round2 / retro artifacts | 9 |

**Bearing on (b):** "persist the tally in the artifact" is satisfied for the 3, and it demonstrably
worked — but auditability is currently by *human reading*, because there is no canonical shape a
checker could key on. If the ruling wants machine-checkable durability, the shape has to be named,
not just the requirement. If it wants human-auditable durability, the 3-of-16 state is already the
target and the gap is adoption, not mechanism.

---

## 3 · Option space — refuse vs surface (a matrix, not a recommendation)

| | **Refuse** (hard organ) | **Surface** (advisory + backstop) |
|---|---|---|
| Failure it prevents | a code-impact merge lands with no review artifact, permanently | same, but *after* the fact |
| Failure it introduces | a false positive blocks a legitimate merge; "code-impact" must be decided ex-ante and correctly | a real gap can ship and stay unnoticed until the backstop runs |
| Depends on | a correct, complete definition of "code-impact" at gate time | a backstop that actually runs, and someone reading it |
| Escape | `--no-verify` (non-silent iff a backstop reports it) | none needed |
| Cost of being wrong | blocks real work at 3am | records a gap nobody reads |
| Precedent in this repo | `block_unanchored_push` (ADR-85 hard leg, pre-push, fails CLOSED) | `preflight_backlog_ids` (`[#483]` R3, WARN-tier, structurally incapable of FAIL) |

### 3.1 Data point — the ADR-85 layered precedent (asymmetry is the feature)

The ADR-85 amendment deliberately made the pre-push organ's discharge **range-level** and the audit
backstop **per-entry**. Within two days the gap fired for real: a merge introduced `b18bf29f` that
no JOURNAL entry named; the pre-push gate passed the range and the **backstop caught it after the
fact** — the design's stated purpose, making a `--no-verify`-shaped hole visible later. It then
caught its own author a second time the same day.

Recorded verdict on that design, quoted not paraphrased: *"Nothing to fix; the asymmetry is the
feature. Do not 'simplify' the two organs into one predicate."*
(`docs/handoffs/2026-08-04-dev-knowledge-architect/RESIDUAL.md:101-109`)

**Why it is a data point and not an answer:** it establishes that this repo has already ruled, once,
that a hard organ and a softer backstop can coexist *on the same invariant* and that the asymmetry
between them is load-bearing. It does not establish which tier `[#480]` belongs in.

### 3.2 Data point — today's `[#310]` disposition flow

`[#483]`'s R3 wired the `preflight_backlog_ids` leg as **advisory, WARN-tier, structurally
incapable of FAIL** — verified at this anchor: the function's only return tiers are `n/a`, `warn`,
`pass`, including its exception handler.

```
$ sed -n '3594,3665p' scripts/audit.py | grep -c '"fail"'   -> 0
```

The ruling's stated reason is a measured one, not a preference: the leg's predecessor flagged
**11/11 correct historical citations** on its first production run, so a naive gate "REDs every
handoff bundle by construction." R3 defers hard-gating pending *measured evidence* — zero false
positives over two consecutive windows, reported at each seal.

Its one live finding was then dispositioned row-specifically rather than organ-wide:

```yaml
- id: warn-preflight-backlog-ids-310-292
  organ: preflight_backlog_ids
  match: "[#310] -> #292"          # the SPECIFIC row-and-id pair, not the organ
  ref: "#310"
  review_date: 2026-09-04           # shelf-life, so it cannot rot into paper suppression (ADR-75)
```

with the retire-on-close condition stated in the entry: *"it should clear by itself when FR-8a
grooms `[#310]`, at which point the entry decorates stale and is removed with it."*

**Why it is a data point:** it is a worked example of the *surface* branch done rigorously —
advisory tier by ruling, promotion gated on measured evidence, and the one known finding suppressed
precision-first (one row-and-id pair) with a shelf-life and a named retirement path, so the
suppression cannot silently become permanent. It shows what "surface" costs when done properly. It
does not show whether `[#480]` warrants the same treatment.

### 3.3 The outgoing seat's prior — **PRIOR, NOT EVIDENCE**

The outgoing 2026-08-02→04 seat's prior is **surface + backstop over hard refuse**.

It is recorded here because the plan-of-record requires it be visible and correctly labelled, and
for exactly one reason: so the incoming seat cannot mistake it for a finding. **§3 of the
plan-of-record states the argument runs fresh.** Nothing in this pack is arranged to support it.

---

## 4 · What this pack deliberately does NOT contain

- No recommendation on (a) or (b), and no implied one through ordering or emphasis.
- No acceptance contract and no build. FR-5's build is delegated to CC *after* the ruling.
- No claim that the 3-of-16 tally-persistence rate is good or bad — it is reported as measured.
- No re-litigation of the ADR-85 model, which is SETTLED.

## 5 · Honest limits of this pack

1. **Read at one anchor.** Every count is at `b9190b3a`. The window figures (10 vs 12) are quoted
   from their durable homes, not recomputed — the artifacts they counted include files this clone
   can see, but the *attribution window* that produced "10" is a session-time property this lane
   cannot reconstruct. The property in §1.1 is what survives, and it is what the ruling needs.
2. **Heading-shape census is regex-based**, run over the 16 window codex artifacts only. A finding
   recorded in prose under a shape none of the three regexes match counts as "no recognised shape";
   that is the intended reading (a machine cannot count it either), but it is not a claim that the
   artifact lacks findings.
3. **`0/0/0/0` was not re-observed by this lane** — the wrapper was not run. The figure is quoted
   from RESIDUAL/JOURNAL, which is precisely the durability problem `[#480](b)` names: there is no
   committed trace to re-read.

---

**Filed by:** CC night batch, 2026-08-04 · **Governs:** input to `[#480]` / FR-5 ·
**Cites:** `b9190b3a`, RESIDUAL.md §4, JOURNAL.md:717, `ecosystem/disposition-register.yaml`,
`scripts/audit.py:3594-3665`
