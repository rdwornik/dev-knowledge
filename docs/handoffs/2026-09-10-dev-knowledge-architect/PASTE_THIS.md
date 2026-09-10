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

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

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

## AMENDMENT 2026-09-10 (supplement fill) — the incoming seat's first act

> In-file amendment marker, not an in-place edit: this bundle is immutable and this block is
> appended at the fill step, alongside the transcription of `SUPPLEMENT.md`'s ANSWERS.

**`DECLARE-HARNESS-IS-PROCESS-2026-09-08` is still absent on `main`, and that is the incoming
seat's first act.** Re-checked at fill time, not assumed: `git ls-tree -r --name-only main` returns
**no file** matching `HARNESS-IS-PROCESS` anywhere in the tree, while the name is cited on `main`
by `docs/audits/2026-09-08-technical-process-trigger-census.md`,
`docs/audits/2026-09-09-technical-lane-v-642-assembly-debt-rows.md` and
`docs/audits/2026-09-09-technical-lane-v-643-enforcement-debt.md` — the three committed audits the
supplement's Q7 names — plus `JOURNAL.md` and the night bundle. The ruling that defines what a
harness *is* — the reframing §6(a) of the supplement calls "upstream of every other decision in the
window" — lives only on the transport. **Land it before anything else: an intake or an ADR, with
the three audits' citations then resolving.** Until it lands, three committed audits cite an
authority their reader cannot open, and the row that would own it does not exist.

**Two further fill-time findings, recorded here because they change what the next seat should
believe about this bundle:**

- **Q4's claim that the 16-stage delivery-loop order is enumerated nowhere is CONFIRMED against
  `main`.** No stage number above 10 appears anywhere outside the night bundle. The fullest in-repo
  description remains `docs/intake/2026-09-09-tech-recovery-plan.md:24` — *"8 of 16 loop stages
  mechanical"* — which is a ratio, not an order. A seat cannot execute a loop it cannot enumerate,
  so Q4's "either enumerate it or stop citing it" is the live disposition, unchanged.
- **Six of Q7's seven "interface behaviours not yet named in `protocols/OPERATOR-INTERFACE.md`"
  were struck at transcription because that file already names them**; only **named-session
  addressing** survives as genuinely absent. The per-row citations are in `SUPPLEMENT.md`'s
  transcription note. Two substantive residues survive their strike and are real work: the
  documented END-OF-PASTE sentinel is the bare `=== END OF PASTE ===` while the live assembler
  emits `=== END OF PASTE — n sections · b bytes ===`, and the documented model-switch lines carry
  no explicit *stay / return / switch* verb, which is the ambiguity the operator actually reported.

---

## AMENDMENT 2026-09-10 (window-close cleanup) — the paste is 2.7x its target, and two rows are filed

> Second in-file amendment marker, appended at the cleanup act. The first amendment (supplement
> fill) stands unedited above; this one adds to it rather than revising it.

**`PASTE_THIS.md` is 55,340 B against a 20,000 B target — 2.7x.** Known, reported, and **not a
blocker**: the ceiling is a target rather than a gate (`DECLARE-BOOT-REVIEW-2026-09-08` ruling 3),
and the growth is the folded supplement, which is the operator-authored payload this bundle exists
to carry. It is named here because it is **the same class the operator already ruled a defect on
the 22 KB SEAT-BOOT** — a boot artifact whose size is re-billed on every browser turn — and a class
does not stop applying when the oversized artifact happens to be the one we wanted. The next seat
inherits the cost, not a decision.

**Two rows were filed from this bundle's own consistency checks**, both surviving the strike that
removed the behaviours around them: **`[#681]`** — `protocols/OPERATOR-INTERFACE.md` documents the
bare `=== END OF PASTE ===` while the assembler emits the counted form, and its model-switch line
carries no explicit *stay / return / switch* verb; **`[#682]`** — named-session addressing is
absent, so nothing tells the operator which session a paste belongs to. Being documented is not
being correct, and `:83` "A chat paste is not addressable" argues ownership of the work, not
addressing of the paste.

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
The operator has **filled** the supplement, so its ANSWERS are in the paste and the beat **NARROWS** to *"anything changed since the supplement was written?"*.

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

