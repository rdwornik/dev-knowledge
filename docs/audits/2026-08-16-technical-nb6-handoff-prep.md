# NB6-D handoff prep — residual, drift flags, pending words, and the next-window arc map

> **STATUS: DRAFT — INPUTS ONLY.** This file drafts the *inputs* to a HANDOFF_PROCESS v6
> supplement. **The architect authors the real supplement.** Nothing here is a ruling, a
> disposition, a closure or a schedule. It births no row, edits no gate, and moves no date.
> Where a lane's own words are load-bearing they are quoted and attributed rather than
> paraphrased.

- **Class:** technical (ADR-101 R3 enum) · **Date:** 2026-08-16 · **Slug:** nb6-handoff-prep
- **Lane:** NB6-D, branch `claude/nb6-handoff-prep-report-liifks` — Anthropic cloud session, read-only
- **Base:** `origin/main` @ `88422f5c` ("Merge branch 'docs/batch6-close' — batch 6 closes")
- **Shape:** HANDOFF_PROCESS v6 §2 — *the residual is what CC emits, not a re-transmission*

---

## 0. Measurement environment — read this before reading a number

This lane ran in an Anthropic cloud container. Two things were done to make its numbers
comparable to the operator's host, and both are stated because a number whose environment is
unstated is not evidence.

```
git rev-parse --is-shallow-repository  ->  true   (at boot; 290 commits)
git fetch --unshallow                  ->  false  (5174 commits — full first-parent history)
uv run --locked ...                    ->  error: Required uv version `==0.11.19` does not
                                              match the running version `0.8.17`
python scripts/audit.py health         ->  ModuleNotFoundError: No module named 'click'
pip install --target <scratch> click pyyaml markdown-it-py rich
PYTHONPATH=<scratch> python scripts/audit.py health  ->  RAN. health: DEGRADED
```

**What that buys, and what it does not.** The unshallow makes every history-dependent check
(`no_ff_merges`, `git_backlog_drift`, `journal_spine_anchor`) reproduce for the first time in a
cloud lane — the night-3 ledger had to cite those from a packet rather than measure them. The
dependency-side route makes the organs runnable **without** the `uv` pin. What it does not buy:
the interpreter is **3.11.15** against a `.python-version` pin of **3.12.10**, and the hooks are
unarmed. So this is a **corroborating** reading, not a sanctioned one.

**Two checks still cannot see the operator's tree**, and both are named in §1 rather than
silently absorbed: `stale_worktrees` passes vacuously here (no linked worktrees in this
container; the operator has **12**), and `fleet_parity` walked 0 of the 2 sibling repos.

---

## 1. RESIDUAL — everything open with an owner at window end

Eighteen items. Each names an owner, a state, and what would move it. Ordered by owner, not by
severity.

### 1a. The suite — 2 owned REDs, both ruled

```
uv run --locked pytest -q --dist worksteal --max-worker-restart=0
2 failed, 2968 passed, 3 skipped, 1 xfailed in 1473.52s   (integrator's run, JOURNAL 2026-08-16 (d))
```

**R1 · `test_routine_consumers_live_backlog_governs_exactly_one_row`** — owner **batch-7 lane
`l`** (`[#348]` family). Deferred by ruling **D-1v2**, so nothing on batch 6's roster could have
cleared it. The batch-6 contract's *"0 RED is then the expectation"* was conditional on a lane
that did not run; 1 was always the right expectation for that roster.

**R2 · `test_live_corpus_has_no_accretion_arm_findings_only_length_findings`** — owner **lane x
/ `[#532]`**. `doc_rot` ARM 1 fires correctly on `BACKLOG#428` (3 dates spanning 52 d, 2030
chars) — lane h's row after its D6 locator correction. **The detector is right; the pin is a
live-corpus assertion that a ruled edit changed.** It was deliberately *not* relaxed, because
relaxing it deletes the evidence that ARM 1 works. Two exits exist and neither is chosen here:
condense `#428` (which is what the WARN asks for), or re-scope the pin off the live corpus.

**R3 · The third apparent RED is ENVIRONMENTAL and is NOT dispositioned.**
`test_finding_headline_resolves_with_provenance` fails at 16 xdist workers (`assert 3 >= 50`)
and **passes serially** — the pyright oracle returns partial results under contention inside its
40 s timeout. The batch recorded this rather than triaging it. **It has no owner, no row and no
register entry**, which means the next full-suite run at width will re-surface it as an unknown.
That is the residual: not the failure, the absence of a disposition for it.

### 1b. The WARN ledger — 47 on the operator's host, reconciled live

Measured live this lane at `88422f5c`:

```
audit.py health     ->  52 WARN · 0 FAIL-class findings · health: DEGRADED
audit.py ship-gate  ->  RED — 1 hard-fail organ · 26 dispositioned · 26 undispositioned
                        + 2 [stale] register entries matching no live WARN
```

**Five of the 52 are container artifacts, established by mechanism rather than assumed:**

```
fleet_parity                  x4   ai-council + corp-monorepo absent (not git repos here);
                                   hooks-not-armed probe; pytest-xdist absent from the interpreter
deployed_methodology_version  x1   the check keys on the repo-ROOT BASENAME. The registry
                                   ecosystem/deployed-versions.yaml:25 holds `.dev-knowledge`;
                                   this clone's root basename is `dev-knowledge` (no dot),
                                   so the lookup misses. Host-side it resolves.
                              ---
52 - 5 = 47  ==  the figure the brief carries. Independent arrival, same number.
```

**R4 · The 47, by owner.** The dispositioned/undispositioned split is what actually gates:

