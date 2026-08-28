# NB2 · CLOUD FM-C — FULL FUNNEL CENSUS (READ-ONLY)

**Lane:** night-batch-2 wave 1, FM-C · **Repo:** `dev-knowledge` · **Revision:** `origin/main` @ `fcc9485567f81814d24b84fe2db5ceff23b743ee` · **Substrate:** cloud · **Date:** 2026-08-28
**Contract of record:** `docs/audits/2026-08-28-technical-batch2-launch-contracts/NB2-CLOUD-FMC-funnel-census.md` (read and compared — the dispatched brief matches it)
**Posture:** zero writes, zero deletes, zero commits, zero branches, zero tags. Proof at §9.
**Coverage:** all four directories completed in full. `docs/audits/` is **not** a partial.

---

## 0. PREMISE DEFECTS FOUND BEFORE EXECUTING — read these first

Four premises in the brief do not hold on the clone. Each was worked around; each is named because FM-3 inherits them.

**P1 — `tasks/` rows have no `source:` field. Zero of 344.**
The brief's backward direction is defined as *"for every OPEN `tasks/` row, does its `source:` resolve"*. The `tasks/` frontmatter schema is `id · title · status · priority · size · theme · story · generates` — there is no `source:`.

```
$ grep -l '^source:' tasks/*.md | wc -l          -> 0
$ awk '/^---$/{n++;next} n==1{print $1}' tasks/*.md | sort -u
generates:  id:  priority:  size:  status:  story:  theme:  title:
```

**Substitute used, and it is complete:** every row body carries a `· refs …` provenance clause. **153 of 153 open rows carry one** (`grep -c '· refs ' `). The backward direction at §4.2 is executed against `refs`, which is the de-facto `source:`.

**P2 — the clone's git history is SHALLOW, so git birth dates are mostly fiction.**
`.git/shallow` exists; history starts 2026-08-23; 340 commits, 7 distinct dates.

```
$ ls .git/shallow && git rev-list --count HEAD && git log --reverse --format='%ad' --date=short | head -1
.git/shallow
340
2026-08-23
```

`git log --diff-filter=A` — the command the brief's clause A1 names — returns **2026-08-23 for 835 of 951 objects (87.8 %)**, which is the graft boundary, not a birth. Per A1 those transitions are reported **`UNDATED (shallow graft)`**, never invented. Only **116 objects** have a trustworthy git birth date. Dated transitions in this report therefore come from **frontmatter and filename dates**, which are intact.

**P3 — the brief's own provenance locator does not resolve.** It cites *"verbatim from `FM-WAVE2-CONTRACTS-2026-08-28.md` §FM-C"*. No file of that name exists in the tree (`find . -name '*FM-WAVE2*'` → nothing). The real contract is the `NB2-CLOUD-FMC-funnel-census.md` path above. Content matches; only the locator is wrong.

**P4 — `docs/audits/` top-level count disagrees with the operator's disk.** Brief says 769; the clone has **773**. Reported both, per the standing clause. Intake 56 ✓, decisions 89 ✓, tasks 344 ✓, `BACKLOG.md` 67,883 B ✓ all match exactly.

---

## 1. METHOD, AND THE CLASS PRECEDENCE — stated so it is reproducible

### 1.1 The citation graph was built mechanically, in one pass

```bash
# 951 objects enumerated; 2,623 corpus files scanned in 14.6 s
git ls-files 'docs/intake/' 'docs/decisions/' 'docs/audits/'   # + conformance.html + codex/AGENTS.md
# tokens extracted per corpus file: dated stems, basenames, \bADR-0*(\d+)\b,
#   #(\d+), and intake[\s-]*#\s*(\d+)
```

### 1.2 IDENTIFIER-KEYED, never filename-keyed — and this is not optional

`scripts/consumer_at_landing.py:22-27` records the hub's own measured lesson: *"three of the four false-positive buckets were false because the corpus cites by IDENTIFIER (`ADR-<n>`, `intake #<n>`, `wf-<id>`) rather than by path… Any future reaper that keys on filenames alone would have proposed deleting 14 live documents and 420 live handoff files."*

**I reproduced that failure and then fixed it, and the delta is large:**

