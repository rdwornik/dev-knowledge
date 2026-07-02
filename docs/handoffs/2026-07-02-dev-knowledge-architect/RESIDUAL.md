# Residual — 2026-07-02 architect handoff (the part the repo does not already encode)

<!-- scope: meta -->

> **What this is (v5 §2).** CC's handoff is **only the residual** — the un-committed "why," the
> pointers, and the **drift-flags as the headline**. It does **not** re-transmit methodology
> (pointer + mechanical enforcement, §3) or re-narrate task-state (pointer to `BACKLOG.md`, §6).
> This is **architect mode** (§13): the residual is scoped to the *planning* "why," task-state
> points at the whole BACKLOG / relevant themes, and the open architecture questions travel as
> residual so the next session resumes the design rather than rediscovering it.
>
> **Generated LIVE at the end of a CC-execution window.** The window since the 2026-07-01
> architect handoff **executed that handoff's arm-first brief** — the deploy carrier arming
> (#226), the #230 conformance self-test, the real ai-council arming, the ARCHITECTURE currency
> arc (#222/#223/#224), plus an external-review audit and the first cross-repo handoff. The
> strategic "why" is **largely in the repo**: **ADR-93** (floor model A), `LESSONS.md`, PLAYBOOK
> §20, the two 2026-07-02 audit artifacts, and the JOURNAL arc. There was **no single outgoing
> browser architect chat** holding un-committed deliberation, so `SUPPLEMENT.md` is generated
> **empty (the cold-handoff disposition)** and the incoming **§13(d) beat fires FULL**.
>
> **Four-tag discipline.** `witnessed` = CC re-derived it live this generation (the §1 gate
> outputs); `recall`/`inferred` = reconstructed from the JOURNAL/git window, may have moved —
> the load-bearing ones are re-checkable via `PROBES.md`. `unknown` = stated as such.

---

## §1 — Drift-flags (THE HEADLINE — surfaced first, not buried)

Produced by the live read-only drift-checks (`audit.py ship-gate`, `validate_git_backlog`,
`validate_doc_claims`, `validate_backlog`) at generation (**witnessed**).
**Re-derive each at read-time** — the teeth are in `PROBES.md`, not in trusting these lines.

### ✅ HEADLINE — `ship-gate` is GREEN and **CLEAN**; the 2026-07-01 forced-freshness debt is **RESOLVED**

`python scripts/audit.py ship-gate` → **GREEN** (**6 WARN dispositioned**, **NO `[stale]` line**) —
verification organs green against this arc. This window did **not** add drift; it **drained** the
one real debt the prior handoff flagged:

- **The forced-freshness-stamp anti-pattern is FIXED (#222, witnessed).** The three volatile
  count-claims (audit check-count / pre-commit gate-count / pytest-collected) were **moved out of
  `ARCHITECTURE.md`** into the loose-generated `ecosystem/doc-counts.md` (a non-`_FRESHNESS_FILES`
  file, so a count-bump no longer forces a `canonical_freshness` re-stamp). `validate_doc_claims`
  now reads **pytest_collected 1030/1030 MATCH** against the generated file — the drift that was
  dispositioned pending #222 at the last handoff is **gone**, no disposition needed.
- **`ARCHITECTURE.md` now DOCUMENTS the deploy subsystem (#223, witnessed).** The prior handoff's
  "ARCHITECTURE omits the ADR-91/92 `deploy/` subsystem" gap is closed via a **genuine end-to-end
  re-read**; `last_reviewed: 2026-07-02` is now an **honest** stamp (not the forced stamp #222
  described). `canonical_freshness`: **6 canonical files fresh** [OK]. `PROBES.md` P5 re-checks.

### Standing flags (benign / dispositioned — unchanged, do NOT touch)

- `git_backlog_drift`: **#77** — the known voided-closure false positive (`77e5d7df9` closes #77 but
  #77 stays in BACKLOG by design — operator ruled keep-open). Dispositioned
  (`warn-77-voided-closure`). **Standing false positive — do not touch.**
- `no_ff_merges`: **3** journal-wrap / transcript-archive direct-to-`main` commits (`533109f20`,
  `3a894eeb5`, `d0f9ead67`) print `[~~]` under `health`, `[disp]` under `ship-gate`. **Expected
  seam, not a regression.** **#210** (open) proposes converting this class from per-instance
  disposition to a standing rule (path-scoped EXEMPT or branch-then-merge the JOURNAL wrap) — a
  §4-adjacent decision.
- `handoff_probes`: **P5/P7 cross-repo** in `2026-07-02-ai-council-architect` — the first cross-repo
  bundle's `.claude/`-target + ambiguous-basename probes degrade to WARN (`skipped`, honest-partial).
  Dispositioned (`warn-handoff-probes-p5/p7-crossrepo-ai-council-2026-07-02`), pending **#234** (harden
  `.claude/` cross-repo targets to full FAIL teeth). **Expected — not a regression.**

---

## §2 — Shipped this window (2026-07-01 → 2026-07-02) — the map, not the narration

Pointer-first (`git log --first-parent`, `JOURNAL.md` top ~5, `LESSONS.md`, ADR index). **recall/inferred**
from the window; re-derive load-bearing counts via `PROBES.md`.

**The arm-first chain EXECUTED — this is the window's spine (the prior handoff's brief, delivered):**
- **#226 + #230 (`b986711`, `feat/226-arm-floor-230-conformance`):** the **floor carrier was ARMED**
  (@-include in child `CLAUDE.md`, `check_floor_hash.py`, floor-hash-verify hook, `pre-commit install`,
  `.gitignore` negation — the model-A mechanism) and the **#230 conformance self-test built**; then
  **real ai-council was ARMED** — turning the "configured, not armed" facade the prior supplement
  named into an **armed** system (Layer-2 9/9 green). **ADR-93 ratified** (floor provisioning model A,
  armed + conformance-proven). This closes the two load-bearing items of the arm-first chain.
- **#222/#223/#224 (`a95e3b0`, `docs/architecture-deploy-currency`):** ARCHITECTURE currency —
  **decoupled** the three count-claims into `ecosystem/doc-counts.md` via a new loose
  `scripts/gen_doc_counts.py` (**#222**, the forced-freshness fix), **documented** the deploy
  subsystem in `ARCHITECTURE.md` Ch2/Ch4/Ch6 + Validators + Governing-ADRs via genuine re-read
  (**#223**), and **rotated** CLAUDE §11 + the Governing-ADR lists to 89→93 (**#224**). 1030 tests pass.

**Two adjacent doc arcs also landed:**
- **External-review system audit** (`4467159` + `a157dda` §4 completion): a comprehensive
  system audit for external architectural review + per-doc §4 coverage of the six append-only /
  protocol / session docs (LESSONS/JOURNAL/CONTRIBUTING/ESSENTIALS/HANDOFF_PROCESS/DEFINITION_OF_DONE).
- **First-ever cross-repo architect handoff** (`fef026e`): a v5.3 cross-repo bundle for **ai-council**
  (read-only per ADR-36/41). It **tripped the #163 probe-teeth validator's cross-repo assumption**
  (probes bound to ai-council paths resolved against the hub → false FAIL/PASS); operator-ruled
  **Option 3** (resolve against the target repo) → patched `check_handoff_probes` +
  `verify_handoff_probes.py` (cross-repo dispatch, honest-partial WARN for foreign `.claude/`),
  and filed **#234** to harden `.claude/` targets to full teeth.

---

## §3 — Task-state (pointer, not narration — §6)

- **Primary source: `BACKLOG.md`** (**94 tasks, 7 themes, 21 stories** — witnessed via
  `validate_backlog`) — the spec; items are tickets. Do not re-narrate; open it.
- **Live branches:** `git branch -v`. At generation: `main` (integrated), `automation/fleet-audit`
  (a standing automation branch), and this handoff branch `docs/2026-07-02-architect-handoff`.
- **Durable task-graph (schema, #156):** `python scripts/validate_backlog.py` prints the
  serialize-groups + any `depends-on` cycle. This window's tells (verify via `PROBES.md` P9):
  **code-edge = just `#218`**, **coherence = `#180/#181/#182/#220`** (unchanged), **audit-py group now
  includes `#234`** (the new cross-repo-teeth item). **`#221`'s `depends-on: #226` is SATISFIED and
  cleared** — #226 (arming) closed this window, so the hard edge that gated fleet is gone; fleet is now
  navigable.

---

## §4 — The next frontier (open architecture decisions — this is a DECISION + SEQUENCING session)

The deploy subsystem is now **BUILT + ARMED + PROVEN (n=1) + DOCUMENTED**. The arm-first chain
(#226 → #230 → #222/#223) is **done**. The center of gravity shifts to **disseminating an armed,
proven subsystem to the fleet** — the leaf that was gated on arming is now **unblocked**. **recall/inferred**
— the architect resumes the design here.

**The remaining chain (the repo encodes the dependency; the priority is the architect's call):**
> **#225 (surgical precommit carrier — clean diffs at scale)** → **#221 (fleet rollout to n=2+, the leaf)**.

1. **#221 — fleet rollout (the now-unblocked leaf).** Run `deploy/tool.py` on the other consumers
   (**corp-monorepo / corp-ops / corp-sca-time-automation**) to reach the **n=2+ generalization gate**
   and populate the `deployed_methodology_version` registry fleet-wide; each repo's deploy uses the
   **#230 conformance self-test as its acceptance gate**. #221's done-when **also requires #225 closed**
   (the deploy-arc residual) — so the sequencing decision is **#225 first (surgical diffs), then fleet**.
   The generalization probe (from #215): the first non-hub, structurally-different repo is the real test
   of whether the two lifelines transfer — surface any hub-specific convention that does NOT transfer
   **before** assuming universality.
2. **#225 — precommit carrier surgical edit.** `deploy/carrier_precommit.py` currently round-trips the
   whole `.pre-commit-config.yaml` (YAML load/dump), stripping comments + reindenting → noisy deploy
   diffs. Replace with a comment-preserving surgical insert/update of only the methodology-owned hooks
   (matching the version-record writer's byte-faithful principle). Precedes fleet so rollout diffs are
   clean at scale.
3. **#231 — consumer→hub feedback loop (open).** When a consumer detects a gap/ambiguity/broken piece
   (incl. a failing #230), it emits a **structured hub-destined report** instead of guessing. Encodes
   "when unsure, ask the hub; verification flows upstream." Open: report **schema + transport + home**;
   the philosophy-line placement (ESSENTIALS/PLAYBOOK) is a flagged sub-note, scope when built.
4. **#234 — cross-repo probe FAIL-teeth (filed this window).** Harden `check_handoff_probes` so a
   cross-repo bundle's `.claude/<file>` target resolves against the **target root** — a present
   floor-guard probe PASSes, a genuinely-absent one **FAILs** (real teeth) — while excluded-dir
   duplicates stay pruned. Currently honest-partial WARN; the operator accepted that as the interim.

**Adjacent open decisions (smaller):**
- **#220 — the MODIFY / semantic-drift axis.** VERIFY-FIRST: does the ADR-89 Pyright oracle or any
  existing organ gate a *meaning-change-without-version-bump*, or only add/remove/exist? Establish a
  demonstrated-catch bar before any design.
- **#210 — journal-wrap no-ff standing rule.** 3 instances of one class now dispositioned one-by-one →
  decide the shape: a path-scoped EXEMPT in `no_ff_merges` (JOURNAL/transcripts-only diffs pass, any
  other path still WARNs — must NOT weaken core-invariant #5) vs branch-then-merge the wrap (eliminate
  the class).
- **#233 — deploy-record-index test tempdir isolation.** Test-hygiene debt: `test_no_temp_index_leftovers`
  snapshots the shared tempdir → false-fails under concurrent suite runs. Fix: per-run isolated tempdir.
- **#232 — ship-gate right-sizing (UNFILED candidate, carried from the 2026-07-01 supplement).** Full-pytest
  on a doc-only change is disproportionate; the fix is **right-size, not skip** (the doc gates caught real
  errors). Referenced by #233 but **never filed as its own BACKLOG id** — the architect files it or folds it.

---

## §5 — Pointers (open the primary source; do not trust a paraphrase)

- **Orient:** `VISION.md` `## Vision`, `ARCHITECTURE.md` Ch1 `## Purpose [CORE]` (forced-read via P1).
- **Methodology:** `protocols/PLAYBOOK.md` (esp. §20 deploy runbook), `protocols/ESSENTIALS.md`,
  `CLAUDE.md`. Referenced by pointer, enforced mechanically (§3) — never re-narrated.
- **The arm-first arc's "why":** **ADR-93** (floor model A, armed + conformance-proven), `LESSONS.md`,
  PLAYBOOK §20, `deploy/` (tool.py + carriers + `carrier_floor.py`), the two 2026-07-02 audit artifacts.
- **This window's captures:** `BACKLOG.md` #221 / #225 / #231 / #234 / #233; the JOURNAL top entries
  (`f97360e`, the ai-council handoff arc, `b986711`).
- **Gate the design against live state:** run `PROBES.md` P1–P9. Any FAIL blocks onboarding.
