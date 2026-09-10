=== HANDOFF_BOOT.md (session header) ===

# Handoff boot — session header + paste-pointer (architect mode)
<!-- scope: meta -->

| Field | Value |
|---|---|
| **Slug** | `2026-09-10-dev-knowledge-architect` |
| **Chat title** | `[dev-knowledge] Technical Architect — 2026-09-10-dev-knowledge-architect · SEQ 1` — name the fresh browser chat this (bump `SEQ` per parallel chat) |
| **Mode** | **architect** (HANDOFF_PROCESS §13 — planning / way-of-working scope) |
| **Purpose** | <!-- FILL-IN:purpose START (hand-authored — ~3 sentences + a BACKLOG pointer; a session HEADER, NOT a second residual; the generator never writes this) -->Rule the seven OPEN R1 rulings the 2026-09-09 night mission returned, and the five operator words it could not answer for you. The window that precedes this one closed three acts (the night bundle landed as audits, the window-close intake confirmed, HANDOFF_PROCESS bumped to 7.1.0) and deliberately ruled nothing the mission raised. Start at `docs/audits/2026-09-10-technical-night-aj-m03/REVIEW.md`, which is built to be read first and states its own evidence ratio against itself. The rows this frontier moves against are `[#644]` (the deploy freeze, and `REVIEW.md`'s finding #1), `[#664]`, `[#676]`, and the two filed this window, `[#679]` and `[#680]`. Queue and owners: `BACKLOG.md`.<!-- FILL-IN:purpose END --> |
| **Destination** | worktree <!-- FILL-IN:dest-worktree START (hand-authored — the worktree name, or `none (primary tree)`) -->`none (primary tree)`<!-- FILL-IN:dest-worktree END --> · branch `main` · write-scope <!-- FILL-IN:dest-scope START (hand-authored — what this lane may write; PROSE, deliberately outside P3) -->rulings and their carriers - `docs/decisions/`, `docs/intake/`, `tasks/` + the `BACKLOG.md` regen, `protocols/STANDING_RULINGS.md`. NOT the night bundle: `docs/audits/` is immutable and `REVIEW.md` is evidence to rule ON, never to edit.<!-- FILL-IN:dest-scope END --> · MODE **architect** — basis <!-- FILL-IN:dest-mode-basis START (hand-authored — WHY this mode, per ADR-87 item 5; PROSE, deliberately outside P3) -->architect per ADR-87 item 5 - the frontier is decisions with no in-repo carrier, not a named backlog item to advance. Six of the seven open rulings need a ruling before any lane can be chartered, and REVIEW's finding #1 is that our decisions have no state carrier at all.<!-- FILL-IN:dest-mode-basis END --> |
| **Generated at** | Bundle cut by `scripts/gen_handoff.py` from **committed** repo state on branch `docs/window-close-handoff`. This line names only which branch was checked out — it states **no** sha, count, or verdict. **Re-derive HEAD / tree-clean / branch / ahead-behind live** (`PROBES.md` P3). |

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

> **The `Destination` row is declared ex-ante** — a lane inherits none of it. Only its **branch**
> field has a mechanical counterpart (`PROBES.md` **P3**; mismatch = FAIL). Worktree, write-scope
> and MODE-basis stay prose and carry no probe leg — a leg that cannot fail honestly discredits
> the block (R3).

> **Nothing doctrinal is copied into this paste — five pointers, one hop each.** Launch commands:
> `protocols/PLAYBOOK.md` Ch8 "The dispatch table — the SOLE literal-command site" (**copy** a row;
> a composed line is the defect class that cost ~30 consecutive seats their lane —
> `STANDING_RULINGS.md` §V). Dispatch prep, batching, completion: Ch8 "Handoff prep for the next
> architect". Standing rulings applied without asking: `protocols/STANDING_RULINGS.md`. Operator
> runbook (who each file is for, the run loop): `docs/handoffs/README.md` — bundles carry no
> per-bundle README. Anti-bluff contract: this bundle's own `PROBES.md` header, spec
> `HANDOFF_PROCESS.md` §5. Ask CC to pull any of them.

---

=== ROLE PIN (protocols/HANDOFF_BOOT.md — RESIDENT, not inlined) ===

ROLE PIN — HANDOFF_BOOT.md @ handoff-process v7.1.0
sha256: a9a5a7a86408ef3bea3c4fdbac4cdf8fde3dff0c042ebb1e0c165357c0b0ed71
If your project instructions do not carry this contract at this version+sha, say so before answering.

---

=== RESIDUAL.md ===

# Residual — 2026-09-10-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.
>
> **Supplement fill-state:** stated once, in this bundle's `HANDOFF_BOOT.md` session header
> ([#611] — not duplicated here).

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

> **Standing vs NEW — generated, names only.** Three lists computed from `ecosystem/disposition-register.yaml` ∩ this window's own diff. **No verdict, count, stale-disposition line, sha or backlog id appears here** — those are P7/P4/P6/P9's live answers and the evidence block carries them. The frame covers the standing-WARN family only; an organ outside it is the FILL-IN's business, not silently filed as standing.

**Window** — the diff since `docs/handoffs/2026-09-08-dev-knowledge-architect-2/` was added.

**Dispositioned by the register.** The register already carries an entry for these organs, so a WARN from one is standing unless its evidence signature is new:
- `no_ff_merges`
- `journal_spine_anchor`
- `doc_rot`
- `undeclared_edges`
- `funnel_coverage`

**Dispositioned by absence from the window diff.** This window touched nothing these organs read, so a WARN from one is not this window's doing:
- _(none)_

**NEW-and-undispositioned.** No register entry, and this window DID touch what they read — so a WARN from one of these is this window's, and the note below says which is a decision rather than a defect:
- `reconciled_versions` (reads the registered specs and the docs declaring a `reconciled_with:` edge)
- `fleet_parity` (reads the parity-surface manifest and the surfaces it names)

<!-- FILL-IN:driftflags START (hand-authored — ONE judgment only: name which NEW flag above is a DECISION rather than a defect. The standing-vs-new attribution is GENERATED directly above; do not restate it. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->**`reconciled_versions` is the DECISION, not the defect.** This window executed the bump the
previous window recorded as OWED: `HANDOFF_PROCESS.md` `Version:` 7.0.0 -> 7.1.0 under
`DECLARE-SITTING-2026-09-08` ruling 9, with every `reconciled_with:` dependent re-stamped in the
same coupled act and the ROLE PIN re-issued. This organ was touched deliberately, by a ruling with
an owner, and the act is recorded in the spec's own Section history. **`fleet_parity` is the other
NEW organ and is NOT claimed as a decision** - this window added no parity surface, so anything
from it is a defect to investigate rather than a filed obligation, and P7 is what says whether it
fired. No verdict, count or `[stale]` value is stated here; P7/P4 re-derive them.<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->Three acts landed on `main`, each a `--no-ff` merge with its own JOURNAL anchor; `JOURNAL.md`
2026-09-10 (a) and (b) carry the detail and this map does not repeat it.

- **The 2026-09-09 night mission bundle** -> `docs/audits/2026-09-10-technical-night-aj-m03/`.
  Audits only, verified by diff: no script, protocol, manifest or task row. Evidence for `[#582]`,
  `[#661]`, `[#676]` by its own closing section. Its branch is **deliberately retained** until the
  operator has read `REVIEW.md`.
- **The window-close rulings intake** was CONFIRMED already on `main` (intake #90), not re-landed.
  It carries three of the four transports; the fourth is named in section 4 as pending.
- **`HANDOFF_PROCESS` 7.1.0** - ruling 9's OWED bump, as ONE coupled release act. Carries **no new
  normative section text**; intake **#68**, the v7.1 amendment pack, stays DRAFT and unratified and
  nothing in it is adopted. ADR-82 remains the deciding ADR; no ADR was added or amended.
- **`[#679]` filed** - an architect ruling that answers a `QUESTION-*.md` does not write the
  `disposition:` back onto the file that asked, so the ruling is given and not landed.<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->### The night bundle is the frontier, and it is evidence to rule ON

`docs/audits/2026-09-10-technical-night-aj-m03/` - **read `REVIEW.md` first**; it is built to be,
and it states its own limits before its findings. **Its evidence ratio, as the bundle states it
against itself: 24 locators independently verified against ~220 carried UNVERIFIED** - roughly one
in ten, on a denominator that is itself soft, because four of the six leg-1a row counts are
approximations in the source table. Only leg 1c (`codex`) was checked adversarially and **three of
its twenty-four locators were defective** - the rate `REVIEW.md` instructs a reader to assume for
the ~220 that were not checked. Its own consequence, quoted rather than paraphrased: *"no reader's
table should be cited downstream as though it had been checked."* The dagger marks travel with
every unverified claim; stripping them converts an argument into a false citation.

### Seven R1 rulings are OPEN. The mission raised them; this window ruled none

Counted at seven rather than six: the two questions inside leg 1e are separable and are listed
apart, because the first is expensive and the second is not.

1. **LEG 1d (`grok`) UNFULFILLED** - is an in-repo re-measurement an acceptable arbitrator of a
   disagreement it is one half of? Lane v-664's 39 is one of the two numbers in dispute. Re-run on
   a paid account, or the DELETE LIST stands permanently at its current length with the remaining
   census orphans untouched.
2. **LEG 1e (`cursor-agent`) UNFULFILLED, first question** - is `.claude/settings.json:21` fixed
   before any non-Claude reader is ordered again? Attempts 1 and 2 were **our** fault, not the
   vendor's: two paid runs were burned discovering a defect in our own configuration.
3. **LEG 1e, second question** - is the cannot-fail-test scan re-run on a paid reader, or
   reassigned to the synthetic-flawed-item mechanism, which answers it with no reader at all?
4. **The `codex` reviewer role** - does the read-only L0 doctrine bind `codex` when it is ordered
   as a **deriver** rather than a reviewer? 85,017 tokens of real derivation were done and
   discarded before the deliverable was changed to stdout. *"The caller was never warned; the
   money was spent first."*
5. **`agy`'s file-write mode** - banned for ordered legs? Two of six legs printed `DONE` at exit 0
   and wrote nothing: *"silent write failure reported as success - the worst shape, because
   nothing downstream can tell."*
6. **The registry contradiction** - `ecosystem/provider-registry.yaml` records `grok` as
   PAY-PER-CALL, measured 2026-08-26; the night's refusal names a free tier with a usage limit.
   Both cannot describe the same account. Not repaired by the bundle. The consequence for
   `[#676]`: a **fifth** outcome exists - reachable, correctly invoked, refused for quota - which
   the current four-way split would file as "answered" or "unreachable", both wrong.
7. **Contamination** - `MISSION-PROMPT.md` was committed into the tree the readers were auditing
   **before** legs 1d/1e ran, and attempt 1's reply quotes the mission's own phrase. No leg is
   known to be affected; the possibility is on the record. Acceptable, or are the affected legs
   void?

**Recorded, not a ruling:** the branch-prefix deviation. The mission specified
`night-aj-m03-review`; the closed enum admits only `worktree-<name>`, so the branch carries the
prefix and the worktree carries the mission's name. The operator's own merge instruction used the
prefixed name, which reads as ratification - say so if it was not.

### Rows this frontier moves against

`[#664]` `[#673]` `[#674]` `[#675]` `[#676]`, plus `[#679]` and `[#680]` filed this window.

**One citation defect, named so it is not inherited:** `DECLARE-JOURNAL-DECISION-2026-09-09`
section 5 cites `[#675]` for a minutes-to-merge measurement. Live `[#675]` is *"manifest tooling
reads a heterogeneous node list with a bare `.get` default"* - a different row entirely. A bare id
resolved into the wrong namespace, so that DECLARE's measurement has no live carrier.

### The recovery intake, and the map that does not exist

Steps **A-G** are `docs/intake/2026-09-09-tech-recovery-plan.md` section 4. Its `:24` ratio -
*"8 of 16 loop stages mechanical"* - is the **fullest in-repo description of the 16-stage
universalization order**, and **the order itself is enumerated nowhere**. `REVIEW.md` section 1
row 4 pays for that directly: the bundle's whole stage-12/stage-15 analysis carries a caveat
because those names are taken from the mission prompt's own gloss. A ship named by its stage
number, in an order that is not a document, cannot be sequenced against anything.

### The operator's five open words

- **GitHub Pro.**
- **Orphan deletion** - BLOCKED, and the blocker is ours: the census population is contested by
  our own two measurements, 32 against 39, one day apart, unreconciled. `MATRIX.md` section 5.2
  refuses to act on it in those terms - *"Deleting on a contested census is how a real caller gets
  removed."* `file_purpose_graph.py`, wired by v-664, is the existing organ that should own the
  count.
- **The five DEAD PLAYBOOK sections** - marked DEAD 2026-09-09, disposition still owed. They are
  sections 1, 6, 9, 12 (**config hierarchy only**) and 13 (**Obsidian row only**); the scoping is
  deliberate, because the operator ruled those parts and not the sections containing them.
- **The 2026-08-29 deploy freeze** - `[#644]`, and `REVIEW.md`'s **finding #1**: the single named
  blocker on Stage 10, never put to the operator, and the document that measures the delay
  (`DECLARE-REVIEWS`) does not exist under `docs/`, `protocols/`, `tasks/` or `deploy/`.
- **JOURNAL's verb** - UNDECIDED, and now provably so rather than merely open.
  `DECLARE-JOURNAL-DECISION-2026-09-09` section 5 makes the night mission's DELETE-LIST **row 0**
  the decider: *which process READ JOURNAL in the last 30 days for anything but checking JOURNAL
  was written.* **That row was never produced.** No reader found is not the same as no reader.

### Stated plainly, including where the incoming brief was wrong

- **`ARCHITECTURE.md` and `protocols/PLAYBOOK.md`: bodies unchanged this window - but not
  untouched.** Act 3 moved frontmatter only: `ARCHITECTURE.md` two lines (`last_reviewed`,
  `reconciled_with`), `PLAYBOOK.md` one (`reconciled_with`). Zero body or content change to
  either. "Unchanged" is true in substance and false to the byte, and the byte is what a diff
  shows the next reader.
- **Three husk directories remain under `.claude/worktrees/`** - `lane-provider-liveness-probe`,
  `lane-v-000-offload-admission`, `lane-v-643-enforcement-debt`. `git worktree list` shows
  **primary only**, so all three are unregistered husks rather than live trees.

### Carried debt - named here rather than cleared, because a window may hand off with debt only when the debt is explicit

**The undispositioned ship-gate WARNs, by organ and owning row.** No verdict, count or `[stale]`
value appears here - P7 re-derives all three live. Enumerated from one `audit.py ship-gate` run
this seat made and read in full, the organs carrying undispositioned WARNs, each with the owner
that should absorb it:

- `consumer_at_landing` - the largest family by a wide margin, and **not one defect**: most of its
  rows ARE dispositioned by the batch-T/batch-U manifests and the R-citer pending set
  (`to-cc/DECLARE-R-CITER.md` section 2). What survives undispositioned is the residue, of which
  `SEED_RUBRIC.md` and `VERDICT_RULE.md` are the named members - each cited by no governance
  surface and in no arm-time baseline. Owner: the R-citer arc.
- `proof_layer` -> `[#638]`. A property gated behind a function-level `skipif` on `git` in
  `tests/test_review_artifact_coverage.py`. The fix is to move the property out from behind the
  guard, or make a skipped proof render as NOT-PROVEN - never to suppress it.
- `review_artifact_coverage` and `doc_code_edge` - the same review-artifact arc as `proof_layer`;
  they travel with `[#638]` rather than owning a row of their own.
- `doc_claims`, `canonical_freshness`, `generated_artifact_freshness` - the freshness/claims
  family. `canonical_freshness`'s live row is `protocols/PLAYBOOK.md` reading *ungated-and-stale*
  by one day (a prose stamp, declared 2026-09-08, derived 2026-09-09), which predates this window
  and is ungated. No owning row exists for the trio; the first sitting should assign one.
The register-dispositioned families - `no_ff_merges`, `journal_spine_anchor`, `doc_rot`,
`undeclared_edges`, `funnel_coverage`, and `adr_status_grammar` - are standing, and section 1
attributes the first five. **`adr_status_grammar` is called out here only to kill a plausible
misreading**, because this seat made it first: its WARN looks like an ADR with a bad status and is
not one. It is a **baseline-ratchet report** carrying `0 enum/single-field defects`, dispositioned
by `warn-adr-status-grammar-ratchet-holding-v2`. ADR-118 is not its subject - that ADR's status
line reads `Proposed`, which IS a member of the enum, with a comment recording that the operator's
own word was DRAFT and that `DRAFT` is not in the enum. Nothing there is owed.
**Where the evidence stops:** this list is organ-level, taken from one run at one SHA. Which
individual rows remain undispositioned is what `python scripts/audit.py ship-gate` answers at
read-time, and that run is the authority over this list.

**Three decision files on the transport are OPEN carriers, named because P11 requires it and
because omitting them is exactly the defect they describe:**

- `to-cc/DECLARE-HARNESS-IS-PROCESS-2026-09-08.md`
- `to-cc/DECLARE-HARNESS-PROVENANCE-2026-09-08.md`
- `to-cc/DECLARE-DISPATCH-SEAM-AND-ENTERPRISE-2026-09-08.md`

The first is **`REVIEW.md`'s finding #1 in its purest form**: `DECLARE-HARNESS-IS-PROCESS` is
cited as authority by **three committed audits** - the process-trigger census at its line 4, the
v-642 assembly-debt lane and the v-643 enforcement-debt lane - and a glob for it across the
repository returns **zero matches**. A reader of those audits cannot check what commissioned them.
`MATRIX.md` section 0 treats this class as the mission's most important output and this residual
agrees: *"our decisions have no state carrier"* is upstream of "we lack a runner", because a
conductor that executes phases still needs to know what was decided.

**`DECLARE-JOURNAL-DECISION-2026-09-09` is PENDING, not landed, and is deliberately absent from
`main`.** It is `carried-by: BACKLOG.md`, a different home from the window-close intake, and it is
cited nowhere in the repository. Two independent reasons it was not landed, both from the document
itself: its section 6 requires *"One terra-reviewed lane, V+1, after the night's row-0
measurement. Not an evening word: it changes the spine"*, and its section 5's deciding measurement
was never produced. Landing it as an evening act would have contradicted its own text.

**A new defect, found by trying to land this bundle.** The generator emits `FUNNEL_HEALTH.md` and
the five `SEAT-BOOT-*.md` pastes from `templates/handoff/seats/`, and none of those templates
names an owning row - so `[#664]` clause 2's task-coverage gate refuses the commit of **every**
architect cut that carries them. Same shape as `[#679]`: a mechanism producing artifacts that
nothing claims. Filed as `[#680]`, which owns the defect and names the files.<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.

---

=== PROBES.md ===

# Probe manifest — architect mode: orientation first, then teeth (HANDOFF_PROCESS §5 + §13c)
<!-- scope: meta -->

> **Contract, rationale, execution order, escalation ladder: `protocols/HANDOFF_PROCESS.md` §5 —
> there ONCE ([#611]).** Every row ships a **question + source-locator + command**, never an
> answer. CC runs the whole set against live state via `/handoff-verify` and emits **one evidence
> block**. **Any FAIL blocks onboarding; a missing required row is not a pass.** Table order IS
> execution order. Cut on `docs/window-close-handoff` — which branch, not a value; re-derive live (P3). Run
> with `PYTHONUTF8=1`, and verify `ship-gate` (P7) in git-bash — a bare cp1252 PowerShell console
> false-REDs `handoff_probes`.

## P0 — Standing-topic reconciliation (above P1 — A7 / R2; rationale §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P0a | Quote, **substring-exact**, the theme-preamble line of each **active** `[E#]` theme in `BACKLOG.md`, and confirm the generated backlog is **CURRENT**. | `BACKLOG.md` `[E#]` theme headers + each preamble line | preambles drift on any theme edit, and a generated file can be stale | `grep -A1 '^## \[E' BACKLOG.md` → each quote substring-matches (a paraphrase FAILs); then `python scripts/gen_task_tree.py --check` exits 0 |
| P0b | Enumerate live the docs under `docs/intake/` with `status: ACCEPTED`, and quote each one's **TITLE line**. Titles only (§5). | `docs/intake/*.md` frontmatter + first heading; areas at `docs/intake/README.md` | the set and its titles drift on any status change; neither is in this bundle | `grep -l '^status: ACCEPTED' docs/intake/*.md` then read each hit's first heading |
| P0c | Does this bundle's **Purpose** NAME an authority the P0a/P0b enumeration returned? No match = **FAIL**. | `docs/handoffs/2026-09-10-dev-knowledge-architect/HANDOFF_BOOT.md` Purpose ∩ live P0a/P0b output | Purpose is hand-authored, the authorities are live; computable only after P0a and P0b run | `sed -n '/FILL-IN:purpose/,+1p' docs/handoffs/2026-09-10-dev-knowledge-architect/HANDOFF_BOOT.md` → it names an enumerated authority, or FAILs |

## P1 — Orientation (the architect's **first move** — §13c)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P1a | Quote, **substring-exact**, the opening sentence of `README.md` `## Vision` — what .dev-knowledge is. In a child repo still on `VISION.md`, re-bind the path (ADR-114). | `README.md` `## Vision` | a paraphrase is not a substring; a summary rounds it off | `grep -A4 '^## Vision' README.md` → the quote must be a substring |
| P1b | Quote, **substring-exact**, the opening line of `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`) — where this work sits. | `ARCHITECTURE.md` `## Purpose [CORE]` | the line is in the live file only; a summary holds a gist | `sed -n '/^## Purpose \[CORE\]/,+5p' ARCHITECTURE.md` → the quote must be a substring |

**Gate:** no design until both orienting lines are held, read live and substring-matched. Then the
operator-context beat fires (§13d).
This bundle's supplement is **generated EMPTY**, so the beat fires **FULL** — *"what off-repo context: intent, priorities, findings not in the repo, changed decisions?"* — not a narrowed "anything changed since?". (If the operator runs `supplement filled`, its ANSWERS fold in and the beat narrows.)

## Teeth probes (state fidelity — answers withheld, §5)

| # | Probe (question) | Binds to (primary source) | Why a summary can't answer it | CC verifies via |
|---|---|---|---|---|
| P2 | How many checks are in `ALL_CHECKS`, and what is the registry **name** of the last one? | `ALL_CHECKS` in `scripts/audit.py` | count and last name drift every time a check lands | `python scripts/audit.py checks` |
| P3 | Short **HEAD sha**, tree clean?, **branch** checked out, `main` **ahead/behind** `origin/main` — and does the live branch match the **Destination** row's branch field? Mismatch = **FAIL**. | live git ∩ the **Destination** row of `docs/handoffs/2026-09-10-dev-knowledge-architect/HANDOFF_BOOT.md` | Destination is declared ex-ante, the branch is read now | `git rev-parse --short HEAD`, `git status -sb`, `git branch --show-current`, `git rev-list --left-right --count origin/main...main` (the fourth leg is REQUIRED — §5), then compare against `docs/handoffs/2026-09-10-dev-knowledge-architect/HANDOFF_BOOT.md` |
| P4 | Which `#id`(s) does `validate_git_backlog` flag **now**, and the **full short-sha** of each closing merge? | live git ∩ `BACKLOG.md` | the set is computed at answer-time; the sha is high-entropy and in no document | `python scripts/validate_git_backlog.py` |
| P5 | Is `ARCHITECTURE.md`'s `last_reviewed` **on/after or before** its last commit touch — and the **two dates**? | `ARCHITECTURE.md` frontmatter + live git | a relation over commits; a summary holds neither date precisely | `git log -1 --format=%cs -- ARCHITECTURE.md` vs the frontmatter stamp |
| P6 | What does `validate_doc_claims` report for **`pytest_collected`** — doc integer, live integer, do they match? | `ecosystem/doc-counts.md` (`doc=` target) + live pytest | the live count drifts on any test change; neither integer is in this bundle | `python scripts/validate_doc_claims.py` (the `pytest_collected` line) |
| P7 | Is `audit.py ship-gate` **GREEN or RED** now, **how many WARNs are dispositioned**, any `[stale]` disposition? | live git ∩ `main` history ∩ `ecosystem/disposition-register.yaml` | the §1 headline, computed at answer-time; one direct-on-`main` commit re-REDs it | `python scripts/audit.py ship-gate` — read the verdict, the disposition count, any `[stale]` line; do **not** trust the residual's prose |
| P8a | File count of this bundle, is `SUPPLEMENT.md` present, ANSWERS empty or filled — and does each filled answer **CITE A FILE** (repo or transport path) rather than a chat turn? Chat-only = **FAIL** (§5). | `docs/handoffs/2026-09-10-dev-knowledge-architect/` listing ∩ `protocols/HANDOFF_PROCESS.md` §13 | a summary holds a stale count or fill-state; the citation form is readable only in the live text | `ls docs/handoffs/2026-09-10-dev-knowledge-architect/` ∩ `grep -A3 'PASTE CHAT ANSWERS' docs/handoffs/2026-09-10-dev-knowledge-architect/SUPPLEMENT.md` — substantive text below the divider, each answer naming a path |
| P8b | For the transport's `STATUS-<seat>.md` files: each one's **byte size**, and is its **first `## ` heading** the "now" section? Over **5,000 bytes**, or a first heading that is not "now", = **FAIL** (§5 — the threshold is bytes, not an ambiguous "5 KB"). | the live transport dir ∩ the grammar table in `protocols/OPERATOR-INTERFACE.md` `## 1. File exchange goes through the Downloads directory` | these belong to files written after this bundle was cut | `ls -l "$env:CLAUDE_PROMPTS_DIR/to-browser"` then `grep -n -m1 '^## '` per hit — report size + first heading each |
| P9 | How many **serialize-groups** does `validate_backlog` summarize **now**, and which `#id`s are in the **code-edge** and **coherence** groups? | `BACKLOG.md` ∩ `scripts/validate_backlog.py` | group membership drifts on any BACKLOG edit and is absent here | `python scripts/validate_backlog.py` (the serialize-groups line) |
| P11 | For the window's decision files on the transport (`DECLARE-`, `AMEND-`, `BATCH-` prefixes): does a **flush-left `carried-by:`** appear in the file HEAD, and does its value name a repo home that **resolves on `main`** or state the literal `OPEN` (an `OPEN` being named in this bundle's residual)? Neither = **FAIL**. **Anchored and valued — a bare substring match is NOT this check** (§5). | the live transport dir ∩ `protocols/HANDOFF_PROCESS.md` §5 ∩ `docs/handoffs/2026-09-10-dev-knowledge-architect/RESIDUAL.md` | written after this bundle is cut: neither the file set, nor a carrier value, nor the residual's naming of them exists here | in the transport dir, per decision file: `head -6 "$f" \| grep -m1 -E '^carried-by:'` — an empty result is the FAIL set (the HEAD window and the `^` anchor are both load-bearing; `grep -l` over the whole file is a different and broken check, §5). Then take the value: `git cat-file -e main:<path>` for a path, else match the literal `OPEN` in `docs/handoffs/2026-09-10-dev-knowledge-architect/RESIDUAL.md`. Report per file WHICH value resolved and from where |

## Gate procedure (CC)

`protocols/HANDOFF_PROCESS.md` §5 — "Who runs it" + "Execution order" ([#611]). Table order IS the
execution order.

---

=== END OF PASTE — 4 sections · 30456 bytes ===
