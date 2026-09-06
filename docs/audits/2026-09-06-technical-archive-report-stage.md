# Archive REPORT-STAGE — the groom lane witnessed, its nine bundles re-resolved, and a folder-rot census (2026-09-06)

**Consumers:** `ADR-111` (every item below is a proposal into OWNED / DISCHARGED / CANDIDATE /
REJECTED triage; **no bundle is adjudicated here and no row is filed**) · the 2026-09-05 funnel
groom sheet, whose nine bundles this report re-resolves · the rows those bundles name — `[#613]`
`[#564]` `[#242]` `[#487]` `[#626]` `[#552]` `[#628]` `[#520]` `[#420]` `[#418]` · `ADR-110` and
`ADR-84` (the two amendment bundles) · intake `#43` / `#47` / `#51` ·
`protocols/STANDING_RULINGS.md` section AD candidates (g) and (k) ·
`docs/audits/2026-09-05-technical-r5-disposition-sheet.md` (R5 B1–B12, **DECLARED — read here, not
re-adjudicated**).

**Class:** technical, READ-ONLY. **Zero rows closed, zero files moved, zero deletions, zero
adjudications.** The verb throughout is **RETIRE-PROPOSED**. The operator rules the bundles.

**Lane:** `lane-t-000-v4-archive-report`, batch T contract §3.3, wave 1, cloud (read-only).

---

## 0 · THE PINNED SHA — every count below is measured at it, by this lane, not restated

```
HEAD                a39edb2d4cb8d16a024d1041c426337114edd3fa
resolved by         git rev-parse HEAD
branch at boot      (detached from refs/heads/main)
lane branch         claude/lane-t-000-v4-archive-report
git status          clean at boot; clean apart from this file at commit
git stash list      empty at boot and at STOP

groom sheet SHA     78daf4006c6d9231bb0f7dbfefbdfb911a659ce5   (the sheet's own pin)
distance            171 commits  (git rev-list --count 78daf400..HEAD)
```

---

## 1 · WITNESS — the groom lane RAN, and its artifact is on `main`

Contract leg (1). Each locator opened, not cited.

```
artifact        docs/audits/2026-09-05-technical-funnel-groom-sheet.md   PRESENT, 52,773 bytes
add commit      3d5a423525c40250f3bb83517bbc4e942ce71eb9
                "docs(audit): funnel groom -- READ-ONLY proposal sheet, nine bundles at 78daf400"
authored        2026-09-05 15:21:06 +0000
on main         git merge-base --is-ancestor 3d5a4235 origin/main  ->  exit 0   ANCESTOR
history         one commit; the file has never been edited since it landed (immutable, as ruled)
```

The sheet's own pinned SHA `78daf400` resolves at HEAD, and `git diff 78daf400 HEAD` over the
files the sheet quotes is what §2 and §3 below report.

### 1.1 The detectors it named, re-run by this lane at `a39edb2`

Every number in the left column is quoted from the groom sheet's §2 (its own measurement at
`78daf400`); every number in the right column was produced by this lane running the same detector
at HEAD. **No number in the right column is hand-derived** where the detector prints it.

```
detector                        at 78daf400 (sheet §2)        at a39edb2 (this lane)
funnel_lifecycle --report
  intakes                       57 live / 12 archived         62 live / 12 archived
  live ADRs                     89                            89
  rows                          364                           364
  leg a1 terminal-not-archived  0                             0
  leg a2 ACCEPTED-terminal      0                             0
  leg b  terminal ADR           0                             0
  leg c  post-cutoff provenance 5   (#35 #71 #123 #437 #518)  5   (same five ids)
  leg d  READY past threshold   0                             0
  exit                          1                             1

validate_git_backlog            OK — no closed-but-present    OK — no closed-but-present
                                drift ("full history")        drift ("full history")   << SEE §6.1

propose_closures                0 strong, 0 weak / 377 cmt    1 strong, 0 weak / 516 cmt
                                weak suppressed: cold start   weak suppressed: cold start
                                                              << the 1 STRONG is a FALSE POSITIVE, §6.2

boot_frontier                   5 proposed; 159 unblocked     5 proposed (SAME five ids);
                                in 170 open                   160 unblocked in 171 open

validate_doc_rot                75 loci past threshold        7 loci past threshold    << SEE §6.3
  backlog-row-length            70                            1 (now one aggregate locus)
  backlog-accretion             3                             5
  section-history               1                             0   (cleared)
  grooming-cadence              1                             1   (STILL FIRING, 38d)

funnel_coverage
  corpus N                      879                           899
  ledgers                       1                             2   (an R5 ledger landed)
  dispositioned                 78                            109
  pending                       2                             3
  uncovered                     726                           710

validate_adr_status             coherence=3 duplicate-id=2    coherence=3 duplicate-id=2
                                grammar=47 wrapped-value=1    grammar=47 wrapped-value=1
                                89 status fields              89 status fields

batch_manifest                  prints nothing, exit 0        prints nothing, exit 0
                                (zero open batches)           (zero open batches)
```

**The groom sheet's own leg-c detail moved and the sheet could not have known.** All five ids are
identical, but every one now reports `landed 2026-09-01` where the sheet reported
`landed 2026-08-31`. The rows did not change; the **clone's graft date** did — see §6.1.

### 1.2 Toolchain — declared, because the same defect the groom lane hit is still shipped

```
container uv        0.8.17
repo pin            required-version = "==0.11.19"     (pyproject.toml:25)
uv run --locked     REFUSED, verbatim:
    error: Required uv version `==0.11.19` does not match the running version `0.8.17`.

container python3   3.11.15
repo floor          requires-python = ">=3.12"         (pyproject.toml:15)
```

The dispatcher pin for this lane says *"run gates as `python3` by hand and DECLARE in your packet
that you did."* **That path is not available**, for the same two reasons the groom lane recorded:
the system interpreter is below the repo's floor and carries none of the declared dependencies.

**What was done instead, and it changes no repo file.** `uv==0.11.19` — the repo's own exact pin,
never a newer one — was installed into a throwaway venv **outside the repository**
(`<scratchpad>/uvenv`), and `uv sync --locked` rebuilt the declared environment into `.venv/`,
which is gitignored (`.gitignore:11`). No pin bumped, no lockfile touched. This is the resolution
the groom lane already recorded on `main` at `3d5a4235` §1; under C-3 a fork with a standing
in-repo precedent is followed silently rather than escalated, and it is reported here.

```
DETECTORS RUN UNDER `uv run --locked` AT THE PINNED uv 0.11.19:   ALL OF THEM
DETECTORS RUN UNDER THE python3 FALLBACK:                          NONE
```

