# NIGHT-MISSION 2026-08-28/29 — CLOSE PACKET

**Authorization.** `NIGHT-MISSION-2026-08-28.md`, ratified in writing by the operator's GO paste.
Executed with **zero operator contact**, as designed. GO-carried decisions applied: **D2** ratchet
granted to lane C only · **D3** `tasks/archive/` approved · **D4** merge order confirmed ·
self-merge authorized **only** for the mission's serialized integration steps.

**What this file does when it lands.** It is the `closed_by:` path named by
`docs/audits/2026-08-28-technical-batch-2-manifest.md`, so committing it **closes the ADR-110
exemption automatically**. Nothing else expires it; nothing has to be edited.

---

## 1 · THE TRUST LINE (A5) — every ex-ante number, verbatim, then what was measured

| id | ex-ante, **verbatim from the mission** | measured | verdict |
|---|---|---|---|
| **W1-1** | *7/7 local lanes commit-and-STOP; 6/6 cloud artifacts (C1-C5 + FM-C) delivered or harvest-pending with receipts* | 7/7 reached commit-and-STOP and were merged; 6/6 cloud reports delivered, G1+G2 hard gates passed for all six, G3 receipts in 21–72 s | **MET** |
| **W1-2** | *audit repo win-tooling: floor present, pre-commit armed, role=consumer; 11/11 branches carry upstreams (git branch -vv recorded)* | floor **PASS** (was N/A "has not adopted the floor"); `deployed_methodology_version` **PASS v1.4.0**; checks passing **13 → 15**; pre-commit **configured, NOT armed**; role **held at pre-deploy**; upstreams **11/11** | **PARTIAL — 2 of 4 legs** |
| **W1-3** | *validate_doc_rot findings: 77 (re-measured) -> strictly lower, zero content destroyed* | **77 → 60**; `backlog-row-length` arm 68 → 55; 20 rows relocated byte-identically, md5 per object, **zero content destroyed** | **MET** |
| **W1-4** | *ratchet: 443 -> new value reported, delta == N3's authorized bound exactly* | **443 → 443, delta ZERO**. Verified twice: in lane C's own worktree (443/61) against the primary (443/61), and again on merged main | **MET — the grant went unused** |
| **W1-5** | *[#577] byte-cap test green at 9,161 B payload; fails on planted oversize fixture* | 8 tests **pass**; planted-oversize half proven; payload is **9,430 B = 28.78 %**, **not 9,161 B** | **MET, with the ex-ante's own number corrected** |
| **W2-1..W2-5** | *(the wave-2 numbers)* | **not run** — see §2 | **NOT RUN** |
| **W2-6** | *operator process questions consumed tonight+morning: 0* | **0**. No question was asked; the one fork that arose was resolved against a standing ruling (§2) and is handed over as a one-line decision rather than a query | **MET** |

**W1-5's ex-ante number was itself wrong, and that is the finding.** `9,161 B` came from
`CLAUDE.md` §2.68's claim that root `AGENTS.md` is *"103 lines, 5,270 B"*. Measured:
**5,539 B / 107 lines**, and `git cat-file -s 43c18e9f:AGENTS.md` == **5539** against the file's
**only** content commit — so those figures were wrong **when written**, not stale by drift. The
lane asserted against the **cap**, re-measuring live, rather than against a remembered constant.

---

## 2 · WAVE 2 DID NOT START — the gate fired, and here is exactly why

The mission's step 5: *"Verify wave-1 success numbers. **ALL green -> boot wave 2. Any RED ->
STOP**, write the morning packet with what stands, do not start wave 2."*

**W1-2 is not green.** Two of its four legs are unmet:

- **"pre-commit armed"** — the deployed set is **configured, not armed**. The arming vector *is*
  deployed (the `tier1-lifecycle` plugin's SessionStart hook runs `pre_commit install`), so it
  arms on the consumer's next session. Note also that `audit repo` **cannot assert this leg at
  all**: `hooks_armed` reports `N/A — hub-only` for a non-hub repo, so the ex-ante names a check
  that is structurally unable to answer it.
- **"role=consumer"** — **NOT flipped, and deliberately so.** Lane A made the flip, measured it,
  and **reverted** it: as `consumer`, `test_check_fleet_parity_green_on_live_repo` REDs, and that
  test's own docstring reads *"promotion REDs nothing"* — so the RED is a true signal about that
  exact act, and editing anything to make the promotion pass would have been falsifying the
  instrument. The convenient explanation (*"it is only red because the deploy sits on an unmerged
  branch"*) was **refuted**, not assumed, by walking parity directly against the deployed tree.
  win-tooling carries real divergences (`docs-genre-decisions`, `methodology-yaml`,
  `pytest-minversion`, `root-gitattributes`, …) whose resolution is its own arc.

**Why I stopped rather than reading "PARTIAL" as "green".** The mission offers two cells, ALL
green and any RED, and W1-2 fits neither cleanly: nothing is broken, no gate is failing, and yet
the stated number is not met. That is a **no-ruling fork**, and the decision budget routes a
no-ruling fork to the operator — while tonight's contact budget is **zero**. When those two
collide, this repo already has a tie-breaker, and it is **Z-G4**: *a check that cannot compute its
ground truth **FAILS** — it does not skip.* Applied to a stop-gate, that reads: when the gate
cannot decide, it **stops**. Booting eight more lanes on my own re-reading of a ratified stop rule
would have been precisely the act S4 exists to refuse, performed by the integrator instead of by a
lane.

**The cost is named rather than hidden: roughly five hours of night went unused.** What that
bought instead is below, and the reversal is one line.

**Wave 2 is loaded and safe to fire.** All eight contracts are authored, carry `**Substrate:**`
and worktree-pairing declarations, and **dry-run clean through `dispatch`** (`source: contract` on
all eight — no derivation, no WARN). They sit in the prompts dir as
`NB2-W2-LANE-{H,I,J,K,L,M,N,O}-*.md`. Two carry late addenda written from FM-C's returned census —
see §5. **One operator line — "W1-2 partial is accepted, boot wave 2" — starts them.**

---

## 3 · THE SUBSTRATE ATTEMPT (Z-G3) — one attempt, authorized, and it paid off backwards

The mission authorized exactly one Codespace smoke-6 attempt during step 5. It was made at
**01:37** against `origin/main` @ `b4ab25ab`, `basicLinux32gb`, `-IdleTimeout 30m`,
`-Retention 24h`.

**Verdict against Z-G3's entry condition — `Ok=True` AND `RemoteExitCode=0` AND
`receipt HEAD == pushed HEAD`: NOT PRODUCED.** `Ok=False`, no `RemoteExitCode`, no receipt.
The codespace created in 9 s and then the contract copy-in failed:

```
[codespace] FAILED -- copying the contract in exited 1.
scp.exe: dest open "'/workspaces/dev-knowledge/NB2-SMOKE6-zg3-entry.md'": No such file or directory
scp.exe: failed to upload file C:/Users/1028120/Downloads/NB2-SMOKE6-zg3-entry.md
        to '/workspaces/dev-knowledge/NB2-SMOKE6-zg3-entry.md'
```

**Read the quoting.** The destination reaches `scp` as `'/workspaces/…'` — wrapped in **literal
single quotes**. That is W4 defect 1, the cp-quote defect, **reproduced end-to-end for the first
time, with its exact error text.**

**This discharges lane B's one MEASUREMENT-OWED.** Lane B's contract said: *"if it cannot be
reproduced without a live codespace, ship the verbs, mark the cp fix MEASUREMENT-OWED with the
reproduction recipe, and say so."* It did exactly that, and marked done-item 2b **NOT MET —
MEASUREMENT-OWED**. The mission's substrate attempt then produced the missing measurement, on the
**pre-fix** module, which is the correct control: `~/.dispatch-helpers/Modules/DispatchHelpers/`
still carries the **old** module, because the fix landed in win-tooling `main` and
`Apply-DispatchHelpers.ps1` was **not run**.

**Deliberately not done, and why.** Deploying a 860-line module change to the operator's **live**
dispatch surface at 01:40, unattended, to test one leg — when the same module drives the local and
cloud dispatch paths the operator actually uses every night — is an outward-facing risk with no
one awake to catch a regression. The evidence is better served by leaving the control intact.

**The morning action is two lines, with the before-measurement already in hand:**

```
pwsh -File <win-tooling>/scripts/dispatch-helpers/Apply-DispatchHelpers.ps1
Dispatch-Codespace -Contract ~/Downloads/NB2-SMOKE6-zg3-entry.md -Slug nb2-smoke6b
```

If the second line copies the contract in, defect 1 is closed **with a before and an after**.

**Z-G3 remains unmet regardless, and that is structural.** Its entry condition needs **all three**
W4 defects closed. This batch closed **one** (at the argv, now with a reproduction to test the fix
against). Defect 2 (`uv` absent / wrong in the container) and defect 3 (the silently stale clone)
were touched by **no lane tonight** — so the wave-2 router ADR's central evidence cannot exist yet,
by construction, and **LOCAL stays the default substrate**.

**Leftover, declared:** codespace `nb2-smoke6-g5rvj4w6qx4hv5q4` was **stopped** (compute billing
ended, confirmed `ShuttingDown`) and carries `retention=24h`, so it self-deletes. It is **not**
deleted by this session because `gh codespace delete` is deliberately unwrapped in the tooling —
deletion is an operator act, and overriding that to tidy up would be the wrong kind of initiative.

---

## 4 · PER QUEUE, PER LANE

Every lane reached commit-and-STOP. No lane merged itself. No lane wrote `JOURNAL.md`. Terra ran
pre-merge on every local lane, tally in each lane's own packet.

### Hub queue — merged in the frozen D4 order, `--no-ff`, one at a time

| lane | row(s) | merge SHA | verdict | terra |
|---|---|---|---|---|
| **C** (N3) | `[#610]` doc half | `44c2e90f` | **7/8 MET**, item (7) forms-card half **PARTIAL** | ran; caught item 1 at PARTIAL, **fixed not argued** |
| **D** (N4) | `[#612]` | `43c94846` | **MET** — 77 → 60, 20 rows, zero content destroyed | ran; 6 findings on `archive_row_body`, all closed |
| **G** (N8) | `[#591]` | `11db524e` | **6/6 MET** | ran; first round productive, not cosmetic |
| **A** (N1) | `[#604]` + `[#606]` | `89af0f8e` | items 1,2,5,7 **MET**; 3 **PARTIAL**; 4 **NOT-MET (measured)** | ran; 3 passes, incl. one on the unscoped diff |
| **E** (N6) | `[#605]` | `0060900f` | **4/4 MET** | ran |
| **F** (N7) | `[#577]` | `b4ab25ab` | **3/3 MET**; `[#577]` discharged **5 of 5 clauses** | ran; narrowed an overclaiming docstring, added an emptiness floor |

Anchor merge (not a lane, so not exempt — anchored in `JOURNAL.md` like any arc): `8b6de993`.

### win-tooling queue — B before A, which is D4 **and** mechanically necessary

| lane | merge SHA | verdict |
|---|---|---|
| **B** (N2) | `353d891` | (1) MET · (2) **PARTIAL** — locate MET, reproduce **MEASUREMENT-OWED** (now discharged, §3), fix MET at the argv · (3) MET · (4) MET |
| **A-consumer** | `d399bf2` | the v1.4.0 deploy — floor + sha256 + `check_floor_hash.py` + `.pre-commit-config.yaml` + session gate + intake spine |

B **had** to merge first: lane A arms the hook set B was written without, and both commit into one
`.git/hooks`. Merging A first would have gated B's merge through hooks that did not exist when B
was authored. That ordering was ruled by D4 for a different reason and turned out to be load-bearing
for a mechanical one.

### Deviations, each with an owner

| # | deviation | owner |
|---|---|---|
| **V-1** | Lane D wrote `scripts/validate_hermetization.py`, outside its frozen write-scope. **Not an S4 breach** — the dispatch contract's D3 paragraph pre-authorized exactly this: Rule C refuses a new home, and the operator's D3 approval is the authority to allowlist `tasks/archive/` **in the same commit, narrowly, with the ruling cited**. It did that, and did **not** reach for `--no-verify`. | recorded, no action |
| **V-2** | Lane B wrote `scripts/dispatch-helpers/Apply-DispatchHelpers.ps1` (+15), outside its frozen write-scope. Plausibly necessary — the applier deploys the module whose export list just grew — but it is a scope departure and the lane owns it in its packet. | architect, to ratify or narrow |
| **V-3** | Lane A pushed 10 branches to win-tooling `origin`. **Pre-authorized** by contract item (7). It correctly declined to push the two lane branches created after freeze, citing the contract's own *"Push nothing else"*. | recorded, no action |
| **V-4** | Wave 2 not started. §2. | **operator — one line reverses it** |
| **V-5** | The Codespace created by the substrate attempt is stopped, not deleted. §3. | operator (deletion is an operator act by design) |

### Stop conditions — which fired

| | condition | fired? |
|---|---|---|
| **S1** | unresolvable conflict on `JOURNAL.md` or a generated surface | **no** — every merge was clean; **zero conflicts in either queue** |
| **S2** | ship-gate **NEW** WARN naming a surface a tonight-lane touched | **no** — and the movement was the other way: `check_substrate_declaration` went **2 findings → 1** |
| **S3** | ratchet delta outside lane C's authorized bound | **no** — delta was **ZERO** |
| **S4** | a lane attempting an act its contract forbids | **no** — V-1 and V-2 are scope notes, and V-1 was pre-authorized |
| **S5** | hard stop 07:30 | **not reached** — the wave-2 gate at §2 stopped the mission first |

---

## 5 · THE ASSET BALANCE — your three categories, numbers not adjectives

### SMALLER

| measure | before | after | delta |
|---|---|---|---|
| `validate_doc_rot` loci | **77** | **60** | **−17** |
| `backlog-row-length` arm | 68 | 55 | −13 |
| backlog row-body characters | **42,927** | **28,078** | **−14,849 (−34.6 %)** over 20 rows / 27 clauses |
| `docs/intake/*.md` | 56 | **56** | **0** — see below |
| `docs/decisions/*.md` | 89 | **89** | **0** — see below |
| `tasks/**` | 344 | 365 | +21: the 20 durable per-row records + a README, ~**59,006 B** of narrative moved **out of the rows and KEPT** |
| `docs/audits/*.md` | 769 | 787 | +18 (the night's own evidence) |

**Why the two counts the mission expected to drop did not, and why that is a result rather than a
miss.** FM-3 never ran (§2) — but FM-C already established that **it would have had nothing lawful
to relocate**. Corpus-wide, across **951 objects, 100 % classified, UNCLASSIFIED = 0**:
**CONSUMED-AND-ARCHIVABLE = 0**. Three retention authorities account for it —
**ADR-100 §1** (*"Every accepted audit is kept, unbounded; audit files are never physically moved,
rolled up, or compacted"*) covers all 793 audit objects, **CLAUDE.md §5 rule 3** covers all 88
ADRs, and the intake predicate at `docs/intake/README.md:228-231` has **zero backlog**: live
statuses are ACCEPTED 19 · READY 19 · SEED 10 · DRAFT 7, **no terminal doc sits at depth 1**, and
all 8 files already in `archive/` are terminal. **Zero mis-filings in either direction.**

So the honest headline for this category: **the archival step is not what is broken.** The
shrinkage that *was* available — backlog row bloat — is the one that moved, by a third.

### VISIBLE

| census | numbers |
|---|---|
| **Funnel (FM-C)** | 951 objects · **100 % classified, UNCLASSIFIED 0** · PROTECTED **895** · CONSUMED-BY **45** · **CONSUMED-AND-ARCHIVABLE 0** · ORPHAN **11 (1.2 %)** |
| **Orphans, both directions** | forward: **11** intake docs, each re-tested by a second search method, none a false positive · backward: **61 → 24** rows with dangling refs after directory- and intake-id-aware resolution |
| **Codex surface (C4)** | **168** artifacts / **630,460 B** · 13 surfaces classified · **REMOVAL-READY: 0 surfaces, 0 bytes** · the `codex/AGENTS.md` precedence trap named explicitly |
| **README/VISION (C5)** | ~**5,881** references censused · ~**5,700** immutable / append-only / generated / gate-coupled · **mergeable surface: 5 lines in 1 file** |
| **Candidate triage (C1)** | n=11 → OWNED **2** · DISCHARGED **4** · CANDIDATE **5** · REJECTED **0**, collapsing to **at most 3** intake acts |
| **Consumption ledger** | 6 discharged · 4 owned · **12 candidates, each with a named owner** · 2 rejected with reasons · 5 method findings |

**Both of the big censuses came back NEGATIVE, and that is what makes them worth the night.**
"There is nothing to remove here, and here is the ruling that says so" ends a recurring proposal;
a worklist would only have deferred it.

### UNBLOCKED

| question | answer | evidence |
|---|---|---|
| win-tooling: **floor** present? | **YES** | `floor_integrity` **PASS** — present, hash matches sidecar, F5 clean, pointers resolve. Was `N/A — repo has not adopted the methodology floor` |
| win-tooling: **pre-commit** armed? | **configured, NOT armed** | the set is deployed; arming rides the plugin's SessionStart hook. `audit repo` **cannot answer this** — `hooks_armed` is `N/A — hub-only` for a consumer |
| win-tooling: **role=consumer**? | **NO — held at pre-deploy, measured** | the flip REDs `test_check_fleet_parity_green_on_live_repo`, whose docstring says *"promotion REDs nothing"*. Made, measured, **reverted** |
| win-tooling checks passing | **13 → 15** | `audit repo win-tooling`, before and after |
| win-tooling branches backed up | **11/11** (was 1/11) | 10 × `git push -u origin`, `git branch -vv` recorded in lane A's packet |
| **verbs exist?** | **YES, both** | `Harvest-Cloud` and `Dispatch-After` on win-tooling `main`. `Dispatch-After` is documented as *"a SCHEDULE around the three above — it owns a wait and then calls one of them unchanged"* — a **form of** the ruled Dispatch verb, never a rival, exactly as contracted |
| **validator armed?** | **organ YES, gate NO — by contract** | `scripts/preflight_contract.py --freeze` ships the four predicates + a CLI. Wiring it into a hook was **withheld** on purpose: arming a new pre-commit gate carries roster and doc consequences outside any lane's write-scope. Reported as a candidate filing, not smuggled in |
| **funnel gate RED-capable?** | **NO — FM-2 never ran** | wave 2 stopped at §2 |
| **FUNNEL HEALTH in bundle?** | **NO — FM-4 never ran** | wave 2 stopped at §2 |

**The validator's acceptance evidence, run tonight on merged `main`.** Batch-1's own frozen
contract, through `preflight_contract.py --freeze --predicates-only`, reproduces **all three**
architect premise errors of 2026-08-28 — and finds a **fourth** that batch-1's own retrospective
missed:

- **(i)** the `Basis:` clause *"names an input with NO locator — no path, no `[#id]`, no ADR.
  Nothing here can be opened, so nothing here can be confirmed to exist"* → premise error 1.
- **(ii)** six unwitnessed `verified`/`measured` claims, including line 142's *"Ratchet untouched
  (ecosystem/ + code are outside its scope roots — verified, not assumed)"* → premise error 2.
- **(iii)** `[#587]` — *"Liveness is not identity: two open rows in one theme, story and
  serialize-group are told apart by their title and nothing else"* → premise error 3, and the
  message names the general rule rather than the instance.
- **(iv)** **the fourth, previously unfound:** the contract claims the ratchet is untouched while
  *"its own write-scope names `templates/claude-regions/*.md`, which `silent_rule_detector._in_scope`
  puts INSIDE ratchet scope"*.

A gate that finds a defect its own commissioning retrospective missed is the only kind worth arming.

---

## 6 · FOUR CONTRACT-PREMISE DEFECTS CAUGHT AT FREEZE — before a single lane booted

Recorded in `docs/audits/2026-08-28-technical-batch-2-manifest.md`, repaired in no lane's contract
silently.

- **D-F1** — lane F's Intent restated *"9,161 B = 28.0 %"*. Measured: **9,430 B = 28.78 %**, because
  root `AGENTS.md` is **5,539 B / 107 lines**, not `CLAUDE.md` §2.68's *"103 lines, 5,270 B"*.
  `git cat-file -s 43c18e9f:AGENTS.md` == **5539** against the file's **only** content commit.
  **Still owed:** §2.68's figures are false in a canonical doc and were not corrected — that is a
  `CLAUDE.md` write outside every lane's scope, and the file sits at 196/200 of its budget.
- **D-B1** — *"the paginated events loop already exists ~line 1079"* is false: that is a
  **receipt-polling** loop, and `next_cursor` appears **nowhere** in the module. Harvest-Cloud was
  half new code, not an extraction.
- **D-B2** — the cp-defect line numbers (1279/1282/1402) point at **comment blocks**; the live argv
  arrays are at 1591/1637/1669.
- **D-M1** — the launch-contracts home has an **implicit schema nothing documents**: every `*.md`
  in it is parsed as a lane contract. The first commit **REFUSED** on `substrate-no-live-verb`,
  which FAILs `audit-health` and would have blocked **every commit in every lane, all night**.

**And a fifth, caught by the naming validator rather than by reading:** the frozen bundle names its
lanes `N1..N8`. `validate_branch_naming --lane` requires `lane-<letter>-<id>-<slug>` and returns
**BAD** for every `N<n>` form — so all seven would have merged **outside** `LANE_BRANCH_RE`, losing
the ADR-110 exemption, and the queue would have wedged at the first conflicted merge. Names were
derived from the validator, not from the bundle (STANDING_RULINGS F2). N1..N8 → lanes A..G.

**This is the class lane G now refuses mechanically.** The four freeze-time predicates exist
because of three of these; tonight produced two more of the same shape before the predicates were
merged. The next batch can run its own contract through `preflight_contract.py --freeze` at freeze
time instead.

---

## 7 · WHAT IS OWED, AND TO WHOM

Full detail in `docs/audits/2026-08-29-technical-night-harvest-consumption-ledger.md`. **Every
disposition there is a CC derivation awaiting a ruling, never a ruling** — tonight had zero
operator contact by design, and technical questions are the architect's (ADR-108 §A).

**The one item with a live clock — C5 in the ledger.** `docs/intake/README.md` is **fresh and
wrong**: six live intakes (ids **56–61**) render `[MISSING-ID]` inside an off-enum `### OTHER (6)`
group, and the index says `READY (13)` while disk has **19**. Root cause reproduced: an unquoted
backtick opening a YAML scalar on the `consumers:` line, **line 5 column 12, identical in all
six**; `_parse_frontmatter` returns `{}` by design. **The `intake-index-freshness` gate cannot see
it** — regen-and-diff reproduces the wrong output byte-for-byte. A freshness gate is a **currency**
check, not a **correctness** check. The fix is six quoted strings; it was **not** done tonight
precisely because "six quoted strings" is how unscoped work starts.

**The rest, by owner:** ratchet-headroom policy · the SDA-1 admission instrument (three candidates,
one intake) · the tile manifest (joins intake #59) · `intake-id: 14` assigned to three files ·
`tasks/` rows carrying **no `source:` field at all — 0 of 344**, so the funnel doctrine and FM-2's
FAIL-leg (c) are both written against a field that does not exist (`· refs …` is the de-facto one,
**153 of 153** open rows carry it) · the README/VISION 5-line merge · `funnel_coverage` being
non-recursive · the launch-contracts implicit schema · ADR numbering gaps · `[#598]`'s dead
`conftest.py` locator. **Three intake docs are archivable behind an operator status ruling** —
#19 (strongest), #26, #28 (with a caution: ADR-112 says fourteen of #28 §C's candidates are still
actionable).

**Two closure candidates, reported not filed:** `[#577]` and `[#584]` are still `open` on `main`
although batch-1 landed their work and lane F discharged `[#577]`'s done-when **5 of 5 clauses**
tonight. Closure is `/review-closures`' call.

---

## 8 · METHOD FINDINGS — about the instruments, not the corpus

- **The cloud clone is SHALLOW.** `.git/shallow` exists, history starts 2026-08-23, 340 commits
  over 7 dates. `git log --diff-filter=A` returns the **graft boundary** for **835 of 951 objects
  (87.8 %)**. Only 116 have a trustworthy git birth date there. **Any cloud brief asking for
  git-derived dates is asking for fiction** — a standing property of that substrate, not a
  one-night accident. FM-C used frontmatter and filename dates and reported `UNDATED (shallow
  graft)` rather than inventing.
- **A filename-keyed consumption graph has a measured ~42 % false-orphan rate.** FM-C's pass 1
  produced 19 orphan intakes; identifier keying cut it to **11**. The same graph mis-flagged 1 of 4
  archivable candidates. Both were caught by the report's own **self-audit clause** — which is the
  argument for keeping that clause in every brief.
- **An explicit output-shape clause fixed the byte-identity deviation for free.** 2026-08-27: 2 of
  4 reports opened with prose before their own heading and the deviation had to be recorded.
  Tonight: **6 of 6 start at byte 0 with their own heading.** One clause in the shared brief; no
  harvester change.
- **`audit.py repo <name>` reverts uncommitted working-tree changes.** Its scope restore is a real
  checkout. The first index regeneration of the night was silently undone by the win-tooling audit
  run that followed it; `--check` caught it, `git status` did not. Run `audit repo` **before**
  regenerating, never after.
- **One attribution error against a lane, recorded rather than repeated.** C2 states its brief's
  "WHAT TO GROUND IT IN" names `conftest.py`. It does not. The **substantive** half is true and is
  carried as a candidate: `[#598]`'s own `refs` list cites a file that exists nowhere in the repo.

---

## 9 · THE FULL SUITE, ONCE, ON MERGED MAIN — every failure attributed

`uv run --locked pytest -q` on `main` @ `b4ab25ab`: **6 failed, 4409 passed, 3 skipped, 1 xfailed,
777.60 s (12:57)**. **No test file in the whole suite was modified by this batch** — verified:
`git log fcc94855..main -- <each failing test file>` returns **0 commits** for all six. So every
failure is caused by an *input* that moved, never by an edited assertion.

| # | test | attribution |
|---|---|---|
| 1 | `test_consumer_at_landing::test_the_live_corpus_measures_and_the_baseline_matches_it` | **OURS, and self-clearing.** The night landed 18 audit artifacts; `ecosystem/audit-consumer-baseline.json` was **not** touched (0 commits). These artifacts' declared consumer is **this packet** — the same pattern batch-1's manifest recorded — so §10 names every one of them and the finding resolves on landing rather than by widening a ratchet. **A blanket baseline regeneration was deliberately not done:** it would silently accept 18 unconsumed artifacts, which is exactly what the ratchet exists to refuse. |
| 2 | `test_funnel_coverage::test_committed_baseline_agrees_with_a_live_measurement` | **OURS, same cause, same resolution** — `ecosystem/audit-funnel-baseline.json` untouched (0 commits) against a corpus that grew. |
| 3 | `test_enforcement_coverage::test_anchor_gate_probe_distinguishes_installed_from_absent` | **PRE-EXISTING — not this batch.** RED on `main` since **2026-08-22**; neither the test nor the organ it probes was touched (0 commits). |
| 4 | `test_export_backlog_view::test_no_gate_hook_or_script_reads_the_export` | **PRE-EXISTING — not this batch.** *"`ecosystem/conformance.html` references `export_backlog_view`"*: `ecosystem/` lacks the naming-vs-reading carve-out the check applies elsewhere, so a **mention** reads as a **read**. Nothing tonight regenerated the dashboard (0 commits on the test, none on `conformance.*`). |
| 5 | `test_desired_state_report::test_live_report_renders_the_real_fleet` | **OURS — lane A.** *"Left contains 2 more items, first extra item: `terminal-setup`"*: lane A's `[#604]` fold added `terminal-setup` to `ecosystem/deployed-versions.yaml` (**1** commit in range), and this test pins the fleet as a **literal**. Lane A hit the same shape in `test_desired_state_loader.py` and fixed it properly — commit `a3f7c668`, *"derive the live fleet-membership pin instead of pinning a literal"*. It did **not** reach into this sibling test, which is outside its frozen write-scope. **The fix is known and is one commit's worth of the same change.** |
| 6 | `test_validate_doc_rot::test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | **PRE-EXISTING, and tonight IMPROVED it.** The test asserts **zero** accretion findings. The dispatch-time run recorded accretion findings against `#146`, `#277`, `#171`, `#267`, `#297` **before any lane booted** — so it was already RED. Now **4** remain (`#267`, `#297`, `#82`, `#276`): lane D drained `#146`, `#277` and `#171`. The arm is smaller, not newly broken. |

**Two ours-and-self-clearing, one ours-with-a-named-one-commit-fix, three pre-existing.** Nothing
tonight broke a test that was green.

---

## 10 · ARTIFACT INVENTORY — what this packet consumes

This section is the **consumer declaration** `[#595]`'s consumer-at-landing rule asks a landed
`docs/audits/` artifact to carry. Every artifact this batch produced is named here, which is what
makes finding #1 in §9 resolve on landing.

**The dispatch record** — `docs/audits/2026-08-28-technical-batch-2-manifest.md` (the gate-readable
key this packet closes) · `docs/audits/2026-08-28-technical-batch2-launch-contracts/` (13
dispatchable contracts: `NB2-LANE-{A..G}-*.md`, `NB2-CLOUD-{C1..C5,FMC}-*.md`) ·
`docs/audits/2026-08-28-technical-night-mission-authorization.md` ·
`docs/audits/2026-08-28-technical-night-batch2-frozen-bundle.md` ·
`docs/audits/2026-08-28-technical-fm-wave2-frozen-bundle.md`.

**The cloud harvest** — `docs/audits/2026-08-29-technical-night-harvest-manifest.md` ·
`-technical-night-harvest-consumption-ledger.md` · `-technical-nb2-candidate-triage.md` (C1) ·
`-technical-nb2-slow-marker-evidence.md` (C2) · `-technical-nb2-intake61-ratification.md` (C3) ·
`-census-nb2-codex-surface.md` (C4) · `-census-nb2-readme-vision.md` (C5) ·
`-census-nb2-funnel.md` (FM-C).

**The lane packets** — `docs/audits/2026-08-28-technical-nb2-{a,c,d,e,f,g}-packet.md` in the hub;
lane B's is `docs/2026-08-28-nb2-lane-b-packet.md` in **win-tooling**, because a consumer-repo lane
cannot write to the hub.

---

## 11 · THE ORGAN BUILT TONIGHT, DOGFOODED ON TONIGHT'S OWN OUTPUT

Lane G's freeze predicates were run over **this mission's own eight wave-2 contracts** before they
were left for you. That is the organ's first real use, and it earned its place twice and cost
something once — all three reported rather than smoothed:

**It found a defect in the architect's own frozen text.** `register R3` — cited in FM-WAVE2 §A4-AGY
as *"per R3/A4"* — **does not resolve**: there is no `### R3` heading in `STANDING_RULINGS.md`. In
this repo `R3` means **`[#483] R3`**, a ruling scoped to a *backlog row* and written
`PERMANENT per [#483] R3` (`STANDING_RULINGS.md:69`, `:73`, `:178`). Resolved in an addendum
beneath the quote rather than by editing the quote.

**Two false positives, and both name a real limit of the predicate:**

- **Predicate (i) does not expand globs.** It FAILed `~/.gemini/antigravity-cli/log/cli-*.log` as
  *"does not exist at freeze"*. Measured: that directory holds `cli-20260820_133326.log` and
  siblings. A legitimately glob-shaped off-repo reference reads as absent.
- **Predicate (iii) cannot tell a dispatch target from terminal-state evidence.** It FAILed
  `[#446]` as *"resolves to a CLOSED row … a contract cannot dispatch work against it"* — but the
  citation exists **precisely because** the row is closed: that is what makes intake #19 the
  strongest archival candidate. An archival contract is made almost entirely of that second kind
  of citation.
- **And predicate (ii) fires on instructions, not only assertions.** Across the eight contracts it
  produced ~35 `unwitnessed-claim` FAILs, and the great majority are the contract *telling the lane
  to measure something* (*"pick a library by measured fit"*, *"verify the output bytes after
  regenerating"*) rather than *claiming something was measured*. On batch-1's contract the same
  predicate was almost all true positives, because that contract's `verified` words were
  assertions. **Precision is therefore document-mode-dependent**, which is the trade lane G's
  contract asked it to state and which only a second corpus could reveal.

**All four are candidate filings against `[#591]`, not repairs.** The organ is not wired into any
gate — deliberately, by its contract — so nothing is blocked by any of this, and the operator can
rule on precision before it ever fires at commit time.

---

## 12 · SEAT LESSONS — appended verbatim, and witnessed

The mission required the five SEAT LESSONS appended to `LESSONS.md` **verbatim** before this
packet. Done, and checked rather than asserted: each of the five bullet texts was matched
**byte-for-byte** against the file after the append — `L-S1..L-S5: VERBATIM PRESENT`, 5 of 5.
`LESSONS.md` goes **310 → 315** entries; the file is append-only, newest-first, and sits **outside**
the silent-rule ratchet's scope roots (`protocols/*.md`, `templates/**`, `ecosystem/*.yaml`), which
is why a five-entry append costs the ratchet nothing.

Each lesson carries its `action taken` field pointing at what mechanized it **tonight** — L-S1 to
lane G's predicates (and to the fourth defect they found that batch-1's own retrospective missed),
L-S2 to lane C's five-phase protocol, L-S3 to predicate (i) and its first live catch, L-S4 to the
consumption ledger's derivation-not-ruling stance **and to the wave-2 stop decision**, L-S5 to §1
of this packet.

**Standing note, unchanged by this append:** `LESSONS.md` is past its ratified 300-entry split
trigger (**315**), and nothing has fired. That was already recorded on 2026-08-27 at 303.

---

## 13 · THE ONE-LINE DECISIONS WAITING FOR YOU

1. **Boot wave 2, or not.** Eight contracts are frozen, dry-run clean and locator-checked. The only
   thing between them and running is §2. *"W1-2 partial is accepted, boot wave 2."*
2. **Flip win-tooling's parity role, or rule the divergences first.** Lane A held it and recorded
   why; the divergence list is in its packet.
3. **`docs/intake/README.md` is fresh and wrong** (six intakes, ids 56–61). Six quoted strings fix
   it. It was left alone on purpose.
4. **Three intake docs are archivable behind a status ruling** — #19, #26, #28.
5. **Verify the cp-quote fix**, now that it has a reproduction: run
   `Apply-DispatchHelpers.ps1`, then re-fire the smoke-6 probe.
6. **Delete the stopped codespace** `nb2-smoke6-g5rvj4w6qx4hv5q4`, or let its 24 h retention do it.
7. **`[#577]` and `[#584]` are closure candidates** — lane F discharged `[#577]`'s done-when 5 of 5.

---

## AMENDMENT 1 — 2026-08-29, added in-file after this packet's first commit (`04f32784`)

> `docs/audits/` is immutable and is amended by an **in-file amendment marker**, never edited in
> place (CLAUDE.md §5 rule 3). Everything above stands as first written; this section corrects two
> of its claims and is the sanctioned form of that correction.

### The two corrections

**C-1 — §9 finding #1 was over-optimistic, and the gate caught it, not me.** I wrote that the
`consumer_at_landing` failure would *"resolve on landing"* because §10 names every artifact. That
is only half right, and the half it gets wrong is the half that matters:
`check_consumer_at_landing` measures **two** things — *declaration* (does the artifact itself
declare a consumer) and *consumption* (does a governance surface cite it, **against a committed
identity baseline**). §10 fixes consumption. It does **not** move
`ecosystem/audit-consumer-baseline.json`, which is what
`test_the_live_corpus_measures_and_the_baseline_matches_it` compares against — and that baseline
is regenerated only by an explicit `--write-baseline`, never as a side effect of measuring.

**So findings #1 and #2 in §9 do NOT self-clear.** They clear when the operator (or a ratified act)
regenerates the two baselines, which is an **acceptance** act — it says *"these artifacts are
admitted with the consumers now declared"* — and that is exactly why it was not done unattended.
The measured position is recorded here rather than left for the next seat to discover.

**C-2 — the close commit was REFUSED once, on a real defect of this packet's own making.**
`consumer_at_landing` FAILed the smoke-6 probe contract: *"landed on/after 2026-08-27 and declares
no consumer"*. It was a genuine miss — the probe is a one-shot artifact and I had committed it with
no declaration. Fixed the way the gate asks: the file now names
`docs/audits/2026-08-29-verification-night-mission-close-packet.md` §3 as its consumer, which is
true — this packet is what reads its result. **No baseline was widened to get past it.** After the
fix the check reports **0 FAILs**.

**And the diagnosis cost a repeat of a known trap.** The first attempt at this commit was run as
`git commit … | tail -6`, so the shell reported the **pipe's** exit code (0) while the commit had
actually failed, and the six lines kept were the harmless tail rather than the `[!!]` line at the
top. The second attempt wrote the full hook output to a file and the blocker was one `grep` away.
`| tail` on a gated command hides both the verdict and the reason.

**Both corrections are MEASURED, not predicted.** After `04f32784` landed the packet, the two
tests were re-run: `test_the_live_corpus_measures_and_the_baseline_matches_it` and
`test_committed_baseline_agrees_with_a_live_measurement` **both still FAIL** — which is what
C-1 says they would, and the opposite of what §9 first claimed.
