# Residual — 2026-07-02 architect handoff (`-2`, generated cold → FILLED → re-scoped) — the part the repo does not already encode

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **Generated as a cold refresh, then FILLED — and the fill RE-SCOPED the priority.** The window's
> only git delta since the prior bundle (`docs/handoffs/2026-07-02-dev-knowledge-architect/`) is a
> **housekeeping stale-disposition prune** (`b255a8c`, §1/§2). But the operator then **FILLED
> `SUPPLEMENT.md`** from an outgoing architect chat holding a **CC-verified live finding** that
> **supersedes** the prior three-goal priority: **the enforcement-transfer gap is now P0** (§4). The
> filled ANSWERS are folded into `PASTE_THIS`; the incoming **§13(d) beat NARROWS** to *"anything
> changed since?"* **§4 below leads with the enforcement-mesh P0**; the three goals + fleet #221 are
> demoted to **sequenced-after** (kept, not deleted). The full rationale is the folded
> `SUPPLEMENT.md` ANSWERS — read them.
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

## §4 — The next frontier (open architecture decisions — RE-SCOPED by the FILLED supplement to the enforcement-mesh P0)

**The filled supplement's CC-verified finding re-scoped the priority.** The deploy subsystem is
**BUILT + ARMED + PROVEN (n=1) + DOCUMENTED** — but it carries the **presence** of the methodology,
**not its enforcement**. **Authoritative source (READ IT):** the folded
`SUPPLEMENT.md` ANSWERS (this bundle). **recall/inferred from the fill** — the architect resumes here.

**THE P0 (new — supersedes the prior three-goal priority):**
> **Close the enforcement-transfer gap — make "held by mechanism, not memory" TRUE for consumers, not just the hub.**

- **The finding (CC-verified live, all 4 consumers).** Five hub enforcement organs —
  `session_end_backpressure` (JOURNAL hard-block), `canonical_freshness`, `doc_claims`,
  `git_backlog_drift`, the coherence spine — are **HUB-ONLY**: they fire only when the hub runs
  `audit.py` against a consumer from outside. **Nothing inside any consumer enforces them locally
  (5/5 ABSENT across ai-council / corp-monorepo / corp-ops / corp-sca-time-automation).** The one
  organ present fleet-wide is the plugin's `propose_closures` — **non-blocking by design.** So there
  is **zero fail-closed enforcement in any consumer.** Proof it bites, not theory: ai-council shipped
  3 feature epics this window with JOURNAL ~1 month stale and nothing blocked it. **"Held by mechanism,
  not memory" is TRUE for the hub, FALSE for every consumer — a constitution violation replicated 4×.**
- **The gap:** the deploy subsystem's 4 carriers (globalconfig / plugin / precommit / floor) were
  **never designed to transfer** the hub Stop-hook or the `audit.py` organs. There is **no
  consumer-local enforcement carrier.**
- **The decomposition (dependency-ordered; steps 0–1 DONE this window):** (0) stabilize live + (1)
  fleet-map — **done** (the blast-radius map above; ai-council JOURNAL-backfill instruction sent to
  its architect) → **(2) build the Informant Organ** (read-only per-consumer × per-organ coverage
  reporter: enforcing-local / absent) — **low-regret, correct regardless of mesh-model, gives the mesh
  work its acceptance signal; its file path is a new-path decision needing operator approval** →
  **(3) build the mesh carrier** — **the located Fable consult** → (4) record the lesson (LESSONS +
  PLAYBOOK: *deployed presence ≠ deployed enforcement; done only when enforcement-in-effect is
  demonstrated — the configured→armed→proven distinction, generalized to the mesh*).
- **The core fork (→ Fable RULES, CC IMPLEMENTS):** the **mesh-transfer model** — **(A)** mesh as a
  **5th carrier**, organs run locally inside each consumer; **(B) hub-sweep-as-mesh**, the hub runs
  `audit.py` against the fleet on a cadence (must actually run, not "when I remember"); **(C) hybrid** —
  fail-closed organs (JOURNAL) go local via (A), awareness organs (freshness/drift) go hub-sweep via
  (B). **Tension:** local enforcement (autonomy/immediacy) **vs the Layer-2 autonomy-no invariant** — a
  hub pushing running hooks into consumers on a schedule brushes against "hub initiates no autonomous
  cross-repo writes." Contested + high-stakes + no-obvious-answer + a Layer-2-invariant tension → clears
  the routing bar for a Fable consult. **Feed Fable the fleet-map, not an n=1 sample.**
