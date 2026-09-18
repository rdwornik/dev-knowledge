# B2 step 2 — calibration: prose bytes per task in three peer harnesses

Measured 2026-09-18 on shallow clones: maister `f75ef4f`, architekt-jutra-code `0a4a90d`, copilot-collections `2fbe51e`. Prose = *.md/*.mdc/*.txt. WITNESSED (python byte sums by the orchestrating seat); the Haiku enumeration's totals were wrong by ~50x and are NOT used.

## Existing audits — still accurate?
- 2026-09-05 architekt-jutra gap analysis — right three repos; no per-task byte count, no "absent" list. Accurate for what it claims; does not answer this question.
- 2026-06-07 copilot-collections peer audit v2, 2026-09-16 lane ab-832 — copilot only; no byte counts.
- 2026-09-15 lane z-11 comparison matrix/packet — matrix of findings, no byte counts.
- So no current audit answers the question, and the repos were read first-hand.

## THE NUMBER — prose a contributor reads for ONE task
- copilot-collections: ~29 KB typical (1 instruction file 1.8 + one prompt median 3.6 + one agent median 8.2 + one skill dir median 15.3); worst case ~110 KB. Total prose 1.54 MB, of which .github 1.04 MB.
- maister: 1.7 KB (quick-dev skill) to ~107 KB (development skill 55.0 + orchestrator-framework 51.6); contributing to maister itself adds 52 KB (two CLAUDE.md files). Total prose 1.82 MB (agents 318 KB, loaded by subagents, not by the main seat).
- architekt-jutra-code: ~1.4–40 KB (CLAUDE.md 1.4 + plugins/CLAUDE.md 15.7 + .claude 22.6). Total prose 7.28 MB, almost all generated task output (.maister 2.3 MB) and course material (tools 4.0 MB, week7–10 0.9 MB), not read before a task.
- .dev-knowledge: 49–653 KB per build-list row on top of a 43 KB boot base; median row 143 KB, so ~186 KB. That is ~6x copilot-collections' typical task and ~1.7x maister's heaviest workflow.
- Delete target for lane 1: a row's read set ≤ ~60 KB including the base.

## What they deliberately do NOT have (existence probes on the clones)
- None of the three has: a pre-commit config, an ADR/decision directory, a backlog file, a lessons file, handoff documents, an ARCHITECTURE document, an AGENTS.md.
- architekt-jutra and copilot-collections have no CI workflows; maister has CI and one plugin hooks.json.
- Only copilot-collections keeps a changelog.
- Their rulings, not their shape: the rules live INSIDE the skill or agent that runs the task and load only when it fires, and nothing is always-on beyond one short instruction file (1.4–4.8 KB). Anything that is not in the task path is not read. They serve a narrower task (one project, one tool) than a fleet hub; the byte gap is still the measurement.

## Leg cost and model
Haiku enumerator 63,484 tokens (step cap 60k total, exceeded by the enumerator alone). The Sonnet synthesis was NOT launched; the seat synthesised from deterministic measurements instead. The orchestrating seat RAN Opus 5 (session model) though the primary session was ordered Sonnet — the build-list row "model: ORDERED vs RAN" records it.
