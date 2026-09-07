# Census — `docs/audits/` (sweep 2026-09-07, lane S-04, READ-ONLY)

**Consumers:** `[#552]` — *"Window-close disposition + archival routine"*, the row that already
owns this folder's disposition backlog; `[#595]` — the `consumer_at_landing` ratchet whose corpus
this census re-measures; `[#590]` — the `audit-index-freshness` narrowing, whose ship-gate leg this
census reports against. Governing decisions: `ADR-100` (audit retention — keep-all-accepted),
`ADR-101` (naming grammar + tree seal), `ADR-111` (one triage per finding). Substantive citations
by path throughout: `docs/audits/2026-09-06-technical-archive-report-stage.md` §3.2 (the prior
measurement this census re-runs), `docs/decisions/ADR-100-audit-retention-index-rule.md`,
`scripts/consumer_at_landing.py`, `scripts/validate_hermetization.py`, `scripts/gen_audit_index.py`,
`ecosystem/audit-consumer-baseline.json`, `ecosystem/audit-funnel-baseline.json`,
`ecosystem/audit-title-baseline.json`, `ecosystem/fleet-shape-spec.yaml`.

**Class:** technical, **READ-ONLY**. Zero files moved, deleted, edited or renamed. Every verdict
below is a **PROPOSAL** the operator rules. `docs/audits/README.md` was **not** regenerated
(`[#590]`; the integrator regenerates it once, after the last merge).

**Lane:** S-04, sweep `BATCH-2026-09-07-SWEEP-CONTRACTS.md`, one of 13 parallel census lanes.
Branch `claude/census-docs-audits`.

**Measured at `21576e3a4fe77373c936247e6560263b7cd3fbd2`.** Every count below is taken at that
commit, **excluding this lane's own two artifacts** — a census does not count itself, and the
appendix names every file in the corpus, so leaving it in the citing set would flatten every
reference tier to "cited". The tree moved once under this lane mid-pass (`5f27b20` → `21576e3`,
one new audit); the numbers were re-derived at the later commit rather than shipped stale. It may
move again before this merges: batch U wave 2 is draining beside this lane.

**Full per-file inventory:** `docs/audits/2026-09-07-technical-census-docs-audits-appendix.md`
(1,028 rows, same commit). This file carries the grouped inventory; the appendix carries the table.

---

## 0 · What was measured, and with what

Three witnesses, in this order of authority:

1. **The live detector's own constants**, imported rather than restated —
   `consumer_at_landing.POOL_DIRS` / `POOL_ROOT_FILES` / `CORPUS_EXCLUDE` / `ARM_DATE` /
   `_CITATION_RES`, and `validate_hermetization.AUDIT_CLASS_ENUM` / `rule_b_violation`. Every
   pool, enum and grammar figure below is the detector's definition applied to today's tree, not
   a second implementation of it.
2. **The committed baselines** — `ecosystem/audit-consumer-baseline.json`
   (`consumer-at-landing/v2`, measured 2026-09-01 at `9644e815`),
   `ecosystem/audit-funnel-baseline.json` (`funnel-coverage/v1`, 2026-09-01 at `13fb1538`),
   `ecosystem/audit-title-baseline.json`.
3. **Reference counting over `git ls-files`**, keyed on **bare stem** and bucketed by the surface
   doing the citing, using `consumer_at_landing`'s own inclusion/exclusion split.

**The witness tiers** used in every table below. A file sits in the highest tier that applies:

```
A pool   cited by the GOVERNANCE POOL -- tasks/, docs/decisions/, docs/intake/, protocols/,
         and the six root canonical docs. This is the detector's definition of a consumer.
B peer   cited only by another docs/audits/ artifact.
C log    named only in JOURNAL.md or a docs/handoffs/ bundle -- surfaces consumer_at_landing
         EXCLUDES on purpose: "a mention in a session log or a machine baseline is a record
         that the file existed, not evidence that anything consumes it."
D code   named only under scripts/, tests/ or ecosystem/ (non-baseline).
E gen    present ONLY on generated surfaces (the three baselines, docs/audits/README.md, a
         handoff 08_TREE.txt) -- surfaces that cite everything by construction.
F none   no reference anywhere in the tracked tree.
```

