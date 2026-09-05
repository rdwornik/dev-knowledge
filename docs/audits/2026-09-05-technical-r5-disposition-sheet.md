# R5 DISPOSITION SHEET — the 133 undispositioned ship-gate WARNs, grouped for one ruling pass

**Class:** technical · **Date:** 2026-09-05 · **Author:** CC (Opus 5), R5 PREP session
**Posture:** READ-ONLY PREP. Nothing here is dispositioned. Every disposition below is
**PROPOSED**; the architect rules in the window. No register entry, ledger row, task row or
gate was edited by this session.

**No-consumer:** this artifact is the input to the R5 dispositioning window itself; it is
consumed by the window's rulings, which do not exist yet. It names `[#552]` (window-close
disposition routine) as the row that should own its remedy.

---

## §0 Provenance — what was measured, at which SHA, and what has moved since

- **Inventory SHA:** `6de676fb` (2026-09-05, *Merge branch 'docs/playbook-essentials-routes'*).
  `uv run --locked python scripts/audit.py ship-gate`.
- **Verdict at that SHA:** `RED — 1 hard-fail organ; 133 new/undispositioned WARN(s)`.
  **156 WARN rows total**, of which **23 are dispositioned** by
  `ecosystem/disposition-register.yaml`, leaving **133**. Two register entries print `[stale]`.
- **Historical anchors were re-measured, not inferred.** Two detached probe worktrees were
  created, the gate run in each, and both removed and their removal verified
  (`git worktree list` back to its prior set):
  - `cd4035e7` (2026-09-02) → **123 undispositioned**
  - `b3023108` (2026-09-04) → **133 undispositioned**
- **Main has moved during this session.** It was `6de676fb`, then `1d96e0de`, and stood at
  `3200757d` when the probes were cleaned up. Concurrent sessions are committing. Re-run the
  gate before ruling if precision at the margin matters; the *shape* of every finding below is
  stable across the window.

### A correction to the brief's growth series

The brief gives `123 (09-02) → 136 (09-04) → 156 (now)`. Those are not the same unit, and one
is not reproducible:

- **123** and **136** are *undispositioned* counts. 123 is recorded at
  `protocols/STANDING_RULINGS.md` §AC ruling R-G0-1; 136 at `JOURNAL.md:55` (2026-09-04).
- **156** is the *total* WARN-row count, which includes the 23 dispositioned. The comparable
  figure today is **133**.
- **136 is not reproducible at any commit.** The gate at `b3023108` — the last merge of
  2026-09-04, the day that JOURNAL entry covers — returns **133**. The three-WARN gap is
  explained and verified: that same session closed `[#276]`, `[#614]` and `[#630]`, which
  removed four `doc_rot` loci (`#276` fires both arms). The 136 was measured mid-session,
  before its own closures landed.

**The series in one unit (undispositioned):** `123 → 133 → 133`.
**The series in total WARN rows:** `145 → 156 → 156`.

---

## §1 GROWTH — every net-new WARN since 2026-09-02, and who introduced it

Measured by **identity diff** of the two full gate inventories (`cd4035e7` vs `6de676fb`), not
by subtracting counts. Net: **145 → 156 WARN rows (+11)**, composed of **+19 genuinely new
rows** and **−8 cleared**.

### 1.1 The net-new: 19 rows, and all 19 are batch-G audit artifacts

Ten `.md` audit artifacts landed in the window. Each produced one `funnel_coverage` WARN; nine
of the ten also produced a `consumer_at_landing` WARN. **That is the entire growth.**

```
organ                  locator                                                    introduced by
funnel_coverage        2026-09-02-technical-batch-g-manifest.md                   b2355207 (09-02) docs/batch-g-manifest
funnel_coverage        2026-09-02-verification-parity-b5753f52.md                 85827046 (09-02) worktree-lane-g-632-parity
funnel_coverage        2026-09-02-technical-lane-g-276-deploy-waiver.md           e9c6bbad (09-02) worktree-lane-g-276-deploy-waiver
funnel_coverage        2026-09-02-technical-lane-g-621-freshness-absent.md        55fecf34 (09-02) worktree-lane-g-621-freshness-absent
funnel_coverage        2026-09-02-technical-lane-g-626-terra-tally.md             cfa9a8e3 (09-02) worktree-lane-g-626-executing-copies
funnel_coverage        2026-09-02-technical-lane-g-628-essentials-debless-packet.md  830e6286 (09-03) worktree-lane-g-628-essentials-debless
funnel_coverage        2026-09-02-technical-lane-g-614-hygiene-close-packet.md    a436545a (09-03) worktree-lane-g-614-hygiene
funnel_coverage        2026-09-02-technical-lane-g-611-bundle-thinning.md         e9d39ed9 (09-03) worktree-lane-g-611-bundle-thinning
funnel_coverage        2026-09-03-technical-lane-g-621-c7.md                      001bb261 (09-04) worktree-lane-g-621-c7
funnel_coverage        2026-09-02-technical-batch-g-close-packet.md               6ee7c897 (09-04) docs/batch-g-close-packet

consumer_at_landing    the same nine, EXCLUDING 2026-09-02-verification-parity-b5753f52.md
                       (that one IS cited from a governance surface -- protocols/STANDING_RULINGS.md:2855
                        and protocols/HANDOFF_PROCESS.md:1118 -- so it cleared consumer_at_landing
                        and fired funnel_coverage only)
```

