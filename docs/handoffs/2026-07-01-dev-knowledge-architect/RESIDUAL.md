# Residual — 2026-07-01 architect handoff (the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **Generated LIVE at the end of a CC-execution window; SUPPLEMENT EMPTY (cold disposition).**
> The window since the 2026-06-27 architect handoff was a **CC-execution-driven** arc — the deploy
> subsystem build (ADR-91/92), the first real deploy (ai-council → v1.0.0), the C5 loop close, the
> hub currency+coherence audit → BACKLOG reconciliation, and this session's pre-handoff capture.
> There was **no outgoing browser architect chat** holding un-committed strategic deliberation, so
> `SUPPLEMENT.md` ships **empty** and the incoming **§13(d) beat fires FULL**. The strategic *why*
> is largely already in the repo: **ADR-91/92**, `LESSONS.md` (the run-#1 retrospective + 3
> meta-lessons), **PLAYBOOK §20** (the deploy runbook), and the JOURNAL arc.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved —
> the load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and **CLEAN**; the window added **zero** new drift

`python scripts/audit.py ship-gate` → **GREEN** (**4 WARN dispositioned**) — verification organs
green against this arc. **No new WARN and NO `[stale]` disposition this window.** This was a heavy
**build + reconciliation** window that *drained* drift, not one that created it: it built the entire
`deploy/` subsystem (two ADRs ratified, four carriers + orchestrator), filed the audit-surfaced debt
as tracked BACKLOG items (#220–#231) rather than leaving it latent, and kept every doc-only capture
commit net-neutral on the doc_rot budget.

### The one currency debt is TRACKED, not silent — ARCHITECTURE.md ↔ the deploy subsystem

The single real coherence gap this window is **already filed**, so it is not a surprise:
- **`ARCHITECTURE.md` omits the ADR-91/92 `deploy/` subsystem entirely** (the only 'deploy' hit is
  the unrelated nightly Routine) — filed **#223** (document the deploy subsystem via a genuine
  re-read) with **#222** (decouple the volatile pytest-count claim from the freshness gate) and
  **#224** (rotate the Governing-ADR lists to include ADR-90/91/92). **inferred** from the audit.
- **`ARCHITECTURE.md`'s `last_reviewed: 2026-07-01` is a FORCED stamp** (#222): the last ~6 commits
  that touched it were pytest-count bumps (947→965→977→979→980), each forcing a `canonical_freshness`
  re-stamp **with no genuine end-to-end re-read**. `canonical_freshness` PASSES (stamp on/after last
  touch) — the *genuineness* is the open item, not the gate. `PROBES.md` P5 surfaces this. **witnessed.**

### Standing flags (benign / dispositioned — unchanged, do NOT touch)

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned
  (`warn-77-voided-closure`). **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits print `[~~]` under
  `health` but are `[disp]` under `ship-gate`. **Expected seam, not a regression** — `ship-gate`
  GREEN. **#210** (open) proposes converting this class from per-instance disposition to a standing
  rule (path-scoped EXEMPT or branch-then-merge the JOURNAL wrap) — a §4-adjacent decision.

---

## §2 — Shipped this window (2026-06-27 → 2026-07-01) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~12, `LESSONS.md`, ADR index). **recall/inferred**
from the window; re-derive load-bearing counts via `PROBES.md`.

**The deploy subsystem was built end-to-end and proven on run #1 — this is the window's spine:**
- **ADR-91** (methodology corpus versioning) + **ADR-92** (deploy runbook doctrine) — both **ratified
  Accepted**; v1.0.0 baseline; the `deployed_methodology_version` registry + reader landed (live
  `audit.py` check #25).
- **`deploy/` orchestrator + 4 carriers built**: carrier contract (C1) → precommit / global-config /
  floor / tier1-plugin carriers → ASSESS half (C2a, read-only) → EXECUTE half (C2b, apply/verify loop
  with a verify-gate that records only on full verify).
- **First real deploy: ai-council → methodology v1.0.0** (run #1). Halted mid-close on a **CRLF
  blocker**, then a **second encoding bug**, → a **full Windows-text-mode-git-I/O class sweep**
  (LF-normalize the writer; stdout-strict/stderr-lenient decode; byte-fidelity regression tests). The
  record verified on **both axes** (committed registry record + committed ruff-gate).
- **C5 loop close** (ADR-92 archive→document→educate): **PLAYBOOK §20** deploy runbook + floor
  semantics; **4 LESSONS** (the run-#1 retrospective + 3 meta-lessons: Windows-I/O as a tested-from-
  start invariant; verify-the-bytes-before-merge; the verify-gate + executor judgment is the
  load-bearing safety net).

**Then the corpus was reconciled to the deploy reality (doc-only):**
- **Hub currency+coherence audit → BACKLOG reconciliation**: filed **#220–#229** (deploy-arc
  reconciliation + carrier residuals #225/#226; the MODIFY/semantic-drift dependency axis #220;
  ARCHITECTURE currency #222/#223/#224; repo hygiene #227/#228/#229) + the **#131↔#215 SPLIT**.
- **This session's pre-handoff capture** (the reason this handoff exists — turning tacit decisions
  into tracked state): **#226(a) DECIDED = floor model A**; filed **#230** (end-to-end conformance
  self-test) + **#231** (consumer→hub feedback report); **#221** sequenced (`depends-on: #226`, #230
  as the per-repo acceptance gate). Shipped `7cc4b6a`.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** (97 tasks, 7 themes, 21 stories) — the spec; items are tickets.
  Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (integrated), `automation/fleet-audit`
  (a standing automation branch), and this handoff branch `docs/2026-07-01-architect-handoff`.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the
  serialize-groups + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9):
  **code-edge = just `#218`**, **coherence = `#180/#181/#182/#220`** (`#220` newly joined),
  and the new hard edge **`#221 depends-on #226`**. Soft/provenance relations stay residual prose (below).

