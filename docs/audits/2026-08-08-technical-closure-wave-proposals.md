# Closure wave — verified close PROPOSALS from the [#506] open set

<!-- scope: meta -->

**This file proposes; it closes nothing.** No `closes` token was issued, no `tasks/` record
was edited, no BACKLOG row was removed, no generator was rerun beyond the one this repo's
`audit-index-freshness` hook mandates. Per-id adjudication is the architect's; this file is
the evidence that makes each call cheap.

| Field | Value |
|---|---|
| **Generated at** | 2026-08-08, lane `worktree-lane-wave-closures` |
| **HEAD read** | `3ed60c4c` (`main` at lane-branch base) |
| **Source sheet** | `docs/audits/2026-08-08-technical-506-open-set-grooming-sheet.md` @ `worktree-lane-506-groom-sheet` (unmerged) |
| **Live open-count** | **202** (see §0) |
| **In scope** | **194** (202 − 8 batch-3 exclusions) |
| **Proposed for close** | **3** |

---

## 0. Enumeration reconciliation — what 202 counts, and what 169 counts

Both numbers are live and both are correct; they count **different sets**, and neither is
wrong. The 169 is a strict subset of the 202.

**The 202 — `validate_backlog.py`'s task count.**

```
$ python scripts/validate_backlog.py
validate_backlog: OK (9 themes, 26 stories, 202 tasks, 1 warning(s))
```

**The 169 — `tasks/*.md` frontmatter `status: open`.**

```
$ grep -h '^status:' tasks/*.md | sort | uniq -c
     44 status: closed
     33 status: deferred
    169 status: open
      1 status: retired
      1 status: superseded
```

**The reconciliation: 169 open + 33 deferred = 202.** `validate_backlog`'s "tasks" figure is
the *live* set — everything not terminal — so it admits the 33 `status: deferred` rows that the
frontmatter-open filter excludes. Set-identity was checked, not inferred: the 202 ids from the
sheet's table and the 202 ids from `{open} ∪ {deferred}` compare **identical** (`Compare-Object`
returns no differences after normalising the `"[#N]"` frontmatter quoting to bare digits).

**Honest limit on the 169's provenance.** The contract says this window's boot gate reported
169. This lane's own `SessionStart` output carried three surfacing lines (changelog / self-arm /
nightly-triage) and **no open-count**, and no script in `scripts/` emits the figure — so the
number is reproducible from the filter above but its emitting organ was not located from inside
this lane. Reported as a filter, not attributed to a gate.

**Which figure is the velocity law's `open-total`?** The **202** — it is the set the sheet
enumerates, the set this report partitions, and the only one that includes the deferred rows a
close would also have to retire. The 169 is the right number for "actively open work" and the
wrong one for a closure denominator, because a deferred row is not a closed row.

---

## The verification bar as applied

The contract's bar: *a close proposal is valid only if the cited merge's actual DIFF discharges
the row's own Done-when.* Applied mechanically:

1. **Closure-declaration scan (deterministic).** `propose_closures.closure_ids` — the repo's own
   shared closure-token core, quoting-stripped — run over **all 4,637 commits reachable from
   `main`**, matched against the 202 live ids. **Result: exactly two live ids carry an ADR-65
   `closes [#N]` declaration anywhere in history — `[#430]` and `[#505]`** (and `[#505]`'s is the
   documented false positive). Every other in-scope row is open with *no closure ever declared*.
2. **Candidate re-derivation.** For each in-scope id, every `--first-parent main` merge citing
   `[#N]` in subject **or body** was re-derived from git rather than taken from the sheet (which
   truncates at 3). 67 in-scope rows carry ≥1 bracketed candidate merge.
3. **Diff inspection.** Those 67 rows were inspected against their Done-when clauses — file sets,
   hunks, and `<merge>^1..<merge>^2` work-commit logs — by ten parallel read-only agents,
   instructed to prefer `UNKNOWN` over a guess and to treat a subject citation as no evidence.
4. **Adversarial re-verification (main thread).** Every `DISCHARGED` claim was re-checked against
   **live HEAD state**, not the merge. Seven were claimed; **four were refuted and demoted** —
   see §6. Only what survived refutation is in Group A.

**The proposal store contributes nothing.** All 65 `logs/PROPOSALS-*.md` files were scanned in
the primary checkout. Across the whole store only **11 ids have ever been classified STRONG**
(`5 77 205 306 307 355 367 370 430 504 505`), and of those only `#430` and `#505` are still live —
both named above. Every one of the **153** pending proposals attached to an in-scope row is
**WEAK**, which the store's own header defines as *"a file the task names was modified, but no
`closes` fired… these are inferences, not declarations"*. The repo has rejected WEAK en bloc
before (`57ae83a6`: "39/39 WEAK proposals rejected at architect review"). **No Group-A proposal
in this report rests on a proposal-store entry.**

---

## 1. GROUP A — diff-verified closes (3)

Each row below: the merge's diff was read, the row's Done-when was decomposed clause by clause,
and **every clause was matched to named files and hunks**, then re-confirmed against live HEAD.
Proposed verdict for all three: **`close (ADR-65)`**.

### `[#213]` — PLAYBOOK rule/history condensation

- **Merge:** `9ab191f5` — docs/playbook-condensation — SEAL-1a PLAYBOOK rule/history condensation
- **Files:** `docs/audits/2026-06-26-playbook-condensation-rule-inventory.md, protocols/PLAYBOOK.md`
- **Done-when:** a rule-inventory diff shows zero rules lost AND every inbound pointer still resolves
- **Diff evidence:** The audit IS the required rule-inventory diff. §1: 'HARD metric — MET. Zero rules removed.' and 'Inbound-pointer integrity — MET. No chapter/section renumbered; every ##/### heading title preserved verbatim. All 14 ## ChN. + 18 Part-II ## N. headings present.' §2 carries the per-group preservation proof; §3 resolves NAME-, NUMBER- and LINE-style pointers individually.
- **Clauses:** all discharged — no clause left open.
- **Proposed verdict:** `close (ADR-65)`

### `[#215]` — Onboard + verify methodology in a new repo

