# Funnel groom — READ-ONLY proposal sheet (2026-09-05)

**Consumers:** `ADR-111` (the decision funnel — every bundle below is a proposal into its
OWNED / DISCHARGED / CANDIDATE / REJECTED triage, and no bundle births a row) · the rows each
bundle names: `[#613]` `[#564]` `[#242]` `[#487]` `[#626]` `[#418]` `[#552]` `[#585]` `[#586]` ·
`ADR-110` and `ADR-84` (the two amendment bundles) · intake `#43`, intake `#47`, intake `#51` ·
`protocols/STANDING_RULINGS.md` section AD (the batch-G candidate register this sheet dedupes).

**Class:** technical, READ-ONLY reconnaissance. **Zero rows closed, zero files archived, zero
deletions.** Every bundle is a proposal carrying a witness and a copy-ready command; nothing here
was executed.

---

## 0 · THE PINNED SHA — every count and every quoted output below is measured at it

```
HEAD              78daf4006c6d9231bb0f7dbfefbdfb911a659ce5
resolved by       git rev-parse HEAD
branch at boot    (detached from refs/heads/main)
lane branch       docs/funnel-groom-2026-09-05
git status        clean at boot; clean apart from this file at commit
```

---

## 1 · TOOLCHAIN — what actually ran, and the fallback that was NOT taken

The contract's clause 4 offers two paths: `uv run --locked` at the repo's exact pin, or a
`python3` fallback that must be declared. **Neither was available as shipped, and the resolution
was a third thing, so it is stated in full rather than summarised.**

```
container uv          0.8.17
repo pin              required-version = "==0.11.19"   (pyproject.toml:25)
uv run --locked ...   REFUSED, verbatim:
    error: Required uv version `==0.11.19` does not match the running version `0.8.17`.

container python3     3.11.15
repo floor            requires-python = ">=3.12"       (pyproject.toml:15)
python3 scripts/...   REFUSED, verbatim (funnel_lifecycle.py, first detector attempted):
    ModuleNotFoundError: No module named 'click'
```

So the declared fallback could not run a single detector either: the system interpreter is below
the repo's Python floor and carries none of the declared dependencies.

**What was done instead, and it changes no repo file.** `uv==0.11.19` — the repo's own exact pin,
not a newer one — was installed into a throwaway venv in the container scratchpad
(`/tmp/.../scratchpad/uvenv`), outside the repository. `uv sync --locked` then rebuilt the declared
environment. No pin was bumped, no lockfile touched, `.venv/` is gitignored (`.gitignore:11`).

```
DETECTORS RUN UNDER `uv run --locked` AT THE PINNED uv 0.11.19:   ALL OF THEM
DETECTORS RUN UNDER THE python3 FALLBACK:                          NONE
```

**One side-effect write, disclosed rather than discovered later.** `propose_closures.py` writes its
own artifact by design; this run produced `logs/PROPOSALS-2026-09-05-01.md`. It is gitignored
(`.gitignore:26` — `logs/PROPOSALS-*.md`), so `git status` stays clean and nothing outside this
deliverable enters the commit. The file's own banner calls itself *"Gitignored, ephemeral"*.

**Survey listings** (intake orphans, task path resolution, citation witnesses, near-duplicate
pairs) were derived with ad-hoc read-only Python in the scratchpad. **No new detector was written
into the repo**, and no number a detector already computes was hand-derived — where a detector has
the number, the detector's own output is quoted below.

---

## 2 · DETECTOR OUTPUTS — verbatim, at `78daf400`

### 2.1 `funnel_lifecycle.py --report` (legs a1 / a2 / b / c / d)

```
detector           funnel-lifecycle/v1
intakes            57 live / 12 archived
live ADRs          89
rows               364 (364 on/after 2026-08-27)
READY threshold    30  (protocols/FUNNEL_LIFECYCLE.md:316)

a1 terminal intake not archived        0
a2 ACCEPTED, all named rows terminal   0
b  terminal ADR not archived           0
c  post-cutoff row provenance          5
    [#35] tasks/35-fix-the-self-owned-low-severity-cleanups.md -- landed 2026-08-31 (on/after 2026-08-27) and no token in its provenance clause resolves: 'coherence-audit'
    [#71] tasks/71-reconcile-environment-md-s-claude-directory-tree.md -- landed 2026-08-31 (on/after 2026-08-27) and no token in its provenance clause resolves: 'G6 process-hardening sweep'
    [#123] tasks/123-routine-observability-convention-value-review.md -- landed 2026-08-31 (on/after 2026-08-27) and no token in its provenance clause resolves: '#85, #14, #113, audit C matrix R7'
    [#437] tasks/437-closes-re-quoting-defect-backtick-strip-before-t.md -- landed 2026-08-31 (on/after 2026-08-27) and no token in its provenance clause resolves: 'propose_closures.py:51,80, validate_git_backlog.py:87, `12e6b45b`, `096364ac`'
    [#518] tasks/518-audit-py-git-runs-unscrubbed-and-undecoded-at-one.md -- landed 2026-08-31 (on/after 2026-08-27) and no token in its provenance clause resolves: 'N4-F1/F6/F5/F12'
d  READY past threshold                0
```

Exit status 1 (leg c non-empty). **Legs a1, a2, b and d are all clean at this SHA** — the intake
and ADR archival classes carry no terminal-object debt the detector can see. Leg c's five rows are
in the appendix, §A5.

### 2.2 `validate_git_backlog.py` (rows closed by a SHA but still present)

```
validate_git_backlog: OK — no closed-but-present drift (direction (a) STRONG, full history)
```

### 2.3 `propose_closures.py` (rows whose Done-when is witnessed on `main`)

```
propose_closures: 0 strong, 0 weak over 377 commit(s) -> PROPOSALS-2026-09-05-01.md (weak suppressed: cold start)
```

And from the artifact it wrote:

```
since_commit: (none — cold start / no prior baseline)
window_commits: 377

> _WEAK detection suppressed: no prior session baseline (cold start), so
> a file-touch window would span the whole history and over-surface._
> _STRONG (closing-commit) detection is precise regardless and still ran._

**No closures detected** in this window.
```

**Read this result correctly.** The zero is not evidence that no row is closable — it is evidence
that the STRONG leg found no `closes [#N]` commit and the WEAK leg did not run. Bundle **B6**
explains why the WEAK leg can never run on a clone that is not the operator's machine, and bundle
**B1** is a closable row this detector is structurally unable to see.

### 2.4 `boot_frontier.py` (serialize-group holds)

