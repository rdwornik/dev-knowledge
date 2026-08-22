# CLOUD-WAVE CLOSE — the funnel table

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-22 · **Slug:** cloud-wave-close-funnel
- **Produced by:** the part-D wave-close integrator, primary checkout, `main` after the merge queue.
- **Scope:** every finding, recommendation and residual from **all five** dispatched cloud lanes,
  plus what the integration itself surfaced. Each line is classified into exactly one lawful next
  step and cites the clause that puts it there.
- **Decision tree of record:** ADR-111 §1 (the four outcomes) and §2 (a finding may not become a
  row without triage) · `protocols/STANDING_RULINGS.md` **P-2** (anti-orphan ratification) ·
  **Q6** (contract-as-file) and **Q7–Q9** (the admission instrument).
- **Mapping, stated once so each line can stay terse.** The brief's five labels are the repo's four
  outcomes plus the executed case: MECHANICAL = ADR-111 §1(b) DISCHARGED *with its locator* ·
  ADR / INTAKE = §1(c) CANDIDATE (ADR only where ADR-98 §3's fork test is met) · REJECT = §1(d)
  REJECTED, reason recorded where the finding lives · COVERED = §1(a) OWNED, cite the id and add
  nothing.

> **This table is the deliverable. Nothing below it is filed, ruled or closed by this session
> beyond the MECHANICAL block, which is already executed and carries its locator.** The architect
> returns ONE batched ruling over the ADR / INTAKE / REJECT blocks; D5 executes that ruling.

---

## 0. What the wave actually was

**Four lanes, not five.**

| lane | branch | head | artifact | merged as |
|---|---|---|---|---|
| cloud-3 `[#566]` | `claude/cloud-3-566-axis-lean` | `59dedfdd` | yes | `94821cba` |
| cloud-2 `[#563]` | `claude/cloud-2-563-view-layer` | `b02871c8` | yes | `73d66819` |
| cloud-4v2 | `feat/cloud-4v2-universalization` | `7b16f258` | yes + 2 decision docs | `bb056fe1` |
| cloud-graph | `claude/technical-graph-and-workflows` | `178d6106` | yes (docs-only) | `c584a39c` |
| **cloud-1 `[#562]`** | **none** | — | **none** | **n/a** |

`cloud-1-562-admission-rerun` produced **no branch and no artifact**. Reported, not inferred:
`claude/*`, `docs/*`, `feat/*` and every local and remote ref were enumerated, and every ref's tree
was scanned for a 562/admission file. The only hit is `tasks/562-*.md` — the BACKLOG row itself,
tracked and therefore present on every branch.

**The uv-pin caveat (the R4 precedent) was declared by every lane that hand-ran gates.** Zero
undeclared hand-runs, so that finding class does not recur. cloud-2 went further: it installed the
pinned `uv 0.11.19` mid-session, re-ran the real gate set through its configured entrypoints, and
**corrected its own §7 in an in-file amendment** — including an exit code it had misread because the
command was piped to `tail` before `$?` was read.

## 1. MECHANICAL — executed in this session, each with its locator

ADR-111 §1(b): a discharge is only a discharge with a locator that resolves.

| # | line | origin | locator |
|---|---|---|---|
| M1 | terra **CRITICAL** — the no-leftovers test cleaned up with `ignore_errors=True` and never asserted removal, so a *failed* cleanup passed green while leaving the export behind. Critical Rule #9 requires removal be VERIFIED. | cloud-2, found by this session's terra pass | `a7391b56` |
| M2 | terra **HIGH** — the exporter emitted `default_status` alone while the two lines below it dual-spell `check_active_branches`/`remote_operations` *precisely because* the live Backlog.md file uses camelCase. The key was inert; the default stayed `To Do`, outside the emitted status enum. | cloud-2, terra | `a7391b56` |
| M3 | terra **HIGH** — `check_s10` returned clean whenever the pins it *found* agreed, so deleting two of the three Stage-1 `model:` pins passed — while the artifact claims S10 asserts "all three". Now asserts the pin COUNT; the deletion regression test is **mutation-checked** (assertion reverted → `cpr.run()` returns `[]` → the test REDs). | cloud-4v2, terra | `a7391b56` |
| M4 | cloud-2 residual 1 — "a `gpt-5.6-terra` review of this diff is OWED; run it pre-merge on a host carrying the wrapper". | cloud-2 §8 | `e0d0e361` |
| M5 | cloud-4v2 residual 1 — the same leg, owed for the same reason. | cloud-4v2 §7 | `e0d0e361` |
| M6 | fenced diff — `protocols/STANDING_RULINGS.md` **N-2** gains its third landed site (`export_backlog_view.py`), keeping the predicate honest. | cloud-2 §5.2 | this branch |
| M7 | fenced diff — `.gitignore` gains `.backlog-view/`. Belt-and-braces (the export root is already self-ignoring); landed because the row's literal wording names it. | cloud-2 §5.1 | this branch |
| M8 | `ecosystem/doc-counts.md` regenerated **once for the whole wave**: tests **3411 → 3459**. Both cloud-2 and cloud-3 correctly declined to write a whole-tree count from a container that could not collect the whole tree. | cloud-2 §5.3, cloud-3 §6 | `7cc187a6` |
| M9 | `docs/audits/README.md` regenerated — the graph lane added two artifacts without regenerating the index, and three merges conflicted on it. Every conflict resolved **by regeneration**, never by hand. | integration | the merge commits |
| M10 | `.claude/generated/*` regenerated — ADR-114 enters the last-5 roster. | integration | `bb056fe1` |

**Two fenced diffs were deliberately NOT swept in**, and they appear below as I5 and I3.
cloud-4v2's `provider-registry-agreement` hook needs a `CLAUDE.md` §9 roster row the file has no
line budget for, and cloud-3's `lane-contract-check` diff is described **by its own author** as
"an interim narrowing, not a claimed cure". Executing either would be a judgment call wearing a
mechanical label.

## 2. ADR — a decision is needed and its evidence is complete

| # | line | route | why a ruling and not an intake |
|---|---|---|---|
| **A1** | **`ADR-114` — may a root `README.md` be recreated, and what does substituting a canonical living-doc filename actually cost?** Landed **Proposed, Decision section deliberately blank**. Priced: fleet parity **MUST ×9** (`VISION.md` is `tier: {hub: MUST, consumer: MUST}` across the nine ADR-104 members, four of them `pre-deploy` and carrying no `VISION.md` today, for which this is an onboarding act rather than a rename); **104 of 114 immutable handoff bundles and 69 `PROBES` files** carrying a locator that can never be corrected; the `gen_handoff` degrade contract that stamps a placeholder into an artifact immutable the moment it is committed. A **fourth cost R2 never priced:** the `## Vision` H2 spine is a second, independent migration surface replicated across five deploy manifests — filename and spine are two decisions and the ADR prices only the first. | **OPERATOR** — it reverses his own 2026-05-23 deletion decision. Architect recommendation on file: **PARK**. | ADR-98 §3's fork test is met: a reasonable person could choose otherwise and reversal is costly. |
| **A2** | **The R1 decision packet — is `AGENTS.md` admitted or refused, and under which reading of ADR-53?** Route **verbatim**; it is built to be ruled from on its own. Its load-bearing new measurement closes the intake's own open question 3: the proposed shape is **47.1% of the Codex 32 KiB cap, with 17 KiB of headroom**, so **R2 §2.5's refusal conditional does not fire and the size argument for refusal is unavailable** — refusal, if ruled, must rest on doctrine. **No `AGENTS.md` file was created**; the intake's hard gate is honoured. | **ARCHITECT** | The reading of a ratified ADR cannot be settled by an intake. ADR-53 Decision 2 would need explicit supersession — and the packet's own point is that a *silent* reinterpretation is the exact drift ADR-53 exists to end. |
| **A3** | **The L0 boundary.** `~/.claude/ROUTING.md` is the canonical model-routing table and **is not in this repository**; neither is the reviewer pin (`~/.claude/bin/codex-review.ps1`) nor the Codex config. Options unchanged: **(a)** bring a copy in-repo with a drift gate, reversing #158 Decision B for a stated reason — the repo already runs regen-and-diff seven times over, so the mechanism exists; **(b)** state in `ARCHITECTURE.md` Ch3 that routing is an L0 concern and out of universalization scope. **"Either is fine; silence is not."** | **ARCHITECT** | It gates `[#82]`: if the reviewer pin lives at L0 then `[#82]` is partly unverifiable from this repo *by construction*, which belongs in the row rather than being discovered at closure. **Decide before the schema, not after.** |
| **A4** | **`[#562]` admission — there are NO SCORES TO RULE ON.** The rerun produced no branch, no artifact, no candidate scores and no control-item result. Per **Q7–Q9** the per-model verdicts land as row bodies under `[#491]`/`[#562]`; there is nothing to land. This session neither scores nor infers — the architect admits or refuses models. The lawful next step is a decision about the **rerun**, not about the models: re-dispatch, or record the window as void. | **ARCHITECT** | Q7–Q9 reserve the admission instrument to the architect. |
| **A5** | **The doc-graph cycle gate.** Lane recommendation: **REPORT-ONLY COMMAND — not FAIL, not WARN**, with `--bucket actionable` as the default so the answer is 2 rather than 18. See R3 for the measured grounds. | **ARCHITECT** rules | Arming an organ is a ruling in this repo, never a default. |

## 3. INTAKE — a candidate needing evaluation

Per ADR-111 §2 the **only** path from a finding to a row runs through intake → ratification; per
**P-2** an intake flipped to `ACCEPTED` must carry a live carrier row or a dated deferral.

| # | line | note |
|---|---|---|
| **I1** | **Phase-2 rustworkx graph library.** ADR-112 **Tier L** (evaluate before adopting) — it adds a dependency to a repo in the fleet's distribution path. Opening question, per the lane: **install path under the pinned `uv 0.11.19` is UNVERIFIED**, as is Windows, on a Windows-developed repo. | The lane's own routing, adopted unchanged. |
| **I2** | **Phase-1 SQL doc-graph organ** (~370–490 LOC; the extractor is ~35% of it and the part that has to be right). **CORRECTION TO THE LANE'S OWN RECOMMENDATION:** it asks for "one new `[P3][M]` BACKLOG row". **ADR-111 §2 forbids that** — a finding may not be filed directly as a row. It runs through intake → ratification like anything else. The *shape* the lane specifies is sound and should be carried into the intake verbatim. | The single place a lane's recommendation is not lawful as written. |
| **I3** | **Four orphaned out-of-lane findings from cloud-3, whose named owners are ALL CLOSED.** See §5 — the sharpest structural finding of the wave. Needs a live home, not a COVERED cite. | |
| **I4** | **A machine-specific absolute path is committed configuration.** `C:\Users\1028120\Documents\Dev\.dev-knowledge` at `.claude/settings.json:63`, now mirrored at `ecosystem/provider-registry.yaml:60`. **Pre-existing and owned by no row.** | Terra reported the registry as *introducing* it; that half is refuted (R2). The underlying defect is real. |
| **I5** | **`provider-registry-agreement` pre-commit entry + its `CLAUDE.md` §9 roster row.** Owed to the integrator by the `[#539]`/batch-4-W5 precedent — but **`CLAUDE.md` sits at 198/200 of its ADR-53 budget with headroom 2**, and the roster row is ~10 lines. Landing it requires a condense act (choosing which §12 bullets fold into the git pointer), which is judgment, not mechanics. | Deliberately NOT executed. The coupling is already enforced by pytest today; the hook moves it to commit time. |
| **I6** | **The detector R2 §1.5(c) recommends and cloud-4v2 did not build:** a `doc_claims`-family check asserting every canonical-doc token in the live corpus resolves to a tracked path. Re-measured this wave: **1,956 occurrences across 678 files, of which 0 are markdown links** — so nothing today can tell you a canonical-doc reference has gone stale. | "Out of that lane's scope; still the right next mechanism." |
| **I7** | **If R1 is admitted, the R5 guard must be stated in BYTES, not lines.** This repo averages ~117 B/line, so a ≤N-line ceiling does not bound the thing the 32 KiB cap measures. | Contingent on A2. |
| **I8** | **An unpriced third precedence layer.** `codex/AGENTS.md` sits at an *intermediate directory inside this repo*, so a cwd at or below `codex/` yields `role → doctrine → role` and **the role wins by position rather than by intent**. Harmless today (identical bytes, later-wins); not harmless if R1 is admitted. | Contingent on A2. |
| **I9** | **Two independent mechanisms copy a script out of `scripts/` and run it beside a partial sibling set** — `deploy/carrier_mesh.py` and a test fixture — and **neither is discoverable from the module being edited**. cloud-4v2's review caught the first; only the suite caught the second (16 tests red). Any future "read it from one table" repoint must check both. | Possibly a `LESSONS.md` append rather than an intake — the architect picks the home. |
| **I10** | **Ship `report-only-wall.yml` to the consumers through the existing `carrier_docs` manifest** — the graph lane's constructive alternative to reusable workflows. Zero new mechanism, zero PAT, zero access-policy change, one job per push instead of six. | Contingent on R1's rejection standing. |

## 4. REJECT — declined, with the reason recorded where the finding lives

| # | line | recorded at |
|---|---|---|
| **R1** | **Reusable workflows as a fleet-wide CI gate layer — REJECTED AGAIN, on new grounds.** The previously-stated ground (outside collaborators) is **correctly withdrawn** and is explicitly *not* why this fails: zero outside collaborators is now VERIFIED live, as is `owner.type: User` and `private: true`. It fails on three independently sufficient measured grounds. **(1) The gate class does not exist** — required checks are unavailable on Free + private, so the "fleet-wide CI gate" survivor is a fleet-wide CI *record*; our own `report-only-wall.yml:2–5` already says exactly that. **(2) The cost overruns the entire allowance** — 2,322 min/month against 1,400 remaining, the decomposition premium alone being **+774 min/month for zero additional coverage**, because a reusable-workflow call *is* a job split and GitHub bills per job rounded up to the minute. **(3) It needs a PAT per consumer and a new `fleet_parity` probe kind**, because `uses:` delivers the workflow definition but **not the tree our gates execute**. | graph artifact §B1–B4. Measured on our own runs — run 106's `changes` job does 10 s of work and bills 1 min — not quoted from documentation. The operator's 30% figure is independently reproduced at 33%. |
| **R2** | **Terra's "the registry *introduces* a machine-specific absolute path" — REFUTED AS STATED.** The registry does not introduce it: that exact string is already committed on `main` at `.claude/settings.json:63`, and the registry's own comment says so. Charging it to cloud-4v2 would blame a lane that only mirrored existing state **and** let the real defect keep its current owner of nobody. | `docs/audits/2026-08-22-codex-cloud4v2-registries-terra.md`, integrator disposition line. The underlying defect survives as **I4**. |
| **R3** | **Arming a WARN or FAIL leg on nontrivial-SCC count — REJECTED on measured grounds.** The metric's sign is inverted: **SCC count is a throughput gauge, not a rot gauge.** 13 of the 18 SCCs are lane-contract↔output pairs *mandated* by the lane protocol, and the graph lane **manufactured SCC #19 out of its own two files** — verified by re-running the extraction, not predicted. A WARN that increments every time a lane executes correctly trains the operator to ignore it, which is the ADR-105 §2 failure `[#419]` names. Even scoped to the actionable corpus where the count is a tractable **2**, both findings are **compliant states**: they are the bidirectional pointers `CLAUDE.md` §5 rule 6 *requires*, since two files that each need the other's authority must form a 2-cycle. **A gate that fires on our own doctrine being obeyed.** | graph artifact §A1–A4 |

## 5. THE ORPHANED FOUR — the wave's sharpest structural finding

cloud-3 ran a full adversarial pass and found **0 findings in its own diff**. It also surfaced four
findings in code it did not touch and **recorded them rather than sweeping them in** — widening a
lane into another row's footprint being the failure mode the batch protocol exists to prevent. Each
was carried with a named owner:

| sev | site | finding | owner named | status **now** |
|---|---|---|---|---|
| **High** | `scripts/single_flight.py:731` | the lease-rejected branch of `release` calls `_not_ours(owner=None)`, printing "it carries no run_id" about a lock it never read — steering the operator to the unguarded `ESCAPE: git push <remote> :<ref>` printed below, **deleting a LIVE sibling's lock**. `_remote_lock_token` is reachable there. | `[#530]` | **CLOSED** |
| Medium | `scripts/single_flight.py:325` | `_not_ours` prints its per-claim ownership TOKEN as "belongs to run {owner[:8]}" — an id matching nothing in the telemetry store, plus **8 bytes of another run's capability**. | `[#530]`/`[#565]` | **BOTH CLOSED** |
| Medium | `.pre-commit-config.yaml:167` | `lane-contract-check` omits `pass_filenames: false`; pre-commit's default passes ALL matched files while `gen_lane_contract.py check` declares exactly one `click.argument("path")`. Latent **only** because zero tracked files match the glob. | `[#539]` | **CLOSED** |
| Medium | `scripts/gen_lane_contract.py:467` | `is_cloud = CLOUD_SECTION in sections` is an EXACT match while every other mandatory section is prefix-matched, so `## Receipt gate (Q5)` reads as a local lane and the Q5 conjunction is **silently skipped**. | `[#539]` | **CLOSED** |

**All four code sites were re-verified live on `main` by this session** — these are not stale reads.

**Why it happened, and it is not a lane defect.** `[#530]`, `[#539]` and `[#565]` were closed by the
**part-C arc on 2026-08-22 — the same day, while these lanes were in flight**. The lanes were
dispatched against a pre-part-C backlog and did exactly the right thing; the sibling arc closed the
owners underneath them. This is a **concurrency artifact of parallel dispatch**, and it is precisely
how a correctly-filed finding becomes invisible: classify these COVERED and the cite resolves to a
closed row, which is how a finding dies quietly.

**Classification: INTAKE (I3).** They cannot be COVERED — the owner is gone. They cannot be filed
directly as rows — ADR-111 §2. The High one can delete another session's lock, so the architect may
wish to rule it out of band rather than let it wait on a leisurely evaluation.

## 6. COVERED — an existing row or ADR already owns it

| # | line | id |
|---|---|---|
| C1 | The prose `path:LINE` locator gate. **Complements the doc-graph organ; is not superseded by it** — disjoint classes: `[#534]` is a semantic claim about a line number, the organ is edge topology. It **gains a dependency** (~80 LOC becomes ~40 if it reads the organ's edge table) but **must not block on it**, being P2 where the organ is P3. | `[#534]` |
| C2 | Markdown-link rot on the actionable corpus — cited only as the zero-baseline precedent that makes R3's argument. Nothing added. | `[#573]` |
| C3 | The priority-axis DECISION row. Its LEAN is ruled and now built; see §7. | `[#488]` |
| C4 | Per-repository agentic-review profiles. **A3's outcome belongs in this row** — if the reviewer pin lives at L0, the row is partly unverifiable from this repo by construction. | `[#82]` |
| C5 | The disposition on intake #16 §3 recorded 2026-08-22 is **not contradicted** by the graph lane: that disposition rested on "no consumer exists"; the architect has since named one. The lane's finding is narrower and compatible — the named consumer is served entirely by the SQL half, so the filing is warranted and the graph-library activation still lacks a query with demonstrated yield. | intake #16 |
| C6 | `doc_rot` backlog-row-length WARNs (~24 rows over the 1320 ceiling) and the grooming-cadence WARN (23 d > 21 d, ADR-41). Pre-existing and owned by the annotation ledger and the ADR-41 cadence. Not this wave's. | ledger / ADR-41 |
| C7 | **The one standing suite RED**, `test_anchor_gate_probe_distinguishes_installed_from_absent`. `[#569]` names it verbatim: *"does not discriminate, because the pre-push organ refuses an anchored push in the synthetic consumer too."* **Its sibling half is now discharged** — the same row's `test_routine_consumers_live_backlog_governs_exactly_one_row` was fixed by the part-C arc earlier today (`353149ab`), so `[#569]` item (A) is half-done and the row narrows. | `[#569]` |

## 7. D3 — closure sweep on this wave's own results

Verified against the merged tree, **not** against the artifacts' self-assessment.

| row | Done-when | verdict |
|---|---|---|
| `[#563]` | exporter writes the on-disk format from `tasks/` into a gitignored dir, re-exports every invocation, export path gitignored with a test asserting nothing tracked, both flags `false`, `--agent-instructions none` honoured structurally, a test asserts no gate/hook/script reads the export | **all clauses discharged.** The `.gitignore` clause is now true both ways — the export root is self-ignoring *and* M7 landed the literal entry. |
| `[#566]` | ranking computed by the existing generator from `serialize-group` with no new authored field, `[P1..P3]` primary, contention breaking ties within a tier, `P-enum + age` breaking the rest, a test pinning a seeded tie block | **all clauses discharged.** |
| `[#488]` | the DECISION row whose ruling released `[#566]`; `[#566]`'s own `kill-candidates` line records that `[#488]` "closes on its own research-and-ruling clause" | **candidate** — the ruling is given and the build has landed. |

**banked_D = 3 proposed** (`[#563]`, `[#566]`, `[#488]`), **0 executed.** ADR-70 Tier-1 reserves
execution to operator-approved closures, so these are proposed, not taken. **Births in D5 are capped
at banked_D**, remainder as a named queue — the same R2 arithmetic part C used.

## 7a. The suite, and the proof the one RED is not this wave's

```
uv sync --locked --group analytics   (the analytics group matters: a plain sync drops
                                      pandas and manufactures 17 false REDs)
uv run --locked pytest -q
  ->  1 failed - 3453 passed - 4 skipped - 1 xfailed   in 830.41s (13m50s)
```

The single failure is `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent`.

**It was proved pre-existing rather than assumed pre-existing.** The same test was run at `23d72d51` — bare `main` before any of this wave's merges — and **fails identically there**. The wave therefore introduces **zero new failures**. It is COVERED by `[#569]` (row C7), which names it verbatim.

Worth stating because it is a live claim about an armed organ: the evidence line reads *"pre-push organ REFUSED an anchored push too (exit 1) — it does not discriminate; a constant refusal enforces nothing."* That is the exact vacuity the test's own docstring says it exists to prevent, now asserted of the ADR-85 hard leg's probe. The organ still refuses; what is unproven is that it refuses *selectively*. `[#569]` owns it.

## 8. What the operator can SEE or USE that he could not yesterday

1. **A deterministic next-row pick inside a 103-way tie.** `python scripts/gen_task_tree.py --rank`
   turns 3 ordered buckets over 190 open rows into a **total order** — no pair unordered — using
   zero new authored fields. The largest tie block falls 103 → 37.
2. **The queue's serialization, before dispatch rather than after a refusal.** 119 of 190 open rows
   carry a `serialize-group` across 11 groups; the prework records this as *the only one of six
   candidate axes that would have predicted the batch-6 dispatch refusal before it happened*.
3. **The backlog in a real board/web UI**, one way and disposable: `python scripts/export_backlog_view.py`
   renders all 299 rows in **0.19 s** into a self-ignoring `.backlog-view/`, with the authoritative
   body line landing in `## Description` **byte-for-byte**, so the view is diffable against its source.
4. **A provider/model swap that can no longer half-happen.** Nine table-edit seams across five
   different formats — `.md` frontmatter, a `.js` object literal, `.md` prose, JSON config, YAML —
   are held in agreement by one checker against `ecosystem/provider-registry.yaml`.
5. **Two priced decisions instead of two intuitions** — ADR-114 and the R1 packet, each carrying the
   measurement that changes the argument (the ×9 fleet program; the 47.1%-of-cap headroom that
   removes the size objection).
6. **A measured answer on CI**, not an opinion: reusable workflows would cost **2,322 min/month
   against 1,400 remaining**, and required checks — the thing that would make them gates at all —
   are unavailable on this plan.

---

## Amendment A1 — 2026-08-22: the batched ruling, and what it disposed

> **In-file amendment marker (`CLAUDE.md` §5 rule 3).** Nothing above is edited; this section
> records the architect/operator ruling returned over the table and the disposition of every
> line. The table above is the input the ruling was given; this is its output.

The pause at §4 was answered with **one batched ruling** covering all five ADR lines, the intake
block, the three rejections and the closure proposals. Dispositions:

| line | ruling | executed as |
|---|---|---|
| **A1** ADR-114 rename | **PARKED** (operator) — revisit only if A2's `AGENTS.md` track fails the universal-entry purpose | Decision recorded in `ADR-114`; Status `Proposed → PARKED`; the three priced options retained; `docs/decisions/README.md` reconciled on all three surfaces |
| **A2** `AGENTS.md` | **ADMITTED** — the size objection is dead (16.9 KiB headroom) and ADR-53 forbids two content-carrying files, not the name | `protocols/STANDING_RULINGS.md` **R-1**; execution filed as the bounded lane `[#577]` |
| **A3** L0 boundary | **RULED (b)** — declare it; *"the finding is right that silence is not a boundary — the declaration is the boundary"* | `ARCHITECTURE.md` Ch3 + register **R-2**, landing predicate resolving TRUE on both sites |
| **A4** `[#562]` admission | **MOOT-IN-MOTION** — the operator re-dispatched `cloud-1-retry`; the verdict is HELD until it returns. A second absence VOIDS the rerun attempt and converts the row's next step into a **transport investigation citing both absences** | status line in this artifact's close report; no verdict inferred |
| **A5** cycle gate | **APPROVED as scoped by R-A** — SQL keeps reachability/orphans/degree; the library **earns** cycles/SCC | rides intake **#40**; no direct row, exactly as ADR-111 §2 forced |
| **I3** live-harm line | **YES, out-of-band NOW** — *"a doc that steers the operator into deleting a LIVE sibling session's lock is live-harm"* | fixed at `a7391b56`'s successor commit, mutation-checked; the other three stay COVERED-closed |
| **I5** roster line | file it **WITH consolidation** — *"do not shave under the cap"* | hook armed + roster row landed; the v2.60–v2.62 arc **merged** as one overlapping entry; headroom 3, not 0 |
| **REJECTS** ×3 | **ACCEPTED as recorded**, including R1's re-rejection on the **new** grounds | recorded below |
| **closures** | **OPERATOR GO** — execute all three | `[#563]` `[#566]` `[#488]` closed; ledger 214 → 211; `banked_D = 3` |

**On R1, recorded because the ruling asked for it explicitly.** The **old ground was correctly
withdrawn** — zero outside collaborators is verified live, and that is no longer why reusable
workflows fail. The rejection **stands on the new grounds**: required checks do not exist on
Free + private, so the gate class itself is absent; and the cost is **2,322 min/month against
1,400 remaining**. A rejection that quietly kept its disproven reason would be worth less than no
rejection at all, which is why the withdrawal is recorded beside the grounds that replaced it.

**D5 births: 1 of 3 taken.** `[#577]` (the `AGENTS.md` execution lane) is birth priority (1).
Priority (2) — intake #40's carrier — is deliberately **unborn**, because the ruling conditions
it on ratification and **P-2** binds only at `ACCEPTED`; filing it now would invert the
ratification order. Priority (3) was an act rather than a row, and is executed.

**The named queue — the remainder, carried rather than dropped** (funnel lines that the cap or
the ruling left unexecuted, listed so the next window inherits them by name):

- **I4** — the machine-specific absolute path at `.claude/settings.json:63`, mirrored in the
  provider registry. Pre-existing, owned by no row.
- **I6** — the canonical-doc token detector R2 §1.5(c) recommends: 1,956 references, 0 of them
  links, nothing able to detect a stale one.
- **I7 / I8** — now **live** rather than contingent, since A2 admitted the track: the byte-based
  R5 guard, and the unpriced third precedence layer at `codex/AGENTS.md` where the reviewer role
  wins by position rather than by intent. Both are written into `[#577]`'s Done-when.
- **I9** — the two-copiers lesson (`deploy/carrier_mesh.py` and a test fixture both copy a script
  out of `scripts/` beside a partial sibling set, and neither is discoverable from the module
  being edited). Home unruled: `LESSONS.md` or an intake.
- **I10** — shipping `report-only-wall.yml` to consumers through the existing `carrier_docs`
  manifest, the constructive alternative R1's rejection leaves standing.
- **The three remaining orphaned findings** of §5 — the `single_flight` token-vs-`run_id` Medium
  and the two `[#539]`-owned Mediums. COVERED-closed per the ruling; they need a live home if
  they are ever to be fixed.
- **`[#569]` item (A) is now half-discharged** — its `routine_consumers` half was fixed by the
  part-C arc today; the anchor-probe half remains, and it is the wave's one standing suite RED.

**D6 discharged:** `protocols/PLAYBOOK.md` Ch8 gains *"The wave close — every dispatched wave ends
D0–D5, and the funnel table is mandatory"*, including the line this window's own incident
produced: **one integrator at a time is enforced by mechanism (a lock or a branch guard), not by
convention — its build rides the queued Q2-enforcement item.** The discipline held here because
one operator was watching, and a discipline that holds only while someone is watching is not a
mechanism.