- **Merge:** `32db7eb7` — feat/wave1-prep — repo-onboarding runbook + v1.3.x release contract
- **Files:** `protocols/REPO_ONBOARDING.md (created as docs/runbooks/repo-onboarding.md, relocated by e490275c), tests/test_floor_conformance.py`
- **Done-when:** one onboard runbook + a conformance verification exist (or the item is explicitly merged into #131 with a recorded reason)
- **Diff evidence:** The runbook carries '## Install sequence (#131)' and '## Conformance verify (#215)' as distinct sections plus '## Dry-run attestation (#215 acceptance)'. Its own header states: '#215 — the conformance-verify half (## Conformance verify). Done when: one onboard runbook + a conformance verification exist.' The attestation section names the verify commands as runnable-today and cites tests/test_floor_conformance.py (green) as the exercising harness.
- **Clauses:** all discharged — no clause left open.
- **Proposed verdict:** `close (ADR-65)`

### `[#441]` — Way-of-working: the DEFAULT is one strong self-contained prompt on primary; worktrees are the ex

- **Merge:** `2f924424` — docs/window-winddown-2026-07-29 — window wind-down + bundle cut
- **Files:** `protocols/PLAYBOOK.md, BACKLOG.md`
- **Done-when:** PLAYBOOK Ch8 carries the ruling + the four-condition test, and the ADR-61 worktree-discipline checks are reconciled so the corpus carries one launch test, not two
- **Diff evidence:** PLAYBOOK Ch8 now opens with '0 — Launch decision ([#441])' carrying (i) an explicit *Ruling record — ADOPTED (operator, 2026-07-29)*; (ii) 'The four-condition worktree test' with all four conditions and the 'One NO = fat prompt' rule; and (iii) an explicit '*Mapping from the superseded three-check test*' block reconciling the ADR-61-era checks ('disjoint substantive files' -> condition 2; 'two distinct goals' -> condition 1; conditions 3-4 are new), so the corpus carries one launch test. The one owed reconciliation (condition 2 vs the §8 allocation convention) is recorded as resolved at the intake #18 ratification 2026-07-30.
- **Clauses:** all discharged — no clause left open.
- **Proposed verdict:** `close (ADR-65)`

**Residual note the architect should carry into these three:**

- `[#215]` — its Done-when is the narrow *"one onboard runbook + a conformance verification
  exist"*, and that is met. Its **body prose** additionally ties the verify-half to `#171`
  (`ecosystem/conformance.md`), which is still open. The tie is body text, not a Done-when
  clause; closing `[#215]` does not close `[#171]` and does not orphan it.
- `[#213]` — the row also carries *"absorbs #214"*. `#214` is not in the live 202, so the
  absorption is already settled; the close orphans nothing.
- `[#441]` — JOURNAL 2026-07-29 (b) recorded *"the codification is live but closure is the
  Tier-1 loop's call and one reconciliation is still owed"*. That reconciliation (condition 2 vs
  the §8 allocation convention) is recorded discharged at the intake #18 ratification 2026-07-30,
  and the discharge is visible in the live PLAYBOOK Ch8 block.

---

## 2. GROUP B — evidence exists, the diff did not settle it (79)

Per the contract, Group B holds the `gap:bare-citation-only` class **plus every Group-A
candidate that failed the diff test**. That is 79 rows, and lumping them together would hide the
only distinction that matters to an adjudicator — so they are sub-split by *how far off* they are.

### B1 — partially discharged; one named check settles each (12)

Real work landed against the row and part of the Done-when is genuinely met. Each row names the
single clause still open and the one check that would settle it.

