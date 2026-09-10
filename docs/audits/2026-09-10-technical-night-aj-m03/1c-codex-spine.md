# 1c - adversarial spine derivation: Maister vs ours

**Reader:** codex - **ORDERED**, invocation CORRECTED once. Not a substitution.
**Model:** gpt-5.6-sol (confirmed in the run banner; the configured default gpt-6-astra returns HTTP 400 on this CLI version).

**First attempt FAILED TO DELIVER.** `codex exec -c model=gpt-5.6-sol -s danger-full-access "<...write the answer to out/1c-codex-spine.md>"` ran to completion, spent **85,017 tokens**, exited 0, and then refused:

> BLOCKED: Repository policy restricts Codex to read-only review, so I cannot create the requested output file.

That is **our own L0 doctrine** - the read-only reviewer role in `~/.codex/AGENTS.md` that this repo's `AGENTS.md` "Precedence" section names - not a provider fault and not an auth fault. The derivation was performed and discarded, and the caller learned of the constraint only after paying for it.

**Exact invocation (the one that delivered):** `codex exec -c model=gpt-5.6-sol -s danger-full-access "<same derivation, but: READ-ONLY - do not create or modify any file. PRINT your entire answer to stdout>"`
**Wall time:** ~7 min. **Tokens:** 92,866.
**Adversarial conditions honoured:** the prompt forbade reading DECLARE-HARNESS-IS-PROCESS or any audit stating a conclusion about either spine, and required independent derivation BEFORE comparison.

## R2 status: VERIFIED, with three corrections - and one finding that overturns this file's framing

Every locator below was checked line-by-line against both source trees by a CC verification subagent.
**All fourteen Maister phase locators CONFIRMED. All eight PLAYBOOK spine locators CONFIRMED.**

Three defects found, carried rather than dropped:

1. **`SKILL.md:559` is WRONG as cited.** It is only the intro line to the domain-extension field block. The routing flags, option flags and risk/architecture fields ARE real, at 561-608 - but `completed_phases`, `failed_phases` and `auto_fix_attempts` live in a DIFFERENT file, `orchestrator-framework/references/orchestrator-patterns.md` ~218-236. The claim's substance survives; its single-locator citation does not.
2. **`PLAYBOOK.md:6070`** - the gloss "closure cites a named SHA / actual command output" is not at that line. The line reads `| 7 | **OPERATOR WITNESS** | section 8 "Discharge with evidence" |`; the detail lives in section 8. The gloss is the reader's own unsourced addition.
3. **`PLAYBOOK.md:6071`** - likewise, "JOURNAL.md, LESSONS.md, ADRs" is not stated at the line or in the text it links.

**AND THE FINDING THAT MATTERS MOST, which this file's own framing gets wrong:**
`orchestrator-state.yml` **is never mechanically written or read by anything in the Maister repository.** The verification searched the whole tree: 33 mentions, all in `.md` files, plus exactly one non-markdown hit - a 21-line shell hook, `plugins/maister/hooks/post-compact-reminder.sh:12,15`, which checks only that a directory exists and then emits a static reminder telling the LLM to go read the YAML. It never opens, parses or writes it. The Maister tree contains **no `.py`, `.js` or `.ts` files at all**.

So where this file says "state carrier", read: **a YAML file an LLM is instructed by prose to maintain**. That does not make the design worthless - it is still a far richer state SHAPE than ours - but it is not an enforced mechanism, and the distinction is the whole of the SPINE section in MATRIX.md. See `R2-VERIFICATION.md`.

---

## REPO C — Maister