=== SUPPLEMENT.md ===

## 1 · Strategic intent — what the next session should achieve at the way-of-working level

**Subtract and connect. Prove the harness on a consumer, not on itself.**

This window MEASURED. It did not connect and it did not subtract. The census (216 processes,
160 triggered, 32 orphan), the armed FPG-1 spine, the Windows baseline, the 16-stage loop map,
the chapter map — every one of them is an instrument, and instruments were the right thing to
build because nothing could be deleted honestly without them. But the operator's own verdict
stands: *"Ty tylko dodajesz i dodajesz."* Thirteen decision files, eight merged lanes, twenty
new rows, and **zero bytes removed from the corpus and zero bytes delivered to a consumer repo.**

So the next window's way-of-working rule, and it should be enforced at dispatcher step 0 rather
than remembered:

> **Every lane either DELETES something or CONNECTS two organs that already exist. No lane adds
> a new organ. A contract whose Done-when contains no number that goes DOWN, and no edge that
> joins two existing things, is refused.**

And the window's own success metric is not a repo metric. It is **operator hours to land one
feature in corp-monorepo** — today infinite, because Stage 10 of the delivery loop has never
fired. A window that improves hub hygiene and leaves that number infinite has failed on its own
terms, however clean its close packet.

The methodological target underneath: make **"declared enforcement without enforcement"**
extinct by mechanism. Nine-plus instances were witnessed in two days — P11 specified with no
code · `asserted_by` naming a non-reading organ · `test_logs_retention` asserting `is not None` ·
the generator↔verb seam whose own docstring claimed it could not drift · two resolver copies ·
`[#563]`'s test grepping a name to prove a relationship · a drift probe matching the literal
`--report` · `.get(key, default)` over a heterogeneous node list · a ruling that never travelled
back to the question that asked it. These are not nine bugs. They are one bug with nine faces:
**a claim about a relationship that nothing verifies.** The spine exists now to check exactly
that class, and the next window's highest-leverage act is to point it at itself.

## 2 · Tensions weighed, where this seat landed, and why

**(a) Boot forensics vs planning.** The window opened on a failed gate (`-1` and `-2` both
failed P11) and this seat gave five turns to forensics before planning. **Landed: ONBOARDING
BLOCKED blocks rulings and dispatch — it does not block planning.** Recorded as a defect against
this seat, not against the gate. The incoming seat should plan from turn two even if the gate is
red.

**(b) State location — repo files vs GitHub Issues.** Weighted matrix, five options, ten
criteria (`DECLARE-CONDUCTOR-DECISION-2026-09-09`). **Landed: E — state stays in `tasks/`,
GitHub Actions becomes the runner, required checks become the gates.** Rationale: Issues would
have scored well on deletion but broke "decisions are files" and added lock-in; E takes the
runner without moving the state. **Caveat that arrived after the decision: the account is on
GitHub Free and rulesets return 403, so E's GATE leg is unavailable without Pro (~$4/mo). E's
runner leg is unaffected.** The operator's word is owed.

**(c) Dispatch — move to the hub, or retire.** **Landed: retire, do not move.** Moving it into
the hub breaks ADR-28 (the hub is passive storage and governance, not an orchestrator). The
error being corrected is older and subtler: the hub's process needed a runner and the hub had
forbidden itself from having one, so the runner went to win-tooling — a repo with no floor. That
is why the harness's hands lived for months in ungoverned code with two resolver copies and a
deployed module from an unmerged lane.

**(d) Baseline substrate.** Codespaces (44 RED) vs Windows (28 RED). "28 == 28" was arithmetic
coincidence and the integrator was right to refuse it. **Landed: the gates ship against Windows,
therefore Windows is the baseline.** Codespaces keeps a real role — fast read-only compute, a
RED *list*, never a verdict.

