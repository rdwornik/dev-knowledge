<!-- scope: meta -->

# Methodology + Canonical-Files Audit vs `copilot-collections`

> **DRAFT analysis artifact — not implementation.** Produced on branch
> `docs/methodology-canonical-audit-2026-05-31` (off `main` @ `22cf2de`).
> Audits the full `.dev-knowledge` methodology surface (artifacts + canonical
> living-files) against the `copilot-collections` reference, maps transferable
> patterns onto **our Claude Code toolchain**, and produces a prioritized,
> toolchain-mapped action plan. The focused **BACKLOG architecture diagnosis**
> (operator priority-one) is a companion doc:
> `2026-05-31-backlog-architecture-diagnosis.md`.
>
> Nothing here is restructured, migrated, deleted, or merged. All findings are
> for operator + Council review.

**Reference:** TheSoftwareHouse/`copilot-collections` (Copilot Customization track only).
**Tracks:** (1) artifact methodology — skills/commands/hooks/instructions; (2) canonical living-files methodology; (3) BACKLOG architecture (companion doc).
**Date:** 2026-05-31 · **Author:** Claude Code (Opus) · **Status:** draft, awaiting operator + fresh-eyes review.

---

## UNDERSTAND (restatement)

- **Problem.** Our methodology grew organically and is under-consolidated at both the artifact level (skills/commands/hooks/instructions) and the canonical-file level (VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING/LESSONS/JOURNAL/BACKLOG). The operator (ADHD/autism; needs low-friction, deterministic, scannable systems) cannot see "what exists / how to author it / what to do next" at a glance.
- **Scope.** `.dev-knowledge` only. Audit + diagnosis + plan. **Not** implementation.
- **Risks designed against.** (1) Porting VS Code/Copilot artifacts (wrong toolchain). (2) Inventing folders/conventions (W6). (3) Surface "copy their layout" audit. (4) Auto-restructuring BACKLOG (forbidden — Council scope). (5) Reviving a deleted file without flagging that it amends a prior decision.
- **Failure mode to avoid.** A generic "adopt their layout" plan, or a backlog "fix" applied instead of a Council-ready options analysis.

---

## §0 — Current-state inventory (all three tracks)

### Track 1 — Artifact methodology (verified live, not from docs)

| Surface | Actual state @ `22cf2de` | Note |
|---|---|---|
| **Repo-level skills** (`.claude/skills/`) | **None — directory absent** | Confirms CLAUDE.md §8. All active skills are user-level. |
| **Repo-level commands** (`.claude/commands/`) | `save.md`, `handoff.md` | `handoff.md` carries the 5-case decision matrix (recent). |
| **Repo-level subagents** (`.claude/agents/`) | **None** | User-level subagents only (below). |
| **Repo-level rules** (`.claude/rules/`) | `git-discipline.md` | Commit-after-every-edit + clean-tree-at-end. |
| **Pre-commit hooks** (`.pre-commit-config.yaml`) | `normalize-dated-headers` + `codemap-freshness` **only** | **ruff is NOT present** despite CLAUDE.md §9/§4 + ARCHITECTURE claiming it (live confirmation of ecosystem-audit HK-1). |
| **Claude Code hooks** | SessionStart EVOLUTION sweep (user-level `~/.claude`); **no functional SessionStop automation** | Reads `sessions/violations/corrections/observations.jsonl` — none exist (ecosystem-audit SK-3/HK-2/HK-3). Machinery wired, vacuous. |
| **Validators** (`scripts/`) | `audit.py` (9 checks), `normalize_headers.py`, `migrate_links.py`, `codemap/` package | `backlog_extract.py` **retired/absent** — but ARCHITECTURE.md §Validators still lists it (stale, WF-2). |
| **User-level skills** (govern this repo) | `gotchas`, `verify`, `boot`, `session-summary`, `handoff`, `save`, `codex-review`, `evolve` | Per CLAUDE.md §8 + `/boot` load. |
| **User-level subagents** (`~/.claude/agents/`) | `ecosystem-snapshot`, `report-generator` (Haiku, read-only) | Per PLAYBOOK §7d. |