```
boot_frontier: 5 proposed (width<=6, ledger<=5) -- PROPOSAL ONLY; requires an explicit operator GO before any lane dispatches (AUT-R1 Phase 4: adjudication stays a human act)
  [#581] P1 · Backlog vitals — three flow instruments, a committed digest, and what-is-unblocked-now (packet ARC-C)
  [#519] P1 · The close path is two edits, and nothing makes a half-done close visible
  [#359] P1 · PHANTOM ENFORCEMENT — `protocols/HANDOFF_PROCESS.md` §14a FILE-BOUNDARY claims a mechanism that does not exist.
  [#528] P1 · Lane-latency — the full suite multiplied by per-lane + per-merge runs is the real batch cost
  [#625] P1 · The rule-adherence eval corpus — a FRESH corpus, because neither fold target can carry it
  held back (serialize-group disjointness): #587, #588, #580, #582, #277, #357, #362, #389, #418, #430, #448, #451, #454, #457, #477, #533, #552, #597, #601, #605, #624, #383, #387, #401, #440, #523, #561, #567, #572, #574, #604, #390, #404, #422, #511, #520, #522, #599, #600, #602, #570, #575, #576, #618, #619, #623, #210, #342, #343, #361, #365, #392, #393, #403, #470, #485, #598, #388, #402, #420, #526, #603
  more unblocked work exists beyond the ledger bound -- not endless by design
```

`--frontier` reports `159 unblocked row(s) in 170 open`.

### 2.5 `validate_doc_rot.py` — the doc-rot module (name resolved on disk, 2026-09-05)

```
validate_doc_rot: 75 doc-rot locus(es) past threshold:
```

Class tally over those 75 loci:

```
backlog-row-length   70
backlog-accretion     3
section-history       1
grooming-cadence      1
```

The two non-BACKLOG-row loci, verbatim:

```
    grooming-cadence  BACKLOG#grooming-cadence  ->  last groom 2026-07-30, 37d ago (> 21d cadence, ADR-41)
     section-history  protocols/HANDOFF_PROCESS.md#section-history  ->  12 entries (>= 12; condense to git per ADR-49/65)
```

**The `grooming-cadence` locus is the reason this arc exists**, and adjudicating this sheet is what
clears it.

### 2.6 Supporting detectors (run to resolve item 006-A's audit and ADR legs)

`funnel_coverage.py`:

```
detector      funnel-coverage/v1
corpus N      879   (docs/audits/*.md, excluding README.md)
ledgers       1   2026-08-17-technical-audit-disposition-ledger.md
dispositioned 78
pending       2
uncovered     726
malformed     0
dangling      0

by term:
  ACTIONED    49
  FILED       25
  REJECTED    2
  SUPERSEDED  2
```

`validate_adr_status.py`, non-grammar findings plus its summary line:

```
adr-status: DEFECT(S)
  [WARN] coherence: ADR-45 -- header 'Explored, not adopted' != README index 'Superseded'
  [WARN] coherence: ADR-46 -- header 'Partially superseded' != README index 'Accepted'
  [WARN] coherence: ADR-47 -- header 'Partially superseded' != README index 'Accepted'
  [WARN] duplicate-id: ADR-51 -- 2 files claim this number: ADR-51-amendment-2026-07-05-llm-first-canonical-docs.md, ADR-51-architecture-doc-convention.md -- index coherence is ambiguous for all of them
  [WARN] duplicate-id: ADR-70 -- 2 files claim this number: ADR-70-amendment-2026-07-07-fable-xl-tier.md, ADR-70-three-tier-process-automation.md -- index coherence is ambiguous for all of them
  [WARN] wrapped-value: ADR-67-ai-council-process-operationalization.md:5 -- value continues onto the next physical line -- a line-oriented reader truncates it silently
[adr-status] 89 status field(s); defects: coherence=3, duplicate-id=2, grammar=47, wrapped-value=1 -- canonical grammar G1
```

`batch_manifest.py` prints nothing and exits 0 — **zero open batches at this SHA.**

---

## 3 · THE DECISION BUNDLES — nine, each with a witness and a command

None of these was executed. Each command is copy-ready from the primary checkout.

---

### B1 · CLOSE `[#613]` — the routing carrier landed and its gate is armed

**Verb:** CLOSE. **Class:** tasks. **Confidence:** high — all three Done-when legs resolve.

**The clause, from `tasks/613-in-repo-routing-table-agreement-check.md`:**
*"Done when: the operator selects a path; the authoritative table exists there; a check asserts L0
agreement and FAILs on divergence."*

**Witness, leg by leg, each locator opened:**

```
leg 1  path selected        candidate (a) `ecosystem/routing-table.yaml` was taken. The row says
                            "no file is created until it is [selected]"; the file EXISTS at HEAD.
leg 2  table exists         ecosystem/routing-table.yaml, present and tracked.
                            Landed on merge 1e064921681873ff824d116ff9e167258e74647d
                            ("Merge branch 'feat/g0-routing-carrier'"), batch G lane G0.
leg 3  check FAILs on       scripts/audit_checks/check_routing_agreement.py:64-67
       divergence               if state == "diverge": return [Finding(CHECK_NAME, "fail", ...)]
                            registered at scripts/audit.py:4925
                                _tier(TIER_SHIP, check_routing_agreement),
                            tests at tests/test_routing_agreement.py
                            live run on this host:
                                l0-absent: the L0 derived copy ~/.claude/ROUTING.md is absent on
                                this host, so agreement could not be computed for 4 role(s) — a
                                reported gap, not a pass (Z-G4)
                            i.e. WARN on absence (Z-G4-conformant), FAIL on divergence. As ruled.
```

**Why no detector proposed this.** `propose_closures`'s STRONG leg keys on a `closes [#N]` commit
subject; G0's merge subject names the carrier, not the row. Its WEAK leg was suppressed (§2.3, and
see B6). The batch-G close packet's §3 adjudicated eight arcs and did not include `[#613]`.

**Command:**

```bash
# from the primary checkout, on a branch
uv run --locked python scripts/audit.py health          # confirm green before the flip
/review-closures                                        # ADR-70 Tier-1: the operator declares
# then, as the declaration:
#   tasks/613-in-repo-routing-table-agreement-check.md  status: open -> closed
uv run --locked python scripts/gen_task_tree.py --emit-source
uv run --locked python scripts/gen_task_tree.py --check
git commit -m "chore(backlog): closes [#613] -- routing carrier landed at 1e064921, agreement check armed TIER_SHIP"
```

---

### B2 · AMEND-ADR `ADR-110` — "no batch above 3 has run" is false at three sites

