<!-- scope: meta -->

# DRAFT — night2-A hygiene sweep (`.dev-knowledge`)

> **THIS DOCUMENT IS A DRAFT AND BINDS NOTHING.** Every item below is a **PROPOSAL** for
> architect adjudication. No fix was executed, no row was filed, no register entry was
> written, and nothing outside this file was edited. The §1 register entries are
> **paste-ready but unpasted** — they are drafted in the live
> `ecosystem/disposition-register.yaml` schema so one adjudication pass can accept, amend or
> discard each without re-authoring it. Adopting any of them is a separate, ruled act.

**Sweep:** night2-A read-only hygiene · **Branch:** `claude/night2-hygiene-sweep-8zgyjx`
**Base:** `7bbb06748` (2026-08-14) · **Derived:** 2026-08-14, all figures re-derived live, not quoted.

---

## 0. Method, and two environment corrections that change the numbers

Everything below was re-derived by running the organs, not by reading prior reports. Two
environment facts materially affected the derivation and are stated up front, because a
reader who skips them will mis-rank the findings.

**0.1 — The clone arrived SHALLOW, and a shallow clone makes this gate lie.**
The container cloned the hub at depth-limit (318 commits; `.git/shallow` present). The first
`ship-gate` run on that tree reported **3 hard-fail organs**. After `git fetch --unshallow`
(5043 commits) the same command on the same working tree reported **1**. The two runs differ
only in available history. What the shallow clone fabricated:

```
canonical_freshness  FAIL "6 stale (edited since review)"  -> OK  (9 canonical files fresh)
journal_spine_anchor FAIL "backstop could not complete"    -> OK  (floor 24882f8cc unreachable)
no_ff_merges         WARN 4bef950fe (a --no-ff merge)      -> the 3 real, already-dispositioned commits
```

All three were **artifacts of missing objects**, not repo state. This is the documented
shallow-clone false-positive class (PLAYBOOK Ch11 "The shallow-clone false-positive class"),
observed here in a new place: it hit `canonical_freshness` and `journal_spine_anchor`, not
just a SHA-existence verifier. **Every number in this report is from the post-unshallow run.**

**0.2 — Four of the 45 WARNs are container artifacts and are NOT repo defects.**
This container has no sibling repos and never ran the `SessionStart` `arm_hooks.py` self-arm,
and it cloned the hub to `/home/user/dev-knowledge` rather than `.dev-knowledge`. Those facts
alone produce 4 WARNs (and the single remaining `hooks_armed` hard FAIL). They are itemised
in §1 and explicitly marked **do not paste** — a register entry keyed to a container-only
signature would match nothing on the operator's host and decorate stale on its first run
(ADR-75), which is precisely the paper-suppression rot the register forbids.

**0.3 — Toolchain deviation (disclosed).** `pyproject.toml` pins `uv==0.11.19`
(ADR-106); that version is not resolvable in this container, so `uv sync --locked` could not
run. The organs were executed under an isolated interpreter built outside the repo tree with
the `[dependency-groups] dev` packages installed by name. Dependency *resolution* therefore
was not lock-pinned. No repo file was touched by this, and the scratch interpreter lives
outside the tree (CLAUDE.md §5 rule 9, no leftovers). Re-derivation on the operator's pinned
environment is the authoritative run; the counts here should be treated as high-confidence
but environment-caveated.

Commands used: `python scripts/audit.py ship-gate` · `pytest --collect-only -q` ·
`python scripts/gen_doc_counts.py --check` · `gen_audit_index/gen_intake_index/`
`gen_claude_rosters/generate_organ_index/gen_methodology_roster --check` · `git log` per file.

---

## 1. Undispositioned ship-gate WARNs — 45 live (brief expected ~41)

`python scripts/audit.py ship-gate` → `RED — not shipped-ready (1 hard-fail organ(s); 45
new/undispositioned WARN(s))`. The 45 were extracted by re-using the gate's own
`_load_dispositions()` / `_match_disposition()` rather than by parsing its stdout, so this
inventory is the gate's set, not a lookalike.

### 1.1 By check

```
doc_rot                        38   (37 backlog-accretion rows + 1 CLAUDE.md file-budget)
fleet_parity                    3   (ALL 3 container artifacts)
doc_claims                      1   (the §2 P6 drift — same defect, two surfaces)
deployed_methodology_version    1   (container artifact)
journal_spine_anchor            1   (advisory-by-design, 401 commits)
review_artifact_coverage        1   (one unreviewed code-impact merge)
                               --
                               45
```

### 1.2 By owner row

Only 3 of the 45 have an owning BACKLOG row; the rest are unowned drift. Stated plainly
because "classify by owner row where one exists" mostly returns *none*, and that absence is
itself the finding — 42 of 45 WARNs have no ticket carrying them.

