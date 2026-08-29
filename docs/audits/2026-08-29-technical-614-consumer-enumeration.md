# [#614] lane-b — the gate-coupled consumer enumeration, BEFORE any edit

**Lane:** `lane-b-614-vision-to-readme` · branch `worktree-lane-b-614-vision-to-readme` · batch D.
**Contract of record:** `docs/audits/2026-08-29-technical-batchd-launch-contracts/LANE-b-614-vision-to-readme.md`,
sha256 `a17261a0d217727c1779d0cbfffd8cf99c703927a77fe4b30e533180a1b61ca8` — verified byte-identical
to the dispatched copy at `~/Downloads/LANE-b-614-vision-to-readme.md` before any work started.
**Authority:** ADR-114, **Accepted 2026-08-29** (AMENDMENT 1), `[#614]`.
**Source census:** `docs/audits/2026-08-29-census-nb2-readme-vision.md` (C5).
**Why this file exists:** done-contract item 1 — *"The enumeration is the lane's FIRST ARTIFACT, not
an implementation detail… enumerated from the C5 census before any edit — ADR-114 AMENDMENT 1 says
this verbatim."* Nothing in the tree was edited before this file was committed.

---

## 0. Premise check (Q10) — the premise HOLDS

The contract's premise is that the supersession is *ruled*. Verified live, not assumed:

```
docs/decisions/ADR-114-readme-recreation-legality.md:3
  Status: **Accepted** — ruled by the operator 2026-08-29, superseding the 2026-08-22 PARK.
docs/decisions/ADR-114-readme-recreation-legality.md:161
  ## AMENDMENT 1 — 2026-08-29, the operator's ruling. ADR-114 is DECIDED.
  "VISION.md is superseded by a recreated root README.md (this DECIDES parked ADR-114)."
```

The C5 census (written against `fcc9485`, when ADR-114 was still PARKED) quotes *"Until it is ruled,
nothing in this repo may cite ADR-114 as authority"*. **That clause is spent** — the ruling landed the
same day. The census's *measurements* stand; its *constraint framing* is superseded by AMENDMENT 1.
No PAUSE is owed.

---

## 1. Method

Every row below is (a) named by C5 §3.A.1 / §6 as a gate-coupled consumer of `VISION.md`, and
(b) **re-resolved live in this worktree** before being written down — `CLAUDE.md` §4's
*"Resolve a locator before you act on it"*, which C5 itself quotes and which binds the enumerator
too. Two census locators had drifted since `fcc9485` and are corrected inline (marked **DRIFT**).

The verdict column is a closed enum:

- **RE-POINT** — changed by this lane (inside the frozen write-scope).
- **HOLD** — deliberately unchanged, because `VISION.md` **stays on disk** (§3). Not deferred work;
  the constant keeps pointing at a file that keeps existing, so the constant stays true.
- **DEFER** — genuinely owed, genuinely outside this lane's frozen write-scope. Each DEFER is
  carried by a row filed in §6.

---

## 2. The enumeration — every gate-coupled consumer of `VISION.md`

### 2.1 The registry and the ten machine constants (C5 §6)

`scripts/canonical_docs.py` is the single table the ten constants read. Verified live:

```
CONSUMER (locator verified in this worktree)          GATE IT FEEDS                        VERDICT
scripts/canonical_docs.py:40  VISION = "VISION.md"    all ten, transitively                HOLD
scripts/canonical_docs.py:54  README = "README.md"    check_canonical_md_visibility        HOLD
scripts/canonical_docs.py:67  CANONICAL_MANDATORY     check_adr38_baseline,                HOLD
                                                       check_canonical_md_visibility,
                                                       validate_hermetization Rule A (:103)
scripts/canonical_docs.py:81  FRESHNESS_FILES         canonical_freshness_gate, audit #10  HOLD
scripts/canonical_docs.py:86  SECTION_HISTORY_DOCS    validate_doc_rot                     HOLD
scripts/canonical_docs.py:93  STRUCTURE_DOCS          validate_doc_structure               HOLD
scripts/canonical_docs.py:99  BACKPRESSURE_CANON      session_end_backpressure             HOLD
scripts/canonical_docs.py:103 CONFORMANCE_V2_SCAN     conformance-hub.js seam S11          HOLD
scripts/canonical_docs.py:109 CANONICAL_SPINE[VISION] check_canonical_structure + 5        HOLD
                              = the five ## H2s        deploy manifests
scripts/canonical_docs.py:126 VISION_EXTRACT_HEADING  gen_handoff._vision_extract          HOLD
scripts/canonical_docs.py:127 VISION_EXTRACT_MISSING  gen_handoff degrade string           HOLD
scripts/canonical_docs.py:2-13  MODULE DOCSTRING      none (prose)                         RE-POINT
```

