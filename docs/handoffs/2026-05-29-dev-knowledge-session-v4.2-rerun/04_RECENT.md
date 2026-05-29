# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread.

## The arc

This is the closing chapter of a multi-day **ecosystem universalization +
handoff-redesign arc** (≈2026-05-26 → 2026-05-29). The handoff process itself was
the through-line:

- **v3.4 → v4 redesign.** The old handoff process (13–14 hand-maintained files,
  multi-stage, placeholder dance, JSON manifest) was diagnosed as **multi-surface
  fragility**: patching its bug list left the next bug list inevitable. A v3.4 real
  run was *aborted* mid-flight; an empirical process audit returned 13 findings
  (`docs/audits/2026-05-29-handoff-v3.4-process-audit.md`), all fixed via Path C
  (append-only amendments to six ADRs — 42/45/55/56/57/58). v4 then **collapsed the
  surfaces by design**: 8 files (README + `01`–`07`), two phases, **generated from
  source**, a **sage→apprentice** interview frame, and an operator escalation ladder.
- **v4.0 → v4.1 fix.** The first Phase 1 invocation surfaced two *implementation*
  defects (not architectural): a unilaterally-introduced `_scratch/` folder (reverted
  to the existing `in-progress/<slug>/` convention) and a two-cluster interview whose
  methodology cluster duplicated PLAYBOOK/ESSENTIALS (collapsed to the single
  sage→apprentice cluster).
- **v4.1 first real run.** Handed off *this very session* end-to-end: Phase 1
  interview → operator answers → Phase 2 consolidation → bundle at
  `docs/handoffs/2026-05-29-dev-knowledge-session/`, merged to `main` (merge
  `93b7b1c`). **Phase 2 verification caught two drifts** in the sender's claims — the
  v4 architecture's central virtue working as designed.
- **v4.2 refinements (tonight).** A deep review of the v4.1 bundle found **7
  refinement-level issues, no architectural defects — the design is sound.** They
  were implemented on the current branch (6 commits, `a333265` → `3ae2b6b`, baseline
  green throughout): four-tag sage discipline; always-emit verification table in
  `04_RECENT`; README drift section moved up; version+status stamp; bundle-maintenance
  section; `05_NOW` forced-ranking warning; Codex clarity sentence; and the
  "handoff is back-and-forth" rule promoted from handoff-specific to general PLAYBOOK
  methodology. **This bundle is the v4.2 re-test** — the proof-of-improvement run.

Parallel waves over the same days (recall — verify via git log if load-bearing):
ADR-59 visual pattern + ADR-60 docs taxonomy + ADR-61 git-worktree codification;
four Mermaid process diagrams + AI Council CLI v1.0 + `protocols/AI_COUNCIL_PROCESS.md`
(343 lines); Mermaid dark-theme v1→v2 (audit.py check #7, health 6/6 → 7/7);
cross-repo cleanup (~73 merged branches) + a 22-finding overnight ecosystem audit
(`docs/audits/2026-05-29-ecosystem-coherence-audit.md`).

## What the sender chat said (interview, four-tag tagged)

The sage tagged every claim. The dominant **wisdom**: when audit findings *cluster*,
the cluster is the diagnosis — patching the bug list misses the disease (this drove
v4). And **hard-metric closure over easy-metric**: "all tests green" missed the 7
refinement issues that a hard review caught; easy-metric closure is the recurring
failure mode of LLM work.

The dominant **structural warning** is **ML-2 — the un-enforced-guard pattern**: this
repo authors conventions strongly but enforces them weakly, which is ironic given its
VISION names "drift detected proactively" (12 of 22 ecosystem findings were
doc-truth drift). Until enforcement infrastructure lands (audit.py check #8,
sacred-files check, eval suite, an agent layer that pre-checks prompts), every new
advisory guard is a future bug source.

The strongest **operator signal**: an **agent-framework gap** — Rob's own words,
*"musimy zbudować agent framework … żebym nie musiał po prostu powtarzać."* Weight
this highly; it is the enforcement-layer need in different language.

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Verdict | Verification command |
|---|---|---|---|
| v4.2 branch tip `3ae2b6b` NOT merged to main | main tip = `93b7b1c` (the v4.1 merge); `3ae2b6b` only on the feature branch | ✅ matches | `git branch --contains 3ae2b6b` |
| 6 v4.2 commits `a333265`→`3ae2b6b`, baseline green | confirmed | ✅ matches | `git log --oneline main..HEAD` |
| spec at 395 lines vs ≤350 budget | `HANDOFF_PROCESS.md` = 395 lines | ✅ matches | `(Get-Content protocols/HANDOFF_PROCESS.md).Count` |
| LESSONS.md ~4 days stale (last 2026-05-25) | last commit `e6dfca1`, 2026-05-25 | ✅ matches | `git log -1 --format='%ai' LESSONS.md` |
| aborted-handoff folder deleted in `987edac` | confirmed, 475 deletions ("delete aborted handoffs folder") | ✅ matches | `git show 987edac --stat` |
| v4.1 first-run bundle preserved (8 files) | present, untouched | ✅ matches | `ls docs/handoffs/2026-05-29-dev-knowledge-session/` |
| corp-monorepo CM-1 branch unmerged at `a1007b1` | `chore/extract-p1-2-to-backlog-2026-05-28` @ `a1007b1`, only on that branch | ✅ matches (cross-repo, ADR-41: surface only) | `git -C ../corp-monorepo branch --contains a1007b1` |
| §3.1 three-tag vs Amendment A four-tag supersedence | spec body §3.1 = 3 tags; Amendment A = 4 tags; skill enforces 4 | ✅ matches | read `protocols/HANDOFF_PROCESS.md` |
| `.ecosystem/` registry exists (dot-prefixed) | registry is `ecosystem/<repo>/state.yaml` (**no** dot); `.ecosystem/` absent | ⚠️ **drift** (sender tagged `unknown`) | `ls ecosystem/` |

All load-bearing claims verified except the `.ecosystem/` path, which the sender
correctly flagged `unknown` — the four-tag discipline did its job upstream.

## Decisions & reasoning to carry forward

- **v4/v4.2 implemented WITHOUT an ADR** — intentional. Architecture decisions go
  through AI Council; it was deferred this session due to operator fatigue. v4 + v4.2
  ratify **together** as one architectural decision (P2 BACKLOG). If you modify v4
  substantively, the ratification gap compounds.
- **Spec budget tension accepted:** ADR-39 append-only beat the soft ≤350 budget
  (now 395). The decision: accept growth via amendments, consolidate at a future
  major version (v5) through Council.
- **Recursion worth seeing:** the v4.1 → v4.2 cycle is the methodology operating on
  itself — use → review → refine → re-validate. That's the model for handling defects
  you find: don't paper over, iterate the process to eliminate the class.
