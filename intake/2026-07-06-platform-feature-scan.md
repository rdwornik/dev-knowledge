---
intake-id: 2
status: SEED
origin: operator ask + architect web research, 2026-07-06
consumed-by:
---

# INTAKE BRIEF — platform feature scan: buy-vs-build audit (Claude/CC, H1-2026 features)
Status: INTAKE-DRAFT (SEED → for functional-architect review, then technical triage) · Origin: operator ask + architect web research, 2026-07-06 · Sources: official CC what's-new/changelogs + release notes + Code-with-Claude-2026 coverage (verify each item against docs at build time — third-party writeups may drift).

## 1. Problem / motivation
The platform absorbed several patterns we hand-built (scheduled agents, multi-agent worktree orchestration, output-grading loops, live dashboards). Hand-rolled scaffolding that a native primitive now covers is rot surface — derive-don't-maintain applies to our OWN tooling. We need a deliberate buy-vs-build pass: adopt native where it replaces ceremony, keep our governance layer (boundaries, contracts, §14, closure discipline) where it is the actual value-add.

## 2. Scenarios (+1 view)
- As the operator I schedule the nightly loop natively (Routines) instead of a fragile Task-Scheduler harness, and read a triaged morning digest.
- As the root architect I see every lane on ONE screen (claude agents): running / blocked-on-me / done — no more orphan-process archaeology.
- As the root I attach a grading rubric (Outcomes) derived from an epic's done-contract, and an independent grader scores the EPIC RETURN before I spend attention on it.
- As a lane, permission needs surface in-session instead of silently dying (the sandbox permission-wall class).