**Only the docstring moves.** It currently asserts *"Whether `VISION.md` is ever renamed is an open
operator decision (R2 §1.5 records it as NO-GO as briefed)"* — **false since 2026-08-29**. That
sentence is the one thing in this file the ruling falsifies; every constant below it stays true
because `VISION.md` stays tracked (§3).

### 2.2 The consumers that read the registry (all HOLD, all verified live)

```
scripts/audit_checks/check_vision_md.py:26-27     audit.py check #1              HOLD
scripts/audit_checks/check_adr38_baseline.py:37   audit.py adr38_baseline        RE-POINT (docstring only)
scripts/canonical_freshness_gate.py:49            deploy-carried SOFT fallback   HOLD
scripts/session_end_backpressure.py:145           deploy-carried SOFT fallback   HOLD
scripts/consumer_at_landing.py:124                landing canonical tuple        HOLD
scripts/nopack_sandbox.py:226                     sandbox seed list              HOLD
scripts/gen_handoff.py:553-566, :650, :1163       VISION_EXTRACT slot            HOLD
.claude/workflows/conformance-hub.js:133          JS literal (test-held)         HOLD
deploy/manifest-v1.1.0.yaml:389                   doc_shapes spine               HOLD
deploy/manifest-v1.2.0.yaml:604                   doc_shapes spine               HOLD
deploy/manifest-v1.3.0.yaml:669                   doc_shapes spine               HOLD
deploy/manifest-v1.3.1.yaml:678                   doc_shapes spine               HOLD
deploy/manifest-v1.4.0.yaml:810                   doc_shapes spine               HOLD
ecosystem/disposition-register.yaml:113, :255      scan_undeclared_edges keys     HOLD
```

`scripts/audit_checks/check_adr38_baseline.py` carries **no `README.md` literal** — `required_files`
is derived from `canonical_docs.ADR38_BASELINE_REQUIRED` (`:37`). Its **docstring** is the ADR-114
decommission surface (c): *"README.md is optional (deprecated from the baseline)"*. Docstring only.

### 2.3 The gate that would BLOCK the recreation

```
scripts/validate_hermetization.py:97 SANCTIONED_TIER1_FILES     pre-commit validate-hermetization
```

Rule A (`:261-271`) BLOCKS any added top-level file not in this frozenset. `README.md` is absent from
it today, so `git add README.md` is refused at commit time. **RE-POINT** — and this is ADR-114's
`Amends` line firing (*"the closed Tier-1 file enum in `SANCTIONED_TIER1_FILES` gains `README.md`"*).

