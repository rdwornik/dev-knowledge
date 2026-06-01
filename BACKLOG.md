# .dev-knowledge BACKLOG

Open and in-progress `.dev-knowledge` work only. **Done items leave the file** (git history + the per-session JOURNAL entry are the record — ADR-65); there is no archive file (CLAUDE.md §5). Schema + layout: **PLAYBOOK §10 / ADR-64 / ADR-65**; machine-checked by `scripts/validate_backlog.py`. One item lives in exactly one section (section = status); repo affiliation is the `repo:` field.

**Grooming log:** 2026-05-09 (P1 HANDOFF_PROCESS) · 2026-05-23 (tier-deprecation) · 2026-05-24 (post-arc audit) · 2026-05-31 (marathon-arc reconciliation) · **2026-06-01 (ADR-64/65 migration: 42 done items retired, restructured to status-and-priority, ids assigned)**. Next quarterly: 2026-07-01.

---

## Now

_(nothing in progress — next actions are the top of `## Open` → `### P1`)_

---

## Open

### P1

### [P1] Adversarial fresh-eyes pass in routine handoff generation
- **id:** 1
- **repo:** .dev-knowledge
- **status:** open
- **What:** Extend triangulation from the promotion gate to routine handoff artifacts. v4.3.1 (caveat N1) guards process *versioning* only; every routine handoff still rides on Phase-2 self-verification — the insider-only coverage (~25%) the v4 arc disproved. Options: (a) lightweight skeptical sub-prompt in every Phase 2; (b) periodic adversarial audit (every N handoffs); (c) full agent-framework with an adversarial layer. Council scope.
- **Why:** The curse-of-knowledge result is empirical (insider review caught 1/4 critical; fresh-eyes 4/4). Routine bundles inherit the blind spot.
- **Added:** 2026-05-30 by rob (v4.3.1 caveat-patch session)
- **Refs:** `protocols/AGENT_FRAMEWORK.md`; HANDOFF_PROCESS v4.3.1 Amendment item A; `scripts/audit.py` #8/#9

### [P1] Council decisions management consolidation
- **id:** 2
- **repo:** .dev-knowledge
- **status:** open
- **What:** Decision artifacts are dispersed across `docs/decisions/`, `transcripts/`, and per-file ADR refs. Remaining sub-items (the consolidated-index sub-item closed 2026-05-11): (1) contradiction-detection mechanism between decisions over time; (2) ownership model for decision evolution — amendment vs new ADR vs conversational clarification. Both Council territory.
- **Why:** As ADR count grows (65+), navigating + drift-detecting compounds; governance debt accrues silently.
- **Added:** 2026-05-09 by rob

### [P1] Sacred-files maintenance enforcement
- **id:** 3
- **repo:** .dev-knowledge
- **status:** open
- **What:** Canonical files drift because sessions forget to update them at boundaries. `.dev-knowledge` list is 8 files (ARCHITECTURE/BACKLOG/CLAUDE/CONTRIBUTING/JOURNAL/LESSONS/VISION + project CLAUDE; CHANGELOG dropped 2026-05-16). Need an enforcement mechanism: `last_reviewed` staleness pre-commit, session-end checklist skill, or diff-based staleness detection. Enumerate per-repo lists, design, implement ≥1, validate.
- **Why:** Stale ground truth silently misleads future sessions. The sacred-files list itself was found stale 2026-05-20.
- **Added:** 2026-05-09 by rob

### P2

### [P2] Lessons activation P1 implementation
- **id:** 4
- **repo:** .dev-knowledge
- **status:** open
- **What:** Build lessons-index.json + retrieval (SessionStart hook) + querying (CLI) per ADR-35.
- **Why:** Activates LESSONS.md from passive archive to active feedback loop; bidirectional `corrections.jsonl` ↔ LESSONS.md ↔ `~/.claude/rules/`.
- **Added:** 2026-04-30 by rob

### [P2] ESSENTIALS.md cheat-sheet additions for ADRs 35-63
- **id:** 5
- **repo:** .dev-knowledge
- **status:** open
- **What:** Review which of ADRs 35-63 warrant high-leverage ESSENTIALS cheats (lessons retrieval 35, audit triggers 36, two-phase handoff 37, BACKLOG cadence 41, ARCHITECTURE 51, CLAUDE single-instruction 53, Codex global 54, visual pattern 59, docs taxonomy 60, v4 ratification 62, scrum-master 63). ADR-61 parallel-sessions + the ADR-64/65 Backlog cheat already landed. Apply the "Keep under 1 page" constraint — judgment call.
- **Why:** ESSENTIALS update trigger is methodology change; significant changes accumulated since 2026-04-30. Additions require pruning or explicit relaxation.
- **Added:** 2026-04-30 by rob; scope expanded 2026-05-20, 2026-05-31

### [P2] Handoff advisory framing leaks into receiver behavior
- **id:** 6
- **repo:** .dev-knowledge
- **status:** open
- **What:** Advisory framing in a handoff ("REST recommended") propagated to a receiver chat as unprompted session-end suggestions despite an explicit operator rule against it. Classify root cause (handoff design vs receiver discipline vs both) and propose mitigation before the next high-stakes handoff.
- **Why:** ADR-37 assumes handoff content is informational; in practice advisory framing becomes behavioral pressure. Likely recurs with other framings.
- **Added:** 2026-05-11 by rob
- **Refs:** ADR-37, ADR-42, LESSONS 2026-05-11