```
[#524] leg c   -> journal_spine_anchor (the mention-not-record advisory this row shipped)
[#480] P3      -> review_artifact_coverage (the advisory leg; hard leg deferred by that ruling)
#222           -> doc_claims pytest_collected (the decoupled-counts locus #222 built)
(no owner)     -> all 38 doc_rot + all 3 fleet_parity + deployed_methodology_version  = 42
```

### 1.3 The single highest-value finding: 26 of 45 are one mis-calibrated threshold

**37 of the 45 WARNs (82%) are `doc_rot` backlog rows, and 26 of those are not rot at all.**
`scripts/validate_doc_rot.py` sets `_BACKLOG_GROSS_CHARS = 1200` — a row longer than 1200
chars is flagged regardless of dated blocks. Re-derived against the live tree:

```
BACKLOG.md rows                       196
rows carrying a `Done when:` clause   196  (100% — the conversion wave is complete)
median row length                    1120 chars
p75                                  1195 chars
p80                                  1199 chars
p81                                  1200 chars   <-- the threshold sits HERE
p90                                  1318 chars
rows over 1200                         37  (19%)
threshold / median                   1.07x
```

The threshold fires above **p81 of the tree's own normal shape**. It is not detecting
outliers; it is detecting the top fifth of an ordinary distribution. The cause is visible in
this week's history: the W4a/W4b/W4c/W4d **Done-when conversion wave** (2026-08-13,
`a4fc652d`, `8a091278`) rewrote rows to carry explicit Done-when clauses, lengthening them —
and 10 of the 26 gross-length rows (`#112 #277 #278 #338 #341 #344 #353 #356 #362 #371`) are
literally the ids those two lanes converted. They were flagged the day after the wave that
lengthened them. The threshold predates the shape it is now measuring.

**Proposed one-line fix:** re-calibrate `_BACKLOG_GROSS_CHARS` in
`scripts/validate_doc_rot.py` from 1200 to a value derived from the post-conversion
distribution (p90 ≈ 1320 or p95 ≈ 1675), as **one** data change — instead of writing 26
register entries that would each be a paper suppression of a normal row.

The remaining **11** doc_rot rows are genuine history-accretion (≥3 dated blocks): `#511
#522 #505 #510 #419 #492 #528 #426 #322 #278 #387`. For those the register's own standing
doctrine applies verbatim — from the retired `#492` entry: *"self-induced bloat gets drained
rather than dispositioned."* **Note the correct fix site:** `BACKLOG.md` is **generated**;
draining a row means editing `tasks/<id>-*.md` and regenerating with
`python scripts/gen_task_tree.py --emit-source`. Editing BACKLOG.md directly would be
overwritten.

### 1.4 Verdict census across all 45

```
THRESHOLD RE-CALIBRATION (one decision, not 26 entries)   26
DRAIN at tasks/ source, then regenerate                   11
NOT A REPO DEFECT — container artifact, do not paste       4
DISPOSITION (advisory-by-design, unfixable in bulk)        1   journal_spine_anchor
FIX — regen, one command                                   1   doc_claims pytest count
FIX — trim 3 lines                                         1   CLAUDE.md file-budget
OPERATOR CALL — retro-review or disposition                1   review_artifact_coverage
                                                          --
                                                          45
```

**Only 1 of the 45 is a clean disposition candidate on the merits.** That is the honest
headline: the register is not where most of this belongs. Dispositioning all 45 would convert
one threshold defect and one regen into 45 permanent suppressions.

### 1.5 The 45 proposed register entries (paste-ready, unpasted)

Drafted in the live schema (`id` · `organ` · `match` · `ref` · `reason`, plus the optional
`review_date` ADR-75 shelf-life carried by 12 of the 27 live entries). Machine-validated:
all 45 parse as YAML, carry every required key, have unique ids, and **each `match` is a
verified substring of exactly one live WARN's evidence** — 45/45 coverage, zero over-matching
(the whole-Finding contract the register header demands).

Each block carries a `# PROPOSED VERDICT:` line. **Blocks marked NOT A REPO DEFECT or FIX /
DRAIN / RE-CALIBRATION are drafted for completeness as the brief requires — they should not
be pasted unless the architect overrules the stated verdict.** `match` for the doc_rot rows
keys on the `RotFinding.locus` token (`BACKLOG#<id> (`), which the validator's own docstring
names as the stable disposition handle; the tradeoff is that it also suppresses *future*
growth of the same row, which is what the `review_date` shelf-life is there to bound.

<!-- The generated entry blocks follow. They are DATA for adjudication, not instructions. -->

