# Technical lane ab-832 — three-repo methodology comparison

**Date:** 2026-09-16  
**Scope:** `Architekt-Jutra/architekt-jutra-code`, `SkillPanel/maister`, `TheSoftwareHouse/copilot-collections`, compared with `.dev-knowledge`  
**Producer:** Copilot Enterprise, execute mode  
**External anchor:** `docs/audits/2026-06-07-copilot-collections-peer-audit-v2.md`  
**Fresh clone:** `TheSoftwareHouse/copilot-collections` at `2fbe51e31c8006e5a330c624264af112a19ec54d` (shallow clone, latest commit 2026-08-05)  
**License note:** the fresh clone carries MIT, © 2026 The Software House, in `LICENSE`.

## What changed

The earlier comparison selected the wrong three external repositories. This rerun uses the
operator's named repositories. `architekt-jutra-code` and `maister` are not re-read from
scratch: their evidence is carried from the first-hand 2026-09-10 bundle, principally
`docs/audits/2026-09-10-technical-night-aj-m03/MATRIX.md` §1c and
`docs/audits/2026-09-10-technical-night-aj-m03/1b-ajcode.md`. Only the matrix-dependent
claims are carried forward.

The fresh clone is materially newer than the 2026-06-07 anchor. Its 2026-06-01 BA entry is
still present, but later commits changed the implementation orchestration route: Quick Flow
was removed, Full Flow became the only route, and the owner-routing table was expanded
(`.github/skills/tsh-orchestrating-implementation/SKILL.md`; `CHANGELOG.md:1-21`).

## Fresh-clone claim diff against the 2026-06-07 audit

Each claim from the anchor is classified as **still true**, **changed**, or **gone**. Every
classification names a path in the fresh clone at the SHA above.

| Anchor claim | Verdict | Fresh-HEAD evidence |
|---|---|---|
| Copilot/VS Code carrier is repo instructions plus scoped instruction files | still true | `.github/instructions/naming-conventions.instructions.md`; `.github/agents/`; `.github/prompts/`; `.github/skills/` |
| Skills are folders with `SKILL.md`, agents are `.agent.md`, prompts are `.prompt.md` | still true | `.github/skills/tsh-creating-skills/SKILL.md:10-17`; `.github/agents/tsh-business-analyst.agent.md`; `.github/prompts/tsh-analyze-materials.prompt.md` |
| `tsh-explore-materials` is an Explore Mode that emits readiness context before extraction | still true | `.github/prompts/tsh-explore-materials.prompt.md:5-18`; `.github/agents/tsh-business-analyst.agent.md:55-63` |
| BA was reworked into an orchestrator with five isolated workers and orchestrator-owned writes | still true | `.github/agents/tsh-business-analyst.agent.md:15-31`; `.github/agents/tsh-ba-analysis-worker.agent.md:1-45` |
| Workers return in memory and do not own Jira access or file writes | still true | `.github/agents/tsh-business-analyst.agent.md:15-31`; `.github/agents/tsh-ba-formatting-worker.agent.md:9-45` |
| Gate 0, Gate 1, Gate 1.5, Gate 2 and post-push verification remain in the BA path | still true | `.github/agents/tsh-business-analyst.agent.md:76-95`; `.github/prompts/tsh-analyze-materials.prompt.md:30-86` |
| The 2026-06-01 changelog entry is the only post-05-31 BA delta | changed | `CHANGELOG.md:1-21` contains later orchestration changes; the 2026-06-01 entry remains at `CHANGELOG.md:185-190` |
| Skills use gerund names and progressive disclosure | still true | `.github/skills/tsh-creating-skills/SKILL.md:26-54`; `.github/skills/tsh-creating-skills/SKILL.md:68-116` |
| The skill-authoring scaffold, examples and references exist | still true | `.github/skills/tsh-creating-skills/skill.template.md`; `.github/skills/tsh-creating-skills/examples/reviewing-code.skill.md`; `.github/skills/tsh-creating-skills/references/common-patterns.md` |
| XML is used for bounded structure and Markdown for sequences | still true | `.github/skills/tsh-creating-skills/SKILL.md:55-66` |
| `tsh-` namespace prefix remains pervasive | still true | `.github/agents/`, `.github/prompts/`, `.github/skills/` |
| `applyTo` scoped instructions remain a Copilot-specific carrier | still true | `.github/instructions/naming-conventions.instructions.md:1-8` |
| Multi-model per-agent selection is present | changed | `.github/agents/tsh-business-analyst.agent.md:35-46` and `.github/agents/tsh-engineering-manager.agent.md` carry model arrays, but the exact model names and assignments differ from the June description |
| Jira/Atlassian/Figma MCP-heavy BA flow remains | still true | `.github/agents/tsh-business-analyst.agent.md:2-4`; `.vscode/mcp.json`; `.github/prompts/tsh-analyze-materials.prompt.md:5-7` |
| `vscode/askQuestions` is used for human gates | still true | `.github/agents/tsh-business-analyst.agent.md:2-4`; `.github/skills/tsh-creating-skills/SKILL.md:91-116` |
| Technical Context is persisted in implementation plans | still true | `.github/skills/tsh-creating-implementation-plans/plan.example.md:70-80` |
| Human approval is persisted as a revision-bound plan record | still true | `.github/skills/tsh-creating-implementation-plans/plan.example.md:45-69` |
| Explore readiness avoids creating backlog items until continuation | still true | `.github/prompts/tsh-explore-materials.prompt.md:12-18` |
| The external collection has a public onboarding/distribution surface | still true | `README.md`; `website/docs/getting-started/`; `website/docs/intro.md` |
| The collection contains roughly twenty domain implementation skills | changed | The named domain families remain under `.github/skills/`, but the anchor's approximate count is a June measurement and is not re-stated as a current count |
| The anchor's recommended-against `tsh-`, `applyTo`, and XML patterns are unchanged | still true | `.github/instructions/naming-conventions.instructions.md`; `.github/skills/tsh-creating-skills/SKILL.md:55-66`; `.github/agents/` |
| The anchor's `conformance-hub.js` verification claim concerns this repo, not TSH | not applicable | The anchor's own addendum is about `.dev-knowledge`; no TSH clone path can verify it. The current repo-side evidence remains the cited `.claude/workflows/conformance-hub.js` in that addendum. |

