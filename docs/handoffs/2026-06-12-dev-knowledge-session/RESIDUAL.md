# Residual — 2026-06-12 session, **architect mode** (v5 canonical §13)

<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the
> **open architecture questions**, and the **task-graph** — carried as *ephemeral residual
> prose*, **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a
> footnote. Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at HEAD
> `d6538ed`, working tree clean, **`main` ahead 1 / behind 1 of `origin/main`** at generation
> (a real divergence — §1).
>
> **Scope of this handoff.** It boots a *planning* session on the **way-of-working** — now
> specifically **finishing the v5 handoff machinery deferred at the #149 flip**: the v5
> `/handoff` **generator** (#164) and the read-only **teeth validator** (#163), plus the
> carried-open cleanups (§8 pointerization #152, the architect actor-vs-mode vocab #162, the
> probe-core #161, the durable task-graph schema #156, the operator-context-beat exercise
> #159). It does **not** advance a single ticket; that is execution mode. Orient first
> (`PROBES.md` P1), **then ask the operator for off-repo context** (§13d), then resume the
> design — do not rediscover it.

---

## 1. Drift-flags — the headline

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus
CC's state read at generation. **A flag is a question, not a verdict.**

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still
present (open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** `ecosystem/disposition-register.yaml` → `warn-77-voided-closure` (match
  `77e5d7d`). The merge carried `closes [#77]` but shipped *different* work — #77 was
  **re-scoped, not done**, so it legitimately stays open. Direction-(a) #90a cannot tell a
  misattributed closure from a real one; only arc-content inspection (**#139** / #90b) can —
  which auto-clears this entry once #139 ships.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational) and
  still exits OK (17/18 pass, health OK at generation).
- **Consult the register before acting on any #90 flag.** Treating the flag as an action item
  would "close" a correctly-open ticket.
- **Confirm:** `python scripts/validate_git_backlog.py` + read `ecosystem/disposition-register.yaml`.

### No `doc_claims` (#89) drift at generation *(state note)*

`audit.py health` reports `doc_claims` all-match at this generation (3 self-claims verified).
Re-derive, don't trust this line: **P6** in `PROBES.md` forces the live check (the
`ARCHITECTURE.md` `**N collected**` count drifts on any test change).

### STATE NOTE — `main` is **ahead 1 / behind 1** of `origin/main` *(housekeeping, ask the operator — not a drift-check flag)*

At generation, `git status -sb` shows `main [ahead 1, behind 1]`. The local `ahead 1` is the
`d6538ed` fleet-audit baseline commit; the `behind 1` is a commit on `origin/main` not yet
pulled. This is a **genuine sync divergence** — a `git pull --rebase` (or a reconcile) is
owed before the next push, and it is **not actioned here** (ask the operator first;
core-invariant #4 wants a clean, in-sync tree before new work). **Confirm at read-time:**
`git status -sb` + `git log --oneline origin/main..main` and `git log --oneline main..origin/main`.
NB this is the P3 teeth probe's live answer — re-derive, don't trust this paragraph.

### No leftover branches *(state note)*

Unlike session-3, `git branch -v` shows **only `main`** at generation (the two merged-but-
undeleted branches from the session-3 arc were pruned in the 2026-06-11 arc-cleanup). This
handoff's own branch (`docs/handoff-2026-06-12-session`) merges on completion via `--no-ff`.
`git branch --merged main` to confirm no straggler accrues.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

Not in git/JOURNAL/BACKLOG (which record *what shipped*, not the design reasoning). The
arc since the last handoff (session-4) and the design tensions this planning session inherits:

1. **The #149 flip LANDED — the machinery is now *specified* but not fully *built*.** On
   2026-06-12 the keystone flip promoted v5 to canonical (`Version 5.0` / `Status stable`),
   archived v4.4 (ADR-83 tombstone), moved the 4 gate-coupled surfaces + the ~10 non-gated
   prose surfaces (#151) atomically, and closed #149/#151/#160/#148/#124/#25. **Two
   deferrals were conscious operator rulings**, captured as tickets so the flip stayed atomic:
   - **#164 — the v5 `/handoff` generator.** The `.claude/commands/handoff.md` body **still
     carries the v4 8-file two-phase generator, marked SUPERSEDED**, and `SESSION_SETUP.md`'s
     two-phase flow likewise. The v5 emissions (residual + probe manifest + thin-boot pointer
     + lean task-state) are *specified* but not yet the *wired generator*.
   - **#163 — the read-only teeth validator** `scripts/verify_handoff_probes.py`. It would
     validate a v5 bundle's probe manifest (each command PASSes against live state; each
     forced-read probe is **not** answerable from the compaction summary alone). Deferred
     because audit checks #8/#9 degrade cleanly without it; until it lands the **manual
     probe-gate** (`HANDOFF_PROCESS.md` §5 / `PROBES.md`) covers v5 verification.
2. **This very handoff is the live argument for #164 (and #161).** It was **hand-assembled by
   CC** following the v5 spec — the generator does not exist yet, so the probe set (P1–P6) was
   **assembled by hand**, exactly the toil #161 (stable probe-core) names and #164 (generator)
   removes. The self-referential proof: the SUPERSEDED v4-shaped command produced a v5-shaped
   bundle by the operator + CC reading the spec, not by machine. *That gap is the work.*
3. **The architect "architect" collision is still live (#162).** "architect" means two things
   on overlapping surfaces — the Layer-1 **actor** (the browser-chat role, ARCHITECTURE.md /
   ADR-28) **and** the handoff **mode** (`architect|execution`, HANDOFF_PROCESS §13 /
   HANDOFF_BOOT). Only a narrow slice shipped (the 2026-06-11 boot-ack now says "Layer-1
   browser", no on-load mode claim); the **model decision** — rename one sense or formally
   scope both, **atomically across every enumerated surface** — remains. Leaving it live risks
   exactly the kind of two-readings-one-term defect the repo exists to kill.
4. **Resident-copy drift keeps recurring on the repo's *own* handoff self-description (#152).**
   The flip repointed PLAYBOOK §8's *authority* v4→v5 (#151), but §8 still **describes** the
   v5 handoff rather than being a **pure pointer** to `HANDOFF_PROCESS.md`. Settled
   *direction*: replace the copy with a pointer (`source → gate → agent`), never edit the
   copy. The **open** part is doing the §8-half now that the flip has landed (its blocker is
   gone).
5. **Ship-now-defer-durable shaped #150/#159 — and now bounds #156.** The two-mode switch +
   orientation layer + operator-context beat all **landed**, but **#150 stays open** because
   the durable BACKLOG-resident task-graph (deps/parallelization) was *not* built — that would
   be fake-green. The named successor is **#156** (ADR-66 amendment + `validate_backlog`
   extension). The task-graph in §5 below is therefore **still ephemeral residual prose** —
   #156 is the meta-item that lets the *next* architect handoff carry a durable graph instead.
6. **#159 (operator-context beat) — the flip-carry is DONE; the real-session exercise is not.**
   The beat lives in the canonical spec §13(d); the only remaining clause is **exercising it in
   a real architect session**. *This handoff is a candidate* — orient via P1, then the off-repo
   ask, and judge whether one targeted ask is the right weight.

## 3. Pointers (paths — read these live; do not copy them into the handoff)

- **Process (v5, canonical, governing this handoff + its modes):** `protocols/HANDOFF_PROCESS.md`
  (architect mode = §13; orientation = §13(c); the operator-context beat = **§13(d)**;
  deferred machinery = §11 + §13 close-note); thin boot `protocols/HANDOFF_BOOT.md` (carries
  both postures + the operator-context step).
- **Archived prior process:** `protocols/archive/HANDOFF_PROCESS_v4.4.md` (ADR-83 tombstone);
  v4 templates `templates/archive/handoff-v4/`.
- **Orientation sources (P1 — read live, never copied):** `VISION.md` `## Vision` (line 11);
  `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`, line 47).
- **The deferred machinery (the spine of this session):** `.claude/commands/handoff.md` +
  `protocols/SESSION_SETUP.md` (both carry the v4 generator marked SUPERSEDED — #164 target);
  `scripts/audit.py` `check_handoff_bundle_structure` (the historical-v4 sibling #163 mirrors).
- **Operator-context beat — fences + grounding:** `tests/test_handoff_modes.py`
  (`test_v5_architect_carries_operator_context_beat`,
  `test_boot_architect_posture_carries_operator_context_step`,
  `test_boot_ack_is_mode_neutral`); grounding =
  `docs/audits/2026-06-11-surface-responsibility-audit.md` "Noted limitation" (profile↔repo
  overlap is browser-side, repo-blind — the channel the beat fills).
- **Methodology (referenced, never copied):** `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md`.
- **Decision records:** `docs/decisions/ADR-82-*.md` (operator-ratified; Council gate waived,
  #149); `docs/decisions/ADR-83-protocols-archive-convention.md`.
- **Drift-check sources:** `scripts/validate_doc_claims.py` (#89), `scripts/validate_git_backlog.py` (#90),
  `ecosystem/disposition-register.yaml`.
- **Task spec:** `BACKLOG.md` — the way-of-working theme (see §6).

---

## 4. Open architecture questions (architect §13e — surfaced, not buried)

The design decisions **not yet made** — so the next session resumes the design rather than
rediscovering it. Each is a *question*, with the ticket that holds it:

- **Q1 — Build order: validator (#163) or generator (#164) first?** They are independently
  shippable, but #163 (the read-only teeth validator) gives #164 (the generator) its
  *verification cadence* — a generator that emits a probe manifest wants a validator that
  proves the manifest bites. Decide: validator-first (teeth before automation) or
  generator-first (operators touch the command daily; this hand-assembly is the felt pain).
- **Q2 — #161 probe-core: scope it now, or keep capture-only?** Today every bundle
  hand-assembles its probe set (this one included), and the architect bundle historically
  lacked execution's §5-labels probe. Define a **stable shared probe-core (~5 forced-read
  probes) + the architect-only orientation probe** so #164 emits a fixed core instead of
  improvising — or explicitly defer. #161 is a natural **predecessor** to #164.
- **Q3 — #162 vocab disambiguation: rename one sense, or formally scope both?** Enumerate every
  surface where "architect" appears as actor vs mode and decide **atomically** (an ADR or
  operator ruling). Do not leave the collision live.
- **Q4 — #156 durable task-graph schema.** Decide the ADR-66 amendment: `depends-on` /
  `parallel` fields + a `validate_backlog` extension (reference existence + no cycle). Until
  then the graph is *only* §5 below — ephemeral; **#150 closes** when this lands.
- **Q5 — #152 §8 pointerization (blocker now cleared).** The flip landed, so PLAYBOOK §8 can
  become a **pure pointer** to `HANDOFF_PROCESS.md` rather than a v5 description. Decide:
  pointerize §8 now, or fold it into the #164 generator work (the generator's existence makes
  §8's "how" redundant).
- **Q6 — #158 PLAYBOOK pointerizations + #153 enforcement-completeness.** #158: §"Repo
  conventions" + Appendices A/B/C → pointers (incremental, each operator-approved). #153: for
  each remaining prose-only constraint (minimal-diffs / append-only / no-CHANGELOG-recreation)
  — **mechanize, or accept-as-prose with a reason** (the `--no-ff` FF-guard already shipped as
  detect-and-surface).
- **Q7 — #155 loops architecture.** Operator-flagged, **scope TBD** — VERIFY-FIRST with the
  operator what "loops architecture" means (in-session backpressure / `/loop` persistence /
  night-Routine cadence / verification-mesh outcome loop) before any design.
- **Q8 — #159: is one targeted ask the right weight for the operator-context beat?** *This
  handoff is the first real architect session to carry it* — run it, then judge too-light /
  right / too-heavy, and confirm it stays unchanged now that v5 is canonical. **Settled
  sub-question:** architect-only is final — **no** beat in execution mode (strategic-vs-tactical
  split).

---

## 5. The task-graph — **ephemeral residual prose, NOT a durable BACKLOG field** (architect §13b)

> **Honest scope (v5 §13b).** The BACKLOG schema encodes **no** dependencies or parallelization.
> This graph is carried **in the residual, ephemerally** — not a durable, BACKLOG-resident
> graph. Durable encoding is **#156**. Read it as *the architect's current read of the arc*, to
> be re-derived against the live `BACKLOG.md`.

**The "finish the v5 machinery" arc, as a dependency read:**

- **New keystone deliverable: #164 (the v5 `/handoff` generator).** It is what operators
  touch and the felt pain (this hand-assembly). Natural **predecessors** — independently
  shippable but cleaner first:
  - **#161** (stable probe-core) — gives #164 a fixed probe set to emit instead of improvising.
  - **#163** (teeth validator) — gives #164 its verification cadence; the generator emits a
    manifest, the validator proves it bites.
- **#163 (teeth validator)** — independent; unblocks mechanical verification of any v5 bundle
  (today the manual probe-gate covers it). Mirrors the historical-v4 `check_handoff_bundle_structure`.
- **Parallelizable now (independent of the generator build):**
  - **#152** §8-half (pointerize PLAYBOOK §8 → HANDOFF_PROCESS) — **its #149-flip blocker is
    now gone.**
  - **#162** (architect actor-vs-mode vocab) — atomic across surfaces; independent.
  - **#158** (high-confidence PLAYBOOK pointerizations) — incremental, each operator-approved.
  - **#153** (enforcement-completeness remaining constraints) — FF-guard already shipped.
  - **#155** (loops architecture) — gated only on the operator's VERIFY-FIRST scope.
  - **#159** (operator-context beat) — *landed + canonical*; remaining work is
    *validate-in-session* (this session) + a weight judgment, not new build.
- **#156 (durable task-graph schema)** is the **meta-item that retires this very section** —
  once it ships, the architect emits a durable graph instead of this prose, and **#150 closes**.

**Net:** **#164** (generator) is the new critical path, best preceded by **#161** (probe-core)
and **#163** (validator); the cleanups (#152/#162/#158/#153/#155) run in parallel beside it
(several now unblocked by the flip); **#156** is the meta-item that makes the *next* architect
handoff carry a real graph instead of residual prose.

---

## 6. Lean task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets** — `BACKLOG.md` is the source; do not re-narrate
IDs here. State at generation:

- **Theme pointer (architect §13b):** the **way-of-working / finish-the-v5-machinery** theme in
  `BACKLOG.md` — the "Finish the v5 handoff machinery deferred at the #149 flip" story
  (#163 · #164) + the carried-open handoff-continuity items (#1 · #26 · #150 · #152 · #156 ·
  #158 · #159 · #161 · #162) + #153 · #155. Read the live file; the §5 graph above is the
  *ephemeral* dependency read over these.
- **Live branches:** `main` (clean working tree, but **ahead 1 / behind 1 of `origin/main`** —
  §1, ask the operator to reconcile) + this handoff's own branch
  (`docs/handoff-2026-06-12-session`, merges on completion via `--no-ff`). `git branch -v` to
  confirm at read-time; no straggler branches at generation.
- **Task-state drift-flag:** #77 — dispositioned voided closure (§1 above); **not work.**