**Authoring methodology that governs these:** PLAYBOOK §"Claude Code internals" (7a–7d disambiguation table + per-mechanism when/when-not + anti-patterns) and §"Adoption protocol" (5-stage: Triage → Decision → Validation → Install → Document). This is **strong and already in place** — a key finding is that the reference's separation-of-concerns is *largely already covered* by PLAYBOOK §7.

### Track 2 — Canonical living-files methodology

| File | Present | Lifecycle (ADR-39) | Scannability / determinism notes |
|---|---|---|---|
| `VISION.md` | ✅ (v1.0, `last_reviewed: 2026-05-24`) | Mutable, quarterly, canonical | `last_reviewed` predates ADRs 59–63 (GO-2). |
| `ARCHITECTURE.md` | ✅ (405 lines, 4 Mermaid diagrams) | Mutable, event-triggered | §Validators lists retired `backlog_extract.py`; governing-ADRs omit 59/61 (WF-1/WF-2). Split candidate (BACKLOG line 801). |
| `CLAUDE.md` | ✅ (v2.3, ≤200-line target) | Mutable, quarterly | §7 omits `/codex-review`+`/evolve`; §8 calls commands "skills"; §4 cites a stale known-failing test; footer date vs §12 mismatch (SK-1/SK-2/CD-1/CD-2). |
| `CONTRIBUTING.md` | ✅ | Mutable, quarterly | Present (prompt asked to verify). Not yet audited for ADR-59/60/61 currency. |
| `LESSONS.md` | ✅ (root, append-only, newest-top) | Append-only, never groomed | ARCHITECTURE calls it "oldest-top per ADR-29" — file is newest-top (ML-1, descriptor drift). |
| `JOURNAL.md` | ✅ (append-only, newest-first) | Append-only, per-session | Healthy; current to 2026-05-31. |
| `BACKLOG.md` | ✅ (**871 lines**) | Mutable, per-handoff + quarterly | **Diagnosis subject — companion doc.** |
| `TOKEN-LOG.md` | ✅ at **`logs/TOKEN-LOG.md`** | Append-only | CLAUDE.md §4/§5 imply root location (minor path drift, ML-4 nuance). |

**Cross-cutting Track-2 observation:** the canonical set is *complete and lifecycle-governed* (ADR-39 registry), but suffers **documented-vs-actual drift** — the repo whose VISION is "drift detected proactively" is itself the locus of ~12 doc-truth drifts (ecosystem-audit 2026-05-29). The maintenance *cadence* is the gap, not the file set.

### Track 3 — BACKLOG metrics (verified live; full diagnosis in companion doc)

| Metric | Live value @ `22cf2de` | Problem-doc claim | Verdict |
|---|---|---|---|
| Total entries | **107** | "~76" | Problem doc **undercounted** (stale; pre-arc). Worse than stated. |
| Open entries | **66** | — | 62% of entries. |
| Closed/superseded/resolved retained **in-place** | **41** (38%) | — | Direct contradiction of retained ADR-47 ("done items leave; git history is the record"). |
| Lines | **871** | "~840" | Confirmed. |
| H2 sections | **9** | — | Streams A–D + Cross-stream + **4 session-arc-named sections** (hybrid taxonomy). |
| Status vocabulary | `open/closed/superseded/resolved` | — | **Schema drift:** ADR-41 + ADR-47 + PLAYBOOK §10 all specify `open/in-progress/blocked/done`. |

---

## §1 — Reference pattern catalog (`copilot-collections`, Customization track)

Extracted by a bounded sub-agent reading only the Customization track (agents `tsh-copilot-{engineer,orchestrator,artifact-creator}`; skills `tsh-creating-{skills,agents,prompts,instructions}`; naming-conventions instructions). Lifecycle implementation skills (backend/frontend/SQL/E2E/UI) noted-not-read per cost rule.