| PHASE | STATE-CARRIER | TRIGGER | GATE | LOCATOR | CONFIDENCE |
|---|---|---|---|---|---|
| 1 · Codebase analysis | `.maister/tasks/development/<task>/orchestrator-state.yml` | New development workflow initializes | Analysis and critical clarifications recorded; auto-continues | `maister/plugins/maister/skills/development/SKILL.md:128` | derived |
| 2 · Gap analysis | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 1 completes | Scope decisions resolved and mandatory routing question answered | `maister/plugins/maister/skills/development/SKILL.md:143` | derived |
| 3 · TDD red | `.maister/tasks/development/<task>/orchestrator-state.yml` | `has_reproducible_defect: true` | Reproduction test must fail; user approves continuation | `maister/plugins/maister/skills/development/SKILL.md:193` | derived |
| 4 · UI mockups | `.maister/tasks/development/<task>/orchestrator-state.yml` | `ui_heavy: true` and no existing mockups | Operator reviews/approves the live gallery or saved mockups | `maister/plugins/maister/skills/development/SKILL.md:212` | derived |
| 5 · Requirements and specification | `.maister/tasks/development/<task>/orchestrator-state.yml` | Prior conditional phases complete or are inapplicable | Specification summary presented and user approves audit | `maister/plugins/maister/skills/development/SKILL.md:243` | derived |
| 6 · Specification audit | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 5 approval | Independent audit verdict presented; user approves planning | `maister/plugins/maister/skills/development/SKILL.md:300` | derived |
| 7 · Implementation planning | `.maister/tasks/development/<task>/orchestrator-state.yml` | Specification audit completes or is skipped | Plan summary presented and user approves implementation | `maister/plugins/maister/skills/development/SKILL.md:319` | derived |
| 8 · Implementation | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 7 approval | All plan groups resolve, state records Phase 8 complete, user approves verification | `maister/plugins/maister/skills/development/SKILL.md:346` | derived |
| 9 · TDD green | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 3 ran and implementation completes | Reproduction test must pass; user approves continuation | `maister/plugins/maister/skills/development/SKILL.md:376` | derived |
| 10 · Verification selection | `.maister/tasks/development/<task>/orchestrator-state.yml` | Implementation or TDD-green approval | Mandatory user selection records enabled verification options | `maister/plugins/maister/skills/development/SKILL.md:395` | derived |
| 11 · Verification and issue resolution | `.maister/tasks/development/<task>/orchestrator-state.yml` | Verification options are fixed | No critical issues remain, or user explicitly accepts them; canonical verdict must reflect final state | `maister/plugins/maister/skills/development/SKILL.md:436` | derived |
| 12 · E2E testing | `.maister/tasks/development/<task>/orchestrator-state.yml` | `e2e_enabled: true` after Phase 11 | E2E succeeds and Phase 12 is marked complete; user approves documentation phase | `maister/plugins/maister/skills/development/SKILL.md:496` | derived |
| 13 · User documentation | `.maister/tasks/development/<task>/orchestrator-state.yml` | `user_docs_enabled: true`; E2E complete when enabled | Documentation completes and user approves finalization | `maister/plugins/maister/skills/development/SKILL.md:516` | derived |
| 14 · Finalization | `.maister/tasks/development/<task>/orchestrator-state.yml` | Prior phase’s mandatory approval | `task.status` is set to `completed` | `maister/plugins/maister/skills/development/SKILL.md:538` | derived |

## REPO F — .dev-knowledge

| PHASE | STATE-CARRIER | TRIGGER | GATE | LOCATOR | CONFIDENCE |
|---|---|---|---|---|---|
| 1 · Frozen ex-ante contract | Markdown task/lane contract | Ratified intent enters delivery | Executable acceptance criterion exists before building and cannot be weakened by the executor | `protocols/PLAYBOOK.md:6064` | derived |
| 2 · Branch and commit-and-STOP | Git branch and commit object store | Frozen contract is delegated for execution | Executor commits on a branch and stops without self-merging | `protocols/PLAYBOOK.md:6065` | derived |
| 3 · Target-repo gates | ABSENT | Branch implementation is ready for validation | Required target-repository gates run green | `protocols/PLAYBOOK.md:6066` | derived |
| 4 · Pre-merge review | Markdown review artifact | Target-repository gates are green | Named terra review covers the declared surface | `protocols/PLAYBOOK.md:6067` | derived |
| 5 · Operator authorization | ABSENT | Review is acceptable | Operator explicitly says GO | `protocols/PLAYBOOK.md:6068` | derived |
| 6 · Serial integration | Git first-parent history on `main` | Operator GO | `--no-ff` merge is performed serially from the primary checkout | `protocols/PLAYBOOK.md:6069` | derived |
| 7 · Operator witness | ABSENT | Integration completes | Closure cites a named SHA, actual command output, or operator observation | `protocols/PLAYBOOK.md:6070` | derived |
| 8 · Educate | `JOURNAL.md`, `LESSONS.md`, ADRs or archive records | Operator witnesses the hard end-state | Change, rationale, and next action are recorded | `protocols/PLAYBOOK.md:6071` | derived |

## DIVERGENCE