**Verb:** AMEND-ADR. **Class:** ADRs. **Confidence:** high — the measured premise moved and the
falsifying artifacts are in-tree.

**The claim, quoted from `docs/decisions/ADR-110-parallel-execution-batch-protocol.md`:**

```
:150  - **§2's 4–10 range is a design target, not a measured ceiling.** No batch above 3 has run. The
:197  measured ceiling* — is likewise unchanged: no batch above 3 has run, and the artifacts are
:290  but no batch above 3 has run. Batch 2 is its first live exercise, and is also the first test
```

`:150` sits in §7 Honest limits; `:197` in the 2026-08-07 amendment; `:290` in that amendment's own
honest limits. All three are load-bearing: §2's 4–10 envelope is read as *unproven* because of them.

**Witness — batches above 3 have run, repeatedly, and their manifests say so:**

```
docs/audits/2026-08-28-technical-batch-2-manifest.md:5
    shape: ADR-110 — ONE pre-authorized mission -> 7 local file-disjoint lanes + 6 cloud read-only -> TWO integrator queues
docs/audits/2026-08-31-technical-batch-e-manifest.md:4
    shape: ADR-110 — DERIVE -> architect's cut -> FREEZE -> DISPATCH; 7 cloud read-only censuses (executed) + 15 committing lanes + 1 codespace admission probe (executed, RED)
docs/audits/2026-09-01-technical-batch-f-manifest.md:4
    shape: ADR-110 — DERIVE -> architect's cut -> FREEZE -> DISPATCH; 7 committing lanes (1 codespace ATTENDED + 6 local)
docs/audits/2026-09-02-technical-batch-g-manifest.md:4
    shape: ADR-110 — ...; 9 committing lanes (1 codespace parity witness + 8 local)
```

And batch G's close packet witnesses the nine to completion, not merely to dispatch:

```
docs/audits/2026-09-02-technical-batch-g-close-packet.md:21
    ## 1 · THE QUEUE — nine lanes, all merged, all anchored
```

**What the amendment should record, and it is not simply "the number is bigger".** The honest limit
this ADR wrote was *"the 4–10 range is unproven"*. That limit is now **discharged at width 9 and
exceeded at width 15**, and the batch-G packet supplies the datapoint the ADR actually wanted:
nine lanes merged, 99 commits, 32 merges, **one row status changed**. The width envelope is proven;
the *return* on width is the open question, and it belongs in the amended limit.

**Command:**

```bash
# ADRs are immutable: supersede by in-file amendment marker (CLAUDE.md §5 rule 3), never edit :150/:197/:290
$EDITOR docs/decisions/ADR-110-parallel-execution-batch-protocol.md
#   append: "## Amendment — <date>: the 4–10 envelope is exercised; the honest limit is re-stated"
#   citing docs/audits/2026-08-31-technical-batch-e-manifest.md (15),
#          docs/audits/2026-09-02-technical-batch-g-manifest.md (9) and its close packet
uv run --locked python scripts/validate_adr_status.py
git commit -m "docs(adr-110): amend -- the 'no batch above 3' limit is discharged; widths 7/9/15 measured"
```

---

### B3 · AMEND-ADR `ADR-84` — "date-unique filenames" is not "run-unique", and it collided twice

**Verb:** AMEND-ADR. **Class:** ADRs. **Confidence:** high — two independent measurements.

**The claim, quoted from `docs/decisions/ADR-84-automation-writer-isolation.md`:**
*"**Fact 2 — outputs are append-only with date-unique filenames.** Each run writes a new dated
file; nothing is removed. Because filenames are date-unique and there is a single writer per
stream, additive merges never collide, so no merge-cleanup step is needed."*

**Witness 1 — the writer runs many times a day, `[#418]`, which already refs ADR-84:**
*"the writer branch carries up to 10 commits on a single day (2026-07-10) and 0 on many others
(none since 2026-07-16), so 'the daily baseline' is neither daily nor singular… its once-per-day
throttle reads `logs/FLEET-HEALTH.md`, which is gitignored and therefore PER-WORKING-TREE — so
every worktree and clone independently believes the baseline is stale and re-runs it."*

**Witness 2 — an adjacent stream measured the collision, `protocols/STANDING_RULINGS.md` section
AD, candidate (k):** *"`logs/PROPOSALS-2026-09-02.md` and `logs/2026-09/PROPOSALS-2026-09-02.md`
are both 208,062 bytes, differ in content, and record `head_commit` `040dec74` / window 4763 versus
`55fecf34` / window 4754 — eleven minutes apart during integration. Flat, the second write silently
overwrites the first."*

**The generalisation the amendment should carry:** *date-unique* is a property of the **day**, not
of the **run**. A grammar that assumes one run per day is safe only while the throttle holds, and
the throttle here is a gitignored per-working-tree file. ADR-84's Fact 2 is the doctrine both
collisions inherited.

**Scope honesty:** candidate (k)'s collision is in `logs/`, not on ADR-84's two automation streams.
The amendment records the falsified *reasoning* and the live exposure `[#418]` measures on ADR-84's
own `automation/fleet-audit` stream — not a claim that the digest stream has already collided.

**Command:**

```bash
$EDITOR docs/decisions/ADR-84-automation-writer-isolation.md
#   append: "## Amendment — <date>: Fact 2 corrected — date-unique is not run-unique"
#   citing [#418] (10 commits on 2026-07-10) and STANDING_RULINGS section AD candidate (k)
uv run --locked python scripts/validate_adr_status.py
git commit -m "docs(adr-84): amend Fact 2 -- date-unique filenames are not run-unique; two measured collisions"
```

---

### B4 · REWORD `[#564]` — three of its measured premises have moved, one to false

**Verb:** REWORD. **Class:** tasks. **Confidence:** high — all three re-measured at this SHA.

**The row's own measurements, quoted from `tasks/564-lifecycle-archival-implemented-adrs-and-decided-int.md`:**
*"`docs/decisions/archive/` holds 2 files (`ADR-40`, `ADR-52`) against 86 live ADRs, 83 of them
`Accepted`, and `docs/intake/` holds 34 files with 16 `ACCEPTED` and zero archived — there is no
intake archive at all."*

**Re-measured at `78daf400`:**

```
docs/decisions/archive/          2 files          UNCHANGED (ADR-40, ADR-52)
live ADR files                   89               was 86
docs/intake/ live                57               was 34
docs/intake/archive/             12 files         was "zero archived / no intake archive at all"
```

The intake half of the premise is now **false**: `docs/intake/archive/` exists and holds twelve
files, and `funnel_lifecycle` reports `intakes 57 live / 12 archived`.

