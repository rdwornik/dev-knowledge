# Architectural Decision Records — `.dev-knowledge`

<!-- scope: meta -->

Architecture decisions for `.dev-knowledge` in Michael Nygard ADR format. The `transcripts/`
subfolder holds AI Council debate outputs that informed them.

## ADR Index

<!-- scope: meta -->

| ADR | Date | Title |
|-----|------|-------|
| ADR-27 | 2026-04-21 | Scope tagging — single-repo `dev\|llm\|hybrid\|runtime\|meta` vocabulary, hybrid ≤25% ceiling, pre-commit enforcement |
| ADR-28 | 2026-04-21 | Three-layer architecture — browser chat → .dev-knowledge → projects; descriptive ADR documenting existing practice |
| ADR-29 | 2026-04-21 | LESSONS.md grandfathering — existing entries untouched; new entries include inline `[scope: X]` tag |
| ADR-30 | 2026-04-26 | Default git branch `main` — universal rule for all Rob's repos |
| ADR-31 | 2026-04-27 | Authority model — prescriptive with conformance audit (Option 1B); .dev-knowledge prescriptions are binding |
| ADR-32 | 2026-04-27 | Handoff format and browser/agent role split — folder-format handoffs, strict role boundary |
| ADR-33 | 2026-04-28 | VISION.md universalization — mandatory at ≥1 dependent; Standard/Lite tiers per scale |
| ADR-34 | 2026-04-29 | File naming convention — per-file-type table; codifies existing de-facto patterns cross-repo |
| ADR-35 | 2026-04-29 | Lessons base activation — lessons-index.json + SessionStart retrieval + CLI querying |
| ADR-36 | 2026-04-30 | Audit tool architecture — .dev-knowledge as ecosystem auditor; 4-phase implementation plan |
| ADR-37 | 2026-04-30 | Session boundary protocol — two-phase handoff (Current State + Future State) |
| ADR-38 | 2026-04-30 | Universal repo architecture baseline — mandatory files per tier S/M/L; foundation for ADR-39/40/41; amended 2026-05-23 (A5: tier deprecation → universal baseline) + 2026-06-02 (A6: seven-file canonical set + canonical structure standard) |
| ADR-39 | 2026-04-30 | File lifecycle governance — 6-element pattern per file (purpose/trigger/owner/grooming/boundaries/enforcement) |
| ADR-40 | 2026-04-30 | Scale tier evaluation algorithm — logarithmic Maintainability Index pattern; 3 signals (module count, test count, TCR) |
| ADR-41 | 2026-04-30 | Cross-session backlog architecture — BACKLOG.md mandate at M+ tier; no Scrum vocabulary; amended 2026-06-02 (supersession chain 47/64/65/66 + ecosystem story-map binding with proportional depth, closes #20) |
| ADR-42 | 2026-05-09 | Handoff format v3 — three-stage generation flow; v3.2 = flat per-session folder, Q&A iteration loop; amended 2026-05-26 (Q5: full invariants retained + executor-gate contract + manifest integrity) |
| ADR-43 | 2026-05-11 | Cross-project transcript routing — per-invocation, opt-in, config-driven; `target-project:` frontmatter + `--target-project` flag; `TargetResolver` in ai-council CLI |
| ADR-44 | — | Reserved — scrum-master review propagation authority codification; held pending N=2 empirical instance (corp-monorepo scrum-master review). See PLAYBOOK § 17. |
| ADR-45 | 2026-05-13 | ~~Handoff Architecture v4 — invariant/session separation + defense-in-depth enforcement~~ Superseded by 2026-05-13 night minimum-viable refinement (HANDOFF_PROCESS v3.3) |
| ADR-46 | 2026-05-15 | Cross-repo dated-entries format — retained as convention, NOT audit-enforced (demoted 2026-05-16) |
| ADR-47 | 2026-05-15 | Cross-repo BACKLOG.md organization — retained as convention, NOT audit-enforced (demoted 2026-05-16) |
| ADR-48 | 2026-05-17 | Trim documentation governance to structural enforcement — amends ADR-46/47 (demoted), ADR-27 (scope-tagging retired) |
| ADR-49 | 2026-05-17 | Consolidate past-recording documentation files — amends ADR-46/47 (fewer files governed) |
| ADR-50 | 2026-05-17 | Machine-document encoding standard — governance-admission rule for machine-written content |
| ADR-51 | 2026-05-18 | Architecture documentation convention — `ARCHITECTURE.md` mandatory at M/L scale; hybrid staleness control (auto-generated codemap + CI check + hand-written invariants); graphical at M/L, text-only at S |
| ADR-52 | 2026-05-19 | ~~AGENTS.md convention — cross-tool agent-instruction contract~~ Superseded by ADR-53 |
| ADR-53 | 2026-05-19 | CLAUDE.md as single canonical per-repo agent-instruction file — supersedes ADR-52 |
| ADR-54 | 2026-05-19 | Codex reviewer config as global standard — canonical source at `codex/AGENTS.md`, deployed to `~/.codex/AGENTS.md`; per-repo `AGENTS.md` for repo-specific review rules only |
| ADR-55 | 2026-05-26 | Applied-task internalization gate — replaces 4-item paraphrase gate with role+constraints citations + one applied probe (`10_GATE_PROBE.md`) + one bounded retry (closes Council Q1) |
| ADR-56 | 2026-05-26 | Inline Prompt Generation Card — replaces PLAYBOOK-pointer with a self-contained card in `00_first-message.md`; authority stays in browser chat; ≤200-line budget + dual-maintenance rule (closes Council Q3) |
| ADR-57 | 2026-05-26 | Two-layer bundle contract — unconditional governance floor (VISION/PLAYBOOK/ESSENTIALS) + scoped operational layer (skills/gotchas/JOURNAL) via `next_session_scope` + mapping table; extends ADR-42 (closes Council Q2) |
| ADR-58 | 2026-05-26 | Structured claims + symmetric verification — sender produces `11_CLAIMS.md` (cited load-bearing claims) + expected-articulation; executor validates locatability; operator ratifies; removes bare `role confirmed` (closes Council Q4) |
| ADR-59 | 2026-05-27 | Universal visual repository pattern — dot-prefix discipline (verified exception list incl. `tach.toml`), ALL-CAPS canonical `.md` visibility, workspace sort settings (`sortOrderLexicographicOptions: upper`); enforced via 3 new `audit.py` checks; rolled out to `.dev-knowledge` + 4 child-repo retrofit plans |
| ADR-60 | 2026-05-27 | docs/ folder taxonomy — semantic role per subfolder (`audits/`=outputs, `council-questions/`=inputs, `decisions/`=ADRs+transcripts, `handoffs/`=session bundles, `research/`=working scratchpad, `archive/`=superseded/dormant); implements Option B of the 2026-05-25 pipeline proposal (closes finding A1); `tech-radar/` archived; append-only/immutable records left as point-in-time history on move |
| ADR-61 | 2026-05-28 | Git worktree pattern for parallel Claude Code sessions — same-repo parallel sessions require `git worktree` (distinct working dir + HEAD per session); cross-repo parallel is safe without worktree; closes BACKLOG #5 (escalated P1 after ≥3 race incidents 2026-05-26/27) |
| ADR-62 | 2026-05-30 | v4 handoff process ratification — ratifies HANDOFF_PROCESS v4 + v4.2 + v4.3 + v4.3.1 collectively as canonical (Path A); disambiguates the "v4" naming collision with ADR-45 (explored-not-adopted) |
| ADR-63 | 2026-05-30 | Scrum-master review authority — unified asymmetric review-authority covering Facet 1 (cross-repo strażnik review, N=3) + Facet 2 (operator→architect intra-session); Option E hybrid trigger-based + per-artifact-class (Path A) |
| ADR-64 | 2026-06-01 | BACKLOG.md architecture — lean active file (done items leave, git history is the record), status-and-priority taxonomy (streams/arc sections retired → `repo:` field), per-repo routing of child-repo items, narrow read-only schema validator (AI Council pick verdict) |
| ADR-65 | 2026-06-01 | BACKLOG done-item disposition — git is the technical record (forward-indexed via commit convention), JOURNAL per-session narrative is the business record (no per-item write); refines ADR-64 Decision 1 (Path A) |
| ADR-66 | 2026-06-01 | BACKLOG story-map hierarchy — Big Picture → Theme → User Story → Task (Scrum + Patton story mapping); operator scans goals, LLM reads task detail; drops `repo:`; supersedes ADR-64 Decision 2 (flat layout) only (Path A) |
| ADR-67 | 2026-06-01 | AI-Council process operationalization — six-step gated loop (Frame→Generate→Gate→Run→Verdict→Return); `/council-question` trigger; three-domain split (process here, template+gate in `ai-council`, return-dir in `~/.claude`); amends `AI_COUNCIL_PROCESS.md` v1.0 (Path A) |
| ADR-68 | 2026-06-01 | Autonomous overnight review agent — local Task Scheduler → headless `claude -p` read-only review → morning briefing (Option B); subscription auth (operator override of Council API-key rec) + model-tiering (Sonnet scan / Opus synth) + token/runtime caps; scoped deny-policy makes read-only physically true; read-only worktrees (ADR-61); sequential over ~6 repos; max-5 cited findings; runtime system self-contained in `~/.claude/night-agent/` |
| ADR-69 | 2026-06-02 | Cross-repo audit reach model — `audit.py` reaches child repos via a Layer-2 read-only cross-repo runner (`run` iterates the `ecosystem/` registry, reads each read-only, writes only into `.dev-knowledge`); per-repo ports + governance-only rejected; commit-time enforcement stays self-only (the #72 residual); records the BACKLOG #44 reach decision (Path A) |
| ADR-70 | 2026-06-02 | Three-tier self-enforcing process layer — Tier 1 always-on lifecycle (native primitives bundled as one methodology plugin: git-as-capture, Stop-hook propose-closures skill, `/boot`, ruff gate, lesson-promotion), Tier 2 scheduled `audit.py run` → `fleet-health.md`, Tier 3 explicit/scoped Dynamic Workflows for heavy episodic work; Workflow = heavy-execution analog of the Council on the decision ladder; supersedes the evidence-ledger custom-file design (git is the ledger); capture-only, build sequence in BACKLOG (Council verdict + three-tier synthesis) |
| ADR-71 | 2026-06-03 | Doc-tooling distribution via the pre-commit hook source repo pattern — the hub ships a root `.pre-commit-hooks.yaml` exposing codemap+TOC as four hooks (`codemap`/`toc` × freshness/generate); children consume via `repo:/rev:` (single-source, version-pinned, no copy-drift). `language: script` thin wrappers in `scripts/` (no pip package — zero-dep tools; preserves Layer-2 non-distributable identity); local-path reachability now, URL-swappable; generation stays local per repo (hub never writes siblings — ADR-28/ADR-69). Validated by the corp-monorepo pilot (pending) |
| ADR-72 | 2026-06-06 | Cloud Routines are hub-independent (self-containment) — a cloud Routine clones only its target repo and consults only that repo's own git/docs/backlog; no hub reference is load-bearing on the executing path. The hub being **private** closes ADR-71's "URL-swappable later" hatch for the cloud case (a git-source/URL hub needs auth in the sandbox — forbidden), so plugin/skill distribution (#86.3) does not resolve in cloud. Existing hub refs (pre-commit `repo:../`, the `tier1-lifecycle` plugin) are inert-by-design/harmless in cloud (verified). No resolver shipped (would be cloud-inert = false coverage); a future cloud need for a hub ref = STOP-and-escalate (publish a subset, operator call). Records #86 sub-decision 2; amends (does not edit) ADR-71 |
| ADR-81 | 2026-06-09 | Feature-lifecycle definition of done (organs) — an organ (plugin, hook, command, skill, workflow, generator, convention) is not DONE until it has all four: (a) a methodology home in PLAYBOOK, (b) a deployment path (runbook/install sequence), (c) a maintenance/refresh cadence with staleness detection, (d) actual deployment OR an explicit named deferral. Build-and-test ≠ done (the half-feature rot trap); generalizes ADR-80's routine-scoped "What every routine must meet" to every organ class. (Index rows ADR-73…ADR-80 are a known pre-existing gap in this table, not part of this ADR.) |
| ADR-82 | 2026-06-11 | **Proposed (Council-pending)** — HANDOFF_PROCESS v5, CC-owned primary-source-forced handoff (model C): CC owns/initiates the handoff and emits only the residual (un-committed reasoning + pointers + **drift-flags as headline**); a ~3-line thin browser boot (with the browser operating-role resident in it) replaces the heavy 8-file bundle; methodology enforced mechanically, referenced thinly; the forced primary-source read has **teeth** (probe answers exist only in live state, reusing `audit.py checks`/`validate_doc_claims`/`validate_git_backlog` + quote-grounded probes); lean pointer-not-narration task-state; verification split (browser=artifact, CC=state fidelity) + bidirectional adjudication. Ships beta as `HANDOFF_PROCESS_v5.md` (parallel); promotion to canonical is a Council+fresh-eyes-gated atomic flip. Supersedes ADR-62 + ADR-79's bundle delivery *at promotion*, not now. |
| ADR-83 | 2026-06-11 | Protocols-archive convention — superseded/dead protocols move to `protocols/archive/<name>.md` with a blockquote tombstone (archived date + superseded-by/path + frozen-record line); `protocols/` top level holds only live specs. Codifies the **existing** v3.4 format (zero retrofit); moves no file. Parallel-beta (`HANDOFF_PROCESS_v5.md`/`HANDOFF_BOOT.md`) + intentional-anchor (`AGENT_FRAMEWORK.md`) are live, NOT dead. **Hard gate: v4.4 stays canonical — its archival is a #149 flip-step, not done here.** |
| ADR-84 | 2026-06-13 | Automation-writer outputs fully isolated from `main` (Q9) — each unattended writer (conformance digest, fleet-audit baseline) commits only to its own dedicated `automation/*` branch, never merged into `main`; `surface_triage.ps1`'s digest probe repoints to `?ref=automation/conformance-digest`; once writers no longer land on `main` the `_is_automation` marker-exemption is **removed** from `no_ff_merges` (#153) — restoring the gate to one rule (every non-merge commit on `main` is a violation) — and disposition `warn-61c5b50` is retired. Legacy automation already on `main` left in place (forward-only); branch retention deferred. Resolves the #156/#163 cherry-pick collision + the behind-N origin divergence structurally. |
| ADR-85 | 2026-06-16 | Session-lifecycle enforcement — deterministic JOURNAL/BACKLOG stop-gate (AI Council, 4-model panel). Scope-reduce currency enforcement to the two docs that rot worst + change every session; extend the session-end Stop-hook (no LLM): **hard block on the JOURNAL leg** (un-gameable commit-SHA anchor, supersedes the advisory journal-presence check), **advisory nudge on the BACKLOG leg** in v1 (promoted to a hard gate when the traceability-spine lands, R1); demote ARCHITECTURE/VISION/LESSONS/CONTRIBUTING to "update when materially affected"; escape only via logged HEAD-bound `/override` (no auto-bypass); single-source `protocols/DEFINITION_OF_DONE.md`; 4-week scope-freeze. R2 defers ungated-doc staleness to the conformance dashboard (→ ADR-86). |
| ADR-86 | 2026-06-16 | Conformance-dashboard location — the dashboard ADR-85 R2 deferred to lives at `ecosystem/conformance.md`, classified as an **ADR-80 committed-generated zone** (a read-only validator generates + commits its own output, pathspec-bounded/fail-soft; Layer-2-safe). ARCHITECTURE Ch2 gains a pointer to it (resolves the G7 coverage-matrix gap) — the pointer lands with the build (#171), not before. Settles location + zone class + navigation intent; the write-channel (main vs `automation/*`) + generator + freshness hook are deferred to the build (#171). Path-A capture (2026-06-16 consolidation). |
| ADR-87 | 2026-06-18 | Architect↔CC equilibrium contract — conditional intent-only prompting. STEP 1 verified CC self-loads context **reliably only for code-impact tasks**; read-only (GAP-1), execution-time gotcha (GAP-2), and governance-context (GAP-3) self-load are unreliable. Division of labor: **architect emits** intent · closure · anti-patterns · plan/auto mode · a thin per-task governance-pointer (the ADR/LESSONS/sibling-spec the task touches — GAP-3 won't self-infer); **CC owns** code-impact context · generic gotchas · the skeleton (now CC's consumption-spec) · model/effort. Intent-only is **conditional** (reliable for code-impact; governance/read-only tasks require the pointer); the mode carries an actionable basis (→ PLAYBOOK §2 "How to choose Mode"). The GAP-2 deterministic backstop is filed-not-built (#185); the arc's empirical closure is #184. Path-A direct ruling. |

## Transcript naming convention

<!-- scope: meta -->

### Canonical (since 2026-04-30 revert commit `4a00560`)

`council-out-YYYYMMDD-HHMMSS-{slug}.md` — timestamped, CLI-emitted from AI Council. 12 files
currently in `transcripts/`.

### Legacy (pre-canonical)

`DECISION_NN_{slug}.md` — 3 files (`DECISION_27`, `DECISION_28`, `DECISION_29`) are pre-CLI
historical artifacts from the manual archival era. **Relocated to `transcripts/archive/legacy/` (2026-05-12). Not renamed retroactively.**

> **Important:** legacy `DECISION_NN` numbering does NOT align with ADR-NN numbering.
> `DECISION_28_authority_model` informed ADR-31 (not ADR-28); `DECISION_29_handoff_synergy`
> informed ADR-32 (not ADR-29).

## ADR↔transcript traceability

<!-- scope: meta -->

| ADR | Originating transcript(s) |
|-----|---------------------------|
| ADR-27 | `transcripts/archive/legacy/DECISION_27_llm_practice_ecosystem.md` — verified: Council #27 brief about single-repo vs split; decided Option A (scope tagging) |
| ADR-28 | *(no transcript — conversational decision documenting existing practice)* |
| ADR-29 | *(no transcript — derivative of ADR-27, same session)* |
| ADR-30 | *(no Council transcript — decided via Codex audit `docs/audits/2026-04-26-codex-adr-30-default-branch-main.md`)* |
| ADR-31 | `transcripts/archive/legacy/DECISION_28_authority_model.md` — verified: per ADR-31 "Debate transcript" reference |
| ADR-32 | `transcripts/archive/legacy/DECISION_29_handoff_synergy.md` — verified: per ADR-32 "Debate transcript" reference |
| ADR-33 | `council-out-20260428-125133-format-and-structure-of-visionmd-for-dev.md` (research) + `council-out-20260428-162415-pick-council-prompt-adr33-vision-universalization.md` (decision) |
| ADR-34 | `council-out-20260429-190922-pick-council-adr34-file-naming-convention.md` |
| ADR-35 | `council-out-20260429-210057-pick-council-adr35-lessons-base-activation.md` |
| ADR-36 | `council-out-20260430-123043-pick-council-adr36-audit-tool-architecture.md` + `council-out-20260430-125039-research-question-what-prior-art-exists-for-cross-repo-audi.md` (research) |
| ADR-37 | `council-out-20260430-132308-pick-council-adr37-two-phase-handoff.md` |
| ADR-38 | `council-out-20260430-134721-pick-council-adr38-scrum-framework.md` — verified: "adr38" in filename; content is scrum-as-framework debate that produced universal repo architecture ADR; "scrum_framework" slug reflects original question framing |
| ADR-39 | *(no obvious transcript — may be conversational)* |
| ADR-40 | `council-out-20260430-154818-research-question-how-should-an-llm-driven-multi-repo-ecosy.md` — per ADR-40 Related field |
| ADR-41 | `council-out-20260430-134721-pick-council-adr38-scrum-framework.md` (also cited in ADR-41 Related field as structural context) + `council-out-20260430-150751-research-question-for-a-solo-developer-with-multiple-active.md` (research) |
| ADR-42 | `council-out-20260509-143831-research-brief-for-ai-council-architect-browser-session-con.md` + `council-out-20260509-144836-research-question-how-should-an-llm-driven-solo-developer-a.md` |
| ADR-51 | `council-out-20260518_215241-pick-2026-05-18_council-debate-architecture-doc.md` |
| ADR-55 | `council-out-20260526_142806-pick-2026-05-25-handoff-council-Q1-internalization-assurance.md` |
| ADR-56 | `council-out-20260526_144228-pick-2026-05-25-handoff-council-Q3-procedural-competence-transfer.md` |
| ADR-57 | `council-out-20260526_143605-pick-2026-05-25-handoff-council-Q2-bundle-content-composition.md` |
| ADR-58 | `council-out-20260526_144851-pick-2026-05-25-handoff-council-Q4-sender-verification-symmetry.md` |
| ADR-52 | *(no Council transcript — Rob's decision, 2026-05-19; ratifies extant PLAYBOOK convention)* |
| ADR-53 | *(no Council transcript — Rob's decision, 2026-05-19; based on empirical verification `docs/audits/2026-05-19-cohort1-verification.md`)* |
| ADR-62 | *(no Council transcript — Path A direct ADR, 2026-05-30; post-hoc record of v4 already implemented + fresh-eyes-validated)* |
| ADR-63 | *(no Council transcript — Path A direct ADR, 2026-05-30; empirical grounding N=3)* |
| ADR-64 | `council-out-20260601_103339-pick-council-backlog-architecture-2026-05-31.md` — pick mode, 4-model panel + openai synthesizer, 2 rounds |
| ADR-65 | *(no Council transcript — Path A direct ADR, 2026-06-01; refines ADR-64 Decision 1 per operator self-review)* |
| ADR-66 | *(no Council transcript — Path A direct ADR, 2026-06-01; operator-chosen layout refinement, supersedes ADR-64 Decision 2)* |
| ADR-67 | *(no Council transcript — Path A direct ADR, 2026-06-01; process formalization of a running loop; amends `AI_COUNCIL_PROCESS.md` v1.0)* |
| ADR-68 | Council `pick` debate — 4-model panel (claude-opus-4-7, deepseek-v4-pro, grok-4.3, gpt-5.4) + Gemini synth, unanimous on architecture + autonomy boundary (per ADR-68 "Decision method"). Canonical transcript in `ai-council/output/`; **not archived in `docs/decisions/transcripts/`** — the debate set no `target-project`, so the manual-archival fallback was not run. |
| ADR-69 | *(no Council transcript — Path A direct ADR, 2026-06-02; records the cross-repo audit reach model already implemented; closes BACKLOG #44)* |
| ADR-70 | AI Council verdict 2026-06-02 (three-tier process automation) — canonical transcript in `ai-council/output/`; debate set no `target-project`, so not archived in `docs/decisions/transcripts/` (manual-archival fallback not run, same as ADR-68). The three-tier synthesis on top of the verdict was the operator's. |
| ADR-71 | *(no Council transcript — Path A direct ADR, 2026-06-03; records the doc-tooling distribution vehicle grounded in `docs/audits/2026-06-03-doc-tooling-inventory.md`; validation pending the corp-monorepo pilot)* |
| ADR-72 | *(no Council transcript — Path A direct ADR, 2026-06-06; records #86 sub-decision 2 / the cloud self-containment ruling, grounded in the #86.2 UNDERSTAND inventory: hub PRIVATE + plugin verified inert in cloud per JOURNAL 2026-06-04)* |
| ADR-73 | *(no Council transcript — Path A direct ADR, 2026-06-06; "Per-repo orchestration distribution" — records #86 sub-decision 3; amends ADR-72; operator paste-=-consent, recorded corp-monorepo JOURNAL 2026-06-06)* |
| ADR-74 | *(no Council transcript — Path A direct ADR, 2026-06-06; "Automation doctrine consolidation; layer→job matrix canonical" — amends ADR-70; operator ratification, browser doctrine-pass synthesis; amended in-file 2026-06-07 to scope the /loop REJECTED row to persistence-host)* |
| ADR-75 | *(no Council transcript — Path A direct ADR, 2026-06-06; "Exclusion-zone register" — doctrine-pass gap G4; operator ratification, browser session; refs global CLAUDE.md §P0)* |
| ADR-76 | `council-out-20260606_172555-pick-council-local-scheduled-tier.md` — pick debate, 4-model panel (claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3) + openai synth, 2 rounds; "Local fleet-baseline host: Task Scheduler → python directly"; amends ADR-74; operator paste-consent 2026-06-06 |
| ADR-77 | *(no Council transcript — Path A direct ADR / operator GO, 2026-06-06; "Immutable-paths zone class (transcripts)" — amends ADR-75 (adds a second zone class); implementation wave, scope ruled after the UNDERSTAND-valve)* |
| ADR-78 | `council-out-20260607_124757-pick-council-f2-child-floor.md` — pick debate, unanimous post-R2; "Child methodology floor (O2 Bounded Hybrid)"; amends ADR-75 (adds `methodology_surface` zone class); operator ratification via distillation prompt 2026-06-07 |
| ADR-79 | `council-out-20260607_125247-pick-council-f1-browser-carrier.md` — pick debate, 3-of-4 panelists pivoted in R2; "Browser methodology carrier: bundle-only; Projects deferred"; amends none; operator ratification via distillation prompt 2026-06-07 |
| ADR-80 | *(no Council transcript — Path A direct ADR, 2026-06-07; "Two-tier automation adoption: writer policy + Routine/night operational standard" — amends ADR-74 (consumes its OPEN local-tier row); operator chat-drafted ruling, codification of BACKLOG #84)* |
| ADR-81 | none — direct operator decision (2026-06-09; Council deferred). Records the feature-lifecycle definition-of-done; codifies BACKLOG-side scar-tissue surfaced this session. |
| ADR-82 | **Council-pending** — operator decision 2026-06-11 (CC prompt, model C); architecture routed to AI Council per #148 / ADR-41. Transcript will be added when Council ratifies; v5 ships beta in the interim. |
| ADR-87 | *(no Council transcript — Path A direct ADR, 2026-06-18; records the STEP 1 self-load finding + the architect↔CC equilibrium contract)* |

## Pending Council decisions

<!-- scope: meta -->

No `pending-council-questions.md` exists yet — pending questions are currently tracked in
`BACKLOG.md` under "Council debate territory" annotations. Future convention: create
`docs/decisions/pending-council-questions.md` when the queue warrants a dedicated file.

## Council output reality note

<!-- scope: meta -->

AI Council CLI writes the canonical transcript to `ai-council/output/` and routes a copy to a
project's `docs/decisions/transcripts/` **automatically** when a debate sets a `target-project:`
(frontmatter) or `--target-project` (CLI), per ADR-43 (`routing.py` `TargetResolver`). Routed
debates need no manual archival; debates that do not name a target-project still emit only to
`ai-council/output/` and are archived manually. Canonical filename is preserved; source of truth
remains `ai-council/output/`. Full operational detail in PLAYBOOK "Council Debate Archival
Protocol".

## Related

<!-- scope: meta -->

- `docs/council-questions/` — Council debate INPUTS (question sets, evidence, set indexes); staging for the pipeline (per ADR-60)
- `docs/research/` — WORKING scratchpad: exploratory pre-decision drafts that mature into audits/decisions/council-questions (per ADR-60)
- `docs/audits/` — point-in-time audit OUTPUTS (per-repo state analysis, validation reports, forensics)