**Two corrections made during the pass, recorded because each changed a number.**

- A first reference sweep anchored on the `.md`/`.html`/`.json` extension reported three artifacts
  with *no reference anywhere*. Re-opening each showed all three are cited **by bare stem** — and
  one carries a `.` in its slug, which the anchored pattern rejected outright. The count was an
  artifact of my regex, not a fact about the tree. Every figure below uses **stem** keying, which
  is what `consumer_at_landing` itself uses.
- A re-measurement after this lane's own files were staged returned tiers C/D/E/F all at **zero**.
  Cause: the appendix cites all 1,028 artifacts by path, so it is itself a surface that "cites
  everything by construction". Excluding this lane's two files from the **citing** set, not only
  from the corpus, restored the measurement. Both exclusions are in force throughout.

---

## Inventory

### By month — top-level artifacts

`.md`/`.html` sidecar pairs are counted **once** (two pairs exist:
`2026-09-01-technical-atlas-r1-layer-graph` and `2026-09-01-census-atlas-r1-def-usage-ledger`).
`README.md` is excluded from the corpus, as `consumer_at_landing.CORPUS_EXCLUDE` excludes it.

| month | artifacts | bytes | A pool | B peer | C log | D code | E gen | F none | grandfathered name |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03 | 1 | 7,071 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2026-04 | 17 | 258,195 | 6 | 11 | 0 | 0 | 0 | 0 | 16 |
| 2026-05 | 65 | 782,113 | 15 | 50 | 0 | 0 | 0 | 0 | 56 |
| 2026-06 | 92 | 879,288 | 24 | 68 | 0 | 0 | 0 | 0 | 41 |
| 2026-07 | 170 | 2,204,499 | 56 | 114 | 0 | 0 | 0 | 0 | 23 |
| 2026-08 | 492 | 10,527,151 | 179 | 296 | 1 | 0 | 16 | 0 | 0 |
| 2026-09 | 73 | 1,715,296 | 48 | 22 | 2 | 0 | 1 | 0 | 0 |
| **top-level total** | **910** | **16,373,613** | **328** | **562** | **3** | **0** | **17** | **0** | **137** |

### By enum class — top-level artifacts

Class assigned by the **live** whole-token longest-match against
`validate_hermetization.AUDIT_CLASS_ENUM` (11 members, sourced from
`ecosystem/fleet-shape-spec.yaml` `naming_grammar.audit_class_enum`), not by splitting on the
first hyphen.

| enum class | artifacts | bytes | A pool | B peer | C log | D code | E gen | F none |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `technical` | 486 | 11,426,605 | 208 | 264 | 3 | 0 | 11 | 0 |
| `codex` | 166 | 610,114 | 18 | 143 | 0 | 0 | 5 | 0 |
| `(grandfathered)` | 137 | 2,028,787 | 50 | 87 | 0 | 0 | 0 | 0 |
| `verification` | 42 | 832,706 | 26 | 15 | 0 | 0 | 1 | 0 |
| `census` | 23 | 788,228 | 17 | 6 | 0 | 0 | 0 | 0 |
| `conformance-nightly-digest` | 22 | 278,581 | 3 | 19 | 0 | 0 | 0 | 0 |
| `ecosystem-audit` | 17 | 163,117 | 1 | 16 | 0 | 0 | 0 | 0 |
| `fresh-eyes` | 8 | 150,023 | 2 | 6 | 0 | 0 | 0 | 0 |
| `changelog-review` | 6 | 37,640 | 3 | 3 | 0 | 0 | 0 | 0 |
| `qa` | 3 | 57,812 | 0 | 3 | 0 | 0 | 0 | 0 |

Two enum classes hold **zero** files: `functional` and `incident-evidence`. Declared, never used.

### The 12 lane-contract subdirectories

