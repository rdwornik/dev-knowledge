# ARC-2 consolidation — adjudicate, then triage, then land

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** consolidation-report
- **Contract:** `ARC-2-v2-adjudicate-triage-land.md`, plus three architect amendments delivered mid-run
- **Seat:** CC (Opus 5), hub PRIMARY checkout, serial, sole writer to `main`
- **Base:** `df1b05b0` · **Phases:** 0 → A → B → C → D → E → F, each merged through its own integration branch

**Contract-file note, reported not assumed.** `$env:CLAUDE_PROMPTS_DIR` resolves to
`C:\Users\1028120\Downloads`. `ARC-2-v2-adjudicate-triage-land.md` and its predecessor
`ARC-2-triage-and-land.md` are **not present there**; only `ADDENDUM-ARC-2-research-and-pipeline.md`
is. The v2 contract was pasted verbatim into the dispatch, so nothing was reconstructed from a
summary — this is recorded because amendment 2 asks that a resolution failure never be mistaken for
a missing file, and here the resolution succeeded and the files are genuinely absent.

---

## 1. Velocity — the number, and the filter it is measured on

```
Phase A alone :  opened 0 · closed 3 · net -3 · open-total 191
Whole arc     :  opened 3 · closed 3 · net  0 · open-total 194
```

**The filter, named:** `open-total` is `validate_backlog`'s live task count — every row not in a
terminal state, i.e. `status: open` **plus** `status: deferred` (**168 + 26 = 194**). This is the
denominator the closure wave chose and the reason is unchanged: *a deferred row is not a closed
row.* The narrower `status: open` reading is **168**. Both are live; they differ by exactly the
deferred set.

**Said plainly, as the contract requires: the backlog did not shrink this arc.** It began at 194 and
ends at 194. Three closes were real and diff-verified; three births consumed them exactly. Nothing
was closed optimistically to make the number move, and the number did not move.

---

## 2. Phase 0 — the gate restored, by two different routes

| WARN class | n | Route | Why this route |
|---|---|---|---|
| `undeclared_edges → prompt-template` | 8 | **Dispositioned** under ref `#241` | Same reference as the nine `→ handoff-process` rows. D3 not reverted; no `reconciled_with` declared on a doc that merely *mentions* a spec |
| `review_artifact_coverage` on `df1b05b0` | 1 | **Discharged by running the review** | Retroactive review has precedent here; the WARN was cleared by doing the work, not by suppressing it |

**Gate state: RED (9 new/undispositioned) → GREEN (26 dispositioned).**

The reviewer lane ran codex-cli 0.145.0 / `gpt-5.6-terra` pinned / code profile against
`df1b05b0^1..df1b05b0` filtered to `*.py`. **Tally 0/0/0/0**
(`docs/audits/2026-08-09-codex-arc1-doc-defects-retro.md`).

**The zero was refuted before it was accepted.** On a diff whose entire content is a *claim about
other code*, a rubber stamp and a real pass are indistinguishable. The claim: `coherence_nudge`
"silently never fires, since `should_nudge` requires a parsed version on both sides". Had
`_extract_version` returned the spine parser's `""`, then `hv is not None` would be True and
`hv == sv == ""` would fire the nudge on **every** content edit — the exact inverse. It returns
`spec_version_numeric(text) or None`. **Claim holds.**

**Two defect-class recurrences recorded from Phase 0:**

1. **17 live WARNs of one class** (9 + 8, two specs). This is a signal about the *check*: nothing
   distinguishes a doc that **mentions** a spec from one that **depends on** it, so both arrive as
   the same undifferentiated WARN whose only discharge is a hand-written register row.
2. **Exactly one of the eight was not a mention.** `protocols/PLAYBOOK.md` cites
   `templates/prompt-template.md (v1.7)` against a spec now at `Version: 1.13`. The claim that token
   labels is still **true** (the ~10 work-lane ceiling survives verbatim at v1.13) — only the token
   rotted. Eight WARNs looked identical to the scanner; one had rotted. **Deferred, not dismissed**,
   and carried below as triage item **T-D1**.

**A ninth edge was minted by this arc, and rephrasing it away was refused.** Intake #25's
ratification erratum names the template's path; that one accurate sentence created a tier-1 edge.
Dropping the path would have cleared the WARN and kept the meaning — precisely the move the `[#492]`
`doc_rot` entry refused as *"rephrasing … games the detector"*. Dispositioned on its merits instead.
It is the cheapest evidence for finding T-D1: **one true sentence about a spec is, to every organ,
indistinguishable from depending on it.**

---

## 3. Amendment 1 — intake #25 ratified (its own standalone commit, `ef5b6252`)

`DRAFT → ACCEPTED`. A **correction, not a decision**: #25's content was already cited as governing in
three places — the ~10 work-lane ceiling quoted by `templates/prompt-template.md` *and*
`protocols/PLAYBOOK.md`; V-2/V-3 carried by the work-lane card and `/lane-boot`; and six rows in
intake #27 reading `DEFERRED(W-wave batch — after intake #25 acceptance …)`, naming this document's
acceptance as their own trigger. **Un-parks the W-wave and therefore batch 4.**

**Two departures from "status field only", both forced by the flip:**

- **Companion frontmatter added** (`decided-by`, `disposition: active`). README §3 marks both REQUIRED
  at ACCEPTED and all eight prior ACCEPTED intakes carry them — but a bare flip **does parse**
  (`_STATUS_ORDER` accepts it; no validator or test enforces the companions). The schema-invalid
  version would have shipped with nothing saying so. The instruction to *verify the parsers accept
  it* is what caught this — and what it found is that the parser was the wrong thing to trust.