**Shape, chosen on a landed precedent rather than invented.** `README.md` is added as a **literal**,
exactly as `AGENTS.md` was under ADR-115 (`:116-118`: *"DELIBERATELY a literal and NOT a member of
`_cdocs.CANONICAL_MANDATORY`"*). It is **not** promoted into `CANONICAL_MANDATORY`, because that
tuple is pinned by `tests/test_canonical_docs.py:53` and by `tests/test_audit.py:193-194`
(*"README.md is optional post-amendment (A5) — its absence does not fail the check"*), and
`tests/**` is **lane-a's frozen write-scope in this same batch**. Membership migration is §6 row (c).

### 2.4 The nine-member parity surface

```
ecosystem/parity-surfaces.yaml:164-174   id: canonical-doc-vision
                                          tier: {hub: MUST, consumer: MUST}
                                          probe: {type: path_tracked, path: VISION.md}
```

**DRIFT vs the census.** C5 §3.A.1 and ADR-114's decommission clause both cite `:140-150`; the row is
at **`:164-174`** in this worktree. Corrected here, and this is the second time this one row's
locator has moved (ADR-114 cited `:133-139`, C5 corrected it to `:140-150`, it is now `:164-174`).

**RE-POINT — the `reason:` and provenance, NOT the probe path.** The measurement that decides this:

```
consumer README.md presence, measured on the operator's disk 2026-08-29:
  terminal-setup  YES      ai-council      no      corp-ops                  no
  win-tooling     YES      corp-monorepo   no      corp-sca-time-automation  no
                                            demo-prep no    life-architect   no
  -> 2 of 8 consumers carry a root README.md
```

Flipping `probe.path` to `README.md` at `consumer: MUST` would turn **six of eight** consumers RED
in one commit. The done-contract restates the tier as `{hub: MUST, consumer: MUST}` — i.e. the tier
does **not** move — and warns that *"a partial resolution breaks parity fleet-wide"*. The row is a
single fleet-wide declaration, so the **one act** that resolves all nine is re-authoring the row so
it is *truthful after the supersession*: `VISION.md` is still tracked in all nine, still MUST in all
nine, and the row now records that the hub's front door is `README.md` and that the fleet-wide
filename migration is a sequenced program (ADR-114's option (C) nine-repo program), not a flag flip.
No new `canonical-doc-readme` row is added: at `consumer: MUST` it REDs six members, and at
`consumer: MAY` it is not the row the done-contract names.

### 2.5 The P1a boot probe (done-contract item 2)

```
templates/handoff/v5/PROBES.md.tmpl:81
  | P1a | … opening sentence of `VISION.md` `## Vision` … | grep -A4 '^## Vision' VISION.md |
docs/handoffs/2026-08-28-dev-knowledge-architect/PROBES.md:64   (rendered, IMMUTABLE — untouched)
```

`.claude/commands/handoff-verify.md:78` and `:99` name P1a but carry no `VISION.md` path literal at
the probe line; the **template is the only mutable authoring site**. **RE-POINT — and this is the
lane's one declared footprint extension; see §5.**

### 2.6 The three ADR-114 decommission surfaces (done-contract item 6)

ADR-114 header `:10` names them; all three are inside the frozen write-scope:

```
(a) CLAUDE.md:99  §5 rule 5 "… — do not recreate it"                       RE-POINT
(b) ARCHITECTURE.md — the echo of it                                       RE-POINT (see DRIFT)
(c) scripts/audit_checks/check_adr38_baseline.py:27-28 docstring           RE-POINT
```

**DRIFT vs the ADR, confirming C5 §5 D-4.** ADR-114 cites the echo at `ARCHITECTURE.md:366`.
`grep -n "recreate" ARCHITECTURE.md` returns **no match**. The surviving statement is
**`ARCHITECTURE.md:478`** (*"root `README.md` deleted 2026-05-23 (ADR-38 A5)"*) — a deletion record,
not the *"do not recreate"* echo the ADR describes. C5's read is confirmed: decommission item (b) is
**already discharged by attrition**; what remains at `:478` is a stale *fact*, which this lane
corrects. `ARCHITECTURE.md:1187` additionally still reads **"ADR-114 … PARKED 2026-08-22"** —
falsified by AMENDMENT 1 the same day, and not named by any census. **RE-POINT.**

### 2.7 The mutable-but-not-gate-coupled `VISION.md` citers (C5 §3.A.1 LIVE class)

`protocols/{ESSENTIALS,HANDOFF_BOOT,HANDOFF_PROCESS,DEFINITION_OF_DONE,ENVIRONMENT,PLAYBOOK}.md`,
`templates/child-methodology-floor.md.tmpl:40`, `templates/handoff/03_PROJECT.md.tmpl:15`,
`.claude/commands/handoff.md:111`, `.claude/commands/handoff-verify.md:99`, `tasks/` (4).

**HOLD, every one.** They are navigation pointers to `VISION.md`, which still exists. None is
gate-coupled; none is in the frozen write-scope; `protocols/**` is *hot* in this batch (lane-d owns a
`PLAYBOOK.md` line, lane-e censuses `ESSENTIALS`). Re-pointing prose is the fleet-wide migration
program, §6 row (b).

---

## 3. The executed shape, and why `VISION.md` is not deleted in this lane

`[#614]`'s row names four acts: create `README.md`; migrate the live-normative content out of
`VISION.md`; re-point every gate-coupled consumer; **archive `VISION.md`**. The **frozen contract's
Steps name only the first three** and its done-contract names no archival. The write-scope lists
`VISION.md` as an *editable* file, not a removed one.

That is not an oversight, and the enumeration above is what proves it. `VISION.md`'s removal would
break, in one commit and all outside this lane's write-scope: `check_vision_md` (audit #1),
`check_adr38_baseline` (via `ADR38_BASELINE_REQUIRED`), `check_canonical_structure` (the five-H2
spine, mirrored in **five** live deploy manifests), `canonical_freshness_gate` + audit #10,
`validate_doc_rot`, `validate_doc_structure`, `session_end_backpressure`, `consumer_at_landing`,
`nopack_sandbox`, `gen_handoff._vision_extract`, `conformance-hub.js`, the ×9 parity MUST row, and
**91 test occurrences in `tests/`, which is lane-a's frozen write-scope**.

**So the executed shape is:**

1. `README.md` is created and carries the **live-normative** content — including the `## Vision`
   H2, so P1a re-points to a real section and the probe passes for the right reason.
2. `VISION.md` **stays tracked**, marked SUPERSEDED, keeping its frontmatter and its five-H2 spine
   (`## Vision · ## Scope · ## Values · ## Lifecycle · ## References`) so every HOLD row above stays
   true, with the normative body replaced by pointers into `README.md` — migrated **out**, not
   duplicated. `CLAUDE.md` §4's anti-duplication rule is the reason the bodies are pointers.
3. The fleet-wide filename migration — the constants, the manifests, the tests, the prose citers,
   the parity probe path, and `VISION.md`'s eventual archival — is ADR-114 option (C)'s nine-repo
   program, filed as §6 row (b). **This lane executes the hub's front-door half; it does not
   pretend to execute the fleet's.**

`gen_handoff._vision_extract` is the one **content** dependency (C5 §3.A.1): it regex-copies
`VISION.md`'s `## Vision` body into every new handoff bundle and **degrades to a literal string
rather than raising**. After this lane it extracts the supersession pointer — correct and honest,
not a degrade. Making it read `README.md` is `scripts/gen_handoff.py`, **lane-a's write-scope**;
§6 row (b) carries it.

---

## 4. Files this lane will NOT touch (done-contract item 5)

**ZERO immutable or append-only files.** Verified as a class, not per-file: no edit lands in
`docs/decisions/`, `docs/handoffs/`, `docs/audits/*` (other than this new artifact and the lane's
end packet, both **adds**), `docs/archive/`, `docs/intake/`, `JOURNAL.md`, `LESSONS.md`,
`logs/TOKEN-LOG.md`. C5's arithmetic is the reason: **~5,881 references, ~5,700 of them in files the
repo forbids editing.**

Also untouched, and named so the absence is not read as an oversight: `tests/**` and
`scripts/gen_handoff.py` (**lane-a**), `.claude/generated/**` (**lane-c**), `codex/**` (**lane-d**),
`docs/intake/**` + `docs/decisions/**` (**lane-f**). Checked against every batch-D contract's
Write-scope block at freeze.

---

## 5. Two contract-internal conflicts, disposed rather than discovered later

The contract's **done-contract is immutable** and its **write-scope is frozen**. Two done-contract
items mandate an act on a file the write-scope does not list. Both are recorded here, before the
edit, with the disposition and the reason.

**C-1 · The P1a boot probe (done-contract item 2) vs the write-scope.**
Item 2 requires the probe *"re-pointed, then EXECUTED against the new `README.md`"*. Its only mutable
authoring site is `templates/handoff/v5/PROBES.md.tmpl:81`, which the write-scope omits. The rendered
copy in the active bundle is immutable (item 5 forbids touching it), so the obligation is
dischargeable **nowhere else**. Disposition: **the template line is edited**, one line, P1a only.
Basis: (i) the done-contract is the superior instrument — it is labelled *immutable* while the
write-scope is an ex-ante enumeration, and item 1 exists precisely because that enumeration could not
be complete before the census pass; (ii) **collision risk measured at zero** — no batch-D lane
declares `templates/**` in its write-scope. This is a **declared footprint extension**, reported in
the commit body and the end packet, not a silent one.

**C-2 · The three backlog rows (done-contract item 6) vs the write-scope.**
Item 6 requires ADR-114's three decommission surfaces each to become a backlog row; `tasks/` and
`BACKLOG.md` are not in the write-scope. Same disposition, same basis (no batch-D lane declares
`tasks/`). The rows filed are the **residuals** — the part of each surface this lane genuinely
cannot finish — not born-closed ceremony; see §6.

**Neither is escalated.** The V-2 budget escalates on (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. These are neither: they are
conflicts *within one instrument*, resolved by that instrument's own stated hierarchy, with the
blast radius measured. They are reported, per *"decided per contract defaults and reported in the end
packet rather than asked"*.

---

## 6. The three rows (done-contract item 6 · ADR-114 `:10`)

Each surface is **decommissioned in this lane**; each row carries what is left over.

- **(a) `CLAUDE.md` §5 rule 5's *"do not recreate it"*** — decommissioned here. **Residual:** the
  prohibition's fleet-wide copies. The clause sits **repo-owned** in this hub's `CLAUDE.md` (verified:
  it is between the `critical-rules-records` end-marker at `:98` and the `critical-rules-consistency`
  start-marker at `:100`, so **no lockstep template act is owed** and `templates/claude-regions/`
  is untouched) — but ADR-38 A5's deprecation is fleet doctrine and eight consumers still inherit it.
- **(b) `ARCHITECTURE.md`'s echo** — discharged by attrition (§2.6); the stale deletion fact at
  `:478` and the stale PARKED verdict at `:1187` are corrected here. **Residual:** ADR-114 option
  (C)'s **nine-repo filename migration program** — the ten machine constants, five deploy manifests,
  `gen_handoff._vision_extract`, the 91 `tests/` occurrences, `conformance-hub.js`, the parity probe
  path, the mutable prose citers of §2.7, and `VISION.md`'s archival.
- **(c) the `README.md`-is-optional docstring in `check_adr38_baseline.py`** — decommissioned here.
  **Residual:** `README.md`'s membership in `canonical_docs.CANONICAL_MANDATORY` /
  `ADR38_BASELINE_REQUIRED`, blocked today by three test pins inside **lane-a's** frozen write-scope
  (`tests/test_canonical_docs.py:53`, `tests/test_audit.py:193-194`, `:323-329`).

---

## 7. Reproduce

```bash
sha256sum docs/audits/2026-08-29-technical-batchd-launch-contracts/LANE-b-614-vision-to-readme.md
sed -n '3p;10p;161,164p' docs/decisions/ADR-114-readme-recreation-legality.md
sed -n '40,129p'  scripts/canonical_docs.py
sed -n '97,120p'  scripts/validate_hermetization.py
grep -n "canonical-doc-vision" -A 10 ecosystem/parity-surfaces.yaml
sed -n '81p'      templates/handoff/v5/PROBES.md.tmpl
sed -n '99p'      CLAUDE.md
grep -n "recreate" ARCHITECTURE.md ; sed -n '478p;1187p' ARCHITECTURE.md
grep -n "VISION" scripts/canonical_freshness_gate.py scripts/session_end_backpressure.py \
                 scripts/consumer_at_landing.py scripts/nopack_sandbox.py \
                 .claude/workflows/conformance-hub.js
grep -n "VISION.md" deploy/manifest-v*.yaml ecosystem/disposition-register.yaml
grep -n -A 12 "Write-scope" docs/audits/2026-08-29-technical-batchd-launch-contracts/LANE-*.md
```

**Consumer:** `[#614]`, ADR-114 (AMENDMENT 1), `docs/audits/2026-08-29-census-nb2-readme-vision.md`.