| lane-contract directory | files | bytes | A pool | B peer | D code | E gen | F none |
|---|---:|---:|---:|---:|---:|---:|---:|
| `2026-08-25-technical-batch1-launch-contracts` | 5 | 31,534 | 1 | 3 | 0 | 1 | 0 |
| `2026-08-28-technical-batch1-launch-contracts` | 2 | 18,011 | 2 | 0 | 0 | 0 | 0 |
| `2026-08-28-technical-batch2-launch-contracts` | 13 | 102,637 | 1 | 8 | 0 | 4 | 0 |
| `2026-08-29-technical-batch2-wave2-launch-contracts` | 9 | 92,093 | 0 | 7 | 0 | 2 | 0 |
| `2026-08-29-technical-batchd-launch-contracts` | 8 | 41,304 | 0 | 4 | 0 | 4 | 0 |
| `2026-08-31-technical-batche-launch-contracts` | 26 | 147,981 | 8 | 11 | 1 | 6 | 0 |
| `2026-09-01-technical-batchf-launch-contracts` | 7 | 44,036 | 1 | 4 | 0 | 2 | 0 |
| `2026-09-01-technical-followon-launch-contracts` | 1 | 6,380 | 1 | 0 | 0 | 0 | 0 |
| `2026-09-05-technical-627-readjudication-artifacts` | 12 | 40,973 | 1 | 11 | 0 | 0 | 0 |
| `2026-09-05-technical-batch-r5p-launch-contracts` | 3 | 15,153 | 0 | 3 | 0 | 0 | 0 |
| `2026-09-06-technical-batch-t-launch-contracts` | 13 | 211,550 | 0 | 0 | 13 | 0 | 0 |
| `2026-09-06-technical-batch-u-launch-contracts` | 19 | 351,568 | 0 | 1 | 0 | 0 | 18 |
| **total** | **118** | **1,103,220** | **15** | **52** | **14** | **19** | **18** |

---

## Proposals

### The contract's four questions, answered first

**Q1 — audits whose arcs are closed and uncited → ARCHIVE.**
**ARCHIVE is not an available verdict for this folder, and the reason is a ratified decision, not
a judgment of mine.** Three witnesses, each opened:

```
docs/decisions/ADR-100-audit-retention-index-rule.md:34
  "Everything older moves to an archive *section of the index* -- a section of the index, not
   the filesystem. Files never move; only their index grouping does."

docs/decisions/ADR-100-audit-retention-index-rule.md:63  (Considered and rejected)
  "Physically move older audits to an `archive/` dir. Rejected here and gated for the future
   (section 3): no `archive/` dir exists, the move is under-scanned (the known gap), and
   ADR-36/ADR-60 cite the directory structurally -- a move needs a full referential-currency
   scan PLUS an explicit architect ruling."

ls -d docs/audits/archive   ->  ABSENT  (verified at 21576e3a)
```

A fourth witness agrees, measured 24 hours before this lane and by a different lane:
`docs/audits/2026-09-06-technical-archive-report-stage.md:468` — *"**RETIRE-PROPOSED: none.**
`docs/audits/` deliberately has no archive (`ADR-100` keep-all-accepted, restated in `[#420]`'s own
body), so there is nothing to retire *to*. The disposition backlog is already OWNED by `[#552]`."*

So the "closed and uncited" set is worth **measuring**, and this census measures it — but it
resolves to KEEP, not ARCHIVE, until an architect ruling creates the destination. The measured set
is nonetheless the answer to the question actually being asked:

- **328 of 910** top-level artifacts (36%) are cited by the governance pool.
- **562 (62%)** are cited **only by peer audits** — the corpus talking to itself.
- **3** are named only in `JOURNAL.md` or a handoff bundle, both surfaces the detector excludes
  by design: `2026-08-30-technical-window-close-operator-brief.md`,
  `2026-09-05-technical-lane-r-000-zc-candidates.md`, `2026-09-07-technical-seal-report-fleet.md`.
  The last two landed in the last 72 hours; this is landing latency, not rot.
