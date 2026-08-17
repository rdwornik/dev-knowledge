# Archive sweep — what accumulates, what may retire, and the mechanism that would make it a system

- **Class:** census (ADR-101 §2 enum) · **Date:** 2026-08-16 · **Slug:** nb6-archive-sweep
- **Status:** **DRAFT — evidence + proposal.** Zero moves, zero deletions, zero status edits, zero BACKLOG touches. The proposal in §5 is *for the architect's birth ruling*; nothing in it is executed here.
- **Source-session:** night-batch 6 lane C, branch `claude/nb6-archive-sweep-5a7rch`, base `88422f5` (`main` at provisioning).
- **Consumer:** the architect seat that rules whether an archival mechanism is born.
- **Consumption path:** §1–§4 are the four per-class inventories with their governing rules quoted; §5 is the single ruling this report asks for, with a kill-candidates line ready to file.
- **Retrieval:** deterministic — frontmatter parse, `git log`, directory listings, validator source. Not model-summarized.

---

## Headline

**The operator's frustration is well-founded, but the diagnosis is not "nothing retires" — it is that
retirement is manual, unproposed, and only defined for two of the four corpora.**

- **Where a rule exists (intake, ADRs), the live sets are conformant** — and have been kept that way
  by hand, by one operator ruling of 2026-07-22, never by an organ.
- **Where a rule does not exist (audits, handoffs), the absence is *ruled*, not an oversight** —
  ADR-100 keep-all-accepted. Those two corpora are *supposed* to grow monotonically.
- **The relief valve that ADR-100 ruled in place of archival — the count-tiered index — was never
  built.** It is filed as `[#269]`. That single unbuilt item is the whole of what "nothing visibly
  retires" means for the corpus that actually grows: **the audit corpus grew +123 files in 8 days
  and its index is a flat 550-entry list.**

**Archivable-now under the rules as written: 0 files in every class.** The honest sweep is not a
move — it is **six intake status transitions that nobody has proposed**, and one unbuilt index.

---

## 0. Relationship to the 2026-08-08 archival-lifecycle audit — delta only

`docs/audits/2026-08-08-technical-archival-lifecycle-audit.md` (8 days ago) already established the
doctrine survey, the mechanism search, and the ADR/intake censuses. **This report does not repeat
them.** It is credited as prior art and its findings are treated as the baseline. What is new here:

| # | New in this report | Why it is new |
|---|---|---|
| 1 | **Handoffs** — bundle retention state, 3-shape classification | The 2026-08-08 audit did not cover `docs/handoffs/` at all |
| 2 | **Audit classes** — consumed-and-archivable vs permanently-canonical | Not attempted before; the brief asks for it |
| 3 | **8-day drift** — audits +123, intake +6 live, ADRs +2 | Measures accumulation velocity, which is the operator's actual complaint |
| 4 | **The `#328` departed-trigger finding** (§1.3) | Three ACCEPTED-deferred intakes are parked on an un-park condition that can no longer fire |
| 5 | **`docs/decisions/README.md` census is stale by one** (§2.2) | An un-gated hand-maintained index; the exact rot class `audit-index-freshness` guards elsewhere |
| 6 | **THE PROPOSAL** (§5) | The 2026-08-08 audit explicitly proposed no mechanism ("§7 What this arc did NOT do") |

**Two of its findings have since been FIXED, verified live — recorded so they are not re-litigated:**