```yaml
# PROPOSED VERDICT: FIX (regen) — one command, zero judgement
- id: warn-doc-claims-pytest-collected
  organ: doc_claims
  match: "pytest_collected@ecosystem/doc-counts.md"
  ref: "#222"
  review_date: 2026-11-14
  reason: >-
    Generated-fragment drift, not a doc defect: ecosystem/doc-counts.md claims 2895 collected tests, live `pytest --collect-only` reports 2897. Regenerate with `python scripts/gen_doc_counts.py --write`. doc-counts.md is deliberately outside the freshness gate, so the regen forces no last_reviewed re-stamp (that decoupling is exactly what #222 built).

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-511
  organ: doc_rot
  match: "backlog-accretion BACKLOG#511 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 7 dated block(s), 3006 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/511-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-344
  organ: doc_rot
  match: "backlog-accretion BACKLOG#344 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1609 chars, 1 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-112
  organ: doc_rot
  match: "backlog-accretion BACKLOG#112 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1279 chars, 0 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-353
  organ: doc_rot
  match: "backlog-accretion BACKLOG#353 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1266 chars, 2 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-425
  organ: doc_rot
  match: "backlog-accretion BACKLOG#425 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1271 chars, 0 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-510
  organ: doc_rot
  match: "backlog-accretion BACKLOG#510 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 3 dated block(s), 2146 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/510-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-514
  organ: doc_rot
  match: "backlog-accretion BACKLOG#514 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 2420 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-527
  organ: doc_rot
  match: "backlog-accretion BACKLOG#527 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1319 chars, 2 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-277
  organ: doc_rot
  match: "backlog-accretion BACKLOG#277 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1288 chars, 2 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-408
  organ: doc_rot
  match: "backlog-accretion BACKLOG#408 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1292 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-418
  organ: doc_rot
  match: "backlog-accretion BACKLOG#418 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1303 chars, 2 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-414
  organ: doc_rot
  match: "backlog-accretion BACKLOG#414 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1296 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-423
  organ: doc_rot
  match: "backlog-accretion BACKLOG#423 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1322 chars, 0 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-522
  organ: doc_rot
  match: "backlog-accretion BACKLOG#522 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 5 dated block(s), 2685 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/522-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-505
  organ: doc_rot
  match: "backlog-accretion BACKLOG#505 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 5 dated block(s), 2303 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/505-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-456
  organ: doc_rot
  match: "backlog-accretion BACKLOG#456 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1292 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-506
  organ: doc_rot
  match: "backlog-accretion BACKLOG#506 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1273 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-430
  organ: doc_rot
  match: "backlog-accretion BACKLOG#430 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1372 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-278
  organ: doc_rot
  match: "backlog-accretion BACKLOG#278 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 3 dated block(s), 1374 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/278-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-322
  organ: doc_rot
  match: "backlog-accretion BACKLOG#322 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 3 dated block(s), 1675 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/322-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-338
  organ: doc_rot
  match: "backlog-accretion BACKLOG#338 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1297 chars, 1 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-341
  organ: doc_rot
  match: "backlog-accretion BACKLOG#341 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1285 chars, 1 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-415
  organ: doc_rot
  match: "backlog-accretion BACKLOG#415 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1351 chars, 0 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-453
  organ: doc_rot
  match: "backlog-accretion BACKLOG#453 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1300 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-487
  organ: doc_rot
  match: "backlog-accretion BACKLOG#487 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1388 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-528
  organ: doc_rot
  match: "backlog-accretion BACKLOG#528 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 3 dated block(s), 1741 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/528-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-387
  organ: doc_rot
  match: "backlog-accretion BACKLOG#387 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 3 dated block(s), 1336 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/387-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-523
  organ: doc_rot
  match: "backlog-accretion BACKLOG#523 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1738 chars, 2 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-492
  organ: doc_rot
  match: "backlog-accretion BACKLOG#492 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 7 dated block(s), 1807 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/492-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-419
  organ: doc_rot
  match: "backlog-accretion BACKLOG#419 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 3 dated block(s), 1908 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/419-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-464
  organ: doc_rot
  match: "backlog-accretion BACKLOG#464 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1267 chars, 2 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: DRAIN (fix, do not disposition) — dated blocks are drainable history; ADR-49 leaves them in git
- id: warn-doc-rot-backlog-accretion-426
  organ: doc_rot
  match: "backlog-accretion BACKLOG#426 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    History-accretion: 4 dated block(s), 1681 chars. The register's own standing doctrine (the #492 entry) is that self-induced bloat gets DRAINED rather than dispositioned. Fix at the SOURCE: tasks/426-*.md body, then `python scripts/gen_task_tree.py --emit-source` (BACKLOG.md is generated). Disposition ONLY if a dated block is a ruled peg the next seat needs.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-428
  organ: doc_rot
  match: "backlog-accretion BACKLOG#428 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1342 chars, 2 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-356
  organ: doc_rot
  match: "backlog-accretion BACKLOG#356 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1214 chars, 1 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-399
  organ: doc_rot
  match: "backlog-accretion BACKLOG#399 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1307 chars, 1 dated block(s) — length alone, no history to drain. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-362
  organ: doc_rot
  match: "backlog-accretion BACKLOG#362 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1237 chars, 0 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: THRESHOLD RE-CALIBRATION (adjudicate as ONE decision with the other 25) — not a per-row disposition
- id: warn-doc-rot-backlog-accretion-371
  organ: doc_rot
  match: "backlog-accretion BACKLOG#371 ("
  ref: "docs/audits/2026-08-14-verification-night2-hygiene.md (DRAFT proposal — replace with the ruling commit/ADR on adoption)"
  review_date: 2026-11-14
  reason: >-
    Gross-length branch: 1318 chars, 1 dated block(s) — length alone, no history to drain. Converted by the 2026-08-13 W4a/W4b Done-when wave. Row-length median across all 196 BACKLOG rows is 1120 chars, so _BACKLOG_GROSS_CHARS=1200 fires above p81 of the tree's OWN post-Done-when shape. 26 such rows dispositioned individually would be 26 paper suppressions; the honest fix is one threshold data-change in scripts/validate_doc_rot.py.

# PROPOSED VERDICT: FIX (regen/trim, do not disposition) — the budget is real and 3 lines over
- id: warn-doc-rot-claude-md-size
  organ: doc_rot
  match: "file-budget CLAUDE.md#size"
  ref: "ADR-53"
  review_date: 2026-11-14
  reason: >-
    CLAUDE.md is 203 counted lines (comment-only machine lines already excluded) against its own declared <=200 budget (ADR-53, stated in the file's own header). Three lines over is a trim, not a disposition: condense the oldest CLAUDE.md section-history bullet per the v2.49 precedent (ADR-49/65 info-preserving condense; git retains the text).

# PROPOSED VERDICT: NOT A REPO DEFECT — container artifact; do NOT paste (it would decorate stale on the operator host)
- id: warn-deployed-version-dev-knowledge
  organ: deployed_methodology_version
  match: "dev-knowledge not listed in deployed-versions.yaml"
  ref: "ADR-91"
  review_date: 2026-11-14
  reason: >-
    ENVIRONMENT ARTIFACT of the cloud checkout. The check keys on the repo-ROOT directory basename; this container cloned the repo to /home/user/dev-knowledge, while ecosystem/deployed-versions.yaml keys the hub as `.dev-knowledge` (its name on the operator host). The row EXISTS and is correctly null (pre-deploy). Re-derive on the operator host before ruling; expected to be absent there.

# PROPOSED VERDICT: NOT A REPO DEFECT — container artifact; do NOT paste
- id: warn-fleet-parity-hooks-armed
  organ: fleet_parity
  match: ".dev-knowledge hooks-armed WARN-undeclared"
  ref: "RF-2"
  review_date: 2026-11-14
  reason: >-
    ENVIRONMENT ARTIFACT: this fresh container never ran the SessionStart arm_hooks.py self-arm, so no hook stage is installed in .git/hooks. The committed .pre-commit-config.yaml is intact and correct. Also the source of the paired `hooks_armed` HARD FAIL in this run. Clears with `pre-commit install -t pre-commit -t commit-msg -t pre-push`.

# PROPOSED VERDICT: NOT A REPO DEFECT — container artifact; do NOT paste
- id: warn-fleet-parity-ai-council-unresolved
  organ: fleet_parity
  match: "ai-council fleet-membership unavailable"
  ref: "ADR-104"
  review_date: 2026-11-14
  reason: >-
    ENVIRONMENT ARTIFACT: the sibling repo ai-council is not present in this cloud container (only the hub is cloned), so the fleet-membership probe cannot resolve /home/user/ai-council. Says nothing about the sibling's real state. Re-derive on the operator host.

# PROPOSED VERDICT: NOT A REPO DEFECT — container artifact; do NOT paste
- id: warn-fleet-parity-corp-monorepo-unresolved
  organ: fleet_parity
  match: "corp-monorepo fleet-membership unavailable"
  ref: "ADR-104"
  review_date: 2026-11-14
  reason: >-
    ENVIRONMENT ARTIFACT: the sibling repo corp-monorepo is not present in this cloud container (only the hub is cloned), so the fleet-membership probe cannot resolve /home/user/corp-monorepo. Says nothing about the sibling's real state. Re-derive on the operator host.

# PROPOSED VERDICT: DISPOSITION (advisory-by-design, noisy at scale) — strongest genuine disposition candidate in this set
- id: warn-journal-spine-anchored-by-mention
  organ: journal_spine_anchor
  match: "anchored by mention, not by record"
  ref: "[#524] leg c"
  review_date: 2026-11-14
  reason: >-
    ADVISORY BY DESIGN and structurally unfixable in bulk: the [#524] leg-c WARN fires when a spine SHA appears in JOURNAL prose rather than on an explicit `Anchors:` record line. It currently names 401 commits (5 listed + 396 more) — the accumulated history of a convention adopted AFTER most of those entries were written, and JOURNAL.md is append-only (CLAUDE.md §5 rule 2), so the backlog of 401 cannot be retro-fixed without the edit the append-only rule forbids. The HARD leg (block_unanchored_push) is unaffected — it passes; this is the softer record-shape advisory. Disposition the historical mass; the convention holds going forward.

# PROPOSED VERDICT: OPERATOR CALL — retro-review (fix) or disposition; do not self-rule
- id: warn-review-artifact-387b794a-repin-close
  organ: review_artifact_coverage
  match: "387b794a integrator/513-repin-close"
  ref: "[#480] P3"
  review_date: 2026-11-14
  reason: >-
    One code-impact merge since 2026-08-05 carries no linked review artifact: 387b794a integrator/513-repin-close. Advisory per the [#480] P3 ruling (the hard pre-push leg is deferred pending 0 false positives over two windows). Two honest routes, both the operator's to pick: perform the retroactive review and land the artifact (the route the sibling WARNs in this class took), or disposition it as a mechanical re-pin whose diff is a line-number bump. A sweep cannot rule which.

```