- **17** top-level artifacts exist **only on generated surfaces** — the closest thing in this
  folder to a genuinely orphaned set. Fifteen of the seventeen are the 2026-08-27 → 2026-08-29
  night-batch packets and lane reviews (`nb2-*-packet`, `codex-batch1-lane-*-review`,
  `technical-lane-n*-*`). They are past the normal-latency window and no pool surface names them.
- **0** top-level artifacts have no reference at all.

**Q2 — lane-scratch shapes.** Two findings, both structural, both reported and neither fixed.

**F-1 · The 12 lane-contract subdirectories are invisible to BOTH audit gates, and each gate
misses them for a different reason.** 118 files, 1,103,220 bytes.

```
Rule B (naming grammar), scripts/validate_hermetization.py:376-378
    if not (len(parts) == 3 and parts[0] == "docs" and parts[1] == "audits"
            and parts[2].lower().endswith(".md")):
        return None      # not an audit file -> Rule B is silent
  -> a file at docs/audits/<dir>/<name>.md has len(parts) == 4. Rule B never sees it.
  -> measured: 109 of the 118 would be REFUSED by Rule B if they sat one level up
     (UPPERCASE lane ids: LANE-u-000-*.md, NB2-LANE-A-604-*.md, BATCH1-LANE-CONTRACTS-*.md,
     PLAN.md, CUT.md, MANIFEST.md, SEED_RUBRIC.md, VERDICT_RULE.md, ARM3_NOTE.md).

consumer_at_landing landing leg, ARM_DATE = 2026-08-27
  -> the leg binds artifacts "landed on or after ARM_DATE", and landing date is parsed from a
     YYYY-MM-DD filename prefix. These files have none, so `landed` is None and every one of
     them is grandfathered. Measured: post-ARM_DATE subdir files = 0, of 118.
```

This is not an inference. `ecosystem/audit-consumer-baseline.json` records it as the baseline's
own stated provenance: *"the contracts declare No-consumer per the check's own escape and are
**structurally uncitable (no YYYY-MM-DD in the filename)**"*. The shape is known; what this census
adds is that it now accounts for **11.5% of the corpus by file count** and grows one directory per
batch night.

**F-2 · Nine executable Python files live in a documentation home.** All in one directory,
29,819 bytes total:

```
docs/audits/2026-09-05-technical-627-readjudication-artifacts/
    check_63_65.py   drive.py        drive2.py      extract_prompts.py   recount_n04.py
    run_adddir.py    run_agy.py      score_f0.py    seed_corpus.py
```

They are the only non-`.md` files anywhere under the 12 subdirectories. They are inside
`consumer_at_landing`'s corpus (which is recursive over **all** file types), so they inflate the
corpus count, and they are outside every naming and title gate. `docs/audits/` is the *outputs*
role in the ADR-60 folder taxonomy; the home allowlist places executable code under `scripts/`.
**Verdict: RELOCATE (proposal).** Witness: their extension against the folder's declared role, and
their tier — 8 of 9 are cited by peer audits only, one by nothing.

**Q3 — the six RETIRE files from D9, present/absent.** **UNDETERMINED.** See Honest limits §1.

**Q4 — index freshness.** `docs/audits/README.md` is **stale by two artifacts**, and both are from
the last 24 hours.

```
README.md claim line                      "**906 audit documents.**"
README.md distinct linked .md              906
disk, docs/audits/*.md minus README.md
  and minus this lane's two files          908
on disk and NOT linked                     2026-09-06-technical-erratum-aj-second-pass.md
                                           2026-09-07-technical-seal-report-fleet.md
linked but NOT on disk                     (none)
```

Both missing entries landed from batch U wave 2 while this sweep was running. The staleness is
**live and growing**: it was one artifact at `5f27b20` and two at `21576e3`, one commit later.

Two further index-scope facts, reported rather than proposed:

- The generator globs `audits_dir.glob("*.md")` — **non-recursive**
  (`scripts/gen_audit_index.py:156`). The 109 `.md` files inside the 12 lane-contract
  subdirectories are **not indexed and cannot be**, and the 2 `.html` + 2 `.json` top-level
  artifacts are outside the `*.md` glob. The index covers **908 of the 1,031** tracked files under
  `docs/audits/`.
