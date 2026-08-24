# LANE L3 — ADR status-grammar validator + marker sweep (M5, `[#242]`)

- **Date:** 2026-08-23 (batch date; executed 2026-08-24)
- **Lane:** `worktree-status-grammar`, branch `worktree-status-grammar`
- **Contract:** `LANE-L3-status-grammar.md` (frozen, authored before the build)
- **Merge base:** `aeec0fd1` (main tip at dispatch)
- **Scope:** the status *grammar* and its gate. Not deciding any ADR's status, not archiving.

---

## Contract-locator corrections (preflight)

Resolved before acting, per CLAUDE.md §4 M1.

| Contract cites | Actual | Impact |
|---|---|---|
| `docs/adr/` (dispatch gate) | `docs/decisions/` | None on intent — both name the ADR corpus. The dispatch gate's ordering claim still reads correctly against the real path. |
| "four incompatible `Status:` grammars" | **four in the live zone, five corpus-wide** | The fifth (`G5`, blockquote) lives only in `docs/decisions/archive/`. The contract's figure is right for the zone it was measuring. |

Dispatch gate verified satisfied: the ADR-100 ruling landed at `a40bac40`, an ancestor of the
merge base; the Phase-0 packet is present at
`docs/audits/2026-08-23-technical-phase0-preconditions.md`.

---

## Step 1 — Measured divergence (the evidence base)

Method: every `docs/decisions/ADR-*.md` (and `archive/`) scanned over its first 30 lines for a
status field under five candidate grammars, most-specific-first, one match per line. Measured
2026-08-24 against merge base `aeec0fd1`.

**Live zone: 87 ADR files, 87 status fields — a clean 1:1.** No file lacks a status field; no
live file carries two.

### The syntactic axis — four live grammars

| ID | Shape | Live | Archive |
|---|---|---|---|
| **G1** | `- **Status:** V` — list item, bold, colon outside the bold | **40** | 1 |
| **G2** | `**Status:** V` — bare bold paragraph | **34** | 0 |
| **G3** | `Status: V` — plain text, no markup | **12** | 1 |
| **G4** | `status: V` — YAML frontmatter, lowercase key | **1** | 0 |
| **G5** | `> **Status: V**` — blockquote banner, **colon inside the bold** | **0** | 1 |

### Roster by grammar (live zone)

- **G1 (40)** — ADR 48, 49, 50, 51×2, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 94, 95, 96, 97, 98, 99, 100, 101, 104, 111, 112, 113, 114
- **G2 (34)** — ADR 27, 28, 29, 30, 31, 32, 33, 64, 65, 66, 67, 68, 69, 70, 71, 72, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 102, 103, 105, 106, 107, 108, 109, 110
- **G3 (12)** — ADR 34, 35, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47
- **G4 (1)** — ADR 61
- **G5 (0 live / 1 archived)** — ADR 40

`51` and `70` each appear twice because two files carry each number (see "Collateral findings").

### The semantic axis — the value vocabulary is separately divergent

The grammar axis is *how the field is marked up*. The value axis is *what vocabulary it uses*,
and it diverges independently:

| Head token | Count | Files |
|---|---|---|
| `Accepted` | 82 | — |
| `Partially superseded` | 2 | ADR-46, ADR-47 |
| `PARKED` (bold-wrapped `**PARKED**`) | 1 | ADR-114 |
| `Explored, not adopted` | 1 | ADR-45 |
| `Accepted 2026-05-28` (date fused, no separator) | 1 | ADR-61 |

Qualifier shape across all 87: **47 bare**, 20 em-dash-qualified (`Accepted — 2026-06-06`),
17 paren-qualified (`Accepted (ratified by merge 2026-06-29)`), 3 other.

**Neither `Superseded` nor `Deprecated` appears on any live ADR.** Both appear only in the
archive. This independently confirms the `[#552]` observation that a terminal-status check keyed
on those two values is *structurally unreachable* against the live corpus — nothing ever writes
them.

### Verbatim — every live field whose value is not exactly `Accepted`

The other 47 fields carry the byte-identical string `Accepted`; they are listed by number in the
roster above and nothing is elided by not repeating one string 47 times.

