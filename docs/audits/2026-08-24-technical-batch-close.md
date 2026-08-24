# Batch close — the 2026-08-23/24 nine-branch batch

**Seat:** integrator, local, primary checkout · **Base:** `aeec0fd1` · **Head:** `4a476e89`
**Verification:** `docs/audits/2026-08-24-verification-integrator-merged-result.md`

---

## 0. What landed

Ten first-parent spine entries: nine queue branches plus the Step 3 checkpoint.

```
723618da  L6  worktree-rulings-landing            a85179bd  L6-FINAL
7a73a867  L1  worktree-provider-config            3cdf1126  L1-FINAL
d071e146  --  Step 3 operator checkpoint
c4f54c97  L3  worktree-status-grammar             3f663996  L3-FINAL
136fe4fd  L7  worktree-dispatch-codification      1e224c5a  L7-FINAL
0ad0cef7  L5  docs/l5-docs-actual-state           9638a626  L5-FINAL
18f2696a  C2  claude/ruling-provenance-audit      60a41ea9  C2-FINAL
3661d6e1  C1  claude/funnel-retro-classification  c3b0f45b  C1-FINAL
6bd59aa7  C3  claude/backlog-adjudication-prep    cabfa850  C3-FINAL
236da477  M9  claude/research-model-bus           7afd37c3  M9-FINAL
a0be7f1b  --  integrator Steps 4-7 + 9
```

**L2 (`2c6587d5`) and L4 (`278c26c6`) are OUT and untouched** — neither carries a sentinel
anywhere on its branch and each holds several hundred uncommitted lines. Held, not abandoned;
worktrees not entered, branches not merged, nothing torn down.

Every tip was asserted to BE its sentinel commit before merging. **No `--no-verify` anywhere.**

---

## 1. Mandate items M1–M12 — change · why · what-next

**An item with no carrier is an unmet mandate, and is labelled so.**

### M1 — Provider configuration · **LANDED**
- **Change:** L1 merged (`7a73a867`) — `ecosystem/schema/provider_registry.py` (pydantic,
  `extra="forbid"`), a hardened `check_provider_registry.py`, ~616 lines of new tests, and the
  `provider-registry-agreement` pre-commit gate. Plus this window's **provider-discoverability
  section** in `CONTRIBUTING.md` (`a3bfad8f`).
- **Why:** `claude-sonnet-5` was hardcoded in three file formats with nothing asserting they agree.
- **What-next:** **carrier = intake `#42`** (the root-`AGENTS.md` conflict that blocks `[#577]`)
  **+ L1's own fork 6.2**, drafted-not-ratified: *when a provider fails an admission floor, does
  the refusal remove it from configuration, or only from the roles it was evaluated for?* L1
  implements **(b)**; ratification is the architect's act, never a lane's.

### M2 — `codex/` folder disposition · **CLOSED BY RULING**
- **Change:** none, deliberately. **Ruling R7**: *keep in place, no relocation, no deletion; M2
  closed with the reason recorded.*
- **What-next:** nothing owed. R7 also records that M2 "was asking the wrong question"; the
  substance underneath it is carried by `[#577]`.

### M3 — Audit funnel coverage checker · **UNMET — lane held**
- **Change:** none. L2 (`worktree-funnel-coverage`) carries **no sentinel** and several hundred
  uncommitted lines; the contract holds it out of the queue.
- **What-next:** **carrier = `[#560]` (open)**. The work exists on an unmerged branch and in an
  un-torn-down worktree. **This is an unmet mandate for this window** — by deliberate hold, not
  by omission.

### M4 — Archival premise · **CLOSED BY RULING**
- **Change:** none in-tree. **Ruling R3**: the archival premise is retired; **ADR-100 reaffirmed
  index-only**, with the reason recorded.
- **What-next:** R3's item (i) — record `docs/intake/README.md` §5 as ratified in place and arm
  its two invariants — is **not** verified as landed by this window. **Flagged, not claimed.**

### M5 — Status-grammar validator + ADR marker sweep · **LANDED + REGISTERED**
- **Change:** L3 merged (`c4f54c97`); this window **registered** it — `ALL_CHECKS` **43 → 44**,
  `check_adr_status_grammar` is check #44, `coverage_scope` annotated, and the 2-site
  `governance-adr-status` edge resolving (`807685c6`, `948c6a3c`).
- **Why:** 47 of 87 live ADRs use a non-canonical grammar and nothing gated it.
- **Arming, stated honestly:** `enum` + `single-field` arm **FAIL** (both measure 0);
  `grammar(47)` / `coherence(3)` / `wrapped(1)` / `duplicate-id(2)` arm **WARN against a recorded
  baseline**. A WARN with a baseline is a measurement, not a gate — nothing stops 47 becoming 48.
