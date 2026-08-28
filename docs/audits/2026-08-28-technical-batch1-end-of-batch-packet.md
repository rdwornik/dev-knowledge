---
batch: 1
closes: docs/audits/2026-08-28-technical-batch-1-manifest.md
---

# BATCH-1 END-OF-BATCH PACKET - 2026-08-28 - SEQ 2 - ADR-110 shape

**Consumer:** `docs/audits/2026-08-28-technical-batch-1-manifest.md` (this packet is its
declared `closed_by:`, so landing it expires the batch's integration-arc exemption), plus the
rows the lanes serve: `[#577]`, `[#584]`, `[#608]`, `[#613]`, `[#491]`/`[#492]`.

**Shape:** ONE plan -> 5 file-disjoint lanes -> ONE serial integration. Operator gated at
exactly two points: **GO** at dispatch, **this packet** at close.

## 1. Per-lane MET / NOT-MET

### L1 - [#577]+[#584] root AGENTS.md + the section-10 lockstep - **MET**

| done-contract item | verdict |
|---|---|
| 1. section 10 no longer carries the false anti-pattern; region mechanism verified, not eyeballed | **MET** - region body **1,075 B == template 1,075 B**; `boundary_headers.py --check` clean |
| 2. Root `AGENTS.md` per ADR-115's ruled shape; `CLAUDE.md` references it truthfully | **MET** - 107 lines (bound <=120), 5,539 B; the `~/.codex` collision resolved BY SCOPE in the header incl. the `codex/` third layer; section 2 carries the bullet + the thin `@AGENTS.md` **importer** |
| 3. `CLAUDE.md` budget measured before AND after; within ceiling | **MET** - **197/200 -> 196/200, headroom 4**, bought by condensing v2.65-v2.67 to git per ADR-49/65, not shaved |
| 4. RATCHET clause: delta measured pre-edit | **MET - delta ZERO (443 -> 443)** |
| 5. Terra review persisted, tally in body; commit-and-STOP | **MET** - critical=0 high=2 |

**NOT taken, named rather than left to be discovered:** `[#577]`'s done-when also asks for a
**test** asserting the combined global+root payload in **bytes** against the 32 KiB cap.
`tests/` is outside L1's frozen write-scope. The payload is **measured** (9,430 B = **28.8%**
of the cap) but **unguarded by a gate**, so **`[#577]` is not fully discharged.** Terra reached
the same conclusion independently (its HIGH-2), which raises it from a footnote to a
corroborated finding. Filed as candidate C-A.

### L2 - [#608] the rotation seam, SEAM ONLY - **MET**

| done-contract item | verdict |
|---|---|
| 1. Seam lands with ZERO bytes of content moved; mechanism check green | **MET** - byte-identity pinned by test; zero journal content moved |
| 2. If the seam required moving content: STOP | **N/A** - it did not |
| 3. Terra review, tally in body; commit-and-STOP | **MET** - critical=0 high=2 |

### L3 - SDA-1 fan-out acceptance + provider preflights - **NOT-MET (preconditions failed)**

**This is the contract's own conditional path, not a lane failure.** Step 3 reads *"Q0-Q7
preconditions hold or the run does not start."* They did not hold, so it did not start.

| done-contract item | verdict |
|---|---|
| 1. SDA-1 artifact persisted verbatim | **NOT-MET - the artifact does not exist on this machine.** Searched the prompts dir, `docs/`, the tree; the only occurrence of the token anywhere reachable is **inside the batch contract itself**. No cloud provenance, no receipt id |
| 2. Preflight table complete for all four providers | **MET** - complete, and three of four are blocked |
| 3-4. Fan-out matrix with UNCALIBRATED/VACUOUS/EXHAUSTED discipline | **NOT-MET - not started**, per item 1 plus the transport blockers |
| candidate filings handed to the integrator | **MET** - five, two discovered by this lane |
| terra review; commit-and-STOP | **MET** - critical=0 high=1, fixed |

**The lane did not synthesise the missing artifact**, and the reason is its own subject matter:
L3 exists to measure whether fan-out heads fabricate. Writing a plausible adversarial artifact
from the contract's summary of it would be exactly the failure the fan-out scar records.
**Terra was pointed at that question directly and found the stop contract-conformant with no
fabrication.**

Provider transports, probed live (receipts embedded in the lane artifact):

