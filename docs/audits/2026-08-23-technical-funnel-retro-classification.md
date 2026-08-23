<!-- scope: meta -->
# Funnel retro-classification — every file in `docs/audits/` given a disposition state and one proposed classification

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-23 · **Slug:** `funnel-retro-classification`
- **Lane:** CLOUD C1 (`Dispatch-CloudV2`), M3 leg ii · **Branch:** `claude/funnel-retro-classification` · **Base:** `main` @ `aeec0fd`
- **Mode:** READ-ONLY. One artifact plus a `JOURNAL.md` entry; no other repo file touched. `scripts/` untouched. `ecosystem/disposition-register.yaml` **not written**.
- **Posture:** **this lane proposes; the architect rules.** Nothing below is a ruling. Every row is
  meant to be attackable, and §3 is the quote block that makes it attackable.
- **Governing rule:** `protocols/PLAYBOOK.md` Ch8 *"The wave close — every dispatched wave ends
  D0–D5, and the funnel table is mandatory"*, step **D4**; classifications are ADR-111 §1's four
  outcomes plus the executed case.

---

## 0. The answer first

```
N (files in docs/audits/)                     693      = 692 audit artifacts + 1 generated README.md index
enumerated, none skipped                      693
not reached                                     0

current disposition state
  PRESENT   (a resolvable carrier exists)     254
  NAMED-UNDISPOSITIONED (L17 section 4 list)   49
  STALE     (only a CLOSED row cites it)       14
  WEAK      (BACKLOG.md prose only)             1
  ABSENT    (no carrier anywhere)             375

one proposed classification                   306
  MECHANICAL                                  146
  REJECT-with-reason                           76
  COVERED                                      61
  INTAKE                                       22
  OUT-OF-SCOPE (the generated index)            1
UNSURE (two candidates + the decider)         387
```

**The two things this lane found that are worth the architect's attention before the table:**

1. **A second, architect-ruled disposition vocabulary already exists in the corpus** and it is not
   the funnel's five. `docs/audits/2026-08-17-technical-audit-disposition-ledger.md` carries a
   standing ruling of 2026-08-17 with the terms **ACTIONED / FILED / REJECTED / SUPERSEDED**
   (+ **PENDING** as used), and it dispositioned **80** audits under them and named **49** more as
   an explicit follow-on. The brief said *reconcile, do not add a sixth*; the sixth was already
   there before this lane started. §4 reconciles it and names the two terms that do not map.
2. **The corpus splits hard at 2026-08-10**, the day ADR-111 was ruled. **318 of the 387 UNSURE
   rows are pre-ratification.** Whether the retro-classification binds that half is a class ruling
   the architect owes, not a per-file judgement — fork **F1** in §7.

---

## 1. Container check — probed, not assumed

The brief required a probe rather than a static bypass. The probe **failed in two independent
ways**, so the mesh was hand-run.

```
uv --version                     -> uv 0.8.17
pyproject.toml:25 required-version = "==0.11.19"
uv run --locked python -c "..."  -> error: Required uv version `==0.11.19` does not match
                                    the running version `0.8.17`.
python3 --version                -> Python 3.11.15
python3 scripts/audit.py ship-gate -> ModuleNotFoundError: No module named 'click'
```

**Interpreter declaration.** Every measurement in this artifact was taken with **`python3` =
CPython 3.11.15**, invoked directly, with `scripts/` on `sys.path`. The two version strings are
**`uv 0.8.17` (running)** against **`==0.11.19` (pinned, `pyproject.toml:25`)**. The mismatch is
not the only blocker: this container also has **no `click`**, so `scripts/audit.py`'s CLI — and
therefore `ship-gate`, the surface that renders dispositions — **cannot be invoked here at all**.
That is a stronger statement than "the pin drifted", and it is why no `ship-gate` output is quoted
below as first-hand evidence.

**What was still measured first-hand.** `scripts/validate_doc_rot.py` imports without `click`, so
§8's row-length drift numbers were produced by **calling the repo's own detector**
(`validate_doc_rot.scan_backlog_accretion` on the live `BACKLOG.md`) rather than by reimplementing
it or by copying the phase-0 packet's figures. Where §8 agrees with
`docs/audits/2026-08-23-technical-phase0-preconditions.md`, that agreement is an independent
reproduction, not a citation.

---

## 2. Enumeration

`N = 693`. Every tracked file in `docs/audits/` is a `.md`; there are no non-markdown files. One of
the 693 is `docs/audits/README.md`, the **generated** index — it is enumerated and given a row, and
it was **not regenerated** (the brief reserves that for the integrator, and
`audit-index-freshness` in `CLAUDE.md` §9 is the gate that owns it).

Distribution by date, for the F1 fork:

```
2026-03   1     2026-06   92
2026-04  17     2026-07  170
2026-05  65     2026-08  347      (README.md carries no date)

before 2026-08-10 (ADR-111 ruled)   458
on/after 2026-08-10                 234   (+ README.md)
```

---

## 3. The clause block — the citation target

**Every classification below cites a key in this block, and the key resolves to quoted text here.**
A row citing a key whose quote is absent would be UNVERIFIED; there are none, because the block is
closed. Quotes are verbatim from the named file at `aeec0fd`.

**C1 — ADR-111 §1, the umbrella** (`docs/decisions/ADR-111-finding-triage-pipeline.md`):

> ### 1. Every finding is triaged into exactly one of four outcomes
>
> An audit finding is not actionable until it carries one of:

and, closing the same section:

> **An audit whose findings are untriaged is incomplete.** This is a property of the audit, not of
> the reader: producing 153 findings and no outcomes is an unfinished deliverable.

**C1a — OWNED:**

> - **(a) OWNED** — an open row already covers it. **Attach the evidence to that row; birth
>   nothing.**

**C1b — DISCHARGED:**

> - **(b) DISCHARGED** — already done, or already ruled. **Record it with its locator.** The
>   locator is mandatory and must resolve; "we already do that" without a locator is not a
>   discharge.

**C1c — CANDIDATE:**

> - **(c) CANDIDATE** — it needs a decision. It becomes, or joins, an **intake** — which is an idea
>   that may be rejected, not a commitment.

**C1d — REJECTED:**

> - **(d) REJECTED** — recorded with its reason, and **not relitigated**.

**C2 — ADR-100 §4, the genre split**, quoted verbatim inside ADR-111's Context section:

> *An audit produces evidence, never decisions* — **ADR-100 §4**, verbatim: "**Audit = evidence
> *about* state. Intake (ADR-98) = a request to *change* state.** They are **separate genres with
> separate lifecycles.**"

**C3 — PLAYBOOK Ch8, step D4** (`protocols/PLAYBOOK.md`, the wave-close subsection):

> **D4** | **THE FUNNEL TABLE.** Every finding, recommendation and residual from every artifact,
> classified into **exactly one** lawful next step, **each line citing its clause**. Then
> **PAUSE** — the architect returns one batched ruling over the whole table.

and the five terms, same subsection:

> - **MECHANICAL** — §1(b) DISCHARGED. […] a discharge is only a discharge **with a locator that
>   resolves** — "we already do that" without one is not a discharge.
> - **ADR** — §1(c) CANDIDATE where ADR-98 §3's fork test is met […]
> - **INTAKE** — §1(c) CANDIDATE otherwise. **A finding may not become a backlog row directly**
>   (§2) […]
> - **REJECT** — §1(d), **with the reason recorded where the finding lives**. A rejection is a
>   recorded decision rather than a silent drop, and it is **not relitigated**.
> - **COVERED** — §1(a) OWNED. Cite the id and **add nothing**.

**C4 — PLAYBOOK Ch8, honesty check 1** (the liveness rule this lane mechanized):

> 1. **A COVERED cite resolves to a LIVE row, or it is not COVERED.** Check it. A sibling arc
>    closing a row *while the lanes are in flight* is not hypothetical […] **That is how a
>    correctly-filed finding dies quietly.**

**C5 — ADR-111 §2, the no-direct-row rule:**

> The only path from a finding to a row runs through (c) → intake → ratification. A finding may not
> be filed directly as a row.

**C6 — `CLAUDE.md` §9, the index is generated:**

> - `audit-index-freshness` — regen-and-diff gate for the generated `docs/audits/README.md` index
>   vs `docs/audits/*.md` (`gen_audit_index.py --check`; shape-agnostic […]); guards against
>   silent index rot

**C7 — `CLAUDE.md` §5 rule 3, immutability** (why a retro-classification cannot be written *into*
these files and must live in a separate artifact such as this one):

> 3. **ADRs, transcripts, handoffs, and audits are immutable** — supersede with a new file or an
>    in-file amendment marker; never edit in place.

**C8 — the 2026-08-17 standing ruling** (`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`),
the vocabulary this lane discovered already in force:

> *Architect standing ruling, 2026-08-17 — audit-to-row conversion authority.* Every audit artifact
> carries exactly one disposition: **ACTIONED** (conclusion already live — cite the commit),
> **FILED** (a row owns it — cite the id), **REJECTED** (a ruling declined it — cite it),
> **SUPERSEDED** (a later artifact replaced it — cite it). An undisposed audit is a defect, not a
> document.

**C9 — the register's own decoration rule** (`ecosystem/disposition-register.yaml` header), used in §8:

> Decoration rule (ADR-75): an entry that matches NO live WARN on a run is SURFACED as
> stale in the gate's output (awareness — it does not block); the register is not allowed
> to silently rot into paper suppressions.

and the `match` contract from the same header:

> `match`  — a substring that must appear in the WARN's evidence. KEY ON THE SPECIFIC
> BENIGN SIGNATURE (e.g. the commit sha), NOT a bare id, so a DIFFERENT future
> drift on the same id re-surfaces and blocks (precision-over-recall).

**C10 — the repo's own forward-only precedent for a retro-reaching leg**
(`scripts/audit.py::check_review_artifact_coverage` docstring), which fork F1 turns on:

> FORWARD-ONLY from the ruling date. Of the 16 window artifacts only 3 carried a machine
> readable tally and 9 matched no recognised shape; those are immutable records, so a leg
> that reached backwards would demand retro-editing precisely what the ruling forbids
> touching. The date filter is the mechanism that makes "never retro-edited" true.

---

## 4. Reconciliation — the mandate's four terms, the funnel's five, and the ruled four already in the corpus

The brief asked for a reconciliation and said to report a mismatch rather than invent a term.
**There are three mismatches, and one of them is structural.**

### 4.1 The mandate's four terms → the funnel five

| mandate term | funnel term | clean? |
|---|---|---|
| rejected-with-reason | **REJECT** | clean — C1d and C3 are the same clause |
| → intake | **INTAKE** | clean — C1c |
| → ADR | **ADR** | clean — C1c where ADR-98 §3's fork test is met |
| → backlog row | **COVERED** *only* | **NOT clean — see 4.2** |
| *(no mandate term)* | **MECHANICAL** | the mandate has no term for §1(b) DISCHARGED |

### 4.2 Mismatch **M3** — "→ backlog row" is not a lawful outcome

C5 forbids it in terms: *"A finding may not be filed directly as a row."* The mandate's fourth term
can only mean **COVERED** — an **existing** live row absorbs the artifact. It can never mean *file a
new row for this audit*; that route is finding → **INTAKE** → ratification → row. **No row in this
table proposes a birth.** This is reported, not resolved: fork **F3**.

### 4.3 Mismatch **M1 / M2** — the ruled 2026-08-17 vocabulary has two terms the funnel does not

C8 is an architect standing ruling with four terms, and the ledger additionally used **PENDING**.
Mapping it onto the funnel:

| C8 term | funnel term | clean? |
|---|---|---|
| **ACTIONED** ("conclusion already live — cite the commit") | **MECHANICAL** | clean — C1b's "already done… record it with its locator" |
| **FILED** ("a row owns it — cite the id") | **COVERED** | clean **only if the row is still live** (C4) — 11 are not, §8.2 |
| **REJECTED** ("a ruling declined it — cite it") | **REJECT** | clean — C1d |
| **SUPERSEDED** ("a later artifact replaced it — cite it") | *none* | **M1 — no funnel term.** 2 instances |
| **PENDING** (as used: the decision is not this lane's) | *none* | **M2 — no funnel term.** 2 instances |

**M1.** A superseded artifact is neither owned, discharged, a candidate, nor rejected — its
conclusion was *replaced*, and C7 makes the supersession a new file rather than an edit. REJECT
with reason "superseded by X" is the nearest lawful shape; MECHANICAL with the successor as locator
is the other. This lane does not pick: fork **F2**.

**M2.** PENDING is the honest answer where the evidence stops and the decision belongs to someone
else — which is exactly ADR-111 §1(c) CANDIDATE in substance, but the ledger deliberately did *not*
route these to intake because the question is an operator GO, not an idea. Fork **F2**.

### 4.4 Mismatch **M4** — the funnel triages **findings**; this mandate triages **files**

C1 and C3 both take a **finding** as their unit. The mandate's unit is an **audit artifact**. A
file-level classification is therefore a **rollup**, and a rollup can be right about a file while
being wrong about one finding inside it. C8's ruling took the same file-level shape, so there is
precedent — but the precedent is a different vocabulary, which is how the two drifted apart in the
first place. **Every row in §6 is a file-level rollup.** Fork **F4**.

---

## 5. Method, and the honest limits of it

**What was computed, for all 693:**

1. **Every reference to the file from anywhere in `git ls-files`**, by two patterns — the full
   `docs/audits/<name>.md` path, and the bare dated stem. References from inside `docs/audits/`
   were separated from references outside it.
2. **Carrier strength and liveness.** A `tasks/*.md` citation was resolved to that row's frontmatter
   `status:`; only `open` and `deferred` count as LIVE (C4). `docs/intake/` citations were resolved
   to the intake's own status, including `docs/intake/archive/`.
3. **In-file disposition markers** — a literal `**Disposition:**` line (15 files), and the codex
   review header `**Tally:** C/H/M/L` (51 files; 7 of them `0/0/0/0`).
4. **The 2026-08-17 ledger, parsed** — its 80 table rows and their disposition cells, plus the 49
   names in its §4 follow-on list, plus the ids each FILED cell cites.
5. **The two wave-close funnels** (`2026-08-22-technical-cloud-wave-close-funnel.md`,
   `2026-08-23-technical-wave-close-funnel.md`) and the artifacts they name.

**What was read end-to-end by a human-equivalent pass:** `protocols/PLAYBOOK.md` Ch8's wave-close
subsection; `docs/decisions/ADR-111-finding-triage-pipeline.md` in full; all 30 entries of
`ecosystem/disposition-register.yaml` plus its header; `scripts/audit.py::check_review_artifact_coverage`'s
docstring; `scripts/validate_doc_rot.py`'s row-length arm.

**What was NOT read end-to-end: the 693 artifacts themselves.** Their first 40 lines were read
mechanically; six rows were hand-verified against the tree (two COVERED, two MECHANICAL, one INTAKE
whose intake turned out to live in `archive/` — the instrument was corrected for it — and one
no-carrier claim re-checked by grep). **This is the boundary that makes 387 rows UNSURE rather than
classified.** A single proposal is offered only where a predicate over the tree decides it; where
deciding would require reading the artifact's findings, the row says UNSURE and names what would
decide it.

**Four named limits of the instrument, each of which makes it MISS or over-credit:**

- **A reference is not ownership.** A `tasks/` row citing an audit as *prior art* is
  indistinguishable here from one that *owns its findings*. Every COVERED row is therefore a
  proposal about a citation, not a verified ownership claim.
- **The bare-stem matcher can over-match.** A dated slug appearing as prose could be counted as a
  reference. It cannot under-match a real path reference.
- **Contract detection is shape-based** — filename ending in `-contract`/`-brief`/`-prompt`/
  `-dispatch`, or a self-declaration in the head. A results artifact that merely *names* its
  contract is not counted (that false positive was found and removed); a contract with an unusual
  name may be missed.
- **`0/0/0/0` proves a tally, not a review.** `check_review_artifact_coverage`'s own honest limit
  applies verbatim: *"It cannot verify the review happened, was competent, or that the tally is
  truthful — a fabricated header passes."*

**Legend for the `◦` column:** `P` disposition PRESENT · `N` NAMED-UNDISPOSITIONED (in the L17 §4
follow-on list) · `S` STALE (only a CLOSED row cites it) · `W` WEAK (BACKLOG prose only) · `A`
ABSENT. A `·pre` suffix means the file predates ADR-111's 2026-08-10 ratification (fork F1).
`L17:` = the 2026-08-17 disposition ledger.

---

## 6. The funnel table

One row per file, all 693, grouped by proposed classification so the architect can rule a whole
class in one pass, then by filename descending (newest first) inside each class.

#### OUT-OF-SCOPE — 1

Not an audit artifact and not a finding; the brief forbids regenerating it.

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `README.md` | P | C6 | live row #269 |

#### MECHANICAL — §1(b) DISCHARGED — 146

Rule applied: a locator that resolves already carries this artifact's conclusion — the 2026-08-17 ledger's ACTIONED cell, the artifact's own `**Disposition:**` line, a wave-close funnel row, an ADR, or the doctrine/code file that cites it.

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-23-technical-lane-562-local-admission.md` | P | C1b | wave-close funnel |
| 2 | `2026-08-22-technical-cloud-2-563-view-layer.md` | P | C1b | scripts/export_backlog_view.py |
| 3 | `2026-08-22-technical-annotation-and-rulings-ledger.md` | P | C1b | wave-close funnel |
| 4 | `2026-08-22-fresh-eyes-cloud-4v2.md` | P | C1b | ecosystem/provider-registry.yaml |
| 5 | `2026-08-22-codex-cloud4v2-registries-terra.md` | P | C1b | wave-close funnel |
| 6 | `2026-08-22-codex-563-view-layer-terra.md` | P | C1b | in-file `**Disposition:**` |
| 7 | `2026-08-22-codex-562-nopack-sandbox-terra.md` | P | C1b | in-file `**Disposition:**` |
| 8 | `2026-08-21-fresh-eyes-cloud-r2-universalization.md` | P | C1b | ADR-114-readme-recreation-legality |
| 9 | `2026-08-21-census-cloud-r4-adr-review.md` | P | C1b | in-file `**Disposition:**` |
| 10 | `2026-08-20-technical-grok-ab-results-2.md` | P | C1b | scripts/nopack_sandbox.py |
| 11 | `2026-08-19-technical-n3-ratification-pack.md` | P | C1b | protocols/STANDING_RULINGS.md |
| 12 | `2026-08-19-technical-c4-ruling-prework.md` | P | C1b | scripts/gen_task_tree.py |
| 13 | `2026-08-19-technical-c1-seeded-defect-pack.md` | P | C1b | protocols/STANDING_RULINGS.md,scripts/nopack_sandbox.py |
| 14 | `2026-08-19-technical-554-proof.md` | P | C1b | scripts/cloud_provisioning.py,tests/test_cloud_provisioning.py |
| 15 | `2026-08-18-technical-phase0-baselines.md` | P | C1b | LESSONS.md,ecosystem/conformance.html |
| 16 | `2026-08-18-technical-batch1-integrator-packet.md` | P | C1b | ecosystem/conformance.html,ecosystem/conformance.md |
| 17 | `2026-08-18-technical-a9-trim-lane-packet.md` | P | C1b | ecosystem/disposition-register.yaml |
| 18 | `2026-08-17-technical-batch-7a-manifest.md` | P | C1b | L17:ACTIONED |
| 19 | `2026-08-17-technical-batch-7a-lane-a-contract.md` | P | C1b | L17:ACTIONED |
| 20 | `2026-08-16-technical-w2f-conversions-lane-contract.md` | P | C1b | L17:ACTIONED |
| 21 | `2026-08-16-technical-w2d-lane-contract.md` | P | C1b | L17:ACTIONED |
| 22 | `2026-08-16-technical-w2c-conversions-lane-contract.md` | P | C1b | L17:ACTIONED |
| 23 | `2026-08-16-technical-nb4-consolidated-briefing.md` | P | C1b | L17:ACTIONED |
| 24 | `2026-08-16-technical-k-293-cross-repo-seeding-lane-contract.md` | P | C1b | L17:ACTIONED |
| 25 | `2026-08-16-technical-batch-6-packet.md` | P | C1b | L17:ACTIONED |
| 26 | `2026-08-16-technical-batch-6-manifest.md` | P | C1b | L17:ACTIONED |
| 27 | `2026-08-16-technical-82-conversions-lane-contract.md` | P | C1b | L17:ACTIONED |
| 28 | `2026-08-16-technical-533-audit-decompose-lane-contract.md` | P | C1b | L17:ACTIONED |
| 29 | `2026-08-16-technical-532-docrot-arms-lane-contract.md` | P | C1b | L17:ACTIONED |
| 30 | `2026-08-16-technical-409-conversions-lane-a-contract.md` | P | C1b | L17:ACTIONED |
| 31 | `2026-08-16-technical-310-ledger-docs-lane-contract.md` | P | C1b | L17:ACTIONED |
| 32 | `2026-08-16-technical-277-issues-evidence-lane-contract.md` | P | C1b | L17:ACTIONED |
| 33 | `2026-08-16-technical-271-conversions-lane-contract.md` | P | C1b | L17:ACTIONED |
| 34 | `2026-08-16-technical-210-conversions-lane-contract.md` | P | C1b | L17:ACTIONED |
| 35 | `2026-08-15-verification-night3-landed-review.md` | P | C1b | L17:ACTIONED |
| 36 | `2026-08-15-technical-w20-draft-landing-lane-contract.md` | P | C1b | L17:ACTIONED |
| 37 | `2026-08-15-technical-night3-sessionplan.md` | P | C1b | L17:ACTIONED |
| 38 | `2026-08-15-technical-night3-decision-queue.md` | P | C1b | L17:ACTIONED |
| 39 | `2026-08-15-technical-night2-consolidated-briefing.md` | P | C1b | L17:ACTIONED |
| 40 | `2026-08-15-technical-gateclose-drain8-lane-contract.md` | P | C1b | L17:ACTIONED |
| 41 | `2026-08-15-technical-batch-phase1-packet.md` | P | C1b | L17:ACTIONED |
| 42 | `2026-08-15-technical-batch-phase1-manifest.md` | P | C1b | L17:ACTIONED |
| 43 | `2026-08-15-technical-530-single-flight-lane-contract.md` | P | C1b | L17:ACTIONED |
| 44 | `2026-08-15-technical-529-telemetry-emit-lane-contract.md` | P | C1b | L17:ACTIONED |
| 45 | `2026-08-15-technical-528-legs12-manifest.md` | P | C1b | L17:ACTIONED |
| 46 | `2026-08-15-technical-528-legs12-latency-lane-contract.md` | P | C1b | L17:ACTIONED |
| 47 | `2026-08-15-technical-527-block-main-lane-contract.md` | P | C1b | L17:ACTIONED |
| 48 | `2026-08-15-technical-293-consumer-runbook-fan-out-lane-contract.md` | P | C1b | L17:ACTIONED |
| 49 | `2026-08-14-verification-night2-plancheck.md` | P | C1b | L17:ACTIONED |
| 50 | `2026-08-14-verification-night2-hygiene.md` | P | C1b | L17:ACTIONED |
| 51 | `2026-08-14-technical-w4-wave2-conversion-drafts.md` | P | C1b | L17:ACTIONED |
| 52 | `2026-08-14-technical-night2-research.md` | P | C1b | L17:ACTIONED |
| 53 | `2026-08-14-technical-night2-latency.md` | P | C1b | L17:ACTIONED |
| 54 | `2026-08-14-technical-batch-4-true-close-packet.md` | P | C1b | L17:ACTIONED |
| 55 | `2026-08-14-technical-525-arch-organ-rows-lane-contract.md` | P | C1b | L17:ACTIONED |
| 56 | `2026-08-14-codex-524-check-extensions.md` | P | C1b | L17:ACTIONED |
| 57 | `2026-08-13-codex-w3-landing-predicate.md` | P | C1b | in-file `**Disposition:**` |
| 58 | `2026-08-12-verification-night-1-truth-audit-and-handoff-numbers.md` | P | C1b | protocols/STANDING_RULINGS.md |
| 59 | `2026-08-11-technical-batch-4-manifest.md` | P | C1b | protocols/STANDING_RULINGS.md |
| 60 | `2026-08-11-codex-lane-f-521-syspath-substrate.md` | P | C1b | in-file `**Disposition:**` |
| 61 | `2026-08-10-verification-fable-adversarial-plan-review.md` | P | C1b | ARCHITECTURE.md,protocols/STANDING_RULINGS.md |
| 62 | `2026-08-10-technical-origin-branch-census.md` | P | C1b | in-file `**Disposition:**` |
| 63 | `2026-08-10-technical-decision-sheet-verification.md` | P | C1b | in-file `**Disposition:**` |
| 64 | `2026-08-10-technical-backlog-testability-census.md` | P | C1b | protocols/STANDING_RULINGS.md |
| 65 | `2026-08-10-conformance-nightly-digest.md` | P | C1b | L17:ACTIONED |
| 66 | `2026-08-08-technical-502-pythonpath-measurement.md` | P·pre | C1b | LESSONS.md,protocols/STANDING_RULINGS.md |
| 67 | `2026-08-08-codex-lane-e-396-512-gitenv-scrub.md` | P·pre | C1b | L17:ACTIONED |
| 68 | `2026-08-08-codex-deploy-doc-carrier.md` | P·pre | C1b | L17:ACTIONED |
| 69 | `2026-08-07-technical-lane-2-worktree-portability.md` | P·pre | C1b | tests/test_worktree_import_proof.py |
| 70 | `2026-08-07-technical-batch-2-lessons.md` | P·pre | C1b | protocols/PLAYBOOK.md |
| 71 | `2026-08-07-conformance-nightly-digest.md` | P·pre | C1b | L17:ACTIONED |
| 72 | `2026-08-07-codex-pre2-selfreview-arc.md` | P·pre | C1b | L17:ACTIONED |
| 73 | `2026-08-07-codex-pre2-arc-retro.md` | P·pre | C1b | L17:ACTIONED |
| 74 | `2026-08-07-codex-pre-cut-retro-handoff-engine-thinning.md` | P·pre | C1b | in-file `**Disposition:**` |
| 75 | `2026-08-07-codex-morning-f4-retro.md` | P·pre | C1b | L17:ACTIONED |
| 76 | `2026-08-07-codex-lane-b-503-retro.md` | P·pre | C1b | L17:ACTIONED |
| 77 | `2026-08-07-codex-lane-a-501-retro.md` | P·pre | C1b | L17:ACTIONED |
| 78 | `2026-08-07-codex-lane-1-490-430-parity-manifest.md` | P·pre | C1b | L17:ACTIONED |
| 79 | `2026-08-06-technical-night-prep-packs.md` | P·pre | C1b | ADR-101-hermetization |
| 80 | `2026-08-06-technical-batch1-verification.md` | P·pre | C1b | ADR-110-parallel-execution-batch-protocol |
| 81 | `2026-08-06-codex-lane-c-504-failclosed.md` | P·pre | C1b | ecosystem/disposition-register.yaml |
| 82 | `2026-08-04-technical-483-enforcement-ruling.md` | P·pre | C1b | protocols/STANDING_RULINGS.md,scripts/preflight_contract.py |
| 83 | `2026-08-03-technical-night-lb-groom.md` | P·pre | C1b | ADR-82-handoff-process-v5-model-c |
| 84 | `2026-08-02-technical-night-batch-lb-fleet-audit-commits.md` | P·pre | C1b | tests/test_hub_identity.py |
| 85 | `2026-08-01-technical-night-batch-l4-frontmatter-parser.md` | P·pre | C1b | scripts/gen_task_tree.py |
| 86 | `2026-07-31-verification-382-ladder-evidence.md` | P·pre | C1b | ADR-113-l0-l5-maturity-ladder-ratification |
| 87 | `2026-07-31-technical-v6-open-rulings.md` | P·pre | C1b | protocols/HANDOFF_PROCESS.md,scripts/assemble_paste.py |
| 88 | `2026-07-31-technical-382-schema-derivation-sol.md` | P·pre | C1b | ADR-109-fleet-desired-state-contract-v1 |
| 89 | `2026-07-31-technical-382-registry-prep-dossier.md` | P·pre | C1b | ADR-109-fleet-desired-state-contract-v1 |
| 90 | `2026-07-31-codex-382-w4-report.md` | P·pre | C1b | scripts/desired_state_report.py,tests/test_desired_state_report.py |
| 91 | `2026-07-31-codex-382-w3-loader.md` | P·pre | C1b | tests/test_desired_state_loader.py |
| 92 | `2026-07-31-codex-382-w2-schema-v1.md` | P·pre | C1b | tests/test_desired_state_schema.py |
| 93 | `2026-07-30-technical-night-batch-standing-section-draft.md` | P·pre | C1b | in-file `**Disposition:**` |
| 94 | `2026-07-28-technical-382-charter.md` | P·pre | C1b | ADR-109-fleet-desired-state-contract-v1 |
| 95 | `2026-07-28-codex-437-closure-recheck.md` | P·pre | C1b | in-file `**Disposition:**` |
| 96 | `2026-07-27-verification-433-schema-spike.md` | P·pre | C1b | ADR-107-backlog-restructure-engine-schema-viewer |
| 97 | `2026-07-27-codex-adversarial-review-adr-107-sol.md` | P·pre | C1b | ADR-107-backlog-restructure-engine-schema-viewer |
| 98 | `2026-07-27-census-silent-rule-ratchet-arm-measurement.md` | P·pre | C1b | ecosystem/silent-rule-baseline.yaml,scripts/silent_rule_detector.py |
| 99 | `2026-07-19-codex-residual-completeness-gate.md` | P·pre | C1b | tests/test_residual_completeness.py |
| 100 | `2026-07-19-census-silent-rule-ledger.md` | P·pre | C1b | LESSONS.md |
| 101 | `2026-07-16-technical-fleet-structure-census.md` | P·pre | C1b | ADR-103-parity-ownership-axis |
| 102 | `2026-07-13-technical-wave3-reading-friction-census.md` | P·pre | C1b | in-file `**Disposition:**` |
| 103 | `2026-07-11-technical-fleet-boundary-marker-design.md` | P·pre | C1b | protocols/PLAYBOOK.md |
| 104 | `2026-07-09-night-hygiene-audit.md` | P·pre | C1b | ADR-101-hermetization |
| 105 | `2026-07-09-changelog-review.md` | P·pre | C1b | ecosystem/tool-versions.yaml |
| 106 | `2026-07-07-overnight-mission-ledger.md` | P·pre | C1b | LESSONS.md |
| 107 | `2026-07-06-changelog-review.md` | P·pre | C1b | protocols/PLAYBOOK.md |
| 108 | `2026-07-05-ai-council-measurement-2.md` | P·pre | C1b | LESSONS.md |
| 109 | `2026-07-04-fable-architecture-review.md` | P·pre | C1b | protocols/DEFINITION_OF_DONE.md |
| 110 | `2026-07-04-codex-lived-sandbox-slice-a.md` | P·pre | C1b | tests/fixtures/lived-workflow/arc-silent.jsonl |
| 111 | `2026-06-23-handoff-process-audit-findings.md` | P·pre | C1b | ADR-81-feature-lifecycle-definition-of-done |
| 112 | `2026-06-21-doc-code-edge-fit-check.md` | P·pre | C1b | ADR-89-computed-code-dependency-edges |
| 113 | `2026-06-20-pyright-reverse-dep-oracle-findings.md` | P·pre | C1b | ADR-89-computed-code-dependency-edges |
| 114 | `2026-06-19-hook-completeness-audit.md` | P·pre | C1b | ADR-85-session-lifecycle-enforcement |
| 115 | `2026-06-15-changelog-review.md` | P·pre | C1b | ADR-70-amendment-2026-07-07-fable-xl-tier |
| 116 | `2026-06-14-ecosystem-audit.md` | P·pre | C1b | tests/test_audit.py,tests/test_validate_hermetization.py |
| 117 | `2026-06-11-surface-responsibility-audit.md` | P·pre | C1b | LESSONS.md |
| 118 | `2026-06-11-architecture-coherence-audit.md` | P·pre | C1b | LESSONS.md |
| 119 | `2026-06-07-methodology-transfer-audit.md` | P·pre | C1b | ARCHITECTURE.md |
| 120 | `2026-06-07-conformance-nightly-digest.md` | P·pre | C1b | ADR-80-two-tier-automation-adoption |
| 121 | `2026-06-06-conformance-nightly-digest.md` | P·pre | C1b | ADR-80-two-tier-automation-adoption |
| 122 | `2026-06-06-85-validation-record.md` | P·pre | C1b | ADR-80-two-tier-automation-adoption |
| 123 | `2026-06-05-living-doc-staleness.md` | P·pre | C1b | ARCHITECTURE.md,protocols/PLAYBOOK.md |
| 124 | `2026-06-05-conformance-nightly-digest.md` | P·pre | C1b | ADR-72-cloud-routine-hub-independence |
| 125 | `2026-06-03-protocols-rot-audit.md` | P·pre | C1b | LESSONS.md |
| 126 | `2026-06-03-doc-tooling-inventory.md` | P·pre | C1b | ADR-71-doc-tooling-hook-source-repo |
| 127 | `2026-06-03-codemap-grounding.md` | P·pre | C1b | ADR-71-doc-tooling-hook-source-repo |
| 128 | `2026-06-01-backlog-migration-inventory.md` | P·pre | C1b | ADR-65-backlog-done-item-disposition |
| 129 | `2026-05-31-backlog-architecture-diagnosis.md` | P·pre | C1b | ADR-64-backlog-architecture,ADR-65-backlog-done-item-disposition |
| 130 | `2026-05-29-handoff-v3.4-process-audit.md` | P·pre | C1b | ADR-42-handoff-format-v3,ADR-45-handoff-architecture-v4,ADR-55-applied-task-internalization-gate,ADR-56-prompt-generation-card,ADR-57-two-layer-bundle-contract,ADR-58-structured-claims-verification,ADR-62-v4-handoff-process-ratification,ADR-63-scrum-master-review-authority |
| 131 | `2026-05-29-ecosystem-coherence-audit.md` | P·pre | C1b | ADR-63-scrum-master-review-authority |
| 132 | `2026-05-27-taxonomy-simplification-verification.md` | P·pre | C1b | ADR-60-docs-folder-taxonomy |
| 133 | `2026-05-27-concurrency-anomaly-cleanup-2026-05-26.md` | P·pre | C1b | ADR-61-git-worktree-parallel-sessions |
| 134 | `2026-05-26-cross-repo-universalization-verification.md` | P·pre | C1b | ADR-59-universal-visual-repository-pattern |
| 135 | `2026-05-25-council-pipeline-proposal.md` | P·pre | C1b | ADR-60-docs-folder-taxonomy |
| 136 | `2026-05-25-council-pipeline-audit.md` | P·pre | C1b | ADR-60-docs-folder-taxonomy |
| 137 | `2026-05-24-backlog-audit-and-universalization-scoping.md` | P·pre | C1b | ADR-63-scrum-master-review-authority |
| 138 | `2026-05-23-ai-council-deep-audit.md` | P·pre | C1b | ADR-38-universal-repo-architecture |
| 139 | `2026-05-20-handoff-process.md` | P·pre | C1b | ADR-39-file-lifecycle-governance,ADR-45-handoff-architecture-v4 |
| 140 | `2026-05-19-dev-knowledge-posture-audit.md` | P·pre | C1b | protocols/PLAYBOOK.md |
| 141 | `2026-05-19-cohort1-verification.md` | P·pre | C1b | ADR-53-claude-md-single-instruction-file |
| 142 | `2026-05-12-handoff-process-audit.md` | P·pre | C1b | ADR-45-handoff-architecture-v4 |
| 143 | `2026-05-11-ai-council-scrum-master-review.md` | P·pre | C1b | LESSONS.md,protocols/PLAYBOOK.md |
| 144 | `2026-04-30-dev-knowledge-self-audit.md` | P·pre | C1b | ADR-39-file-lifecycle-governance |
| 145 | `2026-04-21-dev-knowledge-scope-tagging.md` | P·pre | C1b | ADR-27-scope-tagging,ADR-29-lessons-grandfathering |
| 146 | `2026-04-21-dev-knowledge-inventory.md` | P·pre | C1b | ADR-27-scope-tagging |

#### COVERED — §1(a) OWNED — 61

Rule applied: a **live** `tasks/` row (frontmatter `status: open` or `deferred`) cites the artifact. Liveness was checked per PLAYBOOK D4 check 1, never assumed.

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-23-technical-wave-close-funnel.md` | P | C1a | live row #578 |
| 2 | `2026-08-22-technical-intake-r1-decision-packet.md` | P | C1a | live row #577 |
| 3 | `2026-08-22-technical-cloud-wave-close-funnel.md` | P | C1a | live row #577 |
| 4 | `2026-08-21-technical-library-first-research.md` | P | C1a | live row #573 |
| 5 | `2026-08-21-technical-lane-tel-run-id.md` | P | C1a | live row #575 |
| 6 | `2026-08-21-technical-lane-rat-intake-ratification.md` | P | C1a | live row #572 |
| 7 | `2026-08-20-technical-playbook-status.md` | P | C1a | live row #569 |
| 8 | `2026-08-20-technical-gemini-ab-results.md` | P | C1a | live row #491 |
| 9 | `2026-08-20-technical-codespaces-audit.md` | P | C1a | live row #541,#567 |
| 10 | `2026-08-19-technical-n5-codification-pack.md` | P | C1a | live row #560 |
| 11 | `2026-08-19-technical-n4-grooming-wave1.md` | P | C1a | live row #534 |
| 12 | `2026-08-17-technical-audit-disposition-ledger.md` | P | C1a | live row #551 |
| 13 | `2026-08-17-census-nb7-orphan-census.md` | P | C1a | live row #559 |
| 14 | `2026-08-16-verification-nb4-playbook-gap.md` | P | C1a | L17:FILED(#538=open) |
| 15 | `2026-08-16-technical-nb6-handoff-prep.md` | P | C1a | L17:FILED(#453=open) |
| 16 | `2026-08-16-technical-nb5-seam-repoint.md` | P | C1a | L17:FILED(#533=open,#535=open) |
| 17 | `2026-08-16-technical-nb5-consumer-home.md` | P | C1a | L17:FILED(#293=open,#303=open) |
| 18 | `2026-08-16-technical-nb4-llm-acceptance.md` | P | C1a | L17:FILED(#491=deferred) |
| 19 | `2026-08-16-technical-nb4-g-scaleout-substrate-v2.md` | P | C1a | L17:FILED(#541=open) |
| 20 | `2026-08-16-technical-nb4-fleet-parity.md` | P | C1a | L17:FILED(#293=open,#303=open,#393=open) |
| 21 | `2026-08-16-technical-k-293-cross-repo-seeding-lane-packet.md` | P | C1a | L17:FILED(#293=open,#303=open) |
| 22 | `2026-08-16-census-nb4-closing-campaign.md` | P | C1a | L17:FILED(#506=open) |
| 23 | `2026-08-15-technical-night3-research.md` | P | C1a | L17:FILED(#540=open) |
| 24 | `2026-08-15-codex-n-review.md` | P | C1a | L17:FILED(#528=open) |
| 25 | `2026-08-14-census-night2-census.md` | P | C1a | L17:FILED(#506=open) |
| 26 | `2026-08-13-verification-492-corpus-reconciliation.md` | P | C1a | live row #492 |
| 27 | `2026-08-12-technical-roadmap-north-star-frozen.md` | P | C1a | live row #523 |
| 28 | `2026-08-11-technical-batch-4-packet.md` | P | C1a | live row #514 |
| 29 | `2026-08-08-technical-lane-c-393-corpsca-rot-review.md` | P·pre | C1a | L17:FILED(#393=open) |
| 30 | `2026-08-08-technical-closure-wave-proposals.md` | P·pre | C1a | L17:FILED(#506=open) |
| 31 | `2026-08-07-technical-batch-2-packet.md` | P·pre | C1a | live row #509 |
| 32 | `2026-08-06-technical-night-408-coupling-manifest-design.md` | P·pre | C1a | live row #408 |
| 33 | `2026-08-04-codex-483-preflight-discrimination.md` | P·pre | C1a | live row #492 |
| 34 | `2026-08-04-codex-481-organ-id-rename.md` | P·pre | C1a | live row #496 |
| 35 | `2026-08-03-technical-383-caches-wave-record.md` | P·pre | C1a | live row #383 |
| 36 | `2026-07-31-technical-p10-grooming-dossier.md` | P·pre | C1a | live row #506 |
| 37 | `2026-07-30-technical-v6-spec-sol-draft.md` | P·pre | C1a | live row #448 |
| 38 | `2026-07-29-codex-postflip-fix-batch-review.md` | P·pre | C1a | live row #445 |
| 39 | `2026-07-27-codex-436-ratchet-final.md` | P·pre | C1a | live row #438 |
| 40 | `2026-07-23-technical-status-enum-reconcile.md` | P·pre | C1a | live row #402 |
| 41 | `2026-07-22-verification-night-batch-integration-386-384.md` | P·pre | C1a | live row #391,#392,#393 |
| 42 | `2026-07-22-technical-night-batch-deep-audit.md` | P·pre | C1a | live row #400 |
| 43 | `2026-07-22-technical-hygiene-pre-handoff-inventory.md` | P·pre | C1a | live row #399 |
| 44 | `2026-07-21-technical-night-vision-audit.md` | P·pre | C1a | live row #388 |
| 45 | `2026-07-20-technical-352-boundary-render-diagnostic.md` | P·pre | C1a | live row #371 |
| 46 | `2026-07-19-technical-night-s7-prompt-authoring-quality.md` | P·pre | C1a | live row #389 |
| 47 | `2026-07-19-technical-night-s4-handoff-playbook-currency.md` | P·pre | C1a | live row #356 |
| 48 | `2026-07-19-technical-night-consolidated-cycle-close.md` | P·pre | C1a | live row #354 |
| 49 | `2026-07-19-codex-residual-rule-declaration.md` | P·pre | C1a | live row #366 |
| 50 | `2026-07-19-codex-cycle-close-terra-review.md` | P·pre | C1a | live row #354 |
| 51 | `2026-07-12-technical-night-codex-review.md` | P·pre | C1a | live row #324 |
| 52 | `2026-07-12-codex-ruff-hub-pin.md` | P·pre | C1a | live row #334 |
| 53 | `2026-07-11-technical-fleet-parity-register.md` | P·pre | C1a | live row #327,#329,#331 |
| 54 | `2026-07-08-fleet-consistency-census.md` | P·pre | C1a | live row #269,#285 |
| 55 | `2026-07-08-census-amendment-docs-handoffs-ruling.md` | P·pre | C1a | live row #303 |
| 56 | `2026-07-06-ai-council-measurement-3.md` | P·pre | C1a | live row #267 |
| 57 | `2026-07-05-draft-tier2-nightly-layer.md` | P·pre | C1a | live row #271 |
| 58 | `2026-06-21-audit-ops-findings.md` | P·pre | C1a | live row #277 |
| 59 | `2026-06-20-removal-closure-spike-findings.md` | P·pre | C1a | live row #218 |
| 60 | `2026-06-07-platform-max-audit.md` | P·pre | C1a | live row #116,#117 |
| 61 | `2026-06-04-pilot81-hub-conformance-digest.md` | P·pre | C1a | live row #288 |

#### INTAKE — §1(c) CANDIDATE — 22

Rule applied: an intake doc under `docs/intake/` (or `docs/intake/archive/`) cites the artifact; the intake's own status is shown.

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-21-technical-graph-and-workflows.md` | P | C1c | intake 2026-08-22-tech-document-dependency-graph-organ.md |
| 2 | `2026-08-12-technical-night-2-lessons-governance-strategy.md` | P | C1c | intake 2026-08-12-func-repo-self-description-consolidation.md |
| 3 | `2026-08-11-technical-batch-4-brief-next-architect.md` | P | C1c | intake 2026-08-12-func-repo-self-description-consolidation.md |
| 4 | `2026-08-10-verification-arc9-rulings-recording.md` | P | C1c | intake 2026-08-08-func-multi-model-execution-and-distillation.md |
| 5 | `2026-08-10-technical-research-corpus-distillate.md` | P | C1c | intake 2026-08-08-func-multi-model-execution-and-distillation.md |
| 6 | `2026-08-09-technical-night-n3-performance-instrumentation.md` | P·pre | C1c | intake 2026-08-06-tech-adoption-consolidation-intake.md,2026-08-09-tech-compute-placement-and-remote-execution.md |
| 7 | `2026-08-09-technical-consolidation-report.md` | P·pre | C1c | intake 2026-08-05-func-simplification-distribution-wave.md,2026-08-09-func-code-style-doctrine.md,2026-08-09-tech-compute-placement-and-remote-execution.md |
| 8 | `2026-08-08-technical-successor-prep.md` | P·pre | C1c | intake 2026-08-06-tech-adoption-consolidation-intake.md |
| 9 | `2026-08-08-technical-seeded-defect-substrate-inventory.md` | P·pre | C1c | intake 2026-08-08-func-multi-model-execution-and-distillation.md |
| 10 | `2026-08-08-technical-library-research.md` | P·pre | C1c | intake 2026-08-06-tech-adoption-consolidation-intake.md |
| 11 | `2026-08-08-technical-batch-3-packet.md` | P·pre | C1c | intake 2026-08-06-tech-adoption-consolidation-intake.md,2026-08-09-tech-compute-placement-and-remote-execution.md |
| 12 | `2026-08-03-technical-night-lf-rulings-prep.md` | P·pre | C1c | intake 2026-07-30-func-operator-decision-routing-and-standards.md |
| 13 | `2026-07-30-technical-vscode-w1-execution-record.md` | P·pre | C1c | intake 2026-07-30-tech-browser-architect-orientation.md |
| 14 | `2026-07-30-technical-intake18-ratification-record.md` | P·pre | C1c | intake 2026-07-27-tech-handoff-process-v6-proposal.md,2026-07-30-tech-browser-architect-orientation.md |
| 15 | `2026-07-27-verification-handoff-process-audit.md` | P·pre | C1c | intake 2026-07-27-tech-handoff-process-v6-proposal.md |
| 16 | `2026-07-13-technical-satellite-onboarding-census.md` | P·pre | C1c | intake 2026-07-16-satellite-onboarding-prompts.md |
| 17 | `2026-07-12-technical-night-c4-requirements.md` | P·pre | C1c | intake 2026-07-11-tech-c4-visualization-memo.md |
| 18 | `2026-07-11-technical-fleet-structure-comparison.md` | P·pre | C1c | intake 2026-07-13-siem-fleet-management-requirements-codex.md,2026-07-13-siem-fleet-management-requirements.md |
| 19 | `2026-07-07-changelog-review.md` | P·pre | C1c | intake 2026-07-07-changelog-review-seeds.md |
| 20 | `2026-07-06-arc5-routines-pilot-design.md` | P·pre | C1c | intake 2026-07-06-platform-feature-scan.md |
| 21 | `2026-07-06-arc5-must-verification.md` | P·pre | C1c | intake 2026-07-06-platform-feature-scan.md |
| 22 | `2026-07-06-arc5-buy-vs-build-verdicts.md` | P·pre | C1c | intake 2026-07-07-arc5-pilot-followup-seeds.md,2026-07-06-platform-feature-scan.md |

#### REJECT-with-reason — §1(d) — 76

Rule applied: the artifact bears **no finding to triage** — it is a dispatch record (contract / brief / prompt), or a codex review whose own `**Tally:**` is `0/0/0/0`, or the 2026-08-17 ledger already recorded a named authority's declination.

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-22-technical-lane-fix-562-guard.md` | A | C2 | no reference outside docs/audits/ |
| 2 | `2026-08-22-codex-562-guard-fix-terra-r12.md` | A | C1 | no reference outside docs/audits/ |
| 3 | `2026-08-21-technical-seat-act0-act1-contract.md` | A | C2 | no reference outside docs/audits/ |
| 4 | `2026-08-21-technical-library-first-research-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 5 | `2026-08-21-technical-lane-tel-run-id-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 6 | `2026-08-21-technical-lane-rat-intake-ratification-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 7 | `2026-08-21-technical-lane-arch-lifecycle-archival-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 8 | `2026-08-21-technical-lane-554-cloud-provisioning-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 9 | `2026-08-21-technical-graph-and-workflows-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 10 | `2026-08-21-technical-cloud-r4-brief.md` | A | C2 | no reference outside docs/audits/ |
| 11 | `2026-08-21-technical-cloud-r3-brief.md` | A | C2 | no reference outside docs/audits/ |
| 12 | `2026-08-21-technical-cloud-r2-brief.md` | A | C2 | no reference outside docs/audits/ |
| 13 | `2026-08-21-technical-cloud-r1-brief.md` | A | C2 | no reference outside docs/audits/ |
| 14 | `2026-08-21-technical-ch8-dispatch-codification.md` | A | C2 | JOURNAL/handoff mention only |
| 15 | `2026-08-21-technical-ch8-dispatch-codification-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 16 | `2026-08-20-technical-transcription-seat-contract.md` | P | C2 | protocols/STANDING_RULINGS.md |
| 17 | `2026-08-20-technical-playbook-status-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 18 | `2026-08-20-technical-parallel-flip-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 19 | `2026-08-20-technical-grok-ab-lane-contract-2.md` | A | C2 | no reference outside docs/audits/ |
| 20 | `2026-08-20-technical-gemini-ab-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 21 | `2026-08-20-technical-gemini-ab-lane-contract-slot1.md` | A | C2 | JOURNAL/handoff mention only |
| 22 | `2026-08-20-technical-final-integrator-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 23 | `2026-08-19-technical-s1-seat-arc-contract.md` | P | C2 | intake 2026-08-17-tech-fleet-config-standardization.md,2026-08-17-tech-off-machine-agent-substrate.md |
| 24 | `2026-08-19-technical-n5-codification-pack-contract.md` | A | C2 | no reference outside docs/audits/ |
| 25 | `2026-08-19-technical-n3-ratification-pack-contract.md` | A | C2 | no reference outside docs/audits/ |
| 26 | `2026-08-19-technical-n2-seam-worksheet-contract.md` | A | C2 | no reference outside docs/audits/ |
| 27 | `2026-08-19-technical-n1-wiring-spec-contract.md` | A | C2 | no reference outside docs/audits/ |
| 28 | `2026-08-19-technical-morning-consolidation-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 29 | `2026-08-19-technical-l2-wiring-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 30 | `2026-08-19-technical-cloud-c6-brief.md` | A | C2 | no reference outside docs/audits/ |
| 31 | `2026-08-19-technical-cloud-c4-brief.md` | A | C2 | no reference outside docs/audits/ |
| 32 | `2026-08-19-technical-cloud-c3-brief.md` | A | C2 | no reference outside docs/audits/ |
| 33 | `2026-08-19-technical-cloud-c2-brief.md` | A | C2 | no reference outside docs/audits/ |
| 34 | `2026-08-19-technical-cloud-c1-brief.md` | A | C2 | no reference outside docs/audits/ |
| 35 | `2026-08-19-technical-c6-telemetry-readpath-contract.md` | A | C2 | no reference outside docs/audits/ |
| 36 | `2026-08-19-technical-c4-ruling-prework-contract.md` | A | C2 | no reference outside docs/audits/ |
| 37 | `2026-08-19-technical-c3-grooming-wave2-contract.md` | A | C2 | no reference outside docs/audits/ |
| 38 | `2026-08-19-technical-c2-review-profiles-contract.md` | A | C2 | no reference outside docs/audits/ |
| 39 | `2026-08-19-technical-c1-seeded-defects-contract.md` | A | C2 | no reference outside docs/audits/ |
| 40 | `2026-08-19-technical-backlogmd-trial.md` | S | C2 | only CLOSED row #563 |
| 41 | `2026-08-19-technical-backlogmd-trial-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 42 | `2026-08-19-technical-554-proof-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 43 | `2026-08-19-technical-486-cp1252-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 44 | `2026-08-19-technical-171-dashboard-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 45 | `2026-08-18-technical-review-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 46 | `2026-08-18-technical-p10-regen-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 47 | `2026-08-18-technical-batch1-integrator-contract.md` | A | C2 | no reference outside docs/audits/ |
| 48 | `2026-08-18-technical-adoption-preflight-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 49 | `2026-08-18-technical-a9-trim-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 50 | `2026-08-18-technical-554-devcontainer-lane-contract.md` | P | C2 | ADR-101-hermetization |
| 51 | `2026-08-18-technical-533-leg2-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 52 | `2026-08-18-technical-502-mutmut-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 53 | `2026-08-17-technical-research-intake-lane-contract.md` | P | C2 | intake 2026-08-17-tech-agent-instruction-layers-and-distillation.md,2026-08-17-tech-fleet-config-standardization.md,2026-08-17-tech-machine-verifiable-done-when.md,2026-08-17-tech-off-machine-agent-substrate.md,2026-08-17-tech-repository-autonomy-and-gate-liveness.md |
| 54 | `2026-08-17-technical-batch-7a-lane-c-contract.md` | A | C2 | no reference outside docs/audits/ |
| 55 | `2026-08-17-technical-batch-7a-lane-b-contract.md` | P | C2 | live row #546,#547,#552 |
| 56 | `2026-08-15-codex-o-review.md` | P | C1d | L17:REJECTED |
| 57 | `2026-08-13-technical-w4b-conversions-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 58 | `2026-08-13-technical-w4a-conversions-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 59 | `2026-08-13-technical-batch-4-w4d-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 60 | `2026-08-13-technical-batch-4-w4c-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 61 | `2026-08-13-technical-batch-4-w3-lane-contract.md` | A | C2 | no reference outside docs/audits/ |
| 62 | `2026-08-13-technical-524-check-extensions-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 63 | `2026-08-13-technical-492-corpus-reconciliation-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 64 | `2026-08-11-technical-batch-4-w521-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 65 | `2026-08-11-technical-batch-4-w5-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 66 | `2026-08-11-technical-batch-4-w2-lane-contract.md` | S | C2 | only CLOSED row #270 |
| 67 | `2026-08-11-technical-batch-4-w1-lane-contract.md` | A | C2 | JOURNAL/handoff mention only |
| 68 | `2026-08-09-codex-arc1-doc-defects-retro.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 69 | `2026-08-08-conformance-nightly-digest.md` | P·pre | C1d | L17:REJECTED |
| 70 | `2026-08-08-codex-lane-290-floor-teeth.md` | A·pre | C1 | no reference outside docs/audits/ |
| 71 | `2026-08-07-codex-pre-cut-retro-batch2-consolidation.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 72 | `2026-08-05-codex-498-hook-exec-bit.md` | S·pre | C1 | only CLOSED row #498 |
| 73 | `2026-08-04-codex-483-preflight-contract.md` | A·pre | C2 | no reference outside docs/audits/ |
| 74 | `2026-07-31-technical-v6-frozen-contract.md` | A·pre | C2 | JOURNAL/handoff mention only |
| 75 | `2026-07-11-census-consolidated-morning-brief.md` | P·pre | C2 | live row #308 |
| 76 | `2026-04-21-council-27-brief.md` | P·pre | C2 | ADR-27-scope-tagging |

#### UNSURE — 387

Each row names the two candidate classifications and the fork it belongs to (§7). **Not rounded up to a verdict.**

**REJECT vs INTAKE — 253**

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-23-technical-window-seal.md` | A | C1 | JOURNAL/handoff mention only |
| 2 | `2026-08-23-technical-phase0-preconditions.md` | A | C1 | JOURNAL/handoff mention only |
| 3 | `2026-08-23-technical-lane-docs-governance.md` | A | C1 | JOURNAL/handoff mention only |
| 4 | `2026-08-22-technical-cloud-3-566-axis-lean.md` | A | C1 | no reference outside docs/audits/ |
| 5 | `2026-08-22-technical-cloud-1-562-admission-rerun.md` | A | C1 | no reference outside docs/audits/ |
| 6 | `2026-08-21-technical-north-star-position.md` | A | C1 | JOURNAL/handoff mention only |
| 7 | `2026-08-21-technical-lane-arch-lifecycle-archival.md` | A | C1 | JOURNAL/handoff mention only |
| 8 | `2026-08-21-technical-lane-554-cloud-provisioning.md` | A | C1 | no reference outside docs/audits/ |
| 9 | `2026-08-21-fresh-eyes-cloud-r3-conformance.md` | A | C1 | no reference outside docs/audits/ |
| 10 | `2026-08-21-fresh-eyes-cloud-r1-governance-drift.md` | A | C1 | no reference outside docs/audits/ |
| 11 | `2026-08-20-technical-gemini-ab-results-slot1.md` | A | C1 | JOURNAL/handoff mention only |
| 12 | `2026-08-19-technical-s1-seat-arc-packet.md` | A | C1 | JOURNAL/handoff mention only |
| 13 | `2026-08-19-technical-n2-seam-worksheet.md` | A | C1 | no reference outside docs/audits/ |
| 14 | `2026-08-19-technical-n1-529-530-wiring-spec.md` | A | C1 | no reference outside docs/audits/ |
| 15 | `2026-08-19-technical-l2-wiring-lane-packet.md` | A | C1 | JOURNAL/handoff mention only |
| 16 | `2026-08-19-technical-c6-telemetry-readpath.md` | A | C1 | no reference outside docs/audits/ |
| 17 | `2026-08-19-technical-c3-grooming-wave2.md` | A | C1 | no reference outside docs/audits/ |
| 18 | `2026-08-19-technical-c2-review-profiles.md` | A | C1 | no reference outside docs/audits/ |
| 19 | `2026-08-19-technical-c-lanes-consolidated.md` | A | C1 | JOURNAL/handoff mention only |
| 20 | `2026-08-18-technical-533-leg2-measurements.md` | A | C1 | no reference outside docs/audits/ |
| 21 | `2026-08-18-technical-502-mutmut-attribution.md` | A | C1 | no reference outside docs/audits/ |
| 22 | `2026-08-18-codex-review-batch1-a.md` | A | C1 | no reference outside docs/audits/ |
| 23 | `2026-08-18-census-p10-grooming-evidence.md` | A | C1 | no reference outside docs/audits/ |
| 24 | `2026-08-18-census-adoption-preflight.md` | A | C1 | no reference outside docs/audits/ |
| 25 | `2026-08-17-technical-nb7-lifecycle-instrument-verdict.md` | A | C1 | JOURNAL/handoff mention only |
| 26 | `2026-08-17-technical-batch-7a-packet.md` | A | C1 | JOURNAL/handoff mention only |
| 27 | `2026-08-17-census-north-star-inventory.md` | A | C1 | JOURNAL/handoff mention only |
| 28 | `2026-08-11-verification-batch-4-challenge-answer.md` | A | C1 | JOURNAL/handoff mention only |
| 29 | `2026-08-10-verification-ruled-dispositions-and-digest-gap.md` | A | C1 | JOURNAL/handoff mention only |
| 30 | `2026-08-10-technical-satisfied-row-census.md` | A | C1 | no reference outside docs/audits/ |
| 31 | `2026-08-10-technical-research-ingest-reconcile-and-packet.md` | A | C1 | JOURNAL/handoff mention only |
| 32 | `2026-08-10-technical-night-n3-ratification-pack.md` | A | C1 | JOURNAL/handoff mention only |
| 33 | `2026-08-10-technical-night-n1-window-synthesis.md` | A | C1 | JOURNAL/handoff mention only |
| 34 | `2026-08-10-technical-batch-night-cloud-packet.md` | A | C1 | JOURNAL/handoff mention only |
| 35 | `2026-08-10-technical-batch-night-cloud-manifest.md` | A | C1 | JOURNAL/handoff mention only |
| 36 | `2026-08-10-technical-batch-4-prep-evidence.md` | A | C1 | JOURNAL/handoff mention only |
| 37 | `2026-08-10-census-conformance-digest-content.md` | A | C1 | JOURNAL/handoff mention only |
| 38 | `2026-08-09-technical-night-n5-library-first-sweep.md` | A·pre | C1 | no reference outside docs/audits/ |
| 39 | `2026-08-09-technical-night-batch-findings-index.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 40 | `2026-08-09-technical-n4-code-review.md` | A·pre | C1 | no reference outside docs/audits/ |
| 41 | `2026-08-09-technical-n1-position-northstar.md` | A·pre | C1 | no reference outside docs/audits/ |
| 42 | `2026-08-09-technical-decision-sheet.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 43 | `2026-08-09-technical-challenge-retrieval.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 44 | `2026-08-09-technical-batch-night-packet.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 45 | `2026-08-09-technical-batch-night-manifest.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 46 | `2026-08-09-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 47 | `2026-08-08-technical-handoff-cut-staging.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 48 | `2026-08-08-technical-batch-3-manifest.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 49 | `2026-08-08-technical-batch-3-consolidation-report.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 50 | `2026-08-08-technical-archival-lifecycle-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 51 | `2026-08-08-technical-506-open-set-grooming-sheet.md` | A·pre | C1 | no reference outside docs/audits/ |
| 52 | `2026-08-08-codex-batch-3-integrator-arc.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 53 | `2026-08-07-technical-handoff-engine-thinning.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 54 | `2026-08-07-technical-fleet-backup-posture.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 55 | `2026-08-07-technical-batch-2-manifest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 56 | `2026-08-06-verification-lane-c-arch-327.md` | N·pre | C1 | L17 §4 follow-on list |
| 57 | `2026-08-06-technical-night-window-review.md` | A·pre | C1 | no reference outside docs/audits/ |
| 58 | `2026-08-06-technical-night-morning-packet.md` | N·pre | C1 | L17 §4 follow-on list |
| 59 | `2026-08-06-technical-night-library-research.md` | A·pre | C1 | no reference outside docs/audits/ |
| 60 | `2026-08-06-technical-lane-a-architecture-rows.md` | N·pre | C1 | L17 §4 follow-on list |
| 61 | `2026-08-06-technical-batch-1-integration-packet.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 62 | `2026-08-05-conformance-nightly-digest.md` | N·pre | C1 | L17 §4 follow-on list |
| 63 | `2026-08-04-technical-closure-proposal-ranked-sheet.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 64 | `2026-08-04-technical-480-ruling-input-pack.md` | A·pre | C1 | no reference outside docs/audits/ |
| 65 | `2026-08-04-conformance-nightly-digest.md` | N·pre | C1 | L17 §4 follow-on list |
| 66 | `2026-08-03-technical-night-le-library-first.md` | A·pre | C1 | no reference outside docs/audits/ |
| 67 | `2026-08-03-technical-night-ld-472-option-b.md` | A·pre | C1 | no reference outside docs/audits/ |
| 68 | `2026-08-03-technical-night-lc-w4-staging.md` | A·pre | C1 | no reference outside docs/audits/ |
| 69 | `2026-08-03-technical-night-batch-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 70 | `2026-08-03-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 71 | `2026-08-02-technical-night-ladder-and-plan-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 72 | `2026-08-02-technical-night-batch-lf-backlog-health.md` | A·pre | C1 | no reference outside docs/audits/ |
| 73 | `2026-08-02-technical-night-batch-le-library-first.md` | A·pre | C1 | no reference outside docs/audits/ |
| 74 | `2026-08-02-technical-night-batch-ld-currency-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 75 | `2026-08-02-technical-night-batch-lc-agents-md-analysis.md` | A·pre | C1 | no reference outside docs/audits/ |
| 76 | `2026-08-02-conformance-nightly-digest.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 77 | `2026-08-01-technical-night-batch-plan-prep.md` | N·pre | C1 | L17 §4 follow-on list |
| 78 | `2026-08-01-technical-night-batch-l7-wave2-pre-analysis.md` | A·pre | C1 | no reference outside docs/audits/ |
| 79 | `2026-08-01-technical-night-batch-l6-460-decision-pack.md` | A·pre | C1 | no reference outside docs/audits/ |
| 80 | `2026-08-01-technical-night-batch-l5-delta-groom.md` | A·pre | C1 | no reference outside docs/audits/ |
| 81 | `2026-08-01-technical-night-batch-l3-copier-record.md` | A·pre | C1 | no reference outside docs/audits/ |
| 82 | `2026-08-01-technical-night-batch-l1-filing-pre-pack.md` | A·pre | C1 | no reference outside docs/audits/ |
| 83 | `2026-08-01-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 84 | `2026-07-31-verification-first-live-v6-boot-report.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 85 | `2026-07-31-technical-intake22-d-research-rows.md` | A·pre | C1 | no reference outside docs/audits/ |
| 86 | `2026-07-31-technical-intake-split-generality-discharge.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 87 | `2026-07-31-technical-closure-ids-negation-defect.md` | N·pre | C1 | L17 §4 follow-on list |
| 88 | `2026-07-31-technical-433-spike-prep.md` | N·pre | C1 | L17 §4 follow-on list |
| 89 | `2026-07-31-technical-382-w2-grok-shadow-ab.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 90 | `2026-07-31-technical-382-arc-educate.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 91 | `2026-07-31-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 92 | `2026-07-31-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 93 | `2026-07-30-technical-v6-open-questions-ruling-dossier.md` | A·pre | C1 | no reference outside docs/audits/ |
| 94 | `2026-07-30-technical-proposals-2026-07-29-triage.md` | A·pre | C1 | no reference outside docs/audits/ |
| 95 | `2026-07-30-qa-assemble-paste-test-gap-review.md` | A·pre | C1 | no reference outside docs/audits/ |
| 96 | `2026-07-30-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 97 | `2026-07-30-census-fleet-state-boot-prep.md` | A·pre | C1 | no reference outside docs/audits/ |
| 98 | `2026-07-29-technical-vscode-w1-visibility-ruling.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 99 | `2026-07-29-technical-postflip-stale-procedure-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 100 | `2026-07-29-technical-intake18-ratification-dossier.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 101 | `2026-07-29-conformance-nightly-digest.md` | N·pre | C1 | L17 §4 follow-on list |
| 102 | `2026-07-28-technical-vscode-sizing-decision-surface.md` | A·pre | C1 | no reference outside docs/audits/ |
| 103 | `2026-07-28-technical-drain-slice-prep.md` | A·pre | C1 | no reference outside docs/audits/ |
| 104 | `2026-07-28-technical-d-queue-0826.md` | A·pre | C1 | no reference outside docs/audits/ |
| 105 | `2026-07-28-technical-437-closure-token-design.md` | A·pre | C1 | no reference outside docs/audits/ |
| 106 | `2026-07-28-technical-364-cap-option-matrix.md` | N·pre | C1 | L17 §4 follow-on list |
| 107 | `2026-07-28-codex-p6-prep-review.md` | A·pre | C1 | no reference outside docs/audits/ |
| 108 | `2026-07-27-verification-conformance-extraction-aggregate.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 109 | `2026-07-21-technical-night-code-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 110 | `2026-07-21-technical-night-backlog-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 111 | `2026-07-19-verification-night-e1-probe-fire-evidence.md` | N·pre | C1 | L17 §4 follow-on list |
| 112 | `2026-07-19-technical-night-s9-testing-harness-agentic.md` | N·pre | C1 | L17 §4 follow-on list |
| 113 | `2026-07-19-technical-night-s8-fleet-state-management.md` | N·pre | C1 | L17 §4 follow-on list |
| 114 | `2026-07-19-technical-night-s6-worktree-discipline.md` | N·pre | C1 | L17 §4 follow-on list |
| 115 | `2026-07-19-technical-night-s5-consumer-disk-info-audit.md` | N·pre | C1 | L17 §4 follow-on list |
| 116 | `2026-07-19-technical-night-s3-archives-lifecycle-records.md` | N·pre | C1 | L17 §4 follow-on list |
| 117 | `2026-07-19-technical-night-s2-backlog-decision-ops.md` | N·pre | C1 | L17 §4 follow-on list |
| 118 | `2026-07-19-technical-night-s1-intake-adr-lifecycle.md` | N·pre | C1 | L17 §4 follow-on list |
| 119 | `2026-07-19-technical-night-luna-carrier-inventory.md` | N·pre | C1 | L17 §4 follow-on list |
| 120 | `2026-07-19-technical-arc5-educate.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 121 | `2026-07-19-codex-cycle-close-sol-adversarial-diff.md` | A·pre | C1 | no reference outside docs/audits/ |
| 122 | `2026-07-18-technical-arc4-leg1-ruff-equalization.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 123 | `2026-07-17-technical-night-verdict-sheet.md` | A·pre | C1 | no reference outside docs/audits/ |
| 124 | `2026-07-17-technical-night-live-fire-sheet.md` | A·pre | C1 | no reference outside docs/audits/ |
| 125 | `2026-07-17-technical-night-handoff-evidence-pack.md` | A·pre | C1 | no reference outside docs/audits/ |
| 126 | `2026-07-17-technical-night-divergence-ledger.md` | A·pre | C1 | no reference outside docs/audits/ |
| 127 | `2026-07-13-technical-content-parity-inventory.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 128 | `2026-07-13-technical-a0-traceability-closure.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 129 | `2026-07-12-technical-night-verdict-sheet.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 130 | `2026-07-12-technical-night-rollout-corp-monorepo.md` | A·pre | C1 | no reference outside docs/audits/ |
| 131 | `2026-07-12-technical-night-rollout-ai-council.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 132 | `2026-07-12-technical-night-plan-continuity-proposal.md` | A·pre | C1 | no reference outside docs/audits/ |
| 133 | `2026-07-12-technical-night-e2e-evidence.md` | A·pre | C1 | no reference outside docs/audits/ |
| 134 | `2026-07-11-technical-audit-corpus-verb-list.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 135 | `2026-07-11-changelog-review-codex-cc.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 136 | `2026-07-09-night-verification-report.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 137 | `2026-07-08-qa-role-incident-evidence.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 138 | `2026-07-08-grooming-worksheet.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 139 | `2026-07-08-demo-prep-global-infra-incident.md` | A·pre | C1 | no reference outside docs/audits/ |
| 140 | `2026-07-07-stage3-adjudication-memo.md` | A·pre | C1 | no reference outside docs/audits/ |
| 141 | `2026-07-07-ai-council-measurement-4.md` | A·pre | C1 | no reference outside docs/audits/ |
| 142 | `2026-07-05-overnight-autonomy-run.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 143 | `2026-07-05-draft-tier3-claudemd-generability.md` | A·pre | C1 | no reference outside docs/audits/ |
| 144 | `2026-07-05-audit-vs-reality.md` | A·pre | C1 | no reference outside docs/audits/ |
| 145 | `2026-07-04-rot-algorithm-design.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 146 | `2026-07-04-handoff-adoption-review.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 147 | `2026-07-04-coherence-spine-review.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 148 | `2026-07-02-comprehensive-system-audit-for-external-review.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 149 | `2026-06-26-playbook-condensation-rule-inventory.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 150 | `2026-06-26-corpus-graph-justify-or-retire.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 151 | `2026-06-25-process-trigger-usage-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 152 | `2026-06-25-dependency-architecture-coverage-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 153 | `2026-06-23-playbook-fidelity-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 154 | `2026-06-23-canonical-corpus-coherence-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 155 | `2026-06-23-architecture-fidelity-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 156 | `2026-06-21-audit-technical-findings.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 157 | `2026-06-21-audit-process-findings.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 158 | `2026-06-19-playbook-essentials-currency-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 159 | `2026-06-19-consolidation-state-report.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 160 | `2026-06-14-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 161 | `2026-06-13-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 162 | `2026-06-13-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 163 | `2026-06-12-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 164 | `2026-06-12-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 165 | `2026-06-11-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 166 | `2026-06-11-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 167 | `2026-06-10-fleet-handoff-readiness.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 168 | `2026-06-10-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 169 | `2026-06-10-consolidation-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 170 | `2026-06-10-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 171 | `2026-06-09-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 172 | `2026-06-09-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 173 | `2026-06-08-floor-repilot-corp-sca-validation.md` | A·pre | C1 | no reference outside docs/audits/ |
| 174 | `2026-06-08-floor-pilot-corp-sca-validation.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 175 | `2026-06-08-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 176 | `2026-06-08-corp-sca-time-automation-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 177 | `2026-06-07-wave-a-validation.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 178 | `2026-06-07-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 179 | `2026-06-07-codex-max-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 180 | `2026-06-07-changelog-review.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 181 | `2026-06-06-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 182 | `2026-06-06-corp-monorepo-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 183 | `2026-06-05-machinery-inventory.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 184 | `2026-06-05-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 185 | `2026-06-04-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 186 | `2026-06-04-conformance-rerun-delta-digest.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 187 | `2026-06-04-conformance-nightly-digest.md` | A·pre | C1 | no reference outside docs/audits/ |
| 188 | `2026-06-03-phase0-workflow-gates-findings.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 189 | `2026-06-03-ecosystem-audit.md` | A·pre | C1 | no reference outside docs/audits/ |
| 190 | `2026-06-02-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 191 | `2026-06-01-fresh-eyes-story-map.md` | A·pre | C1 | no reference outside docs/audits/ |
| 192 | `2026-06-01-fresh-eyes-sacred-files-cadence.md` | A·pre | C1 | no reference outside docs/audits/ |
| 193 | `2026-06-01-fresh-eyes-precommit-enforcement-gate.md` | A·pre | C1 | no reference outside docs/audits/ |
| 194 | `2026-06-01-fresh-eyes-backlog-migration.md` | A·pre | C1 | no reference outside docs/audits/ |
| 195 | `2026-06-01-child-repo-relocation-proposal.md` | W·pre | C1 | BACKLOG.md prose only |
| 196 | `2026-06-01-backlog-commit-naming-retro.md` | A·pre | C1 | no reference outside docs/audits/ |
| 197 | `2026-05-31-methodology-canonical-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 198 | `2026-05-31-backlog-reconciliation-classification.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 199 | `2026-05-29-overnight-morning-briefing.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 200 | `2026-05-29-harness-engineering-positioning.md` | A·pre | C1 | no reference outside docs/audits/ |
| 201 | `2026-05-29-handoff-v3.4-fix-campaign-verification.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 202 | `2026-05-28-universalization-durability-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 203 | `2026-05-28-mermaid-readability-v2-verification.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 204 | `2026-05-28-mermaid-dark-theme-verification.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 205 | `2026-05-28-final-state-and-process-diagrams-verification.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 206 | `2026-05-27-cross-repo-retrofit-verification.md` | A·pre | C1 | no reference outside docs/audits/ |
| 207 | `2026-05-27-corp-sca-time-automation-visual-pattern-retrofit-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 208 | `2026-05-27-corp-ops-visual-pattern-retrofit-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 209 | `2026-05-27-corp-monorepo-visual-pattern-retrofit-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 210 | `2026-05-27-ai-council-visual-pattern-retrofit-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 211 | `2026-05-26-handoff-stabilization-validation-report.md` | A·pre | C1 | no reference outside docs/audits/ |
| 212 | `2026-05-26-handoff-stabilization-discovery.md` | A·pre | C1 | no reference outside docs/audits/ |
| 213 | `2026-05-26-cross-repo-universalization-synthesis.md` | A·pre | C1 | no reference outside docs/audits/ |
| 214 | `2026-05-26-cross-repo-audit-discovery.md` | A·pre | C1 | no reference outside docs/audits/ |
| 215 | `2026-05-26-corp-sca-time-automation-execution-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 216 | `2026-05-26-corp-sca-time-automation-audit-refresh.md` | A·pre | C1 | no reference outside docs/audits/ |
| 217 | `2026-05-26-corp-ops-execution-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 218 | `2026-05-26-corp-ops-audit-refresh.md` | A·pre | C1 | no reference outside docs/audits/ |
| 219 | `2026-05-26-corp-monorepo-execution-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 220 | `2026-05-26-corp-monorepo-audit-refresh.md` | A·pre | C1 | no reference outside docs/audits/ |
| 221 | `2026-05-26-ai-council-audit-status-reference.md` | A·pre | C1 | no reference outside docs/audits/ |
| 222 | `2026-05-25-council-pipeline-index.md` | A·pre | C1 | no reference outside docs/audits/ |
| 223 | `2026-05-25-council-pipeline-discovery.md` | A·pre | C1 | no reference outside docs/audits/ |
| 224 | `2026-05-25-council-mechanism-discovery.md` | A·pre | C1 | no reference outside docs/audits/ |
| 225 | `2026-05-25-council-debate-forensics.md` | A·pre | C1 | no reference outside docs/audits/ |
| 226 | `2026-05-25-ai-council-universalization-execution-plan.md` | A·pre | C1 | no reference outside docs/audits/ |
| 227 | `2026-05-25-ai-council-universalization-audit-refresh.md` | A·pre | C1 | no reference outside docs/audits/ |
| 228 | `2026-05-24-dev-knowledge-self-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 229 | `2026-05-23-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 230 | `2026-05-23-corp-monorepo-deep-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 231 | `2026-05-23-.dev-knowledge-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 232 | `2026-05-20-posture-audit-verification.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 233 | `2026-05-19-rollout-readiness.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 234 | `2026-05-19-corp-monorepo-architecture-inspection.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 235 | `2026-05-17-skills-hooks-usage-review.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 236 | `2026-05-17-corp-monorepo-governance-rollout-plan.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 237 | `2026-05-16-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 238 | `2026-05-15-ecosystem-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 239 | `2026-05-12-hooks-discovery.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 240 | `2026-05-12-hooks-discovery-resolution.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 241 | `2026-04-30-ai-council-rediscovery.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 242 | `2026-04-30-ai-council-discovery.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 243 | `2026-04-30-ai-council-audit-report.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 244 | `2026-04-27-pre-debate-audit-cross-repo-and-handoff.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 245 | `2026-04-27-numbers-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 246 | `2026-04-27-deep-cleansing-diagnostic.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 247 | `2026-04-25-claude-code-features-inventory.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 248 | `2026-04-24-stream-b-gaps-mapping.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 249 | `2026-04-24-stream-a-gap-report.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 250 | `2026-04-24-playbook-tagging-sanity-check.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 251 | `2026-04-24-council-28-29-consolidated-actions.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 252 | `2026-04-21-corp-monorepo-operating-model-analysis.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 253 | `2026-03-30-dev-practice-os-state-audit.md` | A·pre | C1 | JOURNAL/handoff mention only |

**MECHANICAL vs REJECT — 108**

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-22-codex-562-guard-fix-terra.md` | A | C1 | no reference outside docs/audits/ |
| 2 | `2026-08-22-codex-562-guard-fix-terra-r9.md` | A | C1 | no reference outside docs/audits/ |
| 3 | `2026-08-22-codex-562-guard-fix-terra-r8.md` | A | C1 | no reference outside docs/audits/ |
| 4 | `2026-08-22-codex-562-guard-fix-terra-r7.md` | A | C1 | no reference outside docs/audits/ |
| 5 | `2026-08-22-codex-562-guard-fix-terra-r6.md` | A | C1 | no reference outside docs/audits/ |
| 6 | `2026-08-22-codex-562-guard-fix-terra-r5.md` | A | C1 | no reference outside docs/audits/ |
| 7 | `2026-08-22-codex-562-guard-fix-terra-r4.md` | A | C1 | no reference outside docs/audits/ |
| 8 | `2026-08-22-codex-562-guard-fix-terra-r3.md` | A | C1 | no reference outside docs/audits/ |
| 9 | `2026-08-22-codex-562-guard-fix-terra-r2.md` | A | C1 | no reference outside docs/audits/ |
| 10 | `2026-08-22-codex-562-guard-fix-terra-r11.md` | A | C1 | no reference outside docs/audits/ |
| 11 | `2026-08-22-codex-562-guard-fix-terra-r10.md` | A | C1 | no reference outside docs/audits/ |
| 12 | `2026-08-18-codex-review-batch1-c-e.md` | A | C1 | no reference outside docs/audits/ |
| 13 | `2026-08-12-codex-closing-arc-organ-index-guard.md` | A | C1 | JOURNAL/handoff mention only |
| 14 | `2026-08-11-codex-batch4-w5-organ-index.md` | A | C1 | no reference outside docs/audits/ |
| 15 | `2026-08-11-codex-batch4-w1-lane-regex.md` | A | C1 | JOURNAL/handoff mention only |
| 16 | `2026-08-11-codex-arc9-absorb-m6-gen-audit-index.md` | A | C1 | JOURNAL/handoff mention only |
| 17 | `2026-08-09-technical-night-n2-mechanism-map.md` | A·pre | C1 | no reference outside docs/audits/ |
| 18 | `2026-08-09-codex-batch-3-integrator-arc.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 19 | `2026-08-07-codex-lane-2-worktree-portability.md` | A·pre | C1 | no reference outside docs/audits/ |
| 20 | `2026-08-06-codex-batch-protocol.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 21 | `2026-08-05-codex-480-review-artifact-organ.md` | N·pre | C1 | L17 §4 follow-on list |
| 22 | `2026-08-04-codex-483-terra-round2.md` | N·pre | C1 | L17 §4 follow-on list |
| 23 | `2026-08-04-codex-482-glob-engine-true-glob.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 24 | `2026-08-04-codex-465-terra-round2.md` | N·pre | C1 | L17 §4 follow-on list |
| 25 | `2026-08-04-codex-465-leg4-inert-check-detector.md` | N·pre | C1 | L17 §4 follow-on list |
| 26 | `2026-08-03-codex-arc3-terra-round2.md` | N·pre | C1 | L17 §4 follow-on list |
| 27 | `2026-08-03-codex-arc3-mechanical-adoptions.md` | A·pre | C1 | no reference outside docs/audits/ |
| 28 | `2026-08-03-codex-arc2-vacuous-green-trio.md` | N·pre | C1 | L17 §4 follow-on list |
| 29 | `2026-08-03-codex-arc2-terra-round2.md` | N·pre | C1 | L17 §4 follow-on list |
| 30 | `2026-08-03-codex-adr85-integration-enforcement.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 31 | `2026-08-03-codex-475-seal-identity-precommit-gate-retro.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 32 | `2026-08-03-codex-474-gen-task-tree-write-guard-retro.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 33 | `2026-08-03-codex-472-terra-round2.md` | N·pre | C1 | L17 §4 follow-on list |
| 34 | `2026-08-03-codex-472-declaration-anchor.md` | N·pre | C1 | L17 §4 follow-on list |
| 35 | `2026-08-01-codex-generator-newlines-and-groom.md` | A·pre | C1 | no reference outside docs/audits/ |
| 36 | `2026-08-01-codex-462-membership-agreement-census.md` | A·pre | C1 | no reference outside docs/audits/ |
| 37 | `2026-08-01-codex-460-replication-and-close.md` | A·pre | C1 | no reference outside docs/audits/ |
| 38 | `2026-07-31-codex-intake-split-generality-discharge.md` | N·pre | C1 | L17 §4 follow-on list |
| 39 | `2026-07-30-codex-446-v6-boot-prose.md` | N·pre | C1 | L17 §4 follow-on list |
| 40 | `2026-07-30-codex-446-v6-boot-build.md` | A·pre | C1 | no reference outside docs/audits/ |
| 41 | `2026-07-28-codex-444-release-0-1-11.md` | A·pre | C1 | no reference outside docs/audits/ |
| 42 | `2026-07-28-codex-437-closure-diff.md` | A·pre | C1 | no reference outside docs/audits/ |
| 43 | `2026-07-28-codex-437-closure-design.md` | A·pre | C1 | no reference outside docs/audits/ |
| 44 | `2026-07-27-codex-lane-filings-uv-bakeoff-extraction.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 45 | `2026-07-27-codex-handoff-v6-pack.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 46 | `2026-07-27-codex-conformance-extraction-aggregate.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 47 | `2026-07-27-codex-436-silent-rule-ratchet.md` | N·pre | C1 | L17 §4 follow-on list |
| 48 | `2026-07-27-codex-436-ratchet-recheck.md` | N·pre | C1 | L17 §4 follow-on list |
| 49 | `2026-07-27-codex-436-ratchet-gate9.md` | N·pre | C1 | L17 §4 follow-on list |
| 50 | `2026-07-27-codex-436-ratchet-gate8.md` | N·pre | C1 | L17 §4 follow-on list |
| 51 | `2026-07-27-codex-436-ratchet-gate7.md` | N·pre | C1 | L17 §4 follow-on list |
| 52 | `2026-07-27-codex-436-ratchet-gate6.md` | N·pre | C1 | L17 §4 follow-on list |
| 53 | `2026-07-27-codex-436-ratchet-gate5.md` | N·pre | C1 | L17 §4 follow-on list |
| 54 | `2026-07-27-codex-436-ratchet-gate10.md` | N·pre | C1 | L17 §4 follow-on list |
| 55 | `2026-07-27-codex-436-ratchet-clear.md` | N·pre | C1 | L17 §4 follow-on list |
| 56 | `2026-07-26-codex-routine-consumers-check.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 57 | `2026-07-26-codex-routine-consumer-prose.md` | N·pre | C1 | L17 §4 follow-on list |
| 58 | `2026-07-25-codex-vision-reread.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 59 | `2026-07-25-codex-vision-reread-recheck.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 60 | `2026-07-25-codex-lane-d-rulings.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 61 | `2026-07-25-codex-fix-live-backlog-test.md` | N·pre | C1 | L17 §4 follow-on list |
| 62 | `2026-07-20-codex-leg2-handoff-bundle-selection.md` | N·pre | C1 | L17 §4 follow-on list |
| 63 | `2026-07-20-codex-leg1-fleet-parity-gitdir-scrub.md` | N·pre | C1 | L17 §4 follow-on list |
| 64 | `2026-07-19-codex-canon-inoculation.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 65 | `2026-07-18-codex-ruling-w-adr-amendment.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 66 | `2026-07-18-codex-ruling-w-adr-amendment-v2.md` | N·pre | C1 | L17 §4 follow-on list |
| 67 | `2026-07-18-codex-adr-101-two-tier-new-path.md` | N·pre | C1 | L17 §4 follow-on list |
| 68 | `2026-07-18-codex-adr-101-two-tier-new-path-v5.md` | N·pre | C1 | L17 §4 follow-on list |
| 69 | `2026-07-18-codex-adr-101-two-tier-new-path-v4.md` | N·pre | C1 | L17 §4 follow-on list |
| 70 | `2026-07-18-codex-adr-101-two-tier-new-path-v3.md` | N·pre | C1 | L17 §4 follow-on list |
| 71 | `2026-07-18-codex-adr-101-two-tier-new-path-v2.md` | N·pre | C1 | L17 §4 follow-on list |
| 72 | `2026-07-17-codex-role-governance.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 73 | `2026-07-17-codex-gate-rev-axis.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 74 | `2026-07-17-codex-arc3-ownership-axis.md` | A·pre | C1 | no reference outside docs/audits/ |
| 75 | `2026-07-17-codex-adr29-legacy-split-amendment.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 76 | `2026-07-16-codex-tail-firstread-lessons.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 77 | `2026-07-06-codex-g7-mirror.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 78 | `2026-07-06-codex-consumer-instrument-hardening.md` | A·pre | C1 | no reference outside docs/audits/ |
| 79 | `2026-07-05-codex-slice-b-fix-batch.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 80 | `2026-07-05-codex-consumer-arc.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 81 | `2026-06-17-codex-coherence-integration.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 82 | `2026-06-14-codex-q9-automation-isolation.md` | A·pre | C1 | no reference outside docs/audits/ |
| 83 | `2026-06-13-codex-163-probe-validator.md` | A·pre | C1 | no reference outside docs/audits/ |
| 84 | `2026-06-13-codex-163-basename-fallback.md` | A·pre | C1 | no reference outside docs/audits/ |
| 85 | `2026-06-13-codex-156-taskgraph.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 86 | `2026-06-10-codex-amendment-gate-11.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 87 | `2026-06-10-codex-147-ship-gate.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 88 | `2026-06-09-codex-prose-state-checker-89.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 89 | `2026-06-06-codex-immutability-guard.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 90 | `2026-06-06-codex-85-fleet-scheduler.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 91 | `2026-06-03-codex-tier1-precommit-stage-fix.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 92 | `2026-06-03-codex-dynamic-toc.md` | A·pre | C1 | no reference outside docs/audits/ |
| 93 | `2026-06-03-codex-doctools-hook-repo.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 94 | `2026-06-03-codex-audit-self-documenting.md` | A·pre | C1 | no reference outside docs/audits/ |
| 95 | `2026-06-02-codex-pytest-ini-exception.md` | A·pre | C1 | no reference outside docs/audits/ |
| 96 | `2026-06-02-codex-no-leftovers-detector.md` | A·pre | C1 | no reference outside docs/audits/ |
| 97 | `2026-06-02-codex-canonical-standard-lock.md` | A·pre | C1 | no reference outside docs/audits/ |
| 98 | `2026-06-01-codex-sacred-files-cadence-check10.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 99 | `2026-06-01-codex-precommit-enforcement-gate.md` | A·pre | C1 | no reference outside docs/audits/ |
| 100 | `2026-06-01-codex-backlog-story-map.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 101 | `2026-06-01-codex-backlog-migration-adr64.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 102 | `2026-05-23-codex-codemap-mermaid-fence-wrap.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 103 | `2026-05-23-codex-codemap-amendment-and-dogfood.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 104 | `2026-05-22-codex-drift-burndown-2026-05-22.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 105 | `2026-05-22-codex-codemap-generator-tool.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 106 | `2026-05-12-codex-ai-council-handoff-stage3.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 107 | `2026-05-11-codex-prompt-b-docs-alignment.md` | A·pre | C1 | JOURNAL/handoff mention only |
| 108 | `2026-04-26-codex-adr-30-default-branch-main.md` | A·pre | C1 | JOURNAL/handoff mention only |

**COVERED vs REJECT — 11**

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-11-codex-lane-b-270-load-gauge.md` | S | C4 | only CLOSED row #270 |
| 2 | `2026-08-10-technical-batch-4-execution-plan-draft.md` | S | C4 | only CLOSED row #525 |
| 3 | `2026-08-05-technical-night-batch-morning-report.md` | S·pre | C4 | only CLOSED row #489,#498 |
| 4 | `2026-08-03-technical-night-la-w2-verification.md` | S·pre | C4 | only CLOSED row #480 |
| 5 | `2026-08-01-technical-window-metrics.md` | S·pre | C4 | only CLOSED row #461 |
| 6 | `2026-08-01-technical-night-batch-l2-repomix-pilot.md` | S·pre | C4 | only CLOSED row #467 |
| 7 | `2026-08-01-technical-codex-wrapper-model-pin-and-lf.md` | S·pre | C4 | only CLOSED row #469 |
| 8 | `2026-07-12-technical-night-delete-candidates.md` | S·pre | C4 | only CLOSED row #320 |
| 9 | `2026-07-11-technical-fleet-boundary-matrix.md` | S·pre | C4 | only CLOSED row #315 |
| 10 | `2026-07-09-deletion-candidates-report.md` | S·pre | C4 | only CLOSED row #320 |
| 11 | `2026-06-07-copilot-collections-peer-audit-v2.md` | S·pre | C4 | only CLOSED row #132 |

**COVERED vs re-file — 11**

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-16-verification-nb6-backlog-truth.md` | P | C4 | L17:FILED(#534=open,#535=open,#536=closed,#537=open,#533=open,#293=open,#492=deferred,#506=open) |
| 2 | `2026-08-16-verification-nb6-achievements.md` | P | C4 | L17:FILED(#505=closed) |
| 3 | `2026-08-16-verification-nb4-equilibrium.md` | P | C4 | L17:FILED(#539=closed) |
| 4 | `2026-08-16-technical-nb4-telemetry-read.md` | P | C4 | L17:FILED(#529=closed) |
| 5 | `2026-08-15-verification-night3-warn-ledger.md` | P | C4 | L17:FILED(#531=open,#532=closed) |
| 6 | `2026-08-15-technical-530-single-flight-lane-packet.md` | P | C4 | L17:FILED(#530=closed) |
| 7 | `2026-08-15-technical-529-telemetry-emit-lane-packet.md` | P | C4 | L17:FILED(#529=closed) |
| 8 | `2026-08-15-technical-528-legs12-packet.md` | P | C4 | L17:FILED(#528=open,#529=closed) |
| 9 | `2026-08-15-codex-p-review.md` | P | C4 | L17:FILED(#530=closed) |
| 10 | `2026-08-15-codex-m-review.md` | P | C4 | L17:FILED(#529=closed) |
| 11 | `2026-08-07-codex-mutmut-sandbox-skip.md` | P·pre | C4 | L17:FILED(#502=closed) |

**SUPERSEDED has NO funnel term — 2**

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-16-technical-nb4-g-scaleout-substrate.md` | P | M1 | L17:SUPERSEDED |
| 2 | `2026-08-15-technical-293-consumer-runbook-fan-out-lane-packet.md` | P | M1 | L17:SUPERSEDED |

**PENDING has NO funnel term — 2**

| # | file | ◦ | clause | current disposition state / evidence |
|---|---|---|---|---|
| 1 | `2026-08-16-census-nb6-archive-sweep.md` | P | M2 | L17:PENDING |
| 2 | `2026-08-14-qa-night2-quality.md` | P | M2 | L17:PENDING |

---

## 7. The forks — what this lane refuses to decide

Ordered so the whole table can be ruled in one pass: **F1 alone disposes of 318 of the 387 UNSURE
rows.**

### F1 — Does the retro-classification bind the pre-2026-08-10 corpus at all?

**458 files** predate ADR-111's ratification (2026-08-10); **318 of the 387 UNSURE rows are among
them.** The repo already has a precedent for exactly this question and it points one way — C10, the
`review_artifact_coverage` docstring: a retro-reaching leg *"would demand retro-editing precisely
what the ruling forbids touching"*, and C7 makes audits immutable, so a retro-classification can
only ever live in a separate artifact like this one.

- **(a) Class-REJECT the pre-ratification half**, reason recorded once here: *ADR-111 was ruled
  2026-08-10; the repo's own forward-only precedent (C10) plus immutability (C7) mean these
  artifacts cannot carry a disposition in themselves, and re-triaging 458 immutable records
  discharges nothing that is still live.* Cost: any live finding still sitting in a pre-ratification
  audit stays unowned — and §8.2 shows that class is real.
- **(b) Bind the whole corpus.** Cost: 318 files each need a read of their findings; that is the
  work the mandate names, and it is a multi-lane job, not this lane's.
- **(c) Bind a bounded prefix** — e.g. only **2026-08-07 and later**, which is exactly the boundary
  the 2026-08-17 ledger already drew for itself: *"everything dated 2026-08-07 or later is ledgered,
  and the follow-on is 2026-08-06 and older."*

**This lane's recommendation is (c)**, because the boundary already exists in the corpus: the L17
ledger drew it, named the 49 files it left behind, and those 49 are still undispositioned today.

### F2 — Which vocabulary governs, and what happens to SUPERSEDED and PENDING? (M1/M2)

C8 is an architect standing ruling with four terms; C3 is codified doctrine with five. They are not
the same set, and **two C8 terms have no C3 counterpart** (§4.3). Either C3 gains a lawful mapping
for them, or C8 is declared superseded by C3 and the four instances are re-classified. **Do not
leave both live** — that is how a file gets two different dispositions and neither is wrong.

### F3 — Confirm "→ backlog row" means COVERED and never a birth (M3)

C5 forbids finding → row. This lane read the mandate's fourth term as **COVERED only** and proposed
**zero** births. Confirm, or the reading is wrong.

### F4 — Is a file-level rollup a lawful disposition? (M4)

C1/C3's unit is a **finding**; this table's unit is a **file** (§4.4). If the answer is no, this
table is a *coverage map* rather than a funnel, and the funnel work is per-finding inside each file.

### F5 — The 25 closed-row dispositions and the 3 drifted register entries (§8)

Re-disposition against a live row, re-file, or ratify as historical? Reported here, fixed nowhere.

---

## 8. The two known shapes — instances found, nothing fixed

### 8.1 Shape B — a disposition whose `match` embeds a measured value that has since drifted

**6 of the 30** entries in `ecosystem/disposition-register.yaml` embed a measured character count in
`match`; all six are `doc_rot` / `backlog-row-length`. Measured live this session by calling the
repo's own detector (`validate_doc_rot.scan_backlog_accretion` on `BACKLOG.md`, `python3` 3.11.15):

| entry id | `match` value | live value | verdict |
|---|---|---|---|
| `warn-row-length-546-adr60-taxonomy` | `(2227 chars` | 2227 chars | agrees |
| `warn-row-length-547-split-brain-referent` | `(2099 chars` | 2099 chars | agrees |
| `warn-row-length-552-governance-clauses` | `(3576 chars` | 3576 chars | agrees |
| `warn-row-length-533-audit-decomposition` | `(4210 chars` | **2239 chars** | **DRIFTED** — substring no longer matches, so `#533`'s live WARN is now UNDISPOSITIONED |
| `warn-row-length-529-telemetry-emit` | `(2001 chars` | **no live WARN** | **STALE** — row `#529` is closed; nothing to suppress |
| `warn-row-length-530-single-flight` | `(1871 chars` | **no live WARN** | **STALE** — row `#530` is closed; nothing to suppress |

**3 of 6 are dead**, and the mechanism that makes that visible is C9's decoration rule — the entries
decorate `[stale]` rather than blocking, which is correct and is also why they can sit dead
indefinitely. The class defect is that the `match` contract in C9 tells an author to key on *the
specific benign signature*, and a character count **is** a specific signature — it is just a
**volatile** one, unlike the commit sha the contract offers as its example. Independently reproduced;
it agrees with `docs/audits/2026-08-23-technical-phase0-preconditions.md` §3.5, which reached the
same 6-and-3 split by a different route.

### 8.2 Shape A — a disposition whose subject row is closed

Three distinct populations, **25 instances in the corpus + 8 in the register**.

**(i) Register entries whose `ref` cites only CLOSED rows — 8 of 30.** `warn-review-artifact-lane-c-504-no-tally`
(`#504` closed) · `warn-journal-spine-anchored-by-mention` (`#524` closed) · and all six
`warn-row-length-*` (`#532` closed). Note the two readings differ and both matter: for the
row-length six, the *establishing* row `#532` is closed for all six, while the *subject* row named
inside `match` is closed for only two (`#529`, `#530`).

**(ii) 2026-08-17 ledger cells marked FILED whose cited row has since closed — 11.** These are the
exact C4 failure — *"That is how a correctly-filed finding dies quietly"* — and they happened in the
six days since the ledger was written.

| artifact | row cited by the L17 FILED cell, now closed |
|---|---|
| `2026-08-07-codex-mutmut-sandbox-skip.md` | `#502` |
| `2026-08-15-codex-m-review.md` | `#529` |
| `2026-08-15-codex-p-review.md` | `#530` |
| `2026-08-15-technical-528-legs12-packet.md` | `#529` |
| `2026-08-15-technical-529-telemetry-emit-lane-packet.md` | `#529` |
| `2026-08-15-technical-530-single-flight-lane-packet.md` | `#530` |
| `2026-08-15-verification-night3-warn-ledger.md` | `#532` |
| `2026-08-16-technical-nb4-telemetry-read.md` | `#529` |
| `2026-08-16-verification-nb4-equilibrium.md` | `#539` |
| `2026-08-16-verification-nb6-achievements.md` | `#505` |
| `2026-08-16-verification-nb6-backlog-truth.md` | `#536` |

**(iii) Audits whose only carrier anywhere is a closed row — 14** (the `S` rows in §6).

| artifact | closed row |
|---|---|
| `2026-06-07-copilot-collections-peer-audit-v2.md` | `#132` |
| `2026-07-09-deletion-candidates-report.md` | `#320` |
| `2026-07-11-technical-fleet-boundary-matrix.md` | `#315` |
| `2026-07-12-technical-night-delete-candidates.md` | `#320` |
| `2026-08-01-technical-codex-wrapper-model-pin-and-lf.md` | `#469` |
| `2026-08-01-technical-night-batch-l2-repomix-pilot.md` | `#467` |
| `2026-08-01-technical-window-metrics.md` | `#461` |
| `2026-08-03-technical-night-la-w2-verification.md` | `#480` |
| `2026-08-05-codex-498-hook-exec-bit.md` | `#498` |
| `2026-08-05-technical-night-batch-morning-report.md` | `#489`, `#498` |
| `2026-08-10-technical-batch-4-execution-plan-draft.md` | `#525` |
| `2026-08-11-codex-lane-b-270-load-gauge.md` | `#270` |
| `2026-08-11-technical-batch-4-w2-lane-contract.md` | `#270` |
| `2026-08-19-technical-backlogmd-trial.md` | `#563` |

Nothing above was fixed. No register entry was written, no row edited, no artifact amended.

---

## 9. Coverage statement

```
N   files in docs/audits/                             693
X   given ONE proposed classification                 306   (44.2%)
Y   UNSURE — two candidates + the decider named       387   (55.8%)
Z   not reached                                         0
```

**Where the 387 come from, and why each is UNSURE rather than a verdict:**

- **253 — REJECT vs INTAKE.** No carrier anywhere in the tree. Deciding requires reading the
  artifact for a recommendation that never landed. **216 of these are pre-ratification** and fall
  to fork F1; the remaining **37** are post-ratification and are the sharpest debt in the corpus.
- **108 — MECHANICAL vs REJECT** (92 pre-ratification, 16 post). A codex review artifact with a
  non-zero tally, no `**Disposition:**` line and no carrier. Deciding requires checking whether the
  arc it reviewed actually landed its fixes — a per-artifact git question this lane did not run 108
  times.
- **11 — COVERED vs REJECT.** Only a closed row cites it (§8.2 iii).
- **11 — COVERED vs re-file.** An L17 FILED cell whose row has since closed (§8.2 ii).
- **2 + 2 — the M1/M2 vocabulary gaps** (SUPERSEDED, PENDING). Not decidable inside the funnel's
  five terms at all; fork F2.

**Where this lane stopped, stated plainly.** It stopped at the point where a classification would
have required reading an artifact end-to-end. Every file has a **measured** disposition state; only
306 have a **proposed** classification, because only 306 are decided by a predicate over the tree.
Rounding the other 387 up would have produced a complete-looking table whose largest class was
guesswork — and the brief is explicit that a partial table with a stated boundary is worth more.

**What would move the number.** F1(a) converts the **318** pre-ratification UNSURE rows into a
single class ruling. F2 converts 4. The residue is the **69 post-ratification UNSURE rows** —
37 REJECT-vs-INTAKE, 16 MECHANICAL-vs-REJECT, 10 COVERED-vs-re-file, 2 COVERED-vs-REJECT, 4 M1/M2 —
which is one bounded lane, not an open-ended sweep.

---

## 10. What this lane did not do

- **Did not write `ecosystem/disposition-register.yaml`.** Not one byte. §8 reports; it does not fix.
- **Did not touch `scripts/`** — L2 owns the instrument. The scan code for this artifact ran from the
  session scratchpad and is not committed. `scripts/validate_doc_rot.py` was **imported and called**,
  never modified.
- **Did not regenerate `docs/audits/README.md`.** Adding this file makes the generated index stale;
  `audit-index-freshness` (C6) will flag it and the integrator regenerates it once, per the brief.
  Stated rather than left to be discovered.
- **Did not touch `tasks/`, `BACKLOG.md`, or `docs/decisions/`.** No row born, no row edited, no ADR
  drafted.
- **Did not rule.** No classification here is final; §7 lists the five forks this lane declined.
- **Did not run the gate mesh** — it is not runnable in this container (§1), and that is declared
  rather than routed around.
- **Did not self-merge.** Branch `claude/funnel-retro-classification`, commit-and-STOP.