**(e) JOURNAL.** Keep / render / delete / window / PR-as-anchor, matrix with seven criteria.
**Landed: B — the anchor is a property of the commit (`[#id]` + a body), the pre-push gate reads
commit messages, and `JOURNAL.md` becomes a render of `git log --first-parent --merges`.**
Deliberately NOT landed as a repo change: it amends ADR-85, which is spine, and its own decider
(the night's DELETE-LIST row 0 — which process READ JOURNAL in 30 days for anything but checking
it was written) **was never produced**, so the verdict is provisional by construction.

**(f) Batch V's lane list.** V-7 (FPG-1 spine) was swapped out for V-8 (offload admission) on
the operator's "Enterprise is a priority". **This seat now judges that swap wrong on the merits:**
the spine returned as V-9 in the same batch anyway, so the swap bought nothing and briefly
removed the single most important lane from the plan. Recorded so the next seat does not repeat
the pattern — *a priority ask is a reason to add a lane to the next batch, not to displace the
critical path from this one.*

**(g) Speed vs measurement on deletion.** The census counted 32 orphans on 2026-09-08; something
counted 39 on 2026-09-09; nothing reconciled them. **Landed: do not delete on a contested count.**
Only three deletions survive unambiguously (three `SUPERSEDED` OneDrive hook copies, `/override`,
`setup-fleet-scheduler.ps1` as a declared bootstrap). This is frustrating and correct.

**(h) Review as paste vs gate.** Terra review was requested by an operator paste at least twice
this window. **Landed: review is a merge gate — a lane branch with no tally line carrying
reviewer model and HIGH raw/fixed/unresolved cannot merge.** Filed.

## 3 · Considered and REJECTED — do not relitigate

| Option | Rejected because |
|---|---|
| **GitHub Issues as the state carrier** (conductor option A) | lock-in; breaks "decisions are files"; scored 52 vs E's 58 |
| **Claude Code native orchestration as the primary conductor** (option B) | runs on the operator's workstation and bills tokens per orchestration turn. **KEPT as E's fallback** — same task files, same graph, no state migration |
| **A workflow engine — Prefect / Windmill / Kestra / Temporal** (option C) | adds a server to operate and replaces not one existing hook; 38/58 |
| **A local `transitions` + sqlite state machine** (option D) | another custom loop file; the operator rejected it in the same words |
| **Moving the PowerShell dispatch layer into the hub** | breaks ADR-28; see 2(c) |
| **Copying Maister's code** | would stand a second organ set beside ours. The *shape* is adopted; the code is not |
| **Extending `ecosystem/organ-registry.yaml` to all 216 census rows** | **retracted by this seat mid-window.** It would be a hand-maintained copy of the graph — INBOX-037's defect at the spine. The registry is a QUERY |
| **Raising `[#589]`'s byte bar to fit new rows** | raising a bar to fit the first rows that hit it is what the row forbids; grooming is archival, and archival is an operator closure act |
| **Cutting a `-3` bundle to discharge P11** | at the time, validated by nothing — P11 had no code. Superseded: V-5 built the predicate |
| **Deleting the 32 orphans on the 2026-09-08 count** | contested by the 39-count; see 2(g) |
| **Substituting a different reviewer model when Codex hit quota mid-series** | changes the measure mid-measurement; the tally would lie |
| **Reasoning the six unattributed REDs into attribution** | one same-substrate run at `08c35b9c` decides it. `[#673]` says "never by argument" in the row body for exactly this reason |
| **AI Council for the conductor decision** | **the operator ruled it out explicitly** ("there will be no AI counsel"). Architecture decisions in this fleet now come from browser web-research + a weighted matrix + the operator's ruling. See §6 |

## 4 · Open questions — unresolved or deliberately deferred

