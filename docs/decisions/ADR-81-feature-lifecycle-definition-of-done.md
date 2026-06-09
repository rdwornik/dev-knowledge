# ADR-81: Feature-lifecycle definition of done (organs)

- **Status:** Accepted
- **Date:** 2026-06-09
- **Related:** ADR-80 (two-tier automation adoption — "What every routine must meet" is the routine-scoped analog this generalizes); ADR-70 (the organ taxonomy: plugin / hook / command / skill / workflow)
- **Decommission:** none
- **Source:** Rob's decision, 2026-06-09 (this session; no Council debate — Council deferred)

<!-- Decommission: none -->

## Context

The ecosystem has repeatedly built organs — plugins, hooks, commands, skills, workflows, generators, conventions — that passed build-and-test and were then treated as "done," while lacking a written rule, a deployment path, a refresh cadence, or actual deployment. The result is **half-feature rot**: a built artifact that no doctrine references, that nothing installs, that no one keeps current, and that may never have shipped.

ADR-80's "What every routine must meet (the operational standard)" already encodes a definition-of-done for one organ class (recurring unattended routines). The same discipline was missing as a *general* rule spanning every organ class.

## Decision

An organ — a plugin, hook, command, skill, workflow, generator, or convention — is **not DONE** until it has all four:

- **(a) a methodology home** — its rule/doctrine written in PLAYBOOK;
- **(b) a deployment path** — a runbook or documented install sequence;
- **(c) a maintenance/refresh cadence** — how it stays current, and how staleness is detected;
- **(d) actual deployment, OR an explicit documented deferral** that names the gap and what remains.

Stopping at build+test is the half-feature rot trap: **build-and-test ≠ done.** The doctrine is recorded in PLAYBOOK § "Definition of done (organs)".

## Consequences

- **Easier:** a uniform completion bar across all organ classes — "is this done?" becomes a four-point check, not a judgment call. Deferrals become explicit and named rather than silent gaps a later audit must rediscover.
- **Harder / cost:** more up-front work to declare a home, a deploy path, and a cadence before an organ counts as done; some genuinely-experimental organs will sit in an "explicit deferral" state, which must be honestly recorded rather than quietly skipped.
- **Relation to ADR-80:** generalizes ADR-80's routine-scoped operational standard to every organ class; the routine standard remains the specialized instance for recurring unattended reviews.

## Alternatives considered

- **Leave it as a routine-only standard (ADR-80).** Rejected: the half-feature pattern recurred across non-routine organs (commands, generators, conventions), so the bar needed generalizing.
- **Three-point bar (drop the deferral clause).** Rejected: without an explicit-deferral escape valve, the rule would either be ignored for experimental work or force premature deployment; the named-deferral clause keeps it honest and usable.