```
live intake docs                                  55
zero pool-citers under FILENAME keying only       19
zero pool-citers under IDENTIFIER keying          11   <-- the true orphan set
FALSE ORPHANS a filename-only census would emit    8   (42 % of its own orphan list)
```

Witness: intakes are cited overwhelmingly by id, not by name — `intake #18` ×145, `intake #25` ×142, `intake #16` ×101 (`grep -rhoE 'intake[ -]#[0-9]+' --include='*.md' .`).

### 1.3 The governance pool is the repo's own, COPIED not re-decided

`scripts/consumer_at_landing.py:122-124`:

```
POOL_DIRS       = tasks/ · docs/decisions/ · docs/intake/ · protocols/
POOL_ROOT_FILES = BACKLOG.md ARCHITECTURE.md CLAUDE.md LESSONS.md VISION.md CONTRIBUTING.md
DELIBERATELY EXCLUDED = JOURNAL.md, docs/handoffs/**, ecosystem/, scripts/, tests/,
                        .claude/, templates/, deploy/
```

Rationale quoted at `scripts/consumer_at_landing.py:35-38`: *"A mention in a session log or a machine baseline is a record that the file existed, not evidence that anything consumes it."* I additionally discount **generated blanket rosters** — `docs/{audits,intake,decisions}/README.md`, `docs/intake/manifest.json`, `BACKLOG.md`, `.claude/generated/*` — for the identical reason. Measured justification: `docs/audits/README.md` alone cites **789 of 951 objects**, so counting it as a consumer makes every object "consumed" by construction.

### 1.4 The terminal-state test, stated once and applied uniformly

| Consumer kind | Terminal when | Locator |
|---|---|---|
| `tasks/` row | `status:` ∈ {closed, retired, superseded} | `tasks/*.md` frontmatter |
| ADR | Status ∈ {Superseded, Retired, Rejected, Withdrawn}, or in `docs/decisions/archive/` | ADR status line |
| intake doc | `status:` ∈ {CONSUMED, SUPERSEDED, REJECTED} | `docs/intake/README.md:192-195` |
| audit / handoff / LESSONS / JOURNAL | **never terminal** — immutable or append-only, so the citation is permanent | CLAUDE.md §5 rules 1–3 |

That last row is the load-bearing one and it is ADR-100's own argument: an immutable citer can never be re-pointed, so an object it cites is **permanently cited** and can never satisfy "nothing else cites it."

### 1.5 Class precedence (highest wins)

`PROTECTED` → `CONSUMED-AND-ARCHIVABLE` → `CONSUMED-BY` → `ORPHAN`.
`PROTECTED` requires a **cited retention rule or ruling** — never a judgement call. Because PROTECTED absorbs an entire genre, §2.2 carries the **consumption sub-axis** underneath it, so nothing is hidden by the precedence.

---

## 2. HEADLINE COUNTS — THE BEFORE NUMBERS

### 2.1 Per directory × class (all 951 objects, 100 % classified)

```
directory                                     total  PROTECTED  CONSUMED-BY  CONS-&-ARCHIVABLE  ORPHAN
docs/audits/            (top level)             773        773            0                  0       0
docs/audits/<launch-contract subdirs>/           20         20            0                  0       0
docs/decisions/         (88 ADRs + README)       89         89            0                  0       0
docs/decisions/archive/                           2          2            0                  0       0
docs/intake/            (55 live + README
                          + manifest.json)       57          2           44                  0      11
docs/intake/archive/                              8          8            0                  0       0
ecosystem/conformance.html                        1          0            1                  0       0
codex/AGENTS.md                                   1          1            0                  0       0
-----------------------------------------------------------------------------------------------------
TOTAL                                           951        895           45                  0      11
UNCLASSIFIED                                                                                         0
```

Reconciliation witness (totals recomputed independently of the classifier):

```bash
git ls-files 'docs/audits/*.md'    | wc -l   # 793  (773 top level + 20 in subdirs)
git ls-files 'docs/decisions/*.md' | wc -l   # 91   (88 ADRs + README + 2 archived)
git ls-files 'docs/intake/'        | wc -l   # 65   (56 top level + 8 archive + manifest.json)
# 793 + 91 + 65 + conformance.html + codex/AGENTS.md = 951
```

### 2.2 The PROTECTED retention citations — one per genre, no special pleading

