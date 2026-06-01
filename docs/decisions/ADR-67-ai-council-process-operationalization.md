<!-- scope: meta -->

# ADR-67 — AI-Council process operationalization

**Status:** Accepted — 2026-06-01, **Path A** (operator-chosen; no Council convene — a process
formalization of an already-running loop, not an architectural decision).
**Amends:** `protocols/AI_COUNCIL_PROCESS.md` v1.0 (the process spec; no dedicated originating ADR
exists — v1.0 closed a BACKLOG item as a companion to ARCHITECTURE.md C3; related authority ADRs:
ADR-43 cross-project routing, ADR-60 folder taxonomy).

## Context

The Council loop works but carries manual friction and quality variance. As of v1.0 the loop
is documented but not gated:

1. **Context gap** — providers see one question with little of the evolving, cross-referencing ADR
   corpus. A bare question underperforms because Council has no ADR-corpus memory; context must be
   carried per-question.
2. **Manual file-shuttling** — "where's the file" steps at both ends (dropping into `council_inbox/`
   and picking up the output transcript) are undocumented and error-prone.
3. **No question-quality gate** — nothing prevents a poorly framed question (leading headline,
   asker-leakage, false dichotomy) from reaching the panel.

The `HANDOFF_PROCESS` (ADR-42, ADR-62) solved analogous friction with a defined, gated,
deterministic loop. The Council process should mirror that pattern.

## Decision

Formalize the AI-Council process as a **six-step gated loop**:

1. **Frame** — state the one decision/problem to resolve (one sentence; two questions = two debates).
2. **Generate (templated)** — Claude Code fills a Council-question template that mandates the
   context Council lacks: exactly one decision asked, the options, the constraints/invariants, and
   the relevant prior ADRs (cited or summarized inline). Template lives in `ai-council` (see
   "Where each piece lives").
3. **Gate** — the filled question is validated against the template before release: required
   sections present, exactly one decision, options enumerated, ADR context attached. Fail → fix
   before running. Mirrors the BACKLOG validator / handoff articulation gate. Gate check lives in
   `ai-council`.
4. **Run** — `council` consumes the gated question from the `ai-council` inbox; output → output
   folder per the existing Stage 3 mechanics.
5. **Verdict → ADR** — the operator pastes the verdict; Claude Code drafts an ADR from it in the
   target repo (per existing Stage 5 mechanics).
6. **Deterministic return** — the ADR is written to the operator's return directory held in
   `~/.claude` global config (`council.return_dir`), and Claude Code ingests it from that known
   path. No relocation guesswork.

**Trigger (symmetry with `wygeneruj handoff`):** `/council-question` — Claude Code generates
the templated question and self-gates it. Operator reviews, then drops into the inbox.

### Where each piece lives (cross-domain separation)

| Piece | Domain | Downstream work |
|-------|--------|-----------------|
| Process spec + this ADR | `.dev-knowledge` | This ADR + updated `AI_COUNCIL_PROCESS.md` |
| Council-question template + gate check + known-path I/O | `ai-council` | Separate session, implements ADR-41 + this ADR's contract |
| Return-dir path | `~/.claude` global config (`council.return_dir`) | Separate session; NOT `.secrets/.env` — a path is runtime config, not a secret |

The three-domain separation is the same pattern as `HANDOFF_PROCESS`: process doc here,
implementation in the tool repo, runtime config in `~/.claude`.

## Consequences

- **Friction down** — deterministic I/O replaces manual file-shuttling at both ends.
- **Question quality up** — template + gate closes the context gap and prevents leading/biased
  questions from reaching the panel.
- **Context gap closed** — mandated ADR-context section in the template carries what Council
  cannot hold across questions.
- **Cost:** one template + one gate check to maintain in `ai-council`; one `~/.claude` config key.
  Council itself stays stateless — the template carries context per-question (correct: providers
  have no ADR-corpus memory and should not; per-question context is the safe pattern).

## Alternatives considered

- **Leave v1.0 as-is (no gate)** — rejected: the context gap and file-shuttling friction are
  recurring; this is the same asymmetric risk (low-cost fix vs. repeated friction) that drove the
  handoff gate (ADR-55/56/57/58).
- **Gate in `.dev-knowledge` (this repo)** — rejected: ADR-28 layer invariant. This repo holds
  process specs, not executable gate logic. Validators live in `scripts/` (read-only) or in the
  tool repo that owns the artifact.
- **Council convene** — not taken: a process formalization of a running loop, operator-confirmed;
  Path A per ADR-65 precedent.

## Dependencies

This ADR defines the contract (template fields + gate rules + return path). The `ai-council`
implementation and the `~/.claude` config key are downstream — they implement what this specifies.
This ADR is complete when `AI_COUNCIL_PROCESS.md` encodes the loop; the downstream pieces are
tracked separately in the respective domain BACKLOG/config files.

## References

- `protocols/AI_COUNCIL_PROCESS.md` (v1.0 — amended by this ADR)
- `HANDOFF_PROCESS.md` + ADR-42/55/56/57/58/62 (the gated-loop pattern this mirrors)
- ADR-43 (`cross-project transcript routing` — unchanged by this ADR)
- ADR-60 (folder taxonomy, ephemeral briefs — unchanged)
- ADR-28 (three-layer invariant — grounds the cross-domain split)