| provider | state |
|---|---|
| Kimi | **ABSENT** - not on PATH |
| GLM | **BROKEN - the file on PATH is HTML** (`<!DOCTYPE html>`), a failed download that **exits rc=0** while erroring. Worse than absent: a harness testing callability by exit code reads it as healthy |
| DeepSeek | **ABSENT** - consistent with ADR-115 section 2.1 "not viable today" |
| agy | **PRESENT** (1.1.21) |

**Q2 served-id (C-9): FAIL on the one live transport.** The `agy` JSON envelope carries
conversation_id, status, response, duration_seconds, num_turns and usage - and **no model
identifier of any kind**. Found **before** 71 items were spent, which is precisely what the
preflight step was inserted to achieve.

### L4 - I-DOC first slice, ARCHITECTURE per W2/D5 - **MET (narrow, and reported narrow)**

| done-contract item | verdict |
|---|---|
| 1. Slice matches W2/D5 as written | **MET** - two machine-computed rosters became pointers |
| 2. Nothing deleted without an in-ruling basis; named destination | **MET** - terra confirmed both removals authorized with resolvable destinations |
| 3. `last_reviewed` updated; doc gates green | **MET** |
| 4. Terra review; commit-and-STOP | **MET** - **critical=0 high=0 medium=0 low=0**, the batch's only clean review |

**Honest size:** 7 insertions / 6 deletions. W2/D5's own limit is that it *sets a direction and
diets no file*, and the operator's P1 rule forbids unasked deletion - so the authorized slice is
genuinely small and is reported small rather than padded. Chapter 2's Organ map **stays**: it
uniquely carries **how each organ fails**, a column `ecosystem/organ-index.md` does not compute
and its own header says it cannot carry.

### L5 - [#613] in-repo routing table + L0 agreement check - **MET**

