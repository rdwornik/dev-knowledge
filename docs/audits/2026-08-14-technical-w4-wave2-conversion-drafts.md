# W4 wave-2 conversion drafts — the 29 needs-draft rows + the `[#419]` re-check

**Produced:** 2026-08-14 · night-2 wave-2 draft-production lane (`claude/night2-wave2-drafts-fmbwa4`)
**Instrument:** the census draft-form (`docs/audits/2026-08-10-technical-backlog-testability-census.md` §4)
**Consumers:** the wave-2 conversion lanes, after architect review + operator GO

> **EVERY DRAFT BELOW IS A DRAFT.** It applies only under a later operator ruling. Nothing in
> this file has been written to any task file, and this lane has no authority to write one. No
> `BACKLOG.md` row, no `tasks/*.md` body, no register entry and no manifest was touched to
> produce it. Verbatim from the census's own disclaimer, because the constraint is the same.

Each draft preserves the row's intent or says where it could not. **Where the source material is
ambiguous the draft is produced anyway with an AMBIGUITY flag naming the fork** (§5) — never a
silent skip, never a silent guess.

---

## 1. Provenance — how these 30 ids were derived

The operator-side input file (`~/Downloads/W4-WAVE2-INPUT.md`) is Downloads-only and has no
on-main twin: JOURNAL 2026-08-14 (d) step 8 records it as *"Downloads-only, no repo change"*.
The set was therefore **re-derived from the in-repo record** rather than taken on faith, which
is possible because wave-1's own contract forbade a silent skip:

> *"Every skip carries a one-line reason in its lane's own JOURNAL entry (no census draft, or a
> stale draft against the live row) — no skip is silent."*
> — `docs/audits/2026-08-14-technical-batch-4-true-close-packet.md` §3

| Wave-1 lane | Contract | Assigned | Converted | Skipped | Skipped ids |
|---|---|---|---|---|---|
| h | W4a (group A) | 17 | 6 | 11 | 82, 130, 145, 146, 210, 239, 263, 266, 271, 274, 285 |
| i | W4b (group B) | 18 | 13 | 5 | 324, 350, 351, 361, 364 |
| j | W4c (group C) | 18 | 9 | 9 | 385, 391, 393, **419**, 409, 410, 411, 412, 417 |
| k | W4d (group D) | 16 | 11 | 5 | 438, 443, 484, 491, 502 |
| **Total** | | **69** | **39** | **30** | **29 needs-draft + 1 re-check** |

Reconciles exactly with the packet's 69/39/30 arithmetic and with the handoff's *"29 needs-draft
ids + 1 re-check `[#419]`"*. Sources: JOURNAL 2026-08-13 (g) lane h · (h) lane i · (i) lane j ·
(j) lane k.

**L14 re-resolve, run before drafting:** all 30 ids verified `status: open` live in
`tasks/<id>-*.md` at this lane's boot — none closed, none in flight. 29 are P3 (the needs-draft
class: the census drafted only its P1+P2 band, so a P3 row has no draft by the census's own
contract); `[#419]` is the P2/M re-check, skipped by lane j for the opposite reason — its draft
existed but had **rotted against an amendment**.

Every "**Now:**" quote below is extracted verbatim from the live row body, not from the census.

---

## 2. Levers reused

### Form E — the escape-hatch home (census §4, applied 21 times there, 11 times here)

An unhomed escape branch (*"…, or recorded permanent-defer-with-reason"*) is what makes an
otherwise-mechanical clause unverdictable, because *recorded where?* has no answer.

