# Overnight audit — TECHNICAL / DOCTRINE layer findings (2026-06-21)

> **Scope:** `ARCHITECTURE.md` + `docs/decisions/*` (the ADRs), reconciled against
> `JOURNAL.md` (source of truth) and live repo state. Read-only on `scripts/` for the
> organ inventory. **Mode:** auto-apply mechanical currency fixes (committed + logged
> here); PROPOSE everything judgment-bearing. **Merge-back owed** — the operator merges
> `feat/audit-technical` after reviewing this doc; nothing reaches `main` unsupervised.
> `/ship` was NOT run from this worktree.

**Run:** 2026-06-21 · CC (Opus, MAX) · worktree `audit-technical` · branch `feat/audit-technical`

---

## TL;DR

The technical/doctrine layer is **substantially current**. Every load-bearing count the
brief named is **live-correct** (verified, not assumed): pre-commit gates **10**, audit
checks **22**, `pytest_collected` **772** — all four `validate_doc_claims` claims match.
ADR-88 and ADR-89 statuses + open-question states are accurate. One mechanical drift was
auto-fixed; six items need an operator decision.

| # | Item | Type | Severity |
|---|---|---|---|
| **A1** | ARCHITECTURE pre-commit gate list listed 9, header/config say 10 (missing `block-ff-push`) | **AUTO-APPLIED** | — |
| **P1** | ADR-82 reads `Proposed` / README says `Council-pending`, but v5 was operator-ratified canonical 2026-06-11 | PROPOSE | High (legibility) |
| **P2** | README ADR index is missing rows **ADR-73–80** (8 ADRs; known gap) | PROPOSE | Medium |
| **P3** | ADR-89 OQ3 has no back-reference to the #196 removal-closure findings + "direct-boundary-union" framing | PROPOSE | Medium |
| **P4** | ARCHITECTURE §Validators inventory omits `validate_reconciliation.py` (and is not exhaustive) | PROPOSE | Medium |
| **P5** | Per-ADR ratification-readiness notes (ADR-88, ADR-89) | PROPOSE (requested) | — |
| **P6** | Organ-map restructuring assessment | PROPOSE (requested) | None needed |

