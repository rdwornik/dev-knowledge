===== FILE: 04_RECENT — start =====

# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread. Prose, not a log dump.

## The arc

Read this arc as the story of the **working method**, not a list of events (events live
in `JOURNAL.md`; per-learning rules live in `LESSONS.md`). The disease this whole arc
fought is **prose-vs-state drift** — the gap between what a document *narrates* and what
the repo *is*. Every failure across the last week was one instance of it: a nightly run
whose counts existed only as narration; living docs claiming commands that had been
archived; a JOURNAL entry that generalized one repo's fact to another; fixtures
hand-written instead of generated from the real shape.

The arc's real output is that the methodology now has **organs** against that disease,
each proven in production at least once. **Contract guarantees were moved onto the
executing path:** the nightly conformance digest now computes its counts in code, carries
them in a machine-readable marker, and the consuming parser reads only the marker and
fails *closed* (commits `70e1e9b`, `c3024e9`, `821ef02` — the "nightly counts-contract"
session). The **escalation ladder** was codified in PLAYBOOK (conversational → formal
prompt → scoped Dynamic Workflow → AI Council; commit `11ef2d8`, closes #74), and
**Dynamic Workflows graduated from research topic to proven tier** — one hub pilot (#81,
the scoped methodology-conformance workflow, `28613f7`) plus one corp deep-audit (#75, 29
targets / ~588k tok / ~4 min, `bd3482e`), both running the verifier-fanout → adversarial
skeptic → READ-ONLY proposals → operator-ratification shape that is now the standard
verification pattern at every scale.

The **nightly conformance loop** (the immune system) proved its value the best possible
way: on corp-monorepo's first night it caught a real, week-old violation of the
sole-change-record rule that no human had noticed, and its skeptic correctly killed a
false positive in the *same* run. Cloud doctrine settled as **self-containment**: #86.2's
UNDERSTAND step verified that the private hub makes plugin/skill *and* URL-fetch all inert
in a clone-only cloud session, which **killed its own premise** — and that became
**ADR-72** (cloud Routines are hub-independent; commit `931034c`). The most recent days
were hardening and bookkeeping: the 2026-06-06 morning triage ratified the nightly digest
(N1 #74 clarification, N2 ARCHITECTURE re-read + ADR-72 add); corp's superior *code-owned*
digest renderer surfaced a backport candidate, and two of its guards (a leading
`gh auth status` gate, then a digest-existence guard that fixes a `gh api` 404-body-to-
stdout misread) were **backported into the hub's `surface_triage.ps1`** (`cfdcc31`,
`e9c9e6a`). A Routine display-name naming standard landed in PLAYBOOK (`bd5c5e9`), and the
CLAUDE.md §9 toc-hook drift was fixed (v2.15).

Parallel threads over the same days — external-research note landing + #84/#85/#86
dispositions, #81 pilot-finding application + archived-command sweep, plugin 0.1.3
consumer install, doc-debt staleness audit — see `JOURNAL.md` 2026-06-05/06 for
chronological detail if load-bearing.

What did NOT work, honestly: a wrong cross-repo claim entered JOURNAL unverified and
needed a **correction entry** (`6e29b24`); one scheduled hub night left no trace while the
panel implied otherwise — **closed by operator ruling, watched by the digest-presence
check, not explained** (do not reopen — see landmines); and the architect (the sage)
improvised process from memory twice (deferral creep; misstating where handoffs start) —
the operator's quality-counter caught it. The honest summary: the method's strength is now
less about any one session being right and more about **the loops that catch sessions
being wrong**.

## Four-tag discipline (canonical)

The sage tagged every claim using this discipline (canonical per HANDOFF_PROCESS
v4.3 Amendment A; supersedes the earlier three-tag body in spec §3.1):

- **witnessed** — sage just verified this OR saw it happen recently AND has no
  reason to think it changed since
- **recall** — sage remembers from earlier in the session; **state may have
  changed** — verify via CC inline if the claim is load-bearing
- **inferred** — reasoning from evidence (not direct knowledge)
- **unknown** — sage doesn't know — flagged explicitly

When you encounter `recall` or `unknown` on a load-bearing claim in this file,
verify via CC before acting on it. This is the "handoff is back-and-forth" rule
from PLAYBOOK methodology.

## What the sender chat said (interview)

The sender framed the session as adding organs against prose-vs-state drift, each proven
in production at least once [witnessed]. On the **present state of the organs**
[witnessed]: the nightly conformance routine is LIVE on both hub and corp (proven incl. a
real catch on corp); the fail-closed triage Action and SessionStart surfacing (+ the new
gh-auth gate and 404-guard) are live on both; the digest generator is **free-rendered on
the hub (weaker) but code-owned on corp (stronger)** — corp's renderer is the back-port
candidate, and proves child→hub propagation matters too. Orchestration lives in-repo on
the hub (it IS the template) and as an adapted in-repo copy on corp (per #86.3). Both
repos: clean trees, everything merged and pushed at capture.

On **gates and pendings** [witnessed]: #84 codification is **gated at n=1-of-2** real
runs — run 2 is corp's first *scheduled* night, whose digest dates **2026-06-07**; read
it, including whether the corp renderer emits a delta-vs-baseline section (currently
unproven). Hub bookkeeping is **owed**: record #86.3 (source: corp JOURNAL 2026-06-06),
close #86, log n=2. The branch+merge `--no-ff` rule is now universal (operator ruling),
including one-line doc edits. The freshness rule is in force: editing any freshness-gated
canonical doc obligates a genuine end-to-end re-read + same-day `last_reviewed` restamp —
both genuine re-reads this session found real drift, which is the point.

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| ADR-72 records cloud self-containment (#86.2 → Path A) | `docs/decisions/ADR-72-cloud-routine-hub-independence.md` exists; BACKLOG #86 sub-decision 2 records ADR-72 | ✅ confirmed | `ls docs/decisions/ADR-72*` ; `grep -n "ADR-72" BACKLOG.md` |
| #84 codification gated at n=1-of-2 (run 1 = corp scoped audit 2026-06-06) | BACKLOG #84 carries "run 1-of-2 recorded (corp scoped audit 2026-06-06, 29 targets / ~588k tok / ~4 min)" | ✅ confirmed | `grep -n "#84" BACKLOG.md` |
| #86 sub-decision 3 (R2 saved-workflow distribution) still open | BACKLOG #86: "Remaining: sub-decision 3 (R2 saved-workflow distribution ruling)" | ✅ confirmed | `grep -n "#86" BACKLOG.md` |
| 404-guard + gh-auth gate backported into hub `surface_triage.ps1` | Commits `e9c9e6a` (digest-existence guard), `cfdcc31` (gh auth gate) on `main` | ✅ confirmed | `git log --oneline -10 main` |
| Both trees clean, everything merged/pushed at capture | Hub working tree clean at HEAD `608f26b` (this branch is the handoff branch) | ✅ confirmed (hub) | `git status --porcelain` |
| #89 has a concrete check-source (~6 of 29 corp checks are binary, mechanizable) | BACKLOG #89 disposition note records exactly this | ✅ confirmed | `grep -n "#89" BACKLOG.md` |

**No drift detected** — every load-bearing sender claim matches repo state at Phase 2.
(corp-monorepo claims are cross-repo and were NOT independently re-verified here per the
ADR-36/41 read-only boundary; they are sourced to corp's JOURNAL 2026-06-06 and should be
confirmed in that repo if load-bearing for a decision.)

## Decisions & reasoning to carry forward

- **Falsification is a success mode.** The best moment of the session was a task
  *stopping*: #86.2's UNDERSTAND verified two facts that killed its own premise, and the
  session presented options instead of shipping dead machinery. Treat a triggered
  STOP-valve as the system working, not as a failure.
- **Skepticism pays where claims have interpretive room.** Skeptic kill-rates ran ~2/12
  on prose-heavy docs, 0/6 on binary existence checks, 1/2 on a mixed set — structural,
  not noise. That is the evidence base for **mechanizing existence checks
  deterministically (#89)** and reserving LLM verification for judgment-laden conformance.
- **The operator's ratification bandwidth is the scarcest resource.** Every organ funnels
  through generate → FILTER → ratify. When evaluating any new reviewer/routine/checker,
  the first question is what it adds to the operator's *morning*, not what it catches.
- **Accepted tensions beat hidden ones.** #86.3's per-repo orchestration copies
  contradict the ownership-cadence principle — accepted consciously because
  self-containment forces it, with a named mitigation (hub as canonical template,
  rollout-moment propagation in *both* directions). Don't relitigate it casually; do honor
  it via back-ports.
- **Evidence gates instead of confidence.** Rubrics get written from evidence, not memory:
  #84 stays gated until n=2 real runs (recommendation, marked as such).

===== FILE: 04_RECENT — end =====
