===== FILE: 04_RECENT — start =====

# 04 · What just happened

A narrative of recent work on `.dev-knowledge`, written so a chat with zero prior
context can pick up the thread. Prose, not a log dump.

## The arc

The deepest "what happened" across this arc is not a commit — it is that
`.dev-knowledge` finished **changing identity**, from personal methodology notes into
the ecosystem's methodology brain (Guardian / Author / Auditor / Disseminator). Almost
everything below is that mandate made concrete. The building phase has **essentially
converged**: the subsystems are built and running; what remains on the board is
overwhelmingly *codify / harden / decide-rollout*, not net-new construction. The
present is less "mid-build" and more "a mature system at a decision point."

The dominant recent thread is the **child-methodology-floor** (ADR-78, #121). The
shape: a generator (`scripts/generate_floor.py`) emits a per-child `.claude/CLAUDE-FLOOR.md`
(≤1,500 tokens) + a `.sha256` sidecar, referenced from the child's `CLAUDE.md` via an
`@.claude/CLAUDE-FLOOR.md` import (verified empirically on CC 2.1.168), guarded on
both sides (a child pre-commit hash hook + the hub's `audit.py floor_integrity`). It
went generator → pilot in corp-sca-time-automation (#121 closed, three close-gate
witnesses recorded in `docs/audits/2026-06-08-floor-pilot-...`) → a `.claude/`
placement corrective (#137 closed, `011d304`) → two install-note fix-forwards
(docstring quotes, then ASCII/cp1252 console safety) → a from-scratch
`.pre-commit-config.yaml` robustness fix (today's tip, `e6154d3`): step 3 of the
install note now emits a complete top-level `repos:` envelope and branches
create-if-absent vs append, with 3 new tests. A full end-to-end re-pilot against a
**disposable** temp repo ran at **zero correction rounds** (8 gates PASS, hub
untouched). The honest verdict, forced by the operator over several rounds: the floor's
**value is thin and prospective** — it is team-infrastructure built for a team that
does not yet exist. It is shelved-as-ready; #138 (gitignore-negation fix) is open;
#131 carries the rollout requirements.

Surrounding the floor, several arcs landed just before. **Waves A/B** wired
`audit.py` as the sole local committer of its own baselines under the **ADR-80
two-tier automation doctrine** (#84/#125/#114/#115/#98/#8) — a post-ship witness
caught three real bugs including a silent gate bypass. **Native worktrees** landed
(#107) with the load-bearing `.worktreeinclude`, born from a witnessed shared-HEAD
collision and the rule "read-only parallel means ZERO commits." **ARCHITECTURE.md was
rewritten** (#91) into a six-chapter navigation map — and was net-*negative* in lines
(a first), because the diagram-form 5-rule algorithm demoted seven of eight Mermaid
diagrams to tables/text. The **backlog had its first-ever net decrease** (#134, 78→67):
done-undetected closures (#81 conformance workflow, #14 ecosystem substrate), merges,
stale removals. A real **audit program** ran (peer-audit v2 of TSH copilot-collections;
platform-max + codex-max changelog audits; methodology-transfer + protocols-rot audits)
— these are why the backlog is shaped the way it is. Parallel doc/governance work over
the same days — ADR-76/77/78/79/80, the immutability guard, the billing-leak sentinel,
the changelog sentinel, /ship maturation — see JOURNAL for chronological detail if
load-bearing.

One road **not** taken worth inheriting: the Graphify pilot was **rejected** (#88)
when its pre-registered kill criteria failed — grep was 2.5–5.6× cheaper than 3,003
noisy graph nodes. The discipline: pre-register kill criteria and honor them.

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

The sender framed the present as **a mature system at a decision point** [inferred].
Hard tree state: both the hub and corp-sca clean, on main, in sync with origin; hub
HEAD `e6154d3`; no live feature branches; no CC task executing — the only thing
in-flight is this handoff itself [witnessed]. The **floor at rest**: closed and
proven, value judged thin/prospective; it physically lives at corp-sca's
`.claude/CLAUDE-FLOOR.md`, force-added because `.claude/` is gitignored there, hash
`4d268f32`, guard armed and witnessed [witnessed/inferred — cross-repo, see
cross-check]. **Fleet automation is live**: `fleet_health.py` (daily cross-repo
audit), `conformance-hub.js` (nightly Dynamic Workflow), `audit.py` (structural
validators + sole local committer of baselines), all on schedule under ADR-80; this
session's routine baselines tripped — and were correctly cleared by *pushing*, not by
spurious entries — the live Stop-hook backpressure [witnessed]. **Plugins/hooks**:
the tier1-lifecycle plugin is at **0.1.10**; `/ship` auto-deletes merged branches,
refuses to run from a worktree, and is wired to a PowerShell notification sound;
propagation of the recent plugin guards (0.1.7–0.1.10) to siblings is pending the next
rollout, not done [recall].

**One live wound** the sender flagged: the **CLAUDE.md §5 self-contradiction** — it
both mandates "never edit in place" for ADRs and needs a sanctioned append-only path —
still unresolved, owned by **#112** [recall]. Named small drifts: corp-sca's
`canonical_freshness` is FAILing (a restamp owed in the corp chat, not a floor
problem); `ENVIRONMENT.md`'s `~/.claude/` tree is stale (#71); TOKEN-LOG placement
undecided (#10) [witnessed/recall]. The **backlog snapshot is stale** — predates this
session's #137 close and #138 add — and wants a git re-sync (#134/#90) before anyone
acts on its counts [inferred].

## Load-bearing facts (cross-checked vs repo at Phase 2)

| Claim from sender | Repo fact | Phase-2 verdict | Verification command |
|---|---|---|---|
| Hub clean, on main, HEAD e6154d3 | HEAD `e6154d3`, tree clean (captured at Phase 1) | ✅ confirmed | `git rev-parse HEAD; git status --porcelain` |
| #137 closed | Closed via `011d304` "close #137"; not in active task list | ✅ confirmed | `git log --oneline --grep="#137"` |
| #138 open | Present as an active P2 task | ✅ confirmed | `grep -n "#138" BACKLOG.md` |
| #131 carries the rollout requirements | #131 = repo-onboarding runbook, 6 layers + re-pilot findings (a)-(d) | ✅ confirmed | `grep -n "#131" BACKLOG.md` |
| tier1-lifecycle plugin at 0.1.10 | `"version": "0.1.10"` | ✅ confirmed | `grep version plugins/tier1-lifecycle/.claude-plugin/plugin.json` |
| ARCHITECTURE re-read, last_reviewed 2026-06-08 | `last_reviewed: 2026-06-08` | ✅ confirmed | `grep last_reviewed ARCHITECTURE.md` |
| Backlog "around 66" | **67** active tasks (#134 groom 78→67) | ⚠️ minor — 67 not 66 (sender hedged as stale) | `grep -cE "^- \[#[0-9]+\]" BACKLOG.md` |
| "Eighty-plus ADRs" | Highest = **ADR-80**; 53 ADR files on disk | ⚠️ loose phrasing — reach real, count loose | `ls docs/decisions/ADR-*.md \| wc -l` |
| CLAUDE.md §5 self-contradiction, owned by #112 | #112 active; its Done-when names "de-contradict CLAUDE.md §5" | ✅ confirmed (the contradiction is a live, owned item) | `grep -n "#112" BACKLOG.md` |
| corp-sca floor hash 4d268f32; AI Council ~310 tests | cross-repo (corp-sca, ai-council) | 🔵 sender-reported — out of ADR-41 scope to verify from hub | (verify in the target repo's own session) |

## Decisions & reasoning to carry forward

- **The operator's frame: maximize the methodology BEFORE fleet rollout.** That
  selects the cheap codification cluster (#135 diagram-form algorithm, #136
  pruning-symmetry, #34 pre-emit checklist + 4 postures) as pre-rollout, highest-leverage
  work [recall]. *So what:* you are about to propagate the standard — an uncodified
  rule does not propagate, and this session's friction (wrong model, omitted Done-when)
  is the proof the checklist is overdue.
- **On agents/heterogeneous review — shape, not count** [inferred]. The peer-audit
  settled that a large gated-worker roster is safe only because a team staffs the
  gates; **headcount parity is an anti-goal for a solo operator.** The substitute is
  adversarial blind-vote (Council) + a *heterogeneous* second reader. **Codex matters
  precisely because it is a different vendor** — same-model self-review collapses to
  sycophantic agreement (~58% convergence, ~24% unanimous-wrong by round 3). Chase
  cross-vendor heterogeneity and native-first, not TSH's headcount.
- **The governance enterprise risks generating more governance than it consumes**
  [inferred]. 67 items, heavily P3, many "evaluate native X" / "codify Y" —
  meta-work can outpace object-work. The floor was one instance of a broader trap.
  *Discipline:* spend on the methodology only where a real gap or contradiction would
  otherwise propagate; resist the rest.
- **What worked** [inferred]: the audit-driven posture (audits surfaced real gaps +
  real native capabilities we'd otherwise rebuild); codify-into-the-mechanism (when
  lessons went into the generator's *output* rather than into heads, the clean pass
  came for free); the two-tier discipline letting routines commit their own baselines
  without trampling the operator's tree.
- **What didn't** [witnessed/inferred]: build-ahead-of-need (the floor's friction was
  team-infra for a team that doesn't exist — buildable-and-provable ≠ worth-building-now);
  easy-metric closure (the operator had to force the value reckoning three times); a
  high error rate is a signal (when fixes keep finding fixes, the machinery is heavier
  than the problem); the executing CC session's *witnessed* report beats the architect's
  inference (twice the hub insisted the floor was at root while its own audit disproved it).

===== FILE: 04_RECENT — end =====
