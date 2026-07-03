# ADR-95: AI-council query lane-split — architect frames, CC mechanically expands

- **Status:** Accepted
- **Date:** 2026-07-03
- **Decision tier:** Architecture (Path A — direct architect ruling, Fable consult #1; no Council transcript, like ADR-87/90/92)
- **Related:** ADR-67 (AI-council process operationalization — the six-step gated loop this specializes), ADR-87 (Architect↔CC equilibrium contract — the general lane-split this is the ai-council-query instance of), ADR-91/92 (corpus versioning + deploy-runbook — the deployment channel to the `ai-council` repo)
- **Source:** Fable consult #1, 2026-07-03 (architect-ratified). Consult chat expired; this records the accepted ruling.
- **Decommission:** none

## Context

ADR-67 defines the AI-council operational loop (Frame → Generate → Gate → Run → Verdict→ADR → Deterministic return; trigger `/council-question`, implemented in the `ai-council` repo). ADR-87 established the general Architect↔CC equilibrium: the architect emits intent / closure / anti-patterns / governance-pointer, and CC owns the mechanical skeleton, code-impact context, and generic gotchas.

A specific division of labor for the **ai-council-query** case was left implicit: when a council question is being prepared, who owns *what the question asks* versus *how it is expanded into the templated, gate-ready query artifact*? Left unstated, this drifts — CC either under-expands (the question loses the framing the architect intended) or over-reaches (CC re-frames the substance, not just the mechanics).

## Decision

For the ai-council query lifecycle, the lane-split is:

- **The architect frames the question** — the substance: what is being asked, why, the decision at stake, the forks, the evidence to weigh, the closure criterion. This is the ADR-67 "Frame" step's content, and it is the architect's, not CC's.
- **CC mechanically expands** — the templated query artifact: fitting the framed question into the ADR-67 template, assembling the gate-ready payload, wiring the deterministic return, running the lifecycle mechanics. CC does not re-frame the substance; it expands the architect's framing into the runnable form.

This is the **ai-council-query specialization of ADR-87's equilibrium contract** — the same "architect emits intent, CC owns the mechanical skeleton" division, applied to the council-question channel. Question-framing is intent (architect-owned, will not self-infer); query-expansion is skeleton (CC-owned, mechanical).

## Consequences

- **Easier:** the boundary is explicit, so a council question doesn't lose its framing to CC over-expansion nor stall on CC waiting for a fully-formed artifact. The architect writes intent; CC produces the runnable query.
- **Cost / scope:** this is **record-only**. It states the principle; it does **not** build the `/council` (or `/council-question`) wiring — that wiring is sequenced-after and owned by the `ai-council` repo (ADR-67; PLAYBOOK §"AI Council"). No mechanism is created here.
- **Relation to ADR-87:** ADR-87 is the general contract; this is one instance. If ADR-87's division is later revised, this specialization inherits the revision.

## Alternatives considered

- **Leave it implicit under ADR-87.** Rejected: the ai-council-query case recurred as a concrete framing-vs-expansion ambiguity worth naming, so a fresh session applies the split without re-deriving it — the same reason ADR-90 recorded an already-decided scheme as its own ADR.
- **Build the wiring here.** Out of scope: the ruling is record-only; the `/council-question` mechanism lives in `ai-council` (ADR-67) and is sequenced-after. Building it here would violate the record-only ruling and the Layer-2 no-orchestration invariant.