```
ADR-42   [G3:5]  Accepted (amended four times: 2026-05-09 afternoon, 2026-05-09 later afternoon, 2026-05-09 night, 2026-05-26)
ADR-43   [G3:5]  Accepted — 2026-05-11
ADR-45   [G3:5]  Explored, not adopted; ADR-42 v3.2 remains canonical authority for handoff architecture
ADR-46   [G3:3]  Partially superseded — retained as convention, NOT audit-enforced
ADR-47   [G3:3]  Partially superseded — retained as convention, NOT audit-enforced
ADR-51a  [G1:3]  Accepted (ratified by ROOT at Wave-2 integration 2026-07-05, ADR-94 status-line-only path; authored in epic lane `llm-first-docs` [#259] under root conditional grant, ADR-97 — the lane did not self-accept). Ratification affirms the frozen direction: ... audit check #7 (`mermaid_theme_directive`) retired.
ADR-61   [G4:4]  Accepted 2026-05-28
ADR-62   [G1:5]  Accepted (post-implementation ratification; decision already made + implemented + validated)
ADR-64   [G2:5]  Accepted — 2026-06-01, via AI Council debate (pick mode, 4-model panel + openai synthesizer, 2 rounds).
ADR-65   [G2:5]  Accepted — 2026-06-01, **Path A** (direct ADR refining ADR-64; no Council convene — ...).
ADR-66   [G2:5]  Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — ...).
ADR-67   [G2:5]  Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — a process
                 >>> VALUE CONTINUES ON LINE 6: "formalization of an already-running loop, not an architectural decision)."
ADR-69   [G2:5]  Accepted — 2026-06-02, **Path A** (operator-confirmed; post-hoc record ...).
ADR-70a  [G1:3]  Accepted — 2026-07-07 architect ratification session (operator ruling R4). Ratifies the addition of an **XL** routing tier ...
ADR-70b  [G2:5]  Accepted — 2026-06-02. AI Council verdict (2026-06-02) + the operator's three-tier synthesis. ...
ADR-71   [G2:5]  Accepted — 2026-06-03 (operator-confirmed). **Consumption contract VALIDATED** ... **Codemap deployment is NOT validated** ...
ADR-72   [G2:5]  Accepted — 2026-06-06 (operator-ruled, Path A of the #86.2 fork). Records **#86 sub-decision 2** ...
ADR-73   [G1:5]  Accepted — 2026-06-06 (ratification date)
ADR-74   [G1:5]  Accepted — 2026-06-06
ADR-75   [G1:5]  Accepted — 2026-06-06
ADR-76   [G1:5]  Accepted — 2026-06-06
ADR-77   [G1:5]  Accepted — 2026-06-06
ADR-78   [G1:5]  Accepted — 2026-06-07
ADR-79   [G1:5]  Accepted — 2026-06-07
ADR-80   [G1:5]  Accepted — 2026-06-07
ADR-82   [G1:3]  Accepted (ratified 2026-08-04 — architect adjudication; canonical since 2026-06-11 by operator waiver of the Council gate, #149. Status line edited in place per ADR-94 Pattern B ...)
ADR-88   [G2:5]  Accepted (ratified 2026-06-21 by operator edit; header flipped 2026-08-04 per ADR-94 Pattern B — see the 2026-08-04 amendment. ...)
ADR-89   [G2:5]  Accepted (ratified 2026-06-21 by operator edit; header flipped 2026-08-04 per ADR-94 Pattern B — see the 2026-08-04 amendment. ...)
ADR-91   [G2:5]  Accepted (ratified by merge 2026-06-29; baseline release `v1.0.0` tagged)
ADR-92   [G2:5]  Accepted (ratified by merge 2026-06-29)
ADR-93   [G2:5]  Accepted (ratified by merge; authored DURING the #226(b) build ...)
ADR-101  [G1:3]  Accepted (ratified 2026-07-11 — operator ruling via the 2026-07-11 morning verdict sheet [M1]; ...)
ADR-107  [G2:3]  Accepted (ratified 2026-07-28 — operator word, architect session)
ADR-108  [G2:3]  Accepted (ratified 2026-07-31 — operator word, relayed via the outgoing browser seat)
ADR-109  [G2:3]  Accepted (ratified 2026-07-31 — accepted by operator GO, architect session; ADR-94 status-line-only edit)
ADR-110  [G2:3]  Accepted (operator GO 2026-08-06, on SESSION PLAN v2 §3 — acceptance granted in-session)
ADR-111  [G1:3]  Accepted (operator ruling 2026-08-10 — seat-27 ruling checklist, Fork 1 = Option A: ratify AS WRITTEN, the §4 departure intact)
ADR-112  [G1:3]  Accepted (operator ratification 2026-08-12 — ruled TAK on the ARC2 packet, Q2)
ADR-113  [G1:3]  Accepted (architect ruling 2026-08-19, the L-5 rulings block delivered to the S-1 night-adjudication seat)
ADR-114  [G1:3]  **PARKED** — ruled by the operator 2026-08-22. *The priced options below are retained unchanged ...*
```

### Archive zone (2 files, 3 status fields)

```
ADR-40   [G5:5]   DEPRECATED 2026-05-23.**  (blockquote banner; value bleeds past the bold close onto 3 more lines)
ADR-40   [G3:10]  Deprecated (was: Accepted)
ADR-52   [G1:3]   ~~Accepted~~ Superseded by ADR-53 (2026-05-19)
```

**ADR-40 carries two status fields, in two grammars, at two casings** (`DEPRECATED` vs
`Deprecated`) — the only intra-file status disagreement in the corpus.

---

## Parser hazards this measurement found (each one is a test case in Step 3)

These are the cases that make a naive parser wrong, and the reason the count above is
trustworthy only because each was handled explicitly:

1. **`Status update` is not `Status:`** — `ADR-82:11` opens an amendment marker
   `> **Status update (in-place marker — ...)`. A regex treating the colon as optional
   swallows it as a *second, bogus* status field for ADR-82. The discriminator is that a real
   field has `Status` **immediately** followed by `:`. This false positive was live in this
   lane's own first measurement pass and was caught by inspection, not by the regex.
2. **The value can wrap across physical lines** — `ADR-67:5` ends mid-parenthetical and
   continues on line 6. A line-oriented parser silently truncates it and reports a
   well-formed-looking value that is not the real one.
3. **The key case varies** — `Status:` (86) vs YAML `status:` (ADR-61).
4. **The colon can sit inside or outside the bold** — `**Status:**` vs `**Status: value**`.
5. **The value can carry markup** — `**PARKED**` (ADR-114), `~~Accepted~~` (ADR-52). A raw
   equality test against `"Accepted"` fails on markup that does not change the meaning.

**`[#552]`'s recorded parser hazard is incomplete.** That row names three formats — "bold
`Status:`, list-item bold `Status:`, and YAML frontmatter". It **misses G3-plain, which 12 live
ADRs use** (ADR 34–39, 41, 42, 43, 45, 46, 47), and misses G5 entirely. A parser built to
`[#552]`'s stated hazard returns a false `None` on those 12, not just on ADR-61. Filed below.

---

## Collateral findings (measured, not acted on)