- **The marker sweep executed NOTHING, and that is the ruled outcome:** ADR-94's in-place
  exception triggers only on a ratification event, and `Proposed` is **empty** across the live
  corpus — the trigger is unmeetable, not merely unmet.
- **What-next:** carriers **`[#242]`, `[#362]`**, both open.

### M6 — Functional docs to ACTUAL state · **LANDED**
- **Change:** L5 merged (`0ad0cef7`) — `CLAUDE.md` plus seven `protocols/` files reconciled to
  actual state.
- **Why:** the file that forbids restating a roster was restating one three lines below the rule.
- **What-next:** **no carrier row, by design** — L5 was an unfiled sweep. Nothing owed.

### M7 — Backlog view · **DISCHARGED THIS WINDOW**
- **Change:** ran `scripts/export_backlog_view.py`. **308 rows in 1.07 s (3.5 ms/row)** into the
  gitignored `.backlog-view/`; `git status` shows zero tracked files under it.
- **Why:** **Ruling R4 — "demonstrate, do not wire."** `[#563]`'s own binding condition 3 forbids
  re-pointing any gate, hook or script at the export. It was run and **never wired**.
- **Rank, measured from `tasks/` rather than restated:** **212 open rows** — 5 P1, 74 P2, 45 P3,
  and **39 open P2 sized S**. The answer to "unchanged and enormous" is that the set is 212 while
  its actionable near-term face is ~44 rows.
- **What-next:** carrier **`[#563]`**. One observation filed and not banked: **88 of the 212 open
  rows parse no priority/size band at all** — 41% of the open set is invisible to any priority
  sort.

### M8 — Generated-output commit path · **UNMET — lane held**
- **Change:** none. L4 (`worktree-dashboard-commit-path`) carries no sentinel and holds
  uncommitted work.
- **What-next:** **carrier = `[#171]` leg 1 (open)** — and Phase 0's Premise A already found leg 1
  is an **unruled (a)/(b) fork**, not an execution item. M8 is therefore unmet on two counts: the
  lane is held, *and* the thing it was to execute has not been ruled. **Unmet mandate.**

### M9 — Model-bus research · **LANDED**
- **Change:** merged (`236da477`); research only, read-only, no code.
- **What-next:** **carrier = a named ADR fork, unruled** — **A** registry-and-table (incumbent),
  **B** adapter-by-dependency, **C** bus-with-supersession. **A prior question must settle
  first:** does "model switching" mean switching the API a library calls, or switching the agent
  harness a lane runs under? If "harness", all three forks are the wrong menu and the live rows
  are `[#577]` and `[#568]`. **No intake was filed for it** — M9 is the one landed item whose
  carrier is a fork with no intake behind it, because `banked = 0` and the fork is already
  written up in its own artifact §7.

### M10 — Dispatch codification · **LANDED**
- **Change:** L7 merged (`136fe4fd`) — PLAYBOOK Ch8's three dispatch shapes, `gen_lane_contract`
  emitting the right one, ~266 lines of new tests. **Ruling R8** discharged here as the measured
  baseline (§3).
- **What-next:** **L7's R1 is owed and is NOT discharged by this window** —
  `templates/prompt-template.md` needs an update and its predecessor said so. No carrier row was
  filed (`banked = 0`). **Flagged as owed.**

### M11 — **UNRECOVERABLE FROM REPO STATE**
- `git grep M11` across `docs/` and `protocols/` returns exactly one hit, inside a **2026-07-11
  census brief using a different `[M1]`–`[M12]` namespace**. This batch's M-numbering exists only
  in the architect's off-repo mandate document.
- **This is itself the finding**, and it is precisely the defect intake `#43` documents: a mandate
  that lands nowhere cannot be closed out, audited, or even enumerated. **M11 cannot be reported
  on, because the repo does not know what M11 is.**

### M12 — Substrate router · **INTAKE FILED**
- **Change:** none in-tree, by design. **Carrier = intake `#45`**, fork named (machine-readable
  config consumed by `gen_lane_contract`, vs an ADR carrying the table as an appendix).
- **Why it is real, measured this window:** no cloud lane's commits passed a gate, because no hook
  was armed in any container — and **C1 shipped an audit artifact without regenerating the
  generated index**, a miss its container had no hook to catch. The integrator repaired it at
  merge. The compensating control worked, but it lives in prose in a hand-written contract; if a
  future contract omits that paragraph, ungated cloud output merges and nothing says so.

