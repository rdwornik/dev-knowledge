---
last_reviewed: 2026-09-08
reconciled_with: handoff-process@7.1.0
status: active
owner: Rob
---

# Architecture — `.dev-knowledge`
<!-- scope: meta -->

> Living document — the **navigation map** of the methodology system. It charts the
> layers, organs, and flows and **points** to the ADRs/protocols that hold the
> doctrine; it never restates doctrine text (resident-copy drift is the failure
> class this repo exists to kill). Fix the map when reality moves; fix the *source*
> when the doctrine moves.
>
> Last updated: `2026-09-08` — **batch CLOSE, lane `c2-living-docs-hygiene`: Ch2 gains the one-graph
> organ class, written in the FUTURE TENSE because none of it is built.** ADR-118 is `Proposed`, so
> the block adds **no organ row** (the Status legend keeps a RULED-UNBUILT organ out of the table,
> and this one is not even ruled) and **no Governing-ADRs bullet** (the same rule that correctly
> excluded ADR-116). What it records: FPG-1 exists and is wired to nothing; the graph/catalog/refusal
> triple is a plan; the scope is narrower than ADR-118's own text — **corpus-structure edges only**;
> and **state gates stay gates**, because a graph over tracked files cannot answer a question about a
> ref range or a staged index. The provenance of that narrowing is marked **relayed, not resolved
> against a source** — the review artifact is not in this tree. **Stamp semantics, stated:**
> `last_reviewed` moves because this pass re-read the file end-to-end from disk — Purpose, Codemap,
> all six chapters and Governing ADRs, 1,230 lines — and re-derived what it touched against live
> source: ADR-118's status line and Context, `scripts/file_purpose_graph.py`'s docstring and
> `EDGE_KINDS`, and the absence of `gen_catalog.py`. **Honest limits, three:** (1) it did not
> re-derive doctrinal correctness against the full text of every cited ADR — unchanged from every
> prior pass; (2) Ch6's *"currently 15 open, newest 2026-06-25"* Issues count stays unverified, this
> lane exercised no `gh` reach; (3) the Governing ADRs tail stays out of numeric order (cosmetic).
> Prior: `2026-09-01` — **[#614] lane-e-5: the pre-relocation review — this pass re-reads Purpose,
> Codemap, all six chapters and Governing ADRs end-to-end BEFORE the lane's own `VISION.md` → `docs/archive/VISION.md`
> move lands, per Done-contract item 3 (`LANE-e-5-vision-relocation.md`): the read happens here, the stamp is
> adjudicated at integration, not self-declared. **Checked against live source and confirmed accurate:** the
> Governing ADRs list correctly stops at **ADR-115** (Accepted 2026-08-25) and correctly excludes **ADR-116**
> (`docs/decisions/ADR-116-fuzzy-band-acceptance-shape.md:3`, Status: Proposed — not yet Accepted) — no gap;
> `ecosystem/organ-index.md`, `ecosystem/doc-counts.md`, `ecosystem/conformance.md` and `ecosystem/registry.md`
> all exist as cited; the Codemap block is untouched by this pass and stays guarded by `codemap-freshness`.
> **What this lane's NEXT commit changes, reviewed for here rather than after the fact:** the Ch5 file-lifecycle
> Living row and the two `[#614]`-era prose sites (Ch2 "Machinery retired" bullet; the ADR-114 Governing-ADR
> bullet) currently read `VISION.md` as "retained and still tracked" without saying WHERE — true today, false
> the moment the relocation commits, so this pass names the fix in advance: point at the hub's own relocation
> (`git mv` to `docs/archive/VISION.md`, executed by this lane) as ADR-114 option (C)'s sequenced nine-repo
> migration's step one, per `docs/audits/2026-09-01-technical-dc3-split.md` §4. **Drift this pass found beyond
> what it was sent to fix:** the ADR-114 Governing-ADR bullet still read `VISION.md` as `{hub: MUST, consumer:
> MUST}` on "the nine ADR-104 members" — both halves already stale before this lane touched anything.
> `ecosystem/parity-surfaces.yaml`'s `canonical-doc-vision` row demoted to `{hub: SHOULD, consumer: SHOULD}` on
> 2026-08-31 ([#614] lane-a), and the same row's own prose already corrected the count to **eight** of nine
> (`terminal-setup` never carried one) — this bullet had not been re-read since and still said nine/MUST. Fixed
> in the same commit as the relocation, alongside the newly-false claims, rather than left for a second pass.
> **Honest limits, unchanged from
> every prior pass:** it did not re-derive doctrinal correctness against the full text of every cited ADR; Ch6's
> *"currently 15 open, newest 2026-06-25"* Issues count stays unverified (no `gh` reach this lane); the Governing
> ADRs tail stays out of numeric order (cosmetic). **Adjudication note:** this record states what was checked;
> whether it discharges the A2 stamp for this pass is the integrator's call, not this lane's own. Prior:
> `2026-08-29` — **[#614] lane-b: ADR-114 is RULED, and the map's three README/VISION cells move in the commit that makes them false.** ADR-114 is **Accepted 2026-08-29** (AMENDMENT 1) — *"VISION.md is superseded by a recreated root README.md"* — so three cells are corrected here: the Governing-ADRs bullet flips from **PARKED** to the ruling and states, in the same breath, **what the ruling did NOT move** (`VISION.md` stays tracked and stays `{hub: MUST, consumer: MUST}` on the nine members; the ten `canonical_docs.py` constants still name it — measured: only **2 of the 8** children carry a root `README.md`, so a probe flip would red six); Ch5's file-lifecycle **Living** row gains `README.md` and `AGENTS.md` and marks `VISION` superseded-but-tracked; and the Ch2 *"Machinery retired"* sentence — which read *"root `README.md` deleted 2026-05-23"* as a bare fact — now records the recreation **and** the finding that **ADR-114's own decommission locator `ARCHITECTURE.md:366` does not exist** (`grep -n "recreate" ARCHITECTURE.md` → no match), so that decommission item was discharged by attrition before the ADR was ruled. **Drift this re-read found, unrelated to the lane's own acts:** the **ADR-115** bullet still named `[#577]` as the *owner of an unfixed* CLAUDE.md §10 anti-pattern; `[#577]` landed that fix (CLAUDE.md §12 v2.68) and §10 now carries the replacement bullet — corrected. **Stamp semantics, stated:** `last_reviewed` moves because this pass re-read the file **end-to-end from disk** (Purpose, Codemap, all six chapters, Governing ADRs) before editing, and re-derived each claim it touched against live source — the ADR-114 status line and AMENDMENT 1, the `canonical-doc-vision` row in `ecosystem/parity-surfaces.yaml` (found at `:164-174`, a **third** locator after the ADR's `:133-139` and the C5 census's `:140-150`), the consumer README presence count on the operator's disk, and CLAUDE.md §10 against `[#577]`. **Honest limits, three:** (1) it did not re-derive doctrinal correctness against the full text of every cited ADR — unchanged from every prior pass; (2) the Governing ADRs tail stays out of numeric order, and the ADR-114 bullet was rewritten in place rather than reflowed, so it is no better ordered than before; (3) Ch6's *"currently 15 open, newest 2026-06-25"* Issues count stays unverified — this lane exercised no `gh` reach. Prior: `2026-08-28` — **closure-harvest lane (K4 acts 1-3): three cells this lane's own acts falsified, corrected in the commit that falsified them.** `[#391]` is RULED — `fleet_analytics.py` stays a **manual reporter**; the Ch2 trigger cell said *"nightly wiring open #391"*, which the ruling makes false, and now records manual as the **ruled end state, not a gap**. The `routine_consumers` COVERAGE BOUNDARY read *"exactly one row at acceptance, [#348]"*; `[#348]` closed in this same lane and its ADR-105 declaration was re-anchored into `protocols/PLAYBOOK.md` §10, so the cell now carries **one at acceptance, two live** and — the part worth keeping — the limit that exposure revealed: a declaration that moves to its living home leaves this organ's scope entirely. **Drift this re-read found, unrelated to the lane's own acts:** the Governing ADRs list stopped at **ADR-113** while **ADR-115** (Accepted 2026-08-25) and **ADR-114** (PARKED 2026-08-22) were both decided; ADR-115 is load-bearing — it supersedes ADR-53 Decision 2, which makes `CLAUDE.md` §10's AGENTS.md anti-pattern false doctrine, and that bullet now says so and names `[#577]` as its owner. **Stamp semantics, stated:** `last_reviewed` moves because this pass re-read the file **end-to-end from disk** (Purpose, Codemap, all six chapters, Governing ADRs) before editing, and re-derived each claim it touched against live source — the `routine_consumers` marker count against a live `check_routine_consumers` run, the `fleet_analytics` invocation claim against a repo-wide grep that found the manual-CLI cell to be the only live assertion, and the ADR roster against `.claude/generated/recent-adrs.md`. **Honest limits, three:** (1) it did not re-derive doctrinal correctness against the full text of every cited ADR — unchanged from every prior pass; (2) the Governing ADRs tail stays out of numeric order, and ADR-114/115 were appended at the tail rather than reflowed, which makes it *more* out of order — cosmetic, and reflowing would bury this diff; (3) Ch6's *"currently 15 open, newest 2026-06-25"* Issues count stays unverified, this lane exercised no `gh` reach. Prior: `2026-08-27` — **[#597] per-check gate tiers: four Ch2 trigger cells and the
> §Validators seam are corrected by the change that falsified them, in the same commit.** `audit.py`
> retired `_GATE_MODE` for a tier declared per check, so `health` now runs only the commit tier —
> which makes four organ rows' *"`audit.py health` — pre-commit gate"* trigger claim false the moment
> it lands (`git_backlog_drift`, `doc_claims`, `doc_structure`, `fleet_parity`). All four are
> re-pointed, `fleet_parity`'s row records that **[#597] discharges the ship-gate-scoping follow-up
> this map had carried since [#337]**, and §Validators gains the mechanism paragraph plus the
> corrected seam sentence. **Stamp semantics, stated:** `last_reviewed` moves because this pass
> re-read the file **end-to-end from disk** (Purpose, Codemap, all six chapters, Governing ADRs)
> before editing, and mechanically re-derived every claim it touched against live source
> (`ALL_CHECKS` tier stamps, the measured per-check durations, `fleet_health.py`'s runner). **Honest
> limits, two, both narrower than prior passes' and both real:** (1) it did not re-derive doctrinal
> correctness against the full text of every cited ADR — unchanged from every prior pass; (2) the
> re-read found **one pre-existing imprecision it deliberately did NOT absorb**: the trigger cells
> reading *"+ SessionStart `fleet_health`"* describe a route that goes through `audit.py **run**`,
> not `health` (`fleet_health.py:900`), which was already loose before this lane and is not this
> lane's to relitigate — it is recorded here rather than silently smoothed, and the
> `git_backlog_drift` cell now names the actual command. **Found and NOT fixed, unchanged:** the
> Governing ADRs tail stays out of numeric order; Ch6's *"currently 15 open, newest 2026-06-25"*
> Issues count stays unverified (this lane exercised no `gh` reach). Prior: `2026-08-23` — **governance-drift discharge (lane `lane-docs-governance`): the
> 2026-08-21 CLOUD-R1 audit's ARCHITECTURE findings are executed, and the end-to-end re-read found
> three more the audit missed.** Landed in two commits — the SAFE-MECHANICAL set, then the three
> architect-ruled items. **Ruled items (R1 top-10 8 and 9):** Ch2's *"every enforcement/awareness
> organ"* **completeness claim is retired** in favour of the pointer its own note already licensed —
> the hand table carried **35 rows** against a generated index of **eight classes**, omitting the
> `agent`, `rule` and `plugin` classes whole — while **keeping the failure-posture column**, which
> `ecosystem/organ-index.md` states in its own header that it cannot carry; and the map finally
> points at **PLAYBOOK Ch8 "Session boundaries"** for the repo's dominant working mode (parallel
> worktree lanes, dispatch, the ADR-110 batch protocol), which it referenced **nowhere** despite a
> JOURNAL that is overwhelmingly lane work. **Ch4 gains an execution-substrates block** —
> `.devcontainer/` and `deploy/lived_sandbox/` — deliberately NOT a sixth channel row: nothing is
> *carried* through either, they are *venues*, and they are what makes Ch4's existing "inert by
> design in a fresh clone" bullet concrete. **From R1's verdict
> table: **A2** the "read-only validators" claim re-scoped (Purpose + §Validators) — the prohibition
> is on driving a CHILD repo's state, which is invariant 2's already-checkable form; **A3** the Ch2
> pre-commit id enumeration **retired in favour of the pointer the sentence already carried** —
> R1's *second* written option, taken because its first (add `block-commit-on-main`) would have
> landed eighteen-of-a-live-**twenty-one**, a fourth recurrence of the defect that sentence's own
> parenthetical already records three times; `block-commit-on-main` is instead named where it is
> load-bearing, in the `always_run` paragraph below it; **A5/A6** two locator repairs
> (`fleet_health.py:82`→`:156`; `validate_doc_claims.py:225-236`→**`:224-239`** — R1's own proposed
> `:224-240` was itself off by one against live source, which is M1 catching M1); **A7** the ADR-86
> §3 Ch2 pointer to `ecosystem/conformance.md`. **Drift this re-read found that R1 did not, and
> fixed here:** (1) the Enforcement-model bullet and (2) the `audit.py` §Validators bullet each
> carried the *same* "read-only" falsity — sites **six and seven** of the `[#558]` claim, in a file
> R1 reported as holding two; and (3) Ch5's file-lifecycle table still listed `BACKLOG` as **Living /
> update in place**, contradicting Ch5's own source-zone prose twenty lines below and falsifying
> R1's *"CLAUDE.md is the only one of the three"*. That triple is **M3's lesson landing on M3's own
> audit: a sweep scoped to the sites a prior sweep named will keep reporting zero.** **Found and NOT
> fixed, with reasons:** the Governing ADRs tail stays out of numeric order (cosmetic; reflowing
> would bury this diff); Ch6's *"currently 15 open, newest 2026-06-25"* Issues count (R1 **A17**)
> stays unverified — this lane exercised no `gh` reach, and restating it at a guessed value is the
> very failure it already is; **`[#171]` is NOT closed** — its Done-when's "generated + *committed*
> by a read-only validator" leg is unimplemented (the Ch2 dashboard note states it). **Stamp
> semantics, stated:** this pass re-read the file **end-to-end from disk, all six chapters plus
> Governing ADRs**, and mechanically re-derived every claim it touched against live source
> (`.pre-commit-config.yaml` ids, `_CLAIMS` bounds, the `fleet_health` throttle line,
> `gen_dashboard`'s write path). **Honest limit, unchanged from prior passes:** it did not re-derive
> doctrinal correctness against the full text of every cited ADR. Prior: `2026-08-22` — **A3 ruled: Ch3 declares the L0 boundary, and the re-read closed two
> drifts it found.** Ch3's automation axes gain the ruled declaration that the routing table
> (`~/.claude/ROUTING.md`), the reviewer pin and the Codex config are **L0 surfaces, out of this
> repo's universalization scope** — architect ruling 2026-08-22 over the cloud-wave funnel table
> (line A3), taken because *silence is not a boundary*: an absent table reads as a gap rather than a
> placement. The declaration names `[#82]`'s inherited limit explicitly so it is not discovered at
> closure. **Drift found by this re-read and fixed here:** (1) the Governing ADRs list did not carry
> **ADR-113** (Accepted 2026-08-19) — load-bearing for this very edit, since it is the ruling that
> separates the three "L" namespaces the new paragraph depends on; (2) Ch3's model-routing
> parenthetical named `Opus 4.8` as the inherited main-session model while sessions run Opus 5 — it
> is now **repointed at the live session rather than restating a value**, the same fix this file
> applied to its counts in the 2026-08-10 pass, because restating a volatile value is what put it on
> the wrong side of its own stamp. **Drift found and NOT fixed:** the Governing ADRs tail is out of
> numeric order (110, 111, 109, 112, 113) — cosmetic, left rather than reflowed to keep this diff
> reviewable. **Stamp semantics, stated:** `last_reviewed` moves because this pass re-read the file
> **end-to-end from disk, all six chapters plus Governing ADRs**, and mechanically checked the ADR
> roster against `.claude/generated/recent-adrs.md`. **Honest limit, unchanged from prior passes:**
> it did not re-derive doctrinal correctness against the full text of every cited ADR. Prior:
> `2026-08-14` — **packet-close drift repair: the flagged ADR-112 gap is closed.**
> The Governing ADRs list gains its ADR-112 bullet (Two-tier adoption bar, Accepted 2026-08-12) —
> exactly the gap the immediately-prior pass below flagged and explicitly left unfixed. Pure
> drift-repair, not a fresh re-read: `last_reviewed` stays `2026-08-14` (already stamped by that
> pass), unchanged here. Prior: `2026-08-14` — **[#525] the owed load-gauge organ rows land.** Ch2's organ map
> gains a row for the `[load]` operator-load gauge — `collect_load`/`load_line`/`append_load_row`
> (`scripts/fleet_health.py:610,642,689`), the `[#270]` sub-organ of `fleet_health.py`'s
> SessionStart trigger that neither table named since it shipped (owed since W2 per
> `docs/audits/2026-08-12-technical-roadmap-north-star-frozen.md:30`); Ch6's verification-mesh
> "Nightly (local)" row now names the gauge as a dimension alongside structural/freshness-stamp
> health, with the same two locators. **Drift found by this re-read, out of scope to fix (Ch2/Ch6
> only per this lane's contract):** the Governing ADRs list still stops at ADR-111/ADR-109 and
> does not carry **ADR-112** (Accepted 2026-08-12, per `.claude/generated/recent-adrs.md`) —
> flagged for the next pass that touches that section. **Stamp semantics, stated:** `last_reviewed`
> is re-stamped because this pass re-read the file end-to-end from disk (all six chapters); the
> only correction it was licensed to make is the two rows above. **Honest limit:** it did not
> re-derive doctrinal correctness against the full text of every cited ADR, and it did not fix the
> ADR-112 gap it found. Prior: `2026-08-12` — **pre-handoff closing arc: the organ index relocates, and two
> defects this re-read found are fixed.** Ch2's map note and §Validators now name
> `ecosystem/organ-index.md` (moved from `docs/ORGAN-INDEX.md` by operator ruling A of
> 2026-08-11; register `protocols/STANDING_RULINGS.md` K-1), and the Ch2 note is no longer
> stale on its own terms — it read *"will become its verified source once it ships"* about an
> index that shipped 2026-08-11. **Drift caught by this re-read, unrelated to the relocation:**
> (1) the §Validators `validate_hermetization` entry described Rule A + Rule B only, and now
> carries **Rule C** (the home allowlist landed in this same arc); (2) the pre-commit gate list
> was missing `organ-index-freshness` — seventeen of eighteen against the live count in
> `ecosystem/doc-counts.md` — which is the *second* time that list has silently trailed the
> config by one, so the parenthetical now records both misses rather than only the first;
> (3) the governing-ADR roster stopped at **ADR-109** while **ADR-110** and **ADR-111** were
> Accepted, and both are live doctrine this window leaned on. **Stamp semantics, stated:**
> `last_reviewed` is re-stamped because this pass re-read the file end-to-end from disk and
> mechanically checked the claims it could (gate count vs `doc-counts.md`, ADR statuses vs
> `.claude/generated/recent-adrs.md`, every `ORGAN-INDEX` reference vs the tree). **Honest
> limit, unchanged:** it did not re-derive doctrinal correctness against the full text of every
> cited ADR. Prior: `2026-08-10` — **claims-correction pass: 16 checkably-false claims fixed** (the
> 12 named in `docs/audits/2026-08-10-verification-fable-adversarial-plan-review.md` §Mandate 2,
> plus 4 the follow-up sweep found beyond that report's count of 14 — `logs/PARITY-EVENTS.jsonl`
> casing, the corp pre-commit-channel row, #195-as-pending, and the dead `#85` pointer). Where a
> claim was a volatile cardinality it is **re-pointed at the surface that computes it** rather
> than re-stated at today's value (carrier roster → the manifest `carriers:` block; gate count →
> `ecosystem/doc-counts.md`; doc→code rules → `coverage_scope`; check registry →
> `audit.py checks`; conformance branches → `git branch -r`) — restating the number is what put
> ≥3 of these claims on the wrong side of their own review stamp. **Stamp semantics, stated:**
> `last_reviewed` is re-stamped because this pass did re-read the file end-to-end from disk and
> mechanically verified its checkable claims (paths, cardinalities, rosters, ref/branch
> existence, BACKLOG id liveness, tool behaviour vs code). **Honest limit:** it did *not*
> re-derive doctrinal correctness against the full text of every cited ADR — a claim that
> faithfully restates an ADR whose own content has drifted would survive this pass. Prior:
> `2026-08-07` — **[#501] closed; two Ch2 status cells corrected.** The
> `report-only-wall.yml` row loses `ARMED (never fired)`: run `31161874468` (event `push`) fired
> it on this morning's own push and discharged BOTH owed conditions at once — the anchor leg ran
> a real push range for the first time, and two legs recorded exit 1 while the job stayed green,
> which is exactly the "green with the red recorded" proof the cell demanded. **Drift caught by
> this re-read, unrelated to that:** the `session_end_backpressure.py` row still claimed
> `hard-block on detected non-compliance`, a posture the ADR-85 amendment 2026-08-03 §A5 retired
> — the hook is **advisory in full** and the script's own docstring (`:14`) says it "no longer has
> a HARD leg". CLAUDE.md §9 had been correct since 2026-08-03; this map had not. Prior:
> `2026-08-06` — **batch-1 integration (ADR-110), integrator-owned edits from
> three parallel lanes.** Ch2 gains the **server** Layer value and the **report-only** failure
> posture (a posture that *cannot* be hardened — the repo is private on the Free tier, where
> required checks do not exist), plus the `report-only-wall.yml` organ row, `ARMED (never
> fired)`; Ch6's mesh gains the **Post-merge (server)** layer. Ch3's `block_ff_push.py` entry
> flips from the retired `fail-soft to exit 0` claim to **fails CLOSED (exit 2)** ([#504],
> ADR-85 amendment §A6). Ch6 records that `.github/` **returned** for a different organ on a
> fixed trigger — [#255]'s judgement is corrected in its trigger, not reversed, and Stage 2 of
> the nightly loop stays DEAD. **Two cross-lane reconciliations the batch itself forced:** Ch6's
> "CONTRIBUTING still describes the Action in the present tense" warning is retired ([#503]
> fixed it in this same batch), and CONTRIBUTING's converse `.github/ no longer exists` claim
> is corrected against [#501]. Prior: `2026-08-02` — [#475]: the Ch2 pre-commit gate list + Validators gain
> `check-seal-identity` (commit-time handoff-bundle seal-identity, reusing
> `gen_handoff.verify_seal_identity`); [#474]: the Ch5 source-zone `--write` sentence flips
> from warn-then-rewrite to refuse-unless-`--force`. Prior: `2026-08-01` — [#459]: Ch2 gains the **desired-state organ class**
> (ADR-109 contract/loader/report) and the codemap source-root question is RULED —
> `ecosystem/schema/` stays out of scope, cost stated. Prior: `2026-07-28` — ADR-107 strangler **step 3** ([#439]): Ch5's `tasks/` zone flips
> from **derived** to **SOURCE OF TRUTH**, with `BACKLOG.md` now generated from it
> (`--emit-source`), `--prune` refused under retire-not-delete, and the frontmatter-honesty leg
> recorded. The same edit retires that block's "honest enforcement limit" note, which had gone
> stale: `--check` stopped being an unwired mode when [#433] C1 armed it as an ALL_CHECKS
> ship-gate leg — and arming it was ADR-107 §7.2's precondition for this very flip. Prior:
> `2026-07-27` — window-close currency lane (bounded, not an audit): governing-ADR
> roster through **106** (uv / environment isolation) and the Purpose ratification line with it;
> Ch5 gained the `tasks/` zone ([#433]); the Ch2 `/ship` row records that **merge is atomic**
> (merge → push → delete source branch). Deliberately NOT added *that day*: `silent_rule_ratchet`
> ([#436], ruled-unbuilt at the time) — this chapter's own Status legend keeps a RULED-UNBUILT
> organ *out* of the table until it is built. **That exclusion is spent: the check has since been
> built** and is a blocking `ALL_CHECKS` member (`scripts/audit.py::check_silent_rule_ratchet`);
> the live check registry is `python scripts/audit.py checks`, which is what §Validators points
> at rather than a roster restated here. Prior: `2026-07-26` micro-window currency lane (intake #17 §5): governing-ADR
> roster through **105**; the fleet count repointed at the surface that computes it; the
> organ map gained a **Status** column; Ch6's nightly loop marked **broken at the triage
> edge**; the paid ADR-92 amendment recorded. Prior: `2026-07-23` currency lane (carrier
> count 4→5, registered child set, roster through 102/103). Structure: the `2026-06-07` six-chapter
> rewrite (layers · organs · automation axes · distribution · zones · verification
> mesh, closes [#91]), superseded the pre-ADR-80 layout. Prior history:
> `git log --follow ARCHITECTURE.md`.
>
> **How to read this doc (progressive disclosure).**
> - A **Claude Code session** wants the floor first: **Ch1** (where you sit, what you
>   may touch) → **Ch2** (which organ fires when) → **Ch5** (what is frozen). That
>   trio is the minimum grounding before edits.
> - An **audit / conformance run** enters at **Ch6** (the verification mesh +
>   decision flow) and uses **Ch2** as the organ checklist.
> - The **operator** scans **Ch3** (what runs unattended, on what posture) and
>   **Ch4** (what is distributed where, what is still hub-only).
> - **Deep dives leave this map** — every section points to its ADR/protocol. Read
>   the source, not a copy here.
> - **The daily working mode is NOT in this map.** Parallel worktree lanes, lane dispatch, the
>   ADR-110 batch protocol and session boundaries live in **`protocols/PLAYBOOK.md` Ch8
>   "Session boundaries"** — the single deep-dive this file had never pointed at, though the
>   JOURNAL is overwhelmingly `worktree-lane-*` / `batch-N` work. Ch2 rows the organs that
>   police it (`stale_worktrees`, `no_sibling_orphans`, `/lane-boot`, `/lane-integrate`);
>   **Ch8 holds the procedure**, and ADR-110 the contract.

## Purpose [CORE]

`.dev-knowledge` is the universal LLM-driven development guide and methodology
framework for all `Dev/` projects. It is **Layer 2** of the ADR-28 three-layer
ecosystem model — passive storage and governance authority, not an execution
engine. It holds operational protocols, ADRs, intake docs, handoffs, templates, and
hub-local validators, generators and gates; it prescribes conventions that child repos
must follow. **What Layer 2 may not do is drive a CHILD repo's state** — the prohibition is
on siblings, not on this repo's own tree (invariant 2 below is the checkable form). **A fleet count
is meaningless without its surface — three nest, and each is authoritative for its own
question** (machine-registered ⊂ human-registered ⊂ all git repos):

| Denominator | Authoritative surface | Answers |
|---|---|---|
| machine-registered | `ecosystem/index.yaml` — **derived** from `ecosystem/<repo>/state.yaml` presence, regenerated wholesale by `audit.py registry update`; **never hand-edit it** | which repos the audit machinery walks |
| human-registered | `ecosystem/registry.md` — hand-maintained; add a row when a repo joins `Dev/` | which repos the operator tracks at all |
| all git repos | **ADR-104** | the fleet's shape as ruled |

`onboarded` is a **separate axis, not a fourth denominator** — it is `registry.md`'s Status
column, backed by `ecosystem/deployed-versions.yaml`, and a machine-registered repo may still
be unonboarded. Read a count off the surface that defines it; do not restate one here. It is
consulted as context by
Claude Code, Codex, Cursor, and other agents. **Nothing here executes orchestration**
— everything is read, consulted, or passively validated. The six chapters below are
the system as built; the decisions that ratified it are curated in **Governing ADRs**
below against the complete ledger `docs/decisions/README.md`. A bare "ratified through
ADR-NN" horizon is not stated here — it rots at the next accepted ADR and did (this line
read "through ADR-109" while ADR-110 had been Accepted since 2026-08-06).

---

## Codemap [CORE]

The canonical *code*-structure artifact — "what code exists and how does it relate?"
Auto-generated by `python -m scripts.codemap.cli generate . --source-root scripts
--write` (ADR-51 amendment 2026-05-22; compact-text form per ADR-51 amendment
2026-07-05 — canonical docs are LLM-first, Mermaid left them); **do not hand-edit**.
Two modules (`scripts/codemap/` and `scripts/toc/` both qualify as Python packages).
The behavioural *organ* map — what fires when — is Ch2, not here.

<!-- CODEMAP:START -->
Modules (source root: `scripts/`; layer from tach.toml, `-` = unassigned):

| module | layer | path | flags |
|---|---|---|---|
| codemap | - | scripts/codemap/ | orphan |
| toc | - | scripts/toc/ | orphan |

Dependencies (`from -> to`; `[cycle]` marks an edge on an import cycle):
- (none)
<!-- generated by codemap tool; do not edit by hand -->
<!-- CODEMAP:END -->

---

## Layer Boundaries & Invariants [CORE]

**Chapter 1 — Layers & authority.** `.dev-knowledge` is **Layer 2** of the ADR-28
ecosystem three-layer model. The model
is a closed loop across three actors — the browser-chat **architect**, the
**operator** (Rob), and the Claude Code **executor**:

Actors (role in the loop):
- **L1 — browser chat**: architect — analysis & design
- **Operator (Rob)**: consent gate — consent · ratification · scope
- **L3 — Claude Code**: executor — Layer 3 work
- **L2 — `.dev-knowledge`**: passive storage & governance

The loop, edge by edge (`from -> to: what flows`):
- L1 architect -> Operator: prompt / handoff (operator pastes = consent)
- Operator -> L3 executor: ratified prompt
- L3 -> L2: handoff -> git commit
- L2 -> L3: read / pull as context
- L2 -> L3: prescribes (read-only — prescription, not execution)
- L3 -> L1: reflection -> new browser chat

**Authority chain.** The architect proposes; the **operator is the consent gate**
(the architect never executes — the operator pasting a prompt into Claude Code *is*
the act of consent; ESSENTIALS "Architect → operator channel-discipline"); the
executor acts only inside the ratified scope. **Ratification bandwidth is the scarce
resource** the whole system economizes — every protocol that compresses context
(handoff bundles, the methodology floor, valves) exists to spend less of it.

**Invariants** (binding; → ADR-28, ADR-36, ADR-39, ADR-41):
1. **Layer 2 never executes.** No script here orchestrates actions in, or drives
   state changes in, another repo.
2. **Validators are read-only on siblings.** `scripts/` only reads, checks, reports;
   the cross-repo `audit.py run` reads each sibling read-only and writes **only**
   into `.dev-knowledge` (ADR-36, ADR-69).
3. **Prescriptive authority.** PLAYBOOK + ADRs bind child repos; children may not
   locally override them (ADR-31; see Authority below).
4. **Append-only files are never edited** — `LESSONS.md`, `logs/TOKEN-LOG.md`
   accept only appends (ADR-29, ADR-39). *LESSONS.md-only exception (ADR-29 amend.
   2026-07-17):* a contiguous older block MAY relocate **byte-identical** into a dated
   `LESSONS-legacy-<span>.md` (chronological archival; edits/deletes still forbidden;
   `logs/TOKEN-LOG.md` stays strict).
5. **Dated artifacts are immutable** — ADRs, transcripts, handoffs, audits are
   superseded by a new file or in-file marker, never edited in place (Ch5).

| Ecosystem layer | This repo's role |
|---|---|
| Layer 1 — browser chat (architect) | external — analysis & design |
| **Layer 2 — `.dev-knowledge`** | **this repo** — passive storage, governance, prescription |
| Layer 3 — projects (executor) | external — the child repos; membership is **not enumerated here** (Purpose names the three denominators and their surfaces: `ecosystem/index.yaml` machine-registered · `ecosystem/registry.md` human-registered · ADR-104 all git repos) |

---

## Authority and governance [CORE]

Per **ADR-31**, `.dev-knowledge` is the **binding source of cross-repo prescriptions**
(Authority model 1B — *prescriptive with conformance audit*). The operator is the
ratification authority; the hub is the prescription authority; enforcement is
out-of-band and read-only.

- **Ratification, not adjudication.** On technical proposals the operator rules on
  *constraints, priority, scope* — not technical correctness; cross-repo review
  authority is asymmetric (ADR-63). The architect surfaces trade-offs; the operator
  picks (ESSENTIALS "Architect routing for technical proposals").
- **Enforcement model.** Centralized `scripts/audit.py` — read-only **on siblings** (self-audit
  `health` + cross-repo `run`; live registry via `python scripts/audit.py checks`).
  The cross-repo `run` is **manual, no downstream commit-gating**; the self-audit
  `health` runs as a **local pre-commit gate** here (Ch2 / ADR-31, ADR-36, ADR-69).
- **Tier system retired** 2026-05-23 — repos declare no `tier:`/`scale:`; the
  universal governance baseline (ADR-38 A5) applies to every repo regardless of
  size. `ARCHITECTURE.md` is mandatory for every repo (ADR-51, amended 2026-05-23).
- **Baseline rule (ADR-31):** the audit runs green on first invocation; no known
  violations remain open.

→ Full authority doctrine: ADR-31, ADR-36, ADR-63. Codex reviewer config is a global
standard (`~/.codex/AGENTS.md`, canonical source `deploy/global-instructions-codex.md`; ADR-54).

---

## Organ map

**Chapter 2 — Organ map.** A **curated** behavioural map: what fires an organ, the layer it
lives in, and — the column nothing else carries — **how it fails**. It is deliberately NOT
the inventory; `ecosystem/organ-index.md` is (see below).

> **Map, not prose.** This table is hand-maintained. The generated
> `ecosystem/organ-index.md` (**#132**) **is** its **verified source** — it shipped
> 2026-08-11 (`83a869e6`, merge `e624a172`) and is guarded by the
> `organ-index-freshness` pre-commit gate; this section is reconciled with it and may be
> replaced by a pointer to it. When they disagree, trust the index. The index moved from
> `docs/ORGAN-INDEX.md` to `ecosystem/organ-index.md` on 2026-08-12 by operator ruling A
> of 2026-08-11 (register `protocols/STANDING_RULINGS.md` K-1): it is generated ecosystem
> state, not a `docs/<genre>/` artifact.

> **Conformance dashboard → `ecosystem/conformance.md`** (+ its HTML sibling
> `ecosystem/conformance.html`, operator addendum 2026-08-19), generated by
> `scripts/gen_dashboard.py`. This is the **claims-vs-state** surface — where the ADR-85 R2 /
> [#169] ungated-doc staleness signal lands, and where anti-orphan violations, the ADR ledger
> and the commit-tax figures are rendered. The organ index above answers *what exists and what
> fires it*; this table answers *what happens when it says no*; the dashboard answers *does the
> repo currently match what it claims about itself*. Required by **ADR-86 §3** (the G7
> coverage-matrix gap), which specifies the pointer "lands with the build, not before" — the
> build shipped, so it lands here. **Honest limits, both live as of 2026-08-23:** the dashboard
> is HEAD-pinned and regenerates only on demand — nothing gates it (`--check` exists in
> `gen_dashboard.py` and is armed nowhere, the lone ungated committed-generated surface in this
> repo) — and the generator **does not commit its own output** despite both artifact faces
> claiming it does (`write_outputs` writes two files and returns; the sole subprocess is a
> read-only `GitReader`). Those two are R3 findings F5 and F3 and are why **[#171] is not
> closed by this pointer**: its Done-when also requires "generated + *committed* by a read-only
> validator", which no code path performs.

**This table does not claim completeness, and the claim it used to make was false.** It read
*"Every enforcement/awareness organ, with its trigger…"* while carrying **35 rows** against the
generated index's **eight classes** — omitting the `agent`, `rule` and `plugin` classes whole.
The note above already licensed the fix (*"may be replaced by a pointer to it"*), so: **for
*what exists and what fires it*, read `ecosystem/organ-index.md`** — it is generated from the
organ sources, gated by `organ-index-freshness`, and cannot silently trail them the way a hand
table does. Do not read a count off this table, and do not restate the index's count here.

What this table keeps is the column the index **states it cannot carry**: **failure posture**
(fail-closed = blocks the action; propose-only = writes a proposal, never mutates; fail-soft =
logs/exits 0, never blocks; report-only = runs the checks and records the outcome, judges
nothing, and has no gate to arm even in principle) — a judgement about an organ's code,
derivable from no frontmatter block or hook id. The rows below are the organs whose posture
this map is the source for; a row's absence means *posture not yet recorded here*, never
*organ does not exist*. "Layer" notes
whether the organ travels: **L0** = global `~/.claude` (fleet-wide), **hub** =
this repo's `.claude/`, **plugin** = `tier1-lifecycle` (repo-class), **pre-commit** =
local git gate, **server** = GitHub Actions, off-host, after the push has already landed.

**Status** (added 2026-07-26 per intake #17 §5) answers a question "failure posture"
does not: *does this organ actually reach reality today?* — **ARMED** = present and
invocable, and its trigger column says how it is reached; **RULED-UNBUILT** = ruled into
existence, not yet built (it is not in this table until it is; the declared-only
`editor-config` carrier, `implemented: false`, is the current example); **RETIRED** =
removed, kept only as a record.

ARMED is *availability*, not *automatic execution* — read it with the Trigger column. A
parenthetical narrows it where the row would otherwise overclaim:

- *(manual)* — real and invocable, but **nothing invokes it on a schedule or a gate**; it
  runs only when a human runs it. Its automatic wiring is a named open ticket.
- *(no-op zone)* — armed against a zone that no longer exists, so it can never fire.
- *(stale input)* — fires correctly, on input from an upstream stage that no longer
  produces (Ch6). The organ is healthy; what it reports is not.

An organ can be ARMED and still tell you nothing. Read the qualifier before trusting it.

| Organ | Trigger | Layer | Failure posture | Status | Defining ref |
|---|---|---|---|---|---|
| `block-onedrive.ps1` (PreToolUse) | every Bash/PowerShell/Edit/Write/NotebookEdit call (command + file_path/notebook_path) | L0 | **fail-closed** (P0) | ARMED | ADR-75, global CLAUDE.md §P0 |
| `block_immutable_edits.py` (PreToolUse) | Claude **mutating tools only** (Edit/MultiEdit/Write/NotebookEdit) on `docs/decisions/transcripts/**` — that zone was **deleted at `b4435fad` (2026-07-23), per the operator ruling of 2026-07-22**, so the guard currently matches nothing; a Bash/PowerShell write is **not** caught | hub | fail-closed in-zone, fail-open out-of-zone | **ARMED (no-op zone)** — kept armed deliberately as the standing refusal that re-creating the zone does not silently re-open in-place editing | ADR-77 (#105); **`.methodology.yaml` `adr77-transcript-guard`** (RULED 2026-07-25, re-read at `review_date: 2026-10-25`) |
| `fleet_health.py` (SessionStart) | session start, throttled to **once per calendar day** (`fleet_health.py:156`, `d != date.today()` — a date comparison, not a rolling 24h window: two sessions either side of midnight both run) | hub · Tier-2 | fail-soft | ARMED | ADR-69/70/76 |
| `fleet_health.py` `[load]` operator-load gauge — `collect_load` reads triage/closures/dispositions/review-pending/backlog, `load_line` renders the one-line digest, `append_load_row` writes the trend row | rides the same once-per-day SessionStart throttle as the row above | hub · Tier-2 | fail-soft per producer (an unreadable `BACKLOG.md` yields `n/a`, never a false zero) | ARMED | [#270]; `scripts/fleet_health.py:610` (`collect_load`), `:642` (`load_line`), `:689` (`append_load_row`); trend sink `logs/OPERATOR-LOAD.csv` (gitignored) |
| `surface_triage.ps1` (SessionStart) | session start | hub | fail-soft | **ARMED (stale input)** | nightly outcome loop (Ch6) |
| `billing_leak_sentinel.ps1` (SessionStart) | session start | hub | fail-soft (WARN) | ARMED | #101 |
| `changelog_sentinel.py` (SessionStart) | session start | hub | fail-soft | ARMED | #113 |
| `surface-closures.ps1` (SessionStart) | session start | L0 | fail-soft | ARMED | ADR-70 (5c) |
| `propose_closures.py` (Stop) | session end | plugin · Tier-1 | **propose-only** (never mutates BACKLOG) | ARMED | ADR-70 |
| `session_end_backpressure.py` (Stop) | session end | hub | **advisory in full** since the ADR-85 amendment 2026-08-03 §A5 — it has **no hard leg and cannot block a turn**; the JOURNAL teeth moved to `block_unanchored_push.py` (pre-push) because a Stop hook is exhaustible by the host's consecutive-block cap, and an organ that can be exhausted cannot carry teeth. Its outer error is now loud rather than a silent `return 0` | **ARMED (advisory)** | #126; ADR-85 amendment 2026-08-03 §A5; `scripts/session_end_backpressure.py:14` |
| `verify` (skill) | invoked per numbered step | hub | advisory (pytest+ruff+git) | ARMED | #104 (home #9 open) |
| `gotchas` (skill) | auto-consulted before edits | L0 | advisory | ARMED | global |
| `artifact-reader` (agent) | reading a >20k-token artifact | hub | read-only (Read/Grep/Glob) | ARMED | #97 |
| `/save`, `/handoff`, `/handoff-verify` (commands) | operator | hub | — | ARMED | repo; ADR-82 / HANDOFF v6 |
| `/ship`, `/review-closures` (commands) | operator | plugin (fleet-wide) | branch→`--no-ff`→push→**delete source branch**→clean-tree gate (merge is ATOMIC — the delete is part of the same operation, not a later decision; git-discipline) | ARMED | git-discipline; ADR-70 |
| `/changelog-review`, `/codex-review` | operator (push) | hub / L0 | — | ARMED | #113 / ADR-54 |
| `conformance-hub.js` (Workflow) | operator (`ultracode`) or cloud Routine | Tier-3 | read-only + skeptic + evidence-required | ARMED | ADR-70 (#81) |
| `_commit_routine_outputs` → `automation/fleet-audit` (audit.py Routine writer) | Routine/nightly durable-output commit | hub | **fail-soft** (pathspec-bounded `commit-tree`; main tree untouched, never `git add -A`) | ARMED | ADR-84; #125; #254(a) |
| `git_backlog_drift` (audit check) | `ship-gate` + SessionStart `fleet_health` (which runs `audit.py run`, the full sweep) — **ship-tier since [#597]**, so it no longer fires at the pre-commit gate: WARN-only, and a WARN never blocked a commit | hub | fail-soft (WARN) | ARMED | #90; ADR-65 |
| `doc_claims` (audit check) | `ship-gate` + full sweep — **ship-tier since [#597]**. The `_GATE_MODE` split that ran counts/lists at commit and the test-count only off-gate is retired; every claim now runs wherever the check runs | hub | fail-soft (WARN) | ARMED | #89 |
| `no_ff_merges` (audit check) | `audit.py health` — pre-commit gate + SessionStart `fleet_health` | hub | fail-soft (WARN) | ARMED | #153; ADR-84; core-invariants #5 |
| `handoff_probes` (audit check) | `audit.py health` — pre-commit gate + `ship-gate` | hub | **fail-closed** (FAIL on broken probe binding; WARN on anchor-missing/skipped) | ARMED | #163; HANDOFF_PROCESS §5/§10 |
| `doc_rot` (audit check) | `audit.py health` — pre-commit gate + `ship-gate` (disposition baseline) | hub | fail-soft (WARN, one per locus) | ARMED | #140; ADR-88 FC4 (ADR-65/49/41) |
| `doc_structure` (audit check) | `ship-gate` (disposition baseline) — **ship-tier since [#597]**: WARN-only at 4,531 ms, so its cost at the commit gate bought no gating power | hub | fail-soft (WARN, one per locus) | ARMED | #192; ADR-88 prose-shape |
| `hooks_armed` (audit check) | `audit.py health` — pre-commit gate + SessionStart `fleet_health` | hub | **fail-closed** (FAIL on a missing/foreign `.git/hooks` gate) | ARMED | RF-2 (Fable arch review 2026-07-04 §4); self-armed by the SessionStart `pre_commit install` |
| `fleet_parity.py` → `check_fleet_parity` (audit check) | `ship-gate` — blocking `ALL_CHECKS` member since [#337] ([#336] cleared the last WARN); the standalone CLI stays read-only | hub | **fail-closed** on a real divergence (FAIL: refused/must-absent/tombstone-violated; WARN→RED: undeclared/unavailable/tracked-ephemera; stale-declaration/advisory-rewarn stay advisory). The walk measured **14,520 ms** and no longer runs per-commit: **[#597] discharged the filed ship-gate-scoping follow-up**. It is the one ship-tier member that CAN emit `fail`, so it carries a risk argument beyond cost — parity is a CROSS-REPO property that a hub commit cannot create, and the arc boundary is where a fleet-wide claim can honestly be made. Given up, stated: a parity regression introduced elsewhere now surfaces at ship rather than at the next hub commit | ARMED | #328/#332/#337; intake #12 + RULED #14; ADR-102/103; `ecosystem/parity-surfaces.yaml` + `dependency-baseline.yaml` |
| `routine_consumers` (audit check) | `audit.py health` — pre-commit gate + `ship-gate` | hub | **fail-closed** on a declared routine whose `consumer`/`consumption_path` is missing, blank, placeholder, or duplicated. **COVERAGE BOUNDARY — green says almost nothing:** it checks ONLY BACKLOG rows carrying an ADR-105 `· routine:` marker — **one** row at acceptance ([#348]), **two** live as of 2026-08-28 ([#552], [#426]) after [#348] closed and its declaration was re-anchored into `protocols/PLAYBOOK.md` §10. That re-anchoring exposes the organ's real limit: a declaration that moves to its living home leaves this check's scope entirely, because the check reads backlog rows and nothing else. The ~30 live routines — session hooks, commit-time gates, scheduled jobs — are not BACKLOG rows, carry no marker, and are **NOT checked**; retrofit is [#426] | ARMED (scope = marked rows only) | [#419]/ADR-105 (gated at ACTIVATION, not at filing) |
| `residual_completeness` (audit check) | `audit.py health` — pre-commit gate + `ship-gate` (changed handoff-bundle files) | hub | **fail-closed** (FAIL on a FILL-IN region still carrying its generator placeholder; degrades to WARN on internal error; scans the working tree — the staged-blob gap is #366) | ARMED | ARC-5 first enforcing mechanism; HANDOFF_PROCESS "Residual completeness"; #365/#366 |
| `boundary_report.py` (reporter) | manual CLI | hub · read-only | fail-soft (writes `logs/BOUNDARY-DRIFT.md`; a reporter, NOT a gate — deliberately not in `ALL_CHECKS`) | **ARMED (manual)** | #312; CLAUDE.md Form-A regions |
| `boundary_headers.py` (generator) | manual CLI (`--check` regen-and-diff · `--coverage`; pre-commit wiring open #369) | hub | generated-not-hand-maintained (headers derived from the #312 markers via `boundary_report` imports — a hand-edit is overwritten on regen); suite-guarded at ship-gate | **ARMED (manual)** — pre-commit wiring is #369 | #352; `tests/test_boundary_headers.py` |
| `fleet_analytics.py` (reporter) | manual CLI (**ruled manual**, 2026-08-28) | hub · read-only | fail-soft (writes `logs/FLEET-ANALYTICS.md`; `main()` always 0; NOT in `ALL_CHECKS`) | **ARMED (manual)** — manual is the ruled end state, not a gap ([#391] closed) | #384 (L5a descriptive analytics); intake #16 §3 |
| `deploy/tool.py` + its registered carrier modules (roster of record: `deploy/manifest-v*.yaml` `carriers:`; enumerated in §Validators) | operator (hub, per-consumer) | hub → consumer | verify-gated (record iff every carrier verifies); write-yes / commit-no | ARMED | ADR-91/92/93; PLAYBOOK §20 |
| `floor-hash-verify` (pre-commit) + SessionStart floor guard (`.claude/check_floor_hash.py`) | consumer commit / session start | consumer (armed by `carrier_floor`) | **fail-closed** (loud on floor drift) | ARMED | ADR-93 (#226) |
| pre-commit gates (`.pre-commit-config.yaml`) | local commit | pre-commit · Tier-1 | **fail-closed** | ARMED | §Validators below (count in `ecosystem/doc-counts.md`) |
| `report-only-wall.yml` (GitHub Actions) | `push` to `main` (+ `workflow_dispatch`) | **server** | **report-only** — the three measured legs (`pytest`, `audit.py health`, `block_unanchored_push.py`) are `continue-on-error` and never block; the job still reds on a *setup* failure (uv pin assertion / `uv sync`), deliberately, because a green job with no environment would be a lie | **ARMED (FIRED — verification discharged 2026-08-07 by run `31161874468`, event `push`, head `2f2edd2b`: `pytest` exit 1 and `audit.py health` exit 1 recorded in the summary table while the job concluded `success`, and the anchor leg ran a REAL push range `319f885d..2f2edd2b` for the first time, exit 0)** | [#501] closed 2026-08-07; ADR-101 amendment 2026-08-06; `docs/audits/2026-08-06-technical-night-prep-packs.md` §B1 |

The **Tier-1 closure loop** is three of these organs in a cycle:
`commit closes [#id]` → `Stop: propose_closures.py` writes `logs/PROPOSALS-*.md`
(STRONG/WEAK, gitignored) → next `SessionStart: surface-closures.ps1` prints
`[closures] N proposed` → `/review-closures` confirms → `BACKLOG.md` updated. Detect-
and-propose only; the human gate closes (ADR-70; distribution in Ch4).

**The deploy subsystem** (orchestrator detail in Ch4; validators below) versions the
methodology corpus (ADR-91) and delivers it to a consumer through its carrier modules behind a
**per-carrier verify-gate** (ADR-92) — the version record lands only if every carrier
verifies. The `floor` carrier additionally **arms** the ADR-78 floor under **model A**
(ADR-93): committed + two-leg hash-guarded (a SessionStart guard + the commit-time
`floor-hash-verify` hook, both running the consumer's `.claude/check_floor_hash.py`), so floor
drift fails loud. Operator-run from the hub, one consumer per invocation; runbook PLAYBOOK §20.

**The desired-state organ class (ADR-109).** Three parts, one class: `ecosystem/schema/` holds
the typed, versioned **contract** (`desired_state.py`, `schema_version: "1.0.0"`);
`scripts/desired_state_loader.py` is the **loader** that parses the live sources into one
validated model; `scripts/desired_state_report.py` is the **divergence report** over it. All
read-only, all operator-invoked — no trigger, no gate, nothing converges state (ADR-109 §8:
"Read-only, no execution engine", and the report "is not convergence"). Membership resolves
toward `ecosystem/deployed-versions.yaml` (§2), so the report's matrix is narrower than
ADR-104's 9-repo declaration; the [#462] `membership_agreement` check is what makes a declared
member absent from every surface visible.

`ecosystem/schema/` is deliberately outside the codemap's `--source-root scripts` scope: the
codemap maps executables; the typed contract lives with the data it governs (ADR-109 §9). Cost
accepted: the schema package and the loader→schema edge do not appear in the structural map.
Revisiting requires NEW evidence (e.g. the codemap growing multi-root support) as a NEW row —
this ruling is not reopenable by preference.

**The one-graph organ class — PROPOSED, NOT RATIFIED, and NOTHING BELOW IS BUILT AS A VIEW.**
Read this whole block in the future tense. **ADR-118 is `Proposed`** (2026-09-07), not `Accepted`;
its own status note records that the operator's ruling and the filing prompt both call the state
**DRAFT**, and `Proposed` is only the enum's spelling of that. It is therefore **absent from
Governing ADRs by the same rule that kept ADR-116 out** — a Proposed ADR is not governing
doctrine — and **no row is added to the organ table above**, per this chapter's own Status legend:
a RULED-UNBUILT organ stays out of the table until it is built, and this one is not even ruled.

What is **landed** is one module and no wiring. `scripts/file_purpose_graph.py` (**FPG-1**) exists,
declares `rustworkx` through the ADR-106 path, and answers `why <path>` with purpose / consumers /
edges. ADR-118's Context measures it at 1922 nodes, 12664 edges and 12 edge kinds, and states in
the same breath that it is *"wired into NO gate, no check and no hook"*. Twelve organs still
compute their own edges. **That is the state of the tree; everything else here is a plan.**

- **Graph (planned).** FPG-1 becomes the single source for edges, and an organ that needs an edge
  relation **queries** it instead of extracting its own. **Scope is narrower than ADR-118's own
  wording, and the narrowing is load-bearing:** the review pass that followed the filing confined
  FPG-1 to **corpus-structure edges only** — citation, generation, template, test, and script
  call-site. Those five are properties of *what the corpus contains*, which is what a graph over
  tracked files can answer.
- **Catalog (planned).** Node attributes on FPG-1 rather than a second store — path, id, genre,
  one-line description, last content commit, in-degree, trigger count, owner — generated,
  committed as a registered derived copy, and **diffed nightly, the diff being the report**. A
  `resolve(id) → path` resolver is what would make citations id-based. None of it is generated
  today; `gen_catalog.py` does not exist in this tree.
- **Refusals (planned, and the half already proven in miniature).** The refusal is the point:
  *a file nothing explains is a defect, not a mystery.* FPG-1's `why` already refuses an
  unexplained path, and its RED-first witness is
  `tests/test_file_purpose_graph.py::test_why_refuses_a_planted_unknown_file`. The **planned**
  organ over it is an orphan census — in-degree 0 over the corpus-structure kinds, WARN on first
  sight, FAIL after the groom cadence without a disposition. It is not registered in `ALL_CHECKS`
  and fires nowhere.

**STATE GATES ARE NOT VIEWS, AND THIS IS THE BOUNDARY THE MAP EXISTS TO HOLD.** The JOURNAL
spine-anchor gate and the staged-ADD refusals (`block_unanchored_push.py`,
`validate_hermetization.py`, `check_derived_copies.py`'s rebind leg) judge **commit-time state** —
what this push contains, what this commit stages — not what the corpus cites. A graph over tracked
files cannot answer *"does the range being pushed carry an anchor"*, because the fact is about a
ref range and a working index, not about a file's edges. **They stay gates.** Folding them into
the view layer would trade a fail-closed answer about the act being performed for a derived answer
about the tree that resulted, which is a different question asked one step too late — and the
organ map's whole value is the failure-posture column that distinction lives in.

*Provenance, marked so it is not read as stronger than it is.* The scope narrowing above reaches
this map through the batch-CLOSE lane contract's restatement of a review-pass finding; **the
review artifact itself is not in this tree**, so the narrowing is recorded here as **relayed, not
resolved against a source** — an Inference in the Ch8-epistemic sense, deliberately not written as
Witnessed. When the ADR is ratified the scope clause should be re-derived from whatever surface
carries it, and this paragraph struck.

**Machinery retired (C3 sweep, 2026-06-05).** `/boot` and `/evolve` archived to
`~/.claude/archive/2026-06-05-machinery-c3/`; `CHANGELOG.md` + `BACKLOG_ARCHIVE.md`
deleted 2026-05-16 (git + JOURNAL replace them); root `README.md` deleted 2026-05-23
(ADR-38 A5) and **RECREATED 2026-08-29** — ADR-114 is Accepted and supersedes A5 in that
single respect, so the root `README.md` is now a sanctioned Tier-1 file
(`validate_hermetization.SANCTIONED_TIER1_FILES`) and this repo's canonical front door;
`VISION.md` is superseded and retained, not deleted — **relocated** to `docs/archive/VISION.md`
at the hub (`git mv`, byte-identical, [#614] lane-e-5, 2026-09-01), the hub's own step one of
ADR-114 option (C)'s sequenced nine-repo filename migration; still tracked. The ADR-114
`Decommission` clause cites an echo of the prohibition at `ARCHITECTURE.md:366` — **no
such line exists**, and `grep -n "recreate" ARCHITECTURE.md` returns nothing; that
decommission item was discharged by attrition before the ADR was ruled, and this
sentence is the stale *deletion fact* corrected in its place.
The ADR-68 **local** night-agent was **never registered** — superseded
in reality by the cloud Routine (Ch6 supersession note).

## Validators and enforcement (executable, here) [CORE]

Per the ADR-28 invariant, Layer 2 hosts **hub-local validators, generators and gates** —
read-only **on siblings** (invariant 2), never read-only on its own tree, where many of these
scripts write and `audit.py` pushes to `origin` (`audit.py:3967`). It does not orchestrate a child repo, but it
verifies, generates and gates itself. These are the *executable* organs the map
above references — the **named deterministic-trigger organs**, curated to what the map
references, **not an exhaustive inventory** of every script in `scripts/`:

- `scripts/audit.py` — cross-repo conformance + self-audit; a registered check suite
  (count in `ecosystem/doc-counts.md`; **the roster is not restated here** — run
  `uv run --locked python scripts/audit.py checks` for the live registry. A partial `incl.`
  list is the M2 failure class twice over: it rots against the registry AND reads as complete
  while omitting most of it).
  `run` = manual ecosystem sweep; `health` = pre-commit gate (FAIL blocks, WARN informs);
  `ship-gate` = the #147 pre-ship verification-organ gate (Definition-of-shipped point 6).
  **Seam `ship-gate` vs `health`:** both reuse `ALL_CHECKS`, but `health` gates each
  *commit* (FAIL-only; WARNs pass) and — **since [#597]** — runs only the **commit tier**, while `ship-gate`
  gates the feature *arc* at `/ship` — it reads `Finding.status` not exit codes (the awareness
  organs exit 0 on drift), blocks on FAIL **and** any new/undispositioned WARN, runs claim-3
  (full verification), and dispositions expected WARNs via `ecosystem/disposition-register.yaml`
  (live examples: the three grandfathered `no_ff_merges` June commits; the `undeclared_edges`
  prose-reference set). A register entry matching no live WARN is surfaced as stale and is
  **removed**, not kept as decoration (ADR-75) — which is where the former
  `warn-77-voided-closure` entry went once #77 was KILL-removed from BACKLOG; the register's own
  comment block keeps that record. Read-only **on siblings**, not on this tree — `health`/`ship-gate`
  write findings, `_replicate_automation_branch` pushes to `origin` (`audit.py:3967`) and
  `_commit_routine_outputs` commits to `automation/fleet-audit`; hub-only organs no-op on children
  (the `/ship` wiring is hub-guarded).
  **Per-check gate tier ([#597]).** Every `ALL_CHECKS` member declares the tier it runs at —
  `_tier(TIER_COMMIT, …)` / `_tier(TIER_SHIP, …)` in the registry itself, read by `run_checks`.
  The ladder is **nested** (commit ⊂ ship): `health` runs the commit tier, `ship-gate`/`run`/`repo`
  run everything, so the tier can only ever move a check to a LATER gate, never off the gate set —
  ship-gate's finding stream is unchanged **byte for byte**, proved side-by-side rather than
  asserted. A ship-tier check still appears in the `health` report, as an `n/a` naming the deferral,
  because a silently-omitted check is indistinguishable from a deleted one. **A check is ship-tier
  only when it BOTH cannot emit `fail`** — `health` exits 1 on `fail` alone, so a WARN-only check's
  commit-time verdict blocks nothing — **and costs ≥1 s measured**; the sub-second WARN-only checks
  stay at commit, because a tier decision with no measurable payoff is not a decision. This
  generalizes and **retires `_GATE_MODE`**, the module global that two of forty-six checks consulted.
  Read the assignment off the registry, not off a roster here; the measured basis is
  `docs/audits/2026-08-27-technical-lane-nb-tiering.md`.
- `scripts/normalize_headers.py` — dated-log header normalization (pre-commit).
- `scripts/validate_backlog.py` — BACKLOG story-map schema (ADR-66; pre-commit).
- `scripts/validate_git_backlog.py` — git↔backlog drift, direction (a) STRONG: a
  main-line `closes [#id]` whose item is still in BACKLOG = drift (ADR-65; #90).
  Read-only; surfaced via the `git_backlog_drift` audit check (WARN). Direction (b)
  deferred to #90b. Standalone CLI: `python scripts/validate_git_backlog.py`.
- `scripts/validate_no_ff.py` — `--no-ff` merge guard (core-invariants #5): a non-merge
  commit on main's first-parent spine since the enforcement baseline (a direct/FF commit).
  ONE rule, no exemptions — the ADR-80 automation allowlist was removed once the writers
  moved off `main` (ADR-84/Q9). Read-only; surfaced via the `no_ff_merges` audit check (WARN);
  hub-only (fleet-wide deferred, #153). Detect-and-surface, not prevent.
- `scripts/block_ff_push.py` — pre-push GATE: the PREVENT counterpart to validate_no_ff's
  detect-and-surface (core-invariants #5). Refuses a push that would put a non-merge commit
  on main's first-parent spine (a direct-to-main commit or a true fast-forward merge); a
  `--no-ff` merge passes. Delegates the scan to `validate_no_ff.find_violations` (ONE shared
  FF-signature, so detector and gate cannot disagree). Wired as the `block-ff-push`
  pre-commit-managed `pre-push` hook (activate once: `pre-commit install --hook-type
  pre-push`); HUB-ONLY; **fails CLOSED (exit 2) on internal error** (ADR-85 amendment
  2026-08-03 §A6). Client-side teeth (bypassable via `git push --no-verify`) — the
  `no_ff_merges` audit WARN stays the post-hoc backstop; bypass-proof server-side teeth
  deferred under #153 (#153; ADR-84; core-invariants #5).
- `scripts/validate_doc_claims.py` — prose-vs-state: a living doc's count/list CLAIMS
  vs ground truth. Four claims (`_CLAIMS`, `validate_doc_claims.py:224-239`): the audit
  check-count (vs `len(ALL_CHECKS)`), the pre-commit gate-count and the pytest collected-count
  (vs `pytest --collect-only`) all read the committed-generated
  **`ecosystem/doc-counts.md`** — #222 moved them off ARCHITECTURE.md, and **this file no longer
  carries them**; the roster set-claim reads **CLAUDE.md §9**'s named hook list against
  `.pre-commit-config.yaml` (order-independent). Read-only; surfaced via the `doc_claims` audit check (WARN). Single-doc
  accuracy only — history-accretion rot is the `doc_rot` check (#140); cross-file fidelity
  is the coherence spine (#179–#182). Standalone CLI: `python scripts/validate_doc_claims.py` (#89).
- `scripts/validate_doc_rot.py` — doc-rot / grooming checker: history-accretion bloat
  (**ADR-88 FC4**; load-bearing doctrine ADR-65 condense-to-git / ADR-49 retired changelogs /
  ADR-41 cadence). Four read-only sub-detectors — BACKLOG inline-history accretion, per-section
  Section-history accretion, file-bloat vs a self-declared budget, grooming-cadence lapse —
  WARN-only, one Finding per locus, DETECT-ONLY (never condenses; condense-preserving).
  Surfaced via the `doc_rot` audit check; pre-existing loci grandfathered in the disposition
  register. Defers cross-file fidelity → coherence spine and intra-file duplication → #190.
  Standalone CLI: `python scripts/validate_doc_rot.py` (#140).
- `scripts/validate_doc_structure.py` — prose **structural** linter: section-numbering
  integrity, header-scheme consistency, ToC accuracy, dangling-allow self-policing (**ADR-88**
  prose-shape coherence). Reuses the fence-aware ToC parser so the linter and ToC agree (the
  property that keeps embedded-template H2s from reading as rot). WARN-only, one Finding per
  locus, DETECT-ONLY (never renumbers / auto-fixes); documented-intentional cases (the §18 gap)
  pass via co-located `structure-allow` markers. Distinct failure class from #140 (structural
  shape, not history-accretion). Standalone CLI: `python scripts/validate_doc_structure.py` (#192).
- `scripts/validate_reconciliation.py` — declared-edge **reconciliation** checker: the
  `reconciled_versions` audit check / **ADR-88's named deterministic trigger** for the doc→doc
  **declared** edge. A dependent declaring `reconciled_with: <spec>@<version>` must match the spec's
  live version; a drifted edge **FAILs** (the coherence-spine gate, #172 v1). The *declared* half of
  dependency coherence — the complement to `scan_undeclared_edges.py`'s discovery half (below).
  Standalone CLI: `python scripts/validate_reconciliation.py`.
- `scripts/scan_undeclared_edges.py` — undeclared-edge referential-currency scan: the
  **discovery** half of dependency coherence (**ADR-88 FC2**; #179) — the complement to the
  declared-edge checker (`reconciled_versions` / `validate_reconciliation.py`). Infers
  **prose-only** edges (a doc prose-references a registered spec but carries no `reconciled_with`)
  and surfaces them as **candidates for human confirm — NO auto-declare**; writes nothing, exits 0
  (awareness layer). Registry-scoped heuristic (Tier-1 path/basename + Tier-2 spec-id → candidates;
  Tier-3 title-prose → retained weak signals); fenced code regions excluded from matching. Surfaced
  via the `undeclared_edges` audit check — **in `ALL_CHECKS`** since 2026-07-03 as a **WARN-only**
  ship-gate leg (Fable consult #1 ruling #2; never FAIL-gates), not a hook (a flat module, so not a
  codemap node). **Candidate scope (#199):**
  the scan prunes immutable zones (handoff bundles, ADRs, transcripts, audits, append-only
  JOURNAL/LESSONS/TOKEN-LOG, ADR-80 `ecosystem/*/history`) and gitignored scratch (via
  `git check-ignore`, fail-open if git absent) — neither can carry a `reconciled_with` edge — so the
  candidate list is the actionable, tracked-mutable corpus; the two living READMEs inside those
  trees are allowlisted (no recall loss). Standalone CLI: `python scripts/scan_undeclared_edges.py` (#179).
- `scripts/validate_doc_code_edge.py` — doc→code **declared-edge** integrity: discovery + resolution
  behind the `doc_code_edge` advisory check (**ADR-89 OQ1**). Discovers `<!-- rule: <id> -->` tokens in the
  authoritative declaration docs registered in `ecosystem/doc-code-edge.yaml` (`declaration_docs:`) and
  resolves each to its `# rule: <id>` code annotation under `scripts/` — rule-ID identity + path/AST content
  resolution, **move-safe** (the e22e883 spike). `broken_edge`/`ambiguous`/`code_orphan` → **WARN**
  (advisory-first; **never FAILs** this arc — promotion to a gate is data-gated, OQ3). The **#194 *Done-when***
  landed: `build_edge_index` (the derived **rebuildable index** — rebuilt from source each scan, no
  hand-maintained manifest, ADR-88 P3) + `scan_structural_integrity` (**L1**: dangling / `code_orphan` =
  code→nonexistent-rule / duplicate), proven on a fixture; the live check now also surfaces `code_orphan`.
  Hub-only; read-only; live on **the rules registered in `ecosystem/doc-code-edge.yaml`
  `coverage_scope`** per the ADR-89 OQ1 naming convention — the #194 cohort-1 + the #201
  governance trio + the #202 Tier-3 quartet (`coherence-doc-claims`/`-rot`/`-structure` +
  `handoff-probes-bind`) + `handoff-boot-budget` ([#446] R4) + `seal-journal-spine-anchor`. Read
  the count off that file, not off this sentence (it said "13" while `coverage_scope` held 15);
  the `doc_code_coverage_drift` check is what stops the registered set drifting off the
  auto-enumerable `ALL_CHECKS` surface. The multi-organ rules resolve via **resolver-allows-N /
  ADR-90**: a rule enforced in N code organs declares its expected `# rule:` count in
  `multi_site:`. Check in
  `audit.py::check_doc_code_edge`.
- `scripts/verify_handoff_probes.py` — handoff-probe teeth: every probe in the latest
  `PROBES.md` bundle binds to live state, by STRUCTURAL resolvability (resolve-only — no
  subprocess; Critical Rule #4). It proves each row BINDS; the v6 `/handoff-verify` command RUNS
  the rows at check-time — two organs, not interchangeable, because Layer 2 never executes.
  Mechanizes the manual probe-gate (HANDOFF_PROCESS §5/§10):
  malformed row / missing source-or-command target → FAIL, row-scoped `expected[ :]`
  answer-hint → FAIL (the v5.4 anti-bluff rung — a probe that ships its answer is bluffable
  by construction), reworded `#`-anchor → WARN
  anchor-missing, absent tool → skipped. Read-only; surfaced via the `handoff_probes` audit
  check (FAIL-class — a toothless probe blocks `/ship`). Standalone CLI:
  `python scripts/verify_handoff_probes.py <bundle>` (#163).
- `scripts/check_backlog_commit_msg.py` — `[#id]`-on-task-removal (commit-msg).
- `scripts/check_seal_identity.py` — handoff-bundle seal-identity pre-commit gate ([#475]):
  runs `gen_handoff.verify_seal_identity` (reused, one verifier) over the bundle dir of every
  staged `docs/handoffs/**` file — the commit-time twin of the [#473] seal-time refusal, so a
  mislabelled bundle cannot become an immutable committed artifact. Exit 0/1/2 (clean /
  violation / internal error — an error blocks); HUB-ONLY. Honest limit: Slug-row-vs-directory
  only, not stale P0c/P3/P8 locators inside a correctly-labelled bundle.
- `scripts/validate_hermetization.py` — ADR-101 §3 tree-seal refusal gate (pre-commit,
  prospective-only on staged ADDs; Rule A top-level/genre seal, Rule B audit-name grammar
  + R4 casing, **Rule C home allowlist** — an added file whose home directory is outside the
  allowlist derived from the live taxonomy is refused (operator ruling A of 2026-08-11,
  register `protocols/STANDING_RULINGS.md` K-1). Rule C exists because A and B between them
  read the top level, the `docs/<genre>/` level and audit filenames, and nothing read the
  rest of the path — which is how `docs/ORGAN-INDEX.md` came to sit loose at the `docs/`
  root. Honest limit: it polices the HOME of an added file, and the two open homes
  (`docs/handoffs/**`, `tests/fixtures/**`) admit arbitrary depth by design; HUB-ONLY;
  fail-open-loud on git error) (#306).
- `scripts/validate_residual_completeness.py` — handoff residual-completeness gate: a
  changed v5 bundle file may not ship a hand-authored FILL-IN region still carrying its
  generator placeholder. Surfaced via the `residual_completeness` audit check
  (**FAIL-class**; ARC-5's first enforcing mechanism); honest limit — scans the working
  tree, not the staged blob (#366).
- `scripts/codemap/` · `scripts/toc/` — codemap + TOC generators & freshness checks.
- `scripts/gen_doc_counts.py` — generates the committed `ecosystem/doc-counts.md` count
  fragment (audit check-count · pre-commit gate-count · pytest collected), moved off
  ARCHITECTURE.md so a count bump no longer trips the freshness gate (`canonical_freshness`
  A2) into forcing a `last_reviewed` re-stamp (#222). Reuses the #89 derivers; `--write`
  regenerates, `--check [--gate]` verifies (drift → the `doc_claims` WARN; ship-gate is the
  teeth). A **loose** module by design — not a codemap node, so its edits never regen the map.
- `scripts/fleet_parity.py` — the #328 fleet-parity checker (a blocking `ALL_CHECKS` member via `check_fleet_parity` since [#337]; the CLI itself stays read-only): a deterministic
  read-only walk of the registered fleet (hub included, intake #12 §9a) against the versioned
  `ecosystem/parity-surfaces.yaml` + `ecosystem/dependency-baseline.yaml` (#332 dep leg),
  consulting each repo's `.methodology.yaml` through the Informant's own reader (one taxonomy;
  expired `review_date` = advisory re-WARN per §9b). Register-grammar verdicts; effect-probes
  (`git check-ignore`, armed hook stages, tag-ancestry) over text-grep; refusal findings on
  ambiguous/mis-addressed pointers — detect-and-report, NEVER an action proposal. Writes the
  gitignored `logs/FLEET-PARITY.md` digest + appends schema-versioned checker-run JSONL events
  to the gitignored rotation-capped `logs/PARITY-EVENTS.jsonl` (`fleet_parity.py:123`,
  `EVENTS_PATH`; conformed to the [#395] UPPERCASE-KEBAB `logs/` convention on 2026-07-22 —
  this line still spelled it lowercase) (fail-open emission). A loose
  module (not a codemap node). **Promoted to a blocking `ALL_CHECKS` member** ([#337], 2026-07-18):
  `audit.py::check_fleet_parity` calls `fleet_parity.walk()` in-process and maps blocking verdicts
  to gating Findings (`exempt:` in doc-code-edge.yaml — manifest-driven, not a doc→code rule). The
  standalone CLI is unchanged: `python scripts/fleet_parity.py --run-date YYYY-MM-DD` (#328/#337).
- `deploy/tool.py` + `deploy/contract.py` + the carrier modules registered in
  `tool.py::make_carriers` — the carrier set is **computed, not restated**: read the
  manifest's `carriers:` block (`deploy/manifest-v*.yaml`), which is the surface the
  orchestrator itself reads — the ADR-92 **deploy orchestrator** (Ch4).
  **The roster of record is the manifest's `carriers:` block** (`deploy/manifest-v*.yaml`, gated
  by the `roster-freshness` hook), not a count restated in prose: at v1.4.0 it declares seven —
  six `implemented: true` plus `editor-config` `implemented: false`. (`carrier_docs` landed at
  `ec924ae2`, [#280]; this list said "five" until 2026-08-10.) A read-only ASSESS CLI (`deploy <repo> --target <vX.Y.Z>`) detects each carrier's
  state vs a per-tag manifest and prints a plan; `--execute` applies + **per-carrier
  verify-gates** the version record (`ecosystem/deployed-versions.yaml`, ADR-91) + stages the
  consumer carriers (write-yes / commit-no — the Layer-2 boundary). Every carrier implements
  `contract.py`'s `detect`/`apply`/`verify`. Runbook PLAYBOOK §20.
- `deploy/floor_conformance.py` — #230 end-to-end floor-conformance harness (ADR-93): proves
  the ARMED floor loop *functions* (not merely present) — the `@`-include hashes to its
  `.sha256` sidecar, the SessionStart self-arm wiring, the commit-time `floor-hash-verify` hook
  blocks a poisoned commit, a deleted floor fails loud. Hub CI (synthetic consumer) + Layer-2
  (`--consumer ../ai-council`, real clone). Read-only.
- `scripts/reverse_dep_oracle.py` — code→code reverse-dependency **oracle** (**ADR-89**
  computed-edge doctrine; #193). Given a Python symbol, returns its reverse-dependents via a
  headless Pyright `references()` query, with a mandatory **provenance** block (git rev, dirty
  set, completeness/truncation caveat) plus the three honest limits (static-Python-only,
  repo-scoped, references-only) on **every** answer. Read-only query TOOL — **not** a
  validator/gate, **not** in `ALL_CHECKS`, not wired to a hook (a flat module, so not a codemap
  node). The gate that gives it teeth is **built**: `audit.py::check_safe_removal` (#195, logic
  in `scripts/safe_remove.py`) is a FAIL-class `ALL_CHECKS` member — diff-triggered, fail-OPEN
  when Pyright is absent. #195 is closed; the deferred L3 real-deletion phases are **[#218]**
  (this bullet named #195 as the *pending* consumer until 2026-08-10). Pyright is vendored via
  `npm install` (pinned in `package.json`; `node_modules/` gitignored). Standalone CLI:
  `python scripts/reverse_dep_oracle.py <symbol> [--json|--text]`.

**Graph-level conformance — the legibility graph as an integrated whole.** The four
edge-validators above are each proven by their own suite; the *integrating* property — all
four **registered + operational**, and each **firing on a representative break through its
real integrated entry point** — is owned by `tests/test_legibility_graph_conformance.py` (it
adds the graph-level proof and closes nothing). Three edge-types are **registered in the
`audit.py` gate** (`ALL_CHECKS`) — one FAIL-gates (spec→dependent), two are **WARN-only awareness
legs that exit 0 by design** (doc→code, and undeclared — wired 2026-07-03); the fourth is a
**query tool** that exits 0 and is **not** registered (code↔code) — so "integrated" is **not**
"all four FAIL-gate" (the "in gate?" column keeps that honest). The
code↔code fires-cell is **skipif-guarded** on the *same* `find_langserver` check the test's
3-state ledger (proven/skipped/gap) derives from: with Pyright vendored (`node_modules/`, this
env) it runs+passes; where Pyright is absent it **skips** and the tally drops the "fully
proven" headline — green never lies. Per-oracle **deep modes** stay in the per-oracle suites
(referenced in the last column), never re-run here.

| Edge-type | In gate? | Registered + operational | Fires on a representative break (integrated entry) | Deep modes (referenced — not owned here) |
|---|---|---|---|---|
| spec→dependent (#172) | yes (`ALL_CHECKS`) | PROVEN | PROVEN — stale `reconciled_with` → `check_reconciled_versions` FAIL | `test_coherence_integration.py` + `test_validate_reconciliation.py` |
| doc→code (#194) | yes (`ALL_CHECKS`, hub-only) | PROVEN | PROVEN — declaration-registry doc + a broken/orphaned rule-ID → `check_doc_code_edge` WARN (broken_edge / code_orphan) | `test_doc_code_edge.py` (move-safety, dup-guard, coverage gate, registry-scoping guard, **L1 structural-integrity + rebuildable-index round-trip**, multi-site + coverage-drift teeth); coverage tail #201/#202/#203 **complete** — the `coverage_scope` set + the `doc_code_coverage_drift` guard |
| undeclared (#179/#199) | yes (`ALL_CHECKS`, WARN-only) | PROVEN | PROVEN — prose ref to a registered spec + no edge → candidate surfaced via `scan`/`main` | `test_scan_undeclared_edges.py` (tiers, fenced-exclusion, false-flag precision) |
| code↔code (#193) | no (query tool; its gate is `safe_removal`) | PROVEN | PROVEN here (vendored Pyright, skipif-guarded) — real reverse-dep query → ≥1 dependent w/ provenance | `test_reverse_dep_oracle.py`; transitive closure → #193/#195 |
| **graph-integration** | — | **4/4 PROVEN** | **4/4 PROVEN this env** (code↔code skipif-guarded) | referenced above |

**Env-aware tally.** This env (Pyright vendored) → **8/8 cells proven** (4/4 registered +
operational, 4/4 fires-on-break); integration **fully proven (this env)**. An unprovisioned env
→ **7/8 proven, 1 skipped** (code↔code fires — Pyright not provisioned): fully **provable**, not
fully proven there. No green — test name, output, or this map — reads as "fully proven" while a
cell is skipped or gapped. **Skip/gap tracking:** code↔code fires → skip-guarded, here proven;
its integrated enforcement (#195) and the oracle (#193) both **landed** — the live residual is
**[#218]** (the deferred L3 real-deletion phases); doc→code coverage tail
**#201/#202/#203 complete** (every `coverage_scope` rule mapped + the `doc_code_coverage_drift`
guard over the auto-enumerable `ALL_CHECKS` surface; the heterogeneous non-`ALL_CHECKS`
remainder stays curated).

- `tests/` — pytest unit tests for the validators (collected count in `ecosystem/doc-counts.md`; `pytest -x --tb=short`).

**Pre-commit gates.** **The id set and its count are not enumerated here** — they live in
`.pre-commit-config.yaml` (the source), `ecosystem/doc-counts.md` (the computed count), and
CLAUDE.md §9 (the annotated roster, held against the config by `validate_doc_claims` claim 2b,
the one enumeration of this class a gate protects). Read those three; this map points, and the
pointer cannot rot. What they do not carry, and this map does: the gates run at **three git
stages** — pre-commit, commit-msg (`backlog-id-on-close` + `backlog-filing-backpressure`, the
remove-side and add-side backlog gates), and **pre-push** (`block-ff-push`, the #153 prevent
half, + `block-unanchored-push`, the ADR-85 hard leg per amendment 2026-08-03 §A5). The
pre-push pair needs a one-time `pre-commit install --hook-type pre-push`; `default_install_hook_types`
wires it only on a fresh install.

*Why the enumeration is gone rather than corrected.* It rotted three times, each time by the
same mechanism — a sibling surface gained a gate and this sentence was not re-typed: sixteen of
seventeen from 2026-08-03 to 2026-08-10 (missing `block-unanchored-push`), seventeen of
eighteen from 2026-08-11 to 2026-08-12 (missing `organ-index-freshness`), and — found by the
2026-08-21 governance-drift audit and confirmed live on 2026-08-23 — **eighteen against a live
twenty-one**, missing `block-commit-on-main`, `lane-contract-check` and
`provider-registry-agreement`. The sentence had already claimed *"the roster is not re-counted
here"* while re-counting it. Restating a roster in prose is CLAUDE.md §4's named
anti-pattern and #222's reason for moving counts off this file; the fix is the pointer, not a
fourth re-typing.

Editing **this file** fires every `always_run: true` hook — `block-commit-on-main`,
`validate-hermetization` and `audit-health` at pre-commit, `backlog-id-on-close` and
`backlog-filing-backpressure` at commit-msg — plus the two whose `files:`/`types:` match it:
`normalize-dated-headers` (markdown) and `codemap-freshness` (its regex names
`ARCHITECTURE.md`). `block-commit-on-main` is the PREVENT half of core-invariant #5 at commit
time (`block-ff-push`'s pre-commit sibling): it refuses a direct non-merge commit while `HEAD`
is on `main`, so editing this file on `main` is refused *before* the push gate ever sees it.
The two pre-push gates are `always_run` too, but fire at push, not at the edit.

---

## Automation axes

**Chapter 3 — Automation axes.** Automation is read on **two orthogonal axes**. Hold
them separate — conflating them
is the historical confusion this chapter exists to prevent.

- **Axis 1 — LLM judgment (ADR-80).** *Does the organ run a model?* **Deterministic**
  (no model) vs **LLM-judgment** (runs a model).
- **Axis 2 — friction cadence (ADR-70/74).** Tier 1 always-on · Tier 2 scheduled ·
  Tier 3 episodic. **This axis is never renumbered** (ADR-80 §1).

The two axes are independent: a cloud Routine is *judgment* **and** ADR-74 *Tier 3*;
the scheduled fleet baseline is *deterministic* **and** *Tier 2*.

| | Deterministic (no model) | LLM-judgment (read-only + skeptic + ratified) |
|---|---|---|
| **Posture** | fail-closed on executing paths; fail-soft on awareness | nothing binds unattended; a skeptic kills false positives; a human funnel ratifies |
| **Tier 1 (always-on)** | pre-commit + commit-msg hooks; `audit.py health` | — |
| **Tier 2 (scheduled)** | `fleet_health.py` (Task Scheduler → Python, **no `claude -p`**; ADR-76) | — |
| **Tier 3 (episodic)** | — | cloud **Routine** (scheduled-unattended) · dynamic **Workflow** (operator-invoked) |

→ Operating doctrine: PLAYBOOK "Two-tier automation doctrine"; ADR-70/74/80.

**Channels (where automation output goes).** Post-Q9 (**ADR-84**) automation output is
**isolated from `main`** — each unattended writer commits only to its own dedicated
`automation/*` branch, never merged in. Two, deliberately distinct:

- **Cloud (judgment):** Routine commits nothing itself → `claude/conformance-YYYY-MM-DD`
  branch → PR → `nightly-conformance-triage` Action diff-guards → **diverts** the digest
  onto `automation/conformance-digest` (commit-tree plumbing) and **closes** the PR
  (does not merge to `main`). `surface_triage.ps1` reads the digest from that branch
  (`?ref=automation/conformance-digest`). (ADR-84; superseded the prior squash-merge-to-`main`
  channel, ADR-80 §2.)
- **Local writer (deterministic):** `audit.py`'s `_commit_routine_outputs` records durable
  outputs onto `automation/fleet-audit` via a separate index + `commit-tree` (main's
  HEAD/index/working tree untouched; the just-written files are restored out of the main
  tree). Pathspec-bounded (never `git add -A`), fail-soft, `Routine: fleet-audit` trailer;
  `state.yaml` gitignored, retained. (ADR-84; was ADR-80 §3 direct-on-`main`, wiring #125.)

**Model routing (t-shirt).** Pin every fan-out stage by size: **S = Haiku · M = Sonnet
· L/judgment = Opus** (PLAYBOOK Appendix B; ADR-70). **Unpinned fan-out is a bug** — an unpinned
subagent inherits the *main session model* (whatever the session is running — read it off
the live session, not off this sentence; it read `Opus 4.8` while sessions ran Opus 5), silently running the costliest
tier. **No `fallbackModel` on a pinned stage** — a silent swap breaks evidence
comparability across runs (ADR-80 §5).

**The routing table and the reviewer pin are L0 surfaces, and they are OUT of this repo's
universalization scope (RULED, architect 2026-08-22).** The canonical model-routing table is
`~/.claude/ROUTING.md`; the reviewer pin is `~/.claude/bin/codex-review.ps1`; the Codex config is
`~/.codex/config.toml`. **None of the three is in this repository**, and that is a decision, not an
oversight — PLAYBOOK Appendix B killed the resident routing copy deliberately (#158 Decision B) to
prevent drift. This paragraph exists because *silence is not a boundary*: a reader who found the
table absent could not tell a deliberate L0 placement from a gap, and a table-driven provider swap
would then look blocked on a missing file rather than correctly out of scope. **L0 here is the
distribution layer of Ch2's Layer column (global `~/.claude`, fleet-wide) — not a rung of the
ADR-113 L0–L5 maturity ladder**, which is a different namespace on the same letter and is the
confusion that ruling exists to end.

**The consequence, stated rather than left to be discovered at closure:** anything requiring the
reviewer pin to live *at its stated home in this repo* is unverifiable from here **by
construction** — `[#82]` (per-repository agentic-review profiles) inherits exactly that limit, and
it belongs in the row rather than surfacing as a surprise when the row is closed. The CLOUD-4 v2
lane lived the finding rather than merely restating it: `/codex-review` could not run in its
container because all three surfaces are L0, outside the clone.

→ The alternative that was NOT taken: bringing a copy in-repo behind a regen-and-diff drift gate
(the mechanism exists here seven times over). It remains available if the boundary is ever
revisited; revisiting requires reversing #158 Decision B for a stated reason.
(`docs/audits/2026-08-22-technical-cloud-wave-close-funnel.md` line A3; ADR-113 for the namespace.)

**Spec-orchestration.** The native `Workflow` launcher is not enabled in cloud
(re-probed 2026-06-05); a cloud Routine **falls back** to reading
`conformance-hub.js` as a *spec* and orchestrating it by hand. Doctrine:
**native-attempt-first, nightly re-probe**. Consequence — a guarantee written as
in-script code is **inert on the fallback path** (the `.js` is read, not run); the
real backstop must sit on the **executing path** (the Action/parser), not the
generator (PLAYBOOK "Routine/night deployment standard"; ADR-72).

**Adoption (how a pattern graduates).** Rubric = tool-vs-platform / pain-owned-vs-
imagined / subscription-economy fit, with **pre-registered kill criteria** and an
**n=2 evidence gate** — a routine codifies only after **two** real runs (ADR-74
Footnote B; ADR-80 cleared its gate via a red 06-06 + clean 06-07 digest). Case law:
Dynamic Workflows **ADOPT**, GitHub Action **ADOPT**, graphify **REJECT**, `/loop`
as a persistence host **REJECT** (ADR-74; in-session repair-loop split to #126).

---

## Distribution and transfer

**Chapter 4 — Distribution & transfer.** The methodology is authored in the hub and
**carried** to where it is consumed. Five distribution **channels**, each with a
different scope and freshness model (a distinct set from the deploy tool's
*carrier modules*, Ch2/Validators — the orchestrator bullet below maps the two):

| Channel | Scope | What it carries | Ref |
|---|---|---|---|
| user-layer `~/.claude` | fleet-wide (L0) | `block-onedrive`, gotchas, ROUTING, Codex config, `surface-closures`, the `--no-ff` rule | global; ADR-54 |
| `tier1-lifecycle` plugin | repo-class | `/ship`, `/review-closures`, `propose_closures`, `validate_backlog` (marketplace install) | ADR-70/73 |
| pre-commit `.pre-commit-hooks.yaml` | consumer-pull | the hub's six exported hook ids — `codemap-freshness`/`-generate`, `toc-freshness`/`-generate`, `backlog-id-on-close`, `block-ff-push` (hub is the source repo). **Exported ≠ consumed:** corp-monorepo pulls only `backlog-id-on-close` + `block-ff-push`, pinned at the tag **`v1.3.1`**, and has withdrawn the codemap/toc four by recorded `.methodology.yaml` waiver (`corp-monorepo/.pre-commit-config.yaml:83-95`). This row read "codemap ×2 + toc ×2 … corp consumes @`69558c7`" until 2026-08-10 — wrong on both legs | ADR-71; ADR-102 (gate-rev axis) |
| child floor `.claude/CLAUDE-FLOOR.md` | per child repo | ≤1,500-tok generated floor + `.sha256` under the child's `.claude/` (not repo root); operator-invoked generator (`scripts/generate_floor.py`, `@.claude/CLAUDE-FLOOR.md`-include from child CLAUDE.md) | ADR-78; hub shipped #121, pilot done |
| browser boot | browser sessions | the Handoff v6 **thin browser boot** — `HANDOFF_BOOT.md` + `PASTE_THIS.md` inside each `docs/handoffs/<bundle>/`. **ADR-79's consolidated-`BUNDLE.md` delivery was superseded by ADR-82** ("a ~3-line thin browser boot … replaces the heavy 8-file bundle", `docs/decisions/README.md:71`); no `BUNDLE.md` exists in the tree. Projects stay deferred — that half of ADR-79 stands | ADR-79 (Projects deferred); ADR-82 (delivery) |

- **Agents-distribution doctrine (extends ADR-71).** Agents are **authored and
  versioned in the hub**; they distribute **user-level (`~/.claude/agents/`) for
  cross-repo** organs and **via the plugin for repo-class** organs. **Children consume,
  never author.** (PLAYBOOK "Subagents" carries this; this map agrees.)
- **Cloud is hub-independent.** A cloud Routine clones only its own repo and consults
  no hub reference on the executing path; the private hub permanently closes ADR-71's
  "URL-swappable later" hatch *for cloud* (ADR-72). The plugin/pre-commit channels are
  **inert by design** in a fresh cloud clone — not bugs.
- **Deploy orchestrator (ADR-91/92; ADR-93 for the floor; validators in Ch2).** The five rows
  above are the *channels*; the **deploy tool** (`deploy/tool.py` + its registered carrier
  modules — roster in `deploy/manifest-v*.yaml` `carriers:`, enumerated in Ch2/Validators) is the
  **versioned orchestrator across them** —
  it reconciles **four of the five** channels (all but the browser boot) into a consumer at a
  pinned corpus version (ADR-91), behind a per-carrier verify-gate, then records the deployed
  version (Ch6 `deployed_methodology_version`). Two carriers deploy surfaces of their **own**
  rather than one of the five channels: `mesh` (#236, the enforcement-mesh corpus) and `docs`
  ([#280], `ec924ae2` — the hub doc areas: the intake area + `INSTALL.md`);
  a further `editor-config` carrier is manifest-declared but not yet implemented
  (`implemented: false`, v1.4.0). The tool is **not itself a carrier** — it is *how* the
  five are delivered as one gated release; the `floor` carrier also arms the floor under model A
  (ADR-93). Runbook PLAYBOOK §20; proven end-to-end on run #1 (ai-council → v1.0.0).

**Execution substrates (where a session RUNS — not a sixth channel).** The five rows above are
*carriage*: what travels to a consumer. These two are *venue*: where a Claude Code session executes
when it is not this workstation's primary checkout. Neither carries methodology, so neither joins
the channel table — but a map silent on them cannot explain the two contexts in which the channels
above are **inert by design** (the bullet above says so without saying where).

| Substrate | What it is | Why the map needs it | Ref |
|---|---|---|---|
| `.devcontainer/` | the off-machine lane substrate — a container spec plus an idempotent provisioning script, read by a container runtime (Codespaces, or `devcontainer up` on any host) and by **nothing in this repo's gate mesh**. It carries no organ, judges nothing, fires on no git event | it is where the "inert in a fresh clone" bullet above becomes concrete: a fresh off-machine clone starts **shallow, hooks unarmed, `uv` pin unsatisfiable**, so every spine-walking instrument (`validate_no_ff`, `block_ff_push`, `journal_anchor`, `validate_git_backlog`) is unrunnable until provisioning asserts otherwise. The provisioning script exists to close exactly those traps | **ADR-101 amendment 2026-08-18** (the sole directory that amendment admits); `[#554]`; cost/perf memo `docs/audits/2026-08-20-technical-codespaces-audit.md` |
| `deploy/lived_sandbox/` | an operator-invoked deterministic **observer** that spawns a headless `claude -p` session under an isolated `CLAUDE_CONFIG_DIR`, inside a `mkdtemp` clone, and verdicts **enforcement-in-effect** from transcript events + hook stdout + git state — never from the session's narration | it is the only organ that measures whether the carried methodology actually *engages* in a consumer-shaped session, rather than whether it is *present*. Ch3's axis table has no cell for its shape — deterministic observer over an LLM stimulus — which is the honest gap, recorded rather than smoothed | Fable architecture review 2026-07-04 §6 (Slice A isolation proof); `[#252]` (Slice B acceptance instrument); Layer-2-safe — every mutation lands under a `_rmtree_guarded` temp root, no live sibling is touched |

**The transfer matrix is the canonical gap map.** Who carries the method, in which of
seven contexts (hub/child CC, hub/child browser, cloud, local, new-repo) — full
12-row × 7-context matrix in
`docs/audits/2026-06-07-methodology-transfer-audit.md`. Headline: friction
concentrates in **one cell-column** — child-repo CC sessions, where the methodology
floor is a *pointer the agent must choose to follow*, not resident text.

**F5 — `methodology_surface` zone (ADR-78).** What may travel to a child floor is a
verifiable register, not editorial judgment: **whitelist** = prompt-header,
valve-discipline, cadence, ship-rule, context-budget; **blacklist** = hub BACKLOG,
hub LESSONS, hub handoffs, hub-only ADRs. This bounds the child floor (Ch5 zone
register).

---

## Key conventions & zones

**Chapter 5 — Zones & immutability.** The conventions that decide what may be edited,
and the zones where edits are blocked outright.

**File lifecycle** (ADR-39) — the disposition that decides what may be edited:

| Class | Files | Rule |
|---|---|---|
| Append-only | `LESSONS.md`, `logs/TOKEN-LOG.md` | only append; never edit old entries (LESSONS.md may relocate an older block byte-identical to `LESSONS-legacy-<span>.md` — ADR-29 amend. 2026-07-17; TOKEN-LOG strict) |
| Append-only (newest-first) | `JOURNAL.md` | prepend at session/day close |
| Immutable | ADRs, transcripts, handoffs, audits, research | supersede via new file / in-file marker; never edit in place |
| Living | `README.md`, `VISION` (superseded by README, relocated to `docs/archive/VISION.md` at the hub — [#614] lane-e-5, ADR-114 — still tracked), `ARCHITECTURE`, `CLAUDE.md`, `AGENTS.md`, `PLAYBOOK`, `ESSENTIALS` | update in place when reality shifts |
| Generated | `BACKLOG.md` | **never hand-edit** — edit `tasks/`, then `scripts/gen_task_tree.py --emit-source` (ADR-107 §7.2 flip, [#439], 2026-07-28; source zone below) |

**Filenames.** `ADR-NN-topic.md` (ADR-34); `council-out-YYYYMMDD-HHMMSS-topic.md`
(Council CLI); `YYYY-MM-DD-slug.md` for dated artifacts; ALL-CAPS for top-level
governance markdown (ADR-59). **Scope tags** `<!-- scope: X -->` are informal metadata
only (ADR-27; enforcement withdrawn ADR-48).

**Archive-inside-each-folder (operator ruling 2026-07-22).** A terminal-status artifact
relocates **byte-identical** to its own folder's `archive/` (`docs/intake/archive/` —
CONSUMED|REJECTED; `docs/decisions/archive/` — Superseded/Deprecated ADRs); live files
stay put. Relocation is not an edit (the LESSONS-legacy precedent); the ADR-101 genre
seal is unaffected (an `archive/` nests *inside* a sanctioned genre). Manual for now —
the status-coupled validator is wave work (BACKLOG W3 seed 2; spec
`docs/audits/2026-07-23-technical-status-enum-reconcile.md` §4 — the enums themselves
are deployed, [#398] closed 2026-07-23). `logs/`
artifact naming: CLAUDE.md §9 ([#395] convention).

**Source zone — `tasks/` (ADR-101 amendment 2026-07-27; [#433] STEP 1–2, [#439] STEP 3).**
A top-level tree of per-task `.md` files + `manifest.json`. Since the **2026-07-28
source-of-truth flip** (ADR-107 §7.2, executed by [#439]) **`tasks/` IS the source of
truth and `BACKLOG.md` is generated from it** — the arrow used to point the other way, and
anything describing the tree as "derived" predates the flip. The source is **both**
artifacts: each task file's **body** is the authoritative task line, while its
**frontmatter is derived from that body**; `manifest.json` is the residue carrier holding
every non-task prose line in order, so document structure lives there.

Regenerate `BACKLOG.md` with `scripts/gen_task_tree.py --emit-source` after any edit under
`tasks/`. `--write` still exists but runs the **import/recovery** direction (file → tree)
and, since [#474], **refuses against a populated `tasks/` tree** (post-flip it overwrites
source from a generated file — warn-then-destroy inverted to warned-means-abort); `--force`
is the loud, named escape hatch, and the clean bootstrap state is unchanged. **`--prune` is
refused**: deleting a task file would delete source and free its id for re-issue, so
retirement drops a task's node from `manifest.json` while its file **remains as the
allocation record** (ADR-107 §6.3, retire-not-delete). **Limit:** the gate REDs a
re-issued id while the retired record is present, but **cannot detect that record being
deleted** — nothing declares which files ought to exist — so the ledger is not
tamper-evident; a tombstone record is [#440], and ADR-107 §6.3 already records the
directory as "not complete today".

`BACKLOG.md` is **not decommissioned** — it stays on disk byte-identical, so every gate
reading it (`doc_rot`, `validate_backlog`, the commit-msg hooks, `propose_closures`) is
unaffected by the flip. It is **excluded from prose-edge scanning** as the generated side
(the #335 class: scanning both re-mints every BACKLOG edge twice).

**Enforcement (armed, and it was a precondition of the flip, not a follow-up).**
`audit.py::check_task_tree_coherence` ([#433] C1) invokes `gen_task_tree --check` as an
ALL_CHECKS ship-gate leg, so this zone satisfies the chapter's "no organ = decoration"
test. Three legs: manifest structure resolves; **every task file re-renders byte-identically
from its own body** (frontmatter honesty — the leg the flip made necessary, since derived
metadata sitting in a source file is otherwise editable, inert and silently wrong); and the
full reassembly equals `BACKLOG.md` on disk. Arming preceded flipping deliberately: a stale
*derived* tree is merely wrong, a stale *source-of-truth* tree is a corrupted record.
**Honest scope limit:** the check compares the two artifacts against each other, so it
cannot detect a consistent rewrite of both together; source integrity rests on a clean
`git status` plus the manifest's `generated_sha256`.

**Zone register (ADR-75).** Exclusion/immutability/scope policy lives in one
amendable register; **"no organ = decoration"** — every zone is backed by a
fail-closed organ on the executing path, or it is not active:

| Zone class | Pattern | Enforcing organ | Ref |
|---|---|---|---|
| P0 exclusion (path-write) | any path containing `OneDrive - Blue Yonder` | `block-onedrive.ps1` (global PreToolUse) | ADR-75, P0 |
| Immutable-paths | `docs/decisions/transcripts/**` | `block_immutable_edits.py` (hub PreToolUse) | ADR-77 |
| `methodology_surface` (content-scope) | child-floor whitelist / F5 blacklist | `audit.py floor_integrity` (hash + F5 grep + pointer-existence) + child `.sha256` hook + `/ship` gate | ADR-78; hub shipped #121 |

→ Output-formatting render-layer convention (flat + code-fenced for operator copy-out):
CLAUDE.md §4; PLAYBOOK §8. Canonical docs are LLM-first — Mermaid left them; the ADR-51 v2
Mermaid theme is re-scoped to the visualization surface (ADR-51 amendment 2026-07-05).
Auto-TOC: ADR-51.

---

## Verification mesh and decision flow

**Chapter 6 — Verification mesh & decision flow.** How checks layer from cheap-local to
unattended-cross-repo, and how a contested need becomes binding doctrine.

**The methodology engine (the loop).** The repo is a feedback engine, not a static
library — each stage feeds the next and the loop closes:
`Lessons (LESSONS.md)` → `Decision/ADR (docs/decisions/ + Council)` →
`Conventions (PLAYBOOK / ESSENTIALS / CLAUDE.md)` → `Enforcement (audit.py + hooks)`
→ `Dissemination (conformance audit to child repos)` → *(run in live sessions → new
friction)* → back to `Lessons`. The two frontier stages — **Enforcement** and
**Dissemination** — are where active work concentrates (VISION; ESSENTIALS "Feedback
Loop").

**The verification mesh** — layered checks, escalating from cheap/local to
unattended/cross-repo. Each layer is a different *dimension*, so a green one and a red
other are both correct:

| Layer | Organ | Dimension checked | Posture |
|---|---|---|---|
| In-session | `verify` skill (pytest + ruff + git) | does this step pass its gates | per numbered step |
| Pre-merge | `/codex-review`; `/ship` gate | code-diff correctness; branch→`--no-ff`→clean | operator-invoked |
| Post-merge (server) | `report-only-wall.yml` (GitHub Actions) | **what actually landed on `main`** — **three measured legs**, re-run off-host on a full-depth clone (`pytest` — not a hook at all —, `audit.py health`, and the anchor backstop). **NOT** the whole gate set: exactly **two** pre-commit-managed hooks have a server-side counterpart (`audit-health`, `block-unanchored-push`); every other gate — `ruff` among them — is not re-run, so a `--no-verify` push carrying a ruff violation still leaves no server record. Read the gate count off `ecosystem/doc-counts.md`, not off this cell (it said "`ruff` and 13 others" against a live 17−2 = 15). (LA-3, corrected 2026-08-07 — this row previously said "the client-side gate set", which over-claimed.) Widening it to a fourth `pre-commit run --all-files` leg is an open ticket, not an oversight: it changes what the record MEANS | report-only; records, never blocks |
| Nightly (cloud) | conformance Routine | **claims-vs-docs** coherence (own repo) | read-only + skeptic |
| Nightly (local) | `fleet_health.py` / `audit.py run` | structural + **freshness-stamp** health (repo + siblings) + the **operator-load funnel gauge** (`[load]`, [#270]: `collect_load`/`load_line`, `fleet_health.py:610,642`; trend in `logs/OPERATOR-LOAD.csv`) | deterministic, fail-soft |
| Funnel | `surface_triage.ps1` + morning triage | operator ratifies findings before they bind | human gate (#123) |

The 06-07 cloud digest `0/0/0` while the local baseline shows one `canonical_freshness`
FAIL is **not** a contradiction — different *dimension* (claims-vs-docs vs
freshness-stamp) and *scope* (hub-self vs corp-sibling, #100). Per-tier value =
findings-acted-on vs noise, reviewed in the funnel (PLAYBOOK "What each tier checks").
The end-to-end **delivery loop** — the gates above in shipped sequence, with
discharge-with-evidence at close — is PLAYBOOK §21 "The delivery loop (end-to-end)"
(codified 2026-07-22, [#386]).

**Deployed-version record (`deployed_methodology_version`; ADR-91).** Each repo's deployed
methodology-corpus version is recorded in the committed `ecosystem/deployed-versions.yaml`
(the `tool-versions.yaml` durable-version pattern — committed · written-by-command ·
read-by-a-check), **written only by the deploy runbook's per-carrier verify-gate** — the
record lands iff every carrier verifies (ADR-92; Ch2/Ch4). The reader
`audit.py deployed_methodology_version` reports it per repo (`n/a` until a release is
tagged+deployed → `pass` once set), surfaced via `fleet_health` — the version-aware successor
to a raw commit-count drift signal.

**The nightly outcome loop — BROKEN AT THE TRIAGE EDGE. Do not read the table below
as live.** The loop had three stages: producer (cloud Routine) → triage (a GitHub
Action) → consumer (`SessionStart: surface_triage.ps1`). **The middle stage is dead.**
The `nightly-conformance-triage` Action was retired by `82227f08` (`.github/` deleted),
merged to `main` at `57ae83a6` under [#255], because a PR-triggered organ under a
local-merge workflow was vacuous — it never fired. **Date, stated precisely:** both commits
are dated **2026-07-08**; the retirement is labelled **2026-07-09** everywhere it is cited
(`surface_triage.ps1`'s own header, [#428], ADR-105 §Context) after the `chore/session-close-0709`
arc that carried it. The commits are the harder evidence; the 07-09 label is recorded here so the
two are not read as a contradiction.

What that leaves, and why it is worse than a cleanly-removed loop:

**The two upstream stages are different organs, and only one died** — keep them apart or
the `ARMED (stale input)` status in Ch2 reads as a contradiction:

- **Stage 1, digest producer — ALIVE.** The cloud Routine still emits a digest nightly
  onto `claude/conformance-*` branches (live list: `git branch -r | grep conformance` — naming
  one dated branch here rots within days, and the branch this line used to name,
  `origin/claude/conformance-2026-07-26`, is long gone). Nothing merges or reads them — the ADR-105 precipitating evidence: the 07-21
  High finding F1 was fixed on `main` by a session that never opened the branch that
  found it, so the finding's second half went unfixed as a direct result.
- **Stage 2, triage / Issue producer — DEAD** since 2026-07-09 (above). This is the
  organ that turned a digest into a diverted record and an Issue. Nothing has replaced
  it: no digest is diverted, and **no `nightly-triage` Issue has been opened since**.
- **Stage 3, consumer — ALIVE, surfacing a frozen backlog as if it were current.**
  `surface_triage.ps1` reads open `nightly-triage` Issues and prints
  `[triage] N nightly finding(s) await` at every session start. Those Issues are
  **historical artifacts of the retired Action** — currently **15 open, the newest opened
  2026-06-25**, none of which any live organ produced or can close. The hook is healthy;
  its input is a fossil. Filed as **[#428]**.

So `ARMED (stale input)` on the Ch2 `surface_triage.ps1` row means: dead **Stage-2**
producer, not the still-running Routine.

The table below is the **retired** Action's behaviour, kept as the record of what the
severed edge did — not as a description of anything that runs:

| Digest state | Action behaviour (RETIRED — `82227f08`, 2026-07-08) |
|---|---|
| clean (`survived=0`) | divert the digest to `automation/conformance-digest` + close the PR (delete its branch) |
| findings (`survived>0`) | divert the digest (it is the record, on the branch) + open a `nightly-triage` Issue |
| anomalous (diff ≠ one ADDED digest file) | guard FAIL — nothing recorded, open an `Anomalous nightly PR` Issue |

(ADR-72/76/80/84; ADR-105 §Context; [#428]. CONTRIBUTING's "Nightly outcome management"
section described the retired Action in the present tense — naming
`.github/workflows/nightly-conformance-triage.yml` as the organ that "handles the morning" —
until **[#503] reconciled it on 2026-08-06**; it now records the retirement explicitly, so
both sides of that severance finally agree. The standing "do not follow it as live guidance"
warning is retired with the defect it named.)

**`.github/` returned 2026-08-06 ([#501]) — for a different organ, on a fixed trigger.** The
retirement above stands as written: the `nightly-conformance-triage` Action *was* vacuous, and
`82227f08` was right to delete it. What returns is not that organ. The report-only wall
(Ch2) triggers on `push`, which is the exact defect that made the predecessor never fire under
a local-merge workflow — so this is a correction of the trigger, not a reversal of the [#255]
judgement. Two things follow, and they are easy to conflate:

- **Stage 2 of the nightly outcome loop is still DEAD.** The recorder does not divert digests,
  does not open `nightly-triage` Issues, and does not close them. [#428] is untouched, and
  `surface_triage.ps1` keeps its `ARMED (stale input)` status for exactly the same reason.
- **A green badge on this workflow still means nothing about the checks.** It means the record
  was written. The verdict is in the job summary table, never in the badge — the wall states
  this in its own summary text so a reader cannot take the badge for a pass.

**Requirements intake (upstream of decomposition; ADR-98).** Operator intent →
`gen_handoff.py --mode functional` boots the intake-capture chat → confirm-gated intake doc in
`docs/intake/` (WHAT/WHY; acceptance criteria copy verbatim into the epic UAT) → technical-architect
triage → BACKLOG epics / ADRs. Format + lifecycle: `docs/intake/README.md`; chain documentation:
PLAYBOOK Part II §2; boot contract: HANDOFF_PROCESS §16.

**Decision flow (how a contested need becomes binding doctrine).**
`Council brief (ephemeral)` → `ai-council debate (5-provider, blind vote — ai-council ADR-03)`
→ `canonical transcript (ai-council/output/ — the routed-mirror retired 2026-07-22, ADR-43 amendment 2026-07-23; hub archive deleted)` → `operator
distils an ADR` → `BACKLOG item + convention edit` → `enforcement organ (Ch2)`.
Runbook: `protocols/AI_COUNCIL_PROCESS.md` (ADR-67). The complexity router (1-file
mechanical → conversational; 3+ files / 2+ packages → formal CC prompt;
architecture/contested → Council) is PLAYBOOK "Project complexity bands"; degraded
context → Handoff v6 (`protocols/HANDOFF_PROCESS.md`, ADR-82).

**ADR-68 supersession note (the night-agent).** ADR-68 specified a **local**
mechanism — Windows Task Scheduler → headless `claude -p` review → morning briefing,
in ephemeral read-only worktrees. That local job was **never registered as a
scheduled task**. In reality the recurring unattended review ships as the **cloud
Routine + spec-orchestration** described in Ch3/this chapter (the nightly-conformance
arc). ADR-68 is **immutable** — superseded-in-reality, noted here and in Governing
ADRs, not edited. **The local track has no live backlog home:** this line said it
"survives as BACKLOG **#85**", but #85 was closed on **2026-06-07** (`cb59705b`, wave-A
closeout) and no `tasks/` allocation record for it exists — the pointer had been dead for
two months. The surviving record is the evidence, not a row: `docs/audits/2026-06-05-living-doc-staleness.md`;
LESSONS/JOURNAL 2026-06-05.

---

## Governing ADRs

The governing decisions, grouped by area — **curated, not exhaustive**; the complete
ledger is `docs/decisions/README.md`. Council transcripts: the in-hub archive
(`docs/decisions/transcripts/`) was **deleted 2026-07-22** (operator ruling — decisions
live in the ADRs; git history retains; the ADR-77 guard stays armed, Ch2).
(Most-recent five are mirrored in CLAUDE.md §11.)

- **ADR-27/48** — scope tagging: vocabulary retained, enforcement withdrawn (informal metadata).
- **ADR-28** — three-layer architecture (Ch1).
- **ADR-29/39** — file lifecycle: append-only + immutable invariants (Ch5).
- **ADR-30** — default branch `main` for all repos.
- **ADR-31/36/63/69** — authority model (prescriptive + conformance audit); read-only auditor; asymmetric review authority; cross-repo audit reach (Ch1/Ch6).
- **ADR-33/34/38** — VISION universalization; filename convention; universal repo baseline (tier gating removed, A5/A6).
- **ADR-43/67** — Council transcript routing (re-scoped by the 2026-07-23 amendment: routed-mirror clause retired, canonical-only output in ai-council); AI-Council process operationalization (Ch6).
- **ADR-50/51/59/60** — machine-document encoding; ARCHITECTURE convention + auto-TOC (Mermaid left canonical docs — LLM-first compact-text codemap, theme re-scoped to the visualization surface; ADR-51 amendment 2026-07-05); visual repository pattern; docs/ taxonomy.
- **ADR-53/54** — CLAUDE.md as single canonical agent file; Codex reviewer config as global standard.
- **ADR-61/62/82** — git worktree for parallel sessions; Handoff v4 ratification (ADR-62), superseded by v5 (ADR-82, canonical 2026-06-11).
- **ADR-64/65/66** — BACKLOG architecture / done-item disposition / story-map hierarchy.
- **ADR-68** — autonomous overnight review agent. **[REFUTED — historical]** — the *local* night-agent was never registered; superseded in reality by the cloud Routine (see Ch6 supersession). Immutable, untouched.
- **ADR-70/74/80** — three-tier process automation; layer→job matrix (canonical); two-tier adoption + writer policy + Routine/night operational standard (Ch2/Ch3).
- **ADR-71/72/73** — doc-tooling source-repo distribution; cloud-Routine hub-independence; per-repo orchestration distribution (Ch4).
- **ADR-75/77/78** — exclusion-zone register; immutable-paths zone class; child methodology floor + `methodology_surface` zone (Ch5/Ch4).
- **ADR-76** — local fleet-baseline host (Task Scheduler → Python; no LLM on path).
- **ADR-79** — browser methodology carrier: bundle-only; Projects deferred (Ch4 — the browser *channel* in today's vocabulary; "carrier" in the ADR title predates the deploy carrier-module set). **Its bundle-delivery half is superseded by ADR-82** — the thin browser boot replaced the consolidated bundle; the Projects-deferred half stands. Immutable, untouched.
- **ADR-84** — automation-writer isolation (Q9): both writers commit only to dedicated `automation/*` branches (never `main`); the `no_ff_merges` automation exemption removed — one rule (Ch3/Ch6).
- **ADR-85/86/87** — session-lifecycle enforcement (deterministic session-end Stop-gate; un-gameable JOURNAL commit-SHA anchor); conformance-dashboard location (`ecosystem/conformance.md`, ADR-80 committed-generated zone); Architect↔CC equilibrium contract (conditional intent-only prompting) (Ch2/Ch6).
- **ADR-88/89** — file-oriented dependency management (repo files are the dependency unit; declared edges held by machinery, not memory) and computed code-dependency edges (declare-what-you-cannot-compute; Pyright reverse-dependency oracle) — both Accepted 2026-06-21 (`911b561`); ADR-88/89 in-place markers (Ch5/Ch6).
- **ADR-90/91/92/93** — doc→code resolver-allows-N (a rule declares its expected `# rule:` site count in `multi_site:`; Ch2/Validators); methodology-corpus versioning (semver + a git-tag release marker; the `deployed_methodology_version` record, Ch6); deploy-runbook doctrine (a versioned, verification-gated deploy tool + a carrier-module set that keeps outgrowing any number written into prose; ADR-92's body says "four hard-coded carriers", corrected by its **2026-07-25 in-file amendment marker** (`ADR-92:95`, operator-ruled — body preserved verbatim per ADR-94). Read the live roster off `deploy/manifest-v*.yaml` `carriers:` (v1.4.0: seven declared, six `implemented: true`, `editor-config` false) — operator-run from the hub; Ch2/Ch4); floor provisioning model A (commit + two-leg hash-guard the ADR-78 floor; Ch2 arming / Ch4 floor carrier) — Accepted.
- **ADR-98** — requirements-intake pipeline: functional/technical/developer modes turn operator intent into a decomposed epic set (Ch5 requirements intake).
- **ADR-101** — hermetization: sanctioned top-level set, per-class name grammar, refusal gate (`validate_hermetization.py` pre-commit; Ch2/Ch5).
- **ADR-102/103** — parity-surfaces axes: enforcement-gate-rev modeled separately from corpus `source_tag`; per-entry ownership `{value, reason, provenance}` classification (fleet_parity organ row, Ch2).
- **ADR-104** — fleet repository shape: **PARTIAL fold on engineering grounds, polyrepo mostly retained** (the fleet's first shape ADR; corp-monorepo permanently OUT, incremental consolidation). Declares the fleet as 9 git repos — the widest of this file's three denominators (Purpose). **No fold executes on this ADR**; execution is the downstream chain #382 → #383 → #385. Closes [#381] — Accepted 2026-07-24.
- **ADR-105** — routine consumer declaration: a six-field row shape, **gated at ACTIVATION not at filing**. A declared routine must name a `consumer` and a `consumption_path` (the `routine_consumers` organ row, Ch2). Answers [#419] (*we run routines whose output nobody consumes*), which stays OPEN; the live-routine retrofit is [#426] — Accepted 2026-07-26.
- **ADR-106** — environment isolation via `uv`: pinned toolchain (`required-version == 0.11.19`, a uv upgrade is its own gated change), committed `uv.lock` + `.python-version`, and every gate invoked through `uv run --locked` so the gate environment is *declared* rather than per-machine folklore. Closes two defect classes — environment/test isolation and gate reproducibility. Fleet rollout is **gated per repo**, never a bulk sweep; the hub went first ([#432]). The ADR-101 amendment 2026-07-27 sanctions `uv.lock`/`.python-version` in the top-level set (Ch5) — Accepted 2026-07-27.
- **ADR-107** — BACKLOG restructure: **build-thin engine, fleet-owned schema, viewer slot declared EMPTY**. Rules the architecture only — it authorizes no execution, and gates the source-of-truth flip on **two** preconditions (the ADR Accepted **and** the `tasks/` coherence gate armed). Both held on 2026-07-28, so **strangler step 3 executed under its own contract as [#439]**: `tasks/` became the source of truth and `BACKLOG.md` became generated (Ch5 source zone). Amends ADR-65 narrowly — a retired task keeps a minimal allocation record so its id is never re-issued (**retire, never delete**). **Step 4 (prose relocation + the genre-lifecycle leg) stays explicitly DEFERRED**, and the viewer slot stays parked empty behind four re-entry criteria; [#433] does **not** close on this ADR (§6.2's generalization obligation is undischarged) — Accepted (ratified) 2026-07-28.
- **ADR-108** — decision-routing doctrine + standing engineering standards (ratifies intake #22 §A + §B by **promotion**, the intake doc stays SEED): the operator rules FUNCTIONAL questions only; the architect rules TECHNICAL questions in its own lane (decide → record → revert-if-wrong; no operator option-menus); AI Council is the distillation organ for genuinely contested technical decisions. Doctrine only — no organ, no execution — Accepted 2026-07-31.
- **ADR-110** — parallel multi-agent execution: the batch protocol as **versioned artifacts**
  (a manifest committed at dispatch, a packet at close), and the exemption that lets a merge
  queue run while a batch is open. The exemption is scoped to lane branches the batch declares
  and **does not reach `claude/*` cloud lanes** — Accepted 2026-08-06.
- **ADR-111** — the finding pipeline: every audit finding is triaged into exactly one of four
  outcomes, so a finding cannot be left in an undeclared state — Accepted 2026-08-09.
- **ADR-109** — fleet desired-state contract v1: one typed, versioned, queryable schema (`ecosystem/schema/desired_state.py`, the Terraform *model* — declarative typed data, state in git, apply = the existing regenerate-and-diff machinery) over the hand-divergent registries; `ecosystem/registry.md` **loses authority** (§2 — file retirement is loader-wave/[#383] work; [#455] moot); intake #22 §E transcribed as the functional requirement. Downstream consumers [#383]/[#385]; ARCHITECTURE organ-class prose is [#459] — Accepted 2026-07-31.
- **ADR-112** — two-tier adoption bar: adoption runs at two tiers by CODE IMPACT, not artifact
  format. Tier L (libraries/code) stays measured-divergence evaluation, ADOPT/REJECT on numbers,
  consuming a gap-week slot. Tier S (skills/plugins/commands) is install → 30-minute sandbox try →
  KEEP or DELETE → one ledger line — no evaluation ceremony, **no births**, keeping trials out of
  the open-set BACKLOG arithmetic — Accepted 2026-08-12.
- **ADR-115** — **`AGENTS.md` is the portable instruction layer**: ADR-53 Decision 2 (CLAUDE.md as the single agent-instruction file) is **superseded**, and the ADR-101 Tier-1 file class amended in the same act to admit it. Consequence for this map: §10's *"Narrating or managing AGENTS.md"* anti-pattern in `CLAUDE.md` was false doctrine on landing; `[#577]` **discharged it** in the batch-1 L1 lane (CLAUDE.md §12 v2.68) — the bullet was replaced in lockstep with `templates/claude-regions/antipatterns-universal.md` under register licence Z-G2, and §10 now carries the anti-pattern that is actually live (copying `CLAUDE.md` wholesale into `AGENTS.md`, 43.50 KiB against a 32 KiB cap). This map named `[#577]` as an open owner until 2026-08-29 — Accepted 2026-08-25.
- **ADR-114** — root `README.md` recreation — **Accepted 2026-08-29** (AMENDMENT 1), superseding the 2026-08-22 park: *"VISION.md is superseded by a recreated root README.md."* Consequence for this map: `README.md` is a sanctioned Tier-1 file and this repo's canonical front door; ADR-38 A5 is superseded in that single respect; `CLAUDE.md` §5 rule 5's *"do not recreate it"* is retired. **What the ruling did NOT move, and the map must not imply it did:** `VISION.md` stays tracked fleet-wide; this line previously read `{hub: MUST, consumer: MUST}` on "the nine ADR-104 members" — both halves stale as of this pass. `ecosystem/parity-surfaces.yaml`'s `canonical-doc-vision` row demoted to `{hub: SHOULD, consumer: SHOULD}` on 2026-08-31 ([#614] lane-a, once `canonical_docs.CANONICAL_MANDATORY` dropped it), and the tracked-member count is re-measured at **eight** of the nine ADR-104 members (`terminal-setup` has never carried one), not all nine. The ten `canonical_docs.py` constants still name it. **At the hub itself, `VISION.md` is now relocated** to `docs/archive/VISION.md` (`git mv`, byte-identical, [#614] lane-e-5, 2026-09-01) — the hub's own step one of ADR-114 option (C)'s sequenced nine-repo filename migration; the remaining eight members' migration stays open. Executed at the hub by `[#614]`.
- **ADR-113** — the **L0–L5 maturity ladder is ratified vocabulary**, and it is **one of three "L"
  namespaces, not the only one**: the maturity rung, the ADR-28 architecture layer (L1/L2/L3), and
  the distribution layer of Ch2's Layer column (L0 = global `~/.claude`) are distinct axes that
  share a letter. Ch3's L0-boundary declaration turns on that distinction — Accepted 2026-08-19.

---

**Maintained by:** Rob