No anchor claim was found to be **gone** in the fresh clone. Claims whose exact historical
count or model spelling no longer applies are marked **changed**, not silently carried.

## Capability matrix

Cell vocabulary is deliberately strict: `has (path)`, `lacks`, or `partial (what)`. A claim
without a checkable path is `unverified`, never `has`.

| Capability | architekt-jutra-code | SkillPanel/maister | copilot-collections @ `2fbe51e` | `.dev-knowledge` |
|---|---|---|---|---|
| Per-task state carrier | has (`.maister/tasks/development/.../orchestrator-state.yml`, cited in `MATRIX.md` §1c) | partial (the plugin describes `orchestrator-state.yml`, but the 2026-09-10 verification found no writer; `MATRIX.md` §1c) | lacks (the collection defines `specifications/<task>/` artifacts but no committed per-task execution-state carrier; `.github/agents/tsh-business-analyst.agent.md:15-31`) | partial (task frontmatter carries identity and queue metadata but not execution position or phase results; `MATRIX.md` §1c; `tasks/README.md`) |
| Conditional phase routing | has (`.maister/tasks/.../SUMMARY.md`, cited in `MATRIX.md` §1c) | has (`plugins/maister/skills/development/SKILL.md`, cited in `MATRIX.md` §1c) | has (`.github/skills/tsh-orchestrating-implementation/SKILL.md`, planning-readiness and Task-to-Owner Routing tables) | partial (the lane contract and batch protocol route work, but task characteristics do not select a persisted phase graph; `MATRIX.md` §1c) |
| GO/NO-GO artifact | has (`.maister/tasks/.../verification/reality-check.md`, cited in `1b-ajcode.md`) | partial (verification artifacts exist, but the cited first-hand matrix attributes the committed NO-GO example to repo B rather than this source) | partial (human approvals and STOP behavior are persisted for plans, but no deployment-style GO/NO-GO artifact is defined; `.github/skills/tsh-creating-implementation-plans/plan.example.md:45-69`) | lacks (operator GO is a protocol step without a per-task carrier; `MATRIX.md` §1c; `protocols/PLAYBOOK.md:6068`) |
| Per-task work log | has (`.maister/tasks/.../implementation/work-log.md`, cited in `1b-ajcode.md`) | partial (workflow artifacts describe progress, but the first-hand matrix does not verify an append-only work-log instance for the plugin) | partial (plan/task artifacts and changelog exist, but no per-task append-only work-log contract is defined; `.github/skills/tsh-orchestrating-implementation/SKILL.md`) | lacks (institutional ledgers are repo-level, not per-task; `MATRIX.md` §1c; `JOURNAL.md`) |
| Model-boundary PII/secret filter | has (`litellm/config.yaml`, Presidio guardrails, cited in `MATRIX.md` §1c) | unverified (the 2026-09-10 bundle provides no verified path for this capability) | lacks (no fresh-clone PII gateway or secret-filter path found; `.vscode/mcp.json` only declares tool connections) | lacks (no model gateway in the hub; `MATRIX.md` §1c) |
| CI | lacks (no workflow, cited in `1b-ajcode.md`) | unverified (not re-read; no matrix-dependent CI path is cited) | lacks (no `.github/workflows/` in the fresh clone) | partial (pre-commit, commit-msg and pre-push gates, but not hosted CI; `.pre-commit-config.yaml`; `MATRIX.md` §1c) |
| Agent hooks | partial (`.maister` command/skill routing is cited; no repository-level Claude hooks, `1b-ajcode.md`) | partial (plugin hooks exist, but the matrix found no hook that mechanically writes state; `MATRIX.md` §1c) | partial (agent tool declarations and handoffs exist, but no executable hook layer; `.github/agents/tsh-business-analyst.agent.md:2-4`) | has (`.pre-commit-config.yaml`; `.claude/settings.json`; `MATRIX.md` §1c) |
| Mechanical enforcement | lacks (instruction-driven workflow; `1b-ajcode.md`) | lacks (phase state is instruction-level; `MATRIX.md` §1c) | partial (planning and approval predicates are explicit and auditable, but instruction-level rather than repository gates; `plan.example.md:45-69`) | has (commit-time refusal gates and audit health; `.pre-commit-config.yaml`; `MATRIX.md` §1c) |
| Isolated worker orchestration | has (standalone agents with isolated context, `1b-ajcode.md`) | has (14-phase workflow and delegated agents, `MATRIX.md` §1c) | has (`.github/agents/tsh-business-analyst.agent.md:15-31`; worker agent files) | has (isolated verifier fan-out, skeptic and digest; `.claude/workflows/conformance-hub.js`, anchor addendum) |
| Skill-authoring scaffold | unverified | unverified | has (`.github/skills/tsh-creating-skills/skill.template.md` and examples) | lacks (`templates/` has no equivalent scaffold, anchor §3.6) |
| Technical-context re-anchor before implementation | partial (standards are mandatory in `1b-ajcode.md`) | has (mandatory skill-driven development workflow, `MATRIX.md` §1c) | has (`.github/skills/tsh-technical-context-discovering/SKILL.md`; `tsh-orchestrating-implementation/SKILL.md`) | partial (session-start read and handoff protocol; `CLAUDE.md §6`, anchor §3.5) |

