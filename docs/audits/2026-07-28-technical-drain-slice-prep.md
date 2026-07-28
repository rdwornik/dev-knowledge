# Drain-slice prep — input for the 2026-08-26 drain review ([E8] clause (b), ruling D1)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-28 · **Slug:** drain-slice-prep
- **Serves:** the **2026-08-26** drain review — slice **[#356] + [#358]–[#361]** selected by operator ruling D1
  (2026-07-28), recorded in the `[E8]` clause-(b) amendment blockquote (`BACKLOG.md:314`). Architect prepares /
  operator ratifies.
- **Arc:** PROMPT P6 prep arc, branch `docs/p6-dated-pressure-prep`.

> **PREP, NOT EXECUTION.** This artifact proposes dispositions; it executes none. No rule is drained, mechanized,
> or retired here; no BACKLOG/`tasks/` row is edited; no register entry is added. Every "proposed disposition"
> below is INPUT for the 2026-08-26 ruled session, which must re-verify the cited evidence live before acting —
> the anchors below were live at 2026-07-28 HEAD (`eea2c1c7`) and rot from the moment this file is committed.

**Naming/home disposition (recorded, not silent):** the commissioning prompt suggested
`docs/audits/2026-08-26-drain-prep.md`. That name fails ADR-101 Rule B — no `<class>` token
(`scripts/validate_hermetization.py` `AUDIT_CLASS_ENUM`) — and would carry a future date on a present artifact.
The convention's dated-prep home is `docs/audits/` under the `technical` class with the artifact's own date
(precedent: `2026-07-11-technical-fleet-boundary-marker-design.md`, `2026-07-28-technical-437-closure-token-design.md`),
which this file follows.

---

## 1. Frame — the recorded full-pool intent, and what the flip changed

**Operator intent (2026-07-28), verbatim from `BACKLOG.md:316`:** "the FULL silent-rule pool (428 @ detector
`silent-rule-v4`) is to be dispositioned over time — drained, mechanized, or DELIBERATELY RETIRED as
no-longer-valid; staged, wholesale classes post-flip. **Nothing expires by being forgotten.**"

- Pool size: **428** normative-keyword occurrences across **56** files, `ecosystem/silent-rule-baseline.yaml`,
  detector `silent-rule-v4` (D4 semantics — a proxy occurrence count, not a rule census; census artifact
  `2026-07-27-census-silent-rule-ratchet-arm-measurement.md` §Amendment).
- The drain matrix (D1, `BACKLOG.md:314`): **slice × mechanism × owner × review date**. Disposition vocabulary
  used below: **drain now** (fix/declare the rule so it leaves `silent`) · **mechanize instead** (route to a
  named build ticket; interim declaration) · **deliberately retire** (record the rule expired/no-longer-valid,
  with reason).
