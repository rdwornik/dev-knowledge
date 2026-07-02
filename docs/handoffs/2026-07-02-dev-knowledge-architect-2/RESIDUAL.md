# Residual — 2026-07-02 architect handoff (`-2`, cold refresh) — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **This is a COLD REFRESH of the prior 2026-07-02 bundle.** The session was `/clear → /handoff`
> with no in-session design work; the only window delta since the prior bundle
> (`docs/handoffs/2026-07-02-dev-knowledge-architect/`) is a **housekeeping stale-disposition
> prune** (`b255a8c`). The strategic frontier is **unchanged and un-acted-upon** — the three-goal
> priority is carried forward here (§4) from that prior bundle's **FILLED** supplement, which stays
> **authoritative on priority**. This bundle's own `SUPPLEMENT.md` is committed **empty** (cold
> disposition), so its ANSWERS are not folded into `PASTE_THIS`; the incoming **§13(d) beat**
> narrows to *"anything changed since the prior supplement's three goals?"*
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window + the prior bundle,
> may have moved — the load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and **CLEAN**; the disposition register is now **6 → 4** (the prune cleared 2 stale cross-repo entries)

`python scripts/audit.py ship-gate` → **GREEN** (**4 WARN dispositioned**, **NO `[stale]` line**) —
verification organs green against this arc. The window's **only** change is a register cleanup:

- **2 stale cross-repo probe dispositions PRUNED (`b255a8c`, witnessed).** At the prior bundle's
  generation the ai-council cross-repo probes degraded to WARN and were dispositioned
  (`warn-handoff-probes-p5/p7-crossrepo-ai-council-2026-07-02`). The newer
  `2026-07-02-dev-knowledge-architect` bundle **superseded** the ai-council bundle as *latest*, so
  `handoff_probes` now binds **10 probes clean** ([OK]) and both dispositions matched **no live WARN**
  → tombstoned per the ADR-75 clearing convention. Result: the register drops **6 → 4** dispositioned,
  **NO `[stale]`**. The underlying cross-repo resolve-only gap stays tracked by **#234** (unchanged).

### Standing flags (benign / dispositioned — unchanged, do NOT touch) — the 4 that remain

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned
  (`warn-77-voided-closure`). **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) print `[~~]` under `health`, `[disp]` under `ship-gate`. **Expected
  seam, not a regression.** **#210** (open) proposes converting this class from per-instance
  disposition to a standing rule (path-scoped EXEMPT or branch-then-merge the JOURNAL wrap) — a
  §4-adjacent decision.

_(The two ai-council cross-repo P5/P7 dispositions that were here at the prior handoff are **gone** —
pruned this window. That is the whole §1 delta.)_

---

## §2 — Shipped this window (prior 2026-07-02 bundle → now) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~2). **recall/inferred** from the window;
re-derive load-bearing counts via `PROBES.md`.

**The window is housekeeping-only — one arc:**
- **Stale-disposition prune** (`b255a8c` + journal anchor `41bc935`, merged `f3c3f51`): tombstoned the
  2 stale ai-council cross-repo probe dispositions (see §1). `ecosystem/disposition-register.yaml`
  (−26/+7). No design decision, no methodology change.

**The sealed backdrop (do NOT redo — carried by the PRIOR bundle, not re-narrated here):**
- The **arm-first chain executed** (#226/#230, **ADR-93** floor model A armed + conformance-proven n=1;
  real ai-council armed), the **ARCHITECTURE currency arc** (#222/#223/#224 — decoupled the volatile
  count-claims into `ecosystem/doc-counts.md`, documented the deploy subsystem, rotated the ADR lists),
  the **external-review system audit**, and the **first-ever cross-repo architect handoff** (ai-council,
  filed #234). Full map: `docs/handoffs/2026-07-02-dev-knowledge-architect/RESIDUAL.md` §2.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** (**94 tasks, 7 themes, 21 stories** — witnessed via
  `validate_backlog`) — the spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (integrated) + this handoff branch
  `docs/2026-07-02-architect-handoff-2`.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the
  serialize-groups + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9,
  unchanged from the prior bundle): **code-edge = just `#218`**, **coherence = `#180/#181/#182/#220`**,
  **audit-py group includes `#234`** (the cross-repo-teeth item). **`#221`'s `depends-on: #226` is
  SATISFIED** (arming closed) — the hard edge that gated fleet is gone; fleet is navigable but
  **sequenced-after** the three goals (§4).

---

## §4 — The next frontier (open architecture decisions — carried forward from the prior FILLED supplement)

**Unchanged from the prior 2026-07-02 bundle** — nothing this window touched the design. The deploy
subsystem is **BUILT + ARMED + PROVEN (n=1) + DOCUMENTED**; the arm-first chain is **done and sealed**.
The repo's dependency graph reads fleet (#221) as next, but **the operator's FILLED supplement
re-scoped that** — fleet is real but **sequenced AFTER** the three goals below. The operator ruled the
supplement **authoritative on priority**. **Authoritative source (READ IT):**
`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md` ANSWERS. **recall/inferred** — the
architect resumes the design here.