## Triage

Every finding in which an external surface has shape that this repo lacks is assigned exactly
one ADR-111 disposition. No new backlog row is filed by this audit.

| Finding | Disposition | Reason |
|---|---|---|
| Machine-readable per-task execution state (`phase`, attempts, skipped gates, risk) | CANDIDATE | Valuable shape appears in AJ/Maister evidence, but adoption needs an explicit design and an open row before filing. |
| Per-task GO/NO-GO artifact | CANDIDATE | The current protocol records operator GO without a durable task artifact; the external pattern is concrete and bounded. |
| Append-only per-task work log | CANDIDATE | A task-local log would complement, not replace, the repo-level JOURNAL; no existing open row owns it. |
| Conditional phase routing persisted with task state | CANDIDATE | External routing is richer than the current hand-composed lane shape, but adoption must not create a second orchestration engine. |
| Skill-authoring scaffold and examples | CANDIDATE | The fresh clone proves the scaffold pattern is concrete; it is not present under this repo's `templates/`. |
| Mid-session technical-context re-anchor | CANDIDATE | The pattern is stronger than our session-start-only read, but the cited historical #121 is not open in the current BACKLOG view, so this audit does not claim ownership. |
| PII/model gateway | REJECTED | A runtime model gateway is outside this Layer-2 governance hub; the external capability is a child-repo/runtime concern, not a hub surface. |
| Hosted CI in the comparison repos | DISCHARGED | Neither the fresh TSH clone nor the verified AJ evidence has CI; `.dev-knowledge`'s local gate model is a deliberate carrier difference, not a one-sided gap. |
| `tsh-` namespace, `applyTo` scoping, and XML tags | REJECTED | The anchor's recommended-against verdict still holds: these solve Copilot/team-scale mechanics with no demonstrated benefit for this solo Claude-Code hub. |
| Large domain-specific agent/skill roster | REJECTED | The small-roster doctrine and Layer-2 boundary reject headcount parity; importing the collection's implementation library would add breadth without a hub-owned trigger. |

## To file

The following are CANDIDATEs only; they are intentionally not added to `tasks/` by this lane:

- A machine-readable per-task execution-state carrier with phase, attempts, skipped gates and risk.
- A per-task GO/NO-GO artifact bound to the lane/task lifecycle.
- An append-only per-task work log.
- Conditional phase routing persisted with the state carrier.
- A `templates/SKILL-scaffold.md`-style skill-authoring scaffold with examples/references.
- A mid-session technical-context re-anchor mechanism, designed without duplicating the session-start contract.

## Open items and limits

- The AJ and Maister cells are bounded carry-forward evidence from the 2026-09-10 bundle, not
  fresh clones; that is required by the frozen contract.
- The TSH clone has no hosted CI workflow and no runtime PII gateway. The matrix therefore does
  not infer those capabilities from tool declarations or prose.
- The fresh clone is MIT-licensed. Any future verbatim adaptation would need to retain its
  license and copyright notice; this audit copied no source text beyond short evidence quotes.
- The approximate skill count in the June anchor is not re-measured because it is not a
  capability threshold and would add a stale number rather than evidence.