- `audit-index-freshness` **cannot catch this staleness by design** since `[#590]` narrowed it to
  `^docs/audits/README\.md$|^scripts/gen_audit_index\.py$`. The hook's own comment names the
  replacement: *"the ship-gate-only `generated_artifact_freshness` leg, artifact `audits-index`."*
  That leg was **not run** here (Honest limits §2). Per the contract, the index is **not**
  regenerated by this lane.

All file counts in this census are taken **before** this lane's own two files:
`git ls-files docs/audits | wc -l` → **1,031** at `21576e3a`.

### Verdicts

**KEEP — 1,019 artifacts** (910 top-level + 109 subdirectory `.md`).
*Witness:* `ADR-100` rules retention **keep-all-accepted** for this tree and explicitly gates the
filesystem move behind a referential-currency scan plus an architect ruling; no `docs/audits/archive/`
exists; `[#552]` already owns the disposition backlog, and `ADR-111` admits one triage per finding,
so no second row is proposed. This is a **folder-level** verdict with a folder-level witness, and
it is stated once rather than repeated 1,019 times — the appendix carries the per-file row.

**RELOCATE — 9 artifacts.** The nine `.py` files listed under F-2, proposed to a code home.
*Witness:* file type against `docs/audits/`'s declared outputs role; they are the only files in the
tree that no naming, title or index gate can see, and the only executable ones.

**ARCHIVE — 0.** *Witness:* `ADR-100:34` and `:63` (quoted above) plus `ls -d docs/audits/archive`
→ ABSENT. The destination does not exist and creating it is explicitly an architect act. Every
artifact that would otherwise be archive-shaped resolves to KEEP.

**RETIRE — 0.** *Witness:* same, plus `2026-09-06-technical-archive-report-stage.md:468`, which
reached **RETIRE-PROPOSED: none** for this folder one day earlier on an independent pass. This
census does not overturn it and found nothing it missed.

**UNDETERMINED — 1 question, 0 files.** The D9 roster (Honest limits §1). No file is marked
UNDETERMINED: every artifact in the tree carries at least a tier witness and the folder-level
retention ruling, and padding the sheet with UNDETERMINED rows to look thorough would be the
failure the contract names.

### Reported, not verdicted

Four measurements that belong to the operator's picture but are not proposals:

1. **The naming ratchet has held perfectly.** 137 top-level `.md` files violate the live Rule B —
   **every one of them a `class:` violation**, zero casing or slug violations — and they occupy a
   **closed historical band: 2026-03-30 → 2026-07-09, with nothing after it.** All 137 are
   grandfathered by `ADR-101` §6 (no retroactive rename); the rule binds ADDs only. **771 of 908**
   conform. This is the strongest clean signal in the folder and it deserves to be recorded as one.
2. **Two `.json` artifacts declare no consumer and would be refused if added today.**
   `2026-09-02-verification-base-failed-set-1e064921.json` and
   `2026-09-02-verification-parity-container-set-b5753f52.json` — measured against
   `consumer_at_landing._CITATION_RES` and `_NO_CONSUMER_RE`: neither matches. They are the only
   two post-`ARM_DATE` top-level artifacts that fail the declaration leg. The structural point:
   the corpus is recursive over **all** file types, but only prose can carry a `Consumers:` line, so
   a machine data set is admissible only through a gap.
3. **The consumer ratchet has moved 71 names since its baseline.** Against
   `ecosystem/audit-consumer-baseline.json` (630 unconsumed at 2026-09-01 / `9644e815`), today's
   stem-keyed replication gives **684 unconsumed of a 1,030-file corpus**: **+71 net-new, −17
   cleared**. **46 of the 71 net-new are lane-contract files with no date prefix** — i.e. debt the
   ratchet counts but no gate can ever refuse. **This is my replication, not the detector's output**
   (Honest limits §2); the delta's *shape* is the finding, and the shape is that the growth is
   concentrated in the class that is structurally unrefusable.