### 1.2 The cleared: 8 rows, and every one was a real defect

```
organ                          what cleared
doc_rot (x4)                   BACKLOG#276 (both arms), #614, #630 -- rows closed, left the manifest
doc_claims                     2 prose claims re-synced (precommit_hook_count 21->22, pytest_collected)
funnel_lifecycle               intake 2026-07-16-satellite-onboarding-prompts.md READY 51d -> archived
git_backlog_drift              #614 closed-but-present resolved
canonical_freshness            the GATED-and-stale row: CLAUDE.md re-stamped
```

### 1.3 Per-organ verdict: real defect, or the check taxing the batch's own evidence?

```
funnel_coverage        +10  SELF-INFLICTED. Fires on docs/audits/*.md. The ADR-110 batch protocol
                            REQUIRES a manifest, a close packet and one end-of-lane artifact per
                            lane. Nine lanes therefore mint >=11 artifacts, each an automatic WARN
                            until a ledger row is written. The check cannot distinguish "evidence
                            the protocol demanded" from "an audit nobody wanted".

consumer_at_landing     +9  SELF-INFLICTED, AND STRUCTURALLY UNSATISFIABLE BY A LANE. The consumption
                            pool is tasks/, docs/decisions/, docs/intake/, protocols/ + six root docs.
                            It EXPLICITLY EXCLUDES docs/audits/, JOURNAL.md and ecosystem/. A lane
                            close packet's real consumers are the batch close packet (docs/audits/)
                            and the JOURNAL anchor -- both in the excluded set. A lane that does
                            everything right still WARNs. Verified: all 16 live loci have zero
                            pool-surface hits; every citation found is in an excluded path.

doc_rot                 -4  NOT GROWING. 78 -> 74 loci; zero net-new; four cleared by row closures.
                            The pile is INHERITED, not accruing in this window.

undeclared_edges         0  NO CHANGE. All 22 loci (14 dispositioned, 8 not) pre-date the window;
                            the newest source edit is 2026-08-29.

no_ff_merges             0  NO CHANGE. All 3 dispositioned, all 2026-06 history.
fleet_parity             0  NO CHANGE. Both pre-date the window (2026-09-01 VISION relocation).
review_artifact_coverage 0  NO NEW ROWS, but the number INSIDE the aggregate grew -- it is one
                            Finding reporting "95 code-impact merges", and this window added
                            merges to it. Advisory by the [#480] P3 ruling.
adr_status_grammar       0  NO CHANGE. Live measurement still equals the authoring baseline exactly
                            (grammar 47 / coherence 3 / duplicate-id 2 / wrapped-value 1).
canonical_freshness     -1  IMPROVED (the gated row cleared). The two survivors are ungated reports.
generated_artifact_freshness 0  Same row, worse number: 9d -> 11d stale.
journal_spine_anchor     0  Same dispositioned row, different SHAs listed. See §2 B12 for the
                            SEPARATE hard-fail on this organ.
```

**The finding this section exists to deliver:** the window produced **zero new governance or
code defects**. It fixed eight real ones. The +11 is entirely two checks firing on the artifacts
the methodology obliges every lane to write. A drain campaign against those 19 rows would be
work done to satisfy a measurement, not to fix anything.

---

## §2 DECISION BUNDLES — 12 bundles covering all 133

Each bundle is one ruling. Proposal classes: **fix-now** (S, edit named) · **disposition**
(reason) · **defer** (row id) · **false-positive** (why the check is wrong).

### B1 · consumer_at_landing — 15 lane and batch artifacts · PROPOSED: **false-positive**

**Rows:** 15 of the 16 (all but `2026-09-01-technical-article-harness-substrate-brief.md`).
**Why the check is wrong:** the pool that defines "consumed" excludes the only surfaces that
can cite a lane artifact. `consumer_at_landing.POOL_DIRS` is `tasks/`, `docs/decisions/`,
`docs/intake/`, `protocols/`; the docstring deliberately excludes `docs/audits/`, `JOURNAL.md`,
`ecosystem/`, `tests/`, `.claude/`, `templates/`, `deploy/`. A lane close packet is consumed by
its **batch close packet** (`docs/audits/`) and anchored in **JOURNAL.md**. Both excluded. Zero
of the 16 have a pool hit; every citation that exists is in an excluded path.
**Corroborating:** the register carries **no** `consumer_at_landing` entry at all — the organ
has never once been dispositioned, in either direction.
**Named fix if the ruling goes that way:** admit a batch close packet as a consumer (a
`docs/audits/` file whose `closed_by:`/roster names the artifact), **or** require the lane's
`tasks/` row to cite its own end-of-lane artifact — which would make the obligation satisfiable
by the lane that incurs it. Owner: `[#552]` (open) or a new row.

### B2 · consumer_at_landing — the article research brief · PROPOSED: **disposition**

**Row:** `2026-09-01-technical-article-harness-substrate-brief.md`.
**Reason:** an operator-commissioned external research brief landed verbatim with a §0
provenance record. It has no governance consumer *by design* — it feeds an article outside the
hub. This is the case the check's own `no-consumer:` escape exists for; it is genuinely
unconsumed, not mis-measured. Disposition with that reason.

### B3 · funnel_coverage — the 10 net-new batch-G artifacts · PROPOSED: **fix-now (S)**

