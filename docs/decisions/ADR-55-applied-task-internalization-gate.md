# ADR-55: Applied-task internalization gate

- **Status:** Accepted
- **Date:** 2026-05-26
- **Related:** ADR-42 (handoff format v3 — the gate lives in its `00_first-message.md`), ADR-56 (Prompt Generation Card), ADR-58 (structured claims — operator ratification flow), `protocols/HANDOFF_PROCESS.md` (operational counterpart)
- **Decommission:** the 4-item paraphrase articulation gate in `templates/HANDOFF_FOLDER_TEMPLATE.md` `### 00_first-message.md` (replaced by the applied-task gate in this session's Phase C template amendment)
- **Source:** AI Council debate Q1, 2026-05-26 — `docs/decisions/transcripts/council-out-20260526_142806-pick-2026-05-25-handoff-council-Q1-internalization-assurance.md` (Recommended Decision L796-862; Action Items L864-898)

## Context

The current handoff gate asks the NEW chat to paraphrase four items (role per
VISION, current phase, next action, top-3 hard constraints) in its own words,
then waits for the operator to type `role confirmed`. This gate failed
empirically.

- `docs/research/2026-05-25-handoff-failures-evidence.md` documents two NEW chats
  that **passed** the paraphrase gate then **could not operationalize** the same
  bundle content one turn later: "bundle delivered standards; NEW chat could
  paraphrase them at articulation gate; could not operationalize them when
  operator asked for substantive grounding."
- Root mechanism (evidence file, Cross-actor pattern): "plausible-output
  generation outpaced verified-grounding. Articulation gates that asked
  'paraphrase X' were satisfiable by pattern-match; substantive work that
  required 'use X to make decision Y' exposed that internalization hadn't
  happened."

The observed failures are **application** failures, so the gate must test
application, not retrieval.

## Decision

Replace the 4-item paraphrase gate with an **applied-task proof gate**, delivered
in a single upload, with one bounded retry.

- **Grounding check (citation-anchored).** The NEW chat states its role per VISION
  and the top-3 hard constraints, each with a file/section citation. Anchor is
  file + heading/section — not mandatory line-number precision (avoids citation
  brittleness).
- **One mandatory applied probe.** A concrete mini-scenario whose correct answer
  is determined by the bundle. The answer must include: (a) the directed action,
  (b) the controlling bundle location, (c) any preconditions or sequencing
  dependencies. The probe and a receiver-invisible expected answer ship as a
  required bundle artifact, `10_GATE_PROBE.md`.
- **Operator confirmation against an answer key.** The operator confirms only
  after checking the probe answer against the operator-only expected answer.
  Bare `role confirmed` is replaced by `role confirmed + probe passed`.
- **Failure protocol.** First failure → operator points to the contradicted
  bundle location, NEW chat re-reads and retries once. Second failure → terminate
  the attempt, treat the bundle as inadequate, regenerate/refine upstream.
- **Minimal operator audit trace.** Record which citation was checked, whether
  the probe answer matched, and whether a retry was needed (Stage 3 checklist in
  `HANDOFF_PROCESS.md`).

**Deviation from Council action item AI3.** The transcript names the artifact
`08_GATE_PROBE.md`; the bundle already uses `08_TREE.txt`. Per operator decision
2026-05-26 the artifact is numbered `10_GATE_PROBE.md` (no renumber of existing
files).

## Consequences

- The gate now tests whether the NEW chat can *use* bundle content to decide an
  action — the failure mode the evidence actually showed.
- One bounded retry is a low-cost diagnostic step; it prevents needless
  regeneration on transient misses without letting a poisoned session run on.
- Repeated gate failure is reframed as a *bundle* problem (unclear/inconsistent),
  not only a receiver problem — triggers upstream regeneration.
- New per-handoff authoring cost: the sender must write a probe + answer key.
  Mitigated by a structured probe template (`### 10_GATE_PROBE.md`) and operator
  review of early handoffs.
- Implemented as a template/process amendment, not a new automated architecture
  (no Layer-2 orchestration code).

## Risks (from Q1 risk register, L842-862)

- **Poor probe quality** (generic/ambiguous/too easy) → require structured probe
  template + operator-visible expected answer; review early handoffs.
- **Operator rubber-stamping** under time pressure → require the minimal
  confirmation record above.
- **Bundle contradictions masquerading as reader failure** → treat repeated gate
  failure as a bundle problem; regenerate upstream.
- **False confidence from a too-narrow probe** → choose the probe from the
  highest-risk live decision in the handoff; if post-gate failures persist,
  expand to two probes covering different rule types.
- **Citation brittleness** → use file + section/header as default anchor unless
  stable line refs already exist.

## Alternatives considered

- **Retrieval-only / keep paraphrase gate** — rejected: the evidenced failures
  were application failures; retrieval is too weak.
- **Immediate kill on first fail** — rejected: too aggressive given no proof one
  correction attempt is usually useless.
- **Multi-stage sequential loading** — rejected: adds cost without evidence.

## Trace

Measurement plan (pass/fail rate, retries, post-gate failures over 5-10 handoffs)
is deferred to a BACKLOG measurement entry per Council AI6 — triggered
post-rollout, not this session.

---

## Amendment 2026-05-29 — evidence file relocation

> Append-only reference correction per ADR-39 (immutable body preserved). Grounds:
> `docs/audits/2026-05-29-handoff-v3.4-process-audit.md` finding E1.

The Context section above cites the empirical-basis evidence file at
`docs/research/2026-05-25-handoff-failures-evidence.md`. That file was relocated to
**`docs/archive/2026-05-25-handoff-failures-evidence.md`** by the 2026-05-28
ADR-60 archive triage. The original path in the body is retained for historical
accuracy; the current canonical path is the `docs/archive/` one.