4. **One artifact carries a malformed slug that predates the grammar.**
   `2026-05-23-.dev-knowledge-audit.md` (816 B) — a leading `.` in the slug position, a
   machine-generated ecosystem report from an older `audit.py`, duplicating the genre of
   `2026-05-23-ecosystem-audit.md`. Grandfathered; **KEEP**; recorded so it is not rediscovered.

---

## Counts before → proposed after

Nothing moves under this census, so the "after" column is what the operator would get **if** the
one RELOCATE proposal were ruled and executed. It is a projection, not a state. All figures
exclude this lane's own two artifacts.

```
                                          before (21576e3a)   proposed after
docs/audits/ tracked files                        1,031            1,022
  top-level .md (excl. README.md)                   908              908
  top-level .html                                     2                2
  top-level .json                                     2                2
  README.md (generated index)                         1                1
  lane-contract subdirectory .md                    109              109
  lane-contract subdirectory .py                      9                0    -> RELOCATE
  lane-contract subdirectories                       12               12

corpus as consumer_at_landing counts it           1,030            1,021
artifacts after sidecar grouping                  1,028            1,019

bytes under docs/audits/                     17,593,435       17,563,616
  top-level artifacts                        16,373,613       16,373,613
  README.md                                     116,602          116,602
  lane-contract subdirectories                 1,103,220        1,073,401

VERDICT TALLY
  KEEP                                            1,019            1,019
  RELOCATE                                            9                0    (executed)
  ARCHIVE                                             0                0
  RETIRE                                              0                0
  UNDETERMINED (files)                                0                0

index coverage (docs/audits/README.md)        906 of 1,031     906 of 1,022
  indexable top-level .md on disk                   908              908
  index staleness                          2 artifacts behind   unchanged by this lane
```

The index row is deliberately unchanged: regenerating `README.md` is the integrator's single act
after the last of the 13 merges (`[#590]`), not this lane's.

---

## Honest limits

**This section is the point of the census. Seven things I could not establish.**

**1 · The D9 roster is UNRESOLVED — I never established which six files it names.**
The contract asks me to confirm "the six RETIRE files from D9" present or absent. D-numbered
decisions in this repo are carried on the operator's Drive transport, not in the tree:
`docs/audits/2026-09-06-technical-batch-u-manifest.md` names the source as
`DECLARE-SITTING-2026-09-06.md` (D1–D15), a `to-cc/` artifact. **`to-cc/` and `to-browser/` do not
exist in this container**, and neither does `BATCH-2026-09-07-SWEEP-CONTRACTS.md` — so I worked from
the relayed working copy in my prompt and could not read the authority file, as the contract's own
§ "Authority" instructs. What I searched, all negative for a six-file RETIRE roster:
`find` for `DECLARE-*` / `BATCH-2026-09-07*` (0 hits); every `D9` token in `docs/**` (all are
unrelated review- or decision-ids in other documents); every line pairing `RETIRE` with a
`docs/audits/` path; the 2026-09-05/06 groom, disposition, manifest and close-packet artifacts;
the active handoff bundle `docs/handoffs/2026-09-06-dev-knowledge-architect/`. **I did not guess a
roster, and I did not report the absence as clean.** If D9's six files are top-level `docs/audits/`
artifacts, the appendix lists every one of the 1,028 with its size and tier and the operator can
resolve them by name in one pass.

**2 · No repo detector was RUN. Every gate figure here is a re-implementation from imported
constants, not the gate's own output.** The container's `uv` is **0.8.17**; `pyproject.toml` pins
`required-version = "==0.11.19"`, so **every `uv run --locked` command in this repo fails before it
starts**, and the declared environment cannot be rebuilt. `python3 scripts/audit.py health` fails at
`ModuleNotFoundError: No module named 'click'`. `pre-commit` is not installed and
`.git/hooks/` holds no armed hooks. I therefore did **not** run `audit.py health`,
`funnel_coverage.py`, `consumer_at_landing.py`, `gen_audit_index.py --check`,
`validate_hermetization` as a hook, or the ship-gate `generated_artifact_freshness` leg. What I did
instead: imported `consumer_at_landing` and `validate_hermetization` directly (both are
stdlib-only) and applied **their** constants and **their** `rule_b_violation` function to the tree.
That makes the naming figures the gate's own logic; it makes the **consumption** figures a faithful
but independent replication of a substring match, and a replication can diverge from the original.
One divergence is visible and I do not reconcile it:
`docs/audits/2026-09-06-technical-archive-report-stage.md` reports *"unconsumed at landing
(audit.py health) 22"* at `a39edb2`, where my corpus-wide replication gives 684 unconsumed and a
+71 delta against the committed baseline. **These are different legs of different detectors and I
could not run either to settle it.** Do not read my 71 as a correction of their 22.