## 3. Requirements — triaged (must=ADOPT now · should=PILOT one real use · could=WATCH)
**MUST (zero/low cost, direct pain hits):**
- `claude agents` view — adopt as the standard root cockpit (yesterday's agent-cleanup pain). 
- `/usage` breakdown (per skill/subagent/plugin/MCP) — wire into cost awareness; complements per-lane attribution.
- Background-subagent permission prompts surfacing in main session — confirm behavior on our sandbox children; may retire part of the G-batch workarounds (VERIFY, don't assume).
- `/less-permission-prompts` — run it, diff its proposed allowlist against our hand-built ARC_ALLOW_RULES; adopt as allowlist-maintenance tooling.
- Sonnet 5 as CC default (native 1M context; promo $2/$10 through Aug 31; needs ≥2.1.197 — we're on 2.1.200): refresh PLAYBOOK's model-selection table AND the three pinned organs the 07-06 changelog review located exactly — `.claude/agents/artifact-reader.md:8`, `.claude/workflows/conformance-hub.js:150-152` (V1/V2/V3 verifier pins), `.claude/settings.json:73` prose. GATED on V1: run `claude --model claude-sonnet-4-6 -p "ok" --debug 2>&1 | grep -i "deprecat\|updated to"` first — a deprecation warn makes this mandatory, not optional.
- **DECIDE (pending since 06-15, zero build cost): Fable 5 in the t-shirt routing doctrine** (ARCHITECTURE Appendix B / ADR-70: S=Haiku M=Sonnet L=Opus — Fable absent despite GA + the auto-mode Opus→Fable fallback). The operator now has weeks of empirical Fable-5 use (this very architect session ran on it) — decide its tier or its explicit exclusion; note ADR-80's no-fallbackModel-on-pinned-stages rule governs a different mechanism, state that to avoid conflation.
- `/recap` + `/rewind`-past-`/clear` — session hygiene, free.

**SHOULD (pilot on one real workload before doctrine):**
- **Routines (CC on the web: scheduled/templated cloud agents)** — CORRECTION from the 07-06 in-repo review: a cloud-night Routine ALREADY EXISTS (#86 cloud-night envelope, nightly conformance run producing PRs/digests). The pilot is therefore EXTEND-not-create: (a) add the Epic-5 full-serial test suite + timing trend as a second routine under the same envelope discipline; (b) adopt the review's A2 — native auto-mode safety nets (2.1.178 pre-launch subagent classification, 2.1.183 destructive-git blocks, 2.1.193 classifyAllShell) as a complementary layer on #86; reinforces core-invariant #3, does not replace it.
- **Outcomes (rubric + independent grader)** — pilot on ONE epic: rubric = the epic's done-contract; grader independence maps to our Codex-heterogeneity doctrine. If it works, EPIC RETURNs arrive pre-graded.
- **/batch + managed multi-agent orchestration + nested subagents + scoped per-agent permissions** — depth: 5 levels per the repo's own 06-15 review of 2.1.172 (third-party coverage said 3 — trust the in-repo review); nested-subagent workflows are ALREADY IN USE (conformance-hub fan-out). Overlaps ADR-97 mechanics (worktree spawning, decomposition). Pilot question: can /batch run UNDER our governance (file-boundaries, commit-and-STOP, root-only merge) — if yes, it replaces hand-provisioning; if it insists on its own PR flow, keep ours.
- **Ultraplan** (cloud plan drafting + web review + remote/local run) — pilot as the plan-first surface for one L-sized epic; maps to our plan-review gate with better UX.
- **/goal** (work-until-condition-holds) — pilot inside one lane with the done-contract as the condition; guard: condition must be mechanically checkable, not self-asserted (our closure doctrine).
- **Artifacts in Claude Code** (live shareable pages: dashboards, walkthroughs) — pilot as the Tier-4 human visualization surface; candidate consumer for #264 (mermaid_emit wiring) and the operator's dashboard want.

**COULD (watch, don't move):**
- Dreaming (platform scheduled memory review) — overlaps our nightly proposal loop; re-evaluate AFTER our loop's survival metrics exist (don't buy before knowing what we need).
- Agent checkpointing / multi-repo orchestration (beta per third-party coverage — verify against official docs; schemas may change) — relevant to P6 fleet roll later.
- /team-onboarding (replayable setup guide) — compare with consumer-onboarding-runbook at fleet-roll time; likely ours wins (methodology-specific).
- fallbackModel chains, per-agent budget caps — nice-to-have hardening for lanes.

## 4. Acceptance criteria (for the triage epic this brief seeds)
1. Each MUST item verified against official docs on our install and either adopted (recorded where) or rejected with a one-line why.
2. Each SHOULD item has ONE bounded pilot with an ex-ante success metric; pilot outcomes recorded as intake follow-ups.
3. PLAYBOOK model-selection table refreshed (Sonnet 5 reality).
4. A buy-vs-build verdict per overlap: Routines-vs-harness, /batch-vs-ADR-97 mechanics, Outcomes-vs-manual-RETURN-review, Artifacts-vs-#264 — each states what we RETIRE of our own scaffolding if adopted (the point is deleting rot, not adding features).

## 5. Non-goals
No doctrine changes from this brief alone (pilots first). No adoption of anything that bypasses the safety envelope or closure discipline (e.g. /goal with self-asserted conditions; auto mode replacing our gates unexamined). No corp-* repos in pilots.

## 6. Changelog-review mechanism — meta-requirements (functional-architect addendum, 2026-07-06)
Context: the /changelog-review command (#113, sentinel-driven, buckets ADOPT/OBSOLETES-WORKAROUND/STALE-NAMES/VERIFY/NOISE) is well-designed and had a clean first run (2026-06-07). But ~32 CC versions passed unreviewed between that run and today — including Sonnet-5 and auto-mode class changes — because its ADOPT bucket had no consumer (the fleet-audit lesson, review edition).
- **R1 (must):** wire /changelog-review's ADOPT + OBSOLETES-WORKAROUND outputs into `intake/` as status=SEED docs — the review gains a consumer, the intake scene gains a feed. No more "operator routing" dead-ends.
- **R2 (must):** verify #119 (codex 0.136→0.137, the 06-07 window's only ADOPT — Windows SQLite fix relevant to the codex exec wrapper) was actually executed; a month old and status unknown.
- **R3 (should):** cadence teeth — the sentinel fires at SessionStart, but a month-long gap happened anyway; add a staleness escalation (unreviewed-window > N versions or > 14 days → surfaced in the morning triage, not just a boot line).
- **R4 (should):** dogfood-signal heuristic for the ADOPT rubric: features Anthropic ships as CC defaults for its own use (auto mode, agents view, /usage, /recap) carry a prior of adoption-worthiness — triage them first.
- **R5 (could):** reconcile the review's bucket taxonomy with this brief's MUST/PILOT/WATCH triage so the two funnels speak one language at intake.

## 7. Open questions (functional → technical)
- Routines: do cloud agents reach our repos (GitHub-pushed) with acceptable trust boundaries? What leaves the machine?
- Outcomes: where does the rubric live — in the epic bundle (generated from the done-contract) or hand-authored?
- /batch governance compatibility (the make-or-break question for adopting it).
- Auto mode ("background safety checks" replacing prompts) vs our deny-first floor — reconcile or reject; never both silently.
- Which of our G-batch permission workarounds are obsoleted by the Week-26 subagent-permission change (verify empirically).