### Mandate scoreboard

| Outcome | Items |
|---|---|
| Landed | M1, M5, M6, M9, M10 |
| Discharged this window | M7 |
| Closed by ruling | M2, M4 |
| Intake filed, fork named | M12 |
| **UNMET** | **M3** (lane held), **M8** (lane held + unruled fork), **M11** (undefined in-repo) |

---

## 2. Objective functions, scored honestly

### The ledger prediction: **212 predicted, 0 actual**

The ledger predicted **212** — stated up front — as the count of backlog rows whose acceptance
criteria would be found **discharged**. Lane C3 evidenced all 212 rows and found **ZERO** with
discharged acceptance criteria.

**Actual against prediction: 212 predicted, 0 found. The prediction was wrong by its entire
magnitude.** It is recorded here rather than dropped, because a prediction named as wrong is
worth more than one quietly abandoned.

**An independent cross-check that the population itself was right:** this window's M7 rank
counted **212 open rows** directly from `tasks/`, arriving from the opposite direction. So the
denominator was correct and the *discharge* hypothesis was not — which is the more useful failure.
The rows exist; what does not exist is evidence that their stated acceptance was met.

### The silent-rule arithmetic: measured, never inherited

```
441  committed baseline @ 2026-07-30, detector silent-rule-v4
 +4  L7 PLAYBOOK Ch8            VERIFIED: blob 210 -> 214, matches L7 section R0 exactly
 +0  L5's seven protocols/      R8 predicted -5. MEASURED ZERO.
=445 live after the last merge, v4
 -2  RULING R12                 STANDING_RULINGS.md leaves scope
=443 live under silent-rule-v5, 58 files
```

**Neither 441, 445 nor 446 was the post-merge value**, exactly as the contract warned. The
baseline is set to **443**. R8's own diff directed the integrator to re-measure after the LAST
merge rather than pin its 445, and that instruction is what made the number right.

### Ship-gate against the Phase 0 baseline

| Metric | Phase 0 | Now | Δ |
|---|---|---|---|
| findings | 95 | 93 | −2 |
| WARN | 52 | 52 | 0 |
| dispositioned | 27 | 27 | 0 |
| undispositioned | 25 | 25 | 0 |
| `[stale]` | 3 | 3 | 0 |
| FAIL | 0 | **1** | **+1** |

Four of six metrics land **exactly** on baseline after nine merges. The single FAIL is the
detector migration (`origin/main` v4/441 vs `main` v5/443) and **clears on the operator's push** —
precedented verbatim in the baseline file's own provenance for the previous raise.

---

## 3. The two instructions this seat REFUSED, with evidence

### 3.1 Step 7's de-volatilization — refused by its own precondition

The contract ordered the six row-length dispositions stripped of their `(NNNN chars` values, but
required a `git blame` first and *"if the introducing commit gives a re-review rationale, stop and
report instead of stripping."*

- All six come from **`fce8b5b0`**, whose message states the design: *"A9 route (ii): six
  dispositions cover every live backlog-row-length locus, **keyed on row id AND measured
  length**."* A chosen route, not an oversight.
- **The register's own header mandates it:** *"KEY ON THE SPECIFIC BENIGN SIGNATURE … **NOT a
  bare id**, so a DIFFERENT future drift on the same id re-surfaces and blocks
  (precision-over-recall)."* Stripping produces exactly the bare id the header forbids.

**But the opposing evidence is now measured, and it is sharper than the contract's "3 already
dead":** `#533`'s disposition reads `(4210 chars` and decorates `[stale]`, while a **live
undispositioned WARN** reads `#533 (2239 chars`. The row was **trimmed — improved — and that broke
its own suppression**, so the WARN returned looking like new drift. `#529` and `#530` differ: both
dropped below the ceiling, so those two are legitimately stale.

**One proven silent break, not three.** Both readings now carry hard evidence, which is exactly
why this is an architect decision and not an integrator's. **Carrier: intake `#44`.**

### 3.2 Writing C1's funnel classes into the disposition register — no lawful shape

`ecosystem/disposition-register.yaml` suppresses ship-gate WARNs; every entry keys on a live
`Finding.check_name` via `organ:`. A funnel classification of an audit **file** has no organ and
no WARN, so there is no lawful entry shape for it. C1 itself ran **READ-ONLY** and records the
register as *"not written"*, using it only as a citation-target column.