| Pattern | What it is | Why it works | Token/cost angle | Track |
|---|---|---|---|---|
| **WHO/HOW/WHAT/RULES separation** | agent=WHO, skill=HOW, prompt=WHAT, instructions=RULES — strict responsibility boundaries | Prevents duplication; one skill reused across agents/prompts without copy-paste | Consolidation at merge time; agents share skills | Artifact |
| **Gerund naming** (`creating-skills`) | verb-ing-object names for skills/prompts | Mirrors intent; memorable; avoids collision with agent role-nouns | Negligible; saves search overhead | Artifact |
| **Namespace prefix** (`tsh-`) | all customization artifacts share a prefix | Filterable, collision-proof, scales to shared libraries | Negligible | Artifact |
| **Frontmatter for progressive load** | YAML (name/description/applyTo) at artifact head | Metadata loads first for discovery; body loads on-demand | Skips body load for non-triggering artifacts | Artifact / Canonical |
| **Progressive disclosure + body size cap** | skill body ≤500 lines; detail → `references/` | Bounded cognitive load; lazy-load refs | Saves ~100–200 tok vs monolithic | Artifact |
| **Skill template + examples folder** | `SKILL.md` + `skill.template.md` + `examples/` + `references/` | Kills blank-page friction; copy-and-fill onboarding | ~20 tok saved per new skill | Artifact |
| **Orchestrator → isolated workers** | decompose research→synthesis→create→review; each worker gets goal+spec+refs only, no history | No context bleed; fresh worker context; orchestrator keeps design authority | 3–5 focused prompts ≪ 1 monolith | Artifact |
| **Specification-driven creation** | creator agent gets a full spec, does no research | Clean design≠creation handoff; validate output against spec | Eliminates research→create round-trips | Artifact |
| **Gate-based review before promotion** | mandatory review gate (max 2–3 fix cycles) before an artifact is "done" | Catches design mismatch early | 1 gate ≪ rework cost | Artifact / Canonical |
| **Severity-tiered reporting** | 🔴 Critical / 🟡 Important / 🟢 Nice-to-have | Scannable, prioritized, survives review | ~2 tok/item | Canonical / Backlog-org |
| **Repository-level constitution** | one `copilot-instructions.md` = project law, auto-loaded | Single source of truth, consistent across interactions | One load/session, unlimited reuse | Canonical |
| **Granular `applyTo` instructions** | scoped rule files targeting globs (`src/**/*.tsx`) | Contextual rules without bloat | Routes rules; saves irrelevant loads | Canonical (concept only) |
| **XML structure tags** | `<principles>`/`<rules>`/`<specifications>` blocks | Reliable parsing across model tiers | ~3–5 tok/tag, paid back by parse reliability | Artifact |

### Non-transferable (VS Code / Copilot-specific — do NOT port)

- **`.agent.md` / `.prompt.md` / `.instructions.md` / `SKILL.md` file formats** — native Copilot artifact syntax; Claude Code uses `.claude/skills/<name>/SKILL.md` + `.claude/commands/*.md`. *Principles* transfer, syntax does not.
- **Frontmatter `model:` per-artifact routing** — Copilot routes per-prompt; Claude Code selects model at session level.
- **MCP in `.vscode/settings.json`** (Atlassian/Figma/Playwright) — VS Code extension-host mechanism.
- **`applyTo:` glob scoping** — VS Code file-routing; Claude Code loads globally or on explicit trigger. (The *concept* — scoped instructions — is interesting but has no native Claude Code analog.)
- **Playwright UI-verification loops; Jira `/tsh-implement` sync** — external-tool integrations with no Claude Code equivalent.

### Reference has NO backlog methodology — confirmed

`copilot-collections` is a template/toolchain library; task-tracking lives in **Jira (external)**. For Track 3, **only its organizational principles transfer** — severity tiers, separation-of-concerns, progressive disclosure, prioritized-action-plan format. There is **no backlog structure to copy**.

---

## §2 — Mapping matrix (reference pattern → Claude Code analog)

Full set enumerated before assessment (no one-at-a-time reactive judgments). **P/Partial/A** = Present / Partial / Absent in `.dev-knowledge` today.