**3 · The clone is SHALLOW, so "last content commit" is not available as a witness for most of
this folder.** `.git/shallow` is present and `git log --oneline | wc -l` gives **278**; the
earliest reachable commit is dated **2026-09-01**. Every file that landed before that grafts to the
boundary and reports a false 2026-09-05/06 "last touched" date. **I discarded git dates as a witness
entirely** rather than report them — a first pass that used them produced an inventory in which 900
files appeared to have been edited yesterday, which is a measurement artifact and would have been a
lie in the table. Consequence: the verdicts in this census rest on **consumers and generators**, the
contract's other two witness forms, and on no commit dates at all. A dormancy question — *which
audits have not been touched in 90 days* — is **not answerable from this container**, and answering
it needs a full clone.

**4 · "Consumed" is a substring match, and the detector says so about itself.** A pool document
that names an artifact only to declare it obsolete counts as a citer
(`scripts/consumer_at_landing.py`, HONEST LIMITS). So tier A is *"some governance surface types
this name"*, never *"some governance surface depends on this."* I did not open 328 pool citations
to check which are live dependencies and which are historical mentions; at that volume it is a
separate lane's work. **Tier A is an upper bound on real consumption, not a measurement of it.**
The same weakness runs the other way for tier B: a corpus of 910 documents that cite each other 562
times may be a healthy evidence spine or may be an echo chamber, and this census does not
distinguish those two.

**5 · The 18 tier-F files are almost certainly a timing artifact, and I could not prove it.** All
18 are batch-U lane contracts dated 2026-09-06, in the batch whose wave 2 is draining **right now,
beside this lane**. Their consumers land when the lanes land. Reading them as orphans would be
wrong, and the honest statement is that **their tier is a photograph of an unfinished batch**, not
a verdict about them. I left them KEEP and flagged the reason rather than proposing anything. By
contrast the 17 tier-E top-level artifacts from 2026-08-27/29 are **past** that window, and I did
not establish whether their consumers were never written or were written and later removed —
answering that needs the deep history §3 denies me.

**6 · The measurement is a photograph of a moving tree, and it moved once while I was taking it.**
`origin/main` advanced `5f27b20` → `21576e3` mid-pass, adding one audit; I re-derived every number
at the later commit. Batch U wave 2 and twelve peer census lanes are still running, so the corpus
will differ from these figures by the time this merges. The pinned SHA is the only honest anchor,
and **the index-staleness figure in particular is a floor, not a value** — it grew from one artifact
to two across a single commit during this lane.

**7 · Gemini fan-out: NONE, and that is an absence, not a clean bill.** `which gemini` → not on
PATH. **No fan-out ran, so my locator-fabrication count is 0 out of 0 locators — a vacuous zero, not
a passing score**, and it must not be quoted as evidence that a fan-out was clean. Gemini-read
files: **0**. Every locator in this census was opened by me directly. **Copilot Enterprise offload
was NOT available and NOT used** — it is gated behind intake `#75`, unratified as of this commit;
recorded here so no later reading claims it was in play.

**Two further scope limits, stated plainly.** (a) I did not read the contents of the 1,028
artifacts. This is a census of names, sizes, references, grammar and gate-reachability — a
*bibliographic* pass. Nothing here says whether any given audit's findings are still true.
(b) The two `.md`/`.html` sidecar pairs are counted as one artifact each in the artifact tables and
as two files each in the byte and file-count tables; the appendix shows both paths on one row.
