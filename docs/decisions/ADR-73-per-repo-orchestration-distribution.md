<!-- scope: meta -->

# ADR-73 — Per-repo orchestration distribution; canonical template stays hub-side; propagation at rollout moments

- **Status:** Accepted — 2026-06-06 (ratification date)
- **Amends:** ADR-72
- **Related:** BACKLOG #86 (sub-decision 3); ADR-72
- **Decommission:** none
- **Source:** Operator ruling via paste-=-consent (corp routine-build prompt); recorded corp-monorepo JOURNAL 2026-06-06. Form (companion ADR) ruled by operator via paste-=-consent in this prompt, 2026-06-06.

## Context

ADR-72 establishes cloud-routine self-containment — a cloud session sees only the cloned repo. That forces the question of where routine orchestration lives for each cloud-routine repo (#86 sub-decision 3). Per-repo copies stand in tension with the ownership-cadence principle (one canonical owner per artifact).

## Decision

(a) Each cloud-routine repo carries its **own adapted orchestration, committed in-repo**; (b) the **hub remains the canonical template** for the local loop; (c) **propagation happens at rollout moments, in both directions** — hub→child template updates, child→hub back-ports of superior implementations.

## Consequences

The tension with ownership-cadence is **accepted consciously and citable by number**, with a named mitigation (canonical template + rollout-moment propagation). Precedent already exercised: corp→hub back-ports `cfdcc31`, `e9c9e6a`. Cost: copies can drift between rollouts; watched by the nightly conformance loop and back-port discipline.

## Alternatives considered

Hub-distributed central orchestration — rejected; puts a hub reference on a cloud executing path, violating ADR-72.