**Rows:** the 10 listed in §1.1.
**Edit:** one new dated ledger artifact,
`docs/audits/2026-09-05-technical-<slug>.md`, carrying a disposition table with the ruled
columns (file · disposition · evidence locator) and **11 rows** — one per artifact plus one
self-discharging row for the ledger itself. Most are `FILED` against an arc id already named in
the artifact's own header (`[#276]`, `[#611]`, `[#614]`, `[#621]`, `[#626]`, `[#628]`,
`[#629]`/`[#630]`); the batch-G close packet is `ACTIONED` with merge `6ee7c897`.
**Why a new file, not an append:** the existing ledger is
`docs/audits/2026-08-17-technical-audit-disposition-ledger.md` — an audit artifact, and audits
are **immutable** (CLAUDE.md §5 rule 3). The check admits any artifact carrying a
correctly-shaped table, and self-discharge is allowed, so a new dated ledger is the compliant
route. **Flag for the architect:** this means the disposition mechanism mints a new
undispositioned artifact every time it is used unless each ledger self-discharges. That
recursion is a design property worth ruling on explicitly.

### B4 · funnel_coverage — 22 inherited (batch E/F, ATLAS, misc) · PROPOSED: **fix-now (S)**, same act

**Rows:** the other 22 of the 32 — batch-F core (5), batch-F lane packets (4), the ATLAS-R1
cluster (3), the codespace-substrate cluster (2 of 3), the DC-3/ESSENTIALS pair (2), the v7
BOOT-INVERSION pair (1 remaining), and 5 singletons.
**Same edit as B3**, same file, 22 more rows. Separated from B3 only so the architect can rule
"do the new ones, defer the inherited backlog" if the window is short. If both are taken, B3+B4
is one artifact with 33 rows and clears **32 of the 133** in a single act — the largest cheap
win on this sheet.
**Note:** 16 of these 22 have real citations from pool surfaces already (tasks/ rows, intakes,
ARCHITECTURE.md, CLAUDE.md, README.md); they fail `funnel_coverage` only for want of a *ledger
row*, which is a different and stricter predicate than "someone uses this".

### B5 · doc_rot ARM 2 (`backlog-row-length`) — 65 undispositioned · PROPOSED: **false-positive**

**Rows:** 65 of the 69 live loci (4 are already dispositioned: `#546`, `#547`, `#552`, `#533`).
**Why the check is wrong — the ceiling no longer measures what it was calibrated to measure:**

- 1320 was set on 2026-08-15 as the **p90** of the post-conversion distribution, and re-declared
  by `[#532]` on 2026-08-16 as a fixed contract. At that moment ARM 2 fired on **10 rows**.
- Live today: **223 rows in the manifest, 69 over the ceiling — 31%.** 1320 now sits at roughly
  **p69**. Corpus percentiles: p50 1259 · p75 1542 · p90 2210 · p95 2756 · max 5315 (`#628`).
  The median row is 61 chars under the ceiling.

**Why the remedy has been tried and does not hold — twice:**

- `[#536]` was the row that owned this pile. It **closed** at `fce8b5b0` (2026-08-18) on route
  (ii): *"six dispositions cover every live backlog-row-length locus... 6 loci, 6 dispositions,
  and the accretion arm is now at 0 loci."* The same commit records that lane G had trimmed rows
  *"to within 18–30 chars of the ceiling"* — so any later body edit puts them straight back over.
  **18 days later: 69 loci, and only 4 of the 6 dispositions survive.**
- `[#612]` (open) built the ruled archival remedy and ran it at `45ff9a74` (2026-08-29),
  relocating seven rows' bodies and dropping doc_rot 77 → 60. **All seven of those rows —
  `#112`, `#267`, `#277`, `#491`, `#533`, `#555`, `#561` — are over the ceiling again today.**
  The mechanism worked and the measurement returned anyway.

**What the loci actually record:** 17 of the 65 have their last touch at `9fedb07c` (2026-08-28,
*"X1 step 5 — the 45-day icebox sweep (41 rows)"*) — a bulk governance-bookkeeping commit that
appended a `DEFER` clause with a recorded peg to dozens of rows. The rows grew because the
methodology required them to record why they were deferred. Another 8 last-touched at
`d6c77aca`, the intake-birth commit that created them at full length.

**Proposed remedy (the architect's call, not this session's):** stop emitting one WARN per row.
Either (a) re-derive the ceiling with its basis stated and its expected member count named, or
(b) convert ARM 2 to a **corpus-level trend metric** (count + percentile, one Finding) so it
keeps backpressure without minting 65 register-sized obligations. The register's own header
warns against exactly this: dispositions that *"drown the ship gate's disposition register in
rows that share one answer."* `[#536]` is closed and `[#364]` retired — **the pile currently has
no owner**, which was `[#536]`'s original finding, now true again.

### B6 · doc_rot ARM 1 (`backlog-accretion`) — 3 loci · PROPOSED: **defer to `[#612]`**

**Rows:** `#267` (3 dates / 53d), `#297` (3 dates / 51d), `#82` (3 dates / 51d).
**Reason:** this is the genuine ADR-88 FC4 class — real inline history that has accreted over
time — and `[#612]` (open, P2) is its built-and-ruled carrier: byte-identical relocation to
`tasks/archive/<id>.md`. `#267` has already been archived once and re-crossed. Not a
false positive; a real, owned, small piece of work. **Caveat the architect should price:** these
three cross the 30-day span arm by the *calendar*, without any edit — the span grows on its own.

### B7 · doc_rot singletons — grooming-cadence + section-history · PROPOSED: **fix-now (S)**

