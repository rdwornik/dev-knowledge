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

## Amendment — 2026-06-24: deterministic build-task acceptance contracts (test-first, frozen, immutable-to-CC)

**What this generalizes.** Item (d) requires "actual deployment, OR an explicit documented deferral" — but for a **deterministic build task** it left *how "done" is proven* implicit, so "done" defaulted to the easy proxy (unit tests pass / branch merged). This amendment sharpens (d) for that case: a deterministic build is **not done until it meets an executable acceptance contract that the architect authored *before* the build, shipped FROZEN as a first deliverable, immutable to the executor** — and **closure is declared on that contract (the HARD metric — the end-state meets the function-of-goal), not on "tests pass / merged."** Generalized from one proven exemplar — **#194 Phase-A**, the xfail-strict coverage test whose failing output *is* the rollout inventory, committed before any annotation; the xfail-strict decorator made a premature green *fail*, which is the immutability property in action.

**The contract.** For a deterministic build task the architect emits, upstream of the executor: the **executable pass/fail criterion** that proves the function-of-goal (a test / assertion / check — Given/When/Then + I/O examples where they apply) + the **closure criterion** (what state the criterion must reach). It is **frozen**: the executor (CC) **may strengthen it — add cases, tighten assertions — but never weaken the gate** (no assertion removal, input-specific branching, or scope-narrowing). Review **verifies the contract was not gamed** (assertions are the originals; scope is not narrowed) — green status alone does not close. The *"declare on the hard metric, not the easy one"* doctrine this operationalizes is **already resident** in PLAYBOOK Ch12.1 "Definition of shipped" (the six-point ex-post gate); this amendment adds the **ex-ante / test-first** property — the criterion exists, and is frozen, *before* the build — and is mirrored there.

**Scope — deterministic only; fuzzy deferred.** This binds **deterministic build tasks**, where "done" can reduce to an exact, executable assertion. The **fuzzy band** — decks, prose, judgment artifacts where closure cannot be an exact pass/fail — is **explicitly deferred to its own arc** (it needs a different, non-binary acceptance shape). Naming the deferral here keeps it honest rather than silently over-claiming.

**Relationship to original text.** The four-point bar (a)–(d) and its intent are **unchanged**; this sharpens (d)'s notion of "done/deployed" for the deterministic-build case only. It is the methodology codification of audit finding **A2** (`docs/audits/2026-06-23-handoff-process-audit-findings.md` §5/§9). Doctrine home: **PLAYBOOK Ch12.1**; the session-close scope (`protocols/DEFINITION_OF_DONE.md`, ADR-85) carries only a thin scope-pointer to it — it is **build/arc** discipline, not a session-end Stop-gate. **Advances #144** (which folds this requirement in); #144's residual E2E/user-flow specificity + the "in the cloud" (CI vs cloud-CC) execution-location VERIFY-FIRST remain open.

## Amendment — 2026-07-03: leg (e) functional-proof (Fable consult #1 ruling)

**What this adds.** A fifth leg to the done-bar. Fable consult #1 (2026-07-03, architect-ratified) established that build+test+deploy is still insufficient when the organ's job is to *enforce*: an enforcement mechanism that is present and conformant but never demonstrated to fire is not done. This generalizes the 2026-06-24 amendment's hard-metric discipline from the deterministic-build case to every enforcement mechanism.

**Leg (e) — functional proof.** A mechanism (organ / gate / hook / enforcement rule) is not done on presence or configuration alone. Closure requires demonstrated enforcement-in-effect — a functional proof that the mechanism fires: a test observing the gate block/trigger, or an observed in-situ firing, not evidence that the artifact is present or conforms. Presence-conformance is necessary but not sufficient; demonstrated firing is the sufficient condition. Generalizes the 2026-06-24 hard-metric amendment from deterministic builds to every enforcement mechanism.

**Effect on the bar.** The done-bar is now **five points, (a)–(e)**. This **supersedes** the 2026-06-24 amendment's "The four-point bar (a)–(d) and its intent are **unchanged**" line (§Amendment 2026-06-24, "Relationship to original text") — the earlier bar (a)–(d) and its intent are still binding, but the bar is now (a)–(e), and (e) applies specifically to enforcement mechanisms. Legs (a)–(d) are unmodified.

**Doctrine home (leg (b) for this leg itself).** Mirrored into PLAYBOOK § "Definition of done (organs)" so leg (e) has its own methodology home.
