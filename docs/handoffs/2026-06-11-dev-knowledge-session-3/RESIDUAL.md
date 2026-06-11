# Residual — 2026-06-11 session-3, **architect mode** (v5 beta §13)

<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the
> **open architecture questions**, and the **task-graph** — carried as *ephemeral residual
> prose*, **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a
> footnote. Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at the
> operator-context-beat merge HEAD (`22f6030`), working tree clean, `main` pushed and
> **in-sync** with `origin/main` at generation.
>
> **Scope of this handoff.** It boots a *planning* session on the **way-of-working** — the
> handoff-methodology arc (v5 → canonical, the two-mode design, the operator-context beat,
> the resident-copy-drift cleanups). It does **not** advance a single ticket; that is
> execution mode. Orient first (`PROBES.md` P1), **then ask the operator for off-repo
> context** (the beat shipped this very session — §13d), then resume the design — do not
> rediscover it.

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
  stays open. Direction-(a) #90a cannot tell a misattributed closure from a real one; only
  arc-content inspection (**#139** / #90b) can — which auto-clears this entry once #139 ships.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational) and
  still exits OK.
- **Consult the register before acting on any #90 flag.** Treating the flag as an action item
  would "close" a correctly-open ticket.
- **Confirm:** `python scripts/validate_git_backlog.py` + read `ecosystem/disposition-register.yaml`.

### No `doc_claims` (#89) drift at generation *(state note)*

`audit.py health` reports `doc_claims` all-match at this generation (3 self-claims verified).
Re-derive, don't trust this line: **P6** in `PROBES.md` forces the live check (the
`ARCHITECTURE.md` `**N collected**` count drifts on any test change).

### State note — **two leftover branches** to prune *(housekeeping, not a drift-check flag)*