| Set | n | Retention authority (resolving locator) |
|---|---|---|
| `docs/audits/**` | 793 | **ADR-100 §1** *"Every accepted audit is kept, unbounded; audit files are never physically moved, rolled up, or compacted."* `docs/decisions/ADR-100-audit-retention-index-rule.md` |
| `docs/decisions/ADR-*.md` | 88 | **CLAUDE.md §5 rule 3** — ADRs are immutable; supersede with a new file. ADR-94 exempts only the status line. |
| `docs/decisions/archive/` | 2 | Already superseded and relocated; retained (ADR-40 DEPRECATED, ADR-52 superseded by ADR-53) |
| `docs/intake/archive/` | 8 | `docs/intake/README.md:224-230` — *"the doc **stays** (archived, not deleted) — rejections are recorded"* |
| The 3 generated indices + `manifest.json` | 4 | Under freshness gates `audit-index-freshness` / `intake-index-freshness` (CLAUDE.md §9) |
| `codex/AGENTS.md` | 1 | **`AGENTS.md:21`** — the precedence table names it by path as the third layer, *"its own subtree only"*. Explicitly **not** proposed for deletion, per the lane's hard constraint. |

### 2.3 CONSUMPTION SUB-AXIS — the numbers PROTECTED would otherwise hide

Measured with the repo's own detectors, run read-only with `python3` (no `--write-baseline`):

```bash
python3 scripts/consumer_at_landing.py     # exit 0
python3 scripts/funnel_coverage.py --report
```

```
consumer-at-landing/v2   (live @ fcc9485, pool_files=520, pool_resolved=True)
  corpus (recursive)                     792
  CONSUMED by a governance surface       233   (29.4 %)
  UNCONSUMED                             559   (70.6 %)
     of which landed  < 2026-08-27       525   grandfathered by ARM_DATE
     of which landed >= 2026-08-27        34   new debt
  committed baseline (c0ca7c2c)          540 unconsumed  ->  +19 growth, arithmetic reconciles

funnel-coverage/v1       (live @ fcc9485, corpus 772 = top-level *.md minus README)
  dispositioned                           78   ACTIONED 49 · FILED 25 · REJECTED 2 · SUPERSEDED 2
  pending                                  2
  UNCOVERED                              692   (89.6 %)
  committed baseline (52950fa9, 2026-08-23)  corpus 693, uncovered 613
```

**Two BEFORE facts FM-3 must carry:**

1. **`funnel_coverage` is NOT recursive** (corpus 772 vs the recursive 792) — the **20 launch-contract files under `docs/audits/*/` are outside its measurement entirely.** Disposition coverage of my census population is therefore **772/792 = 97.5 %**; the consumption axis is 792/792 = 100 %.
2. **Uncovered grew 613 → 692 (+79) in five days while `dispositioned` stayed frozen at 78.** Every audit landed since 2026-08-23 is undisposed. Per the 2026-08-17 architect standing ruling quoted at `scripts/funnel_coverage.py:14-20`, *"An undisposed audit is a defect, not a document."*

**The interpretation, stated so it cannot be misread:** for `docs/audits/`, unconsumed means **triage debt**, never deletability — ADR-100 §1 forecloses removal. For `docs/intake/`, ADR-100 §4 rules the opposite: *"The intake genre pays rent and is reviewed for removal; audits are never removed. The two are governed oppositely on purpose."* That asymmetry is why the archival worklist below is intake-only, and it is the repo's ruling, not my framing.

---

## 3. THE ARCHIVAL WORKLIST — decision-ready

### 3.1 Archivable **by the ruled mechanical predicate: ZERO**

The predicate is `docs/intake/README.md:228-231` — *"Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to `docs/intake/archive/`."*

```
live intake docs by status:   ACCEPTED 19 · READY 19 · SEED 10 · DRAFT 7   (= 55)
docs at a TERMINAL status still sitting at depth 1:  0
```

Witness: `for f in docs/intake/*.md; do awk '/^status:/{print $2;exit}' $f; done | sort | uniq -c`

And the converse holds too — **all 8 files in `docs/intake/archive/` are terminal** (6 CONSUMED, 1 REJECTED, 1 SUPERSEDED). **The archive relocation mechanism has zero backlog and zero mis-filings.** That is a clean bill of health, and it is the honest headline: *the archival step is not what is broken.*

