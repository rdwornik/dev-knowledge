# Residual — 2026-06-12 session (`-3`), **architect mode** (v5 canonical §13)

<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the
> **open architecture questions**, and the **task-graph** — carried as *ephemeral residual
> prose*, **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a
> footnote. Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at HEAD
> `5d2ffdd`, working tree clean, **`main` ahead 4 of `origin/main` — not yet pushed** (the
> push is operator-gated — §1). Re-derive HEAD/sync at read-time (P3).
>
> **Scope of this handoff.** Same theme as the prior `2026-06-12-dev-knowledge-session` /
> `-session-2` bundles — a *planning* session on the **way-of-working**, specifically
> **finishing the v5 handoff machinery deferred at the #149 flip** (#164 generator · #163
> teeth validator, with #161/#162/#156/#159/#165 beside). What this `-3` bundle adds as
> **new residual**: (1) a small **remote-hygiene truth pass** — a *vacuous-interlock* finding
> that bears directly on the **#163 teeth-validator design** (a check whose anchor doesn't
> resolve must FAIL/WARN, never silently pass); (2) the **`docs/handoffs/_references/` reorg**
> — a new convention separating rendered reference artifacts from immutable bundle dirs. It
> does **not** advance a single ticket; that is execution mode. Orient first (`PROBES.md` P1),
> **then ask the operator for off-repo context** (§13d), then resume the design.

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
  misattributed closure from a real one; only arc-content inspection (**#139** / #90b) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py` + read `ecosystem/disposition-register.yaml`.

### DRIFT — `no_ff_merges` #153: a direct (FF/non-merge) commit on `main` *(honest open question — disposition TBD, ask the operator)*

Carried from the prior handoff and still live. `audit.py health` reports `[~~] no_ff_merges`
naming `61c5b50fa (2026-06-12) docs(audit): nightly conformance digest` — a **nightly automation
writer** commit landing *direct* on `main` rather than via a `--no-ff` merge.

- **The genuine tension (do NOT self-resolve):** ADR-80's writer policy says *automation commits
  its own output*; the `--no-ff`-universal invariant (core-invariant rule 5) says *every change
  goes branch → merge*. These two **collide on the nightly Routine's own commits.** Is an
  automation-direct-commit **sanctioned** under ADR-80 (→ disposition it keyed on the routine's
  signature), or is the Routine **owed a `--no-ff` merge path** (→ a fix on the writer)? **This
  is an architect-session question** (§3 Q9), not a thing to "fix" by reverting the digest.
- **Confirm:** `python scripts/audit.py health` (the `no_ff_merges` line) +
  `git log --first-parent --oneline -8 main`.

### STATE NOTE — `main` is **ahead 4 of `origin/main`**, not pushed *(push is operator-gated)*

This session's four merges (the two README/journal merges from the redesign wrap, plus this
session's `_references` reorg merge and its JOURNAL-wrap merge) sit **local-only**. The push was
**deliberately not done** — it is operator-gated. No sync action is owed *by CC*; the operator
decides when to `git push origin main`. **Re-derive at read-time** (P3): `git status -sb` +
`git log --oneline origin/main..main`.

### STATE NOTE — the local `refs/remotes/origin/main` tracking ref was **missing and was repaired** this session *(the vacuous-interlock lesson — feeds #163)*

Earlier this session a remote-state cleanup was attempted against a read-only interlock built on
`origin/main..main`. The interlock **passed vacuously**: `origin/main` did not resolve locally
(`git rev-parse origin/main` → `fatal: Needed a single revision`), so the left side of the range
was empty and *every* diff/log check returned clean **regardless of real state** — the safety gate
did not actually run. Ground truth was re-derived via `git ls-remote` instead, then the tracking
ref was repaired (`git fetch origin main:refs/remotes/origin/main`). Root cause: the fetch refspec
is the **standard wildcard** (`+refs/heads/*:refs/remotes/origin/*`) — not missing/narrow; the ref
had simply never been populated, now self-maintaining. **Why it's in the residual, not just the
log:** this is a live, concrete instance of the §10 *degrade-loudly* principle that the **#163
teeth validator** must encode — a probe/check whose anchor (ref, file section, command target)
**does not resolve must FAIL or WARN `anchor-missing`, never silently pass**. The vacuous-interlock
is the failure mode #163 exists to prevent. **Confirm:** `git rev-parse --verify origin/main` (now
resolves) + `git config --get remote.origin.fetch`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The theme is unchanged and it is the way-of-working:** v5 is canonical (HANDOFF_PROCESS v5.0,
`Status: stable`, #149 flip 2026-06-11) but the *machinery* the flip deferred is still open. The
spec is written; the **generator** (#164) and the **mechanical teeth** (#163) are not. Every v5
bundle to date — including this one — was **hand-assembled by CC following the spec**, which is
itself the standing argument that the machinery must land: hand-assembly is exactly the
drift-prone hand-maintained-surface the methodology outlaws everywhere else.

**Design tension surfaced this session (new):** the **vacuous-interlock** (§1). It is small in
isolation but it is the *general shape* of the failure the #163 teeth validator must defend
against — a verification that reports green because its **anchor never resolved**, not because the
property held. v4's comprehension questions failed this way ("fake-green," §0 of the spec
rationale); a teeth probe whose command errors or whose anchor is missing must **degrade loudly**
(§10), not count as pass. The session's `origin/main..main` interlock is a real, recent instance
to design the validator against — and a candidate test case for #163's own test-suite
("a probe whose anchor is absent must FAIL").

**Structural change this session (new, minor):** `docs/handoffs/_references/` now exists — rendered
reference artifacts (e.g. the operator-first README reference for session-2) live there, separated
from the immutable bundle dirs. A convention worth either codifying or leaving informal; surfaced
so the next session doesn't rediscover it.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

- **Q1 (#164) — generator shape.** The v5 `/handoff` generator must emit the **operator-first**
  README (`templates/handoff/v5/README.md.tmpl`, landed this day) and the residual/probe/boot
  emissions, replacing the v4 Phase-1/2 prose in `.claude/commands/handoff.md` + `SESSION_SETUP`.
  Open: it is now scoped **repo-parameterized cross-repo** (the ADR-83 v4-restoration arc) — how
  does it deterministically **route** a v4 target repo (one lacking `scripts/audit.py`) to the v4
  path? (The v5 routing ambiguity from the `-2` residual.)
- **Q2 (#163) — teeth validator.** `scripts/verify_handoff_probes.py` (read-only, Layer-2):
  prove a bluffable probe FAILs and a live-grounded probe PASSes. **Fold in the vacuous-interlock
  lesson (§1):** an unresolved anchor must FAIL/WARN, never vacuously pass — make that an explicit
  test case.
- **Q3 (#156) — durable task-graph.** The architect task-graph is *ephemeral residual prose* today
  because the ADR-66 BACKLOG schema encodes no depends-on / parallel fields. Durable encoding =
  `validate_backlog` extension + ADR-66 amendment. Worth it now, or keep it residual-only?
- **Q4 (#161/#162) — teeth probe-core + actor-vs-mode vocab.** Post-flip cleanups: a reusable
  probe-core; disambiguate "architect" the *actor* (Layer-1 browser) from "architect" the *mode*.
- **Q5 (#159) — operator-context beat.** Exercise the §13d beat in a real architect session and
  confirm it carries off-repo intent without re-narrating the residual.
- **Q9 — automation-writer vs `--no-ff`-universal.** The §1 `no_ff_merges` tension: sanction the
  nightly-Routine direct commit (disposition it) or give the writer a merge path? An ADR-80 ×
  core-invariant-5 reconciliation, not a revert.
- **Q10 (#165) — ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment (filed
  during the README redesign), awaiting ratification — not a unilaterally-minted ADR.

---

## 4. The task-graph (ephemeral — NOT a durable BACKLOG field, #156)

Carried as residual prose per §13b; do **not** claim this is encoded in BACKLOG. Under theme
**"Finish the v5 handoff machinery deferred at the #149 flip"**:

- **#163 (teeth validator)** is the closest-to-ready and **gates trust in every v5 bundle**; it is
  also where the §1 vacuous-interlock lesson lands. → do first.
- **#164 (generator)** is **L (large)** and now **depends on the #164/cross-repo routing decision
  (Q1)**; it consumes the operator-first template (done) and ideally the #163 validator (so the
  generator's output is mechanically checkable). → after Q1 is decided; pairs with #163.
- **#156 (durable task-graph), #161, #162** are **independent cleanups** — parallelizable beside
  the above; none blocks #163/#164.
- **#165 (mermaid rule)** and **Q9 (automation/`--no-ff`)** are **decision items**, not build items
  — resolve via ratification / operator ruling, can run in parallel.

(Dependencies/parallelization above are the architect's read, not a schema fact — #156 is what would
make them durable.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` theme **"Finish the v5 handoff machinery deferred at
  the #149 flip"** (under `## Handoff continuity`) for the live tickets: **#163, #164** there, plus
  **#156, #159, #161, #162, #165** across the same continuity theme. Do **not** trust any re-narrated
  ID text — open the live BACKLOG.
- **Live branches:** none in progress (`git branch -v` shows only `main` + this handoff's own branch
  `docs/handoff-2026-06-12-session-3`, which merges on completion). No straggler branches at
  generation.
- **Drift-flags:** the two `[~~]` WARNs in §1 (#90a known-benign/dispositioned; `no_ff_merges` =
  open Q9). Re-derive at read-time via `python scripts/audit.py health`.
- **Push state:** `main` ahead 4 of `origin/main`, **not pushed** — operator-gated (§1).
