<!--
  SUPPLEMENT.md — architect strategic supplement (HANDOFF_PROCESS.md §13
  "Architect strategic supplement"). Generated from templates/handoff/v5/SUPPLEMENT.md.tmpl
  for this bundle. Self-documenting fillable form.

  Lifecycle: CC writes this UNCONDITIONALLY (empty), commits it on the handoff branch;
  the operator pastes the QUESTIONS to the OUTGOING architect chat, pastes answers below
  the divider, says `supplement filled`; CC commits verbatim + re-runs assemble_paste.py,
  which folds the ANSWERS region into the next PASTE_THIS — only if non-empty.

  SCOPE (load-bearing): answer ONLY the non-re-derivable strategic *why*. NEVER repo
  state / methodology / task-state / counts / SHAs (those are source-authoritative +
  forced-read, §3/§5). Advisory, never teeth, never fabricated — unanswered = committed EMPTY.
-->

# Architect strategic supplement — 2026-07-04-dev-knowledge-architect-2

Repo: dev-knowledge · Mode: architect · Date: 2026-07-04

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.

<!-- CC-observed addenda (session-specific; §13 permits 1–2) -->
A. **Slice A acceptance bar** — what is your accept/iterate criterion for the sandbox
   spawn+isolation foundation before Slice B builds on it? (The Codex 2 CRIT + 2 HIGH are
   fixed; is the isolation contract — `CLAUDE_CONFIG_DIR`-hooks, system-temp teardown,
   protected env keys, exit-gating — the seam you want, or does the boundary move?)