### 3.2 Requires a STATUS RULING first — 3 candidates, each verified individually

These are live docs whose content has demonstrably flowed into a ratified ADR with **no open row remaining**. They are not archivable today because their `status:` is not terminal; **flipping it is an operator/architect act, not a mechanical one.** ADR-98's enum change is a ruling, so this list is a decision request, not a work order.

```
intake #19  2026-07-27-func-operator-design-input-night-shift-handoff-reform.md
   status        SEED         (SEED carries no standing authority -> no ACCEPTED protection)
   consumed by   ADR-82 (Accepted, ratified 2026-08-04) -- cited at ADR-82:110 "intake #19 §B(b),
                 rulings R1-R7, built under [#446]"
   rows          [#446] CLOSED  (the only one)
   own field     consumers: "morning-loop wave (A); intake #18 / [#435] ratification session (B)"
   VERDICT       CONSUMED-AND-ARCHIVABLE on the funnel reading. Strongest candidate of the three.

intake #26  2026-08-06-func-parallel-execution-system.md
   status        ACCEPTED · disposition: active · decided-by: operator GO on SESSION PLAN v2 (2026-08-06)
   consumed by   ADR-110 -- header line 7: "**Intake:** #26 (docs/intake/2026-08-06-...) -- ACCEPTED"
   rows          [#505] CLOSED  (the only one)
   BLOCKER       README.md:228-231 -- "ACCEPTED is deliberately NOT in [the terminal set], a standing
                 decision stays live". Needs ACCEPTED -> CONSUMED, which is a ruling.

intake #28  2026-08-08-func-skills-tier-adoption-and-hub-finish-line.md
   status        ACCEPTED · disposition: active · decided-by: operator ruling, batch-4 planning GO
   consumed by   ADR-112 -- line 8: "**Intake:** #28 (§A)"; §A quoted verbatim at ADR-112:66
   rows          none
   BLOCKER       same ACCEPTED protection as #26.
   CAUTION       ADR-112:87 says "fourteen candidates in intake #28 §C become actionable" -- §C is a
                 live candidate pool, not spent content. Rule on §C before flipping the doc.
```

### 3.3 REJECTED as a candidate after opening the file — recorded so FM-3 does not re-derive it

```
intake #42  2026-08-23-tech-generated-artifact-currency.md   status DRAFT
   The graph flagged it archivable (ADR-115 consumer, zero rows). Reading ADR-115 refutes it:
   §6 "the precedence rule this case forces (intake #42's SECOND open question)" and
   §7 "the status token (intake #42's THIRD open question)" -- ADR-115 answered SOME questions,
   not the document. README.md:242-257 governs exactly this: a partially-ruled intake "keeps its
   pre-ratification status -- SEED or DRAFT -- and gains a pointer note."
   VERDICT: correctly DRAFT. NOT archivable. The graph was wrong and the file settled it.
```

This is the one case where the census opened a file because the graph was ambiguous, and it changed the answer. Recorded because a census that never overturns its own graph has not checked it.

---

## 4. THE ORPHAN LIST — BOTH DIRECTIONS

### 4.1 FORWARD — 11 orphan intake docs (each re-tested by a second method)

Second method: `git grep -lF <full-stem>` **and** `git grep -lE 'intake[ -]*#<id>'` across the **whole tree**, not just the pool. Every hit for all 11 landed in `docs/audits/`, `JOURNAL.md`, `docs/handoffs/`, `ecosystem/`, `scripts/`, `tests/`, or the two generated intake indices — **all outside `POOL_DIRS` by construction.** No orphan survived contact with the second method as a false positive.

