# [#433] K1–K5 spike prep — input dossier

**Status: PROPOSED — input dossier, not a decision.** Nothing here rules anything. Every
disposition below is DRAFT and awaits an architect ruling.

**Scope.** Read-only inventory of the facts a K1–K5 spike would need on day one: the five
workloads `BACKLOG.md` currently serves (§i), the current engine's measurable facts (§ii), the
three obligations the [#433] row carries (§iii), and a DRAFT spike skeleton with a DRAFT
operator-elicitation question (§iv). Repo state at read time: `main` @ `65a549b`, working tree
clean. Method: `grep -n` / `python3` counting / file reads only; no writes outside this file, no
git mutations.

**Read this first — the framing in the task order is one arc behind live state.** The K1–K5
spike **has already run once** and its output is `docs/audits/2026-07-27-verification-433-schema-spike.md`
(§1 records the K-definitions verbatim; §3 records the viewer pilot). ADR-107 then **adopted
K1–K5 + SCHEMA COMPOSABILITY as its own vocabulary**
(`docs/decisions/ADR-107-backlog-restructure-engine-schema-viewer.md:93–108`) and ruled the
viewer verdict. The [#433] row's clause *"operator's term, undefined in-repo — the spike records
it first"* (`BACKLOG.md:250`) is therefore **stale text on a live row**. What is actually
undischarged on [#433] is **obligation 2 only** — see §iii and §iv. A morning architect should
decide whether "the K1–K5 spike" now means *re-running the probes against a second candidate
viewer* (ADR-107 §4 clause 4) or *the second-surface generalization proof* (ADR-107 §6.2); these
are different spikes and the row does not distinguish them.

---

## (i) The five workloads `BACKLOG.md` currently serves

Census basis (all counts computed over the 181 task rows in `BACKLOG.md`, i.e. lines matching
`^- \[#`):

- task rows: `181` · theme headings (`^## \[E`): `9` · story headings (`^### \[S`): `26`
- rows carrying `Done when:`: `181/181` · `· refs `: `181/181`
- rows carrying `· serialize-group:`: `126/181` · `· depends-on:`: `7/181` · `kill-candidates:`: `102/181`
- rows carrying `DEFER — peg:`: `30/181` · `· routine:`: `2/181` · `evidence n=`: `1/181`
- row length: median `1048` chars; `146/181` rows exceed 700 chars; **0 rows exceed 1200**, and
  **five rows sit at exactly 1199** (`BACKLOG.md:27, :30, :55, :91, :397`) — one character under
  the `_BACKLOG_GROSS_CHARS = 1200` ceiling at `scripts/validate_doc_rot.py:58`. That clustering
  is the compression-pressure signature, not a coincidence.

### Workload 1 — QUEUE (what to do next)

- `BACKLOG.md:250` — `- [#433] [P1][M] **BACKLOG restructure — build-thin ENGINE + Backlog.md VIEWER** … · Done when: the K1–K5 spike is recorded AND an ADR records engine + viewer + swap-out contract AND the three obligations discharged · refs #382, #387, #347, docs/decisions/README.md`
- `BACKLOG.md:8` — `**Themes (backbone) — epic ids:** [E1] Handoff continuity · [E2] Enforced governance · … · [E9] Fleet Desired-State System (North Star)` (the backbone the story map hangs from)
- `BACKLOG.md:13` / `BACKLOG.md:35` — `## [E1] Handoff continuity` / `## [E2] Enforced governance` (theme headers; nine of them, `:13 :35 :122 :141 :155 :177 :218 :268 :420`)

Enforced shape: `scripts/validate_backlog.py:9–29` (ADR-66 story-map hierarchy; band + `Done
when:` + enclosing story + enclosing theme are hard-fail).

### Workload 2 — GRAPH (ordering / mutual exclusion / kill edges)

- `BACKLOG.md:41` — `- [#112] … · refs ADR-77, #105, #23, ADR-68 · depends-on: #23 · serialize-group: claude-md` (a `#`-prefixed dependency)
- `BACKLOG.md:433` — `- [#383] … · depends-on: 382 · serialize-group: architecture` (a **bare** dependency — the [#424] bare-vs-hash distinction the schema must carry raw)
- `BACKLOG.md:50` — `- [#389] … · kill-candidates: none — guard-to-gate conversion of the ADR-87 contract; #185 is GAP-2 (execution-time gotchas), not the prompt-field contract · depends-on: 390 · serialize-group: audit-py`

Graph density is thin and asymmetric: only `7/181` rows carry `depends-on`, while `126/181`
carry `serialize-group` and `102/181` carry `kill-candidates`. `BACKLOG.md:67` ([#452], filed
2026-07-31) is the live record that a first-class ordering obligation — the `[#433]`→`[#382]`
pilot-precedes-contract edge — **exists only as prose**: *"Verified 2026-07-31: neither
`tasks/433-*` nor `tasks/382-*` carries a `depends-on` clause at all, so no parser sees the edge
and no gate can enforce the ordering."*

### Workload 3 — ARCHIVE (history, deferral pegs, grooming record)

- `BACKLOG.md:452` — `**Grooming log:** git history is the record … Recent: 2026-06-12 (#149 flip) · 2026-06-18 (currency pass) · 2026-06-25 (groom pass, n=2: 84→81) · 2026-07-08 (leg-c full ruling pass, operator-ratified, 124→74: 14 KILL / 27 MERGE / 2 MOVE / 9 CLOSE / 5 RE-SCOPE / 19 DEFER-peg / 2 new filings #289 #290 …) · 2026-07-30 (per-handoff lightweight groom …). Next quarterly: 2026-10-08.` — a rolling history block inside the queue file, machine-read for cadence at `scripts/validate_doc_rot.py:205–215` (`_GROOMING_CADENCE_DAYS = 21`, `:61`).
- `BACKLOG.md:71` — `- [#169] … · refs docs/decisions/ADR-85-session-lifecycle-enforcement.md (R2), scripts/fleet_health.py, #166 · depends-on: #171 · DEFER — peg: #171` (a deferral peg; `30/181` rows carry one)
- `BACKLOG.md:258` — `- [#348] … **DECOMPOSED 2026-07-25** (a)->[#412], (c)->[#411]; holds (b) only — see 89ae1d1d.` (an in-row provenance/decomposition record)

Post-flip the archive workload also has a **filesystem** limb: 7 `tasks/*.md` files carry
`status: closed` and are unreferenced by `manifest.json` — `tasks/386-…`, `tasks/421-…`,
`tasks/435-…`, `tasks/437-…`, `tasks/439-…`, `tasks/444-…`, `tasks/446-…` — retained as id
allocation records per `tasks/README.md:41–52`.

### Workload 4 — DECISION REGISTER (rulings, forks, unruled picks)

- `BACKLOG.md:347` — `#### DECISIONS — dispositioned 2026-07-26 (the "ALL UNRULED" claim was true at filing, false since)`, with the register table header at `BACKLOG.md:359` — `| Ref | Decision | Status (verified 2026-07-26) | Recommendation as filed (NOT a ruling) |`
- `BACKLOG.md:361` — `| **R1** | \`assets/\` disposition: (a) DISSOLVE … | **DEAD-OBE** — the folder is gone. \`ai-council/assets/\` was dissolved by \`6d78851e\` (2026-07-21) … Option (a) was executed without the ruling. | **(a)** — one file, no fleet role … |`
- `BACKLOG.md:369` — `| **R8** | (carried, corp-side) #38 channel pick: 1 primary-direct / 2 worktree / 3 epic-dev | **UNRULED — stays that way.** The operator's own pick; four exhaustive searches across BACKLOG/JOURNAL/docs found no ruling. Explicitly NOT delegated. | *(none recorded — operator's pick)* |`
- Adjacent, same workload: `BACKLOG.md:277` — `#### Wave map W1–W7 (ordered by operator pain-priority, not dependency elegance)` (the ARC-5 plan of record, kept here *because* ADRs are immutable — the rationale is stated at `BACKLOG.md:270`).

This is the surface ADR-107 §6.2 names as a generalization candidate: *"the `[E8]` ruling/decision
register (the surface whose rot in a queue file is a named motivation for this restructure)"*
(`docs/decisions/ADR-107-…md:278–279`).

### Workload 5 — EVIDENCE STORE (SHAs, dated witnesses, incident counts)

- `BACKLOG.md:49` — `- [#353] … · evidence n=7: \`96bafe21\` direct-to-main 2026-07-19, caught manually not by a gate — JOURNAL · serialize-group: audit-py` (the only `evidence n=` clause in the file: `1/181`)
- `BACKLOG.md:94` — `- [#414] [P2][S] **Self-acting-on-main incident family … (n=2 this week)** — … a concurrent/dead session's checkout put non-merge \`94426dc0\` direct on main (core-invariant #5) …` (three SHAs in one row: `94426dc0`, `c5910486`, `f3ead30b`)
- `BACKLOG.md:96` — `- [#442] … **witnessed 2026-07-28**: a \`/review-closures\` invocation was served **pre-flip cached command text** … after \`52394caa\` had already migrated the repo copy to the flipped source of truth`

`13/181` rows carry at least one backticked 7–8 hex commit SHA. **No validator parses any of
this**: `grep -rn "evidence n=" --include=*.py .` returns zero hits outside tests. The evidence
workload is entirely unschematised and entirely uncheckable today.

---

## (ii) Current engine facts

### `tasks/` file census

- total files under `tasks/`: **190**; subdirectories: **0**
- of those: **188** task bodies (`<id>-<slug>.md`, all carrying frontmatter), **1** `manifest.json`, **1** `tasks/README.md` (operator doc, not a task)
- of the 188 bodies: **181** are referenced by `manifest.json` (= the 181 live `BACKLOG.md` rows); **7** are unreferenced retained allocation records, all `status: closed` (enumerated in §i workload 3)
- highest id present in `tasks/`: **452**; highest bracketed id in `BACKLOG.md`: **452**; so `next_free` = **453** under the ADR-107 rule
- frontmatter key census across the 188 bodies: `id` 188 · `title` 188 · `status` 188 · `priority` 188 · `size` 188 · `theme` 188 · `story` 188 · `generates` 188 · `serialize-group` **133** · `depends-on` **7**
- value distributions: `status` = open 151 / deferred 30 / closed 7; `priority` = P3 96 / P2 85 / P1 7; `size` = S 115 / M 66 / L 7

Note the `serialize-group` asymmetry: **133** task files carry the key but only **126**
`BACKLOG.md` rows carry the clause — the 7 retired records are counted in the file census and
have left the queue. Same arithmetic for `depends-on` (7 = 7, coincidental).

### `tasks/manifest.json` structure

Top-level keys, in order (`tasks/manifest.json:2–7`):

- `schema: 2`
- `role: "source-of-truth"`
- `generates: "BACKLOG.md"`
- `generated_sha256: "0952868d…b9e2"` — the sha256 of the full `BACKLOG.md` text this tree claims to produce (`tasks/README.md:75–77`; emitted at `scripts/gen_task_tree.py:327`)
- `generator: "scripts/gen_task_tree.py"`
- `nodes: [...]`

`nodes` holds **453** entries, and there are **exactly two node kinds** — no others:

- **272** nodes of shape `{"prose": "<verbatim physical line>"}` — the residue carrier: every
  non-task line of `BACKLOG.md`, in order (this is what makes one-file→many-files reversible;
  `scripts/gen_task_tree.py:19–22`)
- **181** nodes of shape `{"task": <int>, "file": "<id>-<slug>.md"}` — e.g. `{"task": 162, "file": "162-vocab-decision.md"}`

That is the whole schema. **There is no per-task field set in the manifest** — the per-task
fields live in each body file's frontmatter, and that frontmatter is *derived from the body
line*, not authored (`scripts/gen_task_tree.py:13–18`: *"the FRONTMATTER is DERIVED FROM THAT
BODY … editing frontmatter changes nothing on its own"*). Practical consequence for the spike: a
viewer that writes frontmatter writes into a **derived** surface and will RED the coherence gate.

### Id-allocation mechanism

**The normative rule is stated but NOT implemented.**

- The rule, `docs/decisions/ADR-107-…md:305–307`: *"**The rule (normative):** `next_free = max(id parsed from tasks/<id>-<slug>.md) + 1`, valid **only** while the directory is a complete ledger of every id ever allocated. It is not complete today…"*
- `grep -rn "next_free\|next-free" --include=*.py .` → **zero hits in any script.** The only
  in-repo occurrences are prose: `tasks/README.md:59–60`, `tasks/440-…md:13`, `tasks/429-…md:13`,
  and JOURNAL entries. **GAP: no code computes next-free; a filing session computes it by hand
  (or by `max()` over `ls tasks/`).**
- What *is* implemented is **detection, not allocation**:
  - `scripts/gen_task_tree.py:785–800` — the active-vs-active duplicate-id leg: *"id [#N] is held by two ACTIVE task files … an id is allocated once (ADR-107 6.3; the concurrent-branch collision this gate exists to catch)"*
  - `scripts/gen_task_tree.py:824–834` — retired-record id self-consistency (filename ↔ frontmatter ↔ body must agree)
  - `scripts/gen_task_tree.py:836–842` — terminal-status enforcement on retired records (`_TERMINAL_STATUSES = ("closed", "retired", "superseded")`, `:98`)
  - `scripts/gen_task_tree.py:844–849` — active-vs-retired re-issue refusal
  - `scripts/gen_task_tree.py:753–773` — the three-way id agreement across filename / body / manifest
- Retire-not-delete is the ledger's load-bearing rule: `--prune` is **refused** post-flip
  (`scripts/gen_task_tree.py:42–46`; `tasks/README.md:36–39`).
- Two named, unclosed holes:
  - **Deletion is undetectable** — `tasks/README.md:56–64` and the open row `tasks/440-…md:13`:
    *"deleting a retired file silently frees its id with every leg green."*
  - **Concurrent allocation is not prevented** — `docs/decisions/ADR-107-…md:463`: *"§6.3's
    **concurrent-allocation hole** is unchanged in kind: two branches can still each read the
    same maximum id and write differently-slugged files that git merges cleanly."* Owner: [#429].
- **PROPOSED drift finding (needs architect ruling, not fixed here):** `tasks/README.md:59–61`
  says `next_free = max(id in tasks/) + 1` is *"trustworthy against accident and **against
  concurrent allocation**, not against a deletion."* ADR-107's own amendment (`:463`) says the
  concurrent-allocation hole is **unchanged in kind**. One reading reconciles them (the collision
  is *detectable* post-merge even if not *prevented*), but the README sentence reads stronger
  than the ADR licenses. Flagged, not edited.

### Validator coverage

Validators that read `BACKLOG.md` and/or `tasks/`:

- `scripts/validate_backlog.py:52` (`BACKLOG.md` only). Hard-fails (`:15–29`): task with no
  enclosing story / story with no enclosing theme; missing `[P][S|M|L]` band; missing `Done
  when:`; missing or duplicate `[#id]`; a *done* task still present (ADR-65 done-items-leave —
  `status:done` suffix, `[x]`, struck bullet, `~~…~~`, `**RESOLVED`/`**DONE`); a story missing
  its `So that` line or its stable `[S<n>]` id, or a duplicate `[S<n>]`; a `· depends-on: #id`
  referencing a non-live id; a cycle in the depends-on graph. Warn-only (`:31–36`): a story with
  zero tasks; `#187` near-duplicate title detection (Jaccard, WARN, stated limit at `:36`).
- `scripts/audit.py:2888` `check_task_tree_coherence` — the ship-gate leg. Delegates to
  `gen_task_tree.find_incoherences` (`:2949`), and first refuses to answer if index and working
  tree disagree on `BACKLOG.md` or `tasks` (`:2939–2945`).
- `scripts/audit.py:1278` `check_git_backlog_drift` → `scripts/validate_git_backlog.py:74`.
  Direction (a) only: a `closes [#id]` commit in history whose id is still present in
  `BACKLOG.md` is drift. Direction (b) is explicitly **DEFERRED to #90b**
  (`scripts/validate_git_backlog.py:31–40`).
- `scripts/audit.py:1356` `check_doc_rot` → `scripts/validate_doc_rot.py:230–232`. Two BACKLOG
  sub-detectors: row-accretion (`_BACKLOG_DATED_BLOCKS = 3` + `_BACKLOG_LONG_CHARS = 700`, or
  `_BACKLOG_GROSS_CHARS = 1200` regardless — `:58–60`) and grooming cadence (`:205–215`).
- `scripts/audit.py:2510` `routine_consumers` — validates the `· routine:` six-field row shape
  (ADR-105); only `2/181` rows carry one.
- `scripts/check_backlog_commit_msg.py:44` — commit-msg gate; a commit **removing** a `- [#id]`
  row must name that id in the message.
- `scripts/check_backlog_filing.py:94` — commit-msg gate; a commit **adding** a `- [#id]` row
  must carry a `kill-candidates:` line (`_KILL_RE`, `:35`).
- `scripts/probe_child_backlogs.py:209` — read-only ADR-66 floor conformance probe over *child*
  repos, not this one.
- `scripts/review_closures.py:40` / `scripts/propose_closures.py:46` and their plugin twins
  (`plugins/tier1-lifecycle/scripts/…`) — the Tier-1 closure loop.

What the validators demonstrably do **NOT** check:

- **Nothing parses `evidence n=`** — zero hits for `evidence n=|evidence_n` across all `.py`
  outside tests. The single live clause (`BACKLOG.md:49`) is unvalidated prose.
- **Nothing validates `kill-candidates:` inside a row.** `102/181` rows carry it, but
  `scripts/check_backlog_filing.py:35` only matches it in a **commit message**. A row's clause can
  name a dead id and nothing notices.
- **Both commit-msg gates are scoped `-- BACKLOG.md`** (`check_backlog_commit_msg.py:44`,
  `check_backlog_filing.py:94`). Post-flip that is the **derived** file. Deleting a `tasks/*.md`
  source file is invisible to both.
- **The closure organs know nothing of `tasks/`.** `scripts/review_closures.py:183` and
  `plugins/tier1-lifecycle/scripts/review_closures.py:216` both call `validate_backlog.parse()`
  on `BACKLOG.md` text; `grep -n "tasks\|manifest"` over both returns only the local variable
  named `tasks`. [#442] (`BACKLOG.md:96`) is the witnessed incident of this class.
- **The prose/decision-register block is unschematised.** `validate_backlog.py` classifies any
  non-`- [#` line as prose; the `[E8]` R-table (`BACKLOG.md:359–371`) has no schema, no status
  enum, no id uniqueness check. Its own text records a minting discrepancy (no R9/R10/R11,
  `BACKLOG.md:372`) that was caught by hand, not by a gate.
- **`depends-on` is only checked when present.** Reference-existence and cycles are hard-fail
  (`validate_backlog.py:26–29`), but an obligation never written as a clause passes untouched —
  the [#452] finding (`BACKLOG.md:67`).
- **No ledger-completeness check.** See §ii id-allocation; [#440] and [#429] own the two holes.
- **PROPOSED observation:** the intake #17 §3.2 ruling raising the per-row cap 1200→1597 has
  **not landed** — `scripts/validate_doc_rot.py:58` still reads `_BACKLOG_GROSS_CHARS = 1200`,
  exactly as ADR-107 recorded at `:39–43`. Five rows sit at 1199. Any spike measuring "row
  pressure" is measuring against an unlanded ruling.

---

## (iii) The three obligations the [#433] row carries

The [#433] row points at `docs/decisions/README.md` (`BACKLOG.md:250`: *"**Carries the
pilot-precedes-contract ruling** + its three obligations (`docs/decisions/README.md`)"*). **There
are exactly three, and they are numbered as such.** Quoted verbatim from
`docs/decisions/README.md:134–149`:

> `:134` ### **Restructure pilots the pattern before the fleet contract** — operator ruling 2026-07-26
>
> `:136` **The backlog restructure PILOTS the schema pattern on one surface BEFORE [#382] declares the
> `:137` fleet desired-state contract.** A contract generalized from zero pilots is a guess; a contract
> `:138` generalized from one is at least grounded. Three obligations ride with it:
>
> `:140` 1. **The restructure ADR feeds its schema findings into [#382]** — the pilot is an input to
> `:141`    the fleet contract, not a parallel track that diverges from it.
> `:142` 2. **Its acceptance contract carries a generalization clause** — the pattern must be *shown*
> `:143`    to extend to at least one other governed surface. Shown, not asserted.
> `:144` 3. **The restructure structurally closes methodology-intake commission H** (id-space and
> `:145`    decision-record hygiene) — **the directory becomes the id counter**, so next-free is a
> `:146`    property of the tree rather than a scan that unmerged branches can defeat (the [#427]
> `:147`    collision class; [#429]).
>
> `:149` Carried by [#433]; received by [#382].

**Live disposition of each (per ADR-107 §6, `docs/decisions/ADR-107-…md:255–290`, and the ADR's
own post-flip amendment at `:456–459`):**

- Obligation 1 — **DISCHARGED**. `ADR-107:263–264`: *"**6.1 Obligation 1 — feed schema findings
  into [#382]: DISCHARGED** by §5 above (seven findings, routed, owed either way)."*
- Obligation 2 — **NOT DISCHARGED**, deliberately. `ADR-107:266–268`: *"**6.2 Obligation 2 — the
  generalization clause … NOT DISCHARGED, and deliberately not asserted.** One surface has been
  piloted end-to-end; a second has not."* Discharge criteria are fixed at `:270–274` (*"a second
  governed surface split by the same engine pattern — per-item frontmattered `.md` files with
  byte-exact identity, a residue manifest, and a green regen-and-diff round-trip — demonstrated by
  a committed round-trip proof, not by argument"*); named candidates at `:275–279`
  (`docs/intake/*.md`, then the `[E8]` register); owner is [#383] (`:280–284`).
- Obligation 3 — **RULED, not structurally discharged**. `ADR-107:285–286`: *"**6.3 Obligation 3 —
  RULED, NOT YET STRUCTURALLY DISCHARGED; narrow ADR-65 amendment required.**"* The retire-not-delete
  half executed at the flip ([#439]); `:290–292`: *"Commission H is structurally discharged only
  when retire-not-delete behavior and the duplicate-id ship gate are implemented and witnessed."*
  Both now exist (§ii above), so a morning architect may reasonably ask whether obligation 3 is
  now dischargeable — **PROPOSED, unresolved:** the ledger still has the two named holes ([#440]
  deletion-blindness, [#429] concurrent allocation), so "structurally discharged" is arguable
  either way and is an operator/architect call, not this dossier's.

**Consequently [#433] cannot close on obligations alone.** `ADR-107:376–379`: *"**7.5 [#433]'s
closure language.** [#433] does not close on this ADR alone. … [#433] remains open until that
obligation is demonstrated, or until the operator explicitly amends [#433]'s Done-when; an
explicit non-discharge is a disposition, not a discharge."* Reaffirmed post-flip at `:458`, and
in `docs/decisions/README.md:192–194`.

---

## (iv) DRAFT spike skeleton

**DRAFT — for architect review. Not authorized, not scheduled, not run.**

Working title: *`docs/audits/YYYY-MM-DD-verification-433-k-spike-2.md`* (genre + name shape per
ADR-101 R3/R4; the `verification` genre matches the 2026-07-27 predecessor).

### K1–K5 definition — OPERATOR INPUT, elicited at spike start, recorded here first

*(This placeholder section is reproduced verbatim as the task order specifies. **PROPOSED
amendment for the architect:** K1–K5 are already defined and already adopted as ADR vocabulary —
`docs/audits/2026-07-27-verification-433-schema-spike.md:14–27` records the operator paste
verbatim, and `docs/decisions/ADR-107-…md:99–108` adopts them. So this section may not need a
fresh elicitation of K1–K5 at all. What is genuinely un-elicited is **which spike this is** —
viewer-replacement probes vs the §6.2 second-surface proof. The architect should rule which
question the placeholder holds before anything is sent.)*

### §0 — Frame and authority
- What ruled this spike, when, by whom; the frozen scope; what it may NOT touch.
- Explicit: this spike rules nothing. ADR-107 is Accepted; step 4 stays DEFERRED
  (`ADR-107:456`); the viewer slot stays PARKED EMPTY (`ADR-107:456`).

### §1 — Criteria of record (carried, not re-derived)
- Restate K1–K5 + SCHEMA COMPOSABILITY by pointer to `ADR-107:99–108`, byte-unchanged.
- Record any operator amendment to them **as an amendment**, dated, never as a silent rewrite.

### §2 — Subject under test
- Either (a) a named candidate viewer at a pinned exact version installed **outside** the repo
  (ADR-107 §4 clause 1), or (b) a named second governed surface for the §6.2 proof.
- The four ADR-107 §3 re-entry criteria must be shown satisfied *before* a viewer is probed at
  all — otherwise the slot stays empty and the spike ends at §2.

### §3 — Method
- Probes run against a **byte-copy** of the real `tasks/` tree, never the live tree (the
  2026-07-27 method, spike §3).
- Verbatim command + verbatim output for every probe. No paraphrase.
- Read-only over the repo; any write happens in the scratch copy.

### §4 — Results, one labelled verdict per criterion
- `K1 PASS|FAIL — <evidence>` … through `K5`, plus `SCHEMA COMPOSABILITY`.
- Each verdict labelled **evidence**, not ruling (the 2026-07-27 discipline; the ruling stays
  with an ADR or an operator word).

### §5 — Baseline deltas against the current engine
- Anything §ii of this dossier records that the spike measures differently (file counts, manifest
  node kinds, id ledger state) is recorded as a delta with its cause, not silently overwritten.

### §6 — Obligation impact
- Explicit statement of what the spike does and does not move on obligations 1 / 2 / 3
  (`docs/decisions/README.md:140–147`), with the ADR-107 §6 dispositions carried forward.

### §7 — Residuals and open holes
- Carried forward by default: [#440] (ledger deletion-blindness), [#429] (concurrent
  allocation), [#452] (absent `depends-on` edge), the unlanded 1200→1597 cap ruling.

### §8 — What this spike did NOT authorize
- Named explicitly, in the ADR-107 §7.5 style, so a later session cannot read it wider.

---

### DRAFT elicitation question — FOR ARCHITECT REVIEW, NOT TO BE SENT

> **DRAFT. Do not send. Architect to approve, amend, or discard.**

Candidate phrasing, plain language, no code vocabulary:

> Right now everything on your to-do list lives in one long file. Each line has to do five
> different jobs at once: say what to do next, say what has to happen first, keep the history of
> what was decided, hold the decisions themselves, and carry the proof that something really
> happened. That is why some lines have grown to about a page of text — five of them are
> currently one character short of the limit we set.
>
> We already split that file into one small file per item, and we already tried one off-the-shelf
> viewer to read it. That viewer failed, so we are not using any viewer at the moment — the slot
> is deliberately empty.
>
> Before we spend any more time here, we need one thing from you, and only you can give it:
> **what would have to be true for you to call this finished and stop thinking about it?**
>
> To make that concrete, three smaller questions:
>
> 1. When you open your to-do list in the morning, what are you actually trying to find out — the
>    next thing to work on, why something is stuck, or what was decided and when?
> 2. If you never got a nice viewing tool for this — you just read plain files — would that be
>    fine, or is that the part that matters most to you?
> 3. We owe one more piece of proof: showing the same tidy-up works on a *second* kind of
>    document, not just the to-do list. Which second one would you actually feel the benefit
>    from — the incoming-ideas folder, or the record of decisions you've made?
>
> There is no wrong answer, and nothing changes until you say so.

**Reviewer notes on the draft (for the architect, not part of the question):**
- It deliberately does **not** ask the operator to define K1–K5, because those are already
  defined and adopted (`ADR-107:99–108`). Asking again would invite a silent redefinition of
  ratified ADR vocabulary.
- Question 3 mirrors the ADR-107 §6.2 named candidates in their stated order of cheapness
  (`ADR-107:275–279`) without naming paths.
- The "one character short of the limit" figure is live and checkable (`BACKLOG.md:27, :30, :55,
  :91, :397` at 1199 chars vs `scripts/validate_doc_rot.py:58`), but see the §ii caveat: the cap
  itself is an unlanded ruling. The architect may want that qualifier added or the sentence cut.

---

## GAPs

- **GAP: no code implements `next_free`.** The rule exists only as prose (`ADR-107:305`,
  `tasks/README.md:59–61`); no script computes it, so the allocation step is manual and
  unwitnessed. Detection-only enforcement is the whole mechanism.
- **GAP: the operator's intended meaning of "the K1–K5 spike" on the [#433] row cannot be
  determined from the repo.** The row's own text (`BACKLOG.md:250`) says the term is undefined
  in-repo and the spike records it first; the spike then ran and ADR-107 adopted the definitions.
  Whether the Done-when clause is already satisfied by the 2026-07-27 artifact, or points at a
  future re-run, is an operator/architect question — the files do not settle it.