---

## §4 — The next frontier (open architecture decisions — this is a DECISION + SEQUENCING session)

The dependency-management spine and the deploy *machinery* are **built**. The center of gravity now
shifts to **disseminating a built-but-un-armed subsystem** — the decisions below are sequencing +
priority calls, not builds. **recall/inferred** — the architect resumes the design here.

**The core sequencing chain (the repo encodes the dependency, NOT the priority):**
> **#230 (conformance self-test, unbuilt)** ← gates → **#226(b) (arm the floor carrier + arm
> ai-council)** ← gates → **#221 (fleet rollout to n=2+)**.

1. **#226(b) — arm the floor carrier.** The model is now DECIDED (A: commit-the-floor + hash-guard,
   tracked not gitignored). The build remains: fix `deploy/carrier_floor.py` to ARM (@-include in
   child CLAUDE.md, `check_floor_hash.py`, floor-hash-verify hook, `pre-commit install`, `.gitignore`
   per model A) + arm ai-council (today **configured-not-armed**: no gate fires, the floor does not
   auto-load). **Done-metric = the #230 self-test passes in ai-council.** The ADR that formalizes model
   A is authored **during** this build (not before) — #226 owns it. Also reconcile PLAYBOOK §20's
   "local-only" prose (SUPERSEDED by the tracked+guarded model).
2. **#230 — build the conformance self-test first?** It is the hard-metric acceptance for #226(b) AND
   the per-repo gate for #221 — a shared gate. **Decision:** build #230 before or alongside #226(b), so
   arming has a real acceptance test rather than a files-present check. Distinct from #171/`conformance.md`
   (static presence + staleness); #230 proves the loop FUNCTIONS.
3. **#221 — fleet rollout.** MUST follow #226 (so fleet repos don't replicate ai-council's
   configured-not-armed gap); each repo's deploy uses #230 as its acceptance gate. Target: n=2+
   (corp-monorepo / corp-ops / corp-sca-time-automation) to clear the generalization gate.
4. **#231 — consumer→hub feedback loop** (new): when a consumer detects a gap/ambiguity/broken piece
   (incl. a failing #230), it emits a **structured hub-destined report** instead of guessing. Encodes
   "when unsure, ask the hub; verification flows upstream." Sub-note flagged: the philosophy line may
   belong in ESSENTIALS/PLAYBOOK — scope when built.

**The competing investment — pay down currency debt first?** #222/#223/#224 (document the deploy
subsystem in ARCHITECTURE.md + decouple the count from the freshness gate + rotate the ADR lists).
The architect's call: **arm+rollout now** (momentum, the deploy arc is warm) **vs. currency first**
(ARCHITECTURE is the structural map and is now materially wrong about a whole subsystem). Both are
filed; only the priority is undecided — this is exactly the off-repo *why* the §13(d) beat should
surface.

**Adjacent open decisions (smaller, filed):** #210 (journal-wrap no-ff standing rule vs per-instance
disposition); #220 (the MODIFY/semantic-drift axis — verify-first whether any organ catches a
meaning-change-without-version-bump); the ADR-status-header legibility class (#162/#166 — do NOT "fix"
a frozen ADR header without deciding the convention first).

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook, "## The two lifelines"),
  `protocols/ESSENTIALS.md`, `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The deploy arc's "why":** ADR-91, ADR-92, `LESSONS.md` (run-#1 retrospective + 3 meta-lessons),
  `deploy/` (tool.py + carriers).
- **This session's captures:** `BACKLOG.md` #226 / #230 / #231 / #221; the JOURNAL top entry (`be9922d`).
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