B. **Sequencing the deferred handoff-spec arc vs the sandbox** — do you want the
   HANDOFF_PROCESS §5/§13 → option-b reconciliation + `5.3→5.4` bump folded into the
   ARCHITECTURE-currency pass BEFORE Slice B (so the corpus is settled), or after (so
   Slice B momentum isn't interrupted)? It collides with sandbox-owned `ARCHITECTURE.md`.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

# ARCHITECT SUPPLEMENT — dev-knowledge architect, session wrap 2026-07-04

Outgoing-architect answers for the incoming session. Pairs with CC's repo-derived bundle (BOOT + RESIDUAL + PROBES). This is the off-repo half — rulings, dispositions, forward plan — none derivable from committed state. **Re-verify every state claim against live HEAD before acting** (a point-in-time supplement is not current truth). Supersedes any earlier wrap draft (this one reflects Slice A *shipped*).

## State snapshot (both lanes, final)

- **main = a523fca, pushed** (local == origin). Tree clean. Worktree fully cleaned (no linked worktrees, no stale `feat/*` or `worktree-*` branches, no `.dev-knowledge-*` orphans).
- **Sandbox Slice A SHIPPED** (merged `--no-ff`, Codex-hardened): `deploy/lived_sandbox/` (spawn + isolation + cli). Spawn viability PROVEN empirically; isolation PROVEN (configA-sentinel/configB seam). doc-counts current at 1216.
- **Handoff-generator lane INTEGRATED** (`9d5ebe5`): `gen_handoff.py` + anti-bluff rung + templates + size-warn. Anti-bluff is now structural (option b) — the erosion cannot silently return.
- **RF-2 hub self-arm** (`2e7b072`) + **ARCHITECTURE currency + coherence RF-1 surfaces** (`fbf88ae`) + **OneDrive P0 guard** all landed and verified.
- **Open for operator:** rotate the leaked `ANTHROPIC_API_KEY` (operator-only — CC blocked by the P0 guard from writing `.secrets/.env`, which is OneDrive-redirected). No build impact.

## Q1 — Strategic intent (way-of-working level)

**Prove the COMPOSED system end-to-end on a real consumer — close "presence ≠ enforcement" at the workflow level, on ai-council.** Slice A proved the sandbox *foundation* (spawn + isolation). What's missing is the *measuring instrument*: Slice B's OUTER observer + the essence-spec `engages:` oracle + the six-hook arc + the seeded EXPECTED-BUT-SILENT closure — and then the **first ai-council consumer-run**, which is the operator's stated priority #1 ("the hub tested on ai-council like a sandbox") and is **still undelivered**. Phase 0 (turn the standard inward — the hub meets its own standard) is ~60% done; Phase 1's foundation is proven but its instrument is not built. Q1 = build the observer, then run the first consumer-sandbox on an ai-council clone.

## Q2 — Tensions weighed, where I landed

- **Split the sandbox at the spawn-isolation boundary** (Change #2): landed on split because `claude -p` spawn is the no-precedent part — prove + Codex-review the foundation before building the observer on it. **Validated** — the split caught a false-green isolation bug (Codex CRIT: `IsolationResult.passed` was true even when both runs failed).
- **Ship-Slice-A-then-wrap vs plow into Slice B** (this session): landed on wrap — Slice B is a fresh large build deserving clean context, and CONTEXT SELF-EVAL triggered (≥3 unresolved follow-ups).
- **Fleet-currency signal:** landed on **D5 (coverage) is the dominant signal, not D1 (stamp)** — measured the matrix, don't patch dates.
- **ai-council CLAUDE.md stale:** landed on **timing, not bug** — the gate was born in the same commit it "should have caught"; the next commit hard-blocks; the standing sweep is the proactive catch. Don't patch the date.

## Q3 — Considered + rejected (do NOT relitigate)

- **Anti-bluff option (a)** (ratify drift-reference hints in the bundle) — REJECTED for option (b) (strip values by construction; hints → JOURNAL). Built.
- **Fable consult on the core plan** — REJECTED: the four reviews ARE the consult (convergent, no contested fork). Codex is the heterogeneity mechanism at implement-time, not a fresh consult.
- **The separate 8-finding Phase-0 recon** — RETIRED in favor of plan-first-self-verifying builds (each build verifies its finding in the plan phase — fewer round-trips).
- **LLM-gating on semantic properties in the sandbox** — REJECTED (false-positive death-spiral). Model-mediated engagement is observed-and-reported, never gated.
- **Worktree or container for the sandbox** — REJECTED (shared `.git`/stash class; Windows-native fidelity is the point). Throwaway `mkdtemp` clone + isolated `CLAUDE_CONFIG_DIR`.
- **The §5 edit inside the handoff worktree** (Q1 ruling) — REJECTED (ARCHITECTURE.md collision + freshness-gated). Decoupled to serial integration.
- **Rot-algorithm build-now** — NOT rejected; deferred to Phase 2 (feeds P5). Don't build it before the sandbox.

## Q4 — Open questions (unresolved / deferred)

- **§5/§13 spec-arc sequencing** — see B (ruled: after Slice B).
- **#164 formal disposition** — amend-then-close vs keep-open (cross-repo probes + v4-prose removal remain ADR-83-gated). Architect's call at integration.
- **#251 deploy-CLI red** (`test_cli_execute_success_reports_branch`) — stale-test vs real UX regression (the success render dropped the `record_branch` string). Decide, don't carry indefinitely.
- **Semantic content-drift tier** (fleet matrix dim-2) — deferred behind an n=2-adoption + findings-acted-on gate.
- **Load-gauge** — I ruled it lands BEFORE more mechanisms (the one entropy source with no counter-tactic); confirm still un-built and prioritize in the Phase-0 batch.

## Q5 — Decomposition rationale (the task-graph shape)

Three dependency-gated phases: **Phase 0** (self-application — cheap, unblocks everything) → **Phase 1** (sandbox — gated on RF-2, else it measures a facade) → **Phase 2** (currency + fleet — gated on corpus-settling). WHY: safety before momentum (P6 multiplies unfixed risk across 4 repos); the sandbox is the acceptance instrument so it precedes the fleet; the composed-workflow proof needs the foundation (spawn+isolation, Slice A) before the observer (Slice B). **Do NOT redo/re-decide:** the P1–P4 mechanism (shipped n=1); the sandbox-oracle decision (essence-spec `engages:`); the "what NOT to add" refusals; the 4 sandbox-plan corrections; Slice A's isolation contract (Codex-hardened); the anti-bluff option-b decision; the fleet D5>D1 reframe; the ai-council timing verdict.

## Q6 — Off-repo context

- **Operator priority #1 is STILL undelivered:** prove the hub on ai-council like a sandbox — needs Slice B observer + the first consumer-run. Everything else is subordinate to reaching that.
- **Worktree-isolation lesson (methodology-relevant):** a worktree isolates the CHECKOUT, but an absolute path to the primary bypasses it (the handoff session mis-rooted edits into the primary via subagent-reported absolute paths; recovered, no work lost). Future parallel-worktree delegates MUST operate strictly within their worktree dir (relative paths). CC saved memory `worktree-edits-land-in-primary-via-absolute-paths`.
- **Key rotation pending** (operator-only; the P0 guard blocked CC from `.secrets/.env` — the guard working on its author, the best possible proof it fires).
- No LLM-budget ceiling.

## A — Slice A acceptance bar (ACCEPTED)

I **accept** Slice A; the isolation contract IS the seam I want, and the boundary does NOT move — Slice B builds the observer ON this contract:
- `CLAUDE_CONFIG_DIR` governs user-level hooks (proven configA/configB); project-level hooks in the clone's cwd still fire independently.
- Teardown blast-radius anchored to the system-temp dir (Codex fix), `_rmtree_guarded`.
- Protected env: `CLAUDE_CONFIG_DIR`/`ANTHROPIC_API_KEY` pinned LAST, `CLAUDE_PROJECT_DIR` popped (so `extra_env` can't override; Codex fix).
- Exit-gating: `passed` requires `exitA==0 AND exitB==0` (the false-green fix).

**One re-verify at Slice B start (not a Slice A defect):** confirm the isolation still holds when the inner session does REAL work — the six-hook branch→edit→commit→wrap arc — not just the sentinel probe. I.e., the arc's own hooks fire in the isolated child as expected. That is the first Slice B check, before the observer is trusted.

## B — Sequencing the §5 spec-arc vs the sandbox → AFTER Slice B

**Ruling: do the §5/§13 spec-arc AFTER Slice B, not before.** Reasoning:
- **No technical collision either way.** The ARCHITECTURE.md "collision" only bites if the two run CONCURRENTLY (parallel worktrees). Sequential in one lane, there is no conflict — so the choice is about value/momentum, not safety.
- **§5 is orthogonal to Slice B.** Slice B touches `deploy/lived_sandbox` + manifest + observer; it does NOT touch HANDOFF_PROCESS or the reconciled_with docs. An un-settled §5 does not interfere with Slice B at all.
- **§5 is additive bookkeeping** — it NAMES an already-true invariant (the rung already enforces it; §5 already says "never the answer... rejected") + a version bump. Interrupting the priority-#1 deliverable (Slice B + ai-council run) for bookkeeping is backwards.
- **The corpus doesn't need §5 settled for the bundle** — anti-bluff is already structural (option b built), so a generated bundle is already clean regardless of §5.
- **Efficiency note:** Slice B will touch ARCHITECTURE.md anyway (register the sandbox check). The §5 ARCHITECTURE.md re-stamp CAN fold into that same currency pass (one re-read covering both the sandbox-check-count and the 5.4 bump) to avoid a double re-read — architect's call at integration.

## Audit disposition (the four Fable audits + the Codex review)

| Audit                                     | Key findings                                                                                                                                            | Disposition                                                                                                                                                                       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fable architecture review**             | RF-1 OneDrive P0, RF-2 hub self-arm, RF-3 honest-limits, §6 sandbox, RF-6 consult-lane, RF-7 routing, RF-8 dead v4 checks, RF-9 worktree-context        | RF-1 ✅ built · RF-2 ✅ built · §6 sandbox foundation ✅ (Slice A) · RF-3/6/7/8/9 → Phase 0 batch / Slice B                                                                          |
| **Handoff-adoption review**               | RF-1 anti-bluff, RF-2 generator, RF-3b boot-echo, RF-4 immutability, RF-5 cp1252, RF-6 re-narration, RF-7/8/9                                           | RF-1 ✅ built (option b) · RF-2 ✅ built (generator) · RF-4 → §5 spec-arc (deferred, see B) · RF-3b/5/6/7/8/9 → not built                                                           |
| **Coherence-spine review**                | RF-1 stale surfaces, RF-2 ESSENTIALS↔PLAYBOOK inversion, RF-3/#220 currency≠presence, RF-4 granularity, RF-5 FAIL-trap, RF-6 spec-absent→WARN, RF-7/8/9 | RF-1 ✅ (L318/L392 cleared via currency; PLAYBOOK:253/256 + RF-8 docstrings pending) · RF-3 → fleet-sweep (scoped, not built) · RF-5/RF-6 → Phase 0 batch · RF-2/4/7/9 → not built |
| **Rot-algorithm design**                  | `rot_report.py` — reverse-reference multimap + 3 existence predicates (dangling-path / dangling-wiring / tombstone blast-radius) + `--impact`           | **DESIGNED, NOT BUILT** · Phase 2 · feeds P5 · Track-B sibling of the fleet-currency sweep                                                                                        |
| **Codex review — Slice A** (gpt-5.5 high) | 2 CRIT (isolation false-green; teardown blast-radius) + 2 HIGH (env-key override order; spawn-failure handling)                                         | ✅ all fixed + tested; isolation re-PROVEN. (A code-review artifact for our Slice A build — lives in `docs/audits/` per the review-artifact convention.)                           |

## Forward plan (phases + real status)

**Phase 0 — self-application (~60% done):** ✅ OneDrive P0 · ✅ RF-2 self-arm · ✅ anti-bluff · ✅ coherence RF-1 (L318/L392). **⬜ Remaining batch (disjoint from sandbox):** coherence RF-5 FAIL-trap (one function move + tests), RF-6 spec-absent→FAIL, cp1252 + ASCII-output regression test, honest-limits in DEFINITION_OF_DONE, **load-gauge** (before more mechanisms), PLAYBOOK:253/256 RF-1 surfaces, validate_reconciliation RF-8 docstrings, #251 disposition.

**Phase 1 — sandbox (foundation proven, instrument not built):** ✅ Slice A (spawn + isolation, Codex-hardened). **⬜ Slice B [#252]:** OUTER deterministic observer (transcript + git-state + hook-stdout, never inner narration — LESSONS 2026-06-04) + essence-spec `engages:` oracle (extend `deploy/manifest-v1.2.0.yaml` components with `{trigger, observable, expect}` + `release_lint` lint) + six-hook branch→edit→commit→wrap arc + ≥1 command acts + **seeded EXPECTED-BUT-SILENT closure** (disable a should-fire hook, prove the observer FLAGS it — the harness leg-e). Refusals: no nightly, no LLM-gating, no container, inner never self-certifies, never push to a live remote. **⬜ First ai-council consumer-run** (`cli --consumer <ai-council-clone>`) — this delivers priority #1. **⬜ RF-3b boot-echo** (closes #159).

**Phase 2 — currency + fleet (scoped, not built):** ⬜ rot-report (feeds P5) · ⬜ standing fleet-currency sweep (matrix measured: D5 coverage dominant, 12 uncovered cells, corp-ops zero-mesh) — Track-B family with rot-report · ⬜ P5 hub self-prune (#130, Opus/plan-first) · ⬜ P6 fleet roll n=2+ (gated: Phase 0/1 + D4 + v1.3.0 cut + standing sweep + **per-consumer mesh transfer not just presence** + mesh-commit bumps target stamp + #225/#249/#250; corp-ops needs the whole mesh, corp-monorepo/sca need the freshness gate) · ⬜ semantic content-drift tail (deferred behind adoption gate).

**Integration follow-ons:** §5/§13 spec-arc (after Slice B, per B) · #164 disposition · corp-sca version-provenance backfill.

## First next-session actions

1. Boot + orient (VISION/ARCHITECTURE quotes via CC). Confirm open verification threads (below).
2. Build **Slice B** [#252] — the observer + oracle + arc + seeded-silent closure. First check: re-verify isolation holds under the real arc (not just the sentinel).
3. Run the **first ai-council consumer-sandbox** — delivers priority #1.
4. In parallel (disjoint, worktree — enforce the relative-path lesson): the **Phase-0 batch** (RF-5/RF-6/cp1252/honest-limits/load-gauge/PLAYBOOK/RF-8/#251).
5. §5 spec-arc + #164 disposition after Slice B.

## Open verification threads (confirm at read-time — do not assume)

- Key rotated? (operator, pending)
- #251: stale-test or real regression?
- Any drift on main since a523fca?
