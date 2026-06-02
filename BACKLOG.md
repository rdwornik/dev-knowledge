# .dev-knowledge BACKLOG

## Big picture

`.dev-knowledge` is the ecosystem's methodology brain: it absorbs lessons from every repo, universalizes them into enforced conventions, and audits the ecosystem against them — the LLM-development "scrum master" for all `Dev/` projects (VISION: Knowledge Guardian · Methodology Author · Auditor · Disseminator). The backlog advances that mission across seven themes.

**Themes (backbone):** Handoff continuity · Enforced governance · Lessons feedback loop · Decision management · Canonical-file integrity · Cross-repo universalization · Tooling & evaluation

---

## Handoff continuity
> As a session inheriting this repo, I want to pick up with full state and lose nothing.

### Give every handoff a fresh-eyes review, not just the big ones
So that routine handoffs stop inheriting the ~25% insider blind spot.
- [#1] [P1][L] Extend triangulation from the promotion gate to every routine handoff (sub-prompt / periodic audit / agent-framework) · Done when: every Phase-2 handoff runs a fresh-eyes pass · refs protocols/AGENT_FRAMEWORK.md (Council)

### Stop advisory framing from pressuring the receiver
So that "REST recommended"-style framing stops driving unprompted receiver behavior.
- [#6] [P2][M] Classify the root cause of advisory-framing leakage and propose a mitigation · Done when: root cause documented + a mitigation rule lands in HANDOFF_PROCESS/ESSENTIALS · refs ADR-37, LESSONS 2026-05-11

### Let an inheritor act on the operator's defaults instead of re-asking
So that a fresh chat states-and-acts rather than over-asking on things it should assume.
- [#26] [P3][S] Add an operator-invariants section to the Phase-1 interview/bundle (clean-tree, immediate-merge, three-domain) · Done when: the section ships in the handoff template/skill · refs HANDOFF_PROCESS v4

### Close the deferred handoff-template refinements
So that the v4 templates stop carrying known minor gaps.
- [#25] [P3][M] Apply the 7 deferred v4.3.1 refinements (tag-lint, fresh-eyes cadence, CLI example, ML namespace, wording, auto-routing, passive-storage) at the .tmpl level · Done when: all 7 resolved in templates/handoff/*.tmpl · refs HANDOFF_PROCESS v4.3.1

---

## Enforced governance
> As the operator, I want load-bearing conventions enforced by tools, not memory, so they can't silently drift.

### Turn advisory guards into enforced gates
So that a convention can't be skipped under load (the failure mode behind real aborts).
- [#11] [P2][M] Convert LESSON-#9's advisory cross-case guard into an amendment checklist/gate (Layer-2 checklist, not orchestration) · Done when: a multi-surface amendment must pass the gate · refs coherence-audit ML-2
- [#15] [P2][M] Add hyphen-only-separator enforcement (pre-commit + Action) with a scoped path set + exceptions · Done when: a non-conforming new filename is blocked · refs ADR-34

### Extend structural validation to more governance artifacts
So that drift in transcripts, ADRs, and folders is caught cheaply, not by reviewer luck.
- [#7] [P2][M] Apply the audit.py #8 structural-validator pattern to Council transcripts + ADRs (frontmatter/supersession/template) · Done when: registered checks + tests folded into health · refs scripts/audit.py #8/#9
- [#36] [P3][M] Add read-only check_folder_semantics asserting each docs/ subfolder carries one ADR-60 role · Done when: the check ships with fixtures + tests · refs ADR-60
- [#42] [P3][S] Decide whether mermaid-theme check #7 expands beyond ARCHITECTURE.md (extend paths or accept) · Done when: scope decision recorded · refs durability-audit J4
- [#72] [P3][S] Make no_sibling_orphans (#11) fire across all ecosystem repos, not just the .dev-knowledge self-audit (the audit-health gate checks self only, so an orphan beside a child repo is caught only by a full `audit run`, never at commit time) · Done when: orphan detection runs for every registered repo in a scheduled/automated audit · refs scripts/audit.py #11, PLAYBOOK G5, ADR-70 (Tier-2 scheduled baseline)

### Wire up the lifecycle hooks the workflow relies on
So that session-start/close automation actually runs instead of being wired-but-vacuous.
- [#8] [P2][M] Implement the analysed hooks (session-end clean-tree/staleness + SessionStart lessons-retrieval) and resolve the review-hook overlap — the **closure loop is whole**: Stop→propose (`propose_closures.py`), SessionStart→surface + `/review-closures` review/approve/close (`review_closures.py`), ADR-70 Tier-1; still remaining → session-end clean-tree/staleness hook, SessionStart **lessons-retrieval** (#4 territory), and the review-hook overlap · Done when: the remaining hooks run + are documented · refs 2026-05-29 hooks audit, ADR-70 (Tier-1 lifecycle hooks)
- [#12] [P2][M] Create the evolution .jsonl logs (or repoint hooks/protocol to evolution-log.md) + add one read-only session-close automation · Done when: the evolution machinery is non-vacuous · refs coherence-audit SK-3/HK-2/HK-3, ADR-70 (Tier-1 Stop-hook propose-closures)
- [#73] [P2][L] Bundle Tier-1 (git-as-capture + Stop-hook propose-closures skill + ruff gate + lesson-promotion skill + /boot review) as one methodology plugin and install it across all registered ecosystem repos · Done when: a single plugin install propagates the Tier-1 lifecycle to every registered repo with no per-repo re-derivation · refs ADR-70 (Tier 1)

---

## Lessons feedback loop
> As the methodology author, I want lessons to flow back into enforced rules, not sit in an archive.

### Make lessons an active feedback loop, not a passive archive
So that captured lessons reach runtime rules and stay enforceable.
- [#4] [P2][M] Build lessons-index.json + SessionStart retrieval + CLI query · Done when: lessons are queryable + surfaced at session start · refs ADR-35, ADR-70 (Tier-1 lesson-promotion)
- [#22] [P3][S] Broaden _LESSONS_H3_RE for an optional parenthetical (or reformat the 8 entries with sign-off) · Done when: the 8 parenthetical entries are ordering-checked · refs ADR-29

### Codify recurring patterns into the methodology
So that observed failure-modes become written guidance instead of recurring.
- [#34] [P3][S] Add the 4 posture-audit codifications to PLAYBOOK (stable-end-state, verify-destination, no-delete-canonical-dup, ADR-with-N=1) · Done when: the 4 land in PLAYBOOK · refs posture-audit H3/H4/T1/T2
- [#28] [P3][S] Codify the sage→apprentice metaphor pattern for teaching design intent · Done when: a short methodology section lands in PLAYBOOK/ESSENTIALS · refs HANDOFF_PROCESS v4 §3.1
- [#67] [P3][S] PLAYBOOK §7 polish: skill/command naming-convention note + orchestrator/worker how-to · Done when: both notes land in PLAYBOOK §7 · refs methodology-audit C10/C12

---

## Decision management
> As a reader of 65+ ADRs, I want decisions navigable and free of silent contradiction.

### Keep the decision corpus navigable and contradiction-aware
So that growth past 65 ADRs doesn't bury or quietly contradict prior decisions.
- [#2] [P1][L] Add contradiction-detection across decisions + an ownership model (amend vs new ADR vs clarification) · Done when: a detection mechanism + ownership rule exist · refs ADR-64 (consolidated-index sub-item done)
- [#23] [P3][M] Build a navigable supersedes/related/amends graph from ADR frontmatter (or an index doc) · Done when: the graph renders + is freshness-checked · refs posture-audit I1

### Codify the meta-decision rules
So that future sessions route decisions consistently (convene-vs-Path-A; relax-vs-gate).
- [#18] [P2][M] Codify the convene-vs-Path-A criterion in AI_COUNCIL_PROCESS/PLAYBOOK · Done when: the criterion is written · refs ADR-62/63/65
- [#27] [P3][M] Codify the cost/value-asymmetric relax-vs-gate criterion for drifted guards · Done when: a LESSON/ADR records the criterion · refs ADR-62/63, coherence-audit ML-2
- [#74] [P3][M] Codify the Workflow-escalation rule — when to escalate execution to a scoped Dynamic Workflow (heavy / cross-repo / large-repo / checked-twice), the heavy-execution analog of the Council (heavy-decision) on the decision ladder · Done when: the criterion is written alongside the convene-vs-Path-A (#18) and relax-vs-gate (#27) rules · refs ADR-70 (escalation rule), ADR-67

### Operationalize the Council decision loop
So that Council questions are gated and their verdicts return deterministically instead of being shuttled by hand.
- [#70] [P3][M] Operationalize the AI-Council process — implement the gated question→verdict→ADR loop per ADR-67 (templated question + self-gate + deterministic `council.return_dir` return; downstream pieces in ai-council + ~/.claude). Gate lifted 2026-06-02 — Phase-2 universalization is complete (all 5 repos unified), so this is now actionable. · Done when: the gated loop runs end-to-end (/council-question generates + self-gates → council runs → operator pastes verdict → ADR returns via council.return_dir) · refs ADR-67

### Close the small ADR cross-reference + registry amendments
So that the ADR web is internally consistent.
- [#19] [P3][S] Add a BACKLOG.md lifecycle entry to ADR-39 (formerly bundled with #20) · Done when: ADR-39 registry includes BACKLOG.md · refs ADR-39/41
- [#21] [P3][M] Decide register/exempt/hybrid for the non-handoff templates/ class · Done when: the class decision is recorded in ADR-39 · refs ADR-39

---

## Canonical-file integrity
> As any agent reading this repo, I want the canonical files accurate and current.

### Keep canonical files accurate
So that stale ground truth stops silently misleading sessions (the repo's own VISION is "drift detected proactively").
- [#10] [P2][M] Decide TOKEN-LOG placement + align the docs — the file is at `logs/TOKEN-LOG.md` but CLAUDE/ARCHITECTURE/PLAYBOOK reference it bare (implying root) vs the ADR-59 ALL-CAPS-at-root rule; move-to-root vs docs-say-`logs/` is the operator's call (the broader doc-truth set was already closed by the 2026-06-01 `chore/doc-coherence-audit` — git history + JOURNAL hold that record) · Done when: TOKEN-LOG placement decided + docs aligned · refs coherence-audit 2026-06-01
- [#35] [P3][S] Fix the self-owned low-severity cleanups (ARCHITECTURE diagram attribution + SBAR label; VISION adoption-signal + stale last_reviewed) · Done when: WF-3 + GO-1/2 resolved · refs coherence-audit
- [#71] [P3][S] Reconcile ENVIRONMENT.md's `~/.claude/` directory tree with live contents (commands = boot/codex-review/evolve/session-summary, not handoff; skills = gotchas + verify; agents/hooks already match) · Done when: the ENVIRONMENT `~/.claude/` tree matches `ls ~/.claude/{commands,skills}` · refs G6 process-hardening sweep

### Keep the day-to-day docs right-sized and current
So that the cheat-sheet and architecture stay scannable as conventions accrue.
- [#5] [P2][M] Add high-leverage ESSENTIALS cheats for ADRs 35-63 under the one-page constraint · Done when: the chosen cheats land + ESSENTIALS stays ~1 page · refs posture-audit C2
- [#41] [P3][S] Split ARCHITECTURE §Processes into PROCESS.md if it grows past the comfort threshold · Done when: re-evaluated at the next process addition · refs ADR-51

---

## Cross-repo universalization
> As the disseminator, I want every child repo to converge on the universal baseline.

### Converge every child repo on the universal baseline
So that "open any repo, same layout/governance" actually holds.
- [#47] [P3][S] Confirm status of corp-knowledge-extractor / corp-by-os / corp-rfp-agent · Done when: each is classified (renamed/archived/uncloned/dropped) · refs 2026-05-11 audit
- [#9] [P2][M] Inventory skills across repos, classify repo-specific vs universal, propose a canonical home · Done when: a skills inventory + universalization proposal exists · refs VISION cross-repo consistency

### Make new-repo scaffolding correct-by-default
So that a new repo inherits the full baseline in one step, not by re-derivation.
- [#16] [P2][M] Collapse workspace-{S,M,L}.code-workspace into one maximal scale-adaptive template · Done when: one workspace template + element-selection guidance exist · refs operator Q5
- [#17] [P2][M] Encode ADR-54–63 high-leverage guidance into templates/CLAUDE-md-template.md (structural lock + frontmatter already done at v2.2; the stale "§11 last-5 = 61-65" sub-spec is dropped — the template uses generic `ADR-NN` placeholders by design) · Done when: the template's guidance reflects ADR-54–63 · refs durability-audit J1, template v2.2
- [#43] [P3][L] Decide + (if yes) author a one-step new-repo scaffold (ADR + templates/new-repo-skeleton/, no scripts) · Done when: decision recorded + scaffold authored if approved · refs durability-audit J6

---

## Tooling & evaluation
> As the operator, I want low-friction tooling and timely tech adoption.

### Cut session friction with better tooling
So that cognitive overhead per session drops.
- [#32] [P3][M] Audit VS Code extensions + workflow templates + tooling integration; produce a recommendation · Done when: a recommendation lands · refs VISION (tooling support)
- [#33] [P3][M] Build the 'Pinned Files' VS Code extension (TreeView of canonical files, local) · Done when: it loads + single-click opens + operator confirms ergonomic gain · refs trigger=keybindings-friction
- [#37] [P3][S] Add a workspace-sort-change verification rule (read the merged PR + a visual editor check) · Done when: the rule lands in PLAYBOOK/ESSENTIALS · refs ADR-59 amendment
- [#38] [P3][S] Codify small=single-root / large=multi-root workspace decision · Done when: an ADR-59 amendment or PLAYBOOK note lands · refs ADR-59
- [#39] [P3][S] Codify entry-scripts → scripts/ in PLAYBOOK root-hygiene · Done when: the convention is written · refs 2026-05-27 retrofit

### Decide the undecided artifact/tool models
So that cadence-less artifacts and unevaluated tools don't rot or get adopted blind.
- [#14] [P2][L] Decide the ecosystem/ folder operating model (regenerated snapshot / continuous-audit substrate / retire) · Done when: the model + cadence + ownership are recorded · refs Council-scope
- [#30] [P3][M] Evaluate Kimi K2 (capability / cost / integration); Council decision on adoption level · Done when: a Council verdict recommends an adoption level · refs VISION velocity
- [#75] [P3][M] Adopt + exercise Tier 3 on a first scoped corp-monorepo deep-audit Dynamic Workflow (scope first, then run) · Done when: one scoped corp-monorepo audit Workflow has run end-to-end and its fit + token cost are assessed · refs ADR-70 (Tier 3)

---

**About this file** — open `.dev-knowledge` work as a story map (ADR-66): Big Picture → Theme → User Story → Task. Stories are human (goal + `So that`); tasks carry `[#id] [P][size] · Done when · refs`. Done tasks **leave** (ADR-65); git is the implementation record (`git log --grep 'closes \[#'`). Child-repo execution items live in `docs/audits/2026-06-01-child-repo-relocation-proposal.md`. Schema: PLAYBOOK §10; machine-checked by `scripts/validate_backlog.py`.

**Grooming log:** 2026-05-09 · 2026-05-23 · 2026-05-24 · 2026-05-31 (marathon-arc) · 2026-06-01 (ADR-64/65 migration + readability + ADR-66 story-map) · 2026-06-02 (git-verified retroactive closure: retired #29/#31/#40/#44/#45/#46; re-scoped #17/#13; updated #70/#10; ADR-69 records the #44 reach model) · 2026-06-02 (ADR-70 incorporation: annotated #13/#8/#12/#72/#4 with `refs ADR-70` as the three-tier build units; added #73 Tier-1 plugin bundle + cross-repo install, #74 Workflow-escalation rule, #75 first scoped corp-monorepo Tier-3 Workflow) · 2026-06-02 (closes [#13]: ruff pre-commit gate wired + proven; #13 retired). Next quarterly: 2026-07-01.
