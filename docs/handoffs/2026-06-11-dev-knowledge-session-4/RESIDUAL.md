# Residual — 2026-06-11 session-4 (v5 beta, **execution mode**)
<!-- scope: meta -->

> The **residual**: what the repo does not already encode. Drift-flags are the headline,
> not a footnote. Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md`,
> not re-narrated IDs. Generated from inside the repo at HEAD = the session-3-handoff merge
> (`bdfbe39`), working tree clean at generation.
>
> **Mode = execution (default).** This is the lean v5 residual + thin boot + teeth probes +
> pointer task-state; the browser gets the **§7 reactive-filter** role (not the architect
> generative posture). **It is the execution-mode counterpart to the same-day `session-3`
> architect handoff** — same window (the operator-context-beat arc), different profile: no
> orientation-first probe, no operator-context beat, no open-questions/task-graph; just the
> residual a session needs to *advance a ticket*. Honest note: there is no *new* substantive
> work since `session-3` — the only commit since is `session-3`'s own merge; this bundle
> exists to exercise/compare **execution mode** on the current state, not because new work
> accrued.

---

## 1. Drift-flags — the headline

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus
CC's state read. **A flag is a question, not a verdict.** One live flag at this generation
(the first execution dogfood's DRIFT-1 is now **resolved**).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable)*

`validate_git_backlog` flags a `closes [#77]` merge whose `[#77]` is still present (open) in
`BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** `ecosystem/disposition-register.yaml` → `warn-77-voided-closure`. The merge
  carried `closes [#77]` but shipped *different* work (CONTRIBUTING→v4, not the
  protocols-consolidation #77 names) — #77 was **re-scoped, not done**, so it legitimately
  stays open. Direction-(a) #90a cannot tell a misattributed closure from a real one; only
  arc-content inspection (**#139** / #90b) can — which auto-clears this entry once #139 ships.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational) and
  still exits OK.
- **Consult the register before acting on any #90 flag.** Treating the flag as an action item
  would "close" a correctly-open ticket.
- **Confirm:** `python scripts/validate_git_backlog.py` + read `ecosystem/disposition-register.yaml`.

### No `doc_claims` (#89) drift at generation *(state note — the prior dogfood's DRIFT-1 is resolved)*

The first v5 execution dogfood (sibling `2026-06-11-dev-knowledge-session/`) headlined a
**DRIFT-1**: `ARCHITECTURE.md`'s `**N collected**` test-count was stale. **Now reconciled** —
`audit.py health` reports `doc_claims` all-match (3 self-claims) at this generation. Re-derive,
don't trust this line: **P6** in `PROBES.md` forces the live check (the count drifts on any
test change — this session added 2 tests, so the doc was re-stamped to match).

### State note — **two leftover branches** + an unpushed `main` *(housekeeping, not drift-checks)*

- **Two merged-but-undeleted branches** (prune-candidates per CLAUDE.md §5 #9, but **ask
  before deleting** — core-invariant #3): `docs/arch-coherence-audit` (`b9fa4c4`),
  `docs/handoff-2026-06-11-architect` (`e6b163e`). Surfaced, not actioned.
- **`main` is ahead of `origin/main` by 2** at generation — the `session-3` handoff commit +
  its merge, unpushed. Benign; push is the operator's call. `git status -sb` to confirm.

---

## 2. Un-committed session reasoning — the lived "why"

Not in git/JOURNAL/BACKLOG (which record *what shipped*, not the reasoning). Lean, for an
execution resumption:

1. **What this window shipped (context for the next ticket).** The **operator-context beat**
   (Change B) landed in v5 *architect* mode — `HANDOFF_PROCESS_v5` §13(d) + a `HANDOFF_BOOT.md`
   architect-posture step + two test fences — and **#159** was minted (open). It is an
   *architect-mode* capability; an *execution* session does not invoke it. The full planning
   "why"/design-tensions live in the `session-3` **architect** residual — not re-narrated here
   (mode discipline: execution carries the lean residual, architect carries the planning arc).
2. **Why an execution handoff now.** Deliberate — to exercise/compare **execution mode** on the
   current state in the v5 promotion-dogfood phase (#149). The mode switch (`v5` → execution
   profile + reactive-filter role) is the thing under test, not new work.
3. **The teeth discipline (see §4).** Every probe's exact answer is kept *out* of this residual
   — drift-flags are stated **qualitatively + the command**, never the raw integers/shas/dates.
   That is what makes the probes un-bluffable from a summary.

---

## 3. Pointers (paths — read these; do not copy them into the handoff)

- **Process (v5, beta, governing this handoff):** `protocols/HANDOFF_PROCESS_v5.md` (execution
  is the default mode; modes = §13); thin boot `protocols/HANDOFF_BOOT.md` (use the
  **execution / reactive-filter** role, not the architect posture that also lives in that file).
- **Process (canonical, still authoritative for real handoffs):** `protocols/HANDOFF_PROCESS.md` (v4.4).
- **Methodology (referenced, never copied):** `protocols/PLAYBOOK.md`, `protocols/ESSENTIALS.md`, `CLAUDE.md`.
- **Companion (same window, architect framing):** `docs/handoffs/2026-06-11-dev-knowledge-session-3/`.
- **Decision record:** `docs/decisions/ADR-82-*.md` (Proposed — Council-pending, ADR-41 routing).
- **Drift-check sources:** `scripts/validate_doc_claims.py` (#89), `scripts/validate_git_backlog.py` (#90),
  `ecosystem/disposition-register.yaml`.
- **Task spec:** `BACKLOG.md` — the way-of-working theme (#149 · #150 · #151 · #152 · #153 ·
  #155 · #156 · #157 · #158 · #159); v5 promotion successor **#149**, origin **#148**.

---

## 4. Why the probes have teeth (the design rule — see `PROBES.md`)

A probe is teeth-bearing only when its answer **cannot be read off a compaction summary** — it
exists only in the live primary file/state at answer-time. The three §5 conditions are
deliberately **not restated here** (read them in the spec — P2 makes you quote them
byte-identical, which a restatement would defeat). They reduce to one operational rule this
residual follows: **no probe's exact value appears anywhere in this artifact.** The drift
headline names *that* a flag exists and *which* id — but not the collected-count integers, the
closing-merge sha, or the freshness dates. The only way to answer a probe is to open the live
source. That is the whole point.

---

## 5. Lean task-state (pointer, not narration)

The **BACKLOG is the spec; items are tickets** — `BACKLOG.md` is the source; do not re-narrate
IDs here. State at generation:

- **Theme pointer:** the **way-of-working** theme in `BACKLOG.md` — #149 · #150 · #151 · #152 ·
  #153 · #155 · #156 · #157 · #158 · #159. Live execution candidates (independent of the #149
  flip): **#157** (intra-`CLAUDE.md` lifecycle collapse — coordinate with #112) · **#158**
  (high-confidence PLAYBOOK pointerizations) · **#153** (remaining enforcement-completeness) ·
  **#159** (validate the operator-context beat in a real architect session). Read the live file;
  pick per priority.
- **Live branches:** `main` (clean, **ahead of `origin/main` by 2**, unpushed) + this handoff's
  own branch (`docs/handoff-2026-06-11-session-4`, merges on completion) + **two
  merged-but-undeleted** branches (`docs/arch-coherence-audit`, `docs/handoff-2026-06-11-architect`
  — prune-candidates, §1, ask first). `git branch -v` to confirm at read-time.
- **Task-state drift-flag:** #77 — dispositioned voided closure (§1 above); **not work.**