- **Title reconciled.** The H1 read `# INTAKE DRAFT — …` and the generated index renders each H1 under
  its status group, so **ACCEPTED (9)** would have listed an entry whose visible title said DRAFT.
  Repaired in the shape intake #18 set at its own acceptance.

---

## 4. Phase A — the adjudication ledger

### 4.1 The three closes, each re-verified against LIVE HEAD

| id | Done-when | Evidence at HEAD | Verdict |
|---|---|---|---|
| `[#213]` | rule-inventory diff shows zero rules lost AND every inbound pointer resolves | `9ab191f5` body: *"HARD metric met … zero rules lost; every inbound pointer resolves; no renumber"*; artifact `docs/audits/2026-06-26-playbook-condensation-rule-inventory.md` verified present; PLAYBOOK 3410→3386 at the merge | **CLOSE** |
| `[#215]` | one onboard runbook + a conformance verification exist | `protocols/REPO_ONBOARDING.md` carries `## Install sequence (#131)`, `## Conformance verify (#215)`, `## Dry-run attestation (#215 acceptance)`; `tests/test_floor_conformance.py` present | **CLOSE** |
| `[#441]` | PLAYBOOK Ch8 carries the ruling + four-condition test, ADR-61 checks reconciled to one launch test | Ch8 `:1351` launch decision, `:1367` four-condition test, `:1384` "One NO = fat prompt", `:1393` mapping from the superseded three-check test | **CLOSE** |

**Residuals carried deliberately.** `[#215]`'s *body prose* ties the verify half to `[#171]`
(`ecosystem/conformance.md`, which does **not** exist) — that tie is body text, not a Done-when
clause, so closing `[#215]` neither closes nor orphans `[#171]`, and `[#171]` is un-deferred by this
same arc so it is now visibly open. `[#213]`'s "absorbs #214" orphans nothing (#214 already closed).
**PLAYBOOK is 4507 lines today, larger than the 3410 it started at** — recorded so nobody re-opens
`[#213]`: the row states size is *"a byproduct, never a rule cut to hit it"*, and the Done-when is
about rule preservation. The growth is later content.

### 4.2 Both STRONG proposals REFUSED — which is the point of checking them

- **`[#430]` REFUSED.** The one row where the store's STRONG flag is live and **wrong**. `3cf3a5b0`'s
  own body says it closes half (a) and that *"[#430] REMAINS OPEN on half (b)"*. Verified
  independently: `fleet_parity.py`'s module docstring still reads *"reads sibling trees read-only"*,
  so the clause *"(b) a ship-gate verdict is reproducible from the subject repo's own state"* is
  untouched.