- **Two ADR numbers are used twice.** `ADR-51-architecture-doc-convention.md` +
  `ADR-51-amendment-2026-07-05-llm-first-canonical-docs.md`, and
  `ADR-70-three-tier-process-automation.md` + `ADR-70-amendment-2026-07-07-fable-xl-tier.md`.
  Both collisions are amendment-ADRs deliberately numbered onto their parent. This is a real
  ambiguity for any tool keying on ADR number, and it is **out of this lane's scope** — recorded
  so the next tool author does not discover it the hard way.
- **One filename uses underscores** — `ADR-43_cross_project_transcript_routing.md`, against the
  `ADR-NN-topic.md` convention in CLAUDE.md §4. Not status-related; recorded.
- **ADR-44 does not exist** in either zone. ADR-40 and ADR-52 are archived; 44 is simply absent.

---

## Step 2 — Requirements and prior-art shape

### What ADR-94 actually requires of `[#242]`

Read at `docs/decisions/ADR-94-adr-status-line-mutable-on-ratification.md`. Three clauses bear:

1. **The exception is narrow by construction.** An ADR's *status line* is metadata and MAY be
   edited in place **on ratification**. Decision content stays frozen. Transcripts, handoffs and
   audits remain fully immutable. The ADR's own Consequences section calls the narrowness
   deliberate, and records that a broader "decision content immutable" phrasing was **rejected by
   operator correction** as diluting the other artifact classes.
2. **Retro-normalization is deferred and operator-gated.** Verbatim: *"ADR-88/89 keep their
   frozen `Proposed` headers + markers for now — editing already-ratified history is a separate
   operator-gated task, out of scope here. This ADR governs go-forward."*
3. **`[#242]` is named as the enforcement deferral** — *"no machine check yet reconciles header
   status against README-index effective status, nor enforces Pattern B go-forward."*

So ADR-94 asks `[#242]` for **two legs**: (a) header↔README coherence, (b) Pattern-B go-forward
enforcement. `[#242]`'s own Done-when states only leg (a): *"a seeded ADR with a header↔README
status divergence is flagged by an audit check, with tests."*

**ADR-94 clause 2 is now stale as a statement of fact.** ADR-88/89 were retro-normalized on
2026-08-04 — both headers read `Accepted (ratified 2026-06-21 by operator edit; header flipped
2026-08-04 per ADR-94 Pattern B ...)`. `[#242]`'s row already carries the correction inline
(*"ADR-88/89 now Pattern B; only the go-forward check remains"*). The ADR text is immutable and
correct as of its authoring; recording the change here rather than editing it is the point.

### What `[#362]` covers — and the constraint it puts on this lane

`[#362]` is the **substantive** half, bound to `[#242]`: 49 MUST-rules extracted from the seven
handoff-cluster ADRs (32/37/42/55/56/57/58) were **dropped at the v4→v5 transition with no
successor**, while no document supersedes any of the seven and ADR-32 positively asserts
`Superseded by: none`.

Its Done-when carries a hard ordering constraint on this lane:

> *"and `[#242]` does not reach a terminal status before this row does"*

**This lane therefore cannot close `[#242]`, and does not claim to.** It builds the gate `[#242]`
asks for; the row stays open behind `[#362]`. Stated here so the integrator does not read a
green validator as a closable row.

The constraint is also substantively right, and this lane's measurement is why: a status-only
normalization of the seven handoff-cluster ADRs would write `Superseded` onto files whose
49 dropped guards have no successor — the exact silent discard `[#362]` was filed to prevent.

### Library-first check — the enum is DECLARED, not this lane's to invent

Required by the contract, and it changed the build. `docs/decisions/README.md` §"Status enum"
**already declares the permitted `Status:` domain**, on 2026-08-12, registered at
`protocols/STANDING_RULINGS.md` M-6 / `N2-D2-i`:

| Value | Terminal? |
|---|---|
| Proposed | no |
| Accepted | no |
| Explored, not adopted | no |
| Partially superseded | no |
| **Superseded** | **yes** — archival-eligible at H3's zero-inbound bar |
| **Deprecated** | **yes** — same |

That section also says, in terms: *"Nothing checks this enum — it is a declared domain, not a
gate; **a validator is available work and is not claimed here**."* This lane builds that
validator. **The enum is adopted verbatim; no new vocabulary is minted.**

No new dependency: `pyyaml` and `click` are already in the baseline and already used by the
sibling validators. Nothing here needs `markdown-it-py` or `pydantic` — the field is a single
line, and a line-anchored regex set is both sufficient and the idiom already in use.