```
id  file                                                     status  born(frontmatter)  second-method result
 4  2026-07-07-arc5-pilot-followup-seeds.md                   SEED    2026-07-07   audits+JOURNAL+indices only
 5  2026-07-07-changelog-review-seeds.md                      SEED    2026-07-07   audits+JOURNAL+indices only
 7  2026-07-08-func-ai-council-interface.md                   SEED    2026-07-08   audits + scripts/gen_dashboard.py
 8  2026-07-08-func-night-routines-suite.md                   SEED    2026-07-08   audits + indices only
15  2026-07-16-satellite-onboarding-prompts.md                READY   2026-07-16   audits + handoffs + JOURNAL
43  2026-08-24-tech-ruling-register-landing-gap.md            READY   2026-08-24   2 audits + indices
44  2026-08-24-tech-disposition-register-schema.md            READY   2026-08-24   2 audits + indices
46  2026-08-24-tech-contract-integrity-gate.md                READY   2026-08-24   2 audits + indices
47  2026-08-24-tech-supplement-probe-fill-state-defect.md     READY   2026-08-24   1 audit  + indices
51  2026-08-26-tech-provider-capacity-anthropic-compatible.md READY   2026-08-26   *** GENERATED INDICES ONLY ***
61  2026-08-28-tech-handoff-engine-deployable-carrier.md      READY   2026-08-28   JOURNAL + indices only
```

**Read these correctly — they split into three kinds, and only one is debt:**

- **`READY` = "operator-approved, waiting on its consumer"** (`docs/intake/README.md:211-213`). A READY orphan is a doc **correctly parked**, not waste. Ids 43/44/46/47/61 are ≤ 4 days old; **#61 was born today**. Six of the eleven are in this class.
- **`SEED` ×4 (ids 4, 5, 7, 8), all from 2026-07-07/08 — 52 days unconsumed.** These are the real forward debt. Cross-check: ids 4 and 15 already appear in a **prior** orphan census, `docs/audits/2026-08-17-census-nb7-orphan-census.md` — they were flagged 11 days ago and nothing consumed them since.
- **`intake #51` is the hardest single object in the census.** Its only mentions anywhere in 2,623 tracked files are `docs/intake/README.md` and `docs/intake/manifest.json` — the two files that list it *because it exists*. Nothing in the repo has ever referred to its content.

Also recorded: **`ADR-83-protocols-archive-convention.md` is the one ADR with zero governance-pool citers** (43 citers overall, every one in `docs/audits/`, `JOURNAL.md` or `.claude/`). It stays PROTECTED under CLAUDE.md §5 rule 3 — an ADR is not deletable — but it is the decisions genre's single consumption orphan and is named here rather than left inside a 895-object PROTECTED bucket.

### 4.2 BACKWARD — every OPEN row's provenance, resolved

Executed against the `· refs …` clause (see P1).

```
OPEN rows (tasks/ frontmatter status: open)          153
rows carrying a refs clause                          153   (100 %)
rows with >= 1 RESOLVING ref                         152
rows with ZERO resolving ref  = BACKWARD ORPHANS       1
rows carrying >= 1 DANGLING ref                       24
ref tokens: 746 resolved / 27 dangling / 773 total  ->  96.5 % resolve rate
```

**The single backward orphan:**

```
[#518]  tasks/518-audit-py-git-runs-unscrubbed-and-undecoded-at-one.md
        refs clause reads, in full:  "N4-F1/F6/F5/F12"
        Those are FINDING ids inside an audit -- the audit itself is never named.
        Resolved by hand: the ids live in docs/audits/2026-08-09-technical-night-batch-findings-index.md
        and docs/audits/2026-08-09-technical-consolidation-report.md.
        The row's SUBJECT (scripts/audit.py::_git) exists; only its PROVENANCE fails to resolve.
        Honest verdict: orphan in provenance, not in substance. One locator would close it.
```

**23 dangling row-ids on 23 open rows** — references to backlog ids that no longer exist as rows anywhere. Verified by a second method (`grep "\[#N\]" BACKLOG.md` + `grep -rl '^id: "\[#N\]"' tasks/`); all 23 return **0 rows in `tasks/`**:

```
#105 (on #112,#185) · #256 (#340,#528) · #384 (#392,#393) · #124,#131 (#145) · #168 (#170)
#238 (#267) · #86 (#271) · #211 (#277) · #164 (#293) · #260 (#340) · #336 (#342) · #337 (#343)
#306 (#345) · #381 (#388) · #398 (#402) · #222 (#403) · #111,#312 (#427) · #255 (#428)
#121 (#430) · #333 (#431) · #436 (#438)
```