- **`[#505]` REFUSED.** The documented false positive — `25ff8ec37`'s subject *"3 rows filed, 0 closed
  [#505]"* trips `CLOSES_RE` while declaring zero closures. Substantively too: N2 states only leg 1
  would land, and D8 shows even leg 1 is unmet.

### 4.3 The 141 WEAK proposals — rejected en bloc, on evidence

The store defines WEAK as *"a file the task names was modified, but no `closes` fired… these are
inferences, not declarations"*. Across all 65 store files and all history only **11 ids were ever
STRONG**, of which just `#430`/`#505` are live — both refused above. The closure wave then
re-derived every bracketed candidate merge from git and diff-inspected the **67** rows carrying one;
**7 were claimed DISCHARGED and 4 were REFUTED on adversarial re-check**. Precedent: `57ae83a6`
(*"39/39 WEAK proposals rejected at architect review"*). **No close in this arc rests on a store entry.**

*Live-count note:* the contract cites 149 WEAK; live at HEAD it is **141** (2 STRONG + 141 = 143,
matching the SessionStart surfacing). Reported, not reconciled — the store is regenerated nightly.

### 4.4 The expired pegs — and the census itself was defective

**MEASURED DEFECT IN N1.** It claims *"15 of 33 pegs have EXPIRED … in five classes"*, but Classes
A–E enumerate **13** (7+3+1+1+1); its not-expired list is 18; **13 + 18 = 31 of 33**. `[#301]` and
`[#494]` are censused in **neither list**. Fifteen rows were adjudicated here: the 13 enumerated plus
the 2 the census dropped.

| Disposition | Rows | Basis |
|---|---|---|
| **UN-DEFERRED → open** (7) | `[#82]` `[#145]` `[#171]` `[#239]` `[#293]` `[#297]` `[#298]` | A peg whose condition is MET is not a deferral, and re-pegging it would invent a blocker. Wave-1 completed **2026-07-07** (`[#221]` closed; `deployed-versions.yaml` corroborates); the pegs naming it were written **2026-07-08**. **32 days behind a satisfied condition.** `[#298]` is Class E — the handoff-group pass ran this window and skipped it |
| **RE-PEGGED** (3) | `[#294]` `[#492]` `[#494]` | Each old referent could not fire |
| **REPORTED, not executed** (4) | `[#102]` `[#308]` `[#325]` `[#310]` | Kill candidates — §4.5 |
| **RECORDED, no edit** (1) | `[#301]` | Its referent `[#298]` is now open; the deferred-on-deferred chain is single-ended (answers N1 R-4) |

- `[#171]` alone held a **three-row chain** — `[#169]` both `depends-on` and pegs on it; `[#322]`
  names it as a data source.
- `[#293]` was checked for closure and **refused**: measured today, **0 of 6** consumer repos carry a
  seeded `docs/handoffs/README.md`, so its `n>=1` clause is unmet. An un-defer, never a close.
- `[#492]`'s spent calendar leg was **dropped rather than re-dated** — inventing a date is the
  placeholder-peg trap the 2026-08-08 ruling already closed. The release leg is OPERATOR-owed.
- `[#494]`'s peg *"the §6-spine close"* is **UNLOCATABLE** — it appears nowhere in the tracked corpus
  except the JOURNAL entry that wrote it and the row itself. Same defect class as `[#294]`'s
  non-existent epic, and one of the two rows N1 never censused.

**Side effect, surfaced not absorbed:** re-pegging `[#492]` dropped its spent date, taking the row
from three dates to two and off the `>=3 dates AND >700` branch — so
`warn-doc-rot-backlog-accretion-492-grok-peg` matched no live WARN **on the run that produced it**.
Removed per the ADR-75 decoration rule. It retired at the peg adjudication rather than at the Grok
arc its own text anticipated; `[#492]` remains DEFERRED, so this is not a flip-open.

### 4.5 The four kill proposals — REPORTED with evidence, none executed

Deletion candidates are reported and never acted on without operator approval (standing ruling).

| # | Row | The Done-when clause that can no longer be met | Evidence | Recommendation |
|---|---|---|---|---|
| **K-1** | `[#102]` P2/M — machine-readable repo index | *"a pilot index on one repo demonstrably replaces exploratory reads"* — its peg names the precondition, and the peg's own text says the condition will never occur | Peg verbatim: *"a repo whose codemap is generator-MANAGED (#262/#295 closed 2026-07-25 — flat / single-package layouts stay hand-authored **by policy, so no fleet codemap migration is coming to peg on**)"*. `#262`/`#295` verified closed at `19b5d598` | **KILL.** This is an undeclared kill already: a row whose own text states its precondition is unreachable. No superseding id exists, and the `verify-first` clause (confirm `stacklit`/`scip-search` exist) was never discharged |
| **K-2** | `[#308]` P3/S — the `verify` skill's canonical home | *"the verify-skill home is decided … at/along the P6 carrier step"* — the P6 carrier step is gone | The row's own `kill-candidates:` line: *"the P6 corpus roll it pegged to (#221) closed at 8aab4356 **with no successor**"* | **RE-PEG, not kill.** The underlying decision (distribute vs permanently hub-local) is still real and still undecided; only its scheduling vehicle died. Its natural new referent is the intake #25 W-wave carrier decision — the same one `[#294]` was re-pegged to |
| **K-3** | `[#325]` P3/S — carry `/save` to consumers | *"`/save` ships to a consumer via a manifest command-artifact carrier"* — same dead P6 referent | Same `#221`-with-no-successor peg. `[#294]` is the nearest live carrier row | **FOLD into `[#294]`.** A fold is likelier correct than a kill: the work is real, it is a manifest-carrier question, and `[#294]` now carries the live W-wave peg. Folding also discharges the row's second clause (record `/handoff`'s intentional absence) inside a row that already reasons about carriers |
| **K-4** | `[#310]` P3/S — cold-bundle annotation surface | *"a sanctioned cold-annotation surface is defined AND the 07-05 bundle is recorded as-cold"* | Cheapest in the set: the live audit's `preflight_backlog_ids` WARN points at it **every run**, and `#292` — the precondition named in its own escape clause (*"if the operator rules the 07-05 bundle's cold state is adequately recorded in #292's evidence text, close without building any surface"*) — is **verified closed** | **KILL via its own escape clause**, which is a close rather than a deletion. Operator confirms whether `#292`'s evidence text adequately records the cold state. Clearing it also silences a standing WARN |

---

## 5. Amendment 2 — the coverage diff (Phase C's first act)

`$env:CLAUDE_PROMPTS_DIR` → `C:\Users\1028120\Downloads`; both draft contracts **present and read**.

### 5.1 `CONSOLIDATE-AND-CLEAN.md`

| Clause | Status | Note |
|---|---|---|
| 0.1 branch inventory (name/tip/ahead-behind/files/STOP packet) | **PARTIAL** | ARC-2 covers only the *retained* branches (§9). A full inventory of every branch is not in scope here |
| 0.2 every audit finding has a row id, a disposition, or nothing | **COVERED** | §6 triage; ADR-111 makes it a rule |
| 0.3 every intake: status + downstream ADR/rows | **NOT-COVERED** | → **T-N1** |
| 0.4 every ADR: status + landing predicate | **NOT-COVERED** | → **T-N2** |
| 0.5 spec-version refs disagreeing with live | **NOT-COVERED as a sweep** — but **one instance found** | PLAYBOOK's `(v1.7)` vs live 1.13 → **T-D1**. The contract's own worked example (PLAYBOOK Ch8 citing HANDOFF_PROCESS v5) is a *different* citation and was **not** re-verified |
| 1 branch drain | **NOT-COVERED** | ARC 1 drained; ARC-2 reports the retained set only |
| 2 closure adjudication wave with the `[#506]` sheet | **COVERED** | Phase A |
| 3 audit→backlog food chain: row or disposition per finding; births capped by close capacity; **land the rule**; **add an orphan-finding check** | **MOSTLY COVERED** | Rule landed as ADR-111; birth cap honoured at net 0. **The orphan-finding CHECK is NOT built** and ADR-111 says so explicitly → **T-N3** |
| 4a fix stale spec-version refs | **NOT-COVERED** | T-D1 reported, not fixed |
| 4b ARCHITECTURE reconcile + re-stamp only if genuinely re-read | **NOT-COVERED** | Not re-read this arc; **not re-stamped**, and saying so is the point |
| 4c archive completed intakes/ADRs/audits per convention | **NOT-COVERED** | → **T-N4** |
| 4d report-don't-delete redundancy | **COVERED** | §9 |
| 5.1 PLAN travels with the handoff · 5.2 verification at the cut | **COVERED** | Ruled operator-endorsed but **UNRATIFIED**; attached to `[#511]` as evidence and scope (§7) |
| 6 packet with velocity line | **COVERED** | §1 |