**The priority (operator-ruled — the repo's dependency graph does NOT encode this):**
> **(a) FABLE review (time-boxed, FIRST)** → **(b)+(c) wire ai-council-as-governed-query + close the ADR + ai-council methodology tracks (one coupled work-stream, after Fable)** → **fleet #221 (sequenced-after)**.

1. **(a) Run the Fable whole-system review + merge its rulings — FIRST, because it is time-boxed.** The
   `.dev-knowledge` system audit + the review-ask (Part A: the §7 architecture forks; Part B: process-meta
   — over-engineering-for-solo, verify-proportionality, canonical-doc naming, deterministic-gate-vs-semantic-
   property) are **drafted**. Get them to Fable, extract maximum value from the **perishable preview window**
   (Mythos-tier, possibly export-restricted), then merge Fable's architectural rulings back into the
   methodology. **Do this first** — Fable's rulings (esp. two-track coherence + the deterministic-gate-vs-
   semantic-property class) **may reshape goals (b)/(c)**, so closing the methodologies before merging risks
   an unwind. OPEN: the review **scope** under the time-box (lean focused, not "review everything").
2. **(b) Wire ai-council as a CC-GOVERNED query mechanism.** Elevate ai-council from a standalone tool to a
   governed part of the methodology: an architect's multi-model-debate request routes **browser → CC (skill/
   hook) → ai-council**, with **CC managing the query lifecycle** — question authoring, save-to-correct-path
   discipline, and ADR management of the output. Closes the loop where ai-council *produces* ADRs but their
   governance is not yet mechanized. OPEN: the **integration shape** (skill vs hook vs other CC-side trigger)
   — settled in intent (CC governs the lifecycle regardless of trigger form), undecided in mechanism.
3. **(c) Close the two open methodology tracks — ADR methodology + ai-council methodology.** These are the
   operator's named "not yet done" loops; **(b) and (c) are one work-stream** (ai-council produces ADRs, the
   ADR methodology governs them). Seal both by mechanism, not memory. OPEN: what "closed" **means** for the
   ADR methodology — the **#170/#168 traceability spine** is the half-built sticking point.

**Fleet #221 + the hardening items — sequenced AFTER (demoted, not deleted):**
- **#221 — fleet rollout** (gated by intent, not dependency): run `deploy/tool.py` on corp-monorepo /
  corp-ops / corp-sca-time-automation to reach n=2+, each using **#230** as its acceptance gate; done-when
  also requires **#225** (surgical precommit carrier) closed. Scaling to n=3 before merging Fable's rulings
  would propagate a soon-to-change methodology. Carry the pilot rule: **treat each consumer's `.gitignore` +
  config shape as an UNKNOWN to probe, not a copy of the hub** (prior SUPPLEMENT §B; LESSONS 2026-07-01).
- **#225 — precommit carrier surgical edit** (comment-preserving; precedes fleet for clean diffs at scale).
- **#231 — consumer→hub feedback loop** (schema + transport + home open; pairs with (b)).
- **#234 — cross-repo probe FAIL-teeth** (harden `.claude/` cross-repo targets; honest-partial WARN today —
  the gap the pruned dispositions rode on).

**Adjacent open decisions (smaller, unchanged):**
- **#220 — the MODIFY / semantic-drift axis.** VERIFY-FIRST: does the ADR-89 Pyright oracle or any existing
  organ gate a *meaning-change-without-version-bump*, or only add/remove/exist? Demonstrated-catch bar first.
- **#210 — journal-wrap no-ff standing rule.** Path-scoped EXEMPT (JOURNAL/transcripts-only) vs branch-then-
  merge the wrap — must NOT weaken core-invariant #5.
- **#233 — deploy-record-index test tempdir isolation** (per-run isolated tempdir; hygiene debt).
- **#232 — ship-gate right-sizing (UNFILED candidate).** Right-size, not skip; referenced by #233 but never
  filed as its own id — the architect files it or folds it.

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The priority "why" (READ FIRST — this bundle's supplement is empty by cold disposition):** the PRIOR
  bundle's FILLED supplement — `docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md` ANSWERS —
  the three-goal priority, the Fable-first rationale (§5), the "what NOT to redo" list (§3), and the
  fleet-after ruling (§A). **Authoritative on priority; un-acted-upon; still live.**
- **The Fable review input (goal a):** `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`
  (the system audit + the review-ask, Part A §7 architecture forks + Part B process-meta).
- **The arm-first arc's "why" (sealed backdrop):** **ADR-93** (floor model A, armed + conformance-proven),
  `LESSONS.md`, PLAYBOOK §20, `deploy/` (tool.py + carriers + `carrier_floor.py`), and the prior bundle's
  `RESIDUAL.md`/`HANDOFF_BOOT.md`.
- **This window's one capture:** `JOURNAL.md` top entry (`b255a8c`, the prune) + `ecosystem/disposition-register.yaml`.
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