Per the "no leftovers" invariant (CLAUDE.md §5 #9), two branches are **merged into `main` but
undeleted** — but **ask the operator before deleting any branch** (core-invariant #3):

- `docs/arch-coherence-audit` (`b9fa4c4`) — merged, undeleted (carried since session-2).
- `docs/handoff-2026-06-11-architect` (`e6b163e`) — session-2's own handoff branch, merged
  (`53f775d`), undeleted.

Both surfaced, **not actioned**. `git branch --merged main` to confirm; this handoff's own
branch (`docs/handoff-2026-06-11-session-3`) merges on completion. NB session-2's residual
flagged only the first; the second accrued because the session-2 handoff branch was never
pruned after its own `--no-ff` merge — the same leftover class, now n=2.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

Not in git/JOURNAL/BACKLOG (which record *what shipped*, not the design reasoning). The
way-of-working arc — including **this session's** operator-context beat — weighed:

1. **Operator-context beat (Change B — shipped this session).** CC's handoff is
   **repo-derived**: it structurally *cannot* carry operator intent or off-repo findings. The
   local proof was sharp — this arc's own `profile ↔ repo` overlap finding was **browser-side**
   (the operator's user-preferences profile is not in the repo) and was **nearly lost** because
   the architect handoff had no channel for it. Resolution: a **lightweight operator-context
   beat** in *architect mode only* — after orienting, before design, the browser makes **one**
   targeted ask for off-repo context (intent / priorities / off-repo findings / changed
   decisions). Tensions resolved: **(a)** architect-only vs both modes → **architect-only**
   (human-in-the-loop steering belongs at the strategic/planning layer, not the tactical
   execution layer); **(b)** lightweight one-ask vs the heavy v4 eight-file interview →
   **one ask** — it is the v4 interview's *operator-injection* function **without** the
   gap-filling (the residual fills gaps now); **(c)** off-repo-only vs re-narrating the residual
   → **off-repo-only**, so it does not duplicate the CC-generated residual. Landed as
   `HANDOFF_PROCESS_v5` §13(d) + a `HANDOFF_BOOT.md` architect-posture step + two test fences;
   tracked **open** as **#159** (it is *unproven in a real architect session* and must survive
   the #149 flip — no fake-green). **Change A** (demote the orientation probe / P1) is
   **parked** — out of scope pending a real empirical signal. *This handoff dogfoods the beat
   it shipped — the browser will exercise it after P1.*
2. **Resident-copy drift is the class this repo exists to kill — and it keeps recurring on the
   repo's *own* self-description.** Two same-day audits found it: PLAYBOOK §"System Architecture"
   was a stale hand-copy of `ARCHITECTURE.md`'s layer model, and `CLAUDE.md` defines the
   file-lifecycle rule **twice in one file** (§4:54 ↔ §5:69-71). Settled *direction*: **single
   authority + pointer everywhere** (`source → gate → agent`) — fix drift by *replacing the
   copy with a pointer*, never by editing the copy. The **open** part is sequencing + the
   canonical-home decisions (§4).
3. **Fake-green avoidance shaped #150's (and now #159's) closure.** The two-mode switch +
   orientation layer **landed**, but **#150 stays OPEN** (the durable BACKLOG-resident
   task-graph was *not* built — that would be a fake "done"; named successor **#156**).
   **#159** follows the same discipline — the beat shipped but stays open pending real-session
   use + the flip. Ship-now-defer-durable, on the operator's ruling.
4. **Teeth vs. orientation (the scope-D gap).** The v5 execution bundle had teeth but **no
   readable big-picture**. Re-narrating VISION was barred (§2/§3) *and* a plain-language answer
   is summary-bluffable (fails §5's bar). Resolution: an **exact-line-quote probe** bound to
   `VISION.md` + `ARCHITECTURE.md` Ch1 — forced read, never copied/paraphrased (P1). The
   operator-context beat (point 1) is the *next* layer after orientation: orient from the repo,
   then inject what the repo cannot hold.
5. **Parallel-ship invisibility is load-bearing until the flip.** v5 stays invisible to the
   `audit.py` coupling gates until **one atomic flip commit** (#149) moves the canonical
   `Version:` + its ~5 gated + ~10 non-gated prose surfaces together. Resolved atomic-flip,
   gated on Council + fresh-eyes + the empirical-teeth dogfood.

## 3. Pointers (paths — read these live; do not copy them into the handoff)

- **Process (v5, beta, governing this handoff + its modes):** `protocols/HANDOFF_PROCESS_v5.md`
  (architect mode = §13; the operator-context beat = **§13(d)**); thin boot
  `protocols/HANDOFF_BOOT.md` (carries both postures + the new operator-context step).
- **Process (canonical, still authoritative for real handoffs):** `protocols/HANDOFF_PROCESS.md` (v4.4).
- **Orientation sources (P1 — read live, never copied):** `VISION.md` `## Vision` (line 11);
  `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`, line 47).
- **Operator-context beat — fences + grounding:** `tests/test_handoff_modes.py`
  (`test_v5_architect_carries_operator_context_beat`, `test_boot_architect_posture_carries_operator_context_step`);
  grounding = `docs/audits/2026-06-11-surface-responsibility-audit.md` "Noted limitation
  (out of scope here)" (profile↔repo overlap is browser-side, repo-blind — the channel the beat
  fills). NB the audit has **no literal "Q2"** — that grounding lives in the noted-limitation.
- **Methodology (referenced, never copied):** `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md`.
- **The two audits that mapped this arc:** `docs/audits/2026-06-11-architecture-coherence-audit.md`
  (scopes A–F), `docs/audits/2026-06-11-surface-responsibility-audit.md`.
- **Decision record:** `docs/decisions/ADR-82-*.md` (Proposed — Council-pending, ADR-41 routing).
- **Drift-check sources:** `scripts/validate_doc_claims.py` (#89), `scripts/validate_git_backlog.py` (#90),
  `ecosystem/disposition-register.yaml`.
- **Task spec:** `BACKLOG.md` — the way-of-working theme is #149 · #150 · #151 · #152 · #153 ·
  #155 · #156 · #157 · #158 · **#159** (new this session).

---

## 4. Open architecture questions (architect §13d — surfaced, not buried)

The design decisions **not yet made** — so the next session resumes the design rather than
rediscovering it. Each is a *question*, with the ticket that holds it:

- **Q1 — Responsibility-matrix canonical home.** Where does the responsibility matrix live
  durably — `ARCHITECTURE.md` (organ map), a new doc, or stay an audit artifact? (Mapped, not
  ticketed — this session's call.)
- **Q2 — The 4-way file-lifecycle authority.** The append-only/immutable disposition is stated
  in `CLAUDE.md` §4 **and** §5, in `ARCHITECTURE.md`, and in the rules — which is the single
  authority, and do the others become pointers? **#157** fixes the intra-`CLAUDE.md`
  duplication; the cross-file 4-way decision is unticketed. Coordinate with **#112** (also
  edits §5 — the supersede-vs-never-edit contradiction).
- **Q3 — How much PLAYBOOK extracts, and to where.** #158 carries the high-confidence
  pointerizations; the deeper per-section extraction (procedures → skills) is *mapped, not
  pre-committed* — this session decides scope/sequence, not a big-bang rewrite.
- **Q4 — #150 closes on the durable task-graph schema (#156).** Decide the ADR-66 amendment:
  `depends-on` / `parallel` fields + a `validate_backlog` extension. Until then the graph is
  *only* §5 below — ephemeral.
- **Q5 — Enforcement-completeness (#153).** The `--no-ff` FF-guard shipped as
  detect-and-surface (no pre-push *prevention*). Decide per remaining prose-only constraint
  (minimal-diffs / append-only / no-CHANGELOG-recreation): **mechanize, or accept-as-prose
  with a reason.**
- **Q6 — Loops architecture (#155).** Operator-flagged, **scope TBD** — VERIFY-FIRST with the
  operator what "loops architecture" means before any design.
- **Q7 — The #149 flip choreography.** The atomic flip moves 5 gated + ~10 non-gated prose
  surfaces (#151). Ship a **durable prose-drift gate** or a one-shot checklist? Gated on Council
  ratification of ADR-82 + one fresh-eyes beta→stable review (the empirical-teeth dogfood is
  rehearsed; **the operator-context beat must be exercised at least once** before the flip —
  Q8).
- **Q8 — Validating + carrying the operator-context beat (#159, new).** The beat shipped but is
  **unproven in a real architect session** — *this handoff is the first to carry it*; run it and
  judge whether one targeted ask is the right weight (vs. too-light / too-heavy), then decide
  whether it carries through the #149 flip unchanged. **Confirmed closed sub-question:**
  architect-only is settled — **no** operator-context beat in execution mode (the
  strategic-vs-tactical split). **Open companion:** Change A (demote P1) stays parked until a
  real signal says orientation should move.

---

## 5. The task-graph — **ephemeral residual prose, NOT a durable BACKLOG field** (architect §13b)

> **Honest scope (v5 §13b).** The BACKLOG schema encodes **no** dependencies or parallelization.
> This graph is carried **in the residual, ephemerally** — not a durable, BACKLOG-resident
> graph. Durable encoding is **#156**. Read it as *the architect's current read of the arc*, to
> be re-derived against the live `BACKLOG.md`.

**The way-of-working arc, as a dependency read:**

- **Root / blocking spine:** **#149** (v5 → canonical flip) is the keystone. It **blocks**:
  - **#151** (flip doc-sync of the ~10 non-gated surfaces) — happens *at* the flip.
  - the §8-half of **#152** (pointerize PLAYBOOK §8 → HANDOFF_PROCESS) — deferred *to* the flip.
  - **#150**'s final close — stays open until the durable-graph decision (**#156**).
  - **#159**'s carry — the operator-context beat carries through the flip to canonical (or is
    re-decided there); its *open* status also depends on a real-session exercise (Q8).
- **#149's own three gates** (upstream of the flip): Council ratifies ADR-82 · one fresh-eyes
  beta→stable review · the empirical-teeth dogfood (**rehearsed**). Add a soft gate: **#159's
  beat exercised once** (this session is the candidate).
- **Parallelizable now (independent of the flip):**
  - **#157** (collapse intra-`CLAUDE.md` file-lifecycle restatement) — coordinate with **#112**
    (same §5).
  - **#158** (high-confidence PLAYBOOK pointerizations) — incremental, each operator-approved.
  - **#153** (enforcement-completeness remaining constraints) — FF-guard already shipped.
  - **#155** (loops architecture) — gated only on the operator's VERIFY-FIRST scope.
  - **#159** (operator-context beat) — *landed*; remaining work is *validate-in-session* + the
    flip-carry, not new build.
- **#156** (durable task-graph schema) is the **enabler that retires this very section** — once
  it ships, the architect emits a durable graph instead of this prose, and **#150 closes**.

**Net:** the flip (#149) is the critical path; the cleanups (#157/#158/#153/#155) and the
beat-validation (#159) run in parallel beside it; #156 is the meta-item that makes the *next*
architect handoff carry a real graph instead of residual prose.

---

## 6. Lean task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets** — `BACKLOG.md` is the source; do not re-narrate
IDs here. State at generation:

- **Theme pointer (architect §13b):** the **way-of-working** theme in `BACKLOG.md` —
  #149 · #150 · #151 · #152 · #153 · #155 · #156 · #157 · #158 · **#159**. Read the live file;
  the §5 graph above is the *ephemeral* dependency read over exactly these.
- **Live branches:** `main` (clean + pushed/in-sync with `origin/main` at generation) + this
  handoff's own branch (`docs/handoff-2026-06-11-session-3`, merges on completion) + **two
  merged-but-undeleted** branches (`docs/arch-coherence-audit`, `docs/handoff-2026-06-11-architect`
  — prune-candidates, §1, ask first). `git branch -v` to confirm at read-time.
- **Task-state drift-flag:** #77 — dispositioned voided closure (§1 above); **not work.**