### 5.2 `RESEARCH-INGEST.md`

| Clause | Status | Note |
|---|---|---|
| 1 land the five memos, taxonomy-correct home, quote the clause | **COVERED, and the answer is DO NOT LAND** | No governance clause defines a home for external research artefacts and ADR-101 seals the tree against inventing one. Each memo is cited by title + workflow id inside the intake carrying its proposals |
| 2 file intakes #30/#31 verbatim DRAFT; verify #28/#29 | **NOT-COVERED — and the contract's premise is FALSE** | #28 and #29 **are** filed (both DRAFT). **#30 and #31 are NOT filed.** ARC-2 Phase C lists "intakes #30/#31 as filed" as an *input*; they do not exist → **T-N5** |
| 3 the distillate: one table, LANDED-ALREADY column | **COVERED** | §6 |
| 4 cross-check memo claims against live repo | **COVERED** | §6.4 |

---

## 6. Phase C — the triage. Zero untriaged.

**Outcomes:** **(a) OWNED** · **(b) DISCHARGED** · **(c) CANDIDATE** · **(d) REJECTED** · **OPERATOR**.

### 6.1 Counts

| Outcome | Findings | Ruling items | Memo proposals | Total |
|---|---|---|---|---|
| (a) OWNED | 34 | 6 | 3 | **43** |
| (b) DISCHARGED | 52 | 4 | 9 | **65** |
| (c) CANDIDATE | 39 | 18 | 14 | **71** |
| (d) REJECTED | 20 | 3 | 12 | **35** |
| OPERATOR | 8 | 7 | 0 | **15** |
| **Total** | **153** | **38** | **38** | **229** |

### 6.2 Findings — every id, by outcome

**(b) DISCHARGED — the LANDED-ALREADY column. This is the anti-rebuy mechanism; every row cites a resolving locator.**

| Finding(s) | LANDED-ALREADY locator |
|---|---|
| C-1, N1-37, N4 R4, N5-23, N5-24, I-5 | `[#453]` OPEN P2/M — records all three container gaps *with these exact workarounds* since the 2026-07-31 cloud batch. **Four lanes re-measured an open row** |
| N1-17 | Discharged by the night packet itself (§7 of the batch) — criterion (2) closes if net ≤ 0 |
| N1-23, N3-23 | `[#461]` CLOSED — `window_metrics.py` already shipped; the proposal is to *extend* it, not build it |
| N2-05, N4-18 | `[#483]` CLOSED — `/preflight` adopted (ungated); the stale-locator class it catches is exactly N4-18 |
| N2-08 | `[#429]` CLOSED — `worktree_seed --plan` verified to print two halves |
| N2-21 | `[#480]` CLOSED — the coverage leg; this arc *exercised* it on `df1b05b0` |
| N2-04, N2-13, N2-14, N2-18, N2-22, N2-28, N3-08, N3-15, N5-01, N5-14, N5-15, N5-16, N5-17, N5-19, N5-21, N3-22 | **DO-NOT-BUILD / REFUTED / SETTLED by their own lane.** Recorded so they are not relitigated (do-not-relitigate discipline). `lychee`, `mkdocs`, contract-lint, companion-file predictor, HEAD-swap organ, schema library, Jinja2 templating, orchestration replacement — all declined **with reasons** |
| N1-01, N1-02, N1-03, N1-13, N1-38, N2-17, N2-26, N3-01, N3-02, N3-05, N3-06, N3-09, N3-14, N3-27, N3-28, N4-15, N4-17, N4-19, N4-20, N5-04, N5-07, N5-11, N5-18, N5-22, N5-25, N5-26, I-3, I-6, I-7 | **MEASUREMENTS / INFO with no action owed.** Recorded; no birth |
| N1-34 | Considered and explicitly **not** proposed for death — `[#506]` grooming call |
| N4-F10 | Recorded by its own lane precisely because *"an inert validator is indistinguishable from a passing one until someone checks"* |

**(a) OWNED — an open row already covers it; evidence attached, nothing born**

