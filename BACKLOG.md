# .dev-knowledge BACKLOG

Open/in-progress `.dev-knowledge` work only. **Done items leave the file** (git history + the per-session JOURNAL entry are the record — ADR-65); no archive (CLAUDE.md §5). Terse 3-line entries — full `Why`/`Added`/history is in git. Schema: **PLAYBOOK §10 / ADR-64/65**; machine-checked by `scripts/validate_backlog.py`.

**Grooming log:** 2026-05-09 · 2026-05-23 · 2026-05-24 · 2026-05-31 (marathon-arc) · 2026-06-01 (ADR-64/65 migration). Next quarterly: 2026-07-01.

---

## Now

_(nothing in progress — see `## Open` → `### P1` for next actions)_

---

## Open

### P1

### [P1][L] Adversarial fresh-eyes pass in routine handoff generation
`id:1 · repo:.dev-knowledge · status:open`
Extend triangulation from the promotion gate to every routine handoff (sub-prompt / periodic audit / agent-framework). Council scope. (ref: AGENT_FRAMEWORK.md)

### [P1][L] Council decisions management consolidation
`id:2 · repo:.dev-knowledge · status:open`
Add contradiction-detection across decisions + an ownership model (amend vs new ADR vs clarification); the consolidated-index sub-item is done.

### [P1][M] Sacred-files maintenance enforcement
`id:3 · repo:.dev-knowledge · status:open`
Enforce canonical-file freshness (last_reviewed staleness hook / session-end checklist) so the 8 sacred files stop drifting.

### P2

### [P2][M] Lessons activation P1 implementation
`id:4 · repo:.dev-knowledge · status:open`
Build lessons-index.json + SessionStart retrieval + CLI query per ADR-35 (turn LESSONS into a live feedback loop).

### [P2][M] ESSENTIALS cheat-sheet additions for ADRs 35-63
`id:5 · repo:.dev-knowledge · status:open`
Add high-leverage ESSENTIALS cheats for ADRs 35-63 under the one-page constraint (judgment which warrant it).

### [P2][M] Handoff advisory framing leaks into receiver behavior
`id:6 · repo:.dev-knowledge · status:open`
Classify root cause of advisory framing becoming receiver behavioral pressure; propose mitigation.

### [P2][M] Extend audit-check enforcement to other governance artifacts
`id:7 · repo:.dev-knowledge · status:open`
Apply the audit.py #8 structural-validator pattern to Council transcripts + ADRs (frontmatter/supersession/template).

### [P2][M] Hooks implementation (additions + consolidation + automation)
`id:8 · repo:.dev-knowledge · status:open`
Implement the analysed hooks: session-end clean-tree/staleness + SessionStart lessons-retrieval; resolve the review-hook overlap.

### [P2][M] Skills universalization across repos
`id:9 · repo:.dev-knowledge · status:open`
Inventory skills across repos, classify repo-specific vs universal, propose a canonical home in `.dev-knowledge`.

### [P2][M] Ecosystem doc-truth sweep (CLAUDE + ARCHITECTURE)
`id:10 · repo:.dev-knowledge · status:open`
Fix 8 self-description drifts (CLAUDE §7/§8; ARCHITECTURE validators + governing-ADRs; LESSONS descriptor; ruff claim; TOKEN-LOG path). (ref: 2026-05-29 coherence audit)

### [P2][M] Ecosystem feedback-loop enforcement (un-enforced guards → gate)
`id:11 · repo:.dev-knowledge · status:open`
Convert LESSON-#9's advisory cross-case guard into an amendment checklist/gate (Layer-2 checklist, not orchestration).

### [P2][M] Evolution memory logs missing + no session-close automation
`id:12 · repo:.dev-knowledge · status:open`
Create the .jsonl logs OR repoint hooks/protocol to evolution-log.md; add one read-only session-close automation.

### [P2][S] Ruff lint enforcement for .dev-knowledge
`id:13 · repo:.dev-knowledge · status:open`
Add the ruff pre-commit hook OR correct the docs that claim it (currently documented-not-enforced).

### [P2][L] Ecosystem-folder operating-model design
`id:14 · repo:.dev-knowledge · status:open`
Decide the `ecosystem/` folder model (regenerated snapshot / continuous-audit substrate / retire). Council-scope.