| Reference pattern | Claude Code analog (ours) | P/Partial/A | Value if adopted | Cost | ADR-level? | Track |
|---|---|---|---|---|---|---|
| WHO/HOW/WHAT/RULES separation | PLAYBOOK §7 disambiguation: Skill=HOW · Command=invoke-WHAT · Hook=enforce-RULES · Subagent=WHO-delegate | **P** | — (already covered) | — | No | 1 |
| Spec-driven creation | Formal CC prompt (Model/Mode/Effort + UNDERSTAND + Steps + COMMIT); ADR-56 Prompt Generation Card | **P** | — (strong) | — | No | 1 |
| Progressive disclosure + body cap | PLAYBOOK §7a (skill ≤500 lines → `references/`); CLAUDE.md ≤200 lines | **P** | — | — | No | 1 |
| Gate-based review before promotion | Codex review (≥3 files); fresh-eyes beta→stable (ESSENTIALS); scrum-master review (ADR-63) | **P** (richer than ref) | — | — | No | 1,2 |
| Repository-level constitution | `CLAUDE.md` single canonical instruction file (ADR-53), auto-loaded | **P** (strong) | — | — | No | 2 |
| Orchestrator → isolated workers | Subagents (PLAYBOOK §7d; Cognition read-heavy/write-light); used live in this audit | **Partial** | Med — a worked "orchestrator/worker" pattern note would make delegation repeatable | Low | No (PLAYBOOK note) | 1 |
| Frontmatter for progressive load | SKILL.md `name`/`trigger`; VISION/ARCHITECTURE frontmatter | **Partial** | Low-Med — canonical-file frontmatter is inconsistent (CLAUDE/LESSONS/JOURNAL/BACKLOG have none) | Low | No | 1,2 |
| **Severity-tiered + scannable reporting** | PLAYBOOK §17 + audit docs use 🔴🟡🟢; **BACKLOG uses P1/P2/P3 with no actionability surface** | **Partial** | **HIGH** — the one principle with real leverage; feeds Track 3 | Low-Med | Maybe (BACKLOG = Council) | 2,3 |
| Gerund naming convention | Skills mix verbs (`save`,`boot`,`evolve`) + nouns (`gotchas`); no codified rule | **A** | Med — naming consistency aids recall | Low | No (PLAYBOOK note) | 1 |
| Skill template + examples folder | No `SKILL.md` template / skill scaffold in `templates/` | **A** | Med (but ~0 repo-level skills today → low near-term) | Low | No | 1 |
| Namespace prefix (`tsh-`) | None | **A** | **Low** — solves multi-team library collision we don't have (solo, single-tool) | — | No | 1 |
| Granular `applyTo` instructions | None (CLAUDE.md is whole-repo) | **A** | Low — no Claude Code file-scoping mechanism; concept only | — | No | 2 |
| XML structure tags | Markdown headers throughout | **A** | Low — markdown headers suffice at our scale; XML helps parse-reliability we don't need | — | No | 1 |

**Honest conclusion (avoids the "copy their layout" failure mode):** the reference largely **validates what we already do** — separation-of-concerns, spec-driven creation, progressive disclosure, gate review, and the single-constitution file are all Present, several richer than the reference. Of the genuine gaps, only **severity-tiered + progressive-disclosure organization applied to the BACKLOG actionability surface** carries high leverage. The rest (naming convention, skill template, orchestrator note, frontmatter consistency) are low-cost polish that should ride existing PLAYBOOK update items, **not** drive new structure. Three reference patterns are explicitly **low-value for our context** (namespace prefix, applyTo, XML tags) and are recommended *against* adoption.

---

## Files actually read (cost ledger)

Phase 0 (own state): `CLAUDE.md`, `VISION.md`, `ARCHITECTURE.md`, `BACKLOG.md` (full), `protocols/ESSENTIALS.md`, `protocols/AI_COUNCIL_PROCESS.md`, `protocols/PLAYBOOK.md` (TOC + §7 internals + §10 backlog grooming), `docs/audits/2026-05-31-backlog-reconciliation-classification.md`, ADR-39/41/47/48, `.pre-commit-config.yaml`; grep over `LESSONS.md` + `scripts/` glob.
Phase 1 (reference): delegated to a bounded sub-agent (Customization track only) — returned a pattern catalog; lifecycle implementation skills skipped per cost rule.

*Deliberately NOT read:* reference lifecycle skills (backend/frontend/SQL/E2E/UI); any other repo (ADR-41); `OneDrive - Blue Yonder` (excluded).
