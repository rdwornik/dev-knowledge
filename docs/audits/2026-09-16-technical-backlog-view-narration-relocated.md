# BACKLOG view narration relocated — ten prose blocks out of `BACKLOG.md`, and the growth finding the pass uncovered

**Consumers:** `[#589]` (owns the `BACKLOG.md` view and its byte bar) · `[#807]` (filed by this pass) · `[#731]` · `[#754]` (both corrected by it)
**Base:** `main` at `3d435d36` · branch `worktree-backlog-narration-relocation` · one commit.
**Ruling:** operator, 2026-09-16 — relocate the ten blocks, pointer at each site; §8 BINDING pointer carries the rule itself; no row closed, no ceiling raised.

---

## 0 · The finding — the defect is the filing-to-closing ratio, not the narration

**Manifest prose has been FLAT since the 2026-09-01 re-baseline while row lines nearly doubled.** This relocation is a one-time recovery of ~25 KB against a growth rate that will refill it.

```
                         2026-09-01 re-baseline ([#589])   2026-09-16 at 3d435d36
row lines                32,383 B (223 rows)               61,436 B (361 rows)
non-row prose            37,893 B                          38,525 B
total                    70,276 B                          99,961 B
```

On 2026-09-16 alone, before this commit, **10 rows entered the view and none left** (`main` first-parent: 351 rows / 98,090 B at `49143eb3` → 361 rows / 99,961 B at `3d435d36`; entered: 789, 791, 792, 800–806; `[#790]` was filed and superseded the same day and never rendered). The operator's ruling cited "four filed and none closed"; the measured figure is ten. The prose did not grow the file — the rows did. The fix that lasts is `[#731]`'s enforced closure budget, not a recurring narration drain.

## 1 · Why the earlier drain bought zero bytes — confirmed from the code

- `scripts/gen_task_tree.py::render_view` emits every `{"prose": ...}` node of `tasks/manifest.json` **verbatim**, and for each task node only `project_row(...)` — band, title, pointer. No body text reaches `BACKLOG.md`.
- `scripts/archive_row_body.py` relocates clauses inside `tasks/<id>-*.md` **bodies**. It therefore cannot move the view, by construction.
- Witness: the 2026-09-14 paired run — 60 rows relocated, `BACKLOG.md` 91,514 B before and 91,514 B after (`docs/audits/2026-09-14-technical-lane-y-754-backlog-to-bar-evidence.md`).
- The view's non-row mass is manifest prose: **data**, removable by a manifest edit. The instrument was aimed at the wrong corpus — filed as `[#807]`; `[#731]` and `[#754]` repeated the wrong explanation and are corrected in the same commit.

## 2 · Before / after

```
                    before (3d435d36)   after (this commit)
BACKLOG.md bytes    99,961              75,143
row count           361                 362   (+[#807]; no row closed or retired)
row-line bytes      61,436              61,663
non-row prose       38,525              13,480
vs 100,000 ceiling  +39                 +24,857 headroom
vs 72,000 bar       -27,961             -3,143  (not the target of this pass; the rest is row count)
```

Pointers cost 1,509 B more than the Phase-1 projection (73,634 B + the new row): each carries the destination path and a description, and §8 carries the full BINDING rule (571 B) by ruling.

## 3 · Method