| done-contract item | verdict |
|---|---|
| 1. `ecosystem/routing-table.yaml` carries the table + the fabricated-count scar as the REASON | **MET** |
| 2. Agreement check, [#592]-shaped, registered; FAILs (never skips - Z-G4); named report when L0 absent | **MET**, at **ship tier** - see section 5 |
| 3. "Ratchet untouched (verified, not assumed)" | **CONTRACT DEFECT - see D1.** The claim is false; the outcome was held to **delta 0** by authoring the file token-free |
| 4. Terra review; commit-and-STOP | **MET** - critical=0 high=2 |

## 2. Merge SHAs and teardown proofs

Merge order as frozen: **L2 -> L1 -> L4 -> L5 -> L3**, `--no-ff`, one at a time, from the
primary checkout.

| # | lane | lane tip | merge commit |
|---|---|---|---|
| 1 | L2 | c52c5daa | 0b08c3e1 |
| 2 | L1 | 43c18e9f | f3d3d96a |
| 3 | L4 | c24c949a | 899c95c5 |
| 4 | L5 | 09fd7a00 | 85f3e71c |
| 5 | L3 | ea6312c9 | bfc815be |

Dispatch and repair arcs: 5916b362 (manifest at dispatch) -> a312ae43; 11af32db / 3f49043d
(manifest re-filed at the glob-matching path + the dispatch anchors) -> bc311d11; b4e73ea2
(manifest schema) -> its merge. Integration arc: c0ca7c2c (regenerated surfaces) plus this
packet and the JOURNAL entry naming it.

Teardown proofs are recorded in section 11 after the fact, not predicted here.

## 3. Terra tallies - five lanes, five reviews

| lane | critical | high | medium | low | outcome |
|---|---:|---:|---:|---:|---|
| L1 | 0 | 2 | 0 | 0 | HIGH-1 refuted on ADR-115 section 3.2's own text, citation added; HIGH-2 accepted -> candidate |
| L2 | 0 | 2 | 0 | 0 | **HIGH-2 FIXED + test**; HIGH-1 accepted as a documented limit -> candidate |
| L3 | 0 | 1 | 0 | 0 | **FIXED** - verdict word removed, grep returns 0 |
| L4 | 0 | 0 | 0 | 0 | clean |
| L5 | 0 | 2 | 0 | 0 | **HIGH-2 FIXED + test**; HIGH-1 answered against the contract's own text |
| **total** | **0** | **7** | **0** | **0** | **3 fixed in-lane, 4 adjudicated with reasons** |

**No lane merged without a review**, per the contract's rule that absence of a review means the
lane does not merge. Zero criticals across the batch.

**Reviewer-harness note, because it cost four attempts and every later lane reused the fix.**
The first three L1 invocations produced no usable verdict:

1. a prompt naming the diff without supplying it sent terra reading the repo - 323 KB of
   output, a PowerShell quoting error, no verdict;
2. supplying a **filled** example tally produced exactly that line back with zero findings - a
   **vacuous pass**, which is the failure class this repo already names for validators run with
   no args. It was rejected rather than banked;
3. a ~21 KB prompt passed via **argv** returned empty - the same class as the recorded
   `claude -p` argv-corruption gotcha; and `nohup ... &` under the harness was reaped before
   codex finished.

**The shape that works:** prompt on **stdin** (`codex exec ... -`), the diff inline, exploration
explicitly forbidden, an output contract with **placeholders rather than filled examples**, run
**synchronously**. Recorded here because it is reusable and cost real time to find.

## 4. Contract defects - three, all found at dispatch by preflight rather than by a lane at commit time

- **D1 - L5's "Ratchet untouched ... verified, not assumed" is FALSE.**
  `silent_rule_detector._SCOPE_RULES` carries `("ecosystem", False, (".yaml",))`, so
  `ecosystem/routing-table.yaml` lands **inside** a ratchet with **zero headroom**.
  **Proved by measurement, not argument:** with the table staged the detector's file count moves
  **60 -> 61**, and the count held at **443 = 443** only because the file was authored with
  **zero** must/shall/never occurrences. In ordinary normative prose it would have RED
  `audit-health` and blocked the commit.
- **D2 - L2 cites the wrong row.** The contract names `[#587]` for the tiling seam; `[#587]` is
  the anchor-check **single-pass inversion**, and the seam is **`[#608]`**, whose body carries
  the contract's own words verbatim (X5/C3, "moves zero bytes"). `[#608]` further carries
  `depends-on: "#587"`, and **`[#587]` is still open**, so the dependency is unmet. Resolved per
  CLAUDE.md **M1**; both facts reported rather than one silently chosen.
- **D3 - the frozen contract is REFUSED by `check_substrate_declaration`.**
  `validate_substrate.declared_substrate()` reads `**Shape:**` **first** as the generator's
  machine-produced field; the contract uses `**Shape:**` for batch topology ("ONE plan -> 5
  lanes"), so the parser takes the value `one` and refuses it as outside the registry. The
  contract **does** declare LOCAL. Recorded as a **visible REFUSE -> WARN deviation carrying its
  reason** - `_apply_override` never removes a refusal - and filed as candidate C-F.

## 5. Decided under budget, that an architect would want to have been asked

- **L5's check is registered at SHIP tier, not COMMIT tier.** `[#592]`'s arming bar is *"measured
  before arming ... 0 findings, so the FAIL leg cannot RED a clean tree."* This organ **does not
  clear it**: the live L0 copy **diverges on all four roles today**, because the derived copy has
  never been written and writing it is the operator's act this lane may not take. A COMMIT-tier
  FAIL would wedge **every commit in the repository** on a file the repository may not write.
  The verdict stays fail-on-divergence / warn-on-absent - never `unavailable`, which
  `_check_outcome` projects onto pass (Z-G4). **OPERATOR ACTION ITEM: derive
  `~/.claude/ROUTING.md` from `ecosystem/routing-table.yaml`, after which this check goes green
  and could be promoted to commit tier.**
- **L1's ratchet pre-authorization went UNUSED.** The grant was bounded to the measured
  section-10 correction delta; the delta was **zero**, because the replacement bullet was
  authored token-free. Worth recording: `validate_transition` refuses a baseline **raise** in
  code regardless of operator authorization, so the grant could not have been spent as written.
- **L3 stopped rather than fabricating**, and **L4's slice is deliberately small** - both covered
  in section 1 with their reasons.
- **The dispatch manifest was filed wrong twice**, and both failures were **silent** - section 7.

## 6. Filing wave (Z-G1 applied) - CANDIDATEs recorded, no rows born

Per Z-G1 a **raw finding is not past triage**: the only route is CANDIDATE -> intake (ADR-98)
-> ratification. **Nothing below is a birth. The ledger is untouched and no `tasks/` row was
added or removed by this batch.**

The two standing ones the contract named:

- **CANDIDATE - ratchet zero-headroom freeze on `protocols/`** (the 7a FLAG; raw finding). This
  batch is fresh evidence rather than a restatement: **two** lanes (L1, L5) had to author around
  a baseline with zero headroom, and L5's own contract asserted the constraint did not apply to
  it.
- **CANDIDATE - cloud-container `uv` 0.8.17 against the pin `==0.11.19`**, under which hub gates
  are silently unrunnable on the Dispatch-Cloud rung (sol session, measured). This is what made
  every lane in this batch route LOCAL.

Handed up by L3:

- **C-B** producer-pack prerequisites (C-1 rejection-tax cost model, C-6 adversarial suite,
  C-15 load-bearing list).
- **C-C** corpus rotation (C-13) - ground truth never committed alongside the items.
- **C-D** **served-id reporting as an admission precondition.** A transport that cannot report
  which model served a round hits C-9's ceiling, so it decides whether a provider is evaluable
  at all. Measure it at admission, not at pack time.
- **C-E** **a transport-health preflight that does not trust exit codes.** The GLM witness: an
  HTML file on PATH exiting 0.
- **C-G** **locate or re-commission SDA-1.** The contract treats it as existing and as L3's
  frame. Either it is unreachable from this host and needs a locator recorded, or it was never
  produced and the contract's basis clause is unfounded.

Discovered by the batch itself:

- **C-A** `[#577]`'s byte-cap test (L1, corroborated by terra) - `[#577]` does not fully
  discharge without it.
- **C-F** `**Shape:**` is ambiguous between substrate-shape and batch-shape (D3). A
  hand-authored contract has no way to know the token is reserved by a gate.
- **C-H** a declared **tile manifest** for journal rotation (L2 HIGH-1) - a deleted legacy tile
  is undetectable without one, shrinking the anchoring universe into a false gap.
- **C-I** `journal_spine_anchor`'s **664+ "anchored by mention, not by record"** WARNs - the
  advisory backlog this batch's own entries were deliberately written against, each carrying an
  explicit `Anchors:` line.

## 7. The batch's most expensive lesson - a malformed manifest fails SILENTLY

The batch manifest was filed **wrong twice**, and neither failure announced itself:

1. **Wrong path.** It went to
   `docs/audits/2026-08-28-technical-batch1-launch-contracts/MANIFEST.md`, while
   `batch_manifest.MANIFEST_GLOB` is `docs/audits/*-batch-*-manifest.md`. `open_batches()`
   returned empty and the manifest **granted nothing at all**.
2. **Wrong schema.** `batch:` held the descriptive `batch-1-2026-08-28`, while
   `test_the_live_repos_own_manifest_is_well_formed` asserts `b.batch.isdigit()`.

And the assumption underneath both was **also wrong**: `exempt()` covers only merges whose
branch matches `LANE_BRANCH_RE`, so a `docs/`-class **dispatch or integration** arc is **never**
exempt and anchors in `JOURNAL.md` like any other arc.

The symptom surfaced far from the cause - `journal_spine_anchor` FAILing inside **lane L1's**
pre-commit hook, blocking a commit that had nothing to do with the manifest. Because
`audit-health` is a **pre-commit** gate rather than a push-time one, one malformed manifest
blocks **every commit in every lane**. Both defects are now recorded **inside the manifest
itself**, so the next author meets them before repeating them.

## 8. The two numbers, counted separately ([#505] clause 2)

- **operator <-> integration: 2.** The **GO** at dispatch (carrying the substrate self-check
  order and the L1 ratchet pre-authorization), and **this packet** at close. **Target 2. Met.**
- **operator <-> lane: 0 escalations.** No ask-class (a)-(c) round-trip was spent. Every fork -
  L1's write-scope question, L2's mis-cited row, L3's missing basis artifact, L5's false ratchet
  claim, and the ship-tier decision - was decided per contract defaults and reported here rather
  than budgeted away. **Target <=1. Met.**

## 9. Process-lane cap - reported, per the protocol's own instruction

The cap (*from batch 2 onward, at most one quarter of a batch's lanes target methodology or
hub-process surfaces*) is **not yet binding on batch 1**, but the shortfall is reported because
the protocol requires a batch that cannot fill its non-process lanes to say so:

> **5 of 5 lanes are process/methodology lanes.** L3 is the closest to product work and it is an
> acceptance instrument, not product. **Dispatched width 5, close width 5, delta 0.**

Batch 2 inherits a real constraint here: under the cap it may run at most one process lane in
four, and this repo's open work is overwhelmingly process-shaped.

## 10. Suite and gates - measured, and every failure attributed

**Full suite, once on the merged result** (the refuse-to-finish item): **6 failed, 4274 passed,
3 skipped, 1 xfailed** in 30m41s. The first run measured **15 failed / 4265 passed**; the
difference is the seven failures this batch caused, all **fixed rather than dispositioned**.

**Caused by the batch (7) - FIXED:**

| failure | cause | fix |
|---|---|---|
| 5 x `assert 53 == 52` | `[#613]` registered `check_routing_agreement`, moving ALL_CHECKS 52 -> 53 | five hardcoded pins bumped with provenance notes |
| `test_check_order_still_agrees_with_all_checks` | CHECK_ORDER must mirror ALL_CHECKS **order**, not alphabetical - the first attempt placed it alphabetically | repositioned immediately before `check_dispatch_drift` |
| `test_check_fleet_parity_green_on_live_repo` | L1's root `AGENTS.md` was a tracked top-level entry in **no parity template** | `root-agents-md` added at `{hub: MUST, consumer: LOCAL}` |
| `test_the_live_corpus_measures_and_the_baseline_matches_it` | the batch landed 9 `docs/audits/` artifacts | baseline regenerated via the sanctioned `--write-baseline` |

Two further reds (`generated_artifact_freshness_is_registered`, a `reverse_dep_oracle` headline)
were collateral of the count pin and went green with it.

**Pre-existing (5) - PROVEN, not assumed.** Measured on a **detached worktree at pre-batch main
`ac1c69b9`**, all five failing there identically:

`test_no_gate_hook_or_script_reads_the_export` - `test_anchor_gate_probe_distinguishes_installed_from_absent` -
`test_committed_baseline_agrees_with_a_live_measurement` (funnel_coverage) -
`test_live_corpus_has_no_accretion_arm_findings_only_length_findings` (doc_rot) -
`test_live_report_renders_the_real_fleet` (desired_state_report).

**One xdist flake (1), proven green serially.** `test_reverse_dep_oracle` reds under `-n auto`
(`assert 3 >= 50`) and the whole module **passes 21/21 with `-n 0`** on this same tree. It is the
recorded *measuring-while-measuring* class - the oracle counting while other workers are also
scanning - not a defect this batch introduced.

**The attribution method is worth keeping, because one failure lied about its provenance.**
`test_live_report_renders_the_real_fleet` looked like a regression: it FAILED on the merged tree
and **SKIPPED** at baseline. The skip was `importorskip("pandas")` - the baseline worktree's venv
lacked pandas. Re-run at baseline with `--group analytics`, it fails **identically**. Had the
skip been read as a pass, this batch would have owned a defect it did not cause. That is exactly
the failure mode **Z-G4** was ruled against this same session: *a skip is indistinguishable from
a pass in every summary line anyone reads*, and it goes absent precisely where it is needed.
Filed as candidate C-J.

**Gate state:** `uv run --locked python scripts/audit.py health` reports **OK** on the merged
result. The ship-gate WARN frame is unchanged from the standing set (`journal_spine_anchor`'s
664+ anchored-by-mention advisories, `adr_status_grammar`'s recorded baseline,
`consumer_at_landing`'s ratchet), plus the newly-declared `routing_agreement` **fail** on L0
divergence, which is a real operator action item rather than a regression - see section 5.

## 11. Refuse-to-finish checklist (ADR-110 section 3, five items)

| item | state |
|---|---|
| every lane branch merged-or-explicitly-abandoned | **5 of 5 merged**, none abandoned |
| full suite run once on the merged result | **run twice** - once as the batch requires, once to confirm the carried fixes; both recorded above |
| `git worktree list` == primary only | see the teardown record in the JOURNAL entry that anchors this packet |
| manifest/packet archived - both halves | **manifest at dispatch** (re-filed at the glob-matching path once its silence was found), **this packet** at close |
| `git stash list` empty | **empty** - checked at each lane's STOP and at close |

## 12. What batch-1 actually proved about the machinery

The lanes did their work, and the batch also produced evidence about the batch protocol itself:

1. **A malformed manifest fails silently, twice over** - wrong path and wrong schema, each
   granting nothing while looking correct. The symptom appeared inside an unrelated lane's
   pre-commit hook. Now recorded in the manifest itself.
2. **The exemption is narrower than it reads.** `exempt()` covers only `worktree-lane-*` merges;
   dispatch and integration arcs anchor like any other arc.
3. **A skip can impersonate a pass across a baseline comparison** (section 10).
4. **A reviewer harness can return a vacuous pass** - a filled example tally came back verbatim
   with zero findings, and was rejected rather than banked (section 3).
5. **A contract can name a path a gate refuses, a row that does not exist, and a constraint that
   does not hold** - D1, D2, D3, all three found by preflight before a lane paid for them.
