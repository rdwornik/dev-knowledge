===== FILE: 05_NOW — start =====

# 05 · What to do now

## Immediate objective

Two parallel, non-conflicting moves. **(1)** Read the **first production nightly PR**
when it lands (03:00 local) — the operational thread; it feeds assumptions Phase D will
codify. **(2)** Open the **Phase-D chat with the EXISTING `2026-06-05-dev-knowledge-session`
bundle** (v4.3.2). Do **not** regenerate that bundle under v4.4 — bundles are immutable,
and v4.4 applies to the NEXT handoff. The natural first v4.4 exercise is the handoff that
closes Phase D (or the universalization arc after it). Scope: docs/methodology + reading
an operational PR — no code.

## Top priorities (from BACKLOG)

Open P1s most relevant to this thread (full queue in `BACKLOG.md`):

- **[#1] Fresh-eyes review for every routine handoff** — extend triangulation from the
  promotion gate to every Phase-2 handoff. Directly live: v4.4 is beta and its first
  real exercise *is* its promotion test (the built-in measurement).
- **[#2] Contradiction-detection across ADRs** + an ownership model (amend vs new ADR
  vs clarification) — the 65+ ADR corpus needs it.
- Session-context priorities from the sender: the nightly run's three looks (below),
  the Phase-D chat, and `[#86]`'s three ADRs + AI-Council work (deliberately post-Phase-D).

## In-progress branches & repo state

- Local branches: `main` (`d031d39`) and `docs/handoff-2026-06-04` (this handoff's
  feature branch — merge after Phase 2). No other feature branches; `origin` has only
  `main`. The `docs/machinery-inventory` branch the sender flagged **no longer exists**
  (verified absent at Phase 2 — see `04_RECENT` facts table).
- **First production nightly run is pending** (scheduled, outcome unknown). Three looks
  when it lands: raw count **without** the shallow-clone false-positive class (V1 guard's
  first real test), a clean porcelain tripwire (fleet fail-soft's first real test), and
  the Run-line path (expected: spec-orchestration fallback; a native run would be news).
- **Branch:** `main`  ·  **HEAD:** `d031d39`
- **Working tree at generation:** clean

## Boundaries

- Do not open the Phase-D chat by regenerating its bundle — use the existing v4.3.2 one.
- Do not begin `[#86]`'s ADRs / AI-Council work before Phase D — deliberately sequenced after.
- Do not treat v4.4 as stable — it is beta until a real handoff passes the promotion criterion.
- The `docs/machinery-inventory` branch is gone; nothing to adjudicate there now.

## How to choose

If this presents multiple candidate first-moves, **propose your choice with rationale
to Rob** — don't ask him to forced-rank. The two moves above are parallel and
non-conflicting; reading the nightly PR first (if it has landed) is the low-cost,
assumption-feeding move. Rob confirms or redirects.

## Top landmines (do-not list)
<!-- positional-redundancy: deliberate duplicate, do not deduplicate (v4.4 §A/§B) —
     RECENCY-PEAK tail: the last thing read before acknowledgment. -->

### Session landmines

- **Do NOT regenerate the `2026-06-05` Phase-D bundle under v4.4** — bundles are
  immutable; v4.4 applies to the NEXT handoff.
- **Do NOT trust any bundle/map prose about repo state without grep** — the
  staleness-map incident is this window's proof; `[#89]` exists for exactly this.
- **Do NOT stamp records with the harness (UTC) date** — local convention governs;
  this very interview first shipped with a wrong `06-04` slug, since re-slugged.
- **Do NOT deduplicate the A1/A2 positional redundancy or strip its guard comments** —
  it's a deliberate DRY violation, stated in the v4.4 amendment.
- **Do NOT deviate silently from A1–A6 when generating the next bundle** — v4.4 is beta
  and its first exercise IS the promotion test. (Also: the `/handoff` skill now reads
  version/status from the spec — do not re-introduce a hardcoded version "for clarity".)

### Standing invariants (repeat)

The load-bearing invariants from `01_ROLE`, repeated here at the recency peak:

- **Append-only** `LESSONS.md` / `logs/TOKEN-LOG.md`; **immutable** ADRs / handoffs /
  transcripts / audits (supersede, never edit in place).
- **Layer 2 never executes** — read-only validators only.
- **No leftovers** — clean up and verify removal of anything you create.
- **OneDrive - Blue Yonder** — never write to or delete inside it.

===== FILE: 05_NOW — end =====