Plus **cross-domain flags** (not fixed — other layers' scope) in the final section.

---

## AUTO-APPLIED (mechanical, committed on `feat/audit-technical`)

### A1 — ARCHITECTURE pre-commit gate list completed (`block-ff-push`) · commit `c4ffb6e`

**What:** The §Validators "Pre-commit gates (`.pre-commit-config.yaml`)" prose enumeration
(ARCHITECTURE.md ~L325) listed only **9** hooks and omitted `block-ff-push`. Added
`block-ff-push (pre-push — #153 prevent half; activate once via pre-commit install
--hook-type pre-push)`.

**Why it is mechanical (provable / reversible / content-preserving):** three independent
ground-truth sources already counted it as the 10th gate, so the list was internally
self-contradicting:
- The Organ-map header says **"pre-commit gates (10)"** (ARCHITECTURE.md L217) — and
  `validate_doc_claims` confirms doc 10 / actual 10 against `.pre-commit-config.yaml`.
- The §Validators **`block_ff_push.py` bullet already exists** (ARCHITECTURE.md L262–270).
- `.pre-commit-config.yaml` L93–104 defines the `block-ff-push` hook (10th id).

**JOURNAL evidence:** 2026-06-20 "block-ff-push pre-push gate" entry — *"ARCHITECTURE
`pre-commit gates` count 9 → 10 + a §Validators bullet"* (the count + bullet landed; the
bottom prose roster was the one surface the #153 doc-sync missed). Shipped to `main` at
merge `fbab423` / trims `dec7726`.

**Companion restamp:** the edit touched freshness-gated `ARCHITECTURE.md`, so per the
canonical-freshness cadence I did a **genuine end-to-end re-read** this session and
restamped `last_reviewed: 2026-06-20 → 2026-06-21`; remaining drift is filed below (the
cadence permits "re-read end-to-end and confirmed accurate **or drift filed**"). Verified
post-edit: `canonical_freshness` OK, `doc_claims` OK, `doc_structure` OK, `ruff` clean,
all pre-commit hooks Passed.

---

## PROPOSE (judgment — operator decides; NOT auto-applied)

### P1 — ADR-82 status legibility: `Proposed` header + `Council-pending` index vs. a spec canonical since 2026-06-11 — **High**

**What:** `docs/decisions/ADR-82-…md` L3 reads **`Status: Proposed`**, and the README ADR
index (L61) labels it **"Proposed (Council-pending)"**. But HANDOFF_PROCESS v5 has been the
**live canonical handoff spec for 10 days**:
- `protocols/HANDOFF_PROCESS.md` header: *"Version: 5.2 · Status: stable · Effective:
  2026-06-11 (canonical) · Decision: **ADR-82 (operator-ratified 2026-06-11; Council gate
  waived by operator authority per #149)**"*.
- v4.4 is archived at `protocols/archive/HANDOFF_PROCESS_v4.4.md`.
- `audit.py` validates every living doc against *"canonical HANDOFF_PROCESS v5.2"*.

**Why this is nuanced (read before acting):** the `Proposed` header is **deliberate, not an
oversight.** ADR-82's own **Amendment 2026-06-16 (L57)** states: *"This ADR's header
remains `Proposed` (its original state); the spec it records was operator-ratified canonical
at the #149 flip (2026-06-11)… does not alter the original decision text (ADR immutability —
an append-only marker)."* So the author froze the header per one reading of ADR immutability,
recording ratification via append-only amendment + CONTRIBUTING + HANDOFF_PROCESS instead.

**The genuine problems that remain:**
1. **The single most-scanned ADR signal is actively misleading.** A status grep (or a reader
   skimming) sees `Proposed` and concludes v5 is not ratified — false. The ratification fact
   is buried 50+ lines deep in an amendment.
2. **The README index label is flatly wrong, not just frozen.** "Council-**pending**" is
   false — the Council gate was **waived** per #149, not left pending. The README index is a
   **living** doc (not immutable), so this half is a clean currency error regardless of the
   header-immutability question.
3. **The frozen-header reading is inconsistent with repo precedent.** ADR-52
   (`~~Accepted~~ Superseded by ADR-53`), ADR-45 (`Explored, not adopted`), and ADR-46
   (`Partially superseded`) all carry **in-place status markers** on their headers. ADR-89
   itself was annotated in place (OQ2 "RESOLVED 2026-06-20 (#193)"). So "never touch the
   status header" is not a uniform convention here.

**Risk of acting:** Low–medium. Editing an ADR header brushes the immutability convention —
but the precedents above show an **append-only in-place marker** is the sanctioned form.

**Recommendation (operator's call):**
- **Minimum:** fix the README index L61 label — `Proposed (Council-pending)` →
  e.g. `Proposed (header frozen per immutability) — operatively ratified 2026-06-11, Council
  gate waived #149`. (Living doc; the clearly-wrong half.)
- **Preferred:** also add a one-line in-place marker to ADR-82's `Status:` line in the
  ADR-52/45/46 style, e.g. `Status: Proposed → operative (operator-ratified canonical
  2026-06-11; Council gate waived #149; header frozen per ADR immutability — see Amendment
  2026-06-16)`. This makes a status-scanner correct without rewriting the decision text.
- I did **not** auto-apply either: both require choosing the representation of a
  "frozen-Proposed-but-ratified" ADR, which is a governance-representation judgment, not a
  mechanical reconciliation.

> **Note — out-of-scope decommission slip (flagged, not fixed):** ADR-82 L6 lists three
> decommissions due "on promotion to canonical." The promotion happened (2026-06-11), and
> (3) checks #8/#9 are retargeted to historical-v4 (confirmed live). But **(1)
> `templates/handoff/*.tmpl` → `templates/archive/handoff-v4/` is NOT done** — the v4 `.tmpl`
> files (`01_ROLE…07`, README) still sit in `templates/handoff/`, and `templates/archive/`
> holds only `AGENTS-md-template.md`. This is `templates/` scope (not ARCHITECTURE/ADRs) and
> a move/delete (needs the ask-before-delete + no-leftovers discipline) — surfaced for the
> operator to verify/route, not touched here.

### P2 — README ADR index is missing rows ADR-73–80 — **Medium**

**What:** `docs/decisions/README.md`'s ADR Index table jumps **ADR-72 (L59) → ADR-81 (L60)**.
Eight ADR files exist on disk with no index row: **ADR-73, 74, 75, 76, 77, 78, 79, 80**.

**Why it persisted:** it is a **known, acknowledged** gap — the ADR-81 row itself says
*"(Index rows ADR-73…ADR-80 are a known pre-existing gap in this table, not part of this
ADR.)"* All eight are `Accepted` (verified from each file's status line). The index uses
rich one-line summaries, so filling them is editorial authoring, not a count bump → PROPOSE.

**Risk:** Low (additive rows). **Recommendation:** authorize filling. Draft rows below
(verified dates + titles from each ADR file; condense/expand to taste before pasting):

```
| ADR-73 | 2026-06-06 | Per-repo orchestration distribution — each repo carries its own orchestration/automation; no hub-centralized driver (Layer-2 invariant). |
| ADR-74 | 2026-06-06 | Automation doctrine consolidation — friction-cadence tiers (1 always-on / 2 scheduled / 3 episodic), adoption rubric with pre-registered kill-criteria + n=2 evidence gate; case law (Dynamic Workflows ADOPT, GitHub Action ADOPT, graphify REJECT, /loop-as-host REJECT). |
| ADR-75 | 2026-06-06 | Exclusion-zone register — one amendable register for exclusion/immutability/scope policy; "no organ = decoration" (every zone backed by a fail-closed organ on the executing path). |
| ADR-76 | 2026-06-06 | Local fleet-baseline host — Windows Task Scheduler → `python scripts/fleet_health.py` directly (no `claude -p`, no LLM on the scheduled path); fail-soft + catch-up on a missed run. |
| ADR-77 | 2026-06-06 | Immutable-paths zone class — `docs/decisions/transcripts/**` guarded by a PreToolUse hook (`block_immutable_edits.py`), fail-closed in-zone / fail-open out-of-zone; amends the ADR-75 register. |
| ADR-78 | 2026-06-07 | Child methodology floor (O2 Bounded Hybrid) — generated `CLAUDE-FLOOR.md` (≤1,500 tok) + `.sha256` per child under `.claude/`; operator-invoked generator; adds the `methodology_surface` zone. |
| ADR-79 | 2026-06-07 | Browser methodology carrier — bundle-only (one consolidated `BUNDLE.md`); Projects deferred (an LLM-governed freshness check is an unverifiable safety property). |
| ADR-80 | 2026-06-07 | Two-tier automation adoption — the LLM-judgment axis (deterministic ↔ judgment) orthogonal to ADR-74's friction-cadence tiers; writer policy (pathspec-bounded, fail-soft, commits own output) + Routine/night standard + n=2 adoption gate; no `fallbackModel` on pinned stages. |
```

### P3 — ADR-89 OQ3 should cite the #196 removal-closure findings + "direct-boundary-union" framing — **Medium**

**What:** ADR-89 OQ3 (L202–204, *"Advisory→gate promotion for code-edge checks… data-gated…
not pre-decided"*) is the exact doctrine question the **#196 removal-closure computation
spike** addressed, but OQ3 carries **no reference** to `docs/audits/2026-06-20-removal-closure-
spike-findings.md` nor the corrected framing. The findings doc points the other way —
*"sufficient to decide D-2b's build approach **or** to write the ADR-89 OQ3 ruling"* (L10) and
binds *"ADR-89… OQ3 advisory→gate still open, data-gated"* (L15) — so the link is one-directional.

**Why not auto-applied:** the JOURNAL is explicit that #196 **does not resolve OQ3** —
*"On ADR-89 OQ3: does NOT resolve by fiat (OQ3 is data-gated)… operator turns the proposal
into the #195-2b build approach OR the ADR-89 OQ3 ruling"* (2026-06-20 #196 entry). The OQ3
ruling is **operator-owned**, and ADR-89 is a Proposed-doctrine doc. Adding the cite is an
interpretive annotation the operator should make when they rule.

**Risk:** Low. **Recommendation:** when ruling OQ3 (or before ratifying ADR-89), add an
in-place marker on OQ3 in the ADR-89-OQ2 (#193) precedent style, e.g.:
*"— INFORMED 2026-06-20 (#196). The removal-closure spike (`docs/audits/2026-06-20-removal-
closure-spike-findings.md`) verdicts GO for a **heterogeneous direct-boundary union** (a
boundary check, not a transitive walk; it refines #196's filed "traverse uniformly") and
recommends the computed legs gate **advisory-first**. OQ3 stays open — promotion remains
data-gated."* (Optional minor enrichment: ARCHITECTURE L320's `#195` mention could gain a
"(design: #196 findings)" pointer, but the canonical locus is ADR-89 OQ3.)

### P4 — ARCHITECTURE §Validators inventory omits `validate_reconciliation.py` and is not exhaustive — **Medium**

**What:** The §Validators section is introduced as *"the `scripts/` inventory"* of executable
organs, but several shipped `scripts/*.py` have no entry. Most notable:
**`validate_reconciliation.py`** — the declared-edge coherence checker behind audit check #20
(`reconciled_versions`) — appears only inline (ARCHITECTURE L295, as the complement to the
scan) with **no dedicated bullet**, even though its discovery-sibling `scan_undeclared_edges.py`
has a full one **and ADR-88 names it the proven v1 "deterministic trigger"** (ADR-88 L61).

Also absent from the inventory (live in `scripts/`, confirmed via the tree + JOURNAL):
`coherence_enumerator.py` (the site enumerator; ADR-88 L64), `review_closures.py` (backs
`/review-closures`), `probe_child_backlogs.py` (#120 child-BACKLOG readiness probe),
`assemble_paste.py` (#159 handoff PASTE_THIS assembler), `generate_floor.py` (named in Ch4
only, not §Validators), and hook wrappers `codemap_hook.py` / `toc_hook.py`. `migrate_links.py`
appears to be a one-off utility.

**Why not auto-applied:** deciding whether the inventory is **meant to be exhaustive** vs.
curated-to-organs — and which utilities qualify as "organs" — is an editorial/structural
judgment, and the brief says "any organ-map restructuring… propose it." Adding bullets is
additive but it is curation, not a count reconciliation.

**Risk:** Low. **Recommendation:** at minimum add `validate_reconciliation.py` (it is a
first-class coherence-spine organ + ADR-88's named trigger; its absence is the clearest gap).
Draft bullet, ready to paste under the §Validators list:

```
- `scripts/validate_reconciliation.py` — declared-edge coherence checker (the **deterministic
  trigger** of the ADR-88 coherence spine; #172): a dependent declares `reconciled_with:
  <spec-id>@<version>` in frontmatter; the checker resolves the spec's current version from
  `_SPEC_REGISTRY` and flags a dependent whose declared version lags. Read-only; surfaced via
  the `reconciled_versions` audit check (#20). Pairs with `coherence_enumerator.py` (site
  enumerator) and `scan_undeclared_edges.py` (the undeclared-edge discovery half). Standalone
  CLI: `python scripts/validate_reconciliation.py`.
```

Decide separately whether to also add `coherence_enumerator.py` / `review_closures.py` /
`probe_child_backlogs.py` / `assemble_paste.py`, or to add a one-line scope note that the
inventory is **curated to enforcement/awareness organs** (so handoff/utility scripts are
intentionally out). Either resolves the "exhaustive vs curated" ambiguity.

### P5 — Per-ADR ratification-readiness notes (requested) — ADR-88 & ADR-89

Both are **Proposed**; both carry "resolve before Accepted" open questions. Current readiness:

**ADR-88 (file-oriented dependency management).** The *doctrine is empirically validated* —
the failure-class organs have shipped since authoring: FC2 `scan_undeclared_edges.py` (#179),
FC3 BACKLOG dedup (#187), FC4 `validate_doc_rot.py` (#140), and the v1 proof
(`validate_reconciliation.py` + `coherence_enumerator.py` + the mutation closure-test) is
live. FC1 (probe regime) is "partial" by design. The blocker to Accepted is its **forward-
gated OQs**, not unproven mechanism:
- OQ1 (FC-taxonomy completeness) and OQ3 (global/local contract) — both *gated on the #131
  deployment pilot*, which has not run.
- OQ2 (#170 edge-model reuse) — explicitly **owned by #170's own ADR**, not ADR-88; need not
  block ADR-88.
- OQ4 (#181 data-gate) — waits on real `logs/coherence-nudge.log` firing signal.
- **Decision the operator/architect owns:** ratify the **core doctrine now with OQ1/OQ3/OQ4
  carried-open** (most are long-horizon pilot/data gates), or hold ADR-88 until #131. If
  ratifying, add the **ADR-88 → ADR-89 back-link** (currently deferred to exactly this edit —
  ADR-89 L132–133 already carries the forward link).

**ADR-89 (computed code-dependency edges).** Core doctrine *proven*: the Pyright oracle
shipped (`reverse_dep_oracle.py`, #193) with the provenance payload that **resolved OQ2**
(annotated in place, L188–201). Remaining:
- OQ1 (doc→code ID-scheme) — explicitly "a later build, not designed here."
- OQ3 (advisory→gate promotion) — data-gated; **informed but not resolved** by #196 (see P3).
- **Decision the operator owns:** as with ADR-88, ratify the core with OQ1/OQ3 carried-open,
  or hold. Ratifying ADR-88 and ADR-89 **together** lets the deferred ADR-88→ADR-89 back-link
  land cleanly in one pass. Apply P3's OQ3 annotation at/ before ratification.

### P6 — Organ-map restructuring assessment (requested) — none recommended

I reviewed Ch2 (Organ map) + §Validators for structural problems. **No restructuring is
warranted** — the organ table (trigger × layer × failure-posture), the Tier-1-loop callout,
and the "machinery retired" note are coherent and current; the generated `ORGAN-INDEX.md`
(#132) is correctly flagged as the future verified source. The only inventory issue is
**completeness, not structure** (P4). Recommendation: address P4; leave the map's shape as-is.

---

## Cross-domain inconsistencies (FLAGGED — not in this layer's scope; not fixed)

These touch other layers (CLAUDE.md, BACKLOG.md, templates/, protocols/) and are surfaced
per the brief's "flag cross-domain, don't fix" rule:

1. **CLAUDE.md §11 "Recent ADRs binding here (last 5)" is stale.** It lists ADR-76–80; the
   actual last five are ADR-85–89. The JOURNAL repeatedly notes this as an "operator-deferred
   groom" (v2.17/v2.19 deferral precedent). → CLAUDE.md layer.
2. **README index "Council-pending" label** (P1) lives in `docs/decisions/README.md` (in my
   scope to flag, recommended above) but its fix should be coordinated with the CLAUDE.md /
   CONTRIBUTING handoff-version surfaces.
3. **BACKLOG #195-2b "direct-boundary-union" framing carry** — git `da2723f` ("close [#196]
   … carry corrected framing into #195-2b") indicates the corrected framing should now live in
   BACKLOG #195-2b. Verify it landed (BACKLOG layer).
4. **Standing dispositioned WARNs** (all known, none introduced here): `git_backlog_drift` #77
   (voided closure), two 2026-06-19 `no_ff_merges` (3a894ee / d0f9ead, grandfathered
   `0941855`), `doc_rot` on BACKLOG #164/#77/#134/#10 and **CLAUDE.md §12 section-history (22
   entries ≥ 12)**. The CLAUDE §12 accretion is a real grooming candidate → CLAUDE.md layer.
5. **ADR-82 decommission item (1)** — `templates/handoff/*.tmpl` not yet archived (P1 note) →
   templates/ layer.

---

## Verified GREEN (the reconciliation that PASSED — recorded for confidence)

- **Counts (live, not assumed):** `validate_doc_claims` → audit checks **22/22**, pre-commit
  gates **10/10**, roster **10/10** (incl. `block-ff-push`), `pytest_collected` **772/772**.
- **Codemap:** "Two nodes" accurate — only `scripts/codemap/` + `scripts/toc/` carry
  `__init__.py`; `scripts/hooks/` has none (not a node). Codemap fresh.
- **Organ inventory (named in the brief):** `block_ff_push`, `scan_undeclared_edges`,
  `reverse_dep_oracle`, `validate_doc_structure`, `validate_no_ff`, `propose_closures`,
  `audit.py` all present in Organ map / §Validators. (`validate_reconciliation` is the gap → P4.)
- **ADR statuses:** all consistent between ADR files and the README index **except ADR-82**
  (P1). ADR-84–87 Accepted; ADR-88/89 Proposed (correct); ADR-61 Accepted (not superseded).
- **ADR-88/89 OQ states:** ADR-88 OQ1–OQ4 open (OQ2 = #170, owned elsewhere); ADR-89 OQ2
  RESOLVED (#193, in-place), OQ1 + OQ3 open. Matches the brief exactly.
- **ADR-89 ↔ ADR-88 cross-link:** ADR-89 forward link present; ADR-88 back-link deferred to
  ratification **by design** (not drift).
- **Today's organ work reflected:** #153 `block_ff_push` (ARCHITECTURE Validators bullet + the
  now-fixed gate list), #199 scan precision (ARCHITECTURE "Candidate scope (#199)" sentence),
  #196 closure findings doc (exists; ADR-89 link is P3) — all reconciled against JOURNAL + git.
- **JOURNAL ↔ HEAD:** the JOURNAL's "merge owed from primary" lines for #199/#196/#153 are
  superseded by `main` first-parent (`d752179`/`e4b3035`/`fbab423`/`2118ec3`/`da2723f`/
  `dec7726`) — JOURNAL predates HEAD, git is the record, as expected.

---

## Closure

1. **Mechanically reconciled + committed** on `feat/audit-technical`: A1 (`c4ffb6e`) + this
   findings doc. ARCHITECTURE.md is factually current to live state.
2. **Decision-ready proposals:** P1–P6 above, each with evidence + a concrete recommendation
   (P2/P3/P4 carry ready-to-paste drafts).

**Merge-back owed:** operator reviews this doc, then merges `feat/audit-technical` → `main`
`--no-ff` from the **primary** checkout (not from this worktree). No autonomous push.