```
DISPOSITIONED (26) — ship-gate clears these, health still prints them
  undeclared_edges        18   ref #241 — 18/18. The declare-vs-defer adjudication is [#241]'s.
  no_ff_merges             3   immutable June history; unfixable without a rewrite. NEVER revisit.
  review_artifact_coverage 2   387b794a (D1.7, already dispositioned) + 5af0b33c (no Tally line)
  reconciled_versions      1   templates/CONTRIBUTING-md-template.md:3 — a template placeholder;
                               the fix is a detector carve-out for templates/*-template.md
  journal_spine_anchor     1   advisory SHAPE leg, WARN by ruling (STANDING_RULINGS L-10)
  git_backlog_drift        1   #505 closed-but-present — dies when [#505] leaves BACKLOG

UNDISPOSITIONED (21 host-side, 26 here) — THE BLOCKING SET, and it is ONE CLASS
  doc_rot                 21   19 backlog-row-length + 2 backlog-accretion
  (+ fleet_parity 4, deployed_methodology_version 1 — container-only, see above)
```

**The whole blocking set is `doc_rot`, and it is 19 rows.** Listed by row so the campaign can
cost it, ceiling 1320 chars:

```
#533 4210   #293 2864 (+accretion, 4 dates / 40d)   #514 2420   #528 2397   #417 2360
#531 2067   #428 2030 (+accretion, 3 dates / 52d)   #277 2006   #529 2001   #530 1871
#523 1738   #492 1807   #502 1390   #412 1389   #484 1374   #443 1370   #271 1364
#361 1331   #146 1323
```

**Ownership reading, stated as arithmetic:** **8 of the 19** are rows born or heavily edited in
the last two batches (`#533 #531 #530 #529 #528 #523 #514 #502`), and `#533` alone is **3.2× the
ceiling**. The ledger is not a legacy-debt list — it is largely **this fortnight's own output**,
which is the same self-demonstrating shape the batch-6 Position-0 arc recorded when `doc_rot`
went 7 → 9 on the two rows born to fix it.

**R5 · Two `[stale]` register entries** matching no live WARN — `warn-preflight-backlog-ids-310-292`
(the `[#310]`/`#292` fix landed, so the disposition is orphaned) and
`warn-review-artifact-d62796ad-boot-acts`. ADR-75's decoration rule says review/remove. Owner:
whoever next touches `ecosystem/disposition-register.yaml`.

### 1c. `[#533]` — the decomposition, PARTIAL by design

**R6 · Class 1 — the 27 held checks.** `scripts/audit_checks/` exists with an ordered
`CHECK_ORDER`; `audit.py` went 5243 → 4270 lines; count and order preserved at 43; `health`
output byte-identical on every line the refactor can reach. **16 of 43 extracted, 27 held in the
facade under the Done-when's own escape clause** — which is the contract's success condition,
not a shortfall. The blocker is measured: **a test monkeypatches a name in the check's closure
onto the `audit` module — 25 checks, `_is_hub`/`_REPO_ROOT` alone 19 — and moving one detaches
the seam SILENTLY, so the check would pass while asserting nothing.** Owner: **batch-7 lane
`l`/`y`**, via the ruled follow-on leg (re-point the `tests/test_audit.py` monkeypatch seams;
that file was read-only to lane m).

**R7 · Class 2 — `_gitenv` position-dependent path load (`check_handoff_probes`). A SEPARATE
RULING ITEM**, deliberately not folded into lane m's seam leg.

**R8 · Class 3 — a declared landing predicate names `scripts/audit.py` for a symbol the check
owns** (`check_import_edges` vs `STANDING_RULINGS` N-1's `from markdown_it import MarkdownIt`
site). **Also a separate ruling item.** Found by running the gate, not by reading the code —
worth carrying, because it is the class of defect that only a live gate surfaces.