- **Maister → ours:** Maister persists explicit phase completion, routing characteristics, verification choices, summaries, risks, decisions, and artifacts in a resumable orchestration record; ours has no equivalent phase-state carrier (`maister/plugins/maister/skills/development/SKILL.md:559`).
- **Ours → Maister:** Ours makes serial `--no-ff` integration plus a post-merge operator witness and education record distinct closure phases; Maister finalizes by setting task status complete and merely guiding later commit/PR/deployment steps (`protocols/PLAYBOOK.md:6069`; `maister/plugins/maister/skills/development/SKILL.md:542`).

## ATTACK

**REFUTES.** Maister carries more than a process spine: it carries executable domain machinery for design-resource discovery and generated UI mockups, including a reviewable live gallery and downstream binding visual references (`maister/plugins/maister/skills/development/SKILL.md:212`). It also carries structured task-characteristic detection, configurable verification suites, research/design references, and per-phase decisions, risks, summaries, and artifact inventories (`maister/plugins/maister/skills/development/SKILL.md:559`).

## STATE-CARRIER-DELTA

Maister’s `orchestrator-state.yml` can express, in one machine-readable resumable record: current versus completed phases; failed attempts; conditional routing facts such as reproducible-defect, data-operation, entity-creation and UI-heavy flags; enabled or skipped audit/test/review/E2E/documentation branches; risk and architecture decisions; research and design references; and structured per-phase summaries with decisions, risks, and artifact paths (`maister/plugins/maister/skills/development/SKILL.md:559`). The markdown task directory can express task identity, open/terminal status, priority, size, hierarchy, serialization group, dependencies, ordering and prose, but not execution position, phase attempts, phase results, conditional workflow options, or resumable phase-local context (`tasks/README.md:81`).
[2mtokens used[0m
92,866
## REPO C — Maister

| PHASE | STATE-CARRIER | TRIGGER | GATE | LOCATOR | CONFIDENCE |
|---|---|---|---|---|---|
| 1 · Codebase analysis | `.maister/tasks/development/<task>/orchestrator-state.yml` | New development workflow initializes | Analysis and critical clarifications recorded; auto-continues | `maister/plugins/maister/skills/development/SKILL.md:128` | derived |
| 2 · Gap analysis | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 1 completes | Scope decisions resolved and mandatory routing question answered | `maister/plugins/maister/skills/development/SKILL.md:143` | derived |
| 3 · TDD red | `.maister/tasks/development/<task>/orchestrator-state.yml` | `has_reproducible_defect: true` | Reproduction test must fail; user approves continuation | `maister/plugins/maister/skills/development/SKILL.md:193` | derived |
| 4 · UI mockups | `.maister/tasks/development/<task>/orchestrator-state.yml` | `ui_heavy: true` and no existing mockups | Operator reviews/approves the live gallery or saved mockups | `maister/plugins/maister/skills/development/SKILL.md:212` | derived |
| 5 · Requirements and specification | `.maister/tasks/development/<task>/orchestrator-state.yml` | Prior conditional phases complete or are inapplicable | Specification summary presented and user approves audit | `maister/plugins/maister/skills/development/SKILL.md:243` | derived |
| 6 · Specification audit | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 5 approval | Independent audit verdict presented; user approves planning | `maister/plugins/maister/skills/development/SKILL.md:300` | derived |
| 7 · Implementation planning | `.maister/tasks/development/<task>/orchestrator-state.yml` | Specification audit completes or is skipped | Plan summary presented and user approves implementation | `maister/plugins/maister/skills/development/SKILL.md:319` | derived |
| 8 · Implementation | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 7 approval | All plan groups resolve, state records Phase 8 complete, user approves verification | `maister/plugins/maister/skills/development/SKILL.md:346` | derived |
| 9 · TDD green | `.maister/tasks/development/<task>/orchestrator-state.yml` | Phase 3 ran and implementation completes | Reproduction test must pass; user approves continuation | `maister/plugins/maister/skills/development/SKILL.md:376` | derived |
| 10 · Verification selection | `.maister/tasks/development/<task>/orchestrator-state.yml` | Implementation or TDD-green approval | Mandatory user selection records enabled verification options | `maister/plugins/maister/skills/development/SKILL.md:395` | derived |
| 11 · Verification and issue resolution | `.maister/tasks/development/<task>/orchestrator-state.yml` | Verification options are fixed | No critical issues remain, or user explicitly accepts them; canonical verdict must reflect final state | `maister/plugins/maister/skills/development/SKILL.md:436` | derived |
| 12 · E2E testing | `.maister/tasks/development/<task>/orchestrator-state.yml` | `e2e_enabled: true` after Phase 11 | E2E succeeds and Phase 12 is marked complete; user approves documentation phase | `maister/plugins/maister/skills/development/SKILL.md:496` | derived |
| 13 · User documentation | `.maister/tasks/development/<task>/orchestrator-state.yml` | `user_docs_enabled: true`; E2E complete when enabled | Documentation completes and user approves finalization | `maister/plugins/maister/skills/development/SKILL.md:516` | derived |
| 14 · Finalization | `.maister/tasks/development/<task>/orchestrator-state.yml` | Prior phase’s mandatory approval | `task.status` is set to `completed` | `maister/plugins/maister/skills/development/SKILL.md:538` | derived |

## REPO F — .dev-knowledge

| PHASE | STATE-CARRIER | TRIGGER | GATE | LOCATOR | CONFIDENCE |
|---|---|---|---|---|---|
| 1 · Frozen ex-ante contract | Markdown task/lane contract | Ratified intent enters delivery | Executable acceptance criterion exists before building and cannot be weakened by the executor | `protocols/PLAYBOOK.md:6064` | derived |
| 2 · Branch and commit-and-STOP | Git branch and commit object store | Frozen contract is delegated for execution | Executor commits on a branch and stops without self-merging | `protocols/PLAYBOOK.md:6065` | derived |
| 3 · Target-repo gates | ABSENT | Branch implementation is ready for validation | Required target-repository gates run green | `protocols/PLAYBOOK.md:6066` | derived |
| 4 · Pre-merge review | Markdown review artifact | Target-repository gates are green | Named terra review covers the declared surface | `protocols/PLAYBOOK.md:6067` | derived |
| 5 · Operator authorization | ABSENT | Review is acceptable | Operator explicitly says GO | `protocols/PLAYBOOK.md:6068` | derived |
| 6 · Serial integration | Git first-parent history on `main` | Operator GO | `--no-ff` merge is performed serially from the primary checkout | `protocols/PLAYBOOK.md:6069` | derived |
| 7 · Operator witness | ABSENT | Integration completes | Closure cites a named SHA, actual command output, or operator observation | `protocols/PLAYBOOK.md:6070` | derived |
| 8 · Educate | `JOURNAL.md`, `LESSONS.md`, ADRs or archive records | Operator witnesses the hard end-state | Change, rationale, and next action are recorded | `protocols/PLAYBOOK.md:6071` | derived |

## DIVERGENCE

- **Maister → ours:** Maister persists explicit phase completion, routing characteristics, verification choices, summaries, risks, decisions, and artifacts in a resumable orchestration record; ours has no equivalent phase-state carrier (`maister/plugins/maister/skills/development/SKILL.md:559`).
- **Ours → Maister:** Ours makes serial `--no-ff` integration plus a post-merge operator witness and education record distinct closure phases; Maister finalizes by setting task status complete and merely guiding later commit/PR/deployment steps (`protocols/PLAYBOOK.md:6069`; `maister/plugins/maister/skills/development/SKILL.md:542`).

## ATTACK

**REFUTES.** Maister carries more than a process spine: it carries executable domain machinery for design-resource discovery and generated UI mockups, including a reviewable live gallery and downstream binding visual references (`maister/plugins/maister/skills/development/SKILL.md:212`). It also carries structured task-characteristic detection, configurable verification suites, research/design references, and per-phase decisions, risks, summaries, and artifact inventories (`maister/plugins/maister/skills/development/SKILL.md:559`).

## STATE-CARRIER-DELTA

Maister’s `orchestrator-state.yml` can express, in one machine-readable resumable record: current versus completed phases; failed attempts; conditional routing facts such as reproducible-defect, data-operation, entity-creation and UI-heavy flags; enabled or skipped audit/test/review/E2E/documentation branches; risk and architecture decisions; research and design references; and structured per-phase summaries with decisions, risks, and artifact paths (`maister/plugins/maister/skills/development/SKILL.md:559`). The markdown task directory can express task identity, open/terminal status, priority, size, hierarchy, serialization group, dependencies, ordering and prose, but not execution position, phase attempts, phase results, conditional workflow options, or resumable phase-local context (`tasks/README.md:81`).

[exited with code 0]


---

## Rows this file is evidence for

- **[#676]** - *no check verifies a provider CLI's non-interactive invocation shape.* This file's header records a codex run that spent 85,017 tokens and delivered nothing because of an L0 role constraint the caller could not see in advance - a failure mode the row's four-way outcome split does not currently express.