- **The flip has happened since D1 was recorded.** ADR-107 was ratified and the strangler flip executed
  2026-07-28 (JOURNAL 2026-07-28 (f); [#439] closed on evidence `e53dee46` / `fa3f10a3`, JOURNAL (m)):
  `tasks/` is the source of truth, `BACKLOG.md` is generated. §4 below lists the wholesale classes this
  makes actionable — the "wholesale classes post-flip" clause of the intent is no longer future tense.

## 2. The five slice rows — evidence · proposed disposition · what 08-26 re-verifies

### [#356] — RULING-W + merge-delegation composite: legible, but no mechanism and no declaration

**Row (quoted, `tasks/356-*.md`):** "RULING-W and the merge-delegation composite are LEGIBLE but have neither a
mechanism nor a declaration — `8c913a6a` made both readable in PLAYBOOK/ESSENTIALS, closing the legibility gap
and *only* that gap. Each now needs one or the other: a mechanism, or a declared-unenforced entry with owner +
review date (closure criterion (b)). Also to record: the worktree side-effect rule exists only as [#353] … and
the merge-delegation composite only as JOURNAL narrative — two rules binding in force today with no ratified
decision record at all…" [P2][M], serialize-group `playbook`.

**Live state (2026-07-28):**
- Legibility spans present: RULING-W at `protocols/PLAYBOOK.md:1239` ("Hub→consumer writes — the only
  sanctioned shape (RULING-W…)"); the composite at `protocols/PLAYBOOK.md:1274` ("Consumer-leg merge delegation
  (the composite)") and `protocols/ESSENTIALS.md:84`; landed at merge `8c913a6a`.
- No declaration exists: `grep RULING-W|merge-delegation` over `ecosystem/disposition-register.yaml` and
  `.methodology.yaml` → zero hits. No mechanism exists: the W5 organ (HEAD-bound authorization token, R5)
  is unbuilt — [#344]/[#353] both open.
- No ratified decision record: RULING-W's record is ADR-36/41 *amendments* (exists); the worktree side-effect
  rule lives only in [#353]'s row text; the composite only in PLAYBOOK prose + JOURNAL narrative.

**Proposed disposition: DRAIN NOW** — two declared-unenforced entries (owner + review date, bound to the open
W5 tickets [#344]/[#353] per the ADR-81(d) leg of the declaration test, `BACKLOG.md:326-331`) + one compact
ratified decision record (ADR or ADR-amendment) covering the worktree side-effect rule and the composite.
**Why:** the mechanism is W5-class, L-sized and unbuilt; the declaration limb is exactly what closure criterion
(b) prices as the honest cheap path, and the two-rules-without-a-record defect is fixed by recording, not building.

**08-26 must re-verify:** PLAYBOOK:1239/:1274 + ESSENTIALS:84 spans still carry the rules · still zero
declaration entries · [#344]/[#353] still open (if W5 shipped meanwhile, the disposition flips to
mechanized-already) · no decision record landed since.

### [#358] — `parity-surfaces.yaml` misdescribes its own enforcement posture

**Row (quoted, `tasks/358-*.md`):** "header `:6` and `:93-94` still declare 'WARN-only v1, zero blocking gates'
/ 'the checker never blocks', and `scripts/fleet_parity.py:131` carries 'never blocks in v1', while
`scripts/audit.py:2425` makes it a BLOCKING `ALL_CHECKS` member and `ARCHITECTURE.md:192` agrees… Live
doc-vs-code contradiction, not a classification artifact. Routes to W2." [P2][S], serialize-group `architecture`.

**Live state (2026-07-28):** all three stale sites confirmed — `ecosystem/parity-surfaces.yaml:6-7`
("WARN-only v1, zero blocking gates") and `:94-95` ("the checker never blocks"), `scripts/fleet_parity.py:131`
("never blocks in v1"). The enforcement side confirmed at moved anchors: `check_fleet_parity` registered in
`ALL_CHECKS` at `scripts/audit.py:2986` ("[#337] blocking #328 fleet-parity gate"); `ARCHITECTURE.md:237`
("blocking `ALL_CHECKS` member since [#337] … fail-closed on a real divergence"). The row's own `:2425`/`:192`
anchors have rotted (audit.py churn) — substance intact, lines moved.

**Proposed disposition: DRAIN NOW** — a three-site text fix stating the post-#337 blocking posture (or a
recorded divergence-with-reason, the row's own alternative limb). **Why:** an actively misleading live
contradiction; the fix is S-sized prose; a self-description checker (mechanize) would be ceremony for a
one-time promotion drift.

**08-26 must re-verify:** the three sites unchanged (they may be fixed by a W2 arc before then — then close on
that evidence instead) · `audit.py` still lists `check_fleet_parity` in `ALL_CHECKS` (grep, don't trust `:2986`).

### [#359] — PHANTOM ENFORCEMENT: HANDOFF_PROCESS claims a mechanism that does not exist

**Row (quoted, `tasks/359-*.md`):** "…The FILE-BOUNDARY rule asserts the parallelism ruling was 'made
mechanical'; nothing implements it. `scripts/boundary_report.py` is a keyword false-friend — the #312 fleet
CLAUDE.md region reporter, self-declared 'a reporter, NOT a gate'… phantom enforcement is worse than a silent
rule… the four-state ledger has no cell for it. Routes to W6." [P1][M], serialize-group `handoff`.

**Live state (2026-07-28):** the claim moved but stands — `protocols/HANDOFF_PROCESS.md:523-524` ("This is the
parallelism ruling made mechanical — two concurrent epics MUST have disjoint boundaries") and `:734-735`
(same phrase in the §14a summary). No implementing mechanism found; `scripts/boundary_report.py:8-9` still
self-declares "reporter, NOT a gate … deliberately NOT registered in `audit.ALL_CHECKS`". The row's
`:517-518` anchor has rotted (spec churn) — substance intact.

**Proposed disposition: DRAIN NOW (the claim) + the ledger cell is the 08-26 ruling content** — correct
`:523-524`/`:734-735` to state what is true (a declared file/dir set, checked by discipline, not by a gate),
and have the operator rule how the four-state ledger records the phantom-enforcement class (the row's second
Done-when limb — that is a model decision only the operator can take). **Why:** building the FILE-BOUNDARY
gate is W5/[#344]-class work; the phantom *claim* is the immediate harm and is a prose fix. Mechanize-instead
remains open as the W5 follow-on; the claim fix must not wait for it.

**08-26 must re-verify:** the two HANDOFF_PROCESS sites (grep "made mechanical", not line numbers — they moved
once already) · `boundary_report.py` still not in `ALL_CHECKS` · whether HANDOFF_PROCESS v6 work ([#435] /
intake #18) already reworded the spans.

### [#360] — DEFINITION_OF_DONE scope-freeze expired in place

**Row (quoted, `tasks/360-*.md`):** "the `## Scope-freeze` clause froze the gate's doc set 'for 4 weeks from
ADR-85 (i.e. until ~2026-07-14)'; that window elapsed before the census HEAD (2026-07-19) with no successor
clause, so a clause that still reads as binding has silently lapsed. Routes to W6." [P3][S], serialize-group
`audit-py`.

**Live state (2026-07-28):** confirmed at `protocols/DEFINITION_OF_DONE.md:106-107` — the clause is verbatim
present and the window is now 14 days past its own expiry; no successor clause found in the file or PLAYBOOK.

**Proposed disposition: DELIBERATELY RETIRE — CONDITIONAL on the freeze's own data clause (terra P2,
adopted).** The freeze was not a bare timer: ADR-85 §Decision item 6 froze the gate's doc set to "gather
reliability/override-rate data first", and `DEFINITION_OF_DONE.md:107-109` still states that condition. Merely
reaching 2026-07-14 does not show the purpose was met. So the 08-26 act is two-step: **(1)** check whether the
data exists — the `/override` log (ADR-85's logged, HEAD-bound override records) and the gate's
firing/false-positive record over the window; **(2)** if the data was gathered and shows a stable gate, retire
the clause expired-with-reason citing it; if the data was never collected, RENEW with a new window **and** an
owner for the collection — retiring on an empty record would be exactly the "forgetting dressed as retiring"
failure this prep must not license. **Why retire remains the recommendation *if* step (1) passes:** an expired
clause that still reads as binding misleads; the stale-never-do-X class is real — but only the data, not the
date, earns it.

**08-26 must re-verify:** `DEFINITION_OF_DONE.md:106-109` unchanged (incl. the data clause) · the override-log
/ gate-reliability record for the freeze window · no successor freeze landed elsewhere · whether any doc was
added to the gate set since.

### [#361] — ADR-immutability's real coverage declared only in code

**Row (quoted, `tasks/361-*.md`):** "`protocols/AI_COUNCIL_PROCESS.md:350` and
`templates/claude-regions/critical-rules-records.md:3` assert ADRs, transcripts, handoffs and audits are all
immutable, but `scripts/hooks/block_immutable_edits.py:83` scopes the guard to `/docs/decisions/transcripts/`
only… a reader of either protocol cannot tell that three of the four classes are ungated. Routes to W6."
[P3][S], serialize-group `audit-py`.

**Live state (2026-07-28):** both declaration sites confirmed (the AI_COUNCIL anchor moved to `:343`
"Amendments not rewrites. ADRs are immutable"; `critical-rules-records.md:3` verbatim). Guard scope confirmed:
`block_immutable_edits.py:83` `_ZONE_SEGMENT = "/docs/decisions/transcripts/"`, with `:9-11` recording ADRs
deliberately out of v1 scope. **The gap has widened since filing:** the transcripts zone itself was DELETED
2026-07-23 (`b4435fad`, operator ruling 2026-07-22), so the guard currently matches **nothing** — ARMED
(no-op zone) per `ARCHITECTURE.md:214`. All four immutability classes are now prose-only.

**Proposed disposition: DRAIN NOW** — state the guard's real scope at the two protocol sites (the row's first
limb). Do **not** widen the guard: ADRs carry a sanctioned in-place amendment path (ADR-94 status line +
append-only amendment markers), so a naive widening would fight the repo's own lifecycle — the hook's
exclusion is by design, only its invisibility is the defect. **Why:** declaration-locus fix is S-sized prose;
widening is a design decision the row does not require.

**08-26 must re-verify:** the two protocol sites (grep the immutability sentences) · guard zone still
transcripts-only and still a no-op (ARCHITECTURE Ch2 row) · ADR-77 declaration `adr77-transcript-guard`
(`.methodology.yaml`, review 2026-10-25) still standing.

## 3. The drain-owed trio + the 43-line delta (also review-dated 2026-08-26)

`BACKLOG.md:318` records these as owed alongside the slice; the census artifact
(`2026-07-27-census-silent-rule-ratchet-arm-measurement.md` §Delta + §Amendment) is the evidence home. All
three re-verified live 2026-07-28:

- **`PLAYBOOK.md:1270`** — "**Never branch, commit, or merge under a live session.**" Still present (verbatim at
  `:1270`); still silent (`grep -l "live session" scripts/*.py` → zero hits). **Proposed: MECHANIZE INSTEAD** —
  its natural organ is the W5 session-guard family ([#344]/[#353]/#414's live-session checks); interim
  declared-unenforced entry bound to those open tickets satisfies both legs of the declaration test.
- **`REPO_ONBOARDING.md:92`** — "`marketplace add` **must** precede `install`." Still present; still silent.
  **Proposed: DRAIN NOW (declare)** — an install-order rule on a consumer's one-time onboarding flow is outside
  any hub hook's reach; a declared-unenforced entry with the onboarding runbook as owner is the honest state.
- **`REPO_ONBOARDING.md:199`** — "`.gitignore` floor negations **must use the contents form**." Still present;
  still silent (restated only in a generator docstring, `generate_floor.py`; no consumer `.gitignore` checker in
  `fleet_parity.py`). **Proposed: MECHANIZE INSTEAD** — a `fleet_parity` probe on the consumer `.gitignore`
  floor block is cheap and fits the existing probe grammar; declare interim, file the probe ticket at 08-26 if
  the operator adopts.
- **The 43-line net-new delta** (census §Delta itemization, files: REPO_ONBOARDING 14 · PLAYBOOK 13 ·
  AI_COUNCIL_PROCESS 9 · HANDOFF_PROCESS 6 · one PROBES.tmpl row) — unadjudicated candidates, not rules. The
  08-26 session should adjudicate them per the census's sampled method (mechanism lookup per rule subject),
  or explicitly carry them to the [#357] second census. Not proposed row-by-row here: adjudicating 43 candidates
  is [#357]-class judgment work, and this prep does not pre-empt it.

## 4. Wholesale classes now actionable post-flip (the intent's second stage, no longer future)

The flip (`tasks/` source of truth, generated `BACKLOG.md`, coherence gates armed and twice-fired — JOURNAL
2026-07-28 (f), RESIDUAL 2026-07-28 §4 precondition 2) converts entire classes of previously-silent
BACKLOG-mechanics rules into mechanized or obsolete ones. Candidates for wholesale (per-class) disposition at
08-26 — each still needs its per-rule check before the ledger moves:

1. **BACKLOG hand-editing / regeneration mechanics** (PLAYBOOK §10 grooming conventions and every "regenerate,
   never hand-edit" span): now enforced by `gen_task_tree.py --check` + the `task_tree_coherence` audit gate —
   witnessed firing twice in the 2026-07-28 window in two distinct modes (RESIDUAL §1). Class disposition:
   **mechanized** — the [E8] clause-(e) "witnessed, not installed" standard is already met.
2. **Done-items-leave lifecycle rules** (ADR-65 mechanics prose): now mechanized by `--write --prune`
   (marker-gated, `25c734f3`) + the `backlog-id-on-close` commit-msg gate. Class disposition: **mechanized**.
3. **Story-map schema rules** (ADR-66 shape prose): enforced by `validate_backlog` (pre-commit `validate-backlog`
   hook). Class disposition: **mechanized** — likely already counted `enforced` in the census; the wholesale act
   is confirming the class, not moving it.
4. **Single-file-BACKLOG assumptions** (any rule phrased against "the BACKLOG file" as the editing surface):
   candidates for **deliberately retire** — the surface they govern no longer exists as an editable object.
   Needs the per-rule sweep to enumerate; the detector corpus (protocols/ + templates/) is where they live.

**Boundary repeated:** classes 1–4 are *candidates with evidence*, not dispositions. Nothing moves in the
ledger until the 08-26 session rules, per rule or per class.

## 5. Contract check (this artifact)

- Zero drains / mechanizations / retirements executed — this file is the only output.
- Every claim carries a file:line, SHA, or a named grep re-derivable at review time.
- Anchor-rot honesty: [#358]'s `:2425`/`:192` and [#359]'s `:517-518` had already rotted by 2026-07-28;
  re-located by anchor text above. The 08-26 session should cite by anchor text, not by these line numbers.
