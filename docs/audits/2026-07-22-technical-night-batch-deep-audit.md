# Night-batch deep audit + repo cleanup — running log (2026-07-22 → 23 overnight)

<!-- scope: meta -->

> **Charter:** operator-pre-authorized NIGHT BATCH (operator away; no pauses between
> phases; safety = armed stops). Phases: 1 integrate+branch-hygiene · 2 archival audit
> (intake/ADR) · 3 transcripts + docs/archive disposition · 4 living-docs currency ·
> 5 ai-council read-only cross-repo audit · 6 next-session readiness. Forbidden:
> handoff bundles · new folders · immutable-record edits (amendment markers only) ·
> fleet machinery (#381 brake) · VISION re-stamp ([#368] stays honest) ·
> `automation/fleet-audit`.
>
> **Naming convention used (quoted from `scripts/validate_hermetization.py` Rule B,
> ADR-101 §2 + R3/R4):** *"an added `docs/audits/*.md` whose name fails
> `<YYYY-MM-DD>-<class>[-<slug>]` with `<class>` whole-token LONGEST-MATCH against the
> CLOSED 11-class enum […] and the R4 casing rule (all-lowercase kebab-case everywhere
> […]) -> BLOCK."* Class chosen from the closed enum: **`technical`**.
> Date-slug is the batch's start date 2026-07-22 (work ran into the small hours).

---

## Phase 0 — pre-batch baselines (armed-stop reference points)

- **Live-session scan (mutation gate):** transcript-cwd authoritative scan of
  `~/.claude/projects/C--Users-1028120-Documents-Dev--dev-knowledge/*.jsonl` +
  unfiltered `claude.exe` process scan. Second-newest transcript `7139e756…` (the
  runbooks-collapse session) last wrote 23:38; **oldest live claude.exe started
  23:39:28** → that session's process is gone (closed, not idle). All live processes
  belong to this batch session. **CLEAR** — mutations authorized.
- **pytest baseline (branch tree @ `9848a23b` = post-merge tree, see P1):**
  **1731 passed / 3 skipped / 0 failed** (`-n auto`, 429s).
- **`audit.py health` baseline: OK (0 FAIL).** Pre-existing WARN inventory (the
  net-new-WARN armed stop is measured against this set):
  1× `canonical_freshness` VISION.md 33d ([#368], stays honest) · 3× `no_ff_merges`
  legacy June spine commits (533109f2, 3a894eeb, d0f9ead6) · 1× `reconciled_versions`
  templates/CONTRIBUTING-md-template.md malformed · 4× `doc_rot` backlog-accretion
  (#344 #262 #332 #278) · 6× `undeclared_edges` handoff-process prose edges
  (BACKLOG, VISION, AI_COUNCIL_PROCESS, ESSENTIALS, PLAYBOOK, SESSION_SETUP).
- Fleet digest at boot: 2 issue(s) in 6 repos (`logs/FLEET-HEALTH.md`); 15 nightly
  triage findings + 102 closure proposals pending — **not** this batch's scope
  (operator triages).

## Phase 1 — INTEGRATE + BRANCH HYGIENE — **PASS**

- **Merge:** `docs/runbooks-collapse` @ `9848a23b` → main via `--no-ff` =
  **`e490275c`** (commit-msg gates passed; branch diff removed no BACKLOG task lines
  — repoints only, so no close-ids owed). Tree identical to the pytest-baselined
  branch tree (main `f1c9911d` was the branch's direct parent) → the P0 baseline
  doubles as post-merge test verification. Post-merge `audit.py health`: **OK**,
  WARN set unchanged.
- **Push:** `f1c9911d..e490275c` → origin/main (`block-ff-push` Passed).
- **Full branch inventory at batch start (local + remote):**

| Branch | Last commit | Merged into main? | Unique commits | Action |
|---|---|---|---|---|
| `docs/runbooks-collapse` | 2026-07-22 | after P1 merge, yes | 0 (post-merge) | **deleted** (`-d`) |
| `docs/handoff-dev-knowledge-architect-0721` | 2026-07-21 | yes | 0 | **deleted** (`-d`) |
| `docs/journal-integration-0721` | 2026-07-21 | yes | 0 | **deleted** (`-d`) |
| `automation/fleet-audit` | 2026-07-22 | **no** | **126** (nightly `chore(routine/fleet-audit)` baseline records; local ahead-28 of its origin) | **untouched** — operator ruling (leave it) |
| `origin/claude/conformance-2026-07-21` | 2026-07-21 | no | 1 (`52bc08bb` nightly conformance digest) | **kept** — unmerged deliverable awaiting operator triage |
| `origin/claude/conformance-2026-07-22` | 2026-07-22 | no | 1 (`30e0aa46` digest — 0 high / 3 med / 2 low) | **kept** — same |
| `origin/automation/fleet-audit` | 2026-07-16 | no | (behind local) | **untouched** — same ruling |

- **Worktree inventory: primary only** (`C:/Users/1028120/Documents/Dev/.dev-knowledge` @ main). End state = required end state. ✔
- No stashes touched; no remote deletions performed (nothing remote was both merged
  and outside the forbidden set).

## Phase 2a — INTAKE ARCHIVAL AUDIT — **PASS (terminal set EMPTY — nothing to move)**

Canonical lifecycle (docs/intake/README.md §5): `SEED → DRAFT → READY-FOR-TECHNICAL →
CONSUMED | REJECTED`; terminal docs (CONSUMED | REJECTED) relocate byte-identical to
`docs/intake/archive/` (operator ruling 2026-07-22). The hygiene lane (`f1c9911d`)
already archived the 3 CONSUMED docs; `docs/intake/archive/` currently holds exactly
those 3 (`2026-07-06-functional-architect-nightly-loop`, `2026-07-06-platform-feature-scan`,
`2026-07-07-test-suite-hygiene`).

**Verdict per live doc (15):** status quoted verbatim from frontmatter; last-touch =
last git commit date; refs = inbound references outside the generated index.

| # | Doc | `status:` (verbatim) | Last touch | Referenced by | Class |
|---|---|---|---|---|---|
| 4 | 2026-07-07-arc5-pilot-followup-seeds | `SEED` | 07-07 | JOURNAL, census brief, functional bundle | **LIVE** — canon SEED awaiting triage; §7 rent review due ~08-07 |
| 5 | 2026-07-07-changelog-review-seeds | `SEED` | 07-07 | JOURNAL, 3 audits | **LIVE** — same |
| 6 | 2026-07-08-func-new-project-bootstrap | `SEED` | 07-22 | BACKLOG | **LIVE** — same |
| 7 | 2026-07-08-func-ai-council-interface | `SEED` | 07-07 | JOURNAL, census brief | **LIVE** — same |
| 8 | 2026-07-08-func-night-routines-suite | `SEED` | 07-07 | 2 audits | **LIVE** — same |
| 9 | 2026-07-08-func-dashboards-local-html | `SEED` | 07-07 | BACKLOG, census brief | **LIVE** — same |
| 10 | 2026-07-11-tech-c4-visualization-memo | `input-for-deferred-work` | 07-11 | JOURNAL, 2 audits | **OFF-CANON** |
| 11 | 2026-07-11-tech-fleet-divergence-register | `superseded-pending` | 07-11 | JOURNAL, 3 audits | **OFF-CANON** |
| 12 | 2026-07-11-tech-ownership-manifest | `settled` | 07-12 | ADR-101, parity-surfaces.yaml, 6 audits, 3 intakes | **OFF-CANON** |
| 13 | 2026-07-11-tech-plan-of-record-fleet-hygiene | `plan-of-record-active` | 07-12 | JOURNAL, 3 audits, phase-a0 bundle, 2 intakes | **OFF-CANON** |
| 14 | 2026-07-12-siem-requirements-ruled-pack | `RULED` | 07-12 | JOURNAL, 2 audits, intake #14 drafts | **OFF-CANON** |
| 14 | 2026-07-13-siem-…-requirements-codex | `DRAFT` | 07-13 | JOURNAL, 3 audits, ruled pack | **EDGE CASE** (below) |
| 14 | 2026-07-13-siem-…-requirements | `DRAFT` | 07-13 | JOURNAL, 2 audits, ruled pack | **EDGE CASE** (below) |
| 15 | 2026-07-16-satellite-onboarding-prompts | `READY-TO-FIRE` | 07-16 | JOURNAL, BACKLOG, census brief | **OFF-CANON** |
| 16 | 2026-07-21-func-fleet-north-star | `DRAFT` | 07-21 | BACKLOG, census brief | **LIVE** — the plan spine; §4 feeds the [#381] polyrepo ruling, §1–3+5 feed the desired-state ADR |

- **TERMINAL set: EMPTY.** No live doc carries `CONSUMED` or `REJECTED`. Zero moves,
  zero index regen needed. (The archive convention was applied for the first time
  yesterday and is current.)
- **OFF-CANON STATUS — the six, named:** `input-for-deferred-work` (#10) ·
  `superseded-pending` (#11) · `settled` (#12) · `plan-of-record-active` (#13) ·
  `RULED` (#14 pack) · `READY-TO-FIRE` (#15). **NOT migrated** — [#398] owns the
  enum-reconcile-then-migrate (2026-07-19 ruling: not grandfathered; live enum is
  decided-not-deployed). Exactly matches the generated index's OTHER group of 6.
- **Named edge case (input for [#398]):** the two #14 DRAFTs carry populated
  `consumed-by:` (the RULED pack) while status stays `DRAFT` — schema says
  `consumed-by` populates only at CONSUMED. They are terminal-in-substance
  (provenance for the pack) but status-blocked from archival. Recommend: at the
  [#398] reconcile, either flip them to `CONSUMED` (consumer = intake #14 pack, not
  an ADR/epic — the enum may need a `CONSOLIDATED` value) and archive, or rule the
  provenance-retention pattern explicitly.

## Phase 3a — transcripts/ DISPOSITION — executed below (deletion commit follows)

**What it is:** `docs/decisions/transcripts/` (repo-root `transcripts/` does not
exist) — 51 files, 4.5 MB, + `archive/` subfolder (3 files, 264 KB). Contents:
council-out-* debate outputs + dated council research records, Mar–Jun 2026. The
producing pipeline (council-in-ADR output routing, ADR-43) is retired per the
operator ruling in this batch's charter: **DELETE — will never recur; pure
redundancy** (each debate's decision lives in its ADR; the raw 4-model transcript is
the redundant layer).

**Dependency check (armed-stop gate) — result: EMPTY, deletion cleared:**
- **pytest:** `tests/test_block_immutable_edits.py` decision-core tests inject a fake
  `exists`; the one wire test naming a real transcript uses the **Edit** tool, which
  blocks in-zone *without* an existence check (its comment goes stale, no assertion
  breaks); the Write-tool wire test uses a deliberately nonexistent `2099-…` path.
  `tests/test_scan_undeclared_edges.py` builds synthetic files under `tmp_path`.
- **Gates/generators:** no `audit.py` check enumerates the folder;
  `gen_audit_index`/`gen_intake_index`/`gen_claude_rosters` don't scan it;
  `generate_floor.py` uses the path only as a regex classification pattern;
  `scan_undeclared_edges.py` excludes the zone by path prefix (vacuous when empty).
- **Handoff probes:** zero transcript references in either 2026-07-21 bundle (the
  probe-bound set per `handoff_probes`).
- **Parity surfaces:** `ai-local-transcripts` (parity-surfaces.yaml:659) probes
  **ai-council's** repo-local `transcripts/`, not the hub's — unaffected.
- **Inbound prose refs:** many, but in **immutable records** (ADRs 34/43/77,
  JOURNAL, audits, handoffs — point-in-time, stay accurate as historical prose,
  docs/smoke precedent) or in **living docs** whose lines get the Phase 4 currency
  fix (CLAUDE.md L73, ARCHITECTURE L644/L665, PLAYBOOK taxonomy rows). VISION.md:112
  describes the ADR-43 fleet routing pattern — **left untouched** (VISION is
  forbidden this batch; flagged for the operator below). Editor-config sorting
  entries (`.code-workspace`, `.vscode/settings.json`) reference the dir cosmetically
  — harmless on a nonexistent dir; left (fleet-declared material).

**The ADR-77 guard (`scripts/hooks/block_immutable_edits.py`) — exact behavior when
the folder is gone:** the guard matches a *path pattern* (`_ZONE_SEGMENT =
"/docs/decisions/transcripts/"`), never enumerates the folder, and fails open
outside the zone. With the folder deleted it becomes **vacuously armed**: Edit/
MultiEdit attempts under the path still block (nothing exists to edit); Write of a
NEW file there is still ALLOWED (creation is the lifecycle — so the guard does NOT
prevent re-creation); every out-of-zone call is untouched. Nothing crashes, no gate
breaks, no test fails.

**End-state ruling (executed): KEEP ARMED for re-creation.** Retiring the guard is
the *eventually*-correct end state given "will never recur", but it is not a night
call: ADR-77 (Accepted) names this organ as the zone's enforcement — removing it
without an ADR-77 amendment manufactures doc-vs-state drift; [#112]'s queued
ADR-zone extension (Option A) builds on this guard; and removal of a `scripts/*.py`
module engages the `safe_removal` machinery. **Named re-rule candidate for the
operator:** amend ADR-77 (zone emptied by operator ruling 2026-07-22; organ retired
or re-scoped to the #112 ADR zone), then remove hook + registration + 18 tests +
ARCHITECTURE organ rows + CLAUDE.md §9 mention + doc-counts regen in one lockstep
commit. Until then the armed guard costs one no-op subprocess per Edit/Write call
and claims nothing false.

**Execution:** `git rm -r docs/decisions/transcripts/` on this branch (recoverable);
guard handling (= the keep-armed ruling + this record) in the same commit.

## Phase 3b — docs/archive/ DISPOSITION — report + proposal (non-destructive half only)

**What it actually is:** exactly what the record says — **not an archive.** Per
ADR-60 amendment 2026-05-27 it is the *pending-classification zone*: a triage queue
whose own README contract says items get promoted or deleted, and "if something sits
here across two reviews with no decision, default to deletion." First review:
2026-05-28 (7 transcripts promoted out). **No second review ever happened.** The 9
content files (+ README) have sat untouched since 2026-05-28/06-06 — ~8 weeks.

**Inventory + per-file second-review proposal (deletion decisions = operator's; none
executed):**

| File | Size | Refs that matter | Proposed disposition |
|---|---|---|---|
| 2026-06-05-agent-automation-external-research-note | 6K | ADR-72 cites it (immutable) | operator call: promote-to-audits or delete (one-shot value extracted into ADR-72) |
| 2026-06-03-dynamic-workflows-research-note | 17K | **PLAYBOOK.md:2372 live pointer** | KEEP until the PLAYBOOK pointer is re-homed, or promote to docs/audits |
| 2026-05-25-handoff-failures-evidence | 14K | ADR-55/56/57/58 + HANDOFF_PROCESS_v3.4 cite it | KEEP — the densest evidence node; promote-to-audits candidate |
| 2026-05-25-handoff-methodology-council-index | 8.5K | audits only (immutable) | delete candidate (provenance duplicated in the ADRs) |
| 2026-05-17-kimi-k2-scoping | 5.2K | old BACKLOG #243 mention | delete candidate (scoping superseded by model churn) |
| 2026-04-27-handoff-patterns-external-research | 71K | ADR-32 cites it (immutable) | delete candidate (largest file; value extracted into ADR-32) |
| 2026-04-24-multi-agent-debate-patterns | 24K | audits (immutable) | delete candidate |
| 2026-04-24-claude-md-best-practices | 31K | audits (immutable) | delete candidate |
| 2026-04-23-llm-dev-patterns-2026 | 14K | audits (immutable) | delete candidate |

**Proposed correct end state:** run the overdue second review (operator, ~15 min):
promote the 2–3 keepers to `docs/audits/` (they are evidence — audit-class by the
folder-line rule), delete the rest per the folder's own two-review contract, then
**empty-and-remove `docs/archive/`** and mark the ADR-60 pending-classification zone
retired by amendment marker (the folder's queue role is superseded by the
archive-inside-each-folder convention, operator ruling 2026-07-22). Non-destructive
half executed this batch: **this inventory + proposal** (the folder's own README
already documents the queue contract; adding an in-file note would churn a file
proposed for removal). No file touched.

## Phase 2b — ADR ARCHIVAL AUDIT — **PASS (terminal set EMPTY — nothing to move)**

77 live ADR files in `docs/decisions/` (ADR-27…ADR-103, incl. two amendment files);
`archive/` holds the 2 already-terminal ones the hygiene lane relocated (ADR-40
Deprecated 2026-05-23 · ADR-52 Superseded-by-ADR-53). Status lines quoted verbatim in
the retrieval record; every remaining ADR is `Accepted` except the five named below.
Inbound-ref counts are non-zero for every ADR (12–1181 hits), so the zero-live-refs
archival bar is met by **none** — and none is status-terminal anyway.

**Named candidates (report, not moved):**
- **ADR-45** — `Status: Explored, not adopted; ADR-42 v3.2 remains canonical authority…`
  Dead-in-substance (v4/v5 superseded the whole v3 line) but PLAYBOOK prose refs fail
  the zero-refs bar — exactly the shape the charter predicted. **Re-rule candidate:**
  either add a terminal status by amendment marker + re-home the PLAYBOOK refs, or
  ratify "explored-not-adopted stays in the live folder as a knowledge record."
- **ADR-82** — `Status: Proposed`, yet operator-ratified canonical 2026-06-11 (#149;
  CONTRIBUTING + ARCHITECTURE both state it). A stale status line, not a dead ADR —
  [#242]'s retro-normalize domain (ADR-94 sanctions the in-place flip at ratification;
  a 6-week-later retro-flip is #242's call, not a night drive-by).
- **ADR-88 / ADR-89** — frozen `Proposed` headers, ratified by in-file amendment
  markers (Pattern A). Known, tracked in [#242].
- **ADR-46 / ADR-47** — `Status: Partially superseded — retained as convention, NOT
  audit-enforced`: a hybrid status outside any enum; live by intent.
- **Enum drift (side-finding):** CONTRIBUTING "ADR process" prescribes
  `Accepted | Superseded | Withdrawn` — on-disk reality also uses `Proposed`,
  `Deprecated`, `Partially superseded`, `Explored, not adopted`. The ADR status enum
  needs the same reconcile-then-enforce treatment [#398] gives the intake enum.

## Phase 2c — SYSTEMIC FINDING: the archival system has no mechanism

The 2026-07-22 archive-inside-each-folder ruling is executed by hand and verified by
nothing. What a **status-coupled validator** would have to check (build input; sibling
of `validate_hermetization` in shape — read-only, WARN-first):
1. **Parse status per genre** — intake: frontmatter `status:`; ADR: the `Status` line
   (needs the per-genre CLOSED enum first — [#398] for intake, the CONTRIBUTING enum
   reconcile above for ADRs. The enum is the blocker; the validator is trivial after).
2. **Terminal-status ⇒ location coupling** — a terminal doc (CONSUMED/REJECTED,
   Superseded/Deprecated) still in the live folder → WARN; a live-status doc inside
   `archive/` → WARN (the inverse leak).
3. **Byte-identity on move** — the relocation is sanctioned only byte-identical
   (LESSONS-legacy precedent); validator compares git blob hashes across the move.
4. **Index coupling** — regen-and-diff the generated indexes after any move
   (`gen_intake_index` depth-1 already drops archived docs; decisions README rows
   need their annotation convention checked or generated).
5. **Ref-class-aware zero-refs bar for ADRs** — living-doc/protocol/script refs
   block archival; immutable-record refs (audits/handoffs/JOURNAL/transcript-history)
   do not. The validator needs that distinction or ADR-45-shaped files block forever.
6. **Status-transition legality** — forward-only lifecycle; `consumed-by:` populated
   ⇔ status CONSUMED (the intake #14 DRAFT-with-consumed-by edge would WARN today).

## Phase 4 — LIVING-DOCS CURRENCY — **PASS** (fixed: plain drift; reported: judgment)

**Fixed (commit `9a04e23c`; each with a genuine end-to-end re-read + same-day
`last_reviewed` re-stamp 2026-07-23):**
- `CLAUDE.md:73` — §4 transcripts destination claim → retirement record (v2.46, §12
  folded, prose count unchanged; lockstep with `b4435fad`).
- `ARCHITECTURE.md:644` — decision-flow transcript stage annotated (hub archive
  deleted); `:665` — Governing-ADRs transcripts location claim → deletion record.
  Organ rows :169/:571 stay TRUE (guard armed) — deliberately untouched.
- `CONTRIBUTING.md:114` — ruff row still claimed `language: system` (the v2.40
  pinned-rev conversion missed this file); `:115` — `logs/coherence-nudge.log` →
  `COHERENCE-NUDGE.log` ([#395] lockstep miss); `:113` — stale "~1.4s" audit-health
  timing dropped (witnessed ~3 min at the 41-check registry).
- `docs/decisions/README.md:5` — transcripts-subfolder claim → deletion record +
  archive/ role note.
- `BACKLOG.md` — checked #112/#210/#361 (transcripts-guard references): all remain
  TRUE (guard armed, zone pattern defined). No task premise falsified. LESSONS.md:
  append-only, entries point-in-time — nothing editable, nothing false as a standing
  rule. PLAYBOOK/ESSENTIALS: no `docs/runbooks` refs anywhere.
**Reported (judgment — operator):**
- **The ADR-43 / Council-routing doctrine cluster** — PLAYBOOK:950, 1052, 1858, 1907,
  2658, 2667, 2672–2673, 2696, 2832 + `protocols/AI_COUNCIL_PROCESS.md`:171, 313, 323
  + VISION.md:112 (untouchable this batch) all describe transcript routing into
  `docs/decisions/transcripts/`. The mechanism (ai-council `routing.py`) still exists;
  only the hub landing is gone. Retiring/re-scoping ADR-43 + the Council-process docs
  is ONE deliberate re-rule, not line-fixes — flagged as a named candidate.
- CONTRIBUTING ADR-status enum (Phase 2b side-finding above).
- VISION.md [#368]: 33d-stale WARN stands honest, untouched per charter.

## Phase 5 — ai-council CROSS-REPO AUDIT (READ-ONLY, zero writes) — **PASS**

- **Sync:** `main` == `origin/main` @ `8888d9e` (0 ahead / 0 behind). Working tree
  clean; no stashes; no linked worktrees; no MERGE_HEAD; hooksPath unset;
  pre-commit/commit-msg/pre-push all armed (fresh, pre-commit-managed).
- **Branches:** `chore/pre-handoff-cleanup` (checked out; == main's tip, 0 unique) ·
  `feat/vscode-boundary-colors` (fully merged via `c35bc3e`, 0 unique — routine
  post-merge stale local, deletable at that repo's next session; NOT deleted, zero
  writes). Nothing unmerged, nothing dangling.
- **Gates:** ruff clean. pytest (`-n auto`, no-cache, no-bytecode): **822 passed,
  2 FAILED, 1 xfailed** — both pre-existing, not batch-attributable:
  (1) `test_cli.py::test_no_persist_removes_scratch_on_success` — leaked scratch dir
  under xdist (possible parallel-collision artifact vs genuine `--no-persist`
  regression — unconfirmed which); (2) `test_integration.py::test_full_debate_pipeline`
  — `ImportError: _build_all_providers` absent from `ai_council.cli` (source/test
  drift). **Both belong on ai-council's backlog** (its repo, its tickets).
- **CLAUDE.md region map:** 23 regions (13 owner=repo, 10 owner=hub interleaved),
  full listing in the retrieval record. §9 prose roster == live
  `.pre-commit-config.yaml` exactly (12 hook ids) — no drift.
- **The ownership question:** the roster regions — `commands-repo-roster` (§7),
  `skills-repo-roster` (§8), `hooks-repo-roster` (§9), `recent-adrs-roster` (§11) —
  are all plain `owner=repo`, yet the hub mandates their existence + section shape;
  only the content is repo-specific. The two-state model has no cell for
  mandated-structure/local-content ([#370] names the adjacent third-class gap:
  user-level `~/.claude` lines). **Filed [#400]** (S22, kill-candidate #370 — one
  completeness ruling should absorb both cells). No other region flagged: §1-local /
  §6-local sub-region pattern (`first-read-local`, `session-start-protocol-local`)
  is the sanctioned escape hatch working as designed.

## Phase 6 — NEXT-SESSION READINESS (cold-architect orientation)

**Where the plan lives:** `docs/intake/2026-07-21-func-fleet-north-star.md` (intake
**#16**, DRAFT — the consolidated vision; §4 feeds the polyrepo ruling, §1–§3+§5 feed
the desired-state ADR) + BACKLOG theme **[E9]** (S24–S27 sequence, brake note at its
head). The intake #13 plan-of-record (v4) is the older fleet-hygiene baseline — still
OFF-CANON status, superseded in spirit by #16 but not formally; [#398] then a
supersession pass should settle it.
**Decisions state:** 77 live ADRs (…ADR-103), 2 archived (ADR-40, ADR-52). No further
terminal ADRs exist (Phase 2b). Stale-status trio: ADR-82 (Proposed-but-canonical),
ADR-88/89 (Pattern A) — [#242]. ADR-45 = the named re-rule candidate. ADR-43 +
Council-process docs = the post-transcripts-deletion re-rule cluster (Phase 4).
**Intake state:** 15 live docs — 6 SEED (canon, rent review due ~08-07) + #16 DRAFT
(the spine) + two #14 DRAFT-provenance edge cases; 6 OFF-CANON statuses blocked on
**[#398]** (reconcile-then-migrate). 3 archived (CONSUMED).
**Open-ticket map (gating):** **[#381]** polyrepo shape ruling — P1, NEEDS-RULING,
operator-only, its own session; **the #381 brake blocks all new fleet machinery**
([E9] S24–S27: #382 data-model, #383, #385 all `depends-on: 381`). Independent of the
brake: [#398] intake enum → unlocks the six migrations + the archival validator
(Phase 2c spec above); [#242] ADR status normalization; [#397] scripts/ structure;
[#399] v5 README.tmpl phantom claim; [#391] fleet_analytics nightly wiring; [#370] +
**[#400]** (this batch) — the ownership-model ruling pair; [#386] awaits operator
witness of PLAYBOOK §21; ai-council: 2 failing tests (Phase 5) to ticket in that repo.
**What this batch changed:** merged the runbooks-collapse lane (`e490275c`, pushed);
deleted 3 merged branches (worktrees/branches now: primary + `automation/fleet-audit`
only); **deleted `docs/decisions/transcripts/`** (`b4435fad` — 51 files; guard kept
armed); living-docs currency pass (`9a04e23c`); this artifact + [#400]. Intake/ADR
archival: **zero moves** — both terminal sets verified empty.
**The ONE next move:** the **[#381] polyrepo ruling session** — inputs: intake #16 §4
+ the 2026-07-21 read-only recon; the ADR must price (a) the unfold cost if the fold
is wrong, (b) the Blue Yonder employer-data compliance boundary (hard constraint),
(c) blast radius on live pre-sales work. Note [#388]: the "10–20 repo" figure is
fabricated — the live target is 5–8+, which *weakens* the dissolution case; price
against 5–8+. Everything in [E9] queues behind this ruling.

## FINAL — one-screen summary

```
NIGHT BATCH 2026-07-22→23 — per-phase verdicts
P1 integrate+branch-hygiene   PASS   merge e490275c pushed; 3 merged branches deleted;
                                     unmerged reported (fleet-audit 126c untouched,
                                     2 conformance remotes await triage); primary-only
P2a intake archival           PASS   terminal set EMPTY (0 moves); 6 SEED+#16 LIVE;
                                     six OFF-CANON named -> [#398]; #14 edge reported
P2b ADR archival              PASS   terminal set EMPTY (0 moves); ADR-45 re-rule
                                     candidate; ADR-82/88/89 status drift -> [#242]
P2c systemic finding          DONE   6-point status-coupled-validator spec (enum first)
P3a transcripts deletion      PASS   b4435fad — 51 files/47,748 lines (commit msg says
                                     54/4.8MB — exact figure is 51 tracked files);
                                     dependency check EMPTY; ADR-77 guard KEPT ARMED,
                                     retire-path = named re-rule candidate
P3b docs/archive              DONE   report-only: a stalled ADR-60 triage queue, second
                                     review overdue since ~06-06; per-file proposals
                                     recorded; deletions = operator
P4 living-docs currency       PASS   4 files fixed @ 9a04e23c (re-read + re-stamped);
                                     ADR-43 doctrine cluster + ADR-status enum +
                                     VISION:112 reported for judgment
P5 ai-council (read-only)     PASS   main==origin @ 8888d9e; gates: ruff clean, pytest
                                     822P/2F (both pre-existing, belong on ai-council
                                     backlog); 23 regions mapped; [#400] filed
P6 next-session readiness     DONE   this section; substitute for the (forbidden)
                                     handoff bundle
Armed stops triggered: NONE. Net-new pytest failures: 0 (hub 1731/3 before and after).
Net-new hub WARNs: 0 (verified against the P0 baseline set at close).
The ONE thing to look at first: P6 "The ONE next move" — the [#381] polyrepo ruling.
```