One side-effect write, disclosed: `propose_closures.py` wrote `logs/PROPOSALS-2026-09-06-01.md`,
which is gitignored (`.gitignore:26`). Nothing outside this deliverable enters the commit.

---

## 2 · RE-RESOLUTION — every bundle witness, opened at HEAD

Contract leg (2). **41 locators across the nine bundles. 39 resolve. 2 have drifted**, both named
below with their live value. Nothing here re-adjudicates a bundle; it reports whether the evidence
the bundle rests on is still true.

### 2.1 The tally

```
bundle  verb        locators  resolve  drift  premise moved  VERDICT AT HEAD
B1      CLOSE        6         5        1      no            evidence INTACT (one line-number drift)
B2      AMEND-ADR    8         7        1      no            evidence INTACT (one line-number drift)
B3      AMEND-ADR    3         3        0      no            evidence INTACT
B4      REWORD       6         6        0      YES           evidence INTACT, one figure moved further
B5      REWORD       4         4        0      no            evidence INTACT
B6      REWORD       4         4        0      no            evidence INTACT and re-witnessed
B7      ARCHIVE      3         3        0      YES           HALF DISCHARGED since 78daf400
B8      RETIRE       4         4        0      no            evidence INTACT
B9      REWORD       3         3        0      YES           one leg is aimed at text that is
                                                             already correct
TOTAL               41        39        2
```

### 2.2 B1 · CLOSE `[#613]`

```
ecosystem/routing-table.yaml                       PRESENT, 3,552 bytes, tracked        RESOLVES
scripts/audit_checks/check_routing_agreement.py:64 `if state == "diverge":` -> Finding
                                                   (..., "fail", ...) at :65-67         RESOLVES
scripts/audit.py:4925  _tier(TIER_SHIP, check_routing_agreement)                        *** DRIFT ***
    live at HEAD:      scripts/audit.py:5011
    HEAD :4925 now reads `_tier(TIER_COMMIT, check_canonical_md_visibility),`
    cause: audit.py grew by 86 lines between the two SHAs; the registration itself is
    byte-identical, comment included (`# [#613] — L0 routing copy vs the`)
tests/test_routing_agreement.py                    PRESENT                              RESOLVES
merge 1e064921681873ff824d116ff9e167258e74647d     "Merge branch 'feat/g0-routing-
                                                   carrier' -- batch G opens..."        RESOLVES
tasks/613-in-repo-routing-table-agreement-check.md status: open                         RESOLVES
```

**New at HEAD, and it cuts against reading the row as detector-witnessed:** `propose_closures` now
emits `[#613]` as a **STRONG** hit. It is a false positive — see §6.2. The row is still closable
on B1's own three legs; it is *not* closable on the detector that now names it.

### 2.3 B2 · AMEND-ADR `ADR-110`

```
docs/decisions/ADR-110-...md   byte-identical to 78daf400 (git diff --stat: empty)
  :150  "**§2's 4–10 range is a design target, not a measured ceiling.** No batch above
         3 has run. The"                                                                RESOLVES
  :197  "...no batch above 3 has run, and the artifacts are"                            RESOLVES
  :290  "but no batch above 3 has run. Batch 2 is its first live exercise..."           RESOLVES
docs/audits/2026-08-28-technical-batch-2-manifest.md:5                                  *** DRIFT ***
    the `shape:` line the sheet quotes is at :4, not :5 — at HEAD **and at 78daf400**.
    An off-by-one in the sheet itself, not corpus movement. The quoted text is exact.
docs/audits/2026-08-31-technical-batch-e-manifest.md:4   shape: ... 15 committing lanes RESOLVES
docs/audits/2026-09-01-technical-batch-f-manifest.md:4   shape: ... 7 committing lanes  RESOLVES
docs/audits/2026-09-02-technical-batch-g-manifest.md:4   shape: ... 9 committing lanes  RESOLVES
docs/audits/2026-09-02-technical-batch-g-close-packet.md:21
                                "## 1 · THE QUEUE — nine lanes, all merged, all anchored" RESOLVES
```

ADR-110 carries four dated amendments at HEAD (`:172` 2026-08-06, `:206` 2026-08-07, `:293`
2026-08-12, `:310` 2026-08-12). **None of them is B2's**; the bundle is unexecuted.

### 2.4 B3 · AMEND-ADR `ADR-84`

```
docs/decisions/ADR-84-automation-writer-isolation.md:20
    "**Fact 2 — outputs are append-only with date-unique filenames.** ... Because filenames
     are date-unique and there is a single writer per stream, additive merges never collide,
     so no merge-cleanup step is needed."                                               RESOLVES
tasks/418-automation-fleet-audit-records-0-10-baselines-a.md:13
    "the writer branch carries up to 10 commits on a single day (2026-07-10)"           RESOLVES
protocols/STANDING_RULINGS.md:3561  candidate (k), the 208,062-byte collision, verbatim RESOLVES
```

`grep '^## Amendment' docs/decisions/ADR-84-...md` returns **nothing** — the ADR carries no dated
amendment at all. B3 is unexecuted.

### 2.5 B4 · REWORD `[#564]`

```
tasks/564-...md:12  quotes "86 live ADRs", "34 files with 16 ACCEPTED and zero archived —
                    there is no intake archive at all"                                  RESOLVES
docs/decisions/archive/            2 files (ADR-40, ADR-52)          UNCHANGED          RESOLVES
live ADR files                     89   (row says 86)                                   RESOLVES
docs/intake/ live                  62   (row says 34; sheet re-measured 57)             *** MOVED FURTHER ***
docs/intake/archive/               12   (row says "zero archived")                      RESOLVES
protocols/STANDING_RULINGS.md:691  "### H3 · An ADR archives at zero inbound references" RESOLVES
H3's predicate, re-measured over every tracked file at a39edb2:
    ADRs with ZERO inbound citation anywhere in the tracked tree:                    0
    ADRs cited by no file OUTSIDE docs/decisions|audits|handoffs|archive:            0
    method: for each docs/decisions/ADR-*.md, \bADR-<n>\b across `git ls-files`        RESOLVES
```

**B4's decisive claim survives re-measurement 171 commits later: H3 selects nothing.** Leg (a) of
`[#564]` is empty as specified; leg (b), the lag check, is untouched. The intake half of the row's
premise is now wrong by a wider margin than the sheet recorded (34 → 62 live, not 34 → 57).

### 2.6 B5 · REWORD `[#242]`

```
tasks/242-adr-status-flip-coherence-check.md:14  "Done when: a seeded ADR with a
    header↔README status divergence is flagged by an audit check, with tests"           RESOLVES
validate_adr_status at a39edb2, verbatim:
  [WARN] coherence: ADR-45 -- header 'Explored, not adopted' != README index 'Superseded'
  [WARN] coherence: ADR-46 -- header 'Partially superseded' != README index 'Accepted'
  [WARN] coherence: ADR-47 -- header 'Partially superseded' != README index 'Accepted'  RESOLVES
```

Three live divergences, same three ADRs, at both SHAs. Nothing dispositioned them in 171 commits.

### 2.7 B6 · REWORD `[#487]` — leg (v)

```
tasks/487-closure-proposal-consumption-arc-139-parked-prop.md   PRESENT                 RESOLVES
scripts/propose_closures.py:323
    _SINCE_RE = re.compile(r"since_commit:\s*([0-9a-fA-F]{7,40})")                      RESOLVES
.gitignore:26   logs/PROPOSALS-*.md                                                     RESOLVES
this lane's own run, a second independent non-operator checkout:
    since_commit: (none — cold start / no prior baseline)
    propose_closures: 1 strong, 0 weak over 516 commit(s) (weak suppressed: cold start) RESOLVES
```

**B6 is now witnessed twice, on two different cloud clones, 171 commits apart.** The WEAK leg has
never run off the operator's machine. §6.1 adds a second, sharper instance of the same class.

### 2.8 B7 · ARCHIVE — candidate (g) · **HALF DISCHARGED since the sheet was written**

```
protocols/STANDING_RULINGS.md:3538
    "**(g) Gemini/agy whole-corpus doctrine-coherence audit** *(ADDED by the 2026-09-02
     amendment)*. ... **H0 PRECONDITION**, alongside (a)."                              RESOLVES
    -- and `grep -n 'EXECUTED\|DISCHARGED' protocols/STANDING_RULINGS.md` matches NOTHING
       in section AD. Leg 1 of B7 is UNEXECUTED.
docs/audits/2026-09-05-technical-corpus-coherence-gemini.md:1  the artifact, in-tree     RESOLVES
disposition                                                                              *** MOVED ***
    at 78daf400: uncovered; the sheet proposed adding a row to
                 docs/audits/2026-08-17-technical-audit-disposition-ledger.md
    at a39edb2:  ALREADY DISPOSITIONED, as **PENDING**, in a NEW dated ledger —
                 docs/audits/2026-09-05-technical-r5-funnel-disposition-ledger.md:61
                 with the reason recorded verbatim: "Q: candidate (g) — does the Gemini
                 whole-corpus reader's finding set become a backlog row, or stay a Z-C
                 register candidate owned by the STANDING_RULINGS writer? ... FILINGS-1
                 holds the Z-C register for this inbox, so naming an owner here would be
                 this seat deciding another seat's allocation."
```

**Two consequences, reported not ruled.** (a) B7's *coverage* leg is discharged — `funnel_coverage`
counts the artifact under `pending`, not `uncovered`, and `ledgers` is now 2. (b) The repo took
exactly the lawful shape B7's own honest limit named as the alternative — *"the lawful shape is a
new dated ledger"* — so that honest limit is spent. What remains of B7 is leg 1 (mark candidate
(g) discharged in the register) plus converting `PENDING` → a term, and the ledger says out loud
that the term is an allocation another seat holds.