Writing 318 file classifications into a gate-critical file would have corrupted it. **The ruled
classes F1 (bounded prefix at 2026-08-07, disposing 318 of 387 UNSURE), F3 (→ backlog row means
COVERED, never a birth) and F4 (file-level rollup is lawful) are recorded here instead**, and the
surface mismatch is reported rather than silently resolved. F2 and F5 are routed, not ruled, and
were not applied.

---

## 4. Contract premises that did not survive measurement

Recorded because they are one class — a contract stating a fact it had not verified — and that
class is now intake `#46`.

| Contract said | Measured | Consequence |
|---|---|---|
| `JOURNAL.md` touched by **six** branches, **two** collide | **eight** touch it; **six** all claim `2026-08-23 (k)` | 4× the predicted re-letter work |
| L5's rewording moves the silent-rule count **down by 5** | **net ZERO**; the whole +4 is L7's | baseline would have been wrong |
| L3's pin roster (four test pins) | **five** live pins — `tests/test_doc_code_edge.py:713` omitted | suite would have RED |
| `[#532]/A9` cited by **20** WARNs | **6** cite it; **18** cite the still-open `#241` | the defect is real, the count is not |

The contract was **right** where it said *"measure it, set it, and show your arithmetic"* — that
instruction produced the correct number precisely because there was nothing to inherit.

---

## 5. Every lane question, batched for the architect

1. **L1 fork 6.2 — configuration vs admission.** When a provider fails an admission floor, does
   the refusal remove it from *configuration* or only from the *roles* it was evaluated for? L1
   implements (b) and drafted a standing ruling **S-1** it did not land — ratification is the
   architect's, and L1 additionally records that the register could not take a new section at all.
2. **L7 R1 — `templates/prompt-template.md` is owed an update**, and its predecessor said so. Not
   discharged; no row filed (`banked = 0`).
3. **M9's ADR fork (A/B/C) and its prior question** — API-switching or harness-switching? The
   prior question changes which fork is even responsive.
4. **C1 F2 — which disposition vocabulary governs?** Two live vocabularies with four terms and
   five, and two terms have no counterpart. *"Do not leave both live — that is how a file gets two
   different dispositions and neither is wrong."* Routed, not ruled; needs the L17 ledger text.
5. **C1 F5 — the 25 closed-row dispositions and the 3 drifted register entries.** Rides intake
   `#44`.
6. **Intake `#42`'s open question, which generalizes well past `AGENTS.md`:** does a recorded
   ruling ever outrank a ratified `Accepted` ADR, or is the register strictly subordinate? This
   batch is the forcing example.
7. **`[#577]`'s Done-when is unexecutable as written** — it requires correcting `CLAUDE.md` §10, a
   hub-single-sourced region byte-matched to `templates/claude-regions/antipatterns-universal.md`,
   which the row never mentions. An architect item.
8. **The `[#241]` orphan risk:** 18 live dispositions `ref` it. It is open today; the day it
   closes, 18 suppressions orphan in one commit and nothing fires (P-2). Intake `#44`.

---

## 6. Queued row specifications — carried forward, NOT banked

**`banked = 0`. Zero task rows were filed this window.** Every row specification a lane wrote is
a queued proposal awaiting an explicit architect grant, listed here with its owning lane:

| Owning lane | Row specification | Status |
|---|---|---|
| L1 | standing ruling **S-1** (config-vs-admission), drafted verbatim | queued — needs ratification + a register that can take a section |
| L7 | **R1** `templates/prompt-template.md` update | queued — owed, unfiled |
| C3 | its adjudication row specifications across the 212-row prep sheet | queued — no verdicts, by design |
| C1 | the 306 proposed classifications | queued — proposal only; C1 ruled nothing |
| integrator | the 88 open rows carrying no priority/size band | observation only |

---

## 7. Held, and deliberately untouched

- **L2 `worktree-funnel-coverage` (`2c6587d5`)** — no sentinel, several hundred uncommitted lines.
- **L4 `worktree-dashboard-commit-path` (`278c26c6`)** — same.

Not merged, not entered, not torn down, worktrees intact. Their mandates (M3, M8) are reported
**unmet** above rather than quietly omitted.

---

## 8. What the operator must do

1. **Push `main`.** It is the operator's act and the contract reserves it. It also **clears the
   single ship-gate FAIL** — the `mixed` detector state resolves the moment `origin/main` carries
   the v5 baseline.
2. **Rule intake `#42`** — it blocks `[#577]`, and `[#577]`'s Done-when needs re-writing either way.
3. **Rule intake `#44`** — the row-length keying question this seat refused to decide unilaterally.
4. The remaining questions in §5 at whatever cadence suits.

**Nothing in this window was pushed. `main` is local and ahead of `origin/main`.**
