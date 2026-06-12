# Residual — 2026-06-12 session (`-2`), **architect mode** (v5 canonical §13)

<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the
> **open architecture questions**, and the **task-graph** — carried as *ephemeral residual
> prose*, **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a
> footnote. Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at HEAD
> `48bb5a4`, working tree clean, **`main` in-sync with `origin/main`** at generation (the
> prior handoff's ahead-1/behind-1 divergence has since been reconciled — §1).
>
> **Scope of this handoff.** Same theme as the prior `2026-06-12-dev-knowledge-session`
> bundle — a *planning* session on the **way-of-working**, specifically **finishing the v5
> handoff machinery deferred at the #149 flip** (#164 generator · #163 teeth validator, with
> #161/#162/#152/#156/#159 cleanups beside). What this `-2` bundle adds as **new residual**:
> the **v4-template-restoration arc** that landed after the prior handoff — un-regressing the
> #149 flip's premature archival of the live v4 cross-repo templates — which **sharpens #164**
> into a *repo-parameterized cross-repo* generator and surfaces the **v5 routing ambiguity**.
> It does **not** advance a single ticket; that is execution mode. Orient first (`PROBES.md`
> P1), **then ask the operator for off-repo context** (§13d), then resume the design.

---

## 1. Drift-flags — the headline

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus
CC's state read at generation. **A flag is a question, not a verdict.** `audit.py health` is
**OK** at generation (16/18 pass; the 2 below are both WARN, informational — health still
exits OK).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still
present (open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** `ecosystem/disposition-register.yaml` → `warn-77-voided-closure` (match
  `77e5d7d`). The merge carried `closes [#77]` but shipped *different* work — #77 was
  **re-scoped, not done**, so it legitimately stays open. Direction-(a) #90a cannot tell a
  misattributed closure from a real one; only arc-content inspection (**#139** / #90b) can —
  which auto-clears this entry (`auto_clearable_by: "#139"`) once #139 ships.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Consult the register before acting on any #90 flag.** Treating the flag as an action item
  would "close" a correctly-open ticket.
- **Confirm:** `python scripts/validate_git_backlog.py` + read `ecosystem/disposition-register.yaml`.

### NEW DRIFT — `no_ff_merges` #153: a direct (FF/non-merge) commit on `main` *(honest open question — disposition TBD, ask the operator)*

New since the prior handoff. `audit.py health` reports `[~~] no_ff_merges`:

```
non-merge commit on main (FF/direct -- expected a --no-ff merge): 61c5b50fa (2026-06-12)
docs(audit): nightly conformance digest 2026-06-12 -- 2 high / 3 med / 0 low (#24)
```

- **What it is:** the `--no-ff` merge guard (#153, core-invariant rule 5, **detect-and-surface**)
  caught `61c5b50fa` — a **nightly automation writer** commit (the conformance digest) — landing
  *direct* on `main` rather than via a `--no-ff` merge. The sibling `98e9b1e`
  (`chore(routine/fleet-audit): record 2026-06-12 baseline`) is the same class.
- **The genuine tension (do NOT self-resolve):** ADR-80's writer policy says *automation commits
  its own output*; the `--no-ff`-universal invariant says *every change goes branch → merge*.
  These two **collide on the nightly Routine's own commits**. Is an automation-direct-commit
  **sanctioned** under ADR-80 (→ disposition it in `ecosystem/disposition-register.yaml`, keyed
  on the routine's signature), or is the Routine **owed a `--no-ff` merge path** (→ a fix on the
  writer)? **This is an architect-session question** (a candidate Q — §4 Q9), not a thing to
  "fix" by reverting the digest. It is **not** dispositioned today.
- **Confirm:** `python scripts/audit.py health` (the `no_ff_merges` line) +
  `git log --first-parent --oneline -6 main` (the digest shows as a direct commit, not a merge).

### STATE NOTE — `main` is now **in-sync** with `origin/main` *(the prior bundle's divergence resolved)*

The prior `2026-06-12-dev-knowledge-session` residual flagged `main [ahead 1, behind 1]` of
`origin/main` as a real divergence owed a reconcile. At **this** generation `git status -sb`
shows a clean `## main...origin/main` (no ahead/behind) — **the reconcile happened**; no sync
action is owed. **Re-derive at read-time** (P3): `git status -sb` +
`git log --oneline origin/main..main` / `git log --oneline main..origin/main` (both empty = in-sync).

### STATE NOTE — one **straggler branch** owed a prune *(housekeeping, ask the operator — core-invariant #3)*

`git branch --merged main` shows the **prior** handoff's own branch
`docs/handoff-2026-06-12-session` is **merged but not deleted** — a leftover (the no-leftovers
invariant, CLAUDE.md §5 #9). It is owed a `git branch -d docs/handoff-2026-06-12-session`, but
**branch deletion is gated on the operator** (core-invariant #3 — never delete a branch without
asking). This bundle's own branch (`docs/handoff-2026-06-12-session-2`) merges on completion via
`--no-ff` and should be pruned in the same sweep. **Confirm:** `git branch --merged main`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

Not in git/JOURNAL/BACKLOG (which record *what shipped*, not the design reasoning). The arc
since the prior handoff and the design tensions this planning session inherits:

1. **NEW — the #149 flip over-archived live v4 machinery; it was un-regressed (the v4-template
   restoration).** The flip `git-mv`'d `templates/handoff/*` → `templates/archive/handoff-v4/`,
   treating v4 as **fully** dead. It is only **partially** dead: **corp-monorepo (and any v4
   repo) still runs the v4 8-file two-phase cross-repo generator** that the `/handoff` command
   body retains (marked SUPERSEDED), and that path **reads `templates/handoff/` at Phase 2** —
   so archiving broke `create handoff for corp-monorepo`. Per **ADR-83** ("only dead things
   archive") the templates are **live for v4 repos** → restored to `templates/handoff/` via
   rename (history preserved; the archival was R100, `c3ba6d4`). The v4 README **stamp was also
   pinned**: `templates/handoff/README.md.tmpl:9` resolves `{{VERSION}}`/`{{STATUS}}` from
   `protocols/HANDOFF_PROCESS.md` — now **v5.0/stable** — so a v4 bundle would mis-stamp v5.0;
   the stamp was hardcoded to literal `v4.4 (status: live)` (resolver untouched). **E2E proof
   (the closure gate):** a full v4 cross-repo bundle generated for corp-monorepo to `%TEMP%`
   (throwaway) — valid, **v4.4-stamped**, targets corp-monorepo's live state, zero unresolved
   `{{…}}`, no `.dev-knowledge` sha leaked. The **design lesson:** *"v5 is canonical" ≠ "v4 is
   dead."* The two coexist until every v4 repo migrates — and the canonical-flip's instinct to
   archive everything v4 was a regression the ADR-83 "only-dead-things-archive" rule exists to
   catch.
2. **This sharpens #164 from "wire the v5 generator" into "build the *repo-parameterized
   cross-repo* generator," and surfaces the v5 routing ambiguity.** The restoration is a
   **stopgap**: the v4 templates (and the stamp pin) become removable **only when** a
   repo-parameterized v5 cross-repo generator lands and corp-monorepo migrates off v4 — that
   removal is now **gated to #164's close** (recorded on the #164 backlog note, 2026-06-12).
   The deeper defect it exposed: **a v4 target repo has no deterministic route to the v4 path** —
   an executing agent *infers* v4 because the v5 emissions can't bind a target that lacks
   `scripts/audit.py`. The durable fix is the repo-parameterized generator; the routing problem
   is now part of #164's scope, not a separate ticket (captured as #164's "v5 routing ambiguity"
   note; out-of-scope for the restoration session, deliberately not fixed there).
3. **The #149 flip LANDED — the machinery is *specified* but not fully *built*** (carried from
   the prior handoff, still the spine). The flip promoted v5 to canonical (`Version 5.0` /
   `Status stable`), archived v4.4 (ADR-83 tombstone), moved the 4 gate-coupled surfaces + the
   ~10 prose surfaces (#151) atomically, closed #149/#151/#160/#148/#124/#25. **Two conscious
   deferrals**, captured so the flip stayed atomic:
   - **#164 — the v5 `/handoff` generator.** `.claude/commands/handoff.md` **still carries the
     v4 8-file two-phase generator (SUPERSEDED)**, and `SESSION_SETUP.md` likewise. The v5
     emissions (residual + probe manifest + thin-boot pointer + lean task-state) are *specified*
     but not yet the *wired generator*. **Now also scoped: repo-parameterized cross-repo + the
     routing fix** (point 2).
   - **#163 — the read-only teeth validator** `scripts/verify_handoff_probes.py` — validates a
     v5 bundle's probe manifest (each command PASSes against live state; each forced-read probe
     is **not** answerable from the compaction summary alone). Deferred because audit #8/#9
     degrade cleanly without it; until it lands the **manual probe-gate**
     (`HANDOFF_PROCESS.md` §5 / `PROBES.md`) covers v5 verification.
4. **This very handoff is *still* the live argument for #164 (and #161).** Like the prior one,
   it was **hand-assembled by CC** following the v5 spec — no generator exists, so the probe set
   (P1–P6) was assembled by hand. The SUPERSEDED v4-shaped command produced a v5-shaped bundle
   by operator + CC reading the spec, not by machine. *That gap is the work.*
5. **The "architect" actor-vs-mode collision is still live (#162).** "architect" means the
   Layer-1 **actor** (browser-chat role, ARCHITECTURE.md / ADR-28) **and** the handoff **mode**
   (`architect|execution`, §13). Only the boot-ack slice shipped (2026-06-11: ack now says
   "Layer-1 browser", no on-load mode claim); the **model decision** — rename one sense or
   formally scope both, **atomically across every enumerated surface** — remains.
6. **Resident-copy drift on the repo's *own* handoff self-description (#152, §8-half).** The flip
   repointed PLAYBOOK §8's *authority* v4→v5 (#151), but §8 still **describes** the v5 handoff
   rather than being a **pure pointer** to `HANDOFF_PROCESS.md`. Settled *direction*: replace the
   copy with a pointer (`source → gate → agent`). The **open** part is doing the §8-half — its
   #149-flip blocker is now gone.
7. **Ship-now-defer-durable shaped #150/#159 — and bounds #156.** The two-mode switch +
   orientation layer + operator-context beat **landed**, but **#150 stays open** because the
   durable BACKLOG-resident task-graph (deps/parallelization) was *not* built (that would be
   fake-green). Successor = **#156** (ADR-66 amendment + `validate_backlog` extension). The §5
   task-graph below is therefore **still ephemeral residual prose**.
8. **#159 (operator-context beat) — flip-carry DONE; the real-session exercise is not.** The beat
   lives in canonical spec §13(d); the only remaining clause is **exercising it in a real
   architect session**. *This handoff is again a candidate* — orient via P1, then the off-repo
   ask, and judge whether one targeted ask is the right weight.

## 3. Pointers (paths — read these live; do not copy them into the handoff)

- **Process (v5, canonical, governing this handoff + its modes):** `protocols/HANDOFF_PROCESS.md`
  (architect mode = §13; orientation = §13(c); operator-context beat = **§13(d)**; deferred
  machinery = §11 + §13 close-note); thin boot `protocols/HANDOFF_BOOT.md` (carries both
  postures + the operator-context step).
- **The v4-restoration arc (this session's new residual):** restored live templates
  `templates/handoff/*` (8 files; `README.md.tmpl:9` carries the pinned literal `v4.4 (status:
  live)` stamp); archived-but-superseded process `protocols/archive/HANDOFF_PROCESS_v4.4.md`;
  governing principle `docs/decisions/ADR-83-protocols-archive-convention.md` ("only dead things
  archive"); the JOURNAL entry (2026-06-12 "un-regress the v4 cross-repo handoff"); branch
  `fix/restore-v4-handoff-templates` (`1ea0b57` + `19f3b4d`, merged `48bb5a4`).
- **Orientation sources (P1 — read live, never copied):** `VISION.md` `## Vision` (line 11);
  `ARCHITECTURE.md` Ch1 (`## Purpose [CORE]`, line 47).
- **The deferred machinery (the spine of this session):** `.claude/commands/handoff.md` +
  `protocols/SESSION_SETUP.md` (both carry the v4 generator marked SUPERSEDED — #164 target);
  `scripts/audit.py` `check_handoff_bundle_structure` (the historical-v4 sibling #163 mirrors).
- **Operator-context beat — fences + grounding:** `tests/test_handoff_modes.py`
  (`test_v5_architect_carries_operator_context_beat`,
  `test_boot_architect_posture_carries_operator_context_step`, `test_boot_ack_is_mode_neutral`);
  grounding = `docs/audits/2026-06-11-surface-responsibility-audit.md` "Noted limitation".
- **Methodology (referenced, never copied):** `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md`.
- **Decision records:** `docs/decisions/ADR-82-*.md` (operator-ratified; Council gate waived,
  #149); `docs/decisions/ADR-83-protocols-archive-convention.md`; ADR-80 (automation writer
  policy — the `no_ff_merges` tension, §1).
- **Drift-check sources:** `scripts/validate_doc_claims.py` (#89), `scripts/validate_git_backlog.py`
  (#90), `ecosystem/disposition-register.yaml`.
- **Task spec:** `BACKLOG.md` — the way-of-working theme (see §6).

---

## 4. Open architecture questions (architect §13e — surfaced, not buried)

The design decisions **not yet made** — so the next session resumes the design rather than
rediscovering it. Each is a *question* with the ticket that holds it:

- **Q1 — Build order: validator (#163) or generator (#164) first?** Independently shippable, but
  #163 (teeth validator) gives #164 (generator) its *verification cadence*. Decide
  validator-first (teeth before automation) or generator-first (operators touch the command
  daily; this hand-assembly is the felt pain).
- **Q2 — #161 probe-core: scope it now, or keep capture-only?** Every bundle hand-assembles its
  probe set (this one included). Define a **stable shared probe-core (~5 forced-read probes) +
  the architect-only orientation probe** so #164 emits a fixed core — or explicitly defer. #161
  is a natural **predecessor** to #164.
- **Q3 — #162 vocab disambiguation: rename one sense, or formally scope both?** Enumerate every
  surface where "architect" appears as actor vs mode and decide **atomically** (ADR or operator
  ruling). Do not leave the collision live.
- **Q4 — #156 durable task-graph schema.** Decide the ADR-66 amendment: `depends-on` / `parallel`
  fields + a `validate_backlog` extension (reference existence + no cycle). Until then the graph
  is *only* §5 — ephemeral; **#150 closes** when this lands.
- **Q5 — #152 §8 pointerization (blocker now cleared).** PLAYBOOK §8 can become a **pure pointer**
  to `HANDOFF_PROCESS.md`. Decide: pointerize §8 now, or fold it into the #164 generator work.
- **Q6 — #158 PLAYBOOK pointerizations + #153 enforcement-completeness.** #158: §"Repo
  conventions" + Appendices A/B/C → pointers (incremental, each operator-approved). #153: for each
  remaining prose-only constraint — **mechanize, or accept-as-prose with a reason** (the
  `--no-ff` FF-guard already shipped as detect-and-surface — see **Q9**).
- **Q7 — #155 loops architecture.** Operator-flagged, **scope TBD** — VERIFY-FIRST with the
  operator what "loops architecture" means before any design.
- **Q8 — #159: is one targeted ask the right weight for the operator-context beat?** *This is the
  second real architect session to carry it* — run it, then judge too-light / right / too-heavy.
  **Settled sub-question:** architect-only is final — **no** beat in execution mode.
- **Q9 — NEW: how does #164 cross-repo route, and does the v4-coexistence period get a durable
  rule?** Two coupled sub-decisions surfaced by the v4-restoration arc (§2 points 1–2):
  **(a)** the **v5 routing ambiguity** — a v4 target repo has no deterministic route to the v4
  path (the executing agent *infers* it from the absence of `scripts/audit.py`). Decide the
  repo-parameterized generator's routing contract (explicit `--process v4|v5` param? auto-detect
  by target-repo capability? a per-repo manifest?). **(b)** the **automation-writer vs
  `--no-ff`-universal collision** (§1 `no_ff_merges`): is the nightly Routine's direct commit
  *sanctioned* under ADR-80 (→ disposition it) or *owed a merge path* (→ fix the writer)? Both
  belong with #164/#153 — do not resolve by reverting the digest.

---

## 5. The task-graph — **ephemeral residual prose, NOT a durable BACKLOG field** (architect §13b)

> **Honest scope (v5 §13b).** The BACKLOG schema encodes **no** dependencies or parallelization.
> This graph is carried **in the residual, ephemerally** — not a durable, BACKLOG-resident graph.
> Durable encoding is **#156**. Read it as *the architect's current read of the arc*, to be
> re-derived against the live `BACKLOG.md`.

**The "finish the v5 machinery" arc, as a dependency read:**

- **Keystone deliverable: #164 (the v5 `/handoff` generator) — now scoped *repo-parameterized
  cross-repo*** (the v4-restoration arc widened it). It is what operators touch and the felt pain
  (this hand-assembly). It also **gates the removal** of the just-restored v4 templates + the
  stamp pin (only removable when #164 lands and corp-monorepo migrates off v4). Natural
  **predecessors** (independently shippable but cleaner first):
  - **#161** (stable probe-core) — gives #164 a fixed probe set to emit instead of improvising.
  - **#163** (teeth validator) — gives #164 its verification cadence.
- **#163 (teeth validator)** — independent; unblocks mechanical verification of any v5 bundle
  (today the manual probe-gate covers it). Mirrors the historical-v4 `check_handoff_bundle_structure`.
- **Parallelizable now (independent of the generator build):**
  - **#152** §8-half (pointerize PLAYBOOK §8 → HANDOFF_PROCESS) — **#149-flip blocker now gone.**
  - **#162** (architect actor-vs-mode vocab) — atomic across surfaces; independent.
  - **#158** (high-confidence PLAYBOOK pointerizations) — incremental, each operator-approved.
  - **#153** (enforcement-completeness) — FF-guard shipped; the `no_ff_merges` automation-writer
    tension (§1 / Q9b) is its newest live input.
  - **#155** (loops architecture) — gated only on the operator's VERIFY-FIRST scope.
  - **#159** (operator-context beat) — *landed + canonical*; remaining work is
    *validate-in-session* (this session) + a weight judgment.
- **#156 (durable task-graph schema)** is the **meta-item that retires this very section** — once
  it ships, the architect emits a durable graph instead of this prose, and **#150 closes**.

**Net:** **#164** (generator, now cross-repo-scoped + the v4-template-removal gate) is the
critical path, best preceded by **#161** (probe-core) and **#163** (validator); the cleanups
(#152/#162/#158/#153/#155) run in parallel beside it (several unblocked by the flip); **#156** is
the meta-item that makes the *next* architect handoff carry a real graph instead of residual prose.

---

## 6. Lean task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets** — `BACKLOG.md` is the source; do not re-narrate
IDs here. State at generation:

- **Theme pointer (architect §13b):** the **way-of-working / finish-the-v5-machinery** theme in
  `BACKLOG.md` — the "Finish the v5 handoff machinery deferred at the #149 flip" story
  (#163 · #164, the latter now carrying the v4-restoration arc's cross-repo + routing scope) +
  the carried-open handoff-continuity items (#1 · #26 · #150 · #152 · #156 · #158 · #159 · #161 ·
  #162) + #153 · #155. Read the live file; the §5 graph above is the *ephemeral* dependency read
  over these.
- **Live branches:** `main` (clean working tree, **in-sync with `origin/main`** — §1, no reconcile
  owed) + this handoff's own branch (`docs/handoff-2026-06-12-session-2`, merges on completion via
  `--no-ff`). **One straggler:** the prior handoff's `docs/handoff-2026-06-12-session` is merged
  but undeleted (§1 — owed a prune, operator-gated). `git branch -v` / `git branch --merged main`
  to confirm at read-time.
- **Task-state drift-flags:** #77 — dispositioned voided closure (§1, **not work**); the
  `no_ff_merges` automation-writer WARN (§1 / Q9b, **a question, not work**).