| Finding(s) | Owning row |
|---|---|
| N2-01, N2-09, N2-10, N2-15, N2-23, N2-26, N3-16, N3-29, I-4 | `[#505]` P1/M batch protocol |
| N2-12, N3-13, N4-16 | `[#502]` P3/M import convention — **ruled Shape B** (`[".", "scripts", "deploy"]`, measured `23198aae`); its Done-when should carry the residual 24+1 sites and verification by isolated collection |
| N1-20, N2-29, N2-30, N2-31 | `[#511]` P2/M handoff cut |
| N1-21 | `[#341]` P2/S codex producer lane |
| N1-22 | `[#426]` P2/M routine consumers — the one standing RED |
| N1-26, N1-27 | `[#270]` / `[#213]` — the latter now CLOSED by this arc |
| N1-35 | `[#499]` P3/M — its peg cannot fire while the FP count is not reported at each seal |
| N1-36, N5-12, N5-13 | `[#487]` P2/L closure-proposal pipeline (+ `[#454]`, `[#277]`) |
| N3-11, N3-30 | `[#317]` P2/M default-parallel invocation |
| N4-13, N4-14, N4-F11, N5-09, N5-10, N5-11 | `[#397]` P3/M `scripts/` structure |
| N4-F3, N4-F4 | `[#485]` P3/S — the natural landing seam for carrier containment |
| N4-F8 | `[#369]` P3/S partially; **`ecosystem/index.yaml` itself is UNOWNED** → (c) |
| N2-25 | `[#345]` P2/M externalize the ADR-101 frozensets |
| N5-08 | `[#345]` adjacent — `check-jsonschema` for `deploy/manifest-v*.yaml` |
| N2-06 (prose half), N2-07 | `[#508]` / `[#510]` — the **code-vs-code** half is NOT owned and is born as `[#514]` |
| N1-19 | `[#293]` `[#294]` `[#305]` — all three un-deferred or re-pegged by this arc |

**(c) CANDIDATE — needs a decision; joins an intake or (where already ruled) births**

| Finding(s) | Route |
|---|---|
| N5-03, N5-05, N3-04, C-5 | **BORN `[#513]`** — propagation completeness, ONE row at n=3 per the architect's ruling |
| N4-F2, N2-06 (code half), I-1, I-2, N2-07 | **BORN `[#514]`** — the two rival `LANE_BRANCH_RE` constants, provisioning-first |
| N4-F1, N4-F6, N4-F5, N4-F12 | **BORN `[#518]`** — one call site, two reproduced defects |
| N1 R-16, N4 R4, N5 R3, C-1 | **HELD `[#515]`** — enforcement reach as a three-layer property → intake #32 |
| graph commission `footprint:` | **HELD `[#516]`** → intake #29 Fold B (measured there at 5/168) |
| cloud attestation | **HELD `[#517]`** → intake #32 (its central rule) |
| N2-16, N2-19, N2-20, N2-24 | Rule C (consumer-glob round-trip) — batch-4 build candidate, **not** born; its `_CONSUMER_CONTRACTS` growth surface needs closure discipline first (*"a Rule C with six speculative rows is worse than no Rule C"*) |
| N3-03, N3-26 | Cheap-win #1/#2 — folded into `[#513]`'s third instance |
| N3-07, N3-25 | **The largest measured saving rests on INFERENCE, and the lane says so against its own recommendation.** Not built, not dismissed — the tension is the architect's to resolve |
| N3-10, N3-12, N3-20, N4-F7, N4-F9, N5-02, N5-06, N5-20 | Batch-4 build candidates, each cheap and each unowned. **N5-02 is the sharpest: there is NO secret scanning of any kind, bespoke or delegated** |
| N1-04, N1-15, N1-16, N1-18, N1-24, N1-25, N1-28, N1-29 | Scoreboard / prioritisation — §8 |
| N1-14 | Intake #28 §B is DRAFT — the North Star is scored against an unratified finish line → ratification batch |
| N2-11, N3-18, N3-24, N4-F8 (`index.yaml`) | Open questions carried to batch-4 planning |

**(d) REJECTED — recorded with a reason, not relitigated.** The dead list stands and was **not**
re-opened: *Functional Programming in Scala* as fleet source of truth · notebook environments ·
server-based graph databases and the archived embedded one (Kùzu) · symlinks as the provider-stub
mechanism on Windows · parallel memory layers beside the repo · single-GPU training tooling ·
auto-closing stale-bots and backlog bankruptcy as a first resort · big-bang refactor without hotspot
measurement · parallelising the probe gate · a standard security-report format for review artefacts ·
public benchmark scores as the selection instrument · routing a consumer subscription through a
foreign agent harness. Plus every DO-NOT-BUILD in the (b) table above, which is rejection *with a
lane's reasoning attached*.

**OPERATOR** — 15 items, kept short (§7).

### 6.3 The 38 ruling items