**R9 · Leg 2 — parallel check execution.** Appended at source, batch-7-scoped, precondition met
by lane m's merge. **The executor question is already answered by measurement**: `audit.py
health` is **I/O-bound** (~2 min CPU per ~5 min wall at 8 % load, measured during the batch-6
merge queue), so the ruling's condition for `ProcessPoolExecutor` is **not met** and
`ThreadPoolExecutor` is indicated. Includes the NB3-D-measured `journal_anchor` memoization
(~42.7 s → ~17.8 s per commit).

### 1d. Rows blocked on a word or a date

**R10 · `[#293]` — BLOCKED-ON-RULING.** Lane k executed operator-authorised cross-repo seeding
(7 of 8 consumers, PRs opened), then kept auditing, found that `[#303]` + ADR-60 + the
2026-07-08 census amendment **all forbid a child repo carrying a local `docs/handoffs/`**, and
**reverted all seven PRs**. Independently verified at integration: all CLOSED, `mergedAt=null`,
zero open PRs, all 7 branches deleted, all 7 consumer repos back to clean. **Net change in every
consumer repo: zero.** Content preserved verbatim in the lane-k packet appendix. The open
question is the *correct consumer-side home*; two candidate homes are named in existing
governance and **no path was invented**. `[#303]` is the row's own prerequisite and must land
first. NB4-F reaches the same place independently and adds: **seeding-ready 0 of 8 on two
independent grounds, either alone sufficient** — 5 have no reachable remote, all 8 are blocked
on content.

**R11 · `[#492]` — the re-check falls due TOMORROW, 2026-08-17.** The row's own
`EVIDENCE 2026-08-10` line records Grok 4.6 unreleased (browser-verified), peg unmet. **NB4-A
reports the peg is now MET — Grok 4.6 released 2026-08-12, with both legs the row names (model
card, API id) now existing.** NB4-A states its own limit before using the claim: the first-party
card and `docs.x.ai` are **EGRESS_BLOCKED** from its container, so the finding is corroborated
across secondary sources — *"one grade weaker than the browser verification the row itself
used"*. **NB4-A's own recommendation:** run the 2026-08-17 re-check in a browser anyway, *"but
it should be run expecting to lift the peg."* NB4-E independently classes `[#492]` NEEDS-ACT
with the same date. This lane did **not** attempt to re-verify the release.

**R12 · `#371` is left UN-RULED** — carried explicitly, as the batch-6 wrap ledger §A10 requires
the record to say.

**R13 · `[#428]` condense-or-rescope** is the operator's call and is the single thing standing
between the tree and a clean suite (it is R2's subject and a `doc_rot` accretion locus).

### 1e. Machine-local state — the part a fresh clone cannot see

**R14 · Teardown was NOT run in this arc.** Twelve worktrees and twelve lane branches are
intact; `git stash list` empty. `git branch -d worktree-lane-e-82-conversions` **will REFUSE by
design** — its held tip `f5c5e9dd` is a lane-authored `JOURNAL.md` entry that was deliberately
not merged (a batch lane never journals, and holding it also averted a duplicate-letter
collision on `(d)`). **That refusal is reported, never forced with `-D`.**

> **VERIFIED LIVE, AND IT SHARPENS THE ITEM: `f5c5e9dd` DOES NOT EXIST ON `origin`.**
> `git cat-file -t f5c5e9dd` → *"Not a valid object name"* against a full-history clone, and
> `git ls-remote --heads origin` carries **none of the twelve `worktree-lane-*` branches** —
> only their `--no-ff` merges reached `main`. So the held tip, the twelve worktrees and the
> twelve lane branches exist in **exactly one place on earth**, with no remote copy. The
> teardown is not merely owed; **the content it is holding is unbacked.** Nothing here proposes
> pushing it — that is a decision, and the ruling that held it was deliberate — but a successor
> reading "teardown owed" from a fresh clone will find nothing to teardown and should not
> conclude it was done.

**R15 · Ten cloud report branches on `origin` await land-then-delete.** Measured live against
`origin/main` @ `88422f5c` (the earlier shallow state gave wrong ancestry; these are the
full-history numbers):

```
branch                                        ahead  behind  report file
claude/nb4-llm-acceptance-benchmark-pnoo2q      1      60    technical-nb4-llm-acceptance.md
claude/nb4-telemetry-read-path-ivoka2           1      60    technical-nb4-telemetry-read.md
claude/nb4-playbook-gap-coverage-1ktsuc         1      60    verification-nb4-playbook-gap.md
claude/adr-104-fleet-parity-audit-f1lr7a        1      60    technical-nb4-fleet-parity.md
claude/nb4-closing-campaign-prep-gb68l0         3      60    census-nb4-closing-campaign.md
claude/nb4-equilibrium-audit-el1o0w             3      60    verification-nb4-equilibrium.md
claude/nb4-consolidated-ychsah                  2      56    technical-nb4-consolidated-briefing.md
claude/nb4-scaleout-substrate-f8fhi1            4      56    technical-nb4-g-scaleout-substrate{,-v2}.md
claude/nb5-seam-repoint-analysis-lmaspu         1      56    technical-nb5-seam-repoint.md
claude/consumer-home-adr60-audit-xd341y         1      56    technical-nb5-consumer-home.md
```

**Every one touches exactly its own report plus the generated `docs/audits/README.md`** — so the
only merge conflict class in the whole set is the generated index, which resolves by
**regeneration** (`gen_audit_index.py --write`), never by picking a side. That is the same
resolution the 2026-07-31 arc recorded, and it is the reason this set can be landed in one pass.

> **A CORRECTION TO THE BRIEF, stated because a residual that carries a wrong denominator is
> worse than none.** The brief names *"night2/nb4/nb5/nb6 branches on origin"*. **There are no
> `night2` (or night-3) branches on `origin`** — those artifacts already LANDED, at JOURNAL
> `2026-08-15 (d)` (5 night-2 UNIQUE-HOLD artifacts) and `2026-08-16 (a)` (5 night-3 lane
> reports, byte-faithful). The live set is **10 branches: 8 NB4-family + 2 NB5-family**, plus
> this lane's own. Two of them are topic-named rather than `nb`-prefixed
> (`adr-104-fleet-parity-audit`, `consumer-home-adr60-audit`) and would be missed by a
> name-prefix sweep — which is exactly how a land-then-delete pass leaves orphans.

**R16 · `automation/fleet-audit` is a STANDING KEEP, not a residual.** 171 commits, **no merge
base with `main`** (unrelated root — the nightly routine lane's own history), tip
`chore(routine/fleet-audit): record 2026-08-16 baseline`. It is kept by standing ruling and must
not be swept up by a land-then-delete pass that reads "unmerged branch" as "orphan".

**R17 · NB6 sibling lanes are NOT on `origin` as of this writing.** `git ls-remote --heads
origin` carries exactly one `nb6` ref — this lane's. **NB6-C (the archival mechanism) is
referenced by the brief and its report is not visible from here.** Recorded so the successor
does not read its absence as cancellation, and does not read this file as the complete NB6 set.

### 1f. Owed from the batch-6 wrap, each with its stated reason

**R18 · Three items were named OWED rather than done, and none was half-performed:**

```
D3.1-D3.5 promotions   ruled "at close-out"; no close-out occurred
ARCHITECTURE.md:427    "four sub-detectors" -> five. Freshness-gated at 1020 lines, and one word
                       does not justify a review stamp the arc had not earned
[#415] / [#425]        identical Form-E predicate defect; VERIFIED rather than edited,
                       which is the ruling's own verb for them
```

---

## 2. DRIFT FLAGS

Eight. A flag is a *class* that has demonstrated itself, not an instance.

### F1 · The stale-denominator class — it bit TWICE in one window

**Bite 1 — same number, different set.** NB4-E measured 196 live rows; the census reported 196.
Reporting that bare reads as *nothing moved*, and **8 rows changed identity underneath it**:

```
census 196  -  4 closed (#352 #364 #524 #527)  +  4 born (#529 #530 #531 #532)  =  196 live
```

NB4-E's rule, carried verbatim as the reporting contract: *"a closing-campaign report cites the
live count measured at the commit it reports against, names that commit, and reports closed and
born separately — never a bare net, and never the census's 196 as a standing figure. A net of
zero is the outcome of 4 and 4; it is not the observation."*

**Bite 2 — and this one found a real defect.** At integration the arithmetic said 196 and the
live measure said **197**. Chasing that single-unit gap is what surfaced F2. Had the integrator
trusted the arithmetic, the defect ships silently.

**Live at `88422f5c`, measured this lane:** `grep -c "^- \[#" BACKLOG.md` → **196**. The
denominator is 196 and not the anticipated 195 because `[#533]` was born mid-arc.

### F2 · Manifest-coherence ≠ correctness — the resolver class

The merge resolver treated `tasks/manifest.json` as a generated file and took `--ours`, silently
discarding lane x's node removal and **reverting the ruled close of `[#532]`** — so `main`
carried the row OPEN while its own merge commit said *"closes [#532]"*.

> **No gate caught it. `gen_task_tree --check` passed throughout, because node-present +
> `status: open` is an internally COHERENT pair. Coherence is not correctness.**

Repaired at `3def2821`. **The corrected resolver now compares node lists and REFUSES rather than
choosing — and caught a real case on its first use, at lane k's merge**, then again at m. The
open half is the **detector gap**: nothing compares the task tree against its own history.
`gen_task_tree --check` needs a *closed-in-history-vs-open-in-manifest* leg. Candidate, not
filed.

### F3 · The ADR-110 exemption evaporates at closure — verbatim, because the mechanism is subtle

From `docs/audits/2026-08-16-technical-batch-6-packet.md`:

> *"**Closes:** `docs/audits/2026-08-16-technical-batch-6-manifest.md` (its declared `closed_by`).
> Committing this file expires the ADR-110 declared-integration-arc exemption automatically, with
> no edit anywhere."*

And the trap it sprang, from JOURNAL `2026-08-16 (f)`:

> *"`audit-health` is a PRE-COMMIT gate and `journal_spine_anchor` reads the spine, so an
> unanchored `fix/` merge (no ADR-110 exemption, unlike a lane merge) turned health DEGRADED —
> which in turn failed two `test_audit.py` tests that invoke `cmd_health` against the real repo
> and expect exit 0. Those two looked like a lane-m regression and were not: they were this
> arc's own missing anchor. The gate then blocked the very commit that would supply it."*

**The general shape:** committing the closer retroactively re-scopes what every already-merged
lane commit needs. Resolved by landing the anchor **in the same commit** as the packet rather
than reaching for `SKIP=` — which stays unused across the whole batch. Also from (f), the reason
lane k's anchor had to move: *"a merge cannot name its own hash, which is what makes a
journal-only wrap merge unanchorable."*

### F4 · The doubled-prefix dispatch defect — repaired, and the PLAYBOOK now carries the witness

`--worktree` takes the **bare** lane name and the provisioner prefixes `worktree-` **exactly
once**. A hand-assembled dispatch line passed the intended *branch* name as the `--worktree`
value, so `worktree-lane-a-409-conversions` produced
`worktree-worktree-lane-a-409-conversions`, **uniformly across all twelve lanes**.

**Nothing surfaced it at dispatch:** the pre-dispatch grammar check had validated the *intended*
names rather than the ones git created, so the manifest's "zero refusals" claim was false —
`batch_manifest.is_lane_merge` matched **0 of 12** and the ADR-110 exemption silently did not
apply. Found by lane x, corroborated by k and m; **lane x declined to self-fix because "the
exemption is the integrator's surface, not a lane's."** Repaired by uniform rename; **12 of 12
pass**, verified live on the first merge; withdrawn in the manifest's AMENDMENT 2.

**Fix state, verified live this lane:** `protocols/PLAYBOOK.md:2093-2101` carries the witness
under *"The dispatch surface is `dispatch <file>`"*, naming the flag, the mechanism, the 0-of-12
cost and `[#531]` as the gate that refuses such a name at creation. **The doctrine leg is
closed; the enforcement leg is `[#531]` and is OPEN.** NB4-C's row 2 is the standing indictment:
lane grammar is *"advisory and wired into no gate at all"*, `grep -n "worktree-lane-"
protocols/PLAYBOOK.md` → **0 hits**, and **three consecutive batches were damaged** (batch 4
dropped 2 lanes; batch 5 forfeited the exemption on 2 of 7 and hand-anchored; batch 6 reached
12/12 *by running every name through the regex by hand*).

### F5 · Organ executability in a cloud container — `[#453]` gap (2), now with a THIRD route

This lane is **at least the sixth live witness** in this window: `uv run --locked` refused with
the pin error, and every organ that shells through it — `audit.py`, the pre-commit stack, the
`Stop` backpressure hook — was inert on arrival. NB4-D's framing is the accurate one: *"not a
gate that says no, but **an organ that never gets to speak**, on the one surface that fires
unattended."*

**What this lane adds, and it is new evidence rather than a re-witness.** The NB4 briefing's
AMENDMENT 1 withdrew NB4-E's un-shadow remedy as container-local (no 0.11.19 binary exists on
these images, shadowed or otherwise) and left NB4-D's shape standing: the preflight must *"either
assert the pin and fail fast with a named reason, or obtain"* it. **A third route exists and was
executed here: bypass `uv` entirely for read-only organ runs** — `pip install --target` the four
imports (`click`, `pyyaml`, `markdown-it-py`, `rich`) and run `scripts/audit.py` under
`PYTHONPATH` with the system interpreter. Both `health` and `ship-gate` ran to completion and the
result reconciles to the expected host figure (§1b), which is evidence of fidelity rather than a
claim of it.

**Its honest limit, stated so it is not adopted by accident:** the interpreter is 3.11.15 against
a 3.12.10 pin, so this is fit for **read-only measurement in a cloud lane**, not for a gated
commit. It belongs in `[#453]`'s option set as a *measurement* fallback — a fourth cell in
NB4-D's table, not a replacement for the preflight.

### F6 · A WARN count silently changes with the clone's DIRECTORY NAME

New this lane, and it is the same family as F1. `check_deployed_methodology_version` keys the
audited repo by its **repo-root basename**, resolved via `git rev-parse --git-common-dir`.
`ecosystem/deployed-versions.yaml:25` holds `.dev-knowledge`; a cloud clone lands in
`dev-knowledge` (the leading dot dropped by the clone path), so the lookup misses and the check
fail-opens to a WARN.

**Why it is a flag and not a curiosity:** it costs **+1 WARN in every cloud lane, invisibly**,
and any lane that reports a raw health total without decomposing it will report a number the
operator's host does not produce. Two `night-3` lanes already tripped over the composition
problem in the other direction (*"the two 36s are not the same 36. Do not read the match as
agreement."*). **The general rule this suggests, offered not ruled:** a cloud lane reports WARN
totals **decomposed by check**, never bare.

### F7 · The Form-E predicate — partially repaired, and the defect is in the INSTRUMENT

NB4-E measured **spurious satisfaction**: the drafted Form-E clause (*"STANDING_RULINGS.md
carries a section naming `[#NNN]`"*) reads MET against `### L-8`, `### M-7` and `### H4` for rows
that carry no genuine ruling. Tested against all 12 Form-E rows: **a genuine ruling section
exists for ZERO of the 12.** NB4-E's framing: *"a conversion-instrument defect, not a row defect,
and it is cheapest to fix in the contract rather than after 29 clauses ship."*

**State, verified live:** batch-6 wrap act (vi) applied NB4-E's repair to `[#409] [#410] [#411]`.
**`[#415]` and `[#425]` carry the identical defect and were VERIFIED rather than edited** (R18).
So the instrument is repaired at three sites and the class is not closed.

### F8 · Wave 2 buys verdictability, not closure — the budgeting trap

NB4-E's most load-bearing finding, and it is a flag because it will mis-set the next campaign's
budget if carried wrong. All **29** dispatched wave-2 rows were tested against their own drafted
clauses and **not one reads MET**. Batch 6 converted exactly 29 rows (a:4 b:3 c:4 d:5 e:4 f:4
g:5) and **closed zero rows by design**.

> *"A campaign plan that budgets net closure against wave 2 will miss by 29."*

---

## 3. PENDING OPERATOR WORDS

Every item below is blocked on a decision, not on work. Grouped by what the word releases.
**Two are expired-by-integration and are listed anyway, because their outcome is now a fact that
needs recording rather than a choice.**

```
EXPIRED BY INTEGRATION (record the outcome; the choice is gone)
 W1  [#417] — convert via lane f, or propose closed?   Lane f integrated. NB4-E proposed
              NOW-CLOSABLE and explicitly did not close it. Done-when met on main (4bef950).
 W2  Form-E predicate repair before lane a integrates. Applied to #409/#410/#411 at wrap (vi);
              #415/#425 verified-not-edited. Outcome to record, plus the remaining class (F7).

LIVE, AND DATED
 W3  [#492] — the 2026-08-17 browser re-check. FALLS DUE TOMORROW. NB4-A: expect to lift the peg.
 W4  [#428] — condense or re-scope. Unblocks R2, and clears 2 of the 21 doc_rot WARNs.

LIVE, ROW-BLOCKING
 W5  [#293] — the correct consumer-side home per ADR-60. [#303] lands first; two candidate homes
              already named in governance; no path invented. NB4-F: gate lane k behind [#303],
              or re-scope the Done-when to docs/intake-only.
 W6  [#533] class 2 (_gitenv / check_handoff_probes) — a SEPARATE ruling item.
 W7  [#533] class 3 (N-1 landing predicate vs check_import_edges) — a SEPARATE ruling item.
 W8  #371 — left UN-RULED, carried explicitly.
 W9  The 25 NEEDS-RULING rows. NB4-E: "A quarter-day of rulings unblocks 25 rows — a larger
              change to the workable set than any close batch available." Its own collision
              warning: four of the 25 (#409 #410 #411 #491) are inside batch-6's wave-2 set, so
              the ruling batch and the conversion batch must not both claim them.

LIVE, ARC-SHAPING
W10  Intake #34 ratification. DRAFT BINDS NOTHING; the source artifact is operator-held and
              lands WITH the ratification, by ruling.
W11  The PLAYBOOK 12-act arc — any subset may be ruled; the one ordering constraint is that
              Act 8 points at Acts 9 and 10. Acts 2 and 11 REPLACE text (Act 11 also bumps
              version 1.0 -> 1.1, "the one act with a reconciliation consequence").
W12  The routing-table amendment. NB4-A: an OPERATOR act, not a session act — the canonical table
              is ~/.claude/ROUTING.md and #158 Decision B killed the resident copy. The in-repo
              alternative is named WITH its cost, not recommended.
W13  Batch-7 roster and its cap. l · y · 533-leg2 · harvest at width 4 => cap floor(4/4)=1,
              and 2 hub-process lanes are declared. OVER CAP BY ONE, stated as arithmetic.
              Three ways out on the record: widen to 8, fold 533-leg2 into harvest, or defer one.
W14  Land-then-delete for the 10 cloud report branches (R15) — and the standing keep for
              automation/fleet-audit (R16) restated so a sweep does not take it.
W15  Teardown of the 12 worktrees / 12 lane branches, and what happens to the held tip f5c5e9dd,
              which exists nowhere but the operator's machine (R14).
```

---

## 4. NEXT-WINDOW ARC MAP

Seven arcs. **Proposed, not scheduled.** Each names its precondition and its honest limit.
Batch 7 is the *vehicle* for several of these, not an arc in its own right — its roster is W13.

### A1 · The closing campaign — HEADLINER

NB4-E's C1–C7, carried as it specified them:

```
C1  RULING BATCH        window 3   25 NEEDS-RULING rows, one seat, ~quarter-day
                                   PRECONDITION: the Form-E predicate repair lands FIRST
C2  RATIFY + RE-PEG     window 3   #417 #506 close; #102 #181 #325 #492 re-peg   (rides C1)
C3  AUDIT-PY DRAIN I    window 4   width 8-10, S-class only, birth cap 2
C4  AUDIT-PY DRAIN II   window 5   + the 24 wave-2 rows batch 6 makes verdictable
C5  STRANDED + DEFERRED window 6   the 17 deferred LIVE rows read against their pegs
C6  M-CLASS BATCH       window 7   width 8, M-class, 1-2 per lane
C7  MEASURE AND REPORT  window 8   the L-3 evidence set: 2+ windows of net-closure data
```

**The finding the campaign must be built around** — measured over 19 days of first-parent
history: **closed 52 (2.74/day) · born 72 (3.79/day) · NET +20. The set is growing, not
shrinking.** Against §B clause 3 (*open backlog < 100*): 196 → <100 needs **net −97** over
L-3's 6 windows = **−16.2 per window**, and **the best window ever observed is −8**.

> *"Closure alone cannot reach the number, and the binding constraint is the birth rate, not the
> closure rate. **A closing campaign that does not carry a birth budget is not a closing
> campaign.**"*

**Two corrections the campaign inherits:** the denominator moved under the plan already (F1), and
**C3/C4's premise is now partly held by batch 6** — E shaped them around `audit.py` admitting one
lane per batch, and `[#533]` has since decomposed that monolith, so the drain batches can widen.
E could not know this; the ruling postdated its base by ~90 minutes.

### A2 · Enforcement intake #34 — filed as DRAFT, awaiting ratification

`docs/intake/2026-08-16-code-architecture-enforcement.md`, `intake-id: 34`, `status: DRAFT`.
Filed by batch-6 wrap act (iv) with the source artifact's TL;DR quoted **verbatim** (the
off-repo-claim convention). **The theme is the one six NB4 lanes converge on without any of them
naming it: organs that exist and gate nothing** — nine findings across five lanes, each with its
own locator and severity.

**Why it is next-window rather than later:** the intake names **import-linter module boundaries**
as *"the natural `[#533]` follow-on"*, and **boundaries cannot be enforced on a monolith.** A
decomposed tree is the first tree in which import contracts are expressible at all — so `[#533]`
landing is what opens this arc, and the window in which it landed is this one.

**Filing cost, stated because the gate will ask:** a new BACKLOG id needs a `kill-candidates:`
line (`backlog-filing-backpressure`), and an L-sized new-feature epic draws the advisory ADR-98
intake-id WARN.

### A3 · The `[#412]` measurement design — DESIGN ONLY, NOT STARTED

**The roadmap gate is discharged** (it scoped this *"after batch-4 closes"*, and batch 4 closed
2026-08-14), and the night-3 sessionplan independently ruled the leg *"a next-window headliner,
not a rider."* In batch 6 `#412` rode lane g as a Done-when **conversion**, which is not this
leg. **Nothing is started.**

**The design's whole point: the instrument already exists.** `telemetry_emit.py` is landed and
wires nothing, so *"the measurement needs no new store, no new dependency, and no new organ
family — it needs call sites."* Unit = a **dispatch**, keyed by branch name, denominator known
ex-ante from the manifest — *"the property that stops the measurement being reconstructed from
survivors."* Three fields with sources that exist today (`t_start`, `t_end`, `prompt_bytes`) and
a **pre-registered hypothesis** (does reducing a contract's authored byte-count change lane
outcome? — prediction: no effect on outcome, a reduction in authoring cost).

**Its stated limit, before anyone runs it:** n is tiny (7 + 12 lanes) and byte-count is
confounded with task difficulty. *"This design yields a descriptive series, not a controlled
comparison, and must be reported as one."*

**Why it is unblocked when the dashboard arc is not:** its three fields deliberately avoid the
`events` store, so it does not depend on the two legs NB4-B found open — **`logs/TELEMETRY.db`
has never been written** (`[#529]` merged the emit library with zero call sites), and lane
telemetry resolves under the worktree and is **deleted at teardown**. Neither lane cites the
other.

### A4 · Substrate migration — NB4-G v2

`docs/audits/2026-08-16-technical-nb4-g-scaleout-substrate-v2.md` (**on an unlanded branch**;
supersedes v1 + amendments 1–3, which stay on disk as the record). Three independently swappable
planes — control / execution / deployment — and a plan that **starts this week**:

```
Stage 1  day 1     ~EUR 0        ~2-4 h
Stage 2  week 1    ~EUR 3-10/mo  ~2-4 h
Stage 3  month 1   widen and decide
```

**v2 exists because v1 got the problem wrong in six named ways**, and two of them are the reason
this arc is worth the architect's time rather than a re-read: v1 **priced monthly for a host
idle ~89 % of the month**, and it **never asked what the control plane was** — the operator has
to *watch* 16–32 lanes, and the human interface was treated as free. §5.4 shows that inverts a v1
conclusion. GitHub Codespaces — VS-Code-native, hourly-billed, private-repo-safe — was **absent
from v1's option set entirely**, and v2's own diagnosis of why is the part worth carrying:
*"v1's option set was shaped by the questions asked rather than by the problem."*

**Status: DRAFT, advisory until ratified.** Decides nothing, births no row. Model routing is
condensed to §8 and stays gated on a corpus run that has not happened.

### A5 · The multi-LLM acceptance run — gated on W3

`[#492]`'s method is fixed and does not need re-deriving: seed a defect list drawn from **this
fleet's own history** (vacuous test, fail-open except, stale locator, fence corruption) into real
diffs, then compare catch rate against the **terra baseline on the SAME diffs**. Entry by
measured acceptance, never vibes. The **corpus is current** — the 12 seed verdicts were
re-derived against the landed spec on 2026-08-13 with **0 flips**; that closed the
corpus-currency leg only and **moved no date**.

NB4-A attaches the promotion gate: HARD REFUSE on any fabricated locator; ADMIT-full vs
ADMIT-shadow vs REFUSE; and ADR-74 Footnote B's **n=2** rule that a first ADMIT is provisional.
Every new lane obeys artifact-or-RED and **writes its severity tally into the artifact body** from
day one.

### A6 · The PLAYBOOK 12-act arc — NB4-C

Tally **covered 1 / partial 6 / absent 6** across 13 mechanism shapes. C's shape finding:

> *"Every ABSENT row is a mechanism born in the last EIGHT DAYS and every PARTIAL row is an older
> section whose machine contract moved underneath it. The PLAYBOOK is current on DOCTRINE and
> behind on the MACHINE the doctrine now runs on."*

**12 acts · Ch8 ×7, Ch11 ×3, §5 ×1, Ch10 ×1 · ≈ +250 lines on 4628 (~5 %) · +0 ratchet tokens,
measured.** All twelve drafts are **paste-ready**, so *"the architect's cost is a ruling rather
than an authoring pass."* Each act stands alone (see W11 for the one ordering constraint and the
two replace-not-append acts).

**Two rows C says are actively costing work rather than being merely silent:** row 2, lane
grammar (F4), and **row 11, the codex tally — the documented format fails the live parser on 2 of
4 legs** (`**HEAD:**` MISS, `**Tally:**` MISS), so an artifact authored *from the PLAYBOOK* is
recognized and then discounted into the check's `untallied` list. Live corroboration: the four
Position-0 artifacts were *"authored against the parser regexes rather than against prose
intent."*

**C states the bar so it can be overturned:** under a *"does a section exist"* bar the tally reads
**covered 6 / partial 1 / absent 6** instead; rows 1, 2, 6, 10 are bar-sensitive.

### A7 · The archival mechanism — NB6-C

**Named by the brief; its report is NOT visible from this lane** (R17 — `origin` carries no NB6
ref but this one). Recorded as a placeholder with its adjacent in-repo state, so the architect
can slot it without re-deriving the surround:

- Retention is ruled **keep-all-accepted** (ADR-100). The count-tiered index shape ADR-100 also
  names is `[#269]` and is **NOT built** — `docs/audits/README.md` groups by month.
- The corpus is **550 audit documents** and the index is generated + gated
  (`audit-index-freshness`), so any archival mechanism must move files *and* survive
  regeneration.
- Precedent exists and constrains the design: the 2026-07-22 verb-list ruling accepted
  **186 keep / 34 archive-candidate / 0 delete-candidate with 0 deletions**, handling
  archive-candidates by **index grouping only, NO physical moves**.
- The one sanctioned physical-relocation precedent in the tree is the ADR-29 2026-07-17
  `LESSONS-legacy-<span>.md` exception, which is **byte-identical relocation of a contiguous
  older block** — a narrow carve-out, not a general archival power.

**Nothing above is NB6-C's finding.** It is the surround, so its finding can be read against it.

---

## 5. DO-NOT-REDERIVE — for the successor

Established facts with locators. Re-measuring these spends budget for no information.

```
BOOT / STATE
  origin/main @ 88422f5c "Merge branch 'docs/batch6-close' -- batch 6 closes". Batch 6 is CLOSED;
    open_batches() is empty and the ADR-110 exemption is expired.
  Live BACKLOG = 196 rows (172 open + 24 deferred). NOT 195, NOT 197: [#533] was born mid-arc,
    and the 197 reading was the resolver defect (F2), repaired at 3def2821.
  Batch 6: 12 of 12 lanes merged, dispatched width 11 + lane k by ruling. Close-width delta +1.
  No `--no-verify` and no `SKIP=` at ANY point in the batch, including where block-commit-on-main
    refused a repair commit and audit-health blocked a merge. Both fixed forward.

GATE READINGS (this lane, 88422f5c, cloud container)
  health    52 WARN / 0 FAIL / DEGRADED     ship-gate  26 disp / 26 undisp / 2 stale / RED
  Container-only: fleet_parity x4 + deployed_methodology_version x1  =>  47 host-side.
  The undispositioned set is ONE CLASS: doc_rot, 19 rows, ceiling 1320. Full list at §1b.
  The ship-gate hard-fail organ here is `hooks_armed` (unarmed fresh clone) — a container
    artifact, not repo state.

MEASURED, DO NOT RE-MEASURE
  audit.py health is I/O-BOUND: ~2 min CPU per ~5 min wall at 8% load. ThreadPoolExecutor is the
    indicated executor for [#533] leg 2; the ProcessPoolExecutor condition is NOT met.
  Eleven lanes running whole-repo audit.py health concurrently cost 25-40 min wall-clock per
    gated commit (lane m, verbatim). Price it into batch sizing.
  journal_anchor memoization: ~42.7s -> ~17.8s per commit (NB3-D).
  silent_rule_ratchet: live 440 <= baseline 441. One below; ratchet-down available.
  ALL_CHECKS = 43 members. audit.py 5243 -> 4270 lines. 16 extracted, 27 held.
  Untestable rows: 58 - 29 converted = 29 remaining against a denominator of 196. Arithmetic over
    the 2026-08-10 grades plus verified deltas, NOT a fresh row-by-row re-grading (O-3's limit).

BRANCH / REF FACTS
  origin carries 13 refs: main, automation/fleet-audit (STANDING KEEP, unrelated root, 171
    commits, no merge base), 10 cloud report branches (R15), and this lane's.
  There are NO night2 / night3 branches on origin — those artifacts already landed
    (JOURNAL 2026-08-15 (d) and 2026-08-16 (a)).
  NONE of the 12 worktree-lane-* branches is on origin. Only their --no-ff merges reached main.
  f5c5e9dd is NOT a valid object against a full-history clone. It exists only on the operator's
    machine.

TRAPS ALREADY PAID FOR
  A cloud clone boots SHALLOW (290 commits). Every history-dependent check is wrong until
    `git fetch --unshallow` (5174). Do this FIRST or discard the readings.
  `uv run --locked` refuses on the pin in every cloud container. Route: pip install --target
    click pyyaml markdown-it-py rich, then PYTHONPATH + system python. READ-ONLY use only —
    the interpreter is 3.11.15 against a 3.12.10 pin.
  The clone's root basename is `dev-knowledge`, not `.dev-knowledge`. That alone costs +1 WARN
    (F6). Decompose every WARN total by check; never report it bare.
  A generated-index merge conflict (docs/audits/README.md) resolves by REGENERATION, never by
    picking a side. That is the only conflict class in the 10-branch land-then-delete set.

STANDING READINGS THAT ARE ALREADY ADJUDICATED — do not re-open
  no_ff_merges x3: immutable June history, dispositioned, unfixable without a rewrite. NEVER.
  undeclared_edges x18: 18/18 dispositioned under ref #241. Dispositioning them again buys
    nothing; the declare-vs-defer adjudication is [#241]'s own.
  journal_spine_anchor "anchored by mention": advisory SHAPE leg, WARN by ruling
    (STANDING_RULINGS L-10). Zero by design. Leave it.
```

---

## 6. What this lane did NOT do

Stated so the boundary is checkable rather than inferred.

- **No ruling, no disposition, no closure, no birth, no re-peg.** Zero rows moved.
- **Did not re-verify the Grok 4.6 release.** R11 carries NB4-A's finding *with NB4-A's own
  egress limit attached*; the 2026-08-17 browser re-check is unmoved and un-pre-empted.
- **Did not read every NB4 report end to end.** NB4-A, NB4-B, NB4-D and NB4-F are carried
  **through the NB4 consolidated briefing** and are attributed to it, not read at source. NB4-C,
  NB4-E and NB4-G v2 were read directly. Anything sourced from the briefing inherits the
  briefing's grades, including its `PROPOSED` and `UNVERIFIABLE` marks.
- **Did not resolve any of the briefing's 14 contradictions.** X1's three-way resolution is
  quoted in F5 because AMENDMENT 1 states it as fact; the rest are left as the fan-out's product.
- **Did not run the test suite.** The 2-RED figure is the integrator's run, cited not re-measured.
- **Did not land, push, delete or touch any of the 10 cloud report branches**, and did not
  propose pushing `f5c5e9dd`.
- **Wrote exactly two files** — this report and the regenerated `docs/audits/README.md` index,
  which the `audit-index-freshness` gate requires and which every sibling cloud lane also touched.

---

residual 18 items · flags 8 · arcs 7

---

## AMENDMENT 1 — 2026-08-16, post-push: F5 fires on this session, and the third route is narrower than F5 claims

*(In-file amendment marker per CLAUDE.md §5 rule 3 — `docs/audits/` is immutable, so this is
marked rather than woven into §2. Nothing above this line is edited, including the metric line,
which the amendment does not move: this adds no residual item and no flag — it sharpens **F5**
and corrects an over-claim inside it.)*

**The trigger.** After the commit above was pushed, the `Stop` hook ran and returned:

```
[uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"]:
error: Required uv version `==0.11.19` does not match the running version `0.8.17`.
```

That is `[#453]` gap (2) verbatim — *"the container shipped uv 0.8.17 against the ADR-106
`==0.11.19` pin"* — and it makes this **at least the seventh live witness in this window**. §2 F5
predicted this surface would be silent; this is the state occurring, on the session-end surface,
**after** the report describing it was written and pushed.

**What this lane could establish that no prior witness could, and it is the part worth carrying.**
Every earlier witness recorded the organ as inert and stopped there, because none of them could
run it. The §0 route can. Run directly:

```
PYTHONPATH=<scratch> python scripts/session_end_backpressure.py
  ->  no output, rc=0        the organ PASSES. It had nothing to say about this session.
```

> **So the observable at the `Stop` surface was identical to a pass — and it was a pass. That is
> the defect stated precisely: an inert organ and a passing organ are indistinguishable from
> outside.** NB4-D's *"an organ that never gets to speak"* is right, and this is the sharper
> version: the operator cannot tell speaking-and-saying-nothing from not-speaking. Every prior
> witness in this window resolved that ambiguity by assumption; this one resolved it by
> measurement, and the answer happened to be benign. **The next one may not be, and nothing in
> the surface would look different.**

**The correction F5 owes.** F5 offers the dependency-side route as a third entry in `[#453]`'s
option set. **It does not rescue a harness-invoked organ, and F5 does not say so.** The
invocation line is fixed in `.claude/settings.json:9` as `uv run --locked python …`; a session
cannot reach inside it. The route is therefore **a manual measurement fallback only** — good for
a read-only cloud lane taking a reading, useless for any organ the harness fires on its own
schedule, which is precisely the unattended class `[#453]` exists for. F5's stated limit
(interpreter 3.11.15 against a 3.12.10 pin) is true but was the *wrong* limit to lead with.

**One mechanism this joins up, reported because §1b and §5 listed the pieces separately.**
`.claude/settings.json:52` fires the RF-2 self-arm — `arm_hooks.py`, whose whole job is the
idempotent `pre-commit install` — through **the same `uv run --locked` line**. So the pin
silences the organ that arms the hooks, which is *why* the hooks stay unarmed, which is *why*
`check_hooks_armed` hard-fails, which is *why* §1b's ship-gate reads `RED — 1 hard-fail organ`.
**One cause, four effects**, three of which this report attributed to "a fresh clone" as though
they were independent. They are not: a fresh clone alone would self-arm on SessionStart. It is
the pin that stops it, and the same pin then hides that it stopped it.

**Nothing here is ruled or filed.** `[#453]` already owns the class and its Done-when already
names the runbook; this is evidence against that row, not a new one. The `Stop` hook is
**advisory in full** (ADR-85 amendment 2026-08-03 §A5) and has no hard leg, so nothing was
bypassed and there was nothing to override — `/override` is RETIRED and discharges no gate.
