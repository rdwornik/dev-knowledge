===== FILE: 05_NOW — start =====

# 05 · What to do now

## Immediate objective

The operator dictated a **macro-agenda** for the next arc — do not reorder it on your
own judgment. The natural *first moves* (mechanical, low-risk) are: **(1)** clear the
owed hub bookkeeping — record #86.3 (source: corp JOURNAL 2026-06-06), close #86 once
sub-decision 3 is ruled, log n=2; **(2)** read the **2026-06-07** corp scheduled-night
digest (run 2-of-2 for #84), including whether the corp renderer emits a
delta-vs-baseline section; **(3)** then **#84 codification** — because the rubric and the
onboarding runbook downstream depend on it. Scope is one coherent objective, not the
whole agenda at once. Work type: docs / architecture / audit (no code-level work).

The operator-ratified sequence (the agenda these first moves open):

1. **Close the automation system as a SYSTEM** — one consolidated doctrine pass over
   hooks, configs, workflows, loops, routines: which layer for which job, what the ADR
   set still owes, #84 codification (after the n=2 night), #85's local-tier decision. The
   pieces are individually proven; the coherent whole is not yet written in one place.
2. **ai-council handoff in a DEDICATED new browser chat** (one chat per repo is the
   operator's standing model). This dev-knowledge successor chat *supports* that — the two
   repos are coupled (the council mediates methodology decisions).
3. **Governance process design** — how dev-knowledge, as the managing layer, runs ADR
   lifecycle, skills design, and conformance across all repos.
4. **monorepo handoff LAST**, in its own dedicated chat, supported from here —
   corp-monorepo is the oldest repo and the methodology changed substantially this arc;
   its handoff must carry the NEW standards.
5. **Meta-process (stage TBD by operator)** — which routines the ecosystem should run
   (morning briefing, doc-drift, LESSONS mining, debate→ADR distiller, full #81 rulebook);
   a repo-onboarding runbook; methodology-conformance verification — all anchored in
   dev-knowledge's VISION/ARCHITECTURE. Operator framing: *dev-knowledge is well-built;
   what remains is onboarding it properly against everything else.*

## Top priorities (from BACKLOG)

- **[#84] [P2]** Workflow-doctrine codification package — **gated at n=1-of-2**; the
  second real run is the corp 2026-06-07 night. Author the PLAYBOOK two-tier section +
  adoption ADR + Routine/night standard once n=2 lands.
- **[#86] [P3]** Cloud-night decision package — sub-decisions 1 & 2 recorded (ADR-72);
  **sub-decision 3 (R2 saved-workflow distribution ruling) remains** before #86 closes.
- **[#89] [P3]** Deterministic prose-vs-state checker — concrete check-source now exists
  (~6 of 29 corp checks are binary, mechanizable); the natural mechanization of this arc.
- **[#1] [P1]** Extend triangulation (fresh-eyes pass) to every routine handoff.
- **[#2] [P1]** Contradiction-detection across decisions + ownership model (amend vs new
  ADR vs clarification). See `BACKLOG.md` for the full queue.

## In-progress branches & repo state

- **Branch:** `docs/handoff-2026-06-06` (this handoff's working branch; merges to `main`
  via `--no-ff`). No other unmerged feature branches at capture.
- **HEAD:** `608f26b` (the captured base) · **Working branch tip** advances with the
  handoff commits.
- **Working tree at generation:** clean (handoff artifacts staged on the handoff branch).

## Boundaries

- **Do not reopen the 2026-06-06 hub missed-night question** — operator ruling; the
  digest-presence check watches the class; only a SECOND consecutive miss reopens it.
- **Do not author #84 codification before the n=2 night lands** — that is the
  easy-metric premature-closure failure this gate exists to prevent.
- **corp-monorepo is read-only from here** (ADR-36/41) — its handoff is a separate
  dedicated chat (agenda item 4); never direct its work or edit its files from this chat.

## How to choose

If multiple first-moves are candidates, **propose your choice with rationale to Rob** —
don't ask him to forced-rank. Operator energy is finite; reasoned pre-selection is your
job. Rob confirms or redirects.

## Top landmines (do-not list)
<!-- positional-redundancy: deliberate duplicate, do not deduplicate (v4.4 §A/§B) —
     RECENCY-PEAK tail: the last thing read before acknowledgment. -->

### Session landmines

- **Do NOT put a hub reference on a cloud executing path (ADR-72)** — a future cloud need
  for hub material = STOP and escalate; publishing a methodology subset is the operator's
  data-classification call alone.
- **Do NOT trust prose about state — including this bundle.** Grep before acting on any
  load-bearing claim; cross-repo claims name the repo per claim.
- **Do NOT reopen the 2026-06-06 hub missed-night** — operator-ruled closed.
- **Do NOT improvise process from memory** — read LESSONS / gotchas for the environment
  traps (PS 5.1 runtime, gh-auth expiry, parallel-session tree contamination, harness
  clock a day behind); they carry `verify:` lines. Don't rely on this narrative for them.
- **Do NOT codify a pattern from one run** — #84 waits for n=2 (the 2026-06-07 night).

### Standing invariants (repeat)

The load-bearing invariants from `01_ROLE`, repeated here at the recency peak:

- **Append-only** `LESSONS.md` / `logs/TOKEN-LOG.md`; **immutable** ADRs / handoffs /
  transcripts / audits (supersede, never edit in place). JOURNAL corrections are NEW
  entries. Synthetic-proof `2099-*` PRs are intentional — leave them.
- **Layer 2 never executes** — read-only validators only.
- **No leftovers** — clean up and verify removal of anything you create.
- **OneDrive - Blue Yonder** — never write to or delete inside it.

===== FILE: 05_NOW — end =====