### [P2][M] CI enforcement of hyphen-only separator rule
`id:15 · repo:.dev-knowledge · status:open`
Pre-commit + Action enforcing hyphen-only file/folder names; decide which paths + exceptions.

### [P2][M] Remove tier-residue from workspace templates
`id:16 · repo:.dev-knowledge · status:open`
Collapse `workspace-{S,M,L}.code-workspace` into one maximal scale-adaptive template (operator Q5).

### [P2][M] templates/CLAUDE-md-template.md refresh (ADRs 54-63)
`id:17 · repo:.dev-knowledge · status:open`
Refresh the new-repo CLAUDE template to encode ADRs 54-63 (mermaid theme, visual pattern, taxonomy, worktree); §11 last-5 = 61-65. (ref: durability audit J1)

### [P2][M] AI Council convene-vs-Path-A decision criterion
`id:18 · repo:.dev-knowledge · status:open`
Codify when an architecture decision convenes Council vs a Path-A direct ADR (ADR-62/63/65 were Path-A).

### P3

### [P3][S] ADR-39 amendment — add BACKLOG.md lifecycle entry
`id:19 · repo:.dev-knowledge · status:open`
Add a BACKLOG.md registry entry to ADR-39 (bundle with #20).

### [P3][S] ADR-41 amendment — cross-reference ADR-47/64/65
`id:20 · repo:.dev-knowledge · status:open`
Dated amendment to immutable ADR-41 cross-referencing the schema/architecture/disposition ADRs.

### [P3][M] ADR-39 registry decision — unregistered template files
`id:21 · repo:.dev-knowledge · status:open`
Decide register / exempt / hybrid for the non-handoff `templates/` class.

### [P3][S] LESSONS parenthetical-qualifier entries escape the audit regex
`id:22 · repo:.dev-knowledge · status:open`
Broaden `_LESSONS_H3_RE` for an optional parenthetical, or reformat the 8 entries (ADR-29 sign-off).

### [P3][M] ADR relationship index / supersession graph
`id:23 · repo:.dev-knowledge · status:open`
Build a navigable supersedes/related/amends graph from ADR frontmatter (or an index doc).

### [P3][S] CLAUDE.md §4 cites a stale known-failing test
`id:24 · repo:.dev-knowledge · status:open`
Remove the stale known-failure clause (the test passes); fold into the doc-truth sweep (#10).

### [P3][M] Process refinements deferred from the v4.3.1 caveat patch
`id:25 · repo:.dev-knowledge · status:open`
Seven .tmpl/spec refinements (tag-lint #10, fresh-eyes cadence, CLI example, ML namespace, wording, auto-routing, passive-storage).

### [P3][S] Phase-1 handoff operator-invariants section
`id:26 · repo:.dev-knowledge · status:open`
Add an operator-invariants section so an inheritor assumes defaults (clean-tree, immediate-merge, three-domain) instead of over-asking.

### [P3][M] Relax-vs-gate principle for drifted guards
`id:27 · repo:.dev-knowledge · status:open`
Codify the cost/value-asymmetric relax-vs-gate criterion (ADR-62 relaxed, ADR-63 gated the same disease).

### [P3][S] Incorporate metaphor-based communication into PLAYBOOK + ESSENTIALS
`id:28 · repo:.dev-knowledge · status:open`
Codify the sage→apprentice-style metaphor pattern for teaching design intent.

### [P3][M] Cross-repo audit (Phase 3) — tool-driven compliance run
`id:29 · repo:.dev-knowledge · status:open`
`audit ecosystem --all` generating an adoption/compliance report (Layer-2 read-only); overlaps #44.

### [P3][M] Kimi K2 model integration evaluation
`id:30 · repo:.dev-knowledge · status:open`
Evaluate Kimi K2 (capability / cost / integration); Council decision on adoption level.

### [P3][L] Large repo migration preparation
`id:31 · repo:.dev-knowledge · status:open`
Council-level plan for migrating one significant repo (structure/naming/sacred-files/ADRs); repo unnamed until scoped.

### [P3][M] VS Code productivity maximization
`id:32 · repo:.dev-knowledge · status:open`
Extensions audit + workflow templates + tooling integration; produce a recommendation.

### [P3][M] Custom 'Pinned Files' VS Code extension
`id:33 · repo:.dev-knowledge · status:open`
TreeView of pinned canonical files (~100-150 LOC TS, local); trigger = keybindings-friction or operator-proactive.

### [P3][S] PLAYBOOK codifications from the 2026-05-19 posture audit
`id:34 · repo:.dev-knowledge · status:open`
Add 4 codifications (stable-end-state phrasing, verify-destination, no-delete-canonical-dup exception, ADR-with-N=1).

### [P3][S] Ecosystem low-severity cleanups (self-owned subset)
`id:35 · repo:.dev-knowledge · status:open`
ARCHITECTURE handoff-diagram attribution + SBAR label (WF-3); VISION adoption-signal + stale last_reviewed (GO-1/2).

### [P3][M] Audit tool — folder-semantics validation check (ADR-60)
`id:36 · repo:.dev-knowledge · status:open`
Read-only `check_folder_semantics` asserting each `docs/` subfolder carries exactly one ADR-60 role.

### [P3][S] Sort-regression verification protocol — workspace settings
`id:37 · repo:.dev-knowledge · status:open`
PLAYBOOK/ESSENTIALS rule: verify workspace sort changes via the merged PR + a visual editor check.

### [P3][S] Workspace scale-to-size ADR-59 refinement
`id:38 · repo:.dev-knowledge · status:open`
Codify small=single-root / large=multi-root workspace decision (ADR-59 amendment or PLAYBOOK note).

### [P3][S] Entry-scripts → scripts/ convention codification
`id:39 · repo:.dev-knowledge · status:open`
Codify in PLAYBOOK root-hygiene that run-entry scripts live in `scripts/`, not the repo root.

### [P3][S] requirements.txt ADR-59 exception note
`id:40 · repo:.dev-knowledge · status:open`
Make the `requirements*.txt` dot-prefix exception prominent in ADR-59 with a pip/PEP rationale, or close no-op.

### [P3][S] Consider PROCESS.md split for ARCHITECTURE.md
`id:41 · repo:.dev-knowledge · status:open`
Split `## Processes` into PROCESS.md if ARCHITECTURE (405 lines) grows past the comfort threshold; not blocking now.

### [P3][S] Widen audit.py mermaid theme check scope (or accept)
`id:42 · repo:.dev-knowledge · status:open`
Decide whether check #7 expands beyond ARCHITECTURE.md to other mermaid-bearing files (J4).

### [P3][L] New-repo scaffolding template / starter pack
`id:43 · repo:.dev-knowledge · status:open`
Decide whether to author a one-step new-repo baseline scaffold (ADR + `templates/new-repo-skeleton/`, no scripts); J6. Pairs with #16/#17.

### [P3][M] Child-repo audit reach — port audit.py or accept governance-only
`id:44 · repo:.dev-knowledge · status:open`
Decide per-repo port / cross-repo runner / governance-only for reaching child repos (J5); overlaps #29.

---

## Blocked

_(none)_

---

## Coordination

> Cross-repo items. **Governance pointers** stay here. **Pending-relocation** items are child-repo execution work awaiting their own sessions (ADR-41); they move to the relocation queue in `docs/audits/2026-06-01-child-repo-relocation-proposal.md`.

### Governance pointers (stay in .dev-knowledge)

### [P2][M] Phase 2 universalization rollout
`id:45 · repo:ecosystem · status:open`
Apply ADR-33/34/35/37/38/39/41 to ai-council + corp-monorepo; ai-council substantially done, corp-monorepo not started.

### [P3][M] Apply scrum-master review pattern to other child repos
`id:46 · repo:ecosystem · status:open`
Extend the ADR-63 review cycle to remaining repos (corp-monorepo → verify undiscovered → corp-ops/sca).

### [P3][S] Undiscovered repos confirmation
`id:47 · repo:ecosystem · status:open`
Confirm status of corp-knowledge-extractor / corp-by-os / corp-rfp-agent (renamed / archived / uncloned / dropped).

_18 child-repo execution items were moved to the relocation queue → `docs/audits/2026-06-01-child-repo-relocation-proposal.md` (they leave that queue as their target-repo sessions run)._
