# BATCH E — HERMETIZATION · THE DERIVED PLAN, for the architect's cut

> **Status: DERIVED, NOT FROZEN.** Tier (A) is dispatched and needs no cut (operator
> instruction). **Nothing else below is frozen.** No lane contract in §5 has been written to the
> prompts dir, no worktree provisioned, no manifest committed. The cut turns §5 into contracts.
>
> **Derived from LIVE state** at `ec8731a9` (main, clean, zero live worktrees at start):
> `tasks/` serialize-groups · the decision tree's 55 leaves · `ecosystem/north-star.md` ·
> the batch-D ESSENTIALS census · `scripts/validate_substrate.py` · `scripts/batch_manifest.py` ·
> `CLAUDE.md` boundary markers · `ecosystem/provider-registry.yaml`.
>
> **Formatting:** flat by design — no pipe tables — so the whole file can be copied into browser
> chat without the TUI painting border glyphs (`CLAUDE.md` §4, output-formatting).

---

## 1 · TIER (A) — DISPATCHED. Record, not proposal.

Seven cloud censuses, dispatched 2026-08-31 16:44–16:50 CEST via `Dispatch-CloudV2`
(DispatchHelpers v1.5.0). **7 of 7 returned `Ok=True` and `Bound=True`** — G1 CREATED, G2 BOUND
to `git_repository https://github.com/rdwornik/dev-knowledge @ main`, G3 RECEIPT echoed. Zero
failures. Model `claude-opus-5`, env `env_01MJCy4htNWTZL8Tn2PMRoEU`,
permission-mode `bypassPermissions`.

Contracts as dispatched are landed beside this file. Receipts:
`~/Downloads/BATCH-E-A-DISPATCH-RECEIPTS-2026-08-31.txt`.

```
A1  batch-e-a1-single-file-folder-census        session_01U9wkpZncq9GMf6S54CwUUm
A2  batch-e-a2-templates-consumer-census        session_01NBnDtWhQGwVqFtvcqrwVhG
A3  batch-e-a3-stale-doctrine-reference-census  session_01BxXjpYNAzow4Qj4KDY3mXN
A4  batch-e-a4-doc-freshness-derivation-audit   session_01Pj8no7mTqTneUZVmRxGe2m
A5  batch-e-a5-harness-portability-map          session_018bwHzUJuxV4pCEd59jf3TS
A6  batch-e-a6-langgraph-class-rejection-record session_01N8WRkWp8dyqipeKpxZFzWZ
A7  batch-e-a7-agy-admission-and-quota-visibility session_0161NBLfKDSitbRmTbZtQ3oq
```

All seven are **read-only by contract**: write-scope NONE, zero commits, zero rows, no gate run
and none asserted. Output returns by `Harvest-Cloud` (alias of `Save-CloudSessionReport`).

**Two contracts departed from the brief, deliberately and on the record:**

- **A1's subject was re-derived.** The brief says *"conflict/ single-file-folder consumer
  census"*. **`conflict/` does not exist** — zero tracked files under it in the hub, absent from
  all six sibling fleet repos on this host, and no tracked `.md`/`.py`/`.yaml` cites it as a
  path. The subject was re-pointed to Z-G5's actual discipline (*"No single-file folders,
  ever"*) over the whole tracked tree: **44 tracked single-file directories** at freeze. The
  contract carries the refutation in its own body so the lane cannot silently re-invent a subject.
