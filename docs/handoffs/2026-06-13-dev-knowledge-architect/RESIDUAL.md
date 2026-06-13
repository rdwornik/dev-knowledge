# Residual — 2026-06-13 session, **architect mode** (v5 canonical §13)
<!-- scope: meta -->

> The **architect residual**: the planning "why" the repo does not already encode, the **open
> architecture questions**, and the **task-graph** — carried as *ephemeral residual prose*,
> **not** a durable BACKLOG field (#156). Drift-flags are the headline, not a footnote.
> Pointers are paths, not copies. Task-state is a pointer to `BACKLOG.md` and the
> way-of-working theme, not re-narrated IDs. Generated from inside the repo at HEAD
> `8d9d35d`, working tree clean, **`main` ahead 3 / behind 1 of `origin/main`** (diverged —
> §1). Re-derive HEAD/sync at read-time (P3).
>
> **Scope of this handoff — a refresh, named honestly.** Same theme as
> `2026-06-12-dev-knowledge-architect` (and the `-session`/`-2`/`-3` bundles): a *planning*
> session on the **way-of-working**, specifically **finishing the v5 handoff machinery deferred
> at the #149 flip** (#163 teeth validator · #164 generator, with #156/#159/#161/#162/#165 + the
> Q9 reconciliation beside). **No design move advanced the way-of-working since the `-architect`
> bundle** (HEAD `66d0293`): the only commits since are that bundle's own merge, a routine
> 2026-06-13 fleet baseline, and — on `origin` only — the 2026-06-13 nightly conformance digest.
> So the open architecture questions (§3) and the task-graph (§4) **carry forward unchanged**
> [recall/inferred from `-architect`]; verify against the live BACKLOG (§5), do not trust the
> re-narration. **What is genuinely new is state, not design** [witnessed]: (1) the `main ↔
> origin/main` **divergence** below — the new headline; (2) two fresh nightly-digest findings
> needing an operator judgment call (§3 Q11); (3) a queue of pending operator actions (§6).
> Orient first (`PROBES.md` P1), **then ask the operator for off-repo context** (§13d), then
> resume the design.

---

## 1. Drift-flags — the headline

