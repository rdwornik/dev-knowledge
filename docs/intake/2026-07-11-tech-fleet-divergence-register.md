---
intake-id: 11
status: SUPERSEDED
origin: architect-compiled from this session's witnessed reports + the operator's standing list, 2026-07-11 — snapshot pending verification by the fleet-parity sweep
superseded-by: "the fleet-parity sweep register (ecosystem/parity-surfaces.yaml) — named the verified successor in the intake note below"
---

> **Intake note:** Architect-compiled master register of operator-raised divergences (23 items); snapshot — the fleet-parity sweep register is the verified successor; keep for provenance of the operator's standing list.

# Fleet Divergence Register — Master List (operator-raised items)

> Compiled 2026-07-11 by the architect from: this session's witnessed reports (corp rollout, ai-council rollout, census/boundary-matrix references) + the operator's repeated statements. Column "Verified?" is honest: WITNESSED = confirmed in a CC report this session; OPERATOR = you observed it, not yet machine-verified; UNKNOWN = nobody has checked. The running fleet-parity sweep verifies every OPERATOR/UNKNOWN row against live state.
> Column "In audits?" answers your question "czy to w ogóle wyszło w audycie" — honestly.

## A. Root dot-folders / caches / env

| # | Item | State per repo | Should it differ? | Verified? | In audits? |
|---|---|---|---|---|---|
| 1 | .mypy_cache | ai-council: present; hub: absent (hub doesn't run mypy); corp: ? | Tool cache — NEVER tracked; presence on disk is fine IF gitignored. Parity = gitignore parity, not folder parity | OPERATOR | Partially — corp rollout verified corp caches gitignored; no fleet-wide pass |
| 2 | .pytest_cache | hub + ai-council: present; corp: present | Same class as #1 — IGNORE, gitignore parity | WITNESSED (corp) / OPERATOR (rest) | Same as #1 |
| 3 | .ruff_cache | varies | Same class — IGNORE | WITNESSED (corp only) | Same as #1 |
| 4 | .hypothesis | corp only (uses hypothesis testing lib) | LEGITIMATE LOCAL (tool corp uses) — but must be gitignored | WITNESSED (corp: gitignored) | corp rollout row 7 only |
| 5 | .venv | all repos | IGNORE class — gitignored everywhere | OPERATOR | No fleet check |
| 6 | .env (ai-council) | ai-council: present; others: ? | OPEN QUESTION you asked: why is it there, is it needed, is it gitignored (secrets risk). Nobody has answered | UNKNOWN | **NO — never caught** |
| 7 | .vscode / settings | hub: present; ai-council: absent (?); corp: ? | OPEN RULING: are workspace settings methodology-carried (template) or local? No decision exists | OPERATOR | **NO** |
| 8 | .github | hub: present; consumers: ? | Probably per-repo CI = LOCAL; needs a declared verdict | OPERATOR | **NO** |
| 9 | assets/ (ai-council only) | Holds ruff-pre-commit.yaml, referenced by hub-canonical INSTALL.md §2 | Half-explained: corp ruled LOCAL-not-carried this session. UNRESOLVED: if only ai-council has it and INSTALL.md references it, either hub should carry it or the INSTALL reference is misleading | WITNESSED (corp fork-3) | Partially — surfaced only as the corp fork, not as a fleet question |

## B. Documents / content conventions

| # | Item | State | Should it differ? | Verified? | In audits? |
|---|---|---|---|---|---|
| 10 | ARCHITECTURE.md: ToC + Mermaid | corp: BOTH still present; hub: has ToC-bound gates; ai-council: ? | NO — your ruling (2026-07-11): ARCHITECTURE is CC-facing, strip ToC+Mermaid fleet-wide; ToC lives ONLY in PLAYBOOK. Filed as #326 (hub first), execution = next step, WITH the gate re-point (toc hooks are keyed on ARCHITECTURE) | WITNESSED | Mermaid inventory (12) caught by the C4 night pack as INVENTORY, not as violation — the rule is yours, from today. ToC-in-ARCHITECTURE as a violation: **NO** |
| 11 | INSTALL.md | **YES — it IS methodology** (your direct question). Hub canonical: plugins/tier1-lifecycle/INSTALL.md; ai-council + corp: interim byte-copies (this session) | Should NOT differ; durable carrier = hub #315 (manifest-carried). Until #315 lands, the copies WILL drift — recorded honestly in the corp parity table | WITNESSED | YES — #315 existed; the rollout drafts however OMITTED it (corp CC flagged the draft gap) |
| 12 | protocols/ | hub: yes; ai-council: yes (marked local, #314); corp: ABSENT (deferred #314) | Temporary difference, ticketed (#314) — legitimate until delivered | WITNESSED | YES (#314) |
| 13 | Audit filename convention | corp: `_AUDIT_` UPPERCASE (corp ADR-14); hub: lowercase class-token (ADR-101) | NO — one fleet convention must win. Clash created TODAY by the corp rollout artifact itself | WITNESSED | **NO — no audit flagged it; I (architect) missed it in plan review too** |
| 14 | BACKLOG schema (E-prefix / S-n story-map) | hub: E1–E7 + S-n + [#id] (today); consumers: NOT migrated | OPEN RULING: do consumer backlogs adopt the hub story-map schema? No decision, no ticket until today's sweep | WITNESSED (hub) / OPERATOR (consumers) | **NO** |
| 15 | CLAUDE.md stale/archived references | hub session-start-protocol references archived `boot`; possibly more, all repos | NO — your NEW RULE (codify): nothing archived may be referenced from root/CLAUDE.md; archived content moves to templates/archive (exists in hub) or LESSONS/docs. Root = only current | OPERATOR | **NO — boundary matrix compared divergence BETWEEN repos, not reference-validity WITHIN a file** |

## C. Commands roster

| # | Item | State | Should it differ? | Verified? | In audits? |
|---|---|---|---|---|---|
| 16 | code-review vs codex-review | Both exist (rename to codex-review happened 2026-05-12; a code-review surface still present) — duplication/confusion | NO — one command, one name; the leftover goes to archive | OPERATOR | Partially — the 2026-05-12 hooks-discovery caught the ORIGINAL clash; the leftover after rename: **NO** |
| 17 | evolve | Missing (consumers? entirely?) | UNKNOWN whether it should exist per-repo — needs the roster diff | OPERATOR | **NO** |
| 18 | /save | Missing in consumers | NO — genuine gap, ticketed #325 (manifest command-carrier) | WITNESSED | YES (rollout report-back) |
| 19 | /handoff | Absent in consumers | YES — INTENTIONAL (ADR-42/36 centralize handoffs). This is what a SANCTIONED divergence looks like: ruled, recorded, machine-checkable | WITNESSED | YES |

## D. Unexplained hub root entries

| # | Item | State | Should it exist? | Verified? | In audits? |
|---|---|---|---|---|---|
| 20 | runbox/ (hub) | One file; purpose never explained to you despite asking repeatedly | UNKNOWN — sweep must answer from git log: origin, purpose → keep-with-README or delete-candidate (you rule) | UNKNOWN | **NO** |
| 21 | temp/ (hub) | Empty; created by CC at some point | Almost certainly junk — root rule violation. Delete-candidate (you rule; never deleted without your word) | UNKNOWN | **NO** |

## E. The missing mechanism (root cause of the 20-session loop)

| # | Item | State | Verdict |
|---|---|---|---|
| 22 | Machine-readable methodology-vs-local manifest per repo | DOES NOT EXIST as one surface. Pieces scattered: manifest-v1.3.1.yaml (carried artifacts), .methodology.yaml (waivers only), CLAUDE.md markers (doc sections only). NOTHING covers root folders/files ownership | BUILD IT — your core demand: entering any fleet repo, the ecosystem declares which root entries are methodology (template/family) vs repo-local vs ignored. This is the fleet-parity check designed in the running sweep |
| 23 | Root-archive prohibition rule | Not codified anywhere | CODIFY: root and CLAUDE.md contain only current content; archived → templates/archive (hub has the folder), LESSONS, or docs |

## Honest answer: why the night audits didn't show this

The census (07-08) and boundary matrix (07-11) compared the CONTENT of governed surfaces (CLAUDE.md sections, gates, versions). **Nobody ever wrote the trivial check you named: the root-entry set-diff across the three repos.** The rollout staged drafts omitted root-surface entirely (the corp session itself reported this as a draft gap). Items 6, 7, 8, 13, 14, 15(partially), 16(leftover), 17, 20, 21 were caught by NO audit — only by you, repeatedly. That is the failure: the audits audited what they were told to audit, and the root surface was never in scope. The fix is item 22 — after which this register regenerates mechanically and anything undeclared is a WARN nobody can ignore.

## What happens next (already in motion)
1. Fleet-parity sweep (running in hub) verifies every OPERATOR/UNKNOWN row live and proposes verdicts — including runbox, temp, .env, the naming clash, the command diff.
2. You rule the verdicts in one pass (like the audit-corpus verb list).
3. Execution per repo (hub first per #326), each divergence → parity, .methodology.yaml declaration, or archive.
4. The fleet-parity audit CHECK ships — the mechanism that makes silent regression impossible.