**Operator words owed (each blocks something named):**
1. **GitHub Pro** — E's gate leg is unavailable on Free (403 on rulesets, verified).
2. **Orphan deletion** — BLOCKED on the 32-vs-39 census contradiction. Reconcile first.
3. **Five DEAD PLAYBOOK sections** — §1, §6, §9, §12 (config hierarchy only), §13 (Obsidian row only), each with per-section evidence in the chapter map.
4. **The 2026-08-29 deploy freeze** — the single named blocker on Stage 10. Never put to the operator before this window; put to him three times within it; still open. **This is the one that decides whether the next window delivers anything to a consumer.**
5. **JOURNAL's verb** — delete or wire, decided by a measurement not yet taken.

**Unratified intakes:** `#75` (offload admission — the recommendation is to ratify the BAR, which Copilot failed; ratifying the bar is not ratifying Copilot) · `#86` (`orphan_census` — ratify only if the intake names the census's own trigger, else V+1 builds an orphan that measures orphans) · the ADR-98 intake owed by AF-1 (unread by this seat; no recommendation offered rather than a blind one).

**Design questions genuinely open:**
- **Does win-tooling get the floor before corp-monorepo?** `AMEND-PROMPTS-DIR-001` §3 recommends yes — a consumer cannot be universalised by an ungoverned launcher — and it was never ruled. It costs corp-monorepo one window.
- **The 16-stage delivery-loop order is enumerated NOWHERE in the repo** (REVIEW §1 row 4); the recovery intake's ratio line is its fullest in-repo description. Either enumerate it or stop citing it.
- **Are the night bundle's ~220 UNVERIFIED locators usable?** 24 verified against ~220 carried. The Maister/spine leg (1c, codex) is the only adversarially checked one. The bundle is honest about this; the next seat must not read it as uniformly evidenced.
- **The model-agnosticism audit (leg 1f) has not been read by this seat.** It is the input to "swap the architect model in one config line", which is now an explicit operator requirement.
- **Seven R1 rulings** in REVIEW §4, including two ordered readers that died on free-tier quota with no substitute run (R1 held correctly), and one that is our own fault: our `PreToolUse` guard wedged `cursor-agent` and burned two paid runs, because `$CLAUDE_PROJECT_DIR` does not expand outside Claude Code and matcher `"*"` makes that a total refusal of every non-Claude tool. **In a repo that must become model-agnostic, our own guard refuses every other vendor.**

## 5 · Decomposition rationale — and what NOT to redo

**Why batch V had this shape.** Six committing lanes at the ADR-110 ceiling; all local because
all commit; one worktree each; V-4 (assembly debt) held on Sitting 1 because its rows are the
rulings' output. The sitting itself split three ways because Fable turns are budgeted (≤10) and
eleven rulings plus a version declaration do not fit one: S0 ruled homes-by-kind (the critical
path to a consumer that can be sealed), S1 ruled the eleven, S2 was administrative.

**Do NOT redo:**
- **The process-trigger census.** Merged; 216/160/24/32 with per-row evidence and both of its own wrong passes recorded. *Do* reconcile it against the 39-count — that is new work, not a re-derivation.
- **The eleven carried questions.** `DECLARE-SITTING-2026-09-08` is landed as intake; V-4's rows carry them.
- **The conductor decision.** Re-open only if one of `DECLARE-CONDUCTOR-DECISION` §6's five numbers moves (phase transitions without operator action · operator hours per feature · operator pastes per week · organs deleted · Actions minutes per week).
- **Dispatch retirement.** Ruled with its ordering condition: new hands hold before old hands let go — E must run one batch before anything in win-tooling is deleted.
- **Substrate pricing.** Measured (Codespaces ~5 min · local chunked ~110 min · local overnight ~60–90 min · `-n auto` is the OOM path and `-n 0` alone holds peak at ~600 MB).
- **P11's implementation gap.** Built by V-5; predicate runs against the live transport and reproduces the hand-run recipe by name.
- **Reading the 500 KB PLAYBOOK.** The chapter map exists (33,450 B, pinned `d12beac6`), with per-section verdicts on quoted pairs. Its DUP verdicts stand on citation pairs, not on a similarity score — `[#190]`'s detector cannot find what is wrong here, because the duplication is conceptual (a rule restated in different words), not copy-paste.
- **The Organ-map-is-a-registry-copy hypothesis.** DISPROVEN by measurement: 5 of 23 names shared with `organ-index.md`; ARCHITECTURE carries a failure-posture column nothing else has. The render must give the registry that column first.

**One decomposition lesson to carry:** the apparatus fires on the CONTRACT, never on what the
contract WRITES. A one-line backlog row provisioned a worktree and, after batch V closed, cost
~12 minutes and two merges under the self-referential anchor rule. `[#675]` carries this with a
size-gate Done-when.

## 6 · Off-repo context — changed INTENT only

**(a) The definition of "harness" changed mid-window, and it is now the operator's, not ours.**
It is process management: a registry of automatically triggered processes, *trigger event →
organ → artifact*. Anything no process triggers is **inventory, not harness** — it gets a
trigger or it is removed, and there is no third state. He never asks CC to run a library by
hand; the process must call it. This reframing is upstream of every other decision in the
window and it is why the census exists.

**(b) "Nothing is implemented without a task."** `nic nie wdrażamy bez tasków` — a task is the
control point over the process even when it is the longer road. Enforced today only at CLOSE;
the intent is at OPEN.

**(c) The measure of success moved to the operator's own day.** Not "the hub is healthy" but
**"I open corp-monorepo and I work."** Three months of building, nothing in a consumer. Every
plan should be read against that sentence.

**(d) Model-agnosticism became an explicit requirement this window.** The whole process —
handoff, seat boots, routing, dispatch, the browser contract — must survive swapping Anthropic
for Codex or Gemini. The goal is that switching the architect model is one config line. This is
new intent, not a restatement.

**(e) Deletion outranks addition, as a standing posture.** Not a preference — a complaint with
evidence behind it. The next window is judged on what it removed.

**(f) AI Council is out as a decision mechanism.** Ruled explicitly. Architecture decisions come
from browser web-research plus a weighted matrix with named criteria, presented for the
operator's ruling. He additionally demands that a decision be **re-evaluable later** — hence the
30-day measurement blocks now attached to the conductor and JOURNAL decisions. A recommendation
without a falsifier is not acceptable output.

**(g) Provider posture.** GLM and DeepSeek deferred (API-only, CLI unreliable). `gpt-6-astra` is
treated as the XL tier on cost — ruling-class and adversarial derivations only, explicit opt-in,
never a default, never lanes/reviews/fan-out. The cheaper providers are to be USED, not
theorised about: the operator is explicit that offloading read-only work to them is the point.

**(h) A hard boundary the next seat must not cross.** Substituting a tool the operator ordered,
without saying so, is treated as a false report — not as initiative. It happened once this
window (an ordered reader failed and CC's own subagents produced the work; this seat relayed the
result as fact). R1 of the night mission is the codified form: record the failure, mark the leg
SUBSTITUTED-PENDING-OPERATOR, do not silently swap.

## 7 · Ratified-in-chat register — not yet in the repo

**Terms and rulings ratified in chat, with their durable homes:**

| Term / ruling | One line | Home |
|---|---|---|
| **assembly debt / enforcement debt** | ruled-but-unrowed vs specified-but-uncoded — the two halves of "everything is built, nothing is connected" | LESSONS; partially carried in `docs/intake/2026-09-09-tech-window-close-rulings.md` (#90) |
| **declared enforcement without enforcement** | the class: a claim about a relationship that nothing verifies. Nine-plus instances in two days | LESSONS, as a named class with its instance list |
| **map vs conductor** | the graph answers questions; the conductor fires phases. Independent; the graph can exist without the conductor | ADR (spine), citing ADR-118 |
| **`DECLARE-HARNESS-IS-PROCESS-2026-09-08`** | the operator's harness definition — **cited by three committed audits and ABSENT from the tree.** REVIEW's finding #1 in its purest form | the repo, urgently — an intake or ADR; a P11 OPEN carrier today |
| **`DECLARE-JOURNAL-DECISION-2026-09-09`** | the anchor-in-commit decision — **deliberately not landed**; amends ADR-85, needs a terra-reviewed lane and a measurement | ADR-85 amendment via a lane |
| **"no AI Council"** | architecture decisions by research + weighted matrix + operator ruling, with a 30-day falsifier | PLAYBOOK (decision-making section) or STANDING_RULINGS |
| **the ordering condition on dispatch retirement** | new hands hold before old hands let go — E runs one batch before win-tooling deletes anything | carried in `DECLARE-DISPATCH-RETIREMENT` §4; needs a row |

**Interface behaviours relied on and not yet named in `protocols/OPERATOR-INTERFACE.md`:**

| Behaviour | What relying on it looked like | Home |
|---|---|---|
| **Named-session addressing** | the browser tells the operator WHICH session a paste goes to (integrator · dispatcher · working CC · win-tooling · night), because Cloud SDK shows many concurrent sessions. Getting this wrong cost turns | `OPERATOR-INTERFACE.md` |



> **Transcription note (CC, 2026-09-10) — six of the seven interface behaviours were struck as
> already documented.** The operator's instruction was that anything already named in
> `protocols/OPERATOR-INTERFACE.md` is struck before transcription. Verified line-by-line against
> that file; the six removed rows and their citations are:
>
> - **Browser writes decisions to the transport via the Drive connector** — `OPERATOR-INTERFACE.md:46-48`,
>   the prompts-dir constant: "a Google Drive folder synced by Drive for Desktop, **which the browser
>   reads/writes via the Drive connector**"; reinforced by "Rule 1 (inbox 029) — a browser decision
>   exists only as a file" (:147).
> - **Browser READS the transport itself** — the same `reads/writes` clause at :46-48, and §2's
>   `CC output` row: "read from the transport — `STATUS-*`, `LEDGER-<repo>`, `QUESTION-*`, close
>   packets — on 'check'. A pasted session log counts as a browser-seat defect."
> - **The END-OF-PASTE sentinel as a truncation detector** — :143-145, verbatim purpose: `PASTE_THIS.md`
>   "ships a terminal `=== END OF PASTE ===` sentinel so a truncated one is visible on sight."
>   **Residual drift, reported not struck:** the file documents the BARE sentinel; the live assembler
>   emits `=== END OF PASTE — n sections · b bytes ===`. The counts are undocumented.
> - **Model-switch line format** — :165 carries both strings verbatim: `ROUTINE — Opus is enough` /
>   `RULING AHEAD — Fable (est. ~N k tokens: <files>)`. **The answer's actual complaint survives the
>   strike and is a change request against that documented line, not an unnamed behaviour:** neither
>   form carries an explicit *stay / return / switch* verb, which is why the operator could not tell
>   them apart.
> - **A copy-ready block substitutes for a described action** — it is §7's own heading, at :250:
>   "Operator-action steps end with a copy-ready block." (The answer's Home column already conceded
>   this: "already the operator's standing rule".)
> - **CC transcripts pasted into chat arrive corrupted mid-token** — §2 is the named home, heading at
>   :132 ("Inline chat paste of large content arrives empty — so uploads are `.md` files"), with the
>   discriminator at :140-141 ("A paste that ends mid-sentence ended mid-transport"). The answer's own
>   Home column calls it "defect report against `OPERATOR-INTERFACE.md`" — which is Q6's stated
>   carve-out, not a behaviour missing from the file. **Its substance survives: the rule is written
>   and nothing enforces it**, which is this window's own `declared enforcement without enforcement`
>   class applied to the interface file.
>
> **`Named-session addressing` is genuinely absent and is the only row kept.** Nothing in
> `OPERATOR-INTERFACE.md` tells the operator which session a paste goes to. The nearest text is
> :83, "A chat paste is not addressable", which argues that *ownership metadata belongs in the file*
> (`owner-role:` at :70) — a different claim: it addresses the WORK, not the operator's paste.

---

=== END OF PASTE — 5 sections · 55282 bytes ===
