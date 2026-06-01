# ADR-68 — Autonomous overnight review agent

**Status:** Accepted
**Date:** 2026-06-01
**Decision method:** AI Council, `pick` mode, 4-model panel (claude-opus-4-7, deepseek-v4-pro, grok-4.3, gpt-5.4) + Gemini synthesis. Unanimous on architecture and autonomy boundary.
**Related:** ADR-41 (per-repo ownership), ADR-61 (git worktree pattern), ADR-67 (AI Council process — parked), three-domain separation invariant.
**Supersedes:** none.

> Verify this is the next free ADR number before committing (ADR-67 is parked-unmerged; renumber if a collision exists — ADR hygiene per the ADR-27 precedent).

## Context

The operator wants to use idle overnight hours for high-value *review* across the ~6-repo ecosystem — canonical-file content accuracy (do docs still match recent decisions?), cross-document coherence, per-repo compliance audits — and wake to a findings briefing rather than to changes.

Proven precedent: one overnight multi-phase ecosystem audit (2026-05-29) already produced 7 phase-findings that became backlog items, using nothing more than a structured prompt + filesystem reads + a markdown briefing. The pattern works; this decides how to systematize it.

Platform reality that constrains the design:
- Native primitives exist — headless `claude -p`, Claude Code Routines (cloud-scheduled), Agent Teams (parallel split-and-merge).
- The Max subscription has a weekly cap (plus an Opus-specific weekly cap) shared across Claude Code + chat + Cowork, introduced specifically to curb 24/7 background runs. Heavy overnight subscription use therefore subtracts directly from daytime working capacity.
- A dedicated API key decouples automation from the subscription weekly cap and is the supported path for automated runs; cost is per-token.

## Decision

Adopt **Option B**: a local OS scheduler triggers a headless `claude -p` run performing **read-only review** and emitting a **morning briefing**. No custom orchestrator. No unattended writes beyond the briefing file. *Auth is the logged-in Max subscription — an operator override of the Council's API-key recommendation; see sub-decision 2.*

Sub-decisions:

1. **Substrate.** Windows Task Scheduler → a PowerShell runner → `claude -p` invoked sequentially per repo. (The panel's bash/cron examples are translated to the operator's Windows environment.)
2. **Auth / budget — operator override of the Council recommendation.** The Council recommended a dedicated API key to insulate daytime capacity. The operator elected **subscription auth** (headless `claude -p` runs on the logged-in Max subscription — no API key, no separate billing), explicitly accepting that overnight runs draw from the *same shared weekly pool* as daytime work. Mitigations: (a) **model-tiering** — Sonnet for the bulk per-repo review scan, Opus reserved only for the final synthesis pass — to spare the scarce Opus weekly allowance; (b) a hard per-run **token + runtime cap** (not a dollar cap — there is no per-token dollar cost on subscription); (c) log token consumption per run and monitor weekly headroom. **Revisit → API key** if overnight runs measurably throttle daytime work.
3. **Autonomy boundary: read-only → report.** No draft ADRs, no draft PRs, no branches, no edits, no issue filing. Enforced by a **scoped Claude Code permission policy** — *pre-allow* `Read`/`Grep`/`Glob` and `Write` restricted to the briefings directory (these run **silently, so the unattended run never stalls on a permission prompt**), and *deny* `Edit`, write-capable `Bash`, and any git-mutating command (**refused outright, not queued for approval**). This is **not** `--dangerously-skip-permissions`: both approaches eliminate the 3am prompt, but the dangerous flag also eliminates the *guardrail* — it auto-approves everything. An unattended agent reading dozens of files across repos could be steered by adversarial content in a file (the methodology's own untrusted-input concern) into a write or delete, and the flag would let it execute while the operator sleeps. The deny-policy makes "read-only" **physically true at the tool level**, which is the precondition for running unattended at all. Rationale: prompt-level constraints are aspirational; policy-level constraints are debuggable invariants.
4. **Clean state.** The agent reads a dedicated **read-only git worktree** checked out to each repo's latest canonical commit (per ADR-61) — never the live working tree. This prevents auditing half-finished local refactors and producing false anomalies.
5. **Execution model: sequential** over the ~6 repos. Overnight wall-clock (6–10h) is ample; parallelism adds race conditions, dedup overhead, and synthesis-merge hallucination risk. Defer parallel breadth (Agent Teams) until a single run demonstrably exceeds the wake window.
6. **Output.** A timestamped `briefings/YYYY-MM-DD.md`: **max 5 findings**, ranked by severity × confidence, each with a **mandatory exact `file:line` citation or the synthesis pass drops it**. "No significant findings" is a valid, expected output. Structural citation requirement beats asking the model to self-assess confidence (LLMs are poorly calibrated at that).
7. **Seed file.** A dumb, diff-able operator-edited markdown queue (which repos, which concerns) seeds the next run.
8. **Homes (three-domain).** The *decision* (this ADR) lives in `.dev-knowledge` (methodology owns the decision). The *operational system* — runner script, review-prompt, briefing template, permission policy, scheduler config — is self-contained in the runtime domain at `~/.claude/night-agent/`. Briefings land in `~/.claude/night-agent/briefings/` as operational artifacts; the operator **promotes** real findings into the methodology backlog, keeping the knowledge base curated rather than flooded with raw nightly output. *(Judgment call: the review-prompt is placed in runtime for self-containment/maintainability rather than split into the methodology repo. Operator may veto for strict separation.)*
9. **Reliability.** The scheduler job uses absolute paths and explicit environment export (stripped scheduler environments — missing PATH/keys — are the #1 silent-failure cause). A **separate, independent** scheduler job at ~08:00 checks for the existence and non-emptiness of today's briefing and fires a desktop notification if missing — because if the machine slept, the in-pipeline notifier never ran either.

## Alternatives considered

- **Option A (Routines + subscription budget): rejected.** The weekly cap was introduced precisely to curb the 24/7 background pattern A enables; overnight subscription use cannibalizes daytime capacity — a daily, felt cost, not theoretical. The "laptop-off" convenience does not outweigh degrading the operator's primary daytime instrument.
- **Option C (custom orchestrator): rejected as premature.** The proven precedent ran with just `claude -p` + a prompt. A shell/PowerShell script + scheduler + prompt file is reconstructible from memory; a custom orchestrator with queue/budget/parallel-coordination logic is not. Build the artifact the future solo maintainer can rebuild in 20 minutes.
- **Limited-write autonomy (draft ADRs / draft PRs): rejected.** In a review-gated, one-human methodology, an unattended draft *anchors* the morning review — the operator reviews the agent's narrative instead of doing genuine fresh-eyes review of the code. Findings are interrogatable; drafts are anchoring. Add the error-propagation risk of any unattended write, and the case is clear. Reconsider only after 30+ briefings show ≥80% of suggestions would have merged unmodified, and only into a sandboxed non-canonical target.

## Consequences

Trade-offs accepted: the machine must stay on (or wake) overnight — but a missed run is graceful degradation (no briefing that morning) versus the catastrophic degradation of running out of daytime capacity mid-week. No separate dollar cost (subscription), but overnight consumption is **not free** — it draws from the shared weekly pool, so it must be kept modest (model-tiering + caps) to avoid throttling daytime work. No initial parallelism — nothing real is lost at this scale.

Risks & mitigations:
- **Weekly-cap contention** (overnight runs eat the shared weekly pool, throttling daytime work) → model-tiering (Sonnet scan / Opus synthesis), hard per-run token + runtime cap, file-extension allowlist, weekly-consumption monitoring; revisit → API key if daytime throttling is observed.
- **Briefing-quality drift** → fixed template, max-5, mandatory citations; track findings→backlog conversion; revise the prompt if <30% convert for two consecutive weeks.
- **Silent scheduler failure** → independent morning missing-briefing alarm; non-zero exits; run logs.
- **Accidental write** → permission policy + read-only worktree (defence in depth).
- **Findings-as-authority** → the methodology's human fresh-eyes pass stays mandatory; agent findings are inputs to review, never review itself.

## Signals to revisit / kill

- **→ Option C** if the prompt file needs editing >2×/week to tune prioritization, or multi-stream coordination becomes necessary.
- **→ API-key auth** if overnight runs measurably reduce daytime working capacity. This was the Council's recommended default; the operator chose subscription to avoid separate billing. The switch is cheap (set `ANTHROPIC_API_KEY`, drop the model-tiering constraint).
- **→ Option A** if Anthropic decouples overnight subscription use from the daytime cap *and* Routines gains durable failure handling.
- **→ limited-write** only under the 30-briefing / ≥80%-merge-worthy / sandboxed-target conditions above.
- **Kill the system** if 6+ weeks of briefings produce <1 backlog-worthy finding per week. Value over volume means being willing to switch it off.
