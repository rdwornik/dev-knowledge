# ADR-85: Session-lifecycle enforcement — deterministic JOURNAL/BACKLOG stop-gate

**Status:** Accepted
**Date:** 2026-06-16
**Decision tier:** Architecture (AI Council, 4-model panel — see verdict: council-out-20260616_131123)

## Context
The human is the manual trigger at every session end, reciting which canonical docs to update. The reminder is unreliable: docs rot (CONTRIBUTING untouched for days) and a recent agent-authored close-plan silently omitted most of the doc set. The workflow's value is its discipline — every change traceable, no fabricated state — so any enforcement must not be gameable into box-ticking. A 4-model Council debated mechanism (deterministic vs LLM-judge), teeth (hard/soft), and scope (strict/adaptive), plus a contrarian (enforce vs simplify).

## Decision
1. **Scope reduction is the primary intervention.** Gate **only JOURNAL + BACKLOG** per session — the two docs that both rot worst and legitimately change every working session. Demote ARCHITECTURE, VISION, LESSONS, CONTRIBUTING to **"update when materially affected"** — not per-session-gated.
2. **Mechanism: deterministic, executor-side.** Extend the existing session-end-hygiene Stop-hook; no LLM in the gate. Rationale: once scope is two docs, currency is no longer a fuzzy semantic question — it is a deterministic check that is debuggable, zero-latency-per-turn, and cannot hallucinate compliance.
3. **Teeth: hard block on the JOURNAL leg only in v1.** JOURNAL leg verified by an **un-gameable commit-SHA anchor** (the journal diff must reference ≥1 commit SHA produced this session) — this **supersedes** the prior advisory journal-presence check, which the SHA anchor strictly subsumes. The **BACKLOG leg is advisory (a nudge, not a block) in v1** — verified by a structural-marker delta — and is **promoted to a hard block when the traceability-spine gives it an airtight, always-warranted anchor (see R1)**. Rationale: a hard gate is justified only for a check that is both un-gameable *and* always-warranted; the backlog-marker check is neither (it is gameable, and per the "done tasks leave the file" convention a session that advances but does not finish a task warrants no backlog change), so hard-gating it in v1 would manufacture the false-positives the criteria below warn against.
4. **Override: explicit + logged, HEAD-bound.** A blocked turn exits only via `/override [reason]`, which is logged. The override is a gitignored token recording the current HEAD; the Stop-hook **pure-reads** it and allows while HEAD is unchanged, **re-arming automatically when a new commit lands** — keeping the hook a read-only validator (per the repo's scripts-are-read-only invariant). **No auto-bypass-after-cap** — auto-bypass trains the agent that persistence beats policy.
5. **Single source of truth.** One `definition-of-done` doc, injected into the executor at session-start and into the orchestrator handoff.
6. **Scope-freeze.** No docs added to the gate for 4 weeks; gather reliability/override-rate data first.

### Architect refinements (on top of the panel verdict)
- **R1 — Backlog anchor couples to the traceability-spine.** The journal leg is airtight (SHA); the backlog "structural-marker" leg is the weak, gameable leg. Its real anchor (issue-ID↔commit) IS the separate traceability-spine decision. Therefore: ship the JOURNAL gate hard now; the BACKLOG leg runs as an **advisory nudge** on the interim marker-check and is **promoted to a hard block when the traceability-spine ADR lands**. Co-design. *(Hard-gating the weak leg in v1 would manufacture the false-positives the criteria warn against — this refines an earlier version of R1 that had backlog as a hard interim gate.)*
- **R2 — Ungated-doc rot is handled by detection, not human review.** The panel's "human bi-weekly review" of the ungated docs reintroduces the human-as-trigger. Instead, ungated-doc staleness (e.g. ARCHITECTURE untouched >N sessions while code changed) is **surfaced as a signal in the daily digest / conformance dashboard** — deterministic, not per-session-gated, not human-memory. This is a later item that rides with the conformance-dashboard work; v1 accepts the other docs are ungated.
- **R3 — Explicit override only on the new gate (no auto-bypass).** *Implementation verified the existing hook is purely advisory — it emits a soft nudge, always exits 0, and has no hard block and no auto-allow-after-cap. There is nothing to remove; the original framing of this refinement ("remove the existing auto-override antipattern") was based on a wrong premise and was corrected after CC read the live hook.* This is therefore a **forward constraint on the new hard gate**: a blocked turn exits only via explicit `/override`, never via a retry-counter that auto-allows (which would train "persistence beats policy").

## Consequences
**Positive:** human is no longer the trigger; deterministic (debuggable at 2am, no per-turn LLM latency/cost); journal leg un-gameable; narrow scope → low false-positive surface; v1 removable in one revert sequence.
**Negative / accepted trade-offs:** the four ungated docs will rot more until R2 lands (accepted for v1); the backlog leg is advisory-only until the traceability-spine hardens it to a gate (R1); override-normalisation risk — mitigated by logging (if overrides exceed ~10% of sessions, the rules need tuning, not the human).

## Alternatives rejected
- **LLM-judged primary gate** (the going-in lean): nondeterministic, per-turn latency, can hallucinate compliance — and scope-reduction dissolves the semantic-fuzziness that justified it.
- **Hard block on the full doc set:** guarantees false-positives → the gate gets disabled; incentivises box-ticking.
- **`/wrap` operator routine as primary:** still a human trigger — fails the core goal.
- **Auto-allow after N retries:** trains the agent to loop until the gate yields.

## Amendment — 2026-06-16 (CC implementation correction; defect fix, not a new decision)
The v1 hook exposed a **contract error** in this ADR's framing. A Stop hook's
`hookSpecificOutput.additionalContext` is **not** a clean allow: per CC changelog v2.1.163 it
"continues the conversation" — it **keeps the turn going** — and consecutive keep-goings count
toward CC's block-cap (v2.1.143), which auto-overrides the turn. So the "advisory = exit-0,
non-blocking" premise (Decision 3 / R3) was **wrong**: an advisory built on additionalContext
**loops to the cap** when its condition persists across stop attempts (a no-task session's
BACKLOG-no-marker — the *correct* state per the DoD — or freshness same-day, where re-stamping
is a no-op diff) → the exact "persistence beats policy" auto-bypass §4 / "Alternatives
rejected" forbid. Witnessed live: "a hook blocked the turn from ending 9 consecutive times —
overriding and ending turn."

Realized fix: advisory legs are made guaranteed-terminating by a **structural floor** —
advisory-only output never keeps the turn going; advisory rides **only** folded inside a hard
block. This is the *load-bearing* guarantee, because `stop_hook_active` is **NOT** in the
CC-2.1.178 Stop-hook stdin schema (verified) so a fire-once-on-retry scheme cannot carry it; a
fire-once path is wired but **dormant** (activates only if a runtime ever supplies the field).
The **hard JOURNAL leg is unchanged** and explicitly does **NOT** honor `stop_hook_active`
(honoring it = fire-once = the forbidden antipattern); it terminates by *compliance*, never the
cap. Fix commit `8840b33`; tests reproduce the keep-going loop red→green. See JOURNAL &
LESSONS 2026-06-16.

## Links
- Council verdict: `council-out-20260616_131123-pick-council-brief-session-lifecycle-enforcement.md`
- Coupled decisions: traceability-spine (R1), handoff-supplement (the DoD-via-handoff is process-context-in-handoff), conformance-dashboard (R2).
