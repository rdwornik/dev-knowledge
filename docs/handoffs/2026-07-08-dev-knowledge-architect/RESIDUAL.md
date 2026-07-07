# Residual — 2026-07-08-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is FILLED.** Its ANSWERS fold into `PASTE_THIS.md`; the incoming §13(d) operator-context beat **NARROWS** to *"anything changed since the supplement was written?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
**One NEW, un-dispositioned drift this window — re-derive its live gate impact via `PROBES.md` P7, then clear it first (§4-A).** The census-triage arc (JOURNAL 2026-07-07, `2e3ccf5..799d0b9`) added the `audit-index-freshness` pre-commit hook and shifted the collected-test count, but **`CLAUDE.md` §9's hook roster and `ecosystem/doc-counts.md` were not reconciled** — the intake-SEED-block entry (`9d3176e`) explicitly recorded leaving them. So `doc_claims` flags the §9 roster (missing the new hook) plus two `doc-counts.md` counts. Mechanical to clear, but **`CLAUDE.md` is canonical-freshness-gated**, so the §9 fix carries a genuine end-to-end re-read + `last_reviewed` re-stamp — its own small arc, not a drive-by (and the reason this handoff did not fold it in).

**Everything else is STANDING + dispositioned** in `ecosystem/disposition-register.yaml`: the `git_backlog_drift` voided-closure (#77), the `no_ff_merges` journal-wrap / transcript-archive commits, and the `undeclared_edges` handoff-process prose edges (#241 — the tracked deferral). **This handoff arc introduces no new drift** — a pure ADD (the bundle + a JOURNAL entry). Re-derive the live verdict / WARN count / any `[stale]` marker via `PROBES.md` P7/P4; this bundle states none.
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Since the prior architect bundle (`2026-07-06`), all merged to `main` — detail in `JOURNAL.md` (2026-07-07 → 2026-07-08) / `BACKLOG.md`:
- **Intake trilogy ratified + built** — **ADR-98** (intake pipeline: functional/technical/developer modes), **ADR-99** (epic-naming: Track-X now, story-map at P6), **ADR-100** (audit-retention: keep-all + count-tiered index; folds/closes #212). Pipeline Phase 1: `git mv intake/ → docs/intake/`, the `/handoff` **operator runbook** (PLAYBOOK §8 "How to hand off"), functional mode; **#280** filed (deploy manifest doesn't propagate the intake area).
- **Fleet-consistency census** (read-only, 7 repos) — `docs/audits/2026-07-08-fleet-consistency-census.md`; fleet healthy (no secrets, floor hash intact ×3, no `core.hooksPath` relic); 14-finding triage queue.
- **Census-triage rulings (Wave 0)** — `ecosystem/REGISTRY.md` (human fleet registry), the `audit-index-freshness` pre-commit gate, `{func|tech}` intake naming, **#281–#287** filed + #262/#269/#278 amended, grooming worksheet (`docs/audits/2026-07-08-grooming-worksheet.md`).
- **Intake SEED block** — 4 func SEED docs (**ids 6–9**: new-project-bootstrap [folds #43], ai-council-interface, night-routines-suite, dashboards-local-html), **#288** (model-identity guard, unattended-run detector) filed.

This is the map — the JOURNAL encodes the detail.
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The session's decision queue — resume, don't rediscover.** Start from `BACKLOG.md` (the seven themes); this is the *shape* of what's open, not a re-narration of item text.

**A. Clear the one live drift first (§1 headline).** The census-triage arc left `CLAUDE.md` §9's hook roster + `ecosystem/doc-counts.md` un-reconciled — `doc_claims` will flag the §9 roster (missing the `audit-index-freshness` hook) plus two doc-counts. A small fix arc: regenerate doc-counts, add the hook line to §9, then a genuine `CLAUDE.md` re-read + `last_reviewed` re-stamp (it is canonical-freshness-gated). **Re-derive the live gate state via `PROBES.md` P7** — if still blocking, clear this before the frontier work so the tree is green to build on.

**B. Run the intake pipeline's first end-to-end consumption — this is what proves ADR-98.** The 4 SEED docs (ids 6–9, `docs/intake/`) are filed `status: SEED` and await **functional elaboration → technical triage → epic decomposition**. This is the intake↔epic edge's first real exercise; ADR-98 §5 keeps that edge **advisory until n=2** docs are consumed end-to-end, so this run earns the tightening. Confirm any pending operator sign-off on the SEED acceptance-criteria before elaborating. Each SEED carries its own downstream: new-project-bootstrap (folds **#43** scaffold scope), ai-council-interface, night-routines-suite (behind #270/#271), dashboards-local-html (**#264** re-scope).

**C. Decide Wave-1 fleet onboarding — the P6 roll (the biggest open decision).** The essence-spec lifecycle epic (**#244**) has P1–P5 shipped; **P6 = fleet rollout n=2+ (#221)** is the open go/no-go. The census confirmed 6/7 repos already on the ADR-66 story-map, ai-council the sole Track-X outlier (**#281** — carry the convergence at onboarding, or accept Track-X as durable). Onboarding runbook = **#131** (6-layer install) / **#215** (conformance-verify); the carrier-side hook-arming fix (**#275** leg-b) ships at the next release (v1.3.x). **Open question:** is the P6 WAIT lifted, and does Wave-1 onboard ai-council first?

**D. Backlog grooming leg-c — the operator+architect ruling (a browser-session decision, not CC's).** The census produced a grooming **worksheet** (`docs/audits/2026-07-08-grooming-worksheet.md`, **#286**); leg-c is the KEEP/KILL/MERGE/DEFER pass over ~120 open tasks across seven themes. This planning session is the right place to prune.

**E. Operator-pending calls (surfaced — not for CC to decide):**
- **#284** — backup posture: corp-ops has no git remote; corp-sca's `feature/tenrox-loader` is 6 commits unpushed — a one-disk data-loss risk. **PENDING-OPERATOR**.
- **#264** — dashboards: the operator's direction is **local HTML in VS Code, not cloud Artifacts** (intake-id 9 records it); the usability/scope call is open.
- **#270 / #271** — nightly-layer revival (night-routines suite), rent-rule-gated, load-gauge first; **#288** (model-identity guard) sits under it. Behind #270.

**Routed elsewhere (ADR-41 — not hub scope; for the named dedicated chat):** ai-council carries the story-map convergence (#281) + the #275 carrier-side leg in its own chat; per-child codemap migration (#262) executes in each child's chat.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
