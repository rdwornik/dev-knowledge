# LANE I — ADOPTION PREFLIGHT (NB7-D′, LOCAL) — READ-ONLY, ITEMS NAMED

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | medium |

**Why this exists:** NB7-D was dispatched to cloud and produced no ref and no commit — its
absence was undetectable. This rerun is LOCAL, and per ruling A8 it opens with a committed
dispatch-stamp so "dispatched-and-died vs never-dispatched" can never be ambiguous again. Its
predecessor also died unnamed — so every item is NAMED below; do all of them or record BLOCKED
per item, never silently skip.
**ADR-110 + dispatch-stamp (STEP 0):** save this prompt as
`docs/audits/2026-08-18-technical-adoption-preflight-lane-contract.md`, COMMIT first — that
commit IS the stamp.

## ITEMS (CLEAR/BLOCKED line each — no adoptions, no verdicts, measurements only)
1. **lychee (link checker) trial.** Acquire EPHEMERALLY only (existing binary, scoop shim, or a
   downloaded release binary run from the worktree — never a persistent system-wide install; if
   no acquisition channel exists on this box, record BLOCKED with the exact wall). Run over the
   repo's markdown link surface; record: broken-link count, total links, runtime, false-positive
   sample (5 links hand-checked). Library-first note: lychee IS the library — no hand-rolled
   link checker under any circumstances.
2. **Intake #31 §D residue.** Read §D verbatim; diff its demands against the Phase-0 baselines
   artifact (`docs/audits/2026-08-18-technical-phase0-baselines.md`). Execute whatever §D names
   that T0.5 did not cover, or record "no residue" with the quote proving it.
3. **`gh` CLI formalization readiness.** Verify the (e)-substitute claim: nothing blocks it and
   it is one ledger line in intake #27 — quote the intake location where the line would land.
4. **Tier-S home absence.** Confirm (grep) that no Tier-S ledger surface exists anywhere
   (`ponytail`/`skill-creator` have never been tried) — the R13 premise, re-verified live.

## OUTPUT
One artifact: `docs/audits/2026-08-18-census-adoption-preflight.md` — per-item CLEAR/BLOCKED
line + measurements + exact commands verbatim. Regen the audits index via its generator.
`COMMIT` after STEP 0 (stamp) and once per completed item-pair.

## FINAL
Commit-and-STOP. STOP packet: 4 CLEAR/BLOCKED lines · lychee numbers or wall · shas.
**No adoption verdicts, no rows, no BACKLOG/tasks writes, no persistent installs, no merge.**
