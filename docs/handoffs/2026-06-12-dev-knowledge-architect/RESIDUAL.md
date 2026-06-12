# Residual — 2026-06-12 session, **architect mode** (v5 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph** — carried as *ephemeral residual prose*,
> **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a footnote.
> Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at HEAD
> `66d0293`, working tree clean, **`main` in sync with `origin/main`** (the prior handoff's
> ahead-4 was pushed; no sync owed). Re-derive HEAD/sync at read-time (P3).
>
> **Scope of this handoff.** Same theme as the `2026-06-12-dev-knowledge-session` /
> `-2` / `-3` bundles — a *planning* session on the **way-of-working**, specifically
> **finishing the v5 handoff machinery deferred at the #149 flip** (#164 generator · #163
> teeth validator, with #156/#159/#161/#162/#165 + the Q9 reconciliation beside). What this
> bundle adds as **new residual vs `-3`**: the **canonical-runbook collapse landed** — the
> per-bundle README is **gone**, v5 bundles are now **three files**, and the operator
> boilerplate lives once in the freshness-gated `docs/handoffs/README.md`. That **resolved**
> two `-3` residual items (the operator-first README shape; the `_references/` convention) and
> **rescoped #164**. It does **not** advance a single ticket; that is execution mode. Orient
> first (`PROBES.md` P1), **then ask the operator for off-repo context** (§13d), then resume
> the design.

---