### [P2] Extend audit-check enforcement to other governance artifacts
- **id:** 7
- **repo:** .dev-knowledge
- **status:** open
- **What:** Apply the read-only structural-validator pattern (audit.py #8) to AI Council transcripts (naming + cover-letter + verdict structure) and ADRs (frontmatter + supersession field + template alignment). Each a registered check with fixtures + tests, folded into the health gate.
- **Why:** #8/#9 prove the lint-at-health-time pattern catches drift cheaply; ADRs + transcripts carry the same risk, currently caught only by reviewer judgment.
- **Added:** 2026-05-29 by rob
- **Refs:** `scripts/audit.py` #8/#9; `protocols/AGENT_FRAMEWORK.md`

### [P2] Hooks audit + consolidation + workflow-automation patterns
- **id:** 8
- **repo:** .dev-knowledge
- **status:** open
- **What:** Implementation phase (the 2026-05-29 inventory + automation-pattern analysis is done, `docs/audits/scratch/2026-05-29-ecosystem-hooks.md`). Add/consolidate the actual hooks: session-end clean-tree / canonical-file-staleness check (pairs with id 3), lessons-retrieval on SessionStart (pairs with id 4); resolve the Codex-vs-internal review-hook overlap. Findings HK-1..HK-4 are tracked in ids 9-12/coordination.
- **Why:** Lifecycle hooks are the mechanical-enforcement layer ("convention without enforcement drifts"); their use + expansion deserve explicit implementation, not implicit habit.
- **Added:** 2026-05-09 by rob; scope expanded 2026-05-24

### [P2] Skills universalization across repos
- **id:** 9
- **repo:** .dev-knowledge
- **status:** open
- **What:** Cross-repo skills review: (a) inventory all skills across repos, (b) classify repo-specific vs cross-ecosystem, (c) identify universalization targets that should live in `.dev-knowledge`, (d) propose a canonical location. Output: inventory + universalization proposal.
- **Why:** Redundantly-defined skills drift; universalization reduces maintenance + ensures consistency.
- **Added:** 2026-05-09 by rob

### [P2] Ecosystem: doc-truth sweep (CLAUDE.md + ARCHITECTURE self-description)
- **id:** 10
- **repo:** .dev-knowledge
- **status:** open
- **What:** Eight doc-accuracy drifts, all small edits: CLAUDE §7 omits `/codex-review`+`/evolve` (SK-1); §8 calls commands "skills" + omits `verify` (SK-2); §7 `/handoff` says v3.3.3 not v4 (CD-1); footer date vs §12 (CD-2); ARCHITECTURE governing-ADRs omits 59/61 (WF-1); ARCHITECTURE validators list repeats the false ruff-pre-commit claim + lists non-existent `backlog_extract.py` + omits codemap-freshness (WF-2); LESSONS "oldest-top" descriptor vs newest-top (ML-1 — verify vs ADR-29); TOKEN-LOG.md location vs CLAUDE §4/§5 (ML-4).
- **Why:** The repo whose VISION is "drift detected proactively" is the locus of drift; none breaking, all trust-eroding.
- **Added:** 2026-05-29 by rob
- **Refs:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md` §3/§4

### [P2] Ecosystem: feedback-loop enforcement (un-enforced guards → gate)
- **id:** 11
- **repo:** .dev-knowledge
- **status:** open
- **What:** Convert LESSON #9's cross-case-trace guard from advisory prose into an amendment checklist/gate (Layer-2: checklist, not orchestration). ML-3 (promote the v3.4-abort lesson) done in the 2026-05-30 LESSONS batch; ML-2 partly addressed by ADR-63 (review-authority backstop). **Open:** the literal guard→gate conversion.
- **Why:** Structural root cause of the v3.4 abort; predicts recurrence on the next multi-surface amendment unless the guard becomes a gate.
- **Added:** 2026-05-29 by rob
- **Refs:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (ML-2/ML-3); ADR-63

### [P2] Ecosystem: evolution memory logs missing + no session-close automation
- **id:** 12
- **repo:** .dev-knowledge
- **status:** open
- **What:** boot.md + Self-Evolution Protocol + SessionStart/Stop hooks read `sessions/violations/corrections/observations.jsonl` — none exist (only `learned-rules.md` + `evolution-log.md`); the machinery is wired but vacuous. Stop hook does no functional session-close automation. Fix: create the logs OR repoint hooks+protocol to `evolution-log.md`; add one read-only session-close automation. (owner: `~/.claude` runtime + self)
- **Why:** Session-trend + correction-promotion tracking silently does nothing; `/boot` reports "no sessions.jsonl."
- **Added:** 2026-05-29 by rob
- **Refs:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (SK-3/HK-2/HK-3/SK-5)

### [P2] Ecosystem: ruff lint enforcement for .dev-knowledge
- **id:** 13
- **repo:** .dev-knowledge
- **status:** open
- **What:** CLAUDE §9/§4 + ARCHITECTURE document ruff as a pre-commit hook, but it is NOT in `.pre-commit-config.yaml` (only normalize-dated-headers + codemap-freshness). Decide: add the ruff hook, or correct the docs. (Foldable into id 10.)
- **Why:** A load-bearing convention documented-as-enforced is actually manual; a ruff violation could land while docs imply it was blocked.
- **Added:** 2026-05-29 by rob
- **Refs:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (HK-1)

### [P2] Ecosystem-folder operating-model design (snapshot vs continuous audit)
- **id:** 14
- **repo:** .dev-knowledge
- **status:** open
- **What:** Define the operating model for the `ecosystem/` folder — (a) periodically-regenerated static snapshot, (b) substrate for a continuous cross-repo audit process, or (c) retire in favor of on-demand audit runs. Design ownership, regeneration cadence/trigger, relationship to `scripts/audit.py` cross-repo reach, Layer-2 read-only invariant.
- **Why:** Operator flagged 2026-05-31 that the folder exists but its operating model is unknown — a static snapshot is not a process; without a model it rots (tech-radar precedent). Council-scope; pairs with ids 27, 39.
- **Added:** 2026-05-31 by rob

### [P2] CI enforcement of hyphen-only separator rule
- **id:** 15
- **repo:** .dev-knowledge
- **status:** open
- **What:** Pre-commit hook + GitHub Action enforcing hyphen-only separators in new file/folder names. Scope TBD: which paths (`.md` only vs all), generated-artifact handling, exceptions list.
- **Why:** Convention without enforcement drifts; manual discipline insufficient per the 2026-05-11 audit.
- **Added:** 2026-05-11 by rob
- **Status note:** scope decision needed before implementation (small Council question or conversational).

### [P2] Remove tier-residue from .dev-knowledge workspace templates
- **id:** 16
- **repo:** .dev-knowledge
- **status:** open
- **What:** Collapse `templates/workspace-{S,M,L}.code-workspace` (three richness-tiered files) + PLAYBOOK §"VS Code workspace" into one maximal `.code-workspace` template from which elements are selected by repo complexity (not three scale-keyed variants). S/M/L was de-tiered in PLAYBOOK v1.1 but three files persist.
- **Why:** Operator decision (universalization Q5): "one complex template, scale-adaptive by element selection, NOT scale-different templates." Affects the template framework, not any child repo; may warrant a small ADR/PLAYBOOK amendment.
- **Added:** 2026-05-26 by rob
- **Refs:** `protocols/PLAYBOOK.md` §VS Code workspace; `templates/workspace-{S,M,L}.code-workspace`

### [P2] templates/CLAUDE-md-template.md refresh — encode ADRs 54-63
- **id:** 17
- **repo:** .dev-knowledge
- **status:** open
- **What:** Refresh `templates/CLAUDE-md-template.md` (v2.1, predates ADRs 54-63): §3 mermaid theme directive (ADR-51 v2); §4 visual pattern (59) + docs taxonomy variant (60); §5 worktree pre-flight (61); §7 `/handoff` + HANDOFF_PROCESS ref; §11 rotate to last-5 ADRs (now 61-65). Bump version.
- **Why:** Durability-audit J1 — "the largest single durability gap": the single new-repo scaffolding artifact for agent-instruction content; stale → every new repo inherits stale conventions.
- **Added:** 2026-05-28 by rob; scope expanded 2026-05-31
- **Refs:** `docs/audits/2026-05-28-universalization-durability-audit.md`

### [P2] AI Council convene-vs-Path-A decision criterion
- **id:** 18
- **repo:** .dev-knowledge
- **status:** open
- **What:** Codify when an architecture decision goes to a full Council convene vs a Path-A direct ADR. ADR-62/63/65 were Path-A (post-hoc record of a decision already made + validated), but the justifying criterion lives only in JOURNAL prose. Add the rule to `protocols/AI_COUNCIL_PROCESS.md` (or PLAYBOOK).
- **Why:** AI_COUNCIL_PROCESS v1.0 assumes every architecture decision convenes; the arc established Path A as legitimate for post-hoc records. Pairs with id 21 (relax-vs-gate).
- **Added:** 2026-05-31 by rob

### P3

### [P3] ADR-39 amendment — add BACKLOG.md lifecycle entry
- **id:** 19
- **repo:** .dev-knowledge
- **status:** open
- **What:** Amend ADR-39 registry to add a BACKLOG.md entry per ADR-41 (bundle with id 20 to minimize ADR churn).
- **Why:** Lifecycle compliance per ADR-39.
- **Added:** 2026-04-30 by rob

### [P3] ADR-41 amendment — cross-reference ADR-47 (BACKLOG schema)
- **id:** 20
- **repo:** .dev-knowledge
- **status:** open
- **What:** Add a dated amendment to ADR-41 (file-mandate authority) cross-referencing ADR-47 (schema) — and now ADR-64/65 (architecture/disposition). Small amendment in ADR-41 §Storage + Related.
- **Why:** Without the cross-ref, readers treat ADR-41 as the only BACKLOG authority and miss the operational schema. (Deferred from the 2026-06-01 migration step-2 reconcile, which aligned at the PLAYBOOK layer only — editing the immutable ADR is this item's proper channel.)
- **Added:** 2026-05-15 by rob

### [P3] ADR-39 registry decision — unregistered template files (class-level)
- **id:** 21
- **repo:** .dev-knowledge
- **status:** open
- **What:** Decide register vs exempt vs hybrid for the non-handoff `templates/` class (`ADR-template.md`, `ARCHITECTURE-template.md`, `CLAUDE-md-template.md`, `codex-review-config-template.md`, `prompt-template.md`, `scrum-master-cover-letter.md`, `workspace-{S,M,L}.code-workspace`, `templates/archive/`). The two handoff templates were registered 2026-05-25.
- **Why:** ADR-39 says "every file MUST have 6 lifecycle elements"; either extend the registry or formally narrow scope. Drift risk if neither.
- **Added:** 2026-04-30 by rob

### [P3] LESSONS.md parenthetical-qualifier entries escape the dated-entry audit regex
- **id:** 22
- **repo:** .dev-knowledge
- **status:** open
- **What:** 8 entries use `### YYYY-MM-DD (qualifier) |`; `_LESSONS_H3_RE` requires the date immediately before `|`, so they are invisible to the ordering check. Decide: (a) broaden the regex to allow an optional parenthetical, or (b) reformat the 8 entries (needs operator sign-off under ADR-29 append-only).
- **Why:** Latent coverage gap — future misordering around these 8 would not be caught.
- **Added:** 2026-05-16 by rob

### [P3] ADR relationship index / supersession graph
- **id:** 23
- **repo:** .dev-knowledge
- **status:** open
- **What:** With 65+ ADRs, the supersedes/supersededBy/related/amends structure is not navigable. Build either (a) a machine-generated graph from ADR frontmatter, or (b) an index doc with explicit edges (DOT/Mermaid/table). Same shape as the codemap generator.
- **Why:** Fresh readers miss relationship structure; cost compounds as the corpus grows. Pairs with id 2 (contradiction detection).
- **Added:** 2026-05-20 by rob

### [P3] CLAUDE.md §4 cites a stale known-failing test
- **id:** 24
- **repo:** .dev-knowledge
- **status:** open
- **What:** CLAUDE §4 says "known pre-existing failure: `test_audit_run_passes_structural_checks_on_synthetic_repo`" — but it passes and the suite is green. Remove the known-failure clause (one-line edit). (Fold into id 10 doc-truth sweep.)
- **Why:** A false "known failure" in the session contract masks real regressions.
- **Added:** 2026-05-24 by rob

### [P3] Process refinements deferred from the v4.3.1 caveat patch
- **id:** 25
- **repo:** .dev-knowledge
- **status:** open
- **What:** Seven non-blocking refinements: (1) semantic tag-lint (audit.py #10, Council-scope); (2) periodic fresh-eyes audit cadence; (3) AI Council CLI example in `02_METHODOLOGY.md.tmpl`; (4) ML namespace expansion in 04_RECENT; (5) operating-mode wording in `01_ROLE.md.tmpl`; (6) AI Council auto-routing claim verify; (7) "passive storage" reframe in `03_PROJECT.md.tmpl`. All 7 remain open at the durable `.tmpl` level (the session-2 bundle exercised (3)/(7) at instance level only).
- **Why:** Surfaced by the v4.3 fresh-eyes review as minor/clarity items; batched to avoid queue fragmentation.
- **Added:** 2026-05-30 by rob
- **Refs:** `templates/handoff/*.tmpl`; `scripts/audit.py` #9

### [P3] Phase-1 handoff: operator-invariants section
- **id:** 26
- **repo:** .dev-knowledge
- **status:** open
- **What:** Add a small "operator invariants" section to the Phase-1 interview / apprentice bundle capturing defaults a fresh chat should assume rather than re-ask: clean-git-tree-after-handoff, immediate-merge habit, three-domain separation, operator-paced multi-step workflows.
- **Why:** Surfaced 2026-05-31 when a fresh chat over-asked despite strong priors; operationalizes the 2026-05-30 inheritor-pushback LESSON.
- **Added:** 2026-05-31 by rob

### [P3] Relax-vs-gate principle for drifted guards (paired-ADR tension)
- **id:** 27
- **repo:** .dev-knowledge
- **status:** open
- **What:** ADR-62 (relax the Council-for-architecture guard) and ADR-63 (gate the scrum-master pattern) prescribe opposite cures for the same disease (un-enforced guard drift). The implicit cost/value-asymmetric reasoning (gate when cost low + catch-value high; relax when cost high + retroactive value low) is never articulated. Candidate output: a LESSONS entry or small ADR.
- **Why:** Sharpest cross-ADR finding from the ADR-62/63 fresh-eyes review; without a reconciling principle, future guard-drift decisions inherit the implicit reasoning.
- **Added:** 2026-05-30 by rob
- **Refs:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md` (ML-2)

### [P3] Incorporate metaphor-based communication into PLAYBOOK + ESSENTIALS
- **id:** 28
- **repo:** .dev-knowledge
- **status:** open
- **What:** Codify a small methodology section on communicating design intent via concrete metaphors (the sage→apprentice / *mędrzec–uczeń* framing that fixed the methodology-quiz interview defect). Capture the patterns and when to reach for them.
- **Why:** Bare ADR-number/abstract-mechanics communication is high-friction; a metaphor carries the *why* in one image. Worth generalizing.
- **Added:** 2026-05-29 by rob
- **Status note:** separate focused session; do NOT bundle with code/process changes.

### [P3] Cross-repo audit (Phase 3) — audit-tool-driven compliance run
- **id:** 29
- **repo:** .dev-knowledge
- **status:** open
- **What:** The audit tool runs across all repos with VISION.md and generates an ecosystem compliance report verifying adoption of ratified ADRs. Manual cross-repo audits delivered the intent (2026-05-29 coherence audit; 2026-05-27 retrofit verification); **open:** the tool-driven run (`audit ecosystem --all`, overlaps id 40 option b; Layer-2 read-only).
- **Why:** Validates universalization is actually adopted (not just ratified); drift detection over time.
- **Added:** 2026-04-30 by rob

### [P3] Kimi K2 model integration evaluation
- **id:** 30
- **repo:** .dev-knowledge
- **status:** open
- **What:** Evaluate Kimi K2: (a) capability for Council debate / code-gen / reasoning, (b) cost vs Claude per task type, (c) integration patterns. Decision artifact: Council debate recommending adoption level.
- **Why:** Significantly lower cost per Rob; velocity in LLM adoption is a competitive advantage. Council before production use.
- **Added:** 2026-05-09 by rob

### [P3] Large repo migration preparation
- **id:** 31
- **repo:** .dev-knowledge
- **status:** open
- **What:** Plan the structural migration of one significant ecosystem repo (folder/naming, sacred-files, scope tags, ADR adoption). Council-debate-level design before execution. Specific repo not named until a planning session scopes it.
- **Why:** Migration is disruptive if unplanned; early planning enables correct sequencing.
- **Added:** 2026-05-09 by rob

### [P3] VS Code productivity maximization
- **id:** 32
- **repo:** .dev-knowledge
- **status:** open
- **What:** Maximize Claude Code + git productivity via VS Code tooling: extensions audit, workflow templates, integration with validators/hooks/git. Output: extensions + settings recommendation.
- **Why:** Low-friction tooling reduces cognitive overhead. Deferred until higher-priority methodology items close.
- **Added:** 2026-05-09 by rob

### [P3] Custom "Pinned Files" VS Code extension for canonical-doc access
- **id:** 33
- **repo:** .dev-knowledge
- **status:** open
- **What:** TreeView in Explorer showing pinned canonical files (VISION/JOURNAL/BACKLOG/ARCHITECTURE/LESSONS/CLAUDE), configurable via `pinnedFiles.paths`, single-click to open. ~100-150 LOC TS (TreeDataProvider), local install. Acceptance: loads in the workspace, configurable, visible without leaving the file tree, single-click opens, operator confirms ergonomic gain.
- **Why:** Keybindings (Ctrl+Alt+V/J/B/R/L/C) give keyboard access but no visual at-a-glance presence; multi-root workspaces can't pin individual files natively.
- **Added:** 2026-05-24 by rob
- **Status note:** trigger = 1-week keybindings trial shows friction, or operator decides proactively.

### [P3] PLAYBOOK codifications from the 2026-05-19 posture audit
- **id:** 34
- **repo:** .dev-knowledge
- **status:** open
- **What:** Four candidate PLAYBOOK additions (N≥2 each): (1) governance docs phrased as stable end-state, transient status lives in JOURNAL; (2) verify destination before drop; (3) no-delete exception for canonical-source duplicates; (4) ADR-with-N=1 valid for singular choices. Bundle into one PLAYBOOK update.
- **Why:** Each codification prevents an already-observed failure mode from recurring.
- **Added:** 2026-05-20 by rob
- **Refs:** `docs/audits/2026-05-19-dev-knowledge-posture-audit.md` (H3/H4/T1/T2)

### [P3] Ecosystem: low-severity cleanups (self-owned subset)
- **id:** 35
- **repo:** .dev-knowledge
- **status:** open
- **What:** Self-owned low-pri items from the 2026-05-29 coherence audit: ARCHITECTURE handoff-diagram attributes scope/claims to "Operator" not architect + unused "SBAR/I-PASS" label (WF-3); VISION emphasis #1 "adoption pace tracked" has no instrument + stale `last_reviewed` (GO-1/GO-2). (Cross-repo sub-items SK-4/CM-2/HK-4 split to their owners — see Coordination.)
- **Why:** Cleanup/cosmetic; none blocks work.
- **Added:** 2026-05-29 by rob
- **Refs:** `docs/audits/2026-05-29-ecosystem-coherence-audit.md`

### [P3] Audit tool — folder-semantics validation check (ADR-60)
- **id:** 36
- **repo:** .dev-knowledge
- **status:** open
- **What:** Add a read-only `check_folder_semantics` asserting every `docs/` subfolder carries exactly one ADR-60 role (verified by README presence + a matchable convention). Surfaces drift when an ad-hoc folder is added without a declared role.
- **Why:** ADR-60 is enforced by review discipline only; bringing it under `audit.py health` makes drift visible.
- **Added:** 2026-05-27 by rob

### [P3] Sort-regression verification protocol — workspace settings
- **id:** 37
- **repo:** .dev-knowledge
- **status:** open
- **What:** Add a one-line PLAYBOOK/ESSENTIALS rule: any change to `.dev-knowledge.code-workspace` sort settings must be verified by (a) reading the linked PR/release (not just the issue page) AND (b) launching VS Code and visually checking dated-folder order before commit.
- **Why:** The ADR-59 sort-regression cost a full diagnostic+commit cycle because verification stopped at the issue page; a two-step rule catches it at write-time.
- **Added:** 2026-05-27 by rob

### [P3] Workspace scale-to-size ADR-59 refinement
- **id:** 38
- **repo:** .dev-knowledge
- **status:** open
- **What:** Codify the "scale-to-size" workspace decision: small repos get a minimal single-root workspace (+ 4 sort keys + repo Python/extensions); larger repos may keep richer multi-root configs. Small ADR-59 amendment or PLAYBOOK note.
- **Why:** Without codification, the next new-repo decision re-derives the threshold. Pairs with id 16.
- **Added:** 2026-05-27 by rob

### [P3] Entry-scripts → scripts/ convention codification
- **id:** 39
- **repo:** .dev-knowledge
- **status:** open
- **What:** Codify in PLAYBOOK (root hygiene) that run-entry scripts (`run.py`, `main.py`) live in `scripts/`, not repo root. Applied opportunistically in the 2026-05-27 retrofit but not codified.
- **Why:** Root cleanliness; ALL-CAPS canonical .md + dot-prefix configs cluster cleanly when entry scripts move out.
- **Added:** 2026-05-27 by rob

### [P3] requirements.txt ADR-59 exception note
- **id:** 40
- **repo:** .dev-knowledge
- **status:** open
- **What:** Make the `requirements*.txt` dot-prefix exception more prominent in ADR-59 (already listed) with a one-line pip/PEP rationale — or close as no-op if existing wording suffices.
- **Why:** Reduce future ambiguity for repos using `requirements.txt` instead of `pyproject.toml`.
- **Added:** 2026-05-27 by rob

### [P3] Consider PROCESS.md split for ARCHITECTURE.md
- **id:** 41
- **repo:** .dev-knowledge
- **status:** open
- **What:** If a future addition pushes `ARCHITECTURE.md` (405 lines, structural + 4 flow diagrams) past the operator's comfort threshold, split `## Processes` into `docs/PROCESS.md` (or `protocols/PROCESS.md`) and reference from ARCHITECTURE. Not blocking now.
- **Why:** ARCHITECTURE is read by every CLAUDE §3 pointer (ADR-51); keeping it scannable matters.
- **Added:** 2026-05-28 by rob

### [P3] Widen audit.py mermaid theme check scope (or accept current)
- **id:** 42
- **repo:** .dev-knowledge
- **status:** open
- **What:** Decide whether check #7 should expand beyond `ARCHITECTURE.md` + the template to other files carrying Mermaid (future `protocols/*.md`, docs/diagrams/) — (a) extend the path list (keep ADR-39 immutable exclusions) or (b) accept current scope.
- **Why:** Durability-audit J4 — the check is durable for ARCHITECTURE but not for future hand-authored Mermaid elsewhere; governance coverage is already in PLAYBOOK/ESSENTIALS.
- **Added:** 2026-05-28 by rob

### [P3] New-repo scaffolding template / starter pack
- **id:** 43
- **repo:** .dev-knowledge
- **status:** open
- **What:** Decide whether to author a canonical new-repo scaffold (one-step universalization baseline: dot-prefix configs, ALL-CAPS roots, dot-prefixed workspace + sort settings, `docs/{decisions,audits,archive}/README.md` seeds, BACKLOG/JOURNAL/LESSONS shells, instantiated templates). Layer-2 invariant — template snapshots, no orchestration script; operator runs the copy. Likely an ADR + `templates/new-repo-skeleton/`.
- **Why:** Durability-audit J6 — no canonical "what a new child repo looks like at t=0" reference; each new repo re-derives. Pairs with ids 16, 17.
- **Added:** 2026-05-28 by rob

### [P3] Child-repo audit reach — port audit.py checks or accept governance-only
- **id:** 44
- **repo:** .dev-knowledge
- **status:** open
- **What:** Decide how `audit.py` checks reach child repos: (a) per-repo port, (b) cross-repo runner (`audit ecosystem --all`, Layer-2 read-only), or (c) accept governance-only. Affects audit-tool architecture.
- **Why:** Durability-audit J5 — child repos run no analogous audit; conformance is verified only on a manual `.dev-knowledge` sweep. Overlaps id 29.
- **Added:** 2026-05-28 by rob

---

## Blocked

_(none)_

---

## Coordination

> Cross-repo items. **Governance pointers** stay in `.dev-knowledge`. **Pending-relocation** items are child-repo *execution* work awaiting their own sessions (ADR-41 — relocation is the Step-7 proposal `docs/audits/2026-06-01-child-repo-relocation-proposal.md`; the move happens in the target repo, then the pointer leaves here).
>
> ⚠ **Oversized vs the ≤10 target (currently 21).** This is the expected signal that the child-repo relocations are pending — it drains to ~3 governance pointers as those sessions execute. Per ADR-64 §"Open implementation questions" #1, the triage rule + coordination-pointer format are still to be pinned in the migration spec.

### Cross-repo governance pointers (stay in .dev-knowledge)

### [P2] Phase 2 universalization rollout
- **id:** 45
- **repo:** ecosystem
- **status:** open
- **What:** Apply ADR-33/34/35/37/38/39/41 to ai-council and corp-monorepo. ai-council substantially complete (hyphen compliance, ADR-38 gaps, VISION); corp-monorepo not yet started. Tracked here as the disseminator-function coordination point; per-repo execution lands in ids 51-65.
- **Why:** Validates the universalization pattern; unblocks trigger-based cohort migration.
- **Added:** 2026-04-30 by rob

### [P3] Apply scrum-master review pattern to other child repos
- **id:** 46
- **repo:** ecosystem
- **status:** open
- **What:** Extend the scrum-master review cycle (now unblocked — codified by ADR-63) to remaining repos: (1) corp-monorepo, (2) corp-knowledge-extractor / corp-by-os / corp-rfp-agent (verify existence first — id 47), (3) corp-ops + corp-sca (lighter). The review is triggered from `.dev-knowledge`; remediation executes in each child repo.
- **Why:** Phase 3 of ecosystem universalization; each review catches drift before it compounds.
- **Added:** 2026-05-12 by rob
- **Refs:** ADR-63

### [P3] Undiscovered repos confirmation
- **id:** 47
- **repo:** ecosystem
- **status:** open
- **What:** Confirm status of `corp-knowledge-extractor`, `corp-by-os`, `corp-rfp-agent` (not found under `Dev/` in the 2026-05-11 audit): renamed, archived, not-yet-cloned, or dropped.
- **Why:** Unknown repo status is a gap in audit coverage; blocks fully scoping the universalization rollout.
- **Added:** 2026-05-11 by rob

### Pending relocation to child repos (Step-7 proposal; await target-repo sessions)

### [P1] Apply tier-deprecation to corp-monorepo
- **id:** 48
- **repo:** corp-monorepo
- **status:** open
- **What:** Remove `tier:`/`scale:` from VISION.md (+ ARCHITECTURE.md) frontmatter; strike tier-conditional prose; add `status`/`last_reviewed` per the amended ADR-33 schema.
- **Why:** Ecosystem-wide tier deprecation; child frontmatter must conform to the amended universal schema.
- **Added:** 2026-05-23 by rob
- **Relocate:** → corp-monorepo (dedicated session)

### [P1] Apply tier-deprecation to ai-council
- **id:** 49
- **repo:** ai-council
- **status:** open
- **What:** Remove `tier:`/`scale:` from VISION.md (+ ARCHITECTURE.md); add the missing `status` key (vision_md WARN, 2026-05-23) and verify `last_reviewed`.
- **Why:** Same as id 48; the amended audit `vision_md` check flags ai-council WARN.
- **Added:** 2026-05-23 by rob
- **Relocate:** → ai-council (dedicated session)

### [P1] Execute the ai-council universalization execution plan
- **id:** 50
- **repo:** ai-council
- **status:** open
- **What:** A dedicated ai-council session executes `docs/audits/2026-05-25-ai-council-universalization-execution-plan.md` (Actions 1-8): README delete, tier-residue removal, `[L-opt]`→untagged, naming + ADR-08 rename, hand-authored Mermaid codemap, `.env.example` removal + workspace dot-prefix, BACKLOG header. Supersedes the loose scope of ids 49/61.
- **Why:** Closes the 14 findings in the 2026-05-25 audit refresh; ai-council is the universalization test case before corp-monorepo.
- **Added:** 2026-05-26 by rob
- **Relocate:** → ai-council (dedicated session)

### [P2] Handoff folder format adoption (corp-monorepo)
- **id:** 51
- **repo:** corp-monorepo
- **status:** open
- **What:** corp-monorepo still has flat `docs/HANDOFF.md` (pre-ADR-42). Convert to folder format at next handoff event, or explicitly deprecate. Tied to an A4 decision on whether the flat file is acceptable legacy. (ai-council resolved: absent at `1bcc6ab`.)
- **Why:** Flat files mislead future sessions about the active standard.
- **Added:** 2026-05-11 by rob
- **Relocate:** → corp-monorepo

### [P2] corp-monorepo P1-2 path-traversal branch unmerged
- **id:** 52
- **repo:** corp-monorepo
- **status:** open
- **What:** The P1-2 path-traversal extraction landed (`a1007b1`) but sits on unmerged branch `chore/extract-p1-2-to-backlog-2026-05-28`; corp-monorepo HEAD is not on main. Merge + resolve the pre-delete gate.
- **Why:** A security finding's tracking is stranded on a feature branch.
- **Added:** 2026-05-29 by rob
- **Relocate:** → corp-monorepo

### [P2] Root hygiene application — corp-monorepo
- **id:** 53
- **repo:** corp-monorepo
- **status:** open
- **What:** Consolidate standalone tool configs (`ruff.toml`/`pytest.ini`/`mypy.ini`) into `pyproject.toml` `[tool.*]`; dot-prefix `<repo>.code-workspace`; verify `tach.toml` movability. (corp-monorepo has pyproject.toml so consolidation applies.)
- **Why:** Root cleanliness; PLAYBOOK Root hygiene convention.
- **Added:** 2026-05-23 by rob
- **Relocate:** → corp-monorepo

### [P2] Root hygiene application — ai-council
- **id:** 54
- **repo:** ai-council
- **status:** open
- **What:** Consolidate tool configs into `pyproject.toml` where present; dot-prefix the `.code-workspace` file (verify ai-council has one); confirm root is clean.
- **Why:** Root cleanliness; PLAYBOOK Root hygiene convention.
- **Added:** 2026-05-23 by rob
- **Relocate:** → ai-council

### [P2] README disposition decision (corp-monorepo)
- **id:** 55
- **repo:** corp-monorepo
- **status:** open
- **What:** Decide keep-or-delete corp-monorepo's root README (does it have an external audience?). README is OPTIONAL universally since ADR-38 A5. (ai-council resolved 2026-05-26: DELETE.)
- **Why:** Child repos need an explicit keep/delete decision rather than silent drift.
- **Added:** 2026-05-23 by rob
- **Relocate:** → corp-monorepo

### [P2] corp-monorepo hyphen migration + ADR-38 compliance
- **id:** 56
- **repo:** corp-monorepo
- **status:** open
- **What:** (1) Hyphen filename migration for corp-monorepo ADR files; (3) `docs/archive/` content reclassification. (Subitem (2) ADR-38 Scale-L gaps closure CONFIRMED COMPLETE 2026-05-23.)
- **Why:** ADR-34 universal-mandate + ADR-38 root-placement amendments apply.
- **Added:** 2026-05-11 by rob
- **Relocate:** → corp-monorepo

### [P2] ai-council hyphen migration + ADR-38 compliance
- **id:** 57
- **repo:** ai-council
- **status:** open
- **What:** (1) Hyphen migration (likely low impact — verify first); (2) ADR-38 gaps: ARCHITECTURE.md to root, add LESSONS.md, BACKLOG.md. Largely subsumed by id 50.
- **Why:** Confirm compliance before claiming clean.
- **Added:** 2026-05-11 by rob
- **Relocate:** → ai-council

### [P2] Prevent auto-debate of stray Council-keyed files
- **id:** 58
- **repo:** ai-council
- **status:** open
- **What:** Prevent stray files carrying Council frontmatter keys in a watched location from being auto-picked-up and debated. Define a guard (allow-list, required marker, or inbox-only scoping).
- **Why:** An unintended auto-debate wastes ~$0.50/~5min and pollutes outputs.
- **Added:** 2026-05-26 by rob
- **Relocate:** → ai-council

### [P2] ADR-59 universal visual pattern — child-repo retrofits (4×)
- **id:** 59
- **repo:** ecosystem
- **status:** open
- **What:** Apply ADR-59 (dot-prefix discipline, canonical-.md visibility/clustering, workspace sort settings) to the four child repos. Plans authored 2026-05-27. Sub-items: ai-council (bundle with id 50); corp-ops (independent); corp-sca (independent); corp-monorepo (blocked on the corp-monorepo ruff-strictness decision).
- **Why:** ADR-59 self-applies only to `.dev-knowledge`; until child repos conform, audit checks FAIL on them and the "same visual layout everywhere" goal isn't delivered.
- **Added:** 2026-05-27 by rob
- **Relocate:** → each child repo (per-repo sessions)

### [P2] corp-sca-time-automation dev-tooling install + run.py → scripts/
- **id:** 60
- **repo:** corp-sca-time-automation
- **status:** open
- **What:** (1) Install pytest + ruff in the corp-sca venv (currently commented-out dev deps); (2) move `run.py` (root) → `scripts/run.py` and update its 6 references; verify with pytest. The move was deferred for lack of test tooling.
- **Why:** Completes the 2026-05-27 retrofit's per-repo conformance.
- **Added:** 2026-05-27 by rob
- **Relocate:** → corp-sca-time-automation

### [P3] ai-council LESSONS.md scope-tag backfill (ADR-46 advisory)
- **id:** 61
- **repo:** ai-council
- **status:** open
- **What:** ai-council LESSONS entries lack `[scope: X]` tags per the ADR-46 sniff test; add them to each entry's 6-field schema position.
- **Why:** Advisory WARN on `dated_entries_lessons`; methodology drift from the ADR-46 standard.
- **Added:** 2026-05-16 by rob
- **Relocate:** → ai-council

### [P3] UPPERCASE TYPE tag in legacy archive filenames (retire opportunistically)
- **id:** 62
- **repo:** corp-monorepo
- **status:** open
- **What:** corp-monorepo + corp-sca use `YYYY-MM-DD_TYPE_topic.md` in `docs/archive/` (pre-ADR-34). Rename to `YYYY-MM-DD-topic.md` opportunistically when touching those files; no dedicated prompt.
- **Why:** Pre-ADR-34 pattern creates ecosystem naming inconsistency.
- **Added:** 2026-05-11 by rob
- **Relocate:** → corp-monorepo, corp-sca-time-automation

### [P3] docs/HANDOFF.md flat-file deprecation (corp-monorepo, ai-council)
- **id:** 63
- **repo:** corp-monorepo
- **status:** open
- **What:** Both repos have flat `docs/HANDOFF.md` (pre-ADR-42). Retire at next handoff event or explicitly designate legacy. Tied to id 51's A4 decision.
- **Why:** Parallel patterns mislead future sessions about the active standard.
- **Added:** 2026-05-11 by rob
- **Relocate:** → corp-monorepo, ai-council

### [P3] Per-repo deeper cleanup follow-up (post-retrofit)
- **id:** 64
- **repo:** ecosystem
- **status:** open
- **What:** Decide per repo whether to address retrofit leftovers: ai-council 18 pre-existing ruff errors; corp-monorepo 89 (lenient select); corp-sca untracked `__pycache__/`; ai-council `.env` 100B (leave).
- **Why:** Scoped "report, don't delete" in the retrofit; worth a deliberate decision rather than indefinite drift.
- **Added:** 2026-05-27 by rob
- **Relocate:** → each child repo

### [P3] Cross-repo low-severity cleanups (child-repo-owned subset)
- **id:** 65
- **repo:** ecosystem
- **status:** open
- **What:** Child-repo-owned items from the 2026-05-29 coherence audit: `verify/cross-repo-boundaries.ps1` hard-codes a possibly-stale corp-monorepo layout (SK-4); corp-monorepo CLAUDE.md references flat `docs/handoffs/*.md` (CM-2); corp-ops/corp-sca have no pre-commit, ai-council only normalize-headers + hook-id naming drift (HK-4). (Self-owned subset is id 35.)
- **Why:** Cleanup/cosmetic; split per owner.
- **Added:** 2026-05-29 by rob
- **Relocate:** → respective child repos
