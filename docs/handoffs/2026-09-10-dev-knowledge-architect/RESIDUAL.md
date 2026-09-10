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