- `grooming-cadence`: last groom **2026-07-30**, 37d ago, against a 21-day ADR-41 cadence.
  **Edit:** run a groom pass and append its date to the `**Grooming log:**` line in `BACKLOG.md`.
  The checker reads the most recent *past* date on that line; `Next quarterly: 2026-10-08` is
  correctly ignored.
- `section-history`: `protocols/HANDOFF_PROCESS.md#section-history` carries exactly **12**
  entries at the `>= 12` threshold. **Edit:** condense the oldest entries to git per ADR-49/65 —
  the same act CLAUDE.md §12 has performed three times. `HANDOFF_PROCESS.md` is a living spec,
  so this is an ordinary edit, not an immutability problem.

### B8 · undeclared_edges — 8 undispositioned · PROPOSED: **defer to `[#241]`**, and un-defer it

**The 8, disambiguated from the 14 already dispositioned:**
```
README.md                                                    -> handoff-process   (tier 1)
README.md                                                    -> prompt-template   (tier 1)
protocols/OPERATOR-INTERFACE.md                              -> handoff-process   (tier 1)
protocols/STANDING_RULINGS.md                                -> handoff-process   (tier 1)
docs/intake/2026-08-22-tech-document-dependency-graph-organ.md -> handoff-process (tier 1)
docs/intake/2026-08-28-tech-handoff-engine-deployable-carrier.md -> handoff-process (tier 1)
docs/intake/2026-08-26-tech-handoff-operator-interface.md    -> handoff-process   (tier 2)
ecosystem/conformance.md                                     -> handoff-process   (tier 2)
```
**Reason:** `[#241]` "Undeclared-edge groom" is the owner, and its Done-when is already written
generically — *"every id the `undeclared_edges` ship-gate leg surfaces... the predicate reads the
live surfaced set, never a fixed count"* — so it covers all 8 without amendment. It is
`status: deferred`, but the defer is explicitly an **attention decision, not a blocked-by**:
*"Un-defers when an arc claims the row or the operator re-prioritises it."* This window claiming
it is exactly that trigger.
**Two of the 8 have decided precedent and need no adjudication effort:**
- `ecosystem/conformance.md` is a **generated** dashboard and cannot carry hand-authored
  frontmatter — identical shape to the already-dispositioned `docs/intake/README.md` entry
  (*"A GENERATED file cannot carry a hand-authored `reconciled_with`"*).
- `protocols/STANDING_RULINGS.md → handoff-process` fires on a **quoted audit finding** that
  literally contains the string `reconciled_with: handoff-process@6.2.0` while describing a
  *different* file's stale frontmatter. The detector is matching a quotation of its own syntax.
**Stale row hazard to fix in the same pass:** `[#241]`'s prose still describes the original 6
candidates from 2026-07-03; the live set is 22.

### B9 · fleet_parity — 2 rows · PROPOSED: **fix-now (S)**, two one-line declarations