**One defect found in the declared enum itself:** the table has six rows, but the same section's
**2026-08-22 update paragraph** states *"`PARKED` is now a live status"* and ADR-114 carries it.
`PARKED` was never added to the table. A validator enforcing the table literally REDs ADR-114 —
which is a correctly-ruled, operator-selected status. **The validator therefore accepts seven
values and names `PARKED`'s declaring site in its own source**, so the divergence is visible at
the point of enforcement rather than buried. Filed as a proposal in Step 5; not repaired here
(the README is not this lane's file, and two sibling rows already touch it).

### Prior-art shape — which validator this one follows

Read for shape: `scripts/validate_onboarding_rulings.py` (the standalone-validator idiom) and
`scripts/audit_checks/check_amendment_coherence.py` (the `ALL_CHECKS` member idiom). This lane
**follows both and diverges from neither** — the fourth-idiom cost the contract warns about is
not paid:

| Idiom element | Source followed |
|---|---|
| `#!/usr/bin/env python` + POSTURE/exit-contract docstring | `validate_onboarding_rulings.py` |
| `click` CLI, `_REPO_ROOT` from `Path(__file__)` | `validate_onboarding_rulings.py` |
| Exit **0** clean / **1** defects / **2** unusable, never-silently-green | `validate_onboarding_rulings.py`; matches the `check_seal_identity` / `check_provider_registry` posture where an internal error **BLOCKS** |
| Pure `load_*` / `*_defects` / `surface_line` split | `validate_onboarding_rulings.py` |
| `Finding(name, status, evidence)` from `audit_checks._common` | `check_amendment_coherence.py` |
| `# rule: <id>` annotation immediately above the `def` (the doc→code edge `_markers_for_check` walks) | `check_amendment_coherence.py` |
| Child-repo-safe skip; honest-enforcement-limit paragraph in the docstring | `check_amendment_coherence.py` |

**Measured divergence: one, and it is forced.** The check module lands in
`scripts/audit_checks/` but the reusable parser lands in `scripts/validate_adr_status.py`,
because the parser is needed by both the check and a standalone CLI run, and
`scripts/audit_checks/` is a PEP-420 namespace package deliberately carrying no `__init__.py`
(`registry.py` records that adding one would change the generated ARCHITECTURE codemap). The
check imports the parser rather than duplicating it — one parser, two callers, matching how
`block_ff_push` and `validate_no_ff` share `find_violations`.

### The governing rulings — located, quoted, and NOT resolved here

Two registered rulings bear on the sweep. Both were found by reading
`protocols/STANDING_RULINGS.md`, not assumed:

- **J-3** *(amendment marker as standard form)* — *"a manifest row flip lands as an appended
  amendment marker … `docs/audits/` is immutable, so a disclosed marker is the route and a
  silent in-place row rewrite is out."* **Its stated basis is `docs/audits/` immutability** —
  the ruling is reasoned from the audit genre, and does not on its face reach an ADR status line.
- **L-11** *(2026-08-12, `ADR-61` carries no parsable status line — recorded, repair deferred)* —
  this one is **directly on point** and is the single most important input to Step 5:

  > *"Ruled 2026-08-12: recorded here; the repair rides ADR-61's next genuine ratification event.
  > **Neither an in-place edit nor an appended marker lands in this arc.** The reasoning is
  > ADR-94's, taken at its word: its in-place exception covers a status line **on ratification**,
  > and **reshaping a status line for a parser's convenience is not a ratification**, so the edit
  > that would fix this has no authorizing event yet. An appended marker was available and is
  > **declined as disproportionate**."*

The tension the contract asked this lane to surface is therefore **narrower than the contract
supposed, and already ruled at its centre** — see Step 5, where the question is put precisely
rather than answered.

---

## Step 3 — The validator

**Landed** (this lane's own files, no shared surface touched):

- `scripts/validate_adr_status.py` — the parser + rules. Read-only, `click` CLI, exit
  **0** clean / **1** defects / **2** corpus-unusable.
- `scripts/audit_checks/check_adr_status_grammar.py` — the thin `ALL_CHECKS` adapter,
  **written but deliberately not registered** (Step 4).
- `tests/test_validate_adr_status.py` — 99 tests.

### Six rules, and what each measures on the live corpus

| Rule | Meaning | Live count | Armed |
|---|---|---|---|
| `enum` | value outside the declared domain | **0** | **FAIL** |
| `single-field` | a file must carry exactly one status field | **0** | **FAIL** |
| `grammar` | not the canonical G1 | **47** | WARN (baseline) |
| `coherence` | header status != README-index effective status | **3** | WARN (baseline) |
| `wrapped-value` | value continues onto the next physical line | **1** | WARN (baseline) |
| `duplicate-id` | two files claim one ADR number | **2** | WARN (baseline) |
| `unindexed` | ADR carries no README-index row | **0** | WARN (baseline) |

Live verdict: `warn` — `coherence=3, duplicate-id=2, grammar=47, wrapped-value=1`, with the two
FAIL-armed legs at zero.

**The three `coherence` hits are real defects, not parser noise** — this is `[#242]`'s
Done-when leg finding actual divergence on its first run:

```
ADR-45  header "Explored, not adopted"  !=  index "Superseded"      (different CLAIMS, not
                                                                     different spellings)
ADR-46  header "Partially superseded"   !=  index "Accepted"        (index states no status)
ADR-47  header "Partially superseded"   !=  index "Accepted"        (index states no status)
```

### Proof it rejects — the contract's named failure mode, tested

The contract warns against *"a validator that passes because it accepts every grammar it
finds."* Two independent proofs:

1. **One rejection test per divergent grammar measured in Step 1** (G2, G3, G4, G5), each
   asserting a `grammar` defect is *raised*, not that the run completed. Plus a rejection test
   per off-enum value, and an acceptance test per declared enum member.
2. **A mutation run — 18 mutations, 18 killed, 0 survivors** (final set, after the terra
   rounds below; see Step 7 for the full roster). Each mutation disables exactly one rule and
   the suite must go RED.

**A first mutation run reported a survivor and it was a false alarm in the harness, not a hole
in the suite** — the mutation was written `return [] or [...]`, which evaluates to the original
list, so it mutated nothing. Recorded because a mutation harness that silently fails to mutate
reports a green suite as rigorous, which is worse than not running one at all.

### A defect this lane found in its own validator

The first implementation keyed the coherence map with `headers.setdefault(adr_number(...))`,
so the two duplicate-numbered files collapsed into their parents — which meant `R_UNINDEXED`
could **never fire** for the only two files it applies to, while the module docstring claimed
the collision was "reported rather than resolved". The code picked a winner silently. Fixed by
a separate `duplicate_id_defects` leg (rule `duplicate-id`, 2 live hits) and the honest limit
rewritten to describe what the code does. Recorded because it is exactly the vacuous-pass class
the gate exists to prevent, found in the gate itself.

---

## Step 4 — Registration (fenced diff — NOT applied by this lane)

`ALL_CHECKS` and its registry are shared with two sibling lanes in this batch, so per the
contract the registration ships as a diff for the integrator, not as an edit.

### Arming decision, and why it is not FAIL

The contract says: *"arm at the level the corpus can actually pass today — if the corpus fails,
arm WARN with a measured baseline and say so; do not arm a gate that RED-blocks every commit on
day one."*

**The corpus cannot pass a FAIL-armed grammar leg: 47 of 87 live ADRs use a non-canonical
grammar.** Arming it would RED `audit-health`, which is a **pre-commit** gate, and wedge every
commit in the repo on day one. So the legs are split rather than blanket-WARNed:

- `enum` + `single-field` arm **FAIL** — both measure 0, so they gate real regressions from
  today without blocking anything, and they are the legs that actually protect the declared
  domain.
- `grammar`, `coherence`, `wrapped-value`, `duplicate-id`, `unindexed` arm **WARN** against the
  baseline recorded above.

**Stated plainly: a WARN with a recorded baseline is a measurement, not a gate.** Nothing stops
the grammar count drifting from 47 to 48. Promoting it needs either a normalization pass (which
needs the Step-5 ruling) or a ratchet on the `silent_rule_ratchet` model. Neither is claimed
here, and the WARN should not be read as one.

### The diff

```diff
--- a/scripts/audit_checks/registry.py
+++ b/scripts/audit_checks/registry.py
@@ from .check_adr38_baseline import check_adr38_baseline
 from .check_adr38_baseline import check_adr38_baseline
+from .check_adr_status_grammar import check_adr_status_grammar
 from .check_amendment_coherence import (

@@ CHECK_ORDER — append at the END (order is the emission contract; appending
@@ perturbs no existing position)
     "check_review_artifact_coverage",     # facade — _is_hub/_REPO_ROOT seam
     "check_landing_predicate",            # facade — DISPOSITION_REGISTER/_is_hub seams
+    "check_adr_status_grammar",           # [#242] ADR status grammar/enum + README coherence
 )

@@ EXTRACTED_CHECKS — append at the end (kept CHECK_ORDER-relative)
     check_boot_byte_budget,
+    check_adr_status_grammar,
 )

@@ __all__ — sorted position is between check_adr38_baseline and check_amendment_coherence
     "check_adr38_baseline",
+    "check_adr_status_grammar",
     "check_amendment_coherence",
```

```diff
--- a/scripts/audit.py
+++ b/scripts/audit.py
@@ the _registry re-export block (~line 233)
 check_adr38_baseline = _registry.check_adr38_baseline
+check_adr_status_grammar = _registry.check_adr_status_grammar
 check_claude_md = _registry.check_claude_md

@@ ALL_CHECKS — append at the END, matching CHECK_ORDER
     check_landing_predicate,   # [#513] propagation-completeness — GATING (FAIL-capable), one
                                # Finding per declared ruling in STANDING_RULINGS.md
+    check_adr_status_grammar,   # [#242] — ADR Status grammar/enum + header↔README coherence.
+                                # enum/single-field FAIL-armed (both measure 0); grammar(47)/
+                                # coherence(3)/wrapped(1)/duplicate-id(2) WARN against the
+                                # baseline in docs/audits/2026-08-23-technical-lane-status-grammar.md
 ]
```

```diff
--- a/ecosystem/doc-code-edge.yaml
+++ b/ecosystem/doc-code-edge.yaml
@@ declaration_docs — the enum is DECLARED in the decisions README; see the note below
   - protocols/HANDOFF_PROCESS.md     # handoff-probes-bind (§5 probe-gate, ADR-82)
+  - docs/decisions/README.md         # governance-adr-status (§"Status enum", declared 2026-08-12)

@@ coverage_scope
   - seal-journal-spine-anchor  # DONE 2-site (ADR-85 amend. 2026-08-03) -- ...
+  - governance-adr-status      # DONE 2-site ([#242]) -- docs/decisions/README.md §"Status enum"
+                               #   -> validate_adr_status.py + audit.py::check_adr_status_grammar

@@ multi_site
   handoff-probes-bind: 2         # audit.py::check_handoff_probes (adapter) + ...
+  governance-adr-status: 2       # validate_adr_status.py (logic) + audit.py::check_adr_status_grammar (adapter)
```

```diff
--- a/docs/decisions/README.md
+++ b/docs/decisions/README.md
@@ immediately above the "## Status enum" heading — the doc-side rule token
+<!-- rule: governance-adr-status -->
 ## Status enum
```

### Everything else the registration drags with it — named, because it is not obvious

The integrator applying the above must also move these, or `audit-health` REDs:

| Site | Change | Why |
|---|---|---|
| `tests/test_audit.py:2207` | `== 43` → `== 44` | ALL_CHECKS count pin |
| `tests/test_audit.py:2223` | `== 43` → `== 44` | second pin in the same file |
| `tests/test_doc_code_edge.py:248` | `== 43` → `== 44` | third pin |
| `tests/test_writer_integrity.py:185` | `== 43` → `== 44` | fourth pin (`test_all_checks_count_is_pinned`) |
| `tests/test_audit_parallel.py:188` | no edit — asserts `ALL_CHECKS == CHECK_ORDER` | passes iff both diffs above are applied together |

**Two judgement calls the integrator should make consciously rather than inherit:**

1. **`declaration_docs` gains a fourth entry.** The three current entries are all
   `protocols/*`. The alternative is to declare the rule in `protocols/PLAYBOOK.md` instead —
   but the enum is genuinely declared in `docs/decisions/README.md`, and restating it in
   PLAYBOOK would create exactly the duplication CLAUDE.md §5 rule 6 names as the drift failure
   mode. Recommended as diffed; flagged because it widens a curated list.
2. **`ARCHITECTURE.md` Ch2 does *not* need a row.** Its pre-commit gate enumeration was retired
   in favour of a pointer on 2026-08-23 (CLAUDE.md §4 M2, after the list proved wrong three
   times). No count lives there to bump. Verified, not assumed.

### Registration is NOT applied here — the honest state

`check_adr_status_grammar` is imported by nothing but its tests until the integrator applies
the diff. Until then **the gate does not run at any level**, WARN included. The validator is
runnable standalone (`py scripts/validate_adr_status.py`) and the tests pin its verdict, so the
measurement is live and regression-protected; the *gate* is not.

---

## Step 5 — Marker sweep: narrow execution, wide proposal

### Executed: NOTHING. Here is the proof that this is the ruled outcome, not an omission.

ADR-94's in-place exception has exactly one trigger: **a ratification event.** Its own words —
*"MAY be edited in place **on ratification** (e.g. `Proposed → Accepted`)"*.

**There is no ratification event anywhere in the live corpus to attach a correction to.** The
Step-1 measurement is the evidence: head tokens are `Accepted` (82), `Partially superseded` (2),
`PARKED` (1), `Explored, not adopted` (1), `Accepted 2026-05-28` (1). **`Proposed`: zero.**
`docs/decisions/README.md` independently states the same — *"the `Proposed` row is empty
again"*. Nothing is awaiting ratification, so ADR-94's trigger is not merely unmet, it is
**unmeetable** for every file in the corpus as it stands.

Standing ruling **L-11** (2026-08-12) closes the remaining gap, and it is directly on point
because it ruled on `ADR-61` — the single worst-formed status line in the corpus, the exact case
a sweep would reach for first:

> *"reshaping a status line for a parser's convenience is not a ratification, so the edit that
> would fix this has no authorizing event yet. An appended marker was available and is
> **declined as disproportionate**."*

So every correction below is a **proposal**. The execution set is empty, and it is empty under
**both** readings of how far L-11 reaches — see the escalation at the end of this step.

### The per-ADR sweep plan

**Class A — grammar normalization (47 ADRs).** Current: G2 (34), G3 (12), G4 (1). Proposed: G1.
Governing basis: **none available.** This is textbook "reshaping for a parser's convenience";
L-11 refuses it and ADR-94 offers no other trigger. **PROPOSED, BLOCKED.**

```
G2 -> G1 (34)  ADR 27,28,29,30,31,32,33,64,65,66,67,68,69,70b,71,72,84,85,86,87,
               88,89,90,91,92,93,102,103,105,106,107,108,109,110
G3 -> G1 (12)  ADR 34,35,36,37,38,39,41,42,43,45,46,47
G4 -> G1  (1)  ADR 61  -- ALREADY RULED, see Class E. Not re-proposed.
```

**Class B — the three header↔index divergences.** These are the defects `[#242]` was filed to
surface, and the correction is on the **index** side in all three, which means they are edits to
`docs/decisions/README.md` — a file this lane does not own and that `[#553]` already holds.

| ADR | Header | Index | Proposed correction | Basis |
|---|---|---|---|---|
| ADR-45 | `Explored, not adopted` | `Superseded` (via `~~title~~ Superseded by …`) | **Fix the index.** A decision that was never taken cannot be *superseded* — nothing replaced it. The header is right. | The ADR body: *"Explored, not adopted; ADR-42 v3.2 remains canonical authority"* |
| ADR-46 | `Partially superseded` | *(no marker ⇒ Accepted)* | **Fix the index** — its row states the fact (*"retained as convention, NOT audit-enforced"*) without ever using the enum token, so a machine reads it as Accepted | Enum declared 2026-08-12; the value is live on the header |
| ADR-47 | `Partially superseded` | *(no marker ⇒ Accepted)* | as ADR-46 | as ADR-46 |

**PROPOSED, not executed** — and note this is the *good* case for the ruling: had the lane
"normalized" these by editing the three headers to match the index, it would have written
`Superseded` onto ADR-45 and erased a real distinction.

**Class C — ADR-67's wrapped status value.** Reflowing lines 5–6 into one physical line changes
no character of content. It is still a status-line edit with no ratification event.
**PROPOSED, BLOCKED.**

**Class D — ADR-40 (archive) carries two status fields.** A `> **Status: DEPRECATED …**`
blockquote banner *and* a `Status: Deprecated (was: Accepted)` plain field, at two casings. The
only intra-file status disagreement in the corpus. Both say Deprecated, so nothing is factually
wrong; the file is simply unparseable by a single-field reader. **PROPOSED, BLOCKED** — and it
is in the archive, where ADR-100's keep-all ruling means nothing is chasing it.

**Class E — ADR-61. Already ruled; deliberately NOT re-proposed.** L-11 ruled on 2026-08-12 that
the repair rides ADR-61's next genuine ratification event, and declined a marker as
disproportionate. **This lane records that the ruling still holds and stops.** Re-proposing a
settled question as though it were open is how a register rots.

**Class F — the declared enum omits a live value.** `docs/decisions/README.md` §"Status enum"
lists six values; its own 2026-08-22 update paragraph declares `PARKED` live (ADR-114) and the
table was never updated. **PROPOSED:** add the `PARKED` row. The validator accepts seven values
today and says so in its source, so nothing is silently absorbed. Adjacent to `[#553]`, which
already holds that section's accuracy.

**Class G — supersession lineage: recorded here, and NOT written to any status line.**

The contract invites this explicitly — *"recording supersession is not changing a decision."*
The lineage is real, well-evidenced, and **entirely absent from the status lines it concerns**:

- `ADR-62`'s own `Related` field states **ADR-42 is "superseded by v4"** and **ADR-55/56/57/58
  are "superseded by v4"**. All five of those ADRs carry a bare `Accepted` status line.
- `ADR-82`'s `Related` field states **ADR-62 is "superseded by v5 *at promotion to canonical*"**
  and **ADR-79**'s heavy-bundle delivery likewise. ADR-82 is `Accepted` and **canonical since
  2026-06-11**, so the stated condition has been **met**. Neither ADR-62 nor ADR-79 records it.

So the corpus knows about at least seven supersessions that no status line carries. This is the
mechanism behind `[#552]`'s "structurally unreachable" finding, seen from the other end: the
archival bar keys on `Superseded`, and nothing ever writes `Superseded`.

**Writing it is nevertheless REFUSED here, and the refusal is `[#362]`'s, not this lane's
caution.** ADR-42/55/56/57/58 are five of the seven handoff-cluster ADRs `[#362]` covers, and
that row's finding is that **49 MUST-rules were dropped at the v4→v5 transition with no
successor**, warning in terms that *"a status-only retirement silently discards these."* Flipping
those five to `Superseded` is precisely the silent discard. `[#362]` further binds *"`[#242]`
does not reach a terminal status before this row does."*

ADR-62 and ADR-79 are **not** in `[#362]`'s named seven, so their conditional supersessions are
the two nearest to actionable — but both are handoff-process ADRs sitting in the same v4→v5
transition `[#362]` is auditing, so this lane treats them as inside the blast radius and
proposes rather than acts. **Recorded, not written.**

### The escalation — named precisely, and NOT resolved

The contract requires this question be handed up rather than answered.

**The question:** *Does L-11's reasoning bind the whole ADR corpus, or only ADR-61?*

L-11 ruled on one file. Its **reasoning** — "reshaping a status line for a parser's convenience
is not a ratification" — is general and, taken generally, permanently blocks Class A: 47 ADRs
would each wait for a ratification event that, for a long-Accepted ADR, will never come. The
grammar leg would then be a WARN forever by construction, not by deferral.

Taken narrowly, L-11 settles ADR-61 only, and Classes A/C/D fall to **ADR-94 clause 2**, which
calls retro-normalization *"a separate operator-gated task"* — available, but requiring an
operator act this lane does not hold.

**What is NOT in question, and why this lane completed anyway:** the execution set is **empty
under both readings** — narrow or broad, nothing authorizes *this lane* to touch a status line.
The fork does not gate this lane's work; it gates whichever act comes next. That is why the
question is handed up rather than blocked on.

**A precision worth keeping:** standing ruling **J-3** (the amendment-marker ruling the contract
names as the live conflict) is reasoned *from `docs/audits/` immutability* — *"`docs/audits/` is
immutable, so a disclosed marker is the route"*. On its face it governs the audit genre, not ADR
status lines, and **L-11 already declined the marker route for an ADR status line specifically**,
as disproportionate. So the J-3-vs-ADR-94 conflict the contract anticipated is, for this subject
matter, **narrower than supposed and already adjudicated at its centre**. The open fork is the
scope of L-11, not the collision of J-3 with ADR-94.

---

## Step 6 — Archival-eligibility state after the gate

This is the answer the archival demand has been waiting on, and it is not the expected one.

### The bar has two conditions, not one

Standing ruling **H3**: *"A terminal-status ADR (`Superseded` / `Deprecated`) moves to
`docs/decisions/archive/` when its inbound reference count is zero. A live prose reference
elsewhere in the corpus holds it in place."*

- **Condition 1 — terminal status.** Carried by **zero** live ADRs (Step 1). Nothing is
  eligible on the status axis.
- **Condition 2 — zero inbound references.** Measured below. Fails for every candidate,
  independently and by a wide margin.

### Archival-eligible today: ZERO ADRs. And fixing every status line would not change that.

Inbound reference counts for the twelve archival candidates, measured across 1,860 files
(`docs/`, `protocols/`, `templates/`, `.claude/`, `ecosystem/`, `scripts/`, `deploy/`, plus the
root living docs) at merge base `aeec0fd1`. Self-references excluded. Two readings, because H3
says *"live prose"* and the corpus contains a great deal of immutable historical record:

| ADR | All refs | **Live-prose refs** (audits / handoffs / JOURNAL / archives excluded) |
|---|---|---|
| ADR-32 | 191 | **45** |
| ADR-37 | 177 | **49** |
| ADR-42 | 372 | **54** |
| ADR-55 | 62 | **15** |
| ADR-56 | 36 | **10** |
| ADR-57 | 42 | **8** |
| ADR-58 | 46 | **8** |
| ADR-62 | 69 | **11** |
| ADR-79 | 35 | **15** |
| ADR-45 | 237 | **21** |
| ADR-46 | 173 | **12** |
| ADR-47 | 204 | **22** |

**Under the strictest reading available to it, every candidate fails H3's second condition.**
The narrow reading was constructed deliberately to give archival its best case — excluding
audits, handoffs, JOURNAL, `protocols/archive/`, `templates/archive/`, intake and ecosystem
history — and the minimum is still **8**.

### So the binding constraint was never the status grammar

This lane was dispatched on the premise that unparseable status is *why* archival is blocked.
**That premise is half right and the more important half is wrong.** The status axis was
genuinely unmeasurable before this gate, and now it is measurable. But the reference axis is
what actually holds every candidate in place, and it is untouched by anything this lane could
have done. Had the sweep normalized all 47 grammars and written `Superseded` onto all seven
handoff-cluster ADRs, **zero files would have become archival-eligible.**

### A structural finding H3 should probably absorb

Most live-prose references to these ADRs come from **other ADRs** — ADR-42 is held by ADR-45
(22) and ADR-39 (8); ADR-37 by ADR-36 (11) and ADR-41 (10); ADR-32 by ADR-39 and ADR-41 (7
each). A decision record citing its predecessor is what an ADR corpus *is*.

Read literally, then, H3's zero-inbound bar makes the ADR corpus **permanently unarchivable**:
the citation that holds a file in place is the same citation that makes it a decision trace.
H3's own expiry clause says it *"retires when a mechanism computes the inbound count at archival
time"* — and this measurement is a preview of what that mechanism would return: **non-zero, for
everything, forever**, unless the bar is refined to exclude sibling-ADR citation. Recorded, not
proposed as a change; H3 is a standing ruling and re-scoping it is not this lane's act.

### What is blocked, on what, and who owns it

| Blocked | On what | Owner |
|---|---|---|
| All 47 grammar normalizations | No authorizing event (ADR-94 needs a ratification; L-11 refuses parser-convenience reshaping) | Operator — the L-11 scope question in Step 5 |
| Writing `Superseded` on ADR-42/55/56/57/58 | `[#362]` — 49 dropped MUST-rules with no successor; a status-only retirement discards them | `[#362]` |
| `[#242]` reaching a terminal status | `[#362]`'s Done-when binds it explicitly | `[#362]` |
| The three index corrections (ADR-45/46/47) | `docs/decisions/README.md` is not this lane's file | `[#553]` |
| Adding `PARKED` to the enum table | same file | `[#553]` |
| **Archival of anything** | **H3 condition 2 — 8–54 live refs per candidate** | Operator / an H3 refinement |

### What this lane actually unblocked

Narrower than the dispatch supposed, and real:

1. **The status axis is measurable for the first time.** `docs/decisions/README.md` declared an
   enum on 2026-08-12 and said in terms that nothing checked it. Now something does.
2. **Three genuine header↔index divergences surfaced** (ADR-45/46/47) — `[#242]`'s Done-when
   finding real defects on its first run, not a synthetic seed.
3. **The moment any ADR does become terminal, the gate says so** — and the `enum` +
   `single-field` legs are FAIL-armed, so a regression cannot land silently.
4. **The archival question is answered with evidence instead of deferred again.** The answer is
   "zero, and the blocker is H3's reference bar, not the grammar."

**`[#242]` is NOT closed by this lane** — `[#362]` forbids it, and leg (b) of ADR-94's ask
(Pattern-B go-forward enforcement) is only partly served: the gate detects a non-canonical
grammar, but it cannot detect that a *flip* used Pattern A rather than Pattern B, because a
correctly-executed Pattern-B flip and a file that was always `Accepted` are byte-identical.
That distinction needs commit history, which this check does not read. Stated rather than
claimed as done.

---

## Step 7 — terra review

**Reviewer:** `gpt-5.6-terra` via `codex exec --sandbox read-only`, reasoning effort `high`,
model pinned exactly as `~/.claude/bin/codex-review.ps1` pins it (S19). Invoked directly rather
than through `/codex-review`: that command writes its artifact into `docs/audits/` and this
lane's diff is mixed code+docs, which is the recorded failure mode for it.

### Tally

| Round | Critical | High | Medium | Low |
|---|---|---|---|---|
| 1 | 0 | 5 | 0 | 0 |
| 2 | 0 | 3 | 2 | 0 |
| 3 | 0 | 2 | 1 | 0 |
| 4 | 0 | 2 | 0 | 0 |
| 5 | 0 | 2 | 3 | 0 |
| 6 | 0 | 2 | 1 | 0 |
| **7 (final)** | *(pending — filled from the round-7 artifact)* | | | |

**Running total after 6 rounds: 0 Critical, 16 High, 7 Medium — every one fixed, each with a
regression test naming the round and the concrete failing input.** Counts are taken from the
artifact files, not from any console tally.

### What the rounds actually found — a summary, because the pattern matters

Every High was a **false verdict**, in one of two directions, and both directions are serious
for a gate armed at FAIL:

- **False PASS (a bad value laundered into a good one):** `~~Accepted~~ Superseded by ADR-53`
  normalizing to `Accepted` — inverting the only genuinely superseded ADR in the corpus;
  `A_ccepted`, `Acceptedness`, `Acce*pted`, `**Accepted` all reaching `Accepted`; a missing
  README silently returning `pass` with the coherence leg unrun; duplicate ADR numbers
  collapsing so one file's status was never compared.
- **False FAIL (a good file blocked):** a `Status:` line quoted inside a code fence firing BOTH
  FAIL-armed legs and REDDING the pre-commit gate on a legitimate ADR; `****Accepted****`
  (valid nested emphasis) rejected as off-enum; ADR-72's `**Amends (does not edit):**` line
  misread as a wrapped value.

### The measurement never moved

The strongest evidence the fixes were correctness-only rather than baseline-shifting: across
every round and all 23 fixes, the live corpus verdict was byte-identical every time —

```
87 status field(s); coherence=3, duplicate-id=2, grammar=47, wrapped-value=1
```

The one time a count did move — `wrapped-value` briefly 1 → 2 — it was a **false positive
introduced by a fix** (ADR-72), caught by re-measuring after every change, and reverted to 1
by tightening the rule rather than by accepting the new number.

### Mutation check — 26/26 killed, 0 survivors

Each mutation disables exactly one rule; the suite must go RED. The final run applies all 26
cleanly and kills all 26.

**Two honest notes about the mutation runs themselves**, because a mutation harness that
silently fails to mutate reports a green suite as rigorous:

1. An early run reported a survivor that was **a harness bug, not a test hole** — the mutation
   was written `return [] or [...]`, which evaluates to the original list.
2. A later run found a **genuine test hole**: reverting the round-6 archive fix survived,
   because nothing covered the `--include-archive` duplicate path. That hole is closed by
   `test_cli_include_archive_folds_archive_missing_into_duplicate_detection`, and the mutation
   now dies. **The mutation run found a gap the review had not.**

### Review-driven test growth

48 tests at first green → **123** at final. The additions are almost entirely regression tests
carrying the reviewer's own failing inputs, so a future edit reintroducing any of the 23
defects fails loudly rather than silently.
