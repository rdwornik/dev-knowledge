# PLAN — wave 5 and the handoff: one file so nothing is lost

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN`. Source: `to-cc/PLAN-WAVE5-2026-09-23.md`. Status line from the source:
> "MASTER PLAN — the single source for waves 5a / 5b / 5c and the handoff. Every order of this
> window defers to it." This lane (LANE-5A-5) is wave 5a merge-priority item 9 in §3's table.
> Carrier: this record itself is the plan LANE-5A-5's own frozen contract cites as required
> reading; no defect row separately carries it.

carried-by: OPEN
lands-via: LANE-5A-5 commits it verbatim under docs/audits/ (date-slug) as the wave-5 plan record; the repaired handoff boot points to it
date: 2026-09-23
from: 2026-09-19-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)
status: MASTER PLAN — the single source for waves 5a / 5b / 5c and the handoff. Every order of this window defers to it.

## 1. Doctrine (operator rulings, in force)

- **The backbone is code.** Scripts, hooks, gates and data carry the process. Prose states intent and
  checks against the code; it never triggers the process.
- **The PLAYBOOK is human documentation, never an authority for Claude** (O-5). Commands come from
  `scripts/dispatch.py launch --help`; routing from `ecosystem/provider-registry.yaml`; rules from
  `STANDING_RULINGS`.
- **Decisions, audits and operator requests land in the repo** — as rows, rulings and records.
  The transport is a courier, not a store.
- **Nobody waits for the operator at night.** Rulings are pre-authorized. A lane decides by its
  contract's Value line and records the decision.
- **Routing by role:**

  | Role | Served by |
  |---|---|
  | orchestrate / dispatch / integrate | Opus |
  | bounded produce | Sonnet; Copilot once admitted |
  | code review | Codex terra |
  | independent verification | Codex sol |
  | long reads (over 50 KB) | Gemini via agy |
  | lookups | Haiku |
  | debate | Claude vs Codex Astra, via `codex exec` rounds |

  Record the model that actually served each step.

## 2. What the seven reviews of 2026-09-23 established

1. **VERIFY-TIME:**
   - merge median 93-98 min;
   - the local compare takes 28-59 min;
   - prose edits pull in 58 test files;
   - CI runs the full suite in about 8 min but is 20/20 red against a stale baseline.
2. **S2 hooks:**
   - the 09-25 verdict is unsafe: its counters die with the worktree;
   - start hooks take 7-16 s in real sessions; one end-of-turn hook times out and nothing reads it;
   - 6 of 11 hooks break the read/trigger rule;
   - the banner lies.
3. **S1:** the router exists and gates admission; the launcher bypasses it. Copilot's admission is
   not in the registry. Opus 5.5 is served under the `opus` alias while the registry pins an older
   Opus. Three tool changes to adopt: `/skill-doctor`, `/doctor` trim, `omitClaudeMd`.
4. **ENV:** the two globals are set. There are no hard-coded Drive paths in code — 119 read sites
   read the variable, each on its own. One report was written to the wrong folder.
5. **S3:**
   - the handoff is not ready: P9 (10 backlog hard-fails) and P11 (37 OPEN decision files) fail;
   - the paste is 35 KB against a 20 KB WARN-only ceiling;
   - 10 stale statements;
   - 10 operator requests without a row;
   - organ census: 78 called, 80 unobserved, 17 unreachable; 23 organs at moments, 166 nowhere.
6. **CROSSCHECK:** 11 of 16 claims confirmed. **The per-batch registry launders regressions:** CI
   regressions rose from 9 to 17 while local said clean. Fix test selection first; CI replaces the
   local compare only after an honest baseline.
7. **ADR-121 (Proposed):**
   - the state problem is authority and identity, not storage;
   - a single-writer event log on the orphan ref `harness-state`, with per-lane outbox refs;
   - a throw-away SQLite projection that fails closed;
   - every verdict names its baseline id;
   - scores 409 vs files+schema 390 (the fallback);
   - git: adopt trailers + a commit-msg hook, CAS ref updates, bisect run; refuse `merge=union` and
     notes;
   - compute: a persistent Linux VM, 16 vCPU / 64 GB, running the devcontainer, plus Actions large
     runners after the baseline;
   - ai-council ran from its front door; rebuild the debate organ on the router.

**One diagnosis behind all seven:**
- no single choke point;
- two sources of truth;
- built but never called;
- prose routing ignored;
- a quality cost: laundered regressions.

The cure is single writers, single entry points and identities — ADR-121 at the root.

## 3. Wave 5a — tonight (orders: BATCH-WAVE5A v2, INTEGRATOR-WAVE5A v2, BATCH-NIGHT-READONLY)

| Merge priority | Worktree | Contract | Purpose |
|---|---|---|---|
| 1 | lane-memory-gate | LANE-5A-3 | heavy runs wait for memory; `-n` computed from free memory |
| 2 | lane-test-selection | LANE-5A-2 | prose no longer pulls in 58 files; MERGE-RECEIPTS mapped |
| 3 | lane-hooks-urgent | LANE-5A-7 | counters survive teardown; the 09-24 and 09-25 deadlines; banner; hook statements |
| 4 | lane-provider-registry | LANE-5A-8 | Copilot admitted with in-repo evidence; Opus 5.5 rates; roles as data |
| 5 | branch worktree-postwave-changelog @66a616a9 | (S1) | changelog review, tool versions |
| 6 | branch worktree-lane-adr-state-store @48c0cdc2 | (ADR) | ADR-121 Proposed; treat as code |
| 7 | lane-handback-fixes | LANE-5A-4 | one comparator; no path collisions; seat live on bind; plan-lint fate rule |
| 8 | lane-ci-verdict | LANE-5A-6 | CI verdict organ, recorded beside the local one |
| 9 | lane-landing-window | LANE-5A-5 | rows, rulings, audits and markers; P9/P11 pass |
| 10 | lane-handoff-repair | LANE-5A-9 | paste gate at 20 KB; no PLAYBOOK authority; 4 seats; templates |
| 11 | lane-one-registry-ci | LANE-5A-1 | ADR-121 step 1: attributed reds and a baseline id on every verdict |
| 12 | lane-graph-stage-edge | LANE-5A-10 | Copilot-produced: the missing stage-to-script graph edge |

Plus a read-only session covering: the organ triage (wire or retire, with Codex sol re-checking
every RETIRE), the self-proposals (containerization, transport contract), and measurements
(`/skill-doctor`, `/doctor`, the Opus 4.8-vs-5.5 A/B).

**Night goals:**

| # | Goal |
|---|---|
| N1 | at least 9 of 12 merges by morning |
| N2 | 0 operator inputs overnight |
| N3 | median merge after lane-test-selection at most 45 min |
| N4 | 0 lanes lost to memory after the memory gate |
| N5 | 09-24 and 09-25 defused before 06:00 |
| N6 | P9 and P11 pass |
| N7 | paste gate test green |
| N8 | at least 1 Copilot-produced lane, or a recorded SUBSTITUTION |
| N9 | CI-vs-local agreement reported |
| N10 | every red above the 09-17 freeze attributed to a sha |

**Not tonight:** no new ADR files (the hook-taxonomy ADR is 5b), no hook re-arming, no settings,
rulesets or global config, no bundle cut.

## 4. Operator decisions owed (morning)

1. **ADR-121:** ratify its direction, with the pilot thresholds and the files fallback.
2. **Debate question D1:** may a seat act on state that is saved locally but not pushed?
   Architect's recommendation: accept the draft — no across seats, yes only inside the
   integrator's own step.
3. **Compute:** buy the VM (16 vCPU / 64 GB); a GitHub Team plan for the large runners.
4. **ai-council:** retire it, or keep it as a pattern source.
5. **Opus 5.5** for orchestrate/plan, on the A/B numbers.
6. **The handoff shed** (35 to 11-13 KB): treated as accepted from "fix the whole handoff"; confirm.
7. **The organ retire list** from the triage — GO per item.
8. **Any OPERATOR-ACTION line** a lane leaves — for example, the 09-24 expiry if it lives in global
   config.
9. **Required checks on,** after the baseline is honest and the commit-gate is diff-scoped.

## 5. Handoff (after the night, on the operator's GO)

- The repaired tooling cuts a paste of at most 20 KB. The boot points to where things live:
  - this plan;
  - the ledger;
  - the templates (dispatcher, integrator, batch common rules, lane contract);
  - the registry;
  - `dispatch.py --help`.
- The RESIDUAL is the OPEN list.
- Four seats are named: architect, dispatcher, integrator, lane.

## 6. Wave 5b — next window

1. **ADR-121 step 2:**
   - single-writer event log;
   - lane outbox refs;
   - the integrator library;
   - the merge path as code, built on events;
   - a trailers commit-msg hook (the CONTRIBUTING convention as data);
   - a fault test for the pre-push fallback.
2. **Launcher to router:** explicit model ids; contracts name roles; plan lint refuses model names
   and requires prior-art evidence for a new organ.
3. **Hook target design:** the eight S2 rows plus the hook-taxonomy ADR — one read-only start entry,
   one trigger-only end-of-turn entry.
4. **Path layer and transport adapter** (Drive API or rclone), with schema enforcement; 0 direct
   variable reads outside the module.
5. **Organ triage executed** (wire or retire, with GO): the harness **shrinks**.
6. **Debate organ on the router,** keeping ai-council's three patterns.
7. **Front-door conformance check** for every fleet repo — README, run instructions, headless use,
   no stale pointers.
8. **Commit-gate diff-scoped,** then required checks, with GO.
9. **Gated learning loop:** incident, then mechanism, then a regression test, on the event log.
10. **Tooling:**
    - `/changelog-review` scheduled weekly;
    - `omitClaudeMd` for bounded roles;
    - skills pruned by `/skill-doctor`;
    - an O-5 check that no file cites the PLAYBOOK as an authority.
11. **Night-autonomy mechanisms:** liveness watchdog, session janitor, deny-and-point guard.

## 7. Wave 5c

- **VM pilot:**
  - `devcontainer up`;
  - the full suite at `-n 16` in under 4 min;
  - one lane end to end;
  - laptop memory about 0.
- Actions large runners.
- Copilot lanes routed by the table.
- The SQLite projection.
- At least 50 % of night lanes off-box.

## 8. Finish line

**One real monorepo feature through the loop,** row to merge, on the VM, with operator touches =
task + GO (O-2b). BUILD MODE then exits by O-2a, O-2b and O-2d.