- **OPEN:** mesh-model A/B/C (→ Fable); per-organ local-vs-hub assignment (JOURNAL clearly local;
  `git_backlog_drift` + coherence spine may be inherently hub-scoped); Informant-Organ file path
  (operator approval); does #139 (merged-arc→record) + #170/#168 (arc-tracking spine) fold into this
  work-stream (likely yes — record-integrity family); **the #168-hard vs Fable-WARN conflict** (#168's
  Done-when says promote the JOURNAL leg to fail-closed HARD; Fable consult #1 ruled arc-tracking stays
  WARN with no-item disposition) — **unresolved.**
- **DON'T lose the un-merged Fable consult #1 rulings** (accepted, disposition pass halted by the
  re-scope — fold into the next session or they die in the outgoing chat): leg-(e) functional-proof into
  ADR-81; undeclared-edge scan → ship-gate WARN; immutability re-scope (status-line mutable on
  ratification, decision-content frozen — narrows core-invariant #5, operator sign-off pending);
  ai-council wiring lane-split (architect frames, CC mechanically expands).

**The prior three-goal priority — DEMOTED to sequenced-after (real, kept, not deleted):**
- **(a) FABLE whole-system review + merge rulings** — but note the **mesh-model ruling (step 3 above)
  is now the highest-value remaining use of the perishable Fable window**; the drafted §7 system-audit
  review-ask is real but sequenced behind the mesh consult. Input:
  `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`.
- **(b) Wire ai-council as a CC-GOVERNED query mechanism** (`/council` via the plugin carrier;
  browser → CC → ai-council; CC owns the mechanical lifecycle, architect owns question-framing) —
  **designed, not built.** Sequenced after the mesh gap.
- **(c) Close the two methodology tracks — ADR + ai-council.** **Unblocked this window:** #170/#168
  were verified-at-source as **arc-tracking** (issue-ID↔commit anchor, same family as #139), **NOT
  ADR-lifecycle — the prior handoff mis-filed them as the ADR sticking point.** So ADR-methodology
  closure is less blocked than believed; **(b)+(c) remain one work-stream**, sequenced after the mesh gap.

**Fleet #221 + the hardening items — sequenced AFTER (demoted, not deleted):**
- **#221 — fleet rollout** (gated by intent, not dependency): run `deploy/tool.py` on corp-monorepo /
  corp-ops / corp-sca-time-automation to reach n=2+, each using **#230** as its acceptance gate; done-when
  also requires **#225** (surgical precommit carrier) closed. Scaling to n=3 before merging Fable's rulings
  would propagate a soon-to-change methodology. Carry the pilot rule: **treat each consumer's `.gitignore` +
  config shape as an UNKNOWN to probe, not a copy of the hub** (prior SUPPLEMENT §B; LESSONS 2026-07-01).
  **Rejected — do NOT onboard corp-monorepo now** (supplement §3): it was deliberately sequenced last so
  this gap would surface on the n=1 pilot; onboarding it through the **current** deploy subsystem would
  inherit the same enforcement-mesh gap — **do not onboard until the mesh carrier + Informant Organ are
  proven.**
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
- **The priority "why" (READ FIRST — the P0 re-scope):** THIS bundle's FILLED `SUPPLEMENT.md` ANSWERS —
  the enforcement-mesh finding (5/5 organs ABSENT fleet-wide), the decomposition (Informant Organ → mesh
  carrier → Fable consult on A/B/C), the "deployed presence ≠ deployed enforcement" lesson, the rejected
  paths (§3), and the un-merged Fable consult #1 rulings (§6). **Authoritative on priority; P0.** The PRIOR
  bundle's supplement (`docs/handoffs/2026-07-02-dev-knowledge-architect/SUPPLEMENT.md`) holds the now-demoted
  three-goal priority — read it for that context, but it is **superseded** on priority.
- **The Fable review input (demoted goal a):** `docs/audits/2026-07-02-comprehensive-system-audit-for-external-review.md`
  (the system audit + the review-ask) — sequenced behind the mesh-model Fable consult.
- **The arm-first arc's "why" (sealed backdrop):** **ADR-93** (floor model A, armed + conformance-proven),
  `LESSONS.md`, PLAYBOOK §20, `deploy/` (tool.py + carriers + `carrier_floor.py`), and the prior bundle's
  `RESIDUAL.md`/`HANDOFF_BOOT.md`.
- **This window's captures:** `JOURNAL.md` top entry (`b255a8c`, the prune) + `ecosystem/disposition-register.yaml`;
  the enforcement finding is off-repo (browser-side, CC-verified live) — it lives in the folded `SUPPLEMENT.md`.
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