---

## 2. P6 drift — `ecosystem/doc-counts.md` vs live pytest

Both sides re-derived:

```
ecosystem/doc-counts.md claims       "tests: **2895 collected**"
live `pytest --collect-only -q`       2897 tests collected in 3.31s
drift                                 -2 (doc understates by 2)
```

The other two claims in the same fragment are **in sync** — `audit_check_count` 43/43 and
`precommit_hook_count` 18/18 — so this is a single-claim drift, not a stale file.
`python scripts/gen_doc_counts.py --check` confirms independently:
`mismatch pytest_collected (file 2895 / actual 2897)`.

**Exact regen command (as requested):**

```
python scripts/gen_doc_counts.py --write
```

**Proposed one-line fix:** run that command and commit the regenerated fragment; it clears
both this item and WARN #1 of §1 (they are one defect surfacing on two organs — `doc_claims`
reads the same fragment the generator writes).

Worth noting for the architect: `doc-counts.md` deliberately carries **no** `last_reviewed`
frontmatter and is deliberately outside `_FRESHNESS_FILES`, so this regen forces **no**
re-stamp on any freshness-gated document. That decoupling is exactly what `#222` was built
for, and it is working — the fix here costs one command and zero review debt.

---

## 3. `last_reviewed` stamps older than the file's last content commit