### 2.9 B8 · RETIRE — three READY intakes with no carrier

Re-run in full at HEAD over all 19 READY intakes (`status: READY` ∧ no `[#id]` in body ∧ no
citation from `tasks/` by filename ∧ no `intake #<n>` citation from `tasks/`):

```
intake  file                                                    body[#id] name-cit  intake#N  CARRIER
  43    docs/intake/2026-08-24-tech-ruling-register-landing-gap.md      no      no        no      NO
  47    docs/intake/2026-08-24-tech-supplement-probe-fill-state-defect.md no    no        no      NO
  51    docs/intake/2026-08-26-tech-provider-capacity-anthropic-compatible.md no no       no      NO
  ...   the other 16 READY intakes                                                       YES (all)

READY total: 19        READY with NO carrier: 3        identical set to the sheet's
```

`protocols/FUNNEL_LIFECYCLE.md:316` — `**READY threshold: 30 days.**` — RESOLVES. `funnel_lifecycle`
leg d is still 0. The three fire on **2026-09-23** (#43, #47) and **2026-09-25** (#51): **17 and 19
days out at HEAD**, down from the sheet's 18/20. Nothing has consumed them in 171 commits.

### 2.10 B9 · REWORD `[#626]`

```
tasks/626-logs-retention-exempts-the-prefixes-that-accumulate.md   PRESENT, status open RESOLVES
docs/audits/2026-09-02-technical-batch-g-close-packet.md:343
    "archived, apply_moves correctly REFUSES to overwrite it and aborts the whole plan"  RESOLVES
protocols/STANDING_RULINGS.md:3561  candidate (k), "Resolution is a naming decision ...
    and it is the operator's, so nothing was deleted."                                  RESOLVES
```

**One leg of B9 is aimed at text that is already correct, and this is a reporting finding, not a
re-adjudication.** B9 proposes *"correct `logs/proposals/` + `logs/detector-errors/` to the live
`logs/YYYY-MM/` bucketing"*. At HEAD the row's **Done-when already reads** ``logs/YYYY-MM/PROPOSALS-*.md``
verbatim. The `logs/proposals/` string the bundle targets appears in the row's **body**, where it
is a *quotation of intake #66's direction* that the row then answers — the row's own words:
*"`logs/proposals/` is not new work: it IS this row's relocation."* B9's **first** leg (name
candidate (k) as the row's precondition) is untouched by this and still applies: the row carries no
`BLOCKED-ON` marker at HEAD.

---

## 3 · FOLDER-ROT CENSUS — per top-level folder, with the RETIRE-PROPOSED list

Contract leg (3). **17 tracked top-level paths.** "Rot" here is operational and narrow: *the folder
holds artifacts whose own governing convention says they should have moved on, and the convention
has stopped being exercised.* Volume alone is not rot; a folder that is large by design is not
rotting.

**Result: 2 of 17 folders carry rot** — `docs/` and `protocols/`.

```
path              tracked  verdict     witness
docs/              1944    ROT         two loci; see 3.1 and 3.2
tasks/              391    no rot      3.3
tests/              220    no rot      audit.py health: proof_layer OK, 243 guards at baseline
scripts/            135    no rot      audit.py health: doc_code_coverage_drift OK (all 54
                                       ALL_CHECKS members covered); safe_removal OK
ecosystem/          105    no rot      generated indices + baselines; organ-index freshness is a
                                       pre-commit gate (CLAUDE.md §9)
templates/           49    no rot      3.4
deploy/              27    no rot      3.5
(root)               20    no rot      canonical_docs registry governs it; VISION.md is
                                       registry-RETIRED and already relocated to docs/archive/
.claude/             19    no rot      generated rosters, drift-gated (roster-freshness,
                                       claude-rosters-freshness)
protocols/           16    ROT         3.6
plugins/             11    no rot      one plugin, wholly live (tier1-lifecycle, enabled)
.devcontainer/        4    no rot      substrate declaration
logs/                 2    no rot      only 2 files TRACKED; the accumulation is gitignored and
                                       is `[#626]`'s, not a folder-rot finding
.vscode/              2    no rot      shared editor config, manifest-carried
config/               1    no rot      single file (requirements-dev.txt)
.github/              1    no rot
.claude-plugin/       1    no rot
```

### 3.1 `docs/handoffs/` — the archive convention stopped absorbing after one era

**This is the single largest rot locus in the repo**: 762 tracked files, 119 bundle directories in
the folder root, of which **exactly one is active**.

The convention is stated by the folder's own runbook and is unambiguous:

```
docs/handoffs/README.md:222-223
    "...older eras are archived, not deleted."
docs/handoffs/README.md:237
    "**v3.2 (2026-05-09 → 2026-05-25, ADR-42)** — twelve-file flat folder. Historical."
docs/handoffs/README.md:238
    "**Pre-v3.2 (legacy)** — ... under `archive/legacy/`."
```

`docs/handoffs/archive/` EXISTS and holds **15** bundles — so the mechanism is built and was
exercised. Its newest entry by name is `2026-05-25-corp-monorepo-session-sync`. **It has absorbed
nothing since.** Every bundle cut on or after 2026-05-09 sits in the folder root:

```
era                       date range              bundles in ROOT   README status
v3.2                      2026-05-09 → 2026-05-25       15          "Historical"
v4                        2026-05-29 → 2026-06-10       13          prior era; templates retained
v5                        2026-06-11 → 2026-07-30       68          "prior era"
v6                        2026-07-31 → 2026-08-31       21          "the immediately prior era"
v7 (canonical)            2026-09-01 →                   2          canonical
                                                       ---
                                                       119
active bundle (newest by git add-date, CLAUDE.md §1 predicate):
    docs/handoffs/2026-09-06-dev-knowledge-architect
```

**Ownership check, run before proposing anything (ADR-111: one triage per finding).** Two open rows
sit near this and **neither owns it**:

- `[#520]` *"No sanctioned way to retire a committed bundle whose seal is wrong"* — scoped to a
  **marker surface for a mis-sealed bundle**, one named bundle, `check_seal_identity`. Not era
  archival.
- `[#420]` *"Does a TOP-LEVEL `docs/archive/` still make sense?"* — scoped to `docs/archive/`, and
  its body explicitly notes that `docs/handoffs/archive/` already exists as a per-area archive. It
  also carries a standing instruction this report obeys: *"**Do NOT touch `docs/archive/` while
  this is open** — no move, no promotion, no deletion."*

**No open row owns handoff-bundle era archival.** That is the finding; filing the row is an act and
this lane files nothing.

#### RETIRE-PROPOSED

```
RP-1   docs/handoffs/  15 v3.2-era bundles (2026-05-09 → 2026-05-25)
       -> docs/handoffs/archive/
       CONFIDENCE  high. The README calls this era "Historical" in as many words (:237), and
                   archive/ already holds 15 bundles of the SAME era and date range.
       RISK        the lowest of the four; this is finishing a move that was started.

RP-2   docs/handoffs/  13 v4-era bundles (2026-05-29 → 2026-06-10)
       -> docs/handoffs/archive/
       CONFIDENCE  medium, and the caveat is load-bearing. README:234-236 says v4 is
                   "**Still live for cross-repo handoffs** (corp-monorepo and any v4 repo) per
                   ADR-83; the v4 templates under `templates/handoff/` are intentionally
                   retained." What is retained is the TEMPLATES, under templates/, not these
                   thirteen dated bundle records. Archiving the records leaves the live v4
                   template set untouched. If the operator reads the retention as covering the
                   records too, RP-2 is REJECTED and RP-1 stands alone.

RP-3   docs/handoffs/  68 v5-era bundles (2026-06-11 → 2026-07-30)
       -> docs/handoffs/archive/
       CONFIDENCE  medium-high. README:231 labels v5 "prior era" and :222 rules that older eras
                   are archived. 68 bundles is 57% of the folder root.

RP-4   docs/handoffs/  21 v6-era bundles (2026-07-31 → 2026-08-31)
       -> HOLD, do not archive yet.
       REASON      README:221-222 singles v6 out as "the immediately prior era", and v7 is five
                   days old. Archiving the era a reader may still need to diff against is the
                   one move here with a real cost. PROPOSED: hold until v7 has a second month.
```

**Every RP above is a MOVE inside `docs/handoffs/`, to a destination that already exists.** No file
is deleted, no new repo folder is created, and bundle bytes are unchanged — which is what keeps it
compatible with bundle immutability (CLAUDE.md §5 rule 3): archival relocation is not an edit.

**Projected effect, if RP-1 + RP-2 + RP-3 are ruled and RP-4 held:**

```
                       before (a39edb2)     after (projected)
docs/handoffs/ root         119 bundles          23 bundles   (21 v6 + 2 v7)
docs/handoffs/archive/       15 bundles         111 bundles
files tracked under docs/handoffs/   762            762       (a move, not a deletion)
```

### 3.2 `docs/audits/` — 710 uncovered, and the unconsumed set grew

```
corpus N                                    899   (funnel_coverage, excludes README.md)
uncovered (no disposition in any ledger)    710
unconsumed at landing (audit.py health)      22   <- was 13 at 78daf400, per the groom sheet §5
```

**RETIRE-PROPOSED: none.** `docs/audits/` deliberately has no archive (`ADR-100` keep-all-accepted,
restated in `[#420]`'s own body), so there is nothing to retire *to*. The disposition backlog is
already OWNED by `[#552]` — *"Window-close disposition + archival routine — every new audit gets a
disposition"* — and ADR-111 admits one triage per finding, so no second row is proposed. Recorded
as a **rot locus with a live owner**, not as a candidate.

The unconsumed set grew from 13 to 22 in 171 commits. **9 of the 9 net-new entries are lane and
batch artifacts from 2026-09-05**, i.e. the same normal-latency shape the groom sheet named — and
the same shape R5's B1 already ruled on. Not re-adjudicated here.

### 3.3 `tasks/` — 140 terminal row files retained, and that is by design

```
tasks/*.md                365 files  (364 rows + tasks/README.md, which carries no `status:`)
  status: open            171
  status: deferred         53
  status: closed          135
  status: retired           4
  status: superseded        1
terminal rows retained in tasks/   140   (38% of the folder)
BACKLOG.md rows                    224   == open + deferred, exactly
tasks/archive/                      25 files — ANNOTATIONS ("Archived annotations:
                                    tasks/archive/146.md"), not archived rows
```

**No rot.** `audit.py health` reports `task_tree_coherence: BACKLOG.md coherent with the tasks/
source of truth (structure + frontmatter honesty + full reassembly)`. A closed row's file staying
in `tasks/` while dropping out of the generated `BACKLOG.md` is the designed shape — the groom
sheet's own §4 states it: *"closing retires, never deletes."* **RETIRE-PROPOSED: none.**

### 3.4 `templates/` — no rot; the retention is explicit

The v4 handoff templates under `templates/handoff/` are the one obvious stale-looking set, and
`docs/handoffs/README.md:235-236` retains them **by name**: *"the v4 templates under
`templates/handoff/` are intentionally retained"* per ADR-83. **RETIRE-PROPOSED: none.**

### 3.5 `deploy/` — seven manifest versions, and every one is still cited

The folder carries `manifest-v1.0.0` … `manifest-v1.5.0` (7 files) with only v1.5.0 live. Inbound
citation count over every tracked file, excluding self and the generated indices:

```
deploy/manifest-v1.0.0.yaml      16 inbound   (2 from the governance pool)
deploy/manifest-v1.1.0.yaml      20 inbound   (2)
deploy/manifest-v1.2.0.yaml      34 inbound   (7, incl. protocols/REPO_ONBOARDING.md)
deploy/manifest-v1.3.0.yaml      13 inbound   (2)
deploy/manifest-v1.3.1.yaml      12 inbound   (5)
deploy/manifest-v1.4.0.yaml      63 inbound   (8, incl. ADR-92)
deploy/manifest-v1.5.0.yaml      15 inbound   (2, incl. protocols/HANDOFF_PROCESS.md)
```

Zero orphans. A superseded manifest that an ADR and a protocol still cite is a record, not residue.
**RETIRE-PROPOSED: none.**

### 3.6 `protocols/` — one superseded file still living in the boot folder

```
protocols/ESSENTIALS.md      16,461 bytes
  frontmatter:               status: superseded      (line 3)
  body line 9:               "> **SUPERSEDED — not a boot read.** Dissolution tracked in
                              `[#628]` with v1.5.0. Live boot frame = `CLAUDE.md` +
                              FUNNEL HEALTH + north-star."
  CLAUDE.md §1 item 2:       "**SUPERSEDED, pending `[#628]`.** Not a boot read; skip it."
  inbound citations:         391 across the tracked tree (34 from the governance pool,
                             including CLAUDE.md itself)
  tasks/628-dc2-recut-essentials-dissolution-is-a-release-act.md   status: open
protocols/archive/           2 files (HANDOFF_PROCESS_v3.4.md, v4.4.md) — the mechanism exists
```

**RETIRE-PROPOSED: none — and the reason is the finding.** With 391 inbound references, moving
`ESSENTIALS.md` to `protocols/archive/` breaks 391 locators; the retirement is a **dissolution**
(re-point every consumer, then remove), which is precisely what `[#628]` is scoped to and why it is
titled *"…dissolution is a release act."* The rot is real — a boot-folder file that every boot
instruction tells the session to skip — and it is **OWNED and open**. Recorded, not proposed.

### 3.7 Two adjacent facts found while censusing, neither of them rot

- **`docs/decisions/` carries 2 duplicate-id files** — `ADR-51-amendment-2026-07-05-...` and
  `ADR-70-amendment-2026-07-07-...` each claim a number an existing ADR already holds, and
  `validate_adr_status` reports index coherence as *"ambiguous for all of them"*. A naming class,
  already a standing WARN in the `adr_status_grammar` baseline. Not proposed.
- **`[#420]`'s own count has moved.** The row says `docs/archive/` holds *"9 external-research /
  scoping / evidence files"* and its Done-when says *"each of the 22 files given a destination."*
  At HEAD the folder holds **23** content files plus `README.md` — `VISION.md` arrived there on
  2026-08-29 under `[#614]` lane-e-5 (CLAUDE.md §5 rule 5). Same class as B4: a row whose measured
  premise drifted. Reported for the operator; **no reword is proposed here** — that is a bundle,
  and this lane authors none.

---

## 4 · COUNTS — before (re-measured at HEAD) → projected after

Contract leg (4). Every **before** figure is a detector's own output at `a39edb2`, produced by this
lane. **No before figure is copied from the groom sheet or from the contract.** The projections
assume the nine bundles are adopted exactly as the sheet wrote them; the RETIRE-PROPOSED column is
separate, because it is a different decision.

```
INTAKES                          before   after (9 bundles)          after (+RETIRE-PROPOSED)
  live                             62     59 (if #43/#47/#51 retire)   unchanged — no RP here
                                          62 (if all three ratify)
  archived                         12     15 / 12  correspondingly     unchanged
  READY (frontmatter)              19     16                           unchanged
  READY with no carrier             3     0                            unchanged
  ACCEPTED                         19     19 (retire) / 22 (ratify)    unchanged
  source: funnel_lifecycle.py --report; the carrier join is §2.9

AUDITS                           before   after (9 bundles)          after (+RETIRE-PROPOSED)
  corpus N                        899     900  (this report)           900
  ledgers                           2     2                            2
  dispositioned                   109     110  (B7: PENDING -> a term) 110
  pending                           3     2                            2
  uncovered                       710     711  (this report lands
                                                undispositioned, as
                                                every audit does)      711
  unconsumed at landing            22     23                           23
  source: funnel_coverage.py; scripts/audit.py health (consumer_at_landing)

ADRs                             before   after (9 bundles)          after (+RETIRE-PROPOSED)
  live ADR files                   89     89   (amendments are
                                                in-file, never new
                                                numbers)               89
  archived                          2     2                            2
  ADR-110 dated amendments          4     5    (B2)                    5
  ADR-84  dated amendments          0     1    (B3)                    1
  header-vs-README divergences      3     3    (B5 rewords the row,
                                                it does not fix the
                                                ADRs)                  3
  duplicate-id                      2     2                            2
  ADRs meeting H3 (zero inbound)    0     0    (leg (a) of [#564]
                                                stays empty)           0
  source: funnel_lifecycle.py --report; validate_adr_status.py; H3 re-measured in §2.5

TASKS                            before   after (9 bundles)          after (+RETIRE-PROPOSED)
  rows                            364     364  (closing retires,
                                                never deletes)         364
  open                            171     170  (B1 closes [#613])      170
  deferred                         53     53                           53
  closed                          135     136                          136
  retired                           4     4                            4
  superseded                        1     1                            1
  BACKLOG.md rows                 224     223                          223
  rows reworded                     -     4    ([#564] B4, [#242] B5,
                                                [#487] B6, [#626] B9)  4
  rows FILED by this report         -     0                            0
  source: funnel_lifecycle.py --report (rows 364);
          split reproduced: grep -h '^status:' tasks/*.md | sort | uniq -c

HANDOFF BUNDLES                  before   after (9 bundles)          after (+RETIRE-PROPOSED)
  in docs/handoffs/ root          119     119  (no bundle touches
                                                handoffs)             23   (RP-1+2+3; RP-4 held)
  in docs/handoffs/archive/        15     15                          111
  files tracked under docs/handoffs/  762  762                        762  (a move, not a delete)
  source: this lane's era classification, §3.1
```

**Deltas the 171 commits produced, stated so the operator is not surprised by a moved number:**
intakes `57 → 62` (five new, all 2026-09-05); audits `879 → 899` (23 added); dispositioned
`78 → 109` and uncovered `726 → 710` (the R5 ledger landed); open rows `170 → 171` and deferred
`54 → 53` (one row un-deferred); unblocked `159 → 160`. ADRs and total rows are unmoved.

---

## 5 · WHAT WAS CHECKED AND FOUND CLEAN — recorded so it is not re-derived

- **Every one of the nine bundles is still UNEXECUTED.** `[#613]` is `status: open`; ADR-110 and
  ADR-84 carry no new dated amendment; `[#564]` / `[#242]` / `[#487]` / `[#626]` carry their
  original wording; the three READY intakes are unchanged; section AD carries no EXECUTED marker.
  The one movement is B7's coverage half (§2.8), and it was moved by a different lane's ledger.
- **R5's B1–B12 are DECLARED and were not re-adjudicated.** Their headings were read
  (`docs/audits/2026-09-05-technical-r5-disposition-sheet.md` §2, twelve bundles) to establish
  ownership boundaries only. Two of their subjects are visibly half-landed at HEAD — R5 B7's
  `section-history` locus is cleared and its `grooming-cadence` locus is not — and that is
  **reported, not ruled**.
- **The grooming-cadence locus that motivated the groom lane is STILL FIRING.**
  `grooming-cadence BACKLOG#grooming-cadence -> last groom 2026-07-30, 38d ago (> 21d cadence,
  ADR-41)`. The groom sheet said *"adjudicating this sheet is what clears it"*; the sheet has not
  been adjudicated, so it has not cleared. It was 37d at `78daf400`.
- **Zero open batches.** `batch_manifest.py` prints nothing and exits 0, at both SHAs.
- **Zero ADRs meet H3.** Re-measured over every tracked file (§2.5), not inherited.
- **No orphaned deploy manifest, template or protocol file** (§3.4–3.6). Every candidate tested for
  inbound citation came back cited.
- **`docs/archive/` was not touched, examined only.** `[#420]` carries a standing "do not touch
  while this is open" and it is open.

---

## 6 · INSTRUMENT FINDINGS — five, and the first one re-prices every number in §1.1

These are **not** bundles and **not** proposals against a row. They are facts about the measurement
apparatus that a reader of either sheet needs, and three of them make an existing detector's or
test's output unsafe to read at face value. **None is filed; each names its likely owner.**

### 6.1 This clone is SHALLOW, and the repo's own guard says so out loud

```
git rev-parse --is-shallow-repository        true
git rev-list --count HEAD                    516
git rev-list --count --first-parent HEAD     137
"first" commit                               b7fef9b  2026-09-01   <- a graft, not a root

scripts/cloud_provisioning.py history   (read-only, NO --repair), verbatim:
  [cloud-provisioning] INFO  history: main walks 85 first-parent spine entries
  [cloud-provisioning] ERROR history: clone is SHALLOW - every history-dependent detector
                                      reads vacuously
  [cloud-provisioning] ERROR history: ref 'main' is BEHIND origin/main (a39edb2d4) - the spine
                                      walk would miss every entry in between and still report
                                      clean
  exit 1   (= "a real violation: looked, and found drift")
```

`cloud_provisioning.py`'s own docstring states the design intent — *"history B1. Leg 2 unshallows,
so a cloud clone has DEPTH"* — and sizes the repo at *"~5400 commits"*. **This lane's clone carries
516.** The unshallow leg did not run for this cloud session. Per the receipt gate, the container
was **not repaired**: a lane that repairs its own container destroys the receipt it exists to
produce.

**Three consequences, and they are load-bearing:**

1. **`validate_git_backlog` renders a green that says `full history` on a clone that has none.**
   `scripts/validate_git_backlog.py:123` prints the literal string `(direction (a) STRONG, full
   history)` unconditionally, and `grep -n 'shallow' scripts/validate_git_backlog.py` matches
   **nothing**. `audit.py` DOES guard the same hazard — `_git_is_shallow` at `:996`, raising
   `DerivationRefused` at `:1303-1307` with *"the clone is shallow -- every git-derived date is a
   floor, not a fact"* — so the guard exists in one organ and is absent from the other. **The
   groom sheet's §2.2 green and this report's §1.1 green are both vacuous**, and neither sheet
   could have known from the detector's own output.
2. **Every date in `funnel_lifecycle` leg c is a graft floor.** The same five rows report
   `landed 2026-08-31` at `78daf400` and `landed 2026-09-01` at `a39edb2`. The rows did not move;
   the graft did.
3. **`propose_closures`'s window is a shallow window.** `377` then, `516` now — both are the depth
   of the clone, not the history of the repo.

**This is `[#487]` leg (v) generalised.** B6 found that the closure *baseline* does not travel;
this finds that the *history the baseline indexes* does not travel either, and that one detector
reports full coverage over it anyway. Whether that becomes a leg (vi) on `[#487]`, a row against
`validate_git_backlog`, or a provisioning row is the operator's call — **this lane files nothing**.

### 6.2 `propose_closures` now emits a STRONG false positive, and its cause is the groom sheet

```
propose_closures: 1 strong, 0 weak over 516 commit(s)
  - [ ] **#613** — [P2][M] In-repo routing table + L0 agreement check
        evidence: `3d5a42352` docs(audit): funnel groom -- READ-ONLY proposal sheet, ...
```

**No commit in the repository carries `closes [#613]`.** `git log --all --grep='closes \[#613\]'`
returns nothing. What `3d5a4235` carries, in its commit **body**, is the groom lane's own narration
of its own proposal:

```
Nine bundles: CLOSE [#613] (routing carrier landed at 1e064921, agreement check armed
TIER_SHIP -- a closable row no detector can see); ...
```

`scripts/propose_closures.py:51` — `CLOSES_RE = re.compile(r"\b(?:closes?|closed|fixes?|fixed)\s+\[#(\d+)\]", re.I)`
— matches `CLOSE [#613]` (the `s` is optional and the match is case-insensitive), and the `[#437]`
quoting guard at `:53-54` does not fire because the token is bare prose, not quoted.

**The shape, stated generally because it will recur:** a READ-ONLY proposal artifact that describes
a proposed closure in its commit message is indistinguishable, to the STRONG leg, from a commit that
performed one. The sheet's §2.3 recorded *"a closable row no detector can see"*; one day later the
detector sees it, for the wrong reason. STRONG is documented as *"precise regardless"* of the
cold-start suppression — that precision claim is what this falsifies. Reported; **no row filed**.

### 6.3 The doc-rot delta is an INSTRUMENT change, not a corpus improvement

`validate_doc_rot` reports **75 loci** at `78daf400` and **7** at `a39edb2`. That is not 68 loci
cleared:

```
git diff --stat 78daf400 HEAD -- scripts/validate_doc_rot.py
  scripts/validate_doc_rot.py | 187 ++++++++++++++--------  163 insertions(+), 24 deletions(-)
```

The `backlog-row-length` arm was re-shaped from **70 per-row loci into 1 aggregate locus** carrying
a distribution (`71 of 224 rows over the declared ceiling 1320 chars … p50/p75/p90 =
1259/1555/2276`) — the change `docs/audits/2026-09-05-technical-r5p-lane1-docrot-arm2.md` landed.
Underneath, the row-length population **grew** from 70 to 71. `section-history` genuinely cleared
(1 → 0); `backlog-accretion` **grew** 3 → 5. Anyone diffing the two totals without the instrument
diff reads a 91% improvement where the corpus got slightly worse.

### 6.4 The `[#590]` narrowing reached the pre-commit hook and NOT the test suite

Found by running this lane's own targeted tests, and reported because it decides what "green in a
lane" can mean for any lane that writes an audit.

```
targeted tests for this diff (one new docs/audits/*.md file), at a39edb2:

  scripts/validate_hermetization.py            EXIT 0   PASS   (Rule A + Rule B; computes its
                                                               own staged-add set, so a bare
                                                               invocation is not vacuous here)
  scripts/gen_audit_index.py --check-titles    EXIT 0   PASS   (audit-title-gate)
  pytest tests/test_validate_hermetization.py           PASS
  pytest tests/test_audit_index_merge_free.py           PASS
  pytest tests/test_gen_audit_index.py                  2 FAILED, and see below
      FAILED test_live_index_is_fresh
      FAILED test_live_index_excludes_nothing_because_every_audit_is_tracked
      both, verbatim: "gen_audit_index: docs/audits/README.md is stale vs docs/audits/"
      the entire diff both assert on is ONE line plus the corpus count: 899 -> 900
  total: 78 passed, 2 failed
```

`[#590]` narrowed the **pre-commit hook** `audit-index-freshness` to `docs/audits/README.md` and
`scripts/gen_audit_index.py`, and the config states the reason in as many words at
`.pre-commit-config.yaml:106-112`: *"`files:` used to match ANY `docs/audits/*.md`, which made
regenerating the index mandatory for every lane that wrote an artifact — and under the ADR-110
batch protocol every lane writes one. That is what put this file in 6 of the last 7 conflicted
merges (86% of all manual merge resolution in the repo)."*

**`tests/test_gen_audit_index.py` was not narrowed with it.** Both failing tests call
`gen_audit_index.main(['--check'])` over the live tree, so **any lane that adds an audit and runs
this module turns it red**, and the only way for that lane to make it green is to regenerate the
shared index — which is precisely the act `[#590]` removed and this lane's dispatcher pin
forbids.

**This is coherent with the batch design and still worth naming.** The `[#528]` cadence is
*targeted tests in-lane, one full suite at integration*, and the integrator regenerates the index
once on the merged result — at which point both tests go green. So the sequence works. What does
not work is a lane trying to reach green on its own diff: for this artifact class, in-lane green is
unreachable by construction, and a seat that does not know why will either regenerate the index
(re-creating the merge coupling) or disposition the failure (a named anti-pattern). The
`audit-title-gate` config block at `.pre-commit-config.yaml:126-131` shows the repo already
reasoning about exactly this separation for hooks — *"This check WRITES NOTHING and touches no
shared artifact, so arming it on the audits tree re-creates none of that coupling"* — the same
reasoning has not been applied to the test module.

`[#590]` is **open**. Whether this becomes a leg on it is the operator's call; **this lane files
nothing**.

### 6.5 `audit.py health` at HEAD, in this substrate

```
health: DEGRADED        self-audit 35/87 pass;  markers: 38 [OK] · 33 [~~] · 16 [--] · 4 [!!]

the four [!!]:
  repos registered  (none)
  canonical_freshness: derived leg REFUSES (shallow clone)
  hooks_armed: git hooks not armed (RF-2)
  journal_spine_anchor: backstop could not complete (AnchorError('disposition floor 24882f8cc
    is not an ancestor of main: ... fatal: Not a valid object name 24882f8cc'))
```

**All four are container-provisioning consequences, not repo defects**, and `cloud_provisioning.py`
is the organ built to repair exactly three of them (`history`, `ecosystem`, and the hook arming
that `SessionStart` does elsewhere). It did not run for this session. **The container was left as
found** — the receipt gate forbids repairing it, and a repaired container reports a health verdict
that is not the substrate's own.

---

## 7 · BEFORE → AFTER

The line this lane's contract §3.3 names, with the **before half re-measured by this lane at
`a39edb2`**, never restated from the contract:

```
before   archive candidates verified: 0/41 witnesses resolved at HEAD — the nine bundles were
         witnessed once, at 78daf400, 171 commits back, and nothing had re-opened a locator since;
         folders with rot: 0 of 17 censused

after    archive candidates verified: 39/41 witnesses resolve at a39edb2 — 2 locator drifts, both
         named with their live value (audit.py:4925 -> :5011; batch-2 manifest :5 -> :4, an
         off-by-one present at the sheet's own SHA); 3 bundles carry a premise that moved (B4, B7,
         B9) and B7's coverage half is already discharged by a ledger that landed since;
         folders with rot: 2 of 17 (docs/, protocols/)
```

---

## 8 · HONEST LIMITS

1. **This report executes nothing and files nothing.** No row closed, no status flipped, no file
   moved, no candidate marked EXECUTED, no backlog id allocated. The RETIRE-PROPOSED list in §3.1
   is four proposals, and every one of them is a move to a directory that already exists.
2. **`docs/audits/README.md` was deliberately NOT regenerated** (dispatcher pin; `[#590]` narrowed
   `audit-index-freshness` to that file precisely because it dominates merge conflicts). This
   report therefore lands with the index stale by one entry, on purpose. The integrator regenerates
   once on the merged result. **The direct consequence is that this lane's targeted-test run is
   78 passed / 2 failed, and both failures are that one stale entry** — stated plainly rather than
   reported as green, and analysed in §6.4. This lane does not disposition them to reach green;
   dispositioning to reach GREEN is a named anti-pattern.
3. **The shallow clone bounds what this lane could witness.** §6.1 states it in full. Concretely:
   nothing here should be read as a claim about the repo's history before 2026-09-01, and the two
   `validate_git_backlog` greens (the sheet's and this one's) are vacuous rather than false.
   Everything else in this report is measured over the **working tree** at `a39edb2` — file
   contents, frontmatter, detector output over the tree — which the graft does not affect.
4. **The folder-rot census's definition of rot is narrow and stated** (§3 preamble). A different
   definition — bytes per folder, age, read frequency — produces a different list. Under a
   size-only definition `docs/audits/` would lead; under this one it is a locus with a live owner
   and no archive to move to.
5. **§3.1's era classification is derived from bundle-directory dates against the README's own
   era table** (`docs/handoffs/README.md:225-238`), not from each bundle's internal format. A
   bundle cut in one era's window using another era's shape would be misclassified. The counts sum
   to 119, matching the directory listing.
6. **Inbound-citation counts in §3.5 and §3.6 use substring matching** over `git ls-files`,
   excluding the file itself and the four generated indices. They are safe as a **non**-orphan
   proof (a hit is a hit) and unsafe as an orphan proof (a miss could be a rename). Nothing here
   rests on a zero.
7. **B7 and B9 are reported as moved, not re-scoped.** Rewriting either bundle is authoring, and
   the operator rules the bundles.
8. **No peer session was reachable.** `ListAgents` returned no other Claude session, so
   `integrator`, `dispatcher-T` and `filings-N` could not be addressed. The HANDBACK and SESSION
   content is carried in §9 instead, per this lane's substrate note.

---

## 9 · SESSION / HANDBACK — carried in-artifact, because the browser channel is off-substrate

This lane runs off the operator's machine. `to-cc/` and `to-browser/` are on the operator's disk
and are **not reachable from this substrate**, which C-0 anticipates: *"If the path is unreachable
from your substrate, write that fact in your STATUS/SESSION file and proceed only on what the
dispatch brief carried."* That is what this section is.

```
SESSION   lane-t-000-v4-archive-report
peers     ListAgents -> none reachable. integrator, dispatcher-T, filings-N: UNREACHABLE.
          No peer message was sent or received. No peer message was treated as authority.
HANDBACK  claude/lane-t-000-v4-archive-report @ <the commit that adds this file>  [docs-only]
QUESTION  none raised. No fork this lane hit fell into C-3's three classes:
            (a) no curated-baseline file was touched — the diff is one new docs/audits/ file;
            (b) no rule-vs-ruling conflict arose;
            (c) the one real fork — an unusable toolchain (§1.2) — has a standing in-repo
                precedent at 3d5a4235 §1, so it was followed silently and reported, per C-3's
                own instruction that a covered fork is not escalated.
DEVIATIONS reported per C-2, batched here rather than dripped:
          1. The dispatcher pin's python3 fallback was UNUSABLE (§1.2). The groom lane's
             recorded resolution was used instead. Declared, not silent.
          2. `docs/audits/README.md` NOT regenerated — dispatcher pin, deliberate (§8.2).
          3. The container was NOT repaired despite four [!!] health markers (§6.5) — the
             receipt gate forbids it.
TEARDOWN  the scratchpad venv and the three read-only scripts written into it are OUTSIDE the
          repository and outside the tree; `.venv/` and `logs/PROPOSALS-2026-09-06-01.md` are
          gitignored. `git status` carries this file and nothing else. `git stash list` empty.
```

**Substrate deviation, declared:** `substrate-teardown-enum-coverage`. This lane's branch is
`claude/lane-t-000-v4-archive-report`, minted by the cloud transport, which `LANE_BRANCH_RE`
deliberately does not match — so the lane is invisible to an enum-iterating teardown. The discharge
the rule's own text names is enumeration by slug in the batch-T manifest, and the dispatcher carries
it in the close packet's teardown list.

### 9.1 One locator in the frozen contract does not resolve in this substrate

Reported rather than silently worked around, in the same shape the groom sheet used for its §6.

```
"docs/audits/2026-09-06-technical-batch-t-manifest.md, ## THE LANES"        DOES NOT RESOLVE
    cited by this lane's contract as the discharge for the teardown-enum deviation.
    At a39edb2:  `git ls-files docs/audits | grep 2026-09-06`  matches NOTHING, and
                 `git log --all -- 'docs/audits/*batch-t*'`    matches NOTHING.
    reading:     the manifest is not on origin/main at this lane's clone SHA — it is either
                 unpushed on the dispatcher's checkout or held on the operator's disk. A cloud
                 session clones from `origin` and cannot see either.
    effect:      NONE on this report's findings. The deviation is declared here regardless, so
                 the enumeration exists in a committed artifact even if the manifest lands later
                 or under a different name. The dispatcher owns reconciling the two.
```

The other repo locators the contract carries — `scripts/validate_branch_naming.py`
(`LANE_WORKTREE_RE`), `[#590]`'s narrowing of `audit-index-freshness`, `[#528]`,
`validate-hermetization` Rule B's audit-name grammar (`AUDIT_CLASS_ENUM`, which admits
`technical`), `protocols/STANDING_RULINGS.md` — all resolve, and each was opened before it was
relied on.