```
Form E — replace:   ..., or recorded <X>-with-reason
with:               ..., or `protocols/STANDING_RULINGS.md` carries a section
                    naming `[#NNN]` and stating the reason
Predicate:          a `###` section in protocols/STANDING_RULINGS.md whose body
                    contains the literal `[#NNN]`
```

Live-verified: `STANDING_RULINGS.md` carries lettered `###` sections through §O. Applied here to
`[#146]` `[#210]` `[#239]` `[#263]` `[#350]` `[#351]` `[#364]` `[#391]` `[#412]` `[#417]`
`[#443]` `[#484]` `[#491]`.

### Form R — the routine block (census §6 row 1, made paste-ready)

The census flagged the shape but stopped short of a draft, which is exactly why lane j left
`[#409]`/`[#410]`/`[#411]` unconverted (*"a strategy note, not a paste-ready draft, and this lane
designs nothing"*). Producing that draft is this lane's job. The live marker, from ADR-105 §
and `BACKLOG.md`'s two conforming rows (`[#348]`, `[#426]`):

```
· routine: trigger=<what fires it> · scope=<what it covers> · consumer=<who reads it>
  · consumption_path=<how the output reaches a decision> · verified_by=<what proves it>
  · review_date=<YYYY-MM-DD>
```

`scripts/audit.py::check_routine_consumers` verdicts the two fields that gate activation
(`consumer`, `consumption_path`) and FAILs on missing/blank/placeholder/duplicate. Applied to
`[#409]` `[#410]` `[#411]` `[#324]` `[#271]` `[#391]`.

**Honest limit, carried into every Form R draft:** `routine_consumers` checks only BACKLOG rows
carrying the `· routine:` marker — not the ~30 live hooks and schedules. Its own docstring says
so, and `[#426]` owns the retrofit. A Form R draft therefore makes a row's *declaration*
checkable; it does not claim the fleet's routines are consumed.

### Open substitution — the home question (the census's Q2, unresolved)

Three drafts want a home the tree does not yet designate: `[#82]` (per-repo review profiles),
`[#324]` (audit-corpus verb-list), `[#412]` (routing doctrine). Each names the most defensible
live candidate and is a **textual substitution** if the operator names another — same posture as
the census's Form E Q2.

---

## 3. Group A — wave-1 lane h (11 drafts)

#### `[#82]` P3/M — Per-repository agentic-review profiles
- **Now:** *"each repo's agentic-review profile is recorded"*
- **DRAFT:** *"every member of the `adr104-fleet-members` declaration carries a recorded agentic-review profile (which review runs, and on what cadence) at its stated home, and any member deliberately without one is named there with its reason"*
- **Intent:** "each repo" had no denominator; one already exists and is machine-checked — ADR-104's `adr104-fleet-members` anchor (9 ids), read by `check_membership_agreement`, so the count cannot drift silently. "Recorded" gains a home and the deliberate-absence case gains an explicit branch rather than reading as an omission. The row's design inputs (heterogeneous second reader, evaluate-natives-first, per-profile `model_reasoning_effort`) stay design inputs — the draft adds no clause for them.

#### `[#130]` P3/S — Memory-hygiene review
- **Now:** *"one hygiene pass runs and emits a ratify-only candidates digest (duplicates / stale-RETIRED / cap-proximity) AND a capture-time scrub step exists in the gotcha/memory write path"*
- **DRAFT:** *"one hygiene pass emits a ratify-only candidates digest to a `docs/audits/<date>-technical-*` artifact with per-class counts (duplicates / stale-RETIRED / cap-proximity), and the gotcha/memory write path carries a dedupe-against-existing step proven by a test that seeds a duplicate and asserts it is caught at write time"*
- **Intent:** both legs keep their substance and gain an artifact. The digest gets a filed home (the same move the census made for `[#123]`'s value review); "a scrub step exists" becomes a test, since *exists* is the class of claim that passes by inspection and fails in use. The no-delete invariant is untouched — the digest stays ratify-only.

#### `[#145]` P3/M — Codification-completeness pass
- **Now:** *"a read-only pass enumerates fresh-session transmission gaps across PLAYBOOK/bundle and each is filed or closed"*
- **DRAFT:** *"a `docs/audits/<date>-technical-*` artifact enumerates the fresh-session transmission gaps found across `protocols/PLAYBOOK.md` and the active handoff bundle, and every gap it enumerates carries either a BACKLOG id or a stated closure in that same artifact"*
- **Intent:** the pass gains a filed artifact, and "each is filed or closed" gains its denominator — *every gap this artifact enumerates* — so completeness is verdictable by reading one file instead of by trusting that the pass was thorough. The row's A4 advance (gate-map, delivery-lifecycle, premises self-check now resident in HANDOFF_BOOT) stays recorded context; the draft converts only the outstanding enumeration leg.

#### `[#146]` P3/S — De-hardcode-first doctrine + sweep
- **Now:** *"de-hardcode-first is doctrine AND a sweep is run (each candidate de-hardcoded, or explicitly kept-as-manifest with a reason)"*
- **DRAFT:** *"`protocols/PLAYBOOK.md`'s `amendment_coherence` honest-limits section carries de-hardcode-first as doctrine, and a `docs/audits/<date>-technical-*` sweep names every hand-maintained version surface with a per-surface verdict of de-hardcoded or kept-as-manifest — each kept-as-manifest surface carrying its reason"*
- **Intent:** clause (a) is already satisfied in the tree, and the draft names the **section** rather than a line range on purpose: the row's own `PLAYBOOK:1016-1024` pin has drifted (the de-hardcode paragraph now sits at `PLAYBOOK:1032`), and a clause pinned to a line number re-rots on the next edit. Clause (b), the sweep that has not run, gains an artifact plus a per-surface denominator. The row's "authorship unverified" note stays context — the draft does not convert it into an acceptance criterion.

#### `[#210]` P3/S — Journal-wrap no-ff WARNs → standing rule
- **Now:** *"the shape is decided AND either (a) the exemption ships with a test proving a JOURNAL-only direct commit passes while a same-commit code-path edit still WARNs, or (b) the wrap moves behind a --no-ff arc; the 3 per-instance dispositions then retire"*
- **DRAFT:** *"the shape is recorded in `protocols/STANDING_RULINGS.md` in a section naming `[#210]`, AND either (a) the `no_ff_merges` exemption ships with a test proving a JOURNAL-only direct commit passes while a same-commit code-path edit still WARNs, or (b) the wrap moves behind a `--no-ff` arc; and `ecosystem/disposition-register.yaml` carries none of the 3 journal-wrap per-instance entries"*
- **Intent:** this row was already near-mechanical — both build branches and the (a) test are the row's own words and are kept verbatim. Only two things changed: "the shape is decided" gains Form E's home (a decision with no recorded home cannot be verdicted), and "the dispositions then retire" gains a countable predicate against the register, which carries exactly 3 journal entries today. Core-invariant #5 is not weakened: the (a) branch keeps the row's own requirement that a same-commit code-path edit still WARNs.

#### `[#239]` P3/M — Informant Organ Tier-2 beyond the 4 carriers
- **Now:** *"those methodology elements gain `detect()`/versioned target-state AND the Informant reports their present-and-wired state, or each is explicitly deferred with a recorded reason"*
- **DRAFT:** *"each of skills, commands (including `/codex-review`) and review-closure tooling either carries a `detect()` + versioned target-state that `scripts/enforcement_coverage.py` reports present-and-wired, or `protocols/STANDING_RULINGS.md` carries a section naming `[#239]` and stating that element's deferral reason"*
- **Intent:** "those methodology elements" pointed back at the row's own prose, so the draft inlines the three and the clause becomes self-contained and countable at 3/3. The build branch names the live organ that already reports carrier PRESENCE (`enforcement_coverage.py`, the row's own ref). Form E homes the per-element deferral — and it is per-element, as the row wrote it, not a blanket escape.

#### `[#263]` P3/S — Protocols/edge-map reconciliation residuals
- **Now:** *"the stale doc-code-edge entries are removed and the pre-existing ESSENTIALS refs reconciled or dispositioned"*
- **DRAFT:** *"`ecosystem/doc-code-edge.yaml` no longer carries the `mermaid_theme_directive` exempt entry or its stale comment word, the two `protocols/PLAYBOOK.md` 'per ESSENTIALS…English-only' refs and the `protocols/AI_COUNCIL_PROCESS.md` 'ESSENTIALS § Repo artifacts' ref each either resolve to live `protocols/ESSENTIALS.md` text or are recorded in `protocols/STANDING_RULINGS.md` in a section naming `[#263]`, and `doc_code_coverage_drift` stays OK"*
- **Intent:** the row's (a)/(b) already enumerate the exact loci, so the draft inlines them and the clause becomes greppable at 1 + 3 sites. Entries are named **by key, not by line** — the row's `L110`/`L61` pins have already drifted (the exempt entry is at L115 today), which is the same lesson `[#146]` teaches. All three ESSENTIALS refs verified live at drafting. `doc_code_coverage_drift` is named because the row's own safety evidence is that the guard ignores unknown exempt entries — the draft keeps that proof obligation on the removal.

#### `[#266]` P3/S — Codify the test-scoped-grant language lesson
- **Now:** *"the grant-language guidance names the count/pinning-assertion inclusion, with the E4-1 precedent cited"*
- **DRAFT:** *"the grant-authoring guidance states that a narrow test-scoped grant includes the mechanical count/pinning assertions the change forces, at both `templates/handoff/epic/EPIC_BOOT.md.tmpl`'s FILE-BOUNDARY section and `ADR-97` §14a, citing the E4-1 precedent"*
- **Intent:** "the grant-language guidance" was an unhomed noun; the row's own refs name both homes and the draft inlines them, so the clause is countable at 2/2. Both verified live at drafting (`templates/handoff/epic/EPIC_BOOT.md.tmpl` exists; ADR-97 §14a carries the FILE-BOUNDARY clause). Substance unchanged — this is a locus conversion, not a scope change.

#### `[#271]` P3/L — Nightly proposal loop
- **Now:** *"the loop runs nightly under ALL §6 constraints with the load-gauge live AND the first 2-week survival review is recorded"*
- **DRAFT:** *"the loop runs nightly under a `· routine:` block that `routine_consumers` passes with `[#270]`'s load-gauge live; each §6 constraint — the ~5 proposals/night cap, the 7-day auto-expire, no autonomous semantic refactoring at night, and proposals landing in `docs/intake/` as `status: SEED` — is enforced by a check or a test rather than by convention; and a `docs/audits/<date>-technical-*` artifact records the first 2-week survival review with its measured accept-rate against the <20% kill threshold"*
- **Intent:** "ALL §6 constraints" gains its enumeration inline from the row's own body, plus the requirement that each be **mechanized rather than remembered** — which is what a constraint has to mean for a lane that runs unattended while judgment sleeps. The survival review gains a filed home and its verdict gains the row's own number. The intake brief's carried-ex-ante terms are quoted, not renegotiated: nothing here is new scope.

#### `[#274]` P3/S — Dogfood-signal prior in the `/changelog-review` ADOPT rubric
- **Now:** *"the command's ADOPT rubric names the dogfood-signal prior and one subsequent review demonstrably applies it"*
- **DRAFT:** *"`.claude/commands/changelog-review.md`'s ADOPT rubric names the dogfood-signal prior, and one subsequent `docs/audits/<date>-changelog-review-*` digest cites that prior by name against at least one classified item"*
- **Intent:** the rubric gains its file (the row's own ref, verified live — the ADOPT rubric is at `changelog-review.md:35`). "Demonstrably applies it" becomes greppable: the prior named in a real digest against a real item. `changelog-review` is already a class in ADR-101's closed audit-class enum, so the digest has a conforming home and needs no new taxonomy.

#### `[#285]` P3/S — Extend hub freshness gating to PLAYBOOK
- **Now:** *"PLAYBOOK is genuinely re-read end-to-end, carries a `last_reviewed` stamp, and is in `_FRESHNESS_FILES` (audit-health gates it) with `test_freshness_includes_hub_only_protocol_docs` updated (drop its PLAYBOOK-absent assertion)"*
- **DRAFT:** *"`protocols/PLAYBOOK.md` carries `last_reviewed` frontmatter, `protocols/PLAYBOOK.md` is a member of `_HUB_ONLY_FRESHNESS_FILES` in `scripts/audit.py`, `test_freshness_includes_hub_only_protocol_docs` no longer asserts PLAYBOOK's absence, and the re-read is evidenced by per-section notes in the commit that stamps it — not by the stamp alone"*
- **Intent:** three of four legs were already mechanical (the row names the constant, the test and the assertion) and are kept. Two repairs: the editable constant is `_HUB_ONLY_FRESHNESS_FILES` — `_FRESHNESS_FILES` is the composed list (`DEFAULT + _HUB_ONLY`) and cannot be edited directly, so the row as written names a target that does not accept the change; and "genuinely re-read" cannot be mechanized, so it converts to the evidence form this repo already uses for exactly this claim (the CLAUDE.md §12 per-section re-read note carried in the commit). That preserves the row's real guard — a bare stamp to green a gate is forbidden — instead of dropping it as unverdictable. Both premises verified live: PLAYBOOK has no `last_reviewed` (prose "Last updated" only) and is absent from the hub-only list, which holds SESSION_SETUP, AI_COUNCIL_PROCESS and DEFINITION_OF_DONE.

---

## 4. Group B — wave-1 lane i (5 drafts)

#### `[#324]` P3/M — Phase-6 axis-2 carrier
- **Now:** *"the night-batch standing routine + morning verdict-sheet consumer + audit-corpus verb-list are codified (next session)"*
- **DRAFT:** *"the night-batch standing routine carries a `· routine:` block that `routine_consumers` passes, the morning verdict-sheet consumer is named as that routine's `consumer=` with the sheet as its `consumption_path=`, and the audit-corpus verb-list is recorded in a `docs/audits/<date>-technical-*` artifact"*
- **Intent:** the row's three charter deliverables map cleanly onto the live ADR-105 shape — (b) *is* a consumer declaration, which is precisely what `routine_consumers` verdicts, so two of three legs become checkable with no new machinery. The "(next session)" parenthetical is dropped: it dated a charter to the session following 2026-07-12 and can never be verdicted now, so keeping it would leave the clause permanently unmeetable. Charter-only scope is unchanged — codifying is still not building. Verb-list home is an open substitution (§2).

#### `[#350]` P3/S — Handoff-process refinements
- **Now:** *"(a) a non-CC browser can trigger a handoff, (b) the handoff file-dependency class is resolved or recorded, and (c) refinements are filed — each landed or recorded permanent-defer-with-reason"*
- **DRAFT:** *"(a) a non-CC browser can trigger a handoff and the path is documented in `protocols/HANDOFF_PROCESS.md`, (b) the handoff file-dependency class — a bundle citing a file that moved or was renamed — is detected by a check or recorded as accepted, and (c) each filed refinement carries a BACKLOG id; each of (a)/(b)/(c) landed, or `protocols/STANDING_RULINGS.md` carries a section naming `[#350]` and stating why it is deferred"*
- **Intent:** Form E homes the escape branch, which is the whole reason this clause was unverdictable. (b) gains its concrete subject from the row's own parenthetical and (c) gains a filing predicate, so "filed" means an id exists rather than that someone remembers writing it down. The operator's explicit LAST-priority dictate is untouched: this converts the clause, not the priority.

#### `[#351]` P3/M — Fleet-Python-upgrade ticket (RULING-PY)
- **Now:** *"a coordinated fleet Python/target-version upgrade path is defined AND the newest-Python baseline is either raised fleet-wide in one arc or recorded deferred-with-next-review-date"*
- **DRAFT:** *"a `docs/audits/<date>-technical-*` artifact defines the coordinated upgrade path across every member of the `adr104-fleet-members` declaration, and the newest-Python baseline is either raised for all of them in one arc — ruff `target-version` and the `pyproject.toml` required-version floor moving together — or `protocols/STANDING_RULINGS.md` carries a section naming `[#351]` with a stated next-review date"*
- **Intent:** "fleet-wide" gains the machine-checked denominator (ADR-104's 9-id anchor, gated by `membership_agreement`), which is what makes "one coordinated arc, never per-repo drift" checkable rather than aspirational. The deferral gains Form E's home while keeping the row's own next-review-date requirement, so the ticket cannot quietly become permanent. RULING-PY's standing direction is quoted, not reopened.

#### `[#361]` P3/S — ADR-immutability's real coverage is declared only in code
- **Now:** *"the protocol states the guard's real scope, or the guard widens to match the claim"*
- **DRAFT:** *"either `protocols/AI_COUNCIL_PROCESS.md` and `templates/claude-regions/critical-rules-records.md` state the guard's real zone — `docs/decisions/transcripts/**` only, and that the zone is a live no-op since that tree was deleted — or `scripts/hooks/block_immutable_edits.py` widens to cover ADRs, handoffs and audits, with a test per newly-covered class"*
- **Intent:** both disjuncts gain the exact loci the row's own refs already name, so each is verdictable by reading one file. The widen branch gains a per-class test obligation, which is what "match the claim" has to mean when the claim is *four of four classes are immutable* — verified live at drafting: the guard's zone is still transcripts-only. The row's finding is preserved intact, including the uncomfortable half (the guard's only zone no longer exists).

[#364] withdrawn — obsoleted 2026-08-15, premise discharged by the 1320 threshold (Y-2)

---

## 5. Group C — wave-1 lane j (8 drafts + the `[#419]` re-check)

#### `[#385]` P3/M — L4 tech-currency lane
- **Now:** *"one proposal flows contract → ruling → deploy end-to-end"*
- **DRAFT:** *"one version-bump proposal is written into the desired-state contract, ruled, and distributed through the apply channel, with the resulting version visible in `ecosystem/deployed-versions.yaml` and the proposal at no point mutating the contract directly"*
- **Intent:** "end-to-end" gains a terminal artifact — `deployed-versions.yaml` is the durable record `desired_state_loader.py` resolves toward, so the whole flow becomes verdictable from one file's diff instead of from a narrative. The proposals-only invariant is lifted out of the row body into the clause, where it can actually be checked; it was the row's stated guard against the lane degrading back into a one-off. The `[#383]` dependency is unchanged and still open, so the gate stands.

#### `[#391]` P3/S — Wire `fleet_analytics` into a nightly lane — **AMBIGUITY (§5.2)**
- **Now:** *"fleet_analytics fires nightly OR #384 is narrowed to manual + scheduling filed separately"*
- **DRAFT:** *"`scripts/fleet_analytics.py` fires on a schedule under a `· routine:` block that `routine_consumers` passes, fail-soft, with `[S20]`'s load-gauge discipline applied"*
- **Intent:** branch (a) gains the organ that verdicts a routine declaration and keeps the row's own fail-soft and load-gauge conditions verbatim. **Branch (b) could not be converted as written: it acts on `[#384]`, which was closed 2026-07-23, and a closed row cannot be narrowed.** The draft re-expresses (b) as recording the scope decision and filing the scheduling work fresh — the recoverable intent — rather than guessing at a rewrite. See §5.2.

#### `[#393]` P3/S — corp-sca rot review, 3 candidates
- **Now:** *"each of the 3 is confirmed-live or retired"*
- **DRAFT:** *"each of `config/category_mapping.yaml`, `requirements.txt` and `config/excluded.yaml` in `corp-sca-time-automation` carries a recorded confirmed-live or retired verdict, and a subsequent `fleet_analytics` run no longer flags the retired ones"*
- **Intent:** "the 3" gains its inline enumeration from the row's own body, so the clause is self-contained and countable at 3/3 without opening the audit it came from. The second leg makes the verdict reach the instrument that raised the flag — otherwise "retired" is a claim in prose while the reporter keeps flagging the file, which is the review-queue-never-drains failure this row exists to end. Consumer-repo routing is unchanged: the work still lands in corp-sca.

#### `[#409]` P3/S — Standing night batch: CODE review
- **Now:** *"the code-review night batch is defined as a routine (trigger, scope, consumption path) and ruled in or out"*
- **DRAFT:** *"the code-review night batch carries an ADR-105 `· routine:` block with all six fields populated (`trigger`/`scope`/`consumer`/`consumption_path`/`verified_by`/`review_date`) that `routine_consumers` passes — or it is ruled out in `protocols/STANDING_RULINGS.md` in a section naming `[#409]`"*
- **Intent:** Form R (§2). The row's parenthetical names three of the six fields ADR-105 already declares, so the draft completes the set rather than inventing one, and `routine_consumers` verdicts the two that gate activation — checkable today, no new machinery. "Ruled in or out" gains Form E's home for the *out* branch, which was the unhomed half. The ADR-105 activation gate the row already carries is unchanged: carrying a block is filing, not activating.

#### `[#410]` P3/S — Standing night batch: ARCHITECTURE review
- **Now:** *"the architecture-review night batch is defined as a routine (trigger, scope, consumption path) and ruled in or out"*
- **DRAFT:** *"the architecture-review night batch carries an ADR-105 `· routine:` block with all six fields populated (`trigger`/`scope`/`consumer`/`consumption_path`/`verified_by`/`review_date`) that `routine_consumers` passes — or it is ruled out in `protocols/STANDING_RULINGS.md` in a section naming `[#410]`"*
- **Intent:** identical substitution to `[#409]`, deliberately word-for-word: the census graded all three rows as one shape with one destination organ, and drafting them differently would invent a distinction the corpus does not have. The rows stay separate because they read different surfaces (diff vs shape) — that is the row's own reason for existing as a pair, and the draft does not disturb it.

#### `[#411]` P3/S — Standing night batch: creative session + Q&A cadence
- **Now:** *"the creative-session batch AND the recurring Q&A cadence are defined as routines (trigger, scope, consumption path) and ruled in or out"*
- **DRAFT:** *"the creative-session batch and the recurring Q&A cadence each carry an ADR-105 `· routine:` block with all six fields populated that `routine_consumers` passes — or each is ruled out in `protocols/STANDING_RULINGS.md` in a section naming `[#411]`"*
- **Intent:** same substitution as its two siblings, with one difference the row itself forces: this row carries **two** subjects (the batch, plus the Q&A cadence folded in from `[#348]` on 2026-07-25), so the draft requires two blocks and lets each be ruled out independently. Collapsing them to one would drop half the row's scope.

#### `[#412]` P3/M — Subagent/workflow routing + configured fan-out
- **Now:** *"the research is captured (published commands/skills + a fleet-adoption gap read) AND a routing doctrine covering configured fan-out is recorded, or recorded deferred-with-reason"*
- **DRAFT:** *"a `docs/audits/<date>-technical-*` artifact captures Anthropic's published command/skill set with a per-item fleet-adoption verdict, and a routing doctrine covering when to fan out, use a workflow, or use a subagent — configured fan-out included — is recorded in `protocols/PLAYBOOK.md`; or `protocols/STANDING_RULINGS.md` carries a section naming `[#412]` and stating why it is deferred"*
- **Intent:** the research leg gains an artifact and a per-item verdict, which is what turns "a gap read" into something with a shape and a stopping point. The doctrine leg is homed at PLAYBOOK — note that the row's `refs` names `ROUTING.md`, which **does not exist in the tree**; the draft therefore points at the live canonical home rather than inheriting a dead referent. Filing-only scope is unchanged: research plus doctrine, zero build. Doctrine home is an open substitution (§2).

#### `[#417]` P3/S — `check_dirty_tree` runs with no pathspec — **AMBIGUITY (§5.3)**
- **Now:** *"the dirty-tree leg ignores tool-owned writer-isolated paths with a test, or the exclusion is recorded rejected with a reason"*
- **DRAFT:** *"`check_dirty_tree` excludes tool-owned writer-isolated paths — untracked `ecosystem/*/history/*.md` dailies already replicated on the lane — proven by a test in both directions (a lane-owned daily passes; a stray untracked file still fires) — or `protocols/STANDING_RULINGS.md` carries a section naming `[#417]` and stating why the exclusion was rejected"*
- **Intent:** Form E homes the reject branch; the build branch gains the both-directions test, because an exclusion tested only on the passing case is indistinguishable from disabling the check. **This clause appears already MET in the live tree — see §5.3.** The draft is written as the conversion the row would take if it is kept open; if the operator rules it discharged, the draft is moot rather than wrong.
- **Remainder (D6.4(b)):** the landed half (§5.3) is acknowledged in-row; the converted clause carries the row's unlanded remainder — extracting the shared scope list from `scripts/audit.py:2625-2633` — with no closure and no birth.

#### `[#419]` P2/M — Routines whose output nobody consumes — **THE RE-CHECK**
- **Now:** *"every standing routine has a named consumer and a consumption path; unconsumed output is SURFACED, not silently accumulating; and for the nightly conformance routine specifically, the absorb is an ORGAN and not a habit — it has a trigger that fires without an operator remembering, a detector that reports queue depth (count of unmerged `claude/conformance-*`) at a surface the operator already reads, **and a scheduler-run check, so a night the job did not run is distinguishable from a night whose output was not absorbed** (from operator input I-2: 2026-08-06 had no branch because there was no run, and the repo alone could not establish that) — so a lapse is visible on the day it starts rather than eight days later"*
- **DRAFT:** *"`routine_consumers` reports zero routines missing `consumer:` or `consumption_path:` within its stated coverage; unconsumed output is reported by a detector rather than silently accumulating; and for the nightly conformance routine specifically — (i) the absorb has a trigger that fires without an operator remembering, (ii) a detector reports queue depth (the count of unmerged `claude/conformance-*` branches) at a surface the operator already reads, and (iii) a scheduler-run check distinguishes a night with no run from a night whose output went unabsorbed — each of (i)–(iii) proven by a test"*
- **Intent:** **this supersedes the census's `[#419]` draft, which is stale and must not be applied.** That draft (census §4) predates the 2026-08-11 amendment (operator ruling, Fork 3 / I-F3) and covers only the first two legs; applying it would silently drop the three amended clauses — the exact L14 failure mode, and precisely why wave-1's lane j left this row unconverted rather than pasting a rotten draft. Here leg 1 keeps the live organ **with its coverage boundary intact rather than overclaimed** — `routine_consumers` gates only BACKLOG rows carrying the marker, and `[#426]` owns the retrofit, so "within its stated coverage" is doing deliberate work. Legs (i)–(iii) are the amendment's own words given test obligations; (ii) names the SessionStart surfacing set, which is the surface the operator already reads every session, so the detector needs no new surface built for it. Nothing is added beyond what the amended row states.

---

## 6. Group D — wave-1 lane k (5 drafts)

#### `[#438]` P3/S — Codify gate-class posture: design review before build
- **Now:** *"PLAYBOOK carries the gate-class rule (which arcs it binds + what the design pass must answer) AND one arc has run under it"*
- **DRAFT:** *"`protocols/PLAYBOOK.md` carries the refusal-gate class rule, naming which arcs it binds and the questions the pre-build design pass must answer, and one arc's `docs/audits/` record shows its design pass preceding its first implementation commit"*
- **Intent:** both legs were already close to mechanical; the change is that "one arc has run under it" gains an artifact **and an ordering predicate**. Ordering is the entire content of this row — the finding is that review *placement*, not review quality, is the variable — so a draft that proved only "a review happened" would convert the clause while losing the point. Order is checkable from the record's own dates and shas. The `[#436]` ten-pass evidence stays evidence, not a clause.

#### `[#443]` P3/S — Planning artifacts outside the three enforced classes
- **Now:** *"each uncovered class carries either a stated rent/binding rule at its canonical home or a recorded deliberately-not-a-rule with its reason"*
- **DRAFT:** *"each of handoff bundles, session plans and audit docs carries either a stated rent/binding rule at its canonical home — `protocols/HANDOFF_PROCESS.md` for bundles, `protocols/PLAYBOOK.md` for session plans and audit docs — or a section in `protocols/STANDING_RULINGS.md` naming `[#443]` that records it as deliberately-not-a-rule with its reason"*
- **Intent:** "each uncovered class" gains its inline enumeration (the row's own three), so the clause is countable at 3/3, and Form E homes the not-a-rule branch. The row's "there is no open-ended third option" is preserved exactly — the draft has two branches and no default. One deliberate routing choice: audit docs are homed at PLAYBOOK, **not** `docs/audits/README.md`, because that index is generated and gated by the `audit-index-freshness` hook — doctrine written there would be erased by the next regeneration.

#### `[#484]` P3/M — ADR-106 system-Python divergence
- **Now:** *"the system-vs-locked Python divergence is either closed on the operator's machines or recorded permanent-defer-with-reason, and the cp1252 console class is either fixed at the source or declared out of scope with a stated workaround"*
- **DRAFT:** *"the system-vs-locked Python divergence is either closed on the operator's machines, evidenced by a recorded interpreter-version check on each, or `protocols/STANDING_RULINGS.md` carries a section naming `[#484]` stating the deferral reason; and the cp1252 console class is either fixed at the source — a stated encoding posture applied across `scripts/`, with a test asserting a non-ASCII glyph survives console output — or declared out of scope in that same section with its stated workaround"*
- **Intent:** Form E homes both escape branches, in one section so the row's two halves cannot drift apart. The close branch gains evidence (a version check per machine) because "closed on the operator's machines" is otherwise a claim no one in the repo can verdict. The fix branch gains a test that distinguishes a real posture from another one-glyph patch — the row's own kill-candidates note draws exactly that line against `[#470]`, which owns one glyph in one script and is still open. ADR-106's ruling is not reopened; the row is a named deferral and stays one.

#### `[#491]` P3/S — Gemini scanning lane: ruling R-G + acceptance contract
- **Now:** *"the R-G one-line ruling is recorded and the lane has passed one real-work acceptance run with spot-verification evidence"*
- **DRAFT:** *"`protocols/STANDING_RULINGS.md` carries the R-G ruling in a section naming `[#491]`, and one acceptance run over real work — `[#487]`'s ranked sheet or the fleet dependency scan, read-only — is recorded in a `docs/audits/` artifact naming the load-bearing rows that were spot-verified and the outcome of that verification"*
- **Intent:** "recorded" gains the register that already holds lettered rulings, and the acceptance run gains a filed artifact where "spot-verification evidence" becomes nameable: which rows, and what the check found. That specificity is the row's own guard — acceptance is real work, never a synthetic probe. The retrieval-not-classification constraint and Antigravity's exclusion stay standing terms of the lane, not new acceptance clauses.

#### `[#502]` P3/M — mutmut mutation-testing evaluation — **AMBIGUITY (§5.4)**
- **Now:** *"a scoped pilot runs on CI, the `uv run --locked` question is answered from a real run, and the result is a recorded ADOPT/REJECT with measured divergence"*
- **DRAFT:** *"a `[tool.mutmut] paths`-scoped pilot runs in `.github/workflows/report-only-wall.yml` or a sibling workflow, the `uv run --locked` question is answered from that run's own log, and a recorded ADOPT/REJECT names the measured surviving-mutant count over the pilot slice — `tests/test_fleet_analytics*`, since `[#392]`'s rename-alias defect is the known catch"*
- **Intent:** all three legs were already near-mechanical, so the draft mostly supplies the CI host — **which now exists.** "Measured divergence" gains a unit (surviving-mutant count) so the ADOPT/REJECT rests on a number rather than an impression, and the slice is named from the row's own pilot-evidence pointer. **The row's "BLOCKED ON `[#501]`" premise is discharged — see §5.4.**

---

## 7. Ambiguity register — 4 flagged forks

Each was produced as a draft anyway, per this lane's contract. None is a guess: each names the
fork and leaves the resolution to the architect review.

### 5.1 · `[#364]` — the premise has been overtaken, prevention → repair

The row reads *"at 1189 chars it has ~11 left under the 1200 cap… at the current rate it hits the
cap within about two more incidents."* Live at drafting, `[#353]` is **1266 chars and already
tripping the gate**:

```
$ python scripts/validate_doc_rot.py
   backlog-accretion  BACKLOG#353  ->  2 dated block(s), 1266 chars (>= 3 dates & > 700, or > 1200)
```

**The fork:** the row is written as *prevention* (act before the cap is hit); the live state is
*repair* (the WARN is already emitting, and `[#353]` cannot record its next incident without
adding to a finding that already fires). The draft is written to work either way — it requires
that a further incident be recorded **without** a `backlog-accretion` finding, which is satisfied
by either reading. What the architect may want to decide is whether the overtaken premise raises
the row's priority off P3, since the degradation the row predicted has begun.

### 5.2 · `[#391]` — branch (b) names a closed row

The row's second disjunct is *"#384 is narrowed to manual + scheduling filed separately."*
`[#384]` has **no task file, and zero rows in `BACKLOG.md`**; it was closed 2026-07-23 —
*"`[#384]` CLOSED — L5a fleet analytics reporter (`fleet_analytics.py`, read-only)"*
(`docs/handoffs/2026-07-23-dev-knowledge-architect/RESIDUAL.md:38`). A closed row cannot be
narrowed, so half this Done-when is unactionable as written — the census's own DEAD REFERENT
class (§3, `[#170]`'s verdict).

**The fork:** (a) drop the dead disjunct and require the nightly wiring outright; or (b) keep a
two-branch clause by re-expressing (b) as *record the manual-reporter scope + file the scheduling
work fresh*, which is what the draft does. The draft takes (b) because it preserves the row's
either/or structure without inventing a target; a reader who prefers (a) can delete the second
half of the draft with no other change. **Not converted silently, and not guessed.**

Note also: `scripts/fleet_analytics.py` does appear in `.github/workflows/report-only-wall.yml`,
but in the wall's **path/test scope**, not as a scheduled invocation — so the row's core premise
(nothing fires it nightly) still holds.

### 5.3 · `[#417]` — the clause appears already met in live code

The row states the defect as *"`scripts/session_end_backpressure.py:340-349` calls a bare `git
status --porcelain`."* Live, `check_dirty_tree` at `scripts/session_end_backpressure.py:412`
filters that output through `_is_lane_owned_daily` (line 402), which excludes exactly the
untracked `ecosystem/*/history/*.md` dailies the row names — and the test leg exists too, in both
directions: `tests/test_session_end_backpressure.py:758`
`test_lane_owned_daily_present_on_the_lane_does_not_flag`, with siblings at 770/779/794 asserting
a stray untracked file **still** fires and an unreplicated daily is never excused. Landed via
`4bef950`.

**The fork:** (a) the Done-when is discharged and the correct act is a closure proposal, not a
conversion; or (b) something in the row's intent remains unbuilt (its note about extracting the
shared scope list from `scripts/audit.py:2625-2633` is not addressed by what landed) and the
converted clause should carry that remainder. **This lane proposes neither** — it edits no row and
closes nothing. The draft is supplied for reading (b); under reading (a) it is simply moot.

### 5.4 · `[#502]` — the stated blocker is discharged

The row reads *"**BLOCKED ON `[#501]`** — until that wall exists there is nowhere to host the
eval."* `[#501]` is **`status: closed`**, and the wall is live at
`.github/workflows/report-only-wall.yml` (16,640 bytes; it already runs `uv sync --locked --group
analytics`). The host the row was waiting for now exists.

**The fork:** whether the row is simply unblocked and ready to run as written, or whether the
report-only constraint changes the eval's shape — `[#501]` is REPORT-ONLY by standing ruling
(Free tier, private repo, no promote-to-gate path), so a mutation pilot hosted there **records**
a result and can never gate on it. The draft names the live host and keeps the row's own
ADOPT/REJECT framing, which is compatible with report-only. Worth an explicit word at review,
since "runs on CI" reads differently once the CI in question is a recorder.

---

## 8. Arithmetic

- **30 drafts produced** — 29 needs-draft rows + the 1 `[#419]` re-check. **0 skipped.**
- **4 ambiguity-flagged** — `[#364]` `[#391]` `[#417]` `[#502]`, each drafted, each fork named (§7).
- **Form E applied 13×**, **Form R applied 6×**; 3 open home-substitutions listed in §2.
- **L14 re-resolve:** 30/30 verified `status: open` live before drafting.
- **Supersedes:** the census's `[#419]` draft (stale against the 2026-08-11 amendment). Every
  other draft here is new — the census drafted only its P1+P2 band, and these 29 rows are P3.
- **Locator drift found while drafting** (each repaired in the draft by naming a key or section
  rather than a line): `[#146]` PLAYBOOK `1016-1024` → the de-hardcode paragraph now at `1032` ·
  `[#263]` `doc-code-edge.yaml` `L110` → `L115` · `[#361]` guard scope cited at `:83` → `:9` ·
  `[#417]` `:340-349` → `:412`. Substance held in all four; only the pins had rotted.
- **Referent defects found and worked around, not papered over:** `[#391]` → `[#384]` closed
  (§5.2) · `[#412]` → `refs ROUTING.md`, no such file in the tree (draft homes the doctrine at
  PLAYBOOK) · `[#285]` → row names `_FRESHNESS_FILES`, but the editable constant is
  `_HUB_ONLY_FRESHNESS_FILES` · `[#443]` → `docs/audits/README.md` is generated and hook-gated,
  so it cannot host doctrine.

**These drafts bind nothing.** They apply only under a later operator ruling, after architect
review and the wave-2 GO. Conversion lanes consume this file; they do not inherit authority from
it.