- **A5, A6 and A7 record CLOUD as a parallelism choice, not a sizing verdict.** Each fits the
  213,225-token payload ceiling comfortably. Manufacturing a sizing argument for them would have
  been a lie in a frozen contract; the operator instruction ("dispatch FIRST, all in parallel,
  zero local load") is the real reason and is what each contract states.

---

## 2 · PREREQUISITES — 0a / 0b / 0c, as measured

### 0a · TEARDOWN ENUM = LANE ENUM — the defect is real, and it is worse than "one predicate"

**Mechanically confirmed.** `scripts/batch_manifest.py` imports `LANE_BRANCH_RE` from
`validate_branch_naming` and it is `^worktree-lane-[a-z0-9]+(?:-[a-z0-9]+)*$`. The ADR-110
declared-integration-arc exemption requires BOTH an open committed manifest AND a merge of a
branch matching that regex. **`claude/<slug>` cloud lanes and codespace lanes can never match
it**, however correct the manifest is. Batch E dispatches on three substrates; two of them fall
outside the enum entirely. ADR-116 stranded on `claude/lane-f` is the witness the brief cites,
and it is accurate.

**CORRECTION — it is predicate FIVE, not six.** `scripts/validate_substrate.py` carries **four**
legs today, not five:

```
1  substrate-no-live-verb             REFUSE
2  substrate-cloud-gate-dependent     REFUSE
3  substrate-offmachine-operator-path REFUSE
4  substrate-second-local-writer      WARN
```

So the teardown-enum predicate lands as **#5**. Recorded rather than silently renumbered.

**Second correction.** `[#591]` is an **open** row, but its validator **exists and runs** — it is
a pre-commit hook (`lane-contract-check` is the sibling shape gate; `validate_substrate.py` is
the substrate layer). 0a therefore **extends a built organ**, not a planned one, and `[#591]`
may be partially discharged. Verify the row against the module before funding it as new work.

### 0b · THE SIX BASELINE-DRIFT REDS — MEASURED

Full suite, `uv run --locked pytest -q --tb=line -p no:randomly`, run in the batch-E worktree at
`de909ca5`:

```
28 failed · 4,605 passed · 11 skipped · 1 xfailed · 842.30s (14:02)
```

**THE BRIEF'S "SIX" IS CONFIRMED — six drift FAMILIES across nine tests.** The other 19 REDs are
environment or worktree artefacts and are **not** drift; a re-stamp that counted them would be
re-stamping against where the suite ran.

**Genuine drift — six families, each with its measured delta and its own remedy:**

```
D1 test_validate_adr_status (4 tests)  <- the brief's "ADR count after ADR-116", CONFIRMED
     live ADR count moved; grammar distribution G1 42 vs baseline 41 (+1);
     coherence divergences {grammar 47, wrapped-value 1, duplicate-id 2, ...} vs the
     three measured; check reports "89 ADR status field(s)" against an expected
     "coherence=3".  REMEDY: re-measure the Step-1 baseline, record the delta.
D2 test_funnel_coverage::test_committed_baseline_agrees_with_a_live_measurement
     RATCHET 1 of the brief's two.  REMEDY: re-commit the funnel baseline.
D3 test_validate_doc_rot::test_live_corpus_has_no_accretion_arm_findings_only_length_findings
     RATCHET 2 of the brief's two.  REMEDY: re-measure; doc_rot floors at 59.
D4 test_consumer_at_landing::test_the_live_corpus_measures_and_the_baseline_matches_it
     live corpus vs baseline; names the 2026-08-29 claude-md-regenre audit.
D5 test_preflight_freeze_predicates::test_vi_batch1_reproduces_the_wrong_id_citation
     ['[#577]','[#584]','[#587]'] vs expected ['[#587]'] (+2).
D6 test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export
     "the export is read by governance: ecosystem/conformance.htm..." -- a KNOWN
     false positive of dashboard regeneration, not this batch. Verify before re-stamping.
```

**Not drift — subtract all 19 before any re-stamp:**

```
17  tests/test_fleet_analytics.py   ModuleNotFoundError: No module named 'pandas'
                                    -> needs `--group analytics`; a worktree lacks it
 1  test_stale_worktrees::test_linked_worktrees_reader_excludes_the_primary
                                    -> REDs *because* a worktree is live. Structural.
 1  test_enforcement_coverage::test_anchor_gate_probe_distinguishes_installed_from_absent
                                    -> known RED on main; not this batch.
```

**HONEST LIMIT ON THIS MEASUREMENT, stated rather than buried.** It was taken **after** this
session's two commits, which added `docs/audits/2026-08-31-technical-batche-launch-contracts/`
(eight files) and regenerated the audits index. New audit files are exactly what moves D2, D3 and
D4. **So these deltas include this session's own contribution and are NOT the clean pre-batch
baseline the brief asks for.** The integrator's opening act should re-measure at `main` before
`de909ca5` merges, or subtract this commit's contribution explicitly. **Never re-stamp silently**
— the delta is the record.

### 0c · MANIFEST CARRIES `closed_by:`

Confirmed as a hard mechanic, not a convention: `batch_manifest.open_batches` requires **all
four** of — manifest TRACKED by git, `status: open`, a `closed_by:` whose *shape can resolve*
(`_valid_closer`), and that path **absent** from the tree. A manifest with no `closed_by:`
**opens nothing at all**; an unresolvable `closed_by:` is a non-expiring exemption and is
refused. Inline comments are stripped. The batch-E manifest must carry it at dispatch or the
exemption grants nothing.

The 11 structural census WARNs clearing on merge commits is **carried from the brief unverified**
— see U-12.

---

## 3 · REFUTED AND UNVERIFIED PREMISES — the cut needs these first

Numbered so the cut can answer by number.

**U-1 · TWO FLEET DEPLOYMENT ORDERS ARE NOW ON THE RECORD, AND THEY DISAGREE.**
DC-1 states a ruled order: `hub -> monorepo -> ai-council -> win-tooling`. The operator's
2026-08-31 `.CLAUDE GOVERNANCE MODEL` filing states:
`batch E -> engine ratification -> win-tooling full cycle -> monorepo -> ai-council`.
**win-tooling moves from LAST to FIRST.** The payloads differ (VISION->README carrier vs the
`.CLAUDE` governance corpus), so both may be correct — but running two fleet orders inside one
batch is a coordination hazard. **Both are recorded and labelled; neither was overridden.**
Landed as the amendment to intake #62 and as the `sequence` field on the DEPLOYMENT WAVE arc.
**This is the highest-value single cut in the batch.**

**U-2 · "predicate six" is predicate five.** See 0a. No judgment needed, just renumbering.

**U-3 · `conflict/` does not exist.** See §1. A1 already re-pointed; if the operator meant a
folder in a repo not on this host, the census will report the gap rather than invent one.

**U-4 · DC-2 AND DC-3 ARE FLEET-WIDE ACTS, NOT HUB-LOCAL EDITS — and this may be circular.**
All eleven CLAUDE.md locators in the brief **resolve exactly** (unusually clean; verified line by
line). But resolving them against the `methodology:start/end` boundary markers changes what the
work IS:

```
:16   outside all regions            REPO-owned   DC-2  safe, hub-local
:25   region first-read       (hub)  HUB          DC-2  fleet-wide
:29   region first-read       (hub)  HUB          DC-2  fleet-wide
:39   region repo-identity   (repo)  REPO         DC-3  safe, hub-local
:40   region repo-identity   (repo)  REPO         DC-3  safe, hub-local  <- ObsidianVault
:63   conventions-commit-branch(hub) HUB          DC-3  fleet-wide       <- branch-prefix enum
:68   outside all regions            REPO-owned   DC-3  safe, hub-local
:77   outside all regions            REPO-owned   DC-3  safe, hub-local  <- ObsidianVault
:81   conventions-output-formatting  HUB          DC-3  fleet-wide       <- TUI rationale
:97   critical-rules-consistency     HUB          DC-2  fleet-wide
:201  antipatterns-universal  (hub)  HUB          DC-2  fleet-wide
```

**Good news on the operator's one DELETE instruction:** *both* ObsidianVault lines (`:40`, `:77`)
are **REPO-owned**. Deleting them outright is a clean hub-local act with zero fleet consequence
— exactly as the brief rules it.

**The hazard is the other six.** Region bodies are **byte-identical** to
`templates/claude-regions/*.md`, which the deploy carriers ship to every ADR-104 member. Editing
any of those six means editing the region template, which means a deploy — and
**DEPLOYMENT WAVE is `blocked_by` DOCTRINE CONSOLIDATION**, which is what DC-2/DC-3 are. Left
unruled this is circular: doctrine consolidation cannot finish without a deploy, and the deploy
arc is blocked until doctrine consolidation finishes.

Three ways out, for the cut to choose — **not chosen here**:
- **(a)** DC-2/DC-3 edit hub-local lines ONLY; the six hub-region lines move in a separate
  region-template lane sequenced into the DEPLOYMENT WAVE.
- **(b)** DC-2/DC-3 edit region templates too, and the batch accepts a fleet parity RED window
  closed by the first consumer deploy — a declared, time-boxed RED, never a silent one.
- **(c)** The arc `blocked_by` is amended so a region-template change is explicitly exempt from
  the block. That is an ADR-level act, not a lane's.

**U-5 · `[#591]`'s validator already exists.** See 0a. Do not fund built work as new.

**U-6 · DC-1, DC-2 AND DC-3 ARE NOT FILE-DISJOINT.** The brief requires committing lanes to be
file-disjoint. All three write `CLAUDE.md`; DC-1 and HY-1 both write `scripts/canonical_docs.py`.
DC-3's own text concedes the coupling (*"drop VISION ... once DC-1 lands"*). They **must
serialize**, not parallelise. §5 reflects this; it is the biggest constraint on the batch's
wall-clock and should be seen before the cut, not after.

**U-7 · The six baseline-drift REDs.** Being measured; two known-false worktree REDs must be
subtracted. See 0b.

**U-8 · Tier (C)'s status is a GATE, and the batch plan branches on it.** The codespace admission
probe decides whether committing lanes route Codespace or LOCAL. `Dispatch-Codespace` /
`Stop-Codespace` / `Invoke-CodespaceGh` are live in DispatchHelpers, so the verb exists. Until
the probe returns 3-of-3 + gate green, **§5 assumes LOCAL** — the brief's own fallback.

**U-9 · A7's headline answer is already in the tree.** `ecosystem/provider-registry.yaml`
(`antigravity` row) states `agy` is registered PRESENT with **NO ROLE**, because admitting it
would give the **REFUSED** `gemini-3.7-flash` family a second route into the fleet — a `[#578]`
rerun question, not a registry act. So the token policy's *"whole-repo analysis -> agy when
admitted"* has **no live route today**. A7 verifies and makes the quota curve legible; it does
not admit anything. **Plan the batch as though agy is unavailable, because it is.**

**U-10 · DM-4 IS THE WEAKEST LANE IN THE BATCH — THREE INDEPENDENT PROBLEMS, ALL RULED AGAINST IT.**
The brief says *"sqlite-vec proven under pinned uv by lane-g"* and files DM-4 under
*"execute the Tier-S experiments"*. Resolved against the artifact, all three legs fail:

**(1) The claim overstates what was proved.** `docs/audits/2026-08-29-technical-autonomy-synthesis.md`
proves only that `enable_load_extension` works on this host — *"The Windows extension-loading
blocker does not exist on this substrate... `sqlite-vec` remains a live candidate"*, and
explicitly: **"Nothing was installed and nothing was written to run this."** A substrate
capability was proved. **sqlite-vec was never installed, never run, and never exercised under the
pinned `uv`.** "Live candidate" is not "proven".

**(2) IT IS TIER L, NOT TIER S — and the same synthesis already ruled that, correcting two cloud
lanes that got it wrong.** ADR-112's guard sentence: *"Tier S never touches gates, hooks that
block, or `scripts/` — anything that would, is Tier L by definition."* Adopting sqlite-vec means
editing `pyproject.toml` + `uv.lock` and writing a `scripts/` embedding producer. The synthesis
records: *"Neither cloud lane checked its own tier label against ADR-112's text."* Intake #63
already says so verbatim — *"ADR-112 Tier-L applies: evaluate before adopting."*
**So the brief repeats, for a third time, the exact mislabel the synthesis was written to
correct.** Tier L means EVALUATE BEFORE ADOPTING — a heavier bar than Tier S's try-and-keep-or-delete.

**(3) Its embedder is on the REJECTED list.** DM-4 names `sentence-transformers`; the decision
tree lists it under REJECTED (with ChromaDB, LanceDB, Mem0, Letta/MemGPT, Zep). The synthesis's
own pairing is **model2vec**, not sentence-transformers.

**Recommendation, offered because the evidence is one-sided and the cut should not have to
re-derive it:** DM-4 does not belong in this batch as a Tier-S experiment. Either re-file it as a
Tier-L evaluation under intake #63, or drop it from batch E. Not decided here — but freezing it
as written would land a `uv.lock` change under the wrong adoption bar with a rejected dependency.

**U-11 · Harbor is PARKED with a trigger that has not fired.** The decision tree parks Harbor on
*"a second executor is admitted"* — none is. (B)'s SDA-1-to-Harbor translation is **text only**
and that is fine; but DM-1 must not quietly become a Harbor adoption. The admission gate the
`.CLAUDE GOVERNANCE MODEL` filing introduces is a *consumer* of THE METRIC (north-star rank 1),
so it cannot precede it.

**U-12 · The 11 structural census WARNs clearing on merge commits** — carried from the brief,
unverified.

**U-13 · DM-3's ROW CITATION IS REFUTED. `[#615]` IS A DIFFERENT SUBJECT.**
The brief routes DM-3 (graph: typed layers + thesis architectural attributes as node metadata) to
`[#615]`. **`[#615]` is "MODEL ATTRIBUTION — a model+version signature trailer on every
model-authored commit"** (open, P2/M, theme `[E2]`, from intake #50). Not the graph. Further, **no
`tasks/*.md` mentions FPG, "typed layer" or "architectural attribute" at all** — the graph has no
backlog row in any form.

Its real home is **intake #40**, `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md`
— `status: DRAFT`, extended by operator direction on 2026-08-29 from a *document* dependency graph
to a **typed, multi-layer** one whose layers are code · docs · backlog · intake/ADR · **L0**, and
which **explicitly cross-references intake #62** — the umbrella this session just amended. It
carries **no row**, deliberately, because ADR-111 §2 forbids a lane birthing one.

**Consequence for the cut:** DM-3 cannot be a build lane against a DRAFT intake with no carrier
row without violating the batch's own reconcile-before-birth rule. Either freeze it as a
**drafting** lane, or ratify intake #40 first. Recorded, not chosen.

**A useful accident:** `[#615]` is not irrelevant to this batch — it is the **enabling row** for
per-model telemetry, and §3's token policy demands exactly that (*"Record per-lane
provider+model+credits in the quota-source telemetry; the burn-down + quota panels are this
batch's visibility proof"*). `[#615]` is currently unfunded in this plan and probably should not
be: without it the quota curve cannot attribute a lane to a model. **Consider funding `[#615]`
as the quota-panel precondition** — that is a cut, and it is not taken here.

---

## 4 · THE PARALLELISM CONSTRAINT, MEASURED

`serialize-group` is the contention axis (`gen_task_tree.derive_serialize_group`). Live counts
over open rows:

```
audit-py 143 · architecture 82 · handoff 46 · settings-json 40 · environment 31
playbook 30 · gates 26 · pre-commit-config 18 · claude-md 16 · codex-review 12
none 8 · coherence 6 · docs-gate 2 · code-edge 2
```

Two lanes sharing a serialize-group cannot run concurrently. **`claude-md` and `audit-py` are
this batch's contended groups** — `claude-md` holds DC-1/DC-2/DC-3, `audit-py` holds HY-1 plus
the freshness/gate work. That is the whole reason §5's doctrine chain is serial.

---

## 5 · THE LANE LIST — proposed, NOT frozen

Format per lane: `id · subject · row/intake · write-scope · substrate · serialize-group · blocked-by`.
Substrate reads **LOCAL** wherever tier (C) has not yet passed; flip to Codespace on a green probe.

### The doctrine chain — SERIAL, one writer at a time on CLAUDE.md

```
DC-1  VISION -> README, fleet-wide
      row/intake: [#614] (VISION->README), intake #38 (root-contract), ADR-114
      write-scope: README.md, VISION.md (archive byte-identical), scripts/canonical_docs.py,
                   the P1a boot probe, hermeticity validators, ADR-38 baseline check,
                   deploy/ carrier for the migration
      substrate: LOCAL   serialize-group: claude-md + audit-py   blocked-by: nothing
      NOTE: run the P1a probe against the new README BEFORE merge (brief's own gate).

DC-2  ESSENTIALS dissolution, on the batch-D census
      row/intake: docs/audits/2026-08-29-census-essentials-consumers.md; A3's output sharpens it
      write-scope: protocols/ESSENTIALS.md (archive), protocols/PLAYBOOK.md, CLAUDE.md :16,
                   the thin floor carrier; :25/:29/:97/:201 ONLY under U-4's ruling
      substrate: LOCAL   serialize-group: claude-md + playbook   blocked-by: DC-1, U-4 ruling
      REFUSE-TO-PROCEED: a consumer the census shows would break => name it and STOP.

DC-3  CLAUDE.md genre purification
      row/intake: continues batch-D lane-c (docs/audits/2026-08-29-technical-claude-md-regenre.md)
      write-scope: CLAUDE.md :39 :40 :68 :77 (hub-local, safe), protocols/PLAYBOOK.md
                   (relocation destinations), tests/test_claude_md_byte_cap.py re-gate;
                   :63/:81 ONLY under U-4's ruling
      substrate: LOCAL   serialize-group: claude-md   blocked-by: DC-1, DC-2, U-4 ruling
      Every removal is a relocation to a NAMED destination, except the two ruled ObsidianVault
      deletions.

DC-4  ROOT-CONTRACT (intake #38) — the hub root's canonical clean shape
      row/intake: intake #38, amended 2026-08-30
      write-scope: the root file set + ordering + workspace declaration; no consumer touched
      substrate: LOCAL   serialize-group: architecture   blocked-by: DC-1 (README is the front door)
      MUST land BEFORE the first consumer deploy — it is the surface that deploys.

DC-5  AI-COUNCIL instantiation contract from the win-tooling template
      row/intake: intake #38 + the win-tooling template; consumer #2, same engine
      write-scope: ecosystem/ai-council/, deploy carrier declaration; NO bespoke path
      substrate: LOCAL   serialize-group: architecture   blocked-by: DC-4, and U-1's order ruling
```

### Dimensions — parallel with each other, disjoint from the doctrine chain

```
DM-1  EVAL — one SDA-1 pack in Harbor format, run once, compared to the hand-rolled run
      consumes (B)'s draft   substrate: LOCAL   serialize-group: gates
      blocked-by: (B) draft; see U-11 — text translation only, not a Harbor adoption

DM-2  OBSERVABILITY — telemetry emits OTel GenAI events, collector pluggable
      consumes (B)'s schema  substrate: LOCAL   serialize-group: audit-py
      blocked-by: (B) draft. Verdict layer (trends -> rulings) UNCHANGED.

DM-3  GRAPH — typed layers + thesis architectural attributes as node metadata
      intake: #40 (docs/intake/2026-08-22-tech-document-dependency-graph-organ.md), DRAFT,
              extended 2026-08-29 to a TYPED MULTI-LAYER graph and explicitly cross-referencing
              intake #62 — the umbrella this session just amended. It has NO carrier row.
      NOT [#615] — see U-13.   substrate: LOCAL   serialize-group: architecture
      blocked-by: intake #40 is DRAFT with no carrier row; birthing one is an ADR-98/111 act,
                  not a lane's. Freeze this as a DRAFTING lane or ratify #40 first.

DM-4  LOCAL MEMORY — sqlite-vec + sentence-transformers over docs/ + tasks/;
      hit-rate vs grep on 20 real questions, recorded
      substrate: LOCAL   serialize-group: environment
      *** DO NOT FREEZE AS WRITTEN — see U-10. Three independent problems: the
      "proven under pinned uv" claim is refuted (nothing was ever installed or run);
      it is ADR-112 TIER L, not Tier S, and the brief repeats for a third time the
      mislabel the autonomy synthesis was written to correct; and its embedder
      (sentence-transformers) is on the decision tree's REJECTED list — the
      synthesis pairs sqlite-vec with model2vec instead.
      Re-file as a Tier-L evaluation under intake #63, or drop from batch E. ***

DM-5  DISTILLER filing amendment — eval-loop is a PRECONDITION (SkillsBench)
      row: [#617]; now also carried by the .CLAUDE GOVERNANCE MODEL umbrella (intake #62)
      FILING ONLY   substrate: LOCAL   serialize-group: none   blocked-by: nothing

DM-6  EQUILIBRIUM — R3's checkpoint blind spots as rows per the decision tree
      FILING ONLY   substrate: LOCAL   serialize-group: none   blocked-by: nothing
```

### Hygiene

```
HY-1  Doc freshness DERIVED from git for every living doc + gated (extend P5 fleet-wide);
      PLAYBOOK's doctrine table shows live version + date
      consumes A4's output   write-scope: scripts/canonical_docs.py, scripts/audit.py,
      protocols/PLAYBOOK.md   substrate: LOCAL   serialize-group: audit-py
      blocked-by: A4 harvest, DC-1 (canonical_docs.py contention)

HY-2  logs/ — dated logs into dated subfolders by a RETENTION RULE; one token log stays flat
      A MECHANISM, not a cleanup   substrate: LOCAL   serialize-group: gates
      CAUTION: logs/TOKEN-LOG.md is strict append-only (ADR-29/39) with NO archival exception —
      the LESSONS.md relocation carve-out does NOT extend to it.

HY-3  conflict/ and templates/ per the (A) censuses — universalize / relocate / retire
      consumes A1 + A2   substrate: LOCAL   serialize-group: architecture
      blocked-by: A1 + A2 harvest. NO DELETION OF A LIVE SOURCE.
      NOTE: the conflict/ half has no subject (U-3) — it is the single-file-folder half.

HY-4  TRENDS burn-down panel — done vs remaining per north-star arc over time
      substrate: LOCAL   serialize-group: audit-py   blocked-by: nothing
      This plus the quota panel is the batch's visibility proof (§3 of the brief).

HY-5  win-tooling: new chat defaults to LOCAL PowerShell, not the cloud rung (RULING-W)
      CROSS-REPO — win-tooling, not the hub   substrate: LOCAL   serialize-group: n/a
      blocked-by: U-1's order ruling (win-tooling is FIRST in one order, LAST in the other)
```

### Filing already landed this session (not a lane — done)

```
FILING  .CLAUDE GOVERNANCE MODEL -> amendment to intake #62 + the HERMETIZATION order on the
        DEPLOYMENT WAVE arc. Zero new folders, intakes or rows. #62 stays DRAFT.
        Landed b3f489b5 on worktree-batch-e-derive. Targeted tests: 51 passed
        (test_gen_north_star, test_gen_intake_index, test_gen_intake_tree).
        gen_north_star.py grew an OPTIONAL per-arc `sequence` field; a rival sixth arc was
        NOT created, because arc membership is a theme selector and a second arc sharing
        [E6]/[E9] would double-count every row in both.
```

---

## 6 · MERGE ORDER

Serial where contended, parallel where disjoint. One integrator, from the primary checkout.

```
0.  0a + 0b + 0c            (LOCAL, serial, minutes — before any committing lane)
1.  DC-1                    (unblocks DC-3, DC-4, HY-1)
2.  DC-2                    (needs U-4 ruling if it touches hub regions)
3.  DC-3                    (needs DC-1 + DC-2 landed)
4.  DC-4  ->  DC-5          (root contract before the first consumer deploy)
5.  DM-3 · DM-5 · DM-6 · HY-4   (disjoint — merge any time after 0)
6.  DM-1 · DM-2             (after (B) drafts land)
7.  DM-4                    (after U-10 + the sentence-transformers reconcile)
8.  HY-1                    (after A4 harvest AND DC-1 — canonical_docs.py contention)
9.  HY-2 · HY-3             (after A1/A2 harvest)
10. HY-5                    (cross-repo; after U-1)
```

**The journal-anchor mechanic is forced, not optional.** Cloud `claude/*` lanes fall outside
`LANE_BRANCH_RE`, so `check_journal_spine_anchor` sees every one of their merges as unanchored
and the queue wedges. Pre-anchor: commit a real artifact on a branch, then a JOURNAL entry naming
that artifact's SHA **plus every lane branch tip SHA**, merge it `--no-ff` FIRST, then run the
queue. **The batch carries two JOURNAL entries, not one** — say so rather than hiding it. Never
reach for `SKIP=audit-health` when the flagged merges are your own.

---

## 7 · EX-ANTE NUMBERS

```
Tracked corpus                 2,761 files / 42,083,797 B  (~19.6M tokens)
Payload ceiling (75% of 284.3k) 213,225 tokens             -> whole-tree work is ~92x over
templates/                     47 tracked files / 554 referencing files
ESSENTIALS|Universal Protocols  519 referencing files (narrow filter; +29 the filter misses)
Living docs carrying last_reviewed  493
Single-file tracked directories 44
LangGraph-class mentions        14 files
Decision-tree leaves            55 routed / 18 TRUE GAP / 2 became rows
North-star open rows            163 of 218 manifest-referenced (55 deferred)
validate_substrate predicates   4 (3 REFUSE + 1 WARN)
Committing lanes proposed       16  (DC 5 · DM 6 · HY 5)
Serial chain length             3   (DC-1 -> DC-2 -> DC-3, all on claude-md)
Cloud lanes dispatched          7   (tier A, all read-only, 7/7 bound)
```

**Counts above are freeze-time measurements, not doctrine.** Every one is re-derivable by the
command that produced it; none is restated from another document.

---

## 8 · WHAT IS DELIBERATELY NOT DONE HERE

- **No lane in §5 is frozen.** No contract written to the prompts dir, no worktree provisioned,
  no manifest committed, no `closed_by:` chosen.
- **No tier (B) dispatch.** Enterprise Copilot drafts wait on the cut.
- **No tier (C) probe.** The codespace admission probe is the first committing-tier act and is
  the operator's to start.
- **No ruling.** U-1 through U-12 are named, evidenced and left open. The operator rules
  functional questions, the architect technical ones (ADR-108 §A).
- **No row born, none closed.** Reconcile-before-birth: the only filing act this session took
  was an amendment to an existing intake.