- Its §1c stale-pointer finding (`docs/audits/README.md:5` naming closed `[#212]`) is **closed**:
  `grep -c '#212' docs/audits/README.md` = **0**; the header now reads *"Retention is ruled
  keep-all-accepted (ADR-100); the count-tiered index shape ADR-100 also names is [#269] and is NOT
  built."*
- Its §5a headline finding — *"There is a 'zero-refs bar' governing ADR archival, and it exists only
  in a commit message"* — is **closed**: the bar is now written doctrine at
  `docs/decisions/README.md:27`, quoted below.

---

## 1. `docs/intake/` — count by status, discharge, and the governing rule

### 1.1 The governing rule EXISTS. Quoted.

**A rule for intake archival exists and is unusually complete** — it names its own terminal set, its
destination, its byte-identity requirement, and its own missing mechanism.

`docs/intake/README.md:163-166` — the lifecycle:

> ```
> SEED → DRAFT → READY → ACCEPTED (decided-by + disposition)   [live]
>                      → CONSUMED (consumed-by)                [terminal → archive/]
>                      → SUPERSEDED (superseded-by)            [terminal → archive/]
>                      → REJECTED (reason, kept)               [terminal → archive/]
> ```

`docs/intake/README.md:199-204` — the relocation rule:

> Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to
> `docs/intake/archive/` (operator ruling 2026-07-22, archive-inside-each-folder;
> terminal set per the [#398] deploy — ACCEPTED is deliberately NOT in it, a standing
> authority must stay visible live); live docs stay here. **The move is MANUAL for now —
> the status-coupled validator that would gate/automate it is wave work, not built.**
> Archived docs drop out of the generated Contents index (depth-1 scan); their
> `intake-id` join keys stay valid at the archive path.

`docs/intake/README.md:185-187` — **ACCEPTED is explicitly non-archival**, and this is load-bearing:

> - **ACCEPTED (decided-by + disposition)** — ruled standing authority: the content was
>   accepted as a charter / plan-of-record / requirements authority. **Not archival** —
>   an ACCEPTED doc stays live and visible.

**The precedent move is `f095a81f`** (2026-08-12, intake #10 → REJECTED → relocated). Its commit body
quotes its own destination from §5 rather than inventing one, and states the property the rule turns
on: *"The status flip and the `reason:` line were written first, then the file relocated with git mv
and no further edit — so the move itself is byte-identical, which is what §5 asks for."*

### 1.2 Count by status (live folder, 2026-08-16)

**29 live** + **7 archived** = **36 intake documents.** (The 2026-08-08 audit measured 23 live + 6
archived = 29; the delta is +6 live and +1 archived in 8 days.)

| Status | Count | intake-ids |
|---|---|---|
| SEED | 10 | #4, #5, #6, #7, #8, #9, #19, #21, #22, #23 |
| DRAFT | 4 | #24, #27, #33, #34 |
| READY | 1 | #15 |
| ACCEPTED | **14** | #12, #13, #14, #16, #17, #18, #20, #25, #26, #28, #29, #30, #31, #32 |
| CONSUMED / SUPERSEDED / REJECTED | **0** | — |
| **Live total** | **29** | matches the generated index's own "29 intake documents." |
| **Archived** | 7 | #1, #2, #3, #10 (REJECTED), #11 (SUPERSEDED), #14 ×2 (provenance drafts) |

**Archivable-now under the rule as written: 0.** No live document carries a terminal status. The rule
is satisfied with zero exceptions — as it was 8 days ago, and by hand both times.

### 1.3 Which ACCEPTED intakes are fully discharged?

The brief asks which ACCEPTED intakes are "fully discharged and archivable". **Under the quoted rule
the answer is doctrinally *none* — ACCEPTED never routes to archive.** The archivable path is a
*status transition* to CONSUMED, which requires evidence the content landed. That evidence, per
document:

| # | Discharge evidence | Verdict |
|---|---|---|
| **#26** | `ADR-110:7` — **`Intake:** #26 … — ACCEPTED, `disposition: active`"`. The whole intake, not a section. ADR-110 Accepted 2026-08-06; batches 4/5/6 have since run under it. | **CONSUMED candidate — fully discharged** |
| **#28** | `ADR-112:8` — **`Intake:** #28 (§A)`**. §B's two amendments are recorded at `protocols/STANDING_RULINGS.md` I-F2 per its own `decided-by`. Both halves landed, on two surfaces. | **CONSUMED candidate — fully discharged** |
| **#18** | Its `consumers:` names *"a HANDOFF_PROCESS version bump (v5.8-additive or v6)"*. v6 landed (ADR-82 ratified 2026-08-04; `docs/handoffs/README.md` frontmatter reads `reconciled_with: handoff-process@6.2.0`). Per-amendment verdicts at `docs/audits/2026-07-30-technical-intake18-ratification-record.md`. `[#435]`, its carrier, is closed. | **CONSUMED candidate — fully discharged** |
| #16 | `ADR-104:7` consumes §4 only; §1–§3/§5 → ADR-109. Its own in-file NOTE keeps §6's plan spine live. | Stays ACCEPTED — partial |
| #17 | `ADR-107` header: D1 and D5 land there; *"§3 Fibonacci and §4 scoring are … **carried forward, not ruled here**"*. | Stays ACCEPTED — partial |
| #20 | `consumers:` = `[#382]`→`[#383]`→`[#385]` + `[#388]`. `[#382]` is closed; **`[#383]`, `[#385]`, `[#388]` are all still open** in `BACKLOG.md`. | Stays ACCEPTED — consumers live |
| #25, #29, #30, #31, #32 | Ratified at the batch-4 GO 2026-08-11; actively driving batches 4–6. | Stays ACCEPTED — active |
| **#12, #13, #14** | All three carry `disposition: deferred` + `trigger: "#328 build"`. **`[#328]` no longer exists** — no `tasks/328-*.md`, no `^- [#328]` row in `BACKLOG.md`; it survives only as a dangling reference inside `[#329]`, `[#331]` and `[#332]`. | **Stays ACCEPTED — but the un-park condition can never fire as written.** See below. |

**The `#328` finding is the sharpest thing in this report.** Three ACCEPTED intakes are parked on a
`trigger:` naming a departed backlog id. `docs/intake/README.md:120` requires a deferred ACCEPTED doc
to carry `trigger:` or `review-date:` precisely so that *"the un-park condition is part of the record,
not tribal memory"* — but nothing checks that the trigger still resolves. These three documents are
schema-conformant and permanently parked at the same time. That is not accumulation by neglect; it is
accumulation that the schema *certifies as healthy*.

**So the discharge answer is: 3 documents (#26, #28, #18) are fully discharged and would become
archivable the moment someone proposes the status flip — and nothing proposes it.** That gap, not a
missing folder, is the mechanism §5 addresses.

### 1.4 The scene's own survival metric has been firing for 8 days

`docs/intake/README.md:232-235`:

> - **Survival metric:** intake docs sitting unconsumed after **~1 month of operation**
>   trigger a review of the scene for removal (ADR-98 §6). A folder that only
>   accumulates SEED/DRAFT docs nobody triages has failed the same test a routine
>   fails.

The 2026-08-08 audit §5e recorded this condition as **met** (6 of 10 SEED docs dated 2026-07-07/08).
**Today those same six are still SEED, 40 days on, and the review it names has not been recorded.**
The rule fired, was reported, and produced no act — which is the operator's complaint stated in the
corpus's own words.

---

## 2. `docs/decisions/` — count and supersession candidates

### 2.1 Count

**85 live** + **2 archived** = **87 ADR files.** By live status: **Accepted 82**, off-enum 3 (ADR-45
`Explored, not adopted`; ADR-46/47 `Partially superseded — retained as convention, NOT
audit-enforced`). Archived: ADR-40 (`Deprecated`), ADR-52 (`~~Accepted~~ Superseded by ADR-53`).
`ADR-44` is Reserved with no file. `ADR-51` and `ADR-70` each carry a separate amendment file.

The governing rule, `docs/decisions/README.md:8`:

> `archive/` holds terminal (Superseded/Deprecated) ADRs, relocated byte-identical.

…and the archival bar that the 2026-08-08 audit found living only in commit `216ce3a8` is now
**written**, `docs/decisions/README.md:27`:

> | **Superseded** | wholly replaced; the successor is named. Terminal — eligible for `archive/` at H3's zero-inbound bar |

**Archivable-now: 0.** Zero live ADRs carry `Superseded` or `Deprecated`. The three off-enum live ADRs
are pre-declared carve-outs at `CONTRIBUTING.md:192-198`, not violations.

### 2.2 Superseded/absorbed candidates, with evidence

No ADR is *archivable* today. Three are the standing **candidates** a supersession review would open,
and each is blocked by a recorded reason rather than by neglect:

| ADR | Evidence of supersession | Why it is not archivable |
|---|---|---|
| **ADR-45** (Handoff architecture v4) | Status line: *"Explored, not adopted; ADR-42 v3.2 remains canonical authority"*. **Its own README index row `:34` renders it as "Superseded by … (HANDOFF_PROCESS v3.3)" — the index and the ADR disagree.** | Fails the **zero-inbound bar** (`README.md:27`): live prose points at it from `protocols/PLAYBOOK.md:3646/:3659/:3686`, `CONTRIBUTING.md:196-198`, `JOURNAL.md`. Additionally gated by `[#362]`. The index-vs-status divergence is `[#242]`'s domain and is **unresolved today**. |
| **ADR-46 / ADR-47** (cross-repo dated entries / backlog org) | Status: *"Partially superseded — retained as convention, NOT audit-enforced"*. Two later ADRs name them in `**Amends:**` — one as *"ADR-46, ADR-47 (demoted)"*, one as *"ADR-46, ADR-47 (fewer files governed)"*. | *Partially* superseded is not the terminal `Superseded`; both are explicitly *retained as convention*. Correctly live. |

**A live index-rot finding, verified this session.** `docs/decisions/README.md:31` states the census
across *"the 86 ADR files in this folder and `archive/`"* with **Accepted (81)**. The measured live
tree is **87 files / 82 Accepted** — the census is **stale by exactly one** (ADR-111, ratified
2026-08-10; the sentence was touched at ADR-112's ratification without incrementing). This index is
**hand-maintained with no generator and no freshness gate** — precisely the silent-rot class that
`audit-index-freshness` guards for `docs/audits/` and `claude-rosters-freshness` guards for the
CLAUDE.md fragments. It is reported, not fixed (this arc edits no doctrine).

---

## 3. `docs/audits/` — total, growth, and which classes could ever retire

### 3.1 Total and growth this window

**550 audit documents** at this lane's provisioning base (excluding `README.md`), reconciling exactly
with the generated index's count at that commit. **551 once this report lands** — the mandated index
regen in this arc's own commit carries that increment, so the figure below is the *pre-report* corpus
and the index will read one higher.

| Basis | Figure |
|---|---|
| Total (filename-date corpus, pre-report) | **550** |
| At the 2026-08-08 archival audit | 427 |
| **Growth in 8 days** | **+123 (+29%)** |
| Filename-dated 2026-08 | 205 (37% of the entire corpus, in 16 days) |
| Last three days (08-14 / 08-15 / 08-16) | 10 / 24 / 15 = **49** |

*Measurement note, stated because it would otherwise mislead:* this repo's git history begins
**2026-08-11** (290 commits; `git log --reverse` head is a batch-4 merge), so `git`-add-date is
unusable for growth before that date and returns a spurious 488-file spike on the seed day. All growth
figures above are **filename dates**, which ADR-101 §3 names as the honest content/session date:
*"filename date = content/session date and lags git-add date by ~15–19% by design."*

### 3.2 There is NO archival rule for audits, and the absence is RULED

This is the single most important thing to state before any class-by-class analysis, because it
forecloses the obvious move. `ADR-100:25` and `:34`:

> ### 1. Keep-all-accepted (no physical move, no roll-up, no compaction)
> Every accepted audit is **kept, unbounded**; audit files are **never physically moved, rolled up, or compacted.**

> - **Everything older moves to an archive *section of the index*** — **a section of the index, not the filesystem.** **Files never move; only their index grouping does.**

The reason is referential, not aesthetic: *"~78% of those citations are in immutable/append-only files
that can never be re-pointed … the referential cost of a move is permanent breakage."* And `ADR-100`
§3 gates any future move behind **both** a referential-currency scan **and** an explicit architect
ruling.

**Therefore the answer to "which audit classes are consumed-and-archivable" is: none — by ruling, not
by analysis.** The class table below is supplied because the brief asks for it, and because it is the
input a future §3-gated ruling would need. **It is not a proposal to move anything.**

### 3.3 Class inventory — what *would* be consumed-and-archivable if the §3 gate ever opened

| Class | Count | Consumed-and-archivable in principle? | Reasoning |
|---|---|---|---|
| **Lane contracts** (`*-lane-contract`) | **30** | **Yes — strongest candidate.** All 30 are filename-dated 2026-08. | A contract is *consumed at lane merge*. Its content is frozen into the lane's commits and its packet. `[#520]` already shows the class has a retirement problem with no sanctioned surface. |
| **Lane/batch packets + manifests** (`*-packet`, `*-manifest`) | 16 + 10 | **Partly.** | A manifest is consumed at integration. A packet is the lane's *evidence of what landed* — closer to canonical. |
| **Night reports** (`*night*`) | **109** (60 in 2026-08) | **Partly** — only where the briefing landed. | A night research/plan report whose decision queue was ruled is consumed. But night *findings* are cited by later ADRs, so the class is not uniform. |
| **Codex reviews** (`codex-*`) | 140 | **No — permanently canonical.** | Adversarial-review records; ADR-107's own header cites one as its ratification evidence. |
| **Conformance digests** (`conformance-nightly-*`) | 22 | **No.** | Recurring evidence stream; ADR-105's precipitating evidence. |
| **Ecosystem audits** | 17 | **No.** | The evidence spine proper. |
| **Changelog reviews** | 6 | **No.** | Feed `docs/intake/` SEEDs by id. |
| **Everything else** (census, verification, fresh-eyes, cross-repo, corp-*, incident) | ~210 | **No — permanently canonical.** | This is the evidence spine ADR-100 §1 protects by name. |

**Read across the table: roughly 56 files (30 contracts + 26 packets/manifests) are the only plausible
consumed class, ~10% of the corpus — against a permanent breakage risk on the other 90%.** That ratio
is why ADR-100 ruled the way it did, and this inventory confirms rather than challenges it.

### 3.4 ADR-107 names the root cause, and it is not a missing folder

`ADR-107` Context, quoting `docs/handoffs/2026-07-26-dev-knowledge-architect/SUPPLEMENT.md` §1
verbatim:

> BACKLOG.md is not too big, it is the WRONG DATA STRUCTURE. One file serves five workloads
> (work queue, dependency graph, archive, decision register, evidence store). Every defect of
> this window maps to that: … **nothing is ever deleted because closing means editing a 170KB file**;
> id collisions because the counter is prose, not a directory.

*"Nothing is ever deleted because closing means editing a 170KB file"* is the operator's frustration
in the repo's own words, diagnosed as a **friction** problem, not a **rule** problem. It is the
strongest argument in the corpus for the §5 shape: the fix is to make retirement *proposed and cheap*,
not to write another rule.

---

## 4. `docs/handoffs/` — bundle retention state

### 4.1 Inventory

**108 live bundles** + **15 archived bundles** + a `legacy/` subtree (43 files, 2026-04 era).

| Shape | Count | What it is |
|---|---|---|
| v5/v6 bundles (carry `HANDOFF_BOOT.md`) | **75** | 2026-06 ×21, 2026-07 ×44, 2026-08 ×10 |
| Pre-v5 with `README.md` | 13 | superseded-era |
| Pre-v5 heavy numbered-file bundles (neither) | 20 | 2026-05 era, e.g. `00_README.md`…`06_STATE_OF_PLAY.md` |
| **Live total** | **108** | |
| `docs/handoffs/archive/` | 15 | **a different artifact class** — council `stage1-question.md` / `stage2-response.md` pairs |

### 4.2 The rule: keep-all, same as audits

`ADR-100:45`:

> ### 5. #212 (handoffs) resolves the same way — keep-all-accepted

…*"handoff bundles are cited and immutable, so a physical move / roll-up breaks references it cannot
re-point. This **closes #212**."*

And `ADR-101:76` disposes of the superseded-era bundles explicitly:

> - **Superseded-era bundles STAY.** The superseded-era **pre-v5 handoff bundles** (v3.2 + v4, 2026-05-09→2026-06-10) remain as by-design historical: §S4-3 found **no rule mandates archiving them**, and `docs/handoffs/archive/` holds a *different* artifact class here. They are grandfathered in place, not swept.

**Verified live:** `docs/handoffs/archive/2026-05-09-ai-council-audit-sync/` contains only
`stage1-question.md` + `stage2-response.md`, while a *live* directory of the **same slug** carries the
11-file heavy bundle. The two are genuinely different artifacts sharing a name — ADR-101's claim holds.

**Archivable-now: 0.** The 33 pre-v5 live bundles are grandfathered by explicit ruling.

### 4.3 Two open retirement gaps, both already filed

- **`[#520]`** — *"No sanctioned way to retire a committed bundle whose seal is wrong."*
  `docs/handoffs/2026-08-01-dev-knowledge-architect-2` declares its sibling's slug, so
  `check_seal_identity` FAILs it on every `--all-files` sweep and its own probes verify green **about
  the wrong bundle**. Direction is already ruled: *"retire via an external dated marker, bundle left
  byte-unchanged."* **This is the repo's only ruled retirement-without-moving pattern, and it is
  unbuilt.**
- **`[#300]`** — the committed `docs/handoffs/2026-07-07-dev-knowledge-functional/` mode-boot bundle,
  which ADR-101 §5 rules ephemeral-and-never-committed. Its row records the sweep as *"AWAITING
  explicit operator deletion GO (no drive-by deletion)."* **One file, one GO, open since 2026-07-10.**

---

## 5. THE PROPOSAL

### 5.1 Library-first: is a `docs/archive/` move-with-index pattern already precedented?

**Yes for the move. Yes for the index. And the top-level `docs/archive/` is the wrong destination and
is frozen.** All three matter:

- **The move is precedented three times**, all within 24 hours of one ruling: `af63a0f3` (intake),
  `216ce3a8` (ADRs), `6551d363` (intake, under `[#398]`) — plus `f095a81f` (2026-08-12). The pattern
  is **`git mv` byte-identical into a per-folder `archive/`**, and it is written doctrine in two
  READMEs. **Nothing needs designing here.**
- **The index half is already built.** `gen_intake_index.py`'s depth-1 glob means an archived file
  drops out of the Contents block automatically — the generator's own docstring states *"This
  generator itself MOVES NO FILE."* The move-with-index pattern therefore already exists end-to-end
  for intake.
- **`docs/archive/` (top-level) must NOT be the destination.** It is the ADR-60 pending-classification
  triage queue, a different genre — and `[#420]` freezes it in terms: **"Do NOT touch `docs/archive/`
  while this is open — no move, no promotion, no deletion."** Any proposal routing artifacts there
  collides with an open operator-raised ruling. *(Its own rule at `docs/archive/README.md:10` —
  "if something sits here across two reviews with no decision, default to deletion" — has a met
  condition and one recorded review, 2026-05-28. Naming it only; `[#420]` owns it.)*
- **A fourth archive convention exists and is worth citing as the shape to copy:** `ADR-83:20` —
  *"Superseded or dead protocols move to `protocols/archive/<name>.md` carrying a blockquote tombstone
  at the top of the file."* Two files live there. `ADR-83:52` states the posture that has since proven
  true of **every** archival rule in this repo: *"the convention is enforced by discipline + review,
  not a hook."*

**Conclusion: no new archival mechanism should be built. Four conventions and one working
move-with-index already exist. The missing organ is a DETECTOR and a PROPOSER.**

### 5.2 The mechanism — two legs, **zero new organs**

Organ sprawl is a named standing concern (`[#401]`: *"refusal at the point of use is ONE organ;
extending an existing guard adds a SECOND organ watching the first, and this fleet already carries
organ sprawl"*). Both legs below extend an existing organ rather than adding one.

**Leg A — the ratchet (hard, cheap).** One new check `archival_residency` in the existing
`scripts/audit_checks/` package (the `[#533]` decomposition landed the seam this session), registered
in `audit.py`'s check registry and therefore already carried by the `audit-health` pre-commit gate.
It answers exactly one question: **does any document's status say terminal while its location says
live?**

- `docs/intake/*.md` with status ∈ {CONSUMED, SUPERSEDED, REJECTED} → **FAIL**
- `docs/decisions/ADR-*.md` with status ∈ {Superseded, Deprecated} **and zero inbound live-prose
  refs** (the `README.md:27` H3 bar, now written) → **FAIL**; non-zero inbound → **WARN** naming the
  referring sites
- `docs/audits/**` and `docs/handoffs/**` → **NOT CHECKED, by ADR-100 ruling.** The check must state
  this exclusion in its own docstring so a future reader does not mistake silence for an oversight.
- **Parser note that will otherwise bite:** three ADR status-line formats coexist — `**Status:** X`,
  `- **Status:** X`, and YAML frontmatter (`ADR-61` only). A single-format parser returns a false
  `None` on ADR-61. The 2026-08-08 audit's own first extractor made this mistake; so did this
  report's.

This leg converts *"the rule is satisfied today, by hand"* into *"the rule cannot silently stop being
satisfied."* On today's tree it reports **EMPTY** — which is the point: it is a ratchet, not a sweep.

**Leg B — the proposer (advisory), folded into the existing Tier-1 `Stop` hook.** This is the leg that
actually addresses "nothing visibly retires." The library is `propose_closures.py` — ADR-70's Tier-1
loop is already **detect → propose → operator approves at `/review-closures` → execute**, and already
carries the never-mutates posture. Add a second section to its output, not a new hook:

1. **Discharged ACCEPTED intakes** — an ACCEPTED doc whose `consumers:`/`decided-by` targets are all
   closed or landed → propose the CONSUMED transition with a **drafted `consumed-by:` line**. On
   today's tree this emits exactly three: **#26 → ADR-110**, **#28 → ADR-112 §A + STANDING_RULINGS
   I-F2**, **#18 → HANDOFF_PROCESS v6 + the 2026-07-30 ratification record**.
2. **Unresolvable deferrals** — a `disposition: deferred` doc whose `trigger:` names a departed
   backlog id, or whose `review-date:` has passed. Today: **#12, #13, #14 (`trigger: "#328 build"`,
   id departed)**.
3. **Survival-metric breaches** — SEED/DRAFT older than the ADR-98 §6 ~1-month bar. Today: **6 docs
   (#4, #5, #6, #7, #8, #9), 40 days old.**

Output to `logs/PROPOSALS-ARCHIVAL.md` (UPPERCASE-KEBAB `.md` per the 2026-07-22 `logs/` naming
ruling). **Mutates nothing.** The operator's existing `/review-closures` act gains an archival
section; execution stays the same `git mv` + status-flip the four precedents already define.

**What is deliberately NOT proposed:** any audit-file or handoff-bundle move (ADR-100 forecloses it),
any use of `docs/archive/` (`[#420]` freezes it), and any new folder (ADR-101 Rule A refuses it).

### 5.3 The batch shape that executes the first sweep

ADR-110 form — one plan → N lanes → one integrator; lanes file-disjoint. **Four lanes, one of which
is gated on an operator GO that does not yet exist.**

| Lane | Work | Files owned | Gate |
|---|---|---|---|
| **A** | `archival_residency` check + tests (Leg A) | `scripts/audit_checks/archival_residency.py`, `scripts/audit.py` (registry line), `tests/test_archival_residency.py` | none |
| **B** | `[#269]` — count-tiered audit index + header repoint | `scripts/gen_audit_index.py`, `docs/audits/README.md` | none — already ruled by ADR-100 §2 |
| **C** | Leg B proposer section + tests | `plugins/tier1-lifecycle/**/propose_closures.py`, `tests/test_propose_archival.py` | none |
| **D** | **The first sweep** — flip #26/#28/#18 to CONSUMED with `consumed-by:`, `git mv` byte-identical to `docs/intake/archive/`, regen the index | `docs/intake/*.md` (3 files), `docs/intake/README.md` | **OPERATOR GO REQUIRED** — a status flip is a ruling, not an execution |

**Collision check:** A and C both add test files — distinct paths, no collision. B is the only lane
touching `docs/audits/README.md`. D is the only lane touching `docs/intake/`. **No lane touches
`CLAUDE.md`**, keeping the freshness-gated collision file out of the batch (the batch-4 W5 / batch-5
lane-O precedent: any owed §9 roster row is paid by the integrator).

**Lane B is the highest-value lane and the one to run first if only one runs.** It is the only lane
that changes what the operator *sees*: a 550-entry flat list becomes ~20 fresh + an archive section.
It is already ruled, already filed, and moves no file.

### 5.4 The recurring routine row (ADR-105 six-field form) — draft, ready to file

ADR-105 §1 requires the six-field in-line clause; §2 gates at **activation**, not filing, and
explicitly permits filing a proposal without them — but this row can name all six, so it does.

```
- [#NNN] [P2][S] **Archival residency ratchet + retirement proposer** — retirement in this repo is
  manual, unproposed, and defined for only two of four corpora; every archival move in the repo's
  history was executed by hand under one ruling of 2026-07-22 (`af63a0f3`, `216ce3a8`, `6551d363`,
  `f095a81f`). Two legs, zero new organs: (a) an `archival_residency` check in the existing
  `scripts/audit_checks/` registry that FAILs a terminal-status document sitting outside its
  `archive/` — intake + decisions only, `docs/audits/**` and `docs/handoffs/**` EXCLUDED by ADR-100
  keep-all; (b) a proposer section folded into the existing Tier-1 `Stop` hook that names discharged
  ACCEPTED intakes, deferrals whose `trigger:` id has departed, and ADR-98 §6 survival-metric
  breaches. Parser must handle all three ADR status-line formats (`**Status:**`, `- **Status:**`,
  YAML — `ADR-61`). · routine: trigger=`audit.py health` at every commit via the `audit-health`
  pre-commit gate, plus the Tier-1 `Stop` hook for the advisory leg · scope=`docs/intake/**` +
  `docs/decisions/**` status↔location residency; audits and handoffs excluded by ADR-100 §1/§5 ·
  consumer=the operator at `/review-closures` · consumption_path=a terminal-status-outside-archive
  FAILs the `audit-health` commit gate (blocking, not a report); retirement candidates print in the
  Stop-hook proposal block and persist to `logs/PROPOSALS-ARCHIVAL.md`, which `/review-closures`
  reads · verified_by=a test that plants a CONSUMED doc in `docs/intake/` and asserts FAIL, one that
  plants the same doc in `docs/intake/archive/` and asserts PASS, and one that asserts an `ADR-61`-
  shaped YAML status line parses rather than returning None · review_date=2026-11-16
  · Done when: a CONSUMED intake doc left in `docs/intake/` FAILs `audit.py health`, the same doc in
  `archive/` PASSes, and one `/review-closures` run surfaces the three discharged ACCEPTED intakes
  (#26, #28, #18) as named candidates without mutating any file
  · refs ADR-100, ADR-105, ADR-70, docs/intake/README.md §5, docs/decisions/README.md:27,
  docs/audits/2026-08-08-technical-archival-lifecycle-audit.md, #242, #269, #420, #520
  · kill-candidates: [#242] (ADR status-flip coherence check) — same corpus, same three status-line
  formats, same parser; [#242] checks status LEGIBILITY (header vs README index) and this checks
  status↔LOCATION residency. Folding [#242]'s legibility leg in as a second predicate is the
  consolidation and would retire one row; if the architect rules them genuinely distinct organs,
  this reads `none — [#242] is legibility, not residency`
  · serialize-group: audit-py
```

**Why `review_date` and not a trigger:** ADR-105's field wants a date when no un-parking event exists.
2026-11-16 is 90 days out — and the `#328` finding in §1.3 is the standing argument for preferring a
date over an id-shaped trigger.

### 5.5 One honest limit on the whole proposal

**Leg A reports EMPTY on today's tree, and will keep reporting EMPTY as long as nobody flips a status.**
A residency check cannot detect a document that *should* be terminal but is still marked ACCEPTED —
that judgement is a ruling, not a predicate. **Leg B is therefore the load-bearing half, and it is the
advisory one.** A reader who adopts only Leg A gets a ratchet that never fires and no change to what
accumulates. Stated plainly so the cheaper half is not mistaken for the fix.

---

## 6. What this arc did NOT do

- Moved nothing, deleted nothing, edited no status line, filed no BACKLOG row, wrote no rule.
- Did not touch `docs/archive/` in any way (`[#420]` freezes it).
- Did not fix the three live findings reported above — the `docs/decisions/README.md:31` stale census
  (86/81 vs measured 87/82), the ADR-45 index-vs-status divergence (`[#242]`'s domain), or the empty
  `consumed-by:` on intake #16. All are reported for an architect ruling.
- Did not re-run the 2026-08-08 audit's doctrine survey or mechanism search; they are cited as
  baseline.

**Gate posture — stated because it is weaker than a hub-local lane's, and a reader would otherwise
assume otherwise.** This lane ran in an Anthropic cloud container where **`.git/hooks/` carries no
`pre-commit`, `commit-msg` or `pre-push` hook** (`arm_hooks.py`'s idempotent install did not run
here) and `scripts/audit.py` is not importable (`ModuleNotFoundError: click`). **The commit therefore
did not pass through the `audit-health`, `ruff`, `backlog-filing-backpressure` or pre-push organs** —
not by `--no-verify`, but because they are absent. The two gates that actually bear on this arc's
diff were run directly and both pass:

- `validate_hermetization` — `rule_a_violation` / `rule_b_violation` / `rule_c_violation` all return
  `None` for this filename; `check([...])` returns `[]`. Class `census` is confirmed present in
  `AUDIT_CLASS_ENUM` (`scripts/validate_hermetization.py:106`).
- `gen_audit_index.py --check` — exit **0** after the mandated regen.

`check_seal_identity` is not applicable (it fires only on staged `docs/handoffs/**`; none here).
**A merge of this branch should be gated on the primary checkout, where the hooks are armed.**

---

## 7. Archivable-now, per class

| Class | Live | Archived | **Archivable NOW under the rule as written** | Governing rule |
|---|---|---|---|---|
| `docs/intake/` | 29 | 7 | **0** — no live doc carries a terminal status | `docs/intake/README.md:199` — rule EXISTS |
| `docs/decisions/` | 85 | 2 | **0** — no live ADR carries `Superseded`/`Deprecated` | `docs/decisions/README.md:8` + `:27` — rule EXISTS |
| `docs/audits/` | 550 (551 with this report) | — | **0 — by ruling, not by analysis** | `ADR-100:25` keep-all-accepted; **NO archival rule, deliberately** |
| `docs/handoffs/` | 108 bundles | 15 (different class) | **0** — pre-v5 bundles grandfathered explicitly | `ADR-100:45` + `ADR-101:76` — **NO archival rule, deliberately** |

**Pending one operator GO, not a mechanism: 3 intake status transitions (#26, #28, #18) and 1 handoff
bundle deletion (`[#300]`).**