- **Reader:** `agy` 1.2.3, model `gemini-3.1-pro-high`, reader role, stdout-only, one serialised run (232 s, 54,950 input tokens — in scope for a ~100 KB file; tree clean after). Every locator it returned was re-checked against the view by this seat.
- **Four agy verdicts overridden**, each because a gate reads the block — a block a gate reads is data, not narration: `Big picture` and `Themes (backbone)` (read by `scripts/validate_backlog.py`, `scripts/audit_checks/check_canonical_structure.py`, `tests/test_validate_backlog.py`) and `Grooming log` (read by `validate_doc_rot._latest_groom_date`) — KEEP; and the ARC-5 blocks agy kept as "binding" were judged by this seat on their content (unchanged since 2026-07-28, carried work already ticketed).
- **Kept in place** (the view needs them): the title and generated-view marker; every theme/story heading and its story line (a row's theme is positional); `[E9]` Source; `[E9]` "The brake is DISCHARGED" (still gates open `[#385]` on open `[#383]`); About this file; Grooming log; dividers.
- **Destination:** `docs/audits/` (immutable, referentially protected per ADR-100), not `docs/archive/`, whose README defines it as a triage queue defaulting to deletion.
- **Byte identity:** each section below is the block's manifest prose nodes joined by `\n`, between START/END markers; the sha256 prefix is over exactly those bytes.

## 4 · The ten relocated blocks

```
§1  L202-207    1561 B  sha256:d63762e8cdd1c79a  [S8] Backbone
§2  L465-470    1452 B  sha256:a61d0afab54450ab  [E8] Basis, accretion discipline, source
§3  L471-486    6719 B  sha256:7fe73c5a6624fb3a  [E8] Wave map W1–W7
§4  L487-494     861 B  sha256:351cca051c5cb794  [E8] Seedless waves
§5  L495-517    2848 B  sha256:4483dcc2fc0f73a3  [E8] Closure contract (frozen) and clause (b) rulings
§6  L518-540    1729 B  sha256:79461f09c0a2fa7a  [E8] Metric definition and baseline
§7  L541-569   10020 B  sha256:eefb74e1f774bc48  [E8] DECISIONS dispositioned 2026-07-26
§8  L570-579    1432 B  sha256:9529f791057828a3  [E8] BINDING
§9  L615-616     445 B  sha256:c990e7e9d7f5d024  [S24] Completion notice
§10 L636-637     729 B  sha256:4b503b55d9a6c8e3  ai-council audit residuals
```

## §1 · [S8] Backbone (view L202-207 at `3d435d36`)

<!-- §1 verbatim START sha256:d63762e8cdd1c79a -->
Backbone (dependency-ordered; done stages recorded here as the epic ledger — ADR-65: git is the implementation record, so the DONE stages are narrative, not live task lines):
- Stage 0 — stabilize live (ship-gate GREEN + clean tree). [DONE]
- Stage 1 — fleet blast-radius map (5 organs x 4 consumers classified from live config). [DONE]
- Stage 2 [#235] — Informant Organ: the read-only enforcement-coverage reporter that measures enforcement-in-effect (whether the gate FIRES, not presence — proven by the present-inert->absent / blocking->enforcing-local fixture pair; first live run reproduces the differentiated fleet map, 0 enforcing-local; no organ modified). [DONE 2026-07-03, feat/informant-organ, commits 99401d7/03a3280/07a061a — closed against #235]
- Stage 3 [#236 + sub-item #237] — the mesh carrier (the enforcement-transfer mechanism). Stage 4 [#238] — record + formalize. Follow-ups: Tier-2 breadth #239, audit-leg regression teeth #240. Sequenced-after (off the critical path): fleet rollout n=2+ (#221), each repo gated on the Informant's enforcing-local — only after Stage 3 is proven on n=1.
- FLAG RESOLVED (architect, 2026-07-07): the arc-tracking / record-integrity fold is adjudicated — #168/#170 **co-sequence with #239/#240** (they harden the same `session_end_backpressure` organ the enforcement-transfer epic ports consumer-local in #237); #243 co-sequences there too (its #168-hard vs Fable-WARN conflict resolves at that mesh-consult). #139 **stays separate** (hub record-integrity, tangential — not folded).
<!-- §1 verbatim END -->

## §2 · [E8] Basis, accretion discipline, source (view L465-470 at `3d435d36`)

<!-- §2 verbatim START sha256:a61d0afab54450ab -->
**Why this form (basis).** The plan of record needs a home that changes as waves land. An **ADR is the wrong form** — ADRs are immutable (CLAUDE.md §5 rule 3); only the status line is editable (ADR-94), so a wave map could never be updated in place. `BACKLOG.md` is **living / update-in-place** (§4 File lifecycle) and is already the repo's declared spec surface ("the BACKLOG is the spec; items are tickets"). The live schema is a story map — verified **7 themes / 20 stories / 116 tasks** at filing (ADR-66; `scripts/validate_backlog.py`). So the plan lands as a **theme + stories** here, not an ADR and not a new path. `[E8]` is marked a time-boxed arc, not a permanent mission theme, so it retires when ARC-5 closes.

**Accretion discipline.** The seven waves are recorded as the **wave map below**, not as seven pre-filed stories with placeholder tasks. Each wave's build tasks are filed **when that wave opens**, so this filing adds three carried tickets rather than a speculative +10 — which is what closure criterion (d) below requires.

**Source.** `docs/handoffs/2026-07-20-dev-knowledge-architect-arc5/` (SUPPLEMENT ANSWERS, operator-authored 2026-07-19) ∩ `docs/audits/2026-07-19-technical-night-consolidated-cycle-close.md` §3 (the nine seeds, terra-corrected). Strategic intent, verbatim: **"AUDITS ARE OVER. ARC 5 IS EXECUTION."** Meta-finding the arc closes: *"decision recorded ≠ decision enforced ≠ decision legible."*
<!-- §2 verbatim END -->

## §3 · [E8] Wave map W1–W7 (view L471-486 at `3d435d36`)

<!-- §3 verbatim START sha256:7fe73c5a6624fb3a -->
#### Wave map W1–W7 (ordered by operator pain-priority, not dependency elegance)

**W1 — VISIBLE BOUNDARY** (the "colors"; the operator's most-repeated ask). Build #329/#352: versioned `.vscode` background decoration (grey/navy, dark theme) of `owner=hub` / `owner=repo` regions, deployed fleet-wide as carrier material; plus a sweep completing RULING-S reader-visible universal-vs-repo section headers in every governed file across all three repos. **Done when:** the operator opens any governed file in any repo and SEES which lines are methodology and which are repo-personal. **Deadline:** must land before the P4a `.vscode` ruling shelf-life **2026-08-13**. **SEEDLESS** — see the seedless note below.

**W2 — STRUCTURE EQUALIZATION LEG 2** (the `assets/` folder, mypy, "why do folders differ"). Disposes `ai-council/assets/ruff-pre-commit.yaml` per **R1**; mypy/cache posture per **R1b**; `hub-toc-hooks` resolution (S5 §4.2 — recommended path (b): hub manifest re-scope v1.3.2 matching the hub's own retirement, then prune ai-council + retire corp's waiver); #331 ratification + `parity-surfaces.yaml` consumer-tier rows for the BACKLOG story-map schema + gate; reconcile the corp-vs-ai `validate_backlog.py` fork; corp `deployed-versions.yaml` currency (evidence for #276). **This wave carries consolidated-report seed 5** (consumer parity-surface reconciliation, S5) — mapped by CONTENT, not by label. **[#355] routes here.** **Done when:** each named divergence is either equalized or recorded as a declared, time-boxed divergence; every consumer write goes via RULING-W worktree/branch → report; changes land as manifest/template carrier material (replication-first, not one-off fixes).

**W3 — LIFECYCLE MECHANISMS** (intake→ADR→backlog→close→DELETE — "the process problem"). Carries **seeds 2, 3, 4** + the #269 build. Seed 2: `validate_intake.py` HARD pre-commit gate — closed status enum (+ ratified tech-extension per **R4**), unique `intake-id` (fixes the live id:14 triple collision), required `consumed-by` on CONSUMED, machine-readable `Intake:` provenance on ADRs + citation enforcement (ADR-102/103 backfill or recorded non-intake-origin). **[#398] update (2026-07-23):** the enum is DEPLOYED (README §5 + `gen_intake_index._STATUS_ORDER` + template), the id:14 triple is dissolved, and the R4 tech-extension allowlist is DEAD (rejected by the 2026-07-19 ruling, SUPPLEMENT.md:68-70); the validator's current spec is `docs/audits/2026-07-23-technical-status-enum-reconcile.md` §4 (supersedes night-batch P2c). Seed 3: build #242 (ADR header↔README status reconciliation; ADR-88/89 frozen-Proposed case). Seed 4: `gen_grooming_worksheet.py` + an `audit.py` grooming-cadence/net-delta WARN (witnessed accretion 74→116 in 11 days, ≈3.8/day) + extend `safe_remove.py` M2/M3 as #347's sanctioned REAL-DELETION mechanism per **R3**. Plus #269 (count-tiered audit index, ADR-100). **Done when:** a seeded off-enum status, a duplicate `intake-id`, and an uncited ADR are each flagged with tests; #242 and #269 are built; the grooming worksheet + accretion WARN are live; `safe_remove.py` M2/M3 is the sanctioned deletion path.

**W4 — ARCHIVE LEGIBILITY** (the operator's archiving ask). **R2** decides the shape. Facts already true: file NAMES encode genre+date by convention (`ADR-NN-slug`, date-class-slug audits, date-genre-slug intakes); the ruled convention is stay-in-place (join keys, ADR-101 seal) with status on index surfaces. **Done when:** R2 is ruled AND its build has landed — either (a) the index/status surfaces (seeds 2/3 + #269 + the handoff-README micro-era clause) OR (b) a physical `archive/` with a genre-preserving naming rule via ADR amendment. **NOT both by default; no silent relitigating.** **SEEDLESS** — see the seedless note below.

**W5 — SESSION/WRITE GUARDS** (worktree pain; #353/#344/#349). **This wave carries consolidated-report seed 6** (session-boot + consumer-write guards, S6) — mapped by CONTENT, not by label. Per **R5**, ONE unifying organ: a HEAD-bound operator-authorization token (naming worktree + branch + allowed paths) checked by a `PreToolUse` guard, satisfying #344 Ask-2 (consumer hub-write guard), #353 (boot contract), and the S7 prompt-attestation at once. Plus S6's boot-snapshot `SessionStart` hook, the `.claude/.session-lock` HEAD-movement advisory, #349's close-discipline boot echo, and a signed integration-return token for self-merge detection. **Justification:** six recovered-not-prevented incidents, the sixth carrying a clean reflog trace (a concurrent session swapped HEAD in the primary tree mid-command during handoff generation; no guard fired). **Done when:** the organ REFUSES a witnessed unauthorized write (n≥1 witnessed refusal, not merely installed) — the incident class moves from recovered to prevented.

**W6 — CANON INOCULATION + PROMPT EQUILIBRIUM** (PLAYBOOK/handoff currency). Carries **seeds 1 and 7**. May run FIRST, in parallel, as a doc lane — file-disjoint from W1/W2. Seed 1: transcribe the four un-inoculated rulings (RULING-W · two-tier · worktree side-effect rule · consumer merge-delegation composite) into PLAYBOOK (operational) + ESSENTIALS (one-liner), grep-verified against the ADR amendments; **plus** the staged-diff CO-CHANGE checker (**[#354]**). Seed 7: the 7-item inbound prompt-spec as a PLAYBOOK §2 amendment + a handoff-time self-check probe (**R6** decides hard-probe vs soft). Plus handoff-README micro-era documentation (stage1/stage2 archive class). **Done when:** the four rulings carry PLAYBOOK + ESSENTIALS text grep-verified against their ADR amendments AND the co-change checker flags an ADR-36/41/101 amendment lacking a companion PLAYBOOK/ESSENTIALS edit. *Legibility half already landed at merge `8c913a6a`; the enforcement half is [#354].*

**W7 — TESTING + FLEET STATE** (last, per dependency). Carries **seeds 8 and 9**. Seed 9: dynamic-test evidence gate (code-impact tier in `ship.md` or a versioned `test-harness.yaml`), **WARN-first then FAIL after two demonstrated runs**, depends-on #270; `protocols/AGENTIC_TESTING.md` as #412 config material (re-owned 2026-07-25 — #348 was decomposed to grooming-only; the configured-workflow layer this seed feeds now lives in #412). Seed 8: a scheduled `fleet_collect` PULL collector with watermarks ("silence ≠ absence") subsuming the two reporters; SQL/SIEM stays SHELVED until a witnessed join-pain (**R7** confirms this as the standing answer, matching the intake #14 ruling). **Done when:** the evidence gate is live WARN-first with its FAIL-after-two-runs rule recorded, `AGENTIC_TESTING.md` exists as #348 config, and the collector runs on a watermarked schedule.
<!-- §3 verbatim END -->

## §4 · [E8] Seedless waves (view L487-494 at `3d435d36`)

<!-- §4 verbatim START sha256:351cca051c5cb794 -->
#### Seedless waves (do not read the seed list as the wave list)

**W1 and W4 are the SEEDLESS waves** — neither is backed by a seed from the nine-seed consolidated report:

- **W1** is justified by **operator priority and the 2026-08-13 `.vscode` ruling shelf-life — NOT by audit evidence.** It is first because it is the most visible, deliberately (the operator's frustration is itself context: visible results per wave).
- **W4** owns no seed of its own; it **discharges W3's seeds 2/3** (index/status surfaces) if R2 lands on shape (a). If R2 lands on shape (b), W4 acquires its own build via ADR amendment.
- **Seeds 5 and 6 map to W2 and W5 by CONTENT, not by label** — they are named explicitly in those waves' text above. A reader matching seed numbers to wave numbers will drop them in execution; that is why they are named rather than numbered.
<!-- §4 verbatim END -->

## §5 · [E8] Closure contract (frozen) and clause (b) rulings (view L495-517 at `3d435d36`)

<!-- §5 verbatim START sha256:4483dcc2fc0f73a3 -->
#### Closure contract (frozen — reproduced verbatim)

```
ARC 5 is CLOSED when and only when: (a) the ledger exists as a mechanism, four-state, over
MUST-shaped governed rules — not ADRs; (b) the silently-unenforced count strictly decreases and
everything still unenforced has moved to declared-unenforced with an owner and a review date;
(c) each shipped wave carries a frozen done-contract, a Codex review before merge, an educate
artifact with file-level before→after, and a BACKLOG structural-marker change; (d) backlog
accretion is net ≤ 0 excluding tickets minted by ARC-5's own waves, every open item adjudicated at
least once, and the accretion rate measured and reported; (e) enforcement is witnessed, not
installed — for every guard or gate shipped, a run exists in which it fired or refused; (f) the
operator confirms, per wave, in his own words, that the named pain is gone.
NOT closure: waves merged, ship-gate green, tests passing, items marked done.
```

> **Clause (b) — RULED F1 (operator, 2026-07-27; discharges the R12 fork below).** Clause (b) will be amended to **ratchet + bounded drain**: gate the GROWTH of silent rules (the ratchet — built by [#436], row-independent) *and* drain a bounded slice, rather than dispositioning all 176. The **drain row selection (scope) is still pending** the operator's pick; the drain matrix is **slice × mechanism × owner × review date**. The frozen text above is deliberately UNCHANGED — this records the ruling; the amendment lands with the row selection.

> **Clause (b) — AMENDED (operator ruling D1, 2026-07-28; lands the F1 row selection above).** The frozen contract text stays verbatim — this blockquote is the amendment of record. Clause (b) is discharged by **ratchet + bounded drain**: the ratchet ([#436], BUILT — merge `6195d932`) gates the GROWTH of silent rules, and the **drain slice is [#356] + [#358]–[#361]** (the two still-silent seed-1 rules + the four census escalations; [#362]'s 49 dropped #242 guards are NOT in the slice). **Architect prepares / operator ratifies.** **Review date 2026-08-26.** Matrix unchanged: slice × mechanism × owner × review date. **Recorded, never executed** — this selects the slice; no drain is performed by this entry.
>
> **Operator intent (2026-07-28):** the FULL silent-rule pool (428 @ detector `silent-rule-v4`) is to be dispositioned over time — drained, mechanized, or DELIBERATELY RETIRED as no-longer-valid; staged, wholesale classes post-flip. **Nothing expires by being forgotten.**
>
> **Drain-owed now:** `PLAYBOOK.md:1270`, `REPO_ONBOARDING.md:92`, `REPO_ONBOARDING.md:199` + the 43-line delta per `docs/audits/2026-07-27-census-silent-rule-ratchet-arm-measurement.md`, review **2026-08-26**. **Baseline semantics:** architect-proposed 2026-07-27, operator-adopted (D4), test-and-iterate.
<!-- §5 verbatim END -->

## §6 · [E8] Metric definition and baseline (view L518-540 at `3d435d36`)

<!-- §6 verbatim START sha256:79461f09c0a2fa7a -->
#### Metric definition — the declaration test (operative; governs closure clause (b))

Closure clause (b) turns on the four-state ledger, so the boundary between `silent` and
`declared-unenforced` is load-bearing. Operator-ruled 2026-07-19, recorded verbatim:

```
A MUST-shaped rule counts as declared-unenforced only if the non-mechanisation clause is BOTH
on-surface -- at the rule's own file:line or its canonical PLAYBOOK/ESSENTIALS span, because
`silent` means a reader OF THE RULE cannot tell it is unenforced -- AND bound to an OPEN ticket
naming the remaining work, per ADR-81(d). Neither condition suffices alone. Without the second,
N_silent is gameable by writing 'this isn't enforced' next to every rule.
```

**Baseline — first measurement under that definition, pinned to `bf49cbf9`.** Denominator **320**
MUST-shaped rules · **N_silent 176 (55%)** · **N_enforced 130** · **N_declared 14**. Scope was
`protocols/` + `templates/` + `ecosystem/*.yaml`; `docs/decisions/` is deferred to a second sweep
([#357]), so **176 is a floor, not a total**. N_enforced is deliberately **conservative** — ~55
partial-mechanism rules (one leg gated, the rest not) are folded into `enforced`, and splitting
them strictly would raise N_silent. Controls held: the ADR-template intake-id cite rule and the
merge-delegation composite both measured `silent`; the worktree side-effect rule measured
`declared-unenforced`, having been converted out of `silent` by `8c913a6a` — the canon inoculation
working as designed, not a model failure. **Evidence** — the 176-item itemisation, the declared list, the near-misses, and the pending-#242 per-ADR table are archived at `docs/audits/2026-07-19-census-silent-rule-ledger.md`.
<!-- §6 verbatim END -->

## §7 · [E8] DECISIONS dispositioned 2026-07-26 (view L541-569 at `3d435d36`)

<!-- §7 verbatim START sha256:eefb74e1f774bc48 -->
#### DECISIONS — dispositioned 2026-07-26 (the "ALL UNRULED" claim was true at filing, false since)

Every decision below was **UNRULED as of its filing** (2026-07-19). The recommendations are the outgoing architect's, carried verbatim in substance; **a recommendation is not a ruling.**

> **Disposition sweep 2026-07-26 (intake #17 §5 micro-window).** Each row was re-verified against LIVE state, not against the filing. The table had survived at least one operator ruling by three days.
>
> **Delegation authority for the four RULED rows** — and it is a delegation, not a recommendation promoting itself: the operator's 2026-07-26 micro-window execution order (intake #17 §5) instructed that rows verified still-LIVE be recorded as *"RULED per attached recommendation — operator-delegated 2026-07-26"*. That standing instruction is the ruling record for R1b/R3/R5/R6; the per-row cells carry the LIVE-premise verification that qualified each row for it. R8 was excluded by the same order (his own pick) and R12 has no recommendation to delegate to.
>
> Outcome (final, after two review passes): **1 DEAD-OBE** (R1 — the folder it decides about no longer exists), **3 ALREADY-RULED** (R1b, R2, R4), **4 RULED by operator-delegated adoption** (R3, R5, R6, R7), **1 still open for the operator** (R8 — PARKED, his own pick; **R12 discharged 2026-07-27 by the clause-(b) ruling F1 above**, so the sweep's "2 still open" no longer holds). **All three already-ruled rows went AGAINST their recommendation** — R1b rejected (Pyrefly universal, not a divergence), R2 chose (b) over (a), R4 rejected outright. That is the sweep's most useful finding: where this table had a prior ruling, the recommendation lost 3 times out of 3, so an unverified recommendation is a poor predictor of the operator's call. A ruling here is **recorded, never executed** — each adopted row still needs its build.
>
> **Reconciliation debt this sweep creates — the FULL list, enumerated after sol's adversarial pass found the first version incomplete.** Dependent rows still carry the pre-sweep status and were deliberately NOT reworded (out of this window's two-row edit scope): **`[#389]`** reads "R6 … **UNRULED**; rule R6 first" and gates its own Done-when on it · **W3 seed 2** says "+ ratified tech-extension per **R4**" (already self-superseded later in the same paragraph by the `[#398]` update) · **W4** says "**R2** decides the shape" though R2 is ruled · **W6 seed 7** says "**R6** decides hard-probe vs soft" · **W7 seed 9** says "**R7** confirms". Reconcile each when its wave opens; none is a silent contradiction now that all five are named.

| Ref | Decision | Status (verified 2026-07-26) | Recommendation as filed (NOT a ruling) |
|---|---|---|---|
| **R1** | `assets/` disposition: (a) DISSOLVE — relocate `ruff-pre-commit.yaml` to the canonical config location, delete the folder (RULING-W leg + safe-deletion path); or (b) UNIVERSALIZE `assets/` as a fleet deployment convention | **DEAD-OBE** — the folder is gone. `ai-council/assets/` was dissolved by `6d78851e` (2026-07-21) "dissolve vestigial assets/ and repair its two live references"; `git ls-files assets/` is empty and no `ruff` path remains tracked. Option (a) was executed without the ruling. | **(a)** — one file, no fleet role; (b) would mint a new mandatory folder fleet-wide for no carrier need |
| **R1b** | mypy posture: declare ai-council's mypy a sanctioned divergence vs roll out fleet-wide | **ALREADY-RULED — REJECTED, against its recommendation.** Caught on sol's adversarial pass: a **BINDING** operator ruling already exists and the delegated adoption first recorded here was withdrawn as a relitigation. `docs/handoffs/2026-07-20-dev-knowledge-architect/SUPPLEMENT.md:113` heads the block "BINDING — do not relitigate" and `:119` reads "Pyrefly is universal across the fleet — **NOT** a sanctioned mypy divergence"; `PASTE_THIS.md:528` records "mypy as a sanctioned divergence → **REJECTED by the operator**. Python stack, tooling universal → Pyrefly". The ruling is UNIVERSALIZE, not diverge. (Method note: the first pass searched JOURNAL/LESSONS/docs-decisions and missed it — `docs/handoffs/` carries binding rulings too.) | **Declare sanctioned divergence** |
| **R2** | Archive shape: (a) INDEX-ARCHIVE — status/count-tiered index surfaces, files stay, names already carry genre; or (b) PHYSICAL `archive/` folders with a genre-preserving rename rule via ADR-98/100/101 amendments | **ALREADY-RULED 2026-07-22 — and the ruling went to (b), NOT the recommended (a).** "**Archive-inside-each-folder** (operator ruling 2026-07-22)" in `ARCHITECTURE.md` Ch5 (quote the heading, not a line range — this window's own edits shifted it from :563 to :595); six physical `archive/` dirs exist on disk; applied at `JOURNAL.md:548-550`. The recommendation was not followed — recorded so the divergence is not re-litigated as an open pick. | **(a)** — zero join-key breakage, builds already seeded |
| **R3** | #347 safe-deletion = `safe_remove.py` M2/M3 extension as THE sanctioned mechanism | **RULED per attached recommendation — operator-delegated 2026-07-26.** Premise verified LIVE: `safe_remove.py` exists but is **M1 only** (no M2/M3 in the file), `[#218]` carries M2/M3 and is DEFER, `[#347]` is open and unruled. Recorded, not executed. | **YES** |
| **R4** | Intake enum: ratify the 6 off-canon statuses as a documented tech-genre extension vs reclassify the docs | **ALREADY-RULED 2026-07-19 — REJECTED, against its recommendation** (reclassified from DEAD-OBE on terra review: a decision that was decided is not one overtaken by events). The 2026-07-19 ruling (`SUPPLEMENT.md:68-70`) rejected ratifying the six off-canon statuses outright; W3's `[#398]` update records "the R4 tech-extension allowlist is DEAD", and the ruled enum SEED→DRAFT→READY→{ACCEPTED\|CONSUMED\|SUPERSEDED\|REJECTED} is deployed in `gen_intake_index._STATUS_ORDER`. | **Ratify-with-documentation** — they are functioning plan-of-record artifacts |
| **R5** | Unifying HEAD-bound authorization token as ONE organ for #344/#353/attestation, vs three separate builds | **RULED per attached recommendation — operator-delegated 2026-07-26.** Premise verified LIVE: `[#344]` and `[#353]` are both open, the unified organ is unbuilt, and the only HEAD-bound token in code is `/override`'s `logs/.session-override-token` — a different organ. Recorded, not executed. | **ONE organ** |
| **R6** | Prompt-spec: hard handoff probe vs soft self-check | **RULED per attached recommendation — operator-delegated 2026-07-26.** Premise verified LIVE, against a first-pass misread: `verify_handoff_probes.py` is the **#163 PROBES.md-teeth** validator, NOT the prompt-spec probe R6 decides. No prompt-spec probe exists (`scripts/` has no `prompt_spec`; PLAYBOOK carries no §2 prompt-spec amendment) and W6 seed 7 still reads "**R6** decides hard-probe vs soft". Recorded, not executed. | **Hard probe on the bundle side** — the off-repo prompt itself can't be gated; attestation covers the paste |
| **R7** | Fleet-state: confirm "collector + reporters now, SQLite shelved" as standing | **RULED per attached recommendation — operator-delegated 2026-07-26.** Corrected on sol's adversarial pass: this was first recorded ALREADY-RULED, but the cited authority says the opposite — `docs/intake/2026-07-12-siem-requirements-ruled-pack.md:61` explicitly retains least commitment, "store/viewer class (SQLite vs DuckDB) … are Phase A build decisions, **not settled here**", and FR-18 lives only in the ARCHIVED provenance draft, not the ruled pack. So the shelving genuinely was open and is ruled here by delegation. Live state already matches: reporters on disk, zero `.db`/`.sqlite` anywhere. | **Confirm** |
| **R8** | (carried, corp-side) #38 channel pick: 1 primary-direct / 2 worktree / 3 epic-dev | **UNRULED — stays that way.** The operator's own pick; four exhaustive searches across BACKLOG/JOURNAL/docs found no ruling. Explicitly NOT delegated. | *(none recorded — operator's pick)* |
| **R12** | Closure clause (b) is **not achievable in one arc** at N_silent 176 — "everything still unenforced has moved to declared-unenforced" would require dispositioning 176 rules. Two options: **(i) NARROW** the arc target to a bounded load-bearing slice — the 4 census escalations ([#358]–[#361]) + the 2 still-silent seed-1 rules (RULING-W, merge-delegation, [#356]) + the 49 dropped #242 guards ([#362]); or **(ii) GATE THE GROWTH** of silent rules rather than drain the pool. | **LIVE, and NOT delegable — needs the operator.** Premise verified current: `[#242]`, `[#356]`, `[#358]`–`[#362]` are all still open, N_silent 176 still stands (`BACKLOG:316`, census ledger `:111`), evidence artifact present. But **no recommendation is attached**, so there is nothing to rule by delegation — narrow-vs-gate is a genuine operator choice. | *(none attached — a recommendation is not a ruling)* |

> **Numbering note (2026-07-19):** the census-derived decision above is filed as **R12**, not R9 — the discrepancy below records that R9/R10/R11 never existed in the ARC-5 bundle, and minting R9 now would resurrect a ref the record says does not exist.

> **Discrepancy recorded — the ruling set is R1–R8 (+R1b), nine picks; there is no R9, R10, or R11.** The lane prompt for this filing specified "R1–R11". An exhaustive search of the ARC-5 bundle (`SUPPLEMENT.md`, `PASTE_THIS.md`), all fourteen `docs/audits/2026-07-19-*` night-audit artifacts, and `JOURNAL.md` found exactly the eight R-labels above plus the R1b sub-ruling. The only `R9`/`R10`/`R11` strings in the repo belong to a **different, unrelated R-namespace** (`docs/audits/2026-06-07-methodology-transfer-audit.md`). Three rulings were **NOT invented to reach eleven** — per the filing instruction "do not invent rulings". If the operator holds R9–R11 off-repo, they are missing from every repo source and must be supplied.
<!-- §7 verbatim END -->

## §8 · [E8] BINDING (view L570-579 at `3d435d36`)

<!-- §8 verbatim START sha256:9529f791057828a3 -->
#### BINDING (travels verbatim; do NOT relitigate)

The ARC-4 rulings (RULING-W/S/PY/CF; two-tier "compliance IS authorization" in force now); the terra ×7 corrections as applied; sol's 4 mechanism upgrades as accepted strengthenings; **satellite wave FROZEN** until Wave-1 lessons are extracted; luna's floor-misreport corrected (consumers DO carry the floor, hash-matched — Haiku fan-out is indicative, not authoritative); E1 scope honesty (only two organs were fire-proved this run).

**CONSIDERED + REJECTED:** SQL/SIEM now (premature per intake #14 + S8); a `coherence-nudge` extension for co-change (terra: not implementable — see [#354]); blanket new-path blocking (the two-tier rule supersedes); physical file moves for archival as the default (R2 decides; convention says stay-in-place); more audits (operator: enough).

**DO-NOT-REDO:** the nine seeds' adjudication (terra-corrected kill-candidates stand); the 8-domain gap derivation (sol-triangulated); the ARC-4 equalization values (py311 / 120 / >=0.15.5 / minversion 9.0 — at-parity, verified); the grooming closes #306/#307/#328.

**Per-wave standing requirements** (from the closure contract, applied to every wave): a frozen acceptance contract before delegation · Codex terra review pre-merge · RULING-W for any consumer write · replication material over one-off fixes · an educate artifact with file-level before→after · one wave = one merged arc.
<!-- §8 verbatim END -->

## §9 · [S24] Completion notice (view L615-616 at `3d435d36`)

<!-- §9 verbatim START sha256:c990e7e9d7f5d024 -->
**COMPLETED 2026-08-01.** All tasks closed: [#382] (`0acc3328`, merged `f7abe228`) and [#459] (`bf373b13`, merged `31c80714`). The heading is RETAINED, not deleted — retire-not-delete at story level: a completed story keeps its place in the map so the [E9] sequence stays readable and its id is never re-issued, exactly as a retired task keeps its allocation record (ADR-107 §6.3). FIRST empty story on main — this marker is the precedent.
<!-- §9 verbatim END -->

## §10 · ai-council audit residuals (view L636-637 at `3d435d36`)

<!-- §10 verbatim START sha256:4b503b55d9a6c8e3 -->
**ai-council audit residuals (pointer, not filed here)** — the ai-council audit surfaced ai-council-owned cleanups (stale force-added `settings.local.json` pointing at dead paths; an empty `worktrees/fix/` dir; codemap/backlog-hook universalization gaps). Added 2026-07-06 (Wave-3, root adjudication 5): the relative-path pre-commit source (`repo: ../.dev-knowledge`) makes ai-council's toc-freshness gates layout-dependent — ANY out-of-layout checkout (CI, second clone, another machine) silently loses them (witnessed: the sandbox clone; measurement-3 audit) — decide pin-by-URL+rev vs documented layout constraint. Per ADR-41 routing these are filed in a dedicated ai-council session, not duplicated in the hub backlog.
<!-- §10 verbatim END -->