| id | title | merge | clause discharged | clause OPEN — the single settling check |
|---|---|---|---|---|
| `[#210]` | Convert journal-wrap no-ff WARNs from per-instance disposi | `984ad66e` | The wrap does now ride a --no-ff arc in practice (clause b), but the cited merge ADDS a third per-instance disposition rather than retiring the three. | the 3 per-instance dispositions then retire |
| `[#244]` | Essence-spec lifecycle epic | `2c869518` | P2 lands the remove leg with a 446-line prune test; ai-council's ruff component is demonstrably pruned and verified-ABSENT. Roster regeneration (P3, a7504565) and fleet_health drift surfacing (P4, 25b104ed) are separate merges tha | the roster regenerates without it, and per-repo drift surfaces in fleet_health — needs one read of a7504565 + 25b104ed |
| `[#267]` | Scope-exercising arc extension | `ffe4d875` | Half-b lands: engages: entries carry the scope condition (FIRED / ARMED-BUT-SKIPPED) and observer tests pin FIRED semantics. The merge explicitly marks half-a (the live consumer re-measurement) DEFERRED. | a consumer measurement shows both components FIRED under a scope-matching edit |
| `[#324]` | Phase-6 axis-2 carrier | `65c9827e` | Leg-c (the verb list) is codified: 186 keep / 34 archive-candidate / 0 delete-candidate across 220 audits. Legs (a) night-batch standing routine and (b) morning verdict-sheet consumer are absent from the diff. | the night-batch standing routine + morning verdict-sheet consumer are codified |
| `[#332]` | Fleet dependency-version parity | `2bc02196` | The check leg is fully built: dependency-baseline.yaml (versioned, version 1.0.0), the fleet_parity dependency leg, and AC-2 tests asserting WARN on a drifted consumer and AT_PARITY on a declared one — including below-baseline-pin | a versioned dependency manifest SHIPS WITH THE METHODOLOGY PACKAGE |
| `[#352]` | Versioned `.vscode` region decoration | `21ec4653` | The row's AMENDED done-when is literally satisfied at HEAD: .vscode/settings.json is versioned, holds exactly two highlight.regexes keyed on the owner=hub / owner=repo marker vocabulary, paints grey rgba(140,140,140) / navy rgba(3 | NONE in the current row text — but the record contradicts it: docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md is stamped 'render-status: PREDICTED / PENDING-ADOPTION — NOT WITNESSED' and says the stamp 'flips to WITNESSED only on that eye, i |
| `[#383]` | Execution waves per surface | `abbb1899` | Clauses (a) and (b) both executed and pasted verbatim into the wave record: desired_state_report shows no diverge cell on the 8 rows; fleet_parity reports 0 warn-undeclared / 0 must-absent / 0 tombstone-violated. | (c) the operator has read them — the merge body itself says 'Clause (c) needs the OPERATOR's read' |
| `[#402]` | Intake naming clause — DEPLOY the `YYYY-MM-DD-<class>-<slu | `fb868199` | README §4 gains the <class> grammar with companion fields — clause 1 met. The 4 post-ratification off-pattern docs are not dispositioned by this diff. | each of the 4 post-ratification off-pattern docs is dispositioned |
| `[#419]` | We run routines whose output nobody consumes | `903638c5` | ADR-105 lands Accepted, establishing the six-field routine row shape and gating at ACTIVATION, with check_routine_consumers(). But the check is scoped to marked BACKLOG rows (one row at acceptance); the merge body says '[#419] STA | every standing routine has a named consumer and a consumption path, and unconsumed output is surfaced |
| `[#430]` | Consumer template rejects root `conftest.py`; `fleet_parit | `47bd4f52` | Half (a) genuinely landed at 3cf3a5b0: new root-conftest LOCAL row with declared_by: ruling-2026-08-07-root-conftest, TEMPLATE_DECLARATION_MARKERS validated enum, disposition entry removed, 5 tests. Half (b) untouched — fleet_pari | (b) a ship-gate verdict is reproducible from the subject repo's own state |
| `[#438]` | Codify gate-class posture: terra design review BEFORE buil | `cb8c7b9d` | One arc did run under the posture (terra design review before build, 4-pass loop, TDD). But grep of protocols/PLAYBOOK.md returns zero occurrences of 'refusal-gate' or 'gate-class'. | PLAYBOOK carries the gate-class rule (which arcs it binds + what the design pass must answer) |
| `[#507]` | Report-only wall — decide the fourth recorded leg (`pre-co | `945598f9` | The merge implements LA-4 gating for the mutation-pilot job and fixes the LA-2 setup-uv input, with tests. Whether any artifact records an explicit RULING on the fourth leg (pre-commit run --all-files) — landed, or accepted-with-r | a ruling records either the leg landed or an explicit accepted-with-reason hold naming what stays unrecorded |

Two B1 rows deserve a sentence of their own, because both were claimed `DISCHARGED` by the
diff pass and both are refuted by the producing commit's own words:

- **`[#430]`** — `3cf3a5b0`'s body reads *"Closes [#430] half (a)"* and, five paragraphs later,
  *"[#430] REMAINS OPEN on half (b) — fleet_parity reads LIVE sibling state"*. Half (a) is
  genuinely, testably done (new `root-conftest` LOCAL row, `declared_by` promoted to a validated
  enum, the disposition entry removed rather than reworded, 5 tests). Half (b) is untouched:
  `fleet_parity.py`'s own module docstring still says *"reads sibling trees read-only"*, and the
  `declared_by` early-return covers declared LOCAL rows only. **This is the one row where the
  proposal store's STRONG classification is live and wrong** — see §6.
- **`[#332]`** — the check leg is fully built and tested; the *"ships with the methodology
  package"* clause is not. `grep dependency-baseline deploy/manifest-v*.yaml
  .claude/methodology-roster.md` returns **zero hits** — the baseline is hub-local and no carrier
  moves it. Both the 2026-07-13 and 2026-07-17 architect bundles say so verbatim: *"#328 / #332
  stay OPEN (consumer-side deploy carrier unbuilt)"*.

### B2 — cited merge inspected; it does not discharge the Done-when (52)

These rows have a bracketed candidate merge, the diff was read, and the merge **filed, trimmed,
journaled, narrowed, re-routed or dispositioned** the row without touching its Done-when. They
are in Group B only because the contract routes every failed Group-A candidate here; the evidence
is settled, not ambiguous. **None should be closed.**

| id | title | cited merge | what the diff actually did | clause left open |
|---|---|---|---|---|
| `[#218]` | Safe-removal gate M2+M3 boundary | `0bfa64b0` | Row trimmed for doc_rot and re-scoped to DEFER with peg #487. No gate logic in scripts/safe_remove.py. | the gate refuses a removal with an M2 referrer AND an M3 referrer on a fixture |
| `[#220]` | MODIFY / semantic-drift axis | `fbf4a2d0` | Filing merge only — row added to BACKLOG plus a JOURNAL entry. No verify-first pass recorded anywhere in the diff. | a verify-first pass records whether any existing organ detects a semantic/MODIFY change on a fixture |
| `[#227]` | Relocate AGENT_FRAMEWORK.md out of protocols/ | `fbf4a2d0` | Filing only. AGENT_FRAMEWORK.md is not moved and no inbound ref is repointed. | AGENT_FRAMEWORK.md lives under docs/ and every inbound ref resolves to the new path |
| `[#231]` | Consumer → hub feedback report | `7cc4b6a6` | Row added with metadata only. No schema, no destination, no consumer-side emitter. | a consumer that hits a methodology gap emits a structured hub-destined report (schema + destination defined) |
| `[#234]` | Cross-repo probe validator | `fef026ed` | Adds a cross_repo parameter and _resolve_status() that treats .claude/ paths as excluded -> 'skipped' (a WARN), which is the opposite of the PASS/FAIL the row asks for. No tests for the .claude/ distinction. | a cross-repo bundle whose floor-guard probe names a present .claude/<file> PASSes and one naming an absent .claude/<file> FAILs, with tests |
| `[#273]` | Changelog-review staleness escalation | `02389890` | Filed the row. No changelog_sentinel.py or fleet_health.py hunk; no thresholds recorded. | an over-threshold window renders an escalation line in the SessionStart digest (with a test) and the N/days thresholds are recorded |
| `[#274]` | Dogfood-signal prior in the /changelog-review ADOPT  | `02389890` | Files the row. .claude/commands/changelog-review.md is not modified; the ADOPT rubric is unchanged. | the command's ADOPT rubric names the dogfood-signal prior and one subsequent review demonstrably applies it |
| `[#300]` | Hermetization residual d.ii | `e490275c` | Row text updated to reflect the d.i reversal; BACKLOG still reads 'bundle sweep AWAITING explicit operator deletion GO'. | the mode-boot home is ruled AND the committed functional bundle's fate is landed |
| `[#305]` | Add a verify-only / already-onboarded re-run mode to | `e490275c` | Pure rename (0 insertions / 0 deletions in the diffstat). The file carries no verify-only re-run path and no dirty-tree assess support. | the runbook documents a verify-only re-run path AND assess runs on a dirty tree |
| `[#317]` | Default-parallel test invocation | `315a0345` | Merge subject says narrows, not closes. Leg (b) shipped; leg (a) — point the per-step verify cadence at parallel — remains in the row, and no measured <60s figure is recorded. | verify cadence parallel by default AND the 'not slow' run completes under 60s (measured time recorded at build) |
| `[#334]` | Fleet-wide ruff hook id migration `ruff` → `ruff-che | `97cf58e0` | BACKLOG.md only. No .pre-commit-config.yaml hunk in any repo; the hub still uses the legacy id. | all three repos use ruff-check and the legacy ruff alias is gone, witnessed per repo |
| `[#338]` | codex-review drift consolidation | `315a0345` | Narrows scope from (a)-(e) to (b)-(e) by striking leg (a) to #469. Narrowing is not discharge; (b)-(e) remain in the row text. | each of (b)-(e) resolved or recorded permanent-defer-with-reason |
| `[#344]` | Session-close gate for handoff generation + consumer | `7ef40567` | Row-text trim only (-2/+1). No mechanism file touched. | Ask 1 and Ask 2 are each resolved or recorded permanent-defer-with-reason |
| `[#348]` | Backlog grooming as a standing routine, not ad-hoc | `05450245` | Adds cross-references to [#348] from other rows; #348's own row is not modified and no routine definition (trigger/scope/consumption path) is created. | the grooming cadence is captured as a routine definition rather than per-session improvisation |
| `[#356]` | RULING-W and the merge-delegation composite are LEGI | `9a3fb86b` | Trimmed the row under doc_rot and added census findings. No PLAYBOOK/ESSENTIALS hunk adding a mechanism or a declared-unenforced entry. | RULING-W and the composite each carry either a mechanism or a declared-unenforced entry (owner + review date) |
| `[#369]` | Wire `boundary_headers.py --check` into pre-commit | `0e5d015b` | Records [#369] as work routed to W6. No .pre-commit-config.yaml hunk registering boundary_headers.py, no CLAUDE.md §9 entry, doc-counts not moved to 16 gates. | the hook is registered and blocks a hand-edited header, CLAUDE.md §9 lists it, and doc-counts reflects 16 gates |
| `[#371]` | Consumer editor-config write-through — declared at v | `3fc9458d` | Merge body states 'Files two new OPEN tickets — no closures in this merge'. deploy/manifest-v1.4.0.yaml still carries implemented: false. | the ADR rules the vehicle, the config reaches both consumers under it, and implemented: reflects reality |
| `[#389]` | Prompt-lint — gate the five architect fields before  | `db878f4c` | [#389] is named a ride-along filing. PLAYBOOK gains the delivery loop but no prompt-field validation lands. | R6 is ruled AND a seeded prompt missing a required field is refused/WARNed, with tests |
| `[#390]` | Resolve the ADR-87 effort-ownership contradiction, t | `db878f4c` | [#390] is a ride-along filing. ADR-87 is not amended (zero edits) and templates/prompt-template.md still carries Effort low\|medium\|high. | ADR-87 carries the resolution AND the template matches it |
| `[#391]` | Wire fleet_analytics into a nightly lane, or narrow  | `423a372e` | Filed six rows and relocated evidence. No scheduling wiring for fleet_analytics and no narrowing of #384. | fleet_analytics fires nightly OR #384 is narrowed to manual + scheduling filed separately |
| `[#400]` | Ownership-model: the hub-mandated-STRUCTURE / repo-o | `952c10ad` | The merge ADDS the annotation 'EFFECT OF THE owner=user RULING: NOT satisfied, NOT closure-eligible.' The row disposes ITSELF as not closeable. | the ownership-model ruling explicitly covers the roster cell and is recorded |
| `[#401]` | ai-council routing still ARMED at the deleted hub la | `c5f65165` | Merge body is explicit: 'Ruling only: no build, no test, no routing.py edit. Clause (a) is ai-council-side and untouched.' | (a) shipped in ai-council AND (b) built per this ruling |
| `[#403]` | Extend `doc_claims` to ARCHITECTURE's machine-deriva | `44e47b48` | Fixes the claims by hand (carrier count 4->5, child roster +win-tooling, Governing-ADRs 80->103). No scripts/audit.py or tests/ hunk gating them. | carrier-set AND child-roster gated (doc_claims or a regen-and-diff sibling) with tests |
| `[#404]` | gen_handoff execution-mode SUPPLEMENT leak (mode-bli | `de402b1c` | The merge subject itself says 'hand-corrected to §13 shape; generator SUPPLEMENT leak'. The bundle was fixed by hand; scripts/gen_handoff.py was not. | an execution-mode render passes verify_handoff_probes with zero SUPPLEMENT references, pinned by a per-mode test |
| `[#405]` | Session-end leftover check — nothing verifies \"no l | `21a21e81` | Across all three cited merges (b4dd3e48 trim/close-out, f3ead30b doc_rot trim, 21a21e81 filing): b4dd3e48 states the guard is 'proposed in one line, not built'. scripts/session_end_backpressure.py is untouched. | the Stop-hook hygiene leg flags each named leftover class with a test |
| `[#406]` | Commit-time doc_rot surfacing — an over-threshold BA | `5eebee91` | Re-routes the row to the architect lane per ADR-108 §A. Routing is not a ruling; no enforcement point picked, no accept-as-is recorded. | an architect ruling picks the enforcement point (or records accept-as-is) |
| `[#408]` | Auto-coupled doc updates — closing a backlog item mu | `b8957c98` | A 409-line design doc plus a pointer. Design is documented, not built — no audit check, no test. | closing a backlog item mechanically surfaces or blocks on the coupled ARCHITECTURE + JOURNAL updates, with a test |
| `[#414]` | Self-acting-on-main incident family — a session chan | `5eebee91` | Merge body: '[#414] re-routed to the architect lane per ADR-108 §A'. Routing, not a ruling. | an architect ruling picks the organ(s) and the mechanism refuses/flags a no-GO or unanchored change to main with a test |
| `[#415]` | Tests must bind fixtures, not live mutable repo cont | `8e2ecc80` | One test re-pointed to a fixture with teeth verified. The sibling audit across the other live-content-coupled tests was not run. | the sibling audit is run and each live-content-coupled test is re-pointed to a fixture or recorded justified |
| `[#422]` | `reflow_framing`'s cold→FILLED flip is partial by de | `b4dd3e48` | Merge body claims a manual sweep 'zero surviving cold-state claims'. A sweep is not a check: no Python or test hunk in the diff. | a post-fold check FAILs on a bundle carrying cold-state framing prose after a FILLED flip, pinned by a test |
| `[#423]` | The integration sequence runs on prose every time, n | `c74f918c` | Files [#423] and dispositions other items. The /ship command is unchanged; no precondition is mechanized. | /ship carries the sequence with each precondition checked mechanically, or the gap is recorded permanent-defer-with-reason |
| `[#424]` | Backlog `depends-on` gates are INERT — `_DEPID_RE` r | `42ff1323` | Updates the census from 8/4-inert to 6 clauses / 4 parse / 2 inert. Two inert clauses remain ([#389] '390', [#385] '383'); no parser change, no regression test, no plugin twin move. | every depends-on clause parses, a regression test pins the bare-id form, and the tier1-lifecycle twin moves in lockstep |
| `[#426]` | Declare `consumer` + `consumption_path` for every LI | `903638c5` | Adds the routine_consumers check (ALL_CHECKS 31->32) but its own docstring scopes it to marked BACKLOG rows; the merge body says '[#426] files the retrofit'. ~30 live routines uncovered. | every live routine declares a consumer and consumption path or is retired |
| `[#427]` | Region templates carry a repo-POSITION-DEPENDENT pat | `863cb804` | BACKLOG.md only — the row was filed. No templates/claude-regions/ hunk, no per-consumer substitution. | the carry mechanism supports a per-consumer substitution and ai-council's divergence retires by reference |
| `[#428]` | `nightly-triage` reports a dead producer to every se | `495b8a22` | Narrowed, not closed — the row now reads 'NARROWED by [#434]'s ruling — BUILD THE CONSUMER'. surface_triage.ps1 unchanged; the 15 open Issues are undispositioned (this session's own boot printed all 15). | no session-start surface asserts pending work from a producer that does not run, AND the 15 open Issues are dispositioned or the surface is retired |
| `[#431]` | `codex-review` silently drops the doc lane on any mi | `d584ff4a` | Across all six cited merges: rows filed and the severity-counter defect recorded. No mixed-diff dual-profile routing, no loud skipped-prose warning, no counter fix. | a mixed diff gets both profiles or emits a loud skipped-prose warning naming the unreviewed files, AND the counter agrees with the body |
| `[#442]` | Plugin command-cache staleness — cached command text | `952c10ad` | Filed the row with full prose. No cache invalidation, no load-time stamp comparison, no seeded-stale test. | a stale cached command cannot be served unnoticed, with a test that seeds a stale copy |
| `[#443]` | Planning artifacts outside the three enforced classe | `31fe0e01` | Row creation only. No rent/binding rule stated at any canonical home for the uncovered classes. | each uncovered class carries either a stated rent/binding rule or a recorded deliberately-not-a-rule with its reason |
| `[#447]` | Self-referential gate family — the committing act ca | `ebda157e` | All three cited merges touch handoff bundles, JOURNAL and BACKLOG/tasks only. No hunk in scripts/arm_hooks.py or scripts/session_end_backpressure.py. | one commit can raise a ratchet and be judged by the raised value, and a wrap commit can satisfy its own anchor gate, with tests |
| `[#448]` | A11 staged-diff guard — cover EVERY candidate bundle | `3f4a1819` | Files the row. No hunk in scripts/audit.py check_handoff_probes and no test. | a staged diff containing two candidate bundles fails the guard when either is uncovered, with a test |
| `[#449]` | Assembled-paste byte budget — should `PASTE_THIS.md` | `65a549bf` | Merge body: 'all four new rows are question-shaped or gap rows with no existing owner... each declines the scope'. No byte budget ruled, no accepted-with-reason hold recorded. | a ruling records either a hard budget (with its number and gate) or an explicit accepted-with-reason hold |
| `[#452]` | `[#433]`→`[#382]` pilot-precedes-contract dependency | `65a549bf` | Files the question-shaped row. No depends-on clause added to tasks/433-*.md or tasks/382-*.md, no intentionally-prose-carried record. | the pair is either expressed as a parseable depends-on clause or recorded as intentionally prose-carried |
| `[#457]` | Two live-repo tests fail on main against green gates | `05450245` | Task annotation flipped from 'census the six-field rows BEFORE repinning' to 'census DONE'. No hunk in tests/test_audit.py or scripts/audit.py. Merge 461fa233 records 'Full suite 2357 passed / 2 failed — both f | both tests pass on main for verified reasons |
| `[#463]` | win-tooling onboarding debt — 2 FAILs + 2 WARNs unch | `13b98f22` | Filing only. None of the four win-tooling defects is fixed and the fleet baseline is not shown green. | each of the four is fixed in win-tooling or recorded accept-with-reason, and the fleet baseline shows win-tooling green |
| `[#464]` | corp-*/ai-council governance drift — five findings l | `13b98f22` | Filed three rows documenting five findings across consumer repos. No consumer repo is touched; no fix, no accept-with-reason. | each of the five is fixed in its repo or recorded accept-with-reason |
| `[#470]` | `audit.py checks` crashes mid-listing on a cp1252 co | `4306a46a` | Merge body: 'the two carried wrap items, filed not acted on'. No U+2192 swap in scripts/audit.py and no cp1252-encodability regression. | the U+2192 is ASCII-swapped and a regression asserts every ALL_CHECKS docstring first line is cp1252-encodable |
| `[#477]` | `deployed_methodology_version` keys the registry by  | `0c64a76a` | Filed from night-batch defects. No hunk fixing the basename keying in scripts/audit.py, no clone-name-variance test. | the check resolves the hub's row from a checkout whose directory name differs from the registry key, with a test |
| `[#499]` | Promote the review-artifact coverage leg to a hard p | `e676cd3f` | Closes [#480] (the advisory WARN leg) and files [#499]. Merge body: 'The hard pre-push leg stays DEFERRED behind its evidence bar'. doc-code-edge.yaml still carries the TEMPORARY exempt entry. | two consecutive windows sealed with a 0 false-positive count, the hard leg lands with tests, and the coverage debt is discharged |
| `[#500]` | The Stop hook's BACKLOG advisory reads a correctly-c | `e676cd3f` | Filed the row only; merge body states [#500] records the defect. No hunk in scripts/session_end_backpressure.py, no test. | the advisory recognises row-DELETION plus the paired tasks/*.md terminal-status flip, pinned by a test |
| `[#502]` | mutmut 3.7.0 mutation-testing evaluation — CI-hosted | `3234abb3` | The merge body states '[#502] stays OPEN until real numbers exist'; 945598f9 repeats 'blocker chain is fixed but no mutation numbers exist yet'; 4ad76bc5 'deliberately NOT closed — zero mutants measured'. | a scoped pilot runs on CI and the result is a recorded ADOPT/REJECT with measured divergence |
| `[#508]` | Couple the lane-prefix enum's cardinality to its pro | `945598f9` | Merge body reports 'enum drift 0 sites' — the four prose sites were repaired by hand at d388d0f2. That is the symptom, not the coupling: no check was added to validate_doc_claims.py or audit.py, and no ruling r | a check FAILs when cardinality and in-repo prose disagree (pinned by a test that flips one), or a ruling records it deliberately unmechanized |
| `[#511]` | The 30-minute handoff cut is ~99.8% session authorin | `b669bd8f` | The version bump (6.0.1 -> 6.1.0) and a measured byte delta (3,948 B -> 2,909 B, -26.3%) are both real and in the tree. But the arc's own packet states: 'Zero rows filed, zero closed. [#511] is consumed, not cl | the operator rules WHICH LOAD is cut and by how much |

Recurring shape worth naming, measured rather than eyeballed: for each B2 row, the oldest
first-parent merge whose diff ADDS that row's `- [#N] ` line to `BACKLOG.md` was computed
(`git log --first-parent main --merges -S'- [#N] ' -- BACKLOG.md`) and compared with the cited
merge. **In 30 of the 52 rows they are the same commit — the cited "candidate closing merge" is
the merge that CREATED the row.** A filing merge cites the id it files, subject-citation records
it as a closure candidate, and the row reads as having evidence when the evidence is its own
birth certificate. That is the structural reason the sheet's `complete` flag runs so far ahead of
closeability.

```
cited merge == the row's filing merge (30 of 52):
  [#220]  [#227]  [#231]  [#234]  [#273]  [#274]  [#334]  [#369]  [#371]  [#389]
  [#390]  [#391]  [#403]  [#404]  [#405]  [#415]  [#426]  [#427]  [#431]  [#442]
  [#443]  [#448]  [#449]  [#452]  [#463]  [#464]  [#477]  [#499]  [#500]  [#508]
```

### B3 — bare-`#N` citation only; the subject must be read before it counts (15)

The sheet's `gap:bare-citation-only` class, carried through unchanged. Each row's only signal is
an unbracketed `#N` in a merge subject, which the sheet's own precision caveat marks as
namespace-free and unsafe to count. **Single settling check for every row in this class:** read
the cited subject and decide whether the `#N` is this backlog id or a different registry
(`intake #N`, `consult #N`, or a bare enumerator like `#1 … #4`). Low ids are the ones to distrust.

| id | title | bare-cited merge | subject to read |
|---|---|---|---|
| `[#4]` | Build lessons-index.json + SessionStart retrieval + CLI | `a0f5aac2` | Merge feat/consult1-disposition — disposition the 4 Fable consult #1 rulings: #1 ADR-81 |
| `[#19]` | Complete the ADR-39 register | `1ee48e68` | Merge chore/backlog-groom-134 — #134 n=1 backlog groom: 78->67 tasks. closes [#81] close |
| `[#23]` | Validate ADR frontmatter relation-fields | `ee61dff9` | Merge docs/handoff-ai-council-p6-window — ai-council P6 window-completion handoff bundle |
| `[#71]` | Reconcile ENVIRONMENT.md's `~/.claude/` directory tree  | `1ee48e68` | Merge chore/backlog-groom-134 — #134 n=1 backlog groom: 78->67 tasks. closes [#81] close |
| `[#82]` | Define per-repository agentic-review profiles | `a4d081bd` | Merge docs/backlog-capture-sota — SOTA gap analysis: #102-#111 + annotations #17/#82/#96 |
| `[#102]` | Machine-readable repo index for agent consumption | `a4d081bd` | Merge docs/backlog-capture-sota — SOTA gap analysis: #102-#111 + annotations #17/#82/#96 |
| `[#123]` | Routine observability convention + value review | `08c5ef81` | Merge docs/backlog-routine-observability — add #123 routine observability convention + v |
| `[#144]` | Feature DoD = end-to-end / user-flow test | `57dd61a2` | Merge docs/a2-acceptance-contract --no-ff -- A2: test-first acceptance contract generali |
| `[#145]` | Codification-completeness pass | `8f5694b8` | Merge docs/a4-contract-essence-completion --no-ff -- A4: Architect Operating Contract es |
| `[#146]` | De-hardcode-first doctrine + sweep | `afe1bd8a` | Merge docs/backlog-146-dehardcode — file #146 de-hardcode-first doctrine + sweep (ADR-81 |
| `[#188]` | Deny-rule + hook completeness audit | `de7d0405` | Merge chore/file-191-onedrive-filepath-guard --no-ff -- file #191 (file_path PreToolUse |
| `[#189]` | Execute in ~/.claude | `62763d73` | Merge chore/backlog-groom-2026-06-18 -- apply approved 2026-06-18 groom: close [#138] (d |
| `[#190]` | General intra-file duplication detector | `e48da286` | Merge grooming-amended --no-ff -- Phase-1 seal Track C: #140 doc_rot grooming-gate (ADR- |
| `[#288]` | Model-identity guard for unattended runs | `29054cf6` | Merge docs/2026-07-08-intake-seed-block -- intake SEED block: 4 func intake docs (ids 6- |
| `[#341]` | Codex producer-lane activation mechanism | `91b36fbe` | merge: docs/codex-role-governance — Codex role-governance R1/R4/R5 doctrine + #341 produ |

---

## 3. GROUP C — superseded / obsolete candidates (0)

**Empty, and the emptiness was tested rather than assumed.** Every in-scope live row was scanned
for supersession language — `superseded by`, `absorbed`, `folded into`, `subsumed`, `owned by
[#N]`, `OBSOLETE`, `shipped elsewhere`, `already shipped/landed/done`. The scan returned 24 rows,
and **every hit fails to yield a close proposal** for one of three reasons:

- **Wrong direction (13 rows).** `absorbs #N` means *this* row swallowed another; it is evidence
  the row is larger, not that it is dead. Examples: `[#112]` absorbs #105+#157, `[#170]` absorbs
  #168+#243, `[#285]` absorbs six ids, `[#277]` absorbs #211.
- **A negation inside `kill-candidates:` (8 rows).** `[#334]` `[#342]` `[#343]` `[#344]` `[#345]`
  `[#347]` `[#351]` `[#352]` each carry the phrase *"no existing task subsumes…"* — the literal
  assertion that nothing supersedes them. A naive grep reads these as supersession hits; they are
  its opposite.
- **Superseded scope, deliberately-retained row (1 row).** `[#43]` is the only genuine
  supersession in the set: *"2026-07-08: scaffold scope folded into
  `docs/intake/2026-07-08-func-new-project-bootstrap.md` (intake-id 6) — superseded-by that
  intake"*. But the same sentence continues: *"**this task persists as the decomposition target
  the technical triage will decompose**"*. The row forecloses its own closure in its own text.

Two rows dispose of *themselves* as not-closeable and are filed in Group D rather than here,
because they are not superseded — they are blocked: `[#400]` and `[#413]` both carry *"EFFECT OF
THE `owner=user` RULING: NOT satisfied, NOT closure-eligible."*

---

## 4. GROUP D — stays open, gap named (112)

No verdict proposed. One line each, naming what is actually missing.

### D1 — WEAK-proposal-only or branch-only signal, no bracketed merge (90)

The sheet flags these `complete` because a pending closure-proposal exists. **That flag measures
the sheet's evidence, not the row's condition, and here it overstates:** every one of these
proposals is WEAK — the file-touch inference the store itself disclaims. The gap is identical
across all 90 rows: **no closure was ever declared and no merge cites the id, so there is nothing
to diff-test.** Adjudicating these is archaeology against the row's own Done-when, not against a
commit.

```
  [#43]  [#132]  [#139]  [#153]  [#162]  [#169]  [#170]  [#171]  [#181]  [#239]  [#240]  [#241]  [#242]  [#245]
  [#263]  [#266]  [#269]  [#270]  [#271]  [#276]  [#277]  [#278]  [#280]  [#281]  [#285]  [#290]  [#293]  [#294]
  [#296]  [#297]  [#298]  [#301]  [#303]  [#308]  [#310]  [#315]  [#322]  [#323]  [#325]  [#327]  [#329]  [#331]
  [#335]  [#340]  [#342]  [#343]  [#345]  [#349]  [#350]  [#351]  [#353]  [#354]  [#357]  [#358]  [#359]  [#360]
  [#361]  [#364]  [#365]  [#366]  [#385]  [#387]  [#388]  [#392]  [#397]  [#399]  [#413]  [#417]  [#418]  [#420]
  [#425]  [#440]  [#445]  [#450]  [#451]  [#453]  [#454]  [#484]  [#485]  [#486]  [#487]  [#488]  [#491]  [#492]
  [#493]  [#495]  [#496]  [#497]  [#509]  [#510]
```

Spot-checked one at random against live HEAD to confirm the class is honest rather than merely
unexamined: **`[#269]`** (audit-index count-tiered shape) — its Done-when asks for the
count-tiered shape plus a header repointed to ADR-100. Live `docs/audits/README.md` renders
**426 documents grouped by month**, not a fresh-20 + archive-section shape, and its header still
names `[#212]` as the open policy. Both clauses open. The row is correct to be open.

### D2 — no closure signal at all (22)

The sheet's `gap:no-closure-signal` class: no candidate merge, no branch ref, no pending
proposal. This is the irreducible archaeology — 22 rows the evidence half could not shrink.

| id | title | named gap |
|---|---|---|
| `[#99]` | FLEET-HEALTH digest names the failing check per red repo | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#112]` | adr_amend helper + ADR immutable-zone extension | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#116]` | Hooks hygiene | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#117]` | Evaluate prompt/agent-based hooks | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#122]` | Retire the PATH shim | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#126]` | Backpressure-loop pattern evaluation | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#127]` | verify skill failure-output contract | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#130]` | Memory-hygiene review | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#166]` | doctrine_enforcement_coherence check | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#185]` | GAP-2 deterministic gotcha-injection guard | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#289]` | Hub-own the OneDrive-Blue-Yonder guard | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#346]` | Persist the two-tier new-path executor rule into `~/.claude` | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#347]` | Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion p | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#362]` | #242 carries a SUBSTANTIVE guard loss, not status hygiene | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#407]` | Universal fleet Python style — functional-vs-OOP stance + uniform naming (the  | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#409]` | Standing night batch — CODE review (formalize as routine) | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#410]` | Standing night batch — ARCHITECTURE review (formalize as routine) | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#411]` | Standing night batch — creative session, and the recurring Q&A cadence | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#412]` | Subagent / workflow routing + configured fan-out + online research into Anthro | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#456]` | Ruling-blocked cohort sweep — re-route the remaining Done-when clauses per ADR | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#478]` | `changelog_sentinel` drops PEP 440 suffixes — a prerelease as the reviewed val | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |
| `[#494]` | Ladder ratification — L0–L5 promote-vs-leave is unruled, and prose already cit | no candidate merge, no branch ref, no proposal — adjudicate from the row's Done-when against live state |

Two of these carry a **self-declared** blocker rather than an absence, and should be read
differently from the other twenty:

- `[#400]` / `[#413]` — both annotated *"EFFECT OF THE `owner=user` RULING (recorded on [#370]):
  NOT satisfied, NOT closure-eligible."* These are not un-evidenced; they are ruled-blocked, and
  the blocker is the second ownership ruling, not archaeology. (`[#400]` sits in B2 by candidate
  merge; `[#413]` sits in D1. Named here so the pair reads together.)

---

## 5. Counts and velocity preview

| Group | Rows | Meaning |
|---|---|---|
| **A** — diff-verified close | **3** | every Done-when clause matched to hunks, re-verified at HEAD |
| **B1** — partial, one check settles | 12 | real work landed; one named clause open |
| **B2** — merge inspected, does not discharge | 52 | filed / trimmed / journaled / narrowed / re-routed |
| **B3** — bare-citation-only | 15 | read the subject before the citation counts |
| **C** — superseded / obsolete | 0 | tested for; see §3 |
| **D1** — WEAK-proposal or branch signal only | 90 | no closure declared, no merge cites the id |
| **D2** — no closure signal | 22 | irreducible archaeology |
| **In scope** | **194** | 202 − 8 excluded |
| **Excluded** | 8 | batch-3 owns them (§7) |
| **Total** | **202** | = live open-count |

**Proposed-close total: 3.**

**Velocity preview — if the architect ratifies all of Group A:**

| Measure | Now | After Group A | Δ |
|---|---|---|---|
| `open-total` (live: open + deferred) | 202 | **199** | −3 |
| frontmatter `status: open` | 169 | **166** | −3 |
| `status: deferred` | 33 | 33 | 0 |

All three Group-A rows are `status: open` (none is deferred), so both counters move by 3.

**The honest headline: a whole-set diff-verified sweep of 194 open rows yields 3 defensible
closes — 1.5%.** That is not a failure of the sweep; it is the measurement. The backlog is not
carrying a large stock of silently-finished work. It is carrying 79 rows with partial or
ambiguous evidence and 112 rows with none, and the bottleneck is adjudication capacity, not
closure detection.

---

## 6. Known-FP register and refuted claims

### 6a. Matcher false positives — listed, never proposed for close

| id | commit | why the matcher misreads it | in scope? |
|---|---|---|---|
| `[#505]` | `25ff8ec3` | Subject *"3 rows filed, **0 closed** [#505] [#430]"* — `CLOSES_RE` fires on `closed [#505]` while the subject explicitly declares zero closures. The `[#454]` negation defect, already dispositioned by the repo. | no — excluded |
| `[#430]` | `3cf3a5b0` | **A new instance, and a different failure mode.** The body genuinely says `Closes [#430]` — but it says `Closes [#430] **half (a)**`, and the same message later states `[#430] REMAINS OPEN on half (b)`. `closure_ids` reads a **scope-qualified partial closure as a whole-row closure**, which is why `propose_closures` promoted `#430` to **STRONG — closing commit landed, item still open** in `logs/PROPOSALS-2026-08-08.md`. | **yes** |

`[#430]` is the one in-scope row where the live proposal store actively recommends a close that
the evidence refutes. It is filed to **B1**, never to A. The defect generalises: `[#454]` covers
the *negation* case (`0 closed [#N]`); the *scope-qualifier* case (`Closes [#N] half (a)`) is a
sibling no open row names.

### 6b. Claims made by the diff pass and refuted on re-verification

Seven rows were returned `DISCHARGED` by the parallel diff inspection. Four did not survive
re-checking against live HEAD and the producing commits' own text. Recorded because a
suppressed refutation is how a bad close gets ratified.

| id | claimed | refuted by | landed in |
|---|---|---|---|
| `[#430]` | DISCHARGED at `47bd4f52` | `3cf3a5b0`'s own body: *"[#430] REMAINS OPEN on half (b)"*; `fleet_parity.py` still walks sibling trees | B1 |
| `[#332]` | DISCHARGED at `2bc02196` | `grep dependency-baseline deploy/manifest-v*.yaml` → 0 hits; two architect bundles record *"#332 stays OPEN (consumer-side deploy carrier unbuilt)"* | B1 |
| `[#511]` | DISCHARGED at `b669bd8f` | the arc's own packet: *"[#511] is consumed, not closed — its done-when asks the operator to rule which load is cut, and this arc cut none of the three"* | B2 |
| `[#352]` | DISCHARGED at `21ec4653` | `docs/audits/2026-07-20-…-352-boundary-render-diagnostic.md` is stamped *"render-status: PREDICTED / PENDING-ADOPTION — NOT WITNESSED"* | B1 |

**`[#352]` is the one that needs an architect sentence, not another check.** Its *current* row
Done-when is literally satisfied at HEAD — `.vscode/settings.json` is versioned, holds exactly two
`highlight.regexes` keyed on the `owner=hub` / `owner=repo` marker vocabulary, paints grey
`rgba(140,140,140)` / navy `rgba(38,79,140)`, scopes to `CLAUDE.md` + `.claude/*.md`, and carries
no per-region state. But the record carries a clause the current row no longer enumerates:
JOURNAL 6847 states *"`[#352]` IS MERGED BUT NOT CLOSED… it stays open pending that render
confirmation"*, and the render diagnostic says its stamp *"flips to WITNESSED only on that eye,
in a later commit"* — which has not happened. The visible-boundary-lane **AMENDMENT** in the row
names only the *generator* clause as satisfied-by-elimination; it is silent on the render witness,
which nonetheless vanished from the row text. **The question is whether the amendment retired the
render clause or narrowed the row past it** — a ruling, not a diff.

---

## 7. Excluded — batch-3 owns these (8)

Listed with reason, per the contract. **Nothing is proposed for any of them**; closing one here
would race the batch-3 integration.

| id | title | reason |
|---|---|---|
| `[#283]` | corp-monorepo `hybrid_classifier.json` 1.08MB duplication | batch-3 lane `worktree-lane-a-283-dedup` (corp-monorepo classifier dedup) |
| `[#416]` | ai-council `ARCHITECTURE.md` codemap drift at L23/L109 | batch-3 lane `worktree-lane-b-416-codemap` (ai-council codemap drift) |
| `[#393]` | corp-sca rot review — confirm-live-or-retire 3 candidates | batch-3 lane `worktree-lane-c-393-rot` (corp-sca rot review) |
| `[#282]` | Fleet `.gitattributes` EOL-normalization parity | batch-3 lane `worktree-lane-d-282-eol` (fleet .gitattributes EOL parity) |
| `[#396]` | Extract `scripts/gitenv.py` — the GIT_* env-scrub is in 3 plac | batch-3 lane `worktree-lane-e-gitenv-scrub` (gitenv extraction) |
| `[#512]` | `gen_handoff.py`'s open-batch refusal doesn't scrub `GIT_DIR` | batch-3 lane `worktree-lane-e-gitenv-scrub` (shares the gitenv lane) |
| `[#505]` | Batch-protocol encoding — the parallel-execution way-of-workin | batch-3 owns it (ADR-110 batch-protocol encoding); also the known-FP subject |
| `[#506]` | Whole-set P10 grooming arc — the open set is unreconciled | this arc's own parent row (`worktree-lane-506-groom-sheet`) |

---

## 8. Where the evidence contradicted the sheet

The sheet is an evidence artifact and says so; these are not defects in it, they are the places
its mechanical columns and the diff disagree. Recorded because the architect reads both.

1. **`complete` (165 rows) overstates closeability by roughly two orders of magnitude.** The flag
   means *"carries at least one signal to adjudicate against"*, and it is accurate on its own
   terms. But 153 of those signals are WEAK proposals, and diff-testing the remaining candidate
   merges yields **3** defensible closes out of 194. The flag and closeability are close to
   uncorrelated in this set.
2. **A filing merge is indistinguishable from a closing merge in the candidate column.** Measured:
   **30 of the 52** B2 rows cite the very merge that created the row. Subject citation cannot
   separate birth from death.
3. **`[#430]` carries a live STRONG proposal that the evidence refutes** (§6a) — the sheet's third
   caveat correctly flagged `[#505]`'s FP; this is a second, structurally different one that the
   sheet did not have cause to surface.
4. **Zero closure declarations exist for 192 of the 194 in-scope rows.** The full-history
   `closure_ids` scan is a stronger negative than the sheet's per-row columns can express: it is
   not that these rows lack a *cited* merge, it is that no commit in 4,637 has ever declared them
   closed.

---

**Produced by:** lane `worktree-lane-wave-closures`, `[#506]` closure-proposal wave.
**Writes made by this arc:** this file, plus the `audit-index-freshness`-mandated regeneration of
`docs/audits/README.md`. No `tasks/` edit, no `BACKLOG.md` edit, no `logs/` write, no write to the
primary checkout, no `closes` token, no JOURNAL entry (the integrator anchors this branch at merge).
