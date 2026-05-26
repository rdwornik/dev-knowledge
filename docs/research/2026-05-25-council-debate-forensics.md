# Council Debate Forensics 2026-05-25

> **Type:** Operational forensics — diagnose state of the async Council run started during the prior turn.
> **Status:** Diagnosis complete. The run did start and is producing correctly-routed transcripts. Operator's "did not run" report was a premature check (debates take ~5 min each; first inbox transcript landed ~14:28).
> **Premise correction:** the prior prompt's worry ("debate did not run / no transcripts") is contradicted by evidence — Q1 already landed in `.dev-knowledge`. The run is healthy, not dead.

## Process state

Two `python.exe` processes alive at forensics time:
- PID **21944** (~130 MB RSS) — the active Council `--inbox` run (started prior turn, background ID `b9fjsb20o`).
- PID 28236 (~4 MB) — small/idle; not the debate run.

The debate process is **alive and progressing**, not hung. Run log shows continuous API activity (round 1 → round 2 → synthesis per question) with no error stalls.

## ai-council/output/ contents (today)

| File | Meaning |
|------|---------|
| `_inbox-run-20260526.log` | full stdout/stderr capture of the run |
| `council-out-20260526_142316-pick-handoff-methodology-council-preparation-2026-05-25.md` (+ `_metrics.json`) | **stray** debate — see below |
| `council-out-20260526_142806-pick-2026-05-25-handoff-council-Q1-internalization-assurance.md` (+ `_metrics.json`) | Q1 transcript (canonical copy) |

## .dev-knowledge transcripts existing (today)

- `council-out-20260526_142806-pick-2026-05-25-handoff-council-Q1-internalization-assurance.md` (91,600 bytes) — **Q1 mirrored successfully via `target-project` routing.** Confirms Q5-of-discovery (ADR-43 routing) works end-to-end.

## council_inbox state

- **Still queued (`council_inbox/*.md`):** Q2-bundle-content-composition, Q3-procedural-competence-transfer, Q4-sender-verification-symmetry, Q5-delivery-custody-abstraction.
- **Archived today (`council_inbox/archive/`):**
  - `2026-05-26T1423_handoff-methodology-council-preparation-2026-05-25.md` (the stray Downloads file)
  - `2026-05-26T1428_2026-05-25-handoff-council-Q1-internalization-assurance.md` (Q1, processed)

Archive happens *after* a debate's transcript is written + mirrored (`cli.py:510`), so "archived" ⟹ "transcript complete." Q2 is currently being debated (still in inbox; archives on completion).

## The stray Downloads debate (incidental finding)

`council --inbox` also scans `~/Downloads/*.md` (ARCHITECTURE.md:211-216; `cli.py:410-417`, `all_files = dl_files + files`). A leftover file `~/Downloads/handoff-methodology-council-preparation-2026-05-25.md` (content: the *previous* session's "Council Question Preparation" prompt) carried council frontmatter keys, so it was auto-detected and debated **first**, before the 5 inbox files. It:
- produced a transcript in `output/` only — it had **no `target-project`**, so it did **not** mirror to `.dev-knowledge` (correct behavior),
- cost ~$0.53 (one extra debate), and
- is now archived.

Impact: harmless (no pollution of `.dev-knowledge`), but it explains (a) the ~5 min delay before Q1 even started and (b) why an operator scanning early would have seen activity but no `.dev-knowledge` transcript yet. **Follow-up for operator:** the Downloads auto-scan will keep re-detecting any council-keyed `.md` left in `~/Downloads`; that file is now archived out of Downloads, so it won't recur.

## Diagnosis

Matches hypothesis **"Async process still running, just slow"** + **"partially completed"** from the recovery table. NOT dead, NOT never-started, NOT transcripts-elsewhere. Q1 complete and correctly landed; Q2-Q5 pending under the still-running process.

## Recovery action selected

**Shepherd the existing healthy run to completion — do not kill/re-run.**

Rationale (objective-hierarchy driven):
- Objective #1 (5 transcripts present) is best served by letting the working, correctly-routing process finish; it is already past Q1 and into Q2.
- Killing it to re-invoke synchronously would discard in-flight Q2 work + re-spend cost, with no reliability gain (same mechanism, same ~5 min/debate).
- Launching a second `council --inbox` is explicitly avoided: both processes would race on the same `council_inbox/*.md` set (double-processing / archive conflicts).
- "Not waiting blind" is satisfied by actively monitoring to completion within this session (poll until `council_inbox` drained), then verifying each transcript and committing — rather than ending the turn with an unresolved background job.

Fallback: if the process dies before draining the inbox, re-run **only the still-queued files** synchronously with full logging (they remain in `council_inbox/`, so a plain `--inbox` re-run would resume exactly the unprocessed set).
