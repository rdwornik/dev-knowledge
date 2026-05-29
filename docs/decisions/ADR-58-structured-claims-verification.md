# ADR-58: Structured claims + symmetric verification

- **Status:** Accepted
- **Date:** 2026-05-26
- **Related:** ADR-42 (handoff format v3), ADR-55 (applied-task gate — receiver side of the same ratification), `protocols/HANDOFF_PROCESS.md` (Stage 2 / Stage 3)
- **Decommission:** bare `role confirmed` as sufficient Stage 3 ratification (replaced by structured ratification in this session's Phase C process amendment)
- **Source:** AI Council debate Q4, 2026-05-26 — `docs/decisions/transcripts/council-out-20260526_144851-pick-2026-05-25-handoff-council-Q4-sender-verification-symmetry.md` (Recommended Decision L826-892; Action Items L931-955)

## Context

Handoff verification is asymmetric: the receiver (NEW chat) is gated, but the
sender (OLD chat) ships claims with no verification gate, and a bare `role
confirmed` ratifies the transfer.

- `docs/research/2026-05-25-handoff-failures-evidence.md` documents **N=7 sender
  verification misses in a single session** — the OLD chat with *maximum* context
  made confident, unverified, wrong claims (e.g., a hallucinated 11→4 file map
  referencing files that do not exist; a wrong ADR-39 fix mechanism). "Context
  volume did not prevent verification failure."
- The same evidence shows the sender-reviewer "confirmed `role confirmed` without
  flagging Item 2 drift — receiver gates were treated as ACK checkpoints rather
  than substantive review."

The sender must stop shipping prose-only claims; but the (potentially
contaminated) sender must not be the sole reviewer of the receiver's
understanding either.

## Decision

Adopt **symmetric sender-side verification** as an enforced gate: a structured
claim artifact produced by the sender, mechanically validated by the executor,
and substantively ratified by the operator.

- **Sender owns the reviewable contract.** Produces `11_CLAIMS.md`: every
  load-bearing claim has a citation (repo path / `ADR-NN` / `session: YYYY-MM-DD`)
  OR an explicit assumption marker. Plus a compact expected-articulation contract
  (what the receiver should understand).
- **Executor owns mechanical checks.** Validates cited file existence /
  line-range locatability / decision-reference format. Optionally limited
  articulation alignment for concrete entities. Structural facts only — not
  semantic understanding.
- **Operator owns substantive ratification.** Not by memory or bare `role
  confirmed`, but by comparing the receiver's articulation against the sender's
  `11_CLAIMS.md` + the executor's validation report. Bare `role confirmed` is
  removed as sufficient.
- **Trigger rule (fixed):** "A confident claim about an unread or unverified
  source requires verification + citation."
- **Load-bearing claim** = decision-affecting: file paths, commit SHAs, ADR refs,
  action plans/sequencing, architecture descriptions, current-state assertions.
  Non-examples (no citation needed): reasoning steps, recommendations, clearly
  marked opinions.
- **Degraded mode:** if executor validation is unavailable, the handoff is marked
  `UNVERIFIED`; the operator must explicitly acknowledge; no silent bypass.

**Deviation from Council action item AI1.** The transcript names the artifact
`CLAIMS.md`; per operator decision 2026-05-26 it is the bundle file
`11_CLAIMS.md` (sequential after `10_GATE_PROBE.md`).

## Consequences

- Sender hallucinations are caught at the source (structured + executor-validated)
  rather than propagating into the next session's premises.
- Operator ratification becomes bounded and binary (claims present? executor
  green? articulation matches expected?) instead of a memory-based rubber stamp.
- Adds front-loaded sender + executor cost — accepted: the evidence shows real
  downstream cost from sender hallucinations.

## Risks (from Q4 risk register, L894-929)

- **Citation theater** (mechanical citations without real verification) → executor
  validates existence/locatability; require a quoted snippet for sampled claims;
  audit first N handoffs.
- **Artifact drift** (bundle changes after claims generation) → make `11_CLAIMS.md`
  the final Stage 2 output; regenerate if bundle content changes materially.
- **Operator overload** → keep operator review bounded/binary; remove bare `role
  confirmed`.
- **False confidence in mechanical checks** → document explicitly that executor
  checks structural validity only.
- **Workflow fragility if executor pre-flight unavailable** → degraded mode
  (`UNVERIFIED` + explicit operator acknowledgment, no silent bypass).

## Alternatives considered

- **Prose-only sender gate (option A)** — rejected: prose claims are exactly what
  failed N=7 times.
- **Sender as sole reviewer of receiver articulation** — rejected: a contaminated
  sender cannot be the sole downstream reviewer.
- **Mechanical semantic checking** — rejected: articulation understanding remains
  a human judgment problem; executor checks structural facts only.

## Trace

`11_CLAIMS.md` template (claims table + assumptions table + verification-status
checklist + trigger-rule reminder + load-bearing definition) is added as a
bundle-file section in this session's Phase C template amendment.

---

## Amendment 2026-05-29 — evidence file relocation

> Append-only reference correction per ADR-39 (immutable body preserved). Grounds:
> `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` finding E1.

The Context section above cites the empirical-basis evidence file at
`docs/research/2026-05-25-handoff-failures-evidence.md`. That file was relocated to
**`docs/archive/2026-05-25-handoff-failures-evidence.md`** by the 2026-05-28
ADR-60 archive triage. The original path in the body is retained for historical
accuracy; the current canonical path is the `docs/archive/` one. (Noted: ADR-58 is
the citation-verification decision — this corrects its own broken citation.)
---

## Amendment 2026-05-29 — Superseded by v4

HANDOFF_PROCESS.md was rewritten as v4 on 2026-05-29 as a radical
simplification. v3.x content preserved at protocols/archive/HANDOFF_PROCESS_v3.4.md
for historical reference. The Q1-Q5 architectural concepts captured in this ADR
(claims / scope / probe / manifest / ratification) are simplified in v4:
- Claims -> inline narrative in 04_RECENT, cross-verified by CC in Phase 2
- Scope -> embedded in 05_NOW narrative
- Gate probe -> replaced by operator-side comprehension check at 06_QUESTIONS
- Manifest -> no JSON sidecar; bundle structure declared in README.md
- Ratification -> replaced by operator escalation ladder (Tier 1/2/3)

Decision body preserved as historical record.
