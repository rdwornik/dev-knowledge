# Residual — 2026-07-10-dev-knowledge-architect — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (§2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> Mode: **architect** (§13).
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation; `recall`/`inferred`
> = reconstructed from the JOURNAL/git window, may have moved (the load-bearing ones are re-checkable
> via `PROBES.md`); `unknown` = stated as such.

> **`SUPPLEMENT.md` is generated EMPTY.** Until the operator fills it (`supplement filled`) the ANSWERS region is empty -> the assembler folds nothing -> the incoming §13(d) operator-context beat fires **FULL** (a full off-repo ask), not the narrowed *"anything changed since?"*.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`). **Re-derive each at read-time — the teeth are in
`PROBES.md` (P4/P6/P7/P9), not in trusting these lines.** This bundle states **no** ship-gate
verdict, WARN count, `[stale]` status, drifted `#id`, or count — those are the probes' live answers.

<!-- FILL-IN:driftflags START (hand-authored — describe WHICH flags are STANDING vs NEW and WHY, BY REFERENCE. Do NOT state the ship-gate verdict, the WARN count, the [stale] status, or any drifted #id/sha — those are P7/P4's LIVE answer; naming a value here re-inverts the anti-bluff contract.) -->
All drift-flags this window are **STANDING and dispositioned** in `ecosystem/disposition-register.yaml`; the night run introduced **none new** (the two filings + the audit report + this bundle were authored net-neutral — no new `doc_rot`, no new serialize-group). Standing classes, by reference: `no_ff_merges` — the grandfathered journal-wrap / transcript-archive direct-to-main commits (`#210` is the standing-rule proposal); `doc_rot` backlog-accretion — `#262` + `#278` (dispositioned); `undeclared_edges` — the six handoff-process prose edges (`#241`); `handoff_probes` P1a/P1b/P8 — the grep/sed/ls tool-absent SKIPs (environmental, not drift). Run **P4/P6/P7** for the live verdict / count / `[stale]` — this file names none by design. _[witnessed — `audit.py health` re-run live this generation, OK]_
<!-- FILL-IN:driftflags END -->

---

## §2 — Shipped this window (the map — pointer, not re-narration)

<!-- FILL-IN:shipped START (hand-authored — a terse map of what shipped, by #id + ADR, pointing at BACKLOG/JOURNAL; NOT a detailed recap JOURNAL already encodes, §2/RF-6) -->
Window = the **2026-07-09 night hygiene run** (this generation). The map (detail in `JOURNAL.md`):
- **`#301`** filed — session-plan artifact class (architect bundles gain a bundle-resident `PLAN.md`; the mode→artifact symmetry). → `BACKLOG.md` [S2], arc `5fdd074`.
- **`#302`** filed — branch-protection parity: answers the ai-council lived-QA **F1** (hub has NO commit-time branch-guard, only push-time `block-ff-push` HUB-ONLY; consumers lack even that). → `BACKLOG.md` [S8], arc `5fdd074`.
- **Night hygiene audit** — 6-corpus read-only Sonnet fan-out (intake / decisions / audits / handoffs / BACKLOG-coherence / ai-council). Headline: exactly one cold committed bundle leaks (`2026-07-05-dev-knowledge-architect`, 8 fill-markers); corpus referentially clean but no age-based backstop. → `docs/audits/2026-07-09-night-hygiene-audit.md`, arc `558a131`.
- **Prior same-day context** (5 earlier 2026-07-09 sessions — night-verification · morning-ops · session-close · `#164` finish · GATE-0): see the five `JOURNAL.md` 2026-07-09 entries (`#164` CLOSED, `#255` retired, `#291` backup fix).

State pointer: `BACKLOG.md` (82 tasks after the two night filings). _[witnessed — this run]_
<!-- FILL-IN:shipped END -->

---

## §4 — Next-frontier decisions (the design "why" that travels)

<!-- FILL-IN:frontier START (hand-authored — the open architecture questions + decision context the next session must resume rather than rediscover; the residual's core payload in architect mode) -->
**The operator's execution-first bar still governs** — *visible outcomes over governance*; any new meta/governance work must unblock onboarding or be rejected. **The plan-v3-specific operator intent is NOT yet in this bundle** — `SUPPLEMENT.md` ANSWERS is generated EMPTY, so the §13d beat fires FULL; fill it at session start. The un-committed "why," in plan-v3 sequence (full plan in `PLAN.md`):

- **G8 runbook fix FIRST (small, serial) — it gates B-S2** (`#299`): the onboarding runbook Layer-6 verify must invoke the SessionStart hook's command line VERBATIM (`python -m pre_commit install`), not a proxy `import pre_commit` that passed on a different interpreter than the hook uses. corp-monorepo shares the latent fragility (`pre_commit` in `.venv`, undeclared in pyproject → a fresh re-clone won't repopulate it). _[recall — plan-v3 §D · `#299`]_
- **B-S2 corp-monorepo onboarding** (dedicated chat, plan-first) — the **n=2** runbook gate after the ai-council n=1 pilot; runs the leg-b seeder as its first real consumer; surfaces D4 + `#262` tool-MANAGED codemap n≥1 (corp-monorepo is tach-bearing, so it can close the generator-managed owe ai-council's flat layout couldn't, `#295`). _[recall — plan-v3 §D]_
- **QA-role intake decomposition (EPIC G)** — after the operator's functional QA session: technical decomposition → ADR (role · protocol · report-gate) → build → **FLEET CARRIER** (every onboarded repo inherits it). Evidence set: incidents **I1–I6** (plan-v3 §A) + OD2 proportional test-depth keyed to the T1–T5 scope-tags. Admission: **`#270` re-enters** — it now unblocks the operator-demanded night capability (OD4). _[recall — plan-v3 §A/§B]_
- **`#300` hermetization ADR (EPIC I) — BEFORE Wave-2**: d.i `docs/runbooks/` location · d.ii mode-boot bundle home (incl. the committed-ephemeral `docs/handoffs/2026-07-07-dev-knowledge-functional/` fate — one migration pass, no drive-by delete) · d.iii audit-class grammar. **Tonight's audit made d.iii decidable**: 41 already-compliant + 31 trivially-compliant vs ~130 subject-before-class + 4 class-less → the honest ruling is **prospective-only + grandfather + a canonical CLASS enum** (not a retroactive rename of ~65% of the corpus, which the index already disambiguates by date). See audit §S3. _[witnessed — this run's finding]_
- **EPIC H — subagent/model-routing doctrine** (OD3): research spike → PLAYBOOK doctrine (Opus = orchestration/judgment · Sonnet = bounded probes/mechanical · Haiku = cheap fan-out where the quality floor allows) → binds EPIC G's QA runs as the first consumer. **This night run is itself an evidence datapoint** — an Opus orchestrator + 6 Sonnet read-only subagents ran cleanly with all git mutations serial in the main thread. _[recall — plan-v3 OD3/§B]_
- **Night-layer `#270` → `#271`** re-admission — the operator-load gauge is the gating FIRST element; night EXECUTES pre-authorized deterministic contracts only and PROPOSES the rest (this run IS the pattern; D8 go/no-go rests on `#270` + intake-8 triage). _[recall — plan-v3 OD4/§C-D8]_
- **Carried CC-observed residuals (reconcile, do NOT drive-by):** (a) the `docs/decisions/README.md` ADR-51 one-liner still speaks tier language, superseded by the 2026-05-23 amendment (audit §S2-2, **verify-then-fix**); (b) the cold `2026-07-05-dev-knowledge-architect` bundle's 8 fill-markers (audit §S4-1 — **backfill or accept-and-annotate**, not a night-fix: immutable + I cannot fabricate that session's retrospective); (c) BACKLOG `#292`'s evidence text is now stale (fixed 07-09 bundle, misses the 07-05 one — audit §S4-2); (d) the hub BACKLOG footer's ai-council-residuals pointer appears already resolved in-repo (audit §S6). _[witnessed — this run's findings]_

**This bundle supersedes `docs/handoffs/2026-07-09-dev-knowledge-architect/`** (complete + immutable, but predates plan-v3 + tonight's findings) — boot THIS one; the 07-09 bundle stays as history. Slug is dated **2026-07-10** (next working session) because the 07-09 slug is held by that complete bundle; the collision + choice are recorded in the night audit + morning briefing.
<!-- FILL-IN:frontier END -->

---

## §6 — Task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets.** Task-state is: a pointer to `BACKLOG.md`, the live
in-progress branches (`git branch -v`), and any **drift-flag** `validate_git_backlog` raises (§1 /
`PROBES.md` P4). Re-narrating item text splits the truth and drifts — the pointer + the drift-flag is
the whole task-state.