Swept **every** `*.md` in the tree carrying a `last_reviewed` frontmatter key (38 files),
comparing the stamp against `git log -1 --format=%cs` for that path.

**3.1 The canonical gated set is CLEAN — 0 stale.** All 9 files in `_FRESHNESS_FILES`
(`DEFAULT_FRESHNESS_FILES` + the 3 hub-only extras) pass, and `canonical_freshness` reports
`OK` on the full-history tree:

```
ARCHITECTURE.md              2026-08-14  ==  2026-08-14 d63a6dc6
CLAUDE.md                    2026-08-12  ==  2026-08-12 98d50e78
CONTRIBUTING.md              2026-08-08  ==  2026-08-08 8f09c12d
VISION.md                    2026-07-25  ==  2026-07-25 30a8c42b
docs/handoffs/README.md      2026-08-08  ==  2026-08-08 8f09c12d
protocols/ESSENTIALS.md      2026-08-10  ==  2026-08-10 6e76b3f0
protocols/SESSION_SETUP.md   2026-07-29  ==  2026-07-29 9e456504
protocols/AI_COUNCIL_PROCESS.md 2026-07-29 == 2026-07-29 9e456504
protocols/DEFINITION_OF_DONE.md 2026-08-06 == 2026-08-06 59b191c5
```

(The 6-file FAIL a reader may recall from a shallow run is the §0.1 artifact. It is not real.)

**3.2 Nineteen stale stamps exist, all in IMMUTABLE handoff bundles — stale by
construction, not by neglect.** Every one is a `02_VISION.md` / `02b_ECOSYSTEM_VISION.md`
inside a 2026-05-* bundle: a point-in-time COPY of `VISION.md` carrying the stamp `VISION.md`
had on the day it was copied, committed on the (later) bundle-cut date. Examples:

```
docs/handoffs/2026-05-12-ai-council-session-sync/02_VISION.md      stamp 2026-05-09 < commit 2026-05-12
docs/handoffs/2026-05-14-ai-council-session-sync/02_VISION.md      stamp 2026-05-12 < commit 2026-05-15
docs/handoffs/2026-05-25-corp-monorepo-session-sync/02_VISION.md   stamp 2026-05-18 < commit 2026-05-25
(+16 more of identical shape, all 2026-05-09 .. 2026-05-25)
```

**Proposed one-line fix: NONE — do not touch these.** Handoffs are immutable (CLAUDE.md §5
rule 3) and the stamp is *accurate about the copied content*. The only defensible action is
to leave them alone; they are correctly excluded from `_FRESHNESS_FILES` already. Recorded
here so a future sweep does not "discover" them again and propose a forbidden edit.

**3.3 Three template files carry the literal placeholder `<YYYY-MM-DD>`** —
`templates/{ARCHITECTURE,CLAUDE-md,CONTRIBUTING-md}-template.md`. Correct by design (a
template must not ship a real date). No action. Flagged only because a naive stamp-sweep
reads them as malformed.

