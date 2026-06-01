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
- [#13] [P2][S] Add the ruff pre-commit hook, or correct the docs that claim it · Done when: ruff is enforced OR the docs no longer claim it · refs coherence-audit HK-1
- [#15] [P2][M] Add hyphen-only-separator enforcement (pre-commit + Action) with a scoped path set + exceptions · Done when: a non-conforming new filename is blocked · refs ADR-34

### Extend structural validation to more governance artifacts
So that drift in transcripts, ADRs, and folders is caught cheaply, not by reviewer luck.
- [#7] [P2][M] Apply the audit.py #8 structural-validator pattern to Council transcripts + ADRs (frontmatter/supersession/template) · Done when: registered checks + tests folded into health · refs scripts/audit.py #8/#9
- [#36] [P3][M] Add read-only check_folder_semantics asserting each docs/ subfolder carries one ADR-60 role · Done when: the check ships with fixtures + tests · refs ADR-60
- [#42] [P3][S] Decide whether mermaid-theme check #7 expands beyond ARCHITECTURE.md (extend paths or accept) · Done when: scope decision recorded · refs durability-audit J4

### Wire up the lifecycle hooks the workflow relies on
So that session-start/close automation actually runs instead of being wired-but-vacuous.
- [#8] [P2][M] Implement the analysed hooks (session-end clean-tree/staleness + SessionStart lessons-retrieval) and resolve the review-hook overlap · Done when: the hooks run + are documented · refs 2026-05-29 hooks audit
- [#12] [P2][M] Create the evolution .jsonl logs (or repoint hooks/protocol to evolution-log.md) + add one read-only session-close automation · Done when: the evolution machinery is non-vacuous · refs coherence-audit SK-3/HK-2/HK-3

---

## Lessons feedback loop
> As the methodology author, I want lessons to flow back into enforced rules, not sit in an archive.

### Make lessons an active feedback loop, not a passive archive
So that captured lessons reach runtime rules and stay enforceable.
- [#4] [P2][M] Build lessons-index.json + SessionStart retrieval + CLI query · Done when: lessons are queryable + surfaced at session start · refs ADR-35
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

### Close the small ADR cross-reference + registry amendments
So that the ADR web is internally consistent.
- [#19] [P3][S] Add a BACKLOG.md lifecycle entry to ADR-39 (bundle with #20) · Done when: ADR-39 registry includes BACKLOG.md · refs ADR-39/41
- [#20] [P3][S] Add a dated amendment to ADR-41 cross-referencing ADR-47/64/65 · Done when: the amendment lands · refs ADR-41/47/64/65
- [#21] [P3][M] Decide register/exempt/hybrid for the non-handoff templates/ class · Done when: the class decision is recorded in ADR-39 · refs ADR-39

---

## Canonical-file integrity
> As any agent reading this repo, I want the canonical files accurate and current.

### Keep canonical files accurate
So that stale ground truth stops silently misleading sessions (the repo's own VISION is "drift detected proactively").
- [#10] [P2][M] Fix the doc-truth drifts (CLAUDE §7/§8; ARCHITECTURE validators [done in #3] + governing-ADRs + §Authority "audit.py pending full implementation" stale (ships 10 checks) + handoff diagram/version v3.4->v4.3.1 (diagram describes the retired 13-file flow) + §Validators "audit.py manual invocation" now imprecise (health is pre-commit-gated since [#69]); LESSONS descriptor; ruff claim; TOKEN-LOG path) · Done when: all listed corrected · refs coherence-audit (SK/CD/WF/ML) + methodology-engine session 2026-06-01
- [#35] [P3][S] Fix the self-owned low-severity cleanups (ARCHITECTURE diagram attribution + SBAR label; VISION adoption-signal + stale last_reviewed) · Done when: WF-3 + GO-1/2 resolved · refs coherence-audit

### Keep the day-to-day docs right-sized and current
So that the cheat-sheet and architecture stay scannable as conventions accrue.
- [#5] [P2][M] Add high-leverage ESSENTIALS cheats for ADRs 35-63 under the one-page constraint · Done when: the chosen cheats land + ESSENTIALS stays ~1 page · refs posture-audit C2
- [#41] [P3][S] Split ARCHITECTURE §Processes into PROCESS.md if it grows past the comfort threshold · Done when: re-evaluated at the next process addition · refs ADR-51

---

## Cross-repo universalization
> As the disseminator, I want every child repo to converge on the universal baseline.

### Converge every child repo on the universal baseline
So that "open any repo, same layout/governance" actually holds.
- [#45] [P2][M] Apply ADR-33/34/35/37/38/39/41 to ai-council + corp-monorepo (ai-council substantially done; corp-monorepo not started) · Done when: both repos pass the baseline audit · refs VISION Disseminator
- [#46] [P3][M] Extend the ADR-63 scrum-master review cycle to remaining repos (corp-monorepo → verify undiscovered → corp-ops/sca) · Done when: each repo has had a review cycle · refs ADR-63
- [#47] [P3][S] Confirm status of corp-knowledge-extractor / corp-by-os / corp-rfp-agent · Done when: each is classified (renamed/archived/uncloned/dropped) · refs 2026-05-11 audit
- [#9] [P2][M] Inventory skills across repos, classify repo-specific vs universal, propose a canonical home · Done when: a skills inventory + universalization proposal exists · refs VISION cross-repo consistency
- [#31] [P3][L] Council-level plan for migrating one significant repo to standards (repo unnamed until scoped) · Done when: a sequenced migration plan exists · refs VISION Disseminator

### Give the auditor cross-repo reach
So that drift across repos is caught without a manual sweep.
- [#29] [P3][M] Implement the tool-driven cross-repo compliance run (`audit ecosystem --all`, Layer-2 read-only) · Done when: one command produces an adoption/compliance report · refs ADR-36 (overlaps #44)
- [#44] [P3][M] Decide how audit.py checks reach child repos (per-repo port / cross-repo runner / governance-only) · Done when: the reach decision is recorded · refs durability-audit J5 (overlaps #29)

### Make new-repo scaffolding correct-by-default
So that a new repo inherits the full baseline in one step, not by re-derivation.
- [#16] [P2][M] Collapse workspace-{S,M,L}.code-workspace into one maximal scale-adaptive template · Done when: one workspace template + element-selection guidance exist · refs operator Q5
- [#17] [P2][M] Refresh templates/CLAUDE-md-template.md to encode ADRs 54-63 (§11 last-5 = 61-65) · Done when: the template is current · refs durability-audit J1
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
- [#40] [P3][S] Make the requirements*.txt dot-prefix exception prominent in ADR-59 (or close no-op) · Done when: clarified or closed · refs ADR-59 Exceptions

### Decide the undecided artifact/tool models
So that cadence-less artifacts and unevaluated tools don't rot or get adopted blind.
- [#14] [P2][L] Decide the ecosystem/ folder operating model (regenerated snapshot / continuous-audit substrate / retire) · Done when: the model + cadence + ownership are recorded · refs Council-scope
- [#30] [P3][M] Evaluate Kimi K2 (capability / cost / integration); Council decision on adoption level · Done when: a Council verdict recommends an adoption level · refs VISION velocity

---

**About this file** — open `.dev-knowledge` work as a story map (ADR-66): Big Picture → Theme → User Story → Task. Stories are human (goal + `So that`); tasks carry `[#id] [P][size] · Done when · refs`. Done tasks **leave** (ADR-65); git is the implementation record (`git log --grep 'closes \[#'`). Child-repo execution items live in `docs/audits/2026-06-01-child-repo-relocation-proposal.md`. Schema: PLAYBOOK §10; machine-checked by `scripts/validate_backlog.py`.

**Grooming log:** 2026-05-09 · 2026-05-23 · 2026-05-24 · 2026-05-31 (marathon-arc) · 2026-06-01 (ADR-64/65 migration + readability + ADR-66 story-map). Next quarterly: 2026-07-01.
