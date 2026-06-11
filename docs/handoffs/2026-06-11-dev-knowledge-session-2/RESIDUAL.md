# Residual — 2026-06-11, **architect mode** (v5 beta §13)

<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the
> **open architecture questions**, and the **task-graph** — carried as *ephemeral residual
> prose*, **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a
> footnote. Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at the 2026-06-11
> surface-responsibility-audit merge HEAD; working tree clean at generation.
>
> **Scope of this handoff.** It boots a *planning* session on the **way-of-working** — the
> handoff-methodology arc (v5 → canonical, the two-mode design, the resident-copy-drift
> cleanups). It does **not** advance a single ticket; that is execution mode. Orient first
> (`PROBES.md` P1), then resume the design — do not rediscover it.

---

## 1. Drift-flags — the headline

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus
CC's state read at generation. **A flag is a question, not a verdict.**

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable)*

`validate_git_backlog` flags a `closes [#77]` merge whose `[#77]` is still present (open) in
`BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** `ecosystem/disposition-register.yaml` → `warn-77-voided-closure`. The
  merge carried `closes [#77]` but shipped *different* work (CONTRIBUTING→v4, not the
  protocols-consolidation #77 names) — #77 was **re-scoped, not done**, so it legitimately
  stays open (corrected 2026-06-09). Direction-(a) #90a cannot tell a misattributed closure
  from a real one; only arc-content inspection (**#139** / #90b) can — which is why the
  register auto-clears this entry once #139 ships.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational) and
  still exits OK; the ship-gate suppresses the single WARN via the register.
- **The lesson the validator line can't carry:** "this is fine" lives in the register + the
  git arc, **not** in the one-line validator output. A receiver treating every flag as an
  action item would "close" a correctly-open ticket. **Consult the register before acting on
  any #90 flag.**
- **Confirm:** `python scripts/validate_git_backlog.py` + read `ecosystem/disposition-register.yaml`.

### No `doc_claims` (#89) drift at generation *(state note — a prior flag is now resolved)*

The first v5 dogfood (sibling bundle `2026-06-11-dev-knowledge-session/`) headlined a
**DRIFT-1**: `ARCHITECTURE.md`'s `**N collected**` test-count was stale. **That is now
reconciled** — the Phase-0 foundation-stabilization session re-stamped it, and `audit.py
health` reports `doc_claims` all-match at this generation. Re-derive, don't trust this line:
**P6** in `PROBES.md` forces the live check (the count drifts on any test change; if it has
drifted again since generation, P6 catches it).

### State note — a **leftover branch** to prune *(housekeeping, not a drift-check flag)*

`docs/arch-coherence-audit` is **merged** into `main` (merge `c3c2513`) but **undeleted**.
Per the repo's "no leftovers" invariant (CLAUDE.md §5 #9) it should be pruned — but **ask the
operator before deleting any branch** (core-invariant #3). Surfaced, not actioned.
`git branch --merged main` to confirm; this handoff's own branch is the only *other* non-`main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

Not in git/JOURNAL/BACKLOG (which record *what shipped*, not the design reasoning behind the
open questions). The way-of-working arc over the last several 2026-06-11 sessions weighed:

1. **Resident-copy drift is the class this repo exists to kill — and it keeps recurring on
   the repo's *own* self-description.** Two same-day audits found it twice: PLAYBOOK
   §"System Architecture" was a *stale hand-copy* of `ARCHITECTURE.md`'s layer model (showed
   the browser producing handoffs; "Layer 2 never executes" — both contradicted by the canon
   at `ARCHITECTURE.md:106` / `:130-134`), and `CLAUDE.md` defines the file-lifecycle rule
   **twice in one file** (§4:54 ↔ §5:69-71). The settled design *direction*: **single
   authority + pointer everywhere** (`source → gate → agent`) — fix drift by *replacing the
   copy with a pointer*, never by editing the copy's content so nothing is left to sync.
   The **open** part is sequencing + the canonical-home decisions (§4 below).
2. **Fake-green avoidance shaped #150's closure.** The two-mode switch + the orientation layer
   **landed** on the v5-beta track, but **#150 was deliberately kept OPEN**: the durable,
   BACKLOG-resident task-graph (deps/parallelization) was *not* built — that would be a fake
   "done." This pass scopes the architect task-graph to the **ephemeral residual** (this very
   §5) and mints **#156** as the named successor for the durable schema. The tension —
   *ship the readable orientation now vs. wait for the durable graph* — was resolved
   ship-now-defer-durable, on the operator's ruling.
3. **Teeth vs. orientation (the scope-D gap).** The v5 *execution* bundle had teeth but **no
   readable big-picture** — a fresh architect could verify a sha but not answer "what is this
   project." Re-narrating VISION into the handoff was barred (§2/§3 no-copy) *and* a
   plain-language answer is **summary-bluffable** (fails §5's own bar). The resolution
   delivered: an **exact-line-quote probe** (§5 manifest row) bound to `VISION.md` +
   `ARCHITECTURE.md` Ch1 — **forced read, never copied, never paraphrased**. "Readable-first"
   becomes a *verified property of the handoff* with **zero content copied**. This bundle is
   the first to actually carry it (P1).
4. **Parallel-ship invisibility is load-bearing until the flip.** v5 must stay invisible to
   the `audit.py` coupling gates (`amendment_coherence` / `handoff_version_stamp`) until **one
   atomic flip commit** — so the canonical `Version:` line and its ~5 gated + ~10 *non-gated*
   prose surfaces move together. The tension — *promote piecemeal vs. one atomic flip* — was
   resolved atomic-flip, gated on Council + fresh-eyes + the empirical-teeth dogfood (the
   sibling bundle rehearsed gate 3).

## 3. Pointers (paths — read these live; do not copy them into the handoff)

- **Process (v5, beta, governing this handoff + its modes):** `protocols/HANDOFF_PROCESS_v5.md`
  (architect mode = §13); thin boot `protocols/HANDOFF_BOOT.md` (carries both postures).
- **Process (canonical, still authoritative for real handoffs):** `protocols/HANDOFF_PROCESS.md` (v4.4).
- **Orientation sources (P1 — read live, never copied):** `VISION.md` `## Vision`;
  `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`).
- **Methodology (referenced, never copied):** `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md`.
- **The two audits that mapped this arc:** `docs/audits/2026-06-11-architecture-coherence-audit.md`
  (scopes A–F), `docs/audits/2026-06-11-surface-responsibility-audit.md` (responsibility map +
  PLAYBOOK extraction classification).
- **Decision record:** `docs/decisions/ADR-82-*.md` (Proposed — Council-pending, ADR-41 routing).
- **Drift-check sources:** `scripts/validate_doc_claims.py` (#89), `scripts/validate_git_backlog.py` (#90),
  `ecosystem/disposition-register.yaml`.
- **Task spec:** `BACKLOG.md` — the way-of-working theme is #149 · #150 · #151 · #152 · #153 ·
  #155 · #156 · #157 · #158.

---

## 4. Open architecture questions (architect §13d — surfaced, not buried)

The design decisions **not yet made** — so the next session resumes the design rather than
rediscovering it. Each is a *question*, with the ticket that holds it:

- **Q1 — Responsibility-matrix canonical home.** The surface-responsibility audit mapped each
  governance surface → its one job but **deliberately did not ticket** the "where does the
  responsibility matrix live durably" decision — that is *this* architect session's call. Open:
  does it live in `ARCHITECTURE.md` (organ map), a new doc, or stay an audit artifact?
- **Q2 — The 4-way file-lifecycle authority.** The append-only/immutable disposition is stated
  in `CLAUDE.md` §4 **and** §5, in `ARCHITECTURE.md`, and in the rules — which one is the single
  authority, and do the others become pointers? (#157 fixes the *intra-CLAUDE.md* duplication;
  the cross-file 4-way decision is unticketed, mapped for here. Coordinate with **#112** —
  also edits §5: the supersede-vs-never-edit contradiction.)
- **Q3 — How much PLAYBOOK extracts, and to where.** The audit classifies the *majority* of
  PLAYBOOK as extractable. #158 carries the *high-confidence* pointerizations
  (§"Repo conventions" → its ADRs; Appendices A/B/C → `~/.claude` / `CLAUDE.md`). The **deeper
  per-section extraction** (procedures → skills) is *mapped, not pre-committed* — this session
  decides scope/sequence, not a big-bang rewrite.
- **Q4 — #150 closes on the durable task-graph schema (#156).** Decide the ADR-66 schema
  amendment: `depends-on` / `parallel` fields + a `validate_backlog` extension (reference
  existence + no cycle). Until then the graph is *only* §5 below — ephemeral.
- **Q5 — Enforcement-completeness (#153).** The `--no-ff` FF-guard shipped as
  detect-and-surface (no pre-push *prevention*). Decide per remaining prose-only constraint
  (minimal-diffs / append-only / no-CHANGELOG-recreation): **mechanize, or accept-as-prose
  with a reason.** True FF *prevention* (pre-push hook) is noted as deferred machinery.
- **Q6 — Loops architecture (#155).** Operator-flagged, **scope TBD** — VERIFY-FIRST with the
  operator what "loops architecture" means (in-session backpressure #126 · `/loop` persistence
  ADR-74 · night/Routine cadence · the Ch6 verification-mesh outcome loop) before any design.
- **Q7 — The #149 flip choreography.** The atomic flip moves 5 gated surfaces (the coupling
  gates force atomicity) **plus ~10 non-gated prose surfaces** (#151). Open: ship a **durable
  prose-drift gate** covering the ungated set, or a one-shot checklist? (The audit recommends
  the gate.) Gated on Council ratification of ADR-82 + one fresh-eyes beta→stable review (the
  empirical-teeth dogfood is rehearsed).

---

## 5. The task-graph — **ephemeral residual prose, NOT a durable BACKLOG field** (architect §13b)

> **Honest scope (v5 §13b).** The BACKLOG schema (ADR-66 / `validate_backlog`) encodes **no**
> dependencies or parallelization. This graph is carried **in the residual, ephemerally** — it
> is **not** a durable, BACKLOG-resident graph and must not be presented as one. Durable
> encoding is **#156**. Read it as *the architect's current read of the arc*, to be re-derived
> against the live `BACKLOG.md`, not a committed structure.

**The way-of-working arc, as a dependency read:**

- **Root / blocking spine:** **#149** (v5 → canonical flip) is the keystone. It **blocks**:
  - **#151** (flip doc-sync of the ~10 non-gated surfaces) — happens *at* the flip.
  - the §8-half of **#152** (pointerize PLAYBOOK §8 → HANDOFF_PROCESS) — deferred *to* the
    flip because §8 describes the handoff being redesigned.
  - **#150**'s final close — #150 stays open until the durable-graph decision (**#156**), and
    its orientation/mode work already landed on the v5-beta track.
- **#149's own three gates** (all upstream of the flip): Council ratifies ADR-82 · one
  fresh-eyes beta→stable review · the empirical-teeth dogfood (**rehearsed** by the sibling
  bundle). These are *external* (Council) or *review* gates, not code.
- **Parallelizable now (independent of the flip):**
  - **#157** (collapse intra-`CLAUDE.md` file-lifecycle restatement) — small; coordinate with
    **#112** (same §5) to avoid a collision.
  - **#158** (high-confidence PLAYBOOK pointerizations) — incremental, each operator-approved
    before landing.
  - **#153** (enforcement-completeness remaining constraints) — FF-guard already shipped.
  - **#155** (loops architecture) — gated only on the operator's VERIFY-FIRST scope.
- **#156** (durable task-graph schema) is the **enabler that retires this very section** — once
  it ships, the architect emits a durable graph instead of this prose, and **#150 closes**.

**Net:** the flip (#149) is the critical path; the cleanups (#157/#158/#153/#155) run in
parallel beside it; #156 is the meta-item that makes the *next* architect handoff carry a real
graph instead of residual prose.

---

## 6. Lean task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets** — `BACKLOG.md` is the source; do not re-narrate
IDs here. State at generation:

- **Theme pointer (architect §13b):** the **way-of-working** theme in `BACKLOG.md` —
  #149 · #150 · #151 · #152 · #153 · #155 · #156 · #157 · #158. Read the live file; the §5
  graph above is the *ephemeral* dependency read over exactly these.
- **Live branches:** `main` (clean at generation) + this handoff's own branch
  (`docs/handoff-2026-06-11-architect`, merges on completion) + the **merged-but-undeleted**
  `docs/arch-coherence-audit` (prune-candidate, §1 — ask first). `git branch -v` to confirm at
  read-time.
- **Task-state drift-flag:** #77 — dispositioned voided closure (§1 above); **not work.**