- **Adjudicated by this arc (10):** N1 R-4 (`[#298]` end opened) · R-8 (`[#322]`'s referent was ruled
  against — the row waits on nothing; re-peg owed) · R-13 (the 15 pegs, §4.4) · N2 R7 + N4 R1
  (`LANE_BRANCH_RE` — **one ruling, asked twice**, now `[#514]` with the sequence fixed) · N5 R4
  (propagation ownership, adjudicated on **n=3** → `[#513]`) · N1 R-9 (the `open backlog < 100`
  filter — **194**, named in §1) · N5 R3 + N1 R-15 (the uv pin → `[#517]` held, intake #32) ·
  N4 R3 (`_git`'s missing scrub is a **defect**, not an exemption → `[#518]`).
- **Routed to the ratification batch (18):** every remaining N1/N2/N3/N5 item whose answer is a
  decision the operator or a ratified intake must supply.
- **OPERATOR (7):** N1 R-5, R-14 · N2 R6 · N3 4 · N5 R1 — plus the two in §7.
- **Three rulings asked twice were adjudicated once**, as the index requested: `LANE_BRANCH_RE`,
  cloud-runtime gate coverage, the uv pin.

### 6.4 Memo proposals — cross-checked against live repo state

**One memo claim explicitly marked FALSE about this repo.** The graph memo (`wf-f6851745`) states
grimp is *"already the engine behind your import-linter usage."* **Verified 2026-08-09: neither
`grimp` nor `import-linter` exists anywhere here** — `pyproject.toml`, `.pre-commit-config.yaml` and
`uv.lock` are all clean; the single hit in the whole tree is an unrelated placeholder in
`templates/ARCHITECTURE-template.md`. **The memo's cheapest proposed edge source is not free here;
it is an unadopted dependency.** Its `footprint:` denominator (169) is also one window stale — live
is **5 of 168 (3.0%)**, numerator confirmed.

**One well-argued proposal DECLINED on measured, repo-specific grounds.** The code-style memo
(`wf-8a83eb70`) proposes a complexity-ratchet stack — `xenon` hard ceilings over `radon`, `wily`
trend ratchets, `complexipy` cognitive complexity, and a set of ruff `PLR*`/`C901` size rules.
**Declined**, on this repo's own numbers:

1. **The premise it would serve is refuted here.** N5 measured **0 of 41** audit checks as generic
   lint — every one encodes ADR-cited policy with a repo-specific constant. There is no style layer
   for a complexity gate to protect.
2. **The cost centre it targets does not exist.** N3 measured the whole 41-check mesh at **11.66 s,
   ~0.2 % of an integration arc**, and three checks are 83.5 % of that. A complexity ceiling buys no
   measurable time.
3. **The one measured performance defect was not complexity.** It was an `rglob` path-walking bug in
   two test files (15.13× inflation). No complexity metric would have found it; a corpus-definition
   rule did.
4. **The ratchet the memo praises already exists** — `silent_rule_ratchet`, live at **437 ≤ 441**.
   The memo itself says *"your existing silent_rule_ratchet is already best practice — extend it,
   don't refactor blindly"*, and *"only refactor where high churn meets high complexity"* — **and no
   hotspot measurement exists.** Adopting the gate before the measurement inverts its own advice.
5. **Two of the three tools are maintenance risks by the memo's own text** — `radon`'s last PyPI
   release predates 2024, `wily`'s cadence is *"slower; validate before adopting fleet-wide"*.

**The two traps the architect named are held OPEN, not resolved:** the code-style ruff rule-family
list and the graph storage choice (DuckDB vs SQLite) **read like decisions and are not** — the
author flags both as his least-defended. Neither is treated as ruled here.

**Cloud compute is presented as INDEPENDENT, not as one of six.** Commissions 1–5 decompose *"which
rules survive without a human remembering them"*; #6 is a capacity problem. Its own research says
**fix local first**: the suite is wait-bound at **~14.6 % CPU**, the path-walking defect is ~24 % of
the worktree penalty, and filesystem placement, antivirus scanning and editor indexing carry much of
the rest — all $0. *"Buying compute now would paper over a bug."*

---

## 7. What is now OPERATOR-owed — one line each

1. **`[#492]`** — has Grok 4.6 released? External fact, unverifiable from the repo (N1 R-5).
2. **The four kill proposals** — K-1 `[#102]` KILL · K-2 `[#308]` re-peg · K-3 `[#325]` fold into `[#294]` · K-4 `[#310]` close via its own `#292` escape clause (§4.5).
3. **The OneDrive rule conflict** — ai-council forbids reads of those paths; corp-ops permits enumerated non-destructive reads; global core-invariants matches corp-ops. Three surfaces, two rules.
4. **ADR-111 ratification**, and specifically its **§4 departure**: the contract's *"only an accepted ADR births rows"* conflicts with ratified ADR-98 §3. If an ADR really is to be mandatory per birth, that is an amendment to ADR-98 §3 and should be ruled as one.
5. **`[#511]`** — which handoff load is cut. No engineering closes criterion (5); the mechanized cost is ~4.5 s of a 30-minute wall clock.
6. **Intake #30 / #31** — authored, id-reserved, still unfiled (T-N5).
7. **N2 R6** — the n=5 unattributed HEAD swaps are UNVERIFIED; the reflog needed to check is gitignored.
8. **N3 item 4** — the contract's `2h43m` / `~9 minutes` figures are unlocated anywhere in the tracked record.
9. **N5 R1** — do rewriting pre-commit hooks get in, or the read-only set only? (`trailing-whitespace`/`end-of-file-fixer` collide with the append-only and immutability invariants.)
10. **N1 R-14** — the 153 pending closure proposals could not be examined from a cloud clone; the store is gitignored.
11. **The two engine amendments** — operator-endorsed but **UNRATIFIED**; attached to `[#511]` as evidence and scope, not treated as ruled.
12. **ARCHITECTURE.md was not re-read and was NOT re-stamped** this arc — stated rather than papered over.
13. **`[#322]`** — its peg referent exists and was ruled *against* ("visualization deferred wholesale"); a row waiting on answered research needs a new peg.
14. **`[#502]`'s Done-when** should be amended to carry the residual 24+1 sites and isolated-collection verification (ruled, not yet written).
15. **Intake #28 §B is DRAFT** — the whole North Star scoreboard is scored against an unratified finish line.

---

## 8. Priority pass — the ordering for the next window (report only; no row edited)

**16 P1/P2 rows idle > 30 days.** 10 of the 16 were last touched by a *bulk grooming pass*, so their
real "considered on merits" date is older than any table shows.

1. **`[#270]` P1, idle 32 days — the standout.** One of only three open P1s **and a prerequisite**:
   `[#271]` and `[#348]` carry `depends-on: #270`, and `[#117]` pegs on it. Unblocking it unblocks three.
2. **`[#514]` P1 (born this arc)** — blocks batch 4 by wedging the merge queue.
3. **The 3 P3-blocking-P1/P2 edges:** `[#23]`→`[#112]` (3-deep) · `[#170]`→`[#139]` · `[#298]`→`[#301]`
   — the last is now single-ended, since `[#298]` was un-deferred by this arc.
4. **The 8 rows that are P1/P2 *and* deferred** — two are P1 (`[#218]`, `[#300]`). A row simultaneously
   urgent and parked carries a priority it cannot act on (N1 R-12 asks whether that should be legal).
5. `[#213]` is off this list — it was idle 32 days **and diff-verified closeable**, and is now closed.
   That was a consumption failure, not a work failure.

---

## 9. Retained branches — reported, nothing deleted

| Branch | Ahead / behind `main` | What it holds | Protection still applies? | Recommendation |
|---|---|---|---|---|
| `automation/fleet-audit` | **163 ahead**, 4758 behind | 352 distinct paths, all `docs/audits/*-ecosystem-audit.md` daily baselines | **YES** — organ-produced replication lane (STANDING_RULINGS B5); the standing lesson is that these dailies must never reach `main` | **KEEP, do not merge, do not delete.** `fleet_audit_replication` reports it at parity with origin (0 ahead) — it is doing exactly its job |
| `claude/conformance-2026-08-{03,04,05,07,08,09}` (6) | 1–2 ahead each | one nightly conformance digest apiece + the audits index regen | **YES** — explicitly protected by `.claude/rules/git-discipline.md`; silence is not protection, and these are *named* | **KEEP.** Each is a single dated digest; merging them would put nightly automation output on the spine |

**No branch was deleted, and none is recommended for deletion.** Both families are the same class:
machine-produced daily artefacts whose value is precisely that they stay off `main`.

**One consumer item, verified not fixed — and the finding is REFUTED.** ARC 1 reported
`corp-sca-time-automation` carrying no `.gitattributes`. Measured today: the file **is present on
`main`** (batch 3's `5518c36`, which exists in that repo), and the repo's primary checkout sits on
`feature/tenrox-loader`, where it is **absent from the tree**. **The finding is a branch-context
artefact** — ARC 1 read a working tree whose branch predates the batch-3 merge. The consumer was
left untouched, as instructed.

---

## 10. Row map

**Born (3)** — full profiles in `BACKLOG.md`; each verified UNOWNED against the live open set:

| id | P/S | Theme · Story | Why it exists |
|---|---|---|---|
| `[#513]` | P2/M | [E8] · [S22] | Propagation completeness at n=3, ONE row not three; the **detector** is the landing predicate |
| `[#514]` | **P1**/M | [E2] · [S3] | Two rival `LANE_BRANCH_RE` constants; blocks batch 4; provisioning-enforcement **first** |
| `[#518]` | P2/S | [E2] · [S3] | `audit.py::_git` — one call site, two reproduced defects, one corrupting a gate's own baseline |

**Held, not dropped (3)** — each already has an intake carrying its content; full row text preserved
in `git show` of the Phase-E commit's parent, ready to birth in one paste when closes are demonstrated:
`[#515]` enforcement reach → intake #32 · `[#516]` `footprint:` predicate → intake #29 Fold B ·
`[#517]` cloud attestation → intake #32.

**Closed (3):** `[#213]` `[#215]` `[#441]` — §4.1. **Re-pegged (3):** `[#294]` `[#492]` `[#494]`.
**Un-deferred (7):** `[#82]` `[#145]` `[#171]` `[#239]` `[#293]` `[#297]` `[#298]`.
**Kill candidates reported, none executed (4):** `[#102]` `[#308]` `[#325]` `[#310]`.

---

## 11. Phase D — the three orphan commissions (amendment 3)

**One new intake, two amendments, one scope note — nothing silently dropped.**

- **Cloud compute → intake #32** (new). Filed at **32, not 30**: ids 30/31 are **reserved** by two
  authored-but-unfiled operator drafts, and taking 30 would have collided with a permanent join key.
- **Graph + telemetry → intake #29** amendments. Telemetry **converges with N3-21 independently**
  (*"most of what you want is already recorded"* vs *"the correct organ is a READER, not a
  RECORDER"*), so S3a's first move is extraction, not plumbing.
- **Portability → a scope note on intake #25 W-9(a)**, whose territory it already is. It **confirms**
  W-9(a)'s `@AGENTS.md`-shim mechanism on external grounds and bounds W-10 sharply: only the
  instruction-file layer ports; hooks, slash commands, subagents, skills and permissions do not.

**No memo file was landed, and the clause is quoted rather than assumed:** no governance clause
defines a home for external research artefacts, and ADR-101 seals the tree against inventing one.

---

## 12. Pipeline law — ADR-111 (Proposed)

`docs/decisions/ADR-111-finding-triage-pipeline.md`. **Five of eight proposed clauses were already
law and are cited, not restated** — ADR-100 §4 (audit = evidence, intake = a request to change
state), `docs/intake/README.md` §5 (REJECTED terminal + `docs/intake/archive/`, **no new register and
no new path**), ADR-98 §4 and §3, PLAYBOOK filing-backpressure. The genuine gap is narrow: **nothing
governed the edge from a FINDING to any of those**, and that is all ADR-111 rules.

Two things it deliberately does **not** do, both recorded in the ADR itself: it does not adopt the
ADR-mandatory birth rule (§4 — it contradicts ratified ADR-98 §3, and live practice matches ADR-98),
and it does not ratify the quantitative equilibrium clause (§5 — that is intake #22 §F, which ADR-108
explicitly leaves unratified). **It arms no gate and says so**; whether it earns one is an n=2
question to be measured on the next two audits.

---

## 13. Gate state

| | Before (`df1b05b0`) | After |
|---|---|---|
| `audit.py ship-gate` | **RED** — 9 new/undispositioned WARNs | **GREEN** — 26 dispositioned |
| `audit.py health` | DEGRADED (2 advisory) | **OK** |
| `doc_rot` | 1 (dispositioned) | **clean** — 0 findings, 0 dispositions needed |
| BACKLOG rows | 194 | **194** |
| Bypasses used | — | **zero** `SKIP=` · **zero** `--no-verify` · **zero** force-push |

**Self-induced bloat was drained twice rather than dispositioned** — the peg annotations tripped
`doc_rot` on 7 rows, and the three born rows tripped it again. Both were condensed. The register's own
standing distinction held: a row's own framing prose gets trimmed; only a ruled, load-bearing date
earns a disposition. The one pre-existing `doc_rot` disposition **retired** in the process.

---

## 14. One correction, recorded plainly

**The Phase-A closes were not real when first committed.** `cd38fb8a` set `status: closed` on three
task files and stopped; `BACKLOG.md` still rendered all three and the row count never moved
(194 → 194). Closing is **two edits**: the terminal status **and** the manifest-node removal, in the
same edit (ADR-107 §6.3; precedent `f98d1262`). Task frontmatter is **derived** — `gen_task_tree.py
--emit-source` re-derives it from the manifest, so with the nodes still present it **silently reverted
all three back to `open`** in the very command that regenerated `BACKLOG.md`. Its output said so
(*"refreshed derived frontmatter in 3 task file(s)"*) and I read that as the closes landing rather
than being undone. Every gate stayed green throughout, correctly — nothing was incoherent; the rows
were simply still open. Completed at `a62d988e`.

**How it surfaced is the lesson:** not from a gate and not from re-reading my own work. It came from
verifying an unrelated *external* claim — a memo's `footprint:` denominator — which required a live
open-row count, and that count disagreed with the number I had just published. **A cross-check aimed
at someone else's claim caught mine.**

---

## 15. The sequence the successor inherits

1. **Ratification batch** — intakes #28–#31 **plus #32** and the ARC-2 triage distillate, adjudicated
   as **ONE batch**. ADR-111 rides it. (#30/#31 must be filed first — T-N5.)
2. **Adversarial review of the concrete batch-4 plan, BEFORE the operator's GO.**
3. **Handoff cut.**
4. **Execution week.**

**Blocking note for batch 4:** `[#514]` is P1 because the ADR-110 exemption is *unreachable* for cloud
lanes. Until provisioning-side enforcement lands, a cloud batch's merge queue wedges at its first
conflicted merge — which is how batch 3 lost 2h12m to a run that produced nothing mergeable.

---

## 16. Acceptance contract — SELF-TEST

| # | Item | Verdict |
|---|---|---|
| 1 | Phase 0 done: gate GREEN, 8 WARNs dispositioned under `#241`, reviewer lane run on `df1b05b0` | **PASS** |
| 2 | Phase A ran FIRST and its velocity line is reported separately | **PASS** — §1 |
| 3 | Every finding and memo proposal triaged; zero untriaged; OPERATOR bucket short and justified | **PASS** — §6, 229 items, 15 OPERATOR |
| 4 | At most six rows born | **PASS** — three |
| 5 | LANDED-ALREADY column non-empty and cited | **PASS** — §6.2, every (b) carries a locator |
| 6 | ≥1 well-argued memo proposal DECLINED on measured, repo-specific grounds | **PASS** — the complexity-ratchet stack, §6.4, five measured grounds |
| 7 | ≥1 memo claim explicitly marked FALSE about this repo | **PASS** — grimp/import-linter, verified absent |
| 8 | Net ≤ 0 on the velocity line | **PASS** — net 0, at the cost of three held births (§10) |
| 9 | Each orphan commission has an owning intake or an explicit not-now-with-trigger | **PASS** — §11 |
| 10 | Zero `SKIP=` / `--no-verify` / force-push; every merge anchored; nothing deleted without approval | **PASS** — §13 |

**Two items that are PASS only with a stated caveat, flagged rather than claimed clean:**

- **#4/#8 collided.** "At most six" and "net ≤ 0" cannot both be maximised at a demonstrated close
  capacity of three. I resolved toward the smaller bound, births ≤ closes, because that is the
  doctrine this arc itself ratifies. **Three ruled decisions were held rather than born**, with their
  text preserved and their intake homes named.
- **#3's completeness is at the granularity of the findings index**, which is itself a summary of
  3,487 lines across five reports. Every indexed finding, ruling item and memo proposal carries an
  outcome; a claim buried in a source report and not surfaced by its own index would not have been
  seen by this pass.

**Not attempted, and named rather than left silent:** the `CONSOLIDATE-AND-CLEAN` clauses marked
NOT-COVERED in §5.1 — the full branch inventory, the intake/ADR landing-predicate sweeps (T-N1/T-N2),
the spec-version sweep (only one instance found, T-D1), the ARCHITECTURE reconcile (T-N/A — not
re-read, **not re-stamped**), the archival pass (T-N4), and the orphan-finding **check** (T-N3, which
ADR-111 declines to build without n=2 evidence).