Four of them (#238, #381, #398, #436) still appear as *prose* inside `BACKLOG.md` but exist as no row — consistent with KILL-removal under the filing-backpressure mechanism, not with an error. They are **history, cited as if live**.

**1 dangling path on an open row:**

```
[#509] refs  scripts/dispatch/Invoke-Dispatch.ps1
       ls scripts/dispatch/ -> No such file or directory
       find . -name 'Invoke-Dispatch*' -not -path './.git/*' -> no match
```

**8 open rows sit on an AMBIGUOUS join key.** A bare `#N` is valid in **two id namespaces** — task ids and intake ids (both start at 1). These 8 cite an `#N` that is *not* a task id but *is* an intake id, so which object is meant cannot be decided from the text:

```
[#146]->#11   [#170]->#8   [#210]->#5   [#340]->#21
[#341]->#30   [#510]->#2   [#561]->#32  [#572]->#37
```

Counting conservatively, **31 provenance tokens on open rows (23 dangling + 8 ambiguous) do not resolve cleanly** — 4.0 % of 773.

---

## 5. UNCLASSIFIED = 0 — and the exceptions, named individually

Every one of the 951 objects carries a class. Six objects are exceptions to the ordinary genre rule and each is explained rather than bucketed silently:

1. **`ecosystem/conformance.html`** — the conformance HTML dashboard, censused **like any other artifact** per the hard constraint. It is a **committed-generated** artifact (`scripts/gen_dashboard.py:22`, ADR-80 committed-generated zone, operator addendum 2026-08-19). Governance-pool consumers: **`tasks/586-…md` ([#586], status `open`)** and **`ARCHITECTURE.md`**. → **CONSUMED-BY [#586] · ARCHITECTURE.md.** Not PROTECTED — a regenerable artifact earns no retention ruling, and I decline to invent one for it.
2. **`codex/AGENTS.md`** — **PROTECTED**, cited to `AGENTS.md:21` (precedence table, third layer, *"its own subtree only"*). Not proposed for deletion. The `codex/` directory holds this one file and nothing else.
3. **`docs/intake/manifest.json`** — the only non-`.md` object inside the three directories. Generated by `scripts/gen_intake_tree.py`, `direction: derived-from`, `source_sha256` pinned to `docs/intake/README.md`. → PROTECTED as a gated generated artifact.
4. **The three `README.md` index files** — PROTECTED as generated navigation under freshness gates, and simultaneously **discounted as citers** (§1.3). They are objects of the census and non-evidence within it; both roles are stated so neither is smuggled.
5. **`docs/decisions/archive/` (2 files)** — ADR-40 (`DEPRECATED 2026-05-23`) and ADR-52 (`~~Accepted~~ Superseded by ADR-53`). Terminal and already relocated; PROTECTED, no action.
6. **The 20 files under `docs/audits/*/launch-contracts/`** — real objects, PROTECTED under ADR-100 like any audit, but **invisible to `funnel_coverage` because that detector is non-recursive**. Counted here; excluded there. That gap is the 97.5 % coverage fraction at §2.3.

---

## 6. DEFECTS FOUND IN PASSING — each reproduced, none fixed (read-only lane)

**D1 — `docs/intake/README.md` mis-renders 6 of 55 live intakes, and the freshness gate cannot see it.**

The generated index carries an off-enum `### OTHER (6)` group (`docs/intake/README.md:82`) whose six entries render `[MISSING-ID]` (lines 84-89) — although all six files carry a valid `intake-id:`. Consequence: the index says `### READY (13)` while disk has **19 READY**.

Root cause reproduced by running the generator's own parser:

```bash
python3 -c "import sys;sys.path.insert(0,'scripts');import gen_intake_index as g;
            print(g._parse_frontmatter(open('docs/intake/2026-08-27-tech-append-only-rotation-execution.md').read()))"
# -> {}
```

```
yaml.scanner.ScannerError: found character '`' that cannot start any token
  line 5, column 12:   consumers: `docs/audits/2026-08-27-technical-...
```

All six fail identically — an **unquoted backtick opening a YAML scalar** on the `consumers:` line, always line 5 column 12. `gen_intake_index._parse_frontmatter` returns `{}` on malformed YAML by design (its docstring: *"the doc surfaces in OTHER instead"*), so status and id are both lost.

Affected: ids **56, 57, 58, 59, 60, 61**. Note also that `consumers:` is **not in the ADR-98 companion-field schema** (`docs/intake/README.md:146-156` names `consumed-by`, `decided-by`, `disposition`, `trigger`, `review-date`, `superseded-by`, `reason`).

**The gate-blindness is the real finding:** `intake-index-freshness` is a regen-and-diff hook. The generator reproduces its own wrong output byte-for-byte, so **the gate passes and the index is fresh and wrong.** A freshness gate cannot detect a generator bug. (Gate verdict itself: **MEASUREMENT-OWED-LOCAL**.)

**D2 — `intake-id: 14` is assigned to three different files.**

```
docs/intake/2026-07-12-siem-requirements-ruled-pack.md                    (ACCEPTED, live)
docs/intake/archive/2026-07-13-siem-fleet-management-requirements.md      (CONSUMED)
docs/intake/archive/2026-07-13-siem-fleet-management-requirements-codex.md (CONSUMED)
```

Every `intake #14` citation in the corpus is therefore ambiguous — and `intake #14` is the join key `consumer_at_landing` and this census both rely on. Otherwise the id space is clean: **1..61 present, no gaps, no other duplicate.**

**D3 — ADR numbering: 27 numbers absent.** ADRs 1–26 and 44 have no file (`present: 88, range 27..115`). Not asserted as loss — ADR-49/65 condense-to-git is live doctrine — but the gap is unexplained by anything in `docs/decisions/README.md` and is recorded so it is not rediscovered.

**D4 — ADR-61 uses a different status schema.** `docs/decisions/ADR-61-git-worktree-parallel-sessions.md` carries YAML frontmatter (`status: Accepted 2026-05-28`) rather than the `- **Status:**` prose line all 87 siblings use. Status is Accepted; only the shape is off-schema.

**Clean bills of health, recorded because a census that reports only defects is also biased:** all 19 ACCEPTED intakes carry the required `decided-by:` **and** `disposition:`; all 4 with `disposition: deferred` carry the required `trigger:` (`docs/intake/README.md:151-153`); all 8 archived intakes are terminal; the archive relocation backlog is zero.

---

## 7. SELF-AUDIT — applying the brief's own failure mode to this report

**Class tally:** `PROTECTED 895 · CONSUMED-BY 45 · CONSUMED-AND-ARCHIVABLE 0 · ORPHAN 11 · UNCLASSIFIED 0`.

**ORPHAN is NOT the plurality** — 11 of 951 = **1.2 %**. The brief's stated failure mode (*"a census routing most objects to ORPHAN without evidence has not censused"*) did **not** occur. All 11 were nonetheless re-tested by a second, independent search method (§4.1) and all 11 survived.

**But the honest inversion, said plainly rather than buried:** the plurality class is **PROTECTED at 94.1 %**, and that is a different way for a census to look complete while saying nothing. Three things keep it from being one:

1. Every PROTECTED assignment cites a **specific retention ruling** (§2.2), not a judgement — and 793 of those 895 rest on one ruling, **ADR-100 §1**, quoted verbatim. If that ruling is wrong the census is wrong in one identifiable place, which is the property a census should have.
2. The **consumption sub-axis is published in full underneath it** (§2.3). On that axis **unconsumed IS the plurality — 559/792 = 70.6 %** for audits. Nothing is hidden by the precedence; the two axes are simply not the same question, and ADR-100 §4 is the repo's own ruling that they must not be collapsed.
3. The classes that drive **action** — the archival worklist and both orphan lists — are exactly the ones where PROTECTED does *not* apply, and they are the ones I opened files to verify.

**Where I was wrong during this lane, recorded rather than smoothed over:**

- My first pass keyed on **filenames** and produced **19 orphan intakes**. Identifier keying cut it to **11** — an **8-object, 42 % false-orphan rate** in my own draft output. Had I stood behind pass 1, FM-3 would have archived eight live documents. The repo had already recorded this exact trap (`consumer_at_landing.py:22-27`) and I walked into it anyway.
- My first pass flagged **intake #42 as archivable**. Opening ADR-115 refuted it (§3.3). One of four graph-derived candidates — a **25 % error rate on the highest-consequence list in this report** — which is why §3.2 ships three verified candidates rather than four convenient ones, and why every one names the exact line that proves it.
- My first backward pass reported **61 rows with dangling refs**. Directory-aware and intake-id-aware resolution cut it to **24**. Same class of error, third time.

**Limits of this census, stated rather than left for FM-3 to discover:**

- Consumption is **substring presence in the governance pool**, exactly as `consumer_at_landing` defines it. Its own honest limit applies unchanged: *"A row that names an artifact only to say it is obsolete counts as a citer."* This census inherits that weakness; it does not repair it.
- The **terminal-state test is applied to consumers, not validated against them.** I did not verify that a `closed` row was actually done — only that its frontmatter says `closed`.
- **Dated transitions are frontmatter-derived, not git-derived** (P2). Any statement here about *when* an object changed state comes from what the file says about itself.
- I read **~35 files end to end** out of 951. The rest were classified from the mechanical graph. That is the method the brief prescribed, and the two overturns above are the measured cost of it.

---

## 8. MEASUREMENT-OWED-LOCAL

The container's `uv` is 0.8.17 against `required-version = "==0.11.19"`, so no `uv run --locked` gate could start. These claims are **owed**, never estimated:

```
MEASUREMENT-OWED-LOCAL  intake-index-freshness  -- does gen_intake_index.py --check PASS while
                        README.md carries "### OTHER (6)"?  (D1 predicts PASS; that is the finding)
MEASUREMENT-OWED-LOCAL  audit-index-freshness / gen_audit_index.py --check
MEASUREMENT-OWED-LOCAL  scripts/audit.py health · audit.py checks (the roster of live checks)
MEASUREMENT-OWED-LOCAL  the pytest suite -- including tests/test_funnel_coverage.py and
                        tests/test_gen_dashboard.py, which pin two detectors this census leans on
MEASUREMENT-OWED-LOCAL  any pre-commit / commit-msg / pre-push hook verdict
```

**Not owed — obtained.** `consumer_at_landing.py` and `funnel_coverage.py` are stdlib-plus-pyyaml and read-only absent `--write-baseline`; both ran under bare `python3` and their live numbers at §2.3 are measurements, not estimates.

---

## 9. REPRODUCTION — every command, and the zero-write proof

```bash
# revision under census
git rev-parse HEAD                      # fcc9485567f81814d24b84fe2db5ceff23b743ee

# object enumeration (951)
git ls-files 'docs/audits/*.md' | wc -l         # 793
git ls-files 'docs/decisions/*.md' | wc -l      # 91
git ls-files 'docs/intake/' | wc -l             # 65
# + ecosystem/conformance.html + codex/AGENTS.md

# forward direction, audits -- the repo's own detectors, read-only
python3 scripts/consumer_at_landing.py                # 19 growth lines, exit 0
python3 scripts/funnel_coverage.py --report           # 78 / 2 / 692 of 772

# forward direction, intake -- identifier-keyed
for f in docs/intake/*.md; do awk '/^status:/{print $2;exit}' "$f"; done | sort | uniq -c
grep -rhoE 'intake[ -]#[0-9]+' --include='*.md' . | sort | uniq -c | sort -rn

# backward direction, open rows
for f in tasks/*.md; do awk -F': ' '/^status:/{print $2;exit}' "$f"; done | sort | uniq -c
#   open 153 · closed 130 · deferred 55 · retired 4 · superseded 1  = 344
grep -c '· refs ' tasks/*.md            # every open row carries one

# D1 reproduction
python3 -c "import sys;sys.path.insert(0,'scripts');import gen_intake_index as g;\
print(g._parse_frontmatter(open('docs/intake/2026-08-27-tech-append-only-rotation-execution.md').read()))"

# D2 reproduction
grep -h '^intake-id:' docs/intake/*.md docs/intake/archive/*.md | sort -n | uniq -d
```

**Zero-write proof, run after all analysis:**

```
$ git status --porcelain
                      <- empty: no file created, modified, staged, deleted or renamed
$ git rev-parse HEAD
fcc9485567f81814d24b84fe2db5ceff23b743ee   <- unchanged from session start
```

Analysis scripts and JSON intermediates were written **outside the repository**, to the session scratchpad (`/tmp/claude-0/…/scratchpad/`). Nothing under `/home/user/dev-knowledge` was touched. No branch, tag, commit, stash or `--write-baseline` invocation occurred.

---

**END — NB2 · CLOUD FM-C.** One artifact. 951 objects, 100 % classified, UNCLASSIFIED 0. Four premise defects, four repo defects, three verified archival candidates, twelve orphans across both directions.