From the read-only drift-checks (`validate_doc_claims` #89, `validate_git_backlog` #90) plus
CC's state read at generation. **A flag is a question, not a verdict.** `audit.py health` is
**OK** at generation (16/18 pass; the two `[~~]` below are informational WARNs — health still
exits OK). Re-derive at read-time (P3/P4/P7).

### DRIFT — `main` has **diverged** from `origin/main`: ahead 3 / behind 1 *(NEW headline — reconciliation owed, operator/architect call → Q9-adjacent)*

The `-architect` bundle generated with `main` **in sync**. It no longer is. `git status -sb`
reports **`main...origin/main [ahead 3, behind 1]`** at generation.

- **behind 1** = `ad56397` *"docs(audit): nightly conformance digest 2026-06-13 — 3 high / 0 med /
  0 low (#26)"* — the **nightly cloud Routine** (ADR-72 hub-independence) committed + pushed
  straight to `origin/main`; local `main` has not fetched-and-integrated it.
- **ahead 3** = local-only `1d52af0` (the `-architect` bundle) + `518b0c7` (its merge) + `8d9d35d`
  (the 2026-06-13 fleet baseline) — none pushed.
- **The question (do NOT self-resolve):** this is the **same ADR-80 × core-invariant-5 collision
  as Q9, now in its push-side form** — the cloud Routine writes *direct to `origin/main`* (no PR,
  no `--no-ff` merge from local), so local and remote `main` diverge every nightly. Reconcile how
  — `git pull --rebase` then push the local arc? merge origin's digest in? — **and** decide
  whether the Routine's direct-to-`origin` writes are *sanctioned* (ADR-80 "automation commits its
  own output," extended to the push) or *owed a non-divergent path*. An operator/architect ruling,
  **not** a unilateral CC pull.
- **Confirm:** `git status -sb` + `git log --oneline main..origin/main` (the behind set) +
  `git log --oneline origin/main..main` (the ahead set).

### DRIFT — `no_ff_merges` #153: a direct (FF/non-merge) commit on `main` *(carried — open question, disposition TBD → Q9)*

`audit.py health` reports `[~~] no_ff_merges` naming `61c5b50fa (2026-06-12) docs(audit): nightly
conformance digest 2026-06-12 — 2 high / 3 med / 0 low (#24)` — a **nightly automation writer**
commit landing *direct* on `main` rather than via a `--no-ff` merge. (Note: the new origin-side
digest `ad56397` is the *push-side* sibling of this same pattern — see the divergence flag above.)

- **The genuine tension (do NOT self-resolve):** ADR-80's writer policy says *automation commits
  its own output*; the `--no-ff`-universal invariant (core-invariant rule 5) says *every change
  goes branch → merge*. These **collide on the nightly Routine's own commits.** Sanction it
  (disposition, keyed on the routine's signature) or owe the Routine a `--no-ff` merge path? **An
  architect-session question** (§3 Q9), not a thing to "fix" by reverting the digest.
- **Confirm:** `python scripts/audit.py health` (the `no_ff_merges` line) +
  `git log --first-parent --oneline -8 main`.

### DRIFT — `git_backlog_drift` #90a: a `closes [#77]` still open in BACKLOG *(known-benign, NOT actionable)*

`validate_git_backlog` flags a `closes [#77]` merge (`77e5d7df9`) whose `[#77]` is still present
(open) in `BACKLOG.md`. **This is a dispositioned voided closure — do not "fix" it.**

- **Disposition:** #77 was **re-scoped, not done** (the merge carried `closes [#77]` but shipped
  *different* work — Tier-1 closeout fixes, not the content-consolidation #77 owns), so #77
  legitimately stays open. Direction-(a) #90a structurally cannot distinguish a misattributed
  closure from a real one; only arc-content inspection (**#139** / direction-(b)) can.
- **Why it doesn't block:** `audit.py health` reports it `[~~]` (WARN, informational).
- **Confirm:** `python scripts/validate_git_backlog.py` + check `ecosystem/disposition-register.yaml`.

---

## 2. Planning "why" + the design tensions weighed (architect §13a)

**The theme is unchanged and it is the way-of-working:** v5 is canonical (HANDOFF_PROCESS v5.0,
`Status: stable`, #149 flip 2026-06-11) but the *machinery* the flip deferred is still open. The
spec is written; the **generator** (#164) and the **mechanical teeth** (#163) are not. Every v5
bundle to date — **including this one** — was **hand-assembled by CC following the spec**, which
is itself the standing argument that the machinery must land: hand-assembly is exactly the
drift-prone hand-maintained-surface the methodology outlaws everywhere else. (This refresh
hand-assembled P1–P8 again, for the second `-architect` bundle running — the #161 capture point.)

**No design move was resolved this session.** Unlike the `-architect` bundle (which folded in the
canonical-runbook collapse as a resolved move), this refresh advances no way-of-working decision —
nothing in the commit window since `66d0293` touched the design. The standing design move from the
prior bundle remains the latest: the **canonical-runbook collapse** (per-bundle README dropped;
boilerplate lives once in the freshness-gated `docs/handoffs/README.md`; v5 bundle = three files;
#164 rescoped to seed the runbook idempotently). That move is **done and in the spec** — its
residue is the open tension it created (Q1: per-repo runbook sync without copy-drift).

**The state divergence (§1) sharpens an existing tension, it is not a new design move.** The
nightly Routine writing direct to `origin/main` is the push-side face of Q9 — the same
ADR-80 × `--no-ff`-universal collision, now visible as a remote divergence rather than only a
local `no_ff_merges` WARN. Worth folding into the Q9 ruling rather than treating as separate.

---

## 3. Open architecture questions (carried as residual — design decisions not yet made)

Carried forward from `-architect` unchanged except Q9 (sharpened by §1) and the new Q11.

- **Q1 (#164) — generator shape, *no-per-bundle-README*.** The v5 `/handoff` generator must (a)
  emit the **three-file** bundle (`HANDOFF_BOOT.md` + `RESIDUAL.md` + `PROBES.md`, **no README**)
  with the session-header in the bundle `HANDOFF_BOOT.md`, and (b) **idempotently seed/update each
  repo's `docs/handoffs/README.md` runbook** from the single source
  `templates/handoff/v5/README.md.tmpl` (a **deferred stub** until #164 lands), replacing the v4
  Phase-1/2 prose in `.claude/commands/handoff.md` + `SESSION_SETUP`. **Open:** (i) the
  per-repo-runbook sync rule — write-if-absent-or-version-changed, but *how is "version" keyed*
  (handoff-process version? a content hash?) so a genuine runbook edit isn't clobbered and a stale
  one isn't left? (ii) the **cross-repo v4 routing** ambiguity (ADR-83): a v4 target repo (one
  lacking `scripts/audit.py`) needs a deterministic route to the v4 Phase-1/2 path — the v5
  emissions can't bind a target that has no audit checks to probe.
- **Q2 (#163) — teeth validator.** `scripts/verify_handoff_probes.py` (read-only, Layer-2): prove
  a bluffable probe FAILs and a live-grounded probe PASSes, wired into the verification cadence.
  **Fold in degrade-loudly:** an unresolved anchor (missing ref / renamed section / errored
  command) must FAIL or WARN `anchor-missing`, **never vacuously pass** — an explicit test case.
- **Q3 (#156) — durable task-graph.** The architect task-graph (§4) is *ephemeral residual prose*
  today because the ADR-66 BACKLOG schema encodes no depends-on / parallel fields. Durable
  encoding = `validate_backlog` extension + ADR-66 amendment. Worth it now, or residual-only until
  there are enough multi-item arcs to pay for it?
- **Q4 (#161/#162) — teeth probe-core + actor-vs-mode vocab.** Post-flip cleanups: a reusable
  probe-core (bundles stop hand-assembling probe sets per handoff — note this is the **second**
  `-architect` bundle to hand-assemble P1–P8); disambiguate "architect" the *actor* (Layer-1
  browser) from "architect" the *mode* (§13) atomically across every surface.
- **Q5 (#159) — operator-context beat.** Exercise the §13d beat in a *real* architect session and
  confirm it carries off-repo intent without re-narrating the residual. (The #149 v5→canonical
  carry is DONE; only the real-session exercise remains — *this* session is again a candidate.)
- **Q9 — automation-writer vs `--no-ff`-universal (now two-faced: local WARN + remote
  divergence).** The §1 `no_ff_merges` WARN (local direct commit) **and** the §1 `origin/main`
  divergence (nightly Routine pushing direct to remote) are the **same** ADR-80 × core-invariant-5
  collision in two forms. Sanction the nightly-Routine writes (disposition, keyed on the routine
  signature, covering both the local commit and the remote push) or give the writer a non-divergent
  merge/PR path? An ADR-80 × core-invariant-5 reconciliation, **not** a revert and **not** a
  unilateral pull.
- **Q10 (#165) — ASCII-vs-mermaid selection rule.** A *proposed* ADR-51-family amendment
  (operator-set 2026-06-12; first applied when the runbook chose mermaid), awaiting ratification —
  not a unilaterally-minted ADR. Record where the diagram convention lives once ratified.
- **Q11 (NEW, #81 nightly arc) — shallow-history guard + the persisting CLAUDE.md §8 finding.**
  The 2026-06-13 nightly digest (`ad56397`, #26: 3 high / 0 med / 0 low; raw 8 → survived 3 →
  killed 5) reports **two distinct things needing an operator judgment call:** (a) a **persisting**
  finding F3/S3 — `CLAUDE.md` §8 carries a *stale skills-dir claim* (this survived 4-of-5 prior
  findings being resolved); (b) **two new skeptic-borderline findings (S1/S2)** — pre-shallow-
  boundary JOURNAL SHAs from May 2026 the conformance check flags, raising whether the
  **shallow-history guard** applies to JOURNAL SHA-citation checks. Neither is a way-of-working
  *design* decision; both are operator dispositions the next session should clear. **Confirm:** read
  `docs/audits/nightly/2026-06-13-conformance-nightly-digest.md` (on `origin/main` — fetch/integrate
  per §1 before it is local).

---

## 4. The task-graph (ephemeral — NOT a durable BACKLOG field, #156)

Carried as residual prose per §13b; do **not** claim this is encoded in BACKLOG. Under theme
**"Finish the v5 handoff machinery deferred at the #149 flip"** — unchanged from `-architect`:

- **#163 (teeth validator)** is the closest-to-ready and **gates trust in every v5 bundle** (it
  mechanically replaces the manual probe-gate every bundle so far — this one included — has leaned
  on). → **do first.**
- **#164 (generator)** is **L (large)** and now **depends on the cross-repo / runbook-sync routing
  decisions (Q1)**; it consumes the (stubbed) `templates/handoff/v5/README.md.tmpl` and ideally the
  #163 validator (so its output is mechanically checkable). → after Q1; pairs with #163.
- **#156 (durable task-graph), #161, #162** are **independent cleanups** — parallelizable beside
  the above; none blocks #163/#164.
- **#165 (mermaid rule)** and **Q9 (automation/`--no-ff`, now incl. the remote divergence)** are
  **decision items**, not build items — resolve via ratification / operator ruling; parallel.
- **Q11 (nightly dispositions)** is an **operator-judgment clearance**, off the build path — clear
  it independently of the machinery work.

(Dependencies/parallelization above are the architect's read, **not** a schema fact — #156 is what
would make them durable.)

---

## 5. Lean task-state — pointer, not narration (§6)

- **Spec is the BACKLOG.** Read `BACKLOG.md` theme **"Finish the v5 handoff machinery deferred at
  the #149 flip"** (line ~30, under `## Handoff continuity`) for the live tickets: **#163, #164**
  there, plus **#156, #159, #161, #162, #165** across the same continuity theme. Do **not** trust
  any re-narrated ID text — open the live BACKLOG (the §3 text is recall, the file is truth).
- **Live branches:** at generation, `git branch -v` shows `main`, a straggler
  `docs/handoff-canonical-runbook` (a prior handoff branch — **not merged/deleted**; flag for
  cleanup), and this handoff's own `docs/handoff-2026-06-13-architect` (merges on completion).
- **Drift-flags:** the three in §1 — the **`origin/main` divergence** (NEW headline; reconcile +
  Q9), `no_ff_merges` #153 `[~~]` (open Q9), `git_backlog_drift` #90a `[~~]` (known-benign/
  dispositioned). Re-derive at read-time via `python scripts/audit.py health` + `git status -sb`.
- **Push state:** `main` **ahead 3 / behind 1** of `origin/main` at generation — **diverged, not
  in sync** (the change from `-architect`). Re-derive (P3): `git status -sb` +
  `git log --oneline main..origin/main`.

---

## 6. Pending operator actions surfaced at session start (off-theme — pointers, not architect work)

Not way-of-working planning; surfaced so they are not lost. Each is an operator-gated action, not
CC's to run unprompted:

- **18 closure proposals** await — `/review-closures` (human-gated, done-items-leave).
- **changelog drift** — `claude-code 2.1.177 > last reviewed 2.1.168` — `/changelog-review`.
- **5 nightly triage findings** await — #27, #25, #23, #21, #19 (Issues tab) — distinct from the
  #26 digest's F3/S1/S2 above (Q11).
- **fleet health** — 2 issue(s) across 5 repos (`logs/FLEET-HEALTH.md`).