**And the decisive one — the row's mechanism is a no-op as specified.** Its leg (a) is a one-time
pass under ruling **H3** (`protocols/STANDING_RULINGS.md:691`, *"An ADR archives at zero inbound
references"*). Measured over every tracked file at this SHA:

```
ADRs with ZERO inbound citation anywhere in the tracked tree:                    0
ADRs cited by no file OUTSIDE docs/decisions|audits|handoffs|archive:            0
reproduce: for each docs/decisions/ADR-*.md, grep the `ADR-<n>` token across `git ls-files`
```

So H3's predicate selects **nothing** at HEAD. The row's own honest limit already anticipated the
shape (*"leg (a) cannot fire on an ADR whose supersession was never written into its status
line"*) — this measurement confirms it is the whole of leg (a), not an edge case. **Leg (b), the
lag check, is the part that survives** and is untouched by this re-measurement.

**Command:**

```bash
$EDITOR tasks/564-lifecycle-archival-implemented-adrs-and-decided-int.md
#   body: re-measure the three figures against docs/audits/2026-09-05-technical-funnel-groom-sheet.md §B4
#   body: record that H3 selects 0 ADRs at 78daf400, so leg (a) is empty as specified
#   body: strike "there is no intake archive at all" -- docs/intake/archive/ holds 12 files
uv run --locked python scripts/gen_task_tree.py --emit-source
uv run --locked python scripts/gen_task_tree.py --check
git commit -m "docs(backlog): reword [#564] -- three measured premises re-measured; H3 selects zero ADRs at 78daf400"
```

---

### B5 · REWORD `[#242]` — the divergence it wants to seed is live in three ADRs

**Verb:** REWORD. **Class:** tasks. **Confidence:** high — the detector prints the three cases.

**The clause, from `tasks/242-adr-status-flip-coherence-check.md`:**
*"ADR-88/89 now Pattern B; only the go-forward check remains · Done when: a seeded ADR with a
header↔README status divergence is flagged by an audit check, with tests."*

**Witness — the divergence is not hypothetical at this SHA:**

```
  [WARN] coherence: ADR-45 -- header 'Explored, not adopted' != README index 'Superseded'
  [WARN] coherence: ADR-46 -- header 'Partially superseded' != README index 'Accepted'
  [WARN] coherence: ADR-47 -- header 'Partially superseded' != README index 'Accepted'
```

`validate_adr_status.py` **already detects** the class the row asks to build; what it does not have
is an `audit.py` registration with the tests the clause names, and the three live cases are
undispositioned. The row reads as if the only remaining work were a seeded fixture, which
understates it: there is a live three-case backlog behind the check.

**Adjacency, so this is not filed twice.** `[#553]` owns `docs/decisions/README.md`'s **aggregate
census figures**; `[#362]` owns the substantive-guard half. This bundle touches neither — it
records that `[#242]`'s own subject is live, not seedable-only.

**Command:**

```bash
$EDITOR tasks/242-adr-status-flip-coherence-check.md
#   body: name ADR-45 / ADR-46 / ADR-47 as the live divergences at 78daf400
#   Done-when: "...a seeded ADR ... is flagged, with tests, AND the three live cases carry a disposition"
uv run --locked python scripts/gen_task_tree.py --emit-source && uv run --locked python scripts/gen_task_tree.py --check
git commit -m "docs(backlog): reword [#242] -- three live header-vs-README divergences, not a seeded case only"
```

---

### B6 · REWORD `[#487]` — add leg (v): the closure baseline is gitignored, so WEAK is dead off the operator's machine

**Verb:** REWORD. **Class:** tasks. **Confidence:** high — measured by this run.

**The row already enumerates four pipeline defects (i)–(iv)**, including *"(ii) unpin
`since_commit` — an unchecked-still-open id pins the baseline"*. That is a defect about the
baseline being held **too far back**. This is the opposite failure and is not in the row.

**Witness — this run, on a fresh clone at `78daf400`:**

```
propose_closures: 0 strong, 0 weak over 377 commit(s) -> PROPOSALS-2026-09-05-01.md (weak suppressed: cold start)
since_commit: (none — cold start / no prior baseline)
```

**The mechanism.** `resolve_window` derives the baseline from prior `logs/PROPOSALS-*.md`
artifacts (`scripts/propose_closures.py:323`, `_SINCE_RE`). Those artifacts are gitignored
(`.gitignore:26`). Therefore **any checkout that is not the operator's own working tree** — a cloud
lane, a codespace, CI, a freshly provisioned worktree — has no baseline, cold-starts, and
suppresses the WEAK leg permanently. It is not a first-run cost that amortises; the state never
travels.

**Why it matters to this row specifically:** `[#487]` is scoped *"repair the pipeline first"* on
the grounds that *"a broken pipeline's output just re-parks"*. A pipeline whose only proposing leg
cannot run anywhere except one machine is a fifth repair, and it interacts with (ii): fixing the
pin does nothing where there is no baseline to pin.

**Command:**

```bash
$EDITOR tasks/487-closure-proposal-consumption-arc-139-parked-prop.md
#   body: add "(v) the baseline does not travel -- resolve_window reads gitignored logs/PROPOSALS-*.md
#         (:323 _SINCE_RE, .gitignore:26), so every non-operator checkout cold-starts and WEAK never runs;
#         measured 78daf400, cloud clone: 'weak suppressed: cold start' over 377 commits"
#   Done-when: extend "(i)-(iv)" to "(i)-(v)"
uv run --locked python scripts/gen_task_tree.py --emit-source && uv run --locked python scripts/gen_task_tree.py --check
git commit -m "docs(backlog): reword [#487] -- add leg (v), the closure baseline is gitignored and never travels"
```

---

### B7 · ARCHIVE — candidate (g) is EXECUTED; disposition it and the artifact it produced

**Verb:** ARCHIVE (disposition, not a file move — ADR-100 is keep-all-accepted). **Class:** audits.
**Confidence:** high.

**The candidate, from `protocols/STANDING_RULINGS.md` section AD:**
*"**(g) Gemini/agy whole-corpus doctrine-coherence audit** … Contradictions, dead rules, duplicated
clauses and never-cited files, each WITH locators; retrieval-only, architect rules. **H0
PRECONDITION**, alongside (a)."*

**Witness — it ran, and the artifact is in-tree:**

```
docs/audits/2026-09-05-technical-corpus-coherence-gemini.md:1
    # Corpus coherence audit (candidate g) — Gemini as whole-corpus reader
    Reader: Gemini 3.1 Pro (High) via the `agy` (Antigravity) CLI — the fan_out lane
    Verifier: Claude Code, live locator re-read against the working tree
```

Section 11 of the batch-G close packet proposed **(g) first**, *"because it is retrieval-only and
its output re-prices everything after it"*. That sequencing step is now spent, and the register
still carries (g) as an open candidate. Leaving it open is exactly the accumulation `[#552]` names.

**Command:**

```bash
# 1) mark the candidate discharged in the register (append-only section, dated addendum)
$EDITOR protocols/STANDING_RULINGS.md      # section AD: candidate (g) -> EXECUTED, citing the audit path
# 2) give the audit a disposition row so funnel_coverage stops counting it uncovered
$EDITOR docs/audits/2026-08-17-technical-audit-disposition-ledger.md
#   add: 2026-09-05-technical-corpus-coherence-gemini.md | ACTIONED | candidate (g), register section AD
uv run --locked python scripts/funnel_coverage.py
git commit -m "docs(rulings,audits): candidate (g) EXECUTED -- disposition the corpus-coherence audit"
```

**Honest limit:** the disposition ledger is itself an immutable dated audit. If appending a row to
it is refused under CLAUDE.md §5 rule 3, the lawful shape is a **new dated ledger**, which is the
same shape `[#552]` leg (b) is designed to produce. That choice is the operator's; both discharge
the coverage gap.

---

### B8 · RETIRE — three READY intakes with no carrier, ten days before the threshold fires

**Verb:** RETIRE (status transition; the alternative is ratification, and that is the operator's).
**Class:** intakes. **Confidence:** high on the measurement, **the disposition is a decision**.

**Measurement.** Across all 57 live intakes, exactly three are `status: READY`, name **no** `[#id]`
in their own body, **and** are cited by **no** file in `tasks/` (searched both by filename and by
`intake #<n>`):

```
intake #43  READY  docs/intake/2026-08-24-tech-ruling-register-landing-gap.md
                   "Rulings are made and then land nowhere — the register stopped absorbing on 2026-08-15"
                   24 of 39 ruling sets absent from the register; 4 landed nowhere in the repo at all
intake #47  READY  docs/intake/2026-08-24-tech-supplement-probe-fill-state-defect.md
                   "The `SUPPLEMENT` probe passes while the consequence it states is false"
intake #51  READY  docs/intake/2026-08-26-tech-provider-capacity-anthropic-compatible.md
                   "Provider capacity — Chinese cloud models via Anthropic-compatible endpoints"
```

Every other READY intake resolves to at least one row (§A2 has the full join).

**Why now rather than at the threshold.** `funnel_lifecycle` leg d is **0** because its READY
threshold is 30 days (`protocols/FUNNEL_LIFECYCLE.md:316`) and these are 10–12 days old. They fire
on **2026-09-23** (#43, #47) and **2026-09-25** (#51). Grooming them at the threshold means
adjudicating them under a red detector; grooming them now means adjudicating them on their merits.

**The recommendation, stated so the operator rules rather than authors.** #43 documents a live
governance failure with numbers — it reads as *ratify*, not retire, and section AD's own existence
is evidence the register absorbs again. #47 and #51 are the retire-or-ratify calls.

**Command:**

```bash
# per intake, ONE of the two lawful transitions -- both are frontmatter edits, intakes are not immutable
$EDITOR docs/intake/2026-08-24-tech-ruling-register-landing-gap.md   # status: READY -> ACCEPTED (ratify)
$EDITOR docs/intake/2026-08-24-tech-supplement-probe-fill-state-defect.md
$EDITOR docs/intake/2026-08-26-tech-provider-capacity-anthropic-compatible.md
#   retire path: status: READY -> REJECTED, then move to docs/intake/archive/ per the file's own lifecycle
uv run --locked python scripts/gen_intake_index.py --write
uv run --locked python scripts/funnel_lifecycle.py --report
git commit -m "docs(intake): adjudicate #43/#47/#51 -- READY with no carrier, ahead of the 30-day threshold"
```

---

### B9 · REWORD `[#626]` — its Done-when is unreachable while the naming collision wedges retention

**Verb:** REWORD. **Class:** tasks. **Confidence:** high — the close packet measured the block.

**The clause, from the batch-G close packet's own transcription:**
*"`[#626]` CLAUSE `ls logs/` after retention: no dated `PROPOSALS-*` / `DETECTOR-ERROR-*` flat
(step A). WITNESS step A, run 2026-09-04: 3 flat before, 3 flat after. Retention REFUSED."*

**Witness for why it stays unreachable, not merely unmet:**

```
docs/audits/2026-09-02-technical-batch-g-close-packet.md §9 item 2
    "Once one copy is archived, apply_moves correctly REFUSES to overwrite it and aborts the whole
     plan, so 09-03 and 09-04 queue behind a collision that will never clear itself. The guard is
     right; the naming grammar guarantees the collision it guards against."
```

and the register's own framing of the fix as **not this row's**:

```
protocols/STANDING_RULINGS.md section AD, candidate (k)
    "Resolution is a naming decision (run-scoped suffix, or an archive-side merge rule), and it is
     the operator's, so nothing was deleted."
```

Two further facts step A surfaced that the clause's wording does not survive: retention buckets by
**month** (`logs/YYYY-MM/`), not into the `logs/proposals/` + `logs/detector-errors/` pair the
clause assumes.

**So the reword is two things:** name candidate (k)'s naming decision as `[#626]`'s **precondition**
(so the row is honestly blocked rather than repeatedly failing), and correct the clause's assumed
destination from the pair of directories to the month buckets that actually exist.

**Command:**

```bash
$EDITOR tasks/626-logs-retention-exempts-the-prefixes-that-accumulate.md
#   body: BLOCKED-ON candidate (k) -- the PROPOSALS-<date> naming decision (STANDING_RULINGS section AD)
#   Done-when: correct "logs/proposals/ + logs/detector-errors/" to the live logs/YYYY-MM/ bucketing
#   refs: docs/audits/2026-09-02-technical-batch-g-close-packet.md §9 item 2
uv run --locked python scripts/gen_task_tree.py --emit-source && uv run --locked python scripts/gen_task_tree.py --check
git commit -m "docs(backlog): reword [#626] -- blocked on candidate (k)'s naming decision; clause targets the wrong destination"
```

---

## 4 · COUNTS — before, and projected after all nine bundles

Every "before" figure is a detector's own output at `78daf400`; the projections assume every bundle
is adopted as written.

```
INTAKES                       before        after (projected)
  live                        57            54   (if #43/#47/#51 all retire+archive)
                                            57   (if all three ratify -- no file moves)
  archived                    12            15 / 12  correspondingly
  READY (frontmatter)         19            16
  READY with no carrier        3            0
  ACCEPTED                    19            19 / 22  (retire path / ratify path)
  source: funnel_lifecycle.py --report; join in §A2

AUDITS                        before        after (projected)
  corpus N                    879           880  (this sheet)
  dispositioned               78            79   (+ the corpus-coherence audit, B7)
  pending                      2            2
  manifest-linked             73            73   (derived: 879 - 78 - 2 - 726; see §A6)
  uncovered                   726           726  (this sheet lands undispositioned, as every audit does)
  source: funnel_coverage.py

ADRs                          before        after (projected)
  live ADR files              89            89   (amendments are in-file, never new numbers)
  archived                     2            2
  carrying a NEW dated         -            2    (ADR-110 B2, ADR-84 B3)
    amendment
  header-vs-README coherence   3            3    (B5 rewords the row, does not fix the ADRs)
    divergences
  source: funnel_lifecycle.py --report; validate_adr_status.py

TASKS                         before        after (projected)
  rows                        364           364  (closing retires, never deletes)
  open                        170           169  (B1 closes [#613])
  deferred                    54            54
  closed                      135           136
  retired                      4            4
  superseded                   1            1
  rows reworded                -            4    ([#564] B4, [#242] B5, [#487] B6, [#626] B9)
  source: funnel_lifecycle.py --report (rows 364);
          reproduce the split: grep -h '^status:' tasks/*.md | sort | uniq -c
```

---

## 5 · WHAT WAS CHECKED AND FOUND CLEAN — the non-findings, recorded so they are not re-derived

A groom that reports only positives hides the work. Each of these was a named target of item 006-A
and produced **no bundle**, for a stated reason.

**Batch manifests carrying `status: open` after their close packet landed — NOT a defect.**
Fourteen manifests declare `status: open` while their `closed_by:` target exists on disk. This
looks like stale state and is the designed shape. `scripts/batch_manifest.py:27` states it: *"HOW
OPENNESS EXPIRES, and why it is NOT a mutable `status:` flag. Manifests live under `docs/audits/`,
which is IMMUTABLE… the batch is open only while that path is ABSENT from the COMMITTED tree."*
`batch_manifest.py` exits 0 with no output — zero open batches. No bundle.

**Audits cited by nothing — six, all in-flight.** Excluding the generated `docs/audits/README.md`
index (which cites every audit and makes the metric vacuous), exactly six audits have zero inbound
citation from any tracked file:

```
2026-09-01-technical-629-630-lane-g-packet.md
2026-09-01-technical-boot-r1-prioritization-scheduling.md
2026-09-01-technical-lane-d-4-deploy-waiver-honoring.md
2026-09-02-technical-lane-g-614-hygiene-close-packet.md
2026-09-02-technical-lane-g-628-essentials-debless-packet.md
2026-09-05-verification-lane-h0-suite-speed.md
```

All are lane packets from the last four days; the newest is from today's in-flight batch H. This is
normal latency, not rot.

**But the corpus's own predicate is stricter, and it is the authoritative one.**
`consumer_at_landing`'s governance pool is deliberately narrow — `tasks/`, `docs/decisions/`,
`docs/intake/`, `protocols/` and the root canonical docs only, because *"a mention in a session log
or a machine baseline is a record that the file existed, not evidence that anything consumes it"*.
Under that pool, `audit.py health` at this SHA reports **thirteen** artifacts past the arm-time
baseline, verbatim from the run:

```
2026-09-01-technical-629-630-lane-g-packet.md          2026-09-05-technical-corpus-coherence-gemini.md
2026-09-01-technical-article-harness-substrate-brief.md 2026-09-05-technical-research-architekt-jutra-gap-analysis.md
2026-09-01-technical-boot-r1-prioritization-scheduling.md 2026-09-05-verification-lane-h0-suite-speed.md
2026-09-01-verification-batchf-integration-suite.md    ARM3_NOTE.md
2026-09-02-technical-lane-g-626-terra-tally.md         SEED_RUBRIC.md
2026-09-05-technical-627-readjudication.md             VERDICT_RULE.md
2026-09-05-technical-funnel-groom-sheet.md  (this file)
```

Two consequences worth stating. First, my looser six-file measurement understates the real
consumption gap — cite the detector, not the grep. Second, **`2026-09-05-technical-corpus-coherence-gemini.md`
is in that list**, which strengthens bundle B7: dispositioning it discharges the coverage gap *and*
names its consumer in one act. Still no separate bundle for the class — `[#552]` owns it.

**ADRs cited by zero live files — zero.** Measured over every tracked file: no ADR is uncited, and
none is uncited outside `docs/decisions|audits|handoffs|archive`. No bundle. (This is also the
measurement that empties `[#564]`'s leg (a) — see B4.)

**Near-duplicate rows — one candidate pair, and it is a false positive.** A title-similarity scan
over all 224 open+deferred rows produced exactly one pair above threshold:

```
0.678  [#145] Codification-completeness pass
       [#153] Enforcement-completeness pass
```

Read in full, they share a suffix and nothing else: `[#145]` audits what a fresh session cannot do
from PLAYBOOK + the handoff bundle; `[#153]` moves browser-re-stated constraints to mechanical
enforcement. Not duplicates. **No `#629`/`#630`-shaped duplication survives at this SHA** — and
that pair was itself a *deliberate* split, stated in both row bodies (*"deliberately a separate row
because it is a different gate at a different moment"*) and confirmed by the batch-G packet §9
item 6. No MERGE-ROWS bundle exists.

**Rows with no theme or no story — zero.** All 364 task files carry both frontmatter fields.

**L rows with no decomposition — not a defect class here.** Eighteen `size: L` rows exist, fifteen
open or deferred (§A4). `tasks/` carries no parent/child edge, so "decomposition" is not machine-
resolvable; the corpus expresses it as `depends-on` and `serialize-group`, and `boot_frontier`
already holds 62 rows back on serialize-group disjointness. Proposing decomposition per L row would
be authoring, not grooming. Listed in the appendix, no bundle.

**Rows whose Done-when names a now-existing test — two, both still RED.** `[#585]` and `[#586]` are
"Suite RED" rows whose clause is that the named test goes green. Both tests exist; both were run at
this SHA and both fail:

```
FAILED tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export
FAILED tests/test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent
2 failed in 1.19s
```

with, for `[#585]`, the discriminating assertion still inverted (`assert 'absent' == 'enforcing-local'`).
Both rows correctly stay open. No bundle.

**`[#627]` — explicitly stays open.** Today's `docs/audits/2026-09-05-technical-627-readjudication.md`
ratifies the batch-F REFUSE and names `[#627]` in its own Consumers line as *"stays open"*. No bundle.

**The 726 uncovered audits — already OWNED.** `[#552]` owns exactly this: *"Window-close disposition
+ archival routine — every new audit gets a disposition."* This sheet files no second row against
it (ADR-111: one triage per finding). B7 dispositions one artifact; the mechanism is `[#552]`'s.

---

## 6 · TWO LOCATORS IN THE CONTRACT THAT DO NOT RESOLVE

Clause 6 binds this lane to resolve every locator before using it. Two in the frozen text do not
resolve, and both are reported rather than silently worked around.

**"intakes `#68`/`#69`" — no such intakes exist.** The dedupe target named in the contract's TASKS
leg cannot be honoured as written. Highest allocated intake id at this SHA is **#67**
(`2026-09-01-tech-lane-packet-artifacts-block.md`); the archive tops out at **#64**
(`2026-09-01-tech-quota-source-field.md`, REJECTED). `grep -rn "^intake-id:" docs/intake/` matched
nothing for 68 or 69. The only in-repo string resembling "#69" is an unrelated deferral id in a
2026-07-19 handoff bundle. **The batch-G candidates were therefore deduped against `tasks/` and
against the live intake set instead** — §A3.

**"batch-G candidates (a)-(t)" — the register runs (a)–(g), (i), (j), (k): ten, not twenty.** And
the gap is deliberate, stated in the register itself: *"The lettering runs (a)–(g), (i), (j), (k):
**there is no (h)**, and its absence is deliberate rather than a lost entry."* All ten are deduped
in §A3.

**One name in the contract that DID resolve, recorded because it was flagged as uncertain:** the
doc-rot module is `scripts/validate_doc_rot.py`, as the contract's own parenthetical stated. It ran.

---

## APPENDIX

### A1 · Intake status distribution at `78daf400`

Live: 57 (`funnel_lifecycle`). By frontmatter `status:` — SEED 10, DRAFT 9, READY 19, ACCEPTED 19.
Archived: 12, of which CONSUMED 8, REJECTED 3, SUPERSEDED 1. (Grepping `^status:` across
`docs/intake/*.md` over-counts by three: `README.md` carries two prose lines and one placeholder
that match. Exclude it.)

**One integrity observation, no bundle proposed.** Three files claim `intake-id: 14`:

```
docs/intake/2026-07-12-siem-requirements-ruled-pack.md:2
docs/intake/archive/2026-07-13-siem-fleet-management-requirements.md:2
docs/intake/archive/2026-07-13-siem-fleet-management-requirements-codex.md:2
```

The join key `funnel_coverage` and `consumer_at_landing` rely on (`intake #<n>`) is therefore
ambiguous for #14. It is the only collision in the corpus. Not filed as a bundle: `[#440]` owns
id-ledger tamper-evidence and `[#580]` owns atomic id allocation, and this is arguably within
`[#580]`'s scope — routing it is a triage call, not this sheet's.

### A2 · The intake→row join, ACCEPTED and READY only

Intakes reaching rows only by **reverse** citation (the intake names no `[#id]`; a row names the
intake) — these are healthy, not orphans:

```
#12 ACCEPTED <- [#548]                      #49 READY <- [#589] [#590] [#608]
#13 ACCEPTED <- [#332] [#549]               #50 READY <- [#615]
#14 ACCEPTED <- [#550]                      #52 READY <- [#591] [#592] [#593] [#594]
#17 ACCEPTED <- [#403] [#431]               #53 READY <- [#603]
#24 ACCEPTED <- [#570]                      #55 READY <- [#599] [#600] [#601] [#602] [#603]
#31 ACCEPTED <- [#579]                      #58 READY <- [#609]
                                            #60 READY <- [#271] [#391] [#610] [#611]
```

Neither direction resolves for **#43, #47, #51** — bundle B8.

### A3 · Batch-G candidate register (section AD) deduped against `tasks/` and the live intakes

```
(a) README as a human front door        OVERLAPS  [#622] (promote README into ADR-38 mandatory),
                                                  [#620] (retire the root-README prohibition fleet-wide),
                                                  [#621] (the nine-repo filename migration)
                                        DELTA     none of the three owns README's CONTENT SHAPE
                                                  (what-it-is / quickstart / link map). Genuine remainder.
(b) two files named HANDOFF_BOOT.md     OVERLAPS  [#611] (v7 minimal bundle) -- the register itself
                                                  files it as "[#611] family". Fold, do not birth.
(c) DERIVED-COPIES REGISTRY             NO ROW    grep over tasks/ for routing_agreement / "derived cop"
                                                  returns nothing. Genuine CANDIDATE.
(d) [#627] admission = retrieval        OWNED     [#627], open. Today's readjudication audit ratifies
    fidelity on a seeded corpus                   REFUSE and keeps it open. No action.
(e) codespace container-only nodeids    OWNED     [#632], open; register says "held open deliberately".
(f) contract-freeze COUPLING SCAN       NO ROW    grep for "coupling scan" over tasks/ returns nothing.
                                                  [#629]/[#630] are the amendment and manifest-slug gates,
                                                  a different moment. Genuine CANDIDATE.
(g) Gemini/agy corpus-coherence audit   EXECUTED  docs/audits/2026-09-05-technical-corpus-coherence-gemini.md
                                                  -> bundle B7.
(i) lane liveness / heartbeat           NO ROW    grep for heartbeat|"lane liveness" over tasks/ returns
                                                  nothing. Genuine CANDIDATE.
(j) per-consumer freshness registry     OVERLAPS  [#276] (the .methodology.yaml waiver carrier) -- CLOSED.
    in .methodology.yaml                DELTA     the registry itself is unowned. Genuine remainder,
                                                  flagged H0 PRECONDITION by the register.
(k) PROPOSALS-<date> is day-granular    OVERLAPS  [#626] (logs/ does not thin) -- open, and BLOCKED BY (k).
    for a per-RUN artifact              DELTA     the naming decision is the operator's, per the register.
                                                  -> bundle B9 makes the block explicit.
```

Routing, per ADR-111, is CANDIDATE → intake (ADR-98) → ratification. **This sheet births nothing.**
The three with no existing row — **(c), (f), (i)** — plus the two remainders **(a-shape), (j)** are
the intake-pass input.

### A4 · `size: L` rows, open or deferred (15 of 18)

```
[#43]  deferred P3   Decide +
[#139] deferred P2   merged-arc -> record verifier
[#244] deferred P2   Essence-spec lifecycle epic
[#271] open     P3   Nightly proposal loop
[#383] open     P2   Execution waves per surface
[#487] open     P2   Closure-proposal consumption arc -- repair the pipeline first      (bundle B6)
[#559] open     P2   Kernel/lab check tiering + dev-knowledge-kernel as an installable package
[#570] open     P2   Consume intake #27's W-wave rows
[#579] open     P1   Code doctrine & FDD -- one ADR merging intakes #31 and #34
[#581] open     P1   Backlog vitals -- three flow instruments                            (boot_frontier proposes)
[#582] open     P1   Substrate router
[#606] open     P2   The win-tooling first-slice instantiation arc
[#621] open     P2   ADR-114 option (C): the nine-repo VISION.md -> README.md migration
[#628] open     P1   DC-2 re-cut -- ESSENTIALS dissolution is a fleet-coupled release act
[#632] open     P1   Codespace ADMITTED for transport, UNSTABLE for inference
```

### A5 · `funnel_lifecycle` leg c — five post-cutoff rows whose provenance clause resolves nothing

Reproduced verbatim in §2.1. All five landed 2026-08-31 and cite provenance tokens that resolve to
nothing in the tree (`'coherence-audit'`, `'G6 process-hardening sweep'`, `'N4-F1/F6/F5/F12'`, a
bare list of ids and line pins, an audit-matrix cell). **No bundle proposed**: the detector already
names them, they are already RED, and repairing a provenance clause on five rows is a lane's work
with a write scope, not a groom proposal. Recorded so the next batch can pick it up as one unit.

### A6 · Two reading notes on detector output, so the next seat does not re-derive them

**`funnel_coverage`'s printed lines do not sum to its corpus, and that is correct.** `78 + 2 + 726
= 806`, against `corpus N 879`. The missing **73** are the `manifest_linked` bucket:
`uncovered = corpus − (dispositioned ∪ pending ∪ manifest_linked)` (`scripts/funnel_coverage.py:228-232`).
That bucket has no line in the report. Not filed as a bundle — it is a one-line reporting addition
inside `[#552]`'s and `[#581]`'s territory — but it is exactly the arithmetic a reader would
otherwise flag as a defect.

**The generated audits index is stale at HEAD, by four documents, before this file existed.**
`gen_audit_index.py --check` reports `-**875 audit documents.** / +**879 audit documents.**`. This
does **not** block a new audit: `[#590]` narrowed `audit-index-freshness`'s `files:` to the index
and its own generator precisely so a lane adding an audit is not forced to regenerate a shared file
(*"requiring every lane to regenerate a shared file put `docs/audits/README.md` in 6 of the last 7
conflicted merges"*). So the staleness is by design at lane time and is the integrator's or the
`merge=ours` driver's to resolve — recorded here because a reader running `--check` will otherwise
read it as this lane's mess. **No regeneration was performed**, which keeps clause 2 intact.

**`audit.py health` is DEGRADED in this container, identically with and without this file.**
Measured both ways: `health rc=1` with the deliverable staged, `health rc=1` on the stashed clean
tree. Every `[!!]` is an artifact of the cloud substrate, not of this arc — a **shallow clone**
(`git rev-parse --is-shallow-repository` → `true`, 377 commits) which makes `canonical_freshness`
refuse its derived leg and `journal_spine_anchor` fail to resolve its disposition floor, plus
unarmed git hooks. Nothing in the health verdict moved because of this sheet.

**Three detectors ignore `--help` and run their check instead.** `validate_git_backlog.py`,
`propose_closures.py` and `validate_doc_rot.py` each executed a full pass when invoked with
`--help`. Harmless for read-only checks; worth knowing before assuming a `--help` invocation is
inert. `propose_closures.py` in particular **writes its artifact** on any invocation.

### A7 · Open rows citing a path absent at HEAD — resolved, and mostly not defects

Eleven open or deferred rows cite a repo-relative path that does not exist at `78daf400`. Each was
opened; the honest split:

```
INTENDED TARGETS (the row exists to create the file) -- not defects
  [#112] scripts/hooks/adr_amend.py
  [#540] scripts/harvest_batch.py
  [#632] tests/test_dispatch_helpers_codespace.py

DELIBERATE REFERENCES TO AN ABSENT THING (the absence IS the row's subject) -- not defects
  [#428] .github/workflows/nightly-conformance-triage.yml   "deleted at 82227f08" -- the row says so
  [#613] protocols/ROUTING.md                                the REJECTED candidate path (see B1)

GITIGNORED ARTIFACTS (absent by design in any clone) -- not defects
  [#322] logs/BOUNDARY-DRIFT.md
  [#418] logs/FLEET-HEALTH.md                                the row itself calls it gitignored

CROSS-REPO PATHS, correctly prefixed in the row -- not defects
  [#509] scripts/dispatch/Invoke-Dispatch.ps1                refs read "win-tooling scripts/dispatch/..."
  [#393] config/category_mapping.yaml, config/excluded.yaml  corp-sca paths

GENUINELY STALE LOCATOR
  [#564] decisions/README.md                                 missing the docs/ prefix -> bundle B4 rewords
                                                             this row anyway; fold the fix in.
  [#427] .dev-knowledge/logs/TOKEN-LOG.md                    repo-name-prefixed path. The row's SUBJECT is
                                                             repo-position-dependent paths in region
                                                             templates, so this is plausibly deliberate.
                                                             Left as-is; flagged for the row's owner.
```

**One bundle-worth of signal, folded rather than filed separately:** only one of eleven is
unambiguously stale, and it belongs to a row already being reworded. The "vanished path" class is
in far better health than the raw count suggests.

---

## CLOSURE — how this sheet answers its own contract

```
(1) pinned SHA printed before any count                §0, before §2's first number
(2) every bundle cites a witness that resolves         each bundle's Witness block; all locators opened
(3) every bundle carries an executable command         each bundle's Command block
(4) git status shows no file changed outside this      confirmed at commit; logs/PROPOSALS-2026-09-05-01.md
    deliverable                                        is gitignored (.gitignore:26) and disclosed in §1
(5) the deliverable is a COMMIT on the lane branch,    docs/funnel-groom-2026-09-05, pushed
    pushed
```

**Owed, and not discharged by this lane.** The frozen text asks for a copy into the operator's
`to-browser` directory. A cloud lane has no access to the operator's disk, so the copy is owed by a
**local seat at harvest** and is recorded here as an open residual rather than silently dropped.
Merging is the primary-checkout integrator's.