**3.4 One genuine adjacent defect, surfaced by this sweep:**
`templates/CONTRIBUTING-md-template.md` trips `reconciled_versions` —
*"malformed (`reconciled_with` not `<spec-id>@<version>`)"*. It is already dispositioned in
the register (`warn-reconciled-versions-contributing-template`, ref `#335`), so it does not
appear in the 45. Noted for completeness, not proposed for action.

**3.5 Structural observation (no fix proposed, operator's call):**
`protocols/PLAYBOOK.md` — the largest canonical doc at 4554 lines — carries **no**
`last_reviewed` frontmatter and is therefore in **no** freshness gate. `audit.py`'s own
comment records this as a knowing deferral ("PLAYBOOK is the largest ungated canonical doc
but is DEFERRED"). Restated here because §5 below found its two live defects, which is what
an ungated doc looks like after time passes.

---

## 4. BACKLOG / tasks coherence

Machine-verified: `task_tree_coherence` reports
*"BACKLOG.md coherent with the tasks/ source of truth (structure + frontmatter honesty +
full reassembly)"*. Independently re-derived below rather than taken on that organ's word.

**4.1 `[#529]` and `[#530]` — CONFIRMED ABSENT.**

```
tasks/ files for 529 or 530     : none
BACKLOG.md rows for 529 or 530  : none
highest allocated id            : 528
```

Both ids appear **only** as prose in `JOURNAL.md`, `LESSONS.md` and the 2026-08-14 handoff
bundle, all describing the duplicate-execution incident that briefly double-assigned
`[#526]`-`[#529]` before those branches were discarded. The handoff's own §5 states
*"ids [#529]/[#530] are FREE"*. **This sweep confirms that claim against the tree: free,
unallocated, no residue.**

**4.2 Status vs task file — 0 contradictions.**

```
task files                                    261 (+ tasks/README.md, no frontmatter — expected)
status census   open 171 · closed 62 · deferred 25 · retired 2 · superseded 1
BACKLOG rows                                  196
closed/killed task file still rendered as a row   0
BACKLOG row with no backing task file             0
open task file missing from BACKLOG               0
```

The 3 files that do not render (`[#452]` retired, `[#479]` superseded, `[#489]` retired) are
correct: `gen_task_tree.py` `_TERMINAL_STATUSES = ("closed", "retired", "superseded")`, and
ADR-107 §6.3 rules retire-not-delete, so the record file persisting while the row does not is
the designed behaviour. **No fix proposed.**

**4.3 Dangling `[#id]` references — 48 across live surfaces, and the honest reading is that
none is a defect.** Ids cited in `CLAUDE.md` (8), `ARCHITECTURE.md` (8), `PLAYBOOK.md` (7),
`CONTRIBUTING.md` (6), `BACKLOG.md` (13), and 6 more elsewhere have no `tasks/` file. All
inspected are **provenance citations to ids closed before the ADR-107 `tasks/` tree existed**
— e.g. `CLAUDE.md` "added by `[#69]`", `CONTRIBUTING.md` "`closes [#57]`". A provenance
citation is a pointer into git history, which resolves; it is not a live work reference.
**Proposed one-line fix: none — do not "repair" these**; rewriting a historical citation
destroys the traceability it exists to provide.

The one genuinely actionable instance in this class is already caught and dispositioned:
`preflight_backlog_ids` → *"1 kill-candidates assertion(s) name a non-open row: [#310] ->
#292"*, suppressed by `warn-preflight-backlog-ids-310-292`. It does not appear in the 45.

---

## 5. Dead pointers in ESSENTIALS / PLAYBOOK

Checked three ways: markdown links resolving to repo paths, backticked path tokens, and
`§`/`Ch` cross-references resolving to real headings.

**5.1 `protocols/ESSENTIALS.md` — CLEAN.** 0 unresolved links, 0 unresolved path tokens.
All 12 outbound `§`/`Ch` references into PLAYBOOK (`§2 §3 §4 §7 §8 §9 §11 §17`, `Ch4`, and
the `"The two lifelines" § Lifeline 1` heading reference) resolve to live headings.

**5.2 `protocols/PLAYBOOK.md` — 0 broken links, 0 broken section references, 2 genuinely
dead pointers.** Section numbering is sound: Part I is `Ch1`–`Ch14` contiguous, Part II is
`§1`–`§21` with the **§18 gap intentional and machine-marked**
(`<!-- structure-allow: numbering-gap 18 -->`, policed by `scan_dangling_allow`), so the gap
is documented rather than rot. Cross-reference resolution across all 11 canonical surfaces:
**0 unresolved.**

**FINDING 5.2a (the real one) — PLAYBOOK describes a RETIRED GitHub Action in the present
tense, at two sites.**

```
protocols/PLAYBOOK.md:2269  "3. **Action** — the outcome handler
                             (`.github/workflows/nightly-conformance-triage.yml`):
                             diff-guard + auto-merge / triage on the PR the run opens."
protocols/PLAYBOOK.md:2305  "(1) the Action sets `fetch-depth: 0` ...
                             (`.github/workflows/nightly-conformance-triage.yml`)"
```

That file does not exist. It was **deleted at `82227f08`** ("chore(automation): retire
conformance-digest mechanism `[#255]`"); `.github/workflows/` now contains only
`report-only-wall.yml`. Both `ARCHITECTURE.md:877` and `CONTRIBUTING.md:141` correctly record
the retirement — **PLAYBOOK is the one surface that was not updated.** This is exactly the
`[#503]` class ("the thing it describes moved underneath it"), and §3.5 explains why it
survived: PLAYBOOK is in no freshness gate, so nothing ever asked.

**Proposed one-line fix:** mark both sites retired-at-`82227f08` (mirroring the wording
already in `ARCHITECTURE.md:877`) rather than deleting them, so the shallow-clone guard
rationale at L2305 — which is still true and was load-bearing for §0.1 of this very report —
survives the correction.

**FINDING 5.2b (minor) — an illustrative example is shaped like a live locator.**
`protocols/PLAYBOOK.md:3517` reads ``Example: `docs/audits/2026-04-22-codex-handoff-process-rewrite.md` ``.
No such audit exists (nearest neighbours are 2026-04-21 and 2026-04-24). It is an *example*
under a naming-convention heading, so it misleads nothing structurally — but it is
indistinguishable from a citation to a `/preflight` run or a reader checking locators.
**Proposed one-line fix:** point the example at a real audit, or prefix it
`Example (illustrative, not a real file):`.

**5.3 Triaged and dismissed — 38 further path tokens that resolve nowhere but are correct.**
Recorded so the next sweep does not re-raise them: deliberately-retired files referenced *as*
retired (`CHANGELOG.md` ×3, `OPEN_DECISIONS.md` ×2, `BACKLOG_ARCHIVE.md` — each appears in a
sentence stating it is retired); user-level `~/.claude` assets absent from any repo
(`surface-closures.ps1`, `gotchas.md`, `learned-rules.md`, `ecosystem-snapshot.md`,
`report-generator.md`); sibling-repo paths (the Ch8 dispatch surface, `Invoke-Dispatch.ps1`
and the `dev-terminals` set); the gitignored-by-design `state.yaml`; consumer-side
`.claude/CLAUDE-FLOOR.md` (the hub has not adopted the floor — `floor_integrity` reports
`n/a`); and grammar placeholders (`ADR-NN-topic.md`, `YYYY-MM-DD-slug.md`, `ruff.toml`).

---

## 6. Index freshness — `docs/handoffs/` and `docs/audits/`

**6.1 `docs/audits/` — FRESH.** `python scripts/gen_audit_index.py --check` exits 0.
At sweep time the generated `docs/audits/README.md` reported **504 audit documents** against
505 `*.md` in the directory; the difference is `README.md` itself, which the generator
correctly excludes. No drift. The `audit-index-freshness` pre-commit hook gates it.

> **Disclosure — the one edit this sweep made outside this report.** Adding this file to
> `docs/audits/` necessarily staled that index, and `audit-index-freshness` exists to block
> exactly that. The index was therefore regenerated with
> `python scripts/gen_audit_index.py --write` in the same commit: a **2-line mechanical
> delta** (`504` → `505 audit documents`, plus this report's own row). It is the obligatory
> companion of writing the file, not a fix to any finding in this report — leaving it stale
> would have created a fresh instance of the exact index-rot class this very section audits.
> No other file outside this report was touched.

Every other generated index in the repo was checked at the same time, all **exit 0 / fresh**:
`gen_claude_rosters` · `gen_intake_index` · `generate_organ_index` · `gen_methodology_roster`.
The only stale generated artifact in the entire repo is `ecosystem/doc-counts.md` (§2).

**6.2 `docs/handoffs/` — there is NO index to be stale, and that is the finding.**

```
docs/handoffs/*/            108 bundles
docs/handoffs/archive/       15 bundles
docs/handoffs/README.md      the operator RUNBOOK — process prose, not an inventory
                             (verified: contains no bundle listing of any kind)
generator                    none (gen_handoff.py CREATES bundles; it indexes nothing)
freshness hook               none
```

Four of the five sanctioned `docs/` genres have a generated, hook-gated index
(`audits`, `intake`, `decisions` via its hand-authored README, and the relocated organ index).
`handoffs` — at **123 bundles**, the largest bundle count in the tree — has none. Navigating
it requires the `_select_active_bundle` git-add-date predicate that `CLAUDE.md` §1 item 3 and
§6 item 3 both now cite, i.e. **the only way to find the current bundle is to run code**.
This is the §5.5 navigation-overhead trigger that `gen_audit_index.py` was built to satisfy,
unmet on a sibling genre.

**Proposed one-line fix:** generate `docs/handoffs/INDEX.md` (date · slug · mode ·
destination, reverse-chronological, marking the `_select_active_bundle` winner) on the exact
`gen_audit_index.py` + `audit-index-freshness` pattern — reusing `_select_active_bundle`
rather than re-implementing the predicate, so the index cannot disagree with the boot
instruction.

**Caveat on this item, stated rather than buried:** this is the one §6 proposal that is a
*build*, not a repair. It is bigger than the one-line fixes elsewhere in this report and
would need a row before anyone acts on it. **This sweep filed no row** (the brief forbids
births); the proposal is recorded here for the architect to file or discard.

---

## 7. Summary of proposals

Nothing below was executed.

```
one command, zero judgement   python scripts/gen_doc_counts.py --write            (§2; clears 2 WARNs)
one data change               _BACKLOG_GROSS_CHARS 1200 -> ~1320                  (§1.3; clears 26 WARNs)
one trim                      CLAUDE.md 203 -> <=200 lines, condense oldest §12    (§1; clears 1 WARN)
source-edit + regen           drain 11 history-accreted tasks/ bodies              (§1.3; clears 11 WARNs)
one register entry            journal_spine_anchor mention-not-record              (§1; clears 1 WARN)
operator call                 review_artifact_coverage 387b794a                    (§1; clears 1 WARN)
re-derive on operator host    4 container artifacts                                (§0.2; expected to vanish)
two-site correction           PLAYBOOK L2269/L2305 retired Action                  (§5.2a)
one-line correction           PLAYBOOK L3517 illustrative example                  (§5.2b)
needs a row first             docs/handoffs/ generated index                       (§6.2)
no action, deliberately       19 immutable-bundle stamps · 48 provenance [#id]s    (§3.2, §4.3)
```

**The load-bearing observation:** 41 of the 45 WARNs resolve to **four** actions — one regen,
one threshold re-calibration, one bulk drain, and re-deriving on the operator's host. Only
**one** is a disposition on the merits. The gate is not RED because 45 things are wrong; it is
RED because two derived surfaces drifted and one threshold no longer fits the tree it measures.

---

## AMENDMENT 2026-08-14 (same session, post-push — §0.3 corrected; all findings re-derived under the pinned toolchain and UNCHANGED)

In-file amendment marker per CLAUDE.md §5 rule 3 — the sections above stand as written and
are **not** edited; this section is the delta.

**§0.3 was WRONG on one point, and it was the caveat attached to every number in this report.**
It stated that the ADR-106 pin `uv==0.11.19` "is not resolvable in this container", inferred
from `uv self update 0.11.19` returning *"version 0.11.19 was not found"*. That was uv's own
release-channel lookup failing, not the version's availability: **uv 0.11.19 is published on
PyPI and installs cleanly** (`pip install uv==0.11.19`). The inference was wrong, so the
conclusion drawn from it — that the organs could only be run under a hand-built interpreter
with dependency resolution *not* lock-pinned — was wrong too.

Corrected by doing the thing §0.3 said could not be done: the pinned uv was installed,
`uv sync --locked` rebuilt the declared gate environment from the committed `uv.lock`, and
**every derivation in this report was re-run under it**.

**Result — nothing moved.** The pinned `uv run --locked python scripts/audit.py ship-gate`
output is byte-identical to the run this report was written from, except for one extraneous
`UV_NATIVE_TLS` deprecation line on stderr:

```
ship-gate: RED — not shipped-ready (1 hard-fail organ(s); 45 new/undispositioned WARN(s))
pytest --collect-only          2897 tests collected   (doc-counts still claims 2895 — §2 holds)
gen_doc_counts --check         mismatch pytest_collected (file 2895 / actual 2897)
ruff check                     All checks passed!
session_end_backpressure.py    exit 0
```

**Standing of this report after the amendment:** §0.3's toolchain caveat is **withdrawn**.
The 45 WARNs, the 26-of-45 threshold finding, the P6 drift, the freshness sweep, the
BACKLOG/tasks coherence result and the dead-pointer findings are all confirmed under the
repo's own declared, lock-pinned environment — they are no longer environment-caveated.
**§0.1 (the shallow-clone corrections) and §0.2 (the 4 container artifacts) are UNAFFECTED
and still stand:** unshallowing and the pinned toolchain are independent facts, and the four
container artifacts arise from absent sibling repos, unarmed hooks and the checkout
directory name — none of which the uv pin touches. Those 4 entries remain **do-not-paste**.

**The lesson, recorded because it is the same class this report audits:** a tool's own
"version not found" was accepted as ground truth about availability without checking the
package index. That is an unverified inference presented as a derived fact — precisely what
§0.1 catches the shallow clone doing to `canonical_freshness`. It was caught only because
the `Stop` hook kept failing on the pinned invocation and the failure was investigated
instead of being dismissed as the already-disclosed environment artifact.