- **`canonical-doc-vision`** — `VISION.md` was relocated to `docs/archive/VISION.md` at the hub
  ([#614] lane-e-5). `ecosystem/parity-surfaces.yaml` already carries the lane's written
  disclosure: *"the hub-role WARN stays live until a `.methodology.yaml` entry for
  `canonical-doc-vision` lands."* **The declaration was written and never landed.**
  **Edit:** add one `sanctioned_divergences` entry for component `canonical-doc-vision` to
  `.dev-knowledge/.methodology.yaml`, with a reason and a `review_date` (the schema requires
  one of `expiry`/`review_date`). Verified absent today: 19 entries, none named that.
- **`claude-commands-roster`** — `.claude/commands/boot-session.md` exists and is declared in
  `deploy/manifest-v1.5.0.yaml` (twice) *and* listed in `.claude/methodology-roster.md`, but the
  parity check reads neither: `_eval_commands_roster` reads only
  `parity-surfaces.yaml`'s `claude-commands-roster.probe.expected_repo`, where `boot-session.md`
  is absent. **Edit:** add `boot-session.md` to that list.
  **Worth a second's thought before ruling:** four separate surfaces declare this repo's
  commands (manifest, methodology-roster, parity-surfaces `expected_repo`, `.methodology.yaml`
  command-* waivers) and nothing keeps them in sync. `[#343]` "fleet_parity ship-gate-only
  scoping" (open, P3) is adjacent.

### B10 · canonical_freshness — 2 aggregate rows · PROPOSED: **1 disposition + 1 defer**

Both rows are **derived reports over ungated files**. The gated set is 8 files
(`canonical_docs.FRESHNESS_FILES` + `audit.py::_HUB_ONLY_FRESHNESS_FILES`) and **all 8 are
fresh**; the gated-and-stale row cleared this window. Neither surviving row is a gate breach.

- **`derived ungated-and-unstamped: 27`** → **disposition.** These 27 files (9 `.claude/commands/`,
  3 plugin docs, 7 `protocols/`, `AGENTS.md`, 2 `deploy/`, etc.) carry no `last_reviewed` stamp
  and are not required to. Reporting them forever as amber, with no contract behind them, is the
  "permanently-amber detector teaches that amber is normal" failure. Disposition with that reason,
  or narrow the derived scope.
- **`derived ungated-and-stale: 3`** → **defer to `[#285]`** (open, P3, *"Extend hub freshness
  gating to PLAYBOOK"*). Of the three, `protocols/PLAYBOOK.md` is the substantive one (declared
  2026-08-01, derived 2026-09-05, +35d) and `[#285]` is precisely its owner.
  `protocols/ENVIRONMENT.md` (+57d) has no owner and may deserve its own row.
  `README.md` is a **same-day ordering artifact**, not staleness: the stamp landed at `96f956528`
  and one content commit followed it on the same date, which a date-only compare cannot see.

### B11 · advisory singletons — 3 rows · PROPOSED: **1 fix-now, 1 defer, 1 disposition**

- **`generated_artifact_freshness` — conformance-dashboard 11d stale (baseline 4d)** →
  **fix-now (S):** `uv run --locked python scripts/gen_dashboard.py --write`, then commit
  `ecosystem/conformance.md` + `ecosystem/conformance.html`.
  **Two hazards to hand whoever takes it:** the generator needs `PYTHONUTF8=1` on this console,
  and regenerating the dashboard is known to RED `export_backlog_view` — a false positive, not
  the lane's fault. The check is WARN-never-FAIL by construction.
- **`review_artifact_coverage` — 95 code-impact merges with no linked review artifact** →
  **defer to `[#499]`.** Advisory by the `[#480]` P3 ruling (closed 2026-08-05), whose hard
  pre-push leg is explicitly deferred behind *"0 false positives over two consecutive windows"*,
  with `[#499]` carrying that bar. `[#560]` (open, P2) additionally reports the check reads only
  the first branch/HEAD triple per file, so a real review can be invisible to it — meaning the
  95 is an **upper bound**, not a count of missing reviews.
  The second `review_artifact_coverage` row (2 artifacts with no parseable `**Tally:**`) is half
  dispositioned: `5af0b33c` is covered; **`584fb1ed → 2026-08-27-codex-lane-na-gates.md` is not**
  and has no register entry. Same class as the dispositioned one (review happened, tally line
  unparseable, file immutable) — one disposition would close it.
- **`adr_status_grammar`** → **disposition.** This is a **ratchet-holding report, not drift.**
  The values are recomputed live every run and today equal the authoring baseline **exactly**
  (89 fields, 0 enum/single-field defects, grammar 47 / coherence 3 / duplicate-id 2 /
  wrapped-value 1). The two FAIL-tier rules measure 0. Nothing has moved since the check was
  written; it WARNs because the corpus could not pass `grammar` at FAIL on day one.

### B12 · window business that is NOT a WARN — 2 stale dispositions + 1 hard fail

Not part of the 133. Included because the dispositioning window is where they belong.

- **The hard-fail organ (this is what makes the gate RED, independent of every WARN):**
  `journal_spine_anchor` — merge `6de676fb` (2026-09-05, *docs/playbook-essentials-routes*)
  carries **no JOURNAL anchor**. The 2026-09-05 (a) entry's `Anchors:` line names `7e7402d5`,
  `7b3ba003`, `7f75033b` — the branch commits — but not the merge commit that wraps them, whose
  SHA did not exist when the line was written. **Fix-now (S):** one anchor line. This is the
  known single-commit/merge-anchor deadlock, and `[#623]` (open, P2) owns mechanizing it.
- **Two `[stale]` register entries:** `warn-edge-lane-rl-registry-filings` and
  `-v2`. Both target files under `docs/audits/`, which
  `scan_undeclared_edges._IMMUTABLE_PREFIXES` skips entirely — so neither can **ever** match a
  live WARN again. The register's own comment already concedes they are *"INERT SINCE
  2026-08-26... belt-and-braces, not active suppressions"* and they were **re-verified and
  deliberately KEPT** on 2026-09-02. **PROPOSED: remove.** ADR-75's decoration rule exists so a
  reader can tell a disposition that holds something from one that holds nothing; a
  permanently-unmatchable entry is the case the rule names. Note `[#557]` closed on this exact
  class (three stale entries) on 2026-08-18 — **the class has recurred**, which argues for
  removal over another keep-and-re-verify.

---

## §3 Counts per proposal class

Over the **133** undispositioned WARNs:

```
false-positive (the check is wrong)      80   B1 (15) + B5 (65)
fix-now (S, edit named)                  37   B3 (10) + B4 (22) + B7 (2) + B9 (2) + B11 gen-artifact (1)
defer (to an existing row)               13   B6 -> [#612] (3) + B8 -> [#241] (8)
                                              + B10 -> [#285] (1) + B11 -> [#499] (1)
disposition (accept with a reason)        3   B2 (1) + B10 unstamped-27 (1) + B11 adr-grammar (1)
                                        ----
                                         133
```

By organ, undispositioned:
```
doc_rot                  70   (65 row-length + 3 accretion + grooming-cadence + section-history)
funnel_coverage          32
consumer_at_landing      16
undeclared_edges          8
canonical_freshness       2
fleet_parity              2
generated_artifact_freshness  1
review_artifact_coverage  1
adr_status_grammar        1
                        ----
                        133
```

**Two rulings move 80 of the 133** (B1 and B5), and both are "fix the check", not work.
**Two more (B3+B4) move 32** in one new ledger artifact. Everything else is 21 rows.

---

## §4 Per-row appendix

### 4.1 `doc_rot` ARM 2 — all 69 loci, longest first

Measured at `6de676fb` by reassembling `tasks/manifest.json` + task blobs and applying
`validate_doc_rot`'s own rule (`len(line)` on `^- \[#\d+\]`). The reconstruction returns 69,
matching the gate exactly. Ceiling 1320.

- `#628` — 5315 chars · P1 · open · last touch 11088e5b 2026-09-01 · `tasks/628-dc2-recut-essentials-dissolution-is-a-release-act.md`
- `#610` — 4961 chars · P2 · open · last touch bf1f2cac 2026-08-29 · `tasks/610-the-night-batch-protocol-named-with-its-two-verb.md`
- `#631` — 3657 chars · P1 · open · last touch b707d50b 2026-09-01 · `tasks/631-a-freeze-cannot-bind-a-rule-that-postdates-it.md`
- `#552` — 3576 chars · P2 · open · last touch aab0e1d7 2026-08-17 · `tasks/552-window-close-disposition-and-archival-routine.md`  [DISPOSITIONED]
- `#632` — 3522 chars · P1 · open · last touch cd80ed66 2026-09-01 · `tasks/632-codespace-is-admitted-for-transport-and-unstable-for-inference.md`
- `#626` — 3235 chars · P2 · open · last touch aa1232d0 2026-09-01 · `tasks/626-logs-retention-exempts-the-prefixes-that-accumulate.md`
- `#627` — 3219 chars · P2 · open · last touch faf9db8d 2026-09-01 · `tasks/627-agy-route-is-inert-no-row-authorizes-analysis-admission.md`
- `#559` — 3104 chars · P2 · open · last touch 7bf20766 2026-08-27 · `tasks/559-kernel-lab-check-tiering-dev-knowledge-kernel-as.md`
- `#244` — 2946 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/244-essence-spec-lifecycle-epic.md`
- `#271` — 2935 chars · P3 · open · last touch a83d4e5a 2026-08-28 · `tasks/271-nightly-proposal-loop.md`
- `#633` — 2827 chars · P2 · open · last touch 33a5c867 2026-09-01 · `tasks/633-boot-session-gains-history-delta-and-equilibrium-map.md`
- `#629` — 2761 chars · P1 · open · last touch f2e120e7 2026-09-01 · `tasks/629-a-contract-amendment-cannot-subtract-an-act.md`
- `#578` — 2711 chars · P3 · open · last touch b45e4146 2026-08-23 · `tasks/578-the-earned-mitigated-rerun-one-slot-role-reminder.md`
- `#619` — 2653 chars · P2 · open · last touch 08029542 2026-08-31 · `tasks/619-the-fm-2-to-fm-4-funnel-health-coupling-is-dead.md`
- `#625` — 2549 chars · P1 · open · last touch fbe70097 2026-08-31 · `tasks/625-the-rule-adherence-eval-corpus-fresh.md`
- `#615` — 2541 chars · P2 · open · last touch 3a4066eb 2026-09-01 · `tasks/615-model-attribution-signature-trailer-on-every.md`
- `#606` — 2402 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/606-the-win-tooling-first-slice-instantiation-arc-ru.md`
- `#618` — 2379 chars · P2 · open · last touch 7f01e51a 2026-08-29 · `tasks/618-the-silently-stale-codespace-clone-detection-and.md`
- `#589` — 2297 chars · P1 · open · last touch 6b256fb9 2026-09-01 · `tasks/589-one-line-per-row-the-backlog-view-projection-wit.md`
- `#561` — 2294 chars · P2 · open · last touch 45ff9a74 2026-08-29 · `tasks/561-re-base-the-compute-plan-onto-the-hetzner-cx-sha.md`
- `#546` — 2227 chars · P3 · open · last touch 77e3147f 2026-08-17 · `tasks/546-adr-60-docs-taxonomy-no-longer-describes-the-tree.md`  [DISPOSITIONED]
- `#609` — 2227 chars · P2 · open · last touch 4cf4de84 2026-08-28 · `tasks/609-free-ruff-ratchet-the-zero-cost-python-standard.md`
- `#617` — 2214 chars · P2 · open · last touch aa1232d0 2026-09-01 · `tasks/617-file-distillation-the-output-half-and-the-only-w.md`
- `#554` — 2193 chars · P2 · open · last touch cd80ed66 2026-09-01 · `tasks/554-devcontainer-provisioning-script-nb4-g-stage-1.md`
- `#267` — 2188 chars · P2 · open · last touch 45ff9a74 2026-08-29 · `tasks/267-scope-exercising-arc-extension.md`
- `#624` — 2172 chars · P2 · open · last touch 08029542 2026-08-31 · `tasks/624-nothing-watches-a-blockers-status.md`
- `#82` — 2110 chars · P3 · deferred · last touch 90adb456 2026-08-28 · `tasks/82-define-per-repository-agentic-review-profiles.md`
- `#547` — 2099 chars · P3 · open · last touch 523411de 2026-08-17 · `tasks/547-split-brain-prevention-has-no-referent-under-v6.md`  [DISPOSITIONED]
- `#533` — 2088 chars · P2 · open · last touch 45ff9a74 2026-08-29 · `tasks/533-decompose-the-audit-py-check-monolith-into-scrip.md`  [DISPOSITIONED]
- `#491` — 2049 chars · P3 · deferred · last touch 45ff9a74 2026-08-29 · `tasks/491-gemini-scanning-lane-ruling-r-g-plus-an-acceptan.md`
- `#607` — 2019 chars · P2 · open · last touch 914dc4aa 2026-08-28 · `tasks/607-playbook-census-discharge-the-mechanical-half-of.md`
- `#269` — 2015 chars · P3 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/269-audit-index-count-tiered-shape-freshness-hook.md`
- `#608` — 2005 chars · P1 · open · last touch 914dc4aa 2026-08-28 · `tasks/608-tiling-aware-journal-read-the-rotation-seam-befo.md`
- `#605` — 1936 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/605-de-hardcode-consumer-root-resolution-in-deploy-t.md`
- `#604` — 1876 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/604-admit-win-tooling-and-terminal-setup-to-the-depl.md`
- `#564` — 1826 chars · P2 · open · last touch b6e2044b 2026-08-20 · `tasks/564-lifecycle-archival-implemented-adrs-and-decided-int.md`
- `#599` — 1825 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/599-generated-standing-vs-new-drift-block-in-the-han.md`
- `#603` — 1802 chars · P3 · open · last touch d6c77aca 2026-08-26 · `tasks/603-an-operator-interface-capability-file-the-facts.md`
- `#602` — 1796 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/602-land-the-ruled-dispatch-verb-in-the-bundle-s-for.md`
- `#567` — 1746 chars · P2 · open · last touch b6e2044b 2026-08-20 · `tasks/567-cx53-daily-driver-substrate-lane-the-every-prompt-r.md`
- `#285` — 1740 chars · P3 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/285-extend-hub-freshness-gating-to-playbook.md`
- `#278` — 1728 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/278-test-suite-hygiene-epic.md`
- `#274` — 1708 chars · P3 · open · last touch aba76527 2026-08-28 · `tasks/274-dogfood-signal-prior-in-the-changelog-review-ado.md`
- `#43` — 1703 chars · P3 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/43-decide.md`
- `#568` — 1671 chars · P2 · open · last touch b6e2044b 2026-08-20 · `tasks/568-provider-config-as-code-dev-knowledge-as-source-of-.md`
- `#534` — 1640 chars · P2 · open · last touch b099f3ff 2026-08-19 · `tasks/534-audit-py-line-locators-on-four-open-rows-died-at-t.md`
- `#600` — 1637 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/600-delete-p10-from-the-shipped-probe-manifest-and-g.md`
- `#241` — 1625 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/241-undeclared-edge-groom.md`
- `#601` — 1605 chars · P2 · open · last touch d6c77aca 2026-08-26 · `tasks/601-supplement-folded-audit-check-a-filled-supplemen.md`
- `#571` — 1602 chars · P2 · open · last touch 80af6da8 2026-08-22 · `tasks/571-define-architecture-described-surface.md`
- `#153` — 1594 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/153-enforcement-completeness-pass.md`
- `#245` — 1569 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/245-add-path-status-awareness.md`
- `#327` — 1566 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/327-protocols-as-interface-genre-ruling.md`
- `#303` — 1558 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/303-make-seed-runbook-py-child-class-aware.md`
- `#623` — 1555 chars · P2 · open · last touch 86bed827 2026-08-29 · `tasks/623-mechanize-the-journal-anchor-record-line.md`
- `#332` — 1545 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/332-fleet-dependency-version-parity.md`
- `#289` — 1538 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/289-hub-own-the-onedrive-blue-yonder-guard.md`
- `#317` — 1499 chars · P2 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/317-default-parallel-test-invocation-slow-tier-marke.md`
- `#549` — 1491 chars · P2 · deferred · last touch 353149ab 2026-08-22 · `tasks/549-fleet-hygiene-plan-of-record-has-no-carrier.md`
- `#234` — 1445 chars · P3 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/234-cross-repo-probe-validator.md`
- `#570` — 1439 chars · P2 · open · last touch 80af6da8 2026-08-22 · `tasks/570-consume-the-tech-adoption-ledger-w-wave.md`
- `#611` — 1407 chars · P2 · open · last touch 4cf4de84 2026-08-28 · `tasks/611-handoff-process-v7-the-minimal-bundle-package.md`
- `#324` — 1407 chars · P3 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/324-phase-6-axis-2-carrier.md`
- `#426` — 1370 chars · P2 · open · last touch 353149ab 2026-08-22 · `tasks/426-declare-consumer-consumption-path-for-every-live.md`
- `#555` — 1364 chars · P1 · open · last touch 45ff9a74 2026-08-29 · `tasks/555-closing-campaign-batch-1-kill-candidates-instrum.md`
- `#277` — 1340 chars · P2 · open · last touch 45ff9a74 2026-08-29 · `tasks/277-propose-closures-signal-repair.md`
- `#548` — 1338 chars · P2 · open · last touch 7bf20766 2026-08-27 · `tasks/548-intake-12-settled-ownership-manifest-has-no-carrier.md`
- `#112` — 1330 chars · P2 · open · last touch 45ff9a74 2026-08-29 · `tasks/112-adr-amend-helper-adr-immutable-zone-extension.md`
- `#297` — 1327 chars · P3 · deferred · last touch 9fedb07c 2026-08-28 · `tasks/297-lightweight-dry-observe-arc-coverage-mode.md`

### 4.2 `doc_rot` — ARM 1 and the two singleton rules

```
backlog-accretion  BACKLOG#267   3 history dates spanning 53d, 2188 chars   tasks/267-scope-exercising-arc-extension.md
backlog-accretion  BACKLOG#297   3 history dates spanning 51d, 1327 chars   tasks/297-lightweight-dry-observe-arc-coverage-mode.md
backlog-accretion  BACKLOG#82    3 history dates spanning 51d, 2110 chars   tasks/82-define-per-repository-agentic-review-profiles.md
grooming-cadence   BACKLOG#grooming-cadence   last groom 2026-07-30, 37d ago (> 21d, ADR-41)   BACKLOG.md grooming-log footer
section-history    protocols/HANDOFF_PROCESS.md#section-history   12 entries (>= 12; condense per ADR-49/65)   last touch f33e1d62 2026-09-04
```

### 4.3 `funnel_coverage` — 32 loci by provenance cluster

Ledger predicate: a row in a `docs/audits/` disposition table naming the file, with a term from
`ACTIONED | FILED | REJECTED | SUPERSEDED` (or `PENDING` + a `Q:` question) and a non-empty
evidence locator. Baseline `ecosystem/audit-funnel-baseline.json` (armed 2026-09-01 at
`13fb1538`; corpus 843 / dispositioned 78 / uncovered 763). All 32 landed after that stamp.

```
Batch G core (2)          2026-09-02-technical-batch-g-manifest.md
                          2026-09-02-technical-batch-g-close-packet.md
Batch G lanes (7)         2026-09-02-technical-lane-g-276-deploy-waiver.md          [#276]
                          2026-09-02-technical-lane-g-611-bundle-thinning.md        [#611]
                          2026-09-02-technical-lane-g-614-hygiene-close-packet.md   [#614]
                          2026-09-02-technical-lane-g-621-freshness-absent.md       [#621]
                          2026-09-03-technical-lane-g-621-c7.md                     [#621], supersedes the above
                          2026-09-02-technical-lane-g-626-terra-tally.md            [#626]
                          2026-09-02-technical-lane-g-628-essentials-debless-packet.md  [#628]
Batch F core (5)          2026-09-01-technical-batch-f-manifest.md
                          2026-09-01-technical-batchf-derivation.md
                          2026-09-01-verification-batchf-integration-suite.md
                          2026-09-01-verification-batchf-terra-tallies.md
                          2026-09-02-technical-batch-f-close-packet.md
Batch F lanes (4)         2026-09-01-technical-629-630-lane-g-packet.md             [#629] [#630]
                          2026-09-01-technical-lane-b-2-handoff-v7-close-packet.md
                          2026-09-01-technical-lane-d-4-deploy-waiver-honoring.md   [#276]
                          2026-09-01-technical-ruff-gate-divergence-classification.md
Batch E (1)               2026-09-01-technical-batch-e-close-packet.md
Codespace substrate (3)   2026-09-01-verification-codespace-admission-report.md     [#632]
                          2026-09-01-verification-codespace-longrun-proof.md        [#632] [#634]
                          2026-09-02-verification-parity-b5753f52.md                [#632]
ATLAS-R1 (3)              2026-09-01-census-atlas-r1-def-usage-ledger.md
                          2026-09-01-technical-atlas-r1-layer-graph.md
                          2026-09-01-verification-atlas-r1-harvest-attempt.md
DC-3 / ESSENTIALS (2)     2026-09-01-technical-dc3-split.md
                          2026-09-01-technical-act-one-preserved.md                 [#628]
v7 BOOT-INVERSION (2)     2026-09-01-technical-boot-r1-prioritization-scheduling.md [#611]
                          2026-09-01-technical-v7-history-delta-equilibrium-map.md  [#633]
Singletons (3)            2026-09-01-technical-agy-admission-verdict.md             [#627]
                          2026-09-01-technical-article-harness-substrate-brief.md
                          2026-09-01-verification-model-routing-witness.md          [#615] [#631]
```

### 4.4 `consumer_at_landing` — 16 loci, all a strict subset of §4.3

All 16 are in the `funnel_coverage` set; there are no `consumer_at_landing`-only rows. The 16
are the seven batch-G lane packets, the two batch-G core artifacts, the four batch-F lane
packets, the two batch-F verification artifacts, and the article brief. Every one has **zero**
citations from a pool surface; every citation found sits in `docs/audits/`, `JOURNAL.md`,
`ecosystem/.dev-knowledge/state.yaml` (the check's own cached WARN text), or `tests/`.

### 4.5 `undeclared_edges` — the 8 undispositioned

Listed with prose evidence in B8. The remaining 14 are dispositioned under `ref: #241` and are
not this window's business unless the architect re-opens the class.

---

## §5 Honest limits

1. **The inventory is a snapshot at `6de676fb`.** Main advanced at least twice during this
   session. Counts may differ by a row or two on re-run; no bundle's shape depends on that.
2. **Nothing here is a verdict.** Every "PROPOSED" is a recommendation from evidence, not a
   ruling. Two proposals — B1 and B5, covering 80 of the 133 — assert that a **check is wrong**.
   That is the strongest claim on this sheet and the one that most deserves argument.
3. **Sub-agent shell access was blocked.** All five retrieval agents inherited this session's
   worktree-isolation guard and could not run `git`. Every git-derived fact in this sheet
   (measurements, anchors, commit attributions, the two historical gate runs) was produced by
   this session directly. Retrieval agents contributed file content, code reading and citation
   searches only.
4. **The B5 corpus percentiles** were computed against the 223-row manifest at `6de676fb`. A
   concurrent session filed `[#634]` during the window; a re-measure may show 224.
5. **Two probe worktrees were created and removed**, and their removal verified. The
   provision→cleanup round-trip left the tree identical (CLAUDE.md §5 rule 9). One retrieval
   agent briefly wrote a scratch file into the shared checkout and deleted it; independently
   verified absent.
</content>