## 1. Drift-flags — the headline

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus
CC's state read at generation. **A flag is a question, not a verdict.** `audit.py health` is
**OK** at generation (16/18 pass; the 2 below are both `[~~]` WARN, informational — health
still exits OK). Re-derive at read-time (P4/P7).

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still
present (open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed
  closure from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py` + check `ecosystem/disposition-register.yaml`.

### DRIFT — `no_ff_merges` #153: a direct (FF/non-merge) commit on `main` *(honest open question — disposition TBD, ask the operator → Q9)*

Carried across handoffs and still live. `audit.py health` reports `[~~] no_ff_merges` naming
`61c5b50fa (2026-06-12) docs(audit): nightly conformance digest` — a **nightly automation
writer** commit landing *direct* on `main` rather than via a `--no-ff` merge.

- **The genuine tension (do NOT self-resolve):** ADR-80's writer policy says *automation commits
  its own output*; the `--no-ff`-universal invariant (core-invariant rule 5) says *every change
  goes branch → merge*. These two **collide on the nightly Routine's own commits.** Is an
  automation-direct-commit **sanctioned** under ADR-80 (→ disposition it, keyed on the routine's
  signature), or is the Routine **owed a `--no-ff` merge path** (→ a fix on the writer)? **This
  is an architect-session question** (§3 Q9), not a thing to "fix" by reverting the digest.
- **Confirm:** `python scripts/audit.py health` (the `no_ff_merges` line) +
  `git log --first-parent --oneline -8 main`.

### STATE NOTE — `main` is **in sync** with `origin/main` *(no push owed — changed since `-3`)*

The `-3` residual carried `main` ahead-4 of `origin/main`, operator-gated. **That push has since
landed** — `git status -sb` reports `main...origin/main` even. No sync action is owed by CC.
Re-derive at read-time (P3): `git status -sb` + `git log --oneline origin/main..main` (expect
empty).

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The theme is unchanged and it is the way-of-working:** v5 is canonical (HANDOFF_PROCESS v5.0,
`Status: stable`, #149 flip 2026-06-11) but the *machinery* the flip deferred is still open. The
spec is written; the **generator** (#164) and the **mechanical teeth** (#163) are not. Every v5
bundle to date — including this one — was **hand-assembled by CC following the spec**, which is
itself the standing argument that the machinery must land: hand-assembly is exactly the
drift-prone hand-maintained-surface the methodology outlaws everywhere else.

**Design move resolved this session (new — supersedes `-3` open items):** the **canonical-runbook
collapse**. The chain that closed:

- `-3` left open *"the operator-first README shape — codify or leave informal?"* and introduced
  `docs/handoffs/_references/` as a *"new convention worth codifying or leaving informal."* Both
  are now **resolved by deletion**: the per-bundle README is **dropped entirely** and the
  `_references/` band-aid is **retired** (commit `ac796bf`).
- The stable operator boilerplate (walkthrough · run loop · mermaid · rationale) now lives
  **once** in the canonical per-repo runbook `docs/handoffs/README.md` (operator-first:
  walkthrough first, rationale demoted), wired into the freshness gate (`audit.py` check #10
  `_FRESHNESS_FILES`) so it cannot silently rot. A v5 bundle is now **three files**
  (`HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md`); the session-header (slug · purpose · mode)
  moved into the bundle `HANDOFF_BOOT.md`.
- **Why this is the right shape (the tension weighed):** regenerating identical boilerplate into
  every bundle was token waste **and** a drift surface (each copy could rot independently), and
  the root index rotted *because* it was redundant. One freshness-gated runbook + a thin
  per-session header kills all three. The cost it accepts — and the **new open tension** it
  creates — is that the runbook is *"generic across repos of the same handoff version"* yet lives
  **per-repo**: keeping N repos' runbooks in sync without re-introducing copy-drift is now
  **#164's** job (seed/update idempotently from one source, write-if-absent-or-version-changed).
  See Q1.

**No new structural conventions this session** (the `-3` `_references/` one was retired, not
added). The only standing convention change is the three-file bundle shape, now in the spec.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

- **Q1 (#164) — generator shape, now *no-per-bundle-README*.** The v5 `/handoff` generator must
  (a) emit the **three-file** bundle (`HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md`, **no
  README**) with the session-header in the bundle `HANDOFF_BOOT.md`, and (b) **idempotently
  seed/update each repo's `docs/handoffs/README.md` runbook** from the single source
  `templates/handoff/v5/README.md.tmpl` (a **deferred stub** until #164 lands), replacing the v4
  Phase-1/2 prose in `.claude/commands/handoff.md` + `SESSION_SETUP`. **Open:** (i) the
  per-repo-runbook sync rule — write-if-absent-or-version-changed, but *how is "version" keyed*
  (handoff-process version? a content hash?) so a genuine runbook edit isn't clobbered and a
  stale one isn't left? (ii) the **cross-repo v4 routing** ambiguity (ADR-83): a v4 target repo
  (one lacking `scripts/audit.py`) needs a deterministic route to the v4 Phase-1/2 path — the
  v5 emissions can't bind a target that has no audit checks to probe.
- **Q2 (#163) — teeth validator.** `scripts/verify_handoff_probes.py` (read-only, Layer-2):
  prove a bluffable probe FAILs and a live-grounded probe PASSes, wired into the verification
  cadence. **Fold in the degrade-loudly principle:** an unresolved anchor (missing ref / renamed
  section / errored command) must FAIL or WARN `anchor-missing`, **never vacuously pass** — make
  that an explicit test case (the `-3` vacuous-`origin/main`-interlock was the concrete instance;
  that ref is now repaired, but the *failure shape* is what #163 must defend against).
- **Q3 (#156) — durable task-graph.** The architect task-graph (§4) is *ephemeral residual prose*
  today because the ADR-66 BACKLOG schema encodes no depends-on / parallel fields. Durable
  encoding = `validate_backlog` extension + ADR-66 amendment. Worth it now, or keep it
  residual-only until there are enough multi-item arcs to pay for it?
- **Q4 (#161/#162) — teeth probe-core + actor-vs-mode vocab.** Post-flip cleanups: a reusable
  probe-core (bundles stop hand-assembling probe sets per handoff — note this architect bundle
  again hand-assembled P1–P7); disambiguate "architect" the *actor* (Layer-1 browser) from
  "architect" the *mode* (§13) atomically across every surface.
- **Q5 (#159) — operator-context beat.** Exercise the §13d beat in a *real* architect session and
  confirm it carries off-repo intent without re-narrating the residual. (The #149 v5→canonical
  carry is DONE; only the real-session exercise remains — *this* session is a candidate.)
- **Q9 — automation-writer vs `--no-ff`-universal.** The §1 `no_ff_merges` tension: sanction the
  nightly-Routine direct commit (disposition it, keyed on the routine signature) or give the
  writer a merge path? An ADR-80 × core-invariant-5 reconciliation, **not** a revert.
- **Q10 (#165) — ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment
  (operator-set 2026-06-12; first applied when the runbook chose mermaid), awaiting ratification —
  not a unilaterally-minted ADR. Record where the diagram convention lives once ratified.

---

## 4. The task-graph (ephemeral — NOT a durable BACKLOG field, #156)

Carried as residual prose per §13b; do **not** claim this is encoded in BACKLOG. Under theme
**"Finish the v5 handoff machinery deferred at the #149 flip"**:

- **#163 (teeth validator)** is the closest-to-ready and **gates trust in every v5 bundle** (it
  mechanically replaces the manual probe-gate every bundle so far has leaned on). → **do first.**
- **#164 (generator)** is **L (large)** and now **depends on the cross-repo / runbook-sync routing
  decisions (Q1)**; it consumes the (stubbed) `templates/handoff/v5/README.md.tmpl` and ideally
  the #163 validator (so its output is mechanically checkable). → after Q1; pairs with #163.
- **#156 (durable task-graph), #161, #162** are **independent cleanups** — parallelizable beside
  the above; none blocks #163/#164.
- **#165 (mermaid rule)** and **Q9 (automation/`--no-ff`)** are **decision items**, not build
  items — resolve via ratification / operator ruling; can run in parallel.

(Dependencies/parallelization above are the architect's read, **not** a schema fact — #156 is what
would make them durable.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` theme **"Finish the v5 handoff machinery deferred at
  the #149 flip"** (line ~30, under `## Handoff continuity`) for the live tickets: **#163, #164**
  there, plus **#156, #159, #161, #162, #165** across the same continuity theme. Do **not** trust
  any re-narrated ID text — open the live BACKLOG.
- **Live branches:** none in progress (`git branch -v` shows only `main` + this handoff's own
  branch `docs/handoff-2026-06-12-architect`, which merges on completion). No straggler branches
  at generation.
- **Drift-flags:** the two `[~~]` WARNs in §1 (#90a known-benign/dispositioned; `no_ff_merges` =
  open Q9). Re-derive at read-time via `python scripts/audit.py health`.
- **Push state:** `main` **in sync** with `origin/main` at generation (the `-3` ahead-4 was
  pushed). Re-derive (P3).
